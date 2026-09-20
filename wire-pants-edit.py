#!/usr/bin/env python3
"""wire-pants-edit.py — homepage card, slideTexts, sitemap, search. 20 Sept 2026.

Four jobs, each idempotent, each verified against the FINISHED FILE rather than
against its own return value. The recurring failure on this site is a guard
that reads the string it just built and passes while the artifact on disk is
wrong, so nothing here trusts its own output.

CAROUSEL SLIDES. Five, chosen to show five different silhouettes rather than
five versions of the same trouser: Malbon's military-green Station Pant,
Criquet's corduroy, ANTi's one-tuck, Odd Ritual's pleated black and Siegelman's
retro track. Every one of those is a frame the brand shot on a person.

THE SLIDETEXTS ARE LITERAL CHARACTERS, NOT HTML ENTITIES. They end up inside a
JS array and reach the DOM through textContent, which does not decode entities
— so "&mdash;" renders as those eight characters on the homepage card. Caught
on the Local Rule build by looking at the rendered card rather than the markup.
The slide NAMES are different: those are written as HTML, so entities are
correct there.

Dry run by default.
"""
import importlib.util, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
SITEMAP = ROOT / "sitemap.xml"
SEARCH = ROOT / "search-index.json"
KEY = "pantsedit1"
SLUG = "the-pants-edit"

spec = importlib.util.spec_from_file_location("lp", ROOT / "localize-pants.py")
lp = importlib.util.module_from_spec(spec); spec.loader.exec_module(lp)
BY_SLUG = {p[0]: p for p in lp.PICKS}

SLIDE_SLUGS = ["malbon", "criquet", "anti-country-club", "odd-ritual", "siegelman"]

# LITERAL EM DASHES AND CURLY QUOTES BELOW. See the docstring.
TEXTS = {
 "malbon":
  "Malbon Station Pant, Military Green — stone-washed cotton herringbone twill, "
  "army-derived, relaxed leg, mid rise. Seven of seven sizes live. $228.",
 "criquet":
  "Criquet Comfort Corduroy, Khaki — 74% cotton, 25% Tencel, three inseam lengths "
  "and an embroidered Grassy C at the back right hip. Designed in Austin, and the "
  "deepest size run on the list at twenty-one combinations. $154.",
 "anti-country-club":
  "ANTi Country Club Tokyo One-Tuck Chino, Beige — a single tuck, straight and "
  "deliberately not tapered below the knee, 100% cotton. Priced in yen: the dollar "
  "figure ANTi's storefront serves a US browser is Shopify conversion arithmetic, "
  "not a number the brand set. ¥28,600.",
 "odd-ritual":
  "Odd Ritual Pleated Daily Trouser, Black — 235gsm cotton twill, loose with a subtle "
  "carrot silhouette, elasticated back waistband, made locally in Cape Town. Three of "
  "five sizes left, so this is the one to move on. R1,300.",
 "siegelman":
  "Siegelman Stable Retro Track Pant — 70/30 cotton-poly, nylon coil zips lined in "
  "athletic mesh, unisex, made in Los Angeles. Dry clean only, which tells you what "
  "kind of track pant it is. $212.",
}


def card_html():
    slides = []
    for s in SLIDE_SLUGS:
        slug, brand, name, price, avail, kind, url, img = BY_SLUG[s]
        slides.append(f'''          <div class="gear-slide">
            <a href="{url}" target="_blank" rel="noopener">
              <img src="/images/pants-edit/{slug}.jpg" alt="{brand} {name}" loading="lazy" />
              <div class="gear-slide-info"><div class="gear-slide-brand">{brand}</div><div class="gear-slide-name">{name} &middot; {price}</div></div>
            </a>
          </div>''')
    return f'''<!-- THE PANTS EDIT -->
  <div class="card" data-type="drop">
    <div class="card-media" style="position:relative;">
      <span class="card-tag grass">[Drops &amp; Brands]</span>
      <div class="gear-carousel" data-carousel="{KEY}">
        <div class="gear-carousel-track">
{chr(10).join(slides)}
        </div>
        <button class="gear-arrow prev" onclick="gearSlide(this, -1)">&#8249;</button>
        <button class="gear-arrow next" onclick="gearSlide(this, 1)">&#8250;</button>
      </div>
    </div>
    <div class="card-body">
      <div class="card-title"><a href="/drops/{SLUG}" style="color:inherit;text-decoration:none;border-bottom:none;">The Pants Edit &mdash; The Pleat Came Back</a></div>
      <div class="card-text" data-slidetext="{KEY}">{TEXTS[SLIDE_SLUGS[0]]}</div>
      <div class="gear-dots" data-dots="{KEY}"></div>
      <div class="gear-counter" data-counter="{KEY}">1 / {len(SLIDE_SLUGS)}</div>
      <a href="/drops/{SLUG}" class="card-readmore" style="display:inline-block;margin-top:12px;font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:0.12em;text-transform:uppercase;border-bottom:1px solid var(--ink);padding-bottom:2px;">See the Full Post &rarr;</a>
    </div>
  </div>
'''


