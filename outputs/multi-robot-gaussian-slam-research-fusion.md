# Multi-Robot / Multi-Agent Gaussian SLAM Fusion Architecture Research

## 1. Short executive summary

The current literature has only a small number of true multi-robot or multi-agent Gaussian Splatting SLAM systems. The strongest target-class matches are HAMMER, GRAND-SLAM, MAGS-SLAM, and Compact Keyframe-Optimized Multi-Agent Gaussian Splatting SLAM. These systems explicitly address multiple moving agents/robots and a shared Gaussian or Gaussian-like map, but they choose different fusion contracts:

- HAMMER is server-based, heterogeneous, online, metric-semantic 3DGS mapping from asynchronous robot data streams, with explicit global frame alignment and no prior relative robot poses.
- GRAND-SLAM is centralized multi-agent RGB-D Gaussian SLAM; agents exchange/merge 3D Gaussian maps and use centralized loop closure with rendered-depth or camera-depth alignment.
- MAGS-SLAM is monocular RGB-only multi-agent Gaussian SLAM; agents maintain local Gaussian submaps and communicate compact submap summaries for occupancy-aware Gaussian fusion and cross-agent loop verification.
- Compact Keyframe-Optimized Multi-Agent Gaussian Splatting SLAM is RGB-D multi-agent SLAM with centralized merging/optimization, compact Gaussian-map exchange, and loop closure without an initial guess.

Adjacent single-robot systems are important because they define reusable modality and fusion patterns, but they are not target-class multi-robot shared-map fusion. GSFusion, SplaTAM, MonoGS, GS-SLAM, Photo-SLAM, GS-LIVO, LiV-GS, LVI-GS, LIVE-GS, RMGS-SLAM, LVD-GS, and AgriGS-SLAM are best classified as single-agent online mapping/SLAM, multi-sensor fusion, multi-camera rig, or large-scale online reconstruction systems unless a multi-agent collaboration layer is explicit.

## 2. Architecture classification table

