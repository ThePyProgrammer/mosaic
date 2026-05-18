# Argus to Mosaic Migration Plan

## Goal

Mosaic is a new typed Python library for 3D Gaussian Splatting SLAM over multi-view moving cameras across robotic systems such as quadrupeds, UGVs, and humanoids. It should borrow Argus's strongest architectural ideas without copying Argus's implementation shape wholesale.

The first hard milestone is the Splat SLAM core: typed camera/pose contracts, splat-map state, backend lifecycle interfaces, and minimal dataset replay. Agent-friendly representation posteriors should remain a first-class API seam, but they should not block the first core milestone.

## Migration Principles

- Treat this as a clean-room port: borrow concepts, contracts, testing habits, and design lessons, not implementation coupling.
- Design Mosaic as a headless Python package first. UI, WebSocket, and demo concerns can be downstream consumers later.
- Make Gaussian splats and posterior state central, rather than adapting occupancy-grid or classic-SLAM assumptions into the core.
- Keep robot embodiment details behind platform and camera-rig interfaces.
- Prefer small typed interfaces that can support multiple backends, including CUDA-heavy or native-dependency implementations.
- Leave the agent-facing posterior API thin until the parallel agent-friendly representation research resolves its core model.

## Argus Assets to Borrow

### Protocol and Registry Patterns

Source references:

- `/home/prannayag/pragnition/robotics/argus/src/slam/protocol.py`
- `/home/prannayag/pragnition/robotics/argus/src/perception/protocol.py`
- `/home/prannayag/pragnition/robotics/argus/docs/adr/0006-use-protocol-registry-pattern-for-pluggable-backends.md`

Mosaic should borrow the idea of pluggable backends with capability metadata, parameter schemas, availability checks, and contract tests. The Mosaic version should be splat-native: backend outputs should describe tracking state, map updates, splat-map snapshots, uncertainty, and diagnostic metrics.

### Heavy Backend Isolation

Source reference:

- `/home/prannayag/pragnition/robotics/argus/docs/adr/0008-isolate-heavy-and-crashy-backends-in-subprocesses.md`

Gaussian splatting backends may depend on CUDA, native libraries, research code, and fragile runtime state. Mosaic should preserve a seam where backends can run in-process for simple tests or out-of-process for crash isolation.

### Robot Platform Abstraction

Source references:

- `/home/prannayag/pragnition/robotics/argus/docs/adr/0015-introduce-robot-platform-abstraction.md`
- `/home/prannayag/pragnition/robotics/argus/src/bridge/platforms/base.py`
- `/home/prannayag/pragnition/robotics/argus/src/bridge/platforms/types.py`
- `/home/prannayag/pragnition/robotics/argus/src/bridge/platforms/registry.py`

Mosaic should borrow the separation between robot-specific configuration and shared perception/mapping logic. The Mosaic version should describe camera rigs, sensor timing, frame conventions, and embodiment metadata for quadrupeds, UGVs, humanoids, and custom rigs.

### Multi-Map Coordination Ideas

Source references:

- `/home/prannayag/pragnition/robotics/argus/src/coordination/merge_protocol.py`
- `/home/prannayag/pragnition/robotics/argus/src/coordination/merge_strategies/`

Mosaic should borrow the strategy-interface shape for map fusion and registration, but the implementation model should be posterior-aware. Splat-map fusion must preserve uncertainty and provenance rather than defaulting to union-style occupancy behavior.

### Evaluation and Regression Discipline

Source references:

- `/home/prannayag/pragnition/robotics/argus/tests/contract/`
- `/home/prannayag/pragnition/robotics/argus/tests/slam/`
- `/home/prannayag/pragnition/robotics/argus/tests/perception/`
- `/home/prannayag/pragnition/robotics/argus/tests/metrics/`
- `/home/prannayag/pragnition/robotics/argus/docs/locomotion-benchmark.md`

Mosaic should borrow Argus's emphasis on contract tests, deterministic fixtures, integration-style validation, machine-readable metric artifacts, and regression gates. Mosaic's evaluation targets should be camera trajectory consistency, map/splat quality, replay determinism, backend lifecycle correctness, and agent-facing query stability.

### Agent-Friendly Representation Research

Source references:

- `/home/prannayag/pragnition/robotics/argus/outputs/agent-friendly-representations.md`
- `/home/prannayag/pragnition/robotics/argus/outputs/agent-friendly-representations-research-architecture.md`
- `/home/prannayag/pragnition/robotics/argus/outputs/agent-friendly-representations-research-mapping.md`
- `/home/prannayag/pragnition/robotics/argus/outputs/agent-friendly-representations-research-agent-interfaces.md`
- `/home/prannayag/pragnition/robotics/argus/outputs/agent-friendly-representations-research-3d-twins.md`

These should inform Mosaic's `agents` API seam, but they should not force an early implementation. Another research thread is already exploring this topic, so Mosaic should reserve clean interfaces for posterior queries and scene summaries while keeping the first milestone focused on Splat SLAM core.

