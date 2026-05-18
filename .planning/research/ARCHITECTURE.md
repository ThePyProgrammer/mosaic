# Architecture Research: Mosaic v1 Phasing and Layering

**Domain:** Typed headless Python library for 3DGS SLAM and agent-friendly representation posteriors  
**Researched:** 2026-05-18  
**Overall confidence:** HIGH for repository/worktree-derived architecture, MEDIUM for future real-backend integration details

## Executive Architecture Recommendation

Mosaic v1 should be phased as a dependency-ordered library foundation, not as a backend demo. The active `splat-slam-foundation` worktree already establishes the correct lower layers: `core`, `datasets`, `splats`, `slam`, and `platforms`. Roadmap planning should treat that worktree as the baseline to merge first, then build upward through serialization, backend registry, fusion, evaluation, a thin agent posterior seam, and finally representation memories.

The architectural spine is: immutable typed value objects at the bottom, protocol seams in the middle, deterministic artifact/evaluation contracts before heavy integrations, and bounded agent-facing query tools at the top. Do not reverse this order. If fusion, evaluation, or agent memories are added before serialization and backend capability metadata, you will end up with bespoke in-memory structures that cannot be regression-tested or compared across future real backends. That is exactly the kind of slow-motion architecture rot that looks productive for a week and then ruins v1.

Mosaic should keep data flow one-way and mostly upward: observations and platform rigs feed backend processing; backend updates produce splat-map snapshots; serialization and evaluation consume snapshots/results; fusion consumes snapshots and emits new snapshots with provenance; agent posterior queries consume snapshots and evaluation/fusion metadata; representation memories consume posterior query results and synthetic extractors. Lower layers must not import from upper layers.

## Recommended v1 Layer Stack

```text
External callers / downstream robots / future agent runtimes
        |
        v
Public package facades: mosaic, mosaic.core, mosaic.splats, ...
        |
        v
Agent-friendly representation memories
  agents.memory, agents.tools, agents.belief, agents.commitments
        |
        v
Thin agent posterior seam
  agents.queries, agents.posteriors
        |
        v
Evaluation and regression harness
  evaluation.metrics, evaluation.scenarios, evaluation.runner, evaluation.regression
        |
        v
Posterior-aware fusion
  fusion.protocol, fusion.strategies
        |
        v
Backend registry and backend contract parametrization
  slam.registry, slam.protocol extensions, optional backend metadata
        |
        v
Serialization and artifact schemas
  serialization or domain-owned schemas for core/splats/slam/evaluation
        |
        v
Foundation baseline from splat-slam-foundation
  core, datasets, splats, slam protocol/fake backend, platforms
        |
        v
Python standard library, pytest, uv; no required CUDA/native runtime
```

This diagram is intentionally bottom-heavy. Stable v1 value comes from contracts, artifacts, and regression gates, not from prematurely wiring a flashy 3DGS implementation into an unstable API.

## Component Boundaries

