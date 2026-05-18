<!-- refreshed: 2026-05-18 -->
# Architecture

**Analysis Date:** 2026-05-18

## System Overview

```text
┌─────────────────────────────────────────────────────────────┐
│                    Public Python Package                     │
│                  `src/mosaic/__init__.py`                    │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                  Minimal Implemented Surface                 │
│        `src/mosaic/__init__.py` exposes `hello()` only        │
│        `src/mosaic/py.typed` marks package as typed           │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 Planned Headless SLAM Library                │
├──────────────┬──────────────┬──────────────┬────────────────┤
│ Core Types   │ Splat State  │ SLAM Backend │ Dataset Replay │
│ `core/`      │ `splats/`    │ `slam/`      │ `datasets/`    │
└──────┬───────┴──────┬───────┴──────┬───────┴────────┬───────┘
       │              │              │                │
       ▼              ▼              ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│             Planned Extension Seams / Consumers              │
├──────────────┬──────────────┬──────────────┬────────────────┤
│ Platforms    │ Fusion       │ Evaluation   │ Agents         │
│ `platforms/` │ `fusion/`    │ `evaluation/`│ `agents/`      │
└──────────────┴──────────────┴──────────────┴────────────────┘
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

**Overall:** Headless typed Python package with planned layered contracts.

**Key Characteristics:**
- Keep Mosaic as a library-first package under `src/mosaic/`; avoid UI, WebSocket, ROS, simulator, or demo orchestration concerns in the core package.
- Use small typed contracts as the architectural boundary between core geometry, splat state, SLAM backends, datasets, platforms, fusion, evaluation, and agents.
- Keep CUDA-heavy or research-code SLAM backends behind lifecycle protocols instead of coupling core types to one implementation.
- Keep robot embodiment details behind platform and camera-rig contracts; do not put quadruped, UGV, humanoid, or simulator assumptions inside `mosaic.core` or `mosaic.slam`.
- Keep agent-facing posterior APIs thin and deterministic; do not expose raw full splat maps directly to agent consumers by default.

## Layers

**Implemented Package Layer:**
- Purpose: Provide the current installable `mosaic` package.
- Location: `src/mosaic/`
- Contains: `src/mosaic/__init__.py` and `src/mosaic/py.typed`.
- Depends on: Standard Python only.
- Used by: Any import of `mosaic` after package installation or `PYTHONPATH=src`.

**Project Configuration Layer:**
- Purpose: Define package metadata and build behavior.
- Location: `pyproject.toml`
- Contains: Project name `mosaic`, version `0.1.0`, Python requirement `>=3.12`, and `uv_build` backend.
- Depends on: `uv_build>=0.10.10,<0.11.0` for builds.
- Used by: `uv`, packaging tools, editable installs, and future test commands.

**Planned Core Geometry Layer:**
- Purpose: Own frames, timestamps, poses, transforms, camera intrinsics/extrinsics, image buffers, camera observations, and multi-view observations.
- Location: `src/mosaic/core/` planned in `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`.
- Contains: Planned `frames.py`, `poses.py`, `cameras.py`, and `observations.py`.
- Depends on: Standard library dataclasses, typing, and validation logic.
- Used by: Planned `src/mosaic/datasets/`, `src/mosaic/splats/`, `src/mosaic/slam/`, `src/mosaic/platforms/`, `src/mosaic/evaluation/`, and `src/mosaic/agents/`.

**Planned Splat State Layer:**
- Purpose: Own Gaussian primitive contracts and immutable splat-map snapshots.
- Location: `src/mosaic/splats/` planned in `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`.
- Contains: Planned `primitives.py` and `maps.py`.
- Depends on: Planned `mosaic.core.FrameId` and typed primitive validation.
- Used by: Planned `src/mosaic/slam/`, `src/mosaic/fusion/`, `src/mosaic/evaluation/`, and `src/mosaic/agents/`.

**Planned SLAM Backend Layer:**
- Purpose: Own backend capability metadata, lifecycle protocol, tracking/map-update results, diagnostics, snapshots, reset behavior, and a deterministic reference backend.
- Location: `src/mosaic/slam/` planned in `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`.
- Contains: Planned `protocol.py` and `fake_backend.py`.
- Depends on: Planned `mosaic.core`, `mosaic.datasets`, and `mosaic.splats` contracts.
- Used by: Planned evaluation harnesses, integration tests, and future real Gaussian splatting backends.

**Planned Dataset Replay Layer:**
- Purpose: Represent deterministic multi-view sequences for backend ingestion and tests.
- Location: `src/mosaic/datasets/` planned in `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`.
- Contains: Planned `replay.py`.
- Depends on: Planned `mosaic.core` observation and timestamp types.
- Used by: Planned `mosaic.slam` backend contract tests and `mosaic.evaluation` scenarios.

**Planned Platform Layer:**
- Purpose: Describe robot-neutral camera rigs, embodiment metadata, frame trees, and platform registries.
- Location: `src/mosaic/platforms/` planned in `docs/superpowers/plans/2026-05-18-platform-camera-rig-layer.md`.
- Contains: Planned `types.py`, `registry.py`, and `presets.py`.
- Depends on: Planned `mosaic.core` camera and pose types.
- Used by: Planned datasets, SLAM configuration, evaluation scenarios, and downstream robot integrations.

**Planned Fusion Layer:**
- Purpose: Combine immutable `SplatMap` snapshots through posterior-aware protocols with provenance-rich diagnostics.
- Location: `src/mosaic/fusion/` planned in `docs/superpowers/plans/2026-05-18-posterior-aware-splat-fusion.md`.
- Contains: Planned `protocol.py` and `strategies.py`.
- Depends on: Planned `mosaic.splats.SplatMap` and `mosaic.core.FrameId`.
- Used by: Multi-camera, multi-session, and multi-robot map composition flows.

**Planned Evaluation Layer:**
- Purpose: Provide deterministic metrics, synthetic scenarios, benchmark artifacts, and regression gates.
- Location: `src/mosaic/evaluation/` planned in `docs/superpowers/plans/2026-05-18-evaluation-regression-harness.md`.
- Contains: Planned `metrics.py`, `scenarios.py`, `runner.py`, and `regression.py`.
- Depends on: Planned `mosaic.datasets`, `mosaic.slam`, and `mosaic.splats`.
- Used by: CI, backend regression checks, and future backend comparison workflows.

**Planned Agent Layer:**
- Purpose: Expose bounded deterministic posterior queries, scene summaries, uncertainty summaries, and provenance summaries for agent consumers.
- Location: `src/mosaic/agents/` planned in `docs/superpowers/plans/2026-05-18-agent-posterior-query-seam.md` and `docs/superpowers/specs/2026-05-18-agent-friendly-representation-design.md`.
- Contains: Planned `queries.py` and `posteriors.py`.
- Depends on: Planned `mosaic.splats.SplatMap` and future layered belief graph memory contracts.
- Used by: Agentic planners and downstream consumers that need representation posteriors without raw dense geometry dumps.

## Data Flow

### Current Import Path

1. Python imports package root (`src/mosaic/__init__.py:1`).
2. Caller invokes placeholder `hello()` (`src/mosaic/__init__.py:1`).
3. Function returns the static string from package root (`src/mosaic/__init__.py:2`).

### Planned Splat SLAM Request Path

1. Dataset replay yields ordered multi-view observations from planned `src/mosaic/datasets/replay.py`.
2. Core contracts validate frames, timestamps, poses, intrinsics, image buffers, and multi-view consistency in planned `src/mosaic/core/`.
3. A backend implementing the planned `src/mosaic/slam/protocol.py` lifecycle ingests observations and produces tracking state, map updates, uncertainty, and diagnostics.
4. Splat primitives and immutable snapshots are represented by planned `src/mosaic/splats/primitives.py` and `src/mosaic/splats/maps.py`.
5. Evaluation reads backend updates and snapshots through planned `src/mosaic/evaluation/` metrics and regression gates.
6. Agent-facing posterior queries read bounded views of snapshots through planned `src/mosaic/agents/` contracts.

### Planned Platform Configuration Flow

1. Platform presets or registries create robot-neutral rig descriptions in planned `src/mosaic/platforms/presets.py` and `src/mosaic/platforms/registry.py`.
2. Camera rigs produce frame, pose, and intrinsic metadata using planned `mosaic.core` types.
3. Dataset replay and SLAM backend configuration consume rig metadata without depending on robot SDKs.

### Planned Posterior Fusion Flow

1. One or more immutable `SplatMap` snapshots enter planned `src/mosaic/fusion/protocol.py` as a fusion input.
2. Fusion validates common frame compatibility and source provenance.
3. A strategy in planned `src/mosaic/fusion/strategies.py` returns a fused snapshot plus diagnostics; occupancy-grid union assumptions stay out of the API.

**State Management:**
- Current package state is stateless; `src/mosaic/__init__.py` has no mutable module-level state.
- Planned state containers should be immutable dataclasses for geometry, observations, splats, maps, results, metrics, and query outputs.
- Planned backend runtime state belongs behind `src/mosaic/slam/protocol.py` lifecycle implementations, not in global package variables.

## Key Abstractions

**Frame and Time Contracts:**
- Purpose: Provide shared coordinate-frame and timestamp semantics across cameras, platforms, datasets, and backends.
- Examples: Planned `src/mosaic/core/frames.py`, `src/mosaic/core/poses.py`.
- Pattern: Frozen value objects with validation.

**Camera and Observation Contracts:**
- Purpose: Represent pinhole intrinsics, camera observations, image buffers, and multi-view observation batches.
- Examples: Planned `src/mosaic/core/cameras.py`, `src/mosaic/core/observations.py`.
- Pattern: Typed dataclasses with shape and consistency validation.

**Splat Map Snapshot:**
- Purpose: Represent a Gaussian-splat map state at a stable point in the backend lifecycle.
- Examples: Planned `src/mosaic/splats/primitives.py`, `src/mosaic/splats/maps.py`.
- Pattern: Immutable snapshot container with explicit frame and provenance metadata.

**Backend Lifecycle Protocol:**
- Purpose: Decouple Mosaic core from real CUDA/native/research Gaussian splatting backends.
- Examples: Planned `src/mosaic/slam/protocol.py`, `src/mosaic/slam/fake_backend.py`.
- Pattern: `typing.Protocol` plus contract tests and deterministic reference implementation.

**Camera Rig / Platform Description:**
- Purpose: Keep robot embodiment and camera layout metadata separate from SLAM and dataset logic.
- Examples: Planned `src/mosaic/platforms/types.py`, `src/mosaic/platforms/registry.py`, `src/mosaic/platforms/presets.py`.
- Pattern: Robot-neutral dataclasses plus registry lookup.

**Fusion Protocol:**
- Purpose: Combine splat-map snapshots while preserving uncertainty and provenance.
- Examples: Planned `src/mosaic/fusion/protocol.py`, `src/mosaic/fusion/strategies.py`.
- Pattern: Protocol over immutable snapshots returning result objects with diagnostics.

**Evaluation Artifacts:**
- Purpose: Make backend quality and regression checks deterministic and machine-readable.
- Examples: Planned `src/mosaic/evaluation/metrics.py`, `src/mosaic/evaluation/runner.py`, `src/mosaic/evaluation/regression.py`.
- Pattern: Typed metric objects and JSON-ready artifacts.

**Agent Posterior View:**
- Purpose: Give agent consumers bounded, deterministic views of splat posterior state.
- Examples: Planned `src/mosaic/agents/queries.py`, `src/mosaic/agents/posteriors.py`.
- Pattern: Tool/query contracts over snapshots, not LLM provider integration.

## Entry Points

**Package Import:**
- Location: `src/mosaic/__init__.py`
- Triggers: `import mosaic` or `from mosaic import hello`.
- Responsibilities: Currently exposes a placeholder `hello()` function only.

**Package Build Metadata:**
- Location: `pyproject.toml`
- Triggers: Packaging/build tools such as `uv`, `pip`, and `uv_build`.
- Responsibilities: Defines package name, version, Python requirement, and build backend.

**Architecture Planning Sources:**
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

**What happens:** CUDA, native library, or research-backend dependencies leak into core geometry, camera, splat, or dataset modules.
**Why it's wrong:** It makes pure-Python tests, import-time reliability, and backend substitution harder.
**Do this instead:** Keep backend-specific runtime code behind the planned lifecycle seam in `src/mosaic/slam/protocol.py` and use `src/mosaic/slam/fake_backend.py` for deterministic tests.

### Mixing robot embodiment with camera calibration

**What happens:** Quadruped, UGV, humanoid, or simulator assumptions get embedded in core frames, poses, camera intrinsics, or SLAM backend code.
**Why it's wrong:** It prevents the same Splat SLAM core from serving multiple robotic platforms.
**Do this instead:** Put embodiment metadata and camera rig descriptions in planned `src/mosaic/platforms/types.py`, `src/mosaic/platforms/registry.py`, and `src/mosaic/platforms/presets.py`.

### Exposing raw dense splat state as the agent API

**What happens:** Agent consumers inspect full splat maps, point clouds, or dense map dumps directly.
**Why it's wrong:** It couples agent behavior to low-level representation details and makes bounded deterministic tool outputs harder.
**Do this instead:** Expose scene summaries, local spatial queries, uncertainty summaries, and provenance summaries through planned `src/mosaic/agents/queries.py` and `src/mosaic/agents/posteriors.py`.

### Using occupancy-grid union assumptions for splat fusion

**What happens:** Multi-map fusion is modeled as classic occupancy union and loses uncertainty/provenance semantics.
**Why it's wrong:** Gaussian splatting posterior fusion needs explicit uncertainty, source, and frame compatibility handling.
**Do this instead:** Use planned posterior-aware fusion contracts in `src/mosaic/fusion/protocol.py` and deterministic reference strategies in `src/mosaic/fusion/strategies.py`.

## Error Handling

**Strategy:** Current implemented code has no explicit error handling beyond normal Python behavior; planned modules should validate dataclass construction and raise `ValueError` for invalid domain values.

**Patterns:**
- Validate typed value objects at construction time in planned files such as `src/mosaic/core/frames.py`, `src/mosaic/core/poses.py`, and `src/mosaic/core/cameras.py`.
- Validate collection invariants such as duplicate camera IDs, empty replay sequences, empty splat maps, and frame mismatches in planned modules.
- Return typed status/result objects for backend lifecycle and fusion outcomes in planned `src/mosaic/slam/protocol.py` and `src/mosaic/fusion/protocol.py`.
- Preserve diagnostics as structured mappings instead of free-form strings in planned backend, fusion, and evaluation result types.

## Cross-Cutting Concerns

**Logging:** Not implemented. Future backend lifecycle and evaluation code should keep diagnostics in typed result objects and only add logging at integration boundaries.

**Validation:** Current package has no domain validation. Planned contracts in `src/mosaic/core/`, `src/mosaic/splats/`, `src/mosaic/platforms/`, `src/mosaic/fusion/`, `src/mosaic/evaluation/`, and `src/mosaic/agents/` should validate public dataclass inputs on construction.

**Authentication:** Not applicable. Mosaic is currently a local Python library with no network server or external service boundary.

**Serialization:** Not implemented. Planned evaluation artifacts in `src/mosaic/evaluation/runner.py` should produce JSON-ready metric outputs; avoid adding serialization requirements to core data objects unless needed by tests or artifacts.

**Testing Boundary:** No `tests/` directory is currently present. Planned modules should add colocated domain-specific test directories under `tests/core/`, `tests/datasets/`, `tests/splats/`, `tests/slam/`, `tests/platforms/`, `tests/fusion/`, `tests/evaluation/`, and `tests/agents/` as described in `docs/superpowers/plans/`.

## Notable Gaps

- The implemented package currently contains only `src/mosaic/__init__.py` and `src/mosaic/py.typed`; the intended `src/mosaic/core/`, `src/mosaic/splats/`, `src/mosaic/slam/`, `src/mosaic/datasets/`, `src/mosaic/platforms/`, `src/mosaic/fusion/`, `src/mosaic/evaluation/`, and `src/mosaic/agents/` namespaces are not present.
- `pyproject.toml` has no runtime dependencies and no test configuration; planned pytest configuration appears in `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`.
- `src/mosaic/__init__.py` exposes `hello()` rather than a package version or public Mosaic API exports.
- No backend protocol, deterministic fake backend, splat-map state, camera model, dataset replay, evaluation harness, or agent posterior query implementation exists yet.
- `README.md` is effectively empty, so architectural guidance currently lives in `docs/argus-migration-plan.md` and `docs/superpowers/` rather than top-level user documentation.

---

*Architecture analysis: 2026-05-18*
