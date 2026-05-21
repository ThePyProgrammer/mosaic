---
phase: 07
slug: representation-memories-and-tools
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-05-21
---

# Phase 07 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | pyproject.toml |
| **Quick run command** | `uv run pytest tests/agents tests/evaluation -q` |
| **Full suite command** | `uv run pytest -q` |
| **Estimated runtime** | ~10 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest tests/agents tests/evaluation -q`
- **After every plan wave:** Run `uv run pytest -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 07-TBD | TBD | TBD | REPR-01..REPR-08 | TBD | N/A | unit/scenario | `uv run pytest tests/agents tests/evaluation -q` | TBD | pending |

*Status: pending · green · red · flaky*

---

## Wave 0 Requirements

- [ ] Planner must assign concrete tests under `tests/agents/` and `tests/evaluation/` for each plan task.
- [ ] Planner must map every REPR-01 through REPR-08 behavior to at least one automated pytest command.

---

## Manual-Only Verifications

All phase behaviors should have automated verification through deterministic unit or scenario tests.

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
