# Quick Research: LaTeX pseudocode-first algorithm blocks

**Researched:** 2026-05-21
**Task:** Update `research/slam-survey/main.tex` algorithms from prose-first ordered items to pseudocode/math-first lines with explanatory trailing comments.
**Confidence:** HIGH for package capabilities; MEDIUM for final lowest-risk choice because compile behavior must still be verified after editing.

## Recommendation

Use `algorithmicx` with the `algpseudocode` style inside the paper's existing custom `algorithm` float, not the older `algorithms` bundle float. `algorithmicx` explicitly does not define a floating environment and expects a float from another package; this makes it compatible with the current `\newfloat{algorithm}{tbp}{loa}` approach. [CITED: https://ctan.org/pkg/algorithmicx] [CITED: algorithmicx.pdf]

Keep the existing float definition:

```latex
\floatstyle{ruled}
\newfloat{algorithm}{tbp}{loa}
\floatname{algorithm}{Algorithm}
```

Add only the pseudocode package:

```latex
\usepackage{algpseudocode}
```

Then replace each `enumerate` block inside `algorithm` with:

```latex
\begin{algorithmic}[1]
  \Require RGB-D streams $\{\mathcal{Z}_i^{1:t}\}_{i\in\mathcal{A}}$; local maps $\{\mathcal{M}_{i,t-1}\}$
  \Ensure Global Gaussian map $\mathcal{G}_t$
  \State $\hat{\mathbf{T}}_{\ell_i\leftarrow i,t} \gets \arg\min_{\mathbf{T}\in SE(3)}
    \mathcal{L}_{\mathrm{rgbd}}(z_{i,t},\mathrm{render}(\mathcal{M}_{i,t-1},\mathbf{T}))$
    \Comment{local photometric--depth tracking}
  \State $\mathcal{M}_{i,t} \gets \phi_i(\mathcal{Z}_i^{1:t},\hat{\mathbf{X}}_{i,1:t},\mathcal{P}_{i,t})$
    \Comment{update local Gaussian map}
  \State $p_{i,t} \gets \mu_i(\mathcal{M}_{i,t},\mathcal{K}_{i,t},\hat{\mathbf{X}}_{i,1:t};b_i)$
    \Comment{bounded packet selection}
  \State $\mathcal{G}_t \gets \Psi_t(\{\mathbf{T}_{0\leftarrow i,t}\mathcal{M}_{i,t}\}_i,\mathcal{C}_t,\mathcal{P}_t)$
    \Comment{global fusion}
\end{algorithmic}
```

## Findings

- `algorithmicx` is a CTAN package for flexible pseudocode/source-code typesetting and includes the `algpseudocode` style. [CITED: https://ctan.org/pkg/algorithmicx]
- The `algpseudocode` style provides `\Require`, `\Ensure`, `\State`, `\Statex`, `\Comment`, `\If`, `\For`, `\While`, `\Repeat`, `\Return`, `\Procedure`, and related end commands. These match the requested pseudocode-first style with side comments. [CITED: algorithmicx.pdf]
- `algorithmicx` documentation states it "does not define any floating environment" and that "the floating environment has to be provided by another package," so it can be embedded in the existing custom float rather than replacing it. [CITED: algorithmicx.pdf]
- CTAN's older `algorithms` bundle consists of two environments, `algorithm` and `algorithmic`; using its `algorithm` float would collide conceptually with the paper's already-defined custom `algorithm` float and is higher risk for this document. [CITED: https://ctan.org/pkg/algorithms]
- The current source defines a custom ruled `algorithm` float and has 12 algorithm blocks whose bodies are `enumerate` lists: seven method algorithms and five taxonomy-pattern algorithms. [VERIFIED: codebase grep]
- Local tool audit: `tectonic 0.15.0` is available; `kpsewhich` is not installed, so local TeX package presence could not be preflighted with `kpsewhich`. Tectonic may still fetch/use bundle packages during compile. [VERIFIED: local shell]

## Lowest-risk edit pattern

1. Add `\usepackage{algpseudocode}` after the math/list packages in the preamble.
2. Do not add `\usepackage{algorithm}` or `\usepackage{algorithmic}`; the paper already owns the float through `float` + `\newfloat`.
3. For each block, move Input/Output into `\Require` and `\Ensure` lines inside `algorithmic`.
4. Convert each prose `\item` into a `\State` whose first token is the operation or assignment, then attach a short `\Comment{...}` when explanatory context is needed.
5. Keep long equations either inline in `\State` or split as `\Statex \[ ... \]` when line width would be bad. Prefer concise inline assignments for this paper to avoid tall algorithm boxes.

## Anti-patterns to avoid

- Do not use prose-first `\item Estimate ...` lines; they reproduce the current problem.
- Do not load the `algorithms` bundle's `algorithm` float unless the custom float is removed; otherwise the document has two competing notions of `algorithm`.
- Do not turn explanatory comments into leading text. The visual grammar should be `assignment/control-flow` first, `\Comment{explanation}` second.
- Do not overuse `\Procedure` wrappers; these survey boxes describe method mechanics, not callable procedures.

## Sources

- CTAN `algorithmicx`: https://ctan.org/pkg/algorithmicx
- CTAN `algorithmicx` manual: https://mirrors.ctan.org/macros/latex/contrib/algorithmicx/algorithmicx.pdf
- CTAN `algorithms`: https://ctan.org/pkg/algorithms
- Codebase grep of `/home/prannayag/pragnition/robotics/mosaic/research/slam-survey/main.tex`
