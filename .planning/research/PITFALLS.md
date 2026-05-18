# Domain Pitfalls

**Domain:** typed Python library foundation for 3DGS SLAM, robotics camera rigs, posterior-aware fusion, evaluation, and agent-friendly representation APIs
**Project:** Mosaic v1
**Researched:** 2026-05-18
**Overall confidence:** HIGH for project-specific planning risks from repository plans and codebase audits; MEDIUM for ARNA-derived agent representation risks because no public ARNA implementation artifacts were found.

## Critical Pitfalls

Mistakes that cause rewrites, invalid evaluation, unsafe backend coupling, or agent APIs that cannot be trusted.

### Pitfall 1: Leaving coordinate-frame semantics implicit

**What goes wrong:** `Pose3`, camera mounts, platform rigs, backend tracking outputs, fusion inputs, evaluation metrics, and agent spatial queries all interpret transforms differently. One component treats a pose as child-to-parent, another as parent-to-child; optical frame axes are guessed; covariance frames are unstated; timestamp precision silently changes ordering.

**Why it happens:** The foundation currently has typed frame and pose containers, but the active worktree concern audit says transform direction semantics, coordinate handedness, camera optical conventions, composition, inversion, and covariance frame are under-specified. Planning also explicitly says frame semantics must be pinned before pose math, camera-to-rig transforms, fusion, or evaluation metrics.

**Consequences:** Silent geometry errors, invalid multi-camera fusion, bad trajectory metrics, wrong traversability/frontier outputs, and agent-facing explanations grounded in the wrong location. This is the classic robotics foot-gun: tests pass because objects are typed, while maps are upside-down or transforms are inverted.

**Warning signs:**
- Functions named generically like `transform`, `pose`, or `extrinsics` without direction in docs/tests.
- Tests only assert dataclass construction, not composition/inversion or camera-to-rig-to-world chains.
- Platform preset tests verify names and counts but not frame-tree math.
- Evaluation metrics are added before frame conventions have golden fixtures.
- Agent query examples reference `map`, `base_link`, or camera frames without evidence of transform-path validation.

**Prevention strategy:**
- Make a frame semantics phase non-negotiable before serialization, fusion, evaluation, and agent APIs.
- Define `Pose3` direction in names and documentation, e.g. whether it represents `T_parent_child` or `T_child_parent`; do not allow ambiguous prose.
- Add golden tests for identity, inverse, composition, transform-point, camera optical frame projection, camera-to-rig-to-world chaining, and covariance frame labeling.
- Add fixture examples for at least one body frame, one optical camera frame, and one map/world frame.
- Reject empty frame IDs, duplicate camera frames, mismatched observation frames, and unstated timestamp units at constructors or validators.

**Phase should address it:** Phase 1: Foundation stabilization / frame semantics. This must block Phase 2 serialization, Phase 4 fusion, Phase 5 evaluation, and Phase 6 agent posterior APIs.

**Confidence:** HIGH. This is called out independently in project requirements, migration plan risks, main-checkout concerns, and active-worktree concerns.

### Pitfall 2: Treating the deterministic fake backend as evidence of SLAM correctness

**What goes wrong:** The roadmap integrates real 3DGS behavior or claims SLAM progress because the fake backend lifecycle passes tests. The deterministic backend creates synthetic splats and validates plumbing only; it does not validate tracking, multi-view fusion, uncertainty, convergence, rendering quality, loop closure, relocalization, or failure recovery.

**Why it happens:** A working fake backend is seductive. It gives green tests and a usable interface, so planners may mistake contract coverage for algorithmic validation.

**Consequences:** Mosaic can ship APIs that look backend-ready but cannot distinguish a real backend improvement from a regression. Later backend integration will either contort the protocol or punch through it with backend-specific fields.

**Warning signs:**
- Roadmap tasks say "integrate backend" before evaluation artifacts and contract tests exist.
- Tests assert splat counts or first-view pose passthrough but not lost tracking, diagnostics, reset-after-failure, or multi-view behavior.
- The fake backend accumulates research-specific logic.
- Backend APIs return unstructured dictionaries for diagnostics because result contracts were too thin.

