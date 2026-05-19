from __future__ import annotations

from dataclasses import dataclass
from math import dist, isfinite
from typing import Sequence

from mosaic.agents import LocalRadiusQuery, SplatPosteriorView
from mosaic.core import FrameId
from mosaic.fusion import FusionResult
from mosaic.slam import SplatSlamUpdate, TrackingState
from mosaic.splats import SplatMap


@dataclass(frozen=True, slots=True)
class MetricResult:
    name: str
    value: float
    unit: str
    family: str = "general"

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("MetricResult name must not be blank")
        if not isfinite(self.value):
            raise ValueError("MetricResult value must be finite")
        if not self.unit.strip():
            raise ValueError("MetricResult unit must not be blank")
        if not self.family.strip():
            raise ValueError("MetricResult family must not be blank")

    def as_dict(self) -> dict[str, str | float]:
        return {"name": self.name, "value": self.value, "unit": self.unit, "family": self.family}


def splat_count_metric(snapshot: SplatMap) -> MetricResult:
    return MetricResult(name="splat_count", value=float(len(snapshot)), unit="splats", family="map_quality")


def lifecycle_metrics(updates: Sequence[SplatSlamUpdate], snapshot: SplatMap) -> tuple[MetricResult, ...]:
    update_count = len(updates)
    tracking_count = sum(1 for update in updates if update.tracking_state is TrackingState.TRACKING)
    lost_count = sum(1 for update in updates if update.tracking_state is TrackingState.LOST)
    not_initialized_count = sum(
        1 for update in updates if update.tracking_state is TrackingState.NOT_INITIALIZED
    )
    tracking_success_rate = float(tracking_count / update_count) if update_count else 0.0
    return (
        MetricResult(name="update_count", value=float(update_count), unit="count", family="lifecycle"),
        MetricResult(
            name="tracking_success_rate",
            value=tracking_success_rate,
            unit="ratio",
            family="lifecycle",
        ),
        MetricResult(
            name="lost_tracking_count",
            value=float(lost_count),
            unit="count",
            family="lifecycle",
        ),
        MetricResult(
            name="not_initialized_tracking_count",
            value=float(not_initialized_count),
            unit="count",
            family="lifecycle",
        ),
        MetricResult(name="splat_count", value=float(len(snapshot)), unit="splats", family="lifecycle"),
    )


def trajectory_consistency_metrics(updates: Sequence[SplatSlamUpdate]) -> tuple[MetricResult, ...]:
    tracking_updates = tuple(update for update in updates if update.tracking_state is TrackingState.TRACKING)
    has_all_tracking_poses = bool(tracking_updates) and all(
        update.estimated_pose is not None for update in tracking_updates
    )
    deltas = tuple(
        dist(
            previous.estimated_pose.translation.as_tuple(),
            current.estimated_pose.translation.as_tuple(),
        )
        for previous, current in zip(tracking_updates, tracking_updates[1:])
        if previous.estimated_pose is not None and current.estimated_pose is not None
    )
    delta_consistent = has_all_tracking_poses and all(isfinite(delta) for delta in deltas)
    return (
        MetricResult(
            name="trajectory_pose_available",
            value=_flag(has_all_tracking_poses),
            unit="flag",
            family="trajectory",
        ),
        MetricResult(
            name="trajectory_pose_delta_consistent",
            value=_flag(delta_consistent),
            unit="flag",
            family="trajectory",
        ),
    )


def map_quality_metrics(
    snapshot: SplatMap,
    *,
    expected_frame: FrameId | None = None,
    fusion_result: FusionResult | None = None,
) -> tuple[MetricResult, ...]:
    provenance_count = len({splat.provenance for splat in snapshot.splats if splat.provenance is not None})
    frame_matches = expected_frame is None or snapshot.frame == expected_frame
    metrics = [
        MetricResult(
            name="map_splat_count",
            value=float(len(snapshot)),
            unit="splats",
            family="map_quality",
        ),
        MetricResult(
            name="map_frame_match",
            value=_flag(frame_matches),
            unit="flag",
            family="map_quality",
        ),
        MetricResult(
            name="map_provenance_source_count",
            value=float(provenance_count),
            unit="count",
            family="map_quality",
        ),
    ]
    if fusion_result is not None:
        metrics.append(
            MetricResult(
                name="fusion_diagnostic_presence",
                value=_flag(bool(fusion_result.diagnostics)),
                unit="flag",
                family="map_fusion",
            )
        )
    return tuple(metrics)


def agent_query_stability_metrics(
    posterior: SplatPosteriorView,
    query: LocalRadiusQuery,
    *,
    repetitions: int = 2,
) -> tuple[MetricResult, ...]:
    if repetitions <= 0:
        raise ValueError("agent_query_stability_metrics repetitions must be positive")
    local_results = tuple(posterior.query_local(query) for _ in range(repetitions))
    summary_results = tuple(posterior.summary() for _ in range(repetitions))
    provenance_results = tuple(posterior.provenance() for _ in range(repetitions))
    return (
        MetricResult(
            name="agent_query_local_stable",
            value=_flag(_all_equal(local_results)),
            unit="flag",
            family="agent_query",
        ),
        MetricResult(
            name="agent_query_summary_stable",
            value=_flag(_all_equal(summary_results)),
            unit="flag",
            family="agent_query",
        ),
        MetricResult(
            name="agent_query_provenance_stable",
            value=_flag(_all_equal(provenance_results)),
            unit="flag",
            family="agent_query",
        ),
        MetricResult(
            name="agent_query_repetition_count",
            value=float(repetitions),
            unit="count",
            family="agent_query",
        ),
    )


def _flag(value: bool) -> float:
    return 1.0 if value else 0.0


def _all_equal(values: tuple[object, ...]) -> bool:
    if not values:
        return True
    first = values[0]
    return all(value == first for value in values)
