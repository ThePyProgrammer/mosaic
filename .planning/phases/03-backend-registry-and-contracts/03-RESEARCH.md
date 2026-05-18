# Phase 3: Backend Registry and Contracts - Research

**Researched:** 2026-05-18
**Domain:** Pure-Python SLAM backend registry, availability checks, and reusable pytest lifecycle contracts
**Confidence:** HIGH

## User Constraints (from CONTEXT.md)

### Locked Decisions

#### Registry Shape
- **D-01:** Use a factory-based backend registry. Registered entries create fresh `SplatSlamBackend` instances so benchmarks and contract tests do not share mutable backend state.
- **D-02:** Reject duplicate backend names with `ValueError`, matching the existing `PlatformRegistry` duplicate-handling style.
- **D-03:** Provide a default backend registry containing only the deterministic built-in backend. Do not include metadata-only placeholders for future real backends.
- **D-04:** The primary retrieval API should be `create(name)`, which looks up a registered backend and returns a fresh backend instance.

#### Metadata Fields
- **D-05:** Keep static backend metadata separate from runtime behavior capabilities. Add a descriptor-style object for registry metadata such as name, version, dependencies, factory, and availability behavior; keep `BackendCapabilities` focused on runtime capability flags.
- **D-06:** Model dependency requirements as optional Python package names/version specs plus a human-readable install hint. Do not build a full CUDA/device/binary/environment model in this phase.
- **D-07:** Keep backend parameter metadata JSON-ready and lightweight using immutable mappings of scalar values such as `bool | int | float | str`, consistent with current `MetricValue` and benchmark artifact conventions.
- **D-08:** Represent out-of-process support with a boolean metadata/capability flag. This phase records the boundary but does not implement process adapters.

#### Availability Checks
- **D-09:** Use declarative, lightweight availability probes carried by the backend descriptor. Probes must return an availability result without constructing the backend or importing heavy/native backend modules.
- **D-10:** Availability results must include an available/unavailable status plus machine-readable missing requirements and human-readable diagnostics/install hints.
- **D-11:** Availability checks are on-demand only. Registry listing and registration should remain cheap and side-effect free.
- **D-12:** The deterministic built-in backend should have an explicit always-available availability result with no missing requirements.

#### Contract Tests
- **D-13:** Expose reusable pytest helper/assertion functions for backend lifecycle contracts rather than a Mosaic pytest plugin.
- **D-14:** Contract helpers must cover the roadmap lifecycle set: reset, process, snapshot, lost tracking, not-initialized behavior, diagnostics, deterministic replay, and availability gating.
- **D-15:** Contract parametrization should check availability first and skip unavailable optional backends with the availability diagnostic as the skip reason.
- **D-16:** Contract tests should reuse the existing synthetic deterministic multi-view sequence/scenario so every backend sees comparable observations.

### Claude's Discretion
No implementation areas were explicitly delegated to Claude discretion. Downstream agents should follow the decisions above.

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope.

## Project Constraints (from CLAUDE.md)

