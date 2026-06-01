from __future__ import annotations

import json
import math
import subprocess
import sys
import struct
import zlib
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, Mapping

from mosaic.core.frames import FrameId
from mosaic.core.observations import ImageEncoding, MultiViewObservation
from mosaic.datasets.replay import MultiViewSequence
from mosaic.slam.registry import AvailabilityResult, BackendDescriptor
from mosaic.slam.protocol import BackendCapabilities, MetricValue, SplatSlamUpdate
from mosaic.splats import GaussianSplat
from mosaic.splats.maps import SplatMap

if TYPE_CHECKING:
    from mosaic.evaluation.runner import BenchmarkArtifact


_KNOWN_ARTIFACTS = {
    "merged_coarse_ply": "merged_coarse.ply",
    "merged_refined_ply": "merged_refined.ply",
    "coarse_render_metrics_json": "coarse_render_metrics.json",
    "fine_render_metrics_json": "fine_render_metrics.json",
    "novel_render_metrics_json": "novel_render_metrics.json",
    "walltime_stats_json": "walltime_stats.json",
}
_DIAGNOSTIC_PREFIXES = {
    "coarse_render_metrics_json": "coarse_render",
    "fine_render_metrics_json": "fine_render",
    "novel_render_metrics_json": "novel_render",
    "walltime_stats_json": "walltime",
}
_METRIC_UNITS = {
    "psnr": "db",
    "ssim": "ratio",
    "lpips": "score",
    "depth_l1": "meters",
    "registration_time": "seconds",
    "total_merge_time": "seconds",
}
_SH_C0 = 0.28209479177387814
_PLY_SCALAR_FORMATS = {
    "char": "b",
    "int8": "b",
    "uchar": "B",
    "uint8": "B",
    "short": "h",
    "int16": "h",
    "ushort": "H",
    "uint16": "H",
    "int": "i",
    "int32": "i",
    "uint": "I",
    "uint32": "I",
    "float": "f",
    "float32": "f",
    "double": "d",
    "float64": "d",
}


@dataclass(frozen=True, slots=True)
class MagicSlamConfig:
    magic_repo: Path
    config_path: Path
    input_path: Path
    output_path: Path
    python_executable: str = sys.executable
    seed: int | None = None
    multi_gpu: bool = False
    use_wandb: bool = False
    wandb_offline: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "magic_repo", Path(self.magic_repo))
        object.__setattr__(self, "config_path", Path(self.config_path))
        object.__setattr__(self, "input_path", Path(self.input_path))
        object.__setattr__(self, "output_path", Path(self.output_path))

        if not self.magic_repo.is_dir():
            raise ValueError("MagicSlamConfig magic_repo must be an existing directory")
        if not (self.magic_repo / "run_slam.py").is_file():
            raise ValueError("MagicSlamConfig magic_repo must contain run_slam.py")
        if not self.config_path.is_file():
            raise ValueError("MagicSlamConfig config_path must be an existing file")
        if not self.input_path.is_dir():
            raise ValueError("MagicSlamConfig input_path must be an existing directory")
        if not self.python_executable.strip():
            raise ValueError("MagicSlamConfig python_executable must not be blank")


@dataclass(frozen=True, slots=True)
class MagicSlamRunner:
    config: MagicSlamConfig

    def build_command(self) -> tuple[str, ...]:
        command = [
            self.config.python_executable,
            str(self.config.magic_repo / "run_slam.py"),
            str(self.config.config_path),
            "--input_path",
            str(self.config.input_path),
            "--output_path",
            str(self.config.output_path),
        ]
        if self.config.seed is not None:
            command.extend(("--seed", str(self.config.seed)))
        if self.config.multi_gpu:
            command.append("--multi_gpu")
        if self.config.use_wandb:
            command.append("--use_wandb")
        if self.config.wandb_offline:
            command.append("--wandb_offline")
        return tuple(command)

    def run(self) -> MagicSlamRunResult:
        self.config.output_path.mkdir(parents=True, exist_ok=True)
        completed = subprocess.run(
            self.build_command(),
            cwd=self.config.magic_repo,
            capture_output=True,
            text=True,
            check=False,
        )
        artifacts = _discover_artifacts(self.config.output_path)
        diagnostics: dict[str, MetricValue] = {
            "returncode": completed.returncode,
            "success": completed.returncode == 0,
            "artifact_count": len(artifacts),
        }
        _add_json_diagnostics(self.config.output_path, diagnostics)
        return MagicSlamRunResult(
            returncode=completed.returncode,
            command=self.build_command(),
            output_path=self.config.output_path,
            artifacts=artifacts,
            diagnostics=diagnostics,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )


@dataclass(frozen=True, slots=True)
class MagicSlamRunResult:
    returncode: int
    command: tuple[str, ...]
    output_path: Path
    artifacts: Mapping[str, Path]
    diagnostics: Mapping[str, MetricValue]
    stdout: str = ""
    stderr: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "command", tuple(self.command))
        object.__setattr__(self, "output_path", Path(self.output_path))
        object.__setattr__(self, "artifacts", MappingProxyType(dict(self.artifacts)))
        object.__setattr__(self, "diagnostics", MappingProxyType(dict(self.diagnostics)))

    @property
    def success(self) -> bool:
        return self.returncode == 0


@dataclass(frozen=True, slots=True)
class MagicReplicaExportResult:
    dataset_path: Path
    frame_count: int
    color_paths: tuple[Path, ...]
    depth_paths: tuple[Path, ...]
    trajectory_path: Path
    camera_metadata: Mapping[str, float | int]

    def __post_init__(self) -> None:
        object.__setattr__(self, "dataset_path", Path(self.dataset_path))
        object.__setattr__(self, "color_paths", tuple(Path(path) for path in self.color_paths))
        object.__setattr__(self, "depth_paths", tuple(Path(path) for path in self.depth_paths))
        object.__setattr__(self, "trajectory_path", Path(self.trajectory_path))
        object.__setattr__(self, "camera_metadata", MappingProxyType(dict(self.camera_metadata)))


@dataclass(frozen=True, slots=True)
class MagicReplicaMultiAgentExportResult:
    dataset_path: Path
    agent_exports: Mapping[str, MagicReplicaExportResult]
    camera_metadata: Mapping[str, float | int]

    def __post_init__(self) -> None:
        agent_exports = dict(self.agent_exports)
        if not agent_exports:
            raise ValueError("MAGiC multi-agent export requires at least one agent sequence")
        object.__setattr__(self, "dataset_path", Path(self.dataset_path))
        object.__setattr__(self, "agent_exports", MappingProxyType(agent_exports))
        object.__setattr__(self, "camera_metadata", MappingProxyType(dict(self.camera_metadata)))

    @property
    def agent_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self.agent_exports))


