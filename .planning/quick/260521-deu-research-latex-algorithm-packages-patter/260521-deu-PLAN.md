---
phase: quick-research-latex-algorithm-packages-patterns
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - research/slam-survey/main.tex
  - research/slam-survey/main.pdf
autonomous: true
requirements:
  - QUICK-260521-DEU
must_haves:
  truths:
    - "All 12 survey algorithm blocks render as pseudocode-first algorithmicx bodies, not prose enumerate lists."
    - "Each algorithm body uses algorithmic statements with short trailing explanatory comments where useful."
    - "The LaTeX source compiles with Tectonic and leaves main.pdf updated in place."
  artifacts:
    - path: "research/slam-survey/main.tex"
      provides: "algpseudocode package import and 12 converted algorithm bodies"
      contains: "\\usepackage{algpseudocode}"
    - path: "research/slam-survey/main.pdf"
      provides: "compiled survey PDF after algorithm conversion"
  key_links:
    - from: "research/slam-survey/main.tex"
      to: "algorithmicx algpseudocode"
      via: "\\begin{algorithmic}[1] with \\Require, \\Ensure, \\State, and \\Comment"
      pattern: "\\\\begin\{algorithmic\}\[1\]"
---

<objective>
Update `research/slam-survey/main.tex` so the 12 custom-float algorithm blocks use `algpseudocode` from `algorithmicx` inside the existing `algorithm` float, with pseudocode/math-first statements and short trailing explanatory comments.

Purpose: The survey algorithms should read like formal procedures rather than prose ordered lists while preserving the paper's existing float styling and compile path.
Output: Updated `main.tex`, updated compiled `main.pdf`, and `.planning/quick/260521-deu-research-latex-algorithm-packages-patter/260521-deu-SUMMARY.md`.
</objective>

<execution_context>
@$HOME/.claude/get-shit-done/workflows/execute-plan.md
@$HOME/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/STATE.md
@CLAUDE.md
@.planning/quick/260521-deu-research-latex-algorithm-packages-patter/260521-deu-RESEARCH.md
@research/slam-survey/main.tex

Locked direction: Use `algpseudocode` from `algorithmicx` inside the existing custom `algorithm` float. Convert algorithm bodies from `enumerate` prose items to `algorithmic` with `\Require`, `\Ensure`, `\State`, and trailing `\Comment{...}`. Keep statements pseudocode/math-first; comments short and explanatory. Do not load the `algorithm` or `algorithmic` packages from the older `algorithms` bundle.
</context>

<tasks>

<task type="auto">
  <name>Task 1: Add algpseudocode without changing the custom algorithm float</name>
  <files>research/slam-survey/main.tex</files>
  <action>Add `\usepackage{algpseudocode}` near the existing math/list package imports. Keep the existing `float` package, `\floatstyle{ruled}`, `\newfloat{algorithm}{tbp}{loa}`, and `\floatname{algorithm}{Algorithm}` unchanged. Do not add `\usepackage{algorithm}` or `\usepackage{algorithmic}` because the document already owns the `algorithm` float and the research recommendation selected `algorithmicx` for compatibility.</action>
  <verify>
    <automated>grep -q '\\usepackage{algpseudocode}' research/slam-survey/main.tex && ! grep -q '\\usepackage{algorithm}' research/slam-survey/main.tex && ! grep -q '\\usepackage{algorithmic}' research/slam-survey/main.tex</automated>
  </verify>
  <done>`main.tex` imports `algpseudocode` exactly through `\usepackage{algpseudocode}` and does not import the older algorithm float or algorithmic package.</done>
</task>

<task type="auto">
  <name>Task 2: Convert all 12 algorithm bodies to pseudocode-first algorithmicx blocks</name>
  <files>research/slam-survey/main.tex</files>
  <action>For each of the 12 existing `algorithm` floats, replace the `\noindent\textbf{Input:}` / `\textbf{Output:}` lines and inner `enumerate` body with `\begin{algorithmic}[1]`, `\Require`, `\Ensure`, `\State`, and `\Comment{...}`. Preserve captions and labels. Convert prose-first list items into math/operator-first statements: assignments, optimizations, set updates, packet selection, exchange, alignment, fusion, query-return, or control-like statements should come before the explanatory `\Comment{...}`. Keep comments short and explanatory, not as leading prose. Use `\Statex` only when an equation is too wide for a readable `\State`. Do not reduce or omit any algorithm step; preserve the existing method mechanics while changing presentation.</action>
  <verify>
    <automated>python - <<'PY'
