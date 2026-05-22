# Outline: SLAM Algorithm Appendix Refactor

Slug: `slam-algorithm-appendix`

## Proposed Title

**Appendix Refactor for Collaborative Gaussian SLAM Algorithms**

This is not a new standalone paper draft. It is an edit plan for `research/slam-survey/main.tex`: keep the main paper readable by replacing dense inline objectives with named helper functions, then define the helper procedures in an appendix.

## Target Paper Sections

Existing paper structure:

1. Introduction
2. Setting the Stage
3. Existing Works
4. Overall Architecture Taxonomy
5. Discussion and Conclusion
6. Bibliography

Proposed additions/edits:

1. **Setting the Stage**
   - Add a short paragraph: main algorithms use normalized helper functions; Appendix A expands the helper functions.
   - Keep the notation warning that algorithm boxes are survey-level procedures, not executable source code.

2. **Existing Works**
   - Replace confusing inline objectives in system algorithms with named functions.
   - Use system-specific helper names where local tracking differs materially:
     - `\operatorname{magic\_rgbd\_tracking}` for MAGiC-SLAM and CoKo inherited tracking.
     - `\operatorname{mac\_consensus\_tracking}` for MAC-Ego3D local pose/consensus alignment.
     - `\operatorname{mags\_monocular\_tracking}` for MAGS-SLAM local DROID/JDSA front end.
   - Keep generic operators for shared abstractions: `\operatorname{local\_mapping}`, `\operatorname{update\_selection}`, `\operatorname{cross\_agent\_alignment}`, `\operatorname{global\_fusion}`.
   - Replace inline argmin blocks for PGO/alignment/fusion with named helper calls where they distract from main flow.

3. **Overall Architecture Taxonomy**
   - Use the same named helper functions and refer to appendix algorithms for definitions.
   - Keep taxonomy algorithms concise and comparable.

4. **New Appendix: Expanded Survey Operators**
   - Insert before `\bibliography{references}`.
   - Define helper algorithms with labels and brief explanatory paragraphs.
   - Avoid overclaiming exact implementation details; label these as survey-level expansions derived from paper/source evidence.

## Proposed Appendix Structure

### Appendix A. Expanded Survey Operators

A.1 **How to Read These Operators**
- State that these are normalized survey functions, not executable source code.
- State that exact implementation details may differ across public repositories and paper-only systems.

A.2 **RGB-D Gaussian Tracking (`magic_rgbd_tracking`)**
- Applies to MAGiC-SLAM and CoKo-SLAM's inherited tracker.
- Inputs: RGB-D frame `z_{i,t}`, active local Gaussian map/submap, previous pose/state.
- Steps:
  1. Build colored point cloud from RGB-D frame.
  2. Initialize relative pose by dense frame-to-frame registration.
  3. Freeze Gaussian parameters.
  4. Render color/depth/alpha from active submap under candidate pose.
  5. Minimize masked RGB/depth tracking loss.
  6. Return updated local pose and trajectory fragment.
- Critical equation: masked `L_tracking` from MAGiC-SLAM.

A.3 **MAC-Ego3D Gaussian-Consensus Tracking (`mac_consensus_tracking`)**
- Applies to MAC-Ego3D local per-agent tracking as a survey-level abstraction.
- Inputs: RGB-D observations, local Gaussian map, previous pose, candidate-map policy.
- Steps:
  1. Select local candidate Gaussians in field of view / near pose.
  2. Associate observed RGB-D-derived points/Gaussians with map Gaussians.
  3. Refine pose through Gaussian/point-cloud alignment.
  4. Pass trackable evidence to local mapping/consensus.
  5. Return pose and local trajectory.
- Caveat: code evidence checked for MAC-Ego3D shows `Tracker.tracking()` with alignment calls; RGB/depth rendering losses are clearly evidenced in mapping, not necessarily in tracker code.

A.4 **MAGS Monocular Local Tracking (`mags_monocular_tracking`)**
- Applies to MAGS-SLAM.
- Inputs: monocular RGB sequence, local window, depth prior, scale state, active submap.
- Steps:
  1. Run DROID-style front end over sliding co-visibility window.
  2. Refine poses and depth maps using dense BA.
  3. Apply JDSA with learned depth prior to adjust depth and scale.
  4. Seed or update local Gaussians from inverse-depth keyframes.
  5. Freeze submap at keyframe/motion threshold and assign Sim(3) correction.
- Caveat: paper-level evidence only; code/data not verified as public.

