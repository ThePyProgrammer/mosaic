# Phase 7: Representation Memories and Tools - Research

**Researched:** 2026-05-21
**Domain:** Pure-Python typed representation memories, deterministic agent tool/query contracts, and evaluation scenario coverage
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
## Implementation Decisions

### Memory Scope and Shape
- **D-01:** Implement all five representation memory families as first-class Phase 7 contracts: spatial/raster memory, scene graph memory, text memory, belief/provenance memory, and commitment memory.
- **D-02:** Expose one aggregate representation-memory object as the primary caller-facing model. Callers should not need to manually compose separate stores for normal use.
- **D-03:** The aggregate memory object should own the five memory families and be the place where deterministic tool/query methods live.
- **D-04:** Use immutable update semantics by default: operations return new representation-memory snapshots rather than mutating caller-owned state in place.
- **D-05:** Include deterministic synthetic update helpers that can turn test fixtures into memory entries. These helpers may create cells, entities, relations, claims, notes, and commitments, but they must not claim real perception, real object detection, or real splat-to-occupancy extraction.

### Claim, Evidence, and Belief Semantics
- **D-06:** When two active robot reports contradict each other, keep both claims and mark the conflict visible. Do not auto-resolve by latest report, confidence ranking, or hidden winner selection.
- **D-07:** Conflicted claims should remain queryable through belief/provenance and tool results so agent consumers can inspect uncertainty rather than receiving silently merged truth.
- **D-08:** Claims should carry explicit `valid_until`-style expiry data. A deterministic transition helper should mark claims stale when a supplied timestamp passes that expiry.
- **D-09:** Evidence references should be typed but opaque: evidence kind plus opaque URI/string is enough. Phase 7 must not dereference or load evidence payloads by default.
- **D-10:** Every claim should carry required numeric confidence in the closed interval `[0, 1]`, even when synthetic tests use simple deterministic values.

### Tool/Query Surface
- **D-11:** Do not introduce a separate facade class for the initial tool surface. Put named deterministic query methods directly on the aggregate representation-memory object.
- **D-12:** Satisfy the one-query-per-family roadmap requirement with explicitly named methods rather than a generic `query(request)` dispatcher. Suitable initial method families include perception/search, navigation/reasoning, coordination/commitment, belief/provenance, and memory/context.
- **D-13:** Tool/query results should include bounded returned items plus relevant claim IDs, evidence references, status, and confidence where applicable. Results should be useful to an agent without exposing a raw full memory dump.
- **D-14:** List-like queries must accept request-level bounds such as `max_results` or `max_items` and return truncation metadata when more entries match than were returned.

### Scenario and Ablation Coverage
- **D-15:** Phase 7 should use three equal small deterministic scenario anchors: blocked path, search frontier, and task allocation. Do not treat one as the sole primary smoke path.
- **D-16:** The blocked-path scenario should cover conflicting traversability/blockage reports, visible conflicted claims, stale state where relevant, and route/blockage explanation behavior.
- **D-17:** The search-frontier scenario should cover spatial/raster frontier state, scene graph or context updates, and uncertainty about what remains unexplored or unconfirmed.
- **D-18:** The task-allocation scenario should cover commitment memory, robot/task/resource assignment or reservation, and conflict detection for coordination.
- **D-19:** ARNA-style memory ablation tests should be capability-oriented: removing a required memory family should block or degrade the corresponding query capability. Do not make numeric performance claims in Phase 7.
- **D-20:** Scenario coverage should live in the evaluation test area/harness rather than only under agent unit tests. Keep the representation implementation provider-free and deterministic, but route scenario validation through evaluation-facing tests so REPR-08 is visible as scenario coverage.

### Claude's Discretion
- The planner may choose exact class, enum, method, and module names, provided they follow existing Mosaic naming/export patterns and preserve the decisions above.
- The planner may choose the exact minimal fields for each memory family, provided all REPR-01 through REPR-08 requirements remain covered and all five memories are first-class contracts.
- The planner may choose how synthetic update helpers are factored, provided they are deterministic, pure-Python, and do not imply real perception/extraction support.

### Deferred Ideas (OUT OF SCOPE)
## Deferred Ideas

