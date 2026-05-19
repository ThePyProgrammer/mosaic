from __future__ import annotations

from collections.abc import Callable, Mapping

import pytest

from mosaic.evaluation.scenarios import synthetic_forward_sequence
from mosaic.slam.protocol import MetricValue, SplatSlamBackend, SplatSlamUpdate, TrackingState
from mosaic.slam.registry import BackendDescriptor
from mosaic.splats import SplatMap


_JSON_READY_SCALARS = (bool, int, float, str)


def skip_unavailable_backend(descriptor: BackendDescriptor) -> None:
    availability = descriptor.check_availability()
    if availability.available:
        return

    reason_parts = [*availability.missing_requirements]
    reason_parts.extend(str(value) for value in availability.install_hints.values())
    reason_parts.extend(str(value) for value in availability.diagnostics.values())
    reason = ", ".join(reason_parts) or f"Backend {descriptor.name!r} is unavailable"
    pytest.skip(reason)


def assert_backend_state_update_contract(
    backend: SplatSlamBackend,
    expected_states: tuple[TrackingState, ...] = (
        TrackingState.TRACKING,
        TrackingState.LOST,
        TrackingState.NOT_INITIALIZED,
    ),
) -> None:
    observation = next(iter(synthetic_forward_sequence(frame_count=1).sequence))
    update = backend.process(observation)

    assert isinstance(update, SplatSlamUpdate)
    assert isinstance(update.tracking_state, TrackingState)
    assert update.tracking_state in expected_states
    if update.tracking_state is TrackingState.TRACKING:
        assert update.estimated_pose is not None
    if update.tracking_state in (TrackingState.LOST, TrackingState.NOT_INITIALIZED):
        assert update.estimated_pose is None
    assert isinstance(update.map_update, SplatMap)
    _assert_scalar_mapping(update.diagnostics)


def assert_backend_lifecycle_contract(factory: Callable[[], SplatSlamBackend], frame_count: int = 3) -> None:
    backend = factory()
    backend.reset()
    reset_snapshot = backend.snapshot()
    assert isinstance(reset_snapshot, SplatMap)
    pre_replay_length = len(reset_snapshot)

    scenario = synthetic_forward_sequence(frame_count=frame_count)
    for observation in scenario.sequence:
        update = backend.process(observation)
        assert isinstance(update, SplatSlamUpdate)
        assert update.timestamp == observation.timestamp
        assert isinstance(update.map_update, SplatMap)
        _assert_scalar_mapping(update.diagnostics)

    post_replay_snapshot = backend.snapshot()
    assert isinstance(post_replay_snapshot, SplatMap)

    backend.reset()
    final_snapshot = backend.snapshot()
    assert isinstance(final_snapshot, SplatMap)
    assert len(final_snapshot) <= pre_replay_length


def assert_backend_deterministic_replay(factory: Callable[[], SplatSlamBackend], frame_count: int = 3) -> None:
    first_outcome = _replay_contract_outcome(factory(), frame_count)
    second_outcome = _replay_contract_outcome(factory(), frame_count)

    assert first_outcome == second_outcome


def _replay_contract_outcome(
    backend: SplatSlamBackend,
    frame_count: int,
) -> tuple[tuple[str, ...], tuple[int, ...], tuple[tuple[tuple[str, MetricValue], ...], ...], int]:
    backend.reset()
    states: list[str] = []
    map_update_lengths: list[int] = []
    diagnostics: list[tuple[tuple[str, MetricValue], ...]] = []

    for observation in synthetic_forward_sequence(frame_count=frame_count).sequence:
        update = backend.process(observation)
        assert isinstance(update, SplatSlamUpdate)
        states.append(update.tracking_state.value)
        map_update_lengths.append(len(update.map_update))
        _assert_scalar_mapping(update.diagnostics)
        diagnostics.append(tuple(sorted(update.diagnostics.items())))

    snapshot = backend.snapshot()
    assert isinstance(snapshot, SplatMap)
    return (tuple(states), tuple(map_update_lengths), tuple(diagnostics), len(snapshot))


def _assert_scalar_mapping(diagnostics: Mapping[str, MetricValue]) -> None:
    for key, value in diagnostics.items():
        assert isinstance(key, str)
        assert isinstance(value, _JSON_READY_SCALARS)


__all__ = [
    "assert_backend_deterministic_replay",
    "assert_backend_lifecycle_contract",
    "assert_backend_state_update_contract",
    "skip_unavailable_backend",
]
