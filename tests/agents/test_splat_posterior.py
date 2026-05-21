from pathlib import Path

from mosaic.agents import AgentQueryKind, LocalRadiusQuery, SplatPosteriorView
from mosaic.core import FrameId
from mosaic.splats import GaussianSplat, SplatMap


def _map() -> SplatMap:
    return SplatMap(
        frame=FrameId("map"),
        splats=(
            GaussianSplat(
                center=(0.0, 0.0, 0.0),
                covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1),
                opacity=0.5,
                provenance="front",
            ),
            GaussianSplat(
                center=(1.0, 0.0, 0.0),
                covariance_upper=(0.2, 0.0, 0.0, 0.2, 0.0, 0.2),
                opacity=1.0,
                provenance="front",
            ),
            GaussianSplat(
                center=(5.0, 0.0, 0.0),
                covariance_upper=(0.3, 0.0, 0.0, 0.3, 0.0, 0.3),
                opacity=0.25,
                provenance="rear",
            ),
        ),
    )


def test_local_radius_query_returns_splat_indices_inside_radius() -> None:
    view = SplatPosteriorView(_map())

    result = view.query_local(LocalRadiusQuery(center=(0.0, 0.0, 0.0), radius=1.1))

    assert result.query_kind is AgentQueryKind.LOCAL_GEOMETRY
    assert result.splat_ids == (0, 1)
    assert result.count == 2
    assert result.total_matches == 2
    assert result.truncated is False


def test_local_radius_query_returns_bounded_tuple_order_results() -> None:
    view = SplatPosteriorView(_map())

    result = view.query_local(
        LocalRadiusQuery(center=(0.0, 0.0, 0.0), radius=10.0, max_results=2)
    )

    assert result.query_kind is AgentQueryKind.LOCAL_GEOMETRY
    assert result.splat_ids == (0, 1)
    assert result.count == 2
    assert result.total_matches == 3
    assert result.truncated is True


def test_summary_reports_count_provenance_and_mean_opacity() -> None:
    summary = SplatPosteriorView(_map()).summary()

    assert summary.splat_count == 3
    assert summary.provenance_count == 2
    assert summary.mean_opacity == 0.583333


def test_provenance_summary_counts_known_sources() -> None:
    provenance = SplatPosteriorView(_map()).provenance()

    assert provenance.counts == {"front": 2, "rear": 1}


def test_uncertainty_returns_global_descriptive_statistics() -> None:
    uncertainty = SplatPosteriorView(_map()).uncertainty()

    assert uncertainty.semantics == "descriptive_only"
    assert uncertainty.splat_count == 3
    assert uncertainty.mean_covariance_diagonal == (0.2, 0.2, 0.2)
    assert uncertainty.max_covariance_diagonal == (0.3, 0.3, 0.3)
    assert uncertainty.mean_opacity == 0.583333
    assert uncertainty.min_opacity == 0.25
    assert uncertainty.max_opacity == 1.0


def test_agent_posterior_boundary_stays_provider_free() -> None:
    pyproject = Path("pyproject.toml").read_text()
    posteriors_source = Path("src/mosaic/agents/posteriors.py").read_text()

    assert "dependencies = []" in pyproject
    assert all(
        forbidden not in posteriors_source
        for forbidden in (
            "openai",
            "anthropic",
            "langchain",
            "rospy",
            "rclpy",
            "habitat",
            "torch",
            "cv2",
        )
    )
