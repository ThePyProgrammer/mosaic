# Phase 08: Documentation and Release Readiness - Pattern Map

**Mapped:** 2026-05-21
**Files analyzed:** 6 new/modified files
**Analogs found:** 6 / 6

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `README.md` | documentation | request-response | `README.md` | exact-existing-file |
| `docs/API.md` | documentation | transform | `src/mosaic/__init__.py`, package `__init__.py` files, `tests/test_public_api.py` | role-match |
| `docs/EXAMPLES.md` | documentation | batch + file-I/O + request-response | `README.md`, `tests/evaluation/test_runner.py`, `tests/agents/test_splat_posterior.py`, `tests/agents/test_representation_memory.py` | role-match |
| `CONTRIBUTING.md` | documentation | request-response | `pyproject.toml`, `tests/slam/test_backend_registry.py`, `tests/slam/test_backend_contract_helpers.py` | partial-role-match |
| `tests/test_readme_contract.py` | test | file-I/O + request-response | `tests/test_readme_contract.py` | exact-existing-file |
| `tests/test_docs_contract.py` | test | file-I/O + request-response | `tests/test_readme_contract.py`, `tests/test_public_api.py` | role-match |

## Pattern Assignments

### `README.md` (documentation, request-response)

**Analog:** `README.md`

**Current orientation pattern to preserve and rewrite** (lines 1-5):
```markdown
# Mosaic

Mosaic is a typed, headless Python library for 3D Gaussian Splatting SLAM contracts over multi-view moving cameras on robotic systems. Phase 1 establishes the merged main-checkout baseline: pure-Python representation types, deterministic reference implementations, public package surfaces, tests, and documentation that let later backend, fusion, evaluation, and agent work harden against a known contract.

Mosaic is intentionally library-first. It provides stable Python APIs for robotic SLAM backends, evaluation tools, platform camera rigs, fusion seams, and bounded agent-facing posterior queries without coupling the core package to one robot, simulator, provider runtime, browser runtime, or accelerator-heavy backend; those integrations are deferred and not required for the core.
```

**How to copy it:** keep the concise, library-first opening shape, but replace stale `Phase 1`/baseline wording with `Mosaic v1 foundation`. README should become an entry point and link hub, not the full API reference.

**Install/test command pattern** (lines 22-39):
```markdown
## Install and Test

Mosaic targets Python 3.12+ and uses `uv` for the project environment.

```bash
uv sync
uv run pytest -q
```

The current deterministic contract suite is the supported quality gate for this package; the earlier merged baseline recorded 73 passing tests and the suite has expanded since then.

The package keeps the Phase 1 runtime boundary empty in `pyproject.toml`:

```toml
dependencies = []
```

`pytest` is a development dependency used by the test workflow. Do not add runtime dependency installation steps to use the core package.
```

**How to copy it:** retain `uv sync`, `uv run pytest -q`, and `dependencies = []`. Remove exact historical count `73` and replace `Phase 1 runtime boundary` with v1 foundation dependency-boundary language.

**Public API table pattern** (lines 41-55):
```markdown
## Public API Map

Public imports are exposed from explicit package surfaces. The root `mosaic` package re-exports stable primitives, while subpackages group the same contracts by responsibility.

| Package surface | Responsibility | Representative APIs |
|-----------------|----------------|---------------------|
| `mosaic.core` | Frames, timestamps, poses, cameras, image buffers, and observations | `FrameId`, `Timestamp`, `Pose3`, `CameraIntrinsics`, `MultiViewObservation` |
| `mosaic.datasets` | Replayable multi-view sequences | `MultiViewSequence`, `InMemorySequence` |
| `mosaic.splats` | Gaussian primitives and immutable map snapshots | `GaussianSplat`, `SplatMap` |
| `mosaic.slam` | Backend lifecycle protocols and deterministic reference backend | `SplatSlamBackend`, `SplatSlamUpdate`, `TrackingState`, `DeterministicSplatBackend` |
| `mosaic.platforms` | Robot-neutral platform descriptions and camera rigs | `CameraRig`, `PlatformRegistry`, `quadruped_front_rig`, `ugv_surround_rig`, `humanoid_stereo_rig` |
| `mosaic.fusion` | Splat-map fusion contracts and deterministic reference strategy | `FusionInput`, `FusionResult`, `FusionStatus`, `FusionProvenanceSummary`, `FusionUncertaintySummary`, `FusionConflictSummary`, `ProvenancePreservingFusion` |
| `mosaic.evaluation` | Synthetic scenarios, benchmark artifacts, metric families, regression gates, and readiness checks | `synthetic_forward_sequence`, `run_slam_benchmark`, `FailureClass`, `RegressionGate`, `evaluation_ready_for_real_backend`, `write_benchmark_artifacts_jsonl` |
| `mosaic.agents` | Provider-free bounded descriptive posterior views over immutable splat snapshots | `AgentQueryKind.UNCERTAINTY`, `LocalRadiusQuery`, `SplatQueryResult`, `PosteriorSummary`, `PosteriorUncertaintySummary`, `ProvenanceSummary`, `SplatPosteriorView.uncertainty()` |
```

