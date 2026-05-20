---
phase: 05-evaluation-metric-and-failure-gate-hardening
plan: 02
subsystem: evaluation
tags: [benchmark-artifacts, jsonl, scenario-summary, diagnostics]

requires:
  - phase: 05-evaluation-metric-and-failure-gate-hardening
    plan: 01
    provides: typed metric families and lifecycle metric constructors
provides:
  - enriched BenchmarkArtifact scenario_summary and gate_results fields
  - compact JSONL benchmark artifact writer
  - lifecycle and map-quality metric population in run_slam_benchmark
  - scalar metric diagnostic mirrors for compatibility
affects: [evaluation-runner, benchmark-artifacts, scenario-metadata, artifact-compatibility]

tech-stack:
  added: []
  patterns:
    - additive frozen artifact fields with copied mapping/sequence boundaries
    - compact JSONL one-artifact-per-line serialization
    - scenario metadata summaries without raw observation/image dumps

key-files:
  created:
    - .planning/phases/05-evaluation-metric-and-failure-gate-hardening/05-02-SUMMARY.md
  modified:
    - src/mosaic/evaluation/runner.py
    - src/mosaic/evaluation/scenarios.py
    - src/mosaic/evaluation/__init__.py
    - tests/evaluation/test_runner.py
    - tests/evaluation/test_scenarios.py
    - tests/artifacts/test_slam_and_evaluation_artifacts.py

key-decisions:
  - "Scenario summaries are serialized as compact metadata only: name, frame_count, update_count, camera_ids, and expected_map_frame."
  - "BenchmarkArtifact keeps failure_classification for compatibility and adds empty gate_results for Plan 05-03 typed gate data."
  - "Metric diagnostics mirror selected lifecycle scalar names with metric_ prefixes while keeping snapshot_splat_count and last_* update diagnostics."

patterns-established:
  - "write_benchmark_artifacts_jsonl writes json.dumps(artifact.as_dict(), sort_keys=True) plus one newline per artifact."
  - "run_slam_benchmark uses Phase 5 lifecycle_metrics and map_quality_metrics constructors instead of re-deriving raw metric dictionaries."

requirements-completed: [EVAL-02, EVAL-04]

duration: 8min
completed: 2026-05-19
---

# Phase 05 Plan 02: Benchmark Artifact Enrichment and JSONL Summary

**Benchmark artifacts now carry deterministic scenario metadata, lifecycle/map metric families, compatibility diagnostic mirrors, and compact JSONL output.**

## Performance

- **Duration:** 8 min
- **Started:** 2026-05-19T09:24:00Z
- **Completed:** 2026-05-19T09:32:00Z
- **Tasks:** 2
- **Files modified:** 6

## Accomplishments

- Added failing tests for scenario summary metadata, lifecycle/map metric family presence, scalar diagnostic mirrors, additive artifact keys, and compact JSONL output.
- Implemented `scenario_summary()` and enriched `BenchmarkArtifact` with copied/frozen `scenario_summary` and `gate_results` fields.
- Updated `run_slam_benchmark()` to collect updates, call Plan 05-01 metric constructors, mirror selected metric totals into diagnostics, and avoid raw observation/image data in artifact summaries.
- Added and exported `write_benchmark_artifacts_jsonl()` while preserving pretty sorted single-artifact JSON output.

## Task Commits

Each task was committed atomically:

1. **Task 05-02-01: Lock enriched artifact and JSONL behavior in tests** - `1daf19d` (test)
2. **Task 05-02-02: Implement benchmark artifact enrichment and JSONL writer** - `261f494` (feat)

Additional compatibility fix:

3. **Full-suite compatibility update** - `332d372` (fix)

## Files Created/Modified

- `src/mosaic/evaluation/runner.py` - Adds additive artifact fields, lifecycle/map metric population, scalar diagnostic mirrors, and JSONL writing.
- `src/mosaic/evaluation/scenarios.py` - Adds scenario metadata summary helper that omits raw observations, views, image color, and image data.
- `src/mosaic/evaluation/__init__.py` - Exports `scenario_summary` and `write_benchmark_artifacts_jsonl` from the stable evaluation surface.
- `tests/evaluation/test_runner.py` - Locks enriched artifact shape, metric families, diagnostic mirrors, JSON writer compatibility, and JSONL one-line output.
- `tests/evaluation/test_scenarios.py` - Locks scenario summary metadata and raw-observation exclusion.
- `tests/artifacts/test_slam_and_evaluation_artifacts.py` - Updates additive artifact shape compatibility expectations while preserving schema-envelope exclusion.

## Verification

- `uv run pytest tests/evaluation/test_runner.py tests/evaluation/test_scenarios.py -q` — passed, 9 tests.
- `uv run pytest tests/evaluation -q` — passed, 20 tests.
- `uv run pytest tests/artifacts/test_slam_and_evaluation_artifacts.py tests/evaluation -q` — passed, 30 tests.
- `uv run pytest -q` — passed, 190 tests.

## Decisions Made

- Used the backend snapshot frame as the current expected map frame source for deterministic benchmark artifacts.
- Kept `gate_results` empty by default so Plan 05-03 can populate typed gate/failure data without another artifact-shape migration.
- Serialized `camera_ids` as tuples in Python-facing summary mappings and JSON lists through `BenchmarkArtifact.as_dict()`.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Updated artifact compatibility test for additive artifact fields**
- **Found during:** Full-suite verification after Task 05-02-02
- **Issue:** `tests/artifacts/test_slam_and_evaluation_artifacts.py` still asserted the exact pre-Plan-02 `BenchmarkArtifact.as_dict()` shape and failed once `scenario_summary` and `gate_results` were correctly added.
- **Fix:** Updated the assertion to include the additive fields while preserving the test's schema-envelope exclusion checks.
- **Files modified:** `tests/artifacts/test_slam_and_evaluation_artifacts.py`
- **Verification:** `uv run pytest tests/artifacts/test_slam_and_evaluation_artifacts.py tests/evaluation -q && uv run pytest -q`
- **Committed in:** `332d372`

---

**Total deviations:** 1 auto-fixed (1 Rule 1 bug)
**Impact on plan:** Compatibility test update was required by the planned additive artifact shape; no runtime scope changed.

## Issues Encountered

- The RED phase failed during collection because `scenario_summary` and `write_benchmark_artifacts_jsonl` were not exported yet, satisfying the expected failing-test gate.
- Full-suite verification found one stale exact artifact-shape assertion outside the plan's primary test files; fixed as a compatibility bug.

## Known Stubs

None detected in files created or modified by this plan.

## Threat Flags

| Flag | File | Description |
|------|------|-------------|
| threat_flag: persisted-jsonl-boundary | `src/mosaic/evaluation/runner.py` | Benchmark artifacts now cross a JSONL filesystem boundary; mitigated with compact sorted JSON per artifact line and splitlines tests. |

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- Plan 05-03 can populate typed gate results and derive failure classifications from the additive `gate_results` artifact field.
- Downstream benchmark consumers can use either the preserved pretty single-run JSON writer or the new compact JSONL multi-artifact writer.

## Self-Check: PASSED

- Confirmed summary path exists before metadata commit.
- Confirmed task commits `1daf19d`, `261f494`, and compatibility fix `332d372` exist in git history.
- Confirmed modified code/test files exist and the full suite passes.

---
*Phase: 05-evaluation-metric-and-failure-gate-hardening*
*Completed: 2026-05-19*
