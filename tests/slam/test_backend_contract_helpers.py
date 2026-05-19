from __future__ import annotations

import pytest

from mosaic.core import FrameId
from mosaic.slam import (
    BackendCapabilities,
    BackendDependency,
    BackendDescriptor,
    DeterministicSplatBackend,
    SplatSlamUpdate,
    TrackingState,
    assert_backend_deterministic_replay,
    assert_backend_lifecycle_contract,
    assert_backend_state_update_contract,
    skip_unavailable_backend,
)
from mosaic.splats import SplatMap


class LostTrackingBackend:
    @property
    def name(self) -> str:
        return "lost-tracking-test"

    @property
    def capabilities(self) -> BackendCapabilities:
        return BackendCapabilities(
            supports_multi_view=True,
            supports_incremental_mapping=False,
            supports_uncertainty=False,
        )

    def reset(self) -> None:
        return None

    def process(self, observation) -> SplatSlamUpdate:
        return SplatSlamUpdate(
            timestamp=observation.timestamp,
            tracking_state=TrackingState.LOST,
            estimated_pose=None,
            map_update=SplatMap(frame=FrameId("map")),
            diagnostics={"reason": "lost"},
        )

    def snapshot(self) -> SplatMap:
        return SplatMap(frame=FrameId("map"))


class NotInitializedBackend:
    @property
    def name(self) -> str:
        return "not-initialized-test"

    @property
    def capabilities(self) -> BackendCapabilities:
        return BackendCapabilities(
            supports_multi_view=True,
            supports_incremental_mapping=False,
            supports_uncertainty=False,
        )

    def reset(self) -> None:
        return None

    def process(self, observation) -> SplatSlamUpdate:
        return SplatSlamUpdate(
            timestamp=observation.timestamp,
            tracking_state=TrackingState.NOT_INITIALIZED,
            estimated_pose=None,
            map_update=SplatMap(frame=FrameId("map")),
            diagnostics={"reason": "not_initialized"},
        )

    def snapshot(self) -> SplatMap:
        return SplatMap(frame=FrameId("map"))


def _unavailable_descriptor() -> BackendDescriptor:
    return BackendDescriptor(
        name="missing-optional-backend",
        version="0.1.0",
        capabilities=BackendCapabilities(
            supports_multi_view=True,
            supports_incremental_mapping=True,
            supports_uncertainty=False,
        ),
        dependencies=(
            BackendDependency(
                package="mosaic_backend_missing_dependency_for_tests_zzz",
                install_hint="install optional backend",
            ),
        ),
        factory=DeterministicSplatBackend,
    )


def test_contract_helpers_are_importable_from_slam_package() -> None:
    assert callable(assert_backend_lifecycle_contract)
    assert callable(assert_backend_deterministic_replay)
    assert callable(assert_backend_state_update_contract)
    assert callable(skip_unavailable_backend)


def test_contract_helper_skips_unavailable_descriptor_with_diagnostic() -> None:
    with pytest.raises(pytest.skip.Exception) as exc_info:
        skip_unavailable_backend(_unavailable_descriptor())

    reason = str(exc_info.value)
    assert (
        "mosaic_backend_missing_dependency_for_tests_zzz" in reason
        or "install optional backend" in reason
    )


def test_lifecycle_contract_helper_accepts_deterministic_backend_factory() -> None:
    assert_backend_lifecycle_contract(DeterministicSplatBackend)


def test_deterministic_replay_helper_compares_contract_level_outcomes() -> None:
    assert_backend_deterministic_replay(DeterministicSplatBackend)


@pytest.mark.parametrize(
    ("backend", "state"),
    (
        (DeterministicSplatBackend(), TrackingState.TRACKING),
        (LostTrackingBackend(), TrackingState.LOST),
        (NotInitializedBackend(), TrackingState.NOT_INITIALIZED),
    ),
)
def test_state_update_contract_helper_accepts_tracking_edge_states(backend, state: TrackingState) -> None:
    assert_backend_state_update_contract(backend, expected_states=(state,))
