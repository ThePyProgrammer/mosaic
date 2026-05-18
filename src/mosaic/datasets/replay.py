from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Protocol

from mosaic.core.observations import MultiViewObservation


class MultiViewSequence(Protocol):
    def __iter__(self) -> Iterator[MultiViewObservation]:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class InMemorySequence:
    observations: tuple[MultiViewObservation, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "observations", tuple(self.observations))
        if not self.observations:
            raise ValueError("InMemorySequence requires at least one observation")
        timestamps = [observation.timestamp for observation in self.observations]
        if timestamps != sorted(timestamps):
            raise ValueError("InMemorySequence observations must be in timestamp order")

    def __iter__(self) -> Iterator[MultiViewObservation]:
        return iter(self.observations)

    def __len__(self) -> int:
        return len(self.observations)
