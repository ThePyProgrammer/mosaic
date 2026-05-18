# Phase 3: Backend Registry and Contracts - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-18
**Phase:** 3-Backend Registry and Contracts
**Areas discussed:** Registry shape, Metadata fields, Availability checks, Contract tests

---

## Registry Shape

| Question | Option | Description | Selected |
|----------|--------|-------------|----------|
| Should the backend registry store live backend instances or backend factories? | Factory registry | Register callables/specs that create fresh `SplatSlamBackend` instances, so tests and benchmarks avoid shared mutable backend state. | ✓ |
| Should the backend registry store live backend instances or backend factories? | Instance registry | Register already-created backend objects; simpler, but easy to leak state between contract tests because backends are stateful. | |
| Should the backend registry store live backend instances or backend factories? | Support both | Allow instances and factories; flexible, but adds validation branches and ambiguity to a small library seam. | |
| How strict should backend registration be when a name is already registered? | Reject duplicates | Raise `ValueError` on duplicate names, matching `PlatformRegistry` and preventing accidental backend shadowing. | ✓ |
| How strict should backend registration be when a name is already registered? | Explicit replace | Allow replacement only through a named replace/register_override method; useful for tests, but expands the registry API. | |
| How strict should backend registration be when a name is already registered? | Last wins | Silently overwrite duplicate names; convenient for experimentation, but risky for reproducible benchmarks. | |
| What should the default backend registry include out of the box? | Deterministic only | Include only `DeterministicSplatBackend` by default; keeps v1 pure-Python and makes tests/benchmarks immediately runnable. | ✓ |
| What should the default backend registry include out of the box? | Empty registry | Force users to register everything themselves; clean, but less discoverable and duplicates boilerplate in tests. | |
| What should the default backend registry include out of the box? | Future placeholders | Include metadata-only entries for expected real backends; discoverable, but risks implying unsupported integrations exist. | |
| How should users retrieve a backend from the registry? | create(name) | Lookup by name and return a fresh backend instance from the registered factory; mirrors the factory-registry decision. | ✓ |
| How should users retrieve a backend from the registry? | get(name) factory | Return the registered factory/spec and let callers instantiate it; more explicit, but more boilerplate for common use. | |
| How should users retrieve a backend from the registry? | Both methods | Expose both `get()` and `create()`; ergonomic, but more API surface to document and test. | |

**User's choice:** Factory registry; reject duplicates; deterministic-only default registry; `create(name)` retrieval.
**Notes:** User moved to next area after these decisions.

---

## Metadata Fields

| Question | Option | Description | Selected |
|----------|--------|-------------|----------|
| Should backend metadata be a separate descriptor object from runtime capabilities? | Separate descriptor | `BackendDescriptor` holds name/version/dependencies/factory while `BackendCapabilities` stays runtime behavior-focused. | ✓ |
| Should backend metadata be a separate descriptor object from runtime capabilities? | Expand capabilities | Add version and dependency fields directly to `BackendCapabilities`; fewer types, but mixes static registry metadata with runtime capability flags. | |
| Should backend metadata be a separate descriptor object from runtime capabilities? | Flat registry entry | Use one `BackendRegistration` object for everything; simple enough, but less clear where capabilities end and registry metadata begins. | |
| How detailed should dependency requirements be in backend metadata for v1? | Package specs | Record optional Python package names/version specs plus human-readable install hint; enough for diagnostics without importing heavy modules. | ✓ |
| How detailed should dependency requirements be in backend metadata for v1? | Free text only | Store dependency notes as strings; flexible, but contract tests cannot inspect or assert missing requirements reliably. | |
| How detailed should dependency requirements be in backend metadata for v1? | Full env model | Model packages, CUDA, binaries, devices, env vars, and process requirements now; expressive, but likely too much before real backends exist. | |
| Should backend parameters be typed schemas or simple JSON-ready defaults for this phase? | JSON-ready defaults | Keep parameter metadata as immutable `Mapping[str, bool | int | float | str]` defaults/descriptions; consistent with current `MetricValue` and artifacts. | ✓ |
| Should backend parameters be typed schemas or simple JSON-ready defaults for this phase? | Typed schema objects | Define parameter descriptors with kind/default/range/required; more useful for real adapters, but heavier than needed for deterministic backend contracts. | |
| Should backend parameters be typed schemas or simple JSON-ready defaults for this phase? | No parameters | Leave parameter metadata out until real backend integration; simplest, but misses BACK-01 and current capabilities already expose parameters. | |
| How should out-of-process support be represented? | Metadata flag | Keep a boolean `runs_out_of_process` flag on descriptor and capabilities; this phase records the boundary without implementing process adapters. | ✓ |
| How should out-of-process support be represented? | Enum isolation mode | Use in-process/out-of-process/remote enum; clearer future vocabulary, but adds values not exercised by v1. | |
| How should out-of-process support be represented? | Defer it | Do not model out-of-process until real adapters; conflicts with BACK-01 and roadmap success criteria. | |

