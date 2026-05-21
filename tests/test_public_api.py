from pathlib import Path

from mosaic import (
    AgentQueryKind,
    BenchmarkArtifact,
    CameraIntrinsics,
    CameraRig,
    ClaimStatus,
    DeterministicSplatBackend,
    Embodiment,
    EntityKind,
    EvaluationReadinessResult,
    EvidenceReference,
    FailureClass,
    FrameId,
    FusionInput,
    GaussianSplat,
    InMemorySequence,
    LocalRadiusQuery,
    MemoryQueryResult,
    PlatformRegistry,
    PosteriorUncertaintySummary,
    ProvenancePreservingFusion,
    QueryFamily,
    RegressionGate,
    RepresentationMemory,
    SplatMap,
    SplatPosteriorView,
    Timestamp,
    TrackingState,
    evaluation_ready_for_real_backend,
    mark_stale_claims,
    quadruped_front_rig,
    synthetic_forward_sequence,
    write_benchmark_artifacts_jsonl,
)
from mosaic.agents import (
    BeliefProvenanceMemory,
    CellState,
    Claim,
    ClaimStatus as AgentClaimStatus,
    CommitmentMemory,
    CommitmentStatus,
    EntityKind as AgentEntityKind,
    EvidenceKind,
    EvidenceReference as AgentEvidenceReference,
    MemoryQueryResult as AgentMemoryQueryResult,
    QueryFamily as AgentQueryFamily,
    RelationKind,
    RepresentationMemory as AgentRepresentationMemory,
    SceneGraphMemory,
    SpatialRasterMemory,
    TextMemory,
    mark_stale_claims as agent_mark_stale_claims,
)
from mosaic.evaluation import (
    FailureClass as EvaluationFailureClass,
    evaluation_ready_for_real_backend as evaluation_ready,
    write_benchmark_artifacts_jsonl as write_jsonl,
)


def test_public_api_exports_core_foundation_types() -> None:
    assert Timestamp.from_seconds(0.5).nanoseconds == 500_000_000
    assert FrameId("map").value == "map"
    assert CameraIntrinsics(width=1, height=1, fx=1.0, fy=1.0, cx=0.5, cy=0.5).width == 1
    assert GaussianSplat(center=(0.0, 0.0, 1.0), covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1)).opacity == 1.0
    assert len(SplatMap(frame=FrameId("map"))) == 0
    assert DeterministicSplatBackend().name == "deterministic-splat"
    assert TrackingState.TRACKING.value == "tracking"
    assert InMemorySequence.__name__ == "InMemorySequence"


def test_public_api_exports_platform_types() -> None:
    platform = quadruped_front_rig()

    assert platform.embodiment is Embodiment.QUADRUPED
    assert isinstance(platform.camera_rig, CameraRig)
    assert PlatformRegistry.__name__ == "PlatformRegistry"


def test_public_api_exports_fusion_types() -> None:
    assert FusionInput.__name__ == "FusionInput"
    assert ProvenancePreservingFusion().name == "provenance-preserving"


def test_public_api_exports_evaluation_types() -> None:
    scenario = synthetic_forward_sequence(frame_count=1)

    assert scenario.name == "synthetic-forward-1"
    assert BenchmarkArtifact.__name__ == "BenchmarkArtifact"
    assert RegressionGate(metric_name="splat_count", minimum=1.0).minimum == 1.0
    assert FailureClass.LIFECYCLE.value == "lifecycle"
    assert EvaluationFailureClass is FailureClass
    assert EvaluationReadinessResult.__name__ == "EvaluationReadinessResult"
    assert evaluation_ready is evaluation_ready_for_real_backend
    assert write_jsonl is write_benchmark_artifacts_jsonl


def test_readme_locks_real_backend_integration_block() -> None:
    readme = Path("README.md").read_text()

    assert "real 3DGS backend integration remains blocked until deterministic evaluation gates pass" in readme
    assert "DeterministicSplatBackend" in readme
    assert "metadata-only fake real backend" not in readme
    assert "sample descriptor" not in readme
    assert "cuda" not in readme.casefold()
    assert "pytorch" not in readme.casefold()
    assert "opencv" not in readme.casefold()
    assert "ros" not in readme.casefold()
    assert "habitat" not in readme.casefold()
    assert "openai" not in readme.casefold()
    assert "anthropic" not in readme.casefold()


def test_public_api_exports_agent_types() -> None:
    view = SplatPosteriorView(SplatMap(frame=FrameId("map")))
    query = LocalRadiusQuery(center=(0.0, 0.0, 0.0), radius=1.0)
    uncertainty = PosteriorUncertaintySummary(splat_count=0)

    assert query.kind is AgentQueryKind.LOCAL_GEOMETRY
    assert AgentQueryKind.UNCERTAINTY.value == "uncertainty"
    assert view.query_local(query).count == 0
    assert uncertainty.semantics == "descriptive_only"
    assert PosteriorUncertaintySummary.__name__ == "PosteriorUncertaintySummary"


def test_public_api_exports_representation_memory_from_agents() -> None:
    agent_exports = (
        AgentRepresentationMemory,
        SpatialRasterMemory,
        SceneGraphMemory,
        TextMemory,
        BeliefProvenanceMemory,
        CommitmentMemory,
        Claim,
        AgentClaimStatus,
        AgentEntityKind,
        RelationKind,
        EvidenceKind,
        AgentQueryFamily,
        CellState,
        CommitmentStatus,
        AgentEvidenceReference,
        AgentMemoryQueryResult,
        agent_mark_stale_claims,
    )

    assert all(export is not None for export in agent_exports)
    assert AgentRepresentationMemory is RepresentationMemory
    assert AgentQueryFamily.PERCEPTION.value == "perception"
    assert AgentClaimStatus.CONFLICTED.value == "conflicted"
    assert AgentEntityKind.FRONTIER.value == "frontier"
    assert AgentMemoryQueryResult.__name__ == "MemoryQueryResult"


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


def test_readme_locks_bounded_posterior_view_boundary() -> None:
    readme = Path("README.md").read_text()
    readme_lower = readme.casefold()

    assert "bounded descriptive posterior views" in readme
    assert "descriptive_only" in readme
    assert "not representation memories" in readme
    assert "Phase 7" in readme
    assert "LocalRadiusQuery" in readme
    assert "max_results" in readme
    assert "total_matches" in readme
    assert "truncated" in readme
    forbidden_as_implemented = (
        "implemented phase 6 scene graph memory",
        "implemented phase 6 spatial memory",
        "implemented phase 6 raster memory",
        "implemented phase 6 textual memory",
        "implemented phase 6 belief store",
        "implemented phase 6 provenance store",
        "implemented phase 6 commitment memory",
        "implemented phase 6 navigation tool",
        "implemented phase 6 perception tool",
        "implemented phase 6 coordination tool",
        "implemented phase 6 provider wrapper",
        "implemented phase 6 robot execution",
        "implemented phase 6 spatial indexing",
        "implemented phase 6 real backend",
    )
    assert all(phrase not in readme_lower for phrase in forbidden_as_implemented)
