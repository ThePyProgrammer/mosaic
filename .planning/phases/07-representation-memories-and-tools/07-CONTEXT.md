# Phase 7: Representation Memories and Tools - Context

**Gathered:** 2026-05-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 7 adds ARNA-informed representation-memory contracts and deterministic tool/query methods for agent-friendly access across perception, navigation, coordination, belief/provenance, and memory/context use cases.

This phase turns the Phase 6 bounded posterior-view boundary into a richer provider-free representation layer: typed IDs, entities, relations, evidence references, source metadata, claims, conflict/staleness status, spatial/raster memory, scene graph memory, text memory, belief/provenance memory, commitment memory, synthetic update helpers, and deterministic scenario coverage. It does not integrate LLM/LVLM providers, ROS/Habitat, robot execution, real object detection, real splat-to-occupancy extraction, persistent storage, distributed synchronization, or real 3DGS backend behavior.

Phase 7 depends on Phase 6 hardening of `SplatPosteriorView`; downstream agents must verify Phase 6 state before planning execution order.

</domain>

<decisions>
## Implementation Decisions

### Memory Scope and Shape
- **D-01:** Implement all five representation memory families as first-class Phase 7 contracts: spatial/raster memory, scene graph memory, text memory, belief/provenance memory, and commitment memory.
- **D-02:** Expose one aggregate representation-memory object as the primary caller-facing model. Callers should not need to manually compose separate stores for normal use.
- **D-03:** The aggregate memory object should own the five memory families and be the place where deterministic tool/query methods live.
- **D-04:** Use immutable update semantics by default: operations return new representation-memory snapshots rather than mutating caller-owned state in place.
- **D-05:** Include deterministic synthetic update helpers that can turn test fixtures into memory entries. These helpers may create cells, entities, relations, claims, notes, and commitments, but they must not claim real perception, real object detection, or real splat-to-occupancy extraction.

### Claim, Evidence, and Belief Semantics
- **D-06:** When two active robot reports contradict each other, keep both claims and mark the conflict visible. Do not auto-resolve by latest report, confidence ranking, or hidden winner selection.
- **D-07:** Conflicted claims should remain queryable through belief/provenance and tool results so agent consumers can inspect uncertainty rather than receiving silently merged truth.
- **D-08:** Claims should carry explicit `valid_until`-style expiry data. A deterministic transition helper should mark claims stale when a supplied timestamp passes that expiry.
- **D-09:** Evidence references should be typed but opaque: evidence kind plus opaque URI/string is enough. Phase 7 must not dereference or load evidence payloads by default.
- **D-10:** Every claim should carry required numeric confidence in the closed interval `[0, 1]`, even when synthetic tests use simple deterministic values.

### Tool/Query Surface
- **D-11:** Do not introduce a separate facade class for the initial tool surface. Put named deterministic query methods directly on the aggregate representation-memory object.
- **D-12:** Satisfy the one-query-per-family roadmap requirement with explicitly named methods rather than a generic `query(request)` dispatcher. Suitable initial method families include perception/search, navigation/reasoning, coordination/commitment, belief/provenance, and memory/context.
- **D-13:** Tool/query results should include bounded returned items plus relevant claim IDs, evidence references, status, and confidence where applicable. Results should be useful to an agent without exposing a raw full memory dump.
- **D-14:** List-like queries must accept request-level bounds such as `max_results` or `max_items` and return truncation metadata when more entries match than were returned.

### Scenario and Ablation Coverage
- **D-15:** Phase 7 should use three equal small deterministic scenario anchors: blocked path, search frontier, and task allocation. Do not treat one as the sole primary smoke path.
- **D-16:** The blocked-path scenario should cover conflicting traversability/blockage reports, visible conflicted claims, stale state where relevant, and route/blockage explanation behavior.
- **D-17:** The search-frontier scenario should cover spatial/raster frontier state, scene graph or context updates, and uncertainty about what remains unexplored or unconfirmed.
- **D-18:** The task-allocation scenario should cover commitment memory, robot/task/resource assignment or reservation, and conflict detection for coordination.
- **D-19:** ARNA-style memory ablation tests should be capability-oriented: removing a required memory family should block or degrade the corresponding query capability. Do not make numeric performance claims in Phase 7.
- **D-20:** Scenario coverage should live in the evaluation test area/harness rather than only under agent unit tests. Keep the representation implementation provider-free and deterministic, but route scenario validation through evaluation-facing tests so REPR-08 is visible as scenario coverage.