from pathlib import Path
text = Path('research/slam-survey/main.tex').read_text()
alg_count = text.count('\\begin{algorithm}[H]')
algorithmic_count = text.count('\\begin{algorithmic}[1]')
state_count = text.count('\\State')
comment_count = text.count('\\Comment{')
require_count = text.count('\\Require')
ensure_count = text.count('\\Ensure')
inside_enumerate = 0
pos = 0
while True:
    start = text.find('\\begin{algorithm}[H]', pos)
    if start == -1:
        break
    end = text.find('\\end{algorithm}', start)
    block = text[start:end]
    if '\\begin{enumerate}' in block or '\\end{enumerate}' in block:
        inside_enumerate += 1
    pos = end + len('\\end{algorithm}')
assert alg_count == 12, alg_count
assert algorithmic_count == 12, algorithmic_count
assert require_count == 12, require_count
assert ensure_count == 12, ensure_count
assert state_count >= 70, state_count
assert comment_count >= 12, comment_count
assert inside_enumerate == 0, inside_enumerate
PY</automated>
  </verify>
  <done>All 12 algorithm floats contain `algorithmic` bodies with `\Require`, `\Ensure`, `\State`, and `\Comment{...}`, and no `enumerate` environment remains inside any algorithm float.</done>
</task>

<task type="auto">
  <name>Task 3: Compile the survey PDF and record the quick-task summary</name>
  <files>research/slam-survey/main.tex, research/slam-survey/main.pdf, .planning/quick/260521-deu-research-latex-algorithm-packages-patter/260521-deu-SUMMARY.md</files>
  <action>Run Tectonic from `research/slam-survey` so `main.pdf` is compiled and left in place. After the compile passes, create the GSD summary at `.planning/quick/260521-deu-research-latex-algorithm-packages-patter/260521-deu-SUMMARY.md` describing the algorithmicx conversion, verification counts, and PDF compile result.</action>
  <verify>
    <automated>cd research/slam-survey && tectonic main.tex && test -s main.pdf</automated>
    <automated>test -s .planning/quick/260521-deu-research-latex-algorithm-packages-patter/260521-deu-SUMMARY.md</automated>
  </verify>
  <done>`tectonic main.tex` succeeds, `research/slam-survey/main.pdf` exists and is non-empty after compilation, and the quick-task summary exists at the required path.</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| LaTeX source to Tectonic engine | Edited TeX macros and package imports are compiled by Tectonic into PDF output. |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-quick-260521-deu-01 | Tampering | `research/slam-survey/main.tex` algorithm floats | mitigate | Preserve captions/labels and verify exactly 12 algorithm floats, 12 algorithmic blocks, 12 `\Require`, 12 `\Ensure`, and zero enumerate bodies inside algorithms. |
| T-quick-260521-deu-02 | Denial of Service | Tectonic compile | mitigate | Run `tectonic main.tex` from `research/slam-survey` and require non-empty `main.pdf`. |
| T-quick-260521-deu-SC | Tampering | LaTeX package selection | mitigate | Use researched existing TeX package `algpseudocode`; do not add npm/pip/cargo installs. |
</threat_model>

<verification>
Run the Task 2 Python structural check, then run `cd research/slam-survey && tectonic main.tex && test -s main.pdf`. Inspect any compile error before changing package strategy; the locked direction is `algpseudocode` inside the existing custom `algorithm` float.
</verification>

<success_criteria>
- `research/slam-survey/main.tex` loads `algpseudocode` and does not load the older `algorithm` or `algorithmic` packages.
- Exactly 12 algorithm floats contain exactly 12 `algorithmic` bodies.
- All 12 algorithm bodies use `\Require`, `\Ensure`, `\State`, and short trailing `\Comment{...}` where explanatory context is needed.
- No `enumerate` body remains inside any algorithm float.
- `tectonic main.tex` succeeds and leaves `research/slam-survey/main.pdf` in place.
- `.planning/quick/260521-deu-research-latex-algorithm-packages-patter/260521-deu-SUMMARY.md` exists when execution finishes.
</success_criteria>

<output>
Create `.planning/quick/260521-deu-research-latex-algorithm-packages-patter/260521-deu-SUMMARY.md` when done.
</output>
