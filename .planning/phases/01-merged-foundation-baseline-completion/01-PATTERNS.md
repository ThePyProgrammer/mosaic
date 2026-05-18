# Phase 1: Merged Foundation Baseline Completion - Pattern Map

**Mapped:** 2026-05-18
**Files analyzed:** 15 new/modified planning targets
**Analogs found:** 15 / 15

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `README.md` | documentation | request-response | `01-RESEARCH.md` code examples + current public API/tests | role-match |
| `pyproject.toml` | config | request-response | `pyproject.toml` | exact |
| `src/mosaic/__init__.py` | public API/barrel | transform | `src/mosaic/__init__.py` | exact |
| `src/mosaic/fusion/protocol.py` | model/protocol | transform | `src/mosaic/fusion/protocol.py` | exact |
| `src/mosaic/fusion/strategies.py` | service/strategy | transform | `src/mosaic/fusion/strategies.py` | exact |
| `src/mosaic/evaluation/runner.py` | service/utility | batch + file-I/O | `src/mosaic/evaluation/runner.py` | exact |
| `src/mosaic/evaluation/regression.py` | utility | batch | `src/mosaic/evaluation/regression.py` | exact |
| `src/mosaic/evaluation/scenarios.py` | utility/factory | transform | `src/mosaic/evaluation/scenarios.py` | exact |
| `src/mosaic/agents/queries.py` | model | transform | `src/mosaic/agents/queries.py` | exact |
| `src/mosaic/agents/posteriors.py` | service/view | request-response | `src/mosaic/agents/posteriors.py` | exact |
| `tests/test_public_api.py` | test | request-response | `tests/test_public_api.py` | exact |
| `tests/test_readme_contract.py` | test | request-response | `tests/test_public_api.py` + `tests/test_package_import.py` | role-match |
| `tests/fusion/test_fusion_protocol.py` | test | transform | `tests/fusion/test_fusion_protocol.py` | exact |
| `tests/evaluation/test_runner.py` | test | batch + file-I/O | `tests/evaluation/test_runner.py` | exact |
| `tests/agents/test_splat_posterior.py` | test | request-response | `tests/agents/test_splat_posterior.py` | exact |

## Pattern Assignments

### `README.md` (documentation, request-response)

**Analog:** current root public API, README examples from `01-RESEARCH.md`, and public API smoke tests.

**Scope/commands pattern** from `01-RESEARCH.md` (lines 105-110):
```bash
uv sync
uv run pytest -q
```

**Public import example pattern** from `01-RESEARCH.md` (lines 293-304):
```python
from mosaic import (
    DeterministicSplatBackend,
    FrameId,
    ProvenancePreservingFusion,
    SplatMap,
    SplatPosteriorView,
    synthetic_forward_sequence,
)
```

**Benchmark example pattern** from `01-RESEARCH.md` (lines 310-328):
```python
from pathlib import Path

from mosaic import (
    DeterministicSplatBackend,
    FrameId,
    RegressionGate,
    check_regression_gates,
    run_slam_benchmark,
    synthetic_forward_sequence,
    write_benchmark_artifact,
)

scenario = synthetic_forward_sequence(frame_count=3)
backend = DeterministicSplatBackend(map_frame=FrameId("map"))
artifact = run_slam_benchmark(scenario, backend)
write_benchmark_artifact(artifact, Path("benchmark.json"))
results = check_regression_gates(artifact, (RegressionGate(metric_name="splat_count", minimum=3.0),))
```

**Boundary wording to preserve:** README must say Phase 1 is pure-Python, provider-free, no CUDA/native/robot/LLM runtime dependency, and `DeterministicSplatBackend` / `ProvenancePreservingFusion` are deterministic reference/test seams, not real Gaussian optimization.

---

### `pyproject.toml` (config, request-response)

**Analog:** `pyproject.toml`

**Dependency boundary pattern** (lines 1-15):
```toml
[project]
name = "mosaic"
version = "0.1.0"
description = "Typed Gaussian-splatting SLAM primitives for multi-view robotic perception"
readme = "README.md"
authors = [
    { name = "Prannaya Gupta", email = "prannayagupta@gmail.com" }
]
requires-python = ">=3.12"
dependencies = []

[dependency-groups]
dev = [
    "pytest>=8.4.0",
]
```

