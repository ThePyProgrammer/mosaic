# Online / Incremental 3D Gaussian Splatting SLAM Systems for Moving Cameras

Researcher: R1  
Date: 2026-05-18  
Scope: academic papers and official project pages for online, real-time, or incremental 3D Gaussian Splatting SLAM / Gaussian Splatting mapping systems relevant to moving-camera robotics, 2023-2026. This report prioritizes primary sources and code/project availability claims, not a deep repository implementation inventory.

## Executive synthesis

The 3DGS SLAM landscape moved quickly after 3D Gaussian Splatting became a practical rendering representation. The most implementation-relevant open-source or project-backed systems for Mosaic are currently RGB-D systems such as SplaTAM, GS-SLAM, Gaussian-SLAM, CG-SLAM, LoopSplat, RTG-SLAM, and Splat-SLAM; monocular/RGB-only systems such as MonoGS, Photo-SLAM, Splat-SLAM, HI-SLAM2, M^3, and VIGS-SLAM; and multi-sensor robotics systems such as Gaussian-LIC, Gaussian-LIC2, LIV-GaussMap, GS-LIVO, LIVE-GS, LiV-GS, and RMGS-SLAM. Multi-agent systems such as GRAND-SLAM, CoKo-SLAM, and MAGS-SLAM are especially relevant to multi-robot or distributed-map questions, but they are not the same as synchronized multi-camera rig SLAM.

For an open-source implementation baseline, SplaTAM and MonoGS remain the clearest starting points: SplaTAM is an online dense RGB-D SLAM system with public code and common benchmarks, while MonoGS provides a public monocular-first implementation with RGB-D and experimental stereo support. For robot-mounted moving cameras with inertial/LiDAR priors, Gaussian-LIC and VIGS-SLAM are more robotics-aligned, but several of the newest LiDAR-inertial-visual systems are paper-only or have promised rather than verified code release.

## Evidence table

