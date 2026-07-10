# Draft Outline: Multi-Robot Gaussian SLAM Survey

## Slug
`robot-gaussian-slam-survey`

## Requested output location
The user requested a LaTeX survey paper in `./research/slam-survey/` using templates from `~/harness_eng`.

Because the `/feynman:draft` skill normally saves exactly one Markdown draft to `papers/<slug>.md`, this run will adapt the requirement as follows after confirmation:
- Create the requested LaTeX paper package under `research/slam-survey/`.
- Use `~/harness_eng/latex-document-skill/assets/templates/academic-paper.tex` as the primary paper template scaffold because it is an arXiv-compatible academic paper template.
- Use `~/harness_eng/assets/latex/googledeepmind.cls` / `~/harness_eng/science/paper/science.tex` as style reference if the Google DeepMind class is practical to copy locally.
- Save a concise Markdown companion / source appendix at `papers/robot-gaussian-slam-survey.md` only if needed to satisfy the skill artifact convention; the authoritative requested deliverable will be the LaTeX paper in `research/slam-survey/`.

## Proposed title
**Collaborative Gaussian SLAM for Multi-Robot Mapping: A Survey of Online Shared-Map Systems**

## Proposed LaTeX files
- `research/slam-survey/main.tex` — survey paper using the academic-paper template structure.
- `research/slam-survey/references.bib` — BibTeX entries for primary papers, project pages, repositories, and datasets.
- `research/slam-survey/README.md` — brief build/readme note only if needed for local compilation instructions.

## Draft structure
1. **Title and abstract**
   - Define the corrected problem: multi-robot / multi-agent online Gaussian SLAM with shared-map fusion.
   - Summarize the open/public and paper-only landscape.
2. **Problem statement**
   - Distinguish this target from single-agent 3DGS SLAM, stereo, multi-camera rigs, static multi-view 3DGS, and offline reconstruction.
   - Formalize a target-class definition in prose and a compact notation: agents $a_i$, local observations $O_i^t$, local submaps $M_i^t$, shared map $M_G^t$, fusion operator $\mathcal{F}$.
3. **Background and related work**
   - Brief context on 3D Gaussian Splatting SLAM and collaborative SLAM.
   - Explain why Gaussian maps change the fusion problem: duplicate Gaussians, bandwidth, frame alignment, provenance, loop closure, and map consistency.
4. **Survey method / evidence criteria**
   - Explain source selection: completed research reports, paper/project pages, repositories, benchmark tables.
   - Define evidence tiers: public implementation, public but license-risk, promised/paper-only, low-confidence lead.
5. **Candidate systems**
   - Detailed subsections for:
     1. MAGiC-SLAM
     2. MAC-Ego3D
     3. CoKo-SLAM
     4. CoMA-SLAM
     5. HAMMER
     6. GRAND-SLAM
     7. MAGS-SLAM
   - Each subsection covers modality, map representation, fusion architecture, source availability, benchmarks, strengths, and caveats.
6. **Architecture taxonomy**
   - Central server shared-map pattern: MAGiC-SLAM, CoKo-SLAM, HAMMER.
   - Distributed Gaussian consensus pattern: MAC-Ego3D, CoMA-SLAM.
   - Submap + pose-graph global consistency pattern: GRAND-SLAM.
   - Monocular compact-submap fusion pattern: MAGS-SLAM.
   - Include a TikZ diagram adapted from the prior Mermaid taxonomy.
7. **Evidence table and benchmark synthesis**
   - Table comparing modality, source status, map representation, fusion timing/location, benchmarks, runtime/memory/communication evidence.
   - Include only numbers already supported by the completed research: e.g. MAGiC-SLAM ATE/memory/merge time; MAC-Ego3D ATE/PSNR/timing; HAMMER bandwidth/update time; GRAND-SLAM Multiagent Replica/Kimera-Multi metrics; CoKo/CoMA communication-reduction claims as claims, not independently verified reproduction.
8. **Implications for Mosaic**
   - Multi-agent observation contracts.
   - Separation of local mapping and fusion.
   - Shared Gaussian map snapshots.
   - Provenance, alignment constraints, communication metrics, and backend isolation.
