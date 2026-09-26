#!/usr/bin/env python3
"""apply-publication.py — centre the type on recent posts so they read like a publication.
26 September 2026. Lenny: "center all the text on all the recent posts so it
reads more like a publication" (first asked about the DTC category text).

Adds one CSS block (/*TGI-PUB-V1*/) before the LAST </style> of each page, so
it wins over the templates' own rules, several of which repeat inside <body>.
Nothing in the markup changes. Headings, tags, section decks, tier bands,
prose, pull-quotes, captions, product cards and the FAQ all centre; the Take's
details box drops below the Take instead of sitting to its right (centred type
beside a right-hand box reads as a mistake). Nav, footer and the More strip are
untouched.

Runs on every deploy (Deploy TGI.command), so a rebuilt page keeps it.
Idempotent: an existing block is replaced. Dry run by default; --apply to write.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
PAGES = [
    "drops/fall-golf-towel-roundup-2026.html",
    "drops/dtc-golf-club-brands.html",
    "drops/brand-to-know-sounder.html",
    "drops/fall-drops-eastside-students-devereux.html",
    "drops/brand-to-know-galvin-green.html",
    "drops/best-golf-pants-ranked.html",
    "drops/8-special-day-rounds-near-austin.html",
    "drops/upgrading-your-golf-bag.html",
    "drops/the-needlepoint-belt-report.html",
    "drops/brand-to-know-manors.html",
]
if "--only" in sys.argv:
    PAGES = [sys.argv[sys.argv.index("--only") + 1]]

CSS = """/*TGI-PUB-V1*/
main .drop-tag,section.products .drop-tag,section[data-btk] .drop-tag{display:table!important;margin-left:auto!important;margin-right:auto!important}
section.products h2,section.products .products-hdr,section[data-btk] .products-hdr{text-align:center!important;margin-left:auto!important;margin-right:auto!important}
.cat-kicker,section[data-btk] .cat-kicker,section[data-btk="take"] .cat-kicker,.sec-intro,section[data-btk="take"] .sec-intro{text-align:center!important;border-left:0!important;padding-left:0!important;margin-left:auto!important;margin-right:auto!important;max-width:720px!important}
section[data-btk="take"]{display:block!important}
section[data-btk="take"] .writeup-body,section.products .writeup-body{max-width:720px!important;margin-left:auto!important;margin-right:auto!important;text-align:center!important}
section[data-btk="take"] .products-hdr,section[data-btk="take"] .drop-tag{margin-left:auto!important;margin-right:auto!important}
section[data-btk="take"] .sidebar{position:static!important;max-width:520px!important;margin:40px auto 0!important}
.writeup{display:block!important}
.writeup .writeup-body{max-width:720px!important;margin-left:auto!important;margin-right:auto!important;text-align:center!important}
.writeup .writeup-body .products-hdr,.writeup .writeup-body h2{text-align:center!important;margin-left:auto!important;margin-right:auto!important}
.writeup .sidebar{position:static!important;max-width:520px!important;margin:40px auto 0!important}
section.products>div[style*="max-width:760px"]{margin-left:auto!important;margin-right:auto!important;text-align:center!important;max-width:720px!important}
.tier-band{text-align:center!important}
.tier-band h2.tier-title{text-align:center!important}
.tier-band .tier-brands{margin:0 9px 14px!important}
.tier-band p.tier-intro{margin:0 auto!important}
.pull-quote-inner{margin:0 auto!important;text-align:center!important}
.pull-quote-inner:before{display:none!important}
.pull-quote-attr{text-align:center!important;display:table!important;margin-left:auto!important;margin-right:auto!important}
.ig-cap{text-align:center!important}
.product-body{text-align:center!important}
.product-body .product-link{margin-left:auto;margin-right:auto}
.faq-q summary,.faq-q p{text-align:center!important}
.products-grid:has(>.product-card:nth-child(2):last-child){grid-template-columns:repeat(2,minmax(0,calc((100% - 48px)/3)))!important;justify-content:center}
.products-grid:has(>.product-card:only-child){grid-template-columns:minmax(0,calc((100% - 48px)/3))!important;justify-content:center}
@media(max-width:900px){.products-grid:has(>.product-card:nth-child(2):last-child),.products-grid:has(>.product-card:only-child){grid-template-columns:repeat(auto-fit,minmax(0,1fr))!important}}
.entry,.entry-body,.entry p{text-align:center}
/*/TGI-PUB-V1*/"""

BLOCK = re.compile(r"/\*TGI-PUB-V1\*/.*?/\*/TGI-PUB-V1\*/\n?", re.S)


def main(apply):
    n = 0
    for rel in PAGES:
        p = ROOT / rel
        if not p.is_file():
            print(f"  skip (missing) {rel}")
            continue
        s = p.read_text(encoding="utf-8")
        t = BLOCK.sub("", s)
        i = t.rfind("</style>")
        if i < 0:
            print(f"  skip (no <style>) {rel}")
            continue
        t = t[:i] + CSS + "\n" + t[i:]
        if t != s:
            n += 1
            if apply:
                p.write_text(t, encoding="utf-8")
    print(f"apply-publication: {n} page(s) {'updated' if apply else 'would change'}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
