# Multi-Robot / Multi-Agent Online Gaussian SLAM Follow-up: Code, License, and Target-Class Verification

## 1. Executive summary of corrections

This targeted follow-up changes the first-round picture in several important ways:

1. **MAC-Ego3D should be treated as target-class, not merely adjacent, if the survey gate is functional rather than title-based.** The arXiv abstract describes a multi-agent framework in which each agent builds local maps and inter-agent consensus asynchronously aligns/optimizes/fuses them into a global model, and the repository is public with MIT license and full code visible. Sources: https://arxiv.org/abs/2412.09723, https://github.com/Xiaohao-Xu/MAC-Ego3D.
2. **CoMA-SLAM is a real public code candidate, but license is unresolved.** The AAAI page says it is a distributed multi-agent Gaussian SLAM framework using 2D Gaussian surfels, distributed keyframe optimization, submap-centric updates, and intra-/inter-loop closure; the GitHub repository is public and contains implementation-looking code under `CoMA-SLAM/`, but GitHub reports no repository license and no root LICENSE file exists. Sources: https://ojs.aaai.org/index.php/AAAI/article/view/37283, https://github.com/npu-chenlin/CoMA-SLAM.
3. **HAMMER is target-class by architecture claims, but its code is not publicly auditable from the current project page/GitHub searches.** The arXiv page calls it a server-based collaborative Gaussian Splatting method for heterogeneous multi-robot/device streaming data; the project page says code was “coming June 2025” with only a placeholder link, and GitHub searches for the title/arXiv did not find a repo. Sources: https://arxiv.org/abs/2501.14147, http://hammer-project.github.io.
4. **MAGS-SLAM remains promised-only.** The project page claims RGB-only monocular multi-agent 3DGS SLAM with compact submap summaries, loop verification, and occupancy-aware Gaussian fusion, but it says “Paper under double-blind review” and “Code & Data (Released upon Acceptance)”; the public GitHub org/repo found is website-only with no license. Sources: https://mags-slam.github.io/, https://github.com/mags-slam/mags-slam.github.io.
5. **MANG-SLAM is bibliographically real but not code-verifiable.** DBLP confirms the RA-L entry and DOI, but no arXiv result or GitHub repository was found in exact searches, and IEEE direct fetch was blocked. Classify it as likely target-class or near-target based on title only, with low confidence for implementation details. Sources: https://dblp.org/rec/journals/ral/LiYJ26.html, https://doi.org/10.1109/LRA.2025.3643274.
6. **Do not conflate code license with website/paper license.** HAMMER’s project website is Creative Commons BY-SA 4.0, but that is not a software license for implementation code. MAGS-SLAM’s website repo has no license metadata. CoMA-SLAM’s vendored `thirdparty/gsplat` has a license file, but the top-level CoMA-SLAM repository lacks one.

## 2. Verification table

