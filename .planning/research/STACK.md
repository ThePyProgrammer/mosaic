# Technology Stack Research: Mosaic v1 Foundation

**Project:** Mosaic  
**Research dimension:** Stack choices for v1 typed Python library foundation and near-term backend/evaluation readiness  
**Researched:** 2026-05-18  
**Overall confidence:** HIGH for core/dev stack; MEDIUM for future optional backend extras because exact 3DGS backend is intentionally not selected yet.

## Executive Recommendation

Mosaic v1 should standardize on a **small, typed, pure-Python core**: Python 3.12+, `uv`, `uv_build`, frozen/slotted dataclasses, `typing.Protocol`, stdlib serialization primitives, and pytest contract tests. Keep `dependencies = []` for the installable core until serialization and artifact schemas prove they need a runtime dependency. This is not austerity for its own sake; it keeps the foundation importable on laptops, CI, robots, and CPU-only evaluation hosts before CUDA-heavy 3DGS backends enter the room and make everything brittle.

Near-term readiness should come from **clean optional dependency boundaries**, not from pulling CUDA/research packages into the base package. Add extras only when a phase needs them: `serialization`, `arrays`, `backend-gsplat`, `backend-nerfstudio`, `evaluation`, `agents`, and possibly `ros` later. Real backend packages should live behind protocols, registries, availability checks, capability metadata, contract-test parametrization, and eventually subprocess isolation. If a backend can segfault, import CUDA libraries at module import time, or require a particular PyTorch/CUDA ABI, it does not belong in Mosaic core.

Testing should be treated as a product feature. Standardize `pytest` for unit tests, replay tests, backend contract tests, platform-rig tests, evaluation artifact tests, and agent-query determinism tests. Add Ruff and Pyright in the dev group before the public API grows; retrofitting type/lint discipline after coordinate frames, poses, splat maps, and backend protocols sprawl is how libraries become archaeological digs.

## Recommended Stack

### Core Runtime

| Technology | Version / Policy | Purpose | Recommendation | Confidence |
|------------|------------------|---------|----------------|------------|
| CPython | `>=3.12`; develop against `.python-version` `3.12`; do not raise to 3.13+ for v1 without a deliberate ADR | Library runtime | Keep Python 3.12+ as the floor. It provides modern typing features, faster runtime-checkable protocols, `typing.override`, better `**kwargs` typing, and a clean post-`distutils` baseline while staying conservative enough for robotics/CUDA ecosystems. | HIGH |
| Standard library dataclasses | Built-in | Domain model implementation | Use frozen/slotted dataclasses for core value objects: frame IDs, timestamps, poses, intrinsics, observations, splat primitives, backend results, platform rigs, claims, and artifact manifests. | HIGH |
| `typing.Protocol` / `runtime_checkable` | Built-in | Backend and dataset contracts | Use protocols for backend, replay sequence, artifact writer, posterior query, fusion, and platform seams. Avoid inheritance-heavy base classes until stateful behavior genuinely needs shared implementation. | HIGH |
| `enum.StrEnum` | Built-in in 3.11+ | Stable symbolic values | Use for public states such as tracking state, claim status, occupancy state, artifact kind, and backend health. String-valued enums make JSON artifacts and user debugging less hostile. | HIGH |
| `pathlib`, `json`, `csv`, `gzip`, `hashlib` | Built-in | Artifact IO foundation | Use stdlib for first artifact writers: deterministic JSON/JSONL, CSV summaries, checksums, and optional gzip compression. Keep binary formats deferred. | HIGH |

### Packaging and Dependency Management