**Prevention strategy:**
- Keep the fake backend boring and explicitly label it a contract fixture.
- Expand backend contract tests before any real backend: initialize/process/snapshot/reset, `NOT_INITIALIZED`, `TRACKING`, `LOST`, diagnostic fields, deterministic replay, availability checks, and parameter validation.
- Add a backend registry with capability metadata and optional dependency availability before real backends.
- Define failure semantics and machine-readable diagnostics as first-class result types, not backend-specific exceptions.
- Defer CUDA/native/research backend work until serialization and evaluation gates can record whether behavior improved.

**Phase should address it:** Phase 3: Backend registry and lifecycle contracts; Phase 5: Evaluation/regression before real backend integration.

**Confidence:** HIGH. Active worktree concerns identify fake backend limitations and missing registry; project constraints explicitly defer real backend integration.

### Pitfall 3: Adding serialization too late, after evaluation and agents invent incompatible encodings

**What goes wrong:** Core frames, poses, observations, splats, maps, backend updates, benchmark outputs, and evidence references each get ad hoc JSON/dict representations. Evaluation artifacts cannot be compared across runs; agent evidence URIs cannot be resolved consistently; dataset replay cannot round-trip exact timestamps and frames.

**Why it happens:** Serialization feels like bookkeeping, so implementers may prioritize visible features such as fusion, metrics, or agent tools first.

**Consequences:** Roadmap phases become coupled to private encodings. Regression gates are untrustworthy, external datasets can poison frame trees or covariance values, and agent provenance becomes decorative rather than auditable.

**Warning signs:**
- New modules define local `to_json` helpers instead of a versioned artifact schema.
- Benchmark results embed large image/splat payloads directly instead of evidence references.
- `Timestamp.from_seconds()` is used in ordering-sensitive tests instead of exact nanoseconds.
- Agent query outputs include `evidence` strings with no type/version/source semantics.
- Evaluation schemas are designed after metrics already exist.

**Prevention strategy:**
- Create versioned schemas immediately after frame/pose semantics are pinned.
- Add round-trip tests for `Timestamp`, `Pose3`, camera observations, `GaussianSplat`, `SplatMap`, backend update/result objects, and benchmark artifact summaries.
- Prefer summary artifacts plus opaque typed evidence references for large payloads.
- Validate external inputs at boundaries: timestamp units/order, non-unit quaternions, camera dimensions, image payload limits, Gaussian covariance layout/positive definiteness, frame IDs, and query result limits.
- Treat serialization schema changes as compatibility events with version fields, not incidental refactors.

**Phase should address it:** Phase 2: Serialization and artifact schemas. It should precede backend registry contract-test parametrization, evaluation artifacts, fusion diagnostics, and agent evidence APIs.

**Confidence:** HIGH. Both main and active worktree concerns call out missing serialization and trust-boundary risks.

### Pitfall 4: Letting a CUDA/native research backend contaminate the core library

**What goes wrong:** Mosaic's core imports PyTorch/CUDA, research code, renderer internals, simulator packages, or backend-specific tensor types. The package stops being a lightweight typed foundation and becomes a wrapper around one implementation.

**Why it happens:** Real 3DGS SLAM requires heavy dependencies, and the quickest integration path is usually to import them where the protocol types live.

**Consequences:** Core imports become fragile on machines without GPUs; tests require heavyweight environments; backend crashes take down the process; optional backends leak assumptions into `mosaic.core`, `mosaic.splats`, and `mosaic.slam`; agent/evaluation layers couple to one backend's data layout.

**Warning signs:**
- `mosaic.core`, `mosaic.splats`, or `mosaic.slam.protocol` imports CUDA, PyTorch, Habitat, ROS, or a research backend.
- Backend capability metadata exists but is not used for availability checks.
- Optional dependency failures happen at package import time.
- Backend adapters return backend-native tensors through public core contracts.
- No subprocess or isolation plan exists before native backend integration.

**Prevention strategy:**
- Keep core contracts standard-library/lightweight for v1.
- Introduce heavy libraries only behind optional extras and adapter modules.
- Add backend registry entries with capability metadata, availability checks, parameter schemas, and contract-test parametrization.
- Keep subprocess isolation, timeout handling, and serialized transport available before crashy native integrations.
- Require adapters to translate backend-native state into Mosaic `SplatMap` snapshots, diagnostics, and artifact schemas at boundaries.

**Phase should address it:** Phase 3: Backend registry and isolation seams. Actual real backend integration should be explicitly out of v1 or placed after Phase 5 evaluation gates.

