from __future__ import annotations

from dataclasses import dataclass, field

from mosaic.platforms.types import PlatformDescription


@dataclass(slots=True)
class PlatformRegistry:
    _platforms: dict[str, PlatformDescription] = field(default_factory=dict, init=False, repr=False)

    def register(self, platform: PlatformDescription) -> None:
        if platform.name in self._platforms:
            raise ValueError(f"Platform {platform.name!r} is already registered")
        self._platforms[platform.name] = platform

    def get(self, name: str) -> PlatformDescription:
        try:
            return self._platforms[name]
        except KeyError as exc:
            raise KeyError(f"Platform {name!r} is not registered") from exc

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._platforms))
