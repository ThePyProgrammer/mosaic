from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from math import isfinite
from typing import Sequence

from mosaic.evaluation.runner import BenchmarkArtifact


class FailureClass(StrEnum):
    NONE = "none"
    LIFECYCLE = "lifecycle"
    TRAJECTORY = "trajectory"
    MAP_FUSION = "map_fusion"
    AGENT_QUERY = "agent_query"


_FAILURE_PRIORITY = (
    FailureClass.LIFECYCLE,
    FailureClass.TRAJECTORY,
    FailureClass.MAP_FUSION,
    FailureClass.AGENT_QUERY,
    FailureClass.NONE,
)
_REQUIRED_READINESS_CLASSES = (
    FailureClass.LIFECYCLE,
    FailureClass.TRAJECTORY,
    FailureClass.MAP_FUSION,
    FailureClass.AGENT_QUERY,
)


@dataclass(frozen=True, slots=True)
class RegressionGate:
    metric_name: str
    minimum: float
    failure_class: FailureClass = FailureClass.MAP_FUSION
    maximum: float | None = None

    def __post_init__(self) -> None:
        if not self.metric_name.strip():
            raise ValueError("RegressionGate metric_name must not be blank")
        if not isfinite(self.minimum):
            raise ValueError("RegressionGate minimum must be finite")
        if self.maximum is not None and not isfinite(self.maximum):
            raise ValueError("RegressionGate maximum must be finite")
        if self.failure_class is FailureClass.NONE:
            raise ValueError("RegressionGate failure_class must represent a concrete failure")
        if self.maximum is not None and self.minimum > self.maximum:
            raise ValueError("RegressionGate minimum must not exceed maximum")


@dataclass(frozen=True, slots=True)
class RegressionResult:
    metric_name: str
    passed: bool
    observed: float | None
    threshold: float
    failure_class: FailureClass = FailureClass.MAP_FUSION

    def as_dict(self) -> dict[str, bool | float | str | None]:
        return {
            "metric_name": self.metric_name,
            "passed": self.passed,
            "observed": self.observed,
            "threshold": self.threshold,
            "failure_class": self.failure_class.value,
        }


@dataclass(frozen=True, slots=True)
class EvaluationReadinessResult:
    ready: bool
    primary_failure_class: FailureClass
    gate_results: tuple[RegressionResult, ...]
    missing_failure_classes: tuple[FailureClass, ...]

    def as_dict(self) -> dict[str, bool | str | list[dict[str, bool | float | str | None]] | list[str]]:
        return {
            "ready": self.ready,
            "primary_failure_class": self.primary_failure_class.value,
            "gate_results": [result.as_dict() for result in self.gate_results],
            "missing_failure_classes": [failure_class.value for failure_class in self.missing_failure_classes],
        }


def check_regression_gates(
    artifact: BenchmarkArtifact,
    gates: tuple[RegressionGate, ...],
) -> tuple[RegressionResult, ...]:
    metrics: dict[str, float] = {}
    for metric in artifact.metrics:
        name = str(metric["name"])
        if name in metrics:
            raise ValueError(f"BenchmarkArtifact metric name is duplicated: {name}")
        value = float(metric["value"])
        if not isfinite(value):
            raise ValueError(f"BenchmarkArtifact metric value must be finite: {name}")
        metrics[name] = value
    results: list[RegressionResult] = []
    for gate in gates:
        observed = metrics.get(gate.metric_name)
        threshold = gate.maximum if gate.maximum is not None else gate.minimum
        passed = observed is not None and observed >= gate.minimum
        if passed and gate.maximum is not None:
            passed = observed <= gate.maximum
        results.append(
            RegressionResult(
                metric_name=gate.metric_name,
                passed=passed,
                observed=observed,
                threshold=threshold,
                failure_class=gate.failure_class,
            )
        )
    return tuple(results)


def primary_failure_class(results: Sequence[RegressionResult]) -> FailureClass:
    failed_classes = {result.failure_class for result in results if not result.passed}
    for failure_class in _FAILURE_PRIORITY:
        if failure_class in failed_classes:
            return failure_class
    return FailureClass.NONE


def evaluation_ready_for_real_backend(
    artifact: BenchmarkArtifact,
    gates: tuple[RegressionGate, ...],
) -> EvaluationReadinessResult:
    gate_results = check_regression_gates(artifact, gates)
    covered_classes = {gate.failure_class for gate in gates}
    missing_failure_classes = tuple(
        failure_class for failure_class in _REQUIRED_READINESS_CLASSES if failure_class not in covered_classes
    )
    primary_class = primary_failure_class(gate_results)
    ready = bool(gates) and not missing_failure_classes and primary_class is FailureClass.NONE
    return EvaluationReadinessResult(
        ready=ready,
        primary_failure_class=primary_class,
        gate_results=gate_results,
        missing_failure_classes=missing_failure_classes,
    )
