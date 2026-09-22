#!/usr/bin/env python3
"""localize-needlepoint.py — imagery for the needlepoint belt roundup.
22 September 2026.

Lenny: "I want to do a round up on Needlepoint belts, classic golf accessory
that looks great one & off the course", then "feature the ric flair at the one
spot on the homepage, then 3 of your choices + a key fob".

EIGHTEEN BELTS FROM SIX MAKERS, PLUS THREE KEY FOBS. Multiple pieces per maker
is a deliberate exception to the no-repeat-brands rule agreed with Lenny:
needlepoint is a small field and the pattern IS the product, so one belt per
maker would have capped the post at six cards.

MINIMUM SOURCE WIDTH 500px, AND THAT IS NOT A STYLE PREFERENCE. The Ric Flair
belt's first image is 300x168 while every other frame in its set is 1148x643.
Taking images[0] blindly — which is what the selection grid did first — put a
postage stamp on the card and made a good belt look like a mistake. Baldwin and
Charleston have the same pattern: a small legacy thumbnail sitting at index 0.
Anything under 500px wide is dropped before frames are chosen.

PRICES AND STOCK come from research/needlepoint/items.json, which read them from
each storefront's collection listing on 22 September 2026, USD. Stock is NOT
taken from a per-product .json: J.Press's reported 0/6 available on belts whose
product pages show InStock with live add-to-cart, and Lenny caught me repeating
that claim after I had written the rule down.

Idempotent. Dry run by default.
"""
import io
import json
import pathlib
import re
import sys
import time
import urllib.request

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
RES = ROOT / "research/needlepoint"
OUT = ROOT / "images/needlepoint"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}
MINW, FRAME_W, FRAMES = 500, 1100, 4

# EVERY ITEM IN THE APPROVED GRID. Lenny: "we have all 18 belts in the dedicated
# page plus the key fobs?" — yes. The lineup is not a hand-picked subset any
# more, it is research/needlepoint/items.json in full, which is exactly what he
# reviewed and approved in the carousel preview. Deriving the list from the same
# file he looked at removes the chance of the post and the preview disagreeing.
#
# That puts Charleston Belt at five of the eighteen, over the two-to-three per
# maker we had agreed. Lenny's later instruction supersedes it; the ratio is a
# consequence of him wanting the whole grid, not drift.
def slugify(brand, title):
    s = f"{brand}-{title}".lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return re.sub(r"-(needlepoint|belt|hand-stitched|key-fob)\b", "", s)[:46].strip("-")


def fetch(u, raw=False):
    r = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=45).read()
    return r if raw else json.loads(r)


def main(apply_):
    items = json.loads((RES / "items.json").read_text(encoding="utf-8"))

    manifest, bad = {}, []
    seen_slug = set()
    for it in items:
        slug = slugify(it["brand"], it["title"])
        if slug in seen_slug:
            bad.append(f"duplicate slug {slug!r} — two products would overwrite each other")
            continue
        seen_slug.add(slug)
        try:
            p = fetch(it["url"] + ".json")["product"]
        except Exception as e:
            bad.append(f"{slug}: {type(e).__name__} fetching product")
            continue
        usable = [i for i in p.get("images", []) if (i.get("width") or 0) >= MINW]
        if not usable:
            bad.append(f"{slug}: no frame >= {MINW}px (had {len(p.get('images', []))})")
            continue
        got = []
        for k, im in enumerate(usable[:FRAMES]):
            f = OUT / f"{slug}-{k}.jpg"
            if not f.is_file():
                g = Image.open(io.BytesIO(fetch(im["src"], raw=True))).convert("RGB")
                w0, h0 = g.size
                tw = min(FRAME_W, w0)                     # never upscale
                g = g.resize((tw, round(h0 * tw / w0)), Image.LANCZOS)
                if apply_:
                    OUT.mkdir(parents=True, exist_ok=True)
                    g.save(f, "JPEG", quality=88, optimize=True, progressive=True)
            got.append(f"/images/needlepoint/{f.name}")
        manifest[slug] = dict(brand=it["brand"], title=it["title"], price=it["price"],
                              stock=it["stock"], url=it["url"], frames=got,
                              kind=it["kind"])
        print(f"  {slug:<20}{it['brand'][:17]:<19}{len(got)} frames  "
              f"(source had {len(p.get('images', []))}, {len(usable)} over {MINW}px)")
        time.sleep(0.8)

    if bad:
        sys.exit("! " + "\n    ".join(bad))
    if not apply_:
        print("\n  dry run — pass --apply")
        return

    # ---- VERIFY WHAT IS ON DISK ----
    probs = []
    for slug, m in manifest.items():
        for rel in m["frames"]:
            f = ROOT / rel.lstrip("/")
            if not f.is_file():
                probs.append(f"{rel}: missing"); continue
            im = Image.open(f)
            if im.width < 400:
                probs.append(f"{rel}: only {im.width}px wide")
            if f.stat().st_size > 900_000:
                probs.append(f"{rel}: {f.stat().st_size/1024:.0f} KB")
    # no two products may share a frame — that silently shows the wrong belt
    seen = {}
    for slug, m in manifest.items():
        for rel in m["frames"]:
            if rel in seen:
                probs.append(f"{rel} used by both {seen[rel]} and {slug}")
            seen[rel] = slug
    if probs:
        sys.exit("! " + "\n    ".join(probs))

    (RES / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    belts = sum(1 for m in manifest.values() if m["kind"] == "belt")
    print(f"\n  verified: {len(seen)} frames on disk, none shared, none upscaled\n"
          f"  {belts} belts + {len(manifest)-belts} key fobs -> research/needlepoint/manifest.json")


if __name__ == "__main__":
    main("--apply" in sys.argv)
