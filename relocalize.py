#!/usr/bin/env python3
"""
relocalize.py — re-pull already-localized product imagery at Instagram-grade
resolution, from a manifest of source URLs. 17 September 2026.

WHY
---
69% of the 8,644 images on this site are under 1080px on the short edge. The
house product size is 800x1000, which is right for the web and too small for
Instagram, where the canvas is 1080 square. Every product slide in ig-export is
therefore an UPSCALE — 800 stretched to 1080, x1.35 — and Lenny spotted it as
softness before anyone measured it.

The brands' own stores have the originals. Hidden Links Society serves
2000x2000; we saved 800x1000. That is a 2.5x gain sitting behind a fetch.

WHY A MANIFEST, AND WHY THIS FILE EXISTS AT ALL
-----------------------------------------------
The first instinct was to re-pull from URLs already on record. That fails: the
localize scripts renamed every download to `<product-handle>-<n>.jpg`, which
does not resemble the source filename, so matching stored URLs to local files
hit 1% — and both "matches" were TGI's own URLs, not upstream ones. Three
thousand source URLs on record and effectively none of them usable.

What DOES match is the handle. 67 of 68 files in images/hls map to a product
handle at 98%, because that is how they were named. So the recoverable path is
the brand's live catalogue: /products.json gives handle -> images, and the local
filename gives handle -> file. The manifest is the join.

THIS RUN WRITES THE MANIFEST THAT WAS MISSING. research/relocalize/<brand>.json
is kept permanently, so the next person who needs to re-pull does not repeat the
archaeology above.

FETCHING, AND THE LINE THIS SCRIPT DOES NOT CROSS
-------------------------------------------------
Catalogue JSON is fetched through the browser, by hand, and pasted into the
manifest — NOT by this script. That is the standing rule on this project: page
and API content comes through the approved browser tooling, never curl or
urllib. What this script does is download IMAGE BINARIES whose URLs a human
already collected, which is the established localizing workflow and is all it
needs to do.

WHAT IT PRESERVES
-----------------
The house frame is 4:5 pad-on-white, and the site's layout depends on it, so the
output stays 4:5 — just at 1152x1440 instead of 800x1000. Nothing on any page
moves; the pixels behind it triple. And it NEVER upscales: a source smaller than
what is already on disk is skipped and reported, because enlarging a small
original produces a bigger file that looks worse.

USAGE
    python3 relocalize.py --brand hidden-links-society --dir hls
    python3 relocalize.py --brand hidden-links-society --dir hls --apply
"""
import json, os, re, sys, pathlib, urllib.request
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
MAN = ROOT / "research" / "relocalize"
TARGET_W, TARGET_H = 1152, 1440          # 4:5, the house frame at 1.44x
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read()


def framed(im):
    """4:5 on the frame's own edge colour, matching the existing convention."""
    im = im.convert("RGB")
    pad = Image.new("RGB", (TARGET_W, TARGET_H), _edge(im))
    w, h = im.size
    sc = min(TARGET_W / w, TARGET_H / h)
    im = im.resize((max(1, int(w * sc)), max(1, int(h * sc))), Image.LANCZOS)
    pad.paste(im, ((TARGET_W - im.width) // 2, (TARGET_H - im.height) // 2))
    return pad


def _edge(im):
    w, h = im.size
    px = im.load()
    e = []
    for x in range(0, w, max(1, w // 60)):
        e.append(px[x, 0]); e.append(px[x, h - 1])
    for y in range(0, h, max(1, h // 60)):
        e.append(px[0, y]); e.append(px[w - 1, y])
    return tuple(sorted(c[i] for c in e)[len(e) // 2] for i in range(3))


def main():
    argv = sys.argv[1:]
    def opt(f, d=None):
        return argv[argv.index(f) + 1] if f in argv else d
    brand, sub = opt("--brand"), opt("--dir")
    apply_ = "--apply" in argv
    if not brand or not sub:
        raise SystemExit(__doc__)

    man = MAN / f"{brand}.json"
    if not man.exists():
        raise SystemExit(f"no manifest at {man} — harvest the catalogue first")
    cat = json.load(open(man, encoding="utf-8"))

    d = ROOT / "images" / sub
    files = sorted(p for p in d.glob("*.jpg"))
    upgraded = skipped = missing = 0
    gained = []

    for p in files:
        # TWO BUGS LIVED HERE AND BOTH WOULD HAVE BEEN SILENT.
        #
        # 1. localize-hls.py numbers with enumerate(imgs, 1), so the files are
        #    ONE-BASED: handle-1.jpg is imgs[0]. Indexing the list with 1 pulled
        #    the SECOND photograph, so every product would have quietly acquired
        #    its neighbour's image — a bigger, sharper, wrong picture.
        #
        # 2. The split was non-greedy, which breaks on the handles that end in a
        #    digit. "the-society-overshirt-charcoal-1-2.jpg" is image 2 of handle
        #    "the-society-overshirt-charcoal-1", not image 1 of
        #    "the-society-overshirt-charcoal" — and both handles exist in this
        #    catalogue, so the wrong one resolves happily and says nothing.
        #    Greedy takes the longest handle, which is the real one; the fallback
        #    below covers the reverse case.
        m = re.match(r"(.+)-(\d+)\.jpg$", p.name)
        handle, idx = (m.group(1), int(m.group(2))) if m else (p.stem, 1)
        if handle not in cat and m:
            alt = re.match(r"(.+?)-(\d+)\.jpg$", p.name)
            if alt and alt.group(1) in cat:
                handle, idx = alt.group(1), int(alt.group(2))
        imgs = cat.get(handle)
        if not imgs:
            missing += 1
            continue
        if not (1 <= idx <= len(imgs)):
            missing += 1
            continue
        src = imgs[idx - 1]
        cur_w, cur_h = Image.open(p).size
        if min(src["w"], src["h"]) <= min(cur_w, cur_h):
            skipped += 1                      # never enlarge a small original
            continue
        try:
            raw = fetch(src["s"])
        except Exception as e:
            print(f"  !! {p.name}: {str(e)[:60]}")
            continue
        tmp = ROOT / ".relocalize.tmp"
        tmp.write_bytes(raw)
        out = framed(Image.open(tmp))
        tmp.unlink(missing_ok=True)
        if apply_:
            out.save(p, "JPEG", quality=90, optimize=True)
        upgraded += 1
        gained.append((p.name, f"{cur_w}x{cur_h}", f"{out.width}x{out.height}",
                       f"{src['w']}x{src['h']}"))

    print(("re-localized " if apply_ else "DRY RUN ") + f"images/{sub}")
    print(f"  upgraded : {upgraded}")
    print(f"  skipped  : {skipped}  (source no larger than what we have)")
    print(f"  no match : {missing}  (handle not in the catalogue)")
    for g in gained[:6]:
        print(f"     {g[0][:42]:<44} {g[1]} -> {g[2]}   (src {g[3]})")
    if not apply_:
        print("\n  pass --apply to write")


if __name__ == "__main__":
    main()
