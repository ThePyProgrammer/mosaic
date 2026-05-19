---
phase: 03-backend-registry-and-contracts
plan: 02
subsystem: testing
tags: [python, pytest, slam, backend-contracts, registry]

requires:
  - phase: 03-backend-registry-and-contracts
    provides: BackendDescriptor availability checks and default backend registry from plan 03-01
provides:
  - Reusable backend lifecycle contract helpers importable from mosaic.slam
  - Availability-gated pytest skip helper for optional backend descriptors
  - Deterministic replay and state-update helper coverage for backend factories
affects: [backend-registry, optional-backends, evaluation, real-backend-integration]

tech-stack:
  added: []
  patterns:
    - Ordinary importable pytest helper functions instead of pytest plugin hooks
    - Contract-level deterministic replay comparison over synthetic_forward_sequence

key-files:
  created:
    - src/mosaic/slam/contracts.py
    - tests/slam/test_backend_contract_helpers.py
  modified:
    - src/mosaic/slam/__init__.py

key-decisions:
  - "Kept helper assertions at contract level and avoided fake-backend splat geometry coupling."
  - "Used descriptor.check_availability() before pytest.skip() so unavailable optional backends are gated before factory creation."

patterns-established:
  - "Backend contract helpers validate lifecycle, update states, scalar diagnostics, and deterministic replay through plain functions."
  - "Optional backend tests can skip with missing requirements, install hints, and diagnostics in the skip reason."

requirements-completed: [BACK-03, BACK-04]

duration: 2min 13s
completed: 2026-05-19
---

# Phase 03 Plan 02: Backend Contract Helpers Summary

**Reusable pytest backend contract helpers with availability-gated skips and deterministic synthetic replay coverage**

## Performance

- **Duration:** 2min 13s
- **Started:** 2026-05-19T05:31:28Z
- **Completed:** 2026-05-19T05:33:41Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments

- Added `mosaic.slam.contracts` helper functions for lifecycle, state update, deterministic replay, and optional backend availability gating.
- Exported the helper functions from `mosaic.slam` as ordinary importable functions for downstream pytest suites.
- Added tests for helper imports, unavailable descriptor skip reasons, deterministic backend lifecycle/replay, and lost/not-initialized state stubs.

## Task Commits

Each task was committed atomically:

1. **Task 03-02-01: Add failing contract helper tests and state stubs** - `992bbfc` (test)
2. **Task 03-02-02: Implement reusable backend contract helpers** - `5307a46` (feat)

**Plan metadata:** committed after summary creation

_Note: TDD tasks used test then feature commits._

## Files Created/Modified

- `src/mosaic/slam/contracts.py` - Reusable pytest helper/assertion functions for backend lifecycle contracts and availability skips.
- `src/mosaic/slam/__init__.py` - Public SLAM export surface for the contract helper functions.
- `tests/slam/test_backend_contract_helpers.py` - Helper coverage for importability, unavailable descriptors, lifecycle replay, and tracking edge states.

## Verification

- `uv run pytest -q tests/slam/test_backend_contract_helpers.py` failed before implementation with missing helper imports.
- `uv run pytest -q tests/slam/test_backend_contract_helpers.py` passed after implementation: 7 passed.
- `uv run pytest -q tests/slam/test_backend_registry.py tests/slam/test_backend_contract.py tests/slam/test_backend_contract_helpers.py` passed: 20 passed.

## Decisions Made

- Kept generic helpers free of fake-backend center/provenance assertions; deterministic replay compares tracking states, map-update lengths, scalar diagnostics, and final snapshot lengths only.
- Made `skip_unavailable_backend()` include missing requirements, install hints, and availability diagnostics in pytest skip text.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None beyond the expected RED-phase import failure before helper implementation.

## User Setup Required

None - no external service configuration required.

## Known Stubs

None found in files created or modified for this plan.

## Threat Flags

None - helper changes only consume existing descriptor availability and backend process outputs described in the plan threat model.

## Next Phase Readiness

Plan 03-03 can use the registry and contract helper surface to add backend descriptor parametrization or benchmark integration without coupling Mosaic to optional native backend dependencies.

## Self-Check: PASSED

- FOUND: `src/mosaic/slam/contracts.py`
- FOUND: `tests/slam/test_backend_contract_helpers.py`
- FOUND: `.planning/phases/03-backend-registry-and-contracts/03-02-SUMMARY.md`
- FOUND: `992bbfc`
- FOUND: `5307a46`

---
*Phase: 03-backend-registry-and-contracts*
*Completed: 2026-05-19*
