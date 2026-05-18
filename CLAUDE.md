<!-- GSD:project-start source:PROJECT.md -->
## Project

**Mosaic**

Mosaic is a typed, headless Python library for 3D Gaussian Splatting SLAM over multi-view moving cameras on robotic systems including quadrupeds, UGVs, humanoids, and custom rigs. It provides pure-Python contracts for frames, poses, cameras, observations, splat maps, backend lifecycles, platform camera rigs, evaluation, fusion, and agent-facing representation posteriors.

The long-term direction is to make LLM/LVLM agents first-class consumers of the representation: agents should perceive, inspect belief, reason over uncertainty/provenance, and act through bounded deterministic APIs rather than reading raw splats or dense map dumps.

**Core Value:** Mosaic must provide stable typed representation contracts that let robotic SLAM backends, evaluation tools, platform rigs, and agent-friendly posterior APIs evolve independently without coupling the library to one robot, simulator, LLM provider, or CUDA-heavy backend.

### Constraints

- **Tech stack**: Python 3.12+, `uv`, pure-Python foundation modules, `pytest` — keeps the core importable without CUDA/native dependencies.
- **Repository state**: Main checkout and active migration worktree differ substantially — use the worktree as baseline context, but commit planning artifacts in the main checkout unless explicitly working in the worktree.
- **Backend boundary**: Real 3DGS/CUDA/research backends must stay behind protocols, registries, optional dependencies, and eventual isolation boundaries — prevents fragile runtime dependencies from contaminating core contracts.
- **Frame semantics**: Coordinate frames, pose direction, handedness, optical frame conventions, and timestamp precision must be nailed down early — downstream fusion, evaluation, and agent queries will otherwise disagree silently.
- **Evaluation before backend integration**: Real backend work waits until deterministic artifacts and regression gates exist — avoids integrating a backend without a way to tell whether behavior improved or regressed.
- **Agent boundary**: Agent APIs return bounded typed outputs with evidence/provenance, not raw full splat maps or provider-specific prompts — protects the representation layer from LLM/runtime churn.
<!-- GSD:project-end -->

<!-- GSD:stack-start source:codebase/STACK.md -->
## Technology Stack

