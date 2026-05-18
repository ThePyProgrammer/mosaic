import pytest

from mosaic.core import CameraIntrinsics, FrameId, Pose3, Quaternion, Translation3
from mosaic.platforms import CameraMount, CameraRig, Embodiment, PlatformDescription


def _intrinsics() -> CameraIntrinsics:
    return CameraIntrinsics(width=640, height=480, fx=400.0, fy=400.0, cx=320.0, cy=240.0)


def _pose(child_frame: str) -> Pose3:
    return Pose3(
        parent_frame=FrameId("base_link"),
        child_frame=FrameId(child_frame),
        translation=Translation3(),
        rotation=Quaternion.identity(),
    )


def test_camera_rig_exposes_camera_ids_in_order() -> None:
    rig = CameraRig(
        frame=FrameId("base_link"),
        cameras=(
            CameraMount(camera_id="front", pose=_pose("camera/front"), intrinsics=_intrinsics()),
            CameraMount(camera_id="left", pose=_pose("camera/left"), intrinsics=_intrinsics()),
        ),
    )

    assert rig.camera_ids == ("front", "left")
    assert rig.camera("left").pose.child_frame == FrameId("camera/left")


def test_camera_rig_rejects_duplicate_camera_ids() -> None:
    with pytest.raises(ValueError, match="unique"):
        CameraRig(
            frame=FrameId("base_link"),
            cameras=(
                CameraMount(camera_id="front", pose=_pose("camera/front"), intrinsics=_intrinsics()),
                CameraMount(camera_id="front", pose=_pose("camera/front2"), intrinsics=_intrinsics()),
            ),
        )


def test_camera_mount_pose_must_attach_to_rig_frame() -> None:
    with pytest.raises(ValueError, match="parent frame"):
        CameraRig(
            frame=FrameId("base_link"),
            cameras=(
                CameraMount(
                    camera_id="front",
                    pose=Pose3(
                        parent_frame=FrameId("world"),
                        child_frame=FrameId("camera/front"),
                        translation=Translation3(),
                        rotation=Quaternion.identity(),
                    ),
                    intrinsics=_intrinsics(),
                ),
            ),
        )


def test_platform_description_keeps_embodiment_metadata_separate_from_rig() -> None:
    platform = PlatformDescription(
        name="custom-quad",
        embodiment=Embodiment.QUADRUPED,
        base_frame=FrameId("base_link"),
        camera_rig=CameraRig(
            frame=FrameId("base_link"),
            cameras=(CameraMount(camera_id="front", pose=_pose("camera/front"), intrinsics=_intrinsics()),),
        ),
        metadata={"vendor": "research"},
    )

    assert platform.name == "custom-quad"
    assert platform.embodiment is Embodiment.QUADRUPED
    assert platform.camera_rig.camera_ids == ("front",)
    assert platform.metadata["vendor"] == "research"
