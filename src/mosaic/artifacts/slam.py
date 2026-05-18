from __future__ import annotations

from typing import cast

from mosaic.artifacts.core import pose3_from_artifact, pose3_to_artifact, timestamp_from_artifact, timestamp_to_artifact
from mosaic.artifacts.schema import ArtifactDict, make_artifact, require_artifact
from mosaic.artifacts.splats import splat_map_from_artifact, splat_map_to_artifact
from mosaic.slam import SplatSlamUpdate, TrackingState
from mosaic.slam.protocol import MetricValue


def splat_slam_update_to_artifact(update: SplatSlamUpdate) -> ArtifactDict:
    return make_artifact(
        "mosaic.splat_slam_update",
        {
            "timestamp": timestamp_to_artifact(update.timestamp),
            "tracking_state": update.tracking_state.value,
            "estimated_pose": pose3_to_artifact(update.estimated_pose) if update.estimated_pose is not None else None,
            "map_update": splat_map_to_artifact(update.map_update),
            "diagnostics": dict(update.diagnostics),
        },
    )


def splat_slam_update_from_artifact(artifact: object) -> SplatSlamUpdate:
    payload = require_artifact(artifact, "mosaic.splat_slam_update")
    estimated_pose = payload["estimated_pose"]
    return SplatSlamUpdate(
        timestamp=timestamp_from_artifact(payload["timestamp"]),
        tracking_state=TrackingState(cast(str, payload["tracking_state"])),
        estimated_pose=pose3_from_artifact(estimated_pose) if estimated_pose is not None else None,
        map_update=splat_map_from_artifact(payload["map_update"]),
        diagnostics=cast(dict[str, MetricValue], payload["diagnostics"]),
    )