- LLM/LVLM provider wrappers around Mosaic tools — deferred to v2/runtime integration work.
- ROS, Habitat, robot command execution, and full ARNA benchmark reproduction — deferred outside v1 Phase 7.
- Persistent storage/database-backed representation memories — deferred until in-memory contracts prove insufficient.
- Real object detection, room segmentation, and real splat-to-raster extraction — deferred to future perception/extraction phases.
- Distributed multi-robot synchronization — deferred until local memory contracts stabilize.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| REPR-01 | Representation contracts define typed IDs, entity kinds, relation kinds, evidence references, source metadata, and query families. | Use frozen/slotted dataclasses for typed IDs and `StrEnum` for kinds; this matches Python stdlib capabilities and Mosaic's current agent style. [CITED: https://docs.python.org/3.14/library/dataclasses.html] [CITED: https://docs.python.org/3.14/library/enum.html] [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/agents/queries.py] |
| REPR-02 | Belief/provenance memory stores claims with confidence, status, timestamps, evidence, conflicts, and staleness transitions. | Implement `Claim` records with `Timestamp`, `ClaimStatus`, opaque `EvidenceReference`, `conflicts_with`, and `valid_until`; Phase 7 decisions require visible conflicts and deterministic stale transitions. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/core/frames.py] |
| REPR-03 | Spatial/raster memory stores occupancy, explored/free/occupied/frontier state, traversability hints, and evidence claim links. | Implement an in-memory cell contract with frame, resolution, cell coordinate, state, frontier/explored flags, traversability score, and claim IDs; this follows the project representation design. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/references/superpowers/specs/2026-05-18-agent-friendly-representation-design.md] |
| REPR-04 | Scene graph memory stores entities, regions, hazards, objects, landmarks, relations, confidence, and claim references. | Implement entity and relation records as immutable tuples inside `SceneGraphMemory`, with query methods bounded by max results. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/references/superpowers/specs/2026-05-18-agent-friendly-representation-design.md] |
| REPR-05 | Text memory stores bounded prompt-ready notes, summaries, uncertainty notes, and source claim references. | Implement notes/summaries as typed records with scope, bounded text, source claim IDs, and timestamps; do not add provider prompt logic. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] |
| REPR-06 | Commitment memory tracks tasks, route/resource reservations, robot intentions, time windows, and conflicts. | Implement commitment records with target/resource IDs, robot IDs, time windows, status, and conflict claim/reference IDs. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/references/superpowers/specs/2026-05-18-agent-friendly-representation-design.md] |
| REPR-07 | Agent tool facade answers one deterministic query from each family: perception, navigation, coordination, belief/provenance, and memory/context. | Put named methods directly on the aggregate `RepresentationMemory` object, not a separate facade, per locked decisions D-11/D-12. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] |
| REPR-08 | Scenario tests demonstrate conflicting robot reports, stale claims, frontier/traversability queries, blocked-path explanations, and ARNA-style memory ablations. | Add evaluation-facing tests for blocked path, search frontier, task allocation, and ablations; current evaluation tests already use deterministic scenarios and JSON-ready artifacts. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/tests/evaluation/test_scenarios.py] [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/tests/evaluation/test_runner.py] |
</phase_requirements>

## Summary

Phase 7 should be planned as a pure-Python contract expansion under the existing provider-free agent boundary, not as a runtime integration with LLMs, ROS, Habitat, databases, object detectors, or real splat extraction. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md] [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]

The recommended architecture is one immutable aggregate `RepresentationMemory` snapshot that owns five first-class memory families: spatial/raster, scene graph, text, belief/provenance, and commitment. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] It should expose named deterministic query methods directly on that aggregate for perception/search, navigation/reasoning, coordination/commitment, belief/provenance, and memory/context. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]

Use Python stdlib value-object machinery and the existing Mosaic style: frozen/slotted dataclasses, `StrEnum`, tuples, immutable mappings, validation in `__post_init__()`, explicit `__all__`, and tests that assert deterministic exact outputs. [CITED: https://docs.python.org/3.14/library/dataclasses.html] [CITED: https://docs.python.org/3.14/library/enum.html] [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/agents/queries.py] [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/evaluation/runner.py]

**Primary recommendation:** Implement `mosaic.agents.memory` as the main Phase 7 module, export stable symbols through `mosaic.agents`, add only selected root exports if public API tests require them, and place scenario/ablation coverage in `tests/evaluation/` with lower-level unit tests in `tests/agents/`. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/tests/evaluation/test_scenarios.py]

## Project Constraints (from CLAUDE.md)

