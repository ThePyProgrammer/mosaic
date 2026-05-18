from __future__ import annotations

from dataclasses import dataclass

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
from mosaic.datasets import InMemorySequence


@dataclass(frozen=True, slots=True)
class SyntheticScenario:
    name: str
    sequence: InMemorySequence

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("SyntheticScenario name must not be blank")


def synthetic_forward_sequence(frame_count: int) -> SyntheticScenario:
    if frame_count <= 0:
        raise ValueError("synthetic_forward_sequence frame_count must be positive")
    observations = tuple(_observation(index) for index in range(frame_count))
    return SyntheticScenario(name=f"synthetic-forward-{frame_count}", sequence=InMemorySequence(observations))


def _observation(index: int) -> MultiViewObservation:
    timestamp = Timestamp(index * 100_000_000)
    image = ImageBuffer(width=1, height=1, channels=3, encoding=ImageEncoding.RGB8, data=b"\xff\xff\xff")
    return MultiViewObservation(
        timestamp=timestamp,
        views=(
            CameraObservation(
                camera_id="front",
                timestamp=timestamp,
                camera_pose=Pose3(
                    parent_frame=FrameId("world"),
                    child_frame=FrameId("camera/front"),
                    translation=Translation3(x=float(index), y=0.0, z=0.0),
                    rotation=Quaternion.identity(),
                ),
                intrinsics=CameraIntrinsics(width=1, height=1, fx=1.0, fy=1.0, cx=0.5, cy=0.5),
                color=image,
            ),
        ),
    )
