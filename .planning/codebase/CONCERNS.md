# Codebase Concerns

**Analysis Date:** 2026-05-18

## Tech Debt

**Package scaffold is still a placeholder:**
- Issue: The importable package contains only `hello()` returning a greeting, while `pyproject.toml` still has the placeholder description and no runtime or development dependencies.
- Files: `src/mosaic/__init__.py`, `pyproject.toml`, `README.md`
- Impact: Future implementation agents cannot rely on any stable public API, version export, package documentation, or test harness. Any downstream code importing Mosaic is coupled to a placeholder rather than the planned SLAM library surface.
- Fix approach: Replace `src/mosaic/__init__.py` with a minimal versioned public API, update `pyproject.toml` metadata, add test configuration, and introduce the first real namespaces from `docs/argus-migration-plan.md`: `src/mosaic/core/`, `src/mosaic/splats/`, `src/mosaic/slam/`, and `src/mosaic/datasets/`.

**Plans are ahead of implementation:**
- Issue: The repository contains detailed implementation plans for core SLAM, platform rigs, fusion, evaluation, and agent posterior APIs, but the corresponding packages and tests do not exist in `src/mosaic/` or `tests/`.
- Files: `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`, `docs/superpowers/plans/2026-05-18-platform-camera-rig-layer.md`, `docs/superpowers/plans/2026-05-18-posterior-aware-splat-fusion.md`, `docs/superpowers/plans/2026-05-18-evaluation-regression-harness.md`, `docs/superpowers/plans/2026-05-18-agent-posterior-query-seam.md`, `src/mosaic/__init__.py`
- Impact: Planning documents describe APIs such as `mosaic.core.FrameId`, `mosaic.splats.SplatMap`, `mosaic.slam.DeterministicSplatBackend`, `mosaic.fusion.FusionInput`, `mosaic.evaluation.MetricResult`, and `mosaic.agents.LocalRadiusQuery`, but none are implemented. Executors must treat the plans as intended direction, not current API truth.
- Fix approach: Execute the plans in dependency order. Start with `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`; do not implement platform, fusion, evaluation, or agent posterior layers before the core contracts exist.

**No test harness is present:**
- Issue: There is no `tests/` directory, no pytest dependency, and no pytest configuration.
- Files: `pyproject.toml`, `src/mosaic/__init__.py`
- Impact: Refactors and new APIs have no regression protection. This is especially risky for geometry, frame, timestamp, camera, and backend lifecycle contracts where small convention drift can invalidate SLAM outputs.
- Fix approach: Add pytest as a development dependency in `pyproject.toml`, configure `testpaths = ["tests"]` and `pythonpath = ["src"]`, and create smoke, contract, and unit tests before adding real SLAM behavior.

**README is effectively empty:**
- Issue: `README.md` has no meaningful content describing package purpose, setup, usage, architecture boundaries, or current status.
- Files: `README.md`, `docs/argus-migration-plan.md`
- Impact: New contributors and agents must infer project intent from planning documents. This increases the chance of implementing UI, ROS, Habitat, or agent orchestration concerns before the headless Python SLAM core.
- Fix approach: Update `README.md` only when documentation work is explicitly requested. Keep implementation planning anchored to `docs/argus-migration-plan.md` until the public API exists.

**No concrete module boundaries exist yet:**
- Issue: The planned package shape is documented but not represented in code.
- Files: `docs/argus-migration-plan.md`, `src/mosaic/__init__.py`
- Impact: Initial implementation choices will set the architecture. If new code is added directly to `src/mosaic/__init__.py` or a single large module, the project will accumulate structure debt immediately.
- Fix approach: Add focused namespaces exactly as seams: `src/mosaic/core/` for frames, timestamps, poses, cameras, and observations; `src/mosaic/splats/` for Gaussian primitives and map snapshots; `src/mosaic/slam/` for backend protocols and fake backend; `src/mosaic/datasets/` for deterministic replay.

## Known Bugs