- Use Python 3.12+, `uv`, pure-Python foundation modules, and `pytest`. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Keep core and agent contracts importable without CUDA/native dependencies. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Keep real 3DGS/CUDA/research backends behind protocols, registries, optional dependencies, and isolation boundaries. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Preserve frame semantics and timestamp precision; use existing `FrameId` and `Timestamp` style where representation memories need frame/time fields. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md] [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/core/frames.py]
- Keep agent APIs bounded, typed, evidence/provenance carrying, and provider-free; do not expose raw full splat maps or provider-specific prompts. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Use `src/` layout, snake_case modules/functions, PascalCase public classes, uppercase `StrEnum` members with lower-case string values, package-root barrel files, and explicit `__all__` lists. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md] [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/agents/__init__.py]
- Validate dataclass invariants in `__post_init__()` and raise `ValueError` with domain-specific messages. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Prefer immutable tuples and freeze mappings with `MappingProxyType`; avoid mutating caller-owned objects. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md] [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/agents/queries.py]
- Avoid `print()` in library code; return typed diagnostics/results instead. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Use package imports rooted at `mosaic`, not relative imports, in tests and public examples. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md] [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/tests/test_public_api.py]
- Planned local checks should use `uv run pytest ... -q`; do not invent a separate local-vs-CI entry point. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|--------------|----------------|-----------|
| Typed representation IDs/kinds/evidence/source metadata | Python library / Agent contract layer | Core frame/time values | These are stable public contracts consumed by agents and tests, while frame/time should reuse `mosaic.core` primitives. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/core/frames.py] |
| Belief/provenance claims and conflicts | Python library / Agent contract layer | Evaluation tests | Claim semantics are agent-facing representation state; scenario tests verify visible conflicts and staleness. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] |
| Spatial/raster memory | Python library / Agent contract layer | Core frame IDs | The phase requires in-memory spatial/raster contracts, not real raster extraction or occupancy-grid-first mapping. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md] |
| Scene graph memory | Python library / Agent contract layer | Belief/provenance memory | Entity/relation results should cite claim IDs/evidence rather than claim truth without provenance. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/references/superpowers/specs/2026-05-18-agent-friendly-representation-design.md] |
| Text memory | Python library / Agent contract layer | Belief/provenance memory | Text notes are bounded deterministic context records, not prompts or provider messages. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] |
| Commitment memory | Python library / Agent contract layer | Evaluation tests | Commitments track coordination state and conflicts but do not command robots. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/references/superpowers/specs/2026-05-18-agent-friendly-representation-design.md] |
| Tool/query methods | Python library / Aggregate memory object | Evaluation tests | Locked decisions require named deterministic methods directly on the aggregate memory object. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] |
| Scenario/ablation validation | Evaluation test layer | Agent unit tests | D-20 requires evaluation-facing scenario coverage for REPR-08. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] |

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python stdlib `dataclasses` | Python 3.12+ project baseline; docs checked on Python 3.14 | Frozen/slotted typed value objects for IDs, claims, cells, graph records, notes, commitments, and result types | `frozen=True` emulates immutability by raising `FrozenInstanceError` on field assignment and `slots=True` generates slots for fixed-shape objects. [CITED: https://docs.python.org/3.14/library/dataclasses.html] |
| Python stdlib `enum.StrEnum` | Added in Python 3.11 | String-valued public enums for entity kinds, relation kinds, evidence kinds, query families, claim statuses, cell states, and commitment statuses | `StrEnum` members are also strings, and `auto()` lowercases member names; Mosaic already uses this style. [CITED: https://docs.python.org/3.14/library/enum.html] [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/agents/queries.py] |
| Python stdlib `types.MappingProxyType` | Python stdlib | Freeze mapping fields in summaries/diagnostics/source metadata | Existing Mosaic result contracts freeze mapping fields this way. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/agents/queries.py] [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/evaluation/runner.py] |
| `mosaic.core.Timestamp` and `mosaic.core.FrameId` | Local package 0.1.0 | Time and frame semantics for claims, cells, notes, and commitments | Existing `Timestamp` stores integer nanoseconds and rejects negative values; `FrameId` rejects blank values. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/core/frames.py] |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `pytest` | Installed 9.0.2; latest on index 9.0.3; project dev dependency `pytest>=8.4.0` | Unit and evaluation scenario validation | Use for `tests/agents/` and `tests/evaluation/` phase coverage. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/pyproject.toml] [VERIFIED: PyPI via `uv pip index versions pytest`] [CITED: https://docs.pytest.org/en/stable/how-to/invoke.html] |
| `uv` | 0.10.10 installed | Run project tests in the repository workflow | Project configuration and CLAUDE.md point to `uv`; `uv run pytest tests/agents tests/evaluation -q` passed 78 tests in this session. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/pyproject.toml] [VERIFIED: local command] |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Stdlib dataclasses | Pydantic or attrs | Do not add dependencies for Phase 7; project constraints require pure-Python foundation modules with no new runtime deps. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md] |
| Named methods on aggregate memory | Generic `query(request)` dispatcher | Locked decisions require explicitly named methods directly on the aggregate object, not a generic dispatcher. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] |
| Persistent DB-backed stores | SQLite/Postgres/vector DB | Persistent storage is explicitly deferred; use in-memory contracts first. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] |
| Real detectors / splat-to-raster extraction | Grounding DINO, OpenCV, Habitat extraction | Real object detection and real splat-to-raster extraction are deferred; Phase 7 helpers must be synthetic and deterministic. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] |

**Installation:**
```bash
# No new runtime packages for Phase 7.
# Existing dev dependency is already declared:
uv run pytest tests/agents tests/evaluation -q
```

**Version verification:** `uv --version` returned `uv 0.10.10`; `uv run pytest --version` returned `pytest 9.0.3`; `uv pip index versions pytest` reported installed `9.0.2` and latest `9.0.3`. [VERIFIED: local command]

## Package Legitimacy Audit

> Phase 7 should not add new runtime packages. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/pyproject.toml] The existing dev package `pytest` was checked because validation depends on it. [VERIFIED: local command]

