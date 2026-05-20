# Phase 06: Agent Posterior View Hardening - Research

**Researched:** 2026-05-20  
**Domain:** Typed provider-free Python posterior query contracts over immutable `SplatMap` snapshots [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:9-11]  
**Confidence:** HIGH [VERIFIED: codebase files and phase context were read directly]

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
## Implementation Decisions

### Uncertainty Summaries
- **D-01:** Add a separate `SplatPosteriorView.uncertainty()` method returning a typed uncertainty summary rather than expanding the existing `PosteriorSummary` shape.
- **D-02:** Base the Phase 6 uncertainty summary on covariance diagonal statistics plus opacity statistics. These fields already exist on `GaussianSplat` and support conservative posterior inspection without adding new backend assumptions.
- **D-03:** The uncertainty summary must carry a stable machine-readable semantics label `descriptive_only` to make clear that values are descriptive statistics over preserved splats, not calibrated belief, optimized posterior fusion, or reconstruction-quality scoring.
- **D-04:** Keep uncertainty summary scope global/map-level in Phase 6. Do not add per-provenance uncertainty breakdowns unless a later representation-memory phase requires them.

### Bounded Outputs
- **D-05:** Local spatial queries must be bounded by a required or default result limit so `query_local()` cannot become a raw full-map dump by default.
- **D-06:** Put the local-query limit on `LocalRadiusQuery` as an explicit request-boundary field such as `max_results`, rather than hiding it on the view object.
- **D-07:** When more splats match than the request limit, return bounded `splat_ids` plus stable truncation metadata such as total matches and a truncated flag. The result `count` should continue to describe returned IDs.
- **D-08:** Keep provenance summaries aggregate-only in Phase 6: source counts are allowed, but per-splat provenance records, evidence examples, and source-specific uncertainty records are out of scope.

### Determinism Coverage
- **D-09:** Repeated calls against the same fixed `SplatMap` snapshot must return exactly equal frozen dataclasses and immutable mappings for local, scene summary, uncertainty, and provenance queries.
- **D-10:** Local-query ordering should preserve existing `SplatMap.splats` tuple order and return the first matching IDs up to `max_results`; do not sort by distance in Phase 6.
- **D-11:** Numeric posterior summaries should use explicit fixed rounding, following the current six-decimal `mean_opacity` pattern, so exact-equality tests remain stable.
- **D-12:** Keep Phase 6 determinism coverage in `tests/agents/`. Do not add new evaluation-facing agent-query probes in this phase; Phase 5 owns evaluation harness work and can consume the hardened behavior later.

### Phase 7 Boundary
- **D-13:** Phase 6 must explicitly avoid all Phase 7 representation-memory concepts: no scene graph memory, spatial/raster memory, textual memory, belief/provenance memory store, commitment memory, navigation/perception/coordination tool families, or ARNA-style tool facade.
- **D-14:** Document the posterior-view vs future-memory boundary in both README language and tests, so the distinction is public and machine-checked.
- **D-15:** Do not add evidence/provenance references beyond aggregate provenance counts in Phase 6. Detailed evidence references belong to Phase 7 representation-memory contracts.
- **D-16:** Add uncertainty as the only new query family/method in Phase 6. Leave navigation, perception, coordination, belief/provenance, and memory/context query families to Phase 7.

### Claude's Discretion
No implementation areas were delegated to Claude discretion. Downstream agents should follow the decisions above.

### Deferred Ideas (OUT OF SCOPE)
## Deferred Ideas

None — discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| AGNT-02 | Posterior queries support local spatial queries, scene/map summaries, uncertainty summaries, and provenance summaries without exposing raw full map dumps by default. [VERIFIED: .planning/REQUIREMENTS.md:49-51] | Add `LocalRadiusQuery.max_results`, truncation metadata on `SplatQueryResult`, and a separate global `uncertainty()` method using existing splat covariance/opacity fields. [VERIFIED: src/mosaic/agents/queries.py:15-35; src/mosaic/splats/primitives.py:16-20] |
| AGNT-04 | Query determinism tests cover repeated calls against fixed snapshots. [VERIFIED: .planning/REQUIREMENTS.md:52-53] | Extend `tests/agents/` with exact equality checks for local, summary, uncertainty, and provenance outputs. [VERIFIED: tests/agents/test_splat_posterior.py:34-55] |
</phase_requirements>

## Summary

Phase 6 is a small hardening phase over an already implemented provider-free `mosaic.agents` seam. [VERIFIED: .planning/ROADMAP.md:159-169] The current implementation has `LocalRadiusQuery`, `SplatQueryResult`, `PosteriorSummary`, `ProvenanceSummary`, and `SplatPosteriorView` with local, summary, and provenance methods, but it lacks bounded local-query limits, truncation metadata, uncertainty summaries, and explicit repeated-query determinism tests. [VERIFIED: src/mosaic/agents/queries.py:9-63; src/mosaic/agents/posteriors.py:10-40; tests/agents/test_splat_posterior.py:34-55]

