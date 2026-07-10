# Multi-Robot / Multi-Agent Online Gaussian SLAM Follow-up: Architecture Cross-check

## 1. Executive summary of confirmed target-class systems

This follow-up cross-check confirms that the strongest target-class systems for multi-robot or multi-agent online Gaussian SLAM / Gaussian mapping are:

1. **HAMMER: Heterogeneous, Multi-Robot Semantic Gaussian Splatting** — confirmed target-class. It is explicitly multi-robot / heterogeneous, server-based, online / streaming, and builds a shared 3D metric-semantic Gaussian Splatting map. Its key architectural feature is a frame-alignment module that maps local SLAM poses and images from robots into a shared global frame without prior relative pose knowledge.
2. **GRAND-SLAM: Local Optimization for Globally Consistent Large-Scale Multi-Agent Gaussian SLAM** — confirmed target-class, but the first-round report should not describe it with CoKo-SLAM's rendered-depth / camera-depth centralized loop-closure modes. GRAND-SLAM is RGB-D multi-agent 3DGS SLAM with local submap optimization, inter- and intra-robot loop closure, and pose-graph optimization for global consistency. The arXiv page does not prove a central server architecture.
3. **CoKo-SLAM / Compact Keyframe-Optimized Multi-Agent Gaussian Splatting SLAM** — confirmed target-class. It is multi-agent RGB-D Gaussian Splatting SLAM with a centralized server that merges and optimizes local maps, compacts redundant 3D Gaussians, and supports loop closure without an initial guess. Its rendered-depth and camera-depth modes belong to CoKo-SLAM, not GRAND-SLAM.
4. **MAGS-SLAM: Monocular Multi-Agent Gaussian Splatting SLAM** — confirmed target-class from arXiv evidence. It is RGB-only / monocular multi-agent 3DGS SLAM, uses local monocular Gaussian submaps and compact submap summaries, and performs geometry- and appearance-aware loop verification plus occupancy-aware Gaussian fusion. The page does not explicitly establish central vs distributed deployment, so classify fusion location as collaboration layer / not fully resolved.
5. **MAC-Ego3D** — should be elevated from doubtful / adjacent to at least near-target, and arguably target-class if the definition includes collaborative ego-motion plus mapping rather than only papers titled “SLAM.” It is real-time multi-agent collaborative ego-motion and 3D reconstruction with a unified Gaussian splat representation, intra-agent and inter-agent Gaussian consensus, asynchronous cross-agent map alignment, and a public repository. It is not merely static reconstruction.

Not confirmed as target-class from primary-source checks:

- **CoMA-SLAM** — no arXiv primary result found for exact “CoMA-SLAM” or “CoMA SLAM Gaussian” queries. Do not classify as target-class unless a direct paper/project URL is provided.
- **MANG-SLAM** — no arXiv primary result found for exact “MANG-SLAM” or “MANG Gaussian SLAM” queries. Do not classify as target-class unless a direct paper/project URL is provided.

## 2. Architecture classification table

