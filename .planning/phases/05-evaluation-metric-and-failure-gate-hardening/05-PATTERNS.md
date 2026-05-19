# Phase 5: Evaluation Metric and Failure Gate Hardening - Pattern Map

**Mapped:** 2026-05-19
**Files analyzed:** 11 new/modified files
**Analogs found:** 11 / 11

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `src/mosaic/evaluation/metrics.py` | model/utility | transform | `src/mosaic/evaluation/metrics.py` | exact |
| `src/mosaic/evaluation/runner.py` | service/utility | batch + file-I/O | `src/mosaic/evaluation/runner.py` | exact |
| `src/mosaic/evaluation/regression.py` | model/utility | transform | `src/mosaic/evaluation/regression.py` | exact |
| `src/mosaic/evaluation/scenarios.py` | model/factory | batch | `src/mosaic/evaluation/scenarios.py` | exact |
| `src/mosaic/evaluation/__init__.py` | config/export surface | request-response import | `src/mosaic/evaluation/__init__.py` | exact |
| `src/mosaic/__init__.py` | config/export surface | request-response import | `src/mosaic/__init__.py` | exact |
| `tests/evaluation/test_metrics.py` | test | transform | `tests/evaluation/test_metrics.py` | exact |
| `tests/evaluation/test_runner.py` | test | batch + file-I/O | `tests/evaluation/test_runner.py` | exact |
| `tests/evaluation/test_regression.py` | test | transform | `tests/evaluation/test_regression.py` | exact |
| `tests/evaluation/test_scenarios.py` | test | batch | `tests/evaluation/test_scenarios.py` | role-match |
| `README.md` | documentation | request-response import examples | `README.md` | exact |

## Pattern Assignments

### `src/mosaic/evaluation/metrics.py` (model/utility, transform)

**Analog:** `src/mosaic/evaluation/metrics.py`

**Imports pattern** (lines 1-5):
```python
from __future__ import annotations

from dataclasses import dataclass

from mosaic.splats import SplatMap
```

**Frozen metric contract pattern** (lines 8-21):
```python
@dataclass(frozen=True, slots=True)
class MetricResult:
    name: str
    value: float
    unit: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("MetricResult name must not be blank")
        if not self.unit.strip():
            raise ValueError("MetricResult unit must not be blank")

    def as_dict(self) -> dict[str, str | float]:
        return {"name": self.name, "value": self.value, "unit": self.unit}
```

**Core constructor pattern** (lines 24-25):
```python
def splat_count_metric(snapshot: SplatMap) -> MetricResult:
    return MetricResult(name="splat_count", value=float(len(snapshot)), unit="splats")
```

**Apply to Phase 5:** Preserve frozen `MetricResult` and `as_dict()` JSON boundary. Add typed family/category fields or constructors additively. Use numeric `float` metric values for gate thresholds unless the planner deliberately widens `MetricResult.value` and all artifact/test surfaces.

---

### `src/mosaic/evaluation/runner.py` (service/utility, batch + file-I/O)

**Analog:** `src/mosaic/evaluation/runner.py`

**Imports and type alias pattern** (lines 1-16):
```python
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
```

**Frozen sequence/copy pattern** (lines 19-33):
```python
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
```

**Benchmark artifact serialization pattern** (lines 36-62):
```python
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
```

**Benchmark execution pattern** (lines 65-85):
```python
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
```

**Stable JSON writer pattern** (lines 88-89):
```python
def write_benchmark_artifact(artifact: BenchmarkArtifact, path: Path) -> None:
    path.write_text(json.dumps(artifact.as_dict(), indent=2, sort_keys=True) + "\n")
```

**Backend metadata pattern** (lines 92-103):
```python
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
```

**Apply to Phase 5:** Extend, do not replace, `BenchmarkArtifact.as_dict()` fields. Add scenario summaries, gate results, and typed failure data as copied/frozen fields. Keep selected scalar mirrors in `diagnostics`. Add JSONL with one compact `json.dumps(artifact.as_dict(), sort_keys=True) + "\n"` per artifact, not pretty JSON.

