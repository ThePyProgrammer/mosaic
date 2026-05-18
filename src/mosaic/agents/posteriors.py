from __future__ import annotations

from dataclasses import dataclass
from math import dist

from mosaic.agents.queries import AgentQueryKind, LocalRadiusQuery, PosteriorSummary, ProvenanceSummary, SplatQueryResult
from mosaic.splats import SplatMap


@dataclass(frozen=True, slots=True)
class SplatPosteriorView:
    splat_map: SplatMap

    def query_local(self, query: LocalRadiusQuery) -> SplatQueryResult:
        splat_ids = tuple(
            index
            for index, splat in enumerate(self.splat_map.splats)
            if dist(query.center, splat.center) <= query.radius
        )
        return SplatQueryResult(query_kind=AgentQueryKind.LOCAL_GEOMETRY, splat_ids=splat_ids)

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

    def provenance(self) -> ProvenanceSummary:
        counts: dict[str, int] = {}
        for splat in self.splat_map.splats:
            if splat.provenance is None:
                continue
            counts[splat.provenance] = counts.get(splat.provenance, 0) + 1
        return ProvenanceSummary(counts=counts)
