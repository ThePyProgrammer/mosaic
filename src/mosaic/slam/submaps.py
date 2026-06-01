from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from math import isfinite
from types import MappingProxyType
from typing import Mapping, Self

from mosaic.core.frames import FrameId, Timestamp
from mosaic.core.poses import Pose3
from mosaic.slam.protocol import MetricValue
from mosaic.splats.maps import SplatMap


@dataclass(frozen=True, order=True, slots=True)
class AgentId:
    value: str

    def __post_init__(self) -> None:
        _validate_identity_value(self.value, "AgentId value")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, order=True, slots=True)
class SessionId:
    value: str

    def __post_init__(self) -> None:
        _validate_identity_value(self.value, "SessionId value")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, order=True, slots=True)
class SubmapId:
    value: str

    def __post_init__(self) -> None:
        _validate_identity_value(self.value, "SubmapId value")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, order=True, slots=True)
class LoopId:
    value: str

    def __post_init__(self) -> None:
        _validate_identity_value(self.value, "LoopId value")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, order=True, slots=True)
class PoseGraphNodeId:
    value: str

    def __post_init__(self) -> None:
        _validate_identity_value(self.value, "PoseGraphNodeId value", allow_slash=True)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, order=True, slots=True)
class SubmapReference:
    agent_id: AgentId
    session_id: SessionId
    submap_id: SubmapId

    @property
    def node_id(self) -> PoseGraphNodeId:
        return PoseGraphNodeId(str(self))

    def __str__(self) -> str:
        return f"{self.agent_id}/{self.session_id}/{self.submap_id}"


class SubmapLifecycleState(StrEnum):
    ACTIVE = "active"
    FROZEN = "frozen"
    MERGED = "merged"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class GaussianSubmap:
    reference: SubmapReference
    local_frame: FrameId
    map_frame: FrameId
    local_to_map: Pose3
    splat_map: SplatMap
    state: SubmapLifecycleState = SubmapLifecycleState.ACTIVE
    first_timestamp: Timestamp | None = None
    last_timestamp: Timestamp | None = None
    diagnostics: Mapping[str, MetricValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.state, SubmapLifecycleState):
            raise ValueError("GaussianSubmap state must be a SubmapLifecycleState")
        if self.splat_map.frame != self.local_frame:
            raise ValueError("GaussianSubmap splat_map frame must match local_frame")
        if self.local_to_map.parent_frame != self.map_frame or self.local_to_map.child_frame != self.local_frame:
            raise ValueError("GaussianSubmap local_to_map frames must map local_frame into map_frame")
        if self.first_timestamp is not None and not isinstance(self.first_timestamp, Timestamp):
            raise ValueError("GaussianSubmap first_timestamp must be a Timestamp")
        if self.last_timestamp is not None and not isinstance(self.last_timestamp, Timestamp):
            raise ValueError("GaussianSubmap last_timestamp must be a Timestamp")
        if (
            self.first_timestamp is not None
            and self.last_timestamp is not None
            and self.first_timestamp > self.last_timestamp
        ):
            raise ValueError("GaussianSubmap first_timestamp must be less than or equal to last_timestamp")
        object.__setattr__(self, "diagnostics", _validate_diagnostics(self.diagnostics))

    @property
    def agent_id(self) -> AgentId:
        return self.reference.agent_id

    @property
    def session_id(self) -> SessionId:
        return self.reference.session_id

    @property
    def submap_id(self) -> SubmapId:
        return self.reference.submap_id

    @property
    def node_id(self) -> PoseGraphNodeId:
        return self.reference.node_id

    @property
    def anchor(self) -> tuple[float, float, float]:
        return self.local_to_map.translation.as_tuple()

    def with_pose(self, local_to_map: Pose3) -> Self:
        return type(self)(
            reference=self.reference,
            local_frame=self.local_frame,
            map_frame=self.map_frame,
            local_to_map=local_to_map,
            splat_map=self.splat_map,
            state=self.state,
            first_timestamp=self.first_timestamp,
            last_timestamp=self.last_timestamp,
            diagnostics=self.diagnostics,
        )


def _validate_identity_value(value: str, label: str, *, allow_slash: bool = False) -> None:
    if not value.strip():
        raise ValueError(f"{label} must not be blank")
    if "/" in value:
        if not allow_slash:
            raise ValueError(f"{label} must not contain '/'")
        if any(not segment.strip() for segment in value.split("/")):
            raise ValueError(f"{label} slash-delimited segments must not be blank")


def _validate_diagnostics(diagnostics: Mapping[str, MetricValue]) -> Mapping[str, MetricValue]:
    frozen: dict[str, MetricValue] = {}
    for key, value in diagnostics.items():
        if not isinstance(key, str) or not key.strip():
            raise ValueError("GaussianSubmap diagnostics must use non-blank string keys")
        if not isinstance(value, bool | int | float | str):
            raise ValueError("GaussianSubmap diagnostics must use JSON-ready scalar values")
        if isinstance(value, float) and not isfinite(value):
            raise ValueError("GaussianSubmap diagnostic float values must be finite")
        frozen[key] = value
    return MappingProxyType(frozen)


__all__ = [
    "AgentId",
    "GaussianSubmap",
    "LoopId",
    "PoseGraphNodeId",
    "SessionId",
    "SubmapId",
    "SubmapLifecycleState",
    "SubmapReference",
]
