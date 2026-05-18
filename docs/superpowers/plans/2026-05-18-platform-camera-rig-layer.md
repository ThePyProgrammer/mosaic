# Platform Camera Rig Layer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add robot-agnostic platform and camera-rig contracts for quadrupeds, UGVs, humanoids, and custom multi-view rigs.

**Architecture:** The platform layer consumes Mosaic core geometry/camera types and produces typed camera-rig descriptions without depending on any robot SDK, simulator, or SLAM backend. It clean-room ports Argus's platform-registry idea while keeping embodiment metadata separate from camera calibration.

**Tech Stack:** Python 3.12, `dataclasses`, `enum.StrEnum`, `typing.Protocol`, `pytest`, `uv`.

---

## Prerequisite

Complete `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md` first. This plan assumes `mosaic.core` exports `CameraIntrinsics`, `FrameId`, `Pose3`, `Quaternion`, and `Translation3`.

## File Structure

Create or modify these files:

```text
src/mosaic/platforms/__init__.py          # Public platform exports
src/mosaic/platforms/types.py             # Embodiment and camera-rig data contracts
src/mosaic/platforms/registry.py          # Platform registry and lookup behavior
src/mosaic/platforms/presets.py           # Representative quadruped, UGV, humanoid rig factories
src/mosaic/__init__.py                    # Root-level exports for stable platform API
tests/platforms/test_camera_rig.py        # Camera rig validation tests
tests/platforms/test_registry.py          # Registry behavior tests
tests/platforms/test_presets.py           # Built-in platform preset tests
tests/test_public_api.py                  # Add root export expectations
```

Run all commands from:

```bash
cd /home/prannayag/pragnition/robotics/mosaic
```

---

### Task 1: Add Camera Rig and Platform Description Contracts

**Files:**
- Create: `src/mosaic/platforms/__init__.py`
- Create: `src/mosaic/platforms/types.py`
- Create: `tests/platforms/test_camera_rig.py`

- [ ] **Step 1: Write failing camera-rig tests**

Create `tests/platforms/test_camera_rig.py`:

```python
import pytest

from mosaic.core import CameraIntrinsics, FrameId, Pose3, Quaternion, Translation3
from mosaic.platforms import CameraMount, CameraRig, Embodiment, PlatformDescription


def _intrinsics() -> CameraIntrinsics:
    return CameraIntrinsics(width=640, height=480, fx=400.0, fy=400.0, cx=320.0, cy=240.0)


def _pose(child_frame: str) -> Pose3:
    return Pose3(
        parent_frame=FrameId("base_link"),
        child_frame=FrameId(child_frame),
        translation=Translation3(),
        rotation=Quaternion.identity(),
    )


def test_camera_rig_exposes_camera_ids_in_order() -> None:
    rig = CameraRig(
        frame=FrameId("base_link"),
        cameras=(
            CameraMount(camera_id="front", pose=_pose("camera/front"), intrinsics=_intrinsics()),
            CameraMount(camera_id="left", pose=_pose("camera/left"), intrinsics=_intrinsics()),
        ),
    )

    assert rig.camera_ids == ("front", "left")
    assert rig.camera("left").pose.child_frame == FrameId("camera/left")


def test_camera_rig_rejects_duplicate_camera_ids() -> None:
    with pytest.raises(ValueError, match="unique"):
        CameraRig(
            frame=FrameId("base_link"),
            cameras=(
                CameraMount(camera_id="front", pose=_pose("camera/front"), intrinsics=_intrinsics()),
                CameraMount(camera_id="front", pose=_pose("camera/front2"), intrinsics=_intrinsics()),
            ),
        )


def test_camera_mount_pose_must_attach_to_rig_frame() -> None:
    with pytest.raises(ValueError, match="parent frame"):
        CameraRig(
            frame=FrameId("base_link"),
            cameras=(
                CameraMount(
                    camera_id="front",
                    pose=Pose3(
                        parent_frame=FrameId("world"),
                        child_frame=FrameId("camera/front"),
                        translation=Translation3(),
                        rotation=Quaternion.identity(),
                    ),
                    intrinsics=_intrinsics(),
                ),
            ),
        )


def test_platform_description_keeps_embodiment_metadata_separate_from_rig() -> None:
    platform = PlatformDescription(
        name="custom-quad",
        embodiment=Embodiment.QUADRUPED,
        base_frame=FrameId("base_link"),
        camera_rig=CameraRig(
            frame=FrameId("base_link"),
            cameras=(CameraMount(camera_id="front", pose=_pose("camera/front"), intrinsics=_intrinsics()),),
        ),
        metadata={"vendor": "research"},
    )

    assert platform.name == "custom-quad"
    assert platform.embodiment is Embodiment.QUADRUPED
    assert platform.camera_rig.camera_ids == ("front",)
    assert platform.metadata["vendor"] == "research"
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
uv run pytest tests/platforms/test_camera_rig.py -q
```

