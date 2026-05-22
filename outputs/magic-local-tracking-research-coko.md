# CoKo-SLAM local tracking evidence slice

## Scope and answer

Scope: CoKo-SLAM only, for distinguishing CoKo-SLAM's local tracking evidence from MAGiC-SLAM-style photometric-depth tracking. I checked the local survey sources under `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey`, the CoKo-SLAM arXiv page/paper, and the public repository.

Short answer: `local_tracking` is not a named CoKo-SLAM paper module or repository function. It is a survey/inferred stage name for each agent's pose-estimation step. CoKo-SLAM explicitly says its tracking is the same as MAGiC-SLAM and builds on MAGiC-SLAM's codebase; the CoKo-specific contributions are feature-vector keyframing, Gaussian compaction, and server-side loop closure/registration without initial inter-agent relative poses. In the public code, the concrete local tracking implementation is `Tracker.track(...)`, not `local_tracking`.

## Canonical paper metadata

- Title: **Compact Keyframe-Optimized Multi-Agent Gaussian Splatting SLAM**
- Authors: Monica M. Q. Li, Pierre-Yves Lajoie, Jialiang Liu, Giovanni Beltrame
- Identifier: arXiv:2604.00804, primary class cs.RO, DOI `10.48550/arXiv.2604.00804`
- Date visible in PDF: April 2, 2026
- Local BibTeX source: `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey/references.bib`
- Primary URL: `https://arxiv.org/abs/2604.00804`
- Public code URL: `https://github.com/lemonci/coko-slam`

## Is `local_tracking` a paper concept, code function, script, or inferred stage?

| Item | Status | Evidence |
|---|---:|---|
| Paper concept named `local_tracking` | No direct evidence | The arXiv text discusses tracking and says CoKo-SLAM's tracking is inherited/same as MAGiC-SLAM, but the visible paper text does not define a symbol or component named `local_tracking`. |
| Code function named `local_tracking` | No direct evidence | Repository search found `src/entities/tracker.py:class Tracker` and `def track(...)`, but no `local_tracking` function/script name in the searched Python/README files. |
| Script named `local_tracking` | No direct evidence | README run entry is `python run_slam.py configs/<dataset_name>/<config_name> --input_path <path_to_the_scene> --output_path <output_path>`; no local-tracking script was visible. |
| Inferred/survey stage | Yes | The local survey draft uses `\operatorname{local\_tracking}_i` as a generic operator in `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey/main.tex:101` and places CoKo-SLAM's pose/keyframe update under that operator at lines 221-222. This is survey notation, not a CoKo paper term. |
| Concrete CoKo code implementation | `Tracker.track(...)` | Public repo clone at `/tmp/coko-slam/src/entities/tracker.py:107` defines `track(self, frame_id, gaussian_model, prev_c2ws) -> np.ndarray`; `/tmp/coko-slam/src/entities/agent.py:300-303` calls it during each agent's run loop. |

## Tracking/local-map/window objective details

### Direct paper evidence

1. CoKo-SLAM is built on MAGiC-SLAM and inherits tracking.
   - Paper text: "Building on MAGiC-SLAM's codebase, we made three key improvements: we enhanced the keyframe selection method, adopted a compaction technique during 3D Gaussian training to reduce submap size, and implemented loop closure using pure 3D Gaussian submaps without requiring prior knowledge of the initial relative poses between agents."
   - Paper text: "As our tracking is the same as that of MAGiC-SLAM, tracking error is not reported."
   - Interpretation: CoKo-SLAM does not introduce a new local tracking objective in the paper. Any CoKo local-tracking description should be marked as inherited from MAGiC-SLAM or code-level behavior, not a novel CoKo contribution.

2. Paper recap of inherited MAGiC-SLAM tracking.
   - Paper text: "During tracking, MAGiC-SLAM employs a hybrid implicit frame-to-frame and frame-to-model strategy. First, a coarse pose initialization uses deterministic dense registration via multi-scale ICP: at each scale s in {1, ..., S}, voxelized point clouds P_t, P_{t-1} are aligned by minimizing the joint loss of rendered color and depth according to the camera RGB-D images. Next, pose refinement freezes Gaussian parameters and minimizes the re-rendering loss based on color and depth errors. In the refinement, pixels with low opacity or high residuals are masked out to focus on well-reconstructed regions."
   - Variables optimized, from this text: camera pose/relative pose during tracking; Gaussian parameters are frozen during refinement.
   - Objective terms, from this text: joint rendered color and depth loss; re-rendering loss based on color and depth errors; masks for low opacity and high residual pixels.
   - Rendering/map source: rendered color/depth from the existing Gaussian model/submap, compared against current RGB-D camera images.

