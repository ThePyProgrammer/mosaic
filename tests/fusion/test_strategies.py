from pytest import approx

from mosaic.core import FrameId
from mosaic.fusion import FusionInput, FusionStatus, ProvenancePreservingFusion
from mosaic.splats import GaussianSplat, SplatMap


def _splat(
    x: float,
    provenance: str,
    *,
    covariance_upper: tuple[float, float, float, float, float, float] = (
        0.1,
        0.0,
        0.0,
        0.1,
        0.0,
        0.1,
    ),
    color_rgb: tuple[float, float, float] = (1.0, 1.0, 1.0),
    opacity: float = 1.0,
) -> GaussianSplat:
    return GaussianSplat(
        center=(x, 0.0, 1.0),
        covariance_upper=covariance_upper,
        color_rgb=color_rgb,
        opacity=opacity,
        provenance=provenance,
    )


def test_provenance_preserving_fusion_concatenates_maps_without_mutating_inputs() -> None:
    first = SplatMap(frame=FrameId("map"), splats=(_splat(0.0, "front"),))
    second = SplatMap(frame=FrameId("map"), splats=(_splat(1.0, "rear"),))
    strategy = ProvenancePreservingFusion()

    result = strategy.fuse(FusionInput(maps=(first, second)))

    assert strategy.name == "provenance-preserving"
    assert result.status is FusionStatus.FUSED
    assert len(first) == 1
    assert len(second) == 1
    assert len(result.fused_map) == 2
    assert [splat.provenance for splat in result.fused_map.splats] == ["front", "rear"]


def test_provenance_preserving_fusion_reports_typed_provenance_and_flat_counts() -> None:
    first = SplatMap(frame=FrameId("map"), splats=(_splat(0.0, "front"), _splat(1.0, "left")))
    second = SplatMap(frame=FrameId("map"), splats=(_splat(2.0, "rear"),))

    result = ProvenancePreservingFusion().fuse(FusionInput(maps=(first, second)))

    assert result.status is FusionStatus.FUSED
    assert result.provenance.source_map_count == 2
    assert result.provenance.source_splat_count == 3
    assert result.provenance.fused_splat_count == 3
    assert dict(result.provenance.per_provenance_counts) == {
        "front": 1,
        "left": 1,
        "rear": 1,
    }
    assert result.diagnostics["source_map_count"] == 2
    assert result.diagnostics["source_splat_count"] == 3
    assert result.diagnostics["fused_splat_count"] == 3


def test_provenance_preserving_fusion_normalizes_blank_provenance_to_unknown() -> None:
    splat_map = SplatMap(frame=FrameId("map"), splats=(_splat(0.0, " "),))

    result = ProvenancePreservingFusion().fuse(FusionInput(maps=(splat_map,)))

    assert result.status is FusionStatus.FUSED
    assert result.provenance.per_provenance_counts == {"unknown": 1}


def test_provenance_preserving_fusion_reports_preserved_uncertainty_summary() -> None:
    first = SplatMap(
        frame=FrameId("map"),
        splats=(
            _splat(0.0, "front", covariance_upper=(0.1, 0.0, 0.0, 0.2, 0.0, 0.3)),
        ),
    )
    second = SplatMap(
        frame=FrameId("map"),
        splats=(
            _splat(1.0, "rear", covariance_upper=(0.4, 0.0, 0.0, 0.5, 0.0, 0.6)),
        ),
    )

    result = ProvenancePreservingFusion().fuse(FusionInput(maps=(first, second)))

    assert result.uncertainty.model_label == "preserved_not_optimized"
    assert result.uncertainty.covariance_diagonal_min == approx(0.1)
    assert result.uncertainty.covariance_diagonal_max == approx(0.6)
    assert result.uncertainty.covariance_diagonal_mean == approx(0.35)
    assert result.diagnostics["fusion_uncertainty_model"] == "preserved_not_optimized"


def test_provenance_preserving_fusion_preserves_overlapping_conflicting_splats() -> None:
    first = SplatMap(
        frame=FrameId("map"),
        splats=(
            _splat(
                0.0,
                "front",
                covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1),
                color_rgb=(1.0, 0.0, 0.0),
                opacity=1.0,
            ),
        ),
    )
    second = SplatMap(
        frame=FrameId("map"),
        splats=(
            _splat(
                0.0,
                "rear",
                covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1),
                color_rgb=(0.0, 0.0, 1.0),
                opacity=0.5,
            ),
        ),
    )

    result = ProvenancePreservingFusion().fuse(FusionInput(maps=(first, second)))

    assert result.status is FusionStatus.FUSED
    assert len(result.fused_map.splats) == 2
    assert [splat.provenance for splat in result.fused_map.splats] == ["front", "rear"]
    assert result.conflicts.total_candidate_count == 1
    assert result.conflicts.involved_provenance_pairs["front|rear"] == 1
    assert result.conflicts.reason_counts["overlap/color"] == 1
    assert result.conflicts.reason_counts["overlap/opacity"] == 1
    assert result.diagnostics["fusion_conflict_candidate_count"] == 1


def test_provenance_preserving_fusion_ignores_non_overlapping_splats_for_conflicts() -> None:
    first = SplatMap(frame=FrameId("map"), splats=(_splat(0.0, "front"),))
    second = SplatMap(
        frame=FrameId("map"),
        splats=(_splat(10.0, "rear", color_rgb=(0.0, 0.0, 1.0), opacity=0.5),),
    )

    result = ProvenancePreservingFusion().fuse(FusionInput(maps=(first, second)))

    assert result.status is FusionStatus.FUSED
    assert result.conflicts.total_candidate_count == 0
    assert result.diagnostics["fusion_conflict_candidate_count"] == 0
