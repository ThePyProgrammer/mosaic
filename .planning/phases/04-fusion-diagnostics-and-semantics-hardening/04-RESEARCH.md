# Phase 04: fusion-diagnostics-and-semantics-hardening - Research

**Researched:** 2026-05-19 [VERIFIED: project config]
**Domain:** Pure-Python typed fusion diagnostics for immutable 3D Gaussian splat map snapshots [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md]
**Confidence:** HIGH [VERIFIED: codebase inspection]

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
## Implementation Decisions

### Diagnostic Shape
- **D-01:** Keep `FusionResult.diagnostics` as a JSON-ready machine-readable mapping, but add typed summary objects alongside it.
- **D-02:** Use fusion-prefixed summary names such as `FusionProvenanceSummary`, `FusionUncertaintySummary`, and `FusionConflictSummary` so these diagnostics do not blur into existing agent posterior summaries like `mosaic.agents.ProvenanceSummary`.
- **D-03:** Make provenance, uncertainty, and conflicts first-class typed fields on `FusionResult`; selected flat diagnostic keys should mirror key totals for artifact stability.
- **D-04:** Expose provenance detail as source map count, source splat count, fused splat count, and per-provenance counts. Do not add full per-output-splat lineage or stable splat IDs in this phase unless the existing model already supports them cleanly.

### Conflict Semantics
- **D-05:** Treat conservative overlap-plus-mismatch cases as fusion conflict candidates: nearby/overlapping splats from different provenance sources whose covariance, opacity, or color summaries disagree enough to be suspicious.
- **D-06:** Conflict detection should be deterministic and conservative. Prefer obvious center-distance/covariance-radius overlap plus mismatch over sensitive heuristics that create noisy false alarms.
- **D-07:** `FusionConflictSummary` should expose total conflict candidate count, involved provenance pairs, and reason counts such as overlap/color, overlap/opacity, or overlap/covariance mismatch. Avoid exposing individual splat-pair records unless required for tests.
- **D-08:** Conflicts remain diagnostics for the reference strategy. `ProvenancePreservingFusion` should still return `FusionStatus.FUSED` when conflicts are found because it preserves inputs rather than rejecting or optimizing them.

### Uncertainty Summary
- **D-09:** The exact reference-strategy uncertainty policy is delegated to downstream planning, but it should stay conservative and preserve the current "preserved, not optimized" meaning unless tests justify more.
- **D-10:** `FusionUncertaintySummary` should include a stable model label plus covariance diagonal range/stat summaries such as min, max, and mean. These are diagnostics over preserved source splats, not calibrated posterior-fusion claims.
- **D-11:** Phase 4 should prepare deterministic uncertainty fields for Phase 5 evaluation work, but should not add regression gates or threshold policy now.
- **D-12:** `ProvenancePreservingFusion` should communicate non-optimization through an explicit stable machine-readable label such as `preserved_not_optimized` in both the typed summary and flat diagnostics.

### Anti-Occupancy-Grid Tests
- **D-13:** The priority of the first anti-grid behavior test is delegated to downstream planning; choose behavior-focused tests that prove splat/posterior semantics rather than cosmetic API assertions.
- **D-14:** Include a conflict case where two overlapping splats from different provenance sources are both preserved in the fused output while conflict diagnostics record the mismatch.
- **D-15:** Verify the non-optimization boundary in both tests and a concise README/public-doc note: the reference strategy preserves and diagnoses splats but does not optimize Gaussians.
- **D-16:** Tests should assert both typed summary values and selected flat diagnostic keys so Python consumers and JSON/artifact consumers remain stable.

### Claude's Discretion
- The planner may choose the exact conservative uncertainty policy for `ProvenancePreservingFusion`, provided it preserves the explicit `preserved_not_optimized` boundary and does not claim real posterior optimization.
- The planner may choose the strongest initial anti-grid behavior test, provided it demonstrates splats are preserved as splats and not collapsed into occupancy cells.

### Deferred Ideas (OUT OF SCOPE)
## Deferred Ideas

None — discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| FUSE-02 | Fusion results preserve provenance, source-map diagnostics, uncertainty/conflict summaries, and machine-readable status. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md] | Add typed fusion summary dataclasses to `mosaic.fusion.protocol`, freeze internal mappings, populate summaries in `ProvenancePreservingFusion`, and mirror selected scalar totals into `FusionResult.diagnostics`. [VERIFIED: codebase inspection] |
| FUSE-04 | Fusion tests reject occupancy-grid union assumptions and verify provenance-preserving behavior. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md] | Extend `tests/fusion/test_strategies.py` with behavior tests that preserve overlapping splats, report conflict candidates, and assert `preserved_not_optimized` rather than grid/cell collapse. [VERIFIED: codebase inspection] |
</phase_requirements>

