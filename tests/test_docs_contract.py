from pathlib import Path

from mosaic import (
    DeterministicSplatBackend,
    FrameId,
    MemoryQueryResult,
    QueryFamily,
    RepresentationMemory,
    SplatMap,
    SplatPosteriorView,
    evaluation_ready_for_real_backend,
    run_slam_benchmark,
    synthetic_forward_sequence,
    write_benchmark_artifact,
)
from mosaic.agents import CellState, ClaimId, LocalRadiusQuery, SpatialCell


ROOT = Path(__file__).resolve().parents[1]
API_DOC = ROOT / "docs" / "API.md"
EXAMPLES_DOC = ROOT / "docs" / "EXAMPLES.md"
PYPROJECT = ROOT / "pyproject.toml"


API_ROOT_EXPORTS = (
    "DeterministicSplatBackend",
    "FrameId",
    "SplatPosteriorView",
    "RepresentationMemory",
    "MemoryQueryResult",
    "QueryFamily",
    "write_benchmark_artifact",
    "evaluation_ready_for_real_backend",
)

DEFERRED_INTEGRATIONS = (
    "real 3DGS backends",
    "ROS",
    "Habitat",
    "UI/WebSockets",
    "LLM/LVLM providers",
    "CUDA/native stacks",
    "production SLAM quality",
)

GOLDEN_PATH_NAMES = (
    "synthetic_forward_sequence",
    "DeterministicSplatBackend",
    "backend.snapshot",
    "SplatMap",
    "SplatPosteriorView",
    "LocalRadiusQuery",
    "query_local",
    "RepresentationMemory",
    "query_navigation_frontiers",
    "run_slam_benchmark",
    "write_benchmark_artifact",
)


assert MemoryQueryResult is not None
assert QueryFamily is not None
assert evaluation_ready_for_real_backend is not None


def _api_doc() -> str:
    return API_DOC.read_text(encoding="utf-8")


def _examples_doc() -> str:
    return EXAMPLES_DOC.read_text(encoding="utf-8")


def test_split_api_and_examples_docs_exist() -> None:
    assert API_DOC.exists()
    assert EXAMPLES_DOC.exists()
    assert PYPROJECT.exists()


def test_api_docs_reference_current_root_exports() -> None:
    api_doc = _api_doc()

    for name in API_ROOT_EXPORTS:
        assert name in api_doc


def test_api_docs_name_deferred_integrations() -> None:
    api_doc = _api_doc()

    for term in DEFERRED_INTEGRATIONS:
        assert term in api_doc


def test_examples_doc_names_the_canonical_golden_path() -> None:
    examples_doc = _examples_doc()

    for name in GOLDEN_PATH_NAMES:
        assert name in examples_doc

    assert "mosaic-benchmark.json" in examples_doc
    assert "local/disposable" in examples_doc or "disposable/local" in examples_doc
    assert "pip install torch" not in examples_doc
    assert "uv add torch" not in examples_doc
    assert "pip install ros" not in examples_doc
    assert "uv add habitat" not in examples_doc


def test_documented_golden_path_writes_local_artifact(tmp_path: Path) -> None:
    scenario = synthetic_forward_sequence(frame_count=3)
    backend = DeterministicSplatBackend(map_frame=FrameId("map"))

    for observation in scenario.sequence:
        backend.process(observation)

    snapshot = backend.snapshot()
    assert isinstance(snapshot, SplatMap)
    assert len(snapshot) == 3

    posterior = SplatPosteriorView(snapshot)
    local_result = posterior.query_local(
        LocalRadiusQuery(center=(0.0, 0.0, 0.0), radius=10.0, max_results=2)
    )
    assert local_result.count == 2
    assert local_result.total_matches == 3
    assert local_result.truncated is True

    memory = RepresentationMemory.empty(frame=FrameId("map")).with_cell(
        SpatialCell(
            frame=FrameId("map"),
            coordinate=(1, 2),
            resolution=0.5,
            state=CellState.FRONTIER,
            traversability=0.75,
            claim_ids=(ClaimId("claim-frontier-1"),),
        )
    )
    frontiers = memory.query_navigation_frontiers(max_results=1)
    assert frontiers.query_family is QueryFamily.NAVIGATION
    assert frontiers.total_matches == 1
    assert frontiers.truncated is False
    assert frontiers.items[0].state is CellState.FRONTIER

    artifact = run_slam_benchmark(
        scenario=scenario,
        backend=DeterministicSplatBackend(map_frame=FrameId("map")),
    )
    output = tmp_path / "mosaic-benchmark.json"

    write_benchmark_artifact(artifact, output)

    assert artifact.scenario_name == "synthetic-forward-3"
    assert artifact.backend_name == "deterministic-splat"
    assert output.read_text(encoding="utf-8").endswith("\n")


def test_documented_memory_query_endpoint_is_bounded() -> None:
    memory = (
        RepresentationMemory.empty(frame=FrameId("map"))
        .with_cell(
            SpatialCell(
                frame=FrameId("map"),
                coordinate=(1, 2),
                resolution=0.5,
                state=CellState.FRONTIER,
                traversability=0.75,
                claim_ids=(ClaimId("claim-frontier-1"),),
            )
        )
        .with_cell(
            SpatialCell(
                frame=FrameId("map"),
                coordinate=(2, 3),
                resolution=0.5,
                state=CellState.FRONTIER,
                traversability=0.6,
                claim_ids=(ClaimId("claim-frontier-2"),),
            )
        )
    )

    frontiers = memory.query_navigation_frontiers(max_results=1)

    assert isinstance(frontiers, MemoryQueryResult)
    assert frontiers.query_family is QueryFamily.NAVIGATION
    assert frontiers.total_matches == 2
    assert frontiers.truncated is True
    assert len(frontiers.items) == 1
