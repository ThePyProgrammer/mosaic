# T3: Code, license, dependency, and maturity check for multi-robot Gaussian SLAM systems

## 1. Executive summary

The open-source landscape for true multi-agent / multi-robot Gaussian Splatting SLAM is very small. The only mature public implementation found is **MAGiC-SLAM** (`VladimirYugay/MAGiC-SLAM`), a CVPR 2025 RGB-D multi-agent Gaussian SLAM system with runnable scripts, configs, CUDA/PyTorch dependencies, and an MIT repository license with third-party caveats. **CoKo-SLAM** (`lemonci/coko-slam`) is a newer public RGB-D multi-agent extension focused on compact keyframe/submap communication; it is also runnable-looking and MIT-licensed, but younger, lower-star, and has rough dependency hygiene (`requirments.txt`, absolute local build paths in the frozen dependency file). **MAGS-SLAM** currently appears to be a promised release only: its project page says code/data will be released upon acceptance and no public implementation repository was found. **RobotFlow-Labs/project_slam_coko** is an adjacent scaffold/reimplementation wrapper around CoKo-SLAM concepts and vendored CoKo-SLAM code, but its README says the core runtime is still incomplete; despite a README MIT statement, no root LICENSE file was found via GitHub API. I found no credible public repository for **GRAND-SLAM** in this target class.

For Mosaic integration planning, these systems are valuable as research backends and architecture references, not as clean library dependencies. They are CUDA-heavy, research-code style, Python 3.11 / PyTorch 2.5-era systems with compiled Gaussian rasterizer / KNN components, Open3D, graph optimization, and dataset-specific layouts. Mosaic should keep them behind optional backend adapters or process boundaries and extract only typed contracts for frames, maps, submaps, provenance, and fusion diagnostics.

## 2. Repository inventory table

