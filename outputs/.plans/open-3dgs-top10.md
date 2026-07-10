# Comparison Plan: Top 10 Open-Source 3DGS SLAM Systems

## Slug
`open-3dgs-top10`

## Goal
Rank the top 10 3D Gaussian Splatting SLAM algorithms/systems with open-source implementations from the completed catalogue, optimized for Mosaic relevance and implementation usefulness.

## Sources to compare
Primary source material will come from existing artifacts, not new research:

1. `papers/3dgs-slam-catalogue.md` — consolidated model catalogue with 55 system rows and 60 source URLs.
2. `outputs/multiview-3dgs-slam.md` — verified final research report.
3. `outputs/multiview-3dgs-slam-research-code.md` — code/license/dependency inventory.
4. `outputs/multiview-3dgs-slam-research-multicamera.md` — native vs adaptable multi-camera classification.
5. `outputs/multiview-3dgs-slam-research-benchmarks.md` — benchmark and runtime evidence.
6. `outputs/multiview-3dgs-slam-research-corrections.md` — source/license/name corrections.

## Candidate pool
Open-source/public implementation candidates likely to be ranked:
- AgriGS-SLAM
- SplaTAM
- MonoGS / Gaussian Splatting SLAM
- Gaussian-SLAM
- Photo-SLAM
- RTG-SLAM
- Google Splat-SLAM
- DiskChunGS
- Gaussian-LIC
- VINGS-Mono
- HI-SLAM2
- WildGS-SLAM
- OpenGS-SLAM
- LSG-SLAM
- SEGS-SLAM
- DG-SLAM
- Semantic/variant systems if they outrank the above on Mosaic fit

Systems with no confirmed full implementation, inaccessible code, or only paper-level evidence will be excluded or mentioned below the top 10, e.g. GS-SLAM full implementation, VIGS-SLAM code link, and newer promised-code systems.

## Evaluation dimensions
Rank by a weighted qualitative score:

1. **Open implementation confidence** — public repo, runnable code, source clarity.
2. **License/reuse friendliness** — permissive licenses score higher; GPL/custom/non-commercial risks lower but may still rank for reference value.
3. **Mosaic modality fit** — native multi-camera > stereo/RGB-D/ROS > single RGB-D > monocular > niche domain.
4. **Online/SLAM relevance** — online tracking/mapping and backend lifecycle relevance.
5. **Benchmark evidence** — datasets, ATE/rendering/runtime/memory evidence.
6. **Robotics relevance** — robot datasets, ROS/external pose, LiDAR/IMU, embedded/field evidence.
7. **Integration risk** — CUDA/C++/ROS/license/dataset coupling; lower risk ranks higher when other factors tie.

## Expected output structure
1. Short note on ranking criteria.
2. Top 10 ranked table with columns:
   - Rank
   - System
   - Why it ranks here
   - Modality
   - License / code status
   - Multi-camera relevance
   - Benchmark evidence
   - Caveats
   - Confidence
3. Comparison matrix covering required dimensions:
   - Source
   - Key claim
   - Evidence type
   - Caveats
   - Confidence
4. Agreement / disagreement / uncertainty notes.
5. Sources section with direct URLs.
6. Chat response will include the same ranked top 10 in concise form.

## Verification plan
- Reuse already verified sources where possible.
- Fresh WebFetch check for the 10 selected repository/source URLs before final answer.
- Artifact check: verify `outputs/open-3dgs-top10-comparison.md` exists and includes the top 10 table, comparison matrix, and Sources section.

## No-new-research assumption
No new discovery research is needed. This is a comparison/ranking over the completed catalogue and previously verified source set.
