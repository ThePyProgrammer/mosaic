---
phase: 07-representation-memories-and-tools
plan: 02
subsystem: agents
tags: [python, dataclasses, belief-provenance, claims, pytest]
requires:
  - phase: 07-representation-memories-and-tools
    provides: Base representation memory contracts and typed IDs from plan 07-01
provides:
  - Belief/provenance claims with confidence, status, timestamps, opaque evidence, and visible conflict links
  - Deterministic stale-claim transition helper driven by supplied Timestamp values
  - Unit coverage for claim validation, conflict visibility, evidence opacity, and immutable stale transitions
affects: [agents, representation-memory, evaluation-scenarios]
tech-stack:
  added: []
  patterns: [frozen-slotted dataclasses, StrEnum statuses, immutable tuple snapshots, timestamp-driven transitions]
key-files:
  created:
    - tests/agents/test_representation_claims.py
  modified:
    - src/mosaic/agents/memory.py
key-decisions:
  - "Preserved existing BeliefProvenanceMemory constructor compatibility by allowing existing ClaimId fixtures while adding full Claim records."
  - "Implemented stale transitions as an explicit pure helper over supplied Timestamp values; no wall-clock time is read."
patterns-established:
  - "Claim records keep contradictory reports visible through ClaimStatus.CONFLICTED and reciprocal conflicts_with links."
  - "mark_stale_claims returns a new BeliefProvenanceMemory and leaves the original snapshot unchanged."
requirements-completed: [REPR-02]
duration: 11min
completed: 2026-05-21T03:31:46Z
---

# Phase 07 Plan 02: Belief/Provenance Claim Semantics Summary

**Typed belief claims with visible conflicts, opaque evidence references, confidence validation, and deterministic timestamp-driven staleness**

## Performance

- **Duration:** 11 min
- **Started:** 2026-05-21T03:20:14Z
- **Completed:** 2026-05-21T03:31:46Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments

- Added failing TDD coverage for claim confidence bounds, opaque evidence references, conflicting robot reports, no hidden winner selection, and explicit stale transitions.
- Implemented `ClaimStatus`, `Claim`, `BeliefProvenanceMemory.with_claim()`, and `mark_stale_claims()` in the provider-free memory contract module.
- Verified claim behavior alongside the existing representation-memory suite, then ran the broader agent/evaluation test slice.

## Task Commits

Each task was committed atomically:

1. **Task 1: Add failing tests for claims, conflicts, and stale transitions** - `07b720a` (test)
2. **Task 2: Implement claims, visible conflicts, and stale transition helper** - `20d7271` (feat)

**Plan metadata:** committed separately after this summary.

_Note: TDD tasks used separate test and implementation commits._

## Files Created/Modified

- `tests/agents/test_representation_claims.py` - Claim semantics tests for confidence validation, evidence opacity, visible conflicts, preserved claim ordering, and deterministic stale transitions.
- `src/mosaic/agents/memory.py` - Claim status enum, claim value object, immutable claim append helper, and timestamp-driven stale transition helper.

## Verification

- `uv run pytest tests/agents/test_representation_claims.py -q` failed before implementation with missing `Claim`, satisfying the RED gate.
- `uv run pytest tests/agents/test_representation_claims.py tests/agents/test_representation_memory.py -q` passed: 13 tests.
- `uv run pytest tests/agents tests/evaluation -q` passed: 91 tests.

## Decisions Made

- Kept `BeliefProvenanceMemory.claims` backward-compatible with existing `ClaimId` fixtures while enabling full `Claim` records for Plan 07-02 semantics.
- Used an explicit pure helper for staleness rather than implicit wall-clock checks, preserving deterministic replay and evaluation behavior.

## Deviations from Plan

None - plan executed as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Known Stubs

None. The only stub-scan hit was `valid_until=None` in a test case intentionally covering non-expiring claims.

## Next Phase Readiness

Plan 07-03 can build bounded belief/provenance and tool-query behavior on top of visible claim statuses, conflict links, and deterministic stale transitions.

## Self-Check: PASSED

- Found created file: `tests/agents/test_representation_claims.py`
- Found modified file: `src/mosaic/agents/memory.py`
- Found task commit: `07b720a`
- Found task commit: `20d7271`

---
*Phase: 07-representation-memories-and-tools*
*Completed: 2026-05-21T03:31:46Z*
