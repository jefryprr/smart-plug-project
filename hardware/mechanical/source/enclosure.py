"""Parametric 220 x 120 x 70 CORE_ONLY enclosure for a 300 x 300 mm printer.

Prototype mechanical design only. It is not a certified electrical enclosure.
The model is sized for the CORE_ONLY_SHOPEE shopping list:
- DV DSMS-2P-16A surface socket: 50x50 flange, 38x38 fixing, 45.6x45.6 cutout
- PZEM-004T V4 PCB approx 74 x 31 x 18 mm
- M3 x 5 mm heat-set inserts (8): 4 lid + 4 carrier
- M3 x 8 module screws, M3 x 16 lid screws, M4 PE stud
- No M12 vent fitted and no vent hole in this revision (deferred)
- 5 mm x 1 mm gasket in a body groove

Run:
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


def _box(dx: float, dy: float, dz: float, x: float, y: float, z: float) -> cq.Workplane:
    return cq.Workplane("XY").box(dx, dy, dz).translate((x, y, z))


def _ring(outer: tuple[float, float], inner: tuple[float, float], height: float, x: float, y: float, z: float) -> cq.Workplane:
    # z is the bottom of the ring.
    shell = _box(outer[0], outer[1], height, x, y, z + height / 2)
    hole = _box(inner[0], inner[1], height + 1.0, x, y, z + height / 2)
    return shell.cut(hole)


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

    # Lid screw bosses with M3x5 heat-set insert holes.
    for x, y in p["lid_screw_positions"]:
        body = body.union(_cylinder(float(p["lid_screw_boss_diameter_mm"]) / 2, bottom_h - wall, x, y, wall))
    for x, y in p["lid_screw_positions"]:
        body = body.cut(_cylinder(float(p["lid_insert_hole_mm"]) / 2, float(p["lid_insert_depth_mm"]), x, y, bottom_h - float(p["lid_insert_depth_mm"])))

    # Carrier bosses with M3x5 heat-set insert holes.
    for bx, by in p["pcb_hole_positions_board_mm"]:
        x, y = _board_to_enclosure(p, bx, by)
        body = body.union(_cylinder(float(p["carrier_standoff_diameter_mm"]) / 2, 5.5, x, y, wall))
        body = body.cut(_cylinder(float(p["carrier_insert_hole_mm"]) / 2, float(p["carrier_insert_depth_mm"]), x, y, wall))

    # Module bosses (self-tapping M3x8 into 2.5 mm pilots).
    for name, points in p["module_bosses"].items():
        top = float(p["module_boss_height_mm"][name])
        for x, y in points:
            body = body.union(_cylinder(float(p["module_boss_diameter_mm"]) / 2, top - wall, x, y, wall))
            body = body.cut(_cylinder(float(p["module_boss_pilot_mm"]) / 2, float(p["module_boss_pilot_depth_mm"]), x, y, top - float(p["module_boss_pilot_depth_mm"])))

    # PE stud boss: M4 clearance, not M3.
    pe_x, pe_y = p["pe_stud_xy"]
    body = body.union(_cylinder(float(p["pe_stud_boss_diameter_mm"]) / 2, float(p["pe_stud_height_mm"]) - wall, pe_x, pe_y, wall))
    body = body.cut(_cylinder(float(p["pe_stud_hole_mm"]) / 2, 20.0, pe_x, pe_y, wall))

    # Internal barrier with two grommet holes.
    barrier_x = float(p["barrier_x_mm"])
    barrier_h = float(p["barrier_height_mm"])
    y0, y1 = p["barrier_y_mm"]
    body = body.union(
        cq.Workplane("XY").box(2.0, y1 - y0, barrier_h, centered=(True, True, False)).translate((barrier_x, (y0 + y1) / 2, wall))
    )
    for hy, hz in p["barrier_hole_yz"]:
        body = body.cut(_cylinder(float(p["barrier_hole_diameter_mm"]) / 2, 4.0, barrier_x, hy, hz, axis=(1, 0, 0)))

    # DV surface socket: round 45.6 mm cutout, 50x50 flange land, 38x38 M4 fixing.
    sx, sy, sz = p["socket_center"]
    cw, ch = p["socket_cutout_mm"]
    # Round cutout: a square 45.6 corner would remove the 38x38 fixing bosses.
    body = body.cut(_cylinder(max(cw, ch) / 2, 12.0, 104.0, sy, sz, axis=(1, 0, 0)))
    fw, fh = p["socket_flange_mm"]
    body = body.cut(_box(float(p["socket_flange_recess_mm"]), fw, fh, 110.0 - float(p["socket_flange_recess_mm"]) / 2, sy, sz))
    fx, fz = p["socket_fixing_mm"]
    boss_depth = float(p["socket_boss_depth_mm"])
    boss_outer_x = 107.5  # inner face of the right wall
    boss_start = boss_outer_x - boss_depth
    for dy in (-fx / 2, fx / 2):
        for dz in (-fz / 2, fz / 2):
            body = body.union(_cylinder(float(p["socket_boss_diameter_mm"]) / 2, boss_depth, boss_start, sy + dy, sz + dz, axis=(1, 0, 0)))
            # M4 self-tapping pilot in the printed boss (do not use a clearance hole).
            body = body.cut(_cylinder(float(p["socket_screw_pilot_mm"]) / 2, boss_depth, boss_start, sy + dy, sz + dz, axis=(1, 0, 0)))
            # 4.5 mm clearance through the wall + outer 2 mm of the boss.
            body = body.cut(_cylinder(float(p["socket_screw_hole_mm"]) / 2, 5.0, 105.5, sy + dy, sz + dz, axis=(1, 0, 0)))

    # M16 cable gland on the back wall (away from socket/PSU).
    gx, gy, gz = p["cable_gland_center"]
    body = body.union(_cylinder(float(p["cable_gland_boss_diameter_mm"]) / 2, float(p["cable_gland_boss_depth_mm"]), gx, 57.5, gz, axis=(0, -1, 0)))
    body = body.cut(_cylinder(float(p["cable_gland_thread_mm"]) / 2, 12.0, gx, 60.0, gz, axis=(0, -1, 0)))

    # No M12 vent fitted and no vent hole in this revision. Add a vent only
    # after a thermal/IP review and a new model revision.

    # Onboard RGB left-wall window.
    wx, wy, wz = p["devkit_rgb_window_center"]
    body = body.cut(_cylinder(float(p["devkit_rgb_window_diameter_mm"]) / 2, 3.0, -110.0, wy, wz, axis=(1, 0, 0)))

    # Front USB service opening.
    ux, uy, uz = p["usb_cover_center"]
    uw, uh = p["usb_cover_opening_mm"]
    body = body.cut(_box(uw, 12.0, uh, ux, uy, uz))

    # Relay shelf wall bosses, inside the wall (no through-wall holes).
    for bx, by, bz in p["relay_shelf_bosses"]:
        body = body.union(_cylinder(float(p["relay_shelf_boss_diameter_mm"]) / 2, float(p["relay_shelf_boss_depth_mm"]), 101.5, by, bz, axis=(1, 0, 0)))
        body = body.cut(_cylinder(float(p["relay_shelf_pilot_mm"]) / 2, float(p["relay_shelf_boss_depth_mm"]), 101.5, by, bz, axis=(1, 0, 0)))

    # Flat gasket land: the lid ring presses the 1 mm sheet against the rim.
    # No union ring here; keeping the shell manifold avoids non-manifold STL edges.
    # Gasket compression/sealing is UNVERIFIED until a physical leak test.

    # Shallow label recess on the front wall.
    body = body.cut(_box(90.0, 0.8, 18.0, 20.0, -59.6, 45.0))
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

    # 5 mm gasket land on the lid underside.
    outer = (length - 2.0, width - 2.0)
    lid = lid.union(_ring(outer, (outer[0] - 10.0, outer[1] - 10.0), 2.5, 0, 0, bottom_h))

    # Lid screws: clearance + counterbore from the top face.
    for x, y in p["lid_screw_positions"]:
        lid = lid.cut(_cylinder(float(p["lid_screw_clearance_mm"]) / 2, 12.0, x, y, bottom_h - 1.0))
        lid = lid.cut(_cylinder(float(p["lid_screw_counterbore_diameter_mm"]) / 2, float(p["lid_screw_counterbore_depth_mm"]), x, y, 70.0 - float(p["lid_screw_counterbore_depth_mm"])))

    # Top UI cutout: physical button only.
    bx, by = p["button_center_xy"]
    lid = lid.cut(_cylinder(float(p["button_diameter_mm"]) / 2, 6.0, bx, by, 67.0))
    return lid


def build_gasket() -> cq.Workplane:
    p = load_params()
    ow, oh = p["gasket_outer_mm"]
    iw, ih = p["gasket_inner_mm"]
    t = float(p["gasket_thickness_mm"])
    return _ring((float(ow), float(oh)), (float(iw), float(ih)), t, 0, 0, 0)


def build_usb_cover() -> cq.Workplane:
    p = load_params()
    ux, uy, uz = p["usb_cover_center"]
    uw, uh = p["usb_cover_opening_mm"]
    plate = _box(uw + 6, 3, uh + 6, ux, uy + 1.5, uz)
    lip = _box(uw, 5, uh, ux, uy - 1.5, uz)
    cover = plate.union(lip)
    for x in (ux - uw / 2 + 1, ux + uw / 2 - 1):
        cover = cover.cut(_cylinder(1.6, 6.0, x, uy, uz, axis=(0, 1, 0)))
    return cover


def build_devkit_key() -> cq.Workplane:
    p = load_params()
    arm = _box(8, 63, 3, -99, 0, 20.5)
    leg_a = _box(8, 8, 11, -99, -31.5, 14.5)
    leg_b = _box(8, 8, 11, -99, 31.5, 14.5)
    key = arm.union(leg_a).union(leg_b)
    for y in (-31.5, 31.5):
        key = key.cut(_cylinder(1.6, 12.0, -99, y, 10.0))
    return key


def build_assembly() -> cq.Assembly:
    from components import module_list

    assy = cq.Assembly(name="smartplug_core_only_shopee")
    assy.add(build_bottom(), name="body_bottom", color=cq.Color(0.25, 0.55, 0.45, 1.0))
    assy.add(build_top(), name="body_top", color=cq.Color(0.35, 0.65, 0.55, 1.0))
    assy.add(build_gasket().translate((0, 0, 59.2)), name="gasket", color=cq.Color(0.75, 0.75, 0.75, 1.0))
    assy.add(build_usb_cover(), name="usb_cover", color=cq.Color(0.4, 0.4, 0.4, 1.0))
    assy.add(build_devkit_key(), name="devkit_key", color=cq.Color(0.2, 0.2, 0.2, 1.0))
    assy.add(cq.Workplane("XY").box(100, 70, 1.6).translate((-55, 0, 8.8)), name="carrier_pcb", color=cq.Color(0.1, 0.5, 0.2, 0.9))
    for module in module_list():
        if module.name in {"carrier", "esp32", "devkit_key"}:
            continue
        box = cq.Workplane("XY").box(module.size_mm[0], module.size_mm[1], module.size_mm[2]).translate(module.center_mm)
        color = cq.Color(0.85, 0.2, 0.15, 0.55) if module.domain == "MAINS" else cq.Color(0.15, 0.45, 0.85, 0.45)
        assy.add(box, name=module.name, color=color)
    return assy


def export_all() -> None:
    for name, part in {
        "body_bottom_recommended": build_bottom(),
        "body_top_recommended": build_top(),
        "gasket": build_gasket(),
        "usb_cover": build_usb_cover(),
        "devkit_key": build_devkit_key(),
    }.items():
        cq.exporters.export(part, str(EXPORT / f"{name}.step"), exportType="STEP")
        cq.exporters.export(part, str(EXPORT / f"{name}.stl"), exportType="STL", tolerance=0.05)
    build_assembly().save(str(EXPORT / "assembly_recommended.step"))
    print("Exported CORE_ONLY_SHOPEE enclosure, lid, gasket, USB cover, DevKit key, assembly STEP")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preset", choices=["recommended", "both"], default="recommended")
    parser.parse_args()
    export_all()


if __name__ == "__main__":
    main()
