from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from math import isfinite
from types import MappingProxyType
from typing import Mapping


class AgentQueryKind(StrEnum):
    LOCAL_GEOMETRY = "local_geometry"
    SCENE_SUMMARY = "scene_summary"
    PROVENANCE = "provenance"
    UNCERTAINTY = "uncertainty"


@dataclass(frozen=True, slots=True)
class LocalRadiusQuery:
    center: tuple[float, float, float]
    radius: float
    max_results: int = 32
    kind: AgentQueryKind = AgentQueryKind.LOCAL_GEOMETRY

    def __post_init__(self) -> None:
        object.__setattr__(self, "center", tuple(self.center))
        if len(self.center) != 3:
            raise ValueError("LocalRadiusQuery center must contain three coordinates")
        if not all(isfinite(value) for value in self.center):
            raise ValueError("LocalRadiusQuery center coordinates must be finite")
        if not isfinite(self.radius) or self.radius <= 0.0:
            raise ValueError("LocalRadiusQuery radius must be finite and positive")
        if self.kind is not AgentQueryKind.LOCAL_GEOMETRY:
            raise ValueError("LocalRadiusQuery kind must be local_geometry")
        if self.max_results <= 0:
            raise ValueError("LocalRadiusQuery max_results must be positive")


@dataclass(frozen=True, slots=True)
class SplatQueryResult:
    query_kind: AgentQueryKind
    splat_ids: tuple[int, ...]
    total_matches: int | None = None
    truncated: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "splat_ids", tuple(self.splat_ids))
        if self.total_matches is None:
            object.__setattr__(self, "total_matches", len(self.splat_ids))
        if self.total_matches < len(self.splat_ids):
            raise ValueError("SplatQueryResult total_matches must cover returned splat_ids")
        expected_truncated = self.total_matches > len(self.splat_ids)
        if self.truncated is not expected_truncated:
            raise ValueError("SplatQueryResult truncated must equal total_matches > count")

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
class PosteriorUncertaintySummary:
    splat_count: int
    mean_covariance_diagonal: tuple[float, float, float] = (0.0, 0.0, 0.0)
    max_covariance_diagonal: tuple[float, float, float] = (0.0, 0.0, 0.0)
    mean_opacity: float = 0.0
    min_opacity: float = 0.0
    max_opacity: float = 0.0
    semantics: str = "descriptive_only"

    def __post_init__(self) -> None:
        object.__setattr__(self, "mean_covariance_diagonal", tuple(self.mean_covariance_diagonal))
        object.__setattr__(self, "max_covariance_diagonal", tuple(self.max_covariance_diagonal))
        if self.splat_count < 0:
            raise ValueError("PosteriorUncertaintySummary splat_count must be non-negative")
        if self.semantics != "descriptive_only":
            raise ValueError("PosteriorUncertaintySummary semantics must be descriptive_only")
        for name, diagonal in (
            ("mean_covariance_diagonal", self.mean_covariance_diagonal),
            ("max_covariance_diagonal", self.max_covariance_diagonal),
        ):
            if len(diagonal) != 3:
                raise ValueError(f"PosteriorUncertaintySummary {name} must contain three values")
            if any(value < 0.0 for value in diagonal):
                raise ValueError(f"PosteriorUncertaintySummary {name} values must be non-negative")
        for name, value in (
            ("mean_opacity", self.mean_opacity),
            ("min_opacity", self.min_opacity),
            ("max_opacity", self.max_opacity),
        ):
            if value < 0.0 or value > 1.0:
                raise ValueError(f"PosteriorUncertaintySummary {name} must be between 0 and 1")
        if not self.min_opacity <= self.mean_opacity <= self.max_opacity:
            raise ValueError(
                "PosteriorUncertaintySummary opacity values must satisfy "
                "min_opacity <= mean_opacity <= max_opacity"
            )
        if any(
            mean_value > max_value
            for mean_value, max_value in zip(
                self.mean_covariance_diagonal,
                self.max_covariance_diagonal,
                strict=True,
            )
        ):
            raise ValueError(
                "PosteriorUncertaintySummary covariance values must satisfy "
                "mean_covariance_diagonal <= max_covariance_diagonal"
            )


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
