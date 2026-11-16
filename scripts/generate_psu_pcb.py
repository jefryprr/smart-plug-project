#!/usr/bin/env python3
"""Generate the REV_C mains-entry PSU board (provisional, not for fabrication).

Board: 50 x 70 mm, 2-layer FR4, HLK-5M05, fuse/MOV/TCO, L/N terminals,
3x JST-XH 5 V outputs. The board has a routed isolation notch between the
mains leg and the SELV leg; the HLK module bridges it.

Safety status: ENGINEERING_REVIEW_REQUIRED / HARDWARE_VALIDATION_REQUIRED /
NOT_FOR_FABRICATION. Creepage/clearance values are provisional and unverified.

Run:
  tools\\kicad\\bin\\python.exe scripts\\generate_psu_pcb.py
"""
from __future__ import annotations

from pathlib import Path

import pcbnew

ROOT = Path(__file__).resolve().parents[1]
KICAD = ROOT / "hardware" / "kicad"
KICAD.mkdir(parents=True, exist_ok=True)
BOARD_PATH = KICAD / "psu_rev_c.kicad_pcb"
FP_LIB = ROOT / "tools" / "kicad" / "share" / "kicad" / "footprints"

W, H = 50.0, 65.0
IO = pcbnew.PCB_IO_MGR.FindPlugin(pcbnew.PCB_IO_MGR.KICAD_SEXP)


def mm(v: float) -> int:
    return pcbnew.FromMM(v)


def add_outline(board: pcbnew.BOARD) -> None:
    pts = [
        (0, 0), (19, 0), (19, 45), (21, 45), (21, 0), (50, 0),
        (50, 65), (0, 65), (0, 0),
    ]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        line = pcbnew.PCB_SHAPE(board)
        line.SetShape(pcbnew.SHAPE_T_SEGMENT)
        line.SetStart(pcbnew.VECTOR2I(mm(x1), mm(y1)))
        line.SetEnd(pcbnew.VECTOR2I(mm(x2), mm(y2)))
        line.SetLayer(pcbnew.Edge_Cuts)
        line.SetWidth(mm(0.1))
        board.Add(line)


def add_text(board: pcbnew.BOARD, text: str, x: float, y: float, size: float = 1.0) -> None:
    item = pcbnew.PCB_TEXT(board)
    item.SetText(text)
    item.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
    item.SetLayer(pcbnew.B_SilkS)
    item.SetMirrored(True)
    item.SetTextSize(pcbnew.VECTOR2I(mm(size), mm(size)))
    item.SetTextThickness(mm(0.15))
    board.Add(item)


def add_mounting_holes(board: pcbnew.BOARD) -> None:
    for ref, x, y in [
        ("H1", 3, 3), ("H3", 47, 3), ("H4", 16, 42),
    ]:
        fp = IO.FootprintLoad(str(FP_LIB / "MountingHole.pretty"), "MountingHole_3.2mm_M3")
        fp.SetReference(ref)
        fp.SetValue("M3")
        fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
        fp.SetAttributes(pcbnew.FP_EXCLUDE_FROM_BOM | pcbnew.FP_EXCLUDE_FROM_POS_FILES)
        board.Add(fp)


def add_fiducials(board: pcbnew.BOARD) -> None:
    for ref, x, y in [("FID1", 47, 50), ("FID2", 47, 35), ("FID3", 20, 63)]:
        fp = IO.FootprintLoad(str(FP_LIB / "Fiducial.pretty"), "Fiducial_1mm_Mask2mm")
        fp.SetReference(ref)
        fp.SetValue("FID")
        fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
        fp.SetAttributes(pcbnew.FP_EXCLUDE_FROM_BOM | pcbnew.FP_EXCLUDE_FROM_POS_FILES)
        board.Add(fp)


def load_fp(board: pcbnew.BOARD, ref: str, value: str, lib: str, name: str, x: float, y: float, rot: float = 0.0) -> pcbnew.FOOTPRINT:
    fp = IO.FootprintLoad(str(FP_LIB / f"{lib}.pretty"), name)
    if fp is None:
        raise RuntimeError(f"footprint not found: {lib}:{name}")
    fp.SetReference(ref)
    fp.SetValue(value)
    fp.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
    fp.SetOrientationDegrees(rot)
    fp.Reference().SetVisible(False)
    fp.Value().SetVisible(False)
    for item in fp.GraphicalItems():
        if item.GetLayer() == pcbnew.F_SilkS:
            item.SetLayer(pcbnew.F_Fab)
    board.Add(fp)
    return fp


