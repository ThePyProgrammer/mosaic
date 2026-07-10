# AgriGS-SLAM follow-up evidence: native multi-camera / robot-mounted multi-view online 3DGS SLAM

Date: 2026-05-18

Scope: targeted evidence collection for AgriGS-SLAM and any other true native multi-camera, robot-mounted, online 3D Gaussian Splatting SLAM implementations. This report is evidence-only and uses conservative classification rules: stereo, RGB-D, multi-agent, and temporally accumulated multi-view frames are not treated as a general synchronized multi-camera rig unless the source documents that support.

## Executive evidence notes

- AgriGS-SLAM is the only source found in this follow-up with primary-source evidence for a robot-mounted synchronized multi-camera 3DGS SLAM pipeline.
- Primary sources consistently describe AgriGS-SLAM as a Visual-LiDAR SLAM framework using multi-camera / multi-view 3DGS, direct LiDAR odometry, loop closures, and orchard deployment.
- The repository README and demo dataset card give the strongest concrete rig evidence: three synchronized RGB-D cameras, tractor-mounted platform, Ouster/FixPosition-style agricultural sensor suite, demo data with `zed_multi/cam_1`, `cam_2`, `cam_3`, and per-camera calibration in `config/default.yaml`.
- The paper adds algorithmic evidence: all cameras at each keyframe are optimized jointly against one shared Gaussian map, with batch rasterization over complementary viewpoints rather than per-camera splat copies.
- Benchmarks are paper-level for full numbers. The paper reports apple and pear orchards across dormancy, flowering, and harvesting, with PSNR/SSIM/LPIPS and ATE, compared against Photo-SLAM, Splat-SLAM, PINGS, OpenGS-SLAM, and DLO+3DGS. Exact table extraction from the PDF text is noisy, so only unambiguous numbers are quoted below.
- Other candidates checked in this follow-up are not native multi-camera rigs: Photo-SLAM is mono/stereo/RGB-D; RTG-SLAM is RGB-D in the fetched README evidence; CoKo/MultiAgent Gaussian Splatting SLAM systems are multi-agent or independent-camera systems, not one calibrated robot rig.

## Evidence table

