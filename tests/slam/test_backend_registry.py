from __future__ import annotations

from collections.abc import Callable

import pytest

from mosaic.slam import (
    AvailabilityResult,
    BackendCapabilities,
    BackendDependency,
    BackendDescriptor,
    BackendRegistry,
    DeterministicSplatBackend,
    default_backend_registry,
)

_MISSING_PACKAGE = "mosaic_backend_missing_dependency_for_tests_zzz"


def _capabilities() -> BackendCapabilities:
    return BackendCapabilities(
        supports_multi_view=True,
        supports_incremental_mapping=True,
        supports_uncertainty=False,
        runs_out_of_process=False,
        parameters={"deterministic": True},
    )


def _descriptor(
    name: str = "deterministic-splat",
    *,
    dependencies: tuple[BackendDependency, ...] = (),
    factory: Callable[[], DeterministicSplatBackend] = DeterministicSplatBackend,
) -> BackendDescriptor:
    return BackendDescriptor(
        name=name,
        version="0.1.0",
        capabilities=_capabilities(),
        dependencies=dependencies,
        parameters={"quality": 1.0, "accepted": True, "label": "deterministic", "count": 1},
        runs_out_of_process=False,
        factory=factory,
    )


def test_descriptor_metadata_is_inspectable_without_calling_factory() -> None:
    factory_calls = 0

    def factory() -> DeterministicSplatBackend:
        nonlocal factory_calls
        factory_calls += 1
        return DeterministicSplatBackend()

    descriptor = _descriptor(factory=factory)

    assert descriptor.name == "deterministic-splat"
    assert descriptor.version == "0.1.0"
    assert descriptor.capabilities.supports_multi_view is True
    assert descriptor.dependencies == ()
    assert descriptor.parameters == {
        "quality": 1.0,
        "accepted": True,
        "label": "deterministic",
        "count": 1,
    }
    assert descriptor.runs_out_of_process is False
    assert factory_calls == 0

    with pytest.raises(TypeError):
        descriptor.parameters["x"] = "blocked"  # type: ignore[index]


def test_descriptor_parameters_accept_json_ready_scalars() -> None:
    descriptor = _descriptor()

    assert descriptor.parameters["quality"] == 1.0
    assert descriptor.parameters["accepted"] is True
    assert descriptor.parameters["label"] == "deterministic"
    assert descriptor.parameters["count"] == 1


@pytest.mark.parametrize(
    "parameters",
    [
        {"weights": [1, 2, 3]},
        {"nested": {"x": 1}},
    ],
)
def test_descriptor_parameters_reject_non_scalar_values(parameters: object) -> None:
    with pytest.raises(ValueError, match="JSON-ready scalar"):
        BackendDescriptor(
            name="bad-backend",
            version="0.1.0",
            capabilities=_capabilities(),
            parameters=parameters,  # type: ignore[arg-type]
            factory=DeterministicSplatBackend,
        )


def test_availability_reports_missing_dependency_without_calling_factory() -> None:
    factory_calls = 0

    def factory() -> DeterministicSplatBackend:
        nonlocal factory_calls
        factory_calls += 1
        return DeterministicSplatBackend()

    descriptor = _descriptor(
        name="optional-splat",
        dependencies=(
            BackendDependency(
                package=_MISSING_PACKAGE,
                version_spec=">=1.0",
                install_hint=f"Install {_MISSING_PACKAGE}",
            ),
        ),
        factory=factory,
    )

    result = descriptor.check_availability()

    assert result.available is False
    assert result.missing_requirements == (_MISSING_PACKAGE,)
    assert result.diagnostics[_MISSING_PACKAGE] == "missing"
    assert result.install_hints[_MISSING_PACKAGE] == f"Install {_MISSING_PACKAGE}"
    assert factory_calls == 0


def test_availability_result_requires_missing_requirement_when_unavailable() -> None:
    with pytest.raises(ValueError, match="missing requirement"):
        AvailabilityResult(available=False)


def test_registry_metadata_paths_do_not_call_factory_but_create_does() -> None:
    factory_calls = 0

    def factory() -> DeterministicSplatBackend:
        nonlocal factory_calls
        factory_calls += 1
        return DeterministicSplatBackend()

    registry = BackendRegistry()
    registry.register(_descriptor(factory=factory))

    assert registry.names == ("deterministic-splat",)
    assert registry.descriptor("deterministic-splat").name == "deterministic-splat"
    availability = registry.availability("deterministic-splat")
    assert availability.available is True
    assert availability.missing_requirements == ()
    assert factory_calls == 0

    first = registry.create("deterministic-splat")
    second = registry.create("deterministic-splat")

    assert isinstance(first, DeterministicSplatBackend)
    assert isinstance(second, DeterministicSplatBackend)
    assert first is not second
    assert factory_calls == 2


def test_registry_rejects_duplicate_names() -> None:
    registry = BackendRegistry()
    registry.register(_descriptor())

    with pytest.raises(ValueError, match="already registered"):
        registry.register(_descriptor())


def test_registry_reports_missing_backend_names() -> None:
    registry = BackendRegistry()

    with pytest.raises(KeyError, match="is not registered"):
        registry.descriptor("missing")
    with pytest.raises(KeyError, match="is not registered"):
        registry.availability("missing")
    with pytest.raises(KeyError, match="is not registered"):
        registry.create("missing")


def test_default_backend_registry_contains_only_deterministic_backend() -> None:
    registry = default_backend_registry()

    assert registry.names == ("deterministic-splat",)
    descriptor = registry.descriptor("deterministic-splat")
    assert descriptor.name == "deterministic-splat"
    assert descriptor.version == "0.1.0"
    assert descriptor.dependencies == ()
    assert descriptor.runs_out_of_process is False
    assert descriptor.parameters["deterministic"] is True

    availability = registry.availability("deterministic-splat")
    assert availability.available is True
    assert availability.missing_requirements == ()
    assert availability.install_hints == {}

    assert registry.create("deterministic-splat") is not registry.create("deterministic-splat")
