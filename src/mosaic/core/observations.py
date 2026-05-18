from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Mapping

from mosaic.core.cameras import CameraIntrinsics
from mosaic.core.frames import Timestamp
from mosaic.core.poses import Pose3


class ImageEncoding(StrEnum):
    RGB8 = "rgb8"
    DEPTH_F32 = "depth_f32"


@dataclass(frozen=True, slots=True)
class ImageBuffer:
    width: int
    height: int
    channels: int
    encoding: ImageEncoding
    data: bytes

    def __post_init__(self) -> None:
        if self.width <= 0:
            raise ValueError("ImageBuffer width must be positive")
        if self.height <= 0:
            raise ValueError("ImageBuffer height must be positive")
        if self.channels <= 0:
            raise ValueError("ImageBuffer channels must be positive")
        bytes_per_channel = 4 if self.encoding is ImageEncoding.DEPTH_F32 else 1
        expected_length = self.width * self.height * self.channels * bytes_per_channel
        if len(self.data) != expected_length:
            raise ValueError("ImageBuffer data length does not match dimensions")


@dataclass(frozen=True, slots=True)
class CameraObservation:
    camera_id: str
    timestamp: Timestamp
    camera_pose: Pose3
    intrinsics: CameraIntrinsics
    color: ImageBuffer | None = None
    depth: ImageBuffer | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.camera_id.strip():
            raise ValueError("CameraObservation camera_id must not be blank")
        if self.color is None and self.depth is None:
            raise ValueError("CameraObservation requires color or depth data")
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


@dataclass(frozen=True, slots=True)
class MultiViewObservation:
    timestamp: Timestamp
    views: tuple[CameraObservation, ...]

    def __post_init__(self) -> None:
        if not self.views:
            raise ValueError("MultiViewObservation requires at least one camera view")
        for view in self.views:
            if view.timestamp != self.timestamp:
                raise ValueError("All camera views must share the same timestamp")
        camera_ids = [view.camera_id for view in self.views]
        if len(camera_ids) != len(set(camera_ids)):
            raise ValueError("MultiViewObservation camera_ids must be unique")

    @property
    def camera_ids(self) -> tuple[str, ...]:
        return tuple(view.camera_id for view in self.views)
