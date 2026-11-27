import fitz
import zxingcpp
from PIL import Image
import io

URL = "https://github.com/jefryprr/smart-plug-project/blob/main/hardware/schematic/SYSTEM_SCHEMATIC.pdf"
pdf = fitz.open('hardware/pcb/qr/pcb_label_22mm.pdf')
page = pdf[0]
for dpi in (600, 400, 350, 320, 300, 280, 260, 240, 220, 200, 180, 160):
    pix = page.get_pixmap(dpi=dpi, alpha=False)
    img = Image.open(io.BytesIO(pix.tobytes('png')))
    results = zxingcpp.read_barcodes(img)
    texts = [r.text for r in results]
    ok = URL in texts
    print(f"dpi={dpi:4} px={img.width:4}x{img.height:<4} {'PASS' if ok else 'FAIL'} {texts[:1]}")
