---
phase: 05
slug: evaluation-metric-and-failure-gate-hardening
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-05-19
---

# Phase 05 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 9.0.3 through `uv run pytest --version` |
| **Config file** | `pyproject.toml` with `testpaths = ["tests"]` and `pythonpath = ["src"]` |
| **Quick run command** | `uv run pytest tests/evaluation -q` |
| **Full suite command** | `uv run pytest -q` |
| **Estimated runtime** | ~1 second |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest tests/evaluation -q`
- **After every plan wave:** Run `uv run pytest -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 05-01-01 | 01 | 1 | EVAL-02 | T-05-01 | Metric names, families, units, and scalar values stay typed and JSON-ready. | unit | `uv run pytest tests/evaluation/test_metrics.py -q` | ✅ | ⬜ pending |
| 05-01-02 | 01 | 1 | EVAL-02 | T-05-01 | Lifecycle, trajectory-hook, map/fusion-proxy, and agent-query-stability metrics stay deterministic. | unit | `uv run pytest tests/evaluation/test_metrics.py -q` | ✅ | ⬜ pending |
| 05-02-01 | 02 | 1 | EVAL-02, EVAL-03 carry-forward | T-05-02 | Benchmark artifacts preserve flat compatibility while adding scenario metadata and JSONL output. | unit/integration | `uv run pytest tests/evaluation/test_runner.py -q` | ✅ | ⬜ pending |
| 05-03-01 | 03 | 2 | EVAL-04 | T-05-03 | Failure classification is derived from gate results with lifecycle > trajectory > map_fusion > agent_query priority. | unit | `uv run pytest tests/evaluation/test_regression.py -q` | ✅ | ⬜ pending |
| 05-03-02 | 03 | 2 | EVAL-05 | T-05-04 | Real backend integration remains blocked until deterministic regression gates pass. | unit/docs smoke | `uv run pytest tests/evaluation/test_regression.py tests/test_public_api.py -q` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements. Extend these existing files before implementation tasks:

- [ ] `tests/evaluation/test_metrics.py` — metric families/categories and hook/proxy semantics for EVAL-02
- [ ] `tests/evaluation/test_runner.py` — scenario summary, JSONL output, gate/failure fields, diagnostics mirrors
- [ ] `tests/evaluation/test_regression.py` — `FailureClass`, gate-derived classification, priority order, readiness helper
- [ ] `tests/test_public_api.py` or a focused README assertion test — real-backend-block wording if the planner chooses a documentation smoke test

---

## Manual-Only Verifications

All phase behaviors have automated verification.

---

## Threat Model

| ID | Threat | Severity | Mitigation | Verification |
|----|--------|----------|------------|--------------|
| T-05-01 | Artifact field injection through non-scalar metric or diagnostic values | medium | Restrict metric/artifact values to JSON-ready scalar types and validate blank names/units/families. | `uv run pytest tests/evaluation/test_metrics.py tests/evaluation/test_runner.py -q` |
| T-05-02 | Invalid JSONL output that cannot be consumed as one benchmark artifact per line | medium | Serialize each artifact as one compact `json.dumps(..., sort_keys=True)` value followed by `\n`. | `uv run pytest tests/evaluation/test_runner.py -q` |
| T-05-03 | Misleading benchmark classification because callers can set arbitrary failure strings | high | Store failure class on gates/results and derive the primary class from failed gates by deterministic priority. | `uv run pytest tests/evaluation/test_regression.py -q` |
| T-05-04 | Real backend/native dependency scope creep before deterministic gates exist | high | Keep default registry deterministic-only and expose a readiness helper that only unlocks after deterministic gates pass. | `uv run pytest tests/evaluation/test_regression.py tests/test_public_api.py -q` |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
