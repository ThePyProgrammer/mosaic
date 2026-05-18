# Feature Landscape

**Domain:** typed Python 3D Gaussian Splatting SLAM library with agent-friendly posterior APIs
**Project:** Mosaic
**Researched:** 2026-05-18
**Research scope:** Features dimension only, based on project planning files and active foundation worktree concerns. Planned docs are treated as intended direction, not implemented code.
**Overall confidence:** HIGH for internal v1 scope and dependency ordering; MEDIUM for broader ecosystem expectations because this pass did not perform external competitor benchmarking.

## Context Boundary

Mosaic v1 should be judged as a **library foundation**, not a product demo. The table-stakes bar is therefore not "does it run a real-time 3DGS SLAM demo?" but "can downstream real 3DGS backends, robot rigs, evaluation tools, fusion strategies, and agent-facing posterior consumers build against stable typed contracts without rewriting the substrate?"

Current repository state matters:

- The main checkout is still mostly placeholder code.
- The active `splat-slam-foundation` worktree reportedly has the first foundation slice implemented and tested: `core`, `datasets`, `splats`, `slam`, and `platforms` with 43 passing tests.
- `fusion`, `evaluation`, and `agents` are still planned seams in the worktree, not implemented packages.
- Real CUDA/native 3DGS backend integration is explicitly deferred until contracts, serialization, and regression gates exist.

## Table Stakes

Features users should expect from a v1 typed library foundation. Missing these makes Mosaic unstable or misleading even if no real backend ships yet.

