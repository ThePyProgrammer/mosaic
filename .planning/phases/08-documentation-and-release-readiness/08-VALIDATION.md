---
phase: 08
slug: documentation-and-release-readiness
status: ready
nyquist_compliant: true
wave_0_complete: true
created: 2026-05-21
---

# Phase 08 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest |
| **Config file** | `pyproject.toml` |
| **Quick run command** | `uv run pytest tests/test_readme_contract.py -q` or `uv run pytest tests/test_docs_contract.py -q` after Plan 08-02 creates split-doc tests |
| **Full suite command** | `uv run pytest -q` |
| **Estimated runtime** | ~1 second |

---

## Sampling Rate

- **After every task commit:** Run the task-specific `<automated>` command from the active PLAN.md
- **After every plan wave:** Run `uv run pytest -q` once all plans in the wave are complete
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 08-01-01 | 01 | 1 | DOCS-01 | T-08-01-01/T-08-01-02/T-08-01-03 | README contract rejects stale phase language, missing split-doc links, unsupported integration claims, and unsafe install-command wording | contract | `uv run pytest tests/test_readme_contract.py -q` | ✅ existing test file | ⬜ pending |
| 08-01-02 | 01 | 1 | DOCS-01/DOCS-02/DOCS-03 | T-08-01-01/T-08-01-02/T-08-01-04 | README is release-versioned, concise, links split docs, preserves dependency boundary, and previews golden path without overclaiming | contract + full suite | `uv run pytest tests/test_readme_contract.py -q`; `uv run pytest -q` | ✅ README.md | ⬜ pending |
| 08-02-01 | 02 | 1 | DOCS-01/DOCS-02 | T-08-02-01/T-08-02-02/T-08-02-03 | Split-doc tests cover docs/API.md and docs/EXAMPLES.md plus representative local benchmark artifact, actual DeterministicSplatBackend SplatMap snapshot, SplatPosteriorView LocalRadiusQuery/query_local behavior, and bounded RepresentationMemory query behavior; no CONTRIBUTING.md or README contributor-link assertion in this plan | contract/API smoke | `uv run pytest tests/test_docs_contract.py -q` | ❌ created by task | ⬜ pending |
| 08-02-02 | 02 | 1 | DOCS-01 | T-08-02-01/T-08-02-04 | API docs document implemented exports and deferred integration boundaries without install guidance for heavy packages | contract | `uv run pytest tests/test_docs_contract.py -q` | ❌ created by task | ⬜ pending |
| 08-02-03 | 02 | 1 | DOCS-02 | T-08-02-02/T-08-02-03 | Golden-path docs use deterministic local APIs, include both a disposable benchmark artifact and an actual backend SplatMap snapshot, sequence SplatPosteriorView/LocalRadiusQuery/query_local before RepresentationMemory.query_navigation_frontiers, and avoid raw-map/provider overclaims | contract + full suite | `uv run pytest tests/test_docs_contract.py -q`; `uv run pytest -q` | ❌ created by task | ⬜ pending |
| 08-03-01 | 03 | 2 | DOCS-03 | T-08-03-01/T-08-03-02/T-08-03-03 | Contributor guidance preserves dependency, optional extras, API stability, test workflow, and backend registry/adapter boundaries using Mosaic v1 foundation release wording rather than phase-era public framing | direct contract + README contract | `uv run python -c 'from pathlib import Path; c = Path("CONTRIBUTING.md").read_text(); p = Path("pyproject.toml").read_text(); assert "dependencies = []" in p; assert "policy-only for the Mosaic v1 foundation release" in c; assert "placeholder extras must not be added until a real optional integration exists" in c; assert all(term in c for term in ("optional extras", "registry", "adapter", "availability", "contract tests", "__all__", "docs/API.md", "tests/test_public_api.py")); assert "Phase 8" not in c'`; `uv run pytest tests/test_readme_contract.py -q` | ❌ created by task | ⬜ pending |
| 08-03-02 | 03 | 2 | DOCS-03 | T-08-03-01/T-08-03-04 | Final release gate verifies CONTRIBUTING.md policy, rejects "Phase 8" public framing in CONTRIBUTING.md, verifies README links to all release docs after CONTRIBUTING.md exists, public docs avoid unsafe heavy-integration install commands, and full suite passes | contract + full suite | `uv run pytest tests/test_docs_contract.py -q`; `uv run pytest tests/test_readme_contract.py -q`; `uv run pytest -q` | ✅ split-doc test file from Plan 08-02 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

No separate Wave 0 scaffold is required. Every planned task includes at least one `<automated>` verification command. Plan 08-02 intentionally creates split-doc tests for API/examples only; Plan 08-03 adds CONTRIBUTING.md and the final README contributor-link assertions after the contributor document exists.

---

## Manual-Only Verifications

All phase behaviors have automated verification.

---

## Validation Sign-Off

- [x] All seven planned tasks have `<automated>` verify commands
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references; no separate Wave 0 scaffold is needed because missing docs/tests are created by planned tasks with automated gates
- [x] No watch-mode flags
- [x] Feedback latency < 10s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** ready for execution