**How to copy it:** README can keep a shortened version of this table and link `docs/API.md` for full details. Update `mosaic.agents` to include implemented `RepresentationMemory` and tool/memory query symbols, not only posterior views.

**Boundary wording pattern to preserve, but update** (lines 157-178):
```markdown
## Backend and Dependency Boundary

Mosaic is a pure-Python headless library. Core imports are expected to work with `dependencies = []` and without accelerator stacks, native computer-vision stacks, robot middleware, browser services, or provider SDKs.

real 3DGS backend integration remains blocked until deterministic evaluation gates pass. Mosaic currently provides deterministic evaluation gates, typed failure classes, benchmark JSON/JSONL artifacts, and the `DeterministicSplatBackend` contract backend. It does not provide native 3DGS optimization integration or dependency expectations for production reconstruction backends.

`DeterministicSplatBackend` is a deterministic reference backend for contract tests, examples, replay validation, and benchmark smoke checks. It is not a real 3D Gaussian Splatting optimizer.

`ProvenancePreservingFusion` is a provenance-preserving contract strategy. It validates compatible map inputs, preserves and diagnoses splats, reports the stable machine-readable label `preserved_not_optimized`, does not optimize Gaussians, and does not collapse overlapping splats into occupancy-grid cells. It is not real Gaussian optimization, calibrated uncertainty minimization, loop closure, map alignment, or multi-session reconstruction.
```

**How to copy it:** keep blunt boundary style. Phase 08 must additionally name real 3DGS backends, ROS, Habitat, UI/WebSockets, LLM/LVLM providers, CUDA/native stacks, and production SLAM quality as out of v1 core scope. Do not leave `real 3DGS` lower-case sentence start.

---

### `docs/API.md` (documentation, transform)

**Analogs:** `src/mosaic/__init__.py`, `src/mosaic/core/__init__.py`, `src/mosaic/agents/__init__.py`, `tests/test_public_api.py`

**Root export import pattern** (`src/mosaic/__init__.py` lines 1-60):
```python
from mosaic.agents import (
    AgentQueryKind,
    ClaimStatus,
    EntityKind,
    EvidenceReference,
    LocalRadiusQuery,
    MemoryQueryResult,
    PosteriorSummary,
    PosteriorUncertaintySummary,
    ProvenanceSummary,
    QueryFamily,
    RepresentationMemory,
    SplatPosteriorView,
    SplatQueryResult,
    mark_stale_claims,
)
from mosaic.core import (
    CameraIntrinsics,
    CameraObservation,
    FrameId,
    ImageBuffer,
    ImageEncoding,
    MultiViewObservation,
    Pixel,
    Pose3,
    Quaternion,
    Timestamp,
    Translation3,
)
from mosaic.datasets import InMemorySequence, MultiViewSequence
from mosaic.evaluation import (
    BenchmarkArtifact,
    EvaluationReadinessResult,
    FailureClass,
    MetricResult,
    RegressionGate,
    RegressionResult,
    SyntheticScenario,
    check_regression_gates,
    evaluation_ready_for_real_backend,
    run_slam_benchmark,
    splat_count_metric,
    synthetic_forward_sequence,
    write_benchmark_artifact,
    write_benchmark_artifacts_jsonl,
)
from mosaic.fusion import FusionInput, FusionResult, FusionStatus, ProvenancePreservingFusion, SplatFusionStrategy
from mosaic.platforms import (
    CameraMount,
    CameraRig,
    Embodiment,
    PlatformDescription,
    PlatformRegistry,
    default_platform_registry,
    humanoid_stereo_rig,
    quadruped_front_rig,
    ugv_surround_rig,
)
from mosaic.slam import BackendCapabilities, DeterministicSplatBackend, SplatSlamBackend, SplatSlamUpdate, TrackingState
from mosaic.splats import GaussianSplat, SplatMap
```

