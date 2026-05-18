---
phase: 01-merged-foundation-baseline-completion
plan: 04
subsystem: agents
tags: [python, pytest, typed-contracts, posterior-queries, provider-free]

requires:
  - phase: 01-merged-foundation-baseline-completion
    provides: merged foundation baseline with SplatMap snapshots and agent modules
provides:
  - Expanded validation coverage for typed agent query/result contracts
  - Provider-free boundary tests for SplatPosteriorView local, summary, and provenance APIs
  - Verification that runtime dependencies remain empty for agent posterior queries
affects: [agent-posterior-query-seam, phase-06-agent-posterior-view-hardening]

tech-stack:
  added: []
  patterns:
    - Frozen typed query/result dataclasses with validation
    - MappingProxyType defensive copies for caller-owned provenance mappings
    - Bounded posterior views returning IDs and summaries instead of raw splat maps

key-files:
  created:
    - .planning/phases/01-merged-foundation-baseline-completion/01-04-SUMMARY.md
  modified:
    - tests/agents/test_queries.py
    - tests/agents/test_splat_posterior.py

key-decisions:
  - "Kept agent posterior APIs provider-free and dependency-free; validation was strengthened through tests only because implementation already satisfied the planned contracts."
  - "Did not add uncertainty summary query kinds; those remain deferred to later AGNT-02/AGNT-04 work."

patterns-established:
  - "Agent contract tests assert bounded outputs and explicit public exports."
  - "Provider boundary checks inspect pyproject.toml and posterior source for forbidden runtime integrations."

requirements-completed:
  - AGNT-01
  - AGNT-03

duration: 2m 17s
completed: 2026-05-18
---

# Phase 01 Plan 04: Agent Posterior Query Seam Summary

**Bounded typed agent posterior query contract coverage with provider-free dependency boundary verification.**

## Performance

- **Duration:** 2m 17s
- **Started:** 2026-05-18T07:08:13Z
- **Completed:** 2026-05-18T07:10:30Z
- **Tasks:** 2 completed
- **Files modified:** 3

## Accomplishments

- Expanded `tests/agents/test_queries.py` to cover local-query center validation, positive radius validation, posterior summary bounds, provenance source/count validation, defensive MappingProxyType copy behavior, and explicit `mosaic.agents.__all__` exports.
- Expanded `tests/agents/test_splat_posterior.py` to assert bounded local query IDs plus query kind, fixed-map summary/provenance behavior, empty runtime dependencies, and absence of provider/robot/heavy imports in the posterior source.
- Verified the existing implementation already satisfies the planned AGNT-01 and AGNT-03 contracts without adding runtime dependencies or exposing raw `SplatMap` dumps through query results.

## Task Commits

Each task was committed atomically:

1. **Task 1: Verify typed query and result contracts** - `3d89d48` (test)
2. **Task 2: Verify SplatPosteriorView behavior and provider-free boundary** - `4623c79` (test)

**Plan metadata:** committed after this summary is written.

## Files Created/Modified

- `tests/agents/test_queries.py` - Strengthened contract tests for query/result validation, immutable copied provenance counts, and public agent exports.
- `tests/agents/test_splat_posterior.py` - Strengthened posterior view tests for bounded IDs, query kind, provider-free source checks, and dependency boundary review.
- `.planning/phases/01-merged-foundation-baseline-completion/01-04-SUMMARY.md` - Captures execution results for plan 01-04.

## Decisions Made

- Kept the implementation unchanged because `src/mosaic/agents/queries.py`, `src/mosaic/agents/posteriors.py`, `src/mosaic/agents/__init__.py`, and `pyproject.toml` already satisfied the planned interface and provider-free requirements.
- Added tests instead of source behavior because the plan was TDD-tagged and the missing work was coverage depth, not runtime functionality.
- Preserved the later-phase boundary by not adding uncertainty summary query kinds or any LLM/ROS/Habitat/robot execution dependencies.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Known Stubs

None found. Stub scan over `src/mosaic/agents` and `tests/agents` found no TODO/FIXME/placeholder patterns or hardcoded empty UI-facing placeholders.

## Threat Flags

None. No new network endpoints, auth paths, file access patterns at trust boundaries, or schema changes were introduced.

## Verification

- `uv run pytest tests/agents/test_queries.py -q` -> 9 passed.
- `uv run pytest tests/agents/test_queries.py tests/agents/test_splat_posterior.py -q` -> 13 passed.
- `grep -F "dependencies = []" pyproject.toml` -> found expected empty runtime dependency declaration.
- `uv run pytest tests/agents -q` -> 13 passed.
- Import review confirmed `src/mosaic/agents/posteriors.py` imports only standard library modules, `mosaic.agents.queries`, and `mosaic.splats`.

## Next Phase Readiness

AGNT-01 and AGNT-03 are validated for the current baseline. Later phases can harden AGNT-02 and AGNT-04 by adding uncertainty summaries and determinism coverage without changing the provider-free boundary established here.

## Self-Check: PASSED

- Summary file exists at `.planning/phases/01-merged-foundation-baseline-completion/01-04-SUMMARY.md`.
- Task commit `3d89d48` exists in git history.
- Task commit `4623c79` exists in git history.
- No `STATE.md` or `ROADMAP.md` modifications were made in this worktree.

---
*Phase: 01-merged-foundation-baseline-completion*
*Completed: 2026-05-18*
