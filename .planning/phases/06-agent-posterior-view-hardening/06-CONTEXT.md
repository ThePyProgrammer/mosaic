# Phase 6: Agent Posterior View Hardening - Context

**Gathered:** 2026-05-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 6 hardens the existing `mosaic.agents` posterior view so agent consumers can ask richer bounded questions over `SplatMap` snapshots through provider-free Python contracts.

This phase extends `SplatPosteriorView`, query/result contracts, determinism tests, and README boundary language around local spatial views, scene/map summaries, uncertainty summaries, and provenance summaries. It does not implement representation memories, scene graphs, spatial/raster memory, textual memory, belief/provenance stores, commitment memory, ARNA-style tool facades, LLM/LVLM providers, ROS/Habitat wrappers, robot execution, or real 3DGS backend behavior.

</domain>

<decisions>
## Implementation Decisions

### Uncertainty Summaries
- **D-01:** Add a separate `SplatPosteriorView.uncertainty()` method returning a typed uncertainty summary rather than expanding the existing `PosteriorSummary` shape.
- **D-02:** Base the Phase 6 uncertainty summary on covariance diagonal statistics plus opacity statistics. These fields already exist on `GaussianSplat` and support conservative posterior inspection without adding new backend assumptions.
- **D-03:** The uncertainty summary must carry a stable machine-readable semantics label `descriptive_only` to make clear that values are descriptive statistics over preserved splats, not calibrated belief, optimized posterior fusion, or reconstruction-quality scoring.
- **D-04:** Keep uncertainty summary scope global/map-level in Phase 6. Do not add per-provenance uncertainty breakdowns unless a later representation-memory phase requires them.

### Bounded Outputs
- **D-05:** Local spatial queries must be bounded by a required or default result limit so `query_local()` cannot become a raw full-map dump by default.
- **D-06:** Put the local-query limit on `LocalRadiusQuery` as an explicit request-boundary field such as `max_results`, rather than hiding it on the view object.
- **D-07:** When more splats match than the request limit, return bounded `splat_ids` plus stable truncation metadata such as total matches and a truncated flag. The result `count` should continue to describe returned IDs.
- **D-08:** Keep provenance summaries aggregate-only in Phase 6: source counts are allowed, but per-splat provenance records, evidence examples, and source-specific uncertainty records are out of scope.

### Determinism Coverage
- **D-09:** Repeated calls against the same fixed `SplatMap` snapshot must return exactly equal frozen dataclasses and immutable mappings for local, scene summary, uncertainty, and provenance queries.
- **D-10:** Local-query ordering should preserve existing `SplatMap.splats` tuple order and return the first matching IDs up to `max_results`; do not sort by distance in Phase 6.
- **D-11:** Numeric posterior summaries should use explicit fixed rounding, following the current six-decimal `mean_opacity` pattern, so exact-equality tests remain stable.
- **D-12:** Keep Phase 6 determinism coverage in `tests/agents/`. Do not add new evaluation-facing agent-query probes in this phase; Phase 5 owns evaluation harness work and can consume the hardened behavior later.

### Phase 7 Boundary
- **D-13:** Phase 6 must explicitly avoid all Phase 7 representation-memory concepts: no scene graph memory, spatial/raster memory, textual memory, belief/provenance memory store, commitment memory, navigation/perception/coordination tool families, or ARNA-style tool facade.
- **D-14:** Document the posterior-view vs future-memory boundary in both README language and tests, so the distinction is public and machine-checked.
- **D-15:** Do not add evidence/provenance references beyond aggregate provenance counts in Phase 6. Detailed evidence references belong to Phase 7 representation-memory contracts.
- **D-16:** Add uncertainty as the only new query family/method in Phase 6. Leave navigation, perception, coordination, belief/provenance, and memory/context query families to Phase 7.

### Claude's Discretion
No implementation areas were delegated to Claude discretion. Downstream agents should follow the decisions above.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Roadmap and Requirements
- `.planning/ROADMAP.md` — Defines Phase 6 goal, dependency on Phase 5, success criteria, and boundary with Phase 7 representation-memory work.
- `.planning/REQUIREMENTS.md` — Defines AGNT-02 and AGNT-04: bounded local/summary/uncertainty/provenance queries and repeated-query determinism.
- `.planning/PROJECT.md` — Captures project-level constraints: pure-Python foundation, provider-free agent APIs, bounded typed outputs, and no raw full splat-map dumps by default.
- `.planning/phases/05-evaluation-metric-and-failure-gate-hardening/05-CONTEXT.md` — Carries forward agent-query stability as an evaluation concern while keeping Phase 6 agent determinism coverage local to agent tests.
- `.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md` — Carries forward conservative uncertainty semantics and the `preserved_not_optimized`/non-calibrated posterior boundary from fusion diagnostics.

