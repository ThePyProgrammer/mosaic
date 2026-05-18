---
phase: 02
slug: coordinate-and-artifact-hardening
status: verified
nyquist_compliant: true
wave_0_complete: true
created: 2026-05-18
updated: 2026-05-18
---

# Phase 02 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 9.0.3 via `uv run pytest --version` |
| **Config file** | `pyproject.toml` with `testpaths = ["tests"]` and `pythonpath = ["src"]` |
| **Quick run command** | `uv run pytest tests/core tests/splats tests/slam tests/evaluation tests/artifacts -q` |
| **Full suite command** | `uv run pytest -q` |
| **Observed full-suite runtime** | 130 tests passed in 0.20s on 2026-05-18 |

---

## Sampling Rate

- **After every task commit:** Run the closest touched pytest subset from the Per-Task Verification Map.
- **After every plan wave:** Run `uv run pytest -q`.
- **Before `/gsd:verify-work`:** Full suite must be green with `uv run pytest -q`.
- **Max feedback latency:** One task; no three consecutive implementation tasks may proceed without an automated pytest command.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 02-01-01 | 01 | 1 | SEM-01 | T-02-01, T-02-05 | Reject ambiguous timestamp, pose-direction, handedness, and optical-frame semantics through exact documented behavior | unit/docs | `uv run pytest tests/core/test_frames_and_poses.py tests/core/test_observations.py -q` | yes | covered |
| 02-01-02 | 01 | 1 | SEM-02 | T-02-02 | Reject incompatible pose composition before math is applied and verify transform order/inversion | unit | `uv run pytest tests/core/test_frames_and_poses.py -q` | yes | covered |
| 02-02-01 | 02 | 1 | SEM-03 | T-02-03 | Preserve covariance_upper layout as upper-triangular `(xx, xy, xz, yy, yz, zz)` and reject layout ambiguity | unit | `uv run pytest tests/splats/test_splat_map.py -q` | yes | covered |
| 02-02-02 | 02 | 1 | SEM-03 | T-02-03 | Reject invalid covariance tuple length, diagonal, determinant, and off-diagonal edge cases | unit | `uv run pytest tests/splats/test_splat_map.py -q` | yes | covered |
| 02-03-01 | 03 | 2 | ART-01 | T-02-04 | Reject unknown artifact schema names or schema versions before constructing domain objects | unit | `uv run pytest tests/artifacts/test_core_artifacts.py -q` | yes | covered |
| 02-03-02 | 03 | 2 | ART-01, ART-02, SEM-01 | T-02-05 | Preserve integer timestamp nanoseconds, pose frame direction, bytes encoding, tuple order, and metadata across core/observation round trips | round-trip | `uv run pytest tests/artifacts/test_core_artifacts.py -q` | yes | covered |
| 02-03-03 | 03 | 2 | ART-01, ART-02, SEM-03 | T-02-03, T-02-04 | Preserve Gaussian covariance tuple order and reject unknown splat/map artifact schema versions before construction | round-trip | `uv run pytest tests/artifacts/test_splat_artifacts.py -q` | yes | covered |
| 02-04-01 | 04 | 3 | ART-01, ART-02 | T-02-04, T-02-05 | Preserve SplatSlamUpdate timestamp, tracking state, optional pose, map update, and diagnostics through validated schema envelopes | round-trip | `uv run pytest tests/artifacts/test_slam_and_evaluation_artifacts.py -q` | yes | covered |
| 02-04-02 | 04 | 3 | ART-01, ART-02 | T-02-04, T-02-06 | Keep existing `BenchmarkArtifact` JSON distinct from the broader v1 artifact envelope and deterministic under `sort_keys=True` | unit/round-trip | `uv run pytest tests/evaluation tests/artifacts/test_slam_and_evaluation_artifacts.py -q` | yes | covered |

---

## Automated Coverage Evidence

