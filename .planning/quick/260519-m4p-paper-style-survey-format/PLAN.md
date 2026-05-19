---
status: in_progress
quick_id: 260519-m4p
slug: paper-style-survey-format
created_at: "2026-05-19T08:00:00.000Z"
---

# Quick Task Plan: Paper-style survey format

Revise `research/slam-survey/main.tex` so the report reads like an academic survey paper rather than a developer brief for Mosaic.

## Scope

- Remove explicit Mosaic framing from the abstract, introduction, methodology, implications, and conclusion.
- Replace developer-facing guidance with neutral survey-paper discussion of methodology, comparative synthesis, limitations, and future work.
- Preserve the surveyed systems, citations, benchmark tables, algorithms, taxonomy figure, and evidence caveats.
- Compile and verify the updated PDF.

## Steps

1. Find and rewrite Mosaic/developer-brief wording in the survey body.
2. Run structural checks for absence of Mosaic/developer framing and preservation of key sections/artifacts.
3. Compile with Tectonic and verify `research/slam-survey/build/main.pdf`.
4. Record summary, update state, save durable user feedback, and commit relevant files only.
