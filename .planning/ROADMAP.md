# Roadmap: Mosaic

## Overview

Mosaic v1 delivers a typed, headless Python library foundation for splat-native robotic SLAM contracts and agent-friendly posterior access. The former `splat-slam-foundation` worktree has now been merged into the main checkout: current source includes core/datasets/platforms/slam/splats plus `fusion`, `evaluation`, and `agents` modules, including the SplatMap-backed `SplatPosteriorView`; `uv run pytest -q` reports 73 passing tests.

The roadmap now treats that merged main-checkout implementation as the Phase 1 code baseline. Later phases no longer duplicate landed modules; they harden the remaining gaps: README/release-facing documentation, coordinate/artifact semantics, backend registry metadata, deeper fusion diagnostics, richer evaluation artifacts and failure classification, posterior uncertainty/determinism hardening, ARNA-informed representation memories, and release readiness. Real 3DGS backends, ROS, Habitat, UI, and LLM integrations remain deferred until these contracts and regression gates exist.

## Phases

**Phase Numbering:**

- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Merged Foundation Baseline Completion** - Finish the merged baseline by documenting and validating the now-main implementation, including initial fusion, evaluation, and agent posterior APIs. (completed 2026-05-18)
- [x] **Phase 2: Coordinate and Artifact Hardening** - Make pose, frame, covariance, timestamp, and versioned artifact semantics explicit and tested. (completed 2026-05-18)
- [x] **Phase 3: Backend Registry and Contracts** - Define backend metadata, availability checks, and lifecycle contract coverage without heavy dependency leakage. (completed 2026-05-19)
- [x] **Phase 4: Fusion Diagnostics and Semantics Hardening** - Extend the initial fusion seam with explicit uncertainty/conflict diagnostics and anti-occupancy-grid tests. (completed 2026-05-19)
- [x] **Phase 5: Evaluation Metric and Failure Gate Hardening** - Extend the initial evaluation harness with richer metrics, failure classification, and regression gates before real backend integration. (completed 2026-05-19)
- [x] **Phase 6: Agent Posterior View Hardening** - Extend the landed SplatPosteriorView with richer bounded posterior summaries, uncertainty semantics, and determinism coverage. (completed 2026-05-21)
- [x] **Phase 7: Representation Memories and Tools** - Add ARNA-informed memory contracts and deterministic tool families for agent-friendly representation access. (completed 2026-05-21)
- [x] **Phase 8: Documentation and Release Readiness** - Document implemented APIs, deferred integrations, examples, contributor policy, and release boundaries. (completed 2026-05-21)

## Phase Details

### Phase 1: Merged Foundation Baseline Completion

**Goal**: Users can install, import, test, and understand the merged Mosaic package baseline from the main checkout.
**Depends on**: Nothing (first phase)
**Requirements**: BASE-01, BASE-02, BASE-03, BASE-04, FUSE-01, FUSE-03, EVAL-01, EVAL-03, AGNT-01, AGNT-03
**Success Criteria** (what must be TRUE):

  1. User can work from the main checkout and find the merged implementation in the Mosaic package.
  2. User can import supported public APIs for core, datasets, splats, SLAM, platforms, initial fusion, initial evaluation, and agent posterior APIs from documented package surfaces.
  3. User can run the main-checkout test workflow and see the merged suite pass at or above the observed 73-test coverage.
  4. User can call initial `FusionInput`/`ProvenancePreservingFusion`, synthetic benchmark artifact writing, regression gate checks, provider-free agent query contract types, and `SplatPosteriorView` local/summary/provenance queries without heavy runtime dependencies.
  5. User can read the README and understand Mosaic's library-first scope, fake-backend boundary, install/test commands, v1 module map, and which initial modules still need hardening.

**Plans**: 4 plans
Plans:

- [x] 01-01-PLAN.md — Document and verify the merged main-checkout package baseline.
- [x] 01-02-PLAN.md — Validate initial fusion protocol and provenance-preserving reference strategy.
- [x] 01-03-PLAN.md — Validate deterministic evaluation scenarios, benchmark artifacts, and initial regression gates.
- [x] 01-04-PLAN.md — Validate provider-free bounded agent posterior query contracts.

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

**Plans**: 4 plans
Plans:
**Wave 1**

- [x] 02-01-PLAN.md — Harden coordinate semantics and pose transform operations.
- [x] 02-02-PLAN.md — Harden Gaussian covariance layout and edge-case validation.

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 02-03-PLAN.md — Add v1 artifact envelopes for core, observations, splats, and maps.

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 02-04-PLAN.md — Add backend/evaluation artifact round trips and benchmark distinction tests.

