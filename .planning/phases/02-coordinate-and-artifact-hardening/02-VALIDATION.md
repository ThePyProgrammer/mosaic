---
phase: 02
slug: coordinate-and-artifact-hardening
status: draft
nyquist_compliant: true
wave_0_complete: false
created: 2026-05-18
---

# Phase 02 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 9.0.3 via `uv run pytest --version` |
| **Config file** | `pyproject.toml` with `testpaths = ["tests"]` and `pythonpath = ["src"]` |
| **Quick run command** | `uv run pytest tests/core tests/splats tests/artifacts -q` |
| **Full suite command** | `uv run pytest -q` |
| **Estimated runtime** | ~1 second for the current full suite; re-check after artifact tests are added |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest tests/core tests/splats tests/artifacts -q` once `tests/artifacts/` exists; before then run the closest touched subset.
- **After every plan wave:** Run `uv run pytest -q`.
- **Before `/gsd:verify-work`:** Full suite must be green with `uv run pytest -q`.
- **Max feedback latency:** One task; no three consecutive implementation tasks may proceed without an automated pytest command.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 02-01-01 | 01 | 1 | SEM-01 | T-02-01 | Reject ambiguous frame/timestamp semantics by testing exact documented behavior | unit | `uv run pytest tests/core/test_frames_and_poses.py tests/core/test_observations.py -q` | yes | pending |
| 02-01-02 | 01 | 1 | SEM-02 | T-02-02 | Reject incompatible pose composition before math is applied | unit | `uv run pytest tests/core/test_frames_and_poses.py -q` | yes | pending |
| 02-02-01 | 02 | 1 | SEM-03 | T-02-03 | Reject invalid covariance tuple length, diagonal, determinant, and off-diagonal edge cases | unit | `uv run pytest tests/splats/test_splat_map.py -q` | yes | pending |
| 02-03-01 | 03 | 2 | ART-01 | T-02-04 | Reject unknown artifact schema names or schema versions before constructing domain objects | unit | `uv run pytest tests/artifacts -q` | no, create in Wave 0 | pending |
| 02-03-02 | 03 | 2 | ART-02 | T-02-05 | Preserve integer timestamp nanoseconds, enum values, bytes encoding, tuple order, and diagnostics mappings across round trips | round-trip | `uv run pytest tests/artifacts -q` | no, create in Wave 0 | pending |
| 02-04-01 | 04 | 2 | ART-01, ART-02 | T-02-06 | Keep existing `BenchmarkArtifact` JSON distinct from the broader v1 artifact envelope and deterministic under `sort_keys=True` | unit/round-trip | `uv run pytest tests/evaluation tests/artifacts -q` | partial | pending |

---

## Wave 0 Requirements

- [ ] `tests/artifacts/test_core_artifacts.py` — stubs for `Timestamp`, `FrameId`, `Translation3`, `Quaternion`, `Pose3`, `CameraIntrinsics`, `ImageBuffer`, `CameraObservation`, and `MultiViewObservation` artifact round trips.
- [ ] `tests/artifacts/test_splat_artifacts.py` — stubs for `GaussianSplat` and `SplatMap` artifact round trips plus covariance layout assertions.
- [ ] `tests/artifacts/test_slam_and_evaluation_artifacts.py` — stubs for `SplatSlamUpdate`, `MetricResult`, `RegressionResult`, and `BenchmarkArtifact` distinction.
- [ ] `src/mosaic/artifacts/__init__.py` — public export surface for v1 artifact helpers.
- [ ] `src/mosaic/artifacts/schema.py` — shared artifact envelope validation helpers.

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

- [x] All tasks have automated pytest verification or Wave 0 dependencies.
- [x] Sampling continuity: no 3 consecutive tasks without automated verification.
- [x] Wave 0 covers all missing artifact-test references.
- [x] No watch-mode flags.
- [x] Feedback latency target is one task.
- [x] `nyquist_compliant: true` set in frontmatter.

**Approval:** approved 2026-05-18
