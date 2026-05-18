# Phase 1: Merged Foundation Baseline Completion - Research

**Researched:** 2026-05-18  
**Domain:** Python 3.12 typed library baseline stabilization, public API validation, pytest/uv workflow, README documentation  
**Confidence:** HIGH

## User Constraints

No `01-CONTEXT.md` exists for this phase; user explicitly chose to continue without captured design context. Research scope is anchored on `.planning/REQUIREMENTS.md`, `.planning/STATE.md`, `.planning/ROADMAP.md`, `CLAUDE.md`, current code, docs, and tests. [VERIFIED: user prompt] [VERIFIED: codebase]

### Locked Decisions

None captured in phase context. [VERIFIED: gsd-sdk init.phase-op]

### Claude's Discretion

Planner may choose task decomposition, but must not contradict roadmap/requirements/project constraints. [VERIFIED: `.planning/ROADMAP.md`] [VERIFIED: `.planning/REQUIREMENTS.md`] [VERIFIED: `CLAUDE.md`]

### Deferred Ideas (OUT OF SCOPE)

Real 3DGS backend integration, CUDA/PyTorch/OpenCV required dependencies, LLM/LVLM provider integration, ROS nodes, Habitat/ARNA reproduction, browser UI/WebSockets/demos, occupancy-grid-first map model, and vendor-calibrated platform presets are explicitly out of scope for v1 or deferred. [VERIFIED: `.planning/REQUIREMENTS.md`]

## Summary

Phase 1 is a baseline-completion and release-facing validation phase, not a greenfield implementation phase. The main checkout already contains the merged Mosaic foundation modules under `src/mosaic/` for `core`, `datasets`, `splats`, `slam`, `platforms`, `fusion`, `evaluation`, and `agents`; `uv run pytest -q` currently reports `73 passed in 0.25s`. [VERIFIED: codebase] [VERIFIED: command]

The highest-value plan should verify and document the package as users experience it: install/sync with `uv`, import supported package surfaces, run the full test workflow, exercise initial fusion/evaluation/agent posterior APIs, and fill the empty `README.md` with scope, fake-backend boundary, commands, v1 module map, and known hardening gaps. [VERIFIED: `.planning/ROADMAP.md`] [VERIFIED: `README.md`]

**Primary recommendation:** Treat implementation as mostly landed; plan a focused validation/documentation wave that codifies the 73-test baseline, public imports, no-heavy-runtime-dependency boundary, and README user path. [VERIFIED: command] [VERIFIED: `.planning/ROADMAP.md`]

## Project Constraints (from CLAUDE.md)

- Use Python 3.12+, `uv`, pure-Python foundation modules, and `pytest`; keep core importable without CUDA/native dependencies. [VERIFIED: `CLAUDE.md`]
- Main checkout and active migration worktree may differ; use the worktree as baseline context, but commit planning artifacts in the main checkout unless explicitly working in the worktree. [VERIFIED: `CLAUDE.md`]
- Real 3DGS/CUDA/research backends must remain behind protocols, registries, optional dependencies, and eventual isolation boundaries. [VERIFIED: `CLAUDE.md`]
- Coordinate frames, pose direction, handedness, optical frame conventions, and timestamp precision must be nailed down early, but hardening is Phase 2 rather than Phase 1. [VERIFIED: `CLAUDE.md`] [VERIFIED: `.planning/ROADMAP.md`]
- Evaluation gates come before real backend integration. [VERIFIED: `CLAUDE.md`]
- Agent APIs return bounded typed outputs with evidence/provenance, not raw full splat maps or provider-specific prompts. [VERIFIED: `CLAUDE.md`]
- Use `src/` package layout, snake_case modules, PascalCase public dataclasses/protocols/enums, explicit `__all__`, package-root exports as stable public surfaces, and no wildcard imports. [VERIFIED: `CLAUDE.md`]
- Validate dataclass invariants in `__post_init__()` and raise domain-specific `ValueError`; use `KeyError` for missing registry/lookups. [VERIFIED: `CLAUDE.md`]
- Prefer immutable/frozen dataclasses, immutable tuples, copied `MappingProxyType` mappings, typed parameters, and no mutation of caller-owned objects. [VERIFIED: `CLAUDE.md`]
- Avoid `print()` in library code; prefer typed diagnostics mappings. [VERIFIED: `CLAUDE.md`]
- Local quality gate should use `uv run pytest ... -q`; no CI workflow is currently committed. [VERIFIED: `CLAUDE.md`] [VERIFIED: codebase]

