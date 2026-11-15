#!/usr/bin/env python3
"""Render the system architecture and safety-domain diagram with Graphviz."""
from __future__ import annotations

import os
from pathlib import Path

from graphviz import Digraph

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "hardware"
OUT.mkdir(parents=True, exist_ok=True)
GRAPHVIZ_BIN = ROOT / "tools" / "graphviz" / "Graphviz-16.1.1-win64" / "bin"
if GRAPHVIZ_BIN.exists():
    os.environ["PATH"] = f"{GRAPHVIZ_BIN}{os.pathsep}{os.environ.get('PATH', '')}"

dot = Digraph("smartplug_architecture", format="png")
dot.attr(rankdir="LR", bgcolor="white", fontname="Arial", fontsize="11", splines="ortho", nodesep="0.35", ranksep="0.6")
dot.attr("node", shape="box", style="rounded,filled", fontname="Arial", fontsize="10", margin="0.12,0.06")
dot.attr("edge", fontname="Arial", fontsize="8", color="#555555")

with dot.subgraph(name="cluster_mains") as mains:
    mains.attr(label="DOMAIN A — MAINS 230 VAC (BLOCKED / REVIEW REQUIRED)", style="rounded,dashed", color="#b42318", bgcolor="#fdecea", fontcolor="#b42318")
    mains.node("P1", "Plug Type F\nL / N / PE", fillcolor="#ffd6d1")
    mains.node("F1", "Fuse 10 A\n+ holder", fillcolor="#ffd6d1")
    mains.node("MOV", "MOV 275 VAC\n(surge study)", fillcolor="#ffd6d1")
    mains.node("TF1", "Thermal cutoff\n99 °C one-shot", fillcolor="#ffd6d1")
    mains.node("K1", "Relay DPST-NO\n8 A class TBD", fillcolor="#ffd6d1")
    mains.node("X1", "Socket Type F\n16 A class TBD", fillcolor="#ffd6d1")

with dot.subgraph(name="cluster_barrier") as barrier:
    barrier.attr(label="ISOLATION BARRIER (UNVERIFIED)", style="rounded,dashed", color="#9a5b00", bgcolor="#fff4df", fontcolor="#9a5b00")
    barrier.node("PS1", "PSU IRM-05-5\n5 V 1 A", fillcolor="#ffe8b8")
    barrier.node("U6", "ADuM1201\nUART isolator", fillcolor="#ffe8b8")
    barrier.node("U7", "B0505S\nisolated 5 V", fillcolor="#ffe8b8")

with dot.subgraph(name="cluster_selv") as selv:
    selv.attr(label="DOMAIN C — SELV 5 V / 3.3 V", style="rounded", color="#067647", bgcolor="#e6f6ee", fontcolor="#067647")
    selv.node("U1", "ESP32-S3\nDevKitC-1 N16R8", fillcolor="#c9f2dd")
    selv.node("CARR", "Low-voltage carrier\nGPIO / I2C / UART", fillcolor="#c9f2dd")
    selv.node("UI", "OLED + button\n+ RGB", fillcolor="#c9f2dd")
    selv.node("TEMP", "TMP102 + RTC\nDS3231", fillcolor="#c9f2dd")
    selv.node("DRV", "Relay driver\nAO3400 + pulldown", fillcolor="#c9f2dd")

with dot.subgraph(name="cluster_cloud") as cloud:
    cloud.attr(label="DOMAIN D — NETWORK / SOFTWARE", style="rounded", color="#175cd3", bgcolor="#e8f1ff", fontcolor="#175cd3")
    cloud.node("MQTT", "MQTT broker\nTLS / ACL", fillcolor="#cfe0ff")
    cloud.node("API", "Backend API\nFastify + SQLite/PG", fillcolor="#cfe0ff")
    cloud.node("WEB", "Next.js dashboard", fillcolor="#cfe0ff")
    cloud.node("APP", "Android Expo app", fillcolor="#cfe0ff")
    cloud.node("NOTIF", "Telegram / push\n(provider mock)", fillcolor="#cfe0ff")

dot.edge("P1", "F1", label="L")
dot.edge("F1", "MOV", label="L-N")
dot.edge("F1", "TF1", label="L")
dot.edge("TF1", "K1", label="L")
dot.edge("K1", "X1", label="L / N")
dot.edge("P1", "X1", label="PE continuous\n(no relay/fuse)", style="bold", color="#067647")
dot.edge("P1", "PS1", label="L/N")
dot.edge("PS1", "CARR", label="+5 V SELV")
dot.edge("P1", "U6", label="PZEM voltage/CT\n(not shown)", style="dashed", color="#9a5b00")
dot.edge("U7", "U6", label="isolated 5 V", style="dashed", color="#9a5b00")
dot.edge("U6", "CARR", label="isolated UART", style="dashed", color="#9a5b00")
dot.edge("CARR", "U1", label="3.3 V / GPIO")
dot.edge("CARR", "UI", label="I2C / GPIO")
dot.edge("CARR", "TEMP", label="I2C")
dot.edge("U1", "DRV", label="RELAY_CTRL")
dot.edge("DRV", "K1", label="coil (SELV)", style="dashed")
dot.edge("U1", "MQTT", label="Wi-Fi")
dot.edge("MQTT", "API", label="telemetry / ACK")
dot.edge("API", "WEB", label="REST / WS")
dot.edge("API", "APP", label="REST")
dot.edge("API", "NOTIF", label="alerts")

dot.attr(label="Smart Plug ESP32-S3 — Functional Architecture & Safety Boundaries\nREV_A_PROVISIONAL — NOT A WIRING DIAGRAM — NOT APPROVED FOR FABRICATION", labelloc="t", fontsize="14", fontcolor="#14213d")

base = OUT / "SYSTEM_ARCHITECTURE"
dot.render(filename=str(base), cleanup=True)
# Graphviz package renders the requested format (png); also render svg and pdf.
for fmt in ("svg", "pdf"):
    dot.format = fmt
    dot.render(filename=str(base), cleanup=True)
print(f"Rendered {base}.png/.svg/.pdf")
print("WARNING: architecture diagram is illustrative; see KiCad/wiring for interfaces.")
