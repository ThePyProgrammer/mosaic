from __future__ import annotations

import importlib.util
from collections.abc import Callable
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping

from mosaic.slam.fake_backend import DeterministicSplatBackend
from mosaic.slam.protocol import BackendCapabilities, MetricValue, SplatSlamBackend


@dataclass(frozen=True, slots=True)
class BackendDependency:
    package: str
    version_spec: str = ""
    install_hint: str = ""

    def __post_init__(self) -> None:
        if not self.package.strip():
            raise ValueError("BackendDependency package must not be blank")
        if "." in self.package:
            raise ValueError("BackendDependency package must be a top-level package name")


@dataclass(frozen=True, slots=True)
class AvailabilityResult:
    available: bool
    missing_requirements: tuple[str, ...] = ()
    diagnostics: Mapping[str, MetricValue] = field(default_factory=dict)
    install_hints: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "missing_requirements", tuple(self.missing_requirements))
        object.__setattr__(self, "diagnostics", MappingProxyType(dict(self.diagnostics)))
        object.__setattr__(self, "install_hints", MappingProxyType(dict(self.install_hints)))
        if not self.available and not self.missing_requirements:
            raise ValueError("Unavailable backend availability requires at least one missing requirement")


@dataclass(frozen=True, slots=True)
class BackendDescriptor:
    name: str
    version: str
    capabilities: BackendCapabilities
    dependencies: tuple[BackendDependency, ...] = ()
    parameters: Mapping[str, MetricValue] = field(default_factory=dict)
    runs_out_of_process: bool = False
    factory: Callable[[], SplatSlamBackend] = DeterministicSplatBackend

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("BackendDescriptor name must not be blank")
        if not self.version.strip():
            raise ValueError("BackendDescriptor version must not be blank")
        for key, value in self.parameters.items():
            if not isinstance(value, bool | int | float | str):
                raise ValueError(
                    "BackendDescriptor parameters must be JSON-ready scalar metadata "
                    f"(bool, int, float, or str); {key!r} is {type(value).__name__}"
                )
        object.__setattr__(self, "dependencies", tuple(self.dependencies))
        object.__setattr__(self, "parameters", MappingProxyType(dict(self.parameters)))

    def check_availability(self) -> AvailabilityResult:
        missing_requirements: list[str] = []
        diagnostics: dict[str, MetricValue] = {}
        install_hints: dict[str, str] = {}
        for dependency in self.dependencies:
            if importlib.util.find_spec(dependency.package) is None:
                missing_requirements.append(dependency.package)
                diagnostics[dependency.package] = "missing"
                if dependency.install_hint:
                    install_hints[dependency.package] = dependency.install_hint
        if missing_requirements:
            return AvailabilityResult(
                available=False,
                missing_requirements=tuple(missing_requirements),
                diagnostics=diagnostics,
                install_hints=install_hints,
            )
        return AvailabilityResult(available=True)


@dataclass(slots=True)
class BackendRegistry:
    _descriptors: dict[str, BackendDescriptor] = field(default_factory=dict, init=False, repr=False)

    def register(self, descriptor: BackendDescriptor) -> None:
        if descriptor.name in self._descriptors:
            raise ValueError(f"Backend {descriptor.name!r} is already registered")
        self._descriptors[descriptor.name] = descriptor

    def descriptor(self, name: str) -> BackendDescriptor:
        try:
            return self._descriptors[name]
        except KeyError as exc:
            raise KeyError(f"Backend {name!r} is not registered") from exc

    def availability(self, name: str) -> AvailabilityResult:
        return self.descriptor(name).check_availability()

    def create(self, name: str) -> SplatSlamBackend:
        return self.descriptor(name).factory()

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._descriptors))


def default_backend_registry() -> BackendRegistry:
    backend = DeterministicSplatBackend()
    capabilities = backend.capabilities
    registry = BackendRegistry()
    registry.register(
        BackendDescriptor(
            name="deterministic-splat",
            version="0.1.0",
            capabilities=capabilities,
            dependencies=(),
            parameters=dict(capabilities.parameters),
            runs_out_of_process=False,
            factory=DeterministicSplatBackend,
        )
    )
    return registry


__all__ = [
    "AvailabilityResult",
    "BackendDependency",
    "BackendDescriptor",
    "BackendRegistry",
    "default_backend_registry",
]