| Package | Registry | Age | Downloads | Source Repo | slopcheck | Disposition |
|---------|----------|-----|-----------|-------------|-----------|-------------|
| `pytest` | PyPI | Not checked in registry metadata | Not checked in registry metadata | Not checked in registry metadata | OK from `slopcheck install pytest`; JSON mode unsupported by installed slopcheck | Approved as existing dev dependency; no new install required. [VERIFIED: local command] |

**Packages removed due to slopcheck [SLOP] verdict:** none. [VERIFIED: local command]
**Packages flagged as suspicious [SUS]:** none. [VERIFIED: local command]

## Architecture Patterns

### System Architecture Diagram

```text
Synthetic fixture / caller update
  cells, entities, relations, claims, notes, commitments
        |
        v
RepresentationMemory.with_* update helpers
  validate fields, freeze tuples/mappings, return a new snapshot
        |
        +------------------------+--------------------------+-----------------------+
        |                        |                          |                       |
        v                        v                          v                       v
SpatialRasterMemory       SceneGraphMemory          BeliefProvenanceMemory     TextMemory
  cells/frontiers           entities/relations        claims/evidence/conflicts notes/summaries
        |                        |                          |                       |
        +------------------------+------------+-------------+-----------------------+
                                             |
                                             v
                                   CommitmentMemory
                                   tasks/reservations/intentions
                                             |
                                             v
Named deterministic query methods on RepresentationMemory
  find_perception_matches / query_navigation / list_coordination / inspect_belief / summarize_context
                                             |
                                             v
Bounded typed result objects
  returned items, claim IDs, evidence refs, confidence, status, total_matches, truncated
                                             |
                                             v
Agent consumer or evaluation scenario test
  no raw full memory dump, no provider prompt, no robot command execution
```

This diagram maps the required data flow from synthetic deterministic inputs into five memory families and out through bounded named query methods. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]

### Recommended Project Structure

```text
src/mosaic/agents/
├── memory.py          # RepresentationMemory aggregate plus memory-family contracts and named query methods
├── queries.py         # Existing posterior query contracts; add only shared query-family enum here if needed
├── posteriors.py      # Existing SplatPosteriorView; do not mix full memory implementation here
└── __init__.py        # Stable agent export barrel

tests/agents/
├── test_representation_memory.py      # Dataclass validation, immutable updates, bounded query results
└── test_representation_claims.py      # Claims, conflicts, staleness, evidence refs

tests/evaluation/
└── test_representation_scenarios.py   # Blocked path, search frontier, task allocation, ablations
```

This structure keeps Phase 7 inside the provider-free agent boundary and routes REPR-08 through evaluation-facing tests. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]

### Component Responsibilities

| Component | Responsibility | Notes |
|-----------|----------------|-------|
| `RepresentationMemory` | Own all five memory families, provide immutable update helpers, and expose named deterministic query methods | Primary caller-facing model per D-02/D-03/D-11. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] |
| `BeliefProvenanceMemory` | Store claims, evidence, source metadata, conflicts, and stale transitions | Must keep conflicting active robot reports visible. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] |
| `SpatialRasterMemory` | Store cells, occupancy/explored/frontier/traversability state, frame/resolution, and claim links | Must not claim real splat-to-raster extraction. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] |
| `SceneGraphMemory` | Store entities/regions/hazards/objects/landmarks and relations with confidence and claim refs | Supports perception/search and blocked-path explanations. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/references/superpowers/specs/2026-05-18-agent-friendly-representation-design.md] |
| `TextMemory` | Store bounded notes/summaries/uncertainty notes with source claim references | Supports memory/context queries without provider prompt machinery. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md] |
| `CommitmentMemory` | Store task assignments, reservations, intentions, time windows, and conflicts | Supports task-allocation scenario and coordination query. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md] |

