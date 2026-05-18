# Codebase Structure

**Analysis Date:** 2026-05-18

## Directory Layout

```text
/home/prannayag/pragnition/robotics/mosaic/
├── pyproject.toml                         # Python package metadata and build backend
├── .python-version                        # Python version pin: 3.12
├── README.md                              # Empty top-level README placeholder
├── docs/                                  # Architecture and implementation planning documents
│   ├── argus-migration-plan.md            # Clean-room Mosaic architecture and milestones
│   └── superpowers/                       # Generated plans/specs for future implementation phases
│       ├── plans/                         # Step-by-step implementation plans
│       └── specs/                         # Design specifications
├── outputs/                               # Research/reference notes
│   └── arna-2506-17462-replication.md     # ARNA replication notes for agent-friendly representation work
├── src/                                   # Python source tree
│   └── mosaic/                            # Installable Mosaic package
│       ├── __init__.py                    # Current package root with placeholder `hello()`
│       └── py.typed                       # PEP 561 typed-package marker
└── .planning/                             # GSD planning artifacts
    └── codebase/                          # Codebase map documents
        ├── ARCHITECTURE.md                # Architecture map
        └── STRUCTURE.md                   # Structure map
```

## Directory Purposes

**Repository Root:**
- Purpose: Holds package metadata, version pinning, documentation, source, research outputs, and planning artifacts.
- Contains: `pyproject.toml`, `.python-version`, `README.md`, `docs/`, `outputs/`, `src/`, and `.planning/`.
- Key files: `pyproject.toml`, `.python-version`, `README.md`.

**`src/`:**
- Purpose: Source-layout root for the installable Python package.
- Contains: `src/mosaic/`.
- Key files: `src/mosaic/__init__.py`, `src/mosaic/py.typed`.

**`src/mosaic/`:**
- Purpose: Current Mosaic Python package namespace.
- Contains: Package root module and typed marker only.
- Key files: `src/mosaic/__init__.py`, `src/mosaic/py.typed`.

**`docs/`:**
- Purpose: Stores architectural direction and implementation planning documents.
- Contains: `docs/argus-migration-plan.md` and `docs/superpowers/`.
- Key files: `docs/argus-migration-plan.md`.

**`docs/superpowers/plans/`:**
- Purpose: Stores task-by-task implementation plans for planned Mosaic architecture slices.
- Contains: Plans for Splat SLAM core, platform layer, posterior-aware fusion, evaluation harness, agent posterior query seam, and agent-friendly representation.
- Key files: `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`, `docs/superpowers/plans/2026-05-18-platform-camera-rig-layer.md`, `docs/superpowers/plans/2026-05-18-posterior-aware-splat-fusion.md`, `docs/superpowers/plans/2026-05-18-evaluation-regression-harness.md`, `docs/superpowers/plans/2026-05-18-agent-posterior-query-seam.md`, `docs/superpowers/plans/2026-05-18-agent-friendly-representation.md`.

**`docs/superpowers/specs/`:**
- Purpose: Stores design specifications that inform future implementation plans.
- Contains: Agent-friendly representation design.
- Key files: `docs/superpowers/specs/2026-05-18-agent-friendly-representation-design.md`.

**`outputs/`:**
- Purpose: Stores research outputs and reference notes.
- Contains: ARNA replication notes used as context for agent-friendly representation design.
- Key files: `outputs/arna-2506-17462-replication.md`.

**`.planning/codebase/`:**
- Purpose: Stores generated codebase maps used by GSD planning and execution commands.
- Contains: Architecture and structure maps for this run.
- Key files: `.planning/codebase/ARCHITECTURE.md`, `.planning/codebase/STRUCTURE.md`.

## Key File Locations

**Entry Points:**
- `src/mosaic/__init__.py`: Current package import surface; defines `hello() -> str` and returns a static greeting.
- `pyproject.toml`: Packaging/build entry point for the `mosaic` Python project.

**Configuration:**
- `pyproject.toml`: Defines project name `mosaic`, version `0.1.0`, Python requirement `>=3.12`, empty runtime dependencies, and `uv_build` build backend.
- `.python-version`: Pins local Python version to `3.12`.
- `src/mosaic/py.typed`: Marks `mosaic` as a typed Python package for PEP 561 tooling.

