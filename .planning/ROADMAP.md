# Roadmap: Mosaic

## Overview

Mosaic v1 delivers a typed, headless Python library foundation for splat-native robotic SLAM contracts and agent-friendly posterior access. A 2026-05-18 scan of `/home/prannayag/pragnition/robotics/.mosaic-worktrees/splat-slam-foundation` found the worktree has advanced beyond the original baseline: it now includes core/datasets/platforms/slam/splats plus initial `fusion`, `evaluation`, and `agents` query-contract modules, with 69 passing tests.

The roadmap now treats that expanded worktree as the Phase 1 merge baseline. Later phases no longer duplicate those initial modules; they harden the remaining gaps: coordinate/artifact semantics, backend registry metadata, deeper fusion diagnostics, richer evaluation failure classification, SplatMap-backed posterior views, ARNA-informed representation memories, and release documentation. Real 3DGS backends, ROS, Habitat, UI, and LLM integrations remain deferred until these contracts and regression gates exist.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Expanded Foundation Baseline Merge** - Stabilize and merge the active worktree, including initial fusion, evaluation, and agent-query contracts, as the public Mosaic package baseline.
- [ ] **Phase 2: Coordinate and Artifact Hardening** - Make pose, frame, covariance, timestamp, and versioned artifact semantics explicit and tested.
- [ ] **Phase 3: Backend Registry and Contracts** - Define backend metadata, availability checks, and lifecycle contract coverage without heavy dependency leakage.
- [ ] **Phase 4: Fusion Diagnostics and Semantics Hardening** - Extend the initial fusion seam with explicit uncertainty/conflict diagnostics and anti-occupancy-grid tests.
- [ ] **Phase 5: Evaluation Metric and Failure Gate Hardening** - Extend the initial evaluation harness with richer metrics, failure classification, and regression gates before real backend integration.
- [ ] **Phase 6: Agent Posterior View Implementation** - Build SplatMap-backed posterior query behavior on top of the existing provider-free query contracts.
- [ ] **Phase 7: Representation Memories and Tools** - Add ARNA-informed memory contracts and deterministic tool families for agent-friendly representation access.
- [ ] **Phase 8: Documentation and Release Readiness** - Document implemented APIs, deferred integrations, examples, contributor policy, and release boundaries.

## Phase Details

### Phase 1: Expanded Foundation Baseline Merge
**Goal**: Users can install, import, test, and understand the expanded Mosaic package baseline from the active worktree.
**Depends on**: Nothing (first phase)
**Requirements**: BASE-01, BASE-02, BASE-03, BASE-04, FUSE-01, FUSE-03, EVAL-01, EVAL-03, AGNT-01, AGNT-03
**Success Criteria** (what must be TRUE):
  1. User can work from the main checkout and find the stabilized implementation from `splat-slam-foundation` merged into the Mosaic package.
  2. User can import supported public APIs for core, datasets, splats, SLAM, platforms, initial fusion, initial evaluation, and agent query contracts from documented package surfaces.
  3. User can run the merged main-checkout test workflow and see the worktree baseline suite pass at or above the observed 69-test coverage.
  4. User can call initial `FusionInput`/`ProvenancePreservingFusion`, synthetic benchmark artifact writing, regression gate checks, and provider-free agent query contract types without heavy runtime dependencies.
  5. User can read the README and understand Mosaic's library-first scope, fake-backend boundary, install/test commands, v1 module map, and which initial modules still need hardening.
**Plans**: TBD

### Phase 2: Coordinate and Artifact Hardening
**Goal**: Users can rely on explicit coordinate, covariance, timestamp, and artifact semantics across downstream fusion and evaluation work.
**Depends on**: Phase 1
**Requirements**: SEM-01, SEM-02, SEM-03, ART-01, ART-02
**Success Criteria** (what must be TRUE):
  1. User can read and test the exact meaning of pose direction, parent/child frames, optical-frame convention, handedness, and timestamp precision.
  2. User can compose, invert, and apply core pose/camera transforms with behavior verified by tests.
  3. User can inspect Gaussian covariance layout and validity rules, including edge cases covered by tests.
  4. User can serialize and round-trip versioned JSON-ready artifacts for core values, observations, splats, maps, backend updates, and evaluation results.
  5. User can distinguish the existing benchmark artifact JSON from the broader v1 artifact schema requirements.
