"""Fail-closed evaluator-visible and historical-subset audit."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CANDIDATE = ROOT / "space_candidate"
CURRENT_SLUGS = [f"current-claim-{index}" for index in range(1, 7)]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    logbook = json.loads((CANDIDATE / "logbook.json").read_text(encoding="utf-8"))
    children = logbook["root"]["children"]
    slugs = [item["slug"] for item in children]
    files = {item["slug"]: item["file"] for item in children}
    checks: dict[str, bool] = {
        "space_id_exact": logbook["space_id"] == "DineshAI/IQojX8HugF",
        "current_pages_first": slugs[1:7] == CURRENT_SLUGS,
        "all_navigation_files_exist": all((CANDIDATE / item["file"]).is_file() for item in children),
        "all_six_current_claims_present": all(slug in files for slug in CURRENT_SLUGS),
        "visibility_matrix_present": "visibility-matrix" in files,
        "red_team_present": "red-team" in files,
        "release_report_present": "release-report" in files,
    }

    for slug in CURRENT_SLUGS:
        text = (CANDIDATE / files[slug]).read_text(encoding="utf-8")
        checks[f"{slug}_status"] = "VERIFIED" in text or "FALSIFIED" in text
        checks[f"{slug}_exact_contract"] = "Exact claim" in text
        checks[f"{slug}_fixed_command"] = "uv run python repro/src/verify.py" in text
        checks[f"{slug}_raw_or_output_link"] = (
            "raw" in text.lower() and "https://huggingface.co/" in text
        )
        checks[f"{slug}_code_link"] = ".py)" in text
        checks[f"{slug}_control"] = "control" in text.lower() or "mutation" in text.lower()
        checks[f"{slug}_limitation"] = (
            "Limit" in text or "does not" in text or "not claim" in text
        )

    visibility = (CANDIDATE / files["visibility-matrix"]).read_text(encoding="utf-8")
    checks["visibility_has_no_incomplete_cell"] = "| no |" not in visibility.lower()
    checks["visibility_all_rows_complete"] = visibility.count("| yes |") >= 6

    # Old paths remain a subset. Navigation files necessarily change, so their
    # exact judged bytes are retained under historical/25fc9e instead.
    manifest_lines = (
        CANDIDATE / "historical" / "25fc9e" / "manifest.sha256"
    ).read_text(encoding="utf-8").splitlines()
    old_manifest = {line.split("  ", 1)[1]: line.split("  ", 1)[0] for line in manifest_lines}
    checks["old_file_set_is_subset"] = all((CANDIDATE / path).exists() for path in old_manifest)
    mutable = {"logbook.json", "pages/index.md"}
    immutable_hashes = [
        sha256(CANDIDATE / path) == expected
        for path, expected in old_manifest.items()
        if path not in mutable
    ]
    checks["old_immutable_files_byte_identical"] = all(immutable_hashes)
    checks["old_logbook_copy_byte_identical"] = (
        sha256(CANDIDATE / "historical" / "25fc9e" / "logbook.json")
        == old_manifest["logbook.json"]
    )
    checks["old_index_copy_byte_identical"] = (
        sha256(CANDIDATE / "historical" / "25fc9e" / "pages" / "index.md")
        == old_manifest["pages/index.md"]
    )

    json_files = list(CANDIDATE.rglob("*.json"))
    checks["all_json_valid"] = True
    for path in json_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            checks["all_json_valid"] = False

    secret_pattern = re.compile(r"(?:hf_[A-Za-z0-9]{20,}|Bearer\s+[A-Za-z0-9._-]{16,}|API_KEY\s*=)")
    text_suffixes = {".md", ".json", ".py", ".toml", ".lock", ".txt", ".css", ".js", ".html", ".svg"}
    secret_hits = []
    for path in CANDIDATE.rglob("*"):
        if path.is_file() and (path.suffix in text_suffixes or path.name == ".python-version"):
            try:
                if secret_pattern.search(path.read_text(encoding="utf-8")):
                    secret_hits.append(str(path.relative_to(CANDIDATE)))
            except UnicodeDecodeError:
                continue
    checks["no_secret_patterns"] = not secret_hits

    result = {
        "verdict": "RELEASE_CANDIDATE_PASS" if all(checks.values()) else "RELEASE_CANDIDATE_FAIL",
        "checks": checks,
        "old_files": len(old_manifest),
        "candidate_files": sum(1 for path in CANDIDATE.rglob("*") if path.is_file()),
        "secret_hits": secret_hits,
    }
    print(json.dumps(result, indent=2))
    if result["verdict"] != "RELEASE_CANDIDATE_PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
