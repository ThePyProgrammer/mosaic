---
phase: 07-representation-memories-and-tools
plan: 01
subsystem: agents
tags: [python, dataclasses, representation-memory, pytest]

requires:
  - phase: 06-agent-posterior-view-hardening
    provides: provider-free bounded agent posterior contracts and Mosaic agent style patterns
provides:
  - foundational typed IDs, evidence references, source metadata, enums, and five first-class representation memory family records
  - deterministic unit coverage for representation memory construction and validation
  - provider-free immutable memory contracts without runtime integrations or new dependencies
affects: [phase-07-representation-memories-and-tools, agents, evaluation-scenarios]

tech-stack:
  added: []
  patterns: [frozen slotted dataclasses, StrEnum public values, MappingProxyType frozen mappings, tuple-normalized memory snapshots]

key-files:
  created:
    - src/mosaic/agents/memory.py
    - tests/agents/test_representation_memory.py
  modified: []

key-decisions:
  - "Kept representation memory as provider-free stdlib dataclasses with no persistence, robot runtime, detector, tensor, or LLM dependencies."
  - "Represented spatial/raster, scene graph, text, belief/provenance, and commitment memories as first-class immutable dataclasses rather than generic dictionaries."

patterns-established:
  - "Memory contract records validate caller-supplied IDs, confidence, traversability, resolution, and time-window inputs before publication."
  - "Sequence and mapping inputs are defensively copied into tuples and MappingProxyType views."

requirements-completed: [REPR-01, REPR-03, REPR-04, REPR-05, REPR-06]

duration: 3min
completed: 2026-05-21
---

# Phase 07 Plan 01: Foundational Representation Memory Contracts Summary

**Provider-free typed representation-memory contracts with five immutable memory-family snapshots and deterministic validation tests**

## Performance

- **Duration:** 3 min
- **Started:** 2026-05-21T03:21:05Z
- **Completed:** 2026-05-21T03:23:48Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments

- Added RED unit coverage for typed IDs, opaque evidence references, frozen source metadata, five first-class memory family snapshots, spatial validation, confidence validation, and commitment time-window validation.
- Implemented `mosaic.agents.memory` with typed ID value objects, lower-case `StrEnum` public kinds, source/evidence records, spatial cells, entities, relations, notes, commitments, five family snapshots, and an aggregate `RepresentationMemory` shell.
- Preserved Phase 7 boundaries: no provider SDKs, no runtime dereference behavior for evidence URIs, no persistence layer, no robot execution, and no new runtime dependencies.

## Task Commits

Each task was committed atomically:

1. **Task 1: Add failing unit coverage for representation base contracts and memory-family records** - `a73ba98` (test)
2. **Task 2: Implement foundational representation memory contracts** - `0e5f9c1` (feat)

**Plan metadata:** committed after this summary.

_Note: TDD tasks used a RED test commit followed by a GREEN implementation commit._

## Files Created/Modified

- `src/mosaic/agents/memory.py` - Foundational Phase 7 provider-free representation-memory contracts and five memory-family dataclasses.
- `tests/agents/test_representation_memory.py` - Unit coverage for typed IDs, opaque evidence references, immutable records, and deterministic validation failures.

## Verification

- `uv run pytest tests/agents/test_representation_memory.py -q` failed before implementation with `ModuleNotFoundError: No module named 'mosaic.agents.memory'`.
- `uv run pytest tests/agents/test_representation_memory.py -q` passed after implementation: 7 passed.
- `uv run pytest tests/agents tests/evaluation -q` passed: 85 passed.
- Source checks confirmed the five family classes exist, metadata mappings use `MappingProxyType(dict(...))`, and no prohibited provider/runtime dependency strings were introduced.

## Decisions Made

- Followed the single-module plan for `src/mosaic/agents/memory.py` so later Phase 7 plans can extend the aggregate memory surface without forcing callers to compose separate stores.
- Kept `EvidenceReference.uri` opaque and deliberately did not add `load`, `dereference`, file, or network behavior.
- Kept all Phase 7 memory-family records immutable and validation-first to satisfy the caller-to-representation trust boundary.

## Deviations from Plan

None - plan executed exactly as written.

## Known Stubs

None.

## Threat Flags

None.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

The foundational records are ready for later Phase 7 plans to add claim semantics, aggregate query methods, public export barrels, synthetic scenario helpers, and evaluation-facing scenario coverage.

## Self-Check: PASSED

- Found `src/mosaic/agents/memory.py`.
- Found `tests/agents/test_representation_memory.py`.
- Found task commit `a73ba98`.
- Found task commit `0e5f9c1`.

---
*Phase: 07-representation-memories-and-tools*
*Completed: 2026-05-21*
