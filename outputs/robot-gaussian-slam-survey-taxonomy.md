# LaTeX-ready architecture taxonomy for multi-robot online Gaussian SLAM

This note is drafted as paper-ready source material for the method/synthesis and architecture-taxonomy sections of a LaTeX survey on multi-robot / multi-agent online Gaussian SLAM. It synthesizes the current confirmed target-class evidence into a conservative taxonomy: central server fusion, distributed Gaussian consensus, submap-plus-pose-graph consistency, monocular compact-submap fusion, and heterogeneous semantic shared mapping.

## Target-class definition and notation

We define **multi-robot online Gaussian SLAM** as a class of systems in which multiple independently moving agents incrementally estimate local motion and map state while contributing to a shared Gaussian or Gaussian-like representation. Let the robot team be
\[
\mathcal{A}=\{1,\ldots,N\}, \qquad N\geq 2,
\]
where each agent \(i\in\mathcal{A}\) has a local body/camera frame \(\mathcal{F}_{i,t}\) at time \(t\), a local trajectory estimate \(\mathbf{T}_{i,t}\in SE(3)\), and a stream of observations
\[
\mathcal{Z}_i^{1:t}=\{z_{i,1},\ldots,z_{i,t}\}.
\]
Each observation may contain RGB, RGB-D, monocular RGB, stereo, LiDAR-derived depth, inertial cues, local SLAM poses, or semantic features depending on the system. A local online mapping backend produces a time-indexed Gaussian submap
\[
\mathcal{M}_{i,t}=\phi_i\!\left(\mathcal{Z}_i^{1:t},\mathbf{T}_{i,1:t}\right),
\]
where \(\mathcal{M}_{i,t}\) is a set or structured collection of Gaussian primitives, Gaussian surfels, keyframes, descriptors, semantic embeddings, and local provenance. The shared map is obtained through a fusion operator
\[
\mathcal{G}_t
=\Psi_t\!\left(\{\mathcal{M}_{i,t_i}\}_{i=1}^{N},\mathcal{C}_t,\mathcal{P}_t\right),
\]
where \(\mathcal{G}_t\) is the shared Gaussian map, \(\mathcal{C}_t\) denotes cross-agent constraints such as frame alignments, inter-robot loop closures, consensus factors, or pose-graph edges, and \(\mathcal{P}_t\) denotes policy variables such as communication budgets, keyframe selection, compaction, confidence thresholds, and semantic-code retention.

A system is target-class if it satisfies all of the following conditions:

1. **Multiple moving agents:** \(N\geq2\), with agents/robots/devices moving independently rather than cameras being fixed on one rigid rig.
2. **Online or incremental operation:** updates occur during mapping or in streaming increments, not only through offline reconstruction from a completed image set.
3. **Gaussian map state:** local or global state is represented by 3D Gaussian splats, Gaussian surfels, Gaussian submaps, or a closely related differentiable Gaussian map representation.
4. **Shared-map semantics:** the system defines a mechanism for shared map formation, e.g., server fusion, consensus, submap alignment, pose-graph consistency, Gaussian-level fusion, or semantic shared-map training.
5. **Cross-agent alignment:** the system handles the fact that local frames differ, through frame alignment, inter-agent loop closure, consensus optimization, or global pose-graph constraints.

This definition excludes static multi-view 3DGS training, ordinary stereo, single-robot multi-camera rigs, and independent per-agent mapping without shared Gaussian-map semantics.

## Method/synthesis framing

The synthesis treats multi-robot Gaussian SLAM as a factorization of four architectural responsibilities:

\[
\underbrace{\phi_i}_{\text{local tracking/mapping}}
\quad + \quad
\underbrace{\mu_i}_{\text{communication/update selection}}
\quad + \quad
\underbrace{\alpha}_{\text{cross-agent alignment}}
\quad + \quad
\underbrace{\Psi}_{\text{shared Gaussian fusion}}.
\]

Here \(\phi_i\) builds local map state from each agent's observations, \(\mu_i\) selects what each agent communicates, \(\alpha\) estimates transforms or constraints between local frames, and \(\Psi\) fuses local states into \(\mathcal{G}_t\). Existing systems differ less in whether they use Gaussians than in where these four responsibilities live:

- **Server-centric systems** put \(\alpha\) and \(\Psi\) on a central mapper that receives local observations, poses, keyframes, or compacted Gaussian state.
- **Distributed consensus systems** push \(\alpha\) and \(\Psi\) into repeated inter-agent alignment or consensus updates without a single authoritative mapper.
- **Submap/pose-graph systems** preserve local submaps and use loop-closure edges plus pose-graph optimization to maintain global consistency.
- **Compact monocular systems** prioritize \(\mu_i\), since monocular agents face scale ambiguity and must communicate bounded submap summaries rather than dense RGB-D maps.
- **Heterogeneous semantic systems** extend \(\mathcal{G}_t\) beyond geometry/radiance to include semantic or open-vocabulary codes while accepting mixed robot streams and local SLAM outputs.

The taxonomy is therefore organized by fusion contract rather than by sensor modality alone.

## Architecture taxonomy comparison

| Pattern | Representative systems | Fusion location | Fusion unit | Alignment mechanism | Strengths | Failure modes / open issues |
|---|---|---|---|---|---|---|
| **Central server fusion** | HAMMER, CoKo-SLAM | Server or central mapper | Robot observations plus local poses; local Gaussian maps; compacted Gaussians; keyframes | Server-side frame alignment, loop closure, rendered-depth or camera-depth registration, global optimization | Simple global authority; easier shared-map consistency; natural place for semantic-map training and compaction | Server bottleneck; network dependence; delayed global merge; privacy/data-volume pressure; single point of failure |
| **Distributed Gaussian consensus** | MAC-Ego3D | Peer/inter-agent optimization; no single mapper required by the taxonomy | Local Gaussian splat representations and consensus updates | Intra-agent and inter-agent Gaussian consensus; asynchronous cross-agent alignment | Avoids central bottleneck; naturally asynchronous; attractive for robot teams with intermittent infrastructure | Harder convergence analysis; duplicate Gaussians; stale maps; communication scheduling; conflict resolution |
| **Submap + pose graph** | GRAND-SLAM | Collaborative global-consistency layer; not necessarily proven as a central server | Local Gaussian submaps and inter/intra-robot loop-closure constraints | Pose-graph optimization over submap constraints | Clear separation between local dense mapping and global consistency; scalable conceptual model for large environments | Requires reliable loop detection; pose graph and Gaussian map can drift apart; map updates after graph changes need careful propagation |
| **Monocular compact-submap fusion** | MAGS-SLAM | Collaboration layer; central-vs-distributed deployment unresolved in available evidence | Local monocular Gaussian submaps and compact submap summaries | Geometry- and appearance-aware loop verification; occupancy-aware Gaussian fusion; scale handling | Works with RGB-only agents; communication-aware; avoids active depth sensors | Monocular scale ambiguity; lower geometric observability; compact summaries can discard useful evidence; deployment architecture still under-specified |
| **Heterogeneous semantic map** | HAMMER | Server-based online mapper | Asynchronous robot data streams, local SLAM poses, images/perception outputs, semantic embeddings | Global frame alignment without prior relative poses; shared metric-semantic 3DGS training | Best fit for mixed robot teams and agent-facing open-vocabulary queries; supports semantic shared map | Depends on local SLAM quality and semantic feature consistency; exact sensor APIs/code unavailable; semantic uncertainty and provenance need explicit treatment |

### Conservative system placement

Use the following placements in the paper unless new primary sources supersede them:

- **HAMMER:** central/server-based heterogeneous metric-semantic 3D Gaussian mapping with global frame alignment and no prior relative pose knowledge.
- **CoKo-SLAM:** central server fusion for RGB-D multi-agent Gaussian SLAM, with compacted Gaussians/keyframes and loop closure without an initial guess. Rendered-depth and camera-depth loop-closure variants belong here.
- **MAC-Ego3D:** distributed or consensus-oriented multi-agent Gaussian reconstruction/ego-motion system; target-class if the survey uses a functional definition including collaborative ego-motion plus Gaussian mapping, near-target if the paper title must explicitly say SLAM.
- **GRAND-SLAM:** submap plus pose-graph global-consistency architecture for multi-agent RGB-D 3DGS SLAM, with inter- and intra-robot loop closure. Do not overstate it as a central-server system unless citing a source that establishes that.
- **MAGS-SLAM:** monocular multi-agent Gaussian SLAM with local monocular Gaussian submaps, compact summaries, geometry/appearance loop verification, and occupancy-aware fusion; central-vs-distributed deployment remains unresolved from available evidence.

CoMA-SLAM and MANG-SLAM should not be used as confirmed target-class exemplars unless direct primary sources are added.

## LaTeX figure skeleton: architecture taxonomy

The following TikZ skeleton avoids exotic packages and should be compatible with the Google DeepMind science template when `tikz` is available. It uses only common TikZ libraries: `positioning`, `arrows.meta`, `fit`, and `calc`.

