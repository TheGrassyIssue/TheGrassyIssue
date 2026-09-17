"""Localize Hidden Links Society imagery at house size. 17 September 2026.

HOUSE SPEC: product images 800x1000 (4:5). HLS shoots flat packshots on white,
so these PAD ON WHITE rather than centre-crop — cropping a hat to 4:5 would cut
the brim. (Centre-crop is for dark-background photography; see Gamut's sticks.)

NEVER HOT-LINK. Every frame is downloaded and served from /images/hls/.
"""
import urllib.request, json, os, io
from PIL import Image

SKUS = json.load(open("/tmp/hls_clean.json", encoding="utf-8"))
OUT = "images/hls"
os.makedirs(OUT, exist_ok=True)
W, H = 800, 1000
ok = fail = 0
report = []
for key, d in SKUS.items():
    for i, u in enumerate(d["imgs"][:4], 1):
        dest = f"{OUT}/{key}-{i}.jpg"
        if os.path.exists(dest):
            ok += 1; continue
        try:
            r = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
            raw = urllib.request.urlopen(r, timeout=40).read()
            im = Image.open(io.BytesIO(raw)).convert("RGBA")
            bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
            bg.alpha_composite(im)
            im = bg.convert("RGB")
            im.thumbnail((W, H), Image.LANCZOS)
            canvas = Image.new("RGB", (W, H), "white")
            canvas.paste(im, ((W - im.width) // 2, (H - im.height) // 2))
            canvas.save(dest, quality=88, optimize=True)
            ok += 1
        except Exception as e:
            fail += 1; report.append(f"{key}-{i}: {e}")
print(f"localized {ok} frames, {fail} failed")
for r in report: print("  !!", r)