| Component | Responsibility | May Depend On | Must Not Depend On |
|-----------|----------------|---------------|--------------------|
| `mosaic.core` | Frames, timestamps, poses, camera intrinsics, image buffers, observations, coordinate conventions. | Standard library only. | `slam`, `splats`, `platforms`, `fusion`, `evaluation`, `agents`, backend packages. |
| `mosaic.datasets` | Deterministic replay of `MultiViewObservation` values and future adapters that normalize data into core contracts. | `core`. | Backend internals, platform presets as hard dependencies, agent/evaluation logic. |
| `mosaic.splats` | Gaussian primitives, immutable `SplatMap` snapshots, posterior/provenance fields. | `core` identifiers. | Backend implementation details, fusion strategies, agent memories. |
| `mosaic.slam` | Backend lifecycle protocol, update/result types, capabilities, fake backend, backend registry. | `core`, `splats`, optionally `datasets` for contract tests. | Platform-specific branches, agent APIs, evaluation runners, CUDA imports in protocol modules. |
| `mosaic.platforms` | Robot-neutral embodiment metadata, camera rigs, frame trees, presets, registries. | `core`. | SLAM algorithms, backend selection policy, ROS/vendor SDKs. |
| `mosaic.serialization` or domain schema modules | Versioned JSON-ready schemas and round-trip helpers for core data, splats, backend updates, evaluation artifacts, and later agent outputs. | `core`, `splats`, `slam` result types, `evaluation` artifact types as they appear. | Backend runtime objects, file formats requiring native dependencies, agent orchestration. |
| `mosaic.fusion` | Posterior-aware map fusion protocols and deterministic reference strategies preserving uncertainty/provenance. | `core`, `splats`, serialization schemas where needed. | Occupancy-grid assumptions, backend-specific map internals, agent memory stores. |
| `mosaic.evaluation` | Deterministic scenarios, metrics, benchmark artifact writing, regression gates, backend contract parametrization. | `core`, `datasets`, `splats`, `slam`, `fusion`, serialization. | Real backend imports unless optional/registry-selected, LLM providers, robot execution. |
| `mosaic.agents` posterior seam | Bounded deterministic queries over splat-map/posterior snapshots: summaries, local spatial queries, uncertainty, provenance. | `core`, `splats`, serialization, selected evaluation/fusion result shapes. | LLM/LVLM providers, ROS, Habitat runners, raw full-map dumps as public query output. |
| `mosaic.agents.memory` / representation memories | Spatial/raster, scene graph, textual, belief/provenance, and commitment memories plus deterministic tool APIs. | Agent posterior seam, `core` IDs/time/frame concepts, opaque evidence refs. | Direct backend lifecycle control, low-level Gaussian optimization, provider prompts. |

## Dependency Rules

1. `core` is the root. Nothing in `core` imports from Mosaic subpackages.
2. `splats`, `datasets`, and `platforms` depend on `core`, not on each other unless a concrete use case forces it.
3. `slam` depends on `core` and `splats`; its protocol modules stay dependency-light.
4. Serialization is introduced before registry/fusion/evaluation becomes serious because artifact compatibility is a v1 contract.
5. Registry depends on protocol contracts; protocols must not depend on registry global state.
6. Fusion consumes immutable `SplatMap` snapshots; it does not mutate backend state.
7. Evaluation consumes datasets, backends, fusion outputs, and serialized artifacts; it should not be imported by production lower layers.
8. Agent posterior queries consume snapshots and metadata; they do not command backends or robots.
9. Representation memories consume posterior/evidence/query outputs; they do not become the source of truth for splat maps.
10. Public `__init__.py` facades re-export stable names only. Low-level modules should import leaf modules, not package facades, to avoid circular imports.

## Data Flow

### 1. Baseline SLAM Flow

```text
PlatformDescription / CameraRig
        |
        v
CameraObservation values with frame, pose, intrinsics, image/depth payloads
        |
        v
MultiViewObservation from dataset replay or runtime adapter
        |
        v
SplatSlamBackend.process(observation)
        |
        v
SplatSlamUpdate: tracking state, optional pose, map update, diagnostics
        |
        v
SplatMap snapshot/update with provenance
```

The baseline worktree already validates the core version of this flow with a deterministic fake backend. Roadmap phase 1 should merge and stabilize it before expanding upward.

### 2. Serialization and Artifact Flow

```text
Core objects / SplatMap / SplatSlamUpdate / evaluation results
        |
        v
Versioned schema conversion: to_dict/from_dict or artifact DTOs
        |
        v
Stable JSON-ready benchmark and regression artifacts
        |
        v
Golden fixtures, compatibility tests, downstream consumers
```

Serialization should be explicit and versioned. Avoid sprinkling arbitrary `asdict()` dumps everywhere; those become accidental wire formats. Use schema types or domain-owned conversion functions that preserve frames, timestamps, provenance, and future compatibility.

### 3. Backend Registry Flow

```text
Backend implementation package/class
        |
        v
BackendDescriptor: name, version, capabilities, parameter schema, availability check, isolation mode
        |
        v
BackendRegistry lookup and construction
        |
        v
Shared backend contract tests and evaluation runner parametrization
```

The registry is not a service locator dumping ground. It exists so tests/evaluation can discover backends consistently and so heavy CUDA/native backends stay optional. Keep `DeterministicSplatBackend` as the default reference backend.

### 4. Fusion Flow

