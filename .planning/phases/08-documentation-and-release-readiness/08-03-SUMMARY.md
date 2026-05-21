---
phase: 08-documentation-and-release-readiness
plan: 03
subsystem: documentation
tags: [docs, contributing, pytest, release-policy, backend-boundary]

requires:
  - phase: 08-documentation-and-release-readiness
    provides: Split README, API, and examples docs from plans 08-01 and 08-02
provides:
  - Contributor release policy for dependency, optional extras, API stability, tests, and backend seams
  - Doc contract checks for contributor policy, split-doc README links, and heavy integration install guards
affects: [release-readiness, documentation, contributor-policy, backend-registry]

tech-stack:
  added: []
  patterns: [Markdown release policy, pytest documentation contract tests]

key-files:
  created: [CONTRIBUTING.md]
  modified: [tests/test_docs_contract.py]

key-decisions:
  - "Kept optional extras as policy-only documentation and left pyproject dependency metadata unchanged."
  - "Locked real-backend contributor guidance at the registry, adapter, availability, and contract-test seam."

patterns-established:
  - "Contributor release policy must name dependencies = [] and forbid placeholder optional extras until real optional integrations exist."
  - "Public docs are scanned for heavy deferred integration install commands across README, API, examples, and contributor docs."

requirements-completed: [DOCS-03]

duration: 3min
completed: 2026-05-21
---

# Phase 08 Plan 03: Contributor Policy and Release Gate Summary

**Contributor release policy with pytest guards for dependency metadata, optional extras, backend seams, public API stability, and heavy integration install drift.**

## Performance

- **Duration:** 3 min
- **Started:** 2026-05-21T07:43:34Z
- **Completed:** 2026-05-21T07:46:26Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments

- Added `CONTRIBUTING.md` with release-facing policy for `dependencies = []`, optional extras, public API export/docs/test obligations, test workflow commands, and real-backend registry/adapter boundaries.
- Extended `tests/test_docs_contract.py` to prove README links all split release docs after the contributor guide exists.
- Added contributor policy and public documentation install-command guards that prevent placeholder optional extras and unsafe heavy integration install recommendations.

## Task Commits

Each task was committed atomically:

1. **Task 1: Write contributor policy for dependency, API, test, and backend boundaries** - `a527f4c` (docs)
2. **Task 2: Extend split-doc tests for contributor policy and full release gate** - `93ce6ae` (test)

**Plan metadata:** pending final metadata commit

## Files Created/Modified

- `CONTRIBUTING.md` - Contributor release policy for dependency boundary, optional extras, API stability, test workflow, and real-backend seams.
- `tests/test_docs_contract.py` - Split-doc link checks, contributor policy assertions, placeholder-extra guards, and heavy integration install-command scanner.

## Verification

- `uv run python -c 'from pathlib import Path; c = Path("CONTRIBUTING.md").read_text(); p = Path("pyproject.toml").read_text(); assert "dependencies = []" in p; assert "policy-only for the Mosaic v1 foundation release" in c; assert "placeholder extras must not be added until a real optional integration exists" in c; assert all(term in c for term in ("optional extras", "registry", "adapter", "availability", "contract tests", "__all__", "docs/API.md", "tests/test_public_api.py")); assert "Phase 8" not in c'`
- `uv run pytest tests/test_docs_contract.py -q` - 9 passed
- `uv run pytest tests/test_readme_contract.py -q` - 6 passed
- `uv run pytest -q` - 287 passed

## Decisions Made

- Kept optional extras policy in `CONTRIBUTING.md` only; `pyproject.toml` remains unchanged with `dependencies = []` and no placeholder optional dependencies.
- Scoped real-backend guidance to descriptor metadata, registry/adapter seams, availability checks, skip gates, and contract tests; no CUDA/native implementation recipe was added.

## Deviations from Plan

None - plan executed exactly as written.

## Known Stubs

None. The word `placeholder` appears only in the explicit optional-extras policy and tests that forbid placeholder extras; it is not a stub.

## Threat Flags

None. Changes are documentation and documentation-contract tests only; they add no network endpoints, auth paths, file-access API surface, or schema boundary.

## Issues Encountered

- The initial contributor-policy source assertion required the literal lowercase phrase `optional extras`; the first draft only had `Optional extras` as a heading. Added the literal phrase in the policy sentence before committing Task 1.
- The initial placeholder-extra test treated `build-backend = "uv_build"` as a forbidden `backend =` optional extra. Narrowed the assertion to line starts so it rejects fake extras without flagging build metadata.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

DOCS-03 is complete. The release documentation now has contributor-facing policy and machine checks for the dependency boundary, optional extras policy, API stability obligations, test workflow, backend seams, split-doc links, and heavy integration install-command drift.

## Self-Check: PASSED

- `CONTRIBUTING.md` exists.
- `tests/test_docs_contract.py` exists and contains contributor policy tests.
- Task commits found: `a527f4c`, `93ce6ae`.

---
*Phase: 08-documentation-and-release-readiness*
*Completed: 2026-05-21*
