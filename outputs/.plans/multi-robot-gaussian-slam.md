# Research Plan: Multi-Robot Online Gaussian SLAM

## Slug
`multi-robot-gaussian-slam`

## Questions
1. Which systems explicitly target **multi-robot / multi-agent / collaborative SLAM** with a Gaussian Splatting, Gaussian map, or closely related neural/point-Gaussian representation?
2. Which systems support moving robots/agents in a shared 3D environment using **RGB, RGB-D, stereo, or RGB+LiDAR** observations?
3. Which systems perform **online fusion into a shared Gaussian map** rather than offline reconstruction, post-hoc map merging, static multi-view training, or independent single-agent maps?
4. Which implementations are open source, partially released, promised-code, closed-source, or paper-only?
5. What is the fusion architecture: central server/shared map, decentralized map exchange, keyframe/pose-graph fusion, submap merging, Gaussian-level fusion, or learned/implicit map aggregation?
6. What pose assumptions are made: estimated per-agent poses, known ground-truth poses, external odometry, RGB-D/stereo depth, LiDAR-inertial odometry, loop closure, or global frame alignment?
7. What benchmarks, datasets, metrics, runtime, memory, communication, and scaling evidence are reported?
8. Which systems are credible Mosaic backend references for typed contracts around multi-robot observations, online fusion, shared map snapshots, provenance, and evaluation?

## Strategy
- Run a broad but targeted survey of 2023-2026 collaborative / multi-agent / multi-robot Gaussian SLAM, Gaussian Splatting SLAM, and distributed neural mapping systems.
- Prioritize systems with **online shared Gaussian-map fusion**; include non-open-source systems separately when they clarify the research frontier.
- Treat "multi-agent", "multi-robot", "multi-session", "multi-camera", and "multi-view" conservatively. A system only counts as the target class if multiple moving agents/robots contribute observations to a shared map or fused map representation.
- Extract implementation status directly from repositories, project pages, paper PDFs/arXiv pages, README files, license files, and benchmark tables.
- Cross-check candidate names against the existing 3DGS SLAM corpus, then search beyond it for systems the previous single-robot/multi-camera query may have missed.

Expected researcher allocations and dimensions:
- **R1: Multi-agent Gaussian SLAM paper/project survey.** Find named systems, papers, project pages, task definitions, and claimed fusion architecture.
- **R2: Code and license inventory.** Verify repositories, implementation maturity, licenses, dependencies, setup instructions, release status, and whether code actually implements collaborative fusion.
- **R3: Fusion architecture and modality analysis.** Classify RGB/RGB-D/stereo/RGB+LiDAR inputs, online vs offline fusion, central vs decentralized architecture, pose assumptions, and shared-map semantics.
- **R4: Benchmarks and robotics evidence.** Extract datasets, metrics, runtime, memory, communication bandwidth, scaling with number of agents, robot/simulator evidence, and baselines.

Expected rounds: one broad parallel round with four researchers, followed by one targeted correction/follow-up round if code availability, online-fusion claims, or benchmark evidence conflict.

## Acceptance Criteria
- [ ] Key candidate systems are identified, including open-source and paper-only systems.
- [ ] All target-class claims are grounded in at least two sources where possible, or explicitly labeled as single-source/paper-only.
- [ ] Each candidate is classified by modality, multi-robot support, online fusion status, shared Gaussian-map semantics, source availability, and Mosaic relevance.
- [ ] Open-source claims are verified against repository pages and license/readme evidence where available.
- [ ] Benchmarks include dataset, metric, number, runtime/context, and citation when available.
- [ ] Contradictions are identified and addressed, especially around "online", "multi-agent", "shared map", and "open source" claims.
- [ ] Non-Gaussian collaborative SLAM baselines are mentioned only when useful for fusion/evaluation context, not mixed into the main Gaussian implementation ranking.

