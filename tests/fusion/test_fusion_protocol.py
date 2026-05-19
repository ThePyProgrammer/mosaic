import math

import pytest

from mosaic.core import FrameId
from mosaic.fusion import (
    FusionConflictSummary,
    FusionInput,
    FusionProvenanceSummary,
    FusionResult,
    FusionStatus,
    FusionUncertaintySummary,
)
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


def test_fusion_input_defensively_freezes_maps() -> None:
    maps = [_map("map")]
    fusion_input = FusionInput(maps=maps)
    maps.append(_map("map"))

    assert isinstance(fusion_input.maps, tuple)
    assert len(fusion_input.maps) == 1
    assert fusion_input.frame == FrameId("map")


def test_fusion_provenance_summary_reports_counts_and_freezes_mapping() -> None:
    counts = {"front": 2, "rear": 1}
    summary = FusionProvenanceSummary(
        source_map_count=2,
        source_splat_count=3,
        fused_splat_count=3,
        per_provenance_counts=counts,
    )
    counts["front"] = 99

    assert summary.source_map_count == 2
    assert summary.source_splat_count == 3
    assert summary.fused_splat_count == 3
    assert summary.per_provenance_counts == {"front": 2, "rear": 1}
    with pytest.raises(TypeError):
        summary.per_provenance_counts["rear"] = 2


@pytest.mark.parametrize(
    "kwargs",
    [
        {"source_map_count": -1, "source_splat_count": 0, "fused_splat_count": 0},
        {"source_map_count": 0, "source_splat_count": -1, "fused_splat_count": 0},
        {"source_map_count": 0, "source_splat_count": 0, "fused_splat_count": -1},
        {
            "source_map_count": 0,
            "source_splat_count": 0,
            "fused_splat_count": 0,
            "per_provenance_counts": {"front": -1},
        },
    ],
)
def test_fusion_provenance_summary_rejects_negative_counts(kwargs: dict[str, object]) -> None:
    with pytest.raises(ValueError, match="non-negative"):
        FusionProvenanceSummary(**kwargs)


def test_fusion_provenance_summary_rejects_blank_provenance_names() -> None:
    with pytest.raises(ValueError, match="must not be blank"):
        FusionProvenanceSummary(per_provenance_counts={" ": 1})


def test_fusion_uncertainty_summary_exposes_covariance_stats() -> None:
    summary = FusionUncertaintySummary(
        model_label="preserved_not_optimized",
        covariance_diagonal_min=0.1,
        covariance_diagonal_max=0.3,
        covariance_diagonal_mean=0.2,
    )

    assert summary.model_label == "preserved_not_optimized"
    assert summary.covariance_diagonal_min == 0.1
    assert summary.covariance_diagonal_max == 0.3
    assert summary.covariance_diagonal_mean == 0.2


def test_fusion_uncertainty_summary_rejects_blank_label() -> None:
    with pytest.raises(ValueError, match="must not be blank"):
        FusionUncertaintySummary(model_label=" ")


@pytest.mark.parametrize("value", [-0.1, math.inf, math.nan])
def test_fusion_uncertainty_summary_rejects_invalid_covariance_stats(value: float) -> None:
    with pytest.raises(ValueError, match="finite non-negative"):
        FusionUncertaintySummary(covariance_diagonal_min=value)


def test_fusion_uncertainty_summary_rejects_max_less_than_min() -> None:
    with pytest.raises(ValueError, match="max.*min"):
        FusionUncertaintySummary(covariance_diagonal_min=0.3, covariance_diagonal_max=0.1)


def test_fusion_conflict_summary_reports_counts_and_freezes_mappings() -> None:
    pairs = {"front|rear": 1}
    reasons = {"overlap/color": 1}
    summary = FusionConflictSummary(
        total_candidate_count=1,
        involved_provenance_pairs=pairs,
        reason_counts=reasons,
    )
    pairs["front|rear"] = 99
    reasons["overlap/color"] = 99

    assert summary.total_candidate_count == 1
    assert summary.involved_provenance_pairs == {"front|rear": 1}
    assert summary.reason_counts == {"overlap/color": 1}
    with pytest.raises(TypeError):
        summary.involved_provenance_pairs["rear|front"] = 1
    with pytest.raises(TypeError):
        summary.reason_counts["overlap/opacity"] = 1