**Confidence:** HIGH. The migration plan and project constraints both explicitly require backend isolation.

### Pitfall 5: Building fusion as occupancy-grid union instead of posterior-aware splat-map fusion

**What goes wrong:** Multi-camera or multi-session fusion silently unions map contents as if every source were equally true. Uncertainty, conflicts, duplicate observations, stale splats, source sessions, robot provenance, and frame compatibility are lost.

**Why it happens:** Occupancy-grid merging is familiar, easy to test, and inherited from classic robotics instincts. But Mosaic's value proposition is splat/posterior native, not occupancy-grid-first SLAM.

**Consequences:** Agent APIs receive overconfident maps; evaluation cannot explain why a fused region exists; conflicting robot observations disappear; later uncertainty-aware behavior requires a rewrite of fusion and map state.

**Warning signs:**
- Fusion output has no source map IDs, source splat counts, confidence/uncertainty propagation, or provenance diagnostics.
- Fusion accepts mismatched frames by transforming or merging implicitly without explicit registration evidence.
- Tests only assert output length equals sum of inputs.
- Agent belief layer treats fused map state as truth rather than claims with evidence.

**Prevention strategy:**
- Start fusion as a strategy protocol over immutable `SplatMap` snapshots, not an eager monolithic algorithm.
- Require explicit frame compatibility or explicit registration evidence before fusion.
- Preserve source map/session/splat provenance in diagnostics and output metadata.
- Include uncertainty/conflict status in fusion results even if first implementation is conservative.
- Add tests for empty inputs, mismatched frames, provenance preservation, rejection behavior, and conflict visibility.

**Phase should address it:** Phase 4: Posterior-aware fusion seam, after core splat types and serialization exist but before agent memory treats fused state as evidence.

**Confidence:** HIGH. The migration plan and concerns repeatedly warn against occupancy-grid union assumptions.

### Pitfall 6: Implementing evaluation after backend integration instead of before it

**What goes wrong:** Real backend integration lands without deterministic scenarios, metrics, artifact schemas, or regression gates. The team cannot tell whether tracking, mapping, fusion, or agent queries improved or regressed.

**Why it happens:** Backend demos feel more tangible than benchmark plumbing. But in SLAM, unmeasured demos are mostly theater.

**Consequences:** Backend-specific hacks accumulate; regressions become subjective; roadmap decisions are driven by screenshots or anecdotal replay behavior; phase completion cannot be audited.

**Warning signs:**
- A real backend is selected before metric definitions and benchmark artifacts exist.
- Evaluation outputs are human-readable logs only.
- No deterministic synthetic replay scenarios exist.
- Metrics mix lifecycle failures, pose failures, map failures, and query failures into one pass/fail result.
- Benchmark artifacts embed large payloads without stable summaries or seeds.

**Prevention strategy:**
- Implement deterministic evaluation scenarios using fake/lightweight backends first.
- Define machine-readable artifacts with metric name, value, unit, scenario, backend, seed, status, and failure class.
- Separate trajectory consistency, map/splat quality, backend lifecycle correctness, fusion behavior, and agent query stability.
- Add regression thresholds and golden artifacts before real backend adapters.
- Keep initial artifacts summary-only; large maps/images should be referenced, not embedded.

**Phase should address it:** Phase 5: Evaluation and regression harness. This phase must precede real 3DGS backend integration.

**Confidence:** HIGH. Project constraints explicitly require evaluation before backend integration; migration plan identifies deterministic metrics as a borrowed Argus discipline.

### Pitfall 7: Freezing the agent API around raw splats or provider-specific LLM workflows

**What goes wrong:** Agents consume raw splat maps, dense point clouds, huge graph dumps, prompt strings, or GPT/Habitat-specific workflows. Mosaic becomes an agent runtime or ARNA clone instead of a deterministic representation library.

**Why it happens:** The ARNA paper is compelling, and it is easy to copy visible pieces like GPT-4o, Habitat, Grounding DINO, and prompt loops rather than the durable architectural lesson: synchronized memory views and deterministic tools.

**Consequences:** Agent APIs are too large, unstable, non-deterministic, provider-coupled, and impossible to regression-test locally. Later users cannot swap LLM providers or use Mosaic without simulation/model dependencies.