**Root `__all__` pattern** (`src/mosaic/__init__.py` lines 62-128):
```python
__version__ = "0.1.0"

__all__ = [
    "AgentQueryKind",
    "BackendCapabilities",
    "BenchmarkArtifact",
    "CameraIntrinsics",
    "CameraMount",
    "CameraObservation",
    "CameraRig",
    "ClaimStatus",
    "DeterministicSplatBackend",
    "Embodiment",
    "EntityKind",
    "EvaluationReadinessResult",
    "EvidenceReference",
    "FailureClass",
    "FrameId",
    "FusionInput",
    "FusionResult",
    "FusionStatus",
    "GaussianSplat",
    "ImageBuffer",
    "ImageEncoding",
    "InMemorySequence",
    "LocalRadiusQuery",
    "MemoryQueryResult",
    "MetricResult",
    "MultiViewObservation",
    "MultiViewSequence",
    "Pixel",
    "PlatformDescription",
    "PlatformRegistry",
    "PosteriorSummary",
    "PosteriorUncertaintySummary",
    "ProvenancePreservingFusion",
    "ProvenanceSummary",
    "Pose3",
    "QueryFamily",
    "RegressionGate",
    "RepresentationMemory",
    "RegressionResult",
    "Quaternion",
    "SplatMap",
    "SplatFusionStrategy",
    "SplatPosteriorView",
    "SplatQueryResult",
    "SplatSlamBackend",
    "SyntheticScenario",
    "SplatSlamUpdate",
    "Timestamp",
    "TrackingState",
    "Translation3",
    "__version__",
    "check_regression_gates",
    "default_platform_registry",
    "evaluation_ready_for_real_backend",
    "humanoid_stereo_rig",
    "mark_stale_claims",
    "quadruped_front_rig",
    "run_slam_benchmark",
    "splat_count_metric",
    "synthetic_forward_sequence",
    "ugv_surround_rig",
    "write_benchmark_artifact",
    "write_benchmark_artifacts_jsonl",
]
```

**Subpackage barrel pattern** (`src/mosaic/core/__init__.py` lines 1-18):
```python
from mosaic.core.cameras import CameraIntrinsics, Pixel
from mosaic.core.frames import FrameId, Timestamp
from mosaic.core.observations import CameraObservation, ImageBuffer, ImageEncoding, MultiViewObservation
from mosaic.core.poses import Pose3, Quaternion, Translation3

__all__ = [
    "CameraIntrinsics",
    "CameraObservation",
    "FrameId",
    "ImageBuffer",
    "ImageEncoding",
    "MultiViewObservation",
    "Pixel",
    "Pose3",
    "Quaternion",
    "Timestamp",
    "Translation3",
]
```

**Agent API distinction pattern** (`src/mosaic/agents/__init__.py` lines 1-45, 47-89):
```python
from mosaic.agents.memory import (
    BeliefInspectionResult,
    BeliefProvenanceMemory,
    CellState,
    Claim,
    ClaimId,
    ClaimStatus,
    Commitment,
    CommitmentId,
    CommitmentMemory,
    CommitmentStatus,
    ContextNoteResult,
    CoordinationCommitmentResult,
    Entity,
    EntityId,
    EntityKind,
    EvidenceId,
    EvidenceKind,
    EvidenceReference,
    MemoryNote,
    MemoryQueryResult,
    NavigationCellResult,
    NoteId,
    PerceptionMatch,
    QueryFamily,
    Relation,
    RelationKind,
    RepresentationMemory,
    SceneGraphMemory,
    SourceId,
    SourceMetadata,
    SpatialCell,
    SpatialRasterMemory,
    TextMemory,
    mark_stale_claims,
)
from mosaic.agents.posteriors import SplatPosteriorView
from mosaic.agents.queries import (
    AgentQueryKind,
    LocalRadiusQuery,
    PosteriorSummary,
    PosteriorUncertaintySummary,
    ProvenanceSummary,
    SplatQueryResult,
)
```