<phase_requirements>

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| BASE-01 | The `splat-slam-foundation` worktree is reviewed, stabilized, and merged as the baseline Mosaic package implementation. | Main checkout contains merged source modules and recent merge history; Phase 1 should verify baseline from main, not worktree. [VERIFIED: codebase] [VERIFIED: `git log`] |
| BASE-02 | Public package exports clearly expose supported foundation APIs for core, datasets, splats, SLAM, and platforms. | Root and subpackage `__all__` surfaces exist and tests cover public API imports. [VERIFIED: codebase] |
| BASE-03 | README documents Mosaic's library-first scope, fake-backend boundary, install/test commands, and v1 module map. | `README.md` is empty; planner must add release-facing content. [VERIFIED: `README.md`] |
| BASE-04 | The test suite from the foundation worktree runs from the merged main checkout and passes under the configured project workflow. | `uv run pytest -q` reports 73 passing tests from main checkout. [VERIFIED: command] |
| FUSE-01 | Mosaic exposes a fusion protocol over immutable `SplatMap` snapshots with explicit input validation and frame compatibility checks. | `FusionInput`, `FusionResult`, `FusionStatus`, and `SplatFusionStrategy` exist; tests cover empty input, frame mismatch, tuple freezing, and read-only diagnostics. [VERIFIED: codebase] |
| FUSE-03 | A deterministic reference fusion strategy exists for tests without claiming real Gaussian optimization quality. | `ProvenancePreservingFusion` concatenates splats, preserves provenance, and reports `uncertainty_model = preserved-not-optimized`. [VERIFIED: codebase] |
| EVAL-01 | Mosaic provides deterministic synthetic multi-view scenarios that can drive the fake backend and future registered backends. | `synthetic_forward_sequence()` creates deterministic `SyntheticScenario`/`InMemorySequence` observations. [VERIFIED: codebase] |
| EVAL-03 | Benchmark runs emit stable JSON/JSONL artifacts with scenario, backend metadata, metrics, diagnostics, and failure classification. | Current `BenchmarkArtifact` emits stable JSON with scenario/backend/update_count/metrics; diagnostics and failure classification are later hardening gaps per roadmap. [VERIFIED: codebase] [VERIFIED: `.planning/ROADMAP.md`] |
| AGNT-01 | Mosaic exposes typed posterior query requests and bounded deterministic result objects over `SplatMap` snapshots. | `LocalRadiusQuery`, `SplatQueryResult`, `PosteriorSummary`, `ProvenanceSummary`, and `SplatPosteriorView` exist. [VERIFIED: codebase] |
| AGNT-03 | Agent-facing APIs are provider-free Python contracts and do not import LLM SDKs, ROS, Habitat, or robot execution dependencies. | `agents` modules import only dataclasses/math plus Mosaic types; project dependencies are empty except dev pytest. [VERIFIED: codebase] |

