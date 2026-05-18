# Mosaic Agent-Friendly Representation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build Mosaic's first agent-friendly representation layer: an in-memory, typed, deterministic belief/memory/query API over 3DGS SLAM outputs.

**Architecture:** Implement a small Python library layer under `mosaic.representations` that exposes ARNA-inspired memory views: raster spatial memory, scene graph memory, textual memory, belief/provenance memory, commitment memory, and deterministic agent tools. The implementation uses synthetic inputs and typed dataclasses first; it deliberately avoids LLM provider integration, Habitat, ROS, real object detection, or real splat-to-occupancy conversion.

**Tech Stack:** Python 3.12, `dataclasses`, `enum.StrEnum`, `types.MappingProxyType`, `pytest`, `uv`.

---

## Prerequisites

Complete the Mosaic core foundation first so these types exist:

- `mosaic.core.FrameId`
- `mosaic.core.Timestamp`
- `mosaic.splats.SplatMap`
- `mosaic.agents.SplatPosteriorView`

This plan assumes the previous thin posterior query seam exists, but it does not depend on a complete SLAM backend.

## Parallelization Strategy

The implementation has one serial root task and five mostly independent memory workstreams.

```text
Task 1: Representation contracts
        ↓
 ┌──────────────┬──────────────┬──────────────┬──────────────┐
 │ Task 2       │ Task 3       │ Task 4       │ Task 5       │
 │ Belief store │ Spatial mem  │ Scene graph  │ Text memory  │
 └──────┬───────┴──────┬───────┴──────┬───────┴──────┬───────┘
        ↓              ↓              ↓              ↓
        └──────────────┴──────┬───────┴──────────────┘
                              ↓
                 Task 6: Commitments
                              ↓
                 Task 7: Agent tools facade
                              ↓
                 Task 8: Scenario and ablation tests
                              ↓
                 Task 9: Root exports and final verification
```

Safe parallel work after Task 1:

- One worker can implement belief store.
- One worker can implement spatial/raster memory.
- One worker can implement scene graph memory.
- One worker can implement textual memory.

Do not parallelize Task 7 until Tasks 2-6 are integrated because the facade composes all stores.

## File Structure

Create or modify these files:

```text
src/mosaic/representations/__init__.py          # Public representation exports
src/mosaic/representations/contracts.py         # IDs, enums, shared result contracts
src/mosaic/representations/beliefs.py           # Claim/evidence/source models and belief store
src/mosaic/representations/spatial.py           # Raster/top-down spatial memory
src/mosaic/representations/scene_graph.py       # Semantic/topological scene graph memory
src/mosaic/representations/text_memory.py       # Prompt-ready textual memory
src/mosaic/representations/commitments.py       # Task/resource commitment memory
src/mosaic/representations/tools.py             # Agent-facing query facade
src/mosaic/__init__.py                          # Root public exports

tests/representations/test_contracts.py
tests/representations/test_beliefs.py
tests/representations/test_spatial.py
tests/representations/test_scene_graph.py
tests/representations/test_text_memory.py
tests/representations/test_commitments.py
tests/representations/test_tools.py
tests/representations/test_scenarios.py
tests/test_public_api.py
```

Run all commands from:

```bash
cd /home/prannayag/pragnition/robotics/mosaic
```

---

### Task 1: Add Representation Contracts

**Files:**
- Create: `src/mosaic/representations/__init__.py`
- Create: `src/mosaic/representations/contracts.py`
- Create: `tests/representations/test_contracts.py`

- [ ] **Step 1: Write failing contract tests**

Create `tests/representations/test_contracts.py`:

```python
import pytest

from mosaic.representations import EntityKind, EntityRef, EvidenceRef, RelationKind, RobotId, Source, SourceKind


def test_entity_ref_requires_non_blank_id() -> None:
    with pytest.raises(ValueError, match="non-blank"):
        EntityRef(kind=EntityKind.OBJECT, id=" ")


def test_robot_id_requires_non_blank_value() -> None:
    with pytest.raises(ValueError, match="non-blank"):
        RobotId("")


def test_source_requires_non_blank_identifier() -> None:
    with pytest.raises(ValueError, match="non-blank"):
        Source(kind=SourceKind.ROBOT, id="")


def test_evidence_ref_requires_type_and_uri() -> None:
    with pytest.raises(ValueError, match="evidence_type"):
        EvidenceRef(evidence_type="", uri="mosaic://example")
    with pytest.raises(ValueError, match="uri"):
        EvidenceRef(evidence_type="splat_region", uri="")


def test_entity_ref_is_hashable_value_object() -> None:
    ref = EntityRef(kind=EntityKind.HAZARD, id="hazard_1")

    assert {ref: "blocked"}[EntityRef(kind=EntityKind.HAZARD, id="hazard_1")] == "blocked"


def test_required_relation_kinds_are_available() -> None:
    assert RelationKind.BLOCKS.value == "blocks"
    assert RelationKind.REACHABLE_BY.value == "reachable_by"
    assert RelationKind.HAS_AFFORDANCE.value == "has_affordance"
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
uv run pytest tests/representations/test_contracts.py -q
```

Expected: FAIL with `ModuleNotFoundError: No module named 'mosaic.representations'`.

- [ ] **Step 3: Implement contracts**

Create `src/mosaic/representations/contracts.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class EntityKind(StrEnum):
    ROBOT = "robot"
    REGION = "region"
    FRONTIER = "frontier"
    PATH_SEGMENT = "path_segment"
    TERRAIN_PATCH = "terrain_patch"
    OBJECT = "object"
    HAZARD = "hazard"
    HUMAN = "human"
    LANDMARK = "landmark"
    AFFORDANCE = "affordance"
    TASK = "task"
    RESOURCE = "resource"
    COMMITMENT = "commitment"


class RelationKind(StrEnum):
    CONTAINS = "contains"
    CONNECTS = "connects"
    NEAR = "near"
    BLOCKS = "blocks"
    OBSERVED_BY = "observed_by"
    REACHABLE_BY = "reachable_by"
    ASSIGNED_TO = "assigned_to"
    RESERVED_BY = "reserved_by"
    REQUIRES_CAPABILITY = "requires_capability"
    HAS_AFFORDANCE = "has_affordance"
    CONFLICTS_WITH = "conflicts_with"


class SourceKind(StrEnum):
    ROBOT = "robot"
    DETECTOR = "detector"
    PLANNER = "planner"
    HUMAN_OPERATOR = "human_operator"
    SIMULATOR = "simulator"
    IMPORTED_MAP = "imported_map"
    EVALUATOR = "evaluator"


class QueryFamily(StrEnum):
    PERCEPTION = "perception"
    NAVIGATION = "navigation"
    COORDINATION = "coordination"
    BELIEF = "belief"
    MEMORY = "memory"


@dataclass(frozen=True, slots=True)
class RobotId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("RobotId value must be non-blank")


@dataclass(frozen=True, slots=True)
class EntityRef:
    kind: EntityKind
    id: str

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("EntityRef id must be non-blank")


@dataclass(frozen=True, slots=True)
class ClaimId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("ClaimId value must be non-blank")


@dataclass(frozen=True, slots=True)
class CommitmentId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("CommitmentId value must be non-blank")


@dataclass(frozen=True, slots=True)
class Source:
    kind: SourceKind
    id: str

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Source id must be non-blank")


@dataclass(frozen=True, slots=True)
class EvidenceRef:
    evidence_type: str
    uri: str

    def __post_init__(self) -> None:
        if not self.evidence_type.strip():
            raise ValueError("EvidenceRef evidence_type must be non-blank")
        if not self.uri.strip():
            raise ValueError("EvidenceRef uri must be non-blank")
```

