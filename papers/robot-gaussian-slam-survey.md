# Collaborative Gaussian SLAM for Multi-Robot Mapping

The authoritative LaTeX survey package for this draft is in `research/slam-survey/`.

## Files

- `research/slam-survey/main.tex` — Google DeepMind-style survey source.
- `research/slam-survey/references.bib` — BibTeX references for the surveyed systems and datasets.
- `research/slam-survey/googledeepmind.cls` — local copy of the Google DeepMind class file, lightly patched for the local Tectonic/XeTeX build path.
- `research/slam-survey/build/main.pdf` — compiled verification artifact produced with Tectonic.

## Scope

This survey covers the key open/public and paper-only candidates for multi-robot or multi-agent online Gaussian SLAM: MAGiC-SLAM, MAC-Ego3D, CoKo-SLAM, CoMA-SLAM, HAMMER, GRAND-SLAM, and MAGS-SLAM. It uses the completed research outputs and subagent drafts from `outputs/` and keeps paper-only, promised-only, and public-code evidence explicitly separated.

## Verification

Fresh checks run on 2026-05-19:

```text
OK structural survey package verified
main_lines=342 bib_entries=20

OK citations and placeholders verified
used_citations=17 defined_bib_entries=20 unused_bib_entries=3

research/slam-survey/build/main.pdf: PDF document, version 1.5 (zip deflate encoded)
-rw-r--r-- 1 prannayag prannayag 105K May 19 15:00 research/slam-survey/build/main.pdf

OK survey structure, citations, and PDF artifact verified
main_lines=343 bib_entries=20 used_citations=17
```

## Sources

Direct source URLs are included in the `Sources Appendix` section of `research/slam-survey/main.tex` and as BibTeX `url` fields in `research/slam-survey/references.bib`.
