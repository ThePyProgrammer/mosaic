from __future__ import annotations

from dataclasses import dataclass
from math import dist, sqrt

from mosaic.fusion.protocol import (
    FusionConflictSummary,
    FusionInput,
    FusionProvenanceSummary,
    FusionResult,
    FusionStatus,
    FusionUncertaintySummary,
)
from mosaic.splats import GaussianSplat, SplatMap

_PRESERVED_UNCERTAINTY_MODEL = "preserved_not_optimized"
_OVERLAP_RADIUS_SCALE = 2.0
_COLOR_MISMATCH_THRESHOLD = 0.5
_OPACITY_MISMATCH_THRESHOLD = 0.25
_COVARIANCE_MISMATCH_RATIO = 2.0


@dataclass(frozen=True, slots=True)
class ProvenancePreservingFusion:
    @property
    def name(self) -> str:
        return "provenance-preserving"

    def fuse(self, fusion_input: FusionInput) -> FusionResult:
        fused_splats: list[GaussianSplat] = []
        for splat_map in fusion_input.maps:
            fused_splats.extend(splat_map.splats)
        fused_map = SplatMap(frame=fusion_input.frame, splats=tuple(fused_splats))
        provenance = _summarize_provenance(fusion_input, fused_splats, fused_map)
        uncertainty = _summarize_uncertainty(fused_splats)
        conflicts = _summarize_conflicts(fused_splats)
        return FusionResult(
            status=FusionStatus.FUSED,
            fused_map=fused_map,
            provenance=provenance,
            uncertainty=uncertainty,
            conflicts=conflicts,
            diagnostics={
                "source_map_count": provenance.source_map_count,
                "source_splat_count": provenance.source_splat_count,
                "fused_splat_count": provenance.fused_splat_count,
                "fusion_uncertainty_model": uncertainty.model_label,
                "fusion_conflict_candidate_count": conflicts.total_candidate_count,
            },
        )


def _summarize_provenance(
    fusion_input: FusionInput,
    fused_splats: list[GaussianSplat],
    fused_map: SplatMap,
) -> FusionProvenanceSummary:
    counts: dict[str, int] = {}
    for splat in fused_splats:
        provenance = _provenance_key(splat)
        counts[provenance] = counts.get(provenance, 0) + 1
    return FusionProvenanceSummary(
        source_map_count=len(fusion_input.maps),
        source_splat_count=len(fused_splats),
        fused_splat_count=len(fused_map),
        per_provenance_counts=counts,
    )


def _summarize_uncertainty(splats: list[GaussianSplat]) -> FusionUncertaintySummary:
    diagonal_values = [diagonal for splat in splats for diagonal in _covariance_diagonal(splat)]
    if not diagonal_values:
        return FusionUncertaintySummary(model_label=_PRESERVED_UNCERTAINTY_MODEL)
    return FusionUncertaintySummary(
        model_label=_PRESERVED_UNCERTAINTY_MODEL,
        covariance_diagonal_min=min(diagonal_values),
        covariance_diagonal_max=max(diagonal_values),
        covariance_diagonal_mean=sum(diagonal_values) / len(diagonal_values),
    )


def _summarize_conflicts(splats: list[GaussianSplat]) -> FusionConflictSummary:
    total_candidate_count = 0
    provenance_pairs: dict[str, int] = {}
    reason_counts: dict[str, int] = {}
    for index, first in enumerate(splats):
        for second in splats[index + 1 :]:
            first_provenance = _provenance_key(first)
            second_provenance = _provenance_key(second)
            if first_provenance == second_provenance or not _overlaps(first, second):
                continue
            reasons = _mismatch_reasons(first, second)
            if not reasons:
                continue
            total_candidate_count += 1
            pair_key = "|".join(sorted((first_provenance, second_provenance)))
            provenance_pairs[pair_key] = provenance_pairs.get(pair_key, 0) + 1
            for reason in reasons:
                reason_counts[reason] = reason_counts.get(reason, 0) + 1
    return FusionConflictSummary(
        total_candidate_count=total_candidate_count,
        involved_provenance_pairs=provenance_pairs,
        reason_counts=reason_counts,
    )


def _overlaps(first: GaussianSplat, second: GaussianSplat) -> bool:
    first_radius = sqrt(max(_covariance_diagonal(first)))
    second_radius = sqrt(max(_covariance_diagonal(second)))
    overlap_distance = _OVERLAP_RADIUS_SCALE * (first_radius + second_radius)
    return dist(first.center, second.center) <= overlap_distance


def _mismatch_reasons(first: GaussianSplat, second: GaussianSplat) -> tuple[str, ...]:
    reasons: list[str] = []
    if _color_distance(first, second) > _COLOR_MISMATCH_THRESHOLD:
        reasons.append("overlap/color")
    if abs(first.opacity - second.opacity) > _OPACITY_MISMATCH_THRESHOLD:
        reasons.append("overlap/opacity")
    if _covariance_ratio_mismatch(first, second):
        reasons.append("overlap/covariance")
    return tuple(reasons)


def _color_distance(first: GaussianSplat, second: GaussianSplat) -> float:
    return dist(first.color_rgb, second.color_rgb)


def _covariance_ratio_mismatch(first: GaussianSplat, second: GaussianSplat) -> bool:
    for first_value, second_value in zip(_covariance_diagonal(first), _covariance_diagonal(second), strict=True):
        smaller = min(first_value, second_value)
        larger = max(first_value, second_value)
        if larger / smaller >= _COVARIANCE_MISMATCH_RATIO:
            return True
    return False


def _covariance_diagonal(splat: GaussianSplat) -> tuple[float, float, float]:
    covariance = splat.covariance_upper
    return covariance[0], covariance[3], covariance[5]


def _provenance_key(splat: GaussianSplat) -> str:
    return splat.provenance if splat.provenance is not None else "unknown"