## Summary

Phase 04 should harden the existing `mosaic.fusion` contract, not replace it. `FusionInput`, `FusionResult`, `FusionStatus`, `SplatFusionStrategy`, and `ProvenancePreservingFusion` already exist, and the current reference strategy concatenates input splats into a new immutable `SplatMap` while reporting flat count diagnostics. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/fusion/protocol.py] [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/fusion/strategies.py]

The plan should add three frozen, fusion-prefixed summary contracts: `FusionProvenanceSummary`, `FusionUncertaintySummary`, and `FusionConflictSummary`. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md] These summaries should become first-class fields on `FusionResult`, while `diagnostics` remains a JSON-ready scalar mapping for artifact consumers. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md] Python's standard `json` encoder supports `dict`, `list`, `tuple`, `str`, `int`, `float`, booleans, and `None` by default, so flat diagnostic values should remain scalar or simple JSON-ready containers if the project expands `FusionMetricValue`. [CITED: https://docs.python.org/3.14/library/json.html]

Conflict and uncertainty outputs must be explicitly diagnostic. The official 3D Gaussian Splatting project describes scene representation with 3D Gaussians, interleaved optimization/density control, anisotropic covariance optimization, and visibility-aware anisotropic splatting; Phase 04 must not imply it performs that optimization. [CITED: https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/] The correct reference-strategy label is `preserved_not_optimized`, not the current hyphenated `preserved-not-optimized`, because CONTEXT locks that stable machine-readable label. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md]

**Primary recommendation:** Extend `mosaic.fusion.protocol` with frozen typed summaries, update `FusionResult` to carry them, populate conservative provenance/uncertainty/conflict summaries in `ProvenancePreservingFusion`, mirror stable scalar diagnostics, and add tests proving overlapping splats are preserved rather than occupancy-grid-unioned. [VERIFIED: codebase inspection]

## Project Constraints (from CLAUDE.md)

