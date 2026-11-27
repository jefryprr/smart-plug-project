from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
QR = ROOT / "hardware" / "pcb" / "qr"
render = Image.open(QR / "carrier_top.png").convert("RGBA")
label = Image.open(QR / "pcb_label_22mm.png").convert("RGBA")

# Board bounding box from the opaque render.
alpha = render.getchannel("A")
bbox = alpha.getbbox()
if bbox is None:
    raise SystemExit("empty render")
left, top, right, bottom = bbox
W, H = right - left, bottom - top
print("bbox", bbox, "size", W, H)

# Board is 100 x 70 mm. Label rectangle x=14..36, y=36..58 mm.
lw = round(W * 22 / 100)
lh = round(H * 22 / 70)
x = left + round(W * 14 / 100)
y = top + round(H * 36 / 70)
label = label.resize((lw, lh), Image.LANCZOS)
render.alpha_composite(label, (x, y))

d = ImageDraw.Draw(render)
d.rectangle([x, y, x + lw, y + lh], outline=(255, 0, 0, 255), width=max(2, W // 300))
# small annotation
d.text((x, max(0, y - 22)), "QR 22x22 mm", fill=(255, 0, 0, 255))

out = QR / "carrier_top_with_qr.png"
render.save(out)
print("wrote", out)
