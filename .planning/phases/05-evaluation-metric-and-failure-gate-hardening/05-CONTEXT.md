# Phase 5: Evaluation Metric and Failure Gate Hardening - Context

**Gathered:** 2026-05-19
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 5 hardens the existing `mosaic.evaluation` harness so users can evaluate deterministic backend behavior, consume richer benchmark artifacts, classify regression failures, and keep real 3DGS backend integration blocked until evaluation gates exist and pass.

This phase extends metrics, benchmark JSON/JSONL artifacts, regression gates, and README/test boundary language. It does not integrate real 3DGS backends, add CUDA/native dependencies, implement real reconstruction-quality scoring, expand Phase 6 posterior-query semantics, or add provider/ROS/Habitat runtime integrations.

</domain>

<decisions>
## Implementation Decisions

### Failure Taxonomy
- **D-01:** Use a closed typed failure-classification enum for Phase 5 artifacts and gates. Required classes should cover at least `none`, `lifecycle`, `trajectory`, `map_fusion`, and `agent_query`.
- **D-02:** Failure classes should be gate-derived. Each regression gate should carry the failure class it represents, and failed gates classify the artifact or gate result.
- **D-03:** When multiple gates fail, choose the primary failure class by deterministic priority order: lifecycle before trajectory before map/fusion before agent-query. Keep all failed gate results available for inspection.
- **D-04:** Lifecycle failures should be based on backend tracking states and scenario processing completeness, especially `TrackingState.LOST`, `TrackingState.NOT_INITIALIZED`, or incomplete processing. Do not reduce lifecycle failure semantics to missing metrics only.

### Metric Set
- **D-05:** Every benchmark artifact should include a mandatory core lifecycle metric family, including update count, tracking success rate, lost tracking count, and final splat count or equivalent stable names.
- **D-06:** Trajectory consistency should be represented as hook metrics for now, not real accuracy claims. Use JSON-ready values such as trajectory-consistency availability and deterministic pose-delta consistency where current backend outputs support it.
- **D-07:** Map-quality metrics should stay conservative and contract-oriented while the deterministic fake backend is the only built-in backend. Use proxies such as final splat count, map-frame match, provenance/source counts, and fusion diagnostic presence. Do not claim real geometric reconstruction quality.
- **D-08:** Agent-query stability metrics should use deterministic probes over fixed `SplatMap` snapshots: repeated bounded posterior queries should return identical local result counts, summary values, and provenance values. Do not add LLM/provider behavior.

### Artifact Shape
- **D-09:** Keep benchmark metrics JSON-ready, but add typed metric-field constructors/categories around them so names, units, and families remain stable for gates and consumers.
- **D-10:** Preserve the current single-run JSON writer and add JSONL output for multiple scenario/backend benchmark results.
- **D-11:** Add stable scenario summary metadata to artifacts: scenario name, frame/update count, camera IDs when available, and expected map frame when available. Do not dump full observations into benchmark artifacts.
- **D-12:** Add typed gate/failure result data while mirroring selected scalar totals into the existing flat diagnostics mapping for compatibility with current artifact consumers.

### Backend Integration Block
- **D-13:** Real 3DGS backend integration must remain blocked until the deterministic benchmark suite produces passing regression gates.
- **D-14:** Make the backend-integration block visible in both tests and README boundary language so the policy is machine-checked and human-readable.
- **D-15:** Do not add real-backend placeholders, metadata-only fake real backends, or sample descriptors in Phase 5. Carry forward Phase 3's deterministic-only default registry stance.
- **D-16:** Add a small phase-ready typed helper or boolean result over `BenchmarkArtifact` plus regression gates so future real-backend plans can reference a clear evaluation-unlock signal.

### Claude's Discretion
- The planner may choose exact metric names, units, and helper boundaries, provided the metric families above are represented with JSON-ready typed contracts and conservative semantics.
- The planner may choose the concrete priority representation for failure classes, provided lifecycle outranks trajectory, trajectory outranks map/fusion, and map/fusion outranks agent-query when deriving the primary class.
- The planner may choose whether the phase-ready helper lives in `mosaic.evaluation.regression` or a neighboring evaluation module, provided it does not store stale derived state on `BenchmarkArtifact`.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Roadmap and Requirements
- `.planning/ROADMAP.md` — Defines Phase 5 goal, dependency on Phase 4, success criteria, and the real-backend block.
- `.planning/REQUIREMENTS.md` — Defines EVAL-02, EVAL-04, and EVAL-05: richer metrics, failure classification, regression gates, and evaluation-before-backend-integration.
- `.planning/PROJECT.md` — Captures project-level constraints: pure-Python foundation, backend isolation, evaluation before backend integration, and headless provider-free scope.
- `.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md` — Carries forward typed fusion diagnostics, conflict/uncertainty summaries, and the boundary that Phase 4 prepared diagnostics for Phase 5 gates.
- `.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md` — Carries forward deterministic-only default registry, on-demand availability, backend metadata, and reusable contract-test discipline.

