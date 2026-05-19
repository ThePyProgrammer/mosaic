# SLAM Survey Notation and Algorithm Conventions

Date: 2026-05-19

## Findings

Recent SLAM, neural mapping, and Gaussian-splatting papers usually introduce the mathematical state before procedural descriptions. Common structures are named `Preliminaries`, `Problem Formulation`, `Approach`, or early `Method` subsections. These sections define coordinate frames, pose direction, observations, map state, rendering/projection models, and optimization objectives before tracking or mapping loops are described.

SLAM notation normally makes the pose group explicit, typically with transforms in `SE(3)`, and distinguishes observation streams, trajectory estimates, map variables, and measurement factors. Gaussian-splatting papers define the scene representation as a set of Gaussian primitives with means, covariances or scale/rotation parameters, opacity, and appearance before discussing densification, tracking, mapping, or rendering updates.

Algorithm boxes are less common for whole SLAM systems than for reusable procedures such as optimization, densification, rasterization, consensus, or fusion. When algorithm boxes are useful in a survey, the clearest convention is to provide `Input`, `Output`, and numbered procedural steps, while keeping detailed explanations and caveats in prose. Compact trigger/update/emit state-machine summaries are not typical paper style and obscure the mathematical objects being transformed.

## Implications for `research/slam-survey/main.tex`

- Define shared notation once in `Setting the Stage`: agents, time, frames, pose direction, observations, Gaussian primitives, maps, packets, constraints, policies, fusion operators, and metrics.
- Keep per-system algorithms as survey-level procedures, not executable source code.
- Use stable symbols across systems: `\mathcal{A}`, `\mathcal{Z}_i^{1:t}`, `\mathbf{T}_{0\leftarrow i,t}`, `\mathcal{M}_{i,t}`, `p_{i,t}`, `\mathcal{C}_t`, `\mathcal{P}_t`, `\Psi_t`, and `\mathcal{G}_t`.
- Introduce method-specific symbols locally only when needed, such as neighbor sets for consensus, semantic embeddings for HAMMER, or scale hypotheses for monocular MAGS-SLAM.
- Avoid unsupported claims about ablations; include ablation statements only when the cited evidence explicitly reports them.