- Mosaic is a typed, headless Python library for 3D Gaussian Splatting SLAM over multi-view moving cameras, with pure-Python contracts for frames, poses, cameras, observations, splat maps, backend lifecycles, platform camera rigs, evaluation, fusion, and agent-facing posterior APIs. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- The core value is stable typed representation contracts that let SLAM backends, evaluation tools, platform rigs, and posterior APIs evolve independently without coupling the library to one robot, simulator, LLM provider, or CUDA-heavy backend. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Use Python 3.12+, `uv`, pure-Python foundation modules, and `pytest`; keep the core importable without CUDA/native dependencies. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Real 3DGS/CUDA/research backends must stay behind protocols, registries, optional dependencies, and eventual isolation boundaries. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Real backend work waits until deterministic artifacts and regression gates exist. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Keep agent APIs bounded, typed, evidence/provenance-aware, and provider-free; do not expose raw full splat maps or provider-specific prompts. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Use a `src/` layout, snake_case module names/functions, PascalCase public classes, uppercase `StrEnum` members with lower-case values, package-root `__init__.py` export surfaces, and explicit `__all__` lists. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Use package imports rooted at `mosaic`, not relative imports. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Validate dataclass invariants in `__post_init__()` and raise `ValueError` with domain-specific messages; use `KeyError` for missing registry/lookup entries. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Prefer typed diagnostics mappings over logging side effects and avoid `print()` in library code. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Return immutable dataclasses or tuples, freeze metadata/diagnostics mappings internally, and avoid mutating caller-owned objects. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Use `uv run pytest ... -q` as the local quality gate until broader lint/type tooling exists. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- No project skill `SKILL.md` files were found under `.claude/skills/` or `.agents/skills/`. [VERIFIED: shell `ls`]

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| BACK-01 | SLAM backends can be described by registry metadata including name, version, capabilities, parameters, dependency requirements, and whether they run out of process. | Use a frozen descriptor dataclass containing static metadata, existing `BackendCapabilities`, immutable JSON-ready parameter metadata, dependency descriptors, and a factory. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md][VERIFIED: codebase]
| BACK-02 | Backend availability checks can report unavailable optional dependencies without importing heavy CUDA/native packages into core modules. | Use descriptor-owned declarative probes based on package names and `importlib.util.find_spec()`; do not call descriptor factories during availability checks. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md][CITED: https://docs.python.org/3/library/importlib.html#importlib.util.find_spec]
| BACK-03 | Backend contract tests can be parametrized across any registered backend implementation. | Expose helper/assertion functions callable from normal pytest tests; use pytest parametrization/skip patterns rather than a plugin. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md][CITED: https://docs.pytest.org/en/stable/example/parametrize.html]
| BACK-04 | Lifecycle contract coverage includes reset, process, snapshot, lost tracking, not-initialized behavior, diagnostics, and deterministic replay. | Reuse `synthetic_forward_sequence()` and existing backend lifecycle tests, then add helper coverage for edge state behavior and deterministic repeated replay. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md][VERIFIED: codebase]

## Summary

Phase 3 should be planned as a pure-Python seam-hardening phase inside `src/mosaic/slam/`, not as backend integration work. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md] The existing `SplatSlamBackend` protocol already defines `name`, `capabilities`, `reset()`, `process()`, and `snapshot()`, while `DeterministicSplatBackend` is stateful and therefore must be created through a factory for every benchmark or contract-test run. [VERIFIED: codebase]

The planner should introduce three small API clusters: backend descriptor/availability value objects, a factory-based backend registry, and reusable pytest contract helpers. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md] These should extend current conventions: frozen/slotted dataclasses, explicit `__all__`, `MappingProxyType` for diagnostics/metadata, `ValueError` for duplicate registration, and `KeyError` for missing names. [VERIFIED: codebase]