---

### `src/mosaic/evaluation/regression.py` (model/utility, transform)

**Analog:** `src/mosaic/evaluation/regression.py`

**Imports pattern** (lines 1-5):
```python
from __future__ import annotations

from dataclasses import dataclass

from mosaic.evaluation.runner import BenchmarkArtifact
```

**Gate validation pattern** (lines 8-15):
```python
@dataclass(frozen=True, slots=True)
class RegressionGate:
    metric_name: str
    minimum: float

    def __post_init__(self) -> None:
        if not self.metric_name.strip():
            raise ValueError("RegressionGate metric_name must not be blank")
```

**Result object pattern** (lines 18-23):
```python
@dataclass(frozen=True, slots=True)
class RegressionResult:
    metric_name: str
    passed: bool
    observed: float | None
    threshold: float
```

**Gate evaluation pattern** (lines 26-39):
```python
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
```

**Apply to Phase 5:** Add `FailureClass(StrEnum)` here. Attach `failure_class` to `RegressionGate` and copy it into `RegressionResult`. Derive primary class from failed results with deterministic priority: lifecycle, trajectory, map_fusion, agent_query, then none. Put the phase-ready helper here unless a planner has a stronger reason not to.

---

### `src/mosaic/evaluation/scenarios.py` (model/factory, batch)

**Analog:** `src/mosaic/evaluation/scenarios.py`

**Package-root import pattern** (lines 5-17):
```python
from mosaic.core import (
    CameraIntrinsics,
    CameraObservation,
    FrameId,
    ImageBuffer,
    ImageEncoding,
    MultiViewObservation,
    Pose3,
    Quaternion,
    Timestamp,
    Translation3,
)
from mosaic.datasets import InMemorySequence
```

**Scenario dataclass validation pattern** (lines 20-28):
```python
@dataclass(frozen=True, slots=True)
class SyntheticScenario:
    name: str
    sequence: InMemorySequence

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("SyntheticScenario name must not be blank")
```

**Deterministic factory pattern** (lines 30-34):
```python
def synthetic_forward_sequence(frame_count: int) -> SyntheticScenario:
    if frame_count <= 0:
        raise ValueError("synthetic_forward_sequence frame_count must be positive")
    observations = tuple(_observation(index) for index in range(frame_count))
    return SyntheticScenario(name=f"synthetic-forward-{frame_count}", sequence=InMemorySequence(observations))
```

**Observation construction pattern for scenario metadata** (lines 37-56):
```python
def _observation(index: int) -> MultiViewObservation:
    timestamp = Timestamp(index * 100_000_000)
    image = ImageBuffer(width=1, height=1, channels=3, encoding=ImageEncoding.RGB8, data=b"\xff\xff\xff")
    return MultiViewObservation(
        timestamp=timestamp,
        views=(
            CameraObservation(
                camera_id="front",
                timestamp=timestamp,
                camera_pose=Pose3(
                    parent_frame=FrameId("world"),
                    child_frame=FrameId("camera/front"),
                    translation=Translation3(x=float(index), y=0.0, z=0.0),
                    rotation=Quaternion.identity(),
                ),
                intrinsics=CameraIntrinsics(width=1, height=1, fx=1.0, fy=1.0, cx=0.5, cy=0.5),
                color=image,
            ),
        ),
    )
```

**Apply to Phase 5:** If adding scenario-summary metadata, derive it from `SyntheticScenario.sequence` and observations: `scenario.name`, frame/update count, `camera_ids`, and expected map frame when available. Do not serialize observations.

---

### `src/mosaic/evaluation/__init__.py` (config/export surface, request-response import)

**Analog:** `src/mosaic/evaluation/__init__.py`

