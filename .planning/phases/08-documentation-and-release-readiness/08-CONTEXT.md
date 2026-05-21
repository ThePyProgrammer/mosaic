# Phase 8: Documentation and Release Readiness - Context

**Gathered:** 2026-05-21
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 8 turns the implemented Mosaic v1 foundation into release-ready public documentation. It must document the current pure-Python library APIs, the minimal end-to-end usage path, release boundaries, deferred integrations, and contributor rules for extending Mosaic without breaking backend, dependency, evaluation, or agent/provider boundaries.

This phase is documentation and doc-test hardening only. It does not add real 3DGS backends, ROS/Habitat wrappers, UI/WebSocket demos, LLM/LVLM provider integration, CUDA/native dependencies, production SLAM claims, or new runtime capabilities beyond documenting the implemented API surface.

</domain>

<decisions>
## Implementation Decisions

### Documentation Shape
- **D-01:** Use split release documentation, not a README-only guide.
- **D-02:** Keep `README.md` concise as the public orientation page and golden-path entry point.
- **D-03:** Add dedicated docs for API surface and examples, with expected targets such as `docs/API.md` and `docs/EXAMPLES.md`.
- **D-04:** Add contributor guidance in a dedicated contributor-facing document, expected as `CONTRIBUTING.md` unless the planner finds a stronger existing convention.
- **D-05:** Add or extend machine checks for the split docs. Tests should assert key headings, commands, boundary terms, and example import/API paths so docs do not drift silently.

### Canonical End-to-End Example
- **D-06:** The canonical example should be one golden path, not an API tour: deterministic replay → fake/backend contract fixture → splat snapshot or benchmark result → benchmark artifact → agent-facing representation-memory query.
- **D-07:** The golden path should end with a representation-memory/tool-style query so Phase 7's implemented agent-friendly layer is visible in release docs.
- **D-08:** The example should write a local benchmark artifact, because DOCS-02 requires evaluation artifact coverage. Keep the artifact local/disposable and do not imply external services.
- **D-09:** Present the golden path as a narrative snippet rather than a full copy-paste script. It should be readable and API-accurate, but does not need to be a standalone tutorial program.

### Release Boundary Wording
- **D-10:** Use blunt explicit boundary language for deferred integrations. Public docs should name real 3DGS backends, ROS, Habitat, UI/WebSockets, LLM/LVLM providers, CUDA/native stacks, and production SLAM quality as out of v1 core scope.
- **D-11:** Describe `DeterministicSplatBackend`, deterministic scenarios, benchmark gates, and `ProvenancePreservingFusion` as contract/reference fixtures for tests, examples, and regression gates. Do not describe them as production SLAM, real Gaussian optimization, calibrated uncertainty minimization, or reconstruction-quality implementations.
- **D-12:** Present posterior views and representation memories as separate provider-free layers: `SplatPosteriorView` is a bounded descriptive splat-snapshot query layer; `RepresentationMemory` and related tools are a higher deterministic memory/tool contract layer.
- **D-13:** Rewrite stale phase-era wording into release-versioned language. Public docs should say “Mosaic v1 foundation” and describe current implemented modules rather than “Phase 1 baseline” or “Phase 7 planned.” Keep phase history in planning artifacts, not as the main public framing.

### Contributor Policy
- **D-14:** Contributor guidance should give equal prominence to dependency boundary, API stability, and test workflow.
- **D-15:** Optional extras guidance should be policy-only in Phase 8. Explain that heavy future integrations must be optional and isolated, but do not add placeholder extras to `pyproject.toml` until a real optional integration exists.
- **D-16:** Public API additions must update appropriate package `__all__` exports, root export decisions where relevant, API docs, and public API tests.
- **D-17:** Real-backend contributor guidance should stop at the contract boundary: registry/adapter seam, availability checks, and contract tests. Do not provide detailed real backend implementation instructions in v1 docs.

### Claude's Discretion
- The planner may choose exact filenames for the dedicated API/examples docs if they preserve the split-doc intent and pass doc contract tests.
- The planner may choose exact doc-test organization, provided tests are low-maintenance and match existing deterministic pytest style.
- The planner may choose how much of the golden path remains in `README.md` versus `docs/EXAMPLES.md`, provided README stays concise and links to the deeper doc.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Roadmap and Requirements
- `.planning/ROADMAP.md` — Defines Phase 8 goal, success criteria, DOCS requirements, and the completed Phase 1–7 implementation context.
- `.planning/REQUIREMENTS.md` — Defines DOCS-01 through DOCS-03 and v1 out-of-scope boundaries.
- `.planning/PROJECT.md` — Captures project-level constraints: pure-Python foundation, backend isolation, evaluation before backend integration, provider-free agent APIs, and bounded typed outputs.
- `.planning/STATE.md` — Current workflow position and latest completed phase state.