| Feature | Why Expected | Complexity | Dependencies | Implementation Status Signal | Notes |
|---------|--------------|------------|--------------|------------------------------|-------|
| Typed public package surface with version export | Consumers need a stable import target and a clear package identity before building against Mosaic. | Low | `pyproject.toml`, root `mosaic.__init__` | Main: missing/placeholder. Worktree: planned/partly implemented. | Export only stable foundation types; do not advertise future modules as shipped. |
| Frame identifiers and timestamp contracts | Every pose, camera, replay, map, fusion, metric, and agent query depends on common frame/time semantics. | Medium | None | Worktree foundation has basic validation; direction semantics remain under-specified. | Must reject blank frames and negative timestamps. Prefer integer nanoseconds for exact replay. |
| Pose, translation, quaternion contracts | SLAM backends and rigs need typed camera/world relationships. | Medium | Frame IDs, timestamps | Worktree has skeletal `Pose3`; no inverse/compose/transform utilities. | v1 table stakes include construction/validation; pose math should be added only after transform direction is pinned. |
| Pinhole camera intrinsics and projection primitive | Multi-view robotic SLAM needs camera calibration shape, even for fake/replay tests. | Medium | Core geometry | Worktree has basic intrinsics/projection. | Include validation for positive dimensions/focal lengths. Add color/depth dimension alignment before external datasets. |
| Image buffer and camera observation contracts | Dataset replay, backend ingestion, and evaluation require typed observations. | Medium | Camera intrinsics, poses, timestamps | Worktree has bytes-backed immutable buffers and observations. | v1 should support color and depth payload contracts, but not high-performance tensor ingestion in core. |
| Multi-view observation grouping | The project promise is multi-view moving cameras, not single-camera-only SLAM. | Medium | Camera observation contracts | Worktree has `MultiViewObservation`. | Enforce same timestamp and unique camera IDs. Fake backend may use one view, but contracts must not collapse to single-view. |
| Deterministic in-memory replay sequence | Contract tests and regression gates require reproducible input ordering. | Low | Multi-view observations | Worktree has `InMemorySequence`. | In-memory only is fine for v1; lazy dataset readers are v2. |
| Gaussian splat primitive | Mosaic is splat-native; a v1 without typed splats is just generic SLAM scaffolding. | Medium | Core frame conventions | Worktree has `GaussianSplat`. | Include center, covariance, color, opacity, provenance. Covariance layout must be documented and tested. |
| Immutable splat-map snapshot | Backends, fusion, evaluation, and agents need a stable map snapshot boundary. | Medium | Gaussian splat primitive, frame IDs | Worktree has flat tuple `SplatMap`. | Immutable snapshots are correct for API boundaries; high-rate mutable backend state is not a v1 requirement. |
| Backend lifecycle protocol | Users need a stable seam for fake and future real 3DGS backends. | High | Observations, splat maps, poses | Worktree has `SplatSlamBackend` protocol and deterministic fake backend. | Include reset/process/snapshot, tracking state, update result, diagnostics, and capability metadata. |
| Deterministic fake backend | Tests need a backend that exercises lifecycle without CUDA/native dependencies. | Low | Backend protocol, splat maps | Worktree has `DeterministicSplatBackend`. | Must be boring. It validates plumbing, not SLAM quality. Do not let it become a research backend dumping ground. |
| Backend capability metadata | Downstream backend selection needs to know multi-view, incremental mapping, uncertainty, and isolation capabilities. | Medium | Backend protocol | Basic capability object exists in worktree; registry/availability missing. | Table stakes for v1 should include metadata shape; registry can follow after serialization if scope pressure exists. |
| Backend registry and availability checks | Optional CUDA/native backends need discovery without importing heavy dependencies into core. | Medium | Backend capabilities, optional dependency policy | Missing in worktree. | Should be v1 if real backend integration starts soon; otherwise phase immediately before real backend integration. |
| Platform/camera-rig contracts | Mosaic targets quadrupeds, UGVs, humanoids, and custom rigs; camera geometry must be robot-neutral. | Medium | Core pose/camera types | Worktree has `platforms`; main does not. | Separate embodiment metadata from calibration. Built-in presets are fixtures, not vendor-accurate robot models. |
| Representative rig presets | Users need examples and deterministic tests for common robot categories. | Low | Platform contracts | Worktree has presets. | Quadruped, UGV, humanoid presets are table-stakes fixtures; not production calibration. |
| Serialization and artifact schemas | Evaluation, replay, regression gates, backend isolation, and agent evidence references need machine-readable exchange. | High | Core, splats, backend updates | Missing in worktree. | This is table stakes before evaluation artifacts and real backend integration. Version schemas from day one; no ad hoc JSON per module. |
| Contract tests for core and backend lifecycle | A typed library lives or dies on contract stability. | Medium | All core contracts | Worktree has 43 tests, but gaps remain. | Include public API, geometry validation, replay determinism, splat validation, backend lifecycle, platform validation. |
| Deterministic evaluation scenarios | Future backend work must have a baseline to compare against. | Medium | Core, datasets, fake backend, platform/fusion as needed | Planned, not implemented. | Synthetic scenarios first; no real datasets needed for v1 foundation. |
| Metric result contracts | Regression gates need typed metric outputs, even if initial metrics are simple. | Low | Splat maps, backend updates | Planned, not implemented. | Start with splat count/update count/tracking state; avoid pretending map quality is measured before real render/trajectory metrics exist. |
| Benchmark artifact writer | Users and CI need machine-readable results. | Medium | Serialization/artifact schemas, metrics | Planned, not implemented. | JSON artifacts should be compact and stable; store large map/image payloads by evidence reference, not inline. |
| Regression gates | Real backend integration without gates is how regressions become folklore. | Medium | Metrics, artifacts, deterministic scenarios | Planned, not implemented. | Gates should distinguish lifecycle, pose, map, and query failures. |
| Posterior-aware fusion seam | Multi-camera/multi-session splat fusion must not devolve into occupancy-grid union. | High | Splat maps, frame semantics, provenance, serialization | Planned, not implemented. | A deterministic provenance-preserving reference strategy is table stakes; real Gaussian optimization is not. |
| Agent posterior query contracts | Mosaic's long-term value is agent-friendly posterior access; v1 needs a thin seam. | Medium | SplatMap, provenance, evaluation gates | Planned, not implemented. | Include bounded deterministic typed requests/responses, not LLM prompts. |
| Local spatial query over splat snapshots | Agents need bounded local geometry access rather than raw full maps. | Medium | Agent query contracts, SplatMap | Planned, not implemented. | Naive scan is acceptable only with explicit limits and deterministic ordering. Add indexing later. |
| Posterior summary and provenance summary | Agent consumers need confidence/provenance visibility without full splat dumps. | Low-Medium | Splat provenance fields, agent contracts | Planned, not implemented. | Summary count, provenance counts, opacity/uncertainty summaries; no semantic claims yet. |
| Public boundary documentation | Contributors need to know fake backend vs real backend, planned vs shipped, and out-of-scope wrappers. | Low | Stable API decisions | README currently empty/placeholder. | Documentation is table stakes for avoiding scope creep into ROS/UI/LLM runtimes. |