| System / repo | URL | Public/private/promised/dead | License | Implementation maturity | Dependencies | Documented modalities | Documented multi-agent fusion support | Install/run evidence | Mosaic integration risk | Confidence |
|---|---|---:|---|---|---|---|---|---|---|---:|
| **MAGiC-SLAM: Multi-Agent Gaussian Globally Consistent SLAM** (`VladimirYugay/MAGiC-SLAM`) | https://github.com/VladimirYugay/MAGiC-SLAM | Public, active-looking | GitHub API reports `Other`, LICENSE text is MIT plus “original license applies to Inria Gaussian Splatting components” | Highest maturity found: CVPR 2025 repo; root `run_slam.py`, `run_visualization.py`, configs for `AriaMultiagent` and `ReplicaMultiagent`, `src/entities` with `agent.py`, `magic_slam.py`, `mapper.py`, `tracker.py`, loop detection, pose graph adapter, eval utilities; 334 stars / 17 forks at query time | Python 3.11 conda; PyTorch 2.5.1 + CUDA 11.8/12.1/12.4; `faiss-gpu=1.8.0`; git deps `simple-knn`, `gaussian_rasterizer`; Open3D, wandb, trimesh, pytorch-msssim, torchmetrics, tqdm, imageio, OpenCV, plyfile, graphslam, roma, transformers | Project page says RGB-D streams; README datasets are ReplicaMultiagent and AriaMultiagent; project page mentions TUM-RGBD comparison | Yes. Per-agent submaps; server does loop closure detection, loop constraint estimation, pose graph optimization, and global map merge. Requires roughly `n + 1` GPUs for `n` agents | README provides conda setup, CUDA compiler warnings, `pip install -r requirements.txt`, optional rerun-sdk, and `python run_slam.py configs/<dataset>/<config> --input_path ... --output_path ...`; SLURM reproduction scripts exist | High: CUDA/native extensions, GPU assumptions, dataset-specific configs, research code, server/agent lifecycle entangled with implementation; suitable only behind optional adapter/process seam | High |
| **CoKo-SLAM: Compact Keyframe-Optimized Multi-Agent Gaussian Splatting SLAM** (`lemonci/coko-slam`) | https://github.com/lemonci/coko-slam | Public, new, active-looking | GitHub API reports `Other`, LICENSE text is MIT plus Inria Gaussian Splatting third-party caveat | Medium-high research maturity: root `run_slam.py`, `run_visualization.py`, configs for `AriaMultiagent`, `ReplicaMultiagent`, `TUM_RGBD`, source modules for agents, mapping, tracking, GTSAM pose graph, loop detection, compaction/checkpoint; 4 stars / 2 forks at query time | README: Python 3.11 conda; PyTorch 2.5.1 CUDA; `faiss-gpu=1.8.0`; `pip install -r requirements.txt`, but repo file is named `requirments.txt`; file includes many frozen packages plus absolute local paths for `arithmetic`, `diff_gaussian_rasterization`, `freqencoder`, `gridcreater`, `gridencoder`; git deps from VladimirYugay rasterizer/KNN; Open3D, OpenCV, projectaria-tools, graphslam, rerun-sdk, transformers, wandb | Paper/WebFetch: RGB-D frames on robot edge devices; keyframe features from DINOv2-Small; rendered depth or camera depth for loop closure; README tested on ReplicaMultiagent and AriaMultiagent; configs also include TUM_RGBD | Yes. Compact Gaussian submaps and keyframe feature vectors are transmitted to server; server-side fusion, pose-graph optimization, pose-free loop closure; claims no initial relative poses and 85–95% lower transmitted data vs baselines | README provides conda setup, CUDA compiler notes, data download/processing instructions, `python run_slam.py configs/...`, and SLURM reproduction script. Dependency typo and absolute local paths are red flags | High: even more integration risk than MAGiC because dependency file appears non-reproducible as published; GTSAM/compiled CUDA/rasterizer dependencies and multi-agent orchestration must stay isolated | High |
| **RobotFlow-Labs/project_slam_coko** | https://github.com/RobotFlow-Labs/project_slam_coko | Public adjacent scaffold/reimplementation; not mature runtime | README says MIT — AIFLOW LABS LIMITED; GitHub API license null; `gh api .../LICENSE` returned 404 | Low-to-medium, scaffold. README status checks: PRDs/tasks, Python 3.11 + UV foundation, dataset catalog and submap schemas done; unchecked: core tracker/mapper runtime, loop closure and GTSAM pose graph, Replica/Aria eval, ROS2 bridge/API/Docker runtime. Tree contains tests, API, schemas, mapping, fusion, registration modules, plus vendored `repositories/coko-slam` | `pyproject.toml`: Python >=3.11,<3.12; numpy, opencv-python, pydantic, pydantic-settings, scipy; optional dev mypy/pytest/ruff; optional `paper` Open3D, Pillow, PyYAML, rich, transformers, typer; optional `cuda` torch/torchaudio/torchvision | Claims SLAM-COKO / Compact Keyframe-Optimized Multi-Agent Gaussian Splatting SLAM; intended Replica/Aria, ROS2 bridge; likely RGB-D via CoKo-SLAM concepts | Intended, but README explicitly marks core tracker/mapper runtime and loop closure/PGO as incomplete. Contains schema/fusion/registration modules but should be treated as scaffold | README quick start uses `uv venv`, `uv sync --extra dev`, and limited pytest targets for settings/schema; CUDA bootstrap script exists; not evidence of full SLAM execution | Medium for Mosaic as design inspiration for typed schemas/tests; high/unsuitable as backend because runtime incomplete and license file absent at root | High |
| **MAGS-SLAM: Monocular Multi-Agent Gaussian Splatting SLAM** (`mags-slam/mags-slam.github.io`) | https://mags-slam.github.io and source https://github.com/mags-slam/mags-slam.github.io | Promised only; project page repo public but contains website, not implementation | No implementation license found; website repo license null | Not available as code. Website says paper under double-blind review and button says “Code & Data (Released upon Acceptance)” | Not disclosed in code. Page describes benchmark and method only | RGB-only / monocular; benchmark page also mentions RGB-D streams and ground-truth poses in ReplicaMultiAgent Plus dataset; datasets shown include ReplicaMultiAgent, ReplicaMultiAgent Plus, ETH3D, Tanks and Temples, 7-Scenes Fire | Claimed compact submap summaries, geometry- and appearance-aware loop verification, occupancy-aware Gaussian fusion, coherent global reconstruction without active depth sensors | No install/run evidence; no implementation repo found by GitHub search for exact title or code search phrases | Unknown/high. Potentially architecturally relevant for RGB-only multi-agent contracts once released, but currently cannot be integrated or audited | High for “promised/no code”; low for implementation details |
| **MultiAgent-GaussianSplat-SLAM** | No public repo found under exact search terms | Ambiguous / not found | Unknown | No credible public repository found. GitHub exact search returned no repo; web search providers failed or returned no result | Unknown | Target name suggests multi-agent Gaussian splatting SLAM, but no code evidence found | Unknown | None | Not integrable; treat as missing/dead until a concrete URL is provided | Medium |
| **MAGS-SLAM implementation repo** | No implementation repo found; only website repo https://github.com/mags-slam/mags-slam.github.io | Promised | Unknown | Website only | Unknown | RGB-only / monocular claimed | Claimed, not auditable | None | Not integrable yet | High |
| **GRAND-SLAM** | No credible public repo found for a Gaussian multi-agent SLAM system | Ambiguous / not found | Unknown | GitHub repository and code searches for GRAND-SLAM + Gaussian/SLAM returned no credible candidate | Unknown | Unknown | Unknown | None | Not integrable; likely a paper/code-link ambiguity or unavailable code | Medium |
| **VladimirYugay/Gaussian-SLAM** | https://github.com/VladimirYugay/Gaussian-SLAM | Public adjacent baseline | MIT per GitHub search result | Mature single-agent Gaussian SLAM baseline; MAGiC-SLAM README says individual tracking/mapping modules are based on it | Similar Gaussian-SLAM stack: CUDA/PyTorch/native rasterizer expected | Photo-realistic dense SLAM; not target multi-agent | No documented multi-agent fusion in the search result; adjacent single-agent backend | Public repo, but not audited in depth here because target is multi-agent | High if used directly; useful as baseline/reference only | Medium |
| **Just-ZJJ/MDGS_SLAM** | https://github.com/Just-ZJJ/MDGS_SLAM | Public adjacent candidate | Apache-2.0 per GitHub search result | Adjacent: “Real-Time RGB-D Gaussian SLAM with Multi-View Ray-Correspondence Densification”; not found as multi-agent | Likely CUDA/PyTorch 3DGS stack, not audited | RGB-D | No multi-agent fusion documented in search result | Public repo exists; not deeply audited due task boundary | High/medium; relevant for single-agent RGB-D mapping only | Low-medium |
| **leggedrobotics/DiskChunGS** | https://github.com/leggedrobotics/DiskChunGS | Public adjacent large-scale candidate | GitHub search reports `Other` | Adjacent: RA-L 2026 large-scale 3D Gaussian SLAM through disk chunking; not multi-agent | Not audited | Not audited | No multi-agent fusion documented in search result | Public repo exists; not deeply audited due task boundary | Medium for large-map storage ideas; not a multi-agent fusion backend | Low-medium |