**Explicit import/export pattern** (lines 1-17):
```python
from mosaic.evaluation.metrics import MetricResult, splat_count_metric
from mosaic.evaluation.regression import RegressionGate, RegressionResult, check_regression_gates
from mosaic.evaluation.runner import BenchmarkArtifact, run_slam_benchmark, write_benchmark_artifact
from mosaic.evaluation.scenarios import SyntheticScenario, synthetic_forward_sequence

__all__ = [
    "BenchmarkArtifact",
    "MetricResult",
    "RegressionGate",
    "RegressionResult",
    "SyntheticScenario",
    "check_regression_gates",
    "run_slam_benchmark",
    "splat_count_metric",
    "synthetic_forward_sequence",
    "write_benchmark_artifact",
]
```

**Apply to Phase 5:** Export new stable contracts explicitly: likely `FailureClass`, any metric-family constructors, JSONL writer, gate/failure helper, scenario summary type, and readiness helper. No wildcard imports.

---

### `src/mosaic/__init__.py` (config/export surface, request-response import)

**Analog:** `src/mosaic/__init__.py`

**Evaluation root re-export pattern** (lines 23-34):
```python
from mosaic.evaluation import (
    BenchmarkArtifact,
    MetricResult,
    RegressionGate,
    RegressionResult,
    SyntheticScenario,
    check_regression_gates,
    run_slam_benchmark,
    splat_count_metric,
    synthetic_forward_sequence,
    write_benchmark_artifact,
)
```

**Root `__all__` pattern** (lines 52-104):
```python
__all__ = [
    "AgentQueryKind",
    "BackendCapabilities",
    "BenchmarkArtifact",
    "CameraIntrinsics",
    "CameraMount",
    "CameraObservation",
    "CameraRig",
    "DeterministicSplatBackend",
    "Embodiment",
    "FrameId",
    "FusionInput",
    "FusionResult",
    "FusionStatus",
    "GaussianSplat",
    "ImageBuffer",
    "ImageEncoding",
    "InMemorySequence",
    "LocalRadiusQuery",
    "MetricResult",
    "MultiViewObservation",
    "MultiViewSequence",
    "Pixel",
    "PlatformDescription",
    "PlatformRegistry",
    "PosteriorSummary",
    "ProvenancePreservingFusion",
    "ProvenanceSummary",
    "Pose3",
    "RegressionGate",
    "RegressionResult",
    "Quaternion",
    "SplatMap",
    "SplatFusionStrategy",
    "SplatPosteriorView",
    "SplatQueryResult",
    "SplatSlamBackend",
    "SyntheticScenario",
    "SplatSlamUpdate",
    "Timestamp",
    "TrackingState",
    "Translation3",
    "__version__",
    "check_regression_gates",
    "default_platform_registry",
    "humanoid_stereo_rig",
    "quadruped_front_rig",
    "run_slam_benchmark",
    "splat_count_metric",
    "synthetic_forward_sequence",
    "ugv_surround_rig",
    "write_benchmark_artifact",
]
```

**Apply to Phase 5:** Only root-export stable user-facing additions. Mirror additions in `tests/test_public_api.py`.

---

### `tests/evaluation/test_metrics.py` (test, transform)

**Analog:** `tests/evaluation/test_metrics.py`

**Imports and helper pattern** (lines 1-9):
```python
import pytest

from mosaic.core import FrameId
from mosaic.evaluation import MetricResult, splat_count_metric
from mosaic.splats import GaussianSplat, SplatMap


def _splat(x: float) -> GaussianSplat:
    return GaussianSplat(center=(x, 0.0, 1.0), covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1))
```

**Validation assertion pattern** (lines 12-15):
```python
def test_metric_result_rejects_blank_name() -> None:
    with pytest.raises(ValueError, match="name"):
        MetricResult(name=" ", value=1.0, unit="count")
```

**Exact metric equality pattern** (lines 17-22):
```python
def test_splat_count_metric_counts_snapshot_splats() -> None:
    snapshot = SplatMap(frame=FrameId("map"), splats=(_splat(0.0), _splat(1.0)))

    metric = splat_count_metric(snapshot)

    assert metric == MetricResult(name="splat_count", value=2.0, unit="splats")
```