```text
SplatMap snapshot A + SplatMap snapshot B + frame/provenance metadata
        |
        v
FusionInput validation: frame compatibility, source identity, timestamp/provenance sanity
        |
        v
FusionStrategy.fuse(input)
        |
        v
FusionResult: fused SplatMap, retained/suppressed/conflicted evidence, diagnostics
```

Fusion must be posterior-aware. Do not model it as occupancy-grid union with nicer names. The fusion result must make uncertainty and provenance visible because agent belief and evaluation will depend on it later.

### 5. Evaluation Flow

```text
Deterministic scenario or replay sequence
        |
        v
Backend selected directly or through registry
        |
        v
Run lifecycle: reset -> process sequence -> snapshot -> optional fusion -> metrics
        |
        v
BenchmarkArtifact: scenario, backend descriptor, metrics, diagnostics, serialized outputs
        |
        v
RegressionGate: pass/fail with reason categories
```

Evaluation must precede real backend integration. Otherwise Mosaic will have no reliable way to tell whether a backend integration improved the system or merely produced plausible-looking splats.

### 6. Agent Posterior Query Flow

```text
SplatMap snapshot / fused snapshot / backend diagnostics / provenance metadata
        |
        v
PosteriorView or QueryContext
        |
        v
Bounded typed query methods: summarize, local region query, uncertainty, provenance, evidence refs
        |
        v
Agent-safe result objects with confidence, source, observed_at, evidence, limits
```

This seam should be thin in v1. It should not implement scene graphs, routing, LLM calls, or robot commands yet. Its job is to make splat posterior state queryable without exposing raw full map internals.

### 7. Representation Memory Flow

```text
Posterior query results or synthetic extractor outputs
        |
        v
Claim builder: entity/relation/confidence/source/evidence/status
        |
        v
Belief memory update: active/superseded/conflicted/stale/rejected
        |
        v
Memory projections:
  - spatial/raster memory
  - scene graph memory
  - textual summary memory
  - commitment memory
        |
        v
Deterministic agent tools: find, summarize, inspect belief, retrieve evidence, allocate/reserve
```

The representation layer should use synthetic extractors at first. Real object detection, room segmentation, traversability inference, or ARNA reproduction should stay out of v1 unless a later phase explicitly earns that complexity.

## Concrete Build Order

### Phase 0: Merge and Freeze Foundation Baseline

**Goal:** Bring the `splat-slam-foundation` worktree into main and make it the baseline.

**Includes:**
- `core`: `Timestamp`, `FrameId`, `Pose3`, `CameraIntrinsics`, `ImageBuffer`, `CameraObservation`, `MultiViewObservation`.
- `splats`: `GaussianSplat`, immutable `SplatMap`.
- `slam`: `SplatSlamBackend`, `BackendCapabilities`, `SplatSlamUpdate`, `TrackingState`, `DeterministicSplatBackend`.
- `datasets`: `MultiViewSequence`, `InMemorySequence`.
- `platforms`: `Embodiment`, `CameraRig`, `PlatformDescription`, `PlatformRegistry`, presets.
- Tests mirrored by subpackage.

**Exit criteria:** Worktree tests pass in main; public facades export stable names; README documents fake backend and test command.

**Architectural reason:** Every later layer consumes these contracts. Replanning from main's placeholder package would waste work and create duplicate foundations.

### Phase 1: Coordinate Semantics and Serialization

**Goal:** Pin frame/pose/time semantics and create machine-readable schemas before more consumers appear.

**Includes:**
- Document pose direction, parent/child frame semantics, quaternion convention, camera optical frame convention, timestamp precision.
- Add schema versioning for core observations, splat primitives/maps, backend updates, capabilities, diagnostics, and benchmark artifacts.
- Add round-trip and golden fixture tests.

**Exit criteria:** Serialized artifacts can round-trip without losing frame, timestamp, covariance, opacity, provenance, or diagnostics; schema version appears in artifacts.

**Architectural reason:** Fusion, evaluation, backend registry, and agent evidence refs all need stable artifact contracts. Serialization after those layers would force rewrites.

### Phase 2: Backend Registry and Contract Parametrization

**Goal:** Make backend discovery explicit without adding real heavy backends.

**Includes:**
- `BackendDescriptor` with name, version, capabilities, parameter schema, availability check, optional dependency hints, and `runs_out_of_process` intent.
- `BackendRegistry` with explicit instance/local registry; avoid mutable global singleton as the only path.
- Contract-test helpers that run the same lifecycle expectations against registered backends.
- Keep deterministic backend registered as the reference implementation.

