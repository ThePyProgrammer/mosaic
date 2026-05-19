import pytest

from mosaic.evaluation import (
    BenchmarkArtifact,
    EvaluationReadinessResult,
    FailureClass,
    RegressionGate,
    RegressionResult,
    check_regression_gates,
    evaluation_ready_for_real_backend,
    primary_failure_class,
)


def _artifact(splat_count: float, update_count: int = 3) -> BenchmarkArtifact:
    return BenchmarkArtifact(
        scenario_name="synthetic-forward-3",
        backend_name="deterministic-splat",
        update_count=update_count,
        metrics=[{"name": "splat_count", "value": splat_count, "unit": "splats"}],
        backend_metadata={"name": "deterministic-splat"},
        diagnostics={"snapshot_splat_count": int(splat_count)},
        failure_classification="none",
    )


def test_failure_class_exposes_closed_string_values() -> None:
    assert FailureClass.NONE.value == "none"
    assert FailureClass.LIFECYCLE.value == "lifecycle"
    assert FailureClass.TRAJECTORY.value == "trajectory"
    assert FailureClass.MAP_FUSION.value == "map_fusion"
    assert FailureClass.AGENT_QUERY.value == "agent_query"


def test_regression_gate_passes_when_metric_meets_minimum() -> None:
    results = check_regression_gates(
        _artifact(3.0),
        (RegressionGate(metric_name="splat_count", minimum=3.0, failure_class=FailureClass.MAP_FUSION),),
    )

    assert results == (
        RegressionResult(
            metric_name="splat_count",
            passed=True,
            observed=3.0,
            threshold=3.0,
            failure_class=FailureClass.MAP_FUSION,
        ),
    )
    assert primary_failure_class(results) is FailureClass.NONE


def test_regression_gate_fails_when_metric_is_too_low() -> None:
    results = check_regression_gates(
        _artifact(2.0),
        (RegressionGate(metric_name="splat_count", minimum=3.0, failure_class=FailureClass.MAP_FUSION),),
    )

    assert results == (
        RegressionResult(
            metric_name="splat_count",
            passed=False,
            observed=2.0,
            threshold=3.0,
            failure_class=FailureClass.MAP_FUSION,
        ),
    )
    assert primary_failure_class(results) is FailureClass.MAP_FUSION


def test_regression_gate_fails_when_metric_is_missing() -> None:
    artifact = BenchmarkArtifact(
        scenario_name="scenario",
        backend_name="backend",
        update_count=0,
        metrics=[],
        backend_metadata={"name": "backend"},
        diagnostics={},
        failure_classification="none",
    )

    results = check_regression_gates(
        artifact,
        (RegressionGate(metric_name="splat_count", minimum=1.0, failure_class=FailureClass.TRAJECTORY),),
    )

    assert results == (
        RegressionResult(
            metric_name="splat_count",
            passed=False,
            observed=None,
            threshold=1.0,
            failure_class=FailureClass.TRAJECTORY,
        ),
    )
    assert primary_failure_class(results) is FailureClass.TRAJECTORY


def test_regression_gate_rejects_duplicated_metric_names() -> None:
    artifact = BenchmarkArtifact(
        scenario_name="scenario",
        backend_name="backend",
        update_count=0,
        metrics=[
            {"name": "tracking_success_rate", "value": 0.0, "unit": "ratio"},
            {"name": "tracking_success_rate", "value": 1.0, "unit": "ratio"},
        ],
        backend_metadata={"name": "backend"},
        diagnostics={},
        failure_classification="none",
    )

    with pytest.raises(ValueError, match="duplicated"):
        check_regression_gates(
            artifact,
            (RegressionGate("tracking_success_rate", 1.0, FailureClass.LIFECYCLE),),
        )


@pytest.mark.parametrize("value", [float("inf"), float("nan"), "inf", "nan"])
def test_regression_gate_rejects_non_finite_metric_values(value: float | str) -> None:
    artifact = BenchmarkArtifact(
        scenario_name="scenario",
        backend_name="backend",
        update_count=0,
        metrics=[{"name": "tracking_success_rate", "value": value, "unit": "ratio"}],
        backend_metadata={"name": "backend"},
        diagnostics={},
        failure_classification="none",
    )

    with pytest.raises(ValueError, match="finite"):
        check_regression_gates(
            artifact,
            (RegressionGate("tracking_success_rate", 1.0, FailureClass.LIFECYCLE),),
        )


