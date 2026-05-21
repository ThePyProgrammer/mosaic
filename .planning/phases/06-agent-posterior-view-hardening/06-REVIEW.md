---
phase: 06-agent-posterior-view-hardening
reviewed: 2026-05-21T00:00:00Z
depth: standard
files_reviewed: 7
files_reviewed_list:
  - src/mosaic/__init__.py
  - src/mosaic/agents/__init__.py
  - src/mosaic/agents/posteriors.py
  - src/mosaic/agents/queries.py
  - tests/agents/test_queries.py
  - tests/agents/test_splat_posterior.py
  - tests/test_public_api.py
findings:
  critical: 1
  warning: 3
  info: 0
  total: 4
status: issues_found
---

# Phase 06: Code Review Report

**Reviewed:** 2026-05-21T00:00:00Z  
**Depth:** standard  
**Files Reviewed:** 7  
**Status:** issues_found  

## Summary

Reviewed the agent posterior query surface, public exports, and associated tests. The implementation is small and typed, but the query boundary is not hardened enough for a public agent-facing API: non-finite coordinates/radii can silently turn a local-radius query into a match-all query, query kind is user-controllable but ignored, and provenance handling can crash on splats that are valid under the current splat primitive contract.

## Critical Issues

### CR-01: Non-finite local query values can silently match every splat

**Classification:** BLOCKER  
**File:** `src/mosaic/agents/queries.py:23-29` and `src/mosaic/agents/posteriors.py:24-29`

**Issue:** `LocalRadiusQuery.__post_init__()` validates tuple length and positive radius, but it does not reject `NaN` or infinite values in `center` or `radius`. In `SplatPosteriorView.query_local()`, `math.dist()` with a `NaN` coordinate returns `NaN`, and `NaN > query.radius` is false. A `radius=float("nan")` has the same problem because `dist(...) > NaN` is false. That means an invalid local query can behave as a match-all query, returning the first `max_results` splat ids and reporting every splat as a total match. This violates the bounded deterministic posterior-query boundary.

**Fix:** Reject non-finite center coordinates and radius in `LocalRadiusQuery.__post_init__()` before query execution.

## Warnings

### WR-01: LocalRadiusQuery accepts incompatible query kinds that query_local ignores

**Classification:** WARNING  
**File:** `src/mosaic/agents/queries.py:21`

**Issue:** `LocalRadiusQuery` exposes a construction-time `kind` field but does not validate that it is `AgentQueryKind.LOCAL_GEOMETRY`. A caller can construct `LocalRadiusQuery(..., kind=AgentQueryKind.UNCERTAINTY)`, pass it to `query_local()`, and receive a local geometry result anyway. That creates contradictory request metadata at the public API boundary and will become a correctness trap as more query kinds are added.

**Fix:** Reject any `LocalRadiusQuery.kind` value other than `AgentQueryKind.LOCAL_GEOMETRY`.

### WR-02: Posterior provenance can crash on splats that are valid under current core contracts

**Classification:** WARNING  
**File:** `src/mosaic/agents/posteriors.py:76-82`

**Issue:** `GaussianSplat` currently accepts `provenance=" "` as valid, but `SplatPosteriorView.provenance()` passes that value to `ProvenanceSummary`, which rejects blank source names and raises `ValueError`. This makes the posterior view unable to summarize a `SplatMap` that is valid according to the splat module’s own validation.

**Fix:** Make posterior summaries and provenance aggregation skip blank provenance strings consistently.

### WR-03: Posterior uncertainty summaries allow impossible descriptive statistics

**Classification:** WARNING  
**File:** `src/mosaic/agents/queries.py:79-100`

**Issue:** `PosteriorUncertaintySummary` validates tuple lengths, non-negative covariance diagonals, and opacity bounds, but it does not validate ordering relationships. Public callers can construct impossible summaries such as `min_opacity=0.9, mean_opacity=0.1, max_opacity=0.2` or `mean_covariance_diagonal=(10, 10, 10)` with `max_covariance_diagonal=(1, 1, 1)`.

**Fix:** Validate `min_opacity <= mean_opacity <= max_opacity` and each mean covariance diagonal component is less than or equal to the corresponding max component.
