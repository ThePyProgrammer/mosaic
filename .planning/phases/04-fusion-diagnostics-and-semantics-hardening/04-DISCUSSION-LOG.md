# Phase 4: Fusion Diagnostics and Semantics Hardening - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-19
**Phase:** 4-Fusion Diagnostics and Semantics Hardening
**Areas discussed:** Diagnostic shape, Conflict semantics, Uncertainty summary, Anti-grid tests

---

## Diagnostic shape

### Main result surface

| Option | Description | Selected |
|--------|-------------|----------|
| Typed + flat | Add typed summary fields for provenance/uncertainty/conflict while preserving a JSON-ready diagnostics mapping. | ✓ |
| Flat only | Keep only the diagnostics mapping and standardize keys. | |
| Typed only | Replace diagnostics with typed summaries. | |
| You decide | Let downstream planning choose the shape. | |

**User's choice:** Typed + flat
**Notes:** Existing `FusionResult.diagnostics` remains useful for artifacts and simple consumers, but Phase 4 should add stronger typed contracts.

### Summary naming

| Option | Description | Selected |
|--------|-------------|----------|
| Fusion-prefixed | Use `FusionProvenanceSummary`, `FusionUncertaintySummary`, and `FusionConflictSummary`. | ✓ |
| Generic names | Use shorter generic names such as `ProvenanceSummary`. | |
| Nested result | Create one `FusionDiagnostics` dataclass. | |
| You decide | Let downstream planning choose names. | |

**User's choice:** Fusion-prefixed
**Notes:** Avoid collision/confusion with existing `mosaic.agents.ProvenanceSummary`.

### First-class groups

| Option | Description | Selected |
|--------|-------------|----------|
| All three | Provenance, uncertainty, and conflicts as typed fields, with flat diagnostics mirroring totals. | ✓ |
| Conflict only | Add typed conflict data only. | |
| One aggregate | Use one `FusionDiagnostics` field wrapping all groups. | |
| You decide | Let downstream planning pick the minimal field set. | |

**User's choice:** All three
**Notes:** FUSE-02 needs provenance, source diagnostics, uncertainty/conflict summaries, and machine-readable status.

### Provenance detail

| Option | Description | Selected |
|--------|-------------|----------|
| Counts + ids | Source/fused counts and per-provenance counts without inventing stable splat IDs. | ✓ |
| Counts only | Only source map/splat/fused totals. | |
| Full lineage | Per-output-splat lineage back to source map/index. | |
| You decide | Let planning choose detail level. | |

**User's choice:** Counts + ids
**Notes:** Capture per-provenance identity/count information using existing `GaussianSplat.provenance`; do not create full lineage in this phase.

---

## Conflict semantics

### Conflict definition

| Option | Description | Selected |
|--------|-------------|----------|
| Overlap + mismatch | Report nearby/overlapping cross-provenance splats when covariance/opacity/color summaries disagree. | ✓ |
| Provenance only | Report same-region multi-source overlap without comparing attributes. | |
| No detection | Add structures only, no detection. | |
| You decide | Let planning define the heuristic. | |

**User's choice:** Overlap + mismatch
**Notes:** Conflict candidates should be deterministic heuristic diagnostics, not optimization results.

### Heuristic strictness

| Option | Description | Selected |
|--------|-------------|----------|
| Conservative | Flag obvious center-distance/covariance-radius overlap plus mismatch. | ✓ |
| Sensitive | Flag any nearby cross-provenance splats. | |
| Exact only | Only flag identical/nearly identical centers with mismatched attributes. | |
| You decide | Let planning pick thresholds. | |

**User's choice:** Conservative
**Notes:** Prefer stable tests and low false-alarm risk.

### Conflict summary contents

| Option | Description | Selected |
|--------|-------------|----------|
| Counts + reasons | Total candidates, provenance pairs, and reason counts. | ✓ |
| Only count | Only conflict candidate count. | |
| Pair records | Individual splat index pairs and reasons. | |
| You decide | Let planning choose the smallest useful structure. | |

**User's choice:** Counts + reasons
**Notes:** Avoid exposing per-pair records unless later needed.

### Status behavior

| Option | Description | Selected |
|--------|-------------|----------|
| Diagnostics only | Keep `FusionStatus.FUSED`; report conflicts in diagnostics. | ✓ |
| Warn status | Add status such as `FUSED_WITH_CONFLICTS`. | |
| Reject conflicts | Return `REJECTED` whenever conflicts are found. | |
| You decide | Let planning decide if status expansion is needed. | |

