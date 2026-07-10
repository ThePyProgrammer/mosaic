# Multi-view / multi-camera 3DGS SLAM applicability research

Researcher: R3  
Date: 2026-05-18  
Scope: true multi-view, multi-camera, robot-mounted moving-camera applicability of open-source online 3D Gaussian Splatting SLAM implementations.

## Executive takeaways

1. **True native multi-camera robot-rig support is rare.** Most open-source 3DGS SLAM systems process one temporal camera stream, optionally with depth, stereo, IMU, or LiDAR. They may be "multi-view" only in the NeRF/3DGS sense of many frames over time, not synchronized multiple robot-mounted cameras.
2. **Best native fit found: AgriGS-SLAM.** It explicitly documents a tractor-mounted platform with **three synchronized RGB-D cameras**, visual + LiDAR SLAM, seasonal orchard data, and real-time on-tractor claims. It is the clearest match to Mosaic's target of multiple moving robot-mounted cameras, but appears domain-specific and batch/pipeline-heavy rather than a clean library backend.
3. **Best adaptable robotics backends:** RTG-SLAM, Photo-SLAM, Gaussian-LIC, GS-LIVO, LVI-3DGS, MM3DGS-SLAM, VINGS-Mono, and TRGS-SLAM each bring useful pieces: ROS wrappers, stereo/RGB-D support, visual-inertial fusion, LiDAR-inertial-camera fusion, or robot datasets. None of these, except AgriGS-SLAM, clearly documents generic synchronized multi-camera rig ingestion.
4. **Poor fit for Mosaic's immediate multi-camera goal:** MonoGS, SplaTAM, Gaussian-SLAM, Splat-SLAM, Splat-SLAM/Google Splat-SLAM, WildGS-SLAM, OpenGS-SLAM, S3PO-GS, SGS-SLAM, 2DGS-SLAM, VTGaussian-SLAM, DG-SLAM, and most semantic/dynamic derivatives are primarily monocular or single RGB-D sequence systems.
5. **Mosaic adaptation should treat every candidate as an isolated backend.** Public APIs should not inherit their dataset/config assumptions. Mosaic needs typed contracts for timestamped multi-camera observations, calibrated rigs, pose direction/frame semantics, external-front-end pose sources, and deterministic regression harnesses before integrating any backend.

## Conservative interpretation rules used

- **Native multi-camera** means documented support for synchronized multiple camera streams or a calibrated multi-camera rig, not just many frames, multi-view optimization, train/test views, or offline novel-view synthesis.
- **Stereo** counts as two cameras but is classified separately as a fixed pair, not a general multi-camera robot rig, unless the implementation documents generic rig handling.
- **RGB-D** counts as a single camera stream with depth, not multi-camera.
- **Visual-inertial** and **LiDAR-camera** systems are strong robotics evidence, but not multi-camera evidence unless multiple cameras are documented.
- **Multi-agent** means multiple independently moving agents/maps; this is not automatically multi-camera support.

## Evidence table