def export_sequence_to_magic_replica(
    sequence: MultiViewSequence,
    *,
    output_path: Path,
    camera_id: str,
    depth_scale: float = 1000.0,
) -> MagicReplicaExportResult:
    if depth_scale <= 0.0:
        raise ValueError("MAGiC Replica export depth_scale must be positive")

    dataset_path = Path(output_path)
    results_path = dataset_path / "results"
    results_path.mkdir(parents=True, exist_ok=True)

    color_paths: list[Path] = []
    depth_paths: list[Path] = []
    trajectory_rows: list[str] = []
    camera_metadata: dict[str, float | int] | None = None

    for index, observation in enumerate(sequence):
        view = _select_view(observation, camera_id)
        if view.color is None or view.depth is None:
            raise ValueError("MAGiC Replica export requires color and depth for each selected view")
        if view.color.encoding is not ImageEncoding.RGB8:
            raise ValueError("MAGiC Replica export requires RGB8 color buffers")
        if view.depth.encoding is not ImageEncoding.DEPTH_F32:
            raise ValueError("MAGiC Replica export requires DEPTH_F32 depth buffers")
        if view.color.width != view.depth.width or view.color.height != view.depth.height:
            raise ValueError("MAGiC Replica export color and depth dimensions must match")

        if camera_metadata is None:
            camera_metadata = {
                "H": view.intrinsics.height,
                "W": view.intrinsics.width,
                "fx": view.intrinsics.fx,
                "fy": view.intrinsics.fy,
                "cx": view.intrinsics.cx,
                "cy": view.intrinsics.cy,
                "depth_scale": depth_scale,
            }

        color_path = results_path / f"frame{index:06d}.jpg"
        depth_path = results_path / f"depth{index:06d}.png"
        color_path.write_bytes(_png_rgb8(view.color.width, view.color.height, view.color.data))
        depth_path.write_bytes(
            _png_gray16(
                view.depth.width,
                view.depth.height,
                _depth_f32_to_u16(view.depth.data, depth_scale),
            )
        )
        color_paths.append(color_path)
        depth_paths.append(depth_path)
        trajectory_rows.append(_pose_row(view.camera_pose))

    if camera_metadata is None:
        raise ValueError("MAGiC Replica export requires at least one observation")

    trajectory_path = dataset_path / "traj.txt"
    trajectory_path.write_text("\n".join(trajectory_rows) + "\n")
    return MagicReplicaExportResult(
        dataset_path=dataset_path,
        frame_count=len(color_paths),
        color_paths=tuple(color_paths),
        depth_paths=tuple(depth_paths),
        trajectory_path=trajectory_path,
        camera_metadata=camera_metadata,
    )


def export_agent_sequences_to_magic_replica(
    agent_sequences: Mapping[str, MultiViewSequence],
    *,
    output_path: Path,
    camera_id: str,
    depth_scale: float = 1000.0,
) -> MagicReplicaMultiAgentExportResult:
    if not agent_sequences:
        raise ValueError("MAGiC multi-agent export requires at least one agent sequence")

    dataset_path = Path(output_path)
    exports: dict[str, MagicReplicaExportResult] = {}
    camera_metadata: Mapping[str, float | int] | None = None
    for agent_id in sorted(agent_sequences):
        if not agent_id.strip() or "/" in agent_id:
            raise ValueError("MAGiC multi-agent export agent ids must be non-blank single path segments")
        export = export_sequence_to_magic_replica(
            agent_sequences[agent_id],
            output_path=dataset_path / agent_id,
            camera_id=camera_id,
            depth_scale=depth_scale,
        )
        if camera_metadata is None:
            camera_metadata = export.camera_metadata
        elif dict(camera_metadata) != dict(export.camera_metadata):
            raise ValueError("MAGiC multi-agent export requires matching camera metadata across agents")
        exports[agent_id] = export

    return MagicReplicaMultiAgentExportResult(
        dataset_path=dataset_path,
        agent_exports=exports,
        camera_metadata=camera_metadata or {},
    )


def write_magic_replica_config(
    *,
    output_path: Path,
    input_path: Path,
    run_output_path: Path,
    export_result: MagicReplicaMultiAgentExportResult,
    scene_name: str = "mosaic-magic",
    seed: int = 0,
    multi_gpu: bool = False,
) -> Path:
    agent_numeric_ids = _magic_numeric_agent_ids(export_result.agent_ids)
    camera = export_result.camera_metadata
    config = f"""project_name: 'MAGiC-SLAM'
dataset_name: 'replica'
multi_gpu: {_yaml_bool(multi_gpu)}
use_wandb: False
wandb_offline: False
experiment_name: 'mosaic'
group_name: 'mosaic_magic'
seed: {seed}
mapping:
  new_submap_every: 50
  map_every: 5
  iterations: 50
  new_submap_iterations: 1000
  new_submap_points_num: 60000
  new_submap_gradient_points_num: 5000
  alpha_thre: 0.6
  pruning_thre: 0.1
  visualize: False
tracking:
  w_color_loss: 0.95
  iterations: 60
  cam_rot_lr: 0.0002
  cam_trans_lr: 0.002
  odometry_type: 'odometer'
  help_camera_initialization: False
  init_err_ratio: 5
  odometer_method: 'point_to_plane'
  filter_outlier_depth: True
  alpha_thre: 0.98
  soft_alpha: True
  mask_invalid_depth: False
loop_detection:
  feature_extractor_name: 'dino'
  weights_path: 'facebook/dinov2-small'
  embed_size: 384
  feature_dist_threshold: 0.35
  device: 'cpu'
  time_threshold: 0
  max_loops_per_frame: 1
  fitness_threshold: 0.5
  inlier_rmse_threshold: 0.1
cam:
  H: {camera["H"]}
  W: {camera["W"]}
  fx: {camera["fx"]}
  fy: {camera["fy"]}
  cx: {camera["cx"]}
  cy: {camera["cy"]}
  depth_scale: {camera["depth_scale"]}
data:
  scene_name: '{_yaml_quote(scene_name)}'
  input_path: '{_yaml_quote(str(input_path))}'
  output_path: '{_yaml_quote(str(run_output_path))}'
  agent_ids: [{", ".join(str(agent_id) for agent_id in agent_numeric_ids)}]
"""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(config)
    return path


