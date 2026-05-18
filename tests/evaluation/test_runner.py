import json

from mosaic.core import FrameId
from mosaic.evaluation import BenchmarkArtifact, run_slam_benchmark, synthetic_forward_sequence, write_benchmark_artifact
from mosaic.slam import DeterministicSplatBackend


def test_run_slam_benchmark_processes_scenario_and_reports_metrics() -> None:
    artifact = run_slam_benchmark(
        scenario=synthetic_forward_sequence(frame_count=3),
        backend=DeterministicSplatBackend(map_frame=FrameId("map")),
    )

    assert artifact.scenario_name == "synthetic-forward-3"
    assert artifact.backend_name == "deterministic-splat"
    assert artifact.metrics == [{"name": "splat_count", "value": 3.0, "unit": "splats"}]
    assert artifact.update_count == 3


def test_benchmark_artifact_is_json_ready() -> None:
    artifact = BenchmarkArtifact(
        scenario_name="scenario",
        backend_name="backend",
        update_count=2,
        metrics=[{"name": "splat_count", "value": 2.0, "unit": "splats"}],
    )

    assert artifact.as_dict() == {
        "scenario_name": "scenario",
        "backend_name": "backend",
        "update_count": 2,
        "metrics": [{"name": "splat_count", "value": 2.0, "unit": "splats"}],
    }


def test_write_benchmark_artifact_writes_stable_json(tmp_path) -> None:
    artifact = BenchmarkArtifact(
        scenario_name="scenario",
        backend_name="backend",
        update_count=1,
        metrics=[{"name": "splat_count", "value": 1.0, "unit": "splats"}],
    )
    path = tmp_path / "artifact.json"

    write_benchmark_artifact(artifact, path)

    assert json.loads(path.read_text()) == artifact.as_dict()
    assert path.read_text().endswith("\n")
