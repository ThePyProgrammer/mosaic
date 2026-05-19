---
status: in_progress
quick_id: 260519-m3s
slug: simplify-algorithm-blocks
created_at: "2026-05-19T07:54:56.959Z"
---

# Quick Task Plan: Simplify algorithm blocks

Rename the seven survey algorithm captions in `research/slam-survey/main.tex` to the method names only, remove the state tracker/state preamble from each block, and keep each algorithm as a normal ordered list of steps.

## Scope

- Rename captions to `MAGiC-SLAM`, `MAC-Ego3D`, `CoKo-SLAM`, `CoMA-SLAM`, `HAMMER`, `GRAND-SLAM`, and `MAGS-SLAM`.
- Remove the explicit `State:` / `stage tracker` preamble line from each algorithm block.
- Replace the custom `s=...` enumerate labels with plain ordered lists.
- Preserve citations, method prose, algorithm labels, algorithm step content, and later taxonomy/benchmark visuals.
- Compile and verify the updated PDF.

## Steps

1. Apply the minimal LaTeX algorithm caption and enumerate edits.
2. Run structural checks for captions, removed state trackers, remaining algorithms, and absent method-flow figures.
3. Compile with Tectonic and verify `research/slam-survey/build/main.pdf`.
4. Record summary, update state, and commit relevant files only.
