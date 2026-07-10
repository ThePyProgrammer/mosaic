# Benchmark Evidence for Online / Incremental 3D Gaussian Splatting SLAM

**Researcher:** R4 benchmark evidence extraction  
**Date:** 2026-05-18  
**Scope:** Benchmark-focused evidence for online/incremental 3D Gaussian Splatting (3DGS) SLAM systems and closely related open-source systems. This report emphasizes datasets, metrics, numbers, runtime/FPS, hardware, baselines, source type, and comparability caveats. It intentionally does not provide a broad repository inventory.

## Executive takeaways

1. **Most directly relevant open-source online 3DGS SLAM systems with benchmark evidence:** SplaTAM, MonoGS / Gaussian Splatting SLAM, GS-SLAM, Photo-SLAM, RTG-SLAM, and Splat-SLAM. Their benchmark regimes are mostly RGB-D or monocular/stereo single-rig SLAM, not synchronized multi-camera robot rigs.
2. **Common datasets:** Replica and TUM RGB-D dominate; ScanNet, ScanNet++, EuRoC MAV, Azure Kinect captures, and selected self-captured sequences appear in fewer papers.
3. **Common metrics:** tracking ATE RMSE in cm, rendering PSNR/SSIM/LPIPS, rendering FPS, system FPS, map/model size, GPU memory, depth L1, and geometry reconstruction metrics such as accuracy/completion/F1.
4. **Main comparability problem:** reported FPS can mean very different things: full online SLAM system FPS, tracking FPS, rendering-only FPS, or mapping iteration time. Rendering FPS numbers in the hundreds to thousands are not end-to-end SLAM FPS.
5. **Multi-camera robot gap:** none of the strongest open benchmark sources found provide a clean benchmark for multiple robot-mounted moving cameras with known extrinsics, synchronized multi-view observations, online 3DGS SLAM, and robot-scale motion. EuRoC stereo and Photo-SLAM stereo are closest, but stereo is not equivalent to arbitrary multi-camera rigs.

## Benchmark table

