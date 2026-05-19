# Phase 04: fusion-diagnostics-and-semantics-hardening - Pattern Map

**Mapped:** 2026-05-19
**Files analyzed:** 8
**Analogs found:** 8 / 8

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `src/mosaic/fusion/protocol.py` | model/protocol | transform | `src/mosaic/slam/protocol.py`; `src/mosaic/agents/queries.py` | exact |
| `src/mosaic/fusion/strategies.py` | service/strategy | transform | `src/mosaic/fusion/strategies.py`; `src/mosaic/slam/fake_backend.py` | exact |
| `src/mosaic/fusion/__init__.py` | config/barrel export | request-response/import surface | `src/mosaic/agents/__init__.py`; `src/mosaic/slam/__init__.py` | exact |
| `src/mosaic/__init__.py` | config/root export | request-response/import surface | `src/mosaic/__init__.py`; `tests/test_public_api.py` | exact |
| `tests/fusion/test_fusion_protocol.py` | test | transform | `tests/fusion/test_fusion_protocol.py`; `tests/agents/test_queries.py` | exact |
| `tests/fusion/test_strategies.py` | test | transform | `tests/fusion/test_strategies.py`; `tests/slam/test_backend_contract.py` | exact |
| `tests/test_public_api.py` | test | request-response/import surface | `tests/test_public_api.py`; `tests/agents/test_queries.py` | exact |
| `README.md` | documentation | request-response/import surface | `README.md`; `tests/test_readme_contract.py` | exact |

## Pattern Assignments

### `src/mosaic/fusion/protocol.py` (model/protocol, transform)

**Analog:** `src/mosaic/slam/protocol.py` plus existing `src/mosaic/fusion/protocol.py`

**Imports pattern** (`src/mosaic/fusion/protocol.py` lines 1-9):
```python
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Mapping, Protocol, runtime_checkable

from mosaic.core import FrameId
from mosaic.splats import SplatMap
```

**Typed protocol/result pattern** (`src/mosaic/slam/protocol.py` lines 13-45):
```python
MetricValue = bool | int | float | str


class TrackingState(StrEnum):
    NOT_INITIALIZED = "not_initialized"
    TRACKING = "tracking"
    LOST = "lost"


@dataclass(frozen=True, slots=True)
class BackendCapabilities:
    supports_multi_view: bool
    supports_incremental_mapping: bool
    supports_uncertainty: bool
    runs_out_of_process: bool = False
    parameters: Mapping[str, MetricValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "parameters", MappingProxyType(dict(self.parameters)))


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

**Existing fusion input/result pattern to extend** (`src/mosaic/fusion/protocol.py` lines 11-44):
```python
FusionMetricValue = bool | int | float | str


class FusionStatus(StrEnum):
    FUSED = "fused"
    REJECTED = "rejected"


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


@dataclass(frozen=True, slots=True)
class FusionResult:
    status: FusionStatus
    fused_map: SplatMap
    diagnostics: Mapping[str, FusionMetricValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "diagnostics", MappingProxyType(dict(self.diagnostics)))
```

**Mapping summary analog, validation, and defensive freeze** (`src/mosaic/agents/queries.py` lines 53-63):
```python
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

**Protocol interface pattern** (`src/mosaic/fusion/protocol.py` lines 46-53):
```python
@runtime_checkable
class SplatFusionStrategy(Protocol):
    @property
    def name(self) -> str:
        raise NotImplementedError

    def fuse(self, fusion_input: FusionInput) -> FusionResult:
        raise NotImplementedError
```

**Planner guidance:** Add `FusionProvenanceSummary`, `FusionUncertaintySummary`, and `FusionConflictSummary` as `@dataclass(frozen=True, slots=True)` contracts in this file. Copy `MappingProxyType(dict(...))` defensive-freeze style exactly. Keep flat `FusionMetricValue` scalar unless the implementation deliberately expands it; put nested per-provenance and reason maps in typed summaries.

---

### `src/mosaic/fusion/strategies.py` (service/strategy, transform)

**Analog:** Existing `src/mosaic/fusion/strategies.py` and `src/mosaic/slam/fake_backend.py`

**Imports pattern** (`src/mosaic/fusion/strategies.py` lines 1-7):
```python
from __future__ import annotations

from dataclasses import dataclass

from mosaic.fusion.protocol import FusionInput, FusionResult, FusionStatus
from mosaic.splats import GaussianSplat, SplatMap
```

**Core preservation transform pattern** (`src/mosaic/fusion/strategies.py` lines 9-29):
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