3. Paper mapping objective is separate from tracking.
   - Paper text defines mapping loss: `L = lambda_color * L_color + lambda_depth * L_depth + lambda_reg * L_reg`.
   - Paper text defines `L_color = (1 - rho) * |I_hat - I|_1 + rho(1 - SSIM(I_hat, I))`, with `I_hat` rendered and `I` input.
   - Paper text defines `L_depth = |D_hat - D|_1`, with `D_hat` rendered and `D` input depth.
   - Paper text defines `L_reg` as an average scale regularizer over Gaussians, penalizing elongation along the principal axis.
   - Interpretation: This is mapping/3DGS training, not the novel local-tracking objective; it matters because CoKo's compaction is inserted into 3D Gaussian training/mapping.

4. CoKo-specific keyframe/window/submap policy.
   - Paper keyframing variables: previous keyframe set in a submap `K`, current incoming frame `E`, feature extractor `phi(.)`, threshold `alpha`.
   - Paper criterion: compute `d = min_{K in K} ||phi(E) - phi(K)||`; select current frame as keyframe if `d >= alpha`.
   - Paper submap window: sets the number of keyframes per submap to 10, aligned with original MAGiC-SLAM configuration.
   - Coupling to local tracking: the paper says keyframes are used as a source for localization, mapping, and loop-closure detection, but the keyframe selection itself is a CoKo contribution separate from inherited tracking.

5. Coupling to mapping and server/global optimization.
   - Agents transmit keyframe feature vectors, camera poses, and 3D Gaussian submaps to the central server; abstract also says the system relies on a centralized server to merge and optimize local maps.
   - Local mapping includes compaction/sparsification to remove redundant Gaussians; code and paper distinguish mapping/submap construction from tracking.
   - Server loop closure begins when a new submap is finalized and has three stages: loop detection, loop edge constraint, pose graph optimization.
   - Rendered-depth loop edge mode: render depth images `D_hat_S` and `D_hat_T` from first keyframe views in source/target submaps; convert to point clouds `P_hat_S`, `P_hat_T`; extract FPFH; coarse registration by RANSAC; refine by ICP.
   - Camera-depth loop edge mode: use camera depth images `D_S`, `D_T` directly to build point clouds `P_S`, `P_T`, with the same registration methods.
   - PGO variables: pose graph nodes `Delta X_k` represent relative corrections for each submap `k`; loop edges connect detected pairs `(k,j)` with relative transform `T_kj` and information matrix `Lambda_kj`; optimizer solves for all `{Delta X_k}` using a robust line-process formulation via GTSAM.
   - Server fusion: after PGO, server concatenates cached submaps while excluding zero-opacity Gaussians in coarse merging, then briefly optimizes Gaussian color and position using rendering losses and prunes zero-opacity Gaussians.

### Direct repository evidence

Repository path inspected: public clone at `/tmp/coko-slam` from `https://github.com/lemonci/coko-slam`.

- `/tmp/coko-slam/src/entities/tracker.py:27` defines `class Tracker`.
- `/tmp/coko-slam/src/entities/tracker.py:107` defines `Tracker.track(self, frame_id: int, gaussian_model: GaussianModel, prev_c2ws: np.ndarray) -> np.ndarray`.
- `/tmp/coko-slam/src/entities/agent.py:300-303` calls `self.tracker.track(frame_id, gaussian_model, prev_c2ws)` for frames after initialization.
- Tracking initialization options in code:
  - `odometry_type == "gt"`: returns ground-truth `gt_c2w`.
  - `odometry_type == "const_speed"`: initializes current pose using constant-speed composition from prior poses.
  - `odometry_type == "odometer"`: estimates a relative pose from RGB-D visual odometry via `VisualOdometer.estimate_rel_pose(image, depth)`.
- Optimized tracking variables in code:
  - `opt_cam_rot`: optimizable quaternion parameter from the estimated relative world-to-camera transform.
  - `opt_cam_trans`: optimizable translation parameter.
  - Code forms a relative transform, applies it to Gaussian means, composes Gaussian rotations with the quaternion, renders, backpropagates loss, and optimizer-steps only the camera parameters set by `gaussian_model.training_setup_camera(...)`.
- Code tracking loss:
  - Rendered outputs: `rendered_color`, `rendered_depth`, `alpha` from `render_gaussian_model(...)` over the current `gaussian_model` with transformed points/rotations.
  - Masks: `depth_mask = gt_depth > 0`; `alpha_mask = alpha > alpha_thre`; `tracking_mask` requires valid depth and optionally removes outlier depth residuals larger than `50 * median(depth_err)`; soft alpha weighting optionally multiplies color/depth losses by `alpha ** 3`; optional invalid-depth mask for color loss.
  - `color_loss = l1_loss(rendered_color, gt_color, agg="none")`, summed after masking/weighting.
  - `depth_loss = l1_loss(rendered_depth, gt_depth, agg="none") * tracking_mask`, summed after optional weighting.
  - `total_loss = w_color_loss * color_loss + (1 - w_color_loss) * depth_loss`.