- Use Python 3.12+, `uv`, pure-Python foundation modules, and `pytest`; keep the core importable without CUDA/native dependencies. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Commit planning artifacts in the main checkout unless explicitly working in a worktree. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Keep real 3DGS/CUDA/research backends behind protocols, registries, optional dependencies, and eventual isolation boundaries. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Preserve frame semantics discipline; downstream fusion, evaluation, and agent queries can silently disagree if pose/frame conventions are loose. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Do evaluation gates before real backend integration; this phase should not integrate real 3DGS backends. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Agent APIs should return bounded typed outputs with evidence/provenance, not raw full splat maps or provider-specific prompts. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Use `src/` layout under `src/mosaic/` and package-root imports such as `from mosaic.fusion import ...`. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Public contracts should be typed, immutable-friendly dataclasses or protocols, with explicit `__all__` exports. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Prefer immutable tuples, `MappingProxyType`-frozen mappings, typed diagnostics, and no caller-owned object mutation. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]
- Avoid `print()` in library code; diagnostics should be returned as typed mappings/objects. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md]

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|--------------|----------------|-----------|
| Fusion result contract hardening | API / Backend library | Database / Storage representation | `FusionResult` is a pure-Python library API over immutable `SplatMap` snapshots, not UI, service, or storage code. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/fusion/protocol.py] |
| Provenance summary | API / Backend library | Database / Storage representation | Provenance counts are derived from `GaussianSplat.provenance` values inside `SplatMap` inputs. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/splats/primitives.py] |
| Uncertainty summary | API / Backend library | Database / Storage representation | Covariance diagonal stats are derived from `GaussianSplat.covariance_upper` without optimizer dependencies. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/splats/primitives.py] |
| Conflict candidate diagnostics | API / Backend library | Database / Storage representation | Overlap/mismatch candidates should be computed deterministically inside the reference fusion strategy and returned as diagnostics. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md] |
| Anti-occupancy-grid tests | API / Backend library | — | Tests should assert splat preservation behavior through public Python APIs, not raster/grid artifacts. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md] |
| README boundary note | Static documentation | API / Backend library | The README already documents the reference fusion strategy as not real Gaussian optimization and should be tightened with Phase 04 terminology. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/README.md] |

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python standard library `dataclasses` | Python 3.12+ project target; docs fetched from Python 3.14.5 | Frozen summary value objects and `FusionResult` contract fields | `@dataclass(frozen=True)` emulates immutability and `__post_init__()` is the standard hook for validation/normalization. [CITED: https://docs.python.org/3.14/library/dataclasses.html] |
| Python standard library `typing.Protocol` | Python 3.12+ project target; docs fetched from Python 3.14 | Preserve `SplatFusionStrategy` structural protocol | `Protocol` supports structural subtyping, and `@runtime_checkable` allows runtime presence checks without signature validation. [CITED: https://docs.python.org/3.14/library/typing.html] |
| Python standard library `types.MappingProxyType` | Python 3.12+ project target; docs fetched from Python 3.14 | Freeze summary count mappings and diagnostics copies | `MappingProxyType` is a read-only proxy for a mapping; copying before wrapping avoids dynamic mutation through the caller's original mapping. [CITED: https://docs.python.org/3.14/library/types.html#types.MappingProxyType] |
| Python standard library `enum.StrEnum` | Python 3.12+ project target | Keep `FusionStatus` string-valued status stable | Existing code already uses `StrEnum` for `FusionStatus`, matching project enum conventions. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/fusion/protocol.py] |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `pytest` [VERIFIED: PyPI + official docs + slopcheck OK] | PyPI latest 9.0.3; local `uv run pytest --version` reported 9.0.3 | Behavior and regression tests for fusion protocol and strategy | Use for `tests/fusion/test_fusion_protocol.py`, `tests/fusion/test_strategies.py`, and public API export tests. [CITED: https://docs.pytest.org/en/stable/how-to/assert.html] [VERIFIED: PyPI command] |
| `uv` | Local `uv 0.10.10` | Project environment and test runner | Use the existing `uv run pytest ...` workflow. [VERIFIED: environment probe] |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Frozen dataclasses | Pydantic models | Do not use; Pydantic would add runtime dependencies and conflict with the pure-Python foundation boundary. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/CLAUDE.md] |
| Pure-Python pairwise conflict scan | NumPy vectorization or spatial index | Do not use in this phase; NumPy/spatial indexes are unnecessary for deterministic small contract tests and would add dependency/scope. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/pyproject.toml] |
| Splat-preserving reference strategy | Occupancy grid / voxel union | Do not use; v1 explicitly excludes occupancy-grid-first map modeling, and Phase 04 requires anti-grid tests. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md] |
| Real Gaussian optimization | 3DGS optimizer backend | Do not use; real 3DGS backend integration is v2/deferred and official 3DGS optimization is qualitatively more complex than this reference strategy. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md] [CITED: https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/] |

**Installation:**

```bash
# No runtime package installation for Phase 04.
# Existing dev workflow:
uv sync
uv run pytest -q
```

**Version verification:** `uv --version` returned `uv 0.10.10`, `uv run pytest --version` returned `pytest 9.0.3`, `python3 --version` returned `Python 3.14.4`, and `pip index versions pytest` reported latest `pytest (9.0.3)`. [VERIFIED: environment probe]

## Package Legitimacy Audit

> Phase 04 should not add new runtime packages. `pytest` is already a development dependency in `pyproject.toml`, but it was still checked because the validation architecture depends on it. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/pyproject.toml]

| Package | Registry | Age | Downloads | Source Repo | slopcheck | Disposition |
|---------|----------|-----|-----------|-------------|-----------|-------------|
| `pytest` | PyPI | Existing mature project; exact age not fetched in this session [ASSUMED] | Not fetched in this session [ASSUMED] | `https://github.com/pytest-dev/pytest` from installed package metadata | OK [VERIFIED: slopcheck] | Approved as existing dev dependency [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/pyproject.toml] |

**Packages removed due to slopcheck [SLOP] verdict:** none. [VERIFIED: slopcheck]
**Packages flagged as suspicious [SUS]:** none. [VERIFIED: slopcheck]

## Architecture Patterns

### System Architecture Diagram

