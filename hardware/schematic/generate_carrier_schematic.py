#!/usr/bin/env python3
"""Draw the REV_C_PSU_BOARD carrier/mains functional schematic with schemdraw."""
from __future__ import annotations

from pathlib import Path

import schemdraw
import schemdraw.elements as elm

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "hardware" / "schematic"
OUT.mkdir(parents=True, exist_ok=True)


def box(d, x, y, w, h, title, subtitle="", color="#f4f4f4"):
    d.add(elm.Rect(w=w, h=h).at((x, y)).fill(color).color("#333333"))
    d.add(elm.Label(title, fontsize=10).at((x + w / 2, y + h * 0.62)))
    if subtitle:
        d.add(elm.Label(subtitle, fontsize=7).at((x + w / 2, y + h * 0.30)))


def arrow(d, start, end, label="", color="#333333", style="-"):
    d.add(elm.Line().at(start).to(end).color(color).linestyle(style))
    if label:
        d.add(elm.Label(label, fontsize=7).at(((start[0] + end[0]) / 2, (start[1] + end[1]) / 2 + 0.12)))


def main():
    d = schemdraw.Drawing(show=False)
    d.config(unit=2.0, fontsize=9)

    # Mains / isolation domain
    box(d, 0.0, 5.2, 3.2, 1.2, "MAINS INPUT", "L / N / PE, fuse, MOV, TCO", "#ffe8e8")
    box(d, 0.0, 2.8, 3.2, 1.4, "HLK-5M05", "90-264 VAC -> 5 V 1 A\ninternal isolation claim", "#fff4d6")
    box(d, 0.0, 0.2, 3.2, 1.6, "PZEM-004T V4", "100 A CT, internal optocoupler\nTTL side = SELV", "#fff4d6")
    box(d, 4.2, 2.5, 3.6, 2.0, "ESP32-S3 CARRIER", "DevKitC-1 two 1x22 sockets, 22.86 mm rows\n5 V from PSU J5, 3 fiducials, SELV only", "#e8f4ff")
    box(d, 9.0, 5.0, 3.0, 1.4, "RELAY MODULE", "2x SPDT, active-LOW\nNOT mechanically linked", "#ffe8e8")
    box(d, 9.0, 3.0, 3.0, 1.2, "SOCKET", "Type F 16 A, PE continuous", "#ffe8e8")
    box(d, 4.2, 0.2, 1.7, 1.2, "OLED", "SSD1306", "#e8ffe8")
    box(d, 6.1, 0.2, 1.7, 1.2, "RTC", "DS3231", "#e8ffe8")
    box(d, 8.0, 0.2, 1.6, 1.2, "BUTTON", "GPIO5", "#e8ffe8")
    box(d, 9.8, 0.2, 1.4, 1.2, "RGB", "WS2812", "#e8ffe8")
    box(d, 11.4, 3.0, 1.2, 1.2, "Q1", "AO3400", "#f0e8ff")
    box(d, 11.4, 1.2, 1.2, 1.2, "U9", "74HCT125", "#f0e8ff")

    # Mains path
    arrow(d, (1.6, 5.2), (1.6, 4.2), "L/N")
    arrow(d, (1.6, 2.8), (1.6, 1.8), "AC")
    arrow(d, (3.2, 3.4), (4.2, 3.4), "5 V")
    arrow(d, (3.2, 0.9), (4.2, 0.9), "TTL 5 V")
    arrow(d, (7.8, 3.6), (9.0, 5.4), "GPIO4 -> Q1")
    arrow(d, (12.0, 5.0), (12.0, 4.2), "COM/NO")
    arrow(d, (12.0, 4.2), (12.0, 3.0), "L/N")
    arrow(d, (11.4, 3.6), (10.5, 3.6), "IN1/2")

    # SELV buses
    arrow(d, (7.8, 3.1), (8.0, 0.8), "I2C")
    arrow(d, (7.8, 2.9), (8.7, 1.4), "I2C")
    arrow(d, (7.8, 2.7), (8.8, 1.0), "GPIO5")
    arrow(d, (7.8, 2.5), (9.8, 0.8), "GPIO10")
    arrow(d, (10.6, 0.8), (11.4, 1.2), "3.3 V")
    arrow(d, (11.4, 1.8), (10.5, 0.8), "5 V data")
    arrow(d, (11.4, 1.5), (11.4, 1.2), "level shift")

    # PZEM UART detail
    d.add(elm.Label("PZEM TX 5 V -> 10k/20k divider -> GPIO18", fontsize=7).at((5.8, 1.55)))
    d.add(elm.Label("GPIO17 -> 74HCT125 (5 V) -> PZEM RX", fontsize=7).at((5.8, 1.25)))
    d.add(elm.Label("No external ADuM/B0505S: PZEM internal optocouplers are the barrier", fontsize=7).at((5.8, 1.95)))
    d.add(elm.Label("5 V input from REV_C PSU J5 (PTC/TVS on PSU board)", fontsize=7).at((5.8, 2.25)))

    # Isolation boundary note
    d.add(elm.Label("Isolation barrier: PZEM / HLK internal; verify creepage + hipot", fontsize=7).at((6.0, 6.7)))
    d.add(elm.Line().at((3.35, 0.0)).to((3.35, 6.6)).color("#c00000").linestyle("--"))
    d.add(elm.Label("SELV", fontsize=8).at((4.0, 6.25)))
    d.add(elm.Label("MAINS", fontsize=8).at((2.7, 6.25)))

    d.add(elm.Label("REV_C_PSU_BOARD — no TMP102, no external UART isolation — NOT FOR FABRICATION / NOT FOR USE", fontsize=8).at((6.0, -0.4)))

    d.save(str(OUT / "carrier_schematic.svg"))
    d.save(str(OUT / "carrier_schematic.png"), dpi=200)
    print(f"Wrote {OUT / 'carrier_schematic.svg'} and .png")


if __name__ == "__main__":
    main()
