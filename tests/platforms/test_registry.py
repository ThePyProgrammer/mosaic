import pytest

from mosaic.core import CameraIntrinsics, FrameId, Pose3, Quaternion, Translation3
from mosaic.platforms import CameraMount, CameraRig, Embodiment, PlatformDescription, PlatformRegistry


def _platform(name: str) -> PlatformDescription:
    base_frame = FrameId("base_link")
    return PlatformDescription(
        name=name,
        embodiment=Embodiment.CUSTOM,
        base_frame=base_frame,
        camera_rig=CameraRig(
            frame=base_frame,
            cameras=(
                CameraMount(
                    camera_id="front",
                    pose=Pose3(
                        parent_frame=base_frame,
                        child_frame=FrameId("camera/front"),
                        translation=Translation3(),
                        rotation=Quaternion.identity(),
                    ),
                    intrinsics=CameraIntrinsics(width=640, height=480, fx=400.0, fy=400.0, cx=320.0, cy=240.0),
                ),
            ),
        ),
    )


def test_registry_registers_and_retrieves_platforms() -> None:
    platform = _platform("research-rig")
    registry = PlatformRegistry()

    registry.register(platform)

    assert registry.get("research-rig") == platform
    assert registry.names == ("research-rig",)


def test_registry_rejects_duplicate_names() -> None:
    registry = PlatformRegistry()
    registry.register(_platform("research-rig"))

    with pytest.raises(ValueError, match="already registered"):
        registry.register(_platform("research-rig"))


def test_registry_reports_missing_platforms() -> None:
    registry = PlatformRegistry()

    with pytest.raises(KeyError, match="missing"):
        registry.get("missing")
