---
phase: 02
slug: coordinate-and-artifact-hardening
status: verified
threats_open: 0
asvs_level: 1
created: 2026-05-18
---

# Phase 02 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| User/backend code -> core transforms | Caller-supplied frame IDs and coordinates enter pose and camera operations. | Frame identifiers and 3D coordinates |
| Serialized artifacts -> core values | JSON-like payloads reconstruct timestamps, poses, observations, splats, backend updates, and evaluation results. | External dictionaries and JSON-ready primitives |
| ImageBuffer bytes -> JSON artifact | Raw image bytes cross into JSON-compatible artifact payloads. | Image bytes encoded as base64 strings |
| Splat artifacts -> uncertainty semantics | Covariance payloads reconstruct Gaussian uncertainty consumed by fusion, evaluation, and agents. | Covariance tuple/list values |
| BenchmarkArtifact output -> artifact consumers | Existing benchmark JSON may be mistaken for a general Mosaic v1 artifact envelope. | Benchmark-run JSON and schema-envelope JSON |

---

## Threat Register

| Threat ID | Category | Component | Disposition | Mitigation | Status |
|-----------|----------|-----------|-------------|------------|--------|
| T-02-01 | Tampering | `src/mosaic/core/poses.py` Pose3 semantics | mitigate | `Pose3` documents `T_parent_child` and child-to-parent mapping; tests assert concrete non-zero translation semantics. Evidence: `src/mosaic/core/poses.py:89`, `tests/core/test_frames_and_poses.py:19`. | closed |
| T-02-02 | Tampering | `Pose3.compose` | mitigate | Composition rejects incompatible frames before math and tests valid/invalid composition order. Evidence: `src/mosaic/core/poses.py:122`, `tests/core/test_frames_and_poses.py:57`. | closed |
| T-02-03 | Tampering | `GaussianSplat` covariance and splat artifact loader | mitigate | Covariance order is documented, invalid covariance matrices are rejected, and artifact loaders reconstruct through `GaussianSplat`. Evidence: `src/mosaic/splats/primitives.py:9`, `src/mosaic/splats/primitives.py:29`, `src/mosaic/artifacts/splats.py:24`, `tests/splats/test_splat_map.py:89`, `tests/artifacts/test_splat_artifacts.py:38`. | closed |
| T-02-04 | Tampering | `mosaic.artifacts` loaders | mitigate | All artifact loaders use `require_artifact()` to reject unexpected schemas and schema versions before domain object construction. Evidence: `src/mosaic/artifacts/schema.py:15`, `src/mosaic/artifacts/slam.py:26`, `src/mosaic/artifacts/evaluation.py:15`, `tests/artifacts/test_core_artifacts.py:106`, `tests/artifacts/test_slam_and_evaluation_artifacts.py:86`. | closed |
| T-02-05 | Information Disclosure / Tampering | Timestamp, image-buffer, backend-update, and diagnostics artifact payloads | mitigate | Timestamp artifacts use integer nanoseconds, image data uses explicit base64 encoding, backend updates preserve nested timestamp artifacts, and diagnostics round-trip as JSON-ready primitive values. Evidence: `src/mosaic/core/frames.py:9`, `src/mosaic/artifacts/core.py:22`, `src/mosaic/artifacts/core.py:113`, `src/mosaic/artifacts/slam.py:16`, `tests/artifacts/test_core_artifacts.py:119`, `tests/artifacts/test_slam_and_evaluation_artifacts.py:57`. | closed |
| T-02-06 | Repudiation | `BenchmarkArtifact` vs v1 artifact envelope | mitigate | Tests prove `BenchmarkArtifact.as_dict()` remains narrow benchmark JSON and wrapper helpers are explicit schema envelopes. Evidence: `src/mosaic/artifacts/evaluation.py:45`, `tests/artifacts/test_slam_and_evaluation_artifacts.py:131`, `tests/artifacts/test_slam_and_evaluation_artifacts.py:150`. | closed |
| T-02-SC | Tampering | Package installs | accept | Phase 02 added no package-manager install tasks or runtime dependencies; pure-Python dependency boundary remains unchanged. | closed |

*Status: open · closed*  
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-02-01 | T-02-SC | No package-manager install tasks exist in Phase 02; the phase remains pure Python with no new runtime dependencies. | GSD secure-phase audit | 2026-05-18 |

---

## Security Audit 2026-05-18

| Metric | Count |
|--------|-------|
| Threats found | 7 |
| Closed | 7 |
| Open | 0 |

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-05-18 | 7 | 7 | 0 | GSD secure-phase |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-05-18
