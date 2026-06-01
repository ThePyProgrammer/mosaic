# Mosaic v1 foundation API

Mosaic v1 foundation is a typed, headless, pure-Python API surface for multi-view 3D Gaussian Splatting SLAM contracts. The implemented package is a library foundation: it defines stable frames, poses, observations, splat maps, backend contracts, deterministic fixtures, evaluation artifacts, fusion contracts, and provider-free agent query layers.

This document describes the implemented v1 package surfaces. It deliberately does not document heavy downstream integrations as installable features.

## Root package

The root `mosaic` package re-exports stable public symbols from the subpackages and exposes `__version__ = "0.1.0"`.

Representative root exports include:

- Core values: `FrameId`, `Timestamp`, `Pose3`, `Quaternion`, `Translation3`, `CameraIntrinsics`, `CameraObservation`, `ImageBuffer`, `ImageEncoding`, `MultiViewObservation`, and `Pixel`.
- Datasets and splats: `MultiViewSequence`, `InMemorySequence`, `GaussianSplat`, and `SplatMap`.
- SLAM backend contracts: `SplatSlamBackend`, `SplatSlamUpdate`, `TrackingState`, `BackendCapabilities`, and `DeterministicSplatBackend`.
- Platform contracts: `CameraMount`, `CameraRig`, `Embodiment`, `PlatformDescription`, `PlatformRegistry`, `default_platform_registry`, `quadruped_front_rig`, `ugv_surround_rig`, and `humanoid_stereo_rig`.
- Fusion contracts and fixtures: `FusionInput`, `FusionResult`, `FusionStatus`, `SplatFusionStrategy`, and `ProvenancePreservingFusion`.
- Evaluation contracts: `SyntheticScenario`, `BenchmarkArtifact`, `MetricResult`, `RegressionGate`, `RegressionResult`, `FailureClass`, `EvaluationReadinessResult`, `synthetic_forward_sequence`, `run_slam_benchmark`, `write_benchmark_artifact`, `write_benchmark_artifacts_jsonl`, `check_regression_gates`, `splat_count_metric`, and `evaluation_ready_for_real_backend`.
- Agent posterior and memory contracts: `SplatPosteriorView`, `LocalRadiusQuery`, `SplatQueryResult`, `PosteriorSummary`, `PosteriorUncertaintySummary`, `ProvenanceSummary`, `RepresentationMemory`, `MemoryQueryResult`, `QueryFamily`, `ClaimStatus`, `EntityKind`, `EvidenceReference`, and `mark_stale_claims`.

Use the subpackage imports below when a bounded context is clearer than a broad root import.

## Core

`mosaic.core` owns representation primitives shared by cameras, datasets, backends, evaluation, fusion, and agent-facing APIs.

- `FrameId` and `Timestamp` provide explicit frame labels and nanosecond timestamps.
- `Pose3`, `Quaternion`, and `Translation3` define rigid pose values and transform semantics.
- `CameraIntrinsics` and `Pixel` define camera projection inputs.
- `ImageBuffer`, `ImageEncoding`, `CameraObservation`, and `MultiViewObservation` define typed multi-view observation payloads.

These are pure value contracts with validation. They are not tied to ROS message types, OpenCV matrices, simulator state, or tensor libraries.

## Datasets

`mosaic.datasets` exposes deterministic replay contracts:

- `MultiViewSequence` is the protocol for replayable multi-view observations.
- `InMemorySequence` is the concrete immutable sequence fixture used by tests and examples.

Dataset fixtures are intentionally small and deterministic. They are contract inputs for backend and evaluation tests, not Habitat dataset loaders or robot log readers.

## Splats

`mosaic.splats` exposes Gaussian map contracts:

- `GaussianSplat` represents one Gaussian primitive with center, covariance, opacity, scale, color, and provenance fields.
- `SplatMap` is an immutable snapshot of splats in a single map frame.

A `SplatMap` is the public snapshot boundary. It is not a raw dense map dump, a CUDA buffer, or a production optimizer state object.

## SLAM backends

`mosaic.slam` defines the backend seam and deterministic reference implementation.

- `SplatSlamBackend` is the backend lifecycle protocol.
- `SplatSlamUpdate` reports tracking state, estimated pose, optional map updates, and diagnostics.
- `TrackingState` names lifecycle states.
- `BackendCapabilities` reports backend properties such as multi-view support, incremental mapping support, uncertainty support, out-of-process execution, and deterministic parameters.
- `DeterministicSplatBackend` is the built-in reference backend for contract tests, examples, replay validation, and benchmark smoke checks.
- `BackendDependency`, `AvailabilityResult`, `BackendDescriptor`, `BackendRegistry`, and `default_backend_registry` are the optional backend registration and availability-check seam.
- `assert_backend_lifecycle_contract`, `assert_backend_deterministic_replay`, `assert_backend_state_update_contract`, and `skip_unavailable_backend` are test helpers for backend implementers.
- `MagicSlamConfig`, `MagicSlamRunner`, `MagicSlamRunResult`, `MagicSlamBackend`, `MagicReplicaExportResult`, `MagicReplicaMultiAgentExportResult`, `export_sequence_to_magic_replica`, `export_agent_sequences_to_magic_replica`, `write_magic_replica_config`, `magic_run_result_to_benchmark_artifact`, `load_magic_ply_splat_map`, and `magic_slam_backend_descriptor` provide a standard-library-only out-of-process integration shell for an external MAGiC-SLAM checkout.