## Languages
- Python 3.12+ - The package requires Python `>=3.12` in `pyproject.toml:9`; local development pins `3.12` in `.python-version:1`.
- Markdown - Planning and research documentation in `docs/argus-migration-plan.md` and `outputs/arna-2506-17462-replication.md`.
- TOML - Project/build metadata in `pyproject.toml`.
## Runtime
- CPython 3.12 - Implied by `.python-version` and `requires-python = ">=3.12"` in `pyproject.toml`.
- Headless Python library runtime - The design explicitly avoids UI/WebSocket/demo concerns in `docs/argus-migration-plan.md:12` and focuses on `src/mosaic/` as a library package.
- uv is implied by the build backend dependency `uv_build>=0.10.10,<0.11.0` in `pyproject.toml:13`.
- Lockfile: missing. No `uv.lock`, `poetry.lock`, `Pipfile.lock`, or requirements lock file is present under `/home/prannayag/pragnition/robotics/mosaic`.
## Frameworks
- No application framework detected - `src/mosaic/__init__.py` currently exposes only `hello() -> str`.
- Planned package architecture is a typed Python library for 3D Gaussian Splatting SLAM, with proposed namespaces listed in `docs/argus-migration-plan.md:91-103`.
- Not detected - no `pytest`, `unittest`, `hypothesis`, `tox`, `nox`, or test configuration is declared in `pyproject.toml`.
- Testing discipline is planned but not implemented: unit tests, backend contract tests, dataset replay tests, platform tests, evaluation tests, and agent API tests are described in `docs/argus-migration-plan.md:159-166`.
- `uv_build>=0.10.10,<0.11.0` - Build backend declared in `pyproject.toml:12-14`.
- `py.typed` - Package marker at `src/mosaic/py.typed` declares type information for downstream type checkers.
- No formatter/linter/type-checker configuration detected - no Ruff, Black, mypy, Pyright, or pytest settings are currently present in `pyproject.toml` or sibling config files.
## Key Dependencies
- None currently declared - `dependencies = []` in `pyproject.toml:10`.
- Future Gaussian Splatting SLAM dependencies are intentionally undecided; `docs/argus-migration-plan.md:170` states the Gaussian splatting backend choice is not selected.
- `uv_build>=0.10.10,<0.11.0` - Required only for packaging/building via `pyproject.toml:13`.
- No runtime infrastructure dependencies are installed or declared in the project metadata.
- Numerical arrays/tensors: no `numpy`, `torch`, `jax`, or `scipy` dependency is present, despite planned pose, camera, splat, and posterior data structures in `docs/argus-migration-plan.md:109-127`.
- Computer vision / geometry: no `opencv-python`, `open3d`, `trimesh`, `viser`, `rerun-sdk`, `gsplat`, `nerfstudio`, or COLMAP wrapper is present.
- Robotics/simulation: no ROS, Habitat, MuJoCo, Isaac, or robot SDK dependency is present; robot platform abstractions are planned in `docs/argus-migration-plan.md:129-137` but intentionally not tied to Go2/MuJoCo in `docs/argus-migration-plan.md:84-87`.
- Agent/LLM integration: no OpenAI, Anthropic, LangChain, or tool-calling SDK is present; agent posterior APIs are planned as a thin seam in `docs/argus-migration-plan.md:149-157`.
## Configuration
- Python version is configured by `.python-version` with value `3.12`.
- Package metadata is configured in `pyproject.toml` with project name `mosaic`, version `0.1.0`, README `README.md`, and author metadata.
- No `.env` or `.env.*` files are present at repository root from the safe existence-only scan.
- No runtime environment variables are required by current code in `src/mosaic/__init__.py`.
- `pyproject.toml` is the only detected build configuration file.
- Build backend: `uv_build` from `pyproject.toml:14`.
- Source package root: `src/mosaic/`.
- Typed package marker: `src/mosaic/py.typed`.
## Platform Requirements
- Python 3.12 or newer.
- A build frontend compatible with PEP 517 and `uv_build`.
- No GPU/CUDA requirement exists in the current package metadata.
- Future backend work may require CUDA/native libraries; `docs/argus-migration-plan.md:30-36` calls out CUDA-heavy and crash-prone Gaussian splatting backends as a design concern.
- Deployment target not detected.
- Current shape is a distributable Python library package, not a service, CLI, notebook, web app, or robot runtime deployment.
- Future production-like deployments are expected to consume Mosaic headlessly from downstream robot, dataset, evaluation, or agent systems rather than from code currently in this repository.
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

