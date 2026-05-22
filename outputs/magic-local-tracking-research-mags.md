# MAGS-SLAM local-tracking evidence slice

## Done / blocked ledger

| Item | Status | Evidence state |
|---|---:|---|
| Canonical paper identity | Done | arXiv entry and local BibTeX agree on title, authors, year, and arXiv ID. |
| Determine whether `local_tracking` is a MAGS-SLAM paper/code term | Done | `local_tracking` is not literal paper terminology in the accessible arXiv HTML; it appears in the local survey notation and local MAGS diagram as an abstraction/label. No public implementation code was found locally or in prior repository notes. |
| Extract tracking/local-map/window objective terms | Done | Direct arXiv HTML extraction gives Section 3.1 terms and equations for DROID-based front-end, sliding co-visibility window, BA, JDSA, local map loss, submap freezing, and Sim(3) correction. |
| Extract variables optimized | Done | Direct paper extraction identifies poses `{T}`, depth maps `{d}`, scale coefficients `{s}`, and local Gaussian-map parameters optimized by gradient descent against keyframes. |
| Extract rendering/map source | Done | Direct paper extraction identifies inverse-depth back-projection for seeding Gaussians and rendering losses over predicted image/depth from the local Gaussian map. |
| Extract coupling to mapping/global fusion | Done | Direct paper extraction identifies submap freezing, per-submap Sim(3) correction, PGBA, compact summaries, occupancy-aware fusion, and final global photometric refinement. |
| Verify public implementation details | Blocked | Project page says code/data released upon acceptance; local notes identify only website source, not implementation code. |
| Compare against MAGiC-SLAM in detail | Out of scope | This slice is MAGS-SLAM only. The comparison-ready conclusion is limited to the MAGS side of the distinction. |

## 1. Canonical title / authors / venue or arXiv identifier

Canonical identity:

- **Title:** *MAGS-SLAM: Monocular Multi-Agent Gaussian Splatting SLAM for Geometrically and Photometrically Consistent Reconstruction*
- **Authors:** Zhihao Cao, Qi Shao, Shuhao Zhai, Jing Zhang, Anh Nguyen, Baoru Huang
- **Identifier / status:** arXiv:2605.10760, 2026, primary class `cs.CV` in local BibTeX.
- **Project page:** https://mags-slam.github.io/
- **Implementation status:** code/data not publicly released in the evidence used here. The project page states “Code & Data (Released upon Acceptance)”; local repository notes identify only the website repository, not implementation code.

Local source: `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey/references.bib` lines 89-105.

## 2. Is `local_tracking` a paper concept, code function, script, or inferred stage?

**Finding:** For MAGS-SLAM, `local_tracking` is best treated as an **inferred/survey-stage abstraction**, not a confirmed paper token or code function.

Evidence:

- WebFetch over `https://arxiv.org/html/2605.10760` reported that the literal token **`local_tracking` does not appear** in the accessible MAGS-SLAM paper text.
- The exact phrase **“Local Tracking” also does not appear** in the accessible arXiv HTML text, although the paper does discuss tracking accuracy and local monocular SLAM.
- The local survey paper introduces `local_tracking_i` as a cross-system notation, not as a MAGS-SLAM-specific API: `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey/main.tex` lines 84-90 define a local tracking operator for the survey taxonomy.
- The local survey’s MAGS algorithm uses `local_tracking_i(...)` at `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey/main.tex` lines 316-325, but this is the survey author’s normalized algorithmic abstraction.
- The local diagram `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey/diagrams/mags_slam.pdf` contains diagram text “LOCAL TRACKING & GAUSSIAN MAPPING” and “Local Tracking,” but this appears to be the local survey diagram, not primary implementation code.
- No public MAGS-SLAM implementation repository was available to verify a function or script named `local_tracking`.

Conclusion: write `local_tracking` in lowercase/code font only as the literature-review notation for MAGS-SLAM’s local per-agent monocular SLAM stage. The primary-paper terminology to cite is **“Local Per-Agent Monocular Gaussian SLAM”**, **“DROID-based front-end”**, **“sliding co-visibility window”**, **“Joint Depth-Scale Adjustment (JDSA)”**, and **local Gaussian map optimization**.

## 3. Exact tracking / local-map / window objective terms

### 3.1 Local tracking/front-end stage

Direct paper extraction from arXiv HTML Section 3.1 gives these exact terms:

- “Each agent runs an independent monocular DROID-based front-end”
- “DROID-based front-end that couples recurrent dense bundle adjustment with a learned monocular depth prior”
- “Over a sliding co-visibility window, poses `{T}` and depth maps `{d}` are refined”

The tracking/front-end bundle-adjustment objective was extracted as:

```tex
\mathcal{L}_{BA}=\sum_{(i,j)\in\mathcal{E}}\|\mathbf{u}_{ij}^{*}-\pi(\mathbf{T}_{ij}\pi^{-1}(\mathbf{u}_i,\mathbf{d}_i))\|_{\mathbf{\Sigma}_{ij}}^2
```

Interpretation with evidence grading:

- **Direct evidence:** local tracking refines camera poses and depth maps in a sliding co-visibility window using a DROID-like dense BA formulation.
- **Inference:** calling this whole stage `local_tracking_i` is survey notation; the paper does not expose a code function by that name.

### 3.2 Monocular scale/depth coupling: JDSA

Direct extraction gives:

- “scale coefficients `{s}` and depth maps `{d}` are jointly minimizing via Joint Depth-Scale Adjustment (JDSA)”
- “where `d_k^prior` is a learned depth prior from Metric3D”

The extracted JDSA objective was:

```tex
\mathcal{L}_{JDSA}=\mathcal{L}_{BA}+\sum_{k\in\mathcal{V}}\|\mathcal{B}_k\mathbf{d}_k-\mathbf{d}_k^{prior}\|^2
```

Variables optimized / constrained:

- `{T}`: camera poses / relative transforms in the DROID-style front-end.
- `{d}`: depth maps or inverse-depth maps refined in the local window.
- `{s}`: scale coefficients, coupled with depth through JDSA.
- `d_k^prior`: learned depth prior from Metric3D, used as a scale/depth regularizing source rather than as active depth input.

### 3.3 Local Gaussian mapping objective

Direct extraction gives:

- “When a new keyframe is registered, its inverse-depth map is back-projected to seed new Gaussians.”
- “The local Gaussian map is then optimized against a sliding window of keyframes by gradient descent on”

The extracted local map objective was:

```tex
\mathcal{L}_{map}=\alpha\mathcal{L}_1(\hat{I},I)+\beta\mathcal{L}_1(\hat{D},D)+\lambda_n\mathcal{L}_{normal}+\lambda_s\mathcal{L}_{iso}
```

Rendering/map source:

- New Gaussians are seeded from back-projected inverse-depth maps when keyframes are registered.
- The local Gaussian map is rendered to produce `\hat{I}` and `\hat{D}` for photometric/depth-style supervision against `I` and `D`.
- Since MAGS-SLAM is RGB-only/monocular, `D` in this local objective should be read as coming from the monocular front-end/depth-prior pipeline, not from an RGB-D sensor, unless the paper states otherwise in a specific evaluation condition.

### 3.4 Local submap/window boundary

Direct extraction gives:

- “A submap is frozen once it reaches `Kmax` keyframes or the camera centers exceed a Euclidean distance of `τmove`”
- “freezing detaches it from local bundle adjustment and assigns it a per-submap Sim(3) correction `C_ℓ^a ∈ Sim(3)`”

This is the cleanest boundary between local tracking/mapping and collaborative alignment:

1. Active local window: DROID/front-end BA, JDSA, local Gaussian map optimization.
2. Frozen submap: detached from local BA, assigned a per-submap Sim(3) correction.
3. Collaborative layer: compact summaries, loop verification, submap graph optimization, occupancy-aware fusion.

## 4. Coupling to mapping, loop verification, and global fusion

### 4.1 Compact submap summaries and verification

Project/arXiv-level direct claims:

- “Each agent independently builds local monocular Gaussian submaps”
- “transmits compact submap summaries rather than raw observations or dense maps”
- “geometry- and appearance-aware loop verification”
- “occupancy-aware Gaussian fusion”
- “coherent global reconstruction without active depth sensors”

Local diagram text from `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey/diagrams/mags_slam.pdf` supports the same stage decomposition with labels including:

- “RGB STREAM”
- “LOCAL TRACKING & GAUSSIAN MAPPING”
- “GLOBAL INTRA-TO-INTER LOOP CLOSURE”
- “Local Submap Summary”
- “GAUSSIAN FUSION & GLOBAL REFINEMENT”
- “Occupancy-Grid Fusion”
- “Global Photometric Refinement”
- “Local Update δT, δD, δs”
- “Sim(3)-based PGBA”

Evidence grading: the diagram is local survey evidence, useful for interpretation, but the arXiv text/equations are stronger primary evidence.

