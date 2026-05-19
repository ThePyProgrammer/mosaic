---
status: in_progress
quick_id: 260519-m5r
slug: remove-repo-footnote-periods
created_at: "2026-05-19T08:05:00.000Z"
---

# Quick Task Plan: Remove repo footnote periods

Remove the trailing full stop from repository URL footnotes in `research/slam-survey/main.tex`.

## Scope

- Remove the period after repository `\url{...}` footnotes.
- Preserve citation text, prose, algorithms, figures, and tables.
- Compile and verify the updated PDF.

## Steps

1. Remove trailing periods from repository URL footnotes.
2. Run a structural check that no `\footnote{\url{...}.}` forms remain.
3. Compile with Tectonic and verify `research/slam-survey/build/main.pdf`.
4. Record summary, update state, and commit relevant files only.
