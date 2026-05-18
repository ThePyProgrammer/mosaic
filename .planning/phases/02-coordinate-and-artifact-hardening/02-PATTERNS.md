# Phase 02: Coordinate and Artifact Hardening - Pattern Map

**Mapped:** 2026-05-18
**Files analyzed:** 12 new/modified files
**Analogs found:** 12 / 12

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `src/mosaic/core/frames.py` | model | transform | `src/mosaic/core/frames.py` | exact-existing |
| `src/mosaic/core/poses.py` | model | transform | `src/mosaic/core/poses.py` | exact-existing |
| `src/mosaic/core/cameras.py` | model | transform | `src/mosaic/core/cameras.py` | exact-existing |
| `src/mosaic/splats/primitives.py` | model | transform | `src/mosaic/splats/primitives.py` | exact-existing |
| `src/mosaic/artifacts/__init__.py` | config | request-response | `src/mosaic/core/__init__.py` | exact-role |
| `src/mosaic/artifacts/schema.py` | utility | transform | `src/mosaic/evaluation/runner.py` | role-match |
| `tests/core/test_frames_and_poses.py` | test | transform | `tests/core/test_frames_and_poses.py` | exact-existing |
| `tests/core/test_observations.py` | test | transform | `tests/core/test_observations.py` | exact-existing |
| `tests/splats/test_splat_map.py` | test | transform | `tests/splats/test_splat_map.py` | exact-existing |
| `tests/artifacts/test_core_artifacts.py` | test | transform | `tests/core/test_observations.py` | role-match |
| `tests/artifacts/test_splat_artifacts.py` | test | transform | `tests/splats/test_splat_map.py` | role-match |
| `tests/artifacts/test_slam_and_evaluation_artifacts.py` | test | transform | `tests/evaluation/test_runner.py` | role-match |

## Pattern Assignments

### `src/mosaic/core/frames.py` (model, transform)

**Analog:** `src/mosaic/core/frames.py`

**Imports pattern** (lines 1-4):
```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Self
```

**Frozen value-object validation pattern** (lines 7-19):
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
```

**Frame ID validation and string conversion** (lines 25-34):
```python
@dataclass(frozen=True, order=True, slots=True)
class FrameId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("FrameId value must not be blank")

    def __str__(self) -> str:
        return self.value
```

**Apply to Phase 2:** Keep integer nanoseconds as canonical artifact payload; add docstrings/tests rather than changing the storage shape.

---

### `src/mosaic/core/poses.py` (model, transform)

**Analog:** `src/mosaic/core/poses.py`

**Imports pattern** (lines 1-7):
```python
from __future__ import annotations

from dataclasses import dataclass, field
from math import isclose, sqrt
from typing import Self

from mosaic.core.frames import FrameId
```

**Tuple conversion pattern** (lines 10-17):
```python
@dataclass(frozen=True, slots=True)
class Translation3:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def as_tuple(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.z)
```

**Quaternion validation and identity constructor** (lines 20-37):
```python
@dataclass(frozen=True, slots=True)
class Quaternion:
    w: float
    x: float
    y: float
    z: float

    def __post_init__(self) -> None:
        norm = sqrt(self.w * self.w + self.x * self.x + self.y * self.y + self.z * self.z)
        if not isclose(norm, 1.0, rel_tol=1e-6, abs_tol=1e-6):
            raise ValueError("Quaternion must be unit length")

    @classmethod
    def identity(cls) -> Self:
        return cls(w=1.0, x=0.0, y=0.0, z=0.0)

    def as_tuple(self) -> tuple[float, float, float, float]:
        return (self.w, self.x, self.y, self.z)
```

**Pose dataclass shape to extend** (lines 40-45):
```python
@dataclass(frozen=True, slots=True)
class Pose3:
    parent_frame: FrameId
    child_frame: FrameId
    translation: Translation3 = field(default_factory=Translation3)
    rotation: Quaternion = field(default_factory=Quaternion.identity)
```

**Apply to Phase 2:** Add pure-Python `Quaternion` rotation/multiplication helpers and `Pose3.apply_to_point()`, `Pose3.inverse()`, and `Pose3.compose()` on this same frozen dataclass pattern. Reject incompatible frames with `ValueError` before math.

---

### `src/mosaic/core/cameras.py` (model, transform)

**Analog:** `src/mosaic/core/cameras.py`

**Imports pattern** (lines 1-3):
```python
from __future__ import annotations

