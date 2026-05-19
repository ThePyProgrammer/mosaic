---
phase: 03-backend-registry-and-contracts
plan: 04
subsystem: backend-registry
tags: [python, pytest, runtime-import-safety, slam-contracts]
requires:
  - phase: 03-backend-registry-and-contracts
    provides: Phase 03 public SLAM registry and backend contract helper exports
provides:
  - pytest-free runtime import regression coverage for mosaic.slam
  - pytest dependency isolation inside skip_unavailable_backend execution
  - preserved public contract helper exports from mosaic.slam
affects: [backend-registry, slam-contracts, runtime-dependency-boundary]
tech-stack:
  added: []
  patterns:
    - dev-only pytest imports stay local to pytest-specific helper execution paths
    - subprocess import guards verify runtime dependency boundaries
key-files:
  created:
    - tests/slam/test_slam_runtime_import.py
  modified:
    - src/mosaic/slam/contracts.py
key-decisions:
  - "Kept pytest out of Mosaic runtime imports instead of adding it as a runtime dependency."
  - "Preserved D-13 helper exports from mosaic.slam while making skip behavior import pytest only when executed."
patterns-established:
  - "Runtime import regression tests should block specific dev-only imports in a subprocess with PYTHONPATH=src."
requirements-completed: [BACK-02, BACK-03]
duration: 10min
completed: 2026-05-19T05:56:39Z
---

# Phase 03 Plan 04: Runtime SLAM Import Gap Closure Summary

**Pytest-free `mosaic.slam` runtime imports with public backend contract helpers preserved for test consumers**

## Performance

- **Duration:** 10 min
- **Started:** 2026-05-19T05:46:00Z
- **Completed:** 2026-05-19T05:56:39Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments

- Added a subprocess regression test proving `import mosaic.slam` succeeds when `pytest` imports are deliberately blocked.
- Preserved public helper names from `mosaic.slam`: `skip_unavailable_backend`, `assert_backend_lifecycle_contract`, `assert_backend_deterministic_replay`, and `assert_backend_state_update_contract`.
- Removed the module-level `pytest` import from `src/mosaic/slam/contracts.py` and localized it inside `skip_unavailable_backend()` immediately before `pytest.skip(reason)`.
- Verified targeted SLAM runtime/helper tests and the full suite.

## Task Commits

Each task was committed atomically:

1. **Task 03-04-01: Add regression test for pytest-free public SLAM import** - `a1fd40e` (test)
2. **Task 03-04-02: Move pytest import inside skip_unavailable_backend** - `ae65dea` (fix)

**Plan metadata:** pending final summary commit

## Files Created/Modified

- `tests/slam/test_slam_runtime_import.py` - Subprocess runtime import regression with guarded pytest import plus helper export callability coverage.
- `src/mosaic/slam/contracts.py` - Localizes pytest import inside `skip_unavailable_backend()` while leaving other contract helpers pytest-free at module import time.

## Decisions Made

- Kept `pytest` as a dev-only dependency and did not add it to runtime `dependencies`.
- Kept helper exports public from `mosaic.slam` to preserve D-13 instead of hiding contract helpers in a private test module.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- The RED test failed as expected before implementation because `mosaic.slam.contracts` imported `pytest` at module import time.
- The initial worktree branch assertion corrected the worktree base to `470f02c287f723293f9a11c422539f96d12fdd20`; no project files were modified by that reset beyond aligning the worktree with the requested base.

## Verification

- `uv run pytest -q tests/slam/test_slam_runtime_import.py` failed before implementation with `ImportError: simulated runtime environment without pytest`, confirming the regression test exposed the gap.
- `uv run pytest -q tests/slam/test_slam_runtime_import.py tests/slam/test_backend_contract_helpers.py` passed: 9 passed.
- `grep -n 'import pytest' src/mosaic/slam/contracts.py` reports only the local import inside `skip_unavailable_backend()`.
- `grep -n 'dependencies = \[\]' pyproject.toml` confirms runtime dependencies remain empty.
- `uv run pytest -q` passed: 151 passed.

## Known Stubs

None found in created or modified files.

## Threat Flags

None - the change reduces runtime dependency exposure and introduces no new endpoints, auth paths, file access patterns, or schema trust boundaries.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Phase 03 runtime dependency-boundary gap is closed. Backend availability checks and registry inspection remain usable through `mosaic.slam` without requiring dev-only pytest at import time, while downstream backend test suites can still use public contract helpers under pytest.

## Self-Check: PASSED

- Found `tests/slam/test_slam_runtime_import.py`.
- Found `src/mosaic/slam/contracts.py`.
- Found task commit `a1fd40e`.
- Found task commit `ae65dea`.

---
*Phase: 03-backend-registry-and-contracts*
*Completed: 2026-05-19T05:56:39Z*
