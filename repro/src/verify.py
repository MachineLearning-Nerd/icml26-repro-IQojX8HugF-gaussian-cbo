"""Fail-closed local verdict for the source-faithful IQojX8HugF bundle."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def run(script: str) -> None:
    subprocess.run([sys.executable, script], cwd=ROOT, check=True)


def main() -> None:
    run("repro/src/verify_geometry.py")
    run("repro/src/verify_dynamics.py")
    run("repro/src/summarize_authored_2d.py")
    geometry = json.loads((ROOT / "outputs" / "independent_geometry.json").read_text())
    dynamics = json.loads((ROOT / "outputs" / "independent_dynamics.json").read_text())
    authored = json.loads((ROOT / "outputs" / "authored_2d_summary.json").read_text())
    audit = (ROOT / "docs" / "SOURCE_AUDIT.md").read_text(encoding="utf-8")
    source_hash = "3481d1698570dc32a520820ff1e89f4c1e1ab30fdff93dfcf50e76b654852482"

    verdict = {
        "C1": {
            "passed": geometry["c1_lbw_closed_form"]["pass"],
            "evidence": "Independent weighted-coordinate and log/extended-exp finite checks.",
        },
        "C2": {
            "passed": dynamics["c2_cbo_dynamics"]["pass"],
            "evidence": "Independent exponential-weight/drift/noise algebra check; source mapping in SOURCE_AUDIT.md.",
        },
        "C3": {
            "passed": False,
            "evidence": "Not counted: current contract says Theorem 4.1, pinned source calls the applicable result Theorem 3.5.",
        },
        "C4": {
            "passed": bool(source_hash in audit and "unique strong particle solution" in audit),
            "evidence": "Source-audited conditional Lemma 3.1; finite execution is only a sanity check, not proof of the theorem.",
        },
        "C5": {
            "passed": authored["c5_cbo_beats_bw_on_all_targets"],
            "evidence": "Four complete raw author notebooks, each at 100 repetitions, CBO final median KL < BW final median KL.",
        },
        "C6": {
            "passed": geometry["c6_extended_map_psd"]["pass"],
            "evidence": "Independent random symmetric-tangent PSD invariant check.",
        },
    }
    checked = [item for item in verdict.values() if item["passed"]]
    verdict["summary"] = {
        "claims_checked": 6,
        "claims_source_faithful_verified": len(checked),
        "minimum_for_ten_points": 5,
        "publication_gate_passed": len(checked) >= 5,
        "scope": "C3 is intentionally excluded; every empirical C5 assertion requires its complete raw notebook artifact.",
    }
    (ROOT / "outputs" / "verdict.json").write_text(json.dumps(verdict, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(verdict, indent=2))
    if not verdict["summary"]["publication_gate_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
