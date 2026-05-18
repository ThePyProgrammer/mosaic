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
from mosaic.datasets import InMemorySequence


def _observation(seconds: float) -> MultiViewObservation:
    timestamp = Timestamp.from_seconds(seconds)
    image = ImageBuffer(width=1, height=1, channels=3, encoding=ImageEncoding.RGB8, data=b"\x00\x00\x00")
    return MultiViewObservation(
        timestamp=timestamp,
        views=(
            CameraObservation(
                camera_id="front",
                timestamp=timestamp,
                camera_pose=Pose3(
                    parent_frame=FrameId("world"),
                    child_frame=FrameId("camera/front"),
                    translation=Translation3(),
                    rotation=Quaternion.identity(),
                ),
                intrinsics=CameraIntrinsics(width=1, height=1, fx=1.0, fy=1.0, cx=0.5, cy=0.5),
                color=image,
            ),
        ),
    )


def test_in_memory_sequence_replays_observations_in_order() -> None:
    first = _observation(1.0)
    second = _observation(2.0)
    sequence = InMemorySequence((first, second))

    assert list(sequence) == [first, second]
    assert len(sequence) == 2


def test_in_memory_sequence_freezes_list_inputs() -> None:
    first = _observation(1.0)
    second = _observation(2.0)
    observations = [first, second]

    sequence = InMemorySequence(observations)
    observations.append(_observation(3.0))

    assert len(sequence) == 2
    assert isinstance(sequence.observations, tuple)
    assert list(sequence.observations) == [first, second]


def test_in_memory_sequence_rejects_empty_sequences() -> None:
    with pytest.raises(ValueError, match="at least one"):
        InMemorySequence(())


def test_in_memory_sequence_rejects_time_reversal() -> None:
    with pytest.raises(ValueError, match="timestamp order"):
        InMemorySequence((_observation(2.0), _observation(1.0)))