**Plans**: TBD

### Phase 3: Backend Registry and Contracts
**Goal**: Users can register, inspect, availability-check, and contract-test SLAM backends without importing CUDA/native dependencies into core modules.
**Depends on**: Phase 2
**Requirements**: BACK-01, BACK-02, BACK-03, BACK-04
**Success Criteria** (what must be TRUE):
  1. User can inspect backend metadata including name, version, capabilities, parameters, dependencies, and out-of-process status.
  2. User can check backend availability and receive unavailable-dependency diagnostics without loading heavy optional packages.
  3. User can run the same backend contract tests against any registered backend implementation.
  4. User can verify lifecycle behavior for reset, process, snapshot, lost tracking, not-initialized behavior, diagnostics, and deterministic replay.
**Plans**: TBD

### Phase 4: Fusion Diagnostics and Semantics Hardening
**Goal**: Users can trust the initial fusion seam as a splat-native protocol with explicit provenance, uncertainty, conflict, and non-occupancy-grid semantics.
**Depends on**: Phase 3
**Requirements**: FUSE-02, FUSE-04
**Success Criteria** (what must be TRUE):
  1. User can inspect fusion results for provenance, source-map diagnostics, uncertainty/conflict summaries, and machine-readable status beyond simple source/splat counts.
  2. User can run tests that explicitly reject occupancy-grid union assumptions and verify provenance-preserving splat behavior.
  3. User can see documented boundaries explaining that the reference strategy concatenates/preserves splats for contract tests and does not claim real Gaussian optimization quality.
**Plans**: TBD

### Phase 5: Evaluation Metric and Failure Gate Hardening
**Goal**: Users can evaluate deterministic backend behavior and regression failures before any real 3DGS backend integration is attempted.
**Depends on**: Phase 4
**Requirements**: EVAL-02, EVAL-04, EVAL-05
**Success Criteria** (what must be TRUE):
  1. User can inspect metrics for splat counts, tracking/lifecycle status, trajectory consistency hooks, map-quality hooks, and agent-query stability hooks.
  2. User can consume benchmark JSON/JSONL artifacts containing scenario data, backend metadata, metrics, diagnostics, and failure classification.
  3. User can use regression gates that distinguish lifecycle, pose/trajectory, map/fusion, and agent-query failures before real backend work begins.
  4. User can verify real 3DGS backend integration is still blocked until these evaluation gates exist and pass.
**Plans**: TBD

### Phase 6: Agent Posterior View Implementation
**Goal**: Agent consumers can ask bounded deterministic posterior questions over splat snapshots through provider-free Python contracts.
**Depends on**: Phase 5
**Requirements**: AGNT-02, AGNT-04
**Success Criteria** (what must be TRUE):
  1. User can request local spatial views, scene/map summaries, uncertainty summaries, and provenance summaries over actual `SplatMap` snapshots without receiving raw full map dumps by default.
  2. User can run determinism tests showing repeated queries against fixed snapshots return stable results.
  3. User can distinguish existing query/result dataclasses from implemented posterior view behavior.
**Plans**: TBD

### Phase 7: Representation Memories and Tools
**Goal**: Agent consumers can use deterministic representation-memory contracts and tool facades for perception, navigation, coordination, belief/provenance, and memory/context queries.
**Depends on**: Phase 6
**Requirements**: REPR-01, REPR-02, REPR-03, REPR-04, REPR-05, REPR-06, REPR-07, REPR-08
**Success Criteria** (what must be TRUE):
  1. User can model typed IDs, entity kinds, relation kinds, evidence references, source metadata, query families, claims, conflicts, confidence, status, timestamps, and staleness transitions.
  2. User can query spatial/raster, scene graph, text, belief/provenance, and commitment memories through typed in-memory contracts.
  3. User can call a deterministic tool facade for one query in each family: perception, navigation, coordination, belief/provenance, and memory/context.
  4. User can run scenario tests for conflicting robot reports, stale claims, frontier/traversability queries, blocked-path explanations, and ARNA-style memory ablations.
