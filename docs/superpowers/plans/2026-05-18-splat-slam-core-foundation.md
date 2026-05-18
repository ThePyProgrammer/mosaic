# Splat SLAM Core Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build Mosaic's first typed, headless Python foundation for multi-view Gaussian-splatting SLAM: geometry/camera contracts, deterministic replay, splat-map state, and a backend lifecycle protocol.

**Architecture:** Mosaic starts as a small typed package with pure-Python data contracts and no CUDA/backend dependency. The first implementation slice creates stable seams for future splatting backends while using deterministic in-memory tests and a reference backend to validate lifecycle behavior.

**Tech Stack:** Python 3.12, `dataclasses`, `typing.Protocol`, `enum.StrEnum`, `pytest`, `uv`.

---

## Scope

This plan implements the first two milestones from `docs/argus-migration-plan.md`:

1. Foundation: typed geometry and camera contracts.
2. Splat SLAM core.

It does not implement robot platform adapters, map fusion, evaluation benchmarks, UI, WebSocket integration, or agent posterior APIs. Those are separate implementation plans after this core is stable.

## File Structure

Create or modify these files:

```text
pyproject.toml                         # Add pytest/dev test configuration
src/mosaic/__init__.py                 # Public package exports
src/mosaic/core/__init__.py            # Core geometry/camera exports
src/mosaic/core/frames.py              # Frame identifiers and timestamps
src/mosaic/core/poses.py               # Translation, quaternion, pose contracts
src/mosaic/core/cameras.py             # Pinhole camera intrinsics and projection
src/mosaic/core/observations.py        # Image buffers, camera observations, multi-view observations
src/mosaic/datasets/__init__.py        # Dataset exports
src/mosaic/datasets/replay.py          # Deterministic in-memory replay sequence
src/mosaic/splats/__init__.py          # Splat exports
src/mosaic/splats/primitives.py        # Gaussian splat primitive
src/mosaic/splats/maps.py              # Immutable splat-map snapshot container
src/mosaic/slam/__init__.py            # SLAM exports
src/mosaic/slam/protocol.py            # Backend capability, update, and lifecycle protocol
src/mosaic/slam/fake_backend.py        # Deterministic backend for tests and examples
tests/test_package_import.py           # Package import smoke test
tests/core/test_frames_and_poses.py    # Frame, timestamp, pose tests
tests/core/test_observations.py        # Camera/image/multi-view tests
tests/datasets/test_replay.py          # Deterministic replay tests
tests/splats/test_splat_map.py         # Splat primitive and map tests
tests/slam/test_backend_contract.py    # Backend lifecycle contract tests
tests/test_public_api.py               # Top-level export tests
```

Run all commands from:

```bash
cd /home/prannayag/pragnition/robotics/mosaic
```

---

### Task 1: Add pytest Harness and Package Version Surface

**Files:**
- Modify: `pyproject.toml`
- Modify: `src/mosaic/__init__.py`
- Create: `tests/test_package_import.py`

- [ ] **Step 1: Write the failing import test**

Create `tests/test_package_import.py`:

```python
from mosaic import __version__


def test_package_version_is_exposed() -> None:
    assert __version__ == "0.1.0"
```

- [ ] **Step 2: Add test tooling configuration**

Replace `pyproject.toml` with:

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

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]

[build-system]
requires = ["uv_build>=0.10.10,<0.11.0"]
build-backend = "uv_build"
```

- [ ] **Step 3: Run the test to verify it fails for the package API**

Run:

```bash
uv run pytest tests/test_package_import.py -q
```

Expected: FAIL with an import error like `cannot import name '__version__' from 'mosaic'`.

- [ ] **Step 4: Write the minimal package API**

Replace `src/mosaic/__init__.py` with:

```python
__version__ = "0.1.0"

__all__ = ["__version__"]
```

- [ ] **Step 5: Run the test to verify it passes**

Run:

```bash
uv run pytest tests/test_package_import.py -q
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml src/mosaic/__init__.py tests/test_package_import.py
git commit -m "test: add package import smoke test"
```

---

### Task 2: Add Frame, Timestamp, and Pose Contracts

**Files:**
- Create: `src/mosaic/core/__init__.py`
- Create: `src/mosaic/core/frames.py`
- Create: `src/mosaic/core/poses.py`
- Create: `tests/core/test_frames_and_poses.py`

- [ ] **Step 1: Write failing core geometry tests**

Create `tests/core/test_frames_and_poses.py`:

```python
import pytest