| Technology | Version / Policy | Purpose | Recommendation | Confidence |
|------------|------------------|---------|----------------|------------|
| `uv` | Required developer tool; commit `uv.lock` | Project and dependency management | Standardize on `uv sync`, `uv lock`, `uv run`, and `uv build`. The active worktree already has `uv.lock`; main should converge to that discipline. | HIGH |
| `uv_build` | `>=0.10.10,<0.11.0` currently declared | Build backend | Keep `uv_build` for v1. The package is simple, src-layout, typed, and already configured for this backend. Do not switch build backends unless packaging requirements outgrow it. | HIGH |
| `pyproject.toml` | Single source of project config | Packaging/tool config | Put runtime deps in `[project].dependencies`, optional extras in `[project.optional-dependencies]`, dev-only tools in `[dependency-groups].dev`, pytest/Ruff/Pyright config under `[tool.*]`. | HIGH |
| Runtime dependencies | Keep empty for foundation: `dependencies = []` | Installable core | Preserve zero third-party runtime dependencies through the contracts/evaluation foundation unless a phase introduces schema validation that clearly justifies one. | HIGH |
| Lockfile | Commit `uv.lock` | Reproducible dev/test environment | Require lockfile updates with dependency changes. The main checkout currently lacks the worktree lockfile; merging the foundation should bring it over. | HIGH |

### Development and Test Tools

| Technology | Version / Policy | Purpose | Recommendation | Confidence |
|------------|------------------|---------|----------------|------------|
| pytest | `>=9.0,<10` preferred after foundation merge; current worktree allows `>=8.4.0` and locks `9.0.3` | Tests | Standardize on pytest. Use parametrization for backend contract tests, replay determinism tests, artifact shape tests, and agent-query tests. | HIGH |
| Ruff | `>=0.15,<0.16` | Linting and formatting | Add to dev group. Use Ruff for both lint and format instead of Black+isort+Flake8 stacks. One fast tool is enough; do not build a lint Rube Goldberg machine. | HIGH |
| Pyright | `>=1.1.409,<1.2` | Static type checking | Add to dev group and run in CI. Mosaic is a typed library; shipping `py.typed` without static checks is decoration, not engineering. Start at `typeCheckingMode = "strict"` for `src/mosaic`, relax narrowly only where needed. | MEDIUM-HIGH |
| `pytest-cov` | Defer until coverage gates are useful | Coverage reporting | Do not add immediately unless CI needs coverage metrics. Contract quality matters more than vanity percentages for this phase. Add later as a dev dependency if regression gates require it. | MEDIUM |
| Hypothesis | Defer; likely `hypothesis>=6` later | Property-based tests | Not v1 foundation default. Add when pose transforms, frame composition, serialization round trips, or fusion invariants become complex enough to justify generated cases. | MEDIUM |
| nox/tox | Do not adopt for v1 | Multi-env automation | Avoid until Mosaic actually supports multiple Python floors or dependency matrices. `uv run pytest`, `uv run ruff`, and `uv run pyright` are enough. | HIGH |

Recommended dev dependency group after foundation merge:

```toml
[dependency-groups]
dev = [
    "pytest>=9.0,<10",
    "ruff>=0.15,<0.16",
    "pyright>=1.1.409,<1.2",
]
```

If staying closer to the active worktree during merge, `pytest>=8.4.0` is acceptable temporarily because the worktree already uses it. The roadmap should still converge on an upper-bounded pytest major before CI becomes the compatibility oracle.

### Serialization and Artifacts

| Choice | Version / Policy | Purpose | Recommendation | Confidence |
|--------|------------------|---------|----------------|------------|
| JSON | stdlib `json`; canonical writer settings | Public artifacts and schema-like manifests | Use deterministic JSON for benchmark summaries, backend capability manifests, replay manifests, and evaluation outputs. Write with `sort_keys=True`, `separators=(",", ":")`, `ensure_ascii=True`, and `allow_nan=False`. | HIGH |
| JSONL | stdlib line-delimited JSON | Event traces | Use JSONL for per-frame replay logs, backend update traces, metric events, and agent tool traces. One JSON object per line; no repeated `json.dump()` into a single JSON document. | HIGH |
| CSV | stdlib `csv` | Human-friendly metric tables | Use only for flat per-run/per-episode summaries. Do not use CSV as the source of truth for nested pose, map, provenance, or posterior data. | HIGH |
| Schema representation | Start with typed dataclasses + explicit `to_json_dict`/`from_json_dict`; consider `msgspec` later | Stable artifact contracts | For the v1 foundation, hand-written stdlib serialization is enough and forces explicit public schema decisions. Add `msgspec` as an optional `serialization` extra if schema validation/performance becomes painful. | MEDIUM-HIGH |
| `msgspec` | Optional later: `msgspec>=0.21,<0.22` | Fast typed validation/serialization | Prefer over Pydantic for internal high-throughput artifact validation if/when a dependency is justified. It supports JSON/MessagePack/YAML/TOML and annotation-based validation. | MEDIUM |
| Pydantic | Do not adopt in core | Rich validation/JSON Schema | Avoid as a core dependency for v1. It is excellent, but Mosaic's foundation needs small immutable domain types more than runtime model magic. Reconsider for external API schema generation only if agent/tool schemas need it. | MEDIUM-HIGH |
| MessagePack/Parquet/Zarr/HDF5 | Defer | Large binary/numeric artifacts | Do not adopt before real backend/evaluation data volumes demand them. Premature binary formats will freeze the wrong abstractions. | HIGH |