**Exit criteria:** Evaluation/contract tests can enumerate registered fake/lightweight backends; unavailable heavy backends can be represented without import failure.

**Architectural reason:** Registry must come before evaluation and real backend work so optional dependencies and availability do not infect core imports.

### Phase 3: Posterior-Aware Fusion Seam

**Goal:** Define splat-native fusion before agent memories or multi-session evaluation assume a merge model.

**Includes:**
- `FusionInput`, `FusionResult`, `FusionDiagnostics`, `FusionStrategy` protocol.
- Deterministic reference strategies: identity/no-op, append-with-provenance, conflict-marking frame-compatible merge.
- Explicit frame compatibility and provenance retention rules.

**Exit criteria:** Tests show fusion rejects incompatible frames, preserves source provenance, returns diagnostics, and never mutates inputs.

**Architectural reason:** Fusion semantics affect evaluation metrics and agent belief. Get the contract right before building consumers.

### Phase 4: Evaluation and Regression Harness

**Goal:** Provide deterministic quality gates before real backend integration.

**Includes:**
- Synthetic scenarios over `InMemorySequence` and platform presets.
- Metrics for lifecycle correctness, replay determinism, pose availability/consistency, map update shape, splat counts/provenance, fusion diagnostics, and later query stability.
- Benchmark runner writing serialized artifacts.
- Regression gates with categorized failures.

**Exit criteria:** Fake backend benchmark produces stable artifacts; regression gates catch intentional lifecycle/map/schema failures.

**Architectural reason:** This is the safety net. Real backend integration before this is just vibes with CUDA.

### Phase 5: Thin Agent Posterior Seam

**Goal:** Expose bounded deterministic queries over snapshots without committing to the full representation memory model.

**Includes:**
- `PosteriorQueryContext` / `PosteriorView` over a `SplatMap` snapshot and optional diagnostics/provenance.
- Query result types for scene summary, local spatial summary, uncertainty summary, provenance/evidence lookup.
- Limits on result size and deterministic ordering.
- Tests for query determinism, bounded outputs, and evidence/provenance plumbing.

**Exit criteria:** Agent callers can ask limited questions without receiving raw full splat maps; outputs are serializable and evidence-carrying.

**Architectural reason:** This seam protects both sides: agents do not bind to raw splat internals, and low-level SLAM does not inherit agent/runtime churn.

### Phase 6: Representation Memories and Deterministic Tools

**Goal:** Add the ARNA-informed memory/tool architecture as typed local library contracts.

**Includes:**
- Identifier types: `RobotId`, `RegionId`, `EntityId`, `ClaimId`, `CommitmentId`, `EvidenceRef`.
- Claim model with status, confidence, source, observed_at, frame_id, valid_until, evidence, conflicts.
- Spatial/raster memory, scene graph memory, textual summary memory, belief/provenance memory, commitment memory.
- Deterministic tools: find objects/hazards, summarize region/context, get frontiers, query traversability, inspect staleness/conflicts, allocate/reserve/list commitments.
- Synthetic extractor inputs only; no real detector or LLM dependency.

**Exit criteria:** Scenario tests cover conflicting robot reports, stale claims, blocked paths, frontier queries, context summaries with source claims, and memory ablations.

**Architectural reason:** Memories should sit on top of posterior queries and evidence refs. If they bypass that seam, they will become a second inconsistent world model.

### Phase 7: Optional Real Backend Integration Readiness, Not v1 Core

**Goal:** Prepare for real 3DGS backends after v1 contracts prove stable.

**Includes:**
- Optional dependency packaging strategy.
- Out-of-process backend runner design if needed.
- Backend-specific adapters that implement `SplatSlamBackend` and register descriptors.

**Exit criteria:** A real backend can fail availability checks gracefully and can be evaluated using existing artifacts/gates.

**Architectural reason:** Project scope says real backend integration is out of v1. The architecture should enable it without dragging it into foundation modules.

## Patterns to Follow

### Pattern: Immutable Snapshot Boundaries

**What:** Core observations, splat maps, fusion results, evaluation artifacts, and agent query outputs should be frozen or treated as immutable after construction.

