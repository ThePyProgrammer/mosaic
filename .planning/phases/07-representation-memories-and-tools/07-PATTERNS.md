# Phase 7: Representation Memories and Tools - Pattern Map

**Mapped:** 2026-05-21
**Files analyzed:** 7 new/modified files
**Analogs found:** 7 / 7

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `src/mosaic/agents/memory.py` | model / utility | transform, request-response | `src/mosaic/agents/queries.py` + `src/mosaic/agents/posteriors.py` | exact |
| `src/mosaic/agents/__init__.py` | config / public export barrel | request-response | `src/mosaic/agents/__init__.py` | exact |
| `src/mosaic/__init__.py` | config / root public export barrel | request-response | `src/mosaic/__init__.py` | role-match |
| `tests/agents/test_representation_memory.py` | test | request-response, transform | `tests/agents/test_queries.py` | exact |
| `tests/agents/test_representation_claims.py` | test | transform | `tests/agents/test_queries.py` + `src/mosaic/core/frames.py` | role-match |
| `tests/evaluation/test_representation_scenarios.py` | test | batch, request-response | `tests/evaluation/test_scenarios.py` + `tests/evaluation/test_runner.py` | exact |
| `README.md` | documentation | transform | `CLAUDE.md` project boundary text | partial |

## Pattern Assignments

### `src/mosaic/agents/memory.py` (model / utility, transform + request-response)

**Analog:** `src/mosaic/agents/queries.py`

**Imports pattern** (lines 1-6):
```python
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Mapping
```

**Enum and frozen dataclass pattern** (lines 9-26):
```python
class AgentQueryKind(StrEnum):
    LOCAL_GEOMETRY = "local_geometry"
    SCENE_SUMMARY = "scene_summary"
    PROVENANCE = "provenance"


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

**Bounded result pattern** (lines 28-35):
```python
@dataclass(frozen=True, slots=True)
class SplatQueryResult:
    query_kind: AgentQueryKind
    splat_ids: tuple[int, ...]

    @property
    def count(self) -> int:
        return len(self.splat_ids)
```

**Validation and mapping freeze pattern** (lines 38-63):
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

**Analog:** `src/mosaic/agents/posteriors.py`

**Named deterministic query methods on aggregate/view object** (lines 10-40):
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

**Analog:** `src/mosaic/core/frames.py`

**Typed ID and deterministic timestamp pattern** (lines 7-34):
```python
@dataclass(frozen=True, order=True, slots=True)
class Timestamp:
    nanoseconds: int

    def __post_init__(self) -> None:
        if self.nanoseconds < 0:
            raise ValueError("Timestamp nanoseconds must be non-negative")

    @classmethod
    def from_seconds(cls, seconds: float) -> Self:
        if seconds < 0.0:
            raise ValueError("Timestamp seconds must be non-negative")
        return cls(round(seconds * 1_000_000_000))

    def as_seconds(self) -> float:
        return self.nanoseconds / 1_000_000_000


@dataclass(frozen=True, order=True, slots=True)
class FrameId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("FrameId value must not be blank")

    def __str__(self) -> str:
        return self.value
```

**Analog:** `src/mosaic/splats/maps.py`

**Immutable snapshot update pattern** (lines 10-19):
```python
@dataclass(frozen=True, slots=True)
class SplatMap:
    frame: FrameId
    splats: tuple[GaussianSplat, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "splats", tuple(self.splats))

    def with_splats(self, splats: Iterable[GaussianSplat]) -> Self:
        return type(self)(frame=self.frame, splats=self.splats + tuple(splats))
```

**Apply to Phase 7:**
- Define `RepresentationMemory` as frozen/slotted aggregate with five frozen memory-family fields.
- Define typed IDs (`EntityId`, `ClaimId`, `EvidenceId`, `CommitmentId`, etc.) like `FrameId`.
- Define public kinds/statuses with `StrEnum` like `AgentQueryKind`.
- Validate nonblank IDs, finite confidence in `[0, 1]`, positive `max_results`, valid time windows, nonnegative resolution, and `total_matches >= len(items)` in `__post_init__()`.
- Freeze tuple/mapping fields in `__post_init__()` using tuple conversion and `MappingProxyType(dict(...))`.
- Implement `with_*` helpers by constructing a new aggregate snapshot, never mutating existing memory.
- Put named query methods directly on `RepresentationMemory`, following `query_local()`, `summary()`, and `provenance()` style; do not add a separate facade or generic `query()` dispatcher.

---

### `src/mosaic/agents/__init__.py` (config / public export barrel, request-response)

**Analog:** `src/mosaic/agents/__init__.py`

**Import/export barrel pattern** (lines 1-17):
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

**Apply to Phase 7:**
- Import stable Phase 7 public symbols explicitly from `mosaic.agents.memory`.
- Add each imported symbol to `__all__` by exact string name.
- Do not wildcard-import the memory module.
- Prefer exporting Phase 7 symbols from `mosaic.agents` first; root exports are optional and should be stable-only.

---

### `src/mosaic/__init__.py` (config / root public export barrel, request-response)

**Analog:** `src/mosaic/__init__.py`

**Root public API import style** (lines 1-49):
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
```