**User's choice:** Separate descriptor; package specs; JSON-ready defaults; metadata flag for out-of-process support.
**Notes:** User moved to next area after these decisions.

---

## Availability Checks

| Question | Option | Description | Selected |
|----------|--------|-------------|----------|
| How should availability checks determine whether a backend can run? | Declarative probes | `BackendDescriptor` carries lightweight probe callables that return `AvailabilityResult` without constructing the backend or importing heavy modules. | ✓ |
| How should availability checks determine whether a backend can run? | Import packages | Use importlib checks against declared packages; simple for Python deps, but not enough for CUDA/binary/device requirements and still couples checks to package names. | |
| How should availability checks determine whether a backend can run? | Instantiate backend | Create the backend and catch failures; catches real runtime problems, but risks importing heavy/native code during discovery. | |
| What should an availability result contain? | Status + reasons | Available bool plus machine-readable missing requirements and human-readable diagnostics/install_hint. | ✓ |
| What should an availability result contain? | Bool only | Return just True/False; easy to consume, but fails the roadmap need for unavailable-dependency diagnostics. | |
| What should an availability result contain? | Exception model | Raise typed exceptions for unavailable backends; useful for control flow, but awkward for listing/inspecting many backends. | |
| When should availability be checked by default? | On demand only | Registry listing is cheap and side-effect free; users call `availability(name)` when they want diagnostics. | ✓ |
| When should availability be checked by default? | During register | Validate availability at registration time; catches broken entries early, but makes registration import/probe-dependent. | |
| When should availability be checked by default? | During create | Check when creating a backend; safer than blind construction, but discovery still cannot show diagnostics unless separate listing exists. | |
| Should the deterministic backend have an explicit availability check? | Always available | Default descriptor returns `available=True` with empty missing requirements, proving the API path without optional deps. | ✓ |
| Should the deterministic backend have an explicit availability check? | No check needed | Skip availability for built-ins; simpler, but makes the default backend a special case. | |
| Should the deterministic backend have an explicit availability check? | Probe stdlib only | Run a trivial probe even for deterministic backend; works, but adds no useful information. | |

**User's choice:** Declarative probes; status plus reasons; on-demand availability; deterministic backend always available.
**Notes:** User moved to next area after these decisions.

---

## Contract Tests

| Question | Option | Description | Selected |
|----------|--------|-------------|----------|
| How should reusable backend contract tests be exposed? | Helper test suite | Provide reusable pytest helper/assertion functions that project tests can parametrize over registry entries without needing a Mosaic pytest plugin. | ✓ |
| How should reusable backend contract tests be exposed? | Pytest plugin | Expose plugin fixtures/markers; powerful, but adds packaging and plugin behavior before the library needs it. | |
| How should reusable backend contract tests be exposed? | Docs only | Document a pattern and keep tests internal; simpler, but does not satisfy reusable contract-test parametrization well. | |
| Which backend lifecycle behaviors must the contract helpers cover in phase 3? | Roadmap full set | Reset, process, snapshot, lost tracking, not-initialized behavior, diagnostics, deterministic replay, and availability gating. | ✓ |
| Which backend lifecycle behaviors must the contract helpers cover in phase 3? | Current behaviors only | Cover process/snapshot/reset/diagnostics only; matches current fake backend, but leaves roadmap lifecycle gaps unresolved. | |
| Which backend lifecycle behaviors must the contract helpers cover in phase 3? | Minimal smoke tests | Only check name/capabilities/process returns update; fast, but too weak for future backend substitution. | |
| How should contract tests handle unavailable optional backends? | Skip with reason | Contract parametrization checks availability first and skips unavailable backends with the `AvailabilityResult` diagnostic. | ✓ |
| How should contract tests handle unavailable optional backends? | Fail unavailable | Fail if any registered backend is unavailable; useful for CI with required extras, but hostile to optional backend discovery. | |
| How should contract tests handle unavailable optional backends? | Exclude manually | Users manually parametrize only available backends; simple, but loses the registry availability contract. | |
| What deterministic replay should contract tests use? | Synthetic sequence | Reuse the existing synthetic deterministic multi-view sequence/scenario so every backend sees the same observations and artifacts. | ✓ |
| What deterministic replay should contract tests use? | Inline fixture | Keep a tiny observation fixture inside slam tests; easy to localize, but duplicates existing evaluation/dataset utilities. | |
| What deterministic replay should contract tests use? | Backend-provided | Each backend provides its own test sequence; flexible, but weakens cross-backend comparability. | |

**User's choice:** Helper test suite; roadmap full lifecycle set; skip unavailable optional backends with reason; synthetic sequence replay.
**Notes:** User selected completion after this area.

---

## Claude's Discretion

None.

## Deferred Ideas

None.