| System | Target-class verdict | Input modality | Agent motion model | Fusion timing | Fusion location | Fusion unit | Shared-map semantics | Pose/depth assumptions | Loop closure/global alignment | Confidence |
|---|---|---|---|---|---|---|---|---|---|---|
| HAMMER: Heterogeneous, Multi-Robot Semantic Gaussian Splatting | True target-class: heterogeneous multi-robot semantic Gaussian mapping | Asynchronous robot data streams; local SLAM poses plus image data; mixed perception modes; heterogeneous devices | Multiple robots/devices with local on-device SLAM pose estimates; exact platform kinematics not specified | Online, streaming | Server-based/client-server via ROS-style communication infrastructure | Streaming robot observations and local poses; server trains semantic 3DGS map | Shared 3D metric-semantic Gaussian scene with CLIP/open-vocabulary semantic codes | No prior initial robot positions and no prior relative pose knowledge; depends on local SLAM pose estimates; depth modality not clearly specified in abstract/page text | Frame-alignment module maps local robot trajectories/data into a global frame; loop closure not emphasized in extracted text | High for multi-robot/server/global-frame claims; medium for modality details |
| GRAND-SLAM: Local Optimization for Globally Consistent Large-Scale Multi-Agent Gaussian SLAM | True target-class: multi-agent Gaussian SLAM | RGB-D visual SLAM | Multiple agents/robots, motion model not specified in abstract | Incremental/online SLAM implied | Collaborative architecture; exact deployment not fully specified in abstract; local optimization over submaps plus global pose graph | Submaps and pose graph constraints | Collaborative 3D Gaussian scene representation / shared reconstruction | RGB-D input; no extra pose/depth assumptions stated in abstract | Inter- and intra-robot loop closure in a pose-graph optimization framework for global consistency | High for RGB-D, multi-agent, loop closure; medium for fusion location/unit specifics |
| MAGS-SLAM: Monocular Multi-Agent Gaussian Splatting SLAM | True target-class: multi-agent Gaussian SLAM | RGB-only monocular | Multiple independent monocular agents; motion model not otherwise specified | Incremental collaborative SLAM | Collaboration layer; page text does not state centralized vs decentralized explicitly | Local monocular Gaussian submaps and compact submap summaries; occupancy-aware Gaussian fusion | Shared Gaussian submap structure rather than raw-frame or dense-map exchange | Designed for monocular scale ambiguity; no active depth sensors | Geometry- and appearance-aware loop verification for cross-agent alignment/coherent global reconstruction | High for monocular multi-agent/submap summary claims; medium for deployment location |
| Compact Keyframe-Optimized Multi-Agent Gaussian Splatting SLAM | True target-class: multi-agent Gaussian SLAM/map fusion | RGB-D | Multiple RGB-D agents; motion model not specified | Incremental/online implied by SLAM; centralized merging and optimization | Centralized server | 3D Gaussian maps, compacted Gaussians, keyframes/depth variants | Shared 3D Gaussian maps exchanged by agents; compaction removes redundant Gaussians while preserving render quality | RGB-D. Loop closure without initial guess. Pure rendered-depth mode needs only Gaussians; camera-depth mode adds lightweight depth images for better registration/pruning | Centralized loop closure with rendered-depth-only or camera-depth-assisted alignment | High for centralized/RGB-D/Gaussian exchange; medium for timing |
| A Survey on Collaborative SLAM with 3D Gaussian Splatting | Survey/secondary evidence, not a system | Survey spans heterogeneous sources, not one modality | Multi-robot collaborative SLAM category | N/A | Taxonomy includes centralized and distributed | N/A: survey categories include communication-efficient fusion, semantic distillation, pose optimization, map alignment | Collaborative Gaussian representation and multi-agent consistency/alignment | N/A | Identifies pose optimization and map alignment as key issues | High as taxonomy evidence; not a primary system |
| GSFusion: Online RGB-D Mapping Where Gaussian Splatting Meets TSDF Fusion | Adjacent: single-agent online RGB-D Gaussian/TSDF fusion, not multi-robot | RGB-D | Single moving camera/drone; external pose source for some data | Online | On-device/local mapper | Depth into octree TSDF; RGB/quadtree seeding of Gaussians; keyframe set | Compact 3D Gaussian map plus volumetric TSDF map | Requires RGB-D. Camera poses assumed from dataset/external estimator; drone data uses OKVIS2 | No multi-agent loop closure; focuses online fusion and map quality | High |
| SplaTAM | Adjacent: single-agent dense RGB-D Gaussian SLAM | RGB-D | Single unposed RGB-D camera | Online tracking and mapping | Local | Adds/optimizes Gaussians from RGB-D frames; silhouette mask/map expansion | Explicit volumetric/dense map with 3D Gaussians | Unknown camera pose estimated online; depth from RGB-D | No multi-robot loop closure in page evidence | High |
| MonoGS | Adjacent: single-agent monocular/RGB-D Gaussian SLAM | Monocular main case; RGB-D supported with external depth | Single moving camera | Online, live ~3 fps in page evidence | Local | Incremental dense Gaussian reconstruction; direct tracking against Gaussians | 3D Gaussians only as scene model | Does not require accurate offline SfM poses; monocular no depth, optional RGB-D depth | No multi-robot loop closure in page evidence | High |
| GS-SLAM | Adjacent: single-agent RGB-D dense Gaussian SLAM | RGB-D | Single unposed RGB-D camera | Online | Local | Tracking/mapping loop, map expansion by adding Gaussians | 3D Gaussian dense map | RGB-D depth; pose initially unknown and estimated | No multi-robot loop closure in page evidence | High |
| Photo-SLAM | Adjacent: single-agent visual SLAM with Gaussian/feature map; supports stereo/multi-camera modalities but not multi-robot | Monocular, stereo, RGB-D | Single camera/rig motion | Online real-time | Local | ORB/factor-graph tracking plus neural photorealistic Gaussian-map optimization | Hyper-primitives map: point-cloud primitives linked with ORB features, pose/appearance attributes, SH coefficients | Uses geometric features; depth optional depending on modality | SLAM-level consistency, but no multi-robot shared-map fusion in page evidence | Medium-high |
| GS-LIVO | Adjacent: single-agent LiDAR-inertial-visual Gaussian mapping | LiDAR + IMU + camera | Single platform with tightly coupled odometry | Online real-time | Local/onboard | IESKF state estimation; local sliding-window Gaussians; image-driven map optimization | Global Gaussian map with local sliding-window and octree/voxel indexing | Pose estimated by IESKF; geometry/depth from LiDAR, images for rendering optimization | Loop closure not mentioned in abstract evidence | High |
| LiV-GS | Adjacent: single-agent laser-camera Gaussian SLAM | LiDAR/laser + camera | Single platform | Online SLAM implied | Local | Point-cloud-to-Gaussian alignment; shared covariance attributes; conditional Gaussian updates beyond LiDAR view | 3D Gaussian differentiable spatial representation | Sparse LiDAR aligned to continuous Gaussian map; no special pose prior stated | Loop closure not described in evidence | Medium-high |
| LVI-GS | Adjacent: single-agent LiDAR-visual-inertial Gaussian SLAM | LiDAR + visual + inertial | Single platform | Online | Local | Tight coupling of 3DGS with LiDAR surfels; global geometric optimization | Hybrid 3DGS plus LiDAR surfel map | Depth-invariant Gaussian initialization and bounded sigmoid constraint for sparse inputs | Globally consistent mapping/global optimization; loop closure not explicitly described | High |
| LIVE-GS | Adjacent: single-agent LiDAR-visual-inertial real-time Gaussian mapping | LiDAR + camera + IMU | Single platform | Real-time/online | Local | Colorized LiDAR points initialize Gaussians; differentiable rendering; pyramid training; expansion/keyframe logic | 3D Gaussian map | LiDAR-derived depth loss; no special pose prior stated | Loop closure not mentioned in extracted evidence | High |
| RMGS-SLAM | Adjacent but architecturally relevant: single-robot multi-sensor 3DGS SLAM with Gaussian-map loop closure | LiDAR + IMU + camera | Single robot | Real-time/online | Local/onboard | Parallel state estimation and Gaussian primitive initialization; global Gaussian optimization | Global Gaussian map | Real-time pose estimation from LiDAR-camera-IMU plus voxel PCA priors | Loop closure directly on optimized global Gaussian map using Gaussian-based GICP and pose-graph optimization | High |
| LVD-GS | Adjacent: single-agent LiDAR-camera dynamic-scene Gaussian SLAM | LiDAR + camera | Single platform | SLAM/online implied, exact timing not specified in extracted text | Local | Hierarchical collaborative representation module and joint dynamic modeling module | 3DGS representation with dynamic masks | Aims to reduce scale ambiguity and pose drift; DINO-Depth features guide depth uncertainty | Loop closure not described in extracted evidence | Medium |
| AgriGS-SLAM | Adjacent: single-robot on-tractor multi-camera Visual-LiDAR Gaussian SLAM | Multi-camera + LiDAR | Single agricultural robot/tractor | Online/real-time on-tractor | Local/onboard | Batch rasterization across complementary viewpoints; keyframe-to-keyframe map lifecycle updates | 3DGS map with unified gradient-driven lifecycle | Direct LiDAR odometry plus probabilistic LiDAR-based depth consistency for pose refinement | Direct LiDAR odometry coupled with loop closures | High |

