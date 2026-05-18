from __future__ import annotations

from dataclasses import dataclass

from mosaic.splats import SplatMap


@dataclass(frozen=True, slots=True)
class MetricResult:
    name: str
    value: float
    unit: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("MetricResult name must not be blank")
        if not self.unit.strip():
            raise ValueError("MetricResult unit must not be blank")

    def as_dict(self) -> dict[str, str | float]:
        return {"name": self.name, "value": self.value, "unit": self.unit}


def splat_count_metric(snapshot: SplatMap) -> MetricResult:
    return MetricResult(name="splat_count", value=float(len(snapshot)), unit="splats")