def add_custom_hlk(board: pcbnew.BOARD) -> pcbnew.FOOTPRINT:
    fp = pcbnew.FOOTPRINT(board)
    fp.SetReference("PS1")
    fp.SetValue("HLK-5M05")
    fp.SetPosition(pcbnew.VECTOR2I(mm(29), mm(20)))
    fp.Reference().SetVisible(False)
    fp.Value().SetVisible(False)
    # Pin positions from the distributor datasheet drawing, rotated 180 deg so
    # AC pins face the mains leg and DC pins face the SELV leg.
    pins = [
        ("1", 45.8, 17.0),  # AC L
        ("2", 45.8, 23.0),  # AC N
        ("3", 12.2, 11.0),  # -Vo
        ("4", 12.2, 29.0),  # +Vo
    ]
    for num, x, y in pins:
        pad = pcbnew.PAD(fp)
        pad.SetNumber(num)
        pad.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
        pad.SetSize(pcbnew.VECTOR2I(mm(2.0), mm(2.0)))
        pad.SetDrillSize(pcbnew.VECTOR2I(mm(1.0), mm(1.0)))
        pad.SetAttribute(pcbnew.PAD_ATTRIB_PTH)
        pad.SetLayerSet(pad.PTHMask())
        pad.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
        fp.Add(pad)
    # Body outline on silkscreen.
    for (x1, y1), (x2, y2) in [
        ((10, 8.5), (48, 8.5)), ((48, 8.5), (48, 31.5)),
        ((48, 31.5), (10, 31.5)), ((10, 31.5), (10, 8.5)),
    ]:
        s = pcbnew.PCB_SHAPE(fp)
        s.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s.SetStart(pcbnew.VECTOR2I(mm(x1), mm(y1)))
        s.SetEnd(pcbnew.VECTOR2I(mm(x2), mm(y2)))
        s.SetLayer(pcbnew.F_Fab)
        s.SetWidth(mm(0.15))
        fp.Add(s)
    board.Add(fp)
    return fp


def add_custom_tco(board: pcbnew.BOARD) -> pcbnew.FOOTPRINT:
    fp = pcbnew.FOOTPRINT(board)
    fp.SetReference("TF1")
    fp.SetValue("SF96E 99C")
    fp.SetPosition(pcbnew.VECTOR2I(mm(42), mm(35.5)))
    fp.Reference().SetVisible(False)
    fp.Value().SetVisible(False)
    for num, y in [("1", 38.0), ("2", 33.0)]:
        pad = pcbnew.PAD(fp)
        pad.SetNumber(num)
        pad.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
        pad.SetSize(pcbnew.VECTOR2I(mm(2.0), mm(2.0)))
        pad.SetDrillSize(pcbnew.VECTOR2I(mm(1.0), mm(1.0)))
        pad.SetAttribute(pcbnew.PAD_ATTRIB_PTH)
        pad.SetLayerSet(pad.PTHMask())
        pad.SetPosition(pcbnew.VECTOR2I(mm(42), mm(y)))
        fp.Add(pad)
    for (x1, y1), (x2, y2) in [
        ((37, 32.0), (47, 32.0)), ((47, 32.0), (47, 39.0)),
        ((47, 39.0), (37, 39.0)), ((37, 39.0), (37, 32.0)),
    ]:
        s = pcbnew.PCB_SHAPE(fp)
        s.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s.SetStart(pcbnew.VECTOR2I(mm(x1), mm(y1)))
        s.SetEnd(pcbnew.VECTOR2I(mm(x2), mm(y2)))
        s.SetLayer(pcbnew.F_Fab)
        s.SetWidth(mm(0.15))
        fp.Add(s)
    board.Add(fp)
    return fp


def add_net(board: pcbnew.BOARD, name: str) -> pcbnew.NETINFO_ITEM:
    net = pcbnew.NETINFO_ITEM(board, name)
    board.Add(net)
    return net


def add_track(board: pcbnew.BOARD, net, start, end, width: float, layer=pcbnew.F_Cu) -> None:
    track = pcbnew.PCB_TRACK(board)
    track.SetStart(pcbnew.VECTOR2I(mm(start[0]), mm(start[1])))
    track.SetEnd(pcbnew.VECTOR2I(mm(end[0]), mm(end[1])))
    track.SetWidth(mm(width))
    track.SetLayer(layer)
    track.SetNet(net)
    board.Add(track)


