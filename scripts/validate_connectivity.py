#!/usr/bin/env python3
"""Crosscheck wiring YAML, GPIO map, BOM, and isolation assumptions.

This is a static consistency check, not a KiCad netlist and not a safety proof.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
VALIDATION = ROOT / "validation"
VALIDATION.mkdir(parents=True, exist_ok=True)
WIRING = ROOT / "hardware" / "wiring"
GPIO = ROOT / "hardware" / "interfaces" / "gpio_map.yaml"
BOARD = ROOT / "firmware" / "main" / "board_config.h"
BOM = ROOT / "bom" / "BOM_MASTER.csv"
BOM_PCBA = ROOT / "hardware" / "manufacturing" / "provisional" / "BOM_PCBA.csv"


class UnionFind:
    def __init__(self) -> None:
        self.parent: dict[str, str] = {}

    def find(self, item: str) -> str:
        self.parent.setdefault(item, item)
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, first: str, second: str) -> None:
        root_a = self.find(first)
        root_b = self.find(second)
        if root_a != root_b:
            self.parent[root_b] = root_a


def load_wiring() -> tuple[list[dict], UnionFind]:
    uf = UnionFind()
    rows: list[dict] = []
    for source in sorted(WIRING.glob("*.yaml")):
        data = yaml.safe_load(source.read_text(encoding="utf-8"))
        for index, connection in enumerate(data.get("connections", [])):
            if len(connection) < 2:
                continue
            left = connection[0]
            for right in connection[1:]:
                left_name = next(iter(left))
                right_name = next(iter(right))
                left_pins = left[left_name]
                right_pins = right[right_name]
                if not isinstance(left_pins, list):
                    left_pins = [left_pins]
                if not isinstance(right_pins, list):
                    right_pins = [right_pins]
                if len(left_pins) != len(right_pins):
                    rows.append({
                        "file": source.name, "connection": index,
                        "status": "PIN_COUNT_MISMATCH",
                        "from": left_name, "to": right_name
                    })
                    continue
                for left_pin, right_pin in zip(left_pins, right_pins):
                    left_node = f"{left_name}:{left_pin}"
                    right_node = f"{right_name}:{right_pin}"
                    uf.union(left_node, right_node)
                    rows.append({
                        "file": source.name, "connection": index,
                        "from": left_node, "to": right_node,
                        "cable": left_name if left_name.startswith("W") else right_name,
                        "wire": left_pin if left_name.startswith("W") else right_pin
                    })
    return rows, uf


def nets_from_uf(uf: UnionFind) -> dict[str, list[str]]:
    nets: dict[str, list[str]] = {}
    for node in uf.parent:
        root = uf.find(node)
        nets.setdefault(root, []).append(node)
    return nets


def net_containing(nets: dict[str, list[str]], node: str) -> list[str]:
    for members in nets.values():
        if node in members:
            return members
    return []


def check_gpio() -> dict:
    data = yaml.safe_load(GPIO.read_text(encoding="utf-8"))
    defines: dict[str, int] = {}
    for match in re.finditer(r"^#define\s+(PIN_[A-Z0-9_]+)\s+(\d+)", BOARD.read_text(encoding="utf-8"), re.M):
        defines[match.group(1)] = int(match.group(2))
    issues: list[str] = []
    for pin in data["pins"]:
        define = pin["firmware_define"]
        expected = int(pin["esp_gpio"])
        actual = defines.get(define)
        if actual is None:
            issues.append(f"MISSING_FIRMWARE_DEFINE:{define}")
        elif actual != expected:
            issues.append(f"GPIO_MISMATCH:{define}:map={expected}:firmware={actual}")
    return {
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "board_revision_verified": bool(data["board"].get("verified_board_revision")),
        "checked_defines": len(defines),
        "limitations": ["Board revision is unverified; static compare only."]
    }


def check_bom() -> dict:
    with BOM.open(newline="", encoding="utf-8") as handle:
        master = list(csv.DictReader(handle))
    with BOM_PCBA.open(newline="", encoding="utf-8") as handle:
        pcba = list(csv.DictReader(handle))
    master_refs = set()
    for row in master:
        for ref in row["reference_designators"].split(","):
            ref = ref.strip()
            if ref:
                master_refs.add(ref)
    pcba_refs = {row["reference_designators"].strip() for row in pcba}
    missing = sorted(pcba_refs - master_refs)
    unpriced = sum(1 for row in master if not row["price_idr_per_unit"])
    unapproved = [row["item_id"] for row in master if "APPROVED" not in row["approved_status"]]
    return {
        "status": "PASS" if not missing else "FAIL",
        "master_rows": len(master),
        "pcba_rows": len(pcba),
        "missing_refs_in_master": missing,
        "unpriced_lines": unpriced,
        "unapproved_lines": len(unapproved),
        "approved_for_fabrication": 0,
        "limitations": ["Engineering BOM is unpriced; bom/BOM_PROCUREMENT.csv is a dated listing matrix, not a supplier quote."]
    }


def main() -> int:
    rows, uf = load_wiring()
    nets = nets_from_uf(uf)
    checks: dict[str, Any] = {}

    pe_net = net_containing(nets, "P1:PE")
    checks["pe_path"] = {
        "status": "PASS" if "X1:PE" in pe_net and not any(node.startswith(("F1:", "K1:", "TF1:")) for node in pe_net) else "FAIL",
        "members": pe_net,
        "rule": "PE must connect input to output without relay/fuse/thermal cutoff."
    }
    checks["relay_contacts_separate"] = {
        "status": "PASS" if "K1:NO1" not in net_containing(nets, "K1:COM1") and "K1:NO2" not in net_containing(nets, "K1:COM2") else "FAIL",
        "note": "NO contacts must be separate nets before/after switching."
    }
    checks["relay_coil_selv"] = {
        "status": "PASS" if "K1:IN1" in net_containing(nets, "J3:RELAY_IN1") and "K1:IN2" in net_containing(nets, "J3:RELAY_IN2") else "FAIL",
        "note": "Relay module inputs are driven from SELV GPIO through the carrier MOSFET; J3 pins 3/4 are tied on the PCB."
    }
    pzem_mains = {"U2:L", "U2:N", "P1:L", "P1:N"}
    pzem_ttl = {"U2:+5V", "U2:GND", "U2:TX", "U2:RX", "J2:PZEM_TX_5V", "J2:PZEM_RX_5V", "U9:1A", "U9:1Y"}
    isolation_failures = []
    for members in nets.values():
        if any(node in pzem_mains for node in members) and any(node in pzem_ttl for node in members):
            isolation_failures.append(members)
    checks["pzem_isolation"] = {
        "status": "PASS" if not isolation_failures else "FAIL",
        "failures": isolation_failures,
        "note": "No net may short PZEM mains terminals to its TTL side. PZEM internal optocouplers are the barrier."
    }
    mains_nodes = {"P1:L", "P1:N", "PS1:L", "PS1:N", "PS2:L", "PS2:N", "K1:COM1", "K1:NO1", "K1:COM2", "K1:NO2", "X1:L", "X1:N", "U2:L", "U2:N"}
    selv_nodes = {"J8:+5V", "J8:GND", "J3:+5V", "J3:GND", "J3:RELAY_IN1", "J3:RELAY_IN2", "PSU_J5:+5V", "PSU_J5:GND", "PSU_J6:+5V", "PSU_J6:GND", "PSU_J7:+5V", "PSU_J7:GND", "K1:IN1", "K1:IN2", "K1:VCC", "K1:GND", "U9:VCC", "U9:GND", "U9:1A", "U9:1Y"}
    cross_domain = []
    for members in nets.values():
        if any(node in mains_nodes for node in members) and any(node in selv_nodes for node in members):
            cross_domain.append(members)
    checks["mains_selv_separation"] = {
        "status": "PASS" if not cross_domain else "FAIL",
        "failures": cross_domain,
        "note": "Static net check only; does not prove PCB/enclosure creepage."
    }
    checks["gpio_crosscheck"] = check_gpio()
    checks["bom_crosscheck"] = check_bom()
    checks["overall_status"] = "PASS" if all(check.get("status") == "PASS" for check in checks.values() if isinstance(check, dict)) else "FAIL"

    with (VALIDATION / "WIRING_CONNECTIONS.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["file", "connection", "from", "to", "cable", "wire", "status"])
        writer.writeheader()
        writer.writerows(rows)

    with (VALIDATION / "NETLIST_SCHEMATIC.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["net_id", "members", "source", "status"])
        for index, (root, members) in enumerate(sorted(nets.items()), start=1):
            writer.writerow([f"NET-{index:03d}", " | ".join(sorted(members)), "WIRING_DERIVED", "PROVISIONAL"])

    (VALIDATION / "CONNECTIVITY_DIFF.json").write_text(json.dumps(checks, indent=2), encoding="utf-8")

    lines = [
        "# Isolation Boundary Check — REV_C_PSU_BOARD",
        "",
        "**Status:** static wiring check only. Manual engineering review is still required.",
        "",
        f"- Overall static status: **{checks['overall_status']}**",
        f"- PE path: **{checks['pe_path']['status']}**",
        f"- Relay contacts separate: **{checks['relay_contacts_separate']['status']}**",
        f"- Relay coil SELV: **{checks['relay_coil_selv']['status']}**",
        f"- PZEM internal isolation (static): **{checks['pzem_isolation']['status']}**",
        f"- Mains/SELV separation: **{checks['mains_selv_separation']['status']}**",
        f"- GPIO crosscheck: **{checks['gpio_crosscheck']['status']}**",
        f"- BOM crosscheck: **{checks['bom_crosscheck']['status']}**",
        "",
        "## Limitations",
        "- This is not a KiCad netlist, ERC, or DRC.",
        "- It does not prove creepage, clearance, dielectric strength, PE continuity, or thermal safety.",
        "- Wiring YAML is a design intent; physical harness must be continuity-tested by a qualified person.",
        "- `PASS` here means static consistency only.",
        "- PSU OUT3 (J7) is conditional on PZEM batch inspection + hipot/leakage (ADR-016).",
        "- The PSU board fuse/MOV/TCO are board-level parts, not harness nodes; their order is checked by `scripts/validate_psu.py`.",
    ]
    (VALIDATION / "ISOLATION_BOUNDARY_CHECK.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    (VALIDATION / "COMPONENT_CROSSCHECK.json").write_text(json.dumps(checks["bom_crosscheck"], indent=2), encoding="utf-8")
    print(json.dumps({key: value.get("status") if isinstance(value, dict) else value for key, value in checks.items()}, indent=2))
    return 0 if checks["overall_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