| System | Paper/project | Year | Online status | Sensor/input | Code availability claim | Benchmark evidence seen | Source refs |
|---|---|---:|---|---|---|---|---|
| SplaTAM | Splat, Track & Map 3D Gaussians for Dense RGB-D SLAM | 2023/2024 | Official page calls it a simple online tracking and mapping system; map grows by adding Gaussians | Single unposed RGB-D camera | Official project links GitHub; repo is public with BSD-3-Clause license | ScanNet++, Replica, online iPhone examples; repo mentions Replica, TUM-RGBD, ScanNet, ScanNet++, Replica-V2 | [1], [2], [3] |
| GS-SLAM | Dense Visual SLAM with 3D Gaussian Splatting | 2023/2024 | Real-time tracking, mapping, and rendering on GPU; adaptive incremental expansion adds/deletes Gaussians | RGB-D | Project page shows paper, modified rasterization code, and GitHub repository links | Replica and TUM-RGBD; page reports 386 FPS average on Replica and comparisons with real-time methods | [4], [5] |
| MonoGS / Gaussian Splatting SLAM | Gaussian Splatting SLAM | 2023/2024 | Project says live monocular SLAM at 3 fps | Monocular primary; extendable to RGB-D; repo also lists stereo experimental and Realsense live demo | Public GitHub repo | TUM monocular sequences, TableTop/Chairs/Teapot/Salad, Replica Office scenes; repo scripts for TUM-RGBD, Replica, EuRoC | [6], [7], [8] |
| Photo-SLAM | Real-time Simultaneous Localization and Photorealistic Mapping for Monocular, Stereo, and RGB-D Cameras | 2023/2024 | Real-time and online photorealistic mapping; CVPR 2024 | Monocular, stereo, RGB-D | Official page and repo link public GitHub; repo visible with GPL-3.0 flag | Replica, TUM RGB-D, EuRoC; page claims 30% PSNR improvement and hundreds-times rendering speedup on Replica | [9], [10], [11] |
| Gaussian-SLAM | Photo-realistic Dense SLAM with Gaussian Splatting | 2023/2024 | Online dense SLAM with incremental new-Gaussian seeding and submaps | Single-camera RGB-D videos | Public GitHub repo, MIT license; arXiv page itself does not explicitly show code | Repo mentions Replica, TUM_RGBD, ScanNet, ScanNet++; paper says synthetic and real-world datasets | [12], [13] |
| RTG-SLAM | Real-time 3D Reconstruction at Scale using Gaussian Splatting | 2024 | Real-time, per-frame, online/incremental update loop | RGB-D camera | No explicit public code/project release seen on arXiv page | Multiple large-scale RGB-D scenes; comparisons to NeRF-based RGB-D SLAM; no named datasets in abstract excerpt | [14] |
| CG-SLAM | Efficient Dense RGB-D SLAM in a Consistent Uncertainty-aware 3D Gaussian Field | 2024 | Online RGB-D SLAM; near real-time with up to 15 Hz tracking and real-time third-person rendering | RGB-D sequence | Project says source code will be publicly available and links GitHub/project | Various datasets; project compares against PointSLAM, Co-SLAM, NeRF-SLAM, concurrent Gaussian methods; dataset names not visible in excerpt | [15], [16] |
| LoopSplat | Loop Closure by Registering 3D Gaussian Splats | 2024 | Online loop closure; not explicitly real-time | RGB-D images | Paper/project say code is available; official page provides GitHub code link | Replica, TUM-RGBD, ScanNet, ScanNet++ | [17], [18] |
| Splat-SLAM | Globally Optimized RGB-only SLAM with 3D Gaussians | 2024 | RGB-only SLAM with keyframe/global optimization; not explicitly real-time, but claims fast runtimes | RGB-only, with monocular depth estimator support | Paper says source code available on GitHub; repo is public archive with Apache-2.0 license | Replica, TUM-RGBD, ScanNet | [19], [20] |
| EndoGSLAM | Real-Time Dense Reconstruction and Tracking in Endoscopic Surgeries using Gaussian Splatting | 2024 | Real-time online tracking/reconstruction; page reports over 100 fps rendering | Endoscopic RGB-D / surgical intrabody imagery | Project page links GitHub code and data/pretrain | Comparisons against traditional/neural SLAM; ORB-SLAM3 and Endo-Depth visible; no standard dataset names seen | [21], [22] |
| HI-SLAM2 | Geometry-Aware Gaussian SLAM for Fast Monocular Scene Reconstruction | 2024/2025 | Online/incremental with on-the-fly global consistency, online loop closing, continuous mapping, instant map updates | Monocular RGB only | Project page and GitHub code available; arXiv says source would be made available at project site | Replica, ScanNet, ScanNet++; project also shows Waymo Open Dataset | [23], [24], [25] |
| WildGS-SLAM | Monocular Gaussian Splatting SLAM in Dynamic Environments | 2025 | ArXiv excerpt does not state online/real-time/incremental | Monocular RGB | No explicit code/project release seen | Multiple datasets, improved dynamic-scene results; dataset names not visible in excerpt | [26] |
| GRAND-SLAM | Local Optimization for Globally Consistent Large-Scale Multi-Agent Gaussian SLAM | 2025 | Collaborative large-scale SLAM; page does not explicitly say online/real-time | RGB-D visual SLAM; multi-agent | No explicit code-release claim seen | Replica and Kimera-Multi; claims 28% higher PSNR and 91% lower multi-agent tracking error | [27] |
| Gaussian-LIC | Real-Time Photo-Realistic SLAM with Gaussian Splatting and LiDAR-Inertial-Camera Fusion | 2024/2025 | Real-time, intended for online robust pose estimation and online mapping | LiDAR + IMU + camera | Abstract says code has been released with GitHub link | Extensive experiments; claims real-time performance and mapping outperforming methods using GT poses; named datasets not visible in excerpt | [28] |
| LIV-GaussMap | LiDAR-Inertial-Visual Fusion for Real-time 3D Radiance Field Map Rendering | 2024 | Real-time rendering; excerpt does not explicitly say online/incremental | LiDAR + inertial + visual | Authors say software, hardware, and self-collected datasets are released | Diverse LIV datasets; no named benchmarks visible | [29] |
| LVI-GS | Tightly-coupled LiDAR-Visual-Inertial SLAM using 3D Gaussian Splatting | 2024 | Real-time photorealistic mapping; online/incremental not explicit in abstract excerpt | LiDAR + camera + inertial | No explicit code release seen | Numerical experiments; no named datasets visible | [30] |
| LiV-GS | LiDAR-Vision Integration for 3D Gaussian Splatting SLAM in Outdoor Environments | 2024 | Outdoor SLAM, reports 7.98 FPS; online implied but not explicit | LiDAR + vision | No explicit code release seen | Extensive comparative experiments on SLAM/rendering/mapping; cross-modal radar-LiDAR localization use case | [31] |
| GS-LIVO | Real-Time LiDAR, Inertial, and Visual Multi-sensor Fused Odometry with Gaussian Mapping | 2025 | Real-time; sliding-window Gaussian updates | LiDAR + IMU + camera/visual | Authors say implementation algorithms, hardware designs, and CAD models will be public | Demonstrated on NVIDIA Jetson Orin NX; no named benchmark in excerpt | [32] |
| Gaussian-LIC2 | LiDAR-Inertial-Camera Gaussian Splatting SLAM | 2025 | Real-time and incrementally reconstructing a 3D Gaussian map | Camera + LiDAR + inertial; RGB plus sparse LiDAR depths | Abstract says dataset and code will be publicly available on project page | Dedicated LiDAR-Inertial-Camera dataset with ground-truth poses/depth/extrapolated trajectories | [33] |
| LIVE-GS | Online LiDAR-Inertial-Visual State Estimation and Globally Consistent Mapping with 3D Gaussian Splatting | 2025/2026 | Explicit online LiDAR-inertial-visual SLAM framework | LiDAR + inertial + visual | No explicit public code repo/project link seen | Public and authors' datasets; compares to 3DGS SLAM baselines | [34] |
| RMGS-SLAM | Real-time Multi-sensor Gaussian Splatting SLAM | 2026 | Explicit real-time; continuous mapping and loop closure | Hardware-synchronized LiDAR-camera-IMU / LiDAR-Inertial-Visual | No code-release claim seen | Public datasets plus authors' large-scale looped outdoor dataset with ground-truth trajectories | [35] |
| VIGS-SLAM | Visual Inertial Gaussian Splatting SLAM | 2025/2026 | Real-time tracking with map updates and loop closure | RGB frames + IMU readings | Project page gives public GitHub code link; arXiv excerpt links project page | Five challenging datasets; claims state-of-the-art | [36], [37] |
| CoKo-SLAM | Compact Keyframe-Optimized Multi-Agent Gaussian Splatting SLAM | 2026 | Multi-agent collaborative SLAM; central server merges maps; online status implied but not deeply verified | RGB-D; pure rendered-depth and camera-depth modes | ArXiv/project points to public GitHub lemonci/coko-slam; repo visible with LICENSE file | ReplicaMultiagent and AriaMultiagent; paper says synthetic and real-world datasets and 85-95% less transmitted data | [38], [39] |
| MAGS-SLAM | Monocular Multi-Agent Gaussian Splatting SLAM for Geometrically and Photometrically Consistent Reconstruction | 2026 | Real-time mapping in collaborative pipeline | Monocular RGB-only, multi-agent | No repository/code release seen | Introduces ReplicaMultiagent Plus; synthetic and real-world datasets | [40] |
| M^3 | Dense Matching Meets Multi-View Foundation Models for Monocular Gaussian Splatting SLAM | 2026 | Streaming/online reconstruction and refinement from video | Uncalibrated monocular video | Official project page points to a Code repository; arXiv page itself shows paper links only | Indoor/outdoor datasets; ScanNet++; project compares to online reconstruction and feed-forward 3DGS baselines | [41], [42] |
| VarSplat | Uncertainty-aware 3D Gaussian Splatting for Robust RGB-D SLAM | 2026 | RGB-D SLAM; online status not deeply verified from abstract excerpt | RGB-D | No code claim seen in arXiv search excerpt | Replica, TUM-RGBD, ScanNet, ScanNet++ | [43] |
| MipSLAM | Alias-Free Gaussian Splatting SLAM | 2026 | Camera-based 3DGS SLAM; online status not deeply verified from search excerpt | Camera-based, likely RGB-D/visual depending paper | GitHub yzli1998/MipSLAM shown in arXiv search excerpt | Replica, TUM | [43] |
| GS3LAM | Gaussian Semantic Splatting SLAM | 2026 | Semantic 3DGS SLAM; online status not deeply verified from search excerpt | RGB + depth + semantics | GitHub lif314/GS3LAM shown in arXiv search excerpt | Benchmark datasets, names not visible in excerpt | [43] |
| SGAD-SLAM | Splatting Gaussians at Adjusted Depth for Better Radiance Fields in RGBD SLAM | 2026 | RGB-D SLAM; online status not deeply verified from search excerpt | RGB-D | Project page shown in arXiv search excerpt | Widely used benchmarks, names not visible in excerpt | [43] |
| Compact / dynamic 4D entries | D^2GSLAM, DAGS-SLAM, RU4D-SLAM, VBGS-SLAM and related dynamic/uncertainty systems | 2025/2026 | Mostly abstract-level evidence; some dynamic-scene/4D SLAM claims | RGB-D, monocular, dynamic-scene variants | Mixed; RU4D has project page; others unclear | Dynamic RGB-D or standard benchmarks; not fully extracted here | [43] |