## Naming Patterns
- Use a `src/` package layout. Runtime code lives under `src/mosaic/`; the current package files are `src/mosaic/__init__.py` and `src/mosaic/py.typed`.
- Use snake_case module names for planned Python modules such as `src/mosaic/core/frames.py`, `src/mosaic/core/poses.py`, `src/mosaic/core/observations.py`, `src/mosaic/datasets/replay.py`, `src/mosaic/slam/fake_backend.py`, and `src/mosaic/evaluation/regression.py`.
- Use package `__init__.py` files as public export surfaces, following the planned files `src/mosaic/core/__init__.py`, `src/mosaic/splats/__init__.py`, `src/mosaic/slam/__init__.py`, `src/mosaic/platforms/__init__.py`, `src/mosaic/fusion/__init__.py`, `src/mosaic/evaluation/__init__.py`, and `src/mosaic/agents/__init__.py`.
- Keep the marker file `src/mosaic/py.typed` present so type checkers treat Mosaic as a typed package.
- Use snake_case for functions and methods. Existing code uses `hello()` in `src/mosaic/__init__.py`; planned APIs use names like `from_seconds()`, `as_seconds()`, `as_tuple()`, `with_splats()`, `process()`, `snapshot()`, `reset()`, `default_platform_registry()`, `quadruped_front_rig()`, `synthetic_forward_sequence()`, and `check_regression_gates()`.
- Use leading underscores for test helper factories and module-private helpers, such as `_pose()`, `_intrinsics()`, `_rgb()`, `_observation()`, `_splat()`, `_mount()`, and `_snapshot_metrics()` in the planned `tests/` and `src/mosaic/` modules.
- Use verb phrases for operations (`project`, `register`, `fuse`, `query_local`, `write_benchmark_artifact`) and noun phrases for constructors/factories that return domain objects (`quadruped_front_rig`, `synthetic_forward_sequence`).
- Use snake_case for local variables and attributes: `camera_id`, `map_frame`, `splat_count`, `source_map_count`, `frame_count`, `mean_opacity`, `estimated_pose`.
- Prefer explicit domain names over abbreviations: use `timestamp`, `observation`, `intrinsics`, `provenance`, `diagnostics`, and `fusion_input`.
- Use uppercase enum members in `StrEnum` classes, with lower-case string values: `TrackingState.TRACKING = "tracking"`, `FusionStatus.FUSED = "fused"`, `AgentQueryKind.LOCAL_GEOMETRY = "local_geometry"` in the planned modules.
- Use PascalCase for public classes, dataclasses, protocols, and enums: `Timestamp`, `FrameId`, `Pose3`, `CameraIntrinsics`, `GaussianSplat`, `SplatMap`, `SplatSlamBackend`, `PlatformRegistry`, `FusionInput`, `MetricResult`, `SplatPosteriorView`.
- Use `Protocol` for pluggable interfaces such as `MultiViewSequence`, `SplatSlamBackend`, and `SplatFusionStrategy` in planned files under `src/mosaic/datasets/`, `src/mosaic/slam/`, and `src/mosaic/fusion/`.
- Use descriptive type aliases where payload types repeat, such as `MetricValue = bool | int | float | str` and `FusionMetricValue = bool | int | float | str` in the planned protocol modules.
## Code Style
- No formatter configuration is currently committed. There is no `.ruff.toml`, `ruff.toml`, `pyproject.toml` formatter section, `.prettierrc`, or `biome.json` under `/home/prannayag/pragnition/robotics/mosaic`.
- Use standard Python 3.12 formatting: 4-space indentation, blank lines between top-level definitions, and readable wrapping for long imports or constructor calls.
- Keep line lengths practical. The plans contain some long import lines, but new implementation should prefer parenthesized multi-line imports and constructor calls in files such as `src/mosaic/__init__.py` and test modules.
- Prefer deterministic JSON formatting for artifacts: planned `src/mosaic/evaluation/runner.py` uses `json.dumps(..., indent=2, sort_keys=True) + "\n"`.
- No linting tool is configured in `pyproject.toml`; `ruff`, `flake8`, `pylint`, `mypy`, and `pyright` configuration files are not detected.
- Treat the planned tests as the current quality gate until lint/type tooling is added.
- Because `src/mosaic/py.typed` exists, keep public APIs typed and type-checker-friendly even without an enforced type-check command.
## Import Organization
- Use package imports rooted at `mosaic`, not relative imports. Planned examples consistently use `from mosaic.core import FrameId`, `from mosaic.splats import SplatMap`, and `from mosaic.slam import DeterministicSplatBackend`.
- `pyproject.toml` currently has no `[tool.pytest.ini_options]`; planned test setup adds `pythonpath = ["src"]` so tests can import `mosaic` without installing the package.
## Error Handling
- Validate dataclass invariants in `__post_init__()` and raise `ValueError` with domain-specific messages. Planned examples include `Timestamp` rejecting negative nanoseconds in `src/mosaic/core/frames.py`, `FrameId` rejecting blank values, `Quaternion` rejecting non-unit rotations, and `CameraIntrinsics` rejecting invalid dimensions.
- Use `pytest.raises(..., match="...")` to assert validation error messages in tests such as `tests/core/test_frames_and_poses.py`, `tests/core/test_observations.py`, `tests/platforms/test_camera_rig.py`, and `tests/agents/test_queries.py`.
- Use `KeyError` for missing registry or lookup entries, such as `PlatformRegistry.get()` and `CameraRig.camera()` in planned `src/mosaic/platforms/` modules.
- For protocol stubs, raise `NotImplementedError` in method bodies so accidental direct calls fail loudly, as planned in `src/mosaic/slam/protocol.py` and `src/mosaic/fusion/protocol.py`.
## Logging
- No logging library or logging configuration is currently present in `pyproject.toml` or `src/mosaic/`.
- Prefer returning typed diagnostics mappings over logging side effects. Planned APIs return diagnostics through `SplatSlamUpdate.diagnostics` in `src/mosaic/slam/protocol.py`, `FusionResult.diagnostics` in `src/mosaic/fusion/protocol.py`, and benchmark artifacts in `src/mosaic/evaluation/runner.py`.
- Avoid `print()` in library code. Use `print()` only in manual verification commands documented in plans, not in implementation files.
## Comments
- Prefer self-explanatory typed dataclasses and validation logic over inline comments.
- Add comments only for non-obvious coordinate-frame conventions, posterior/uncertainty semantics, backend isolation constraints, or agent-facing representation tradeoffs.
- Do not copy large explanatory text from `docs/` into implementation modules; keep docs in `docs/argus-migration-plan.md` and `docs/superpowers/specs/2026-05-18-agent-friendly-representation-design.md`.
- Not applicable. This is a Python package.
- Python docstrings are not currently used in `src/mosaic/__init__.py`. Add docstrings only when they clarify public API contracts or coordinate conventions that type hints cannot express.
## Function Design
- Keep functions small and single-purpose. Planned implementation functions are generally simple constructors, validators, converters, or deterministic strategy methods.
- Move repeated test setup into private helper factories like `_observation()`, `_intrinsics()`, and `_splat()` in test files rather than duplicating large object constructors.
- Use typed parameters everywhere. Planned tests and modules use explicit return annotations such as `def test_package_version_is_exposed() -> None`, `def from_seconds(cls, seconds: float) -> Self`, and `def process(self, observation: MultiViewObservation) -> SplatSlamUpdate`.
- Prefer immutable tuples for fixed-size geometric data and sequences: `tuple[float, float, float]`, `tuple[CameraObservation, ...]`, `tuple[GaussianSplat, ...]`.
- Use `Mapping[str, str]` or `Mapping[str, MetricValue]` for metadata/diagnostics inputs, then freeze internally with `MappingProxyType`.
- Return immutable dataclasses or tuples from library APIs. Planned examples include `Pixel`, `SplatSlamUpdate`, `FusionResult`, `BenchmarkArtifact`, `RegressionResult`, and `SplatQueryResult`.
- Avoid mutating caller-owned objects. Planned `SplatMap.with_splats()` returns a new `SplatMap`; `ProvenancePreservingFusion.fuse()` returns a new fused map.
- Use explicit conversion helpers such as `as_tuple()` and `as_dict()` for stable serialization boundaries.
## Module Design
- Maintain explicit `__all__` lists in every public package module. Planned `src/mosaic/__init__.py`, `src/mosaic/core/__init__.py`, `src/mosaic/splats/__init__.py`, `src/mosaic/slam/__init__.py`, `src/mosaic/platforms/__init__.py`, `src/mosaic/fusion/__init__.py`, `src/mosaic/evaluation/__init__.py`, and `src/mosaic/agents/__init__.py` all use `__all__`.
- Keep root exports in `src/mosaic/__init__.py` stable and covered by `tests/test_public_api.py`.
- Expose stable library primitives from package roots (`mosaic.core`, `mosaic.splats`, `mosaic.slam`) while keeping implementation details in submodules.
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
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

