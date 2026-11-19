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
    mains.node("TB1", "PSU TB1\n230 VAC input", fillcolor="#ffd6d1")
    mains.node("F1", "PSU F1 10 A\n+ MOV / TCO", fillcolor="#ffd6d1")
    mains.node("TB2", "PSU TB2\n230 VAC output", fillcolor="#ffd6d1")
    mains.node("K1", "2-ch opto relay module\n8 A final, off-board", fillcolor="#ffd6d1")
    mains.node("X1", "Socket Type F\n16 A class TBD", fillcolor="#ffd6d1")

with dot.subgraph(name="cluster_barrier") as barrier:
    barrier.attr(label="ISOLATION BARRIER (UNVERIFIED)", style="rounded,dashed", color="#9a5b00", bgcolor="#fff4df", fontcolor="#9a5b00")
    barrier.node("PS1", "PSU HLK-5M05\n5 V 1 A, 5 W\n+ PTC / TVS", fillcolor="#ffe8b8")
    barrier.node("PZEMISO", "PZEM-004T V4\ninternal optocouplers\n(no ADuM/B0505S)", fillcolor="#ffe8b8")

with dot.subgraph(name="cluster_selv") as selv:
    selv.attr(label="DOMAIN C — SELV 5 V / 3.3 V", style="rounded", color="#067647", bgcolor="#e6f6ee", fontcolor="#067647")
    selv.node("PSU5", "PSU 5 V outputs\nJ5 carrier / J6 relay / J7 PZEM", fillcolor="#c9f2dd")
    selv.node("U1", "ESP32-S3\nDevKitC-1 N16R8", fillcolor="#c9f2dd")
    selv.node("CARR", "Low-voltage carrier\nGPIO / I2C / UART", fillcolor="#c9f2dd")
    selv.node("UI", "OLED + button\n+ RGB", fillcolor="#c9f2dd")
    selv.node("RTC", "DS3231 RTC\n(no temperature sensor)", fillcolor="#c9f2dd")
    selv.node("LS", "74HCT125\n+ 10k/20k divider", fillcolor="#c9f2dd")
    selv.node("DRV", "Relay driver\nAO3400 + pulldown", fillcolor="#c9f2dd")

with dot.subgraph(name="cluster_cloud") as cloud:
    cloud.attr(label="DOMAIN D — NETWORK / SOFTWARE", style="rounded", color="#175cd3", bgcolor="#e8f1ff", fontcolor="#175cd3")
    cloud.node("MQTT", "MQTT broker\nTLS / ACL", fillcolor="#cfe0ff")
    cloud.node("API", "Backend API\nFastify + SQLite/PG", fillcolor="#cfe0ff")
    cloud.node("WEB", "Next.js dashboard", fillcolor="#cfe0ff")
    cloud.node("APP", "Android Expo app", fillcolor="#cfe0ff")
    cloud.node("NOTIF", "Telegram / push\n(provider mock)", fillcolor="#cfe0ff")

dot.edge("P1", "TB1", label="L / N")
dot.edge("TB1", "F1", label="L -> fuse/MOV/TCO")
dot.edge("F1", "TB2", label="L_LOAD")
dot.edge("TB2", "K1", label="L / N")
dot.edge("K1", "X1", label="L / N")
dot.edge("P1", "X1", label="PE continuous\n(no relay/fuse)", style="bold", color="#067647")
dot.edge("F1", "PS1", label="AC L/N")
dot.edge("PS1", "PSU5", label="+5 V / PTC / TVS")
dot.edge("PSU5", "CARR", label="J5 +5 V")
dot.edge("PSU5", "K1", label="J6 +5 V", style="dashed")
dot.edge("PSU5", "PZEMISO", label="J7 +5 V (conditional)", style="dashed", color="#9a5b00")
dot.edge("P1", "PZEMISO", label="PZEM voltage/CT\n(mains side)", style="dashed", color="#9a5b00")
dot.edge("PZEMISO", "LS", label="TTL 5 V", style="dashed", color="#9a5b00")
dot.edge("LS", "CARR", label="3.3 V UART", style="dashed", color="#9a5b00")
dot.edge("CARR", "U1", label="3.3 V / GPIO")
dot.edge("CARR", "UI", label="I2C / GPIO")
dot.edge("U1", "TIME", label="time service")
dot.edge("U1", "DRV", label="RELAY_CTRL")
dot.edge("DRV", "K1", label="active-LOW inputs\n(SELV)", style="dashed")
dot.edge("U1", "MQTT", label="Wi-Fi")
dot.edge("MQTT", "API", label="telemetry / ACK")
dot.edge("API", "WEB", label="REST / WS")
dot.edge("API", "APP", label="REST")
dot.edge("API", "NOTIF", label="alerts")

dot.attr(label="Smart Plug ESP32-S3 — Functional Architecture & Safety Boundaries\nREV_D_CORE_ONLY — SEPARATE PSU BOARD — PZEM INTERNAL ISOLATION — NOT APPROVED FOR FABRICATION", labelloc="t", fontsize="14", fontcolor="#14213d")

base = OUT / "SYSTEM_ARCHITECTURE"
dot.render(filename=str(base), cleanup=True)
# Graphviz package renders the requested format (png); also render svg and pdf.
for fmt in ("svg", "pdf"):
    dot.format = fmt
    dot.render(filename=str(base), cleanup=True)
print(f"Rendered {base}.png/.svg/.pdf")
print("WARNING: architecture diagram is illustrative; see KiCad/wiring for interfaces.")