### Pattern 1: Frozen typed value objects
**What:** Represent public IDs, evidence refs, claims, cells, entities, relations, notes, commitments, and result rows as `@dataclass(frozen=True, slots=True)`. [CITED: https://docs.python.org/3.14/library/dataclasses.html]
**When to use:** Use for every externally visible contract where callers should not mutate fields after construction. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
**Example:**
```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class EntityId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("EntityId value must not be blank")
```
Source: Python dataclasses docs and Mosaic validation style. [CITED: https://docs.python.org/3.14/library/dataclasses.html] [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/core/frames.py]

### Pattern 2: String-valued enums for stable public kinds
**What:** Use `StrEnum` for entity kinds, relation kinds, evidence kinds, source kinds, query families, claim status, occupancy state, traversability status, and commitment status. [CITED: https://docs.python.org/3.14/library/enum.html#enum.StrEnum]
**When to use:** Use when serialized/public values must be lower-case strings and callers may compare to strings. [CITED: https://docs.python.org/3.14/library/enum.html#enum.StrEnum]
**Example:**
```python
from enum import StrEnum

class ClaimStatus(StrEnum):
    ACTIVE = "active"
    CONFLICTED = "conflicted"
    STALE = "stale"
    SUPERSEDED = "superseded"
    REJECTED = "rejected"
```
Source: Python `StrEnum` docs and current `AgentQueryKind` pattern. [CITED: https://docs.python.org/3.14/library/enum.html#enum.StrEnum] [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/agents/queries.py]

### Pattern 3: Immutable update helpers on aggregate memory
**What:** `RepresentationMemory.with_claim(...)`, `.with_cell(...)`, `.with_entity(...)`, `.with_note(...)`, and `.with_commitment(...)` should return new aggregate snapshots. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]
**When to use:** Use for synthetic fixture ingestion and deterministic scenario setup. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]
**Example:**
```python
memory = RepresentationMemory.empty(frame=FrameId("map"))
updated = memory.with_claim(blocked_claim).with_cell(blocked_cell)
assert memory is not updated
```
Source: Phase 7 D-04 and current `SplatMap.with_splats()` immutability convention. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]

### Pattern 4: Bounded result objects with truncation metadata
**What:** List-like query results should include returned rows, total match count, and a `truncated` flag. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]
**When to use:** Use for perception/search, frontier listing, commitment listing, evidence/claim comparison, and context summaries. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md]
**Example:**
```python
@dataclass(frozen=True, slots=True)
class MemoryQueryResult:
    query_family: QueryFamily
    item_ids: tuple[EntityId | ClaimId | CommitmentId, ...]
    total_matches: int
    truncated: bool
```
Source: Existing `SplatQueryResult` implements `total_matches` and `truncated` invariant. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/agents/queries.py]

### Anti-Patterns to Avoid
- **Auto-resolving claim conflicts by latest timestamp or highest confidence:** Phase 7 requires keeping both contradictory active robot reports visible. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]
- **Adding provider wrappers or prompt orchestration:** LLM/LVLM provider wrappers are deferred. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]
- **Building a separate facade class:** D-11 requires named tool/query methods directly on the aggregate object. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]
- **Exposing a raw full memory dump as the agent tool result:** Tool/query results must be bounded and useful without full-state exposure. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]
- **Claiming real perception or real splat extraction:** Synthetic helpers may create memory entries but must not imply real perception/extraction support. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Immutable contract objects | Custom `__setattr__` guards | `@dataclass(frozen=True, slots=True)` | The stdlib provides frozen assignment protection and slots for fixed-shape classes. [CITED: https://docs.python.org/3.14/library/dataclasses.html] |
| Public string constants | Ad-hoc module-level strings | `StrEnum` | `StrEnum` is a stdlib base for constants that behave like strings. [CITED: https://docs.python.org/3.14/library/enum.html#enum.StrEnum] |
| Mapping immutability | Returning mutable dict internals | `MappingProxyType(dict(...))` | Existing Mosaic contracts freeze mappings this way. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/agents/queries.py] |
| Test execution selection | Custom test runner | `uv run pytest ... -q` | Project config uses pytest with `testpaths = ["tests"]` and `pythonpath = ["src"]`; pytest supports directory and node selection. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/pyproject.toml] [CITED: https://docs.pytest.org/en/stable/how-to/invoke.html] |
| Belief conflict semantics | Hidden winner selection engine | Explicit `conflicts_with` plus `ClaimStatus.CONFLICTED` | Phase 7 requires visible conflicts. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] |
| Evidence retrieval | URI loaders/dereferencers | Opaque typed `EvidenceReference` values | Phase 7 must not dereference or load evidence payloads by default. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] |
| Persistence/sync | Database or distributed sync layer | In-memory tuples and immutable snapshots | Persistent stores and distributed sync are deferred. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] |

**Key insight:** The hard part is not storage or algorithms; it is preserving explicit uncertainty/provenance semantics while keeping every result bounded, deterministic, typed, and provider-free. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]

## Common Pitfalls

### Pitfall 1: Treating claims as truth
**What goes wrong:** Contradictory reports are collapsed into one hidden answer. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]
**Why it happens:** Developers optimize for convenient route or object answers instead of inspection-friendly belief state. [ASSUMED]
**How to avoid:** Store both claims, mark both conflicted or link via `conflicts_with`, and include conflict IDs in query results. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]
**Warning signs:** Tests assert only a single winning blockage/traversability claim after two robot reports. [ASSUMED]

### Pitfall 2: Making stale transitions depend on wall-clock time
**What goes wrong:** Tests become nondeterministic because stale status changes with the current system clock. [ASSUMED]
**Why it happens:** Code calls `datetime.now()` or similar inside query methods. [ASSUMED]
**How to avoid:** Accept an explicit `Timestamp` in stale-transition helpers and compare against each claim's `valid_until`. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]
**Warning signs:** Repeated fixed-fixture tests can pass or fail depending on current time. [ASSUMED]

