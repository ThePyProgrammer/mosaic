from __future__ import annotations

from dataclasses import dataclass
from math import dist

from mosaic.agents.queries import (
    AgentQueryKind,
    LocalRadiusQuery,
    PosteriorSummary,
    PosteriorUncertaintySummary,
    ProvenanceSummary,
    SplatQueryResult,
)
from mosaic.splats import SplatMap


@dataclass(frozen=True, slots=True)
class SplatPosteriorView:
    splat_map: SplatMap

    def query_local(self, query: LocalRadiusQuery) -> SplatQueryResult:
        matching_ids: list[int] = []
        total_matches = 0
        for index, splat in enumerate(self.splat_map.splats):
            if dist(query.center, splat.center) > query.radius:
                continue
            total_matches += 1
            if len(matching_ids) < query.max_results:
                matching_ids.append(index)
        return SplatQueryResult(
            query_kind=AgentQueryKind.LOCAL_GEOMETRY,
            splat_ids=tuple(matching_ids),
            total_matches=total_matches,
            truncated=total_matches > len(matching_ids),
        )

    def summary(self) -> PosteriorSummary:
        splat_count = len(self.splat_map)
        provenances = {splat.provenance for splat in self.splat_map.splats if splat.provenance is not None}
        mean_opacity = 0.0
        if splat_count:
            mean_opacity = round(sum(splat.opacity for splat in self.splat_map.splats) / splat_count, 6)
        return PosteriorSummary(
            splat_count=splat_count,
            provenance_count=len(provenances),
            mean_opacity=mean_opacity,
        )

    def uncertainty(self) -> PosteriorUncertaintySummary:
        splat_count = len(self.splat_map)
        if splat_count == 0:
            return PosteriorUncertaintySummary(splat_count=0)

        covariance_diagonals = tuple(
            (splat.covariance_upper[0], splat.covariance_upper[3], splat.covariance_upper[5])
            for splat in self.splat_map.splats
        )
        mean_covariance_diagonal = tuple(
            round(sum(diagonal[axis] for diagonal in covariance_diagonals) / splat_count, 6)
            for axis in range(3)
        )
        max_covariance_diagonal = tuple(
            round(max(diagonal[axis] for diagonal in covariance_diagonals), 6)
            for axis in range(3)
        )
        opacities = tuple(splat.opacity for splat in self.splat_map.splats)
        return PosteriorUncertaintySummary(
            splat_count=splat_count,
            mean_covariance_diagonal=mean_covariance_diagonal,
            max_covariance_diagonal=max_covariance_diagonal,
            mean_opacity=round(sum(opacities) / splat_count, 6),
            min_opacity=round(min(opacities), 6),
            max_opacity=round(max(opacities), 6),
        )

    def provenance(self) -> ProvenanceSummary:
        counts: dict[str, int] = {}
        for splat in self.splat_map.splats:
            if splat.provenance is None:
                continue
            counts[splat.provenance] = counts.get(splat.provenance, 0) + 1
        return ProvenanceSummary(counts=counts)
