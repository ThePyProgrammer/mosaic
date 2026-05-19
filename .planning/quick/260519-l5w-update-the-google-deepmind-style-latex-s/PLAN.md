---
status: in_progress
quick_id: 260519-l5w
slug: update-the-google-deepmind-style-latex-s
created_at: "2026-05-19T07:14:16.880Z"
---

# Quick Task Plan: Mechanics-first method sections

Update `research/slam-survey/main.tex` so each surveyed method is explained through compact mechanics, an algorithm-style block, and a visual diagram rather than long prose.

## Scope

- No new research; use existing survey evidence only.
- Add LaTeX algorithm-style environments or equivalent pseudocode blocks.
- Add compact method diagrams for MAGiC-SLAM, MAC-Ego3D, CoKo-SLAM, CoMA-SLAM, HAMMER, GRAND-SLAM, and MAGS-SLAM.
- Reduce prose-heavy sections where practical.
- Compile and verify the updated PDF.

## Steps

1. Add lightweight algorithm/pseudocode macros to `main.tex`.
2. Replace the candidate systems section with mechanics-first subsections.
3. Run structural/citation checks.
4. Compile with Tectonic and verify `research/slam-survey/build/main.pdf`.
5. Record summary, update state, and commit relevant files only.
