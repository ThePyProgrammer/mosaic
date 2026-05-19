---
status: complete
quick_id: 260519-lrc
slug: remove-redundant-sources-appendix
created_at: "2026-05-19T07:31:25Z"
---

# Quick Task Plan: Remove redundant Sources Appendix

Remove the standalone Sources Appendix from the LaTeX survey now that canonical paper/project URLs are in BibTeX and implementation repositories are footnotes.

## Scope

- Modify `research/slam-survey/main.tex`.
- Modify `papers/robot-gaussian-slam-survey.md`.
- Do not run new research.
- Keep `\bibliography{references}` and all normal citations intact.
- Rebuild/verify the LaTeX package.

## Verification

- Check no `Sources Appendix` section remains in `main.tex`.
- Check the companion note no longer points readers to the removed appendix.
- Check all used citation keys are defined.
- Compile with Tectonic and verify the PDF artifact exists.
