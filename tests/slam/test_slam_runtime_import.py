from __future__ import annotations

import os
import subprocess
import sys
import textwrap
from pathlib import Path


def test_slam_public_import_succeeds_without_pytest_importability() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    python_path = repo_root / "src"
    script = textwrap.dedent(
        """
        import builtins

        original_import = builtins.__import__

        def guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "pytest" or name.startswith("pytest."):
                raise ImportError("simulated runtime environment without pytest")
            return original_import(name, globals, locals, fromlist, level)

        builtins.__import__ = guarded_import

        import mosaic.slam

        helper_names = (
            "skip_unavailable_backend",
            "assert_backend_lifecycle_contract",
            "assert_backend_deterministic_replay",
            "assert_backend_state_update_contract",
        )
        for helper_name in helper_names:
            helper = getattr(mosaic.slam, helper_name)
            if not callable(helper):
                raise AssertionError(f"{helper_name} is not callable")
        """
    )

    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(python_path)
    result = subprocess.run(
        [sys.executable, "-c", script],
        check=False,
        env=environment,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr


def test_public_contract_helper_names_remain_importable_with_pytest_installed() -> None:
    from mosaic.slam import (
        assert_backend_deterministic_replay,
        assert_backend_lifecycle_contract,
        assert_backend_state_update_contract,
        skip_unavailable_backend,
    )

    assert callable(skip_unavailable_backend)
    assert callable(assert_backend_lifecycle_contract)
    assert callable(assert_backend_deterministic_replay)
    assert callable(assert_backend_state_update_contract)
