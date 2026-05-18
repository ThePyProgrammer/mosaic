---
phase: 02-coordinate-and-artifact-hardening
plan: 02
subsystem: splats
tags: [python, pytest, covariance, gaussian-splats, semantics]

requires:
  - phase: 01
    provides: Merged GaussianSplat and SplatMap foundation contracts
provides:
  - GaussianSplat covariance_upper layout documented as upper-triangular order
  - SEM-03 covariance reconstruction and positive-definite edge-case tests
affects: [fusion, evaluation, agents, artifacts, covariance-semantics]

tech-stack:
  added: []
  patterns:
    - Frozen dataclass public docstring for domain tuple-order contracts
    - Pytest covariance reconstruction and ValueError edge-case coverage

key-files:
  created: []
  modified:
    - src/mosaic/splats/primitives.py
    - tests/splats/test_splat_map.py

key-decisions:
  - "Preserved GaussianSplat.covariance_upper as the public field while documenting upper-triangular tuple order."
  - "Used focused pytest construction tests to lock positive-definite covariance boundaries without adding numeric dependencies."

patterns-established:
  - "Covariance layout contract: reconstruct (xx, xy, xz, yy, yz, zz) into symmetric rows (xx, xy, xz), (xy, yy, yz), and (xz, yz, zz)."
  - "Covariance validity tests cover tuple length, positive diagonal, leading 2x2 minor, 3x3 determinant, and off-diagonal magnitude."

requirements-completed: [SEM-03]

duration: 2min 8sec
completed: 2026-05-18
---

# Phase 02 Plan 02: Gaussian Covariance Semantics Summary

**GaussianSplat covariance semantics pinned with upper-triangular layout documentation and positive-definite edge-case tests**

## Performance

- **Duration:** 2 min 8 sec
- **Started:** 2026-05-18T08:37:00Z
- **Completed:** 2026-05-18T08:39:08Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments

- Documented `GaussianSplat.covariance_upper` as the symmetric 3x3 upper-triangular order `(xx, xy, xz, yy, yz, zz)`.
- Added explicit reconstruction coverage proving `xy`, `xz`, and `yz` occupy both symmetric matrix positions.
- Added SEM-03 covariance validation tests for tuple length, non-positive diagonal values, zero leading 2x2 minor, non-positive 3x3 determinant, and oversized off-diagonal values.

## Task Commits

Each task was committed atomically:

1. **Task 02-02-01 RED: Document covariance layout and add explicit reconstruction tests** - `d6ac057` (test)
2. **Task 02-02-01 GREEN: Document covariance layout and add explicit reconstruction tests** - `93756b9` (feat)
3. **Task 02-02-02: Add covariance invalid edge-case tests** - `eb41ee7` (test)

**Plan metadata:** pending final docs commit

_Note: TDD task 02-02-01 has separate test and feature commits._

## Files Created/Modified

- `src/mosaic/splats/primitives.py` - Adds the public `GaussianSplat` docstring for covariance tuple layout and matrix row reconstruction.
- `tests/splats/test_splat_map.py` - Adds covariance layout reconstruction, public docstring assertion, non-diagonal positive-definite acceptance, and invalid edge-case tests.

## Decisions Made

- Preserved the existing `covariance_upper` field and dataclass shape; only the public contract wording and tests changed.
- Kept covariance validation dependency-free by relying on the existing determinant checks and pytest edge cases.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Known Stubs

None found in files modified by this plan.

## Threat Flags

None - this plan hardened an existing value-object validation boundary and introduced no new network endpoints, auth paths, file access patterns, or schema trust boundaries.

## Verification

- `uv run pytest tests/splats/test_splat_map.py -q` passed with 14 tests.

## Self-Check: PASSED

- Found modified source file: `src/mosaic/splats/primitives.py`
- Found modified test file: `tests/splats/test_splat_map.py`
- Found task commits: `d6ac057`, `93756b9`, `eb41ee7`

## Next Phase Readiness

- Fusion, evaluation, artifact, and agent posterior work can now depend on a documented SEM-03 covariance tuple order.
- Invalid covariance matrices now fail loudly in covered edge cases before downstream uncertainty consumers interpret them.

---
*Phase: 02-coordinate-and-artifact-hardening*
*Completed: 2026-05-18*
