---
phase: 04-fusion-diagnostics-and-semantics-hardening
reviewed: 2026-05-19T00:00:00Z
depth: standard
files_reviewed: 7
files_reviewed_list:
  - src/mosaic/fusion/protocol.py
  - src/mosaic/fusion/__init__.py
  - tests/fusion/test_fusion_protocol.py
  - src/mosaic/fusion/strategies.py
  - tests/fusion/test_strategies.py
  - README.md
  - tests/test_readme_contract.py
findings:
  critical: 1
  warning: 3
  info: 0
  total: 4
status: issues_found
---

# Phase 4: Code Review Report

**Reviewed:** 2026-05-19T00:00:00Z  
**Depth:** standard  
**Files Reviewed:** 7  
**Status:** issues_found

## Summary

Reviewed the Phase 4 fusion diagnostics and semantics hardening changes across the fusion protocol, provenance-preserving strategy, public fusion exports, README contract language, and README tests.

The implementation has one correctness blocker: `ProvenancePreservingFusion` can crash on a currently valid `GaussianSplat` input with blank provenance. There are also contract/test quality gaps around unchecked runtime diagnostics values and a broken README smoke example that the README tests fail to execute.

## Critical Issues

### CR-01: Blank splat provenance crashes fusion instead of being normalized or rejected at the boundary

**File:** `src/mosaic/fusion/strategies.py:143-144`

**Issue:** `_provenance_key()` only normalizes `None` to `"unknown"`, while `GaussianSplat` currently permits `provenance=""` and `provenance=" "`. Those values are therefore valid inputs to `ProvenancePreservingFusion.fuse()`, but `_summarize_provenance()` passes the blank key into `FusionProvenanceSummary`, which rejects blank provenance names and raises `ValueError`.

**Fix:** Normalize blank provenance the same way as missing provenance, or move the rejection into `GaussianSplat` so invalid provenance is rejected at construction time. The safer local fix is to normalize blank strings to `"unknown"` and add a regression test.

## Warnings

### WR-01: `FusionResult.diagnostics` claims scalar typed values but accepts arbitrary runtime objects

**File:** `src/mosaic/fusion/protocol.py:124-125`

**Issue:** `FusionMetricValue` is declared as `bool | int | float | str`, but `FusionResult.__post_init__()` only freezes `diagnostics`; it does not validate keys or values. Because this is a runtime Python library and the project convention is to validate dataclass invariants in `__post_init__()`, callers can create invalid diagnostics that break downstream JSON artifact/export code later.

**Fix:** Validate diagnostic keys and values before freezing, including blank keys, unsupported value types, and non-finite floats.

### WR-02: README fusion smoke example uses a non-existent `FusionResult.map` attribute

**File:** `README.md:123-127`

**Issue:** The README smoke example uses `result.map`, but `FusionResult` exposes `fused_map`. Running this documented example raises `AttributeError`.

**Fix:** Use `result.fused_map`.

### WR-03: README contract tests only check strings, so broken public smoke examples pass

**File:** `tests/test_readme_contract.py:101-119`

**Issue:** The README tests assert required headings, strings, and boundary phrases, but they do not execute the README fusion example. As a result, the broken fusion example passes the test suite even though it fails at runtime.

**Fix:** Add a focused executable smoke test for the README fusion example.

### WR-04: Root public exports do not include the new Phase 4 fusion summary types

**File:** `README.md:47-58`

**Issue:** The subpackage export in `src/mosaic/fusion/__init__.py` is correct, but the reviewer suggested the root public surface is inconsistent with the README’s public export contract.

**Disposition:** Push back unless the public API policy changes. The README states root `mosaic` re-exports stable Phase 1 primitives and documents the new summary types under the `mosaic.fusion` row, not as root exports.

---

_Reviewed: 2026-05-19T00:00:00Z_  
_Reviewer: Claude (gsd-code-reviewer)_  
_Depth: standard_