## Task Ledger
| ID | Owner | Task | Status | Output |
|---|---|---|---|---|
| T1 | lead | Draft research plan and get confirmation | done | `outputs/.plans/multi-robot-gaussian-slam.md` |
| T2 | researcher R1 | Survey papers/project pages for multi-robot or multi-agent Gaussian SLAM systems | done | `outputs/multi-robot-gaussian-slam-research-papers.md` |
| T3 | researcher R2 | Inventory source code, licenses, dependencies, and implementation maturity | done | `outputs/multi-robot-gaussian-slam-research-code.md` |
| T4 | researcher R3 | Classify sensor modalities, online fusion architectures, shared-map semantics, and pose assumptions | done | `outputs/multi-robot-gaussian-slam-research-fusion.md` |
| T5 | researcher R4 | Extract benchmarks, datasets, runtime, memory, communication, and scaling evidence | done | `outputs/multi-robot-gaussian-slam-research-benchmarks.md` |
| T6 | lead | Evaluate evidence gaps and run targeted follow-up if needed | done | `outputs/multi-robot-gaussian-slam-research-followup-code.md`, `outputs/multi-robot-gaussian-slam-research-followup-architecture.md` |
| T7 | lead | Write cited final report and provenance | done | `outputs/multi-robot-gaussian-slam.md`, `outputs/multi-robot-gaussian-slam.provenance.md` |

## Verification Log
| Item | Method | Status | Evidence |
|---|---|---|---|
| Target-class definition: multi-robot online shared Gaussian map | Cross-read papers/project pages and inspect architecture claims | pass with notes | R1/R3 plus follow-up; MAC-Ego3D marked target/near-target, CoMA-SLAM included with license caveat, MANG-SLAM low confidence |
| Open-source availability and license status | Direct repository/project-page fetch; README/license inspection | pass with notes | R2 plus follow-up code report; CoMA-SLAM has no top-level license, HAMMER/MAGS/GRAND/MANG no public code confirmed |
| Online vs offline fusion classification | Cross-read method, experiment setup, demo docs, and code paths where available | pass with notes | R1/R3/follow-up; exact central vs distributed architecture remains uncertain for some paper-only systems |
| Sensor modality classification | Inspect paper setup, dataset loaders, README examples, and benchmark configs | pass with notes | R3/R4/follow-up; HAMMER heterogeneous modality details are partial in accessible text |
| Benchmark/runtime/communication numbers | Extract from paper tables/project pages; avoid unsupported or mixed metrics | pass with notes | R4; bandwidth sparse except HAMMER, memory/map size sparse except MAGiC-SLAM |
| Candidate completeness | Cross-check previous 3DGS SLAM catalogue plus new web/academic search results | pass with notes | R1-R4 plus targeted follow-up; rapidly moving 2025-2026 literature remains time-bounded |
| Final source URLs live | WebFetch verification of all final cited URLs | pass with notes | Core final cited URLs verified with WebFetch; some publisher pages expose only metadata or have implementation/code availability caveats |

## Decision Log
- 2026-05-19: Slug selected as `multi-robot-gaussian-slam`.
- 2026-05-19: Scope corrected from single-robot multi-camera 3DGS SLAM to multi-robot / multi-agent online shared Gaussian-map SLAM.
- 2026-05-19: Include RGB, RGB-D, stereo, and RGB+LiDAR systems; do not restrict to RGB-only because Mosaic may support multiple robot sensor packages.
- 2026-05-19: Include paper-only and closed-source systems for completeness, but rank open-source implementations separately for Mosaic backend usefulness.
- 2026-05-19: Treat shared Gaussian map fusion as the critical evidence gate; generic multi-view reconstruction, stereo, or independent per-agent maps do not satisfy the target unless a fused/shared map is documented.
- 2026-05-19: First broad round completed; targeted follow-up added because MAC-Ego3D, CoMA-SLAM, HAMMER, MAGS-SLAM, and MANG-SLAM had code/architecture classification gaps.
- 2026-05-19: MAC-Ego3D accepted as target-class or near-target by functional criteria despite title not saying SLAM; CoMA-SLAM accepted as relevant public-code Gaussian-surfel system with top-level license unresolved; HAMMER accepted as target-class but paper/project-only; MANG-SLAM retained as low-confidence bibliographic lead.
