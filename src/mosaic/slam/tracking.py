from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from math import isfinite
from types import MappingProxyType
from typing import Mapping

from mosaic.core import Pose3
from mosaic.slam.protocol import MetricValue


class TrackingStage(StrEnum):
    FRAME_TO_FRAME_INITIALIZATION = "frame_to_frame_initialization"
    FRAME_TO_MODEL_REFINEMENT = "frame_to_model_refinement"


@dataclass(frozen=True, slots=True)
class RgbdTrackingLoss:
    color_l1: float
    depth_l1: float
    total: float
    inlier_ratio: float | None = None
    alpha_coverage: float | None = None

    def __post_init__(self) -> None:
        loss_values = (self.color_l1, self.depth_l1, self.total)
        if any(not isfinite(value) or value < 0.0 for value in loss_values):
            raise ValueError("RgbdTrackingLoss loss values must be finite non-negative values")
        _validate_optional_unit_interval(self.inlier_ratio, "inlier_ratio")
        _validate_optional_unit_interval(self.alpha_coverage, "alpha_coverage")


@dataclass(frozen=True, slots=True)
class FrameToFrameInitialization:
    initial_pose: Pose3
    registration_error: float
    iterations: int
    converged: bool
    diagnostics: Mapping[str, MetricValue] = field(default_factory=dict)
    stage: TrackingStage = TrackingStage.FRAME_TO_FRAME_INITIALIZATION

    def __post_init__(self) -> None:
        if self.stage is not TrackingStage.FRAME_TO_FRAME_INITIALIZATION:
            raise ValueError("FrameToFrameInitialization stage must be frame_to_frame_initialization")
        if not isfinite(self.registration_error) or self.registration_error < 0.0:
            raise ValueError("FrameToFrameInitialization registration_error must be finite and non-negative")
        if self.iterations < 0:
            raise ValueError("FrameToFrameInitialization iterations must be non-negative")
        object.__setattr__(self, "diagnostics", _validate_diagnostics(self.diagnostics))


@dataclass(frozen=True, slots=True)
class FrameToModelRefinement:
    refined_pose: Pose3
    loss: RgbdTrackingLoss
    iterations: int
    converged: bool
    diagnostics: Mapping[str, MetricValue] = field(default_factory=dict)
    stage: TrackingStage = TrackingStage.FRAME_TO_MODEL_REFINEMENT

    def __post_init__(self) -> None:
        if self.stage is not TrackingStage.FRAME_TO_MODEL_REFINEMENT:
            raise ValueError("FrameToModelRefinement stage must be frame_to_model_refinement")
        if self.iterations < 0:
            raise ValueError("FrameToModelRefinement iterations must be non-negative")
        object.__setattr__(self, "diagnostics", _validate_diagnostics(self.diagnostics))


@dataclass(frozen=True, slots=True)
class MagicTrackingDiagnostics:
    initialization: FrameToFrameInitialization
    refinement: FrameToModelRefinement
    tracking_model: str = "reported_only"
    diagnostics: Mapping[str, MetricValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.tracking_model != "reported_only":
            raise ValueError("MagicTrackingDiagnostics tracking_model must be reported_only")
        object.__setattr__(self, "diagnostics", _validate_diagnostics(self.diagnostics))

    @property
    def estimated_pose(self) -> Pose3:
        return self.refinement.refined_pose


def _validate_diagnostics(diagnostics: Mapping[str, MetricValue]) -> Mapping[str, MetricValue]:
    frozen: dict[str, MetricValue] = {}
    for key, value in diagnostics.items():
        if not isinstance(key, str) or not key.strip():
            raise ValueError("Tracking diagnostics must use non-blank string keys")
        if not isinstance(value, bool | int | float | str):
            raise ValueError("Tracking diagnostics must use JSON-ready scalar values")
        if isinstance(value, float) and not isfinite(value):
            raise ValueError("Tracking diagnostic float values must be finite")
        frozen[key] = value
    return MappingProxyType(frozen)


def _validate_optional_unit_interval(value: float | None, name: str) -> None:
    if value is None:
        return
    if not isfinite(value) or value < 0.0 or value > 1.0:
        raise ValueError(f"RgbdTrackingLoss {name} must be between 0 and 1")


__all__ = [
    "FrameToFrameInitialization",
    "FrameToModelRefinement",
    "MagicTrackingDiagnostics",
    "RgbdTrackingLoss",
    "TrackingStage",
]