## Notes on core algorithm patterns

### RGB-D online Gaussian SLAM

SplaTAM, GS-SLAM, Gaussian-SLAM, RTG-SLAM, CG-SLAM, and LoopSplat all use RGB-D streams as a stabilizing source of geometry. The common pattern is direct tracking against a rendered Gaussian map, followed by selective densification or Gaussian insertion in newly observed or high-error regions. SplaTAM emphasizes a silhouette/density mask and growing the map; GS-SLAM emphasizes real-time differentiable RGB-D splatting with adaptive expansion and coarse-to-fine pose optimization; Gaussian-SLAM emphasizes submaps and incremental new-Gaussian seeding; RTG-SLAM emphasizes compact splats and optimizing only unstable Gaussians; CG-SLAM emphasizes an uncertainty-aware Gaussian field; LoopSplat adds 3DGS submap registration for loop closure.

For Mosaic, this group is the best source for clean typed contracts around observations, tracking updates, map snapshots, submap IDs, insertion policies, and benchmark-compatible outputs. It is also less dependent on learned monocular depth or LiDAR fusion than the other groups.

### Monocular / RGB-only Gaussian SLAM

MonoGS, Splat-SLAM, HI-SLAM2, M^3, WildGS-SLAM, and parts of Photo-SLAM are relevant to camera-only moving platforms. Their challenge is depth/scale consistency. MonoGS tracks by direct optimization against Gaussians and supports monocular-first operation. Splat-SLAM globally optimizes RGB-only tracking and deforms a Gaussian map after keyframe pose/depth updates. HI-SLAM2 adds loop closure, pose-graph bundle adjustment, scale alignment, and explicit deformation of Gaussian units. M^3 uses multi-view foundation model correspondences and matching heads to improve monocular pose estimation and reconstruction.

