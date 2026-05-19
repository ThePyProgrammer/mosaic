---
status: in_progress
quick_id: 260519-p4o
slug: restandardize-research-slam-survey-main-
created: 2026-05-19
---

Restandardize `research/slam-survey/main.tex` around a local/global terminology split.

## Terminology Contract

- `local map` / `local Gaussian map`: use for `\mathcal{M}_{i,t}`, the mutable Gaussian state maintained by one agent before cross-agent alignment or fusion.
- `Gaussian submap` / `Gaussian-surfel submap`: use for `\mathcal{B}_{i}^{m}` or `\mathcal{S}_{i,t}` only when a method partitions a local map into bounded chunks.
- `global map` / `global Gaussian map`: use for `\mathcal{G}_t`, the fused cross-agent map, including maps held by a central server.
- `local tracking`: use for per-agent pose estimation against local frames/maps.
- `global tracking` / `global alignment`: use for cross-agent pose, frame, or trajectory alignment against `\mathcal{F}_0` or `\mathcal{G}_t`.
- `local fusion`: use for within-agent updates into `\mathcal{M}_{i,t}` or its submaps.
- `global fusion`: use for cross-agent fusion into `\mathcal{G}_t`.
- Avoid `agent-local map`, `shared map`, `server-side shared map`, `shared mapper`, `shared frame`, and `shared state` unless quoted as old terminology or immediately clarifying the local/global split.

## Work

- Replace the Setting the Stage terminology paragraph with the local/global contract.
- Normalize Existing Works method prose, algorithm inputs/outputs, and steps.
- Normalize Overall Architecture Taxonomy prose and taxonomy algorithm inputs/outputs/steps.
- Preserve the math symbols and keep submaps as bounded chunks rather than replacing them with maps.

## Validation

- Grep for deprecated terminology: `agent-local`, `shared map`, `server-side shared`, `shared mapper`, `shared frame`, `shared state`.
- Grep for local/global coverage: `local map`, `global map`, `local tracking`, `global tracking`, `local fusion`, `global fusion`.
- Grep for old algorithm labels: `Trigger`, `Update`, `Emits`, `TRACK`, `LOCALISE`, `COMMUNICATE`, `FUSE`.
- Compile the LaTeX PDF with Tectonic.
- Run `uv run pytest`.
- Update quick summary and project state, then commit only task files.
