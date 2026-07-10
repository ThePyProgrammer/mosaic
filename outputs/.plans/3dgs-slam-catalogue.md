# Draft Outline: 3DGS SLAM Model Catalogue

## Slug
`3dgs-slam-catalogue`

## Proposed title
**A Catalogue of Online and Incremental 3D Gaussian Splatting SLAM Systems for Moving Robotic Cameras**

## Goal
Produce a paper-style Markdown draft at `papers/3dgs-slam-catalogue.md` that turns the completed deep research into a compact catalogue of 3DGS SLAM systems/models, emphasizing modality, code/license status, online behavior, multi-camera relevance, benchmarks, and Mosaic backend fit.

## Proposed sections
1. **Title**
2. **Abstract** — one-paragraph summary: native multi-camera 3DGS SLAM is rare; AgriGS-SLAM is the only verified native multi-camera robot-rig case; most systems are monocular/RGB-D/stereo baselines.
3. **Problem Statement** — why Mosaic needs a catalogue: avoid conflating RGB-D/stereo/multi-agent with synchronized multi-camera robot rigs.
4. **Related Work** — group systems into RGB-D, monocular/RGB-only, stereo/RGB-D real-time, LiDAR/IMU robotics, multi-agent, and native multi-camera.
5. **Catalogue Method / Synthesis Criteria** — define columns and conservative classification rules.
6. **Evidence Catalogue** — primary table of systems with columns:
   - System
   - Year / venue where known
   - Public code status
   - License / reuse risk
   - Sensor modality
   - Online / real-time status
   - Native multi-camera fit
   - Benchmarks / datasets
   - Mosaic fit
   - Source refs
7. **Capability Taxonomy Figure** — Mermaid diagram grouping native, adaptable, robotics multi-sensor, multi-agent, and single-stream baselines.
8. **Benchmark Summary Table** — compact benchmark rows for the systems with reliable benchmark evidence.
9. **Limitations** — rapidly changing source landscape, incomplete code releases, inconsistent FPS terminology, AgriGS per-sequence table extraction caveat, legal/license caveats.
10. **Conclusion** — recommended shortlist for Mosaic: AgriGS-SLAM as native multi-camera candidate; SplaTAM/MonoGS/Gaussian-SLAM/Photo-SLAM/RTG-SLAM/Splat-SLAM as baselines; Gaussian-LIC/DiskChunGS/VINGS-Mono as robotics references.
11. **Sources Appendix** — direct URLs for primary references.

## Key claims to make
1. **Native multi-camera claim:** AgriGS-SLAM is the only verified native robot-mounted multi-camera 3DGS SLAM implementation found in the completed research.
2. **Conflation warning:** Stereo, RGB-D, multi-agent, and temporal multi-view input are not equivalent to synchronized multi-camera robot rigs.
3. **Baseline claim:** SplaTAM, MonoGS, Gaussian-SLAM, Photo-SLAM, RTG-SLAM, GS-SLAM, and Google Splat-SLAM are the main baseline systems for Mosaic contract and benchmark design.
4. **Code availability correction:** RTG-SLAM has public GPL-3.0 code; GS-SLAM full SLAM implementation was not confirmed; VIGS-SLAM code link is inaccessible while VINGS-Mono is separate and public.
5. **Benchmark caution:** Rendering FPS, tracking FPS, system FPS, and final refinement time must be recorded separately.
6. **Mosaic recommendation:** Keep real backends behind optional subprocess/container boundaries due CUDA/C++/ROS/license fragility.

## Source material to draw from
- `outputs/multiview-3dgs-slam.md` — final synthesized report and verified final source list.
- `outputs/multiview-3dgs-slam.provenance.md` — source counts and verification notes.
- `outputs/multiview-3dgs-slam-research-papers.md` — broad paper/project landscape.
- `outputs/multiview-3dgs-slam-research-code.md` — repository, license, dependency, and maintenance evidence.
- `outputs/multiview-3dgs-slam-research-multicamera.md` — multi-camera/native-vs-adaptable classification.
- `outputs/multiview-3dgs-slam-research-benchmarks.md` — benchmark tables and runtime caveats.
- `outputs/multiview-3dgs-slam-research-agrigs-followup.md` — AgriGS-SLAM native multi-camera evidence.
- `outputs/multiview-3dgs-slam-research-corrections.md` — source/license/name corrections.

## Verification log
| Item | Verification method | Status | Evidence |
|---|---|---|---|
| AgriGS-SLAM native multi-camera classification | Reuse final verified report and AgriGS follow-up; verify source URLs again only if final draft adds new claims | pending | `outputs/multiview-3dgs-slam.md`, AgriGS sources |
| Catalogue includes all systems from final report and major intermediate tables | Cross-check against final report main inventory plus research table names | pending | final draft checklist |
| License/code availability claims | Reuse corrections report; avoid stronger claims than verified | pending | `outputs/multiview-3dgs-slam-research-corrections.md` |
| Benchmark numbers | Use only numbers already present in final verified report; do not add new numerics without fresh verification | pending | `outputs/multiview-3dgs-slam.md` benchmark section |
| Source URLs live | Use WebFetch for the final primary source URLs cited in the paper | pending | final WebFetch results |
| Final draft exists in required path | Check `papers/3dgs-slam-catalogue.md` exists and contains required sections | pending | final file check |

## No-new-research assumption
The existing deep research outputs are sufficient. New WebSearch/Agent work is not planned unless final cross-check reveals missing systems or unsupported claims.
