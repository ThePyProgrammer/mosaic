import json

import pytest

from mosaic.artifacts import (
    camera_intrinsics_from_artifact,
    camera_intrinsics_to_artifact,
    camera_observation_from_artifact,
    camera_observation_to_artifact,
    frame_id_from_artifact,
    frame_id_to_artifact,
    image_buffer_from_artifact,
    image_buffer_to_artifact,
    make_artifact,
    multiview_observation_from_artifact,
    multiview_observation_to_artifact,
    pose3_from_artifact,
    pose3_to_artifact,
    quaternion_from_artifact,
    quaternion_to_artifact,
    require_artifact,
    timestamp_from_artifact,
    timestamp_to_artifact,
    translation3_from_artifact,
    translation3_to_artifact,
)
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


def _timestamp_artifact() -> dict[str, object]:
    return make_artifact("mosaic.timestamp", {"nanoseconds": 123})


def _pose(camera_frame: str = "camera/front_optical") -> Pose3:
    return Pose3(
        parent_frame=FrameId("world"),
        child_frame=FrameId(camera_frame),
        translation=Translation3(1.0, 2.0, 3.0),
        rotation=Quaternion.identity(),
    )


def _intrinsics() -> CameraIntrinsics:
    return CameraIntrinsics(width=640, height=480, fx=400.0, fy=401.0, cx=320.0, cy=240.0)


def _rgb() -> ImageBuffer:
    return ImageBuffer(
        width=2,
        height=1,
        channels=3,
        encoding=ImageEncoding.RGB8,
        data=b"\x00\x00\x00\xff\xff\xff",
    )


def _depth() -> ImageBuffer:
    return ImageBuffer(
        width=1,
        height=1,
        channels=1,
        encoding=ImageEncoding.DEPTH_F32,
        data=b"\x00\x00\x80?",
    )


def _observation(camera_id: str = "front") -> CameraObservation:
    return CameraObservation(
        camera_id=camera_id,
        timestamp=Timestamp(1_250_000_000),
        camera_pose=_pose(f"camera/{camera_id}_optical"),
        intrinsics=_intrinsics(),
        color=_rgb(),
        depth=_depth(),
        metadata={"source": "fixture"},
    )


def _assert_json_ready(artifact: dict[str, object]) -> None:
    json.dumps(artifact, sort_keys=True)


def test_make_artifact_creates_versioned_envelope() -> None:
    assert _timestamp_artifact() == {
        "schema": "mosaic.timestamp",
        "schema_version": 1,
        "payload": {"nanoseconds": 123},
    }


def test_require_artifact_returns_payload_for_expected_schema() -> None:
    assert require_artifact(_timestamp_artifact(), "mosaic.timestamp") == {"nanoseconds": 123}


def test_require_artifact_rejects_unknown_schema() -> None:
    with pytest.raises(ValueError, match="schema"):
        require_artifact(_timestamp_artifact(), "mosaic.pose3")


def test_require_artifact_rejects_unknown_schema_version() -> None:
    artifact = _timestamp_artifact()
    artifact["schema_version"] = 2

    with pytest.raises(ValueError, match="schema_version"):
        require_artifact(artifact, "mosaic.timestamp")


def test_timestamp_artifact_round_trips_nanoseconds_without_seconds() -> None:
    timestamp = Timestamp(1_250_000_000)
    artifact = timestamp_to_artifact(timestamp)

    _assert_json_ready(artifact)
    assert artifact["schema"] == "mosaic.timestamp"
    assert require_artifact(artifact, "mosaic.timestamp") == {"nanoseconds": 1_250_000_000}
    assert "seconds" not in require_artifact(artifact, "mosaic.timestamp")
    assert timestamp_from_artifact(artifact) == timestamp


def test_frame_id_artifact_round_trips() -> None:
    frame = FrameId("camera/front_optical")
    artifact = frame_id_to_artifact(frame)

    _assert_json_ready(artifact)
    assert frame_id_from_artifact(artifact) == frame


def test_translation_artifact_preserves_xyz_order() -> None:
    translation = Translation3(1.0, 2.0, 3.0)
    artifact = translation3_to_artifact(translation)

    _assert_json_ready(artifact)
    assert require_artifact(artifact, "mosaic.translation3")["xyz"] == [1.0, 2.0, 3.0]
    assert translation3_from_artifact(artifact) == translation


def test_quaternion_artifact_preserves_wxyz_order() -> None:
    quaternion = Quaternion.identity()
    artifact = quaternion_to_artifact(quaternion)

    _assert_json_ready(artifact)
    assert require_artifact(artifact, "mosaic.quaternion")["wxyz"] == [1.0, 0.0, 0.0, 0.0]
    assert quaternion_from_artifact(artifact) == quaternion


def test_pose_artifact_round_trips_parent_child_direction() -> None:
    pose = _pose()
    artifact = pose3_to_artifact(pose)
    payload = require_artifact(artifact, "mosaic.pose3")

    _assert_json_ready(artifact)
    assert payload["parent_frame"] == "world"
    assert payload["child_frame"] == "camera/front_optical"
    assert payload["translation"] == [1.0, 2.0, 3.0]
    assert payload["rotation_wxyz"] == [1.0, 0.0, 0.0, 0.0]
    assert pose3_from_artifact(artifact) == pose


def test_camera_intrinsics_artifact_round_trips() -> None:
    intrinsics = _intrinsics()
    artifact = camera_intrinsics_to_artifact(intrinsics)

    _assert_json_ready(artifact)
    assert camera_intrinsics_from_artifact(artifact) == intrinsics


def test_image_buffer_artifact_uses_base64_and_preserves_bytes() -> None:
    image = _rgb()
    artifact = image_buffer_to_artifact(image)
    payload = require_artifact(artifact, "mosaic.image_buffer")

    _assert_json_ready(artifact)
    assert payload["data_encoding"] == "base64"
    assert image_buffer_from_artifact(artifact) == image


def test_image_buffer_artifact_rejects_unknown_data_encoding() -> None:
    artifact = image_buffer_to_artifact(_rgb())
    payload = require_artifact(artifact, "mosaic.image_buffer")
    payload["data_encoding"] = "hex"
    artifact["payload"] = payload

    with pytest.raises(ValueError, match="data_encoding"):
        image_buffer_from_artifact(artifact)


def test_camera_observation_artifact_round_trips() -> None:
    observation = _observation()
    artifact = camera_observation_to_artifact(observation)

    _assert_json_ready(artifact)
    assert camera_observation_from_artifact(artifact) == observation


def test_multiview_observation_artifact_round_trips_camera_ids_and_views() -> None:
    first = _observation("front")
    second = _observation("rear")
    multiview = MultiViewObservation(timestamp=Timestamp(1_250_000_000), views=(first, second))
    artifact = multiview_observation_to_artifact(multiview)
    payload = require_artifact(artifact, "mosaic.multiview_observation")

    _assert_json_ready(artifact)
    assert payload["camera_ids"] == ["front", "rear"]
    assert multiview_observation_from_artifact(artifact) == multiview
