# Multi-Robot / Multi-Agent Gaussian SLAM Paper Landscape

## 1. Executive summary

The target class is now real but still narrow: true online multi-agent Gaussian-map SLAM appears to be concentrated in a small 2024-2026 cluster around **MAGiC-SLAM**, **MAC-Ego3D**, **GRAND-SLAM**, **CoKo-SLAM**, **CoMA-SLAM**, **MAGS-SLAM**, and **MANG-SLAM**. The strongest target-class systems explicitly maintain local Gaussian/submap representations per agent and perform server-side or distributed loop closure, pose-graph/submap optimization, map merging, or Gaussian consensus into a shared/global reconstruction.

Highest-confidence target hits:

- **MAGiC-SLAM**: CVPR 2025, RGB-D multi-agent Gaussian SLAM, public code, agent/server architecture, map merging and loop closure.
- **MAC-Ego3D**: CVPR 2025/arXiv 2024, collaborative RGB-D ego-motion + photorealistic 3D reconstruction using shared 3D Gaussian map representation and intra/inter-agent Gaussian consensus, public code.
- **GRAND-SLAM**: RA-L 2025 / arXiv 2025, collaborative Gaussian-splatting SLAM for large-scale outdoor multi-agent settings with inter-/intra-robot loop closure.
- **CoKo-SLAM**: arXiv 2026, RGB-D multi-agent Gaussian Splatting SLAM focused on compact keyframe/submap communication and centralized merge/optimization, public code.
- **CoMA-SLAM**: AAAI 2026, distributed multi-agent 2D Gaussian-surfel SLAM with geometric consistency, distributed keyframe optimization, intra/inter-loop closure, and visible code repo.

Likely target/near-target but less fully verified:

- **MAGS-SLAM**: project page describes RGB-only monocular multi-agent 3DGS SLAM with compact summaries and occupancy-aware Gaussian fusion; under double-blind review with code/data promised after acceptance.
- **MANG-SLAM**: RA-L 2026 bibliographic record confirms multi-agent neural submap + Gaussian representation for dense mapping, but abstract/code details were not visible in available sources.
- **Collaborative Aerial-Ground SLAM System with Gaussian Splatting**: Springer/LNEE 2026 bibliographic hit for UAV/UGV-style aerial-ground collaboration; full abstract inaccessible through available fetch path, so classify as relevant but uncertain.

Many other 3DGS SLAM papers found in broad searches are adjacent only: single-agent RGB-D/monocular/stereo/dynamic/semantic Gaussian SLAM, static multi-view reconstruction, or multi-camera rigs. They should not pass the target gate unless they explicitly support multiple independently moving agents contributing to shared/fused Gaussian/neural maps.

## 2. Candidate table

