"""Approximate module envelopes and fit checks for the CORE_ONLY_SHOPEE enclosure.

Dimensions are datasheet/engineering estimates, not measured samples. The
printed enclosure is a prototype, not a certified electrical enclosure.
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


MODULES: list[ModuleEnvelope] = [
    # SELV side (left). Carrier bottom at z=8.0.
    ModuleEnvelope("carrier", "SELV carrier PCB 100 x 70", (100, 70, 1.6), (-55, 0, 8.8), "SELV", "pcb_design"),
    ModuleEnvelope("esp32", "ESP32-S3-DevKitC-1 v1.0 (63 x 25.5 approx)", (63, 25.5, 10), (-68.33, -13.57, 22.0), "SELV", "datasheet_approx"),
    ModuleEnvelope("button", "Panel button + cap", (12, 12, 8), (-62, 28, 63.5), "SELV", "provisional"),
    ModuleEnvelope("devkit_rgb_window", "Onboard RGB left-wall window", (1, 5, 5), (-107.0, -13.57, 22.0), "MECHANICAL", "provisional"),
    ModuleEnvelope("devkit_key", "DevKit reverse-insertion key bracket", (8, 63, 12), (-99, 0, 15.0), "MECHANICAL", "engineering_calculation"),

    # Mains side (right).
    ModuleEnvelope("pzem", "PZEM-004T V4 PCB ~74 x 31 x 18", (31, 74, 18), (28, 0, 19.0), "MAINS", "datasheet_approx"),
    ModuleEnvelope("pzem_bracket", "PZEM mounting bracket 37 x 80", (37, 80, 2), (28, 0, 9.0), "MAINS", "engineering_calculation"),
    ModuleEnvelope("ct", "100 A CT clamp (approx)", (30, 30, 15), (20, 42, 40.0), "MAINS", "provisional"),
    ModuleEnvelope("psu_board", "PSU PCB 50 x 65 + HLK/terminals", (50, 65, 30), (81, -22.5, 25.0), "MAINS", "pcb_design"),
    ModuleEnvelope("psu_bracket", "PSU mounting plate 50 x 65", (50, 65, 2), (81, -22.5, 9.0), "MAINS", "engineering_calculation"),
    ModuleEnvelope("relay_shelf", "Printed relay shelf 55 x 28 x 3", (55, 28, 3), (79.5, -3, 41.5), "MECHANICAL", "engineering_calculation"),
    ModuleEnvelope("relay", "2-channel relay module 50 x 26 x 18", (50, 26, 18), (80, -3, 52.0), "MAINS", "provisional"),
    ModuleEnvelope("pe_stud", "PE stud / bonding point M4", (10, 10, 12), (45, 50, 8.5), "MAINS", "engineering_calculation"),
    ModuleEnvelope("socket", "DV DSMS-2P-16A body (40 x 40 x 45)", (40, 40, 45), (85.0, 34.9, 35.0), "MAINS", "user_confirmed_socket"),
    ModuleEnvelope("gland", "M16 cable gland (back wall feature)", (22, 22, 12), (20, 56, 18.0), "MAINS", "datasheet"),

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
    ("psu_board", "psu_bracket"),
    ("carrier", "devkit_key"),
    ("esp32", "devkit_key"),
    ("psu_board", "relay_shelf"),
    ("relay", "relay_shelf"),
}


def fit_report(preset: str = "recommended") -> dict:
    modules = [m for m in MODULES if m.name not in {"gland", "pzem_bracket", "psu_bracket", "relay_bracket"}]
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
            "PZEM/socket/relay dimensions must be measured on the purchased parts.",
            "No tolerance stack, cable bend, or thermal expansion is modeled.",
            "A PASS here is only a coarse digital fit check; it is not a mechanical validation.",
            "Barrier crossing check is a simple AABB test, not a creepage/clearance calculation.",
        ],
    }


def module_list(preset: str = "recommended") -> Iterable[ModuleEnvelope]:
    return MODULES
