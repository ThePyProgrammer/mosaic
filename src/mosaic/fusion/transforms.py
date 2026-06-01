from __future__ import annotations

from mosaic.core import FrameId, Pose3
from mosaic.splats import GaussianSplat, SplatMap

COVARIANCE_TRANSFORM_MODEL = "center_only_reference"


def transform_splat_map(
    splat_map: SplatMap,
    transform: Pose3,
    *,
    frame: FrameId,
    provenance_prefix: str | None = None,
) -> SplatMap:
    if transform.child_frame != splat_map.frame:
        raise ValueError("transform child_frame must match splat_map frame")
    if transform.parent_frame != frame:
        raise ValueError("transform parent_frame must match target frame")

    transformed_splats = tuple(
        GaussianSplat(
            center=transform.apply_to_point(splat.center),
            covariance_upper=splat.covariance_upper,
            color_rgb=splat.color_rgb,
            opacity=splat.opacity,
            provenance=_transform_provenance(splat.provenance, provenance_prefix),
        )
        for splat in splat_map.splats
    )
    return SplatMap(frame=frame, splats=transformed_splats)


def _transform_provenance(provenance: str | None, provenance_prefix: str | None) -> str | None:
    if provenance_prefix is None:
        return provenance
    if provenance is None or not provenance.strip():
        return f"{provenance_prefix}:unknown"
    return f"{provenance_prefix}:{provenance}"


__all__ = ["COVARIANCE_TRANSFORM_MODEL", "transform_splat_map"]
