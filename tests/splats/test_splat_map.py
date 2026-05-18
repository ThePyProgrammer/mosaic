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


def test_gaussian_splat_rejects_non_finite_numeric_values() -> None:
    with pytest.raises(ValueError, match="finite"):
        GaussianSplat(center=(float("nan"), 0.0, 0.0), covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1))

    with pytest.raises(ValueError, match="finite"):
        GaussianSplat(center=(0.0, 0.0, 0.0), covariance_upper=(float("nan"), 0.0, 0.0, 0.1, 0.0, 0.1))

    with pytest.raises(ValueError, match="finite"):
        GaussianSplat(
            center=(0.0, 0.0, 0.0),
            covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1),
            color_rgb=(float("inf"), 0.0, 0.0),
        )

    with pytest.raises(ValueError, match="finite"):
        GaussianSplat(
            center=(0.0, 0.0, 0.0),
            covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1),
            opacity=float("nan"),
        )


def test_gaussian_splat_rejects_covariance_tuple_length_other_than_six() -> None:
    with pytest.raises(ValueError, match="six values"):
        GaussianSplat(
            center=(0.0, 0.0, 0.0),
            covariance_upper=(1.0, 0.0, 0.0, 1.0, 0.0),
        )


def test_gaussian_splat_rejects_non_positive_covariance_diagonal() -> None:
    with pytest.raises(ValueError, match="covariance diagonal"):
        GaussianSplat(center=(0.0, 0.0, 0.0), covariance_upper=(0.0, 0.0, 0.0, 0.1, 0.0, 0.1))

    with pytest.raises(ValueError, match="covariance diagonal"):
        GaussianSplat(center=(0.0, 0.0, 0.0), covariance_upper=(0.1, 0.0, 0.0, 0.0, 0.0, 0.1))

    with pytest.raises(ValueError, match="covariance diagonal"):
        GaussianSplat(center=(0.0, 0.0, 0.0), covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.0))


def test_gaussian_splat_coerces_mutable_sequence_inputs() -> None:
    center = [1.0, 2.0, 3.0]
    covariance_upper = [0.5, 0.0, 0.0, 0.5, 0.0, 0.5]
    color_rgb = [0.2, 0.3, 0.4]

    splat = GaussianSplat(center=center, covariance_upper=covariance_upper, color_rgb=color_rgb)

    center[0] = 9.0
    covariance_upper[0] = 9.0
    color_rgb[0] = 9.0

    assert splat.center == (1.0, 2.0, 3.0)
    assert splat.covariance_upper == (0.5, 0.0, 0.0, 0.5, 0.0, 0.5)
    assert splat.color_rgb == (0.2, 0.3, 0.4)
    assert isinstance(splat.center, tuple)
    assert isinstance(splat.covariance_upper, tuple)
    assert isinstance(splat.color_rgb, tuple)


def test_gaussian_splat_covariance_upper_reconstructs_symmetric_matrix() -> None:
    splat = GaussianSplat(
        center=(0.0, 0.0, 0.0),
        covariance_upper=(1.0, 0.2, 0.3, 2.0, 0.4, 3.0),
    )
    xx, xy, xz, yy, yz, zz = splat.covariance_upper

    covariance_matrix = (
        (xx, xy, xz),
        (xy, yy, yz),
        (xz, yz, zz),
    )

    assert covariance_matrix == (
        (1.0, 0.2, 0.3),
        (0.2, 2.0, 0.4),
        (0.3, 0.4, 3.0),
    )


def test_gaussian_splat_accepts_non_diagonal_positive_definite_covariance() -> None:
    covariance_upper = (1.0, 0.2, 0.3, 2.0, 0.4, 3.0)

    splat = GaussianSplat(center=(0.0, 0.0, 0.0), covariance_upper=covariance_upper)

    assert splat.covariance_upper == covariance_upper


def test_gaussian_splat_docstring_states_covariance_layout() -> None:
    assert GaussianSplat.__doc__ is not None
    assert "(xx, xy, xz, yy, yz, zz)" in GaussianSplat.__doc__


def test_gaussian_splat_rejects_non_positive_definite_covariance() -> None:
    with pytest.raises(ValueError, match="positive definite"):
        GaussianSplat(
            center=(0.0, 0.0, 0.0),
            covariance_upper=(1.0, 2.0, 0.0, 1.0, 0.0, 1.0),
        )


def test_gaussian_splat_rejects_zero_leading_2x2_covariance_minor() -> None:
    with pytest.raises(ValueError, match="positive definite"):
        GaussianSplat(
            center=(0.0, 0.0, 0.0),
            covariance_upper=(1.0, 1.0, 0.0, 1.0, 0.0, 1.0),
        )


def test_gaussian_splat_rejects_non_positive_3x3_covariance_determinant() -> None:
    with pytest.raises(ValueError, match="positive definite"):
        GaussianSplat(
            center=(0.0, 0.0, 0.0),
            covariance_upper=(1.0, 0.0, 1.0, 1.0, 1.0, 1.0),
        )


def test_gaussian_splat_rejects_too_large_off_diagonal_covariance() -> None:
    with pytest.raises(ValueError, match="positive definite"):
        GaussianSplat(
            center=(0.0, 0.0, 0.0),
            covariance_upper=(1.0, 1.5, 0.0, 1.0, 0.0, 1.0),
        )


def test_splat_map_appends_without_mutating_original() -> None:
    frame = FrameId("map")
    base = SplatMap(frame=frame)
    splat = GaussianSplat(center=(0.0, 0.0, 1.0), covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1))

    updated = base.with_splats((splat,))

    assert len(base) == 0
    assert len(updated) == 1
    assert updated.frame == frame
    assert updated.splats == (splat,)


def test_splat_map_freezes_mutable_input_sequence() -> None:
    frame = FrameId("map")
    splat = GaussianSplat(center=(0.0, 0.0, 1.0), covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1))
    splats = [splat]

    splat_map = SplatMap(frame=frame, splats=splats)
    splats.append(GaussianSplat(center=(0.0, 1.0, 0.0), covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1)))

    assert isinstance(splat_map.splats, tuple)
    assert len(splat_map) == 1