## Differentiators

Features that make Mosaic meaningfully different from a generic SLAM wrapper or a one-off 3DGS demo. Prioritize these after table-stakes contracts are stable.

| Feature | Value Proposition | Complexity | Dependencies | Recommended v1 Posture | Notes |
|---------|-------------------|------------|--------------|--------------------------|-------|
| Splat-native posterior contracts | Keeps Gaussian posterior state central instead of flattening into occupancy grids or point clouds. | High | Gaussian splats, SplatMap, covariance/provenance semantics | Build v1 seams and reference behavior. | This is Mosaic's core identity. Do not compromise it for convenience. |
| Agent-friendly posterior API | Lets LLM/LVLM agents inspect bounded belief/provenance views instead of raw splats. | High | Agent contracts, evaluation, evidence refs | Thin v1 seam; expand in v2. | First API should be deterministic Python objects usable later as tool-call JSON. |
| Provenance-preserving fusion | Maintains source evidence and uncertainty through map combination. | High | Fusion protocol, splat provenance, frame compatibility | Include deterministic reference strategy in v1. | The differentiator is not optimized fusion; it is refusing to erase uncertainty. |
| Regression-first real backend path | Forces real 3DGS backend integration to prove behavior against deterministic gates. | Medium-High | Evaluation scenarios, metrics, artifacts, backend registry | v1 must establish this before real backend work. | Prevents the common research-code trap: flashy demo, no reproducible evidence. |
| Robot-neutral platform rigs | One library can support quadrupeds, UGVs, humanoids, and custom rigs without SDK coupling. | Medium | Core poses/cameras, platform registry | Include in v1 foundation. | Useful even before real robot wrappers exist. |
| Backend isolation metadata | Prepares for crashy CUDA/native research backends without contaminating core imports. | Medium | Backend capabilities, registry, serialization | Metadata in v1; subprocess transport can be v2 unless backend integration begins. | Capability flags alone do not isolate anything; do not oversell them. |
| Layered Belief Graph + Agent Tool Memory architecture | Provides a path from splat maps to raster memory, scene graph, textual memory, belief, provenance, and commitments. | Very High | Agent posterior seam, claims, evidence refs, memory models, semantic extraction | Design in v1, implement only a thin query seam. | Full layered memory is too broad for v1 foundation. |
| Claim-based belief model | Represents observations as claims with confidence, status, conflict, staleness, and evidence. | High | Evidence refs, IDs, timestamps, agent memory stores | Defer implementation beyond thin posterior query seam. | Strong differentiator for agentic robotics, but premature before posterior seam and evaluation are stable. |
| ARNA-style memory ablation tests | Tests whether raster/scene graph/belief memory actually adds capability. | High | Layered memory implementation, scenario tests | Defer to v2. | Valuable, but not required for v1 typed SLAM contracts. |
| Bounded tool APIs ready for JSON serialization | Smooth path to agent tool calls without provider lock-in. | Medium | Agent result dataclasses, serialization schemas | Include design constraints in v1; implement basic query result schemas. | Do not integrate OpenAI/Anthropic/Habitat in core. |

## V2 / Deferred Features

These are valuable, but building them in v1 would freeze weak abstractions or drag heavy dependencies into the foundation.

