from math import inf, nan

import pytest

from mosaic.agents import (
    AgentQueryKind,
    LocalRadiusQuery,
    PosteriorSummary,
    PosteriorUncertaintySummary,
    ProvenanceSummary,
    SplatPosteriorView,
    SplatQueryResult,
)


def test_local_radius_query_requires_three_coordinates() -> None:
    with pytest.raises(ValueError, match="three coordinates"):
        LocalRadiusQuery(center=(0.0, 0.0), radius=1.0)  # type: ignore[arg-type]


def test_local_radius_query_requires_positive_radius() -> None:
    with pytest.raises(ValueError, match="positive"):
        LocalRadiusQuery(center=(0.0, 0.0, 0.0), radius=0.0)


@pytest.mark.parametrize("value", [nan, inf, -inf])
def test_local_radius_query_rejects_non_finite_center_coordinates(value: float) -> None:
    with pytest.raises(ValueError, match="center coordinates must be finite"):
        LocalRadiusQuery(center=(value, 0.0, 0.0), radius=1.0)


@pytest.mark.parametrize("value", [nan, inf, -inf])
def test_local_radius_query_rejects_non_finite_radius(value: float) -> None:
    with pytest.raises(ValueError, match="radius must be finite and positive"):
        LocalRadiusQuery(center=(0.0, 0.0, 0.0), radius=value)


def test_local_radius_query_rejects_non_local_geometry_kind() -> None:
    with pytest.raises(ValueError, match="kind must be local_geometry"):
        LocalRadiusQuery(
            center=(0.0, 0.0, 0.0),
            radius=1.0,
            kind=AgentQueryKind.UNCERTAINTY,
        )


def test_local_radius_query_defaults_to_local_geometry_kind() -> None:
    query = LocalRadiusQuery(center=(1.0, 2.0, 3.0), radius=2.5)

    assert query.kind is AgentQueryKind.LOCAL_GEOMETRY
    assert query.center == (1.0, 2.0, 3.0)


def test_local_radius_query_defaults_to_bounded_results() -> None:
    query = LocalRadiusQuery(center=(1.0, 2.0, 3.0), radius=2.5)

    assert query.max_results == 32


def test_local_radius_query_rejects_non_positive_max_results() -> None:
    with pytest.raises(ValueError, match="max_results must be positive"):
        LocalRadiusQuery(center=(0.0, 0.0, 0.0), radius=1.0, max_results=0)
    with pytest.raises(ValueError, match="max_results must be positive"):
        LocalRadiusQuery(center=(0.0, 0.0, 0.0), radius=1.0, max_results=-1)


def test_agent_query_kind_includes_uncertainty() -> None:
    assert AgentQueryKind.UNCERTAINTY.value == "uncertainty"


def test_splat_query_result_reports_count() -> None:
    result = SplatQueryResult(query_kind=AgentQueryKind.LOCAL_GEOMETRY, splat_ids=(0, 2, 4))

    assert result.count == 3
    assert result.total_matches == 3
    assert result.truncated is False


def test_splat_query_result_validates_total_matches_and_truncation() -> None:
    with pytest.raises(ValueError, match="total_matches must cover returned splat_ids"):
        SplatQueryResult(
            query_kind=AgentQueryKind.LOCAL_GEOMETRY,
            splat_ids=(0, 1),
            total_matches=1,
        )
    with pytest.raises(ValueError, match="truncated must equal"):
        SplatQueryResult(
            query_kind=AgentQueryKind.LOCAL_GEOMETRY,
            splat_ids=(0, 1),
            total_matches=3,
            truncated=False,
        )
    with pytest.raises(ValueError, match="truncated must equal"):
        SplatQueryResult(
            query_kind=AgentQueryKind.LOCAL_GEOMETRY,
            splat_ids=(0, 1),
            total_matches=2,
            truncated=True,
        )


def test_posterior_summary_rejects_negative_counts() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        PosteriorSummary(splat_count=-1, provenance_count=0, mean_opacity=0.0)
    with pytest.raises(ValueError, match="non-negative"):
        PosteriorSummary(splat_count=0, provenance_count=-1, mean_opacity=0.0)


