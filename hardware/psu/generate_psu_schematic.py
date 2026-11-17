#!/usr/bin/env python3
"""Draw a clean functional block diagram for the REV_C mains-entry PSU board."""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "hardware" / "psu"
OUT.mkdir(parents=True, exist_ok=True)

# Palette
INK = "#1A202C"
MUTED = "#4A5568"
LINE = "#2D3748"
MAINS_FILL = "#FFF3F1"
MAINS_EDGE = "#D96C5F"
PROTECT_FILL = "#FFF4D6"
PROTECT_EDGE = "#B7791F"
HLK_FILL = "#FFE8D6"
HLK_EDGE = "#C05621"
SELV_FILL = "#F1FBF5"
SELV_EDGE = "#4FA579"
BLUE_FILL = "#E8F3FF"
BLUE_EDGE = "#2B6CB0"
OUT_FILL = "#EAF8EF"
OUT_EDGE = "#2F855A"
ISOLATION = "#C53030"


def rounded(ax, x, y, w, h, face, edge, lw=1.5, z=3):
    """Draw a soft card with a subtle shadow."""
    ax.add_patch(
        FancyBboxPatch(
            (x + 0.035, y - 0.045),
            w,
            h,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            facecolor="#000000",
            edgecolor="none",
            alpha=0.06,
            zorder=z - 1,
        )
    )
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        facecolor=face,
        edgecolor=edge,
        linewidth=lw,
        zorder=z,
    )
    ax.add_patch(patch)
    return patch


def card(ax, x, y, w, h, title, subtitle="", face="#FFFFFF", edge="#CBD5E0",
         title_size=11, sub_size=8.4):
    rounded(ax, x, y, w, h, face, edge)
    ax.text(
        x + w / 2,
        y + h - 0.13,
        title,
        ha="center",
        va="top",
        fontsize=title_size,
        fontweight="bold",
        color=INK,
        zorder=4,
    )
    if subtitle:
        ax.text(
            x + w / 2,
            y + h * 0.37,
            subtitle,
            ha="center",
            va="center",
            fontsize=sub_size,
            color=MUTED,
            linespacing=1.25,
            zorder=4,
        )


def arrow(ax, start, end, color=LINE, lw=1.6, z=2):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=11,
            linewidth=lw,
            color=color,
            shrinkA=0,
            shrinkB=0,
            zorder=z,
        )
    )


def path_arrow(ax, points, color=LINE, lw=1.6, z=2):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ax.plot(xs, ys, color=color, linewidth=lw, solid_capstyle="round", zorder=z)
    arrow(ax, points[-2], points[-1], color=color, lw=lw, z=z)


def dot(ax, x, y, color=LINE, size=4.5, z=5):
    ax.plot(x, y, marker="o", markersize=size, color=color, zorder=z)


def note(ax, x, y, text, size=8.2, color=MUTED, ha="left", va="center", weight="normal",
         box=False, z=6):
    kwargs = {}
    if box:
        kwargs["bbox"] = dict(boxstyle="round,pad=0.22", facecolor="white",
                              edgecolor="#CBD5E0", linewidth=0.7, alpha=0.96)
    ax.text(x, y, text, ha=ha, va=va, fontsize=size, color=color,
            fontweight=weight, linespacing=1.25, zorder=z, **kwargs)