**JSON-ready dict pattern** (lines 25-28):
```python
def test_metric_result_converts_to_json_ready_dict() -> None:
    metric = MetricResult(name="tracking_rate", value=1.0, unit="ratio")

    assert metric.as_dict() == {"name": "tracking_rate", "value": 1.0, "unit": "ratio"}
```

**Apply to Phase 5:** Add exact assertions for metric families/categories and conservative hook/proxy metrics. Keep helpers private and deterministic.

---

### `tests/evaluation/test_runner.py` (test, batch + file-I/O)

**Analog:** `tests/evaluation/test_runner.py`

**Imports pattern** (lines 1-6):
```python
import json
from typing import Any, cast

from mosaic.core import FrameId
from mosaic.evaluation import BenchmarkArtifact, run_slam_benchmark, synthetic_forward_sequence, write_benchmark_artifact
from mosaic.slam import DeterministicSplatBackend
```

**Benchmark integration assertions** (lines 9-27):
```python
def test_run_slam_benchmark_processes_scenario_and_reports_metrics() -> None:
    artifact = run_slam_benchmark(
        scenario=synthetic_forward_sequence(frame_count=3),
        backend=DeterministicSplatBackend(map_frame=FrameId("map")),
    )

    assert artifact.scenario_name == "synthetic-forward-3"
    assert artifact.backend_name == "deterministic-splat"
    assert artifact.backend_metadata["name"] == "deterministic-splat"
    assert artifact.backend_metadata["supports_multi_view"] is True
    assert artifact.backend_metadata["supports_incremental_mapping"] is True
    assert artifact.backend_metadata["supports_uncertainty"] is False
    assert artifact.backend_metadata["runs_out_of_process"] is False
    assert artifact.backend_metadata["parameter_deterministic"] is True
    json.dumps(artifact.as_dict()["backend_metadata"], sort_keys=True)
    assert artifact.metrics == [{"name": "splat_count", "value": 3.0, "unit": "splats"}]
    assert artifact.diagnostics == {"last_splat_count": 3, "snapshot_splat_count": 3}
    assert artifact.failure_classification == "none"
    assert artifact.update_count == 3
```

**Artifact shape assertion pattern** (lines 30-49):
```python
def test_benchmark_artifact_is_json_ready() -> None:
    artifact = BenchmarkArtifact(
        scenario_name="scenario",
        backend_name="backend",
        update_count=2,
        metrics=[{"name": "splat_count", "value": 2.0, "unit": "splats"}],
        backend_metadata={"name": "backend"},
        diagnostics={"snapshot_splat_count": 2},
        failure_classification="none",
    )

    assert artifact.as_dict() == {
        "scenario_name": "scenario",
        "backend_name": "backend",
        "backend_metadata": {"name": "backend"},
        "update_count": 2,
        "metrics": [{"name": "splat_count", "value": 2.0, "unit": "splats"}],
        "diagnostics": {"snapshot_splat_count": 2},
        "failure_classification": "none",
    }
```

**Copy/no mutation pattern** (lines 52-73):
```python
serialized = artifact.as_dict()
metrics = cast(list[dict[str, str | float]], serialized["metrics"])
backend_metadata = cast(dict[str, Any], serialized["backend_metadata"])
diagnostics = cast(dict[str, Any], serialized["diagnostics"])
metrics[0]["value"] = 999.0
backend_metadata["name"] = "mutated"
diagnostics["snapshot_splat_count"] = 999

assert artifact.as_dict()["metrics"] == [{"name": "splat_count", "value": 1.0, "unit": "splats"}]
assert artifact.as_dict()["backend_metadata"] == {"name": "backend"}
assert artifact.as_dict()["diagnostics"] == {"snapshot_splat_count": 1}
```

**Stable writer assertion pattern** (lines 76-96):
```python
write_benchmark_artifact(artifact, path)

loaded = json.loads(path.read_text())
assert loaded == artifact.as_dict()
assert loaded["backend_metadata"] == {"name": "backend"}
assert loaded["diagnostics"] == {"snapshot_splat_count": 1}
assert loaded["failure_classification"] == "none"
assert path.read_text().startswith("{\n  \"backend_metadata\"")
assert path.read_text().endswith("\n")
```

