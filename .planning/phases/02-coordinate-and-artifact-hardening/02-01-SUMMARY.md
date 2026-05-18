---
phase: 02-coordinate-and-artifact-hardening
plan: 01
subsystem: coordinate-semantics
tags:
  - SEM-01
  - SEM-02
  - coordinates
  - pose-transforms
dependency_graph:
  requires: []
  provides:
    - explicit timestamp nanosecond semantics
    - explicit Pose3 T_parent_child semantics
    - pure-Python pose transform utilities
    - optical-frame projection semantics
  affects:
    - src/mosaic/core/frames.py
    - src/mosaic/core/poses.py
    - src/mosaic/core/cameras.py
    - tests/core/test_frames_and_poses.py
    - tests/core/test_observations.py
tech_stack:
  added: []
  patterns:
    - frozen typed dataclass value objects
    - pure-Python quaternion math
    - pytest behavior regression tests
key_files:
  created: []
  modified:
    - src/mosaic/core/frames.py
    - src/mosaic/core/poses.py
    - src/mosaic/core/cameras.py
    - tests/core/test_frames_and_poses.py
    - tests/core/test_observations.py
decisions:
  - Timestamp artifacts use integer nanoseconds as canonical precision, not float seconds.
  - Pose3(parent_frame=A, child_frame=B) is T_parent_child and maps B-frame points into A-frame coordinates.
  - CameraIntrinsics.project accepts camera optical-frame coordinates with +z forward, +x right, and +y down.
metrics:
  duration: TBD
  completed_date: 2026-05-18
  tasks_completed: 2
  files_modified: 5
---

# Phase 02 Plan 01: Coordinate Semantics Summary

Timestamp, Pose3, and CameraIntrinsics contracts now pin nanosecond precision, T_parent_child pose direction, optical-frame projection axes, and pure-Python pose transform behavior.

## Completed Tasks

| Task | Name | Commit | Files |
|------|------|--------|-------|
| 02-01-01 | Lock timestamp, pose-direction, and optical-frame semantics in tests and docstrings | 95b5a31 | `src/mosaic/core/frames.py`, `src/mosaic/core/poses.py`, `src/mosaic/core/cameras.py`, `tests/core/test_frames_and_poses.py`, `tests/core/test_observations.py` |
| 02-01-02 | Implement pure-Python pose application, inversion, and composition | 5430c0a | `src/mosaic/core/poses.py`, `tests/core/test_frames_and_poses.py` |

## What Changed

- Added public docstrings specifying canonical timestamp artifact precision, FrameId coordinate-frame assumptions, Pose3 T_parent_child direction, and camera optical-frame projection axes.
- Added tests proving Timestamp.from_seconds() rounds fractional nanoseconds, timestamp payloads use integer nanoseconds without seconds fields, Pose3 maps child-frame coordinates into parent-frame coordinates, and camera projection treats +x/+y as increasing pixel u/v.
- Implemented Quaternion.conjugate(), Quaternion.multiply(), Quaternion.rotate_point(), Pose3.apply_to_point(), Pose3.inverse(), and Pose3.compose().
- Added tests for pose application, inversion, valid composition, incompatible-frame rejection, and non-identity z-axis rotation composition order.

## Verification

- `uv run pytest tests/core/test_frames_and_poses.py tests/core/test_observations.py -q` — 22 passed.
- `uv run pytest tests/core/test_frames_and_poses.py -q` — 12 passed during Task 02-01-02.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing critical functionality] Added minimal Pose3.apply_to_point during Task 02-01-01**
- **Found during:** Task 02-01-01 RED/GREEN verification
- **Issue:** The SEM-01 pose-direction test required executable child-to-parent point mapping, but Pose3 had no transform method yet.
- **Fix:** Added Pose3.apply_to_point and a temporary identity Quaternion.rotate_point implementation so the semantic test could pass before the full transform task.
- **Files modified:** `src/mosaic/core/poses.py`
- **Commit:** 95b5a31

## Known Stubs

None.

## Threat Flags

None.

## Self-Check: PASSED

- Created files: none expected.
- Modified files verified by commits: `src/mosaic/core/frames.py`, `src/mosaic/core/poses.py`, `src/mosaic/core/cameras.py`, `tests/core/test_frames_and_poses.py`, `tests/core/test_observations.py`.
- Commits verified: 95b5a31, 5430c0a.
