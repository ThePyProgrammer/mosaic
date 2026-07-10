# Top 10 Open-Source 3DGS SLAM Systems for Mosaic

## Ranking criteria

This comparison ranks open-source/public 3D Gaussian Splatting SLAM systems by usefulness for Mosaic backend planning, not by paper leaderboard score. The ranking weighs:

1. open implementation confidence,
2. license/reuse friendliness,
3. Mosaic modality fit,
4. online SLAM relevance,
5. benchmark evidence,
6. robotics relevance,
7. integration risk.

## Ranked top 10

| Rank | System | Why it ranks here | Modality | License / code status | Multi-camera relevance | Benchmark evidence | Caveats | Confidence |
|---:|---|---|---|---|---|---|---|---|
| 1 | **AgriGS-SLAM** | Best match to Mosaic's actual target: robot-mounted synchronized multi-camera 3DGS SLAM. | Three RGB-D cameras + LiDAR + GNSS/RTK/odometry | Public repo, Apache-2.0 | **Native multi-camera**: three synchronized RGB-D cameras and per-camera calibration | Orchard seasons, PSNR/SSIM/LPIPS/ATE, Photo-SLAM/Splat-SLAM/PINGS/OpenGS-SLAM baselines | Domain-specific orchard/tractor code; demo dataset only; heavy sensor assumptions | High |
| 2 | **SplaTAM** | Cleanest permissive RGB-D online 3DGS SLAM baseline for typed backend contracts. | RGB-D | Public repo, BSD-3-Clause | Not native multi-camera | Replica, TUM-RGBD, ScanNet, ScanNet++, Replica-V2 | Single RGB-D stream; CUDA/PyTorch dependency stack | High |
| 3 | **Gaussian-SLAM** | MIT-licensed dense RGB-D implementation useful for wrapper/protocol design. | RGB-D | Public repo, MIT | Not native multi-camera | Replica, TUM_RGBD, ScanNet, ScanNet++ | Online behavior should be source-inspected before serious adapter work | Medium-high |
| 4 | **MonoGS / Gaussian Splatting SLAM** | Most important monocular-first open implementation; supports RGB-D and experimental stereo paths. | Monocular, RGB-D, experimental stereo | Public repo, custom academic/non-commercial license risk | Adaptable stereo/RGB-D only | TUM RGB-D, Replica, EuRoC; ATE/rendering/runtime evidence | License and dependency risks; not a generic camera rig | High |
| 5 | **Photo-SLAM** | Strong practical real-time system across mono/stereo/RGB-D, including embedded/Jetson evidence. | Monocular, stereo, RGB-D | Public repo, GPLv3 | Strong stereo/RGB-D baseline, not arbitrary rig | Replica, TUM RGB-D, EuRoC; ATE, PSNR/SSIM/LPIPS, tracking/rendering FPS | GPL and heavy C++/CUDA/OpenCV/LibTorch stack; ORB-SLAM-style frontend | High |
| 6 | **RTG-SLAM** | Best real-time RGB-D stress/reference system from the benchmark evidence. | RGB-D | Public repo, GPL-3.0 | Not native multi-camera | Replica, TUM-RGBD, ScanNet++, Azure/self-collected RGB-D; runtime/memory/geometry | GPL; ORB-SLAM2/Pangolin/OpenCV dependency risk; RGB-D only | High |
| 7 | **Google Splat-SLAM** | Permissive RGB-only baseline with strong reconstruction/quality-runtime evidence. | RGB-only / monocular | Public repo, Apache-2.0; archived/read-only | Not native multi-camera | Replica, TUM-RGBD, ScanNet; ATE, PSNR/SSIM/LPIPS, runtime, Gaussian count | RGB-only depth/scale assumptions; not real-time-first | High |
| 8 | **DiskChunGS** | Most useful open large-scale/ROS/external-pose reference for robot-scale integration patterns. | Mono, stereo, RGB-D; ROS/external pose | Public repo; GPLv3 plus non-commercial third-party caveat | Adaptable stereo/ROS reference, not native rig | Replica, TUM RGB-D, KITTI; Jetson/KITTI claims | Young/complex repo; severe native dependency and license risk | Medium-high |
| 9 | **Gaussian-LIC** | Best open robotics multi-sensor reference: LiDAR-inertial-camera plus Gaussian map. | LiDAR + IMU + camera | Public repo; GPL-3.0 evidence | Multi-sensor robotics, not multi-camera | FAST-LIVO, FAST-LIVO2, R3LIVE, MCD, M2DGR | Singular camera evidence; ROS/C++/CUDA/TensorRT stack | Medium-high |
| 10 | **VINGS-Mono** | Public visual-inertial Gaussian SLAM code relevant to pose-source and calibration contracts. | Monocular + IMU | Public repo; no license visible in final check | Not native multi-camera | Hotel, Waymo, KITTI, KITTI360 | License unclear; not verified as native multi-camera or strongly real-time in final check | Medium |