**When:** Every boundary where data leaves a component.

**Why:** Backend internals can be mutable; public values cannot be. This keeps tests deterministic and prevents spooky action-at-a-distance when evaluation and agents inspect the same map.

### Pattern: Protocol Plus Descriptor

**What:** Runtime behavior is defined by a protocol; discovery and selection are defined by a descriptor.

**When:** Backends, fusion strategies, and possibly extractors/tools.

**Why:** Protocols validate shape; descriptors carry metadata such as capabilities, availability, schema, and isolation. Mixing those creates obese classes and import-time dependency traps.

### Pattern: Explicit Evidence References

**What:** Agent-facing and fusion/evaluation outputs carry opaque evidence refs instead of loading raw image/splat payloads.

**When:** Claims, provenance summaries, query results, regression artifacts.

**Why:** Evidence traceability matters, but v1 should not invent a storage subsystem. Opaque refs keep the API stable.

### Pattern: Synthetic First, Real Later

**What:** Build deterministic synthetic scenarios, fake backend outputs, and synthetic extractor inputs before real data/backends.

**When:** Evaluation, posterior seam, representation memories.

**Why:** If the contract cannot survive synthetic tests, it has no business being coupled to a real backend.

## Anti-Patterns to Avoid

### Anti-Pattern: Serialization as Raw Dataclass Dumps

**What goes wrong:** `dataclasses.asdict()` output becomes an undocumented public artifact format.

**Why bad:** Field renames become breaking changes, versioning is absent, and downstream tools infer semantics that were never promised.

**Instead:** Use explicit versioned artifact schemas and round-trip tests.

### Anti-Pattern: Global Backend Registry as Hidden State

**What goes wrong:** Tests pass or fail depending on import order and installed optional dependencies.

**Why bad:** Backend availability becomes non-deterministic and core imports can break on machines without CUDA/native packages.

**Instead:** Prefer explicit `BackendRegistry` instances, with a helper for a default registry that registers dependency-free backends only.

### Anti-Pattern: Fusion as Occupancy Union

**What goes wrong:** The API discards uncertainty, source identity, and conflicting evidence.

**Why bad:** Mosaic is splat/posterior-native; agent belief and evaluation need uncertainty/provenance.

**Instead:** Fusion results must preserve or explicitly mark retained, suppressed, and conflicted evidence.

### Anti-Pattern: Agent APIs Returning Full Raw Maps

**What goes wrong:** Agent consumers bind to Gaussian internals and produce unbounded outputs.

**Why bad:** It prevents stable deterministic tool semantics and couples agents to backend representation churn.

**Instead:** Return bounded summaries, local query results, uncertainty/provenance records, and evidence refs.

### Anti-Pattern: Representation Memories as the Source of Truth

**What goes wrong:** Scene graph/raster/text memories drift away from splat snapshots and posterior evidence.

**Why bad:** Agents will reason over stale fiction while the map says something else.

**Instead:** Treat memories as projections with claim status, timestamps, evidence refs, and staleness/conflict checks.

## Integration Risks

| Risk | Severity | Where It Appears | Mitigation |
|------|----------|------------------|------------|
| Coordinate frame ambiguity | Critical | Core, platforms, fusion, evaluation, agents | Freeze pose direction and frame conventions in Phase 1 before adding consumers. |
| Serialization lock-in | High | Artifacts, evaluation, downstream agents | Add schema versions and golden fixtures before benchmark outputs proliferate. |
| Optional backend dependency leakage | High | Backend registry and real backends | Keep protocol modules dependency-free; availability checks must not import heavy packages at package import time. |
| Fusion loses posterior semantics | High | Fusion, agent belief, evaluation | Require provenance/uncertainty diagnostics in every `FusionResult`. |
| Evaluation comes too late | High | Real backend integration | Make deterministic evaluation Phase 4 and block real backend roadmap items on it. |
| Agent layer scope creep | High | Agent posterior seam and memories | Keep v1 local deterministic APIs only; no LLM provider, ROS, Habitat, or robot execution. |
| Circular imports through facades | Medium | Public `__init__.py` expansion | Low-level modules import leaf modules only; facades re-export stable types. |
| Registry hidden global state | Medium | Backend selection/tests | Use explicit registries and dependency-free default registry helpers. |
| Memory projections drift | Medium | Representation memories | Claims must carry evidence refs, observed_at, valid_until, status, and conflict links. |

