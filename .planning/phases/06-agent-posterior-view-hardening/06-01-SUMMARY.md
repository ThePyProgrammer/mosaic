---
phase: 06-agent-posterior-view-hardening
plan: 01
subsystem: agents
tags: [python, pytest, posterior-view, bounded-query, uncertainty]

requires:
  - phase: 05-evaluation-metric-and-failure-gate-hardening
    provides: Deterministic validation baseline for posterior-view hardening
provides:
  - Request-bound LocalRadiusQuery.max_results with truncation metadata on SplatQueryResult
  - Global descriptive PosteriorUncertaintySummary over covariance diagonal and opacity statistics
  - Focused tests for bounded local posterior views and uncertainty semantics
affects: [phase-06-agent-posterior-view-hardening, phase-07-representation-memories-and-tools]

tech-stack:
  added: []
  patterns:
    - Frozen dataclass posterior contracts with __post_init__ validation
    - Tuple-order bounded scans over immutable SplatMap snapshots
    - Six-decimal fixed rounding for exact posterior summary equality

key-files:
  created:
    - .planning/phases/06-agent-posterior-view-hardening/06-01-SUMMARY.md
  modified:
    - src/mosaic/agents/__init__.py
    - src/mosaic/agents/queries.py
    - src/mosaic/agents/posteriors.py
    - tests/agents/test_queries.py
    - tests/agents/test_splat_posterior.py

key-decisions:
  - "Kept local result bounding request-scoped on LocalRadiusQuery.max_results with default 32."
  - "Kept uncertainty descriptive and map-level only via PosteriorUncertaintySummary.semantics == descriptive_only."
  - "Preserved SplatMap.splats tuple order rather than sorting local query matches by distance."

patterns-established:
  - "Bounded agent posterior queries return returned IDs plus total_matches/truncated metadata, never raw splat payloads."
  - "Uncertainty summaries report descriptive covariance diagonal and opacity statistics without calibrated belief claims."

requirements-completed: [AGNT-02]

duration: 4 min
completed: 2026-05-21
---

# Phase 06 Plan 01: Agent Posterior View Hardening Summary

**Bounded local posterior queries with truncation metadata and descriptive covariance/opacity uncertainty summaries**

## Performance

- **Duration:** 4 min
- **Started:** 2026-05-21T01:48:00Z
- **Completed:** 2026-05-21T01:52:16Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments

- Added RED tests for request-bound local query limits, SplatQueryResult truncation metadata, AgentQueryKind.UNCERTAINTY, and PosteriorUncertaintySummary validation.
- Implemented LocalRadiusQuery.max_results with default 32 and positive validation, while preserving count as the returned-ID count.
- Implemented SplatPosteriorView.uncertainty() as a global descriptive summary over covariance_upper diagonal entries and opacity statistics rounded to six decimals.
- Preserved provider-free pure-Python agent modules and aggregate-only provenance behavior.

## Task Commits

Each task was committed atomically:

1. **Task 06-01-01: Lock bounded local and uncertainty contract tests** - `5634a5c` (test)
2. **Task 06-01-02: Implement bounded local results and descriptive uncertainty** - `1267eb8` (feat)

**Plan metadata:** pending final metadata commit

_Note: TDD tasks produced RED then GREEN commits._

## Files Created/Modified

- `src/mosaic/agents/__init__.py` - Exports `PosteriorUncertaintySummary` from the public agent package surface.
- `src/mosaic/agents/queries.py` - Adds `AgentQueryKind.UNCERTAINTY`, `LocalRadiusQuery.max_results`, bounded result metadata, and `PosteriorUncertaintySummary` validation.
- `src/mosaic/agents/posteriors.py` - Bounds local query results by request limit and adds global descriptive uncertainty summaries.
- `tests/agents/test_queries.py` - Covers query/result/uncertainty validation and public agent exports.
- `tests/agents/test_splat_posterior.py` - Covers bounded tuple-order local results and six-decimal uncertainty statistics.
- `.planning/phases/06-agent-posterior-view-hardening/06-01-SUMMARY.md` - Records plan execution outcome.

## Decisions Made

- Kept `LocalRadiusQuery.max_results` defaulted to `32`, matching the plan's safe positive default for preventing default raw full-map dumps.
- Stored `total_matches` and `truncated` on `SplatQueryResult`, while keeping `count` derived from returned IDs.
- Used `PosteriorUncertaintySummary.semantics == "descriptive_only"` to prevent calibrated belief or reconstruction-quality claims.
- Preserved tuple-order scans and did not introduce spatial indexes, backend adapters, provider SDKs, or Phase 7 representation-memory concepts.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Verification

- `uv run pytest tests/agents/test_queries.py tests/agents/test_splat_posterior.py -q` failed during RED with the expected missing `PosteriorUncertaintySummary` import before implementation.
- `uv run pytest tests/agents/test_queries.py tests/agents/test_splat_posterior.py tests/test_public_api.py -q` passed: 35 tests.
- `uv run pytest -q` passed: 224 tests.
- Forbidden dependency/import scan for provider, ROS, Habitat, tensor, spatial-index, and backend terms passed for `src/mosaic/agents/queries.py` and `src/mosaic/agents/posteriors.py`.

## Known Stubs

None.

## Threat Flags

None - this plan hardened existing agent posterior trust boundaries without adding network endpoints, auth paths, file access patterns, schema changes, or new runtime imports.

## TDD Gate Compliance

- RED gate present: `5634a5c test(06-01): add failing posterior hardening tests`
- GREEN gate present: `1267eb8 feat(06-01): harden agent posterior query bounds`
- Refactor gate: not needed

## Next Phase Readiness

Plan 06-02 can build on deterministic bounded local results and descriptive uncertainty summaries for repeated-query determinism hardening. Plan 06-03 can update public export/root documentation boundaries without needing implementation changes to local query limits or uncertainty behavior.

## Self-Check: PASSED

- Key modified files exist in the worktree.
- Task commits `5634a5c` and `1267eb8` exist in git history.
- Quick and full validation commands passed after implementation.

---
*Phase: 06-agent-posterior-view-hardening*
*Completed: 2026-05-21*
