---
quick_id: 260519-lbz
status: planned
description: Diagnose and fix the LaTeX template link font issue: links appear in a weird serif font inconsistent with xcharter.
---

# Quick Task 260519-lbz Plan

## Goal
Diagnose why hyperlinks/URLs render in a font that does not match the XCharter text face and apply the smallest template-level fix.

## Tasks
1. Inspect `research/slam-survey/main.tex` and `research/slam-survey/googledeepmind.cls` for font and hyperlink configuration.
2. Patch the class/template so `\url` link text inherits the document roman font instead of the default URL typewriter font.
3. Rebuild the survey with the available LaTeX tool and inspect embedded fonts for the expected reduction in unrelated URL/typewriter fonts.
