# Phase 5: Evaluation Metric and Failure Gate Hardening - Research

**Researched:** 2026-05-19 [VERIFIED: local date/context]
**Domain:** Pure-Python evaluation metrics, benchmark artifacts, regression failure taxonomy, and backend-integration readiness gates for Mosaic [CITED: /home/prannayag/pragnition/robotics/mosaic/.planning/ROADMAP.md]
**Confidence:** HIGH [VERIFIED: codebase inspection + official Python/pytest docs]

<user_constraints>
## User Constraints (from CONTEXT.md)

Source: `/home/prannayag/pragnition/robotics/mosaic/.planning/phases/05-evaluation-metric-and-failure-gate-hardening/05-CONTEXT.md` [VERIFIED: codebase Read]

### Locked Decisions
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

### Deferred Ideas (OUT OF SCOPE)
## Deferred Ideas

None — discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| EVAL-02 | Evaluation metrics cover splat counts, tracking/lifecycle status, trajectory consistency hooks, map-quality hooks, and agent-query stability hooks. [CITED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md] | Existing `MetricResult`, `splat_count_metric`, `SplatSlamUpdate`, `TrackingState`, `SplatMap`, fusion summaries, and `SplatPosteriorView` provide the raw inputs; Phase 5 should add typed metric families/constructors without runtime dependencies. [VERIFIED: codebase Read] |
| EVAL-04 | Regression gates can distinguish lifecycle failures, pose/trajectory failures, map/fusion failures, and agent-query failures. [CITED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md] | Existing `RegressionGate`, `RegressionResult`, and `check_regression_gates()` provide the minimum-threshold seam; Phase 5 should add a closed `StrEnum` failure class, attach it to gates/results, and derive primary class by priority. [VERIFIED: codebase Read] |
| EVAL-05 | The evaluation harness runs before real 3DGS backend integration is attempted. [CITED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md] | Existing default backend registry contains only `deterministic-splat`; README already defers real 3DGS backends; Phase 5 should add a typed readiness helper plus README/tests that keep real backends blocked until deterministic gates pass. [VERIFIED: codebase Read] |
</phase_requirements>

## Summary

Phase 5 should harden the existing Mosaic evaluation seam rather than replace it. `mosaic.evaluation.metrics`, `runner`, `regression`, and `scenarios` already exist; the current harness emits one `splat_count` metric, benchmark artifacts with flat diagnostics and `failure_classification="none"`, and minimum-threshold regression gates. [VERIFIED: codebase Read] The correct plan is to extend these contracts with typed metric families, scenario summaries, JSONL writing, gate-derived failure classes, and readiness checks while preserving current JSON-ready artifact behavior. [VERIFIED: codebase Read]