### Current Evaluation Harness
- `src/mosaic/evaluation/metrics.py` — Current `MetricResult` and `splat_count_metric`; target for richer typed metric families.
- `src/mosaic/evaluation/runner.py` — Current `BenchmarkArtifact`, `run_slam_benchmark`, `write_benchmark_artifact`, backend metadata extraction, and flat diagnostics mapping.
- `src/mosaic/evaluation/regression.py` — Current `RegressionGate`, `RegressionResult`, and `check_regression_gates`; target for gate-derived failure classes and phase-ready helper.
- `src/mosaic/evaluation/scenarios.py` — Current `SyntheticScenario` and `synthetic_forward_sequence`; source of deterministic scenario metadata.
- `src/mosaic/evaluation/__init__.py` — Public evaluation export surface for stable new evaluation contracts.

### Cross-Domain Inputs for Metrics
- `src/mosaic/slam/protocol.py` — Defines `TrackingState`, `SplatSlamUpdate`, backend diagnostics, and lifecycle state values needed for lifecycle metrics and failure classes.
- `src/mosaic/fusion/protocol.py` — Defines typed fusion provenance, uncertainty, and conflict summaries that can feed conservative map/fusion metric proxies.
- `src/mosaic/fusion/strategies.py` — Current `ProvenancePreservingFusion` diagnostic labels and conflict summaries relevant to map/fusion gate probes.
- `src/mosaic/agents/posteriors.py` — Current deterministic `SplatPosteriorView` local, summary, and provenance query behavior for agent-query stability probes.
- `src/mosaic/agents/queries.py` — Current bounded agent query/result contracts and summary dataclasses.

### Tests and Documentation
- `tests/evaluation/test_metrics.py` — Existing metric validation and splat-count metric tests to extend with metric families/categories.
- `tests/evaluation/test_runner.py` — Existing benchmark artifact, metadata, diagnostics, and JSON writer tests to extend with richer artifacts and JSONL output.
- `tests/evaluation/test_regression.py` — Existing minimum-threshold gate tests to extend with failure classes, priority, and phase-ready helper behavior.
- `tests/evaluation/test_scenarios.py` — Existing deterministic scenario coverage relevant to scenario summary metadata.
- `tests/test_public_api.py` — Public API export checks if new evaluation types are root exports.
- `README.md` — Public boundary note target for explaining that real 3DGS backend integration remains blocked until deterministic evaluation gates pass.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `MetricResult` in `src/mosaic/evaluation/metrics.py` already provides a frozen typed metric contract with JSON-ready `as_dict()` output.
- `BenchmarkArtifact` in `src/mosaic/evaluation/runner.py` already freezes metrics, backend metadata, diagnostics, and exposes stable `as_dict()` serialization.
- `run_slam_benchmark()` already iterates a deterministic scenario through a backend, accumulates update diagnostics, snapshots the backend, and records backend capability metadata.
- `RegressionGate`, `RegressionResult`, and `check_regression_gates()` already provide the minimal regression-gate seam that can be extended with failure classes and gate readiness.
- `SyntheticScenario` and `synthetic_forward_sequence()` provide deterministic replay inputs and scenario names for artifact metadata.
- `TrackingState` and `SplatSlamUpdate` provide lifecycle states and estimated poses that can drive lifecycle and trajectory hook metrics.
- `SplatPosteriorView` already offers deterministic local, summary, and provenance queries over a fixed `SplatMap`, suitable for agent-query stability probes without Phase 6 scope creep.
- Phase 4 fusion summaries expose provenance, uncertainty, and conflict diagnostics that can feed conservative map/fusion proxy metrics.

### Established Patterns
- Public contracts are frozen dataclasses with explicit validation and JSON-ready `as_dict()` boundaries.
- Artifact-facing scalar maps use `bool | int | float | str` values and freeze caller-provided mappings with `MappingProxyType`.
- Tests use deterministic pure-Python objects, exact assertions, and no mocks for core/fake-backend behavior.
- Package submodules maintain explicit `__all__` export surfaces; root exports should be updated only for stable public APIs.
- Current evaluation artifacts already preserve stable JSON formatting with `indent=2`, `sort_keys=True`, and trailing newline.

### Integration Points
- Add richer metric constructors and family/category fields in `src/mosaic/evaluation/metrics.py`.
- Extend `src/mosaic/evaluation/runner.py` to populate lifecycle metrics, scenario summary metadata, typed gate/failure data, selected mirrored diagnostics, and JSONL output.
- Extend `src/mosaic/evaluation/regression.py` with a failure-class enum, gate-derived failure classes, deterministic priority selection, and the phase-ready helper.
- Extend `tests/evaluation/` for metrics, artifact shape, JSONL writer behavior, regression failure classification, and backend-block readiness.
- Update `README.md` with concise boundary language that real backend integration remains blocked until deterministic evaluation gates pass.

</code_context>

<specifics>
## Specific Ideas

- Use conservative metric semantics: lifecycle and contract proxies are allowed; real geometric reconstruction-quality scoring is not.
- Keep the artifact backward-compatible where practical by mirroring important scalar totals into `diagnostics` while adding typed structures for new gate/failure data.
- Keep the default backend registry deterministic-only and do not imply any real backend support through placeholders.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 5-Evaluation Metric and Failure Gate Hardening*
*Context gathered: 2026-05-19*