| System | Native camera rig evidence | Sensors | Online/real-time evidence | Benchmarks/numbers | Open-source status/license | Caveats | Source refs |
|---|---|---|---|---|---|---|---|
| **AgriGS-SLAM** | **Yes.** README says it uses **three synchronized RGB-D cameras**. Paper says the platform carries multiple cameras with complementary views and at each keyframe **all cameras are optimized jointly** against a single shared splat set; paper contribution claims first real-time 3DGS-SLAM framework supporting multi-camera setups in outdoor environments. Repo config exposes `enabled_cameras: ["cam_1", "cam_2", "cam_3"]`, per-camera intrinsics and extrinsics. Dataset uses `zed_multi/cam_1`, `cam_2`, `cam_3`. | Three ZED-style RGB-D cameras in demo data; paper figure text says three cameras: one horizontal and two vertical; 32-beam LiDAR; VIO-GNSS-RTK / FixPosition; Ouster OS0 32-channel in dataset card; LiDAR odometry and Scan Context loop closure. | Abstract and README claim real-time performance on-tractor. Paper contribution: real-time Visual-LiDAR 3DGS-SLAM with LiDAR odometry, loop closure, multimodal optimization, memory-aware incremental 3DGS. Source pipeline has keyframe queues, online Gaussian mapping between keyframes, per-keyframe optimization frequency stats, and viewer mode. | Paper evaluates apple and pear orchards across dormancy, flowering, harvesting; protocol includes clockwise training pass and counter-clockwise novel-view pass. Metrics: PSNR, SSIM, LPIPS, ATE. Baselines: Photo-SLAM, Splat-SLAM, PINGS, OpenGS-SLAM, DLO+3DGS. Table IV unambiguously reports multimodal-loss ablation averages: AgriGS-SLAM PSNR 26.7204, SSIM 0.8870, LPIPS 0.2177; Chamfer variant 25.9230/0.8626/0.2638; LOS 26.5652/0.8827/0.2290; Normals 25.8807/0.8544/0.2800; Raydrops 26.5247/0.8813/0.2292. | Public GitHub repo `AIRLab-POLIMI/agri-gs-slam`, Apache-2.0. GitHub metadata: public, default branch main, created 2025-10-30, updated 2026-05-15. README says entire implementation is open source; setup via Docker/script; demo dataset on Hugging Face is CC BY 4.0. | Domain-specific orchard/tractor implementation. README warns research code, not production-ready, hardware-specific assumptions, untested edge cases. Full multi-season dataset is listed as coming soon; only demo dataset verified. Paper limitations: sensitivity to LiDAR-camera calibration and reduced performance in sparse scenes; sensor delays/motion can cause cross-modal temporal discrepancies. Repo code uses nearest timestamp matching rather than a formal synchronization contract in the inspected dataloader. | [1]-[8] |
| Photo-SLAM | No native rig evidence. Supports monocular, stereo, RGB-D cameras; stereo is a fixed pair and not documented as a general synchronized multi-camera rig. | Mono/stereo/RGB-D; RealSense D455 example; ORB-SLAM3-derived tracking. | Title/README evidence says real-time simultaneous localization and photorealistic mapping. | Replica, TUM RGB-D, EuRoC in prior inventory; used as AgriGS-SLAM baseline. | Public GitHub; GPL-3.0 surfaced in repository evidence; license flags may be mixed/unknown in some fetched metadata. | Adaptable as stereo/RGB-D baseline, not native multi-camera rig. Heavy C++/CUDA/OpenCV/LibTorch stack. | [9] |
| RTG-SLAM | No native rig evidence in follow-up fetch. README evidence describes a single RGB-D camera workflow. | RGB-D camera; backend ORB-SLAM2 Python bindings for real data; accurate depth matters. | README says real-time large-scale 3D reconstruction; about 2x speed and half memory versus prior RGBD SLAM. | Replica/TUM/KITTI claims in prior report, but follow-up fetch only verified general RGB-D benchmarking claims. | Public GitHub; GPL-3.0. | Not multi-camera; RGB-D only in fetched evidence. Depth noise/invalid depth harms performance; single-process mode more stable. | [10] |
| MultiAgent-GaussianSplat-SLAM / similar independent-camera prototypes | No native single-rig evidence. README describes **multi-agent RGB-D Gaussian Splatting SLAM** with independent cameras/local submaps and global reconciliation. | RGB-D frames/depth/intrinsics; optional RGB-only depth prediction; optional masks. | Online-ish evidence: predicted depth cached during execution; shared online depth worker for multi-agent runs. | TUM RGB-D, Replica, Aria multi-agent setups mentioned in fetched evidence. | Public GitHub; MIT. | Multi-agent / independent cameras is not the same as one calibrated rigid multi-camera robot rig. Research prototype, not polished native multi-camera backend. | [11] |
| CoKo-SLAM / project_slam_coko | No native single-rig evidence in repository fetch. Framed as Compact Keyframe-Optimized Multi-Agent Gaussian Splatting SLAM. | No explicit camera rig or sensor suite in fetched README evidence; Replica/Aria evaluation clues only. | Repo has paper-backed PRDs/tasks and scaffolded Python+UV foundation; not enough evidence for finished native online rig implementation. | Replica and Aria evaluation mentioned. | Public GitHub; MIT. | Appears early-stage/scaffolded multi-agent module, not verified full native multi-camera robot-rig implementation. | [12] |
| Stereo 3DGS SLAM systems found by search, e.g. BGS-SLAM / Stereo-GS | No general rig evidence. Stereo/binocular systems are fixed two-camera modality, not a documented arbitrary multi-camera rig. | Stereo cameras; sometimes outdoor urban or online mapping. | Some claim online/real-time mapping from streaming stereo pairs. | Outdoor urban/stereo benchmarks depending on paper. | Paper/project status varies; not fully inspected because classification is stereo, not native multi-camera rig. | Treat as adaptable stereo baselines only unless a source documents general calibrated multi-camera rig ingestion. | [13] |

