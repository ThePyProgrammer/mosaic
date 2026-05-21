---
phase: 07-representation-memories-and-tools
reviewed: 2026-05-21T03:52:34Z
depth: standard
files_reviewed: 7
files_reviewed_list:
  - src/mosaic/__init__.py
  - src/mosaic/agents/__init__.py
  - src/mosaic/agents/memory.py
  - tests/agents/test_representation_claims.py
  - tests/agents/test_representation_memory.py
  - tests/evaluation/test_representation_scenarios.py
  - tests/test_public_api.py
findings:
  critical: 0
  warning: 3
  info: 0
  total: 3
status: issues_found
---

# Phase 07: Code Review Report

**Reviewed:** 2026-05-21T03:52:34Z
**Depth:** standard
**Files Reviewed:** 7
**Status:** issues_found

## Summary

Reviewed the Phase 7 representation memory API changes and related public API/test coverage. No critical security issues were found, but the memory contracts currently admit invalid numeric state, allow nonsensical self-conflicting commitments, and one public API test is tied to the caller's current working directory.

## Narrative Findings (AI reviewer)

## Warnings

### WR-01: Unit-interval validation accepts NaN values

**File:** `src/mosaic/agents/memory.py:742-744`

**Issue:** `_validate_unit_interval()` only checks `value < 0.0 or value > 1.0`. `float("nan")` makes both comparisons false, so confidence and traversability fields can be constructed with NaN. That breaks the typed memory contract: query results can carry non-orderable/non-serializable belief scores even though the API promises bounded numeric confidence/traversability values.

**Fix:** Reject non-finite values explicitly before the range check.

```python
from math import isfinite


def _validate_unit_interval(value: float, label: str) -> None:
    if not isfinite(value) or value < 0.0 or value > 1.0:
        raise ValueError(f"{label} must be finite and between 0 and 1")
```

### WR-02: Commitments can conflict with themselves

**File:** `src/mosaic/agents/memory.py:270-278`

**Issue:** `Claim.__post_init__()` rejects self-conflicts, but `Commitment.__post_init__()` does not. A `Commitment` can include its own `commitment_id` in `conflict_ids`, producing an impossible coordination state that downstream conflict tooling cannot distinguish from a real multi-robot conflict.

**Fix:** Mirror the claim invariant for commitments.

```python
object.__setattr__(self, "claim_ids", tuple(self.claim_ids))
object.__setattr__(self, "conflict_ids", tuple(self.conflict_ids))
if self.commitment_id in self.conflict_ids:
    raise ValueError("Commitment conflict_ids must not include its own commitment_id")
object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))
```

### WR-03: README assertions depend on current working directory

**File:** `tests/test_public_api.py:100-102` and `tests/test_public_api.py:183-185`

**Issue:** The tests read `Path("README.md")`, which only works when pytest is launched from the repository root. Running the file from another working directory, an IDE, or some CI test collectors will fail with `FileNotFoundError` even though the package behavior is unchanged.

**Fix:** Resolve README relative to the test file instead of the process working directory.

```python
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_readme_locks_real_backend_integration_block() -> None:
    readme = (PROJECT_ROOT / "README.md").read_text()
```

---

_Reviewed: 2026-05-21T03:52:34Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
