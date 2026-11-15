"""Approximate module envelopes and fit checks. Dimensions are NOT measured."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class ModuleEnvelope:
    name: str
    label: str
    size_mm: tuple[float, float, float]
    center_mm: tuple[float, float, float]
    domain: str  # MAINS | SELV | ISOLATED | MECHANICAL
    provenance: str
    notes: str = ""

    @property
    def bounds(self) -> tuple[float, float, float, float, float, float]:
        x, y, z = self.center_mm
        sx, sy, sz = self.size_mm
        return (x - sx / 2, y - sy / 2, z - sz / 2, x + sx / 2, y + sy / 2, z + sz / 2)


# Positions are relative to the enclosure centre (x, y) and bottom (z=0).
MODULES: dict[str, list[ModuleEnvelope]] = {
    "provisional": [
        ModuleEnvelope("carrier", "Low-voltage carrier PCB (75x50)", (75, 50, 1.6), (-35, 0, 8), "SELV", "engineering_calculation"),
        ModuleEnvelope("esp32", "ESP32-S3-DevKitC-1 (approx)", (68.6, 25.4, 10), (-34, 0, 13), "SELV", "datasheet_approx"),
        ModuleEnvelope("oled", "OLED 0.96 module", (27, 27, 4), (-55, -34, 40), "SELV", "provisional"),
        ModuleEnvelope("button", "Panel button + cap", (12, 12, 8), (-20, -40, 34), "SELV", "provisional"),
        ModuleEnvelope("rgb", "External RGB diffuser", (6, 6, 3), (-5, -40, 40), "SELV", "provisional"),
        ModuleEnvelope("pzem", "PZEM-004T V4 + CT (approx, off-board)", (53, 89, 24), (38.5, 0, 16.5), "MAINS", "provisional"),
        ModuleEnvelope("pzem_bracket", "PZEM mounting bracket (approx)", (58, 94, 2), (38.5, 0, 3.5), "MAINS", "engineering_calculation"),
        ModuleEnvelope("psu", "Hi-Link HLK-5M05 (38x23x18, approx)", (38, 23, 18), (38.5, 0, 40), "MAINS", "distributor_datasheet"),
        ModuleEnvelope("relay", "2-channel optocoupler relay module (off-board, approx)", (50, 24, 18), (38.5, -35, 38), "MAINS", "provisional"),
        ModuleEnvelope("relay_bracket", "Relay module mounting bracket (approx)", (55, 26, 2), (38.5, -34, 29), "MAINS", "engineering_calculation"),
        ModuleEnvelope("fuse", "Fuse holder 5x20 + MOV", (20, 10, 12), (62, -25, 48), "MAINS", "provisional"),
        ModuleEnvelope("terminals", "Mains terminals / PE stud", (18, 30, 10), (62, -30, 36), "MAINS", "provisional"),
        ModuleEnvelope("socket", "Type F socket internal body (approx)", (50, 20, 35), (45, 37.5, 46), "MAINS", "provisional"),
        ModuleEnvelope("gland", "M16 cable gland (wall feature; not internal)", (16, 16, 12), (76, 0, 18), "MAINS", "datasheet"),
        ModuleEnvelope("barrier", "Internal isolation barrier", (2, 95, 50), (5, 0, 27.5), "MECHANICAL", "engineering_calculation"),
    ],
    "recommended": [
        ModuleEnvelope("carrier", "Low-voltage carrier PCB (75x50)", (75, 50, 1.6), (-70, 0, 8), "SELV", "engineering_calculation"),
        ModuleEnvelope("esp32", "ESP32-S3-DevKitC-1 (approx)", (68.6, 25.4, 10), (-68.5, 0, 13), "SELV", "datasheet_approx"),
        ModuleEnvelope("oled", "OLED 0.96 module", (27, 27, 4), (-90, -42, 40), "SELV", "provisional"),
        ModuleEnvelope("button", "Panel button + cap", (12, 12, 8), (-55, -48, 34), "SELV", "provisional"),
        ModuleEnvelope("rgb", "External RGB diffuser", (6, 6, 3), (-35, -48, 40), "SELV", "provisional"),
        ModuleEnvelope("pzem", "PZEM-004T V4 + CT (approx, off-board)", (53, 89, 24), (0, 0, 16.5), "MAINS", "provisional"),
        ModuleEnvelope("pzem_bracket", "PZEM mounting bracket (approx)", (58, 94, 2), (0, 0, 3.5), "MAINS", "engineering_calculation"),
        ModuleEnvelope("psu", "Hi-Link HLK-5M05 (38x23x18, approx)", (38, 23, 18), (60, 10, 40), "MAINS", "distributor_datasheet"),
        ModuleEnvelope("relay", "2-channel optocoupler relay module (off-board, approx)", (50, 24, 18), (52, -40, 38), "MAINS", "provisional"),
        ModuleEnvelope("relay_bracket", "Relay module mounting bracket (approx)", (55, 26, 2), (52, -39, 31), "MAINS", "engineering_calculation"),
        ModuleEnvelope("fuse", "Fuse holder 5x20 + MOV", (20, 10, 12), (90, -15, 48), "MAINS", "provisional"),
        ModuleEnvelope("terminals", "Mains terminals / PE stud", (18, 30, 10), (95, -40, 36), "MAINS", "provisional"),
        ModuleEnvelope("socket", "Type F socket internal body (approx)", (50, 20, 35), (65, 45, 46), "MAINS", "provisional"),
        ModuleEnvelope("gland", "M16 cable gland (wall feature; not internal)", (16, 16, 12), (116, 0, 18), "MAINS", "datasheet"),
        ModuleEnvelope("barrier", "Internal isolation barrier", (2, 115, 50), (-30, 0, 27.5), "MECHANICAL", "engineering_calculation"),
    ],
}


def internal_bounds(preset: str) -> tuple[float, float, float, float, float, float]:
    if preset == "recommended":
        length, width, height, wall = 220.0, 120.0, 70.0, 2.5
    else:
        length, width, height, wall = 150.0, 100.0, 70.0, 2.5
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


EXEMPT_PAIRS = {("carrier", "esp32")}


def fit_report(preset: str) -> dict:
    modules = [m for m in MODULES[preset] if "gland" not in m.name and "bracket" not in m.name]
    bounds = internal_bounds(preset)
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
        "preset": preset,
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


def module_list(preset: str) -> Iterable[ModuleEnvelope]:
    return MODULES[preset]
