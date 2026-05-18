import json

import pytest

from mosaic.artifacts import (
    gaussian_splat_from_artifact,
    gaussian_splat_to_artifact,
    require_artifact,
    splat_map_from_artifact,
    splat_map_to_artifact,
)
from mosaic.core import FrameId
from mosaic.splats import GaussianSplat, SplatMap


def _splat() -> GaussianSplat:
    return GaussianSplat(
        center=(1.0, 2.0, 3.0),
        covariance_upper=(1.0, 0.2, 0.3, 2.0, 0.4, 3.0),
        color_rgb=(0.2, 0.3, 0.4),
        opacity=0.75,
        provenance="front-camera",
    )


def _assert_json_ready(artifact: dict[str, object]) -> None:
    json.dumps(artifact, sort_keys=True)


def test_gaussian_splat_artifact_round_trips() -> None:
    splat = _splat()
    artifact = gaussian_splat_to_artifact(splat)

    _assert_json_ready(artifact)
    assert gaussian_splat_from_artifact(artifact) == splat


def test_gaussian_splat_artifact_preserves_covariance_upper_order() -> None:
    artifact = gaussian_splat_to_artifact(_splat())
    payload = require_artifact(artifact, "mosaic.gaussian_splat")

    assert payload["covariance_upper"] == [1.0, 0.2, 0.3, 2.0, 0.4, 3.0]


def test_splat_map_artifact_round_trips_frame_and_splats() -> None:
    splat_map = SplatMap(frame=FrameId("map"), splats=(_splat(),))
    artifact = splat_map_to_artifact(splat_map)

    _assert_json_ready(artifact)
    assert splat_map_from_artifact(artifact) == splat_map


def test_gaussian_splat_artifact_rejects_unknown_schema_version() -> None:
    artifact = gaussian_splat_to_artifact(_splat())
    artifact["schema_version"] = 2

    with pytest.raises(ValueError, match="schema_version"):
        gaussian_splat_from_artifact(artifact)