| System | Dataset | Metric | Reported value/range | Baselines compared | Runtime/hardware context | Source refs | Comparability caveat |
|---|---|---|---|---|---|---|---|
| SplaTAM | Replica | Tracking ATE RMSE, RGB-D SLAM | Paper/project claims up to 2x better performance; exact primary paper table values were not fully retrievable in this pass from the official page. RTG-SLAM reports SplaTAM as a baseline, but those are secondary values. | Nice-SLAM, Point-SLAM shown on project page; paper compares against neural/dense SLAM baselines. | Official project page did not expose FPS/hardware in extracted text. README says benchmarked with Python 3.10, Torch 1.12.1, CUDA 11.6; also tested with Torch 2.3.0/CUDA 12.1. | [1], [2], [3] | Use SplaTAM official paper tables for final decisions; extracted official page was qualitative. Secondary tables in RTG-SLAM are not a substitute for SplaTAM's own settings. |
| SplaTAM | ScanNet++ S1/S2 | Novel-view PSNR / train-view PSNR | Extracted paper appendix values: method novel-view PSNR avg 24.41 dB, S1 23.99, S2 24.84; train-view PSNR avg 27.98, S1 27.82, S2 28.14. 3DGS with GT poses novel-view avg 24.45; post-processed 3DGS avg 25.14. | 3DGS with GT poses, post-processed 3DGS. | Relative ablation only for time/memory: isotropic Gaussians 83.3% time and 57.5% memory versus anisotropic at 100%/100%. | [3] | ScanNet++ NVS protocol uses ground-truth poses only to align novel frames to map origin, not tracking; not directly comparable to online robot SLAM trajectory metrics. |
| SplaTAM | ScanNet++ S1 | Pose error / PSNR / relative cost ablation | Anisotropic: pose error 0.55 cm, train PSNR 28.11, novel PSNR 23.98, time 100%, memory 100%. Isotropic: pose error 0.57 cm, train PSNR 27.82, novel PSNR 23.99, time 83.3%, memory 57.5%. | Internal ablation only. | Relative time/memory, no absolute hardware/FPS in extracted table. | [3] | Ablation does not establish end-to-end runtime for SLAM; useful for representation-design tradeoff only. |
| MonoGS / Gaussian Splatting SLAM | TUM RGB-D | ATE RMSE in cm; monocular and RGB-D | TUM monocular no-loop average 3.96 cm across fr1/desk, fr2/xyz, fr3/office; RGB-D no-loop average 1.47 cm. Monocular with loop closure baselines ORB-SLAM2 1.60 cm, DROID-SLAM 1.70 cm; RGB-D with loop closure ORB-SLAM2 1.00 cm, BAD-SLAM 1.50 cm. | DSO, DROID-VO, DepthCov-VO, DROID-SLAM, ORB-SLAM2, iMAP, NICE-SLAM, DI-Fusion, Vox-Fusion, ESLAM, Co-SLAM, Point-SLAM, BAD-SLAM, Kintinuous. | Paper runtime hardware: Intel Core i9-12900K 3.50 GHz + RTX 4090. | [4], [5], [6] | Monocular ATE uses scale alignment; RGB-D ATE does not. Loop-closure and no-loop systems are separated but often casually compared. |
| MonoGS / Gaussian Splatting SLAM | Replica | ATE RMSE in cm, RGB-D SLAM | Multi-process avg 0.58 cm; single-process avg 0.32 cm across 8 Replica scenes. Baselines: iMAP avg 2.58, NICE-SLAM 1.07, Vox-Fusion 3.09, ESLAM 0.63, Point-SLAM 0.53. | iMAP, NICE-SLAM, Vox-Fusion, ESLAM, Point-SLAM. | Same RTX 4090 / i9-12900K paper setup. | [4], [5], [6] | Single-process vs multi-process differ significantly; report which one is used. Replica is synthetic and easier than robot field capture. |
| MonoGS / Gaussian Splatting SLAM | Replica | Rendering PSNR / SSIM / LPIPS / rendering FPS | Average rendering performance: Ours 38.94 / 0.968 / 0.070 / 769 FPS. NICE-SLAM 24.42 / 0.809 / 0.233 / 0.54 FPS; Vox-Fusion 24.41 / 0.801 / 0.236 / 2.17 FPS; Point-SLAM 35.17 / 0.975 / 0.124 / 1.33 FPS. | NICE-SLAM, Vox-Fusion, Point-SLAM. | Rendering-only forward pass at full resolution 1200x680. | [5] | Rendering FPS is not full online SLAM FPS. Point-SLAM uses ground-truth depth for rendering in some reported comparisons. |
| MonoGS / Gaussian Splatting SLAM | TUM fr3/office; Replica office1 | End-to-end runtime / FPS | TUM fr3/office: monocular 798.9 s, 3.2 FPS; RGB-D 986.7 s, 2.5 FPS. Replica office1 RGB-D: 1111.1 s, 1.8 FPS; RGB-D single-process 1904.7 s, 1.1 FPS. | Internal runtime analysis. | i9-12900K + RTX 4090. | [5] | End-to-end FPS is much lower than rendering FPS; use these for online feasibility, not the 769 FPS renderer number. |
| MonoGS / Gaussian Splatting SLAM | TUM RGB-D | Map memory | iMAP 0.8 MB; NICE-SLAM about 40.3 MB; Co-SLAM 6.4 MB; Ours mono 2.6 MB; Ours RGB-D 3.97 MB. | iMAP, NICE-SLAM, Co-SLAM. | Same paper setup. | [5] | Model-size accounting differs across neural fields vs Gaussian maps; not necessarily total process memory. |
| MonoGS / Gaussian Splatting SLAM | Live / project page | Runtime claim | Project abstract: runs live at 3 FPS. README speed-up branch reports up to 10 FPS on monocular fr3/office on RTX4090/i9-12900K. | Not a table. | RTX4090/i9-12900K for README speed-up claim; live demo with Intel RealSense D455. | [4], [6] | README speed-up branch claim is implementation-state evidence, not a peer-reviewed benchmark table. |
| GS-SLAM | Replica | ATE RMSE in cm | Average 0.50 cm across 8 scenes; range 0.33-0.70. Baselines: Point-SLAM 0.54, NICE-SLAM 1.06, Vox-Fusion 3.09, ESLAM 0.63, CoSLAM 1.00. | Point-SLAM, NICE-SLAM, Vox-Fusion, ESLAM, CoSLAM. | Python + PyTorch + CUDA; Intel i9-13900K @ 5.50 GHz + RTX 4090. Each method run 10 times and averaged. | [7] | Strong RGB-D/depth dependence; reported averages may include reproduced baseline runs under authors' setup. |
| GS-SLAM | TUM RGB-D | ATE in cm | Average 3.7 cm; fr1_desk 3.3, fr2_xyz 1.3, fr3_office 6.6. Baselines include ORB-SLAM2 1.0, BAD-SLAM 1.5, ElasticFusion 2.1, CoSLAM 2.4, ESLAM 2.0, Point-SLAM 2.4, iMAP 6.1, NICE-SLAM 13.3, Vox-Fusion 10.3. | ORB-SLAM2, BAD-SLAM, ElasticFusion, CoSLAM, ESLAM, Point-SLAM, iMAP, NICE-SLAM, Vox-Fusion. | i9-13900K + RTX 4090. | [7] | Traditional feature-based SLAM still outperforms GS-SLAM on TUM average; do not frame as universally best tracking. |
| GS-SLAM | Replica | Mesh quality | Avg Depth L1 1.16 cm, precision 74.00, recall 67.63, F1 70.15. Baseline avg Depth L1/F1: NICE-SLAM 2.97/43.86, Vox-Fusion 2.46/52.20, CoSLAM 2.59/69.74, ESLAM 2.08/78.29. | NICE-SLAM, Vox-Fusion, CoSLAM, ESLAM. | Same hardware. | [7] | Mesh extraction/evaluation from Gaussians vs implicit methods can differ; geometry metrics depend on extraction pipeline. |
| GS-SLAM | Replica | Rendering PSNR / SSIM / LPIPS / FPS | Avg 34.27 dB / 0.975 / 0.082 / 386.91 FPS. Baselines: NICE-SLAM 24.42 / 0.809 / 0.233 / 0.30 FPS; Vox-Fusion 24.41 / 0.801 / 0.236 / 3.88; CoSLAM 30.24 / 0.939 / 0.252 / 3.68; ESLAM 29.08 / 0.929 / 0.336 / 2.82. | NICE-SLAM, Vox-Fusion, CoSLAM, ESLAM. | i9-13900K + RTX 4090. | [7] | Rendering FPS is not full system FPS. Compare separately from tracking/mapping runtime. |
| GS-SLAM | Replica room0 / TUM RGB-D | System FPS, memory | Replica room0: tracking 11.9 ms x10, mapping 12.8 ms x100, system 8.34 FPS, scene memory 198.04 MB. TUM: fr1_desk 1.83 FPS / 40.8 MB / ATE 3.3; fr2_xyz 1.51 FPS / 48.4 MB / ATE 1.3. GS-SLAM light: fr1 1.92 FPS / 18.8 MB / ATE 4.3; fr2 1.68 FPS / 22.3 MB / ATE 2.7. | Point-SLAM, NICE-SLAM, Vox-Fusion, CoSLAM, ESLAM. | i9-13900K + RTX 4090. | [7] | Replica room0 system FPS and TUM FPS are not the same scenario; memory excludes or includes different model/runtime components depending on method. |
| RTG-SLAM | Replica Off0; Azure Home | Time, FPS, model size, memory | Ours Replica: tracking 0.02 s, mapping iteration 3.5 ms, mapping per frame 0.05 s, 17.24 FPS, model 71 MB, memory 2751 MB. Azure Home: 0.03 s, 4.3 ms, 0.05 s, 17.90 FPS, model 399 MB, memory 8782 MB. | NICE-SLAM, Co-SLAM, ESLAM, Point-SLAM, SplaTAM. | Intel i9-13900KF + RTX 4090; Azure Kinect sensor; Python/PyTorch + custom CUDA kernels. | [8] | RTG-SLAM is strongly optimized for runtime; compare against same resolution/settings and note that SplaTAM/ESLAM run OOM on Azure Home in this paper. |
| RTG-SLAM | TUM RGB-D | Tracking error in cm | fr1_desk 1.66, fr2_xyz 0.38, fr3_office 1.13, avg 1.06. Baselines: NICE-SLAM 13.28 avg, Co-SLAM 2.74, ESLAM 2.11, Point-SLAM 2.38, SplaTAM 3.39, ElasticFusion 2.07, ORB-SLAM2 1.00, BAD-SLAM 1.50. | NICE-SLAM, Co-SLAM, ESLAM, Point-SLAM, SplaTAM, ElasticFusion, ORB-SLAM2, BAD-SLAM. | i9-13900KF + RTX 4090. | [8] | ORB-SLAM2 remains slightly better on average; use RTG-SLAM mainly as a real-time 3DGS-SLAM benchmark. |
| RTG-SLAM | ScanNet++ | Geometry accuracy | Ours Acc 0.95, Acc Ratio 96.41, Comp 1.11, Comp Ratio 97.16. Baselines: NICE-SLAM 4.45/74.49/2.04/86.63; Co-SLAM 5.26/78.86/1.06/96.25; ESLAM 4.43/74.51/1.05/97.42; Point-SLAM 0.67/99.12/0.68/98.94; SplaTAM 1.32/95.31/1.54/93.55. | NICE-SLAM, Co-SLAM, ESLAM, Point-SLAM, SplaTAM. | i9-13900KF + RTX 4090. | [8] | Uses ground-truth camera poses for geometry to remove tracking effects; not a pure online tracking+mapping benchmark. |
| Photo-SLAM | Replica | ATE RMSE/STD, PSNR/SSIM/LPIPS, tracking/rendering FPS, GPU memory | Monocular desktop: 1.091 cm RMSE, PSNR 33.302, SSIM 0.926, LPIPS 0.078, tracking 41.646 FPS, rendering 911.262 FPS, 6 GB. RGB-D desktop: 0.604 cm, 34.958 / 0.942 / 0.059, tracking 42.485 FPS, rendering 1084.017 FPS, 5 GB. Jetson RGB-D: 0.581 cm, 31.978 / 0.916 / 0.101, tracking 17.926 FPS, rendering 116.395 FPS, 4 GB. | ORB-SLAM3, DROID-SLAM, BundleFusion, Nice-SLAM, ESLAM, Co-SLAM, Go-SLAM, Point-SLAM, Orbeez-SLAM. | Desktop RTX 4090 24 GB + i9-13900K + 64 GB; laptop RTX 3080 Ti + i9-12900HX; Jetson AGX Orin Dev Kit. | [9], [10], [11] | Tracking uses ORB-SLAM3-like front-end; rendering quality/speed comes from photorealistic Gaussian map. Some baselines lack photorealistic mapping so cells are blank. |
| Photo-SLAM | TUM RGB-D | ATE RMSE and rendering metrics | Monocular Ours RMSE fr1_desk/fr2_xyz/fr3_office: 1.539 / 0.984 / 1.257 cm; PSNR 20.972 / 21.072 / 19.591. RGB-D Ours RMSE 2.603 / 0.346 / 1.001 cm; PSNR 20.870 / 22.094 / 22.744. | ORB-SLAM3, DROID-SLAM, Go-SLAM, Nice-SLAM, ESLAM, Co-SLAM. | Same paper hardware platforms; supplementary runtime table reports desktop tracking FPS 39.6-81.6 and rendering FPS 754.7-2016.7; Jetson tracking 17.5-36.7, rendering 80.0-380.6. | [11] | TUM rendering metrics are lower than Replica due to real sensor data; not directly comparable to synthetic Replica PSNR. |
| Photo-SLAM | EuRoC MAV stereo | ATE RMSE and rendering metrics | Ours RMSE 4.109 / 4.441 / 8.821 / 26.609 cm across selected sequences; PSNR 13.952 / 14.201 / 17.069 / 15.677; SSIM 0.420 / 0.430 / 0.618 / 0.622; LPIPS 0.366 / 0.356 / 0.266 / 0.323. | ORB-SLAM3, DROID-SLAM for ATE; rendering metrics blank for baselines. | Supplementary platform breakdown: desktop tracking FPS 44.8-48.9, rendering 595.2-835.1; Jetson tracking 21.3-23.9, rendering 94.0-106.0; laptop tracking 25.0-27.6, rendering 307.0-367.9. | [11] | Stereo EuRoC is the closest open benchmark to moving robot-mounted multi-camera, but it is a calibrated stereo pair, not arbitrary multi-view rigs. Rendering scores are hard to compare because baselines lack photorealistic maps. |
| Photo-SLAM | Replica | Ablation / model size | Default Mono: PSNR 33.302, rendering 911.3 FPS, 31.419 MB. Default RGB-D: PSNR 34.958, rendering 1084.0 FPS, 35.211 MB. | Internal ablations and 3DGS variants. | Same desktop platform. | [11] | These are map/rendering ablations, not full online SLAM FPS; Table 5 3DGS comparison uses Photo-SLAM keyframes/poses and same training duration. |
| Splat-SLAM | Replica, RGB-only | PSNR / SSIM / LPIPS / ATE RMSE | Table 1 average over 8 scenes: Ours 36.45 / 0.95 / 0.06 / 0.35 cm. Baselines: GO-SLAM 22.13 / 0.73 / ATE 0.39; NICER-SLAM 25.41 / 0.83 / 0.19 / 1.88; Photo-SLAM 33.30 / 0.93 / ATE 1.09; MonoGS 31.22 / 0.91 / 0.21 / 14.54; GlORIE-SLAM 31.04 / 0.91 / 0.12 / 0.35; Q-SLAM 32.49 / 0.89 / 0.17. | GO-SLAM, NICER-SLAM, MoD-SLAM, Photo-SLAM, MonoGS, GlORIE-SLAM, Q-SLAM. | Main experiments on NVIDIA A100; runtime benchmark on AMD Ryzen Threadripper Pro 3945WX + RTX 3090 Ti 24 GB. | [12] | RGB-only system; uses monocular depth estimator, so geometry quality depends on depth prediction. Some compared systems marked with asterisks have special settings. |
| Splat-SLAM | ScanNet | Rendering PSNR / SSIM / LPIPS | Average: Ours 29.48 / 0.85 / 0.18; GO-SLAM 14.84 / 0.42 / 0.60; MonoGS 18.79 / 0.71 / 0.59; GlORIE-SLAM 22.45 / 0.85 / 0.30. | GO-SLAM, MonoGS, GlORIE-SLAM. | A100 for main experiments. | [12] | ScanNet rendering from RGB-only SLAM; no mesh ground truth for reconstruction in their reported caveat. |
| Splat-SLAM | ScanNet / TUM RGB-D | Tracking ATE RMSE | ScanNet Table S9 averages: Ours 7.6 cm, GO-SLAM 7.7, HI-SLAM 7.4, GlORIE-SLAM 7.6. TUM Table S10 averages: Ours 1.1 cm, GO-SLAM 1.2, GlORIE-SLAM 1.1. | GO-SLAM, HI-SLAM, GlORIE-SLAM. | Main experiments on A100. | [12] | Authors state some tracking numbers reuse GlORIE-SLAM tracking framework; isolate mapping vs tracking contributions. |
| Splat-SLAM | Replica / TUM / ScanNet | Full summaries | Replica: depth L1 2.41 cm, reconstruction accuracy 2.43 cm, completion 3.64 cm, completion ratio 84.69%, PSNR 36.45, SSIM 0.95, LPIPS 0.06, full-traj ATE 0.34 cm, avg Gaussians 102k. TUM: depth L1 15.78 cm, PSNR 25.85, SSIM 0.84, LPIPS 0.19, ATE 2.05 cm, avg Gaussians 133k. ScanNet: depth L1 11.37 cm, PSNR 29.32, SSIM 0.84, LPIPS 0.19, ATE 7.58 cm, avg Gaussians 123k. | Full evaluation summary. | A100 / RTX 3090 Ti runtime context. | [12] | Replica only has ground-truth meshes for full reconstruction evaluation; ScanNet/TUM lack comparable mesh GT in this paper. |
| Splat-SLAM | Replica room0 | Runtime-quality tradeoff | Default keyframe params: PSNR 32.25, depth L1 2.90 cm, 1.24 FPS. Faster settings: 1.45 FPS with PSNR 31.65; 2.02 FPS with PSNR 30.59; 3.67 FPS with PSNR 27.59. | MonoGS note: default PSNR 26.12, render depth L1 17.38 cm. | Runtime machine: Threadripper Pro 3945WX + RTX 3090 Ti 24 GB; final refinement 2K iterations about 15 s. | [12] | This is online RGB-only SLAM with optional final refinement; FPS/quality tradeoff should be compared at matched keyframe policy. |

