#!/usr/bin/env python3
"""Generate the REV_D_CORE_ONLY SELV carrier PCB with pcbnew.

The carrier is deliberately low-voltage only. Mains modules (PZEM, relay,
HLK-5M05) remain off-board. REV_D_CORE_ONLY removes the TMP102 and the external
ADuM1201/B0505S barrier; PZEM's internal optocouplers are the galvanic
barrier, and the carrier only level-shifts its 5 V TTL UART.

Run with KiCad's bundled Python:
  tools\\kicad\\bin\\python.exe scripts\\generate_carrier_pcb.py
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import pcbnew

ROOT = Path(__file__).resolve().parents[1]
KICAD = ROOT / "hardware" / "kicad"
CARRIER = ROOT / "hardware" / "carrier"
KICAD.mkdir(parents=True, exist_ok=True)
CARRIER.mkdir(parents=True, exist_ok=True)

FP_LIB = ROOT / "tools" / "kicad" / "share" / "kicad" / "footprints"
BOARD_W = 100.0
BOARD_H = 70.0
GRID = 1.0
TRACK_W = 0.4
CLEARANCE = 0.3

IO = pcbnew.PCB_IO_MGR.FindPlugin(pcbnew.PCB_IO_MGR.KICAD_SEXP)


def mm(value: float) -> int:
    return pcbnew.FromMM(value)


# ref, value, footprint library, footprint name, x, y, rotation
# The DevKitC-1 has two separate 1x22 headers (J1 and J3), 22.86 mm apart.
# Do not use a 2x22 socket: its rows are only 2.54 mm apart.
COMPONENTS = [
    ("J1A", "ESP32-S3-DevKitC-1 J1", "Connector_PinSocket_2.54mm", "PinSocket_1x22_P2.54mm_Vertical", 10.0, 10.0, 90.0),
    ("J1B", "ESP32-S3-DevKitC-1 J3", "Connector_PinSocket_2.54mm", "PinSocket_1x22_P2.54mm_Vertical", 10.0, 32.86, 90.0),
    ("J2", "PZEM_TTL", "Connector_JST", "JST_XH_B4B-XH-A_1x04_P2.50mm_Vertical", 75.0, 6.0, 0.0),
    ("J3", "RELAY", "Connector_JST", "JST_XH_B4B-XH-A_1x04_P2.50mm_Vertical", 93.0, 57.0, 180.0),
    ("J6", "BUTTON", "Connector_JST", "JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical", 43.0, 63.0, 0.0),
    ("J8", "5V_IN", "Connector_JST", "JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical", 70.0, 63.0, 0.0),
    ("U9", "74HCT125N", "Package_DIP", "DIP-14_W7.62mm", 70.0, 34.0, 0.0),
    ("Q1", "AO3400A", "Package_TO_SOT_SMD", "SOT-23", 85.0, 34.0, 0.0),
    ("R1", "1k", "Resistor_SMD", "R_0805_2012Metric", 76.0, 28.0, 0.0),
    ("R2", "100k", "Resistor_SMD", "R_0805_2012Metric", 84.0, 50.0, 0.0),
    ("R4", "10k", "Resistor_SMD", "R_0805_2012Metric", 80.0, 20.0, 0.0),
    ("R5", "20k", "Resistor_SMD", "R_0805_2012Metric", 84.0, 20.0, 0.0),
    ("R8", "10k", "Resistor_SMD", "R_0805_2012Metric", 40.0, 54.0, 0.0),
    ("C1", "100uF", "Capacitor_SMD", "CP_Elec_6.3x5.4", 64.0, 56.0, 0.0),
    ("C2", "100nF", "Capacitor_SMD", "C_0805_2012Metric", 56.0, 42.0, 0.0),
    ("C3", "100nF", "Capacitor_SMD", "C_0805_2012Metric", 58.0, 48.0, 0.0),
    ("FID1", "FID", "Fiducial", "Fiducial_1mm_Mask2mm", 5.0, 35.0, 0.0),
    ("FID2", "FID", "Fiducial", "Fiducial_1mm_Mask2mm", 95.0, 35.0, 0.0),
    ("FID3", "FID", "Fiducial", "Fiducial_1mm_Mask2mm", 50.0, 40.0, 0.0),
]

# Nets are defined as (reference, pad number) pairs.
# J1A = DevKitC-1 J1, J1B = DevKitC-1 J3. Header pin numbers refer to the
# official 1x22 tables, not odd/even socket numbering.
NETS = {
    "+5V": [("J1A", 21), ("J8", 1), ("J2", 1), ("J3", 1), ("U9", 14), ("C1", 1), ("C2", 1), ("C3", 1)],
    "+3V3": [("J1A", 1), ("J1A", 2), ("R8", 1)],
    "GND": [
        ("J1A", 22), ("J1B", 1), ("J1B", 21), ("J1B", 22), ("J8", 2), ("J2", 4), ("J3", 2),
        ("J6", 2), ("U9", 7), ("U9", 1), ("U9", 4), ("U9", 5),
        ("U9", 9), ("U9", 10), ("U9", 12), ("U9", 13), ("Q1", 2), ("C1", 2), ("C2", 2), ("C3", 2),
        ("R2", 2), ("R5", 2),
    ],
    "BUTTON": [("J1A", 5), ("J6", 1), ("R8", 2)],
    "RELAY_CTRL": [("J1A", 4), ("R1", 1)],
    "RELAY_GATE": [("R1", 2), ("R2", 1), ("Q1", 1)],
    "RELAY_IN": [("Q1", 3), ("J3", 3), ("J3", 4)],
    "PZEM_TX_3V3": [("J1A", 10), ("U9", 2)],
    "PZEM_RX_5V": [("U9", 3), ("J2", 2)],
    "PZEM_TX_5V": [("J2", 3), ("R4", 1)],
    "PZEM_RX_3V3": [("R4", 2), ("R5", 1), ("J1A", 11)],
}

# Unused pads are left netless. J1A pins 3,6,7,8,9,12,13,14,15,16,17-20 and
# almost all J1B pins are intentionally unconnected. U9 gates 2-4 are unused:
# inputs/OE tied to GND, outputs left open.
NO_CONNECT = [("U9", 6), ("U9", 8), ("U9", 11)]

def add_footprint(board, ref, value, lib, name, x, y, rot):
    fp = IO.FootprintLoad(str(FP_LIB / f"{lib}.pretty"), name)
    if fp is None:
        raise RuntimeError(f"footprint not found: {lib}:{name}")
    fp.SetReference(ref)
    fp.SetValue(value)
    fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
    fp.SetOrientationDegrees(rot)
    # Reference/value text on silkscreen causes overlaps on this dense carrier.
    # Keep them in the fab/assembly data instead; board-level labels are added
    # separately below.
    fp.Reference().SetVisible(False)
    fp.Value().SetVisible(False)
    # Slightly smaller annular pads on the 2.54 mm sockets improve routing.
    if ref in {"J1A", "J1B"}:
        for pad in fp.Pads():
            pad.SetSize(pcbnew.VECTOR2I(mm(1.4), mm(1.4)))
    board.Add(fp)
    return fp


def add_outline(board):
    rect = pcbnew.PCB_SHAPE(board)
    rect.SetShape(pcbnew.SHAPE_T_RECT)
    rect.SetStart(pcbnew.VECTOR2I(mm(0.0), mm(0.0)))
    rect.SetEnd(pcbnew.VECTOR2I(mm(BOARD_W), mm(BOARD_H)))
    rect.SetLayer(pcbnew.Edge_Cuts)
    rect.SetWidth(mm(0.1))
    board.Add(rect)


def add_mounting_holes(board):
    for i, (x, y) in enumerate([(3.5, 3.5), (BOARD_W - 3.5, 3.5), (3.5, BOARD_H - 3.5), (BOARD_W - 3.5, BOARD_H - 3.5)], start=1):
        fp = IO.FootprintLoad(str(FP_LIB / "MountingHole.pretty"), "MountingHole_3.2mm_M3")
        fp.SetReference(f"H{i}")
        fp.SetValue("M3")
        fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
        fp.SetAttributes(pcbnew.FP_EXCLUDE_FROM_BOM | pcbnew.FP_EXCLUDE_FROM_POS_FILES)
        board.Add(fp)


def add_text(board, text, x, y, size=1.0, layer=pcbnew.F_SilkS):
    item = pcbnew.PCB_TEXT(board)
    item.SetText(text)
    item.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
    item.SetLayer(layer)
    item.SetTextSize(pcbnew.VECTOR2I(mm(size), mm(size)))
    item.SetTextThickness(mm(0.15))
    board.Add(item)


def assign_nets(board):
    by_ref = {fp.GetReference(): fp for fp in board.GetFootprints()}
    for name, pads in NETS.items():
        if name == "NC":
            continue
        net = pcbnew.NETINFO_ITEM(board, name)
        board.Add(net)
        for ref, padnum in pads:
            fp = by_ref.get(ref)
            if fp is None:
                raise RuntimeError(f"missing {ref}")
            pad = fp.FindPadByNumber(str(padnum))
            if pad is None:
                raise RuntimeError(f"missing pad {ref}.{padnum}")
            pad.SetNet(net)
    # Explicit no-connect flags for unused pads.
    for ref, padnum in NO_CONNECT:
        fp = by_ref.get(ref)
        if fp:
            pad = fp.FindPadByNumber(str(padnum))
            if pad:
                pad.SetProperty(pcbnew.PAD_PROPERTY_NET_NAMES) if False else None


def configure_rules(board):
    ds = board.GetDesignSettings()
    ds.m_MinClearance = mm(0.15)
    try:
        ds.m_NetSettings.GetNetClassByName("Default").SetClearance(mm(0.15))
    except Exception:
        pass
    ds.m_TrackMinWidth = mm(0.25)
    ds.m_CopperEdgeClearance = mm(0.5)
    ds.SetCustomTrackWidth(mm(TRACK_W))
    ds.SetCustomViaSize(mm(0.8))
    ds.SetCustomViaDrill(mm(0.4))
    ds.UseCustomTrackViaSize(True)


def board_svg(board, path):
    # Quick visual check: plot F.Cu + Edge.Cuts to SVG.
    plot = pcbnew.PLOT_CONTROLLER(board)
    opts = plot.GetPlotOptions()
    opts.SetOutputDirectory(str(path.parent))
    opts.SetOutputFilename(str(path.stem))
    opts.SetFormat(pcbnew.PLOT_FORMAT_SVG)
    opts.SetPlotFrameRef(False)
    opts.SetPlotValue(False)
    opts.SetPlotReference(True)
    opts.SetPlotInvisibleText(False)
    opts.SetExcludeEdgeLayer(False)
    for layer in [pcbnew.F_Cu, pcbnew.F_SilkS, pcbnew.Edge_Cuts]:
        plot.SetLayer(layer)
        plot.OpenPlotfile("carrier", pcbnew.PLOT_FORMAT_SVG, layer)
        plot.PlotLayout()
    plot.ClosePlot()


def main():
    board = pcbnew.BOARD()
    board.SetFileName(str(KICAD / "smartplug.kicad_pcb"))
    configure_rules(board)
    add_outline(board)
    add_mounting_holes(board)
    for comp in COMPONENTS:
        add_footprint(board, *comp)
    assign_nets(board)
    board.BuildListOfNets()
    add_text(board, "SMART PLUG REV_D_CORE_ONLY - SELV CARRIER", 50, 3.5, 1.0)
    add_text(board, "NO MAINS ON THIS PCB - NOT CERTIFIED", 50, 68.0, 0.8)
    add_text(board, "ESP32-S3 J1A/J1B - 22.86 mm rows", 37, 21.5, 0.8)
    add_text(board, "PZEM", 66.5, 9.0, 0.8)
    add_text(board, "RELAY", 83, 3.0, 0.8)
    add_text(board, "BTN   5V", 43, 57.0, 0.8)
    add_text(board, "74HCT125", 73, 31.0, 0.8)
    add_text(board, "PZEM DIVIDER / 74HCT125", 62, 16.0, 0.8)
    pcbnew.SaveBoard(str(KICAD / "smartplug.kicad_pcb"), board)
    # SVG preview is exported separately via kicad-cli to avoid GUI plot API drift.
    (CARRIER / "placement.json").write_text(
        json.dumps([{"ref": c[0], "value": c[1], "footprint": f"{c[2]}:{c[3]}", "x": c[4], "y": c[5], "rot": c[6]} for c in COMPONENTS], indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {KICAD / 'smartplug.kicad_pcb'} with {len(COMPONENTS)} footprints and {len(NETS)} nets")


if __name__ == "__main__":
    main()