| System | Native multi-camera? | Sensor setup | Camera motion assumptions | Robot/dataset evidence | What would be needed for Mosaic adaptation | Confidence | Source refs |
|---|---:|---|---|---|---|---|---|
| **AgriGS-SLAM** | **Yes, documented three synchronized RGB-D cameras** | Visual + LiDAR SLAM; three synchronized RGB-D cameras; C++ LiDAR odometry, Scan Context loop closure, 3DGS rendering | Moving tractor-mounted multi-camera platform in orchards; trajectory protocol across seasons | Tractor-mounted platform; apple and pear orchards; dormancy/flowering/harvesting; demo dataset on Hugging Face; claims real-time on-tractor; compares with Photo-SLAM, Splat-SLAM, PINGS, OpenGS-SLAM | Wrap as an isolated backend first. Need inspect license/build, data schema, synchronization model, rig calibration representation, LiDAR pose/depth use, and whether camera count is hard-coded to three. Add Mosaic adapters for `CameraRig`, synchronized `MultiViewObservation`, LiDAR-derived pose/depth metadata, and deterministic orchard subset replay. | **High** for native multi-camera claim; medium for generality beyond orchard/tractor setup | [19], [20] |
| **RTG-SLAM** | **Partial: stereo pair; not generic rig** | ROS modes `mono`, `stereo`, `rgbd`; image/right-image/depth topics; external pose via TF frames | Online moving camera; ROS stream or dataset replay; stereo/RGB-D supported | Replica, TUM RGB-D, KITTI; ZED2 ROS example; Jetson support; all 11 KITTI sequences claimed; evaluation scripts producing logs | Good Mosaic candidate for backend isolation and ROS-like stream adaptation. Need generalize beyond ROS params, model stereo as two calibrated cameras, define timestamp policy, external pose/TF frame mapping, and verify determinism on KITTI/TUM subsets. | High for stereo/RGB-D/ROS evidence; low for generic multi-camera rig | [17] |
| **Photo-SLAM** | **Partial: stereo pair/RGB-D; not generic rig** | Monocular, stereo, RGB-D; ORB-SLAM3-derived tracking; RealSense D455 demo | Online single moving camera stream, stereo pair, or RGB-D sensor | Replica, TUM RGB-D, EuRoC; RealSense D455 example; evaluation toolkit; sequences run five times | Useful as a pragmatic visual SLAM + 3DGS backend. Need isolate C++/CUDA/native deps, map ORB-SLAM3 poses to Mosaic frames, add adapters for monocular/stereo/RGB-D observations, and treat stereo as a special two-camera rig. Not enough evidence for multi-camera arrays. | High for stereo/RGB-D; low for multi-camera rig | [3], [4], [5] |
| **MonoRTGS / RTGS family** | **Partial: stereo/RGB-D configs; not generic rig** | RGB-D, stereo, monocular, live configs; baseline vs MonoRTGS scripts; hardware speedup focus | Online SLAM, likely single stream or fixed stereo/RGB-D mode inherited from MonoGS/Photo-SLAM-style pipelines | TUM and Replica configs; ONX/edge GPU hardware evaluation scripts; no robot platform evidence found | Potential performance-oriented backend only after code inspection. Need verify input APIs, inherited assumptions, frame semantics, and whether stereo is true tracking input or config artifact. | Medium | [8], [9] |
| **Gaussian-LIC** | **No documented multi-camera; strong multi-sensor robotics** | LiDAR + inertial + camera; ROS launch/configs; 3D Gaussian map | Moving LiDAR-inertial-camera platform; online real-time photo-realistic mapping | FAST-LIVO, FAST-LIVO2, R3LIVE, MCD, M2DGR; ROS bag/config examples; ICRA 2025 | Strong candidate for Mosaic's multi-sensor backend seam, not multi-camera seam. Need model LiDAR/camera/IMU extrinsics, timestamp alignment, map output adapter, and keep ROS/native stack isolated. Multi-camera would need extending input frontend and calibrations. | High for LIC; low for multi-camera | [10] |
| **GS-LIVO** | **No documented multi-camera; strong robot LIVO** | LiDAR-inertial-visual odometry; lidar-plus-image measurement fusion; 3DGS mapping | Moving platforms, car/handheld/edge deployments | MARS-LVIG, Landmark, UAV Playground, FAST-LIVO HKU; car platform, handheld platform, vehicle path planning, Jetson Orin NX | Adapt as a LiDAR-inertial-visual backend behind protocols. Need inspect ROS/data interfaces, output splat map stability, camera assumptions, and create a typed LiDAR/IMU adjunct outside core camera contracts. Multi-camera requires separate design work. | High for robot LIVO; low for multi-camera | [25] |
| **LVI-3DGS** | **No documented multi-camera; calibrated LiDAR-IMU-camera** | LiDAR, inertial, visual sensors; IESKF; Gaussian setup from LiDAR + visual info | Vehicle and handheld deployments; online edge compute shown | MARS-LVIG, Landmark, UAV Playground, FAST-LIVO HKU; Jetson Orin NX; RTX 4090 dataset demos | Similar to GS-LIVO/Gaussian-LIC. Useful for Mosaic backend isolation and sensor-fusion contracts. Need enforce typed extrinsics, frame direction, and deterministic replay. Multi-camera support not evidenced. | Medium-high | [26] |
| **MM3DGS-SLAM** | **No; single RGB + depth + IMU/LiDAR evidence** | Vision, depth, inertial measurements; UT-MM rosbag topics include RGB, depth, IMU, LiDAR, pose; camera-to-IMU transform | Moving robot/dataset stream, but single RGB/depth feed | UT-MM and TUM-RGBD; Jackal pose topic `/vrpn_client_node/Jackal_Latest/pose`; trajectory and image evaluation scripts | Good robotics-oriented candidate for typed multi-modal observation contracts. Need clarify whether LiDAR is used online or only dataset metadata, isolate ROS assumptions, and add adapter for one RGB-D+IMU stream. Multi-camera would require extension. | High for multi-modal single-camera; low for multi-camera | [12] |
| **VINGS-Mono** | **No; monocular visual-inertial** | Monocular + visual-inertial Gaussian Splatting SLAM; calibration files; top-view camera images in demo data; sync/unsync configs | Large-scene moving monocular VI setup; KITTI/KITTI360/Waymo-style vehicle motion | Hotel, Waymo, KITTI, KITTI360; calibration and sync/unsync configs; arXiv paper | Useful if Mosaic wants VIO pose priors for a single moving camera. Need model IMU/camera calibration and pose source. No evidence for multiple synchronized cameras. | Medium-high | [11] |
| **TRGS-SLAM** | **No; thermal mono + IMU calibration** | Thermal image stream + IMU; can fall back to pure monocular; camera-IMU calibration YAMLs | Moving thermal camera, indoor/outdoor TRNeRF sequences | TRNeRF slow/medium/fast indoor/outdoor sequences; ATE/SSIM/LPIPS/memory/timing outputs | Specialized modality backend. Need add thermal image buffer semantics if relevant. Not appropriate as first multi-camera Mosaic target. | Medium | [28] |
| **MAGiC-SLAM** | **No generic multi-camera; yes multi-agent** | Multi-agent RGB-only Gaussian SLAM; n+1 GPUs for n agents; Aria/Replica multi-agent data | Multiple moving agents rather than multiple cameras on one robot rig | ReplicaMultiagent, AriaMultiagent, AriaDigitalTwin clips; metrics over three seeds | Conceptually useful for multi-session/multi-robot map fusion, not camera-rig ingestion. Mosaic adaptation would need separate `agent_id`/session/map fusion contracts and deterministic non-CUDA tests. | High for multi-agent; low for multi-camera rig | [13] |
| **OpenGS-SLAM** | **No; RGB-only outdoor monocular** | RGB-only; depth map interface retained but not used for SLAM | Moving outdoor monocular sequences | Waymo 9 segments; ICRA 2025 | Could be an outdoor monocular backend later. Need unbounded-scene pose/frame adapters. Poor fit for robot multi-camera target. | High | [14] |
| **S3PO-GS** | **No; outdoor monocular** | Outdoor monocular SLAM; retained GT depth input interface | Moving outdoor monocular vehicle-like sequences | Waymo, KITTI, DL3DV examples; ICCV 2025 | Similar to OpenGS-SLAM; useful for outdoor monocular baseline, not multi-camera. | High | [31] |
| **MonoGS** | **No; mono/RGB-D/stereo paths but no rig** | Monocular pipeline, RGB-D, experimental stereo, RealSense live demo | Single camera or fixed stereo/RGB-D stream | TUM-RGBD, Replica, EuRoC; CVPR 2024 Highlight; rendering metrics and headless evaluation | Strong baseline for single-camera 3DGS SLAM. For Mosaic, isolate as backend and use for baseline tests. Not appropriate as native multi-camera implementation. | High | [2] |
| **SplaTAM** | **No; RGB-D only** | Dense RGB-D SLAM; iPhone/LiDAR-equipped Apple device via NeRFCapture | Online RGB-D moving camera stream | Replica, TUM-RGBD, ScanNet, ScanNet++, Replica-V2; trajectory and rendering evaluation | Good single-RGB-D baseline. Need RGB-D observation adapter, depth conventions, and deterministic replay. No multi-camera support found. | High | [1] |
| **Gaussian-SLAM** | **No; single RGB-D style datasets** | Input path/dataset sequence; tested on Replica, TUM_RGBD, ScanNet, ScanNet++ | Single moving RGB-D/dataset stream | Replica, TUM_RGBD, ScanNet, ScanNet++; three-seed reporting; depth L1 needs mesh reconstruction | Single-camera dense SLAM baseline only. Need dataset adapter and output-map wrapper. | High | [7] |
| **Google Splat-SLAM / Splat-SLAM** | **No; RGB-only** | RGB-only SLAM with 3D Gaussians; single-camera keyframe tracker | Moving single RGB camera stream | Replica, TUM-RGBD, ScanNet; trajectory error, mesh accuracy/rendering metrics on Replica | Useful as RGB-only baseline. Needs pose/scale handling and evaluation wrapper. Not multi-camera. | High | [6], [24] |
| **WildGS-SLAM** | **No; monocular** | Monocular video sequence; custom data under `rgb/` with intrinsics | Single moving camera in dynamic/wild scenes | Wild-SLAM Mocap/iPhone, Bonn Dynamic, TUM RGB-D dynamic; ATE RMSE and NVS evaluation | Dynamic-scene monocular baseline. Not relevant for multi-camera rigs except as robustness reference. | High | [18] |
| **SGS-SLAM** | **No; RGB-D semantic** | RGB-D sequence with color/depth/semantic frames, poses, intrinsics | Single moving RGB-D camera stream | Replica, ScanNet, ScanNet++; ECCV 2024 semantic/object metrics | Could inform agent-semantic map contracts later. Not a multi-camera backend candidate. | High | [21] |
| **2DGS-SLAM** | **No; RGB-D** | RGB-D SLAM; RealSense D435i/D455 live; iPhone LiDAR via Stray Scanner | Single RGB-D stream | Replica, TUM RGB-D, ScanNet, Stray Scanner; tracking/reconstruction claims | Single RGB-D baseline. Potential RealSense live adapter; not multi-camera. | High | [23] |
| **VTGaussian-SLAM** | **No; RGB-D** | Paired color/depth streams, camera parameters; ScanNet/ScanNet++/Replica/TUM | Single RGB-D stream | Replica, TUM-RGBD, ScanNet, ScanNet++; ICML 2025; evaluation mode for rendering/tracking | Large-scale RGB-D backend candidate. Needs deterministic replay adapter. Not multi-camera. | High | [22] |
| **DG-SLAM** | **No; RGB-D + semantic motion masks** | RGB-D dynamic sequences; OneFormer semantic motion masks | Single moving RGB-D camera in dynamic scenes | TUM RGB-D dynamic, BONN Dynamic RGB-D, ScanNet; run scripts | Dynamic-scene baseline, not multi-camera. | High | [30] |
| **GSFusion** | **No; RGB-D mapping** | RGB-D mapping; dataset readers for Replica, ScanNet++, TUM; optional Kinect/OpenNI2 | Single RGB-D sensor mapping | Replica, ScanNet++, TUM-RGBD; automatic evaluation; RTX 3060 reported | Mapping/reconstruction candidate, not multi-camera SLAM. Need assess online tracking vs mapping scope before Mosaic integration. | Medium-high | [27] |
| **NeRF/3DGS SLAM in the Wild Benchmark** | **Benchmark, not backend; modality evidence includes mono/RGB-D/stereo** | Benchmark mentions D435i monocular/RGB-D, T265 stereo, Pi Cam; systems include MonoGS, Photo-SLAM, Splat-SLAM | Outdoor robot/wild visual SLAM benchmark context | ROVER dataset subset; benchmark compares classical and neural/3DGS SLAM systems; evaluation status noted as coming soon | Useful evaluation source for Mosaic regression scenarios across modalities, especially if ROVER data is accessible. Not an implementation backend. | Medium | [29] |

