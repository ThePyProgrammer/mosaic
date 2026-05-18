from __future__ import annotations

from dataclasses import dataclass

from mosaic.fusion.protocol import FusionInput, FusionResult, FusionStatus
from mosaic.splats import GaussianSplat, SplatMap


@dataclass(frozen=True, slots=True)
class ProvenancePreservingFusion:
    @property
    def name(self) -> str:
        return "provenance-preserving"

    def fuse(self, fusion_input: FusionInput) -> FusionResult:
        fused_splats: list[GaussianSplat] = []
        for splat_map in fusion_input.maps:
            fused_splats.extend(splat_map.splats)
        fused_map = SplatMap(frame=fusion_input.frame, splats=tuple(fused_splats))
        return FusionResult(
            status=FusionStatus.FUSED,
            fused_map=fused_map,
            diagnostics={
                "source_map_count": len(fusion_input.maps),
                "source_splat_count": len(fused_splats),
                "fused_splat_count": len(fused_map),
                "uncertainty_model": "preserved-not-optimized",
            },
        )