For Mosaic, this group is attractive for moving cameras without active depth but should be treated as more fragile than RGB-D baselines until deterministic regression artifacts exist.

### Multi-sensor robotics Gaussian SLAM

Gaussian-LIC, Gaussian-LIC2, LIV-GaussMap, LVI-GS, LiV-GS, GS-LIVO, LIVE-GS, RMGS-SLAM, and VIGS-SLAM are closer to robotics deployments because they combine visual data with IMU and/or LiDAR. The recurring pattern is to use LiDAR/IMU/VIO for robust state estimation and/or initialization, then optimize or update a Gaussian map for photorealistic reconstruction. Gaussian-LIC and Gaussian-LIC2 are especially relevant because they explicitly close the loop between pose estimation and Gaussian mapping. RMGS-SLAM and LIVE-GS push toward outdoor global consistency and loop closure.

For Mosaic, these systems are likely better architectural references for backend protocols than for pure-Python foundation modules: many need C++/CUDA, synchronized sensors, calibration, and dataset-specific preprocessing. Mosaic should keep them behind optional backend adapters and stable observation/pose contracts.

### Multi-agent and distributed Gaussian SLAM

GRAND-SLAM, CoKo-SLAM, and MAGS-SLAM address collaborative or multi-agent Gaussian SLAM. They are relevant to the user's multi-camera/multi-robot concern only indirectly: multi-agent means separate moving platforms or agents with local maps and communication/composition, not necessarily a rigid robot-mounted multi-camera rig. CoKo-SLAM's compact keyframe/map exchange and MAGS-SLAM's compact submap summaries are useful for thinking about bounded map exchange, provenance, and fusion contracts.