### Pitfall 3: Letting query methods leak full memory state
**What goes wrong:** Agent consumers receive raw full graph/cell/claim dumps instead of bounded result records. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
**Why it happens:** Full dumps are easier than designing family-specific result shapes. [ASSUMED]
**How to avoid:** Require `max_results`/`max_items`, include `total_matches` and `truncated`, and return only IDs plus relevant evidence/confidence/status. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]
**Warning signs:** Methods named `as_dict()` expose all cells, all entities, all claims, and all notes for normal agent queries. [ASSUMED]

### Pitfall 4: Smuggling runtime integrations into contracts
**What goes wrong:** The module imports OpenAI/Anthropic SDKs, ROS, Habitat, OpenCV, CUDA, or detector packages. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md]
**Why it happens:** ARNA inspiration is mistaken for an implementation target. [ASSUMED]
**How to avoid:** Keep ARNA as architecture inspiration only; Phase 7 implements deterministic Python contracts and synthetic helpers. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]
**Warning signs:** `pyproject.toml` gains runtime dependencies or tests need model/dataset assets. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/pyproject.toml]

### Pitfall 5: Treating ARNA ablations as numeric benchmark reproduction
**What goes wrong:** Tests assert ARNA paper performance percentages or require Habitat/GPT execution. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]
**Why it happens:** ARNA reported quantitative ablations, but Mosaic Phase 7 is not full ARNA replication. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/references/arna/arna-2506-17462-replication.md]
**How to avoid:** Write capability-oriented ablations: missing raster memory blocks/degrades frontier/traversability; missing scene graph blocks/degrades object/hazard query; missing belief/provenance blocks/degrades conflict/staleness inspection. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]
**Warning signs:** Tests mention ARNA exact correct-rate, path-length, token-usage, Habitat, or GPT-4o requirements. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/references/arna/arna-2506-17462-replication.md]

## Code Examples

Verified patterns from official/current sources:

### Frozen dataclass with validation
```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ClaimId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("ClaimId value must not be blank")
```
Source: Python dataclasses docs and Mosaic `FrameId` pattern. [CITED: https://docs.python.org/3.14/library/dataclasses.html] [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/core/frames.py]

### Bounded result invariant
```python
@dataclass(frozen=True, slots=True)
class RepresentationQueryResult:
    total_matches: int
    item_ids: tuple[str, ...]
    truncated: bool = False

    def __post_init__(self) -> None:
        if self.total_matches < len(self.item_ids):
            raise ValueError("total_matches must cover returned item_ids")
        if self.truncated is not (self.total_matches > len(self.item_ids)):
            raise ValueError("truncated must equal total_matches > count")
```
Source: Existing `SplatQueryResult` invariant. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/agents/queries.py]

### Deterministic stale transition signature
```python
def mark_stale_claims(memory: RepresentationMemory, *, now: Timestamp) -> RepresentationMemory:
    ...
```
Source: Phase 7 requires supplied timestamp stale transitions and existing `Timestamp` is deterministic integer nanoseconds. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/core/frames.py]

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Agent reads raw dense geometry or full map dumps | Agent calls deterministic bounded tool/query methods over memory views | Project direction established in current Mosaic planning docs | Keeps agent boundary stable and provider-free. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md] |
| One monolithic world model | Separate spatial/raster, scene graph, text, belief/provenance, and commitment memories under one aggregate | Phase 7 context locked D-01/D-02 | Preserves separable ablation and capability tests. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] |
| Auto-resolved belief state | Claims with visible conflicts, evidence refs, confidence, and stale statuses | Phase 7 context locked D-06 through D-10 | Agent consumers can inspect uncertainty instead of receiving hidden truth. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] |
| Full ARNA runtime reproduction | ARNA-informed deterministic contract tests and capability ablations | Phase 7 context locked D-19 and deferred ideas | Avoids Habitat/LLM/runtime scope creep while preserving memory/tool lessons. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] |

**Deprecated/outdated:**
- Adding LLM provider wrappers in v1: deferred to v2/runtime integration work. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]
- Persistent representation-memory storage in Phase 7: deferred until in-memory contracts prove insufficient. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]
- Real detector/splat extraction in Phase 7: deferred to future perception/extraction phases. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Developers may otherwise collapse conflicts into a single convenient answer. | Common Pitfalls | If wrong, pitfall wording is overcautious; implementation guidance still follows locked decisions. |
| A2 | Tests using wall-clock time would become nondeterministic. | Common Pitfalls | If wrong, deterministic explicit timestamp helpers are still required by context and safer for tests. |
| A3 | Full dumps are easier than family-specific bounded result shapes. | Common Pitfalls | If wrong, no impact; bounded result shapes remain required. |
| A4 | ARNA inspiration may tempt runtime integration scope creep. | Common Pitfalls | If wrong, no impact; deferred scope remains explicit. |

## Open Questions

1. **Should Phase 7 symbols be root-exported from `mosaic` or only from `mosaic.agents`?**
   - What we know: Existing stable agent types are exported from both `mosaic.agents` and root `mosaic`. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/__init__.py]
   - What's unclear: The phase context says update root only for stable root-level APIs, but does not list exact symbols. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]
   - Recommendation: Export all Phase 7 stable contracts from `mosaic.agents`; root-export only `RepresentationMemory` and core result/query enums if public API tests intentionally lock them. [ASSUMED]