**Apply to Phase 5:** Add tests for scenario summaries, lifecycle metric family presence, JSONL one-line-per-artifact output, gate/failure result fields, diagnostics mirrors, and no mutation through `as_dict()`.

---

### `tests/evaluation/test_regression.py` (test, transform)

**Analog:** `tests/evaluation/test_regression.py`

**Artifact helper pattern** (lines 1-13):
```python
from mosaic.evaluation import BenchmarkArtifact, RegressionGate, RegressionResult, check_regression_gates


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
```

**Pass/fail exact tuple pattern** (lines 16-25):
```python
def test_regression_gate_passes_when_metric_meets_minimum() -> None:
    results = check_regression_gates(_artifact(3.0), (RegressionGate(metric_name="splat_count", minimum=3.0),))

    assert results == (RegressionResult(metric_name="splat_count", passed=True, observed=3.0, threshold=3.0),)


def test_regression_gate_fails_when_metric_is_too_low() -> None:
    results = check_regression_gates(_artifact(2.0), (RegressionGate(metric_name="splat_count", minimum=3.0),))

    assert results == (RegressionResult(metric_name="splat_count", passed=False, observed=2.0, threshold=3.0),)
```

**Missing metric pattern** (lines 28-41):
```python
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

    results = check_regression_gates(artifact, (RegressionGate(metric_name="splat_count", minimum=1.0),))

    assert results == (RegressionResult(metric_name="splat_count", passed=False, observed=None, threshold=1.0),)
```

**Apply to Phase 5:** Extend tuple equality to include `failure_class`. Add multiple-failure priority tests with lifecycle outranking trajectory/map_fusion/agent_query. Add readiness helper tests for all pass vs failed gate blocks.

---

### `tests/evaluation/test_scenarios.py` (test, batch)

**Analog:** `tests/evaluation/test_scenarios.py`

**Determinism pattern** (lines 6-15):
```python
def test_synthetic_forward_sequence_is_deterministic() -> None:
    first = synthetic_forward_sequence(frame_count=3)
    second = synthetic_forward_sequence(frame_count=3)

    assert first == second
    assert first.name == "synthetic-forward-3"
    assert second.name == "synthetic-forward-3"
    assert len(first.sequence) == 3
    assert len(second.sequence) == 3
    assert [observation.timestamp.nanoseconds for observation in first.sequence] == [0, 100_000_000, 200_000_000]
```

**Camera metadata pattern** (lines 18-23):
```python
def test_synthetic_forward_sequence_produces_front_camera_observations() -> None:
    scenario = synthetic_forward_sequence(frame_count=2)

    assert isinstance(scenario, SyntheticScenario)
    assert scenario.sequence.observations[0].camera_ids == ("front",)
    assert scenario.sequence.observations[1].views[0].camera_pose.translation.x == 1.0
```

**Validation pattern** (lines 26-28):
```python
def test_synthetic_forward_sequence_requires_positive_frame_count() -> None:
    with pytest.raises(ValueError, match="positive"):
        synthetic_forward_sequence(frame_count=0)
```

**Apply to Phase 5:** If scenario summary helpers are added, assert deterministic metadata exactly: scenario name, frame count, camera IDs, and expected frame where available.

---

### `tests/test_public_api.py` (test, request-response import)

**Analog:** `tests/test_public_api.py`

**Evaluation public API pattern** (lines 49-54):
```python
def test_public_api_exports_evaluation_types() -> None:
    scenario = synthetic_forward_sequence(frame_count=1)

    assert scenario.name == "synthetic-forward-1"
    assert BenchmarkArtifact.__name__ == "BenchmarkArtifact"
    assert RegressionGate(metric_name="splat_count", minimum=1.0).minimum == 1.0
```

