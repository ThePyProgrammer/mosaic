# External Integrations

**Analysis Date:** 2026-05-18

## APIs & External Services

**Current runtime services:**
- None detected - `src/mosaic/__init__.py` contains only a local `hello() -> str` function, and `pyproject.toml` declares no runtime dependencies.
  - SDK/Client: Not detected
  - Auth: Not applicable

**Planned / implied research backend integrations:**
- Gaussian Splatting SLAM backend implementations - Planned through a pluggable backend protocol rather than a selected SDK; `docs/argus-migration-plan.md:20-28` calls for capability metadata, parameter schemas, availability checks, and contract tests.
  - SDK/Client: Not selected; no `gsplat`, `nerfstudio`, PyTorch, or CUDA backend package is declared in `pyproject.toml`.
  - Auth: Not applicable
- Heavy native/CUDA backend isolation - Planned as an architectural seam for fragile research code in `docs/argus-migration-plan.md:30-36`.
  - SDK/Client: Not implemented
  - Auth: Not applicable

**Planned / implied robotics and dataset integrations:**
- Multi-view sequence datasets - Planned under proposed `src/mosaic/datasets/` in `docs/argus-migration-plan.md:91-103`, with deterministic replay expected in `docs/argus-migration-plan.md:115-117` and `docs/argus-migration-plan.md:163`.
  - SDK/Client: Not implemented
  - Auth: Not applicable
- Robot/camera-rig platform descriptions - Planned under proposed `src/mosaic/platforms/` in `docs/argus-migration-plan.md:38-47` and `docs/argus-migration-plan.md:129-137`.
  - SDK/Client: Not implemented; no ROS, simulator, or robot SDK dependency is declared.
  - Auth: Not applicable

**Research reference integrations present only in documents:**
- Argus source references - `docs/argus-migration-plan.md` references existing Argus protocol, platform, coordination, contract-test, and research documents at `/home/prannayag/pragnition/robotics/argus/...`; these are design references, not imported dependencies.
  - SDK/Client: Not applicable
  - Auth: Not applicable
- ARNA replication plan references GPT-4o, GPT-4o-mini, Habitat Lab, HM3D, MP3D/Matterport3D, HM-EQA, RxR-CE, and Grounding DINO in `outputs/arna-2506-17462-replication.md:17-21` and `outputs/arna-2506-17462-replication.md:73-89`; this is an output research plan and not integrated into `src/mosaic/`.
  - SDK/Client: Not implemented in Mosaic
  - Auth: Not applicable to current package

## Data Storage

**Databases:**
- None detected.
  - Connection: Not applicable
  - Client: Not applicable

**File Storage:**
- Local filesystem only.
- Documentation lives in `docs/` and `outputs/`.
- Package source lives in `src/mosaic/`.
- No runtime file persistence API is implemented in `src/mosaic/__init__.py`.

**Caching:**
- None detected.

## Authentication & Identity

**Auth Provider:**
- None detected.
  - Implementation: No auth code, identity provider SDK, token config, `.env` file, or secrets file is present in the current repository scan.

## Monitoring & Observability

**Error Tracking:**
- None detected.

**Logs:**
- No logging framework or logging configuration detected.
- Current package code in `src/mosaic/__init__.py` performs no logging.
- Future evaluation artifacts are implied by `docs/argus-migration-plan.md:139-147`, which calls for machine-readable metrics and regression gates, but no implementation exists yet.

## CI/CD & Deployment

**Hosting:**
- Not detected.
- Current repository contains no Dockerfile, deployment manifest, service config, or package publishing workflow.

**CI Pipeline:**
- None detected.
- No `.github/workflows/`, GitLab CI, pre-commit config, tox, nox, or test runner config was found in the scanned checkout.

## Environment Configuration

**Required env vars:**
- None required by current source code.
- Future CUDA/native backend selection may need environment configuration, but no variable names are defined in the repository.
- Future LLM/API-based agent integrations are implied by the broader research context but no current Mosaic env vars, SDKs, or clients exist.

**Secrets location:**
- Not detected.
- No root `.env` or `.env.*` file was found during safe existence-only scanning.
- Do not add API keys or robot credentials to tracked project files; future integrations should document variable names without committing values.

## Webhooks & Callbacks

**Incoming:**
- None detected.
- No web server, HTTP routing, CLI callback, ROS topic subscription, or webhook endpoint exists in `src/mosaic/`.

**Outgoing:**
- None detected.
- Current package code performs no network calls, SDK calls, subprocess calls, database calls, or robot middleware calls.

---

*Integration audit: 2026-05-18*
