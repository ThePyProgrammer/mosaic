from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Mapping


class AgentQueryKind(StrEnum):
    LOCAL_GEOMETRY = "local_geometry"
    SCENE_SUMMARY = "scene_summary"
    PROVENANCE = "provenance"


@dataclass(frozen=True, slots=True)
class LocalRadiusQuery:
    center: tuple[float, float, float]
    radius: float
    kind: AgentQueryKind = AgentQueryKind.LOCAL_GEOMETRY

    def __post_init__(self) -> None:
        if len(self.center) != 3:
            raise ValueError("LocalRadiusQuery center must contain three coordinates")
        if self.radius <= 0.0:
            raise ValueError("LocalRadiusQuery radius must be positive")


@dataclass(frozen=True, slots=True)
class SplatQueryResult:
    query_kind: AgentQueryKind
    splat_ids: tuple[int, ...]

    @property
    def count(self) -> int:
        return len(self.splat_ids)


@dataclass(frozen=True, slots=True)
class PosteriorSummary:
    splat_count: int
    provenance_count: int
    mean_opacity: float

    def __post_init__(self) -> None:
        if self.splat_count < 0:
            raise ValueError("PosteriorSummary splat_count must be non-negative")
        if self.provenance_count < 0:
            raise ValueError("PosteriorSummary provenance_count must be non-negative")
        if self.mean_opacity < 0.0 or self.mean_opacity > 1.0:
            raise ValueError("PosteriorSummary mean_opacity must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class ProvenanceSummary:
    counts: Mapping[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for source, count in self.counts.items():
            if not source.strip():
                raise ValueError("ProvenanceSummary source names must not be blank")
            if count < 0:
                raise ValueError("ProvenanceSummary counts must be non-negative")
        object.__setattr__(self, "counts", MappingProxyType(dict(self.counts)))