def wire_index(h):
    changed = []
    if f'data-carousel="{KEY}"' in h:
        changed.append("card already present")
    else:
        anchor = "<!--TGI-SC-HOME-->"
        if anchor not in h:
            sys.exit("! feed anchor <!--TGI-SC-HOME--> not found in index.html")
        h = h.replace(anchor, anchor + "\n" + card_html(), 1)
        changed.append("card inserted")

    if re.search(rf"^\s*{KEY}:\s*\[", h, re.M):
        changed.append("slideTexts already present")
    else:
        m = re.search(r"^(\s*)localrule1:\s*\[", h, re.M) or \
            re.search(r"^(\s*)foundgolf:\s*\[", h, re.M)
        if not m:
            sys.exit("! could not find the slideTexts object to extend")
        ind = m.group(1)
        body = "".join(f'{ind}        "{TEXTS[s]}",\n' for s in SLIDE_SLUGS)
        h = h[:m.start()] + f"{ind}{KEY}: [\n{body}{ind}      ],\n\n" + h[m.start():]
        changed.append("slideTexts inserted")
    return h, changed


def wire_sitemap(x):
    changed = []
    loc = f"https://thegrassyissue.com/drops/{SLUG}"
    if loc in x:
        changed.append("sitemap already has the post")
    else:
        x = x.replace("</urlset>",
                      f"  <url>\n    <loc>{loc}</loc>\n"
                      f"    <lastmod>2026-09-20</lastmod>\n"
                      f"    <changefreq>monthly</changefreq>\n"
                      f"    <priority>0.7</priority>\n  </url>\n</urlset>", 1)
        changed.append("sitemap + the post")
    return x, changed


def wire_search(j):
    """The index uses SHORT KEYS — u/t/d/g/i/k — not the long names a fresh
    reader would guess. Writing title/url/type here would append an entry the
    search UI silently ignores, which is the worst kind of wiring bug: nothing
    errors and the page is simply unfindable. Schema copied off a live entry."""
    changed = []
    url = f"/drops/{SLUG}"
    if any(e.get("u") == url for e in j):
        changed.append("search index already has the post")
        return j, changed
    j.append({
      "u": url,
      "t": "The Pants Edit — The Pleat Came Back",
      "d": ("Eighteen trousers from independent golf brands, one per brand, with "
            "prices read live on 20 September 2026 — and a count of every trouser "
            "style on sale across the TGI brand universe."),
      "g": "Drops & Brands",
      "i": "/images/pants-edit/band-hero.jpg",
      "k": " ".join(f"{p[1]} {p[2]} {p[3]}" for p in lp.PICKS),
    })
    changed.append("search index + the post")
    return j, changed


def main(apply_):
    h = INDEX.read_text(encoding="utf-8")
    x = SITEMAP.read_text(encoding="utf-8")
    j = json.loads(SEARCH.read_text(encoding="utf-8")) if SEARCH.exists() else []

    h2, ic = wire_index(h)
    x2, sc = wire_sitemap(x)
    j2, jc = wire_search(j)
    for c in ic + sc + jc:
        print("  " + c)
    if not apply_:
        print("\n  dry run — pass --apply")
        return

    INDEX.write_text(h2, encoding="utf-8")
    SITEMAP.write_text(x2, encoding="utf-8")
    SEARCH.write_text(json.dumps(j2, indent=2, ensure_ascii=False), encoding="utf-8")

    # ---- VERIFY THE FINISHED FILES ----
    hh = INDEX.read_text(encoding="utf-8")
    xx = SITEMAP.read_text(encoding="utf-8")
    jj = json.loads(SEARCH.read_text(encoding="utf-8"))
    bad = []
    if f'data-carousel="{KEY}"' not in hh: bad.append("card missing")
    if hh.count(f'data-carousel="{KEY}"') != 1: bad.append("card duplicated")
    if not re.search(rf"^\s*{KEY}:\s*\[", hh, re.M): bad.append("slideTexts missing")
    if hh.count(f"/drops/{SLUG}") < 2: bad.append("post links missing")

    # entities inside the JS array would render literally on the card
    m = re.search(rf"^\s*{KEY}:\s*\[(.*?)^\s*\],", hh, re.M | re.S)
    if m and re.search(r"&(mdash|rsquo|amp|middot|ndash|yen|lsquo|ldquo|rdquo);", m.group(1)):
        bad.append("HTML entity inside the JS slideTexts — renders literally")
    if m and len(re.findall(r'^\s*"', m.group(1), re.M)) != len(SLIDE_SLUGS):
        bad.append("slideTexts count does not match the slides")

    # slide count and images, scoped to this card only
    seg = hh[hh.find(f'data-carousel="{KEY}"'):
             hh.find("</div>", hh.find(f'data-counter="{KEY}"'))]
    n = len(re.findall(r'<div class="gear-slide">', seg))
    if n != len(SLIDE_SLUGS): bad.append(f"{n} slides, expected {len(SLIDE_SLUGS)}")
    for s in SLIDE_SLUGS:
        if not (ROOT / f"images/pants-edit/{s}.jpg").exists():
            bad.append(f"missing image for slide {s}")

    if SLUG not in xx: bad.append("sitemap entry missing")
    if not any(e.get("u") == f"/drops/{SLUG}" for e in jj):
        bad.append("search index entry missing")
    if not (ROOT / f"drops/{SLUG}.html").exists():
        bad.append("the post itself is not on disk")
    ours = next((e for e in jj if e.get("u") == f"/drops/{SLUG}"), None)
    if ours is not None and jj:
        sibling = next((e for e in jj if e.get("u") != f"/drops/{SLUG}"), None)
        if sibling and set(ours) != set(sibling):
            bad.append(f"search entry keys {sorted(ours)} != schema {sorted(sibling)}")

    if bad:
        sys.exit("! " + "; ".join(bad))
    print(f"\n  verified on disk: 1 card, {n} slides, slideTexts, sitemap, search index")


if __name__ == "__main__":
    main("--apply" in sys.argv)