from mosaic.core import FrameId, Pose3, Quaternion, Timestamp, Translation3


def test_timestamp_from_seconds_uses_nanoseconds() -> None:
    timestamp = Timestamp.from_seconds(1.25)

    assert timestamp.nanoseconds == 1_250_000_000
    assert timestamp.as_seconds() == 1.25


def test_timestamp_rejects_negative_values() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        Timestamp(-1)


def test_frame_id_rejects_blank_values() -> None:
    with pytest.raises(ValueError, match="FrameId"):
        FrameId("  ")


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


def test_quaternion_rejects_non_unit_rotation() -> None:
    with pytest.raises(ValueError, match="unit length"):
        Quaternion(w=2.0, x=0.0, y=0.0, z=0.0)
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
uv run pytest tests/core/test_frames_and_poses.py -q
```

Expected: FAIL with `ModuleNotFoundError: No module named 'mosaic.core'`.

- [ ] **Step 3: Implement frame and timestamp contracts**

Create `src/mosaic/core/frames.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Self


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

- [ ] **Step 4: Implement pose contracts**

Create `src/mosaic/core/poses.py`:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from math import isclose, sqrt
from typing import Self

from mosaic.core.frames import FrameId


@dataclass(frozen=True, slots=True)
class Translation3:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def as_tuple(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.z)


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


@dataclass(frozen=True, slots=True)
class Pose3:
    parent_frame: FrameId
    child_frame: FrameId
    translation: Translation3 = field(default_factory=Translation3)
    rotation: Quaternion = field(default_factory=Quaternion.identity)
```

- [ ] **Step 5: Export core contracts**

Create `src/mosaic/core/__init__.py`:

```python
from mosaic.core.frames import FrameId, Timestamp
from mosaic.core.poses import Pose3, Quaternion, Translation3

__all__ = [
    "FrameId",
    "Pose3",
    "Quaternion",
    "Timestamp",
    "Translation3",
]
```

- [ ] **Step 6: Run tests to verify they pass**

Run:

```bash
uv run pytest tests/core/test_frames_and_poses.py -q
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/mosaic/core tests/core/test_frames_and_poses.py
git commit -m "feat: add core frame and pose contracts"
```

---

### Task 3: Add Camera and Multi-View Observation Contracts

**Files:**
- Create: `src/mosaic/core/cameras.py`
- Create: `src/mosaic/core/observations.py`
- Modify: `src/mosaic/core/__init__.py`
- Create: `tests/core/test_observations.py`

- [ ] **Step 1: Write failing observation tests**

Create `tests/core/test_observations.py`:

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


def test_camera_intrinsics_project_point() -> None:
    pixel = _intrinsics().project((1.0, 2.0, 4.0))

    assert pixel.u == 420.0
    assert pixel.v == 440.5


def test_camera_intrinsics_rejects_non_positive_depth_projection() -> None:
    with pytest.raises(ValueError, match="non-positive depth"):
        _intrinsics().project((0.0, 0.0, 0.0))


def test_image_buffer_validates_rgb_length() -> None:
    image = _rgb()

    assert image.data == b"\x00\x00\x00\xff\xff\xff"


def test_image_buffer_rejects_wrong_byte_length() -> None:
    with pytest.raises(ValueError, match="data length"):
        ImageBuffer(width=2, height=1, channels=3, encoding=ImageEncoding.RGB8, data=b"short")


def test_multi_view_observation_requires_matching_timestamps() -> None:
    first = CameraObservation(
        camera_id="front",
        timestamp=Timestamp.from_seconds(1.0),
        camera_pose=_pose("camera/front"),
        intrinsics=_intrinsics(),
        color=_rgb(),
    )
    second = CameraObservation(
        camera_id="rear",
        timestamp=Timestamp.from_seconds(2.0),
        camera_pose=_pose("camera/rear"),
        intrinsics=_intrinsics(),
        color=_rgb(),
    )

    with pytest.raises(ValueError, match="same timestamp"):
        MultiViewObservation(timestamp=Timestamp.from_seconds(1.0), views=(first, second))


def test_multi_view_observation_accepts_distinct_camera_ids() -> None:
    timestamp = Timestamp.from_seconds(3.0)
    observation = MultiViewObservation(
        timestamp=timestamp,
        views=(
            CameraObservation(
                camera_id="front",
                timestamp=timestamp,
                camera_pose=_pose("camera/front"),
                intrinsics=_intrinsics(),
                color=_rgb(),
            ),
            CameraObservation(
                camera_id="left",
                timestamp=timestamp,
                camera_pose=_pose("camera/left"),
                intrinsics=_intrinsics(),
                color=_rgb(),
            ),
        ),
    )

    assert observation.camera_ids == ("front", "left")
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
uv run pytest tests/core/test_observations.py -q
```

