# MAGiC-SLAM Integration Design

## Objective

Integrate MAGiC-SLAM with Mosaic without weakening Mosaic core's pure-Python dependency boundary. The implementation should first make MAGiC usable through a file/process bridge, then expose that bridge through a clean Mosaic backend integration surface.

## Chosen Approach

Use a two-phase design:

1. **Out-of-process runner first.** Mosaic prepares MAGiC-compatible inputs, invokes upstream MAGiC-SLAM as an external command, and reads MAGiC outputs back into Mosaic artifacts.
2. **Clean backend integration second.** Wrap the runner in a Mosaic-facing `magic-slam` backend descriptor and factory, with availability checks and no heavy imports during normal Mosaic import.

Directly vendoring or importing MAGiC-SLAM into Mosaic core is out of scope because MAGiC requires CUDA/PyTorch/Open3D/FAISS/custom rasterizer dependencies while Mosaic core intentionally keeps `dependencies = []`.

## Architecture

The integration lives behind the existing `mosaic.slam` registry and backend-contract pattern. Core Mosaic remains importable without MAGiC installed.

New public or semi-public pieces:

- `MagicSlamConfig`: typed configuration for locating upstream MAGiC-SLAM, selecting config paths, setting input/output paths, agent IDs, and execution options.
- `MagicSlamRunner`: out-of-process command runner that validates paths, builds command arguments, runs MAGiC, and returns a typed run result.
- `MagicSlamRunResult`: immutable summary of command status, output path, known artifact paths, and scalar diagnostics.
- `magic_slam_backend_descriptor(...)`: descriptor factory for registering the integration without importing heavy packages.
- `MagicSlamBackend`: clean Mosaic-facing backend shell that delegates full-session execution to `MagicSlamRunner`.

The first implementation may keep these in `mosaic.slam.magic` if it only uses the standard library and never imports MAGiC internals. If the integration later needs direct MAGiC imports, that code must move into a downstream package such as `mosaic-magic`.

## Data Flow

Initial runner flow:

```text
Mosaic caller
  -> MagicSlamConfig
  -> MagicSlamRunner.run()
  -> python <magic_repo>/run_slam.py <config.yaml> --input_path ... --output_path ...
  -> MagicSlamRunResult
  -> optional conversion of known JSON/PLY outputs into Mosaic artifacts
```

Clean backend flow:

```text
default or custom BackendRegistry
  -> magic_slam_backend_descriptor(...)
  -> descriptor.check_availability()
  -> descriptor.factory()
  -> MagicSlamBackend
  -> runner-backed full-session execution
```

MAGiC is batch/session-oriented, while Mosaic's current `SplatSlamBackend.process(...)` is frame-oriented. The clean integration should avoid pretending MAGiC is naturally incremental until a real streaming adapter exists. The backend shell can implement the protocol conservatively for metadata/availability and expose explicit session execution through the runner.

## Availability and Dependencies

Availability must be inspectable without importing MAGiC or CUDA packages. Checks should cover:

- upstream MAGiC repo path exists;
- `run_slam.py` exists;
- Python executable is configured;
- optional package names are present when appropriate, using top-level import checks only.

The default Mosaic registry should not register a hard-coded local MAGiC path. Users or downstream packages should opt in by constructing a descriptor with their MAGiC repo path.

## Output Conversion

First implementation should report known output paths and scalar diagnostics only:

- `merged_coarse.ply`;
- `merged_refined.ply`;
- `coarse_render_metrics.json`;
- `fine_render_metrics.json`;
- `novel_render_metrics.json`;
- `walltime_stats.json`.

Converting MAGiC Gaussian outputs to `SplatMap` is a later step because MAGiC's native Gaussian state contains CUDA tensors, spherical-harmonic features, scale/rotation parameters, and optimizer state. A lossy `PLY -> SplatMap` converter can be added once the runner path is proven.

## Error Handling

The runner should fail before execution for invalid local paths and return structured diagnostics for command failures. It should not swallow stdout/stderr; command output should be captured in bounded fields or written to files under the output directory.

The backend descriptor should report missing requirements through `AvailabilityResult` rather than raising during metadata inspection.

## Testing

Default tests must be CPU-safe and should not require MAGiC, CUDA, or datasets.

Required tests:

- config validation rejects missing repo/config/input paths;
- command builder emits the expected `run_slam.py` invocation;
- runner can execute a fake MAGiC repo script and discover output artifact paths;
- failed subprocess execution returns structured failure diagnostics;
- descriptor availability reports missing repo or missing script cleanly;
- creating the descriptor does not import heavy dependencies;
- root `mosaic` import remains dependency-free.

GPU or real-dataset smoke tests are optional and must not run in the default suite.

## Non-Goals

- No direct vendoring of MAGiC-SLAM source into Mosaic core.
- No CUDA/PyTorch/Open3D/FAISS dependencies in Mosaic core metadata.
- No claim that MAGiC supports Mosaic's frame-by-frame backend protocol without a dedicated streaming adapter.
- No production-quality `SplatMap` conversion until real MAGiC outputs are available and tested.