```text
FusionInput(maps=(SplatMap, ...))
        |
        v
Frame compatibility already validated by FusionInput
        |
        v
ProvenancePreservingFusion.fuse()
        |
        +--> Concatenate/preserve GaussianSplat objects without mutating inputs
        |
        +--> Derive FusionProvenanceSummary
        |       - source_map_count
        |       - source_splat_count
        |       - fused_splat_count
        |       - per_provenance_counts
        |
        +--> Derive FusionUncertaintySummary
        |       - model_label = preserved_not_optimized
        |       - covariance diagonal min/max/mean
        |
        +--> Conservative pairwise conflict scan
        |       - only different provenance sources
        |       - overlap via center distance and covariance diagonal radius proxy
        |       - reason counts for color/opacity/covariance mismatch
        |
        v
FusionResult(status=FUSED, fused_map, typed summaries, flat diagnostics)
        |
        +--> Python consumers use typed fields
        |
        +--> Artifact/JSON consumers use selected flat diagnostics
```

### Recommended Project Structure

```text
src/mosaic/
├── fusion/
│   ├── __init__.py        # Export fusion contracts and summaries
│   ├── protocol.py        # FusionInput, FusionResult, FusionStatus, summary dataclasses, protocol
│   └── strategies.py      # ProvenancePreservingFusion summary population and conflict scan
└── __init__.py            # Root exports only if summaries are stable package-level API

tests/
├── fusion/
│   ├── test_fusion_protocol.py  # Summary validation, freezing, result contract tests
│   └── test_strategies.py       # Provenance, uncertainty, conflict, anti-grid behavior tests
└── test_public_api.py           # Root export tests if root exports are added
```

### Pattern 1: Frozen Summary Dataclasses with Defensive Mapping Copies

**What:** Define summaries as `@dataclass(frozen=True, slots=True)` and wrap copied mappings with `MappingProxyType`. [CITED: https://docs.python.org/3.14/library/dataclasses.html] [CITED: https://docs.python.org/3.14/library/types.html#types.MappingProxyType]

**When to use:** Use for `FusionProvenanceSummary.per_provenance_counts`, `FusionConflictSummary.involved_provenance_pairs`, and `FusionConflictSummary.reason_counts`. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md]

**Example:**

```python
# Source: https://docs.python.org/3.14/library/dataclasses.html
# Source: https://docs.python.org/3.14/library/types.html#types.MappingProxyType
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping

@dataclass(frozen=True, slots=True)
class FusionProvenanceSummary:
    source_map_count: int
    source_splat_count: int
    fused_splat_count: int
    per_provenance_counts: Mapping[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.source_map_count < 0 or self.source_splat_count < 0 or self.fused_splat_count < 0:
            raise ValueError("FusionProvenanceSummary counts must be non-negative")
        for source, count in self.per_provenance_counts.items():
            if not source.strip():
                raise ValueError("FusionProvenanceSummary provenance names must not be blank")
            if count < 0:
                raise ValueError("FusionProvenanceSummary provenance counts must be non-negative")
        object.__setattr__(self, "per_provenance_counts", MappingProxyType(dict(self.per_provenance_counts)))
```

### Pattern 2: Typed Fields plus Flat Diagnostics Mirror

**What:** `FusionResult` should carry typed summaries for Python callers and mirror selected stable scalar totals into `diagnostics`. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md]

**When to use:** Use whenever a diagnostic is important enough to become part of the public contract but still needs JSON/artifact stability. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md]

**Example:**

```python
# Source: project Phase 04 CONTEXT.md D-01/D-03/D-16
return FusionResult(
    status=FusionStatus.FUSED,
    fused_map=fused_map,
    provenance=provenance_summary,
    uncertainty=uncertainty_summary,
    conflicts=conflict_summary,
    diagnostics={
        "source_map_count": provenance_summary.source_map_count,
        "source_splat_count": provenance_summary.source_splat_count,
        "fused_splat_count": provenance_summary.fused_splat_count,
        "fusion_uncertainty_model": uncertainty_summary.model_label,
        "fusion_conflict_candidate_count": conflict_summary.total_candidate_count,
    },
)
```

### Pattern 3: Conservative Diagnostic-Only Conflict Candidates

**What:** Pair splats from different provenance sources, determine obvious overlap using center distance and covariance diagonal scale, then count mismatch reasons for color, opacity, or covariance. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md]

**When to use:** Use inside `ProvenancePreservingFusion` only as a deterministic warning mechanism; conflicts do not change `FusionStatus.FUSED` in this phase. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md]

**Example:**

```python
# Source: project Phase 04 CONTEXT.md D-05 through D-08
# Recommended constants should be module-private and documented by tests.
_OVERLAP_RADIUS_SCALE = 2.0
_COLOR_MISMATCH_THRESHOLD = 0.5
_OPACITY_MISMATCH_THRESHOLD = 0.25
_COVARIANCE_MISMATCH_RATIO = 2.0
```