**Pytest config pattern** (lines 17-19):
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

**Build backend pattern** (lines 21-23):
```toml
[build-system]
requires = ["uv_build>=0.10.10,<0.11.0"]
build-backend = "uv_build"
```

**Apply:** Do not add runtime dependencies in Phase 1. If a README/docs validation test is added, it belongs under dev tooling only if truly necessary; prefer existing pytest setup.

---

### `src/mosaic/__init__.py` (public API/barrel, transform)

**Analog:** `src/mosaic/__init__.py`

**Imports pattern** (lines 1-48):
```python
from mosaic.agents import (
    AgentQueryKind,
    LocalRadiusQuery,
    PosteriorSummary,
    ProvenanceSummary,
    SplatPosteriorView,
    SplatQueryResult,
)
from mosaic.core import (
    CameraIntrinsics,
    CameraObservation,
    FrameId,
    ImageBuffer,
    ImageEncoding,
    MultiViewObservation,
    Pixel,
    Pose3,
    Quaternion,
    Timestamp,
    Translation3,
)
from mosaic.datasets import InMemorySequence, MultiViewSequence
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
from mosaic.fusion import FusionInput, FusionResult, FusionStatus, ProvenancePreservingFusion, SplatFusionStrategy
from mosaic.platforms import (
    CameraMount,
    CameraRig,
    Embodiment,
    PlatformDescription,
    PlatformRegistry,
    default_platform_registry,
    humanoid_stereo_rig,
    quadruped_front_rig,
    ugv_surround_rig,
)
from mosaic.slam import BackendCapabilities, DeterministicSplatBackend, SplatSlamBackend, SplatSlamUpdate, TrackingState
from mosaic.splats import GaussianSplat, SplatMap
```

**Version/export pattern** (lines 50-104):
```python
__version__ = "0.1.0"

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

**Apply:** Public-surface changes must explicitly import symbols and list every export in `__all__`. No wildcard exports.

---

### `src/mosaic/fusion/protocol.py` (model/protocol, transform)

**Analog:** `src/mosaic/fusion/protocol.py`

**Imports pattern** (lines 1-9):
```python
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Mapping, Protocol, runtime_checkable

from mosaic.core import FrameId
from mosaic.splats import SplatMap
```

**Validation/freezing pattern** (lines 19-33):
```python
@dataclass(frozen=True, slots=True)
class FusionInput:
    maps: tuple[SplatMap, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "maps", tuple(self.maps))
        if not self.maps:
            raise ValueError("FusionInput requires at least one map")
        frames = {splat_map.frame for splat_map in self.maps}
        if len(frames) != 1:
            raise ValueError("FusionInput maps must share the same frame")

    @property
    def frame(self) -> FrameId:
        return self.maps[0].frame
```

**Diagnostics immutability pattern** (lines 36-43):
```python
@dataclass(frozen=True, slots=True)
class FusionResult:
    status: FusionStatus
    fused_map: SplatMap
    diagnostics: Mapping[str, FusionMetricValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "diagnostics", MappingProxyType(dict(self.diagnostics)))
```

**Protocol boundary pattern** (lines 46-53):
```python
@runtime_checkable
class SplatFusionStrategy(Protocol):
    @property
    def name(self) -> str:
        raise NotImplementedError

    def fuse(self, fusion_input: FusionInput) -> FusionResult:
        raise NotImplementedError
```

---

### `src/mosaic/fusion/strategies.py` (service/strategy, transform)

**Analog:** `src/mosaic/fusion/strategies.py`

**Imports pattern** (lines 1-7):
```python
from __future__ import annotations

from dataclasses import dataclass

from mosaic.fusion.protocol import FusionInput, FusionResult, FusionStatus
from mosaic.splats import GaussianSplat, SplatMap
```

**Core reference strategy pattern** (lines 9-29):
```python
@dataclass(frozen=True, slots=True)
class ProvenancePreservingFusion:
    @property
    def name(self) -> str:
        return "provenance-preserving"

    def fuse(self, fusion_input: FusionInput) -> FusionResult:
        fused_splats: list[GaussianSplat] = []
        for splat_map in fusion_input.maps:
            fused_splats.extend(splat_map.splats)
        fused_map = SplatMap(frame=fusion_input.frame, splats=tuple(fused_splats))
        return FusionResult(
            status=FusionStatus.FUSED,
            fused_map=fused_map,
            diagnostics={
                "source_map_count": len(fusion_input.maps),
                "source_splat_count": len(fused_splats),
                "fused_splat_count": len(fused_map),
                "uncertainty_model": "preserved-not-optimized",
            },
        )