**Primary recommendation:** Implement `mosaic.slam.registry` plus `mosaic.slam.contracts` with no runtime dependencies, no entry-point auto-discovery in this phase, and no CUDA/native imports in registry listing or availability paths. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md]

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|--------------|----------------|-----------|
| Backend metadata description | API / Backend library core | — | Metadata belongs to the SLAM API seam so users can inspect backend identity, capabilities, parameters, dependency hints, and process boundary without constructing a backend. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md] |
| Backend availability check | API / Backend library core | External optional package boundary | The core library should evaluate lightweight declarations and package presence, while optional CUDA/native packages remain outside import-time code paths. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md][CITED: https://docs.python.org/3/library/importlib.html#importlib.util.find_spec] |
| Backend instantiation | API / Backend library core | Backend implementation | The registry should own lookup and factory invocation; backend implementation owns runtime mutable state after creation. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md] |
| Lifecycle contract tests | Test tier | API / Backend library core | Reusable pytest helper functions should live with SLAM contracts but run from tests against any registered backend. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md][CITED: https://docs.pytest.org/en/stable/example/parametrize.html] |
| Benchmark metadata compatibility | Evaluation layer | API / Backend library core | `run_slam_benchmark()` currently reads `backend.capabilities`; registry descriptor metadata should enrich registered usage without breaking direct backend usage. [VERIFIED: codebase] |

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python standard library `dataclasses` | Python >=3.12 project target | Frozen/slotted descriptor, dependency, and availability result value objects | `frozen=True` adds read-only behavior and `slots=True` generates slot-based storage for value-style classes. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/pyproject.toml][CITED: https://docs.python.org/3/library/dataclasses.html] |
| Python standard library `types.MappingProxyType` | Python >=3.12 project target | Freeze copied metadata, diagnostics, parameters, and hints | Existing Mosaic code uses `MappingProxyType(dict(...))` for immutable public mappings in capabilities, updates, and artifacts. [VERIFIED: codebase] |
| Python standard library `typing.Protocol` | Python >=3.12 project target | Preserve pluggable backend contract shape | Existing `SplatSlamBackend` is a runtime-checkable `Protocol`; extend around it rather than replacing it. [VERIFIED: codebase] |
| Python standard library `importlib.util.find_spec` | Python >=3.12 project target | Declarative package-presence checks for optional dependencies | Official docs say it returns a spec or `None` and does not import the target module itself, with the caveat that dotted submodule checks import the parent package. [CITED: https://docs.python.org/3/library/importlib.html#importlib.util.find_spec] |
| `pytest` | >=8.4.0 declared; local command reports 9.0.2 | Contract helper tests and skip behavior for unavailable optional backends | Project dev dependencies include pytest and existing tests run under `uv run pytest`; pytest docs support parametrized cases and optional implementation skips. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/pyproject.toml][VERIFIED: shell][CITED: https://docs.pytest.org/en/stable/example/parametrize.html] |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Python standard library `importlib.metadata.entry_points` | Python >=3.12 project target | Future installed plugin discovery | Use in a later phase if Mosaic supports third-party backend auto-discovery; do not use for the Phase 3 default registry because the user locked deterministic-only default registration. [CITED: https://docs.python.org/3/library/importlib.metadata.html#entry-points][VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md] |
| Python Packaging entry points | Current packaging guide | Future explicit plugin registration mechanism | The Python Packaging User Guide lists entry points as a plugin discovery mechanism alongside naming conventions and namespace packages. [CITED: https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/] |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Manual factory registry | Entry-point auto-discovery | Entry points are standard for installed plugins, but Phase 3 explicitly requires a deterministic-only default registry and no future real backend placeholders; auto-discovery would expand scope and may load third-party objects during discovery. [CITED: https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/][VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md] |
| Descriptor-owned availability probes | Import backend module and catch `ImportError` | Importing optional backend modules risks triggering CUDA/native imports; the phase requires availability diagnostics without heavy dependency leakage. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md] |
| Helper functions | Pytest plugin | User decision D-13 rejects a plugin in favor of reusable pytest helper/assertion functions. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md] |

**Installation:**
```bash
# No new runtime packages for Phase 3.
# Use existing dev workflow:
uv run pytest -q
```

**Version verification:** `pyproject.toml` declares `pytest>=8.4.0`, and the local environment reports `pytest 9.0.2`. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/pyproject.toml][VERIFIED: shell]

## Package Legitimacy Audit

No external packages should be installed for Phase 3. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md]

| Package | Registry | Age | Downloads | Source Repo | slopcheck | Disposition |
|---------|----------|-----|-----------|-------------|-----------|-------------|
| None | — | — | — | — | — | No install required |

**Packages removed due to slopcheck [SLOP] verdict:** none. [VERIFIED: no new packages recommended]
**Packages flagged as suspicious [SUS]:** none. [VERIFIED: no new packages recommended]

## Architecture Patterns

### System Architecture Diagram

```text
User / Test / Evaluation Runner
        |
        v
BackendRegistry.names / descriptor(name) -----> BackendDescriptor metadata
        |                                      |  - name/version
        |                                      |  - BackendCapabilities
        |                                      |  - DependencyRequirement[]
        |                                      |  - parameter metadata
        |                                      |  - runs_out_of_process
        |                                      |
        |                                      v
        |                         Availability probe (on demand)
        |                                      |
        |                         importlib.util.find_spec(package_name)
        |                                      |
        |                         AvailabilityResult
        |                         - available
        |                         - missing_requirements
        |                         - diagnostics/install_hints
        |
        v
BackendRegistry.create(name)
        |
        v
Descriptor factory() creates fresh SplatSlamBackend
        |
        v
Contract helper / benchmark replay
        |
        v
reset() -> process(synthetic observations) -> snapshot() -> diagnostics/artifacts
```

### Recommended Project Structure