Artifact policy:

1. Every benchmark/evaluation run should emit a machine-readable manifest with Mosaic version, backend name/version, backend capabilities, Python version, platform, dependency lock hash, dataset/replay manifest hash, and metric schema version.
2. Use append-only JSONL for traces: observations, backend updates, splat-map snapshots or snapshot references, metrics, failures, and agent tool calls.
3. Use JSON for aggregate summaries and schema-versioned manifests.
4. Use CSV only as a derived convenience export.
5. Never serialize `NaN`, `Infinity`, or non-string dict keys into public artifacts.

### Numeric and Geometry Dependencies

| Technology | Version / Policy | Purpose | Recommendation | Confidence |
|------------|------------------|---------|----------------|------------|
| Pure Python tuples/floats | Current foundation | Small core geometry | Keep for v1 core contracts. Poses, intrinsics, covariance summaries, and splat primitives can remain dependency-free while semantics stabilize. | HIGH |
| NumPy | Optional later: `numpy>=2.3,<3` or tighter once backend matrix is known | Array interop and evaluation metrics | Do not add to core immediately. Add an `arrays` extra when evaluation metrics or backend adapters need bulk numeric operations. Public APIs should accept/export plain typed structures first and provide NumPy adapters second. | MEDIUM-HIGH |
| SciPy | Optional later | Advanced pose/math/statistics | Defer. It is too heavy for the foundation and unnecessary before trajectory metrics or optimization helpers need it. | HIGH |
| PyTorch | Backend-specific extra only | Real 3DGS backends | Never core. PyTorch/CUDA compatibility is the exact blast radius optional extras are meant to contain. | HIGH |
| OpenCV | Optional evaluation/perception extra only | Image IO/CV helpers | Do not add to core. If needed for dataset adapters or evaluation visualizations, use an extra and isolate imports. | HIGH |

### Backend and Evaluation Readiness Extras

These extras should be planned in `pyproject.toml` but not all implemented immediately. Use placeholders only when packages are actually chosen; extras with no dependencies are noise.

| Extra | Intended Dependencies | When to Add | Why |
|-------|-----------------------|-------------|-----|
| `mosaic[serialization]` | likely `msgspec>=0.21,<0.22` | When hand-written stdlib schema code becomes repetitive or artifact validation needs speed | Keeps validation optional while allowing robust artifact parsing. |
| `mosaic[arrays]` | likely `numpy>=2.3,<3` | When evaluation metrics or backend adapters require dense arrays | Avoids making NumPy mandatory for users who only need contracts. |
| `mosaic[evaluation]` | possibly `numpy`, later plotting/reporting libs | When deterministic metrics and benchmark artifact writing land | Evaluation tooling can be heavier than core but should remain CPU-friendly. |
| `mosaic[backend-gsplat]` | backend-specific PyTorch/CUDA/gsplat pins | Only after contracts, artifacts, and regression gates exist | Real 3DGS backends should be opt-in and contract-tested. |
| `mosaic[backend-nerfstudio]` | backend-specific Nerfstudio/gsplat pins | Only if Nerfstudio-derived integration is selected | Do not choose this by inertia; select after backend research. |
| `mosaic[agents]` | likely none initially; maybe schema tooling later | When posterior query seam and memory/tool API stabilize | Agent APIs should be deterministic local contracts, not LLM SDK wrappers. |
| `mosaic[ros]` | ROS packages, if ever | Not v1 | ROS wrappers are downstream integration, not library foundation. |
| `mosaic[habitat]` | Habitat Lab stack, if ever | Not v1; only for ARNA-like evaluation reconstruction | Habitat is useful for ARNA-style research, but it is not a Mosaic core dependency. |

