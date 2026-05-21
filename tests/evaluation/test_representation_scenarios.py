from mosaic.agents.memory import (
    CellState,
    Claim,
    ClaimId,
    ClaimStatus,
    Entity,
    EntityId,
    EntityKind,
    EvidenceId,
    EvidenceKind,
    EvidenceReference,
    MemoryNote,
    NoteId,
    QueryFamily,
    Commitment,
    CommitmentId,
    CommitmentStatus,
    Relation,
    RelationKind,
    RepresentationMemory,
    SourceId,
    SourceMetadata,
    SpatialCell,
)
from mosaic.core import FrameId, Timestamp


CREATED_AT = Timestamp(1_000_000_000)
OBSERVED_AT = Timestamp(2_000_000_000)
VALID_UNTIL = Timestamp(3_000_000_000)
EXPIRED_AT = Timestamp(4_000_000_000)


def test_blocked_path_scenario_preserves_conflicting_robot_reports() -> None:
    memory = _blocked_path_memory()

    conflicts = memory.inspect_belief(status=ClaimStatus.CONFLICTED, max_results=5)

    assert conflicts.total_matches == 2
    assert conflicts.truncated is False
    assert [row.claim_id for row in conflicts.items] == [
        ClaimId("claim-blocked-a"),
        ClaimId("claim-clear-b"),
    ]
    assert [row.confidence for row in conflicts.items] == [0.8, 0.7]
    assert [row.conflicts_with for row in conflicts.items] == [
        (ClaimId("claim-clear-b"),),
        (ClaimId("claim-blocked-a"),),
    ]
    assert {row.subject for row in conflicts.items} == {"edge:kitchen->hall"}
    assert {row.status for row in conflicts.items} == {ClaimStatus.CONFLICTED}


def test_blocked_path_navigation_query_explains_blockage_with_claim_ids() -> None:
    memory = _blocked_path_memory()

    result = memory.query_navigation_frontiers(max_results=1)

    assert result.total_matches == 1
    assert result.truncated is False
    assert len(result.items) == 1
    row = result.items[0]
    assert row.coordinate == (1, 2)
    assert row.state is CellState.BLOCKED
    assert row.traversability == 0.0
    assert row.status is ClaimStatus.CONFLICTED
    assert row.claim_ids == (ClaimId("claim-blocked-a"), ClaimId("claim-clear-b"))
    assert [evidence.evidence_id for evidence in row.evidence] == [
        EvidenceId("evidence-blocked-a"),
        EvidenceId("evidence-clear-b"),
    ]


def test_blocked_path_stale_transition_uses_supplied_timestamp() -> None:
    memory = RepresentationMemory.empty(frame=FrameId("map")).with_claim(
        _claim(
            claim_id=ClaimId("claim-blocked-expired"),
            source=_source(SourceId("robot-a"), QueryFamily.BELIEF_PROVENANCE),
            confidence=0.8,
            status=ClaimStatus.ACTIVE,
            valid_until=VALID_UNTIL,
            evidence=(
                _evidence(
                    EvidenceId("evidence-blocked-expired"),
                    uri="mosaic://scenario/blocked-path/expired",
                ),
            ),
        )
    )

    stale_memory = memory.mark_stale_claims(now=EXPIRED_AT)
    stale = stale_memory.inspect_belief(status=ClaimStatus.STALE, max_results=5)

    assert memory.inspect_belief(status=ClaimStatus.ACTIVE, max_results=5).total_matches == 1
    assert stale.total_matches == 1
    assert stale.truncated is False
    assert stale.items[0].claim_id == ClaimId("claim-blocked-expired")
    assert stale.items[0].status is ClaimStatus.STALE
    assert stale.items[0].evidence[0].evidence_id == EvidenceId("evidence-blocked-expired")


