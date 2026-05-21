import pytest

from mosaic.agents.memory import (
    BeliefProvenanceMemory,
    CellState,
    ClaimId,
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
    NoteId,
    QueryFamily,
    Relation,
    RelationKind,
    SceneGraphMemory,
    SourceId,
    SourceMetadata,
    SpatialCell,
    SpatialRasterMemory,
    TextMemory,
)
from mosaic.core import FrameId, Timestamp


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
    resolution: float = 0.5,
    traversability: float = 0.75,
) -> SpatialCell:
    return SpatialCell(
        frame=FrameId("map"),
        coordinate=(1, 2),
        resolution=resolution,
        state=CellState.FREE,
        traversability=traversability,
        claim_ids=(ClaimId("claim-1"),),
    )


def _entity(*, confidence: float = 0.8) -> Entity:
    return Entity(
        entity_id=EntityId("entity-1"),
        kind=EntityKind.LANDMARK,
        label="charging-station",
        confidence=confidence,
        frame=FrameId("map"),
        claim_ids=(ClaimId("claim-1"),),
    )


def _relation(*, confidence: float = 0.9) -> Relation:
    return Relation(
        subject_id=EntityId("entity-1"),
        kind=RelationKind.ADJACENT_TO,
        object_id=EntityId("entity-2"),
        confidence=confidence,
        claim_ids=(ClaimId("claim-1"),),
    )


def _note(*, confidence: float = 0.7) -> MemoryNote:
    return MemoryNote(
        note_id=NoteId("note-1"),
        text="frontier remains unexplored",
        family=QueryFamily.MEMORY_CONTEXT,
        created_at=Timestamp(10),
        confidence=confidence,
        claim_ids=(ClaimId("claim-1"),),
    )


def _commitment(
    *,
    confidence: float = 0.95,
    valid_from: Timestamp | None = Timestamp(10),
    valid_until: Timestamp | None = Timestamp(20),
) -> Commitment:
    return Commitment(
        commitment_id=CommitmentId("commitment-1"),
        status=CommitmentStatus.ACTIVE,
        actor_id=EntityId("robot-1"),
        target_id=EntityId("frontier-1"),
        description="inspect frontier",
        confidence=confidence,
        valid_from=valid_from,
        valid_until=valid_until,
        claim_ids=(ClaimId("claim-1"),),
    )
