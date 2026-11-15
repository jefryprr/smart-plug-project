"""Render actual STL exports and generate fit/drawing artifacts."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle, Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from components import fit_report, module_list

ROOT = Path(__file__).resolve().parents[3]
EXPORT = ROOT / "hardware" / "mechanical" / "export"
RENDER = ROOT / "hardware" / "mechanical" / "render"
DRAWINGS = ROOT / "hardware" / "mechanical" / "drawings"
RENDER.mkdir(parents=True, exist_ok=True)
DRAWINGS.mkdir(parents=True, exist_ok=True)

COLOR_TOP = "#7fb8a8"
COLOR_BOTTOM = "#4d8f7d"


def load_mesh(name: str) -> trimesh.Trimesh:
    mesh = trimesh.load(EXPORT / name, force="mesh")
    if isinstance(mesh, trimesh.Scene):
        mesh = mesh.to_mesh()
    return mesh


def add_mesh(ax, mesh: trimesh.Trimesh, color: str, alpha: float = 1.0, offset=(0, 0, 0)) -> None:
    vertices = np.array(mesh.vertices) + np.array(offset)
    faces = np.array(mesh.faces)
    collection = Poly3DCollection(vertices[faces], alpha=alpha, facecolor=color, edgecolor="none")
    ax.add_collection3d(collection)


def set_view(ax, meshes: list[trimesh.Trimesh], elev: float, azim: float) -> None:
    all_vertices = np.vstack([np.array(mesh.vertices) for mesh in meshes])
    minimum = all_vertices.min(axis=0)
    maximum = all_vertices.max(axis=0)
    center = (minimum + maximum) / 2
    span = (maximum - minimum).max() / 2
    ax.set_xlim(center[0] - span, center[0] + span)
    ax.set_ylim(center[1] - span, center[1] + span)
    ax.set_zlim(min(0, center[2] - span), center[2] + span)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()


def render_view(name: str, elev: float, azim: float, exploded: bool = False, cutaway: bool = False, preset: str = "recommended") -> None:
    top = load_mesh(f"body_top_{preset}.stl")
    bottom = load_mesh(f"body_bottom_{preset}.stl")
    fig = plt.figure(figsize=(12, 9), dpi=120)
    ax = fig.add_subplot(111, projection="3d")
    top_offset = (0, 0, 35) if exploded else (0, 0, 0)
    top_alpha = 0.28 if cutaway else 1.0
    add_mesh(ax, bottom, COLOR_BOTTOM, 0.95)
    add_mesh(ax, top, COLOR_TOP, top_alpha, top_offset)
    set_view(ax, [bottom, top], elev, azim)
    ax.set_title(
        f"Smart Plug enclosure — {name}\nREV_B_NO_TEMP · {preset} · APPROXIMATE DIMENSIONS · NOT FOR MAINS",
        fontsize=11,
    )
    fig.tight_layout()
    fig.savefig(RENDER / f"{name}.png", bbox_inches="tight")
    plt.close(fig)


def dimensions_svg() -> None:
    fig, ax = plt.subplots(figsize=(10, 7), dpi=120)
    ax.set_aspect("equal")
    ax.add_patch(Rectangle((0, 0), 220, 120, fill=False, linewidth=1.5))
    ax.annotate("", xy=(220, -8), xytext=(0, -8), arrowprops=dict(arrowstyle="<->", linewidth=1))
    ax.text(110, -14, "220 mm (Q06=C confirmed 2026-11-15)", ha="center", fontsize=10)
    ax.annotate("", xy=(228, 120), xytext=(228, 0), arrowprops=dict(arrowstyle="<->", linewidth=1))
    ax.text(234, 60, "120 mm (recommended)", va="center", rotation=90, fontsize=10)
    ax.text(5, 125, "Height 70 mm · wall 2.5 mm · corner R3 · 150x100 and 180x120 fail clearance review", fontsize=9)
    ax.set_xlim(-20, 255)
    ax.set_ylim(-25, 140)
    ax.axis("off")
    ax.set_title("Enclosure external dimensions - REV_B_NO_TEMP", fontsize=12)
    fig.tight_layout()
    fig.savefig(DRAWINGS / "dimensions.svg", format="svg")
    fig.savefig(DRAWINGS / "dimensions.png", dpi=150)
    plt.close(fig)


def mounting_plan_svg() -> None:
    fig, ax = plt.subplots(figsize=(10, 7), dpi=120)
    ax.set_aspect("equal")
    ax.add_patch(Rectangle((-110, -60), 220, 120, fill=False, linewidth=1.5))
    ax.add_patch(Rectangle((-105, -35), 100, 70, fill=False, linewidth=1, linestyle="--", color="#0f6b5c"))
    ax.text(-104, 37, "Carrier PCB 100x70", fontsize=8, color="#0f6b5c")
    ax.add_patch(Rectangle((1.5, -44.5), 53, 89, fill=False, linewidth=1, linestyle="--", color="#b42318"))
    ax.text(3, 46, "PZEM", fontsize=8, color="#b42318")
    ax.add_patch(Rectangle((55, -15), 50, 24, fill=False, linewidth=1, linestyle="--", color="#b42318"))
    ax.text(56, 11, "2CH relay", fontsize=8, color="#b42318")
    ax.add_patch(Rectangle((61, -39.5), 38, 23, fill=False, linewidth=1, linestyle="--", color="#b42318"))
    ax.text(62, -42, "HLK-5M05", fontsize=8, color="#b42318")
    ax.add_patch(Rectangle((72.4, 11.5), 35, 45, fill=False, linewidth=1, linestyle="--", color="#b42318"))
    ax.text(74, 69, "Socket body", fontsize=8, color="#b42318")
    ax.add_patch(Rectangle((65, -55), 20, 10, fill=False, linewidth=1, linestyle="--", color="#b42318"))
    ax.text(66, -58, "Fuse/MOV", fontsize=8, color="#b42318")
    ax.add_patch(Rectangle((85, -56), 20, 12, fill=False, linewidth=1, linestyle="--", color="#b42318"))
    ax.text(86, -59, "Terminals", fontsize=8, color="#b42318")
    ax.add_patch(Rectangle((5, 35), 30, 30, fill=False, linewidth=1, linestyle="--", color="#b42318"))
    ax.text(6, 67, "CT", fontsize=8, color="#b42318")
    ax.add_patch(Rectangle((100, -34), 8, 8, fill=False, linewidth=1, linestyle="--", color="#b42318"))
    ax.text(101, -37, "PE", fontsize=8, color="#b42318")
    ax.axvline(-4, color="#b42318", linewidth=2)
    ax.text(-3, 53, "Isolation barrier", color="#b42318", fontsize=8)
    ax.add_patch(Rectangle((-106, 21), 28, 14, fill=False, linewidth=1, color="#175cd3"))
    ax.add_patch(Circle((-62, 28), 6, fill=False, linewidth=1, color="#175cd3"))
    ax.add_patch(Circle((-49, 28), 3, fill=False, linewidth=1, color="#175cd3"))
    ax.text(-108, 18, "OLED / BTN / RGB on top lid", fontsize=8, color="#175cd3")
    ax.text(-108, -57, "SELV zone", fontsize=10, color="#0f6b5c")
    ax.text(-27, -57, "MAINS zone", fontsize=10, color="#b42318")
    ax.set_xlim(-120, 120)
    ax.set_ylim(-68, 75)
    ax.axis("off")
    ax.set_title("Mounting plan - top view - NOT A CLEARANCE DRAWING", fontsize=11)
    fig.tight_layout()
    fig.savefig(DRAWINGS / "mounting_plan.svg", format="svg")
    fig.savefig(DRAWINGS / "mounting_plan.png", dpi=150)
    plt.close(fig)


def service_access_svg() -> None:
    fig, ax = plt.subplots(figsize=(10, 5), dpi=120)
    ax.set_aspect("equal")
    ax.add_patch(Rectangle((-110, 60), 220, 10, fill=False, linewidth=1.5))
    ax.text(-108, 72, "Lid top view (z=70)", fontsize=9)
    ax.add_patch(Rectangle((-106, 61), 28, 14, fill=False, linewidth=1, color="#175cd3"))
    ax.text(-106, 62, "OLED 28x14", fontsize=8, color="#175cd3")
    ax.add_patch(Circle((-62, 68), 6, fill=False, linewidth=1, color="#175cd3"))
    ax.text(-74, 62, "Button 12", fontsize=8, color="#175cd3")
    ax.add_patch(Circle((-49, 68), 3, fill=False, linewidth=1, color="#175cd3"))
    ax.text(-47, 62, "RGB 5", fontsize=8, color="#175cd3")
    ax.add_patch(Rectangle((-57, -60), 30, 20, fill=False, linewidth=1.2, color="#9a5b00"))
    ax.text(-56, -56, "USB service cover 30x20", fontsize=8, color="#9a5b00")
    ax.text(-108, -40, "Right wall: socket 45x45 at y=34, z=35", fontsize=8, color="#b42318")
    ax.text(-108, -46, "Right wall: M16 gland at y=-50, z=18; M12 vent at y=-15, z=45", fontsize=8, color="#b42318")
    ax.text(-108, -52, "No USB while mains energized; remove cover only with mains OFF", fontsize=8, color="#9a5b00")
    ax.set_xlim(-120, 120)
    ax.set_ylim(-65, 78)
    ax.axis("off")
    ax.set_title("Service access - panel features - REVIEW REQUIRED", fontsize=11)
    fig.tight_layout()
    fig.savefig(DRAWINGS / "service_access.svg", format="svg")
    fig.savefig(DRAWINGS / "service_access.png", dpi=150)
    plt.close(fig)


def assembly_pdf() -> None:
    target = DRAWINGS / "assembly.pdf"
    temp = DRAWINGS / "assembly.tmp.pdf"
    if temp.exists():
        temp.unlink()
    with PdfPages(temp) as pdf:
        for name in ["isometric", "front", "back", "top", "bottom", "exploded", "cutaway"]:
            image = plt.imread(RENDER / f"{name}.png")
            fig, ax = plt.subplots(figsize=(11, 8.5))
            ax.imshow(image)
            ax.axis("off")
            ax.set_title(f"Assembly view: {name} — REV_B_NO_TEMP — NOT FOR FABRICATION", fontsize=11)
            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)
        fig, ax = plt.subplots(figsize=(11, 8.5))
        ax.axis("off")
        ax.text(
            0.05, 0.95,
            "Smart Plug enclosure assembly\n"
            "REV_B_NO_TEMP\n\n"
            "This drawing is a mechanical concept generated from CadQuery source.\n"
            "Module dimensions are approximate; no physical fit validation exists.\n"
            "3D printed enclosure is prototype-only and not a certified electrical enclosure.\n"
            "Mains assembly and energization require a qualified engineer and lab.\n",
            va="top", fontsize=11, family="monospace"
        )
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)
    if target.exists():
        target.unlink()
    temp.replace(target)


def write_fit_reports() -> None:
    report = {"recommended": fit_report()}
    (ROOT / "hardware" / "mechanical" / "CLASH_REPORT.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = ["# Fit Analysis - REV_B_NO_TEMP", ""]
    lines.append("**Status:** coarse digital fit check only. Dimensions are approximate; no physical fit validation.")
    lines.append("")
    data = report["recommended"]
    lines.append("## Preset: recommended (220 x 120 x 70)")
    lines.append("")
    lines.append(f"- Status: **{data['status']}**")
    lines.append(f"- Modules checked: {data['module_count']}")
    lines.append(f"- Enclosure internal bounds (mm): {data['enclosure_internal_bounds_mm']}")
    if data["outside_enclosure"]:
        lines.append("- Outside enclosure:")
        for item in data["outside_enclosure"]:
            lines.append(f"  - {item['module']}: {item['bounds']}")
    if data["clashes"]:
        lines.append("- AABB clashes:")
        for item in data["clashes"]:
            lines.append(f"  - {item['a']} / {item['b']}")
    if data["barrier_crossings"]:
        lines.append("- Barrier crossings:")
        for item in data["barrier_crossings"]:
            lines.append(f"  - {item['module']}: {item['bounds']}")
    lines.append("")
    lines.append("## Limitations")
    for limitation in report["recommended"]["limitations"]:
        lines.append(f"- {limitation}")
    lines.append("")
    lines.append("## Interpretation")
    lines.append("- A `PASS` is not a safety or manufacturing release.")
    lines.append("- Only the confirmed 220 x 120 x 70 preset is generated; 150 x 100 and 180 x 120 are rejected.")
    lines.append("- Physical fit requires measured samples, tolerance stack, cable bend, and assembly trial.")
    (ROOT / "hardware" / "mechanical" / "FIT_ANALYSIS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_mechanical_bom() -> None:
    rows = [
        ("M-001", "Enclosure body + lid", "220x120x70, 60 mm body + 10 mm lid, ABS/PC FR target", "1 set", "BLOCKED"),
        ("M-002", "M3x16 lid screws", "Stainless steel, pan head, 4 pcs", "4 pcs", "PROVISIONAL"),
        ("M-003", "M3 heat-set inserts", "M3x5.7 brass, 4 pcs", "4 pcs", "PROVISIONAL"),
        ("M-004", "M3x8 module screws", "Stainless steel, pan head", "12 pcs", "PROVISIONAL"),
        ("M-005", "M16 cable gland", "IP68, PA66, UL94 V-0", "1 pcs", "PROVISIONAL"),
        ("M-006", "Type F panel socket", "16 A / 250 V, 2P+E, 45x45 bezel", "1 pcs", "DOCUMENTATION_DEFICIENT"),
        ("M-007", "Type F cord plug", "16 A / 250 V, 3-core", "1 pcs", "DOCUMENTATION_DEFICIENT"),
        ("M-008", "PE stud/screw/lock washer", "Dedicated protective earth bond", "1 set", "BLOCKED"),
        ("M-009", "Thermal pad / barrier", "Flame-retardant, placement TBD", "1 pcs", "PROVISIONAL"),
        ("M-010", "Safety/rating label", "Content TBD after rating chain", "1 pcs", "BLOCKED"),
        ("M-011", "PZEM mounting plate", "Printed/FR plate, 58x94x2 mm, 4xM3", "1 pcs", "PROVISIONAL"),
        ("M-012", "Relay module mounting plate", "Printed/FR plate, 55x26x2 mm, 4xM3", "1 pcs", "PROVISIONAL"),
        ("M-013", "HLK-5M05 mounting plate", "Printed/FR plate, 38x23x2 mm", "1 pcs", "PROVISIONAL"),
        ("M-014", "Lid gasket", "Silicone/EPDM 1.0 mm, 216x116 frame", "1 pcs", "PROVISIONAL"),
        ("M-015", "M12 ePTFE pressure vent", "IP67, M12x1.5", "1 pcs", "PROVISIONAL"),
        ("M-016", "USB service cover", "Printed, 36x26x3 mm, gasket", "1 pcs", "PROVISIONAL"),
        ("M-017", "DevKit reverse-insertion key", "Printed bracket, 2xM3", "1 pcs", "PROVISIONAL"),
        ("M-018", "Cable ties / anchors", "PA66, 100 mm", "8 pcs", "PROVISIONAL"),
    ]
    path = ROOT / "hardware" / "mechanical" / "MECHANICAL_BOM.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        import csv
        writer = csv.writer(handle)
        writer.writerow(["item_id", "description", "specification", "qty", "status"])
        writer.writerows(rows)


def main() -> None:
    for name, elev, azim in [
        ("isometric", 25, -45),
        ("front", 5, -90),
        ("back", 5, 90),
        ("top", 90, -90),
        ("bottom", -90, -90),
    ]:
        render_view(name, elev, azim)
    render_view("exploded", 25, -45, exploded=True)
    render_view("cutaway", 20, -55, cutaway=True)
    dimensions_svg()
    mounting_plan_svg()
    service_access_svg()
    assembly_pdf()
    write_fit_reports()
    write_mechanical_bom()
    print("Rendered views, drawings, fit report, and mechanical BOM.")


if __name__ == "__main__":
    main()