Expected: FAIL with import errors for `CameraIntrinsics`, `ImageBuffer`, or `MultiViewObservation`.

- [ ] **Step 3: Implement camera intrinsics**

Create `src/mosaic/core/cameras.py`:

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Pixel:
    u: float
    v: float


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

- [ ] **Step 4: Implement image and observation contracts**

Create `src/mosaic/core/observations.py`:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Mapping

from mosaic.core.cameras import CameraIntrinsics
from mosaic.core.frames import Timestamp
from mosaic.core.poses import Pose3


class ImageEncoding(StrEnum):
    RGB8 = "rgb8"
    DEPTH_F32 = "depth_f32"


@dataclass(frozen=True, slots=True)
class ImageBuffer:
    width: int
    height: int
    channels: int
    encoding: ImageEncoding
    data: bytes

    def __post_init__(self) -> None:
        if self.width <= 0:
            raise ValueError("ImageBuffer width must be positive")
        if self.height <= 0:
            raise ValueError("ImageBuffer height must be positive")
        if self.channels <= 0:
            raise ValueError("ImageBuffer channels must be positive")
        bytes_per_channel = 4 if self.encoding is ImageEncoding.DEPTH_F32 else 1
        expected_length = self.width * self.height * self.channels * bytes_per_channel
        if len(self.data) != expected_length:
            raise ValueError("ImageBuffer data length does not match dimensions")


@dataclass(frozen=True, slots=True)
class CameraObservation:
    camera_id: str
    timestamp: Timestamp
    camera_pose: Pose3
    intrinsics: CameraIntrinsics
    color: ImageBuffer | None = None
    depth: ImageBuffer | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.camera_id.strip():
            raise ValueError("CameraObservation camera_id must not be blank")
        if self.color is None and self.depth is None:
            raise ValueError("CameraObservation requires color or depth data")
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


@dataclass(frozen=True, slots=True)
class MultiViewObservation:
    timestamp: Timestamp
    views: tuple[CameraObservation, ...]

    def __post_init__(self) -> None:
        if not self.views:
            raise ValueError("MultiViewObservation requires at least one camera view")
        for view in self.views:
            if view.timestamp != self.timestamp:
                raise ValueError("All camera views must share the same timestamp")
        camera_ids = [view.camera_id for view in self.views]
        if len(camera_ids) != len(set(camera_ids)):
            raise ValueError("MultiViewObservation camera_ids must be unique")

    @property
    def camera_ids(self) -> tuple[str, ...]:
        return tuple(view.camera_id for view in self.views)