## Most relevant systems for Mosaic

1. **SplaTAM**: Best early open-source RGB-D online baseline. It aligns with Mosaic's need for a deterministic typed SLAM backend contract: input observations, tracking output, map growth, snapshots, and evaluation on Replica/TUM/ScanNet-style datasets.
2. **MonoGS**: Best open-source monocular-first baseline. It is useful for defining backend capability flags: monocular, RGB-D, stereo experimental, live camera, and dataset replay.
3. **LoopSplat**: Strong reference for map/submap loop closure and global consistency APIs. Mosaic's future fusion/provenance layer can borrow the notion of submap registration and pose-graph constraints without copying implementation internals.
4. **Gaussian-LIC / VIGS-SLAM / Gaussian-LIC2**: Best robotics-aligned references for multi-sensor moving platforms. They suggest contracts for synchronized camera-IMU-LiDAR observations, continuous-time poses, and map-derived constraints feeding back into tracking.
5. **CoKo-SLAM / MAGS-SLAM / GRAND-SLAM**: Relevant for multi-agent distributed map fusion and compact map exchange, but they should not be confused with rigid multi-camera rig support.
6. **HI-SLAM2 / Splat-SLAM / M^3**: Important for RGB-only moving-camera SLAM, especially global optimization and depth/scale consistency. Useful as future backends once Mosaic has evaluation gates.

## Caveats and uncertain claims

- Several arXiv pages expose only abstracts; claims about code availability, exact benchmarks, and online status may be absent even when project pages or repositories exist elsewhere.
- Some systems advertise code as “will be made public” rather than verified released code. This applies especially to newer 2025-2026 LiDAR-inertial-camera and uncertainty/dynamic variants.
- “Real-time,” “online,” “incremental,” and “SLAM” are used inconsistently. Some papers report real-time rendering but rely on offline refinement; others perform online tracking but include offline map cleanup/refinement.
- Multi-agent Gaussian SLAM is not the same as synchronized multi-camera robot-rig SLAM. It provides useful fusion and communication ideas, but R3 should separately evaluate rigid multi-camera fit.
- Benchmark coverage in this R1 report is intentionally not exhaustive. R4 should extract metric tables and exact sequences. Here, benchmark evidence is only what was visible in primary pages/abstracts/repositories.
- Endoscopic, underwater, orchard, radar, and dynamic-scene systems are relevant edge cases but may have domain assumptions that do not transfer directly to Mosaic's robot-neutral core contracts.
- Some search/fetch results were unavailable or returned unrelated pages for guessed arXiv IDs; those entries were excluded or corrected by searching arXiv title queries and official pages.