| System | Target-class verdict | Code URL/status | License | Modality | Online/shared map fusion evidence | Benchmark/code maturity evidence | Confidence |
|---|---|---|---|---|---|---|---|
| MAC-Ego3D | **Target-class** for multi-agent online Gaussian reconstruction/ego-motion; “SLAM” appears in repo topics/positioning even though title says ego-motion/reconstruction. | Public repo: https://github.com/Xiaohao-Xu/MAC-Ego3D. GitHub metadata observed: public, not archived, 72 stars, 3 forks, created 2024-12-12, updated 2026-03-30. Tree includes `mac_ego.py`, `mac_Mapper.py`, `mac_Tracker.py`, `configs/`, `requirements.txt`, `Dockerfile`, `eval_utils/`, renderer/model/util folders, and run scripts. | MIT per GitHub license metadata and root LICENSE: https://raw.githubusercontent.com/Xiaohao-Xu/MAC-Ego3D/main/LICENSE. Note vendored/submodule components may carry their own licenses. | RGB-D is explicit in arXiv/repo; README references Multi-Agent Replica and 7Scenes RGB-D datasets. | arXiv says each agent builds/aligns/refines local maps; intra-agent consensus keeps nearby Gaussians coherent; inter-agent consensus asynchronously aligns/optimizes maps and merges them into a global model. Repo README says shared 3D Gaussian map representation, intra-agent Gaussian consensus, and inter-agent Gaussian consensus. | Full code visible, Dockerfile, requirements, configs, benchmark scripts for 7Scenes and Multi-Agent Replica, 15 commits, no releases. Research-code maturity: usable-looking but CUDA/3DGS-heavy, not a library dependency. | High |
| CoMA-SLAM | **Target-class**, with caveat that it uses **2D Gaussian surfels** rather than conventional 3D Gaussian radiance splats. | Public repo: https://github.com/npu-chenlin/CoMA-SLAM. GitHub metadata observed: public, not archived, 2 stars, 0 forks, created 2025-07-29, updated 2026-05-09. Implementation code is nested under `CoMA-SLAM/`, including `run_slam.py`, `run_visualization.py`, configs, `src/entities/coma_slam.py`, `coma_slam_server.py`, `agent.py`, `mapper.py`, `tracker.py`, `pose_graph_adapter.py`, loop-detection modules, LCM message definitions, and `thirdparty/gsplat`. | **No top-level license found.** GitHub license metadata is null and root `LICENSE` lookup returned 404. A vendored `thirdparty/gsplat/LICENSE` exists, but that does not license the whole repo. | AAAI page does not name a sensor modality in the fetched summary; it explicitly says Gaussian scene representation and 2D Gaussian surfels. Repo configs target `ReplicaMultiagent` and `AriaMultiagent`; previous README fetch did not explicitly list RGB/depth sensors. | AAAI page says distributed multi-agent Gaussian SLAM, robust initialization, geometric consistency, distributed keyframe optimization, submap-centric updates, and intra-/inter-loop closure; it avoids sending data to a central server. Repo has server/agent implementation-looking modules despite paper emphasis on distributed operation. | Early public release: 1 commit from README fetch, 2 stars/0 forks, no releases visible. It has runnable-looking scripts/configs and a `requirements.txt`, but no visible tests/CI. AAAI page claims synthetic and real-world tests and 99.8% lower communication bandwidth. | High for paper target-class; medium-high for code maturity/license because repo is small and unlicensed |
| HAMMER | **Target-class** by architecture claims: heterogeneous multi-robot semantic Gaussian Splatting, server-based collaborative mapping, shared metric-semantic map. | Project page: http://hammer-project.github.io. arXiv: https://arxiv.org/abs/2501.14147. Code link on project page was a placeholder `/` with text “Code (coming June 2025)”. GitHub searches for `"HAMMER" "Gaussian Splatting"` and `"2501.14147"` returned no repositories in fetched result pages. | No software license found because no code repo found. Project website text is Creative Commons Attribution-ShareAlike 4.0 International, but that applies to site content, not implementation code. | ArXiv/project page emphasize heterogeneous robots/devices and mixed perception modes; exact sensor list was not visible in fetched project-page text. ArXiv says asynchronous robot data streams and mixed image preprocessing/perception modes. | arXiv says server-based collaborative Gaussian Splatting, ROS-style communication, asynchronous robot data streams, frame alignment into a shared global frame, online semantic 3DGS training, and no prior initial robot positions. Project page says real-time shared metric-semantic map with coverage from the full robot team. | No public implementation maturity can be audited. arXiv says real-world experiments and about 2x higher-fidelity maps than baselines; fetched project page did not expose named datasets/benchmark tables. | High for target-class paper/page; low for code availability |
| MAGS-SLAM | **Claimed target-class**, but provisional until paper/code release. | Project page: https://mags-slam.github.io/. Public repo found: https://github.com/mags-slam/mags-slam.github.io, but it is website-only (`index.html`, `scripts`, `static`), public, 0 stars, 0 forks, created 2026-05-03. Project page says “Paper under double-blind review” and “Code & Data (Released upon Acceptance)”. | No implementation license found. Website repo GitHub license metadata is null. | RGB-only / monocular is the core claim. Page contrasts against RGB-D methods and says it works only from RGB images; benchmark text also mentions monocular RGB-only or RGB-D streams and ground-truth poses. | Page claims local monocular Gaussian submaps, compact submap summaries instead of raw observations/dense maps, geometry- and appearance-aware loop verification, occupancy-aware Gaussian fusion, and globally fused reconstruction with per-agent trajectories. | No install/run evidence. Page names ReplicaMultiAgent Plus, ReplicaMultiAgent, ETH3D, Tanks and Temples, and 7-Scenes Fire, but no auditable implementation or paper URL was visible. | Medium for target-class claim; high for “no released implementation”; low for implementation details |
| MANG-SLAM | **Likely target-class / near-target**, but evidence is mostly bibliographic and title-level. | No code/project found. DBLP entry: https://dblp.org/rec/journals/ral/LiYJ26.html. DOI: https://doi.org/10.1109/LRA.2025.3643274. Exact GitHub search for `MANG-SLAM` returned no repositories; arXiv search for `MANG-SLAM` returned no results. IEEE page fetch returned HTTP 418, so abstract/details were not retrieved. | No software license found. | Not visible from accessible sources. | Title says “Multi-Agent Neural Submap and Gaussian Representation for Dense Mapping,” implying multi-agent submaps and Gaussian representation, but no accessible abstract/code was found to verify online fusion mechanics. | Bibliographic record: IEEE Robotics and Automation Letters 11(2):2242-2249, 2026; authors Yonghao Li, Ping Ye, Qingxuan Jia; DOI 10.1109/LRA.2025.3643274. No implementation maturity evidence. | Medium for bibliographic existence; low for architecture/code details |