**Warning signs:**
- `mosaic.agents` imports OpenAI/LVLM SDKs, Habitat, Grounding DINO, ROS, or browser/runtime code.
- Tool outputs are unbounded dumps of splats, scene graphs, or prompts.
- API objects include prompt templates instead of typed result schemas.
- Agent tests require live model calls.
- Scene summaries omit evidence, confidence, staleness, or conflict metadata.

**Prevention strategy:**
- Build a thin deterministic posterior query seam first: bounded typed outputs, local Python APIs, evidence/provenance references, uncertainty summaries, and stable ordering.
- Keep LLM/LVLM provider integration, Habitat runners, ROS nodes, and prompt orchestration out of v1 core.
- Treat ARNA as architecture evidence only: separate raster/spatial memory, scene graph memory, textual memory, belief/provenance, and commitments.
- Add query determinism, result bounds, provenance, uncertainty, stale/conflicted claim, and ablation-style tests.
- Make action outputs recommendations/commitments, not robot commands.

**Phase should address it:** Phase 6: Agent posterior seam and Phase 7: ARNA-informed memory layer. The first agent phase should remain read-only/thin; layered memory comes only after evaluation and fusion seams are stable.

**Confidence:** HIGH for project boundary; MEDIUM for ARNA implementation details because no public ARNA code or prompts were found.

### Pitfall 8: Collapsing observations into truth instead of evidence-carrying claims

**What goes wrong:** Object detections, hazards, traversability, frontier status, route blockages, and scene graph relations are stored as final facts. Conflicts, stale observations, source robot IDs, timestamps, and evidence references are lost.

**Why it happens:** Simple graph or memory stores often model the current world as truth. In multi-robot robotics, the current world is a set of claims with varying confidence and freshness.

**Consequences:** Agents cannot ask "why do you believe this?" or "is this stale/conflicted?"; route recommendations become overconfident; fusion hides disagreements; evaluation cannot audit failure causes.

**Warning signs:**
- Scene graph edges lack claim IDs, confidence, observed_at, valid_until, source, and evidence references.
- Text memory says "door blocked" rather than "rover_3 reported corridor_4 blocked; drone confirmation missing."
- Conflicting robot reports overwrite each other.
- Traversability queries return booleans without confidence or recommended confirmation.
- Staleness checks are absent from tool APIs.

**Prevention strategy:**
- Make claim-with-evidence the primitive of the agent representation layer.
- Support statuses: active, superseded, conflicted, stale, rejected.
- Require typed evidence references and source metadata for semantic, spatial, and textual memory updates.
- Add tests where two robots disagree, claims expire, evidence is retrieved by reference, and recommendations degrade under stale/conflicted evidence.
- Avoid auto-resolving entity conflicts in v1; expose uncertainty instead.

**Phase should address it:** Phase 7: ARNA-informed memory layer, with prerequisites from Phase 2 serialization and Phase 6 posterior query outputs.

**Confidence:** HIGH. This follows directly from the agent-friendly representation spec and ARNA notes.

### Pitfall 9: Over-scoping v1 into ROS, UI, Habitat, robot execution, or full ARNA reproduction

**What goes wrong:** Mosaic v1 balloons into ROS nodes, web visualization, Habitat runners, LLM orchestration, robot command execution, calibrated vendor rigs, object detection, segmentation, or full ARNA reproduction.

**Why it happens:** Robotics demos reward end-to-end visible systems. Mosaic's actual v1 value is less flashy: stable contracts, artifacts, fake backend lifecycle, deterministic evaluation, and bounded agent-facing posterior APIs.

**Consequences:** Core contracts remain unstable while peripheral integrations dominate effort. Dependencies explode; test environments become unreproducible; the library boundary disappears.

**Warning signs:**
- Roadmap phases include demo orchestration before core serialization/evaluation.
- New dependencies include ROS, Habitat, OpenAI, Grounding DINO, browser UI, WebSockets, or simulator assets in base package.
- Platform presets are treated as calibrated robot models.
- Agent tools directly execute robot actions instead of returning recommendations.
- README markets real backend or ARNA parity before contracts exist.

**Prevention strategy:**
- Keep v1 explicitly headless and Python-library-first.
- Put UI, ROS, Habitat, provider clients, and robot execution in downstream wrappers or future milestones.
- Keep built-in platform rigs representative fixtures, not vendor calibration packages.
- Require each phase to produce typed contracts and tests before integrations.
- Use ARNA only to shape memory/tool contracts, not as a dependency or reproduction target.