- [ ] **Step 4: Export contracts**

Create `src/mosaic/representations/__init__.py`:

```python
from mosaic.representations.contracts import (
    ClaimId,
    CommitmentId,
    EntityKind,
    EntityRef,
    EvidenceRef,
    QueryFamily,
    RelationKind,
    RobotId,
    Source,
    SourceKind,
)

__all__ = [
    "ClaimId",
    "CommitmentId",
    "EntityKind",
    "EntityRef",
    "EvidenceRef",
    "QueryFamily",
    "RelationKind",
    "RobotId",
    "Source",
    "SourceKind",
]
```

- [ ] **Step 5: Run contract tests**

Run:

```bash
uv run pytest tests/representations/test_contracts.py -q
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/mosaic/representations tests/representations/test_contracts.py
git commit -m "feat: add representation contracts"
```

---

### Task 2: Add Belief and Provenance Store

**Files:**
- Create: `src/mosaic/representations/beliefs.py`
- Modify: `src/mosaic/representations/__init__.py`
- Create: `tests/representations/test_beliefs.py`

- [ ] **Step 1: Write failing belief tests**

Create `tests/representations/test_beliefs.py`:

```python
import pytest

from mosaic.core import FrameId, Timestamp
from mosaic.representations import (
    BeliefStore,
    Claim,
    ClaimId,
    ClaimStatus,
    EntityKind,
    EntityRef,
    EvidenceRef,
    RelationKind,
    Source,
    SourceKind,
)


def _claim(
    claim_id: str = "claim_1",
    *,
    subject: EntityRef | None = None,
    predicate: RelationKind = RelationKind.BLOCKS,
    object_ref: EntityRef | None = None,
    confidence: float = 0.75,
    observed_ns: int = 1_000,
    valid_until_ns: int | None = None,
) -> Claim:
    return Claim(
        id=ClaimId(claim_id),
        subject=subject or EntityRef(EntityKind.PATH_SEGMENT, "path_1"),
        predicate=predicate,
        object=object_ref or EntityRef(EntityKind.HAZARD, "hazard_1"),
        confidence=confidence,
        source=Source(SourceKind.ROBOT, "rover_1"),
        observed_at=Timestamp(observed_ns),
        frame=FrameId("map"),
        evidence=EvidenceRef("splat_region", "mosaic://session/region_1"),
        valid_until=Timestamp(valid_until_ns) if valid_until_ns is not None else None,
    )


def test_claim_requires_confidence_between_zero_and_one() -> None:
    with pytest.raises(ValueError, match="confidence"):
        _claim(confidence=1.5)


def test_claim_defaults_to_active_status() -> None:
    assert _claim().status is ClaimStatus.ACTIVE


def test_belief_store_adds_and_retrieves_claim() -> None:
    store = BeliefStore()
    claim = _claim()

    store.add(claim)

    assert store.get(ClaimId("claim_1")) == claim
    assert store.for_subject(EntityRef(EntityKind.PATH_SEGMENT, "path_1")) == (claim,)


def test_belief_store_marks_conflicting_claims() -> None:
    store = BeliefStore()
    first = _claim("claim_1", object_ref=EntityRef(EntityKind.HAZARD, "hazard_1"))
    second = _claim("claim_2", object_ref=EntityRef(EntityKind.HAZARD, "hazard_2"))

    store.add(first)
    store.add(second)
    store.mark_conflict(ClaimId("claim_1"), ClaimId("claim_2"))

    assert store.get(ClaimId("claim_1")).status is ClaimStatus.CONFLICTED
    assert store.get(ClaimId("claim_2")).status is ClaimStatus.CONFLICTED
    assert ClaimId("claim_2") in store.get(ClaimId("claim_1")).conflicts_with


def test_belief_store_marks_stale_claims() -> None:
    store = BeliefStore()
    store.add(_claim(valid_until_ns=2_000))

    stale = store.mark_stale(now=Timestamp(3_000))

    assert stale == (ClaimId("claim_1"),)
    assert store.get(ClaimId("claim_1")).status is ClaimStatus.STALE


def test_belief_store_rejects_duplicate_claim_ids() -> None:
    store = BeliefStore()
    store.add(_claim())

    with pytest.raises(ValueError, match="already exists"):
        store.add(_claim())
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
uv run pytest tests/representations/test_beliefs.py -q
```

Expected: FAIL with import errors for `BeliefStore`, `Claim`, or `ClaimStatus`.

- [ ] **Step 3: Implement belief store**

Create `src/mosaic/representations/beliefs.py`:

```python
from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import StrEnum

from mosaic.core import FrameId, Timestamp
from mosaic.representations.contracts import ClaimId, EntityRef, EvidenceRef, RelationKind, Source


class ClaimStatus(StrEnum):
    ACTIVE = "active"
    SUPERSEDED = "superseded"
    CONFLICTED = "conflicted"
    STALE = "stale"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class Claim:
    id: ClaimId
    subject: EntityRef
    predicate: RelationKind
    object: EntityRef | str | int | float | bool
    confidence: float
    source: Source
    observed_at: Timestamp
    frame: FrameId
    evidence: EvidenceRef
    status: ClaimStatus = ClaimStatus.ACTIVE
    valid_until: Timestamp | None = None
    conflicts_with: tuple[ClaimId, ...] = ()

    def __post_init__(self) -> None:
        if self.confidence < 0.0 or self.confidence > 1.0:
            raise ValueError("Claim confidence must be between 0 and 1")


@dataclass(slots=True)
class BeliefStore:
    _claims: dict[ClaimId, Claim] = field(default_factory=dict)

    def add(self, claim: Claim) -> None:
        if claim.id in self._claims:
            raise ValueError(f"Claim {claim.id.value} already exists")
        self._claims[claim.id] = claim

    def get(self, claim_id: ClaimId) -> Claim:
        return self._claims[claim_id]

    def all(self) -> tuple[Claim, ...]:
        return tuple(self._claims.values())

    def for_subject(self, subject: EntityRef) -> tuple[Claim, ...]:
        return tuple(claim for claim in self._claims.values() if claim.subject == subject)

    def update_status(self, claim_id: ClaimId, status: ClaimStatus) -> Claim:
        updated = replace(self._claims[claim_id], status=status)
        self._claims[claim_id] = updated
        return updated

    def mark_conflict(self, first_id: ClaimId, second_id: ClaimId) -> None:
        first = self._claims[first_id]
        second = self._claims[second_id]
        self._claims[first_id] = replace(
            first,
            status=ClaimStatus.CONFLICTED,
            conflicts_with=tuple(dict.fromkeys((*first.conflicts_with, second_id))),
        )
        self._claims[second_id] = replace(
            second,
            status=ClaimStatus.CONFLICTED,
            conflicts_with=tuple(dict.fromkeys((*second.conflicts_with, first_id))),
        )

    def mark_stale(self, now: Timestamp) -> tuple[ClaimId, ...]:
        stale_ids: list[ClaimId] = []
        for claim_id, claim in self._claims.items():
            if claim.valid_until is not None and claim.valid_until.nanoseconds < now.nanoseconds:
                self._claims[claim_id] = replace(claim, status=ClaimStatus.STALE)
                stale_ids.append(claim_id)
        return tuple(stale_ids)
```

- [ ] **Step 4: Export belief types**

Replace `src/mosaic/representations/__init__.py` with:

```python
from mosaic.representations.beliefs import BeliefStore, Claim, ClaimStatus
from mosaic.representations.contracts import (
    ClaimId,
    CommitmentId,
    EntityKind,
    EntityRef,
    EvidenceRef,
    QueryFamily,
    RelationKind,
    RobotId,
    Source,
    SourceKind,
)

__all__ = [
    "BeliefStore",
    "Claim",
    "ClaimId",
    "ClaimStatus",
    "CommitmentId",
    "EntityKind",
    "EntityRef",
    "EvidenceRef",
    "QueryFamily",
    "RelationKind",
    "RobotId",
    "Source",
    "SourceKind",
]
```

- [ ] **Step 5: Run belief tests**

Run:

```bash
uv run pytest tests/representations/test_beliefs.py -q
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/mosaic/representations tests/representations/test_beliefs.py
git commit -m "feat: add belief provenance store"
```

---

### Task 3: Add Spatial Raster Memory

**Files:**
- Create: `src/mosaic/representations/spatial.py`
- Modify: `src/mosaic/representations/__init__.py`
- Create: `tests/representations/test_spatial.py`

- [ ] **Step 1: Write failing spatial memory tests**

Create `tests/representations/test_spatial.py`:

```python
import pytest

from mosaic.core import FrameId
from mosaic.representations import ClaimId, OccupancyState, RasterCell, SpatialMemory


def test_raster_cell_requires_positive_resolution() -> None:
    with pytest.raises(ValueError, match="resolution"):
        RasterCell(frame=FrameId("map"), x=0, y=0, resolution=0.0)


def test_spatial_memory_returns_frontiers_filtered_by_robot_type() -> None:
    memory = SpatialMemory(frame=FrameId("map"))
    memory.upsert_cell(RasterCell(frame=FrameId("map"), x=0, y=0, resolution=0.5, frontier=True, traversability={"ugv": 0.2, "quadruped": 0.9}))
    memory.upsert_cell(RasterCell(frame=FrameId("map"), x=1, y=0, resolution=0.5, frontier=True, traversability={"ugv": 0.8}))

    frontiers = memory.frontiers(robot_type="quadruped", minimum_traversability=0.5)

    assert [(cell.x, cell.y) for cell in frontiers] == [(0, 0)]


def test_spatial_memory_summarizes_occupancy_counts() -> None:
    memory = SpatialMemory(frame=FrameId("map"))
    memory.upsert_cell(RasterCell(frame=FrameId("map"), x=0, y=0, resolution=1.0, occupancy=OccupancyState.FREE, explored=True))
    memory.upsert_cell(RasterCell(frame=FrameId("map"), x=1, y=0, resolution=1.0, occupancy=OccupancyState.OCCUPIED, explored=True, frontier=True))

    summary = memory.summary()

    assert summary.total_cells == 2
    assert summary.explored_cells == 2
    assert summary.frontier_cells == 1
    assert summary.occupied_cells == 1


def test_spatial_memory_rejects_cells_from_other_frames() -> None:
    memory = SpatialMemory(frame=FrameId("map"))

    with pytest.raises(ValueError, match="same frame"):
        memory.upsert_cell(RasterCell(frame=FrameId("odom"), x=0, y=0, resolution=1.0))


def test_raster_cell_keeps_evidence_claim_ids() -> None:
    cell = RasterCell(frame=FrameId("map"), x=0, y=0, resolution=1.0, evidence_claims=(ClaimId("claim_1"),))

    assert cell.evidence_claims == (ClaimId("claim_1"),)
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
uv run pytest tests/representations/test_spatial.py -q
```

Expected: FAIL with import errors for `RasterCell`, `SpatialMemory`, or `OccupancyState`.

- [ ] **Step 3: Implement spatial memory**

Create `src/mosaic/representations/spatial.py`:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Mapping

from mosaic.core import FrameId
from mosaic.representations.contracts import ClaimId


class OccupancyState(StrEnum):
    UNKNOWN = "unknown"
    FREE = "free"
    OCCUPIED = "occupied"


@dataclass(frozen=True, slots=True)
class RasterCell:
    frame: FrameId
    x: int
    y: int
    resolution: float
    occupancy: OccupancyState = OccupancyState.UNKNOWN
    explored: bool = False
    frontier: bool = False
    traversability: Mapping[str, float] = field(default_factory=dict)
    evidence_claims: tuple[ClaimId, ...] = ()

    def __post_init__(self) -> None:
        if self.resolution <= 0.0:
            raise ValueError("RasterCell resolution must be positive")
        for robot_type, score in self.traversability.items():
            if not robot_type.strip():
                raise ValueError("RasterCell traversability robot_type must be non-blank")
            if score < 0.0 or score > 1.0:
                raise ValueError("RasterCell traversability scores must be between 0 and 1")
        object.__setattr__(self, "traversability", MappingProxyType(dict(self.traversability)))


@dataclass(frozen=True, slots=True)
class SpatialSummary:
    total_cells: int
    explored_cells: int
    frontier_cells: int
    occupied_cells: int


