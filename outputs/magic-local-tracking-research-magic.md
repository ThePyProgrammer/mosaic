# MAGiC-SLAM local tracking evidence slice

Scope: MAGiC-SLAM only. Focus: photometric-depth tracking mechanics and evidence boundaries for comparison against generic `local_tracking` abstractions in MAC-Ego3D/CoKo-SLAM/MAGS-SLAM.

## Task ledger

| Task | Status | Notes |
|---|---:|---|
| Locate local MAGiC-SLAM sources under `research/slam-survey` | done | Found survey TeX/BibTeX and `diagrams/magic_slam.pdf`. |
| Check primary paper/project/repo URLs | done | Used CVPR OpenAccess, project page, arXiv, and GitHub README page. |
| Extract tracking objective and schedule | done | Extracted from CVPR PDF text via local `pdftotext`; web PDF body extraction was not reliable. |
| Identify blocked items | blocked | Did not inspect supplementary material/source code internals; only primary paper/project/repo landing pages and local survey files were used. |

## Canonical bibliographic identity

- **Title:** *MAGiC-SLAM: Multi-Agent Gaussian Globally Consistent SLAM*.
- **Authors:** Vladimir Yugay, Theo Gevers, Martin R. Oswald.
- **Venue:** CVPR 2025, pp. 6741--6750.
- **arXiv:** arXiv:2411.16785v1, submitted 25 Nov 2024.
- **Project/repo:** project page `https://vladimiryugay.github.io/magic_slam`; repository `https://github.com/VladimirYugay/MAGiC-SLAM`.

## Tracking mechanics evidenced in the paper

MAGiC-SLAM is not just a placeholder `local_tracking_i(Z_i^{1:t}, M_{i,t-1})`. The paper specifies a two-stage **hybrid implicit tracking** module per RGB-D agent:

1. **Pose initialization: deterministic frame-to-frame dense registration.** At time `t`, given colored point cloud `P_t`, MAGiC-SLAM estimates `T_{t-1,t} in SE(3)` relative to previous point cloud `P_{t-1}`. Registration is multi-scale, voxelizes both point clouds, computes correspondences `K = {(p,q)}` using ICP, and optimizes an objective combining color and geometric residuals:

   `E(T_{t-1,t}) = (1-sigma) sum_{(p,q) in K} (r_C^{(p,q)}(T_{t-1,t}))^2 + sigma sum_{(p,q) in K} (r_G^{(p,q)}(T_{t-1,t}))^2`

   with `sigma in [0,1]`; geometric residual `r_G^{(p,q)} = (((T_{t-1,t}(q)-p)n_p))^2`; color residual uses a tangent-plane projection and continuous intensity function. The paper says this loss is optimized to convergence with Gauss-Newton. Source: CVPR paper, Sec. 3.2, Eqs. 6--7/page 6744.

2. **Pose refinement: frame-to-model re-rendering optimization against the active Gaussian sub-map.** The initialized relative pose is refined by freezing all Gaussian parameters and minimizing:

   `argmin_{T_{t-1,t}} L_tracking( I_hat(T_{t-1,t}), D_hat(T_{t-1,t}), I_t, D_t, alpha_t )`

   where `I_hat(T_{t-1,t})` and `D_hat(T_{t-1,t})` are rendered color/depth from the **sub-map warped by the relative transformation**, and `I_t`, `D_t` are the input RGB-D frame. Source: CVPR paper, Sec. 3.2, Eq. 8/page 6744.

3. **Exact photometric-depth tracking loss.** The tracking loss uses RGB/color and depth with masks:

   `L_tracking = sum M_inlier * M_alpha * ( lambda_c |I_hat - I|_1 + (1-lambda_c) |D_hat - D|_1 )`.

   `M_alpha` is a soft alpha mask derived from the alpha map rendered from 3D Gaussians. `M_inlier` discards pixels whose color/depth errors exceed a frame-relative threshold. The paper states the weighting guides optimization to well-reconstructed regions where accumulated alpha values are close to 1 and rendering quality is high. Source: CVPR paper, Sec. 3.2, Eq. 9/page 6744.

4. **Variables optimized.** Local tracking optimizes the **relative camera pose** `T_{t-1,t} in SE(3)`; in the refinement stage Gaussian parameters are explicitly frozen. Mapping optimizes Gaussian/sub-map parameters separately using color, depth, and regularization losses, but that is not the tracking objective.

5. **RGB/depth usage.** MAGiC-SLAM consumes single-camera **RGB-D** streams. Tracking uses both color and depth twice: (a) point-cloud registration is on colored point clouds, with color and geometric residuals; (b) pose refinement minimizes rendered color and rendered depth residuals against `I_t`, `D_t`. The project/survey architecture also says each agent processes an RGB-D stream and maintains a local sub-map.

6. **Rendering/map source.** The refinement renders color/depth from the agent's active 3D Gaussian sub-map after warping it with `T_{t-1,t}`. Local mapping initializes sub-maps from the first frame, adds Gaussians in low-density regions based on rendered opacity, and uses the active sub-map as the local scene representation. Source: CVPR paper, Secs. 3, 3.1, 3.2; local `magic_slam.pdf` diagram.