### Backend Isolation Policy

| Concern | Standardize This | Do Not Do This | Confidence |
|---------|------------------|----------------|------------|
| Backend discovery | Registry entries with name, version, capabilities, parameters, availability checks, and failure reason | Import every backend package at `mosaic.slam` import time | HIGH |
| Contract validation | Parametrized pytest contract suite run against fake backend and any installed real backend | Bespoke tests per backend with incompatible semantics | HIGH |
| Heavy imports | Lazy import inside backend factory/availability check | Top-level `torch`, `cv2`, CUDA, or research-code imports in core modules | HIGH |
| Crash isolation | Protocol seam that can later run in subprocess | Assuming all CUDA/research code is safe in-process | HIGH |
| Capability metadata | Explicit flags: multi-camera support, uncertainty output, posterior snapshots, reset support, deterministic replay support, device requirements | Backend-specific if/else spread through evaluation code | HIGH |

## Recommended `pyproject.toml` Shape

This is the target shape after the foundation worktree is merged and dev tooling is standardized:

```toml
[project]
name = "mosaic"
version = "0.1.0"
description = "Typed Gaussian-splatting SLAM primitives for multi-view robotic perception"
readme = "README.md"
requires-python = ">=3.12"
dependencies = []

[dependency-groups]
dev = [
    "pytest>=9.0,<10",
    "ruff>=0.15,<0.16",
    "pyright>=1.1.409,<1.2",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]

[tool.ruff]
target-version = "py312"
line-length = 100
src = ["src", "tests"]

[tool.pyright]
pythonVersion = "3.12"
typeCheckingMode = "strict"
include = ["src", "tests"]

[build-system]
requires = ["uv_build>=0.10.10,<0.11.0"]
build-backend = "uv_build"
```

Do not add optional dependencies until the corresponding phase uses them. Empty or speculative extras make dependency policy look mature while doing precisely nothing.

## Test Command Standardization

Use these as the canonical developer commands:

```bash
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv build
```

For local formatting:

```bash
uv run ruff format .
uv run ruff check --fix .
```

Contract-test pattern to standardize:

- Fake backend is always installed and always tested.
- Optional real backends are collected through registry availability checks.
- Unavailable optional backends are skipped with explicit reasons.
- Expected backend limitations use `pytest.param(..., marks=...)`, not hidden conditionals inside tests.

## What Not to Adopt Yet

| Do Not Adopt | Why Not | Revisit When | Confidence |
|--------------|---------|--------------|------------|
| ROS / ROS2 packages | Mosaic v1 is a headless library foundation. ROS belongs in wrappers/adapters. | A downstream robot integration milestone exists. | HIGH |
| Habitat Lab | ARNA uses Habitat, but Mosaic is not reproducing ARNA in v1. Habitat would dominate dependency and environment design. | A dedicated simulator/evaluation milestone explicitly targets Habitat. | HIGH |
| LLM SDKs such as OpenAI/Anthropic/LangChain | Agent seam should return deterministic typed outputs, not bind Mosaic to provider churn. | A separate orchestration package needs provider adapters. | HIGH |
| PyTorch/CUDA in core | Backend ABI fragility would contaminate every user and CI job. | Only as backend-specific optional extras. | HIGH |
| Pydantic in core | Strong tool, wrong default for a tiny immutable domain-core library. Adds runtime dependency and model semantics before schemas settle. | External JSON Schema/tool-call schema generation becomes a first-class requirement. | MEDIUM-HIGH |
| Open3D / trimesh / visualization stacks | Visualization is useful but not part of v1 foundation. | Evaluation/debug visualization phase. | HIGH |
| Database storage | In-memory dataclass stores are enough for foundation and deterministic tests. | Artifact volume or multi-session query requirements force persistence. | HIGH |
| Binary artifact formats | JSON/JSONL is inspectable and adequate for schema stabilization. | Real benchmarks produce artifacts too large for sane JSONL handling. | HIGH |
| Plugin frameworks/importlib entry points | A local registry is simpler and testable. | Third-party backend distribution becomes a real requirement. | MEDIUM-HIGH |

