#!/usr/bin/env python3
"""Static BOM-vs-enclosure verification for the CORE_ONLY_SHOPEE print package.

This is a geometry/BOM consistency check, not a safety or fit validation.
Run with the project venv (trimesh/cadquery installed).
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import cadquery as cq
import trimesh
import yaml

ROOT = Path(__file__).resolve().parents[2]
MECH = ROOT / "hardware" / "mechanical"
CSV = ROOT / "bom" / "CORE_ONLY_SHOPEE_SHOPPING_LIST.csv"
OUT = MECH / "BOM_FIT_CHECK.json"


def main() -> None:
    params = yaml.safe_load((MECH / "parameters.yaml").read_text(encoding="utf-8"))
    rows = list(csv.DictReader(CSV.open(encoding="utf-8-sig")))
    by_name = {r["nama_barang"]: r for r in rows}
    issues: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            issues.append(message)

    check(params["socket_flange_mm"] == [50.0, 50.0], "socket flange != 50x50")
    check(params["socket_fixing_mm"] == [38.0, 38.0], "socket fixing != 38x38")
    check(params["socket_cutout_mm"] == [45.6, 45.6], "socket cutout != 45.6")
    check(params["socket_cutout_shape"].startswith("round"), "socket cutout not marked round")
    check(params["pe_stud_hole_mm"] == 4.3, "PE hole != 4.3 for M4")
    check(params["lid_insert_hole_mm"] == 4.2, "lid insert hole != 4.2")
    check(params["carrier_insert_hole_mm"] == 4.2, "carrier insert hole != 4.2")
    check(params["socket_screw_pilot_mm"] == 3.3, "socket screw pilot != 3.3 for M4 self-tapping")
    check(params["socket_boss_depth_mm"] >= 10.0, "socket boss too shallow for M4x16")
    check(params.get("vent_fitted") is False, "vent must be false/absent")

    # Wall-feature clearance: the gland hole must not cut into the PE boss.
    gx, _gy, gz = params["cable_gland_center"]
    pe_x, pe_y = params["pe_stud_xy"]
    gland_hole = cq.Solid.makeCylinder(
        float(params["cable_gland_thread_mm"]) / 2.0,
        12.0,
        cq.Vector(gx, 60.0, gz),
        cq.Vector(0, -1, 0),
    )
    pe_boss = cq.Solid.makeCylinder(
        float(params["pe_stud_boss_diameter_mm"]) / 2.0,
        float(params["pe_stud_height_mm"]),
        cq.Vector(pe_x, pe_y, float(params["wall_thickness_mm"])),
        cq.Vector(0, 0, 1),
    )
    gland_pe_overlap = gland_hole.intersect(pe_boss).Volume()
    check(gland_pe_overlap < 1.0, f"gland hole intersects PE boss by {gland_pe_overlap:.2f} mm3")

    socket = next((r for r in rows if "DSMS-2P-16A" in r["nama_barang"]), None)
    check(socket is not None, "socket row not found in CSV")
    if socket:
        check("50x50" in socket["spesifikasi_singkat"], "CSV socket flange not 50x50")
        check("38x38" in socket["spesifikasi_singkat"], "CSV socket fixing not 38x38")
        check("45.6" in socket["spesifikasi_singkat"], "CSV socket cutout not 45.6")
    check(any(r["nama_barang"].startswith("Baut M4x16 socket") and int(r["qty_pakai"]) == 4 for r in rows), "4x socket M4 screws missing")
    check(any("M12 ePTFE" in r["nama_barang"] and int(r["qty_pakai"]) == 0 for r in rows), "M12 vent must be qty 0")
    check(any("Nylon standoff" in r["nama_barang"] and int(r["qty_pakai"]) == 0 for r in rows), "nylon standoff must be optional qty 0")

    sizes = {}
    for name in ["body_bottom_recommended.stl", "body_top_recommended.stl", "gasket.stl", "usb_cover.stl", "devkit_key.stl", "pzem_bracket.stl", "psu_bracket.stl", "relay_shelf.stl"]:
        path = MECH / "export" / name
        check(path.exists(), f"missing {name}")
        if path.exists():
            mesh = trimesh.load(path, force="mesh")
            sizes[name] = {"watertight": bool(mesh.is_watertight), "bounds_mm": mesh.bounds.round(2).tolist()}
            check(bool(mesh.is_watertight), f"{name} not watertight")
    body = sizes.get("body_bottom_recommended.stl", {}).get("bounds_mm")
    if body:
        check(abs((body[1][0] - body[0][0]) - 220.0) < 0.5, "body X != 220")
        check(abs((body[1][1] - body[0][1]) - 120.0) < 0.5, "body Y != 120")
        check(abs((body[1][2] - body[0][2]) - 60.0) < 0.5, "body Z != 60")

    check((MECH / "export" / "CORE_ONLY_SHOPEE_PRINT_PACKAGE.zip").exists(), "print package zip missing")

    result = {
        "artifact": "hardware/mechanical/BOM_FIT_CHECK.json",
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
        "socket": {
            "flange_mm": params["socket_flange_mm"],
            "fixing_mm": params["socket_fixing_mm"],
            "cutout_mm": params["socket_cutout_mm"],
            "cutout_shape": params["socket_cutout_shape"],
            "note": "round cutout used because a square 45.6 would remove the 38x38 fixing bosses",
            "boss_depth_mm": params["socket_boss_depth_mm"],
            "boss_diameter_mm": params["socket_boss_diameter_mm"],
            "screw_pilot_mm": params["socket_screw_pilot_mm"],
        },
        "gland_pe_overlap_mm3": round(gland_pe_overlap, 3),
        "mesh": sizes,
        "limitations": [
            "BOM text and parameter consistency only; not a measured fit.",
            "Socket/PZEM/relay dimensions must be measured on received parts.",
            "Socket body cross-section/passage through the round 45.6 cutout is not checked.",
            "No thermal, IP, hipot, PE, or mechanical strength test.",
            "Not for mains use.",
        ],
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": result["status"], "issues": issues}, indent=2))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
