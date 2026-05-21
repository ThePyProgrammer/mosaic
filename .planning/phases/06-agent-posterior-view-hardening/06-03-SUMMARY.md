---
phase: 06-agent-posterior-view-hardening
plan: 03
subsystem: agents
tags: [python, pytest, posterior-view, public-api, readme]

requires:
  - phase: 06-agent-posterior-view-hardening
    provides: Bounded local posterior queries and descriptive uncertainty summary contracts from Plan 06-01
provides:
  - Root and mosaic.agents export coverage for PosteriorUncertaintySummary
  - README boundary language for bounded descriptive posterior views and Phase 7 representation-memory/tool deferral
  - Machine-checked public API and README scope-creep assertions
affects: [phase-06-agent-posterior-view-hardening, phase-07-representation-memories-and-tools, phase-08-documentation-and-release-readiness]

tech-stack:
  added: []
  patterns:
    - Explicit package and root re-exports for stable public contracts
    - README boundary wording backed by pytest string assertions
    - TDD RED/GREEN split for public API documentation contracts

key-files:
  created:
    - .planning/phases/06-agent-posterior-view-hardening/06-03-SUMMARY.md
  modified:
    - README.md
    - src/mosaic/__init__.py
    - tests/agents/test_queries.py
    - tests/test_public_api.py

key-decisions:
  - "Root-exported PosteriorUncertaintySummary because existing stable agent contracts are already root-exported."
  - "Kept Phase 6 README language limited to bounded descriptive posterior views and deferred Phase 7 representation memories/tools."

patterns-established:
  - "Public posterior-view scope is enforced by README substring tests, not subjective documentation review."
  - "Phase 6 uncertainty is documented as descriptive_only and not as calibrated belief, memory, tool, provider, runtime, index, or real-backend behavior."

requirements-completed: [AGNT-02]

duration: 2min
completed: 2026-05-21
---

# Phase 06 Plan 03: Agent Posterior View Hardening Summary

**Public Phase 6 posterior uncertainty exports with machine-checked bounded descriptive posterior-view README boundaries**

## Performance

- **Duration:** 2 min
- **Started:** 2026-05-21T01:56:18Z
- **Completed:** 2026-05-21T01:58:36Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments

- Added RED tests proving the root package lacked `PosteriorUncertaintySummary` and README lacked the bounded descriptive posterior-view boundary language.
- Root-exported `PosteriorUncertaintySummary` consistently with existing stable agent contracts.
- Updated README to advertise `AgentQueryKind.UNCERTAINTY`, `PosteriorUncertaintySummary`, `SplatPosteriorView.uncertainty()`, request-bound `max_results`, and truncation metadata.
- Added machine-checked README guardrails for `bounded descriptive posterior views`, `descriptive_only`, `not representation memories`, and `Phase 7` wording without presenting deferred memory/tool/provider/runtime concepts as implemented Phase 6 behavior.

## Task Commits

Each task was committed atomically:

1. **Task 06-03-01: Add export and README boundary tests** - `89fb0a7` (test)
2. **Task 06-03-02: Publish Phase 6 exports and bounded posterior README language** - `3bdd721` (feat)

**Plan metadata:** pending final metadata commit

_Note: TDD task produced RED then GREEN commits._

## Files Created/Modified

- `tests/agents/test_queries.py` - Extends agent export coverage for `AgentQueryKind.UNCERTAINTY` and `PosteriorUncertaintySummary` in `mosaic.agents.__all__`.
- `tests/test_public_api.py` - Adds root export checks and README boundary assertions for bounded descriptive posterior views and Phase 7 deferral.
- `src/mosaic/__init__.py` - Root-exports `PosteriorUncertaintySummary` explicitly and includes it in `__all__`.
- `README.md` - Documents Phase 6 bounded descriptive posterior views, `descriptive_only` uncertainty, local query bounds, truncation metadata, and Phase 7 representation-memory/tool deferral.
- `.planning/phases/06-agent-posterior-view-hardening/06-03-SUMMARY.md` - Records plan execution outcome.

## Decisions Made

- Root-exported `PosteriorUncertaintySummary` because `LocalRadiusQuery`, `PosteriorSummary`, `ProvenanceSummary`, `SplatPosteriorView`, and `SplatQueryResult` are already stable root-exported agent contracts.
- Used concise README boundary wording rather than adding Phase 7 implementation guidance, preserving D-13 through D-16 scope limits.
- Kept negative tests focused on forbidden concepts being described as implemented Phase 6 features, so deferred roadmap language remains possible without false positives.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Verification

- `uv run pytest tests/agents/test_queries.py tests/test_public_api.py -q` failed during RED with the expected missing root `PosteriorUncertaintySummary` import before implementation.
- `uv run pytest tests/agents/test_queries.py tests/agents/test_splat_posterior.py tests/test_public_api.py -q` passed: 36 tests.
- `uv run pytest -q` passed: 225 tests.
- Acceptance string checks passed for `PosteriorUncertaintySummary`, `bounded descriptive posterior views`, `descriptive_only`, `not representation memories`, and `Phase 7`.

## Known Stubs

None.

## Threat Flags

None - this plan changed package exports, README text, and tests only. It introduced no network endpoints, auth paths, file access patterns, schema changes, runtime dependencies, provider integrations, ROS/Habitat wrappers, spatial indexes, or real backend behavior.

## TDD Gate Compliance

- RED gate present: `89fb0a7 test(06-03): add failing public posterior boundary tests`
- GREEN gate present: `3bdd721 feat(06-03): publish posterior uncertainty public boundary`
- Refactor gate: not needed

## Next Phase Readiness

Phase 7 can introduce representation memories/tools as separate contracts while relying on README and tests to preserve the Phase 6 posterior-view boundary. Phase 8 can reuse the public API map and smoke example as documentation baseline.

## Self-Check: PASSED

- Key modified files exist in the worktree.
- Task commits `89fb0a7` and `3bdd721` exist in git history.
- Quick and full validation commands passed after implementation.

---
*Phase: 06-agent-posterior-view-hardening*
*Completed: 2026-05-21*
