# Phase 5: Evaluation Metric and Failure Gate Hardening - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-19
**Phase:** 5-Evaluation Metric and Failure Gate Hardening
**Areas discussed:** Failure taxonomy, Metric set, Artifact shape, Backend block

---

## Failure Taxonomy

### Primary failure-classification shape

| Option | Description | Selected |
|--------|-------------|----------|
| Typed enum | Use a closed enum such as lifecycle, trajectory, map_fusion, agent_query, and none; keeps artifacts stable and easy to gate. | ✓ |
| Free string | Keep failure_classification as arbitrary strings; easiest migration but weaker downstream guarantees. | |
| Multi-label set | Allow multiple failure classes per artifact; captures compound failures but complicates simple gate results. | |
| You decide | Let downstream planning choose the safest shape consistent with current BenchmarkArtifact and RegressionResult patterns. | |

**User's choice:** Typed enum
**Notes:** Current artifacts only store `failure_classification="none"`; Phase 5 should move to closed typed classes.

### Failure-class source

| Option | Description | Selected |
|--------|-------------|----------|
| Gate-derived | Each RegressionGate carries a failure class; failed gates classify the artifact. Fits current check_regression_gates flow. | ✓ |
| Runner-derived | run_slam_benchmark sets the class directly from backend lifecycle behavior; simpler artifact story but weaker for threshold failures. | |
| Separate classifier | Add a classifier over artifact + gate results; most flexible but more moving parts for Phase 5. | |
| You decide | Let planning choose based on the smallest compatible extension. | |

**User's choice:** Gate-derived
**Notes:** Regression gates should be the source of failure classification.

### Multiple failed gates

| Option | Description | Selected |
|--------|-------------|----------|
| Priority order | Use deterministic severity order: lifecycle before trajectory before map_fusion before agent_query, while retaining all failed gate results. | ✓ |
| First failure | Use the first failed gate in the provided gate tuple; simple but makes classification depend on caller ordering. | |
| No primary | Do not choose one primary class; require consumers to inspect all failed gate classes instead. | |
| You decide | Let planning choose the deterministic aggregation rule. | |

**User's choice:** Priority order
**Notes:** Keep all failed gate results, but derive primary class by priority.

### Lifecycle failure semantics

| Option | Description | Selected |
|--------|-------------|----------|
| Tracking states | Classify lost/not-initialized/error-like update states or incomplete scenario processing as lifecycle failures. | ✓ |
| Missing metrics only | Treat lifecycle failure as missing lifecycle metrics rather than interpreting backend update states. | |
| Runner exceptions | Only classify exceptions raised during benchmark execution as lifecycle failures. | |
| You decide | Let planning define the smallest testable lifecycle failure semantics. | |

**User's choice:** Tracking states
**Notes:** Lifecycle failures should reflect backend tracking state behavior.

---

## Metric Set

### Mandatory metric family

| Option | Description | Selected |
|--------|-------------|----------|
| Core lifecycle | Require update_count, tracking_success_rate, lost_tracking_count, and final_splat_count; minimal reliable baseline for every backend. | ✓ |
| All families | Require lifecycle, trajectory, map/fusion, and agent-query metrics in every artifact; comprehensive but forces placeholders early. | |
| Splat + gates | Keep splat_count as the only universal metric and let gates define everything else. | |
| You decide | Let planning choose mandatory metrics based on current deterministic backend support. | |

**User's choice:** Core lifecycle
**Notes:** Core lifecycle metrics are mandatory for every artifact.

### Trajectory consistency before real backends

| Option | Description | Selected |
|--------|-------------|----------|
| Hook metrics | Add JSON-ready placeholder/hook metrics such as trajectory_consistency_available and pose_delta_consistency, with deterministic fake-backend coverage where meaningful. | ✓ |
| Defer entirely | Do not add trajectory metrics until real backends provide poses; simplest but weakens EVAL-02. | |
| Synthetic only | Compute trajectory consistency solely from synthetic scenario expected poses, independent of backend output. | |
| You decide | Let planning choose the smallest trajectory hook satisfying EVAL-02 without pretending real accuracy. | |

**User's choice:** Hook metrics
**Notes:** Use hook metrics without claiming real trajectory accuracy.

### Map-quality metrics before real reconstruction quality

| Option | Description | Selected |
|--------|-------------|----------|
| Contract proxies | Use stable proxies like final_splat_count, map_frame_match, provenance/source counts, and fusion diagnostic presence; no real reconstruction-quality claims. | ✓ |
| Geometry scoring | Try center/covariance/color statistics as a map-quality score; richer but easy to overclaim. | |
| Defer map quality | Treat map quality as future real-backend scope and keep only splat_count now. | |
| You decide | Let planning select conservative map-quality proxies. | |

**User's choice:** Contract proxies
**Notes:** Map-quality metrics should remain conservative contract proxies.

### Agent-query stability metrics

| Option | Description | Selected |
|--------|-------------|----------|
| Determinism probes | Repeated bounded posterior queries over a fixed snapshot return identical result counts/summary/provenance values; no LLM/provider involvement. | ✓ |
| Presence only | Only record whether agent-query APIs are callable; easiest but shallow. | |
| Defer to Phase 6 | Do not include agent-query stability metrics until posterior hardening. | |
| You decide | Let planning choose the smallest stability hook that does not steal Phase 6 scope. | |

