---
status: complete
quick_id: 260519-p4o
slug: restandardize-research-slam-survey-main-
completed: 2026-05-19
---

Restandardized `research/slam-survey/main.tex` around a local/global terminology split.

## Completed

- Replaced the previous agent-local/shared-map terminology contract with a local/global contract.
- Standardized `\mathcal{M}_{i,t}` prose as local map or local Gaussian map.
- Standardized `\mathcal{G}_t` prose as global map or global Gaussian map.
- Kept Gaussian submaps and Gaussian-surfel submaps as bounded chunks of local maps.
- Normalized method and taxonomy prose around local tracking, local mapping, local fusion, global tracking/alignment, and global fusion.
- Removed deprecated `agent-local` and `shared-*` terminology from the paper body and title.

## Validation

- `rg -n -i "agent-local|shared map|shared Gaussian|server-side shared|shared representation|shared state|shared mapper|shared frame|shared fusion|shared consistency|shared structure|shared-map|shared Gaussian-map|shared mapping|shared robotic" research/slam-survey/main.tex` returned no matches.
- `rg -n "Trigger:|Update:|Emits:|TRACK|LOCALISE|COMMUNICATE|FUSE" research/slam-survey/main.tex` returned no matches.
- `tectonic -X compile research/slam-survey/main.tex --outdir research/slam-survey/build` generated `research/slam-survey/build/main.pdf`; only existing LaTeX/font/BibTeX warnings were reported.
- `uv run pytest` passed with 183 tests.