## System notes and evidence interpretation

### SplaTAM

SplaTAM is a key CVPR 2024 RGB-D online dense SLAM baseline using 3D Gaussians. The official project page exposes qualitative claims and links to code/paper, while the README exposes benchmark scripts for Replica, TUM-RGBD, ScanNet, ScanNet++, and Replica-V2 but not benchmark tables. Extracted paper appendix evidence includes ScanNet++ NVS and Gaussian-distribution ablations. RTG-SLAM uses SplaTAM as a baseline and reports SplaTAM runtime/memory/geometry numbers, but those should be treated as secondary evidence for SplaTAM itself.

Best use for Mosaic: SplaTAM is important as a canonical online 3DGS-SLAM design and baseline, but Mosaic should prefer primary SplaTAM paper tables when locking benchmark gates.

### MonoGS / Gaussian Splatting SLAM

MonoGS has strong paper-level benchmark evidence for both monocular and RGB-D modes. The most important distinction is between rendering-only speed and end-to-end online speed: the paper reports 769 FPS rendering on Replica, but end-to-end fr3/office runtime is 3.2 FPS monocular and 2.5 FPS RGB-D on RTX 4090/i9-12900K. The project README also reports a speed-up branch reaching up to 10 FPS on monocular fr3/office on RTX4090/i9-12900K.

