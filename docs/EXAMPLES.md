# Mosaic examples

This page documents one canonical Mosaic v1 foundation golden path. It is a narrative snippet, not a full standalone tutorial program or an API tour.

The path is intentionally local and deterministic: deterministic replay, the deterministic backend contract fixture, an actual `SplatMap` snapshot, a local/disposable benchmark artifact, a bounded posterior query, and a provider-free `RepresentationMemory` memory/tool-style query.

## Canonical deterministic golden path

The example starts with deterministic replay and a reference backend:

```python
from pathlib import Path

from mosaic import (
    DeterministicSplatBackend,
    FrameId,
    RepresentationMemory,
    SplatMap,
    SplatPosteriorView,
    run_slam_benchmark,
    synthetic_forward_sequence,
    write_benchmark_artifact,
)
from mosaic.agents import CellState, ClaimId, LocalRadiusQuery, SpatialCell

scenario = synthetic_forward_sequence(frame_count=3)
backend = DeterministicSplatBackend(map_frame=FrameId("map"))

for observation in scenario.sequence:
    backend.process(observation)

snapshot = backend.snapshot()
assert isinstance(snapshot, SplatMap)
```

`synthetic_forward_sequence(frame_count=3)` returns a deterministic local scenario. `DeterministicSplatBackend(map_frame=FrameId("map"))` processes each observation and `backend.snapshot()` returns the actual immutable `SplatMap` snapshot that later queries inspect.

The benchmark side of the same path writes a disposable local artifact. No external service, provider API, robot middleware, browser runtime, or remote storage is involved:

```python
artifact = run_slam_benchmark(
    scenario=scenario,
    backend=DeterministicSplatBackend(map_frame=FrameId("map")),
)
write_benchmark_artifact(artifact, Path("mosaic-benchmark.json"))

assert artifact.scenario_name == "synthetic-forward-3"
assert artifact.backend_name == "deterministic-splat"
```

`write_benchmark_artifact` writes stable JSON with a trailing newline to `Path("mosaic-benchmark.json")`. Treat that file as local/disposable output for smoke checks and regression artifacts, not as a production benchmark database.

The posterior side queries the snapshot through a bounded descriptive layer:

```python
posterior = SplatPosteriorView(snapshot)
local = posterior.query_local(
    LocalRadiusQuery(center=(0.0, 0.0, 0.0), radius=10.0, max_results=2)
)

assert local.total_matches >= local.count
```

`SplatPosteriorView` is a provider-free layer over a `SplatMap`. `LocalRadiusQuery` bounds local geometry output through `max_results`; `query_local(...)` returns typed aggregate IDs and truncation metadata instead of dumping raw full splat state.

The memory/tool endpoint remains a separate provider-free layer:

```python
memory = RepresentationMemory.empty(frame=FrameId("map")).with_cell(
    SpatialCell(
        frame=FrameId("map"),
        coordinate=(1, 2),
        resolution=0.5,
        state=CellState.FRONTIER,
        traversability=0.75,
        claim_ids=(ClaimId("claim-frontier-1"),),
    )
)
frontiers = memory.query_navigation_frontiers(max_results=1)

assert frontiers.total_matches >= len(frontiers.items)
```

`RepresentationMemory.query_navigation_frontiers(...)` is the terminal provider-free memory/tool-style query in this golden path. It returns a bounded `MemoryQueryResult` for navigation consumers. It does not call an LLM/LVLM provider, issue robot commands, or read raw dense geometry.

## What this example proves

- `synthetic_forward_sequence` supplies deterministic replay input.
- `DeterministicSplatBackend` is executable as a contract/reference fixture.
- `backend.snapshot` returns an actual `SplatMap` snapshot for posterior inspection.
- `run_slam_benchmark` and `write_benchmark_artifact` produce a local/disposable `mosaic-benchmark.json` artifact.
- `SplatPosteriorView`, `LocalRadiusQuery`, and `query_local` keep splat-posterior access bounded and descriptive.
- `RepresentationMemory` and `query_navigation_frontiers` expose the higher deterministic memory/tool contract separately from the posterior view.

## Boundaries

`DeterministicSplatBackend`, deterministic scenarios, benchmark gates, and `ProvenancePreservingFusion` are contract/reference fixtures for tests, examples, and regression gates. They are not production SLAM systems, real 3DGS reconstruction backends, calibrated uncertainty minimizers, CUDA/native optimizers, or reconstruction-quality implementations.

`SplatPosteriorView` and `RepresentationMemory` are separate provider-free layers. The former describes bounded splat-snapshot posterior state; the latter exposes higher memory/tool contracts. Neither layer integrates ROS, Habitat, UI/WebSockets, LLM/LVLM providers, CUDA/native stacks, or production SLAM quality.
