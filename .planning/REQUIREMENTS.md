# Requirements: Mosaic

**Defined:** 2026-05-18
**Core Value:** Mosaic must provide stable typed representation contracts that let robotic SLAM backends, evaluation tools, platform rigs, and agent-friendly posterior APIs evolve independently without coupling the library to one robot, simulator, LLM provider, or CUDA-heavy backend.

## v1 Requirements

Requirements for the initial library-foundation release. Each maps to roadmap phases.

### Foundation Baseline

- [ ] **BASE-01**: The `splat-slam-foundation` worktree is reviewed, stabilized, and merged as the baseline Mosaic package implementation.
- [ ] **BASE-02**: Public package exports clearly expose supported foundation APIs for core, datasets, splats, SLAM, and platforms.
- [ ] **BASE-03**: The README documents Mosaic's library-first scope, fake-backend boundary, install/test commands, and v1 module map.
- [ ] **BASE-04**: The test suite from the foundation worktree runs from the merged main checkout and passes under the configured project workflow.

### Coordinate and Artifact Semantics

- [ ] **SEM-01**: Pose direction, parent/child frame meaning, camera optical-frame convention, handedness, and timestamp precision are explicitly documented and tested.
- [ ] **SEM-02**: Core pose/camera utilities include tested transform composition, inversion, and point transformation semantics needed by downstream fusion and evaluation.
- [ ] **SEM-03**: Gaussian covariance layout and validity semantics are documented and covered by edge-case tests.
- [ ] **ART-01**: Core values, observations, splats, maps, backend updates, and evaluation results have versioned JSON-ready artifact schemas.
- [ ] **ART-02**: Serialization round-trip tests cover timestamps, poses, camera observations, Gaussian splats, splat maps, and backend updates.

### Backend Contracts

- [ ] **BACK-01**: SLAM backends can be described by registry metadata including name, version, capabilities, parameters, dependency requirements, and whether they run out of process.
- [ ] **BACK-02**: Backend availability checks can report unavailable optional dependencies without importing heavy CUDA/native packages into core modules.
- [ ] **BACK-03**: Backend contract tests can be parametrized across any registered backend implementation.
- [ ] **BACK-04**: Lifecycle contract coverage includes reset, process, snapshot, lost tracking, not-initialized behavior, diagnostics, and deterministic replay.

### Posterior-Aware Fusion

- [ ] **FUSE-01**: Mosaic exposes a fusion protocol over immutable `SplatMap` snapshots with explicit input validation and frame compatibility checks.
- [ ] **FUSE-02**: Fusion results preserve provenance, source-map diagnostics, uncertainty/conflict summaries, and machine-readable status.
- [ ] **FUSE-03**: A deterministic reference fusion strategy exists for tests without claiming real Gaussian optimization quality.
- [ ] **FUSE-04**: Fusion tests reject occupancy-grid union assumptions and verify provenance-preserving behavior.

### Evaluation and Regression

- [ ] **EVAL-01**: Mosaic provides deterministic synthetic multi-view scenarios that can drive the fake backend and future registered backends.
- [ ] **EVAL-02**: Evaluation metrics cover splat counts, tracking/lifecycle status, trajectory consistency hooks, map-quality hooks, and agent-query stability hooks.
- [ ] **EVAL-03**: Benchmark runs emit stable JSON/JSONL artifacts with scenario, backend metadata, metrics, diagnostics, and failure classification.
- [ ] **EVAL-04**: Regression gates can distinguish lifecycle failures, pose/trajectory failures, map/fusion failures, and agent-query failures.
- [ ] **EVAL-05**: The evaluation harness runs before real 3DGS backend integration is attempted.

### Agent Posterior Query Seam

- [ ] **AGNT-01**: Mosaic exposes typed posterior query requests and bounded deterministic result objects over `SplatMap` snapshots.
- [ ] **AGNT-02**: Posterior queries support local spatial queries, scene/map summaries, uncertainty summaries, and provenance summaries without exposing raw full map dumps by default.
- [ ] **AGNT-03**: Agent-facing APIs are provider-free Python contracts and do not import LLM SDKs, ROS, Habitat, or robot execution dependencies.
- [ ] **AGNT-04**: Query determinism tests cover repeated calls against fixed snapshots.

### Agent-Friendly Representation Memories

- [ ] **REPR-01**: Representation contracts define typed IDs, entity kinds, relation kinds, evidence references, source metadata, and query families.
- [ ] **REPR-02**: Belief/provenance memory stores claims with confidence, status, timestamps, evidence, conflicts, and staleness transitions.
- [ ] **REPR-03**: Spatial/raster memory stores occupancy, explored/free/occupied/frontier state, traversability hints, and evidence claim links.
- [ ] **REPR-04**: Scene graph memory stores entities, regions, hazards, objects, landmarks, relations, confidence, and claim references.
- [ ] **REPR-05**: Text memory stores bounded prompt-ready notes, summaries, uncertainty notes, and source claim references.
- [ ] **REPR-06**: Commitment memory tracks tasks, route/resource reservations, robot intentions, time windows, and conflicts.
- [ ] **REPR-07**: Agent tool facade answers one deterministic query from each family: perception, navigation, coordination, belief/provenance, and memory/context.
- [ ] **REPR-08**: Scenario tests demonstrate conflicting robot reports, stale claims, frontier/traversability queries, blocked-path explanations, and ARNA-style memory ablations.

