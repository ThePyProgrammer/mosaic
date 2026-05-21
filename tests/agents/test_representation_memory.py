import pytest

from mosaic.agents.memory import (
    BeliefProvenanceMemory,
    CellState,
    Claim,
    ClaimId,
    ClaimStatus,
    Commitment,
    CommitmentId,
    CommitmentMemory,
    CommitmentStatus,
    Entity,
    EntityId,
    EntityKind,
    EvidenceId,
    EvidenceKind,
    EvidenceReference,
    MemoryNote,
    MemoryQueryResult,
    NoteId,
    QueryFamily,
    Relation,
    RepresentationMemory,
    RelationKind,
    SceneGraphMemory,
    SourceId,
    SourceMetadata,
    SpatialCell,
    SpatialRasterMemory,
    TextMemory,
)
from mosaic.core import FrameId, Timestamp


CREATED_AT = Timestamp(1_000_000_000)


def test_typed_ids_reject_blank_values() -> None:
    for id_type in (EntityId, ClaimId, EvidenceId, SourceId, NoteId, CommitmentId):
        with pytest.raises(ValueError, match="blank"):
            id_type(" ")


def test_evidence_reference_stores_opaque_uri_without_loader() -> None:
    reference = EvidenceReference(
        evidence_id=EvidenceId("evidence-1"),
        kind=EvidenceKind.SNAPSHOT,
        uri="splat://map/0",
    )

    assert reference.evidence_id == EvidenceId("evidence-1")
    assert reference.kind is EvidenceKind.SNAPSHOT
    assert reference.uri == "splat://map/0"
    assert not hasattr(reference, "load")
    assert not hasattr(reference, "dereference")


def test_source_metadata_freezes_metadata_mapping() -> None:
    labels = {"robot": "ugv-1"}
    source = SourceMetadata(
        source_id=SourceId("source-1"),
        family=QueryFamily.PERCEPTION,
        metadata=labels,
    )
    labels["robot"] = "mutated"

    assert source.metadata["robot"] == "ugv-1"
    with pytest.raises(TypeError):
        source.metadata["new"] = "blocked"  # type: ignore[index]


def test_all_memory_families_are_constructible_as_independent_snapshots() -> None:
    cell = _cell()
    entity = _entity()
    relation = _relation()
    note = _note()
    evidence = EvidenceReference(
        evidence_id=EvidenceId("evidence-1"),
        kind=EvidenceKind.SYNTHETIC_FIXTURE,
        uri="fixture://observation/1",
    )
    commitment = _commitment()

    spatial = SpatialRasterMemory(cells=[cell])
    scene_graph = SceneGraphMemory(entities=[entity], relations=[relation])
    text = TextMemory(notes=[note])
    belief = BeliefProvenanceMemory(claims=[ClaimId("claim-1")], evidence=[evidence])
    commitments = CommitmentMemory(commitments=[commitment])

    assert spatial.cells == (cell,)
    assert scene_graph.entities == (entity,)
    assert scene_graph.relations == (relation,)
    assert text.notes == (note,)
    assert belief.claims == (ClaimId("claim-1"),)
    assert belief.evidence == (evidence,)
    assert commitments.commitments == (commitment,)

    with pytest.raises(AttributeError):
        spatial.cells = ()  # type: ignore[misc]


def test_representation_memory_empty_owns_all_families() -> None:
    memory = RepresentationMemory.empty(frame=FrameId("map"))

    assert isinstance(memory.spatial, SpatialRasterMemory)
    assert isinstance(memory.scene, SceneGraphMemory)
    assert isinstance(memory.text, TextMemory)
    assert isinstance(memory.belief, BeliefProvenanceMemory)
    assert isinstance(memory.commitments, CommitmentMemory)
    assert memory.spatial.cells == ()
    assert memory.scene.entities == ()
    assert memory.scene.relations == ()
    assert memory.text.notes == ()
    assert memory.belief.claims == ()
    assert memory.commitments.commitments == ()


