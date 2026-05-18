# Roadmap: Mosaic

## Overview

Mosaic v1 delivers a typed, headless Python library foundation for splat-native robotic SLAM contracts. The roadmap starts by stabilizing the `splat-slam-foundation` worktree as the baseline package, then hardens coordinate and artifact semantics before adding backend registries, posterior-aware fusion, deterministic evaluation gates, bounded agent posterior queries, ARNA-informed representation memories, and release documentation. Real 3DGS backends, ROS, Habitat, UI, and LLM integrations remain deferred until these contracts and regression gates exist.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Foundation Baseline** - Stabilize and merge the foundation worktree as the public Mosaic package baseline.
- [ ] **Phase 2: Coordinate and Artifact Hardening** - Make pose, frame, covariance, timestamp, and JSON-ready artifact semantics explicit and tested.
- [ ] **Phase 3: Backend Registry and Contracts** - Define backend metadata, availability checks, and lifecycle contract coverage without heavy dependency leakage.
- [ ] **Phase 4: Posterior-Aware Fusion** - Add splat-native fusion protocols that preserve provenance, uncertainty, diagnostics, and frame compatibility.
- [ ] **Phase 5: Evaluation and Regression Gates** - Provide deterministic scenarios, metrics, benchmark artifacts, and failure classification before real backend integration.
- [ ] **Phase 6: Agent Posterior Query Seam** - Expose bounded deterministic posterior query contracts over splat-map snapshots without provider dependencies.
- [ ] **Phase 7: Representation Memories and Tools** - Add ARNA-informed memory contracts and deterministic tool families for agent-friendly representation access.
- [ ] **Phase 8: Documentation and Release Readiness** - Document implemented APIs, deferred integrations, examples, contributor policy, and release boundaries.

## Phase Details

### Phase 1: Foundation Baseline
**Goal**: Users can install, import, test, and understand the stabilized foundation Mosaic package from the merged baseline.
**Depends on**: Nothing (first phase)
**Requirements**: BASE-01, BASE-02, BASE-03, BASE-04
**Success Criteria** (what must be TRUE):
  1. User can work from the main checkout and find the stabilized foundation implementation from `splat-slam-foundation` merged into the Mosaic package.
  2. User can import supported public APIs for core, datasets, splats, SLAM, and platforms from documented package surfaces.
  3. User can read the README and understand Mosaic's library-first scope, fake-backend boundary, install/test commands, and v1 module map.
  4. User can run the configured test workflow in the merged main checkout and see the foundation suite pass.
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

### Phase 4: Posterior-Aware Fusion
**Goal**: Users can fuse immutable splat-map snapshots through a splat-native protocol that preserves provenance and uncertainty rather than pretending maps are occupancy grids.
**Depends on**: Phase 3
**Requirements**: FUSE-01, FUSE-02, FUSE-03, FUSE-04
**Success Criteria** (what must be TRUE):
  1. User can call a fusion protocol over immutable `SplatMap` snapshots and receive validation errors for invalid inputs or incompatible frames.
  2. User can inspect fusion results for provenance, source-map diagnostics, uncertainty/conflict summaries, and machine-readable status.
  3. User can use a deterministic reference fusion strategy for tests without claims of real Gaussian optimization quality.
  4. User can run tests that reject occupancy-grid union assumptions and verify provenance-preserving fusion behavior.
**Plans**: TBD

### Phase 5: Evaluation and Regression Gates
**Goal**: Users can evaluate deterministic backend behavior and regression failures before any real 3DGS backend integration is attempted.
**Depends on**: Phase 4
**Requirements**: EVAL-01, EVAL-02, EVAL-03, EVAL-04, EVAL-05
**Success Criteria** (what must be TRUE):
  1. User can run deterministic synthetic multi-view scenarios against the fake backend and future registered backends.
  2. User can inspect metrics for splat counts, tracking/lifecycle status, trajectory consistency hooks, map-quality hooks, and agent-query stability hooks.
  3. User can consume benchmark JSON/JSONL artifacts containing scenario data, backend metadata, metrics, diagnostics, and failure classification.
  4. User can use regression gates that distinguish lifecycle, pose/trajectory, map/fusion, and agent-query failures before real backend work begins.
**Plans**: TBD

### Phase 6: Agent Posterior Query Seam
**Goal**: Agent consumers can ask bounded deterministic posterior questions over splat snapshots through provider-free Python contracts.
**Depends on**: Phase 5
**Requirements**: AGNT-01, AGNT-02, AGNT-03, AGNT-04
**Success Criteria** (what must be TRUE):
  1. User can create typed posterior query requests and receive bounded deterministic result objects over `SplatMap` snapshots.
  2. User can request local spatial views, scene/map summaries, uncertainty summaries, and provenance summaries without receiving raw full map dumps by default.
  3. User can import and use agent-facing APIs without installing LLM SDKs, ROS, Habitat, or robot execution dependencies.
  4. User can run determinism tests showing repeated queries against fixed snapshots return stable results.
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
| 1. Foundation Baseline | 0/TBD | Not started | - |
| 2. Coordinate and Artifact Hardening | 0/TBD | Not started | - |
| 3. Backend Registry and Contracts | 0/TBD | Not started | - |
| 4. Posterior-Aware Fusion | 0/TBD | Not started | - |
| 5. Evaluation and Regression Gates | 0/TBD | Not started | - |
| 6. Agent Posterior Query Seam | 0/TBD | Not started | - |
| 7. Representation Memories and Tools | 0/TBD | Not started | - |
| 8. Documentation and Release Readiness | 0/TBD | Not started | - |

## Coverage

| Requirement | Phase |
|-------------|-------|
| BASE-01 | Phase 1 |
| BASE-02 | Phase 1 |
| BASE-03 | Phase 1 |
| BASE-04 | Phase 1 |
| SEM-01 | Phase 2 |
| SEM-02 | Phase 2 |
| SEM-03 | Phase 2 |
| ART-01 | Phase 2 |
| ART-02 | Phase 2 |
| BACK-01 | Phase 3 |
| BACK-02 | Phase 3 |
| BACK-03 | Phase 3 |
| BACK-04 | Phase 3 |
| FUSE-01 | Phase 4 |
| FUSE-02 | Phase 4 |
| FUSE-03 | Phase 4 |
| FUSE-04 | Phase 4 |
| EVAL-01 | Phase 5 |
| EVAL-02 | Phase 5 |
| EVAL-03 | Phase 5 |
| EVAL-04 | Phase 5 |
| EVAL-05 | Phase 5 |
| AGNT-01 | Phase 6 |
| AGNT-02 | Phase 6 |
| AGNT-03 | Phase 6 |
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