**Placeholder public function misrepresents package capability:**
- Symptoms: Calling `mosaic.hello()` returns `"Hello from mosaic!"`, which advertises no SLAM, splat, dataset, platform, fusion, evaluation, or posterior functionality.
- Files: `src/mosaic/__init__.py`
- Trigger: Import `mosaic` and call `hello()`.
- Workaround: Do not build against `hello()`. Replace it with `__version__` and explicit exports as soon as the first implementation phase starts.

**README provides no onboarding signal:**
- Symptoms: Reading `README.md` gives no useful setup or usage instructions.
- Files: `README.md`
- Trigger: Open project documentation from the repository root.
- Workaround: Use `docs/argus-migration-plan.md` as the source of project intent and the `docs/superpowers/plans/*.md` files as implementation guidance.

## Security Considerations

**No secret handling policy in code or docs:**
- Risk: Future integrations for datasets, hosted LLMs, robot backends, cloud storage, or experiment tracking may introduce API keys and credentials without a documented configuration boundary.
- Files: `pyproject.toml`, `README.md`, `outputs/arna-2506-17462-replication.md`
- Current mitigation: No external service dependencies or configuration readers are implemented. No `.env` contents were read or required during this audit.
- Recommendations: Keep Mosaic core dependency-free and headless. When external APIs are introduced, document environment variable names only, never values, and keep provider clients outside the core SLAM contracts.

**Future native/CUDA backend isolation is not implemented:**
- Risk: Gaussian splatting research backends may crash the interpreter, corrupt GPU state, or load unsafe native dependencies in-process.
- Files: `docs/argus-migration-plan.md`, `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`
- Current mitigation: The planned first backend is deterministic and pure Python; no native backend is present.
- Recommendations: Preserve a backend protocol seam in `src/mosaic/slam/protocol.py` and keep subprocess isolation available before integrating CUDA-heavy or native research code.

**No serialization trust boundary exists:**
- Risk: Planned dataset replay, benchmark artifacts, posterior evidence references, and map snapshots may eventually load external files. Without typed validation, malformed inputs can poison frame trees, timestamps, covariance values, or provenance.
- Files: `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`, `docs/superpowers/plans/2026-05-18-evaluation-regression-harness.md`, `docs/superpowers/specs/2026-05-18-agent-friendly-representation-design.md`
- Current mitigation: No loaders or serializers are implemented.
- Recommendations: Validate all external data at package boundaries. Reject negative timestamps, blank frame IDs, non-unit quaternions, invalid camera dimensions, malformed Gaussian covariances, and unbounded query results.

## Performance Bottlenecks

**No performance-critical code exists yet:**
- Problem: There are no SLAM, splat, fusion, replay, evaluation, or posterior query algorithms to profile.
- Files: `src/mosaic/__init__.py`, `pyproject.toml`
- Cause: The repository is currently a minimal package scaffold.
- Improvement path: Introduce deterministic pure-Python reference implementations first, then add benchmarks in `src/mosaic/evaluation/` before integrating heavy backends.

**Planned local-radius posterior queries can become linear scans:**
- Problem: The planned `mosaic.agents` query seam may scan every splat for local geometry if implemented naively.
- Files: `docs/superpowers/plans/2026-05-18-agent-posterior-query-seam.md`, `docs/superpowers/specs/2026-05-18-agent-friendly-representation-design.md`
- Cause: The planned first agent API focuses on deterministic response objects, not spatial indexing.
- Improvement path: Start with bounded deterministic behavior and explicit result limits. Add a spatial index abstraction only after `SplatMap` is stable and tests define query semantics.

**Planned fusion can duplicate large maps:**
- Problem: Provenance-preserving fusion over immutable `SplatMap` snapshots can copy all splats from all source maps.
- Files: `docs/superpowers/plans/2026-05-18-posterior-aware-splat-fusion.md`
- Cause: The planned reference strategy prioritizes frame compatibility and provenance correctness over memory efficiency.
- Improvement path: Use immutable snapshots for correctness in the first pass. Add chunked or lazy map representations later if map sizes make full tuple copies impractical.

