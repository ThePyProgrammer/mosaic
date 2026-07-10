# Open-source online / incremental 3D Gaussian Splatting SLAM code inventory

Researcher: R2  
Date: 2026-05-18  
Scope: open-source or visibly public repositories for online/incremental 3D Gaussian Splatting SLAM, Gaussian Splatting mapping, or close variants relevant to moving-camera robotic mapping. This is evidence for a lead synthesis, not a final recommendation.

## Executive notes for lead

- The strongest directly inspectable baselines are SplaTAM, MonoGS, Gaussian-SLAM, Photo-SLAM, RTG-SLAM, SEGS-SLAM, DiskChunGS, Gaussian-LIC, VINGS-Mono, WildGS-SLAM, OpenGS-SLAM, LSG-SLAM, HI-SLAM2, and GSORB-SLAM.
- Most systems are single moving-camera sequence SLAM, not native simultaneous multi-camera rig SLAM. Multi-camera evidence is usually modality support (mono/stereo/RGB-D), dataset support (EuRoC/Waymo), ROS topics, or LiDAR-camera fusion rather than calibrated multi-view robot rigs.
- For Mosaic backend exploration, the cleanest license surfaces appear to be BSD/MIT/Apache repositories, but several attractive real-time systems are GPL or have mixed/unclear third-party licenses.
- Benchmark coverage clusters around Replica, TUM RGB-D, ScanNet/ScanNet++, EuRoC, KITTI/KITTI360, Waymo, Bonn Dynamic RGB-D, and custom large-scene datasets. Robotics-oriented datasets appear in Gaussian-LIC, VINGS-Mono, DiskChunGS, OpenGS-SLAM, and AgriGS-SLAM.

## Evidence table