def magic_run_result_to_benchmark_artifact(
    result: MagicSlamRunResult,
    *,
    scenario_name: str,
    update_count: int = 0,
) -> BenchmarkArtifact:
    from mosaic.evaluation.runner import BenchmarkArtifact

    metrics = _magic_metrics(result)
    diagnostics: dict[str, MetricValue] = dict(result.diagnostics)
    for name, path in result.artifacts.items():
        diagnostics[f"artifact_{name}"] = str(path)
    return BenchmarkArtifact(
        scenario_name=scenario_name,
        backend_name="magic-slam",
        update_count=update_count,
        metrics=metrics,
        backend_metadata={
            "name": "magic-slam",
            "runs_out_of_process": True,
            "integration": "out_of_process_runner",
        },
        diagnostics=diagnostics,
        failure_classification="none" if result.success else "lifecycle",
    )


def magic_run_result_to_splat_map(
    result: MagicSlamRunResult,
    *,
    frame: FrameId,
    artifact_name: str = "merged_refined_ply",
) -> SplatMap:
    try:
        path = result.artifacts[artifact_name]
    except KeyError as exc:
        raise KeyError(f"MAGiC run result does not contain artifact {artifact_name!r}") from exc
    return load_magic_ply_splat_map(path, frame=frame)


def load_magic_ply_splat_map(
    path: Path,
    *,
    frame: FrameId,
    provenance: str = "magic-slam",
) -> SplatMap:
    ply_path = Path(path)
    raw = ply_path.read_bytes()
    header_text, header_length = _ply_header(raw)
    header_lines = header_text.splitlines()
    if not header_lines or header_lines[0] != "ply":
        raise ValueError("MAGiC PLY converter requires a PLY file")

    format_name, vertex_count, properties = _parse_ply_header(header_lines)
    body = raw[header_length:]
    if format_name == "ascii":
        return _load_magic_ascii_ply(body, vertex_count, properties, frame, provenance)
    if format_name == "binary_little_endian":
        return _load_magic_binary_little_endian_ply(body, vertex_count, properties, frame, provenance)
    raise ValueError("MAGiC PLY converter currently supports ascii and binary_little_endian PLY only")


