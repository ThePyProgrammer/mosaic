---
phase: 260522-nfz-evaluate-algorithm-flow-ordering-in-the-
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - slam-algorithm-flow-research.md
  - outputs/slam-algorithm-flow-review.md
autonomous: true
requirements:
  - QUICK-260522-NFZ
must_haves:
  truths:
    - "The current SLAM survey draft has been checked for whether method algorithm blocks are ordered coherently for reader comprehension."
    - "The review explicitly identifies lineage and dependency relationships among surveyed methods, including whether any methods build on others beyond CoKo-SLAM building on MAGiC-SLAM."
    - "Claims about method dependencies are backed by direct URL sources from papers, project pages, repositories, or existing project output notes."
  artifacts:
    - path: "slam-algorithm-flow-research.md"
      provides: "Evidence notes and source-backed lineage analysis for the algorithm-flow ordering review"
    - path: "outputs/slam-algorithm-flow-review.md"
      provides: "Final review focused on algorithm-flow ordering and explicit method lineage/dependency relationships"
  key_links:
    - from: "research/slam-survey/main.tex"
      to: "slam-algorithm-flow-research.md"
      via: "researcher subagent evidence extraction from the current survey draft"
      pattern: "algorithm-flow|lineage|dependency|CoKo-SLAM|MAGiC-SLAM"
    - from: "slam-algorithm-flow-research.md"
      to: "outputs/slam-algorithm-flow-review.md"
      via: "review synthesis grounded in direct URL sources"
      pattern: "Source|URL|dependency|ordering"
---

<objective>
Evaluate the algorithm-flow ordering in the current SLAM survey draft and produce source-backed review artifacts.

Purpose: The survey should present method algorithms in an order that makes dependencies and lineage legible to an academic reader, without inventing lineage that the papers do not support.
Output: `slam-algorithm-flow-research.md` and `outputs/slam-algorithm-flow-review.md` only.
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/execute-plan.md
@$HOME/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/STATE.md
@CLAUDE.md
@research/slam-survey/main.tex
@outputs/multiview-3dgs-slam.md
@outputs/multiview-3dgs-slam.provenance.md
@outputs/multiview-3dgs-slam-research-papers.md
@outputs/multiview-3dgs-slam-research-code.md
@outputs/multiview-3dgs-slam-research-multicamera.md
@outputs/multi-robot-gaussian-slam.md
@outputs/multi-robot-gaussian-slam.provenance.md
@outputs/multi-robot-gaussian-slam-research-papers.md
@outputs/multi-robot-gaussian-slam-research-code.md
@outputs/magic-local-tracking.md
@outputs/magic-local-tracking.provenance.md
@outputs/coko-slam-magic-slam.md
@outputs/coko-slam-magic-slam.provenance.md

<constraints>
- Documentation/research only. Do not modify source code, LaTeX source, bibliography, project config, tests, or generated PDF artifacts.
- Final artifacts must be exactly `slam-algorithm-flow-research.md` and `outputs/slam-algorithm-flow-review.md`.
- Use neutral academic framing, not a Mosaic developer brief.
- Use concise ordered process descriptions where discussing algorithms; avoid state-tracker preambles.
- Focus the final review on algorithm-flow ordering and explicit lineage/dependency relationships.
</constraints>
</context>

<tasks>

<task type="auto">
  <name>Task 1: Research survey algorithm order and method lineage</name>
  <files>slam-algorithm-flow-research.md</files>
  <action>Use a researcher subagent to inspect `research/slam-survey/main.tex`, the relevant existing `outputs/*slam*` notes/provenance files, and direct external sources where necessary. The researcher must gather direct URL evidence from cited papers, project pages, and repositories for each surveyed method whose algorithm block appears in the survey. Extract the current algorithm-block order, infer the conceptual flow expected by the draft, and identify explicit method lineage/dependency claims. Pay special attention to whether any method builds on another surveyed method beyond CoKo-SLAM building on MAGiC-SLAM. Write `slam-algorithm-flow-research.md` with: current order, method-by-method evidence table, direct URLs, explicit lineage/dependency matrix, uncertain/non-lineage relationships, and ordering implications. Do not edit the survey draft or any code.</action>
  <verify>
    <automated>test -f slam-algorithm-flow-research.md && grep -E "CoKo-SLAM|MAGiC-SLAM|dependency|lineage|https?://" slam-algorithm-flow-research.md >/dev/null && git diff --name-only | grep -v '^#' | grep -E '^(slam-algorithm-flow-research\.md)$' >/dev/null</automated>
  </verify>
  <done>`slam-algorithm-flow-research.md` exists, cites direct URL sources, records the current survey algorithm ordering, and explicitly distinguishes supported lineage from merely similar mechanisms.</done>
