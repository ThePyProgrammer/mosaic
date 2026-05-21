from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Generic, Mapping, Self, TypeVar

from mosaic.core import FrameId, Timestamp


MemoryQueryItem = TypeVar("MemoryQueryItem")


class EntityKind(StrEnum):
    REGION = "region"
    OBJECT = "object"
    HAZARD = "hazard"
    LANDMARK = "landmark"
    ROBOT = "robot"
    FRONTIER = "frontier"


class RelationKind(StrEnum):
    CONTAINS = "contains"
    ADJACENT_TO = "adjacent_to"
    BLOCKS = "blocks"
    SUPPORTS = "supports"
    ASSIGNED_TO = "assigned_to"
    RESERVED_BY = "reserved_by"
    CONFLICTS_WITH = "conflicts_with"


class EvidenceKind(StrEnum):
    SNAPSHOT = "snapshot"
    OBSERVATION = "observation"
    OPERATOR_NOTE = "operator_note"
    SYNTHETIC_FIXTURE = "synthetic_fixture"


class QueryFamily(StrEnum):
    PERCEPTION = "perception"
    NAVIGATION = "navigation"
    COORDINATION = "coordination"
    BELIEF_PROVENANCE = "belief_provenance"
    MEMORY_CONTEXT = "memory_context"


class CellState(StrEnum):
    UNKNOWN = "unknown"
    FREE = "free"
    OCCUPIED = "occupied"
    FRONTIER = "frontier"
    BLOCKED = "blocked"


class CommitmentStatus(StrEnum):
    PROPOSED = "proposed"
    ACTIVE = "active"
    COMPLETED = "completed"
    CONFLICTED = "conflicted"
    CANCELLED = "cancelled"


class ClaimStatus(StrEnum):
    ACTIVE = "active"
    CONFLICTED = "conflicted"
    STALE = "stale"
    SUPERSEDED = "superseded"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class EntityId:
    value: str

    def __post_init__(self) -> None:
        _validate_nonblank(self.value, "EntityId value")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class ClaimId:
    value: str

    def __post_init__(self) -> None:
        _validate_nonblank(self.value, "ClaimId value")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class EvidenceId:
    value: str

    def __post_init__(self) -> None:
        _validate_nonblank(self.value, "EvidenceId value")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class SourceId:
    value: str

    def __post_init__(self) -> None:
        _validate_nonblank(self.value, "SourceId value")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class NoteId:
    value: str

    def __post_init__(self) -> None:
        _validate_nonblank(self.value, "NoteId value")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class CommitmentId:
    value: str

    def __post_init__(self) -> None:
        _validate_nonblank(self.value, "CommitmentId value")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class SourceMetadata:
    source_id: SourceId
    family: QueryFamily
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for key in self.metadata:
            _validate_nonblank(key, "SourceMetadata metadata keys")
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


@dataclass(frozen=True, slots=True)
class EvidenceReference:
    evidence_id: EvidenceId
    kind: EvidenceKind
    uri: str

    def __post_init__(self) -> None:
        _validate_nonblank(self.uri, "EvidenceReference uri")


@dataclass(frozen=True, slots=True)
class Claim:
    claim_id: ClaimId
    subject: str
    predicate: str
    value: str
    source: SourceMetadata
    confidence: float
    status: ClaimStatus
    created_at: Timestamp
    observed_at: Timestamp | None = None
    valid_until: Timestamp | None = None
    evidence: tuple[EvidenceReference, ...] = ()
    conflicts_with: tuple[ClaimId, ...] = ()

    def __post_init__(self) -> None:
        _validate_nonblank(self.subject, "Claim subject")
        _validate_nonblank(self.predicate, "Claim predicate")
        _validate_nonblank(self.value, "Claim value")
        _validate_unit_interval(self.confidence, "Claim confidence")
        object.__setattr__(self, "evidence", tuple(self.evidence))
        object.__setattr__(self, "conflicts_with", tuple(self.conflicts_with))
        if self.claim_id in self.conflicts_with:
            raise ValueError("Claim conflicts_with must not include its own claim_id")


@dataclass(frozen=True, slots=True)
class SpatialCell:
    frame: FrameId
    coordinate: tuple[int, int]
    resolution: float
    state: CellState = CellState.UNKNOWN
    traversability: float = 0.0
    claim_ids: tuple[ClaimId, ...] = ()
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "coordinate", tuple(self.coordinate))
        object.__setattr__(self, "claim_ids", tuple(self.claim_ids))
        if len(self.coordinate) != 2:
            raise ValueError("SpatialCell coordinate must contain two values")
        if self.resolution <= 0.0:
            raise ValueError("SpatialCell resolution must be positive")
        _validate_unit_interval(self.traversability, "SpatialCell traversability")
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