**Apply to Phase 5:** Add smoke assertions for stable new exports such as `FailureClass`, JSONL writer, readiness helper, or public metric constructors. Do not assert private helpers.

---

### `README.md` (documentation, request-response import examples)

**Analog:** `README.md`

**Boundary list pattern** (lines 155-172):
```markdown
## Backend and Dependency Boundary

Mosaic Phase 1 is a pure-Python headless library. Core imports are expected to work with `dependencies = []` and without GPU, native computer-vision stacks, robot middleware, browser services, or provider SDKs.

`DeterministicSplatBackend` is a deterministic reference backend for contract tests, examples, replay validation, and benchmark smoke checks. It is not a real 3D Gaussian Splatting optimizer.

`ProvenancePreservingFusion` is a provenance-preserving contract strategy. It validates compatible map inputs, preserves and diagnoses splats, reports the stable machine-readable label `preserved_not_optimized`, does not optimize Gaussians, and does not collapse overlapping splats into occupancy-grid cells. It is not real Gaussian optimization, calibrated uncertainty minimization, loop closure, map alignment, or multi-session reconstruction.

The following are deferred, not required for Phase 1, and out of scope for the core setup path:

- real 3DGS/CUDA backend integrations
- ROS wrappers, robot execution, and vendor robot SDKs
- Habitat or simulator benchmark runners
- browser UI or WebSockets demos
- LLM provider integrations and agent runtime orchestration
- native image-processing or tensor stacks as required runtime dependencies

Downstream packages can wrap Mosaic for those environments later. The Mosaic core owns typed representation contracts and deterministic seams first.
```

**Hardening gap wording pattern** (lines 174-183):
```markdown
## Known Hardening Gaps

Phase 1 intentionally leaves several hardening tracks for later phases:

- coordinate-frame semantics still need explicit pose direction, parent/child frame meaning, handedness, optical-frame convention, and timestamp precision tests
- Gaussian covariance layout and artifact schemas need versioned serialization and round-trip coverage
- backend registry metadata, availability checks, optional dependency reporting, and parametrized contract tests are not complete
- fusion diagnostics need richer uncertainty, conflict, and anti-occupancy-grid semantics beyond the initial reference strategy
- evaluation needs broader metric families, failure classification, JSON/JSONL schema hardening, and gates before real backend integration
- agent posterior APIs need richer uncertainty summaries and repeated-query determinism coverage before representation memory layers are added
```

**Apply to Phase 5:** Replace/update Phase 1 language as appropriate. Add explicit boundary language: real 3DGS backend integration remains blocked until deterministic benchmark suite gates pass. Keep wording conservative; do not imply placeholder real backends exist.

## Shared Patterns

### Frozen dataclasses with validation
**Sources:** `src/mosaic/evaluation/metrics.py`, `src/mosaic/evaluation/regression.py`, `src/mosaic/evaluation/scenarios.py`, `src/mosaic/fusion/protocol.py`
**Apply to:** New/modified public contracts in metrics, runner, regression, and scenario summaries.
```python
@dataclass(frozen=True, slots=True)
class RegressionGate:
    metric_name: str
    minimum: float

    def __post_init__(self) -> None:
        if not self.metric_name.strip():
            raise ValueError("RegressionGate metric_name must not be blank")
```

### Immutable mapping copy before proxy
**Source:** `src/mosaic/evaluation/runner.py` lines 46-49 and `src/mosaic/slam/protocol.py` lines 30-31
**Apply to:** Artifact metadata, diagnostics, gate result details, scenario summaries, fusion/agent metric maps.
```python
object.__setattr__(self, "backend_metadata", MappingProxyType(dict(self.backend_metadata)))
object.__setattr__(self, "diagnostics", MappingProxyType(dict(self.diagnostics)))
```

### JSON-ready artifact serialization
**Source:** `src/mosaic/evaluation/runner.py` lines 53-62 and 88-89
**Apply to:** `BenchmarkArtifact.as_dict()`, single JSON writer, JSONL writer.
```python
def write_benchmark_artifact(artifact: BenchmarkArtifact, path: Path) -> None:
    path.write_text(json.dumps(artifact.as_dict(), indent=2, sort_keys=True) + "\n")
```

