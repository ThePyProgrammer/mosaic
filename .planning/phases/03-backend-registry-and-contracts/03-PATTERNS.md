# Phase 3: Backend Registry and Contracts - Pattern Map

**Mapped:** 2026-05-18
**Files analyzed:** 8
**Analogs found:** 8 / 8

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `src/mosaic/slam/registry.py` | registry/model/service | request-response | `src/mosaic/platforms/registry.py` + `src/mosaic/slam/protocol.py` | role-match |
| `src/mosaic/slam/contracts.py` | utility/test-helper | batch | `tests/slam/test_backend_contract.py` + `src/mosaic/evaluation/scenarios.py` | flow-match |
| `src/mosaic/slam/__init__.py` | public export surface | transform | `src/mosaic/slam/__init__.py` | exact |
| `src/mosaic/__init__.py` | root public export surface | transform | `src/mosaic/__init__.py` | exact |
| `src/mosaic/evaluation/runner.py` | service | batch | `src/mosaic/evaluation/runner.py` | exact |
| `tests/slam/test_backend_registry.py` | test | request-response | `tests/platforms/test_registry.py` | role-match |
| `tests/slam/test_backend_contract_helpers.py` | test | batch | `tests/slam/test_backend_contract.py` | role-match |
| `tests/slam/test_backend_contract.py` | test | batch | `tests/slam/test_backend_contract.py` | exact |

## Pattern Assignments

### `src/mosaic/slam/registry.py` (registry/model/service, request-response)

**Analog:** `src/mosaic/platforms/registry.py` for registry mechanics; `src/mosaic/slam/protocol.py` and `src/mosaic/evaluation/runner.py` for frozen metadata and mapping conventions.

**Imports pattern** (`src/mosaic/platforms/registry.py` lines 1-5):
```python
from __future__ import annotations

from dataclasses import dataclass, field

from mosaic.platforms.types import PlatformDescription
```

**Registry duplicate and missing-name pattern** (`src/mosaic/platforms/registry.py` lines 8-25):
```python
@dataclass(slots=True)
class PlatformRegistry:
    _platforms: dict[str, PlatformDescription] = field(default_factory=dict, init=False, repr=False)

    def register(self, platform: PlatformDescription) -> None:
        if platform.name in self._platforms:
            raise ValueError(f"Platform {platform.name!r} is already registered")
        self._platforms[platform.name] = platform

    def get(self, name: str) -> PlatformDescription:
        try:
            return self._platforms[name]
        except KeyError as exc:
            raise KeyError(f"Platform {name!r} is not registered") from exc

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._platforms))
```

**Frozen capability/metadata mapping pattern** (`src/mosaic/slam/protocol.py` lines 13-31):
```python
MetricValue = bool | int | float | str


@dataclass(frozen=True, slots=True)
class BackendCapabilities:
    supports_multi_view: bool
    supports_incremental_mapping: bool
    supports_uncertainty: bool
    runs_out_of_process: bool = False
    parameters: Mapping[str, MetricValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "parameters", MappingProxyType(dict(self.parameters)))
```

**Runtime protocol seam to reference, not replace** (`src/mosaic/slam/protocol.py` lines 48-65):
```python
@runtime_checkable
class SplatSlamBackend(Protocol):
    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def capabilities(self) -> BackendCapabilities:
        raise NotImplementedError

    def reset(self) -> None:
        raise NotImplementedError

    def process(self, observation: MultiViewObservation) -> SplatSlamUpdate:
        raise NotImplementedError

    def snapshot(self) -> SplatMap:
        raise NotImplementedError
```

**Benchmark-style immutable artifact metadata pattern** (`src/mosaic/evaluation/runner.py` lines 36-62):
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

**Implementation notes for planner:**
- Create frozen/slotted value objects for `BackendDependency`, `AvailabilityResult`, and `BackendDescriptor`.
- Use `MetricValue = bool | int | float | str` from `mosaic.slam.protocol` or mirror the same JSON-ready scalar alias.
- Backend registry should store descriptors/factories, not backend instances.
- `names`, descriptor lookup, registration, and availability checks must not call backend factories.
- Duplicate backend names should raise `ValueError`; missing names should raise `KeyError`, matching the platform registry style.
- `default_backend_registry()` should register only the deterministic backend descriptor.

---

### `src/mosaic/slam/contracts.py` (utility/test-helper, batch)

**Analog:** `tests/slam/test_backend_contract.py` for lifecycle expectations; `src/mosaic/evaluation/scenarios.py` for deterministic replay source.

