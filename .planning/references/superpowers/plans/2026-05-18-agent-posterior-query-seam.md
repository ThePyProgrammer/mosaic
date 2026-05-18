# Agent Posterior Query Seam Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a thin, stable agent-facing API for querying splat-map posterior snapshots without freezing the final agent-friendly representation research model.

**Architecture:** The `agents` namespace wraps existing `SplatMap` snapshots in typed query requests and deterministic response objects. It exposes local spatial queries, scene summaries, uncertainty summaries, and provenance summaries while deliberately avoiding LLM provider integration or natural-language reasoning.

**Tech Stack:** Python 3.12, `dataclasses`, `enum.StrEnum`, `pytest`, `uv`.

---

## Prerequisite

Complete these plans first:

1. `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`
2. `docs/superpowers/plans/2026-05-18-platform-camera-rig-layer.md`
3. `docs/superpowers/plans/2026-05-18-posterior-aware-splat-fusion.md`
4. `docs/superpowers/plans/2026-05-18-evaluation-regression-harness.md`

This plan assumes `mosaic.splats.GaussianSplat` and `mosaic.splats.SplatMap` exist.

## File Structure

Create or modify these files:

```text
src/mosaic/agents/__init__.py              # Public agent API exports
src/mosaic/agents/queries.py               # Query request and response contracts
src/mosaic/agents/posteriors.py            # Splat posterior view implementation
src/mosaic/__init__.py                     # Root-level exports for stable agent API
tests/agents/test_queries.py               # Query contract tests
tests/agents/test_splat_posterior.py       # Posterior query behavior tests
tests/test_public_api.py                   # Add root agent export expectations
```

Run all commands from:

```bash
cd /home/prannayag/pragnition/robotics/mosaic
```

---

### Task 1: Add Agent Query Contracts

**Files:**
- Create: `src/mosaic/agents/__init__.py`
- Create: `src/mosaic/agents/queries.py`
- Create: `tests/agents/test_queries.py`

- [ ] **Step 1: Write failing query contract tests**

Create `tests/agents/test_queries.py`:

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


def test_posterior_summary_rejects_negative_counts() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        PosteriorSummary(splat_count=-1, provenance_count=0, mean_opacity=0.0)


def test_provenance_summary_freezes_counts() -> None:
    summary = ProvenanceSummary(counts={"front": 2})

    assert summary.counts["front"] == 2
    with pytest.raises(TypeError):
        summary.counts["rear"] = 1
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
uv run pytest tests/agents/test_queries.py -q
```

Expected: FAIL with `ModuleNotFoundError: No module named 'mosaic.agents'`.

- [ ] **Step 3: Implement query contracts**

Create `src/mosaic/agents/queries.py`:

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


@dataclass(frozen=True, slots=True)
class SplatQueryResult:
    query_kind: AgentQueryKind
    splat_ids: tuple[int, ...]

    @property
    def count(self) -> int:
        return len(self.splat_ids)


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

- [ ] **Step 4: Export query contracts**

Create `src/mosaic/agents/__init__.py`:

```python
from mosaic.agents.queries import AgentQueryKind, LocalRadiusQuery, PosteriorSummary, ProvenanceSummary, SplatQueryResult

__all__ = [
    "AgentQueryKind",
    "LocalRadiusQuery",
    "PosteriorSummary",
    "ProvenanceSummary",
    "SplatQueryResult",
]
```

- [ ] **Step 5: Run query tests to verify they pass**

Run:

```bash
uv run pytest tests/agents/test_queries.py -q
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/mosaic/agents tests/agents/test_queries.py
git commit -m "feat: add agent posterior query contracts"
```

---

### Task 2: Add Splat Posterior View

**Files:**
- Create: `src/mosaic/agents/posteriors.py`
- Modify: `src/mosaic/agents/__init__.py`
- Create: `tests/agents/test_splat_posterior.py`

- [ ] **Step 1: Write failing posterior view tests**

Create `tests/agents/test_splat_posterior.py`:

```python
from mosaic.agents import LocalRadiusQuery, SplatPosteriorView
from mosaic.core import FrameId
from mosaic.splats import GaussianSplat, SplatMap


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

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
uv run pytest tests/agents/test_splat_posterior.py -q
```

Expected: FAIL with import error for `SplatPosteriorView`.

- [ ] **Step 3: Implement splat posterior view**

Create `src/mosaic/agents/posteriors.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from math import dist