The exact thresholds are a planning decision, but they should be intentionally coarse to avoid noisy false alarms. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md]

### Anti-Patterns to Avoid

- **Adding full per-output-splat lineage:** Phase 04 explicitly says not to add full per-output-splat lineage or stable splat IDs unless the existing model supports them cleanly, and `GaussianSplat` currently has no stable ID field. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md] [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/splats/primitives.py]
- **Rejecting fusion because conflicts exist:** CONTEXT locks that conflicts are diagnostics for the reference strategy and should still return `FusionStatus.FUSED`. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md]
- **Hyphenated model label drift:** Current code uses `preserved-not-optimized`, but Phase 04 locks `preserved_not_optimized`; update tests and docs to prevent both spellings from drifting. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/fusion/strategies.py] [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md]
- **Occupancy-grid union semantics:** Requirements explicitly exclude an occupancy-grid-first map model and require tests that reject occupancy-grid union assumptions. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Immutable public result contracts | Custom mutable classes | Frozen dataclasses with `__post_init__()` validation | Standard library dataclasses already provide generated initialization, frozen behavior, slots, and post-init hooks. [CITED: https://docs.python.org/3.14/library/dataclasses.html] |
| Read-only diagnostic mappings | Custom dict wrapper | `types.MappingProxyType(dict(input_mapping))` | The standard type provides a read-only mapping proxy; copying first prevents caller-side mutation from leaking through the proxy. [CITED: https://docs.python.org/3.14/library/types.html#types.MappingProxyType] |
| Strategy interface | Abstract base class hierarchy | Existing `typing.Protocol` `SplatFusionStrategy` | Protocols support structural subtyping and match the existing project pattern. [CITED: https://docs.python.org/3.14/library/typing.html] [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/fusion/protocol.py] |
| Gaussian optimization | Ad hoc merge/optimization math | Explicitly do not optimize; label as `preserved_not_optimized` | Official 3DGS optimization involves anisotropic covariance optimization and density control, which is out of phase scope. [CITED: https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/] |
| JSON artifact structure | Free-form prose diagnostics | Stable scalar diagnostic keys mirrored from typed summaries | Python's JSON encoder handles standard scalar/container types; prose is harder to gate in tests. [CITED: https://docs.python.org/3.14/library/json.html] |

**Key insight:** The dangerous mistake is making a tiny reference concatenation strategy sound like probabilistic map fusion. Keep the algorithm boring, the diagnostics explicit, and the boundary label painfully clear. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md]

## Common Pitfalls

### Pitfall 1: Turning diagnostics into behavior-changing policy

**What goes wrong:** Conflict candidates cause `FusionStatus.REJECTED` or splats are dropped/merged. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md]
**Why it happens:** Conflict detection looks like validation, but CONTEXT defines it as diagnostic-only for the reference strategy. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md]
**How to avoid:** Tests should assert `result.status is FusionStatus.FUSED` and both overlapping splats remain present even when conflict count is non-zero. [VERIFIED: codebase inspection]
**Warning signs:** Tests assert fewer fused splats than source splats in an overlap case. [VERIFIED: codebase inspection]

### Pitfall 2: Breaking artifact consumers by replacing `diagnostics`

**What goes wrong:** Typed summaries are added but flat diagnostic keys disappear. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md]
**Why it happens:** Developers treat typed fields as a replacement, but D-01 and D-16 require both typed and flat selected diagnostics. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md]
**How to avoid:** Assert typed values and selected flat keys in the same tests. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md]
**Warning signs:** `test_provenance_preserving_fusion_reports_diagnostics` only checks object fields or only checks dict values. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/tests/fusion/test_strategies.py]

### Pitfall 3: Using provenance names that collide with agent summaries

**What goes wrong:** A generic `ProvenanceSummary` is added in `mosaic.fusion`, creating confusion with `mosaic.agents.ProvenanceSummary`. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/agents/queries.py]
**Why it happens:** The project already has an agent-facing `ProvenanceSummary`. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/agents/queries.py]
**How to avoid:** Use `FusionProvenanceSummary`, `FusionUncertaintySummary`, and `FusionConflictSummary`. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md]
**Warning signs:** `from mosaic import ProvenanceSummary` becomes ambiguous in examples or public API docs. [VERIFIED: codebase inspection]

### Pitfall 4: MappingProxyType without copying