## 3. Corrections to first-round reports

### MAC-Ego3D

- Correction: If the earlier report hedged MAC-Ego3D as “strong adjacent,” this follow-up supports marking it **target-class** for the practical Mosaic survey scope. The paper/repo directly cover multi-agent collaborative ego-motion plus photorealistic 3D reconstruction using a shared Gaussian map and inter-agent consensus; that is exactly the shared-map online Gaussian SLAM cluster even if “SLAM” is not in the paper title. Sources: https://arxiv.org/abs/2412.09723, https://github.com/Xiaohao-Xu/MAC-Ego3D.
- Correction: Code is not merely promised; it is public and MIT-licensed. GitHub inspection found root `LICENSE`, `Dockerfile`, `requirements.txt`, configs, renderer/model/util modules, `mac_ego.py`, `mac_Mapper.py`, and `mac_Tracker.py`. Source: https://github.com/Xiaohao-Xu/MAC-Ego3D.
- Integration note: Treat as a runnable research backend candidate, not a clean dependency. It includes 3DGS/CUDA-style submodules and a large vendored DINOv2/SIBR footprint.

### CoMA-SLAM

- Correction: CoMA-SLAM should not be listed as closed or unavailable. A public GitHub repository exists at https://github.com/npu-chenlin/CoMA-SLAM and contains runnable-looking source under `CoMA-SLAM/`.
- Correction: CoMA-SLAM’s license should be recorded as **unknown/unlicensed at repository top level**, not MIT/open-source by assumption. GitHub metadata is null and no root LICENSE file was found; only vendored third-party licenses were visible.
- Correction: The architecture is distributed, not just centralized multi-agent. The AAAI page says it avoids sending data to a central server and uses distributed keyframe optimization, submap-centric updates, and intra-/inter-loop closure. Source: https://ojs.aaai.org/index.php/AAAI/article/view/37283.
- Scope note: It uses 2D Gaussian surfels. Include it if the target class covers Gaussian map representations broadly; distinguish from 3DGS radiance-splat systems.

### HAMMER

- Correction: HAMMER should be included in the narrow cluster as a target-class **paper/project-page** candidate because it is explicitly heterogeneous multi-robot collaborative Gaussian Splatting with shared metric-semantic mapping. Sources: https://arxiv.org/abs/2501.14147, http://hammer-project.github.io.
- Correction: Do **not** mark HAMMER implementation as open/public based on the project page. The code link is a placeholder and says “coming June 2025”; GitHub searches found no repository by title/arXiv. License for code is unknown.
- Scope note: HAMMER adds semantic/open-vocabulary mapping via CLIP-style scene semantics, so it is especially relevant to Mosaic’s future agent-facing posterior APIs, but code cannot be audited yet.

### MAGS-SLAM

- Correction: MAGS-SLAM remains **promised-only**; do not classify it as open-source. The only public repo found is website source, not implementation code. Sources: https://mags-slam.github.io/, https://github.com/mags-slam/mags-slam.github.io.
- Correction: It is a claimed target-class monocular/RGB-only system, not RGB-D-first. The page explicitly says first RGB-only multi-agent 3DGS SLAM and relies only on RGB images.
- Scope note: Treat its benchmark/dataset claims as project-page claims until archival paper/code appears.

### MANG-SLAM

