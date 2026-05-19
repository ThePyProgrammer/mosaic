---
status: complete
quick_id: 260519-lxx
slug: clean-github-footnote-labels
completed_at: "2026-05-19T07:38:21Z"
---

# Quick Task Summary: Clean GitHub footnote labels

Removed the method-specific `code repository:` labels from GitHub footnotes while keeping the repository URLs in footnotes.

## Files changed

- `research/slam-survey/main.tex`

## Verification

- No `code repository:` phrase remains in `research/slam-survey/main.tex`.
- GitHub repository URLs remain in footnotes.
- All citation keys used by `main.tex` are defined in `references.bib`.
- Tectonic compiled `research/slam-survey/main.tex` to `research/slam-survey/build/main.pdf`.