**Evaluation artifacts may grow quickly:**
- Problem: Machine-readable benchmark artifacts can become large once real trajectories, map snapshots, and diagnostics are emitted.
- Files: `docs/superpowers/plans/2026-05-18-evaluation-regression-harness.md`, `outputs/arna-2506-17462-replication.md`
- Cause: Evaluation planning emphasizes detailed reproducibility metadata.
- Improvement path: Keep initial artifacts summary-only: metric name, value, unit, scenario, backend, and deterministic seed. Store large map or frame payloads behind explicit evidence references rather than embedding them in JSON outputs.

## Fragile Areas

**Coordinate-frame conventions are a critical unresolved seam:**
- Files: `docs/argus-migration-plan.md`, `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`, `docs/superpowers/plans/2026-05-18-platform-camera-rig-layer.md`
- Why fragile: Frames connect camera observations, robot rigs, backend tracking results, fusion compatibility, and agent queries. Ambiguous parent/child direction or frame naming will cause silent geometry errors.
- Safe modification: Implement `FrameId`, `Pose3`, `CameraMount`, and `CameraRig` with strict validation before any backend logic. Tests must assert parent and child frames explicitly.
- Test coverage: Missing. Add `tests/core/test_frames_and_poses.py`, `tests/core/test_observations.py`, and `tests/platforms/test_camera_rig.py` before implementing consumers.

**Backend lifecycle contract is not protected:**
- Files: `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`, `src/mosaic/__init__.py`
- Why fragile: Real Gaussian splatting SLAM backends will need initialize, ingest/update, snapshot, diagnostics, error reporting, and reset semantics. If these are improvised per backend, contract drift will be expensive.
- Safe modification: Define `src/mosaic/slam/protocol.py` with typed capability, update, result, status, snapshot, and reset contracts before adding any real backend.
- Test coverage: Missing. Add `tests/slam/test_backend_contract.py` and a deterministic fake backend in `src/mosaic/slam/fake_backend.py`.

**Splat posterior fusion can accidentally become occupancy union:**
- Files: `docs/argus-migration-plan.md`, `docs/superpowers/plans/2026-05-18-posterior-aware-splat-fusion.md`
- Why fragile: The migration plan explicitly rejects occupancy-grid union assumptions. Fusion must preserve uncertainty and provenance rather than silently merging map contents as truth.
- Safe modification: Keep fusion as a strategy protocol over immutable `SplatMap` snapshots. Require diagnostics such as source map count, source splat count, and provenance preservation.
- Test coverage: Missing. Add `tests/fusion/test_fusion_protocol.py` and `tests/fusion/test_strategies.py` after the core splat types exist.

**Agent-friendly representation requirements are intentionally fluid:**
- Files: `docs/argus-migration-plan.md`, `docs/superpowers/specs/2026-05-18-agent-friendly-representation-design.md`, `docs/superpowers/plans/2026-05-18-agent-posterior-query-seam.md`
- Why fragile: The design calls for layered belief graph, raster memory, scene graph memory, textual summaries, provenance, and commitments, but the first implementation should only expose a thin posterior query seam. Overbuilding early will freeze the wrong abstractions.
- Safe modification: Keep `src/mosaic/agents/` limited to typed deterministic queries over `SplatMap` snapshots until core, platform, fusion, and evaluation layers exist.
- Test coverage: Missing. Add query determinism, provenance summary, and bounded-result tests before any LLM or LVLM integration.

**Planning documents may be mistaken for implemented API:**
- Files: `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`, `docs/superpowers/plans/2026-05-18-platform-camera-rig-layer.md`, `docs/superpowers/plans/2026-05-18-posterior-aware-splat-fusion.md`, `docs/superpowers/plans/2026-05-18-evaluation-regression-harness.md`, `docs/superpowers/plans/2026-05-18-agent-posterior-query-seam.md`
- Why fragile: These files contain full code snippets and expected tests, but they are not source files. Search results can surface `raise NotImplementedError` and API names inside plans rather than implementation.
- Safe modification: When mapping or executing phases, distinguish `docs/superpowers/plans/` from `src/mosaic/` and `tests/`. Treat plan snippets as instructions, not current behavior.
- Test coverage: Not applicable until source files are created.

