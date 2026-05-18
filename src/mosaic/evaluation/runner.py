from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Mapping, Sequence

from mosaic.evaluation.metrics import MetricResult, splat_count_metric
from mosaic.evaluation.scenarios import SyntheticScenario
from mosaic.slam import SplatSlamBackend

ArtifactValue = bool | int | float | str
MetricDict = dict[str, str | float]
ArtifactMapping = Mapping[str, ArtifactValue]


class FrozenMetricSequence(Sequence[MetricDict]):
    def __init__(self, metrics: Sequence[MetricDict]) -> None:
        self._metrics = tuple(MappingProxyType(dict(metric)) for metric in metrics)

    def __getitem__(self, index: int) -> MetricDict:
        return self._metrics[index]

    def __len__(self) -> int:
        return len(self._metrics)

    def __iter__(self) -> Iterator[MetricDict]:
        return iter(self._metrics)

    def __eq__(self, other: object) -> bool:
        return list(self) == other


@dataclass(frozen=True, slots=True)
class BenchmarkArtifact:
    scenario_name: str
    backend_name: str
    update_count: int
    metrics: Sequence[MetricDict]
    backend_metadata: ArtifactMapping = field(default_factory=dict)
    diagnostics: ArtifactMapping = field(default_factory=dict)
    failure_classification: str = "none"

    def __post_init__(self) -> None:
        object.__setattr__(self, "metrics", FrozenMetricSequence(self.metrics))
        object.__setattr__(self, "backend_metadata", MappingProxyType(dict(self.backend_metadata)))
        object.__setattr__(self, "diagnostics", MappingProxyType(dict(self.diagnostics)))
        if not self.failure_classification.strip():
            raise ValueError("BenchmarkArtifact failure_classification must not be blank")

    def as_dict(self) -> dict[str, str | int | list[MetricDict] | dict[str, ArtifactValue]]:
        return {
            "scenario_name": self.scenario_name,
            "backend_name": self.backend_name,
            "backend_metadata": dict(self.backend_metadata),
            "update_count": self.update_count,
            "metrics": [dict(metric) for metric in self.metrics],
            "diagnostics": dict(self.diagnostics),
            "failure_classification": self.failure_classification,
        }


def run_slam_benchmark(scenario: SyntheticScenario, backend: SplatSlamBackend) -> BenchmarkArtifact:
    backend.reset()
    update_count = 0
    diagnostics: dict[str, ArtifactValue] = {}
    for observation in scenario.sequence:
        update = backend.process(observation)
        update_count += 1
        for key, value in update.diagnostics.items():
            diagnostics[f"last_{key}"] = value
    snapshot = backend.snapshot()
    diagnostics["snapshot_splat_count"] = len(snapshot)
    metrics = [splat_count_metric(snapshot).as_dict()]
    return BenchmarkArtifact(
        scenario_name=scenario.name,
        backend_name=backend.name,
        update_count=update_count,
        metrics=metrics,
        backend_metadata=_backend_metadata(backend),
        diagnostics=diagnostics,
        failure_classification="none",
    )


def write_benchmark_artifact(artifact: BenchmarkArtifact, path: Path) -> None:
    path.write_text(json.dumps(artifact.as_dict(), indent=2, sort_keys=True) + "\n")


def _backend_metadata(backend: SplatSlamBackend) -> dict[str, ArtifactValue]:
    capabilities = backend.capabilities
    metadata: dict[str, ArtifactValue] = {
        "name": backend.name,
        "supports_multi_view": capabilities.supports_multi_view,
        "supports_incremental_mapping": capabilities.supports_incremental_mapping,
        "supports_uncertainty": capabilities.supports_uncertainty,
        "runs_out_of_process": capabilities.runs_out_of_process,
    }
    for key, value in capabilities.parameters.items():
        metadata[f"parameter_{key}"] = value
    return metadata


def _snapshot_metrics(backend: SplatSlamBackend) -> tuple[MetricResult, ...]:
    return (splat_count_metric(backend.snapshot()),)