**Phase should address it:** Roadmap governance across all phases; especially Phase 0/1 scope lock and Phase 7 agent representation planning.

**Confidence:** HIGH. Project out-of-scope list and migration plan are explicit.

### Pitfall 10: Planning against the wrong checkout or mistaking plans for implemented APIs

**What goes wrong:** Implementation agents target `main`, which currently has placeholder package state, while the active `splat-slam-foundation` worktree contains the baseline implementation and tests. Or agents grep plan snippets and assume modules like `fusion`, `evaluation`, and `agents` already exist.

**Why it happens:** The repository and active worktree differ substantially; planning docs include code-like snippets and future APIs.

**Consequences:** Duplicate implementation, broken imports, false test results, roadmap phases based on nonexistent package surface, and merge pain.

**Warning signs:**
- `pytest` from main collects zero tests but is treated as success.
- Tasks reference `mosaic.fusion`, `mosaic.evaluation`, or `mosaic.agents` before source packages exist.
- Work estimates ignore the merge/stabilization of the foundation worktree.
- Public API docs claim capabilities from `docs/superpowers/plans/` rather than `src/mosaic/`.

**Prevention strategy:**
- Make the first roadmap phase stabilize and merge the foundation worktree baseline.
- State in every phase whether it targets main or the active worktree.
- Treat `docs/superpowers/plans/` as implementation guidance, not evidence of existing APIs.
- Require executable tests to land with the first source package for each planned namespace.
- Update README and public API exports after the foundation merge so contributors know what is real.

**Phase should address it:** Phase 0: Baseline stabilization and merge hygiene.

**Confidence:** HIGH. The required project context and both concerns audits identify this mismatch.

## Moderate Pitfalls

### Pitfall 1: Timestamp precision and replay determinism drift

**What goes wrong:** High-rate multi-camera observations reorder or collapse because float seconds are rounded to nanoseconds, replay ordering is ambiguous, or dataset loaders validate differently.

**Warning signs:**
- `Timestamp.from_seconds()` used for exact log replay.
- Tests do not include equal/near-equal timestamp edge cases.
- Multi-view observations lack deterministic camera ordering.

**Prevention strategy:** Use integer nanosecond constructors for exact replay; test ordering at nanosecond boundaries; require deterministic sequence iteration and stable camera ordering; include timestamp units in serialization.

**Phase should address it:** Phase 1 for core timestamps; Phase 2 for serialization; Phase 5 for replay/evaluation.

**Confidence:** HIGH.

### Pitfall 2: Image/camera semantic mismatch and unbounded payloads

**What goes wrong:** `CameraObservation` accepts image dimensions inconsistent with `CameraIntrinsics`, or unbounded image payloads cause memory spikes when external datasets arrive.

**Warning signs:**
- Observation constructors validate byte length but not intrinsics dimensions.
- Dataset loaders accept arbitrary image sizes without limits.
- Tests use tiny images only.

**Prevention strategy:** Validate color/depth image dimensions against intrinsics; add configurable payload limits for external inputs; keep bytes-backed buffers for deterministic tests but plan zero-copy/tensor wrappers at backend boundaries later.

**Phase should address it:** Phase 1 for observation validation; Phase 2 for dataset serialization/loading boundaries.

**Confidence:** HIGH.

### Pitfall 3: Gaussian covariance semantics become numerically brittle

**What goes wrong:** Packed covariance layout, positive-definiteness checks, near-singular matrices, and uncertainty propagation are interpreted inconsistently by splat primitives, fusion, posterior queries, and evaluation.

**Warning signs:**
- Covariance represented as a six-tuple without named layout helpers.
- Tests cover obvious invalid covariance only.
- Fusion computes confidence without covariance stress tests.

**Prevention strategy:** Document packed layout `(xx, xy, xz, yy, yz, zz)`; add matrix conversion helpers and near-singular tests; avoid uncertainty propagation algorithms until covariance semantics have golden cases.

**Phase should address it:** Phase 1 for splat primitive semantics; Phase 4 before fusion; Phase 6 before posterior uncertainty summaries.

**Confidence:** HIGH.

### Pitfall 4: Immutable snapshots become accidental high-rate storage