```text
src/mosaic/slam/
├── protocol.py          # existing SplatSlamBackend, BackendCapabilities, SplatSlamUpdate
├── fake_backend.py      # existing DeterministicSplatBackend default entry
├── registry.py          # new descriptors, dependency requirements, availability result, registry
├── contracts.py         # new reusable pytest-style lifecycle assertion helpers
└── __init__.py          # public exports for stable registry and contract APIs

tests/slam/
├── test_backend_registry.py      # registry metadata, duplicate, create, availability behavior
├── test_backend_contract.py      # existing deterministic backend tests migrated/extended through helpers
└── test_backend_contract_helpers.py # helper behavior, skip gating for unavailable descriptors
```

### Pattern 1: Descriptor Separate from Runtime Backend
**What:** Keep static registry metadata in `BackendDescriptor`; keep runtime flags and parameters in existing `BackendCapabilities`. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md]
**When to use:** Use descriptors for listing, inspection, dependency hints, availability checks, and factory creation; use backend instances only for lifecycle operations. [VERIFIED: codebase]
**Example:**
```python
# Source: project pattern from src/mosaic/slam/protocol.py and dataclasses docs
@dataclass(frozen=True, slots=True)
class BackendDescriptor:
    name: str
    version: str
    capabilities: BackendCapabilities
    dependencies: tuple[BackendDependency, ...]
    factory: Callable[[], SplatSlamBackend]

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("BackendDescriptor name must not be blank")
```

### Pattern 2: On-Demand Lightweight Availability
**What:** Availability checks should inspect declarative dependency package names and return `AvailabilityResult`; they must not call `factory()` or import the optional backend implementation. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md]
**When to use:** Use before contract tests or backend creation for optional backends. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md]
**Example:**
```python
# Source: Python docs for importlib.util.find_spec
import importlib.util

available = importlib.util.find_spec("pytest") is not None
```

### Pattern 3: Factory Registry Mirrors PlatformRegistry Error Style
**What:** Store descriptors by name, reject duplicate names with `ValueError`, sort names, and raise `KeyError` for missing backend retrieval. [VERIFIED: codebase]
**When to use:** Use for user-created registries and `default_backend_registry()`. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md]
**Example:**
```python
# Source: src/mosaic/platforms/registry.py pattern
if descriptor.name in self._descriptors:
    raise ValueError(f"Backend {descriptor.name!r} is already registered")
```

### Pattern 4: Reusable Contract Helpers, Not Plugin Hooks
**What:** Provide functions such as `assert_backend_lifecycle_contract(factory_or_descriptor)` and `assert_backend_deterministic_replay(factory_or_descriptor)`. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md]
**When to use:** Downstream backend packages import these helpers in their own pytest files and parametrize descriptors. [CITED: https://docs.pytest.org/en/stable/example/parametrize.html]
**Example:**
```python
# Source: pytest docs for optional implementation skips plus project D-15
availability = descriptor.check_availability()
if not availability.available:
    pytest.skip(availability.summary)
backend = descriptor.create()
assert_backend_lifecycle_contract(backend)
```

### Anti-Patterns to Avoid
- **Calling backend factories during `names`, `descriptor`, or `check_availability`:** This leaks mutable state or optional imports into inspection paths; use descriptor declarations instead. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md]
- **Putting dependency metadata into `BackendCapabilities` only:** The user locked static descriptor metadata separate from runtime behavior capabilities. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md]
- **Adding placeholder real backends to the default registry:** The default registry must contain only the deterministic built-in backend. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md]
- **Building CUDA/device/process-supervision models now:** Dependency requirements are limited to optional Python package names/version specs plus install hints. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md]
- **Using dotted submodule names for safe package probes unless necessary:** Official `find_spec()` docs note dotted submodule checks import the parent package, so top-level package names are safer for lightweight availability. [CITED: https://docs.python.org/3/library/importlib.html#importlib.util.find_spec]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Plugin auto-discovery | Custom module scanners or PyPI-name scraping | Defer; future use should prefer Python packaging entry points | The packaging guide lists entry points as a standard explicit plugin discovery mechanism, but Phase 3 does not need auto-discovery. [CITED: https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/] |
| Optional package presence check | Import optional CUDA/native module and catch import side effects | `importlib.util.find_spec(top_level_package)` | `find_spec()` can check whether a module spec exists without importing the target module itself; avoid dotted submodules because parents are imported. [CITED: https://docs.python.org/3/library/importlib.html#importlib.util.find_spec] |
| Test parametrization and skip behavior | Custom test runner or Mosaic pytest plugin | Plain pytest parametrization plus helper functions | pytest supports per-parameter IDs/marks and optional implementation skips; the user explicitly chose helpers over a plugin. [CITED: https://docs.pytest.org/en/stable/example/parametrize.html][VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md] |
| Metadata immutability | Bespoke immutable dict class | `MappingProxyType(dict(input_mapping))` | Existing Mosaic code already freezes mappings this way in capabilities, updates, and benchmark artifacts. [VERIFIED: codebase] |
| Backend lifecycle replay fixtures | New ad-hoc observation builders | `synthetic_forward_sequence()` | Phase decision D-16 requires the existing synthetic deterministic sequence/scenario for comparable observations. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md][VERIFIED: codebase] |

**Key insight:** The registry is an import-safety boundary; if planning treats it as a backend integration mechanism, it will recreate the exact CUDA/native dependency leakage the phase exists to prevent. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]

## Common Pitfalls

### Pitfall 1: Factory Invocation During Inspection
**What goes wrong:** Listing or inspecting backends constructs `DeterministicSplatBackend` or future heavy backends. [ASSUMED]
**Why it happens:** A registry stores backend instances instead of descriptor/factory pairs. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md]
**How to avoid:** Store immutable descriptors and call factories only in `create(name)`. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md]
**Warning signs:** Tests need to reset registry-held instances between runs or availability checks mutate backend state. [ASSUMED]