from dataclasses import dataclass
```

**Intrinsics validation and projection pattern** (lines 12-37):
```python
@dataclass(frozen=True, slots=True)
class CameraIntrinsics:
    width: int
    height: int
    fx: float
    fy: float
    cx: float
    cy: float

    def __post_init__(self) -> None:
        if self.width <= 0:
            raise ValueError("CameraIntrinsics width must be positive")
        if self.height <= 0:
            raise ValueError("CameraIntrinsics height must be positive")
        if self.fx <= 0.0 or self.fy <= 0.0:
            raise ValueError("CameraIntrinsics focal lengths must be positive")
        if not 0.0 <= self.cx <= float(self.width):
            raise ValueError("CameraIntrinsics cx must be within image width")
        if not 0.0 <= self.cy <= float(self.height):
            raise ValueError("CameraIntrinsics cy must be within image height")

    def project(self, point_camera: tuple[float, float, float]) -> Pixel:
        x, y, z = point_camera
        if z <= 0.0:
            raise ValueError("Cannot project point with non-positive depth")
        return Pixel(u=(self.fx * x / z) + self.cx, v=(self.fy * y / z) + self.cy)
```

**Apply to Phase 2:** Document that `project()` accepts camera optical-frame coordinates with positive `z` depth; tests should lock `z-forward/x-right/y-down` behavior without adding ROS dependencies.

---

### `src/mosaic/splats/primitives.py` (model, transform)

**Analog:** `src/mosaic/splats/primitives.py`

**Imports pattern** (lines 1-3):
```python
from __future__ import annotations

from dataclasses import dataclass
```

**Immutable sequence coercion and covariance validation** (lines 6-42):
```python
@dataclass(frozen=True, slots=True)
class GaussianSplat:
    center: tuple[float, float, float]
    covariance_upper: tuple[float, float, float, float, float, float]
    color_rgb: tuple[float, float, float] = (1.0, 1.0, 1.0)
    opacity: float = 1.0
    provenance: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "center", tuple(self.center))
        object.__setattr__(self, "covariance_upper", tuple(self.covariance_upper))
        object.__setattr__(self, "color_rgb", tuple(self.color_rgb))

        if len(self.center) != 3:
            raise ValueError("GaussianSplat center must contain three coordinates")
        if len(self.covariance_upper) != 6:
            raise ValueError("GaussianSplat covariance_upper must contain six values")
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
```

**Apply to Phase 2:** Treat the unpacking order as the public contract: `(xx, xy, xz, yy, yz, zz)`. Add edge tests for tuple length, upper-triangular reconstruction, zero determinant, negative determinant, and invalid off-diagonal values.

---

### `src/mosaic/artifacts/__init__.py` (config, request-response)

**Analog:** `src/mosaic/core/__init__.py`

**Barrel export pattern** (lines 1-18):
```python
from mosaic.core.cameras import CameraIntrinsics, Pixel
from mosaic.core.frames import FrameId, Timestamp
from mosaic.core.observations import CameraObservation, ImageBuffer, ImageEncoding, MultiViewObservation
from mosaic.core.poses import Pose3, Quaternion, Translation3

__all__ = [
    "CameraIntrinsics",
    "CameraObservation",
    "FrameId",
    "ImageBuffer",
    "ImageEncoding",
    "MultiViewObservation",
    "Pixel",
    "Pose3",
    "Quaternion",
    "Timestamp",
    "Translation3",
]
```

**Apply to Phase 2:** Use package-root imports from `mosaic.*`, list every public artifact helper explicitly in `__all__`, and avoid wildcard imports. Keep `src/mosaic/artifacts/__init__.py` as the stable public surface for v1 artifact helpers.

---

### `src/mosaic/artifacts/schema.py` (utility, transform)

**Analog:** `src/mosaic/evaluation/runner.py`

**Imports for JSON-ready artifacts** (lines 1-8):
```python
from __future__ import annotations

import json
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Sequence
```

**Mapping freeze pattern** (lines 17-31):
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

**JSON-ready dictionary pattern** (lines 34-50):
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

**Stable JSON writer pattern** (lines 68-69):
```python
def write_benchmark_artifact(artifact: BenchmarkArtifact, path: Path) -> None:
    path.write_text(json.dumps(artifact.as_dict(), indent=2, sort_keys=True) + "\n")