def test_search_frontier_scenario_stores_frontier_context_and_uncertainty() -> None:
    memory = _search_frontier_memory()

    perception = memory.find_perception_matches(kind=EntityKind.FRONTIER, max_results=5)
    context = memory.summarize_context(max_notes=5)

    assert perception.total_matches == 1
    assert perception.truncated is False
    assert perception.items[0].entity_id == EntityId("entity-frontier-north")
    assert perception.items[0].kind is EntityKind.FRONTIER
    assert perception.items[0].label == "north frontier"
    assert perception.items[0].status is ClaimStatus.ACTIVE
    assert perception.items[0].claim_ids == (ClaimId("claim-frontier-north"),)
    assert context.total_matches == 1
    assert context.truncated is False
    assert context.items[0].note_id == NoteId("note-unexplored-north")
    assert context.items[0].family is QueryFamily.MEMORY_CONTEXT
    assert context.items[0].claim_ids == (ClaimId("claim-frontier-north"),)
    assert "unexplored" in context.items[0].text
    assert "unconfirmed" in context.items[0].text


def test_frontier_traversability_query_returns_bounded_metadata() -> None:
    memory = _search_frontier_memory().with_cell(
        SpatialCell(
            frame=FrameId("map"),
            coordinate=(6, 8),
            resolution=0.5,
            state=CellState.FRONTIER,
            traversability=0.4,
            claim_ids=(ClaimId("claim-frontier-east"),),
            metadata={"anchor": "east-frontier"},
        )
    )

    result = memory.query_navigation_frontiers(max_results=1)

    assert result.total_matches == 2
    assert result.truncated is True
    assert len(result.items) == 1
    assert result.items[0].coordinate == (4, 7)
    assert result.items[0].state is CellState.FRONTIER
    assert result.items[0].traversability == 0.6
    assert result.items[0].claim_ids == (ClaimId("claim-frontier-north"),)
    assert result.items[0].status is ClaimStatus.ACTIVE


def test_task_allocation_scenario_detects_shared_resource_conflicts() -> None:
    memory = _task_allocation_memory()

    result = memory.list_coordination_commitments(max_results=5)

    assert result.total_matches == 2
    assert result.truncated is False
    assert [row.commitment_id for row in result.items] == [
        CommitmentId("commitment-robot-a-frontier"),
        CommitmentId("commitment-robot-b-frontier"),
    ]
    assert [row.status for row in result.items] == [
        CommitmentStatus.CONFLICTED,
        CommitmentStatus.CONFLICTED,
    ]
    assert [row.actor_id for row in result.items] == [EntityId("robot-a"), EntityId("robot-b")]
    assert {row.target_id for row in result.items} == {EntityId("frontier:north")}
    assert [row.conflict_ids for row in result.items] == [
        (CommitmentId("commitment-robot-b-frontier"),),
        (CommitmentId("commitment-robot-a-frontier"),),
    ]
    assert [row.claim_ids for row in result.items] == [
        (ClaimId("claim-frontier-reserved-a"),),
        (ClaimId("claim-frontier-reserved-b"),),
    ]


def test_navigation_frontier_ablation_blocks_frontier_query_capability() -> None:
    result = RepresentationMemory.empty(frame=FrameId("map")).query_navigation_frontiers(max_results=5)

    assert result.total_matches == 0
    assert result.truncated is False
    assert result.items == ()


def test_perception_hazard_ablation_blocks_scene_graph_capability() -> None:
    result = RepresentationMemory.empty(frame=FrameId("map")).find_perception_matches(
        kind=EntityKind.HAZARD,
        max_results=5,
    )

    assert result.total_matches == 0
    assert result.truncated is False
    assert result.items == ()


def test_belief_conflict_ablation_blocks_claim_inspection_capability() -> None:
    result = RepresentationMemory.empty(frame=FrameId("map")).inspect_belief(
        status=ClaimStatus.CONFLICTED,
        max_results=5,
    )

    assert result.total_matches == 0
    assert result.truncated is False
    assert result.items == ()


def test_memory_context_ablation_blocks_context_summary_capability() -> None:
    result = RepresentationMemory.empty(frame=FrameId("map")).summarize_context(max_notes=5)

    assert result.total_matches == 0
    assert result.truncated is False
    assert result.items == ()


