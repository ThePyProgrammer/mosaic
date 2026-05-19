import json

import pytest

from mosaic.artifacts import (
    benchmark_artifact_from_artifact,
    benchmark_artifact_to_artifact,
    metric_result_from_artifact,
    metric_result_to_artifact,
    regression_result_from_artifact,
    regression_result_to_artifact,
    splat_slam_update_from_artifact,
    splat_slam_update_to_artifact,
)
from mosaic.core import FrameId, Pose3, Quaternion, Timestamp, Translation3
from mosaic.evaluation import BenchmarkArtifact, MetricResult, RegressionResult, write_benchmark_artifact
from mosaic.slam import SplatSlamUpdate, TrackingState
from mosaic.splats import GaussianSplat, SplatMap


def _pose() -> Pose3:
    return Pose3(
        parent_frame=FrameId("map"),
        child_frame=FrameId("camera/front"),
        translation=Translation3(x=1.0, y=2.0, z=3.0),
        rotation=Quaternion.identity(),
    )


def _splat_map() -> SplatMap:
    return SplatMap(
        frame=FrameId("map"),
        splats=(
            GaussianSplat(
                center=(0.0, 0.0, 1.0),
                covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1),
                color_rgb=(0.2, 0.3, 0.4),
                opacity=0.75,
                provenance="front-camera",
            ),
        ),
    )


def test_splat_slam_update_artifact_round_trips_tracking_update() -> None:
    update = SplatSlamUpdate(
        timestamp=Timestamp(1_000_000_000),
        tracking_state=TrackingState.TRACKING,
        estimated_pose=_pose(),
        map_update=_splat_map(),
        diagnostics={"quality": 1.0, "accepted": True, "label": "deterministic"},
    )

    artifact = splat_slam_update_to_artifact(update)
    restored = splat_slam_update_from_artifact(artifact)

    assert artifact["schema"] == "mosaic.splat_slam_update"
    assert artifact["payload"]["tracking_state"] == "tracking"
    assert restored.timestamp == update.timestamp
    assert restored.tracking_state is TrackingState.TRACKING
    assert restored.estimated_pose == update.estimated_pose
    assert restored.map_update == update.map_update
    assert restored.diagnostics == update.diagnostics
    json.dumps(artifact, sort_keys=True)


def test_splat_slam_update_artifact_round_trips_lost_update_without_pose() -> None:
    update = SplatSlamUpdate(
        timestamp=Timestamp(1_000_000_000),
        tracking_state=TrackingState.LOST,
        estimated_pose=None,
        map_update=_splat_map(),
        diagnostics={"quality": 0.0, "accepted": False, "label": "lost"},
    )

    artifact = splat_slam_update_to_artifact(update)
    restored = splat_slam_update_from_artifact(artifact)

    assert artifact["payload"]["tracking_state"] == "lost"
    assert restored.tracking_state is TrackingState.LOST
    assert restored.estimated_pose is None
    assert restored.map_update == update.map_update
    assert restored.diagnostics == update.diagnostics


def test_splat_slam_update_artifact_rejects_unknown_schema_version() -> None:
    update = SplatSlamUpdate(
        timestamp=Timestamp(1_000_000_000),
        tracking_state=TrackingState.LOST,
        estimated_pose=None,
        map_update=_splat_map(),
    )
    artifact = splat_slam_update_to_artifact(update)
    artifact["schema_version"] = 2

    with pytest.raises(ValueError, match="schema_version"):
        splat_slam_update_from_artifact(artifact)


def test_metric_result_artifact_round_trips() -> None:
    metric = MetricResult(name="splat_count", value=2.0, unit="splats")

    artifact = metric_result_to_artifact(metric)
    restored = metric_result_from_artifact(artifact)

    assert artifact["schema"] == "mosaic.metric_result"
    assert artifact["payload"] == {
        "name": "splat_count",
        "value": 2.0,
        "unit": "splats",
        "family": "general",
    }
    assert restored == metric


def test_regression_result_artifact_round_trips() -> None:
    result = RegressionResult(metric_name="splat_count", passed=True, observed=2.0, threshold=1.0)

    artifact = regression_result_to_artifact(result)
    restored = regression_result_from_artifact(artifact)

    assert artifact["schema"] == "mosaic.regression_result"
    assert restored == result


def test_regression_result_artifact_preserves_missing_observed_value() -> None:
    result = RegressionResult(metric_name="splat_count", passed=False, observed=None, threshold=1.0)

    artifact = regression_result_to_artifact(result)
    restored = regression_result_from_artifact(artifact)

    assert artifact["payload"]["observed"] is None
    assert restored.observed is None


def test_benchmark_artifact_as_dict_is_not_general_schema_envelope() -> None:
    artifact = _benchmark_artifact()

    serialized = artifact.as_dict()

    assert serialized == {
        "scenario_name": "scenario",
        "backend_name": "backend",
        "backend_metadata": {"name": "backend"},
        "update_count": 1,
        "metrics": [{"name": "splat_count", "value": 1.0, "unit": "splats"}],
        "diagnostics": {"snapshot_splat_count": 1},
        "failure_classification": "none",
    }
    assert "schema" not in serialized
    assert "schema_version" not in serialized
    assert "payload" not in serialized


def test_benchmark_artifact_wrapper_uses_explicit_schema_envelope() -> None:
    artifact = _benchmark_artifact()

    envelope = benchmark_artifact_to_artifact(artifact)
    restored = benchmark_artifact_from_artifact(envelope)

    assert envelope["schema"] == "mosaic.benchmark_artifact"
    assert envelope["schema_version"] == 1
    assert envelope["payload"] == artifact.as_dict()
    assert restored == artifact


def test_write_benchmark_artifact_keeps_narrow_deterministic_json(tmp_path) -> None:
    artifact = _benchmark_artifact()
    path = tmp_path / "artifact.json"

    write_benchmark_artifact(artifact, path)

    text = path.read_text()
    assert json.loads(text) == artifact.as_dict()
    assert "schema" not in json.loads(text)
    assert text.startswith("{\n  \"backend_metadata\"")
    assert text.endswith("\n")


def test_evaluation_artifact_rejects_unknown_schema_version() -> None:
    artifact = metric_result_to_artifact(MetricResult(name="splat_count", value=2.0, unit="splats"))
    artifact["schema_version"] = 2

    with pytest.raises(ValueError, match="schema_version"):
        metric_result_from_artifact(artifact)


def _benchmark_artifact() -> BenchmarkArtifact:
    return BenchmarkArtifact(
        scenario_name="scenario",
        backend_name="backend",
        update_count=1,
        metrics=[{"name": "splat_count", "value": 1.0, "unit": "splats"}],
        backend_metadata={"name": "backend"},
        diagnostics={"snapshot_splat_count": 1},
        failure_classification="none",
    )
