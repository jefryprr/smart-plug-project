"""Parametric 220 x 120 x 70 enclosure for the REV_D_CORE_ONLY smart plug.

This is a mechanical concept, not a certified electrical enclosure. It adds a
deep body, shallow lid, flat gasket, lid screws, carrier standoffs, module
bosses, an isolation barrier, panel cutouts, a USB service cover and a DevKit
reverse-insertion key. Dimensions are provisional until measured samples and
physical tests exist.

Run with CadQuery's Python:
  .venv\\Scripts\\python.exe hardware\\mechanical\\source\\enclosure.py --preset recommended
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


def load_params() -> dict:
    return yaml.safe_load(PARAMS.read_text(encoding="utf-8"))


def _rounded_box(length: float, width: float, height: float, radius: float) -> cq.Workplane:
    box = cq.Workplane("XY").box(length, width, height, centered=(True, True, False))
    if radius > 0:
        box = box.edges("|Z").fillet(radius)
    return box


def _cylinder(radius: float, height: float, x: float, y: float, z: float, axis: tuple[float, float, float] = (0, 0, 1)) -> cq.Workplane:
    solid = cq.Solid.makeCylinder(radius, height, cq.Vector(x, y, z), cq.Vector(*axis))
    return cq.Workplane(obj=solid)


def _board_to_enclosure(params: dict, bx: float, by: float) -> tuple[float, float]:
    ox, oy = params["pcb_origin_mm"]
    return (ox + bx, oy + by)


def build_bottom() -> cq.Workplane:
    p = load_params()
    length = float(p["enclosure_length_mm"])
    width = float(p["width_mm"])
    bottom_h = float(p["bottom_height_mm"])
    wall = float(p["wall_thickness_mm"])
    radius = float(p["corner_radius_mm"])

    body = _rounded_box(length, width, bottom_h, radius).faces(">Z").shell(-wall)

    # Lid screw bosses, from the floor to the rim.
    for x, y in p["lid_screw_positions"]:
        boss = _cylinder(float(p["lid_screw_boss_diameter_mm"]) / 2, bottom_h - wall, x, y, wall)
        body = body.union(boss)
    for x, y in p["lid_screw_positions"]:
        pilot = _cylinder(float(p["lid_screw_pilot_mm"]) / 2, 12.0, x, y, bottom_h - 10.0)
        body = body.cut(pilot)

    # Carrier standoffs at the PCB mounting holes.
    for bx, by in p["pcb_hole_positions_board_mm"]:
        x, y = _board_to_enclosure(p, bx, by)
        standoff = _cylinder(float(p["carrier_standoff_diameter_mm"]) / 2, 5.5, x, y, wall)
        body = body.union(standoff)
        pilot = _cylinder(float(p["carrier_standoff_pilot_mm"]) / 2, 5.0, x, y, 3.5)
        body = body.cut(pilot)

    # Module bosses. Heights are measured from the enclosure floor.
    for name, points in p["module_bosses"].items():
        height = float(p["module_boss_height_mm"][name])
        for x, y in points:
            boss = _cylinder(float(p["module_boss_diameter_mm"]) / 2, height - wall, x, y, wall)
            body = body.union(boss)
            pilot = _cylinder(float(p["module_boss_pilot_mm"]) / 2, 5.0, x, y, max(wall, height - 5.0))
            body = body.cut(pilot)

    # PE stud boss.
    pe_x, pe_y = p["pe_stud_xy"]
    pe_boss = _cylinder(float(p["pe_stud_boss_diameter_mm"]) / 2, float(p["pe_stud_height_mm"]), pe_x, pe_y, wall)
    body = body.union(pe_boss)
    body = body.cut(_cylinder(float(p["pe_stud_hole_mm"]) / 2, 12.0, pe_x, pe_y, wall))

    # Isolation barrier with two grommet holes.
    barrier_x = float(p["barrier_x_mm"])
    barrier_h = float(p["barrier_height_mm"])
    y0, y1 = p["barrier_y_mm"]
    barrier = (
        cq.Workplane("XY")
        .box(2.0, y1 - y0, barrier_h, centered=(True, True, False))
        .translate((barrier_x, (y0 + y1) / 2, wall))
    )
    body = body.union(barrier)
    for hy, hz in p["barrier_hole_yz"]:
        body = body.cut(_cylinder(float(p["barrier_hole_diameter_mm"]) / 2, 4.0, barrier_x, hy, hz, axis=(1, 0, 0)))

    # Socket opening on the right wall.
    sx, sy, sz = p["socket_center"]
    cw, ch = p["socket_cutout_mm"]
    body = body.cut(cq.Workplane("XY").box(12, cw, ch).translate((110, sy, sz)))

    # M16 gland and M12 pressure vent on the right wall.
    gx, gy, gz = p["cable_gland_center"]
    body = body.cut(_cylinder(float(p["cable_gland_diameter_mm"]) / 2, 12.0, gx, gy, gz, axis=(-1, 0, 0)))
    vx, vy, vz = p["vent_center"]
    body = body.cut(_cylinder(float(p["vent_diameter_mm"]) / 2, 12.0, vx, vy, vz, axis=(-1, 0, 0)))

    # Onboard DevKitC-1 v1.0 RGB window on the left wall (provisional position).
    wx, wy, wz = p["devkit_rgb_window_center"]
    body = body.cut(_cylinder(float(p["devkit_rgb_window_diameter_mm"]) / 2, 8.0, wx, wy, wz, axis=(1, 0, 0)))

    # Front USB service opening (cover is a separate printed part).
    ux, uy, uz = p["usb_cover_center"]
    uw, uh = p["usb_cover_opening_mm"]
    body = body.cut(cq.Workplane("XY").box(uw, 12, uh).translate((ux, uy, uz)))

    # Shallow label recess on the front wall.
    body = body.cut(cq.Workplane("XY").box(90, 0.8, 18).translate((20, -59.6, 45)))
    return body


def build_top() -> cq.Workplane:
    p = load_params()
    length = float(p["enclosure_length_mm"])
    width = float(p["width_mm"])
    bottom_h = float(p["bottom_height_mm"])
    top_h = float(p["top_height_mm"])
    wall = float(p["wall_thickness_mm"])
    radius = float(p["corner_radius_mm"])

    lid = _rounded_box(length, width, top_h, radius).translate((0, 0, bottom_h))
    lid = lid.faces("<Z").shell(-wall)

    # Lid screws: clearance + counterbore from the top face.
    for x, y in p["lid_screw_positions"]:
        lid = lid.cut(_cylinder(3.2 / 2, 12.0, x, y, bottom_h - 1))
        lid = lid.cut(_cylinder(float(p["lid_screw_counterbore_diameter_mm"]) / 2, float(p["lid_screw_counterbore_depth_mm"]), x, y, 70.0 - float(p["lid_screw_counterbore_depth_mm"])))

    # Top UI cutout: physical button only (CORE-only, no OLED/external RGB).
    bx, by = p["button_center_xy"]
    lid = lid.cut(_cylinder(float(p["button_diameter_mm"]) / 2, 6.0, bx, by, 67))
    return lid


def build_gasket() -> cq.Workplane:
    p = load_params()
    outer_w = float(p["enclosure_length_mm"]) - 4.0
    outer_h = float(p["width_mm"]) - 4.0
    inner_w = outer_w - 5.0
    inner_h = outer_h - 5.0
    t = float(p["gasket_thickness_mm"])
    ring = cq.Workplane("XY").box(outer_w, outer_h, t).translate((0, 0, 60.0 - t / 2))
    inner = cq.Workplane("XY").box(inner_w, inner_h, t + 1).translate((0, 0, 60.0 - t / 2))
    return ring.cut(inner)


def build_usb_cover() -> cq.Workplane:
    p = load_params()
    ux, uy, uz = p["usb_cover_center"]
    uw, uh = p["usb_cover_opening_mm"]
    plate = cq.Workplane("XY").box(uw + 6, 3, uh + 6).translate((ux, uy + 1.5, uz))
    lip = cq.Workplane("XY").box(uw, 5, uh).translate((ux, uy - 1.5, uz))
    cover = plate.union(lip)
    for x in (ux - uw / 2 + 1, ux + uw / 2 - 1):
        cover = cover.cut(_cylinder(1.6, 6.0, x, uy, uz, axis=(0, 1, 0)))
    return cover


def build_devkit_key() -> cq.Workplane:
    p = load_params()
    # Arm just above the DevKit antenna end; legs land on the two left carrier
    # mounting holes. Reverse insertion brings the USB connectors into the arm.
    arm = cq.Workplane("XY").box(8, 63, 3).translate((-99, 0, 20.5))
    leg_a = cq.Workplane("XY").box(8, 8, 11).translate((-99, -31.5, 14.5))
    leg_b = cq.Workplane("XY").box(8, 8, 11).translate((-99, 31.5, 14.5))
    key = arm.union(leg_a).union(leg_b)
    for y in (-31.5, 31.5):
        key = key.cut(_cylinder(1.6, 12.0, -99, y, 10.0))
    return key


def build_assembly() -> cq.Assembly:
    from components import module_list

    assy = cq.Assembly(name="smartplug_recommended")
    assy.add(build_bottom(), name="body_bottom", color=cq.Color(0.25, 0.55, 0.45, 1.0))
    assy.add(build_top(), name="body_top", color=cq.Color(0.35, 0.65, 0.55, 1.0))
    assy.add(build_gasket(), name="gasket", color=cq.Color(0.75, 0.75, 0.75, 1.0))
    assy.add(build_usb_cover(), name="usb_cover", color=cq.Color(0.4, 0.4, 0.4, 1.0))
    assy.add(build_devkit_key(), name="devkit_key", color=cq.Color(0.2, 0.2, 0.2, 1.0))
    assy.add(
        cq.Workplane("XY").box(100, 70, 1.6).translate((-55, 0, 8.8)),
        name="carrier_pcb",
        color=cq.Color(0.1, 0.5, 0.2, 0.9),
    )
    for module in module_list():
        if module.name in {"carrier", "esp32", "devkit_key"}:
            continue
        box = (
            cq.Workplane("XY")
            .box(module.size_mm[0], module.size_mm[1], module.size_mm[2], centered=(True, True, True))
            .translate(module.center_mm)
        )
        color = cq.Color(0.85, 0.2, 0.15, 0.55) if module.domain == "MAINS" else cq.Color(0.15, 0.45, 0.85, 0.45)
        assy.add(box, name=module.name, color=color)
    return assy


def export_all() -> None:
    bottom = build_bottom()
    top = build_top()
    gasket = build_gasket()
    usb_cover = build_usb_cover()
    devkit_key = build_devkit_key()
    assy = build_assembly()
    for name, part in {
        "body_bottom_recommended": bottom,
        "body_top_recommended": top,
        "gasket": gasket,
        "usb_cover": usb_cover,
        "devkit_key": devkit_key,
    }.items():
        cq.exporters.export(part, str(EXPORT / f"{name}.step"), exportType="STEP")
        cq.exporters.export(part, str(EXPORT / f"{name}.stl"), exportType="STL", tolerance=0.05)
    assy.save(str(EXPORT / "assembly_recommended.step"))
    print("Exported recommended: enclosure, lid, gasket, USB cover, DevKit key, assembly STEP")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preset", choices=["recommended", "both"], default="recommended")
    args = parser.parse_args()
    export_all()


if __name__ == "__main__":
    main()