## 3. Diagram-friendly taxonomy of architecture patterns found

```text
Multi-robot / multi-agent Gaussian SLAM architectures

A. Central server shared Gaussian map
   A1. Robot clients stream observations + local poses
       - Server aligns local frames into a global frame
       - Server trains/updates a shared Gaussian or metric-semantic Gaussian map
       - Example: HAMMER
   A2. Robot clients exchange/upload Gaussian maps or compacted Gaussian state
       - Server performs map merging, compaction, loop closure, and global optimization
       - Examples: Compact Keyframe-Optimized Multi-Agent Gaussian Splatting SLAM, likely GRAND-SLAM in its global optimization layer

B. Submap-centric collaborative Gaussian SLAM
   B1. Each agent maintains local Gaussian submaps
       - Collaboration exchanges compact submap summaries, not raw frames
       - Cross-agent loop verification aligns local maps
       - Example: MAGS-SLAM
   B2. Local submap optimization plus global pose graph
       - Inter- and intra-robot loop closures feed pose-graph optimization
       - Example: GRAND-SLAM

C. Distributed / communication-efficient collaborative 3DGS category
   - Identified as a survey-level category, but fewer concrete public system details were available in the sources checked.
   - Expected fusion units: compact Gaussians, keyframes, submaps, descriptors, or gradients.
   - Key risks: duplicate Gaussians, inconsistent scale, stale local frames, map-frame drift, and bandwidth pressure.

Adjacent single-agent patterns that can be reused but are not multi-robot by themselves

D. Online RGB-D Gaussian mapping
   - RGB-D frames + estimated/known poses -> Gaussians, sometimes TSDF hybrid
   - Examples: SplaTAM, GS-SLAM, GSFusion

E. Monocular/stereo visual Gaussian SLAM
   - Direct rendering or feature-based tracking against Gaussian map
   - Must handle scale ambiguity for monocular input
   - Examples: MonoGS, Photo-SLAM

F. LiDAR-visual-inertial Gaussian mapping
   - LiDAR supplies metric geometry/depth; camera supplies color/photometric optimization; IMU stabilizes state estimation
   - Examples: GS-LIVO, LVI-GS, LIVE-GS, LiV-GS, RMGS-SLAM

G. Multi-camera rig Gaussian SLAM
   - Multiple cameras on one rigid robot are fused into one local map
   - This is multi-view/multi-camera, not multi-robot shared mapping
   - Example: AgriGS-SLAM
```

## 4. Boundary notes: true shared Gaussian-map fusion vs adjacent concepts

### True multi-robot shared Gaussian-map fusion

