import pytest

from mosaic.core import FrameId, Pose3, Quaternion, Timestamp, Translation3


def test_timestamp_from_seconds_uses_nanoseconds() -> None:
    timestamp = Timestamp.from_seconds(1.25)

    assert timestamp.nanoseconds == 1_250_000_000
    assert timestamp.as_seconds() == 1.25


def test_timestamp_from_seconds_rounds_fractional_nanoseconds() -> None:
    timestamp = Timestamp.from_seconds(0.0000000016)

    assert timestamp.nanoseconds == 2


def test_timestamp_artifact_payload_uses_canonical_integer_nanoseconds() -> None:
    timestamp = Timestamp.from_seconds(1.25)
    payload = {"nanoseconds": timestamp.nanoseconds}

    assert payload == {"nanoseconds": 1_250_000_000}
    assert isinstance(payload["nanoseconds"], int)
    assert "seconds" not in payload


def test_timestamp_rejects_negative_values() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        Timestamp(-1)


def test_timestamp_rejects_non_integer_nanoseconds() -> None:
    with pytest.raises(ValueError, match="integer"):
        Timestamp(1.5)  # type: ignore[arg-type]

    with pytest.raises(ValueError, match="integer"):
        Timestamp(True)  # type: ignore[arg-type]


def test_frame_id_rejects_blank_values() -> None:
    with pytest.raises(ValueError, match="FrameId"):
        FrameId("  ")


def test_translation_rejects_non_finite_coordinates() -> None:
    with pytest.raises(ValueError, match="finite"):
        Translation3(float("nan"), 0.0, 0.0)

    with pytest.raises(ValueError, match="finite"):
        Translation3(0.0, float("inf"), 0.0)


def test_pose_tracks_parent_and_child_frames() -> None:
    pose = Pose3(
        parent_frame=FrameId("world"),
        child_frame=FrameId("camera/front_optical"),
        translation=Translation3(1.0, 2.0, 3.0),
        rotation=Quaternion.identity(),
    )

    assert pose.parent_frame == FrameId("world")
    assert pose.child_frame == FrameId("camera/front_optical")
    assert pose.translation.as_tuple() == (1.0, 2.0, 3.0)
    assert pose.rotation.as_tuple() == (1.0, 0.0, 0.0, 0.0)


def test_pose_direction_maps_child_frame_points_into_parent_frame() -> None:
    pose = Pose3(
        parent_frame=FrameId("world"),
        child_frame=FrameId("camera/front_optical"),
        translation=Translation3(1.0, 2.0, 3.0),
        rotation=Quaternion.identity(),
    )

    assert pose.apply_to_point((0.0, 0.0, 0.0)) == (1.0, 2.0, 3.0)


def test_quaternion_rejects_non_unit_rotation() -> None:
    with pytest.raises(ValueError, match="unit length"):
        Quaternion(w=2.0, x=0.0, y=0.0, z=0.0)


def test_pose_inverse_maps_applied_point_back_to_child_frame() -> None:
    pose = Pose3(
        parent_frame=FrameId("world"),
        child_frame=FrameId("camera/front_optical"),
        translation=Translation3(1.0, 2.0, 3.0),
        rotation=Quaternion.identity(),
    )
    point = (0.25, 0.5, 4.0)

    assert pose.inverse().parent_frame == FrameId("camera/front_optical")
    assert pose.inverse().child_frame == FrameId("world")
    assert pose.inverse().apply_to_point(pose.apply_to_point(point)) == pytest.approx(point)


def test_pose_compose_connects_parent_to_child_frames() -> None:
    world_base = Pose3(
        parent_frame=FrameId("world"),
        child_frame=FrameId("base"),
        translation=Translation3(1.0, 0.0, 0.0),
        rotation=Quaternion.identity(),
    )
    base_camera = Pose3(
        parent_frame=FrameId("base"),
        child_frame=FrameId("camera/front_optical"),
        translation=Translation3(0.0, 2.0, 0.0),
        rotation=Quaternion.identity(),
    )

    world_camera = world_base.compose(base_camera)

    assert world_camera.parent_frame == FrameId("world")
    assert world_camera.child_frame == FrameId("camera/front_optical")
    assert world_camera.apply_to_point((0.0, 0.0, 0.0)) == pytest.approx((1.0, 2.0, 0.0))


def test_pose_compose_rejects_incompatible_frames() -> None:
    world_base = Pose3(parent_frame=FrameId("world"), child_frame=FrameId("base"))
    map_camera = Pose3(
        parent_frame=FrameId("map"),
        child_frame=FrameId("camera/front_optical"),
    )

    with pytest.raises(ValueError, match="incompatible frames"):
        world_base.compose(map_camera)


def test_pose_compose_applies_other_rotation_before_self_translation() -> None:
    world_base = Pose3(
        parent_frame=FrameId("world"),
        child_frame=FrameId("base"),
        translation=Translation3(1.0, 0.0, 0.0),
        rotation=Quaternion.identity(),
    )
    base_camera = Pose3(
        parent_frame=FrameId("base"),
        child_frame=FrameId("camera/front_optical"),
        translation=Translation3(0.0, 2.0, 0.0),
        rotation=Quaternion(w=0.7071067811865476, x=0.0, y=0.0, z=0.7071067811865476),
    )

    world_camera = world_base.compose(base_camera)

    assert world_camera.apply_to_point((1.0, 0.0, 0.0)) == pytest.approx((1.0, 3.0, 0.0))
