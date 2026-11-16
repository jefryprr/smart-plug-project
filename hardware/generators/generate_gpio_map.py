#!/usr/bin/env python3
"""Generate GPIO CSV/Markdown and a crosscheck report from gpio_map.yaml."""
from __future__ import annotations

import csv
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "hardware" / "interfaces" / "gpio_map.yaml"
CSV_OUT = ROOT / "hardware" / "interfaces" / "gpio_map.csv"
MD_OUT = ROOT / "hardware" / "interfaces" / "gpio_map.md"
CHECK_OUT = ROOT / "validation" / "GPIO_CROSSCHECK.json"

FIELDS = [
    "function", "board_pin_name", "physical_header", "esp_gpio", "direction",
    "voltage_level", "external_pull", "boot_default", "hazard_if_high",
    "peripheral", "firmware_define", "schematic_ref", "test",
    "verified_board_revision", "notes",
]


def main() -> None:
    data = yaml.safe_load(SRC.read_text(encoding="utf-8"))
    pins = data["pins"]
    reserved = set()
    for item in data.get("reserved", []):
        reserved.update(int(pin) for pin in item.get("pins", []))

    hard_issues: list[str] = []
    soft_issues: list[str] = []
    seen: dict[int, str] = {}
    for pin in pins:
        gpio = int(pin["esp_gpio"])
        if gpio in seen:
            hard_issues.append(f"DUPLICATE_GPIO:{gpio}:{seen[gpio]}:{pin['function']}")
        seen[gpio] = pin["function"]
        if gpio in reserved:
            hard_issues.append(f"RESERVED_GPIO_USED:{gpio}:{pin['function']}")
        if pin.get("verified_board_revision") is None:
            soft_issues.append(f"BOARD_REVISION_UNVERIFIED:{pin['function']}")

    status = "FAIL" if hard_issues else ("UNVERIFIED" if soft_issues else "PASS")
    issues = hard_issues + soft_issues
    check = {
        "artifact": "validation/GPIO_CROSSCHECK.json",
        "design_revision": data["design_revision"],
        "board": data["board"],
        "pin_count": len(pins),
        "duplicate_or_reserved_issues": hard_issues,
        "unverified_board_revision_issues": soft_issues,
        "firmware_header": data["crosscheck"]["firmware_header"],
        "schematic": data["crosscheck"]["schematic"],
        "wiring": data["crosscheck"]["wiring"],
        "status": status,
        "limitations": [
            "Board revision is unverified; all GPIO assignments are PROVISIONAL.",
            "No physical waveform or boot test was performed.",
            "Firmware header crosscheck is static; it does not prove electrical behavior."
        ],
    }
    CHECK_OUT.parent.mkdir(parents=True, exist_ok=True)
    CHECK_OUT.write_text(json.dumps(check, indent=2), encoding="utf-8")

    with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        for pin in pins:
            row = {field: pin.get(field, "") for field in FIELDS}
            row["verified_board_revision"] = pin.get("verified_board_revision") or ""
            writer.writerow(row)

    lines = [
        "# GPIO Map — REV_C_PSU_BOARD",
        "",
        f"**Board:** {data['board']['model']} ({data['board']['revision']})",
        f"**Status:** `{status}`",
        "",
        "> Nomor GPIO belum final sampai board fisik/revisi diverifikasi. Jangan menganggap GPIO48/38 sebagai kebenaran universal.",
        "",
        "| Function | GPIO | Direction | Pull/Boot | Hazard if high | Firmware define |",
        "|---|---:|---|---|---|---|",
    ]
    for pin in pins:
        lines.append(
            f"| {pin['function']} | {pin['esp_gpio']} | {pin['direction']} | {pin['external_pull']} / {pin['boot_default']} | {pin['hazard_if_high']} | `{pin['firmware_define']}` |"
        )
    lines += [
        "",
        "## Reserved",
        "",
        "| Pins | Reason |",
        "|---|---|",
    ]
    for item in data.get("reserved", []):
        lines.append(f"| {', '.join(str(p) for p in item['pins'])} | {item['reason']} |")
    lines += [
        "",
        "## Crosscheck",
        "",
        f"- Firmware header: `{data['crosscheck']['firmware_header']}`",
        f"- Schematic: `{data['crosscheck']['schematic']}`",
        f"- Wiring: `{data['crosscheck']['wiring']}`",
        f"- Issues: {len(issues)}",
        "",
        "**Catatan:** tabel ini adalah rencana, bukan bukti pengukuran. Boot-safe waveform dan I2C/UART scan wajib di bench low-voltage.",
    ]
    MD_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Generated {CSV_OUT.name}, {MD_OUT.name}, {CHECK_OUT.name}; status={status}; issues={len(issues)}")


if __name__ == "__main__":
    main()
