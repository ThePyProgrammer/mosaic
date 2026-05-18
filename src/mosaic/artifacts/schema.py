from __future__ import annotations

ArtifactDict = dict[str, object]
SCHEMA_VERSION = 1


def make_artifact(schema: str, payload: dict[str, object]) -> ArtifactDict:
    return {
        "schema": schema,
        "schema_version": SCHEMA_VERSION,
        "payload": dict(payload),
    }


def require_artifact(artifact: object, schema: str) -> dict[str, object]:
    if not isinstance(artifact, dict):
        raise ValueError("artifact must be a dict")
    if artifact.get("schema") != schema:
        raise ValueError("artifact schema does not match expected schema")
    if artifact.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("artifact schema_version is not supported")
    payload = artifact.get("payload")
    if not isinstance(payload, dict):
        raise ValueError("artifact payload must be a dict")
    return dict(payload)
