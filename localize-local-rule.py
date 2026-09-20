#!/usr/bin/env python3
"""localize-local-rule.py — pull the Local Rule candidates local. 20 Sept 2026.

Eighteen candidates for Lenny to cut, plus lifestyle frames and a hero.
Everything is downloaded and served from /images/local-rule/. Nothing hot-links.

WHY THESE EIGHTEEN, AND WHAT IS DELIBERATELY NOT HERE.

  * EVERY PICK IS IN STOCK. 20 of Local Rule's 123 products are fully sold out,
    and they are the NEWEST ones — the Irons Coach Jacket, all four Ripstop
    Headcovers. A sample of the first page of products.json reads like a dead
    store; it isn't. 91 live non-archive pieces. Sold-out items are a fact for
    the write-up, not a card.

  * NO 'generated-image-*' FRAMES. Three Lightweight Tech Polo colourways (Gray,
    Light Blue, Blue) carry images named generated-image-1-<epoch> at 1024x1024
    and 502x627 — the signatures of AI generation. That is an INFERENCE from
    filenames and sizes and is published nowhere. But we do not need to build a
    grid on them: the Light Brown colourway of the same polo uses ordinary
    product photography, so that is the one in the shortlist.

  * ARCHIVE EXCLUDED. 14 products sit in a product_type of 'Archive' (past
    season). Gift cards excluded too.

Prices are SEK. The store's home market is Sweden; country=US returns a
converted figure at a constant ~9.6x, which is not a price Local Rule set.

Idempotent — a file that already exists is left alone. Dry run by default.
"""
import io, pathlib, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "images/local-rule"
CDN = "https://cdn.shopify.com/s/files/1/0915/5841/2569/files/"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) TGI-image-fetch"}
SQUARE = 1200
WIDE = (1600, 685)          # house hero size, 2.34:1

# slug, remote filename, label, SEK, availability
PICKS = [
    ("tech-polo-light-brown", "LocalRuleLightweightTechPoloLightBrown6.jpg?v=1770723584",
     "Lightweight Tech Polo | Light Brown", 699, "7 of 7 sizes"),
    ("knit-polo-offwhite", "Local_Rule_Knit_Polo_White_02.jpg?v=1771936876",
     "Knit Polo | Off-White", 1199, "6 of 6 sizes"),
    ("performance-polo-green", "Local_Rule_Performance_Polo_Green_01.jpg?v=1771935681",
     "Performance Polo | Dark Green", 799, "5 of 6 sizes"),
    ("ls-performance-polo-navy", "Local_Rule_Performance_Polo_Navy_LS_01.jpg?v=1771936172",
     "Long-Sleeve Performance Polo | Dark Navy", 899, "6 of 6 sizes"),
    ("football-jersey-navy", "Football_Jersey_Local_Rule_Navy.jpg?v=1779119725",
     "Football Jersey | Striped Navy", 999, "5 of 7 sizes"),
    ("qzip-fleece-light-blue", "LocalRuleQ-zipFleeceSweatshirtLightBlue4.jpg?v=1771424312",
     "Q-zip Fleece Sweatshirt | Light Blue", 1099, "6 of 6 sizes"),
    ("fleece-pullover-blue", "Local_Rule_Fleece_Pullover_Blue_front.jpg?v=1771857229",
     "Fleece Pullover | Blue", 1299, "6 of 6 sizes"),
    ("pleated-trousers-offwhite", "LocalRulePleatedTrouserWhitefront.jpg?v=1771877892",
     "Pleated Trousers | Offwhite", 1499, "4 of 12 sizes"),
    ("tech-pants-light-grey", "LocalRuleLightweightTechPantsLightGreyTaperedstart.jpg?v=1770733528",
     "Lightweight Tech Pants | Light Grey", 899, "11 of 12 sizes"),
    ("shibuya-shorts-navy", "Local_Rule_Shibuya_Shorts__Navy_front.jpg?v=1771426347",
     "Shibuya Shorts | Dark Navy", 1199, "3 of 6 sizes"),
    ("tech-shorts-olive", "Local_Rule_Lightweight_Tech_Shorts__olivegreen_front.jpg?v=1774457749",
     "Tech Shorts | Dusty Olive", 699, "5 of 6 sizes"),
    ("tech-vest-light-green", "LocalRuleTechVestSeagrassGreen11.jpg?v=1770807260",
     "Tech Vest | Light Green", 1499, "3 of 6 sizes"),
    ("tech-anorak-navy", "Local_Rule_Tech_Anorak_Navy_front.jpg?v=1771420148",
     "Tech Anorak | Navy", 1299, "1 of 6 sizes"),
    ("wool-cap-burgundy", "WoolCapBurgundy_c3bfc8b6-8130-4048-9ac2-335f6d1d78e9.jpg?v=1785846144",
     "Wool Cap | Burgundy", 499, "in stock"),
    ("buckethat-military-green", "LocalRuleBuckethatMilitaryGreen2.jpg?v=1741017077",
     "Buckethat | Military Green", 599, "in stock"),
    ("pom-pom-beanie-navy", "PomPomNavy.jpg?v=1779274214",
     "Pom Pom Beanie | Navy", 599, "in stock"),
    ("leather-belt-black", "LeatherBelt-Black_2.jpg?v=1757585299",
     "Leather Belt | Black", 599, "in stock"),
    ("lclrl-towel-green", "LCLRLTowelGreen.jpg?v=1763649539",
     "LCLRL Towel | Dark Green", 399, "in stock"),
]

