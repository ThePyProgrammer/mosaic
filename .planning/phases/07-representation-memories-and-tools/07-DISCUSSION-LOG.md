# Phase 7: Representation Memories and Tools - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-21
**Phase:** 7-Representation Memories and Tools
**Areas discussed:** Memory slice, Claim model, Tool facade, Scenario tests

---

## Memory slice

### Question: Should Phase 7 implement all five representation memory families as first-class contracts, or start with a thinner vertical slice?

| Option | Description | Selected |
|--------|-------------|----------|
| All five | Spatial/raster, scene graph, text, belief/provenance, and commitment memories all get typed contracts and in-memory stores in this phase. | ✓ |
| Vertical slice | Implement enough of all families to support one deterministic query per tool family, but keep each memory minimal and scenario-driven. | |
| Core first | Build only shared IDs, claims, evidence, and belief/provenance core first; defer concrete spatial/scene/text/commitment stores. | |

**User's choice:** All five
**Notes:** Phase 7 should make all five memory families first-class contracts.

### Question: How should those five memories be organized for callers?

| Option | Description | Selected |
|--------|-------------|----------|
| One world model | Expose a single RepresentationMemory object that owns spatial, scene, text, belief, and commitment stores. Simpler tool facade and scenario setup. | ✓ |
| Separate stores | Each memory family is instantiated independently; tools compose whichever stores they need. | |
| Hybrid | Implement separate store classes, plus a convenience aggregate that wires them together for tools and tests. | |

**User's choice:** One world model
**Notes:** Callers should use one aggregate representation-memory object.

### Question: Should Phase 7 include synthetic extractor/update APIs from existing Mosaic observations or splat snapshots, or only manual memory insertion contracts?

| Option | Description | Selected |
|--------|-------------|----------|
| Manual inserts | Callers/tests create cells, entities, claims, notes, and commitments directly; no extractor/update pipeline yet. | |
| Synthetic updates | Provide deterministic synthetic update helpers that turn test fixtures into memory entries without real perception. | ✓ |
| Snapshot ingest | Add an explicit SplatMap/posterior ingest seam now, even if extraction remains simple and synthetic. | |

**User's choice:** Synthetic updates
**Notes:** Synthetic helpers are in scope; real perception/extraction remains out of scope.

### Question: What should be the default mutability model for the Phase 7 memory object?

| Option | Description | Selected |
|--------|-------------|----------|
| Immutable updates | Operations return a new RepresentationMemory snapshot, matching existing Mosaic immutable contract style. | ✓ |
| Mutable store | Operations mutate the memory object in place, simpler for agent/session-like usage but less aligned with current contracts. | |
| Builder style | A mutable builder creates immutable snapshots for queries and tests. | |

**User's choice:** Immutable updates
**Notes:** Memory snapshots should follow existing Mosaic immutable contract style.

---

## Claim model

### Question: What should happen when two active robot reports contradict each other?

| Option | Description | Selected |
|--------|-------------|----------|
| Mark conflicted | Keep both claims, mark both as conflicted, and return conflict metadata through belief/tool queries. | ✓ |
| Rank winner | Keep both claims but derive one active winner by confidence/recency/source priority, demoting the other. | |
| Latest wins | Supersede older claims automatically when a newer contradictory claim arrives. | |

**User's choice:** Mark conflicted
**Notes:** Contradictions should remain visible to agent consumers.

### Question: How should claim staleness work in Phase 7?

| Option | Description | Selected |
|--------|-------------|----------|
| Explicit expiry | Claims carry valid_until; a transition helper marks stale when a supplied timestamp passes it. | ✓ |
| Age threshold | Claims carry observed_at only; each query decides staleness from a max-age parameter. | |
| Manual only | Callers explicitly mark claims stale; Mosaic does not compute stale transitions. | |

**User's choice:** Explicit expiry
**Notes:** Staleness should be deterministic and timestamp-driven.

### Question: How strict should evidence references be?

| Option | Description | Selected |
|--------|-------------|----------|
| Opaque refs | Use typed evidence kind plus opaque URI/string; do not dereference payloads. | ✓ |
| Structured refs | Require structured fields per evidence kind, such as map ID, region ID, frame ID, or cell coordinate. | |
| Payload links | Allow claims to carry optional small evidence payload summaries in addition to refs. | |

**User's choice:** Opaque refs
**Notes:** Evidence references should not pull Phase 7 into storage or payload retrieval.

### Question: Should confidence be a required numeric field on every claim?

| Option | Description | Selected |
|--------|-------------|----------|
| Required 0-1 | Every claim has confidence in [0, 1], even if synthetic tests use simple values. | ✓ |
| Optional | Claims may omit confidence when the source cannot estimate it. | |
| Enum level | Use low/medium/high confidence levels instead of floats. | |

**User's choice:** Required 0-1
**Notes:** Claims carry normalized numeric confidence.

---

## Tool facade

### Question: What should the Phase 7 tool facade expose to Python callers?

