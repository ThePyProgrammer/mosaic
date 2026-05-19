---
phase: 04-fusion-diagnostics-and-semantics-hardening
plan: 02
subsystem: fusion
tags:
  - fusion
  - diagnostics
  - strategy
requirements:
  - FUSE-02
  - FUSE-04
dependency_graph:
  requires:
    - FusionResult typed diagnostic summaries from 04-01
  provides:
    - ProvenancePreservingFusion populated provenance summary
    - ProvenancePreservingFusion preserved_not_optimized uncertainty summary
    - Conservative diagnostic-only fusion conflict candidates
    - Anti-grid preservation behavior tests
  affects:
    - src/mosaic/fusion/strategies.py
    - tests/fusion/test_strategies.py
tech_stack:
  added: []
  patterns:
    - pure-Python deterministic pairwise diagnostics
    - typed summary plus scalar diagnostics mirror
    - splat-preserving anti-occupancy-grid tests
decisions:
  - Kept ProvenancePreservingFusion as a preservation strategy that never drops, merges, or rejects splats because of diagnostic conflicts.
  - Used preserved_not_optimized as the stable strategy uncertainty label in typed and flat diagnostics.
  - Kept conflict pair details in typed summaries while flat diagnostics expose only scalar totals and model labels.
key_files:
  created: []
  modified:
    - src/mosaic/fusion/strategies.py
    - tests/fusion/test_strategies.py
metrics:
  started: 2026-05-19T07:31:52Z
  completed: 2026-05-19T07:34:48Z
  duration_seconds: 176
  tasks_completed: 3
  files_changed: 2
---

# Phase 04 Plan 02: Strategy Diagnostics and Anti-Grid Semantics Summary

`ProvenancePreservingFusion` now preserves source splats while returning first-class provenance, uncertainty, and conservative conflict diagnostics with stable scalar mirrors for artifact consumers.

## What Changed

- Extended strategy behavior tests to assert typed provenance counts, uncertainty summaries, flat scalar diagnostic keys, and splat-native anti-grid behavior together.
- Updated `ProvenancePreservingFusion` to populate `FusionProvenanceSummary`, `FusionUncertaintySummary`, and `FusionConflictSummary` instead of relying on Plan 01 compatibility defaults.
- Replaced the old hyphenated non-optimization label with exact `preserved_not_optimized` in typed and flat strategy diagnostics.
- Added deterministic conservative conflict detection for overlapping splats from different provenance sources with color, opacity, and covariance mismatch reasons.
- Kept conflicts diagnostic-only: overlapping mismatched splats remain preserved in the fused `SplatMap` and `FusionStatus.FUSED` is still returned.

## Task Results

| Task | Name | Commit | Verification |
|------|------|--------|--------------|
| 1 | Specify strategy typed diagnostics and anti-grid behavior | 7d8ff41 | RED gate failed as expected: strategy still returned default typed summaries and old flat diagnostics |
| 2 | Implement provenance, uncertainty, and conflict diagnostics | baef75e | `uv run pytest tests/fusion/test_strategies.py -q` passed |
| 3 | Run focused fusion verification | 3188120 | `uv run pytest tests/fusion -q` passed |

## Verification

- `uv run pytest tests/fusion/test_strategies.py -q` — 5 passed
- `uv run pytest tests/fusion -q` — 30 passed
- Source acceptance checks confirmed `preserved_not_optimized`, conflict threshold constants, populated `FusionResult` typed summary keyword arguments, and no strategy-test expectation that conflicts produce `FusionStatus.REJECTED`.

## Decisions Made

- Kept provenance keys stable by counting missing splat provenance under `unknown`.
- Used covariance diagonal entries `(xx, yy, zz)` from `covariance_upper` for both uncertainty range statistics and conservative radius/covariance mismatch diagnostics.
- Used coarse deterministic thresholds only for diagnostic candidates, not for a rejection or optimization policy.

## Deviations from Plan

None - plan executed exactly as written.

## Known Stubs

None found in files created or modified by this plan.

## Threat Flags

None. The modified surface is the planned caller-provided splat-map to fusion-strategy diagnostic boundary from the plan threat model; no new network endpoints, auth paths, file access patterns, or schema trust boundaries were introduced.

## Auth Gates

None.

## Deferred Issues

None.

## Self-Check: PASSED

- Found `src/mosaic/fusion/strategies.py`
- Found `tests/fusion/test_strategies.py`
- Found `.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-02-SUMMARY.md`
- Found commits `7d8ff41`, `baef75e`, and `3188120`
