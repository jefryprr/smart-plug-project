import fitz
import zxingcpp
from PIL import Image
import io
import numpy as np

URL = "https://github.com/jefryprr/smart-plug-project/blob/main/hardware/schematic/SYSTEM_SCHEMATIC.pdf"
pdf = fitz.open('hardware/pcb/qr/pcb_label_22mm.pdf')
page = pdf[0]
ok_all = True
for dpi in (600, 400, 300, 240, 200, 160):
    pix = page.get_pixmap(dpi=dpi, alpha=False)
    img = Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')
    for rot in (0, 90, 180, 270):
        a = img.rotate(-rot, expand=True)
        results = zxingcpp.read_barcodes(a)
        texts = [r.text for r in results]
        ok = URL in texts
        print(f"dpi={dpi:4} px={img.width:4}x{img.height:<4} rot={rot:3} {'PASS' if ok else 'FAIL'}")
        ok_all &= ok
print("RESULT", "PASS" if ok_all else "FAIL")