| System | True / near / adjacent | Agents | Modality | Fusion timing | Fusion location | Shared representation | Pose / alignment assumptions | Evidence URLs | Confidence |
|---|---|---:|---|---|---|---|---|---|---|
| HAMMER: Heterogeneous, Multi-Robot Semantic Gaussian Splatting | True | Multiple heterogeneous robots / devices; exact count not fixed on page | Images plus local SLAM poses; heterogeneous / mixed sensing and preprocessing. Project page says wide range of robots and sensing devices; arXiv abstract emphasizes robot data streams and local SLAM outputs | Online / streaming / real-time | Centralized / server-based collaborative mapping per arXiv page; ROS-style communication implied by source extraction | Shared 3D metric-semantic Gaussian Splatting map with CLIP / open-vocabulary semantic codes | No prior initial robot positions and no prior relative pose knowledge; frame-alignment module maps local SLAM frames into a shared global frame; depends on local SLAM poses | https://arxiv.org/abs/2501.14147 ; http://hammer-project.github.io | High for multi-robot, server, online, semantic 3DGS, no-prior-alignment claims; medium for exact sensor modalities |
| GRAND-SLAM: Local Optimization for Globally Consistent Large-Scale Multi-Agent Gaussian SLAM | True | Multi-agent / multi-robot; exact count not fixed on page | RGB-D visual SLAM | Online / incremental SLAM implied by tracking and local optimization over submaps | Not proven centralized from arXiv page. Architecture is submap + pose-graph global consistency with inter- and intra-robot loop closure | 3D Gaussian Splatting / Gaussian reconstruction via multi-agent dense SLAM; local submaps | Alignment through inter- and intra-robot loop closures feeding pose-graph optimization. No explicit prior relative pose requirement stated on page | https://arxiv.org/abs/2506.18885 ; https://arxiv.org/html/2506.18885v1 | High for multi-agent RGB-D 3DGS SLAM and loop-closure/pose-graph claims; medium for deployment/fusion-location details |
| CoKo-SLAM / Compact Keyframe-Optimized Multi-Agent Gaussian Splatting SLAM | True | Multi-agent; exact count not fixed on page/repo summary | RGB-D; rendered-depth-only mode and camera-depth mode using lightweight depth images | Incremental SLAM / local map production with centralized loop closure and optimization; exact update schedule not fully specified on arXiv page | Centralized server merges and optimizes local maps | 3D Gaussian maps; compacted 3D Gaussians; keyframe-optimized Gaussian Splatting representation | Loop closure without initial guess. Camera-depth mode improves registration; compaction removes redundant Gaussians | https://arxiv.org/abs/2604.00804 ; https://github.com/lemonci/coko-slam | High for central server, RGB-D, 3D Gaussian map, loop closure without initial guess; medium for online timing details |
| MAC-Ego3D | Near / true depending on strictness. True for multi-agent online Gaussian mapping + ego-motion; near if requiring paper title to say SLAM | Multi-agent; repo supports multiple agents via `agent_ids` | RGB-D in repository/dataset evidence; arXiv page references efficient RGB-D rendering | Real-time / online; agents independently construct, align, and iteratively refine local maps | Distributed / consensus-based. Parallelized Inter-Agent Gaussian Consensus asynchronously aligns and optimizes local maps; no single central mapper indicated in arXiv extraction | Unified Gaussian splat representation / shared 3D Gaussian map representation | Intra-Agent Gaussian Consensus enforces local coherence; Inter-Agent Gaussian Consensus handles cross-agent alignment and global integration; loop-closure support indicated in repository via SALAD weights | https://arxiv.org/abs/2412.09723 ; https://github.com/Xiaohao-Xu/MAC-Ego3D | High for multi-agent, real-time, Gaussian consensus, public repo; medium for whether to label as SLAM rather than collaborative ego-motion + reconstruction |
| MAGS-SLAM: Monocular Multi-Agent Gaussian Splatting SLAM | True | Multi-agent; exact count not fixed on page | Monocular RGB-only; explicitly without active depth sensors | Incremental local mapping and collaborative fusion implied by local submap construction and loop verification | Collaboration layer not fully resolved from arXiv page. Page does not name a central server; evidence points to compact exchange and fusion of submap summaries | Local monocular Gaussian submaps; compact submap summaries; fused 3DGS reconstruction | Explicitly addresses monocular scale ambiguity; geometry- and appearance-aware loop verification; occupancy-aware Gaussian fusion | https://arxiv.org/abs/2605.10760 ; https://arxiv.org/html/2605.10760v1 | High for monocular multi-agent 3DGS SLAM and submap/fusion claims; medium for central-vs-distributed deployment |
| CoMA-SLAM | Not confirmed / exclude until source provided | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | ArXiv exact search no result: https://arxiv.org/search/?query=%22CoMA-SLAM%22&searchtype=all ; broad arXiv search no result: https://arxiv.org/search/?query=%22CoMA%22+%22SLAM%22+%22Gaussian%22&searchtype=all | Low. No primary source found in this pass |
| MANG-SLAM | Not confirmed / exclude until source provided | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | ArXiv exact search no result: https://arxiv.org/search/?query=%22MANG-SLAM%22&searchtype=all ; broad arXiv search no result: https://arxiv.org/search/?query=%22MANG%22+%22Gaussian%22+%22SLAM%22&searchtype=all | Low. No primary source found in this pass |