### Backend lifecycle state source for lifecycle metrics
**Source:** `src/mosaic/slam/protocol.py` lines 16-45 and `src/mosaic/slam/fake_backend.py` lines 33-50
**Apply to:** lifecycle metric family and lifecycle failure gates.
```python
class TrackingState(StrEnum):
    NOT_INITIALIZED = "not_initialized"
    TRACKING = "tracking"
    LOST = "lost"

@dataclass(frozen=True, slots=True)
class SplatSlamUpdate:
    timestamp: Timestamp
    tracking_state: TrackingState
    estimated_pose: Pose3 | None
    map_update: SplatMap
    diagnostics: Mapping[str, MetricValue] = field(default_factory=dict)
```

### Agent-query deterministic probe source
**Source:** `src/mosaic/agents/posteriors.py` lines 14-40 and `src/mosaic/agents/queries.py` lines 15-25
**Apply to:** agent-query stability metrics and tests.
```python
@dataclass(frozen=True, slots=True)
class SplatPosteriorView:
    splat_map: SplatMap

    def query_local(self, query: LocalRadiusQuery) -> SplatQueryResult:
        splat_ids = tuple(
            index
            for index, splat in enumerate(self.splat_map.splats)
            if dist(query.center, splat.center) <= query.radius
        )
        return SplatQueryResult(query_kind=AgentQueryKind.LOCAL_GEOMETRY, splat_ids=splat_ids)
```

### Fusion proxy metric source
**Source:** `src/mosaic/fusion/strategies.py` lines 37-50 and `src/mosaic/fusion/protocol.py` lines 37-60, 63-82, 84-104
**Apply to:** conservative map/fusion metrics only; do not claim real reconstruction quality.
```python
return FusionResult(
    status=FusionStatus.FUSED,
    fused_map=fused_map,
    provenance=provenance,
    uncertainty=uncertainty,
    conflicts=conflicts,
    diagnostics={
        "source_map_count": provenance.source_map_count,
        "source_splat_count": provenance.source_splat_count,
        "fused_splat_count": provenance.fused_splat_count,
        "fusion_uncertainty_model": uncertainty.model_label,
        "fusion_conflict_candidate_count": conflicts.total_candidate_count,
    },
)
```

### Public export discipline
**Sources:** `src/mosaic/evaluation/__init__.py`, `src/mosaic/__init__.py`
**Apply to:** every new stable public contract.
```python
from mosaic.evaluation.metrics import MetricResult, splat_count_metric
from mosaic.evaluation.regression import RegressionGate, RegressionResult, check_regression_gates

__all__ = [
    "MetricResult",
    "RegressionGate",
    "RegressionResult",
    "check_regression_gates",
]
```

### Test style
**Sources:** `tests/evaluation/test_metrics.py`, `tests/evaluation/test_runner.py`, `tests/evaluation/test_regression.py`
**Apply to:** all Phase 5 tests.
```python
with pytest.raises(ValueError, match="name"):
    MetricResult(name=" ", value=1.0, unit="count")

assert results == (RegressionResult(metric_name="splat_count", passed=True, observed=3.0, threshold=3.0),)
```

## No Analog Found

All Phase 5 files have close existing analogs in the codebase. No planner fallback to research-only patterns is required.

| File | Role | Data Flow | Reason |
|------|------|-----------|--------|
| None | N/A | N/A | Existing evaluation, runner, regression, scenario, export, README, and test files already provide direct patterns. |

## Metadata

**Analog search scope:** `src/mosaic/evaluation/`, `src/mosaic/slam/`, `src/mosaic/fusion/`, `src/mosaic/agents/`, `tests/evaluation/`, `tests/test_public_api.py`, `README.md`
**Files scanned:** 20 phase-relevant files discovered; 18 files read for concrete excerpts
**Pattern extraction date:** 2026-05-19