def test_coordination_commitment_ablation_blocks_commitment_capability() -> None:
    result = RepresentationMemory.empty(frame=FrameId("map")).list_coordination_commitments(max_results=5)

    assert result.total_matches == 0
    assert result.truncated is False
    assert result.items == ()



def _blocked_path_memory() -> RepresentationMemory:
    blocked_claim = _claim(
        claim_id=ClaimId("claim-blocked-a"),
        source=_source(SourceId("robot-a"), QueryFamily.BELIEF_PROVENANCE),
        confidence=0.8,
        status=ClaimStatus.CONFLICTED,
        evidence=(
            _evidence(
                EvidenceId("evidence-blocked-a"),
                uri="mosaic://scenario/blocked-path/robot-a",
            ),
        ),
        conflicts_with=(ClaimId("claim-clear-b"),),
    )
    clear_claim = _claim(
        claim_id=ClaimId("claim-clear-b"),
        source=_source(SourceId("robot-b"), QueryFamily.BELIEF_PROVENANCE),
        value="true",
        confidence=0.7,
        status=ClaimStatus.CONFLICTED,
        evidence=(
            _evidence(
                EvidenceId("evidence-clear-b"),
                uri="mosaic://scenario/blocked-path/robot-b",
            ),
        ),
        conflicts_with=(ClaimId("claim-blocked-a"),),
    )
    cell = SpatialCell(
        frame=FrameId("map"),
        coordinate=(1, 2),
        resolution=0.5,
        state=CellState.BLOCKED,
        traversability=0.0,
        claim_ids=(blocked_claim.claim_id, clear_claim.claim_id),
        metadata={"edge": "edge:kitchen->hall", "cell_id": "cell-kitchen-hall"},
    )
    return (
        RepresentationMemory.empty(frame=FrameId("map"))
        .with_claim(blocked_claim)
        .with_claim(clear_claim)
        .with_cell(cell)
    )


def _search_frontier_memory() -> RepresentationMemory:
    claim = _claim(
        claim_id=ClaimId("claim-frontier-north"),
        subject="cell-frontier-north",
        predicate="frontier_state",
        value="frontier",
        source=_source(SourceId("synthetic-frontier"), QueryFamily.NAVIGATION),
        confidence=0.75,
        status=ClaimStatus.ACTIVE,
        evidence=(
            _evidence(
                EvidenceId("evidence-frontier-north"),
                uri="mosaic://scenario/search-frontier/north",
            ),
        ),
    )
    cell = SpatialCell(
        frame=FrameId("map"),
        coordinate=(4, 7),
        resolution=0.5,
        state=CellState.FRONTIER,
        traversability=0.6,
        claim_ids=(claim.claim_id,),
        metadata={"cell_id": "cell-frontier-north"},
    )
    entity = Entity(
        entity_id=EntityId("entity-frontier-north"),
        kind=EntityKind.FRONTIER,
        label="north frontier",
        confidence=0.75,
        frame=FrameId("map"),
        claim_ids=(claim.claim_id,),
        metadata={"cell_id": "cell-frontier-north"},
    )
    relation = Relation(
        subject_id=entity.entity_id,
        kind=RelationKind.ADJACENT_TO,
        object_id=EntityId("region-kitchen"),
        confidence=0.7,
        claim_ids=(claim.claim_id,),
        metadata={"context": "scene graph update"},
    )
    note = MemoryNote(
        note_id=NoteId("note-unexplored-north"),
        text="north frontier remains unexplored and unconfirmed beyond the current map edge",
        family=QueryFamily.MEMORY_CONTEXT,
        created_at=CREATED_AT,
        confidence=0.65,
        claim_ids=(claim.claim_id,),
        metadata={"cell_id": "cell-frontier-north"},
    )
    return (
        RepresentationMemory.empty(frame=FrameId("map"))
        .with_claim(claim)
        .with_cell(cell)
        .with_entity(entity)
        .with_relation(relation)
        .with_note(note)
    )