2. **How granular should memory-family modules be?**
   - What we know: The context permits exact class/module naming discretion. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]
   - What's unclear: Whether one `memory.py` will become too large during implementation. [ASSUMED]
   - Recommendation: Start with one `memory.py` for plan simplicity; split only if class count becomes unreviewable. [ASSUMED]

3. **Should scenario fixtures live in `mosaic.evaluation.scenarios` or only in tests?**
   - What we know: Existing synthetic scenario helpers are in `src/mosaic/evaluation/scenarios.py`; D-20 wants evaluation-facing scenario coverage. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/evaluation/scenarios.py] [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]
   - What's unclear: Whether Phase 7 scenario helpers are stable enough for public package export. [ASSUMED]
   - Recommendation: Keep detailed blocked-path/search-frontier/task-allocation fixture builders private to tests initially unless they are needed by public evaluation artifacts. [ASSUMED]

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| Python | Library and tests | ✓ | `python3` reports 3.14.4; project requires >=3.12 | Use `uv run` environment if local `python3` differs. [VERIFIED: local command] |
| uv | Project test workflow | ✓ | 0.10.10 | `python -m pytest` can run pytest, but project workflow should prefer uv. [VERIFIED: local command] [CITED: https://docs.pytest.org/en/stable/how-to/invoke.html] |
| pytest | Validation | ✓ | `pytest` 9.0.2 globally; `uv run pytest` 9.0.3 | None needed. [VERIFIED: local command] |
| slopcheck | Package legitimacy audit | ✓ | 0.6.1 installed; `--json` unsupported | Non-JSON slopcheck output used. [VERIFIED: local command] |
| Context7 MCP/CLI | Library docs lookup | ✗ | No MCP tools exposed; CLI not checked because stdlib/official docs sufficed | WebFetch official docs used. [VERIFIED: tool availability in this session] |
| Planning graph | Graph context | ✗ | `graphify` disabled | Continue with file/code context. [VERIFIED: local command] |

**Missing dependencies with no fallback:** none for Phase 7 planning. [VERIFIED: local command]

**Missing dependencies with fallback:** Context7 and graphify were unavailable/disabled; official docs and direct code/context reads provided the needed evidence. [VERIFIED: tool availability in this session]

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest; project dev dependency `pytest>=8.4.0`, `uv run pytest --version` returned 9.0.3. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/pyproject.toml] [VERIFIED: local command] |
| Config file | `/home/prannayag/pragnition/robotics/mosaic/pyproject.toml` with `testpaths = ["tests"]` and `pythonpath = ["src"]`. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/pyproject.toml] |
| Quick run command | `uv run pytest tests/agents tests/evaluation -q` passed 78 tests in this session. [VERIFIED: local command] |
| Full suite command | `uv run pytest -q` [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md] |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|--------------|
| REPR-01 | Typed IDs, entity/relation/evidence/source/query families validate and export | unit | `uv run pytest tests/agents/test_representation_memory.py -q` | ❌ Wave 0 |
| REPR-02 | Claims store confidence/status/timestamps/evidence/conflicts and deterministic stale transition | unit | `uv run pytest tests/agents/test_representation_claims.py -q` | ❌ Wave 0 |
| REPR-03 | Spatial/raster cells support occupancy/explored/frontier/traversability and claim links | unit + scenario | `uv run pytest tests/agents/test_representation_memory.py tests/evaluation/test_representation_scenarios.py -q` | ❌ Wave 0 |
| REPR-04 | Scene graph stores entities/relations/confidence/claim refs and supports object/hazard queries | unit + scenario | `uv run pytest tests/agents/test_representation_memory.py tests/evaluation/test_representation_scenarios.py -q` | ❌ Wave 0 |
| REPR-05 | Text memory returns bounded prompt-ready notes/context with claim refs | unit | `uv run pytest tests/agents/test_representation_memory.py -q` | ❌ Wave 0 |
| REPR-06 | Commitment memory tracks tasks/reservations/intentions/time windows/conflicts | unit + scenario | `uv run pytest tests/agents/test_representation_memory.py tests/evaluation/test_representation_scenarios.py -q` | ❌ Wave 0 |
| REPR-07 | Aggregate memory exposes one named deterministic query per required family | unit | `uv run pytest tests/agents/test_representation_memory.py -q` | ❌ Wave 0 |
| REPR-08 | Blocked path, search frontier, task allocation, stale/conflict, and ablation scenarios pass | scenario | `uv run pytest tests/evaluation/test_representation_scenarios.py -q` | ❌ Wave 0 |

### Sampling Rate
- **Per task commit:** `uv run pytest tests/agents tests/evaluation -q` [VERIFIED: local command]
- **Per wave merge:** `uv run pytest -q` [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- **Phase gate:** Full suite green before `/gsd:verify-work`. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]