**Public API test assertion pattern** (`tests/test_public_api.py` lines 157-180):
```python
def test_root_public_api_exports_selected_representation_symbols() -> None:
    root_exports = (
        RepresentationMemory,
        QueryFamily,
        ClaimStatus,
        EntityKind,
        EvidenceReference,
        MemoryQueryResult,
        mark_stale_claims,
    )

    assert all(export is not None for export in root_exports)
    assert RepresentationMemory is AgentRepresentationMemory
    assert QueryFamily is AgentQueryFamily
    assert ClaimStatus is AgentClaimStatus
    assert EntityKind is AgentEntityKind
    assert EvidenceReference is AgentEvidenceReference
    assert MemoryQueryResult is AgentMemoryQueryResult


def test_root_public_api_version_remains_stable() -> None:
    import mosaic

    assert mosaic.__version__ == "0.1.0"
```

**How to copy it:** build `docs/API.md` manually from explicit `__all__` surfaces. Include root exports and subpackage groupings. Use `tests/test_public_api.py` as the contract for which root symbols are stable. Do not generate docs via reflection or add Sphinx/MkDocs.

---

### `docs/EXAMPLES.md` (documentation, batch + file-I/O + request-response)

**Analogs:** `README.md`, `tests/evaluation/test_runner.py`, `tests/agents/test_splat_posterior.py`, `tests/agents/test_representation_memory.py`, `tests/evaluation/test_representation_scenarios.py`

**Existing benchmark artifact smoke example** (`README.md` lines 74-102):
```python
from pathlib import Path

from mosaic import (
    DeterministicSplatBackend,
    FrameId,
    RegressionGate,
    check_regression_gates,
    run_slam_benchmark,
    synthetic_forward_sequence,
    write_benchmark_artifact,
)

scenario = synthetic_forward_sequence(frame_count=3)
backend = DeterministicSplatBackend(map_frame=FrameId("map"))
artifact = run_slam_benchmark(scenario, backend)
write_benchmark_artifact(artifact, Path("benchmark.json"))
results = check_regression_gates(
    artifact,
    (RegressionGate(metric_name="splat_count", minimum=3.0),),
)

assert artifact.scenario_name == "synthetic-forward-3"
assert all(result.passed for result in results)
```

**Benchmark artifact behavior pattern** (`tests/evaluation/test_runner.py` lines 17-31, 169-189):
```python
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
```

```python
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
```

**Posterior query pattern** (`tests/agents/test_splat_posterior.py` lines 36-60, 98-107):
```python
def test_local_radius_query_returns_splat_indices_inside_radius() -> None:
    view = SplatPosteriorView(_map())

    result = view.query_local(LocalRadiusQuery(center=(0.0, 0.0, 0.0), radius=1.1))

    assert result.query_kind is AgentQueryKind.LOCAL_GEOMETRY
    assert result.splat_ids == (0, 1)
    assert result.count == 2
    assert result.total_matches == 2
    assert result.truncated is False


def test_local_radius_query_returns_bounded_tuple_order_results() -> None:
    view = SplatPosteriorView(_map())

    result = view.query_local(
        LocalRadiusQuery(center=(0.0, 0.0, 0.0), radius=10.0, max_results=2)
    )

    assert result.query_kind is AgentQueryKind.LOCAL_GEOMETRY
    assert result.splat_ids == (0, 1)
    assert result.count == 2
    assert result.total_matches == 3
    assert result.truncated is True
```