| System | Year / venue | Sources | Target-class or adjacent | Sensor modality | Number/type of agents | Shared-map / fusion claim | Code status visible | Confidence |
|---|---:|---|---|---|---|---|---|---|
| MAGiC-SLAM: Multi-Agent Gaussian Globally Consistent SLAM | 2025 CVPR; arXiv submitted 2024-11-25 | [1], [2], [3], [4] | Target-class | RGB-D streams | Multiple simultaneously operating agents; no fixed count on project page; configs use ReplicaMultiagent and AriaMultiagent | Agent side keeps local submaps/trajectory; server stores features/submaps, detects loops, optimizes poses, and merges maps; paper claims tracking, map-merging, and loop-closure components for global consistency | Public GitHub, Python, active, 334 stars observed; license marked “Other” by GitHub | High |
| MAC-Ego3D: Multi-Agent Gaussian Consensus for Real-Time Collaborative Ego-Motion and Photorealistic 3D Reconstruction | 2025 CVPR per repo; arXiv submitted 2024-12-12 | [5], [6] | Target-class / strong adjacent if one requires SLAM naming | RGB-D datasets: Multi-Agent Replica and 7Scenes visible in README | Multi-agent cameras/robots; README shows Multi-Agent Replica agents | Uses parallel intra-agent and periodic inter-agent Gaussian consensus for real-time pose tracking and photorealistic reconstruction using a shared 3D Gaussian map representation | Public GitHub, C++, MIT, full code visible, 72 stars observed | High |
| GRAND-SLAM: Local Optimization for Globally Consistent Large-Scale Multi-Agent Gaussian SLAM | 2025 IEEE RA-L 10(12):13129-13136; arXiv submitted 2025-06-23 | [7], [8], [9] | Target-class | RGB-D is explicitly mentioned in arXiv summary; targets large-scale outdoor multi-agent environments | Multi-agent / inter- and intra-robot setting | Collaborative Gaussian-splatting SLAM with local tracking, local optimization over submaps, pose-graph loop closure, inter- and intra-robot loop closure | No code repo found in visible searches during this pass | High for paper; medium for implementation availability |
| CoKo-SLAM / Compact Keyframe-Optimized Multi-Agent Gaussian Splatting SLAM | 2026 arXiv, submitted 2026-04-01 | [10], [11], [12], [13] | Target-class | RGB-D; modes include rendered-depth and camera-depth | Multi-agent; README expects `n + 1` GPUs for n agents + server; evaluated on ReplicaMultiagent and AriaMultiagent | Agents send compact Gaussian/keyframe representations to central server for merge/optimization; compaction removes redundant Gaussians; centralized loop closure without initial pose guess; reports 85-95% lower transmitted data | Public GitHub `lemonci/coko-slam`, Python; repo license shown as Other; README says code based on MAGiC-SLAM. Also a separate RobotFlow-Labs scaffold exists, MIT, but runtime incomplete | High |
| RobotFlow-Labs/project_slam_coko | 2026 repo scaffold referencing arXiv:2604.00804 | [14] | Adjacent repository / implementation scaffold for CoKo-SLAM, not primary paper repo | Intended RGB-D Gaussian SLAM | Multi-agent | README: “SLAM-COKO — Multi-Agent Collaborative Gaussian Splatting SLAM”; status list says core tracker/mapper/runtime, loop closure, evaluation, ROS2 bridge are not yet done | Public GitHub, Python, MIT, 0 stars observed, scaffold/incomplete | Medium as source pointer; low as runnable system |
| CoMA-SLAM: Collaborative Multi-Agent Gaussian SLAM with Geometric Consistency | 2026 AAAI, vol. 40 no. 4, published 2026-03-14 | [15], [16] | Target-class | Not stated on AAAI page summary fetched; repo uses ReplicaMultiagent and AriaMultiagent | Multi-agent | Distributed multi-agent Gaussian SLAM using 2D Gaussian surfels, robust initialization, intra-/inter-loop closure, distributed keyframe optimization, submap-centric updates; claims 99.8% lower communication bandwidth than centralized methods | Public GitHub `npu-chenlin/CoMA-SLAM`, Python, no license visible, 2 stars observed | High for paper claim; medium-high for code because README is brief |
| MAGS-SLAM: Monocular Multi-Agent Gaussian Splatting SLAM for Geometrically and Photometrically Consistent Reconstruction | Under double-blind review; project page visible in 2026 search pass | [17], [18] | Target-class if page claims hold; not yet archival | RGB-only monocular; compares to RGB-D multi-agent Gaussian SLAM; datasets include ReplicaMultiAgent, ReplicaMultiAgent Plus, ETH3D, Tanks and Temples, 7-Scenes Fire | Multiple RGB-only monocular agents | Each robot builds local monocular Gaussian submaps and sends compact summaries; geometry/appearance loop checks plus occupancy-aware Gaussian fusion form coherent global map despite monocular scale ambiguity | Project page says “Code & Data (Released upon Acceptance)”; GitHub page repo only visible, no paper/code linked | Medium |
| MANG-SLAM: Multi-Agent Neural Submap and Gaussian Representation for Dense Mapping | 2026 IEEE RA-L 11(2):2242-2249; DOI issued 2025 | [19], [20] | Likely target-class / closely related | Not visible in accessible sources | Multi-agent | Title confirms multi-agent neural submap and Gaussian representation for dense mapping; no abstract visible from accessible sources | No repository found in GitHub search during this pass | Medium-low until abstract/PDF is retrieved |
| Collaborative Aerial-Ground SLAM System with Gaussian Splatting | 2026 chapter in LNEE / Proceedings of 2025 International Conference on Artificial Intelligence and Autonomous Transportation | [21], [22] | Likely target-class or adjacent target | Likely aerial-ground robotic sensors, but modality not visible | Collaborative aerial-ground agents, likely UAV + ground robot | Title directly claims collaborative aerial-ground SLAM with Gaussian Splatting; details inaccessible via Springer fetch due redirect/access path | No code found | Medium-low |
| Elonian/MultiAgent-GauassianSplat-SLAM | 2026 GitHub repository, not tied to visible paper | [23] | Adjacent / unofficial implementation-like repo; possible target-class code artifact | RGB-D and RGB-only via online MapAnything depth | README examples: Aria room0 with 3 agents; Replica scenes with 2 agents | Local 3D Gaussian submaps, compact descriptors, loop-aware pose graph optimization, corrected static/dynamic Gaussian merge, optional global refinement | Public GitHub, Python, MIT, 0 stars observed; typo in repo name; no paper citation visible | Medium as web/code signal; low as academic source |
| Gaussian Splatting SLAM / MonoGS | 2024 CVPR | [24] | Adjacent only | Single-agent RGB-D/monocular-style Gaussian SLAM family | Single agent | Foundational 3DGS SLAM; no multi-agent shared-map fusion target gate | Public code | High adjacent |
| GS-SLAM: Dense Visual SLAM with 3D Gaussian Splatting | 2024 CVPR | [25] | Adjacent only | RGB-D/dense visual SLAM | Single agent | Dense Gaussian SLAM but not collaborative/multi-agent | Public/visible in literature; not inspected here | High adjacent |
| CP-SLAM / ReplicaMultiagent dataset context | Prior multi-agent SLAM dataset source used by MAGiC/MAC/CoKo/CoMA; not itself necessarily Gaussian | [3], [5], [11], [16] | Context / benchmark adjacent | RGB-D multi-agent dataset | Multiple agents | Provides multi-agent data used by target systems; not itself a Gaussian fusion system in this report | Dataset links visible via HuggingFace/figshare references | Medium context |