| Requirement | Evidence |
|-------------|----------|
| SEM-01 | `tests/core/test_frames_and_poses.py` covers timestamp nanoseconds, fractional rounding, canonical artifact payloads, and Pose3 child-to-parent direction; `tests/core/test_observations.py` covers optical-frame projection axes and non-positive depth rejection. |
| SEM-02 | `tests/core/test_frames_and_poses.py` covers pose application, inversion, valid composition, incompatible-frame rejection, and non-identity composition order. |
| SEM-03 | `tests/splats/test_splat_map.py` covers covariance layout reconstruction, docstring contract, non-diagonal positive-definite acceptance, tuple length, diagonal, leading-minor, determinant, and off-diagonal rejection; `tests/artifacts/test_splat_artifacts.py` covers covariance-order preservation through artifacts. |
| ART-01 | `tests/artifacts/test_core_artifacts.py`, `tests/artifacts/test_splat_artifacts.py`, and `tests/artifacts/test_slam_and_evaluation_artifacts.py` cover v1 schema envelopes and unknown schema/schema_version rejection. |
| ART-02 | Artifact round-trip tests cover core values, observations, Gaussian splats, splat maps, SplatSlamUpdate, MetricResult, RegressionResult, and explicit BenchmarkArtifact wrappers. |

---

## Wave 0 Requirements

- [x] `tests/artifacts/test_core_artifacts.py` — covers `Timestamp`, `FrameId`, `Translation3`, `Quaternion`, `Pose3`, `CameraIntrinsics`, `ImageBuffer`, `CameraObservation`, and `MultiViewObservation` artifact round trips.
- [x] `tests/artifacts/test_splat_artifacts.py` — covers `GaussianSplat` and `SplatMap` artifact round trips plus covariance layout assertions.
- [x] `tests/artifacts/test_slam_and_evaluation_artifacts.py` — covers `SplatSlamUpdate`, `MetricResult`, `RegressionResult`, and `BenchmarkArtifact` distinction.
- [x] `src/mosaic/artifacts/__init__.py` — public export surface for v1 artifact helpers.
- [x] `src/mosaic/artifacts/schema.py` — shared artifact envelope validation helpers.

---

## Validation Audit 2026-05-18

| Metric | Count |
|--------|-------|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

### Commands Run

| Command | Result |
|---------|--------|
| `uv run pytest --version` | pytest 9.0.3 |
| `uv run pytest tests/core/test_frames_and_poses.py tests/core/test_observations.py -q` | 26 passed |
| `uv run pytest tests/splats/test_splat_map.py -q` | 15 passed |
| `uv run pytest tests/artifacts/test_core_artifacts.py -q` | 14 passed |
| `uv run pytest tests/artifacts/test_splat_artifacts.py -q` | 4 passed |
| `uv run pytest tests/artifacts/test_slam_and_evaluation_artifacts.py -q` | 10 passed |
| `uv run pytest tests/evaluation tests/artifacts/test_slam_and_evaluation_artifacts.py -q` | 23 passed |
| `uv run pytest tests/core tests/splats tests/slam tests/evaluation tests/artifacts -q` | 85 passed |
| `uv run pytest -q` | 130 passed |

---

## Manual-Only Verifications

All phase behaviors have automated verification through pytest. Human review should only inspect whether the public wording for pose direction and optical-frame convention is understandable.

---

## Threat Model References

| Threat Ref | Threat | Mitigation Required in Plans |
|------------|--------|------------------------------|
| T-02-01 | Users interpret `Pose3(parent_frame, child_frame)` in the inverse direction | Docstrings and tests must state that `Pose3` represents `T_parent_child`, mapping child-frame coordinates into parent-frame coordinates. |
| T-02-02 | Incompatible frame transforms silently compose | `Pose3.compose()` must raise `ValueError` when `self.child_frame != other.parent_frame`. |
| T-02-03 | Invalid covariance matrices pass because only diagonal values are positive | Covariance validation tests must cover upper-triangular order, zero determinant, negative determinant, and too-large off-diagonal values. |
| T-02-04 | Unknown artifact versions are accepted and interpreted as v1 | Artifact loaders must reject unknown `schema` or `schema_version` values with `ValueError`. |
| T-02-05 | JSON round trips lose canonical timestamp or byte payload information | Artifact payloads must store timestamps as integer nanoseconds and image bytes with an explicit reversible encoding. |
| T-02-06 | Existing benchmark JSON is treated as the complete artifact schema | Tests must assert benchmark output remains an evaluation artifact and v1 domain artifacts use explicit schema envelopes. |

---

## Validation Sign-Off

- [x] All tasks have automated pytest verification.
- [x] Sampling continuity: no 3 consecutive tasks without automated verification.
- [x] Wave 0 artifact-test references exist and pass.
- [x] No watch-mode flags.
- [x] Feedback latency target is one task.
- [x] `nyquist_compliant: true` set in frontmatter.

**Approval:** verified 2026-05-18
