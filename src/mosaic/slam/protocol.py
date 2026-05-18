from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Mapping, Protocol, runtime_checkable

from mosaic.core.frames import Timestamp
from mosaic.core.observations import MultiViewObservation
from mosaic.core.poses import Pose3
from mosaic.splats.maps import SplatMap

MetricValue = bool | int | float | str


class TrackingState(StrEnum):
    NOT_INITIALIZED = "not_initialized"
    TRACKING = "tracking"
    LOST = "lost"


@dataclass(frozen=True, slots=True)
class BackendCapabilities:
    supports_multi_view: bool
    supports_incremental_mapping: bool
    supports_uncertainty: bool
    runs_out_of_process: bool = False
    parameters: Mapping[str, MetricValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "parameters", MappingProxyType(dict(self.parameters)))


@dataclass(frozen=True, slots=True)
class SplatSlamUpdate:
    timestamp: Timestamp
    tracking_state: TrackingState
    estimated_pose: Pose3 | None
    map_update: SplatMap
    diagnostics: Mapping[str, MetricValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.tracking_state is TrackingState.TRACKING and self.estimated_pose is None:
            raise ValueError("Tracking updates require an estimated_pose")
        object.__setattr__(self, "diagnostics", MappingProxyType(dict(self.diagnostics)))


@runtime_checkable
class SplatSlamBackend(Protocol):
    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def capabilities(self) -> BackendCapabilities:
        raise NotImplementedError

    def reset(self) -> None:
        raise NotImplementedError

    def process(self, observation: MultiViewObservation) -> SplatSlamUpdate:
        raise NotImplementedError

    def snapshot(self) -> SplatMap:
        raise NotImplementedError
