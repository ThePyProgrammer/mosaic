# Mosaic

Mosaic is a typed, headless Python library for 3D Gaussian Splatting SLAM over multi-view moving cameras on robotic systems: quadrupeds, UGVs, humanoids, and custom camera rigs.

The library is built around one core idea: robotic world models should be useful to both SLAM backends and intelligent agents. Mosaic treats LLM/LVLM agents as first-class consumers of the representation, not as afterthoughts that scrape raw maps, prompts, or dense splat dumps.

## Mission

Mosaic provides stable pure-Python contracts for splat-native robotic perception:

- frames, timestamps, poses, camera intrinsics, image buffers, and multi-view observations
- immutable Gaussian splats and `SplatMap` snapshots
- deterministic replay sequences and fake backend lifecycles
- robot-neutral platform and camera-rig descriptions
- splat-native fusion seams that preserve provenance
- deterministic evaluation artifacts and regression gates
- bounded agent-facing posterior queries over map state

The long-term goal is to make agents able to perceive, inspect belief, reason over uncertainty and provenance, coordinate with robots, and query memory through typed deterministic APIs. Agents should ask questions of the representation instead of receiving unbounded raw geometry or provider-specific prompt blobs.

## Why agents are first-class citizens

Most robotic mapping stacks expose geometry for planners and visualizers first, then bolt on language-agent access later. Mosaic takes a different stance: if agents are expected to reason inside a robot's world model, the representation must expose agent-appropriate views from the start.

In Mosaic, first-class agent access means:

- **Bounded outputs**: agent APIs return typed summaries, local views, counts, provenance, and diagnostics instead of full map dumps by default.
- **Provider-free contracts**: the core package does not import LLM SDKs, ROS, Habitat, or robot execution dependencies.
- **Evidence and provenance**: posterior and memory APIs carry source information so downstream agents can explain what they believe and why.
- **Determinism before autonomy**: queries and evaluation artifacts are designed to be repeatable before real robot or LLM integrations are added.
- **Representation-native tools**: future agent tools will query spatial/raster memory, scene graphs, text summaries, belief/provenance, commitments, and context through stable Python interfaces.

Current agent-facing APIs include `LocalRadiusQuery`, `SplatQueryResult`, `PosteriorSummary`, `ProvenanceSummary`, and `SplatPosteriorView`.

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
nearby = view.query_local(LocalRadiusQuery(center=(0.0, 0.0, 0.0), radius=1.0))
summary = view.summary()
provenance = view.provenance()

assert nearby.count == 1
assert summary.splat_count == 1
assert provenance.counts == {"front-camera": 1}
```

## Current baseline

The former `splat-slam-foundation` worktree has been merged into the main checkout. The current baseline includes:

| Area | Public surface |
|------|----------------|
| Core geometry and observations | `FrameId`, `Timestamp`, `Pose3`, `Quaternion`, `Translation3`, `CameraIntrinsics`, `CameraObservation`, `ImageBuffer`, `MultiViewObservation` |
| Splat maps | `GaussianSplat`, `SplatMap` |
| Dataset replay | `MultiViewSequence`, `InMemorySequence` |
| SLAM backend contracts | `SplatSlamBackend`, `SplatSlamUpdate`, `BackendCapabilities`, `TrackingState`, `DeterministicSplatBackend` |
| Platform rigs | `CameraMount`, `CameraRig`, `Embodiment`, `PlatformDescription`, `PlatformRegistry`, `quadruped_front_rig`, `ugv_surround_rig`, `humanoid_stereo_rig` |
| Fusion | `FusionInput`, `FusionResult`, `FusionStatus`, `SplatFusionStrategy`, `ProvenancePreservingFusion` |
| Evaluation | `SyntheticScenario`, `MetricResult`, `BenchmarkArtifact`, `RegressionGate`, `RegressionResult`, `run_slam_benchmark`, `check_regression_gates` |
| Agent posterior access | `AgentQueryKind`, `LocalRadiusQuery`, `SplatQueryResult`, `PosteriorSummary`, `ProvenanceSummary`, `SplatPosteriorView` |

The current package has no required runtime dependencies beyond Python. Development uses `pytest` through the `dev` dependency group.

## Install and test

Mosaic targets Python 3.12+ and uses `uv`.

```bash
uv run pytest -q
```

The current merged baseline reports 73 passing tests.

## Roadmap

Mosaic v1 is a library-foundation release. Real CUDA-backed 3DGS SLAM, ROS wrappers, Habitat runners, browser UI, and LLM provider integrations are intentionally deferred until stable contracts and regression gates exist.

### Phase 1: Merged Foundation Baseline Completion

Finish the merged baseline by documenting and validating the now-main implementation. This phase covers the public module map, install/test workflow, fake-backend boundary, initial fusion/evaluation APIs, and initial agent posterior APIs.

### Phase 2: Coordinate and Artifact Hardening

Make pose direction, parent/child frames, optical-frame convention, handedness, timestamp precision, covariance layout, and versioned artifact schemas explicit and tested.

### Phase 3: Backend Registry and Contracts

Define backend metadata, availability checks, capability reporting, lifecycle contract tests, and optional-dependency boundaries so real backends can be added without contaminating core imports.

### Phase 4: Fusion Diagnostics and Semantics Hardening

Extend the initial fusion seam with richer uncertainty, conflict, provenance, and machine-readable diagnostics while explicitly rejecting occupancy-grid union assumptions.

### Phase 5: Evaluation Metric and Failure Gate Hardening

Broaden deterministic scenarios, metrics, benchmark artifacts, and regression gates so lifecycle, trajectory, map/fusion, and agent-query failures can be classified before real backend integration.

### Phase 6: Agent Posterior View Hardening

Extend the landed `SplatPosteriorView` with richer bounded posterior summaries, uncertainty semantics, and repeated-query determinism coverage.

### Phase 7: Representation Memories and Tools

Add ARNA-informed representation memory contracts and deterministic tool families for agent-friendly access:

- spatial/raster memory
- scene graph memory
- text summary memory
- belief/provenance memory
- commitment memory
- perception, navigation, coordination, belief, and context query tools

This is where Mosaic moves from agent posterior queries over splats to a broader representation layer that agents can inspect, reason over, and use for coordination.

### Phase 8: Documentation and Release Readiness

Document implemented APIs, deferred integrations, examples, contributor policy, dependency policy, optional extras guidance, and release boundaries.

## Deferred integrations

These are important, but not part of the v1 core foundation:

- real 3D Gaussian Splatting SLAM backends
- CUDA, PyTorch, OpenCV, or native backend dependencies as required installs
- ROS nodes or robot command execution
- Habitat/ARNA benchmark reproduction
- browser UI, WebSockets, or demo orchestration
- LLM/LVLM SDK integration
- robot-specific calibrated platform packages
- persistent distributed memory stores

The intended shape is: Mosaic owns stable representation contracts; downstream systems wrap those contracts for specific robots, simulators, backends, UIs, or agents.

## Design boundaries

Mosaic should stay:

- **headless**: no UI or service runtime in core
- **typed**: public APIs are explicit Python contracts
- **splat-native**: no occupancy-grid-first abstraction leak
- **backend-isolated**: heavy or fragile real backends stay behind protocols and registries
- **agent-friendly**: bounded deterministic posterior and memory views are first-class APIs
- **provider-free**: no core dependency on any LLM provider or agent framework

## Status

Mosaic is early but no longer empty: the core foundation, fake backend, platform rigs, fusion seam, evaluation harness, and first agent posterior view are implemented. The next priority is completing Phase 1 documentation and validation so later hardening phases can proceed without redefining the baseline.