## 3. Detailed notes on open-source candidates

### 3.1 MAGiC-SLAM (`VladimirYugay/MAGiC-SLAM`)

**Availability and maturity.** This is the strongest public implementation in the target class. GitHub metadata identified it as public, non-archived, created 2024-11-25, updated 2026-05-12, with 334 stars and 17 forks at query time. The repository root contains `LICENSE`, `README.md`, `requirements.txt`, `run_slam.py`, `run_visualization.py`, `assets`, `configs`, `scripts`, and `src`. Recursive tree inspection found concrete implementation modules:

- `src/entities/agent.py`
- `src/entities/magic_slam.py`
- `src/entities/mapper.py`
- `src/entities/tracker.py`
- `src/entities/visual_odometer.py`
- `src/entities/loop_detection/loop_detector.py`, `feature_extractors.py`, `netvlad.py`
- `src/entities/pose_graph_adapter.py`
- `src/utils/mapping_eval.py`, `tracking_eval.py`, visualization and Gaussian utilities

Configs include `AriaMultiagent` and `ReplicaMultiagent` scenes. Scripts include data preparation and SLURM reproduction scripts.

**License.** The GitHub API classifies the license as `Other`, but the repository `LICENSE` content is MIT. It includes a third-party caveat: “The original license applies to the Inria Gaussian Splatting components. This project as a whole is licensed under MIT.” For Mosaic, that means any adapter can depend on the repo as an optional external backend, but copying code or vendoring components would require checking the Inria 3DGS component license and any submodule licenses.

