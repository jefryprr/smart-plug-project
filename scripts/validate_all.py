#!/usr/bin/env python3
"""Single validation gate for digital artifacts.

Runs real commands, captures logs, and writes reports/TEST_MATRIX.csv,
reports/VALIDATION_SUMMARY.json, and reports/FAILURES.md.
Unavailable physical/tooling checks are BLOCKED, never silently skipped.
"""
from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
LOGS = REPORTS / "logs"
REPORTS.mkdir(exist_ok=True)
LOGS.mkdir(exist_ok=True)
PYTHON = ROOT / ".venv" / "Scripts" / "python.exe"
NPM = shutil.which("npm") or "npm"
POWERSHELL = shutil.which("powershell") or "powershell"

STEPS: list[dict] = []
START = datetime.now(timezone.utc)
STAMP = START.strftime("%Y%m%dT%H%M%SZ")


def run_step(test_id: str, area: str, command: list[str] | None, note: str, blocked: bool = False) -> dict:
    if blocked or command is None:
        result = {
            "test_id": test_id,
            "area": area,
            "command": "",
            "status": "BLOCKED",
            "exit_code": None,
            "log": "",
            "note": note,
            "duration_s": 0.0,
        }
        STEPS.append(result)
        print(f"[BLOCKED] {test_id} {area}: {note}")
        return result

    started = time.time()
    log_path = LOGS / f"{test_id}-{STAMP}.log"
    print(f"[RUN] {test_id} {area}: {' '.join(command)}")
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=600,
            shell=False,
        )
        output = (completed.stdout or "") + (completed.stderr or "")
        log_path.write_text(output, encoding="utf-8")
        status = "PASS" if completed.returncode == 0 else "FAIL"
        result = {
            "test_id": test_id,
            "area": area,
            "command": " ".join(command),
            "status": status,
            "exit_code": completed.returncode,
            "log": str(log_path.relative_to(ROOT)),
            "note": note,
            "duration_s": round(time.time() - started, 2),
        }
    except Exception as error:  # noqa: BLE001
        log_path.write_text(f"EXCEPTION: {error}\n", encoding="utf-8")
        result = {
            "test_id": test_id,
            "area": area,
            "command": " ".join(command),
            "status": "FAIL",
            "exit_code": None,
            "log": str(log_path.relative_to(ROOT)),
            "note": f"{note}; exception: {error}",
            "duration_s": round(time.time() - started, 2),
        }
    STEPS.append(result)
    print(f"[{result['status']}] {test_id} {area} ({result['duration_s']}s)")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--e2e", action="store_true", help="Run Playwright E2E (starts API/web/simulator)")
    parser.add_argument("--skip-build", action="store_true", help="Skip Next.js build")
    args = parser.parse_args()

    # Typechecks
    run_step("T-SW-001A", "TypeScript domain", [NPM, "run", "typecheck", "-w", "@smartplug/domain"], "Domain typecheck")
    run_step("T-SW-001B", "TypeScript API", [NPM, "run", "typecheck", "-w", "@smartplug/api"], "API typecheck")
    run_step("T-SW-001C", "TypeScript web", [NPM, "run", "typecheck", "-w", "@smartplug/web"], "Web typecheck")
    run_step("T-SW-001D", "TypeScript simulator", [NPM, "run", "typecheck", "-w", "@smartplug/device-simulator"], "Simulator typecheck")

    # Unit/integration tests
    run_step("T-SW-007", "Domain tests", [NPM, "run", "test", "-w", "@smartplug/domain"], "34 domain tests incl. cost/energy")
    run_step("T-SW-004A", "MQTT contract tests", [NPM, "run", "test", "-w", "@smartplug/mqtt-contract"], "11 contract/ACL tests")
    run_step("T-SW-005", "API + simulator integration", [NPM, "run", "test", "-w", "@smartplug/api"], "38 API tests incl. aedes+simulator ACK")
    run_step("T-SW-004B", "Simulator tests", [NPM, "run", "test", "-w", "@smartplug/device-simulator"], "4 simulator tests")

    # Firmware host core
    run_step(
        "T-HW-018",
        "Firmware core host tests",
        [POWERSHELL, "-ExecutionPolicy", "Bypass", "-File", str(ROOT / "firmware" / "test" / "host" / "run_tests.ps1")],
        "74 C checks; Zig cc host build",
    )

    # Build
    if not args.skip_build:
        run_step("T-SW-001E", "Next.js build", [NPM, "run", "build", "-w", "@smartplug/web"], "Next production build")
    else:
        run_step("T-SW-001E", "Next.js build", None, "Skipped by --skip-build", blocked=True)

    # Static crosschecks and generated artifacts
    run_step("T-HW-003", "Connectivity crosscheck", [str(PYTHON), "scripts/validate_connectivity.py"], "Wiring/GPIO/BOM static diff")
    run_step("T-HW-004", "GPIO map generation", [str(PYTHON), "hardware/generators/generate_gpio_map.py"], "GPIO CSV/MD + crosscheck")
    run_step("T-HW-010A", "WireViz render", [str(PYTHON), "scripts/render_wiring.py"], "6 harnesses SVG/PNG/PDF")
    run_step("T-HW-009A", "CadQuery export", [str(PYTHON), "hardware/mechanical/source/enclosure.py", "--preset", "both"], "STEP/STL bodies + assembly")
    run_step("T-HW-009B", "Mechanical render/fit", [str(PYTHON), "hardware/mechanical/source/render.py"], "Views/drawings/fit report")
    run_step(
        "T-HW-002A",
        "KiCad file parse",
        [str(PYTHON), "-c", "from pathlib import Path; from kiutils.schematic import Schematic; from kiutils.board import Board; import glob; [Schematic.from_file(p) for p in glob.glob('hardware/kicad/*.kicad_sch')]; Board.from_file('hardware/kicad/smartplug.kicad_pcb'); print('kiutils parse OK')"],
        "Native files parse; ERC/DRC not run",
    )
    run_step("T-HW-008A", "PCB placement preview", [str(PYTHON), "scripts/render_pcb_preview.py"], "Preview parsed from .kicad_pcb")
    run_step(
        "T-SW-001F",
        "OpenAPI parse",
        [str(PYTHON), "-c", "import yaml; d=yaml.safe_load(open('packages/api-contract/openapi.yaml', encoding='utf-8')); assert d['openapi'].startswith('3.'); assert len(d['paths'])>=18; print('OpenAPI paths:', len(d['paths']))"],
        "OpenAPI structural check",
    )

    # E2E (optional)
    if args.e2e:
        run_step("T-SW-011", "Playwright E2E", [NPM, "exec", "playwright", "test"], "5 E2E tests incl. axe and command APPLIED")
    else:
        run_step("T-SW-011", "Playwright E2E", None, "Run with --e2e to start API/web/simulator", blocked=True)

    # Physical/tooling blockers
    run_step("T-HW-002", "Schematic ERC", None, "KiCad CLI not installed", blocked=True)
    run_step("T-HW-006", "PCB DRC", None, "KiCad CLI not installed", blocked=True)
    run_step("T-HW-008", "Gerber/drill import", None, "KiCad CLI not installed; no fabrication package", blocked=True)
    run_step("T-HW-011", "Mains isolation review", None, "No qualified reviewer/lab evidence", blocked=True)
    run_step("T-HW-012", "PE continuity", None, "No hardware/lab", blocked=True)
    run_step("T-HW-013", "Thermal/fuse/surge", None, "No lab", blocked=True)
    run_step("T-HW-014", "Boot-safe waveform", None, "No board/scope", blocked=True)
    run_step("T-HW-017", "ESP-IDF clean build", None, "ESP-IDF not installed", blocked=True)
    run_step("T-HW-019", "Physical load/temperature", None, "No lab", blocked=True)
    run_step("T-SW-002", "PostgreSQL migration", None, "PostgreSQL/Docker not installed", blocked=True)
    run_step("T-SW-003", "MQTT broker auth/ACL", None, "Production broker/TLS not executed", blocked=True)
    run_step("T-SW-010", "Offline router/cloud test", None, "No deployed network stack", blocked=True)
    run_step("T-SW-013", "Android APK build", None, "Android SDK not installed", blocked=True)
    run_step("T-SW-020", "Deployment clean-room", None, "Docker/Postgres not installed", blocked=True)
    run_step("T-SW-025", "Full system HIL", None, "No hardware/lab", blocked=True)

    counts: dict[str, int] = {}
    for step in STEPS:
        counts[step["status"]] = counts.get(step["status"], 0) + 1

    matrix = REPORTS / "TEST_MATRIX.csv"
    with matrix.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["test_id", "area", "command", "status", "exit_code", "log", "note", "duration_s"])
        writer.writeheader()
        writer.writerows(STEPS)

    summary = {
        "project": "esp32-s3-iot-smart-plug",
        "design_revision": "REV_A_PROVISIONAL",
        "generated_at": START.isoformat(),
        "duration_s": round((datetime.now(timezone.utc) - START).total_seconds(), 2),
        "counts": counts,
        "overall": "PASS" if counts.get("FAIL", 0) == 0 else "FAIL",
        "note": "PASS is digital evidence only; BLOCKED items require hardware/lab/tooling.",
        "steps": STEPS,
    }
    (REPORTS / "VALIDATION_SUMMARY.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    failures = [step for step in STEPS if step["status"] in {"FAIL", "BLOCKED"}]
    lines = ["# Failures and Blockers", "", f"Generated: {START.isoformat()}", "", f"Overall: **{summary['overall']}**", ""]
    if not failures:
        lines.append("No failures or blockers recorded.")
    else:
        lines += ["| Test | Area | Status | Note | Log |", "|---|---|---|---|---|"]
        for step in failures:
            lines.append(f"| {step['test_id']} | {step['area']} | {step['status']} | {step['note']} | {step['log']} |")
    (REPORTS / "FAILURES.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({"overall": summary["overall"], "counts": counts}, indent=2))
    return 0 if summary["overall"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
