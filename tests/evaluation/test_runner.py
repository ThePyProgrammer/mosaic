import json
from typing import Any, cast

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
    assert artifact.backend_metadata["name"] == "deterministic-splat"
    assert artifact.backend_metadata["supports_multi_view"] is True
    assert artifact.backend_metadata["supports_incremental_mapping"] is True
    assert artifact.backend_metadata["supports_uncertainty"] is False
    assert artifact.backend_metadata["runs_out_of_process"] is False
    assert artifact.backend_metadata["parameter_deterministic"] is True
    json.dumps(artifact.as_dict()["backend_metadata"], sort_keys=True)
    assert artifact.metrics == [{"name": "splat_count", "value": 3.0, "unit": "splats"}]
    assert artifact.diagnostics == {"last_splat_count": 3, "snapshot_splat_count": 3}
    assert artifact.failure_classification == "none"
    assert artifact.update_count == 3


def test_benchmark_artifact_is_json_ready() -> None:
    artifact = BenchmarkArtifact(
        scenario_name="scenario",
        backend_name="backend",
        update_count=2,
        metrics=[{"name": "splat_count", "value": 2.0, "unit": "splats"}],
        backend_metadata={"name": "backend"},
        diagnostics={"snapshot_splat_count": 2},
        failure_classification="none",
    )

    assert artifact.as_dict() == {
        "scenario_name": "scenario",
        "backend_name": "backend",
        "backend_metadata": {"name": "backend"},
        "update_count": 2,
        "metrics": [{"name": "splat_count", "value": 2.0, "unit": "splats"}],
        "diagnostics": {"snapshot_splat_count": 2},
        "failure_classification": "none",
    }


def test_benchmark_artifact_as_dict_does_not_expose_internal_mappings() -> None:
    artifact = BenchmarkArtifact(
        scenario_name="scenario",
        backend_name="backend",
        update_count=1,
        metrics=[{"name": "splat_count", "value": 1.0, "unit": "splats"}],
        backend_metadata={"name": "backend"},
        diagnostics={"snapshot_splat_count": 1},
        failure_classification="none",
    )

    serialized = artifact.as_dict()
    metrics = cast(list[dict[str, str | float]], serialized["metrics"])
    backend_metadata = cast(dict[str, Any], serialized["backend_metadata"])
    diagnostics = cast(dict[str, Any], serialized["diagnostics"])
    metrics[0]["value"] = 999.0
    backend_metadata["name"] = "mutated"
    diagnostics["snapshot_splat_count"] = 999

    assert artifact.as_dict()["metrics"] == [{"name": "splat_count", "value": 1.0, "unit": "splats"}]
    assert artifact.as_dict()["backend_metadata"] == {"name": "backend"}
    assert artifact.as_dict()["diagnostics"] == {"snapshot_splat_count": 1}


def test_write_benchmark_artifact_writes_stable_json(tmp_path) -> None:
    artifact = BenchmarkArtifact(
        scenario_name="scenario",
        backend_name="backend",
        update_count=1,
        metrics=[{"name": "splat_count", "value": 1.0, "unit": "splats"}],
        backend_metadata={"name": "backend"},
        diagnostics={"snapshot_splat_count": 1},
        failure_classification="none",
    )
    path = tmp_path / "artifact.json"

    write_benchmark_artifact(artifact, path)

    loaded = json.loads(path.read_text())
    assert loaded == artifact.as_dict()
    assert loaded["backend_metadata"] == {"name": "backend"}
    assert loaded["diagnostics"] == {"snapshot_splat_count": 1}
    assert loaded["failure_classification"] == "none"
    assert path.read_text().startswith("{\n  \"backend_metadata\"")
    assert path.read_text().endswith("\n")
