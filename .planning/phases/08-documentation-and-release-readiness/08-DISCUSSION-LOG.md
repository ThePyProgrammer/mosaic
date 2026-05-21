# Phase 8: Documentation and Release Readiness - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-21
**Phase:** 8-Documentation and Release Readiness
**Areas discussed:** Doc shape, E2E example, Boundary wording, Contributor policy

---

## Doc Shape

| Question | Options Presented | User's Choice | Notes |
|----------|-------------------|---------------|-------|
| Where should Phase 8 put the release-facing documentation? | README primary; Split docs; You decide | Split docs | Use more than README for release readiness. |
| What split should downstream agents plan for? | README + contributing; README + docs; Release guide; You decide | README + docs | README overview plus dedicated API/examples/contributor docs. |
| How should README relate to the dedicated docs? | README concise; README complete; README index | README concise | README remains orientation and golden-path entry point. |
| Should Phase 8 add machine checks for the new docs beyond the existing README contract test? | Docs contract tests; README tests only; You decide | Docs contract tests | Split docs should be test-guarded against drift. |

---

## E2E Example

| Question | Options Presented | User's Choice | Notes |
|----------|-------------------|---------------|-------|
| What should the canonical minimal end-to-end example optimize for? | One golden path; API tour; Benchmark first | One golden path | Prefer a connected flow over scattered API snippets. |
| Which agent-facing endpoint should the golden path end with? | Posterior query; Memory query; Both briefly; You decide | Memory query | Reflect Phase 7 representation-memory/tool layer. |
| Should the golden path write real local artifacts, or keep output purely in-memory? | Write artifact; In-memory only; Both variants | Write artifact | Include benchmark artifact behavior in public docs. |
| How executable should the example be? | Copy-paste script; Narrative snippet; Test-backed only | Narrative snippet | Readable and API-accurate, but not necessarily standalone. |

---

## Boundary Wording

| Question | Options Presented | User's Choice | Notes |
|----------|-------------------|---------------|-------|
| What tone should the release boundary use for deferred integrations? | Blunt explicit; Soft roadmap; Minimal caveat | Blunt explicit | Name deferred integrations clearly. |
| How should docs describe the deterministic backend and fusion strategy? | Contract fixtures; Reference impls; Tutorial-only | Contract fixtures | Avoid production-SLAM or optimization-quality claims. |
| How should the docs present Phase 7 representation memories relative to posterior views? | Separate layers; Unified agents; Memory-first | Separate layers | Posterior views and representation memories are distinct provider-free layers. |
| Should Phase 8 update stale phase-era wording like Phase 1 baseline and Phase 7 planned? | Release versioned; Keep phases; Hybrid | Release versioned | Public docs should describe current v1 behavior, not phase chronology. |

---

## Contributor Policy

| Question | Options Presented | User's Choice | Notes |
|----------|-------------------|---------------|-------|
| What should contributor guidance emphasize first? | Dependency boundary; API stability; Test workflow; All equal | All equal | Dependency boundaries, API stability, and tests share top priority. |
| How should optional extras guidance be framed for future heavy integrations? | Policy only; Stub extras; No extras talk | Policy only | Explain future optional integration policy without adding placeholder extras. |
| What should contributors be told about adding public APIs? | Docs + exports + tests; Subpackage first; Planner discretion | Docs + exports + tests | Public APIs require docs, export decisions, and tests. |
| Should contributor docs describe how to extend real backends now, or only the contract boundary? | Boundary only; Extension sketch; Detailed guide | Boundary only | Stop at registry/adapter seam, availability checks, and contract tests. |

---

## Claude's Discretion

- Exact dedicated doc filenames may vary if the split-doc intent remains clear.
- Exact doc-test organization may vary if tests stay deterministic and low-maintenance.
- Planner may decide how much golden-path detail belongs in README versus deeper docs.

## Deferred Ideas

None.