### Agent Posterior Design and Current Implementation
- `docs/superpowers/plans/2026-05-18-agent-posterior-query-seam.md` — Original agent posterior seam plan; defines the thin provider-free `SplatMap` query layer and explicitly defers final representation-memory models.
- `src/mosaic/agents/queries.py` — Current `AgentQueryKind`, `LocalRadiusQuery`, `SplatQueryResult`, `PosteriorSummary`, and `ProvenanceSummary` contracts to harden.
- `src/mosaic/agents/posteriors.py` — Current `SplatPosteriorView` implementation with `query_local()`, `summary()`, and `provenance()`.
- `src/mosaic/agents/__init__.py` — Public agent package export surface for stable new query/result types.
- `src/mosaic/__init__.py` — Root package export surface; update only for stable public Phase 6 APIs.

### Splat Inputs and Public Boundary
- `src/mosaic/splats/primitives.py` — Defines `GaussianSplat.center`, `covariance_upper`, `opacity`, and `provenance`, the fields used by bounded local queries and uncertainty summaries.
- `src/mosaic/splats/maps.py` — Defines immutable `SplatMap.splats` tuple order, which Phase 6 uses as the stable local-query result order.
- `README.md` — Public boundary note target for explaining bounded posterior views, uncertainty semantics, provider-free behavior, and the split between Phase 6 posterior summaries and Phase 7 representation memories/tools.

### Tests
- `tests/agents/test_queries.py` — Current query contract tests to extend for result limits, truncation metadata, uncertainty summary validation, and public agent exports.
- `tests/agents/test_splat_posterior.py` — Current posterior-view behavior tests to extend with bounded local queries, uncertainty summaries, and exact repeated-query determinism.
- `tests/test_public_api.py` — Public API export checks if new agent query/result types become root exports.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `LocalRadiusQuery` in `src/mosaic/agents/queries.py` already validates center shape and radius positivity; add the request-bound `max_results` validation here.
- `SplatQueryResult` in `src/mosaic/agents/queries.py` already reports returned ID count; extend it with total-match/truncation metadata without turning it into a raw-map carrier.
- `PosteriorSummary` and `ProvenanceSummary` already demonstrate frozen typed summary objects and immutable mappings suitable for the new uncertainty summary style.
- `SplatPosteriorView` in `src/mosaic/agents/posteriors.py` already performs deterministic tuple-order local queries and six-decimal mean-opacity rounding.
- `GaussianSplat` exposes `covariance_upper`, `opacity`, and `provenance` fields, enough to compute descriptive global uncertainty stats without new dependencies.
- `SplatMap.splats` is an immutable tuple, making map-order result stability straightforward.

### Established Patterns
- Public contracts are frozen dataclasses with validation in `__post_init__()` and explicit package `__all__` exports.
- The project uses provider-free pure-Python contracts with no runtime dependencies; Phase 6 must not import LLM SDKs, ROS, Habitat, tensor libraries, or backend packages.
- Tests use exact assertions over deterministic in-memory objects; no mocks are needed for current agent posterior behavior.
- Numeric summaries already use fixed rounding to six decimal places for deterministic equality.
- README boundary language is used to document what current reference APIs do and do not claim.

### Integration Points
- `src/mosaic/agents/queries.py` is the natural home for `AgentQueryKind.UNCERTAINTY`, `PosteriorUncertaintySummary` or equivalent, `LocalRadiusQuery.max_results`, and expanded `SplatQueryResult` metadata.
- `src/mosaic/agents/posteriors.py` should implement bounded local queries and `uncertainty()` over the existing `SplatMap` snapshot.
- `src/mosaic/agents/__init__.py` and possibly `src/mosaic/__init__.py` should expose only stable Phase 6 public agent APIs.
- `tests/agents/` should carry determinism and boundary coverage; avoid moving this phase's work into `tests/evaluation/`.
- `README.md` should receive a concise note that agent posterior APIs are bounded descriptive views over splat snapshots, not representation memories or provider/tool orchestration.

</code_context>

<specifics>
## Specific Ideas

- Use `descriptive_only` as the stable uncertainty semantics label.
- Treat covariance and opacity summaries as descriptive statistics over the current snapshot, not calibrated uncertainty or optimized posterior fusion.
- Preserve `SplatMap` tuple order for local query output stability.
- Keep provenance output aggregate-only until Phase 7 introduces evidence/provenance memory contracts.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 6-Agent Posterior View Hardening*
*Context gathered: 2026-05-19*
