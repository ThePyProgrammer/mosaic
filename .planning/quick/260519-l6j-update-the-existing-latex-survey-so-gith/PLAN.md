---
status: complete
quick_id: 260519-l6j
slug: update-the-existing-latex-survey-so-gith
created_at: "2026-05-19T07:15:03.729Z"
---

# Quick Task Plan: Move GitHub references to footnotes

Update the existing LaTeX survey so GitHub repository references are presented as footnotes in the paper text instead of bibliography entries.

## Scope

- Modify `research/slam-survey/main.tex`.
- Modify `research/slam-survey/references.bib`.
- Do not run new research.
- Remove GitHub repository BibTeX entries for implementation availability.
- Replace repository citations in prose with `\footnote{...\url{...}}` entries.
- Remove GitHub code URLs from the Sources appendix while keeping paper/project/dataset URLs.
- Rebuild/verify the LaTeX package.

## Verification

- Check no `_code` citation keys remain in `main.tex`.
- Check no GitHub repository BibTeX entries remain for the surveyed systems.
- Check all used citation keys are defined.
- Compile with Tectonic and verify the PDF artifact exists.
