# Testing Patterns

**Analysis Date:** 2026-05-18

## Test Framework

**Runner:**
- `pytest` is the planned test runner. It is not currently configured in `pyproject.toml`, but `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md` specifies adding `pytest>=8.4.0` to the `dev` dependency group.
- Planned config location: `pyproject.toml` under `[tool.pytest.ini_options]` with `testpaths = ["tests"]` and `pythonpath = ["src"]`.
- Current repository state has no `tests/` directory and no `pytest.ini`, `tox.ini`, `noxfile.py`, or coverage configuration.

**Assertion Library:**
- Use plain Python `assert` statements.
- Use `pytest.raises` for validation and error-path checks.

**Run Commands:**
```bash
uv run pytest -q                              # Run all tests once tests/ exists
uv run pytest tests/core -q                   # Run a focused package test subtree
uv run pytest tests/test_public_api.py -q     # Run public API export checks
```

## Test File Organization

**Location:**
- Use a top-level `tests/` directory mirroring `src/mosaic/` package areas.
- Planned test files include `tests/test_package_import.py`, `tests/test_public_api.py`, `tests/core/test_frames_and_poses.py`, `tests/core/test_observations.py`, `tests/datasets/test_replay.py`, `tests/splats/test_splat_map.py`, `tests/slam/test_backend_contract.py`, `tests/platforms/test_camera_rig.py`, `tests/platforms/test_registry.py`, `tests/platforms/test_presets.py`, `tests/fusion/test_fusion_protocol.py`, `tests/fusion/test_strategies.py`, `tests/evaluation/test_metrics.py`, `tests/evaluation/test_scenarios.py`, `tests/evaluation/test_runner.py`, `tests/evaluation/test_regression.py`, `tests/agents/test_queries.py`, and `tests/agents/test_splat_posterior.py`.

**Naming:**
- Test modules use `test_*.py`.
- Test functions use `test_<behavior>() -> None`, for example `test_timestamp_from_seconds_uses_nanoseconds()`, `test_camera_intrinsics_project_point()`, `test_deterministic_backend_reset_clears_state()`, and `test_public_api_exports_agent_types()`.
- Helper factories use leading underscores: `_pose()`, `_intrinsics()`, `_rgb()`, `_observation()`, `_platform()`, `_splat()`, `_map()`, and `_artifact()`.

**Structure:**
```text
tests/
├── test_package_import.py        # Import/version smoke test
├── test_public_api.py            # Root package export contract
├── core/                         # Geometry, camera, observation contracts
├── datasets/                     # Replay and sequence determinism
├── splats/                       # Gaussian splat and map state
├── slam/                         # Backend lifecycle contract tests
├── platforms/                    # Robot/camera-rig contracts and presets
├── fusion/                       # Posterior-aware fusion protocol/strategy tests
├── evaluation/                   # Metrics, benchmark artifacts, regression gates
└── agents/                       # Agent posterior query seam tests
```

## Test Structure

**Suite Organization:**
```python
import pytest

from mosaic.core import FrameId, Pose3, Quaternion, Timestamp, Translation3


def test_timestamp_rejects_negative_values() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        Timestamp(-1)


def test_pose_tracks_parent_and_child_frames() -> None:
    pose = Pose3(
        parent_frame=FrameId("world"),
        child_frame=FrameId("camera/front"),
        translation=Translation3(1.0, 2.0, 3.0),
        rotation=Quaternion.identity(),
    )

    assert pose.parent_frame == FrameId("world")
    assert pose.child_frame == FrameId("camera/front")
```

**Patterns:**
- Arrange/act/assert with blank lines between setup, operation, and assertions.
- Prefer small behavior-focused tests with one primary assertion theme.
- Assert complete values for immutable objects where practical, e.g. `MetricResult(...)`, `RegressionResult(...)`, tuple camera IDs, or JSON-ready dictionaries.
- Test both valid and invalid inputs for every public dataclass or protocol result object.
- Cover public root exports in `tests/test_public_api.py` whenever new stable symbols are added to `src/mosaic/__init__.py`.

## Mocking

**Framework:** Not detected / not currently planned

**Patterns:**
```python
from mosaic.slam import DeterministicSplatBackend, TrackingState


def test_deterministic_backend_processes_observation_into_splat_update() -> None:
    backend = DeterministicSplatBackend(map_frame=FrameId("map"))

    update = backend.process(_observation())

    assert update.tracking_state is TrackingState.TRACKING
    assert len(update.map_update) == 1
```

