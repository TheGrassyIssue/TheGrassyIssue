#!/usr/bin/env python3
"""apply-publication.py — centre the type on recent posts so they read like a publication.
26 September 2026. Lenny: "center all the text on all the recent posts so it
reads more like a publication" (first asked about the DTC category text).

Adds one CSS block (/*TGI-PUB-V1*/) before the LAST </style> of each page, so
it wins over the templates' own rules, several of which repeat inside <body>.
Nothing in the markup changes. Headings, tags, section decks, tier bands,
prose, pull-quotes, captions, product cards and the FAQ all centre. The opening
Take + details box keeps the house two-column layout (Lenny, 27 Sep). Nav, footer and the More strip are
untouched.

Runs on every deploy (Deploy TGI.command), so a rebuilt page keeps it.
Idempotent: an existing block is replaced. Dry run by default; --apply to write.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
PAGES = [
    "drops/curating-your-golf-bag-setup.html",
    "drops/brand-to-know-aug-11.html",
    "drops/8-best-practice-facilities-around-austin.html",
    "drops/enron-golf-collection.html",
    "drops/brand-to-know-no-return-club.html",
    "drops/limited-edition-golf-balls.html",
    "drops/rangefinder-cases-and-pouches.html",
    "drops/golf-ferrules-guide.html",
    "drops/brand-to-know-palm-golf-co.html",
    "drops/brand-to-know-magpie-supply.html",
    "drops/austin-golf-weekend.html",
    "drops/brand-to-know-ashworth.html",
    "drops/brand-to-know-puttwell.html",
    "drops/brand-to-know-shoal-golf.html",
    "drops/golf-bag-accessories-what-to-hang-from-your-bag.html",
    "drops/which-golfer-are-you.html",
    "drops/brand-to-know-local-gc.html",
    "drops/fella-golf.html",
    "drops/brand-to-know-clamp-golf-company.html",
    "drops/best-chicken-sandwiches-in-austin.html",
    "drops/brand-to-know-macade.html",
    "drops/brand-to-know-hudson-sutler.html",
    "drops/best-steakhouses-in-austin.html",
    "drops/required-reading-independent-golf-magazines.html",
    "drops/brand-to-know-st-andre.html",
    "drops/brand-to-know-dimple-divot.html",
    "drops/sugarloaf-autumn-layers-2026.html",
    "drops/austin-food-truck-field-guide.html",
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

CSS = """/*TGI-PUB-V2*/
/* The Take + details box stays as the house two-column opener (Lenny, 27 Sep:
   "TGI take on the left and the box on the right, then the rest of the write
   up"). Everything after it is centred. */
section.products:not([data-btk="take"]) .drop-tag{display:table!important;margin-left:auto!important;margin-right:auto!important}
section.products:not([data-btk="take"]) h2,section.products:not([data-btk="take"]) .products-hdr{text-align:center!important;margin-left:auto!important;margin-right:auto!important}
section.products:not([data-btk="take"]) .cat-kicker,section.products:not([data-btk="take"]) .sec-intro{text-align:center!important;border-left:0!important;padding-left:0!important;margin-left:auto!important;margin-right:auto!important;max-width:720px!important}
section.products:not([data-btk="take"]) .writeup-body{max-width:720px!important;margin-left:auto!important;margin-right:auto!important;text-align:center!important}
.products~.writeup{display:block!important}
.products~.writeup .writeup-body{max-width:720px!important;margin-left:auto!important;margin-right:auto!important;text-align:center!important}
.products~.writeup .writeup-body h2,.products~.writeup .writeup-body .products-hdr{text-align:center!important}
/* The details box: label left, answer right, one clean row each (27 Sep: "format the box text a little better"). */
.sidebar-card .sidebar-detail{display:grid!important;grid-template-columns:max-content 1fr;column-gap:18px;align-items:baseline;margin:0!important;padding:11px 0;border-top:.5px solid rgba(20,20,20,.14)}
.sidebar-card .sidebar-label+.sidebar-detail{border-top:0;padding-top:4px}
.sidebar-card .sidebar-detail .l{white-space:nowrap;line-height:1.4}
.sidebar-card .sidebar-detail>span:last-child{text-align:right;font-size:14px;line-height:1.4;font-family:var(--serif)}
.sidebar-card .sidebar-label{margin-bottom:10px!important}
.sidebar-card .sidebar-cta{margin-top:22px}
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
/*/TGI-PUB-V2*/"""

BLOCK = re.compile(r"/\*TGI-PUB-V\d\*/.*?/\*/TGI-PUB-V\d\*/\n?", re.S)


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
