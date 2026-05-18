---
status: issues_found
phase: 02-coordinate-and-artifact-hardening
depth: standard
files_reviewed: 16
findings:
  critical: 0
  warning: 2
  info: 0
  total: 2
resolved_during_review:
  critical: 3
  warning: 1
---

# Phase 02 Code Review

## Scope

Reviewed the source and test files changed by Phase 02 artifact and coordinate hardening plans.

## Resolved During Review

### CR-01: Timestamp accepted non-integer nanoseconds

Fixed in `src/mosaic/core/frames.py` by rejecting non-`int` nanoseconds and `bool` values. Regression coverage added in `tests/core/test_frames_and_poses.py`.

### CR-02: Gaussian splats accepted non-finite numeric values

Fixed in `src/mosaic/splats/primitives.py` by rejecting NaN/inf center, covariance, color, and opacity values before covariance/range checks. Regression coverage added in `tests/splats/test_splat_map.py`.

### CR-03: Camera intrinsics and projection accepted non-finite values

Fixed in `src/mosaic/core/cameras.py` by rejecting NaN/inf intrinsics and projection inputs. Regression coverage added in `tests/core/test_observations.py`.

### WR-03: Translation3 accepted non-finite coordinates

Fixed in `src/mosaic/core/poses.py` by rejecting NaN/inf translations. Regression coverage added in `tests/core/test_frames_and_poses.py`.

## Open Findings

### WR-01 [WARNING]: Artifact decoders rely on direct indexing and `cast()`

**Files:**
- `src/mosaic/artifacts/core.py`
- `src/mosaic/artifacts/splats.py`
- `src/mosaic/artifacts/slam.py`
- `src/mosaic/artifacts/evaluation.py`

Artifact readers validate the envelope but then rely on direct payload indexing and constructor-level validation. Malformed but correctly enveloped artifacts may raise `KeyError`, `TypeError`, enum errors, or constructor errors instead of consistent artifact validation errors.

**Suggested follow-up:** Add small schema field accessors in `src/mosaic/artifacts/schema.py` and convert malformed payloads into `ValueError` with artifact-specific messages.

### WR-02 [WARNING]: ImageBuffer artifact decoding uses permissive Base64 decoding

**File:** `src/mosaic/artifacts/core.py`

`image_buffer_from_artifact()` uses default `base64.b64decode()`, which may ignore non-alphabet characters. Deterministic artifacts should reject malformed Base64 explicitly.

**Suggested follow-up:** Use `base64.b64decode(..., validate=True)` and convert decoding errors to `ValueError`.

## Verification

- `uv run pytest tests/core/test_frames_and_poses.py tests/core/test_observations.py tests/splats/test_splat_map.py -q` — 41 passed
- `uv run pytest -q` — 130 passed