### Wave 0 Gaps
- [ ] `tests/agents/test_representation_memory.py` — covers REPR-01, REPR-03, REPR-04, REPR-05, REPR-06, REPR-07. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md]
- [ ] `tests/agents/test_representation_claims.py` — covers REPR-02. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md]
- [ ] `tests/evaluation/test_representation_scenarios.py` — covers REPR-08 and D-15 through D-20. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]
- [ ] `src/mosaic/agents/memory.py` — implementation module for Phase 7 contracts. [ASSUMED]

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|------------------|
| V2 Authentication | no | No auth/session/user identity feature in Phase 7; source robot/operator IDs are representation metadata, not authentication. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md] |
| V3 Session Management | no | No sessions or web runtime. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] |
| V4 Access Control | no | No service/API authorization boundary in Phase 7. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] |
| V5 Input Validation | yes | Validate every public dataclass invariant: nonblank IDs, finite confidences in `[0, 1]`, positive bounds, valid time windows, valid cell coordinates/resolution. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md] [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] |
| V6 Cryptography | no | No cryptographic feature or secret handling in Phase 7. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md] |

### Known Threat Patterns for provider-free typed memory contracts

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Unbounded result amplification from large in-memory state | Denial of Service | Require `max_results`/`max_items`, enforce positive bounds, and set `truncated` metadata. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] |
| Misleading evidence dereference or URI execution | Tampering / Information Disclosure | Treat evidence refs as opaque strings and do not load payloads by default. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] |
| Silent conflict suppression | Tampering / Repudiation | Keep conflicting claims visible with explicit status and conflict links. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] |
| Dependency supply-chain expansion | Elevation of Privilege | Add no new runtime dependencies; use stdlib and existing pytest dev tooling. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/pyproject.toml] |

## Sources

### Primary (HIGH confidence)
- `/home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md` — locked Phase 7 decisions, deferred scope, code context, scenario requirements. [VERIFIED]
- `/home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md` — REPR-01 through REPR-08 requirement text. [VERIFIED]
- `/home/prannayag/pragnition/robotics/mosaic/CLAUDE.md` — project constraints, style, module, testing, and boundary directives. [VERIFIED]
- `/home/prannayag/pragnition/robotics/mosaic/src/mosaic/agents/queries.py` — existing agent query/result patterns. [VERIFIED]
- `/home/prannayag/pragnition/robotics/mosaic/src/mosaic/agents/posteriors.py` — existing bounded posterior view. [VERIFIED]
- `/home/prannayag/pragnition/robotics/mosaic/src/mosaic/core/frames.py` — `Timestamp` and `FrameId` semantics. [VERIFIED]
- `/home/prannayag/pragnition/robotics/mosaic/src/mosaic/evaluation/scenarios.py` and `/home/prannayag/pragnition/robotics/mosaic/src/mosaic/evaluation/runner.py` — deterministic scenario/artifact patterns. [VERIFIED]
- Python dataclasses docs — frozen and slots semantics. [CITED: https://docs.python.org/3.14/library/dataclasses.html]
- Python enum docs — `StrEnum` semantics. [CITED: https://docs.python.org/3.14/library/enum.html#enum.StrEnum]
- pytest usage docs — test invocation and target selection. [CITED: https://docs.pytest.org/en/stable/how-to/invoke.html]

### Secondary (MEDIUM confidence)
- `/home/prannayag/pragnition/robotics/mosaic/.planning/references/superpowers/specs/2026-05-18-agent-friendly-representation-design.md` — project-internal design input for layered belief graph and memory/tool families. [VERIFIED]
- `/home/prannayag/pragnition/robotics/mosaic/.planning/references/arna/arna-2506-17462-replication.md` — project-internal ARNA evidence summary and artifact limitations. [VERIFIED]
- arXiv abstract for ARNA — confirms library of perception, reasoning, and navigation tools but not detailed ablations on abstract page. [CITED: https://arxiv.org/abs/2506.17462]

### Tertiary (LOW confidence)
- Assumptions in the Assumptions Log about developer tendencies and module granularity. [ASSUMED]

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — no new runtime deps; stdlib/Python/pytest facts verified from code, local commands, and official docs. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/pyproject.toml] [CITED: https://docs.python.org/3.14/library/dataclasses.html]
- Architecture: HIGH — locked Phase 7 decisions define aggregate memory, five families, named methods, immutable updates, and scenario anchors. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md]
- Pitfalls: MEDIUM — critical pitfalls are derived from locked constraints; some warning-sign explanations are assumed. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/07-representation-memories-and-tools/07-CONTEXT.md] [ASSUMED]
- Validation: HIGH — pytest config and targeted command were verified locally; new Phase 7 tests are Wave 0 gaps. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/pyproject.toml] [VERIFIED: local command]

**Research date:** 2026-05-21
**Valid until:** 2026-06-20 for stdlib/project architecture; re-check pytest/uv versions before package/tooling changes. [ASSUMED]
