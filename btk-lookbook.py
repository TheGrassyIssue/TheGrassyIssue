#!/usr/bin/env python3
"""
btk-lookbook.py — the in-body photographs for a Brand to Know page.
18 September 2026.

WHY THIS EXISTS
---------------
Hiroki carries three lookbook photographs between its sections. The other 40
Brand to Know pages carry none, so the redesigned format would run type and
product with nothing to break it up. Lenny: "source imagery first, then apply."

WHAT WENT WRONG LAST TIME, AND THE RULE THAT COMES OUT OF IT
-------------------------------------------------------------
The first Hiroki crops forced 21:9 bands out of portrait frames. One of them
cut the golfer's cap and the driver head off against the edges, which is what
"cropped a little off" meant. The originals had already been overwritten, so
fixing it needed a fresh download from the brand's CDN.

Two rules follow, and they are the whole design of this file:

  1. SHAPE FIRST. A frame is only a candidate for a band if cropping it does
     not throw away most of its height. Squeezing a 3:4 portrait into a 16:9
     band discards 76% of the frame, and whatever was at the top of it goes
     first — which on a photograph of a person is their head. Frames are scored
     on how close they already are to the target, and a portrait is used only
     when nothing better exists, where it is FLAGGED rather than trusted.

  2. NEVER CROP IN PLACE. Every original is archived to
     research/btk/originals/<slug>/ before anything is written. Re-cropping
     should never require asking the brand's CDN for the file a second time.

WHAT IT DOES NOT DO
-------------------
It does not decide the picture is good. There is no face detection available
here, and an energy profile cannot tell a flattering frame from an awkward one.
So every run writes a contact sheet to outputs/ and the crops are looked at
before any page is rebuilt. The script narrows 20 frames to 3 candidates; a
person still says yes.

PACKSHOTS ARE REFUSED. Borrowed from lifestyle-slides.py: a near-white border
all the way round means a product on a sweep, and a packshot does not become
editorial photography by being cropped wide.

USAGE
    python3 btk-lookbook.py --list                 # what imagery exists
    python3 btk-lookbook.py seamus fyfe-golf       # dry run, contact sheet only
    python3 btk-lookbook.py --all --apply
"""
import json, pathlib, re, sys, urllib.request
from PIL import Image, ImageStat, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent
MANIFESTS = ROOT / "research" / "lifestyle"
ORIGINALS = ROOT / "research" / "btk" / "originals"
OUT = pathlib.Path("/sessions/admiring-pensive-ritchie/mnt/outputs")

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36"}

# One 21:9 band at the top of the page, two 16:9 bands inside it. 21:9 is the
# house hero; 16:9 is used in the body because it discards far less of the
# frame and is therefore much harder to decapitate somebody with.
# Lenny: "let's always separate each section with an image." So the number of
# bands is not fixed — it is however many section joins the page has. The first
# is the 21:9 masthead band; the rest are 16:9, which discards far less of a
# frame and is much harder to decapitate somebody with.
#
# A brand with more section joins than photographs gets as many as it has and
# is reported short. Repeating a photograph to fill a gap would be the same
# mistake as the repeated headline on the lifestyle carousels: it looks like
# the page is padded, because it is.
def bands_for(n):
    return [("hero", 21 / 9)] + [(f"body-{i}", 16 / 9) for i in range(1, n)]


BANDS = bands_for(3)
TARGET_W = 1800
NATIVE = "--native" in sys.argv   # body bands keep the shape they were shot in
MIN_SRC_W = 1400           # below this a 1800px band is an upscale


