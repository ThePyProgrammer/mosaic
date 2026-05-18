# Evaluation Regression Harness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add deterministic evaluation scenarios, metrics, machine-readable benchmark artifacts, and regression gates for Mosaic's Splat SLAM core.

**Architecture:** Evaluation runs entirely against existing pure-Python contracts and the deterministic backend, producing stable artifacts that future real backends can match. Metrics are simple typed objects over backend updates and splat-map snapshots, not a general benchmarking framework.

**Tech Stack:** Python 3.12, `dataclasses`, `json`, `pathlib`, `pytest`, `uv`.

---

## Prerequisite

Complete these plans first:

1. `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`
2. `docs/superpowers/plans/2026-05-18-platform-camera-rig-layer.md`
3. `docs/superpowers/plans/2026-05-18-posterior-aware-splat-fusion.md`

This plan assumes `mosaic.datasets.InMemorySequence`, `mosaic.slam.DeterministicSplatBackend`, and `mosaic.splats.SplatMap` exist.

## File Structure

Create or modify these files:

```text
src/mosaic/evaluation/__init__.py          # Public evaluation exports
src/mosaic/evaluation/metrics.py           # Metric result and deterministic metric functions
src/mosaic/evaluation/scenarios.py         # Synthetic multi-view scenario factories
src/mosaic/evaluation/runner.py            # Benchmark runner and artifact writer
src/mosaic/evaluation/regression.py        # Regression gate contracts and checks
src/mosaic/__init__.py                     # Root-level exports for stable evaluation API
tests/evaluation/test_metrics.py           # Metric tests
tests/evaluation/test_scenarios.py         # Scenario determinism tests
tests/evaluation/test_runner.py            # Benchmark artifact tests
tests/evaluation/test_regression.py        # Regression gate tests
tests/test_public_api.py                   # Add root evaluation export expectations
```

Run all commands from:

```bash
cd /home/prannayag/pragnition/robotics/mosaic
```

---

### Task 1: Add Deterministic Metric Contracts

**Files:**
- Create: `src/mosaic/evaluation/__init__.py`
- Create: `src/mosaic/evaluation/metrics.py`
- Create: `tests/evaluation/test_metrics.py`

- [ ] **Step 1: Write failing metric tests**

Create `tests/evaluation/test_metrics.py`:

```python
import pytest

from mosaic.core import FrameId
from mosaic.evaluation import MetricResult, splat_count_metric
from mosaic.splats import GaussianSplat, SplatMap


def _splat(x: float) -> GaussianSplat:
    return GaussianSplat(center=(x, 0.0, 1.0), covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1))


def test_metric_result_rejects_blank_name() -> None:
    with pytest.raises(ValueError, match="name"):
        MetricResult(name=" ", value=1.0, unit="count")


def test_splat_count_metric_counts_snapshot_splats() -> None:
    snapshot = SplatMap(frame=FrameId("map"), splats=(_splat(0.0), _splat(1.0)))

    metric = splat_count_metric(snapshot)

    assert metric == MetricResult(name="splat_count", value=2.0, unit="splats")


def test_metric_result_converts_to_json_ready_dict() -> None:
    metric = MetricResult(name="tracking_rate", value=1.0, unit="ratio")

    assert metric.as_dict() == {"name": "tracking_rate", "value": 1.0, "unit": "ratio"}
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
uv run pytest tests/evaluation/test_metrics.py -q
```

Expected: FAIL with `ModuleNotFoundError: No module named 'mosaic.evaluation'`.

- [ ] **Step 3: Implement metric contracts**

Create `src/mosaic/evaluation/metrics.py`:

```python
from __future__ import annotations

from dataclasses import dataclass

from mosaic.splats import SplatMap


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


def splat_count_metric(snapshot: SplatMap) -> MetricResult:
    return MetricResult(name="splat_count", value=float(len(snapshot)), unit="splats")
```

- [ ] **Step 4: Export metric contracts**

Create `src/mosaic/evaluation/__init__.py`:

```python
from mosaic.evaluation.metrics import MetricResult, splat_count_metric

__all__ = [
    "MetricResult",
    "splat_count_metric",
]
```

- [ ] **Step 5: Run metric tests to verify they pass**

Run:

```bash
uv run pytest tests/evaluation/test_metrics.py -q
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/mosaic/evaluation tests/evaluation/test_metrics.py
git commit -m "feat: add deterministic evaluation metrics"
```

---

### Task 2: Add Synthetic Multi-View Scenario Factory

**Files:**
- Create: `src/mosaic/evaluation/scenarios.py`
- Modify: `src/mosaic/evaluation/__init__.py`
- Create: `tests/evaluation/test_scenarios.py`

- [ ] **Step 1: Write failing scenario tests**

Create `tests/evaluation/test_scenarios.py`:

```python
from mosaic.evaluation import SyntheticScenario, synthetic_forward_sequence


def test_synthetic_forward_sequence_is_deterministic() -> None:
    first = synthetic_forward_sequence(frame_count=3)
    second = synthetic_forward_sequence(frame_count=3)

    assert first == second
    assert first.name == "synthetic-forward-3"
    assert len(first.sequence) == 3
    assert [observation.timestamp.nanoseconds for observation in first.sequence] == [0, 100_000_000, 200_000_000]


def test_synthetic_forward_sequence_produces_front_camera_observations() -> None:
    scenario = synthetic_forward_sequence(frame_count=2)

    assert isinstance(scenario, SyntheticScenario)
    assert scenario.sequence.observations[0].camera_ids == ("front",)
    assert scenario.sequence.observations[1].views[0].camera_pose.translation.x == 1.0
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
uv run pytest tests/evaluation/test_scenarios.py -q
```

Expected: FAIL with import errors for `SyntheticScenario` or `synthetic_forward_sequence`.

- [ ] **Step 3: Implement synthetic scenario factory**

Create `src/mosaic/evaluation/scenarios.py`:

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

- [ ] **Step 4: Export scenario factory**

Replace `src/mosaic/evaluation/__init__.py` with:

```python
from mosaic.evaluation.metrics import MetricResult, splat_count_metric
from mosaic.evaluation.scenarios import SyntheticScenario, synthetic_forward_sequence

__all__ = [
    "MetricResult",
    "SyntheticScenario",
    "splat_count_metric",
    "synthetic_forward_sequence",
]
```

- [ ] **Step 5: Run scenario tests to verify they pass**

Run:

```bash
uv run pytest tests/evaluation/test_scenarios.py -q
```

Expected: PASS.

- [ ] **Step 6: Run evaluation tests**

Run:

```bash
uv run pytest tests/evaluation -q
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/mosaic/evaluation/scenarios.py src/mosaic/evaluation/__init__.py tests/evaluation/test_scenarios.py
git commit -m "feat: add synthetic evaluation scenarios"
```

---

### Task 3: Add Benchmark Runner and JSON Artifact Writer

**Files:**
- Create: `src/mosaic/evaluation/runner.py`
- Modify: `src/mosaic/evaluation/__init__.py`
- Create: `tests/evaluation/test_runner.py`

- [ ] **Step 1: Write failing benchmark runner tests**

Create `tests/evaluation/test_runner.py`:

```python
import json

from mosaic.core import FrameId
from mosaic.evaluation import BenchmarkArtifact, run_slam_benchmark, synthetic_forward_sequence, write_benchmark_artifact
from mosaic.slam import DeterministicSplatBackend


def test_run_slam_benchmark_processes_scenario_and_reports_metrics() -> None:
    artifact = run_slam_benchmark(
        scenario=synthetic_forward_sequence(frame_count=3),
        backend=DeterministicSplatBackend(map_frame=FrameId("map")),
    )

    assert artifact.scenario_name == "synthetic-forward-3"
    assert artifact.backend_name == "deterministic-splat"
    assert artifact.metrics == [{"name": "splat_count", "value": 3.0, "unit": "splats"}]
    assert artifact.update_count == 3


def test_benchmark_artifact_is_json_ready() -> None:
    artifact = BenchmarkArtifact(
        scenario_name="scenario",
        backend_name="backend",
        update_count=2,
        metrics=[{"name": "splat_count", "value": 2.0, "unit": "splats"}],
    )

    assert artifact.as_dict() == {
        "scenario_name": "scenario",
        "backend_name": "backend",
        "update_count": 2,
        "metrics": [{"name": "splat_count", "value": 2.0, "unit": "splats"}],
    }


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

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
uv run pytest tests/evaluation/test_runner.py -q
```

