---
phase: 04-fusion-diagnostics-and-semantics-hardening
plan: 03
subsystem: fusion
tags:
  - fusion
  - diagnostics
  - documentation
requirements:
  - FUSE-02
  - FUSE-04
dependency_graph:
  requires:
    - FusionResult typed diagnostic summaries from 04-01
    - ProvenancePreservingFusion diagnostics from 04-02
  provides:
    - Public README fusion diagnostics boundary note
    - README contract assertions for preserved_not_optimized terminology
    - README contract assertions for non-optimization and anti-grid semantics
  affects:
    - README.md
    - tests/test_readme_contract.py
tech_stack:
  added: []
  patterns:
    - documentation contract tests
    - exact string assertions for public API semantics
    - dependency-boundary guard assertions
decisions:
  - Locked Phase 4 fusion documentation through exact README contract assertions rather than loose regex matching.
  - Kept fusion diagnostics documentation concise inside the existing public API map and backend/dependency boundary sections.
  - Preserved the no-new-runtime-dependency boundary while documenting non-optimization and anti-occupancy-grid semantics.
key_files:
  created: []
  modified:
    - README.md
    - tests/test_readme_contract.py
metrics:
  started: 2026-05-19T07:37:42Z
  completed: 2026-05-19T07:39:44Z
  duration_seconds: 122
  tasks_completed: 3
  files_changed: 2
---

# Phase 04 Plan 03: Fusion Documentation Boundary Summary

README now publicly locks Mosaic's Phase 4 fusion boundary: typed summaries are named, `preserved_not_optimized` is stable, and the reference strategy preserves splats without Gaussian optimization or occupancy-grid collapse.

## What Changed

- Added README contract coverage for `FusionProvenanceSummary`, `FusionUncertaintySummary`, `FusionConflictSummary`, `preserved_not_optimized`, `does not optimize Gaussians`, and `does not collapse overlapping splats into occupancy-grid cells`.
- Updated the `mosaic.fusion` public API row to name the Phase 4 typed diagnostic summaries alongside `FusionInput`, `FusionResult`, `FusionStatus`, and `ProvenancePreservingFusion`.
- Tightened the backend/dependency boundary note to state that `ProvenancePreservingFusion` preserves and diagnoses splats, reports `preserved_not_optimized`, does not optimize Gaussians, and does not collapse overlapping splats into occupancy-grid cells.
- Preserved the existing README guard that prevents dependency installation instructions for GPU/native/robot/LLM stacks from entering the core setup path.

## Task Results

| Task | Name | Commit | Verification |
|------|------|--------|--------------|
| 1 | Add README contract assertions for fusion boundary language | 57a2dbe | RED gate failed as expected before README update: missing `FusionProvenanceSummary` and related Phase 4 language |
| 2 | Update README fusion boundary note | 2227bf3 | `uv run pytest tests/test_readme_contract.py -q` passed |
| 3 | Run full phase verification | b701519 | `uv run pytest -q` passed |

## Verification

- `uv run pytest tests/test_readme_contract.py -q` — 4 passed
- `uv run pytest -q` — 176 passed

## Decisions Made

- Used exact string assertions for the stable machine-readable label and prose boundary phrases so `preserved-not-optimized` or watered-down anti-grid language cannot drift in unnoticed.
- Updated existing README sections rather than adding a disconnected Phase 4 section, keeping public documentation concise.
- Kept dependency-boundary assertions duplicated in the new Phase 4 README contract test because the plan's threat model specifically tied fusion documentation to avoiding new GPU/native/robot/LLM install guidance.

## Deviations from Plan

None - plan executed exactly as written.

## Known Stubs

None found in files created or modified by this plan. The stub-pattern scan only found negative README contract assertions for forbidden install commands and the forbidden hyphenated model label.

## Threat Flags

None. This plan modified documentation and documentation contract tests only; it introduced no network endpoints, auth paths, file access patterns, or schema trust boundaries.

## Auth Gates

None.

## Deferred Issues

None.

## Self-Check: PASSED

- Found `README.md`
- Found `tests/test_readme_contract.py`
- Found `.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-03-SUMMARY.md`
- Found commits `57a2dbe`, `2227bf3`, and `b701519`