| Deferred Feature | Why Defer | Prerequisites | Suggested Trigger |
|------------------|-----------|---------------|-------------------|
| Real 3D Gaussian Splatting SLAM backend integration | Contracts, serialization, backend registry, isolation, and regression gates must exist first. | Core contracts, artifact schemas, evaluation gates, backend registry. | After fake-backend benchmarks and regression artifacts are stable. |
| CUDA/native subprocess backend runner | Needed for fragile research backends, but transport details should not distort core contracts early. | Serialization schemas, backend availability checks, timeout/error model. | When first real native backend adapter is selected. |
| Real Gaussian fusion/registration/optimization | The reference fusion strategy should preserve provenance, not pretend to optimize posterior state. | Frame semantics, covariance helpers, evaluation metrics, real backend snapshots. | After map quality metrics and frame-alignment tests exist. |
| Pose math utilities: compose, inverse, transform points, frame chains | Easy to implement wrongly before transform direction, handedness, and optical conventions are pinned. | Explicit pose semantics and tests. | Before reprojection metrics, platform-to-world transforms, or real backend integration. |
| Spatial indexing for splat queries | Naive scans are acceptable for small deterministic tests; indexing adds API and performance design choices. | Stable `SplatMap`, query semantics, result limits. | When agent queries or fusion exceed linear scan limits. |
| Lazy/streaming dataset readers | In-memory replay is enough for v1 tests; real logs will need streaming. | Serialization, payload limits, dataset schema. | When integrating real robot logs or benchmark datasets. |
| Zero-copy image/tensor buffers | Bytes-backed buffers are safe for tests but expensive for production streams. | Numerical/tensor dependency decision, backend adapters. | When real backends need image tensors. |
| Full layered memory implementation | Raster memory, scene graph, text memory, belief memory, and commitments are beyond foundation scope. | Agent posterior seam, claims/evidence schema, synthetic scenarios. | After v1 posterior query API is stable. |
| Object detection, segmentation, room/region extraction | These are perception pipeline concerns, not core typed 3DGS SLAM contracts. | Optional perception adapters, evidence refs, scene graph memory. | In downstream agent/perception packages. |
| LLM/LVLM provider integration | Provider APIs churn and would pollute deterministic library core. | Stable tool schemas and external orchestration layer. | In downstream wrappers, not Mosaic core v1. |
| ROS nodes, robot command execution, Habitat runners, UI/WebSockets | These are wrappers/demos, not the typed library foundation. | Stable library APIs. | External packages or later integration demos. |
| Production robot calibration packages | Built-in presets are representative fixtures only. | Config/schema story and calibration ingestion. | When a specific robot integration is owned and tested. |
| Rich map quality/rendering metrics | Need real renderers/backends and ground truth before metrics mean anything. | Real backend, dataset fixtures, artifact schema. | After real backend adapter work begins. |
| Multi-robot commitment memory | Valuable for swarms but unrelated to first posterior query seam. | Belief model, task/resource IDs, conflict detection scenarios. | After layered memory v1. |

## Anti-Features

Features to explicitly not build in Mosaic v1.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| Real 3DGS backend demo before regression gates | Produces impressive but untestable behavior; backend assumptions leak into core. | Build fake backend, artifact schemas, metrics, and gates first. |
| Occupancy-grid-first core abstraction | Violates splat-native posterior goal and loses Gaussian uncertainty/provenance. | Keep Gaussian splats and posterior snapshots central; expose raster memory later as an agent view. |
| Union-style map merge treated as truth | Erases uncertainty and source conflicts. | Use provenance-preserving fusion with explicit diagnostics and uncertainty status. |
| Raw full splat map dumps to agents | Unbounded, unstable, and unsuitable for LLM/LVLM context windows. | Return bounded typed summaries, local query IDs, provenance, and evidence refs. |
| LLM prompt templates or provider clients in core | Couples Mosaic to model vendors and non-deterministic runtime behavior. | Expose deterministic Python query/tool contracts; let downstream orchestrators wrap them. |
| ROS/robot SDK dependencies in base package | Breaks headless installability and robot-neutral library design. | Keep core pure Python; provide adapters outside core later. |
| Habitat/GPT-4o/ARNA reproduction | No public ARNA implementation artifacts were found in project context; full reproduction is outside scope. | Borrow architectural lessons: separate memory views and deterministic tools. |
| Vendor-accurate built-in robot calibration | Incorrect calibration is worse than no calibration. | Ship representative fixtures and allow caller-supplied calibrated rigs. |
| Monolithic `mosaic` module with all logic | Creates immediate structure debt and blocks independent evolution. | Preserve namespaces: `core`, `splats`, `slam`, `datasets`, `platforms`, `fusion`, `evaluation`, `agents`. |
| Heavy numeric/tensor/CUDA dependency in foundation | Makes core fragile and backend-specific before contracts stabilize. | Keep foundation pure Python; introduce optional extras behind adapters. |
| Mutable public map state | Makes regression/evidence semantics slippery. | Use immutable `SplatMap` snapshots at boundaries; allow backend-owned mutable internals later. |
| Silent frame conversion or implicit coordinate assumptions | Geometry bugs become invisible. | Validate frames strictly and require explicit transform semantics. |
| Treating plan snippets as implemented API | The repo contains detailed plans that may not exist in `src/`. | Requirements should distinguish implemented, planned, and deferred features. |

## Feature Dependencies