| Option | Description | Selected |
|--------|-------------|----------|
| One facade class | A RepresentationTools facade wraps RepresentationMemory and exposes one method per tool family. | |
| Module functions | Expose pure functions like find_objects(memory, ...), query_traversability(memory, ...), compare_claims(memory, ...). | |
| Methods on memory | Put tool-like query methods directly on RepresentationMemory. | ✓ |

**User's choice:** Methods on memory
**Notes:** The aggregate memory object should expose tool/query methods directly.

### Question: How should Phase 7 satisfy “one deterministic query from each family”?

| Option | Description | Selected |
|--------|-------------|----------|
| Named methods | Add one explicitly named method per family, e.g. find_objects, query_traversability, list_commitments, compare_claims, summarize_context. | ✓ |
| Generic query | Use a single query(request) dispatch with typed request/result objects for all families. | |
| Both | Expose named convenience methods over an internal typed query dispatch. | |

**User's choice:** Named methods
**Notes:** Avoid a generic query dispatcher for the first public surface.

### Question: What should all tool/query results include by default?

| Option | Description | Selected |
|--------|-------------|----------|
| Evidence+status | Every result includes bounded items plus relevant claim IDs/evidence refs/status/confidence where applicable. | ✓ |
| Items only | Return only the requested objects/frontiers/commitments/notes, leaving evidence lookup to separate belief queries. | |
| Verbose explain | Every result includes explanation text and alternatives in addition to evidence and status. | |

**User's choice:** Evidence+status
**Notes:** Results should be agent-useful without exposing raw memory dumps.

### Question: How should output bounding work for memory/tool queries?

| Option | Description | Selected |
|--------|-------------|----------|
| Request limits | Each list-like query accepts max_results/max_items and returns truncation metadata. | ✓ |
| Fixed defaults | Use hardcoded conservative limits for all list-like queries without exposing per-query limits yet. | |
| Unbounded | Do not bound results in Phase 7; tests use small memories. | |

**User's choice:** Request limits
**Notes:** List-like results should be bounded at the request level.

---

## Scenario tests

### Question: Which scenario should be the main end-to-end anchor for Phase 7?

| Option | Description | Selected |
|--------|-------------|----------|
| Blocked path | Two robots report conflicting traversability/blockage; memory marks conflict/stale state and tools explain route degradation. | |
| Search frontier | A robot explores frontiers, updates raster and scene graph memory, and context summaries cite what remains uncertain. | |
| Task allocation | Commitment memory selects/reserves a robot/resource while detecting coordination conflicts. | |

**User's choice:** can you try all 3
**Notes:** Follow-up confirmed all three should be equal small deterministic anchors.

### Follow-up: For the three scenario ideas, should Phase 7 treat them as equal anchors or choose one primary smoke path?

| Option | Description | Selected |
|--------|-------------|----------|
| All equal | Implement blocked path, search frontier, and task allocation as equal small deterministic scenario anchors. | ✓ |
| Blocked primary | Use blocked path as the primary end-to-end scenario; keep search frontier and task allocation as smaller focused tests. | |
| Frontier primary | Use search frontier as the primary end-to-end scenario; keep blocked path and task allocation as smaller focused tests. | |
| Task primary | Use task allocation as the primary end-to-end scenario; keep blocked path and search frontier as smaller focused tests. | |

**User's choice:** All equal
**Notes:** All three scenarios are equal anchors.

### Question: How should Phase 7 handle ARNA-style memory ablation tests?

| Option | Description | Selected |
|--------|-------------|----------|
| Capability blocked | Ablations prove that removing a memory family blocks or degrades the corresponding query capability, without numeric performance claims. | ✓ |
| Metric scores | Add simple deterministic scores showing worse results when scene/raster/belief memory is removed. | |
| Defer ablation | Skip ablations in Phase 7 and only test positive scenario behavior. | |

**User's choice:** Capability blocked
**Notes:** Ablations should avoid performance claims.

### Question: Where should scenario coverage live?

| Option | Description | Selected |
|--------|-------------|----------|
| Agent tests | Put Phase 7 scenario coverage under tests/agents or a new tests/agents/representation area. | |
| Evaluation tests | Integrate scenarios into the evaluation harness now. | ✓ |
| Both layers | Keep core memory/tool tests under agents, plus add lightweight evaluation hooks for future gate use. | |

**User's choice:** Evaluation tests
**Notes:** Scenario coverage should be visible through evaluation-facing tests.

---

## Claude's Discretion

- Exact names for classes, modules, enums, methods, and result dataclasses.
- Exact factoring of synthetic update helpers.
- Exact minimal fields for each first-class memory family, as long as REPR-01 through REPR-08 remain covered.

## Deferred Ideas

- LLM/LVLM provider wrappers around Mosaic tools.
- ROS, Habitat, robot command execution, and full ARNA benchmark reproduction.
- Persistent storage/database-backed representation memories.
- Real object detection, room segmentation, and real splat-to-raster extraction.
- Distributed multi-robot synchronization.
