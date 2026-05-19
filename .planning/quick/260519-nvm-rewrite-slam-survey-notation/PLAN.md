---
status: in_progress
quick_id: 260519-nvm
slug: rewrite-slam-survey-notation
created: 2026-05-19
---

Rewrite `research/slam-survey/main.tex` so the paper uses conventional survey-paper mathematical notation and readable algorithm blocks.

## Scope

- Keep the Introduction mostly intact.
- Replace `Problem Statement and Target Class` plus `Background and Related Work` with `Setting the Stage`.
- Make `Setting the Stage` mathematically formal: define agents, frames, trajectories, observations, local maps, Gaussian primitives, submaps, communication packets, alignment constraints, fusion operators, shared maps, metrics, and policy variables before they appear in algorithms.
- Rename candidate-system material to `Existing Works`.
- Keep per-system algorithm boxes, but rewrite them from `Trigger / Update / Emits` into conventional `Input`, `Output`, and sequential steps using the shared notation.
- Replace table-led `Architecture Taxonomy` with `Overall Architecture Taxonomy`, using prose subsections for each pattern and citing representative systems.
- Mention ablation studies inside the relevant taxonomy pattern subsections when available from the cited evidence; avoid inventing unsupported ablations.
- Remove `Survey Method and Evidence Criteria`, `Benchmark Synthesis`, and `Limitations`.
- Merge discussion and conclusion into `Discussion and Conclusion`, including forward-looking ideas from the architecture taxonomy.

## Research

- Do a focused literature check on how SLAM/vision survey and methods papers usually introduce notation and algorithms.
- Verify cited paper details enough to avoid unsupported method-specific claims.

## Validation

- Search the final TeX for removed section headings.
- Search the final TeX for old `Trigger`, `Update`, and `Emits` algorithm language.
- Compile the LaTeX paper if the local toolchain permits it.
- Review the final section order manually.
