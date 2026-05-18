from __future__ import annotations

from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True, order=True, slots=True)
class Timestamp:
    nanoseconds: int

    def __post_init__(self) -> None:
        if self.nanoseconds < 0:
            raise ValueError("Timestamp nanoseconds must be non-negative")

    @classmethod
    def from_seconds(cls, seconds: float) -> Self:
        if seconds < 0.0:
            raise ValueError("Timestamp seconds must be non-negative")
        return cls(round(seconds * 1_000_000_000))

    def as_seconds(self) -> float:
        return self.nanoseconds / 1_000_000_000


@dataclass(frozen=True, order=True, slots=True)
class FrameId:
    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("FrameId value must not be blank")

    def __str__(self) -> str:
        return self.value
