import pytest

from mosaic.artifacts import make_artifact, require_artifact


def _timestamp_artifact() -> dict[str, object]:
    return make_artifact("mosaic.timestamp", {"nanoseconds": 123})


def test_make_artifact_creates_versioned_envelope() -> None:
    assert _timestamp_artifact() == {
        "schema": "mosaic.timestamp",
        "schema_version": 1,
        "payload": {"nanoseconds": 123},
    }


def test_require_artifact_returns_payload_for_expected_schema() -> None:
    assert require_artifact(_timestamp_artifact(), "mosaic.timestamp") == {"nanoseconds": 123}


def test_require_artifact_rejects_unknown_schema() -> None:
    with pytest.raises(ValueError, match="schema"):
        require_artifact(_timestamp_artifact(), "mosaic.pose3")


def test_require_artifact_rejects_unknown_schema_version() -> None:
    artifact = _timestamp_artifact()
    artifact["schema_version"] = 2

    with pytest.raises(ValueError, match="schema_version"):
        require_artifact(artifact, "mosaic.timestamp")
