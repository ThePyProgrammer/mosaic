import pytest

from mosaic.core import FrameId, Pose3, Quaternion, Translation3
from mosaic.slam.tracking import (
    FrameToFrameInitialization,
    FrameToModelRefinement,
    MagicTrackingDiagnostics,
    RgbdTrackingLoss,
    TrackingStage,
)


def _pose(x: float = 0.0) -> Pose3:
    return Pose3(
        parent_frame=FrameId("map"),
        child_frame=FrameId("camera/front"),
        translation=Translation3(x=x, y=0.0, z=0.0),
        rotation=Quaternion.identity(),
    )


def test_rgbd_tracking_loss_reports_total_and_masks() -> None:
    loss = RgbdTrackingLoss(
        color_l1=0.2,
        depth_l1=0.3,
        total=0.5,
        inlier_ratio=0.75,
        alpha_coverage=0.8,
    )

    assert loss.color_l1 == 0.2
    assert loss.depth_l1 == 0.3
    assert loss.total == 0.5
    assert loss.inlier_ratio == 0.75
    assert loss.alpha_coverage == 0.8


@pytest.mark.parametrize(
    ("kwargs", "message"),
    (
        ({"color_l1": -0.1, "depth_l1": 0.0, "total": 0.0}, "loss values"),
        ({"color_l1": 0.0, "depth_l1": 0.0, "total": -0.1}, "loss values"),
        ({"color_l1": 0.0, "depth_l1": 0.0, "total": 0.0, "inlier_ratio": 1.5}, "inlier_ratio"),
        ({"color_l1": 0.0, "depth_l1": 0.0, "total": 0.0, "alpha_coverage": -0.1}, "alpha_coverage"),
    ),
)
def test_rgbd_tracking_loss_validates_ranges(kwargs: dict[str, float], message: str) -> None:
    with pytest.raises(ValueError, match=message):
        RgbdTrackingLoss(**kwargs)


def test_tracking_diagnostics_preserve_reported_only_model() -> None:
    initialization = FrameToFrameInitialization(
        initial_pose=_pose(),
        registration_error=0.1,
        iterations=3,
        converged=True,
        diagnostics={"pyramid_levels": 3},
    )
    refinement = FrameToModelRefinement(
        refined_pose=_pose(0.1),
        loss=RgbdTrackingLoss(color_l1=0.1, depth_l1=0.2, total=0.3),
        iterations=5,
        converged=True,
        diagnostics={"masked_pixels": 128},
    )

    diagnostics = MagicTrackingDiagnostics(
        initialization=initialization,
        refinement=refinement,
        diagnostics={"source": "synthetic"},
    )

    assert initialization.stage is TrackingStage.FRAME_TO_FRAME_INITIALIZATION
    assert refinement.stage is TrackingStage.FRAME_TO_MODEL_REFINEMENT
    assert diagnostics.tracking_model == "reported_only"
    assert diagnostics.estimated_pose == refinement.refined_pose
    assert diagnostics.diagnostics["source"] == "synthetic"


def test_tracking_diagnostics_reject_invalid_iterations_and_model() -> None:
    with pytest.raises(ValueError, match="iterations must be non-negative"):
        FrameToFrameInitialization(
            initial_pose=_pose(),
            registration_error=0.0,
            iterations=-1,
            converged=False,
        )

    with pytest.raises(ValueError, match="JSON-ready scalar values"):
        FrameToModelRefinement(
            refined_pose=_pose(0.1),
            loss=RgbdTrackingLoss(color_l1=0.1, depth_l1=0.2, total=0.3),
            iterations=5,
            converged=True,
            diagnostics={"masked_pixels": [128]},
        )

    with pytest.raises(ValueError, match="non-blank string keys"):
        FrameToFrameInitialization(
            initial_pose=_pose(),
            registration_error=0.0,
            iterations=0,
            converged=False,
            diagnostics={"": 1},
        )

    with pytest.raises(ValueError, match="float values must be finite"):
        MagicTrackingDiagnostics(
            initialization=FrameToFrameInitialization(
                initial_pose=_pose(),
                registration_error=0.0,
                iterations=0,
                converged=False,
            ),
            refinement=FrameToModelRefinement(
                refined_pose=_pose(),
                loss=RgbdTrackingLoss(color_l1=0.0, depth_l1=0.0, total=0.0),
                iterations=0,
                converged=False,
            ),
            diagnostics={"rmse": float("inf")},
        )

    with pytest.raises(ValueError, match="tracking_model must be reported_only"):
        MagicTrackingDiagnostics(
            initialization=FrameToFrameInitialization(
                initial_pose=_pose(),
                registration_error=0.0,
                iterations=0,
                converged=False,
            ),
            refinement=FrameToModelRefinement(
                refined_pose=_pose(),
                loss=RgbdTrackingLoss(color_l1=0.0, depth_l1=0.0, total=0.0),
                iterations=0,
                converged=False,
            ),
            tracking_model="real_renderer",
        )