## AgriGS-SLAM primary-source evidence details

### Repository and metadata

- Repository: `https://github.com/AIRLab-POLIMI/agri-gs-slam`.
- GitHub metadata reports the repo as public, Apache-2.0, description: `[IEEE RA-L 2026] AgriGS-SLAM: Orchard Mapping Across Seasons via Multi-View Gaussian Splatting SLAM`, topics including `gaussian-splatting`, `slam`, `tractor`, and `agriculture`.
- Root contents verified by GitHub API: `LICENSE`, `README.md`, `config/`, `docker/`, `docs/`, `scripts/`, `src/`.
- README evidence extracted by WebFetch:
  - Uses **three synchronized RGB-D cameras**.
  - Combines direct LiDAR odometry and loop closures with multi-camera 3DGS rendering.
  - Tested on a tractor-mounted platform and claims real-time on-tractor.
  - Apache License 2.0.
  - Setup command: `./scripts/setup.sh`.
  - Run command inside container: `cd /agri_gs_slam/src && python3 pipeline.py --gs-slam`.
  - Modes: `--odom`, `--slam`, `--gs-odom`, `--gs-slam`; viewer via `--gs-viewer`.
  - Requirements: NVIDIA GPU, Docker + Docker Compose plugin, NVIDIA Container Toolkit; optional X11 for viewer.
  - Caveat: research code, not production-ready, possible untested edge cases and hardware-specific assumptions.

### License/build/run

- `LICENSE` is Apache License, Version 2.0.
- Repository license note includes research-software disclaimer: academic/research use, tested on specific hardware/field conditions, no warranty, not safety-critical or production deployment.
- Docker-first setup is visible in README and repository root (`docker/Dockerfile`, `docker/docker-compose.yml`, `scripts/setup.sh`).
- README says setup wizard checks Docker/Compose/NVIDIA runtime, creates `data/` and `results/`, builds image, starts container, compiles `src/odometry` and `src/scancontext`, downloads demo dataset, extracts/verifies PLY archives, and opens a shell.

### Dataset link and dataset evidence

- Demo dataset: `https://huggingface.co/datasets/foxmirko/agri-gs-slam-dataset-demo`.
- Hugging Face API metadata: public, not gated, last modified 2026-04-29, license tag `cc-by-4.0`, tags include `agriculture`, `slam`, `3d-reconstruction`, `lidar`, `multi-camera`, `orchard`, `gaussian-splatting`, `pose-estimation`, `visual-navigation`, `multi-view-geometry`.
- Dataset card extraction:
  - Preview/demo of larger orchard SLAM benchmark; full dataset coming soon.
  - Sensor suite: ZED X / ZED X Ultra multi-view cameras, Depth Anything v2, Ouster OS0 32-channel LiDAR, FixPosition GPS/RTK and dead-reckoning fusion.
  - Camera count: **3 cameras total**: `cam_1` front-left, `cam_2` front-center, `cam_3` front-right.
  - Structure includes `train/` and `val/`, per-camera RGB/depth/depth_anything/point_cloud directories under `zed_multi/cam_*`, Ouster point clouds, FixPosition odometry/GPS/twists, and ground-truth CSVs including `groundtruth_cam_*.csv` and `groundtruth_lidar.csv`.
  - Seasons/sites: dormancy, flowering, harvesting; apple and pear orchards; Fruit Research Center in Randwijk acknowledged.
  - Dataset viewer caveat: online HF viewer reports schema mismatch / `StreamingRowsError` / `CastError`.
  - Total file size reported by dataset card extraction: 2.21 GB.

### Multi-camera support evidence

- README says three synchronized RGB-D cameras.
- Repo config `config/default.yaml` evidence:
  - `enabled_cameras: ["cam_1", "cam_2", "cam_3"]`.
  - Per-camera entries for `cam_1`, `cam_2`, `cam_3`, each with 7-value extrinsic `[x, y, z, qx, qy, qz, qw]` and 4-value pinhole intrinsic `[fx, fy, cx, cy]`.
  - Separate LiDAR extrinsic is configured.
  - Loss toggles include RGB loss and LiDAR depth KL-divergence loss; depth supervision disabled by default in inspected config.
