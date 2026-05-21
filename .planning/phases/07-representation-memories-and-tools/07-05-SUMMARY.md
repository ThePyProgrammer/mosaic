---
phase: 07-representation-memories-and-tools
plan: 05
subsystem: evaluation-scenarios
tags:
  - representation-memory
  - evaluation
  - scenarios
  - ablation
requires:
  - 07-03
provides:
  - REPR-08 evaluation-facing scenario coverage
affects:
  - tests/evaluation/test_representation_scenarios.py
tech_stack:
  added: []
  patterns:
    - deterministic pytest scenarios
    - bounded representation-memory query assertions
key_files:
  created:
    - tests/evaluation/test_representation_scenarios.py
  modified: []
decisions:
  - Kept Phase 7 scenario fixtures private to evaluation tests and imported memory contracts directly from mosaic.agents.memory to avoid concurrent public barrel edits.
metrics:
  duration_seconds: 219
  completed_at: 2026-05-21T03:47:49Z
  tasks_completed: 2
  files_changed: 1
---

# Phase 07 Plan 05: Representation Scenario Coverage Summary

Evaluation-facing tests now cover blocked-path, search-frontier, task-allocation, and ARNA-style capability-ablation behavior using deterministic in-memory representation fixtures.

## What Changed

- Added `tests/evaluation/test_representation_scenarios.py` with private fixtures for blocked-path, search-frontier, and task-allocation anchors.
- Asserted conflicted blocked-path claims remain visible with reciprocal conflict IDs, evidence, confidence, status, and bounded query metadata.
- Asserted stale claim transitions use supplied timestamps and preserve inspectable provenance.
- Asserted frontier/traversability results include exact bounded rows, total match counts, truncation metadata, traversability score, status, and linked claim IDs.
- Asserted task-allocation commitments expose two conflicted robot reservations for `frontier:north` with visible commitment conflict IDs.
- Added five capability-ablation tests for navigation/frontier, perception/hazard, belief/conflict, memory/context, and coordination/commitment query families.

## Task Commits

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Add blocked-path and search-frontier scenario tests | e833103 | `tests/evaluation/test_representation_scenarios.py` |
| 2 | Add task-allocation and ARNA-style memory ablation scenario tests | 2062166 | `tests/evaluation/test_representation_scenarios.py` |

## Verification

- `uv run pytest tests/evaluation/test_representation_scenarios.py -q` — 11 passed
- `uv run pytest tests/agents tests/evaluation -q` — 115 passed
- Forbidden term scan for providers, Habitat/ROS/runtime dependencies, and numeric ARNA performance claims — no matches

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Added missing confidence in stale blocked-path fixture**
- **Found during:** Task 1 verification
- **Issue:** The new stale-transition fixture omitted the required `confidence` argument for `Claim`, causing the scenario test to fail before exercising stale behavior.
- **Fix:** Added `confidence=0.8` to the expired blocked-path claim fixture.
- **Files modified:** `tests/evaluation/test_representation_scenarios.py`
- **Commit:** e833103

## Known Stubs

None.

## Threat Flags

None.

## Self-Check: PASSED

- Created file exists: `tests/evaluation/test_representation_scenarios.py`
- Summary file exists: `.planning/phases/07-representation-memories-and-tools/07-05-SUMMARY.md`
- Task commits exist: `e833103`, `2062166`
- No shared orchestrator artifacts (`.planning/STATE.md`, `.planning/ROADMAP.md`) were modified.
