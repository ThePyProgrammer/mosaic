from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Mapping, Protocol, runtime_checkable

from mosaic.core import FrameId
from mosaic.splats import SplatMap

FusionMetricValue = bool | int | float | str


class FusionStatus(StrEnum):
    FUSED = "fused"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class FusionInput:
    maps: tuple[SplatMap, ...]

    def __post_init__(self) -> None:
        if not self.maps:
            raise ValueError("FusionInput requires at least one map")
        frames = {splat_map.frame for splat_map in self.maps}
        if len(frames) != 1:
            raise ValueError("FusionInput maps must share the same frame")

    @property
    def frame(self) -> FrameId:
        return self.maps[0].frame


@dataclass(frozen=True, slots=True)
class FusionResult:
    status: FusionStatus
    fused_map: SplatMap
    diagnostics: Mapping[str, FusionMetricValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "diagnostics", MappingProxyType(dict(self.diagnostics)))


@runtime_checkable
class SplatFusionStrategy(Protocol):
    @property
    def name(self) -> str:
        raise NotImplementedError

    def fuse(self, fusion_input: FusionInput) -> FusionResult:
        raise NotImplementedError