@pytest.mark.parametrize(
    "method_name,bound_name",
    (
        ("find_perception_matches", "max_results"),
        ("query_navigation_frontiers", "max_results"),
        ("list_coordination_commitments", "max_results"),
        ("inspect_belief", "max_results"),
        ("summarize_context", "max_notes"),
    ),
)
def test_representation_memory_query_bounds_must_be_positive(
    method_name: str,
    bound_name: str,
) -> None:
    memory = RepresentationMemory.empty(frame=FrameId("map"))

    with pytest.raises(ValueError, match=bound_name):
        getattr(memory, method_name)(**{bound_name: 0})


def test_memory_query_result_validates_truncation_metadata() -> None:
    with pytest.raises(ValueError, match="total_matches"):
        MemoryQueryResult(
            query_family=QueryFamily.PERCEPTION,
            items=("entity-1",),
            total_matches=0,
            truncated=False,
        )
    with pytest.raises(ValueError, match="truncated"):
        MemoryQueryResult(
            query_family=QueryFamily.PERCEPTION,
            items=("entity-1",),
            total_matches=2,
            truncated=False,
        )


def test_representation_memory_with_helpers_return_new_snapshots() -> None:
    original = RepresentationMemory.empty(frame=FrameId("map"))
    cell = _cell()
    entity = _entity()
    relation = _relation()
    claim = _claim()
    note = _note()
    commitment = _commitment()

    updated = (
        original.with_cell(cell)
        .with_entity(entity)
        .with_relation(relation)
        .with_claim(claim)
        .with_note(note)
        .with_commitment(commitment)
    )

    assert updated is not original
    assert original.spatial.cells == ()
    assert original.scene.entities == ()
    assert original.scene.relations == ()
    assert original.belief.claims == ()
    assert original.text.notes == ()
    assert original.commitments.commitments == ()
    assert updated.spatial.cells == (cell,)
    assert updated.scene.entities == (entity,)
    assert updated.scene.relations == (relation,)
    assert updated.belief.claims == (claim,)
    assert updated.text.notes == (note,)
    assert updated.commitments.commitments == (commitment,)


def test_find_perception_matches_returns_bounded_claim_evidence_and_status() -> None:
    claim_a = _claim(
        claim_id=ClaimId("claim-hazard-a"),
        evidence=(_evidence(EvidenceId("evidence-hazard-a")),),
    )
    claim_b = _claim(
        claim_id=ClaimId("claim-hazard-b"),
        confidence=0.6,
        status=ClaimStatus.CONFLICTED,
        evidence=(_evidence(EvidenceId("evidence-hazard-b")),),
    )
    memory = (
        RepresentationMemory.empty(frame=FrameId("map"))
        .with_claim(claim_a)
        .with_claim(claim_b)
        .with_entity(
            _entity(
                entity_id=EntityId("hazard-a"),
                kind=EntityKind.HAZARD,
                label="blocked doorway",
                claim_ids=(claim_a.claim_id,),
            )
        )
        .with_entity(
            _entity(
                entity_id=EntityId("hazard-b"),
                kind=EntityKind.HAZARD,
                label="spill",
                claim_ids=(claim_b.claim_id,),
            )
        )
    )

    result = memory.find_perception_matches(kind=EntityKind.HAZARD, max_results=1)

    assert result.query_family is QueryFamily.PERCEPTION
    assert result.total_matches == 2
    assert result.truncated is True
    assert len(result.items) == 1
    assert result.items[0].entity_id == EntityId("hazard-a")
    assert result.items[0].claim_ids == (ClaimId("claim-hazard-a"),)
    assert result.items[0].evidence == claim_a.evidence
    assert result.items[0].status is ClaimStatus.ACTIVE
    assert result.items[0].confidence == 0.8


def test_query_navigation_frontiers_returns_bounded_cells() -> None:
    memory = (
        RepresentationMemory.empty(frame=FrameId("map"))
        .with_cell(_cell(coordinate=(1, 2), state=CellState.FRONTIER))
        .with_cell(
            _cell(
                coordinate=(2, 3),
                state=CellState.BLOCKED,
                traversability=0.1,
                claim_ids=(ClaimId("claim-2"),),
            )
        )
    )

    result = memory.query_navigation_frontiers(max_results=1)

    assert result.query_family is QueryFamily.NAVIGATION
    assert result.total_matches == 2
    assert result.truncated is True
    assert result.items[0].coordinate == (1, 2)
    assert result.items[0].state is CellState.FRONTIER
    assert result.items[0].traversability == 0.75
    assert result.items[0].claim_ids == (ClaimId("claim-1"),)