**What goes wrong:** A read-only proxy reflects later mutations to the original mutable dict. [CITED: https://docs.python.org/3.14/library/types.html#types.MappingProxyType]
**Why it happens:** `MappingProxyType` is a dynamic view of the underlying mapping. [CITED: https://docs.python.org/3.14/library/types.html#types.MappingProxyType]
**How to avoid:** Wrap `MappingProxyType(dict(input_mapping))`, matching the existing `FusionResult.diagnostics` pattern. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/fusion/protocol.py]
**Warning signs:** A test mutates the original dict after construction and the summary changes. [VERIFIED: codebase inspection]

### Pitfall 5: Overfitting conflict heuristics

**What goes wrong:** Tests depend on fragile thresholds or realistic covariance semantics that are not yet part of the contract. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md]
**Why it happens:** D-05/D-06 ask for conservative obvious candidates, not calibrated collision/registration math. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md]
**How to avoid:** Use very obvious test splats: same/near center, clearly different color or opacity, and different provenance. [VERIFIED: codebase inspection]
**Warning signs:** Tests need many decimal tolerances or assert exact physical overlap volumes. [ASSUMED]

## Code Examples

Verified patterns from official and project sources:

### Freeze Mapping Fields

```python
# Source: https://docs.python.org/3.14/library/types.html#types.MappingProxyType
# Source: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/fusion/protocol.py
object.__setattr__(self, "diagnostics", MappingProxyType(dict(self.diagnostics)))
```

### Pytest Exception Match

```python
# Source: https://docs.pytest.org/en/stable/how-to/assert.html
with pytest.raises(ValueError, match="same frame"):
    FusionInput(maps=(_map("map"), _map("other")))
```

### Anti-Grid Conflict Behavior Test Shape

