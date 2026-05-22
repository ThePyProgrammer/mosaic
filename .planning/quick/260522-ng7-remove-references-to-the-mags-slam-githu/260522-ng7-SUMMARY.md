---
status: complete
task: 260522-ng7-remove-references-to-the-mags-slam-githu
plan: 260522-ng7-PLAN.md
completed: 2026-05-22
files_modified:
  - research/slam-survey/main.tex
  - research/slam-survey/references.bib
  - research/slam-survey/main.pdf
build:
  command: tectonic research/slam-survey/main.tex
  status: passed
  warnings:
    - "Tectonic reported repeated invalid UTF-8 byte replacement warnings from fmtcount/fcprefix/fcnumparser/fc-english package files."
    - "Tectonic reported font request warnings from XCharter.sty and googledeepmind.cls."
verification:
  removed_project_page_keys_and_urls: passed
  retained_paper_citation_keys: passed
---

# Quick Task 260522-ng7 Summary

Removed the HAMMER and MAGS-SLAM github.io project-page references from the SLAM survey while preserving the normal paper/arXiv citations.

## Changes Made

- Replaced `\citep{yu2025hammer,yu2025hammer_project}` with `\citep{yu2025hammer}` in the HAMMER system prose.
- Replaced `\citep{cao2026mags_slam,cao2026mags_slam_project}` with `\citep{cao2026mags_slam}` in the MAGS-SLAM system prose and appendix prose.
- Deleted the `yu2025hammer_project` BibTeX entry containing `http://hammer-project.github.io`.
- Deleted the `cao2026mags_slam_project` BibTeX entry containing `https://mags-slam.github.io/`.
- Regenerated `research/slam-survey/main.pdf`.

## Verification

- Passed: `grep -RInE 'yu2025hammer_project|cao2026mags_slam_project|hammer-project\.github\.io|mags-slam\.github\.io' research/slam-survey/main.tex research/slam-survey/references.bib || true` returned no matches.
- Passed: retained paper keys `yu2025hammer` and `cao2026mags_slam` remain in `main.tex` and `references.bib`.
- Passed: `tectonic research/slam-survey/main.tex` rebuilt the PDF.

## Build Notes

Tectonic completed successfully with the same style/package warnings seen in the preceding paper build: invalid UTF-8 replacement warnings from `fmtcount`-related package files and font request warnings from `XCharter.sty` / `googledeepmind.cls`.

## Deviations

None.