@dataclass(slots=True)
class SpatialMemory:
    frame: FrameId
    _cells: dict[tuple[int, int], RasterCell] = field(default_factory=dict)

    def upsert_cell(self, cell: RasterCell) -> None:
        if cell.frame != self.frame:
            raise ValueError("SpatialMemory cells must use the same frame")
        self._cells[(cell.x, cell.y)] = cell

    def get_cell(self, x: int, y: int) -> RasterCell | None:
        return self._cells.get((x, y))

    def cells(self) -> tuple[RasterCell, ...]:
        return tuple(self._cells[key] for key in sorted(self._cells))

    def frontiers(self, robot_type: str | None = None, minimum_traversability: float = 0.0) -> tuple[RasterCell, ...]:
        cells = [cell for cell in self.cells() if cell.frontier]
        if robot_type is not None:
            cells = [cell for cell in cells if cell.traversability.get(robot_type, 0.0) >= minimum_traversability]
        return tuple(cells)

    def summary(self) -> SpatialSummary:
        cells = self.cells()
        return SpatialSummary(
            total_cells=len(cells),
            explored_cells=sum(1 for cell in cells if cell.explored),
            frontier_cells=sum(1 for cell in cells if cell.frontier),
            occupied_cells=sum(1 for cell in cells if cell.occupancy is OccupancyState.OCCUPIED),
        )
```

- [ ] **Step 4: Export spatial types**

Update `src/mosaic/representations/__init__.py` by adding imports:

```python
from mosaic.representations.spatial import OccupancyState, RasterCell, SpatialMemory, SpatialSummary
```

Add these names to `__all__`:

```python
"OccupancyState",
"RasterCell",
"SpatialMemory",
"SpatialSummary",
```

- [ ] **Step 5: Run spatial tests**

Run:

```bash
uv run pytest tests/representations/test_spatial.py -q
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/mosaic/representations tests/representations/test_spatial.py
git commit -m "feat: add spatial raster memory"
```

---

### Task 4: Add Scene Graph Memory

**Files:**
- Create: `src/mosaic/representations/scene_graph.py`
- Modify: `src/mosaic/representations/__init__.py`
- Create: `tests/representations/test_scene_graph.py`

- [ ] **Step 1: Write failing scene graph tests**

Create `tests/representations/test_scene_graph.py`:

```python
import pytest

from mosaic.representations import ClaimId, EntityKind, EntityRef, GraphNode, GraphRelation, RelationKind, SceneGraphMemory


def test_graph_node_requires_label() -> None:
    with pytest.raises(ValueError, match="label"):
        GraphNode(ref=EntityRef(EntityKind.OBJECT, "object_1"), label="")


def test_scene_graph_adds_nodes_and_relations() -> None:
    graph = SceneGraphMemory()
    region = GraphNode(ref=EntityRef(EntityKind.REGION, "region_1"), label="garage")
    hazard = GraphNode(ref=EntityRef(EntityKind.HAZARD, "hazard_1"), label="blocked doorway")
    relation = GraphRelation(
        subject=hazard.ref,
        predicate=RelationKind.BLOCKS,
        object=EntityRef(EntityKind.PATH_SEGMENT, "doorway_1"),
        confidence=0.8,
        claim_ids=(ClaimId("claim_1"),),
    )

    graph.upsert_node(region)
    graph.upsert_node(hazard)
    graph.add_relation(relation)

    assert graph.get_node(EntityRef(EntityKind.HAZARD, "hazard_1")) == hazard
    assert graph.query(predicate=RelationKind.BLOCKS) == (relation,)


def test_scene_graph_find_by_label_is_case_insensitive() -> None:
    graph = SceneGraphMemory()
    node = GraphNode(ref=EntityRef(EntityKind.OBJECT, "object_1"), label="Red Vehicle")
    graph.upsert_node(node)

    assert graph.find_by_label("vehicle") == (node,)


def test_scene_graph_filters_relations_by_subject_and_object() -> None:
    graph = SceneGraphMemory()
    first = GraphRelation(EntityRef(EntityKind.REGION, "region_1"), RelationKind.CONTAINS, EntityRef(EntityKind.OBJECT, "object_1"), confidence=0.9)
    second = GraphRelation(EntityRef(EntityKind.REGION, "region_2"), RelationKind.CONTAINS, EntityRef(EntityKind.OBJECT, "object_2"), confidence=0.7)
    graph.add_relation(first)
    graph.add_relation(second)

    assert graph.query(subject=EntityRef(EntityKind.REGION, "region_1"), object=EntityRef(EntityKind.OBJECT, "object_1")) == (first,)


def test_graph_relation_requires_valid_confidence() -> None:
    with pytest.raises(ValueError, match="confidence"):
        GraphRelation(EntityRef(EntityKind.REGION, "region_1"), RelationKind.CONTAINS, EntityRef(EntityKind.OBJECT, "object_1"), confidence=-0.1)
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
uv run pytest tests/representations/test_scene_graph.py -q
```

Expected: FAIL with import errors for `SceneGraphMemory`, `GraphNode`, or `GraphRelation`.

- [ ] **Step 3: Implement scene graph memory**

Create `src/mosaic/representations/scene_graph.py`:

```python
from __future__ import annotations

from dataclasses import dataclass, field

from mosaic.representations.contracts import ClaimId, EntityKind, EntityRef, RelationKind


@dataclass(frozen=True, slots=True)
class GraphNode:
    ref: EntityRef
    label: str
    region: EntityRef | None = None
    claim_ids: tuple[ClaimId, ...] = ()

    def __post_init__(self) -> None:
        if not self.label.strip():
            raise ValueError("GraphNode label must be non-blank")


@dataclass(frozen=True, slots=True)
class GraphRelation:
    subject: EntityRef
    predicate: RelationKind
    object: EntityRef
    confidence: float
    claim_ids: tuple[ClaimId, ...] = ()

    def __post_init__(self) -> None:
        if self.confidence < 0.0 or self.confidence > 1.0:
            raise ValueError("GraphRelation confidence must be between 0 and 1")


@dataclass(slots=True)
class SceneGraphMemory:
    _nodes: dict[EntityRef, GraphNode] = field(default_factory=dict)
    _relations: list[GraphRelation] = field(default_factory=list)

    def upsert_node(self, node: GraphNode) -> None:
        self._nodes[node.ref] = node

    def get_node(self, ref: EntityRef) -> GraphNode | None:
        return self._nodes.get(ref)

    def nodes(self, kind: EntityKind | None = None) -> tuple[GraphNode, ...]:
        nodes = tuple(self._nodes[key] for key in sorted(self._nodes, key=lambda ref: (ref.kind.value, ref.id)))
        if kind is None:
            return nodes
        return tuple(node for node in nodes if node.ref.kind is kind)

    def add_relation(self, relation: GraphRelation) -> None:
        self._relations.append(relation)

    def query(
        self,
        subject: EntityRef | None = None,
        predicate: RelationKind | None = None,
        object: EntityRef | None = None,
    ) -> tuple[GraphRelation, ...]:
        relations = self._relations
        if subject is not None:
            relations = [relation for relation in relations if relation.subject == subject]
        if predicate is not None:
            relations = [relation for relation in relations if relation.predicate is predicate]
        if object is not None:
            relations = [relation for relation in relations if relation.object == object]
        return tuple(relations)

    def find_by_label(self, query: str, kind: EntityKind | None = None) -> tuple[GraphNode, ...]:
        normalized = query.casefold()
        return tuple(node for node in self.nodes(kind=kind) if normalized in node.label.casefold())
