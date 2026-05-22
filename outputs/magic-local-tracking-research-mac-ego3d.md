# MAC-Ego3D local tracking evidence slice

## Scope

This note covers MAC-Ego3D only. It is intended to support a later comparison against MAGiC-SLAM photometric-depth tracking; MAGiC-SLAM evidence is not re-researched here.

## Canonical source identity

- **Title:** *MAC-Ego3D: Multi-Agent Gaussian Consensus for Real-Time Collaborative Ego-Motion and Photorealistic 3D Reconstruction*
- **Authors:** Xiaohao Xu, Feng Xue, Shibo Zhao, Yike Pan, Sebastian Scherer, Xiaonan Huang
- **Identifier/status:** arXiv:2412.09723, cs.CV, 2024 arXiv preprint
- **Primary code URL:** https://github.com/Xiaohao-Xu/MAC-Ego3D
- **Local bibliography evidence:** `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey/references.bib:11-18`

## Is `local_tracking` a MAC-Ego3D paper concept, code function, script, or inferred stage?

`local_tracking` is **not a literal MAC-Ego3D paper term or repository function name** in the evidence checked here. It is best classified as an **inferred survey-stage label** used by the local literature-review notation to represent the per-agent pose-estimation/tracking part of MAC-Ego3D.

Evidence:

- The local survey explicitly warns that its algorithm boxes are survey-level procedures, not executable source code: `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey/main.tex:157-160`.
- The local survey's MAC-Ego3D algorithm uses `\operatorname{local\_tracking}_i(...)` at `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey/main.tex:190-204`, but this is the survey author's notation.
- The repository README fetched from `https://raw.githubusercontent.com/Xiaohao-Xu/MAC-Ego3D/main/README.md` does **not** contain literal `local_tracking`; it uses broader phrases such as “real-time pose tracking,” “Intra-Agent Gaussian Consensus,” and “Inter-Agent Gaussian Consensus.”
- The code-level entry point is a `Tracker` class with `tracking()` in `mac_Tracker.py`, plus `Mapper`/`mapping()` in `mac_Mapper.py`; no literal `local_tracking` function was found in the checked key files.

## Tracking/local-map/window objective terms and optimized variables

### Paper-level formulation

MAC-Ego3D frames the overall problem as collaborative multi-agent RGB-D SLAM. Each agent captures RGB-D observations and estimates poses while refining a local map:

- Observations: `Z_{a_i}^{1:t} = {(I_{a_i}^k, D_{a_i}^k)}_{k=1}^t`.
- Per-agent poses: `T_{a_i}^{1:t} \in SE(3)`.
- Per-agent local map: `M_{a_i}`.
- Global/shared map: `M`.

The paper text extracted from arXiv says each agent “estimates its poses `T_{a_i}^{1:t} \in SE(3)` and incrementally refines a local map `M_{a_i}`,” and formulates “a joint optimization of poses and local maps across agents” to form a consistent global map.

The intra-agent/local objective is named `f^{a_i}`:

- `f^{a_i}` “encapsulates the mapping and pose estimation errors” based on local observations.
- The local process is “Intra-Agent Gaussian Consensus,” where the agent integrates observations into `M_{a_i}`.
- Intra-agent selection chooses candidate Gaussians from `M_{a_i}` inside the current field of view and within a specified distance from estimated pose `T_{a_i}^k`.
- Association matches observed Gaussians `G_{a_i}^k ~ N(x_{a_i}^k, Sigma_{a_i}^k)` to candidate map Gaussians.
- Alignment for pose tracking maximizes the likelihood of observations given the current map: `p(T_{a_i}^{1:t}, M_{a_i} | Z_{a_i}^{1:t})`, with motion model `p(T_{a_i}^k | T_{a_i}^{k-1})` and observation model `p(Z_{a_i}^k | T_{a_i}^k, M_{a_i})`.
- The observed-Gaussian likelihood is written as `p(X_{a_i}^k | M_{a_i}, T_{a_i}^k)` over Gaussian correspondences.
- The paper states that by minimizing Mahalanobis distance between transformed observed points and map points, the agent refines pose `T_{a_i}^k`, aligning observations to the local map.

### Rendering/map source

