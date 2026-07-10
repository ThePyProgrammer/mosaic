# SLAM Algorithm-Flow Ordering and Lineage Review

Date: 2026-05-22

## 1. Current algorithm order in the draft

The draft's method-level order in `research/slam-survey/main.tex` is:

1. MAGiC-SLAM
2. MAC-Ego3D
3. CoKo-SLAM
4. CoMA-SLAM
5. HAMMER
6. GRAND-SLAM
7. MAGS-SLAM

The current order is not strictly chronological and not strictly dependency-first. It starts with two public RGB-D baselines representing centralized/server and consensus architectures, then covers compact communication, distributed Gaussian-surfel optimization, heterogeneous semantic mapping, large-scale submap/pose-graph consistency, and monocular RGB-only collaboration. The appendix then expands shared survey operators: RGB-D Gaussian tracking, RGB-D submap tracking, MAC-Ego3D tracking, MAGS-SLAM monocular tracking, CoKo keyframe selection, local mapping/update selection, cross-agent alignment, and global fusion.

The draft already makes one explicit lineage claim in the algorithm flow: CoKo-SLAM uses MAGiC-SLAM-style tracking and the appendix describes CoKo-SLAM's tracker as inherited from MAGiC-SLAM. The local notes and public CoKo-SLAM repository also support that specific relationship.

## 2. Evidence table

| method | local draft position | modality/architecture | direct sources inspected | explicit lineage/dependency evidence | ordering implication |
|---|---:|---|---|---|---|
| MAGiC-SLAM | 1 | RGB-D multi-agent Gaussian SLAM; agent/server architecture; local Gaussian submaps, loop detection, pose-graph optimization, global map merge | CVPR OpenAccess page; MAGiC-SLAM GitHub; local draft and bibliography; local research notes | GitHub README says tracking/mapping pieces are based on Gaussian-SLAM and credits GraphSLAM as an external component. This is explicit lineage to non-surveyed components, not to another method among the seven surveyed algorithms. | Reasonable first baseline. It is the earliest public, mature multi-agent Gaussian SLAM anchor among the surveyed methods and is the parent for CoKo-SLAM's code/tracker lineage. |
| MAC-Ego3D | 2 | RGB-D multi-agent collaborative ego-motion and photorealistic reconstruction; distributed/intra-agent and inter-agent Gaussian consensus | arXiv abstract page; MAC-Ego3D GitHub; local draft and bibliography; local research notes | No explicit dependency on MAGiC-SLAM, CoKo-SLAM, CoMA-SLAM, HAMMER, GRAND-SLAM, or MAGS-SLAM found. Repository lists external technical dependencies such as gaussian rasterization, simple-knn, fast_gicp, loop-closure weights, and datasets, but not surveyed-method lineage. | Can remain near MAGiC-SLAM as a contrasting public RGB-D baseline. No dependency reason forces it after any surveyed method. |
| CoKo-SLAM | 3 | RGB-D multi-agent Gaussian Splatting SLAM; centralized server; compact keyframe/Gaussian communication, compaction, no-initial-guess loop closure | arXiv abstract page; CoKo-SLAM GitHub; local draft and bibliography; local `coko-slam-magic-slam.md` and provenance notes | Explicit. Public repository README states: "This codebase is based on MAGiC-SLAM." Local evidence also records the paper/source claim that CoKo-SLAM uses the same tracking as MAGiC-SLAM and contributes keyframe selection, compaction, and server registration/fusion changes. | CoKo-SLAM should appear after MAGiC-SLAM if the section communicates algorithmic inheritance. Current order satisfies this. |
| CoMA-SLAM | 4 | Distributed multi-agent Gaussian SLAM with 2D Gaussian surfels; geometric consistency, loop closure, distributed keyframe/submap optimization | AAAI/OJS page attempted; CoMA-SLAM GitHub; local draft and bibliography; local research notes | No explicit dependency on other surveyed algorithms found in accessible repository/source summaries. It is related by pattern to MAC-Ego3D through distributed multi-agent optimization/consensus, but available evidence does not support a build-on claim. | Can be grouped near MAC-Ego3D under distributed methods. No dependency-first constraint except not presenting it as derived from MAC-Ego3D. |
| HAMMER | 5 | Heterogeneous multi-robot/device semantic 3D Gaussian Splatting; server aligns local SLAM outputs into shared metric-semantic map; CLIP/open-vocabulary semantics | arXiv abstract page; HAMMER project page; local draft and bibliography; local research notes | No explicit dependency on the surveyed algorithms found. Sources name broader dependencies/patterns: 3D Gaussian Splatting, local SLAM pose estimates, ROS communication infrastructure, CLIP semantic codes. Project-page template credits Nerfies/PerAct are website/template lineage, not algorithm lineage. | Best placed by taxonomy as heterogeneous semantic mapping, not by dependency. It need not follow MAGiC-SLAM or GRAND-SLAM unless using a taxonomy-first order. |
| GRAND-SLAM | 6 | RGB-D large-scale multi-agent Gaussian SLAM; local submap optimization, inter-/intra-robot loop closure, pose-graph optimization | arXiv abstract page; local draft and bibliography; local research notes; DOI/bibliography URL inspected locally | No explicit dependency on other surveyed algorithms found. It contrasts with prior multi-agent Gaussian SLAM approaches as limited to small indoor settings, but the inspected sources do not state that it builds on MAGiC-SLAM, CoKo-SLAM, MAC-Ego3D, CoMA-SLAM, HAMMER, or MAGS-SLAM. | Can be ordered after MAGiC-SLAM as another submap/pose-graph family member, or later as large-scale extension. Avoid claiming CoKo-style centralized fusion. |
| MAGS-SLAM | 7 | RGB-only/monocular multi-agent 3DGS SLAM; local monocular Gaussian submaps, compact summaries, geometry/appearance loop verification, scale-aware/occupancy-aware fusion | arXiv abstract page; MAGS-SLAM project page; local draft and bibliography; local research notes | No explicit dependency on other surveyed algorithms found. Project page says design borrowed from Nerfies for the website/page design; this is not surveyed-method algorithm lineage. It positions itself against prior RGB-D collaborative Gaussian SLAM methods and claims RGB-only novelty. | Natural to place last or in a separate monocular section because it changes modality and has provisional code/data status. No dependency reason forces it after CoKo-SLAM except taxonomy/modality contrast. |