@dataclass(slots=True)
class MagicSlamBackend:
    runner: MagicSlamRunner
    map_frame: FrameId = field(default_factory=lambda: FrameId("map"))

    @property
    def name(self) -> str:
        return "magic-slam"

    @property
    def capabilities(self) -> BackendCapabilities:
        return BackendCapabilities(
            supports_multi_view=True,
            supports_incremental_mapping=False,
            supports_uncertainty=False,
            runs_out_of_process=True,
            parameters={
                "integration": "out_of_process_runner",
                "streaming_process": False,
            },
        )

    def reset(self) -> None:
        return None

    def process(self, observation: object) -> SplatSlamUpdate:
        raise NotImplementedError(
            "MAGiC-SLAM integration is batch/session-oriented; use run_session() instead of process()."
        )

    def snapshot(self) -> SplatMap:
        return SplatMap(frame=self.map_frame)

    def run_session(self) -> MagicSlamRunResult:
        return self.runner.run()

    def run_sequence(
        self,
        sequence: MultiViewSequence,
        *,
        camera_id: str,
        agent_subdir: str = "agent_0",
        depth_scale: float = 1000.0,
    ) -> MagicSlamRunResult:
        if not agent_subdir.strip() or "/" in agent_subdir:
            raise ValueError("MAGiC-SLAM agent_subdir must be a non-blank single path segment")
        export_sequence_to_magic_replica(
            sequence,
            output_path=self.runner.config.input_path / agent_subdir,
            camera_id=camera_id,
            depth_scale=depth_scale,
        )
        return self.run_session()

    def run_agent_sequences(
        self,
        agent_sequences: Mapping[str, MultiViewSequence],
        *,
        camera_id: str,
        depth_scale: float = 1000.0,
    ) -> MagicSlamRunResult:
        export_agent_sequences_to_magic_replica(
            agent_sequences,
            output_path=self.runner.config.input_path,
            camera_id=camera_id,
            depth_scale=depth_scale,
        )
        return self.run_session()


@dataclass(frozen=True, slots=True)
class MagicSlamBackendDescriptor(BackendDescriptor):
    availability_check: Callable[[], AvailabilityResult] | None = None

    def check_availability(self) -> AvailabilityResult:
        if self.availability_check is not None:
            return self.availability_check()
        return super().check_availability()


def magic_slam_backend_descriptor(
    *,
    magic_repo: Path,
    config_path: Path,
    input_path: Path,
    output_path: Path,
    python_executable: str = sys.executable,
    seed: int | None = None,
    multi_gpu: bool = False,
    use_wandb: bool = False,
    wandb_offline: bool = False,
) -> BackendDescriptor:
    capabilities = BackendCapabilities(
        supports_multi_view=True,
        supports_incremental_mapping=False,
        supports_uncertainty=False,
        runs_out_of_process=True,
        parameters={
            "integration": "out_of_process_runner",
            "streaming_process": False,
        },
    )

    def availability_check() -> AvailabilityResult:
        return _check_magic_runner_availability(
            magic_repo=Path(magic_repo),
            config_path=Path(config_path),
            input_path=Path(input_path),
            python_executable=python_executable,
        )

    def factory() -> MagicSlamBackend:
        config = MagicSlamConfig(
            magic_repo=Path(magic_repo),
            config_path=Path(config_path),
            input_path=Path(input_path),
            output_path=Path(output_path),
            python_executable=python_executable,
            seed=seed,
            multi_gpu=multi_gpu,
            use_wandb=use_wandb,
            wandb_offline=wandb_offline,
        )
        return MagicSlamBackend(runner=MagicSlamRunner(config))

    return MagicSlamBackendDescriptor(
        name="magic-slam",
        version="upstream",
        capabilities=capabilities,
        dependencies=(),
        parameters=dict(capabilities.parameters),
        runs_out_of_process=True,
        factory=factory,
        availability_check=availability_check,
    )


def _discover_artifacts(output_path: Path) -> dict[str, Path]:
    artifacts: dict[str, Path] = {}
    for artifact_name, file_name in _KNOWN_ARTIFACTS.items():
        path = output_path / file_name
        if path.is_file():
            artifacts[artifact_name] = path
    return artifacts


def _add_json_diagnostics(output_path: Path, diagnostics: dict[str, MetricValue]) -> None:
    for artifact_name, file_name in _KNOWN_ARTIFACTS.items():
        if not file_name.endswith(".json"):
            continue
        path = output_path / file_name
        if not path.is_file():
            continue
        try:
            payload = json.loads(path.read_text())
        except json.JSONDecodeError:
            diagnostics[f"{artifact_name}_valid_json"] = False
            continue
        if not isinstance(payload, dict):
            continue
        prefix = _DIAGNOSTIC_PREFIXES.get(artifact_name, artifact_name.removesuffix("_json"))
        for key, value in payload.items():
            if isinstance(value, bool | int | float | str):
                diagnostics[f"{prefix}_{key}"] = value