```

**Apply:** This deterministic strategy concatenates immutable snapshots and reports diagnostics. Do not claim optimization, conflict resolution, or real posterior fusion quality in README/tests.

---

### `src/mosaic/evaluation/runner.py` (service/utility, batch + file-I/O)

**Analog:** `src/mosaic/evaluation/runner.py`

**Imports pattern** (lines 1-12):
```python
from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Sequence

from mosaic.evaluation.metrics import MetricResult, splat_count_metric
from mosaic.evaluation.scenarios import SyntheticScenario
from mosaic.slam import SplatSlamBackend
```

**Frozen sequence pattern** (lines 17-31):
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

**Artifact serialization pattern** (lines 34-50):
```python
@dataclass(frozen=True, slots=True)
class BenchmarkArtifact:
    scenario_name: str
    backend_name: str
    update_count: int
    metrics: Sequence[MetricDict]

    def __post_init__(self) -> None:
        object.__setattr__(self, "metrics", FrozenMetricSequence(self.metrics))

    def as_dict(self) -> dict[str, str | int | list[MetricDict]]:
        return {
            "scenario_name": self.scenario_name,
            "backend_name": self.backend_name,
            "update_count": self.update_count,
            "metrics": [dict(metric) for metric in self.metrics],
        }
```

**Benchmark batch pattern** (lines 53-65):
```python
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
```

**File I/O pattern** (lines 68-73):
```python
def write_benchmark_artifact(artifact: BenchmarkArtifact, path: Path) -> None:
    path.write_text(json.dumps(artifact.as_dict(), indent=2, sort_keys=True) + "\n")


def _snapshot_metrics(backend: SplatSlamBackend) -> tuple[MetricResult, ...]:
    return (splat_count_metric(backend.snapshot()),)
```

---

### `src/mosaic/evaluation/regression.py` (utility, batch)

**Analog:** `src/mosaic/evaluation/regression.py`

**Validation pattern** (lines 8-16):
```python
@dataclass(frozen=True, slots=True)
class RegressionGate:
    metric_name: str
    minimum: float

    def __post_init__(self) -> None:
        if not self.metric_name.strip():
            raise ValueError("RegressionGate metric_name must not be blank")
```

**Gate evaluation pattern** (lines 18-39):
```python
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
```

---

### `src/mosaic/evaluation/scenarios.py` (utility/factory, transform)

**Analog:** `src/mosaic/evaluation/scenarios.py`

**Imports pattern** (lines 1-18):
```python
from __future__ import annotations

from dataclasses import dataclass

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

**Factory validation pattern** (lines 20-34):
```python
@dataclass(frozen=True, slots=True)
class SyntheticScenario:
    name: str
    sequence: InMemorySequence

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("SyntheticScenario name must not be blank")


def synthetic_forward_sequence(frame_count: int) -> SyntheticScenario:
    if frame_count <= 0:
        raise ValueError("synthetic_forward_sequence frame_count must be positive")
    observations = tuple(_observation(index) for index in range(frame_count))
    return SyntheticScenario(name=f"synthetic-forward-{frame_count}", sequence=InMemorySequence(observations))
```

**Private helper pattern** (lines 37-56):
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

---

### `src/mosaic/agents/queries.py` (model, transform)

**Analog:** `src/mosaic/agents/queries.py`

**Imports and enum pattern** (lines 1-12):
```python
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Mapping


class AgentQueryKind(StrEnum):
    LOCAL_GEOMETRY = "local_geometry"
    SCENE_SUMMARY = "scene_summary"
    PROVENANCE = "provenance"
```

**Query validation pattern** (lines 15-25):
```python
@dataclass(frozen=True, slots=True)
class LocalRadiusQuery:
    center: tuple[float, float, float]
    radius: float
    kind: AgentQueryKind = AgentQueryKind.LOCAL_GEOMETRY

    def __post_init__(self) -> None:
        if len(self.center) != 3:
            raise ValueError("LocalRadiusQuery center must contain three coordinates")
        if self.radius <= 0.0:
            raise ValueError("LocalRadiusQuery radius must be positive")
```