### Documentation and Release Readiness

- [ ] **DOCS-01**: Public docs distinguish implemented foundation APIs from planned real backend, ROS, Habitat, UI, and LLM integrations.
- [ ] **DOCS-02**: Public docs include a minimal end-to-end example using deterministic replay, fake backend, splat snapshot, evaluation artifact, and agent posterior query.
- [ ] **DOCS-03**: Contributor guidance explains dependency policy, optional extras, test commands, and the rule that heavy backends stay behind registry/adapter seams.

## v2 Requirements

Deferred to future releases. Tracked but not in the current roadmap.

### Real Backend Integration

- **REAL-01**: Integrate at least one real 3D Gaussian Splatting SLAM backend behind the backend registry.
- **REAL-02**: Provide an out-of-process adapter for fragile CUDA/native/research backends.
- **REAL-03**: Compare real backend artifacts against deterministic regression gates and scenario metrics.

### Real Robot and Dataset Integrations

- **DATA-01**: Add lazy readers for long multi-camera robot logs and high-rate depth/RGB streams.
- **DATA-02**: Add calibrated robot-specific platform configuration packages outside the core presets.
- **ROS-01**: Provide ROS wrappers downstream of the library API.

### Advanced Agent Runtime

- **LLM-01**: Add optional LLM/LVLM tool wrappers around deterministic Mosaic APIs.
- **ARNA-01**: Build Habitat/ARNA-style benchmark runners as optional research tooling.
- **PERCP-01**: Add real object detection, room segmentation, and splat-to-raster extraction pipelines.

### Scaling and Storage

- **IDX-01**: Add spatial indexing or acceleration structures for large splat maps.
- **DB-01**: Add persistent stores for representation memories if in-memory APIs prove insufficient.
- **DIST-01**: Add multi-robot distributed synchronization once local contracts stabilize.

## Out of Scope

Explicitly excluded from v1. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Real 3DGS backend integration | Deferred until contracts, serialization, backend registry, and regression gates exist. |
| CUDA/PyTorch/OpenCV as required dependencies | Core library must remain importable and testable without heavy backend stacks. |
| LLM/LVLM provider integration | v1 exposes deterministic Python APIs; provider wrappers can come later. |
| ROS nodes or robot command execution | Mosaic v1 is a headless library, not a robot runtime. |
| Habitat/ARNA reproduction | ARNA informs architecture, but no public implementation exists and benchmark replication is separate research scope. |
| Browser UI, WebSockets, demos | Downstream consumers can wrap the library once APIs stabilize. |
| Occupancy-grid-first map model | Mosaic's core representation is splat/posterior native. |
| Vendor-calibrated platform presets | Built-in rigs are representative fixtures, not calibrated robot packages. |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| BASE-01 | Phase 1 | Pending |
| BASE-02 | Phase 1 | Pending |
| BASE-03 | Phase 1 | Pending |
| BASE-04 | Phase 1 | Pending |
| SEM-01 | Phase 2 | Pending |
| SEM-02 | Phase 2 | Pending |
| SEM-03 | Phase 2 | Pending |
| ART-01 | Phase 2 | Pending |
| ART-02 | Phase 2 | Pending |
| BACK-01 | Phase 3 | Pending |
| BACK-02 | Phase 3 | Pending |
| BACK-03 | Phase 3 | Pending |
| BACK-04 | Phase 3 | Pending |
| FUSE-01 | Phase 4 | Pending |
| FUSE-02 | Phase 4 | Pending |
| FUSE-03 | Phase 4 | Pending |
| FUSE-04 | Phase 4 | Pending |
| EVAL-01 | Phase 5 | Pending |
| EVAL-02 | Phase 5 | Pending |
| EVAL-03 | Phase 5 | Pending |
| EVAL-04 | Phase 5 | Pending |
| EVAL-05 | Phase 5 | Pending |
| AGNT-01 | Phase 6 | Pending |
| AGNT-02 | Phase 6 | Pending |
| AGNT-03 | Phase 6 | Pending |
| AGNT-04 | Phase 6 | Pending |
| REPR-01 | Phase 7 | Pending |
| REPR-02 | Phase 7 | Pending |
| REPR-03 | Phase 7 | Pending |
| REPR-04 | Phase 7 | Pending |
| REPR-05 | Phase 7 | Pending |
| REPR-06 | Phase 7 | Pending |
| REPR-07 | Phase 7 | Pending |
| REPR-08 | Phase 7 | Pending |
| DOCS-01 | Phase 8 | Pending |
| DOCS-02 | Phase 8 | Pending |
| DOCS-03 | Phase 8 | Pending |

**Coverage:**
- v1 requirements: 37 total
- Mapped to phases: 37
- Unmapped: 0 ✓

---
*Requirements defined: 2026-05-18*
*Last updated: 2026-05-18 after initial definition*