```text
Typed package/version surface
  -> public API stability tests

FrameId + Timestamp
  -> Pose3
  -> CameraObservation
  -> MultiViewObservation
  -> InMemorySequence
  -> Backend lifecycle protocol
  -> Evaluation scenarios
  -> Agent posterior query timestamps/evidence

Pose3 + CameraIntrinsics
  -> Platform CameraRig
  -> Backend estimated pose updates
  -> Future pose metrics and reprojection metrics
  -> Future real backend integration

GaussianSplat + SplatMap
  -> Deterministic fake backend
  -> Posterior-aware fusion
  -> Evaluation metrics
  -> Agent posterior queries
  -> Future real 3DGS backend adapters

Splat provenance fields
  -> Provenance-preserving fusion
  -> Agent provenance summaries
  -> Evidence references
  -> Future claim-based belief memory

Backend protocol + fake backend
  -> Contract tests
  -> Deterministic benchmarks
  -> Backend registry/availability checks
  -> Real backend integration

Serialization/artifact schemas
  -> Benchmark artifact writer
  -> Regression gates
  -> Backend subprocess isolation
  -> Agent evidence references
  -> Dataset persistence and replay fixtures

Platform CameraRig
  -> Multi-view scenario factories
  -> Platform-aware backend input construction
  -> Future robot-specific wrappers

FusionInput/FusionResult protocol
  -> ProvenancePreservingFusion
  -> Fusion metrics
  -> Agent queries over fused snapshots

Evaluation scenarios + metrics
  -> Benchmark artifacts
  -> Regression gates
  -> Safe real backend integration
  -> Agent query stability tests

Agent query contracts
  -> SplatPosteriorView
  -> Posterior/provenance summaries
  -> Future layered belief graph
  -> Future JSON tool-call wrappers
```

## MVP Recommendation

For a v1 typed Python 3DGS SLAM library foundation, prioritize in this order:

1. **Stabilize core typed contracts**
   - `FrameId`, `Timestamp`, `Pose3`, `CameraIntrinsics`, `ImageBuffer`, `CameraObservation`, `MultiViewObservation`.
   - Pin transform direction, handedness, optical frame conventions, and timestamp precision before adding pose math.

2. **Stabilize splat-native SLAM substrate**
   - `GaussianSplat`, `SplatMap`, `SplatSlamBackend`, `SplatSlamUpdate`, `BackendCapabilities`, deterministic fake backend.
   - Keep fake backend deterministic and explicitly non-representative of SLAM quality.

3. **Add platform rig layer**
   - Robot-neutral `CameraRig`, `CameraMount`, `PlatformDescription`, `PlatformRegistry`, and representative presets.
   - Document presets as fixtures, not calibrated models.

4. **Add serialization and machine-readable artifact schemas**
   - Round-trip core data, splat maps, backend updates, and benchmark artifacts.
   - This should come before evaluation output and real backend integration.

5. **Add backend registry and availability checks**
   - Registry entries should expose capability metadata, optional dependency availability, and contract-test parametrization.
   - Do not import CUDA/native packages during core import.

6. **Add posterior-aware fusion seam**
   - `FusionInput`, `FusionResult`, `SplatFusionStrategy`, and a deterministic `ProvenancePreservingFusion` reference.
   - Validate frame compatibility and preserve provenance/uncertainty diagnostics.

7. **Add deterministic evaluation and regression harness**
   - Synthetic scenarios, metric contracts, benchmark artifacts, and gates.
   - Gates should initially test lifecycle/map/query stability, not overclaim real SLAM quality.

8. **Add thin agent posterior query seam**
   - `LocalRadiusQuery`, `SplatQueryResult`, `PosteriorSummary`, `ProvenanceSummary`, `SplatPosteriorView`.
   - Enforce bounded deterministic results. No LLM integration.

### Defer from MVP

- Real 3DGS backend adapter.
- Real Gaussian optimization/fusion.
- Full layered belief graph, raster memory, scene graph memory, textual memory, and commitments.
- LLM/LVLM provider integration.
- ROS, Habitat, browser UI, robot command execution.
- Production calibration packages.

## Suggested Phase Split for Requirements

