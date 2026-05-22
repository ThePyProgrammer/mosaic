---
phase: 260522-myh-amend-research-slam-survey-paper-prose-r
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - research/slam-survey/main.tex
autonomous: true
requirements:
  - QUICK-260522-MYH
must_haves:
  truths:
    - "The surveyed system discussions read as neutral research-paper prose, not repeated labeled Mechanics/Evidence blocks."
    - "Opening system citations place repository footnotes immediately after the system name and before parenthetical citations where the opening sentence has both."
    - "Technical claims, numeric evidence, caveats, citations, footnotes, labels, and algorithm environments remain present."
  artifacts:
    - path: "research/slam-survey/main.tex"
      provides: "Revised LaTeX paper source with prose system discussions and normalized citation-footnote order"
      contains: "\\subsection{MAGiC-SLAM}"
  key_links:
    - from: "research/slam-survey/main.tex"
      to: "research/slam-survey/main.pdf"
      via: "Tectonic LaTeX build"
      pattern: "tectonic main.tex"
---

<objective>
Amend the SLAM survey paper prose so the candidate-system discussion reads like a research paper rather than repeated labeled blocks.

Purpose: The user wants the method descriptions to preserve claims and evidence while eliminating developer-brief labels such as `\\textbf{Mechanics.}` and `\\paragraph{Evidence and caveats.}`.
Output: A revised `research/slam-survey/main.tex` with prose method openings, evidence/caveat prose integrated into each subsection, and normalized citation-footnote ordering.
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/execute-plan.md
@$HOME/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/STATE.md
@CLAUDE.md
@research/slam-survey/main.tex

<source_audit>
- CONTEXT: Remove algorithm/system subsection labels titled `Mechanics` and `Evidence and caveats` from `research/slam-survey/main.tex` and convert them to research-paper prose. Covered by Task 1.
- CONTEXT: Reorder opening citation/repository-footnote patterns from `<algorithm> is ... (Citation).<repo footnote>` to `<algorithm><repo footnote> (Citation) is ...` universally where both citation and GitHub repository footnote occur in an opening sentence. Covered by Task 1 and Task 2 verification.
- CONTEXT: Preserve technical claims and citations while changing presentation. Covered by Task 1 and Task 2 verification.
- PROJECT: This is a LaTeX research survey paper; no implementation code, dependency, or architecture changes are in scope. Covered by file ownership and success criteria.
</source_audit>

<editing_targets>
The repeated labels currently appear in the candidate-system subsections for MAGiC-SLAM, MAC-Ego3D, CoKo-SLAM, CoMA-SLAM, HAMMER, GRAND-SLAM, and MAGS-SLAM.

Examples of citation-footnote order to normalize:
- `MAGiC-SLAM is ... \\citep{yugay2025magic_slam}.\\footnote{...}` should become `MAGiC-SLAM\\footnote{...} \\citep{yugay2025magic_slam} is ...` while preserving the sentence's technical content.
- For multi-citation openings, keep all citation keys unchanged and place the repository footnote after the system name when a repository footnote exists.
- HAMMER has no GitHub repository footnote in the current source; do not invent one.
</editing_targets>
</context>

<tasks>

<task type="auto">
  <name>Task 1: Convert labeled system blocks into paper prose</name>
  <files>research/slam-survey/main.tex</files>
  <action>Rewrite the candidate-system subsection prose in `research/slam-survey/main.tex` so no paragraph begins with `\\textbf{Mechanics.}` or `\\paragraph{Evidence and caveats.}`. Integrate each evidence/caveat paragraph into the surrounding system discussion as ordinary prose immediately before or after the algorithm environment, whichever reads more naturally for a research paper. Preserve all numeric claims, caveats, citations, repository footnotes, subsection labels, algorithm labels, and algorithm contents. Do not remove, weaken, or newly invent evidence. Avoid replacing the labels with other repeated labels such as `Method`, `Evidence`, `Limitations`, or `Caveats`; the output should read as continuous academic prose.</action>
  <verify>
    <automated>cd "/home/prannayag/pragnition/robotics/mosaic" && ! grep -nE '\\textbf\{Mechanics\.\}|\\paragraph\{Evidence and caveats\.\}' research/slam-survey/main.tex</automated>
  </verify>
  <done>`research/slam-survey/main.tex` contains no `Mechanics` or `Evidence and caveats` prose labels, and the seven system subsections still retain their technical descriptions, evidence claims, citations, repository footnotes where present, and algorithm blocks.</done>
