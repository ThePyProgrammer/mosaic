# SLAM Survey Notation Rewrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite `research/slam-survey/main.tex` into a conventional academic survey with formal shared notation, readable per-system algorithms, and prose architecture taxonomy sections.

**Architecture:** This is a single-document LaTeX rewrite. The plan preserves the existing paper assets and bibliography while replacing the section structure, notation setup, algorithm bodies, and taxonomy/discussion prose in `main.tex`.

**Tech Stack:** LaTeX (`googledeepmind.cls`, `natbib`, `amsmath`, custom `algorithm` float), shell search commands, and local LaTeX compilation if available.

---

## File Structure

- Modify: `research/slam-survey/main.tex`
  - Replace current section layout with Introduction, Setting the Stage, Existing Works, Overall Architecture Taxonomy, Discussion and Conclusion.
  - Rewrite all algorithm environments to use `Input`, `Output`, and ordered procedural steps.
  - Remove removed standalone sections and benchmark/taxonomy tables.
- Leave unchanged unless a compile error requires a minimal fix: `research/slam-survey/references.bib`
- Read-only reference: `docs/superpowers/specs/2026-05-19-slam-survey-notation-rewrite-design.md`

## Task 1: Focused Literature and Notation Check

**Files:**
- Read: `research/slam-survey/main.tex`
- Read: `research/slam-survey/references.bib`
- Create if helpful: `outputs/slam-survey-notation-conventions.md`

- [ ] **Step 1: Search for conventions in SLAM/vision papers**

Use web search or available paper sources to confirm how recent SLAM/vision papers typically present notation and algorithms. Look specifically for: a problem formulation/preliminaries section, shared symbol definitions before algorithms, algorithm boxes with inputs/outputs, and method-specific deviations introduced locally.

- [ ] **Step 2: Extract paper-local constraints**

Review `research/slam-survey/main.tex` and note every symbol currently used in algorithm blocks: agent index, time index, observation, pose, local map, shared map, packet, constraints, loop edges, budget, alignment transform, and fusion operator.

- [ ] **Step 3: Record concise findings**

If a research note is created, write no more than one page to `outputs/slam-survey-notation-conventions.md`: conventions found, implications for this paper, and any unsupported claims to avoid. Do not add this note to the paper.

## Task 2: Rewrite Section Skeleton and Formal Setting

**Files:**
- Modify: `research/slam-survey/main.tex:52-101`

- [ ] **Step 1: Keep introduction mostly intact**

Preserve the Introduction text, editing only if needed for flow into the new `Setting the Stage` section.

- [ ] **Step 2: Replace current problem/background/method sections**

Delete standalone `Problem Statement and Target Class`, `Background and Related Work`, and `Survey Method and Evidence Criteria` sections. Insert `\section{Setting the Stage}` immediately after Introduction.

- [ ] **Step 3: Add formal notation**

In `Setting the Stage`, define:

```tex
\mathcal{A}=\{1,\ldots,N\},\quad t\in\mathbb{N},\quad
\mathcal{F}_{i,t},\quad \mathcal{F}_0,\quad
\mathbf{T}_{0\leftarrow i,t}\in SE(3),\quad
\mathcal{Z}_i^{1:t}=\{z_{i,1},\ldots,z_{i,t}\}.
```

Also define observation components, trajectory estimates, Gaussian primitives, local maps, submaps, packets, constraints, fusion, policies, and reported metrics in prose plus displayed equations.

- [ ] **Step 4: Preserve target-class scope**

Keep the target-class inclusion/exclusion logic: multiple independently moving agents, online/incremental operation, Gaussian or Gaussian-like map state, shared-map semantics, and cross-agent alignment.

## Task 3: Rename Candidate Systems to Existing Works

**Files:**
- Modify: `research/slam-survey/main.tex:102-256`

- [ ] **Step 1: Rename section**

Change `\section{Candidate Systems}` to `\section{Existing Works}`.

- [ ] **Step 2: Adjust section preamble**

Replace the current preamble with text explaining that each system is summarized as a survey-level procedure over the shared notation, not executable source code.

## Task 4: Rewrite Per-System Algorithms

**Files:**
- Modify: all `algorithm` environments in `research/slam-survey/main.tex`

- [ ] **Step 1: Rewrite MAGiC-SLAM algorithm**

Use this structure:

```tex
\begin{algorithm}[H]
\caption{MAGiC-SLAM}
\label{alg:magic-slam}
\small
\noindent\textbf{Input:} RGB-D streams $\{\mathcal{Z}_i^{1:t}\}_{i\in\mathcal{A}}$, local map states $\{\mathcal{M}_{i,t-1}\}$, keyframe sets $\{\mathcal{K}_{i,t}\}$.\\
\textbf{Output:} Globally aligned Gaussian map $\mathcal{G}_t$ and optimized submap poses $\{\mathbf{P}_v\}$.
\begin{enumerate}[leftmargin=*,nosep]
  \item For each agent $i$, estimate the current pose $\hat{\mathbf{T}}_{0\leftarrow i,t}$ from the new RGB-D frame and the previous local Gaussian map.
  \item Update the local submap $\mathcal{M}_{i,t}$ with accepted RGB-D observations and selected keyframes.
  \item Select a bounded packet $p_{i,t}=\mu_i(\mathcal{K}_{i,t},\mathcal{M}_{i,t};b_i)$ and transmit it to the server.
  \item Detect intra- and inter-agent loop closures and append verified relative-pose factors to $\mathcal{C}_t$.
  \item Solve a robust pose-graph problem over submap poses,
  \[
  \{\mathbf{P}_v^\star\}=\arg\min_{\{\mathbf{P}_v\}}\sum_{e\in\mathcal{E}_t\cup\mathcal{C}_t}\rho\!\left(\|r_e(\{\mathbf{P}_v\})\|^2\right).
  \]
  \item Transform local submaps by the optimized poses and merge them into $\mathcal{G}_t=\Psi_t(\{\mathbf{P}_v^\star\mathcal{M}_v\},\mathcal{C}_t,\mathcal{P}_t)$.
\end{enumerate}
\end{algorithm}
```

- [ ] **Step 2: Rewrite MAC-Ego3D algorithm**

Use `Input`, `Output`, and ordered steps for local tracking, intra-agent regularization, packet exchange, inter-agent consensus, and shared publication. Use symbols $\mathcal{N}_t(i)$, $h_{i,t}$, and $C_{\mathrm{inter}}$ only after tying them to the shared notation.

- [ ] **Step 3: Rewrite CoKo-SLAM algorithm**

Use ordered steps for local map/keyframe update, compact packet selection, association, alignment with rendered-depth/camera-depth evidence, redundant Gaussian pruning, and global fusion.

- [ ] **Step 4: Rewrite CoMA-SLAM algorithm**

Use ordered steps for local Gaussian-surfel submap update, loop detection, distributed packet exchange, distributed keyframe/submap optimization, and shared surfel-map commitment.

- [ ] **Step 5: Rewrite HAMMER algorithm**

Use ordered steps for buffering heterogeneous packets, estimating global-frame alignment, assimilating observations, updating metric-semantic Gaussians, and serving bounded map views.

- [ ] **Step 6: Rewrite GRAND-SLAM algorithm**

Use ordered steps for local RGB-D tracking, submap spawning, local Gaussian optimization, inter/intra-robot loop detection, pose-graph optimization, and global propagation.

- [ ] **Step 7: Rewrite MAGS-SLAM algorithm**

Use ordered steps for monocular tracking and scale hypothesis, local Gaussian update, compact summary selection, geometry/appearance verification, scale-aware alignment, and occupancy-aware fusion.

## Task 5: Replace Table-Led Architecture Taxonomy

**Files:**
- Modify: `research/slam-survey/main.tex:257-389`

- [ ] **Step 1: Rename section**

Change `\section{Architecture Taxonomy}` to `\section{Overall Architecture Taxonomy}`.

- [ ] **Step 2: Remove the taxonomy table**

Delete `\Cref{tab:architecture_taxonomy}` prose and the entire `tab:architecture_taxonomy` table. Keep the figure only if it still supports the prose; otherwise remove it if it interrupts the section.

- [ ] **Step 3: Remove Benchmark Synthesis**

Delete `\section{Benchmark Synthesis}`, its benchmark table, and its benchmark-only explanatory paragraphs.

- [ ] **Step 4: Add pattern subsections**

Add subsections for:

```tex
\subsection{Central-Server Submap and Gaussian Fusion}
\subsection{Distributed Gaussian Consensus}
\subsection{Submap-Plus-Pose-Graph Consistency}
\subsection{Compact Communication and Monocular Submap Fusion}
\subsection{Heterogeneous Semantic Shared Gaussian Mapping}
```