```

- [ ] **Step 5: Export camera and observation contracts**

Replace `src/mosaic/core/__init__.py` with:

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

- [ ] **Step 6: Run tests to verify they pass**

Run:

```bash
uv run pytest tests/core/test_observations.py -q
```

Expected: PASS.

- [ ] **Step 7: Run all core tests**

Run:

```bash
uv run pytest tests/core -q
```

Expected: PASS.

- [ ] **Step 8: Commit**

```bash
git add src/mosaic/core tests/core/test_observations.py
git commit -m "feat: add camera and multiview observation contracts"
```

---

### Task 4: Add Deterministic Multi-View Dataset Replay

**Files:**
- Create: `src/mosaic/datasets/__init__.py`
- Create: `src/mosaic/datasets/replay.py`
- Create: `tests/datasets/test_replay.py`

- [ ] **Step 1: Write failing replay tests**

Create `tests/datasets/test_replay.py`:

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
from mosaic.datasets import InMemorySequence


def _observation(seconds: float) -> MultiViewObservation:
    timestamp = Timestamp.from_seconds(seconds)
    image = ImageBuffer(width=1, height=1, channels=3, encoding=ImageEncoding.RGB8, data=b"\x00\x00\x00")
    return MultiViewObservation(
        timestamp=timestamp,
        views=(
            CameraObservation(
                camera_id="front",
                timestamp=timestamp,
                camera_pose=Pose3(
                    parent_frame=FrameId("world"),
                    child_frame=FrameId("camera/front"),
                    translation=Translation3(),
                    rotation=Quaternion.identity(),
                ),
                intrinsics=CameraIntrinsics(width=1, height=1, fx=1.0, fy=1.0, cx=0.5, cy=0.5),
                color=image,
            ),
        ),
    )


def test_in_memory_sequence_replays_observations_in_order() -> None:
    first = _observation(1.0)
    second = _observation(2.0)
    sequence = InMemorySequence((first, second))

    assert list(sequence) == [first, second]
    assert len(sequence) == 2


def test_in_memory_sequence_rejects_empty_sequences() -> None:
    with pytest.raises(ValueError, match="at least one"):
        InMemorySequence(())


def test_in_memory_sequence_rejects_time_reversal() -> None:
    with pytest.raises(ValueError, match="timestamp order"):
        InMemorySequence((_observation(2.0), _observation(1.0)))
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
uv run pytest tests/datasets/test_replay.py -q
```

Expected: FAIL with `ModuleNotFoundError: No module named 'mosaic.datasets'`.

- [ ] **Step 3: Implement deterministic replay**

Create `src/mosaic/datasets/replay.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Protocol

from mosaic.core.observations import MultiViewObservation


class MultiViewSequence(Protocol):
    def __iter__(self) -> Iterator[MultiViewObservation]:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class InMemorySequence:
    observations: tuple[MultiViewObservation, ...]

    def __post_init__(self) -> None:
        if not self.observations:
            raise ValueError("InMemorySequence requires at least one observation")
        timestamps = [observation.timestamp for observation in self.observations]
        if timestamps != sorted(timestamps):
            raise ValueError("InMemorySequence observations must be in timestamp order")

    def __iter__(self) -> Iterator[MultiViewObservation]:
        return iter(self.observations)

    def __len__(self) -> int:
        return len(self.observations)
```

- [ ] **Step 4: Export dataset contracts**

Create `src/mosaic/datasets/__init__.py`:

```python
from mosaic.datasets.replay import InMemorySequence, MultiViewSequence

__all__ = ["InMemorySequence", "MultiViewSequence"]
```

- [ ] **Step 5: Run replay tests to verify they pass**

Run:

```bash
uv run pytest tests/datasets/test_replay.py -q
```

Expected: PASS.

- [ ] **Step 6: Run all existing tests**

Run:

```bash
uv run pytest -q
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/mosaic/datasets tests/datasets/test_replay.py
git commit -m "feat: add deterministic multiview replay"
```

---

### Task 5: Add Gaussian Splat Primitive and Splat Map State

**Files:**
- Create: `src/mosaic/splats/__init__.py`
- Create: `src/mosaic/splats/primitives.py`
- Create: `src/mosaic/splats/maps.py`
- Create: `tests/splats/test_splat_map.py`

- [ ] **Step 1: Write failing splat-map tests**

Create `tests/splats/test_splat_map.py`:

```python
import pytest

from mosaic.core import FrameId
from mosaic.splats import GaussianSplat, SplatMap


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


def test_gaussian_splat_rejects_invalid_opacity() -> None:
    with pytest.raises(ValueError, match="opacity"):
        GaussianSplat(
            center=(0.0, 0.0, 0.0),
            covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1),
            opacity=1.5,
        )


def test_gaussian_splat_rejects_non_positive_covariance_diagonal() -> None:
    with pytest.raises(ValueError, match="covariance diagonal"):
        GaussianSplat(center=(0.0, 0.0, 0.0), covariance_upper=(0.0, 0.0, 0.0, 0.1, 0.0, 0.1))


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

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
uv run pytest tests/splats/test_splat_map.py -q
```

