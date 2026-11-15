"""Parametric enclosure for the ESP32-S3 smart plug (REV_A_PROVISIONAL).

This is a mechanical concept, not a certified electrical enclosure. Dimensions
are provisional and module envelopes are approximate. Do not energize mains in
a 3D-printed enclosure.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import cadquery as cq
import yaml

ROOT = Path(__file__).resolve().parents[3]
PARAMS = ROOT / "hardware" / "mechanical" / "parameters.yaml"
EXPORT = ROOT / "hardware" / "mechanical" / "export"
EXPORT.mkdir(parents=True, exist_ok=True)


def load_params(preset: str = "provisional") -> dict:
    data = yaml.safe_load(PARAMS.read_text(encoding="utf-8"))
    if preset == "recommended":
        data = {**data, **data.get("recommended", {})}
    return data


def _rounded_box(length: float, width: float, height: float, radius: float) -> cq.Workplane:
    box = cq.Workplane("XY").box(length, width, height, centered=(True, True, False))
    if radius > 0:
        box = box.edges("|Z").fillet(radius)
    return box


def _cutters(params: dict) -> list[cq.Workplane]:
    length = float(params["enclosure_length_mm"])
    width = float(params["width_mm"])
    wall = float(params["wall_thickness_mm"])
    oled_w, oled_h = params["oled_viewport_mm"]
    socket_w, socket_h, _ = params["socket_dimensions_mm"]
    cutters: list[cq.Workplane] = []

    # OLED window on the front face (y = -W/2). Use a through-block.
    cutters.append(
        cq.Workplane("XY").box(oled_w, wall * 4, oled_h).translate((-55, -width / 2, 40))
    )
    # Button and RGB holes through the front face, along +Y.
    cutters.append(
        cq.Workplane(obj=cq.Solid.makeCylinder(6.0, wall * 4, cq.Vector(-20, -width / 2 - wall, 34), cq.Vector(0, 1, 0)))
    )
    cutters.append(
        cq.Workplane(obj=cq.Solid.makeCylinder(3.0, wall * 4, cq.Vector(-5, -width / 2 - wall, 40), cq.Vector(0, 1, 0)))
    )
    # Socket opening on the back face (y = +W/2).
    cutters.append(
        cq.Workplane("XY").box(socket_w, wall * 4, socket_h).translate((45, width / 2, 40))
    )
    # M16 cable gland on the right side (mains entry).
    cutters.append(
        cq.Workplane(obj=cq.Solid.makeCylinder(8.0, wall * 4, cq.Vector(length / 2 + wall, 25, 18), cq.Vector(-1, 0, 0)))
    )
    # USB service opening on the left side (SELV). Cover required.
    cutters.append(
        cq.Workplane("XY").box(wall * 4, 12, 8).translate((-length / 2, -20, 18))
    )
    # Small side vents (not a substitute for thermal testing).
    for y in (-15, -5, 5, 15):
        cutters.append(cq.Workplane("XY").box(wall * 4, 2, 8).translate((-length / 2, y, 20)))
        cutters.append(cq.Workplane("XY").box(wall * 4, 2, 8).translate((length / 2, y, 20)))
    return cutters


def build_bottom(preset: str = "provisional") -> cq.Workplane:
    params = load_params(preset)
    length = float(params["enclosure_length_mm"])
    width = float(params["width_mm"])
    bottom_h = float(params["bottom_height_mm"])
    wall = float(params["wall_thickness_mm"])
    radius = float(params["corner_radius_mm"])
    body = _rounded_box(length, width, bottom_h, radius).faces(">Z").shell(-wall)

    # Mounting bosses + M3 clearance holes.
    holes = params["mounting_holes"]
    bosses = cq.Workplane("XY").pushPoints(holes).circle(3.5).extrude(7)
    body = body.union(bosses)
    body = body.faces(">Z").workplane().pushPoints(holes).hole(3.2)

    # Internal isolation barrier (mechanical wall; not a creepage calculation).
    barrier_x = float(params["barrier_x_mm"])
    barrier_h = float(params["barrier_height_mm"])
    barrier = (
        cq.Workplane("XY")
        .box(2.0, width - 2 * wall - 2, barrier_h, centered=(True, True, False))
        .translate((barrier_x, 0, wall))
    )
    body = body.union(barrier)
    # Wire pass-through in barrier (grommet required; provisional).
    pass_hole = cq.Workplane(obj=cq.Solid.makeCylinder(5.0, 10.0, cq.Vector(barrier_x - 5, 0, 10), cq.Vector(1, 0, 0)))
    body = body.cut(pass_hole)

    # PE stud boss (mechanical only; electrical bonding hardware not approved).
    pe_boss = cq.Workplane("XY").center(65, 42).circle(4).extrude(8)
    body = body.union(pe_boss)
    body = body.faces(">Z").workplane().center(65, 42).hole(3.2)

    for cutter in _cutters(params):
        body = body.cut(cutter)
    return body


def build_top(preset: str = "provisional") -> cq.Workplane:
    params = load_params(preset)
    length = float(params["enclosure_length_mm"])
    width = float(params["width_mm"])
    bottom_h = float(params["bottom_height_mm"])
    top_h = float(params["top_height_mm"])
    wall = float(params["wall_thickness_mm"])
    radius = float(params["corner_radius_mm"])
    body = _rounded_box(length, width, top_h, radius).faces("<Z").shell(-wall)
    body = body.translate((0, 0, bottom_h))
    for cutter in _cutters(params):
        body = body.cut(cutter)
    return body


def build_assembly(preset: str = "provisional") -> cq.Assembly:
    from components import module_list

    params = load_params(preset)
    assy = cq.Assembly(name=f"smartplug_{preset}")
    assy.add(build_bottom(preset), name="body_bottom", color=cq.Color(0.25, 0.55, 0.45, 1.0))
    assy.add(build_top(preset), name="body_top", color=cq.Color(0.35, 0.65, 0.55, 1.0))
    for module in module_list(preset):
        box = (
            cq.Workplane("XY")
            .box(module.size_mm[0], module.size_mm[1], module.size_mm[2], centered=(True, True, True))
            .translate(module.center_mm)
        )
        color = cq.Color(0.85, 0.2, 0.15, 0.55) if module.domain == "MAINS" else cq.Color(0.15, 0.45, 0.85, 0.45)
        assy.add(box, name=module.name, color=color)
    return assy


def export_preset(preset: str) -> None:
    bottom = build_bottom(preset)
    top = build_top(preset)
    assy = build_assembly(preset)
    cq.exporters.export(bottom, str(EXPORT / f"body_bottom_{preset}.step"), exportType="STEP")
    cq.exporters.export(bottom, str(EXPORT / f"body_bottom_{preset}.stl"), exportType="STL", tolerance=0.05)
    cq.exporters.export(top, str(EXPORT / f"body_top_{preset}.step"), exportType="STEP")
    cq.exporters.export(top, str(EXPORT / f"body_top_{preset}.stl"), exportType="STL", tolerance=0.05)
    assy.save(str(EXPORT / f"assembly_{preset}.step"))
    print(f"Exported {preset}: STEP/STL bodies + assembly STEP")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preset", choices=["provisional", "recommended", "both"], default="both")
    args = parser.parse_args()
    presets = ["provisional", "recommended"] if args.preset == "both" else [args.preset]
    for preset in presets:
        export_preset(preset)


if __name__ == "__main__":
    main()