Expected: FAIL with `ModuleNotFoundError: No module named 'mosaic.platforms'`.

- [ ] **Step 3: Implement camera-rig and platform contracts**

Create `src/mosaic/platforms/types.py`:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Mapping

from mosaic.core import CameraIntrinsics, FrameId, Pose3


class Embodiment(StrEnum):
    QUADRUPED = "quadruped"
    UGV = "ugv"
    HUMANOID = "humanoid"
    CUSTOM = "custom"


@dataclass(frozen=True, slots=True)
class CameraMount:
    camera_id: str
    pose: Pose3
    intrinsics: CameraIntrinsics
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.camera_id.strip():
            raise ValueError("CameraMount camera_id must not be blank")
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


@dataclass(frozen=True, slots=True)
class CameraRig:
    frame: FrameId
    cameras: tuple[CameraMount, ...]

    def __post_init__(self) -> None:
        if not self.cameras:
            raise ValueError("CameraRig requires at least one camera")
        camera_ids = [camera.camera_id for camera in self.cameras]
        if len(camera_ids) != len(set(camera_ids)):
            raise ValueError("CameraRig camera_id values must be unique")
        for camera in self.cameras:
            if camera.pose.parent_frame != self.frame:
                raise ValueError("CameraMount pose parent frame must match CameraRig frame")

    @property
    def camera_ids(self) -> tuple[str, ...]:
        return tuple(camera.camera_id for camera in self.cameras)

    def camera(self, camera_id: str) -> CameraMount:
        for camera in self.cameras:
            if camera.camera_id == camera_id:
                return camera
        raise KeyError(camera_id)


@dataclass(frozen=True, slots=True)
class PlatformDescription:
    name: str
    embodiment: Embodiment
    base_frame: FrameId
    camera_rig: CameraRig
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("PlatformDescription name must not be blank")
        if self.camera_rig.frame != self.base_frame:
            raise ValueError("PlatformDescription base_frame must match camera rig frame")
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))
```

- [ ] **Step 4: Export platform contracts**

Create `src/mosaic/platforms/__init__.py`:

```python
from mosaic.platforms.types import CameraMount, CameraRig, Embodiment, PlatformDescription

__all__ = [
    "CameraMount",
    "CameraRig",
    "Embodiment",
    "PlatformDescription",
]
```

- [ ] **Step 5: Run camera-rig tests to verify they pass**

Run:

```bash
uv run pytest tests/platforms/test_camera_rig.py -q
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/mosaic/platforms tests/platforms/test_camera_rig.py
git commit -m "feat: add robot camera rig contracts"
```

---

### Task 2: Add Platform Registry

**Files:**
- Create: `src/mosaic/platforms/registry.py`
- Modify: `src/mosaic/platforms/__init__.py`
- Create: `tests/platforms/test_registry.py`

- [ ] **Step 1: Write failing registry tests**

Create `tests/platforms/test_registry.py`:

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

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
uv run pytest tests/platforms/test_registry.py -q
```

Expected: FAIL with import error for `PlatformRegistry`.

- [ ] **Step 3: Implement registry**

Create `src/mosaic/platforms/registry.py`:

```python
from __future__ import annotations

from dataclasses import dataclass, field

from mosaic.platforms.types import PlatformDescription


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

- [ ] **Step 4: Export registry**

Replace `src/mosaic/platforms/__init__.py` with:

```python
from mosaic.platforms.registry import PlatformRegistry
from mosaic.platforms.types import CameraMount, CameraRig, Embodiment, PlatformDescription

__all__ = [
    "CameraMount",
    "CameraRig",
    "Embodiment",
    "PlatformDescription",
    "PlatformRegistry",
]
```

- [ ] **Step 5: Run registry tests to verify they pass**

Run:

```bash
uv run pytest tests/platforms/test_registry.py -q
```

Expected: PASS.

- [ ] **Step 6: Run all platform tests**

Run:

```bash
uv run pytest tests/platforms -q
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/mosaic/platforms/registry.py src/mosaic/platforms/__init__.py tests/platforms/test_registry.py
git commit -m "feat: add platform registry"
```

---

### Task 3: Add Built-in Representative Platform Presets

**Files:**
- Create: `src/mosaic/platforms/presets.py`
- Modify: `src/mosaic/platforms/__init__.py`
- Create: `tests/platforms/test_presets.py`

- [ ] **Step 1: Write failing preset tests**

Create `tests/platforms/test_presets.py`:

```python
from mosaic.core import FrameId
from mosaic.platforms import Embodiment, default_platform_registry, humanoid_stereo_rig, quadruped_front_rig, ugv_surround_rig


def test_quadruped_front_rig_uses_quadruped_embodiment() -> None:
    platform = quadruped_front_rig()

    assert platform.name == "quadruped-front"
    assert platform.embodiment is Embodiment.QUADRUPED
    assert platform.base_frame == FrameId("base_link")
    assert platform.camera_rig.camera_ids == ("front",)


def test_ugv_surround_rig_has_four_ordered_cameras() -> None:
    platform = ugv_surround_rig()

    assert platform.name == "ugv-surround"
    assert platform.embodiment is Embodiment.UGV
    assert platform.camera_rig.camera_ids == ("front", "left", "right", "rear")


def test_humanoid_stereo_rig_has_head_stereo_cameras() -> None:
    platform = humanoid_stereo_rig()

    assert platform.name == "humanoid-stereo"
    assert platform.embodiment is Embodiment.HUMANOID
    assert platform.camera_rig.camera_ids == ("left_eye", "right_eye")


def test_default_registry_contains_built_in_presets() -> None:
    registry = default_platform_registry()

    assert registry.names == ("humanoid-stereo", "quadruped-front", "ugv-surround")
    assert registry.get("ugv-surround").camera_rig.camera_ids == ("front", "left", "right", "rear")
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
uv run pytest tests/platforms/test_presets.py -q
```

Expected: FAIL with import errors for preset functions.

- [ ] **Step 3: Implement preset factories**

Create `src/mosaic/platforms/presets.py`:

```python
from __future__ import annotations

from mosaic.core import CameraIntrinsics, FrameId, Pose3, Quaternion, Translation3
from mosaic.platforms.registry import PlatformRegistry
from mosaic.platforms.types import CameraMount, CameraRig, Embodiment, PlatformDescription


def _intrinsics(width: int = 640, height: int = 480) -> CameraIntrinsics:
    return CameraIntrinsics(width=width, height=height, fx=400.0, fy=400.0, cx=width / 2.0, cy=height / 2.0)


def _mount(camera_id: str, x: float, y: float, z: float) -> CameraMount:
    base_frame = FrameId("base_link")
    return CameraMount(
        camera_id=camera_id,
        pose=Pose3(
            parent_frame=base_frame,
            child_frame=FrameId(f"camera/{camera_id}"),
            translation=Translation3(x=x, y=y, z=z),
            rotation=Quaternion.identity(),
        ),
        intrinsics=_intrinsics(),
    )


def quadruped_front_rig() -> PlatformDescription:
    base_frame = FrameId("base_link")
    return PlatformDescription(
        name="quadruped-front",
        embodiment=Embodiment.QUADRUPED,
        base_frame=base_frame,
        camera_rig=CameraRig(frame=base_frame, cameras=(_mount("front", 0.30, 0.0, 0.35),)),
    )