### Claude's Discretion
- The planner may choose exact class, enum, method, and module names, provided they follow existing Mosaic naming/export patterns and preserve the decisions above.
- The planner may choose the exact minimal fields for each memory family, provided all REPR-01 through REPR-08 requirements remain covered and all five memories are first-class contracts.
- The planner may choose how synthetic update helpers are factored, provided they are deterministic, pure-Python, and do not imply real perception/extraction support.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Roadmap and Requirements
- `.planning/ROADMAP.md` — Defines Phase 7 goal, dependency on Phase 6, success criteria, and REPR requirements coverage.
- `.planning/REQUIREMENTS.md` — Defines REPR-01 through REPR-08: typed IDs/entities/relations/evidence/query families, belief claims, spatial/raster memory, scene graph memory, text memory, commitment memory, tool facade, and scenario tests.
- `.planning/PROJECT.md` — Captures project-level constraints: pure-Python foundation, provider-free agent APIs, bounded typed outputs, and no raw full splat-map dumps by default.
- `.planning/STATE.md` — Current workflow position; verify Phase 6 completion state before execution planning because Phase 7 depends on Phase 6.

### Prior Phase Decisions
- `.planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md` — Carries forward Phase 6 boundaries: posterior views stay bounded/provider-free, detailed evidence references and representation memories belong to Phase 7, and raw full map dumps remain out of scope.
- `.planning/phases/05-evaluation-metric-and-failure-gate-hardening/05-CONTEXT.md` — Carries forward evaluation readiness, deterministic scenario/gate discipline, and agent-query stability as an evaluation concern.
- `.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md` — Carries forward conservative uncertainty/provenance semantics and the rule that conflicts should remain visible rather than hidden by optimization claims.

### Representation and ARNA Design Inputs
- `.planning/references/superpowers/specs/2026-05-18-agent-friendly-representation-design.md` — Primary representation design: layered belief graph plus ARNA-style memory/tool separation, memory families, claim model, tool families, flows, and scenario ideas.
- `.planning/references/arna/arna-2506-17462-replication.md` — ARNA evidence summary: memory/tool orchestration, textual/raster/scene graph memories, navigation/reasoning tools, ablation lessons, and lack of public implementation artifacts.
- `.planning/references/superpowers/plans/2026-05-18-agent-friendly-representation.md` — Prior planning reference for agent-friendly representation work if present; use as historical input, not as a substitute for this context.

### Current Agent and Splat Interfaces
- `src/mosaic/agents/queries.py` — Current agent query/result contracts and enum pattern; Phase 7 should extend the provider-free typed style, not bypass it.
- `src/mosaic/agents/posteriors.py` — Current `SplatPosteriorView` implementation; Phase 7 should build representation memories above bounded posterior access rather than expose raw maps.
- `src/mosaic/agents/__init__.py` — Current public agent export surface; update for stable Phase 7 symbols only.
- `src/mosaic/splats/maps.py` — Current immutable `SplatMap` snapshot container that may feed synthetic memory updates or evidence references.
- `src/mosaic/splats/primitives.py` — Current `GaussianSplat` fields available for bounded posterior/evidence context; do not require real extraction from these fields in Phase 7.
- `src/mosaic/core/frames.py` — Current `FrameId`/timestamp style to reuse for memory frame/time semantics where appropriate.