Expected: FAIL with `ModuleNotFoundError: No module named 'mosaic.splats'`.

- [ ] **Step 3: Implement Gaussian splat primitive**

Create `src/mosaic/splats/primitives.py`:

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GaussianSplat:
    center: tuple[float, float, float]
    covariance_upper: tuple[float, float, float, float, float, float]
    color_rgb: tuple[float, float, float] = (1.0, 1.0, 1.0)
    opacity: float = 1.0
    provenance: str | None = None

    def __post_init__(self) -> None:
        if len(self.center) != 3:
            raise ValueError("GaussianSplat center must contain three coordinates")
        if len(self.covariance_upper) != 6:
            raise ValueError("GaussianSplat covariance_upper must contain six values")
        xx, _, _, yy, _, zz = self.covariance_upper
        if xx <= 0.0 or yy <= 0.0 or zz <= 0.0:
            raise ValueError("GaussianSplat covariance diagonal values must be positive")
        if len(self.color_rgb) != 3:
            raise ValueError("GaussianSplat color_rgb must contain three channels")
        if any(channel < 0.0 or channel > 1.0 for channel in self.color_rgb):
            raise ValueError("GaussianSplat color_rgb channels must be between 0 and 1")
        if self.opacity < 0.0 or self.opacity > 1.0:
            raise ValueError("GaussianSplat opacity must be between 0 and 1")
```

- [ ] **Step 4: Implement splat map state**

Create `src/mosaic/splats/maps.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Self

from mosaic.core.frames import FrameId
from mosaic.splats.primitives import GaussianSplat


@dataclass(frozen=True, slots=True)
class SplatMap:
    frame: FrameId
    splats: tuple[GaussianSplat, ...] = ()

    def with_splats(self, splats: Iterable[GaussianSplat]) -> Self:
        return type(self)(frame=self.frame, splats=self.splats + tuple(splats))

    def __len__(self) -> int:
        return len(self.splats)
```

- [ ] **Step 5: Export splat contracts**

Create `src/mosaic/splats/__init__.py`:

```python
from mosaic.splats.maps import SplatMap
from mosaic.splats.primitives import GaussianSplat

__all__ = ["GaussianSplat", "SplatMap"]
```

- [ ] **Step 6: Run splat tests to verify they pass**

Run:

```bash
uv run pytest tests/splats/test_splat_map.py -q
```

Expected: PASS.

- [ ] **Step 7: Run all existing tests**

Run:

```bash
uv run pytest -q
```

Expected: PASS.

- [ ] **Step 8: Commit**

```bash
git add src/mosaic/splats tests/splats/test_splat_map.py
git commit -m "feat: add gaussian splat map state"
```

---

### Task 6: Add SLAM Backend Protocol and Deterministic Backend

**Files:**
- Create: `src/mosaic/slam/__init__.py`
- Create: `src/mosaic/slam/protocol.py`
- Create: `src/mosaic/slam/fake_backend.py`
- Create: `tests/slam/test_backend_contract.py`

- [ ] **Step 1: Write failing backend contract tests**

Create `tests/slam/test_backend_contract.py`:

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

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
uv run pytest tests/slam/test_backend_contract.py -q
```

Expected: FAIL with `ModuleNotFoundError: No module named 'mosaic.slam'`.

- [ ] **Step 3: Implement SLAM protocol contracts**

Create `src/mosaic/slam/protocol.py`:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Mapping, Protocol, runtime_checkable

from mosaic.core.frames import Timestamp
from mosaic.core.observations import MultiViewObservation
from mosaic.core.poses import Pose3
from mosaic.splats.maps import SplatMap

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

- [ ] **Step 4: Implement deterministic backend**

Create `src/mosaic/slam/fake_backend.py`:

```python
from __future__ import annotations

from dataclasses import dataclass, field

from mosaic.core.frames import FrameId
from mosaic.core.observations import MultiViewObservation
from mosaic.slam.protocol import BackendCapabilities, SplatSlamUpdate, TrackingState
from mosaic.splats import GaussianSplat, SplatMap


@dataclass(slots=True)
class DeterministicSplatBackend:
    map_frame: FrameId = field(default_factory=lambda: FrameId("map"))
    _splats: list[GaussianSplat] = field(default_factory=list, init=False, repr=False)

    @property
    def name(self) -> str:
        return "deterministic-splat"

    @property
    def capabilities(self) -> BackendCapabilities:
        return BackendCapabilities(
            supports_multi_view=True,
            supports_incremental_mapping=True,
            supports_uncertainty=False,
            runs_out_of_process=False,
            parameters={"deterministic": True},
        )

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

- [ ] **Step 5: Export SLAM contracts**

Create `src/mosaic/slam/__init__.py`:

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

- [ ] **Step 6: Run backend contract tests to verify they pass**

Run:

```bash
uv run pytest tests/slam/test_backend_contract.py -q
```

Expected: PASS.

- [ ] **Step 7: Run all existing tests**

Run:

```bash
uv run pytest -q
```

Expected: PASS.

- [ ] **Step 8: Commit**

```bash
git add src/mosaic/slam tests/slam/test_backend_contract.py
git commit -m "feat: add splat slam backend protocol"
```

---

### Task 7: Publish the Initial Public API Surface

**Files:**
- Modify: `src/mosaic/__init__.py`
- Create: `tests/test_public_api.py`

- [ ] **Step 1: Write failing public API test**

Create `tests/test_public_api.py`:

```python
from mosaic import (
    CameraIntrinsics,
    DeterministicSplatBackend,
    FrameId,
    GaussianSplat,
    InMemorySequence,
    SplatMap,
    Timestamp,
    TrackingState,
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
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
uv run pytest tests/test_public_api.py -q
```

Expected: FAIL with import errors from `mosaic`.

- [ ] **Step 3: Export first-milestone API from the package root**

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
from mosaic.slam import BackendCapabilities, DeterministicSplatBackend, SplatSlamBackend, SplatSlamUpdate, TrackingState
from mosaic.splats import GaussianSplat, SplatMap

__version__ = "0.1.0"

__all__ = [
    "BackendCapabilities",
    "CameraIntrinsics",
    "CameraObservation",
    "DeterministicSplatBackend",
    "FrameId",
    "GaussianSplat",
    "ImageBuffer",
    "ImageEncoding",
    "InMemorySequence",
    "MultiViewObservation",
    "MultiViewSequence",
    "Pixel",
    "Pose3",
    "Quaternion",
    "SplatMap",
    "SplatSlamBackend",
    "SplatSlamUpdate",
    "Timestamp",
    "TrackingState",
    "Translation3",
    "__version__",
]
```

- [ ] **Step 4: Run public API test to verify it passes**

Run:

```bash
uv run pytest tests/test_public_api.py -q
```

Expected: PASS.

- [ ] **Step 5: Run the full test suite**

Run:

```bash
uv run pytest -q
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/mosaic/__init__.py tests/test_public_api.py
git commit -m "feat: expose splat slam foundation api"
```

---

## Final Verification

- [ ] **Step 1: Run the complete suite**

```bash
uv run pytest -q
```

Expected: PASS for all tests.

- [ ] **Step 2: Inspect working tree**

```bash
git status --short
```

Expected: no uncommitted source or test changes except plan/spec documents that the user has chosen not to commit.

- [ ] **Step 3: Confirm milestone coverage**

Check that these imports work in a Python shell:

```python
from mosaic.core import FrameId, Timestamp, CameraIntrinsics, MultiViewObservation
from mosaic.datasets import InMemorySequence
from mosaic.splats import GaussianSplat, SplatMap
from mosaic.slam import DeterministicSplatBackend, SplatSlamBackend
```

Expected: imports succeed.

---

## Self-Review Notes

- Spec coverage: Tasks 2 and 3 implement typed pose, frame, timestamp, camera, and observation objects. Task 4 implements deterministic replay. Task 5 implements splat-map state. Task 6 implements backend lifecycle contracts and a deterministic backend. Task 7 exposes the first public API.
- Deferred scope: robot platform adapters, fusion strategies, evaluation harnesses, and agent posterior APIs are intentionally outside this first implementation slice.
- Type consistency: `FrameId`, `Timestamp`, `Pose3`, `CameraIntrinsics`, `MultiViewObservation`, `GaussianSplat`, `SplatMap`, `SplatSlamUpdate`, and `DeterministicSplatBackend` names are consistent across tasks and tests.