| Repository/System | Official? | License | Language/dependencies | Input modality/datasets | Online pipeline? | Multi-camera support evidence | Maintenance notes | Source refs |
|---|---:|---|---|---|---|---|---|---|
| SplaTAM: Splat, Track & Map 3D Gaussians for Dense RGB-D SLAM | Yes; project/repo from authors | BSD-3-Clause per GitHub metadata | Python; README reports Python 3.10, Torch 1.12.1, CUDA 11.6; conda/pip, Docker and Singularity paths | RGB-D; Replica, TUM-RGBD, ScanNet, ScanNet++, Replica-V2; online demo via NeRFCapture/iPhone/LiDAR Apple devices | Yes; online demo script and offline record-then-run path | No native multi-camera rig evidence; RGB-D single-camera datasets and phone capture | 2.1k stars; updated 2026-05-15; release SplaTAM V1 from Dec 2023; README promises faster variant | [1], [2] |
| MonoGS / Gaussian Splatting SLAM | Yes; CVPR 2024 Highlight / Best Demo repo | GitHub reports Other/unknown license via LICENSE.md | Mostly Python with GLSL/shell; conda `environment.yml`; tested Ubuntu 20.04/18.04, PyTorch 1.12.1, CUDA 11.6/11.3; pyrealsense2 for live | Monocular core; also RGB-D and experimental stereo; TUM-RGBD, Replica, EuRoC, live RealSense D455 | Yes; dense online SLAM with GUI; `--eval` headless mode | Stereo config and live RealSense support; not evidence of simultaneous multi-camera rig | 2.0k stars; updated 2026-05-18; dev.speedup branch claims up to 10 FPS on RTX 4090/i9-12900K | [3], [4] |
| Gaussian-SLAM: Photo-realistic Dense SLAM with Gaussian Splatting | Yes | MIT | Mostly Python; conda `environment.yml`; Git LFS; tested RTX 3090/A6000 on Ubuntu 22/CentOS 7.5; headless Open3D for depth_L1 eval | Tested on Replica, TUM_RGBD, ScanNet, ScanNet++; run per scene with `run_slam.py` | Unclear from README; SLAM pipeline but online/offline not explicit | No native multi-camera evidence; benchmark sequence input | 1.1k stars; updated 2026-05-18; 7 commits; no releases; metrics averaged over seeds due nondeterministic rasterizer | [5], [6] |
| Photo-SLAM | Yes; CVPR 2024 official | GPL-3.0; WebFetch noted unknown license flag too | Mostly C++/C/CUDA; Eigen, Boost, JsonCpp, OpenGL/GLFW/GLM, CUDA, OpenCV with contrib+CUDA, LibTorch; build script | Monocular, stereo, RGB-D; Replica, TUM RGB-D, EuRoC; RealSense D455 example | Yes; real-time SLAM | Strong modality breadth: mono/stereo/RGB-D; RealSense example; not a generalized multi-camera rig API | 732 stars; updated 2026-05-08; 7 commits, 37 issues, 1 PR, no releases; evaluation toolkit separate | [7], [8], [9] |
| RTG-SLAM: Real-time 3D Reconstruction at Scale Using Gaussian Splatting | Yes | GPL-3.0 | Python-heavy; Python 3.9, CUDA 11.7, PyTorch 1.13.1; conda env; ORB-SLAM2/Pangolin/OpenCV/boost-python via build script | RGB-D; Replica, TUM-RGBD, ScanNet++, “Ours”; accurate depth assumed for ICP front-end | Yes; online/real-time, on-the-fly Gaussian optimization; single-process and multi-process modes | No multi-camera rig; RGB-D camera assumption | 492 stars; updated 2026-05-14; troubleshooting notes for Pangolin/SIGSEGV; points to GPS-SLAM follow-up | [10], [11] |
| GS-SLAM: Dense Visual SLAM with 3D Gaussian Splatting | Project page official; full code repo not found, only modified rasterizer visible | Website CC-BY-SA; code license unknown; modified rasterizer repo no GitHub license visible in search output | Modified diff-gaussian-rasterization-for-gsslam visible; full implementation not publicly visible via gs-slam GitHub page | RGB-D; Replica, TUM-RGBD; tracking and rendering benchmarks | Paper/system is SLAM; public implementation availability appears incomplete | No multi-camera evidence | Project GitHub user shows only website; modified rasterizer repo active and popular | [12], [13], [14] |
| SEGS-SLAM: Structure-enhanced 3D Gaussian Splatting SLAM with Appearance Embedding | Yes; repo says official ICCV 2025 code | GPL-3.0; unknown license flag also noted | Mostly C++ with CUDA/C; submodules; Ubuntu deps plus Python eval env, PyTorch 2.3.1 + CUDA 12.1; rasterizer editable install | RGB-D and monocular workflows; Replica, TUM RGB-D, VECtor; live RealSense D455 example | Yes; real-time SLAM with viewer disable path | Monocular and RGB-D plus RealSense; not simultaneous multi-camera rig | 205 stars; updated 2026-05-04; 17 commits; no releases; evaluation runs each sequence five times | [15], [16] |
| DiskChunGS: Large-Scale 3D Gaussian SLAM Through Efficient Disk Chunking | Yes; leggedrobotics RA-L 2026 repo | WebFetch says GPL-3.0 plus Inria non-commercial research license for third_party/gaussian_splatting; GitHub metadata reports Other | Mostly C++/C/CUDA/Python/Shell/CMake/Docker; Docker-first; ORB-SLAM3 + 3DGS; CUDA/OpenCV/LibTorch/TorchScatter; optional RealSense SDK | Mono, stereo, RGB-D; Replica, TUM RGB-D, EuRoC, ScanNet; KITTI in paper/README evidence; ROS wrapper topics | Yes; online SLAM with ORB-SLAM3 tracking/loop closure and out-of-core chunks | Strongest multi-input/robotics evidence: mono/stereo/RGB-D, ROS image/stereo/depth topics, external TF mode; still not a typed multi-rig library | 12 stars; updated 2026-05-07; active but young; TODOs include cleaner code, viewer, RealSense support/testing; Jetson notes | [17], [18] |
| Gaussian-LIC: Real-Time Photo-Realistic SLAM with Gaussian Splatting and LiDAR-Inertial-Camera Fusion | Yes; ICRA 2025 repo | No GitHub license visible | C++/CUDA/Python; Ubuntu 20.04, RTX 3090/4090, CUDA 11.7, cuDNN, OpenCV CUDA, LibTorch, TensorRT, Coco-LIC and Livox ROS driver | LiDAR + inertial + camera; FAST-LIVO, FAST-LIVO2, R3LIVE, MCD, M2DGR | Yes; real-time online pose estimation and map construction | Sensor fusion across LiDAR, IMU, camera; not multi-camera only, but robotics-relevant multi-sensor | 537 stars; updated 2026-05-13; roadmap items include Dockerfile, meshing, optimized Coco-LIC, Gaussian-LIC2 | [19], [20] |
| VINGS-Mono: Visual Inertial Gaussian Splatting Monocular SLAM in Large Scenes | Yes; TRO 2025 source code | No GitHub license visible | Python; Python 3.9.19, CUDA 11.8; recursive clone; environment.yaml; `set_env.sh`; GTSAM branch guidance; pretrained weights | Monocular visual-inertial; Hierarchical 3DGS demo, RTG-SLAM Hotel, Waymo, KITTI, KITTI360; mobile app/GPU server path | Yes; presented as runtime SLAM with large-scene scripts and mobile app | Camera + inertial; no simultaneous multi-camera rig evidence | 283 stars; updated 2026-05-17; authors provide contact emails; setup may take about an hour | [21], [22] |
| WildGS-SLAM: Monocular Gaussian Splatting SLAM in Dynamic Environments | Yes; CVPR 2025 repo | Apache-2.0 | Python with CUDA/C++; Python 3.10, CUDA 11.8, PyTorch 2.1.0, xformers, torch-scatter, mmcv-full; custom rasterization and lietorch | Monocular videos; Wild-SLAM Mocap/iPhone, Bonn Dynamic, TUM RGB-D dynamic, custom data | Yes; tracks camera and builds static 3D Gaussian map while suppressing dynamic objects | Explicitly one camera; no multi-camera support | 608 stars; updated 2026-05-13; 29 commits, 9 issues, no releases | [23], [24] |
| OpenGS-SLAM: RGB-Only Gaussian Splatting SLAM for Unbounded Outdoor Scenes | Yes; ICRA 2025 repo | MIT | Python/CUDA/C++/GLSL/Jupyter; PyTorch 2.1.0, CUDA 11.8; DUSt3R checkpoint, CroCo RoPE CUDA extension; conda/pip | RGB-only; Waymo 9 preprocessed segments; unbounded outdoor scenes; depth path exists but not used for SLAM | Yes; real-time interactive SLAM window | Waymo is multi-camera dataset, but README example does not establish simultaneous multi-camera rig support; RGB-only outdoor sequence input | 204 stars; updated 2026-05-06; 7 commits, 2 issues, no releases; DUSt3R license acceptance required | [25], [26] |
| DG-SLAM: Robust Dynamic Gaussian Splatting SLAM with Hybrid Pose Optimization | Yes; NeurIPS 2024 official | MIT | Python; Conda; DROID-SLAM front-end fallback; pretrained DROID-SLAM weights; OneFormer masks | RGB-D dynamic scenes; TUM RGB-D dynamic, BONN Dynamic RGB-D, ScanNet subject to access; semantic motion masks in `seg_mask` | Unclear; README gives `python run_tum.py` but does not state online/offline | No multi-camera evidence | 79 stars; updated 2026-04-23; 7 commits, no releases; official implementation | [27], [28] |
| LSG-SLAM: Large-Scale Gaussian Splatting SLAM | Yes | BSD-3-Clause | Python/CUDA/shell/C++; Python 3.10, CUDA 11.6, PyTorch 1.12.1; custom depth rasterizer | EuRoC and KITTI; preprocessing produces depth images and global features | Partly; two-stage pipeline: front end + loop closure, then separate back end for pose-graph optimization/refinement | EuRoC/KITTI camera sequences; no explicit multi-camera rig support | 49 stars; updated 2026-05-18; 2 commits; no releases | [29], [30] |
| HI-SLAM2: Geometry-Aware Gaussian SLAM for Fast Monocular Scene Reconstruction | Yes | BSD-3-Clause | Python/CUDA/C++/GLSL/Shell; conda + `python setup.py install`; PyTorch CUDA 11.8; Omnidata depth/normal checkpoints | Monocular input only; Replica, ScanNet; own videos via preprocessing/COLMAP intrinsics | Yes; online monocular SLAM/reconstruction; demo outputs poses, map, renderings | Explicitly monocular only | 243 stars; updated 2026-05-18; rebuild CUDA kernel after pulls; demo about 2 minutes on RTX 4090 | [31], [32] |
| GSORB-SLAM | Yes; RA-L 2025 repo | GitHub reports Other; WebFetch saw mixed unknown/GPL and README badge inconsistency | Mostly C++ with C/Python; Ubuntu 20.04/22.04, CUDA 11.8, PyTorch 2.1.2, LibTorch, OpenCV CUDA, Eigen3, Pangolin, wandb; CMake edits | RGB-D; TUM-RGBD, Replica, ScanNet; ScanNet extraction from `.sens` | Yes; SLAM experiments; C++ eval can be disabled; Python offline evaluator | No multi-camera evidence beyond RGB-D sequence input | 57 stars; updated 2026-05-18; README says still under development and invites issues | [33], [34] |
| SemGauss-SLAM | Yes; IROS 2025 official | No GitHub license visible in metadata | Python/CUDA/C++; Python 3.10, PyTorch 1.12.1, CUDA 11.6; custom semantic rasterizer with NUM_SEMANTIC rebuild | RGB-D with semantic labels; Replica and ScanNet; rendered semantic GT / label-filt frames | Yes-ish; SLAM with online reconstruction/visualization scripts; eval/export after run | No multi-camera evidence | 77 stars; updated 2026-05-15; 40 commits, 2 issues, no releases | [35], [36] |
| Hier-SLAM: Semantic Gaussian Splatting SLAM with Hierarchical Categorical Representation | Yes; ICRA 2025 repo | Apache-2.0 | Python/CUDA/C++; conda Python 3.10, CUDA 11.6, PyTorch 1.12.1; compiled semantic 3DGS module | RGB-D with semantic labels; Replica and ScanNet; category trees | Yes-ish; online reconstruction/visualization scripts with post-run eval/export | No multi-camera evidence | 164 stars; updated 2026-05-09; 11 commits, 4 issues, no releases | [37], [38] |
| CaRtGS: Computational Alignment for Real-Time Gaussian Splatting SLAM | Yes; RA-L repo | GPL-3.0 per GitHub; WebFetch noted unknown license flags | Mostly C++ with C/Python; Ubuntu 20.04/22.04, CUDA 11.8, PyTorch 2.1.2, LibTorch, OpenCV CUDA, Eigen3, Pangolin, third-party Gaussian Splatting/tinyply/yaml-cpp/wandb | RGB-D; TUM-RGBD, Replica, ScanNet | Yes; real-time GS SLAM experiments; offline Python evaluator also present | No multi-camera evidence | 77 stars; updated 2026-04-21; README says still under development | [39], [40] |
| MDGS_SLAM: Multi-View Ray-Correspondence Densification | Yes-ish; repo title describes official/implementation | Apache-2.0 | Python; CUDA/PyTorch stack; modified ORB-SLAM2 Python binding; Pangolin/OpenCV/boost-python | RGB-D; Replica, TUM-RGBD, “Ours”; accurate depth assumed for ICP | Yes; real-time RGB-D SLAM with single and multi-process modes | “Multi-view ray-correspondence” is densification over views/keyframes, not necessarily multiple simultaneous cameras | 4 stars; updated 2026-04-09; low adoption; build caveats inherited from ORB-SLAM2 binding | [41], [42] |
| RTGS: Real-Time 3D Gaussian Splatting SLAM via Multi-Level Redundancy Reduction | Yes; MICRO 2025 repo | No GitHub license visible | Repo metadata says RTGS hardware/algorithm; details not deeply fetched due limited README evidence | Likely derived from real-time 3DGS SLAM; exact datasets not established in this pass | Likely yes from title, but not verified by README fetch | Unknown | 26 stars; updated 2026-04-06; sparse public evidence | [43] |
| MonoRTGS / MonoRTGS_ONX | Unofficial/derivative; says builds on MonoGS and Photo-SLAM | No license stated in fetched excerpt | C++/C/CUDA/Python; ONX/ARM64; manual PyTorch wheels, numpy/opencv/matplotlib/scipy; Docker CUDA 12.1 | TUM, Replica; config trees for RGB-D, stereo, mono, live | Yes; real-time SLAM / hardware speedup simulator | Config trees cover stereo/RGB-D/mono/live; not full multi-rig | 10 stars for MonoRTGS, 0 for ONX; updated 2026; specialized edge-GPU setup | [44], [45] |
| AgriGS-SLAM | Likely official; RA-L 2026 repo | No license from search metadata | Not fetched in depth | Orchard mapping across seasons via Multi-View Gaussian Splatting SLAM | Likely SLAM/mapping | Name explicitly says multi-view and agricultural robotics; needs follow-up before using | 26 stars; updated 2026-05-15 | [46] |
| MultiAgent-GaussianSplat-SLAM / project_slam_coko | Unofficial/experimental | No license from search metadata | Not fetched in depth | Multi-agent RGB-D Gaussian Splatting SLAM local submaps and shared evidence per description | Likely intended online | Explicitly independent cameras/local submaps; low trust until inspected | 0 stars; updated 2026-05-17/04-03; possible concept/prototype | [47], [48] |

