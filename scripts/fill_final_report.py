#!/usr/bin/env python3
"""Fill the FR table and source commit in the final report from actual data."""
from __future__ import annotations

import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "deliverables" / "FINAL_ENGINEERING_REPORT.md"
TRACE = ROOT / "requirements" / "traceability.yaml"


def main() -> None:
    data = yaml.safe_load(TRACE.read_text(encoding="utf-8"))
    rows = ["| FR | Priority | Phase | Status | Description | Key implementation | Tests |", "|---|---|---|---|---|---|---|"]
    for item in data["requirements"]:
        paths = ", ".join(f"`{path}`" for path in item.get("implementation_paths", [])[:2]) or "—"
        tests = ", ".join(item.get("test_ids", [])) or "—"
        description = str(item["description"]).replace("|", "\\|")
        rows.append(
            f"| {item['id']} | {item['priority']} | {item['phase']} | {item['status']} | {description} | {paths} | {tests} |"
        )
    table = "\n".join(rows)
    text = REPORT.read_text(encoding="utf-8")
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    text = text.replace("{{FR_TABLE}}", table).replace("{{GIT_COMMIT}}", commit)
    REPORT.write_text(text, encoding="utf-8")
    print(f"Filled {len(data['requirements'])} FR rows; source commit {commit}")


if __name__ == "__main__":
    main()