**Stateful deterministic service analog** (`src/mosaic/slam/fake_backend.py` lines 30-53):
```python
    def reset(self) -> None:
        self._splats.clear()

    def process(self, observation: MultiViewObservation) -> SplatSlamUpdate:
        index = len(self._splats)
        first_view = observation.views[0]
        splat = GaussianSplat(
            center=(float(index), 0.0, 1.0),
            covariance_upper=(0.01, 0.0, 0.0, 0.01, 0.0, 0.01),
            color_rgb=(1.0, 1.0, 1.0),
            opacity=1.0,
            provenance=first_view.camera_id,
        )
        self._splats.append(splat)
        return SplatSlamUpdate(
            timestamp=observation.timestamp,
            tracking_state=TrackingState.TRACKING,
            estimated_pose=first_view.camera_pose,
            map_update=SplatMap(frame=self.map_frame, splats=(splat,)),
            diagnostics={"splat_count": len(self._splats)},
        )

    def snapshot(self) -> SplatMap:
        return SplatMap(frame=self.map_frame, splats=tuple(self._splats))
```

**Splat field semantics for uncertainty/conflict calculations** (`src/mosaic/splats/primitives.py` lines 16-20, 36-53):
```python
    center: tuple[float, float, float]
    covariance_upper: tuple[float, float, float, float, float, float]
    color_rgb: tuple[float, float, float] = (1.0, 1.0, 1.0)
    opacity: float = 1.0
    provenance: str | None = None
```
```python
        xx, xy, xz, yy, yz, zz = self.covariance_upper
        if xx <= 0.0 or yy <= 0.0 or zz <= 0.0:
            raise ValueError("GaussianSplat covariance diagonal values must be positive")
        if xx * yy - xy * xy <= 0.0:
            raise ValueError("GaussianSplat covariance must be positive definite")
        determinant = (
            xx * yy * zz
            + 2.0 * xy * xz * yz
            - xx * yz * yz
            - yy * xz * xz
            - zz * xy * xy
        )
        if determinant <= 0.0:
            raise ValueError("GaussianSplat covariance must be positive definite")
        if any(channel < 0.0 or channel > 1.0 for channel in self.color_rgb):
            raise ValueError("GaussianSplat color_rgb channels must be between 0 and 1")
        if self.opacity < 0.0 or self.opacity > 1.0:
            raise ValueError("GaussianSplat opacity must be between 0 and 1")
```

**Planner guidance:** Preserve this strategy's boring concatenation behavior. Add private helper functions if needed for provenance counting, covariance diagonal statistics, and conservative pairwise conflict scans. Update the label from `preserved-not-optimized` to `preserved_not_optimized` in typed and flat diagnostics. Conflict candidates must not drop splats or change `FusionStatus.FUSED`.

---

### `src/mosaic/fusion/__init__.py` (config/barrel export, request-response/import surface)

**Analog:** `src/mosaic/agents/__init__.py`

**Barrel import/export pattern** (`src/mosaic/agents/__init__.py` lines 1-17):
```python
from mosaic.agents.posteriors import SplatPosteriorView
from mosaic.agents.queries import (
    AgentQueryKind,
    LocalRadiusQuery,
    PosteriorSummary,
    ProvenanceSummary,
    SplatQueryResult,
)

__all__ = [
    "AgentQueryKind",
    "LocalRadiusQuery",
    "PosteriorSummary",
    "ProvenanceSummary",
    "SplatPosteriorView",
    "SplatQueryResult",
]
```

**Existing fusion export pattern to extend** (`src/mosaic/fusion/__init__.py` lines 1-10):
```python
from mosaic.fusion.protocol import FusionInput, FusionResult, FusionStatus, SplatFusionStrategy
from mosaic.fusion.strategies import ProvenancePreservingFusion

__all__ = [
    "FusionInput",
    "FusionResult",
    "FusionStatus",
    "ProvenancePreservingFusion",
    "SplatFusionStrategy",
]
```

**Planner guidance:** Import new summary dataclasses explicitly from `mosaic.fusion.protocol` and add them to `__all__`. Do not wildcard import.

---

### `src/mosaic/__init__.py` (config/root export, request-response/import surface)

**Analog:** Existing `src/mosaic/__init__.py` and `tests/test_public_api.py`

**Root import style** (`src/mosaic/__init__.py` lines 35-36):
```python
from mosaic.fusion import FusionInput, FusionResult, FusionStatus, ProvenancePreservingFusion, SplatFusionStrategy
from mosaic.platforms import (
```