### Pitfall 2: Optional Dependency Probe Imports Parent Packages
**What goes wrong:** A supposedly safe probe imports a heavy parent package because the probe name is dotted. [CITED: https://docs.python.org/3/library/importlib.html#importlib.util.find_spec]
**Why it happens:** Official docs state `find_spec()` imports parent modules for submodule names containing dots. [CITED: https://docs.python.org/3/library/importlib.html#importlib.util.find_spec]
**How to avoid:** Store top-level package probes such as `torch` or `gsplat` rather than `torch.cuda` or backend-private submodules. [ASSUMED]
**Warning signs:** Availability tests are slow or fail on machines without GPU drivers even though no backend was created. [ASSUMED]

### Pitfall 3: Contract Helpers Accidentally Only Test the Fake Backend
**What goes wrong:** Helpers embed assumptions about deterministic splat centers or exact fake-backend provenance. [ASSUMED]
**Why it happens:** Current tests assert deterministic backend internals such as splat centers `(0.0, 0.0, 1.0)` and `(1.0, 0.0, 1.0)`. [VERIFIED: codebase]
**How to avoid:** Split generic contract assertions from fake-backend-specific assertions; generic helpers should check lifecycle invariants, not fake map geometry. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md]
**Warning signs:** A valid backend that produces different splat geometry fails the shared contract helper. [ASSUMED]

### Pitfall 4: Confusing `runs_out_of_process` Metadata with Process Isolation
**What goes wrong:** Planner schedules process adapters or supervision behavior. [ASSUMED]
**Why it happens:** The metadata flag sounds like runtime orchestration. [ASSUMED]
**How to avoid:** Phase 3 only records a boolean boundary; actual out-of-process adapters are deferred. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md]
**Warning signs:** Tasks mention multiprocessing, subprocess supervision, IPC, or CUDA worker management. [ASSUMED]

### Pitfall 5: Breaking Existing Benchmark Metadata
**What goes wrong:** `run_slam_benchmark()` only accepts descriptors or stops accepting direct `SplatSlamBackend` instances. [ASSUMED]
**Why it happens:** Registry metadata is added by replacing existing backend metadata extraction instead of extending it. [ASSUMED]
**How to avoid:** Preserve direct backend usage and, if adding descriptor-aware metadata, add a separate path or optional argument without breaking current tests. [VERIFIED: codebase]
**Warning signs:** Existing `tests/evaluation/test_runner.py` expectations fail. [VERIFIED: codebase]

## Code Examples

Verified patterns from official/project sources:

### Availability Probe with Top-Level Package Name
```python
# Source: https://docs.python.org/3/library/importlib.html#importlib.util.find_spec
import importlib.util

if importlib.util.find_spec("pytest") is None:
    missing = "pytest"
```

