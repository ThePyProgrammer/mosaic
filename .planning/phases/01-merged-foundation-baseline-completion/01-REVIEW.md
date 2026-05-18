---
phase: 01-merged-foundation-baseline-completion
reviewed: 2026-05-18T07:19:04Z
depth: standard
files_reviewed: 7
files_reviewed_list:
  - src/mosaic/evaluation/runner.py
  - tests/agents/test_queries.py
  - tests/agents/test_splat_posterior.py
  - tests/evaluation/test_regression.py
  - tests/evaluation/test_runner.py
  - tests/evaluation/test_scenarios.py
  - tests/test_readme_contract.py
findings:
  critical: 0
  warning: 3
  info: 0
  total: 3
status: issues_found
---

# Phase 01: Code Review Report

**Reviewed:** 2026-05-18T07:19:04Z
**Depth:** standard
**Files Reviewed:** 7
**Status:** issues_found

## Summary

Reviewed the evaluation benchmark runner and the listed agent/evaluation/README contract tests. The implementation is small and the reviewed tests currently pass (`uv run pytest ... -q`), but the public benchmark artifact contract has validation/type-contract defects and one test relies on the caller's current working directory.

## Narrative Findings (AI reviewer)

## Warnings

### WR-01: BenchmarkArtifact accepts invalid benchmark identity and counts

**File:** `src/mosaic/evaluation/runner.py:46-51`

**Issue:** **WARNING** — `BenchmarkArtifact.__post_init__()` validates only `failure_classification`. It still accepts blank `scenario_name`, blank `backend_name`, and negative `update_count`, so callers can write machine-readable benchmark artifacts that cannot be reliably attributed or that report impossible processing counts. That undermines the evaluation/regression contract this module is supposed to harden.

**Fix:** Validate the remaining artifact invariants before freezing mappings.

```python
def __post_init__(self) -> None:
    if not self.scenario_name.strip():
        raise ValueError("BenchmarkArtifact scenario_name must not be blank")
    if not self.backend_name.strip():
        raise ValueError("BenchmarkArtifact backend_name must not be blank")
    if self.update_count < 0:
        raise ValueError("BenchmarkArtifact update_count must be non-negative")
    if not self.failure_classification.strip():
        raise ValueError("BenchmarkArtifact failure_classification must not be blank")
    object.__setattr__(self, "metrics", FrozenMetricSequence(self.metrics))
    object.__setattr__(self, "backend_metadata", MappingProxyType(dict(self.backend_metadata)))
    object.__setattr__(self, "diagnostics", MappingProxyType(dict(self.diagnostics)))
```

### WR-02: FrozenMetricSequence lies about returning mutable dictionaries

**File:** `src/mosaic/evaluation/runner.py:15-24`

**Issue:** **WARNING** — `MetricDict` is defined as `dict[str, str | float]`, `FrozenMetricSequence` subclasses `Sequence[MetricDict]`, and `__getitem__()` is annotated to return `MetricDict`, but the constructor stores `MappingProxyType` instances. Runtime callers receive immutable mapping proxies despite the public type promising mutable dictionaries, which is a typed API contract defect in a `py.typed` package and can cause downstream code to fail at runtime when it follows the annotation.

**Fix:** Make the metric element type immutable in the public contract, and reserve mutable `dict` for serialization output.

```python
MetricMapping = Mapping[str, str | float]
MetricDict = dict[str, str | float]

class FrozenMetricSequence(Sequence[MetricMapping]):
    def __init__(self, metrics: Sequence[MetricMapping]) -> None:
        self._metrics = tuple(MappingProxyType(dict(metric)) for metric in metrics)

    def __getitem__(self, index: int) -> MetricMapping:
        return self._metrics[index]

@dataclass(frozen=True, slots=True)
class BenchmarkArtifact:
    metrics: Sequence[MetricMapping]

    def as_dict(self) -> dict[str, str | int | list[MetricDict] | dict[str, ArtifactValue]]:
        ...
```

### WR-03: Provider-boundary test depends on the process working directory

**File:** `tests/agents/test_splat_posterior.py:58-60`

**Issue:** **WARNING** — this test reads `pyproject.toml` and `src/mosaic/agents/posteriors.py` via relative paths. It passes only when pytest is launched from the repository root; invoking the file from another working directory fails with `FileNotFoundError`. That makes the test less reliable than `tests/test_readme_contract.py`, which correctly resolves paths from `__file__`.

**Fix:** Resolve the repository root from the test file location before reading project files.

```python
ROOT = Path(__file__).resolve().parents[2]


def test_agent_posterior_boundary_stays_provider_free() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    posteriors_source = (ROOT / "src/mosaic/agents/posteriors.py").read_text(encoding="utf-8")
    ...
```

---

_Reviewed: 2026-05-18T07:19:04Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
