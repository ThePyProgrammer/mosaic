# Review: Algorithm-Flow Ordering in the SLAM Survey

Date: 2026-05-22

## Verdict

The current method order is defensible, but the strongest scholarly flow would be taxonomy-first with the only explicit lineage edge made visually obvious: MAGiC-SLAM before CoKo-SLAM. The key finding is narrow: among the surveyed methods, the only clearly evidenced algorithm/code lineage is **CoKo-SLAM building on MAGiC-SLAM**. Other pairings show shared architecture or problem setting, not a source-backed build-on relationship.

No FATAL issues were found. The main revision need is explanatory: the draft should tell readers whether the section order is evidence-driven, dependency-aware, or taxonomy-driven so that similarity between methods is not mistaken for inheritance.

## Inline Review Annotations

### 1. MAGiC-SLAM before CoKo-SLAM is required

**Severity: MAJOR**

MAGiC-SLAM appears before CoKo-SLAM in the current draft, which is correct. The review evidence supports CoKo-SLAM as the only explicit successor among the surveyed systems: the CoKo-SLAM repository states that its codebase is based on MAGiC-SLAM, and the draft already encodes this through the inherited `magic_rgbd_tracking` step in the CoKo-SLAM algorithm. This is a real lineage edge, not just topical similarity.

**Revision:** Keep MAGiC-SLAM before CoKo-SLAM. If preserving the current order, add a short transition before CoKo-SLAM: “CoKo-SLAM is presented after MAGiC-SLAM because it inherits the MAGiC-SLAM tracking/codebase lineage while changing communication and global fusion.”

### 2. MAC-Ego3D does not need to precede CoMA-SLAM as a parent

**Severity: MINOR**

MAC-Ego3D and CoMA-SLAM are naturally adjacent under a distributed/consensus family, but the evidence does not support saying CoMA-SLAM builds on MAC-Ego3D. The relationship is architectural proximity: distributed multi-agent Gaussian-map consistency, neighbor/agent exchange, and communication-aware collaboration.

**Revision:** If the draft groups them together, frame this as a distributed-family grouping, not a dependency chain. Avoid language such as “CoMA-SLAM extends MAC-Ego3D” unless a primary source is later found.

### 3. GRAND-SLAM resembles MAGiC-SLAM at the submap/pose-graph level but is not evidenced as a derivative

**Severity: MAJOR**

GRAND-SLAM and MAGiC-SLAM both fit a Gaussian-submap plus loop/pose-graph consistency pattern. That makes them conceptually comparable, and GRAND-SLAM could reasonably be moved closer to MAGiC-SLAM if the draft is reorganized by mechanism. However, inspected sources do not establish that GRAND-SLAM builds on MAGiC-SLAM or CoKo-SLAM.

**Revision:** Present GRAND-SLAM as a submap-plus-pose-graph consistency system, not as a descendant of MAGiC-SLAM. If moving it earlier, introduce the move as taxonomy-based: “A related but not derivative submap/pose-graph line is GRAND-SLAM.”

### 4. MAGS-SLAM should remain separated by modality, not lineage

**Severity: MINOR**

MAGS-SLAM shares compact-summary and cross-agent alignment concerns with CoKo-SLAM and submap concerns with RGB-D systems, but it changes the sensing regime to monocular/RGB-only SLAM and introduces scale-aware collaboration. The evidence does not support a build-on claim from CoKo-SLAM or GRAND-SLAM.

**Revision:** Keeping MAGS-SLAM last is reasonable because it is a modality outlier and has more provisional reproducibility evidence. If taxonomy-first ordering is used, place it after compact communication/submap fusion discussion as the monocular variant.

### 5. HAMMER is a semantic/global-map outlier rather than a descendant of central-server Gaussian SLAM

**Severity: MINOR**

HAMMER shares server-side alignment and global map update concerns with centralized systems, but its heterogeneous device and semantic-map framing is distinct. The inspected sources do not establish surveyed-method lineage from MAGiC-SLAM, CoKo-SLAM, or GRAND-SLAM.

**Revision:** Keep HAMMER in a heterogeneous semantic mapping position. Do not use its server architecture alone as evidence that it follows from MAGiC-SLAM or CoKo-SLAM.

## Novelty and Significance

The draft’s algorithm ordering is significant because it shapes how readers infer the field’s evolution. The current order begins with public RGB-D baselines, then moves through compact communication, distributed surfel optimization, heterogeneous semantics, large-scale submap consistency, and monocular collaboration. That is a defensible evidence/readiness flow, but it is not self-evidently chronological or dependency-first.

