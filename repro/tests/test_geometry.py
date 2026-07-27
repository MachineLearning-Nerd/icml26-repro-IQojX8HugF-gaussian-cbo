import json
import subprocess
import sys
from pathlib import Path


def test_independent_geometry_checks_pass():
    root = Path(__file__).resolve().parents[2]
    subprocess.run([sys.executable, "repro/src/verify_geometry.py"], cwd=root, check=True)
    result = json.loads((root / "outputs/independent_geometry.json").read_text())
    assert result["c1_lbw_closed_form"]["pass"]
    assert result["c6_extended_map_psd"]["pass"]
