from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Mapping

from mosaic.core import CameraIntrinsics, FrameId, Pose3


class Embodiment(StrEnum):
    QUADRUPED = "quadruped"
    UGV = "ugv"
    HUMANOID = "humanoid"
    CUSTOM = "custom"


@dataclass(frozen=True, slots=True)
class CameraMount:
    camera_id: str
    pose: Pose3
    intrinsics: CameraIntrinsics
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.camera_id.strip():
            raise ValueError("CameraMount camera_id must not be blank")
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


@dataclass(frozen=True, slots=True)
class CameraRig:
    frame: FrameId
    cameras: tuple[CameraMount, ...]

    def __post_init__(self) -> None:
        if not self.cameras:
            raise ValueError("CameraRig requires at least one camera")
        camera_ids = [camera.camera_id for camera in self.cameras]
        if len(camera_ids) != len(set(camera_ids)):
            raise ValueError("CameraRig camera_id values must be unique")
        for camera in self.cameras:
            if camera.pose.parent_frame != self.frame:
                raise ValueError("CameraMount pose parent frame must match CameraRig frame")

    @property
    def camera_ids(self) -> tuple[str, ...]:
        return tuple(camera.camera_id for camera in self.cameras)

    def camera(self, camera_id: str) -> CameraMount:
        for camera in self.cameras:
            if camera.camera_id == camera_id:
                return camera
        raise KeyError(camera_id)


@dataclass(frozen=True, slots=True)
class PlatformDescription:
    name: str
    embodiment: Embodiment
    base_frame: FrameId
    camera_rig: CameraRig
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("PlatformDescription name must not be blank")
        if self.camera_rig.frame != self.base_frame:
            raise ValueError("PlatformDescription base_frame must match camera rig frame")
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))
