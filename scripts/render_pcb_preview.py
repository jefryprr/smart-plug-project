#!/usr/bin/env python3
"""Preview the routed SELV carrier; SVG is exported by KiCad CLI.

The matplotlib preview is a coarse outline; carrier.svg is the KiCad plot.
"""
from __future__ import annotations

import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[1]
PCB = ROOT / "hardware" / "kicad" / "smartplug.kicad_pcb"
OUT = ROOT / "hardware" / "pcb" / "render"
OUT.mkdir(parents=True, exist_ok=True)

RECT_RE = re.compile(r"\(gr_rect\s+\(start\s+([\d.\-]+)\s+([\d.\-]+)\)\s+\(end\s+([\d.\-]+)\s+([\d.\-]+)\).*?\(layer\s+\"([^\"]+)\"\)", re.S)
TEXT_RE = re.compile(r"\(gr_text\s+\"([^\"]*)\"\s+\(at\s+([\d.\-]+)\s+([\d.\-]+)\).*?\(layer\s+\"([^\"]+)\"\)", re.S)


def main() -> None:
    text = PCB.read_text(encoding="utf-8")
    rects = RECT_RE.findall(text)
    texts = TEXT_RE.findall(text)
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=150)
    ax.set_aspect("equal")
    for x1, y1, x2, y2, layer in rects:
        x1f, y1f, x2f, y2f = map(float, (x1, y1, x2, y2))
        color = "#14213d" if layer == "Edge.Cuts" else "#9a5b00" if layer == "F.CrtYd" else "#5b677a"
        linestyle = "-" if layer == "Edge.Cuts" else "--"
        linewidth = 2.0 if layer == "Edge.Cuts" else 0.8
        ax.add_patch(Rectangle((x1f, y1f), x2f - x1f, y2f - y1f, fill=False, edgecolor=color, linestyle=linestyle, linewidth=linewidth))
    for content, x, y, _layer in texts:
        ax.text(float(x), float(y), content, fontsize=6, color="#14213d", ha="left", va="bottom")
    ax.set_xlim(-5, 105)
    ax.set_ylim(-5, 75)
    ax.set_title("SMART PLUG — LOW-VOLTAGE CARRIER — PLACEMENT PREVIEW\nREV_C_PSU_BOARD · parsed from smartplug.kicad_pcb · NOT A KICAD PLOT · NOT FOR FABRICATION", fontsize=10)
    ax.set_xlabel("mm")
    ax.set_ylabel("mm")
    ax.grid(True, linewidth=0.3, alpha=0.4)
    fig.tight_layout()
    fig.savefig(OUT / "placement_preview.png", bbox_inches="tight")
    fig.savefig(OUT / "placement_preview.svg", format="svg", bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote placement preview from {PCB.name}: {len(rects)} rects, {len(texts)} texts")
        # Export the real routed SVG with KiCad CLI.
    import subprocess
    kicad = ROOT / "tools" / "kicad" / "bin" / "kicad-cli.exe"
    if kicad.exists():
        subprocess.run([str(kicad), "pcb", "export", "svg", "-o", str(OUT / "carrier.svg"),
                        "-l", "F.Cu,B.Cu,F.SilkS,Edge.Cuts", "--page-size-mode", "2",
                        "--mode-single", str(PCB)], check=False)
        print(f"Wrote routed SVG: {OUT / 'carrier.svg'}")


if __name__ == "__main__":
    main()
