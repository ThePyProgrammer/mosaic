---
phase: 05-evaluation-metric-and-failure-gate-hardening
plan: 03
subsystem: evaluation
tags: [failure-taxonomy, regression-gates, readiness-helper, backend-block]

requires:
  - phase: 05-evaluation-metric-and-failure-gate-hardening
    plan: 02
    provides: enriched BenchmarkArtifact gate_results field and lifecycle metric diagnostics
provides:
  - closed FailureClass enum with none/lifecycle/trajectory/map_fusion/agent_query values
  - gate-derived RegressionResult failure classes and priority primary classification
  - EvaluationReadinessResult and evaluation_ready_for_real_backend helper
  - regression artifact compatibility for failure_class serialization
  - additive BenchmarkArtifact gate result serialization tests
affects: [evaluation-regression, benchmark-artifacts, artifact-compatibility, backend-readiness]

tech-stack:
  added: []
  patterns:
    - closed StrEnum failure classes serialized through scalar enum values
    - frozen readiness result computed from artifact metrics and supplied gates
    - deterministic priority order lifecycle > trajectory > map_fusion > agent_query
    - versioned regression artifact backward compatibility for missing failure_class payloads

key-files:
  created:
    - .planning/phases/05-evaluation-metric-and-failure-gate-hardening/05-03-SUMMARY.md
  modified:
    - src/mosaic/evaluation/regression.py
    - src/mosaic/evaluation/__init__.py
    - src/mosaic/artifacts/evaluation.py
    - tests/evaluation/test_regression.py
    - tests/evaluation/test_runner.py

key-decisions:
  - "RegressionGate defaults to FailureClass.MAP_FUSION for source compatibility, while readiness tests use explicit lifecycle/trajectory/map_fusion/agent_query classes."
  - "Evaluation readiness is computed from supplied gates and artifact metrics and is not stored as stale derived state on BenchmarkArtifact."
  - "Primary failure classification ignores BenchmarkArtifact.failure_classification and derives from failed RegressionResult values only."

patterns-established:
  - "RegressionResult.as_dict() serializes failure_class as the enum value string."
  - "evaluation_ready_for_real_backend blocks empty, incomplete, or failing gate suites and reports missing required failure classes."
  - "Maximum-threshold gates support lifecycle count failures such as lost_tracking_count and not_initialized_tracking_count."

requirements-completed: [EVAL-04, EVAL-05]

duration: 9min
completed: 2026-05-19
---

# Phase 05 Plan 03: Failure Taxonomy and Readiness Gate Summary

**Gate-derived failure taxonomy and typed readiness checks now block real backend integration until deterministic lifecycle, trajectory, map-fusion, and agent-query gates all pass.**

## Performance

- **Duration:** 9 min
- **Started:** 2026-05-19
- **Completed:** 2026-05-19
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments

- Added RED tests for the closed `FailureClass` values, gate-derived failure classes, deterministic primary-class priority, full failed-result retention, and additive benchmark gate-result serialization.
- Implemented `FailureClass`, failure-aware `RegressionGate` and `RegressionResult`, `primary_failure_class()`, `EvaluationReadinessResult`, and `evaluation_ready_for_real_backend()`.
- Added readiness coverage for empty suites, incomplete suites, failing lifecycle gates, `lost_tracking_count`, `not_initialized_tracking_count`, and complete passing suites.
- Exported the new regression contracts from `mosaic.evaluation` and preserved versioned regression artifact round-trip compatibility.

## Task Commits

Each task was committed atomically:

1. **Task 05-03-01: Add failure taxonomy and priority tests** - `3eb9b27` (test)
2. **Task 05-03-02: Implement failure-aware gates and readiness helper** - `2d4150b` (feat)

Additional compatibility fix:

3. **Regression artifact compatibility update** - `42175bd` (fix)

## Files Created/Modified

