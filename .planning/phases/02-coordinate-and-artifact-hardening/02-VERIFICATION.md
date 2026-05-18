---
phase: 02-coordinate-and-artifact-hardening
verified: 2026-05-18T09:07:57Z
status: passed
score: 23/23 must-haves verified
overrides_applied: 0
---

# Phase 2: Coordinate and Artifact Hardening Verification Report

**Phase Goal:** Users can rely on explicit coordinate, covariance, timestamp, and artifact semantics across downstream fusion and evaluation work.
**Verified:** 2026-05-18T09:07:57Z
**Status:** passed
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | User can read and test the exact meaning of pose direction, parent/child frames, optical-frame convention, handedness, and timestamp precision. | VERIFIED | `src/mosaic/core/frames.py` documents canonical integer nanoseconds and right-handed body frames; `src/mosaic/core/poses.py` documents `Pose3(parent_frame=A, child_frame=B)` as `T_parent_child`; `src/mosaic/core/cameras.py` documents optical-frame `+z forward`, `+x right`, `+y down`; tests in `tests/core/test_frames_and_poses.py` and `tests/core/test_observations.py` assert timestamp rounding, artifact payload shape, pose direction, and optical-frame projection behavior. |
| 2 | User can compose, invert, and apply core pose/camera transforms with behavior verified by tests. | VERIFIED | `Pose3.apply_to_point`, `Pose3.inverse`, and `Pose3.compose` are implemented in `src/mosaic/core/poses.py`; composition enforces frame compatibility before math; tests cover apply, inverse, valid compose, incompatible compose, and non-identity rotation composition order. `CameraIntrinsics.project` is implemented and rejects non-positive/non-finite depth inputs. |
| 3 | User can inspect Gaussian covariance layout and validity rules, including edge cases covered by tests. | VERIFIED | `src/mosaic/splats/primitives.py` documents `covariance_upper` as `(xx, xy, xz, yy, yz, zz)` and validates tuple length, finite values, positive diagonal, positive leading 2x2 minor, and positive 3x3 determinant; `tests/splats/test_splat_map.py` covers reconstruction, valid non-diagonal covariance, tuple length, diagonal, 2x2 minor, 3x3 determinant, and oversized off-diagonal failures. |
| 4 | User can serialize and round-trip versioned JSON-ready artifacts for core values, observations, splats, maps, backend updates, and evaluation results. | VERIFIED | `mosaic.artifacts` contains v1 envelope helpers plus core, observation, splat/map, backend update, and evaluation artifact serializers. Tests in `tests/artifacts/test_core_artifacts.py`, `test_splat_artifacts.py`, and `test_slam_and_evaluation_artifacts.py` prove JSON readiness and round trips for Timestamp, FrameId, Translation3, Quaternion, Pose3, CameraIntrinsics, ImageBuffer, CameraObservation, MultiViewObservation, GaussianSplat, SplatMap, SplatSlamUpdate, MetricResult, RegressionResult, and BenchmarkArtifact wrapper. |
| 5 | User can distinguish the existing benchmark artifact JSON from the broader v1 artifact schema requirements. | VERIFIED | `BenchmarkArtifact.as_dict()` and `write_benchmark_artifact()` in `src/mosaic/evaluation/runner.py` retain narrow deterministic benchmark JSON without envelope keys; `benchmark_artifact_to_artifact()` in `src/mosaic/artifacts/evaluation.py` explicitly wraps that dict in schema `mosaic.benchmark_artifact`; `tests/artifacts/test_slam_and_evaluation_artifacts.py` asserts both shapes and trailing-newline deterministic writer behavior. |
| 6 | Pose3 direction is explicit: Pose3(parent_frame=A, child_frame=B) represents T_parent_child and maps B-frame coordinates into A-frame coordinates. | VERIFIED | `src/mosaic/core/poses.py` docstring states `T_parent_child`; `test_pose_direction_maps_child_frame_points_into_parent_frame` asserts child origin maps to parent translation. |
| 7 | Users can compose, invert, and apply poses with frame compatibility enforced before math. | VERIFIED | `Pose3.compose` raises `ValueError("Cannot compose poses with incompatible frames")` when `self.child_frame != other.parent_frame`; tests assert incompatible frame rejection and inverse round-trip. |
| 8 | Camera projection semantics are documented as optical-frame coordinates with +z forward, +x right, +y down and non-positive depth rejected. | VERIFIED | `src/mosaic/core/cameras.py` documents axes and rejects `z <= 0.0`; tests assert positive x/y pixel movement and non-positive depth rejection. |
| 9 | Timestamp canonical precision is integer nanoseconds, with seconds only as a convenience conversion. | VERIFIED | `Timestamp.nanoseconds` is validated as non-bool `int`; `from_seconds()` uses `round(seconds * 1_000_000_000)`; tests include 1.25s and fractional-nanosecond rounding to 2 ns. |
| 10 | Users can inspect Gaussian covariance layout as upper-triangular (xx, xy, xz, yy, yz, zz). | VERIFIED | `GaussianSplat` docstring contains exact layout and row reconstruction; tests reconstruct symmetric matrix from the tuple and assert positions. |
| 11 | Invalid covariance matrices are rejected for tuple length, non-positive diagonal values, non-positive leading 2x2 principal minor, and non-positive 3x3 determinant. | VERIFIED | `GaussianSplat.__post_init__` implements all checks; `tests/splats/test_splat_map.py` covers each invalid edge case with `ValueError` assertions. |
| 12 | Covariance edge-case behavior is locked by tests before fusion/evaluation depend on splat uncertainty semantics. | VERIFIED | `tests/splats/test_splat_map.py` includes SEM-03 covariance layout and invalid covariance edge-case coverage; full test suite passed. |
| 13 | Users can serialize and deserialize core values through explicit v1 artifact envelopes. | VERIFIED | `src/mosaic/artifacts/schema.py` provides `SCHEMA_VERSION = 1`, `make_artifact`, `require_artifact`; `src/mosaic/artifacts/core.py` provides helper pairs for core values and observations; tests assert schema/version envelopes and round trips. |
| 14 | Timestamp round trips preserve integer nanoseconds, not float seconds. | VERIFIED | `timestamp_to_artifact()` emits `{"nanoseconds": timestamp.nanoseconds}` with no seconds field; `test_timestamp_artifact_round_trips_nanoseconds_without_seconds` asserts the payload and round trip. |
| 15 | ImageBuffer round trips preserve bytes through an explicit reversible data_encoding field. | VERIFIED | `image_buffer_to_artifact()` stores `data_encoding: "base64"` and base64 ASCII data; `image_buffer_from_artifact()` rejects other encodings; tests assert byte-exact round trip for `b"\x00\x00\x00\xff\xff\xff"`. |
| 16 | Pose3 artifacts preserve T_parent_child frame direction and wxyz quaternion order. | VERIFIED | `pose3_to_artifact()` emits `parent_frame`, `child_frame`, `translation`, and `rotation_wxyz`; tests assert parent/child values and `[w, x, y, z]` ordering. |
| 17 | GaussianSplat and SplatMap artifacts preserve covariance_upper order and map frame metadata. | VERIFIED | `gaussian_splat_to_artifact()` emits `covariance_upper` list in existing tuple order; `splat_map_to_artifact()` nests frame and splats; tests assert tuple order and map frame round trip. |
| 18 | Unknown artifact schema names or schema_version values are rejected before domain object construction. | VERIFIED | `require_artifact()` checks schema and `schema_version` before returning payload; tests cover unknown schema and schema_version 2 for core, splat, backend, and evaluation artifacts. |
| 19 | Users can serialize and deserialize backend update artifacts with tracking state, optional estimated_pose, map_update, diagnostics, and timestamp preserved. | VERIFIED | `src/mosaic/artifacts/slam.py` serializes `SplatSlamUpdate`; tests cover TRACKING with pose and diagnostics, LOST with `estimated_pose=None`, nested timestamp/map update, and JSON readiness. |
| 20 | Users can serialize and deserialize evaluation MetricResult and RegressionResult artifacts. | VERIFIED | `src/mosaic/artifacts/evaluation.py` implements metric and regression helper pairs; tests assert round trip including `RegressionResult.observed is None`. |
| 21 | Users can distinguish existing BenchmarkArtifact.as_dict() evaluation JSON from the broader v1 schema envelope. | VERIFIED | Tests assert `BenchmarkArtifact.as_dict()` lacks `schema`, `schema_version`, and `payload`; wrapper helper returns explicit `mosaic.benchmark_artifact` envelope. |
| 22 | Unknown backend/evaluation artifact schema names or schema_version values are rejected before domain object construction. | VERIFIED | Backend and evaluation artifact loaders call `require_artifact()`; tests mutate schema_version to 2 and assert `ValueError` before reconstruction. |
| 23 | Benchmark artifact JSON remains deterministic with sort_keys=True and a trailing newline from write_benchmark_artifact. | VERIFIED | `write_benchmark_artifact()` writes `json.dumps(..., indent=2, sort_keys=True) + "\n"`; test asserts sorted-key starting text, JSON equality, absence of envelope keys, and trailing newline. |

