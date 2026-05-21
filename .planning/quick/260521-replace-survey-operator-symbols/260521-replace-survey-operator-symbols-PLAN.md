---
phase: quick-replace-survey-operator-symbols
plan: 01
type: execute
files_modified:
  - research/slam-survey/main.tex
  - research/slam-survey/main.pdf
  - .planning/STATE.md
  - .planning/quick/260521-replace-survey-operator-symbols/260521-replace-survey-operator-symbols-SUMMARY.md
autonomous: true
requirements:
  - QUICK-260521-REPLACE-SURVEY-OPERATOR-SYMBOLS
---

<objective>
Replace the five recurring SLAM survey responsibility operator symbols with snake_case text function names in `research/slam-survey/main.tex`, preserve LaTeX compileability, and rebuild `research/slam-survey/main.pdf`.
</objective>

<tasks>

<task type="auto">
  <name>Replace five operator symbols</name>
  <files>research/slam-survey/main.tex</files>
  <action>Replace `\tau_i`, `\phi_i`, `\mu_i`, `\alpha_t`, and `\Psi_t` with `\operatorname{local\_tracking}_i`, `\operatorname{local\_mapping}_i`, `\operatorname{update\_selection}_i`, `\operatorname{cross\_agent\_alignment}_t`, and `\operatorname{global\_fusion}_t` respectively.</action>
</task>

<task type="auto">
  <name>Verify and rebuild PDF</name>
  <files>research/slam-survey/main.tex, research/slam-survey/main.pdf</files>
  <action>Check that the old symbols have zero remaining occurrences, confirm the 12 algorithm floats and 12 algorithmic blocks remain, and run `cd research/slam-survey && tectonic main.tex && test -s main.pdf`.</action>
</task>

<task type="auto">
  <name>Record GSD summary</name>
  <files>.planning/quick/260521-replace-survey-operator-symbols/260521-replace-survey-operator-symbols-SUMMARY.md, .planning/STATE.md</files>
  <action>Record the quick-task summary and add the completed quick task to `.planning/STATE.md`.</action>
</task>

</tasks>
