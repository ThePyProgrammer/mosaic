from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
PYPROJECT = ROOT / "pyproject.toml"


REQUIRED_HEADINGS = (
    "# Mosaic",
    "## Scope",
    "## Install and Test",
    "## Public API Map",
    "## Quick Smoke Examples",
    "## Backend and Dependency Boundary",
    "## Known Hardening Gaps",
)

REQUIRED_COMMANDS = (
    "uv sync",
    "uv run pytest -q",
)

REQUIRED_MODULES = (
    "mosaic.core",
    "mosaic.datasets",
    "mosaic.splats",
    "mosaic.slam",
    "mosaic.platforms",
    "mosaic.fusion",
    "mosaic.evaluation",
    "mosaic.agents",
)

BOUNDARY_TERMS = (
    "torch",
    "opencv",
    "ros",
    "habitat",
    "openai",
    "anthropic",
    "websocket",
    "cuda",
    "sudo",
)

BOUNDARY_CONTEXT_MARKERS = (
    "deferred",
    "not required",
    "out of scope",
)


def _readme() -> str:
    return README.read_text(encoding="utf-8")


def _pyproject() -> str:
    return PYPROJECT.read_text(encoding="utf-8")


def test_readme_contains_required_phase_1_headings_and_commands() -> None:
    readme = _readme()

    for heading in REQUIRED_HEADINGS:
        assert heading in readme

    for command in REQUIRED_COMMANDS:
        assert command in readme

    assert "73" in readme

    for module_name in REQUIRED_MODULES:
        assert module_name in readme


def test_readme_examples_preserve_dependency_boundary() -> None:
    for line in _readme().splitlines():
        normalized = line.casefold()
        for term in BOUNDARY_TERMS:
            if term in normalized:
                assert any(marker in normalized for marker in BOUNDARY_CONTEXT_MARKERS), line


def test_runtime_dependencies_stay_empty_when_readme_claims_pure_python_boundary() -> None:
    readme = _readme()
    pyproject = _pyproject()

    assert "pure-Python" in readme
    assert "dependencies = []" in readme
    assert "dependencies = []" in pyproject