def test_posterior_summary_rejects_mean_opacity_outside_unit_interval() -> None:
    with pytest.raises(ValueError, match="between 0 and 1"):
        PosteriorSummary(splat_count=1, provenance_count=1, mean_opacity=-0.1)
    with pytest.raises(ValueError, match="between 0 and 1"):
        PosteriorSummary(splat_count=1, provenance_count=1, mean_opacity=1.1)


def test_posterior_uncertainty_summary_validates_descriptive_statistics() -> None:
    summary = PosteriorUncertaintySummary(
        splat_count=3,
        mean_covariance_diagonal=(0.2, 0.2, 0.2),
        max_covariance_diagonal=(0.3, 0.3, 0.3),
        mean_opacity=0.583333,
        min_opacity=0.25,
        max_opacity=1.0,
    )

    assert summary.semantics == "descriptive_only"


@pytest.mark.parametrize(
    "kwargs, message",
    [
        ({"splat_count": -1}, "splat_count must be non-negative"),
        ({"semantics": "calibrated"}, "semantics must be descriptive_only"),
        ({"mean_covariance_diagonal": (0.1, 0.2)}, "three values"),
        ({"max_covariance_diagonal": (0.1, 0.2)}, "three values"),
        ({"mean_covariance_diagonal": (-0.1, 0.0, 0.0)}, "non-negative"),
        ({"max_covariance_diagonal": (0.1, -0.2, 0.0)}, "non-negative"),
        ({"mean_opacity": -0.1}, "between 0 and 1"),
        ({"min_opacity": -0.1}, "between 0 and 1"),
        ({"max_opacity": 1.1}, "between 0 and 1"),
        ({"min_opacity": 0.6, "mean_opacity": 0.5}, "opacity values must satisfy"),
        ({"mean_opacity": 0.8, "max_opacity": 0.7}, "opacity values must satisfy"),
        (
            {"mean_covariance_diagonal": (0.4, 0.2, 0.2)},
            "mean_covariance_diagonal <= max_covariance_diagonal",
        ),
    ],
)
def test_posterior_uncertainty_summary_rejects_invalid_values(
    kwargs: dict[str, object], message: str
) -> None:
    values: dict[str, object] = {
        "splat_count": 3,
        "mean_covariance_diagonal": (0.2, 0.2, 0.2),
        "max_covariance_diagonal": (0.3, 0.3, 0.3),
        "mean_opacity": 0.583333,
        "min_opacity": 0.25,
        "max_opacity": 1.0,
    }
    values.update(kwargs)

    with pytest.raises(ValueError, match=message):
        PosteriorUncertaintySummary(**values)  # type: ignore[arg-type]


def test_provenance_summary_rejects_blank_sources_and_negative_counts() -> None:
    with pytest.raises(ValueError, match="must not be blank"):
        ProvenanceSummary(counts={" ": 1})
    with pytest.raises(ValueError, match="non-negative"):
        ProvenanceSummary(counts={"front": -1})


def test_provenance_summary_freezes_and_copies_counts() -> None:
    counts = {"front": 2}
    summary = ProvenanceSummary(counts=counts)
    counts["front"] = 99

    assert summary.counts["front"] == 2
    with pytest.raises(TypeError):
        summary.counts["rear"] = 1


def test_agents_exports_public_query_and_result_types() -> None:
    import mosaic.agents as agents

    assert agents.AgentQueryKind is AgentQueryKind
    assert agents.AgentQueryKind.UNCERTAINTY is AgentQueryKind.UNCERTAINTY
    assert agents.LocalRadiusQuery is LocalRadiusQuery
    assert agents.PosteriorSummary is PosteriorSummary
    assert agents.PosteriorUncertaintySummary is PosteriorUncertaintySummary
    assert agents.ProvenanceSummary is ProvenanceSummary
    assert agents.SplatPosteriorView is SplatPosteriorView
    assert agents.SplatQueryResult is SplatQueryResult
    assert "PosteriorUncertaintySummary" in agents.__all__
    assert set(agents.__all__) >= {
        "AgentQueryKind",
        "LocalRadiusQuery",
        "PosteriorSummary",
        "PosteriorUncertaintySummary",
        "ProvenanceSummary",
        "SplatPosteriorView",
        "SplatQueryResult",
    }