### 4.2 Submap graph / PGBA objectives

Direct extraction from arXiv HTML Sections 3.2.4 and 3.2.5 gives geometric and photometric residuals:

```tex
r_e^{geo} = \log(M_e^{-1}\circ C_{tgt}^{-1}\circ C_{src}) \in \mathbb{R}^7
```

```tex
r_e^{pho}(u)=I^{src}(u)-I^{tgt}(\pi^{tgt}(C_{tgt}^{-1}\circ C_{src}\cdot p^{src}(u)))
```

The graph objective begins:

```tex
\mathcal{L}^{graph}(\{C_\ell^a\})=\sum_{e\in\mathcal{E}^{sm}}w_e\|r_e^{geo}\|_\rho^2+\sum_{e\in\mathcal{E}^{v}}
```

Direct extraction also states:

- “The graph is solved by damped Gauss-Newton within a Levenberg-Marquardt trust region.”
- “we fit `Δ_{a,ℓ}` by Umeyama on its pre/post-PGBA keyframe camera centers”
- “if it exceeds `τrig`, all incident edges `e∈E_v` are invalidated and queued for re-verification”

Variables/corrections in this layer:

- Per-submap Sim(3) corrections `C_ℓ^a`.
- Relative Sim(3) edge measurements `M_e`.
- Reactive correction `Δ_{a,ℓ}` after PGBA.

### 4.3 Occupancy-aware fusion and global refinement

Direct extraction from arXiv HTML Section 3.3 gives:

- “After pose-graph convergence, each submap carries a Sim(3) correction”
- “A borrowed Gaussian is retained only if” it passes occupancy checks.
- “The occupied test suppresses duplicate Gaussians.”
- “After deduplication, small residual Sim(3) errors and exposure differences are resolved”
- “joint photometric refinement of the fused Gaussian set”

The extracted global refinement objective was:

```tex
\mathcal{L}_{refine}=\alpha'\mathcal{L}_1(\tilde{I},I)+\lambda(1-SSIM(\tilde{I},I))+\beta\mathcal{L}_1(\hat{D},\bar{D})+\lambda_n'\mathcal{L}_{normal}
```

An extracted occupancy condition was:

```tex
\kappa(\mu_j)\notin O_{occ}\ \text{and}\ \kappa(\mu_j)\notin O_{free}
```

Interpretation:

- Local tracking/mapping does not directly optimize one global Gaussian map online from all raw frames.
- It produces bounded local monocular Gaussian submaps and compact summaries.
- Cross-agent consistency is then handled by Sim(3) submap graph optimization and occupancy-aware fusion.
- Final fused-map cleanup uses joint photometric refinement.

## 5. Comparison-ready distinction from MAGiC-SLAM photometric-depth tracking

Within this MAGS-only evidence slice, the key distinction to use against MAGiC-SLAM is:

- **MAGS-SLAM local stage:** monocular RGB-only per-agent front-end; DROID-style dense BA plus learned Metric3D depth prior; JDSA jointly handles scale coefficients and depth maps; local Gaussians are seeded from inverse-depth back-projection and optimized with image/depth/normal/isotropy terms; submaps carry Sim(3) corrections to handle monocular scale ambiguity.
- **Not established for MAGS-SLAM:** a public code function/script named `local_tracking`; code-level photometric-depth tracker implementation; runtime behavior.
- **Therefore:** if the review says “MAGS local_tracking,” it should define that as a normalized stage label for MAGS-SLAM’s local per-agent monocular Gaussian SLAM, not as a primary-paper API. Its tracking differs from a photometric-depth RGB-D tracker by relying on monocular depth priors and scale adjustment rather than active sensor depth.

## 6. Direct evidence vs inference

