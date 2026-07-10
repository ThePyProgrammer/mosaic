---
quick_id: 260519-lon
status: planned
description: Set the LaTeX survey/template URL link font to use zlmtt monospace and verify the PDF build.
---

# Quick Task 260519-lon Plan

## Goal
Render survey URLs in the configured `zlmtt` monospace/typewriter font instead of inheriting XCharter roman text.

## Tasks
1. Replace the current `\urlstyle{same}` override in `research/slam-survey/googledeepmind.cls` with an explicit `\UrlFont` definition using `\ttfamily` after `zlmtt` loads.
2. Rebuild `research/slam-survey/main.tex` with Tectonic.
3. Inspect embedded PDF fonts to confirm typewriter URL text is present.