@dataclass(frozen=True, slots=True)
class Entity:
    entity_id: EntityId
    kind: EntityKind
    label: str
    confidence: float
    frame: FrameId | None = None
    claim_ids: tuple[ClaimId, ...] = ()
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_nonblank(self.label, "Entity label")
        _validate_unit_interval(self.confidence, "Entity confidence")
        object.__setattr__(self, "claim_ids", tuple(self.claim_ids))
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


@dataclass(frozen=True, slots=True)
class Relation:
    subject_id: EntityId
    kind: RelationKind
    object_id: EntityId
    confidence: float
    claim_ids: tuple[ClaimId, ...] = ()
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_unit_interval(self.confidence, "Relation confidence")
        object.__setattr__(self, "claim_ids", tuple(self.claim_ids))
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


@dataclass(frozen=True, slots=True)
class MemoryNote:
    note_id: NoteId
    text: str
    family: QueryFamily
    created_at: Timestamp
    confidence: float
    claim_ids: tuple[ClaimId, ...] = ()
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_nonblank(self.text, "MemoryNote text")
        _validate_unit_interval(self.confidence, "MemoryNote confidence")
        object.__setattr__(self, "claim_ids", tuple(self.claim_ids))
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


@dataclass(frozen=True, slots=True)
class Commitment:
    commitment_id: CommitmentId
    status: CommitmentStatus
    actor_id: EntityId
    target_id: EntityId
    description: str
    confidence: float
    valid_from: Timestamp | None = None
    valid_until: Timestamp | None = None
    claim_ids: tuple[ClaimId, ...] = ()
    conflict_ids: tuple[CommitmentId, ...] = ()
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_nonblank(self.description, "Commitment description")
        _validate_unit_interval(self.confidence, "Commitment confidence")
        if self.valid_from is not None and self.valid_until is not None:
            if self.valid_from > self.valid_until:
                raise ValueError("Commitment time window must satisfy valid_from <= valid_until")
        object.__setattr__(self, "claim_ids", tuple(self.claim_ids))
        object.__setattr__(self, "conflict_ids", tuple(self.conflict_ids))
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


@dataclass(frozen=True, slots=True)
class SpatialRasterMemory:
    cells: tuple[SpatialCell, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "cells", tuple(self.cells))


@dataclass(frozen=True, slots=True)
class SceneGraphMemory:
    entities: tuple[Entity, ...] = ()
    relations: tuple[Relation, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "entities", tuple(self.entities))
        object.__setattr__(self, "relations", tuple(self.relations))


@dataclass(frozen=True, slots=True)
class TextMemory:
    notes: tuple[MemoryNote, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "notes", tuple(self.notes))


@dataclass(frozen=True, slots=True)
class BeliefProvenanceMemory:
    claims: tuple[Claim | ClaimId, ...] = ()
    evidence: tuple[EvidenceReference, ...] = ()
    sources: tuple[SourceMetadata, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "claims", tuple(self.claims))
        object.__setattr__(self, "evidence", tuple(self.evidence))
        object.__setattr__(self, "sources", tuple(self.sources))

    def with_claim(self, claim: Claim) -> BeliefProvenanceMemory:
        return type(self)(
            claims=self.claims + (claim,),
            evidence=self.evidence,
            sources=self.sources,
        )


@dataclass(frozen=True, slots=True)
class CommitmentMemory:
    commitments: tuple[Commitment, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "commitments", tuple(self.commitments))


@dataclass(frozen=True, slots=True)
class MemoryQueryResult(Generic[MemoryQueryItem]):
    query_family: QueryFamily
    items: tuple[MemoryQueryItem, ...]
    total_matches: int
    truncated: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "items", tuple(self.items))
        if self.total_matches < len(self.items):
            raise ValueError("MemoryQueryResult total_matches must cover returned items")
        if self.truncated != (self.total_matches > len(self.items)):
            raise ValueError("MemoryQueryResult truncated must equal total_matches > len(items)")