## Comparison matrix

| Source | Key claim | Evidence type | Caveats | Confidence |
|---|---|---|---|---|
| AgriGS-SLAM | Only verified native robot-mounted multi-camera 3DGS SLAM candidate in the catalogue | Repo, dataset, paper, prior follow-up | Domain-specific orchard/tractor; full dataset not verified public | High |
| SplaTAM | Best permissive RGB-D online baseline | Public repo and project/paper evidence | Single RGB-D stream | High |
| Gaussian-SLAM | Useful MIT RGB-D dense SLAM baseline | Public repo | Online/incremental behavior should be confirmed in source before integration | Medium-high |
| MonoGS | Best monocular-first open Gaussian SLAM baseline | Public repo, paper benchmarks | Custom/non-commercial license risk; not native rig | High |
| Photo-SLAM | Strong real-time mono/stereo/RGB-D implementation | Public repo, paper benchmarks | GPLv3; heavy native stack; stereo is not arbitrary multi-camera | High |
| RTG-SLAM | Strong real-time RGB-D benchmark and implementation | Public repo, paper benchmarks | GPL; RGB-D only | High |
| Google Splat-SLAM | Strong permissive RGB-only reference | Public repo and paper evidence | Archived/read-only; RGB-only assumptions | High |
| DiskChunGS | Useful large-scale/ROS/external-pose robotics integration reference | Public repo | License/dependency complexity; not native multi-camera | Medium-high |
| Gaussian-LIC | Strong LiDAR-inertial-camera robotics reference | Public repo | Multi-sensor but not multi-camera; license/native stack risk | Medium-high |
| VINGS-Mono | Useful visual-inertial monocular reference | Public repo | License unclear; not native multi-camera | Medium |

## Agreement, disagreement, uncertainty

### Agreement

- The open-source landscape is strongest for RGB-D and monocular/stereo baselines, not arbitrary multi-camera robot rigs.
- AgriGS-SLAM is the only clearly native multi-camera robot-rig candidate found in the completed research.
- Real backends should be isolated from Mosaic core because most rely on CUDA, C++ extensions, ROS, ORB-SLAM variants, custom rasterizers, and bespoke datasets.

### Disagreement / corrections

- RTG-SLAM does have public code; earlier uncertainty was corrected.
- GS-SLAM has paper/project evidence and public modified rasterizer code, but a full public SLAM implementation was not confirmed, so it is not in the top 10 despite strong benchmark value.
- VIGS-SLAM and VINGS-Mono are different systems; VIGS-SLAM's linked code was inaccessible, while VINGS-Mono has public code.

### Uncertainty

- License implications need legal review before any code reuse.
- Some top-10 systems may be useful only as isolated subprocess/container backends, not Python imports.
- VINGS-Mono ranks tenth because it is public and robotics-relevant, but its license and online claims need deeper verification before adapter work.

## Sources

1. AgriGS-SLAM GitHub repository: https://github.com/AIRLab-POLIMI/agri-gs-slam
2. SplaTAM GitHub repository: https://github.com/spla-tam/SplaTAM
3. MonoGS GitHub repository: https://github.com/muskie82/MonoGS
4. Gaussian-SLAM GitHub repository: https://github.com/VladimirYugay/Gaussian-SLAM
5. Photo-SLAM GitHub repository: https://github.com/HuajianUP/Photo-SLAM
6. RTG-SLAM GitHub repository: https://github.com/MisEty/RTG-SLAM
7. Google Research Splat-SLAM repository: https://github.com/google-research/Splat-SLAM
8. DiskChunGS GitHub repository: https://github.com/leggedrobotics/DiskChunGS
9. Gaussian-LIC GitHub repository: https://github.com/APRIL-ZJU/Gaussian-LIC
10. VINGS-Mono GitHub repository: https://github.com/Fudan-MAGIC-Lab/VINGS-Mono