## Numbered source list

1. SplaTAM arXiv: https://arxiv.org/abs/2312.02126
2. SplaTAM project page: https://spla-tam.github.io/
3. SplaTAM GitHub: https://github.com/spla-tam/SplaTAM
4. GS-SLAM arXiv: https://arxiv.org/abs/2311.11700
5. GS-SLAM project page: https://gs-slam.github.io/
6. Gaussian Splatting SLAM / MonoGS arXiv: https://arxiv.org/abs/2312.06741
7. Gaussian Splatting SLAM / MonoGS project page: https://rmurai.co.uk/projects/GaussianSplattingSLAM/
8. MonoGS GitHub: https://github.com/muskie82/MonoGS
9. Photo-SLAM arXiv: https://arxiv.org/abs/2311.16728
10. Photo-SLAM project page: https://huajianup.github.io/research/Photo-SLAM/
11. Photo-SLAM GitHub: https://github.com/HuajianUP/Photo-SLAM
12. Gaussian-SLAM arXiv: https://arxiv.org/abs/2312.10070
13. Gaussian-SLAM GitHub: https://github.com/VladimirYugay/Gaussian-SLAM
14. RTG-SLAM arXiv: https://arxiv.org/abs/2404.19706
15. CG-SLAM arXiv: https://arxiv.org/abs/2403.16095
16. CG-SLAM project page: https://zju3dv.github.io/cg-slam/
17. LoopSplat arXiv: https://arxiv.org/abs/2408.10154
18. LoopSplat project page: https://loopsplat.github.io/
19. Splat-SLAM arXiv: https://arxiv.org/abs/2405.16544
20. Splat-SLAM GitHub: https://github.com/google-research/Splat-SLAM
21. EndoGSLAM arXiv: https://arxiv.org/abs/2403.15124
22. EndoGSLAM project page: https://loping151.github.io/endogslam/
23. HI-SLAM2 arXiv: https://arxiv.org/abs/2411.17982
24. HI-SLAM2 project page: https://hi-slam2.github.io/
25. HI-SLAM2 GitHub: https://github.com/Willyzw/HI-SLAM2
26. WildGS-SLAM arXiv: https://arxiv.org/abs/2504.03886
27. GRAND-SLAM arXiv: https://arxiv.org/abs/2506.18885
28. Gaussian-LIC arXiv: https://arxiv.org/abs/2404.06926
29. LIV-GaussMap arXiv: https://arxiv.org/abs/2401.14857
30. LVI-GS arXiv: https://arxiv.org/abs/2411.02703
31. LiV-GS arXiv: https://arxiv.org/abs/2411.12185
32. GS-LIVO arXiv: https://arxiv.org/abs/2501.08672
33. Gaussian-LIC2 arXiv: https://arxiv.org/abs/2507.04004
34. LIVE-GS arXiv: https://arxiv.org/abs/2507.23273
35. RMGS-SLAM arXiv: https://arxiv.org/abs/2604.12942
36. VIGS-SLAM arXiv: https://arxiv.org/abs/2512.02293
37. VIGS-SLAM project page: https://vigs-slam.github.io
38. CoKo-SLAM arXiv: https://arxiv.org/abs/2604.00804
39. CoKo-SLAM GitHub: https://github.com/lemonci/coko-slam
40. MAGS-SLAM arXiv: https://arxiv.org/abs/2605.10760
41. M^3 arXiv: https://arxiv.org/abs/2603.16844
42. M^3 project page: https://city-super.github.io/M3/
43. ArXiv search results for 3D Gaussian Splatting SLAM systems: https://arxiv.org/search/?query=3D+Gaussian+Splatting+SLAM&searchtype=all&abstracts=show&order=-announced_date_first&size=50