@dataclass(frozen=True, slots=True)
class PerceptionMatch:
    entity_id: EntityId
    kind: EntityKind
    label: str
    confidence: float
    claim_ids: tuple[ClaimId, ...] = ()
    evidence: tuple[EvidenceReference, ...] = ()
    status: ClaimStatus | None = None

    def __post_init__(self) -> None:
        _validate_nonblank(self.label, "PerceptionMatch label")
        _validate_unit_interval(self.confidence, "PerceptionMatch confidence")
        object.__setattr__(self, "claim_ids", tuple(self.claim_ids))
        object.__setattr__(self, "evidence", tuple(self.evidence))


@dataclass(frozen=True, slots=True)
class NavigationCellResult:
    coordinate: tuple[int, int]
    state: CellState
    traversability: float
    claim_ids: tuple[ClaimId, ...] = ()
    evidence: tuple[EvidenceReference, ...] = ()
    status: ClaimStatus | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "coordinate", tuple(self.coordinate))
        if len(self.coordinate) != 2:
            raise ValueError("NavigationCellResult coordinate must contain two values")
        _validate_unit_interval(self.traversability, "NavigationCellResult traversability")
        object.__setattr__(self, "claim_ids", tuple(self.claim_ids))
        object.__setattr__(self, "evidence", tuple(self.evidence))


@dataclass(frozen=True, slots=True)
class CoordinationCommitmentResult:
    commitment_id: CommitmentId
    status: CommitmentStatus
    actor_id: EntityId
    target_id: EntityId
    description: str
    confidence: float
    claim_ids: tuple[ClaimId, ...] = ()
    conflict_ids: tuple[CommitmentId, ...] = ()

    def __post_init__(self) -> None:
        _validate_nonblank(self.description, "CoordinationCommitmentResult description")
        _validate_unit_interval(self.confidence, "CoordinationCommitmentResult confidence")
        object.__setattr__(self, "claim_ids", tuple(self.claim_ids))
        object.__setattr__(self, "conflict_ids", tuple(self.conflict_ids))


@dataclass(frozen=True, slots=True)
class BeliefInspectionResult:
    claim_id: ClaimId
    subject: str
    predicate: str
    value: str
    confidence: float
    status: ClaimStatus
    evidence: tuple[EvidenceReference, ...] = ()
    conflicts_with: tuple[ClaimId, ...] = ()

    def __post_init__(self) -> None:
        _validate_nonblank(self.subject, "BeliefInspectionResult subject")
        _validate_nonblank(self.predicate, "BeliefInspectionResult predicate")
        _validate_nonblank(self.value, "BeliefInspectionResult value")
        _validate_unit_interval(self.confidence, "BeliefInspectionResult confidence")
        object.__setattr__(self, "evidence", tuple(self.evidence))
        object.__setattr__(self, "conflicts_with", tuple(self.conflicts_with))


@dataclass(frozen=True, slots=True)
class ContextNoteResult:
    note_id: NoteId
    text: str
    family: QueryFamily
    confidence: float
    claim_ids: tuple[ClaimId, ...] = ()

    def __post_init__(self) -> None:
        _validate_nonblank(self.text, "ContextNoteResult text")
        _validate_unit_interval(self.confidence, "ContextNoteResult confidence")
        object.__setattr__(self, "claim_ids", tuple(self.claim_ids))


