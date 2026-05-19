# Phase 6: Agent Posterior View Hardening - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-19
**Phase:** 6-Agent Posterior View Hardening
**Areas discussed:** Uncertainty summaries, Bounded outputs, Determinism coverage, Phase 7 boundary

---

## Uncertainty Summaries

### Summary basis

| Option | Description | Selected |
|--------|-------------|----------|
| Covariance + opacity | Summarize covariance diagonal ranges and opacity/confidence-like bands; uses fields already present on `GaussianSplat` without claiming calibrated posterior probability. | ✓ |
| Covariance only | Keep uncertainty strictly geometric by summarizing covariance values; simpler but misses low-opacity evidence weakness. | |
| Let Claude decide | Planner chooses the conservative summary fields that best fit the current `SplatPosteriorView` and Phase 4/5 diagnostic patterns. | |

**User's choice:** Covariance + opacity
**Notes:** The summary should stay conservative and descriptive.

### Access surface

| Option | Description | Selected |
|--------|-------------|----------|
| Separate method | Add `SplatPosteriorView.uncertainty()` returning a typed summary, keeping the existing `summary()` stable and focused on counts/opacity. | ✓ |
| Extend summary | Add uncertainty fields directly to `PosteriorSummary`; fewer methods, but it changes the meaning and shape of an existing summary object. | |
| Both surfaces | Add a separate method and mirror a few totals into `summary()`; convenient, but risks duplicating state and expanding the basic summary too much. | |

**User's choice:** Separate method
**Notes:** Keep `summary()` stable.

### Semantics label

| Option | Description | Selected |
|--------|-------------|----------|
| descriptive_only | Makes clear the values are descriptive statistics over preserved splats, not calibrated belief or optimized posterior fusion. | ✓ |
| posterior_proxy | Signals that the summary approximates posterior uncertainty; more agent-friendly wording, but easier to overinterpret. | |
| No label | Rely on field names and docs/tests; simpler contract, but less machine-readable boundary for downstream agents. | |

**User's choice:** descriptive_only
**Notes:** Use a machine-readable boundary label.

### Provenance breakdown

| Option | Description | Selected |
|--------|-------------|----------|
| Global only | One bounded map-level summary for Phase 6; provenance-specific uncertainty can come later if representation memories need it. | ✓ |
| Per source | Include per-provenance uncertainty stats now; useful for agents comparing sensors, but expands result shape and testing complexity. | |
| Global + counts | Global uncertainty plus provenance counts; preserves current provenance behavior without per-source uncertainty stats. | |

**User's choice:** Global only
**Notes:** Per-source uncertainty is deferred.

---

## Bounded Outputs

### Local-query bound

| Option | Description | Selected |
|--------|-------------|----------|
| Required limit | Require or default a maximum result count for local queries, returning stable truncated IDs plus a total-match count. | ✓ |
| Aggregate only | Local queries return only counts/statistics, not splat IDs; safest boundary, but less useful for deterministic agent inspection. | |
| Caller detail level | Let callers choose aggregate vs IDs vs summaries; flexible, but adds more API surface than the current simple query contract. | |

**User's choice:** Required limit
**Notes:** Local queries must not become raw full-map dumps.

### Limit location

| Option | Description | Selected |
|--------|-------------|----------|
| On query object | Add `max_results` to `LocalRadiusQuery` so bounds are explicit at the request boundary and deterministic tests can vary it. | ✓ |
| On view object | Configure `SplatPosteriorView` with a default limit; convenient for one consumer, but less explicit per request. | |
| Hard-coded default | Use an internal default limit only; minimal API change, but callers cannot state their bounds clearly. | |

**User's choice:** On query object
**Notes:** Bounds belong at the request boundary.

### Truncation metadata

| Option | Description | Selected |
|--------|-------------|----------|
| IDs + total | Return bounded `splat_ids`, `count` for returned IDs, and `total_matches`/`truncated` metadata so consumers know evidence was clipped. | ✓ |
| IDs only | Keep the current result shape close to today; simple, but truncation is invisible unless documented elsewhere. | |
| IDs + summary | Return bounded IDs plus aggregate opacity/covariance stats over all matches; useful but overlaps with the uncertainty summary contract. | |

**User's choice:** IDs + total
**Notes:** Returned count and total-match count should be distinguishable.

### Provenance bounds

| Option | Description | Selected |
|--------|-------------|----------|
| Aggregate counts only | Keep `ProvenanceSummary` as aggregate source counts; no per-splat provenance records, so it stays bounded naturally. | ✓ |
| Top sources limit | Return only top N provenance sources plus total source count; useful for huge source sets, but changes behavior before scaling exists. | |
| Detailed optional | Add optional detail mode for per-source examples; helpful for debugging, but starts moving toward richer Phase 7 evidence views. | |