```python
def test_uncertainty_returns_global_descriptive_statistics() -> None:
    uncertainty = SplatPosteriorView(_map()).uncertainty()

    assert uncertainty.semantics == "descriptive_only"
    assert uncertainty.splat_count == 3
    assert uncertainty.mean_covariance_diagonal == (0.2, 0.2, 0.2)
    assert uncertainty.max_covariance_diagonal == (0.3, 0.3, 0.3)
    assert uncertainty.mean_opacity == 0.583333
    assert uncertainty.min_opacity == 0.25
    assert uncertainty.max_opacity == 1.0
```

**Representation memory endpoint pattern** (`tests/agents/test_representation_memory.py` lines 235-257):
```python
def test_query_navigation_frontiers_returns_bounded_cells() -> None:
    memory = (
        RepresentationMemory.empty(frame=FrameId("map"))
        .with_cell(_cell(coordinate=(1, 2), state=CellState.FRONTIER))
        .with_cell(
            _cell(
                coordinate=(2, 3),
                state=CellState.BLOCKED,
                traversability=0.1,
                claim_ids=(ClaimId("claim-2"),),
            )
        )
    )

    result = memory.query_navigation_frontiers(max_results=1)

    assert result.query_family is QueryFamily.NAVIGATION
    assert result.total_matches == 2
    assert result.truncated is True
    assert result.items[0].coordinate == (1, 2)
    assert result.items[0].state is CellState.FRONTIER
    assert result.items[0].traversability == 0.75
    assert result.items[0].claim_ids == (ClaimId("claim-1"),)
```

**Scenario-style memory setup pattern** (`tests/evaluation/test_representation_scenarios.py` lines 268-326):
```python
def _search_frontier_memory() -> RepresentationMemory:
    claim = _claim(
        claim_id=ClaimId("claim-frontier-north"),
        subject="cell-frontier-north",
        predicate="frontier_state",
        value="frontier",
        source=_source(SourceId("synthetic-frontier"), QueryFamily.NAVIGATION),
        confidence=0.75,
        status=ClaimStatus.ACTIVE,
        evidence=(
            _evidence(
                EvidenceId("evidence-frontier-north"),
                uri="mosaic://scenario/search-frontier/north",
            ),
        ),
    )
    cell = SpatialCell(
        frame=FrameId("map"),
        coordinate=(4, 7),
        resolution=0.5,
        state=CellState.FRONTIER,
        traversability=0.6,
        claim_ids=(claim.claim_id,),
        metadata={"cell_id": "cell-frontier-north"},
    )
    entity = Entity(
        entity_id=EntityId("entity-frontier-north"),
        kind=EntityKind.FRONTIER,
        label="north frontier",
        confidence=0.75,
        frame=FrameId("map"),
        claim_ids=(claim.claim_id,),
        metadata={"cell_id": "cell-frontier-north"},
    )
```

**How to copy it:** `docs/EXAMPLES.md` should present one narrative golden path: `synthetic_forward_sequence` → `DeterministicSplatBackend` → `run_slam_benchmark` and/or backend snapshot → `write_benchmark_artifact` → `SplatPosteriorView` bounded query → `RepresentationMemory` tool-style query. Keep snippets API-accurate but not a full standalone tutorial program. In tests, validate representative imports and behavior with `tmp_path` rather than executing Markdown code blocks.

---

### `CONTRIBUTING.md` (documentation, request-response)

**Analogs:** `pyproject.toml`, `tests/slam/test_backend_registry.py`, `tests/slam/test_backend_contract_helpers.py`, `src/mosaic/slam/registry.py`

**Dependency metadata pattern** (`pyproject.toml` lines 1-15, 17-23):
```toml
[project]
name = "mosaic"
version = "0.1.0"
description = "Typed Gaussian-splatting SLAM primitives for multi-view robotic perception"
readme = "README.md"
authors = [
    { name = "Prannaya Gupta", email = "prannayagupta@gmail.com" }
]
requires-python = ">=3.12"
dependencies = []

[dependency-groups]
dev = [
    "pytest>=8.4.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]

[build-system]
requires = ["uv_build>=0.10.10,<0.11.0"]
build-backend = "uv_build"
```

**Backend descriptor/availability pattern** (`tests/slam/test_backend_registry.py` lines 20-44, 101-127):
```python
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
```

