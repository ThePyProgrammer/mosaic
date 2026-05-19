# Phase 4: Fusion Diagnostics and Semantics Hardening - Context

**Gathered:** 2026-05-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 4 hardens the existing `mosaic.fusion` seam so users can trust it as a splat-native protocol with explicit provenance, uncertainty, conflict, and non-occupancy-grid semantics.

This phase extends diagnostics and tests around the deterministic `ProvenancePreservingFusion` strategy. It does not implement real Gaussian optimization, cross-frame alignment, voxel/occupancy-grid fusion, evaluation regression gates, real 3DGS backends, or agent posterior query expansion.

</domain>

<decisions>
## Implementation Decisions

### Diagnostic Shape
- **D-01:** Keep `FusionResult.diagnostics` as a JSON-ready machine-readable mapping, but add typed summary objects alongside it.
- **D-02:** Use fusion-prefixed summary names such as `FusionProvenanceSummary`, `FusionUncertaintySummary`, and `FusionConflictSummary` so these diagnostics do not blur into existing agent posterior summaries like `mosaic.agents.ProvenanceSummary`.
- **D-03:** Make provenance, uncertainty, and conflicts first-class typed fields on `FusionResult`; selected flat diagnostic keys should mirror key totals for artifact stability.
- **D-04:** Expose provenance detail as source map count, source splat count, fused splat count, and per-provenance counts. Do not add full per-output-splat lineage or stable splat IDs in this phase unless the existing model already supports them cleanly.

### Conflict Semantics
- **D-05:** Treat conservative overlap-plus-mismatch cases as fusion conflict candidates: nearby/overlapping splats from different provenance sources whose covariance, opacity, or color summaries disagree enough to be suspicious.
- **D-06:** Conflict detection should be deterministic and conservative. Prefer obvious center-distance/covariance-radius overlap plus mismatch over sensitive heuristics that create noisy false alarms.
- **D-07:** `FusionConflictSummary` should expose total conflict candidate count, involved provenance pairs, and reason counts such as overlap/color, overlap/opacity, or overlap/covariance mismatch. Avoid exposing individual splat-pair records unless required for tests.
- **D-08:** Conflicts remain diagnostics for the reference strategy. `ProvenancePreservingFusion` should still return `FusionStatus.FUSED` when conflicts are found because it preserves inputs rather than rejecting or optimizing them.

### Uncertainty Summary
- **D-09:** The exact reference-strategy uncertainty policy is delegated to downstream planning, but it should stay conservative and preserve the current "preserved, not optimized" meaning unless tests justify more.
- **D-10:** `FusionUncertaintySummary` should include a stable model label plus covariance diagonal range/stat summaries such as min, max, and mean. These are diagnostics over preserved source splats, not calibrated posterior-fusion claims.
- **D-11:** Phase 4 should prepare deterministic uncertainty fields for Phase 5 evaluation work, but should not add regression gates or threshold policy now.
- **D-12:** `ProvenancePreservingFusion` should communicate non-optimization through an explicit stable machine-readable label such as `preserved_not_optimized` in both the typed summary and flat diagnostics.

### Anti-Occupancy-Grid Tests
- **D-13:** The priority of the first anti-grid behavior test is delegated to downstream planning; choose behavior-focused tests that prove splat/posterior semantics rather than cosmetic API assertions.
- **D-14:** Include a conflict case where two overlapping splats from different provenance sources are both preserved in the fused output while conflict diagnostics record the mismatch.
- **D-15:** Verify the non-optimization boundary in both tests and a concise README/public-doc note: the reference strategy preserves and diagnoses splats but does not optimize Gaussians.
- **D-16:** Tests should assert both typed summary values and selected flat diagnostic keys so Python consumers and JSON/artifact consumers remain stable.

### Claude's Discretion
- The planner may choose the exact conservative uncertainty policy for `ProvenancePreservingFusion`, provided it preserves the explicit `preserved_not_optimized` boundary and does not claim real posterior optimization.
- The planner may choose the strongest initial anti-grid behavior test, provided it demonstrates splats are preserved as splats and not collapsed into occupancy cells.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Roadmap and Requirements
- `.planning/ROADMAP.md` — Defines Phase 4 goal, dependencies, success criteria, and boundaries with Phase 5 evaluation work.
- `.planning/REQUIREMENTS.md` — Defines FUSE-02 and FUSE-04: provenance/source diagnostics, uncertainty/conflict summaries, machine-readable status, and anti-occupancy-grid tests.
- `.planning/PROJECT.md` — Captures project-level constraints: pure-Python foundation, splat/posterior-native representation, headless library boundary, and no real backend integration in v1.
- `.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md` — Carries forward machine-readable diagnostics, dependency-light contracts, and deterministic contract-test discipline from Phase 3.

