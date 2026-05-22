# Provenance: MAGiC-SLAM Photometric-Depth Tracking vs `local_tracking`

Date: 2026-05-22
Slug: `magic-local-tracking`
Final review: `outputs/magic-local-tracking.md`
Plan: `outputs/.plans/magic-local-tracking.md`

## Intermediate research files used

| File | Role | Status |
|---|---|---:|
| `outputs/magic-local-tracking-research-magic.md` | MAGiC-SLAM tracking evidence slice | accepted |
| `outputs/magic-local-tracking-research-mac-ego3d.md` | MAC-Ego3D local tracking evidence slice | accepted with caution on tracker-code scope |
| `outputs/magic-local-tracking-research-coko.md` | CoKo-SLAM local tracking evidence slice | accepted |
| `outputs/magic-local-tracking-research-mags.md` | MAGS-SLAM local tracking evidence slice | accepted with code-availability limitation |

## Sources consulted and accepted

| Source | Type | Verification status | Used for |
|---|---|---:|---|
| `research/slam-survey/main.tex` | local survey source | verified/read | Survey notation, `local_tracking_i`, caveat that algorithm boxes are survey-level procedures. |
| `research/slam-survey/references.bib` | local bibliography | verified/read | Canonical local citation metadata. |
| `research/slam-survey/diagrams/magic_slam.pdf` | local diagram | verified via `pdftotext` | MAGiC pipeline labels. |
| `research/slam-survey/diagrams/mac_ego3d_slam.pdf` | local diagram | verified via `pdftotext` | MAC-Ego3D consensus labels. |
| `research/slam-survey/diagrams/coko_slam.pdf` | local diagram | verified via `pdftotext` | CoKo tracking/keyframe/mapping/loop-closure labels. |
| `research/slam-survey/diagrams/mags_slam.pdf` | local diagram | verified via `pdftotext` | MAGS local tracking/mapping, Sim(3), and fusion labels. |
| `https://openaccess.thecvf.com/content/CVPR2025/html/Yugay_MAGiC-SLAM_Multi-Agent_Gaussian_Globally_Consistent__SLAM_CVPR_2025_paper.html` | primary paper page | verified by WebFetch | MAGiC title/authors/venue/abstract/PDF link. |
| `https://openaccess.thecvf.com/content/CVPR2025/papers/Yugay_MAGiC-SLAM_Multi-Agent_Gaussian_Globally_Consistent__SLAM_CVPR_2025_paper.pdf` | primary paper PDF | verified by WebFetch and saved PDF extraction | MAGiC Section 3.2 tracking details. |
| `https://github.com/VladimirYugay/MAGiC-SLAM` | primary repo | verified by WebFetch | Repository existence/code availability. |
| `https://arxiv.org/abs/2412.09723` | primary paper page | verified by WebFetch | MAC-Ego3D metadata and abstract claims. |
| `https://arxiv.org/html/2412.09723` | primary paper HTML | verified by WebFetch | MAC-Ego3D intra-agent consensus and local objective extraction. |
| `https://github.com/Xiaohao-Xu/MAC-Ego3D` | primary repo | verified by WebFetch | Repository existence and README-level claims. |
| `https://raw.githubusercontent.com/Xiaohao-Xu/MAC-Ego3D/main/mac_Tracker.py` | primary repo source | verified by WebFetch | Tracker method name and geometric alignment calls; absence of photometric render loss in checked file. |
| `https://raw.githubusercontent.com/Xiaohao-Xu/MAC-Ego3D/main/mac_Mapper.py` | primary repo source | verified by WebFetch | Mapping render/loss names and distinction from tracking. |
| `https://arxiv.org/abs/2604.00804` | primary paper page | verified by WebFetch | CoKo metadata, abstract claims, code URL. |
| `https://arxiv.org/html/2604.00804` | primary paper HTML | verified by WebFetch | CoKo inherited tracking statement, keyframe policy, compaction, loop closure. |
| `https://github.com/lemonci/coko-slam` | primary repo | verified by WebFetch | Repository existence, README entrypoint, absence of `local_tracking` in README. |
| `https://arxiv.org/abs/2605.10760` | primary paper page | verified by WebFetch | MAGS metadata, monocular/RGB-only abstract claims. |
| `https://arxiv.org/html/2605.10760` | primary paper HTML | verified by WebFetch | MAGS Section 3.1 local front-end, JDSA, local mapping, Sim(3) submaps; absence of literal `local_tracking`. |
| `https://mags-slam.github.io/` | project page | verified by WebFetch | MAGS RGB-only/local submap/compact summary claims and code/data release status. |

## Sources consulted but rejected or downgraded

| Source | Decision | Reason |
|---|---|---|
| Existing `outputs/` survey notes | downgraded to orientation only | Useful context but not primary evidence for final claims. |
| Local survey algorithm boxes | accepted only as notation | The survey itself says algorithm boxes are not executable source; final review treats `local_tracking_i` as taxonomy notation. |
| MAGS implementation-code claims | rejected/blocked | Project page says code/data released upon acceptance; no public implementation evidence was verified. |
| MAC-Ego3D project-page URL beyond GitHub/arXiv | rejected | Research note reported a guessed project page returned 404; no final claim depends on it. |

## Verification log

| Claim | Verification status | Notes |
|---|---:|---|
| `research/slam_survey` is absent and `research/slam-survey` is the local source directory | verified | Initial `ls` failed for underscore path; `find` found hyphenated directory. |
| `local_tracking_i` is local survey notation | verified | `main.tex` defines it and warns algorithms are survey-level procedures. |
| MAGiC-SLAM tracking freezes Gaussian parameters and optimizes pose with RGB/depth render loss | verified | CVPR PDF extraction and MAGiC research note agree. |
| MAGiC tracking has dense frame-to-frame initialization and frame-to-model refinement | verified | CVPR Section 3.2 extraction. |
| MAC-Ego3D uses Gaussian consensus/local maps/RGB-D | verified | arXiv abstract and HTML extraction. |
| MAC-Ego3D checked tracker source lacks literal `local_tracking` and uses alignment calls | verified | Raw `mac_Tracker.py` WebFetch. |
| MAC-Ego3D checked mapper source contains RGB/depth rendering losses | verified | Raw `mac_Mapper.py` WebFetch. |
| CoKo-SLAM says tracking is same as MAGiC-SLAM and does not report tracking error | verified | arXiv HTML extraction. |
| CoKo `local_tracking` is not a README-visible script/function | verified for README; broader absence limited | GitHub README WebFetch did not show the term; research note also inspected repo clone. |
| MAGS-SLAM is RGB-only/monocular and uses DROID/JDSA/local Gaussian mapping | verified | arXiv page, arXiv HTML, project page. |
| MAGS has no verified public implementation code | verified as of this run | Project page says code/data released upon acceptance. |

## Issue sweep

- FATAL issues found: none after downgrading `local_tracking` from paper/code term to survey notation.
- MAJOR issues noted in final review: MAC-Ego3D tracker objective ambiguity; MAGS code unavailable; CoKo code not executed.
- Unsupported strong claims removed or softened: any claim that MAC-Ego3D, CoKo, or MAGS literally define a function named `local_tracking`; any claim that MAGS uses active RGB-D depth; any claim that MAC-Ego3D tracker code uses photometric-depth pose loss.
