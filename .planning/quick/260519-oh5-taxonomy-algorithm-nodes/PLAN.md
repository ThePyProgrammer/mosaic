---
status: in_progress
quick_id: 260519-oh5
slug: taxonomy-algorithm-nodes
created: 2026-05-19
---

Add one compact taxonomy-level algorithm box under each `Overall Architecture Taxonomy` subsection in `research/slam-survey/main.tex`.

## Scope

- Keep the existing section prose.
- Add algorithm boxes for:
  - Central-server submap and Gaussian fusion.
  - Distributed Gaussian consensus.
  - Submap-plus-pose-graph consistency.
  - Compact communication and monocular submap fusion.
  - Heterogeneous semantic shared Gaussian mapping.
- Use the shared notation from `Setting the Stage`.
- Use conventional `Input`, `Output`, and ordered procedural steps.
- Do not reintroduce `Trigger`, `Update`, or `Emits` labels.

## Validation

- Search for old algorithm labels.
- Check the taxonomy section contains the new algorithm labels.
- Compile the LaTeX paper with Tectonic.
- Run the Python test suite.
- Update quick summary and project state, then commit only task files.
