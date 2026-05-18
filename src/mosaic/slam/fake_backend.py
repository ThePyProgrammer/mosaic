from __future__ import annotations

from dataclasses import dataclass, field

from mosaic.core.frames import FrameId
from mosaic.core.observations import MultiViewObservation
from mosaic.slam.protocol import BackendCapabilities, SplatSlamUpdate, TrackingState
from mosaic.splats import GaussianSplat, SplatMap


@dataclass(slots=True)
class DeterministicSplatBackend:
    map_frame: FrameId = field(default_factory=lambda: FrameId("map"))
    _splats: list[GaussianSplat] = field(default_factory=list, init=False, repr=False)

    @property
    def name(self) -> str:
        return "deterministic-splat"

    @property
    def capabilities(self) -> BackendCapabilities:
        return BackendCapabilities(
            supports_multi_view=True,
            supports_incremental_mapping=True,
            supports_uncertainty=False,
            runs_out_of_process=False,
            parameters={"deterministic": True},
        )

    def reset(self) -> None:
        self._splats.clear()

    def process(self, observation: MultiViewObservation) -> SplatSlamUpdate:
        index = len(self._splats)
        first_view = observation.views[0]
        splat = GaussianSplat(
            center=(float(index), 0.0, 1.0),
            covariance_upper=(0.01, 0.0, 0.0, 0.01, 0.0, 0.01),
            color_rgb=(1.0, 1.0, 1.0),
            opacity=1.0,
            provenance=first_view.camera_id,
        )
        self._splats.append(splat)
        return SplatSlamUpdate(
            timestamp=observation.timestamp,
            tracking_state=TrackingState.TRACKING,
            estimated_pose=first_view.camera_pose,
            map_update=SplatMap(frame=self.map_frame, splats=(splat,)),
            diagnostics={"splat_count": len(self._splats)},
        )

    def snapshot(self) -> SplatMap:
        return SplatMap(frame=self.map_frame, splats=tuple(self._splats))