Best use for Mosaic: useful for separating `tracking`, `mapping`, `rendering`, `memory`, and `snapshot quality` metrics in evaluation artifacts.

### GS-SLAM

GS-SLAM has clear tables for Replica/TUM tracking, Replica mesh quality, rendering metrics/FPS, system FPS, and memory. It reports 8.34 FPS on Replica room0 with 198.04 MB scene memory, but TUM FPS is lower at about 1.5-1.8 FPS in the reported sequences. It is RGB-D/depth-dependent and explicitly notes high memory use for larger scenes.

Best use for Mosaic: good source for system-FPS-versus-render-FPS separation, plus depth/mesh reconstruction metrics.

### RTG-SLAM

RTG-SLAM is the strongest extracted evidence for real-time end-to-end 3DGS-SLAM speed: about 17 FPS on Replica Off0 and Azure Home on RTX 4090/i9-13900KF, with large but bounded memory numbers. It also provides a useful larger-scene Azure Home stress case where some baselines run out of memory. Its ScanNet++ geometry benchmark deliberately uses ground-truth poses to remove tracking effects, so it should be classified as geometry-only rather than online SLAM performance.

Best use for Mosaic: useful upper target for real-time online RGB-D evaluation, memory stress tests, and separating tracking-free geometry quality from full SLAM quality.