The implementation should stay dependency-free and pure Python; `pyproject.toml` declares no runtime dependencies and pytest only in the dev dependency group. [VERIFIED: pyproject.toml:10-15] Do not add indexing libraries, tensor libraries, backend adapters, provider SDKs, ROS/Habitat wrappers, persistent memories, or tool facades in this phase. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:11; .planning/REQUIREMENTS.md:103-112]

**Primary recommendation:** Add one request-bound local result limit, one bounded-result metadata extension, one separate descriptive uncertainty summary contract, and targeted tests/docs exports; do not broaden the agent API into Phase 7 memory/tool concepts. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:18-40]

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|--------------|----------------|-----------|
| Local radius query bounding | Python library API / agent posterior contract | Splat snapshot data model | The query object and result object live in `mosaic.agents`, while the splat iteration source is `SplatMap.splats`. [VERIFIED: src/mosaic/agents/queries.py:15-35; src/mosaic/splats/maps.py:10-22] |
| Uncertainty summary | Python library API / agent posterior contract | Gaussian primitive contract | `SplatPosteriorView` owns posterior questions; the raw inputs are `GaussianSplat.covariance_upper` and `GaussianSplat.opacity`. [VERIFIED: src/mosaic/agents/posteriors.py:10-40; src/mosaic/splats/primitives.py:16-20] |
| Provenance summary | Python library API / agent posterior contract | Gaussian primitive contract | Current provenance aggregation is already implemented as counts by `GaussianSplat.provenance`; Phase 6 keeps it aggregate-only. [VERIFIED: src/mosaic/agents/posteriors.py:34-40; .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:27-28] |
| Determinism coverage | Test suite | Public API exports | Existing tests exercise behavior but not repeated exact equality for all query families; Phase 6 should add tests in `tests/agents/` and public API smoke checks where exports change. [VERIFIED: tests/agents/test_splat_posterior.py:34-55; tests/test_public_api.py:89-94] |
| README boundary language | Documentation | Tests | README already documents provider-free posterior queries and hardening gaps; Phase 6 should update it and machine-check that no Phase 7/provider terms leak into current scope. [VERIFIED: README.md:127-151; README.md:174-184] |

## Current Implementation Summary

| File | Current Role | Planning Implication |
|------|--------------|----------------------|
| `src/mosaic/agents/queries.py` | Defines `AgentQueryKind.LOCAL_GEOMETRY`, `SCENE_SUMMARY`, `PROVENANCE`; `LocalRadiusQuery`; `SplatQueryResult`; `PosteriorSummary`; and immutable `ProvenanceSummary`. [VERIFIED: src/mosaic/agents/queries.py:9-63] | Add `AgentQueryKind.UNCERTAINTY`, `LocalRadiusQuery.max_results`, `SplatQueryResult.total_matches`, `SplatQueryResult.truncated`, and a new frozen uncertainty summary dataclass here. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:18-28] |
| `src/mosaic/agents/posteriors.py` | Implements `query_local()`, `summary()`, and `provenance()` on a frozen `SplatPosteriorView`. [VERIFIED: src/mosaic/agents/posteriors.py:10-40] | Apply the limit in `query_local()`, preserve tuple order, and add `uncertainty()` here. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:24-33] |
| `src/mosaic/agents/__init__.py` | Exports the public agent package surface through explicit imports and `__all__`. [VERIFIED: src/mosaic/agents/__init__.py:1-17] | Export any new stable query kind/result/summary type here. [VERIFIED: CLAUDE.md:122-128] |
| `src/mosaic/__init__.py` | Re-exports stable root package APIs including current agent types. [VERIFIED: src/mosaic/__init__.py:1-112] | Add root exports only for stable Phase 6 public APIs that should appear in concise examples and `tests/test_public_api.py`. [VERIFIED: README.md:41-72; tests/test_public_api.py:89-94] |
| `src/mosaic/splats/primitives.py` | Defines `GaussianSplat.center`, `covariance_upper`, `opacity`, and `provenance`; validates covariance positive-definiteness and opacity range. [VERIFIED: src/mosaic/splats/primitives.py:16-53] | Uncertainty statistics can use diagonal covariance entries `(xx, yy, zz)` from `covariance_upper` plus opacity without new data fields. [VERIFIED: src/mosaic/splats/primitives.py:9-13; .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:18-22] |
| `src/mosaic/splats/maps.py` | Stores immutable `splats: tuple[GaussianSplat, ...]` and exposes `__len__`. [VERIFIED: src/mosaic/splats/maps.py:10-22] | Deterministic local query order should use existing tuple order; no spatial index in this phase. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:30-33] |
| `tests/agents/test_queries.py` | Tests current query validation, count property, summary validation, provenance immutability, and agent exports. [VERIFIED: tests/agents/test_queries.py:13-83] | Extend with `max_results`, truncation metadata validation, uncertainty summary validation, and export checks. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:71-74] |
| `tests/agents/test_splat_posterior.py` | Tests local radius output, summary values, provenance counts, and provider-free source boundary. [VERIFIED: tests/agents/test_splat_posterior.py:34-75] | Extend with bounded local output, truncation metadata, uncertainty output, and repeated-call exact equality for all query methods. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:30-35] |
| `tests/test_public_api.py` | Tests root public exports and README boundary checks. [VERIFIED: tests/test_public_api.py:36-94] | Update if new uncertainty types are root exports and add README boundary assertions for posterior view vs future memory/tool concepts. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:36-40] |
| `README.md` | Documents current public API map, smoke examples, backend/dependency boundary, and known hardening gaps. [VERIFIED: README.md:41-184] | Replace the hardening-gap wording for agent posterior APIs with landed Phase 6 semantics once implemented. [VERIFIED: README.md:181-184] |

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python standard library `dataclasses`, `enum.StrEnum`, `types.MappingProxyType`, `math` | Python `>=3.12` project target [VERIFIED: pyproject.toml:9] | Frozen typed contracts, enum query kinds, immutable mappings, and distance/stat math. [VERIFIED: src/mosaic/agents/queries.py:3-6; src/mosaic/agents/posteriors.py:3-6] | Existing code already uses these modules and the project requires pure-Python foundation modules. [VERIFIED: CLAUDE.md:14; src/mosaic/agents/queries.py:3-6] |
| `pytest` | `>=8.4.0` in dev dependency group; `uv run pytest --version` reported `pytest 9.0.3` in this session. [VERIFIED: pyproject.toml:12-15; command output] | Deterministic contract tests. [VERIFIED: tests/agents/test_queries.py:1-83] | Existing project test workflow is `uv run pytest ...`. [VERIFIED: README.md:22-31] |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| None | — | No runtime dependency is needed for Phase 6. [VERIFIED: pyproject.toml:10] | Keep all summary math in standard Python because inputs are tuples and floats. [VERIFIED: src/mosaic/splats/primitives.py:16-20] |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Tuple scan in `query_local()` | Spatial index / KD-tree [ASSUMED] | Not recommended: Phase 6 is about bounded contracts and determinism, while scaling/indexing is explicitly deferred as `IDX-01`. [VERIFIED: .planning/REQUIREMENTS.md:93-96] |
| Dataclass summary | Dict payload [ASSUMED] | Not recommended: existing public contracts use frozen dataclasses and explicit exports. [VERIFIED: src/mosaic/agents/queries.py:15-63; CLAUDE.md:113-128] |