A taxonomy-first order would be more transparent for a survey:

1. Central-server RGB-D Gaussian submap systems: MAGiC-SLAM, CoKo-SLAM
2. Distributed/consensus Gaussian-map systems: MAC-Ego3D, CoMA-SLAM
3. Submap-plus-pose-graph large-scale consistency: GRAND-SLAM
4. Heterogeneous semantic global mapping: HAMMER
5. Monocular compact-submap fusion: MAGS-SLAM

This ordering preserves the only explicit dependency while making clear that most other relationships are design-pattern relationships.

## Empirical Rigor and Baselines

The ordering should not imply empirical dominance. The methods report different slices of ATE, rendering quality, communication, memory, latency, and scale. MAGiC-SLAM and MAC-Ego3D are useful early anchors because they are comparatively auditable public baselines, but that does not make later systems descendants or strictly stronger successors.

Where a method resembles an earlier one, the draft should ask whether it directly compares against that predecessor. In particular:

- CoKo-SLAM should be discussed against MAGiC-SLAM because lineage and inherited tracking are explicit.
- GRAND-SLAM can be compared with MAGiC-SLAM as a submap/pose-graph family member, but not treated as dependent.
- CoMA-SLAM can be compared with MAC-Ego3D as distributed multi-agent Gaussian mapping, but not framed as an extension without source evidence.
- MAGS-SLAM can be compared with RGB-D collaborative systems to show the modality shift, not lineage.

## Reproducibility Concerns

The ordering should account for evidence quality. MAGiC-SLAM, MAC-Ego3D, CoKo-SLAM, and CoMA-SLAM have public repositories or partly auditable implementation artifacts; HAMMER, GRAND-SLAM, and MAGS-SLAM are less implementation-auditable from the inspected sources. This supports the current choice to begin with public-code anchors, but the paper should state that the ordering partly reflects evidence maturity if that is the intended flow.

## Logical Gaps or Unsupported Claims

### MAJOR: Similarity is sometimes close enough that readers may infer unsupported lineage

The draft uses shared survey operators such as local tracking, update selection, cross-agent alignment, and global fusion. Those abstractions are useful, but they can make unrelated systems look more directly connected than the sources justify.

**Revision:** Add one sentence before the method list: “Except where explicitly noted, shared operators denote survey-level functional roles rather than code or algorithm inheritance.”

### MINOR: Current order mixes evidence maturity and taxonomy

The method order starts with mature public baselines but later switches into pattern/modality coverage. This is acceptable, but the organizing principle should be declared.

**Revision:** Either preserve the current order with a sentence explaining it, or reorder the method subsections taxonomy-first.

## Concrete Revision Plan

1. Add an ordering rationale at the start of `Existing Works`: the methods are ordered by architectural flow and evidence maturity, not as a chronology or full dependency chain.
2. Keep MAGiC-SLAM before CoKo-SLAM and make the explicit inheritance sentence visible in CoKo-SLAM’s subsection.
3. Decide between two section orders:
   - Minimal-change: MAGiC-SLAM, MAC-Ego3D, CoKo-SLAM, CoMA-SLAM, HAMMER, GRAND-SLAM, MAGS-SLAM.
   - Taxonomy-first: MAGiC-SLAM, CoKo-SLAM, MAC-Ego3D, CoMA-SLAM, GRAND-SLAM, HAMMER, MAGS-SLAM.
4. Add caveats that MAC-Ego3D/CoMA-SLAM, MAGiC-SLAM/GRAND-SLAM, CoKo-SLAM/MAGS-SLAM, and centralized systems/HAMMER are architectural comparisons rather than evidenced inheritance relationships.
5. Keep the appendix operators, but explicitly state that shared operators are survey abstractions unless a source states inherited implementation or method lineage.

## Direct Answer

Beyond **CoKo-SLAM building on MAGiC-SLAM**, no other clear build-on relationship among the surveyed algorithms was supported by the inspected sources. The other relationships are best described as taxonomy-level relationships:

- MAC-Ego3D and CoMA-SLAM: distributed/collaborative Gaussian-map family.
- MAGiC-SLAM and GRAND-SLAM: RGB-D Gaussian submap plus loop/pose-graph consistency family.
- CoKo-SLAM and MAGS-SLAM: compact communication/cross-agent alignment concerns, but different sensing regimes.
- HAMMER and centralized systems: server/global-map alignment family, but with heterogeneous semantic mapping.

## Sources

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
