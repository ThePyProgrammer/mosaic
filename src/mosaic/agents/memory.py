from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Mapping

from mosaic.core import FrameId, Timestamp


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
    claims: tuple[ClaimId, ...] = ()
    evidence: tuple[EvidenceReference, ...] = ()
    sources: tuple[SourceMetadata, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "claims", tuple(self.claims))
        object.__setattr__(self, "evidence", tuple(self.evidence))
        object.__setattr__(self, "sources", tuple(self.sources))


@dataclass(frozen=True, slots=True)
class CommitmentMemory:
    commitments: tuple[Commitment, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "commitments", tuple(self.commitments))


@dataclass(frozen=True, slots=True)
class RepresentationMemory:
    spatial: SpatialRasterMemory = field(default_factory=SpatialRasterMemory)
    scene_graph: SceneGraphMemory = field(default_factory=SceneGraphMemory)
    text: TextMemory = field(default_factory=TextMemory)
    belief: BeliefProvenanceMemory = field(default_factory=BeliefProvenanceMemory)
    commitments: CommitmentMemory = field(default_factory=CommitmentMemory)


def _validate_nonblank(value: str, label: str) -> None:
    if not value.strip():
        raise ValueError(f"{label} must not be blank")


def _validate_unit_interval(value: float, label: str) -> None:
    if value < 0.0 or value > 1.0:
        raise ValueError(f"{label} must be between 0 and 1")


__all__ = [
    "BeliefProvenanceMemory",
    "CellState",
    "ClaimId",
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
    "NoteId",
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
]