def test_regression_gate_rejects_non_finite_thresholds() -> None:
    with pytest.raises(ValueError, match="minimum"):
        RegressionGate("tracking_success_rate", float("inf"), FailureClass.LIFECYCLE)
    with pytest.raises(ValueError, match="maximum"):
        RegressionGate("tracking_success_rate", 0.0, FailureClass.LIFECYCLE, maximum=float("inf"))


def test_primary_failure_class_uses_priority_not_gate_order_or_artifact_string() -> None:
    artifact = BenchmarkArtifact(
        scenario_name="scenario",
        backend_name="backend",
        update_count=0,
        metrics=[
            {"name": "agent_query_local_stable", "value": 0.0, "unit": "flag"},
            {"name": "fusion_diagnostic_presence", "value": 0.0, "unit": "flag"},
            {"name": "trajectory_pose_available", "value": 0.0, "unit": "flag"},
            {"name": "tracking_success_rate", "value": 0.0, "unit": "ratio"},
        ],
        backend_metadata={"name": "backend"},
        diagnostics={},
        failure_classification="arbitrary-caller-string",
    )
    results = check_regression_gates(
        artifact,
        (
            RegressionGate("agent_query_local_stable", 1.0, FailureClass.AGENT_QUERY),
            RegressionGate("fusion_diagnostic_presence", 1.0, FailureClass.MAP_FUSION),
            RegressionGate("trajectory_pose_available", 1.0, FailureClass.TRAJECTORY),
            RegressionGate("tracking_success_rate", 1.0, FailureClass.LIFECYCLE),
        ),
    )

    assert [result.failure_class for result in results if not result.passed] == [
        FailureClass.AGENT_QUERY,
        FailureClass.MAP_FUSION,
        FailureClass.TRAJECTORY,
        FailureClass.LIFECYCLE,
    ]
    assert primary_failure_class(results) is FailureClass.LIFECYCLE


def _readiness_artifact(**metric_values: float) -> BenchmarkArtifact:
    return BenchmarkArtifact(
        scenario_name="scenario",
        backend_name="backend",
        update_count=3,
        metrics=[{"name": name, "value": value, "unit": "score"} for name, value in metric_values.items()],
        backend_metadata={"name": "backend"},
        diagnostics={},
        failure_classification="caller-controlled-value-is-ignored",
    )


def _complete_gate_suite() -> tuple[RegressionGate, ...]:
    return (
        RegressionGate("tracking_success_rate", 1.0, FailureClass.LIFECYCLE),
        RegressionGate("trajectory_pose_available", 1.0, FailureClass.TRAJECTORY),
        RegressionGate("fusion_diagnostic_presence", 1.0, FailureClass.MAP_FUSION),
        RegressionGate("agent_query_local_stable", 1.0, FailureClass.AGENT_QUERY),
    )


def test_every_failure_class_can_be_retained_on_failed_results() -> None:
    artifact = BenchmarkArtifact(
        scenario_name="scenario",
        backend_name="backend",
        update_count=0,
        metrics=[],
        backend_metadata={"name": "backend"},
        diagnostics={},
        failure_classification="none",
    )
    gates = (
        RegressionGate("tracking_success_rate", 1.0, FailureClass.LIFECYCLE),
        RegressionGate("trajectory_pose_available", 1.0, FailureClass.TRAJECTORY),
        RegressionGate("fusion_diagnostic_presence", 1.0, FailureClass.MAP_FUSION),
        RegressionGate("agent_query_local_stable", 1.0, FailureClass.AGENT_QUERY),
    )

    results = check_regression_gates(artifact, gates)

    assert tuple(result.failure_class for result in results) == (
        FailureClass.LIFECYCLE,
        FailureClass.TRAJECTORY,
        FailureClass.MAP_FUSION,
        FailureClass.AGENT_QUERY,
    )
    assert len([result for result in results if not result.passed]) == 4


