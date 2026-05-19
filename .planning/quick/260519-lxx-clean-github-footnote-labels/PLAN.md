---
status: complete
quick_id: 260519-lxx
slug: clean-github-footnote-labels
created_at: "2026-05-19T07:38:21Z"
---

# Quick Task Plan: Clean GitHub footnote labels

Remove the literal system-name plus code-repository label from method-specific GitHub footnotes while keeping the repository URLs as footnotes.

## Scope

- Modify `research/slam-survey/main.tex` only.
- Do not run new research.
- Preserve the GitHub repository URLs in footnotes.
- Rebuild/verify the LaTeX package.

## Verification

- Check no `code repository:` phrase remains in `main.tex`.
- Check GitHub URLs remain in footnotes.
- Check all used citation keys are defined.
- Compile with Tectonic and verify the PDF artifact exists.