def _task_allocation_memory() -> RepresentationMemory:
    reserved_a = _claim(
        claim_id=ClaimId("claim-frontier-reserved-a"),
        subject="frontier:north",
        predicate="reserved_by",
        value="robot-a",
        source=_source(SourceId("coordinator-a"), QueryFamily.COORDINATION),
        confidence=0.9,
        status=ClaimStatus.CONFLICTED,
        valid_until=Timestamp(6_000_000_000),
        evidence=(
            _evidence(
                EvidenceId("evidence-reservation-a"),
                uri="mosaic://scenario/task-allocation/robot-a",
            ),
        ),
        conflicts_with=(ClaimId("claim-frontier-reserved-b"),),
    )
    reserved_b = _claim(
        claim_id=ClaimId("claim-frontier-reserved-b"),
        subject="frontier:north",
        predicate="reserved_by",
        value="robot-b",
        source=_source(SourceId("coordinator-b"), QueryFamily.COORDINATION),
        confidence=0.85,
        status=ClaimStatus.CONFLICTED,
        valid_until=Timestamp(6_000_000_000),
        evidence=(
            _evidence(
                EvidenceId("evidence-reservation-b"),
                uri="mosaic://scenario/task-allocation/robot-b",
            ),
        ),
        conflicts_with=(ClaimId("claim-frontier-reserved-a"),),
    )
    commitment_a = Commitment(
        commitment_id=CommitmentId("commitment-robot-a-frontier"),
        status=CommitmentStatus.CONFLICTED,
        actor_id=EntityId("robot-a"),
        target_id=EntityId("frontier:north"),
        description="robot-a reserves frontier:north for inspection",
        confidence=0.9,
        valid_from=Timestamp(2_000_000_000),
        valid_until=Timestamp(6_000_000_000),
        claim_ids=(reserved_a.claim_id,),
        conflict_ids=(CommitmentId("commitment-robot-b-frontier"),),
        metadata={"resource": "frontier:north", "assignment": "inspect"},
    )
    commitment_b = Commitment(
        commitment_id=CommitmentId("commitment-robot-b-frontier"),
        status=CommitmentStatus.CONFLICTED,
        actor_id=EntityId("robot-b"),
        target_id=EntityId("frontier:north"),
        description="robot-b reserves frontier:north for inspection",
        confidence=0.85,
        valid_from=Timestamp(3_000_000_000),
        valid_until=Timestamp(5_000_000_000),
        claim_ids=(reserved_b.claim_id,),
        conflict_ids=(CommitmentId("commitment-robot-a-frontier"),),
        metadata={"resource": "frontier:north", "assignment": "inspect"},
    )
    return (
        RepresentationMemory.empty(frame=FrameId("map"))
        .with_claim(reserved_a)
        .with_claim(reserved_b)
        .with_commitment(commitment_a)
        .with_commitment(commitment_b)
    )



def _claim(
    *,
    claim_id: ClaimId,
    subject: str = "edge:kitchen->hall",
    predicate: str = "traversable",
    value: str = "false",
    source: SourceMetadata,
    confidence: float,
    status: ClaimStatus,
    valid_until: Timestamp | None = VALID_UNTIL,
    evidence: tuple[EvidenceReference, ...] = (),
    conflicts_with: tuple[ClaimId, ...] = (),
) -> Claim:
    return Claim(
        claim_id=claim_id,
        subject=subject,
        predicate=predicate,
        value=value,
        source=source,
        confidence=confidence,
        status=status,
        created_at=CREATED_AT,
        observed_at=OBSERVED_AT,
        valid_until=valid_until,
        evidence=evidence,
        conflicts_with=conflicts_with,
    )


def _source(source_id: SourceId, family: QueryFamily) -> SourceMetadata:
    return SourceMetadata(
        source_id=source_id,
        family=family,
        metadata={"scenario": "phase-7-representation"},
    )


def _evidence(evidence_id: EvidenceId, *, uri: str) -> EvidenceReference:
    return EvidenceReference(
        evidence_id=evidence_id,
        kind=EvidenceKind.SYNTHETIC_FIXTURE,
        uri=uri,
    )