**Installation:** No package installation for Phase 6. [VERIFIED: pyproject.toml:10-15]

## Package Legitimacy Audit

No external runtime packages should be installed for Phase 6. [VERIFIED: pyproject.toml:10; .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:89-93]

| Package | Registry | Age | Downloads | Source Repo | slopcheck | Disposition |
|---------|----------|-----|-----------|-------------|-----------|-------------|
| None | — | — | — | — | — | No install |

**Packages removed due to slopcheck [SLOP] verdict:** none. [VERIFIED: no packages recommended]  
**Packages flagged as suspicious [SUS]:** none. [VERIFIED: no packages recommended]

## Architecture Patterns

### System Architecture Diagram

```text
Agent consumer code
    |
    | constructs LocalRadiusQuery / calls summary(), uncertainty(), provenance()
    v
SplatPosteriorView (provider-free Python API)
    |
    | reads immutable SplatMap.splats tuple in stored order
    v
Per-splat fields: center, covariance_upper, opacity, provenance
    |
    +--> query_local(): distance filter -> first max_results ids -> SplatQueryResult
    |       |                                      |
    |       |                                      +--> total_matches + truncated metadata
    |       v
    |   bounded splat_ids only, not raw splat dump
    |
    +--> summary(): count/provenance/mean opacity -> PosteriorSummary
    |
    +--> uncertainty(): covariance diagonal + opacity stats -> PosteriorUncertaintySummary
    |       |
    |       +--> semantics = "descriptive_only"
    |
    +--> provenance(): aggregate source counts -> ProvenanceSummary
```

### Recommended Project Structure

```text
src/mosaic/agents/
├── queries.py        # query kinds, request dataclasses, result/summary dataclasses
├── posteriors.py     # SplatPosteriorView behavior over SplatMap snapshots
└── __init__.py       # public agent package exports

tests/agents/
├── test_queries.py          # dataclass validation, immutability, exports
└── test_splat_posterior.py  # view behavior, determinism, provider-free boundary

tests/test_public_api.py     # root exports and README boundary checks
README.md                   # public posterior-view vs memory/tool boundary
```
[VERIFIED: listed files exist and were read]

### Pattern 1: Request-Bound Local Query Limits

**What:** Put `max_results` on `LocalRadiusQuery`, validate it as a positive integer, and let `SplatPosteriorView.query_local()` return only the first matching IDs up to that limit. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:24-33]

**When to use:** Every local spatial query in Phase 6. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:24-28]

**Planning implication:** Prefer a default such as `max_results: int = 32` to preserve ergonomic examples while preventing default full-map dumps. [ASSUMED]

**Example:**

```python
@dataclass(frozen=True, slots=True)
class LocalRadiusQuery:
    center: tuple[float, float, float]
    radius: float
    max_results: int = 32
    kind: AgentQueryKind = AgentQueryKind.LOCAL_GEOMETRY
```
[ASSUMED: proposed implementation shape based on current code]

