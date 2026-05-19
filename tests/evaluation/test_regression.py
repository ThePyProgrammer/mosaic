from mosaic.evaluation import (
    BenchmarkArtifact,
    FailureClass,
    RegressionGate,
    RegressionResult,
    check_regression_gates,
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


def test_primary_failure_class_uses_priority_not_gate_order_or_artifact_string() -> None:
    artifact = BenchmarkArtifact(
        scenario_name="scenario",
        backend_name="backend",
        update_count=0,
        metrics=[
            {"name": "agent_stability", "value": 0.0, "unit": "flag"},
            {"name": "fusion_diagnostics", "value": 0.0, "unit": "flag"},
            {"name": "trajectory_available", "value": 0.0, "unit": "flag"},
            {"name": "tracking_success_rate", "value": 0.0, "unit": "ratio"},
        ],
        backend_metadata={"name": "backend"},
        diagnostics={},
        failure_classification="arbitrary-caller-string",
    )
    results = check_regression_gates(
        artifact,
        (
            RegressionGate("agent_stability", 1.0, FailureClass.AGENT_QUERY),
            RegressionGate("fusion_diagnostics", 1.0, FailureClass.MAP_FUSION),
            RegressionGate("trajectory_available", 1.0, FailureClass.TRAJECTORY),
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
        RegressionGate("trajectory_available", 1.0, FailureClass.TRAJECTORY),
        RegressionGate("fusion_diagnostics", 1.0, FailureClass.MAP_FUSION),
        RegressionGate("agent_stability", 1.0, FailureClass.AGENT_QUERY),
    )

    results = check_regression_gates(artifact, gates)

    assert tuple(result.failure_class for result in results) == (
        FailureClass.LIFECYCLE,
        FailureClass.TRAJECTORY,
        FailureClass.MAP_FUSION,
        FailureClass.AGENT_QUERY,
    )
    assert len([result for result in results if not result.passed]) == 4