- `src/mosaic/evaluation/regression.py` - Adds closed failure classes, failure-aware gates/results, priority derivation, maximum-threshold support, and readiness helper.
- `src/mosaic/evaluation/__init__.py` - Exports the new failure taxonomy and readiness contracts.
- `src/mosaic/artifacts/evaluation.py` - Serializes `failure_class` through regression artifacts and defaults older payloads for compatibility.
- `tests/evaluation/test_regression.py` - Locks failure taxonomy, gate-derived classification, priority behavior, lifecycle failure semantics, and readiness gating.
- `tests/evaluation/test_runner.py` - Locks additive benchmark gate-result serialization with failure-class values.

## Verification

- `uv run pytest tests/evaluation/test_regression.py tests/evaluation/test_runner.py -q` — passed, 19 tests.
- `uv run pytest tests/evaluation -q` — passed, 31 tests.
- `uv run pytest tests/artifacts/test_slam_and_evaluation_artifacts.py tests/evaluation -q` — passed, 41 tests.
- `uv run pytest -q` — passed, 201 tests.

## Decisions Made

- Kept `RegressionGate.failure_class` defaulted to `FailureClass.MAP_FUSION` only for source compatibility with existing direct constructors; readiness behavior requires explicit coverage of lifecycle, trajectory, map_fusion, and agent_query.
- Represented count-style lifecycle gates with `maximum=0.0`, allowing `lost_tracking_count` and `not_initialized_tracking_count` to fail when any such state appears.
- Returned a frozen `EvaluationReadinessResult` rather than mutating `BenchmarkArtifact`, preventing stale derived readiness state.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Preserved regression artifact compatibility after adding failure_class**
- **Found during:** Full-suite verification after Task 05-03-02
- **Issue:** Existing versioned regression artifact round-trip tests constructed `RegressionResult` without a `failure_class` and deserialized old payloads without that field.
- **Fix:** Added a conservative default failure class on direct `RegressionResult` construction and updated artifact serialization/deserialization to include `failure_class` while defaulting old payloads to `map_fusion`.
- **Files modified:** `src/mosaic/evaluation/regression.py`, `src/mosaic/artifacts/evaluation.py`
- **Verification:** `uv run pytest tests/artifacts/test_slam_and_evaluation_artifacts.py tests/evaluation -q && uv run pytest -q`
- **Committed in:** `42175bd`

---

**Total deviations:** 1 auto-fixed (1 Rule 1 bug)
**Impact on plan:** Compatibility was preserved without weakening gate-derived classification or readiness behavior.

## Issues Encountered

- The RED phase failed at import because `FailureClass` was not exported yet, satisfying the expected failing-test gate.
- Full-suite verification exposed stale versioned artifact compatibility assumptions after `RegressionResult` gained `failure_class`; fixed as a compatibility bug.

## Known Stubs

None detected in files created or modified by this plan.

## Threat Flags

| Flag | File | Description |
|------|------|-------------|
| threat_flag: readiness-boundary | `src/mosaic/evaluation/regression.py` | Readiness helper controls future real-backend integration; mitigated with closed enum classes, required class coverage, and deterministic priority tests. |
| threat_flag: gate-result-serialization | `src/mosaic/artifacts/evaluation.py` | Failure classes now cross artifact serialization boundaries; mitigated with scalar enum value serialization and backward-compatible deserialization. |

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Plan 05-04 can expose the readiness block in public API/README checks using `FailureClass`, `EvaluationReadinessResult`, and `evaluation_ready_for_real_backend()`.
- Real backend integration remains blocked unless a deterministic non-empty suite covers lifecycle, trajectory, map_fusion, and agent_query and all gates pass.

## Self-Check: PASSED

- Confirmed summary path exists before metadata commit.
- Confirmed task commits `3eb9b27`, `2d4150b`, and compatibility fix `42175bd` exist in git history.
- Confirmed modified code/test files exist and the full suite passes.

---
*Phase: 05-evaluation-metric-and-failure-gate-hardening*
*Completed: 2026-05-19*