```

**Apply to Phase 2:** Implement a small artifact envelope utility around `schema`, `schema_version`, and `payload`; reject unknown schema names/versions with `ValueError`. Use JSON primitives only. For bytes, define an explicit reversible encoding, likely base64, inside the payload.

---

### `tests/core/test_frames_and_poses.py` (test, transform)

**Analog:** `tests/core/test_frames_and_poses.py`

**Imports pattern** (lines 1-3):
```python
import pytest

from mosaic.core import FrameId, Pose3, Quaternion, Timestamp, Translation3
```

**Timestamp precision assertion pattern** (lines 6-10):
```python
def test_timestamp_from_seconds_uses_nanoseconds() -> None:
    timestamp = Timestamp.from_seconds(1.25)

    assert timestamp.nanoseconds == 1_250_000_000
    assert timestamp.as_seconds() == 1.25
```

**Exception assertion pattern** (lines 13-20):
```python
def test_timestamp_rejects_negative_values() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        Timestamp(-1)


def test_frame_id_rejects_blank_values() -> None:
    with pytest.raises(ValueError, match="FrameId"):
        FrameId("  ")
```

**Pose constructor pattern** (lines 23-34):
```python
def test_pose_tracks_parent_and_child_frames() -> None:
    pose = Pose3(
        parent_frame=FrameId("world"),
        child_frame=FrameId("camera/front"),
        translation=Translation3(1.0, 2.0, 3.0),
        rotation=Quaternion.identity(),
    )

    assert pose.parent_frame == FrameId("world")
    assert pose.child_frame == FrameId("camera/front")
    assert pose.translation.as_tuple() == (1.0, 2.0, 3.0)
    assert pose.rotation.as_tuple() == (1.0, 0.0, 0.0, 0.0)
```

**Apply to Phase 2:** Add tests for `Pose3` as `T_parent_child`: `apply_to_point()`, `inverse()`, `compose()`, frame mismatch failure, and at least one non-identity rotation case.

---

### `tests/core/test_observations.py` (test, transform)

**Analog:** `tests/core/test_observations.py`

**Import grouping pattern** (lines 1-14):
```python
import pytest

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
```

**Private helper factory pattern** (lines 17-37):
```python
def _pose(camera_frame: str) -> Pose3:
    return Pose3(
        parent_frame=FrameId("world"),
        child_frame=FrameId(camera_frame),
        translation=Translation3(),
        rotation=Quaternion.identity(),
    )


def _intrinsics() -> CameraIntrinsics:
    return CameraIntrinsics(width=640, height=480, fx=400.0, fy=401.0, cx=320.0, cy=240.0)


def _rgb(width: int = 2, height: int = 1) -> ImageBuffer:
    return ImageBuffer(
        width=width,
        height=height,
        channels=3,
        encoding=ImageEncoding.RGB8,
        data=b"\x00\x00\x00\xff\xff\xff",
    )
```

**Projection and validation tests** (lines 40-49):
```python
def test_camera_intrinsics_project_point() -> None:
    pixel = _intrinsics().project((1.0, 2.0, 4.0))

    assert pixel.u == 420.0
    assert pixel.v == 440.5


def test_camera_intrinsics_rejects_non_positive_depth_projection() -> None:
    with pytest.raises(ValueError, match="non-positive depth"):
        _intrinsics().project((0.0, 0.0, 0.0))
```

**Apply to Phase 2:** Extend with optical-frame convention tests. Prefer `_pose()`, `_intrinsics()`, and `_rgb()` helper factories over repeated large constructors.

---

### `tests/splats/test_splat_map.py` (test, transform)

**Analog:** `tests/splats/test_splat_map.py`

**Imports pattern** (lines 1-4):
```python
import pytest

from mosaic.core import FrameId
from mosaic.splats import GaussianSplat, SplatMap
```

**Valid covariance fixture pattern** (lines 7-18):
```python
def test_gaussian_splat_accepts_valid_upper_triangular_covariance() -> None:
    splat = GaussianSplat(
        center=(1.0, 2.0, 3.0),
        covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1),
        color_rgb=(0.2, 0.3, 0.4),
        opacity=0.75,
        provenance="front-camera",
    )

    assert splat.center == (1.0, 2.0, 3.0)
    assert splat.provenance == "front-camera"
