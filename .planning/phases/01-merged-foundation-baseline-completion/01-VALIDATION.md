---
phase: 01
slug: merged-foundation-baseline-completion
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-05-18
---

# Phase 01 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 9.0.3 in the uv project environment |
| **Config file** | `pyproject.toml` (`testpaths = ["tests"]`, `pythonpath = ["src"]`) |
| **Quick run command** | `uv run pytest tests/test_public_api.py tests/test_package_import.py -q` |
| **Full suite command** | `uv run pytest -q` |
| **Estimated runtime** | ~1 second |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest tests/test_public_api.py tests/test_package_import.py -q` plus targeted module tests changed by the task.
- **After every plan wave:** Run `uv run pytest -q`.
- **Before `/gsd:verify-work`:** Full suite must be green and remain at or above the observed 73 passing tests.
- **Max feedback latency:** 10 seconds.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 01-01-01 | 01 | 1 | BASE-01 | T-01-01 | Package imports do not load heavy/CUDA/native/LLM dependencies | smoke | `uv run pytest tests/test_package_import.py -q` | yes | pending |
| 01-01-02 | 01 | 1 | BASE-02 | T-01-01 | Public exports remain explicit package surfaces | smoke | `uv run pytest tests/test_public_api.py -q` | yes | pending |
| 01-01-03 | 01 | 1 | BASE-03 | T-01-02 | README examples use local project paths and avoid privileged/system artifact paths | doc review | `test -s README.md` plus checklist review | yes | pending |
| 01-01-04 | 01 | 1 | BASE-04 | T-01-01 | Full test workflow passes from the main checkout | suite | `uv run pytest -q` | yes | pending |
| 01-02-01 | 02 | 1 | FUSE-01 | T-01-03 | Fusion input validation preserves frame compatibility and read-only diagnostics | unit | `uv run pytest tests/fusion/test_fusion_protocol.py -q` | yes | pending |
| 01-02-02 | 02 | 1 | FUSE-03 | T-01-03 | Reference fusion preserves provenance without claiming optimized uncertainty | unit | `uv run pytest tests/fusion/test_strategies.py -q` | yes | pending |
| 01-03-01 | 03 | 1 | EVAL-01 | T-01-02 | Synthetic scenario remains deterministic and provider-free | unit/integration | `uv run pytest tests/evaluation/test_scenarios.py tests/evaluation/test_runner.py -q` | yes | pending |
| 01-03-02 | 03 | 1 | EVAL-03 | T-01-02 | Benchmark artifacts serialize deterministically to local caller-provided paths | unit | `uv run pytest tests/evaluation/test_runner.py tests/evaluation/test_regression.py -q` | yes | pending |
| 01-04-01 | 04 | 1 | AGNT-01 | T-01-04 | Posterior query outputs stay bounded typed result objects | unit | `uv run pytest tests/agents/test_queries.py tests/agents/test_splat_posterior.py -q` | yes | pending |
| 01-04-02 | 04 | 1 | AGNT-03 | T-01-04 | Agent API remains provider-free and does not import LLM/ROS/Habitat dependencies | smoke/code review | `uv run pytest tests/agents -q` plus dependency review of `pyproject.toml` | yes | pending |

*Status: pending, green, red, flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all Phase 1 requirements:

- `pyproject.toml` already configures pytest with `tests` and `src` import path.
- `tests/test_package_import.py` and `tests/test_public_api.py` cover baseline import and public API smoke checks.
- Module-level tests exist for fusion, evaluation, and agent posterior behaviors.
- README exists but is empty; filling it is a Phase 1 execution task, not missing test infrastructure.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| README explains Mosaic's library-first scope, fake-backend boundary, install/test commands, v1 module map, and hardening gaps | BASE-03 | Documentation quality and scope framing are semantic, not just file existence | Confirm `README.md` is non-empty and contains sections covering scope, install/test workflow, module map, backend boundary, examples, and known hardening gaps. |
| Dependency boundary remains empty for runtime dependencies | AGNT-03 | Requires package metadata review in addition to import tests | Confirm `pyproject.toml` keeps `dependencies = []` and examples do not require CUDA/native/LLM/ROS/Habitat packages. |

---

## Validation Sign-Off

- [x] All tasks have automated verification or documented manual checks.
- [x] Sampling continuity: no 3 consecutive tasks without automated verification.
- [x] Wave 0 covers all missing test infrastructure references.
- [x] No watch-mode flags.
- [x] Feedback latency < 10 seconds.
- [x] `nyquist_compliant: true` set in frontmatter.

**Approval:** pending