**Dependencies and install evidence.** README setup is research-code but complete enough to attempt reproduction on a GPU machine: conda env with Python 3.11, PyTorch 2.5.1 and CUDA 11.8/12.1/12.4, `faiss-gpu=1.8.0`, `pip install -r requirements.txt`, optional `rerun-sdk`. The README warns `nvcc --version` should match `nvidia-smi`, and says it was tested on RTX3090 and RTX A6000 GPUs with Ubuntu 22 and CentOS 7.5. Requirements include `git+https://github.com/VladimirYugay/simple-knn.git@c7e51a...`, `git+https://github.com/VladimirYugay/gaussian_rasterizer.git@9c401...`, Open3D 0.18.0, wandb, graphslam, transformers, OpenCV, torchmetrics, etc.

**Modalities and fusion.** The project page identifies **RGB-D streams**. The README mentions ReplicaMultiagent and AriaMultiagent. It says the system ideally needs `n + 1` GPUs for `n` agents, with a debug mode allowing `multi_gpu: False` and `agent_ids: [0]`. WebFetch of the project page says the server performs loop closure detection, loop constraint estimation, and pose graph optimization, and that per-agent submaps are merged into a unified globally consistent map.

**Mosaic risk.** This is not a library-shaped dependency. It is a runnable research system with process/GPU assumptions, dataset-specific configs, native CUDA extensions, and global orchestration. Good candidate for a future `mosaic.backends.magic_slam` optional adapter that exchanges typed observations/submaps/results across a process boundary, not for importing into Mosaic core.

### 3.2 CoKo-SLAM (`lemonci/coko-slam`)

**Availability and maturity.** GitHub metadata identified it as public, non-archived, created 2026-03-29, updated 2026-05-12, with 4 stars and 2 forks at query time. The README title is “Compact Keyframe-Optimized Multi-Agent Gaussian Splatting SLAM.” The root contains `LICENSE`, `README.md`, `requirments.txt` (misspelled), `run_slam.py`, `run_visualization.py`, `configs`, `scripts`, and `src`. The tree includes implementation modules similar to MAGiC-SLAM plus CoKo-specific additions such as `src/entities/gtsam_pose_graph.py`, `src/entities/magic_slam_checkpoint.py`, and `src/utils/optimizing_spa.py`. Configs include `AriaMultiagent`, `ReplicaMultiagent`, and `TUM_RGBD`, including baseline configs.

**License.** As with MAGiC-SLAM, GitHub classifies the license as `Other`, but the `LICENSE` text is MIT with the same Inria Gaussian Splatting third-party caveat.

**Dependencies and install evidence.** The README instructs Python 3.11 conda, PyTorch 2.5.1 CUDA, `faiss-gpu=1.8.0`, and `pip install -r requirements.txt`; however, the actual root file returned by GitHub is `requirments.txt`, not `requirements.txt`. That typo alone can break the documented install command. The frozen dependency file also contains absolute local file paths under `/home/mistlab/Documents/ml/MAGiC-SLAM/ideas/FCGS/submodules/...` for `arithmetic`, `diff_gaussian_rasterization`, `freqencoder`, `gridcreater`, and `gridencoder`. This is a serious reproducibility defect unless those paths are replaced by submodules or package URLs. It also includes `gaussian_rasterizer` and `simple_knn` git dependencies, PyTorch, Open3D, OpenCV, projectaria-tools, rerun-sdk, graphslam, transformers, faiss, wandb, etc.

**Modalities and fusion.** WebFetch of the arXiv HTML page identifies RGB-D frames on edge devices, DINOv2-Small keyframe features, rendered depth or camera depth for loop closure, Gaussian submaps, and server-side submap fusion/Pose Graph Optimization. The method claims map merging without initial relative poses and transmission of Gaussian submaps + keyframe feature vectors instead of images or point clouds. It claims 85–95% less transmitted data than baselines. README says tested on ReplicaMultiagent and AriaMultiagent datasets; configs additionally include TUM_RGBD.

**Mosaic risk.** CoKo-SLAM is architecturally more relevant than MAGiC for Mosaic’s long-term multi-robot/fusion goals because it foregrounds compact submap communication, keyframe features, provenance/fusion, and bandwidth. But the repository is younger and has rougher packaging. Treat it as a high-value reference and possible experimental backend behind isolation, not as an importable dependency.

### 3.3 MultiAgent-GaussianSplat-SLAM

No public repository was found under the exact name `MultiAgent-GaussianSplat-SLAM` or nearby phrases using GitHub repository search and WebSearch. Because this name is plausible and generic, it may refer to a private repo, renamed repo, paper artifact, or informal project label. Without a concrete URL, there is no license, dependency, maturity, or integration evidence to verify. It should be listed as **ambiguous/not found**, not as an open-source candidate.