## Recommended repositories to inspect first

1. **SplaTAM** ([1], [2]) — Best starting point for an RGB-D online SLAM implementation with permissive BSD-3 license, public benchmarks, Docker/Singularity, and clear dataset loaders. Limitation: single RGB-D camera assumptions; no native multi-camera rig support.
2. **MonoGS** ([3], [4]) — Important monocular baseline with RGB-D/stereo/live RealSense paths and active community use. License should be read carefully because GitHub reports “Other,” and third-party dependencies are material.
3. **Gaussian-SLAM** ([5], [6]) — MIT-licensed Python-heavy baseline with Replica/TUM/ScanNet/ScanNet++ reproduction scripts and seed-averaged benchmark caveats. Good to inspect for typed backend boundary ideas if online behavior is acceptable after source inspection.
4. **Photo-SLAM** ([7], [8], [9]) — Strong real-time C++ system for mono/stereo/RGB-D and RealSense, with separate evaluation toolkit. GPL-3.0 makes it better as an implementation reference than a directly embedded backend.
5. **DiskChunGS** ([17], [18]) — Most directly relevant to robot-scale mapping and multi-modal/ROS integration: mono/stereo/RGB-D, ORB-SLAM3 tracking/loop closure, external TF mode, chunking/offloading, Jetson notes. Risks: young repo, complex C++/CUDA/Docker stack, GPL/mixed third-party licensing.
6. **Gaussian-LIC** ([19], [20]) — Best robotics multi-sensor evidence: LiDAR-inertial-camera fusion, real-time pose and photorealistic GS map, robotics datasets. License not visible, dependency stack heavy.
7. **VINGS-Mono** ([21], [22]) and **OpenGS-SLAM** ([25], [26]) — Useful for outdoor/large-scene and visual-inertial/RGB-only directions, but not multi-camera rig systems.
8. **WildGS-SLAM / DG-SLAM** ([23], [24], [27], [28]) — Good if Mosaic later needs dynamic-scene suppression semantics; less directly relevant to multi-view robot-mounted camera rigs.
9. **GS-SLAM project page + rasterizer** ([12]-[14]) — Important paper/system, but full public implementation was not visible in this pass; treat as paper/rasterizer evidence only.

