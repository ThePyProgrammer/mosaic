from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True, slots=True)
class GaussianSplat:
    """Gaussian primitive with covariance_upper in upper-triangular order.

    covariance_upper stores the symmetric 3x3 covariance matrix as
    (xx, xy, xz, yy, yz, zz), reconstructing rows as (xx, xy, xz),
    (xy, yy, yz), and (xz, yz, zz).
    """

    center: tuple[float, float, float]
    covariance_upper: tuple[float, float, float, float, float, float]
    color_rgb: tuple[float, float, float] = (1.0, 1.0, 1.0)
    opacity: float = 1.0
    provenance: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "center", tuple(self.center))
        object.__setattr__(self, "covariance_upper", tuple(self.covariance_upper))
        object.__setattr__(self, "color_rgb", tuple(self.color_rgb))

        if len(self.center) != 3:
            raise ValueError("GaussianSplat center must contain three coordinates")
        if len(self.covariance_upper) != 6:
            raise ValueError("GaussianSplat covariance_upper must contain six values")
        if len(self.color_rgb) != 3:
            raise ValueError("GaussianSplat color_rgb must contain three channels")
        numeric_values = (*self.center, *self.covariance_upper, *self.color_rgb, self.opacity)
        if not all(isfinite(value) for value in numeric_values):
            raise ValueError("GaussianSplat numeric values must be finite")
        xx, xy, xz, yy, yz, zz = self.covariance_upper
        if xx <= 0.0 or yy <= 0.0 or zz <= 0.0:
            raise ValueError("GaussianSplat covariance diagonal values must be positive")
        if xx * yy - xy * xy <= 0.0:
            raise ValueError("GaussianSplat covariance must be positive definite")
        determinant = (
            xx * yy * zz
            + 2.0 * xy * xz * yz
            - xx * yz * yz
            - yy * xz * xz
            - zz * xy * xy
        )
        if determinant <= 0.0:
            raise ValueError("GaussianSplat covariance must be positive definite")
        if any(channel < 0.0 or channel > 1.0 for channel in self.color_rgb):
            raise ValueError("GaussianSplat color_rgb channels must be between 0 and 1")
        if self.opacity < 0.0 or self.opacity > 1.0:
            raise ValueError("GaussianSplat opacity must be between 0 and 1")
