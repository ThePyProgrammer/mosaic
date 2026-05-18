from __future__ import annotations

from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True, order=True, slots=True)
class Timestamp:
    """Canonical Mosaic timestamp stored as integer nanoseconds.

    Timestamp.nanoseconds is the canonical artifact precision. Timestamp
    artifacts store integer nanoseconds and do not use a seconds payload field.
    from_seconds() is only a convenience conversion and uses
    round(seconds * 1_000_000_000) to produce integer nanoseconds.
    """

    nanoseconds: int

    def __post_init__(self) -> None:
        if isinstance(self.nanoseconds, bool) or not isinstance(self.nanoseconds, int):
            raise ValueError("Timestamp nanoseconds must be an integer")
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
    """Named coordinate frame identifier.

    Mosaic uses right-handed robot/body frames by default. Camera projection
    APIs separately document optical-frame axes when a FrameId names an optical
    camera frame.
    """

    value: str

    def __post_init__(self) -> None:
        if not self.value.strip():
            raise ValueError("FrameId value must not be blank")

    def __str__(self) -> str:
        return self.value