**Summary validation/freezing pattern** (lines 38-63):
```python
@dataclass(frozen=True, slots=True)
class PosteriorSummary:
    splat_count: int
    provenance_count: int
    mean_opacity: float

    def __post_init__(self) -> None:
        if self.splat_count < 0:
            raise ValueError("PosteriorSummary splat_count must be non-negative")
        if self.provenance_count < 0:
            raise ValueError("PosteriorSummary provenance_count must be non-negative")
        if self.mean_opacity < 0.0 or self.mean_opacity > 1.0:
            raise ValueError("PosteriorSummary mean_opacity must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class ProvenanceSummary:
    counts: Mapping[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for source, count in self.counts.items():
            if not source.strip():
                raise ValueError("ProvenanceSummary source names must not be blank")
            if count < 0:
                raise ValueError("ProvenanceSummary counts must be non-negative")
        object.__setattr__(self, "counts", MappingProxyType(dict(self.counts)))
```

---

### `src/mosaic/agents/posteriors.py` (service/view, request-response)

**Analog:** `src/mosaic/agents/posteriors.py`

**Imports pattern** (lines 1-7):
```python
from __future__ import annotations

from dataclasses import dataclass
from math import dist

from mosaic.agents.queries import AgentQueryKind, LocalRadiusQuery, PosteriorSummary, ProvenanceSummary, SplatQueryResult
from mosaic.splats import SplatMap
```

**Bounded local query pattern** (lines 10-20):
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

**Summary/provenance pattern** (lines 22-40):
```python
    def summary(self) -> PosteriorSummary:
        splat_count = len(self.splat_map)
        provenances = {splat.provenance for splat in self.splat_map.splats if splat.provenance is not None}
        mean_opacity = 0.0
        if splat_count:
            mean_opacity = round(sum(splat.opacity for splat in self.splat_map.splats) / splat_count, 6)
        return PosteriorSummary(
            splat_count=splat_count,
            provenance_count=len(provenances),
            mean_opacity=mean_opacity,
        )

    def provenance(self) -> ProvenanceSummary:
        counts: dict[str, int] = {}
        for splat in self.splat_map.splats:
            if splat.provenance is None:
                continue
            counts[splat.provenance] = counts.get(splat.provenance, 0) + 1
        return ProvenanceSummary(counts=counts)
```

---

### `tests/test_public_api.py` (test, request-response)

**Analog:** `tests/test_public_api.py`

**Root import smoke pattern** (lines 1-22):
```python
from mosaic import (
    AgentQueryKind,
    BenchmarkArtifact,
    CameraIntrinsics,
    CameraRig,
    DeterministicSplatBackend,
    Embodiment,
    FrameId,
    FusionInput,
    GaussianSplat,
    InMemorySequence,
    LocalRadiusQuery,
    PlatformRegistry,
    ProvenancePreservingFusion,
    RegressionGate,
    SplatMap,
    SplatPosteriorView,
    Timestamp,
    TrackingState,
    quadruped_front_rig,
    synthetic_forward_sequence,
)
```

**Public API assertions pattern** (lines 25-63):
```python
def test_public_api_exports_core_foundation_types() -> None:
    assert Timestamp.from_seconds(0.5).nanoseconds == 500_000_000
    assert FrameId("map").value == "map"
    assert CameraIntrinsics(width=1, height=1, fx=1.0, fy=1.0, cx=0.5, cy=0.5).width == 1
    assert GaussianSplat(center=(0.0, 0.0, 1.0), covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1)).opacity == 1.0
    assert len(SplatMap(frame=FrameId("map"))) == 0
    assert DeterministicSplatBackend().name == "deterministic-splat"
    assert TrackingState.TRACKING.value == "tracking"
    assert InMemorySequence.__name__ == "InMemorySequence"
```

**Apply:** If README examples introduce public imports, mirror the import smoke coverage here or keep examples limited to already tested exports.

---

### `tests/fusion/test_fusion_protocol.py` (test, transform)

**Analog:** `tests/fusion/test_fusion_protocol.py`