A.5 **Local Gaussian Mapping (`local_mapping`)**
- Inputs: observations, trajectory, mapping parameters.
- Defines the common pattern: insert/adjust/prune Gaussians, optimize rendered color/depth/semantic losses, maintain submaps/keyframes.
- Mention system-specific variants: CoKo compaction, CoMA surfels, HAMMER semantic updates.

A.6 **Update Selection (`update_selection`)**
- Defines bounded packet construction.
- Covers Gaussian submaps, compact keyframe packets, descriptors, loop candidates, semantic packets, and monocular submap summaries.

A.7 **Cross-Agent Alignment (`cross_agent_alignment`)**
- Defines loop/candidate retrieval, geometric/appearance verification, relative transform estimation, and constraint creation.
- Include rendered-depth/camera-depth registration for CoKo, consensus association for MAC-Ego3D, Sim(3) submap alignment for MAGS.

A.8 **Global Fusion (`global_fusion`)**
- Defines central merge, distributed consensus update, pose-graph submap placement, occupancy-aware fusion, and semantic conflict resolution.
- Use named functions in main algorithms: `\operatorname{pose\_graph\_optimize}`, `\operatorname{occupancy\_fusion}`, `\operatorname{semantic\_gaussian\_update}` only if they improve clarity.

## Key Claims to Make

1. Main system algorithms are **survey-level normalizations**, not executable implementations.
2. `local_tracking_i` is too generic when systems use different local front ends; named helper functions reduce ambiguity.
3. MAGiC-SLAM and CoKo-SLAM share an RGB-D rendered-loss tracking family.
4. MAC-Ego3D local tracking should be described as Gaussian-consensus / geometric local pose alignment unless stronger evidence proves a MAGiC-style rendered-loss tracker.
5. MAGS-SLAM local tracking is monocular scale/depth-aware front-end work, not active RGB-D tracking.
6. Appendix algorithms should explain enough mechanics for readers without bloating the main comparison algorithms.

## Source Material to Draw From

Primary local files:

- `research/slam-survey/main.tex` — current paper and algorithms.
- `research/slam-survey/references.bib` — existing citations.
- `outputs/magic-local-tracking.md` — verified comparison of MAGiC photometric-depth tracking vs normalized `local_tracking`.
- `outputs/magic-local-tracking.provenance.md` — verified source status and claim caveats.
- `outputs/magic-local-tracking-research-*.md` — per-system evidence slices.

Primary external URLs already verified in the recent review:

- MAGiC-SLAM CVPR page and PDF.
- MAC-Ego3D arXiv page/HTML and repository tracker/mapper files.
- CoKo-SLAM arXiv page/HTML and repository.
- MAGS-SLAM arXiv page/HTML and project page.

No new web research is required unless adding appendix details for CoMA-SLAM, HAMMER, or GRAND-SLAM beyond the current paper text.

## Verification Log

| Critical claim / artifact | Verification method | Status |
|---|---|---:|
| Main algorithms currently mix generic operators and inline objectives | Read `research/slam-survey/main.tex`; grep algorithm captions and operators | verified |
| `local_tracking_i` is survey notation | Existing paper lines around notation and algorithm caveat; `outputs/magic-local-tracking.md` | verified |
| MAGiC tracker is RGB-D dense registration + rendered RGB-D pose refinement | `outputs/magic-local-tracking.md` and provenance; MAGiC CVPR source | verified in prior review |
| CoKo tracking is inherited from MAGiC | `outputs/magic-local-tracking.md`; CoKo arXiv HTML | verified in prior review |
| MAC tracker evidence should be stated cautiously | MAC tracker/mapper notes in `outputs/magic-local-tracking.md` | verified in prior review |
| MAGS local stage is monocular DROID/JDSA, code unavailable | MAGS arXiv/project notes in `outputs/magic-local-tracking.md` | verified in prior review |
| Appendix labels compile and are referenced correctly | Run LaTeX build after edits | pending |
| No unsupported new numerics introduced | Diff/review edited text before delivery | pending |
| Main algorithms remain concise and readable | Manual read of edited algorithms | pending |

## Editing Plan After Approval

1. Read the relevant sections of `research/slam-survey/main.tex` around notation, system algorithms, taxonomy algorithms, and bibliography boundary.
2. Add a concise appendix-forward reference in Setting the Stage / Existing Works.
3. Replace main algorithm confusing inline objectives with named helper calls.
4. Insert Appendix A before the bibliography with expanded helper algorithms.
5. Avoid new unsupported numbers; cite existing bibliography keys.
6. Run a LaTeX build if the local environment supports it, or at minimum grep/check labels and syntax-sensitive strings.
7. Summarize exact edits and any verification limits.
