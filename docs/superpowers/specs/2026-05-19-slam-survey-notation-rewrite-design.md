# SLAM Survey Notation Rewrite Design

## Goal

Rewrite `research/slam-survey/main.tex` so the survey reads like a conventional academic SLAM/vision paper: shared notation is defined before use, method algorithms are readable procedures, and the architecture taxonomy is expressed as interpretive prose rather than table-first synthesis.

## Section Structure

The rewritten paper should contain these main sections:

1. `Introduction` — keep mostly unchanged, preserving the existing scope and motivation.
2. `Setting the Stage` — replace the current problem/background split with a formal setup.
3. `Existing Works` — retain the candidate systems as method subsections.
4. `Overall Architecture Taxonomy` — replace the current table-led taxonomy with pattern subsections.
5. `Discussion and Conclusion` — merge discussion and conclusion and include forward-looking directions from the taxonomy.

Remove `Survey Method and Evidence Criteria`, `Benchmark Synthesis`, and `Limitations` as standalone sections.

## Mathematical Setting

`Setting the Stage` should introduce the common formal objects used throughout the paper:

- agent set, time index, local frames, global frame, and frame transforms;
- observation streams and modality-specific observations;
- local trajectories and local tracking estimates;
- Gaussian primitives, local maps, submaps, and shared maps;
- communication packets, budgets, and keyframe/submap selection policies;
- cross-agent constraints, loop closures, consensus factors, and alignment transforms;
- fusion operators and optimization objectives;
- benchmark quantities such as trajectory error, rendering metrics, latency, memory, and communication load.

Notation should be stable across all methods unless a system genuinely needs method-specific symbols. Method-specific notation should be introduced locally and tied back to the shared notation.

## Algorithm Style

Keep per-system algorithm boxes. Rewrite each from compact `Trigger / Update / Emits` bullets into conventional pseudocode with:

- `Input:` one line listing observations, prior map state, poses, packets, or constraints;
- `Output:` one line listing the map, poses, shared model, or updated consensus state;
- ordered procedural steps using verbs such as estimate, select, transmit, detect, optimize, align, prune, fuse, and publish;
- equations only where they clarify a key optimization or transformation;
- no `Trigger`, `Update`, or `Emits` labels.

The algorithms are survey summaries, not executable source code. They should stay concise and evidence-bounded.

## Existing Works

The existing system set remains:

- MAGiC-SLAM;
- MAC-Ego3D;
- CoKo-SLAM;
- CoMA-SLAM;
- HAMMER;
- GRAND-SLAM;
- MAGS-SLAM.

Each subsection should include a short mechanics paragraph, the rewritten algorithm, and a compact evidence/caveat paragraph. Avoid turning the paper into a developer brief.

## Architecture Taxonomy

`Overall Architecture Taxonomy` should use prose subsections for the recurring patterns rather than a table as the main structure:

- central-server submap and Gaussian fusion;
- distributed Gaussian consensus;
- submap-plus-pose-graph consistency;
- compact communication and monocular submap fusion;
- heterogeneous semantic shared Gaussian mapping.

Each subsection should identify representative systems, explain the pattern using the shared formalism, discuss known tradeoffs, and mention ablation evidence only when available in the cited papers or existing extracted evidence. Unsupported ablation claims should be omitted or explicitly described as missing.

## Discussion and Conclusion

The final section should synthesize how the taxonomy suggests future work:

- standardize reporting for communication, memory, latency, merge cost, and scaling;
- separate local tracking quality from update selection, alignment, and fusion quality;
- evaluate robustness to delayed, dropped, or stale inter-agent updates;
- connect semantic and uncertainty-aware Gaussian maps to provenance-aware shared representations;
- treat architecture patterns as modular components rather than ranking systems by one score.

## Validation

After editing:

- search for the removed section headings;
- search for old `Trigger`, `Update`, and `Emits` algorithm labels;
- verify section order manually;
- compile the LaTeX paper if the local toolchain supports it;
- review for unsupported claims introduced during the rewrite.