def test_regression_result_serializes_failure_class_value() -> None:
    result = RegressionResult(
        metric_name="not_initialized_tracking_count",
        passed=False,
        observed=1.0,
        threshold=0.0,
        failure_class=FailureClass.LIFECYCLE,
    )

    assert result.as_dict() == {
        "metric_name": "not_initialized_tracking_count",
        "passed": False,
        "observed": 1.0,
        "threshold": 0.0,
        "failure_class": "lifecycle",
    }


def test_readiness_blocks_empty_gate_suite() -> None:
    result = evaluation_ready_for_real_backend(
        _readiness_artifact(),
        (),
    )

    assert result == EvaluationReadinessResult(
        ready=False,
        primary_failure_class=FailureClass.NONE,
        gate_results=(),
        missing_failure_classes=(
            FailureClass.LIFECYCLE,
            FailureClass.TRAJECTORY,
            FailureClass.MAP_FUSION,
            FailureClass.AGENT_QUERY,
        ),
    )


def test_readiness_blocks_incomplete_gate_suite() -> None:
    result = evaluation_ready_for_real_backend(
        _readiness_artifact(tracking_success_rate=1.0),
        (RegressionGate("tracking_success_rate", 1.0, FailureClass.LIFECYCLE),),
    )

    assert result.ready is False
    assert result.primary_failure_class is FailureClass.NONE
    assert result.missing_failure_classes == (
        FailureClass.TRAJECTORY,
        FailureClass.MAP_FUSION,
        FailureClass.AGENT_QUERY,
    )


def test_readiness_blocks_failed_lifecycle_tracking_success_gate() -> None:
    result = evaluation_ready_for_real_backend(
        _readiness_artifact(
            tracking_success_rate=0.0,
            trajectory_pose_available=1.0,
            fusion_diagnostic_presence=1.0,
            agent_query_local_stable=1.0,
        ),
        _complete_gate_suite(),
    )

    assert result.ready is False
    assert result.primary_failure_class is FailureClass.LIFECYCLE
    assert result.gate_results[0].failure_class is FailureClass.LIFECYCLE


def test_readiness_blocks_lost_tracking_lifecycle_gate() -> None:
    result = evaluation_ready_for_real_backend(
        _readiness_artifact(
            lost_tracking_count=1.0,
            trajectory_pose_available=1.0,
            fusion_diagnostic_presence=1.0,
            agent_query_local_stable=1.0,
        ),
        (
            RegressionGate("lost_tracking_count", 0.0, FailureClass.LIFECYCLE, maximum=0.0),
            RegressionGate("trajectory_pose_available", 1.0, FailureClass.TRAJECTORY),
            RegressionGate("fusion_diagnostic_presence", 1.0, FailureClass.MAP_FUSION),
            RegressionGate("agent_query_local_stable", 1.0, FailureClass.AGENT_QUERY),
        ),
    )

    assert result.ready is False
    assert result.primary_failure_class is FailureClass.LIFECYCLE


def test_readiness_blocks_not_initialized_lifecycle_gate() -> None:
    result = evaluation_ready_for_real_backend(
        _readiness_artifact(
            not_initialized_tracking_count=1.0,
            trajectory_pose_available=1.0,
            fusion_diagnostic_presence=1.0,
            agent_query_local_stable=1.0,
        ),
        (
            RegressionGate("not_initialized_tracking_count", 0.0, FailureClass.LIFECYCLE, maximum=0.0),
            RegressionGate("trajectory_pose_available", 1.0, FailureClass.TRAJECTORY),
            RegressionGate("fusion_diagnostic_presence", 1.0, FailureClass.MAP_FUSION),
            RegressionGate("agent_query_local_stable", 1.0, FailureClass.AGENT_QUERY),
        ),
    )

    assert result.ready is False
    assert result.primary_failure_class is FailureClass.LIFECYCLE
    assert result.gate_results[0].metric_name == "not_initialized_tracking_count"


def test_readiness_passes_only_for_complete_passing_gate_suite() -> None:
    result = evaluation_ready_for_real_backend(
        _readiness_artifact(
            tracking_success_rate=1.0,
            trajectory_pose_available=1.0,
            fusion_diagnostic_presence=1.0,
            agent_query_local_stable=1.0,
        ),
        _complete_gate_suite(),
    )

    assert result.ready is True
    assert result.primary_failure_class is FailureClass.NONE
    assert result.missing_failure_classes == ()
    assert all(gate_result.passed for gate_result in result.gate_results)
