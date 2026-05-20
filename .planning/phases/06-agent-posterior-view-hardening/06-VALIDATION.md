---
phase: 06
slug: agent-posterior-view-hardening
status: draft
nyquist_compliant: true
wave_0_complete: false
created: 2026-05-20
---

# Phase 06 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | `pytest` via `uv run` |
| **Config file** | `pyproject.toml` with `testpaths = ["tests"]` and `pythonpath = ["src"]` |
| **Quick run command** | `uv run pytest tests/agents/test_queries.py tests/agents/test_splat_posterior.py tests/test_public_api.py -q` |
| **Full suite command** | `uv run pytest -q` |
| **Estimated runtime** | ~1 second |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest tests/agents/test_queries.py tests/agents/test_splat_posterior.py tests/test_public_api.py -q`
- **After every plan wave:** Run `uv run pytest -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 06-01-01 | 01 | 1 | AGNT-02 | T-06-01 | Local query outputs stay bounded by `LocalRadiusQuery.max_results` and expose truncation metadata instead of raw full-map dumps. | unit | `uv run pytest tests/agents/test_queries.py tests/agents/test_splat_posterior.py -q` | ✅ | ⬜ pending |
| 06-01-02 | 01 | 1 | AGNT-02 | T-06-02 | `SplatPosteriorView.uncertainty()` returns descriptive covariance/opacity statistics with `semantics == "descriptive_only"`. | unit | `uv run pytest tests/agents/test_queries.py tests/agents/test_splat_posterior.py -q` | ✅ | ⬜ pending |
| 06-02-01 | 02 | 2 | AGNT-04 | — | Repeated local, summary, uncertainty, and provenance calls against a fixed `SplatMap` return exactly equal frozen dataclasses. | unit | `uv run pytest tests/agents/test_splat_posterior.py -q` | ✅ | ⬜ pending |
| 06-03-01 | 03 | 3 | AGNT-02 | T-06-02 / T-06-04 | Public exports and README language describe bounded descriptive posterior views and keep Phase 7 memory/tool/provider concepts out of Phase 6. | unit/docs smoke | `uv run pytest tests/agents/test_queries.py tests/test_public_api.py -q` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/agents/test_queries.py` — add failing tests for `LocalRadiusQuery.max_results`, `SplatQueryResult.total_matches`, `SplatQueryResult.truncated`, `PosteriorUncertaintySummary`, and `AgentQueryKind.UNCERTAINTY` exports.
- [ ] `tests/agents/test_splat_posterior.py` — add failing tests for bounded local over-limit behavior, `uncertainty()`, exact repeated-call determinism, and aggregate-only provenance behavior.
- [ ] `tests/test_public_api.py` — add failing tests for root exports if the new uncertainty summary is promoted to root API, plus README boundary language.

---

## Manual-Only Verifications

All phase behaviors have automated verification.

---

## Threat Model

| Threat ID | STRIDE | Scenario | Mitigation | Verification |
|-----------|--------|----------|------------|--------------|
| T-06-01 | Information Disclosure | A local radius query over a large map returns every matching splat ID by default, acting as a raw map dump. | Require a positive `LocalRadiusQuery.max_results` default/field and return only the first matching IDs up to that limit. | Tests assert over-limit queries return bounded IDs, `total_matches`, and `truncated is True`. |
| T-06-02 | Information Integrity | Consumers mistake covariance/opacity statistics for calibrated belief, optimized posterior fusion quality, or reconstruction quality. | Add a stable `descriptive_only` semantics label and README boundary wording. | Tests assert `summary.semantics == "descriptive_only"` and README contains the boundary language. |
| T-06-03 | Tampering | Returned provenance source counts can be mutated by consumers after construction. | Continue using copied immutable mappings via `MappingProxyType`. | Tests assert mutating `source_counts` raises `TypeError`. |
| T-06-04 | Supply Chain / Boundary Creep | Agent posterior APIs import LLM, ROS, Habitat, tensor, or backend packages. | Keep Phase 6 implementation pure Python and provider-free. | Existing provider-free import boundary test remains green. |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 5s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-05-20
