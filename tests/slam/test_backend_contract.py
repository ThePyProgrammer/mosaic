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
from mosaic.slam import DeterministicSplatBackend, TrackingState


def _observation(seconds: float = 1.0) -> MultiViewObservation:
    timestamp = Timestamp.from_seconds(seconds)
    return MultiViewObservation(
        timestamp=timestamp,
        views=(
            CameraObservation(
                camera_id="front",
                timestamp=timestamp,
                camera_pose=Pose3(
                    parent_frame=FrameId("world"),
                    child_frame=FrameId("camera/front"),
                    translation=Translation3(x=1.0, y=0.0, z=0.0),
                    rotation=Quaternion.identity(),
                ),
                intrinsics=CameraIntrinsics(width=1, height=1, fx=1.0, fy=1.0, cx=0.5, cy=0.5),
                color=ImageBuffer(width=1, height=1, channels=3, encoding=ImageEncoding.RGB8, data=b"\xff\xff\xff"),
            ),
        ),
    )


def test_deterministic_backend_processes_observation_into_splat_update() -> None:
    backend = DeterministicSplatBackend(map_frame=FrameId("map"))

    update = backend.process(_observation())

    assert backend.name == "deterministic-splat"
    assert update.tracking_state is TrackingState.TRACKING
    assert update.estimated_pose == _observation().views[0].camera_pose
    assert len(update.map_update) == 1
    assert update.diagnostics["splat_count"] == 1


def test_deterministic_backend_snapshot_accumulates_processed_splats() -> None:
    backend = DeterministicSplatBackend(map_frame=FrameId("map"))

    backend.process(_observation(1.0))
    backend.process(_observation(2.0))

    snapshot = backend.snapshot()

    assert snapshot.frame == FrameId("map")
    assert len(snapshot) == 2
    assert snapshot.splats[0].center == (0.0, 0.0, 1.0)
    assert snapshot.splats[1].center == (1.0, 0.0, 1.0)


def test_deterministic_backend_reset_clears_state() -> None:
    backend = DeterministicSplatBackend(map_frame=FrameId("map"))
    backend.process(_observation())

    backend.reset()

    assert len(backend.snapshot()) == 0
