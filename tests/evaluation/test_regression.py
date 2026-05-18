from mosaic.evaluation import BenchmarkArtifact, RegressionGate, RegressionResult, check_regression_gates


def _artifact(splat_count: float, update_count: int = 3) -> BenchmarkArtifact:
    return BenchmarkArtifact(
        scenario_name="synthetic-forward-3",
        backend_name="deterministic-splat",
        update_count=update_count,
        metrics=[{"name": "splat_count", "value": splat_count, "unit": "splats"}],
    )


def test_regression_gate_passes_when_metric_meets_minimum() -> None:
    results = check_regression_gates(_artifact(3.0), (RegressionGate(metric_name="splat_count", minimum=3.0),))

    assert results == (RegressionResult(metric_name="splat_count", passed=True, observed=3.0, threshold=3.0),)


def test_regression_gate_fails_when_metric_is_too_low() -> None:
    results = check_regression_gates(_artifact(2.0), (RegressionGate(metric_name="splat_count", minimum=3.0),))

    assert results == (RegressionResult(metric_name="splat_count", passed=False, observed=2.0, threshold=3.0),)


def test_regression_gate_fails_when_metric_is_missing() -> None:
    artifact = BenchmarkArtifact(scenario_name="scenario", backend_name="backend", update_count=0, metrics=[])

    results = check_regression_gates(artifact, (RegressionGate(metric_name="splat_count", minimum=1.0),))

    assert results == (RegressionResult(metric_name="splat_count", passed=False, observed=None, threshold=1.0),)