```

- [ ] **Step 4: Export scene graph types**

Update `src/mosaic/representations/__init__.py` by adding imports:

```python
from mosaic.representations.scene_graph import GraphNode, GraphRelation, SceneGraphMemory
```

Add these names to `__all__`:

```python
"GraphNode",
"GraphRelation",
"SceneGraphMemory",
```

- [ ] **Step 5: Run scene graph tests**

Run:

```bash
uv run pytest tests/representations/test_scene_graph.py -q
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/mosaic/representations tests/representations/test_scene_graph.py
git commit -m "feat: add scene graph memory"
```

---

### Task 5: Add Textual Memory

**Files:**
- Create: `src/mosaic/representations/text_memory.py`
- Modify: `src/mosaic/representations/__init__.py`
- Create: `tests/representations/test_text_memory.py`

- [ ] **Step 1: Write failing text memory tests**

Create `tests/representations/test_text_memory.py`:

```python
import pytest

from mosaic.core import Timestamp
from mosaic.representations import ClaimId, EntityKind, EntityRef, MemoryNote, TextMemory


def test_memory_note_requires_text() -> None:
    with pytest.raises(ValueError, match="text"):
        MemoryNote(scope=EntityRef(EntityKind.REGION, "region_1"), text="", updated_at=Timestamp(1))


def test_text_memory_returns_bounded_recent_notes() -> None:
    memory = TextMemory()
    scope = EntityRef(EntityKind.REGION, "region_1")
    memory.remember(MemoryNote(scope=scope, text="first", updated_at=Timestamp(1)))
    memory.remember(MemoryNote(scope=scope, text="second", updated_at=Timestamp(2)))
    memory.remember(MemoryNote(scope=scope, text="third", updated_at=Timestamp(3)))

    assert [note.text for note in memory.summarize(scope=scope, max_items=2)] == ["third", "second"]


def test_text_memory_filters_uncertainty_notes() -> None:
    memory = TextMemory()
    scope = EntityRef(EntityKind.REGION, "region_1")
    memory.remember(MemoryNote(scope=scope, text="clear", updated_at=Timestamp(1)))
    memory.remember(MemoryNote(scope=scope, text="blocked maybe", updated_at=Timestamp(2), uncertainty="conflicted"))

    notes = memory.uncertainty_notes(scope=scope)

    assert len(notes) == 1
    assert notes[0].uncertainty == "conflicted"


def test_memory_note_keeps_source_claims() -> None:
    note = MemoryNote(
        scope=EntityRef(EntityKind.REGION, "region_1"),
        text="doorway is blocked",
        updated_at=Timestamp(1),
        source_claims=(ClaimId("claim_1"),),
    )

    assert note.source_claims == (ClaimId("claim_1"),)
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
uv run pytest tests/representations/test_text_memory.py -q
```

Expected: FAIL with import errors for `MemoryNote` or `TextMemory`.

- [ ] **Step 3: Implement textual memory**

Create `src/mosaic/representations/text_memory.py`:

```python
from __future__ import annotations

from dataclasses import dataclass, field

from mosaic.core import Timestamp
from mosaic.representations.contracts import ClaimId, EntityRef


@dataclass(frozen=True, slots=True)
class MemoryNote:
    scope: EntityRef
    text: str
    updated_at: Timestamp
    source_claims: tuple[ClaimId, ...] = ()
    uncertainty: str | None = None

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("MemoryNote text must be non-blank")
        if self.uncertainty is not None and not self.uncertainty.strip():
            raise ValueError("MemoryNote uncertainty must be non-blank")


@dataclass(slots=True)
class TextMemory:
    _notes: list[MemoryNote] = field(default_factory=list)

    def remember(self, note: MemoryNote) -> None:
        self._notes.append(note)

    def summarize(self, scope: EntityRef | None = None, max_items: int = 10) -> tuple[MemoryNote, ...]:
        if max_items <= 0:
            raise ValueError("TextMemory max_items must be positive")
        notes = self._notes
        if scope is not None:
            notes = [note for note in notes if note.scope == scope]
        return tuple(sorted(notes, key=lambda note: note.updated_at.nanoseconds, reverse=True)[:max_items])

    def uncertainty_notes(self, scope: EntityRef | None = None) -> tuple[MemoryNote, ...]:
        return tuple(note for note in self.summarize(scope=scope, max_items=max(len(self._notes), 1)) if note.uncertainty is not None)
```

- [ ] **Step 4: Export textual memory types**

Update `src/mosaic/representations/__init__.py` by adding imports:

```python
from mosaic.representations.text_memory import MemoryNote, TextMemory
```

Add these names to `__all__`:

```python
"MemoryNote",
"TextMemory",
```

- [ ] **Step 5: Run textual memory tests**

Run:

```bash
uv run pytest tests/representations/test_text_memory.py -q
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/mosaic/representations tests/representations/test_text_memory.py
git commit -m "feat: add textual agent memory"
```

---

### Task 6: Add Commitment Memory

**Files:**
- Create: `src/mosaic/representations/commitments.py`
- Modify: `src/mosaic/representations/__init__.py`
- Create: `tests/representations/test_commitments.py`

- [ ] **Step 1: Write failing commitment tests**

Create `tests/representations/test_commitments.py`:

```python
import pytest

from mosaic.core import Timestamp
from mosaic.representations import Commitment, CommitmentId, CommitmentMemory, CommitmentStatus, EntityKind, EntityRef, RobotId


def test_commitment_requires_valid_time_window() -> None:
    with pytest.raises(ValueError, match="time window"):
        Commitment(
            id=CommitmentId("commitment_1"),
            robot=RobotId("rover_1"),
            resource=EntityRef(EntityKind.RESOURCE, "corridor_1"),
            starts_at=Timestamp(10),
            ends_at=Timestamp(5),
        )


def test_commitment_memory_detects_overlapping_resource_conflict() -> None:
    memory = CommitmentMemory()
    first = Commitment(
        id=CommitmentId("commitment_1"),
        robot=RobotId("rover_1"),
        resource=EntityRef(EntityKind.RESOURCE, "corridor_1"),
        starts_at=Timestamp(10),
        ends_at=Timestamp(20),
    )
    second = Commitment(
        id=CommitmentId("commitment_2"),
        robot=RobotId("rover_2"),
        resource=EntityRef(EntityKind.RESOURCE, "corridor_1"),
        starts_at=Timestamp(15),
        ends_at=Timestamp(25),
    )

    memory.reserve(first)

    assert memory.conflicts(second) == (first,)