Each subsection should identify representative systems, express the pattern with $\phi_i$, $\mu_i$, $\alpha$, $\Psi_t$, discuss tradeoffs, and mention ablations only where supported.

## Task 6: Merge Discussion and Conclusion

**Files:**
- Modify: `research/slam-survey/main.tex:390-408`

- [ ] **Step 1: Remove standalone Limitations**

Delete `\section{Limitations}` and its paragraphs.

- [ ] **Step 2: Merge final sections**

Replace `\section{Discussion}` and `\section{Conclusion}` with `\section{Discussion and Conclusion}`.

- [ ] **Step 3: Add forward-looking synthesis**

Include concise paragraphs on standardized systems reporting, modular evaluation of tracking/update-selection/alignment/fusion, robustness under stale communication, semantic/provenance-aware shared maps, and architecture-pattern comparison instead of universal ranking.

## Task 7: Validate the Rewrite

**Files:**
- Read/verify: `research/slam-survey/main.tex`
- Generated if successful: `research/slam-survey/build/main.pdf`

- [ ] **Step 1: Check removed headings**

Run:

```bash
grep -n "Survey Method\|Benchmark Synthesis\|Limitations\|Candidate Systems\|Architecture Taxonomy" research/slam-survey/main.tex
```

Expected: no matches for removed headings; `Overall Architecture Taxonomy` may match if using a broad pattern, so inspect manually.

- [ ] **Step 2: Check old algorithm labels**

Run:

```bash
grep -n "Trigger:\|Update:\|Emits:" research/slam-survey/main.tex
```

Expected: no matches.

- [ ] **Step 3: Check new section order**

Run:

```bash
grep -n "^\\\\section" research/slam-survey/main.tex
```

Expected order: Introduction, Setting the Stage, Existing Works, Overall Architecture Taxonomy, Discussion and Conclusion.

- [ ] **Step 4: Compile LaTeX**

Run from `research/slam-survey`:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

If `latexmk` is unavailable, try:

```bash
tectonic -X compile main.tex --outdir build
```

Expected: build succeeds and updates `research/slam-survey/build/main.pdf`.

## Task 8: Commit Coherent Units

**Files:**
- Stage: `research/slam-survey/main.tex`
- Stage: `docs/superpowers/specs/2026-05-19-slam-survey-notation-rewrite-design.md`
- Stage: `docs/superpowers/plans/2026-05-19-slam-survey-notation-rewrite.md`
- Stage if created: `outputs/slam-survey-notation-conventions.md`
- Stage: `.planning/quick/260519-nvm-rewrite-slam-survey-notation/PLAN.md`
- Stage: `.planning/quick/260519-nvm-rewrite-slam-survey-notation/SUMMARY.md`

- [ ] **Step 1: Inspect status and diff**

Run:

```bash
git status --short
git diff -- research/slam-survey/main.tex docs/superpowers/specs/2026-05-19-slam-survey-notation-rewrite-design.md docs/superpowers/plans/2026-05-19-slam-survey-notation-rewrite.md .planning/quick/260519-nvm-rewrite-slam-survey-notation/PLAN.md .planning/quick/260519-nvm-rewrite-slam-survey-notation/SUMMARY.md
```

- [ ] **Step 2: Commit**

Commit only the files changed for this quick task with a message such as:

```bash
git add research/slam-survey/main.tex docs/superpowers/specs/2026-05-19-slam-survey-notation-rewrite-design.md docs/superpowers/plans/2026-05-19-slam-survey-notation-rewrite.md .planning/quick/260519-nvm-rewrite-slam-survey-notation/PLAN.md .planning/quick/260519-nvm-rewrite-slam-survey-notation/SUMMARY.md
git commit -m "docs: rewrite SLAM survey notation and taxonomy"
```

Do not stage unrelated modified or untracked files.

## Self-Review

- Spec coverage: Section structure, formal setting, algorithm rewrite, taxonomy prose, removed sections, and final discussion synthesis are all covered by Tasks 2--7.
- Placeholder scan: No open placeholders are present; task steps name exact files and expected validation commands.
- Type consistency: Shared notation names are consistent with the design: $\mathcal{A}$, $\mathcal{Z}_i^{1:t}$, $\mathcal{M}_{i,t}$, $\mathcal{G}_t$, $\mathcal{C}_t$, $\mathcal{P}_t$, $\phi_i$, $\mu_i$, $\alpha$, and $\Psi_t$.