## Native vs adaptable vs poor fit

### Native candidates for multi-camera robot-mounted Mosaic target

1. **AgriGS-SLAM** — the only source found with explicit synchronized multi-camera robot-rig evidence: three synchronized RGB-D cameras on a tractor-mounted orchard platform, with LiDAR odometry/loop closure and real-time on-tractor claims. It should be treated as the primary native candidate to inspect further.

### Adaptable candidates, but not native general multi-camera

1. **RTG-SLAM** — strong because it documents ROS modes, stereo/RGB-D/mono, TF/external pose, KITTI, ZED2, Jetson, and evaluation scripts. Good for Mosaic backend boundaries and stream contracts, but stereo is not the same as an arbitrary multi-camera rig.
2. **Photo-SLAM** — practical open-source monocular/stereo/RGB-D system with ORB-SLAM3 lineage, EuRoC/TUM/Replica evidence, and RealSense demo. Good baseline for stereo/RGB-D but no documented synchronized multi-camera arrays.
3. **Gaussian-LIC, GS-LIVO, LVI-3DGS** — robotics-oriented LiDAR-inertial-camera systems. Excellent for Mosaic's future multi-sensor backend isolation, but evidence points to one camera plus LiDAR/IMU rather than multiple cameras.
4. **MM3DGS-SLAM** — useful robot dataset evidence via Jackal pose topic and RGB/depth/IMU/LiDAR streams, but still a single RGB/depth camera feed.
5. **VINGS-Mono and TRGS-SLAM** — useful for visual-inertial/thermal-inertial single-camera backends, not for multi-camera ingestion.
6. **MAGiC-SLAM** — relevant to multi-agent/multi-session map fusion; not a calibrated multi-camera rig solution.
7. **MonoRTGS/RTGS family** — may help for real-time/edge constraints; needs code inspection to separate real sensor support from inherited configs.

