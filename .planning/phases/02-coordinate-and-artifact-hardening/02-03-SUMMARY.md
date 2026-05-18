---
phase: 02-coordinate-and-artifact-hardening
plan: 03
subsystem: artifacts
tags: [python, pytest, serialization, json, artifacts, coordinates, splats]
requires:
  - phase: 02-coordinate-and-artifact-hardening
    provides: coordinate-frame semantics and covariance layout from plans 02-01 and 02-02
provides:
  - v1 artifact envelope helpers with schema and schema_version validation
  - core value and observation artifact round trips preserving nanoseconds, frame direction, quaternion order, and image bytes
  - GaussianSplat and SplatMap artifact round trips preserving covariance_upper order and map frame metadata
affects: [evaluation-artifacts, backend-update-artifacts, persistence, regression-harness]
tech-stack:
  added: []
  patterns: [explicit JSON-ready artifact envelopes, base64 image payloads, schema-version rejection before domain construction]
key-files:
  created:
    - src/mosaic/artifacts/__init__.py
    - src/mosaic/artifacts/schema.py
    - src/mosaic/artifacts/core.py
    - src/mosaic/artifacts/splats.py
    - tests/artifacts/test_core_artifacts.py
    - tests/artifacts/test_splat_artifacts.py
  modified: []
key-decisions:
  - "Artifact loaders validate schema names and schema_version before constructing Mosaic domain objects."
  - "ImageBuffer artifacts use explicit data_encoding=base64 to preserve bytes through JSON-ready payloads."
  - "Pose3 artifacts encode T_parent_child as parent_frame, child_frame, translation, and rotation_wxyz rather than opaque dataclass serialization."
patterns-established:
  - "Artifact envelope: every v1 helper returns schema, schema_version, and payload top-level keys."
  - "Round-trip serializers construct domain objects through existing dataclass constructors so validation remains centralized."
requirements-completed: [ART-01, ART-02, SEM-01, SEM-03]
duration: 4m05s
completed: 2026-05-18
---

# Phase 02 Plan 03: Artifact Envelope and Round-Trip Serialization Summary

**Versioned v1 artifact envelopes for Mosaic core values, observations, Gaussian splats, and splat maps with explicit schema validation and lossless timestamp/byte/covariance round trips**

## Performance

- **Duration:** 4m05s
- **Started:** 2026-05-18T08:45:13Z
- **Completed:** 2026-05-18T08:49:18Z
- **Tasks:** 3
- **Files modified:** 6

## Accomplishments

- Added `mosaic.artifacts` with shared v1 envelope helpers that reject unexpected schema names and schema versions before any domain object construction.
- Added core and observation serializers for `Timestamp`, `FrameId`, `Translation3`, `Quaternion`, `Pose3`, `CameraIntrinsics`, `ImageBuffer`, `CameraObservation`, and `MultiViewObservation`.
- Added splat serializers for `GaussianSplat` and `SplatMap`, preserving `(xx, xy, xz, yy, yz, zz)` covariance order and map frame metadata.
- Added artifact tests proving JSON readiness with `json.dumps(..., sort_keys=True)` and round-trip equality for all covered value objects.

## Task Commits

Each task was committed atomically:

1. **Task 02-03-01: Create shared artifact envelope helpers and public exports** - `75ebc7d` (test)
2. **Task 02-03-02: Add core and observation artifact round trips** - `17c2123` (feat)
3. **Task 02-03-03: Add splat and map artifact round trips** - `bd9037b` (feat)

## Files Created/Modified

- `src/mosaic/artifacts/__init__.py` - Public barrel exports for artifact envelope, core, observation, splat, and map helpers.
- `src/mosaic/artifacts/schema.py` - Shared `SCHEMA_VERSION = 1`, `make_artifact()`, and `require_artifact()` envelope validation.
- `src/mosaic/artifacts/core.py` - Explicit JSON-ready serializers/deserializers for core and observation value objects.
- `src/mosaic/artifacts/splats.py` - Explicit JSON-ready serializers/deserializers for `GaussianSplat` and `SplatMap`.
- `tests/artifacts/test_core_artifacts.py` - Envelope validation plus core/observation round-trip tests.
- `tests/artifacts/test_splat_artifacts.py` - Splat/map round-trip and covariance-order tests.

## Decisions Made

- Kept artifact schemas as pure-Python helper contracts rather than formal JSON Schema files or new dependencies, matching the plan and Phase 2 pure-Python constraint.
- Used base64 as the only accepted `ImageBuffer.data` encoding and rejected any other `data_encoding` value with `ValueError`.
- Preserved existing domain validation by reconstructing artifacts through Mosaic dataclass constructors instead of bypassing invariants.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- The first TDD red checks failed on missing imports as expected before implementation. No blocking issues remained after the planned helper modules were added.

## Verification

- `uv run pytest tests/artifacts/test_core_artifacts.py -q` — 14 passed
- `uv run pytest tests/artifacts/test_splat_artifacts.py -q` — 4 passed
- `uv run pytest tests/artifacts/test_core_artifacts.py tests/artifacts/test_splat_artifacts.py -q` — 18 passed
- `uv run pytest tests/core tests/splats tests/artifacts -q` — 54 passed

## Known Stubs

None.

## Threat Flags

| Flag | File | Description |
|------|------|-------------|
| threat_flag: untrusted-artifact-input | `src/mosaic/artifacts/core.py` | New deserializers accept external dict-like artifacts; mitigated by shared schema/schema_version validation and domain constructor validation. |
| threat_flag: untrusted-artifact-input | `src/mosaic/artifacts/splats.py` | New splat/map deserializers accept external dict-like artifacts; mitigated by shared schema/schema_version validation and Gaussian covariance validation. |

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

Plan 02-04 can build backend update and evaluation result artifacts on top of the shared envelope helpers and core/splat serializers added here.

## Self-Check: PASSED

- Found created files: `src/mosaic/artifacts/__init__.py`, `src/mosaic/artifacts/schema.py`, `src/mosaic/artifacts/core.py`, `src/mosaic/artifacts/splats.py`, `tests/artifacts/test_core_artifacts.py`, `tests/artifacts/test_splat_artifacts.py`.
- Found task commits: `75ebc7d`, `17c2123`, `bd9037b`.
- Verification commands passed as listed above.

---
*Phase: 02-coordinate-and-artifact-hardening*
*Completed: 2026-05-18*
