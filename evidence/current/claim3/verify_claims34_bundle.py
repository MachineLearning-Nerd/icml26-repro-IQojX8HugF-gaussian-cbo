"""Generate and independently check exact-source Claim 3/4 evidence."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    subprocess.run([sys.executable, "repro/src/verify_claims34.py"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "repro/src/check_claims34.py"], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