def test_list_coordination_commitments_returns_bounded_conflicts() -> None:
    memory = (
        RepresentationMemory.empty(frame=FrameId("map"))
        .with_commitment(
            _commitment(
                commitment_id=CommitmentId("commitment-1"),
                conflict_ids=(CommitmentId("commitment-2"),),
            )
        )
        .with_commitment(
            _commitment(
                commitment_id=CommitmentId("commitment-2"),
                status=CommitmentStatus.CONFLICTED,
                conflict_ids=(CommitmentId("commitment-1"),),
            )
        )
    )

    result = memory.list_coordination_commitments(max_results=1)

    assert result.query_family is QueryFamily.COORDINATION
    assert result.total_matches == 2
    assert result.truncated is True
    assert result.items[0].commitment_id == CommitmentId("commitment-1")
    assert result.items[0].conflict_ids == (CommitmentId("commitment-2"),)
    assert result.items[0].claim_ids == (ClaimId("claim-1"),)
    assert result.items[0].confidence == 0.95


def test_inspect_belief_returns_bounded_conflicted_claims_without_hiding_either() -> None:
    claim_a = _claim(
        claim_id=ClaimId("claim-blocked-a"),
        status=ClaimStatus.CONFLICTED,
        conflicts_with=(ClaimId("claim-clear-b"),),
    )
    claim_b = _claim(
        claim_id=ClaimId("claim-clear-b"),
        value="true",
        confidence=0.7,
        status=ClaimStatus.CONFLICTED,
        conflicts_with=(ClaimId("claim-blocked-a"),),
    )
    memory = RepresentationMemory.empty(frame=FrameId("map")).with_claim(claim_a).with_claim(claim_b)

    result = memory.inspect_belief(status=ClaimStatus.CONFLICTED, max_results=2)

    assert result.query_family is QueryFamily.BELIEF_PROVENANCE
    assert result.total_matches == 2
    assert result.truncated is False
    assert [item.claim_id for item in result.items] == [
        ClaimId("claim-blocked-a"),
        ClaimId("claim-clear-b"),
    ]
    assert [item.conflicts_with for item in result.items] == [
        (ClaimId("claim-clear-b"),),
        (ClaimId("claim-blocked-a"),),
    ]


def test_summarize_context_returns_bounded_notes_with_source_claim_ids() -> None:
    memory = (
        RepresentationMemory.empty(frame=FrameId("map"))
        .with_note(_note(note_id=NoteId("note-1"), text="frontier unexplored"))
        .with_note(
            _note(
                note_id=NoteId("note-2"),
                text="doorway blocked by crate",
                claim_ids=(ClaimId("claim-2"),),
            )
        )
    )

    result = memory.summarize_context(max_notes=1)

    assert result.query_family is QueryFamily.MEMORY_CONTEXT
    assert result.total_matches == 2
    assert result.truncated is True
    assert result.items[0].note_id == NoteId("note-1")
    assert result.items[0].text == "frontier unexplored"
    assert result.items[0].claim_ids == (ClaimId("claim-1"),)


def test_spatial_cells_validate_resolution_and_traversability() -> None:
    with pytest.raises(ValueError, match="resolution"):
        _cell(resolution=0.0)
    with pytest.raises(ValueError, match="traversability"):
        _cell(traversability=-0.1)
    with pytest.raises(ValueError, match="traversability"):
        _cell(traversability=1.1)


def test_entity_relation_note_and_commitment_reject_invalid_confidence() -> None:
    with pytest.raises(ValueError, match="confidence"):
        _entity(confidence=-0.1)
    with pytest.raises(ValueError, match="confidence"):
        _relation(confidence=1.1)
    with pytest.raises(ValueError, match="confidence"):
        _note(confidence=-0.01)
    with pytest.raises(ValueError, match="confidence"):
        _commitment(confidence=1.01)