### Poor fit for the specific multi-camera question, but useful baselines

- **MonoGS, SplaTAM, Gaussian-SLAM, Google Splat-SLAM/Splat-SLAM, WildGS-SLAM, OpenGS-SLAM, S3PO-GS, SGS-SLAM, 2DGS-SLAM, VTGaussian-SLAM, DG-SLAM, GSFusion.** These are primarily monocular or single RGB-D sequence systems. Some are excellent single-sensor baselines and evaluation references, but should not be labeled multi-camera without additional documented loaders/configs.

## Benchmarks and datasets found relevant to multi-camera applicability

- **AgriGS-SLAM:** orchard dataset/demo; apple/pear orchards across dormancy, flowering, harvesting; standardized trajectory protocol for training-view reconstruction and novel-view synthesis; claims better rendering fidelity and trajectory accuracy than Photo-SLAM, Splat-SLAM, PINGS, OpenGS-SLAM; real-time on-tractor.
- **RTG-SLAM:** Replica, TUM RGB-D, KITTI; claims all 11 KITTI sequences completed without memory failures; evaluation scripts produce `log.txt` / `log.csv`; ZED2 ROS example and Jetson notes.
- **Photo-SLAM:** Replica, TUM RGB-D, EuRoC; separate evaluation toolkit; sequences run five times.
- **Gaussian-LIC:** FAST-LIVO, FAST-LIVO2, R3LIVE, MCD, M2DGR; ROS bag/config launch evidence.
- **GS-LIVO / LVI-3DGS:** MARS-LVIG, Landmark, UAV Playground, FAST-LIVO HKU; car/handheld/vehicle/edge demos; Jetson Orin NX and RTX 4090 evaluation context.
- **MM3DGS-SLAM:** UT-MM and TUM-RGBD; trajectory and image evaluation scripts; rosbag topics include Jackal pose.
- **NeRF/3DGS SLAM in the Wild Benchmark:** ROVER subset; D435i mono/RGB-D, T265 stereo, Pi Cam; compares MonoGS, Photo-SLAM, Splat-SLAM among broader methods. Evaluation status still marked coming soon in the fetched material.

