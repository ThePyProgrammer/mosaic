import pytest

from mosaic.core import FrameId
from mosaic.splats import GaussianSplat, SplatMap


def test_gaussian_splat_accepts_valid_upper_triangular_covariance() -> None:
    splat = GaussianSplat(
        center=(1.0, 2.0, 3.0),
        covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1),
        color_rgb=(0.2, 0.3, 0.4),
        opacity=0.75,
        provenance="front-camera",
    )

    assert splat.center == (1.0, 2.0, 3.0)
    assert splat.provenance == "front-camera"


def test_gaussian_splat_rejects_invalid_opacity() -> None:
    with pytest.raises(ValueError, match="opacity"):
        GaussianSplat(
            center=(0.0, 0.0, 0.0),
            covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1),
            opacity=1.5,
        )


def test_gaussian_splat_rejects_non_positive_covariance_diagonal() -> None:
    with pytest.raises(ValueError, match="covariance diagonal"):
        GaussianSplat(center=(0.0, 0.0, 0.0), covariance_upper=(0.0, 0.0, 0.0, 0.1, 0.0, 0.1))


def test_splat_map_appends_without_mutating_original() -> None:
    frame = FrameId("map")
    base = SplatMap(frame=frame)
    splat = GaussianSplat(center=(0.0, 0.0, 1.0), covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1))

    updated = base.with_splats((splat,))

    assert len(base) == 0
    assert len(updated) == 1
    assert updated.frame == frame
    assert updated.splats == (splat,)
