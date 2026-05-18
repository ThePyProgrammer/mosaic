# Posterior-Aware Splat Fusion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a posterior-aware fusion seam for combining splat-map snapshots without baking in occupancy-union assumptions.

**Architecture:** Fusion is modeled as a protocol over immutable `SplatMap` snapshots that returns a new map plus provenance-rich diagnostics. The first implementation provides deterministic reference strategies that validate frame compatibility, preserve source provenance, and keep uncertainty fields explicit without attempting real Gaussian optimization.

**Tech Stack:** Python 3.12, `dataclasses`, `typing.Protocol`, `enum.StrEnum`, `pytest`, `uv`.

---

## Prerequisite

Complete these plans first:

1. `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`
2. `docs/superpowers/plans/2026-05-18-platform-camera-rig-layer.md`

This plan assumes `mosaic.splats` exports `GaussianSplat` and `SplatMap`, and `mosaic.core` exports `FrameId`.

## File Structure

Create or modify these files:

```text
src/mosaic/fusion/__init__.py              # Public fusion exports
src/mosaic/fusion/protocol.py              # Fusion input/result/protocol contracts
src/mosaic/fusion/strategies.py            # Deterministic reference fusion strategies
src/mosaic/__init__.py                     # Root-level exports for stable fusion API
tests/fusion/test_fusion_protocol.py       # Fusion result and input validation tests
tests/fusion/test_strategies.py            # Reference strategy behavior tests
tests/test_public_api.py                   # Add root fusion export expectations
```

Run all commands from:

```bash
cd /home/prannayag/pragnition/robotics/mosaic
```

---

### Task 1: Add Fusion Protocol Contracts

**Files:**
- Create: `src/mosaic/fusion/__init__.py`
- Create: `src/mosaic/fusion/protocol.py`
- Create: `tests/fusion/test_fusion_protocol.py`

- [ ] **Step 1: Write failing fusion protocol tests**

Create `tests/fusion/test_fusion_protocol.py`:

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


def test_fusion_input_requires_at_least_one_map() -> None:
    with pytest.raises(ValueError, match="at least one"):
        FusionInput(maps=())


def test_fusion_input_requires_matching_frames() -> None:
    with pytest.raises(ValueError, match="same frame"):
        FusionInput(maps=(_map("map"), _map("other")))


def test_fusion_input_exposes_common_frame() -> None:
    fusion_input = FusionInput(maps=(_map("map"), _map("map")))

    assert fusion_input.frame == FrameId("map")


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

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
uv run pytest tests/fusion/test_fusion_protocol.py -q
```

Expected: FAIL with `ModuleNotFoundError: No module named 'mosaic.fusion'`.

- [ ] **Step 3: Implement fusion protocol contracts**

Create `src/mosaic/fusion/protocol.py`:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Mapping, Protocol, runtime_checkable

from mosaic.core import FrameId
from mosaic.splats import SplatMap

FusionMetricValue = bool | int | float | str


class FusionStatus(StrEnum):
    FUSED = "fused"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class FusionInput:
    maps: tuple[SplatMap, ...]

    def __post_init__(self) -> None:
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


@runtime_checkable
class SplatFusionStrategy(Protocol):
    @property
    def name(self) -> str:
        raise NotImplementedError

    def fuse(self, fusion_input: FusionInput) -> FusionResult:
        raise NotImplementedError
```

- [ ] **Step 4: Export fusion protocol contracts**

Create `src/mosaic/fusion/__init__.py`:

```python
from mosaic.fusion.protocol import FusionInput, FusionResult, FusionStatus, SplatFusionStrategy

__all__ = [
    "FusionInput",
    "FusionResult",
    "FusionStatus",
    "SplatFusionStrategy",
]
```

- [ ] **Step 5: Run protocol tests to verify they pass**

Run:

```bash
uv run pytest tests/fusion/test_fusion_protocol.py -q
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/mosaic/fusion tests/fusion/test_fusion_protocol.py
git commit -m "feat: add splat fusion protocol"
```

