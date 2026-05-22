# Literature Review Plan: MAGiC vs Local Tracking

Slug: `magic-local-tracking`

## Scope

Explain the difference between MAGiC-SLAM's photometric-depth tracking objective and the `local_tracking` used or referenced in MAC-Ego3D, CoKo-SLAM, and MAGS-SLAM. The review will prioritize method mechanics over broad SLAM background.

## Key Questions

1. What exactly is optimized in MAGiC-SLAM tracking: variables, photometric term, depth term, rendering source, and update schedule?
2. What does `local_tracking` mean in MAC-Ego3D, CoKo-SLAM, and MAGS-SLAM: local map/window construction, objective, pose parameterization, and how it differs from global mapping?
3. Are these methods solving the same tracking subproblem with different names, or do they differ in supervision signal, map scope, and coupling to Gaussian updates?
4. Which claims are directly stated in the papers/code, and which are inferred from diagrams, algorithms, or implementation naming?

## Source Types to Search

- Local files under `research/slam-survey/`, especially PDFs, diagrams, notes, and any downloaded papers for MAGiC-SLAM, MAC-Ego3D, CoKo-SLAM, and MAGS-SLAM.
- Existing project outputs under `outputs/` and `papers/` only as orientation, not as primary evidence.
- Primary papers on arXiv, project pages, and publisher pages.
- Official or author-linked repositories when `local_tracking` appears to be an implementation term.
- Semantic Scholar or broader web search for metadata and paper identity checks if local filenames are ambiguous.

## Time Period

Focus on 2024-2026 3D Gaussian Splatting SLAM / embodied Gaussian mapping papers, because all named systems are recent Gaussian-SLAM variants.

## Expected Final Sections

1. Short answer.
2. Terminology alignment: tracking, local tracking, photometric-depth tracking.
3. MAGiC-SLAM tracking objective.
4. MAC-Ego3D / CoKo-SLAM / MAGS-SLAM local_tracking comparison.
5. Main differences: supervision signal, map scope, optimization target, coupling to mapping, and implementation naming.
6. Consensus, disagreements, and open questions.
7. Minimal method pipeline diagram.
8. Citations and provenance notes.

## Task Ledger

| Task | Status | Notes |
|---|---|---|
| Locate local source files | pending | Use `research/slam-survey/` because `research/slam_survey` is absent in this checkout. |
| Identify canonical papers and URLs | pending | Prefer primary paper/project/repo sources. |
| Extract MAGiC-SLAM tracking details | pending | Record exact objective terms and citations. |
| Extract local_tracking details for MAC-Ego3D | pending | Determine whether term is from paper, code, or both. |
| Extract local_tracking details for CoKo-SLAM | pending | Determine local map/window and pose objective. |
| Extract local_tracking details for MAGS-SLAM | pending | Determine local map/window and pose objective. |
| Synthesize comparison | pending | Separate direct evidence from inference. |
| Verify citations and strong claims | pending | WebFetch every accepted URL and note failures. |
| Write final review | pending | Save to `outputs/magic-local-tracking.md`. |
| Write provenance | pending | Save to `outputs/magic-local-tracking.provenance.md`. |

## Verification Log

| Claim / Source | Verification Method | Status | Notes |
|---|---|---|---|
| Local source directory is `research/slam-survey/` | `find` / `ls` in repository | verified | `research/slam_survey` was absent; hyphenated directory exists. |
| MAGiC-SLAM paper details | local paper + primary URL | pending | Need exact citation and tracking formulation. |
| MAC-Ego3D `local_tracking` details | local paper/code + primary URL | pending | Need distinguish paper term vs repository function. |
| CoKo-SLAM `local_tracking` details | local paper/code + primary URL | pending | Need exact local tracking definition. |
| MAGS-SLAM `local_tracking` details | local paper/code + primary URL | pending | Need exact local tracking definition. |
| Final comparison table | trace each row to accepted source | pending | Downgrade inferred rows. |

## Delegation Plan

This is narrow enough to search directly first. If local files reveal multiple ambiguous paper/code variants or missing source material, use parallel researcher agents split by system: MAGiC-SLAM, MAC-Ego3D, CoKo-SLAM, and MAGS-SLAM.

## Delivery Artifacts

- Plan: `outputs/.plans/magic-local-tracking.md`
- Intermediate research notes if needed: `outputs/magic-local-tracking-research-*.md`
- Final review: `outputs/magic-local-tracking.md`
- Provenance: `outputs/magic-local-tracking.provenance.md`