## 3. Lineage/dependency matrix

Rows are candidate successor methods; columns are possible predecessors. Labels mean:

- **EXPLICIT**: inspected direct source states code/method inheritance or same tracker/component use.
- **WEAK/INFERRED**: similar architecture, benchmark lineage, or positioned against prior work, but no direct build-on statement found.
- **NOT SUPPORTED**: no inspected source supports a build-on relationship.

| successor ↓ / predecessor → | MAGiC-SLAM | MAC-Ego3D | CoKo-SLAM | CoMA-SLAM | HAMMER | GRAND-SLAM | MAGS-SLAM |
|---|---|---|---|---|---|---|---|
| MAGiC-SLAM | — | NOT SUPPORTED | NOT SUPPORTED | NOT SUPPORTED | NOT SUPPORTED | NOT SUPPORTED | NOT SUPPORTED |
| MAC-Ego3D | NOT SUPPORTED | — | NOT SUPPORTED | NOT SUPPORTED | NOT SUPPORTED | NOT SUPPORTED | NOT SUPPORTED |
| CoKo-SLAM | **EXPLICIT** | NOT SUPPORTED | — | NOT SUPPORTED | NOT SUPPORTED | NOT SUPPORTED | NOT SUPPORTED |
| CoMA-SLAM | WEAK/INFERRED | WEAK/INFERRED | WEAK/INFERRED | — | NOT SUPPORTED | WEAK/INFERRED | NOT SUPPORTED |
| HAMMER | WEAK/INFERRED | NOT SUPPORTED | WEAK/INFERRED | NOT SUPPORTED | — | NOT SUPPORTED | NOT SUPPORTED |
| GRAND-SLAM | WEAK/INFERRED | NOT SUPPORTED | NOT SUPPORTED | NOT SUPPORTED | NOT SUPPORTED | — | NOT SUPPORTED |
| MAGS-SLAM | WEAK/INFERRED | NOT SUPPORTED | WEAK/INFERRED | NOT SUPPORTED | NOT SUPPORTED | WEAK/INFERRED | — |