**Helper factory pattern** (lines 8-18):
```python
def _map(frame: str = "map") -> SplatMap:
    return SplatMap(
        frame=FrameId(frame),
        splats=(
            GaussianSplat(
                center=(0.0, 0.0, 1.0),
                covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1),
                provenance="camera/front",
            ),
        ),
    )
```

**Validation tests pattern** (lines 21-38):
```python
def test_fusion_input_requires_at_least_one_map() -> None:
    with pytest.raises(ValueError, match="at least one"):
        FusionInput(maps=())


def test_fusion_input_requires_matching_frames() -> None:
    with pytest.raises(ValueError, match="same frame"):
        FusionInput(maps=(_map("map"), _map("other")))


def test_fusion_input_defensively_freezes_maps() -> None:
    maps = [_map("map")]
    fusion_input = FusionInput(maps=maps)
    maps.append(_map("map"))

    assert isinstance(fusion_input.maps, tuple)
    assert len(fusion_input.maps) == 1
    assert fusion_input.frame == FrameId("map")
```

**MappingProxyType assertion pattern** (lines 41-50):
```python
def test_fusion_result_freezes_diagnostics_mapping() -> None:
    result = FusionResult(
        status=FusionStatus.FUSED,
        fused_map=_map(),
        diagnostics={"source_map_count": 1},
    )

    assert result.diagnostics["source_map_count"] == 1
    with pytest.raises(TypeError):
        result.diagnostics["source_map_count"] = 2
```

---

### `tests/evaluation/test_runner.py` (test, batch + file-I/O)

**Analog:** `tests/evaluation/test_runner.py`

**Benchmark behavior pattern** (lines 9-18):
```python
def test_run_slam_benchmark_processes_scenario_and_reports_metrics() -> None:
    artifact = run_slam_benchmark(
        scenario=synthetic_forward_sequence(frame_count=3),
        backend=DeterministicSplatBackend(map_frame=FrameId("map")),
    )

    assert artifact.scenario_name == "synthetic-forward-3"
    assert artifact.backend_name == "deterministic-splat"
    assert artifact.metrics == [{"name": "splat_count", "value": 3.0, "unit": "splats"}]
    assert artifact.update_count == 3
```

**Serialization defensive-copy pattern** (lines 21-49):
```python
def test_benchmark_artifact_as_dict_does_not_expose_internal_metrics() -> None:
    artifact = BenchmarkArtifact(
        scenario_name="scenario",
        backend_name="backend",
        update_count=1,
        metrics=[{"name": "splat_count", "value": 1.0, "unit": "splats"}],
    )

    serialized = artifact.as_dict()
    metrics = cast(list[dict[str, str | float]], serialized["metrics"])
    metrics[0]["value"] = 999.0

    assert artifact.as_dict()["metrics"] == [{"name": "splat_count", "value": 1.0, "unit": "splats"}]
```

**File I/O test pattern** (lines 52-64):
```python
def test_write_benchmark_artifact_writes_stable_json(tmp_path) -> None:
    artifact = BenchmarkArtifact(
        scenario_name="scenario",
        backend_name="backend",
        update_count=1,
        metrics=[{"name": "splat_count", "value": 1.0, "unit": "splats"}],
    )
    path = tmp_path / "artifact.json"

    write_benchmark_artifact(artifact, path)

    assert json.loads(path.read_text()) == artifact.as_dict()
    assert path.read_text().endswith("\n")
```

---

### `tests/agents/test_splat_posterior.py` (test, request-response)

**Analog:** `tests/agents/test_splat_posterior.py`

**Fixture helper pattern** (lines 6-29):
```python
def _map() -> SplatMap:
    return SplatMap(
        frame=FrameId("map"),
        splats=(
            GaussianSplat(
                center=(0.0, 0.0, 0.0),
                covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1),
                opacity=0.5,
                provenance="front",
            ),
            GaussianSplat(
                center=(1.0, 0.0, 0.0),
                covariance_upper=(0.2, 0.0, 0.0, 0.2, 0.0, 0.2),
                opacity=1.0,
                provenance="front",
            ),
            GaussianSplat(
                center=(5.0, 0.0, 0.0),
                covariance_upper=(0.3, 0.0, 0.0, 0.3, 0.0, 0.3),
                opacity=0.25,
                provenance="rear",
            ),
        ),
    )
```

