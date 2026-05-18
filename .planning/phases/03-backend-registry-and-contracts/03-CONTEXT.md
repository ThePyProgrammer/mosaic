# Phase 3: Backend Registry and Contracts - Context

**Gathered:** 2026-05-18
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 3 delivers a pure-Python SLAM backend registry and reusable backend lifecycle contract-test surface. Users must be able to register, inspect, availability-check, instantiate, and contract-test SLAM backends without importing CUDA/native dependencies into Mosaic core modules.

This phase does not integrate a real 3DGS backend, implement process supervision, add ROS/Habitat wrappers, or introduce heavy optional runtime dependencies. It creates the seam those later integrations must use.

</domain>

<decisions>
## Implementation Decisions

### Registry Shape
- **D-01:** Use a factory-based backend registry. Registered entries create fresh `SplatSlamBackend` instances so benchmarks and contract tests do not share mutable backend state.
- **D-02:** Reject duplicate backend names with `ValueError`, matching the existing `PlatformRegistry` duplicate-handling style.
- **D-03:** Provide a default backend registry containing only the deterministic built-in backend. Do not include metadata-only placeholders for future real backends.
- **D-04:** The primary retrieval API should be `create(name)`, which looks up a registered backend and returns a fresh backend instance.

### Metadata Fields
- **D-05:** Keep static backend metadata separate from runtime behavior capabilities. Add a descriptor-style object for registry metadata such as name, version, dependencies, factory, and availability behavior; keep `BackendCapabilities` focused on runtime capability flags.
- **D-06:** Model dependency requirements as optional Python package names/version specs plus a human-readable install hint. Do not build a full CUDA/device/binary/environment model in this phase.
- **D-07:** Keep backend parameter metadata JSON-ready and lightweight using immutable mappings of scalar values such as `bool | int | float | str`, consistent with current `MetricValue` and benchmark artifact conventions.
- **D-08:** Represent out-of-process support with a boolean metadata/capability flag. This phase records the boundary but does not implement process adapters.

### Availability Checks
- **D-09:** Use declarative, lightweight availability probes carried by the backend descriptor. Probes must return an availability result without constructing the backend or importing heavy/native backend modules.
- **D-10:** Availability results must include an available/unavailable status plus machine-readable missing requirements and human-readable diagnostics/install hints.
- **D-11:** Availability checks are on-demand only. Registry listing and registration should remain cheap and side-effect free.
- **D-12:** The deterministic built-in backend should have an explicit always-available availability result with no missing requirements.

### Contract Tests
- **D-13:** Expose reusable pytest helper/assertion functions for backend lifecycle contracts rather than a Mosaic pytest plugin.
- **D-14:** Contract helpers must cover the roadmap lifecycle set: reset, process, snapshot, lost tracking, not-initialized behavior, diagnostics, deterministic replay, and availability gating.
- **D-15:** Contract parametrization should check availability first and skip unavailable optional backends with the availability diagnostic as the skip reason.
- **D-16:** Contract tests should reuse the existing synthetic deterministic multi-view sequence/scenario so every backend sees comparable observations.

### Claude's Discretion
No implementation areas were explicitly delegated to Claude discretion. Downstream agents should follow the decisions above.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Roadmap and Requirements
- `.planning/ROADMAP.md` — Defines Phase 3 goal, scope, success criteria, and dependency on Phase 2.
- `.planning/REQUIREMENTS.md` — Defines BACK-01 through BACK-04 and v1/v2 dependency boundaries.
- `.planning/PROJECT.md` — Captures project-level constraints: pure-Python foundation, backend isolation, and deferral of real 3DGS integration.

### Existing Backend Surface
- `src/mosaic/slam/protocol.py` — Current `SplatSlamBackend`, `BackendCapabilities`, `TrackingState`, and `SplatSlamUpdate` contracts to extend without heavy dependency leakage.
- `src/mosaic/slam/fake_backend.py` — Existing deterministic built-in backend that should become the default registry entry and always-available backend.
- `src/mosaic/slam/__init__.py` — Public SLAM export surface that should expose any stable registry/descriptor/availability APIs.
- `src/mosaic/__init__.py` — Root public export surface that may need stable exports for backend registry APIs.

### Existing Tests and Replay Utilities
- `tests/slam/test_backend_contract.py` — Current backend lifecycle tests for deterministic process/snapshot/reset behavior; should be hardened into reusable helper-style contract coverage.
- `src/mosaic/evaluation/scenarios.py` — Existing `synthetic_forward_sequence()` scenario source for deterministic replay in backend contracts.
- `src/mosaic/datasets/replay.py` — Existing `InMemorySequence` and `MultiViewSequence` contracts used by synthetic scenarios.
- `src/mosaic/evaluation/runner.py` — Existing benchmark metadata extraction and diagnostic conventions that backend metadata changes should not break.

### Existing Registry Pattern
- `src/mosaic/platforms/registry.py` — Simple registry pattern with duplicate rejection and sorted names; useful style reference, but backend registry must store factories and availability metadata rather than platform instances.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `SplatSlamBackend` in `src/mosaic/slam/protocol.py` already defines the lifecycle seam: `name`, `capabilities`, `reset()`, `process()`, and `snapshot()`.
- `BackendCapabilities` in `src/mosaic/slam/protocol.py` already captures runtime capability flags and JSON-ready parameters; extend around it rather than overloading it with all registry metadata.
- `DeterministicSplatBackend` in `src/mosaic/slam/fake_backend.py` is stateful and currently accumulates splats, so registry factories are necessary to avoid shared state across tests and benchmarks.
- `synthetic_forward_sequence()` in `src/mosaic/evaluation/scenarios.py` provides deterministic multi-view replay input for contract helpers.
- `PlatformRegistry` in `src/mosaic/platforms/registry.py` provides a local precedent for duplicate rejection and sorted name listing.

### Established Patterns
- Public package modules use explicit `__all__` exports; new stable registry APIs should be exported from `mosaic.slam` and possibly the root package only when intended as public API.
- Data contracts are typed dataclasses with frozen/immutable mappings where appropriate; backend descriptors and availability results should follow this style.
- Diagnostics and artifact metadata use JSON-ready scalar mappings; backend metadata and availability output should remain machine-readable and dependency-light.
- The package is pure Python with no runtime dependencies; availability probing must preserve import-time safety.

### Integration Points
- `src/mosaic/slam/` is the natural home for backend descriptors, registry, availability result types, and reusable contract helpers.
- `tests/slam/` should exercise the registry, availability behavior, and helper-style lifecycle contracts against the deterministic backend.
- `src/mosaic/evaluation/runner.py` currently reads `backend.capabilities`; planning must decide whether benchmark metadata should read descriptor metadata when a registered backend is used, without breaking direct backend usage.

</code_context>

<specifics>
## Specific Ideas

No external product references or design examples were introduced. The user selected concrete implementation preferences through the discussion: factory registry, duplicate rejection, deterministic-only default registry, separate descriptors, declarative probes, on-demand availability, and helper-style pytest contracts.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 3-Backend Registry and Contracts*
*Context gathered: 2026-05-18*