- Source `src/dataloader.py` evidence:
  - Initializes cameras from config and filters with `enabled_cameras`.
  - Rejects unknown camera IDs and empty camera selection.
  - Stacks camera intrinsics and robot-to-vision extrinsics across camera list.
  - Loads per-camera files from `zed_multi/{camera_id}/rgb`, `point_cloud`, and `depth_anything`.
  - Finds closest RGB/depth/point-cloud files by timestamp relative to pose timestamp.
  - Iterates over all camera IDs to process images/depths and projects LiDAR points into all cameras.
  - Returns tensors stacked across cameras: RGB images, camera depth tensors, LiDAR depth per camera, projected LiDAR normals, intrinsics, poses/extrinsics.
- Paper PDF text evidence:
  - Contribution: “first real-time 3DGS-SLAM framework supporting multi-camera setups in outdoor environments, enabled by a batch rasterization strategy.”
  - Method section: “We extend 3DGS to a synchronized multi-view setting to handle occlusions in orchards.”
  - “At each keyframe, all cameras are optimized jointly: their gradients update a single shared set of splats. Gaussians are not duplicated per camera; each splat lives once in the global …”
  - “For each camera b ∈ {1, …, B}, splats are projected into that camera via approximate rasterization.”
  - “Joint multi-view supervision lets all cameras refine the same map and the camera poses, improving consistency under dense foliage and repetitive row structure without per-camera splat copies.”
  - Figure 2 text: agricultural platform with three cameras, one horizontal and two vertical, a 32-beam LiDAR, and VIO-GNSS-RTK.

### Synchronization and calibration assumptions

- Strong synchronization evidence:
  - README says three synchronized RGB-D cameras.
  - Paper says synchronized multi-view setting and camera/LiDAR frames recorded simultaneously on the same unit.
  - Dataset filenames are timestamped, and the dataloader parses timestamps.
- Calibration evidence:
  - Per-camera extrinsics and intrinsics are in `config/default.yaml`.
  - LiDAR extrinsic is also in config.
  - Paper limitations explicitly mention sensitivity to LiDAR-camera calibration.
- Caveat:
  - Source dataloader uses nearest-file matching by timestamp for pose/camera/LiDAR files. This verifies a timestamp-association implementation, but not a formal hardware synchronization contract beyond README/paper statements.
  - Paper limitation says sensor delays and motion can still cause cross-modal temporal discrepancies; KL depth consistency alleviates but cannot fully remove them.

### Sensors and odometry involvement

- Visual: three RGB-D cameras with RGB and depth/depth_anything files in dataset.
- LiDAR: 32-beam LiDAR in paper figure; dataset card says Ouster OS0 32-channel; repo config has LiDAR extrinsic; dataloader loads Ouster point cloud files.
- Odometry/pose:
  - Paper: Direct LiDAR Odometry (DLO) scan-to-submap frontend; GICP; second-order motion prior for tractor motion and LiDAR deskewing; iSAM2 factor graph backend; loop closures via pose-space KD-tree and Scan Context descriptors verified with GICP.
  - Dataset card: FixPosition GPS/RTK and dead-reckoning fusion; groundtruth pose files for camera and LiDAR.
  - Source `src/grapher.py` evidence in grep output: GTSAM ISAM2-based LiDAR SLAM, DLO alignment, Scan Context loop candidates, loop closure factor optimization.

### Online / real-time claims

- Abstract: real-time 3D scene understanding; maintains real-time performance on-tractor.
- README: run real-time on-tractor.
- Paper contribution: real-time Visual-LiDAR 3DGS-SLAM with LiDAR odometry, loop closure, multimodal optimization, memory-aware incremental 3DGS.
- Method evidence:
  - Gaussian map updated online between keyframes.
  - Active-set GPU memory policy to sustain real-time operation while retaining complete map for loop closures.
  - Pipeline executes gradient-driven map lifecycle between keyframes.
