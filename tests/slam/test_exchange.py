from types import MappingProxyType

import pytest

from mosaic.core import FrameId, Pose3, Quaternion, Timestamp, Translation3
from mosaic.slam import (
    AgentId,
    ExchangePolicy,
    GaussianSubmap,
    KeyframeExchangeMessage,
    SessionId,
    SubmapExchangeMessage,
    SubmapId,
    SubmapReference,
)
from mosaic.splats import SplatMap


def _reference(
    *,
    agent_id: AgentId | None = None,
    session_id: SessionId | None = None,
    submap_id: SubmapId | None = None,
) -> SubmapReference:
    return SubmapReference(
        agent_id=agent_id or AgentId("agent-1"),
        session_id=session_id or SessionId("session-1"),
        submap_id=submap_id or SubmapId("submap-1"),
    )


def _submap(*, reference: SubmapReference | None = None) -> GaussianSubmap:
    local = FrameId("agent-1/session-1/submap-1/local")
    world = FrameId("map")
    return GaussianSubmap(
        reference=reference or _reference(),
        local_frame=local,
        map_frame=world,
        local_to_map=Pose3(
            parent_frame=world,
            child_frame=local,
            translation=Translation3(),
            rotation=Quaternion.identity(),
        ),
        splat_map=SplatMap(frame=local),
    )


def test_submap_exchange_message_accepts_valid_submap_and_freezes_diagnostics() -> None:
    message = SubmapExchangeMessage(
        sender=AgentId("agent-1"),
        sequence_number=1,
        timestamp=Timestamp(10),
        submap=_submap(),
        receiver=AgentId("agent-2"),
        diagnostics={"accepted": True, "quality": 1.0, "source": "synthetic"},
    )

    assert message.policy is ExchangePolicy.SUBMAP_ONLY
    assert message.submap.agent_id == message.sender
    assert isinstance(message.diagnostics, MappingProxyType)
    assert message.diagnostics["accepted"] is True


def test_submap_exchange_message_rejects_sender_mismatch() -> None:
    with pytest.raises(ValueError, match="sender must match submap agent_id"):
        SubmapExchangeMessage(
            sender=AgentId("agent-2"),
            sequence_number=1,
            timestamp=Timestamp(10),
            submap=_submap(),
        )


def test_submap_exchange_message_rejects_non_submap_payload() -> None:
    with pytest.raises(ValueError, match="submap must be a GaussianSubmap"):
        SubmapExchangeMessage(
            sender=AgentId("agent-1"),
            sequence_number=1,
            timestamp=Timestamp(10),
            submap={},  # type: ignore[arg-type]
        )


def test_submap_exchange_message_rejects_negative_sequence_number() -> None:
    with pytest.raises(ValueError, match="sequence_number must be non-negative"):
        SubmapExchangeMessage(
            sender=AgentId("agent-1"),
            sequence_number=-1,
            timestamp=Timestamp(10),
            submap=_submap(),
        )


def test_submap_exchange_message_rejects_non_submap_policy() -> None:
    with pytest.raises(ValueError, match="policy must be SUBMAP_ONLY"):
        SubmapExchangeMessage(
            sender=AgentId("agent-1"),
            sequence_number=1,
            timestamp=Timestamp(10),
            submap=_submap(),
            policy=ExchangePolicy.MIXED,
        )


def test_keyframe_exchange_message_accepts_valid_keyframe_and_freezes_diagnostics() -> None:
    reference = _reference()
    message = KeyframeExchangeMessage(
        sender=AgentId("agent-1"),
        session_id=SessionId("session-1"),
        keyframe_id="keyframe-1",
        timestamp=Timestamp(20),
        camera_ids=("front", "left"),
        submap_reference=reference,
        receiver=AgentId("agent-2"),
        diagnostics={"tracked": True, "feature_count": 4},
    )

    assert message.policy is ExchangePolicy.KEYFRAME_ONLY
    assert message.camera_ids == ("front", "left")
    assert message.submap_reference == reference
    assert isinstance(message.diagnostics, MappingProxyType)


@pytest.mark.parametrize("camera_ids", (("front", "front"), ("front", "  ")))
def test_keyframe_exchange_message_rejects_duplicate_or_blank_camera_ids(camera_ids: tuple[str, ...]) -> None:
    with pytest.raises(ValueError, match="camera_ids"):
        KeyframeExchangeMessage(
            sender=AgentId("agent-1"),
            session_id=SessionId("session-1"),
            keyframe_id="keyframe-1",
            timestamp=Timestamp(20),
            camera_ids=camera_ids,
        )


def test_keyframe_exchange_message_rejects_non_tuple_camera_ids() -> None:
    with pytest.raises(ValueError, match="camera_ids must be a tuple"):
        KeyframeExchangeMessage(
            sender=AgentId("agent-1"),
            session_id=SessionId("session-1"),
            keyframe_id="keyframe-1",
            timestamp=Timestamp(20),
            camera_ids=["front"],  # type: ignore[arg-type]
        )


def test_keyframe_exchange_message_rejects_invalid_submap_reference_payload() -> None:
    with pytest.raises(ValueError, match="submap_reference must be a SubmapReference"):
        KeyframeExchangeMessage(
            sender=AgentId("agent-1"),
            session_id=SessionId("session-1"),
            keyframe_id="keyframe-1",
            timestamp=Timestamp(20),
            camera_ids=("front",),
            submap_reference={},  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    "reference, error_match",
    (
        (_reference(agent_id=AgentId("agent-2")), "sender must match submap_reference agent_id"),
        (_reference(session_id=SessionId("session-2")), "session_id must match submap_reference session_id"),
    ),
)
def test_keyframe_exchange_message_rejects_submap_reference_sender_or_session_mismatch(
    reference: SubmapReference,
    error_match: str,
) -> None:
    with pytest.raises(ValueError, match=error_match):
        KeyframeExchangeMessage(
            sender=AgentId("agent-1"),
            session_id=SessionId("session-1"),
            keyframe_id="keyframe-1",
            timestamp=Timestamp(20),
            camera_ids=("front",),
            submap_reference=reference,
        )


@pytest.mark.parametrize(
    "diagnostics, error_match",
    (
        ({"": 1}, "non-blank string keys"),
        ({"nested": {"not": "scalar"}}, "JSON-ready scalar values"),
        ({"rmse": float("inf")}, "float values must be finite"),
    ),
)
def test_exchange_messages_reject_invalid_diagnostics(diagnostics: dict[str, object], error_match: str) -> None:
    with pytest.raises(ValueError, match=error_match):
        SubmapExchangeMessage(
            sender=AgentId("agent-1"),
            sequence_number=1,
            timestamp=Timestamp(10),
            submap=_submap(),
            diagnostics=diagnostics,  # type: ignore[arg-type]
        )

    with pytest.raises(ValueError, match=error_match):
        KeyframeExchangeMessage(
            sender=AgentId("agent-1"),
            session_id=SessionId("session-1"),
            keyframe_id="keyframe-1",
            timestamp=Timestamp(20),
            camera_ids=("front",),
            diagnostics=diagnostics,  # type: ignore[arg-type]
        )
