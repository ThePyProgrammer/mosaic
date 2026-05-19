---
phase: 04
slug: fusion-diagnostics-and-semantics-hardening
status: approved
nyquist_compliant: true
wave_0_complete: true
created: 2026-05-19
---

# Phase 04 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | `pyproject.toml` |
| **Quick run command** | `uv run pytest tests/fusion -q` |
| **Full suite command** | `uv run pytest -q` |
| **Estimated runtime** | ~5 seconds focused, ~15 seconds full |

---

## Sampling Rate

- **After every task commit:** Run the task's automated command from the map below.
- **After every plan wave:** Run `uv run pytest tests/fusion -q` for Waves 1-2 and `uv run pytest -q` for Wave 3.
- **Before `/gsd:verify-work`:** `uv run pytest -q` must exit 0.
- **Max feedback latency:** 15 seconds.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 04-01-01 | 01 | 1 | FUSE-02 | T-04-01 / T-04-02 / T-04-03 / T-04-04 | Summary mappings are copied/frozen, scalar diagnostics stay bounded, and non-finite uncertainty stats are rejected. | unit | `uv run pytest tests/fusion/test_fusion_protocol.py -q` | yes | pending |
| 04-01-02 | 01 | 1 | FUSE-02 | T-04-01 / T-04-02 / T-04-03 / T-04-04 | `FusionResult` exposes typed summaries while preserving scalar diagnostic stability. | unit | `uv run pytest tests/fusion/test_fusion_protocol.py -q` | yes | pending |
| 04-01-03 | 01 | 1 | FUSE-02 | T-04-04 | `mosaic.fusion` exports fusion-prefixed summaries without exposing raw splat lineage. | unit | `uv run pytest tests/fusion/test_fusion_protocol.py -q` | yes | pending |
| 04-02-01 | 02 | 2 | FUSE-02, FUSE-04 | T-04-05 / T-04-06 / T-04-07 / T-04-08 | Strategy diagnostics preserve splats and report the stable `preserved_not_optimized` label. | unit | `uv run pytest tests/fusion/test_strategies.py -q` | yes | pending |
| 04-02-02 | 02 | 2 | FUSE-02, FUSE-04 | T-04-05 / T-04-06 / T-04-07 / T-04-08 | Conservative conflicts are deterministic diagnostics and do not reject or merge splats. | unit | `uv run pytest tests/fusion/test_strategies.py -q` | yes | pending |
| 04-02-03 | 02 | 2 | FUSE-02, FUSE-04 | T-04-05 / T-04-06 / T-04-07 / T-04-08 | Focused fusion suite passes with typed summaries and anti-grid preservation behavior. | integration | `uv run pytest tests/fusion -q` | yes | pending |
| 04-03-01 | 03 | 3 | FUSE-02, FUSE-04 | T-04-09 / T-04-10 / T-04-11 / T-04-12 | README contract asserts the stable label and non-optimization/non-grid boundary language. | documentation contract | `uv run pytest tests/test_readme_contract.py -q` | yes | pending |
| 04-03-02 | 03 | 3 | FUSE-02, FUSE-04 | T-04-09 / T-04-10 / T-04-11 / T-04-12 | Public docs avoid claims of Gaussian optimization quality and avoid new dependency instructions. | documentation contract | `uv run pytest tests/test_readme_contract.py -q` | yes | pending |
| 04-03-03 | 03 | 3 | FUSE-02, FUSE-04 | T-04-09 / T-04-10 / T-04-11 / T-04-12 | Full suite verifies public API, fusion behavior, README contracts, evaluation artifacts, backend contracts, and agent posterior tests. | full regression | `uv run pytest -q` | yes | pending |

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements:

- `pyproject.toml` configures pytest with `pythonpath = ["src"]` and `testpaths = ["tests"]`.
- `tests/fusion/test_fusion_protocol.py` exists for protocol-layer checks.
- `tests/fusion/test_strategies.py` exists for strategy behavior checks.
- `tests/test_readme_contract.py` exists for README contract checks.
- No dependency installation, test scaffold, or fixture bootstrap is required before Wave 1.

---

## Manual-Only Verifications

All Phase 04 behaviors have automated verification through the commands above.

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify commands.
- [x] Sampling continuity: no 3 consecutive tasks without automated verify.
- [x] Wave 0 covers all missing infrastructure references.
- [x] No watch-mode flags.
- [x] Feedback latency < 15 seconds.
- [x] `nyquist_compliant: true` set in frontmatter.

**Approval:** approved 2026-05-19
