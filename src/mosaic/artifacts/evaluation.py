from __future__ import annotations

from typing import cast

from mosaic.artifacts.schema import ArtifactDict, make_artifact, require_artifact
from mosaic.evaluation import BenchmarkArtifact, FailureClass, MetricResult, RegressionResult
from mosaic.evaluation.runner import ArtifactValue, MetricDict


def metric_result_to_artifact(metric: MetricResult) -> ArtifactDict:
    return make_artifact("mosaic.metric_result", metric.as_dict())


def metric_result_from_artifact(artifact: object) -> MetricResult:
    payload = require_artifact(artifact, "mosaic.metric_result")
    return MetricResult(
        name=cast(str, payload["name"]),
        value=cast(float, payload["value"]),
        unit=cast(str, payload["unit"]),
        family=cast(str, payload.get("family", "general")),
    )


def regression_result_to_artifact(result: RegressionResult) -> ArtifactDict:
    return make_artifact(
        "mosaic.regression_result",
        result.as_dict(),
    )


def regression_result_from_artifact(artifact: object) -> RegressionResult:
    payload = require_artifact(artifact, "mosaic.regression_result")
    return RegressionResult(
        metric_name=cast(str, payload["metric_name"]),
        passed=cast(bool, payload["passed"]),
        observed=cast(float | None, payload["observed"]),
        threshold=cast(float, payload["threshold"]),
        failure_class=FailureClass(cast(str, payload.get("failure_class", FailureClass.MAP_FUSION.value))),
    )


def benchmark_artifact_to_artifact(artifact: BenchmarkArtifact) -> ArtifactDict:
    return make_artifact("mosaic.benchmark_artifact", artifact.as_dict())


def benchmark_artifact_from_artifact(artifact: object) -> BenchmarkArtifact:
    payload = require_artifact(artifact, "mosaic.benchmark_artifact")
    return BenchmarkArtifact(
        scenario_name=cast(str, payload["scenario_name"]),
        backend_name=cast(str, payload["backend_name"]),
        update_count=cast(int, payload["update_count"]),
        metrics=cast(list[MetricDict], payload["metrics"]),
        backend_metadata=cast(dict[str, ArtifactValue], payload["backend_metadata"]),
        diagnostics=cast(dict[str, ArtifactValue], payload["diagnostics"]),
        failure_classification=cast(str, payload["failure_classification"]),
    )
