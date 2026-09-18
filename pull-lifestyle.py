#!/usr/bin/env python3
"""
pull-lifestyle.py — download the CAMPAIGN photography, not the packshots.
17 September 2026.

WHY THIS IS SEPARATE FROM relocalize.py
---------------------------------------
Lenny: "I want to pull more promotional images that are less product only."

Every localize script this project has ever run reads /products.json, which by
definition returns product photography — a garment on white, lit flat, shot to
show the garment. Stack twenty of those in a grid and it looks like a catalogue,
which is exactly what the Instagram looked like.

The campaign work is somewhere else entirely, and this was the finding that made
the job possible: on Manors it is on their CMS, not their store. Their Sanity
bucket holds frames at 6336x9504 — editorial photography at full resolution —
while the Shopify side of the same homepage serves 723x904 packshots. Four times
the resolution and a completely different kind of picture, and no script had ever
looked at it because no script had reason to leave /products.json.

WHERE EACH BRAND KEEPS IT — checked, not assumed
------------------------------------------------
    Manors              cdn.sanity.io           12 frames, to 6336x9504
    Fyfe Golf           Shopify CDN              5 frames, to 2047x1365
                        named for the courses: Bute, Elie, Jura, North Berwick
    Hidden Links        Shopify CDN              1 frame, 5000x3000
    Birds of Condor     Shopify CDN              1 frame — SEE THE NOTE

BIRDS OF CONDOR CAME UP THIN AND THAT IS REPORTED, NOT PAPERED OVER. Their store
homepage is packshots at 2000x2500 and the only true lifestyle frame on it is a
collection header. Their editorial work is on Instagram, which is not a source
this project pulls from. If that brand needs more, it needs a human decision
about where to get it, not a cleverer scraper.

SHOPIFY SERVES VARIANTS. A URL in the DOM is usually a resized copy — _512x, or
whatever the theme asked for. Stripping that suffix and appending ?width=5000
returns the original, which is how the Fyfe frames went from 512px in the page
to 2047px on disk.

OUTPUT
    ~/Desktop/TheGrassyIssue/ig-lifestyle/<brand>/
Its own folder, per Lenny. Nothing here is wired into the site yet — these are
raw frames for choosing from, not a published change.

USAGE
    python3 pull-lifestyle.py            # dry run
    python3 pull-lifestyle.py --apply
"""
import json, os, sys, pathlib, urllib.request
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
MAN = ROOT / "research" / "lifestyle"
OUT = ROOT.parent / "ig-lifestyle"
MAXPX = 2400                     # plenty for a 1080 slide; keeps the folder sane
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}


def fetch(url):
    if "cdn.shopify.com" in url or "/cdn/shop/" in url:
        url += ("&" if "?" in url else "?") + "width=5000"
    elif "cdn.sanity.io" in url:
        url += ("&" if "?" in url else "?") + "w=2400&q=90&auto=format"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def main():
    apply_ = "--apply" in sys.argv
    tmp = ROOT / ".lifestyle.tmp"
    got = skipped = 0
    rows = []

    for man in sorted(MAN.glob("*.json")):
        d = json.load(open(man, encoding="utf-8"))
        slug = man.stem
        dest = OUT / slug
        if apply_:
            dest.mkdir(parents=True, exist_ok=True)
        for i, (url, w, h) in enumerate(d["imgs"], 1):
            name = f"{i:02d}-{slug}.jpg"
            try:
                raw = fetch(url)
            except Exception as e:
                print(f"  !! {slug} {i}: {str(e)[:60]}")
                continue
            tmp.write_bytes(raw)
            try:
                im = Image.open(tmp).convert("RGB")
            except Exception as e:
                print(f"  !! {slug} {i}: not an image ({str(e)[:40]})")
                continue
            if min(im.size) < 1080:
                skipped += 1
                print(f"  -- {name}: {im.width}x{im.height} is under 1080, skipped")
                continue
            if max(im.size) > MAXPX:
                r = MAXPX / max(im.size)
                im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
            if apply_:
                im.save(dest / name, "JPEG", quality=92, optimize=True)
            got += 1
            rows.append((d["brand"], name, f"{w}x{h}", f"{im.width}x{im.height}"))
    tmp.unlink(missing_ok=True)

    print(("pulled " if apply_ else "DRY RUN ") + f"-> {OUT}")
    print(f"  frames: {got}   under-size skips: {skipped}")
    for b, n, native, saved in rows:
        print(f"    {b[:20]:<22} {n[:34]:<36} native {native:<11} saved {saved}")
    for man in sorted(MAN.glob("*.json")):
        d = json.load(open(man, encoding="utf-8"))
        if d.get("note"):
            print(f"\n  NOTE — {d['brand']}: {d['note']}")
    if not apply_:
        print("\n  pass --apply to write")


if __name__ == "__main__":
    main()
