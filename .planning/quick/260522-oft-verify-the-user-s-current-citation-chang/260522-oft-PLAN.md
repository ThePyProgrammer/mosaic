---
phase: 260522-oft-verify-the-user-s-current-citation-chang
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - research/slam-survey/main.tex
  - research/slam-survey/references.bib
  - research/slam-survey/main.pdf
autonomous: true
requirements:
  - QUICK-260522-OFT
---

<objective>
Verify the user's current SLAM survey citation/bibliography edits, rebuild the PDF, and commit the verified paper files if the LaTeX build succeeds.
</objective>

<context>
The user has intentionally edited `research/slam-survey/main.tex` and `research/slam-survey/references.bib`. Do not revert those citation edits. Only make changes if required for build correctness.
</context>

<tasks>

<task type="auto">
  <name>Inspect current citation diffs</name>
  <files>research/slam-survey/main.tex, research/slam-survey/references.bib</files>
  <action>Review the current git diff to confirm the edits are citation/bibliography cleanup and no unrelated source files need staging.</action>
  <verify>git diff -- research/slam-survey/main.tex research/slam-survey/references.bib</verify>
  <done>Diff reviewed and no revert is needed.</done>
</task>

<task type="auto">
  <name>Compile survey PDF</name>
  <files>research/slam-survey/main.tex, research/slam-survey/references.bib, research/slam-survey/main.pdf</files>
  <action>Run the established Tectonic build for `research/slam-survey/main.tex` and allow it to regenerate `main.pdf`.</action>
  <verify>tectonic research/slam-survey/main.tex</verify>
  <done>Build exits successfully, with warnings recorded if present.</done>
</task>

<task type="auto">
  <name>Commit verified paper changes</name>
  <files>research/slam-survey/main.tex, research/slam-survey/references.bib, research/slam-survey/main.pdf</files>
  <action>Create a local git commit containing the verified paper citation changes and regenerated PDF, plus GSD quick summary/state artifacts if updated.</action>
  <verify>git status --short</verify>
  <done>Commit created and unrelated untracked files left unstaged.</done>
</task>

</tasks>

<success_criteria>
- Current user citation edits are preserved.
- `tectonic research/slam-survey/main.tex` exits successfully.
- Verified changed paper files are committed locally.
</success_criteria>
