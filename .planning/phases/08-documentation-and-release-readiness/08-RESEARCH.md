# Phase 08: Documentation and Release Readiness - Research

**Researched:** 2026-05-21  
**Domain:** Python library release documentation, Markdown contract tests, dependency-boundary policy  
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
## Implementation Decisions

### Documentation Shape
- **D-01:** Use split release documentation, not a README-only guide.
- **D-02:** Keep `README.md` concise as the public orientation page and golden-path entry point.
- **D-03:** Add dedicated docs for API surface and examples, with expected targets such as `docs/API.md` and `docs/EXAMPLES.md`.
- **D-04:** Add contributor guidance in a dedicated contributor-facing document, expected as `CONTRIBUTING.md` unless the planner finds a stronger existing convention.
- **D-05:** Add or extend machine checks for the split docs. Tests should assert key headings, commands, boundary terms, and example import/API paths so docs do not drift silently.

### Canonical End-to-End Example
- **D-06:** The canonical example should be one golden path, not an API tour: deterministic replay → fake/backend contract fixture → splat snapshot or benchmark result → benchmark artifact → agent-facing representation-memory query.
- **D-07:** The golden path should end with a representation-memory/tool-style query so Phase 7's implemented agent-friendly layer is visible in release docs.
- **D-08:** The example should write a local benchmark artifact, because DOCS-02 requires evaluation artifact coverage. Keep the artifact local/disposable and do not imply external services.
- **D-09:** Present the golden path as a narrative snippet rather than a full copy-paste script. It should be readable and API-accurate, but does not need to be a standalone tutorial program.

### Release Boundary Wording
- **D-10:** Use blunt explicit boundary language for deferred integrations. Public docs should name real 3DGS backends, ROS, Habitat, UI/WebSockets, LLM/LVLM providers, CUDA/native stacks, and production SLAM quality as out of v1 core scope.
- **D-11:** Describe `DeterministicSplatBackend`, deterministic scenarios, benchmark gates, and `ProvenancePreservingFusion` as contract/reference fixtures for tests, examples, and regression gates. Do not describe them as production SLAM, real Gaussian optimization, calibrated uncertainty minimization, or reconstruction-quality implementations.
- **D-12:** Present posterior views and representation memories as separate provider-free layers: `SplatPosteriorView` is a bounded descriptive splat-snapshot query layer; `RepresentationMemory` and related tools are a higher deterministic memory/tool contract layer.
- **D-13:** Rewrite stale phase-era wording into release-versioned language. Public docs should say “Mosaic v1 foundation” and describe current implemented modules rather than “Phase 1 baseline” or “Phase 7 planned.” Keep phase history in planning artifacts, not as the main public framing.

### Contributor Policy
- **D-14:** Contributor guidance should give equal prominence to dependency boundary, API stability, and test workflow.
- **D-15:** Optional extras guidance should be policy-only in Phase 8. Explain that heavy future integrations must be optional and isolated, but do not add placeholder extras to `pyproject.toml` until a real optional integration exists.
- **D-16:** Public API additions must update appropriate package `__all__` exports, root export decisions where relevant, API docs, and public API tests.
- **D-17:** Real-backend contributor guidance should stop at the contract boundary: registry/adapter seam, availability checks, and contract tests. Do not provide detailed real backend implementation instructions in v1 docs.

### Claude's Discretion
- The planner may choose exact filenames for the dedicated API/examples docs if they preserve the split-doc intent and pass doc contract tests.
- The planner may choose exact doc-test organization, provided tests are low-maintenance and match existing deterministic pytest style.
- The planner may choose how much of the golden path remains in `README.md` versus `docs/EXAMPLES.md`, provided README stays concise and links to the deeper doc.

### Deferred Ideas (OUT OF SCOPE)
## Deferred Ideas

None — discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| DOCS-01 | Public docs distinguish implemented foundation APIs from planned real backend, ROS, Habitat, UI, and LLM integrations. | Use split release docs, v1 language, explicit out-of-scope terms, and doc contract tests over boundary wording. [VERIFIED: `.planning/REQUIREMENTS.md`; `.planning/phases/08-documentation-and-release-readiness/08-CONTEXT.md`] |
| DOCS-02 | Public docs include a minimal end-to-end example using deterministic replay, fake backend, splat snapshot, evaluation artifact, and agent posterior query. | Build one golden path from `synthetic_forward_sequence`, `DeterministicSplatBackend`, `run_slam_benchmark`/snapshot, `write_benchmark_artifact`, `SplatPosteriorView`, and `RepresentationMemory` query APIs. [VERIFIED: `tests/evaluation/test_runner.py`; `tests/agents/test_representation_memory.py`; `tests/test_public_api.py`] |
| DOCS-03 | Contributor guidance explains dependency policy, optional extras, test commands, and the rule that heavy backends stay behind registry/adapter seams. | Write `CONTRIBUTING.md` around empty runtime dependencies, pyproject optional-dependency policy, `uv sync`, `uv run pytest -q`, backend registry metadata, availability checks, and contract helpers. [VERIFIED: `pyproject.toml`; `tests/slam/test_backend_registry.py`; `tests/slam/test_backend_contract_helpers.py`; CITED: https://packaging.python.org/en/latest/specifications/pyproject-toml/; CITED: https://docs.astral.sh/uv/concepts/projects/locking-and-syncing/] |
</phase_requirements>

## Summary

Phase 08 is a documentation-release hardening phase, not a feature phase. The implementation should restructure public docs into a concise README plus dedicated API, example, and contributor documents while keeping runtime code and dependency metadata unchanged unless doc tests reveal stale public API claims. [VERIFIED: `.planning/phases/08-documentation-and-release-readiness/08-CONTEXT.md`; `pyproject.toml`]

The main planning risk is stale phase-era wording: the current README still frames the package as “Phase 1” and says Phase 7 representation memories are planned, while the current code exports `RepresentationMemory`, `MemoryQueryResult`, `QueryFamily`, `ClaimStatus`, `EntityKind`, and related agent-memory symbols. [VERIFIED: `README.md`; `src/mosaic/__init__.py`; `tests/test_public_api.py`] The planner should treat this as a docs drift correction, with pytest contract tests acting as the drift detector. [VERIFIED: `tests/test_readme_contract.py`; CITED: https://docs.pytest.org/en/stable/how-to/assert.html]

**Primary recommendation:** Plan one documentation wave that creates `docs/API.md`, `docs/EXAMPLES.md`, and `CONTRIBUTING.md`, rewrites `README.md` as the concise “Mosaic v1 foundation” entry point, and extends deterministic pytest doc-contract tests to lock headings, boundary wording, commands, key imports, and the golden path. [VERIFIED: `.planning/phases/08-documentation-and-release-readiness/08-CONTEXT.md`; `tests/test_readme_contract.py`]

## Project Constraints (from CLAUDE.md)

- Mosaic is a typed, headless Python library for 3D Gaussian Splatting SLAM contracts over multi-view moving cameras; v1 docs must keep the library-first framing. [VERIFIED: `CLAUDE.md`]
- The stack is Python 3.12+, `uv`, pure-Python foundation modules, and `pytest`; docs and tests must not introduce CUDA/native runtime requirements. [VERIFIED: `CLAUDE.md`; `pyproject.toml`]
- Real 3DGS/CUDA/research backends must stay behind protocols, registries, optional dependencies, and isolation boundaries. [VERIFIED: `CLAUDE.md`; `tests/slam/test_backend_registry.py`]
- Frame semantics and timestamp precision are core contracts; docs must not hand-wave coordinate-frame conventions where public APIs expose them. [VERIFIED: `CLAUDE.md`; `tests/core/test_frames_and_poses.py`]
- Evaluation gates must exist before real backend integration; contributor docs should say real-backend work is blocked on deterministic artifacts and regression gates. [VERIFIED: `CLAUDE.md`; `.planning/REQUIREMENTS.md`]
- Agent APIs must return bounded typed outputs with evidence/provenance and must not expose raw full splat maps or provider-specific prompts. [VERIFIED: `CLAUDE.md`; `tests/agents/test_splat_posterior.py`; `tests/agents/test_representation_memory.py`]
- Public APIs should remain typed, package-rooted, and exported through explicit `__all__` lists. [VERIFIED: `CLAUDE.md`; `src/mosaic/__init__.py`; package `__init__.py` files]
- Use `uv run pytest ... -q` as the local quality gate; do not invent a different local-vs-CI entry point in docs. [VERIFIED: `CLAUDE.md`; `pyproject.toml`]
- Avoid `print()` in library code; Phase 08 should not touch library code except if a doc-test-discovered API mismatch requires a narrow fix. [VERIFIED: `CLAUDE.md`]
- GSD workflow enforcement applies to repo edits; this research file is part of the requested GSD planning workflow. [VERIFIED: `CLAUDE.md`; user objective]

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Release orientation and v1 boundary docs | Documentation / Repository | Python package metadata | README and docs own public user framing; metadata only supplies version, readme target, and dependency facts. [VERIFIED: `README.md`; `pyproject.toml`] |
| API surface documentation | Documentation / Repository | Python library package | Docs must mirror package `__all__` and public tests; the source package remains the authority for exports. [VERIFIED: `src/mosaic/__init__.py`; `tests/test_public_api.py`] |
| Golden-path example | Documentation / Repository | Python library package; pytest | The example should compose existing deterministic APIs and be guarded by tests, not add runtime behavior. [VERIFIED: `.planning/phases/08-documentation-and-release-readiness/08-CONTEXT.md`; `tests/evaluation/test_runner.py`] |
| Contributor dependency policy | Documentation / Repository | Python package metadata | `CONTRIBUTING.md` owns policy; `pyproject.toml` enforces current empty runtime dependencies and dev pytest dependency. [VERIFIED: `pyproject.toml`; CITED: https://packaging.python.org/en/latest/specifications/pyproject-toml/] |
| Doc drift prevention | Test suite | Documentation / Repository | Existing doc-contract tests already inspect README contents and execute/import public API snippets; extending this pattern keeps drift visible. [VERIFIED: `tests/test_readme_contract.py`; CITED: https://docs.pytest.org/en/stable/how-to/assert.html] |
| Backend extension guidance | Documentation / Repository | `mosaic.slam` registry/contracts | Contributor docs should explain registry/adapter seams, availability checks, and contract helpers while leaving real backend implementation deferred. [VERIFIED: `tests/slam/test_backend_registry.py`; `tests/slam/test_backend_contract_helpers.py`] |

## Standard Stack

### Core
| Library / Tool | Version | Purpose | Why Standard |
|----------------|---------|---------|--------------|
| Python | `>=3.12` project requirement; local `python` reports 3.14.4 | Runtime for the typed headless library and docs examples | Project metadata requires Python 3.12+ and all current runtime dependencies are standard-library-only. [VERIFIED: `pyproject.toml`; local `python --version`] |
| uv | 0.10.10 local | Project environment sync and test command wrapper | `uv sync` aligns the project environment with the lockfile and `uv run` can sync automatically for commands. [VERIFIED: local `uv --version`; CITED: https://docs.astral.sh/uv/concepts/projects/locking-and-syncing/] |
| pytest | `>=8.4.0` dev dependency; local `uv run pytest --version` reports 9.0.3 | Deterministic test and doc-contract framework | Existing project tests use pytest; pytest supports plain `assert` with introspection for readable contract failures. [VERIFIED: `pyproject.toml`; local `uv run pytest --version`; CITED: https://docs.pytest.org/en/stable/how-to/assert.html] |
| Markdown | repository docs format | README, API, examples, and contributor docs | Existing public docs and planning docs are Markdown; Phase 08 decisions require split public docs. [VERIFIED: `README.md`; `.planning/phases/08-documentation-and-release-readiness/08-CONTEXT.md`] |

### Supporting
| Library / Tool | Version | Purpose | When to Use |
|----------------|---------|---------|-------------|
| `pathlib.Path` | Python standard library | Read documentation files and write disposable example artifacts in tests | Use for doc tests and examples that need local file paths; `tmp_path` returns a `pathlib.Path`. [CITED: https://docs.pytest.org/en/stable/how-to/tmp_path.html] |
| pytest `tmp_path` fixture | pytest fixture | Isolated temporary benchmark artifact target | Use in doc/example tests that prove `write_benchmark_artifact` writes a local disposable file; pytest provides a temporary directory unique to each test. [CITED: https://docs.pytest.org/en/stable/how-to/tmp_path.html] |
| `tomllib` | Python standard library [ASSUMED] | Parse `pyproject.toml` in doc contract tests if string checks become brittle | Use only if planner wants structured checks for `dependencies = []`; current tests already use text checks. [VERIFIED: `tests/test_readme_contract.py`; ASSUMED] |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Hand-written README-only docs | Split README + `docs/API.md` + `docs/EXAMPLES.md` + `CONTRIBUTING.md` | README-only contradicts locked decision D-01 and makes API/examples/contributor policy harder to test separately. [VERIFIED: `.planning/phases/08-documentation-and-release-readiness/08-CONTEXT.md`] |
| Doctest blocks | Pytest doc-contract tests over files plus import/API smoke checks | Doctest would require copy-paste executable blocks; locked decision D-09 says the golden path can be narrative and need not be a standalone tutorial program. [VERIFIED: `.planning/phases/08-documentation-and-release-readiness/08-CONTEXT.md`] |
| New docs dependency such as MkDocs/Sphinx | Plain Markdown under repository docs | New docs tooling would add dependency and maintenance surface with no Phase 08 requirement; current docs need release readiness, not a generated site. [VERIFIED: `.planning/phases/08-documentation-and-release-readiness/08-CONTEXT.md`; `pyproject.toml`] |

**Installation:**
```bash
uv sync
uv run pytest -q
```
These commands use the existing project configuration and do not install new runtime dependencies. [VERIFIED: `pyproject.toml`; CITED: https://docs.astral.sh/uv/concepts/projects/locking-and-syncing/]

**Version verification:** No new external packages are recommended for Phase 08, so ecosystem registry verification is not required. Existing local tool versions observed during research: `uv 0.10.10`, `python 3.14.4`, `uv run pytest 9.0.3`. [VERIFIED: local command output]

## Package Legitimacy Audit

Phase 08 should not install new external packages. [VERIFIED: `.planning/phases/08-documentation-and-release-readiness/08-CONTEXT.md`; `pyproject.toml`] The package legitimacy gate is not triggered because the recommended implementation uses existing `pytest`, existing `uv`, Markdown files, and Python standard library helpers. [VERIFIED: `pyproject.toml`; local environment audit]

| Package | Registry | Age | Downloads | Source Repo | slopcheck | Disposition |
|---------|----------|-----|-----------|-------------|-----------|-------------|
| None | — | — | — | — | Not run | No external package installs recommended. [VERIFIED: research scope] |

**Packages removed due to slopcheck [SLOP] verdict:** none. [VERIFIED: no packages recommended]  
**Packages flagged as suspicious [SUS]:** none. [VERIFIED: no packages recommended]

## Architecture Patterns

### System Architecture Diagram

```text
User / Contributor
        |
        v
README.md (concise v1 orientation + golden-path link hub)
        |
        +--------------------------+-----------------------------+-----------------------------+
        |                          |                             |
        v                          v                             v
 docs/API.md                docs/EXAMPLES.md              CONTRIBUTING.md
 (public export map,        (deterministic replay ->       (dependency policy,
 implemented modules,       deterministic backend ->       optional extras policy,
 deferred integrations)     benchmark artifact ->          tests, backend registry /
                            posterior + memory query)      adapter seams)
        |                          |                             |
        +--------------------------+-----------------------------+
                                   |
                                   v
                         tests/test_readme_contract.py
                         and/or tests/test_docs_contract.py
                         (headings, commands, boundary terms,
                         import/API paths, artifact write checks)
                                   |
                                   v
                         uv run pytest -q release gate
```

This architecture keeps public documentation as the release surface and pytest as the verification surface; the Python library remains the source of API truth. [VERIFIED: `tests/test_readme_contract.py`; `tests/test_public_api.py`; `.planning/phases/08-documentation-and-release-readiness/08-CONTEXT.md`]

### Recommended Project Structure

```text
README.md                         # Concise Mosaic v1 foundation orientation and links. [VERIFIED: D-02]
CONTRIBUTING.md                   # Contributor policy for dependencies, tests, API stability, backend seams. [VERIFIED: D-04]
docs/
├── API.md                        # Implemented public API surfaces and explicit deferred integrations. [VERIFIED: D-03]
├── EXAMPLES.md                   # Golden-path narrative example and local artifact behavior. [VERIFIED: D-03, D-06]
└── argus-migration-plan.md       # Existing historical planning doc; do not use as public v1 framing. [VERIFIED: current docs]
tests/
├── test_readme_contract.py       # Existing README drift checks to update for v1 language. [VERIFIED: current tests]
└── test_docs_contract.py         # Recommended split-doc checks if planner keeps README tests focused. [ASSUMED]
```

### Pattern 1: Documentation Contract Tests Over Stable Files
**What:** Test docs as release contracts by asserting required headings, commands, boundary terms, and API snippets against local Markdown files. [VERIFIED: `tests/test_readme_contract.py`]  
**When to use:** Use for README, API docs, examples docs, and contributor docs because Phase 08 success criteria are text/API-boundary requirements. [VERIFIED: `.planning/REQUIREMENTS.md`]  
**Example:**
```python
# Source: tests/test_readme_contract.py and pytest assert docs
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_release_docs_name_deferred_integrations() -> None:
    text = (ROOT / "docs" / "API.md").read_text(encoding="utf-8").casefold()

    for term in ("real 3dgs", "ros", "habitat", "ui", "websocket", "llm", "lvm", "cuda"):
        assert term in text
```
Pytest supports plain `assert` and assertion introspection for readable failures. [CITED: https://docs.pytest.org/en/stable/how-to/assert.html]

### Pattern 2: API Docs Generated by Reading Export Surfaces Manually, Not by Import-Time Reflection
**What:** Document package surfaces from explicit `__all__` exports and public tests, then lock representative names in doc tests. [VERIFIED: `src/mosaic/__init__.py`; `tests/test_public_api.py`]  
**When to use:** Use for `docs/API.md` so release docs match stable package surfaces without adding generated-doc tooling. [VERIFIED: `.planning/phases/08-documentation-and-release-readiness/08-CONTEXT.md`; `pyproject.toml`]  
**Example:**
```python
# Source: tests/test_public_api.py and src/mosaic/__init__.py
from mosaic import DeterministicSplatBackend, FrameId, RepresentationMemory, SplatPosteriorView


def test_api_docs_reference_current_root_exports() -> None:
    api_doc = Path("docs/API.md").read_text(encoding="utf-8")

    for name in ("DeterministicSplatBackend", "SplatPosteriorView", "RepresentationMemory"):
        assert name in api_doc
```

### Pattern 3: Golden Path Uses Existing Deterministic Fixtures Only
**What:** Compose `synthetic_forward_sequence`, `DeterministicSplatBackend`, benchmark artifact writing, posterior query, and representation-memory query in one narrative path. [VERIFIED: `.planning/phases/08-documentation-and-release-readiness/08-CONTEXT.md`; `tests/evaluation/test_runner.py`; `tests/agents/test_representation_memory.py`]  
**When to use:** Use for DOCS-02 and keep it local/disposable with `tmp_path` in tests. [VERIFIED: `.planning/REQUIREMENTS.md`; CITED: https://docs.pytest.org/en/stable/how-to/tmp_path.html]  
**Example:**
```python
# Source: tests/evaluation/test_runner.py and tests/agents/test_representation_memory.py
from mosaic import DeterministicSplatBackend, FrameId, run_slam_benchmark, synthetic_forward_sequence
from mosaic import write_benchmark_artifact


def test_docs_golden_path_writes_artifact(tmp_path) -> None:
    artifact = run_slam_benchmark(
        scenario=synthetic_forward_sequence(frame_count=3),
        backend=DeterministicSplatBackend(map_frame=FrameId("map")),
    )
    path = tmp_path / "mosaic-benchmark.json"

    write_benchmark_artifact(artifact, path)

    assert path.read_text(encoding="utf-8").startswith("{\n")
    assert artifact.backend_name == "deterministic-splat"
```

### Pattern 4: Contributor Policy Separates Required Dependencies From Future Optional Extras
**What:** State that current runtime dependencies remain empty and future heavy integrations must use optional dependency extras plus registry/adapter seams when real integrations exist. [VERIFIED: `pyproject.toml`; `.planning/phases/08-documentation-and-release-readiness/08-CONTEXT.md`]  
**When to use:** Use for `CONTRIBUTING.md` dependency and backend sections. [VERIFIED: DOCS-03]  
**Example:**
```toml
# Source: pyproject.toml and Python packaging spec
[project]
dependencies = []

# Do not add placeholder optional-dependencies in Phase 08.
# Future real integrations may use [project.optional-dependencies]
# only when a real optional integration exists.
```
`project.dependencies` lists expected dependencies, while `project.optional-dependencies` defines extras that install only when requested. [CITED: https://packaging.python.org/en/latest/specifications/pyproject-toml/]

### Anti-Patterns to Avoid
- **README-only release docs:** Contradicts locked split-doc decision and makes API/examples/contributor policy too easy to rot. [VERIFIED: D-01]
- **Phase-history public framing:** “Phase 1 baseline” and “Phase 7 planned” are stale release-facing language; use “Mosaic v1 foundation.” [VERIFIED: D-13; current `README.md`]
- **Copy-paste full tutorial script as the canonical example:** D-09 asks for a narrative snippet, not a standalone script; tests can validate representative imports and behavior separately. [VERIFIED: D-09]
- **Mentioning heavy packages in install commands:** Existing tests already guard against lines starting with `pip install`, `uv add`, or `uv pip install` for boundary terms; preserve and extend this. [VERIFIED: `tests/test_readme_contract.py`]
- **Adding placeholder extras:** D-15 explicitly says optional extras guidance is policy-only in Phase 08; do not mutate `pyproject.toml` to add fake extras. [VERIFIED: D-15]
- **Calling deterministic fixtures production SLAM:** D-11 forbids describing `DeterministicSplatBackend`, deterministic scenarios, gates, or `ProvenancePreservingFusion` as production-quality reconstruction or optimization. [VERIFIED: D-11]
- **Blurring posterior views and representation memories:** D-12 requires `SplatPosteriorView` and `RepresentationMemory` to be presented as separate provider-free layers. [VERIFIED: D-12]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Documentation drift detection | Custom parser framework or generated-doc site | Small pytest tests reading Markdown files | Existing project already uses deterministic pytest file-content checks and import/API checks. [VERIFIED: `tests/test_readme_contract.py`; `tests/test_public_api.py`] |
| Temporary artifact validation | Manual cleanup paths under repo root | pytest `tmp_path` | `tmp_path` provides a temporary directory unique to each test function. [CITED: https://docs.pytest.org/en/stable/how-to/tmp_path.html] |
| Dependency policy enforcement | Custom package scanner | `pyproject.toml` checks plus explicit doc text | Current runtime dependency truth is `dependencies = []`; Python packaging defines optional extras in `project.optional-dependencies`. [VERIFIED: `pyproject.toml`; CITED: https://packaging.python.org/en/latest/specifications/pyproject-toml/] |
| Backend readiness explanation | Real backend tutorial | Existing registry metadata, availability checks, and contract helpers | Phase 08 should explain seams, not implement real backend instructions. [VERIFIED: D-17; `tests/slam/test_backend_registry.py`; `tests/slam/test_backend_contract_helpers.py`] |
| API reference generation | Sphinx/MkDocs/autodoc setup | Hand-maintained Markdown mirrored to `__all__` and public API tests | No docs site tooling is required or declared; adding tooling expands scope and dependencies. [VERIFIED: `pyproject.toml`; `.planning/phases/08-documentation-and-release-readiness/08-CONTEXT.md`] |

**Key insight:** Phase 08 needs release clarity, not a documentation platform. The safe plan is to make public Markdown precise and then lock the critical claims with pytest. [VERIFIED: phase context; existing tests]

## Common Pitfalls

### Pitfall 1: Stale Phase-Era README Language
**What goes wrong:** Docs say “Phase 1 baseline” or “Phase 7 planned” after Phase 7 symbols are implemented and exported. [VERIFIED: `README.md`; `tests/test_public_api.py`]  
**Why it happens:** Earlier phase docs accumulated in README and were not rewritten as release-versioned public docs. [VERIFIED: `.planning/phases/08-documentation-and-release-readiness/08-CONTEXT.md`]  
**How to avoid:** Search public docs for “Phase 1”, “Phase 7 planned”, and “baseline” framing; replace user-facing framing with “Mosaic v1 foundation” while keeping phase history in planning artifacts. [VERIFIED: D-13]  
**Warning signs:** Doc tests still assert old strings like `not required for Phase 1`, or public docs say representation memories remain planned. [VERIFIED: `tests/test_readme_contract.py`; `README.md`]

### Pitfall 2: Example Becomes an API Tour Instead of a Golden Path
**What goes wrong:** `docs/EXAMPLES.md` lists many disconnected snippets but fails DOCS-02’s one end-to-end path. [VERIFIED: DOCS-02; D-06]  
**Why it happens:** Public API surface is broad after seven phases, so documentation authors may try to cover everything equally. [VERIFIED: `src/mosaic/__init__.py`; public export list]  
**How to avoid:** Make one canonical flow: deterministic replay/scenario → deterministic backend → benchmark artifact and snapshot → posterior view → representation-memory/tool-style query. [VERIFIED: D-06; D-07; D-08]  
**Warning signs:** The example lacks `write_benchmark_artifact`, `SplatPosteriorView`, or `RepresentationMemory`; it does not visibly produce a local artifact. [VERIFIED: DOCS-02; D-08]

### Pitfall 3: Boundary Terms Accidentally Look Like Install Instructions
**What goes wrong:** Docs say `pip install torch`, `uv add opencv`, or similar while trying to explain deferred integrations. [VERIFIED: existing boundary test pattern in `tests/test_readme_contract.py`]  
**Why it happens:** Boundary docs often list future integrations near setup instructions. [ASSUMED]  
**How to avoid:** Separate “Install and Test” from “Deferred integrations,” and extend tests that reject heavy terms in install command lines. [VERIFIED: `tests/test_readme_contract.py`]  
**Warning signs:** Any line starting with `pip install`, `uv add`, or `uv pip install` contains real backend, ROS, Habitat, CUDA, tensor/CV, UI, or provider terms. [VERIFIED: `tests/test_readme_contract.py`]

### Pitfall 4: Optional Extras Policy Mutates `pyproject.toml`
**What goes wrong:** Planner adds placeholder extras like `[project.optional-dependencies] cuda = []` with no real integration. [VERIFIED: D-15 forbids this]  
**Why it happens:** Python packaging supports optional extras, so contributors may over-eagerly encode future policy as metadata. [CITED: https://packaging.python.org/en/latest/specifications/pyproject-toml/; ASSUMED]  
**How to avoid:** In Phase 08, describe optional extras policy in `CONTRIBUTING.md` only; leave `dependencies = []` and no placeholder extras. [VERIFIED: D-15; `pyproject.toml`]  
**Warning signs:** `pyproject.toml` changes outside documentation/test needs, or docs refer to installable extras that do not correspond to real optional integrations. [VERIFIED: D-15]

### Pitfall 5: Real Backend Guidance Crosses From Contract Boundary Into Implementation Recipe
**What goes wrong:** Contributor docs start telling users how to wire CUDA/native backend internals into Mosaic. [VERIFIED: D-17 forbids detailed real backend implementation instructions]  
**Why it happens:** Backend registry and contract helpers exist, making it tempting to write a backend tutorial. [VERIFIED: `tests/slam/test_backend_registry.py`; `tests/slam/test_backend_contract_helpers.py`]  
**How to avoid:** Stop at descriptor metadata, dependency availability checks, registry/adapter seams, and contract helper obligations. [VERIFIED: D-17]  
**Warning signs:** Docs mention importing heavy backend packages in core modules or bypassing availability checks. [VERIFIED: `tests/slam/test_backend_registry.py`]

## Code Examples

Verified patterns from project tests and official docs:

### Contract Test for Split Docs
```python
# Source: tests/test_readme_contract.py; pytest assert docs
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_split_docs_exist_and_are_linked_from_readme() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    for relative_path in ("docs/API.md", "docs/EXAMPLES.md", "CONTRIBUTING.md"):
        assert (ROOT / relative_path).exists()
        assert relative_path in readme
```
Plain Python `assert` is the pytest-native way to check test expectations, with assertion introspection on failure. [CITED: https://docs.pytest.org/en/stable/how-to/assert.html]

### Golden Path Artifact Test
```python
# Source: tests/evaluation/test_runner.py; pytest tmp_path docs
from mosaic import DeterministicSplatBackend, FrameId, run_slam_benchmark, synthetic_forward_sequence
from mosaic import write_benchmark_artifact


def test_documented_golden_path_writes_local_artifact(tmp_path) -> None:
    artifact = run_slam_benchmark(
        scenario=synthetic_forward_sequence(frame_count=3),
        backend=DeterministicSplatBackend(map_frame=FrameId("map")),
    )
    output = tmp_path / "mosaic-benchmark.json"

    write_benchmark_artifact(artifact, output)

    assert artifact.scenario_name == "synthetic-forward-3"
    assert artifact.backend_name == "deterministic-splat"
    assert output.read_text(encoding="utf-8").endswith("\n")
```
`tmp_path` gives each test a unique temporary directory as a `pathlib.Path`. [CITED: https://docs.pytest.org/en/stable/how-to/tmp_path.html]

### Backend Boundary Contributor Check
```python
# Source: tests/slam/test_backend_registry.py
from mosaic.slam import BackendRegistry, DeterministicSplatBackend


def test_docs_do_not_bypass_backend_registry() -> None:
    registry = BackendRegistry()
    # Contributor docs should describe registering descriptors and checking availability
    # before creating optional backend instances.
    assert registry.names == ()
    assert DeterministicSplatBackend().name == "deterministic-splat"
```
The real plan should reference actual descriptor and availability examples from `tests/slam/test_backend_registry.py`. [VERIFIED: `tests/slam/test_backend_registry.py`]

### Representation Memory Endpoint for Golden Path
```python
# Source: tests/agents/test_representation_memory.py
from mosaic import FrameId, RepresentationMemory
from mosaic.agents import CellState, ClaimId, SpatialCell

memory = RepresentationMemory.empty(frame=FrameId("map")).with_cell(
    SpatialCell(
        frame=FrameId("map"),
        coordinate=(1, 2),
        resolution=0.5,
        state=CellState.FRONTIER,
        traversability=0.75,
        claim_ids=(ClaimId("claim-1"),),
    )
)
frontiers = memory.query_navigation_frontiers(max_results=1)
assert frontiers.total_matches == 1
```
Representation memory query outputs are bounded and expose truncation metadata through `MemoryQueryResult`. [VERIFIED: `tests/agents/test_representation_memory.py`]

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| README as phase-baseline orientation | Split v1 release docs: concise README, API doc, examples doc, contributor guide | Phase 08 locked decision on 2026-05-21 | Planner must create or update multiple docs and link them from README. [VERIFIED: `08-CONTEXT.md`] |
| README says representation memories/tools remain planned | Docs should describe `RepresentationMemory` and tool-style query families as implemented provider-free contracts | After Phase 7 completion by 2026-05-21 | Planner must remove stale “planned” wording for Phase 7 agent memory layer. [VERIFIED: `tests/test_public_api.py`; `src/mosaic/__init__.py`; `README.md`] |
| Basic README contract tests only | Split-doc contract tests over headings, commands, boundary terms, and example API paths | Phase 08 plan target | Planner should either extend `tests/test_readme_contract.py` or add neighboring `tests/test_docs_contract.py`. [VERIFIED: D-05; `tests/test_readme_contract.py`] |
| Optional integrations discussed informally | Contributor policy says heavy future integrations are optional, isolated, and not placeholder extras | Phase 08 locked decision | Planner must not add fake extras to `pyproject.toml`. [VERIFIED: D-15; `pyproject.toml`] |

**Deprecated/outdated:**
- “Phase 1 baseline” as public framing: replace with “Mosaic v1 foundation.” [VERIFIED: D-13; `README.md`]
- “Phase 7 representation memories/tools remain planned”: replace with implemented-layer language for `RepresentationMemory` while preserving the distinction from `SplatPosteriorView`. [VERIFIED: D-12; `tests/test_public_api.py`]
- Public docs that omit explicit deferred terms for real 3DGS, ROS, Habitat, UI/WebSockets, LLM/LVLM providers, CUDA/native stacks, and production SLAM quality. [VERIFIED: D-10]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | `tests/test_docs_contract.py` is a good filename if planner adds a new split-doc test file. | Recommended Project Structure | Low: planner may instead extend `tests/test_readme_contract.py`, which is allowed by D-05. |
| A2 | Boundary docs often drift into install instructions when future integrations are listed near setup instructions. | Common Pitfalls | Low: existing test pattern already guards the practical failure mode. |
| A3 | `tomllib` can be used for structured `pyproject.toml` checks if string checks become brittle. | Standard Stack / Supporting | Low: planner can keep existing string checks and avoid `tomllib`. |

## Open Questions (RESOLVED)

1. **Should docs include `mosaic.artifacts` as a public API surface?**
   - What we know: `src/mosaic/artifacts/__init__.py` exports artifact conversion helpers, and the final plan treats artifact writers/converters as documented release API support for evaluation and serialization. [VERIFIED: package export scan; `08-CONTEXT.md`; final Phase 08 plans]
   - RESOLVED: Include artifact writers and artifact helper APIs as documented API support, placed under evaluation/serialization or artifact-helper wording in `docs/API.md` rather than as a separate product surface. This preserves DOCS-01/02 coverage without hiding supported writer/helper APIs. [VERIFIED: final Phase 08 plan choices]

2. **Should the golden path use `SplatPosteriorView` only or both `SplatPosteriorView` and `RepresentationMemory`?**
   - What we know: DOCS-02 says “agent posterior query,” while D-07 says the path should end with a representation-memory/tool-style query. [VERIFIED: `.planning/REQUIREMENTS.md`; `08-CONTEXT.md`]
   - RESOLVED: Use both sequentially. The golden path first uses `SplatPosteriorView` for bounded splat-posterior access from the benchmark snapshot/result, then uses `RepresentationMemory` for the higher provider-free memory/tool-style query endpoint. [VERIFIED: D-07; D-12; final Phase 08 plans]

3. **Should doc tests execute code blocks from Markdown?**
   - What we know: D-09 says the golden path need not be a standalone tutorial program; existing tests validate representative API paths directly in Python. [VERIFIED: D-09; `tests/test_readme_contract.py`]
   - RESOLVED: Do not execute Markdown code blocks in Phase 08. Use deterministic pytest contract tests that read Markdown for required claims and separately exercise representative API behavior such as benchmark artifact writing and bounded memory queries. [VERIFIED: D-05; D-09; final Phase 08 plans]

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| Python | Running examples and tests | ✓ | `python 3.14.4` local; project requires `>=3.12` | Use configured `uv` Python if local shell Python differs. [VERIFIED: local command; `pyproject.toml`] |
| uv | `uv sync`, `uv run pytest -q` commands in docs | ✓ | 0.10.10 | Direct `python -m pytest` works locally but docs should keep `uv` as the project-standard command. [VERIFIED: local command; `CLAUDE.md`] |
| pytest | Doc-contract and full test suite | ✓ | `uv run pytest` reports 9.0.3; dev dependency is `pytest>=8.4.0` | None needed. [VERIFIED: local command; `pyproject.toml`] |
| Network / external services | Phase 08 implementation | Not required | — | Use local docs/tests only. [VERIFIED: phase context] |
| CUDA/native CV/ROS/Habitat/provider SDKs | Deferred integrations only | Not required | — | Document as out of v1 core scope; do not install. [VERIFIED: D-10; `pyproject.toml`] |

**Missing dependencies with no fallback:** none for Phase 08. [VERIFIED: environment audit]

**Missing dependencies with fallback:** none required; direct `python -m pytest` exists but is not the documented project command. [VERIFIED: environment audit; `CLAUDE.md`]

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest, dev dependency `pytest>=8.4.0`; `uv run pytest --version` reports 9.0.3 locally. [VERIFIED: `pyproject.toml`; local command] |
| Config file | `pyproject.toml` with `testpaths = ["tests"]` and `pythonpath = ["src"]`. [VERIFIED: `pyproject.toml`] |
| Quick run command | `uv run pytest tests/test_readme_contract.py tests/test_public_api.py -q` [VERIFIED: existing tests] |
| Full suite command | `uv run pytest -q` [VERIFIED: `README.md`; `pyproject.toml`] |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|--------------|
| DOCS-01 | Public docs name implemented foundation APIs and explicitly distinguish deferred real backend, ROS, Habitat, UI/WebSockets, LLM/LVLM, CUDA/native stacks, and production SLAM quality. | unit/doc contract | `uv run pytest tests/test_readme_contract.py -q` initially; add/extend split-doc tests | ✅ existing README test; ❌ split-doc coverage needs Wave 0/implementation. [VERIFIED: `tests/test_readme_contract.py`] |
| DOCS-02 | Golden path includes deterministic replay/scenario, deterministic backend, splat snapshot or benchmark result, local benchmark artifact, posterior query, and representation-memory query. | unit/doc contract + API smoke | `uv run pytest tests/evaluation/test_runner.py tests/agents/test_representation_memory.py tests/test_readme_contract.py -q` | ✅ API behavior tests exist; ❌ public doc golden-path assertion needs Phase 08. [VERIFIED: listed tests] |
| DOCS-03 | Contributor docs explain dependency policy, optional extras policy, test commands, and backend registry/adapter seams. | unit/doc contract | `uv run pytest tests/test_readme_contract.py -q` or new `tests/test_docs_contract.py -q` | ❌ `CONTRIBUTING.md` and split-doc tests need Phase 08. [VERIFIED: file listing] |

### Sampling Rate
- **Per task commit:** `uv run pytest tests/test_readme_contract.py tests/test_public_api.py -q` [VERIFIED: current test layout]
- **Per wave merge:** `uv run pytest -q` [VERIFIED: project command]
- **Phase gate:** Full suite green before `/gsd:verify-work`; docs must pass both content checks and existing public API behavior checks. [VERIFIED: GSD workflow; `pyproject.toml`]

### Wave 0 Gaps
- [ ] `tests/test_readme_contract.py` — update stale Phase 1/Phase 7 expectations to v1 release wording. [VERIFIED: current file]
- [ ] `tests/test_docs_contract.py` or equivalent additions — cover `docs/API.md`, `docs/EXAMPLES.md`, and `CONTRIBUTING.md`. [ASSUMED filename; VERIFIED need from D-05]
- [ ] `CONTRIBUTING.md` — missing contributor policy doc required by D-04/DOCS-03. [VERIFIED: file listing]
- [ ] `docs/API.md` — missing split API doc required by D-03/DOCS-01. [VERIFIED: file listing]
- [ ] `docs/EXAMPLES.md` — missing golden-path doc required by D-03/DOCS-02. [VERIFIED: file listing]

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|------------------|
| V2 Authentication | no | No auth/session surface in Phase 08 docs-only scope. [VERIFIED: phase context; codebase docs] |
| V3 Session Management | no | No sessions, cookies, or web runtime in v1 core docs. [VERIFIED: D-10; `pyproject.toml`] |
| V4 Access Control | no | No multi-user service or authorization layer in docs-only scope. [VERIFIED: phase context] |
| V5 Input Validation | yes | Preserve documented dataclass/protocol validation behavior and pytest examples using `pytest.raises`; doc examples should not bypass constructors. [VERIFIED: `CLAUDE.md`; tests under `tests/core`, `tests/agents`, `tests/slam`] |
| V6 Cryptography | no | No cryptography or secret-handling changes in Phase 08. [VERIFIED: phase context; `pyproject.toml`] |

### Known Threat Patterns for Documentation and Dependency Policy

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Dependency confusion through suggested install of future heavy packages | Tampering / Elevation of Privilege | Do not recommend unneeded external packages; keep `dependencies = []`; future optional integrations must use explicit extras and availability checks. [VERIFIED: `pyproject.toml`; D-15; CITED: https://packaging.python.org/en/latest/specifications/pyproject-toml/] |
| Misleading production-quality claims for deterministic fake backend | Spoofing / Repudiation | Docs must say deterministic backend, scenarios, gates, and fusion strategy are contract/reference fixtures, not production SLAM or real Gaussian optimization. [VERIFIED: D-11] |
| Provider/robot runtime coupling via examples | Information Disclosure / Tampering | Keep examples provider-free, local, deterministic, and bounded; no ROS/Habitat/UI/LLM SDK imports. [VERIFIED: D-10; `tests/test_readme_contract.py`] |
| Raw map dump exposure in agent-facing docs | Information Disclosure | Document bounded posterior and memory query outputs with truncation/provenance rather than raw full splat dumps. [VERIFIED: `CLAUDE.md`; `tests/agents/test_splat_posterior.py`; `tests/agents/test_representation_memory.py`] |

## Sources

### Primary (HIGH confidence)
- `/home/prannayag/pragnition/robotics/mosaic/.planning/phases/08-documentation-and-release-readiness/08-CONTEXT.md` — locked Phase 08 decisions, canonical refs, boundaries, and discretion areas. [VERIFIED]
- `/home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md` — DOCS-01, DOCS-02, DOCS-03 and v1 out-of-scope requirements. [VERIFIED]
- `/home/prannayag/pragnition/robotics/mosaic/.planning/STATE.md` — current phase status and deferred v2 items. [VERIFIED]
- `/home/prannayag/pragnition/robotics/mosaic/CLAUDE.md` — project constraints, stack, conventions, and workflow guidance. [VERIFIED]
- `/home/prannayag/pragnition/robotics/mosaic/pyproject.toml` — package metadata, empty runtime dependencies, dev pytest dependency, pytest config. [VERIFIED]
- `/home/prannayag/pragnition/robotics/mosaic/README.md` — current public docs and stale wording requiring rewrite. [VERIFIED]
- `/home/prannayag/pragnition/robotics/mosaic/src/mosaic/__init__.py` and package `__init__.py` export lists — current public API surfaces. [VERIFIED]
- `/home/prannayag/pragnition/robotics/mosaic/tests/test_readme_contract.py` — existing doc-contract test pattern. [VERIFIED]
- `/home/prannayag/pragnition/robotics/mosaic/tests/test_public_api.py` — current public root and subpackage API expectations. [VERIFIED]
- `/home/prannayag/pragnition/robotics/mosaic/tests/evaluation/test_runner.py` — benchmark artifact and writer patterns. [VERIFIED]
- `/home/prannayag/pragnition/robotics/mosaic/tests/agents/test_representation_memory.py` — representation-memory query behavior and bounded outputs. [VERIFIED]
- `/home/prannayag/pragnition/robotics/mosaic/tests/slam/test_backend_registry.py` and `tests/slam/test_backend_contract_helpers.py` — registry, availability, and contract-helper guidance. [VERIFIED]
- https://docs.pytest.org/en/stable/how-to/assert.html — pytest plain assert and assertion introspection. [CITED]
- https://docs.pytest.org/en/stable/how-to/tmp_path.html — pytest `tmp_path` fixture behavior. [CITED]
- https://packaging.python.org/en/latest/specifications/pyproject-toml/ — `dependencies` and `optional-dependencies` metadata. [CITED]
- https://docs.astral.sh/uv/concepts/projects/locking-and-syncing/ — `uv sync` and `uv run` environment behavior. [CITED]

### Secondary (MEDIUM confidence)
- Local command probes for `uv`, `python`, and `pytest` availability. [VERIFIED: local environment]
- Package export summary generated from local `__all__` lists. [VERIFIED: local code scan]

### Tertiary (LOW confidence)
- Filename recommendation `tests/test_docs_contract.py` if planner chooses a new split-doc test file. [ASSUMED]
- Use of `tomllib` for structured `pyproject.toml` checks if needed. [ASSUMED]

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — Phase uses existing Python/uv/pytest/Markdown stack verified from project metadata, local tools, and official docs. [VERIFIED]
- Architecture: HIGH — Locked decisions define split docs and doc tests; current tests show the established pattern. [VERIFIED]
- Pitfalls: HIGH for stale wording and dependency-boundary pitfalls verified in current README/tests; MEDIUM for generic docs-install drift based partly on assumed documentation failure modes. [VERIFIED; ASSUMED]

**Research date:** 2026-05-21  
**Valid until:** 2026-06-20 for project-specific doc architecture; re-check tool versions and README/test state after any Phase 08 implementation begins. [ASSUMED]
