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

    def conjugate(self) -> Self:
        return type(self)(w=self.w, x=-self.x, y=-self.y, z=-self.z)

    def multiply(self, other: Quaternion) -> Self:
        return type(self)(
            w=(self.w * other.w) - (self.x * other.x) - (self.y * other.y) - (self.z * other.z),
            x=(self.w * other.x) + (self.x * other.w) + (self.y * other.z) - (self.z * other.y),
            y=(self.w * other.y) - (self.x * other.z) + (self.y * other.w) + (self.z * other.x),
            z=(self.w * other.z) + (self.x * other.y) - (self.y * other.x) + (self.z * other.w),
        )

    def rotate_point(self, point: tuple[float, float, float]) -> tuple[float, float, float]:
        point_quaternion = _QuaternionProduct(w=0.0, x=point[0], y=point[1], z=point[2])
        rotated = self._multiply_raw(point_quaternion)._multiply_raw(self.conjugate())
        return (rotated.x, rotated.y, rotated.z)

    def _multiply_raw(self, other: _QuaternionLike) -> _QuaternionProduct:
        return _QuaternionProduct(
            w=(self.w * other.w) - (self.x * other.x) - (self.y * other.y) - (self.z * other.z),
            x=(self.w * other.x) + (self.x * other.w) + (self.y * other.z) - (self.z * other.y),
            y=(self.w * other.y) - (self.x * other.z) + (self.y * other.w) + (self.z * other.x),
            z=(self.w * other.z) + (self.x * other.y) - (self.y * other.x) + (self.z * other.w),
        )


@dataclass(frozen=True, slots=True)
class _QuaternionProduct:
    w: float
    x: float
    y: float
    z: float

    def _multiply_raw(self, other: _QuaternionLike) -> _QuaternionProduct:
        return _QuaternionProduct(
            w=(self.w * other.w) - (self.x * other.x) - (self.y * other.y) - (self.z * other.z),
            x=(self.w * other.x) + (self.x * other.w) + (self.y * other.z) - (self.z * other.y),
            y=(self.w * other.y) - (self.x * other.z) + (self.y * other.w) + (self.z * other.x),
            z=(self.w * other.z) + (self.x * other.y) - (self.y * other.x) + (self.z * other.w),
        )


_QuaternionLike = Quaternion | _QuaternionProduct


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

    def inverse(self) -> Self:
        inverse_rotation = self.rotation.conjugate()
        inverse_translation_tuple = inverse_rotation.rotate_point(
            (-self.translation.x, -self.translation.y, -self.translation.z)
        )
        return type(self)(
            parent_frame=self.child_frame,
            child_frame=self.parent_frame,
            translation=Translation3(*inverse_translation_tuple),
            rotation=inverse_rotation,
        )

    def compose(self, other: Pose3) -> Self:
        if self.child_frame != other.parent_frame:
            raise ValueError("Cannot compose poses with incompatible frames")
        composed_translation = self.apply_to_point(other.translation.as_tuple())
        return type(self)(
            parent_frame=self.parent_frame,
            child_frame=other.child_frame,
            translation=Translation3(*composed_translation),
            rotation=self.rotation.multiply(other.rotation),
        )
