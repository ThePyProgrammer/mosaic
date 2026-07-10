# Provenance: Coko-SLAM over MAGIC-SLAM

Date: 2026-05-22
Slug: `coko-slam-magic-slam`

## Sources consulted

### Local sources

- `research/slam-survey/main.tex` — accepted; primary local survey source for system taxonomy, algorithms, and MAGIC-SLAM/CoKo-SLAM comparison claims.
- `research/slam-survey/references.bib` — accepted; used to identify canonical paper URLs and repository links.
- `research/slam-survey/main.pdf` — noted as the local paper target; `main.tex` was used for exact local text because it is source-equivalent and easier to inspect.

### External sources accepted

- https://arxiv.org/abs/2604.00804 — accepted; CoKo-SLAM title, authors, abstract, communication-reduction claim, code link.
- https://arxiv.org/html/2604.00804 — accepted; CoKo-SLAM method details, contribution phrasing, limitations, and results summary.
- https://ar5iv.labs.arxiv.org/html/2604.00804 — accepted; secondary HTML rendering of CoKo-SLAM with method details and numeric communication ranges.
- https://github.com/lemonci/coko-slam — accepted; repository availability, implementation status, datasets, and statement that codebase is based on MAGIC-SLAM.
- https://raw.githubusercontent.com/lemonci/coko-slam/main/README.md — accepted; exact README phrases about MAGiC-SLAM ancestry, reproducibility, datasets, and nondeterminism caveat.
- https://openaccess.thecvf.com/content/CVPR2025/html/Yugay_MAGiC-SLAM_Multi-Agent_Gaussian_Globally_Consistent__SLAM_CVPR_2025_paper.html — accepted; CVPR metadata, abstract-level method claims.
- https://openaccess.thecvf.com/content/CVPR2025/papers/Yugay_MAGiC-SLAM_Multi-Agent_Gaussian_Globally_Consistent__SLAM_CVPR_2025_paper.pdf — accepted with caveat; PDF was fetched but text extraction was limited.
- https://arxiv.org/abs/2411.16785 — accepted; MAGIC-SLAM abstract and arXiv metadata.
- https://ar5iv.labs.arxiv.org/html/2411.16785 — accepted; MAGIC-SLAM method and quantitative extraction.
- https://github.com/VladimirYugay/MAGiC-SLAM — accepted; implementation availability, dataset/reproduction instructions, multi-agent setup notes.
- https://huggingface.co/datasets/voviktyl/ReplicaMultiagent — accepted with caveat; verifies dataset page exists, but no dataset card or explicit paper-specific protocol was visible.

### Sources rejected or not used materially

- Search-result snippets from ResearchGate, Semantic Scholar, Papers with Code, DagsHub, DeepDyve, LinkedIn, and papers.cool were not used as primary evidence because canonical arXiv/CVF/GitHub sources were available.

## Verification status

| Claim | Status | Evidence |
|---|---:|---|
| CoKo-SLAM builds on MAGIC-SLAM's codebase | verified | CoKo repository README and arXiv HTML extraction. |
| MAGIC-SLAM provides the centralized multi-agent Gaussian SLAM baseline | verified | CVPR page, MAGIC arXiv/ar5iv, local survey. |
| CoKo-SLAM reports up to 85--95% reduction in transmitted data | verified as author claim | CoKo arXiv abstract/HTML and WebSearch snippet. |
| CoKo-SLAM uses compact keyframe features, poses, and Gaussian submaps | verified | CoKo arXiv HTML/ar5iv extraction. |
| CoKo-SLAM includes redundant Gaussian pruning/compaction | verified as author claim | CoKo arXiv HTML/ar5iv extraction. |
| CoKo-SLAM supports loop closure/alignment without an initial relative pose guess | verified | CoKo arXiv HTML/ar5iv extraction. |
| MAGIC-SLAM reports 0.27 cm ATE, 34.26 dB PSNR, 1.12 GiB peak GPU, 54 MB submap storage, and 167 s merge time | verified from ar5iv extraction and local survey | CVF PDF fetch was limited, so numeric values rely on ar5iv extraction plus local survey. |
| ReplicaMultiagent is the dataset used in both workflows | partially verified | Hugging Face page exists; explicit benchmark protocol not visible on dataset card. |

## Intermediate research files used

- Plan: `outputs/.plans/coko-slam-magic-slam.md`
- Final review: `outputs/coko-slam-magic-slam.md`
- No separate `outputs/coko-slam-magic-slam-research-*.md` files were created because the topic was narrow and direct source verification was sufficient.

## Verification caveats

- The MAGIC-SLAM PDF fetch succeeded but automated text extraction did not expose readable tables; the review therefore cites MAGIC numeric details as verified from the ar5iv extraction and local survey, not from direct PDF table inspection.
- CoKo-SLAM is a 2026 arXiv source at the time of review. Claims should be treated as author-reported until independently reproduced.
- Repository availability was verified at the README level, but no code audit or reproduction run was performed.