@dataclass(frozen=True, slots=True)
class RepresentationMemory:
    spatial: SpatialRasterMemory = field(default_factory=SpatialRasterMemory)
    scene: SceneGraphMemory = field(default_factory=SceneGraphMemory)
    text: TextMemory = field(default_factory=TextMemory)
    belief: BeliefProvenanceMemory = field(default_factory=BeliefProvenanceMemory)
    commitments: CommitmentMemory = field(default_factory=CommitmentMemory)

    @property
    def scene_graph(self) -> SceneGraphMemory:
        return self.scene

    @classmethod
    def empty(cls, frame: FrameId) -> Self:
        return cls(spatial=SpatialRasterMemory())

    def with_cell(self, cell: SpatialCell) -> Self:
        return type(self)(
            spatial=SpatialRasterMemory(cells=self.spatial.cells + (cell,)),
            scene=self.scene,
            text=self.text,
            belief=self.belief,
            commitments=self.commitments,
        )

    def with_entity(self, entity: Entity) -> Self:
        return type(self)(
            spatial=self.spatial,
            scene=SceneGraphMemory(
                entities=self.scene.entities + (entity,),
                relations=self.scene.relations,
            ),
            text=self.text,
            belief=self.belief,
            commitments=self.commitments,
        )

    def with_relation(self, relation: Relation) -> Self:
        return type(self)(
            spatial=self.spatial,
            scene=SceneGraphMemory(
                entities=self.scene.entities,
                relations=self.scene.relations + (relation,),
            ),
            text=self.text,
            belief=self.belief,
            commitments=self.commitments,
        )

    def with_claim(self, claim: Claim) -> Self:
        return type(self)(
            spatial=self.spatial,
            scene=self.scene,
            text=self.text,
            belief=self.belief.with_claim(claim),
            commitments=self.commitments,
        )

    def with_note(self, note: MemoryNote) -> Self:
        return type(self)(
            spatial=self.spatial,
            scene=self.scene,
            text=TextMemory(notes=self.text.notes + (note,)),
            belief=self.belief,
            commitments=self.commitments,
        )

    def with_commitment(self, commitment: Commitment) -> Self:
        return type(self)(
            spatial=self.spatial,
            scene=self.scene,
            text=self.text,
            belief=self.belief,
            commitments=CommitmentMemory(
                commitments=self.commitments.commitments + (commitment,)
            ),
        )

    def mark_stale_claims(self, *, now: Timestamp) -> Self:
        return type(self)(
            spatial=self.spatial,
            scene=self.scene,
            text=self.text,
            belief=mark_stale_claims(self.belief, now=now),
            commitments=self.commitments,
        )

    def find_perception_matches(
        self,
        kind: EntityKind | None = None,
        *,
        max_results: int,
    ) -> MemoryQueryResult[PerceptionMatch]:
        _validate_positive_bound(max_results, "max_results")
        matches = tuple(entity for entity in self.scene.entities if kind is None or entity.kind is kind)
        rows = tuple(
            PerceptionMatch(
                entity_id=entity.entity_id,
                kind=entity.kind,
                label=entity.label,
                confidence=entity.confidence,
                claim_ids=entity.claim_ids,
                evidence=_evidence_for_claims(self.belief, entity.claim_ids),
                status=_combined_claim_status(self.belief, entity.claim_ids),
            )
            for entity in matches[:max_results]
        )
        return MemoryQueryResult(
            query_family=QueryFamily.PERCEPTION,
            items=rows,
            total_matches=len(matches),
            truncated=len(matches) > len(rows),
        )

    def query_navigation_frontiers(
        self,
        *,
        max_results: int,
    ) -> MemoryQueryResult[NavigationCellResult]:
        _validate_positive_bound(max_results, "max_results")
        matches = tuple(
            cell
            for cell in self.spatial.cells
            if cell.state in {CellState.FRONTIER, CellState.BLOCKED}
        )
        rows = tuple(
            NavigationCellResult(
                coordinate=cell.coordinate,
                state=cell.state,
                traversability=cell.traversability,
                claim_ids=cell.claim_ids,
                evidence=_evidence_for_claims(self.belief, cell.claim_ids),
                status=_combined_claim_status(self.belief, cell.claim_ids),
            )
            for cell in matches[:max_results]
        )
        return MemoryQueryResult(
            query_family=QueryFamily.NAVIGATION,
            items=rows,
            total_matches=len(matches),
            truncated=len(matches) > len(rows),
        )

    def list_coordination_commitments(
        self,
        *,
        max_results: int,
    ) -> MemoryQueryResult[CoordinationCommitmentResult]:
        _validate_positive_bound(max_results, "max_results")
        matches = self.commitments.commitments
        rows = tuple(
            CoordinationCommitmentResult(
                commitment_id=commitment.commitment_id,
                status=commitment.status,
                actor_id=commitment.actor_id,
                target_id=commitment.target_id,
                description=commitment.description,
                confidence=commitment.confidence,
                claim_ids=commitment.claim_ids,
                conflict_ids=commitment.conflict_ids,
            )
            for commitment in matches[:max_results]
        )
        return MemoryQueryResult(
            query_family=QueryFamily.COORDINATION,
            items=rows,
            total_matches=len(matches),
            truncated=len(matches) > len(rows),
        )

    def inspect_belief(
        self,
        status: ClaimStatus | None = None,
        *,
        max_results: int,
    ) -> MemoryQueryResult[BeliefInspectionResult]:
        _validate_positive_bound(max_results, "max_results")
        matches = tuple(
            claim
            for claim in self.belief.claims
            if isinstance(claim, Claim) and (status is None or claim.status is status)
        )
        rows = tuple(
            BeliefInspectionResult(
                claim_id=claim.claim_id,
                subject=claim.subject,
                predicate=claim.predicate,
                value=claim.value,
                confidence=claim.confidence,
                status=claim.status,
                evidence=claim.evidence,
                conflicts_with=claim.conflicts_with,
            )
            for claim in matches[:max_results]
        )
        return MemoryQueryResult(
            query_family=QueryFamily.BELIEF_PROVENANCE,
            items=rows,
            total_matches=len(matches),
            truncated=len(matches) > len(rows),
        )

    def summarize_context(
        self,
        *,
        max_notes: int,
    ) -> MemoryQueryResult[ContextNoteResult]:
        _validate_positive_bound(max_notes, "max_notes")
        matches = self.text.notes
        rows = tuple(
            ContextNoteResult(
                note_id=note.note_id,
                text=note.text,
                family=note.family,
                confidence=note.confidence,
                claim_ids=note.claim_ids,
            )
            for note in matches[:max_notes]
        )
        return MemoryQueryResult(
            query_family=QueryFamily.MEMORY_CONTEXT,
            items=rows,
            total_matches=len(matches),
            truncated=len(matches) > len(rows),
        )