## Mosaic adaptation implications

1. **Do not collapse stereo/RGB-D/multi-agent into multi-camera.** Mosaic should model `StereoObservation`, `RgbdObservation`, and `MultiViewObservation` distinctly, or at least carry enough metadata to prevent false equivalence.
2. **Require explicit rig calibration contracts.** A real Mosaic backend candidate for multiple robot-mounted cameras needs camera IDs, timestamp policy, extrinsics, frame conventions, pose direction, rolling/global shutter metadata where available, and missing-frame behavior.
3. **Backend isolation is mandatory.** Most candidates carry CUDA, ROS, C++ extensions, dataset folder conventions, non-deterministic rasterizers, and shell scripts. Mosaic should expose a pure-Python protocol and keep these implementations behind adapters/subprocess boundaries.
4. **Evaluation before integration:** Use small deterministic fixtures first: one monocular RGB sequence, one RGB-D sequence, one stereo sequence, and one synchronized multi-camera sequence if AgriGS-SLAM demo data can be normalized. Track trajectory ATE/RPE, rendering PSNR/SSIM/LPIPS where possible, splat count, runtime envelope, and crash/missing-frame behavior.
5. **AgriGS-SLAM deserves code-level follow-up.** Verify whether the three-camera support is hard-coded, whether input timestamps are truly synchronized, whether calibration is exposed cleanly, and whether camera poses are independently modeled or projected through a common vehicle/LiDAR trajectory.
6. **RTG-SLAM and Photo-SLAM are good baseline adapters.** They provide stereo/RGB-D coverage and evaluation datasets, useful to test Mosaic's typed contracts before tackling the heavier multi-camera agricultural/robotics stacks.