- Caveat:
  - Conclusion includes future work to incorporate inertial cues for tighter motion priors and full on-tractor deployment, while elsewhere claiming real-time on-tractor. This wording should be treated as a nuance: demonstrated/claimed real-time tractor performance is source-supported, but “full on-tractor deployment” may refer to additional robustness/inertial integration.

### Benchmarks and reported numbers

Benchmark design evidence:

- Sites/classes: apple orchard and pear orchard.
- Seasons/phenological stages: dormancy, flowering, harvesting.
- Protocol: standardized trajectory template; one clockwise pass for training and one counter-clockwise pass for validation/novel view; evaluates both training-view and novel-view synthesis to reduce 3DGS overfitting.
- Metrics: PSNR, SSIM, LPIPS for rendering; ATE in meters for trajectory error.
- Baselines: Photo-SLAM, Splat-SLAM, PINGS, OpenGS-SLAM, and DLO+3DGS.
- Ablations: localization via LiDAR supervision, mapping/training schedule, multi-camera views, multimodal loss variants.

Reported numbers that were cleanly extractable:

- Table IV multimodal-loss averages:
  - AgriGS-SLAM: PSNR 26.7204, SSIM 0.8870, LPIPS 0.2177.
  - AgriGS-SLAM w/ Chamfer: PSNR 25.9230, SSIM 0.8626, LPIPS 0.2638.
  - AgriGS-SLAM w/ LOS: PSNR 26.5652, SSIM 0.8827, LPIPS 0.2290.
  - AgriGS-SLAM w/ Normals: PSNR 25.8807, SSIM 0.8544, LPIPS 0.2800.
  - AgriGS-SLAM w/ Raydrops: PSNR 26.5247, SSIM 0.8813, LPIPS 0.2292.
- Table II exact rows are visually present in the paper, but plain-text extraction from PDF is column-scrambled; avoid quoting table-wide exact numbers without manual visual table parsing from the PDF.
- Paper narrative findings:
  - AgriGS-SLAM outperforms state of the art across both orchard scenarios.
  - Performance is weaker in dormancy due to sparse trunks/branches; stronger in harvesting and flowering.
  - Multi-camera setups generally improve localization accuracy/ATE: two cameras outperform one and three outperform two, with one exception in apple harvesting where DLO+3DGS marginally performs better.
  - Adding views sharpens reconstructed geometry and reduces drift on training trajectories, but can degrade novel-view synthesis by overfitting.
  - Splat-SLAM diverged on one sequence, pear dormancy, even after tuning; AgriGS-SLAM completed all sequences according to the narrative.
  - PINGS performed worst overall despite LiDAR-based/outdoor design, according to the paper narrative.

## Search for other true native multi-camera robot-rig systems

### Search methods used

- GitHub repository search for AgriGS-SLAM and code search for `AgriGS-SLAM`.
- GitHub code/repository searches for exact phrases: `multi-camera 3D Gaussian Splatting SLAM`, `multi-camera 3DGS-SLAM`, `multi-view 3DGS-SLAM camera`.
- WebSearch attempts for multi-camera / multi-view Gaussian Splatting SLAM queries failed due provider/anti-bot errors; follow-up used GitHub, arXiv pages, Semantic Scholar snippets, prior local research artifacts, and primary README/project pages.
- Crossref query verified IEEE RA-L publication metadata and DOI.
- Follow-up primary inspections included Photo-SLAM, RTG-SLAM, MultiAgent-GaussianSplat-SLAM, and CoKo/project_slam_coko because prior reports flagged them as possible confounders.

### Findings