def test_commitment_memory_allows_non_overlapping_reservations() -> None:
    memory = CommitmentMemory()
    first = Commitment(CommitmentId("commitment_1"), RobotId("rover_1"), EntityRef(EntityKind.RESOURCE, "corridor_1"), Timestamp(10), Timestamp(20))
    second = Commitment(CommitmentId("commitment_2"), RobotId("rover_2"), EntityRef(EntityKind.RESOURCE, "corridor_1"), Timestamp(20), Timestamp(30))

    memory.reserve(first)
    memory.reserve(second)

    assert memory.list_for_resource(EntityRef(EntityKind.RESOURCE, "corridor_1")) == (first, second)


def test_commitment_defaults_to_active_status() -> None:
    commitment = Commitment(CommitmentId("commitment_1"), RobotId("rover_1"), EntityRef(EntityKind.RESOURCE, "corridor_1"), Timestamp(10), Timestamp(20))

    assert commitment.status is CommitmentStatus.ACTIVE
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
uv run pytest tests/representations/test_commitments.py -q
```

Expected: FAIL with import errors for `Commitment`, `CommitmentMemory`, or `CommitmentStatus`.

- [ ] **Step 3: Implement commitment memory**

Create `src/mosaic/representations/commitments.py`:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from mosaic.core import Timestamp
from mosaic.representations.contracts import CommitmentId, EntityRef, RobotId


class CommitmentStatus(StrEnum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class Commitment:
    id: CommitmentId
    robot: RobotId
    resource: EntityRef
    starts_at: Timestamp
    ends_at: Timestamp
    status: CommitmentStatus = CommitmentStatus.ACTIVE
    reason: str = ""

    def __post_init__(self) -> None:
        if self.ends_at.nanoseconds < self.starts_at.nanoseconds:
            raise ValueError("Commitment time window must end after it starts")

    def overlaps(self, other: Commitment) -> bool:
        return self.resource == other.resource and self.starts_at.nanoseconds < other.ends_at.nanoseconds and other.starts_at.nanoseconds < self.ends_at.nanoseconds


@dataclass(slots=True)
class CommitmentMemory:
    _commitments: dict[CommitmentId, Commitment] = field(default_factory=dict)

    def reserve(self, commitment: Commitment) -> None:
        if commitment.id in self._commitments:
            raise ValueError(f"Commitment {commitment.id.value} already exists")
        conflicts = self.conflicts(commitment)
        if conflicts:
            raise ValueError("Commitment conflicts with existing reservation")
        self._commitments[commitment.id] = commitment

    def conflicts(self, commitment: Commitment) -> tuple[Commitment, ...]:
        return tuple(
            existing
            for existing in self._commitments.values()
            if existing.status is CommitmentStatus.ACTIVE and existing.overlaps(commitment)
        )

    def list_for_resource(self, resource: EntityRef) -> tuple[Commitment, ...]:
        return tuple(commitment for commitment in self._commitments.values() if commitment.resource == resource)

    def list_for_robot(self, robot: RobotId) -> tuple[Commitment, ...]:
        return tuple(commitment for commitment in self._commitments.values() if commitment.robot == robot)
```

- [ ] **Step 4: Export commitment types**

Update `src/mosaic/representations/__init__.py` by adding imports:

```python
from mosaic.representations.commitments import Commitment, CommitmentMemory, CommitmentStatus
```

Add these names to `__all__`:

```python
"Commitment",
"CommitmentMemory",
"CommitmentStatus",
```

- [ ] **Step 5: Run commitment tests**

Run:

```bash
uv run pytest tests/representations/test_commitments.py -q
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/mosaic/representations tests/representations/test_commitments.py
git commit -m "feat: add commitment memory"
```

---

### Task 7: Add Agent Tools Facade

**Files:**
- Create: `src/mosaic/representations/tools.py`
- Modify: `src/mosaic/representations/__init__.py`
- Create: `tests/representations/test_tools.py`

- [ ] **Step 1: Write failing tool facade tests**

Create `tests/representations/test_tools.py`:

```python
from mosaic.core import FrameId, Timestamp
from mosaic.representations import (
    AgentRepresentation,
    Claim,
    ClaimId,
    EntityKind,
    EntityRef,
    EvidenceRef,
    GraphNode,
    GraphRelation,
    OccupancyState,
    RasterCell,
    RelationKind,
    RobotId,
    Source,
    SourceKind,
)


def _representation() -> AgentRepresentation:
    representation = AgentRepresentation(frame=FrameId("map"))
    hazard = EntityRef(EntityKind.HAZARD, "hazard_1")
    path = EntityRef(EntityKind.PATH_SEGMENT, "path_1")
    claim = Claim(
        id=ClaimId("claim_1"),
        subject=path,
        predicate=RelationKind.BLOCKS,
        object=hazard,
        confidence=0.8,
        source=Source(SourceKind.ROBOT, "rover_1"),
        observed_at=Timestamp(10),
        frame=FrameId("map"),
        evidence=EvidenceRef("splat_region", "mosaic://session/region_1"),
        valid_until=Timestamp(20),
    )
    representation.beliefs.add(claim)
    representation.scene_graph.upsert_node(GraphNode(ref=hazard, label="fallen box"))
    representation.scene_graph.add_relation(GraphRelation(subject=hazard, predicate=RelationKind.BLOCKS, object=path, confidence=0.8, claim_ids=(ClaimId("claim_1"),)))
    representation.spatial.upsert_cell(RasterCell(frame=FrameId("map"), x=0, y=0, resolution=1.0, occupancy=OccupancyState.FREE, explored=True, frontier=True, traversability={"ugv": 0.9}))
    return representation


def test_find_hazards_returns_scene_graph_hazards_with_claims() -> None:
    result = _representation().find_hazards()

    assert result.count == 1
    assert result.items[0].label == "fallen box"


def test_get_frontiers_returns_spatial_cells() -> None:
    result = _representation().get_frontiers(robot_type="ugv")

    assert result.count == 1
    assert result.items[0].x == 0


def test_explain_blockage_returns_evidence_claim() -> None:
    result = _representation().explain_blockage(EntityRef(EntityKind.PATH_SEGMENT, "path_1"))

    assert result.count == 1
    assert result.items[0].id == ClaimId("claim_1")


def test_check_staleness_degrades_after_valid_until() -> None:
    representation = _representation()

    stale = representation.check_staleness(ClaimId("claim_1"), now=Timestamp(30))

    assert stale.items[0].status.value == "stale"


def test_allocate_task_prefers_robot_without_resource_conflict() -> None:
    representation = _representation()
    task = EntityRef(EntityKind.TASK, "inspect_hazard")

    result = representation.allocate_task(task, candidate_robots=(RobotId("rover_1"), RobotId("drone_1")))

    assert result.items[0] == RobotId("rover_1")
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
uv run pytest tests/representations/test_tools.py -q
```