def _check_magic_runner_availability(
    *,
    magic_repo: Path,
    config_path: Path,
    input_path: Path,
    python_executable: str,
) -> AvailabilityResult:
    missing: list[str] = []
    diagnostics: dict[str, MetricValue] = {}
    install_hints: dict[str, str] = {}

    if not magic_repo.is_dir():
        missing.append("magic_repo")
        diagnostics["magic_repo"] = "missing"
        install_hints["magic_repo"] = "Clone https://github.com/VladimirYugay/MAGiC-SLAM and pass its path"
    elif not (magic_repo / "run_slam.py").is_file():
        missing.append("run_slam.py")
        diagnostics["run_slam.py"] = "missing"

    if not config_path.is_file():
        missing.append("config_path")
        diagnostics["config_path"] = "missing"
    if not input_path.is_dir():
        missing.append("input_path")
        diagnostics["input_path"] = "missing"
    if not python_executable.strip():
        missing.append("python_executable")
        diagnostics["python_executable"] = "blank"

    if missing:
        return AvailabilityResult(
            available=False,
            missing_requirements=tuple(missing),
            diagnostics=diagnostics,
            install_hints=install_hints,
        )
    return AvailabilityResult(available=True)


def _magic_metrics(result: MagicSlamRunResult) -> list[dict[str, str | float]]:
    metrics: list[dict[str, str | float]] = []
    for name, value in result.diagnostics.items():
        if not isinstance(value, int | float) or isinstance(value, bool):
            continue
        render_prefix = _matching_prefix(name, ("coarse_render_", "fine_render_", "novel_render_"))
        if render_prefix is not None:
            metric_key = name.removeprefix(render_prefix)
            metrics.append(
                {
                    "name": name,
                    "value": float(value),
                    "unit": _METRIC_UNITS.get(metric_key, "score"),
                    "family": "render_quality",
                }
            )
        elif name.startswith("walltime_"):
            metric_key = name.removeprefix("walltime_")
            metrics.append(
                {
                    "name": name,
                    "value": float(value),
                    "unit": _METRIC_UNITS.get(metric_key, "seconds"),
                    "family": "runtime",
                }
            )
    return metrics


def _matching_prefix(value: str, prefixes: tuple[str, ...]) -> str | None:
    for prefix in prefixes:
        if value.startswith(prefix):
            return prefix
    return None


def _magic_numeric_agent_ids(agent_ids: tuple[str, ...]) -> tuple[int, ...]:
    numeric_ids: list[int] = []
    for index, agent_id in enumerate(agent_ids):
        prefix = "agent_"
        if agent_id.startswith(prefix) and agent_id.removeprefix(prefix).isdigit():
            numeric_ids.append(int(agent_id.removeprefix(prefix)))
        else:
            numeric_ids.append(index)
    return tuple(numeric_ids)


def _yaml_bool(value: bool) -> str:
    return "True" if value else "False"


def _yaml_quote(value: str) -> str:
    return value.replace("'", "''")


def _load_magic_ascii_ply(
    body: bytes,
    vertex_count: int,
    properties: list[tuple[str, str]],
    frame: FrameId,
    provenance: str,
) -> SplatMap:
    property_names = [name for _, name in properties]
    _validate_magic_ply_properties(vertex_count, property_names)

    try:
        rows = body.decode("utf-8").splitlines()
    except UnicodeDecodeError as exc:
        raise ValueError("MAGiC PLY converter ascii body is not valid UTF-8") from exc

    splats: list[GaussianSplat] = []
    for row in rows[:vertex_count]:
        values = row.split()
        if len(values) < len(property_names):
            raise ValueError("MAGiC PLY converter vertex row has too few values")
        data = {name: float(value) for name, value in zip(property_names, values)}
        splats.append(_magic_vertex_to_splat(data, provenance=provenance))
    return SplatMap(frame=frame, splats=tuple(splats))


