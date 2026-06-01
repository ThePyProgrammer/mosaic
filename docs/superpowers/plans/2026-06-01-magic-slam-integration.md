# MAGiC-SLAM Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a CPU-safe MAGiC-SLAM integration shell that runs upstream MAGiC out of process and exposes a clean Mosaic backend descriptor.

**Architecture:** Keep MAGiC behind a standard-library-only `mosaic.slam.magic` module. The runner builds and executes `python <magic_repo>/run_slam.py ...`, discovers known MAGiC output files, and returns typed results. The descriptor lets callers register `magic-slam` without importing CUDA/PyTorch/Open3D packages.

**Tech Stack:** Python 3.12 standard library, existing Mosaic dataclasses/protocols/registry, pytest.

---

## File Structure

- Create `src/mosaic/slam/magic.py`: config, runner, run result, backend shell, descriptor factory.
- Modify `src/mosaic/slam/__init__.py`: export MAGiC integration symbols from `mosaic.slam`.
- Create `tests/slam/test_magic_integration.py`: CPU-safe tests using fake MAGiC scripts and temporary directories.

## Tasks

### Task 1: Runner Config and Command Builder

**Files:**
- Create: `tests/slam/test_magic_integration.py`
- Create: `src/mosaic/slam/magic.py`

- [ ] **Step 1: Write failing tests**

Add tests for `MagicSlamConfig` validation and command construction:

```python
def test_magic_config_rejects_missing_repo_config_and_input_paths(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="magic_repo"):
        MagicSlamConfig(
            magic_repo=tmp_path / "missing-repo",
            config_path=tmp_path / "config.yaml",
            input_path=tmp_path / "input",
            output_path=tmp_path / "output",
        )
```

```python
def test_runner_builds_upstream_magic_command(tmp_path: Path) -> None:
    repo = _fake_magic_repo(tmp_path)
    config_path = tmp_path / "config.yaml"
    input_path = tmp_path / "input"
    config_path.write_text("seed: 0\n")
    input_path.mkdir()
    cfg = MagicSlamConfig(
        magic_repo=repo,
        config_path=config_path,
        input_path=input_path,
        output_path=tmp_path / "out",
        python_executable="python-test",
        seed=7,
        multi_gpu=True,
    )

    assert MagicSlamRunner(cfg).build_command() == (
        "python-test",
        str(repo / "run_slam.py"),
        str(config_path),
        "--input_path",
        str(input_path),
        "--output_path",
        str(tmp_path / "out"),
        "--seed",
        "7",
        "--multi_gpu",
    )
```

- [ ] **Step 2: Run tests and verify failure**

Run: `uv run pytest tests/slam/test_magic_integration.py -q`
Expected: import or name failure because `mosaic.slam.magic` does not exist.

- [ ] **Step 3: Implement config and command builder**

Create `MagicSlamConfig`, `MagicSlamRunner.build_command`, and helper validation.

- [ ] **Step 4: Run tests and verify pass**

Run: `uv run pytest tests/slam/test_magic_integration.py -q`
Expected: passing tests for config and command builder.

### Task 2: Runner Execution and Artifact Discovery

**Files:**
- Modify: `tests/slam/test_magic_integration.py`
- Modify: `src/mosaic/slam/magic.py`

- [ ] **Step 1: Write failing tests**

Add fake upstream scripts for success and failure. Verify `MagicSlamRunner.run()` returns `MagicSlamRunResult`, captures outputs, and discovers known artifacts:

```python
def test_runner_executes_fake_magic_and_discovers_artifacts(tmp_path: Path) -> None:
    repo = _fake_magic_repo(tmp_path, script_body=_success_script_body())
    config = _valid_config(tmp_path, repo)

    result = MagicSlamRunner(config).run()

    assert result.success is True
    assert result.returncode == 0
    assert "merged_refined_ply" in result.artifacts
    assert result.diagnostics["returncode"] == 0
    assert result.diagnostics["artifact_count"] >= 2
    assert result.diagnostics["walltime_registration_time"] == pytest.approx(1.25)
```

```python
def test_runner_reports_subprocess_failure(tmp_path: Path) -> None:
    repo = _fake_magic_repo(tmp_path, script_body="import sys\nprint('bad', file=sys.stderr)\nsys.exit(3)\n")
    config = _valid_config(tmp_path, repo)

    result = MagicSlamRunner(config).run()

    assert result.success is False
    assert result.returncode == 3
    assert "bad" in result.stderr
    assert result.diagnostics["returncode"] == 3
```

- [ ] **Step 2: Run tests and verify failure**

Run: `uv run pytest tests/slam/test_magic_integration.py -q`
Expected: failures because `run()` and artifact discovery are not implemented.

- [ ] **Step 3: Implement runner execution**

Implement `MagicSlamRunResult`, `MagicSlamRunner.run`, known artifact discovery, and scalar JSON diagnostics.

- [ ] **Step 4: Run tests and verify pass**

Run: `uv run pytest tests/slam/test_magic_integration.py -q`
Expected: all MAGiC integration tests pass.

### Task 3: Backend Descriptor and Exports

**Files:**
- Modify: `tests/slam/test_magic_integration.py`
- Modify: `src/mosaic/slam/magic.py`
- Modify: `src/mosaic/slam/__init__.py`

- [ ] **Step 1: Write failing tests**

Add tests for descriptor availability and exports:

```python
def test_magic_descriptor_reports_missing_repo_without_importing_heavy_deps(tmp_path: Path) -> None:
    descriptor = magic_slam_backend_descriptor(
        magic_repo=tmp_path / "missing",
        config_path=tmp_path / "config.yaml",
        input_path=tmp_path / "input",
        output_path=tmp_path / "out",
    )

    availability = descriptor.check_availability()

    assert availability.available is False
    assert "magic_repo" in availability.missing_requirements
    assert descriptor.name == "magic-slam"
    assert descriptor.runs_out_of_process is True
```

```python
def test_magic_descriptor_factory_creates_runner_backed_backend(tmp_path: Path) -> None:
    repo = _fake_magic_repo(tmp_path)
    config = _valid_config(tmp_path, repo)
    descriptor = magic_slam_backend_descriptor(
        magic_repo=config.magic_repo,
        config_path=config.config_path,
        input_path=config.input_path,
        output_path=config.output_path,
    )

    backend = descriptor.factory()

    assert isinstance(backend, MagicSlamBackend)
    assert backend.name == "magic-slam"
    assert backend.capabilities.runs_out_of_process is True
```

- [ ] **Step 2: Run tests and verify failure**

Run: `uv run pytest tests/slam/test_magic_integration.py -q`
Expected: failures because descriptor/backend/export symbols do not exist.

- [ ] **Step 3: Implement descriptor/backend/export symbols**

Implement `MagicSlamBackend`, `magic_slam_backend_descriptor`, custom availability behavior, and update `mosaic.slam.__all__`.

- [ ] **Step 4: Run targeted and full tests**

Run:

```bash
uv run pytest tests/slam/test_magic_integration.py tests/slam/test_backend_registry.py -q
uv run pytest -q
```

Expected: targeted tests and full suite pass.