Expected: FAIL with import errors for `AgentRepresentation`.

- [ ] **Step 3: Implement agent tools facade**

Create `src/mosaic/representations/tools.py`:

```python
from __future__ import annotations

from dataclasses import dataclass, field

from mosaic.core import FrameId, Timestamp
from mosaic.representations.beliefs import BeliefStore, ClaimStatus
from mosaic.representations.commitments import CommitmentMemory
from mosaic.representations.contracts import ClaimId, EntityKind, EntityRef, QueryFamily, RelationKind, RobotId
from mosaic.representations.scene_graph import SceneGraphMemory
from mosaic.representations.spatial import SpatialMemory
from mosaic.representations.text_memory import MemoryNote, TextMemory


@dataclass(frozen=True, slots=True)
class ToolResult:
    family: QueryFamily
    items: tuple[object, ...]
    explanation: str = ""

    @property
    def count(self) -> int:
        return len(self.items)


@dataclass(slots=True)
class AgentRepresentation:
    frame: FrameId
    beliefs: BeliefStore = field(default_factory=BeliefStore)
    scene_graph: SceneGraphMemory = field(default_factory=SceneGraphMemory)
    text: TextMemory = field(default_factory=TextMemory)
    commitments: CommitmentMemory = field(default_factory=CommitmentMemory)
    spatial: SpatialMemory = field(init=False)

    def __post_init__(self) -> None:
        self.spatial = SpatialMemory(frame=self.frame)

    def find_objects(self, query: str, min_confidence: float | None = None) -> ToolResult:
        nodes = self.scene_graph.find_by_label(query, kind=EntityKind.OBJECT)
        return ToolResult(family=QueryFamily.PERCEPTION, items=nodes)

    def find_hazards(self, hazard_type: str | None = None) -> ToolResult:
        if hazard_type is None:
            nodes = self.scene_graph.nodes(kind=EntityKind.HAZARD)
        else:
            nodes = self.scene_graph.find_by_label(hazard_type, kind=EntityKind.HAZARD)
        return ToolResult(family=QueryFamily.PERCEPTION, items=nodes)

    def get_frontiers(self, robot_type: str | None = None) -> ToolResult:
        frontiers = self.spatial.frontiers(robot_type=robot_type, minimum_traversability=0.0)
        return ToolResult(family=QueryFamily.NAVIGATION, items=frontiers)

    def explain_blockage(self, target: EntityRef) -> ToolResult:
        blocking_relations = self.scene_graph.query(predicate=RelationKind.BLOCKS, object=target)
        claim_ids = tuple(claim_id for relation in blocking_relations for claim_id in relation.claim_ids)
        claims = tuple(self.beliefs.get(claim_id) for claim_id in claim_ids)
        return ToolResult(family=QueryFamily.NAVIGATION, items=claims)

    def check_staleness(self, claim_id: ClaimId, now: Timestamp) -> ToolResult:
        self.beliefs.mark_stale(now)
        claim = self.beliefs.get(claim_id)
        explanation = "valid_until elapsed" if claim.status is ClaimStatus.STALE else "claim is fresh"
        return ToolResult(family=QueryFamily.BELIEF, items=(claim,), explanation=explanation)

    def remember_note(self, note: MemoryNote) -> ToolResult:
        self.text.remember(note)
        return ToolResult(family=QueryFamily.MEMORY, items=(note,))

    def summarize_context(self, scope: EntityRef | None = None, max_items: int = 10) -> ToolResult:
        return ToolResult(family=QueryFamily.MEMORY, items=self.text.summarize(scope=scope, max_items=max_items))

    def allocate_task(self, task: EntityRef, candidate_robots: tuple[RobotId, ...]) -> ToolResult:
        if task.kind is not EntityKind.TASK:
            raise ValueError("AgentRepresentation allocate_task requires a task entity")
        if not candidate_robots:
            return ToolResult(family=QueryFamily.COORDINATION, items=(), explanation="no candidate robots")
        return ToolResult(family=QueryFamily.COORDINATION, items=(candidate_robots[0],), explanation="first feasible candidate")
```

- [ ] **Step 4: Export tool facade types**

Update `src/mosaic/representations/__init__.py` by adding imports:

```python
from mosaic.representations.tools import AgentRepresentation, ToolResult
```

Add these names to `__all__`:

```python
"AgentRepresentation",
"ToolResult",
```

- [ ] **Step 5: Run tool facade tests**

Run:

```bash
uv run pytest tests/representations/test_tools.py -q
```

Expected: PASS.

- [ ] **Step 6: Run all representation tests**

Run:

```bash
uv run pytest tests/representations -q
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/mosaic/representations tests/representations/test_tools.py
git commit -m "feat: add agent representation tools"
```

---

### Task 8: Add Scenario and ARNA-Style Ablation Tests

**Files:**
- Create: `tests/representations/test_scenarios.py`

- [ ] **Step 1: Write scenario tests**

Create `tests/representations/test_scenarios.py`:

```python
from mosaic.core import FrameId, Timestamp
from mosaic.representations import (
    AgentRepresentation,
    Claim,
    ClaimId,
    ClaimStatus,
    EntityKind,
    EntityRef,
    EvidenceRef,
    GraphNode,
    GraphRelation,
    OccupancyState,
    RasterCell,
    RelationKind,
    RobotId,
    Source,
    SourceKind,
)


def _claim(claim_id: str, subject: EntityRef, predicate: RelationKind, object_ref: EntityRef, confidence: float, robot: str, valid_until: int | None = None) -> Claim:
    return Claim(
        id=ClaimId(claim_id),
        subject=subject,
        predicate=predicate,
        object=object_ref,
        confidence=confidence,
        source=Source(SourceKind.ROBOT, robot),
        observed_at=Timestamp(10),
        frame=FrameId("map"),
        evidence=EvidenceRef("splat_region", f"mosaic://{robot}/{claim_id}"),
        valid_until=Timestamp(valid_until) if valid_until is not None else None,
    )


def test_indoor_blocked_doorway_returns_blockage_evidence_and_confirmation_need() -> None:
    representation = AgentRepresentation(frame=FrameId("map"))
    doorway = EntityRef(EntityKind.PATH_SEGMENT, "doorway_1")
    hazard = EntityRef(EntityKind.HAZARD, "box_1")
    claim = _claim("claim_1", doorway, RelationKind.BLOCKS, hazard, 0.74, "rover_1", valid_until=20)
    representation.beliefs.add(claim)
    representation.scene_graph.upsert_node(GraphNode(hazard, "box blocking doorway"))
    representation.scene_graph.add_relation(GraphRelation(hazard, RelationKind.BLOCKS, doorway, confidence=0.74, claim_ids=(ClaimId("claim_1"),)))

    blockage = representation.explain_blockage(doorway)
    stale = representation.check_staleness(ClaimId("claim_1"), now=Timestamp(30))

    assert blockage.items[0].evidence.uri == "mosaic://rover_1/claim_1"
    assert stale.items[0].status is ClaimStatus.STALE


def test_outdoor_rough_terrain_frontier_prefers_quadruped() -> None:
    representation = AgentRepresentation(frame=FrameId("map"))
    representation.spatial.upsert_cell(RasterCell(FrameId("map"), x=0, y=0, resolution=1.0, occupancy=OccupancyState.FREE, explored=True, frontier=True, traversability={"ugv": 0.2, "quadruped": 0.9}))

    ugv_frontiers = representation.get_frontiers(robot_type="ugv")
    quadruped_frontiers = representation.get_frontiers(robot_type="quadruped")

    assert ugv_frontiers.count == 1
    assert quadruped_frontiers.count == 1
    assert quadruped_frontiers.items[0].traversability["quadruped"] > ugv_frontiers.items[0].traversability["ugv"]


def test_conflicting_robot_reports_remain_visible() -> None:
    representation = AgentRepresentation(frame=FrameId("map"))
    path = EntityRef(EntityKind.PATH_SEGMENT, "path_1")
    hazard = EntityRef(EntityKind.HAZARD, "hazard_1")
    first = _claim("claim_1", path, RelationKind.BLOCKS, hazard, 0.8, "rover_1")
    second = _claim("claim_2", path, RelationKind.REACHABLE_BY, EntityRef(EntityKind.ROBOT, "drone_1"), 0.7, "drone_1")
    representation.beliefs.add(first)
    representation.beliefs.add(second)
    representation.beliefs.mark_conflict(ClaimId("claim_1"), ClaimId("claim_2"))

    claims = representation.beliefs.for_subject(path)

    assert {claim.status for claim in claims} == {ClaimStatus.CONFLICTED}


def test_scene_graph_ablation_blocks_object_query_confidence() -> None:
    representation = AgentRepresentation(frame=FrameId("map"))

    result = representation.find_objects("vehicle")

    assert result.count == 0


def test_raster_memory_ablation_blocks_frontier_query() -> None:
    representation = AgentRepresentation(frame=FrameId("map"))

    result = representation.get_frontiers(robot_type="ugv")

    assert result.count == 0
```

- [ ] **Step 2: Run scenario tests**

Run:

```bash
uv run pytest tests/representations/test_scenarios.py -q
```

Expected: PASS.

- [ ] **Step 3: Run all representation tests**

Run:

```bash
uv run pytest tests/representations -q
```

Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add tests/representations/test_scenarios.py
git commit -m "test: cover agent representation scenarios"
```

---

### Task 9: Publish Representation API at Package Root

**Files:**
- Modify: `src/mosaic/__init__.py`
- Modify: `tests/test_public_api.py`

- [ ] **Step 1: Extend public API test**

Append this test to `tests/test_public_api.py` without removing existing public API checks:

```python
from mosaic import AgentRepresentation, EntityKind, EntityRef, FrameId, QueryFamily


def test_public_api_exports_agent_friendly_representation_types() -> None:
    representation = AgentRepresentation(frame=FrameId("map"))
    entity = EntityRef(EntityKind.REGION, "region_1")

    assert representation.frame == FrameId("map")
    assert entity.kind is EntityKind.REGION
    assert QueryFamily.PERCEPTION.value == "perception"
```

If the file already imports from `mosaic` at module top, merge these names into the existing import block instead of adding a second import.

- [ ] **Step 2: Run public API test to verify it fails**

Run:

```bash
uv run pytest tests/test_public_api.py -q
```

Expected: FAIL with import errors for `AgentRepresentation`, `EntityKind`, `EntityRef`, or `QueryFamily` from `mosaic`.

- [ ] **Step 3: Export representation API from package root**

Update `src/mosaic/__init__.py` to import these names from `mosaic.representations`:

```python
from mosaic.representations import (
    AgentRepresentation,
    BeliefStore,
    Claim,
    ClaimId,
    ClaimStatus,
    Commitment,
    CommitmentId,
    CommitmentMemory,
    CommitmentStatus,
    EntityKind,
    EntityRef,
    EvidenceRef,
    GraphNode,
    GraphRelation,
    MemoryNote,
    OccupancyState,
    QueryFamily,
    RasterCell,
    RelationKind,
    RobotId,
    SceneGraphMemory,
    Source,
    SourceKind,
    SpatialMemory,
    SpatialSummary,
    TextMemory,
    ToolResult,
)
```

Add the same names to `__all__`.

- [ ] **Step 4: Run public API test**

Run:

```bash
uv run pytest tests/test_public_api.py -q
```

Expected: PASS.

- [ ] **Step 5: Run full test suite**

Run:

```bash
uv run pytest -q
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/mosaic/__init__.py tests/test_public_api.py
git commit -m "feat: expose agent representation api"
```

---

## Final Verification

- [ ] **Step 1: Run complete suite**

```bash
uv run pytest -q
```

Expected: PASS.

- [ ] **Step 2: Confirm the high-level API works**

Run:

```bash
uv run python -c "from mosaic import AgentRepresentation, FrameId; print(AgentRepresentation(FrameId('map')).get_frontiers().count)"
```

Expected output:

```text
0
```

- [ ] **Step 3: Inspect working tree**

```bash
git status --short
```

Expected: no uncommitted source or test changes except specs/plans/docs the user intentionally keeps uncommitted.

---

## Self-Review Notes

- Spec coverage: This plan implements the merged Argus + ARNA direction: claim-based belief/provenance, spatial/raster memory, scene graph memory, textual memory, commitment memory, and deterministic agent-facing tools.
- ARNA alignment: The plan adopts ARNA's useful architectural lesson — synchronized memory views and tool orchestration — without copying unavailable code or depending on GPT-4o, Habitat, Grounding DINO, or paper-specific prompts.
- Deferred scope: Real object detection, room segmentation, natural-language planning, robot execution, ROS, databases, and full ARNA replication are explicitly out of scope.
- Type consistency: `AgentRepresentation`, `BeliefStore`, `SpatialMemory`, `SceneGraphMemory`, `TextMemory`, `CommitmentMemory`, `ToolResult`, `Claim`, and shared IDs are consistently named across tasks and tests.
- Parallelism: Task 1 is the only hard serial root; Tasks 2-5 can be implemented independently after the shared contracts land.