```python
# Source: project Phase 04 CONTEXT.md D-14/D-16
result = ProvenancePreservingFusion().fuse(FusionInput(maps=(front_map, rear_map)))

assert result.status is FusionStatus.FUSED
assert len(result.fused_map.splats) == 2
assert [splat.provenance for splat in result.fused_map.splats] == ["front", "rear"]
assert result.conflicts.total_candidate_count == 1
assert result.diagnostics["fusion_conflict_candidate_count"] == 1
assert result.uncertainty.model_label == "preserved_not_optimized"
assert result.diagnostics["fusion_uncertainty_model"] == "preserved_not_optimized"
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Occupancy-grid-first map union | Splat/posterior-native immutable splat-map contracts | Locked in v1 requirements on 2026-05-18 [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md] | Phase 04 tests must prove splats are preserved and not collapsed into cells. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md] |
| Flat count-only fusion diagnostics | Typed provenance, uncertainty, and conflict summaries plus mirrored flat keys | Locked in Phase 04 CONTEXT on 2026-05-19 [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md] | Planner should add summary dataclasses and update tests/docs together. [VERIFIED: codebase inspection] |
| Reference strategy label `preserved-not-optimized` | Stable machine-readable label `preserved_not_optimized` | Locked in Phase 04 CONTEXT on 2026-05-19 [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md] | Tests should force the underscore spelling in typed and flat diagnostics. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/fusion/strategies.py] |

**Deprecated/outdated:**

- `uncertainty_model: "preserved-not-optimized"` is outdated for Phase 04; use `preserved_not_optimized`. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/fusion/strategies.py] [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md]
- Count-only diagnostics are insufficient for FUSE-02 because requirements explicitly include provenance, source-map diagnostics, uncertainty/conflict summaries, and machine-readable status. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Exact package age and download counts for `pytest` were not fetched in this session. | Package Legitimacy Audit | Low; `pytest` is already an existing dev dependency, slopcheck returned OK, and official docs were consulted. |
| A2 | Tests needing many decimal tolerances are a warning sign for overfit heuristics. | Common Pitfalls | Low; this is engineering judgment rather than a project-locked rule. |

## Open Questions

1. **Should fusion summary classes be root `mosaic` exports or only `mosaic.fusion` exports?**
   - What we know: Existing public API tests root-export `FusionInput` and `ProvenancePreservingFusion`. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/tests/test_public_api.py]
   - What's unclear: CONTEXT says new typed diagnostics should be stable if added, but does not explicitly require root exports. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md]
   - Recommendation: Export summaries from `mosaic.fusion`; add root exports only if tests/documentation need concise user-facing imports. [ASSUMED]

2. **What exact conflict thresholds should be used?**
   - What we know: Conflict detection must be deterministic and conservative, preferring obvious overlap plus mismatch. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md]
   - What's unclear: Numeric thresholds are delegated to planning/implementation. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md]
   - Recommendation: Use module-private constants with intentionally coarse values and test only obvious positives/negatives. [ASSUMED]

3. **Should `FusionMetricValue` expand beyond scalar values?**
   - What we know: It is currently `bool | int | float | str`, and selected flat diagnostic keys should mirror key totals. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/fusion/protocol.py] [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md]
   - What's unclear: Per-provenance counts are useful for diagnostics but may not fit the current scalar alias. [VERIFIED: codebase inspection]
   - Recommendation: Keep flat diagnostics scalar for artifact stability and put nested counts in typed summaries; add explicit `as_dict()` only if JSON artifacts need nested details later. [ASSUMED]

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| Python | Library and tests | yes | `python3 --version` returned 3.14.4; project requires >=3.12 | Use `uv` managed Python if local default differs. [VERIFIED: environment probe] |
| uv | Project workflow | yes | 0.10.10 | None needed. [VERIFIED: environment probe] |
| pytest | Validation | yes | 9.0.3 via `uv run pytest --version` | None needed. [VERIFIED: environment probe] |
| ctx7 | Documentation lookup | no | — | Official docs were fetched with WebFetch. [VERIFIED: environment probe] |

**Missing dependencies with no fallback:** none. [VERIFIED: environment probe]

**Missing dependencies with fallback:** `ctx7` was not installed; official documentation was fetched directly. [VERIFIED: environment probe]

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | `pytest` 9.0.3 [VERIFIED: environment probe] |
| Config file | `/home/prannayag/pragnition/robotics/mosaic/pyproject.toml` with `testpaths = ["tests"]` and `pythonpath = ["src"]` [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/pyproject.toml] |
| Quick run command | `uv run pytest tests/fusion -q` [VERIFIED: command run, 6 passed] |
| Full suite command | `uv run pytest -q` [VERIFIED: command run, 151 passed] |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| FUSE-02 | `FusionResult` exposes typed provenance/uncertainty/conflict summaries and stable mirrored flat diagnostics. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md] | unit | `uv run pytest tests/fusion/test_fusion_protocol.py -q` | yes, extend existing file [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/tests/fusion/test_fusion_protocol.py] |
| FUSE-02 | `ProvenancePreservingFusion` populates provenance counts, covariance diagonal stats, conflict reason counts, and `preserved_not_optimized`. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md] | unit | `uv run pytest tests/fusion/test_strategies.py -q` | yes, extend existing file [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/tests/fusion/test_strategies.py] |
| FUSE-04 | Overlapping mismatched splats from different provenance sources are both preserved while conflict diagnostics record the mismatch. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md] | unit | `uv run pytest tests/fusion/test_strategies.py -q` | yes, extend existing file [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/tests/fusion/test_strategies.py] |
| FUSE-04 | Public README states the reference strategy preserves/diagnoses splats and does not optimize Gaussians. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md] | documentation smoke/manual plus optional grep | `uv run pytest tests/fusion -q` plus planner may add doc assertion if desired | README exists [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/README.md] |

### Sampling Rate

- **Per task commit:** `uv run pytest tests/fusion -q` [VERIFIED: command run, 6 passed]
- **Per wave merge:** `uv run pytest -q` [VERIFIED: command run, 151 passed]
- **Phase gate:** Full suite green before `/gsd:verify-work`. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/config.json]

### Wave 0 Gaps

- None for framework setup; `pyproject.toml` already configures pytest, `tests/fusion/` exists, and full suite currently passes. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/pyproject.toml] [VERIFIED: command run]
- Add/extend tests in existing files before implementation: `tests/fusion/test_fusion_protocol.py`, `tests/fusion/test_strategies.py`, and optionally `tests/test_public_api.py` if root exports are added. [VERIFIED: codebase inspection]

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|------------------|
| V2 Authentication | no | No auth/session boundary exists in this pure library phase. [VERIFIED: codebase inspection] |
| V3 Session Management | no | No session state exists in this pure library phase. [VERIFIED: codebase inspection] |
| V4 Access Control | no | No user/permission model exists in this pure library phase. [VERIFIED: codebase inspection] |
| V5 Input Validation | yes | Dataclass `__post_init__()` validation for non-negative counts, finite stats, known label strings, and mapping key/count validity. [CITED: https://docs.python.org/3.14/library/dataclasses.html] |
| V6 Cryptography | no | No crypto, secrets, or credential handling exists in this phase. [VERIFIED: codebase inspection] |

### Known Threat Patterns for typed Python diagnostics

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Mutable caller data changes diagnostics after result construction | Tampering | Copy mappings before wrapping with `MappingProxyType`. [CITED: https://docs.python.org/3.14/library/types.html#types.MappingProxyType] |
| Misleading machine-readable label implies optimization quality | Spoofing / Repudiation | Use explicit `preserved_not_optimized` label in typed summary, diagnostics, tests, and README. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md] |
| Non-finite float diagnostics break strict JSON consumers | Tampering / Denial of Service | Reuse existing finite numeric validation style and avoid NaN/Infinity in summary stats. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/src/mosaic/splats/primitives.py] [CITED: https://docs.python.org/3.14/library/json.html] |

## Sources

### Primary (HIGH confidence)

- `/home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md` — locked Phase 04 decisions, canonical refs, scope, and deferred items. [VERIFIED: local file]
- `/home/prannayag/pragnition/robotics/mosaic/.planning/REQUIREMENTS.md` — FUSE-02 and FUSE-04 requirement definitions and out-of-scope occupancy-grid-first model. [VERIFIED: local file]
- `/home/prannayag/pragnition/robotics/mosaic/.planning/STATE.md` — current phase state and historical decisions. [VERIFIED: local file]
- `/home/prannayag/pragnition/robotics/mosaic/CLAUDE.md` — project constraints and conventions. [VERIFIED: local file]
- `/home/prannayag/pragnition/robotics/mosaic/src/mosaic/fusion/protocol.py` — current fusion contracts. [VERIFIED: local file]
- `/home/prannayag/pragnition/robotics/mosaic/src/mosaic/fusion/strategies.py` — current reference fusion strategy. [VERIFIED: local file]
- `/home/prannayag/pragnition/robotics/mosaic/src/mosaic/splats/primitives.py` — available splat fields for summaries. [VERIFIED: local file]
- `/home/prannayag/pragnition/robotics/mosaic/tests/fusion/test_fusion_protocol.py` and `/home/prannayag/pragnition/robotics/mosaic/tests/fusion/test_strategies.py` — current test structure. [VERIFIED: local file]
- Python dataclasses docs — frozen dataclasses, slots, default factories, and `__post_init__()`. [CITED: https://docs.python.org/3.14/library/dataclasses.html]
- Python typing docs — `Protocol` and `@runtime_checkable`. [CITED: https://docs.python.org/3.14/library/typing.html]
- Python types docs — `MappingProxyType`. [CITED: https://docs.python.org/3.14/library/types.html#types.MappingProxyType]
- Python json docs — JSON-supported default object types and scalar/container behavior. [CITED: https://docs.python.org/3.14/library/json.html]
- pytest docs — assertions, `pytest.raises(match=...)`, and good integration practices. [CITED: https://docs.pytest.org/en/stable/how-to/assert.html] [CITED: https://docs.pytest.org/en/stable/explanation/goodpractices.html]
- Official 3D Gaussian Splatting project page — 3D Gaussian representation and optimization boundary context. [CITED: https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/]

### Secondary (MEDIUM confidence)

- Environment probes: `uv --version`, `python3 --version`, `uv run pytest --version`, `uv run pytest tests/fusion -q`, and `uv run pytest -q`. [VERIFIED: command output]
- PyPI probe: `pip index versions pytest` reported `pytest (9.0.3)`. [VERIFIED: PyPI command]
- slopcheck probe: `slopcheck install pytest` returned `[OK] pytest (pypi)`. [VERIFIED: slopcheck]

### Tertiary (LOW confidence)

- Engineering judgment that decimal-heavy threshold tests are a warning sign for overfitted conflict heuristics. [ASSUMED]

## Metadata

**Confidence breakdown:**

- Standard stack: HIGH — stdlib + existing pytest/uv workflow verified from project files, official docs, and environment commands. [VERIFIED: codebase inspection]
- Architecture: HIGH — Phase 04 scope is tightly constrained by CONTEXT and existing fusion modules. [VERIFIED: /home/prannayag/pragnition/robotics/mosaic/.planning/phases/04-fusion-diagnostics-and-semantics-hardening/04-CONTEXT.md]
- Pitfalls: HIGH for locked-decision pitfalls, LOW for heuristic-overfit warning because it is engineering judgment. [VERIFIED: local files] [ASSUMED]

**Research date:** 2026-05-19 [VERIFIED: system date]
**Valid until:** 2026-06-18 for project-local architecture; re-check package/tool versions if changing dependencies. [ASSUMED]