```python
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
```

**Registry seam pattern** (`src/mosaic/slam/registry.py` lines 13-39, 41-82, 85-108):
```python
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
```

```python
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
```

**Contract helper pattern** (`tests/slam/test_backend_contract_helpers.py` lines 98-133):
```python
def test_contract_helpers_are_importable_from_slam_package() -> None:
    assert callable(assert_backend_lifecycle_contract)
    assert callable(assert_backend_deterministic_replay)
    assert callable(assert_backend_state_update_contract)
    assert callable(skip_unavailable_backend)


def test_contract_helper_skips_unavailable_descriptor_with_diagnostic() -> None:
    with pytest.raises(pytest.skip.Exception) as exc_info:
        skip_unavailable_backend(_unavailable_descriptor())

    reason = str(exc_info.value)
    assert (
        "mosaic_backend_missing_dependency_for_tests_zzz" in reason
        or "install optional backend" in reason
    )


def test_lifecycle_contract_helper_accepts_deterministic_backend_factory() -> None:
    assert_backend_lifecycle_contract(DeterministicSplatBackend)


def test_deterministic_replay_helper_compares_contract_level_outcomes() -> None:
    assert_backend_deterministic_replay(DeterministicSplatBackend)
```

**How to copy it:** contributor guidance should be policy-level: runtime dependencies stay empty for core, dev tests use pytest through uv, public API changes update `__all__` and docs/tests, heavy future backends must use optional dependency policy plus registry/adapter seams, availability checks, and contract helpers. Do not add placeholder extras to `pyproject.toml`; document the policy only.

---

### `tests/test_readme_contract.py` (test, file-I/O + request-response)

**Analog:** `tests/test_readme_contract.py`

**Imports and path constants pattern** (lines 1-7):
```python
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
PYPROJECT = ROOT / "pyproject.toml"
```

**Static contract lists pattern** (lines 9-52):
```python
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
```

**Reader helpers pattern** (lines 54-59):
```python
def _readme() -> str:
    return README.read_text(encoding="utf-8")


def _pyproject() -> str:
    return PYPROJECT.read_text(encoding="utf-8")
```

**Heading/command assertion pattern to update** (lines 62-75):
```python
def test_readme_contains_required_phase_1_headings_and_commands() -> None:
    readme = _readme()

    for heading in REQUIRED_HEADINGS:
        assert heading in readme

    for command in REQUIRED_COMMANDS:
        assert command in readme

    assert "73" in readme

    for module_name in REQUIRED_MODULES:
        assert module_name in readme
```

**How to copy it:** rename phase-era test and remove `assert "73" in readme`. Add assertions for `Mosaic v1 foundation`, links to `docs/API.md`, `docs/EXAMPLES.md`, and `CONTRIBUTING.md`, and absence of stale phase-facing language.

**Boundary-command guard pattern** (lines 77-89, 112-118):
```python
def test_readme_examples_preserve_dependency_boundary() -> None:
    readme = _readme()

    assert "not required for Phase 1" in readme
    assert "deferred, not required for Phase 1, and out of scope" in readme

    for line in readme.splitlines():
        normalized = line.casefold()
        for term in BOUNDARY_TERMS:
            if term in normalized:
                assert not normalized.startswith("pip install")
                assert not normalized.startswith("uv add")
                assert not normalized.startswith("uv pip install")
```

**How to copy it:** preserve the line scanner exactly. Replace Phase 1 assertions with v1/out-of-scope assertions and include `real 3dgs`, `ros`, `habitat`, `ui`, `websocket`, `llm`, `lvm`/`lvlm`, `cuda`, `native`, and `production slam` as required boundary terms.

**API smoke test pattern** (lines 121-145):
```python
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
```

**How to copy it:** keep representative import/API smoke tests, but move split-doc and golden-path checks to `tests/test_docs_contract.py` if keeping README tests small.

---

### `tests/test_docs_contract.py` (test, file-I/O + request-response)

**Analogs:** `tests/test_readme_contract.py`, `tests/test_public_api.py`, `tests/evaluation/test_runner.py`, `tests/agents/test_representation_memory.py`