## 3. Corrections to the first-round architecture report

### 3.1 HAMMER wording

Correct wording:

- HAMMER is a **server-based / centralized collaborative semantic 3D Gaussian Splatting mapper** for heterogeneous multi-robot systems.
- It uses **asynchronous robot data streams**, **local SLAM poses**, and images / perception outputs from heterogeneous devices.
- It builds a shared **3D metric-semantic Gaussian map**, including semantic codes for language/open-vocabulary querying.
- Its critical target-class feature is **global frame alignment without prior relative pose knowledge**.

Avoid overclaiming:

- Do not describe HAMMER primarily as a loop-closure / pose-graph optimization system unless quoting a source that says so. The primary evidence surfaced here emphasizes frame alignment, server-based online training, local SLAM pose streams, and semantic 3DGS map construction.
- The project page alone did not mention central server details in the fetched text, but the arXiv page did. Cite the arXiv page for server-based claims.

### 3.2 GRAND-SLAM wording

Correct wording:

- GRAND-SLAM is **multi-agent RGB-D 3D Gaussian SLAM** for globally consistent large-scale mapping.
- Its distinctive architecture is **local optimization over submaps** plus **inter- and intra-robot loop closure** in a **pose-graph optimization framework**.
- It should be described as a submap / pose-graph global-consistency system unless the full paper proves a stronger centralized-server architecture.

Correction:

- The first-round statement that GRAND-SLAM is “centralized multi-agent RGB-D Gaussian SLAM” with “rendered-depth or camera-depth alignment” appears to mix GRAND-SLAM with CoKo-SLAM. The rendered-depth / camera-depth loop-closure modes are CoKo-SLAM evidence, not GRAND-SLAM evidence from the arXiv abstract page.

### 3.3 CoKo-SLAM wording

Correct wording:

- CoKo-SLAM is the system with the **centralized server** that **merges and optimizes local maps**.
- It is RGB-D multi-agent Gaussian Splatting SLAM with **map compaction** to remove redundant 3D Gaussians.
- It supports **loop closure without an initial guess**.
- It has two alignment/loop-closure variants: **pure rendered-depth mode** and **camera-depth mode** using lightweight depth images.

Correction:

- If the first-round report used “Compact Keyframe-Optimized Multi-Agent Gaussian Splatting SLAM” without naming it CoKo-SLAM, align the names: the GitHub repository is `lemonci/coko-slam`, and the arXiv title is “Compact Keyframe-Optimized Multi-Agent Gaussian Splatting SLAM.”

### 3.4 MAC-Ego3D target-class status

Correction:

- MAC-Ego3D should not be dismissed as merely adjacent static reconstruction. The primary arXiv and repository evidence describe **real-time multi-agent collaboration for ego-motion and high-fidelity 3D reconstruction**, a **unified Gaussian splat representation**, **Intra-Agent Gaussian Consensus**, and **Inter-Agent Gaussian Consensus** that asynchronously aligns and optimizes local maps across agents.
- If the research taxonomy requires the title or abstract to explicitly say “SLAM,” mark MAC-Ego3D as **near target-class**.
- If the taxonomy is functional — multiple moving agents, online localization/ego-motion, shared Gaussian-map alignment/fusion — mark MAC-Ego3D as **target-class or target-class-adjacent with high relevance**.

Recommended classification: **Near / true depending on strictness**, with high architectural relevance.

