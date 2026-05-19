---
status: in_progress
quick_id: 260519-oo6
slug: map-terminology-normalization
created: 2026-05-19
---

Normalize map terminology in `research/slam-survey/main.tex` so each term has one enforced meaning.

## Terminology Contract

- `agent-local map` / `agent-local Gaussian map`: use for `\mathcal{M}_{i,t}`, the full mutable map state owned by agent `i` at time `t`.
- `Gaussian submap` / `surfel submap`: use for `\mathcal{B}_{i}^{m}` or `\mathcal{S}_{i,t}` only when the method partitions an agent-local map into bounded chunks.
- `shared map` / `shared Gaussian map`: use for `\mathcal{G}_t`, the fused cross-agent map.
- `server-side shared map`: use for `\mathcal{G}_t` when the shared map is held by a central server.
- Avoid undefined variants such as `agent maps`, unqualified `local maps`, `global map`, or `server map` unless immediately tied to the formal symbol.

## Work

- Add a terminology paragraph/list in `Setting the Stage` after the map definitions.
- Normalize Existing Works algorithm inputs/outputs and steps.
- Normalize Overall Architecture Taxonomy prose and taxonomy algorithm inputs/steps.

## Validation

- Grep for ambiguous terms.
- Grep for old algorithm labels.
- Compile the LaTeX PDF with Tectonic.
- Run `uv run pytest`.
- Update quick summary and project state, then commit only task files.