**Plans**: TBD

### Phase 8: Documentation and Release Readiness
**Goal**: Users and contributors can understand exactly what v1 implements, what remains deferred, how to run the library, and how to extend it without violating backend boundaries.
**Depends on**: Phase 7
**Requirements**: DOCS-01, DOCS-02, DOCS-03
**Success Criteria** (what must be TRUE):
  1. User can read public docs that distinguish implemented foundation APIs from planned real backend, ROS, Habitat, UI, and LLM integrations.
  2. User can follow a minimal end-to-end example using deterministic replay, fake backend, splat snapshot, evaluation artifact, and agent posterior query.
  3. Contributor can find dependency policy, optional extras guidance, test commands, and the rule that heavy backends stay behind registry/adapter seams.
**Plans**: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Expanded Foundation Baseline Merge | 0/TBD | Not started | - |
| 2. Coordinate and Artifact Hardening | 0/TBD | Not started | - |
| 3. Backend Registry and Contracts | 0/TBD | Not started | - |
| 4. Fusion Diagnostics and Semantics Hardening | 0/TBD | Not started | - |
| 5. Evaluation Metric and Failure Gate Hardening | 0/TBD | Not started | - |
| 6. Agent Posterior View Implementation | 0/TBD | Not started | - |
| 7. Representation Memories and Tools | 0/TBD | Not started | - |
| 8. Documentation and Release Readiness | 0/TBD | Not started | - |

## Coverage

| Requirement | Phase |
|-------------|-------|
| BASE-01 | Phase 1 |
| BASE-02 | Phase 1 |
| BASE-03 | Phase 1 |
| BASE-04 | Phase 1 |
| FUSE-01 | Phase 1 |
| FUSE-03 | Phase 1 |
| EVAL-01 | Phase 1 |
| EVAL-03 | Phase 1 |
| AGNT-01 | Phase 1 |
| AGNT-03 | Phase 1 |
| SEM-01 | Phase 2 |
| SEM-02 | Phase 2 |
| SEM-03 | Phase 2 |
| ART-01 | Phase 2 |
| ART-02 | Phase 2 |
| BACK-01 | Phase 3 |
| BACK-02 | Phase 3 |
| BACK-03 | Phase 3 |
| BACK-04 | Phase 3 |
| FUSE-02 | Phase 4 |
| FUSE-04 | Phase 4 |
| EVAL-02 | Phase 5 |
| EVAL-04 | Phase 5 |
| EVAL-05 | Phase 5 |
| AGNT-02 | Phase 6 |
| AGNT-04 | Phase 6 |
| REPR-01 | Phase 7 |
| REPR-02 | Phase 7 |
| REPR-03 | Phase 7 |
| REPR-04 | Phase 7 |
| REPR-05 | Phase 7 |
| REPR-06 | Phase 7 |
| REPR-07 | Phase 7 |
| REPR-08 | Phase 7 |
| DOCS-01 | Phase 8 |
| DOCS-02 | Phase 8 |
| DOCS-03 | Phase 8 |

**Coverage summary:**
- v1 requirements: 37 total
- Mapped to phases: 37
- Unmapped: 0

## Worktree Evidence

Observed on 2026-05-18 in `/home/prannayag/pragnition/robotics/.mosaic-worktrees/splat-slam-foundation`:

- Recent commits include `feat: expose splat fusion api`, `feat: add deterministic evaluation metrics`, `feat: add synthetic evaluation scenarios`, `feat: add slam benchmark artifacts`, `feat: add benchmark regression gates`, `feat: expose evaluation harness api`, and `feat: add agent posterior query contracts`.
- Test command `uv run --directory /home/prannayag/pragnition/robotics/.mosaic-worktrees/splat-slam-foundation pytest -q` reported `69 passed in 0.22s`.
- Implemented initial modules include `src/mosaic/fusion/`, `src/mosaic/evaluation/`, and `src/mosaic/agents/queries.py`.
- Remaining gaps include SplatMap-backed agent posterior view behavior, richer evaluation metrics/failure classes, explicit fusion uncertainty/conflict semantics, coordinate/artifact hardening, and backend registry metadata.
