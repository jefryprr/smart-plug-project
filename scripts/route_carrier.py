#!/usr/bin/env python3
"""Grid-router for the REV_B SELV carrier.

This is deliberately a simple two-layer Manhattan router, not a production
autorouter. It exists to produce a coherent routed prototype carrier and to
surface unroutable placement early. DRC and engineering review are still
required.

Run after scripts/generate_carrier_pcb.py:
  tools\\kicad\\bin\\python.exe scripts\\route_carrier.py
"""
from __future__ import annotations

import heapq
import math
from pathlib import Path

import pcbnew

ROOT = Path(__file__).resolve().parents[1]
BOARD_PATH = ROOT / "hardware" / "kicad" / "smartplug.kicad_pcb"
GRID = 0.5
W = int(100 / GRID)
H = int(70 / GRID)
TRACK_W = 0.3
POWER_W = 0.6
CLEAR = 0.2
CLEAR_PAD = 0.2
VIA_COST = 1000

# Import the same net map used by the generator.
import sys
sys.path.insert(0, str(ROOT / "scripts"))
from generate_carrier_pcb import NETS  # noqa: E402

POWER_NETS = {"+5V", "+3V3"}
GND = "GND"


def to_grid(x_mm: float, y_mm: float) -> tuple[int, int]:
    return max(1, min(W - 2, int(round(x_mm / GRID)))), max(1, min(H - 2, int(round(y_mm / GRID))))


def mm(v: int) -> float:
    return v * GRID


