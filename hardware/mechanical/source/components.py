"""Approximate module envelopes and fit checks for the 220 x 120 x 70 build.

Dimensions are datasheet/engineering estimates, not measured samples. Positions
are in enclosure coordinates: origin at the enclosure centre, z=0 at the outer
bottom. The carrier board origin maps to (-105, -35), so board (x, y) becomes
enclosure (x - 105, y - 35).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class ModuleEnvelope:
    name: str
    label: str
    size_mm: tuple[float, float, float]
    center_mm: tuple[float, float, float]
    domain: str  # MAINS | SELV | MECHANICAL
    provenance: str
    notes: str = ""

    @property
    def bounds(self) -> tuple[float, float, float, float, float, float]:
        x, y, z = self.center_mm
        sx, sy, sz = self.size_mm
        return (x - sx / 2, y - sy / 2, z - sz / 2, x + sx / 2, y + sy / 2, z + sz / 2)


# Enclosure: 220 x 120 x 70 outer, 2.5 mm wall, bottom 60 mm, lid 10 mm.
MODULES: list[ModuleEnvelope] = [
    # SELV side (left). Carrier origin (-105, -35), board 100 x 70.
    ModuleEnvelope("carrier", "SELV carrier PCB 100 x 70", (100, 70, 1.6), (-55, 0, 8.8), "SELV", "pcb_design"),
    ModuleEnvelope("esp32", "ESP32-S3-DevKitC-1 (63 x 25.5 approx)", (63, 25.5, 10), (-68.33, -13.57, 22.0), "SELV", "datasheet_approx"),
    ModuleEnvelope("button", "Panel button + cap", (12, 12, 8), (-62, 28, 63.5), "SELV", "provisional"),
    ModuleEnvelope("devkit_rgb_window", "Onboard RGB left-wall window/light pipe", (1, 5, 5), (-107.0, -13.57, 22.0), "MECHANICAL", "provisional"),
    ModuleEnvelope("devkit_key", "DevKit reverse-insertion key bracket", (8, 63, 12), (-99, 0, 15.0), "MECHANICAL", "engineering_calculation"),

    # Mains side (right). The PSU board is 50 x 70 mm at x=56..106, y=-55..15,
    # with the HLK/fuse/MOV/TCO/terminals on it. The relay sits above it on a
    # printed cantilever shelf.
    ModuleEnvelope("pzem", "PZEM-004T V4 + CT interface", (53, 89, 24), (28, 0, 16.5), "MAINS", "provisional"),
    ModuleEnvelope("pzem_bracket", "PZEM mounting bracket", (58, 94, 2), (28, 0, 3.5), "MAINS", "engineering_calculation"),
    ModuleEnvelope("ct", "100 A CT (split core approx)", (30, 30, 15), (20, 42, 40.0), "MAINS", "provisional"),
    ModuleEnvelope("psu_board", "REV_D_CORE_ONLY mains PSU PCB 50 x 65 + HLK/terminals", (50, 65, 30), (81, -22.5, 23.0), "MAINS", "pcb_design"),
    ModuleEnvelope("relay_shelf", "Printed cantilever relay shelf", (55, 28, 3), (79.5, -3, 40.5), "MECHANICAL", "engineering_calculation"),
    ModuleEnvelope("relay", "2-channel optocoupler relay module (above PSU)", (50, 24, 18), (80, -3, 49.0), "MAINS", "provisional"),
    ModuleEnvelope("pe_stud", "PE stud / bonding point", (8, 8, 10), (60, 50, 25.0), "MAINS", "engineering_calculation"),
    ModuleEnvelope("socket", "Type F panel socket body (inside wall)", (35, 45, 45), (89.9, 34.9, 35.0), "MAINS", "provisional"),
    ModuleEnvelope("gland", "M16 cable gland (wall feature)", (16, 16, 12), (116, 10, 18.0), "MAINS", "datasheet"),
    ModuleEnvelope("vent", "M12 ePTFE pressure vent (wall feature)", (12, 12, 8), (116, -15, 45.0), "MECHANICAL", "datasheet"),

    # Mechanical barrier.
    ModuleEnvelope("barrier", "Internal isolation barrier (mechanical)", (2, 100, 50), (-4, 0, 27.5), "MECHANICAL", "engineering_calculation"),
]


def internal_bounds() -> tuple[float, float, float, float, float, float]:
    length, width, height, wall = 220.0, 120.0, 70.0, 2.5
    return (-length / 2 + wall, -width / 2 + wall, wall, length / 2 - wall, width / 2 - wall, height - wall)


def overlaps(a: tuple[float, ...], b: tuple[float, ...], margin: float = 0.0) -> bool:
    return not (
        a[3] + margin <= b[0]
        or b[3] + margin <= a[0]
        or a[4] + margin <= b[1]
        or b[4] + margin <= a[1]
        or a[5] + margin <= b[2]
        or b[5] + margin <= a[2]
    )


EXEMPT_PAIRS = {
    ("carrier", "esp32"),
    ("pzem", "pzem_bracket"),
    ("carrier", "devkit_key"),
    ("esp32", "devkit_key"),
    ("psu_board", "relay_shelf"),
    ("relay", "relay_shelf"),
}


def fit_report(preset: str = "recommended") -> dict:
    modules = [m for m in MODULES if m.name not in {"gland", "vent", "pzem_bracket", "relay_bracket"}]
    bounds = internal_bounds()
    outside: list[dict] = []
    clashes: list[dict] = []
    barrier_crossings: list[dict] = []
    for module in modules:
        b = module.bounds
        if b[0] < bounds[0] or b[1] < bounds[1] or b[2] < bounds[2] or b[3] > bounds[3] or b[4] > bounds[4] or b[5] > bounds[5]:
            outside.append({"module": module.name, "bounds": b, "enclosure_internal": bounds})
    for index, first in enumerate(modules):
        for second in modules[index + 1:]:
            if first.name == "barrier" or second.name == "barrier":
                continue
            if (first.name, second.name) in EXEMPT_PAIRS or (second.name, first.name) in EXEMPT_PAIRS:
                continue
            if overlaps(first.bounds, second.bounds):
                clashes.append({"a": first.name, "b": second.name, "a_bounds": first.bounds, "b_bounds": second.bounds})
    barrier = next((module for module in modules if module.name == "barrier"), None)
    if barrier is not None:
        for module in modules:
            if module.name == "barrier":
                continue
            if overlaps(module.bounds, barrier.bounds):
                barrier_crossings.append({"module": module.name, "bounds": module.bounds})
    status = "PASS" if not outside and not clashes and not barrier_crossings else "FAIL"
    return {
        "preset": "recommended",
        "status": status,
        "enclosure_internal_bounds_mm": bounds,
        "module_count": len(modules),
        "outside_enclosure": outside,
        "clashes": clashes,
        "barrier_crossings": barrier_crossings,
        "limitations": [
            "All module dimensions are approximate envelopes, not measured samples.",
            "No tolerance stack, cable bend, or thermal expansion is modeled.",
            "A PASS here is only a coarse digital fit check; it is not a mechanical validation.",
            "Barrier crossing check is a simple AABB test, not a creepage/clearance calculation.",
        ],
    }


def module_list(preset: str = "recommended") -> Iterable[ModuleEnvelope]:
    return MODULES