</phase_requirements>

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|--------------|----------------|-----------|
| Package installation/import baseline | Python package/build tier | Test tier | `pyproject.toml`, `uv.lock`, `src/mosaic`, and `py.typed` own installability/importability; tests verify user-facing imports. [VERIFIED: codebase] |
| Public API exports | Python library API tier | Tests | Root and subpackage `__init__.py` files are explicit export surfaces, and `tests/test_public_api.py` asserts representative imports. [VERIFIED: codebase] |
| Deterministic fake SLAM backend | Library backend-contract tier | Evaluation tier | `DeterministicSplatBackend` owns lightweight backend behavior behind `SplatSlamBackend`, while evaluation consumes it through protocol methods. [VERIFIED: codebase] |
| Fusion baseline | Library fusion tier | Core/splats tier | `FusionInput` validates `SplatMap` frame compatibility; `ProvenancePreservingFusion` produces a new `SplatMap` without mutating inputs. [VERIFIED: codebase] |
| Evaluation artifacts/regression gates | Library evaluation tier | Test/documentation tier | `run_slam_benchmark`, `BenchmarkArtifact`, `write_benchmark_artifact`, and `check_regression_gates` own deterministic artifact and threshold behavior. [VERIFIED: codebase] |
| Agent posterior queries | Library agent API tier | Splat snapshot tier | `SplatPosteriorView` answers bounded local/summary/provenance queries over `SplatMap`; it does not own raw map dumping or provider integration. [VERIFIED: codebase] |
| README/user understanding | Documentation tier | Library API tier | Empty README is the major remaining Phase 1 gap; docs must describe the implemented module map and boundaries. [VERIFIED: `README.md`] [VERIFIED: `.planning/ROADMAP.md`] |

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python / CPython | Project requires `>=3.12`; `uv run python --version` uses 3.12.13 | Runtime for typed pure-Python library | `StrEnum`, dataclasses, protocols, and modern typing are standard-library features used by code. [VERIFIED: `pyproject.toml`] [VERIFIED: command] [CITED: https://docs.python.org/3.14/library/enum.html#enum.StrEnum] |
| `uv` | CLI 0.10.10 | Project environment, lock, sync, and command runner | `uv run` executes commands inside the project `.venv` and keeps the project environment up to date. [VERIFIED: command] [CITED: https://docs.astral.sh/uv/concepts/projects/running-commands/] |
| `uv-build` / `uv_build` | constrained `>=0.10.10,<0.11.0`; latest matching 0.10.12, latest PyPI 0.11.14 | PEP 517 build backend | Current `pyproject.toml` uses `build-backend = "uv_build"`; keep the existing constraint unless deliberately upgrading build backend. [VERIFIED: `pyproject.toml`] [VERIFIED: PyPI] |
| Standard library `dataclasses` | Python 3.12+ | Frozen/slotted value objects | `frozen=True` emulates immutability and `slots=True` generates slots for instances. [CITED: https://docs.python.org/3/library/dataclasses.html] |
| Standard library `typing.Protocol` | Python 3.12+ | Pluggable backend/fusion/dataset interfaces | Protocols support structural subtyping; `runtime_checkable` enables simple runtime presence checks but does not validate signatures. [CITED: https://docs.python.org/3/library/typing.html#typing.Protocol] |
| Standard library `MappingProxyType` | Python 3.12+ | Read-only metadata/diagnostics snapshots | It creates a read-only proxy; code correctly wraps `dict(mapping)` first to avoid reflecting caller mutations. [CITED: https://docs.python.org/3/library/types.html#types.MappingProxyType] [VERIFIED: codebase] |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `pytest` | `uv.lock` resolves 9.0.3; `pyproject.toml` requires `>=8.4.0` | Test runner | Use for all Phase 1 verification via `uv run pytest -q`. [VERIFIED: `uv.lock`] [VERIFIED: command] [CITED: https://docs.pytest.org/en/stable/reference/customize.html] |
| Standard library `json` | Python 3.12+ | Stable benchmark artifact serialization | Use `json.dumps(..., indent=2, sort_keys=True) + "\n"`; `sort_keys=True` is useful for regression-test-stable output. [VERIFIED: codebase] [CITED: https://docs.python.org/3/library/json.html] |
| Standard library `pathlib.Path.write_text` | Python 3.12+ | Write benchmark artifact files | `Path.write_text()` opens text mode, writes, closes, and overwrites existing files. [VERIFIED: codebase] [CITED: https://docs.python.org/3/library/pathlib.html#pathlib.Path.write_text] |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Pure standard-library domain objects | `numpy`, `torch`, `opencv-python`, `open3d` | Not for Phase 1; v1 core must stay importable without CUDA/native/heavy runtime dependencies. [VERIFIED: `CLAUDE.md`] [VERIFIED: `.planning/REQUIREMENTS.md`] |
| `pytest` only | `tox`/`nox`/CI matrix | Not needed for Phase 1 because no tox/nox/CI config exists and roadmap asks for main-checkout workflow validation. [VERIFIED: codebase] [VERIFIED: `.planning/ROADMAP.md`] |
| Direct `python -m pytest` | `uv run pytest` | Use `uv run pytest` because uv docs say project commands run in the project environment and Mosaic uses `uv.lock`. [CITED: https://docs.astral.sh/uv/concepts/projects/running-commands/] [VERIFIED: codebase] |

**Installation / sync:**

```bash
uv sync
uv run pytest -q
```

`uv` automatically locks/syncs for `uv run`, and `uv sync` exact-syncs the project environment by default. [CITED: https://docs.astral.sh/uv/concepts/projects/locking-and-syncing/] [CITED: https://docs.astral.sh/uv/concepts/projects/running-commands/]

**Version verification performed:**

```bash
uv --version                         # uv 0.10.10
uv run python --version              # Python 3.12.13
uv run python -c 'import importlib.metadata as m; print(m.version("pytest"))'  # pytest 9.0.3
pip index versions pytest            # latest 9.0.3
pip index versions uv-build          # latest 0.11.14; current constraint <0.11.0
uv lock --check                      # lock resolves cleanly
```

[VERIFIED: command]

## Package Legitimacy Audit

> Required because this phase relies on external dev/build packages already declared in `pyproject.toml`/`uv.lock`. [VERIFIED: codebase]

| Package | Registry | Age | Downloads | Source Repo | slopcheck | Disposition |
|---------|----------|-----|-----------|-------------|-----------|-------------|
| `pytest` | PyPI | Established; latest 9.0.3 uploaded 2026-04-07 | PyPI JSON does not expose downloads | PyPI project metadata page | OK | Approved; use existing dev dependency. [VERIFIED: PyPI] [VERIFIED: slopcheck] |
| `uv-build` | PyPI | Established; latest 0.11.14 uploaded 2026-05-12; project constrains `<0.11.0` | PyPI JSON does not expose downloads | PyPI project metadata page | OK | Approved; keep existing `uv_build>=0.10.10,<0.11.0` unless planning a build-backend upgrade. [VERIFIED: PyPI] [VERIFIED: slopcheck] [VERIFIED: `pyproject.toml`] |

**Packages removed due to slopcheck [SLOP] verdict:** none. [VERIFIED: slopcheck]  
**Packages flagged as suspicious [SUS]:** none. [VERIFIED: slopcheck]

Note: `slopcheck install pytest uv-build` reported both packages `[OK]`, then exited nonzero because it attempted a system `pip install` in an externally managed environment. The legitimacy verdict was still visible before the install failure. [VERIFIED: command]

## Architecture Patterns

### System Architecture Diagram

```text
Developer / user
  |
  | uv sync / uv run pytest -q / import mosaic
  v
pyproject.toml + uv.lock + src layout
  |
  +--> src/mosaic/__init__.py root public API surface
  |       |
  |       +--> core: frames, timestamps, poses, cameras, observations
  |       +--> datasets: in-memory replay sequence protocol
  |       +--> splats: GaussianSplat + immutable SplatMap snapshot
  |       +--> slam: SplatSlamBackend protocol + DeterministicSplatBackend
  |       +--> platforms: camera rigs + registry + representative presets
  |       +--> fusion: FusionInput validation -> ProvenancePreservingFusion -> FusionResult
  |       +--> evaluation: SyntheticScenario -> run_slam_benchmark -> BenchmarkArtifact -> regression gates
  |       +--> agents: LocalRadiusQuery -> SplatPosteriorView -> bounded query/summary/provenance outputs
  |
  +--> tests/
          |
          +--> public import tests
          +--> invariant/validation tests
          +--> deterministic fake backend/evaluation/fusion/agent tests
```

[VERIFIED: codebase]

### Recommended Project Structure

```text
src/mosaic/
├── __init__.py          # stable root public exports and __version__
├── py.typed             # PEP 561 typed package marker
├── core/                # frames, timestamps, poses, cameras, observations
├── datasets/            # replayable multi-view sequences
├── splats/              # Gaussian primitives and SplatMap snapshots
├── slam/                # backend protocol and deterministic fake backend
├── platforms/           # camera rig types, registry, presets
├── fusion/              # fusion protocol and deterministic reference strategy
├── evaluation/          # metrics, synthetic scenarios, benchmark artifacts, regression gates
└── agents/              # provider-free posterior query contracts and SplatPosteriorView

tests/
├── test_package_import.py
├── test_public_api.py
├── core/
├── datasets/
├── splats/
├── slam/
├── platforms/
├── fusion/
├── evaluation/
└── agents/
```

[VERIFIED: codebase]

### Pattern 1: Explicit Barrel Exports

**What:** Each public package module exposes explicitly imported public symbols via `__all__`; root `mosaic` re-exports the stable user-facing foundation API. [VERIFIED: codebase]  
**When to use:** Any Phase 1 README/import validation should document imports from package surfaces (`mosaic`, `mosaic.core`, `mosaic.fusion`, etc.), not private implementation paths. [VERIFIED: `CLAUDE.md`]  
**Example:**

```python
from mosaic import FrameId, SplatMap, ProvenancePreservingFusion, SplatPosteriorView
```

[VERIFIED: codebase]

### Pattern 2: Frozen Value Objects + Defensive Mapping Copies

**What:** Public result/config objects use frozen/slotted dataclasses and convert mutable inputs into tuples or `MappingProxyType(dict(...))`. [VERIFIED: codebase]  
**When to use:** Continue this in README examples and any hardening task; do not expose mutable caller-owned diagnostics or metadata. [VERIFIED: `CLAUDE.md`]  
**Example:** `FusionResult.__post_init__()` freezes diagnostics with `MappingProxyType(dict(self.diagnostics))`. [VERIFIED: codebase] [CITED: https://docs.python.org/3/library/types.html#types.MappingProxyType]

### Pattern 3: Protocol Boundary with Deterministic Reference Implementation

**What:** Protocols define backend/fusion/dataset contracts; deterministic implementations support tests without real CUDA/native dependencies. [VERIFIED: codebase]  
**When to use:** Phase 1 should document `DeterministicSplatBackend` and `ProvenancePreservingFusion` as reference/test implementations, not production-quality Gaussian optimization. [VERIFIED: `.planning/ROADMAP.md`]  
**Example:** `SplatSlamBackend` is a `Protocol`; `DeterministicSplatBackend` implements `reset`, `process`, and `snapshot`. [VERIFIED: codebase] [CITED: https://docs.python.org/3/library/typing.html#typing.Protocol]

### Pattern 4: Stable Machine-Readable Artifacts

**What:** Benchmark artifacts use `as_dict()` and `json.dumps(..., indent=2, sort_keys=True) + "\n"` for deterministic JSON. [VERIFIED: codebase]  
**When to use:** README and tests should show benchmark artifact writing as the supported Phase 1 artifact path. [VERIFIED: codebase] [CITED: https://docs.python.org/3/library/json.html]

### Anti-Patterns to Avoid

- **Adding heavy runtime dependencies to satisfy examples:** Phase 1 must not add CUDA, PyTorch, OpenCV, ROS, Habitat, or LLM SDK dependencies. [VERIFIED: `.planning/REQUIREMENTS.md`] [VERIFIED: `CLAUDE.md`]
- **Documenting future hardening as already complete:** Coordinate/artifact hardening, richer fusion diagnostics, failure classification, and richer posterior uncertainty are later phases. [VERIFIED: `.planning/ROADMAP.md`]
- **Bypassing package surfaces:** Do not teach users to import from deep private implementation modules when public subpackage/root surfaces exist. [VERIFIED: `CLAUDE.md`] [VERIFIED: codebase]
- **Claiming real 3DGS quality:** `ProvenancePreservingFusion` concatenates/preserves splats for contract testing; it does not optimize a Gaussian scene. [VERIFIED: codebase] [VERIFIED: `.planning/ROADMAP.md`]
- **Letting README drift from tests:** README examples should be backed by current passing imports and API calls. [VERIFIED: codebase]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Test runner | Custom shell/Python harness | `uv run pytest -q` | Project already configures pytest `testpaths`/`pythonpath`; pytest supports pyproject config. [VERIFIED: `pyproject.toml`] [CITED: https://docs.pytest.org/en/stable/reference/customize.html] |
| Environment setup | Manual virtualenv instructions as primary path | `uv sync` / `uv run` | uv project commands run in the isolated project environment and keep it current. [CITED: https://docs.astral.sh/uv/concepts/projects/running-commands/] |
| Public API discovery | Dynamic import reflection in docs | Explicit `__all__` and tests | Project convention requires explicit exports and public API tests. [VERIFIED: `CLAUDE.md`] [VERIFIED: codebase] |
| Artifact JSON formatting | Ad-hoc string concatenation | `json.dumps(..., indent=2, sort_keys=True)` + newline | Standard library supports sorted-key JSON useful for regression tests. [CITED: https://docs.python.org/3/library/json.html] |
| Mutability control | Custom immutable dict/list wrappers | `tuple(...)` and `MappingProxyType(dict(...))` | Current code already uses these standard-library patterns. [VERIFIED: codebase] [CITED: https://docs.python.org/3/library/types.html#types.MappingProxyType] |
| Backend/fusion interface checks | Base-class-only coupling | `typing.Protocol` | Protocols allow structural subtyping for pluggable implementations. [CITED: https://docs.python.org/3/library/typing.html#typing.Protocol] |

**Key insight:** Phase 1 is about making the existing baseline boring, inspectable, and repeatable; custom tooling would create more surface area than the package currently needs. [VERIFIED: `.planning/ROADMAP.md`]

## Common Pitfalls

### Pitfall 1: Treating Current README as Sufficient

**What goes wrong:** Users can install/import/test the package but cannot understand scope, fake-backend boundaries, commands, module map, or known gaps. [VERIFIED: `README.md`] [VERIFIED: `.planning/ROADMAP.md`]  
**Why it happens:** Implementation landed before release-facing documentation. [VERIFIED: `.planning/STATE.md`]  
**How to avoid:** Add README sections for scope, install/test, public API map, quick examples, deferred integrations, and hardening gaps. [VERIFIED: `.planning/ROADMAP.md`]  
**Warning signs:** README remains empty or examples reference future APIs. [VERIFIED: `README.md`]

### Pitfall 2: Over-Expanding Phase 1 into Later Hardening

**What goes wrong:** Planner tries to solve coordinate semantics, backend registry metadata, richer fusion conflict diagnostics, or agent uncertainty summaries in Phase 1. [VERIFIED: `.planning/ROADMAP.md`]  
**Why it happens:** Phase 1 touches all modules, but roadmap splits hardening across Phases 2-6. [VERIFIED: `.planning/ROADMAP.md`]  
**How to avoid:** Document gaps honestly in README and tests, but defer semantic hardening to mapped later requirements. [VERIFIED: `.planning/REQUIREMENTS.md`]  
**Warning signs:** Tasks mention SEM, BACK, FUSE-02/FUSE-04, EVAL-02/EVAL-04/EVAL-05, or AGNT-02/AGNT-04 as implementation goals. [VERIFIED: `.planning/REQUIREMENTS.md`]

### Pitfall 3: Importing Heavy Optional Ecosystems

**What goes wrong:** Core importability breaks for users without CUDA/native/robot/LLM stacks. [VERIFIED: `CLAUDE.md`]  
**Why it happens:** Examples or validation code may accidentally import real backend or robot-runtime packages. [VERIFIED: `.planning/REQUIREMENTS.md`]  
**How to avoid:** Keep Phase 1 examples standard-library + Mosaic only; package runtime dependencies remain empty. [VERIFIED: `pyproject.toml`]  
**Warning signs:** `dependencies = []` changes, or README install commands add PyTorch/OpenCV/ROS/Habitat/LLM SDKs. [VERIFIED: `pyproject.toml`] [VERIFIED: `.planning/REQUIREMENTS.md`]

### Pitfall 4: Misrepresenting Evaluation Artifact Completeness

**What goes wrong:** README or acceptance criteria claim full diagnostics/failure classification even though Phase 1 artifact only contains scenario/backend/update_count/metrics. [VERIFIED: codebase]  
**Why it happens:** Requirement EVAL-03 includes richer artifact language, but roadmap explicitly lists richer metrics/failure classification as remaining gaps. [VERIFIED: `.planning/ROADMAP.md`]  
**How to avoid:** State that initial stable JSON artifact exists, while richer diagnostics/failure classification are Phase 5 hardening. [VERIFIED: `.planning/ROADMAP.md`]  
**Warning signs:** Docs call Phase 1 benchmark artifacts a complete regression/failure taxonomy. [VERIFIED: codebase]

### Pitfall 5: Forgetting Main Checkout Baseline

**What goes wrong:** Planner sends executor to the old worktree or assumes modules are missing because older `CLAUDE.md` generated sections mention pre-merge gaps. [VERIFIED: `CLAUDE.md`] [VERIFIED: codebase]  
**Why it happens:** Project instruction says main checkout and migration worktree differ, and some generated codebase sections are stale relative to merged main. [VERIFIED: `CLAUDE.md`] [VERIFIED: codebase]  
**How to avoid:** Use current main checkout source/tests as source of truth for Phase 1; treat `CLAUDE.md` stale inventory lines as constraints/history, not current file inventory. [VERIFIED: codebase]  
**Warning signs:** Plan includes creating modules that already exist. [VERIFIED: codebase]

## Code Examples

Verified patterns from current code and official docs.

### Import Public API from Root Surface

```python
from mosaic import (
    DeterministicSplatBackend,
    FrameId,
    ProvenancePreservingFusion,
    SplatMap,
    SplatPosteriorView,
    synthetic_forward_sequence,
)
```

[VERIFIED: codebase]

### Run a Synthetic Benchmark and Regression Gate

```python
from pathlib import Path

from mosaic import (
    DeterministicSplatBackend,
    FrameId,
    RegressionGate,
    check_regression_gates,
    run_slam_benchmark,
    synthetic_forward_sequence,
    write_benchmark_artifact,
)

scenario = synthetic_forward_sequence(frame_count=3)
backend = DeterministicSplatBackend(map_frame=FrameId("map"))
artifact = run_slam_benchmark(scenario, backend)
write_benchmark_artifact(artifact, Path("benchmark.json"))
results = check_regression_gates(artifact, (RegressionGate(metric_name="splat_count", minimum=3.0),))
```

[VERIFIED: codebase]

### Fuse Splat Maps with the Reference Strategy

```python
from mosaic import FrameId, FusionInput, GaussianSplat, ProvenancePreservingFusion, SplatMap

first = SplatMap(
    frame=FrameId("map"),
    splats=(GaussianSplat(center=(0.0, 0.0, 1.0), covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1), provenance="front"),),
)
second = SplatMap(
    frame=FrameId("map"),
    splats=(GaussianSplat(center=(1.0, 0.0, 1.0), covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1), provenance="rear"),),
)
result = ProvenancePreservingFusion().fuse(FusionInput(maps=(first, second)))
```

[VERIFIED: codebase]

### Query a Bounded Posterior View

```python
from mosaic import FrameId, GaussianSplat, LocalRadiusQuery, SplatMap, SplatPosteriorView

splat_map = SplatMap(
    frame=FrameId("map"),
    splats=(GaussianSplat(center=(0.0, 0.0, 0.0), covariance_upper=(0.1, 0.0, 0.0, 0.1, 0.0, 0.1), opacity=0.5, provenance="front"),),
)
view = SplatPosteriorView(splat_map)
local = view.query_local(LocalRadiusQuery(center=(0.0, 0.0, 0.0), radius=1.0))
summary = view.summary()
provenance = view.provenance()
```

[VERIFIED: codebase]

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Placeholder-only `src/mosaic/__init__.py` with no foundation modules | Merged main checkout contains `core`, `datasets`, `splats`, `slam`, `platforms`, `fusion`, `evaluation`, and `agents` modules | 2026-05-18 merge evidence in roadmap/git history | Phase 1 should validate/document, not recreate, baseline modules. [VERIFIED: `.planning/ROADMAP.md`] [VERIFIED: `git log`] [VERIFIED: codebase] |
| Empty/no lockfile noted in older generated context | `uv.lock` exists and resolves pytest 9.0.3 plus package metadata | Observed 2026-05-18 | Use current `uv.lock` as main-checkout workflow evidence. [VERIFIED: codebase] |
| Planned evaluation/agent/fusion seams only | Initial fusion, evaluation, and `SplatPosteriorView` APIs are present | Recent commits include fusion/evaluation/agent features | README should distinguish landed initial seams from later hardening. [VERIFIED: `git log`] [VERIFIED: codebase] |

**Deprecated/outdated:**

- Generated `CLAUDE.md` inventory lines saying tests/modules/lockfile are absent are stale relative to current checkout; use them only as historical context, not current file inventory. [VERIFIED: `CLAUDE.md`] [VERIFIED: codebase]
- `tool.uv.dev-dependencies` is an older uv field; current project correctly uses `[dependency-groups]`. [VERIFIED: `pyproject.toml`] [CITED: https://docs.astral.sh/uv/concepts/projects/dependencies/]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | README examples should be minimal and may use current root package exports rather than only subpackage imports. [ASSUMED] | Code Examples / Architecture Patterns | If the project wants subpackage-only docs, README examples may need adjustment. |
| A2 | No commit should be created by this research agent unless the orchestrator later runs the configured docs commit command. [ASSUMED] | Metadata | If commit_docs is strictly enforced here, uncommitted research artifacts may need a follow-up commit step. |

## Open Questions

1. **How much README example code is enough for Phase 1 versus Phase 8?**
   - What we know: Phase 1 explicitly requires README scope, fake-backend boundary, install/test commands, v1 module map, and hardening gaps. [VERIFIED: `.planning/ROADMAP.md`]
   - What's unclear: Whether Phase 1 should include a full end-to-end example; DOCS-02 later requires a minimal end-to-end example. [VERIFIED: `.planning/REQUIREMENTS.md`]
   - Recommendation: Include a short smoke example in Phase 1, but leave polished end-to-end documentation for Phase 8. [ASSUMED]

2. **Should Phase 1 update tests for README snippets?**
   - What we know: Existing tests already cover public imports, fusion, evaluation, regression, and agent posterior behavior. [VERIFIED: codebase]
   - What's unclear: Whether README examples should be doctested or simply mirrored by existing tests. [ASSUMED]
   - Recommendation: Prefer existing pytest smoke coverage plus manually runnable README snippets; avoid adding doctest infrastructure in Phase 1. [ASSUMED]

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| Python via `uv run` | Package runtime/tests | yes | 3.12.13 | Install/sync with uv if missing. [VERIFIED: command] |
| Shell `python` / `python3` | Ad-hoc local commands | yes | 3.14.4 | Use `uv run python` for project-correct Python 3.12. [VERIFIED: command] |
| `uv` CLI | Project sync/test workflow | yes | 0.10.10 | Install uv before executing Phase 1; no preferred fallback because project standardizes on uv. [VERIFIED: command] [VERIFIED: `CLAUDE.md`] |
| `pytest` in uv environment | Test workflow | yes | 9.0.3 | `uv sync` from lockfile. [VERIFIED: command] |
| `ctx7` CLI | Optional docs lookup | no | — | Official docs via WebFetch were used. [VERIFIED: command] |
| Planning graph | Optional semantic graph context | no | — | Direct code/doc inspection used. [VERIFIED: command] |

**Missing dependencies with no fallback:** none blocking Phase 1 execution, assuming `uv` remains installed. [VERIFIED: command]

**Missing dependencies with fallback:** `ctx7` and planning graph are absent; official docs and direct code inspection are sufficient for this phase. [VERIFIED: command]

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest 9.0.3 in uv project environment. [VERIFIED: command] |
| Config file | `pyproject.toml` with `testpaths = ["tests"]` and `pythonpath = ["src"]`. [VERIFIED: `pyproject.toml`] |
| Quick run command | `uv run pytest tests/test_public_api.py tests/test_package_import.py -q` [VERIFIED: codebase] |
| Full suite command | `uv run pytest -q` [VERIFIED: command] |

Pytest supports `pyproject.toml` configuration, and `testpaths` can be set as a TOML list. [CITED: https://docs.pytest.org/en/stable/reference/customize.html] Pytest docs also state that with `src` layout and no editable install, `PYTHONPATH=src` or config `pythonpath` makes `src` importable. [CITED: https://docs.pytest.org/en/stable/explanation/goodpractices.html]

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|--------------|
| BASE-01 | Main checkout package baseline exists and imports | smoke | `uv run pytest tests/test_package_import.py -q` | yes [VERIFIED: codebase] |
| BASE-02 | Root public exports expose foundation APIs | unit/smoke | `uv run pytest tests/test_public_api.py -q` | yes [VERIFIED: codebase] |
| BASE-03 | README documents scope, commands, module map, gaps | manual/doc review | `test -s README.md` plus review against checklist | no automated test yet; README currently empty [VERIFIED: `README.md`] |
| BASE-04 | Full main-checkout suite passes | suite | `uv run pytest -q` | yes; 73 passed [VERIFIED: command] |
| FUSE-01 | Fusion input validation and frame compatibility | unit | `uv run pytest tests/fusion/test_fusion_protocol.py -q` | yes [VERIFIED: codebase] |
| FUSE-03 | Deterministic reference fusion preserves provenance | unit | `uv run pytest tests/fusion/test_strategies.py -q` | yes [VERIFIED: codebase] |
| EVAL-01 | Synthetic scenario drives fake backend | unit/integration | `uv run pytest tests/evaluation/test_scenarios.py tests/evaluation/test_runner.py -q` | yes [VERIFIED: codebase] |
| EVAL-03 | Benchmark artifact JSON and regression gates | unit | `uv run pytest tests/evaluation/test_runner.py tests/evaluation/test_regression.py -q` | yes [VERIFIED: codebase] |
| AGNT-01 | Typed posterior query/result objects | unit | `uv run pytest tests/agents/test_queries.py tests/agents/test_splat_posterior.py -q` | yes [VERIFIED: codebase] |
| AGNT-03 | Provider-free agent API imports | smoke/code review | `uv run pytest tests/agents -q` plus dependency review of `pyproject.toml` | yes [VERIFIED: codebase] |

### Sampling Rate

- **Per task commit:** `uv run pytest tests/test_public_api.py tests/test_package_import.py -q` plus targeted module tests changed by the task. [VERIFIED: codebase]
- **Per wave merge:** `uv run pytest -q`. [VERIFIED: command]
- **Phase gate:** Full suite must remain at or above the observed 73 passing tests before `/gsd:verify-work`. [VERIFIED: command] [VERIFIED: `.planning/ROADMAP.md`]

### Wave 0 Gaps

- [ ] `README.md` — currently empty; needs Phase 1 documentation for BASE-03. [VERIFIED: `README.md`]
- [ ] Optional README smoke validation — add only if planner wants an automated guard that README exists and includes required headings/commands. [ASSUMED]
- [ ] No framework install gap — pytest is already configured and available through uv. [VERIFIED: `pyproject.toml`] [VERIFIED: command]

## Security Domain

Security enforcement is enabled by configuration/prompt; this phase has low direct security exposure because Mosaic is a headless pure-Python library with no network service, auth, session, database, browser, robot execution, or LLM provider integration in Phase 1. [VERIFIED: `.planning/config.json`] [VERIFIED: user prompt] [VERIFIED: codebase]

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|------------------|
| V2 Authentication | no | No auth surface in Phase 1. [VERIFIED: codebase] |
| V3 Session Management | no | No sessions/cookies/service runtime in Phase 1. [VERIFIED: codebase] |
| V4 Access Control | no | No user/role/resource authorization layer in Phase 1. [VERIFIED: codebase] |
| V5 Input Validation | yes | Dataclass `__post_init__()` invariant validation and pytest `raises` coverage for domain objects. [VERIFIED: codebase] |
| V6 Cryptography | no | No crypto functions or secrets handling in Phase 1. [VERIFIED: codebase] |
| V8 Data Protection | limited | Keep benchmark artifacts deterministic and local; no sensitive runtime data sources exist in Phase 1. [VERIFIED: codebase] |
| V10 Malicious Code | yes | Do not add heavy/unverified dependencies; rely on existing `uv.lock`, package audit, and pure-Python standard-library patterns. [VERIFIED: `pyproject.toml`] [VERIFIED: slopcheck] |
| V12 File and Resources | limited | `write_benchmark_artifact` writes to caller-provided paths; examples should avoid privileged/system paths. [VERIFIED: codebase] [CITED: https://docs.python.org/3/library/pathlib.html#pathlib.Path.write_text] |

### Known Threat Patterns for Python library baseline

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Dependency confusion / slopsquatted package | Tampering | Do not add runtime deps; verify dev/build packages with slopcheck and PyPI before installs. [VERIFIED: slopcheck] [VERIFIED: PyPI] |
| Mutable diagnostics/provenance maps changed after construction | Tampering | Copy mappings before wrapping with `MappingProxyType`. [VERIFIED: codebase] [CITED: https://docs.python.org/3/library/types.html#types.MappingProxyType] |
| Path overwrite in artifact examples | Tampering | Document artifact writes to explicit local output paths; `Path.write_text` overwrites existing files. [CITED: https://docs.python.org/3/library/pathlib.html#pathlib.Path.write_text] |
| Raw/full map leakage through agent APIs | Information Disclosure | Keep agent APIs bounded typed outputs (`SplatQueryResult`, `PosteriorSummary`, `ProvenanceSummary`) rather than raw full splat dumps by default. [VERIFIED: codebase] [VERIFIED: `CLAUDE.md`] |
| Heavy backend import side effects | Denial of Service | Keep real backends deferred and behind future protocols/registries; Phase 1 runtime dependencies stay empty. [VERIFIED: `.planning/REQUIREMENTS.md`] [VERIFIED: `pyproject.toml`] |

## Sources

### Primary (HIGH confidence)

- `/home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md` — Phase 1 requirement IDs, v1 scope, out-of-scope table, traceability. [VERIFIED: codebase]
- `/home/prannayag/pragnition/robotics/mosaic/.planning/ROADMAP.md` — Phase 1 goal/success criteria, current main checkout evidence, later-phase boundaries. [VERIFIED: codebase]
- `/home/prannayag/pragnition/robotics/mosaic/.planning/STATE.md` — current focus, decisions, blockers, recent activity. [VERIFIED: codebase]
- `/home/prannayag/pragnition/robotics/mosaic/CLAUDE.md` — project constraints, conventions, GSD workflow guidance. [VERIFIED: codebase]
- Current source under `/home/prannayag/pragnition/robotics/mosaic/src/mosaic/` — public APIs and implementation patterns. [VERIFIED: codebase]
- Current tests under `/home/prannayag/pragnition/robotics/mosaic/tests/` — validation architecture and 73-test suite. [VERIFIED: codebase]
- `uv run pytest -q` — `73 passed in 0.25s`. [VERIFIED: command]
- Python docs: dataclasses, Protocol, StrEnum, MappingProxyType, json, pathlib. [CITED: https://docs.python.org/]
- pytest docs: pyproject config and src layout guidance. [CITED: https://docs.pytest.org/en/stable/reference/customize.html] [CITED: https://docs.pytest.org/en/stable/explanation/goodpractices.html]
- uv docs: dependencies, project run, locking/syncing. [CITED: https://docs.astral.sh/uv/concepts/projects/]
- PEP 561 — `py.typed` typed-package marker. [CITED: https://peps.python.org/pep-0561/]

### Secondary (MEDIUM confidence)

- PyPI package metadata and `pip index versions` for `pytest` and `uv-build`. [VERIFIED: PyPI]
- `slopcheck install pytest uv-build` visible verdict output. [VERIFIED: slopcheck]

### Tertiary (LOW confidence)

- None used for implementation-critical claims.

## Metadata

**Confidence breakdown:**

- Standard stack: HIGH — based on current `pyproject.toml`, `uv.lock`, installed uv environment, official uv/pytest/Python docs, and PyPI verification. [VERIFIED: codebase] [VERIFIED: command] [CITED: docs]
- Architecture: HIGH — based on direct source/test inspection and roadmap requirements. [VERIFIED: codebase] [VERIFIED: `.planning/ROADMAP.md`]
- Pitfalls: HIGH — based on explicit roadmap gaps, project constraints, and current empty README. [VERIFIED: codebase] [VERIFIED: `.planning/ROADMAP.md`]
- Security: MEDIUM — ASVS applicability is clear for this pure-library phase, but full threat model is deferred to planner threat_model block. [VERIFIED: codebase] [ASSUMED]

**Research date:** 2026-05-18  
**Valid until:** 2026-06-17 for current codebase facts; package-version checks should be refreshed if dependencies change. [ASSUMED]
