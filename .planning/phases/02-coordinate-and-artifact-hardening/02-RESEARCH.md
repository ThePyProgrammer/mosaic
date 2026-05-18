# Phase 2: Coordinate and Artifact Hardening - Research

**Researched:** 2026-05-18 [VERIFIED: system date]
**Domain:** Typed Python coordinate-frame semantics, Gaussian covariance validation, and versioned JSON-ready artifact contracts [VERIFIED: .planning/ROADMAP.md]
**Confidence:** HIGH for codebase state and local test architecture; MEDIUM for external convention alignment because Mosaic must still choose exact public wording [VERIFIED: codebase][CITED: https://www.ros.org/reps/rep-0103.html]

## User Constraints

No CONTEXT.md exists for this phase; the user explicitly selected "Continue without context". Research scope is constrained by `.planning/REQUIREMENTS.md`, `.planning/STATE.md`, `.planning/ROADMAP.md`, `CLAUDE.md`, and live code patterns. [VERIFIED: user prompt][VERIFIED: gsd-sdk init.phase-op]

### Locked Decisions

- Phase 2 must address SEM-01, SEM-02, SEM-03, ART-01, and ART-02. [VERIFIED: user prompt][VERIFIED: .planning/REQUIREMENTS.md]
- Mosaic v1 must remain a typed, headless, pure-Python library foundation without required CUDA/PyTorch/OpenCV/ROS/Habitat/LLM dependencies. [VERIFIED: CLAUDE.md][VERIFIED: .planning/REQUIREMENTS.md]
- Real 3DGS backend integration is deferred until contracts and regression gates exist. [VERIFIED: .planning/STATE.md][VERIFIED: .planning/REQUIREMENTS.md]
- Phase 2 depends on Phase 1 and should harden the merged main-checkout baseline rather than reimplementing Phase 1 modules. [VERIFIED: .planning/ROADMAP.md]

### Claude's Discretion

- No explicit CONTEXT.md discretion section exists. [VERIFIED: gsd-sdk init.phase-op]
- Research recommends pure-standard-library implementations for transform math and artifact serialization unless a future discussion overrides this. [VERIFIED: pyproject.toml][ASSUMED]

### Deferred Ideas (OUT OF SCOPE)

- Real 3DGS backend integration, CUDA/PyTorch/OpenCV as required dependencies, LLM/LVLM provider integration, ROS nodes, Habitat/ARNA reproduction, browser UI/WebSockets/demos, occupancy-grid-first map models, and vendor-calibrated platform presets are out of scope for v1. [VERIFIED: .planning/REQUIREMENTS.md]
- Backend registry metadata and availability checks belong to Phase 3, not Phase 2. [VERIFIED: .planning/ROADMAP.md]
- Fusion uncertainty/conflict diagnostics belong to Phase 4, richer evaluation failure classification belongs to Phase 5, and richer posterior summaries belong to Phase 6. [VERIFIED: .planning/ROADMAP.md]

## Summary

Phase 2 is a hardening phase over an already-merged typed Python foundation: current modules include `mosaic.core`, `mosaic.splats`, `mosaic.slam`, `mosaic.evaluation`, `mosaic.fusion`, `mosaic.platforms`, `mosaic.datasets`, and `mosaic.agents`, and the local suite currently passes with 73 tests under `uv run pytest -q`. [VERIFIED: codebase][VERIFIED: uv run pytest -q] The implemented baseline already has immutable dataclasses for timestamps, frame IDs, camera intrinsics, poses, observations, Gaussian splats, splat maps, backend updates, and benchmark artifacts, but pose semantics are underspecified and `Pose3` currently has no compose/invert/apply helpers. [VERIFIED: codebase]

The planner should treat this as a semantics-locking phase: document and test the exact coordinate contract before downstream fusion/evaluation phases rely on it. [VERIFIED: .planning/STATE.md][VERIFIED: .planning/ROADMAP.md] Use ROS REP 103 as the external convention anchor for right-handed robot frames and camera optical axes, but encode Mosaic’s chosen meaning directly in public docstrings/tests so users do not have to infer it from ROS. [CITED: https://www.ros.org/reps/rep-0103.html][ASSUMED]

**Primary recommendation:** Add a small `mosaic.artifacts` serialization layer plus targeted core/splat transform hardening, using only Python dataclasses, tuples, enums, `json`, and pytest round-trip tests; do not add schema-generation or numeric dependencies in this phase. [VERIFIED: pyproject.toml][CITED: https://docs.python.org/3/library/json.html][ASSUMED]

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| SEM-01 | Pose direction, parent/child frame meaning, camera optical-frame convention, handedness, and timestamp precision are explicitly documented and tested. [VERIFIED: .planning/REQUIREMENTS.md] | Use REP 103 right-handed/body/optical axes as convention anchor and add docstrings/tests around `FrameId`, `Timestamp`, `Pose3`, and `CameraIntrinsics.project`. [CITED: https://www.ros.org/reps/rep-0103.html][VERIFIED: codebase] |
| SEM-02 | Core pose/camera utilities include tested transform composition, inversion, and point transformation semantics needed by downstream fusion and evaluation. [VERIFIED: .planning/REQUIREMENTS.md] | `Pose3` currently stores frames/translation/quaternion but lacks operations; planner should add quaternion rotation, pose inverse, composition, and point application tests. [VERIFIED: codebase] |
| SEM-03 | Gaussian covariance layout and validity semantics are documented and covered by edge-case tests. [VERIFIED: .planning/REQUIREMENTS.md] | `GaussianSplat.covariance_upper` currently uses six values interpreted as `(xx, xy, xz, yy, yz, zz)` and validates positive diagonal plus positive-definiteness determinants; harden with explicit docs and edge tests. [VERIFIED: codebase] |
| ART-01 | Core values, observations, splats, maps, backend updates, and evaluation results have versioned JSON-ready artifact schemas. [VERIFIED: .planning/REQUIREMENTS.md] | Existing `BenchmarkArtifact.as_dict()` is narrow evaluation JSON; add a broader v1 artifact envelope and per-type serializer/deserializer helpers. [VERIFIED: codebase] |
| ART-02 | Serialization round-trip tests cover timestamps, poses, camera observations, Gaussian splats, splat maps, and backend updates. [VERIFIED: .planning/REQUIREMENTS.md] | Existing tests only cover benchmark JSON-readiness and metric dictionaries; add round-trip tests for all required value families. [VERIFIED: codebase] |
</phase_requirements>

## Project Constraints (from CLAUDE.md)

- Use Python 3.12+, `uv`, pure-Python foundation modules, and `pytest`; keep the core importable without CUDA/native dependencies. [VERIFIED: CLAUDE.md]
- Keep real 3DGS/CUDA/research backends behind protocols, registries, optional dependencies, and future isolation boundaries. [VERIFIED: CLAUDE.md]
- Nail down coordinate frames, pose direction, handedness, optical frame conventions, and timestamp precision early because downstream fusion, evaluation, and agent queries can silently disagree. [VERIFIED: CLAUDE.md]
- Do evaluation/regression infrastructure before real backend integration. [VERIFIED: CLAUDE.md]
- Agent APIs must return bounded typed outputs with evidence/provenance, not raw full splat maps or provider-specific prompts. [VERIFIED: CLAUDE.md]
- Use `src/` package layout and package imports rooted at `mosaic`, not relative imports. [VERIFIED: CLAUDE.md]
- Keep public APIs typed and type-checker-friendly because `src/mosaic/py.typed` exists. [VERIFIED: CLAUDE.md][VERIFIED: codebase]
- Validate dataclass invariants in `__post_init__()` and raise domain-specific `ValueError`; use `pytest.raises(..., match="...")` for validation tests. [VERIFIED: CLAUDE.md][CITED: https://docs.pytest.org/en/stable/how-to/assert.html]
- Prefer immutable tuples for fixed-size geometric data and sequences; avoid mutating caller-owned objects. [VERIFIED: CLAUDE.md]
- Maintain explicit `__all__` lists in public package modules; do not use wildcard imports. [VERIFIED: CLAUDE.md][VERIFIED: codebase]
- Prefer deterministic JSON formatting with `json.dumps(..., indent=2, sort_keys=True) + "\n"`. [VERIFIED: CLAUDE.md][CITED: https://docs.python.org/3/library/json.html]
- Avoid `print()` in library code and return typed diagnostics mappings instead of logging side effects. [VERIFIED: CLAUDE.md]

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Coordinate-frame semantics | Python library core | Tests/docs | `mosaic.core` owns `FrameId`, `Timestamp`, `Pose3`, and camera projection contracts used by datasets, SLAM, platforms, fusion, evaluation, and agents. [VERIFIED: codebase] |
| Pose composition/inversion/application | Python library core | Tests | Transform operations are domain value-object behavior and should not live in evaluation or backend adapters. [VERIFIED: codebase][ASSUMED] |
| Camera optical-frame convention | Python library core | Platform presets/tests | `CameraIntrinsics.project()` already assumes positive camera depth; platform camera rigs reference `Pose3` camera frames. [VERIFIED: codebase] |
| Gaussian covariance layout/validity | Splat contract layer | Tests/docs | `GaussianSplat` is the primitive contract consumed by maps, SLAM updates, fusion, evaluation, and agent posterior views. [VERIFIED: codebase] |
| Versioned artifact schemas | Serialization/artifact layer | Existing value modules | Versioning is cross-cutting across core, observations, splats, backend updates, and evaluation results; use a dedicated serializer layer to avoid polluting geometry operations. [VERIFIED: codebase][ASSUMED] |
| Benchmark artifact distinction | Evaluation layer | Artifact layer | Existing `BenchmarkArtifact` is an evaluation-run output, while Phase 2 ART-01 requires broader v1 artifacts for many value families. [VERIFIED: codebase][VERIFIED: .planning/ROADMAP.md] |

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python standard library `dataclasses` | Python 3.12 project runtime | Frozen typed value objects, `__post_init__()` validation, and immutable-ish records. [VERIFIED: pyproject.toml][CITED: https://docs.python.org/3/library/dataclasses.html] | Already used throughout Mosaic and supports generated equality/hash behavior for frozen dataclasses. [VERIFIED: codebase][CITED: https://docs.python.org/3/library/dataclasses.html] |
| Python standard library `json` | Python 3.12 project runtime | Deterministic JSON encoding for JSON-ready artifacts. [VERIFIED: pyproject.toml][CITED: https://docs.python.org/3/library/json.html] | Existing benchmark writer uses `json.dumps(..., indent=2, sort_keys=True) + "\n"`, and Python docs state `sort_keys=True` sorts dictionaries by key. [VERIFIED: codebase][CITED: https://docs.python.org/3/library/json.html] |
| Python standard library `enum.StrEnum` | Python 3.12 project runtime | Stable string-valued enums for image encodings and tracking states. [VERIFIED: codebase][CITED: https://docs.python.org/3/library/enum.html] | Existing `ImageEncoding` and `TrackingState` use `StrEnum`, keeping serialized enum values human-readable. [VERIFIED: codebase] |
| `pytest` | 9.0.3 via `uv run pytest --version` | Unit and round-trip tests. [VERIFIED: uv run pytest --version] | Existing test suite uses pytest and currently passes 73 tests. [VERIFIED: uv run pytest -q] |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| JSON Schema concepts | Draft 2019-09+ concepts for `unevaluatedProperties`; no runtime dependency recommended. [CITED: https://json-schema.org/understanding-json-schema/reference/object][ASSUMED] | Shape the artifact envelope vocabulary: `type`, `properties`, `required`, and controlled extra fields. [CITED: https://json-schema.org/understanding-json-schema/reference/object] | Use as documentation/design language, not as a required validator package in Phase 2. [ASSUMED] |
| ROS REP 103 conventions | Specification page, not package. [CITED: https://www.ros.org/reps/rep-0103.html] | Coordinate convention anchor: right-handed frames; body axes x-forward/y-left/z-up; camera optical axes z-forward/x-right/y-down. [CITED: https://www.ros.org/reps/rep-0103.html] | Use to define Mosaic’s convention clearly without importing ROS. [ASSUMED] |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Handwritten artifact dictionaries | `pydantic` or `msgspec` [ASSUMED] | These add runtime dependencies, conflict with Phase 2’s pure-Python/no-heavy-dependency posture, and are unnecessary for small stable value objects. [VERIFIED: pyproject.toml][ASSUMED] |
| Handwritten transform math | `numpy`/`scipy.spatial.transform` [ASSUMED] | External numeric packages would simplify matrix/quaternion math but add dependencies absent from project metadata; Phase 2 operations are small enough for standard-library math with tests. [VERIFIED: pyproject.toml][ASSUMED] |
| ROS coordinate libraries | ROS TF packages [ASSUMED] | ROS is explicitly out of scope for v1; use REP 103 as a cited convention only. [VERIFIED: .planning/REQUIREMENTS.md][CITED: https://www.ros.org/reps/rep-0103.html] |

**Installation:**

```bash
# No new runtime dependencies recommended for Phase 2. [VERIFIED: pyproject.toml][ASSUMED]
uv sync
```

**Version verification:**

```bash
uv run python --version      # observed Python 3.12.13 [VERIFIED: uv run python --version]
uv run pytest --version     # observed pytest 9.0.3 [VERIFIED: uv run pytest --version]
uv --version                # observed uv 0.10.10 [VERIFIED: uv --version]
```

## Package Legitimacy Audit

No external packages are recommended for installation in Phase 2, so the Package Legitimacy Gate is not applicable. [VERIFIED: pyproject.toml][ASSUMED]

| Package | Registry | Age | Downloads | Source Repo | slopcheck | Disposition |
|---------|----------|-----|-----------|-------------|-----------|-------------|
| none | — | — | — | — | — | No package install recommended. [ASSUMED] |

**Packages removed due to slopcheck [SLOP] verdict:** none. [ASSUMED]
**Packages flagged as suspicious [SUS]:** none. [ASSUMED]

## Architecture Patterns

### System Architecture Diagram

```text
User code / tests
      |
      v
mosaic.core value objects
(FrameId, Timestamp, Pose3, CameraIntrinsics, observations)
      |                       \
      | transform/project      \ serialize v1 artifact payloads
      v                         v
mosaic.splats primitives ---> mosaic.artifacts (new pure-Python layer)
(GaussianSplat, SplatMap)        |
      |                          | versioned envelope + typed payload
      v                          v
mosaic.slam updates --------> JSON-ready dicts / stable JSON files
(SplatSlamUpdate)                |
      |                          v
      +--------------------> round-trip tests for equality and invariants
      |
      v
mosaic.evaluation benchmark artifacts
(existing narrow BenchmarkArtifact JSON remains distinct from broader v1 schema)
```

This diagram reflects current module boundaries plus the recommended new artifact layer. [VERIFIED: codebase][ASSUMED]

### Recommended Project Structure

```text
src/mosaic/
├── core/                 # Existing coordinate, timestamp, pose, camera, observation contracts. [VERIFIED: codebase]
├── splats/               # Existing GaussianSplat and SplatMap contracts. [VERIFIED: codebase]
├── slam/                 # Existing SplatSlamUpdate and backend protocol contracts. [VERIFIED: codebase]
├── evaluation/           # Existing BenchmarkArtifact and metric output. [VERIFIED: codebase]
└── artifacts/            # Recommended new versioned artifact serializers. [ASSUMED]

tests/
├── core/                 # Extend coordinate and transform semantics tests. [VERIFIED: codebase][ASSUMED]
├── splats/               # Extend covariance layout/edge tests. [VERIFIED: codebase][ASSUMED]
└── artifacts/            # Recommended new JSON-ready round-trip tests. [ASSUMED]
```

### Pattern 1: Explicit Pose Direction Contract

**What:** Define `Pose3(parent_frame=A, child_frame=B)` as the transform that maps coordinates expressed in child frame B into parent frame A, commonly written `T_parent_child`. [ASSUMED]
**When to use:** Use for camera-in-world, rig-in-base, backend estimated pose, and transform composition boundaries. [VERIFIED: codebase][ASSUMED]
**Example:**

```python
# Source: Mosaic existing Pose3 shape plus recommended semantics. [VERIFIED: codebase][ASSUMED]
pose_world_camera = Pose3(
    parent_frame=FrameId("world"),
    child_frame=FrameId("camera/front_optical"),
    translation=Translation3(1.0, 0.0, 0.0),
    rotation=Quaternion.identity(),
)
assert pose_world_camera.apply_to_point((0.0, 0.0, 2.0)) == (1.0, 0.0, 2.0)
```

### Pattern 2: Frame Compatibility Before Math

**What:** `compose()` should reject mismatched frames before performing rotation/translation math. [ASSUMED]
**When to use:** Every pose composition path; silent mismatches are more dangerous than loud `ValueError` failures. [VERIFIED: CLAUDE.md][ASSUMED]
**Example:**

```python
# Source: recommended Mosaic API shape; no current compose method exists. [VERIFIED: codebase][ASSUMED]
world_base.compose(base_camera)      # valid when world_base.child_frame == base_camera.parent_frame
world_base.compose(camera_object)    # invalid when frames do not connect; raise ValueError
```

### Pattern 3: Versioned Artifact Envelope

**What:** Every serialized artifact should include an explicit schema name/version and a payload whose fields are JSON-supported primitives. [CITED: https://docs.python.org/3/library/json.html][CITED: https://json-schema.org/understanding-json-schema/reference/object][ASSUMED]
**When to use:** For `Timestamp`, `Pose3`, `CameraObservation`, `GaussianSplat`, `SplatMap`, `SplatSlamUpdate`, `MetricResult`, `RegressionResult`, and `BenchmarkArtifact`. [VERIFIED: codebase][VERIFIED: .planning/REQUIREMENTS.md]
**Example:**

```python
# Source: Python json docs for primitive JSON mappings; envelope is recommended for Mosaic v1. [CITED: https://docs.python.org/3/library/json.html][ASSUMED]
{
    "schema": "mosaic.pose3",
    "schema_version": 1,
    "payload": {
        "parent_frame": "world",
        "child_frame": "camera/front_optical",
        "translation": [1.0, 0.0, 0.0],
        "rotation_wxyz": [1.0, 0.0, 0.0, 0.0],
    },
}
```

### Pattern 4: Covariance Layout as Contract, Not Naming Hint

**What:** Treat `covariance_upper` as the upper-triangular storage of a symmetric 3x3 covariance matrix in `(xx, xy, xz, yy, yz, zz)` order. [VERIFIED: codebase]
**When to use:** All splat construction, docs, serializers, and tests. [VERIFIED: codebase][ASSUMED]
**Example:**

```python
# Source: current GaussianSplat unpacking order. [VERIFIED: codebase]
xx, xy, xz, yy, yz, zz = splat.covariance_upper
matrix = (
    (xx, xy, xz),
    (xy, yy, yz),
    (xz, yz, zz),
)
```

### Anti-Patterns to Avoid

- **Adding NumPy/SciPy just for a few transforms:** The project currently has no runtime dependencies, and Phase 2 can implement 3D tuple/quaternion helpers with standard-library `math`. [VERIFIED: pyproject.toml][ASSUMED]
- **Leaving pose direction implicit:** Current tests only assert parent/child fields are stored; downstream users need transform direction and frame compatibility tests. [VERIFIED: codebase][VERIFIED: .planning/REQUIREMENTS.md]
- **Serializing dataclasses via `__dict__`:** Slots/frozen dataclasses, enums, mappings, tuples, bytes, and nested value objects need explicit stable payload conversions. [VERIFIED: codebase][CITED: https://docs.python.org/3/library/json.html]
- **Conflating benchmark artifacts with all v1 artifacts:** Existing `BenchmarkArtifact` only covers scenario/backend/update_count/metrics; Phase 2 requires broad schemas for core values, observations, splats, maps, backend updates, and evaluation results. [VERIFIED: codebase][VERIFIED: .planning/REQUIREMENTS.md]
- **Base64-encoding images casually without documenting it:** `ImageBuffer.data` is bytes, which is not a default JSON type, so any image artifact must define an explicit encoding policy. [VERIFIED: codebase][CITED: https://docs.python.org/3/library/json.html][ASSUMED]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| General JSON parser/formatter | Custom string concatenation | Python `json.dumps` / `json.loads` | Python docs define deterministic key sorting and supported JSON mappings. [CITED: https://docs.python.org/3/library/json.html] |
| Test exception checking | Manual try/except flags | `pytest.raises(..., match="...")` | Pytest documents context-manager exception assertions with regex matching. [CITED: https://docs.pytest.org/en/stable/how-to/assert.html] |
| Generic schema-validator runtime | New dependency in Phase 2 | Handwritten typed serializers with documented schema names/versions | Project has no runtime dependencies and phase scope can stay pure Python. [VERIFIED: pyproject.toml][ASSUMED] |
| Coordinate convention invention | Private undocumented axis choices | REP 103-aligned wording plus Mosaic tests | REP 103 specifies right-handed frames and camera optical axes. [CITED: https://www.ros.org/reps/rep-0103.html] |
| Positive-definite covariance guesswork | Checking only positive diagonal | Existing determinant checks plus edge tests for principal minors | Positive-definiteness for symmetric matrices is tied to positive leading principal minors. [VERIFIED: codebase][CITED: https://en.wikipedia.org/wiki/Sylvester%27s_criterion] |

**Key insight:** The hard part is not the math volume; it is freezing semantics so future fusion, evaluation, backend, and agent work cannot interpret the same tuple differently. [VERIFIED: .planning/STATE.md][ASSUMED]

## Common Pitfalls

### Pitfall 1: Pose Direction Ambiguity

**What goes wrong:** One caller treats `Pose3(parent, child)` as parent-to-child while another treats it as child-to-parent. [ASSUMED]
**Why it happens:** Current `Pose3` stores `parent_frame` and `child_frame` but has no documented direction or transform methods. [VERIFIED: codebase]
**How to avoid:** Define one notation in docstrings and tests, e.g. `T_parent_child` maps child coordinates into parent coordinates. [ASSUMED]
**Warning signs:** Tests only assert field equality and do not transform a point through a non-zero translation/rotation. [VERIFIED: codebase]

### Pitfall 2: Quaternion Composition Order Bugs

**What goes wrong:** `A.compose(B)` applies rotations in the wrong order, producing correct identity tests but wrong rotated-point behavior. [ASSUMED]
**Why it happens:** Quaternion multiplication is order-sensitive. [ASSUMED]
**How to avoid:** Include non-commuting rotation tests and a translate-then-rotate point test. [ASSUMED]
**Warning signs:** Only identity-rotation tests exist. [VERIFIED: codebase]

### Pitfall 3: Optical Frame Convention Drift

**What goes wrong:** Projection math assumes positive z depth while camera rig docs imply x-forward robot frames. [VERIFIED: codebase][ASSUMED]
**Why it happens:** REP 103 uses body axes x-forward/y-left/z-up and camera optical axes z-forward/x-right/y-down, which are different frame conventions. [CITED: https://www.ros.org/reps/rep-0103.html]
**How to avoid:** Name optical frames explicitly or document when a `FrameId` is an optical frame; keep `CameraIntrinsics.project()` defined over optical-frame coordinates with positive z depth. [VERIFIED: codebase][ASSUMED]
**Warning signs:** Tests use `camera/front` but docs never say whether it is body or optical. [VERIFIED: codebase]

### Pitfall 4: Timestamp Float Round-Trip Loss

**What goes wrong:** A timestamp serialized as seconds float does not round-trip exactly to nanoseconds. [VERIFIED: codebase][ASSUMED]
**Why it happens:** Current canonical storage is integer nanoseconds; `as_seconds()` returns float. [VERIFIED: codebase]
**How to avoid:** Serialize timestamps as integer nanoseconds in artifacts and keep seconds as convenience display only. [VERIFIED: codebase][ASSUMED]
**Warning signs:** Artifact payloads store only `seconds`. [ASSUMED]

### Pitfall 5: Bytes Are Not JSON Primitives

**What goes wrong:** `ImageBuffer.data` fails JSON serialization or is represented inconsistently. [VERIFIED: codebase][CITED: https://docs.python.org/3/library/json.html]
**Why it happens:** Python `json` supports dict/list/tuple/str/int/float/bool/None by default, not bytes. [CITED: https://docs.python.org/3/library/json.html]
**How to avoid:** Define image artifacts with explicit `data_encoding`, likely base64 for bytes if image payload round-trip is required. [ASSUMED]
**Warning signs:** `json.dumps(camera_observation.__dict__)` or ad hoc `.hex()` without schema docs. [ASSUMED]

### Pitfall 6: Covariance Positive-Definite Edge Cases

**What goes wrong:** Tests accept positive diagonals but miss invalid off-diagonal correlations. [VERIFIED: codebase][ASSUMED]
**Why it happens:** Positive diagonal is necessary but not sufficient for a symmetric matrix to be positive definite. [CITED: https://en.wikipedia.org/wiki/Sylvester%27s_criterion]
**How to avoid:** Test zero determinant, negative determinant, too-large off-diagonal values, and near-boundary values. [VERIFIED: codebase][ASSUMED]
**Warning signs:** Only diagonal covariance examples appear in tests. [VERIFIED: codebase]

## Code Examples

Verified patterns from current project and official sources:

### Current Frozen Dataclass Validation Pattern

```python
# Source: current Mosaic code and Python dataclasses docs. [VERIFIED: codebase][CITED: https://docs.python.org/3/library/dataclasses.html]
@dataclass(frozen=True, slots=True)
class Timestamp:
    nanoseconds: int

    def __post_init__(self) -> None:
        if self.nanoseconds < 0:
            raise ValueError("Timestamp nanoseconds must be non-negative")
```

### Current Deterministic JSON Writer Pattern

```python
# Source: current BenchmarkArtifact writer and Python json docs. [VERIFIED: codebase][CITED: https://docs.python.org/3/library/json.html]
def write_benchmark_artifact(artifact: BenchmarkArtifact, path: Path) -> None:
    path.write_text(json.dumps(artifact.as_dict(), indent=2, sort_keys=True) + "\n")
```

### Recommended Round-Trip Test Shape

```python
# Source: pytest exception/assertion style docs plus Mosaic test style. [CITED: https://docs.pytest.org/en/stable/how-to/assert.html][VERIFIED: codebase][ASSUMED]
def test_pose_artifact_round_trips() -> None:
    pose = Pose3(
        parent_frame=FrameId("world"),
        child_frame=FrameId("camera/front_optical"),
        translation=Translation3(1.0, 2.0, 3.0),
        rotation=Quaternion.identity(),
    )

    payload = pose_to_artifact(pose)
    assert payload["schema"] == "mosaic.pose3"
    assert payload["schema_version"] == 1
    assert pose_from_artifact(payload) == pose
```

### Recommended Pose Composition Test Shape

```python
# Source: recommended semantics; current Pose3 has no compose method. [VERIFIED: codebase][ASSUMED]
def test_pose_composition_applies_child_then_parent() -> None:
    world_base = Pose3(FrameId("world"), FrameId("base"), Translation3(1.0, 0.0, 0.0), Quaternion.identity())
    base_camera = Pose3(FrameId("base"), FrameId("camera"), Translation3(0.0, 2.0, 0.0), Quaternion.identity())

    world_camera = world_base.compose(base_camera)

    assert world_camera.parent_frame == FrameId("world")
    assert world_camera.child_frame == FrameId("camera")
    assert world_camera.apply_to_point((0.0, 0.0, 0.0)) == (1.0, 2.0, 0.0)
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Implicit coordinate conventions in type names | Explicit semantic contracts with transform tests | Needed in Phase 2 before fusion/evaluation hardening [VERIFIED: .planning/ROADMAP.md] | Prevents downstream components from silently disagreeing. [VERIFIED: CLAUDE.md] |
| Narrow benchmark-only JSON | Versioned v1 artifact schemas for multiple value families | Needed in Phase 2 ART-01/ART-02 [VERIFIED: .planning/REQUIREMENTS.md] | Allows stable round-trips and separates evaluation outputs from general serialization. [VERIFIED: codebase][ASSUMED] |
| Runtime dependency convenience for transforms | Pure Python typed contracts | Current project constraint [VERIFIED: pyproject.toml][VERIFIED: CLAUDE.md] | Keeps core importable without native/GPU stacks. [VERIFIED: CLAUDE.md] |

**Deprecated/outdated:**

- Treating `BenchmarkArtifact.as_dict()` as the complete artifact schema is insufficient for Phase 2 because it only serializes benchmark scenario/backend/update_count/metrics. [VERIFIED: codebase][VERIFIED: .planning/REQUIREMENTS.md]
- Treating covariance layout as self-evident from `covariance_upper` is insufficient because downstream users need the exact six-value order and positive-definite rules. [VERIFIED: codebase][VERIFIED: .planning/REQUIREMENTS.md]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | A new `mosaic.artifacts` package is preferable to adding serializers directly into every existing module. | Architecture Patterns | Planner may choose a different organization; implementation remains possible but could scatter cross-cutting schema code. |
| A2 | Mosaic should define `Pose3(parent, child)` as `T_parent_child`, mapping child-frame points into parent-frame coordinates. | Architecture Patterns / Common Pitfalls | If user prefers inverse notation, transform helpers/tests would need inverted names and docs. |
| A3 | Phase 2 should not add `pydantic`, `msgspec`, `numpy`, or `scipy`. | Standard Stack | If user wants dependency-backed validation/math, pure-Python tasks may be too manual. |
| A4 | Image artifacts should use an explicit bytes encoding, likely base64, if `ImageBuffer.data` is round-tripped through JSON. | Common Pitfalls | Wrong encoding choice could affect artifact interoperability. |
| A5 | JSON Schema should be used as design vocabulary rather than a runtime validator dependency in Phase 2. | Standard Stack | If downstream consumers require formal `.schema.json` files now, planner must add tasks for schema documents. |

## Open Questions

1. **Should Phase 2 produce formal `.schema.json` files or only versioned Python artifact dictionaries?** [ASSUMED]
   - What we know: ART-01 says versioned JSON-ready artifact schemas, and JSON Schema object docs define `properties`, `required`, and property controls. [VERIFIED: .planning/REQUIREMENTS.md][CITED: https://json-schema.org/understanding-json-schema/reference/object]
   - What's unclear: The roadmap does not specify whether schemas must be machine-validated files. [VERIFIED: .planning/ROADMAP.md]
   - Recommendation: Start with explicit Python schema names/versions and round-trip tests; add formal schema files only if planner/user wants interoperability deliverables. [ASSUMED]
2. **Should existing `camera/front` frame IDs be renamed to `camera/front_optical` in tests/presets?** [ASSUMED]
   - What we know: REP 103 names optical-frame axes separately, and current tests use generic camera frame IDs. [CITED: https://www.ros.org/reps/rep-0103.html][VERIFIED: codebase]
   - What's unclear: No current Mosaic doc chooses naming conventions for optical frames. [VERIFIED: codebase]
   - Recommendation: Add docs and tests clarifying whether camera poses are optical poses; consider `_optical` suffix where projection is involved. [ASSUMED]
3. **Should `Timestamp.from_seconds()` continue using `round()`?** [VERIFIED: codebase]
   - What we know: Current code rounds seconds to nanoseconds. [VERIFIED: codebase]
   - What's unclear: Rounding policy for half-nanosecond values is not documented. [VERIFIED: codebase]
   - Recommendation: Document integer nanoseconds as canonical artifact representation and test exact known conversions; avoid artifact round-trips through float seconds. [ASSUMED]

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python via `uv run` | Project runtime/tests | yes | 3.12.13 [VERIFIED: uv run python --version] | System `python3` is 3.14.4 but project requires Python >=3.12; prefer `uv run`. [VERIFIED: python3 --version][VERIFIED: pyproject.toml] |
| `uv` | Dependency sync and test command | yes | 0.10.10 [VERIFIED: uv --version] | None needed. [VERIFIED: environment probe] |
| `pytest` in uv env | Validation Architecture | yes | 9.0.3 [VERIFIED: uv run pytest --version] | None needed. [VERIFIED: environment probe] |
| `json` stdlib | Artifact serialization | yes | Python stdlib [CITED: https://docs.python.org/3/library/json.html] | None needed. [CITED: https://docs.python.org/3/library/json.html] |

**Missing dependencies with no fallback:** none found. [VERIFIED: environment probe]

**Missing dependencies with fallback:** none found. [VERIFIED: environment probe]

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest 9.0.3 [VERIFIED: uv run pytest --version] |
| Config file | `pyproject.toml` with `testpaths = ["tests"]` and `pythonpath = ["src"]`. [VERIFIED: pyproject.toml] |
| Quick run command | `uv run pytest tests/core tests/splats tests/evaluation tests/slam -q` [ASSUMED] |
| Full suite command | `uv run pytest -q` [VERIFIED: uv run pytest -q] |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| SEM-01 | Pose direction, parent/child, optical convention, handedness, timestamp precision | unit/docs assertions | `uv run pytest tests/core/test_frames_and_poses.py tests/core/test_observations.py -q` | Existing files yes; semantic tests need additions. [VERIFIED: codebase][ASSUMED] |
| SEM-02 | Pose composition, inversion, point application, camera projection semantics | unit | `uv run pytest tests/core/test_frames_and_poses.py tests/core/test_observations.py -q` | Existing files yes; transform-operation tests missing. [VERIFIED: codebase] |
| SEM-03 | Gaussian covariance layout and edge-case validity | unit | `uv run pytest tests/splats/test_splat_map.py -q` | Existing file yes; edge tests need expansion. [VERIFIED: codebase][ASSUMED] |
| ART-01 | Versioned JSON-ready artifact schemas for value families | unit/schema | `uv run pytest tests/artifacts -q` | No; Wave 0 should create. [VERIFIED: codebase][ASSUMED] |
| ART-02 | Round-trip timestamps, poses, observations, splats, maps, backend updates | unit/round-trip | `uv run pytest tests/artifacts -q` | No; Wave 0 should create. [VERIFIED: codebase][ASSUMED] |

### Sampling Rate

- **Per task commit:** `uv run pytest tests/core tests/splats tests/artifacts -q` after artifact tests exist. [ASSUMED]
- **Per wave merge:** `uv run pytest -q`. [VERIFIED: current test command]
- **Phase gate:** Full suite green before `/gsd:verify-work`; current baseline is 73 passing tests. [VERIFIED: uv run pytest -q]

### Wave 0 Gaps

- [ ] `tests/artifacts/test_core_artifacts.py` — covers SEM-01 and ART-02 round-trips for `Timestamp`, `FrameId`, `Translation3`, `Quaternion`, `Pose3`, `CameraIntrinsics`, `ImageBuffer`, `CameraObservation`, and `MultiViewObservation`. [ASSUMED]
- [ ] `tests/artifacts/test_splat_artifacts.py` — covers SEM-03 and ART-02 round-trips for `GaussianSplat` and `SplatMap`. [ASSUMED]
- [ ] `tests/artifacts/test_slam_and_evaluation_artifacts.py` — covers ART-01/ART-02 for `SplatSlamUpdate`, `MetricResult`, `RegressionResult`, and `BenchmarkArtifact` distinction. [ASSUMED]
- [ ] Additional transform tests in `tests/core/test_frames_and_poses.py` for `Pose3.inverse()`, `Pose3.compose()`, and `Pose3.apply_to_point()`. [ASSUMED]
- [ ] Additional covariance edge tests in `tests/splats/test_splat_map.py` for upper-triangular order, determinant boundary, and off-diagonal invalid cases. [ASSUMED]

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | Mosaic Phase 2 has no auth/session surface. [VERIFIED: .planning/ROADMAP.md] |
| V3 Session Management | no | Mosaic is a headless Python library without web sessions. [VERIFIED: CLAUDE.md] |
| V4 Access Control | no | Phase 2 has no user/role authorization boundary. [VERIFIED: .planning/ROADMAP.md] |
| V5 Input Validation | yes | Dataclass `__post_init__()` validation plus explicit deserializer validation and pytest negative tests. [VERIFIED: codebase][CITED: https://docs.pytest.org/en/stable/how-to/assert.html] |
| V6 Cryptography | no | Phase 2 does not encrypt/sign artifacts; do not hand-roll crypto. [VERIFIED: .planning/ROADMAP.md][ASSUMED] |

### Known Threat Patterns for typed artifact serialization

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Malformed artifact payload accepted silently | Tampering | Validate schema name, schema version, required fields, enum values, frame strings, tuple lengths, numeric ranges, and covariance positive-definiteness before constructing dataclasses. [VERIFIED: codebase][ASSUMED] |
| Resource exhaustion from huge image byte payloads | Denial of Service | Keep existing `ImageBuffer` length validation and reject mismatched dimensions before allocating derived structures. [VERIFIED: codebase][ASSUMED] |
| Ambiguous artifact version causing wrong interpretation | Tampering | Include `schema` and `schema_version` in every top-level artifact and reject unknown versions. [ASSUMED] |
| Non-deterministic JSON ordering causing false regression diffs | Repudiation | Use `json.dumps(..., sort_keys=True, indent=2) + "\n"`. [VERIFIED: codebase][CITED: https://docs.python.org/3/library/json.html] |

## Sources

### Primary (HIGH confidence)

- `/home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md` — Phase 2 requirement definitions and v1 out-of-scope list. [VERIFIED: Read]
- `/home/prannayag/pragnition/robotics/mosaic/.planning/ROADMAP.md` — Phase 2 goal/success criteria and merged baseline evidence. [VERIFIED: Read]
- `/home/prannayag/pragnition/robotics/mosaic/.planning/STATE.md` — project decisions and Phase 2 concern. [VERIFIED: Read]
- `/home/prannayag/pragnition/robotics/mosaic/CLAUDE.md` — project constraints and coding conventions. [VERIFIED: Read]
- `/home/prannayag/pragnition/robotics/mosaic/src/mosaic/**` and `/home/prannayag/pragnition/robotics/mosaic/tests/**` — current implementation and test patterns. [VERIFIED: Read/Bash rg]
- `uv run pytest -q` — observed 73 passing tests. [VERIFIED: Bash]
- Python dataclasses docs — frozen dataclass and `__post_init__()` behavior. [CITED: https://docs.python.org/3/library/dataclasses.html]
- Python json docs — deterministic key sorting, indentation, and supported JSON mappings. [CITED: https://docs.python.org/3/library/json.html]
- Pytest assertion docs — `pytest.raises` context-manager and `match=` usage. [CITED: https://docs.pytest.org/en/stable/how-to/assert.html]
- ROS REP 103 — right-handed frames, body axes, and camera optical axes. [CITED: https://www.ros.org/reps/rep-0103.html]

### Secondary (MEDIUM confidence)

- JSON Schema object reference — schema object vocabulary and `unevaluatedProperties` note. [CITED: https://json-schema.org/understanding-json-schema/reference/object]
- Sylvester criterion reference — positive leading principal minors criterion for positive-definite symmetric matrices. [CITED: https://en.wikipedia.org/wiki/Sylvester%27s_criterion]
- ROS REP 145 — confirms right-handed sensor-frame expectation for IMU data; supporting context only. [CITED: https://www.ros.org/reps/rep-0145.html]

### Tertiary (LOW confidence)

- Recommendations about package organization (`mosaic.artifacts`), exact pose notation, and avoiding runtime schema/numeric dependencies are architectural judgments based on project constraints, not official Mosaic decisions. [ASSUMED]

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — current project metadata has no runtime dependencies, pytest is installed in the uv environment, and standard-library docs were checked. [VERIFIED: pyproject.toml][VERIFIED: environment probe][CITED: https://docs.python.org/3/library/json.html]
- Architecture: MEDIUM — codebase boundaries are verified, but the proposed `mosaic.artifacts` package and exact pose notation require user/planner acceptance. [VERIFIED: codebase][ASSUMED]
- Pitfalls: HIGH for current gaps in pose operations/artifact round-trips because code search found no transform methods or broad artifact serializers; MEDIUM for recommended mitigations because exact API names remain discretionary. [VERIFIED: codebase][ASSUMED]

**Research date:** 2026-05-18 [VERIFIED: system date]
**Valid until:** 2026-06-17 for codebase-local findings; re-check external package/tool versions before execution if dependencies are added. [ASSUMED]