def mark_stale_claims(
    memory: BeliefProvenanceMemory,
    *,
    now: Timestamp,
) -> BeliefProvenanceMemory:
    staleable_statuses = {ClaimStatus.ACTIVE, ClaimStatus.CONFLICTED}
    updated_claims: list[Claim | ClaimId] = []
    for claim in memory.claims:
        if not isinstance(claim, Claim):
            updated_claims.append(claim)
            continue
        if (
            claim.valid_until is not None
            and now > claim.valid_until
            and claim.status in staleable_statuses
        ):
            updated_claims.append(
                Claim(
                    claim_id=claim.claim_id,
                    subject=claim.subject,
                    predicate=claim.predicate,
                    value=claim.value,
                    source=claim.source,
                    confidence=claim.confidence,
                    status=ClaimStatus.STALE,
                    created_at=claim.created_at,
                    observed_at=claim.observed_at,
                    valid_until=claim.valid_until,
                    evidence=claim.evidence,
                    conflicts_with=claim.conflicts_with,
                )
            )
            continue
        updated_claims.append(claim)
    return type(memory)(
        claims=tuple(updated_claims),
        evidence=memory.evidence,
        sources=memory.sources,
    )


def _validate_positive_bound(value: int, label: str) -> None:
    if value <= 0:
        raise ValueError(f"{label} must be positive")


def _evidence_for_claims(
    memory: BeliefProvenanceMemory,
    claim_ids: tuple[ClaimId, ...],
) -> tuple[EvidenceReference, ...]:
    evidence: list[EvidenceReference] = []
    for claim in memory.claims:
        if isinstance(claim, Claim) and claim.claim_id in claim_ids:
            evidence.extend(claim.evidence)
    return tuple(evidence)


def _combined_claim_status(
    memory: BeliefProvenanceMemory,
    claim_ids: tuple[ClaimId, ...],
) -> ClaimStatus | None:
    statuses = tuple(
        claim.status
        for claim in memory.claims
        if isinstance(claim, Claim) and claim.claim_id in claim_ids
    )
    if not statuses:
        return None
    for preferred in (ClaimStatus.CONFLICTED, ClaimStatus.STALE, ClaimStatus.ACTIVE):
        if preferred in statuses:
            return preferred
    return statuses[0]


def _validate_nonblank(value: str, label: str) -> None:
    if not value.strip():
        raise ValueError(f"{label} must not be blank")


def _validate_unit_interval(value: float, label: str) -> None:
    if value < 0.0 or value > 1.0:
        raise ValueError(f"{label} must be between 0 and 1")


__all__ = [
    "BeliefProvenanceMemory",
    "CellState",
    "Claim",
    "ClaimId",
    "ClaimStatus",
    "Commitment",
    "CommitmentId",
    "CommitmentMemory",
    "CommitmentStatus",
    "Entity",
    "EntityId",
    "EntityKind",
    "EvidenceId",
    "EvidenceKind",
    "EvidenceReference",
    "MemoryNote",
    "MemoryQueryResult",
    "NoteId",
    "PerceptionMatch",
    "NavigationCellResult",
    "CoordinationCommitmentResult",
    "BeliefInspectionResult",
    "ContextNoteResult",
    "QueryFamily",
    "Relation",
    "RelationKind",
    "RepresentationMemory",
    "SceneGraphMemory",
    "SourceId",
    "SourceMetadata",
    "SpatialCell",
    "SpatialRasterMemory",
    "TextMemory",
    "mark_stale_claims",
]
