# Mosaic

Mosaic is a typed, headless Python library for 3D Gaussian Splatting SLAM contracts over multi-view moving cameras on robotic systems. Phase 1 establishes the merged main-checkout baseline: pure-Python representation types, deterministic reference implementations, public package surfaces, tests, and documentation that let later backend, fusion, evaluation, and agent work harden against a known contract.

Mosaic is intentionally library-first. It provides stable Python APIs for robotic SLAM backends, evaluation tools, platform camera rigs, fusion seams, and bounded agent-facing posterior queries without coupling the core package to one robot, simulator, provider runtime, browser runtime, or accelerator-heavy backend; those integrations are deferred and not required for the core.

## Scope

The supported Phase 1 baseline includes:

- frame, timestamp, pose, camera, image-buffer, and multi-view observation contracts
- immutable `GaussianSplat` primitives and `SplatMap` snapshots
- deterministic in-memory multi-view replay sequences
- `SplatSlamBackend` lifecycle contracts plus `DeterministicSplatBackend` as a reference backend for tests and examples
- robot-neutral platform, embodiment, camera-rig, registry, and representative preset contracts
- initial fusion contracts over immutable splat maps using `FusionInput`, `FusionResult`, and `ProvenancePreservingFusion`
- deterministic synthetic scenarios, benchmark artifacts, and `RegressionGate` checks
- provider-free agent posterior query contracts including `LocalRadiusQuery` and `SplatPosteriorView`

The baseline does not claim production SLAM quality. It nails down typed surfaces and deterministic behavior first, because the real work later is pointless if every backend, evaluator, robot rig, and agent consumer disagrees about the shape of the representation.

## Install and Test

Mosaic targets Python 3.12+ and uses `uv` for the project environment.

```bash
uv sync
uv run pytest -q
```

The current deterministic contract suite is the supported quality gate for this package; the earlier merged baseline recorded 73 passing tests and the suite has expanded since then.

The package keeps the Phase 1 runtime boundary empty in `pyproject.toml`:

```toml
dependencies = []
```

`pytest` is a development dependency used by the test workflow. Do not add runtime dependency installation steps to use the core package.

## Public API Map

Public imports are exposed from explicit package surfaces. The root `mosaic` package re-exports stable primitives, while subpackages group the same contracts by responsibility.

| Package surface | Responsibility | Representative APIs |
|-----------------|----------------|---------------------|
| `mosaic.core` | Frames, timestamps, poses, cameras, image buffers, and observations | `FrameId`, `Timestamp`, `Pose3`, `CameraIntrinsics`, `MultiViewObservation` |
| `mosaic.datasets` | Replayable multi-view sequences | `MultiViewSequence`, `InMemorySequence` |
| `mosaic.splats` | Gaussian primitives and immutable map snapshots | `GaussianSplat`, `SplatMap` |
| `mosaic.slam` | Backend lifecycle protocols and deterministic reference backend | `SplatSlamBackend`, `SplatSlamUpdate`, `TrackingState`, `DeterministicSplatBackend` |
| `mosaic.platforms` | Robot-neutral platform descriptions and camera rigs | `CameraRig`, `PlatformRegistry`, `quadruped_front_rig`, `ugv_surround_rig`, `humanoid_stereo_rig` |
| `mosaic.fusion` | Splat-map fusion contracts and deterministic reference strategy | `FusionInput`, `FusionResult`, `FusionStatus`, `FusionProvenanceSummary`, `FusionUncertaintySummary`, `FusionConflictSummary`, `ProvenancePreservingFusion` |
| `mosaic.evaluation` | Synthetic scenarios, benchmark artifacts, metric families, regression gates, and readiness checks | `synthetic_forward_sequence`, `run_slam_benchmark`, `FailureClass`, `RegressionGate`, `evaluation_ready_for_real_backend`, `write_benchmark_artifacts_jsonl` |
| `mosaic.agents` | Provider-free bounded descriptive posterior views over immutable splat snapshots | `AgentQueryKind.UNCERTAINTY`, `LocalRadiusQuery`, `SplatQueryResult`, `PosteriorSummary`, `PosteriorUncertaintySummary`, `ProvenanceSummary`, `SplatPosteriorView.uncertainty()` |

Root imports are intended for concise examples and user-facing smoke checks:

```python
from mosaic import (
    DeterministicSplatBackend,
    FrameId,
    ProvenancePreservingFusion,
    FailureClass,
    RegressionGate,
    SplatMap,
    SplatPosteriorView,
    check_regression_gates,
    evaluation_ready_for_real_backend,
    run_slam_benchmark,
    synthetic_forward_sequence,
)
```

## Quick Smoke Examples

Run a deterministic synthetic benchmark and write a local artifact:

```python
from pathlib import Path

from mosaic import (
    DeterministicSplatBackend,
    FrameId,
    RegressionGate,
    check_regression_gates,
    run_slam_benchmark,
    synthetic_forward_sequence,
    write_benchmark_artifact,
)

scenario = synthetic_forward_sequence(frame_count=3)
backend = DeterministicSplatBackend(map_frame=FrameId("map"))
artifact = run_slam_benchmark(scenario, backend)
write_benchmark_artifact(artifact, Path("benchmark.json"))
results = check_regression_gates(
    artifact,
    (RegressionGate(metric_name="splat_count", minimum=3.0),),
)

assert artifact.scenario_name == "synthetic-forward-3"
assert all(result.passed for result in results)
```

Fuse two local splat maps while preserving provenance:

```python
from mosaic import FrameId, FusionInput, GaussianSplat, ProvenancePreservingFusion, SplatMap

map_frame = FrameId("map")
left = SplatMap(
    frame=map_frame,
    splats=(
        GaussianSplat(
            center=(0.0, 0.0, 1.0),
            covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1),
            provenance="left-camera",
        ),
    ),
)
right = SplatMap(frame=map_frame)
result = ProvenancePreservingFusion().fuse(FusionInput(maps=(left, right)))

assert result.status.value == "fused"
assert len(result.fused_map) == 1
```

Query an agent-facing posterior view without exposing a full raw map dump:

```python
from mosaic import FrameId, GaussianSplat, LocalRadiusQuery, SplatMap, SplatPosteriorView

splat_map = SplatMap(
    frame=FrameId("map"),
    splats=(
        GaussianSplat(
            center=(0.0, 0.0, 0.0),
            covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1),
            opacity=0.8,
            provenance="front-camera",
        ),
    ),
)
view = SplatPosteriorView(splat_map)
nearby = view.query_local(LocalRadiusQuery(center=(0.0, 0.0, 0.0), radius=1.0, max_results=8))
summary = view.summary()
uncertainty = view.uncertainty()
provenance = view.provenance()

assert nearby.count == 1
assert nearby.total_matches == 1
assert nearby.truncated is False
assert summary.splat_count == 1
assert uncertainty.semantics == "descriptive_only"
assert provenance.counts == {"front-camera": 1}
```

## Backend and Dependency Boundary

Mosaic is a pure-Python headless library. Core imports are expected to work with `dependencies = []` and without accelerator stacks, native computer-vision stacks, robot middleware, browser services, or provider SDKs.

real 3DGS backend integration remains blocked until deterministic evaluation gates pass. Mosaic currently provides deterministic evaluation gates, typed failure classes, benchmark JSON/JSONL artifacts, and the `DeterministicSplatBackend` contract backend. It does not provide native 3DGS optimization integration or dependency expectations for production reconstruction backends.

`DeterministicSplatBackend` is a deterministic reference backend for contract tests, examples, replay validation, and benchmark smoke checks. It is not a real 3D Gaussian Splatting optimizer.

`ProvenancePreservingFusion` is a provenance-preserving contract strategy. It validates compatible map inputs, preserves and diagnoses splats, reports the stable machine-readable label `preserved_not_optimized`, does not optimize Gaussians, and does not collapse overlapping splats into occupancy-grid cells. It is not real Gaussian optimization, calibrated uncertainty minimization, loop closure, map alignment, or multi-session reconstruction.

Agent posterior APIs provide bounded descriptive posterior views over immutable `SplatMap` snapshots. Their uncertainty summaries use `descriptive_only` semantics and are not representation memories, tool facades, provider wrappers, robot execution paths, spatial indexes, or real backend behavior; those Phase 7 representation memories/tools remain planned as separate contracts.

The following remain deferred, not required for Phase 1, and out of scope for the core setup path:

- production 3DGS backend integrations
- robot execution wrappers and vendor robot SDKs
- simulator benchmark runners
- browser UI or WebSockets demos
- provider integrations and agent runtime orchestration
- native image-processing or tensor stacks as required runtime dependencies

Downstream packages can wrap Mosaic for those environments later. The Mosaic core owns typed representation contracts and deterministic seams first.

## Known Hardening Gaps

Mosaic intentionally leaves several hardening tracks for later phases:

- coordinate-frame semantics still need explicit pose direction, parent/child frame meaning, handedness, optical-frame convention, and timestamp precision tests
- Gaussian covariance layout and artifact schemas need versioned serialization and round-trip coverage
- backend registry metadata, availability checks, optional dependency reporting, and parametrized contract tests are not complete
- fusion diagnostics need richer uncertainty, conflict, and anti-occupancy-grid semantics beyond the initial reference strategy
- future production backend work must keep passing deterministic lifecycle, trajectory, map-fusion, and agent-query evaluation gates before integration
- agent posterior APIs now provide bounded descriptive posterior views with request-limited local results, truncation metadata, descriptive uncertainty summaries, and repeated-query determinism coverage; Phase 7 representation memories/tools remain planned separately
- ARNA-informed representation-memory and deterministic tool APIs are planned but not part of this baseline

The cranky version: Phase 1 gives us a usable typed contract baseline, not magic robotic autonomy. That is a feature, not a bug.