from __future__ import annotations

from dataclasses import dataclass

from mosaic.evaluation.runner import BenchmarkArtifact


@dataclass(frozen=True, slots=True)
class RegressionGate:
    metric_name: str
    minimum: float

    def __post_init__(self) -> None:
        if not self.metric_name.strip():
            raise ValueError("RegressionGate metric_name must not be blank")


@dataclass(frozen=True, slots=True)
class RegressionResult:
    metric_name: str
    passed: bool
    observed: float | None
    threshold: float


def check_regression_gates(artifact: BenchmarkArtifact, gates: tuple[RegressionGate, ...]) -> tuple[RegressionResult, ...]:
    metrics = {str(metric["name"]): float(metric["value"]) for metric in artifact.metrics}
    results: list[RegressionResult] = []
    for gate in gates:
        observed = metrics.get(gate.metric_name)
        results.append(
            RegressionResult(
                metric_name=gate.metric_name,
                passed=observed is not None and observed >= gate.minimum,
                observed=observed,
                threshold=gate.minimum,
            )
        )
    return tuple(results)
