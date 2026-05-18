# Mosaic

## What This Is

Mosaic is a typed, headless Python library for 3D Gaussian Splatting SLAM over multi-view moving cameras on robotic systems including quadrupeds, UGVs, humanoids, and custom rigs. It provides pure-Python contracts for frames, poses, cameras, observations, splat maps, backend lifecycles, platform camera rigs, evaluation, fusion, and agent-facing representation posteriors.

The long-term direction is to make LLM/LVLM agents first-class consumers of the representation: agents should perceive, inspect belief, reason over uncertainty/provenance, and act through bounded deterministic APIs rather than reading raw splats or dense map dumps.

## Core Value

Mosaic must provide stable typed representation contracts that let robotic SLAM backends, evaluation tools, platform rigs, and agent-friendly posterior APIs evolve independently without coupling the library to one robot, simulator, LLM provider, or CUDA-heavy backend.

## Requirements

### Validated

- ✓ Current repository is an installable Python package scaffold with `src/mosaic/` and `pyproject.toml` — existing main checkout
- ✓ The active `splat-slam-foundation` worktree has implemented and tested the first foundation slice: core geometry, camera observations, splat maps, deterministic dataset replay, a fake backend lifecycle, and platform camera rigs — migration worktree baseline
- ✓ Codebase maps exist for both the main checkout and the active migration worktree — initialization mapping
- ✓ Coordinate-frame direction, timestamp precision, pose transforms, camera optical-frame projection, and covariance tuple semantics are explicit and tested — validated in Phase 02
- ✓ Versioned artifact envelopes and round-trip serializers exist for core values, observations, splat maps, backend updates, and evaluation outputs — validated in Phase 02

### Active

- [ ] Stabilize and merge the `splat-slam-foundation` worktree as the baseline library foundation.
- [ ] Add backend registry, capability metadata, availability checks, and contract-test parametrization while keeping heavy backends isolated.
- [ ] Add posterior-aware splat-map fusion seams that preserve uncertainty and provenance instead of occupancy-grid union assumptions.
- [ ] Add deterministic evaluation scenarios, metrics, benchmark artifact writing, and regression gates before integrating real 3DGS backends.
- [ ] Add a thin agent posterior query seam over splat-map snapshots.
- [ ] Add the first ARNA-informed agent-friendly representation layer: spatial/raster memory, scene graph memory, textual memory, belief/provenance memory, commitment memory, and deterministic tool APIs.
- [ ] Document the public API, fake-backend boundary, test command, and contribution path in README guidance.

### Out of Scope

- Real 3D Gaussian Splatting backend integration in v1 — deferred until contracts, serialization, and regression gates exist.
- LLM/LVLM provider integration — Mosaic v1 exposes deterministic Python APIs, not agent runtime orchestration.
- ROS nodes, robot command execution, Habitat runners, browser UI, WebSockets, or demo orchestration — downstream consumers can wrap the library later.
- Full ARNA reproduction or benchmark replication — ARNA informs memory/tool architecture, but paper-specific prompts, Habitat experiments, and GPT-4o workflows are not Mosaic v1.
- Robot-specific calibration packages — built-in platform presets are representative fixtures, not vendor-accurate calibrated models.
- Occupancy-grid-first SLAM abstractions — Mosaic's core representation remains Gaussian splat/posterior native.

## Context

Mosaic is a clean-room extraction of the useful architectural lessons from the adjacent Argus codebase, not a direct port. The Argus migration plan identifies the valuable pieces to borrow: protocol/registry patterns, backend isolation, robot platform abstraction, map-fusion strategy interfaces, contract-test discipline, deterministic metrics, and agent-friendly representation research.

The first implementation set is being built in `/home/prannayag/pragnition/robotics/.mosaic-worktrees/splat-slam-foundation`. That worktree currently has concrete `src/mosaic` modules for `core`, `datasets`, `splats`, `slam`, and `platforms`, plus 43 passing tests according to the codebase map. The main checkout still has a much smaller package surface, so planning should use the worktree as the near-term baseline while avoiding edits that interfere with the active migration agent.

The agent-friendly representation design combines the Argus layered belief graph idea with the ARNA paper's lesson that strong embodied agents rely on coordinated memory/tool views: textual memory, raster/top-down spatial memory, scene graph landmarks, reasoning/navigation tools, provenance, and commitments. Mosaic should expose these as typed local library contracts first.

The ARNA investigation found no public implementation artifacts, so Mosaic should not depend on reproducing ARNA code. The useful takeaway is architectural: synchronized memory views and deterministic tools outperform forcing an agent to reason from a monolithic raw world model.

## Constraints

- **Tech stack**: Python 3.12+, `uv`, pure-Python foundation modules, `pytest` — keeps the core importable without CUDA/native dependencies.
- **Repository state**: Main checkout and active migration worktree differ substantially — use the worktree as baseline context, but commit planning artifacts in the main checkout unless explicitly working in the worktree.
- **Backend boundary**: Real 3DGS/CUDA/research backends must stay behind protocols, registries, optional dependencies, and eventual isolation boundaries — prevents fragile runtime dependencies from contaminating core contracts.
- **Frame semantics**: Coordinate frames, pose direction, handedness, optical frame conventions, and timestamp precision must be nailed down early — downstream fusion, evaluation, and agent queries will otherwise disagree silently.
- **Evaluation before backend integration**: Real backend work waits until deterministic artifacts and regression gates exist — avoids integrating a backend without a way to tell whether behavior improved or regressed.
- **Agent boundary**: Agent APIs return bounded typed outputs with evidence/provenance, not raw full splat maps or provider-specific prompts — protects the representation layer from LLM/runtime churn.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Treat `splat-slam-foundation` worktree as the roadmap baseline | The worktree already implements the first migration slice and has tests; replanning from `main` would duplicate active work. | — Pending |
| Define v1 as the library foundation, not a real backend demo | Stable contracts, evaluation, and agent seams are prerequisites for useful backend integration. | — Pending |
| Integrate real 3DGS backends after contracts and regression gates | Backend behavior cannot be evaluated safely until serialization, metrics, and regression artifacts exist. | — Pending |
| Keep Mosaic headless and Python-library-first | UI, ROS, Habitat, and robot execution should be downstream wrappers, not core package concerns. | — Pending |
| Use ARNA as architectural evidence, not as an implementation dependency | No public ARNA code was found; the memory/tool separation principle is the portable lesson. | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-05-18 after Phase 02 completion*