## System Overview
```text
```
## Component Responsibilities
| Component | Responsibility | File |
|-----------|----------------|------|
| Package root | Current importable Mosaic package; contains a placeholder `hello()` function. | `src/mosaic/__init__.py` |
| Typed marker | Declares the package as PEP 561 typed for downstream type checkers. | `src/mosaic/py.typed` |
| Project metadata | Defines the installable Python package, Python version requirement, and build backend. | `pyproject.toml` |
| Migration plan | Defines the intended clean-room architecture for Mosaic as a 3D Gaussian Splatting SLAM Python library. | `docs/argus-migration-plan.md` |
| Splat SLAM core plan | Specifies the intended core modules for frames, poses, cameras, observations, splats, replay, and backend lifecycle. | `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md` |
| Platform camera rig plan | Specifies the intended robot-agnostic camera rig and platform seam. | `docs/superpowers/plans/2026-05-18-platform-camera-rig-layer.md` |
| Posterior fusion plan | Specifies the intended posterior-aware splat-map fusion seam. | `docs/superpowers/plans/2026-05-18-posterior-aware-splat-fusion.md` |
| Evaluation harness plan | Specifies the intended deterministic metrics, scenarios, benchmark runner, and regression gates. | `docs/superpowers/plans/2026-05-18-evaluation-regression-harness.md` |
| Agent posterior query plan | Specifies the intended thin agent-facing posterior query seam. | `docs/superpowers/plans/2026-05-18-agent-posterior-query-seam.md` |
| Agent representation design | Defines the target layered belief graph plus agent tool memory architecture. | `docs/superpowers/specs/2026-05-18-agent-friendly-representation-design.md` |
## Pattern Overview
- Keep Mosaic as a library-first package under `src/mosaic/`; avoid UI, WebSocket, ROS, simulator, or demo orchestration concerns in the core package.
- Use small typed contracts as the architectural boundary between core geometry, splat state, SLAM backends, datasets, platforms, fusion, evaluation, and agents.
- Keep CUDA-heavy or research-code SLAM backends behind lifecycle protocols instead of coupling core types to one implementation.
- Keep robot embodiment details behind platform and camera-rig contracts; do not put quadruped, UGV, humanoid, or simulator assumptions inside `mosaic.core` or `mosaic.slam`.
- Keep agent-facing posterior APIs thin and deterministic; do not expose raw full splat maps directly to agent consumers by default.
## Layers
- Purpose: Provide the current installable `mosaic` package.
- Location: `src/mosaic/`
- Contains: `src/mosaic/__init__.py` and `src/mosaic/py.typed`.
- Depends on: Standard Python only.
- Used by: Any import of `mosaic` after package installation or `PYTHONPATH=src`.
- Purpose: Define package metadata and build behavior.
- Location: `pyproject.toml`
- Contains: Project name `mosaic`, version `0.1.0`, Python requirement `>=3.12`, and `uv_build` backend.
- Depends on: `uv_build>=0.10.10,<0.11.0` for builds.
- Used by: `uv`, packaging tools, editable installs, and future test commands.
- Purpose: Own frames, timestamps, poses, transforms, camera intrinsics/extrinsics, image buffers, camera observations, and multi-view observations.
- Location: `src/mosaic/core/` planned in `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`.
- Contains: Planned `frames.py`, `poses.py`, `cameras.py`, and `observations.py`.
- Depends on: Standard library dataclasses, typing, and validation logic.
- Used by: Planned `src/mosaic/datasets/`, `src/mosaic/splats/`, `src/mosaic/slam/`, `src/mosaic/platforms/`, `src/mosaic/evaluation/`, and `src/mosaic/agents/`.
- Purpose: Own Gaussian primitive contracts and immutable splat-map snapshots.
- Location: `src/mosaic/splats/` planned in `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`.
- Contains: Planned `primitives.py` and `maps.py`.
- Depends on: Planned `mosaic.core.FrameId` and typed primitive validation.
- Used by: Planned `src/mosaic/slam/`, `src/mosaic/fusion/`, `src/mosaic/evaluation/`, and `src/mosaic/agents/`.
- Purpose: Own backend capability metadata, lifecycle protocol, tracking/map-update results, diagnostics, snapshots, reset behavior, and a deterministic reference backend.
- Location: `src/mosaic/slam/` planned in `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`.
- Contains: Planned `protocol.py` and `fake_backend.py`.
- Depends on: Planned `mosaic.core`, `mosaic.datasets`, and `mosaic.splats` contracts.
- Used by: Planned evaluation harnesses, integration tests, and future real Gaussian splatting backends.
- Purpose: Represent deterministic multi-view sequences for backend ingestion and tests.
- Location: `src/mosaic/datasets/` planned in `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`.
- Contains: Planned `replay.py`.
- Depends on: Planned `mosaic.core` observation and timestamp types.
- Used by: Planned `mosaic.slam` backend contract tests and `mosaic.evaluation` scenarios.
- Purpose: Describe robot-neutral camera rigs, embodiment metadata, frame trees, and platform registries.
- Location: `src/mosaic/platforms/` planned in `docs/superpowers/plans/2026-05-18-platform-camera-rig-layer.md`.
- Contains: Planned `types.py`, `registry.py`, and `presets.py`.
- Depends on: Planned `mosaic.core` camera and pose types.
- Used by: Planned datasets, SLAM configuration, evaluation scenarios, and downstream robot integrations.
- Purpose: Combine immutable `SplatMap` snapshots through posterior-aware protocols with provenance-rich diagnostics.
- Location: `src/mosaic/fusion/` planned in `docs/superpowers/plans/2026-05-18-posterior-aware-splat-fusion.md`.
- Contains: Planned `protocol.py` and `strategies.py`.
- Depends on: Planned `mosaic.splats.SplatMap` and `mosaic.core.FrameId`.
- Used by: Multi-camera, multi-session, and multi-robot map composition flows.
- Purpose: Provide deterministic metrics, synthetic scenarios, benchmark artifacts, and regression gates.
- Location: `src/mosaic/evaluation/` planned in `docs/superpowers/plans/2026-05-18-evaluation-regression-harness.md`.
- Contains: Planned `metrics.py`, `scenarios.py`, `runner.py`, and `regression.py`.
- Depends on: Planned `mosaic.datasets`, `mosaic.slam`, and `mosaic.splats`.
- Used by: CI, backend regression checks, and future backend comparison workflows.
- Purpose: Expose bounded deterministic posterior queries, scene summaries, uncertainty summaries, and provenance summaries for agent consumers.
- Location: `src/mosaic/agents/` planned in `docs/superpowers/plans/2026-05-18-agent-posterior-query-seam.md` and `docs/superpowers/specs/2026-05-18-agent-friendly-representation-design.md`.
- Contains: Planned `queries.py` and `posteriors.py`.
- Depends on: Planned `mosaic.splats.SplatMap` and future layered belief graph memory contracts.
- Used by: Agentic planners and downstream consumers that need representation posteriors without raw dense geometry dumps.
## Data Flow
### Current Import Path
### Planned Splat SLAM Request Path
### Planned Platform Configuration Flow
### Planned Posterior Fusion Flow
- Current package state is stateless; `src/mosaic/__init__.py` has no mutable module-level state.
- Planned state containers should be immutable dataclasses for geometry, observations, splats, maps, results, metrics, and query outputs.
- Planned backend runtime state belongs behind `src/mosaic/slam/protocol.py` lifecycle implementations, not in global package variables.
## Key Abstractions
- Purpose: Provide shared coordinate-frame and timestamp semantics across cameras, platforms, datasets, and backends.
- Examples: Planned `src/mosaic/core/frames.py`, `src/mosaic/core/poses.py`.
- Pattern: Frozen value objects with validation.
- Purpose: Represent pinhole intrinsics, camera observations, image buffers, and multi-view observation batches.
- Examples: Planned `src/mosaic/core/cameras.py`, `src/mosaic/core/observations.py`.
- Pattern: Typed dataclasses with shape and consistency validation.
- Purpose: Represent a Gaussian-splat map state at a stable point in the backend lifecycle.
- Examples: Planned `src/mosaic/splats/primitives.py`, `src/mosaic/splats/maps.py`.
- Pattern: Immutable snapshot container with explicit frame and provenance metadata.
- Purpose: Decouple Mosaic core from real CUDA/native/research Gaussian splatting backends.
- Examples: Planned `src/mosaic/slam/protocol.py`, `src/mosaic/slam/fake_backend.py`.
- Pattern: `typing.Protocol` plus contract tests and deterministic reference implementation.
- Purpose: Keep robot embodiment and camera layout metadata separate from SLAM and dataset logic.
- Examples: Planned `src/mosaic/platforms/types.py`, `src/mosaic/platforms/registry.py`, `src/mosaic/platforms/presets.py`.
- Pattern: Robot-neutral dataclasses plus registry lookup.
- Purpose: Combine splat-map snapshots while preserving uncertainty and provenance.
- Examples: Planned `src/mosaic/fusion/protocol.py`, `src/mosaic/fusion/strategies.py`.
- Pattern: Protocol over immutable snapshots returning result objects with diagnostics.
- Purpose: Make backend quality and regression checks deterministic and machine-readable.
- Examples: Planned `src/mosaic/evaluation/metrics.py`, `src/mosaic/evaluation/runner.py`, `src/mosaic/evaluation/regression.py`.
- Pattern: Typed metric objects and JSON-ready artifacts.
- Purpose: Give agent consumers bounded, deterministic views of splat posterior state.
- Examples: Planned `src/mosaic/agents/queries.py`, `src/mosaic/agents/posteriors.py`.
- Pattern: Tool/query contracts over snapshots, not LLM provider integration.
## Entry Points
- Location: `src/mosaic/__init__.py`
- Triggers: `import mosaic` or `from mosaic import hello`.
- Responsibilities: Currently exposes a placeholder `hello()` function only.
- Location: `pyproject.toml`
- Triggers: Packaging/build tools such as `uv`, `pip`, and `uv_build`.
- Responsibilities: Defines package name, version, Python requirement, and build backend.
- Location: `docs/argus-migration-plan.md`
- Triggers: Development planning and implementation sequencing.
- Responsibilities: Defines the intended module boundaries, milestones, and constraints for the future Mosaic architecture.
## Architectural Constraints
- **Threading:** Current implemented code is single-threaded and has no background workers. Future heavy Gaussian splatting backends should be isolated behind the planned `src/mosaic/slam/protocol.py` lifecycle seam.
- **Global state:** No mutable global state is present in `src/mosaic/__init__.py`. Future registries in planned `src/mosaic/platforms/registry.py` should keep lookup state explicit and testable.
- **Circular imports:** No circular imports exist in the current implemented package because only `src/mosaic/__init__.py` is implemented.
- **Typing:** `src/mosaic/py.typed` is present; all new public modules under `src/mosaic/` should preserve typed public APIs.
- **Backend independence:** The current package has no backend dependencies in `pyproject.toml`; future `mosaic.core`, `mosaic.splats`, and protocol modules should not require CUDA/native runtime packages.
- **Clean-room boundary:** `docs/argus-migration-plan.md` directs Mosaic to borrow concepts from Argus without copying its implementation shape.
- **Headless boundary:** UI, WebSocket, ROS node, Habitat runner, simulator adapters, and demo orchestration are outside the core package boundary.
## Anti-Patterns
### Putting backend-specific code in core contracts
### Mixing robot embodiment with camera calibration
### Exposing raw dense splat state as the agent API
### Using occupancy-grid union assumptions for splat fusion
## Error Handling
- Validate typed value objects at construction time in planned files such as `src/mosaic/core/frames.py`, `src/mosaic/core/poses.py`, and `src/mosaic/core/cameras.py`.
- Validate collection invariants such as duplicate camera IDs, empty replay sequences, empty splat maps, and frame mismatches in planned modules.
- Return typed status/result objects for backend lifecycle and fusion outcomes in planned `src/mosaic/slam/protocol.py` and `src/mosaic/fusion/protocol.py`.
- Preserve diagnostics as structured mappings instead of free-form strings in planned backend, fusion, and evaluation result types.
## Cross-Cutting Concerns
## Notable Gaps
- The implemented package currently contains only `src/mosaic/__init__.py` and `src/mosaic/py.typed`; the intended `src/mosaic/core/`, `src/mosaic/splats/`, `src/mosaic/slam/`, `src/mosaic/datasets/`, `src/mosaic/platforms/`, `src/mosaic/fusion/`, `src/mosaic/evaluation/`, and `src/mosaic/agents/` namespaces are not present.
- `pyproject.toml` has no runtime dependencies and no test configuration; planned pytest configuration appears in `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`.
- `src/mosaic/__init__.py` exposes `hello()` rather than a package version or public Mosaic API exports.
- No backend protocol, deterministic fake backend, splat-map state, camera model, dataset replay, evaluation harness, or agent posterior query implementation exists yet.
- `README.md` is effectively empty, so architectural guidance currently lives in `docs/argus-migration-plan.md` and `docs/superpowers/` rather than top-level user documentation.
<!-- GSD:architecture-end -->

<!-- GSD:skills-start source:skills/ -->
## Project Skills

No project skills found. Add skills to any of: `.claude/skills/`, `.agents/skills/`, `.cursor/skills/`, `.github/skills/`, or `.codex/skills/` with a `SKILL.md` index file.
<!-- GSD:skills-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd-quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd-debug` for investigation and bug fixing
- `/gsd-execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd-profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