## 3. Notes on systems likely relevant from prior context

### CoKo-SLAM

CoKo-SLAM is a strong target-class hit. The arXiv record for **Compact Keyframe-Optimized Multi-Agent Gaussian Splatting SLAM** says it is a multi-agent RGB-D Gaussian Splatting SLAM system for unknown environments with a central server that merges and optimizes local maps. It introduces compaction to remove redundant 3D Gaussians, central loop closure without an initial pose guess, and two sharing modes: rendered-depth and camera-depth. The fetched arXiv summary reports 85-95% less transmitted data than prior methods.

There are two visible repositories. The likely author repository is `lemonci/coko-slam`, whose README is a full runnable-style README and explicitly says the codebase is based on MAGiC-SLAM. GitHub metadata showed Python and license “Other.” A separate `RobotFlow-Labs/project_slam_coko` repository describes “SLAM-COKO — Multi-Agent Collaborative Gaussian Splatting SLAM” and links arXiv:2604.00804, but its README status checklist marks core tracker/mapper runtime, loop closure, evaluations, ROS2 bridge, API, and Docker runtime as not yet done. Treat RobotFlow as a scaffold or derivative project, not the primary code evidence.

### MAGS-SLAM

MAGS-SLAM is highly relevant by claim but lower confidence because it appears as an under-review project page rather than an archival paper. The project page title is **MAGS-SLAM: Monocular Multi-Agent Gaussian Splatting SLAM for Geometrically and Photometrically Consistent Reconstruction** and calls it “the first RGB-only multi-agent 3DGS SLAM framework.” It claims multiple agents build local monocular Gaussian submaps, communicate compact summaries, use geometry/appearance loop checks, and perform occupancy-aware Gaussian fusion into a coherent global map while handling monocular scale ambiguity. It lists ReplicaMultiAgent, ReplicaMultiAgent Plus, ETH3D, Tanks and Temples, and 7-Scenes Fire. Code/data are promised “Released upon Acceptance.” Until the paper or code appears, treat as target-class claim with medium confidence.

### GRAND-SLAM