### Pattern 2: Truncation Metadata Belongs on the Result

**What:** Extend `SplatQueryResult` with `total_matches: int` and `truncated: bool`, while leaving `count` as `len(splat_ids)`. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:26-28]

**When to use:** Any local query where raw matches exceed the request limit. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:26-28]

**Planning implication:** Tests must assert `result.count` describes returned IDs, `result.total_matches` describes all matches before truncation, and `result.truncated` is `True` only when `total_matches > count`. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:26-28]

### Pattern 3: Separate Descriptive Uncertainty Summary

**What:** Add a new frozen summary dataclass for map-level covariance-diagonal and opacity statistics with a stable `semantics` field equal to `"descriptive_only"`. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:18-23]

**When to use:** `SplatPosteriorView.uncertainty()` should return it for the full snapshot. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:18-23]

**Recommended fields:** `splat_count`, `semantics`, `mean_covariance_diagonal`, `max_covariance_diagonal`, `mean_opacity`, `min_opacity`, and `max_opacity`. [ASSUMED]

**Why these fields:** The covariance diagonal values are directly available as `(xx, yy, zz)` from `GaussianSplat.covariance_upper`, and opacity is already validated in `[0, 1]`. [VERIFIED: src/mosaic/splats/primitives.py:9-20; src/mosaic/splats/primitives.py:36-53]

### Anti-Patterns to Avoid

- **Raw-map local query behavior:** Returning every matching ID by default can become an unbounded map dump. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:24-28]
- **Distance sorting in Phase 6:** Sorting by distance changes current tuple-order determinism and is explicitly out of scope. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:30-33]
- **Calibrated uncertainty claims:** The summary must not imply optimized posterior quality, reconstruction quality, or calibrated belief. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:18-23]
- **Per-splat provenance/evidence leakage:** Phase 6 allows aggregate counts only; evidence references and memory stores belong to Phase 7. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:27-40]
- **Provider/runtime imports:** Agent posterior code must remain free of OpenAI/Anthropic/LangChain/ROS/Habitat/Torch/OpenCV-style imports. [VERIFIED: tests/agents/test_splat_posterior.py:58-75; .planning/REQUIREMENTS.md:49-52]

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Immutable public result contracts | Mutable dict payload protocol [ASSUMED] | Frozen dataclasses with `slots=True` [VERIFIED: src/mosaic/agents/queries.py:15-63] | Existing public API uses frozen dataclasses and exact equality tests need stable values. [VERIFIED: tests/agents/test_queries.py:30-64] |
| Read-only mappings | Custom immutable mapping wrapper [ASSUMED] | `MappingProxyType(dict(...))` [VERIFIED: src/mosaic/agents/queries.py:3-6; src/mosaic/agents/queries.py:57-63] | Current provenance summary already copies and freezes counts. [VERIFIED: tests/agents/test_queries.py:57-64] |
| Spatial acceleration | Custom KD-tree / external spatial index [ASSUMED] | Tuple scan plus `max_results` [VERIFIED: src/mosaic/agents/posteriors.py:14-20] | Scaling/indexing is deferred, and tuple-order determinism is a locked Phase 6 decision. [VERIFIED: .planning/REQUIREMENTS.md:93-96; .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:30-33] |
| Uncertainty calibration | Custom belief model or optimizer [ASSUMED] | Descriptive covariance/opacity statistics [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:18-23] | Phase 6 must not claim calibrated posterior fusion or reconstruction scoring. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:20-23] |

**Key insight:** This phase hardens API boundaries, not inference quality; bounded descriptive dataclasses are the product. [VERIFIED: .planning/ROADMAP.md:159-169]

## Planning Implications: `LocalRadiusQuery.max_results` and Truncation Metadata

1. Add `max_results` to `LocalRadiusQuery` as an explicit request field, not a view-level setting. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:24-27]
2. Validate `max_results > 0`; use `ValueError` with a domain-specific message matching existing validation style. [VERIFIED: src/mosaic/agents/queries.py:21-25; CLAUDE.md:98-102]
3. Keep `kind` defaulting to `AgentQueryKind.LOCAL_GEOMETRY`; add the new field before `kind` if using a defaulted `max_results`. [VERIFIED: src/mosaic/agents/queries.py:16-20]
4. Compute all matching IDs in tuple order or count matches during a tuple scan, then return only the first `max_results`. [VERIFIED: src/mosaic/agents/posteriors.py:14-20; .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:30-33]
5. Extend `SplatQueryResult` with `total_matches` and `truncated`; keep `count` as returned ID count. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:26-28]
6. Validate `total_matches >= len(splat_ids)` and `truncated == (total_matches > len(splat_ids))` in `SplatQueryResult.__post_init__()`. [ASSUMED]
7. Tests should include no-match, under-limit, exactly-at-limit, and over-limit cases. [ASSUMED]

## Uncertainty Summary Contract Proposal

Use a separate dataclass, tentatively named `PosteriorUncertaintySummary`, because the locked decision says not to expand `PosteriorSummary`. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:18-20]