**Split-doc existence and linking pattern from research, based on `tests/test_readme_contract.py` path style:**
```python
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
API_DOC = ROOT / "docs" / "API.md"
EXAMPLES_DOC = ROOT / "docs" / "EXAMPLES.md"
CONTRIBUTING = ROOT / "CONTRIBUTING.md"


def test_split_docs_exist_and_are_linked_from_readme() -> None:
    readme = README.read_text(encoding="utf-8")

    for relative_path in ("docs/API.md", "docs/EXAMPLES.md", "CONTRIBUTING.md"):
        assert (ROOT / relative_path).exists()
        assert relative_path in readme
```

**API docs root export assertion pattern** (`tests/test_public_api.py` lines 157-180 + doc file read):
```python
from mosaic import DeterministicSplatBackend, FrameId, RepresentationMemory, SplatPosteriorView


def test_api_docs_reference_current_root_exports() -> None:
    api_doc = API_DOC.read_text(encoding="utf-8")

    for name in (
        "DeterministicSplatBackend",
        "FrameId",
        "SplatPosteriorView",
        "RepresentationMemory",
        "MemoryQueryResult",
        "QueryFamily",
    ):
        assert name in api_doc
```

**Golden-path artifact test pattern** (`tests/evaluation/test_runner.py` lines 17-31, 169-189):
```python
from mosaic import DeterministicSplatBackend, FrameId, run_slam_benchmark, synthetic_forward_sequence
from mosaic import write_benchmark_artifact


def test_documented_golden_path_writes_local_artifact(tmp_path) -> None:
    artifact = run_slam_benchmark(
        scenario=synthetic_forward_sequence(frame_count=3),
        backend=DeterministicSplatBackend(map_frame=FrameId("map")),
    )
    output = tmp_path / "mosaic-benchmark.json"

    write_benchmark_artifact(artifact, output)

    assert artifact.scenario_name == "synthetic-forward-3"
    assert artifact.backend_name == "deterministic-splat"
    assert output.read_text(encoding="utf-8").endswith("\n")
```

**Representation memory endpoint assertion pattern** (`tests/agents/test_representation_memory.py` lines 235-257):
```python
from mosaic import FrameId, RepresentationMemory
from mosaic.agents import CellState, ClaimId, SpatialCell


def test_documented_memory_query_endpoint_is_bounded() -> None:
    memory = RepresentationMemory.empty(frame=FrameId("map")).with_cell(
        SpatialCell(
            frame=FrameId("map"),
            coordinate=(1, 2),
            resolution=0.5,
            state=CellState.FRONTIER,
            traversability=0.75,
            claim_ids=(ClaimId("claim-1"),),
        )
    )

    frontiers = memory.query_navigation_frontiers(max_results=1)

    assert frontiers.total_matches == 1
    assert frontiers.truncated is False
    assert frontiers.items[0].state is CellState.FRONTIER
```

**Contributor policy assertion pattern** (`pyproject.toml` lines 10-15 + backend registry names):
```python
def test_contributor_docs_lock_dependency_and_backend_policy() -> None:
    text = CONTRIBUTING.read_text(encoding="utf-8")
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert "dependencies = []" in pyproject
    for term in ("optional", "registry", "adapter", "availability", "contract test"):
        assert term in text.casefold()
```

**How to copy it:** new docs contract tests should be low-maintenance pytest tests over local Markdown plus small import/API smoke checks. Do not parse Markdown code blocks. Use `tmp_path` for disposable artifacts. Keep no network, provider SDK, ROS, Habitat, CUDA, or browser assumptions.

## Shared Patterns

### Public API source of truth
**Source:** `src/mosaic/__init__.py`, package `__init__.py` files, `tests/test_public_api.py`
**Apply to:** `README.md`, `docs/API.md`, `docs/EXAMPLES.md`, `tests/test_docs_contract.py`

Use explicit export surfaces and public API tests as the docs source of truth. Root symbols currently include `RepresentationMemory`, `MemoryQueryResult`, `QueryFamily`, `ClaimStatus`, `EntityKind`, `EvidenceReference`, `SplatPosteriorView`, benchmark writers, and evaluation readiness helpers.