**Root `__all__` style** (`src/mosaic/__init__.py` lines 52-66):
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
```

**Public API smoke test analog** (`tests/test_public_api.py` lines 44-47):
```python
def test_public_api_exports_fusion_types() -> None:
    assert FusionInput.__name__ == "FusionInput"
    assert ProvenancePreservingFusion().name == "provenance-preserving"
```

**Planner guidance:** Root-export new fusion summaries only if the plan decides they are stable package-level API. If root-exported, add them to both the import list and `__all__`, and extend `tests/test_public_api.py`.

---

### `tests/fusion/test_fusion_protocol.py` (test, transform)

**Analog:** Existing `tests/fusion/test_fusion_protocol.py` and `tests/agents/test_queries.py`

**Imports and helper pattern** (`tests/fusion/test_fusion_protocol.py` lines 1-18):
```python
import pytest

from mosaic.core import FrameId
from mosaic.fusion import FusionInput, FusionResult, FusionStatus
from mosaic.splats import GaussianSplat, SplatMap


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

**Validation test pattern** (`tests/fusion/test_fusion_protocol.py` lines 21-38):
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

**Mapping-freeze test pattern** (`tests/fusion/test_fusion_protocol.py` lines 41-50):
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

**Summary validation/freezing analog** (`tests/agents/test_queries.py` lines 50-64):
```python
def test_provenance_summary_rejects_blank_sources_and_negative_counts() -> None:
    with pytest.raises(ValueError, match="must not be blank"):
        ProvenanceSummary(counts={" ": 1})
    with pytest.raises(ValueError, match="non-negative"):
        ProvenanceSummary(counts={"front": -1})


def test_provenance_summary_freezes_and_copies_counts() -> None:
    counts = {"front": 2}
    summary = ProvenanceSummary(counts=counts)
    counts["front"] = 99

    assert summary.counts["front"] == 2
    with pytest.raises(TypeError):
        summary.counts["rear"] = 1
```

**Planner guidance:** Add tests for each new fusion summary dataclass: reject negative counts, blank provenance/reason keys, invalid/non-finite uncertainty stats if implemented, and verify mapping fields are copied then frozen.

---

### `tests/fusion/test_strategies.py` (test, transform)

**Analog:** Existing `tests/fusion/test_strategies.py` and `tests/slam/test_backend_contract.py`

**Imports/helper pattern** (`tests/fusion/test_strategies.py` lines 1-11):
```python
from mosaic.core import FrameId
from mosaic.fusion import FusionInput, FusionStatus, ProvenancePreservingFusion
from mosaic.splats import GaussianSplat, SplatMap


def _splat(x: float, provenance: str) -> GaussianSplat:
    return GaussianSplat(
        center=(x, 0.0, 1.0),
        covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1),
        provenance=provenance,
    )
```

**Core strategy behavior pattern** (`tests/fusion/test_strategies.py` lines 14-27):
```python
def test_provenance_preserving_fusion_concatenates_maps_without_mutating_inputs() -> None:
    first = SplatMap(frame=FrameId("map"), splats=(_splat(0.0, "front"),))
    second = SplatMap(frame=FrameId("map"), splats=(_splat(1.0, "rear"),))
    strategy = ProvenancePreservingFusion()

    result = strategy.fuse(FusionInput(maps=(first, second)))

    assert strategy.name == "provenance-preserving"
    assert result.status is FusionStatus.FUSED
    assert len(first) == 1
    assert len(second) == 1
    assert len(result.fused_map) == 2
    assert [splat.provenance for splat in result.fused_map.splats] == ["front", "rear"]
```

**Current diagnostics assertion to harden** (`tests/fusion/test_strategies.py` lines 29-40):
```python
def test_provenance_preserving_fusion_reports_diagnostics() -> None:
    first = SplatMap(frame=FrameId("map"), splats=(_splat(0.0, "front"), _splat(1.0, "left")))
    second = SplatMap(frame=FrameId("map"), splats=(_splat(2.0, "rear"),))

    result = ProvenancePreservingFusion().fuse(FusionInput(maps=(first, second)))

    assert result.diagnostics == {
        "source_map_count": 2,
        "source_splat_count": 3,
        "fused_splat_count": 3,
        "uncertainty_model": "preserved-not-optimized",
    }
```