## Repository risks for Mosaic backend integration

- **Most systems couple SLAM, dataset parsing, visualization, evaluation, CUDA kernels, and experiment scripts.** Mosaic should wrap these behind process/protocol boundaries rather than importing their internals directly.
- **Licensing is uneven.** BSD/MIT/Apache repositories exist, but several prominent real-time systems are GPL-3.0 or mixed with Inria/non-commercial or unknown license flags. Direct code reuse requires legal review.
- **Multi-camera robot rigs are not first-class in most code.** Stereo/RGB-D/multi-sensor is common; simultaneous multiple independent robot-mounted cameras with deterministic rig extrinsics and fusion contracts is rare. DiskChunGS ROS/external TF and Gaussian-LIC/VINGS-Mono sensor-fusion designs are the closest inspected patterns.
- **Runtime stacks are fragile.** Many repos pin CUDA, PyTorch, OpenCV-with-CUDA, LibTorch, Pangolin, ORB-SLAM2/3, TensorRT, GTSAM, or custom rasterizers. This argues for optional backend packages or isolated subprocess/container adapters.
- **Benchmark nondeterminism is acknowledged.** Photo-SLAM and SEGS-SLAM run sequences five times; Gaussian-SLAM averages three seeds because the rasterizer is nondeterministic; MonoGS warns paper numbers may vary. Mosaic should store seed/hardware/runtime metadata and tolerance bands.
- **Dataset loaders are highly bespoke.** Replica/TUM/ScanNet/KITTI/Waymo layouts and preprocessing scripts differ by repo. Mosaic should avoid adopting any one repo's dataset layout as core.
- **Online vs offline claims vary.** SplaTAM, MonoGS, Photo-SLAM, RTG-SLAM, DiskChunGS, Gaussian-LIC, WildGS-SLAM, OpenGS-SLAM, HI-SLAM2 are visibly online/real-time; Gaussian-SLAM/DG-SLAM/semantic variants may require source inspection to confirm streaming behavior.
- **Maintenance ranges from active to prototype.** Starred CVPR/ICRA repos are active but many have no releases and few commits. New 2025/2026 repos may be incomplete despite impressive paper labels.