- Correction: MANG-SLAM was not omitted incorrectly as nonexistent; it is bibliographically real in RA-L. Source: https://dblp.org/rec/journals/ral/LiYJ26.html.
- Correction: However, it should not be represented as open-source or implementation-verified. No exact GitHub or arXiv result was found, and IEEE details were not accessible through the fetch path.
- Scope note: Keep it in the survey with low architecture/code confidence until an abstract/PDF/project page is available.

## 4. Source list with direct URLs

1. MAC-Ego3D GitHub repository: https://github.com/Xiaohao-Xu/MAC-Ego3D
2. MAC-Ego3D root LICENSE: https://raw.githubusercontent.com/Xiaohao-Xu/MAC-Ego3D/main/LICENSE
3. MAC-Ego3D requirements file: https://raw.githubusercontent.com/Xiaohao-Xu/MAC-Ego3D/main/requirements.txt
4. MAC-Ego3D Dockerfile: https://raw.githubusercontent.com/Xiaohao-Xu/MAC-Ego3D/main/Dockerfile
5. MAC-Ego3D arXiv abstract: https://arxiv.org/abs/2412.09723
6. MAC-Ego3D paper PDF: https://arxiv.org/pdf/2412.09723
7. CoMA-SLAM GitHub repository: https://github.com/npu-chenlin/CoMA-SLAM
8. CoMA-SLAM README: https://github.com/npu-chenlin/CoMA-SLAM/blob/main/README.md
9. CoMA-SLAM requirements file: https://raw.githubusercontent.com/npu-chenlin/CoMA-SLAM/main/CoMA-SLAM/requirements.txt
10. CoMA-SLAM AAAI article page: https://ojs.aaai.org/index.php/AAAI/article/view/37283
11. CoMA-SLAM DOI: https://doi.org/10.1609/aaai.v40i4.37283
12. CoMA-SLAM dataset link from README: https://figshare.com/s/a7b7dd3de48cde905bab
13. CoMA-SLAM vendored gsplat license path: https://raw.githubusercontent.com/npu-chenlin/CoMA-SLAM/main/thirdparty/gsplat/LICENSE
14. HAMMER arXiv abstract: https://arxiv.org/abs/2501.14147
15. HAMMER arXiv HTML: https://arxiv.org/html/2501.14147v2
16. HAMMER arXiv PDF: https://arxiv.org/pdf/2501.14147
17. HAMMER project page: http://hammer-project.github.io
18. MAGS-SLAM project page: https://mags-slam.github.io/
19. MAGS-SLAM website repository: https://github.com/mags-slam/mags-slam.github.io
20. MANG-SLAM DBLP record: https://dblp.org/rec/journals/ral/LiYJ26.html
21. MANG-SLAM DOI: https://doi.org/10.1109/LRA.2025.3643274
22. MANG-SLAM IEEE landing page: https://ieeexplore.ieee.org/document/11297803/
23. MANG-SLAM Unpaywall lookup: https://unpaywall.org/10.1109%2FLRA.2025.3643274
24. Exact GitHub search checked for MANG-SLAM: https://github.com/search?q=%22MANG-SLAM%22&type=repositories
25. Exact arXiv search checked for MANG-SLAM: https://arxiv.org/search/?query=%22MANG-SLAM%22&searchtype=all
26. GitHub search checked for HAMMER Gaussian Splatting: https://github.com/search?q=%22HAMMER%22+%22Gaussian+Splatting%22&type=repositories
27. GitHub search checked for HAMMER arXiv ID: https://github.com/search?q=%222501.14147%22&type=repositories

## 5. Bottom-line classification for Mosaic backend planning

- **Auditable public implementation candidates:** MAC-Ego3D, CoMA-SLAM. MAC-Ego3D has the cleaner license signal; CoMA-SLAM has a top-level license gap.
- **Target-class but not code-auditable yet:** HAMMER, MAGS-SLAM, MANG-SLAM.
- **Most relevant to Mosaic contracts:** CoMA-SLAM for distributed submap/keyframe optimization and low communication; MAC-Ego3D for Gaussian consensus; HAMMER for heterogeneous robots and semantic/agent-facing shared maps; MAGS-SLAM for monocular multi-agent fusion; MANG-SLAM for neural submap/Gaussian dense mapping once details are accessible.
- **Recommended handling:** keep all as optional research-backend references behind protocols/process boundaries; do not import or vendor their runtime code into Mosaic core.