def add_via(board: pcbnew.BOARD, net, x: float, y: float, size: float = 1.5, drill: float = 0.8) -> None:
    via = pcbnew.PCB_VIA(board)
    via.SetPosition(pcbnew.VECTOR2I(mm(x), mm(y)))
    via.SetWidth(mm(size))
    via.SetDrill(mm(drill))
    via.SetNet(net)
    board.Add(via)


def main() -> None:
    board = pcbnew.BOARD()
    board.SetFileName(str(BOARD_PATH))
    ds = board.GetDesignSettings()
    ds.m_MinClearance = mm(0.5)
    ds.m_TrackMinWidth = mm(0.3)
    ds.m_CopperEdgeClearance = mm(0.5)
    try:
        ds.m_NetSettings.GetNetClassByName("Default").SetClearance(mm(0.5))
    except Exception:
        pass

    add_outline(board)
    add_mounting_holes(board)
    add_fiducials(board)

    # Footprints
    load_fp(board, "TB1", "230VAC IN", "TerminalBlock_Phoenix", "TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal", 29, 62, 0)
    load_fp(board, "TB2", "230VAC OUT", "TerminalBlock_Phoenix", "TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal", 29, 4, 0)
    load_fp(board, "F1", "10A 250V", "Fuse", "Fuseholder_Clip-5x20mm_Littelfuse_111_Inline_P20.00x5.00mm_D1.05mm_Horizontal", 42, 60, 90)
    load_fp(board, "MOV1", "275VAC", "Varistor", "RV_Disc_D9mm_W5.2mm_P5mm", 30, 40, 0)
    add_custom_tco(board)
    add_custom_hlk(board)
    for ref, y, label in [("J5", 55, "OUT1 CARRIER"), ("J6", 45, "OUT2 RELAY"), ("J7", 35, "OUT3 PZEM")]:
        load_fp(board, ref, label, "Connector_JST", "JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical", 5, y, 0)
    load_fp(board, "C1", "100uF", "Capacitor_THT", "CP_Radial_D6.3mm_P2.50mm", 5, 23, 0)
    load_fp(board, "C2", "100nF", "Capacitor_SMD", "C_0805_2012Metric", 5, 30, 0)
    load_fp(board, "F2", "1.1A PTC", "Fuse", "Fuse_1206_3216Metric", 12, 33, 90)
    load_fp(board, "D1", "SMBJ5.0A", "Diode_SMD", "D_SMB", 8, 12, 0)

    # Nets
    nets = {name: add_net(board, name) for name in [
        "L_IN", "N_MAINS", "L_FUSED", "L_LOAD", "+5V_PRE", "+5V", "GND",
    ]}

    by_ref = {fp.GetReference(): fp for fp in board.GetFootprints()}
    def setpad(ref: str, padnum: str, netname: str) -> None:
        fp = by_ref[ref]
        for pad in fp.Pads():
            if pad.GetNumber() == padnum:
                pad.SetNet(nets[netname])

    # Terminal blocks: pin1 N, pin2 L
    setpad("TB1", "1", "N_MAINS"); setpad("TB1", "2", "L_IN")
    setpad("TB2", "1", "N_MAINS"); setpad("TB2", "2", "L_LOAD")
    # Fuse: pad1 lower contact, pad2 upper contact
    setpad("F1", "1", "L_IN"); setpad("F1", "2", "L_FUSED")
    # MOV across L_FUSED/N
    setpad("MOV1", "1", "L_FUSED"); setpad("MOV1", "2", "N_MAINS")
    # TCO in L path
    setpad("TF1", "1", "L_FUSED"); setpad("TF1", "2", "L_LOAD")
    # HLK: 1 AC L, 2 AC N, 3 -Vo, 4 +Vo
    setpad("PS1", "1", "L_LOAD"); setpad("PS1", "2", "N_MAINS")
    setpad("PS1", "3", "GND"); setpad("PS1", "4", "+5V_PRE")
    # 5 V output protection
    setpad("F2", "1", "+5V"); setpad("F2", "2", "+5V_PRE")
    setpad("D1", "1", "+5V"); setpad("D1", "2", "GND")
    setpad("C1", "1", "+5V"); setpad("C1", "2", "GND")
    setpad("C2", "1", "+5V"); setpad("C2", "2", "GND")
    for ref in ("J5", "J6", "J7"):
        setpad(ref, "1", "+5V"); setpad(ref, "2", "GND")

    # Mains tracks: 4 mm L/N, 2.5 mm branches.
    L, N = nets["L_IN"], nets["N_MAINS"]
    LF, LL = nets["L_FUSED"], nets["L_LOAD"]
    add_track(board, N, (29, 62), (26, 62), 4.0)
    add_track(board, N, (26, 62), (26, 5), 4.0)
    add_track(board, N, (26, 5), (29, 5), 4.0)
    add_track(board, L, (34.08, 62), (42, 62), 4.0)
    add_track(board, L, (42, 62), (42, 60), 4.0)
    add_track(board, L, (42, 60), (42, 55), 4.0)
    add_track(board, LF, (42, 45), (42, 40), 4.0)
    add_track(board, LF, (42, 40), (42, 38.0), 4.0)
    add_track(board, LL, (42, 33.0), (42, 4), 4.0)
    add_track(board, LL, (42, 4), (34.08, 4), 4.0)
    # MOV branches (protection device, 1.5 mm)
    add_track(board, LF, (42, 40), (30, 40), 1.5)
    add_track(board, N, (26, 42.5), (35, 42.5), 1.5)
    # HLK AC L branch
    add_track(board, LL, (42, 17), (45.8, 17), 2.5)
    # HLK AC N branch: crossover on B.Cu, vias at both ends.
    add_via(board, N, 26, 23)
    add_via(board, N, 47, 23)
    add_track(board, N, (26, 23), (47, 23), 4.0, pcbnew.B_Cu)
    add_track(board, N, (47, 23), (45.8, 23), 2.5)

    # 5 V SELV tracks: 1 mm. +5V bus x=2, GND bus x=9.2.
    V, PRE, G = nets["+5V"], nets["+5V_PRE"], nets["GND"]
    # HLK +Vo -> PTC input (pad 2 at y=31.6)
    add_track(board, PRE, (12.2, 29), (12, 29), 1.0)
    add_track(board, PRE, (12, 29), (12, 31.6), 1.0)
    # PTC output (pad 1 at y=34.4) -> 5V bus via B.Cu
    add_via(board, V, 12, 34.4, 1.1, 0.8)
    add_via(board, V, 2, 34.4, 1.1, 0.8)
    add_track(board, V, (12, 34.4), (12, 32.5), 1.0, pcbnew.B_Cu)
    add_track(board, V, (12, 32.5), (2, 32.5), 1.0, pcbnew.B_Cu)
    add_track(board, V, (2, 32.5), (2, 34.4), 1.0, pcbnew.B_Cu)
    add_track(board, V, (2, 12), (2, 55), 1.0)
    # GND bus
    add_track(board, G, (12.2, 11), (9.2, 11), 1.0)
    add_track(board, G, (9.2, 11), (9.2, 55), 1.0)
    # JST branches
    for y in (55, 45, 35):
        add_track(board, V, (2, y), (5, y), 1.0)
        add_track(board, G, (7.5, y), (9.2, y), 1.0)
    # C1/C2/D1 branches
    add_track(board, V, (2, 23), (5, 23), 1.0)
    add_track(board, G, (7.5, 23), (9.2, 23), 1.0)
    add_track(board, V, (2, 30), (4.05, 30), 1.0)
    add_track(board, G, (5.95, 30), (9.2, 30), 1.0)
    add_track(board, V, (2, 12), (5.85, 12), 1.0)
    add_track(board, G, (10.15, 12), (9.2, 12), 1.0)

    # Labels
    add_text(board, "MAINS 230VAC 8A - REVIEW ONLY", 14, 58, 0.8)
    add_text(board, "SELV 5V", 4, 10, 0.8)
    add_text(board, "F1 10A 250V", 25, 50, 0.8)
    add_text(board, "TCO 99C", 25, 32, 0.8)
    add_text(board, "HLK-5M05", 6, 20, 0.8)
    add_text(board, "OUT1 CARRIER", 14, 56, 0.8)
    add_text(board, "OUT2 RELAY", 14, 46, 0.8)
    add_text(board, "OUT3 PZEM", 14, 36, 0.8)
    add_text(board, "PE OFF-BOARD - CHASSIS STUD", 32, 8, 0.8)
    add_text(board, "REV_C PSU - NOT FOR FABRICATION", 14, 53, 0.8)

    board.BuildListOfNets()
    pcbnew.SaveBoard(str(BOARD_PATH), board)
    print(f"Wrote {BOARD_PATH} with {len(board.GetFootprints())} footprints and {board.GetNetCount()} nets")


if __name__ == "__main__":
    main()