### 3.5 CoMA-SLAM status

Correction:

- CoMA-SLAM should **not** be target-class from this follow-up evidence. Exact arXiv searches for “CoMA-SLAM” and broader “CoMA SLAM Gaussian” produced no results. It may be a typo, unpublished work, renamed work, or confusion with another acronym.
- Do not use it in the confirmed target-class set unless a direct paper, project page, or repository URL is supplied.

### 3.6 MANG-SLAM status

Correction:

- MANG-SLAM should **not** be target-class from this follow-up evidence. Exact arXiv searches for “MANG-SLAM” and broader “MANG Gaussian SLAM” produced no results.
- Do not use it in the confirmed target-class set unless a direct primary source is supplied.

### 3.7 MAGS-SLAM status

Correction:

- MAGS-SLAM should remain target-class. It directly claims to be a **Monocular Multi-Agent Gaussian Splatting SLAM** framework and, from the arXiv page, explicitly covers local monocular Gaussian submaps, compact submap summaries, geometry- and appearance-aware loop verification, monocular scale ambiguity, and occupancy-aware Gaussian fusion.
- The unresolved detail is not target-class status; it is **fusion deployment location**. The arXiv page evidence does not conclusively say central server vs fully distributed.

## 4. Source list with direct URLs

### Confirmed / high-value primary sources

1. HAMMER: Heterogeneous, Multi-Robot Semantic Gaussian Splatting — arXiv: https://arxiv.org/abs/2501.14147
2. HAMMER project page: http://hammer-project.github.io
3. GRAND-SLAM: Local Optimization for Globally Consistent Large-Scale Multi-Agent Gaussian SLAM — arXiv: https://arxiv.org/abs/2506.18885
4. GRAND-SLAM arXiv HTML: https://arxiv.org/html/2506.18885v1
5. CoKo-SLAM / Compact Keyframe-Optimized Multi-Agent Gaussian Splatting SLAM — arXiv: https://arxiv.org/abs/2604.00804
6. CoKo-SLAM repository: https://github.com/lemonci/coko-slam
7. MAC-Ego3D — arXiv: https://arxiv.org/abs/2412.09723
8. MAC-Ego3D repository: https://github.com/Xiaohao-Xu/MAC-Ego3D
9. MAGS-SLAM: Monocular Multi-Agent Gaussian Splatting SLAM — arXiv: https://arxiv.org/abs/2605.10760
10. MAGS-SLAM arXiv HTML: https://arxiv.org/html/2605.10760v1

### Negative / source-availability checks

11. CoMA-SLAM exact arXiv search: https://arxiv.org/search/?query=%22CoMA-SLAM%22&searchtype=all&abstracts=show&order=-announced_date_first&size=50
12. CoMA + SLAM + Gaussian arXiv search: https://arxiv.org/search/?query=%22CoMA%22+%22SLAM%22+%22Gaussian%22&searchtype=all&abstracts=show&order=-announced_date_first&size=50
13. MANG-SLAM exact arXiv search: https://arxiv.org/search/?query=%22MANG-SLAM%22&searchtype=all&abstracts=show&order=-announced_date_first&size=50
14. MANG + Gaussian + SLAM arXiv search: https://arxiv.org/search/?query=%22MANG%22+%22Gaussian%22+%22SLAM%22&searchtype=all&abstracts=show&order=-announced_date_first&size=50

## 5. Bottom-line classification for downstream planning

Use this confirmed set for Mosaic architecture planning:

- **Central / server shared-map pattern:** HAMMER, CoKo-SLAM.
- **Submap + pose-graph consistency pattern:** GRAND-SLAM.
- **Monocular compact-submap collaborative fusion pattern:** MAGS-SLAM.
- **Distributed Gaussian consensus pattern:** MAC-Ego3D.

Do not use these as confirmed systems without more evidence:

- CoMA-SLAM.
- MANG-SLAM.