## Benchmarks and dataset notes found

- **Replica**: SplaTAM, Gaussian-SLAM, Photo-SLAM, RTG-SLAM, SEGS-SLAM, DiskChunGS, HI-SLAM2, GSORB-SLAM, SemGauss-SLAM, Hier-SLAM, CaRtGS, MDGS_SLAM.
- **TUM RGB-D**: SplaTAM, Gaussian-SLAM, Photo-SLAM, RTG-SLAM, SEGS-SLAM, DiskChunGS, DG-SLAM dynamic, WildGS-SLAM dynamic, GSORB-SLAM, CaRtGS, MDGS_SLAM.
- **ScanNet / ScanNet++**: SplaTAM, Gaussian-SLAM, RTG-SLAM/ScanNet++, SEGS-SLAM/ScanNet, DiskChunGS/ScanNet, HI-SLAM2, GSORB-SLAM, SemGauss-SLAM, Hier-SLAM, CaRtGS.
- **EuRoC**: MonoGS, Photo-SLAM, DiskChunGS, LSG-SLAM.
- **KITTI/KITTI360**: VINGS-Mono, DiskChunGS, LSG-SLAM; Gaussian-LIC-style robotics datasets are separate LiDAR-inertial-camera sets.
- **Waymo**: OpenGS-SLAM and VINGS-Mono evidence.
- **Dynamic RGB-D**: WildGS-SLAM, DG-SLAM, DGS-SLAM-like repos in search results.
- **Robotics sensor-fusion datasets**: Gaussian-LIC lists FAST-LIVO, FAST-LIVO2, R3LIVE, MCD, M2DGR.

