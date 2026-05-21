# Contributing to Mosaic v1 foundation

Mosaic v1 foundation is a typed, headless Python library for multi-view Gaussian-splatting SLAM contracts. Contributions must keep the core pure Python, provider-free, robot-runtime-free, and explicit about what is a contract fixture versus what is deferred integration work.

This guide is contributor-facing release policy. It is not a tutorial for building production reconstruction backends.

## Dependency boundary

The core runtime dependency policy is exactly:

```toml
dependencies = []
```

That line in `pyproject.toml` is intentional. Core imports must not require CUDA/native stacks, tensor libraries, computer-vision bindings, ROS, Habitat, UI/WebSockets services, LLM/LVLM providers, robot SDKs, or real 3DGS backend packages.

If a change requires a new runtime package for the core library, assume the design is wrong until proven otherwise. Keep heavy or environment-specific functionality behind protocols, registries, adapters, availability checks, and downstream packages.

## Optional extras policy

Optional extras are policy-only for the Mosaic v1 foundation release. Future heavy integrations must be optional and isolated, but placeholder extras must not be added until a real optional integration exists. The optional extras policy is documentation-only for v1.

Do not add fake `[project.optional-dependencies]` entries such as CUDA, ROS, Habitat, LLM, UI, or backend extras just to reserve names. Optional metadata should appear only when there is a real optional integration with a maintained boundary, tests, and availability behavior.

Out of v1 core scope: real 3DGS backends, ROS, Habitat, UI/WebSockets, LLM/LVLM providers, CUDA/native stacks, and production SLAM quality. Downstream projects can wrap Mosaic later; Mosaic core owns stable typed representation contracts first.

## Public API stability

Public API additions must keep export and documentation surfaces synchronized. For any new public symbol or behavior, update:

- package `__all__` exports in the owning subpackage
- root export decisions where relevant in `mosaic.__all__`
- `docs/API.md`
- `README.md` if the public entry point or golden-path orientation changes
- `tests/test_public_api.py`
- doc contract tests that lock release-facing behavior and boundary terms

Prefer explicit package-rooted imports such as `from mosaic.core import FrameId` or selected root exports from `mosaic`. Do not add wildcard imports, private helper exports, or undocumented public surfaces.

## Test workflow

Use the project-standard `uv` workflow:

```bash
uv sync
uv run pytest tests/test_readme_contract.py -q
uv run pytest -q
```

Run targeted tests for the area you touched before running the full suite. Documentation changes that alter public release claims should also run the relevant doc contract tests. API changes should run `tests/test_public_api.py` in addition to the full suite.

The test workflow is part of the release contract. Do not replace it with a different local-vs-CI entry point unless the project configuration changes in the same review and the docs/tests are updated together.

## Real backend boundary

Real backend contributors must stop at the registry/adapter seam in Mosaic core. The allowed v1 contribution surface is policy and contracts:

- descriptor metadata such as `BackendDescriptor` or equivalent descriptor metadata
- backend capability metadata that can be inspected without importing heavy packages
- registry registration through the backend registry seam
- adapter boundaries that keep heavy implementation details outside core contracts
- availability checks that report missing optional requirements before backend creation
- `skip_unavailable_backend` or equivalent contract helper gates for optional backends
- contract tests that prove lifecycle, deterministic replay expectations where applicable, and state-update behavior

Do not add CUDA/native implementation instructions to Mosaic v1 docs. Do not import heavy backend packages from core modules. Do not bypass availability checks. Do not describe deterministic fixtures as production SLAM, real Gaussian optimization, calibrated uncertainty minimization, or reconstruction-quality mapping.

`DeterministicSplatBackend`, deterministic scenarios, benchmark gates, and `ProvenancePreservingFusion` are contract/reference fixtures for tests, examples, replay validation, and regression gates. They are not real backend implementations.
