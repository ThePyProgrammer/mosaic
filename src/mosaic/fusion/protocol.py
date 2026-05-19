from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from math import isfinite
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
        object.__setattr__(self, "maps", tuple(self.maps))
        if not self.maps:
            raise ValueError("FusionInput requires at least one map")
        frames = {splat_map.frame for splat_map in self.maps}
        if len(frames) != 1:
            raise ValueError("FusionInput maps must share the same frame")

    @property
    def frame(self) -> FrameId:
        return self.maps[0].frame


@dataclass(frozen=True, slots=True)
class FusionProvenanceSummary:
    source_map_count: int = 0
    source_splat_count: int = 0
    fused_splat_count: int = 0
    per_provenance_counts: Mapping[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.source_map_count < 0:
            raise ValueError("FusionProvenanceSummary source_map_count must be non-negative")
        if self.source_splat_count < 0:
            raise ValueError("FusionProvenanceSummary source_splat_count must be non-negative")
        if self.fused_splat_count < 0:
            raise ValueError("FusionProvenanceSummary fused_splat_count must be non-negative")
        for provenance, count in self.per_provenance_counts.items():
            if not provenance.strip():
                raise ValueError("FusionProvenanceSummary provenance names must not be blank")
            if count < 0:
                raise ValueError("FusionProvenanceSummary provenance counts must be non-negative")
        object.__setattr__(
            self,
            "per_provenance_counts",
            MappingProxyType(dict(self.per_provenance_counts)),
        )


@dataclass(frozen=True, slots=True)
class FusionUncertaintySummary:
    model_label: str = "unspecified"
    covariance_diagonal_min: float = 0.0
    covariance_diagonal_max: float = 0.0
    covariance_diagonal_mean: float = 0.0

    def __post_init__(self) -> None:
        if not self.model_label.strip():
            raise ValueError("FusionUncertaintySummary model_label must not be blank")
        stats = (
            self.covariance_diagonal_min,
            self.covariance_diagonal_max,
            self.covariance_diagonal_mean,
        )
        if any(not isfinite(stat) or stat < 0.0 for stat in stats):
            raise ValueError("FusionUncertaintySummary covariance stats must be finite non-negative values")
        if self.covariance_diagonal_max < self.covariance_diagonal_min:
            raise ValueError("FusionUncertaintySummary covariance max must be greater than or equal to min")


@dataclass(frozen=True, slots=True)
class FusionConflictSummary:
    total_candidate_count: int = 0
    involved_provenance_pairs: Mapping[str, int] = field(default_factory=dict)
    reason_counts: Mapping[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.total_candidate_count < 0:
            raise ValueError("FusionConflictSummary total_candidate_count must be non-negative")
        self._validate_counts(self.involved_provenance_pairs, "provenance pair")
        self._validate_counts(self.reason_counts, "reason")
        if self.total_candidate_count > 0 and (
            not self.involved_provenance_pairs or not self.reason_counts
        ):
            raise ValueError("FusionConflictSummary requires details when total count is positive")
        object.__setattr__(
            self,
            "involved_provenance_pairs",
            MappingProxyType(dict(self.involved_provenance_pairs)),
        )
        object.__setattr__(self, "reason_counts", MappingProxyType(dict(self.reason_counts)))

    @staticmethod
    def _validate_counts(counts: Mapping[str, int], label: str) -> None:
        for key, count in counts.items():
            if not key.strip():
                raise ValueError(f"FusionConflictSummary {label} keys must not be blank")
            if count < 0:
                raise ValueError(f"FusionConflictSummary {label} counts must be non-negative")


@dataclass(frozen=True, slots=True)
class FusionResult:
    status: FusionStatus
    fused_map: SplatMap
    diagnostics: Mapping[str, FusionMetricValue] = field(default_factory=dict)
    provenance: FusionProvenanceSummary = field(default_factory=FusionProvenanceSummary)
    uncertainty: FusionUncertaintySummary = field(default_factory=FusionUncertaintySummary)
    conflicts: FusionConflictSummary = field(default_factory=FusionConflictSummary)

    def __post_init__(self) -> None:
        diagnostics = dict(self.diagnostics)
        for key, value in diagnostics.items():
            if not key.strip():
                raise ValueError("FusionResult diagnostic keys must not be blank")
            if isinstance(value, float) and not isfinite(value):
                raise ValueError("FusionResult diagnostic float values must be finite")
            if not isinstance(value, bool | int | float | str):
                raise ValueError("FusionResult diagnostic values must be bool, int, float, or str")
        object.__setattr__(self, "diagnostics", MappingProxyType(diagnostics))


@runtime_checkable
class SplatFusionStrategy(Protocol):
    @property
    def name(self) -> str:
        raise NotImplementedError

    def fuse(self, fusion_input: FusionInput) -> FusionResult:
        raise NotImplementedError