## Scalability Considerations

| Concern | v1 / 100 sequences | 10K sequences or maps | 1M+ artifacts / real deployment |
|---------|--------------------|-----------------------|----------------------------------|
| Core object volume | Frozen dataclasses and tuples are enough. | Consider array-backed payload adapters while preserving contracts. | External storage and lazy payload refs; do not change public semantic contracts. |
| Serialization | JSON-ready schemas and golden fixtures. | Chunked artifacts and manifest files. | Artifact registry/object store, but evidence refs can remain opaque. |
| Backend execution | In-process fake/reference backend. | Optional real backends via registry and availability checks. | Out-of-process isolation for crashy/GPU backends. |
| Fusion | Deterministic reference strategies. | Strategy descriptors and benchmarked fusion scenarios. | Distributed/session-aware fusion outside v1 core. |
| Evaluation | Pytest and local benchmark runner. | Batch benchmark manifests. | CI matrix plus backend-specific runners. |
| Agent memories | In-memory dataclass stores. | Persistent store abstraction may become necessary. | Database/service wrappers downstream; keep library API typed. |

## Roadmap Implications

Recommended phase order:

1. **Foundation merge and API freeze** - because all later work depends on the active worktree's core contracts.
2. **Frame semantics plus serialization** - because artifacts, fusion, evaluation, and evidence refs need stable schemas.
3. **Backend registry** - because backend parametrization and optional dependency isolation must exist before evaluation and real integrations.
4. **Posterior-aware fusion** - because map composition semantics affect evaluation and agent belief.
5. **Evaluation/regression** - because backend and fusion behavior need deterministic gates before real backend work.
6. **Thin agent posterior seam** - because agents need bounded access to snapshots without raw map coupling.
7. **Representation memories/tools** - because richer agent memory should be a projection over posterior/evidence contracts, not a parallel world model.

Do not put representation memories before the thin posterior seam. Do not put real backend integration before evaluation. Do not put fusion before frame semantics and serialization. That ordering is not bureaucratic ceremony; it is the dependency graph.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Baseline layers | HIGH | Derived directly from current main planning docs and active `splat-slam-foundation` worktree maps. |
| Build order | HIGH | Matches validated project requirements, Argus migration plan milestones, and active worktree gaps. |
| Serialization need | HIGH | Explicit active requirement and prerequisite for artifacts/regression/evidence refs. |
| Backend registry shape | HIGH | Argus migration plan explicitly calls for protocol/registry patterns, capability metadata, availability checks, and contract tests. |
| Fusion contract | HIGH | Project and migration docs explicitly reject occupancy-grid union assumptions and require uncertainty/provenance preservation. |
| Evaluation architecture | HIGH | Project requires evaluation before real backend integration; Argus migration plan emphasizes deterministic artifacts and regression gates. |
| Agent posterior seam | HIGH | Project/specs require bounded deterministic APIs over snapshots, not provider integration or raw map dumps. |
| Representation memory internals | MEDIUM | Agent-friendly spec is detailed, but concrete implementation package names and extractor boundaries remain future design work. |
| Real backend isolation details | MEDIUM | The seam is well-supported by docs, but actual subprocess/GPU adapter design is intentionally deferred. |

## Sources

- `/home/prannayag/pragnition/robotics/mosaic/.planning/PROJECT.md`
- `/home/prannayag/pragnition/robotics/mosaic/.planning/codebase/ARCHITECTURE.md`
- `/home/prannayag/pragnition/robotics/mosaic/.planning/codebase/STRUCTURE.md`
- `/home/prannayag/pragnition/robotics/.mosaic-worktrees/splat-slam-foundation/.planning/codebase/ARCHITECTURE.md`
- `/home/prannayag/pragnition/robotics/.mosaic-worktrees/splat-slam-foundation/.planning/codebase/STRUCTURE.md`
- `/home/prannayag/pragnition/robotics/mosaic/docs/argus-migration-plan.md`
- `/home/prannayag/pragnition/robotics/mosaic/docs/superpowers/specs/2026-05-18-agent-friendly-representation-design.md`