Recommended contract: [ASSUMED]

```python
@dataclass(frozen=True, slots=True)
class PosteriorUncertaintySummary:
    splat_count: int
    semantics: str = "descriptive_only"
    mean_covariance_diagonal: tuple[float, float, float] = (0.0, 0.0, 0.0)
    max_covariance_diagonal: tuple[float, float, float] = (0.0, 0.0, 0.0)
    mean_opacity: float = 0.0
    min_opacity: float = 0.0
    max_opacity: float = 0.0
```

Planning notes:

- `semantics` must be exactly `"descriptive_only"`. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:20-23]
- For an empty `SplatMap`, return zero counts and zero statistics rather than raising. [ASSUMED]
- Use covariance diagonal entries `xx`, `yy`, and `zz` from `covariance_upper` positions `0`, `3`, and `5`. [VERIFIED: src/mosaic/splats/primitives.py:9-13; src/mosaic/splats/primitives.py:36]
- Round floating summaries to six decimals for exact repeated-call tests. [VERIFIED: src/mosaic/agents/posteriors.py:25-31; .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:32-33]
- Do not include per-provenance breakdowns, source evidence, confidence, status, timestamps, staleness, or conflict records. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:21-23; .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:36-40]

## Determinism and Test Strategy

| Behavior | Test Location | Required Assertions |
|----------|---------------|---------------------|
| Local query bounded output | `tests/agents/test_splat_posterior.py` | Query with more matching splats than `max_results`; assert returned IDs preserve `SplatMap.splats` order, `count == max_results`, `total_matches` is all matches, and `truncated is True`. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:24-33] |
| Local query exact determinism | `tests/agents/test_splat_posterior.py` | Repeated calls with the same `LocalRadiusQuery` return exactly equal `SplatQueryResult` dataclasses. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:30-35] |
| Scene summary exact determinism | `tests/agents/test_splat_posterior.py` | `view.summary() == view.summary()` with six-decimal numeric values. [VERIFIED: src/mosaic/agents/posteriors.py:22-32; .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:32-33] |
| Uncertainty summary exact determinism | `tests/agents/test_splat_posterior.py` | `view.uncertainty() == view.uncertainty()` and all numeric fields match expected rounded values. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:18-23; .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:30-35] |
| Provenance summary exact determinism | `tests/agents/test_splat_posterior.py` | `view.provenance() == view.provenance()` and mapping remains immutable. [VERIFIED: src/mosaic/agents/queries.py:53-63; tests/agents/test_queries.py:57-64] |
| Query/result validation | `tests/agents/test_queries.py` | `max_results <= 0` rejected; invalid uncertainty summary values rejected; `SplatQueryResult` inconsistent truncation metadata rejected. [ASSUMED] |
| Public exports | `tests/agents/test_queries.py`, `tests/test_public_api.py` | New uncertainty query kind/summary is exported from `mosaic.agents`; root export only if added to `src/mosaic/__init__.py`. [VERIFIED: src/mosaic/agents/__init__.py:1-17; src/mosaic/__init__.py:56-112] |
| README boundary | `tests/test_public_api.py` or `tests/agents/test_splat_posterior.py` | README states posterior summaries are bounded descriptive snapshot views and not Phase 7 representation memories/tools. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:36-40; README.md:127-151] |

## README and Public API Export Implications

- Update the Public API Map representative APIs for `mosaic.agents` to include the new uncertainty summary type and `SplatPosteriorView.uncertainty()`. [VERIFIED: README.md:41-55]
- Update the smoke example to pass or demonstrate `max_results` and to assert truncation metadata only where a multi-splat example needs it. [VERIFIED: README.md:127-151]
- Replace the known hardening gap that says agent posterior APIs need richer uncertainty summaries once the phase lands. [VERIFIED: README.md:181-184]
- Add public boundary language: posterior views are bounded descriptive views over immutable splat snapshots, not representation memories, scene graphs, belief stores, tool facades, navigation APIs, provider wrappers, or robot execution. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:36-40]
- Export new stable Phase 6 types from `mosaic.agents.__all__`; root `mosaic.__all__` should be updated only if the project wants concise root examples to import the new uncertainty type. [VERIFIED: CLAUDE.md:122-128; src/mosaic/agents/__init__.py:10-17; src/mosaic/__init__.py:56-112]

## Risks and Non-Goals

### Risks

- **Semantic overclaiming:** The word uncertainty can be misread as calibrated posterior belief; the `descriptive_only` label and README boundary must prevent that. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:18-23]
- **Silent raw-map leakage:** If `max_results` is optional but defaults to an unbounded value, the phase fails AGNT-02. [VERIFIED: .planning/REQUIREMENTS.md:49-51]
- **Breaking examples:** Adding a required `max_results` without a default would require updating current README examples and tests; using a positive default reduces churn. [VERIFIED: README.md:127-151; tests/agents/test_splat_posterior.py:34-41] [ASSUMED: default reduces churn]
- **Order instability:** Sorting by distance or using set/dict iteration for splat IDs would violate tuple-order determinism. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:30-33]
- **Scope creep into Phase 7:** Evidence references, belief/provenance stores, scene graphs, memory contexts, and tool families are explicitly deferred. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:36-40; .planning/REQUIREMENTS.md:54-63]