9. **Limitations**
   - Rapid 2025-2026 literature changes.
   - Code availability and licensing gaps.
   - Inconsistent online/runtime definitions.
   - Benchmarks not directly comparable.
   - Some source claims remain paper/project-page only.
10. **Conclusion**
    - Recommended shortlist and practical next steps for Mosaic backend planning.
11. **References / Sources appendix**
    - BibTeX references and direct source URLs.

## Key claims to make
1. **Open implementation claim:** MAGiC-SLAM, MAC-Ego3D, CoKo-SLAM, and CoMA-SLAM have public implementation evidence, but they differ substantially in maturity and license risk.
2. **Paper-only claim:** HAMMER, GRAND-SLAM, and MAGS-SLAM are highly relevant but not currently cleanly auditable as public implementation backends.
3. **Modality claim:** Most auditable systems are RGB-D; MAGS-SLAM is the key RGB-only monocular claim; HAMMER is the strongest heterogeneous robot/device lead.
4. **Fusion claim:** The main architecture families are central server fusion, distributed Gaussian consensus, submap/pose-graph global consistency, and compact monocular submap fusion.
5. **Benchmark claim:** Accuracy/rendering evidence is more common than communication/memory evidence; HAMMER and MAGiC-SLAM provide some of the cleanest non-accuracy operational numbers.
6. **Mosaic claim:** These systems should guide typed contracts and evaluation metrics, but not be imported into Mosaic core because of CUDA/native/research-code dependency risk.

## Source material to draw from
- `outputs/multi-robot-gaussian-slam.md` — final synthesized report.
- `outputs/multi-robot-gaussian-slam.provenance.md` — provenance and verification notes.
- `outputs/multi-robot-gaussian-slam-research-papers.md` — paper/project landscape.
- `outputs/multi-robot-gaussian-slam-research-code.md` — source code/license inventory.
- `outputs/multi-robot-gaussian-slam-research-fusion.md` — architecture/modality classification.
- `outputs/multi-robot-gaussian-slam-research-benchmarks.md` — benchmark/runtime/communication evidence.
- `outputs/multi-robot-gaussian-slam-research-followup-code.md` — targeted code/license corrections.
- `outputs/multi-robot-gaussian-slam-research-followup-architecture.md` — targeted architecture corrections.
- LaTeX templates:
  - `/home/prannayag/harness_eng/latex-document-skill/assets/templates/academic-paper.tex`
  - `/home/prannayag/harness_eng/latex-document-skill/assets/templates/references.bib`
  - `/home/prannayag/harness_eng/science/paper/science.tex`
  - `/home/prannayag/harness_eng/assets/latex/googledeepmind.cls`

## Verification log
| Item | Verification method | Status | Evidence |
|---|---|---|---|
| Template selection | Inspect `~/harness_eng` LaTeX templates and pick a compatible academic paper scaffold | pending | `academic-paper.tex`, `science.tex`, `googledeepmind.cls` |
| Candidate inclusion | Cross-check final report and follow-up reports for the seven requested systems | pending | `outputs/multi-robot-gaussian-slam.md` plus follow-ups |
| Public/open implementation claims | Verify repository/source status from final research and WebFetch where needed | pending | GitHub/project URLs |
| Paper-only/promised claims | Verify HAMMER/GRAND/MAGS code availability caveats against final research | pending | arXiv/project pages and follow-up reports |
| Benchmark numbers | Use only already extracted supported values; no new unsupported numerics | pending | benchmark report and final report table |
| Citations | Add BibTeX entries and cite every system subsection | pending | `research/slam-survey/references.bib` |
| Build/readability | Compile LaTeX if dependencies allow, otherwise run a structural check for required files/sections/citations | pending | build output or structural verification |
| Claim sweep | Downgrade overstrong claims and mark paper-only / project-page-only systems | pending | final `main.tex` sweep |

## No-new-research assumption
The completed deep research and follow-up reports are sufficient for the requested seven-system survey. New WebFetch checks may be used only for citation/source verification or if BibTeX metadata is missing.
