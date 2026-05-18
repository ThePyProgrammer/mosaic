import pytest

from mosaic.core import (
    CameraIntrinsics,
    CameraObservation,
    FrameId,
    ImageBuffer,
    ImageEncoding,
    MultiViewObservation,
    Pose3,
    Quaternion,
    Timestamp,
    Translation3,
)


def _pose(camera_frame: str) -> Pose3:
    return Pose3(
        parent_frame=FrameId("world"),
        child_frame=FrameId(camera_frame),
        translation=Translation3(),
        rotation=Quaternion.identity(),
    )


def _intrinsics() -> CameraIntrinsics:
    return CameraIntrinsics(width=640, height=480, fx=400.0, fy=401.0, cx=320.0, cy=240.0)


def _rgb(width: int = 2, height: int = 1) -> ImageBuffer:
    return ImageBuffer(
        width=width,
        height=height,
        channels=3,
        encoding=ImageEncoding.RGB8,
        data=b"\x00\x00\x00\xff\xff\xff",
    )


def test_camera_intrinsics_project_point() -> None:
    pixel = _intrinsics().project((1.0, 2.0, 4.0))

    assert pixel.u == 420.0
    assert pixel.v == 440.5


def test_camera_intrinsics_rejects_non_positive_depth_projection() -> None:
    with pytest.raises(ValueError, match="non-positive depth"):
        _intrinsics().project((0.0, 0.0, 0.0))


def test_image_buffer_validates_rgb_length() -> None:
    image = _rgb()

    assert image.data == b"\x00\x00\x00\xff\xff\xff"


def test_image_buffer_rejects_wrong_byte_length() -> None:
    with pytest.raises(ValueError, match="data length"):
        ImageBuffer(width=2, height=1, channels=3, encoding=ImageEncoding.RGB8, data=b"short")


def test_multi_view_observation_requires_matching_timestamps() -> None:
    first = CameraObservation(
        camera_id="front",
        timestamp=Timestamp.from_seconds(1.0),
        camera_pose=_pose("camera/front"),
        intrinsics=_intrinsics(),
        color=_rgb(),
    )
    second = CameraObservation(
        camera_id="rear",
        timestamp=Timestamp.from_seconds(2.0),
        camera_pose=_pose("camera/rear"),
        intrinsics=_intrinsics(),
        color=_rgb(),
    )

    with pytest.raises(ValueError, match="same timestamp"):
        MultiViewObservation(timestamp=Timestamp.from_seconds(1.0), views=(first, second))


def test_multi_view_observation_accepts_distinct_camera_ids() -> None:
    timestamp = Timestamp.from_seconds(3.0)
    observation = MultiViewObservation(
        timestamp=timestamp,
        views=(
            CameraObservation(
                camera_id="front",
                timestamp=timestamp,
                camera_pose=_pose("camera/front"),
                intrinsics=_intrinsics(),
                color=_rgb(),
            ),
            CameraObservation(
                camera_id="left",
                timestamp=timestamp,
                camera_pose=_pose("camera/left"),
                intrinsics=_intrinsics(),
                color=_rgb(),
            ),
        ),
    )

    assert observation.camera_ids == ("front", "left")
