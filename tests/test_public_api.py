from mosaic import (
    CameraIntrinsics,
    CameraRig,
    DeterministicSplatBackend,
    Embodiment,
    FrameId,
    FusionInput,
    GaussianSplat,
    InMemorySequence,
    PlatformRegistry,
    ProvenancePreservingFusion,
    SplatMap,
    Timestamp,
    TrackingState,
    quadruped_front_rig,
)


def test_public_api_exports_core_foundation_types() -> None:
    assert Timestamp.from_seconds(0.5).nanoseconds == 500_000_000
    assert FrameId("map").value == "map"
    assert CameraIntrinsics(width=1, height=1, fx=1.0, fy=1.0, cx=0.5, cy=0.5).width == 1
    assert GaussianSplat(center=(0.0, 0.0, 1.0), covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1)).opacity == 1.0
    assert len(SplatMap(frame=FrameId("map"))) == 0
    assert DeterministicSplatBackend().name == "deterministic-splat"
    assert TrackingState.TRACKING.value == "tracking"
    assert InMemorySequence.__name__ == "InMemorySequence"


def test_public_api_exports_platform_types() -> None:
    platform = quadruped_front_rig()

    assert platform.embodiment is Embodiment.QUADRUPED
    assert isinstance(platform.camera_rig, CameraRig)
    assert PlatformRegistry.__name__ == "PlatformRegistry"


def test_public_api_exports_fusion_types() -> None:
    assert FusionInput.__name__ == "FusionInput"
    assert ProvenancePreservingFusion().name == "provenance-preserving"