The phase must stay pure-Python and deterministic: no CUDA, PyTorch, OpenCV, ROS, Habitat, LLM SDK, real 3DGS backend, or sample real-backend descriptor belongs in this phase. [CITED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/05-evaluation-metric-and-failure-gate-hardening/05-CONTEXT.md] Use existing standard-library tools (`dataclasses`, `enum.StrEnum`, `json`, `MappingProxyType`) and the existing dev-test stack (`pytest`) only. [CITED: https://docs.python.org/3.14/library/dataclasses.html] [CITED: https://docs.python.org/3.14/library/enum.html#enum.StrEnum] [CITED: https://docs.python.org/3.14/library/json.html#json.dumps] [CITED: https://docs.pytest.org/en/stable/how-to/write_report_assertions_in_tests.html]

**Primary recommendation:** Plan three implementation waves: first metrics/artifact schema enrichment, then regression failure taxonomy/readiness gates, then README/public API/tests that enforce the real-backend block. [VERIFIED: codebase Read]

## Project Constraints (from CLAUDE.md)

- Mosaic is a typed, headless Python library for 3D Gaussian Splatting SLAM contracts over multi-view robotic systems. [CITED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Use Python 3.12+, `uv`, pure-Python foundation modules, and `pytest`; core imports must not require CUDA/native dependencies. [CITED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Real 3DGS/CUDA/research backends must remain behind protocols, registries, optional dependencies, and future isolation boundaries. [CITED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Evaluation must exist before backend integration. [CITED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Agent APIs must return bounded typed outputs with evidence/provenance, not raw full splat maps or provider-specific prompts. [CITED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Use `src/` layout, package-rooted imports, explicit public `__all__`, frozen/typed dataclasses, JSON-ready `as_dict()` boundaries, immutable tuples/mappings, and `MappingProxyType(dict(...))` for frozen mapping copies. [CITED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Avoid `print()` in library code; return typed diagnostics mappings instead. [CITED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Quality checks should use `uv run pytest ... -q`. [CITED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Metric family construction | Python library: `mosaic.evaluation.metrics` | `mosaic.slam`, `mosaic.splats`, `mosaic.fusion`, `mosaic.agents` as data sources | Metrics are evaluation-facing contracts, but their inputs come from backend updates, snapshots, fusion summaries, and posterior views. [VERIFIED: codebase Read] |
| Benchmark artifact enrichment | Python library: `mosaic.evaluation.runner` | Artifact helpers in `mosaic.artifacts.evaluation` | The runner owns benchmark execution and serialization shape; artifact helpers own versioned wrapper round-trips. [VERIFIED: codebase Read] |
| Regression failure classification | Python library: `mosaic.evaluation.regression` | README/tests | Regression gates already live here, and README/tests should expose/enforce the policy. [VERIFIED: codebase Read] |
| Real-backend integration block | Python library policy + tests | README documentation | The default registry is deterministic-only and the block must be both machine-checked and human-readable. [VERIFIED: codebase Read] |
| Agent-query stability hooks | Python library: `mosaic.evaluation.metrics` or `runner` probe helpers | `mosaic.agents.posteriors` | Stability probes should call deterministic posterior APIs over snapshots; they must not introduce provider behavior. [VERIFIED: codebase Read] |

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python standard library `dataclasses` | Python 3.12+ project target; local probe Python 3.14.4 | Frozen typed value/result objects with `__post_init__` validation and `slots=True`. | Official dataclasses support frozen instances, post-init validation hooks, and slots generation. [CITED: https://docs.python.org/3.14/library/dataclasses.html] |
| Python standard library `enum.StrEnum` | Python 3.12+ | Closed string-valued failure classifications. | `StrEnum` members are strings and can be serialized via their string values; this matches JSON-ready classifications. [CITED: https://docs.python.org/3.14/library/enum.html#enum.StrEnum] |
| Python standard library `json` | Python 3.12+ | Stable JSON/JSONL benchmark serialization. | `json.dumps(..., sort_keys=True)` sorts dictionary keys and is useful for regression tests; `indent=2` gives stable human-readable formatting. [CITED: https://docs.python.org/3.14/library/json.html#json.dumps] |
| Python standard library `types.MappingProxyType` | Python 3.12+ | Read-only views for copied diagnostic/metadata mappings. | `MappingProxyType` creates a read-only proxy, but it is dynamic over the underlying mapping; copy first with `dict(...)` to avoid caller mutation leakage. [CITED: https://docs.python.org/3/library/types.html#types.MappingProxyType] |
| `pytest` | Declared `>=8.4.0`; local `uv run pytest --version` reports 9.0.3; installed metadata reported 9.0.2 outside the uv environment | Unit and regression tests. | Official pytest docs support assert introspection and `pytest.raises(..., match=...)`; slopcheck rated `pytest` OK on PyPI. [CITED: https://docs.pytest.org/en/stable/how-to/write_report_assertions_in_tests.html] [VERIFIED: PyPI/slopcheck] |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| No new runtime package | N/A | Preserve `dependencies = []`. | Use for all Phase 5 implementation; adding runtime dependencies would violate the pure-Python foundation boundary. [VERIFIED: codebase Read] |
| Existing `mosaic.slam` contracts | Local package 0.1.0 | Tracking states, updates, backend metadata. | Lifecycle metrics and lifecycle failure gates. [VERIFIED: codebase Read] |
| Existing `mosaic.fusion` summaries | Local package 0.1.0 | Provenance, uncertainty, conflict diagnostics. | Conservative map/fusion proxy metrics only. [VERIFIED: codebase Read] |
| Existing `mosaic.agents` posterior view | Local package 0.1.0 | Deterministic local, summary, provenance queries over `SplatMap`. | Agent-query stability metrics; do not add LLM/provider integration. [VERIFIED: codebase Read] |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `StrEnum` | Plain string constants | Strings are easy to serialize but do not give a closed typed classification surface. [ASSUMED] |
| Standard-library `json` JSONL writer | Third-party JSONL package | Third-party package is unnecessary; JSON Lines requires one valid JSON value per line and line terminator `\n`, which `json.dumps` plus explicit newline can produce. [CITED: https://jsonlines.org/] |
| Existing `pytest` | Add Hypothesis/property tests | Property tests may be useful later, but Phase 5 can cover deterministic contracts with the existing pytest suite and should avoid adding packages. [ASSUMED] |

**Installation:**

```bash
# No new runtime packages for Phase 5.
uv sync
uv run pytest -q
```

**Version verification:**

```bash
python --version          # Python 3.14.4 locally; project target remains Python 3.12+
uv --version              # uv 0.10.10 locally
uv run pytest --version   # pytest 9.0.3 locally
pip index versions pytest # pytest (9.0.3) on PyPI during research
```

## Package Legitimacy Audit

No new external runtime packages should be installed for Phase 5. [VERIFIED: codebase Read]

| Package | Registry | Age | Downloads | Source Repo | slopcheck | Disposition |
|---------|----------|-----|-----------|-------------|-----------|-------------|
| `pytest` | PyPI | Existing dev dependency; exact age/downloads not retrieved | Not retrieved | `https://github.com/pytest-dev/pytest` from installed metadata | OK | Approved existing dev dependency; no new install required. [VERIFIED: PyPI/slopcheck] |

**Packages removed due to slopcheck [SLOP] verdict:** none. [VERIFIED: slopcheck]
**Packages flagged as suspicious [SUS]:** none. [VERIFIED: slopcheck]

## Architecture Patterns

### System Architecture Diagram

```text
SyntheticScenario + SplatSlamBackend
        |
        v
run_slam_benchmark()
        |
        +--> process each MultiViewObservation
        |       |
        |       +--> collect SplatSlamUpdate tracking_state, estimated_pose, diagnostics
        |
        +--> backend.snapshot() -> SplatMap
        |
        +--> metric family constructors
        |       +--> lifecycle metrics from updates/snapshot
        |       +--> trajectory hook metrics from estimated poses
        |       +--> map/fusion proxy metrics from SplatMap/Fusion summaries
        |       +--> agent-query stability probes from SplatPosteriorView
        |
        +--> BenchmarkArtifact
                +--> scenario_summary + backend_metadata + metrics + diagnostics
                +--> gate_results + failure_classification
                |
                +--> write_benchmark_artifact(.json)
                +--> write_benchmark_artifacts_jsonl(.jsonl)
                +--> check_regression_gates() -> RegressionResult tuple
                        |
                        +--> derive primary FailureClass by priority
                        +--> evaluation_ready_for_real_backend() boolean/helper
```

### Recommended Project Structure

```text
src/mosaic/evaluation/
├── metrics.py        # MetricResult, metric families, typed constructors, stability/proxy helpers
├── runner.py         # BenchmarkArtifact, scenario summary, JSON/JSONL writers, benchmark orchestration
├── regression.py     # FailureClass, RegressionGate, RegressionResult, priority classification, readiness helper
├── scenarios.py      # SyntheticScenario metadata source; likely small additions only
└── __init__.py       # Explicit public exports

tests/evaluation/
├── test_metrics.py      # Metric family/category/value validation and conservative hook semantics
├── test_runner.py       # Artifact shape, JSON/JSONL stability, scenario summaries, diagnostics mirrors
├── test_regression.py   # Failure classes, priority, gate-derived results, readiness helper
└── test_scenarios.py    # Scenario metadata behavior if extended
```

### Pattern 1: Closed String Failure Class
**What:** Define a `FailureClass(StrEnum)` with `NONE`, `LIFECYCLE`, `TRAJECTORY`, `MAP_FUSION`, and `AGENT_QUERY`; serialize with `.value` or `str(...)`. [CITED: https://docs.python.org/3.14/library/enum.html#enum.StrEnum]
**When to use:** Artifact classification, gate metadata, regression results, and readiness helper results. [VERIFIED: codebase Read]
**Example:**

```python
from enum import StrEnum

class FailureClass(StrEnum):
    NONE = "none"
    LIFECYCLE = "lifecycle"
    TRAJECTORY = "trajectory"
    MAP_FUSION = "map_fusion"
    AGENT_QUERY = "agent_query"
```

### Pattern 2: Metric Families With Stable JSON Shape
**What:** Keep `MetricResult.as_dict()` JSON-ready but add family/category fields or typed constructors so gate names remain stable. [VERIFIED: codebase Read]
**When to use:** Lifecycle, trajectory hook, map/fusion hook, and agent-query stability metrics. [CITED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/05-evaluation-metric-and-failure-gate-hardening/05-CONTEXT.md]
**Example:**

```python
@dataclass(frozen=True, slots=True)
class MetricResult:
    name: str
    value: float
    unit: str
    family: str = "core"

    def as_dict(self) -> dict[str, str | float]:
        return {"name": self.name, "value": self.value, "unit": self.unit, "family": self.family}
```

### Pattern 3: JSONL as One Artifact Per Line
**What:** Write each benchmark artifact as one valid JSON value followed by `\n`. [CITED: https://jsonlines.org/]
**When to use:** Multiple scenario/backend benchmark result files. [CITED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/05-evaluation-metric-and-failure-gate-hardening/05-CONTEXT.md]
**Example:**

```python
path.write_text("".join(json.dumps(item.as_dict(), sort_keys=True) + "\n" for item in artifacts))
```

### Anti-Patterns to Avoid
- **Claiming real geometric reconstruction quality:** Phase 5 metrics are lifecycle/contract proxies until a real backend exists. [CITED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/05-evaluation-metric-and-failure-gate-hardening/05-CONTEXT.md]
- **Missing-metric-only lifecycle failure:** Lifecycle failures must inspect tracking states and scenario processing completeness, especially `LOST` and `NOT_INITIALIZED`. [CITED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/05-evaluation-metric-and-failure-gate-hardening/05-CONTEXT.md]
- **Mutating caller-owned mappings:** `MappingProxyType` is a dynamic view, so wrap `dict(mapping)` before proxying. [CITED: https://docs.python.org/3/library/types.html#types.MappingProxyType]
- **Adding fake real-backend descriptors:** Phase 5 must carry forward deterministic-only default registry stance. [CITED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/05-evaluation-metric-and-failure-gate-hardening/05-CONTEXT.md]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Closed failure classification | Ad-hoc string comparisons scattered across runner/tests | `enum.StrEnum` | Provides typed enum members with string values suitable for JSON-ready artifacts. [CITED: https://docs.python.org/3.14/library/enum.html#enum.StrEnum] |
| Stable JSON serialization | Manual string concatenation for JSON objects | `json.dumps(..., sort_keys=True, indent=2)` for JSON and `json.dumps(..., sort_keys=True) + "\n"` per JSONL line | Official JSON supports sorted keys for regression comparisons; JSON Lines requires valid JSON per line. [CITED: https://docs.python.org/3.14/library/json.html#json.dumps] [CITED: https://jsonlines.org/] |
| Read-only artifact metadata | Custom immutable dict class | `MappingProxyType(dict(mapping))` | Built-in read-only proxy works if copied first to avoid dynamic caller mutation. [CITED: https://docs.python.org/3/library/types.html#types.MappingProxyType] |
| Backend behavior probes | Real backend scaffolds or CUDA placeholders | Existing `DeterministicSplatBackend`, `SplatSlamUpdate`, `TrackingState`, and contract tests | Phase 5 must keep real backend integration blocked. [VERIFIED: codebase Read] |
| Agent-query stability | LLM/provider calls or raw map dumps | Existing `SplatPosteriorView` deterministic local/summary/provenance methods | Agent APIs are provider-free and bounded. [VERIFIED: codebase Read] |

**Key insight:** Phase 5 is not about better SLAM; it is about making failures typed, deterministic, serializable, and impossible to wave away before real backend work starts. [CITED: /home/prannayag/pragnition/robotics/mosaic/.planning/ROADMAP.md]

## Common Pitfalls

### Pitfall 1: Treating `failure_classification` as a manually assigned artifact field
**What goes wrong:** Artifacts say `none` while gates fail, or different callers classify failures inconsistently. [ASSUMED]
**Why it happens:** The current `BenchmarkArtifact` stores a string field, and current gates do not carry failure classes. [VERIFIED: codebase Read]
**How to avoid:** Put `failure_class` on `RegressionGate` and `RegressionResult`; derive artifact/summary primary class from failed gate results. [CITED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/05-evaluation-metric-and-failure-gate-hardening/05-CONTEXT.md]
**Warning signs:** Tests manually pass `failure_classification="trajectory"` without failed trajectory gates. [ASSUMED]

### Pitfall 2: Overclaiming trajectory or map quality
**What goes wrong:** Metrics look like ATE/RMSE or reconstruction-quality scores without ground truth or a real optimizer. [ASSUMED]
**Why it happens:** SLAM evaluation terms are tempting, but Mosaic currently has a deterministic fake backend and contract-level artifacts. [VERIFIED: codebase Read]
**How to avoid:** Name metrics as hooks/proxies: `trajectory_pose_delta_consistent`, `trajectory_consistency_available`, `map_frame_matches_expected`, `fusion_diagnostics_present`. [CITED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/05-evaluation-metric-and-failure-gate-hardening/05-CONTEXT.md]
**Warning signs:** README or metric docs mention real reconstruction quality, loop closure, or geometric optimization for Phase 5. [ASSUMED]

### Pitfall 3: Breaking current artifact consumers
**What goes wrong:** Existing tests/consumers expecting flat diagnostics or `metrics` list of dictionaries fail unexpectedly. [ASSUMED]
**Why it happens:** Adding typed structures can accidentally replace old fields rather than extending them. [VERIFIED: codebase Read]
**How to avoid:** Preserve existing `as_dict()` top-level fields and mirror selected scalar totals into `diagnostics` while adding typed `scenario_summary`, `gate_results`, or metric family fields. [CITED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/05-evaluation-metric-and-failure-gate-hardening/05-CONTEXT.md]
**Warning signs:** `tests/evaluation/test_runner.py` requires wholesale rewriting instead of additive assertions. [ASSUMED]

### Pitfall 4: Writing invalid JSONL
**What goes wrong:** Multi-run benchmark files contain pretty-printed multi-line JSON objects or blank lines. [ASSUMED]
**Why it happens:** Reusing the single-run pretty JSON writer for JSONL. [VERIFIED: codebase Read]
**How to avoid:** Use one compact `json.dumps(artifact.as_dict(), sort_keys=True)` per line plus `\n`. [CITED: https://jsonlines.org/]
**Warning signs:** `path.read_text().splitlines()` yields more lines than artifacts. [ASSUMED]

## Code Examples

Verified patterns from official and local sources:

### Deterministic JSON for Regression Artifacts
```python
# Source: https://docs.python.org/3.14/library/json.html#json.dumps
json.dumps(artifact.as_dict(), indent=2, sort_keys=True) + "\n"
```

### JSONL Artifact Writer
```python
# Source: https://jsonlines.org/
lines = (json.dumps(artifact.as_dict(), sort_keys=True) + "\n" for artifact in artifacts)
path.write_text("".join(lines))
```

### Frozen Dataclass With Validation
```python
# Source: https://docs.python.org/3.14/library/dataclasses.html#post-init-processing
@dataclass(frozen=True, slots=True)
class RegressionGate:
    metric_name: str
    minimum: float
    failure_class: FailureClass

    def __post_init__(self) -> None:
        if not self.metric_name.strip():
            raise ValueError("RegressionGate metric_name must not be blank")
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Single `splat_count` metric only | Typed metric families covering lifecycle, trajectory hooks, map/fusion proxies, and agent-query stability hooks | Phase 5 planned | Planner should add metric constructors and tests rather than hard-code one metric in runner. [VERIFIED: codebase Read] |
| Artifact `failure_classification="none"` by default | Gate-derived failure class with deterministic priority | Phase 5 planned | Planner should classify from failed gate results, not from user-provided strings. [CITED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/05-evaluation-metric-and-failure-gate-hardening/05-CONTEXT.md] |
| JSON-only benchmark writer | JSON plus JSONL writer for multiple artifacts | Phase 5 planned | Planner should preserve current JSON writer and add separate JSONL writer. [CITED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/05-evaluation-metric-and-failure-gate-hardening/05-CONTEXT.md] |
| README says evaluation hardening is future work | README says real backend integration remains blocked until deterministic evaluation gates pass | Phase 5 planned | Planner should update README and tests so the policy is visible and checked. [CITED: /home/prannayag/pragnition/robotics/mosaic/.planning/ROADMAP.md] |

**Deprecated/outdated:**
- Treating `failure_classification` as an arbitrary string is outdated for Phase 5; use a closed typed enum and gate-derived classification. [CITED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/05-evaluation-metric-and-failure-gate-hardening/05-CONTEXT.md]
- Treating map-quality metrics as reconstruction-quality scores is out of scope; use conservative proxy metrics. [CITED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/05-evaluation-metric-and-failure-gate-hardening/05-CONTEXT.md]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Plain string constants are weaker than `StrEnum` for closed failure taxonomy. | Standard Stack Alternatives | Low; project could still use literals, but typed API quality would drop. |
| A2 | Property-based tests can wait until later. | Standard Stack Alternatives | Low; deterministic pytest cases satisfy current phase constraints, but future edge-case coverage may benefit from Hypothesis. |
| A3 | Some pitfall warning signs are inferred from common implementation failure modes. | Common Pitfalls | Low; tests can validate actual behavior. |

## Open Questions (RESOLVED)

1. **Should `MetricResult.value` remain `float` or become `bool | int | float | str`?**
   - What we know: Current `MetricResult.value` is `float`, while artifact diagnostics use `bool | int | float | str`. [VERIFIED: codebase Read]
   - RESOLVED: `MetricResult.value` remains numeric `float`. Boolean availability/stability is represented as `1.0`/`0.0` with `unit="flag"`, so threshold gates can compare metric values without widening the metric value type. [VERIFIED: checker revision decision]

2. **Where should the phase-ready helper live?**
   - What we know: Context permits `mosaic.evaluation.regression` or a neighboring evaluation module. [CITED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/05-evaluation-metric-and-failure-gate-hardening/05-CONTEXT.md]
   - RESOLVED: The readiness helper lives in `mosaic.evaluation.regression` and returns a small frozen typed result computed from a `BenchmarkArtifact` plus supplied regression gates. It must not be stored as a stale field on `BenchmarkArtifact`. [VERIFIED: checker revision decision]

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python | Library and tests | yes | 3.14.4 locally; project target `>=3.12` | None needed. [VERIFIED: Bash] |
| uv | Project workflow | yes | 0.10.10 | Use installed project environment; no alternative needed. [VERIFIED: Bash] |
| pytest | Validation | yes | 9.0.3 via `uv run pytest --version` | None needed. [VERIFIED: Bash] |
| CUDA/native CV/robot/LLM stacks | Not required; explicitly out of scope | not probed | N/A | Do not add. [CITED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md] |

**Missing dependencies with no fallback:** none for Phase 5. [VERIFIED: Bash]

**Missing dependencies with fallback:** none for Phase 5. [VERIFIED: Bash]

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 9.0.3 through `uv run pytest --version`. [VERIFIED: Bash] |
| Config file | `/home/prannayag/pragnition/robotics/mosaic/pyproject.toml` with `testpaths = ["tests"]` and `pythonpath = ["src"]`. [VERIFIED: codebase Read] |
| Quick run command | `uv run pytest tests/evaluation -q` |
| Full suite command | `uv run pytest -q` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| EVAL-02 | Metric families include splat count, lifecycle status, trajectory hook, map/fusion proxy, and agent-query stability. | unit | `uv run pytest tests/evaluation/test_metrics.py -q` | yes; extend existing file. [VERIFIED: codebase Read] |
| EVAL-03 carry-forward | Benchmark artifacts remain JSON-ready while adding scenario metadata and JSONL output. | unit/integration | `uv run pytest tests/evaluation/test_runner.py -q` | yes; extend existing file. [VERIFIED: codebase Read] |
| EVAL-04 | Regression gates distinguish lifecycle, trajectory, map/fusion, and agent-query failures and choose primary class by priority. | unit | `uv run pytest tests/evaluation/test_regression.py -q` | yes; extend existing file. [VERIFIED: codebase Read] |
| EVAL-05 | Real backend integration remains blocked until deterministic gates pass. | unit/documentation smoke | `uv run pytest tests/evaluation/test_regression.py tests/test_public_api.py -q` | yes; may need new README assertion test. [VERIFIED: codebase Read] |

### Sampling Rate
- **Per task commit:** `uv run pytest tests/evaluation -q` [VERIFIED: Bash]
- **Per wave merge:** `uv run pytest -q` [VERIFIED: Bash]
- **Phase gate:** Full suite green before `/gsd:verify-work`; current full suite reported 183 passed in 0.55s during research. [VERIFIED: Bash]

### Wave 0 Gaps
- [ ] Extend `/home/prannayag/pragnition/robotics/mosaic/tests/evaluation/test_metrics.py` for metric families/categories and hook/proxy semantics. [VERIFIED: codebase Read]
- [ ] Extend `/home/prannayag/pragnition/robotics/mosaic/tests/evaluation/test_runner.py` for scenario summary, JSONL output, gate/failure fields, and diagnostics mirrors. [VERIFIED: codebase Read]
- [ ] Extend `/home/prannayag/pragnition/robotics/mosaic/tests/evaluation/test_regression.py` for `FailureClass`, gate-derived classification, priority order, and readiness helper. [VERIFIED: codebase Read]
- [ ] Add or extend a README boundary test if the planner wants machine-checked documentation wording. [ASSUMED]

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | No authentication/session surface in Phase 5. [VERIFIED: codebase Read] |
| V3 Session Management | no | No sessions or web runtime in Phase 5. [VERIFIED: codebase Read] |
| V4 Access Control | no | No user roles, permissions, or service boundary in Phase 5. [VERIFIED: codebase Read] |
| V5 Input Validation | yes | Validate dataclass fields, metric names/units/families, finite numeric values, failure classes, and JSON-ready scalar mappings. [VERIFIED: codebase Read] |
| V6 Cryptography | no | No cryptographic behavior in Phase 5. [VERIFIED: codebase Read] |

### Known Threat Patterns for typed artifact/evaluation stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Artifact field injection via non-scalar diagnostics | Tampering | Keep artifact values to `bool | int | float | str`; validate keys and values before storing. [VERIFIED: codebase Read] |
| Misleading benchmark classification | Repudiation/Tampering | Derive failure classification from gate results, not arbitrary caller strings. [CITED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/05-evaluation-metric-and-failure-gate-hardening/05-CONTEXT.md] |
| Non-deterministic artifact output | Repudiation | Use sorted JSON keys and deterministic scenario/backend inputs. [CITED: https://docs.python.org/3.14/library/json.html#json.dumps] |
| Scope creep into real backend/native dependencies | Elevation of privilege/DoS by dependency boundary erosion | Keep default registry deterministic-only and add tests/docs for real-backend block. [CITED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/05-evaluation-metric-and-failure-gate-hardening/05-CONTEXT.md] |

## Sources

### Primary (HIGH confidence)
- `/home/prannayag/pragnition/robotics/mosaic/.planning/phases/05-evaluation-metric-and-failure-gate-hardening/05-CONTEXT.md` — locked Phase 5 decisions, scope, canonical references. [VERIFIED: codebase Read]
- `/home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md` — EVAL-02, EVAL-04, EVAL-05. [VERIFIED: codebase Read]
- `/home/prannayag/pragnition/robotics/mosaic/.planning/ROADMAP.md` — Phase 5 goal/success criteria and phase dependency. [VERIFIED: codebase Read]
- `/home/prannayag/pragnition/robotics/mosaic/src/mosaic/evaluation/*.py` and `/home/prannayag/pragnition/robotics/mosaic/tests/evaluation/*.py` — current implementation and tests. [VERIFIED: codebase Read]
- Python docs: dataclasses, enum.StrEnum, json, MappingProxyType. [CITED: https://docs.python.org/3.14/library/dataclasses.html] [CITED: https://docs.python.org/3.14/library/enum.html#enum.StrEnum] [CITED: https://docs.python.org/3.14/library/json.html#json.dumps] [CITED: https://docs.python.org/3/library/types.html#types.MappingProxyType]
- pytest docs for assertion/exception testing. [CITED: https://docs.pytest.org/en/stable/how-to/write_report_assertions_in_tests.html]
- JSON Lines format page. [CITED: https://jsonlines.org/]

### Secondary (MEDIUM confidence)
- Local environment probes for Python, uv, pytest, PyPI version listing, slopcheck result. [VERIFIED: Bash/PyPI/slopcheck]

### Tertiary (LOW confidence)
- Assumptions listed in the Assumptions Log. [ASSUMED]

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — no new runtime stack; official Python/pytest docs and local probes verify the tools. [VERIFIED: Bash + official docs]
- Architecture: HIGH — phase extends existing modules with explicit context decisions and code references. [VERIFIED: codebase Read]
- Pitfalls: MEDIUM — most pitfalls are derived from locked decisions and current code, while some warning signs are implementation-risk assumptions. [VERIFIED: codebase Read] [ASSUMED]

**Research date:** 2026-05-19 [VERIFIED: local date/context]
**Valid until:** 2026-06-18 for standard-library and local-code patterns; re-check package/tool versions if dependency policy changes. [ASSUMED]