GRAND-SLAM is a strong target-class paper. DBLP/Jonathan How publication page identify **GRAND-SLAM: Local Optimization for Globally Consistent Large-Scale Multi-Agent Gaussian SLAM** as IEEE RA-L 10(12):13129-13136 (2025), with an arXiv version `2506.18885`. The arXiv summary explicitly says prior multi-agent Gaussian splatting was mostly small indoor scenes and that GRAND-SLAM targets large-scale outdoor multi-agent environments using collaborative Gaussian-splatting SLAM, local tracking, local optimization over submaps, and inter-/intra-robot loop closure in a pose-graph setup. No code repository was found in this pass.

### MAGiC-SLAM

MAGiC-SLAM is the clearest public-code baseline for target-class multi-agent Gaussian SLAM. The CVPR OpenAccess page, arXiv, project page, and GitHub README agree on the title **MAGiC-SLAM: Multi-Agent Gaussian Globally Consistent SLAM**. The project page describes RGB-D streams, multiple simultaneously operating agents, a rigidly deformable 3D Gaussian scene representation, tracking, map merging, and loop closure. The README indicates evaluation on ReplicaMultiagent and AriaMultiagent and says the ideal setup needs `n + 1` GPUs for n agents plus a server. Code is public and active.

### MultiAgent-GaussianSplat-SLAM / project_slam_coko

`RobotFlow-Labs/project_slam_coko` is the GitHub result matching `project_slam_coko`; it is a scaffold around the CoKo-SLAM paper with several runtime tasks incomplete. It should not be conflated with the `lemonci/coko-slam` repository, which looks like the actual CoKo implementation and states it is based on MAGiC-SLAM.

A separate GitHub repository `Elonian/MultiAgent-GauassianSplat-SLAM` (note the misspelling “Gauassian”) is not connected to a visible paper but contains a long README describing a multi-agent RGB-D Gaussian Splatting SLAM pipeline: local Gaussian submaps, compact descriptors, loop candidate search, ICP validation, submap pose graph, corrected Gaussian merge, global refinement, dynamic/static map separation, and optional RGB-only depth via MapAnything. It reports Aria and Replica multi-agent result tables. Because there is no paper citation and no visible academic provenance, treat this as a web/code artifact for R2 follow-up rather than paper evidence.

### Additional collaborative Gaussian SLAM systems found

- **MAC-Ego3D**: important, possibly easy to miss because title emphasizes ego-motion/reconstruction rather than “SLAM.” GitHub topics include collaborative-slam and slam; README explicitly says shared 3D Gaussian map representation, intra-agent Gaussian consensus, and inter-agent Gaussian consensus.
- **CoMA-SLAM**: distributed multi-agent 2D Gaussian-surfel SLAM accepted/published at AAAI 2026. It is squarely relevant if “Gaussian maps” includes 2D Gaussian surfels and not just 3DGS radiance splats.
- **MANG-SLAM**: bibliographically confirmed as multi-agent neural submap and Gaussian dense mapping. Needs PDF/abstract follow-up to decide whether it is online SLAM with shared/fused maps or a denser mapping module adjacent to SLAM.
- **Collaborative Aerial-Ground SLAM System with Gaussian Splatting**: title-level relevant; likely aerial-ground robot collaboration, but insufficient details were visible.

## 4. Agreement / disagreement / uncertainty notes

