from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Mapping, Sequence

from mosaic.evaluation.metrics import MetricResult, lifecycle_metrics, map_quality_metrics
from mosaic.evaluation.scenarios import SyntheticScenario, scenario_summary
from mosaic.slam import SplatSlamBackend

ArtifactValue = bool | int | float | str
MetricDict = dict[str, str | float]
ArtifactMapping = Mapping[str, ArtifactValue]
ScenarioSummaryValue = ArtifactValue | list[str]
ScenarioSummaryMapping = Mapping[str, ArtifactValue | Sequence[str]]
GateResultMapping = Mapping[str, ArtifactValue]


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


class FrozenGateResultSequence(Sequence[GateResultMapping]):
    def __init__(self, gate_results: Sequence[GateResultMapping]) -> None:
        self._gate_results = tuple(MappingProxyType(dict(gate_result)) for gate_result in gate_results)

    def __getitem__(self, index: int) -> GateResultMapping:
        return self._gate_results[index]

    def __len__(self) -> int:
        return len(self._gate_results)

    def __iter__(self) -> Iterator[GateResultMapping]:
        return iter(self._gate_results)

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
    scenario_summary: ScenarioSummaryMapping = field(default_factory=dict)
    gate_results: Sequence[GateResultMapping] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "metrics", FrozenMetricSequence(self.metrics))
        object.__setattr__(self, "backend_metadata", MappingProxyType(dict(self.backend_metadata)))
        object.__setattr__(self, "diagnostics", MappingProxyType(dict(self.diagnostics)))
        object.__setattr__(self, "scenario_summary", MappingProxyType(dict(self.scenario_summary)))
        object.__setattr__(self, "gate_results", FrozenGateResultSequence(self.gate_results))
        if not self.failure_classification.strip():
            raise ValueError("BenchmarkArtifact failure_classification must not be blank")

    def as_dict(
        self,
    ) -> dict[
        str,
        str | int | list[MetricDict] | list[dict[str, ArtifactValue]] | dict[str, ArtifactValue | list[str]],
    ]:
        return {
            "scenario_name": self.scenario_name,
            "backend_name": self.backend_name,
            "backend_metadata": dict(self.backend_metadata),
            "update_count": self.update_count,
            "metrics": [dict(metric) for metric in self.metrics],
            "diagnostics": dict(self.diagnostics),
            "failure_classification": self.failure_classification,
            "scenario_summary": _scenario_summary_as_dict(self.scenario_summary),
            "gate_results": [dict(gate_result) for gate_result in self.gate_results],
        }


def run_slam_benchmark(scenario: SyntheticScenario, backend: SplatSlamBackend) -> BenchmarkArtifact:
    backend.reset()
    update_count = 0
    updates = []
    diagnostics: dict[str, ArtifactValue] = {}
    for observation in scenario.sequence:
        update = backend.process(observation)
        updates.append(update)
        update_count += 1
        for key, value in update.diagnostics.items():
            diagnostics[f"last_{key}"] = value
    snapshot = backend.snapshot()
    diagnostics["snapshot_splat_count"] = len(snapshot)
    metrics = [
        *(metric.as_dict() for metric in lifecycle_metrics(updates, snapshot)),
        *(metric.as_dict() for metric in map_quality_metrics(snapshot, expected_frame=snapshot.frame)),
    ]
    _mirror_metric_diagnostics(metrics, diagnostics)
    return BenchmarkArtifact(
        scenario_name=scenario.name,
        backend_name=backend.name,
        update_count=update_count,
        metrics=metrics,
        backend_metadata=_backend_metadata(backend),
        diagnostics=diagnostics,
        failure_classification="none",
        scenario_summary=scenario_summary(
            scenario,
            update_count=update_count,
            expected_map_frame=snapshot.frame,
        ),
        gate_results=(),
    )


def write_benchmark_artifact(artifact: BenchmarkArtifact, path: Path) -> None:
    path.write_text(json.dumps(artifact.as_dict(), indent=2, sort_keys=True) + "\n")


def write_benchmark_artifacts_jsonl(artifacts: Sequence[BenchmarkArtifact], path: Path) -> None:
    path.write_text("".join(json.dumps(artifact.as_dict(), sort_keys=True) + "\n" for artifact in artifacts))


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


def _mirror_metric_diagnostics(metrics: Sequence[MetricDict], diagnostics: dict[str, ArtifactValue]) -> None:
    for metric in metrics:
        name = str(metric["name"])
        if name in {
            "update_count",
            "lost_tracking_count",
            "not_initialized_tracking_count",
            "splat_count",
        }:
            diagnostics[f"metric_{name}"] = float(metric["value"])


def _scenario_summary_as_dict(
    summary: ScenarioSummaryMapping,
) -> dict[str, ArtifactValue | list[str]]:
    serialized: dict[str, ArtifactValue | list[str]] = {}
    for key, value in summary.items():
        if key == "camera_ids" and not isinstance(value, str):
            serialized[key] = list(value)
        else:
            serialized[key] = value if isinstance(value, bool | int | float | str) else list(value)
    return serialized


def _snapshot_metrics(backend: SplatSlamBackend) -> tuple[MetricResult, ...]:
    snapshot = backend.snapshot()
    return (*lifecycle_metrics((), snapshot), *map_quality_metrics(snapshot, expected_frame=snapshot.frame))
