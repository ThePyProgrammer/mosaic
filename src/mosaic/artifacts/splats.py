from __future__ import annotations

from typing import cast

from mosaic.artifacts.core import frame_id_from_artifact, frame_id_to_artifact
from mosaic.artifacts.schema import ArtifactDict, make_artifact, require_artifact
from mosaic.splats import GaussianSplat, SplatMap


def gaussian_splat_to_artifact(splat: GaussianSplat) -> ArtifactDict:
    return make_artifact(
        "mosaic.gaussian_splat",
        {
            "center": list(splat.center),
            "covariance_upper": list(splat.covariance_upper),
            "color_rgb": list(splat.color_rgb),
            "opacity": splat.opacity,
            "provenance": splat.provenance,
        },
    )


def gaussian_splat_from_artifact(artifact: object) -> GaussianSplat:
    payload = require_artifact(artifact, "mosaic.gaussian_splat")
    return GaussianSplat(
        center=tuple(cast(list[float], payload["center"])),
        covariance_upper=tuple(cast(list[float], payload["covariance_upper"])),
        color_rgb=tuple(cast(list[float], payload["color_rgb"])),
        opacity=cast(float, payload["opacity"]),
        provenance=cast(str | None, payload["provenance"]),
    )


def splat_map_to_artifact(splat_map: SplatMap) -> ArtifactDict:
    return make_artifact(
        "mosaic.splat_map",
        {
            "frame": frame_id_to_artifact(splat_map.frame),
            "splats": [gaussian_splat_to_artifact(splat) for splat in splat_map.splats],
        },
    )


def splat_map_from_artifact(artifact: object) -> SplatMap:
    payload = require_artifact(artifact, "mosaic.splat_map")
    return SplatMap(
        frame=frame_id_from_artifact(payload["frame"]),
        splats=tuple(gaussian_splat_from_artifact(splat) for splat in cast(list[object], payload["splats"])),
    )