### Phase 3: Backend Registry and Contracts

**Goal**: Users can register, inspect, availability-check, and contract-test SLAM backends without importing CUDA/native dependencies into core modules.
**Depends on**: Phase 2
**Requirements**: BACK-01, BACK-02, BACK-03, BACK-04
**Success Criteria** (what must be TRUE):

  1. User can inspect backend metadata including name, version, capabilities, parameters, dependencies, and out-of-process status.
  2. User can check backend availability and receive unavailable-dependency diagnostics without loading heavy optional packages.
  3. User can run the same backend contract tests against any registered backend implementation.
  4. User can verify lifecycle behavior for reset, process, snapshot, lost tracking, not-initialized behavior, diagnostics, and deterministic replay.

**Plans**: 3 plans
Plans:
**Wave 1**

- [x] 03-01-PLAN.md — Add backend descriptors, availability checks, and factory registry.

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 03-02-PLAN.md — Add reusable backend lifecycle contract helpers.

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 03-03-PLAN.md — Wire deterministic backend and benchmark compatibility coverage through the new contract seam.

### Phase 4: Fusion Diagnostics and Semantics Hardening

**Goal**: Users can trust the initial fusion seam as a splat-native protocol with explicit provenance, uncertainty, conflict, and non-occupancy-grid semantics.
**Depends on**: Phase 3
**Requirements**: FUSE-02, FUSE-04
**Success Criteria** (what must be TRUE):

  1. User can inspect fusion results for provenance, source-map diagnostics, uncertainty/conflict summaries, and machine-readable status beyond simple source/splat counts.
  2. User can run tests that explicitly reject occupancy-grid union assumptions and verify provenance-preserving splat behavior.
  3. User can see documented boundaries explaining that the reference strategy concatenates/preserves splats for contract tests and does not claim real Gaussian optimization quality.

**Plans**: 3 plans
Plans:
**Wave 1**

- [x] 04-01-PLAN.md — Define typed fusion diagnostic summaries and the expanded FusionResult contract.

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 04-02-PLAN.md — Populate ProvenancePreservingFusion diagnostics and anti-grid conflict behavior.

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 04-03-PLAN.md — Lock README fusion boundary language and run full phase verification.

### Phase 5: Evaluation Metric and Failure Gate Hardening

**Goal**: Users can evaluate deterministic backend behavior and regression failures before any real 3DGS backend integration is attempted.
**Depends on**: Phase 4
**Requirements**: EVAL-02, EVAL-04, EVAL-05
**Success Criteria** (what must be TRUE):

  1. User can inspect metrics for splat counts, tracking/lifecycle status, trajectory consistency hooks, map-quality hooks, and agent-query stability hooks.
  2. User can consume benchmark JSON/JSONL artifacts containing scenario data, backend metadata, metrics, diagnostics, and failure classification.
  3. User can use regression gates that distinguish lifecycle, pose/trajectory, map/fusion, and agent-query failures before real backend work begins.
  4. User can verify real 3DGS backend integration is still blocked until these evaluation gates exist and pass.

**Plans**: 4 plans
Plans:
**Wave 1**

- [x] 05-01-PLAN.md — Add typed metric families and deterministic evaluation metric constructors.

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 05-02-PLAN.md — Enrich benchmark artifacts with scenario summaries, diagnostics mirrors, and JSONL output.

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 05-03-PLAN.md — Add gate-derived failure taxonomy and evaluation-readiness helper.

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 05-04-PLAN.md — Publish Phase 5 exports and machine-check the real-backend integration block.

### Phase 6: Agent Posterior View Hardening

**Goal**: Agent consumers can rely on richer bounded posterior questions over splat snapshots through provider-free Python contracts.
**Depends on**: Phase 5
**Requirements**: AGNT-02, AGNT-04
**Success Criteria** (what must be TRUE):

  1. User can request local spatial views, scene/map summaries, uncertainty summaries, and provenance summaries over actual `SplatMap` snapshots without receiving raw full map dumps by default.
  2. User can run determinism tests showing repeated local, summary, uncertainty, and provenance queries against fixed snapshots return stable results.
  3. User can inspect documented boundaries between landed `SplatPosteriorView` local/summary/provenance behavior and richer future representation-memory queries.

**Plans**: 3 plans
Plans:
**Wave 1**

- [x] 06-01-PLAN.md — Add bounded local query results and descriptive uncertainty summaries.

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 06-02-PLAN.md — Add exact repeated-query determinism coverage for all posterior view query families.
- [x] 06-03-PLAN.md — Publish Phase 6 exports and README boundary language.

### Phase 7: Representation Memories and Tools