**Core Logic:**
- `src/mosaic/__init__.py`: Only implemented source file at present.
- `docs/argus-migration-plan.md`: Defines target core module structure and architecture milestones.
- `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`: Defines planned first concrete source modules under `src/mosaic/core/`, `src/mosaic/datasets/`, `src/mosaic/splats/`, and `src/mosaic/slam/`.

**Testing:**
- Not detected: no `tests/` directory currently exists.
- Planned tests are specified in `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`, `docs/superpowers/plans/2026-05-18-platform-camera-rig-layer.md`, `docs/superpowers/plans/2026-05-18-posterior-aware-splat-fusion.md`, `docs/superpowers/plans/2026-05-18-evaluation-regression-harness.md`, and `docs/superpowers/plans/2026-05-18-agent-posterior-query-seam.md`.

**Architecture Planning:**
- `docs/argus-migration-plan.md`: Primary architecture source for clean-room Argus-to-Mosaic migration and intended package shape.
- `docs/superpowers/specs/2026-05-18-agent-friendly-representation-design.md`: Primary design source for the future agent-facing representation architecture.

## Naming Conventions

**Files:**
- Python package modules use lowercase snake_case names: `src/mosaic/__init__.py`, planned `src/mosaic/core/frames.py`, planned `src/mosaic/slam/fake_backend.py`.
- Documentation files use lowercase kebab-case with dates for plans/specs: `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`.
- Codebase map files use uppercase markdown names: `.planning/codebase/ARCHITECTURE.md`, `.planning/codebase/STRUCTURE.md`.

**Directories:**
- Source namespaces use lowercase plural domain names for feature areas: planned `src/mosaic/datasets/`, `src/mosaic/splats/`, `src/mosaic/platforms/`, `src/mosaic/agents/`.
- Tests should mirror source namespaces under `tests/`: planned `tests/core/`, `tests/datasets/`, `tests/splats/`, `tests/slam/`, `tests/platforms/`, `tests/fusion/`, `tests/evaluation/`, `tests/agents/`.
- Planning documents are grouped by artifact type: `docs/superpowers/plans/` for plans and `docs/superpowers/specs/` for specs.

## Where to Add New Code

**New Splat SLAM Core Feature:**
- Primary code: `src/mosaic/core/`, `src/mosaic/datasets/`, `src/mosaic/splats/`, and `src/mosaic/slam/` as specified by `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`.
- Tests: `tests/core/`, `tests/datasets/`, `tests/splats/`, `tests/slam/`, plus package-level tests such as `tests/test_public_api.py`.
- Public exports: `src/mosaic/__init__.py` and each namespace `__init__.py` should expose stable API objects only.

**New Core Geometry/Camera Module:**
- Implementation: `src/mosaic/core/`.
- Put frame and timestamp identifiers in `src/mosaic/core/frames.py`.
- Put translations, quaternions, poses, and transforms in `src/mosaic/core/poses.py`.
- Put camera intrinsics/projection logic in `src/mosaic/core/cameras.py`.
- Put image buffers, camera observations, and multi-view observation batches in `src/mosaic/core/observations.py`.
- Tests: `tests/core/`.

**New Dataset Replay Module:**
- Implementation: `src/mosaic/datasets/replay.py`.
- Use this namespace for deterministic in-memory sequences and future dataset loaders.
- Tests: `tests/datasets/`.

**New Gaussian Splat/Map Module:**
- Implementation: `src/mosaic/splats/`.
- Put primitive Gaussian state in `src/mosaic/splats/primitives.py`.
- Put immutable map snapshots and map-level invariants in `src/mosaic/splats/maps.py`.
- Tests: `tests/splats/`.