**Score:** 23/23 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `src/mosaic/core/frames.py` | Timestamp nanosecond semantics and FrameId documentation | VERIFIED | Exists, substantive, imported by core/artifact tests, includes integer nanosecond validation and docstrings. |
| `src/mosaic/core/poses.py` | Pose direction, Quaternion math, apply/inverse/compose | VERIFIED | Exists, substantive, public exports wired through `mosaic.core`; tests cover methods and frame mismatch behavior. |
| `src/mosaic/core/cameras.py` | Optical-frame projection contract | VERIFIED | Exists, substantive, public exports wired through `mosaic.core`; tests cover projection axes and depth rejection. |
| `src/mosaic/splats/primitives.py` | Gaussian covariance layout and validation | VERIFIED | Exists, substantive, public exports wired through `mosaic.splats`; tests cover layout and validation. |
| `src/mosaic/artifacts/schema.py` | Shared v1 artifact envelope validation | VERIFIED | Exists, substantive, exported by `mosaic.artifacts`, and used by all artifact loader modules. |
| `src/mosaic/artifacts/core.py` | Core/observation serializers/deserializers | VERIFIED | Exists, substantive, exported by `mosaic.artifacts`, and covered by core artifact tests. |
| `src/mosaic/artifacts/splats.py` | GaussianSplat/SplatMap serializers/deserializers | VERIFIED | Exists, substantive, exported by `mosaic.artifacts`, and covered by splat artifact tests. |
| `src/mosaic/artifacts/slam.py` | SplatSlamUpdate serializers/deserializers | VERIFIED | Exists, substantive, exported by `mosaic.artifacts`, and covered by backend artifact tests. |
| `src/mosaic/artifacts/evaluation.py` | MetricResult/RegressionResult/BenchmarkArtifact artifact helpers | VERIFIED | Exists, substantive, exported by `mosaic.artifacts`, and covered by evaluation artifact tests. |
| `src/mosaic/artifacts/__init__.py` | Public artifact helper export surface | VERIFIED | Explicit imports and `__all__` include schema, core, splat, backend, and evaluation artifact helpers. |
| `tests/core/test_frames_and_poses.py` | SEM-01/SEM-02 regression tests | VERIFIED | Contains timestamp, pose direction, transform, inverse, compose, and mismatch tests. |
| `tests/core/test_observations.py` | Optical-frame camera tests | VERIFIED | Contains projection, optical axis, non-positive depth, and non-finite input tests. |
| `tests/splats/test_splat_map.py` | SEM-03 covariance tests | VERIFIED | Contains covariance layout, reconstruction, positive-definite, and invalid edge-case tests. |
| `tests/artifacts/test_core_artifacts.py` | Core/observation round-trip tests | VERIFIED | Contains envelope, JSON readiness, timestamp, pose, image, observation, and multiview tests. |
| `tests/artifacts/test_splat_artifacts.py` | Splat/map round-trip tests | VERIFIED | Contains GaussianSplat and SplatMap round-trip and covariance-order tests. |
| `tests/artifacts/test_slam_and_evaluation_artifacts.py` | Backend/evaluation artifact and benchmark distinction tests | VERIFIED | Contains SplatSlamUpdate, MetricResult, RegressionResult, BenchmarkArtifact wrapper, and writer distinction tests. |