**Imports pattern for backend lifecycle tests** (`tests/slam/test_backend_contract.py` lines 1-13):
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
from mosaic.slam import DeterministicSplatBackend, TrackingState
```

**Core process/snapshot/reset lifecycle assertions** (`tests/slam/test_backend_contract.py` lines 37-69):
```python
def test_deterministic_backend_processes_observation_into_splat_update() -> None:
    backend = DeterministicSplatBackend(map_frame=FrameId("map"))

    update = backend.process(_observation())

    assert backend.name == "deterministic-splat"
    assert update.tracking_state is TrackingState.TRACKING
    assert update.estimated_pose == _observation().views[0].camera_pose
    assert len(update.map_update) == 1
    assert update.diagnostics["splat_count"] == 1


def test_deterministic_backend_snapshot_accumulates_processed_splats() -> None:
    backend = DeterministicSplatBackend(map_frame=FrameId("map"))

    backend.process(_observation(1.0))
    backend.process(_observation(2.0))

    snapshot = backend.snapshot()

    assert snapshot.frame == FrameId("map")
    assert len(snapshot) == 2
    assert snapshot.splats[0].center == (0.0, 0.0, 1.0)
    assert snapshot.splats[1].center == (1.0, 0.0, 1.0)


def test_deterministic_backend_reset_clears_state() -> None:
    backend = DeterministicSplatBackend(map_frame=FrameId("map"))
    backend.process(_observation())

    backend.reset()

    assert len(backend.snapshot()) == 0
