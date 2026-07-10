# Literature Review Plan: Gaussian SLAM Method Ancestry

Slug: `gaussian-slam-method-ancestry`
Date: 2026-05-25

## Scope

Investigate whether newer multi-robot Gaussian SLAM systems, especially GRAND-SLAM and MAGS-SLAM, explicitly inherit, reuse, fork, adapt, or cite components from MAGiC-SLAM, MAC-Ego3D, CoKo-SLAM, CoMA-SLAM, or adjacent Gaussian SLAM systems. Distinguish hard ancestry claims from softer pattern similarity.

## Key Questions

1. Which papers explicitly cite MAGiC-SLAM, MAC-Ego3D, CoKo-SLAM, CoMA-SLAM, Gaussian-SLAM, SplaTAM, MonoGS, DROID-SLAM, or other key predecessors?
2. Do GRAND-SLAM or MAGS-SLAM state that they build on, adapt, inherit, or reuse any predecessor codebase or method component?
3. Are there public repositories for GRAND-SLAM or MAGS-SLAM, and do they reveal copied/forked dependencies, acknowledgments, or base-code claims?
4. Which components are true ancestry versus common design patterns?
   - Gaussian submaps
   - local RGB-D or monocular tracking
   - DROID-style monocular front end
   - loop closure / pose graph optimization
   - FPFH/RANSAC/ICP alignment
   - compact update selection
   - Gaussian fusion or redundancy pruning
5. Where do authors claim novelty relative to prior systems?
6. What should the local survey say to avoid overclaiming that a method "stole" or inherited a component when evidence only supports convergent design?

## Source Types to Search

Primary local sources:
- `research/slam-survey/main.tex`
- `research/slam-survey/references.bib`
- Existing outputs on multi-robot Gaussian SLAM, especially prior review files under `outputs/`.

External sources:
- GRAND-SLAM paper: IEEE/RA-L, arXiv, project pages, repos if any.
- MAGS-SLAM paper/project page/arXiv and any release notes.
- MAGiC-SLAM paper/repo.
- MAC-Ego3D paper/repo.
- CoKo-SLAM paper/repo.
- CoMA-SLAM paper/repo.
- Citation indexes or pages: Semantic Scholar, Google Scholar snippets where accessible, Papers with Code, GitHub, arXiv references.

## Time Period

Use sources available through 2026-05-25. Treat 2026 papers and unreleased repos as provisional unless code and artifacts are public.

## Evidence Categories

- **Direct implementation ancestry:** paper or repo says "based on", "forked from", "adapted from", includes code provenance, or reuses modules.
- **Direct method borrowing:** paper says it uses/adapts a named predecessor's tracker, mapper, loop closure, fusion, or benchmark setup.
- **Citation-only relationship:** paper cites prior work but does not claim reuse.
- **Shared pattern / convergent architecture:** similar submaps, pose graphs, Gaussian fusion, or tracking front ends without explicit ancestry.
- **Unsupported inference:** similarity only; must not be phrased as borrowing.

## Expected Review Sections

1. Short answer to the user's question.
2. Evidence matrix by method: GRAND-SLAM, MAGS-SLAM, CoKo-SLAM, CoMA-SLAM, HAMMER if relevant.
3. Citation/ancestry graph showing direct ancestry, citation-only, and pattern similarity.
4. Component-level comparison: what is borrowed, what is common, what is novel.
5. Recommended wording for the survey paper.
6. Open questions and follow-up verification steps.

## Task Ledger

| Task | Status | Notes |
|---|---:|---|
| Read local survey references for all target methods | pending | Extract BibTeX and any local ancestry wording. |
| Verify GRAND-SLAM paper and citation/reference list | pending | Look for MAGiC-SLAM/MAC-Ego3D/other named ancestry. |
| Verify MAGS-SLAM paper/project page and citation/reference list | pending | Look for DROID/MAGiC/MAC/MonoGS/SplaTAM inheritance. |
| Verify CoKo-SLAM and CoMA-SLAM ancestry evidence | pending | CoKo likely direct MAGIC codebase; CoMA needs checking. |
| Search repositories/project pages for implementation ancestry | pending | Record public/unavailable status. |
| Build evidence matrix and graph | pending | Separate direct ancestry vs citation-only vs pattern similarity. |
| Sweep strong claims against verification log | pending | Downgrade unsupported or single-source claims. |
| Write final review | pending | Save to `outputs/gaussian-slam-method-ancestry.md`. |
| Write provenance record | pending | Save to `outputs/gaussian-slam-method-ancestry.provenance.md`. |

## Verification Log

| Claim / Source | Status | Verification Action |
|---|---:|---|
| CoKo-SLAM directly builds on MAGiC-SLAM's codebase | pending | Re-verify paper/repo wording. |
| GRAND-SLAM explicitly borrows from MAGiC-SLAM or MAC-Ego3D | pending | Check paper text, references, code/project availability. |
| MAGS-SLAM explicitly borrows from MAGiC-SLAM or MAC-Ego3D | pending | Check paper text, references, project page, code status. |
| MAGS-SLAM uses DROID-style monocular front end | pending | Verify whether this is a named adaptation or survey-level inference. |
| GRAND-SLAM uses submap-plus-pose-graph consistency as a shared pattern | pending | Verify paper method wording and citations. |
| MAC-Ego3D is consensus-oriented rather than a direct ancestor for these papers | pending | Check citation relationships. |
| CoMA-SLAM has direct or citation-only links to MAGIC/MAC | pending | Verify paper and repository. |

## Deliverables

- Final review: `outputs/gaussian-slam-method-ancestry.md`
- Provenance: `outputs/gaussian-slam-method-ancestry.provenance.md`
- Intermediate research files if needed: `outputs/gaussian-slam-method-ancestry-research-*.md`

## Confirmation Gate

Stop after this plan and proceed only after user confirmation.