```latex
% Preamble additions, if not already present:
% \usepackage{tikz}
% \usetikzlibrary{positioning,arrows.meta,fit,calc}

\begin{figure*}[t]
\centering
\begin{tikzpicture}[
    font=\small,
    >=Latex,
    node distance=7mm and 9mm,
    agent/.style={draw, rounded corners, align=center, minimum width=21mm, minimum height=8mm, fill=blue!6},
    local/.style={draw, rounded corners, align=center, minimum width=25mm, minimum height=8mm, fill=green!6},
    fusion/.style={draw, rounded corners, align=center, minimum width=31mm, minimum height=9mm, fill=orange!10},
    shared/.style={draw, rounded corners, align=center, minimum width=34mm, minimum height=10mm, fill=purple!8},
    labelbox/.style={draw, rounded corners, align=center, fill=gray!8, inner sep=3pt},
    flow/.style={->, thick},
    weakflow/.style={->, dashed, thick}
]

% Agents and local maps
\node[agent] (a1) {Agent $1$\\$\mathcal{Z}_1^{1:t}$};
\node[agent, below=of a1] (a2) {Agent $2$\\$\mathcal{Z}_2^{1:t}$};
\node[agent, below=of a2] (an) {Agent $N$\\$\mathcal{Z}_N^{1:t}$};

\node[local, right=of a1] (m1) {Local map\\$\mathcal{M}_{1,t}$};
\node[local, right=of a2] (m2) {Local map\\$\mathcal{M}_{2,t}$};
\node[local, right=of an] (mn) {Local map\\$\mathcal{M}_{N,t}$};

\draw[flow] (a1) -- node[above] {$\phi_1$} (m1);
\draw[flow] (a2) -- node[above] {$\phi_2$} (m2);
\draw[flow] (an) -- node[above] {$\phi_N$} (mn);

% Communication/update selection
\node[labelbox, right=13mm of m2] (comm) {Update selection $\mu_i$\\keyframes, compact Gaussians,\\submaps, descriptors, poses};
\draw[flow] (m1.east) -- (comm.west);
\draw[flow] (m2.east) -- (comm.west);
\draw[flow] (mn.east) -- (comm.west);

% Fusion pattern choices
\node[fusion, right=15mm of comm, yshift=20mm] (central) {Central server fusion\\HAMMER, CoKo-SLAM};
\node[fusion, right=15mm of comm, yshift=7mm] (consensus) {Distributed consensus\\MAC-Ego3D};
\node[fusion, right=15mm of comm, yshift=-7mm] (submap) {Submap + pose graph\\GRAND-SLAM};
\node[fusion, right=15mm of comm, yshift=-20mm] (mono) {Compact monocular\\MAGS-SLAM};

\draw[flow] (comm.east) -- (central.west);
\draw[flow] (comm.east) -- (consensus.west);
\draw[flow] (comm.east) -- (submap.west);
\draw[flow] (comm.east) -- (mono.west);

% Alignment/fusion and shared map
\node[labelbox, right=16mm of consensus] (align) {Cross-agent alignment $\alpha$\\frame alignment, loop closure,\\consensus factors, pose graph};
\node[shared, right=15mm of align] (global) {Shared Gaussian map\\$\mathcal{G}_t=\Psi_t(\{\mathcal{M}_{i,t_i}\},\mathcal{C}_t,\mathcal{P}_t)$};

\draw[flow] (central.east) -- (align.west);
\draw[flow] (consensus.east) -- (align.west);
\draw[flow] (submap.east) -- (align.west);
\draw[flow] (mono.east) -- (align.west);
\draw[flow] (align) -- (global);

% Optional semantic layer
\node[labelbox, below=8mm of global] (sem) {Optional semantic posterior\\open-vocabulary codes, provenance, uncertainty};
\draw[weakflow] (global) -- (sem);

% Group boxes
\node[draw, rounded corners, fit=(a1)(a2)(an), inner sep=4pt, label=above:{Local robot streams}] {};
\node[draw, rounded corners, fit=(central)(consensus)(submap)(mono), inner sep=4pt, label=above:{Fusion contract taxonomy}] {};

\end{tikzpicture}
\caption{Taxonomy of multi-robot online Gaussian SLAM fusion contracts. Each agent converts local observations $\mathcal{Z}_i^{1:t}$ into a local Gaussian submap $\mathcal{M}_{i,t}$; an update-selection policy $\mu_i$ chooses bounded communication units; cross-agent alignment $\alpha$ supplies frame, loop-closure, consensus, or pose-graph constraints; and a fusion operator $\Psi_t$ produces the shared Gaussian map $\mathcal{G}_t$.}
\label{fig:multi_robot_gaussian_slam_taxonomy}
\end{figure*}
```

