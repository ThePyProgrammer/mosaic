import pytest

from mosaic.agents import LocalRadiusQuery, SplatPosteriorView
from mosaic.core import FrameId
from mosaic.evaluation import (
    MetricResult,
    agent_query_stability_metrics,
    lifecycle_metrics,
    map_quality_metrics,
    splat_count_metric,
    trajectory_consistency_metrics,
)
from mosaic.fusion import FusionResult
from mosaic.slam import SplatSlamUpdate, TrackingState
from mosaic.splats import GaussianSplat, SplatMap


def _splat(x: float, provenance: str | None = None) -> GaussianSplat:
    return GaussianSplat(
        center=(x, 0.0, 1.0),
        covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1),
        provenance=provenance,
    )


def test_metric_result_rejects_blank_name() -> None:
    with pytest.raises(ValueError, match="name"):
        MetricResult(name=" ", value=1.0, unit="count", family="lifecycle")


def test_metric_result_rejects_blank_family() -> None:
    with pytest.raises(ValueError, match="family"):
        MetricResult(name="tracking_success_rate", value=1.0, unit="ratio", family=" ")


def test_splat_count_metric_counts_snapshot_splats() -> None:
    snapshot = SplatMap(frame=FrameId("map"), splats=(_splat(0.0), _splat(1.0)))

    metric = splat_count_metric(snapshot)

    assert metric == MetricResult(name="splat_count", value=2.0, unit="splats", family="map_quality")


def test_metric_result_converts_to_json_ready_dict() -> None:
    metric = MetricResult(name="tracking_success_rate", value=1.0, unit="ratio", family="lifecycle")

    assert metric.as_dict() == {
        "name": "tracking_success_rate",
        "value": 1.0,
        "unit": "ratio",
        "family": "lifecycle",
    }


def test_lifecycle_metrics_count_tracking_states_and_final_splats() -> None:
    snapshot = SplatMap(frame=FrameId("map"), splats=(_splat(0.0), _splat(1.0)))
    updates = (
        SplatSlamUpdate(
            timestamp=_timestamp(0),
            tracking_state=TrackingState.NOT_INITIALIZED,
            estimated_pose=None,
            map_update=SplatMap(frame=FrameId("map")),
        ),
        SplatSlamUpdate(
            timestamp=_timestamp(1),
            tracking_state=TrackingState.LOST,
            estimated_pose=None,
            map_update=SplatMap(frame=FrameId("map")),
        ),
        SplatSlamUpdate(
            timestamp=_timestamp(2),
            tracking_state=TrackingState.TRACKING,
            estimated_pose=_pose(),
            map_update=snapshot,
        ),
    )

    metrics = lifecycle_metrics(updates, snapshot)

    assert metrics == (
        MetricResult(name="update_count", value=3.0, unit="count", family="lifecycle"),
        MetricResult(name="tracking_success_rate", value=1.0 / 3.0, unit="ratio", family="lifecycle"),
        MetricResult(name="lost_tracking_count", value=1.0, unit="count", family="lifecycle"),
        MetricResult(name="not_initialized_tracking_count", value=1.0, unit="count", family="lifecycle"),
        MetricResult(name="splat_count", value=2.0, unit="splats", family="lifecycle"),
    )


def test_trajectory_consistency_metrics_are_hook_flags_not_accuracy_claims() -> None:
    updates = (
        SplatSlamUpdate(
            timestamp=_timestamp(0),
            tracking_state=TrackingState.NOT_INITIALIZED,
            estimated_pose=None,
            map_update=SplatMap(frame=FrameId("map")),
        ),
        SplatSlamUpdate(
            timestamp=_timestamp(1),
            tracking_state=TrackingState.TRACKING,
            estimated_pose=_pose(x=1.0),
            map_update=SplatMap(frame=FrameId("map"), splats=(_splat(0.0),)),
        ),
    )

    metrics = trajectory_consistency_metrics(updates)

    assert metrics == (
        MetricResult(name="trajectory_pose_available", value=1.0, unit="flag", family="trajectory"),
        MetricResult(name="trajectory_pose_delta_consistent", value=1.0, unit="flag", family="trajectory"),
    )
    assert "ate" not in {metric.name for metric in metrics}
    assert "rmse" not in {metric.name for metric in metrics}


def test_map_quality_metrics_are_contract_proxies() -> None:
    snapshot = SplatMap(frame=FrameId("map"), splats=(_splat(0.0, "front"), _splat(1.0, "rear")))
    fusion = FusionResult(
        status="fused",
        fused_map=snapshot,
        diagnostics={"source_map_count": 2, "fusion_label": "preserved_not_optimized"},
    )

    metrics = map_quality_metrics(snapshot, expected_frame=FrameId("map"), fusion_result=fusion)

    assert metrics == (
        MetricResult(name="map_splat_count", value=2.0, unit="splats", family="map_quality"),
        MetricResult(name="map_frame_match", value=1.0, unit="flag", family="map_quality"),
        MetricResult(name="map_provenance_source_count", value=2.0, unit="count", family="map_quality"),
        MetricResult(name="fusion_diagnostic_presence", value=1.0, unit="flag", family="map_fusion"),
    )


def test_agent_query_stability_metrics_repeat_fixed_posterior_queries() -> None:
    snapshot = SplatMap(frame=FrameId("map"), splats=(_splat(0.0, "front"), _splat(2.0, "front")))
    view = SplatPosteriorView(snapshot)
    query = LocalRadiusQuery(center=(0.0, 0.0, 1.0), radius=1.5)

    metrics = agent_query_stability_metrics(view, query, repetitions=3)

    assert metrics == (
        MetricResult(name="agent_query_local_stable", value=1.0, unit="flag", family="agent_query"),
        MetricResult(name="agent_query_summary_stable", value=1.0, unit="flag", family="agent_query"),
        MetricResult(name="agent_query_provenance_stable", value=1.0, unit="flag", family="agent_query"),
        MetricResult(name="agent_query_repetition_count", value=3.0, unit="count", family="agent_query"),
    )


def _timestamp(index: int):
    from mosaic.core import Timestamp

    return Timestamp(index)


def _pose(x: float = 0.0):
    from mosaic.core import Pose3, Quaternion, Translation3

    return Pose3(
        parent_frame=FrameId("world"),
        child_frame=FrameId("camera/front"),
        translation=Translation3(x=x, y=0.0, z=0.0),
        rotation=Quaternion.identity(),
    )
