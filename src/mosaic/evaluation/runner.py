from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from mosaic.evaluation.metrics import MetricResult, splat_count_metric
from mosaic.evaluation.scenarios import SyntheticScenario
from mosaic.slam import SplatSlamBackend

MetricDict = dict[str, str | float]


@dataclass(frozen=True, slots=True)
class BenchmarkArtifact:
    scenario_name: str
    backend_name: str
    update_count: int
    metrics: Sequence[MetricDict]

    def as_dict(self) -> dict[str, str | int | list[MetricDict]]:
        return {
            "scenario_name": self.scenario_name,
            "backend_name": self.backend_name,
            "update_count": self.update_count,
            "metrics": list(self.metrics),
        }


def run_slam_benchmark(scenario: SyntheticScenario, backend: SplatSlamBackend) -> BenchmarkArtifact:
    backend.reset()
    update_count = 0
    for observation in scenario.sequence:
        backend.process(observation)
        update_count += 1
    metrics = [_metric.as_dict() for _metric in _snapshot_metrics(backend)]
    return BenchmarkArtifact(
        scenario_name=scenario.name,
        backend_name=backend.name,
        update_count=update_count,
        metrics=metrics,
    )


def write_benchmark_artifact(artifact: BenchmarkArtifact, path: Path) -> None:
    path.write_text(json.dumps(artifact.as_dict(), indent=2, sort_keys=True) + "\n")


def _snapshot_metrics(backend: SplatSlamBackend) -> tuple[MetricResult, ...]:
    return (splat_count_metric(backend.snapshot()),)
