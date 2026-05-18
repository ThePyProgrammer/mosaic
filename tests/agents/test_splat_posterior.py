from mosaic.agents import LocalRadiusQuery, SplatPosteriorView
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

    assert result.splat_ids == (0, 1)
    assert result.count == 2


def test_summary_reports_count_provenance_and_mean_opacity() -> None:
    summary = SplatPosteriorView(_map()).summary()

    assert summary.splat_count == 3
    assert summary.provenance_count == 2
    assert summary.mean_opacity == 0.583333


def test_provenance_summary_counts_known_sources() -> None:
    provenance = SplatPosteriorView(_map()).provenance()

    assert provenance.counts == {"front": 2, "rear": 1}
