# Literature Review Plan: Coko-SLAM over MAGIC-SLAM

Slug: `coko-slam-magic-slam`
Date: 2026-05-22

## Scope

Answer the focused question: what does CoKo-SLAM bring to the table over MAGIC-SLAM, using the local survey paper in `research/slam-survey` as the primary source and external papers/repos only to verify or sharpen the comparison.

## Key Questions

1. What baseline architecture does MAGIC-SLAM establish for multi-agent RGB-D Gaussian SLAM?
2. Which parts of CoKo-SLAM are inherited from MAGIC-SLAM, especially local RGB-D tracking and local Gaussian mapping?
3. What are CoKo-SLAM's distinct contributions over MAGIC-SLAM?
4. Are the claimed improvements primarily algorithmic, systems-level, or communication-efficiency improvements?
5. What evidence supports the comparison: transmitted data reduction, alignment/loop-closure behavior, redundancy pruning, map quality, runtime, memory, and reproducibility?
6. What caveats remain, especially around absolute bandwidth, independent reproduction, and apples-to-apples metrics?

## Source Types to Search

Primary local sources:
- `research/slam-survey/main.pdf`
- `research/slam-survey/main.tex`
- `research/slam-survey/references.bib`

External verification sources:
- CoKo-SLAM paper/preprint page and PDF.
- MAGIC-SLAM paper/preprint page and PDF.
- Public repositories for CoKo-SLAM and MAGIC-SLAM.
- Project pages, arXiv/OpenReview/Semantic Scholar records, and repository READMEs when they provide implementation or result details.

## Time Period

Use sources current through 2026-05-22. Treat 2026 entries as fresh/preprint-stage unless verified by venue, code, or reproducible artifacts.

## Expected Review Sections

1. Short answer: one-paragraph summary of CoKo-SLAM's incremental value over MAGIC-SLAM.
2. Baseline: MAGIC-SLAM's server-mediated Gaussian-submap plus loop-constraint global fusion pipeline.
3. CoKo-SLAM additions: compact keyframe-optimized communication, no-initial-relative-pose loop closure/alignment, redundant-Gaussian pruning, and global optimization/fusion changes.
4. Evidence table: claimed improvements, supporting source, verification status, and caveat.
5. Practical implications for Mosaic: which ideas are worth borrowing as typed contracts or future benchmarks.
6. Open questions and follow-up reading.

## Task Ledger

| Task | Status | Notes |
|---|---:|---|
| Read local survey sections for MAGIC-SLAM and CoKo-SLAM | pending | Use `main.tex` and `main.pdf`; capture exact claims and citations. |
| Extract BibTeX records for both papers | pending | Identify source URLs, titles, authors, years, and repo links. |
| Verify MAGIC-SLAM external paper/repo sources | pending | Confirm baseline mechanics and reported metrics. |
| Verify CoKo-SLAM external paper/repo sources | pending | Confirm claimed contributions and communication reduction. |
| Synthesize differential contribution | pending | Separate inherited pieces from novel pieces. |
| Check strong claims against verification log | pending | Downgrade unsupported or single-source claims. |
| Write final review | pending | Save to `outputs/coko-slam-magic-slam.md`. |
| Write provenance record | pending | Save to `outputs/coko-slam-magic-slam.provenance.md`. |

## Verification Log

| Claim / Source | Status | Verification Action |
|---|---:|---|
| Local survey says CoKo-SLAM inherits MAGIC-SLAM-style RGB-D tracking | pending | Cross-check `main.tex` appendix and CoKo paper. |
| Local survey says CoKo-SLAM transmits compact keyframe/Gaussian state instead of dense/raw streams | pending | Verify against CoKo paper/repo. |
| Local survey says CoKo-SLAM reports 85--95% lower transmitted data | pending | Verify exact wording and whether absolute bandwidth is reported. |
| Local survey says MAGIC-SLAM reports ~0.27 cm ATE, 34.26 dB PSNR, 1.12 GiB peak GPU, 54 MB submaps, 167 s merge | pending | Verify against MAGIC-SLAM paper/repo. |
| CoKo-SLAM supports loop closure/alignment without initial relative pose guess | pending | Verify source wording; flag if inferred. |
| CoKo-SLAM includes redundant-Gaussian pruning before global fusion | pending | Verify algorithm/detail source. |

## Deliverables

- Final review: `outputs/coko-slam-magic-slam.md`
- Provenance: `outputs/coko-slam-magic-slam.provenance.md`
- Intermediate notes, if needed: `outputs/coko-slam-magic-slam-research-*.md`

## Confirmation Gate

Stop after this plan and proceed only after user confirmation.