# Real photography, on people and on courses — for the In the Wild band.
LIFESTYLE = [
    ("life-collegekids-1", "LR_collegekids_lores_8.jpg?v=1785769474"),
    ("life-collegekids-2", "LR_collegekids_lores41.jpg?v=1785054213"),
    ("life-pompom-course", "Local_Rule_Pompom_Beanie_Red_course3.jpg?v=1771514621"),
    ("life-cotton-cap-course", "LocalRule_CottonCap_Yellow_Course.jpg?v=1771955480"),
    ("life-towel-city", "Local_Rule_towel_LCLRL_bag_city.jpg?v=1771953895"),
    # A packshot on white among five real photographs read as the odd one out in
    # the In the Wild band. LR_collegekids_lores27 is a third frame from the same
    # shoot as the other two, so the band is now six genuine photographs.
    ("life-collegekids-3", "LR_collegekids_lores27.jpg?v=1785054213"),
]

HERO_SRC = "L1091827.jpg?v=1779833217"


def fetch(fname):
    req = urllib.request.Request(CDN + fname, headers=UA)
    return urllib.request.urlopen(req, timeout=60).read()


def main(apply_):
    from PIL import Image
    if apply_:
        OUT.mkdir(parents=True, exist_ok=True)
    made, skipped, failed = [], [], []

    jobs = [(s, f, "square") for s, f, *_ in PICKS] + \
           [(s, f, "square") for s, f in LIFESTYLE] + \
           [("hero", HERO_SRC, "wide")]

    for slug, fname, kind in jobs:
        dest = OUT / f"{slug}.jpg"
        if dest.exists():
            skipped.append(slug); continue
        if not apply_:
            made.append((slug, f"would fetch {fname[:46]}")); continue
        try:
            im = Image.open(io.BytesIO(fetch(fname))).convert("RGB")
            if kind == "square":
                s = min(im.size)
                cx = (im.width - s) // 2
                cy = min(im.height - s, round(im.height * 0.04))
                im = im.crop((cx, cy, cx + s, cy + s)).resize((SQUARE, SQUARE), Image.LANCZOS)
            else:
                tw, th = WIDE
                scale = max(tw / im.width, th / im.height)
                im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
                cx = (im.width - tw) // 2
                cy = min(im.height - th, round(im.height * 0.18))
                im = im.crop((cx, cy, cx + tw, cy + th))
            im.save(dest, "JPEG", quality=88, optimize=True)
            made.append((slug, f"{im.size[0]}x{im.size[1]}"))
        except Exception as e:
            failed.append((slug, str(e)[:80]))

    for n, d in made:    print(f"  ok    {n:26} {d}")
    for n in skipped:    print(f"  skip  {n:26} already local")
    for n, e in failed:  print(f"  FAIL  {n:26} {e}")
    if failed:
        sys.exit(f"\n! {len(failed)} failed — do NOT build a grid with holes in it")
    if apply_:
        want = {s for s, *_ in jobs}
        have = {p.stem for p in OUT.glob("*.jpg")}
        missing = want - have
        if missing:
            sys.exit(f"\n! missing: {sorted(missing)}")
        print(f"\n  {len(want)} images local in images/local-rule/ "
              f"({len(PICKS)} picks, {len(LIFESTYLE)} lifestyle, 1 hero)")
    else:
        print("\n  dry run — pass --apply")


if __name__ == "__main__":
    main("--apply" in sys.argv)