### Non-Goals

- No LLM/LVLM provider integration. [VERIFIED: .planning/REQUIREMENTS.md:87-90; .planning/REQUIREMENTS.md:103-108]
- No ROS, Habitat, robot execution, browser UI, WebSockets, or demo orchestration. [VERIFIED: .planning/REQUIREMENTS.md:103-110]
- No real 3DGS backend behavior or uncertainty optimization. [VERIFIED: .planning/REQUIREMENTS.md:75-79; .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:20-23]
- No persistent representation memories, scene graphs, raster/spatial memories, text memories, belief stores, or commitment memories. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:36-40]
- No spatial indexing or acceleration structures. [VERIFIED: .planning/REQUIREMENTS.md:93-96]

## Common Pitfalls

### Pitfall 1: Treating `count` as total matches after truncation

**What goes wrong:** Consumers cannot distinguish returned IDs from all matching IDs. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:26-28]

**Why it happens:** Existing `SplatQueryResult.count` is computed from `len(splat_ids)`. [VERIFIED: src/mosaic/agents/queries.py:28-35]

**How to avoid:** Keep `count` as returned ID count and add `total_matches` for unbounded match count. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:26-28]

**Warning signs:** Tests assert `count == total_matches` in over-limit cases. [ASSUMED]

### Pitfall 2: Uncertainty summary drift from fixed rounding

**What goes wrong:** Exact dataclass equality becomes flaky if floats are not rounded consistently. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:30-35]

**Why it happens:** Floating arithmetic can produce long binary-derived decimal values. [ASSUMED]

**How to avoid:** Round all mean/min/max summary floats that derive from arithmetic to six decimals, matching existing `mean_opacity`. [VERIFIED: src/mosaic/agents/posteriors.py:25-31; .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:32-33]

**Warning signs:** Tests use approximate assertions instead of exact equality for repeated calls. [ASSUMED]

### Pitfall 3: Adding Phase 7 semantics while naming uncertainty/provenance

**What goes wrong:** Phase 6 accidentally introduces belief claims, evidence references, staleness, memory IDs, or tool families. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:36-40]

**Why it happens:** The roadmap places Phase 7 immediately after Phase 6 and uses agent-friendly representation language. [VERIFIED: .planning/ROADMAP.md:172-184]

**How to avoid:** Keep Phase 6 outputs to bounded IDs, aggregate counts, and descriptive statistics over existing splats. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:18-40]

**Warning signs:** New classes contain `Evidence`, `Claim`, `Memory`, `Tool`, `Navigation`, or provider-specific names. [ASSUMED]

## Code Examples

### Bounded Local Query Shape

```python
query = LocalRadiusQuery(center=(0.0, 0.0, 0.0), radius=2.0, max_results=2)
result = view.query_local(query)
assert result.splat_ids == (0, 1)
assert result.count == 2
assert result.total_matches == 3
assert result.truncated is True
```
[ASSUMED: proposed test shape derived from locked decisions]

### Descriptive Uncertainty Summary Shape

```python
summary = view.uncertainty()
assert summary.semantics == "descriptive_only"
assert summary.splat_count == 3
assert summary.mean_covariance_diagonal == (0.2, 0.2, 0.2)
assert summary.mean_opacity == 0.583333
```
[ASSUMED: proposed test shape derived from locked decisions and current fixture]

### Determinism Shape

```python
assert view.query_local(query) == view.query_local(query)
assert view.summary() == view.summary()
assert view.uncertainty() == view.uncertainty()
assert view.provenance() == view.provenance()
```
[ASSUMED: proposed test shape derived from AGNT-04]

## State of the Art

| Old Approach | Current Phase 6 Approach | When Changed | Impact |
|--------------|--------------------------|--------------|--------|
| Local query returns all matching splat IDs. [VERIFIED: src/mosaic/agents/posteriors.py:14-20] | Local query returns first matching IDs up to request `max_results` with truncation metadata. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:24-28] | Phase 6 plan/execution. [VERIFIED: .planning/ROADMAP.md:159-170] | Prevents raw full-map dumps by default. [VERIFIED: .planning/REQUIREMENTS.md:49-51] |
| Posterior summaries cover count, provenance count, and mean opacity only. [VERIFIED: src/mosaic/agents/queries.py:38-50] | Separate descriptive uncertainty summary covers covariance diagonal and opacity statistics. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:18-23] | Phase 6 plan/execution. [VERIFIED: .planning/ROADMAP.md:159-170] | Lets agents inspect conservative map-level uncertainty signals without calibrated belief claims. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:18-23] |
| Determinism is implied by frozen dataclasses and tuple scans. [VERIFIED: src/mosaic/agents/queries.py:15-63; src/mosaic/agents/posteriors.py:14-40] | Determinism is explicitly tested across local, summary, uncertainty, and provenance queries. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:30-35] | Phase 6 plan/execution. [VERIFIED: .planning/ROADMAP.md:159-170] | Satisfies AGNT-04. [VERIFIED: .planning/REQUIREMENTS.md:52-53] |