**Goal**: Agent consumers can use deterministic representation-memory contracts and tool facades for perception, navigation, coordination, belief/provenance, and memory/context queries.
**Depends on**: Phase 6
**Requirements**: REPR-01, REPR-02, REPR-03, REPR-04, REPR-05, REPR-06, REPR-07, REPR-08
**Success Criteria** (what must be TRUE):

  1. User can model typed IDs, entity kinds, relation kinds, evidence references, source metadata, query families, claims, conflicts, confidence, status, timestamps, and staleness transitions.
  2. User can query spatial/raster, scene graph, text, belief/provenance, and commitment memories through typed in-memory contracts.
  3. User can call a deterministic tool facade for one query in each family: perception, navigation, coordination, belief/provenance, and memory/context.
  4. User can run scenario tests for conflicting robot reports, stale claims, frontier/traversability queries, blocked-path explanations, and ARNA-style memory ablations.

**Plans**: 5 plans
Plans:
**Wave 1**

- [x] 07-01-PLAN.md — Define foundational representation-memory contracts and memory-family records.

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 07-02-PLAN.md — Add belief claims, visible conflicts, opaque evidence, and stale transitions.

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 07-03-PLAN.md — Add aggregate representation memory, immutable update helpers, and named bounded queries.

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 07-04-PLAN.md — Publish Phase 7 symbols through public API barrels.
- [x] 07-05-PLAN.md — Add evaluation-facing representation scenario and ablation coverage.

### Phase 8: Documentation and Release Readiness

**Goal**: Users and contributors can understand exactly what v1 implements, what remains deferred, how to run the library, and how to extend it without violating backend boundaries.
**Depends on**: Phase 7
**Requirements**: DOCS-01, DOCS-02, DOCS-03
**Success Criteria** (what must be TRUE):

  1. User can read public docs that distinguish implemented foundation APIs from planned real backend, ROS, Habitat, UI, and LLM integrations.
  2. User can follow a minimal end-to-end example using deterministic replay, fake backend, splat snapshot, evaluation artifact, and agent posterior query.
  3. Contributor can find dependency policy, optional extras guidance, test commands, and the rule that heavy backends stay behind registry/adapter seams.

**Plans**: 3 plans
Plans:
**Wave 1**

- [x] 08-01-PLAN.md — Rewrite README as the concise Mosaic v1 foundation orientation and README contract gate.
- [x] 08-02-PLAN.md — Add dedicated API and golden-path example docs with split-doc contract tests.

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 08-03-PLAN.md — Add contributor policy and final release-readiness doc gates.

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Merged Foundation Baseline Completion | 4/4 | Complete   | 2026-05-18 |
| 2. Coordinate and Artifact Hardening | 4/4 | Complete   | 2026-05-18 |
| 3. Backend Registry and Contracts | 4/4 | Complete   | 2026-05-19 |
| 4. Fusion Diagnostics and Semantics Hardening | 3/3 | Complete   | 2026-05-19 |
| 5. Evaluation Metric and Failure Gate Hardening | 4/4 | Complete   | 2026-05-19 |
| 6. Agent Posterior View Hardening | 3/3 | Complete   | 2026-05-21 |
| 7. Representation Memories and Tools | 5/5 | Complete   | 2026-05-21 |
| 8. Documentation and Release Readiness | 3/3 | Complete   | 2026-05-21 |

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

## Main Checkout Evidence

Observed on 2026-05-18 in `/home/prannayag/pragnition/robotics/mosaic` after merging the Mosaic worktree changes:

- Recent commits include `Merge branch 'mosaic-splat-slam-foundation'`, `feat: expose agent posterior api`, `feat: add splat posterior view`, `feat: add agent posterior query contracts`, `feat: expose evaluation harness api`, `feat: add benchmark regression gates`, and `feat: expose splat fusion api`.
- Test command `uv run pytest -q` reported `73 passed in 0.29s`.
- Implemented modules include `src/mosaic/core/`, `src/mosaic/datasets/`, `src/mosaic/splats/`, `src/mosaic/slam/`, `src/mosaic/platforms/`, `src/mosaic/fusion/`, `src/mosaic/evaluation/`, and `src/mosaic/agents/`.
- Public exports now include `SplatPosteriorView`, `LocalRadiusQuery`, `PosteriorSummary`, `ProvenanceSummary`, and `SplatQueryResult` from the root package surface.
- Remaining gaps include README/release documentation, richer evaluation metrics/failure classes, explicit fusion uncertainty/conflict semantics, coordinate/artifact hardening, backend registry metadata, posterior uncertainty summaries, and broader repeated-query determinism coverage.
