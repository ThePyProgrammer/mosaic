from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
PYPROJECT = ROOT / "pyproject.toml"


REQUIRED_HEADINGS = (
    "# Mosaic",
    "## Scope",
    "## Documentation Map",
    "## Install and Test",
    "## Public API Map",
    "## Golden Path Teaser",
    "## Backend and Dependency Boundary",
    "## Agent-Facing Layers",
)

REQUIRED_LINKS = (
    "docs/API.md",
    "docs/EXAMPLES.md",
    "CONTRIBUTING.md",
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
    "real 3dgs",
    "ros",
    "habitat",
    "ui",
    "websocket",
    "llm",
    "lvlm",
    "cuda",
    "native",
    "production slam",
)

STALE_PUBLIC_FRAMING = (
    "Phase 1 baseline",
    "Phase 7 planned",
    "not required for Phase 1",
)


def _readme() -> str:
    return README.read_text(encoding="utf-8")


def _pyproject() -> str:
    return PYPROJECT.read_text(encoding="utf-8")


def test_readme_contains_required_v1_release_headings_links_and_commands() -> None:
    readme = _readme()

    assert "Mosaic v1 foundation" in readme

    for heading in REQUIRED_HEADINGS:
        assert heading in readme

    for link in REQUIRED_LINKS:
        assert link in readme

    for command in REQUIRED_COMMANDS:
        assert command in readme

    for module_name in REQUIRED_MODULES:
        assert module_name in readme

    for stale_phrase in STALE_PUBLIC_FRAMING:
        assert stale_phrase not in readme


def test_readme_preserves_v1_dependency_and_release_boundary_terms() -> None:
    readme = _readme()

    assert "dependencies = []" in readme

    for term in BOUNDARY_TERMS:
        assert term in readme.casefold()

    for line in readme.splitlines():
        normalized = line.casefold().strip()
        for term in BOUNDARY_TERMS:
            if term in normalized:
                assert not normalized.startswith("pip install")
                assert not normalized.startswith("uv add")
                assert not normalized.startswith("uv pip install")


def test_runtime_dependencies_stay_empty_when_readme_claims_pure_python_boundary() -> None:
    readme = _readme()
    pyproject = _pyproject()

    assert "pure-Python" in readme
    assert "dependencies = []" in readme
    assert "dependencies = []" in pyproject


def test_readme_locks_v1_contract_fixture_language() -> None:
    readme = _readme()

    assert "DeterministicSplatBackend" in readme
    assert "deterministic scenarios" in readme
    assert "benchmark gates" in readme
    assert "ProvenancePreservingFusion" in readme
    assert "contract/reference fixtures" in readme
    assert "preserved_not_optimized" in readme
    assert "preserved-not-optimized" not in readme
    assert "does not optimize Gaussians" in readme
    assert "does not collapse overlapping splats into occupancy-grid cells" in readme

    for line in readme.splitlines():
        normalized = line.casefold().strip()
        for term in BOUNDARY_TERMS:
            if term in normalized:
                assert not normalized.startswith("pip install")
                assert not normalized.startswith("uv add")
                assert not normalized.startswith("uv pip install")


def test_readme_separates_provider_free_agent_layers() -> None:
    readme = _readme()

    assert "SplatPosteriorView" in readme
    assert "RepresentationMemory" in readme
    assert "bounded descriptive splat-snapshot query layer" in readme
    assert "higher deterministic memory/tool contract layer" in readme
    assert "provider-free" in readme


def test_readme_fusion_smoke_example_uses_public_api() -> None:
    readme = _readme()

    assert "assert len(result.fused_map) == 1" in readme
    assert "assert len(result.map)" not in readme

    from mosaic import FrameId, FusionInput, GaussianSplat, ProvenancePreservingFusion, SplatMap

    map_frame = FrameId("map")
    left = SplatMap(
        frame=map_frame,
        splats=(
            GaussianSplat(
                center=(0.0, 0.0, 1.0),
                covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1),
                provenance="left-camera",
            ),
        ),
    )
    right = SplatMap(frame=map_frame)
    result = ProvenancePreservingFusion().fuse(FusionInput(maps=(left, right)))

    assert result.status.value == "fused"
    assert len(result.fused_map) == 1
