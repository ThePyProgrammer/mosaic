---
phase: 04-fusion-diagnostics-and-semantics-hardening
plan: 01
subsystem: fusion
tags:
  - fusion
  - diagnostics
  - protocol
requirements:
  - FUSE-02
dependency_graph:
  requires: []
  provides:
    - FusionProvenanceSummary
    - FusionUncertaintySummary
    - FusionConflictSummary
    - FusionResult typed diagnostic summaries
  affects:
    - src/mosaic/fusion/protocol.py
    - src/mosaic/fusion/__init__.py
    - tests/fusion/test_fusion_protocol.py
tech_stack:
  added: []
  patterns:
    - frozen dataclass contracts
    - MappingProxyType defensive copies
    - scalar flat diagnostics with typed summaries
decisions:
  - Kept fusion summaries scoped to mosaic.fusion rather than root mosaic exports.
  - Kept FusionMetricValue scalar while nested summary details live in typed objects.
key_files:
  created: []
  modified:
    - src/mosaic/fusion/protocol.py
    - src/mosaic/fusion/__init__.py
    - tests/fusion/test_fusion_protocol.py
metrics:
  started: 2026-05-19T07:24:31Z
  completed: 2026-05-19T07:27:49Z
  duration_seconds: 198
  tasks_completed: 3
  files_changed: 3
---

# Phase 04 Plan 01: Typed Fusion Diagnostics Contract Summary

Typed fusion diagnostics now expose immutable provenance, uncertainty, and conflict summaries alongside the existing JSON-ready scalar `FusionResult.diagnostics` mapping.

## What Changed

- Added `FusionProvenanceSummary`, `FusionUncertaintySummary`, and `FusionConflictSummary` as frozen, slots-backed dataclasses in `src/mosaic/fusion/protocol.py`.
- Expanded `FusionResult` with default-compatible `provenance`, `uncertainty`, and `conflicts` fields while preserving scalar flat diagnostics.
- Exported the new fusion-prefixed summary classes from `mosaic.fusion` without adding root-level `mosaic` exports.
- Added protocol tests for validation, defensive mapping copies, immutable mapping proxies, compatibility defaults, selected flat diagnostic keys, and subpackage exports.

## Task Results

| Task | Name | Commit | Verification |
|------|------|--------|--------------|
| 1 | Add protocol tests for typed fusion summaries and compatibility defaults | 0989f22 | RED gate failed as expected before implementation: missing summary exports |
| 2 | Implement frozen fusion summary contracts with default empty summaries | 1b0dc31 | `uv run pytest tests/fusion/test_fusion_protocol.py -q` passed |
| 3 | Export fusion summaries from the fusion package and verify Wave 1 boundary | ba5bb54 | `uv run pytest tests/fusion/test_fusion_protocol.py -q` and `uv run pytest tests/fusion -q` passed |

## Verification

- `uv run pytest tests/fusion/test_fusion_protocol.py -q` — 25 passed
- `uv run pytest tests/fusion -q` — 27 passed

## Decisions Made

- Scoped new summary exports to `mosaic.fusion` only, matching Plan 01 and avoiding a root-level naming collision with agent posterior summaries.
- Used `unspecified` as the compatibility default uncertainty model label so legacy `FusionResult(status, fused_map, diagnostics)` callers still construct valid results before Plan 02 populates real strategy summaries.
- Kept nested provenance/conflict maps out of `FusionResult.diagnostics`; the flat mapping remains scalar-only through `FusionMetricValue = bool | int | float | str`.

## Deviations from Plan

None - plan executed as written.

## Known Stubs

None found in files created or modified by this plan.

## Threat Flags

None. The changed surface is the planned caller-to-fusion public contract and does not introduce new network endpoints, auth paths, file access patterns, or schema trust boundaries.

## Auth Gates

None.

## Deferred Issues

None.

## Self-Check: PASSED

- Found `src/mosaic/fusion/protocol.py`
- Found `src/mosaic/fusion/__init__.py`
- Found `tests/fusion/test_fusion_protocol.py`
- Found `.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-01-SUMMARY.md`
- Found commits `0989f22`, `1b0dc31`, and `ba5bb54`