**User's choice:** Diagnostics only
**Notes:** `ProvenancePreservingFusion` preserves inputs rather than rejecting or optimizing them.

---

## Uncertainty summary

### Reference uncertainty policy

| Option | Description | Selected |
|--------|-------------|----------|
| Preserved only | Report uncertainty as preserved from source splats, not optimized. | |
| Aggregate stats | Compute summary stats such as covariance diagonal min/max/mean. | |
| Risk bands | Classify low/medium/high uncertainty risk. | |
| You decide | Let downstream planning choose a cautious summary. | ✓ |

**User's choice:** You decide
**Notes:** Downstream planning should bias toward conservative preserved-not-optimized semantics unless tests justify more.

### Summary data

| Option | Description | Selected |
|--------|-------------|----------|
| Ranges + model | Model label plus covariance diagonal min/max/mean and source counts. | ✓ |
| Model only | Only report `preserved-not-optimized`. | |
| Per-source stats | Group uncertainty stats by provenance/source. | |
| You decide | Let planning pick the smallest useful summary. | |

**User's choice:** Ranges + model
**Notes:** Aggregate diagnostics are allowed as long as they are not presented as calibrated posterior optimization.

### Evaluation gates

| Option | Description | Selected |
|--------|-------------|----------|
| Prepare only | Expose deterministic fields now; Phase 5 decides thresholds/gates. | ✓ |
| Add gates now | Add simple pass/fail gates now. | |
| Docs only | Document semantics without structured fields. | |
| You decide | Let planning avoid Phase 5 scope creep. | |

**User's choice:** Prepare only
**Notes:** Regression gate policy belongs to Phase 5.

### Non-optimization signal

| Option | Description | Selected |
|--------|-------------|----------|
| Explicit label | Use stable machine-readable label such as `preserved_not_optimized`. | ✓ |
| Boolean flag | Expose `optimized=False`. | |
| Class name only | Rely on `ProvenancePreservingFusion` name and docs. | |
| You decide | Let planning pick the representation. | |

**User's choice:** Explicit label
**Notes:** The label should appear in typed summary and flat diagnostics.

---

## Anti-grid tests

### First anti-grid behavior

| Option | Description | Selected |
|--------|-------------|----------|
| Preserve duplicates | Overlapping/identical-center splats from different provenance remain distinct. | |
| No voxel API | Assert outputs stay as `SplatMap`/`GaussianSplat`, no grid/cell concepts. | |
| Source order | Assert deterministic source-map order in output splats. | |
| You decide | Let planning pick the strongest anti-grid test. | ✓ |

**User's choice:** You decide
**Notes:** Downstream agents should choose behavior-focused tests, not cosmetic API assertions.

### Conflict-preservation case

| Option | Description | Selected |
|--------|-------------|----------|
| Yes preserve | Overlapping mismatch creates conflict diagnostics while preserving both splats. | ✓ |
| No separate | Keep conflict and anti-grid tests separate. | |
| Reject overlap | Treat overlapping mismatch as rejected fusion. | |
| You decide | Let planning combine or separate coverage. | |

**User's choice:** Yes preserve
**Notes:** This test should prove anti-grid behavior and diagnostic-only conflict handling together.

### Non-optimization boundary

| Option | Description | Selected |
|--------|-------------|----------|
| Tests + README note | Behavior tests plus concise public documentation. | ✓ |
| Tests only | Keep the boundary only in tests. | |
| Doc only | Document without extra tests. | |
| You decide | Let planning decide minimal docs. | |

**User's choice:** Tests + README note
**Notes:** Roadmap success criteria include documented boundaries.

### Diagnostic stability tests

| Option | Description | Selected |
|--------|-------------|----------|
| Both surfaces | Assert typed summaries and selected flat diagnostic keys. | ✓ |
| Typed only | Test typed fields only. | |
| Flat only | Test artifact-style keys only. | |
| You decide | Let planning choose API stability level. | |

**User's choice:** Both surfaces
**Notes:** Stabilize both Python typed consumers and JSON/artifact consumers.

---

## Claude's Discretion

- Exact conservative uncertainty policy for `ProvenancePreservingFusion`, while preserving the explicit `preserved_not_optimized` boundary.
- Strongest initial anti-grid behavior test selection, while proving splats remain splats and are not collapsed into occupancy cells.

## Deferred Ideas

None.
