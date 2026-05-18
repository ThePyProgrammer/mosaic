from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GaussianSplat:
    center: tuple[float, float, float]
    covariance_upper: tuple[float, float, float, float, float, float]
    color_rgb: tuple[float, float, float] = (1.0, 1.0, 1.0)
    opacity: float = 1.0
    provenance: str | None = None

    def __post_init__(self) -> None:
        if len(self.center) != 3:
            raise ValueError("GaussianSplat center must contain three coordinates")
        if len(self.covariance_upper) != 6:
            raise ValueError("GaussianSplat covariance_upper must contain six values")
        xx, _, _, yy, _, zz = self.covariance_upper
        if xx <= 0.0 or yy <= 0.0 or zz <= 0.0:
            raise ValueError("GaussianSplat covariance diagonal values must be positive")
        if len(self.color_rgb) != 3:
            raise ValueError("GaussianSplat color_rgb must contain three channels")
        if any(channel < 0.0 or channel > 1.0 for channel in self.color_rgb):
            raise ValueError("GaussianSplat color_rgb channels must be between 0 and 1")
        if self.opacity < 0.0 or self.opacity > 1.0:
            raise ValueError("GaussianSplat opacity must be between 0 and 1")