### Photo-SLAM

Photo-SLAM has broad benchmark coverage: monocular, RGB-D, and stereo; Replica, TUM RGB-D, EuRoC; desktop, laptop, and Jetson AGX Orin. It reports high tracking FPS and rendering FPS, including Jetson results. However, it uses a strong feature-based SLAM front-end and a photorealistic Gaussian map, so it is not the cleanest example of a fully Gaussian tracking/mapping system.

Best use for Mosaic: important embedded/robotics runtime baseline and closest evidence for stereo moving-camera operation, but not evidence for arbitrary multi-camera 3DGS-SLAM.

### Splat-SLAM

Splat-SLAM is useful because it focuses on RGB-only SLAM and reports rich reconstruction/rendering/tracking summaries, average Gaussian counts, and runtime-quality tradeoffs. It reports high Replica rendering quality but online FPS around 1.24 FPS at default settings on Replica room0, rising to 3.67 FPS only with substantial PSNR/depth degradation. It relies on monocular depth, and some tracking setup is inherited from GlORIE-SLAM.

Best use for Mosaic: benchmark source for RGB-only 3DGS mapping and for designing explicit quality-speed tradeoff gates.

## Benchmarks most useful for Mosaic evaluation design

1. **Replica synthetic regression suite**
   - Why: repeated across SplaTAM, MonoGS, GS-SLAM, Photo-SLAM, RTG-SLAM, and Splat-SLAM.
   - Metrics to copy into Mosaic artifacts: ATE RMSE cm, PSNR, SSIM, LPIPS, depth L1, rendering FPS, end-to-end FPS, model/map size, GPU memory, number of Gaussians.
   - Caveat: synthetic scenes underrepresent robot sensor noise, rolling shutter, exposure variation, dynamic obstacles, and rig calibration error.