---

### Task 2: Add Deterministic Provenance-Preserving Fusion Strategy

**Files:**
- Create: `src/mosaic/fusion/strategies.py`
- Modify: `src/mosaic/fusion/__init__.py`
- Create: `tests/fusion/test_strategies.py`

- [ ] **Step 1: Write failing strategy tests**

Create `tests/fusion/test_strategies.py`:

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

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
uv run pytest tests/fusion/test_strategies.py -q
```

Expected: FAIL with import error for `ProvenancePreservingFusion`.

- [ ] **Step 3: Implement deterministic fusion strategy**

Create `src/mosaic/fusion/strategies.py`:

```python
from __future__ import annotations

from dataclasses import dataclass

from mosaic.fusion.protocol import FusionInput, FusionResult, FusionStatus
from mosaic.splats import GaussianSplat, SplatMap


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

- [ ] **Step 4: Export strategy**

Replace `src/mosaic/fusion/__init__.py` with:

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

- [ ] **Step 5: Run strategy tests to verify they pass**

Run:

```bash
uv run pytest tests/fusion/test_strategies.py -q
```

Expected: PASS.

- [ ] **Step 6: Run all fusion tests**

Run:

```bash
uv run pytest tests/fusion -q
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/mosaic/fusion/strategies.py src/mosaic/fusion/__init__.py tests/fusion/test_strategies.py
git commit -m "feat: add provenance preserving splat fusion"
```

---

### Task 3: Publish Fusion API at Package Root

**Files:**
- Modify: `src/mosaic/__init__.py`
- Modify: `tests/test_public_api.py`

- [ ] **Step 1: Extend public API test**

Replace `tests/test_public_api.py` with:

```python
from mosaic import (
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
    SplatMap,
    Timestamp,
    TrackingState,
    quadruped_front_rig,
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
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
uv run pytest tests/test_public_api.py -q
```

Expected: FAIL with import errors for `FusionInput` or `ProvenancePreservingFusion` from `mosaic`.

- [ ] **Step 3: Export fusion API from package root**

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
    "MultiViewObservation",
    "MultiViewSequence",
    "Pixel",
    "PlatformDescription",
    "PlatformRegistry",
    "Pose3",
    "ProvenancePreservingFusion",
    "Quaternion",
    "SplatFusionStrategy",
    "SplatMap",
    "SplatSlamBackend",
    "SplatSlamUpdate",
    "Timestamp",
    "TrackingState",
    "Translation3",
    "__version__",
    "default_platform_registry",
    "humanoid_stereo_rig",
    "quadruped_front_rig",
    "ugv_surround_rig",
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
git commit -m "feat: expose splat fusion api"
```

---

## Final Verification

- [ ] **Step 1: Run the complete suite**

```bash
uv run pytest -q
```

Expected: PASS for all tests.

- [ ] **Step 2: Confirm fusion imports**

Run:

```bash
uv run python -c "from mosaic.fusion import ProvenancePreservingFusion; print(ProvenancePreservingFusion().name)"
```

Expected output:

```text
provenance-preserving
```

- [ ] **Step 3: Inspect working tree**

```bash
git status --short
```

Expected: no uncommitted source or test changes except plan/spec documents that the user has chosen not to commit.

---

## Self-Review Notes

- Spec coverage: This plan creates the posterior-aware fusion seam from the migration plan and avoids Argus's union-merge behavior by explicitly naming the reference strategy `ProvenancePreservingFusion` and reporting `preserved-not-optimized` uncertainty.
- Deferred scope: No real registration, Gaussian optimization, cross-frame alignment, evaluation harness, or agent posterior API is included.
- Type consistency: `FusionInput`, `FusionResult`, `FusionStatus`, `SplatFusionStrategy`, and `ProvenancePreservingFusion` names are consistent across tests, exports, and implementation steps.