## LaTeX prose for taxonomy section

The architecture of multi-robot Gaussian SLAM systems can be understood as a choice of fusion contract over local Gaussian submaps. In central-server designs, agents upload observations, poses, keyframes, or compact Gaussian maps to a server that performs alignment and map fusion. HAMMER exemplifies this design for heterogeneous metric-semantic mapping: local robot SLAM outputs are aligned into a shared frame and used to train a server-side semantic 3D Gaussian map. CoKo-SLAM similarly uses a centralized server, but focuses on RGB-D Gaussian SLAM with compacted Gaussians, keyframes, and loop closure without an initial relative-pose guess.

Distributed designs replace the central fusion authority with consensus over Gaussian map state. MAC-Ego3D is the clearest example in the current evidence base: agents construct local Gaussian maps and use intra-agent and inter-agent Gaussian consensus to align and refine shared structure asynchronously. This pattern is appealing for infrastructure-limited robot teams, but makes convergence, stale updates, duplicate primitives, and communication scheduling first-class problems.

A third pattern preserves local submap autonomy and imposes global consistency through pose-graph constraints. GRAND-SLAM is best described this way: local Gaussian submaps are optimized while inter- and intra-robot loop closures feed a pose-graph optimization framework. This separation is attractive for large-scale mapping because the dense representation and the global topological consistency layer can evolve at different rates.

Monocular multi-agent systems emphasize compact submap exchange because RGB-only agents must handle scale ambiguity and cannot rely on active depth. MAGS-SLAM fits this class: local monocular Gaussian submaps are summarized compactly, cross-agent geometry and appearance are verified through loop checks, and occupancy-aware Gaussian fusion forms a coherent shared reconstruction. Available evidence confirms the fusion concept but does not fully resolve whether the implementation is centralized or distributed.

Finally, heterogeneous semantic mapping extends the shared map from geometry and radiance to agent-facing semantics. HAMMER is the strongest current representative: it targets heterogeneous robot teams, asynchronous data streams, local SLAM pose inputs, and a shared metric-semantic 3DGS map with open-vocabulary query support. This pattern is especially relevant when the shared map must serve downstream robots or language-conditioned agents rather than only rendering or localization metrics.

## Mermaid companion diagram

```mermaid
flowchart LR
    subgraph L[Local robot streams]
        A1[Agent 1<br/>Observations Z_1^{1:t}]
        A2[Agent 2<br/>Observations Z_2^{1:t}]
        AN[Agent N<br/>Observations Z_N^{1:t}]
    end

    subgraph M[Local online mapping]
        M1[Local Gaussian submap M_1,t]
        M2[Local Gaussian submap M_2,t]
        MN[Local Gaussian submap M_N,t]
    end

    A1 -->|phi_1| M1
    A2 -->|phi_2| M2
    AN -->|phi_N| MN

    M1 --> U[Update selection mu_i<br/>keyframes, compact Gaussians,<br/>submaps, descriptors, poses]
    M2 --> U
    MN --> U

    U --> C[Central server fusion<br/>HAMMER, CoKo-SLAM]
    U --> D[Distributed Gaussian consensus<br/>MAC-Ego3D]
    U --> P[Submap + pose graph<br/>GRAND-SLAM]
    U --> R[Monocular compact-submap fusion<br/>MAGS-SLAM]
    U --> S[Heterogeneous semantic map<br/>HAMMER]

    C --> X[Cross-agent alignment alpha<br/>frame alignment, loop closure,<br/>consensus factors, pose graph]
    D --> X
    P --> X
    R --> X
    S --> X

    X --> G[Shared Gaussian map G_t<br/>Psi_t({M_i}, C_t, P_t)]
    G -.-> Q[Optional agent-facing posterior<br/>semantics, provenance, uncertainty]
```

## Short caption alternatives

**Caption A:** Taxonomy of fusion contracts in multi-robot online Gaussian SLAM. Systems differ in the location of fusion, the communicated map unit, and the alignment mechanism that converts local Gaussian submaps into a shared map.

**Caption B:** From local observations to a shared Gaussian map. Each robot builds a local submap; communication policies select bounded updates; alignment estimates cross-agent constraints; and server, consensus, pose-graph, compact-submap, or semantic fusion produces the shared representation.

**Caption C:** Architecture patterns for collaborative Gaussian SLAM: central server fusion, distributed consensus, submap-plus-pose-graph consistency, monocular compact-submap fusion, and heterogeneous semantic shared mapping.