## Scaling Limits

**Current package capacity is effectively zero SLAM functionality:**
- Current capacity: One importable module with a two-line placeholder function.
- Limit: No camera models, poses, observations, splats, map state, dataset replay, backend protocol, platform rigs, fusion, evaluation, or agent posterior APIs.
- Scaling path: Implement the core foundation first using small immutable data contracts and contract tests. Defer heavy dependencies and robotics integrations until the pure-Python seams are stable.

**Dependency model does not support planned development workflow:**
- Current capacity: `pyproject.toml` has no dependencies and no dev dependency group.
- Limit: Test commands in the implementation plans use `uv run pytest`, but pytest is not declared.
- Scaling path: Add a `dev` dependency group with `pytest>=8.4.0` and configure pytest in `pyproject.toml`.

**Agent representation design exceeds first milestone scope:**
- Current capacity: Design only in `docs/superpowers/specs/2026-05-18-agent-friendly-representation-design.md`.
- Limit: Layered belief graph, raster memory, scene graph memory, commitment memory, and tool families are broader than the current package can support.
- Scaling path: Preserve API seams with `src/mosaic/agents/` only after core SLAM, platform, fusion, and evaluation layers exist. Keep first agent layer read-only and deterministic.

## Dependencies at Risk

**No runtime dependencies are pinned:**
- Risk: The project cannot yet express required libraries for numerical arrays, image buffers, geometry, or splatting backends.
- Impact: Implementers may introduce incompatible dependencies ad hoc.
- Migration plan: Keep the first core pass standard-library-only as planned in `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`. Add numerical or GPU libraries only behind backend-specific optional extras after protocols stabilize.

**pytest is referenced but undeclared:**
- Risk: Planned tests fail immediately in a fresh environment because pytest is not in `pyproject.toml`.
- Impact: Implementation agents may run commands that depend on globally installed packages, reducing reproducibility.
- Migration plan: Add `pytest>=8.4.0` under a development dependency group in `pyproject.toml` before creating tests.

**Future CUDA/native splatting dependencies are undecided:**
- Risk: Choosing a research backend too early can leak backend-specific assumptions into `mosaic.core`, `mosaic.splats`, and `mosaic.slam`.
- Impact: The library can become a wrapper around one implementation rather than a backend-agnostic SLAM substrate.
- Migration plan: Implement `typing.Protocol` interfaces and deterministic fake backends first. Add real CUDA/native backends only as separate adapters.

**ARNA/Habitat/OpenAI stack is research context, not Mosaic core dependency:**
- Risk: `outputs/arna-2506-17462-replication.md` discusses Habitat Lab, HM3D, MP3D, Grounding DINO, GPT-4o, and GPT-4o-mini. Pulling these into Mosaic core would make the library heavyweight and provider-coupled.
- Impact: Core SLAM development would inherit simulator assets, external APIs, and large model dependencies unrelated to typed 3DGS SLAM contracts.
- Migration plan: Keep ARNA-derived lessons in `src/mosaic/agents/` and evaluation designs only. Do not add Habitat, OpenAI, or Grounding DINO dependencies to the base package.

## Missing Critical Features

**Typed geometry and camera contracts:**
- Problem: `FrameId`, `Timestamp`, `Pose3`, `Quaternion`, `Translation3`, `CameraIntrinsics`, camera observations, and multi-view observations do not exist.
- Blocks: Any stable SLAM backend protocol, dataset replay, camera-rig platform layer, fusion, or agent posterior query.

**Gaussian splat primitives and map snapshots:**
- Problem: `GaussianSplat` and `SplatMap` do not exist.
- Blocks: Splat-native map state, posterior-aware fusion, evaluation metrics, and agent queries.

**SLAM backend lifecycle protocol:**
- Problem: No backend capabilities, update requests, tracking statuses, map update results, diagnostics, snapshot, or reset contracts exist.
- Blocks: Real backend integration, deterministic fake backend tests, and heavy backend isolation.

