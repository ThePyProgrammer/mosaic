---
status: issues_found
phase: 03-backend-registry-and-contracts
reviewed: 2026-05-19T05:41:33Z
depth: standard
files_reviewed: 7
findings:
  critical: 2
  warning: 2
  info: 0
  total: 4
---

# Phase 03 Code Review

## Summary

Reviewed the backend registry, backend contract helpers, SLAM barrel exports, and related tests. The implementation has correctness defects around runtime dependency boundaries and backend availability semantics. The most serious issue is that importing `mosaic.slam` now requires `pytest`, even though `pytest` is only a dev dependency; this can break normal library consumers.

## Critical Issues

### CR-01: Runtime `mosaic.slam` import depends on dev-only `pytest`

**File:** `src/mosaic/slam/__init__.py`  
**Also affected:** `src/mosaic/slam/contracts.py`

`mosaic.slam.__init__` unconditionally imports contract helpers from `mosaic.slam.contracts`, and `contracts.py` unconditionally imports `pytest`. Since `pyproject.toml` has `pytest` only in the dev dependency group, any installed runtime environment without dev dependencies will fail on `import mosaic.slam`. This violates the pure-library boundary and makes normal use of backend protocols/registry impossible outside test installs.

**Recommendation:** Avoid requiring `pytest` on the runtime SLAM import path. Either make the `pytest` import local to `skip_unavailable_backend()` or move helpers behind a test-support module while preserving the public contract required by Phase 03.

### CR-02: Backend dependency version constraints are silently ignored

**File:** `src/mosaic/slam/registry.py`

`BackendDependency` exposes `version_spec`, but `BackendDescriptor.check_availability()` only checks whether the import package exists. A dependency such as `BackendDependency(package="some_backend", version_spec=">=2.0")` is reported available even if an incompatible installed version is present.

**Recommendation:** Either remove `version_spec` until it is implemented, or enforce it during availability checks. If enforcing PEP 440 specifiers, use `importlib.metadata` plus a specifier parser or deliberately reject unsupported specs.

## Warnings

### WR-01: `AvailabilityResult` allows contradictory available-with-missing-requirements states

**File:** `src/mosaic/slam/registry.py`

`AvailabilityResult.__post_init__()` rejects `available=False` without missing requirements, but does not reject `available=True` with `missing_requirements` or install hints. `skip_unavailable_backend()` trusts `available` first, so malformed availability results can bypass skips.

**Recommendation:** Validate both directions: unavailable results need at least one missing requirement, and available results must not include missing requirements.

### WR-02: `BackendRegistry.create()` does not guard against unavailable registered backends

**File:** `src/mosaic/slam/registry.py`

`BackendRegistry.create()` ignores availability and calls the backend factory unconditionally. For optional backends, callers can accidentally instantiate unavailable backends and get arbitrary factory/import errors instead of deterministic registry-level missing-requirement diagnostics.

**Recommendation:** Consider checking `descriptor.check_availability()` inside `create()` before invoking the factory, or document that `create()` assumes callers checked availability first.

## Info

No info-level findings.
