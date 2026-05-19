---
status: in_progress
quick_id: 260519-lpe
slug: convert-algorithms-to-sequential-flows
created_at: "2026-05-19T07:37:41.965Z"
---

# Quick Task Plan: Convert survey algorithms to sequential flows

Replace the current state-machine-style algorithm blocks in `research/slam-survey/main.tex` with ordered sequential pipeline algorithms for each surveyed method.

## Scope

- No new research; use existing survey evidence only.
- Preserve all seven systems and existing citations/diagrams.
- Each algorithm must show execution order, not just variables.
- Use compact stages with stage index, guard/trigger, state update, and emitted artifact.
- Compile and verify the PDF.

## Steps

1. Add or reuse compact LaTeX table formatting for sequential algorithm stages.
2. Replace the seven algorithm blocks with ordered stage-flow specs.
3. Run structural and citation checks.
4. Compile with Tectonic and verify `research/slam-survey/build/main.pdf`.
5. Record summary, update state, and commit relevant files only.
