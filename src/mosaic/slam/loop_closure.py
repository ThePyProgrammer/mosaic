from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from math import isfinite, sqrt
from types import MappingProxyType
from typing import Mapping, Protocol, runtime_checkable

from mosaic.core.poses import Pose3, Quaternion, Translation3
from mosaic.slam.protocol import MetricValue
from mosaic.slam.submaps import GaussianSubmap, LoopId, SubmapReference


LOOP_DETECTION_MODEL = "deterministic_anchor_distance"


class LoopValidationStatus(StrEnum):
    CANDIDATE = "candidate"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


@dataclass(frozen=True, slots=True)
class LoopCandidate:
    loop_id: LoopId
    source: SubmapReference
    target: SubmapReference
    score: float
    confidence: float
    diagnostics: Mapping[str, MetricValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_distinct_references(self.source, self.target, "LoopCandidate")
        if not isfinite(self.score) or self.score < 0.0:
            raise ValueError("LoopCandidate score must be finite and nonnegative")
        _validate_confidence(self.confidence, "LoopCandidate confidence")
        object.__setattr__(self, "diagnostics", _validate_diagnostics(self.diagnostics, "LoopCandidate"))


@dataclass(frozen=True, slots=True)
class LoopEdge:
    loop_id: LoopId
    source: SubmapReference
    target: SubmapReference
    relative_pose: Pose3
    confidence: float
    status: LoopValidationStatus
    diagnostics: Mapping[str, MetricValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _validate_distinct_references(self.source, self.target, "LoopEdge")
        _validate_confidence(self.confidence, "LoopEdge confidence")
        if not isinstance(self.status, LoopValidationStatus) or self.status not in (
            LoopValidationStatus.ACCEPTED,
            LoopValidationStatus.REJECTED,
        ):
            raise ValueError("LoopEdge status must be accepted or rejected")
        object.__setattr__(self, "diagnostics", _validate_diagnostics(self.diagnostics, "LoopEdge"))


@dataclass(frozen=True, slots=True)
class LoopClosureResult:
    candidates: tuple[LoopCandidate, ...] = ()
    edges: tuple[LoopEdge, ...] = ()
    diagnostics: Mapping[str, MetricValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "candidates", tuple(self.candidates))
        object.__setattr__(self, "edges", tuple(self.edges))
        object.__setattr__(self, "diagnostics", _validate_diagnostics(self.diagnostics, "LoopClosureResult"))


@runtime_checkable
class LoopClosureStrategy(Protocol):
    @property
    def name(self) -> str:
        raise NotImplementedError

    def detect(self, submaps: Sequence[GaussianSubmap]) -> LoopClosureResult:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class DeterministicLoopClosureStrategy:
    max_anchor_distance: float = 0.5
    min_confidence: float = 0.1

    def __post_init__(self) -> None:
        if not isfinite(self.max_anchor_distance) or self.max_anchor_distance <= 0.0:
            raise ValueError("DeterministicLoopClosureStrategy max_anchor_distance must be finite and positive")
        _validate_confidence(self.min_confidence, "DeterministicLoopClosureStrategy min_confidence")

    @property
    def name(self) -> str:
        return "deterministic-anchor-distance"

    def detect(self, submaps: Sequence[GaussianSubmap]) -> LoopClosureResult:
        candidates: list[LoopCandidate] = []
        edges: list[LoopEdge] = []

        loop_index = 1
        for source_index, source in enumerate(submaps):
            for target in submaps[source_index + 1 :]:
                if source.agent_id == target.agent_id:
                    continue
                if source.map_frame != target.map_frame:
                    continue

                distance = _anchor_distance(source.anchor, target.anchor)
                if distance > self.max_anchor_distance:
                    continue

                confidence = max(0.0, 1.0 - (distance / self.max_anchor_distance))
                loop_id = LoopId(f"loop-{loop_index}")
                loop_index += 1
                diagnostics: Mapping[str, MetricValue] = {
                    "anchor_distance": distance,
                    "loop_detection_model": LOOP_DETECTION_MODEL,
                }
                candidates.append(
                    LoopCandidate(
                        loop_id=loop_id,
                        source=source.reference,
                        target=target.reference,
                        score=distance,
                        confidence=confidence,
                        diagnostics=diagnostics,
                    )
                )
                status = (
                    LoopValidationStatus.ACCEPTED
                    if confidence >= self.min_confidence
                    else LoopValidationStatus.REJECTED
                )
                edges.append(
                    LoopEdge(
                        loop_id=loop_id,
                        source=source.reference,
                        target=target.reference,
                        relative_pose=_relative_anchor_pose(source, target),
                        confidence=confidence,
                        status=status,
                        diagnostics=diagnostics,
                    )
                )

        return LoopClosureResult(
            candidates=tuple(candidates),
            edges=tuple(edges),
            diagnostics={
                "loop_detection_model": LOOP_DETECTION_MODEL,
                "candidate_count": len(candidates),
                "edge_count": len(edges),
            },
        )


def _relative_anchor_pose(source: GaussianSubmap, target: GaussianSubmap) -> Pose3:
    return Pose3(
        parent_frame=source.local_frame,
        child_frame=target.local_frame,
        translation=Translation3(
            x=source.anchor[0] - target.anchor[0],
            y=source.anchor[1] - target.anchor[1],
            z=source.anchor[2] - target.anchor[2],
        ),
        rotation=Quaternion.identity(),
    )


def _anchor_distance(source: tuple[float, float, float], target: tuple[float, float, float]) -> float:
    dx = source[0] - target[0]
    dy = source[1] - target[1]
    dz = source[2] - target[2]
    return sqrt((dx * dx) + (dy * dy) + (dz * dz))


def _validate_distinct_references(source: SubmapReference, target: SubmapReference, label: str) -> None:
    if source == target:
        raise ValueError(f"{label} source and target must be different submaps")


def _validate_confidence(confidence: float, label: str) -> None:
    if not isfinite(confidence) or confidence < 0.0 or confidence > 1.0:
        raise ValueError(f"{label} must be finite and in [0, 1]")


def _validate_diagnostics(diagnostics: Mapping[str, MetricValue], label: str) -> Mapping[str, MetricValue]:
    frozen: dict[str, MetricValue] = {}
    for key, value in diagnostics.items():
        if not isinstance(key, str) or not key.strip():
            raise ValueError(f"{label} diagnostics must use non-blank string keys")
        if not isinstance(value, bool | int | float | str):
            raise ValueError(f"{label} diagnostics must use JSON-ready scalar values")
        if isinstance(value, float) and not isfinite(value):
            raise ValueError(f"{label} diagnostic float values must be finite")
        frozen[key] = value
    return MappingProxyType(frozen)


__all__ = [
    "LOOP_DETECTION_MODEL",
    "DeterministicLoopClosureStrategy",
    "LoopCandidate",
    "LoopClosureResult",
    "LoopClosureStrategy",
    "LoopEdge",
    "LoopValidationStatus",
]
