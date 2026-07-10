# Research Plan: Open-source multi-view moving-camera online 3D Gaussian Splatting SLAM implementations

## Questions
1. Which open-source implementations exist for online or incremental 3D Gaussian Splatting SLAM with moving cameras?
2. Which implementations support, or can plausibly be adapted to, multiple independently moving or robot-mounted cameras rather than a single monocular/RGB-D stream?
3. Which systems are real-time or online versus offline reconstruction/localization pipelines?
4. What sensor assumptions do they make: monocular, stereo, RGB-D, LiDAR, IMU, known poses, estimated poses, calibrated rigs, or multi-view synchronized input?
5. What benchmarks, datasets, metrics, and runtime/FPS numbers are reported by papers, repositories, or project pages?
6. Which implementations are most appropriate as future Mosaic backend references, given Mosaic's constraints: typed Python contracts, backend isolation, multi-view robot camera rigs, deterministic evaluation before backend integration, and agent-facing posterior APIs?
7. What gaps remain between available open-source 3DGS SLAM implementations and Mosaic's target of multi-view moving robot-mounted camera online mapping?

## Strategy
- Broad survey: identify recent 3DGS SLAM / Gaussian Splatting SLAM papers and repositories from 2023-2026, prioritizing open-source code.
- Code inventory: verify repository availability, license where visible, installation/runtime expectations, input modality, and whether the code appears maintained.
- Multi-camera/robot fit: separate true multi-camera or multi-view online support from monocular/RGB-D systems that merely process sequential frames.
- Benchmark extraction: collect reported datasets, metrics, accuracy numbers, map quality numbers, FPS/runtime, hardware, and baselines.
- Mosaic relevance scoring: rank candidates by online operation, openness, multi-view adaptability, typed-interface feasibility, backend isolation risk, and benchmark evidence.

Expected researcher allocations and dimensions:
- R1: Academic/system survey of online 3DGS SLAM papers and official project pages.
- R2: GitHub/codebase inventory of open-source implementations, licenses, dependencies, and maintenance status.
- R3: Multi-view, multi-camera, stereo, RGB-D, visual-inertial, and robot-mounted camera applicability.
- R4: Benchmarks and datasets: Replica, TUM RGB-D, ScanNet, EuRoC, KITTI, Tanks/Temples, Mip-NeRF 360, or robotics-specific evaluations if found.

Expected rounds: 1 broad parallel round, then 0-1 targeted follow-up rounds for missing systems, contradictory claims, or weak benchmark evidence.

## Acceptance Criteria
- [ ] All key questions answered with at least two independent sources where possible.
- [ ] Main open-source implementations are listed with source links, paper/project links, input modality, online/offline status, and multi-view relevance.
- [ ] Benchmark claims include dataset, metric, number, hardware/context when available, and citation.
- [ ] Contradictions identified and addressed, especially around real-time claims and multi-camera support.
- [ ] No single-source claims on critical findings unless explicitly labeled as repository-only or paper-only.
- [ ] Final recommendation distinguishes immediately relevant backends from inspiration-only systems.

## Task Ledger
| ID | Owner | Task | Status | Output |
|---|---|---|---|---|
| T1 | lead | Draft research plan and get confirmation | done | `outputs/.plans/multiview-3dgs-slam.md` |
| T2 | researcher R1 | Survey papers/project pages for online 3DGS SLAM systems | done | `outputs/multiview-3dgs-slam-research-papers.md` |
| T3 | researcher R2 | Inventory open-source repositories and implementation details | done | `outputs/multiview-3dgs-slam-research-code.md` |
| T4 | researcher R3 | Assess multi-view, multi-camera, stereo/RGB-D, VIO, and robot-mounted camera fit | done | `outputs/multiview-3dgs-slam-research-multicamera.md` |
| T5 | researcher R4 | Extract benchmark tables, datasets, metrics, runtimes, and hardware context | done | `outputs/multiview-3dgs-slam-research-benchmarks.md` |
| T6 | lead | Evaluate evidence gaps and run targeted follow-up if needed | done | `outputs/multiview-3dgs-slam-research-agrigs-followup.md`, `outputs/multiview-3dgs-slam-research-corrections.md` |
| T7 | lead | Write cited draft, claim sweep, verify URLs, final report, and provenance | done | `outputs/multiview-3dgs-slam.md`, `outputs/multiview-3dgs-slam.provenance.md` |

## Verification Log
| Item | Method | Status | Evidence |
|---|---|---|---|
| Candidate implementation list completeness | Cross-check paper survey vs GitHub inventory vs benchmark survey | pass with notes | T2-T5 plus targeted follow-up; rapidly changing 2025-2026 landscape means completeness is time-bounded |
| Open-source availability and repository URLs | Direct fetch repository/project pages | pass with notes | T3 plus corrections report; VIGS-SLAM and some newer systems remain inaccessible/promised |
| Online vs offline classification | Cross-read paper method sections and repository usage docs | pass with notes | T2/T3/T6; real-time/rendering/system FPS terminology varies by paper |
| Multi-camera or multi-view support classification | Check documented input modality, dataset loaders, examples, and paper setup | pass | T4 plus AgriGS follow-up; AgriGS-SLAM is native multi-camera; most others are stereo/RGB-D/multi-sensor/multi-agent only |
| Benchmark numbers | Verify against paper tables/project pages and avoid mixing metrics | pass with notes | T5; exact AgriGS per-sequence table numbers avoided where PDF extraction was unreliable |
| Mosaic backend suitability ranking | Lead synthesis from verified evidence, labeled as inference | pass | `outputs/multiview-3dgs-slam.md` |

## Decision Log
- 2026-05-18: Slug selected as `multiview-3dgs-slam`.
- 2026-05-18: Scope prioritizes open-source online/incremental 3DGS SLAM implementations; offline Gaussian reconstruction systems are included only when relevant for contrast or backend inspiration.
- 2026-05-18: Multi-camera claims will be treated conservatively: true support requires documented multi-camera/multi-view input handling, calibrated rig assumptions, or explicit multi-sensor fusion; otherwise systems are classified as adaptable but not native.
- 2026-05-18: First broad round completed with four researchers; targeted follow-up added for AgriGS-SLAM and source/license corrections because native multi-camera evidence was the critical uncertainty.
- 2026-05-18: AgriGS-SLAM is accepted as the only verified native robot-mounted multi-camera 3DGS SLAM implementation found; stereo/RGB-D, multi-sensor, and multi-agent systems are classified separately.
