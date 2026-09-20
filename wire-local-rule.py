#!/usr/bin/env python3
"""wire-local-rule.py — homepage feed card, slideTexts, sitemap. 20 Sept 2026.

Three separate jobs, each idempotent and each verified against the finished
file rather than against its own return value:

  1. the homepage carousel card, inserted as the newest card in the feed
  2. the matching entry in the big __slideTexts object near the foot of index.html
  3. sitemap entries for the drop page and the brand page

PRICES ARE SEK. Local Rule's home market is Sweden and the dollar figure Shopify
serves to a US requester is an auto-conversion at a constant ~9.6x, not a price
the brand set. The card says kr, like the page does.

Dry run by default. Run with --apply.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
SITEMAP = ROOT / "sitemap.xml"
KEY = "localrule1"
SLUG = "brand-to-know-local-rule"

# slide: handle, image slug, name, SEK, alt
SLIDES = [
    ("tech-polo-light-brown", "tech-polo-light-brown",
     "Lightweight Tech Polo — Light Brown", 699,
     "Local Rule Lightweight Tech Polo in light brown"),
    ("knit-polo-offwhite", "knit-polo-offwhite",
     "Knit Polo — Off-White", 1199,
     "Local Rule Knit Polo in off-white with a tipped collar"),
    ("pleated-trousers-offwhite", "pleated-trousers-offwhite",
     "Pleated Trousers — Offwhite", 1499,
     "Local Rule Pleated Trousers in offwhite"),
    ("football-jersey-striped-navy", "football-jersey-navy",
     "Football Jersey — Striped Navy", 999,
     "Local Rule Football Jersey in striped navy with a crest"),
    ("lclrl-towel", "lclrl-towel-green",
     "LCLRL Towel — Dark Green", 399,
     "Local Rule LCLRL towel in dark green"),
]

# LITERAL CHARACTERS, NOT HTML ENTITIES.
# These strings end up inside a JS array and are written to the DOM with
# textContent, which does not decode entities — so "&mdash;" renders as the
# five characters &mdash; on the homepage card. Caught by looking at the
# rendered card, not the markup. The slide NAMES above are different: they are
# written as HTML, so entities are correct there.
TEXTS = [
    "Lightweight Tech Polo — the piece Local Rule is known for, and the cheapest "
    "way into a Stockholm label that reads as Swedish sportswear rather than pro-shop "
    "stock. Polyester-elastane with mesh ribbing, an extended sleeve and a split hem. "
    "699 kr.",
    "Knit Polo — knitted rather than jersey, with a tipped collar, and the dressed-up "
    "end of a range that mostly refuses to shout. The brand's first season was chinos, "
    "polos, shorts and caps, described by Swedish trade press as a clear flirtation with "
    "vintage golf. This is that, refined. 1,199 kr.",
    "Pleated Trousers — the vintage flirtation made literal, and the top of the "
    "range. Twelve waist-and-length combinations, four of them live, which is what a brand "
    "that deliberately makes short runs looks like from the outside. 1,499 kr.",
    "Football Jersey — a pinstriped football shirt with a crest, sitting in a golf "
    "catalogue without explanation or apology. Local Rule is named for the sheet a club "
    "prints to sanction its own exceptions, so this tracks. 999 kr.",
    "LCLRL Towel — the wordmark repeated across the whole cloth in the green the "
    "brand keeps returning to. Towels start at 279 kr, which is where a catalogue of "
    "ninety-one live pieces lets you in. 399 kr.",
]


def card_html():
    slides = "\n".join(f'''          <div class="gear-slide">
            <a href="https://local-rule.com/products/{h}" target="_blank" rel="noopener">
              <img src="/images/local-rule/{img}.jpg" alt="{alt}" loading="lazy" />
              <div class="gear-slide-info"><div class="gear-slide-brand">Local Rule</div><div class="gear-slide-name">{name} &middot; {sek:,} kr</div></div>
            </a>
          </div>''' for h, img, name, sek, alt in SLIDES)
    return f'''<!-- BRAND TO KNOW — LOCAL RULE -->
  <div class="card" data-type="drop">
    <div class="card-media" style="position:relative;">
      <span class="card-tag grass">[Drops &amp; Brands]</span>
      <div class="gear-carousel" data-carousel="{KEY}">
        <div class="gear-carousel-track">
{slides}
        </div>
        <button class="gear-arrow prev" onclick="gearSlide(this, -1)">&#8249;</button>
        <button class="gear-arrow next" onclick="gearSlide(this, 1)">&#8250;</button>
      </div>
    </div>
    <div class="card-body">
      <div class="card-title"><a href="/drops/{SLUG}" style="color:inherit;text-decoration:none;border-bottom:none;">Brand to Know — Local Rule</a></div>
      <div class="card-text" data-slidetext="{KEY}">{TEXTS[0]}</div>
      <div class="gear-dots" data-dots="{KEY}"></div>
      <div class="gear-counter" data-counter="{KEY}">1 / {len(SLIDES)}</div>
      <!-- no .card-source line: Lenny cut the local-rule.com text link.
           The slides already link to the store, and See the Full Post carries the post. -->
      <a href="/drops/{SLUG}" class="card-readmore" style="display:inline-block;margin-top:12px;font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:0.12em;text-transform:uppercase;border-bottom:1px solid var(--ink);padding-bottom:2px;">See the Full Post &rarr;</a>
    </div>
  </div>
'''


def wire_index(h):
    changed = []
    # 1. the card, inserted as the newest card in the feed
    if f'data-carousel="{KEY}"' in h:
        changed.append("card already present")
    else:
        anchor = "<!--TGI-SC-HOME-->"
        if anchor not in h:
            sys.exit("! feed anchor <!--TGI-SC-HOME--> not found in index.html")
        h = h.replace(anchor, anchor + "\n" + card_html(), 1)
        changed.append("card inserted")

    # 2. the slideTexts entry, added to the object that already holds the others
    if re.search(rf"^\s*{KEY}:\s*\[", h, re.M):
        changed.append("slideTexts already present")
    else:
        m = re.search(r"^(\s*)foundgolf:\s*\[", h, re.M)
        if not m:
            sys.exit("! could not find the slideTexts object to extend")
        ind = m.group(1)
        body = "".join(f'{ind}        "{t}",\n' for t in TEXTS)
        block = f"{ind}{KEY}: [\n{body}{ind}      ],\n\n"
        h = h[:m.start()] + block + h[m.start():]
        changed.append("slideTexts inserted")
    return h, changed


def wire_sitemap(x):
    changed = []
    for loc, pri in [(f"https://thegrassyissue.com/drops/{SLUG}", "0.7"),
                     ("https://thegrassyissue.com/brands/local-rule", "0.6")]:
        if loc in x:
            changed.append(f"sitemap has {loc.rsplit('/', 1)[-1]}")
            continue
        entry = (f"  <url>\n    <loc>{loc}</loc>\n"
                 f"    <lastmod>2026-09-20</lastmod>\n"
                 f"    <changefreq>monthly</changefreq>\n"
                 f"    <priority>{pri}</priority>\n  </url>\n")
        x = x.replace("</urlset>", entry + "</urlset>", 1)
        changed.append(f"sitemap + {loc.rsplit('/', 1)[-1]}")
    return x, changed


def main(apply_):
    h = INDEX.read_text(encoding="utf-8")
    x = SITEMAP.read_text(encoding="utf-8")
    h2, ic = wire_index(h)
    x2, sc = wire_sitemap(x)
    for c in ic + sc:
        print("  " + c)

    if apply_:
        INDEX.write_text(h2, encoding="utf-8")
        SITEMAP.write_text(x2, encoding="utf-8")

        # VERIFY THE FINISHED FILES, not the strings this function just built.
        # The recurring failure on this site is a guard that reads its own
        # return value and passes while the artifact on disk is wrong.
        hh = INDEX.read_text(encoding="utf-8")
        xx = SITEMAP.read_text(encoding="utf-8")
        bad = []
        if f'data-carousel="{KEY}"' not in hh: bad.append("card missing")
        if not re.search(rf"^\s*{KEY}:\s*\[", hh, re.M): bad.append("slideTexts missing")
        if hh.count(f'data-carousel="{KEY}"') != 1: bad.append("card duplicated")
        if hh.count(f"/drops/{SLUG}") < 2: bad.append("post links missing")
        # entities inside the JS slideTexts would render literally
        m = re.search(rf"^\s*{KEY}:\s*\[(.*?)^\s*\],", hh, re.M | re.S)
        if m and re.search(r"&(mdash|rsquo|amp|middot|ndash);", m.group(1)):
            bad.append("HTML entity inside the JS slideTexts — renders literally")
        n_slides = len(re.findall(r'<div class="gear-slide">',
                                  hh[hh.find(f'data-carousel="{KEY}"'):
                                     hh.find("</div>", hh.find(f'data-counter="{KEY}"'))]))
        if n_slides != len(SLIDES): bad.append(f"{n_slides} slides, expected {len(SLIDES)}")
        for img in (f"/images/local-rule/{s[1]}.jpg" for s in SLIDES):
            if not (ROOT / img.lstrip("/")).exists(): bad.append(f"missing image {img}")
        if f"/drops/{SLUG}</loc>" not in xx.replace("<loc>", ""): pass
        if SLUG not in xx: bad.append("sitemap drop entry missing")
        if bad:
            sys.exit("! " + "; ".join(bad))
        print(f"\n  verified on disk: 1 card, {n_slides} slides, slideTexts, sitemap")
    else:
        print("\n  dry run — pass --apply")


if __name__ == "__main__":
    main("--apply" in sys.argv)