class Router:
    def __init__(self, board):
        self.board = board
        self.blocked = [bytearray(W * H) for _ in range(2)]
        self.owner = [dict() for _ in range(2)]
        self.by_ref = {fp.GetReference(): fp for fp in board.GetFootprints()}
        self.nets = {n.GetNetname(): n for n in board.GetNetsByName().values() if n.GetNetname()}

    def idx(self, x: int, y: int) -> int:
        return y * W + x

    def mark_pad(self, pad, netname: str):
        box = pad.GetBoundingBox()
        x0 = pcbnew.ToMM(box.GetX()) - CLEAR_PAD
        y0 = pcbnew.ToMM(box.GetY()) - CLEAR_PAD
        x1 = x0 + pcbnew.ToMM(box.GetWidth()) + 2 * CLEAR_PAD
        y1 = y0 + pcbnew.ToMM(box.GetHeight()) + 2 * CLEAR_PAD
        gx0, gy0 = to_grid(x0, y0)
        gx1, gy1 = to_grid(x1, y1)
        layers = []
        if pad.IsOnLayer(pcbnew.F_Cu):
            layers.append(0)
        if pad.IsOnLayer(pcbnew.B_Cu):
            layers.append(1)
        for layer in layers:
            for y in range(gy0, gy1 + 1):
                for x in range(gx0, gx1 + 1):
                    self.blocked[layer][self.idx(x, y)] = 1
                    self.owner[layer][(x, y)] = netname

    def build_obstacles(self):
        # Mark every pad, including unused/no-net pads. Tracks must not run
        # through an unassigned header pin just because it is not in NETS.
        for fp in self.board.GetFootprints():
            for pad in fp.Pads():
                self.mark_pad(pad, pad.GetNetname() or "<no net>")

    def pad_cells(self, ref: str, padnum: int):
        fp = self.by_ref[ref]
        pad = fp.FindPadByNumber(str(padnum))
        pos = pad.GetPosition()
        cx, cy = to_grid(pcbnew.ToMM(pos.x), pcbnew.ToMM(pos.y))
        layers = []
        if pad.IsOnLayer(pcbnew.F_Cu):
            layers.append(0)
        if pad.IsOnLayer(pcbnew.B_Cu):
            layers.append(1)
        # Return every grid cell whose centre lies inside the pad bounding
        # box. A single nearest cell can collapse two 0805 pads (1.825 mm
        # apart) onto the same cell on a 0.5 mm grid, causing false shorts.
        box = pad.GetBoundingBox()
        x0 = pcbnew.ToMM(box.GetX())
        y0 = pcbnew.ToMM(box.GetY())
        x1 = x0 + pcbnew.ToMM(box.GetWidth())
        y1 = y0 + pcbnew.ToMM(box.GetHeight())
        cells = []
        for ix in range(int(math.ceil(x0 / GRID)), int(math.floor(x1 / GRID)) + 1):
            for iy in range(int(math.ceil(y0 / GRID)), int(math.floor(y1 / GRID)) + 1):
                if 1 <= ix < W - 1 and 1 <= iy < H - 1:
                    for layer in layers:
                        cells.append((ix, iy, layer))
        if not cells:
            x, y = cx, cy
            if 1 <= x < W - 1 and 1 <= y < H - 1:
                for layer in layers:
                    cells.append((x, y, layer))
        return cells

    def pad_ignore_cells(self, ref: str, padnum: int, netname: str) -> set[tuple[int, int, int]]:
        """Allow escape only from the current net's own pad clearance ring."""
        pad = self.by_ref[ref].FindPadByNumber(str(padnum))
        box = pad.GetBoundingBox()
        expand = CLEAR_PAD + 0.3
        x0 = pcbnew.ToMM(box.GetX()) - expand
        y0 = pcbnew.ToMM(box.GetY()) - expand
        x1 = x0 + pcbnew.ToMM(box.GetWidth()) + 2 * expand
        y1 = y0 + pcbnew.ToMM(box.GetHeight()) + 2 * expand
        layers = []
        if pad.IsOnLayer(pcbnew.F_Cu):
            layers.append(0)
        if pad.IsOnLayer(pcbnew.B_Cu):
            layers.append(1)
        cells = set()
        for ix in range(int(math.ceil(x0 / GRID)), int(math.floor(x1 / GRID)) + 1):
            for iy in range(int(math.ceil(y0 / GRID)), int(math.floor(y1 / GRID)) + 1):
                for layer in layers:
                    if self.owner[layer].get((ix, iy)) == netname:
                        cells.add((ix, iy, layer))
        return cells

    def pad_xy(self, ref: str, padnum: int):
        pad = self.by_ref[ref].FindPadByNumber(str(padnum))
        pos = pad.GetPosition()
        return pcbnew.ToMM(pos.x), pcbnew.ToMM(pos.y)

    def free(self, x: int, y: int, layer: int, ignore: set[tuple[int, int, int]]) -> bool:
        if (x, y, layer) in ignore:
            return True
        return not self.blocked[layer][self.idx(x, y)]

    def astar(self, start_cells, goal_cells, netname: str, width: float, ignore: set[tuple[int, int, int]] | None = None):
        start_set = set(start_cells)
        goal_set = set(goal_cells)
        # Unblock only the clearance ring of the current net's own pads.
        if ignore is None:
            ignore = set()
        ignore = set(ignore) | set(start_set) | set(goal_set)
        openq = []
        gscore = {}
        came = {}
        for x, y, layer in start_set:
            # Start on F.Cu whenever possible; the B.Cu plane is reserved for
            # the GND zone so it stays continuous.
            if layer != 0:
                continue
            if self.free(x, y, layer, ignore):
                s = (x, y, layer)
                gscore[s] = 0
                heapq.heappush(openq, (0, s))
        if not openq:
            return None
        while openq:
            _, cur = heapq.heappop(openq)
            cx, cy, cl = cur
            if (cx, cy, cl) in goal_set:
                path = [cur]
                while cur in came:
                    cur = came[cur]
                    path.append(cur)
                path.reverse()
                return path
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = cx + dx, cy + dy
                if not (1 <= nx < W - 1 and 1 <= ny < H - 1):
                    continue
                if not self.free(nx, ny, cl, ignore):
                    continue
                nxt = (nx, ny, cl)
                ng = gscore[cur] + 1
                if ng < gscore.get(nxt, 1 << 30):
                    gscore[nxt] = ng
                    h = abs(nx - next(iter(goal_set))[0]) + abs(ny - next(iter(goal_set))[1])
                    came[nxt] = cur
                    heapq.heappush(openq, (ng + h, nxt))
            # via
            nl = 1 - cl
            if self.free(cx, cy, nl, ignore):
                nxt = (cx, cy, nl)
                ng = gscore[cur] + VIA_COST
                if ng < gscore.get(nxt, 1 << 30):
                    gscore[nxt] = ng
                    h = abs(cx - next(iter(goal_set))[0]) + abs(cy - next(iter(goal_set))[1])
                    came[nxt] = cur
                    heapq.heappush(openq, (ng + h, nxt))
        return None

    def mark_path(self, path, netname: str, width: float):
        radius = max(1, int(math.ceil((width / 2 + CLEAR) / GRID)))
        for x, y, layer in path:
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    nx, ny = x + dx, y + dy
                    if 1 <= nx < W - 1 and 1 <= ny < H - 1:
                        self.blocked[layer][self.idx(nx, ny)] = 1
                        self.owner[layer][(nx, ny)] = netname

    def add_path(self, path, netname: str, width: float, start_pad=None, end_pad=None):
        net = self.nets.get(netname)
        if net is None:
            print(f"  net missing: {netname}")
            return
        # Merge collinear runs.
        start = path[0]
        prev = path[0]
        direction = None
        for cell in path[1:]:
            x, y, layer = cell
            px, py, pl = prev
            d = (x - px, y - py, layer - pl)
            if direction is None or d == direction:
                direction = d
                prev = cell
                continue
            self._track(start, prev, net, width)
            start = prev
            direction = d
            prev = cell
        self._track(start, prev, net, width)
        # Stub from the first/last grid cell to the actual pad centre so KiCad
        # connectivity recognises the connection (cell centres are approximate).
        # No diagonal pad stubs: the A* start/goal cells are chosen inside the
        # pad, and a diagonal stub can clip an adjacent pad. If connectivity
        # fails, move the pad or adjust the grid rather than adding a stub.
        # Vias at layer changes.
        for a, b in zip(path, path[1:]):
            if a[2] != b[2]:
                via = pcbnew.PCB_VIA(self.board)
                via.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(mm(a[0])), pcbnew.FromMM(mm(a[1]))))
                via.SetWidth(pcbnew.FromMM(0.8))
                via.SetDrill(pcbnew.FromMM(0.4))
                via.SetNet(net)
                self.board.Add(via)

    def _track(self, a, b, net, width):
        if a[0] == b[0] and a[1] == b[1] and a[2] == b[2]:
            return
        track = pcbnew.PCB_TRACK(self.board)
        track.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(mm(a[0])), pcbnew.FromMM(mm(a[1]))))
        track.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(mm(b[0])), pcbnew.FromMM(mm(b[1]))))
        track.SetWidth(pcbnew.FromMM(width))
        track.SetLayer(pcbnew.F_Cu if a[2] == 0 else pcbnew.B_Cu)
        track.SetNet(net)
        self.board.Add(track)

    def route_net(self, netname: str, pads: list[tuple[str, int]]):
        if netname == "NC":
            return True
        width = POWER_W if netname in POWER_NETS else TRACK_W
        unconnected = list(pads)
        first = unconnected.pop(0)
        connected = [first]
        ok = True
        while unconnected:
            # Connect the nearest remaining pad to any already-connected pad.
            best = None
            for a in connected:
                for b in unconnected:
                    pa = self.pad_cells(*a)
                    pb = self.pad_cells(*b)
                    d = min(abs(x1 - x2) + abs(y1 - y2) for x1, y1, _ in pa for x2, y2, _ in pb)
                    if best is None or d < best[0]:
                        best = (d, a, b)
            _, a, b = best
            ignore = self.pad_ignore_cells(*a, netname) | self.pad_ignore_cells(*b, netname)
            path = self.astar(self.pad_cells(*a), self.pad_cells(*b), netname, width, ignore)
            if path is None:
                path = self.astar(self.pad_cells(*b), self.pad_cells(*a), netname, width, ignore)
            if path is None:
                print(f"  FAIL {netname}: {a} -> {b}")
                ok = False
                connected.append(b)
                unconnected.remove(b)
                continue
            self.add_path(path, netname, width, a, b)
            self.mark_path(path, netname, width)
            connected.append(b)
            unconnected.remove(b)
        return ok