**User's choice:** Aggregate counts only
**Notes:** No per-splat provenance records in Phase 6.

---

## Determinism Coverage

### Main determinism contract

| Option | Description | Selected |
|--------|-------------|----------|
| Exact equality | Repeated calls against the same snapshot return equal frozen dataclasses/mappings for local, summary, uncertainty, and provenance queries. | ✓ |
| Stable fields only | Assert selected fields and tolerate other object-shape changes; less brittle, but weaker for downstream agent contracts. | |
| Artifact snapshots | Serialize query outputs and compare JSON-ready snapshots; useful for artifacts, but current agent results do not yet expose serialization helpers. | |

**User's choice:** Exact equality
**Notes:** Use exact dataclass and mapping equality.

### Local-query ordering

| Option | Description | Selected |
|--------|-------------|----------|
| Map order | Preserve current SplatMap tuple order and return the first matching IDs up to `max_results`; simplest and deterministic. | ✓ |
| Distance order | Sort matches by distance then ID; more intuitive for local neighborhoods, but changes current index-order behavior. | |
| Let Claude decide | Planner chooses the ordering that best matches the existing implementation and bounded-query contract. | |

**User's choice:** Map order
**Notes:** Do not sort by distance in Phase 6.

### Numeric stability

| Option | Description | Selected |
|--------|-------------|----------|
| Fixed rounding | Use explicit fixed rounding for mean/range values, following the current `mean_opacity` six-decimal pattern. | ✓ |
| Raw floats | Return Python float calculations directly; simpler, but less stable for exact equality and future artifact comparisons. | |
| Decimal strings | Return formatted strings for numeric summaries; very stable for JSON, but awkward for Python numeric consumers. | |

**User's choice:** Fixed rounding
**Notes:** Follow the existing six-decimal rounding pattern.

### Test scope

| Option | Description | Selected |
|--------|-------------|----------|
| Agent tests only | Phase 6 owns repeated-query tests in `tests/agents`; Phase 5 already defines evaluation-facing probes and can consume the stable behavior later. | ✓ |
| Also evaluation probe | Add a small evaluation-facing probe now; connects to Phase 5, but risks crossing into evaluation harness work after Phase 5 planning. | |
| Let Claude decide | Planner decides whether a minimal evaluation hook is necessary based on Phase 5 implementation state. | |

**User's choice:** Agent tests only
**Notes:** Do not expand evaluation harness in Phase 6.

---

## Phase 7 Boundary

### Memory concepts to avoid

| Option | Description | Selected |
|--------|-------------|----------|
| All Phase 7 memory | No scene graph, spatial/raster memory, textual memory, belief store, commitment memory, or tool facade; Phase 6 only hardens SplatMap-backed posterior views. | ✓ |
| Scene graph only | Avoid scene graph memory, but allow small evidence/provenance primitives if useful; more flexible, but boundary is blurrier. | |
| Let Claude decide | Planner decides which pieces are safely Phase 6 vs should wait for Phase 7. | |

**User's choice:** All Phase 7 memory
**Notes:** Keep Phase 6 strictly SplatMap-backed posterior hardening.

### Boundary documentation

| Option | Description | Selected |
|--------|-------------|----------|
| README + tests | Add concise public boundary language and tests that assert provider-free, memory-free posterior behavior. | ✓ |
| Tests only | Rely on contract tests to enforce behavior; less documentation work, but users may miss the future/now split. | |
| Context only | Keep it in planning context for now; fastest, but Phase 8 docs would carry all public explanation later. | |

**User's choice:** README + tests
**Notes:** The boundary should be both public and machine-checked.

### Evidence/provenance references

| Option | Description | Selected |
|--------|-------------|----------|
| No new refs | Keep provenance as aggregate counts only; detailed evidence references belong to Phase 7 representation memory contracts. | ✓ |
| Bounded examples | Allow a few bounded source examples in results; useful for agents, but begins adding evidence-view semantics. | |
| Let Claude decide | Planner decides based on what is easiest to add without crossing into Phase 7. | |

**User's choice:** No new refs
**Notes:** Detailed evidence belongs to Phase 7.

### New query kinds

| Option | Description | Selected |
|--------|-------------|----------|
| Only uncertainty | Add uncertainty as the one new query family/method; leave navigation, perception, coordination, and memory/context query families to Phase 7. | ✓ |
| No enum change | Add `uncertainty()` method without a new `AgentQueryKind`; minimal churn, but less complete as a query family contract. | |
| Let Claude decide | Planner decides whether `AgentQueryKind.UNCERTAINTY` is worth adding for API consistency. | |

**User's choice:** Only uncertainty
**Notes:** Add uncertainty only; no broader tool-family query kinds.

---

## Claude's Discretion

None.

## Deferred Ideas

None.
