#!/usr/bin/env python3
"""localize-found-golf.py — pull the Found Golf candidates local. 20 Sept 2026.

Eighteen candidates for Lenny to cut: twelve apparel, six from the art and
design side. Everything is downloaded and served from /images/found-golf/.
Nothing hot-links — see feedback_local_images.

WHY THESE TWELVE APPAREL PIECES AND NOT THE OTHER EIGHTEEN.
Three exclusions, each for a stated reason rather than taste:

  * ALL EIGHT DAD CAPS are sold out — every colourway, 0 of 1 available. The
    live TGI page currently ships the Olive one as a "pick", which is a link
    to something nobody can buy. They are a fact for the write-up, not a card.
  * TEE BOX | WHITE is sold out (0/5). Its grey twin is in stock and carries
    the same graphic.
  * BELL SLEEVE (white and striped) and SKIRT-MORE are womenswear-cut. House
    default is menswear and unisex — see feedback_menswear_focus. Worth
    raising with Lenny separately rather than silently dropping from a brand
    whose own lookbook runs both.

The six art pieces are a spread, not a ranking: the two Damien Wright
collaborations, two of the seven Darcy Vescio works, the bench she made with
Locki Humphrey, and Brustman's dartboard for a lower price point.

Idempotent — a file that already exists is left alone. Dry run by default.
"""
import io, pathlib, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "images/found-golf"
CDN = "https://cdn.shopify.com/s/files/1/0758/8524/8814/files/"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) TGI-image-fetch"}
SQUARE = 1200

# slug, remote filename, label, AUD, availability
APPAREL = [
    ("box-par-tee",   "MG_7440.jpg",                                                   "Box Par Tee",              118, "3 of 6 sizes"),
    ("daisy-chain-tee", "MG_7429.jpg",                                                 "Daisy Chain Tee",          118, "4 of 6 sizes"),
    ("tee-box-grey",  "FOUND_T-Shirt_Grey_Front_5566ccfa-c431-4fb6-8665-f94ad42208b4.jpg", "Tee Box | Grey",       85,  "3 of 5 sizes"),
    ("shiz-knit",     "FOUND_TheShizKnit_Front_HR.jpg",                                "The Shiz Knit",            265, "2 of 5 sizes"),
    ("shiz-vest",     "Found-Pull-Over-Front.1_37fdb068-e811-4c16-adc3-e0f7d13b8607.jpg", "The Shiz Vest",         200, "4 of 6 sizes"),
    ("box-crew",      "Black-sweater-front-Large_df90a838-68b9-47a7-bb4b-2c89e4edb124.jpg", "Box Crew | Black",    165, "4 of 6 sizes"),
    ("quarter-zip",   "MG_7489.jpg",                                                   "1/4 Zip",                  190, "4 of 6 sizes"),
    ("windcheater",   "MG_7457.jpg",                                                   "Collared Windcheater",     260, "3 of 6 sizes"),
    ("knitted-polo",  "MG_7526_6c1abb71-2c37-4d9c-8362-5bc0dd476240.jpg",              "Long Sleeve Knitted Polo", 265, "3 of 5 sizes"),
    ("pleated-pants", "MG_7539_f5ccd2c8-88d6-4838-bfc2-b204f1e0c44c.jpg",              "Pleated Pants | Black",    198, "5 of 7 sizes"),
    ("the-slacker",   "FOUND_Tourser_Front_86064162-ed02-4e90-87e6-d90aedf47300.jpg",  "The Slacker | Navy",       198, "4 of 6 sizes"),
    ("short-game",    "FOUND_Shorts_Front_b3bbc25f-c04e-4229-9e54-f868a5e80ceb.jpg",   "Short Game | Black",       135, "3 of 5 sizes"),
]

ART = [
    ("art-country-club",   "DW-x-TB-Close.jpg",                    "Damien Wright &amp; Tony Birch &mdash; Country-club",        16000, "available"),
    ("art-symbolic",       "UPTHERE_MDW_Installation_070.jpg",     "Damien Wright &amp; Bonhula Yunupingu &mdash; Symbolic Capitalist", 1000, "available"),
    ("art-losers",         "Darcy-Vescio-Losers_1f66e636-7fff-4018-a578-5c01a8f0c55d.jpg", "Darcy Vescio &mdash; Losers",        650,  "available"),
    ("art-lip-service",    "Darcy_LipService.01.jpg",              "Darcy Vescio &mdash; Lip Service",                          1400, "available"),
    ("art-break-point",    "UPTHERE_MDW_Installation_033.jpg",     "Darcy Vescio &amp; Locki Humphrey &mdash; Break Point Bench", 5990, "available"),
    ("art-dartboard",      "UPTHERE_MDW_Installation_079.jpg",     "Danielle Brustman &mdash; HOT/NOT Dartboard",                750,  "available"),
]

ALL = [(s, f, l, p, a, "apparel") for s, f, l, p, a in APPAREL] + \
      [(s, f, l, p, a, "art") for s, f, l, p, a in ART]


def main(apply_):
    from PIL import Image
    if apply_:
        OUT.mkdir(parents=True, exist_ok=True)
    made, skipped, failed = [], [], []
    for slug, fname, label, price, avail, kind in ALL:
        dest = OUT / f"{slug}.jpg"
        if dest.exists():
            skipped.append(slug); continue
        if not apply_:
            made.append((slug, f"would fetch {fname[:46]}")); continue
        try:
            req = urllib.request.Request(CDN + fname, headers=UA)
            raw = urllib.request.urlopen(req, timeout=60).read()
            im = Image.open(io.BytesIO(raw)).convert("RGB")
            s = min(im.size)
            cx, cy = (im.width - s) // 2, min(im.height - s, round(im.height * 0.06))
            im = im.crop((cx, cy, cx + s, cy + s)).resize((SQUARE, SQUARE), Image.LANCZOS)
            im.save(dest, "JPEG", quality=88, optimize=True)
            made.append((slug, f"{im.size[0]}x{im.size[1]}"))
        except Exception as e:
            failed.append((slug, str(e)[:80]))

    for n, d in made:    print(f"  ok    {n:20} {d}")
    for n in skipped:    print(f"  skip  {n:20} already local")
    for n, e in failed:  print(f"  FAIL  {n:20} {e}")
    if failed:
        sys.exit(f"\n! {len(failed)} failed — do NOT build a grid with holes in it")
    if apply_:
        want = {s for s, *_ in ALL}
        have = {p.stem for p in OUT.glob("*.jpg")}
        missing = want - have
        if missing:
            sys.exit(f"\n! missing: {sorted(missing)}")
        print(f"\n  {len(want)} candidates local in images/found-golf/")
    else:
        print("\n  dry run — pass --apply")


if __name__ == "__main__":
    main("--apply" in sys.argv)