**Root version and `__all__` pattern** (lines 50-104):
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

**Apply to Phase 7:**
- Only add root exports if the plan decides Phase 7 contracts are stable root-level API.
- If root-exporting, import from `mosaic.agents` and add exact names to `__all__`.
- Keep `__version__` unchanged.

---

### `tests/agents/test_representation_memory.py` (test, request-response + transform)

**Analog:** `tests/agents/test_queries.py`

**Validation and exact assertion pattern** (lines 1-21):
```python
import pytest

from mosaic.agents import AgentQueryKind, LocalRadiusQuery, PosteriorSummary, ProvenanceSummary, SplatQueryResult


def test_local_radius_query_requires_positive_radius() -> None:
    with pytest.raises(ValueError, match="radius"):
        LocalRadiusQuery(center=(0.0, 0.0, 0.0), radius=0.0)


def test_local_radius_query_defaults_to_local_geometry_kind() -> None:
    query = LocalRadiusQuery(center=(1.0, 2.0, 3.0), radius=2.5)

    assert query.kind is AgentQueryKind.LOCAL_GEOMETRY
    assert query.center == (1.0, 2.0, 3.0)


def test_splat_query_result_reports_count() -> None:
    result = SplatQueryResult(query_kind=AgentQueryKind.LOCAL_GEOMETRY, splat_ids=(0, 2, 4))

    assert result.count == 3
```

**Mapping immutability test pattern** (lines 24-34):
```python
def test_posterior_summary_rejects_negative_counts() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        PosteriorSummary(splat_count=-1, provenance_count=0, mean_opacity=0.0)


def test_provenance_summary_freezes_counts() -> None:
    summary = ProvenanceSummary(counts={"front": 2})

    assert summary.counts["front"] == 2
    with pytest.raises(TypeError):
        summary.counts["rear"] = 1
```

**Apply to Phase 7:**
- Test every public memory-family dataclass with direct constructor assertions.
- Use `pytest.raises(ValueError, match="...")` for invalid IDs, bounds, confidence, timestamps, and collection invariants.
- Test aggregate immutable update helpers by asserting original and updated snapshots differ while original fields remain unchanged.
- Test bounded query results with exact `items`, `total_matches`, and `truncated` assertions.
- Test frozen mappings by mutating via index and expecting `TypeError`.

---

### `tests/agents/test_representation_claims.py` (test, transform)

**Analog:** `src/mosaic/core/frames.py` + `tests/agents/test_queries.py`

**Timestamp/ID validation source** (`src/mosaic/core/frames.py` lines 7-34):
```python
@dataclass(frozen=True, order=True, slots=True)
class Timestamp:
    nanoseconds: int

    def __post_init__(self) -> None:
        if self.nanoseconds < 0:
            raise ValueError("Timestamp nanoseconds must be non-negative")


@dataclass(frozen=True, order=True, slots=True)
class FrameId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("FrameId value must not be blank")
```

**Claim tests should copy existing pytest style** (`tests/agents/test_queries.py` lines 6-8):
```python
def test_local_radius_query_requires_positive_radius() -> None:
    with pytest.raises(ValueError, match="radius"):
        LocalRadiusQuery(center=(0.0, 0.0, 0.0), radius=0.0)
```

**Apply to Phase 7:**
- Use explicit `Timestamp(...)` values for created/observed/valid-until times; never use wall-clock time.
- Test `confidence` rejects values below 0 and above 1.
- Test stale transition helper with supplied `now: Timestamp` and exact status changes.
- Test contradiction handling by asserting both claims remain present and both expose conflict links/status; do not assert a winner.
- Test `EvidenceReference` remains opaque by constructing URI/string values without dereference/load behavior.

---

### `tests/evaluation/test_representation_scenarios.py` (test, batch + request-response)

**Analog:** `tests/evaluation/test_scenarios.py`

**Deterministic scenario assertions** (lines 1-19):
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

**Analog:** `tests/evaluation/test_runner.py`

**Artifact/result exact assertion pattern** (lines 9-18):
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

**Apply to Phase 7:**
- Add three equal deterministic scenario anchors: blocked path, search frontier, task allocation.
- Keep scenario fixtures local/private to tests unless the planner decides they become public evaluation helpers.
- Assert exact query outputs, conflict IDs, stale statuses, frontier/traversability rows, commitment conflicts, and ablation behavior.
- For ARNA-style ablations, assert capability blocked/degraded by missing required memory family; do not assert numeric ARNA performance or runtime benchmark claims.

---

### `README.md` (documentation, transform)

