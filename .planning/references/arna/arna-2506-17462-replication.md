# Replication Plan: General-Purpose Robotic Navigation via LVLM-Orchestrated Perception, Reasoning, and Acting

Target paper: arXiv:2506.17462, "General-Purpose Robotic Navigation via LVLM-Orchestrated Perception, Reasoning, and Acting".

Execution mode selected: **Plan only**. No packages were installed, no code was cloned, and no experiments were run.

## 1. Paper and artifact status

### Verified from paper/arXiv

- Paper: "General-Purpose Robotic Navigation via LVLM-Orchestrated Perception, Reasoning, and Acting".
- Authors: Bernard Lange, Anil Yildiz, Mansur Arief, Shehryar Khattak, Mykel Kochenderfer, Georgios Georgakis.
- Method: **ARNA**, Agentic Robotic Navigation Architecture.
- Main idea: use a large vision-language model to orchestrate perception, reasoning, memory, and robot navigation tools rather than directly mapping observations to low-level actions.
- Main simulator: Habitat Lab.
- Main environments/datasets: HM3D, MP3D/Matterport3D, HM-EQA, and RxR-CE.
- Main LVLM for quantitative evaluation: GPT-4o.
- Auxiliary model: GPT-4o-mini for room segmentation.
- Perception component: Grounding DINO for scene-graph updates.
- Evaluation constraints: 500 reasoning steps and $5 cost cap.
- Reported runtime/cost: roughly 30-60 minutes and $1-3 per task.
- Hardware reported: NVIDIA H100 GPU and 64-core CPU.

### Verified artifact search result

No public implementation repository, README, Dockerfile, requirements file, evaluation script, config bundle, prompt files, checkpoints, or project page was found from arXiv, arXiv HTML/PDF/source, GitHub search, Hugging Face search, Papers With Code search, Semantic Scholar, DBLP, OpenAlex, alphaXiv, or author-linked metadata.

### Missing replication-critical details

- Exact source code and tool implementations.
- Exact prompt templates and workflow-generation prompts.
- Exact HM-EQA evaluation split, episode IDs, and random seeds.
- Exact Habitat Lab, CUDA, Python, and dependency versions.
- Exact answer-normalization or grading rules.
- Exact GPT-4o and GPT-4o-mini dated model snapshots.
- Exact RxR-CE episode selection and success numerator.
- Exact statistical methodology behind the paper's reported uncertainty values.

## 2. Method to replicate

ARNA is described as an LVLM-orchestrated robot-navigation loop with perception, reasoning, acting, and memory tools.

### Verified components

- Robot/simulator stack: Habitat Lab operating over HM3D and MP3D/Matterport3D scenes.
- LVLM agent: GPT-4o for numerical ARNA experiments.
- Room segmentation: GPT-4o-mini.
- Scene graph: updated using Grounding DINO.
- Memory: textual memory plus raster/top-down spatial memory and scene graph landmarks.
- Tool categories:
  - Perception: image retrieval and scene-graph queries.
  - Reasoning: shortest path, visibility, reachability, proximity, semantic queries, object-relation predicates.
  - Navigation/control: `goto(x,y,z)`, `rotate(theta)`, `follow_path(node)`, `explore_frontiers()`.
- Workflow generation: modified self-discover-style process where the LVLM selects/adapts heuristics, writes pseudocode, and implements task-specific workflows with tools and control flow.

### Inferred implementation design

Because no code was found, the replication must reconstruct ARNA as follows:

1. Build a Habitat Lab runner for HM-EQA episodes.
2. Implement a tool-calling loop around GPT-4o.
3. Implement tool schemas matching the paper's functional descriptions.
4. Maintain synchronized text memory, occupancy/raster memory, and scene-graph memory.
5. Use Grounding DINO detections to populate/update scene graph nodes.
6. Use GPT-4o-mini to label/segment rooms when required by the workflow.
7. Use Habitat navigation primitives and A* over the navmesh for `goto`/path-following.
8. Log every prompt, model response, tool call, observation, path trace, token count, cost estimate, final answer, and inconclusive reason.

