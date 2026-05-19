---
status: in_progress
quick_id: 260519-lja
slug: formalize-survey-algorithms
created_at: "2026-05-19T07:30:20.700Z"
---

# Quick Task Plan: Formalize survey algorithms

Replace the current prose-like algorithm blocks in `research/slam-survey/main.tex` with formal staged process specifications for each surveyed method.

## Scope

- No new research; use existing survey evidence only.
- Keep the seven systems: MAGiC-SLAM, MAC-Ego3D, CoKo-SLAM, CoMA-SLAM, HAMMER, GRAND-SLAM, and MAGS-SLAM.
- Replace prose bullets with structured inputs, state variables, stage trackers, transitions, and outputs.
- Keep equations evidence-bounded and generic where papers do not expose exact implementation internals.
- Compile and verify the updated PDF.

## Steps

1. Add compact LaTeX helper macros for formal algorithm blocks if useful.
2. Replace the seven algorithm floats with formal staged process specifications.
3. Run citation/block checks.
4. Compile with Tectonic and verify `research/slam-survey/build/main.pdf`.
5. Record summary, update state, and commit relevant files only.
