from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Pixel:
    u: float
    v: float


@dataclass(frozen=True, slots=True)
class CameraIntrinsics:
    width: int
    height: int
    fx: float
    fy: float
    cx: float
    cy: float

    def __post_init__(self) -> None:
        if self.width <= 0:
            raise ValueError("CameraIntrinsics width must be positive")
        if self.height <= 0:
            raise ValueError("CameraIntrinsics height must be positive")
        if self.fx <= 0.0 or self.fy <= 0.0:
            raise ValueError("CameraIntrinsics focal lengths must be positive")
        if not 0.0 <= self.cx <= float(self.width):
            raise ValueError("CameraIntrinsics cx must be within image width")
        if not 0.0 <= self.cy <= float(self.height):
            raise ValueError("CameraIntrinsics cy must be within image height")

    def project(self, point_camera: tuple[float, float, float]) -> Pixel:
        x, y, z = point_camera
        if z <= 0.0:
            raise ValueError("Cannot project point with non-positive depth")
        return Pixel(u=(self.fx * x / z) + self.cx, v=(self.fy * y / z) + self.cy)
