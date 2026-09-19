#!/usr/bin/env python3
"""
localize-bold-tees.py — pull every Bold Tee Edit product image local. 19 Sept 2026.

HOUSE RULE: we never hot-link a brand's CDN. Their URL can rotate, expire or be
re-pointed at a different colourway, and a roundup whose images silently become
someone else's product is worse than one with no images.

GATE ON max(width, height), NOT width. An earlier localizer checked width only
and let two portrait files through at 2048 and 1999 pixels tall. Same bug class
here: several of these are 4053px square (Goat Hill) or 3600px tall.

Idempotent: a file already present at the right size is left alone, so a rerun
touches nothing and the build stays byte-stable.
"""
import json, pathlib, sys, urllib.request
from io import BytesIO
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
SPEC = ROOT / "research/bold-tees.json"
OUTD = ROOT / "images/bold-tees"
MAXPX = 1400          # house cap on the long edge for product cards
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}


def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()


def save(raw, dest):
    im = Image.open(BytesIO(raw))
    if im.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGB", im.size, (255, 255, 255))
        im = im.convert("RGBA")
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")
    if max(im.size) > MAXPX:                       # max(), not width
        r = MAXPX / max(im.size)
        im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    im.save(dest, "JPEG", quality=88, optimize=True)
    return im.size


def main(apply_):
    spec = json.loads(SPEC.read_text(encoding="utf-8"))
    jobs = []
    for key, pref in (("muni", "m"), ("weight", "w"), ("art", "a")):
        for r in spec[key]:
            jobs.append((f"{pref}-{r[0]}.jpg", r[6], r[1]))

    if apply_:
        OUTD.mkdir(parents=True, exist_ok=True)
    got = fail = skip = 0
    for name, url, brand in jobs:
        dest = OUTD / name
        if dest.exists():
            print(f"  skip  {name}"); skip += 1; continue
        if not apply_:
            print(f"  would fetch {name}  <- {brand}"); continue
        try:
            sz = save(fetch(url), dest)
            print(f"  ok    {name}  {sz[0]}x{sz[1]}"); got += 1
        except Exception as e:
            print(f"  FAIL  {name}  {type(e).__name__}: {e}"); fail += 1

    print(f"\n  fetched {got}, skipped {skip}, failed {fail}")
    if apply_:
        # GUARD: every row must have a file, every file must be real, and no two
        # rows may share a file. The last one matters because a copy-paste in the
        # spec would otherwise show the same shirt twice under two brand names.
        missing = [n for n, _, _ in jobs if not (OUTD / n).exists()]
        digests = {}
        import hashlib
        for n, _, _ in jobs:
            p = OUTD / n
            if p.exists():
                digests.setdefault(hashlib.sha256(p.read_bytes()).hexdigest(), []).append(n)
        dupes = [v for v in digests.values() if len(v) > 1]
        big = [n for n, _, _ in jobs if (OUTD / n).exists()
               and max(Image.open(OUTD / n).size) > MAXPX]
        for label, bad in (("every row has a local file", missing),
                           ("no two rows share an image", dupes),
                           ("nothing exceeds the size cap", big)):
            print(f"  {'OK  ' if not bad else 'FAIL'} {label} {bad if bad else ''}")
        if missing or dupes or big:
            sys.exit("! localisation incomplete")


if __name__ == "__main__":
    main("--apply" in sys.argv)
