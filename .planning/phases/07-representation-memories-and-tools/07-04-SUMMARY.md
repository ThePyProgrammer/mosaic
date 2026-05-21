---
phase: 07-representation-memories-and-tools
plan: 04
subsystem: agents-public-api
tags:
  - representation-memory
  - public-api
  - package-barrels
dependency_graph:
  requires:
    - 07-03
  provides:
    - stable Phase 7 representation-memory imports from mosaic.agents
    - selected stable root imports from mosaic
  affects:
    - src/mosaic/agents/__init__.py
    - src/mosaic/__init__.py
    - tests/test_public_api.py
tech_stack:
  added: []
  patterns:
    - explicit package barrel imports
    - provider-free bounded representation-memory exports
key_files:
  created: []
  modified:
    - src/mosaic/agents/__init__.py
    - src/mosaic/__init__.py
    - tests/test_public_api.py
decisions:
  - Root exports intentionally include only stable aggregate/query symbols, not every Phase 7 record type.
  - The public tool surface remains RepresentationMemory with named query methods, not a separate facade or generic dispatcher.
metrics:
  duration: TBD
  completed: 2026-05-21
  tasks: 2
  files_modified: 3
---

# Phase 07 Plan 04: Representation Memory Public API Summary

Published the Phase 7 representation-memory aggregate and bounded query contracts through supported Mosaic package barrels while preserving the selected root API surface.

## Completed Tasks

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 1 | Add public API tests for Phase 7 exports | 46d17d3 | tests/test_public_api.py |
| 2 | Export stable representation memory symbols through package barrels | 9369877 | src/mosaic/agents/__init__.py, src/mosaic/__init__.py |

## What Changed

- Added public API assertions that lock `RepresentationMemory`, all five memory family contracts, core Phase 7 enums, `EvidenceReference`, `MemoryQueryResult`, and `mark_stale_claims` through `mosaic.agents`.
- Added root API assertions for the selected stable surface: `RepresentationMemory`, `QueryFamily`, `ClaimStatus`, `EntityKind`, `EvidenceReference`, `MemoryQueryResult`, and `mark_stale_claims`.
- Updated `mosaic.agents` to explicitly import Phase 7 symbols from `mosaic.agents.memory` with exact `__all__` entries and no wildcard imports.
- Updated root `mosaic` exports for the selected stable representation-memory aggregate/query surface while keeping `__version__ = "0.1.0"` unchanged.

## Verification

- `uv run pytest tests/test_public_api.py -q` failed before barrel updates, as expected for the RED gate.
- `uv run pytest tests/test_public_api.py tests/agents/test_representation_memory.py tests/agents/test_representation_claims.py -q` passed: 36 tests.
- `uv run pytest tests/agents tests/evaluation -q` passed: 104 tests.

## Deviations from Plan

None - plan executed as written.

## Threat Flags

None. The plan only changed public export surfaces and tests; no new network endpoints, auth paths, file access patterns, schema changes, provider integrations, or dependency imports were introduced.

## Known Stubs

None found in modified files.

## Self-Check: PASSED

- FOUND: src/mosaic/agents/__init__.py
- FOUND: src/mosaic/__init__.py
- FOUND: tests/test_public_api.py
- FOUND: 46d17d3
- FOUND: 9369877
- Stub scan reported no stubs in modified files.