@pytest.mark.parametrize(
    "kwargs",
    [
        {"total_candidate_count": -1},
        {"involved_provenance_pairs": {"front|rear": -1}},
        {"reason_counts": {"overlap/color": -1}},
    ],
)
def test_fusion_conflict_summary_rejects_negative_counts(kwargs: dict[str, object]) -> None:
    with pytest.raises(ValueError, match="non-negative"):
        FusionConflictSummary(**kwargs)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"involved_provenance_pairs": {" ": 1}},
        {"reason_counts": {" ": 1}},
    ],
)
def test_fusion_conflict_summary_rejects_blank_mapping_keys(kwargs: dict[str, object]) -> None:
    with pytest.raises(ValueError, match="must not be blank"):
        FusionConflictSummary(**kwargs)


def test_fusion_conflict_summary_requires_details_when_total_is_positive() -> None:
    with pytest.raises(ValueError, match="details"):
        FusionConflictSummary(total_candidate_count=1)


def test_fusion_result_exposes_typed_summaries_and_flat_diagnostics() -> None:
    result = FusionResult(
        status=FusionStatus.FUSED,
        fused_map=_map(),
        diagnostics={
            "source_map_count": 2,
            "source_splat_count": 3,
            "fused_splat_count": 3,
            "fusion_uncertainty_model": "preserved_not_optimized",
            "fusion_conflict_candidate_count": 1,
        },
        provenance=FusionProvenanceSummary(
            source_map_count=2,
            source_splat_count=3,
            fused_splat_count=3,
            per_provenance_counts={"front": 2, "rear": 1},
        ),
        uncertainty=FusionUncertaintySummary(
            model_label="preserved_not_optimized",
            covariance_diagonal_min=0.1,
            covariance_diagonal_max=0.3,
            covariance_diagonal_mean=0.2,
        ),
        conflicts=FusionConflictSummary(
            total_candidate_count=1,
            involved_provenance_pairs={"front|rear": 1},
            reason_counts={"overlap/color": 1},
        ),
    )

    assert result.provenance.per_provenance_counts["front"] == 2
    assert result.uncertainty.model_label == "preserved_not_optimized"
    assert result.conflicts.reason_counts["overlap/color"] == 1
    assert result.diagnostics["fusion_uncertainty_model"] == "preserved_not_optimized"
    assert result.diagnostics["fusion_conflict_candidate_count"] == 1
    with pytest.raises(TypeError):
        result.diagnostics["source_map_count"] = 3


def test_fusion_result_supports_compatibility_default_summaries() -> None:
    result = FusionResult(
        status=FusionStatus.FUSED,
        fused_map=_map(),
        diagnostics={"source_map_count": 1},
    )

    assert result.diagnostics["source_map_count"] == 1
    assert result.provenance.source_map_count == 0
    assert result.provenance.per_provenance_counts == {}
    assert result.uncertainty.model_label
    assert result.conflicts.total_candidate_count == 0


@pytest.mark.parametrize(
    "diagnostics",
    [
        {" ": 1},
        {"source_map_count": object()},
        {"source_map_count": []},
        {"source_map_count": math.inf},
        {"source_map_count": math.nan},
    ],
)
def test_fusion_result_rejects_invalid_flat_diagnostics(diagnostics: dict[str, object]) -> None:
    with pytest.raises(ValueError, match="diagnostic"):
        FusionResult(status=FusionStatus.FUSED, fused_map=_map(), diagnostics=diagnostics)


def test_fusion_exports_summary_types_from_subpackage() -> None:
    import mosaic.fusion as fusion

    assert fusion.FusionProvenanceSummary is FusionProvenanceSummary
    assert fusion.FusionUncertaintySummary is FusionUncertaintySummary
    assert fusion.FusionConflictSummary is FusionConflictSummary
    assert set(fusion.__all__) >= {
        "FusionProvenanceSummary",
        "FusionUncertaintySummary",
        "FusionConflictSummary",
    }