### Key Link Verification

| From | To | Via | Status | Details |
|---|---|---|---|---|
| `src/mosaic/core/poses.py` | `tests/core/test_frames_and_poses.py` | `Pose3.apply_to_point`, `inverse`, `compose` behavior assertions | WIRED | Tests instantiate `Pose3`, call transform methods, and assert frame/coordinate behavior. |
| `src/mosaic/core/cameras.py` | `tests/core/test_observations.py` | `CameraIntrinsics.project` optical-frame tests | WIRED | Tests call `project()` and assert axis and depth behavior. |
| `src/mosaic/splats/primitives.py` | `tests/splats/test_splat_map.py` | `GaussianSplat` validation and `covariance_upper` assertions | WIRED | Tests instantiate `GaussianSplat` and assert valid/invalid covariance behavior. |
| `src/mosaic/artifacts/core.py` | `src/mosaic/core/frames.py` | Timestamp nanoseconds artifact payload | WIRED | `timestamp_to_artifact()` uses `timestamp.nanoseconds`; loader reconstructs `Timestamp`. |
| `src/mosaic/artifacts/core.py` | `src/mosaic/core/observations.py` | ImageBuffer base64 `data_encoding` payload | WIRED | `image_buffer_to_artifact()` and `image_buffer_from_artifact()` serialize/deserialize `ImageBuffer`; observation helpers nest them. |
| `src/mosaic/artifacts/splats.py` | `src/mosaic/splats/primitives.py` | `covariance_upper` tuple-order preservation | WIRED | Serializer emits list from tuple; loader reconstructs through `GaussianSplat`. |
| `src/mosaic/artifacts/slam.py` | `src/mosaic/slam/protocol.py` | `SplatSlamUpdate` and `TrackingState` reconstruction | WIRED | Serializer emits `tracking_state.value`; loader reconstructs `TrackingState` and `SplatSlamUpdate`. |
| `src/mosaic/artifacts/evaluation.py` | `src/mosaic/evaluation/metrics.py` | `MetricResult` artifact round trip | WIRED | Serializer calls `MetricResult.as_dict()`; loader reconstructs `MetricResult`. |
| `tests/artifacts/test_slam_and_evaluation_artifacts.py` | `src/mosaic/evaluation/runner.py` | `BenchmarkArtifact.as_dict` remains non-envelope evaluation JSON | WIRED | Test imports `BenchmarkArtifact` and `write_benchmark_artifact`, asserts narrow JSON and wrapper distinction. |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|---|---|---|---|---|
| `src/mosaic/artifacts/core.py` | Core/observation artifact payloads | Domain object fields and nested serializer calls | Yes | FLOWING |
| `src/mosaic/artifacts/splats.py` | Splat/map artifact payloads | `GaussianSplat` and `SplatMap` fields | Yes | FLOWING |
| `src/mosaic/artifacts/slam.py` | Backend update artifact payload | `SplatSlamUpdate` fields and nested timestamp/pose/map serializers | Yes | FLOWING |
| `src/mosaic/artifacts/evaluation.py` | Evaluation artifact payloads | `MetricResult.as_dict()`, `RegressionResult` fields, and `BenchmarkArtifact.as_dict()` | Yes | FLOWING |
| `src/mosaic/evaluation/runner.py` | Benchmark JSON output | `BenchmarkArtifact.as_dict()` | Yes | FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|---|---|---|---|
| Full project test suite passes | `uv run pytest -q` | `130 passed in 0.14s` | PASS |
| Phase semantic/artifact evidence exists | `grep -R -n -E "Pose3|T_parent_child|from_seconds|nanoseconds|\+z forward|\+x right|\+y down|covariance_upper|data_encoding|schema_version|BenchmarkArtifact|write_benchmark_artifact" ...` | Found implementation and test evidence across core, splats, artifacts, evaluation, and tests | PASS |