Notes on WEAK/INFERRED entries:

- CoMA-SLAM shares distributed multi-agent Gaussian-map concerns with MAC-Ego3D and compact/low-communication concerns with CoKo-SLAM, but no inspected source says it derives from them.
- GRAND-SLAM and MAGiC-SLAM both use RGB-D Gaussian submaps plus loop/pose-graph consistency, but the inspected sources support architectural resemblance and prior-work contrast only, not inheritance.
- HAMMER shares the central-server/no-initial-relative-pose alignment problem with MAGiC-SLAM/CoKo-SLAM, but it is heterogeneous and semantic; no build-on evidence was found.
- MAGS-SLAM positions itself against prior RGB-D multi-agent Gaussian SLAM and uses compact summaries, but its monocular scale-aware pipeline is presented as a new RGB-only direction, not as a derivative of CoKo-SLAM, MAGiC-SLAM, or GRAND-SLAM.

## 4. Clear answer

Beyond **CoKo-SLAM → MAGiC-SLAM**, I did not find another clear build-on relationship among the seven surveyed algorithms.

The only direct, explicit surveyed-method lineage found is CoKo-SLAM's public repository statement that its codebase is based on MAGiC-SLAM, reinforced by the draft/local notes that CoKo-SLAM inherits MAGiC-SLAM tracking while adding keyframe selection, compact communication, redundant-Gaussian pruning, and server-side registration/fusion changes.

Other relationships are better described as architectural proximity, shared problem setting, or prior-work positioning:

- MAC-Ego3D and CoMA-SLAM are both distributed/consensus-like multi-agent Gaussian-map systems, but no source inspected says CoMA-SLAM builds on MAC-Ego3D.
- MAGiC-SLAM and GRAND-SLAM both use RGB-D Gaussian submaps and loop/pose-graph global consistency, but no inspected source says GRAND-SLAM builds on MAGiC-SLAM.
- CoKo-SLAM and MAGS-SLAM both emphasize compact communication, but MAGS-SLAM is monocular/RGB-only and no inspected source says it derives from CoKo-SLAM.
- HAMMER shares server-side alignment/global mapping concerns with the centralized systems, but its heterogeneous semantic framing and inspected sources do not establish surveyed-method inheritance.

## 5. Recommended ordering options

### Option A: preserve current order

Order: MAGiC-SLAM, MAC-Ego3D, CoKo-SLAM, CoMA-SLAM, HAMMER, GRAND-SLAM, MAGS-SLAM.

Rationale:

- Keeps MAGiC-SLAM before CoKo-SLAM, satisfying the only explicit surveyed-method dependency.
- Starts with the strongest public RGB-D baselines: centralized/server MAGiC-SLAM and distributed/consensus MAC-Ego3D.
- Moves from mature public-code systems toward newer, less code-auditable or modality-specialized systems.
- Requires only a small transition sentence saying the order is architecture/evidence driven, not a strict lineage chain.

This is the safest minimal-change option.

### Option B: dependency-first with explicit lineage callout

Order: MAGiC-SLAM, CoKo-SLAM, MAC-Ego3D, CoMA-SLAM, GRAND-SLAM, HAMMER, MAGS-SLAM.

Rationale:

- Places CoKo-SLAM immediately after MAGiC-SLAM so the inherited tracker/codebase relationship is visually obvious.
- Then groups distributed methods, submap/pose-graph methods, heterogeneous semantic mapping, and monocular RGB-only mapping.
- Useful if the survey's reader question is "which algorithms build on which?"

