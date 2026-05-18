import pytest

from mosaic.agents import (
    AgentQueryKind,
    LocalRadiusQuery,
    PosteriorSummary,
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


def test_local_radius_query_defaults_to_local_geometry_kind() -> None:
    query = LocalRadiusQuery(center=(1.0, 2.0, 3.0), radius=2.5)

    assert query.kind is AgentQueryKind.LOCAL_GEOMETRY
    assert query.center == (1.0, 2.0, 3.0)


def test_splat_query_result_reports_count() -> None:
    result = SplatQueryResult(query_kind=AgentQueryKind.LOCAL_GEOMETRY, splat_ids=(0, 2, 4))

    assert result.count == 3


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
    assert agents.LocalRadiusQuery is LocalRadiusQuery
    assert agents.PosteriorSummary is PosteriorSummary
    assert agents.ProvenanceSummary is ProvenanceSummary
    assert agents.SplatPosteriorView is SplatPosteriorView
    assert agents.SplatQueryResult is SplatQueryResult
    assert set(agents.__all__) >= {
        "AgentQueryKind",
        "LocalRadiusQuery",
        "PosteriorSummary",
        "ProvenanceSummary",
        "SplatPosteriorView",
        "SplatQueryResult",
    }
