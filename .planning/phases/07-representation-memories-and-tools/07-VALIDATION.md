---
phase: 07
slug: representation-memories-and-tools
status: draft
nyquist_compliant: true
wave_0_complete: true
created: 2026-05-21
updated: 2026-05-21
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
| 07-01-T1 | 07-01 | 1 | REPR-01, REPR-03, REPR-04, REPR-05, REPR-06 | T-07-01-01, T-07-01-02, T-07-01-04 | Tests require validated immutable IDs, opaque evidence, first-class families, bounded values, and no provider imports before implementation. | unit/red | `uv run pytest tests/agents/test_representation_memory.py -q` | planned: `tests/agents/test_representation_memory.py` | planned |
| 07-01-T2 | 07-01 | 1 | REPR-01, REPR-03, REPR-04, REPR-05, REPR-06 | T-07-01-01, T-07-01-02, T-07-01-03, T-07-01-04, T-07-01-SC | Implements stdlib-only frozen/slotted memory-family contracts with tuple/mapping freezing and invariant validation. | unit/green | `uv run pytest tests/agents/test_representation_memory.py -q` | planned: `src/mosaic/agents/memory.py`, `tests/agents/test_representation_memory.py` | planned |
| 07-02-T1 | 07-02 | 2 | REPR-02 | T-07-02-01, T-07-02-02, T-07-02-03 | Tests require confidence bounds, opaque evidence, visible conflicts, no hidden winner, and supplied-timestamp staleness. | unit/red | `uv run pytest tests/agents/test_representation_claims.py -q` | planned: `tests/agents/test_representation_claims.py` | planned |
| 07-02-T2 | 07-02 | 2 | REPR-02 | T-07-02-01, T-07-02-02, T-07-02-03, T-07-02-04, T-07-02-SC | Implements claim statuses, conflict links, evidence opacity, and deterministic stale transitions without deleting claims. | unit/green | `uv run pytest tests/agents/test_representation_claims.py tests/agents/test_representation_memory.py -q` | planned: `src/mosaic/agents/memory.py`, `tests/agents/test_representation_claims.py` | planned |
| 07-03-T1 | 07-03 | 3 | REPR-01, REPR-03, REPR-04, REPR-05, REPR-06, REPR-07 | T-07-03-01, T-07-03-02, T-07-03-03, T-07-03-04 | Tests require aggregate ownership, immutable synthetic helpers, one named query per family, positive bounds, and truncation metadata. | unit/red | `uv run pytest tests/agents/test_representation_memory.py -q` | planned: `tests/agents/test_representation_memory.py` | planned |
| 07-03-T2 | 07-03 | 3 | REPR-01, REPR-03, REPR-04, REPR-05, REPR-06, REPR-07 | T-07-03-01, T-07-03-02, T-07-03-03, T-07-03-04, T-07-03-SC | Implements aggregate memory, immutable update helpers, bounded query results, and named methods without a facade or generic dispatcher. | unit/green | `uv run pytest tests/agents/test_representation_memory.py tests/agents/test_representation_claims.py -q` | planned: `src/mosaic/agents/memory.py`, `tests/agents/test_representation_memory.py` | planned |
| 07-04-T1 | 07-04 | 4 | REPR-01, REPR-02, REPR-03, REPR-04, REPR-05, REPR-06, REPR-07 | T-07-04-02, T-07-04-03, T-07-04-04 | Tests lock stable public exports through `mosaic.agents` and selected root `mosaic` exports while preserving version. | public-api/red | `uv run pytest tests/test_public_api.py -q` | planned: `tests/test_public_api.py` | planned |
| 07-04-T2 | 07-04 | 4 | REPR-01, REPR-02, REPR-03, REPR-04, REPR-05, REPR-06, REPR-07 | T-07-04-01, T-07-04-02, T-07-04-03, T-07-04-04, T-07-04-SC | Implements explicit barrel exports with no wildcard imports, no dependency leakage, and stable selected root surface. | public-api/green | `uv run pytest tests/test_public_api.py tests/agents/test_representation_memory.py tests/agents/test_representation_claims.py -q` | planned: `src/mosaic/agents/__init__.py`, `src/mosaic/__init__.py`, `tests/test_public_api.py` | planned |
| 07-05-T1 | 07-05 | 4 | REPR-02, REPR-03, REPR-04, REPR-05, REPR-07, REPR-08 | T-07-05-01, T-07-05-02, T-07-05-03, T-07-05-04 | Evaluation tests cover blocked path and search frontier with visible conflicts, stale claims, frontier/traversability rows, and no runtime-provider claims. | scenario | `uv run pytest tests/evaluation/test_representation_scenarios.py -q` | planned: `tests/evaluation/test_representation_scenarios.py` | planned |
| 07-05-T2 | 07-05 | 4 | REPR-06, REPR-07, REPR-08 | T-07-05-03, T-07-05-04, T-07-05-SC | Evaluation tests cover task allocation conflicts and capability-oriented memory ablations without numeric ARNA/runtime claims. | scenario | `uv run pytest tests/evaluation/test_representation_scenarios.py -q` | planned: `tests/evaluation/test_representation_scenarios.py` | planned |

*Status: planned · green · red · flaky*

---

## Wave 0 Requirements

- [x] Planner assigned concrete tests under `tests/agents/`, `tests/test_public_api.py`, and `tests/evaluation/` for each plan task.
- [x] Planner mapped every REPR-01 through REPR-08 behavior to at least one automated pytest command.
- [x] No task has an automated verify marked MISSING.

---

## Requirement Coverage Map

| Requirement | Covered By | Primary Command |
|-------------|------------|-----------------|
| REPR-01 | 07-01-T1, 07-01-T2, 07-03-T1, 07-03-T2, 07-04-T1, 07-04-T2 | `uv run pytest tests/agents/test_representation_memory.py -q` |
| REPR-02 | 07-02-T1, 07-02-T2, 07-04-T1, 07-04-T2, 07-05-T1 | `uv run pytest tests/agents/test_representation_claims.py -q` |
| REPR-03 | 07-01-T1, 07-01-T2, 07-03-T1, 07-03-T2, 07-05-T1 | `uv run pytest tests/agents/test_representation_memory.py tests/evaluation/test_representation_scenarios.py -q` |
| REPR-04 | 07-01-T1, 07-01-T2, 07-03-T1, 07-03-T2, 07-05-T1 | `uv run pytest tests/agents/test_representation_memory.py tests/evaluation/test_representation_scenarios.py -q` |
| REPR-05 | 07-01-T1, 07-01-T2, 07-03-T1, 07-03-T2, 07-05-T1 | `uv run pytest tests/agents/test_representation_memory.py tests/evaluation/test_representation_scenarios.py -q` |
| REPR-06 | 07-01-T1, 07-01-T2, 07-03-T1, 07-03-T2, 07-05-T2 | `uv run pytest tests/agents/test_representation_memory.py tests/evaluation/test_representation_scenarios.py -q` |
| REPR-07 | 07-03-T1, 07-03-T2, 07-04-T1, 07-04-T2, 07-05-T1, 07-05-T2 | `uv run pytest tests/agents/test_representation_memory.py -q` |
| REPR-08 | 07-05-T1, 07-05-T2 | `uv run pytest tests/evaluation/test_representation_scenarios.py -q` |

---

## Manual-Only Verifications

All phase behaviors should have automated verification through deterministic unit, public API, or scenario tests.

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 10s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** planned validation map complete
