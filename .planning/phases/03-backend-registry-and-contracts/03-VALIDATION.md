---
phase: 03
slug: backend-registry-and-contracts
status: draft
nyquist_compliant: true
wave_0_complete: false
created: 2026-05-18
---

# Phase 03 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest declared in `pyproject.toml` (`pytest>=8.4.0`) |
| **Config file** | `pyproject.toml` with `testpaths = ["tests"]` and `pythonpath = ["src"]` |
| **Quick run command** | `uv run pytest -q tests/slam/test_backend_contract.py tests/slam/test_backend_registry.py tests/slam/test_backend_contract_helpers.py` |
| **Full suite command** | `uv run pytest -q` |
| **Estimated runtime** | ~2 seconds for targeted SLAM tests; full suite runtime to be measured during execution |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest -q tests/slam/test_backend_contract.py tests/slam/test_backend_registry.py tests/slam/test_backend_contract_helpers.py`
- **After every plan wave:** Run `uv run pytest -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 2 seconds for targeted SLAM tests

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 03-01-01 | 01 | 1 | BACK-01 | T-03-01 | Descriptor metadata is immutable, JSON-ready, and validates blank names/dependencies | unit | `uv run pytest -q tests/slam/test_backend_registry.py` | ❌ W0 | ⬜ pending |
| 03-01-02 | 01 | 1 | BACK-02 | T-03-01 | Availability checks do not invoke factories or import heavy/native backend modules | unit | `uv run pytest -q tests/slam/test_backend_registry.py` | ❌ W0 | ⬜ pending |
| 03-01-03 | 01 | 1 | BACK-03 | T-03-02 | Registry creates fresh backend instances and rejects duplicate backend names | unit | `uv run pytest -q tests/slam/test_backend_registry.py` | ❌ W0 | ⬜ pending |
| 03-02-01 | 02 | 2 | BACK-03 | T-03-03 | Contract helpers skip unavailable backends using availability diagnostics | unit | `uv run pytest -q tests/slam/test_backend_contract_helpers.py` | ❌ W0 | ⬜ pending |
| 03-02-02 | 02 | 2 | BACK-04 | T-03-04 | Lifecycle helpers verify reset, process, snapshot, diagnostics, and deterministic replay without fake-backend geometry overfitting | unit/integration | `uv run pytest -q tests/slam/test_backend_contract.py tests/slam/test_backend_contract_helpers.py` | ⚠️ partial | ⬜ pending |
| 03-02-03 | 02 | 2 | BACK-04 | T-03-04 | Lost tracking and not-initialized state behavior is covered with test-only stubs if deterministic backend remains always-tracking | unit | `uv run pytest -q tests/slam/test_backend_contract_helpers.py` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/slam/test_backend_registry.py` — stubs for BACK-01, BACK-02, and registry factory behavior
- [ ] `tests/slam/test_backend_contract_helpers.py` — stubs for BACK-03 and helper-specific BACK-04 behavior
- [ ] `tests/slam/test_backend_contract.py` — extend or migrate deterministic backend lifecycle assertions through shared helpers

---

## Manual-Only Verifications

All phase behaviors have automated verification.

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all missing references
- [x] No watch-mode flags
- [x] Feedback latency < 2s for targeted SLAM tests
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-05-18
