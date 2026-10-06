#!/usr/bin/env python3
"""swipe-merrill-metalwood.py — swipeable product galleries on the Merrill Golf and Metalwood Studio
Brand to Know pages. 5 October 2026. Lenny: "we need the merrill golf and the metalwood pages to have
swipeable images on the product shots".

Sources: research/swipe-mm/fetch.json (each brand's own store images; Merrill adds the other colourways
of the same product; four retired Metalwood products use their V1-V3 store images). Products with one
store photo get a close-up detail crop of that photo as frame 2. Instagram collab cards stay single.
Frames: 1000x1250, light backgrounds multiplied onto the TGI gradient. Idempotent; --apply to write.
"""
import json, re, sys, pathlib
import numpy as np
from PIL import Image
ROOT = pathlib.Path(__file__).resolve().parent
R = json.load(open(ROOT / "research/swipe-mm/fetch.json"))
PAGES = {"merrill": ("drops/brand-to-know-merrill-golf.html", "images/merrill-golf/sw"),
         "metalwood": ("drops/brand-to-know-metalwood-studio.html", "images/metalwood/sw")}
DONOR = ROOT / "drops/brand-to-know-metalwood-studio.html"
W, H = 1000, 1250
TOP, BOT = np.array((242, 238, 230), float), np.array((228, 222, 210), float)
GRAD = (TOP * (1 - np.linspace(0, 1, H)[:, None, None]) + BOT * np.linspace(0, 1, H)[:, None, None]).repeat(W, 1)

def edge_light(im):
    a = np.asarray(im.resize((200, max(1, int(200 * im.height / im.width))))).astype(int)
    b = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    return ((b.min(axis=1) >= 228).mean() > 0.9 and b.std(axis=0).max() < 10), tuple(int(c) for c in np.median(b, axis=0))

def frame(im):
    im = im.convert("RGB"); light, col = edge_light(im); w, h = im.size; r = W / H
    if light:
        t = im.copy(); t.thumbnail((int(W * .9), int(H * .9)), Image.LANCZOS)
        bg = Image.new("RGB", (W, H), col); bg.paste(t, ((W - t.width) // 2, (H - t.height) // 2))
        a = np.asarray(bg).astype(float)
        return Image.fromarray((a * GRAD / np.maximum(np.array(col, float), 1)).clip(0, 255).astype(np.uint8))
    if w / h > r: nw = int(h * r); x = (w - nw) // 2; im = im.crop((x, 0, x + nw, h))
    else: nh = int(w / r); y = int((h - nh) * .35); im = im.crop((0, y, w, y + nh))
    return im.resize((W, H), Image.LANCZOS)

def detail(im):
    """Close-up of the product: the upper-middle of its bounding box, 4:5."""
    im = im.convert("RGB"); light, col = edge_light(im)
    a = np.asarray(im).astype(int); diff = np.abs(a - np.array(col)).max(axis=2) > 25
    ys, xs = np.where(diff)
    if len(xs) == 0: return None
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    bw = (x1 - x0) * .55; bh = bw * H / W
    cx = (x0 + x1) / 2; cy = y0 + (y1 - y0) * .38
    bx0 = max(0, int(cx - bw / 2)); by0 = max(0, int(cy - bh / 2))
    c = im.crop((bx0, by0, min(im.width, int(bx0 + bw)), min(im.height, int(by0 + bh))))
    c = c.resize((W, H), Image.LANCZOS)
    if light:
        a = np.asarray(c).astype(float)
        return Image.fromarray((a * GRAD / np.maximum(np.array(col, float), 1)).clip(0, 255).astype(np.uint8))
    return c

def gallery(fr, label):
    n = len(fr)
    imgs = "".join(f'<div class="pg-frame"><img src="/{f}" alt="{label} &middot; view {j+1} of {n}" loading="lazy" /></div>' for j, f in enumerate(fr))
    if n == 1:
        return f'<div class="product-gallery"><div class="pg-track">{imgs}</div></div>'
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>' for j in range(n))
    return (f'<div class="product-gallery"><div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>')

def main(apply_):
    d = DONOR.read_text()
    a = d.index('.product-card{position:relative}'); b = d.index('@media(max-width:900px){.pg-arw{opacity:.85}}') + len('@media(max-width:900px){.pg-arw{opacity:.85}}')
    CSS = d[a:b]
    JS = [m.group(0) for m in re.finditer(r'<script[^>]*>.*?</script>', d, re.S) if 'pg-track' in m.group(0)][0]
    for key, (page, outdir) in PAGES.items():
        P = ROOT / page; s = P.read_text(); (ROOT / outdir).mkdir(parents=True, exist_ok=True)
        rows = {r["n"]: r for r in R if r["page"] == key}
        cards = list(re.finditer(r'<div class="product-card"[^>]*>(.*?)(?=<div class="product-body">)', s, re.S))
        out, last, tot = [], 0, 0
        for n, m in enumerate(cards, 1):
            r = rows.get(n, {}); inner = m.group(1)
            old = re.findall(r'src="(/[^"]+)"', inner)
            alt = re.findall(r'alt="([^"]*?)(?: &middot; view \d+ of \d+)?"', inner)
            label = (alt[0] if alt else "").replace('"', "")
            srcs = [ROOT / f for f in r.get("imgs", []) and [("research/swipe-mm/" + x) for x in r["imgs"]]]
            if not srcs and old: srcs = [ROOT / old[0].lstrip("/")]
            fr = []
            if "instagram.com" in r.get("url", "") and old:
                fr = [old[0].lstrip("/")]
            else:
                for j, src in enumerate(srcs[:5]):
                    fn = f"{outdir}/{key}-{n:02d}-{j+1}.jpg"
                    if apply_: frame(Image.open(src)).save(ROOT / fn, quality=85, optimize=True, progressive=True)
                    fr.append(fn)
                if len(fr) == 1:
                    fn = f"{outdir}/{key}-{n:02d}-2.jpg"
                    if apply_:
                        dimg = detail(Image.open(srcs[0]))
                        if dimg is not None: dimg.save(ROOT / fn, quality=85, optimize=True, progressive=True); fr.append(fn)
                    else: fr.append(fn)
            tot += len(fr)
            open_tag = re.sub(r'\s*data-frames="\d+"', "", s[m.start():m.start(1)])
            open_tag = open_tag.replace('class="product-card"', f'class="product-card" data-frames="{len(fr)}"', 1)
            out.append(s[last:m.start()] + open_tag + "\n      " + gallery(fr, label) + "\n      "); last = m.end(1)
        s = "".join(out) + s[last:]
        if '.pg-track{' not in s:
            s = s.replace("</style>", CSS + "\n</style>", 1)
        if "pg-track'" not in s and 'querySelector(\'.pg-track\')' not in s:
            s = s.replace("</body>", JS + "\n</body>", 1)
        print(f"  {page}: {len(cards)} cards, {tot} frames")
        if apply_: P.write_text(s)
    if not apply_: print("  dry run — pass --apply")

if __name__ == "__main__":
    main("--apply" in sys.argv)