def is_packshot(im):
    """A near-white border all the way round means a product on a sweep."""
    w, h = im.size
    band = max(2, min(w, h) // 25)
    edges = [im.crop((0, 0, w, band)), im.crop((0, h - band, w, h)),
             im.crop((0, 0, band, h)), im.crop((w - band, 0, w, h))]
    return sum(ImageStat.Stat(e.convert("L")).mean[0] for e in edges) / 4 > 225


def shape_cost(src_ratio, target_ratio):
    """Fraction of the frame thrown away to reach the target shape. 0 is a
    frame already the right shape; 0.76 is a 3:4 portrait forced into 16:9."""
    if src_ratio >= target_ratio:
        return 1 - (target_ratio / src_ratio)      # cropping the sides
    return 1 - (src_ratio / target_ratio)          # cropping top and bottom


def energy_rows(im, n=64):
    """Coarse vertical profile of detail. Used to place the band over the part
    of the frame that has something in it rather than over empty sky or grass."""
    g = im.convert("L").resize((48, n), Image.BILINEAR)
    px = g.load()
    out = []
    for y in range(n):
        row = [px[x, y] for x in range(48)]
        out.append(sum(abs(row[i] - row[i - 1]) for i in range(1, 48)))
    return out


def best_top(im, crop_h):
    """Where to start the crop vertically.

    Two pulls, deliberately balanced: put the band where the detail is, but
    bias upward, because in a photograph of a person the head is above the
    centre of mass and the head is the thing you must not cut."""
    H = im.height
    if crop_h >= H:
        return 0
    prof = energy_rows(im)
    n = len(prof)
    scale = H / n
    best, best_score = 0, -1
    for top in range(0, H - crop_h + 1, max(1, (H - crop_h) // 40)):
        a, b = int(top / scale), int((top + crop_h) / scale)
        e = sum(prof[a:b]) / max(1, b - a)
        # the bias: prefer bands that sit high in the frame, gently
        lift = 1.0 - 0.25 * (top / max(1, H - crop_h))
        s = e * lift
        if s > best_score:
            best, best_score = top, s
    return best


def crop_band(im, ratio):
    W, H = im.size
    ch = int(W / ratio)
    if ch <= H:
        top = best_top(im, ch)
        return im.crop((0, top, W, top + ch))
    cw = int(H * ratio)                      # frame wider than the band
    x = (W - cw) // 2
    return im.crop((x, 0, x + cw, H))


def fetch(url, dest):
    if dest.exists():
        return dest
    try:
        data = urllib.request.urlopen(
            urllib.request.Request(url, headers=UA), timeout=60).read()
        if len(data) < 40000:
            return None
        dest.write_bytes(data)
        return dest
    except Exception:
        return None


def candidates(slug):
    """Frames for this brand, best-first, already downloaded and archived."""
    man = MANIFESTS / f"{slug}.json"
    if not man.exists():
        alt = [p for p in MANIFESTS.glob("*.json")
               if p.stem in slug or slug in p.stem]
        if not alt:
            return []
        man = alt[0]
    d = json.loads(man.read_text(encoding="utf-8"))
    arch = ORIGINALS / slug
    arch.mkdir(parents=True, exist_ok=True)

    out = []
    for url, w, h in d.get("imgs", []):
        if w < MIN_SRC_W:
            continue
        name = re.sub(r"[^A-Za-z0-9._-]", "_", url.rsplit("/", 1)[-1].split("?")[0])
        p = fetch(url, arch / name)
        if not p:
            continue
        try:
            with Image.open(p) as im:
                size = im.size
                if is_packshot(im.convert("RGB")):
                    continue
        except Exception:
            continue
        out.append((p, size))
    return out


def pick(frames, ratio, used):
    """Cheapest frame by shape that has not been used for another band."""
    scored = []
    for p, (w, h) in frames:
        if p in used:
            continue
        c = shape_cost(w / h, ratio)
        # resolution is a tiebreak, not a driver
        scored.append((c - 0.00002 * min(w, 4000), p, (w, h)))
    scored.sort(key=lambda x: x[0])
    return scored[0] if scored else None


def do_brand(slug, apply_=False, want=3):
    frames = candidates(slug)
    if not frames:
        return {"slug": slug, "status": "no frames", "bands": []}
    used, made = set(), []
    for name, ratio in bands_for(want):
        got = pick(frames, ratio, used)
        if not got:
            break
        cost, p, (w, h) = got
        used.add(p)
        with Image.open(p) as src:
            src = src.convert("RGB")
            if NATIVE and name != "hero":
                # Lenny: "formatted how they are provided so either landscape or
                # portrait." Cropping every body frame to one ratio is what threw
                # that away — a portrait shot became a letterbox and a wide one
                # got cropped twice. In native mode the body bands are resized
                # and nothing else; only the masthead is still cut to 21:9.
                sw = min(1600, src.width)
                band = src.resize((sw, round(src.height * sw / src.width)),
                                  Image.LANCZOS)
            else:
                band = crop_band(src, ratio).resize(
                    (TARGET_W, int(TARGET_W / ratio)), Image.LANCZOS)
        risky = shape_cost(w / h, ratio) > 0.45
        made.append({"band": name, "src": p.name, "risky": risky,
                     "cost": round(shape_cost(w / h, ratio), 2),
                     "thumb": band.resize((520, round(band.height*520/band.width)), Image.LANCZOS)})
        if apply_:
            d = ROOT / "images" / slug
            d.mkdir(parents=True, exist_ok=True)
            band.save(d / f"btk-{name}.jpg", "JPEG", quality=90, optimize=True)
        del band
    return {"slug": slug, "status": "ok" if len(made) >= want else
            f"short {len(made)}/{want}", "bands": made}


def contact_sheet(results, path):
    rows = [(r["slug"], b) for r in results for b in r["bands"]]
    if not rows:
        return
    W, TH = 520, 300
    sheet = Image.new("RGB", (W + 20, len(rows) * TH + 20), (242, 240, 233))
    d = ImageDraw.Draw(sheet)
    y = 10
    for slug, b in rows:
        th = b["thumb"]
        sheet.paste(th, (10, y))
        d.text((14, y + th.height + 4),
               f"{slug}  {b['band']}  {'<-- SHAPE RISK' if b['risky'] else ''}",
               fill=(20, 20, 20))
        y += TH
    sheet.crop((0, 0, W + 20, y)).save(path)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    apply_ = "--apply" in sys.argv
    if "--list" in sys.argv:
        for p in sorted(MANIFESTS.glob("*.json")):
            d = json.loads(p.read_text())
            print(f"  {p.stem:<24} {len(d.get('imgs', [])):>3} frames")
        raise SystemExit
    import json as _j
    need = {}
    try:
        for r in _j.loads(pathlib.Path("/tmp/btk-survey.json").read_text()):
            need[r["slug"]] = r["grids"] + 3        # one per product category + take/story/coda
    except Exception:
        pass
    slugs = args or [p.stem for p in sorted(MANIFESTS.glob("*.json"))]
    results = []
    for s in slugs:
        w = need.get(s) or next((v for k, v in need.items() if k in s or s in k), 3)
        r = do_brand(s, apply_, want=w)
        results.append(r)
        flag = sum(1 for b in r["bands"] if b["risky"])
        print(f"  {s:<24} {r['status']:<10} {len(r['bands'])} band(s)"
              + (f"   {flag} flagged for shape" if flag else ""))
    OUT.mkdir(parents=True, exist_ok=True)
    contact_sheet(results, OUT / "btk-lookbook-contact.png")
    print(f"\n  contact sheet -> btk-lookbook-contact.png"
          + ("" if apply_ else "   (dry run — pass --apply to write)"))