## Numbered source list

1. https://github.com/spla-tam/SplaTAM
2. https://spla-tam.github.io/
3. https://github.com/muskie82/MonoGS
4. https://github.com/muskie82/MonoGS/blob/main/Dependencies.md
5. https://github.com/VladimirYugay/Gaussian-SLAM
6. https://vladimiryugay.github.io/gaussian_slam/index.html
7. https://github.com/HuajianUP/Photo-SLAM
8. https://huajianup.github.io/research/Photo-SLAM/
9. https://github.com/HuajianUP/Photo-SLAM-eval
10. https://github.com/MisEty/RTG-SLAM
11. https://gapszju.github.io/RTG-SLAM/static/pdfs/RTG-SLAM_arxiv.pdf
12. https://gs-slam.github.io/
13. https://github.com/gs-slam/gs-slam.github.io
14. https://github.com/yanchi-3dv/diff-gaussian-rasterization-for-gsslam
15. https://github.com/leaner-forever/SEGS-SLAM
16. https://github.com/leaner-forever/SEGS-SLAM/blob/master/LICENSE
17. https://github.com/leggedrobotics/DiskChunGS
18. https://github.com/leggedrobotics/DiskChunGS/blob/main/README.md
19. https://github.com/APRIL-ZJU/Gaussian-LIC
20. https://github.com/APRIL-ZJU/Gaussian-LIC/blob/master/README.md
21. https://github.com/Fudan-MAGIC-Lab/VINGS-Mono
22. https://vings-mono.github.io/
23. https://github.com/GradientSpaces/WildGS-SLAM
24. https://gradientspaces.github.io/WildGS-SLAM/
25. https://github.com/3DAgentWorld/OpenGS-SLAM
26. https://3d-aigc.github.io/OpenGS-SLAM/
27. https://github.com/fudan-zvg/DG-SLAM
28. https://fudan-zvg.github.io/DG-SLAM/
29. https://github.com/lsg-slam/LSG-SLAM
30. https://lsg-slam.github.io/
31. https://github.com/Willyzw/HI-SLAM2
32. https://hi-slam2.github.io/
33. https://github.com/Aczheng-cai/GSORB-SLAM
34. https://aczheng-cai.github.io/GSORB-SLAM.github.io/
35. https://github.com/IRMVLab/SemGauss-SLAM
36. https://github.com/IRMVLab/SemGauss-SLAM/blob/main/README.md
37. https://github.com/LeeBY68/Hier-SLAM
38. https://github.com/LeeBY68/Hier-SLAM/blob/main/README.md
39. https://github.com/DapengFeng/cartgs
40. https://github.com/DapengFeng/cartgs/blob/master/README.md
41. https://github.com/Just-ZJJ/MDGS_SLAM
42. https://github.com/Just-ZJJ/MDGS_SLAM/blob/main/README.md
43. https://github.com/UMN-ZhaoLab/RTGS
44. https://github.com/Nemo0412/MonoRTGS
45. https://github.com/Nemo0412/MonoRTGS_ONX
46. https://github.com/AIRLab-POLIMI/agri-gs-slam
47. https://github.com/Elonian/MultiAgent-GauassianSplat-SLAM
48. https://github.com/RobotFlow-Labs/project_slam_coko
49. https://github.com/93won/monocular_gaussian_splatting_slam_benchmark
50. https://github.com/iis-esslingen/nerf-3dgs-benchmark

## Gaps / follow-up candidates

- Inspect AgriGS-SLAM, MultiAgent-GaussianSplat-SLAM, SLAM-COKO, and iis-esslingen benchmark if the lead wants explicit multi-view/multi-agent or benchmark-suite evidence.
- Directly inspect source/config of Gaussian-SLAM and DG-SLAM to determine actual online streaming behavior.
- Check license files and third-party notices manually for MonoGS, GSORB-SLAM, DiskChunGS, Gaussian-LIC, VINGS-Mono, SemGauss-SLAM, and any repo with GitHub `NOASSERTION` or `Other` metadata.
- If Mosaic needs live multi-camera robot rigs, search ROS2 wrappers/forks: `splatam-ros2`, `gaussian_slam_ros`, `photo_slam_ros_combine`, DiskChunGS ROS wrapper, and experimental multi-agent repos.