def _load_magic_binary_little_endian_ply(
    body: bytes,
    vertex_count: int,
    properties: list[tuple[str, str]],
    frame: FrameId,
    provenance: str,
) -> SplatMap:
    property_names = [name for _, name in properties]
    _validate_magic_ply_properties(vertex_count, property_names)
    row_format = "<" + "".join(_ply_scalar_format(property_type) for property_type, _ in properties)
    row_size = struct.calcsize(row_format)
    expected_size = vertex_count * row_size
    if len(body) < expected_size:
        raise ValueError("MAGiC PLY converter binary body is shorter than vertex count")

    splats: list[GaussianSplat] = []
    offset = 0
    for _ in range(vertex_count):
        values = struct.unpack_from(row_format, body, offset)
        offset += row_size
        data = {name: float(value) for name, value in zip(property_names, values)}
        splats.append(_magic_vertex_to_splat(data, provenance=provenance))
    return SplatMap(frame=frame, splats=tuple(splats))


def _ply_header(raw: bytes) -> tuple[str, int]:
    for marker in (b"end_header\n", b"end_header\r\n"):
        index = raw.find(marker)
        if index >= 0:
            header_length = index + len(marker)
            try:
                return raw[:header_length].decode("utf-8"), header_length
            except UnicodeDecodeError as exc:
                raise ValueError("MAGiC PLY converter header must be UTF-8 text") from exc
    raise ValueError("MAGiC PLY converter requires end_header")


def _parse_ply_header(header_lines: list[str]) -> tuple[str, int, list[tuple[str, str]]]:
    format_name = ""
    vertex_count = 0
    properties: list[tuple[str, str]] = []
    in_vertex_element = False
    for line in header_lines[1:]:
        if line == "format ascii 1.0":
            format_name = "ascii"
            continue
        if line == "format binary_little_endian 1.0":
            format_name = "binary_little_endian"
            continue
        if line.startswith("format "):
            format_name = line.split(maxsplit=2)[1]
            continue
        if line.startswith("element "):
            parts = line.split()
            in_vertex_element = len(parts) == 3 and parts[1] == "vertex"
            if in_vertex_element:
                vertex_count = int(parts[2])
            continue
        if in_vertex_element and line.startswith("property "):
            parts = line.split()
            if len(parts) != 3:
                raise ValueError("MAGiC PLY converter only supports scalar vertex properties")
            properties.append((parts[1], parts[2]))
    return format_name, vertex_count, properties


def _validate_magic_ply_properties(vertex_count: int, property_names: list[str]) -> None:
    if vertex_count < 0:
        raise ValueError("MAGiC PLY converter vertex count must be non-negative")
    for required in ("x", "y", "z"):
        if required not in property_names:
            raise ValueError(f"MAGiC PLY converter requires property {required!r}")


def _ply_scalar_format(property_type: str) -> str:
    try:
        return _PLY_SCALAR_FORMATS[property_type]
    except KeyError as exc:
        raise ValueError(f"MAGiC PLY converter does not support property type {property_type!r}") from exc


def _magic_vertex_to_splat(data: Mapping[str, float], *, provenance: str) -> GaussianSplat:
    scales = (
        max(math.exp(data.get("scale_0", -4.0)), 1e-6),
        max(math.exp(data.get("scale_1", -4.0)), 1e-6),
        max(math.exp(data.get("scale_2", -4.0)), 1e-6),
    )
    covariance_upper = (
        scales[0] * scales[0],
        0.0,
        0.0,
        scales[1] * scales[1],
        0.0,
        scales[2] * scales[2],
    )
    return GaussianSplat(
        center=(data["x"], data["y"], data["z"]),
        covariance_upper=covariance_upper,
        color_rgb=(
            _sh_dc_to_rgb(data.get("f_dc_0", _rgb_to_sh_dc(1.0))),
            _sh_dc_to_rgb(data.get("f_dc_1", _rgb_to_sh_dc(1.0))),
            _sh_dc_to_rgb(data.get("f_dc_2", _rgb_to_sh_dc(1.0))),
        ),
        opacity=_sigmoid(data.get("opacity", 10.0)),
        provenance=provenance,
    )


