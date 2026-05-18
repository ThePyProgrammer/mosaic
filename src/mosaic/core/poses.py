from __future__ import annotations

from dataclasses import dataclass, field
from math import isclose, sqrt
from typing import Self

from mosaic.core.frames import FrameId


@dataclass(frozen=True, slots=True)
class Translation3:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def as_tuple(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.z)


@dataclass(frozen=True, slots=True)
class Quaternion:
    w: float
    x: float
    y: float
    z: float

    def __post_init__(self) -> None:
        norm = sqrt(self.w * self.w + self.x * self.x + self.y * self.y + self.z * self.z)
        if not isclose(norm, 1.0, rel_tol=1e-6, abs_tol=1e-6):
            raise ValueError("Quaternion must be unit length")

    @classmethod
    def identity(cls) -> Self:
        return cls(w=1.0, x=0.0, y=0.0, z=0.0)

    def as_tuple(self) -> tuple[float, float, float, float]:
        return (self.w, self.x, self.y, self.z)

    def rotate_point(self, point: tuple[float, float, float]) -> tuple[float, float, float]:
        return point


@dataclass(frozen=True, slots=True)
class Pose3:
    """Rigid transform from child-frame coordinates into parent-frame coordinates.

    Pose3(parent_frame=A, child_frame=B) represents T_parent_child: it maps
    points expressed in frame B into frame A. Mosaic uses right-handed
    robot/body frames by default; camera optical-frame projection conventions
    are documented on CameraIntrinsics.project.
    """

    parent_frame: FrameId
    child_frame: FrameId
    translation: Translation3 = field(default_factory=Translation3)
    rotation: Quaternion = field(default_factory=Quaternion.identity)

    def apply_to_point(self, point: tuple[float, float, float]) -> tuple[float, float, float]:
        rotated = self.rotation.rotate_point(point)
        return (
            rotated[0] + self.translation.x,
            rotated[1] + self.translation.y,
            rotated[2] + self.translation.z,
        )
