from mosaic.core import FrameId
from mosaic.platforms import Embodiment, default_platform_registry, humanoid_stereo_rig, quadruped_front_rig, ugv_surround_rig


def test_quadruped_front_rig_uses_quadruped_embodiment() -> None:
    platform = quadruped_front_rig()

    assert platform.name == "quadruped-front"
    assert platform.embodiment is Embodiment.QUADRUPED
    assert platform.base_frame == FrameId("base_link")
    assert platform.camera_rig.camera_ids == ("front",)


def test_ugv_surround_rig_has_four_ordered_cameras() -> None:
    platform = ugv_surround_rig()

    assert platform.name == "ugv-surround"
    assert platform.embodiment is Embodiment.UGV
    assert platform.camera_rig.camera_ids == ("front", "left", "right", "rear")


def test_humanoid_stereo_rig_has_head_stereo_cameras() -> None:
    platform = humanoid_stereo_rig()

    assert platform.name == "humanoid-stereo"
    assert platform.embodiment is Embodiment.HUMANOID
    assert platform.camera_rig.camera_ids == ("left_eye", "right_eye")


def test_default_registry_contains_built_in_presets() -> None:
    registry = default_platform_registry()

    assert registry.names == ("humanoid-stereo", "quadruped-front", "ugv-surround")
    assert registry.get("ugv-surround").camera_rig.camera_ids == ("front", "left", "right", "rear")