## Roadmap Implications

1. **Foundation merge should carry over the active worktree stack:** Python 3.12, `uv`, `uv.lock`, `uv_build`, pytest config, `py.typed`, zero runtime dependencies, and the existing pure-Python modules.
2. **Next stack change should be dev-tooling, not runtime deps:** add Ruff and Pyright before expanding public APIs.
3. **Serialization should start stdlib-first:** deterministic JSON/JSONL artifacts, explicit schema versions, checksums, and round-trip tests.
4. **Evaluation should add dependencies only under extras:** keep fake-backend benchmark and JSON artifacts CPU-only before any real 3DGS backend enters.
5. **Backend integration should be opt-in and isolated:** do not pick `gsplat`, Nerfstudio, PyTorch, CUDA, or OpenCV as base dependencies until backend research and regression gates justify them.
6. **Agent-friendly representation should remain provider-free:** memory/tool contracts may live in core or an `agents` namespace, but LLM providers and Habitat-style runtime loops stay out of v1.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Python 3.12 baseline | HIGH | Existing project/worktree already require it; official Python docs support it as a strong typed-library baseline. |
| uv / uv_build | HIGH | Existing project uses `uv_build`; active worktree has `uv.lock`; uv official docs support project management and lockfile workflow. |
| Zero runtime dependencies for core | HIGH | Existing foundation proves current core contracts work with stdlib only; project constraints explicitly require pure-Python foundation. |
| pytest standardization | HIGH | Existing worktree already uses pytest; official docs support parametrization needed for backend contract tests. |
| Ruff recommendation | HIGH | Official docs position Ruff as fast linter/formatter with broad rule coverage and pyproject config. |
| Pyright recommendation | MEDIUM-HIGH | Current version verified from package index; official page fetch was too sparse in this environment, but Pyright is the right fit for a `py.typed` strict-library posture. Validate exact config in phase implementation. |
| msgspec later for serialization | MEDIUM | Official docs support performance and typed validation claims; Mosaic may not need it if stdlib artifacts remain manageable. |
| Avoiding Pydantic in core | MEDIUM-HIGH | Official docs confirm Pydantic's strengths; recommendation is architectural: the core should stay smaller until schema generation needs are real. |
| Backend extras | MEDIUM | Policy is clear, but exact backend packages await backend-selection research. |

## Sources

- Project context: `/home/prannayag/pragnition/robotics/mosaic/.planning/PROJECT.md`
- Main checkout stack map: `/home/prannayag/pragnition/robotics/mosaic/.planning/codebase/STACK.md`
- Active foundation worktree stack map: `/home/prannayag/pragnition/robotics/.mosaic-worktrees/splat-slam-foundation/.planning/codebase/STACK.md`
- Migration plan: `/home/prannayag/pragnition/robotics/mosaic/docs/argus-migration-plan.md`
- Agent-friendly representation spec: `/home/prannayag/pragnition/robotics/mosaic/docs/superpowers/specs/2026-05-18-agent-friendly-representation-design.md`
- ARNA replication notes: `/home/prannayag/pragnition/robotics/mosaic/outputs/arna-2506-17462-replication.md`
- Python 3.12 official documentation: https://docs.python.org/3.12/whatsnew/3.12.html
- Python packaging guide for `pyproject.toml`: https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
- uv official documentation: https://docs.astral.sh/uv/
- pytest official documentation: https://docs.pytest.org/en/stable/
- pytest parametrization docs: https://docs.pytest.org/en/stable/how-to/parametrize.html
- Ruff official documentation: https://docs.astral.sh/ruff/
- Python stdlib JSON documentation: https://docs.python.org/3/library/json.html
- msgspec documentation: https://jcristharif.com/msgspec/
- Pydantic documentation: https://pydantic.dev/docs/validation/latest/get-started/
- Package version checks via `python -m pip index versions`: pytest 9.0.3, Ruff 0.15.13, Pyright 1.1.409, msgspec 0.21.1, NumPy 2.4.5 as of 2026-05-18 in this environment.