## What Not to Port Directly

- Argus frontend, WebSocket, and browser visualization code.
- Go2-specific platform behavior.
- MuJoCo and locomotion-specific assumptions.
- Classic SLAM backend details as Mosaic's core abstraction.
- Occupancy-grid and union-merge assumptions where splat posterior fusion is required.
- Demo orchestration code that mixes runtime, UI, and research concerns.

## Proposed Mosaic Package Shape

```text
src/mosaic/
  core/              # Frames, timestamps, poses, camera models, coordinate conventions
  splats/            # Gaussian primitives, splat maps, posterior state containers
  slam/              # Backend protocol, tracking/mapping lifecycle, result types
  datasets/          # Multi-view sequence loaders and replay abstractions
  platforms/         # Robot/camera-rig descriptions for quadrupeds, UGVs, humanoids
  fusion/            # Multi-camera and multi-session splat-map fusion interfaces
  evaluation/        # Metrics, benchmark scenarios, regression artifacts
  agents/            # Agent-facing query and posterior contracts
```

The first implementation pass should make only `core`, `splats`, `slam`, and minimal `datasets` concrete. The other namespaces should be planned as seams, not fully built immediately.

## Milestones

### 1. Foundation: Typed Geometry and Camera Contracts

Define the shared data model for frames, timestamps, poses, transforms, camera intrinsics, camera extrinsics, multi-view observations, and replayable sequences. This milestone should establish coordinate conventions clearly enough that all later backends and robot platforms can share them.

Done means:

- Typed pose, frame, timestamp, camera, and observation objects exist.
- A minimal multi-view sequence can be represented and replayed deterministically.
- Tests cover shape validation, frame consistency, and basic serialization if serialization is included.

### 2. Splat SLAM Core

Define the Gaussian/splat primitives, splat-map state container, backend protocol, tracking/mapping lifecycle, reset behavior, snapshot behavior, and diagnostic result objects. Include a fake or deterministic reference backend so tests can exercise the lifecycle without a real CUDA backend.

Done means:

- A backend protocol can ingest multi-view observations and produce tracking/map-update results.
- Splat-map state has a stable typed representation.
- Contract tests can validate any backend implementation against the same lifecycle expectations.

### 3. Argus-Derived Platform Layer

Clean-room port Argus's platform abstraction into robot-neutral camera-rig descriptions. Focus on camera rig metadata, frame trees, sensor timing, and embodiment labels rather than locomotion behavior.

Done means:

- Quadruped, UGV, humanoid, and custom rig descriptions can share the same interface.
- Platform definitions can produce the camera/frame metadata required by the Splat SLAM core.
- No platform implementation requires Go2, MuJoCo, or a specific simulator.

### 4. Evaluation and Regression Harness

Borrow Argus's testing posture and adapt it to Gaussian splatting SLAM. Create deterministic synthetic sequences, backend contract tests, map quality metrics, trajectory consistency metrics, and machine-readable benchmark outputs.

Done means:

- A small benchmark can run deterministically on a fake or lightweight backend.
- Metrics are emitted in a stable machine-readable format.
- Regression gates can distinguish lifecycle failures, pose failures, map failures, and query/API failures.

### 5. Agent Posterior Integration Seam

Add the first thin agent-facing contracts for querying representation posterior state. This should support scene summaries, local spatial queries, uncertainty-aware views, provenance, and references back to splat-map state without freezing the final agent representation model too early.

Done means:

- Agent-facing APIs can query a splat-map or posterior snapshot through typed interfaces.
- The API can evolve with the parallel agent-friendly representation research without forcing changes into the Splat SLAM backend protocol.
- Tests cover query determinism and basic uncertainty/provenance plumbing.

## Initial Test Strategy

- Unit tests for geometry, camera models, splat primitives, and result objects.
- Contract tests for backend lifecycle behavior: initialize, ingest, update, snapshot, reset, and error reporting.
- Dataset replay tests for deterministic ordering and timestamp/frame consistency.
- Platform tests for camera-rig construction across representative robot categories.
- Evaluation tests for metric output shape and deterministic fake-backend benchmarks.
- Agent API tests limited to stable query contracts once the initial seam exists.

## Risks and Open Questions

- The Gaussian splatting backend choice is intentionally undecided. The core protocol should not assume one research implementation.
- Coordinate-frame conventions must be nailed down early; otherwise platform, dataset, and backend work will drift.
- Splat posterior fusion is not the same problem as occupancy-map union. Fusion APIs should avoid premature implementation details.
- Agent-friendly representation requirements may change after the parallel research finishes. Keep `agents` thin until then.
- Native/CUDA backend isolation may be unnecessary for the fake backend but should remain available before integrating fragile research code.

## Migration Plan Done Criteria

This migration plan is complete when Mosaic has a clear clean-room path from Argus concepts to a headless Python Splat SLAM library, with explicit boundaries around what is borrowed, what is rejected, what the package shape should become, and which milestones should be tackled first.
