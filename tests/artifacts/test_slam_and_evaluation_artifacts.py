import json

import pytest

from mosaic.artifacts import splat_slam_update_from_artifact, splat_slam_update_to_artifact
from mosaic.core import FrameId, Pose3, Quaternion, Timestamp, Translation3
from mosaic.slam import SplatSlamUpdate, TrackingState
from mosaic.splats import GaussianSplat, SplatMap


def _pose() -> Pose3:
    return Pose3(
        parent_frame=FrameId("map"),
        child_frame=FrameId("camera/front"),
        translation=Translation3(x=1.0, y=2.0, z=3.0),
        rotation=Quaternion.identity(),
    )


def _splat_map() -> SplatMap:
    return SplatMap(
        frame=FrameId("map"),
        splats=(
            GaussianSplat(
                center=(0.0, 0.0, 1.0),
                covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1),
                color_rgb=(0.2, 0.3, 0.4),
                opacity=0.75,
                provenance="front-camera",
            ),
        ),
    )


def test_splat_slam_update_artifact_round_trips_tracking_update() -> None:
    update = SplatSlamUpdate(
        timestamp=Timestamp(1_000_000_000),
        tracking_state=TrackingState.TRACKING,
        estimated_pose=_pose(),
        map_update=_splat_map(),
        diagnostics={"quality": 1.0, "accepted": True, "label": "deterministic"},
    )

    artifact = splat_slam_update_to_artifact(update)
    restored = splat_slam_update_from_artifact(artifact)

    assert artifact["schema"] == "mosaic.splat_slam_update"
    assert artifact["payload"]["tracking_state"] == "tracking"
    assert restored.timestamp == update.timestamp
    assert restored.tracking_state is TrackingState.TRACKING
    assert restored.estimated_pose == update.estimated_pose
    assert restored.map_update == update.map_update
    assert restored.diagnostics == update.diagnostics
    json.dumps(artifact, sort_keys=True)


def test_splat_slam_update_artifact_round_trips_lost_update_without_pose() -> None:
    update = SplatSlamUpdate(
        timestamp=Timestamp(1_000_000_000),
        tracking_state=TrackingState.LOST,
        estimated_pose=None,
        map_update=_splat_map(),
        diagnostics={"quality": 0.0, "accepted": False, "label": "lost"},
    )

    artifact = splat_slam_update_to_artifact(update)
    restored = splat_slam_update_from_artifact(artifact)

    assert artifact["payload"]["tracking_state"] == "lost"
    assert restored.tracking_state is TrackingState.LOST
    assert restored.estimated_pose is None
    assert restored.map_update == update.map_update
    assert restored.diagnostics == update.diagnostics


def test_splat_slam_update_artifact_rejects_unknown_schema_version() -> None:
    update = SplatSlamUpdate(
        timestamp=Timestamp(1_000_000_000),
        tracking_state=TrackingState.LOST,
        estimated_pose=None,
        map_update=_splat_map(),
    )
    artifact = splat_slam_update_to_artifact(update)
    artifact["schema_version"] = 2

    with pytest.raises(ValueError, match="schema_version"):
        splat_slam_update_from_artifact(artifact)
