---
phase: 07-representation-memories-and-tools
plan: 03
subsystem: agents
tags: [python, representation-memory, agent-tools, provenance, pytest]
requires:
  - phase: 07-representation-memories-and-tools
    provides: Base memory family contracts and claim semantics from plans 07-01 and 07-02.
provides:
  - RepresentationMemory aggregate owning spatial, scene, text, belief, and commitment memories.
  - Immutable synthetic update helpers for cells, entities, relations, claims, notes, and commitments.
  - Bounded named query methods for perception, navigation, coordination, belief/provenance, and context.
affects: [agents, evaluation, phase-07]
tech-stack:
  added: []
  patterns:
    - Frozen dataclass aggregate with immutable with_* updates.
    - Bounded query result rows with total_matches and truncated metadata.
key-files:
  created:
    - .planning/phases/07-representation-memories-and-tools/07-03-SUMMARY.md
  modified:
    - src/mosaic/agents/memory.py
    - tests/agents/test_representation_memory.py
key-decisions:
  - "Kept deterministic tool methods directly on RepresentationMemory rather than introducing a facade or generic dispatcher."
  - "Returned bounded row dataclasses carrying IDs, evidence, statuses, confidences, and truncation metadata instead of exposing raw memory dumps."
patterns-established:
  - "RepresentationMemory.empty(frame=...) creates the caller-facing aggregate for all five memory families."
  - "Each named query validates a positive request bound and reports total_matches plus truncated."
requirements-completed: [REPR-01, REPR-03, REPR-04, REPR-05, REPR-06, REPR-07]
duration: 5min
completed: 2026-05-21
---

# Phase 07 Plan 03: Aggregate Representation Memory Summary

**RepresentationMemory aggregate with immutable synthetic updates and bounded named agent tool queries across five memory families**

## Performance

- **Duration:** 5 min
- **Started:** 2026-05-21T03:35:54Z
- **Completed:** 2026-05-21T03:40:39Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments

- Added failing aggregate-level tests for immutable updates, query bounds, truncation, evidence/status exposure, and all five required named query families.
- Implemented `RepresentationMemory` as the primary caller-facing aggregate with `spatial`, `scene`, `text`, `belief`, and `commitments` families.
- Added bounded result rows and query methods for perception, navigation frontiers, coordination commitments, belief inspection, and context summaries.

## Task Commits

Each task was committed atomically:

1. **Task 1: Add aggregate memory and named query tests** - `b17eafe` (test)
2. **Task 2: Implement aggregate representation memory and named bounded queries** - `e5f2b6c` (feat)

**Plan metadata:** committed separately after summary creation.

## Files Created/Modified

- `src/mosaic/agents/memory.py` - Adds aggregate memory, immutable update helpers, query result dataclasses, and named bounded query methods.
- `tests/agents/test_representation_memory.py` - Adds aggregate TDD coverage for update helpers, bounds, truncation, and query row semantics.
- `.planning/phases/07-representation-memories-and-tools/07-03-SUMMARY.md` - Records plan execution outcome.

## Decisions Made

- Kept the tool surface on `RepresentationMemory`, matching D-11/D-12 and avoiding facade or generic `query(...)` APIs.
- Preserved provider-free, deterministic synthetic ingestion only; no runtime integrations, detectors, persistence, or new dependencies were added.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- `typing_extensions.Self` was unavailable in the project environment. Resolved by using stdlib `typing.Self`, which is available under the Python 3.12+ project baseline.

## Verification

- `uv run pytest tests/agents/test_representation_memory.py -q` failed before Task 2 because `MemoryQueryResult` and aggregate methods were missing, satisfying the RED gate.
- `uv run pytest tests/agents/test_representation_memory.py tests/agents/test_representation_claims.py -q` passed: 26 tests.
- `uv run pytest tests/agents tests/evaluation -q` passed: 104 tests.
- Source assertions confirmed no `RepresentationToolFacade`, `MemoryFacade`, or `def query(` was added.

## Known Stubs

None.

## Threat Flags

None.

## User Setup Required

None - no external service configuration required.

## Self-Check: PASSED

- Found `src/mosaic/agents/memory.py`.
- Found `tests/agents/test_representation_memory.py`.
- Found `.planning/phases/07-representation-memories-and-tools/07-03-SUMMARY.md`.
- Found task commit `b17eafe`.
- Found task commit `e5f2b6c`.

## Next Phase Readiness

Plan 07-04 can export stable Phase 7 public symbols and README guidance against the aggregate API now present in `mosaic.agents.memory`.

---
*Phase: 07-representation-memories-and-tools*
*Completed: 2026-05-21*