```

**Negative validation test pattern** (lines 29-31, 53-58):
```python
def test_gaussian_splat_rejects_non_positive_covariance_diagonal() -> None:
    with pytest.raises(ValueError, match="covariance diagonal"):
        GaussianSplat(center=(0.0, 0.0, 0.0), covariance_upper=(0.0, 0.0, 0.0, 0.1, 0.0, 0.1))


def test_gaussian_splat_rejects_non_positive_definite_covariance() -> None:
    with pytest.raises(ValueError, match="positive definite"):
        GaussianSplat(
            center=(0.0, 0.0, 0.0),
            covariance_upper=(1.0, 2.0, 0.0, 1.0, 0.0, 1.0),
        )
```

**Immutable map update pattern** (lines 61-71):
```python
def test_splat_map_appends_without_mutating_original() -> None:
    frame = FrameId("map")
    base = SplatMap(frame=frame)
    splat = GaussianSplat(center=(0.0, 0.0, 1.0), covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1))

    updated = base.with_splats((splat,))

    assert len(base) == 0
    assert len(updated) == 1
    assert updated.frame == frame
    assert updated.splats == (splat,)
```

**Apply to Phase 2:** Add covariance layout tests that reconstruct the symmetric matrix from `(xx, xy, xz, yy, yz, zz)` and assert invalid off-diagonal/determinant cases fail.

---

### `tests/artifacts/test_core_artifacts.py` (test, transform)

**Analog:** `tests/core/test_observations.py`

**Use these imports and helper style** (lines 1-14, 17-37):
```python
import pytest

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
```

```python
def _pose(camera_frame: str) -> Pose3:
    return Pose3(
        parent_frame=FrameId("world"),
        child_frame=FrameId(camera_frame),
        translation=Translation3(),
        rotation=Quaternion.identity(),
    )
```

**Apply to Phase 2:** Create round-trip tests for `Timestamp`, `FrameId`, `Translation3`, `Quaternion`, `Pose3`, `CameraIntrinsics`, `ImageBuffer`, `CameraObservation`, and `MultiViewObservation`. Assert artifact envelopes contain `schema`, `schema_version`, and `payload`; use `pytest.raises(ValueError, match=...)` for unknown schema/version.

---

### `tests/artifacts/test_splat_artifacts.py` (test, transform)

**Analog:** `tests/splats/test_splat_map.py`

**Use splat fixture and immutable expectations** (lines 7-18, 61-71):
```python
def test_gaussian_splat_accepts_valid_upper_triangular_covariance() -> None:
    splat = GaussianSplat(
        center=(1.0, 2.0, 3.0),
        covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1),
        color_rgb=(0.2, 0.3, 0.4),
        opacity=0.75,
        provenance="front-camera",
    )

    assert splat.center == (1.0, 2.0, 3.0)
    assert splat.provenance == "front-camera"
```

```python
def test_splat_map_appends_without_mutating_original() -> None:
    frame = FrameId("map")
    base = SplatMap(frame=frame)
    splat = GaussianSplat(center=(0.0, 0.0, 1.0), covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1))

    updated = base.with_splats((splat,))

    assert len(base) == 0
    assert len(updated) == 1
    assert updated.frame == frame
    assert updated.splats == (splat,)
```

**Apply to Phase 2:** Round-trip `GaussianSplat` and `SplatMap` artifacts. Assert covariance payload preserves exact tuple order, not just equivalent diagonal values.

---

### `tests/artifacts/test_slam_and_evaluation_artifacts.py` (test, transform)

**Analog:** `tests/evaluation/test_runner.py`

**Benchmark artifact JSON-ready pattern** (lines 21-34):
```python
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
```

**Stable JSON writer assertion pattern** (lines 52-64):
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

**SplatSlamUpdate validation source** (`src/mosaic/slam/protocol.py` lines 34-45):
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

**Apply to Phase 2:** Round-trip `SplatSlamUpdate`, `MetricResult`, and `RegressionResult`. Add a test proving `BenchmarkArtifact.as_dict()` remains the existing narrow evaluation artifact and is not itself the general v1 artifact envelope.

## Shared Patterns

### Package imports and public surfaces
**Source:** `src/mosaic/core/__init__.py` lines 1-18 and `src/mosaic/__init__.py` lines 52-104
**Apply to:** `src/mosaic/artifacts/__init__.py`, any artifact helper modules, new tests
```python
from mosaic.core.cameras import CameraIntrinsics, Pixel
from mosaic.core.frames import FrameId, Timestamp
from mosaic.core.observations import CameraObservation, ImageBuffer, ImageEncoding, MultiViewObservation
from mosaic.core.poses import Pose3, Quaternion, Translation3

