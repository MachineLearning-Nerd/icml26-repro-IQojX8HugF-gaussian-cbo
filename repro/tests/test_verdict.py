import json
import subprocess
import sys
from pathlib import Path

import pytest


def test_full_verdict_requires_all_authored_artifacts():
    root = Path(__file__).resolve().parents[2]
    if any(not (root / "outputs" / f"authored_2d_{target}.executed.ipynb").exists() for target in "ABCD"):
        pytest.skip("full source-scale notebook suite is still running")
    subprocess.run([sys.executable, "repro/src/verify.py"], cwd=root, check=True)
    result = json.loads((root / "outputs" / "verdict.json").read_text())
    assert result["summary"]["publication_gate_passed"]
    assert result["C3"]["passed"] is False
