---
phase: 05-evaluation-metric-and-failure-gate-hardening
plan: 01
subsystem: evaluation
tags: [metrics, pytest, artifacts, deterministic-evaluation]

requires:
  - phase: 04-fusion-diagnostics-and-semantics-hardening
    provides: typed fusion diagnostics and provenance summaries for conservative map/fusion proxy metrics
  - phase: 03-backend-registry-and-contracts
    provides: backend lifecycle tracking states and deterministic update contracts
provides:
  - typed MetricResult family field with JSON-ready serialization
  - lifecycle, trajectory-hook, map-quality, map-fusion, and agent-query metric constructors
  - artifact round-trip compatibility for metric family payloads
affects: [evaluation-runner, regression-gates, benchmark-artifacts, agent-posterior-queries]

tech-stack:
  added: []
  patterns:
    - frozen typed metric contracts with non-blank family validation
    - conservative hook/proxy metrics using numeric flags and counts only
    - deterministic repeated posterior-query stability probes

key-files:
  created:
    - .planning/phases/05-evaluation-metric-and-failure-gate-hardening/05-01-SUMMARY.md
  modified:
    - src/mosaic/evaluation/metrics.py
    - src/mosaic/evaluation/__init__.py
    - src/mosaic/artifacts/evaluation.py
    - tests/evaluation/test_metrics.py
    - tests/evaluation/test_runner.py
    - tests/artifacts/test_slam_and_evaluation_artifacts.py

key-decisions:
  - "MetricResult.family defaults to general for source/backward construction compatibility while metric constructors emit specific Phase 5 families."
  - "Trajectory and map metrics are named as availability, consistency, frame-match, provenance-count, and diagnostic-presence hooks/proxies rather than real accuracy or reconstruction-quality scores."

patterns-established:
  - "Metric families serialize as name/value/unit/family dictionaries with numeric float values."
  - "Agent-query stability metrics repeat SplatPosteriorView local, summary, and provenance methods over a fixed snapshot and encode equality as flag metrics."

requirements-completed: [EVAL-02]

duration: 4min
completed: 2026-05-19
---

# Phase 05 Plan 01: Evaluation Metric Families Summary

**Typed deterministic metric families for lifecycle state, trajectory hooks, map/fusion proxies, and repeated agent posterior-query stability**

## Performance

- **Duration:** 4 min
- **Started:** 2026-05-19T09:15:49Z
- **Completed:** 2026-05-19T09:19:35Z
- **Tasks:** 2
- **Files modified:** 6

## Accomplishments

- Added `MetricResult.family` validation and serialization while preserving numeric JSON-ready metric values.
- Implemented deterministic constructors for lifecycle metrics, trajectory hook flags, conservative map/fusion proxy metrics, and agent-query stability probes.
- Updated artifact round-trip handling and existing runner/artifact tests so metric family payloads remain stable across serialization boundaries.

## Task Commits

Each task was committed atomically:

1. **Task 05-01-01: Add metric family contract tests** - `6e8658f` (test)
2. **Task 05-01-02: Implement deterministic metric constructors** - `75a368c` (feat)

**Plan metadata:** committed separately after this summary.

_Note: TDD tasks used a RED test commit followed by a GREEN implementation commit._

## Files Created/Modified

- `src/mosaic/evaluation/metrics.py` - Adds metric family validation plus lifecycle, trajectory, map/fusion, and agent-query constructors.
- `src/mosaic/evaluation/__init__.py` - Exports stable Phase 5 metric constructors.
- `src/mosaic/artifacts/evaluation.py` - Preserves metric family during artifact deserialization and defaults older payloads to `general`.
- `tests/evaluation/test_metrics.py` - Locks exact family-aware metric contracts and deterministic constructor behavior.
- `tests/evaluation/test_runner.py` - Updates benchmark metric shape expectations for family-aware serialization.
- `tests/artifacts/test_slam_and_evaluation_artifacts.py` - Updates metric artifact round-trip assertions for family payloads.

## Verification

- `uv run pytest tests/evaluation/test_metrics.py -q` — passed, 8 tests.
- `uv run pytest tests/evaluation -q` — passed, 18 tests.
- `uv run pytest -q` — passed, 188 tests.

## Decisions Made

- Kept `MetricResult.family` defaulted to `general` so direct existing constructors remain source-compatible while Phase 5 constructors emit precise families.
- Used `map_quality` for snapshot/map proxy metrics and `map_fusion` only for fusion diagnostic presence, matching the plan's conservative quality-vs-fusion distinction.
- Represented hook/probe booleans as `1.0` or `0.0` with `unit="flag"`, keeping all metric values numeric.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Updated dependent artifact and runner expectations for family-aware metric dictionaries**
- **Found during:** Task 05-01-02 (Implement deterministic metric constructors)
- **Issue:** Adding `family` to `MetricResult.as_dict()` correctly changed benchmark and metric-artifact payload shapes, causing existing tests to fail on stale exact dictionaries.
- **Fix:** Updated `tests/evaluation/test_runner.py`, `tests/artifacts/test_slam_and_evaluation_artifacts.py`, and `src/mosaic/artifacts/evaluation.py` to preserve and assert metric family payloads while accepting older artifacts with a `general` default.
- **Files modified:** `src/mosaic/artifacts/evaluation.py`, `tests/evaluation/test_runner.py`, `tests/artifacts/test_slam_and_evaluation_artifacts.py`
- **Verification:** `uv run pytest tests/evaluation/test_metrics.py -q && uv run pytest tests/evaluation -q && uv run pytest -q`
- **Committed in:** `75a368c`

---

**Total deviations:** 1 auto-fixed (1 Rule 1 bug)
**Impact on plan:** Required compatibility fix for the planned metric serialization change. No scope creep beyond metric/artifact correctness.

## Issues Encountered

- The RED phase failed at import because the new metric constructors did not exist yet, satisfying the expected failing-test gate.
- Full-suite verification exposed stale artifact expectations after adding the `family` field; resolved as the Rule 1 auto-fix above.

## Known Stubs

None detected in files created or modified by this plan.

## Threat Flags

| Flag | File | Description |
|------|------|-------------|
| threat_flag: serialization-boundary | `src/mosaic/artifacts/evaluation.py` | Metric family now crosses the metric artifact serialization boundary; mitigated with scalar payload shape and round-trip tests. |

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Plan 02 can enrich benchmark artifacts and JSONL output using the stable `name`/`value`/`unit`/`family` metric shape.
- Regression-gate work can threshold lifecycle, trajectory, map/fusion, and agent-query metric families without adding CUDA/native/LLM dependencies.

## Self-Check: PASSED

- Confirmed created summary path exists.
- Confirmed task commits `6e8658f` and `75a368c` exist in git history.
- Confirmed modified code/test files exist and full test suite passes.

---
*Phase: 05-evaluation-metric-and-failure-gate-hardening*
*Completed: 2026-05-19*