__all__ = [
    "CameraIntrinsics",
    "CameraObservation",
    "FrameId",
    "ImageBuffer",
    "ImageEncoding",
    "MultiViewObservation",
    "Pixel",
    "Pose3",
    "Quaternion",
    "Timestamp",
    "Translation3",
]
```

### Dataclass invariants
**Source:** `src/mosaic/core/frames.py` lines 7-19; `src/mosaic/splats/primitives.py` lines 14-42
**Apply to:** all modified models and artifact schema helper dataclasses
```python
@dataclass(frozen=True, order=True, slots=True)
class Timestamp:
    nanoseconds: int

    def __post_init__(self) -> None:
        if self.nanoseconds < 0:
            raise ValueError("Timestamp nanoseconds must be non-negative")
```

### Immutable tuple/mapping freeze
**Source:** `src/mosaic/core/observations.py` lines 26-41, 54-59; `src/mosaic/evaluation/runner.py` lines 17-31
**Apply to:** image payload handling, diagnostics payload handling, artifact payload copies
```python
object.__setattr__(self, "data", bytes(self.data))
```

```python
object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))
```

```python
self._metrics = tuple(MappingProxyType(dict(metric)) for metric in metrics)
```

### JSON-ready serialization
**Source:** `src/mosaic/evaluation/runner.py` lines 44-50 and 68-69
**Apply to:** artifact envelope payload conversion and artifact file-writing tests
```python
def as_dict(self) -> dict[str, str | int | list[MetricDict]]:
    return {
        "scenario_name": self.scenario_name,
        "backend_name": self.backend_name,
        "update_count": self.update_count,
        "metrics": [dict(metric) for metric in self.metrics],
    }
```

```python
def write_benchmark_artifact(artifact: BenchmarkArtifact, path: Path) -> None:
    path.write_text(json.dumps(artifact.as_dict(), indent=2, sort_keys=True) + "\n")
```

### Pytest validation style
**Source:** `tests/core/test_frames_and_poses.py` lines 13-20; `tests/splats/test_splat_map.py` lines 53-58
**Apply to:** all new negative tests for transforms, covariance, and artifact schema validation
```python
def test_timestamp_rejects_negative_values() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        Timestamp(-1)
```

```python
def test_gaussian_splat_rejects_non_positive_definite_covariance() -> None:
    with pytest.raises(ValueError, match="positive definite"):
        GaussianSplat(
            center=(0.0, 0.0, 0.0),
            covariance_upper=(1.0, 2.0, 0.0, 1.0, 0.0, 1.0),
        )
```

### Test helper factories
**Source:** `tests/core/test_observations.py` lines 17-37 and `tests/slam/test_backend_contract.py` lines 16-34
**Apply to:** `tests/artifacts/*`, extended transform tests
```python
def _pose(camera_frame: str) -> Pose3:
    return Pose3(
        parent_frame=FrameId("world"),
        child_frame=FrameId(camera_frame),
        translation=Translation3(),
        rotation=Quaternion.identity(),
    )
```

## No Analog Found

All Phase 2 files have close in-repository analogs. The new `mosaic.artifacts` package has no exact serializer package predecessor, but its implementation should combine the existing barrel-export, frozen dataclass, explicit `as_dict()`, mapping-freeze, and deterministic JSON patterns listed above.

| File | Role | Data Flow | Reason |
|------|------|-----------|--------|
| none | — | — | Every new/modified file has an exact or role-match analog. |

## Metadata

**Analog search scope:** `/home/prannayag/pragnition/robotics/mosaic/src/mosaic`, `/home/prannayag/pragnition/robotics/mosaic/tests`
**Files scanned:** 37 Python files listed under source and tests
**Strong analogs read:** 18 files from `src/mosaic` and `tests`
**Pattern extraction date:** 2026-05-18