**What goes wrong:** `SplatMap.with_splats()` tuple concatenation and immutable image copies are used in high-rate mapping loops, causing O(n) update costs and memory churn.

**Warning signs:**
- Backends append one splat at a time through immutable public snapshots.
- Performance problems appear before real SLAM integration.
- Agent queries scan all splats linearly without explicit bounds.

**Prevention strategy:** Preserve immutable snapshots at API boundaries, but allow backend-owned mutable builders/state internally; add spatial/index abstraction only after query semantics are stable; enforce bounded agent result limits.

**Phase should address it:** Phase 3 for backend state boundaries; Phase 4 for fusion; Phase 6 for agent queries.

**Confidence:** HIGH.

### Pitfall 5: Platform presets become fake calibration truth

**What goes wrong:** Representative quadruped/UGV/humanoid camera rigs are mistaken for vendor-accurate calibrated models.

**Warning signs:**
- Preset intrinsics/extrinsics are used in evaluation claims.
- Docs omit "representative fixture" language.
- Platform layer starts encoding locomotion/simulator assumptions.

**Prevention strategy:** Document presets as smoke-test fixtures; put real calibration in dataset/config metadata; keep embodiment labels separate from SLAM logic.

**Phase should address it:** Phase 1/Platform foundation after baseline merge; Phase 5 evaluation should avoid claims based on placeholder rigs.

**Confidence:** HIGH.

### Pitfall 6: Public API exports drift from intended stable surface

**What goes wrong:** Downstream users import internal modules because top-level exports omit platform/backend/artifact contracts, or top-level exports expose unstable internals too early.

**Warning signs:**
- Tests only import subpackages.
- `__init__.py` exports implementation helpers rather than stable contracts.
- README examples differ from public API tests.

**Prevention strategy:** Add public API smoke tests per phase; decide intentionally which symbols are top-level versus subpackage-only; update README after baseline stabilization.

**Phase should address it:** Phase 0 baseline stabilization and each namespace introduction phase.

**Confidence:** MEDIUM-HIGH.

### Pitfall 7: Python-version compatibility is assumed from a newer local interpreter

**What goes wrong:** Code passes on Python 3.14 locally but breaks on the declared Python 3.12 minimum.

**Warning signs:**
- CI or local validation does not run Python 3.12.
- Code uses newer stdlib behavior or syntax without noticing.

**Prevention strategy:** Validate on Python 3.12 before merging; keep syntax and APIs compatible with `requires-python >=3.12`.

**Phase should address it:** Phase 0 merge hygiene and CI/test setup.

**Confidence:** HIGH from worktree audit.

## Minor Pitfalls

### Pitfall 1: Platform registry determinism becomes premature optimization target

**What goes wrong:** Time is spent optimizing registry name sorting before registry size matters.

**Prevention strategy:** Keep deterministic sorting for small built-in registries; revisit caching only if dynamic registries grow.

**Phase should address it:** No dedicated phase; monitor after backend/platform registry work.

**Confidence:** MEDIUM.

### Pitfall 2: README/documentation lags behind actual boundary decisions

**What goes wrong:** Contributors cannot tell fake backend fixtures from real SLAM support or planned APIs from implemented APIs.

**Prevention strategy:** After baseline merge, document package purpose, current modules, test command, fake-backend boundary, and out-of-scope integrations.

**Phase should address it:** Phase 0 or Phase 1 completion.

**Confidence:** HIGH.

### Pitfall 3: Benchmark artifacts become too large too early

**What goes wrong:** Evaluation writes full frames, maps, or splat dumps into JSON artifacts.

**Prevention strategy:** Use summary metrics plus typed evidence references; store large payloads separately only when explicitly requested.

**Phase should address it:** Phase 2 artifact schema and Phase 5 evaluation.

