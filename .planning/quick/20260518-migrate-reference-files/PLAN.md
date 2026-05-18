# Migrate Reference Files Quick Plan

Goal: Move untracked reference files from `docs/` and `outputs/` into `.planning/references/` while preserving content and committing origin groups separately.

Groups:
- Argus migration reference: `docs/argus-migration-plan.md` -> `.planning/references/argus/argus-migration-plan.md`
- Superpowers reference plans/specs: `docs/superpowers/**` -> `.planning/references/superpowers/**`
- ARNA investigation output: `outputs/arna-2506-17462-replication.md` -> `.planning/references/arna/arna-2506-17462-replication.md`

Checks:
- Use `cmp` before deleting source files.
- Commit each origin group separately.
- Update `.planning/STATE.md` quick-task table after migration.