**Deterministic dataset replay:**
- Problem: No in-memory multi-view sequence or replay abstraction exists.
- Blocks: Reproducible tests, evaluation scenarios, and backend contract validation.

**Platform and camera-rig layer:**
- Problem: Robot-neutral platform descriptions for quadrupeds, UGVs, humanoids, and custom rigs do not exist.
- Blocks: Multi-view moving robotic camera support beyond hand-constructed observations.

**Posterior-aware fusion seam:**
- Problem: No fusion protocol or provenance-preserving strategy exists.
- Blocks: Multi-camera and multi-session splat-map fusion without occupancy-union assumptions.

**Evaluation and regression harness:**
- Problem: No metrics, deterministic scenarios, benchmark runner, artifact writer, or regression gates exist.
- Blocks: Measuring trajectory consistency, map quality, backend lifecycle correctness, and query stability.

**Agent posterior query API:**
- Problem: No typed agent-facing posterior query contracts exist.
- Blocks: Future LVLM/LLM agents from consuming bounded, deterministic, uncertainty/provenance-aware map views.

## Test Coverage Gaps

**Package import and public API:**
- What's not tested: Package version export, root exports, import smoke behavior, and public API stability.
- Files: `src/mosaic/__init__.py`, `pyproject.toml`
- Risk: Public API changes silently or remains placeholder-only.
- Priority: High

**Core geometry validation:**
- What's not tested: Negative timestamps, blank frame IDs, non-unit quaternions, pose parent/child frames, camera intrinsics, projection behavior, and multi-view observation consistency.
- Files: `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`
- Risk: Coordinate or calibration bugs propagate through every later layer.
- Priority: High

**Splat primitive and map validation:**
- What's not tested: Gaussian covariance shape, opacity bounds, provenance handling, immutable map snapshots, length/count behavior, and frame consistency.
- Files: `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`
- Risk: Invalid map state becomes accepted as normal and breaks fusion/evaluation later.
- Priority: High

**Backend contract lifecycle:**
- What's not tested: Initialize, ingest/update, tracking status, diagnostics, snapshot, reset, and deterministic fake backend behavior.
- Files: `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`
- Risk: Backends become mutually incompatible.
- Priority: High

**Dataset replay determinism:**
- What's not tested: Replay order, timestamp ordering, frame consistency, repeatability, and empty sequence validation.
- Files: `docs/superpowers/plans/2026-05-18-splat-slam-core-foundation.md`
- Risk: Benchmark and regression results become non-reproducible.
- Priority: High

**Platform rig validation:**
- What's not tested: Duplicate camera IDs, mount pose parent frame validation, preset rig construction, registry lookup, and embodiment metadata separation.
- Files: `docs/superpowers/plans/2026-05-18-platform-camera-rig-layer.md`
- Risk: Robot-specific assumptions leak into core SLAM logic.
- Priority: Medium

**Fusion protocol and strategy behavior:**
- What's not tested: Empty fusion inputs, mismatched frames, diagnostics immutability, provenance preservation, and rejection behavior.
- Files: `docs/superpowers/plans/2026-05-18-posterior-aware-splat-fusion.md`
- Risk: Fusion loses uncertainty/provenance or accepts incompatible maps.
- Priority: Medium

**Evaluation artifacts and gates:**
- What's not tested: Metric serialization, synthetic scenario determinism, benchmark artifact schema, and regression pass/fail thresholds.
- Files: `docs/superpowers/plans/2026-05-18-evaluation-regression-harness.md`
- Risk: Later performance claims lack stable evidence.
- Priority: Medium

**Agent posterior query determinism:**
- What's not tested: Local radius query validation, bounded query results, provenance summaries, uncertainty summaries, and deterministic scene summaries.
- Files: `docs/superpowers/plans/2026-05-18-agent-posterior-query-seam.md`, `docs/superpowers/specs/2026-05-18-agent-friendly-representation-design.md`
- Risk: Agents receive unstable or oversized world-state outputs.
- Priority: Medium

---

*Concerns audit: 2026-05-18*