**Bounded query/summary assertions pattern** (lines 32-52):
```python
def test_local_radius_query_returns_splat_indices_inside_radius() -> None:
    view = SplatPosteriorView(_map())

    result = view.query_local(LocalRadiusQuery(center=(0.0, 0.0, 0.0), radius=1.1))

    assert result.splat_ids == (0, 1)
    assert result.count == 2


def test_summary_reports_count_provenance_and_mean_opacity() -> None:
    summary = SplatPosteriorView(_map()).summary()

    assert summary.splat_count == 3
    assert summary.provenance_count == 2
    assert summary.mean_opacity == 0.583333


def test_provenance_summary_counts_known_sources() -> None:
    provenance = SplatPosteriorView(_map()).provenance()

    assert provenance.counts == {"front": 2, "rear": 1}
```

## Shared Patterns

### Explicit public exports
**Source:** `src/mosaic/__init__.py` lines 1-104
**Apply to:** root package exports, README examples, public API tests

Use package-root imports and explicit `__all__`; do not document private/deep imports as the primary user path.

---

### `tests/test_readme_contract.py` (test, request-response)

**Analog:** `tests/test_public_api.py` and `tests/test_package_import.py`

**Apply:** README contract tests should follow the same direct pytest assertion style as the public API smoke tests: import no project-only helper framework, read repository files through `pathlib.Path`, and assert exact user-facing contract strings. Keep the test focused on BASE-03/BASE-04: required README headings, `uv sync`, `uv run pytest -q`, all eight module names, deferred-boundary wording for heavy integrations, and `dependencies = []` in `pyproject.toml`.

**Boundary assertion pattern:** If terms such as `cuda`, `torch`, `opencv`, `ros`, `habitat`, `openai`, `anthropic`, or `websocket` appear in README, tests should only allow them in sentences that make the integration deferred, not required, or out of scope. Do not add doctest or another documentation-test dependency.

### Frozen dataclasses and validation
**Source:** `src/mosaic/core/frames.py` lines 7-34 and `src/mosaic/splats/primitives.py` lines 6-42
**Apply to:** all public value objects and query/result objects
```python
@dataclass(frozen=True, order=True, slots=True)
class FrameId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("FrameId value must not be blank")
```

### Defensive immutable containers
**Source:** `src/mosaic/fusion/protocol.py` lines 23-29, 42-43; `src/mosaic/evaluation/runner.py` lines 17-31
**Apply to:** diagnostics, metrics, maps, result snapshots
```python
object.__setattr__(self, "maps", tuple(self.maps))
object.__setattr__(self, "diagnostics", MappingProxyType(dict(self.diagnostics)))
```

### Protocol boundary + deterministic reference implementation
**Source:** `src/mosaic/fusion/protocol.py` lines 46-53; `src/mosaic/slam/fake_backend.py` lines 11-53
**Apply to:** README wording, tests, baseline validation
```python
@runtime_checkable
class SplatFusionStrategy(Protocol):
    @property
    def name(self) -> str:
        raise NotImplementedError

    def fuse(self, fusion_input: FusionInput) -> FusionResult:
        raise NotImplementedError
```

### Stable JSON artifacts
**Source:** `src/mosaic/evaluation/runner.py` lines 44-69
**Apply to:** evaluation examples and artifact tests
```python
def write_benchmark_artifact(artifact: BenchmarkArtifact, path: Path) -> None:
    path.write_text(json.dumps(artifact.as_dict(), indent=2, sort_keys=True) + "\n")
```

### Test style
**Source:** `tests/fusion/test_fusion_protocol.py`, `tests/evaluation/test_runner.py`, `tests/agents/test_splat_posterior.py`
**Apply to:** any Phase 1 tests

Use small private helper factories, direct assertions, `pytest.raises(..., match="...")` for validation, and `tmp_path` for file output checks.

## No Analog Found

None. The current merged baseline already contains direct analogs for all likely Phase 1 planning targets.

## Metadata

**Analog search scope:** `src/mosaic/`, `tests/`, `pyproject.toml`, `README.md`, phase research document
**Files scanned:** 37 source/test/config/documentation candidates
**Pattern extraction date:** 2026-05-18