## 3. Environment requirements

This section is a plan only; do not execute until an environment is explicitly chosen.

### Required assets

- Habitat Lab installation.
- HM3D scene assets.
- MP3D/Matterport3D scene assets.
- HM-EQA benchmark data.
- RxR-CE data for secondary evaluation.
- Grounding DINO model/checkpoint.
- Access to GPT-4o and GPT-4o-mini APIs.

### Recommended software pinning

- Python version pinned in an environment file.
- Habitat Lab version pinned by commit or release.
- CUDA/PyTorch versions pinned to match available GPU.
- Grounding DINO version and checkpoint checksum recorded.
- OpenAI/LLM SDK version pinned.
- All dataset JSON/config files hashed.
- All generated prompts/configs saved under version control.

### Recommended hardware

- GPU comparable to paper's H100 for perception/simulation throughput, or note degradation.
- CPU capacity sufficient for Habitat simulation and navigation planning; paper reports 64-core CPU.
- Sufficient local storage for HM3D/MP3D assets.

## 4. Datasets and splits

### Primary evaluation: HM-EQA

Verified claim: ARNA is evaluated on HM-EQA in Habitat Lab using HM3D/MP3D scenes.

Replication steps:

1. Acquire HM-EQA data and underlying HM3D/MP3D assets from official sources.
2. Identify the paper's evaluation split. If exact split is unavailable, use the official HM-EQA evaluation split and mark results as approximate reproduction.
3. Record episode IDs, scene IDs, start poses, questions, ground-truth answers, and navmesh/config hashes.
4. Preserve an immutable manifest of evaluated episodes.

### Secondary evaluation: RxR-CE

Verified claim: ARNA achieved 12% success over 30 RxR-CE episodes.

Replication steps:

1. Locate the RxR-CE task subset if specified elsewhere by the authors.
2. If exact subset is unavailable, sample 30 official RxR-CE episodes with a fixed seed and clearly label the result as non-identical.
3. Report raw success count, not just percentage.

## 5. Metrics to report

### Verified paper metrics

- Correct answer percentage.
- Incorrect answer percentage.
- Inconclusive percentage.
- Mean path length in meters.
- Mean token usage in thousands of tokens.
- Inconclusive breakdown by time limit, cost limit, and function-call error.

### Required replication metrics

For every run, report:

- Episode ID and scene ID.
- Final answer.
- Correct/incorrect/inconclusive label.
- Inconclusive reason if applicable.
- Path length in meters.
- Reasoning step count.
- Environment step count if separate.
- Prompt tokens, completion tokens, total tokens.
- Estimated API cost.
- Wall-clock runtime.
- Function-call error count.
- Collision count.
- Number of frontier explorations.
- Number of perception calls.

## 6. Paper results to reproduce

### HM-EQA main result

Verified Table I target:

| Method | Correct / Incorrect | Mean path length | Mean token usage |
|---|---:|---:|---:|
| ARNA, GPT-4o | 77% / 14% | 16.55 ± 1.75 m | 673.11 ± 85.89k |

The remaining 9% are inconclusive, consistent with the reported inconclusive breakdown.

Recommended primary pass condition:

- Correct rate at least 72% on the same HM-EQA setup, or bootstrap 95% confidence interval overlaps 77%.
- Incorrect and inconclusive rates close to paper values; inconclusive no more than 15%.
- Mean path length no more than 20 m, or confidence interval overlaps paper value.
- Token usage within ±25%, acknowledging API/model/prompt drift.

### Baseline separation

Verified strongest interactive baseline in the paper:

| Method | Correct / Incorrect | Mean path length | Mean token usage |
|---|---:|---:|---:|
| EuC-GPT-4o | 61% / 39% | 175.91 ± 44.09 m | 42.72 ± 9.13k |

Required qualitative replication:

- ARNA should beat EuC-GPT-4o by at least 10 percentage points or by a statistically significant paired/binomial test.
- ARNA should have much shorter path length than EuC-GPT-4o.
- ARNA should use substantially more tokens than EuC baselines.

### Representation ablations

Verified Table II targets:

| Variant | Correct / Incorrect | Path length | Token usage |
|---|---:|---:|---:|
| NoSG | 41% / 27% | 21.68 ± 2.55 m | 687.66 ± 60.70k |
| NoOGM | 33% / 15% | 24.30 ± 1.78 m | 612.86 ± 29.87k |
| NoRP | 10% / 49% | 20.46 ± 2.91 m | 523.57 ± 90.80k |
| CoT | 7% / 2% | 32.91 ± 2.86 m | 938.50 ± 87.37k |

Verified Table III inconclusive breakdown:

| Variant | Time limit | Cost limit | Function-call error |
|---|---:|---:|---:|
| ARNA | 0% | 3% | 6% |
| NoSG | 27% | 5% | 0% |
| NoOGM | 44% | 2% | 6% |
| NoRP | 27% | 6% | 8% |
| CoT | 69% | 0% | 21% |

Ablation replication passes if:

- Full ARNA clearly outperforms all ablations in correct rate.
- Removing rasterized representations causes a large degradation.
- CoT-only is clearly poor and has a high inconclusive/function-call failure rate.
- Exact ablation percentages may differ, but the qualitative ordering and failure modes should hold.

## 7. Test oracles

### Answer correctness oracle

Use the official HM-EQA answer labels whenever possible.

For categorical answers:

- Normalize case, whitespace, articles, and punctuation.
- Apply a fixed synonym map before evaluation.
- Do not use the evaluated LVLM as the sole judge.

For ambiguous/free-form answers:

- First use deterministic normalization.
- Then use blinded human adjudication or an independent fixed evaluator.
- Save every adjudication decision and rationale.

### Inconclusive oracle

Mark a run as inconclusive if any of the following occur:

- 500 reasoning steps reached.
- Estimated cost reaches or exceeds $5.
- Unrecoverable function-call/tool-schema error.
- Simulator/runtime failure not attributable to a wrong answer.

Keep inconclusive separate from incorrect answers.

### Navigation oracle

- Path length must equal physical agent movement in Habitat, not planned path alone.
- `goto` should be checked against Habitat geodesic distance on known navigable targets.
- Reaching a target should have a fixed distance threshold.
- Rotation-only actions should not inflate path length.

### Tool-call oracle

- Tool arguments must validate against schemas.
- Tool outputs must be deterministic for a fixed simulator state.
- Failed tool calls must be counted and classified.

## 8. Statistical analysis plan

1. Report Wilson or exact binomial confidence intervals for correct, incorrect, and inconclusive rates.
2. Bootstrap over episodes for path length, token usage, cost, and runtime.
3. If baselines are run on the same episodes, use paired bootstrap or McNemar-style tests for correctness.
4. Run at least three independent repeats if budget permits. If not, run a smaller repeated subset and mark uncertainty as under-estimated.
5. Pre-register non-inferiority thresholds:
   - Same setup: pass if ARNA is no more than 5 percentage points below 77% correct.
   - Different model/API snapshot or split: pass if no more than 8 percentage points below 77% correct and qualitative ablation/baseline relationships hold.

## 9. Sanity checks and negative controls

### Dataset integrity

- Hash all episode/config files.
- Verify scene IDs, start poses, questions, and answers.
- Verify scene asset checksums.
- Confirm camera intrinsics, action settings, coordinate frames, and navmesh generation settings.
- Ensure no ground-truth answers leak into prompts, scene graphs, captions, or tool outputs.

### Navigation sanity checks

- Run `goto` on fixed navigable points and compare physical path length to Habitat geodesic distance.
- Confirm frontier exploration increases explored area.
- Confirm occupancy map aligns with pose over long trajectories.
- Log and inspect collision rate.

### Perception sanity checks