- **No other true native multi-camera robot-rig 3DGS SLAM implementation was verified in this pass.**
- **Stereo systems** exist and are relevant as adaptable baselines, but they are not equivalent to general calibrated multi-camera rigs.
- **RGB-D systems** use one RGB-D stream, not multiple robot-mounted cameras.
- **LiDAR-inertial-camera systems** are robotics-relevant and may have hardware synchronization, but inspected summaries describe one camera plus LiDAR/IMU unless otherwise documented.
- **Multi-agent Gaussian SLAM systems** use multiple independent agents/cameras/maps, not a rigid calibrated camera rig on one robot.

## Repository-only / paper-only / unverified flags

- AgriGS-SLAM three-camera support: **repository + README + dataset + paper verified**.
- AgriGS-SLAM exact camera arrangement: **paper figure/caption + dataset card verified**; detailed hardware image/project page content was not visible through WebFetch beyond title/date.
- AgriGS-SLAM full multi-season dataset: **announced, unverified/not yet public**; only demo dataset verified.
- AgriGS-SLAM paper benchmark table exact per-sequence numbers: **paper-only and visually/table-level; not reliably extracted from plain text** except Table IV.
- AgriGS-SLAM real-time on-tractor: **README + abstract/paper claim verified**, but independent runtime reproduction not performed.
- AgriGS-SLAM synchronization: **README/paper claim verified**; code-level association uses nearest timestamp matching, so exact hardware sync behavior remains source-claimed rather than independently validated.
- Photo-SLAM/RTG-SLAM native multi-camera: **not verified; evidence points to mono/stereo/RGB-D or RGB-D only**.
- Multi-agent candidates native rig support: **not verified; evidence points away from rigid robot-rig support**.

## Final verdict

**AgriGS-SLAM should be classified as native multi-camera for the purposes of the current Mosaic research question.**

Rationale: It has convergent primary-source evidence from the paper, repository README, repository config/source, and dataset card for a synchronized three-RGB-D-camera, tractor-mounted, Visual-LiDAR online 3DGS SLAM system. It is not merely stereo, not merely RGB-D, and not merely temporally accumulated multi-view frames. It models multiple named cameras with calibrated intrinsics/extrinsics, ingests per-camera RGB/depth/point-cloud data, jointly optimizes all camera views against one shared Gaussian map, and uses LiDAR odometry/loop closure in a robot-mounted orchard deployment.

Classification nuance: **native but domain-specific**, not yet proven as a general-purpose arbitrary-rig backend. Treat it as the strongest native multi-camera evidence and as an isolated backend candidate, with caveats around research-code maturity, calibration/timing sensitivity, full dataset availability, and reproducibility of real-time on-tractor claims.

## Numbered sources

1. AgriGS-SLAM GitHub repository: https://github.com/AIRLab-POLIMI/agri-gs-slam
2. AgriGS-SLAM raw README: https://raw.githubusercontent.com/AIRLab-POLIMI/agri-gs-slam/main/README.md
3. AgriGS-SLAM license: https://raw.githubusercontent.com/AIRLab-POLIMI/agri-gs-slam/main/LICENSE
4. AgriGS-SLAM arXiv abstract: https://arxiv.org/abs/2510.26358
5. AgriGS-SLAM arXiv PDF: https://arxiv.org/pdf/2510.26358
6. AgriGS-SLAM IEEE DOI: https://doi.org/10.1109/LRA.2026.3685453
7. AgriGS-SLAM IEEE Xplore landing page: https://ieeexplore.ieee.org/document/11487946/
8. AgriGS-SLAM demo dataset: https://huggingface.co/datasets/foxmirko/agri-gs-slam-dataset-demo
9. Photo-SLAM repository: https://github.com/HuajianUP/Photo-SLAM
10. RTG-SLAM repository: https://github.com/MisEty/RTG-SLAM
11. MultiAgent-GaussianSplat-SLAM repository: https://github.com/Elonian/MultiAgent-GauassianSplat-SLAM
12. CoKo/project_slam_coko repository: https://github.com/RobotFlow-Labs/project_slam_coko
13. Semantic Scholar search snippets for stereo 3DGS SLAM systems including BGS-SLAM/Stereo-GS: https://www.semanticscholar.org/search?q=3D%20Gaussian%20Splatting%20SLAM%20stereo
