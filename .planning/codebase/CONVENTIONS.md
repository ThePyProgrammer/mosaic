# Coding Conventions

**Analysis Date:** 2026-05-18

## Naming Patterns

**Files:**
- Use a `src/` package layout. Runtime code lives under `src/mosaic/`; the current package files are `src/mosaic/__init__.py` and `src/mosaic/py.typed`.
- Use snake_case module names for planned Python modules such as `src/mosaic/core/frames.py`, `src/mosaic/core/poses.py`, `src/mosaic/core/observations.py`, `src/mosaic/datasets/replay.py`, `src/mosaic/slam/fake_backend.py`, and `src/mosaic/evaluation/regression.py`.
- Use package `__init__.py` files as public export surfaces, following the planned files `src/mosaic/core/__init__.py`, `src/mosaic/splats/__init__.py`, `src/mosaic/slam/__init__.py`, `src/mosaic/platforms/__init__.py`, `src/mosaic/fusion/__init__.py`, `src/mosaic/evaluation/__init__.py`, and `src/mosaic/agents/__init__.py`.
- Keep the marker file `src/mosaic/py.typed` present so type checkers treat Mosaic as a typed package.

**Functions:**
- Use snake_case for functions and methods. Existing code uses `hello()` in `src/mosaic/__init__.py`; planned APIs use names like `from_seconds()`, `as_seconds()`, `as_tuple()`, `with_splats()`, `process()`, `snapshot()`, `reset()`, `default_platform_registry()`, `quadruped_front_rig()`, `synthetic_forward_sequence()`, and `check_regression_gates()`.
- Use leading underscores for test helper factories and module-private helpers, such as `_pose()`, `_intrinsics()`, `_rgb()`, `_observation()`, `_splat()`, `_mount()`, and `_snapshot_metrics()` in the planned `tests/` and `src/mosaic/` modules.
- Use verb phrases for operations (`project`, `register`, `fuse`, `query_local`, `write_benchmark_artifact`) and noun phrases for constructors/factories that return domain objects (`quadruped_front_rig`, `synthetic_forward_sequence`).

**Variables:**
- Use snake_case for local variables and attributes: `camera_id`, `map_frame`, `splat_count`, `source_map_count`, `frame_count`, `mean_opacity`, `estimated_pose`.
- Prefer explicit domain names over abbreviations: use `timestamp`, `observation`, `intrinsics`, `provenance`, `diagnostics`, and `fusion_input`.
- Use uppercase enum members in `StrEnum` classes, with lower-case string values: `TrackingState.TRACKING = "tracking"`, `FusionStatus.FUSED = "fused"`, `AgentQueryKind.LOCAL_GEOMETRY = "local_geometry"` in the planned modules.

**Types:**
- Use PascalCase for public classes, dataclasses, protocols, and enums: `Timestamp`, `FrameId`, `Pose3`, `CameraIntrinsics`, `GaussianSplat`, `SplatMap`, `SplatSlamBackend`, `PlatformRegistry`, `FusionInput`, `MetricResult`, `SplatPosteriorView`.
- Use `Protocol` for pluggable interfaces such as `MultiViewSequence`, `SplatSlamBackend`, and `SplatFusionStrategy` in planned files under `src/mosaic/datasets/`, `src/mosaic/slam/`, and `src/mosaic/fusion/`.
- Use descriptive type aliases where payload types repeat, such as `MetricValue = bool | int | float | str` and `FusionMetricValue = bool | int | float | str` in the planned protocol modules.

## Code Style

**Formatting:**
- No formatter configuration is currently committed. There is no `.ruff.toml`, `ruff.toml`, `pyproject.toml` formatter section, `.prettierrc`, or `biome.json` under `/home/prannayag/pragnition/robotics/mosaic`.
- Use standard Python 3.12 formatting: 4-space indentation, blank lines between top-level definitions, and readable wrapping for long imports or constructor calls.
- Keep line lengths practical. The plans contain some long import lines, but new implementation should prefer parenthesized multi-line imports and constructor calls in files such as `src/mosaic/__init__.py` and test modules.
- Prefer deterministic JSON formatting for artifacts: planned `src/mosaic/evaluation/runner.py` uses `json.dumps(..., indent=2, sort_keys=True) + "\n"`.

**Linting:**
- No linting tool is configured in `pyproject.toml`; `ruff`, `flake8`, `pylint`, `mypy`, and `pyright` configuration files are not detected.
- Treat the planned tests as the current quality gate until lint/type tooling is added.
- Because `src/mosaic/py.typed` exists, keep public APIs typed and type-checker-friendly even without an enforced type-check command.

## Import Organization

**Order:**
1. `from __future__ import annotations` first in implementation modules that use forward references or modern typing, as planned in `src/mosaic/core/frames.py`, `src/mosaic/core/poses.py`, `src/mosaic/slam/protocol.py`, and similar files.
2. Standard library imports next: `dataclasses`, `enum`, `math`, `pathlib`, `types`, `typing`, `json`.
3. First-party imports from `mosaic.*` after standard library imports: e.g. `from mosaic.core.frames import FrameId`, `from mosaic.splats import SplatMap`.
4. Test-only imports such as `pytest` first in test files, followed by `from mosaic...` imports.

**Path Aliases:**
- Use package imports rooted at `mosaic`, not relative imports. Planned examples consistently use `from mosaic.core import FrameId`, `from mosaic.splats import SplatMap`, and `from mosaic.slam import DeterministicSplatBackend`.
- `pyproject.toml` currently has no `[tool.pytest.ini_options]`; planned test setup adds `pythonpath = ["src"]` so tests can import `mosaic` without installing the package.

## Error Handling