### Pytest Skip for Unavailable Optional Backend
```python
# Source: https://docs.pytest.org/en/stable/example/parametrize.html
availability = descriptor.check_availability()
if not availability.available:
    pytest.skip(availability.summary)
```

### Frozen Mapping Pattern
```python
# Source: src/mosaic/slam/protocol.py and src/mosaic/evaluation/runner.py
from types import MappingProxyType

object.__setattr__(self, "diagnostics", MappingProxyType(dict(self.diagnostics)))
```

### Registry Duplicate Handling Pattern
```python
# Source: src/mosaic/platforms/registry.py
if platform.name in self._platforms:
    raise ValueError(f"Platform {platform.name!r} is already registered")
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Importing backend implementations directly in user code | Registering descriptors/factories behind a typed protocol seam | Locked for Phase 3 on 2026-05-18 | Keeps core importable without CUDA/native packages and gives evaluation/tests a stable creation path. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md] |
| Pytest plugin for backend contracts | Reusable helper/assertion functions | Locked for Phase 3 on 2026-05-18 | Avoids plugin packaging overhead and lets downstream backends import helpers directly. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md] |
| Instance registry | Factory-based registry | Locked for Phase 3 on 2026-05-18 | Avoids shared mutable backend state across tests and benchmarks. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md][VERIFIED: codebase] |

**Deprecated/outdated:**
- Metadata-only placeholders for future real backends are out of scope; the default registry contains only the deterministic backend. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md]
- Required CUDA/PyTorch/OpenCV dependencies are out of scope for v1 core. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Future real backend package probes are likely to use top-level names such as `torch` or `gsplat`. | Common Pitfalls | Planner may choose probe names that import heavy parent packages or miss the intended dependency. |
| A2 | Valid future backends may produce splat geometry different from the deterministic fake backend. | Common Pitfalls | Contract helpers could overfit fake-backend geometry and reject real implementations. |
| A3 | Process supervision tasks would be scope creep for this phase. | Common Pitfalls | Planner could over-schedule IPC/subprocess work despite locked phase boundaries. |
| A4 | Existing benchmark API should remain direct-backend-compatible while descriptor metadata is added separately or optionally. | Common Pitfalls | Planner could unnecessarily break existing evaluation tests. |

## Open Questions (RESOLVED)

1. **RESOLVED: Descriptor metadata should stay JSON-ready in Phase 3, not enter Phase 2 artifact envelopes.**
   - Decision: Implement descriptor metadata as immutable fields and lightweight JSON-ready extraction only where tests need BACK-01 evidence; do not add a new artifact schema or envelope round-trip in this phase.
   - Why: Phase 3 requires inspectable backend metadata, while the CONTEXT.md scope does not require persisted descriptor artifacts. Adding artifact serialization would couple the registry seam to evaluation artifact plumbing before a concrete consumer exists.
   - Plan impact: Plan 03-01 owns descriptor metadata and registry inspection tests; Plan 03-03 may assert benchmark compatibility without changing artifact envelope schemas.

2. **RESOLVED: Backend creation should remain a `BackendRegistry.create(name)` responsibility.**
   - Decision: Keep registry `create(name)` as the public creation API. `BackendDescriptor` may carry the factory and expose availability/metadata, but the plan should not advertise descriptor-level `create()` as the primary public path.
   - Why: D-04 explicitly names registry lookup and creation as the primary retrieval API, and factory invocation during inspection is the main import-safety pitfall.
   - Plan impact: Plan 03-01 must test that `BackendRegistry.create("deterministic")` returns fresh backend instances and that listing/descriptor/availability calls do not invoke factories.

3. **RESOLVED: Lost tracking and not-initialized lifecycle behavior should be covered with test-only stubs.**
   - Decision: Add small test-only stub backends for `TrackingState.LOST` and `TrackingState.NOT_INITIALIZED` contract-helper coverage; do not alter `DeterministicSplatBackend` to manufacture those states.
   - Why: The deterministic backend is the stable replay baseline and currently always tracks. Generic contract helpers should verify lifecycle invariants without overfitting deterministic splat geometry or changing the fake backend's normal behavior.
   - Plan impact: Plan 03-02 owns reusable helper tests for lost/not-initialized stubs, while Plan 03-03 applies the shared helpers to the deterministic backend replay path.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| Python | Package/runtime and availability probe implementation | ✓ | `python3 --version` reports 3.14.4 locally; project requires >=3.12 | Use `uv run python` if local interpreter selection matters. [VERIFIED: shell][VERIFIED: /home/prannayag/pragnition/robotics/mosaic/pyproject.toml] |
| uv | Test workflow | ✓ | 0.10.10 | Use direct `python -m pytest` only for diagnosis; project workflow should remain `uv run pytest`. [VERIFIED: shell][VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md] |
| pytest | Contract tests | ✓ | 9.0.2 locally; `pyproject.toml` declares `pytest>=8.4.0` | None needed. [VERIFIED: shell][VERIFIED: /home/prannayag/pragnition/robotics/mosaic/pyproject.toml] |
| CUDA/native backend packages | Real backend integration | ✗ / not required | — | Not needed; real backend integration is out of v1 scope. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md] |

**Missing dependencies with no fallback:** none for Phase 3. [VERIFIED: no new external dependencies recommended]

**Missing dependencies with fallback:** CUDA/native backend packages are intentionally absent and not required for this phase. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md]

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest, declared `>=8.4.0`; local `pytest --version` reports 9.0.2. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/pyproject.toml][VERIFIED: shell] |
| Config file | `/home/prannayag/pragnition/robotics/mosaic/pyproject.toml` with `testpaths = ["tests"]` and `pythonpath = ["src"]`. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/pyproject.toml] |
| Quick run command | `uv run pytest -q tests/slam/test_backend_contract.py tests/evaluation/test_runner.py tests/artifacts/test_slam_and_evaluation_artifacts.py` [VERIFIED: shell, 17 passed] |
| Full suite command | `uv run pytest -q` [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md] |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|--------------|
| BACK-01 | Inspect backend descriptor metadata: name, version, capabilities, parameters, dependencies, out-of-process flag | unit | `uv run pytest -q tests/slam/test_backend_registry.py -q` | ❌ Wave 0 |
| BACK-02 | Availability checks report missing optional dependencies without constructing backend factories | unit | `uv run pytest -q tests/slam/test_backend_registry.py -q` | ❌ Wave 0 |
| BACK-03 | Contract helpers can be parametrized across registered backend descriptors and skip unavailable backends | unit/integration | `uv run pytest -q tests/slam/test_backend_contract_helpers.py -q` | ❌ Wave 0 |
| BACK-04 | Lifecycle helpers cover reset, process, snapshot, lost tracking, not-initialized behavior, diagnostics, deterministic replay | unit/integration | `uv run pytest -q tests/slam/test_backend_contract.py tests/slam/test_backend_contract_helpers.py -q` | `tests/slam/test_backend_contract.py` exists; helper coverage needs Wave 0 expansion. [VERIFIED: codebase] |

### Sampling Rate
- **Per task commit:** `uv run pytest -q tests/slam/test_backend_contract.py tests/slam/test_backend_registry.py tests/slam/test_backend_contract_helpers.py` [ASSUMED]
- **Per wave merge:** `uv run pytest -q` [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- **Phase gate:** Full suite green before `/gsd:verify-work`. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/config.json]

### Wave 0 Gaps
- [ ] `tests/slam/test_backend_registry.py` — covers BACK-01 and BACK-02. [VERIFIED: file absent from test listing]
- [ ] `tests/slam/test_backend_contract_helpers.py` — covers BACK-03 and helper-specific BACK-04 behavior. [VERIFIED: file absent from test listing]
- [ ] Extend `tests/slam/test_backend_contract.py` or migrate assertions through helpers — covers BACK-04 for deterministic backend. [VERIFIED: codebase]
- [ ] Add small test-only stub backends for lost tracking and not-initialized update behavior if the deterministic backend remains always-tracking. [ASSUMED]

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | No authentication or user identity is introduced in this phase. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md] |
| V3 Session Management | no | No sessions are introduced in this phase. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md] |
| V4 Access Control | no | No authorization boundary is introduced in this phase. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md] |
| V5 Input Validation | yes | Validate descriptor names, versions, dependency names, duplicate registrations, blank hints, and JSON-ready metadata scalar values using dataclass invariants and registry errors. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md] |
| V6 Cryptography | no | No cryptography, secret storage, or token handling is introduced in this phase. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md] |

### Known Threat Patterns for Pure-Python Backend Registry

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Import-time execution of untrusted or heavy optional backend code during listing/availability | Elevation of Privilege / Denial of Service | Do not auto-import backend modules; use declarative descriptors and top-level `find_spec()` probes only. [CITED: https://docs.python.org/3/library/importlib.html#importlib.util.find_spec][VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md] |
| Backend name collision overriding a trusted implementation | Spoofing / Tampering | Reject duplicate backend names with `ValueError`. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md] |
| Mutable metadata changes after registration | Tampering | Use frozen dataclasses, tuples, and mapping proxies for descriptor/availability data. [CITED: https://docs.python.org/3/library/dataclasses.html][VERIFIED: codebase] |
| Misleading availability diagnostics | Repudiation / Information integrity | Return machine-readable missing requirement names plus human-readable install hints; test unavailable paths. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md] |

## Sources

### Primary (HIGH confidence)
- `/home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md` — locked decisions D-01 through D-16, phase boundary, canonical refs, integration points. [VERIFIED: file read]
- `/home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md` — BACK-01 through BACK-04 and out-of-scope constraints. [VERIFIED: file read]
- `/home/prannayag/pragnition/robotics/mosaic/.planning/ROADMAP.md` — Phase 3 goal, dependency on Phase 2, success criteria, current suite context. [VERIFIED: file read]
- `/home/prannayag/pragnition/robotics/mosaic/CLAUDE.md` — project constraints, code style, module design, CI-like checks. [VERIFIED: file read]
- `/home/prannayag/pragnition/robotics/mosaic/src/mosaic/slam/protocol.py` — current backend protocol and capability/update contracts. [VERIFIED: file read]
- `/home/prannayag/pragnition/robotics/mosaic/src/mosaic/slam/fake_backend.py` — deterministic backend behavior and mutable state. [VERIFIED: file read]
- `/home/prannayag/pragnition/robotics/mosaic/src/mosaic/platforms/registry.py` — duplicate rejection and sorted names precedent. [VERIFIED: file read]
- `/home/prannayag/pragnition/robotics/mosaic/src/mosaic/evaluation/scenarios.py` — deterministic synthetic replay source. [VERIFIED: file read]
- `/home/prannayag/pragnition/robotics/mosaic/src/mosaic/evaluation/runner.py` — current benchmark metadata extraction and artifact mapping conventions. [VERIFIED: file read]
- `/home/prannayag/pragnition/robotics/mosaic/pyproject.toml` — Python requirement, pytest dependency, pytest config. [VERIFIED: file read]

### Secondary (MEDIUM confidence)
- `https://docs.python.org/3/library/importlib.html#importlib.util.find_spec` — official `find_spec()` behavior and dotted submodule parent-import caveat. [CITED: official docs]
- `https://docs.pytest.org/en/stable/example/parametrize.html` — official pytest parametrization and optional implementation skip patterns. [CITED: official docs]
- `https://docs.python.org/3/library/dataclasses.html` — official frozen/slotted dataclass behavior. [CITED: official docs]
- `https://docs.python.org/3/library/importlib.metadata.html#entry-points` — official entry point discovery API for future plugin discovery. [CITED: official docs]
- `https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/` — Python Packaging User Guide plugin discovery approaches. [CITED: official docs]

### Tertiary (LOW confidence)
- Assumptions about future real backend probe package names, descriptor convenience methods, and stub strategy for lost/not-initialized behavior. [ASSUMED]

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — no new packages are required; stack is the existing Python standard library plus declared pytest, verified in code and environment. [VERIFIED: codebase][VERIFIED: shell]
- Architecture: HIGH — user decisions tightly constrain registry shape, descriptor separation, availability checks, and contract-helper approach. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/03-backend-registry-and-contracts/03-CONTEXT.md]
- Pitfalls: MEDIUM — import-safety pitfalls are officially documented for `find_spec()`, while future-backend overfitting risks are inferred from current fake-backend tests. [CITED: https://docs.python.org/3/library/importlib.html#importlib.util.find_spec][ASSUMED]

**Research date:** 2026-05-18
**Valid until:** 2026-06-17 for pure-Python API planning; re-check pytest/importlib docs if changing plugin or packaging strategy. [ASSUMED]
