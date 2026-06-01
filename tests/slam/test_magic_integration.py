from __future__ import annotations

import sys
import struct
from pathlib import Path

import pytest

from mosaic.core import (
    CameraIntrinsics,
    CameraObservation,
    FrameId,
    ImageBuffer,
    ImageEncoding,
    MultiViewObservation,
    Pose3,
    Quaternion,
    Timestamp,
    Translation3,
)
from mosaic.datasets import InMemorySequence
from mosaic.evaluation import BenchmarkArtifact
from mosaic.slam import (
    MagicSlamBackend,
    export_agent_sequences_to_magic_replica,
    export_sequence_to_magic_replica,
    load_magic_ply_splat_map,
    magic_run_result_to_benchmark_artifact,
    magic_run_result_to_splat_map,
    magic_slam_backend_descriptor,
    write_magic_replica_config,
)
from mosaic.slam.magic import MagicSlamConfig, MagicSlamRunner


def test_magic_config_rejects_missing_repo_config_and_input_paths(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    input_path = tmp_path / "input"
    repo = tmp_path / "repo"

    with pytest.raises(ValueError, match="magic_repo"):
        MagicSlamConfig(
            magic_repo=repo,
            config_path=config_path,
            input_path=input_path,
            output_path=tmp_path / "output",
        )

    repo.mkdir()
    (repo / "run_slam.py").write_text("print('fake')\n")

    with pytest.raises(ValueError, match="config_path"):
        MagicSlamConfig(
            magic_repo=repo,
            config_path=config_path,
            input_path=input_path,
            output_path=tmp_path / "output",
        )

    config_path.write_text("seed: 0\n")

    with pytest.raises(ValueError, match="input_path"):
        MagicSlamConfig(
            magic_repo=repo,
            config_path=config_path,
            input_path=input_path,
            output_path=tmp_path / "output",
        )


def test_runner_builds_upstream_magic_command(tmp_path: Path) -> None:
    repo = _fake_magic_repo(tmp_path)
    config_path = tmp_path / "config.yaml"
    input_path = tmp_path / "input"
    config_path.write_text("seed: 0\n")
    input_path.mkdir()
    cfg = MagicSlamConfig(
        magic_repo=repo,
        config_path=config_path,
        input_path=input_path,
        output_path=tmp_path / "out",
        python_executable="python-test",
        seed=7,
        multi_gpu=True,
    )

    assert MagicSlamRunner(cfg).build_command() == (
        "python-test",
        str(repo / "run_slam.py"),
        str(config_path),
        "--input_path",
        str(input_path),
        "--output_path",
        str(tmp_path / "out"),
        "--seed",
        "7",
        "--multi_gpu",
    )


def test_runner_executes_fake_magic_and_discovers_artifacts(tmp_path: Path) -> None:
    repo = _fake_magic_repo(tmp_path, script_body=_success_script_body())
    config = _valid_config(tmp_path, repo)

    result = MagicSlamRunner(config).run()

    assert result.success is True
    assert result.returncode == 0
    assert "merged_refined_ply" in result.artifacts
    assert "walltime_stats_json" in result.artifacts
    assert result.diagnostics["returncode"] == 0
    assert result.diagnostics["artifact_count"] >= 2
    assert result.diagnostics["walltime_registration_time"] == pytest.approx(1.25)


def test_magic_run_result_converts_to_benchmark_artifact(tmp_path: Path) -> None:
    repo = _fake_magic_repo(tmp_path, script_body=_success_script_body())
    result = MagicSlamRunner(_valid_config(tmp_path, repo)).run()

    artifact = magic_run_result_to_benchmark_artifact(
        result,
        scenario_name="magic-smoke",
        update_count=4,
    )

    assert isinstance(artifact, BenchmarkArtifact)
    assert artifact.scenario_name == "magic-smoke"
    assert artifact.backend_name == "magic-slam"
    assert artifact.update_count == 4
    assert artifact.backend_metadata == {
        "name": "magic-slam",
        "runs_out_of_process": True,
        "integration": "out_of_process_runner",
    }
    metrics = {metric["name"]: metric for metric in artifact.metrics}
    assert metrics["fine_render_psnr"] == {
        "name": "fine_render_psnr",
        "value": 20.0,
        "unit": "db",
        "family": "render_quality",
    }
    assert metrics["fine_render_ssim"]["unit"] == "ratio"
    assert metrics["fine_render_depth_l1"]["unit"] == "meters"
    assert metrics["walltime_registration_time"]["unit"] == "seconds"
    assert artifact.diagnostics["returncode"] == 0
    assert artifact.diagnostics["artifact_merged_refined_ply"].endswith("merged_refined.ply")
    assert artifact.failure_classification == "none"


def test_load_magic_ascii_ply_as_splat_map(tmp_path: Path) -> None:
    ply_path = tmp_path / "merged_refined.ply"
    ply_path.write_text(
        "\n".join(
            (
                "ply",
                "format ascii 1.0",
                "element vertex 1",
                "property float x",
                "property float y",
                "property float z",
                "property float f_dc_0",
                "property float f_dc_1",
                "property float f_dc_2",
                "property float opacity",
                "property float scale_0",
                "property float scale_1",
                "property float scale_2",
                "end_header",
                "1.0 2.0 3.0 0.0 0.0 0.0 0.0 -2.0 -2.0 -2.0",
            )
        )
        + "\n"
    )

    splat_map = load_magic_ply_splat_map(ply_path, frame=FrameId("magic-map"))

    assert splat_map.frame == FrameId("magic-map")
    assert len(splat_map) == 1
    splat = splat_map.splats[0]
    assert splat.center == (1.0, 2.0, 3.0)
    assert splat.color_rgb == pytest.approx((0.5, 0.5, 0.5))
    assert splat.opacity == pytest.approx(0.5)
    assert splat.provenance == "magic-slam"


def test_load_magic_ply_rejects_non_ascii_for_now(tmp_path: Path) -> None:
    ply_path = tmp_path / "binary.ply"
    ply_path.write_bytes(b"ply\nformat binary_big_endian 1.0\nend_header\n")

    with pytest.raises(ValueError, match="ascii"):
        load_magic_ply_splat_map(ply_path, frame=FrameId("magic-map"))


def test_load_magic_binary_little_endian_ply_as_splat_map(tmp_path: Path) -> None:
    ply_path = tmp_path / "merged_refined.ply"
    header = "\n".join(
        (
            "ply",
            "format binary_little_endian 1.0",
            "element vertex 1",
            "property float x",
            "property float y",
            "property float z",
            "property float f_dc_0",
            "property float f_dc_1",
            "property float f_dc_2",
            "property float opacity",
            "property float scale_0",
            "property float scale_1",
            "property float scale_2",
            "end_header",
        )
    ).encode("ascii") + b"\n"
    row = struct.pack("<10f", 1.0, 2.0, 3.0, 0.0, 0.0, 0.0, 0.0, -2.0, -2.0, -2.0)
    ply_path.write_bytes(header + row)

    splat_map = load_magic_ply_splat_map(ply_path, frame=FrameId("magic-map"))

    assert len(splat_map) == 1
    assert splat_map.splats[0].center == (1.0, 2.0, 3.0)
    assert splat_map.splats[0].opacity == pytest.approx(0.5)


def test_magic_run_result_converts_refined_ply_to_splat_map(tmp_path: Path) -> None:
    repo = _fake_magic_repo(tmp_path, script_body=_success_script_body())
    result = MagicSlamRunner(_valid_config(tmp_path, repo)).run()
    result.artifacts["merged_refined_ply"].write_text(
        "\n".join(
            (
                "ply",
                "format ascii 1.0",
                "element vertex 1",
                "property float x",
                "property float y",
                "property float z",
                "end_header",
                "4.0 5.0 6.0",
            )
        )
        + "\n"
    )

    splat_map = magic_run_result_to_splat_map(result, frame=FrameId("magic-map"))

    assert splat_map.frame == FrameId("magic-map")
    assert splat_map.splats[0].center == (4.0, 5.0, 6.0)


def test_runner_reports_subprocess_failure(tmp_path: Path) -> None:
    repo = _fake_magic_repo(
        tmp_path,
        script_body="import sys\nprint('bad', file=sys.stderr)\nsys.exit(3)\n",
    )
    config = _valid_config(tmp_path, repo)

    result = MagicSlamRunner(config).run()

    assert result.success is False
    assert result.returncode == 3
    assert "bad" in result.stderr
    assert result.diagnostics["returncode"] == 3


def test_magic_descriptor_reports_missing_repo_without_importing_heavy_deps(tmp_path: Path) -> None:
    descriptor = magic_slam_backend_descriptor(
        magic_repo=tmp_path / "missing",
        config_path=tmp_path / "config.yaml",
        input_path=tmp_path / "input",
        output_path=tmp_path / "out",
    )

    availability = descriptor.check_availability()

    assert availability.available is False
    assert "magic_repo" in availability.missing_requirements
    assert descriptor.name == "magic-slam"
    assert descriptor.runs_out_of_process is True


def test_magic_descriptor_factory_creates_runner_backed_backend(tmp_path: Path) -> None:
    repo = _fake_magic_repo(tmp_path)
    config = _valid_config(tmp_path, repo)
    descriptor = magic_slam_backend_descriptor(
        magic_repo=config.magic_repo,
        config_path=config.config_path,
        input_path=config.input_path,
        output_path=config.output_path,
    )

    backend = descriptor.factory()

    assert isinstance(backend, MagicSlamBackend)
    assert backend.name == "magic-slam"
    assert backend.capabilities.runs_out_of_process is True


def test_magic_backend_exports_sequence_before_running_session(tmp_path: Path) -> None:
    repo = _fake_magic_repo(tmp_path, script_body=_success_script_body())
    input_root = tmp_path / "magic-input"
    input_root.mkdir()
    config_path = tmp_path / "config.yaml"
    config_path.write_text("seed: 0\n")
    backend = MagicSlamBackend(
        runner=MagicSlamRunner(
            MagicSlamConfig(
                magic_repo=repo,
                config_path=config_path,
                input_path=input_root,
                output_path=tmp_path / "out",
                python_executable=sys.executable,
            )
        )
    )

    result = backend.run_sequence(
        InMemorySequence((_rgbd_observation(0),)),
        camera_id="front",
        agent_subdir="agent_0",
    )

    assert result.success is True
    assert (input_root / "agent_0/results/frame000000.jpg").is_file()
    assert (input_root / "agent_0/results/depth000000.png").is_file()
    assert (input_root / "agent_0/traj.txt").is_file()


def test_export_agent_sequences_to_magic_replica_writes_multi_agent_folder(tmp_path: Path) -> None:
    exports = export_agent_sequences_to_magic_replica(
        {
            "agent_0": InMemorySequence((_rgbd_observation(0),)),
            "agent_1": InMemorySequence((_rgbd_observation(0, x=2.0),)),
        },
        output_path=tmp_path / "magic-input",
        camera_id="front",
    )

    assert exports.agent_ids == ("agent_0", "agent_1")
    assert (tmp_path / "magic-input/agent_0/results/frame000000.jpg").is_file()
    assert (tmp_path / "magic-input/agent_1/results/depth000000.png").is_file()
    assert exports.camera_metadata["W"] == 2


def test_magic_backend_exports_agent_sequences_before_running_session(tmp_path: Path) -> None:
    repo = _fake_magic_repo(tmp_path, script_body=_success_script_body())
    input_root = tmp_path / "magic-input"
    input_root.mkdir()
    config_path = tmp_path / "config.yaml"
    config_path.write_text("seed: 0\n")
    backend = MagicSlamBackend(
        runner=MagicSlamRunner(
            MagicSlamConfig(
                magic_repo=repo,
                config_path=config_path,
                input_path=input_root,
                output_path=tmp_path / "out",
                python_executable=sys.executable,
            )
        )
    )

    result = backend.run_agent_sequences(
        {
            "agent_0": InMemorySequence((_rgbd_observation(0),)),
            "agent_1": InMemorySequence((_rgbd_observation(0, x=2.0),)),
        },
        camera_id="front",
    )

    assert result.success is True
    assert (input_root / "agent_0/traj.txt").is_file()
    assert (input_root / "agent_1/traj.txt").is_file()


def test_write_magic_replica_config_uses_export_metadata_and_agent_ids(tmp_path: Path) -> None:
    exports = export_agent_sequences_to_magic_replica(
        {
            "agent_0": InMemorySequence((_rgbd_observation(0),)),
            "agent_1": InMemorySequence((_rgbd_observation(0, x=2.0),)),
        },
        output_path=tmp_path / "magic-input",
        camera_id="front",
    )

    config_path = write_magic_replica_config(
        output_path=tmp_path / "magic.yaml",
        input_path=tmp_path / "magic-input",
        run_output_path=tmp_path / "magic-output",
        export_result=exports,
        scene_name="mosaic-smoke",
        seed=3,
        multi_gpu=False,
    )

    text = config_path.read_text()
    assert "project_name: 'MAGiC-SLAM'" in text
    assert "dataset_name: 'replica'" in text
    assert "multi_gpu: False" in text
    assert "seed: 3" in text
    assert "agent_ids: [0, 1]" in text
    assert f"input_path: '{tmp_path / 'magic-input'}'" in text
    assert "W: 2" in text
    assert "H: 1" in text
    assert "depth_scale: 1000.0" in text


def test_export_sequence_to_magic_replica_writes_rgbd_files_and_trajectory(tmp_path: Path) -> None:
    sequence = InMemorySequence((_rgbd_observation(0), _rgbd_observation(1, x=1.5)))

    result = export_sequence_to_magic_replica(
        sequence,
        output_path=tmp_path / "agent_0",
        camera_id="front",
        depth_scale=1000.0,
    )

    assert result.frame_count == 2
    assert result.dataset_path == tmp_path / "agent_0"
    assert result.color_paths == (
        tmp_path / "agent_0/results/frame000000.jpg",
        tmp_path / "agent_0/results/frame000001.jpg",
    )
    assert result.depth_paths == (
        tmp_path / "agent_0/results/depth000000.png",
        tmp_path / "agent_0/results/depth000001.png",
    )
    assert result.color_paths[0].read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    assert result.depth_paths[0].read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    assert (tmp_path / "agent_0/traj.txt").read_text().splitlines() == [
        "1.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 1.0",
        "1.0 0.0 0.0 1.5 0.0 1.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 1.0",
    ]
    assert result.camera_metadata == {
        "H": 1,
        "W": 2,
        "fx": 1.0,
        "fy": 1.0,
        "cx": 0.5,
        "cy": 0.5,
        "depth_scale": 1000.0,
    }


def test_export_sequence_to_magic_replica_requires_rgbd_view(tmp_path: Path) -> None:
    timestamp = Timestamp(0)
    color_only = MultiViewObservation(
        timestamp=timestamp,
        views=(
            CameraObservation(
                camera_id="front",
                timestamp=timestamp,
                camera_pose=_pose(),
                intrinsics=CameraIntrinsics(width=1, height=1, fx=1.0, fy=1.0, cx=0.5, cy=0.5),
                color=ImageBuffer(width=1, height=1, channels=3, encoding=ImageEncoding.RGB8, data=b"\x00\x00\x00"),
            ),
        ),
    )

    with pytest.raises(ValueError, match="requires color and depth"):
        export_sequence_to_magic_replica(
            InMemorySequence((color_only,)),
            output_path=tmp_path / "agent_0",
            camera_id="front",
        )


def _valid_config(tmp_path: Path, repo: Path) -> MagicSlamConfig:
    config_path = tmp_path / "config.yaml"
    input_path = tmp_path / "input"
    config_path.write_text("seed: 0\n")
    input_path.mkdir(exist_ok=True)
    return MagicSlamConfig(
        magic_repo=repo,
        config_path=config_path,
        input_path=input_path,
        output_path=tmp_path / "out",
        python_executable=sys.executable,
    )


def _fake_magic_repo(tmp_path: Path, *, script_body: str = "print('fake magic')\n") -> Path:
    repo = tmp_path / "magic"
    repo.mkdir()
    (repo / "run_slam.py").write_text(script_body)
    return repo


def _success_script_body() -> str:
    return """
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("config_path")
parser.add_argument("--input_path")
parser.add_argument("--output_path")
parser.add_argument("--seed")
args = parser.parse_args()

output = Path(args.output_path)
output.mkdir(parents=True, exist_ok=True)
(output / "merged_refined.ply").write_text("ply\\n")
(output / "walltime_stats.json").write_text(json.dumps({"registration_time": 1.25, "total_merge_time": 2.5}))
(output / "fine_render_metrics.json").write_text(json.dumps({"psnr": 20.0, "ssim": 0.8, "depth_l1": 0.04}))
print("fake magic completed")
"""


def _rgbd_observation(index: int, *, x: float = 0.0) -> MultiViewObservation:
    timestamp = Timestamp(index)
    return MultiViewObservation(
        timestamp=timestamp,
        views=(
            CameraObservation(
                camera_id="front",
                timestamp=timestamp,
                camera_pose=_pose(x=x),
                intrinsics=CameraIntrinsics(width=2, height=1, fx=1.0, fy=1.0, cx=0.5, cy=0.5),
                color=ImageBuffer(
                    width=2,
                    height=1,
                    channels=3,
                    encoding=ImageEncoding.RGB8,
                    data=b"\xff\x00\x00\x00\xff\x00",
                ),
                depth=ImageBuffer(
                    width=2,
                    height=1,
                    channels=1,
                    encoding=ImageEncoding.DEPTH_F32,
                    data=struct.pack("<ff", 1.0, 2.0),
                ),
            ),
        ),
    )


def _pose(*, x: float = 0.0) -> Pose3:
    return Pose3(
        parent_frame=FrameId("world"),
        child_frame=FrameId("camera/front"),
        translation=Translation3(x=x, y=0.0, z=0.0),
        rotation=Quaternion.identity(),
    )
