from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from math import isfinite
from types import MappingProxyType
from typing import Mapping

from mosaic.core.frames import Timestamp
from mosaic.slam.protocol import MetricValue
from mosaic.slam.submaps import AgentId, GaussianSubmap, SessionId, SubmapReference


class ExchangePolicy(StrEnum):
    KEYFRAME_ONLY = "keyframe_only"
    SUBMAP_ONLY = "submap_only"
    MIXED = "mixed"


@dataclass(frozen=True, slots=True)
class SubmapExchangeMessage:
    sender: AgentId
    sequence_number: int
    timestamp: Timestamp
    submap: GaussianSubmap
    receiver: AgentId | None = None
    policy: ExchangePolicy = ExchangePolicy.SUBMAP_ONLY
    diagnostics: Mapping[str, MetricValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.submap, GaussianSubmap):
            raise ValueError("SubmapExchangeMessage submap must be a GaussianSubmap")
        if self.sender != self.submap.agent_id:
            raise ValueError("SubmapExchangeMessage sender must match submap agent_id")
        if isinstance(self.sequence_number, bool) or not isinstance(self.sequence_number, int):
            raise ValueError("SubmapExchangeMessage sequence_number must be an integer")
        if self.sequence_number < 0:
            raise ValueError("SubmapExchangeMessage sequence_number must be non-negative")
        if self.policy is not ExchangePolicy.SUBMAP_ONLY:
            raise ValueError("SubmapExchangeMessage policy must be SUBMAP_ONLY")
        object.__setattr__(self, "diagnostics", _validate_diagnostics(self.diagnostics, "SubmapExchangeMessage"))


@dataclass(frozen=True, slots=True)
class KeyframeExchangeMessage:
    sender: AgentId
    session_id: SessionId
    keyframe_id: str
    timestamp: Timestamp
    camera_ids: tuple[str, ...]
    submap_reference: SubmapReference | None = None
    receiver: AgentId | None = None
    policy: ExchangePolicy = ExchangePolicy.KEYFRAME_ONLY
    diagnostics: Mapping[str, MetricValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.keyframe_id, str) or not self.keyframe_id.strip():
            raise ValueError("KeyframeExchangeMessage keyframe_id must not be blank")
        if not isinstance(self.camera_ids, tuple):
            raise ValueError("KeyframeExchangeMessage camera_ids must be a tuple")
        camera_ids = self.camera_ids
        if not camera_ids:
            raise ValueError("KeyframeExchangeMessage camera_ids must not be empty")
        if any(not isinstance(camera_id, str) or not camera_id.strip() for camera_id in camera_ids):
            raise ValueError("KeyframeExchangeMessage camera_ids must contain non-blank string values")
        if len(set(camera_ids)) != len(camera_ids):
            raise ValueError("KeyframeExchangeMessage camera_ids must be unique")
        if self.policy is not ExchangePolicy.KEYFRAME_ONLY:
            raise ValueError("KeyframeExchangeMessage policy must be KEYFRAME_ONLY")
        if self.submap_reference is not None:
            if not isinstance(self.submap_reference, SubmapReference):
                raise ValueError("KeyframeExchangeMessage submap_reference must be a SubmapReference")
            if self.submap_reference.agent_id != self.sender:
                raise ValueError("KeyframeExchangeMessage sender must match submap_reference agent_id")
            if self.submap_reference.session_id != self.session_id:
                raise ValueError("KeyframeExchangeMessage session_id must match submap_reference session_id")
        object.__setattr__(self, "camera_ids", camera_ids)
        object.__setattr__(self, "diagnostics", _validate_diagnostics(self.diagnostics, "KeyframeExchangeMessage"))


def _validate_diagnostics(diagnostics: Mapping[str, MetricValue], label: str) -> Mapping[str, MetricValue]:
    frozen: dict[str, MetricValue] = {}
    for key, value in diagnostics.items():
        if not isinstance(key, str) or not key.strip():
            raise ValueError(f"{label} diagnostics must use non-blank string keys")
        if not isinstance(value, bool | int | float | str):
            raise ValueError(f"{label} diagnostics must use JSON-ready scalar values")
        if isinstance(value, float) and not isfinite(value):
            raise ValueError(f"{label} diagnostic float values must be finite")
        frozen[key] = value
    return MappingProxyType(frozen)


__all__ = [
    "ExchangePolicy",
    "KeyframeExchangeMessage",
    "SubmapExchangeMessage",
]
