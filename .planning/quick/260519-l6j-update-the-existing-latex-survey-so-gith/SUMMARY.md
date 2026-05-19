---
status: complete
quick_id: 260519-l6j
slug: update-the-existing-latex-survey-so-gith
completed_at: "2026-05-19T07:30:00Z"
---

# Quick Task Summary: Move GitHub references to footnotes

Updated the LaTeX survey so public code repositories are cited as footnotes in the paper text rather than as bibliography entries.

## Files changed

- `research/slam-survey/main.tex`
- `research/slam-survey/references.bib`

## Verification

- No `_code` citation keys remain in `research/slam-survey/main.tex`.
- No GitHub repository URLs remain in `research/slam-survey/references.bib`.
- All citation keys used by `main.tex` are defined in `references.bib`.
- Tectonic compiled `research/slam-survey/main.tex` to `research/slam-survey/build/main.pdf`.

## Notes

GitHub repository URLs remain only in footnotes near the relevant systems: MAGiC-SLAM, MAC-Ego3D, CoKo-SLAM, and CoMA-SLAM.