</task>

<task type="auto">
  <name>Task 2: Normalize opening citation and repository-footnote order</name>
  <files>research/slam-survey/main.tex</files>
  <action>For every candidate-system opening sentence where the current prose has a system name, then explanatory text, then `\\citep{...}.\\footnote{\\url{...}}`, move the repository footnote to immediately follow the system name and keep the citation before `is`, yielding the pattern `System\\footnote{\\url{...}} \\citep{...} is ...`. Apply this to MAGiC-SLAM, MAC-Ego3D, CoKo-SLAM, CoMA-SLAM, GRAND-SLAM, and MAGS-SLAM where repository footnotes exist. Preserve all citation keys and URLs exactly. For HAMMER, preserve citations and prose but do not add a repository footnote because none exists in the source. After rewriting, review nearby punctuation so there is no stray period between citation and footnote and no duplicate footnote marker.</action>
  <verify>
    <automated>cd "/home/prannayag/pragnition/robotics/mosaic" && ! grep -nE '\\citep\{[^}]+\}\.\\footnote\{\\url\{' research/slam-survey/main.tex && grep -nE 'MAGiC-SLAM\\footnote|MAC-Ego3D\\footnote|CoKo-SLAM\\footnote|CoMA-SLAM\\footnote|GRAND-SLAM\\footnote|MAGS-SLAM\\footnote' research/slam-survey/main.tex</automated>
  </verify>
  <done>All system opening sentences with repository footnotes use system-name footnote placement before the parenthetical citation, no `\\citep{...}.\\footnote{...}` ordering remains, and HAMMER remains citation-only without an invented repository footnote.</done>
</task>

<task type="auto">
  <name>Task 3: Build and final consistency check</name>
  <files>research/slam-survey/main.tex, research/slam-survey/main.pdf</files>
  <action>Compile the survey with the repository's established LaTeX build path from `research/slam-survey`. Use Tectonic if available. If Tectonic is unavailable, record that as a blocked automated build in the summary and still run the grep checks from Tasks 1 and 2. Do not change bibliography entries, algorithm environments, diagrams, or package dependencies as part of this prose-only task.</action>
  <verify>
    <automated>cd "/home/prannayag/pragnition/robotics/mosaic/research/slam-survey" && tectonic main.tex</automated>
    <automated>cd "/home/prannayag/pragnition/robotics/mosaic" && ! grep -nE '\\textbf\{Mechanics\.\}|\\paragraph\{Evidence and caveats\.\}|\\citep\{[^}]+\}\.\\footnote\{\\url\{' research/slam-survey/main.tex</automated>
  </verify>
  <done>`research/slam-survey/main.pdf` builds from the revised source when Tectonic is available, and the source passes the label-removal and citation-footnote order grep gates.</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| LaTeX source to PDF build | Local TeX compilation processes repository-controlled paper source. |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-260522-myh-01 | Tampering | `research/slam-survey/main.tex` scholarly claims | mitigate | Preserve citations, numeric claims, URLs, labels, and algorithms; restrict edits to prose presentation and citation-footnote order. |
| T-260522-myh-02 | Repudiation | Verification of prose cleanup | mitigate | Use grep gates for removed labels and forbidden citation-footnote order, plus a Tectonic build when available. |
| T-260522-myh-SC | Tampering | package installs | accept | No package-manager installs are planned or needed. |
</threat_model>

<verification>
Run the automated checks embedded in each task. The required final checks are: no `\\textbf{Mechanics.}` labels, no `\\paragraph{Evidence and caveats.}` labels, no `\\citep{...}.\\footnote{\\url{...}}` ordering, expected repository-footnote openings for the six systems with repositories, and a successful Tectonic build where available.
</verification>

<success_criteria>
- `research/slam-survey/main.tex` reads as research-paper prose in the seven candidate-system subsections.
- All requested label removals and citation-footnote reorderings are applied universally within the candidate-system openings.
- No technical evidence, caveat, citation key, URL, algorithm, or subsection label is lost.
- `research/slam-survey/main.pdf` is regenerated successfully if Tectonic is available.
</success_criteria>

<output>
Create `.planning/quick/260522-myh-amend-research-slam-survey-paper-prose-r/260522-myh-SUMMARY.md` when done.
</output>