- Rendering/map source in code:
  - Current local `GaussianModel` passed from the agent run loop; `get_render_settings(...)` uses the previous camera pose as the reference view; render occurs after applying the optimized relative camera transform to Gaussian means and rotations.
- Coupling to mapping in code:
  - Agent initializes map on frame 0, then for each frame estimates pose with `Tracker.track`, stores `estimated_c2ws[frame_id]`, computes DINO-style frame features, decides whether to start a new submap or map a keyframe, and calls `self.mapper.map(...)` only when mapping/submap conditions trigger.
  - After local run, submaps are saved in one of `pcd`, `depth`, or `render_depth` anchor modes, sent through a pipe with `("pgo", agents_submaps)`, and optimized keyframe poses are received from the server.

## Direct evidence vs inference

| Claim | Evidence type | Confidence | Notes |
|---|---|---:|---|
| CoKo-SLAM canonical title/authors/arXiv ID | Direct | High | Local BibTeX and arXiv page agree. |
| `local_tracking` is not a CoKo paper term/function | Direct absence plus source search | Medium-high | Searched local paper text, diagram text, README, and Python files. Absence cannot be absolute beyond inspected sources, but no evidence found. |
| CoKo tracking is inherited/same as MAGiC-SLAM | Direct | High | Paper explicitly states it builds on MAGiC-SLAM codebase and tracking is the same as MAGiC-SLAM. |
| Concrete code local tracker optimizes relative camera quaternion and translation against rendered color/depth L1 loss | Direct code evidence | High | From `/tmp/coko-slam/src/entities/tracker.py`. |
| CoKo's own novelty is not local tracking but keyframing, compaction, and loop closure without initial relative poses | Direct | High | Stated in paper method/contributions. |
| Survey `local_tracking_i(...)` line for CoKo is an inferred abstraction | Direct local survey evidence plus inference | High | `/research/slam-survey/main.tex` says algorithms are survey-level procedures, not executable source code; CoKo algorithm line uses generic `local_tracking_i`. |
| CoKo differs from MAGiC-SLAM tracking | Negative finding | High | It does not materially differ in local tracking per paper; differences are downstream/update-selection/mapping/server registration. |

## Verification table

| Source | Location / URL | What was verified | Result |
|---|---|---|---|
| Local survey draft | `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey/main.tex` | Generic notation and CoKo survey algorithm | `local_tracking_i` appears as survey notation; local algorithms are declared survey-level, not executable source. |
| Local BibTeX | `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey/references.bib` | Canonical metadata | `li2026coko_slam` gives title, authors, arXiv ID 2604.00804, DOI, URL. |
| Local CoKo diagram | `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey/diagrams/coko_slam.pdf` | Pipeline labels | Diagram says: "3D Gaussian Tracking with rendered loss", "Keyframe selection based on feature vector cosine similarity", "3D Gaussian Mapping with compaction", server-side registration and PGO. |
| arXiv abstract page | `https://arxiv.org/abs/2604.00804` | Metadata and abstract claims | Confirms title/authors/arXiv ID, central server merge/optimization, 85-95% data reduction, rendered-depth and camera-depth loop closure modes. |
| arXiv PDF | `https://arxiv.org/pdf/2604.00804` downloaded to `/tmp/coko.pdf` | Method details | Confirms inherited MAGiC-SLAM tracking, keyframing criterion, compaction algorithm, loop-closure registration and PGO, and "tracking is the same as MAGiC-SLAM" statement. |
| GitHub repo README | `https://github.com/lemonci/coko-slam` | Run scripts and visible names | README exposes `run_slam.py`, configs, datasets, visualization; no `local_tracking` script/function visible. |
| GitHub repo clone | `/tmp/coko-slam/src/entities/tracker.py` | Concrete tracker implementation | Confirms `Tracker.track`, camera-pose optimization variables, rendered RGB-D losses, masks, current Gaussian model source. |
| GitHub repo clone | `/tmp/coko-slam/src/entities/agent.py` | Tracking/mapping coupling | Confirms agent loop calls tracker before keyframe/submap mapping and later sends submaps for PGO. |

## Done / blocked ledger

### Done

- Checked local CoKo sources under `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey`.
- Extracted text from `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey/diagrams/coko_slam.pdf`.
- Verified canonical metadata from local BibTeX and arXiv.
- Downloaded and text-searched the arXiv PDF for tracking, mapping, keyframing, compaction, loop closure, and PGO terms.
- Inspected the public CoKo-SLAM repository for concrete tracking function/script names and tracking objective code.
- Wrote this CoKo-only findings file.

### Blocked / limitations

- The local diagram PDF could not be processed through the CCS image-analysis provider, so I used `pdftotext` instead.
- I did not run CoKo-SLAM; the evidence is static paper/code inspection.
- The public repo was cloned into `/tmp/coko-slam` for inspection, so line references are to that transient clone rather than a vendored local source tree.