Expected: FAIL with import errors for `BenchmarkArtifact`, `run_slam_benchmark`, or `write_benchmark_artifact`.

- [ ] **Step 3: Implement benchmark runner**

Create `src/mosaic/evaluation/runner.py`:

```python
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
```

- [ ] **Step 4: Export benchmark runner**

Replace `src/mosaic/evaluation/__init__.py` with:

```python
from mosaic.evaluation.metrics import MetricResult, splat_count_metric
from mosaic.evaluation.runner import BenchmarkArtifact, run_slam_benchmark, write_benchmark_artifact
from mosaic.evaluation.scenarios import SyntheticScenario, synthetic_forward_sequence

__all__ = [
    "BenchmarkArtifact",
    "MetricResult",
    "SyntheticScenario",
    "run_slam_benchmark",
    "splat_count_metric",
    "synthetic_forward_sequence",
    "write_benchmark_artifact",
]
```

- [ ] **Step 5: Run runner tests to verify they pass**

Run:

```bash
uv run pytest tests/evaluation/test_runner.py -q
```

Expected: PASS.

- [ ] **Step 6: Run evaluation tests**

Run:

```bash
uv run pytest tests/evaluation -q
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/mosaic/evaluation/runner.py src/mosaic/evaluation/__init__.py tests/evaluation/test_runner.py
git commit -m "feat: add slam benchmark artifacts"
```

---

### Task 4: Add Regression Gates

**Files:**
- Create: `src/mosaic/evaluation/regression.py`
- Modify: `src/mosaic/evaluation/__init__.py`
- Create: `tests/evaluation/test_regression.py`

- [ ] **Step 1: Write failing regression gate tests**

Create `tests/evaluation/test_regression.py`:

```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
uv run pytest tests/evaluation/test_regression.py -q
```

Expected: FAIL with import errors for `RegressionGate`, `RegressionResult`, or `check_regression_gates`.

- [ ] **Step 3: Implement regression gates**

Create `src/mosaic/evaluation/regression.py`:

```python
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
```

- [ ] **Step 4: Export regression gates**

Replace `src/mosaic/evaluation/__init__.py` with:

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

- [ ] **Step 5: Run regression tests to verify they pass**

Run:

```bash
uv run pytest tests/evaluation/test_regression.py -q
```

Expected: PASS.

- [ ] **Step 6: Run evaluation tests**

Run:

```bash
uv run pytest tests/evaluation -q
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/mosaic/evaluation/regression.py src/mosaic/evaluation/__init__.py tests/evaluation/test_regression.py
git commit -m "feat: add benchmark regression gates"
```

---

### Task 5: Publish Evaluation API at Package Root

**Files:**
- Modify: `src/mosaic/__init__.py`
- Modify: `tests/test_public_api.py`

- [ ] **Step 1: Extend public API test**

Replace `tests/test_public_api.py` with:

```python
from mosaic import (
    BenchmarkArtifact,
    CameraIntrinsics,
    CameraRig,
    DeterministicSplatBackend,
    Embodiment,
    FrameId,
    FusionInput,
    GaussianSplat,
    InMemorySequence,
    PlatformRegistry,
    ProvenancePreservingFusion,
    RegressionGate,
    SplatMap,
    Timestamp,
    TrackingState,
    quadruped_front_rig,
    synthetic_forward_sequence,
)


def test_public_api_exports_core_foundation_types() -> None:
    assert Timestamp.from_seconds(0.5).nanoseconds == 500_000_000
    assert FrameId("map").value == "map"
    assert CameraIntrinsics(width=1, height=1, fx=1.0, fy=1.0, cx=0.5, cy=0.5).width == 1
    assert GaussianSplat(center=(0.0, 0.0, 1.0), covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1)).opacity == 1.0
    assert len(SplatMap(frame=FrameId("map"))) == 0
    assert DeterministicSplatBackend().name == "deterministic-splat"
    assert TrackingState.TRACKING.value == "tracking"
    assert InMemorySequence.__name__ == "InMemorySequence"


def test_public_api_exports_platform_types() -> None:
    platform = quadruped_front_rig()

    assert platform.embodiment is Embodiment.QUADRUPED
    assert isinstance(platform.camera_rig, CameraRig)
    assert PlatformRegistry.__name__ == "PlatformRegistry"


def test_public_api_exports_fusion_types() -> None:
    assert FusionInput.__name__ == "FusionInput"
    assert ProvenancePreservingFusion().name == "provenance-preserving"


def test_public_api_exports_evaluation_types() -> None:
    scenario = synthetic_forward_sequence(frame_count=1)

    assert scenario.name == "synthetic-forward-1"
    assert BenchmarkArtifact.__name__ == "BenchmarkArtifact"
    assert RegressionGate(metric_name="splat_count", minimum=1.0).minimum == 1.0
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
uv run pytest tests/test_public_api.py -q
```

Expected: FAIL with import errors for `BenchmarkArtifact`, `RegressionGate`, or `synthetic_forward_sequence` from `mosaic`.

- [ ] **Step 3: Export evaluation API from package root**

Replace `src/mosaic/__init__.py` with:

```python
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

__version__ = "0.1.0"

__all__ = [
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
    "MetricResult",
    "MultiViewObservation",
    "MultiViewSequence",
    "Pixel",
    "PlatformDescription",
    "PlatformRegistry",
    "Pose3",
    "ProvenancePreservingFusion",
    "Quaternion",
    "RegressionGate",
    "RegressionResult",
    "SplatFusionStrategy",
    "SplatMap",
    "SplatSlamBackend",
    "SplatSlamUpdate",
    "SyntheticScenario",
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

- [ ] **Step 4: Run public API test to verify it passes**

Run:

```bash
uv run pytest tests/test_public_api.py -q
```

Expected: PASS.

- [ ] **Step 5: Run full test suite**

Run:

```bash
uv run pytest -q
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/mosaic/__init__.py tests/test_public_api.py
git commit -m "feat: expose evaluation harness api"
```

---

## Final Verification

- [ ] **Step 1: Run the complete suite**

```bash
uv run pytest -q
```

Expected: PASS for all tests.

- [ ] **Step 2: Confirm benchmark artifact output**

Run:

```bash
uv run python -c "from mosaic import DeterministicSplatBackend, run_slam_benchmark, synthetic_forward_sequence; print(run_slam_benchmark(synthetic_forward_sequence(2), DeterministicSplatBackend()).as_dict())"
```

Expected output includes:

```text
'scenario_name': 'synthetic-forward-2'
'backend_name': 'deterministic-splat'
'update_count': 2
```

- [ ] **Step 3: Inspect working tree**

```bash
git status --short
```

Expected: no uncommitted source or test changes except plan/spec documents that the user has chosen not to commit.

---

## Self-Review Notes

- Spec coverage: This plan implements deterministic synthetic scenarios, metric output, machine-readable JSON artifacts, and regression gates from the migration plan's evaluation milestone.
- Deferred scope: No real dataset loaders, trajectory ATE/RPE metrics, rendering metrics, backend performance profiling, CI configuration, or agent-query evaluation is included.
- Type consistency: `MetricResult`, `SyntheticScenario`, `BenchmarkArtifact`, `RegressionGate`, `RegressionResult`, and exported function names are consistent across tasks and tests.