from mosaic.agents.queries import AgentQueryKind, LocalRadiusQuery, PosteriorSummary, ProvenanceSummary, SplatQueryResult
from mosaic.splats import SplatMap


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

- [ ] **Step 4: Export posterior view**

Replace `src/mosaic/agents/__init__.py` with:

```python
from mosaic.agents.posteriors import SplatPosteriorView
from mosaic.agents.queries import AgentQueryKind, LocalRadiusQuery, PosteriorSummary, ProvenanceSummary, SplatQueryResult

__all__ = [
    "AgentQueryKind",
    "LocalRadiusQuery",
    "PosteriorSummary",
    "ProvenanceSummary",
    "SplatPosteriorView",
    "SplatQueryResult",
]
```

- [ ] **Step 5: Run posterior tests to verify they pass**

Run:

```bash
uv run pytest tests/agents/test_splat_posterior.py -q
```

Expected: PASS.

- [ ] **Step 6: Run all agent tests**

Run:

```bash
uv run pytest tests/agents -q
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/mosaic/agents/posteriors.py src/mosaic/agents/__init__.py tests/agents/test_splat_posterior.py
git commit -m "feat: add splat posterior view"
```

---

### Task 3: Publish Agent API at Package Root

**Files:**
- Modify: `src/mosaic/__init__.py`
- Modify: `tests/test_public_api.py`

- [ ] **Step 1: Extend public API test**

Replace `tests/test_public_api.py` with:

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


def test_public_api_exports_agent_types() -> None:
    view = SplatPosteriorView(SplatMap(frame=FrameId("map")))
    query = LocalRadiusQuery(center=(0.0, 0.0, 0.0), radius=1.0)

    assert query.kind is AgentQueryKind.LOCAL_GEOMETRY
    assert view.query_local(query).count == 0
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
uv run pytest tests/test_public_api.py -q
```

Expected: FAIL with import errors for `AgentQueryKind`, `LocalRadiusQuery`, or `SplatPosteriorView` from `mosaic`.

- [ ] **Step 3: Export agent API from package root**

Replace `src/mosaic/__init__.py` with:

```python
from mosaic.agents import AgentQueryKind, LocalRadiusQuery, PosteriorSummary, ProvenanceSummary, SplatPosteriorView, SplatQueryResult
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
    "Pose3",
    "PosteriorSummary",
    "ProvenancePreservingFusion",
    "ProvenanceSummary",
    "Quaternion",
    "RegressionGate",
    "RegressionResult",
    "SplatFusionStrategy",
    "SplatMap",
    "SplatPosteriorView",
    "SplatQueryResult",
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
git commit -m "feat: expose agent posterior api"
```

---

## Final Verification

- [ ] **Step 1: Run the complete suite**

```bash
uv run pytest -q
```

Expected: PASS for all tests.

- [ ] **Step 2: Confirm posterior query behavior**

Run:

```bash
uv run python -c "from mosaic import FrameId, LocalRadiusQuery, SplatMap, SplatPosteriorView; print(SplatPosteriorView(SplatMap(FrameId('map'))).query_local(LocalRadiusQuery((0, 0, 0), 1.0)).count)"
```

Expected output:

```text
0
```

- [ ] **Step 3: Inspect working tree**

```bash
git status --short
```

Expected: no uncommitted source or test changes except plan/spec documents that the user has chosen not to commit.

---

## Self-Review Notes

- Spec coverage: This plan implements the thin agent posterior integration seam from the migration plan through typed local queries, posterior summaries, provenance summaries, and deterministic query behavior over `SplatMap` snapshots.
- Deferred scope: No LLM provider integration, natural-language query parsing, long-horizon memory, semantic scene graph, policy interface, or final agent-friendly representation ontology is included.
- Type consistency: `AgentQueryKind`, `LocalRadiusQuery`, `SplatQueryResult`, `PosteriorSummary`, `ProvenanceSummary`, and `SplatPosteriorView` names are consistent across tasks and tests.
