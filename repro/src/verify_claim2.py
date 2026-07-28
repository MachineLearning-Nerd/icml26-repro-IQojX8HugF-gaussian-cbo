"""Generate and independently check the full multi-step Claim 2 evidence."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    subprocess.run([sys.executable, "repro/src/run_claim2_dynamics.py"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "repro/src/check_claim2.py"], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
