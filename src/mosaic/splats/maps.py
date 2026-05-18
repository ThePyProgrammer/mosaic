from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Self

from mosaic.core.frames import FrameId
from mosaic.splats.primitives import GaussianSplat


@dataclass(frozen=True, slots=True)
class SplatMap:
    frame: FrameId
    splats: tuple[GaussianSplat, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "splats", tuple(self.splats))

    def with_splats(self, splats: Iterable[GaussianSplat]) -> Self:
        return type(self)(frame=self.frame, splats=self.splats + tuple(splats))

    def __len__(self) -> int:
        return len(self.splats)