def add_gnd_zone(board):
    net = next((n for n in board.GetNetsByName().values() if n.GetNetname() == GND), None)
    if net is None:
        print("GND net missing")
        return
    zone = pcbnew.ZONE(board)
    zone.SetLayer(pcbnew.B_Cu)
    zone.SetNet(net)
    zone.SetLocalClearance(pcbnew.FromMM(0.3))
    zone.SetMinThickness(pcbnew.FromMM(0.25))
    zone.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)
    try:
        zone.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
    except Exception:
        pass
    outline = zone.Outline()
    outline.NewOutline()
    inset = 0.5
    for x, y in [(inset, inset), (100 - inset, inset), (100 - inset, 70 - inset), (inset, 70 - inset)]:
        outline.Append(pcbnew.FromMM(x), pcbnew.FromMM(y))
    board.Add(zone)
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())


def add_gnd_vias(board):
    net = next((n for n in board.GetNetsByName().values() if n.GetNetname() == GND), None)
    if net is None:
        return
    for fp in board.GetFootprints():
        for pad in fp.Pads():
            if pad.GetNetname() != GND:
                continue
            if pad.IsOnLayer(pcbnew.F_Cu) and not pad.IsOnLayer(pcbnew.B_Cu):
                pos = pad.GetPosition()
                via = pcbnew.PCB_VIA(board)
                via.SetPosition(pos)
                via.SetWidth(pcbnew.FromMM(0.8))
                via.SetDrill(pcbnew.FromMM(0.4))
                via.SetNet(net)
                board.Add(via)


