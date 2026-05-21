---
phase: 06-agent-posterior-view-hardening
plan: 02
subsystem: agents
tags: [python, pytest, posterior-view, determinism, provenance]

requires:
  - phase: 06-agent-posterior-view-hardening
    provides: Bounded local query metadata and descriptive uncertainty summaries from Plan 06-01
provides:
  - Exact repeated-call determinism coverage for local, summary, uncertainty, and provenance posterior query families
  - Immutable aggregate-only provenance assertions for returned source counts
affects: [phase-06-agent-posterior-view-hardening, phase-07-representation-memories-and-tools]

tech-stack:
  added: []
  patterns:
    - Exact equality assertions over frozen posterior dataclasses
    - Aggregate-only provenance boundary tests using MappingProxyType immutability
    - Phase 6 agent determinism coverage kept under tests/agents

key-files:
  created:
    - .planning/phases/06-agent-posterior-view-hardening/06-02-SUMMARY.md
  modified:
    - tests/agents/test_splat_posterior.py

key-decisions:
  - "Kept Plan 06-02 as test-only hardening over the Plan 06-01 posterior APIs."
  - "Used an allowably explicit forbidden-key assertion to keep Phase 6 provenance aggregate-only without adding Phase 7 evidence or memory contracts."

patterns-established:
  - "Repeated posterior view calls are asserted by exact dataclass equality rather than approximate numeric checks."
  - "Provenance determinism tests verify immutable aggregate source-count mappings and no detailed evidence/provenance fields."

requirements-completed: [AGNT-04]

duration: 1 min
completed: 2026-05-21
---

# Phase 06 Plan 02: Agent Posterior Determinism Coverage Summary

**Exact repeated-call determinism tests for bounded local, scene summary, uncertainty, and aggregate provenance posterior views**

## Performance

- **Duration:** 1 min
- **Started:** 2026-05-21T01:55:52Z
- **Completed:** 2026-05-21T01:57:40Z
- **Tasks:** 2
- **Files modified:** 1

## Accomplishments

- Added a focused posterior determinism test that constructs one fixed `SplatMap` and asserts repeated `query_local()`, `summary()`, `uncertainty()`, and `provenance()` calls return exactly equal values.
- Verified bounded local query determinism with `max_results=2`, all three fixture splats matching, tuple-order returned IDs `(0, 1)`, `total_matches == 3`, and `truncated is True`.
- Verified provenance summaries remain immutable aggregate source counts and explicitly do not expose Phase 7-style evidence, source-specific uncertainty, confidence, status, timestamp, staleness, memory ID, or claim records.
- Ran both Phase 6 quick validation and the full project suite after the added coverage.

## Task Commits

Each task was committed atomically:

1. **Task 06-02-01: Add exact repeated-query determinism tests** - `6ad8aaa` (test)
2. **Task 06-02-02: Run Phase 6 quick and full validation after determinism coverage** - `d5d50cc` (test, empty validation-record commit)

**Plan metadata:** pending final metadata commit

## Files Created/Modified

- `tests/agents/test_splat_posterior.py` - Adds exact repeated-call determinism assertions for every Phase 6 posterior view query family and immutable aggregate-only provenance checks.
- `.planning/phases/06-agent-posterior-view-hardening/06-02-SUMMARY.md` - Records plan execution outcome.

## Decisions Made

- Kept this plan test-only because Plan 06-01 already provided the required production APIs and all targeted behavior was present.
- Used a validation-record empty commit for Task 06-02-02 because the task required running quick and full validation after coverage, and no source or test changes were needed.
- Kept determinism coverage in `tests/agents/test_splat_posterior.py`, with no evaluation-harness, backend, provider, tensor, ROS, Habitat, or Phase 7 representation-memory imports.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Verification

- `uv run pytest tests/agents/test_splat_posterior.py -q` passed: 7 tests.
- Acceptance scan confirmed the test file includes exact repeated-call equality assertions for `query_local()`, `summary()`, `uncertainty()`, and `provenance()`.
- Acceptance scan confirmed no evaluation module imports, provider SDK imports, ROS/Habitat imports, tensor-library imports, or backend implementation imports were added.
- `uv run pytest tests/agents/test_queries.py tests/agents/test_splat_posterior.py tests/test_public_api.py -q` passed: 36 tests.
- `uv run pytest -q` passed: 225 tests.

## Known Stubs

None.

## Threat Flags

None - this plan added tests only and introduced no new network endpoints, auth paths, file access patterns, schemas, runtime dependencies, or trust-boundary-changing production code.

## TDD Gate Compliance

- RED gate warning: no RED failure commit was created because the tested behavior already existed after Plan 06-01 and Plan 06-02 did not require production implementation.
- GREEN-equivalent coverage commit present: `6ad8aaa test(06-02): add posterior determinism coverage`.
- Validation record present: `d5d50cc test(06-02): validate posterior determinism suite`.

## Next Phase Readiness

Plan 06-03 can publish Phase 6 exports and README boundary language with deterministic local, summary, uncertainty, and aggregate provenance behavior now machine-checked.

## Self-Check: PASSED

- Key modified file exists: `tests/agents/test_splat_posterior.py`.
- Summary file exists: `.planning/phases/06-agent-posterior-view-hardening/06-02-SUMMARY.md`.
- Task commit `6ad8aaa` exists in git history.
- Task commit `d5d50cc` exists in git history.
- Targeted, quick, and full validation commands passed.
- `STATE.md` and `ROADMAP.md` were not modified by this worktree executor.

---
*Phase: 06-agent-posterior-view-hardening*
*Completed: 2026-05-21*