**Analog:** project boundary text from `CLAUDE.md` and Phase 7 context.

**Boundary language to preserve:**
- Mosaic is a typed, headless Python library for 3D Gaussian Splatting SLAM and agent-facing representation APIs.
- Agent APIs return bounded typed outputs with evidence/provenance, not raw full splat maps or provider-specific prompts.
- Phase 7 representation memories/tools are deterministic Python contracts, not LLM/LVLM providers, ROS/Habitat, robot execution, real object detection, real splat-to-raster extraction, persistent storage, or distributed synchronization.

**Apply to Phase 7:**
- If updating README, add a concise public boundary note only.
- Do not document deferred integrations as implemented features.
- Do not introduce installation or runtime dependency claims beyond current project config.

## Shared Patterns

### Frozen dataclasses and validation
**Source:** `src/mosaic/agents/queries.py` lines 15-26, 38-63; `src/mosaic/core/frames.py` lines 7-34
**Apply to:** `src/mosaic/agents/memory.py`, agent tests
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

### String-valued public enums
**Source:** `src/mosaic/agents/queries.py` lines 9-13
**Apply to:** memory family kinds, query families, claim status, evidence kinds, cell state, commitment status
```python
class AgentQueryKind(StrEnum):
    LOCAL_GEOMETRY = "local_geometry"
    SCENE_SUMMARY = "scene_summary"
    PROVENANCE = "provenance"
```

### Immutable snapshots and update helpers
**Source:** `src/mosaic/splats/maps.py` lines 10-19
**Apply to:** `RepresentationMemory.with_*`, family-level `with_*` helpers
```python
@dataclass(frozen=True, slots=True)
class SplatMap:
    frame: FrameId
    splats: tuple[GaussianSplat, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "splats", tuple(self.splats))

    def with_splats(self, splats: Iterable[GaussianSplat]) -> Self:
        return type(self)(frame=self.frame, splats=self.splats + tuple(splats))
```

### Bounded named queries over full-state dumps
**Source:** `src/mosaic/agents/posteriors.py` lines 14-40
**Apply to:** perception/search, navigation/reasoning, coordination/commitment, belief/provenance, memory/context methods on `RepresentationMemory`
```python
def query_local(self, query: LocalRadiusQuery) -> SplatQueryResult:
    splat_ids = tuple(
        index
        for index, splat in enumerate(self.splat_map.splats)
        if dist(query.center, splat.center) <= query.radius
    )
    return SplatQueryResult(query_kind=AgentQueryKind.LOCAL_GEOMETRY, splat_ids=splat_ids)
```

### Frozen mappings for diagnostics/provenance/context
**Source:** `src/mosaic/agents/queries.py` lines 53-63 and `src/mosaic/evaluation/runner.py` lines 17-31
**Apply to:** source metadata, result diagnostics, note metadata, serialized artifact-like records
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

### Evaluation scenario exact assertions
**Source:** `tests/evaluation/test_scenarios.py` lines 4-19; `tests/evaluation/test_runner.py` lines 9-18
**Apply to:** `tests/evaluation/test_representation_scenarios.py`
```python
def test_synthetic_forward_sequence_is_deterministic() -> None:
    first = synthetic_forward_sequence(frame_count=3)
    second = synthetic_forward_sequence(frame_count=3)

    assert first == second
    assert first.name == "synthetic-forward-3"
    assert len(first.sequence) == 3
    assert [observation.timestamp.nanoseconds for observation in first.sequence] == [0, 100_000_000, 200_000_000]
```

### Public API barrels
**Source:** `src/mosaic/agents/__init__.py` lines 1-17; `src/mosaic/__init__.py` lines 1-104
**Apply to:** `src/mosaic/agents/__init__.py`, optional root `src/mosaic/__init__.py`
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

## No Analog Found

No Phase 7 file is completely without an analog. The closest analogs are strong for dataclass/query contracts, immutable snapshots, public exports, and deterministic pytest scenarios. The new domain content itself (five ARNA-informed representation memory families) has no exact existing implementation, so planners should use `07-RESEARCH.md` and Phase 7 decisions for field selection while copying code shape from the analogs above.

| File | Role | Data Flow | Reason |
|------|------|-----------|--------|
| None | — | — | All proposed files have at least role-match analogs. |

## Metadata

**Analog search scope:** `/home/prannayag/pragnition/robotics/.mosaic-worktrees/splat-slam-foundation/src/mosaic`, `/home/prannayag/pragnition/robotics/.mosaic-worktrees/splat-slam-foundation/tests`, main checkout phase files
**Files scanned:** 35 implementation/test paths listed from the worktree; 12 files read for concrete patterns including context/research/project instructions
**Pattern extraction date:** 2026-05-21
**Repository baseline:** Worktree `/home/prannayag/pragnition/robotics/.mosaic-worktrees/splat-slam-foundation` used for implementation analogs; output written to main checkout phase directory.