**What to Mock:**
- Avoid mocks for current pure-Python contracts. Use deterministic reference implementations such as planned `DetermininisticSplatBackend` in `src/mosaic/slam/fake_backend.py`, `InMemorySequence` in `src/mosaic/datasets/replay.py`, and `ProvenancePreservingFusion` in `src/mosaic/fusion/strategies.py`.
- Introduce mocks only for future external backends, CUDA/native process boundaries, filesystem errors, network services, or robot SDK integrations.

**What NOT to Mock:**
- Do not mock core value objects such as `Timestamp`, `FrameId`, `Pose3`, `CameraIntrinsics`, `ImageBuffer`, `GaussianSplat`, or `SplatMap`.
- Do not mock deterministic in-memory replay for unit tests; construct real `MultiViewObservation` objects.
- Do not mock root package exports; import from `mosaic` in `tests/test_public_api.py` to catch API drift.

## Fixtures and Factories

**Test Data:**
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

**Location:**
- Keep helper factories local to the test module that uses them until reuse is proven.
- Use `tmp_path` for filesystem artifact tests, as planned in `tests/evaluation/test_runner.py` for `write_benchmark_artifact()`.
- No shared `tests/conftest.py` is currently planned or present.

## Coverage

**Requirements:** None enforced

**View Coverage:**
```bash
# Not configured; no coverage dependency or pyproject coverage section detected.
```

- Coverage tooling is not present in `pyproject.toml`.
- The planned regression discipline emphasizes deterministic behavior and public contract coverage over numeric coverage thresholds.
- Add coverage later only after the initial contract test suite exists; do not block the current library foundation on coverage infrastructure.

## Test Types

**Unit Tests:**
- Scope: value objects, dataclass validation, enum values, immutable container behavior, small metric functions, and query result objects.
- Planned examples: `tests/core/test_frames_and_poses.py`, `tests/core/test_observations.py`, `tests/splats/test_splat_map.py`, `tests/evaluation/test_metrics.py`, and `tests/agents/test_queries.py`.
- Use direct object construction and exact assertions.

**Integration Tests:**
- Scope: deterministic interactions across Mosaic modules without external services.
- Planned examples: `tests/slam/test_backend_contract.py` processes `MultiViewObservation` through `DetermininisticSplatBackend`; `tests/evaluation/test_runner.py` runs a synthetic scenario through a backend and writes JSON artifacts; `tests/agents/test_splat_posterior.py` queries a `SplatMap` through `SplatPosteriorView`.
- Keep integration tests in-process and deterministic.

**Contract Tests:**
- Backend lifecycle contract tests belong in `tests/slam/test_backend_contract.py` and should exercise `process()`, `snapshot()`, and `reset()` for any backend implementation.
- Public API contract tests belong in `tests/test_public_api.py` and must be updated whenever `src/mosaic/__init__.py` exports change.
- Fusion protocol tests belong in `tests/fusion/test_fusion_protocol.py` and `tests/fusion/test_strategies.py`.

**E2E Tests:**
- Not used.
- No ROS, robot hardware, CUDA backend, simulator, browser UI, or LLM provider integration is currently part of the test setup.

## Common Patterns

**Async Testing:**
```python
# Not currently used. Mosaic's planned initial APIs are synchronous Python library calls.
```

**Error Testing:**
```python
def test_image_buffer_rejects_wrong_byte_length() -> None:
    with pytest.raises(ValueError, match="data length"):
        ImageBuffer(
            width=2,
            height=1,
            channels=3,
            encoding=ImageEncoding.RGB8,
            data=b"short",
        )
```

**Immutability Testing:**
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

**Determinism Testing:**
```python
def test_synthetic_forward_sequence_is_deterministic() -> None:
    first = synthetic_forward_sequence(frame_count=3)
    second = synthetic_forward_sequence(frame_count=3)

    assert first == second
    assert [observation.timestamp.nanoseconds for observation in first.sequence] == [0, 100_000_000, 200_000_000]
```

**Artifact Testing:**
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

## Current Quality Gaps

- No actual tests are committed under `/home/prannayag/pragnition/robotics/mosaic/tests`.
- `pyproject.toml` does not yet include `pytest` or `[tool.pytest.ini_options]`.
- No CI workflow is detected under `/home/prannayag/pragnition/robotics/mosaic/.github/`.
- No coverage, mutation testing, static typing, linting, formatting, or pre-commit checks are configured.
- `src/mosaic/__init__.py` currently contains only a trivial `hello()` function, so the planned contract test suite will initially fail until the implementation plans are executed.

---

*Testing analysis: 2026-05-18*