def _sh_dc_to_rgb(value: float) -> float:
    return max(0.0, min(1.0, (value * _SH_C0) + 0.5))


def _rgb_to_sh_dc(value: float) -> float:
    return (value - 0.5) / _SH_C0


def _sigmoid(value: float) -> float:
    if value >= 0.0:
        z = math.exp(-value)
        return 1.0 / (1.0 + z)
    z = math.exp(value)
    return z / (1.0 + z)


def _select_view(observation: MultiViewObservation, camera_id: str):
    for view in observation.views:
        if view.camera_id == camera_id:
            return view
    raise ValueError(f"MAGiC Replica export camera_id {camera_id!r} is not present in observation")


def _pose_row(pose) -> str:
    matrix = _pose_matrix(pose)
    return " ".join(str(value) for row in matrix for value in row)


def _pose_matrix(pose) -> tuple[tuple[float, float, float, float], ...]:
    w, x, y, z = pose.rotation.as_tuple()
    xx = x * x
    yy = y * y
    zz = z * z
    xy = x * y
    xz = x * z
    yz = y * z
    wx = w * x
    wy = w * y
    wz = w * z
    tx, ty, tz = pose.translation.as_tuple()
    return (
        (1.0 - 2.0 * (yy + zz), 2.0 * (xy - wz), 2.0 * (xz + wy), tx),
        (2.0 * (xy + wz), 1.0 - 2.0 * (xx + zz), 2.0 * (yz - wx), ty),
        (2.0 * (xz - wy), 2.0 * (yz + wx), 1.0 - 2.0 * (xx + yy), tz),
        (0.0, 0.0, 0.0, 1.0),
    )


def _depth_f32_to_u16(data: bytes, depth_scale: float) -> bytes:
    if len(data) % 4 != 0:
        raise ValueError("DEPTH_F32 data length must be divisible by four")
    values = struct.unpack(f"<{len(data) // 4}f", data)
    return b"".join(_u16be(max(0, min(65535, round(value * depth_scale)))) for value in values)


def _png_rgb8(width: int, height: int, data: bytes) -> bytes:
    row_length = width * 3
    scanlines = b"".join(b"\x00" + data[row_start : row_start + row_length] for row_start in range(0, len(data), row_length))
    return _png(width, height, color_type=2, bit_depth=8, scanlines=scanlines)


def _png_gray16(width: int, height: int, data: bytes) -> bytes:
    row_length = width * 2
    scanlines = b"".join(b"\x00" + data[row_start : row_start + row_length] for row_start in range(0, len(data), row_length))
    return _png(width, height, color_type=0, bit_depth=16, scanlines=scanlines)


def _png(width: int, height: int, *, color_type: int, bit_depth: int, scanlines: bytes) -> bytes:
    return b"".join(
        (
            b"\x89PNG\r\n\x1a\n",
            _png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, bit_depth, color_type, 0, 0, 0)),
            _png_chunk(b"IDAT", zlib.compress(scanlines)),
            _png_chunk(b"IEND", b""),
        )
    )


def _png_chunk(chunk_type: bytes, payload: bytes) -> bytes:
    checksum = zlib.crc32(chunk_type)
    checksum = zlib.crc32(payload, checksum)
    return struct.pack(">I", len(payload)) + chunk_type + payload + struct.pack(">I", checksum & 0xFFFFFFFF)


def _u16be(value: int) -> bytes:
    return struct.pack(">H", value)


__all__ = [
    "MagicReplicaExportResult",
    "MagicReplicaMultiAgentExportResult",
    "MagicSlamBackend",
    "MagicSlamBackendDescriptor",
    "MagicSlamConfig",
    "MagicSlamRunResult",
    "MagicSlamRunner",
    "export_agent_sequences_to_magic_replica",
    "export_sequence_to_magic_replica",
    "load_magic_ply_splat_map",
    "magic_run_result_to_benchmark_artifact",
    "magic_run_result_to_splat_map",
    "magic_slam_backend_descriptor",
    "write_magic_replica_config",
]
