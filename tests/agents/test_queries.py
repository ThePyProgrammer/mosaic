import pytest

from mosaic.agents import AgentQueryKind, LocalRadiusQuery, PosteriorSummary, ProvenanceSummary, SplatQueryResult


def test_local_radius_query_requires_positive_radius() -> None:
    with pytest.raises(ValueError, match="radius"):
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


def test_provenance_summary_freezes_counts() -> None:
    summary = ProvenanceSummary(counts={"front": 2})

    assert summary.counts["front"] == 2
    with pytest.raises(TypeError):
        summary.counts["rear"] = 1