Caveat: this may overemphasize lineage even though only one explicit lineage edge exists. It should be introduced as "dependency-aware grouping," not as a dependency chain.

### Option C: taxonomy-first

Suggested taxonomy order:

1. Central-server RGB-D Gaussian submap systems: MAGiC-SLAM, CoKo-SLAM
2. Distributed/consensus Gaussian-map systems: MAC-Ego3D, CoMA-SLAM
3. Submap-plus-pose-graph large-scale consistency: GRAND-SLAM
4. Heterogeneous semantic global mapping: HAMMER
5. Monocular compact-submap fusion: MAGS-SLAM

Rationale:

- Aligns the method section with the architecture taxonomy already used later in the draft.
- Makes it clear that most relationships are pattern relationships rather than inheritance relationships.
- Keeps CoKo-SLAM after MAGiC-SLAM and avoids implying GRAND-SLAM or CoMA-SLAM derive from specific earlier algorithms.

This is the strongest scholarly flow if the paper wants algorithm ordering to reflect system design patterns rather than publication date or code availability.

## 6. Caveats and unsupported relationships

- The review used existing local notes as secondary evidence and external arXiv/project/GitHub pages as primary evidence where possible. Some primary pages expose only abstracts or README summaries, not full paper text.
- The AAAI/OJS CoMA-SLAM page timed out through one fetch path. The review therefore relies on the local bibliography, local research notes, and the public GitHub page for CoMA-SLAM lineage assessment. No explicit surveyed-method dependency was visible there.
- Direct build-on claims involving non-surveyed methods exist but should not affect the ordering among the seven surveyed algorithms: MAGiC-SLAM's README mentions Gaussian-SLAM and GraphSLAM; HAMMER uses broader 3DGS/SLAM/CLIP/ROS components; MAC-Ego3D lists implementation dependencies; MAGS-SLAM page/template mentions Nerfies design for webpage design.
- Shared datasets such as ReplicaMultiagent or AriaMultiagent do not constitute algorithmic lineage.
- Similar operators in the draft, such as `local_tracking_i`, `update_selection_i`, `cross_agent_alignment_t`, and `global_fusion_t`, are survey abstractions. They should not be read as proof that methods implement the same algorithm unless source evidence says so.
- The local draft's appendix is already careful about MAC-Ego3D tracking: it distinguishes MAC-Ego3D's Gaussian-consensus/geometric alignment evidence from MAGiC-SLAM's rendered RGB-D tracker. That distinction should be preserved.
- GRAND-SLAM should not be described as CoKo-style centralized compact rendered-depth fusion unless a direct source supports that. The inspected evidence supports local Gaussian submaps plus inter-/intra-robot loop closure and pose-graph consistency.
- MAGS-SLAM remains lower-confidence for implementation-level lineage because code/data are not public at the inspected project page; only paper/project-level architecture claims are available.

## 7. Sources

- https://openaccess.thecvf.com/content/CVPR2025/html/Yugay_MAGiC-SLAM_Multi-Agent_Gaussian_Globally_Consistent__SLAM_CVPR_2025_paper.html
- https://github.com/VladimirYugay/MAGiC-SLAM
- https://vladimiryugay.github.io/magic_slam
- https://arxiv.org/abs/2411.16785
- https://arxiv.org/abs/2412.09723
- https://github.com/Xiaohao-Xu/MAC-Ego3D
- https://arxiv.org/abs/2604.00804
- https://github.com/lemonci/coko-slam
- https://arxiv.org/html/2604.00804
- https://ojs.aaai.org/index.php/AAAI/article/view/37283
- https://github.com/npu-chenlin/CoMA-SLAM
- https://arxiv.org/abs/2501.14147
- http://hammer-project.github.io
- https://arxiv.org/abs/2506.18885
- https://doi.org/10.1109/LRA.2025.3623026
- https://arxiv.org/abs/2605.10760
- https://mags-slam.github.io/
