---
phase: 08-documentation-and-release-readiness
plan: 01
subsystem: documentation
tags:
  - readme
  - release-readiness
  - documentation-contracts
dependency_graph:
  requires:
    - DOCS-01
    - DOCS-02
    - DOCS-03
  provides:
    - concise Mosaic v1 foundation README orientation
    - README contract tests for split-doc release framing
  affects:
    - README.md
    - tests/test_readme_contract.py
    - tests/test_public_api.py
tech_stack:
  added: []
  patterns:
    - pytest file-content documentation contracts
    - release-versioned README boundary wording
key_files:
  created:
    - .planning/phases/08-documentation-and-release-readiness/08-01-SUMMARY.md
  modified:
    - README.md
    - tests/test_readme_contract.py
    - tests/test_public_api.py
decisions:
  - README.md is the concise Mosaic v1 foundation orientation and split-doc hub.
  - README boundary tests now require named deferred integrations rather than forbidding their mention.
metrics:
  started: 2026-05-21T07:30:00Z
  completed: 2026-05-21T07:38:23Z
  duration_minutes: 8
  tasks_completed: 2
  files_modified: 3
---

# Phase 8 Plan 1: README v1 Foundation Orientation Summary

## One-Liner

README.md now presents Mosaic v1 foundation as a concise release orientation and split-doc hub, with contract tests locking commands, links, dependency boundaries, deferred integrations, and provider-free agent-layer wording.

## Tasks Completed

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Update README contract tests for v1 split-doc release framing | a5c052a | tests/test_readme_contract.py |
| 2 | Rewrite README as concise Mosaic v1 foundation orientation | ae4d1d6 | README.md, tests/test_public_api.py |

## Verification

- `uv run pytest tests/test_readme_contract.py -q` passed: 6 tests.
- `uv run pytest -q` passed: 278 tests.

## Decisions Made

- Kept README.md as the public orientation and link hub, with links to `docs/API.md`, `docs/EXAMPLES.md`, and `CONTRIBUTING.md` as required release-navigation anchors.
- Updated the older public API README assertions to match Phase 8 release policy: README must name deferred boundaries explicitly instead of hiding terms such as ROS, Habitat, CUDA/native stacks, and LLM/LVLM providers.
- Preserved existing fusion smoke coverage while shifting README framing away from phase-era language and toward Mosaic v1 foundation terminology.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Updated stale README assertions in public API tests**
- **Found during:** Task 2 full-suite verification.
- **Issue:** `tests/test_public_api.py` still required older README behavior that forbade boundary terms now explicitly required by Phase 8, and required phase-era posterior wording.
- **Fix:** Updated the assertions to require the v1 deferred-boundary list and provider-free separation between `SplatPosteriorView` and `RepresentationMemory`.
- **Files modified:** `tests/test_public_api.py`
- **Commit:** ae4d1d6

## Known Stubs

None.

## Threat Flags

None. This plan changed documentation and documentation tests only; it introduced no network endpoints, auth paths, file access APIs, schema trust boundaries, or runtime dependency surfaces.

## Auth Gates

None.

## Requirements Coverage

- DOCS-01: README distinguishes implemented foundation APIs from deferred real backend, ROS, Habitat, UI/WebSockets, LLM/LVLM, CUDA/native, and production SLAM scope.
- DOCS-02: README previews the deterministic replay to backend to benchmark artifact to posterior/memory golden path and links to split examples documentation.
- DOCS-03: README keeps `uv sync`, `uv run pytest -q`, and `dependencies = []` visible while linking contributor guidance.

## Self-Check: PASSED

- Found `README.md`.
- Found `tests/test_readme_contract.py`.
- Found `tests/test_public_api.py`.
- Found commit `a5c052a`.
- Found commit `ae4d1d6`.
