import pytest

from mosaic.evaluation import SyntheticScenario, synthetic_forward_sequence


def test_synthetic_forward_sequence_is_deterministic() -> None:
    first = synthetic_forward_sequence(frame_count=3)
    second = synthetic_forward_sequence(frame_count=3)

    assert first == second
    assert first.name == "synthetic-forward-3"
    assert second.name == "synthetic-forward-3"
    assert len(first.sequence) == 3
    assert len(second.sequence) == 3
    assert [observation.timestamp.nanoseconds for observation in first.sequence] == [0, 100_000_000, 200_000_000]


def test_synthetic_forward_sequence_produces_front_camera_observations() -> None:
    scenario = synthetic_forward_sequence(frame_count=2)

    assert isinstance(scenario, SyntheticScenario)
    assert scenario.sequence.observations[0].camera_ids == ("front",)
    assert scenario.sequence.observations[1].views[0].camera_pose.translation.x == 1.0


def test_synthetic_forward_sequence_requires_positive_frame_count() -> None:
    with pytest.raises(ValueError, match="positive"):
        synthetic_forward_sequence(frame_count=0)