2. **TUM RGB-D tracking sanity suite**
   - Why: common real RGB-D benchmark with traditional SLAM baselines; exposes that feature-based systems can still beat 3DGS systems in trajectory accuracy.
   - Metrics: ATE RMSE cm, per-sequence and average; report mono scale-alignment status separately from RGB-D.
   - Caveat: mostly single RGB-D camera; not representative of multi-camera robots.

3. **EuRoC stereo for robot-motion / stereo-rig smoke testing**
   - Why: Photo-SLAM reports stereo EuRoC results; EuRoC is closer to robot-mounted moving-camera setups than Replica/TUM.
   - Metrics: ATE RMSE, rendering PSNR/SSIM/LPIPS if photometric mapping is available.
   - Caveat: stereo pair is still not multi-camera surround or quadruped body-mounted camera array.

4. **ScanNet / ScanNet++ geometry and NVS tests**
   - Why: SplaTAM, RTG-SLAM, and Splat-SLAM use these for geometry/NVS stress.
   - Metrics: accuracy/completion ratios, depth L1, train/novel PSNR, SSIM, LPIPS.
   - Caveat: some protocols use ground-truth poses or ground-truth depth for rendering/alignment; classify as mapping-only or geometry-only, not full SLAM.

5. **Runtime decomposition benchmark**
   - Why: papers report incompatible speed notions.
   - Mosaic should store separate fields for:
     - input FPS / sequence rate,
     - tracking time per frame,
     - mapping time per keyframe or per iteration,
     - end-to-end online FPS,
     - rendering-only FPS,
     - final-refinement time,
     - GPU model and memory.
   - Use MonoGS, GS-SLAM, RTG-SLAM, Photo-SLAM, and Splat-SLAM as templates for what to record.

