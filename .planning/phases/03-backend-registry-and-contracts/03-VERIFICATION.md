---
phase: 03-backend-registry-and-contracts
verified: 2026-05-19T05:46:07Z
status: gaps_found
score: 3/4 must-haves verified
overrides_applied: 0
gaps:
  - truth: "User can availability-check SLAM backends without importing CUDA/native dependencies into core modules."
    status: failed
    reason: "The phase's public SLAM import path now imports pytest unconditionally via mosaic.slam.__init__ -> mosaic.slam.contracts, but pytest is only a dev dependency. This violates the runtime dependency boundary even though CUDA/native packages are absent."
    artifacts:
      - path: "src/mosaic/slam/__init__.py"
        issue: "Unconditionally imports helper functions from mosaic.slam.contracts."
      - path: "src/mosaic/slam/contracts.py"
        issue: "Unconditionally imports pytest at module import time."
      - path: "pyproject.toml"
        issue: "pytest is declared only in dependency-groups.dev, not runtime dependencies."
    missing:
      - "Move pytest import inside skip_unavailable_backend(), isolate pytest helpers from runtime import paths, or otherwise keep import mosaic.slam usable without dev dependencies."
---

# Phase 3: Backend Registry and Contracts Verification Report

**Phase Goal:** Users can register, inspect, availability-check, and contract-test SLAM backends without importing CUDA/native dependencies into core modules.
**Verified:** 2026-05-19T05:46:07Z
**Status:** gaps_found
**Re-verification:** No - initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | User can inspect backend metadata including name, version, capabilities, parameters, dependencies, and out-of-process status. | VERIFIED | `src/mosaic/slam/registry.py` defines `BackendDependency`, `AvailabilityResult`, `BackendDescriptor`, `BackendRegistry`, and `default_backend_registry`. `BackendDescriptor` stores name/version/capabilities/dependencies/parameters/runs_out_of_process and freezes parameters. `tests/slam/test_backend_registry.py` verifies metadata inspection without factory calls, scalar parameter acceptance/rejection, immutable parameters, and deterministic default descriptor metadata. |
| 2 | User can check backend availability and receive unavailable-dependency diagnostics without loading heavy optional packages. | FAILED | The specific CUDA/native packages are not imported by `src/mosaic/slam/registry.py`; availability uses `importlib.util.find_spec`. However, the public SLAM import path imports `pytest` unconditionally via `src/mosaic/slam/__init__.py` and `src/mosaic/slam/contracts.py`, while `pyproject.toml` declares `pytest` only under `dependency-groups.dev`. A runtime spot-check simulating no pytest failed on `import mosaic.slam` with `ImportError: simulated runtime environment without pytest`. This breaks the phase goal's dependency-boundary guarantee for normal library consumers. |
| 3 | User can run the same backend contract tests against any registered backend implementation. | VERIFIED | `src/mosaic/slam/contracts.py` provides plain helper functions `assert_backend_lifecycle_contract`, `assert_backend_deterministic_replay`, `assert_backend_state_update_contract`, and `skip_unavailable_backend`; tests import them from `mosaic.slam` and apply them to `DeterministicSplatBackend`, lost-tracking, and not-initialized test backends. |
| 4 | User can verify lifecycle behavior for reset, process, snapshot, lost tracking, not-initialized behavior, diagnostics, and deterministic replay. | VERIFIED | `assert_backend_lifecycle_contract` calls reset/process/snapshot over `synthetic_forward_sequence`; `assert_backend_state_update_contract` checks tracking/lost/not-initialized pose rules and scalar diagnostics; `assert_backend_deterministic_replay` compares state, update lengths, diagnostics, and final snapshot length across two fresh backends. Targeted tests passed: `uv run pytest -q tests/slam/test_backend_registry.py tests/slam/test_backend_contract_helpers.py tests/slam/test_backend_contract.py tests/evaluation/test_runner.py` -> 26 passed. |