**Confidence:** HIGH.

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Warning Signs | Mitigation |
|-------------|----------------|---------------|------------|
| Phase 0: Baseline stabilization / merge hygiene | Planning against wrong checkout or mistaking plans for APIs | Main checkout tests collect zero tests; tasks reference planned namespaces as implemented | Merge/stabilize foundation worktree first; require executable tests for each namespace; update public API/README |
| Phase 1: Frame, pose, camera, splat foundation | Implicit frame semantics | No golden transform tests; ambiguous pose direction names | Pin pose direction, optical frames, handedness, timestamp units, covariance frames; add composition/inversion/projection fixtures |
| Phase 2: Serialization and artifact schemas | Ad hoc JSON/dicts proliferate | Local `to_json` helpers; evidence strings without types | Versioned schemas and round-trip tests for core, splat, backend result, benchmark, and evidence refs |
| Phase 3: Backend registry and lifecycle contracts | Fake backend treated as real SLAM | Contract tests only check splat count; no failure states | Add capability metadata, availability checks, failure semantics, diagnostics, reset-after-failure tests |
| Phase 3+: Heavy backend preparation | CUDA/native dependencies leak into core | Core imports heavy libs; optional deps fail at import time | Adapter modules, optional extras, backend registry, subprocess isolation seam, serialized transport |
| Phase 4: Posterior-aware fusion | Fusion becomes occupancy/map union | Output has no provenance, uncertainty, or conflict diagnostics | Strategy protocol over immutable snapshots; explicit frame compatibility; provenance-preserving diagnostics |
| Phase 5: Evaluation/regression | Backend demo precedes measurement | No machine-readable metrics; no deterministic scenarios | Build fake-backend benchmarks first; separate lifecycle/pose/map/query failures; stable artifact schemas |
| Phase 6: Thin agent posterior query seam | Raw splat/graph dumps to agents | Unbounded outputs; no provenance; nondeterministic ordering | Bounded typed query results, stable ordering, evidence refs, uncertainty summaries, local-only APIs |
| Phase 7: ARNA-informed memory layer | Observations stored as truth | Conflicts overwritten; no stale/conflicted status | Claim-with-evidence model, statuses, source/time/confidence/evidence metadata, conflict/staleness tests |
| Future real backend integration | Backend-specific assumptions rewrite protocols | Adapter needs fields not in contracts; diagnostics are dicts | Only integrate after phases 1-5; add backend-specific adapters without changing core contracts unless contract gap is proven |

## Roadmap Prevention Priorities

1. **Do not start with a real backend.** Stabilize the foundation worktree, frame semantics, serialization, registry contracts, and evaluation first. Real backend work without these gates is expensive guesswork.
2. **Make frame semantics the first hard gate.** Every later layer depends on transform direction, optical frame convention, timestamp precision, and covariance frame clarity.
3. **Add serialization before evaluation and agents.** Machine-readable artifacts and evidence references must be shared infrastructure, not per-feature afterthoughts.
4. **Keep fake backend and platform presets honest.** They are fixtures for contract tests, not evidence of SLAM correctness or calibrated robot support.
5. **Preserve uncertainty and provenance everywhere.** Splat fusion and agent memory must expose confidence, source, timestamp, conflict, staleness, and evidence rather than collapsing observations into truth.
6. **Keep Mosaic v1 headless and deterministic.** No ROS, Habitat runners, LLM providers, browser UI, robot command execution, or full ARNA reproduction in core v1.

## Sources

- `/home/prannayag/pragnition/robotics/mosaic/.planning/PROJECT.md` — project requirements, constraints, active scope, and out-of-scope boundaries. Confidence: HIGH.
- `/home/prannayag/pragnition/robotics/mosaic/.planning/codebase/CONCERNS.md` — main checkout concerns, missing implementation, fragile areas, test gaps, dependency risks. Confidence: HIGH.
- `/home/prannayag/pragnition/robotics/.mosaic-worktrees/splat-slam-foundation/.planning/codebase/CONCERNS.md` — active foundation worktree concerns including frame semantics, fake backend, serialization, registry, performance, Python version. Confidence: HIGH.
- `/home/prannayag/pragnition/robotics/mosaic/docs/argus-migration-plan.md` — clean-room migration principles, package shape, milestones, backend isolation, platform/fusion/evaluation/agent seams. Confidence: HIGH.
- `/home/prannayag/pragnition/robotics/mosaic/docs/superpowers/specs/2026-05-18-agent-friendly-representation-design.md` — layered belief graph, ARNA-informed memory/tool design, claims/evidence model, testing strategy, non-goals. Confidence: HIGH for Mosaic design intent.
- `/home/prannayag/pragnition/robotics/mosaic/outputs/arna-2506-17462-replication.md` — ARNA paper extraction, missing artifact status, memory/tool ablations, replication risks. Confidence: HIGH for absence of discovered public artifacts and paper-extracted facts; MEDIUM for implementation implications.
