---
phase: 05-evaluation-metric-and-failure-gate-hardening
plan: 04
subsystem: evaluation
tags: [public-api, readme, backend-boundary, readiness-gate]

requires:
  - phase: 05-evaluation-metric-and-failure-gate-hardening
    plan: 03
    provides: failure taxonomy and evaluation readiness helper
provides:
  - root public exports for Phase 5 readiness and failure contracts
  - public API tests for evaluation exports and README backend-block policy
  - README wording that blocks real 3DGS integration until deterministic gates pass
affects: [public-api, evaluation-exports, documentation-boundary, backend-readiness]

tech-stack:
  added: []
  patterns:
    - explicit package-root exports without wildcard imports
    - README policy text machine-checked by public API tests
    - conservative backend boundary language without native dependency instructions

key-files:
  created:
    - .planning/phases/05-evaluation-metric-and-failure-gate-hardening/05-04-SUMMARY.md
  modified:
    - src/mosaic/__init__.py
    - tests/test_public_api.py
    - README.md

key-decisions:
  - "Root package exports include only stable user-facing Phase 5 additions: FailureClass, EvaluationReadinessResult, evaluation_ready_for_real_backend, and write_benchmark_artifacts_jsonl."
  - "README keeps real backend work blocked with an exact machine-checked sentence and avoids native dependency or provider installation guidance."

patterns-established:
  - "Public API smoke tests import Phase 5 readiness symbols from both mosaic and mosaic.evaluation."
  - "README policy assertions enforce the deterministic gate block and reject real-backend placeholder/dependency wording."

requirements-completed: [EVAL-05]

duration: 3min
completed: 2026-05-19
---

# Phase 05 Plan 04: Public API and Backend Boundary Summary

**Phase 5 readiness exports and README policy now make real 3DGS backend integration visibly blocked until deterministic evaluation gates pass.**

## Performance

- **Duration:** 3 min
- **Started:** 2026-05-19T09:38:02Z
- **Completed:** 2026-05-19T09:40:47Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments

- Added public API tests for `FailureClass`, `EvaluationReadinessResult`, `evaluation_ready_for_real_backend`, and `write_benchmark_artifacts_jsonl` through public package surfaces.
- Added README smoke coverage for the exact backend-block sentence: `real 3DGS backend integration remains blocked until deterministic evaluation gates pass`.
- Exported stable Phase 5 readiness and failure contracts from the root `mosaic` package using explicit imports and `__all__` entries.
- Updated README boundary language to describe deterministic evaluation gates and `DeterministicSplatBackend` as the supported contract backend without adding real backend placeholders or native dependency instructions.

## Task Commits

Each task was committed atomically:

1. **Task 05-04-01: Add public API and README policy tests** - `f98d359` (test)
2. **Task 05-04-02: Publish exports and README backend-block language** - `cff1b55` (feat)

**Plan metadata:** committed separately after this summary.

_Note: Task 05-04-01 followed TDD RED behavior: `uv run pytest tests/test_public_api.py -q` failed on missing root `EvaluationReadinessResult` before implementation._

## Files Created/Modified

- `tests/test_public_api.py` - Adds public import checks for Phase 5 readiness contracts and machine-checked README backend-boundary assertions.
- `src/mosaic/__init__.py` - Re-exports stable Phase 5 evaluation readiness and failure contracts explicitly from the package root.
- `README.md` - Documents deterministic evaluation gates, JSON/JSONL artifacts, the contract backend boundary, and the real-backend integration block.
- `.planning/phases/05-evaluation-metric-and-failure-gate-hardening/05-04-SUMMARY.md` - Captures execution results for the orchestrator.

## Verification

- `uv run pytest tests/test_public_api.py -q` — passed, 6 tests.
- `uv run pytest -q` — passed, 202 tests.

## Decisions Made

- Root-exported only stable user-facing readiness additions rather than every Phase 5 metric helper, keeping the root package surface concise while `mosaic.evaluation` remains the full evaluation barrel.
- Kept the exact backend-block wording lowercase at the start of the sentence so the test can assert the plan-required string exactly.
- Retained legacy README contract-test phrases such as `73` and `not required for Phase 1` while adding Phase 5 boundary language, preserving compatibility with existing README tests.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Preserved existing README contract tests while adding Phase 5 boundary language**
- **Found during:** Task 05-04-02 (Publish exports and README backend-block language)
- **Issue:** Full-suite verification showed existing `tests/test_readme_contract.py` still required the legacy `73` baseline mention and `not required for Phase 1` dependency-boundary phrase after README wording was modernized.
- **Fix:** Reintroduced those compatibility phrases in conservative README text without weakening the Phase 5 real-backend block or adding native dependency guidance.
- **Files modified:** `README.md`
- **Verification:** `uv run pytest tests/test_public_api.py -q && uv run pytest -q`
- **Committed in:** `cff1b55`

---

**Total deviations:** 1 auto-fixed (1 Rule 1 bug)
**Impact on plan:** Compatibility wording preserved existing documentation contracts while still satisfying the Phase 5 backend-block requirement.

## Issues Encountered

- The RED phase failed at collection because root exports for `EvaluationReadinessResult` were missing, satisfying the expected failing-test gate.
- Full-suite verification exposed stale README contract expectations; fixed as a compatibility bug in the implementation commit.

## Known Stubs

None detected in files created or modified by this plan.

## Threat Flags

| Flag | File | Description |
|------|------|-------------|
| threat_flag: public-api-boundary | `src/mosaic/__init__.py` | Root exports now communicate backend-readiness policy to downstream users; mitigated with explicit imports, `__all__`, and public API tests. |
| threat_flag: backend-policy-documentation | `README.md` | README policy influences future real backend work; mitigated with exact machine-checked blocking wording and negative dependency/placeholder assertions. |

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Real backend integration remains blocked unless deterministic lifecycle, trajectory, map-fusion, and agent-query regression gates pass.
- Future backend plans can reference `mosaic.evaluation_ready_for_real_backend` or `mosaic.evaluation.evaluation_ready_for_real_backend` as the explicit unlock signal.

## Self-Check: PASSED

- Confirmed summary path exists before metadata commit.
- Confirmed task commits `f98d359` and `cff1b55` exist in git history.
- Confirmed modified code/test/documentation files exist and the full suite passes.

---
*Phase: 05-evaluation-metric-and-failure-gate-hardening*
*Completed: 2026-05-19*