A system should count as target-class when all of the following are present:

1. Multiple independently moving agents/robots/devices.
2. Online or incremental collaboration, not only post-hoc reconstruction.
3. A shared Gaussian or Gaussian-like map/state, or explicit map-level Gaussian fusion.
4. A pose/alignment mechanism across agents, such as frame alignment, cross-agent loop closure, or pose-graph optimization.

By this standard, HAMMER, GRAND-SLAM, MAGS-SLAM, and Compact Keyframe-Optimized Multi-Agent Gaussian Splatting SLAM are target-class matches.

### Multi-camera rigs are not multi-robot collaboration

A multi-camera rig can have many viewpoints, but the cameras share one rigid body transform tree and one robot trajectory. AgriGS-SLAM is architecturally useful because it fuses complementary viewpoints and LiDAR in a Gaussian map, but it is not a multi-robot shared-map system from the evidence checked.

### Stereo is not multi-agent

Stereo systems use two synchronized cameras with fixed extrinsics to recover depth. Photo-SLAM supports stereo, but stereo fusion is a sensor geometry problem, not distributed shared-map fusion.

### Multi-session is not automatically multi-robot

A system can align multiple sessions or trajectories from the same device and still not support concurrent robot collaboration. Multi-session/global alignment evidence should be kept separate unless the paper explicitly says multiple agents/robots and describes collaboration or shared-map fusion.

### Static multi-view reconstruction is not SLAM

Offline 3DGS reconstruction from posed image collections can yield high-quality Gaussian maps, but it does not solve online tracking, incremental map updates, inter-robot frame alignment, or communication constraints. It is adjacent evidence for representation quality, not for multi-robot SLAM architecture.

### Offline reconstruction is not online shared-map fusion

Some Gaussian Splatting systems optimize a final scene after data collection. These do not provide the online fusion timing, bounded update units, or shared-map consistency contracts needed for multi-robot SLAM. They should be cited only as representation baselines or back-end reconstruction options.

## 5. Numbered source list with direct URLs

1. HAMMER: Heterogeneous, Multi-Robot Semantic Gaussian Splatting. https://arxiv.org/abs/2501.14147
2. IEEE page for HAMMER. https://ieeexplore.ieee.org/document/11018364
3. GRAND-SLAM: Local Optimization for Globally Consistent Large-Scale Multi-Agent Gaussian SLAM. https://arxiv.org/abs/2506.18885
4. MAGS-SLAM: Monocular Multi-Agent Gaussian Splatting SLAM for Geometrically and Photometrically Consistent Reconstruction. https://arxiv.org/abs/2605.10760
5. Compact Keyframe-Optimized Multi-Agent Gaussian Splatting SLAM. https://arxiv.org/abs/2604.00804
6. A Survey on Collaborative SLAM with 3D Gaussian Splatting. https://arxiv.org/abs/2510.23988
7. GSFusion project page: Online RGB-D Mapping Where Gaussian Splatting Meets TSDF Fusion. https://gs-fusion.github.io/
8. GSFusion GitHub repository. https://github.com/ethz-mrl/GSFusion
9. SplaTAM project page. https://spla-tam.github.io/
10. MonoGS project page: Gaussian Splatting SLAM. https://rmurai.co.uk/projects/GaussianSplattingSLAM/
11. GS-SLAM project page. https://shingyukong.github.io/GS-SLAM/
12. Photo-SLAM project page. https://huajianup.github.io/research/Photo-SLAM/
13. GS-LIVO: Real-Time LiDAR, Inertial, and Visual Multi-sensor Fused Odometry with Gaussian Mapping. https://arxiv.org/abs/2501.08672
14. LiV-GS: LiDAR-Vision Integration for 3D Gaussian Splatting SLAM in Outdoor Environments. https://arxiv.org/abs/2411.12185
15. LVI-GS: Tightly Coupled LiDAR-Visual-Inertial SLAM with 3D Gaussian Splatting. https://arxiv.org/abs/2411.02703
16. LIVE-GS: Online LiDAR-Inertial-Visual State Estimation and Mapping with 3D Gaussian Splatting. https://arxiv.org/abs/2507.23273
17. RMGS-SLAM: Real-Time Multi-Sensor 3D Gaussian Splatting SLAM for Large-Scale Scenes. https://arxiv.org/abs/2604.12942
18. LVD-GS: Gaussian Splatting SLAM for Dynamic Scenes with Hierarchical Explicit/Implicit Collaboration. https://arxiv.org/abs/2510.22669
19. AgriGS-SLAM: Multi-view 3D Gaussian Splatting SLAM for Orchard Mapping Across Seasons. https://arxiv.org/abs/2510.26358
