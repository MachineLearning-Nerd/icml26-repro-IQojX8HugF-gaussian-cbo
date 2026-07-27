import json
import subprocess
import sys
from pathlib import Path


def test_independent_cbo_dynamics_check_passes():
    root = Path(__file__).resolve().parents[2]
    subprocess.run([sys.executable, "repro/src/verify_dynamics.py"], cwd=root, check=True)
    result = json.loads((root / "outputs/independent_dynamics.json").read_text())
    assert result["c2_cbo_dynamics"]["pass"]