### 3.4 `project_slam_coko` (`RobotFlow-Labs/project_slam_coko`)

**Availability and maturity.** This repo is public and non-archived, created 2026-04-03, updated 2026-04-03, 0 stars and 0 forks at query time. README describes it as “SLAM-COKO — ANIMA Module” and links the CoKo-SLAM arXiv paper. It is not the same as the author code release. It appears to be a scaffolded ANIMA/RobotFlow implementation plus a vendored copy of CoKo-SLAM under `repositories/coko-slam`.

The README status checklist is candid:

- Done: paper-grounded PRDs/tasks, Python 3.11 + UV foundation, dataset catalog and submap schemas.
- Not done: core tracker/mapper runtime, loop closure and GTSAM pose graph, Replica and Aria evaluation, ROS2 bridge/API/Docker runtime.

Recursive tree inspection shows many useful scaffold modules and tests: `src/anima_slam_coko/schemas/submap.py`, `fusion/merge.py`, `mapping/compaction.py`, `registration/coarse.py`, `registration/fine.py`, `pgo/gtsam_solver.py`, `ros2` bridge stubs, API/job models, and tests for schemas/config/eval/keyframing/loop closure/pgo/registration. This is a structured engineering scaffold, but not a complete SLAM implementation by its own README.

**License.** README says “MIT — AIFLOW LABS LIMITED,” but the GitHub API reports null license and `gh api repos/RobotFlow-Labs/project_slam_coko/contents/LICENSE` returned 404. License should be treated as ambiguous until a root LICENSE file is added. The vendored `repositories/coko-slam/LICENSE` is MIT with Inria caveat, but that does not necessarily license the whole wrapper repo.

**Dependencies and install evidence.** `pyproject.toml` uses Hatchling, Python >=3.11,<3.12, and lightweight dependencies: numpy, opencv-python, pydantic, pydantic-settings, scipy. Optional groups include dev (`mypy`, `pytest`, `ruff`), `paper` (`open3d`, `pillow`, `pyyaml`, `rich`, `transformers`, `typer`), and `cuda` (`torch`, `torchaudio`, `torchvision`). README quick start runs `uv venv`, `uv sync --extra dev`, and a narrow pytest subset. This is good software-engineering hygiene, but it is evidence for config/schema tests, not evidence for a working multi-agent Gaussian SLAM pipeline.

**Mosaic relevance.** This repo is more useful as a typed-schema/testing scaffold reference than as a backend. Mosaic should not depend on it for core SLAM capability.

### 3.5 MAGS-SLAM

The website `https://mags-slam.github.io` identifies MAGS-SLAM as “Monocular Multi-Agent Gaussian Splatting SLAM for Geometrically and Photometrically Consistent Reconstruction.” The public GitHub repo `mags-slam/mags-slam.github.io` contains only website files (`index.html`, `scripts`, `static`). The page says “Paper under double-blind review” and displays a button “Code & Data (Released upon Acceptance),” not a repository URL.

**Claims from website.** It claims to be the first RGB-only multi-agent 3D Gaussian Splatting SLAM system for collaborative photorealistic reconstruction. It says agents build local monocular Gaussian submaps and transmit compact submap summaries; the system uses geometry- and appearance-aware loop verification and occupancy-aware Gaussian fusion. It introduces ReplicaMultiAgent Plus and shows/mentions ReplicaMultiAgent, ReplicaMultiAgent Plus, ETH3D, Tanks and Temples, and 7-Scenes Fire. The benchmark section says ReplicaMultiAgent Plus includes monocular RGB-only or RGB-D streams, ground-truth poses, and semantic/instance labels.

**Code status.** No implementation repo was found through GitHub repository search for the exact title or code search for distinctive phrases. Treat as promised/not auditable.

### 3.6 GRAND-SLAM

No credible public code was found for a Gaussian multi-agent SLAM system named GRAND-SLAM. WebSearch attempts failed or returned no useful results, and GitHub repo/code searches for `GRAND-SLAM` with Gaussian/Splatting/SLAM returned no credible candidate. This may be a missing paper artifact, renamed system, or non-Gaussian project. It should remain in the “dead/promised/ambiguous” bucket until a direct URL is supplied.

### 3.7 Adjacent candidates worth tracking, but not target-class matches