**Diagnostic update assertion analog** (`tests/slam/test_backend_contract.py` lines 56-65):
```python
def test_deterministic_backend_processes_observation_into_splat_update() -> None:
    backend = DeterministicSplatBackend(map_frame=FrameId("map"))

    update = backend.process(_observation())

    assert backend.name == "deterministic-splat"
    assert update.tracking_state is TrackingState.TRACKING
    assert update.estimated_pose == _observation().views[0].camera_pose
    assert len(update.map_update) == 1
    assert update.diagnostics["splat_count"] == 1
```

**Planner guidance:** Extend strategy tests to assert typed summaries and selected flat keys together. Add an anti-grid conflict case with two near/same-center splats from different provenance sources, clearly different color/opacity/covariance, and assert both splats remain in `result.fused_map.splats`, `result.status is FusionStatus.FUSED`, conflict count is non-zero, reason counts include the expected mismatch, and model label is exactly `preserved_not_optimized`.

---

### `tests/test_public_api.py` (test, request-response/import surface)

**Analog:** Existing `tests/test_public_api.py`

**Root import pattern** (`tests/test_public_api.py` lines 1-22):
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

**Fusion export test pattern** (`tests/test_public_api.py` lines 44-47):
```python
def test_public_api_exports_fusion_types() -> None:
    assert FusionInput.__name__ == "FusionInput"
    assert ProvenancePreservingFusion().name == "provenance-preserving"
```

**Subpackage export test analog** (`tests/agents/test_queries.py` lines 67-83):
```python
def test_agents_exports_public_query_and_result_types() -> None:
    import mosaic.agents as agents

    assert agents.AgentQueryKind is AgentQueryKind
    assert agents.LocalRadiusQuery is LocalRadiusQuery
    assert agents.PosteriorSummary is PosteriorSummary
    assert agents.ProvenanceSummary is ProvenanceSummary
    assert agents.SplatPosteriorView is SplatPosteriorView
    assert agents.SplatQueryResult is SplatQueryResult
    assert set(agents.__all__) >= {
        "AgentQueryKind",
        "LocalRadiusQuery",
        "PosteriorSummary",
        "ProvenanceSummary",
        "SplatPosteriorView",
        "SplatQueryResult",
    }
```

**Planner guidance:** If summaries are exported from `mosaic.fusion`, add a fusion subpackage export test matching the agents style. If root-exported, extend root imports and `test_public_api_exports_fusion_types()`.

---

### `README.md` (documentation, request-response/import surface)

**Analog:** Existing `README.md` and `tests/test_readme_contract.py`

**Fusion public API table row** (`README.md` lines 49-58):
```markdown
| Package surface | Responsibility | Representative APIs |
|-----------------|----------------|---------------------|
| `mosaic.core` | Frames, timestamps, poses, cameras, image buffers, and observations | `FrameId`, `Timestamp`, `Pose3`, `CameraIntrinsics`, `MultiViewObservation` |
| `mosaic.datasets` | Replayable multi-view sequences | `MultiViewSequence`, `InMemorySequence` |
| `mosaic.splats` | Gaussian primitives and immutable map snapshots | `GaussianSplat`, `SplatMap` |
| `mosaic.slam` | Backend lifecycle protocols and deterministic reference backend | `SplatSlamBackend`, `SplatSlamUpdate`, `TrackingState`, `DeterministicSplatBackend` |
| `mosaic.platforms` | Robot-neutral platform descriptions and camera rigs | `CameraRig`, `PlatformRegistry`, `quadruped_front_rig`, `ugv_surround_rig`, `humanoid_stereo_rig` |
| `mosaic.fusion` | Splat-map fusion contracts and deterministic reference strategy | `FusionInput`, `FusionResult`, `FusionStatus`, `ProvenancePreservingFusion` |
```

**Boundary note pattern** (`README.md` lines 155-162):
```markdown
## Backend and Dependency Boundary

Mosaic Phase 1 is a pure-Python headless library. Core imports are expected to work with `dependencies = []` and without GPU, native computer-vision stacks, robot middleware, browser services, or provider SDKs.

`DeterministicSplatBackend` is a deterministic reference backend for contract tests, examples, replay validation, and benchmark smoke checks. It is not a real 3D Gaussian Splatting optimizer.

`ProvenancePreservingFusion` is a provenance-preserving contract strategy. It validates compatible map inputs and preserves splats and source information for tests. It is not real Gaussian optimization, uncertainty minimization, loop closure, map alignment, or multi-session reconstruction.
```

