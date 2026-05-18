from mosaic.core import FrameId
from mosaic.fusion import FusionInput, FusionStatus, ProvenancePreservingFusion
from mosaic.splats import GaussianSplat, SplatMap


def _splat(x: float, provenance: str) -> GaussianSplat:
    return GaussianSplat(
        center=(x, 0.0, 1.0),
        covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1),
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


def test_provenance_preserving_fusion_reports_diagnostics() -> None:
    first = SplatMap(frame=FrameId("map"), splats=(_splat(0.0, "front"), _splat(1.0, "left")))
    second = SplatMap(frame=FrameId("map"), splats=(_splat(2.0, "rear"),))

    result = ProvenancePreservingFusion().fuse(FusionInput(maps=(first, second)))

    assert result.diagnostics == {
        "source_map_count": 2,
        "source_splat_count": 3,
        "fused_splat_count": 3,
        "uncertainty_model": "preserved-not-optimized",
    }