### Pure-Python dependency boundary
**Source:** `pyproject.toml` lines 9-15; `README.md` lines 157-178; `tests/test_readme_contract.py` lines 83-89
**Apply to:** all public docs and doc tests

```toml
requires-python = ">=3.12"
dependencies = []

[dependency-groups]
dev = [
    "pytest>=8.4.0",
]
```

```python
for line in readme.splitlines():
    normalized = line.casefold()
    for term in BOUNDARY_TERMS:
        if term in normalized:
            assert not normalized.startswith("pip install")
            assert not normalized.startswith("uv add")
            assert not normalized.startswith("uv pip install")
```

### Deterministic artifact writing
**Source:** `src/mosaic/evaluation/runner.py` lines 96-132
**Apply to:** `docs/EXAMPLES.md`, `tests/test_docs_contract.py`

```python
def run_slam_benchmark(scenario: SyntheticScenario, backend: SplatSlamBackend) -> BenchmarkArtifact:
    backend.reset()
    update_count = 0
    updates = []
    diagnostics: dict[str, ArtifactValue] = {}
    for observation in scenario.sequence:
        update = backend.process(observation)
        updates.append(update)
        update_count += 1
        for key, value in update.diagnostics.items():
            diagnostics[f"last_{key}"] = value
    snapshot = backend.snapshot()
    diagnostics["snapshot_splat_count"] = len(snapshot)
    metrics = [
        *(metric.as_dict() for metric in lifecycle_metrics(updates, snapshot)),
        *(metric.as_dict() for metric in map_quality_metrics(snapshot, expected_frame=snapshot.frame)),
    ]
    _mirror_metric_diagnostics(metrics, diagnostics)
    return BenchmarkArtifact(
        scenario_name=scenario.name,
        backend_name=backend.name,
        update_count=update_count,
        metrics=metrics,
        backend_metadata=_backend_metadata(backend),
        diagnostics=diagnostics,
        failure_classification="none",
        scenario_summary=scenario_summary(
            scenario,
            update_count=update_count,
            expected_map_frame=snapshot.frame,
        ),
        gate_results=(),
    )


def write_benchmark_artifact(artifact: BenchmarkArtifact, path: Path) -> None:
    path.write_text(json.dumps(artifact.as_dict(), indent=2, sort_keys=True) + "\n")
```

### Backend registry and optional integration boundary
**Source:** `src/mosaic/slam/registry.py` lines 65-82, 85-108; `tests/slam/test_backend_registry.py` lines 101-127
**Apply to:** `CONTRIBUTING.md`, `docs/API.md` backend section

```python
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
```

### Bounded agent output boundary
**Source:** `tests/agents/test_splat_posterior.py` lines 48-60, 98-107; `tests/agents/test_representation_memory.py` lines 235-257
**Apply to:** `README.md`, `docs/API.md`, `docs/EXAMPLES.md`

Use `SplatPosteriorView` for bounded descriptive splat-snapshot queries and `RepresentationMemory` for higher provider-free memory/tool-style queries. Keep them separate in wording. Do not say posterior uncertainty is calibrated or production-grade; use `descriptive_only` semantics.

## No Analog Found

All planned Phase 08 files have usable analogs. There is no existing `CONTRIBUTING.md`, but contributor policy can copy patterns from `pyproject.toml`, backend registry code, and backend contract tests.

| File | Role | Data Flow | Reason |
|------|------|-----------|--------|
| None | — | — | Every planned file has at least a role-match or partial-role-match analog. |

## Metadata

**Analog search scope:** `/home/prannayag/pragnition/robotics/mosaic/README.md`, `/home/prannayag/pragnition/robotics/mosaic/pyproject.toml`, `/home/prannayag/pragnition/robotics/mosaic/src/mosaic/**`, `/home/prannayag/pragnition/robotics/mosaic/tests/**`, Phase 08 context/research files.
**Files scanned:** 55 listed Python/Markdown/TOML files plus canonical Phase 08 context and research files.
**Strong analogs read:** 13 files.
**Pattern extraction date:** 2026-05-21