MAC-Ego3D's map source is a 3D Gaussian splat map. The paper defines each Gaussian by mean position `x_i`, covariance `Sigma_i`, opacity `lambda_i`, and color `c_i`. These splats can be rendered from arbitrary viewpoints using differentiable rendering.

For local map optimization after tracking/alignment:

- The agent updates `M_{a_i}` by integrating new Gaussian splats, adjusting existing Gaussians, and adding new ones.
- The local map is further optimized by differentiable rendering against observed RGB-D images.
- The paper states this minimizes a photometric loss between rendered map images and actual observations, refining Gaussian parameters.

For inter-agent/global coupling:

- Inter-agent consensus aligns overlapping local maps by finding a relative transform `T_{a_i a_j}` that minimizes discrepancies between corresponding Gaussians.
- After alignment, local maps are integrated into a global map `M`.
- The global/inter-agent loss penalizes visual and geometric inconsistencies: L1 RGB differences, SSIM structural consistency, and L1 depth difference `|D_i - D_j|_1`, where depths are rendered from Gaussian splats.
- The paper states `alpha` balances map consistency with pose alignment, and that jointly optimizing poses `{T_{a_i}}` and global map `M` lets agents maintain map and pose consistency.

### Code-level implementation evidence

The checked public code looks more ICP/pose-graph driven for tracking than explicit photometric-depth pose optimization:

- `mac_Tracker.py` defines `class Tracker` and `def tracking(self)`.
- The tracker down-samples RGB-D depth to point clouds and trackable points, sets target/source filters, and calls `self.reg.align(initial_pose)` to estimate `current_pose`.
- The code comment at `mac_Tracker.py` says “Here current_pose is the camera's pose.”
- Loop closure uses descriptor similarity, `rel_FGICP.align(current_pose)`, GTSAM `BetweenFactorPose3`, and `gtsam.LevenbergMarquardtOptimizer(...).optimize()` to update pose estimates.
- Mapping receives shared new Gaussians from tracking, initializes/adds them to the Gaussian model, and shares target trackable Gaussians back via `get_trackable_gaussians_tensor(...)`.
- `mac_Mapper.py` optimizes Gaussian map parameters with rendered RGB and depth losses: `render_3(...)`, `render_depth`, `render`, RGB L1+SSIM loss, depth L1 loss, `loss = 1 * loss_rgb + 2 * loss_d`, `loss.backward()`, then `self.gaussians.optimizer.step()`.
- `mac_ego.py` starts tracking and mapping as separate multiprocessing processes via `Tracker(self)` and `Mapper(self)`.

This code evidence supports treating MAC-Ego3D's local tracking as a per-agent geometric registration/pose-estimation stage coupled to mapping through shared Gaussian/trackable point buffers, not as a function literally named `local_tracking`.

## How this differs from MAGiC-SLAM photometric-depth tracking, based on MAC-Ego3D-only evidence

From the MAC-Ego3D side, the difference to preserve for the later comparison is:

- MAC-Ego3D's paper-level local tracking is described as **intra-agent Gaussian consensus pose estimation**: select nearby/covisible Gaussians from the local map, associate observed RGB-D-derived Gaussians/points with map Gaussians, and refine `T_{a_i}^k` by probabilistic/geometric alignment against the local Gaussian map.
- MAC-Ego3D's code-level tracking evidence uses **filtered point-cloud/Generalized-ICP style alignment plus GTSAM pose-graph loop-closure optimization**, while photometric/depth rendering losses are clearly present in mapping/global map optimization.
- Therefore, if MAGiC-SLAM is written as an explicit `argmin_T L_rgbd(z_t, render(M_{t-1}, T))`, that is a stronger photometric-depth pose-tracking statement than the MAC-Ego3D evidence checked here. MAC-Ego3D uses RGB-D rendering and RGB/depth losses for Gaussian map/consensus optimization, but the directly observed tracking implementation centers on geometric registration and pose graph updates.

## Direct evidence vs inference