```

**Synthetic replay source** (`src/mosaic/evaluation/scenarios.py` lines 20-34):
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

**Update validation to respect in generic helpers** (`src/mosaic/slam/protocol.py` lines 34-45):
```python
@dataclass(frozen=True, slots=True)
class SplatSlamUpdate:
    timestamp: Timestamp
    tracking_state: TrackingState
    estimated_pose: Pose3 | None
    map_update: SplatMap
    diagnostics: Mapping[str, MetricValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.tracking_state is TrackingState.TRACKING and self.estimated_pose is None:
            raise ValueError("Tracking updates require an estimated_pose")
        object.__setattr__(self, "diagnostics", MappingProxyType(dict(self.diagnostics)))
```

**Implementation notes for planner:**
- Keep helpers as ordinary importable functions, not a pytest plugin.
- Generic helpers should verify lifecycle invariants: `reset()` clears or returns stable empty state, `process()` returns `SplatSlamUpdate`, `snapshot()` returns `SplatMap`, diagnostics are JSON-ready, deterministic replay creates repeatable contract-level outcomes.
- Do not assert fake-backend-specific splat centers in shared helpers; keep those assertions in deterministic backend tests.
- For availability-gated helpers, import `pytest` only in helper code if skip behavior is intentionally coupled to pytest; otherwise return/raise a simple contract failure and let tests call `pytest.skip()`.

---

### `src/mosaic/slam/__init__.py` (public export surface, transform)

**Analog:** `src/mosaic/slam/__init__.py`.

**Current export pattern** (`src/mosaic/slam/__init__.py` lines 1-10):
```python
from mosaic.slam.fake_backend import DeterministicSplatBackend
from mosaic.slam.protocol import BackendCapabilities, SplatSlamBackend, SplatSlamUpdate, TrackingState

__all__ = [
    "BackendCapabilities",
    "DeterministicSplatBackend",
    "SplatSlamBackend",
    "SplatSlamUpdate",
    "TrackingState",
]
```

**Implementation notes for planner:**
- Add explicit imports for stable new registry and contract helper symbols.
- Add every public symbol to `__all__` explicitly.
- Do not use wildcard imports.
- Prefer exporting registry/descriptor APIs from `mosaic.slam`; root `mosaic` exports should be narrower and deliberate.

---

### `src/mosaic/__init__.py` (root public export surface, transform)

**Analog:** `src/mosaic/__init__.py`.

**Root import style** (`src/mosaic/__init__.py` lines 1-48):
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

**Root `__all__` style** (`src/mosaic/__init__.py` lines 50-104):
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

**Implementation notes for planner:**
- If Phase 3 makes backend registry APIs root-public, add them in the same explicit import/`__all__` style.
- If API stability is uncertain, export from `mosaic.slam` only and avoid root churn.
- Update `tests/test_public_api.py` if root exports change.

---

### `src/mosaic/evaluation/runner.py` (service, batch)

**Analog:** `src/mosaic/evaluation/runner.py`.

**Benchmark loop and metadata extraction pattern** (`src/mosaic/evaluation/runner.py` lines 65-85):
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

**Current direct-backend metadata pattern** (`src/mosaic/evaluation/runner.py` lines 92-103):
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

**Implementation notes for planner:**
- Preserve direct `SplatSlamBackend` usage; do not force benchmarks to use descriptors.
- If descriptor-aware benchmark metadata is added, make it additive or optional so current `tests/evaluation/test_runner.py` behavior remains valid.
- Continue returning JSON-ready scalar metadata only.

---

### `tests/slam/test_backend_registry.py` (test, request-response)

**Analog:** `tests/platforms/test_registry.py`.

**Imports and helper factory style** (`tests/platforms/test_registry.py` lines 1-29):
```python
import pytest

from mosaic.core import CameraIntrinsics, FrameId, Pose3, Quaternion, Translation3
from mosaic.platforms import CameraMount, CameraRig, Embodiment, PlatformDescription, PlatformRegistry


def _platform(name: str) -> PlatformDescription:
    base_frame = FrameId("base_link")
    return PlatformDescription(
        name=name,
        embodiment=Embodiment.CUSTOM,
        base_frame=base_frame,
        camera_rig=CameraRig(
            frame=base_frame,
            cameras=(
                CameraMount(
                    camera_id="front",
                    pose=Pose3(
                        parent_frame=base_frame,
                        child_frame=FrameId("camera/front"),
                        translation=Translation3(),
                        rotation=Quaternion.identity(),
                    ),
                    intrinsics=CameraIntrinsics(width=640, height=480, fx=400.0, fy=400.0, cx=320.0, cy=240.0),
                ),
            ),
        ),
    )
```

**Registry happy-path and duplicate/missing tests** (`tests/platforms/test_registry.py` lines 31-53):
```python
def test_registry_registers_and_retrieves_platforms() -> None:
    platform = _platform("research-rig")
    registry = PlatformRegistry()

    registry.register(platform)

    assert registry.get("research-rig") == platform
    assert registry.names == ("research-rig",)


def test_registry_rejects_duplicate_names() -> None:
    registry = PlatformRegistry()
    registry.register(_platform("research-rig"))

    with pytest.raises(ValueError, match="already registered"):
        registry.register(_platform("research-rig"))


def test_registry_reports_missing_platforms() -> None:
    registry = PlatformRegistry()

    with pytest.raises(KeyError, match="missing"):
        registry.get("missing")
```

**Artifact JSON-ready assertion style to reuse for descriptor metadata** (`tests/artifacts/test_slam_and_evaluation_artifacts.py` lines 45-64):
```python
def test_splat_slam_update_artifact_round_trips_tracking_update() -> None:
    update = SplatSlamUpdate(
        timestamp=Timestamp(1_000_000_000),
        tracking_state=TrackingState.TRACKING,
        estimated_pose=_pose(),
        map_update=_splat_map(),
        diagnostics={"quality": 1.0, "accepted": True, "label": "deterministic"},
    )

    artifact = splat_slam_update_to_artifact(update)
    restored = splat_slam_update_from_artifact(artifact)

    assert artifact["schema"] == "mosaic.splat_slam_update"
    assert artifact["payload"]["tracking_state"] == "tracking"
    assert restored.timestamp == update.timestamp
    assert restored.tracking_state is TrackingState.TRACKING
    assert restored.estimated_pose == update.estimated_pose
    assert restored.map_update == update.map_update
    assert restored.diagnostics == update.diagnostics
    json.dumps(artifact, sort_keys=True)
```

**Implementation notes for planner:**
- Add tests for descriptor validation: blank names, blank versions/dependencies if modeled, JSON-ready metadata scalars, immutable mappings/tuples.
- Add tests that `names`, descriptor lookup, and availability checks do not call the factory.
- Add tests that `create(name)` returns fresh `DeterministicSplatBackend` instances.
- Add tests for default registry containing exactly the deterministic backend.
- Add tests for unavailable dependency probe diagnostics with a definitely missing package name.

---

### `tests/slam/test_backend_contract_helpers.py` (test, batch)

**Analog:** `tests/slam/test_backend_contract.py` and `tests/evaluation/test_runner.py`.

**Existing backend lifecycle test shape** (`tests/slam/test_backend_contract.py` lines 37-69):
```python
def test_deterministic_backend_processes_observation_into_splat_update() -> None:
    backend = DeterministicSplatBackend(map_frame=FrameId("map"))

    update = backend.process(_observation())

    assert backend.name == "deterministic-splat"
    assert update.tracking_state is TrackingState.TRACKING
    assert update.estimated_pose == _observation().views[0].camera_pose
    assert len(update.map_update) == 1
    assert update.diagnostics["splat_count"] == 1


def test_deterministic_backend_snapshot_accumulates_processed_splats() -> None:
    backend = DeterministicSplatBackend(map_frame=FrameId("map"))

    backend.process(_observation(1.0))
    backend.process(_observation(2.0))

    snapshot = backend.snapshot()

    assert snapshot.frame == FrameId("map")
    assert len(snapshot) == 2
    assert snapshot.splats[0].center == (0.0, 0.0, 1.0)
    assert snapshot.splats[1].center == (1.0, 0.0, 1.0)


def test_deterministic_backend_reset_clears_state() -> None:
    backend = DeterministicSplatBackend(map_frame=FrameId("map"))
    backend.process(_observation())

    backend.reset()

    assert len(backend.snapshot()) == 0
```

**Benchmark replay loop to adapt for deterministic replay helper tests** (`src/mosaic/evaluation/runner.py` lines 65-75):
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
```

**State edge-case construction pattern** (`tests/artifacts/test_slam_and_evaluation_artifacts.py` lines 67-83):
```python
def test_splat_slam_update_artifact_round_trips_lost_update_without_pose() -> None:
    update = SplatSlamUpdate(
        timestamp=Timestamp(1_000_000_000),
        tracking_state=TrackingState.LOST,
        estimated_pose=None,
        map_update=_splat_map(),
        diagnostics={"quality": 0.0, "accepted": False, "label": "lost"},
    )

    artifact = splat_slam_update_to_artifact(update)
    restored = splat_slam_update_from_artifact(artifact)

    assert artifact["payload"]["tracking_state"] == "lost"
    assert restored.tracking_state is TrackingState.LOST
    assert restored.estimated_pose is None
    assert restored.map_update == update.map_update
    assert restored.diagnostics == update.diagnostics
```

**Implementation notes for planner:**
- Use small test-only stub backends for `LOST` and `NOT_INITIALIZED` states instead of forcing deterministic backend to simulate errors.
- Assert availability-gated helper skips unavailable descriptors using the availability diagnostic as the reason.
- Test helper functions against a factory/descriptor that creates fresh backends.
- Keep generic helper tests free of fake-backend geometry assertions.

---

### `tests/slam/test_backend_contract.py` (test, batch)

**Analog:** `tests/slam/test_backend_contract.py`.

**Current local observation helper** (`tests/slam/test_backend_contract.py` lines 16-34):
```python
def _observation(seconds: float = 1.0) -> MultiViewObservation:
    timestamp = Timestamp.from_seconds(seconds)
    return MultiViewObservation(
        timestamp=timestamp,
        views=(
            CameraObservation(
                camera_id="front",
                timestamp=timestamp,
                camera_pose=Pose3(
                    parent_frame=FrameId("world"),
                    child_frame=FrameId("camera/front"),
                    translation=Translation3(x=1.0, y=0.0, z=0.0),
                    rotation=Quaternion.identity(),
                ),
                intrinsics=CameraIntrinsics(width=1, height=1, fx=1.0, fy=1.0, cx=0.5, cy=0.5),
                color=ImageBuffer(width=1, height=1, channels=3, encoding=ImageEncoding.RGB8, data=b"\xff\xff\xff"),
            ),
        ),
    )
```

**Current deterministic backend behavior assertions** (`tests/slam/test_backend_contract.py` lines 37-69):
```python
def test_deterministic_backend_processes_observation_into_splat_update() -> None:
    backend = DeterministicSplatBackend(map_frame=FrameId("map"))

    update = backend.process(_observation())

    assert backend.name == "deterministic-splat"
    assert update.tracking_state is TrackingState.TRACKING
    assert update.estimated_pose == _observation().views[0].camera_pose
    assert len(update.map_update) == 1
    assert update.diagnostics["splat_count"] == 1


def test_deterministic_backend_snapshot_accumulates_processed_splats() -> None:
    backend = DeterministicSplatBackend(map_frame=FrameId("map"))

    backend.process(_observation(1.0))
    backend.process(_observation(2.0))

    snapshot = backend.snapshot()

    assert snapshot.frame == FrameId("map")
    assert len(snapshot) == 2
    assert snapshot.splats[0].center == (0.0, 0.0, 1.0)
    assert snapshot.splats[1].center == (1.0, 0.0, 1.0)


def test_deterministic_backend_reset_clears_state() -> None:
    backend = DeterministicSplatBackend(map_frame=FrameId("map"))
    backend.process(_observation())

    backend.reset()

    assert len(backend.snapshot()) == 0
```

**Implementation notes for planner:**
- Keep deterministic-backend-specific assertions here.
- Add or call shared helper functions from `mosaic.slam.contracts` for generic lifecycle coverage.
- Prefer `synthetic_forward_sequence()` for shared replay coverage, while keeping `_observation()` only where exact fake-backend internals are asserted.

## Shared Patterns

### Pure-Python backend isolation
**Source:** `src/mosaic/slam/protocol.py`
**Apply to:** `src/mosaic/slam/registry.py`, `src/mosaic/slam/contracts.py`, all tests
```python
@runtime_checkable
class SplatSlamBackend(Protocol):
    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def capabilities(self) -> BackendCapabilities:
        raise NotImplementedError

    def reset(self) -> None:
        raise NotImplementedError

    def process(self, observation: MultiViewObservation) -> SplatSlamUpdate:
        raise NotImplementedError

    def snapshot(self) -> SplatMap:
        raise NotImplementedError
```

### Immutable mappings for metadata and diagnostics
**Source:** `src/mosaic/slam/protocol.py`, `src/mosaic/evaluation/runner.py`
**Apply to:** `BackendCapabilities`, `BackendDescriptor`, `AvailabilityResult`, `BenchmarkArtifact`, update diagnostics
```python
object.__setattr__(self, "parameters", MappingProxyType(dict(self.parameters)))
object.__setattr__(self, "diagnostics", MappingProxyType(dict(self.diagnostics)))
```

### Registry duplicate/missing error style
**Source:** `src/mosaic/platforms/registry.py`
**Apply to:** `BackendRegistry.register`, `BackendRegistry.descriptor`, `BackendRegistry.create`
```python
if platform.name in self._platforms:
    raise ValueError(f"Platform {platform.name!r} is already registered")
try:
    return self._platforms[name]
except KeyError as exc:
    raise KeyError(f"Platform {name!r} is not registered") from exc
```

### Deterministic backend factory target
**Source:** `src/mosaic/slam/fake_backend.py`
**Apply to:** `default_backend_registry()`
```python
@dataclass(slots=True)
class DeterministicSplatBackend:
    map_frame: FrameId = field(default_factory=lambda: FrameId("map"))
    _splats: list[GaussianSplat] = field(default_factory=list, init=False, repr=False)
```

### Synthetic replay for contract helpers
**Source:** `src/mosaic/evaluation/scenarios.py`
**Apply to:** `src/mosaic/slam/contracts.py`, `tests/slam/test_backend_contract_helpers.py`
```python
def synthetic_forward_sequence(frame_count: int) -> SyntheticScenario:
    if frame_count <= 0:
        raise ValueError("synthetic_forward_sequence frame_count must be positive")
    observations = tuple(_observation(index) for index in range(frame_count))
    return SyntheticScenario(name=f"synthetic-forward-{frame_count}", sequence=InMemorySequence(observations))
```

### Public export surfaces
**Source:** `src/mosaic/slam/__init__.py`, `src/mosaic/__init__.py`
**Apply to:** modified package `__init__.py` files
```python
from mosaic.slam.fake_backend import DeterministicSplatBackend
from mosaic.slam.protocol import BackendCapabilities, SplatSlamBackend, SplatSlamUpdate, TrackingState

__all__ = [
    "BackendCapabilities",
    "DeterministicSplatBackend",
    "SplatSlamBackend",
    "SplatSlamUpdate",
    "TrackingState",
]
```

### Stable JSON output for benchmark artifacts
**Source:** `src/mosaic/evaluation/runner.py`
**Apply to:** any descriptor metadata included in evaluation output
```python
def write_benchmark_artifact(artifact: BenchmarkArtifact, path: Path) -> None:
    path.write_text(json.dumps(artifact.as_dict(), indent=2, sort_keys=True) + "\n")
```

## No Analog Found

No files lack a usable analog. The backend registry itself has only a role-match analog (`PlatformRegistry`) rather than an exact factory/availability registry, but the required pieces are covered by existing registry, protocol, immutable metadata, deterministic backend, and lifecycle test patterns.

| File | Role | Data Flow | Reason |
|------|------|-----------|--------|
| — | — | — | All planned files have at least a role-match or flow-match analog. |

## Metadata

**Analog search scope:** `src/mosaic/**`, `tests/**`, project instructions in `CLAUDE.md`, phase docs in `.planning/phases/03-backend-registry-and-contracts/`
**Files scanned:** 6 source analogs + 4 test analogs + 3 phase context files + project instructions
**Pattern extraction date:** 2026-05-18