def test_commitment_rejects_invalid_time_window() -> None:
    with pytest.raises(ValueError, match="time window"):
        _commitment(valid_from=Timestamp(20), valid_until=Timestamp(10))


def _cell(
    *,
    coordinate: tuple[int, int] = (1, 2),
    resolution: float = 0.5,
    state: CellState = CellState.FREE,
    traversability: float = 0.75,
    claim_ids: tuple[ClaimId, ...] = (ClaimId("claim-1"),),
) -> SpatialCell:
    return SpatialCell(
        frame=FrameId("map"),
        coordinate=coordinate,
        resolution=resolution,
        state=state,
        traversability=traversability,
        claim_ids=claim_ids,
    )


def _entity(
    *,
    entity_id: EntityId = EntityId("entity-1"),
    kind: EntityKind = EntityKind.LANDMARK,
    label: str = "charging-station",
    confidence: float = 0.8,
    claim_ids: tuple[ClaimId, ...] = (ClaimId("claim-1"),),
) -> Entity:
    return Entity(
        entity_id=entity_id,
        kind=kind,
        label=label,
        confidence=confidence,
        frame=FrameId("map"),
        claim_ids=claim_ids,
    )


def _relation(*, confidence: float = 0.9) -> Relation:
    return Relation(
        subject_id=EntityId("entity-1"),
        kind=RelationKind.ADJACENT_TO,
        object_id=EntityId("entity-2"),
        confidence=confidence,
        claim_ids=(ClaimId("claim-1"),),
    )


def _note(
    *,
    note_id: NoteId = NoteId("note-1"),
    text: str = "frontier remains unexplored",
    confidence: float = 0.7,
    claim_ids: tuple[ClaimId, ...] = (ClaimId("claim-1"),),
) -> MemoryNote:
    return MemoryNote(
        note_id=note_id,
        text=text,
        family=QueryFamily.MEMORY_CONTEXT,
        created_at=Timestamp(10),
        confidence=confidence,
        claim_ids=claim_ids,
    )


def _commitment(
    *,
    commitment_id: CommitmentId = CommitmentId("commitment-1"),
    status: CommitmentStatus = CommitmentStatus.ACTIVE,
    confidence: float = 0.95,
    valid_from: Timestamp | None = Timestamp(10),
    valid_until: Timestamp | None = Timestamp(20),
    conflict_ids: tuple[CommitmentId, ...] = (),
) -> Commitment:
    return Commitment(
        commitment_id=commitment_id,
        status=status,
        actor_id=EntityId("robot-1"),
        target_id=EntityId("frontier-1"),
        description="inspect frontier",
        confidence=confidence,
        valid_from=valid_from,
        valid_until=valid_until,
        claim_ids=(ClaimId("claim-1"),),
        conflict_ids=conflict_ids,
    )


def _claim(
    *,
    claim_id: ClaimId = ClaimId("claim-1"),
    subject: str = "entity:hazard",
    predicate: str = "present",
    value: str = "true",
    confidence: float = 0.8,
    status: ClaimStatus = ClaimStatus.ACTIVE,
    evidence: tuple[EvidenceReference, ...] = (),
    conflicts_with: tuple[ClaimId, ...] = (),
) -> Claim:
    return Claim(
        claim_id=claim_id,
        subject=subject,
        predicate=predicate,
        value=value,
        source=SourceMetadata(
            source_id=SourceId("robot-a"),
            family=QueryFamily.BELIEF_PROVENANCE,
        ),
        confidence=confidence,
        status=status,
        created_at=CREATED_AT,
        evidence=evidence,
        conflicts_with=conflicts_with,
    )


def _evidence(evidence_id: EvidenceId) -> EvidenceReference:
    return EvidenceReference(
        evidence_id=evidence_id,
        kind=EvidenceKind.SYNTHETIC_FIXTURE,
        uri=f"fixture://{evidence_id}",
    )
