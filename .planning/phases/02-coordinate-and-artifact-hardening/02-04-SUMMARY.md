---
phase: 02-coordinate-and-artifact-hardening
plan: 04
subsystem: artifacts
tags:
  - artifact-schema
  - slam
  - evaluation
  - benchmark-json
dependency_graph:
  requires:
    - 02-03
    - src/mosaic/artifacts/schema.py
    - src/mosaic/artifacts/core.py
    - src/mosaic/artifacts/splats.py
  provides:
    - SplatSlamUpdate v1 artifact envelope helpers
    - MetricResult and RegressionResult v1 artifact envelope helpers
    - Explicit BenchmarkArtifact v1 wrapper distinct from BenchmarkArtifact.as_dict()
  affects:
    - src/mosaic/artifacts/__init__.py
    - src/mosaic/artifacts/slam.py
    - src/mosaic/artifacts/evaluation.py
    - tests/artifacts/test_slam_and_evaluation_artifacts.py
tech_stack:
  added: []
  patterns:
    - pure-Python JSON-ready artifact dictionaries
    - explicit artifact barrel exports
    - schema/schema_version validation before reconstruction
key_files:
  created:
    - src/mosaic/artifacts/slam.py
    - src/mosaic/artifacts/evaluation.py
    - tests/artifacts/test_slam_and_evaluation_artifacts.py
  modified:
    - src/mosaic/artifacts/__init__.py
decisions:
  - BenchmarkArtifact.as_dict remains the narrow benchmark-run JSON shape; benchmark_artifact_to_artifact is the explicit v1 envelope boundary.
metrics:
  duration_seconds: 201
  completed_at: 2026-05-18T08:56:25Z
  tasks_completed: 2
  files_created: 3
  files_modified: 1
requirements:
  - ART-01
  - ART-02
commits:
  - 8afe556
  - da4c31e
---

# Phase 02 Plan 04: Backend and Evaluation Artifact Coverage Summary

## One-Liner

Backend updates and evaluation results now round-trip through explicit v1 artifact envelopes while benchmark-run JSON remains a separate deterministic output shape.

## Completed Tasks

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 02-04-01 | Add SplatSlamUpdate artifact round trips | 8afe556 | `src/mosaic/artifacts/slam.py`, `src/mosaic/artifacts/__init__.py`, `tests/artifacts/test_slam_and_evaluation_artifacts.py` |
| 02-04-02 | Add evaluation artifacts and benchmark-schema distinction tests | da4c31e | `src/mosaic/artifacts/evaluation.py`, `src/mosaic/artifacts/__init__.py`, `tests/artifacts/test_slam_and_evaluation_artifacts.py` |

## What Changed

- Added `splat_slam_update_to_artifact()` and `splat_slam_update_from_artifact()` using schema `mosaic.splat_slam_update`.
- Preserved `Timestamp`, `TrackingState`, optional `estimated_pose`, nested `SplatMap`, and diagnostics values across backend update round trips.
- Added `MetricResult`, `RegressionResult`, and `BenchmarkArtifact` artifact helpers using schemas `mosaic.metric_result`, `mosaic.regression_result`, and `mosaic.benchmark_artifact`.
- Exported all new helpers from `mosaic.artifacts` with explicit barrel exports.
- Added artifact tests covering schema-version rejection, tracking/lost update behavior, observed `None` preservation, benchmark wrapper behavior, and deterministic benchmark file writing.

## Verification

- `uv run pytest tests/artifacts/test_slam_and_evaluation_artifacts.py -q` — passed during Task 02-04-01.
- `uv run pytest tests/evaluation tests/artifacts/test_slam_and_evaluation_artifacts.py -q` — passed, 23 tests.
- `uv run pytest tests/core tests/splats tests/slam tests/evaluation tests/artifacts -q` — passed, 80 tests.
- `uv run pytest -q` — passed, 125 tests.

## Deviations from Plan

None - plan executed as written.

## Auth Gates

None.

## Known Stubs

None found in created or modified artifact files.

## Threat Flags

| Flag | File | Description |
|------|------|-------------|
| threat_flag: external-dict-deserialization | `src/mosaic/artifacts/slam.py` | Adds external artifact dictionary reconstruction into `SplatSlamUpdate`; mitigated with `require_artifact()` schema and version checks before domain construction. |
| threat_flag: external-dict-deserialization | `src/mosaic/artifacts/evaluation.py` | Adds external artifact dictionary reconstruction into evaluation result objects; mitigated with `require_artifact()` schema and version checks before domain construction. |

## Self-Check: PASSED

Verified created files exist and task commits `8afe556` and `da4c31e` are present in git history.
