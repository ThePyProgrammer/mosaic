---
phase: 01-merged-foundation-baseline-completion
plan: 01
subsystem: docs-testing
tags: [readme, pytest, public-api, uv, baseline]

requires: []
provides:
  - Phase 1 README baseline documentation for Mosaic's merged main-checkout implementation
  - Automated README contract guard for required headings, commands, module map, dependency boundary, and empty runtime dependencies
  - Verified public import and full-suite baseline above the observed 73-test threshold
affects: [phase-01, phase-02, documentation, testing, public-api]

tech-stack:
  added: []
  patterns:
    - README contract tests using pathlib and pytest assertions
    - Documentation of pure-Python runtime boundary with dependencies = []

key-files:
  created:
    - tests/test_readme_contract.py
  modified:
    - README.md

key-decisions:
  - "Documented Phase 1 as a pure-Python typed contract baseline rather than a production SLAM backend."
  - "Guarded README dependency-boundary claims with pytest instead of adding runtime dependencies or integration setup."

patterns-established:
  - "README examples use local project-relative artifact paths such as Path(\"benchmark.json\")."
  - "README contract assertions block setup instructions for deferred CUDA/native/robot/LLM/browser dependencies."

requirements-completed: [BASE-01, BASE-02, BASE-03, BASE-04]

duration: 3min 9s
completed: 2026-05-18
---

# Phase 01 Plan 01: Merged Foundation Baseline README Summary

**Phase 1 README and pytest contract guard document Mosaic's pure-Python baseline, public API map, local examples, backend boundary, and 76-test verification path.**

## Performance

- **Duration:** 3min 9s
- **Started:** 2026-05-18T07:07:07Z
- **Completed:** 2026-05-18T07:10:16Z
- **Tasks:** 3 completed
- **Files modified:** 2 production/test files plus this summary

## Accomplishments

- Replaced the placeholder README with release-facing Phase 1 documentation covering scope, install/test workflow, public API map, smoke examples, backend/dependency boundary, and known hardening gaps.
- Added `tests/test_readme_contract.py` to enforce required README headings, `uv sync`, `uv run pytest -q`, all eight module names, the pure-Python claim, and `dependencies = []` in both README and `pyproject.toml`.
- Verified the main-checkout baseline with targeted public import/package/README tests and the full suite, which now reports `76 passed`, above the observed 73-test baseline required by the plan.

## Task Commits

Each task was committed atomically:

1. **Task 1: Write the Phase 1 README baseline** - `369bb6f` (docs)
2. **Task 2 RED: Add failing README contract guard** - `6df34b6` (test)
3. **Task 2 GREEN: Satisfy README contract guard** - `52353e3` (docs)
4. **Task 3: Verify main-checkout import and test baseline** - `56c32e7` (test, verification-only empty commit)

**Plan metadata:** committed separately after this summary is written.

_Note: Task 2 followed TDD with a failing RED commit and a GREEN commit that made the guard pass._

## Files Created/Modified

- `README.md` - Documents Mosaic's Phase 1 library scope, install/test commands, public API map, examples, backend and dependency boundary, and hardening gaps.
- `tests/test_readme_contract.py` - Pytest guard that reads `README.md` and `pyproject.toml` from the repository root with `pathlib.Path` and enforces the README contract.

## Verification

- `test -s README.md && grep -F "uv run pytest -q" README.md && grep -F "dependencies" pyproject.toml` - passed.
- README source assertions for required headings, `uv sync`, `uv run pytest -q`, `73`, `DeterministicSplatBackend`, `ProvenancePreservingFusion`, `SplatPosteriorView`, and `dependencies = []` - passed.
- README forbidden setup assertions for `/tmp`, `sudo`, `pip install torch`, `pip install opencv`, and `pip install ros` - passed.
- `uv run pytest tests/test_readme_contract.py -q` - passed.
- `uv run pytest tests/test_public_api.py tests/test_package_import.py tests/test_readme_contract.py -q` - passed with 9 tests.
- `uv run pytest -q` - passed with 76 tests.
- `grep -F "dependencies = []" pyproject.toml` - passed.

## Decisions Made

- Kept scope to `README.md` and `tests/test_readme_contract.py`; no package source changes were needed because public import smoke tests passed.
- Used an empty verification commit for Task 3 because the task required an atomic commit but produced no file changes after validation passed.
- Adjusted the README boundary wording so mentions of CUDA/backend integrations clearly state they are deferred and not required for Phase 1.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed over-broad README boundary guard**
- **Found during:** Task 2 (Add an automated README contract guard)
- **Issue:** The initial dependency-boundary test required every line mentioning a deferred technology to include a marker word. That correctly failed RED, but the strict per-line rule was too broad for bullet-list entries already introduced by a deferred/out-of-scope sentence.
- **Fix:** Kept assertions that the README contains boundary marker sentences and rejects install-command lines for deferred terms, while allowing deferred bullet entries under the explicit boundary section.
- **Files modified:** `tests/test_readme_contract.py`, `README.md`
- **Verification:** `uv run pytest tests/test_readme_contract.py tests/test_public_api.py tests/test_package_import.py -q`
- **Committed in:** `52353e3`

---

**Total deviations:** 1 auto-fixed (Rule 1)
**Impact on plan:** The fix kept the dependency-boundary guard strict where it matters: setup commands and runtime dependency claims. No scope creep.

## Issues Encountered

- The RED phase failed as expected against README boundary wording.
- The first GREEN attempt exposed that the test was too broad for deferred bullet-list wording; it was narrowed to block setup commands while preserving the plan's deferred-boundary intent.

## User Setup Required

None - no external service configuration required.

## Known Stubs

None found in `README.md` or `tests/test_readme_contract.py` that prevent the plan goal from being achieved.

## Threat Flags

None. This plan introduced documentation and local file-read tests only; no new network endpoints, auth paths, trust-boundary schema changes, or privileged file access patterns were added.

## TDD Gate Compliance

- RED commit present: `6df34b6` (`test(01-01): add failing README contract guard`)
- GREEN commit present after RED: `52353e3` (`docs(01-01): satisfy README contract guard`)
- REFACTOR commit: not needed.

## Next Phase Readiness

BASE-01 through BASE-04 are now documented and guarded. Later Phase 1 plans can validate fusion, evaluation, and agent posterior APIs against this README baseline; Phase 2 can start coordinate/artifact hardening without redefining the user-facing setup path.

## Self-Check: PASSED

- Found `README.md`.
- Found `tests/test_readme_contract.py`.
- Found task commits `369bb6f`, `6df34b6`, `52353e3`, and `56c32e7` in git history.
- Verified targeted tests and full suite passed before summary creation.

---
*Phase: 01-merged-foundation-baseline-completion*
*Completed: 2026-05-18*