def main():
    fig, ax = plt.subplots(figsize=(14, 8.3))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9.5)
    ax.set_aspect("equal")
    ax.axis("off")

    # ------------------------------------------------------------------ regions
    ax.add_patch(
        Rectangle((0.35, 5.15), 15.3, 3.4, facecolor=MAINS_FILL,
                  edgecolor=MAINS_EDGE, linewidth=1.1, zorder=0)
    )
    ax.add_patch(
        Rectangle((0.35, 0.75), 15.3, 3.8, facecolor=SELV_FILL,
                  edgecolor=SELV_EDGE, linewidth=1.1, zorder=0)
    )
    note(ax, 0.55, 8.38, "MAINS DOMAIN  ·  230 VAC, 50 Hz", size=10.5,
         color="#9B2C2C", weight="bold")
    note(ax, 6.2, 4.38, "SELV DOMAIN  ·  5 V / 3.3 V", size=10.5,
         color="#276749", weight="bold")

    # isolation boundary behind the HLK card
    ax.plot([0.35, 15.65], [4.85, 4.85], color=ISOLATION, linewidth=1.5,
            linestyle=(0, (7, 5)), zorder=1)
    note(ax, 9.8, 5.05,
         "ISOLATION BOUNDARY\nHLK-5M05 internal isolation — datasheet claim, not assembly certification",
         size=8.0, color=ISOLATION, ha="center", va="bottom")

    # ------------------------------------------------------------------ title
    note(ax, 0.5, 9.18, "REV_C PSU BOARD", size=20, color=INK, weight="bold")
    note(ax, 0.5, 8.92,
         "230 VAC mains entry  ·  protection  ·  5 V outputs  ·  50 × 65 mm",
         size=9.6, color=MUTED)
    rounded(ax, 12.45, 8.98, 3.05, 0.42, "#FFF5F5", "#E53E3E", lw=1.2)
    note(ax, 13.975, 9.19, "NOT FOR FABRICATION / NOT FOR USE", size=8.0,
         color="#C53030", weight="bold", ha="center")

    # ------------------------------------------------------------------ mains chain
    card(ax, 3.8, 6.9, 1.6, 1.1, "TB1", "230 VAC IN\nL / N · 5.08 mm",
         MAINS_FILL, MAINS_EDGE)
    card(ax, 5.8, 6.9, 1.4, 1.1, "F1", "10 A · 250 VAC\nslow-blow",
         PROTECT_FILL, PROTECT_EDGE)
    card(ax, 7.6, 6.9, 1.4, 1.1, "MOV1", "275 VAC\nL–N",
         PROTECT_FILL, PROTECT_EDGE)
    card(ax, 9.4, 6.9, 1.5, 1.1, "TF1", "99 °C TCO\n10 A · one-shot",
         PROTECT_FILL, PROTECT_EDGE)
    card(ax, 11.3, 6.9, 1.7, 1.1, "TB2", "230 VAC OUT\nrelay / socket",
         MAINS_FILL, MAINS_EDGE)

    for x1, x2 in [(5.4, 5.8), (7.2, 7.6), (9.0, 9.4), (10.9, 11.3)]:
        arrow(ax, (x1, 7.45), (x2, 7.45))
    arrow(ax, (13.0, 7.45), (14.35, 7.45))
    note(ax, 13.68, 7.66, "to relay / socket", size=8.2, color=MUTED, ha="center")

    # N bus
    ax.plot([4.2, 4.2], [6.9, 6.15], color=LINE, linewidth=1.6, zorder=2)
    ax.plot([4.2, 12.6], [6.15, 6.15], color=LINE, linewidth=1.6, zorder=2)
    ax.plot([12.6, 12.6], [6.15, 6.9], color=LINE, linewidth=1.6, zorder=2)
    ax.plot([8.3, 8.3], [6.15, 6.9], color=LINE, linewidth=1.6, zorder=2)
    for x in (4.2, 8.3, 12.6):
        dot(ax, x, 6.15)
    note(ax, 8.3, 5.99, "N_MAINS", size=8.0, color=MUTED, ha="center",
         box=True)

    # L_LOAD lane above the chain to avoid crossing the N bus
    path_arrow(
        ax,
        [(11.1, 7.45), (11.1, 8.22), (2.0, 8.22), (2.0, 5.6)],
        color="#9B2C2C",
        lw=1.5,
    )
    note(ax, 6.6, 8.34, "L_LOAD (after TCO)  →  HLK AC L", size=8.0,
         color="#9B2C2C", ha="center", box=True)

    # N branch to HLK
    path_arrow(ax, [(4.2, 6.15), (2.8, 6.15), (2.8, 5.6)],
               color="#2B6CB0", lw=1.5)
    note(ax, 3.5, 6.3, "N_MAINS", size=8.0, color="#2B6CB0", ha="center",
         box=True)

    # ------------------------------------------------------------------ HLK
    card(ax, 1.0, 3.75, 2.4, 1.85, "HLK-5M05",
         "230 VAC → 5 V · 1 A\ninternal isolation\nPENDING_APPROVAL",
         HLK_FILL, HLK_EDGE, title_size=11.5, sub_size=8.0)

    # ------------------------------------------------------------------ SELV protection
    card(ax, 4.1, 3.55, 1.8, 1.05, "5 V PROTECTION",
         "F2 1.1 A PTC · D1 SMBJ5.0A\nC1 100 µF · C2 100 nF",
         BLUE_FILL, BLUE_EDGE, title_size=9.5, sub_size=8.0)
    arrow(ax, (3.4, 4.26), (4.1, 4.08))
    note(ax, 3.75, 4.4, "+5 V", size=8.2, color="#2B6CB0", ha="center")

    # 5 V bus
    path_arrow(ax, [(4.95, 3.55), (4.95, 3.0), (12.2, 3.0)],
               color="#2B6CB0", lw=1.7)
    note(ax, 7.4, 3.12, "+5 V  ·  total budget ≤ 1 A", size=8.4,
         color="#2B6CB0", ha="center", box=True)

    # output bus and cards
    ax.plot([12.2, 12.2], [3.8, 1.6], color="#2B6CB0", linewidth=1.7, zorder=2)
    dot(ax, 12.2, 3.0)
    for y, title, subtitle in [
        (3.35, "J5 · OUT1", "carrier\nESP32 / UI"),
        (2.25, "J6 · OUT2", "relay module"),
        (1.15, "J7 · OUT3", "PZEM 5 V *\nconditional"),
    ]:
        card(ax, 12.45, y, 2.4, 0.9, title, subtitle, OUT_FILL, OUT_EDGE,
             title_size=9.5, sub_size=7.9)
        yc = y + 0.45
        arrow(ax, (12.2, yc), (12.45, yc), color="#2B6CB0", lw=1.5)

    # Current / budget annotations
    note(ax, 6.2, 2.35,
         "HLK output: 5 V / 1 A max\nPeak load not measured",
         size=8.0, color=MUTED, ha="left")
    note(ax, 6.2, 1.75,
         "Mains L/N load path: 10 A rated terminals and fuse\n"
         "Final 8 A only after thermal and lifecycle tests",
         size=8.0, color=MUTED, ha="left")

    # ------------------------------------------------------------------ footer
    note(ax, 0.55, 0.48,
         "* OUT3 (PZEM 5 V) is conditional on batch inspection + hipot/leakage (ADR-016).",
         size=8.2, color=MUTED)
    note(ax, 0.55, 0.24,
         "PE is a dedicated chassis stud; not on this PCB and never switched/fused. "
         "Functional block diagram — not a wiring diagram.",
         size=8.2, color=MUTED)
    note(ax, 15.55, 0.48,
         "Status: PENDING_APPROVAL · NOT_FOR_FABRICATION",
         size=7.8, color="#C53030", ha="right")

    fig.subplots_adjust(0, 0, 1, 1)
    fig.savefig(OUT / "psu_schematic.svg", format="svg", facecolor="white")
    fig.savefig(OUT / "psu_schematic.png", dpi=220, facecolor="white")
    plt.close(fig)
    print(f"Wrote {OUT / 'psu_schematic.svg'} and {OUT / 'psu_schematic.png'}")


if __name__ == "__main__":
    main()