7. **Pose update schedule and server interaction.** Each agent maintains local sub-maps and trajectory estimates. A new sub-map is created and the previous one is sent to the server every `theta_submap` frames. When a new sub-map starts, the previous sub-map and image features go to the central server; the server performs loop detection, loop constraint estimation, pose graph optimization, updates stored sub-maps, and returns optimized poses to the agents. Pose graph optimization provides pose corrections for every sub-map of every agent, and all camera poses belonging to a sub-map are corrected. Source: CVPR paper, Fig. 2 caption and Secs. 3.1, 3.3; local diagram.

## Direct quotes and citation-ready claims

- Figure 1 caption: "Given single-camera RGBD input streams from multiple simultaneously operating agents MAGiC-SLAM estimates their trajectories and reconstructs a 3D Gaussian map that can be rendered from previously unseen viewpoints." Source: CVPR paper page 6741.
- Abstract/introduction claim: prior multi-agent NVS SLAM is "slow, cannot accurately render real-world data, are restricted to two agents, and have limited tracking accuracy"; MAGiC-SLAM proposes a rigidly deformable 3D Gaussian representation plus "new tracking and map-merging mechanisms" and loop closure. Source: CVPR paper page 6741.
- Method overview: "Every agent processes an RGB-D stream performing local mapping and tracking. 3D Gaussians are used to represent the agents' sub-maps and to improve tracking accuracy." Source: CVPR paper Sec. 3/page 6743.
- Tracking section: "we propose a hybrid implicit tracking approach" that initializes relative pose with "deterministic frame-to-frame dense registration" and refines it through "frame-to-model optimization." Source: CVPR paper Sec. 3.2/page 6743.
- Difference from common NVS SLAM initialization: this approach "differs from previous NVS SLAM methods, initializing the relative pose based on a constant speed assumption." Source: CVPR paper Sec. 3.2/page 6743.
- Pose refinement: "we freeze all Gaussian parameters" and minimize Eq. 8; rendered color/depth come from "the sub-map warped with the relative transformation `T_{t-1,t}`." Source: CVPR paper Sec. 3.2/page 6744.
- Sub-map schedule: "A new sub-map is created, and the previous one is sent to the server after every `theta_submap` frame." Source: CVPR paper Sec. 3.1/page 6743.

## What is directly evidenced vs inferred

| Item | Status | Basis |
|---|---:|---|
| MAGiC-SLAM uses RGB-D inputs | directly evidenced | Fig. 1 caption, Sec. 3, project page, local survey diagram. |
| Local tracking optimizes `T_{t-1,t} in SE(3)` | directly evidenced | Sec. 3.2 Pose Initialization and Eq. 8. |
| Tracking loss combines rendered RGB and rendered depth | directly evidenced | Eq. 9 and surrounding text. |
| Refinement freezes Gaussian parameters | directly evidenced | Sec. 3.2 Pose Refinement. |
| Rendering source is active Gaussian sub-map warped by relative pose | directly evidenced | Text before/after Eq. 8 and Fig. 2. |
| New sub-map/upload schedule every `theta_submap` frames | directly evidenced | Sec. 3.1. |
| Loop closure/Pose graph corrections feed back to agents | directly evidenced | Sec. 3 and Fig. 2 caption. |
| The survey shorthand `argmin_T L_rgbd(z, render(M,T))` accurately summarizes tracking | inferred abstraction | It compresses the two-stage initialization/refinement into one line; paper is more specific. |
| The final pose stored in a global trajectory is `T_{ell_i <- i,t}` | inferred notation | Local survey notation; MAGiC paper uses relative frame-to-frame and sub-map/correction notation. |
| Direct comparison to MAC-Ego3D/CoKo-SLAM/MAGS-SLAM | out of scope for this slice | This note only gathered MAGiC-SLAM evidence. |

## Verification table

| Source | Type | Used for | Verification status |
|---|---|---|---:|
| `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey/main.tex` | local survey TeX | Existing local algorithm shorthand, survey-level claims, repo footnote | verified/read |
| `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey/references.bib` | local BibTeX | Canonical CVPR citation and URL | verified/read |
| `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey/diagrams/magic_slam.pdf` | local diagram PDF | Agent/server flow labels: tracking, mapping, image features, sub-maps, loop detection/registration, PGO, merge/refinement | verified/read |
| `https://openaccess.thecvf.com/content/CVPR2025/html/Yugay_MAGiC-SLAM_Multi-Agent_Gaussian_Globally_Consistent__SLAM_CVPR_2025_paper.html` | CVPR OpenAccess HTML | Metadata, PDF link, abstract-level claims | verified/fetched |
| `https://openaccess.thecvf.com/content/CVPR2025/papers/Yugay_MAGiC-SLAM_Multi-Agent_Gaussian_Globally_Consistent__SLAM_CVPR_2025_paper.pdf` | CVPR PDF | Primary tracking equations, section/page references, method details | verified/downloaded to `/tmp` and text-extracted |
| `https://vladimiryugay.github.io/magic_slam` | project page | Project links and high-level architecture claims | verified/fetched |
| `https://arxiv.org/abs/2411.16785` | arXiv page | arXiv identifier/version/date | verified/fetched |
| `https://github.com/VladimirYugay/MAGiC-SLAM` | repository page | Public repo existence and README-level run/code availability | verified/fetched |