- `VladimirYugay/Gaussian-SLAM` is the single-agent baseline that MAGiC-SLAM says it builds on for individual tracking/mapping. Useful for understanding per-agent backend assumptions, but not itself a multi-agent fusion system.
- `Just-ZJJ/MDGS_SLAM` is a public Apache-2.0 RGB-D Gaussian SLAM system with multi-view ray-correspondence densification. It is adjacent for RGB-D Gaussian map quality and densification, not a documented multi-agent shared-map system in the search evidence.
- `leggedrobotics/DiskChunGS` is a public large-scale 3D Gaussian SLAM/chunking project. It may be useful for Mosaic large-map storage or streaming abstractions, but no multi-agent fusion evidence was found in this task.
- `gaussianflow-slam/gaussianflow-slam.github.io`, `url-kaist/gaussianflow-slam`, `Sabers-Lily/AdaG-SLAM`, and other recent Gaussian SLAM repositories surfaced in broad search. They appear single-agent or unrelated to online multi-robot fusion from the available snippets, so they were not deeply audited here.

## 4. Dead / promised / ambiguous code links

1. **MAGS-SLAM implementation** — promised only. Website button says “Code & Data (Released upon Acceptance)”; public repo found is website source only: https://github.com/mags-slam/mags-slam.github.io.
2. **MultiAgent-GaussianSplat-SLAM** — no public repository found under exact or near-exact search terms. Status: ambiguous/not found.
3. **GRAND-SLAM** — no credible public repository found for a Gaussian multi-agent SLAM system. Status: ambiguous/not found.
4. **RobotFlow-Labs/project_slam_coko license** — repo is public and README says MIT, but root `LICENSE` is absent via GitHub API and GitHub license metadata is null. Status: license ambiguous, implementation scaffold incomplete.
5. **CoKo-SLAM dependency reproducibility** — public source exists, but documented `pip install -r requirements.txt` conflicts with root file `requirments.txt`, and frozen dependencies include absolute local paths. Status: code available, install instructions need repair.

## 5. Numbered source list

1. MAGiC-SLAM GitHub repository: https://github.com/VladimirYugay/MAGiC-SLAM
2. MAGiC-SLAM project page: https://vladimiryugay.github.io/magic_slam
3. MAGiC-SLAM arXiv abstract: https://arxiv.org/abs/2411.16785
4. MAGiC-SLAM CVPR 2025 OpenAccess page: https://openaccess.thecvf.com/content/CVPR2025/html/Yugay_MAGiC-SLAM_Multi-Agent_Gaussian_Globally_Consistent__SLAM_CVPR_2025_paper.html
5. MAGiC-SLAM simple-knn dependency: https://github.com/VladimirYugay/simple-knn
6. MAGiC-SLAM gaussian_rasterizer dependency: https://github.com/VladimirYugay/gaussian_rasterizer
7. CoKo-SLAM GitHub repository: https://github.com/lemonci/coko-slam
8. CoKo-SLAM arXiv HTML: https://arxiv.org/html/2604.00804v1
9. CoKo-SLAM arXiv abstract: https://arxiv.org/abs/2604.00804v1
10. CoKo-SLAM arXiv PDF: https://arxiv.org/pdf/2604.00804v1
11. ReplicaMultiagent Hugging Face dataset referenced by MAGiC/CoKo READMEs: https://huggingface.co/datasets/voviktyl/ReplicaMultiagent
12. AriaMultiagent Hugging Face dataset referenced by MAGiC README: https://huggingface.co/datasets/voviktyl/AriaMultiagent
13. Project Aria Digital Twin dataset page referenced by READMEs: https://www.projectaria.com/datasets/adt/
14. Project Aria data tools docs referenced by READMEs: https://facebookresearch.github.io/projectaria_tools/docs/open_datasets/aria_digital_twin_dataset/dataset_download
15. RobotFlow-Labs project_slam_coko repository: https://github.com/RobotFlow-Labs/project_slam_coko
16. MAGS-SLAM project page: https://mags-slam.github.io
17. MAGS-SLAM website source repository: https://github.com/mags-slam/mags-slam.github.io
18. VladimirYugay Gaussian-SLAM adjacent baseline: https://github.com/VladimirYugay/Gaussian-SLAM
19. Just-ZJJ MDGS_SLAM adjacent candidate: https://github.com/Just-ZJJ/MDGS_SLAM
20. leggedrobotics DiskChunGS adjacent candidate: https://github.com/leggedrobotics/DiskChunGS
