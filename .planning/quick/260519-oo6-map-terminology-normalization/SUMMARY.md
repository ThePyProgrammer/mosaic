---
status: complete
quick_id: 260519-oo6
slug: map-terminology-normalization
completed: 2026-05-19
---

Normalized map terminology in `research/slam-survey/main.tex` so the paper consistently distinguishes agent-local maps, Gaussian submaps, Gaussian-surfel submaps, shared maps, and server-side shared maps.

## Completed

- Added an explicit terminology convention in `Setting the Stage` after the map definitions.
- Rewrote method mechanics, algorithm inputs/outputs, and algorithm steps so `\mathcal{M}_{i,t}` is described as an agent-local map.
- Rewrote bounded chunks `\mathcal{B}_{i}^{m}` and `\mathcal{S}_{i,t}` as Gaussian submaps or Gaussian-surfel submaps.
- Rewrote `\mathcal{G}_t` references as shared maps or server-side shared maps depending on ownership.
- Removed ambiguous uses of unqualified `local maps`, `local submaps`, `agent maps`, `server map`, and `global map`.

## Validation

- `rg -n -i -P "(?<!agent-)\\blocal\\s+(?:Gaussian\\s+)?(?:maps?|submaps?)\\b|(?<!-)\\bagent\\s+maps?\\b|\\bserver\\s+map\\b|\\bglobal\\s+map\\b|\\bglobally\\s+aligned\\s+Gaussian\\s+map\\b" research/slam-survey/main.tex` returned no matches.
- `rg -n "Trigger:|Update:|Emits:|TRACK|LOCALISE|COMMUNICATE|FUSE" research/slam-survey/main.tex` returned no matches.
- `tectonic -X compile research/slam-survey/main.tex --outdir research/slam-survey/build` generated `research/slam-survey/build/main.pdf`; only LaTeX/font/BibTeX warnings were reported.
- `uv run pytest` passed with 183 tests.