**New SLAM Backend Integration:**
- Implementation: `src/mosaic/slam/`.
- Put protocol, capabilities, result types, lifecycle contracts, and statuses in `src/mosaic/slam/protocol.py`.
- Put deterministic in-memory reference backend in `src/mosaic/slam/fake_backend.py`.
- Keep real CUDA/native/research backends behind the protocol; do not add backend-specific imports to `src/mosaic/core/` or `src/mosaic/splats/`.
- Tests: `tests/slam/`, especially backend lifecycle contract tests.

**New Robot Platform or Camera Rig Support:**
- Implementation: `src/mosaic/platforms/`.
- Put embodiment and camera-rig contracts in `src/mosaic/platforms/types.py`.
- Put lookup/registration behavior in `src/mosaic/platforms/registry.py`.
- Put built-in representative rigs in `src/mosaic/platforms/presets.py`.
- Tests: `tests/platforms/`.

**New Fusion Feature:**
- Implementation: `src/mosaic/fusion/`.
- Put fusion input/result/protocol contracts in `src/mosaic/fusion/protocol.py`.
- Put deterministic reference fusion strategies in `src/mosaic/fusion/strategies.py`.
- Tests: `tests/fusion/`.

**New Evaluation Feature:**
- Implementation: `src/mosaic/evaluation/`.
- Put metric result types and metric functions in `src/mosaic/evaluation/metrics.py`.
- Put deterministic synthetic scenarios in `src/mosaic/evaluation/scenarios.py`.
- Put benchmark execution and artifact writing in `src/mosaic/evaluation/runner.py`.
- Put regression gate checks in `src/mosaic/evaluation/regression.py`.
- Tests: `tests/evaluation/`.

**New Agent-Facing Posterior Feature:**
- Implementation: `src/mosaic/agents/`.
- Put query and response contracts in `src/mosaic/agents/queries.py`.
- Put splat posterior view behavior in `src/mosaic/agents/posteriors.py`.
- Keep LLM provider, ROS, Habitat, or natural-language orchestration out of this namespace.
- Tests: `tests/agents/`.

**Utilities:**
- Shared helpers: Prefer domain-owned private helpers inside the relevant module first, such as `src/mosaic/core/poses.py` or `src/mosaic/evaluation/runner.py`.
- Cross-domain utility modules: Add only after repeated use across multiple namespaces; keep them under `src/mosaic/` with an explicit domain name rather than a vague `utils.py`.

## Special Directories

**`src/`:**
- Purpose: Source-layout root for installable Python package.
- Generated: No.
- Committed: Yes.

**`src/mosaic/`:**
- Purpose: Python package namespace for Mosaic.
- Generated: No.
- Committed: Yes.

**`docs/superpowers/`:**
- Purpose: Implementation plans and specs generated/managed by planning workflow.
- Generated: Yes, by planning workflow.
- Committed: Yes.

**`outputs/`:**
- Purpose: Research outputs and paper replication notes.
- Generated: Yes, by research/analysis workflow.
- Committed: Yes.

**`.planning/`:**
- Purpose: GSD planning and codebase map artifacts.
- Generated: Yes.
- Committed: Not determined from filesystem alone; present in working tree.

**`.git/`:**
- Purpose: Git repository metadata.
- Generated: Yes, by Git.
- Committed: No.

## Current Structure Gaps

- `src/mosaic/core/` is not present; add it before implementing frames, timestamps, poses, cameras, or observations.
- `src/mosaic/datasets/` is not present; add it before implementing deterministic replay.
- `src/mosaic/splats/` is not present; add it before implementing Gaussian primitives or splat-map snapshots.
- `src/mosaic/slam/` is not present; add it before implementing backend protocols or deterministic fake backend.
- `src/mosaic/platforms/` is not present; add it before implementing camera rigs or platform registries.
- `src/mosaic/fusion/` is not present; add it before implementing posterior-aware map fusion.
- `src/mosaic/evaluation/` is not present; add it before implementing metrics, scenarios, runner, or regression gates.
- `src/mosaic/agents/` is not present; add it before implementing agent posterior query APIs.
- `tests/` is not present; add test directories in parallel with the first real source modules.
- `README.md` contains no usable project documentation; keep architectural source of truth in `docs/argus-migration-plan.md` until README content is intentionally added.

---

*Structure analysis: 2026-05-18*