1. **MAGiC-SLAM, GRAND-SLAM, CoKo-SLAM, CoMA-SLAM, and MAC-Ego3D pass the target gate** based on visible claims: multiple moving agents, online or SLAM-like operation, Gaussian/Gaussian-splat map representation, and global consistency via fusion/merging/consensus/pose graph/loop closure.
2. **MAGS-SLAM likely passes the target gate**, but current public evidence is a double-blind project page and no released code/paper. The claims are exactly on-target, especially RGB-only multi-agent Gaussian fusion, but should be marked provisional.
3. **MANG-SLAM likely belongs in the survey**, but available evidence was mostly bibliographic. The title is on-target; absence of visible abstract/source means the exact sensor modality, online nature, and fusion mechanism remain uncertain.
4. **CoKo-SLAM repository ambiguity matters**. The `lemonci/coko-slam` repo appears to be the actual codebase and cites/implements CoKo; `RobotFlow-Labs/project_slam_coko` is a scaffold with many unchecked runtime tasks. Reports should cite both only with this distinction.
5. **2D Gaussian surfel systems should be included if the scope says “Gaussian maps or closely related Gaussian/neural map representations.”** CoMA-SLAM uses 2D Gaussian surfels rather than conventional 3D Gaussian radiance splats. It is still a multi-agent Gaussian SLAM system with shared/distributed map optimization.
6. **MAC-Ego3D is target-class by function but may be labeled adjacent by strict naming.** It is not branded “SLAM” in the title, yet its repo topics include SLAM/collaborative-SLAM and the pipeline performs collaborative ego-motion plus reconstruction using a shared 3D Gaussian map. I would include it as target-class or at minimum “strong adjacent.”
7. **Static multi-view 3DGS training, single-agent 3DGS SLAM, dynamic-scene single-agent SLAM, semantic Gaussian SLAM, and multi-camera rigs are not enough.** These can inform architecture but should not count as target-class unless independent agents contribute to shared/fused Gaussian/neural maps.
8. **Source-access limits:** arXiv and Semantic Scholar frequently rate-limited; IEEE pages returned 418 for direct fetch; Springer redirected through identity management. Crossref, DBLP, GitHub CLI, CVF OpenAccess, project pages, and selected arXiv abstract pages provided the most useful evidence.

## 5. Numbered source list

1. MAGiC-SLAM project page: https://vladimiryugay.github.io/magic_slam
2. MAGiC-SLAM arXiv abstract: https://arxiv.org/abs/2411.16785
3. MAGiC-SLAM GitHub repository: https://github.com/VladimirYugay/MAGiC-SLAM
4. MAGiC-SLAM CVPR OpenAccess page: https://openaccess.thecvf.com/content/CVPR2025/html/Yugay_MAGiC-SLAM_Multi-Agent_Gaussian_Globally_Consistent__SLAM_CVPR_2025_paper.html
5. MAC-Ego3D GitHub repository: https://github.com/Xiaohao-Xu/MAC-Ego3D
6. MAC-Ego3D arXiv abstract: https://arxiv.org/abs/2412.09723
7. GRAND-SLAM arXiv abstract: https://arxiv.org/abs/2506.18885
8. GRAND-SLAM DOI / IEEE RA-L record: https://doi.org/10.1109/LRA.2025.3623026
9. GRAND-SLAM DBLP/publication-page record: https://dblp.org/rec/journals/ral/ThomasSRH25.html
10. CoKo-SLAM arXiv abstract: https://arxiv.org/abs/2604.00804
11. CoKo-SLAM author GitHub repository: https://github.com/lemonci/coko-slam
12. CoKo-SLAM GitHub clone URL in README: https://github.com/lemonci/Coko-SLAM.git
13. CoKo-SLAM arXiv DOI form: https://doi.org/10.48550/arXiv.2604.00804
14. RobotFlow-Labs SLAM-COKO repository: https://github.com/RobotFlow-Labs/project_slam_coko
15. CoMA-SLAM AAAI page: https://ojs.aaai.org/index.php/AAAI/article/view/37283
16. CoMA-SLAM GitHub repository: https://github.com/npu-chenlin/CoMA-SLAM
17. MAGS-SLAM project page: https://mags-slam.github.io/
18. MAGS-SLAM project-page GitHub repository: https://github.com/mags-slam/mags-slam.github.io
19. MANG-SLAM DOI / IEEE RA-L record: https://doi.org/10.1109/LRA.2025.3643274
20. MANG-SLAM DBLP record: https://dblp.org/rec/journals/ral/LiYJ26.html
21. Collaborative Aerial-Ground SLAM System with Gaussian Splatting DOI: https://doi.org/10.1007/978-981-95-8056-9_46
22. Collaborative Aerial-Ground SLAM Springer chapter URL: https://link.springer.com/10.1007/978-981-95-8056-9_46
23. Elonian MultiAgent-GauassianSplat-SLAM repository: https://github.com/Elonian/MultiAgent-GauassianSplat-SLAM
24. MonoGS / Gaussian Splatting SLAM GitHub repository: https://github.com/muskie82/MonoGS
25. GS-SLAM CVPR 2024 DOI: https://doi.org/10.1109/CVPR52733.2024.01853