| Claim | Classification | Evidence |
|---|---:|---|
| Canonical paper title/authors/arXiv ID | Direct | arXiv page and local bibliography `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey/references.bib:11-18` |
| MAC-Ego3D uses Gaussian consensus, local maps, and RGB-D rendering | Direct | arXiv abstract/method text; local survey `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey/main.tex:185-207` |
| Literal `local_tracking` is part of MAC-Ego3D's paper terminology | Not supported | Not found in fetched README or checked code; local survey uses it as notation and says algorithms are survey-level procedures |
| `local_tracking_i` in the local survey denotes per-agent RGB-D tracking from observations and prior local map | Direct for local survey notation; inference for MAC-Ego3D terminology | `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey/main.tex:190-204` |
| MAC-Ego3D optimizes per-agent poses `T_{a_i}^{1:t}` and local maps `M_{a_i}` | Direct | arXiv PDF text around problem formulation and intra-agent consensus |
| MAC-Ego3D local pose refinement minimizes Mahalanobis distance between transformed observed points and map points | Direct | arXiv PDF text around intra-agent alignment |
| Code-level tracking uses `Tracker.tracking()`, `self.reg.align(initial_pose)`, and GTSAM optimization | Direct | GitHub raw `mac_Tracker.py` inspected via GitHub raw URLs |
| Photometric/depth losses are present in mapping, not proven as the code's tracking objective | Direct for mapping loss; inference for absence from tracking objective | GitHub raw `mac_Mapper.py` and `mac_Tracker.py` inspected |

## Verification table

| Source | Type | What was checked | Result |
|---|---|---|---|
| `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey/references.bib` | Local file | MAC-Ego3D citation metadata | Verified arXiv title/authors/eprint at lines 11-18 |
| `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey/main.tex` | Local file | Survey notation and MAC-Ego3D local-tracking algorithm | Verified `local_tracking_i` is survey notation and MAC-Ego3D section at lines 185-207; survey caveat at lines 157-160 |
| `https://arxiv.org/abs/2412.09723` | Primary paper page | Canonical title/authors/arXiv status and abstract terms | Verified title, authors, arXiv ID, Gaussian consensus, local maps, RGB-D rendering |
| `https://arxiv.org/pdf/2412.09723` | Primary paper PDF | Method details for variables/objectives | Verified poses `T`, local maps `M_a_i`, intra/inter-agent objectives, Gaussian association/alignment/optimization, RGB/depth rendering losses |
| `https://github.com/Xiaohao-Xu/MAC-Ego3D` | Primary repo | Repository existence and README | Verified README; no literal `local_tracking`; found real-time pose tracking and scripts |
| `https://raw.githubusercontent.com/Xiaohao-Xu/MAC-Ego3D/main/mac_Tracker.py` | Primary repo raw file | Tracking implementation names/objectives | Verified `Tracker.tracking()`, filtered point clouds, `self.reg.align(initial_pose)`, loop closure, GTSAM optimizer |
| `https://raw.githubusercontent.com/Xiaohao-Xu/MAC-Ego3D/main/mac_Mapper.py` | Primary repo raw file | Mapping/rendering losses | Verified Gaussian insertion, trackable Gaussian sharing, RGB L1+SSIM and depth L1 rendering losses |
| `https://raw.githubusercontent.com/Xiaohao-Xu/MAC-Ego3D/main/mac_ego.py` | Primary repo raw file | Tracking/mapping process coupling | Verified separate `tracking` and `mapping` multiprocessing entry points |

## Done/blocked ledger

### Done

- Read local MAC-Ego3D citation and survey section under `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey`.
- Verified primary arXiv metadata and extracted method-level tracking/local-map/consensus terms from arXiv PDF text.
- Verified public repository README and key raw files for `Tracker`, `Mapper`, and process coupling.
- Classified `local_tracking` as local-survey notation / inferred stage rather than a literal MAC-Ego3D paper or code construct.
- Wrote this evidence note to `/home/prannayag/pragnition/robotics/mosaic/outputs/magic-local-tracking-research-mac-ego3d.md`.

### Blocked or unresolved

- The project-page URL guessed from the author/repo pattern returned 404, so no separate project-page evidence was used.
- Web search provider failed on the initial broad query; primary arXiv and GitHub URLs were still reachable directly.
- Full repository-wide string search was not performed by cloning the repo; evidence comes from README plus key raw source files identified through GitHub API listing.