### Fusion Design and Current Implementation
- `docs/superpowers/plans/2026-05-18-posterior-aware-splat-fusion.md` — Original fusion seam plan; defines `ProvenancePreservingFusion` as deterministic and not real Gaussian optimization.
- `src/mosaic/fusion/protocol.py` — Current `FusionInput`, `FusionResult`, `FusionStatus`, `SplatFusionStrategy`, and flat diagnostics mapping to extend.
- `src/mosaic/fusion/strategies.py` — Current `ProvenancePreservingFusion` concatenates splats and reports only counts plus `uncertainty_model`.
- `src/mosaic/fusion/__init__.py` — Public fusion export surface that should expose stable typed diagnostics if added.
- `src/mosaic/__init__.py` — Root public export surface; update only for stable public APIs.

### Splat and Agent Surfaces
- `src/mosaic/splats/primitives.py` — Current `GaussianSplat` fields available for deterministic conflict/uncertainty summaries: center, covariance_upper, color_rgb, opacity, provenance.
- `src/mosaic/splats/maps.py` — Current immutable `SplatMap` frame/splats container used as fusion input/output.
- `src/mosaic/agents/queries.py` — Existing agent `ProvenanceSummary` naming collision to avoid with fusion-prefixed summary types.

### Tests and Documentation
- `tests/fusion/test_fusion_protocol.py` — Current fusion input/result validation and diagnostics freezing tests to extend.
- `tests/fusion/test_strategies.py` — Current provenance-preserving strategy tests to extend with typed summaries, conflict diagnostics, and anti-grid behavior.
- `tests/test_public_api.py` — Public API export checks if new fusion diagnostics become root exports.
- `README.md` — Public boundary note target for explaining that the reference fusion strategy preserves/diagnoses splats and does not optimize Gaussians.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `FusionInput` in `src/mosaic/fusion/protocol.py` already validates non-empty inputs and shared map frames.
- `FusionResult` in `src/mosaic/fusion/protocol.py` already freezes a JSON-ready diagnostics mapping; Phase 4 should extend rather than remove it.
- `ProvenancePreservingFusion` in `src/mosaic/fusion/strategies.py` already preserves input splats by concatenation and reports basic source/fused counts.
- `GaussianSplat` in `src/mosaic/splats/primitives.py` already exposes center, covariance, color, opacity, and provenance fields that are enough for deterministic diagnostic summaries.
- Existing `mosaic.agents.ProvenanceSummary` proves summary dataclass patterns exist, but fusion summaries need distinct names.

### Established Patterns
- Public contracts are frozen dataclasses with explicit `__all__` exports.
- Diagnostics and benchmark-facing values are JSON-ready scalar mappings.
- Tests use direct object construction, exact assertions, and deterministic pure-Python reference implementations rather than mocks.
- Root exports are stable public API and should be changed only when the new fusion diagnostics are intended for package-level consumption.

### Integration Points
- `src/mosaic/fusion/protocol.py` is the natural home for `FusionProvenanceSummary`, `FusionUncertaintySummary`, `FusionConflictSummary`, and any expanded `FusionResult` fields.
- `src/mosaic/fusion/strategies.py` should populate typed summaries and mirror selected scalar totals into `diagnostics`.
- `tests/fusion/` should carry most behavior coverage; `tests/test_public_api.py` should cover any new root exports.
- `README.md` should receive the concise public boundary note requested for non-optimization semantics.

</code_context>

<specifics>
## Specific Ideas

- Use fusion-prefixed summary type names to avoid confusion with existing agent posterior summaries.
- Keep conflict handling diagnostic-only for the deterministic reference strategy.
- Preserve both overlapping splats in anti-grid tests while surfacing conflict diagnostics.
- Use an explicit model label such as `preserved_not_optimized` instead of relying on prose or class names.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 4-Fusion Diagnostics and Semantics Hardening*
*Context gathered: 2026-05-19*
