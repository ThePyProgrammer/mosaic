---
status: in_progress
quick_id: 260519-lxg
slug: remove-method-flow-figures
created_at: "2026-05-19T07:47:20.166Z"
---

# Quick Task Plan: Remove method-flow figures

Remove the seven per-method method-flow TikZ figures from `research/slam-survey/main.tex` while preserving the formal sequential algorithm blocks and later taxonomy/benchmark visuals.

## Scope

- Remove figures labeled `fig:magic-flow`, `fig:mac-flow`, `fig:coko-flow`, `fig:coma-flow`, `fig:hammer-flow`, `fig:grand-flow`, and `fig:mags-flow`.
- Keep the seven algorithm blocks.
- Keep later figure/table environments such as the architecture taxonomy and benchmark tables.
- Compile and verify the updated PDF.

## Steps

1. Remove only the seven method-flow figure environments.
2. Run structural checks for removed labels, remaining algorithm blocks, and remaining later figures.
3. Compile with Tectonic and verify `research/slam-survey/build/main.pdf`.
4. Record summary, update state, and commit relevant files only.