## Source list

1. SplaTAM repository, https://github.com/spla-tam/SplaTAM
2. MonoGS repository, https://github.com/muskie82/MonoGS
3. Photo-SLAM repository, https://github.com/HuajianUP/Photo-SLAM
4. Photo-SLAM evaluation toolkit, https://github.com/HuajianUP/Photo-SLAM-eval
5. ORB-SLAM3 repository, https://github.com/raulmur/ORB_SLAM3
6. Google Research Splat-SLAM repository, https://github.com/google-research/Splat-SLAM
7. Gaussian-SLAM repository, https://github.com/VladimirYugay/Gaussian-SLAM
8. MonoRTGS repository, https://github.com/Nemo0412/MonoRTGS
9. RTGS repository, https://github.com/UMN-ZhaoLab/RTGS
10. Gaussian-LIC repository, https://github.com/APRIL-ZJU/Gaussian-LIC
11. VINGS-Mono repository, https://github.com/Fudan-MAGIC-Lab/VINGS-Mono
12. MM3DGS-SLAM repository, https://github.com/VITA-Group/MM3DGS-SLAM
13. MAGiC-SLAM repository, https://github.com/VladimirYugay/MAGiC-SLAM
14. OpenGS-SLAM repository, https://github.com/3DAgentWorld/OpenGS-SLAM
15. 3D-Vision-World Awesome NeRF and 3DGS SLAM list, https://github.com/3D-Vision-World/awesome-NeRF-and-3DGS-SLAM
16. 3DGS SLAM GitHub search results via `gh search repos "Gaussian-SLAM"`, used only for discovery, https://github.com/search?q=Gaussian-SLAM&type=repositories
17. RTG-SLAM repository, https://github.com/MisEty/RTG-SLAM
18. WildGS-SLAM repository, https://github.com/GradientSpaces/WildGS-SLAM
19. AgriGS-SLAM repository, https://github.com/AIRLab-POLIMI/agri-gs-slam
20. AgriGS-SLAM README, https://github.com/AIRLab-POLIMI/agri-gs-slam/blob/main/README.md
21. SGS-SLAM repository, https://github.com/ShuhongLL/SGS-SLAM
22. VTGaussian-SLAM repository, https://github.com/MachinePerceptionLab/VTGaussian-SLAM
23. 2DGS-SLAM repository, https://github.com/PRBonn/2DGS-SLAM
24. Splat-SLAM repository, https://github.com/eriksandstroem/Splat-SLAM
25. GS-LIVO repository README, https://raw.githubusercontent.com/HKUST-Aerial-Robotics/GS-LIVO/main/README.md
26. LVI-3DGS repository, https://github.com/arclab-hku/LVI-3DGS
27. GSFusion repository, https://github.com/goldoak/GSFusion
28. TRGS-SLAM repository, https://github.com/umautobots/trgs_slam
29. NeRF and Gaussian Splatting SLAM in the Wild Benchmark repository, https://github.com/iis-esslingen/nerf-3dgs-benchmark
30. DG-SLAM repository, https://github.com/fudan-zvg/DG-SLAM
31. S3PO-GS repository, https://github.com/3DAgentWorld/S3PO-GS