</task>

<task type="auto">
  <name>Task 2: Write final algorithm-flow ordering review</name>
  <files>outputs/slam-algorithm-flow-review.md</files>
  <action>Using `slam-algorithm-flow-research.md` as evidence, write `outputs/slam-algorithm-flow-review.md` as the final review. Structure it around: verdict on whether the current algorithm-flow ordering is defensible; any recommended reordering; explicit method lineage/dependency relationships; a clear answer to whether any methods build on others beyond CoKo-SLAM building on MAGiC-SLAM; and source-backed caveats. Keep the review neutral and paper-facing. Do not propose implementation tasks, do not modify `research/slam-survey/main.tex`, and do not create any additional artifacts.</action>
  <verify>
    <automated>test -f outputs/slam-algorithm-flow-review.md && grep -E "ordering|lineage|dependency|CoKo-SLAM|MAGiC-SLAM" outputs/slam-algorithm-flow-review.md >/dev/null && git diff --name-only | grep -v '^#' | grep -E '^(slam-algorithm-flow-research\.md|outputs/slam-algorithm-flow-review\.md)$' >/dev/null</automated>
  </verify>
  <done>`outputs/slam-algorithm-flow-review.md` gives an evidence-backed ordering verdict and directly answers the lineage/dependency question without changing the draft itself.</done>
</task>

<task type="auto">
  <name>Task 3: Confirm artifact-only scope</name>
  <files>slam-algorithm-flow-research.md, outputs/slam-algorithm-flow-review.md</files>
  <action>Run a final scope check that only the two requested artifacts are newly created or modified by this quick task. If any source code, LaTeX, bibliography, PDF, config, or unrelated output file changed, revert those unrelated changes before completing the plan. Do not commit unless the caller explicitly asks for a commit.</action>
  <verify>
    <automated>git diff --name-only | grep -v '^#' | grep -Ev '^(slam-algorithm-flow-research\.md|outputs/slam-algorithm-flow-review\.md)$' | test $(wc -l) -eq 0</automated>
  </verify>
  <done>Working-tree changes from this plan are limited to `slam-algorithm-flow-research.md` and `outputs/slam-algorithm-flow-review.md`.</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| External papers/repos/project pages -> review artifacts | External claims may be stale, ambiguous, or marketing-framed. |
| Existing output notes -> final review | Prior notes may contain interpretation errors and must not override primary sources. |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-260522-NFZ-01 | Tampering | Source-backed lineage claims | mitigate | Record direct URLs in `slam-algorithm-flow-research.md` and separate explicit lineage from inferred similarity. |
| T-260522-NFZ-02 | Repudiation | Review conclusions | mitigate | Tie final verdicts in `outputs/slam-algorithm-flow-review.md` back to source rows in the research artifact. |
| T-260522-NFZ-03 | Information Disclosure | Local repo contents | accept | Task only reads project research/draft files and writes public-facing review notes; no secrets or private credentials are needed. |
| T-260522-NFZ-SC | Tampering | Package installs | accept | No package-manager install tasks are planned. |
</threat_model>

<verification>
- `test -f slam-algorithm-flow-research.md`
- `test -f outputs/slam-algorithm-flow-review.md`
- `git diff --name-only` shows only `slam-algorithm-flow-research.md` and `outputs/slam-algorithm-flow-review.md` for this quick task.
</verification>

<success_criteria>
- Research artifact exists at `slam-algorithm-flow-research.md` with direct URL evidence and a lineage/dependency matrix.
- Review artifact exists at `outputs/slam-algorithm-flow-review.md` with a clear ordering verdict and explicit answer about method dependencies beyond CoKo-SLAM building on MAGiC-SLAM.
- No source code, LaTeX draft, bibliography, PDF, config, or unrelated output files are changed.
</success_criteria>

<output>
Create `.planning/quick/260522-nfz-evaluate-algorithm-flow-ordering-in-the-/260522-nfz-SUMMARY.md` when done.
</output>
