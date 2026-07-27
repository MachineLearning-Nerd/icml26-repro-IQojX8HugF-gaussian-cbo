"""Execute the exact released 100-repeat 2D comparison for each paper target.

The author notebook exposes one target through `test = "A"`.  This wrapper
loads the pinned notebook, changes only that selector in memory, and executes
its setup plus comparison cell (cells 0--5) with nbclient.  It deliberately
does not alter author code or reduce Ntests, steps, particles, baselines, or
the seed schedule.  One completed target notebook is atomically written before
the next target starts, avoiding a monolithic all-or-nothing artifact.
"""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

import nbformat
from nbclient import NotebookClient


ROOT = Path(__file__).resolve().parents[2]
UPSTREAM = ROOT / "repro" / "upstream"
SOURCE_NOTEBOOK = UPSTREAM / "experiment_2D.ipynb"


def execute_target(target: str, timeout: int) -> Path:
    notebook = nbformat.read(SOURCE_NOTEBOOK, as_version=4)
    notebook.cells = notebook.cells[:6]
    cell = notebook.cells[5]
    changed, substitutions = re.subn(r'(?m)^test = "A"$', f'test = "{target}"', "".join(cell.source))
    if substitutions != 1:
        raise RuntimeError(f"expected exactly one target selector, found {substitutions}")
    cell.source = changed
    # This post-comparison cell is deliberately I/O only.  It does not change
    # any source parameter or recompute the experiment; it preserves the four
    # full 100-run trajectory matrices that the notebook otherwise keeps only
    # in kernel memory.
    raw_name = f"../../outputs/authored_2d_{target}.raw.npz"
    raw_temporary_name = f"../../outputs/.authored_2d_{target}.raw.tmp"
    notebook.cells.append(
        nbformat.v4.new_code_cell(
            "# Reproduction wrapper: persist existing source-run arrays only.\n"
            "import os\n"
            f"with open({raw_temporary_name!r}, 'wb') as _raw_file:\n"
            "    np.savez_compressed(\n"
            "        _raw_file,\n"
            "        KL_bw_runs=KL_bw_runs,\n"
            "        KL_cbo_runs=KL_cbo_runs,\n"
            "        KL_svgd_runs=KL_svgd_runs,\n"
            "        KL_fr_runs=KL_fr_runs,\n"
            "    )\n"
            "    _raw_file.flush()\n"
            "    os.fsync(_raw_file.fileno())\n"
            f"os.replace({raw_temporary_name!r}, {raw_name!r})\n"
            f"print('raw trajectories: {raw_name}')"
        )
    )
    client = NotebookClient(notebook, timeout=timeout, kernel_name="python3", resources={"metadata": {"path": str(UPSTREAM)}})
    client.execute()
    output = ROOT / "outputs" / f"authored_2d_{target}.executed.ipynb"
    temporary = output.with_suffix(".tmp.ipynb")
    nbformat.write(notebook, temporary)
    os.replace(temporary, output)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--targets", nargs="+", choices=list("ABCD"), default=list("ABCD"))
    parser.add_argument("--timeout", type=int, default=3600)
    args = parser.parse_args()
    for target in args.targets:
        output = ROOT / "outputs" / f"authored_2d_{target}.executed.ipynb"
        raw_output = ROOT / "outputs" / f"authored_2d_{target}.raw.npz"
        if output.exists() and raw_output.exists():
            print(f"{target}: retained existing {output.relative_to(ROOT)}")
            continue
        if output.exists():
            print(f"{target}: existing notebook lacks raw arrays; rerunning complete deterministic source protocol")
        print(f"{target}: starting exact source protocol")
        result = execute_target(target, args.timeout)
        print(f"{target}: wrote {result.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