6. **Memory and map-size gates**
   - Why: GS-SLAM, RTG-SLAM, Photo-SLAM, and Splat-SLAM show that map size, model size, and GPU memory can diverge dramatically.
   - Mosaic should separately record:
     - serialized map/snapshot size,
     - Gaussian count,
     - resident GPU memory,
     - peak process memory,
     - optional backend-specific model/decoder parameters.

## Benchmark gaps for multi-camera robots

1. **No clean open benchmark found for arbitrary multi-camera robot-mounted online 3DGS SLAM.** Existing evidence mostly covers monocular, RGB-D, or stereo. Multi-view in these papers usually means frames over time, not multiple synchronized cameras on a moving robot.
2. **Stereo is not enough.** Photo-SLAM on EuRoC provides useful stereo evidence, but a quadruped/UGV/humanoid rig may have non-overlapping FOVs, asynchronous camera clocks, different exposure/noise, and nontrivial body-frame extrinsics.
3. **Rig calibration/extrinsic uncertainty is not benchmarked.** Papers generally assume known camera parameters and do not evaluate degradation under extrinsic drift, temporal offsets, or per-camera rolling-shutter effects.
4. **Robot motion regimes are underrepresented.** Replica/TUM/ScanNet do not cover legged locomotion vibration, rapid yaw, height changes, motion blur, or uneven timestamp cadence.
5. **Dynamic and outdoor settings are weakly covered.** EuRoC and some self-captured Photo-SLAM demos help, but there is little benchmark evidence for multi-camera outdoor robotic mapping with 3DGS SLAM.
6. **Agent-facing uncertainty/provenance metrics are absent.** None of the benchmark tables evaluate posterior uncertainty calibration, provenance of Gaussians by camera/time/source, confidence summaries, or bounded query quality for downstream agents.
7. **Cross-system numbers are fragile.** Rendering metrics may exclude keyframes or train views; ATE may use scale alignment for monocular but not RGB-D; geometry metrics may use GT poses; FPS may be renderer-only; hardware ranges from A100 to RTX 4090 to Jetson.

