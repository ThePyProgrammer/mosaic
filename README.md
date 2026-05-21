# Mosaic

Mosaic v1 foundation is a typed, headless Python library for 3D Gaussian Splatting SLAM contracts over multi-view moving cameras. It provides pure-Python representation contracts for frames, poses, cameras, observations, splat maps, backend lifecycles, platform camera rigs, evaluation artifacts, fusion seams, posterior views, and representation memories.

Mosaic v1 is a library foundation, not a robot runtime or production reconstruction stack. It gives backend authors, evaluation tools, platform integrations, and agent consumers a stable contract surface before any real backend integration is allowed to drag CUDA, native packages, simulators, providers, or wishful thinking into the core.

## Scope

The v1 core includes:

- frame, timestamp, pose, camera, image-buffer, and multi-view observation contracts
- immutable `GaussianSplat` primitives and `SplatMap` snapshots
- deterministic in-memory multi-view replay sequences
- `SplatSlamBackend` lifecycle contracts plus `DeterministicSplatBackend` as a reference backend for tests and examples
- robot-neutral platform, embodiment, camera-rig, registry, and representative preset contracts
- fusion contracts over immutable splat maps using `FusionInput`, `FusionResult`, and `ProvenancePreservingFusion`
- deterministic scenarios, benchmark artifacts, metric helpers, and `RegressionGate` benchmark gates
- provider-free agent-facing layers: bounded `SplatPosteriorView` queries and deterministic `RepresentationMemory` memory/tool contracts

The v1 foundation does not claim production SLAM quality. It nails down typed surfaces and deterministic behavior first, because integrating a real backend before the contracts and gates exist would just manufacture expensive ambiguity.

## Documentation Map

README.md is the concise public orientation and golden-path entry point. The split release documentation is:

- [docs/API.md](docs/API.md) for the full public API map and package-surface responsibilities
- [docs/EXAMPLES.md](docs/EXAMPLES.md) for the deterministic replay, backend, artifact, posterior, and memory golden path
- [CONTRIBUTING.md](CONTRIBUTING.md) for dependency policy, test workflow, and backend extension rules

## Install and Test

Mosaic targets Python 3.12+ and uses `uv` for the project environment.

```bash
uv sync
uv run pytest -q
```

The core runtime dependency boundary is intentionally empty in `pyproject.toml`:

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
| `mosaic.slam` | Backend lifecycle protocols, registry contracts, and deterministic reference backend | `SplatSlamBackend`, `SplatSlamUpdate`, `TrackingState`, `DeterministicSplatBackend` |
| `mosaic.platforms` | Robot-neutral platform descriptions and camera rigs | `CameraRig`, `PlatformRegistry`, `quadruped_front_rig`, `ugv_surround_rig`, `humanoid_stereo_rig` |
| `mosaic.fusion` | Splat-map fusion contracts and deterministic reference strategy | `FusionInput`, `FusionResult`, `FusionStatus`, `ProvenancePreservingFusion` |
| `mosaic.evaluation` | Synthetic scenarios, benchmark artifacts, metric families, regression gates, and readiness checks | `synthetic_forward_sequence`, `run_slam_benchmark`, `FailureClass`, `RegressionGate`, `write_benchmark_artifact` |
| `mosaic.agents` | Provider-free posterior views and representation-memory/tool contracts | `SplatPosteriorView`, `LocalRadiusQuery`, `RepresentationMemory`, `MemoryQueryResult`, `QueryFamily` |

## Golden Path Teaser

The release example path is deterministic replay to contract backend to benchmark artifact to bounded agent-facing query:

```python
from pathlib import Path

from mosaic import (
    DeterministicSplatBackend,
    FrameId,
    RegressionGate,
    RepresentationMemory,
    SplatPosteriorView,
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

snapshot = backend.snapshot()
posterior = SplatPosteriorView(snapshot).summary()
memory = RepresentationMemory.empty(frame=FrameId("map"))

assert artifact.scenario_name == "synthetic-forward-3"
assert all(result.passed for result in results)
assert posterior.splat_count == len(snapshot)
assert memory.frame == FrameId("map")
```

For the fuller narrative, including deterministic replay, `DeterministicSplatBackend`, `write_benchmark_artifact`, `SplatPosteriorView`, and `RepresentationMemory`, see [docs/EXAMPLES.md](docs/EXAMPLES.md).

A fusion smoke check remains intentionally simple:

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

## Backend and Dependency Boundary

Mosaic is a pure-Python headless library. Core imports are expected to work with `dependencies = []` and without accelerator stacks, native computer-vision stacks, robot middleware, browser services, or provider SDKs.

real 3DGS backend integration remains blocked until deterministic evaluation gates pass.

The following are out of v1 core scope: real 3DGS backends, ROS, Habitat, UI/WebSockets, LLM/LVLM providers, CUDA/native stacks, and production SLAM quality. Downstream packages can wrap Mosaic for those environments later; the core owns typed representation contracts and deterministic seams first.

`DeterministicSplatBackend`, deterministic scenarios, benchmark gates, and `ProvenancePreservingFusion` are contract/reference fixtures for tests, examples, replay validation, and regression gates. They are not production SLAM, real Gaussian optimization, calibrated uncertainty minimization, or reconstruction-quality implementations.

`ProvenancePreservingFusion` validates compatible map inputs, preserves and diagnoses splats, reports the stable machine-readable label `preserved_not_optimized`, does not optimize Gaussians, and does not collapse overlapping splats into occupancy-grid cells.

## Agent-Facing Layers

`SplatPosteriorView` is a bounded descriptive splat-snapshot query layer. It exposes bounded descriptive posterior views for local geometry, summary, uncertainty, and provenance queries over immutable `SplatMap` snapshots without handing agent consumers a raw full map dump. Its uncertainty summaries use `descriptive_only` semantics.

`RepresentationMemory` is a separate higher deterministic memory/tool contract layer. It models provider-free memory and tool-style results for perception, navigation, coordination, belief/provenance, and context queries.

Neither layer integrates an LLM/LVLM provider, Habitat runner, ROS node, UI/WebSockets service, CUDA/native backend, or production robot execution path in v1.
