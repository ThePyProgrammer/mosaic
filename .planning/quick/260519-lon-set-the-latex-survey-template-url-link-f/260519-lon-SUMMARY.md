---
quick_id: 260519-lon
status: complete
date: 2026-05-19
---

# Quick Task 260519-lon Summary

## Result
Changed `research/slam-survey/googledeepmind.cls` so survey URLs render in a Latin Modern typewriter/mono face rather than inheriting XCharter roman text.

## Implementation
- Kept `zlmtt` for pdfTeX builds.
- Added a XeTeX/Tectonic path that sets `\ttfamily` to `lmmono10-regular.otf` with `Scale=1.1`.
- Set `\UrlFont` to `\ttfamily`.

## Verification
- Ran `tectonic -X compile "research/slam-survey/main.tex" --outdir "research/slam-survey/build"` successfully.
- Ran `pdffonts research/slam-survey/build/main.pdf`; the PDF now embeds `LMMono10-Regular-Identity-H`.
- Ran `pdftohtml -xml` on the rebuilt PDF; URL text maps to the `LMMono10` fontspec.

## Notes
A plain `\RequirePackage[scaled=1.1]{zlmtt}` plus `\ttfamily` resolved to Latin Modern Roman under the current Tectonic/XeTeX + XCharter setup, so the XeTeX path explicitly selects the Latin Modern Mono OpenType file.