- Run Grounding DINO on fixed frames with known visible objects.
- Verify scene-graph queries return plausible object locations.
- Check common false positives for chair, sofa, bed, table, door, and room labels.
- Re-run room segmentation on fixed observations to estimate label stability.

### Memory sanity checks

- Landmarks should not teleport between timesteps.
- Text memory should distinguish "not found yet" from "absent".
- Occupancy/raster memory should remain pose-aligned.
- Stale object observations should be timestamped or confidence-weighted.

### Negative controls

- Blind/no-navigation control should remain near the paper's blind baseline of 40% correct.
- Shuffled question-scene pairs should collapse toward chance or majority baseline.
- Disabled perception should not approach ARNA's 77%.
- Randomized scene-graph labels should materially reduce accuracy.
- Scrambled occupancy map should degrade path efficiency.
- Lowering the step/cost cap should increase inconclusive rate.

## 10. Execution layout for future runs

If execution is later requested, use a reproducible layout like:

```text
outputs/arna-2506-17462/
  configs/
    habitat.yaml
    arna.yaml
    model_versions.json
    dataset_manifest.json
  prompts/
    system_prompt.txt
    workflow_generation_prompt.txt
    tool_schemas.json
  logs/
    <run_id>/
      episode_manifest.json
      prompts.jsonl
      tool_calls.jsonl
      observations.jsonl
      paths.jsonl
      answers.jsonl
      costs.jsonl
      failures.jsonl
  results/
    per_episode.csv
    aggregate_metrics.json
    bootstrap_intervals.json
    ablations.csv
    baselines.csv
  reports/
    replication_report.md
```

## 11. Methodology for future execution

1. Reconstruct ARNA's tools and memory modules from the paper.
2. Validate tools independently before full episodes.
3. Run a smoke test on 3-5 HM-EQA episodes.
4. Inspect full prompt/tool/action traces manually.
5. Run primary HM-EQA split.
6. Run EuC-GPT-4o or the closest available interactive baseline on identical episodes.
7. Run representation ablations: NoSG, NoOGM, NoRP, CoT.
8. Run negative controls.
9. Compute metrics and statistical intervals.
10. Write final report comparing results to paper claims.

## 12. Expected risks

High replication risk because no public implementation artifacts were found.

Primary risks:

- Prompt templates are missing and may dominate performance.
- Tool schemas and memory serialization are missing.
- Exact evaluation split is missing.
- GPT-4o API behavior may have drifted from the paper's experiments.
- Grounding DINO and room segmentation errors may compound over long episodes.
- Inconclusive/error classification may differ from the authors' implementation.
- Reconstructing baselines may require separate codebases with their own assumptions.

## 13. Confidence assessment

- Confidence in paper result extraction: **High** for headline results, ablations, models, datasets, and limits.
- Confidence in artifact availability: **High** that no public code was discoverable during this search.
- Confidence in exact reproducibility: **Low** without author code, prompts, splits, and model snapshots.
- Confidence in approximate reproduction: **Medium** if the official datasets are available, ARNA is carefully reconstructed, and evaluation uses the same benchmark protocol.
- Recommended claim wording after future execution: use "approximate independent reproduction" unless exact code, prompts, and episode split are obtained.

## Sources

- Paper abstract: https://arxiv.org/abs/2506.17462
- Paper HTML: https://arxiv.org/html/2506.17462v2
- Paper PDF: https://arxiv.org/pdf/2506.17462
- DOI: https://doi.org/10.48550/arXiv.2506.17462
- Semantic Scholar record: https://www.semanticscholar.org/paper/General-Purpose-Robotic-Navigation-via-Perception%2C-Lange-Yildiz/1a28214089b1d48416292dc07043f16634694b2a
- DBLP record: https://dblp.org/rec/journals/corr/abs-2506-17462
- OpenAlex record: https://openalex.org/W4415901659
- alphaXiv record: https://www.alphaxiv.org/abs/2506.17462v1