### Probe Execution

No phase-declared probe scripts were found or required for this Python library phase. Step 7c skipped.

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|---|---|---|---|---|
| SEM-01 | 02-01, 02-03 | Pose direction, parent/child frame meaning, camera optical-frame convention, handedness, and timestamp precision are explicitly documented and tested. | SATISFIED | Core docstrings and tests cover nanoseconds, `T_parent_child`, right-handed frame note, optical-frame axes, and artifact preservation. |
| SEM-02 | 02-01 | Core pose/camera utilities include tested transform composition, inversion, and point transformation semantics needed by downstream fusion and evaluation. | SATISFIED | `Pose3.apply_to_point`, `inverse`, and `compose` exist and are covered by tests including non-identity rotation and incompatible frames. |
| SEM-03 | 02-02, 02-03 | Gaussian covariance layout and validity semantics are documented and covered by edge-case tests. | SATISFIED | `GaussianSplat` docstring and validation plus splat/artifact tests cover layout and invalid edge cases. |
| ART-01 | 02-03, 02-04 | Core values, observations, splats, maps, backend updates, and evaluation results have versioned JSON-ready artifact schemas. | SATISFIED | `src/mosaic/artifacts/*` modules implement schema/version envelopes for all listed domains and tests call `json.dumps(..., sort_keys=True)`. |
| ART-02 | 02-03, 02-04 | Serialization round-trip tests cover timestamps, poses, camera observations, Gaussian splats, splat maps, and backend updates. | SATISFIED | Artifact tests cover required round trips plus evaluation results and benchmark wrapper distinction. |

