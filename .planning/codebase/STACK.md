# Technology Stack

**Analysis Date:** 2026-05-18

## Languages

**Primary:**
- Python 3.12+ - The package requires Python `>=3.12` in `pyproject.toml:9`; local development pins `3.12` in `.python-version:1`.

**Secondary:**
- Markdown - Planning and research documentation in `docs/argus-migration-plan.md` and `outputs/arna-2506-17462-replication.md`.
- TOML - Project/build metadata in `pyproject.toml`.

## Runtime

**Environment:**
- CPython 3.12 - Implied by `.python-version` and `requires-python = ">=3.12"` in `pyproject.toml`.
- Headless Python library runtime - The design explicitly avoids UI/WebSocket/demo concerns in `docs/argus-migration-plan.md:12` and focuses on `src/mosaic/` as a library package.

**Package Manager:**
- uv is implied by the build backend dependency `uv_build>=0.10.10,<0.11.0` in `pyproject.toml:13`.
- Lockfile: missing. No `uv.lock`, `poetry.lock`, `Pipfile.lock`, or requirements lock file is present under `/home/prannayag/pragnition/robotics/mosaic`.

## Frameworks

**Core:**
- No application framework detected - `src/mosaic/__init__.py` currently exposes only `hello() -> str`.
- Planned package architecture is a typed Python library for 3D Gaussian Splatting SLAM, with proposed namespaces listed in `docs/argus-migration-plan.md:91-103`.

**Testing:**
- Not detected - no `pytest`, `unittest`, `hypothesis`, `tox`, `nox`, or test configuration is declared in `pyproject.toml`.
- Testing discipline is planned but not implemented: unit tests, backend contract tests, dataset replay tests, platform tests, evaluation tests, and agent API tests are described in `docs/argus-migration-plan.md:159-166`.

**Build/Dev:**
- `uv_build>=0.10.10,<0.11.0` - Build backend declared in `pyproject.toml:12-14`.
- `py.typed` - Package marker at `src/mosaic/py.typed` declares type information for downstream type checkers.
- No formatter/linter/type-checker configuration detected - no Ruff, Black, mypy, Pyright, or pytest settings are currently present in `pyproject.toml` or sibling config files.

## Key Dependencies

**Critical:**
- None currently declared - `dependencies = []` in `pyproject.toml:10`.
- Future Gaussian Splatting SLAM dependencies are intentionally undecided; `docs/argus-migration-plan.md:170` states the Gaussian splatting backend choice is not selected.

**Infrastructure:**
- `uv_build>=0.10.10,<0.11.0` - Required only for packaging/building via `pyproject.toml:13`.
- No runtime infrastructure dependencies are installed or declared in the project metadata.

**Implied but absent for the stated Mosaic direction:**
- Numerical arrays/tensors: no `numpy`, `torch`, `jax`, or `scipy` dependency is present, despite planned pose, camera, splat, and posterior data structures in `docs/argus-migration-plan.md:109-127`.
- Computer vision / geometry: no `opencv-python`, `open3d`, `trimesh`, `viser`, `rerun-sdk`, `gsplat`, `nerfstudio`, or COLMAP wrapper is present.
- Robotics/simulation: no ROS, Habitat, MuJoCo, Isaac, or robot SDK dependency is present; robot platform abstractions are planned in `docs/argus-migration-plan.md:129-137` but intentionally not tied to Go2/MuJoCo in `docs/argus-migration-plan.md:84-87`.
- Agent/LLM integration: no OpenAI, Anthropic, LangChain, or tool-calling SDK is present; agent posterior APIs are planned as a thin seam in `docs/argus-migration-plan.md:149-157`.

## Configuration

**Environment:**
- Python version is configured by `.python-version` with value `3.12`.
- Package metadata is configured in `pyproject.toml` with project name `mosaic`, version `0.1.0`, README `README.md`, and author metadata.
- No `.env` or `.env.*` files are present at repository root from the safe existence-only scan.
- No runtime environment variables are required by current code in `src/mosaic/__init__.py`.

**Build:**
- `pyproject.toml` is the only detected build configuration file.
- Build backend: `uv_build` from `pyproject.toml:14`.
- Source package root: `src/mosaic/`.
- Typed package marker: `src/mosaic/py.typed`.

## Platform Requirements

**Development:**
- Python 3.12 or newer.
- A build frontend compatible with PEP 517 and `uv_build`.
- No GPU/CUDA requirement exists in the current package metadata.
- Future backend work may require CUDA/native libraries; `docs/argus-migration-plan.md:30-36` calls out CUDA-heavy and crash-prone Gaussian splatting backends as a design concern.

**Production:**
- Deployment target not detected.
- Current shape is a distributable Python library package, not a service, CLI, notebook, web app, or robot runtime deployment.
- Future production-like deployments are expected to consume Mosaic headlessly from downstream robot, dataset, evaluation, or agent systems rather than from code currently in this repository.

---

*Stack analysis: 2026-05-18*
