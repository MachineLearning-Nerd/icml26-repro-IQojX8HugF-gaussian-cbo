"""Read the raw executed author notebooks without rerunning or modifying them."""

from __future__ import annotations

import json
import re
from pathlib import Path

import nbformat
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
SUMMARY_RE = re.compile(
    r"Ntests\s*=\s*(?P<ntests>\d+).*?"
    r"CBO:\s+median start=(?P<cbo_start>[-+0-9.eE]+), final=(?P<cbo_final>[-+0-9.eE]+).*?"
    r"BW:\s+median start=(?P<bw_start>[-+0-9.eE]+), final=(?P<bw_final>[-+0-9.eE]+).*?"
    r"SVGD:\s+median start=(?P<svgd_start>[-+0-9.eE]+), final=(?P<svgd_final>[-+0-9.eE]+).*?"
    r"FR:\s+median start=(?P<fr_start>[-+0-9.eE]+), final=(?P<fr_final>[-+0-9.eE]+)",
    re.DOTALL,
)


def read_target(target: str) -> dict[str, object]:
    path = ROOT / "outputs" / f"authored_2d_{target}.executed.ipynb"
    raw_path = ROOT / "outputs" / f"authored_2d_{target}.raw.npz"
    notebook = nbformat.read(path, as_version=4)
    streams = "\n".join(
        str(output.get("text", ""))
        for cell in notebook.cells
        for output in cell.get("outputs", [])
        if output.output_type == "stream"
    )
    errors = [
        {"cell": index, "ename": output.ename, "evalue": output.evalue}
        for index, cell in enumerate(notebook.cells)
        for output in cell.get("outputs", [])
        if output.output_type == "error"
    ]
    match = SUMMARY_RE.search(streams)
    if errors or not match:
        raise RuntimeError(f"{target}: missing complete summary or contains notebook errors: {errors}")
    if not raw_path.is_file():
        raise RuntimeError(f"{target}: missing raw source trajectory artifact: {raw_path}")
    with np.load(raw_path) as raw:
        expected_shapes = {
            "KL_bw_runs": (100, 201),
            "KL_cbo_runs": (100, 201),
            "KL_svgd_runs": (100, 801),
            "KL_fr_runs": (100, 401),
        }
        raw_shapes = {name: list(raw[name].shape) for name in expected_shapes if name in raw.files}
        if raw_shapes != {name: list(shape) for name, shape in expected_shapes.items()} or not all(
            np.isfinite(raw[name]).all() for name in expected_shapes
        ):
            raise RuntimeError(f"{target}: malformed/non-finite raw trajectory arrays: {raw_shapes}")
    values = match.groupdict()
    result: dict[str, object] = {
        "notebook": str(path.relative_to(ROOT)),
        "raw_trajectories": str(raw_path.relative_to(ROOT)),
        "raw_shapes": raw_shapes,
        "errors": errors,
    }
    result.update({key: int(value) if key == "ntests" else float(value) for key, value in values.items()})
    result["cbo_beats_bw_final"] = bool(result["cbo_final"] < result["bw_final"])
    result["all_four_baselines_present"] = True
    return result


def main() -> None:
    targets = {target: read_target(target) for target in "ABCD"}
    passed = all(
        row["ntests"] == 100 and row["all_four_baselines_present"] and row["cbo_beats_bw_final"]
        for row in targets.values()
    )
    output = {
        "protocol": "author experiment_2D.ipynb cells 0--5; only test selector changed in memory",
        "targets": targets,
        "c5_cbo_beats_bw_on_all_targets": passed,
        "scope": "Median final-KL comparison only; this does not claim universal superiority over every baseline or target.",
    }
    (ROOT / "outputs" / "authored_2d_summary.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
