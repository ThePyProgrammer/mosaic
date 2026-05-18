# Project Research Summary: Mosaic

**Defined:** 2026-05-18
**Project:** Mosaic

## Executive Summary

Mosaic v1 should be a typed, headless Python library foundation for 3D Gaussian Splatting SLAM over multi-view robotic cameras, not a real backend demo or robotics runtime. The active `splat-slam-foundation` worktree should be treated as the implementation baseline: it already establishes the first foundation slice and should be stabilized, merged, and hardened before downstream seams are built.

The correct roadmap order is: foundation baseline, coordinate/serialization hardening, backend registry and lifecycle contracts, posterior-aware fusion, deterministic evaluation/regression, thin agent posterior query seam, then ARNA-informed representation memories and deterministic agent tools. Real 3DGS backend integration should wait until contracts, serialization, availability metadata, and regression gates exist.

## Stack Decisions

### Adopt for v1

- **Python 3.12+** as the minimum supported runtime.
- **`uv` + `uv_build`** for package, lockfile, and build workflows.
- **Committed `uv.lock`** once implementation dependencies stabilize.
- **`pytest`** for unit, contract, and deterministic integration tests.
- **Ruff and Pyright** as near-term quality gates once the foundation branch lands.
- **Frozen/slotted dataclasses and `typing.Protocol`** for stable value objects and extension seams.
- **Stdlib JSON/JSONL artifact schemas** before heavier persistence choices.
- **Zero required runtime dependencies** for foundation modules.
- **Optional extras** for future heavy backends, numeric dependencies, ROS/Habitat integrations, and LLM-facing wrappers.

### Avoid in v1 core

- Required CUDA, PyTorch, OpenCV, ROS, Habitat, simulator, or LLM SDK dependencies.
- Direct integration with a research 3DGS backend before evaluation gates exist.
- Database-backed world models before in-memory contracts prove the shape.
- Provider-specific agent APIs or prompt/runtime orchestration.

## v1 Table Stakes

1. Stabilized foundation API from the `splat-slam-foundation` worktree.
2. Explicit coordinate-frame, pose-direction, timestamp, camera optical-frame, and covariance semantics.
3. Versioned serialization/artifact schemas for core data, splat maps, backend updates, and evaluation outputs.
4. Backend registry and capability descriptors with availability checks and contract-test parametrization.
5. Posterior-aware splat-map fusion protocol that preserves provenance, uncertainty, diagnostics, and frame compatibility.
6. Deterministic synthetic evaluation scenarios, metrics, benchmark artifacts, and regression gates.
7. Thin agent posterior query seam over splat snapshots with bounded deterministic outputs.
8. ARNA-informed representation memory layer with spatial/raster memory, scene graph memory, textual memory, belief/provenance memory, commitments, and deterministic tools.
9. README guidance for public API, fake backend boundary, test commands, and v1 scope.

## Differentiators

- Treat Gaussian splats and posterior state as the central representation instead of retrofitting occupancy-grid assumptions.
- Make agent-friendly posterior queries a first-class library seam early, while avoiding LLM provider lock-in.
- Preserve uncertainty, provenance, and conflict visibility through fusion and agent-facing APIs.
- Borrow Argus-style protocol/registry discipline while keeping Mosaic clean-room, headless, and backend-neutral.
- Include deterministic regression artifacts before real backend integration.

## Deferred Scope

- Real 3DGS SLAM backend integration.
- Real object detection, room segmentation, or splat-to-occupancy extraction.
- Full ARNA/Habitat/GPT-4o reproduction.
- ROS nodes, robot command execution, UI, WebSockets, or demo orchestration.
- Calibrated robot-specific platform packages.
- Production-scale map indexing, rendering, tensor storage, or distributed multi-robot runtime.

## Recommended Architecture Phase Order

1. **Foundation baseline merge and API freeze** — stabilize the active worktree, root exports, README, and public API boundary.
2. **Coordinate semantics and serialization hardening** — pin pose/frame/time/covariance semantics and add versioned artifact schemas.
3. **Backend registry and lifecycle contracts** — add descriptors, availability checks, parameter schemas, and backend contract-test harnesses.
4. **Posterior-aware fusion seam** — add fusion protocols and deterministic reference strategies that preserve provenance and uncertainty.
5. **Evaluation and regression harness** — build synthetic scenarios, metrics, JSON artifacts, and regression gates before real backend work.
6. **Thin agent posterior query seam** — expose bounded deterministic posterior views over splat snapshots.
7. **Representation memories and deterministic tools** — implement ARNA-inspired memory views and tool APIs over claims, graph, raster, text, and commitments.
8. **Real backend readiness / adapter spike** — optional post-v1 or v1+ phase after regression gates prove the substrate.

## Critical Pitfalls and Mitigations

| Pitfall | Warning Sign | Mitigation | Roadmap Phase |
|---------|--------------|------------|---------------|
| Implicit coordinate-frame semantics | Pose math or platform transforms appear before transform direction and optical frames are documented | Add explicit frame/pose tests and serialization fields before fusion/evaluation | Phase 2 |
| Fake backend mistaken for SLAM correctness | Tests only check splat count/lifecycle but roadmap claims mapping quality | Keep fake backend as contract fixture; add metrics/gates before real backend | Phases 1, 5 |
| Late serialization | Evaluation, agent APIs, and backend registry invent incompatible dict shapes | Add versioned artifacts immediately after baseline stabilization | Phase 2 |
| CUDA/native leakage into core | Foundation modules import heavy backend libraries | Use optional extras and adapter packages behind protocols | Phase 3+ |
| Occupancy-grid fusion assumptions | Fusion API names or behavior imply union/occupied/free logic | Make fusion splat/posterior native with provenance and diagnostics | Phase 4 |
| Evaluation after backend integration | Real backend work lands without pass/fail regression or artifact output | Build deterministic synthetic harness first | Phase 5 |
| Raw splat dump as agent API | Agents receive full splat maps instead of bounded query results | Add posterior view/query seam before representation memories | Phase 6 |
| Provider-coupled agent layer | LLM prompts or SDK calls become core package dependencies | Keep representation tools deterministic Python APIs | Phase 7 |

## Research Confidence

- **High confidence:** v1 stack, phase order, foundation scope, table-stakes features, and core pitfalls.
- **Medium confidence:** future real backend integration details, real Gaussian fusion algorithms, and full ARNA-style memory/evaluation design.
- **Low confidence:** exact reproduction of ARNA paper results without public code, prompts, splits, and model snapshots.

## Inputs Used

- `.planning/PROJECT.md`
- `.planning/codebase/` maps for the main checkout
- `.planning/codebase/` maps for `/home/prannayag/pragnition/robotics/.mosaic-worktrees/splat-slam-foundation`
- `docs/argus-migration-plan.md`
- `docs/superpowers/plans/2026-05-18-*.md`
- `docs/superpowers/specs/2026-05-18-agent-friendly-representation-design.md`
- `outputs/arna-2506-17462-replication.md`

---
*Research synthesized: 2026-05-18*
