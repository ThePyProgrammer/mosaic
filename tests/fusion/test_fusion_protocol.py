import pytest

from mosaic.core import FrameId
from mosaic.fusion import FusionInput, FusionResult, FusionStatus
from mosaic.splats import GaussianSplat, SplatMap


def _map(frame: str = "map") -> SplatMap:
    return SplatMap(
        frame=FrameId(frame),
        splats=(
            GaussianSplat(
                center=(0.0, 0.0, 1.0),
                covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1),
                provenance="camera/front",
            ),
        ),
    )


def test_fusion_input_requires_at_least_one_map() -> None:
    with pytest.raises(ValueError, match="at least one"):
        FusionInput(maps=())


def test_fusion_input_requires_matching_frames() -> None:
    with pytest.raises(ValueError, match="same frame"):
        FusionInput(maps=(_map("map"), _map("other")))


def test_fusion_input_exposes_common_frame() -> None:
    fusion_input = FusionInput(maps=(_map("map"), _map("map")))

    assert fusion_input.frame == FrameId("map")


def test_fusion_result_freezes_diagnostics_mapping() -> None:
    result = FusionResult(
        status=FusionStatus.FUSED,
        fused_map=_map(),
        diagnostics={"source_map_count": 1},
    )

    assert result.diagnostics["source_map_count"] == 1
    with pytest.raises(TypeError):
        result.diagnostics["source_map_count"] = 2