def main():
    board = pcbnew.LoadBoard(str(BOARD_PATH))
    router = Router(board)
    router.build_obstacles()
    order = ["RTC_INT", "RGB_DATA_3V3", "PZEM_TX_3V3", "PZEM_RX_3V3", "+3V3", "BUTTON", "RELAY_CTRL", "SCL", "SDA", "PZEM_RX_5V", "RELAY_GATE", "RELAY_IN", "PZEM_TX_5V", "RGB_DATA_5V", "RGB_DATA_OUT", "+5V"]
    order += [n for n in NETS if n not in set(order) and n not in {GND, "NC"}]
    all_ok = True
    for netname in order:
        pads = NETS[netname]
        print(f"route {netname}: {len(pads)} pads")
        if not router.route_net(netname, pads):
            all_ok = False
    add_gnd_vias(board)
    add_gnd_zone(board)
    try:
        board.GetDesignSettings().m_NetSettings.GetNetClassByName("Default").SetClearance(pcbnew.FromMM(0.15))
    except Exception:
        pass
    pcbnew.SaveBoard(str(BOARD_PATH), board)
    # Re-open and set the default netclass clearance to 0.15 mm. Setting it
    # before the first SaveBoard can be overwritten by KiCad's board setup.
    board2 = pcbnew.LoadBoard(str(BOARD_PATH))
    try:
        board2.GetDesignSettings().m_NetSettings.GetNetClassByName("Default").SetClearance(pcbnew.FromMM(0.15))
    except Exception:
        pass
    pcbnew.SaveBoard(str(BOARD_PATH), board2)
    print("routing complete" if all_ok else "routing complete WITH FAILURES")
    print(f"saved {BOARD_PATH} (default clearance 0.15 mm)")


if __name__ == "__main__":
    main()