`DeterministicSplatBackend` is a contract/reference fixture. It is not production SLAM, not real Gaussian optimization, and not reconstruction-quality mapping.

The MAGiC-SLAM integration shell does not vendor MAGiC-SLAM and does not import CUDA, PyTorch, Open3D, FAISS, or custom rasterizer packages during normal Mosaic import. It prepares single-agent and multi-agent MAGiC-style RGB-D folders, can write a conservative Replica-style MAGiC config from exported camera metadata, invokes an external `run_slam.py` process, reports known output artifacts, converts MAGiC metric JSON into `BenchmarkArtifact`, and exposes availability through the backend descriptor seam. `load_magic_ply_splat_map` provides a lossy ASCII and binary-little-endian PLY conversion path from MAGiC Gaussian outputs to Mosaic `SplatMap`. MAGiC remains batch/session-oriented; the Mosaic shell does not claim frame-by-frame `process(...)` execution.

## Platforms

`mosaic.platforms` describes robot-neutral camera rigs and representative platform metadata.

- `CameraMount` and `CameraRig` define camera placement and lookup behavior.
- `Embodiment` and `PlatformDescription` describe robot embodiment without binding Mosaic to one robot SDK.
- `PlatformRegistry` and `default_platform_registry` provide explicit registry lookup.
- `quadruped_front_rig`, `ugv_surround_rig`, and `humanoid_stereo_rig` are representative presets.

Platform presets are deterministic contract fixtures. They are not vendor-calibrated robot packages.

## Fusion

`mosaic.fusion` defines posterior-aware splat-map fusion contracts.

- `FusionInput` packages immutable source maps.
- `FusionResult` reports fused output, status, diagnostics, and summaries.
- `FusionStatus`, `FusionProvenanceSummary`, `FusionUncertaintySummary`, and `FusionConflictSummary` expose machine-readable diagnostics.
- `SplatFusionStrategy` is the strategy protocol.
- `ProvenancePreservingFusion` is the deterministic reference strategy.

`ProvenancePreservingFusion` is a contract/reference fixture. It validates map compatibility, preserves splat provenance, and reports diagnostics. It does not optimize Gaussians, calibrate uncertainty, perform loop closure, align maps, or collapse splats into occupancy-grid cells.

## Evaluation

`mosaic.evaluation` provides deterministic scenario and benchmark contracts:

- `SyntheticScenario` and `synthetic_forward_sequence` create local deterministic replay fixtures.
- `run_slam_benchmark` runs a scenario through a backend and returns a `BenchmarkArtifact`.
- `write_benchmark_artifact` writes one stable JSON artifact with a trailing newline.
- `write_benchmark_artifacts_jsonl` writes stable JSONL artifacts.
- `MetricResult`, `splat_count_metric`, and metric-family helpers describe benchmark outputs.
- `RegressionGate`, `RegressionResult`, `FailureClass`, `check_regression_gates`, `EvaluationReadinessResult`, and `evaluation_ready_for_real_backend` provide deterministic gates before real backend work.

Benchmark gates and deterministic scenarios are contract/reference fixtures. They are meant to detect regressions in public behavior before backend integration, not to certify production SLAM quality.

## Agents

`mosaic.agents` has two provider-free layers. Keep them separate.

`SplatPosteriorView` is a bounded descriptive splat-snapshot query layer. It accepts a `SplatMap` snapshot and exposes methods such as `query_local`, `summary`, `uncertainty`, and `provenance` through `LocalRadiusQuery`, `SplatQueryResult`, `PosteriorSummary`, `PosteriorUncertaintySummary`, and `ProvenanceSummary`. Its uncertainty semantics are descriptive, not calibrated production uncertainty.

`RepresentationMemory` is a higher deterministic memory/tool contract layer. It owns spatial raster, scene graph, text, belief/provenance, and commitment snapshots, and returns bounded `MemoryQueryResult` values for tool-style queries such as `find_perception_matches`, `query_navigation_frontiers`, `list_coordination_commitments`, `inspect_belief`, and `summarize_context`. Related public symbols include `QueryFamily`, `ClaimStatus`, `EntityKind`, `EvidenceReference`, and `mark_stale_claims`.

Neither layer integrates an LLM/LVLM provider. Agent consumers get bounded typed outputs with provenance hooks, not raw full splat maps or provider-specific prompts.

## Deferred integrations

Mosaic v1 core explicitly defers real 3DGS backends, ROS, Habitat, UI/WebSockets, LLM/LVLM providers, CUDA/native stacks, and production SLAM quality.

Those deferred integrations must stay behind protocols, registries, optional dependency boundaries, availability checks, and downstream wrappers. The v1 package does not require install commands for heavy integrations and does not make reconstruction-quality or robot-execution claims.