| Claim | Evidence grade | Basis |
|---|---:|---|
| MAGS-SLAM title/authors/arXiv ID | Direct | Local BibTeX and arXiv page. |
| MAGS-SLAM is RGB-only / monocular multi-agent 3DGS SLAM | Direct | Project/arXiv text: “RGB-only,” “monocular,” “multi-agent,” “local monocular Gaussian submaps.” |
| `local_tracking` is a MAGS paper term | Negative direct evidence | WebFetch over arXiv HTML found no literal `local_tracking`; local survey uses it as notation. |
| MAGS local tracking uses DROID-based front-end | Direct | ArXiv Section 3.1 extraction: “independent monocular DROID-based front-end.” |
| Local window optimizes poses and depth maps | Direct | ArXiv Section 3.1 extraction: sliding co-visibility window refines `{T}` and `{d}`. |
| JDSA jointly optimizes scale coefficients and depth maps | Direct | ArXiv Section 3.1 extraction and `L_JDSA` formula. |
| Local Gaussian map is optimized against keyframes using `L_map` | Direct | ArXiv Section 3.1 extraction and `L_map` formula. |
| Active submaps are frozen by keyframe count or camera-center displacement | Direct | ArXiv Section 3.1 extraction mentions `Kmax` and `τmove`. |
| Submap graph uses Sim(3), geometric residuals, and anchor-image photometric residuals | Direct | ArXiv Sections 3.2.4-3.2.5 extraction. |
| Occupancy-aware fusion deduplicates borrowed Gaussians | Direct | ArXiv Section 3.3 extraction and project-page claim. |
| MAGS has public code implementing this tracker | Blocked / unsupported | Project page says code/data released upon acceptance; prior local notes found website only. |
| MAGS differs from MAGiC by monocular depth/scale handling rather than RGB-D depth tracking | Inference from MAGS evidence plus topic framing | MAGS direct evidence supports monocular/JDSA/scale; this slice did not re-audit MAGiC internals. |

## 7. URL / local-file verification table

| Source | Type | Checked for | Result |
|---|---|---|---|
| `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey/references.bib` | Local BibTeX | Canonical MAGS metadata | Lines 89-96 list title, authors, year 2026, arXiv `2605.10760`, class `cs.CV`, URL. Lines 99-105 list project page and release-upon-acceptance note. |
| `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey/main.tex` | Local survey source | Whether `local_tracking` is local notation | Lines 84-90 define survey-level `local_tracking_i`; lines 316-325 use it in the normalized MAGS algorithm. |
| `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey/diagrams/mags_slam.pdf` | Local diagram PDF | MAGS stage labels | `pdftotext` extracts “LOCAL TRACKING & GAUSSIAN MAPPING,” “Local Update δT, δD, δs,” “Sim(3)-based PGBA,” “Occupancy-Grid Fusion,” and “Global Photometric Refinement.” |
| `https://arxiv.org/abs/2605.10760` | Primary arXiv page | Canonical metadata and abstract-level claims | Confirms title/authors/arXiv ID; abstract-level terms include local monocular Gaussian submaps, compact summaries, geometry/appearance loop verification, occupancy-aware Gaussian fusion, and tracking/rendering claims. |
| `https://arxiv.org/html/2605.10760` | Primary arXiv HTML | Section 3.1 local tracking/mapping terms and equations | Extracted DROID front-end, sliding co-visibility window, `L_BA`, JDSA, `L_map`, submap freezing, Sim(3) correction. Literal `local_tracking` was not found. |
| `https://arxiv.org/html/2605.10760` | Primary arXiv HTML | Graph/fusion coupling | Extracted `r_e^geo`, `r_e^pho`, graph objective prefix, LM/Gauss-Newton solver, reactive PGBA update, occupancy fusion, and `L_refine`. |
| `https://mags-slam.github.io/` | Project page | Project claims and availability | Project page text identifies the method as RGB-only multi-agent 3DGS SLAM, says agents build local monocular Gaussian submaps and transmit compact summaries, and says code/data released upon acceptance. |
| `/home/prannayag/pragnition/robotics/mosaic/outputs/multi-robot-gaussian-slam-research-code.md` | Prior local research note | Code availability | Lines around the MAGS row state only website/source repo found, no implementation repo; useful corroboration but secondary. |

## 8. Suggested literature-review wording

Use wording like:

> In MAGS-SLAM, the review’s `local_tracking_i` should be read as a normalized stage label rather than a named paper function. The primary paper describes this stage as local per-agent monocular Gaussian SLAM: each agent runs a DROID-based monocular front-end over a sliding co-visibility window, refines poses and depth maps with dense BA, and couples depth to learned Metric3D priors through Joint Depth-Scale Adjustment. Registered keyframes back-project inverse-depth maps to seed Gaussians, and the local Gaussian map is optimized against keyframes with image, depth, normal, and isotropy losses. Once a submap reaches a keyframe or motion threshold it is frozen, detached from local BA, and assigned a Sim(3) correction for subsequent submap-graph alignment and occupancy-aware fusion. Thus the MAGS local stage is monocular scale/depth aware and submap-bounded, not a confirmed code-level `local_tracking` function and not an RGB-D photometric-depth tracker in the MAGiC-SLAM sense.
