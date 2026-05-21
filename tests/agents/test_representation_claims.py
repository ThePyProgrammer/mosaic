import pytest

from mosaic.agents.memory import (
    BeliefProvenanceMemory,
    Claim,
    ClaimId,
    ClaimStatus,
    EvidenceId,
    EvidenceKind,
    EvidenceReference,
    QueryFamily,
    SourceId,
    SourceMetadata,
    mark_stale_claims,
)
from mosaic.core import Timestamp


CREATED_AT = Timestamp(1_000_000_000)
OBSERVED_AT = Timestamp(2_000_000_000)
VALID_UNTIL = Timestamp(3_000_000_000)


def test_claim_requires_confidence_in_closed_unit_interval() -> None:
    with pytest.raises(ValueError, match="confidence"):
        _claim(confidence=-0.01)
    with pytest.raises(ValueError, match="confidence"):
        _claim(confidence=1.01)

    assert _claim(confidence=0.0).confidence == 0.0
    assert _claim(confidence=1.0).confidence == 1.0


def test_claim_rejects_blank_fact_fields_and_self_conflict() -> None:
    with pytest.raises(ValueError, match="subject"):
        _claim(subject=" ")
    with pytest.raises(ValueError, match="predicate"):
        _claim(predicate=" ")
    with pytest.raises(ValueError, match="value"):
        _claim(value=" ")
    with pytest.raises(ValueError, match="conflict"):
        _claim(conflicts_with=(ClaimId("claim-blocked-a"),))


def test_evidence_reference_remains_typed_and_opaque() -> None:
    evidence = _evidence()
    claim = _claim(evidence=(evidence,))

    assert claim.evidence == (evidence,)
    assert evidence.evidence_id == EvidenceId("evidence-blocked-a")
    assert evidence.kind is EvidenceKind.OBSERVATION
    assert evidence.uri == "mosaic://evidence/blocked-a"
    assert not hasattr(evidence, "load")
    assert not hasattr(evidence, "dereference")
    assert not hasattr(evidence, "payload")


def test_contradictory_robot_reports_remain_visible_conflicts() -> None:
    blocked_claim, clear_claim = _contradictory_claims()
    memory = BeliefProvenanceMemory().with_claim(blocked_claim).with_claim(clear_claim)

    assert memory.claims == (blocked_claim, clear_claim)
    assert [claim.claim_id for claim in memory.claims] == [
        ClaimId("claim-blocked-a"),
        ClaimId("claim-clear-b"),
    ]
    assert {claim.status for claim in memory.claims} == {ClaimStatus.CONFLICTED}
    assert blocked_claim.conflicts_with == (ClaimId("claim-clear-b"),)
    assert clear_claim.conflicts_with == (ClaimId("claim-blocked-a"),)


def test_memory_does_not_remove_latest_or_highest_confidence_claim() -> None:
    blocked_claim, clear_claim = _contradictory_claims()
    memory = BeliefProvenanceMemory().with_claim(clear_claim).with_claim(blocked_claim)

    assert len(memory.claims) == 2
    assert memory.claims[0].claim_id == ClaimId("claim-clear-b")
    assert memory.claims[0].confidence == 0.7
    assert memory.claims[1].claim_id == ClaimId("claim-blocked-a")
    assert memory.claims[1].confidence == 0.8


def test_mark_stale_claims_uses_supplied_timestamp_and_preserves_original_memory() -> None:
    active_expired = _claim(
        claim_id=ClaimId("claim-active-expired"),
        status=ClaimStatus.ACTIVE,
        valid_until=VALID_UNTIL,
    )
    conflicted_expired = _claim(
        claim_id=ClaimId("claim-conflicted-expired"),
        status=ClaimStatus.CONFLICTED,
        valid_until=VALID_UNTIL,
    )
    rejected_expired = _claim(
        claim_id=ClaimId("claim-rejected-expired"),
        status=ClaimStatus.REJECTED,
        valid_until=VALID_UNTIL,
    )
    active_without_expiry = _claim(
        claim_id=ClaimId("claim-active-open"),
        status=ClaimStatus.ACTIVE,
        valid_until=None,
    )
    not_yet_expired = _claim(
        claim_id=ClaimId("claim-active-fresh"),
        status=ClaimStatus.ACTIVE,
        valid_until=Timestamp(5_000_000_000),
    )
    memory = BeliefProvenanceMemory(
        claims=(
            active_expired,
            conflicted_expired,
            rejected_expired,
            active_without_expiry,
            not_yet_expired,
        )
    )

    stale_memory = mark_stale_claims(memory, now=Timestamp(4_000_000_000))

    assert stale_memory is not memory
    assert [claim.status for claim in memory.claims] == [
        ClaimStatus.ACTIVE,
        ClaimStatus.CONFLICTED,
        ClaimStatus.REJECTED,
        ClaimStatus.ACTIVE,
        ClaimStatus.ACTIVE,
    ]
    assert [claim.status for claim in stale_memory.claims] == [
        ClaimStatus.STALE,
        ClaimStatus.STALE,
        ClaimStatus.REJECTED,
        ClaimStatus.ACTIVE,
        ClaimStatus.ACTIVE,
    ]
    assert [claim.claim_id for claim in stale_memory.claims] == [
        claim.claim_id for claim in memory.claims
    ]


def _contradictory_claims() -> tuple[Claim, Claim]:
    blocked = _claim(
        claim_id=ClaimId("claim-blocked-a"),
        value="false",
        confidence=0.8,
        source=_source(SourceId("robot-a")),
        status=ClaimStatus.CONFLICTED,
        conflicts_with=(ClaimId("claim-clear-b"),),
    )
    clear = _claim(
        claim_id=ClaimId("claim-clear-b"),
        value="true",
        confidence=0.7,
        source=_source(SourceId("robot-b")),
        status=ClaimStatus.CONFLICTED,
        conflicts_with=(ClaimId("claim-blocked-a"),),
    )
    return blocked, clear


def _claim(
    *,
    claim_id: ClaimId = ClaimId("claim-blocked-a"),
    subject: str = "edge:kitchen->hall",
    predicate: str = "traversable",
    value: str = "false",
    source: SourceMetadata | None = None,
    confidence: float = 0.8,
    status: ClaimStatus = ClaimStatus.ACTIVE,
    created_at: Timestamp = CREATED_AT,
    observed_at: Timestamp | None = OBSERVED_AT,
    valid_until: Timestamp | None = VALID_UNTIL,
    evidence: tuple[EvidenceReference, ...] = (),
    conflicts_with: tuple[ClaimId, ...] = (),
) -> Claim:
    return Claim(
        claim_id=claim_id,
        subject=subject,
        predicate=predicate,
        value=value,
        source=source or _source(SourceId("robot-a")),
        confidence=confidence,
        status=status,
        created_at=created_at,
        observed_at=observed_at,
        valid_until=valid_until,
        evidence=evidence,
        conflicts_with=conflicts_with,
    )


def _source(source_id: SourceId) -> SourceMetadata:
    return SourceMetadata(
        source_id=source_id,
        family=QueryFamily.BELIEF_PROVENANCE,
        metadata={"platform": str(source_id)},
    )


def _evidence() -> EvidenceReference:
    return EvidenceReference(
        evidence_id=EvidenceId("evidence-blocked-a"),
        kind=EvidenceKind.OBSERVATION,
        uri="mosaic://evidence/blocked-a",
    )