def ugv_surround_rig() -> PlatformDescription:
    base_frame = FrameId("base_link")
    return PlatformDescription(
        name="ugv-surround",
        embodiment=Embodiment.UGV,
        base_frame=base_frame,
        camera_rig=CameraRig(
            frame=base_frame,
            cameras=(
                _mount("front", 0.45, 0.0, 0.55),
                _mount("left", 0.0, 0.35, 0.55),
                _mount("right", 0.0, -0.35, 0.55),
                _mount("rear", -0.45, 0.0, 0.55),
            ),
        ),
    )


def humanoid_stereo_rig() -> PlatformDescription:
    base_frame = FrameId("base_link")
    return PlatformDescription(
        name="humanoid-stereo",
        embodiment=Embodiment.HUMANOID,
        base_frame=base_frame,
        camera_rig=CameraRig(
            frame=base_frame,
            cameras=(
                _mount("left_eye", 0.08, 0.04, 1.55),
                _mount("right_eye", 0.08, -0.04, 1.55),
            ),
        ),
    )


def default_platform_registry() -> PlatformRegistry:
    registry = PlatformRegistry()
    registry.register(quadruped_front_rig())
    registry.register(ugv_surround_rig())
    registry.register(humanoid_stereo_rig())
    return registry
```

- [ ] **Step 4: Export preset factories**

Replace `src/mosaic/platforms/__init__.py` with:

```python
from mosaic.platforms.presets import default_platform_registry, humanoid_stereo_rig, quadruped_front_rig, ugv_surround_rig
from mosaic.platforms.registry import PlatformRegistry
from mosaic.platforms.types import CameraMount, CameraRig, Embodiment, PlatformDescription

__all__ = [
    "CameraMount",
    "CameraRig",
    "Embodiment",
    "PlatformDescription",
    "PlatformRegistry",
    "default_platform_registry",
    "humanoid_stereo_rig",
    "quadruped_front_rig",
    "ugv_surround_rig",
]
```

- [ ] **Step 5: Run preset tests to verify they pass**

Run:

```bash
uv run pytest tests/platforms/test_presets.py -q
```

Expected: PASS.

- [ ] **Step 6: Run all platform tests**

Run:

```bash
uv run pytest tests/platforms -q
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/mosaic/platforms/presets.py src/mosaic/platforms/__init__.py tests/platforms/test_presets.py
git commit -m "feat: add built-in robot camera rig presets"
```

---

### Task 4: Publish Platform API at Package Root

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
    GaussianSplat,
    InMemorySequence,
    PlatformRegistry,
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
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
uv run pytest tests/test_public_api.py -q
```

Expected: FAIL with import errors for `CameraRig`, `Embodiment`, `PlatformRegistry`, or `quadruped_front_rig` from `mosaic`.

- [ ] **Step 3: Export platform API from package root**

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
    "Quaternion",
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
git commit -m "feat: expose platform camera rig api"
```

---

## Final Verification

- [ ] **Step 1: Run the complete suite**

```bash
uv run pytest -q
```

Expected: PASS for all tests.

- [ ] **Step 2: Confirm platform imports**

Run:

```bash
uv run python -c "from mosaic.platforms import default_platform_registry; print(default_platform_registry().names)"
```

Expected output includes:

```text
('humanoid-stereo', 'quadruped-front', 'ugv-surround')
```

- [ ] **Step 3: Inspect working tree**

```bash
git status --short
```

Expected: no uncommitted source or test changes except plan/spec documents that the user has chosen not to commit.

---

## Self-Review Notes

- Spec coverage: This plan implements the Argus-derived platform layer with platform-neutral camera rigs for quadrupeds, UGVs, humanoids, and custom rigs.
- Deferred scope: No robot SDKs, simulators, locomotion behavior, map fusion, evaluation harness, or agent posterior API is included.
- Type consistency: `CameraMount`, `CameraRig`, `Embodiment`, `PlatformDescription`, `PlatformRegistry`, and preset names are consistent across tests, exports, and implementation steps.
