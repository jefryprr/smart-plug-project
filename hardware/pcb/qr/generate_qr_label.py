#!/usr/bin/env python3
"""Generate a 22 x 22 mm PCB label with a QR code to the system schematic.

The label is designed for a white polyester/polyimide label with black print.
It is NOT copper, NOT solder mask, and NOT a PCB electrical change.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Polygon, Arc, Circle
import qrcode
from qrcode.constants import ERROR_CORRECT_M

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "hardware" / "pcb" / "qr"
OUT.mkdir(parents=True, exist_ok=True)

URL = "https://github.com/jefryprr/smart-plug-project/blob/main/hardware/schematic/SYSTEM_SCHEMATIC.pdf"
LABEL_MM = 22.0
QR_MM = 13.5
QR_X = (LABEL_MM - QR_MM) / 2
QR_Y = 2.8
INK = "#111111"
GREEN = "#1B5E20"
LIGHT = "#E8F5E9"


def qr_matrix(data: str):
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_M,
        box_size=10,
        border=0,
    )
    qr.add_data(data)
    qr.make(fit=True)
    return qr


def draw_icon(ax):
    # Simple microchip + antenna + lightning bolt, in dark green.
    # Chip body at top-left of the label.
    x0, y0, w, h = 0.9, 19.3, 2.7, 1.8
    ax.add_patch(FancyBboxPatch((x0, y0), w, h,
        boxstyle="round,pad=0.03,rounding_size=0.25",
        facecolor=LIGHT, edgecolor=GREEN, linewidth=0.45, zorder=5))
    # pins
    for i in range(3):
        px = x0 + 0.7 + i * 1.25
        ax.plot([px, px], [y0 - 0.35, y0], color=GREEN, lw=0.45, zorder=6)
        ax.plot([px, px], [y0 + h, y0 + h + 0.35], color=GREEN, lw=0.45, zorder=6)
    for i in range(2):
        py = y0 + 0.7 + i * 1.2
        ax.plot([x0 - 0.35, x0], [py, py], color=GREEN, lw=0.45, zorder=6)
        ax.plot([x0 + w, x0 + w + 0.35], [py, py], color=GREEN, lw=0.45, zorder=6)
    # antenna arcs
    for r in (0.8, 1.2, 1.6):
        ax.add_patch(Arc((x0 + w + 0.9, y0 + h * 0.55), r * 2, r * 2,
                         theta1=-55, theta2=55, color=GREEN, lw=0.45, zorder=6))
    # lightning bolt
    bolt = Polygon([
        [x0 + w * 0.52, y0 + h * 0.78],
        [x0 + w * 0.40, y0 + h * 0.48],
        [x0 + w * 0.50, y0 + h * 0.48],
        [x0 + w * 0.43, y0 + h * 0.18],
        [x0 + w * 0.66, y0 + h * 0.55],
        [x0 + w * 0.55, y0 + h * 0.55],
        [x0 + w * 0.64, y0 + h * 0.82],
    ], closed=True, facecolor=GREEN, edgecolor="none", zorder=7)
    ax.add_patch(bolt)

    # Title text
    ax.text(6.4, 20.7, "SMART PLUG", fontsize=3.6, fontweight="bold",
            color=INK, va="center", ha="left", zorder=8)
    ax.text(6.6, 17.45, "ESP32-S3  ·  IoT", fontsize=4.6,
            color=GREEN, va="center", ha="left", zorder=8)


def label():
    qr = qr_matrix(URL)
    matrix = qr.get_matrix()
    n = len(matrix)
    mod = QR_MM / n

    fig = plt.figure(figsize=(LABEL_MM / 25.4, LABEL_MM / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, LABEL_MM)
    ax.set_ylim(0, LABEL_MM)
    ax.set_aspect("equal")
    ax.axis("off")

    # white label background + thin border
    ax.add_patch(Rectangle((0, 0), LABEL_MM, LABEL_MM, facecolor="white",
                           edgecolor="#222222", lw=0.35, zorder=0))

    # QR modules (quiet zone provided by the white margins)
    for row in range(n):
        for col in range(n):
            if matrix[row][col]:
                x = QR_X + col * mod
                y = QR_Y + (n - 1 - row) * mod
                ax.add_patch(Rectangle((x, y), mod, mod, facecolor=INK,
                                       edgecolor="none", zorder=3))

    draw_icon(ax)

    # bottom text
    ax.text(LABEL_MM / 2, 1.50, "SCAN FOR", fontsize=2.8,
            fontweight="bold", color=INK, va="center", ha="center", zorder=8)
    ax.text(LABEL_MM / 2, 0.72, "SCHEMATIC", fontsize=3.0, fontweight="bold",
            color=INK, va="center", ha="center", zorder=8)

    fig.savefig(OUT / "pcb_label_22mm.png", dpi=1200, facecolor="white")
    fig.savefig(OUT / "pcb_label_22mm.pdf", facecolor="white")
    fig.savefig(OUT / "pcb_label_22mm.svg", facecolor="white")
    plt.close(fig)

    # QR-only image for reference/testing
    qr_img = qrcode.make(URL, error_correction=ERROR_CORRECT_M, border=4)
    qr_img.save(OUT / "schematic_qr.png")
    print("URL", URL)
    print("QR version", qr.version, "modules", n, "module mm", round(mod, 4))
    print("label", OUT / "pcb_label_22mm.png")


if __name__ == "__main__":
    label()