**Score:** 3/4 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `src/mosaic/slam/registry.py` | BackendDependency, AvailabilityResult, BackendDescriptor, BackendRegistry, default_backend_registry | VERIFIED | Exists and is substantive. `gsd-sdk query verify.artifacts` passed. Registry file imports `importlib.util`, deterministic backend, and protocol types; no `torch`, `gsplat`, `cuda`, `cv2`, or `open3d` imports found. |
| `src/mosaic/slam/contracts.py` | Reusable pytest helper/assertion functions for backend lifecycle contracts | WARNING | Exists, substantive, and wired to tests and `mosaic.slam`. It is also the source of the blocking runtime dependency leak because it imports `pytest` at module import time. |
| `src/mosaic/slam/__init__.py` | Public SLAM exports for registry APIs and contract helpers | WARNING | Exports registry and helper symbols, but imports `mosaic.slam.contracts` unconditionally, making `import mosaic.slam` require dev-only pytest. |
| `tests/slam/test_backend_registry.py` | Registry and availability coverage | VERIFIED | Exists and substantive; covers descriptor metadata, scalar parameters, missing dependency diagnostics, duplicate/missing registry behavior, factory side-effect isolation, and deterministic default registry. |
| `tests/slam/test_backend_contract_helpers.py` | Helper, availability skip, and state edge-case coverage | VERIFIED | Exists and substantive; defines lost/not-initialized backends and verifies helper imports, skip reason, lifecycle/replay, and state update edge cases. |
| `tests/slam/test_backend_contract.py` | Built-in deterministic backend coverage through shared helpers plus fake-specific assertions | VERIFIED | Uses `default_backend_registry().create("deterministic-splat")` for shared lifecycle and replay helpers while keeping deterministic geometry assertions local. |
| `tests/evaluation/test_runner.py` | Direct benchmark metadata compatibility coverage | VERIFIED | Tests direct `DeterministicSplatBackend()` benchmark metadata including capability flags, `runs_out_of_process`, parameter metadata, and JSON serialization. |
| `src/mosaic/evaluation/runner.py` | Direct SplatSlamBackend benchmark metadata extraction | VERIFIED | `run_slam_benchmark(scenario, backend)` signature remains direct-backend-based; `_backend_metadata()` reads `backend.capabilities` and emits JSON-ready fields. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `src/mosaic/slam/registry.py` | `mosaic.slam.fake_backend.DeterministicSplatBackend` | `default_backend_registry` factory | WIRED | `default_backend_registry()` registers a deterministic descriptor with factory `DeterministicSplatBackend`. |
| `src/mosaic/slam/registry.py` | `importlib.util.find_spec` | declarative top-level package probes | WIRED | `BackendDescriptor.check_availability()` calls `importlib.util.find_spec(dependency.package)`. |
| `src/mosaic/slam/__init__.py` | `src/mosaic/slam/registry.py` | explicit imports and `__all__` | WIRED | Registry symbols are imported and exported. |
| `src/mosaic/slam/contracts.py` | `src/mosaic/evaluation/scenarios.py` | `synthetic_forward_sequence(frame_count=...)` | WIRED | Lifecycle/state/replay helpers call `synthetic_forward_sequence`. |
| `src/mosaic/slam/contracts.py` | `src/mosaic/slam/registry.py` | BackendDescriptor availability gate | WIRED | `skip_unavailable_backend(descriptor)` calls `descriptor.check_availability()`. |
| `tests/slam/test_backend_contract_helpers.py` | `src/mosaic/slam/contracts.py` | helper import and execution | WIRED | Tests import helper names from `mosaic.slam` and execute them. |
| `tests/slam/test_backend_contract.py` | `src/mosaic/slam/contracts.py` | shared helper calls against registry-created backend | WIRED | Tests call lifecycle/replay helpers with `_registered_deterministic_backend`. |
| `tests/evaluation/test_runner.py` | `src/mosaic/evaluation/runner.py` | direct benchmark metadata extraction | WIRED | Test calls `run_slam_benchmark()` with direct `DeterministicSplatBackend`. |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| `BackendDescriptor.check_availability()` | `AvailabilityResult.missing_requirements`, `diagnostics`, `install_hints` | Declarative `BackendDependency` tuple and `importlib.util.find_spec()` | Yes for presence/absence of top-level packages; version constraints are stored but not enforced. | FLOWING_WITH_WARNING |
| `BackendRegistry.create()` | Created backend instance | Registered descriptor `factory` callable | Yes; tests prove two calls return distinct deterministic backend instances. | FLOWING |
| `assert_backend_lifecycle_contract()` | Backend updates and snapshots | Fresh backend factory plus `synthetic_forward_sequence(frame_count)` | Yes; processes scenario observations and validates update timestamps, map updates, diagnostics, and reset/snapshot behavior. | FLOWING |
| `run_slam_benchmark()` | `BenchmarkArtifact.backend_metadata` | Direct backend instance `name` and `capabilities` | Yes; `_backend_metadata()` copies capability flags and parameter values, and tests assert JSON serialization. | FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Targeted Phase 3 tests pass | `uv run pytest -q tests/slam/test_backend_registry.py tests/slam/test_backend_contract_helpers.py tests/slam/test_backend_contract.py tests/evaluation/test_runner.py` | `26 passed in 0.13s` | PASS |
| Public SLAM import remains usable without dev-only pytest | `PYTHONPATH=/home/prannayag/pragnition/robotics/mosaic/src python - <<'PY' ... guarded import raises on pytest ... import mosaic.slam ... PY` | `ImportError: simulated runtime environment without pytest` | FAIL |
| `BackendDependency.version_spec` affects availability | Constructed descriptor with fake installed package and `version_spec='>=999.0'`; checked `check_availability()` | `available=True; missing=(); diagnostics={}` | WARNING |