**User's choice:** Determinism probes
**Notes:** Agent-query metrics should test deterministic bounded posterior behavior without expanding Phase 6 semantics.

---

## Artifact Shape

### Metric representation

| Option | Description | Selected |
|--------|-------------|----------|
| Typed metric fields | Keep JSON-ready metric dicts but add typed MetricResult-style constructors/categories so names, units, and families stay stable. | ✓ |
| Plain dicts only | Continue with list[dict] only; simplest but less safe for downstream gates. | |
| Nested by family | Group metrics under lifecycle/trajectory/map/agent sections; readable but bigger artifact migration. | |
| You decide | Let planning choose the artifact structure compatible with current BenchmarkArtifact.as_dict(). | |

**User's choice:** Typed metric fields
**Notes:** Add stronger typed metric structure while keeping JSON-ready output.

### JSONL output

| Option | Description | Selected |
|--------|-------------|----------|
| Add JSONL | Keep stable JSON for one run and add JSONL for multiple scenario/backend runs; directly satisfies JSON/JSONL artifact language. | ✓ |
| JSON only | Keep write_benchmark_artifact as the only writer for now; simpler but leaves JSONL success criterion weaker. | |
| JSONL only | Move toward streaming-style artifacts; not ideal because current tests and consumers use JSON. | |
| You decide | Let planning choose if JSONL is worth adding in this phase. | |

**User's choice:** Add JSONL
**Notes:** Preserve JSON and add JSONL for multi-run output.

### Scenario metadata

| Option | Description | Selected |
|--------|-------------|----------|
| Stable summary | Add scenario name, frame/update count, camera IDs if available, and expected map frame; avoid dumping full observations. | ✓ |
| Name only | Keep current scenario_name only; minimal but weak for benchmark reproducibility. | |
| Full scenario dump | Serialize all observations into the benchmark artifact; complete but bloats artifacts and overlaps artifact-schema work. | |
| You decide | Let planning choose the smallest reproducibility metadata set. | |

**User's choice:** Stable summary
**Notes:** Include reproducibility metadata without dumping full observations.

### Diagnostics and typed gate/failure data

| Option | Description | Selected |
|--------|-------------|----------|
| Typed + mirrored keys | Add typed gate/failure result data and mirror selected scalar totals into diagnostics for compatibility. | ✓ |
| Typed only | Move gate/failure data out of diagnostics entirely; cleaner but may break existing artifact consumers. | |
| Diagnostics only | Keep all new data as flat diagnostic keys; fastest but recreates the current weak typing problem. | |
| You decide | Let planning balance artifact stability and typed contracts. | |

**User's choice:** Typed + mirrored keys
**Notes:** Preserve compatibility while adding typed structures.

---

## Backend Block

### Explicit blocker

| Option | Description | Selected |
|--------|-------------|----------|
| Passing gates | Document and test that real backend integration is blocked until the deterministic benchmark suite produces passing regression gates. | ✓ |
| Artifact exists | Block only until benchmark artifacts can be emitted; weaker because artifacts could encode failing behavior. | |
| Manual note | Keep the block as README/planning language only; no code-level enforcement in Phase 5. | |
| You decide | Let planning choose the concrete blocker mechanism. | |

**User's choice:** Passing gates
**Notes:** Real backend integration remains blocked until deterministic evaluation gates pass.

### Visibility

| Option | Description | Selected |
|--------|-------------|----------|
| Tests + README | Encode it in regression tests and concise README boundary language so both machines and humans see it. | ✓ |
| Tests only | Use code/tests as the only enforcement source; less documentation churn. | |
| README only | Document the policy but do not add a test for it. | |
| You decide | Let planning choose where the policy belongs. | |

**User's choice:** Tests + README
**Notes:** The block should be machine-checked and human-readable.

### Real-backend placeholders

| Option | Description | Selected |
|--------|-------------|----------|
| No placeholders | Keep the default registry deterministic-only, carrying forward Phase 3; block real backends without adding fake real-backend names. | ✓ |
| Metadata placeholder | Add a non-instantiable real-backend descriptor to demonstrate blocked status; more visible but risks implying support. | |
| Skipped contract case | Add a skipped optional-backend test case to show how future backends will be gated. | |
| You decide | Let planning choose whether a placeholder helps or hurts. | |

**User's choice:** No placeholders
**Notes:** Carry forward Phase 3 deterministic-only default registry stance.

### Unlock signal

| Option | Description | Selected |
|--------|-------------|----------|
| Phase-ready helper | Expose a small boolean/typed result such as evaluation_gates_passed over BenchmarkArtifact + gates; future backend plans can reference it directly. | ✓ |
| Regression tuple only | Rely on all RegressionResult.passed values; no extra helper. | |
| Artifact field | Store evaluation_ready directly in BenchmarkArtifact; convenient but risks stale derived state. | |
| You decide | Let planning choose the cleanest unlock signal. | |

**User's choice:** Phase-ready helper
**Notes:** Use a derived helper/result, not stale artifact state.

---

## Claude's Discretion

- Exact metric names, units, and helper boundaries may be chosen by planning, provided the locked families and conservative semantics are preserved.
- The concrete failure-priority implementation may be chosen by planning, provided lifecycle > trajectory > map/fusion > agent-query for primary classification.
- The phase-ready helper location may be chosen by planning, provided it derives from artifacts/gates rather than being stored as stale state on `BenchmarkArtifact`.

## Deferred Ideas

None.