**README smoke test constraints** (`tests/test_readme_contract.py` lines 62-73, 77-89):
```python
def test_readme_contains_required_phase_1_headings_and_commands() -> None:
    readme = _readme()

    for heading in REQUIRED_HEADINGS:
        assert heading in readme

    for command in REQUIRED_COMMANDS:
        assert command in readme

    assert "73" in readme

    for module_name in REQUIRED_MODULES:
        assert module_name in readme
```
```python
def test_readme_examples_preserve_dependency_boundary() -> None:
    readme = _readme()

    assert "not required for Phase 1" in readme
    assert "deferred, not required for Phase 1, and out of scope" in readme

    for line in readme.splitlines():
        normalized = line.casefold()
        for term in BOUNDARY_TERMS:
            if term in normalized:
                assert not normalized.startswith("pip install")
                assert not normalized.startswith("uv add")
                assert not normalized.startswith("uv pip install")
```

**Planner guidance:** Add a concise Phase 04 boundary sentence near the existing `ProvenancePreservingFusion` paragraph: it preserves and diagnoses splats, reports `preserved_not_optimized`, and does not optimize Gaussians or collapse overlapping splats into occupancy-grid cells. Do not add dependency installation instructions.

## Shared Patterns

### Frozen dataclass contracts
**Source:** `src/mosaic/fusion/protocol.py` lines 19-33; `src/mosaic/agents/queries.py` lines 38-63
**Apply to:** `FusionProvenanceSummary`, `FusionUncertaintySummary`, `FusionConflictSummary`, and expanded `FusionResult`
```python
@dataclass(frozen=True, slots=True)
class FusionInput:
    maps: tuple[SplatMap, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "maps", tuple(self.maps))
        if not self.maps:
            raise ValueError("FusionInput requires at least one map")
```
```python
object.__setattr__(self, "counts", MappingProxyType(dict(self.counts)))
```

### Machine-readable scalar diagnostics
**Source:** `src/mosaic/fusion/protocol.py` lines 11, 36-44; `src/mosaic/evaluation/runner.py` lines 14-18, 53-62
**Apply to:** `FusionResult.diagnostics`, strategy flat diagnostics, tests
```python
FusionMetricValue = bool | int | float | str
```
```python
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

### Public export surfaces
**Source:** `src/mosaic/fusion/__init__.py` lines 1-10; `src/mosaic/__init__.py` lines 35-36, 52-66
**Apply to:** fusion summary exports and optional root exports
```python
from mosaic.fusion.protocol import FusionInput, FusionResult, FusionStatus, SplatFusionStrategy
from mosaic.fusion.strategies import ProvenancePreservingFusion

__all__ = [
    "FusionInput",
    "FusionResult",
    "FusionStatus",
    "ProvenancePreservingFusion",
    "SplatFusionStrategy",
]
```

### Error handling and validation
**Source:** `src/mosaic/splats/primitives.py` lines 27-53; `tests/fusion/test_fusion_protocol.py` lines 21-28
**Apply to:** summary constructors and protocol tests
```python
        if len(self.center) != 3:
            raise ValueError("GaussianSplat center must contain three coordinates")
        if len(self.covariance_upper) != 6:
            raise ValueError("GaussianSplat covariance_upper must contain six values")
```
```python
    with pytest.raises(ValueError, match="same frame"):
        FusionInput(maps=(_map("map"), _map("other")))
```

### Deterministic pure-Python test style
**Source:** `tests/fusion/test_strategies.py` lines 14-27
**Apply to:** anti-grid/conflict tests and typed+flat diagnostics assertions
```python
    result = strategy.fuse(FusionInput(maps=(first, second)))

    assert strategy.name == "provenance-preserving"
    assert result.status is FusionStatus.FUSED
    assert len(first) == 1
    assert len(second) == 1
    assert len(result.fused_map) == 2
    assert [splat.provenance for splat in result.fused_map.splats] == ["front", "rear"]
```

## No Analog Found

No files lack analogs. Phase 04 modifies existing code paths with strong local precedents.

| File | Role | Data Flow | Reason |
|------|------|-----------|--------|

## Metadata

**Analog search scope:** `/home/prannayag/pragnition/robotics/mosaic/src/mosaic`, `/home/prannayag/pragnition/robotics/mosaic/tests`, `/home/prannayag/pragnition/robotics/mosaic/README.md`
**Files scanned:** 56 source/test/docs files listed; 17 analog files read directly
**Project instructions read:** `/home/prannayag/pragnition/robotics/mosaic/CLAUDE.md`
**Project skills:** checked `/home/prannayag/pragnition/robotics/mosaic/.claude` and `/home/prannayag/pragnition/robotics/mosaic/.agents`; no project skills found
**Pattern extraction date:** 2026-05-19