**Patterns:**
- Validate dataclass invariants in `__post_init__()` and raise `ValueError` with domain-specific messages. Planned examples include `Timestamp` rejecting negative nanoseconds in `src/mosaic/core/frames.py`, `FrameId` rejecting blank values, `Quaternion` rejecting non-unit rotations, and `CameraIntrinsics` rejecting invalid dimensions.
- Use `pytest.raises(..., match="...")` to assert validation error messages in tests such as `tests/core/test_frames_and_poses.py`, `tests/core/test_observations.py`, `tests/platforms/test_camera_rig.py`, and `tests/agents/test_queries.py`.
- Use `KeyError` for missing registry or lookup entries, such as `PlatformRegistry.get()` and `CameraRig.camera()` in planned `src/mosaic/platforms/` modules.
- For protocol stubs, raise `NotImplementedError` in method bodies so accidental direct calls fail loudly, as planned in `src/mosaic/slam/protocol.py` and `src/mosaic/fusion/protocol.py`.

## Logging

**Framework:** console / none detected

**Patterns:**
- No logging library or logging configuration is currently present in `pyproject.toml` or `src/mosaic/`.
- Prefer returning typed diagnostics mappings over logging side effects. Planned APIs return diagnostics through `SplatSlamUpdate.diagnostics` in `src/mosaic/slam/protocol.py`, `FusionResult.diagnostics` in `src/mosaic/fusion/protocol.py`, and benchmark artifacts in `src/mosaic/evaluation/runner.py`.
- Avoid `print()` in library code. Use `print()` only in manual verification commands documented in plans, not in implementation files.

## Comments

**When to Comment:**
- Prefer self-explanatory typed dataclasses and validation logic over inline comments.
- Add comments only for non-obvious coordinate-frame conventions, posterior/uncertainty semantics, backend isolation constraints, or agent-facing representation tradeoffs.
- Do not copy large explanatory text from `docs/` into implementation modules; keep docs in `docs/argus-migration-plan.md` and `docs/superpowers/specs/2026-05-18-agent-friendly-representation-design.md`.

**JSDoc/TSDoc:**
- Not applicable. This is a Python package.
- Python docstrings are not currently used in `src/mosaic/__init__.py`. Add docstrings only when they clarify public API contracts or coordinate conventions that type hints cannot express.

## Function Design

**Size:**
- Keep functions small and single-purpose. Planned implementation functions are generally simple constructors, validators, converters, or deterministic strategy methods.
- Move repeated test setup into private helper factories like `_observation()`, `_intrinsics()`, and `_splat()` in test files rather than duplicating large object constructors.

**Parameters:**
- Use typed parameters everywhere. Planned tests and modules use explicit return annotations such as `def test_package_version_is_exposed() -> None`, `def from_seconds(cls, seconds: float) -> Self`, and `def process(self, observation: MultiViewObservation) -> SplatSlamUpdate`.
- Prefer immutable tuples for fixed-size geometric data and sequences: `tuple[float, float, float]`, `tuple[CameraObservation, ...]`, `tuple[GaussianSplat, ...]`.
- Use `Mapping[str, str]` or `Mapping[str, MetricValue]` for metadata/diagnostics inputs, then freeze internally with `MappingProxyType`.

**Return Values:**
- Return immutable dataclasses or tuples from library APIs. Planned examples include `Pixel`, `SplatSlamUpdate`, `FusionResult`, `BenchmarkArtifact`, `RegressionResult`, and `SplatQueryResult`.
- Avoid mutating caller-owned objects. Planned `SplatMap.with_splats()` returns a new `SplatMap`; `ProvenancePreservingFusion.fuse()` returns a new fused map.
- Use explicit conversion helpers such as `as_tuple()` and `as_dict()` for stable serialization boundaries.

## Module Design

**Exports:**
- Maintain explicit `__all__` lists in every public package module. Planned `src/mosaic/__init__.py`, `src/mosaic/core/__init__.py`, `src/mosaic/splats/__init__.py`, `src/mosaic/slam/__init__.py`, `src/mosaic/platforms/__init__.py`, `src/mosaic/fusion/__init__.py`, `src/mosaic/evaluation/__init__.py`, and `src/mosaic/agents/__init__.py` all use `__all__`.
- Keep root exports in `src/mosaic/__init__.py` stable and covered by `tests/test_public_api.py`.
- Expose stable library primitives from package roots (`mosaic.core`, `mosaic.splats`, `mosaic.slam`) while keeping implementation details in submodules.

**Barrel Files:**
- Use package `__init__.py` files as barrel files for stable public APIs.
- Do not create broad wildcard imports. Import each public symbol explicitly and list it in `__all__`.
- Root-level `mosaic` exports should only include stable public APIs, not private helpers such as `_observation()` or `_snapshot_metrics()`.

## CI-like Checks

- No `.github/workflows/`, GitLab CI, pre-commit config, tox, nox, or Makefile is detected.
- Current configured package metadata is only in `pyproject.toml`; it declares Python `>=3.12`, no dependencies, and `uv_build` as the build backend.
- Planned quality checks are command-line pytest invocations using `uv run pytest ... -q` from `/home/prannayag/pragnition/robotics/mosaic`.
- Add CI in the future around the same commands once the test suite exists; avoid inventing a different local-vs-CI test entry point.

## Quality Gaps

- `src/mosaic/__init__.py` currently exposes only `hello() -> str`; planned public API and version exports are not implemented yet.
- No tests currently exist under `/home/prannayag/pragnition/robotics/mosaic/tests`; all test patterns are defined in plan documents under `docs/superpowers/plans/`.
- No formatter, linter, type checker, coverage, or CI configuration is currently committed.
- `README.md` is empty, so implementation conventions currently live in planning documents rather than user-facing project documentation.

---

*Convention analysis: 2026-05-18*