No orphaned Phase 2 requirements were found in `.planning/REQUIREMENTS.md`: SEM-01, SEM-02, SEM-03, ART-01, and ART-02 are all declared in phase plans and accounted for above.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|---|---:|---|---|---|
| `.planning/phases/02-coordinate-and-artifact-hardening/02-REVIEW.md` | 42 | Artifact decoders rely on direct indexing and `cast()` | WARNING | Code review follow-up: malformed payloads may surface mixed exception types after envelope validation. Does not block stated Phase 2 must-haves because schema/schema_version rejection and valid round trips are implemented and tested. |
| `.planning/phases/02-coordinate-and-artifact-hardening/02-REVIEW.md` | 54 | ImageBuffer artifact decoding uses permissive Base64 decoding | WARNING | Code review follow-up: stricter malformed Base64 rejection is desirable. Does not block stated Phase 2 must-haves because explicit `data_encoding` and byte-exact valid round trip are implemented and tested. |

Source/test anti-pattern scan across modified phase files found no `TBD`, `FIXME`, `XXX`, `TODO`, `HACK`, placeholder text, empty returns, or console-only implementations.

### Human Verification Required

None. The phase deliverables are typed Python library contracts and artifact serializers with deterministic automated tests; no visual, external-service, or real-time behavior requires human UAT.

### Gaps Summary

No blocking gaps found. All roadmap success criteria, PLAN frontmatter must-haves, and Phase 2 requirement IDs are verified against actual source and test evidence. Review warnings remain follow-up hardening items, not blockers for the Phase 2 goal.

---

_Verified: 2026-05-18T09:07:57Z_
_Verifier: Claude (gsd-verifier)_