## Recommended Mosaic benchmark schema fields

For each future Mosaic benchmark artifact, record:

- `dataset`, `scene`, `sensor_mode` (`mono`, `stereo`, `rgbd`, `multi_camera_rgb`, `multi_camera_rgbd`), `num_cameras`, `camera_ids`, `rig_extrinsics_source`.
- `trajectory_metric`: ATE RMSE, RPE if available, alignment mode, scale correction yes/no.
- `rendering_metrics`: PSNR, SSIM, LPIPS, train-vs-novel split, whether keyframes/training frames are excluded.
- `geometry_metrics`: depth L1, accuracy, completion, completion ratio, precision/recall/F1, mesh/sampling method.
- `runtime`: tracking ms/frame, mapping ms/iteration, mapping ms/frame/keyframe, end-to-end FPS, rendering FPS, final-refinement time.
- `memory`: serialized map size, Gaussian count, model size, GPU memory, peak RAM.
- `hardware`: CPU, GPU, VRAM, embedded platform if any, CUDA/PyTorch versions.
- `baseline_context`: which baselines were run by the authors vs copied from papers; number of runs; mean/std.
- `comparability_notes`: GT poses/depth used, scale alignment, loop closure status, online vs offline/final refinement, single-process vs multi-process.

## Source list

1. SplaTAM project page: https://spla-tam.github.io/
2. SplaTAM GitHub README: https://github.com/spla-tam/SplaTAM
3. SplaTAM arXiv HTML / paper evidence: https://arxiv.org/html/2312.02126 and abstract metadata https://arxiv.org/abs/2312.02126
4. MonoGS / Gaussian Splatting SLAM project page: https://rmurai.co.uk/projects/GaussianSplattingSLAM/
5. MonoGS / Gaussian Splatting SLAM arXiv HTML / paper evidence: https://arxiv.org/html/2312.06741
6. MonoGS GitHub README: https://github.com/muskie82/MonoGS
7. GS-SLAM arXiv HTML / paper evidence: https://arxiv.org/html/2311.11700
8. RTG-SLAM arXiv HTML / paper evidence: https://arxiv.org/html/2404.19706
9. Photo-SLAM project page: https://huajianup.github.io/research/Photo-SLAM/
10. Photo-SLAM GitHub README: https://github.com/HuajianUP/Photo-SLAM
11. Photo-SLAM arXiv HTML / paper evidence: https://arxiv.org/html/2311.16728
12. Splat-SLAM arXiv HTML / paper evidence: https://arxiv.org/html/2405.16544