**Deprecated/outdated:** None found in the current Phase 6 code path. [VERIFIED: files read directly]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Use a default `max_results` such as `32`. | Architecture Patterns / Planning Implications | If user wants a required limit with no default, examples and test expectations must change. |
| A2 | Add validation coupling `truncated == (total_matches > len(splat_ids))`. | Planning Implications | If planner prefers derived property instead of stored field, dataclass shape changes. |
| A3 | Use fields `mean_covariance_diagonal`, `max_covariance_diagonal`, `mean_opacity`, `min_opacity`, `max_opacity`. | Uncertainty Summary Contract Proposal | If planner chooses different statistic names, README/tests must align. |
| A4 | Empty-map uncertainty returns zero statistics instead of raising. | Uncertainty Summary Contract Proposal | If empty maps should be invalid for uncertainty, tests and docs differ. |
| A5 | Exact tests should include no-match, under-limit, exactly-at-limit, and over-limit cases. | Planning Implications | Low risk; more tests than minimum may be unnecessary. |

## Open Questions

1. **Should the new uncertainty summary type be root-exported from `mosaic` or only package-exported from `mosaic.agents`?**
   - What we know: Existing agent types are root-exported. [VERIFIED: src/mosaic/__init__.py:1-8; src/mosaic/__init__.py:56-112]
   - What's unclear: Whether every Phase 6 type should be root-level stable API immediately. [ASSUMED]
   - Recommendation: Root-export the uncertainty summary only if README examples import it from `mosaic`; always export it from `mosaic.agents`. [ASSUMED]

2. **What exact default should `LocalRadiusQuery.max_results` use?**
   - What we know: The limit must be request-bound and prevent default raw full-map dumps. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:24-28]
   - What's unclear: The locked context does not specify a numeric default. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:24-28]
   - Recommendation: Use `32` as a small ergonomic default unless the planner chooses a required argument. [ASSUMED]

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| `uv` | Running project tests and dependency environment | Yes | `uv 0.10.10` [VERIFIED: command output] | Use installed project environment if `uv` remains available. [ASSUMED] |
| Python | Package runtime | Yes | System `python3` reported `Python 3.14.4`; project requires `>=3.12`. [VERIFIED: command output; pyproject.toml:9] | `uv run` manages the project test runtime. [VERIFIED: README.md:22-31] |
| `pytest` via `uv run` | Validation | Yes | `pytest 9.0.3` [VERIFIED: command output] | None needed. [VERIFIED: command output] |

**Missing dependencies with no fallback:** None found for Phase 6. [VERIFIED: command output and no runtime dependencies]

**Missing dependencies with fallback:** None found for Phase 6. [VERIFIED: command output and no runtime dependencies]

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | `pytest` via `uv run`, observed `pytest 9.0.3`; project dev dependency is `pytest>=8.4.0`. [VERIFIED: command output; pyproject.toml:12-15] |
| Config file | `pyproject.toml` with `testpaths = ["tests"]` and `pythonpath = ["src"]`. [VERIFIED: pyproject.toml:17-19] |
| Quick run command | `uv run pytest tests/agents/test_queries.py tests/agents/test_splat_posterior.py tests/test_public_api.py -q` [VERIFIED: command returned 19 passed in this session] |
| Full suite command | `uv run pytest -q` [VERIFIED: README.md:26-31] |

### Phase Requirements -> Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|--------------|
| AGNT-02 | Local spatial queries are bounded and report truncation metadata. [VERIFIED: .planning/REQUIREMENTS.md:49-51] | Unit | `uv run pytest tests/agents/test_queries.py tests/agents/test_splat_posterior.py -q` | Yes [VERIFIED: tests/agents/test_queries.py; tests/agents/test_splat_posterior.py] |
| AGNT-02 | Scene/map summary still returns bounded summary fields rather than raw splats. [VERIFIED: .planning/REQUIREMENTS.md:49-51] | Unit | `uv run pytest tests/agents/test_splat_posterior.py -q` | Yes [VERIFIED: tests/agents/test_splat_posterior.py] |
| AGNT-02 | Uncertainty summary returns descriptive covariance diagonal and opacity stats. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:18-23] | Unit | `uv run pytest tests/agents/test_queries.py tests/agents/test_splat_posterior.py -q` | Yes; needs new tests [VERIFIED: tests/agents/test_queries.py; tests/agents/test_splat_posterior.py] |
| AGNT-02 | Provenance summary remains aggregate-only. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:27-28] | Unit | `uv run pytest tests/agents/test_splat_posterior.py -q` | Yes [VERIFIED: tests/agents/test_splat_posterior.py] |
| AGNT-04 | Repeated local/summary/uncertainty/provenance queries return exactly equal outputs. [VERIFIED: .planning/REQUIREMENTS.md:52-53] | Unit | `uv run pytest tests/agents/test_splat_posterior.py -q` | Yes; needs expanded tests [VERIFIED: tests/agents/test_splat_posterior.py] |
| AGNT-02 | README and public exports describe provider-free bounded posterior views and Phase 7 boundary. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:36-40] | Unit/docs smoke | `uv run pytest tests/test_public_api.py tests/agents/test_queries.py -q` | Yes [VERIFIED: tests/test_public_api.py; tests/agents/test_queries.py] |