### Tests and Evaluation Integration
- `tests/agents/test_queries.py` — Current agent query contract tests; extend for low-level representation dataclasses if useful.
- `tests/agents/test_splat_posterior.py` — Current posterior-view behavior tests; keep Phase 7 boundary from regressing into raw map access.
- `tests/evaluation/test_runner.py` — Existing evaluation artifact/scenario pattern; candidate integration point for Phase 7 scenario coverage.
- `tests/evaluation/test_regression.py` — Existing gate/failure classification pattern; useful if Phase 7 scenarios need evaluation-facing classifications.
- `tests/test_public_api.py` — Public API export checks if stable Phase 7 representation types become root exports.
- `README.md` — Public boundary note target for explaining that representation memories/tools are deterministic Python contracts, not LLM, ROS, Habitat, or robot execution integrations.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `AgentQueryKind`, `LocalRadiusQuery`, `SplatQueryResult`, `PosteriorSummary`, and `ProvenanceSummary` in `src/mosaic/agents/queries.py` show the current frozen dataclass and enum style for provider-free agent-facing contracts.
- `SplatPosteriorView` in `src/mosaic/agents/posteriors.py` shows the current bounded-query layer over `SplatMap` snapshots. Phase 7 should sit above this and should not expose raw full splat maps to agents.
- `SplatMap` and `GaussianSplat` provide immutable snapshot and provenance-bearing primitive inputs that can be referenced by evidence refs or synthetic update helpers.
- Existing evaluation modules already support deterministic benchmark/scenario thinking, making `tests/evaluation/` a natural home for Phase 7 scenario coverage.

### Established Patterns
- Mosaic public contracts use frozen dataclasses, typed enums, validation in `__post_init__()`, immutable tuples/mappings, and explicit `__all__` export lists.
- Public APIs remain pure-Python and provider-free; do not import LLM SDKs, ROS/Habitat, tensor libraries, CUDA/native packages, or robot execution dependencies.
- Existing tests use deterministic in-memory objects and exact assertions rather than mocks.
- Bounded outputs and raw-map avoidance are already core agent-boundary rules from prior phases.
- Diagnostics/provenance should stay machine-readable, not prose-only.

### Integration Points
- Add Phase 7 representation contracts under `src/mosaic/agents/` or a clearly named child module/package that preserves the provider-free agent boundary.
- Update `src/mosaic/agents/__init__.py` for stable public representation-memory contracts and query result types.
- Update `src/mosaic/__init__.py` only for stable root-level APIs that should be part of the package public surface.
- Add scenario coverage in `tests/evaluation/` while keeping lower-level unit coverage near the representation contracts.
- Update README boundary language to distinguish Phase 6 posterior views, Phase 7 representation memories/tools, and deferred runtime integrations.

</code_context>

<specifics>
## Specific Ideas

- Use one aggregate `RepresentationMemory`-style object that owns spatial/raster, scene graph, text, belief/provenance, and commitment memories.
- Prefer named query methods on the memory object, such as object/hazard search, traversability/frontier query, commitment listing/conflict detection, claim comparison/staleness check, and context summary retrieval.
- Keep contradiction handling visibility-first: conflicting claims remain present and marked, rather than silently choosing a winner.
- Use explicit expiry for staleness and required `[0, 1]` confidence for claims.
- Treat blocked path, search frontier, and task allocation as equal deterministic scenario anchors.
- Use ARNA-style ablations as capability-blocking tests, not performance benchmarks.

</specifics>

<deferred>
## Deferred Ideas

- LLM/LVLM provider wrappers around Mosaic tools — deferred to v2/runtime integration work.
- ROS, Habitat, robot command execution, and full ARNA benchmark reproduction — deferred outside v1 Phase 7.
- Persistent storage/database-backed representation memories — deferred until in-memory contracts prove insufficient.
- Real object detection, room segmentation, and real splat-to-raster extraction — deferred to future perception/extraction phases.
- Distributed multi-robot synchronization — deferred until local memory contracts stabilize.

</deferred>

---

*Phase: 7-Representation Memories and Tools*
*Context gathered: 2026-05-21*
