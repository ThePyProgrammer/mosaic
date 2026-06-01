import pytest
from pytest import approx

from mosaic.core import FrameId, Pose3, Quaternion, Translation3
from mosaic.fusion import COVARIANCE_TRANSFORM_MODEL, transform_splat_map
from mosaic.splats import GaussianSplat, SplatMap


def _splat(
    *,
    center: tuple[float, float, float] = (1.0, 2.0, 3.0),
    covariance_upper: tuple[float, float, float, float, float, float] = (
        0.2,
        0.0,
        0.0,
        0.3,
        0.0,
        0.4,
    ),
    color_rgb: tuple[float, float, float] = (0.25, 0.5, 0.75),
    opacity: float = 0.6,
    provenance: str | None = "front",
) -> GaussianSplat:
    return GaussianSplat(
        center=center,
        covariance_upper=covariance_upper,
        color_rgb=color_rgb,
        opacity=opacity,
        provenance=provenance,
    )


def test_transform_splat_map_transforms_centers_into_target_frame() -> None:
    source_frame = FrameId("sensor")
    target_frame = FrameId("map")
    splat_map = SplatMap(frame=source_frame, splats=(_splat(center=(1.0, 2.0, 3.0)),))
    transform = Pose3(
        parent_frame=target_frame,
        child_frame=source_frame,
        translation=Translation3(x=10.0, y=20.0, z=30.0),
        rotation=Quaternion.identity(),
    )

    transformed = transform_splat_map(splat_map, transform, frame=target_frame)

    assert COVARIANCE_TRANSFORM_MODEL == "center_only_reference"
    assert transformed.frame == target_frame
    assert transformed.splats[0].center == approx((11.0, 22.0, 33.0))


def test_transform_splat_map_preserves_splat_attributes_and_provenance() -> None:
    source_frame = FrameId("sensor")
    target_frame = FrameId("map")
    covariance_upper = (0.5, 0.1, 0.0, 0.6, 0.0, 0.7)
    color_rgb = (0.1, 0.2, 0.3)
    splat = _splat(
        center=(0.0, 1.0, 0.0),
        covariance_upper=covariance_upper,
        color_rgb=color_rgb,
        opacity=0.4,
        provenance="camera-left",
    )
    splat_map = SplatMap(frame=source_frame, splats=(splat,))
    transform = Pose3(
        parent_frame=target_frame,
        child_frame=source_frame,
        translation=Translation3(),
        rotation=Quaternion(w=0.0, x=0.0, y=0.0, z=1.0),
    )

    transformed_splat = transform_splat_map(splat_map, transform, frame=target_frame).splats[0]

    assert transformed_splat.center == approx((0.0, -1.0, 0.0))
    assert transformed_splat.covariance_upper == covariance_upper
    assert transformed_splat.color_rgb == color_rgb
    assert transformed_splat.opacity == approx(0.4)
    assert transformed_splat.provenance == "camera-left"


def test_transform_splat_map_prefixes_provenance_and_unknown_values() -> None:
    source_frame = FrameId("sensor")
    target_frame = FrameId("map")
    splat_map = SplatMap(
        frame=source_frame,
        splats=(
            _splat(center=(0.0, 0.0, 0.0), provenance="front"),
            _splat(center=(1.0, 0.0, 0.0), provenance=None),
            _splat(center=(2.0, 0.0, 0.0), provenance=" "),
        ),
    )
    transform = Pose3(parent_frame=target_frame, child_frame=source_frame)

    transformed = transform_splat_map(
        splat_map,
        transform,
        frame=target_frame,
        provenance_prefix="session-a",
    )

    assert [splat.provenance for splat in transformed.splats] == [
        "session-a:front",
        "session-a:unknown",
        "session-a:unknown",
    ]


def test_transform_splat_map_validates_child_frame_matches_source_map() -> None:
    source_frame = FrameId("sensor")
    target_frame = FrameId("map")
    splat_map = SplatMap(frame=source_frame, splats=(_splat(),))
    transform = Pose3(parent_frame=target_frame, child_frame=FrameId("other-sensor"))

    with pytest.raises(ValueError, match="transform child_frame must match splat_map frame"):
        transform_splat_map(splat_map, transform, frame=target_frame)


def test_transform_splat_map_validates_parent_frame_matches_target_frame() -> None:
    source_frame = FrameId("sensor")
    target_frame = FrameId("map")
    splat_map = SplatMap(frame=source_frame, splats=(_splat(),))
    transform = Pose3(parent_frame=FrameId("world"), child_frame=source_frame)

    with pytest.raises(ValueError, match="transform parent_frame must match target frame"):
        transform_splat_map(splat_map, transform, frame=target_frame)