### Probe Execution

| Probe | Command | Result | Status |
|-------|---------|--------|--------|
| Conventional phase probes | `find /home/prannayag/pragnition/robotics/mosaic/scripts -path '*/tests/probe-*.sh' -type f` | No probe scripts found. | SKIP |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| BACK-01 | 03-01, 03-03 | SLAM backends can be described by registry metadata including name, version, capabilities, parameters, dependency requirements, and whether they run out of process. | SATISFIED | `BackendDescriptor` includes all listed fields; tests assert deterministic descriptor metadata and benchmark metadata compatibility. |
| BACK-02 | 03-01 | Backend availability checks can report unavailable optional dependencies without importing heavy CUDA/native packages into core modules. | BLOCKED | Availability checks report missing packages and no CUDA/native imports were found, but the public SLAM import path requires dev-only `pytest`; runtime dependency boundary is not clean. |
| BACK-03 | 03-01, 03-02, 03-03 | Backend contract tests can be parametrized across any registered backend implementation. | SATISFIED | Shared helper functions accept factories/backends/descriptors; deterministic backend tests instantiate through `default_backend_registry().create("deterministic-splat")`; lost/not-initialized stubs exercise state helpers. |
| BACK-04 | 03-02, 03-03 | Lifecycle contract coverage includes reset, process, snapshot, lost tracking, not-initialized behavior, diagnostics, and deterministic replay. | SATISFIED | `contracts.py` implements lifecycle/state/replay helpers; tests cover reset/process/snapshot, lost/not-initialized state stubs, scalar diagnostics, and deterministic replay. |

No orphaned Phase 3 requirement IDs were found in `.planning/REQUIREMENTS.md`; BACK-01 through BACK-04 are all declared in plan frontmatter and accounted for above.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `src/mosaic/slam/contracts.py` | 5 | `import pytest` at module import time | BLOCKER | Because `src/mosaic/slam/__init__.py` imports `contracts.py` unconditionally and `pytest` is dev-only, runtime `import mosaic.slam` fails without dev dependencies. This violates the phase dependency-boundary goal. |
| `src/mosaic/slam/registry.py` | 16, 69-82 | `version_spec` stored but not checked | WARNING | Descriptor metadata includes version constraints, but availability only checks package presence. A fake installed package with `version_spec='>=999.0'` still reports `available=True`. This is an advisory correctness gap unless the project intentionally treats version constraints as metadata only. |
| `src/mosaic/slam/registry.py` | 37-38 | `AvailabilityResult(available=True, missing_requirements=...)` not rejected | WARNING | Matches the review advisory: contradictory availability states are not validated. Not blocking the roadmap truth because current `check_availability()` does not generate that state. |
| `src/mosaic/slam/registry.py` | 103-104 | `BackendRegistry.create()` ignores availability | WARNING | Optional backends can be instantiated without a registry-level availability gate if callers skip `availability()`/`skip_unavailable_backend()`. Not blocking because plan requires separate availability checks and helper gating, not create-time gating. |

### Human Verification Required

None.

### Gaps Summary

Phase 3 mostly landed substantive registry metadata, availability diagnostics, shared lifecycle helpers, deterministic registry-created backend tests, and benchmark compatibility coverage. The blocking issue is not CUDA/native import leakage specifically; it is a runtime dependency-boundary leak introduced by exporting pytest helper functions through `mosaic.slam`. Since `pytest` is dev-only in `pyproject.toml`, a normal library consumer without dev dependencies cannot import `mosaic.slam`, which undermines the phase goal's promise that users can inspect/check/register backends through core public modules without optional dependency leakage.

The code review also identified version-spec and availability-state semantic issues. I verified that version constraints are indeed ignored by `check_availability()`. I am keeping that as a warning rather than a blocker because the roadmap requirement says metadata includes dependency requirements and availability reports unavailable optional dependencies; it does not explicitly require version-spec enforcement in Phase 3. The runtime `pytest` import failure is the blocker.

---

_Verified: 2026-05-19T05:46:07Z_
_Verifier: Claude (gsd-verifier)_
