from types import MappingProxyType

import pytest

from mosaic.core import FrameId, Pose3, Quaternion, Translation3
from mosaic.slam import (
    LOOP_DETECTION_MODEL,
    AgentId,
    DeterministicLoopClosureStrategy,
    GaussianSubmap,
    LoopCandidate,
    LoopClosureResult,
    LoopEdge,
    LoopId,
    LoopValidationStatus,
    SessionId,
    SubmapId,
    SubmapReference,
)
from mosaic.splats import SplatMap


def _reference(agent: str = "agent-1", session: str = "session-1", submap: str = "submap-1") -> SubmapReference:
    return SubmapReference(
        agent_id=AgentId(agent),
        session_id=SessionId(session),
        submap_id=SubmapId(submap),
    )


def _submap(
    *,
    agent: str = "agent-1",
    session: str = "session-1",
    submap: str = "submap-1",
    map_frame: str = "map",
    anchor: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> GaussianSubmap:
    reference = _reference(agent=agent, session=session, submap=submap)
    local_frame = FrameId(f"{agent}/{session}/{submap}/local")
    world_frame = FrameId(map_frame)
    return GaussianSubmap(
        reference=reference,
        local_frame=local_frame,
        map_frame=world_frame,
        local_to_map=Pose3(
            parent_frame=world_frame,
            child_frame=local_frame,
            translation=Translation3(*anchor),
            rotation=Quaternion.identity(),
        ),
        splat_map=SplatMap(frame=local_frame),
    )


def _relative_pose() -> Pose3:
    return Pose3(
        parent_frame=FrameId("source-local"),
        child_frame=FrameId("target-local"),
        translation=Translation3(),
        rotation=Quaternion.identity(),
    )


def test_loop_candidate_rejects_same_submap_and_freezes_diagnostics() -> None:
    reference = _reference()

    with pytest.raises(ValueError, match="different submaps"):
        LoopCandidate(
            loop_id=LoopId("loop-1"),
            source=reference,
            target=reference,
            score=0.0,
            confidence=1.0,
        )

    candidate = LoopCandidate(
        loop_id=LoopId("loop-1"),
        source=reference,
        target=_reference(agent="agent-2"),
        score=0.25,
        confidence=0.5,
        diagnostics={"anchor_distance": 0.25},
    )

    assert isinstance(candidate.diagnostics, MappingProxyType)
    assert candidate.diagnostics["anchor_distance"] == 0.25


def test_loop_edge_rejects_same_submap_and_candidate_status() -> None:
    reference = _reference()

    with pytest.raises(ValueError, match="different submaps"):
        LoopEdge(
            loop_id=LoopId("loop-1"),
            source=reference,
            target=reference,
            relative_pose=_relative_pose(),
            confidence=1.0,
            status=LoopValidationStatus.ACCEPTED,
        )

    with pytest.raises(ValueError, match="accepted or rejected"):
        LoopEdge(
            loop_id=LoopId("loop-1"),
            source=reference,
            target=_reference(agent="agent-2"),
            relative_pose=_relative_pose(),
            confidence=1.0,
            status=LoopValidationStatus.CANDIDATE,
        )


def test_deterministic_cross_agent_overlap_produces_candidate_and_accepted_edge() -> None:
    source = _submap(agent="agent-1", submap="source", anchor=(1.0, 0.0, 0.0))
    target = _submap(agent="agent-2", submap="target", anchor=(1.25, 0.0, 0.0))

    result = DeterministicLoopClosureStrategy(max_anchor_distance=0.5, min_confidence=0.1).detect((source, target))

    assert len(result.candidates) == 1
    assert len(result.edges) == 1
    assert result.diagnostics == {
        "loop_detection_model": LOOP_DETECTION_MODEL,
        "candidate_count": 1,
        "edge_count": 1,
    }

    candidate = result.candidates[0]
    assert candidate.loop_id == LoopId("loop-1")
    assert candidate.source == source.reference
    assert candidate.target == target.reference
    assert candidate.score == pytest.approx(0.25)
    assert candidate.confidence == pytest.approx(0.5)
    assert candidate.diagnostics["anchor_distance"] == pytest.approx(0.25)
    assert candidate.diagnostics["loop_detection_model"] == LOOP_DETECTION_MODEL

    edge = result.edges[0]
    assert edge.loop_id == candidate.loop_id
    assert edge.status is LoopValidationStatus.ACCEPTED
    assert edge.confidence == pytest.approx(0.5)
    assert edge.relative_pose.parent_frame == source.local_frame
    assert edge.relative_pose.child_frame == target.local_frame
    assert edge.relative_pose.translation.as_tuple() == pytest.approx((-0.25, 0.0, 0.0))
    assert edge.relative_pose.rotation == Quaternion.identity()


def test_same_agent_far_and_different_frame_submaps_are_ignored() -> None:
    source = _submap(agent="agent-1", submap="source", anchor=(0.0, 0.0, 0.0))
    same_agent = _submap(agent="agent-1", submap="same-agent", anchor=(0.1, 0.0, 0.0))
    far = _submap(agent="agent-2", submap="far", anchor=(2.0, 0.0, 0.0))
    different_frame = _submap(agent="agent-3", submap="different-frame", map_frame="other-map", anchor=(0.1, 0.0, 0.0))

    result = DeterministicLoopClosureStrategy(max_anchor_distance=0.5, min_confidence=0.1).detect(
        (source, same_agent, far, different_frame)
    )

    assert result.candidates == ()
    assert result.edges == ()
    assert result.diagnostics["candidate_count"] == 0
    assert result.diagnostics["edge_count"] == 0


def test_low_confidence_overlap_produces_rejected_edge_without_accepted_edges() -> None:
    source = _submap(agent="agent-1", submap="source", anchor=(0.0, 0.0, 0.0))
    target = _submap(agent="agent-2", submap="target", anchor=(0.48, 0.0, 0.0))

    result = DeterministicLoopClosureStrategy(max_anchor_distance=0.5, min_confidence=0.1).detect((source, target))

    assert len(result.candidates) == 1
    assert [edge for edge in result.edges if edge.status is LoopValidationStatus.ACCEPTED] == []
    assert result.edges[0].status is LoopValidationStatus.REJECTED


@pytest.mark.parametrize("score", (-0.1, float("nan")))
def test_loop_candidate_validates_score_range(score: float) -> None:
    with pytest.raises(ValueError, match="score"):
        LoopCandidate(
            loop_id=LoopId("loop-1"),
            source=_reference(agent="agent-1"),
            target=_reference(agent="agent-2"),
            score=score,
            confidence=1.0,
        )


@pytest.mark.parametrize("confidence", (-0.1, 1.1, float("nan")))
def test_loop_contracts_validate_confidence_ranges(confidence: float) -> None:
    with pytest.raises(ValueError, match="confidence"):
        LoopCandidate(
            loop_id=LoopId("loop-1"),
            source=_reference(agent="agent-1"),
            target=_reference(agent="agent-2"),
            score=0.0,
            confidence=confidence,
        )

    with pytest.raises(ValueError, match="confidence"):
        LoopEdge(
            loop_id=LoopId("loop-1"),
            source=_reference(agent="agent-1"),
            target=_reference(agent="agent-2"),
            relative_pose=_relative_pose(),
            confidence=confidence,
            status=LoopValidationStatus.ACCEPTED,
        )


@pytest.mark.parametrize(
    ("max_anchor_distance", "min_confidence"),
    ((0.0, 0.1), (float("nan"), 0.1), (0.5, -0.1), (0.5, 1.1), (0.5, float("nan"))),
)
def test_strategy_validates_configuration(max_anchor_distance: float, min_confidence: float) -> None:
    with pytest.raises(ValueError):
        DeterministicLoopClosureStrategy(
            max_anchor_distance=max_anchor_distance,
            min_confidence=min_confidence,
        )


def test_loop_closure_result_freezes_tuple_fields_and_validates_diagnostics() -> None:
    result = LoopClosureResult(candidates=[], edges=[], diagnostics={"model": LOOP_DETECTION_MODEL})  # type: ignore[arg-type]

    assert result.candidates == ()
    assert result.edges == ()
    assert isinstance(result.diagnostics, MappingProxyType)

    with pytest.raises(ValueError, match="non-blank string keys"):
        LoopClosureResult(diagnostics={"": 1})

    with pytest.raises(ValueError, match="JSON-ready scalar values"):
        LoopClosureResult(diagnostics={"nested": {"not": "scalar"}})  # type: ignore[dict-item]

    with pytest.raises(ValueError, match="float values must be finite"):
        LoopClosureResult(diagnostics={"distance": float("inf")})
