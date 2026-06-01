from types import MappingProxyType

import pytest

from mosaic.core import FrameId, Pose3, Quaternion, Timestamp, Translation3
from mosaic.slam import (
    AgentId,
    GaussianSubmap,
    LoopId,
    PoseGraphNodeId,
    SessionId,
    SubmapId,
    SubmapLifecycleState,
    SubmapReference,
)
from mosaic.splats import SplatMap


def _reference() -> SubmapReference:
    return SubmapReference(
        agent_id=AgentId("agent-1"),
        session_id=SessionId("session-1"),
        submap_id=SubmapId("submap-1"),
    )


def _pose(
    *,
    parent_frame: FrameId | None = None,
    child_frame: FrameId | None = None,
    x: float = 0.0,
) -> Pose3:
    return Pose3(
        parent_frame=parent_frame or FrameId("map"),
        child_frame=child_frame or FrameId("agent-1/session-1/submap-1/local"),
        translation=Translation3(x=x, y=0.0, z=0.0),
        rotation=Quaternion.identity(),
    )


def _submap(
    *,
    local_frame: FrameId | None = None,
    map_frame: FrameId | None = None,
    local_to_map: Pose3 | None = None,
    splat_map: SplatMap | None = None,
    first_timestamp: Timestamp | None = Timestamp(10),
    last_timestamp: Timestamp | None = Timestamp(20),
    state: SubmapLifecycleState = SubmapLifecycleState.ACTIVE,
    diagnostics: dict[str, object] | None = None,
) -> GaussianSubmap:
    local = local_frame or FrameId("agent-1/session-1/submap-1/local")
    world = map_frame or FrameId("map")
    return GaussianSubmap(
        reference=_reference(),
        local_frame=local,
        map_frame=world,
        local_to_map=local_to_map or _pose(parent_frame=world, child_frame=local),
        splat_map=splat_map if splat_map is not None else SplatMap(frame=local),
        state=state,
        first_timestamp=first_timestamp,
        last_timestamp=last_timestamp,
        diagnostics=diagnostics if diagnostics is not None else {"source": "synthetic", "splat_count": 0},
    )


@pytest.mark.parametrize(
    "identity_type",
    (AgentId, SessionId, SubmapId, LoopId, PoseGraphNodeId),
)
def test_identity_classes_reject_blank_values(identity_type: type[AgentId | SessionId | SubmapId | LoopId | PoseGraphNodeId]) -> None:
    with pytest.raises(ValueError, match=f"{identity_type.__name__} value must not be blank"):
        identity_type("  ")


def test_submap_reference_formats_as_stable_pose_graph_node_id() -> None:
    reference = _reference()

    assert str(reference) == "agent-1/session-1/submap-1"
    assert reference.node_id == PoseGraphNodeId("agent-1/session-1/submap-1")
    assert str(reference.node_id) == "agent-1/session-1/submap-1"


@pytest.mark.parametrize("identity_type", (AgentId, SessionId, SubmapId, LoopId))
def test_submap_reference_identity_parts_reject_slashes(identity_type: type[AgentId | SessionId | SubmapId | LoopId]) -> None:
    with pytest.raises(ValueError, match="must not contain"):
        identity_type("part/with/slash")


def test_pose_graph_node_id_rejects_empty_slash_segments() -> None:
    with pytest.raises(ValueError, match="segments must not be blank"):
        PoseGraphNodeId("agent-1//submap-1")


def test_gaussian_submap_exposes_reference_state_anchor_and_frozen_diagnostics() -> None:
    submap = _submap()

    assert submap.agent_id == AgentId("agent-1")
    assert submap.session_id == SessionId("session-1")
    assert submap.submap_id == SubmapId("submap-1")
    assert submap.node_id == PoseGraphNodeId("agent-1/session-1/submap-1")
    assert submap.state is SubmapLifecycleState.ACTIVE
    assert submap.anchor == (0.0, 0.0, 0.0)
    assert isinstance(submap.diagnostics, MappingProxyType)
    assert submap.diagnostics["source"] == "synthetic"

    updated_pose = _pose(parent_frame=submap.map_frame, child_frame=submap.local_frame, x=1.0)
    moved = submap.with_pose(updated_pose)

    assert moved.local_to_map == updated_pose
    assert moved.reference == submap.reference
    assert moved.splat_map == submap.splat_map
    assert moved.diagnostics == submap.diagnostics
    assert submap.local_to_map != updated_pose


def test_gaussian_submap_rejects_splat_map_frame_mismatch() -> None:
    with pytest.raises(ValueError, match="splat_map frame must match local_frame"):
        _submap(splat_map=SplatMap(frame=FrameId("other-local")))


@pytest.mark.parametrize(
    "local_to_map",
    (
        _pose(parent_frame=FrameId("other-map"), child_frame=FrameId("agent-1/session-1/submap-1/local")),
        _pose(parent_frame=FrameId("map"), child_frame=FrameId("other-local")),
    ),
)
def test_gaussian_submap_rejects_pose_frame_mismatch(local_to_map: Pose3) -> None:
    with pytest.raises(ValueError, match="local_to_map frames"):
        _submap(local_to_map=local_to_map)


def test_gaussian_submap_rejects_timestamp_bounds() -> None:
    with pytest.raises(ValueError, match="first_timestamp"):
        _submap(first_timestamp=Timestamp(20), last_timestamp=Timestamp(10))

    with pytest.raises(ValueError, match="first_timestamp must be a Timestamp"):
        _submap(first_timestamp=10)  # type: ignore[arg-type]

    with pytest.raises(ValueError, match="last_timestamp must be a Timestamp"):
        _submap(last_timestamp=20)  # type: ignore[arg-type]


def test_gaussian_submap_rejects_invalid_state_and_diagnostics() -> None:
    with pytest.raises(ValueError, match="state must be a SubmapLifecycleState"):
        _submap(state="active")  # type: ignore[arg-type]

    with pytest.raises(ValueError, match="non-blank string keys"):
        _submap(diagnostics={"": 1})

    with pytest.raises(ValueError, match="JSON-ready scalar values"):
        _submap(diagnostics={"nested": {"not": "scalar"}})  # type: ignore[dict-item]

    with pytest.raises(ValueError, match="float values must be finite"):
        _submap(diagnostics={"rmse": float("nan")})
