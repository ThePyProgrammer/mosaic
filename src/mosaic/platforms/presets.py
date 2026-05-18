from __future__ import annotations

from mosaic.core import CameraIntrinsics, FrameId, Pose3, Quaternion, Translation3
from mosaic.platforms.registry import PlatformRegistry
from mosaic.platforms.types import CameraMount, CameraRig, Embodiment, PlatformDescription


def _intrinsics(width: int = 640, height: int = 480) -> CameraIntrinsics:
    return CameraIntrinsics(width=width, height=height, fx=400.0, fy=400.0, cx=width / 2.0, cy=height / 2.0)


def _mount(camera_id: str, x: float, y: float, z: float) -> CameraMount:
    base_frame = FrameId("base_link")
    return CameraMount(
        camera_id=camera_id,
        pose=Pose3(
            parent_frame=base_frame,
            child_frame=FrameId(f"camera/{camera_id}"),
            translation=Translation3(x=x, y=y, z=z),
            rotation=Quaternion.identity(),
        ),
        intrinsics=_intrinsics(),
    )


def quadruped_front_rig() -> PlatformDescription:
    base_frame = FrameId("base_link")
    return PlatformDescription(
        name="quadruped-front",
        embodiment=Embodiment.QUADRUPED,
        base_frame=base_frame,
        camera_rig=CameraRig(frame=base_frame, cameras=(_mount("front", 0.30, 0.0, 0.35),)),
    )


def ugv_surround_rig() -> PlatformDescription:
    base_frame = FrameId("base_link")
    return PlatformDescription(
        name="ugv-surround",
        embodiment=Embodiment.UGV,
        base_frame=base_frame,
        camera_rig=CameraRig(
            frame=base_frame,
            cameras=(
                _mount("front", 0.45, 0.0, 0.55),
                _mount("left", 0.0, 0.35, 0.55),
                _mount("right", 0.0, -0.35, 0.55),
                _mount("rear", -0.45, 0.0, 0.55),
            ),
        ),
    )


def humanoid_stereo_rig() -> PlatformDescription:
    base_frame = FrameId("base_link")
    return PlatformDescription(
        name="humanoid-stereo",
        embodiment=Embodiment.HUMANOID,
        base_frame=base_frame,
        camera_rig=CameraRig(
            frame=base_frame,
            cameras=(
                _mount("left_eye", 0.08, 0.04, 1.55),
                _mount("right_eye", 0.08, -0.04, 1.55),
            ),
        ),
    )


def default_platform_registry() -> PlatformRegistry:
    registry = PlatformRegistry()
    registry.register(quadruped_front_rig())
    registry.register(ugv_surround_rig())
    registry.register(humanoid_stereo_rig())
    return registry