### Sampling Rate

- **Per task commit:** `uv run pytest tests/agents/test_queries.py tests/agents/test_splat_posterior.py tests/test_public_api.py -q` [VERIFIED: command returned 19 passed in this session]
- **Per wave merge:** `uv run pytest -q` [VERIFIED: README.md:26-31]
- **Phase gate:** Full suite green before `/gsd:verify-work`. [VERIFIED: GSD workflow expectations]

### Wave 0 Gaps

- [ ] `tests/agents/test_queries.py` — add `max_results`, truncation metadata, uncertainty summary validation, and new export coverage. [VERIFIED: current file lacks these tests at tests/agents/test_queries.py:13-83]
- [ ] `tests/agents/test_splat_posterior.py` — add bounded local over-limit behavior, `uncertainty()`, exact repeated-call determinism for all query families, and README/provider boundary expansion. [VERIFIED: current file lacks these tests at tests/agents/test_splat_posterior.py:34-75]
- [ ] `tests/test_public_api.py` — add root export and README boundary assertions if public API surface changes. [VERIFIED: tests/test_public_api.py:89-94]

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|------------------|
| V2 Authentication | No | No authentication surface exists in Phase 6. [VERIFIED: Phase scope is Python posterior view API at .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:9-11] |
| V3 Session Management | No | No session state exists in Phase 6. [VERIFIED: src/mosaic/agents/posteriors.py:10-40] |
| V4 Access Control | No | No user/role boundary exists in Phase 6. [VERIFIED: src/mosaic/agents/posteriors.py:10-40] |
| V5 Input Validation | Yes | Dataclass `__post_init__()` validation for query/result/summary invariants. [VERIFIED: src/mosaic/agents/queries.py:21-25; src/mosaic/agents/queries.py:44-63] |
| V6 Cryptography | No | No cryptographic behavior exists in Phase 6. [VERIFIED: src/mosaic/agents/posteriors.py:1-40] |

### Known Threat Patterns for This Stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Unbounded data exposure through local query | Information Disclosure | Enforce request-bound `max_results` and truncation metadata. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:24-28] |
| Misleading uncertainty semantics | Spoofing / Information Integrity | Fixed `descriptive_only` semantics label and README boundary language. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:18-23; .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:36-40] |
| Mutable result mappings | Tampering | Copy and freeze mappings with `MappingProxyType`. [VERIFIED: src/mosaic/agents/queries.py:53-63] |
| Dependency boundary creep | Supply-chain / Elevation of Privilege | Keep runtime dependencies empty and test against provider/robot/heavy backend imports. [VERIFIED: pyproject.toml:10; tests/agents/test_splat_posterior.py:58-75] |

## Sources

### Primary (HIGH confidence)

- `.planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md` — locked decisions, phase boundaries, canonical references. [VERIFIED: file read]
- `.planning/REQUIREMENTS.md` — AGNT-02 and AGNT-04 definitions plus deferred Phase 7/v2 scope. [VERIFIED: file read]
- `.planning/ROADMAP.md` — Phase 6 goal/success criteria and project progress. [VERIFIED: file read]
- `src/mosaic/agents/queries.py` — current query/result/summary contracts. [VERIFIED: file read]
- `src/mosaic/agents/posteriors.py` — current posterior view implementation. [VERIFIED: file read]
- `src/mosaic/splats/primitives.py` — covariance/opacity/provenance source fields. [VERIFIED: file read]
- `src/mosaic/splats/maps.py` — immutable splat tuple order. [VERIFIED: file read]
- `tests/agents/test_queries.py`, `tests/agents/test_splat_posterior.py`, `tests/test_public_api.py` — current validation surfaces. [VERIFIED: files read]
- `README.md` — public API and boundary language. [VERIFIED: file read]
- `pyproject.toml` — runtime/dev dependency and pytest configuration. [VERIFIED: file read]

### Secondary (MEDIUM confidence)

- None. [VERIFIED: no external research was needed because this is codebase-constrained]

### Tertiary (LOW confidence)

- Assumptions listed in `## Assumptions Log`. [ASSUMED]

## Metadata

**Confidence breakdown:**

- Standard stack: HIGH — no new runtime packages; current Python/pytest setup was verified from project files and commands. [VERIFIED: pyproject.toml:10-19; command output]
- Architecture: HIGH — locked decisions and current agent/splat code define the implementation path. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:18-40; src/mosaic/agents/posteriors.py:10-40]
- Pitfalls: HIGH for scope/boundary pitfalls from CONTEXT.md; MEDIUM for proposed exact field names/default limit because they are recommendations. [VERIFIED: .planning/phases/06-agent-posterior-view-hardening/06-CONTEXT.md:18-40] [ASSUMED]

**Research date:** 2026-05-20  
**Valid until:** 2026-06-19 for this codebase-constrained phase, unless agent query contracts change first. [ASSUMED]