### Prior Phase Decisions
- `.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md` — Carries forward implemented representation-memory/tool contracts, scenario anchors, provider-free boundary, and Phase 7 agent layer semantics.
- `.planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md` — Carries forward posterior-view boundaries, bounded output rules, descriptive uncertainty semantics, and raw-map avoidance.
- `.planning/phases/05-evaluation-metric-and-failure-gate-hardening/05-CONTEXT.md` — Carries forward evaluation artifacts, failure classes, JSON/JSONL output, regression gates, and the real-backend integration block.

### Current Public Docs and Doc Tests
- `README.md` — Existing public documentation to revise into concise v1 release orientation and golden-path entry point.
- `tests/test_readme_contract.py` — Existing doc contract tests and boundary assertions to extend or complement for split docs.
- `pyproject.toml` — Runtime dependency and pytest configuration source; confirms empty runtime dependencies and `pytest` dev dependency.

### Public API Surfaces
- `src/mosaic/__init__.py` — Root public export surface; use to keep API docs synchronized with stable root exports.
- `src/mosaic/core/__init__.py` — Core frame, timestamp, pose, camera, image, and observation export surface.
- `src/mosaic/datasets/__init__.py` — Deterministic replay export surface.
- `src/mosaic/splats/__init__.py` — Gaussian splat primitive and map export surface.
- `src/mosaic/slam/__init__.py` — Backend protocol, deterministic backend, registry, and contract export surface.
- `src/mosaic/platforms/__init__.py` — Platform and camera-rig export surface.
- `src/mosaic/fusion/__init__.py` — Fusion protocol and reference strategy export surface.
- `src/mosaic/evaluation/__init__.py` — Metrics, scenarios, benchmark artifacts, JSON/JSONL, regression gates, and readiness export surface.
- `src/mosaic/agents/__init__.py` — Posterior query and representation-memory/tool export surface.

### Example and Policy Validation Targets
- `tests/test_public_api.py` — Existing public API export tests; align API docs and root export claims with this style.
- `tests/evaluation/test_runner.py` — Benchmark artifact behavior and writer patterns relevant to the golden path.
- `tests/evaluation/test_representation_scenarios.py` — Representation-memory scenario coverage relevant to the final example endpoint.
- `tests/agents/test_representation_memory.py` — Representation memory query behavior relevant to the release example.
- `tests/slam/test_backend_registry.py` — Backend registry and availability boundary behavior relevant to contributor policy.
- `tests/slam/test_backend_contract_helpers.py` — Contract-test helper behavior relevant to contributor policy.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `README.md` already contains install/test commands, public API map, smoke examples, and boundary language, but it is phase-era and partly stale after Phase 7.
- `tests/test_readme_contract.py` already enforces README headings, commands, dependency-boundary wording, fusion boundary wording, and example API correctness. Phase 8 can extend this pattern for new split docs.
- `src/mosaic/__init__.py` exposes the current stable root API, including `RepresentationMemory`, `MemoryQueryResult`, `QueryFamily`, `EvidenceReference`, `FailureClass`, `RegressionGate`, benchmark writers, and evaluation readiness helpers.
- `pyproject.toml` has `dependencies = []`, dev `pytest`, and pytest config for `tests` plus `src`, making the release docs' install/test/dependency claims machine-checkable.
- Existing tests under `tests/evaluation/` and `tests/agents/` provide realistic API paths for benchmark artifacts and representation-memory queries.

### Established Patterns
- Public docs should align with explicit package export surfaces and `__all__` lists.
- Documentation tests should be deterministic pytest checks over local files and imports, not network calls or external services.
- Runtime dependency boundaries are core release semantics: no required CUDA, ROS, Habitat, browser, provider SDK, tensor, or native CV stack.
- Examples should use pure-Python deterministic fixtures and should not imply production reconstruction quality or real robot execution.
- Planning history can inform docs, but release-facing text should describe current v1 behavior rather than phase chronology.

### Integration Points
- Update `README.md` into a concise v1 orientation and link hub.
- Add dedicated API and examples docs, expected under `docs/`, and add contributor guidance expected at `CONTRIBUTING.md`.
- Extend `tests/test_readme_contract.py` or add neighboring doc contract tests to cover split docs, boundaries, commands, and key example imports.
- Keep `pyproject.toml` runtime dependencies empty unless a real optional integration exists in a future phase.

</code_context>

<specifics>
## Specific Ideas

- Public docs should use “Mosaic v1 foundation” language instead of phase-number framing.
- `README.md` should stay concise and point to deeper API, example, and contributor docs.
- The golden path should visibly connect deterministic replay/backend/evaluation artifacts to the Phase 7 representation-memory layer.
- Contributor policy should explicitly say future heavy integrations must be optional and isolated, but should not create placeholder extras yet.

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 8-Documentation and Release Readiness*
*Context gathered: 2026-05-21*
