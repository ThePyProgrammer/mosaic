from __future__ import annotations

import base64
from typing import cast

from mosaic.artifacts.schema import ArtifactDict, make_artifact, require_artifact
from mosaic.core import (
    CameraIntrinsics,
    CameraObservation,
    FrameId,
    ImageBuffer,
    ImageEncoding,
    MultiViewObservation,
    Pose3,
    Quaternion,
    Timestamp,
    Translation3,
)


def timestamp_to_artifact(timestamp: Timestamp) -> ArtifactDict:
    return make_artifact("mosaic.timestamp", {"nanoseconds": timestamp.nanoseconds})


def timestamp_from_artifact(artifact: object) -> Timestamp:
    payload = require_artifact(artifact, "mosaic.timestamp")
    return Timestamp(cast(int, payload["nanoseconds"]))


def frame_id_to_artifact(frame_id: FrameId) -> ArtifactDict:
    return make_artifact("mosaic.frame_id", {"value": frame_id.value})


def frame_id_from_artifact(artifact: object) -> FrameId:
    payload = require_artifact(artifact, "mosaic.frame_id")
    return FrameId(cast(str, payload["value"]))


def translation3_to_artifact(translation: Translation3) -> ArtifactDict:
    return make_artifact("mosaic.translation3", {"xyz": list(translation.as_tuple())})


def translation3_from_artifact(artifact: object) -> Translation3:
    payload = require_artifact(artifact, "mosaic.translation3")
    return Translation3(*cast(list[float], payload["xyz"]))


def quaternion_to_artifact(quaternion: Quaternion) -> ArtifactDict:
    return make_artifact("mosaic.quaternion", {"wxyz": list(quaternion.as_tuple())})


def quaternion_from_artifact(artifact: object) -> Quaternion:
    payload = require_artifact(artifact, "mosaic.quaternion")
    return Quaternion(*cast(list[float], payload["wxyz"]))


def pose3_to_artifact(pose: Pose3) -> ArtifactDict:
    return make_artifact(
        "mosaic.pose3",
        {
            "parent_frame": pose.parent_frame.value,
            "child_frame": pose.child_frame.value,
            "translation": list(pose.translation.as_tuple()),
            "rotation_wxyz": list(pose.rotation.as_tuple()),
        },
    )


def pose3_from_artifact(artifact: object) -> Pose3:
    payload = require_artifact(artifact, "mosaic.pose3")
    return Pose3(
        parent_frame=FrameId(cast(str, payload["parent_frame"])),
        child_frame=FrameId(cast(str, payload["child_frame"])),
        translation=Translation3(*cast(list[float], payload["translation"])),
        rotation=Quaternion(*cast(list[float], payload["rotation_wxyz"])),
    )


def camera_intrinsics_to_artifact(intrinsics: CameraIntrinsics) -> ArtifactDict:
    return make_artifact(
        "mosaic.camera_intrinsics",
        {
            "width": intrinsics.width,
            "height": intrinsics.height,
            "fx": intrinsics.fx,
            "fy": intrinsics.fy,
            "cx": intrinsics.cx,
            "cy": intrinsics.cy,
        },
    )


def camera_intrinsics_from_artifact(artifact: object) -> CameraIntrinsics:
    payload = require_artifact(artifact, "mosaic.camera_intrinsics")
    return CameraIntrinsics(
        width=cast(int, payload["width"]),
        height=cast(int, payload["height"]),
        fx=cast(float, payload["fx"]),
        fy=cast(float, payload["fy"]),
        cx=cast(float, payload["cx"]),
        cy=cast(float, payload["cy"]),
    )


def image_buffer_to_artifact(image: ImageBuffer) -> ArtifactDict:
    return make_artifact(
        "mosaic.image_buffer",
        {
            "width": image.width,
            "height": image.height,
            "channels": image.channels,
            "encoding": image.encoding.value,
            "data_encoding": "base64",
            "data": base64.b64encode(image.data).decode("ascii"),
        },
    )


def image_buffer_from_artifact(artifact: object) -> ImageBuffer:
    payload = require_artifact(artifact, "mosaic.image_buffer")
    data_encoding = payload["data_encoding"]
    if data_encoding != "base64":
        raise ValueError("ImageBuffer artifact data_encoding must be base64")
    return ImageBuffer(
        width=cast(int, payload["width"]),
        height=cast(int, payload["height"]),
        channels=cast(int, payload["channels"]),
        encoding=ImageEncoding(cast(str, payload["encoding"])),
        data=base64.b64decode(cast(str, payload["data"])),
    )


def camera_observation_to_artifact(observation: CameraObservation) -> ArtifactDict:
    return make_artifact(
        "mosaic.camera_observation",
        {
            "camera_id": observation.camera_id,
            "timestamp": timestamp_to_artifact(observation.timestamp),
            "camera_pose": pose3_to_artifact(observation.camera_pose),
            "intrinsics": camera_intrinsics_to_artifact(observation.intrinsics),
            "color": image_buffer_to_artifact(observation.color) if observation.color is not None else None,
            "depth": image_buffer_to_artifact(observation.depth) if observation.depth is not None else None,
            "metadata": dict(observation.metadata),
        },
    )


def camera_observation_from_artifact(artifact: object) -> CameraObservation:
    payload = require_artifact(artifact, "mosaic.camera_observation")
    color = payload["color"]
    depth = payload["depth"]
    return CameraObservation(
        camera_id=cast(str, payload["camera_id"]),
        timestamp=timestamp_from_artifact(payload["timestamp"]),
        camera_pose=pose3_from_artifact(payload["camera_pose"]),
        intrinsics=camera_intrinsics_from_artifact(payload["intrinsics"]),
        color=image_buffer_from_artifact(color) if color is not None else None,
        depth=image_buffer_from_artifact(depth) if depth is not None else None,
        metadata=cast(dict[str, str], payload["metadata"]),
    )


def multiview_observation_to_artifact(observation: MultiViewObservation) -> ArtifactDict:
    return make_artifact(
        "mosaic.multiview_observation",
        {
            "timestamp": timestamp_to_artifact(observation.timestamp),
            "camera_ids": list(observation.camera_ids),
            "views": [camera_observation_to_artifact(view) for view in observation.views],
        },
    )


def multiview_observation_from_artifact(artifact: object) -> MultiViewObservation:
    payload = require_artifact(artifact, "mosaic.multiview_observation")
    return MultiViewObservation(
        timestamp=timestamp_from_artifact(payload["timestamp"]),
        views=tuple(camera_observation_from_artifact(view) for view in cast(list[object], payload["views"])),
    )
