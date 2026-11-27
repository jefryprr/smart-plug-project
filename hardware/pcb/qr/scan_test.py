#!/usr/bin/env python3
"""Scan-test the PCB QR label at several sizes and rotations."""
from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
LABEL = ROOT / "hardware" / "pcb" / "qr" / "pcb_label_22mm.png"
QR = ROOT / "hardware" / "pcb" / "qr" / "schematic_qr.png"
URL = "https://github.com/jefryprr/smart-plug-project/blob/main/hardware/schematic/SYSTEM_SCHEMATIC.pdf"

det = cv2.QRCodeDetector()


def decode(img: np.ndarray):
    data, points, _ = det.detectAndDecode(img)
    return data, points is not None


def test(path: Path, label: str, min_dpi: int = 160):
    base = Image.open(path).convert("RGB")
    print(f"\n== {label} {base.size} ==")
    ok_all = True
    for dpi in (1200, 800, 600, 400, 300, 240, 200, 160):
        if dpi < min_dpi:
            continue
        w = max(1, round(base.width * dpi / 1200))
        h = max(1, round(base.height * dpi / 1200))
        img = base.resize((w, h), Image.LANCZOS)
        arr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        for rot in (0, 90, 180, 270):
            a = np.rot90(arr, k=rot // 90).copy()
            data, found = decode(a)
            ok = found and data == URL
            if not ok:
                ok_all = False
                print(f"  dpi={dpi:4} px={w:4}x{h:<4} rot={rot:3} FAIL found={found} data={data[:60]!r}")
            else:
                print(f"  dpi={dpi:4} px={w:4}x{h:<4} rot={rot:3} PASS")
    return ok_all


def main():
    ok1 = test(LABEL, "complete label", min_dpi=200)
    ok2 = test(QR, "QR only (reference)", min_dpi=240)
    print("\nRESULT", "PASS" if ok1 and ok2 else "FAIL")
    if not (ok1 and ok2):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