| Phase | Feature Focus | Why This Order | Key Exit Criteria |
|-------|---------------|----------------|-------------------|
| 1. Foundation contracts | Package surface, frames/time, poses, cameras, observations, splats, maps, backend protocol, fake backend, in-memory replay | Everything else depends on these types. | Public imports stable; deterministic backend lifecycle tests pass. |
| 2. Frame semantics and serialization hardening | Transform direction, optical conventions, round-trip schemas, artifact schema baseline | Prevents later fusion/evaluation/backend disagreements. | Pose semantics documented/tested; core objects serialize round-trip. |
| 3. Platform and backend registry | Camera rigs, presets, backend registry, capability/availability metadata | Supports robot-neutral inputs and pluggable backends without heavy imports. | Built-in rigs testable; backend registry can run contract tests against fake backend. |
| 4. Fusion and evaluation gates | Provenance-preserving fusion, synthetic scenarios, metrics, artifacts, regression gates | Creates evidence before real backend integration. | Benchmark artifact emitted; gates detect known lifecycle/map failures. |
| 5. Agent posterior seam | Bounded local queries, summaries, provenance over `SplatMap` snapshots | Agent API needs stable maps and evaluation gates first. | Query determinism and bounded result tests pass. |
| 6. Real backend readiness | Optional backend adapter spike, subprocess boundary, richer metrics | Only after gates exist. | Real backend can be integrated without changing core contracts. |

## Requirement-Level Acceptance Criteria

### Foundation contract acceptance

- All public dataclasses/protocols validate invalid inputs deterministically.
- Top-level exports include only implemented stable symbols.
- Tests distinguish current API from planned future modules.
- No CUDA/native/numeric heavy dependency is required to import Mosaic core.

### Fusion acceptance

- Fusion rejects empty and cross-frame inputs.
- Fusion result diagnostics include source map count, source splat count, fused count, and uncertainty handling label.
- Provenance from input splats remains visible in output splats.
- Reference strategy does not claim optimized posterior fusion.

### Evaluation acceptance

- Synthetic scenario generation is deterministic.
- Fake backend benchmark output is stable JSON or equivalent machine-readable artifact.
- Regression gates fail when metrics are missing or below threshold.
- Artifacts do not inline large images/maps by default.

### Agent posterior acceptance

- Query inputs validate radius, center shape, and result bounds.
- Local query results are deterministic for a fixed `SplatMap`.
- Summaries report count/provenance/uncertainty-relevant fields.
- Agent APIs return typed objects and evidence/provenance summaries, not raw full map dumps.

## Risk Notes for Requirements Authors

- Do not write requirements that imply real SLAM correctness from the deterministic fake backend. It only proves contracts.
- Do not treat planned files under `docs/superpowers/plans/` as implemented modules.
- Do not require full ARNA reproduction. The useful requirement is memory/tool separation, not paper-specific prompts or Habitat workflows.
- Do not add pose math until transform direction and optical frame conventions are unambiguous.
- Do not add real backend integration until serialization and regression gates exist.

## Sources

Internal project sources read on 2026-05-18:

- `/home/prannayag/pragnition/robotics/mosaic/.planning/PROJECT.md` — project scope, active/out-of-scope requirements, constraints.
- `/home/prannayag/pragnition/robotics/mosaic/.planning/codebase/CONCERNS.md` — main checkout placeholder state and missing critical features.
- `/home/prannayag/pragnition/robotics/.mosaic-worktrees/splat-slam-foundation/.planning/codebase/CONCERNS.md` — active worktree implementation status and remaining gaps.
- `/home/prannayag/pragnition/robotics/mosaic/docs/argus-migration-plan.md` — package shape, migration principles, milestone ordering.
- `/home/prannayag/pragnition/robotics/mosaic/docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md` — planned foundation contracts and tests.
- `/home/prannayag/pragnition/robotics/mosaic/docs/superpowers/plans/2026-05-18-platform-camera-rig-layer.md` — planned platform/camera-rig layer.
- `/home/prannayag/pragnition/robotics/mosaic/docs/superpowers/plans/2026-05-18-posterior-aware-splat-fusion.md` — planned fusion seam.
- `/home/prannayag/pragnition/robotics/mosaic/docs/superpowers/plans/2026-05-18-evaluation-regression-harness.md` — planned evaluation and regression harness.
- `/home/prannayag/pragnition/robotics/mosaic/docs/superpowers/plans/2026-05-18-agent-posterior-query-seam.md` — planned thin agent posterior API.
- `/home/prannayag/pragnition/robotics/mosaic/docs/superpowers/specs/2026-05-18-agent-friendly-representation-design.md` — layered belief graph and agent tool memory design.
