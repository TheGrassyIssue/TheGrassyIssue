#!/usr/bin/env python3
"""Trim the Water Bottle Edit to the brands TGI actually follows — 17 Sept 2026.

LENNY'S TWO NOTES: no flasks, and lean harder on the brands we like and follow.

THE FLASK. One entry, Seamus Golf's Tartan Flask at ~$50. It is a hip flask, not
a water bottle, and it was the only thing on the page that was not the thing the
page is about. Out.

THE MASS-MARKET FOUR. The rest of the trim is the entries that are not
independent golf brands, are not in the Brand Index in their own right, or whose
links point at a collection or a blog post rather than a product:

  · lululemon        — Back to Life Sport 24oz. A mass athleisure bottle.
  · TravisMathew     — Paint Sport Canteen. Link went to /collections/drinkware.
  · Owala            — Fairways For Days FreeSip. Link went to a blog post about
                       the design, not a product page.
  · Bettinardi x Tervis — Rainbow Script Venture Lite. Link went to
                       /collections/drinkware; the bottle is a Tervis blank.

WHY NOT BACKFILL TO SIXTEEN. Because the bottles do not exist. A sweep across
roughly a hundred Index-brand stores on 17 Sept 2026 turned up almost nothing:
Local Rule has Nalgenes (both sold out), Foray Golf has a $6 sport bottle,
Holderness & Bourne has a 16oz Tervis. None is a better entry than the ones
already here, and padding the count with weak picks is the opposite of what
Lenny asked for. Eleven independent bottles beats sixteen with five passengers.

WHAT SURVIVES, and why each one earns it: Tomorrow Golf, Manors, Malbon, Vessel,
Sugarloaf, MARK & LONA, Metalwood, Bivo, Dimpled Golf x SIC, Mogshade, Huega
House. Bivo is a cycling brand rather than a golf one and is kept deliberately —
the bottle is genuinely different engineering and the page says so.

Counts, the H2, the intro and the meta description are all recalculated from the
surviving card count rather than hand-edited, because this page has already been
caught three times today claiming a number it did not have.
"""
import re, os, sys, json, html as H

apply_ = "--apply" in sys.argv
P = "drops/the-water-bottle-edit.html"

# (identifying substring unique to the card, label for the log)
DROP = [
 ("www.seamusgolf.com/collections/flasks", "Seamus Golf — Tartan Flask (a flask, not a bottle)"),
 ("shop.lululemon.com", "lululemon — Back to Life Sport 24oz (mass athleisure)"),
 ("travismathew.com/collections/drinkware", "TravisMathew — Paint Sport Canteen (collection link)"),
 ("owalalife.com/blogs", "Owala — Fairways For Days FreeSip (blog link, mass brand)"),
 ("bettinardi.com/collections/drinkware", "Bettinardi x Tervis — Rainbow Script (collection link)"),
]

WORDS = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
         "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen"]

t = open(P, encoding="utf-8").read()
before_n = t.count('class="product-card"')
log = []

for needle, label in DROP:
    k = t.find(needle)
    if k == -1:
        log.append(f"  !! not found (already gone?): {label}")
        continue
    s = t.rfind('<div class="product-card"', 0, k)
    if s == -1:
        log.append(f"  !! no card wrapper around {label}")
        continue
    depth, j, end = 0, s, None
    while j < len(t):
        m = re.compile(r"<div\b|</div>").search(t, j)
        if not m:
            break
        if m.group(0).startswith("<div"):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                end = m.end(); break
        j = m.end()
    if end is None:
        raise SystemExit(f"unbalanced card around {label} — aborting")
    block = t[s:end]
    if needle not in block or block.count("product-card") != 1:
        raise SystemExit(f"refusing to delete a block I have not positively identified: {label}")
    e = end
    while e < len(t) and t[e] in "\n ":
        e += 1
    t = t[:s] + t[e:]
    log.append(f"removed  {label}")

N = t.count('class="product-card"')
W = WORDS[N] if N < len(WORDS) else str(N)

# ------------------------------------------------- counts recalculated, not typed
t = re.sub(r'(<h2 class="products-hdr">)The Collection[^<]*(</h2>)',
           lambda m: m.group(1) + f"The Collection &mdash; {N} Bottles" + m.group(2), t)
t = re.sub(r'(<div class="sidebar-detail"><span class="l">Pieces</span><span>)[^<]*(</span>)',
           lambda m: m.group(1) + f"{N} items" + m.group(2), t)
log.append(f"H2 and sidebar now read {N}")

INTRO = (
 f"<p>Nobody here is selling you a YETI or a Stanley. These are {W} bottles from {W} independent "
 "brands &mdash; the makers this site actually follows &mdash; and between them they cover MiiR and Ocean "
 "Bottle collaborations, a Nalgene in a colourway, a bike bottle borrowed wholesale from cycling, and one "
 "squeeze bottle that costs fifteen dollars and makes no apology for it.</p>"
 "<p>The spread runs $14 to $59. That is a four-fold gap for objects that all do the same job, which is why "
 "the section below the grid exists: the money in a water bottle goes almost entirely into things you "
 "cannot see in a product photograph.</p>"
 "<p>Every price here was read off the seller&rsquo;s own page on 17 September 2026, and anything not "
 "buyable that day says so on its card. Small brands run small batches and bottles are a category where "
 "collaborations sell out and do not come back, so read a sold-out tag as information rather than a "
 "disappointment.</p>")
m = re.search(r'(<div class="writeup-body">)(.*?)(</div>)', t, re.S)
if not m:
    raise SystemExit("no writeup-body found")
t = t[:m.start(2)] + INTRO + t[m.end(2):]
log.append("intro recounted")

DESC = (f"{N} water bottles from {N} independent golf brands, $14 to $59 — MiiR and Ocean Bottle collabs, "
        "a Nalgene, a bike bottle. Prices read live, 17 September 2026.")
for k_, attr in [("description", "name"), ("og:description", "property"), ("twitter:description", "name")]:
    t = re.sub(rf'(<meta {attr}="{re.escape(k_)}" content=")[^"]*(")',
               lambda mm: mm.group(1) + DESC + mm.group(2), t)
log.append("meta description recounted")

# ------------------------------------------------------------------- guards
plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", H.unescape(
    re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", t, flags=re.S))))
words = len(re.findall(r"[A-Za-z0-9']+", plain))
brands = re.findall(r'product-brand"[^>]*>([^<]+)</div>', t)
problems = []
if N != before_n - len(DROP):
    problems.append(f"expected {before_n - len(DROP)} cards, got {N}")
if len(brands) != N or len(set(b.strip() for b in brands)) != N:
    problems.append("brand count does not match card count, or a brand repeats")
if words < 1200:
    problems.append(f"only {words} words")
for tag in ("<div", "<section", "<a "):
    close = tag.replace("<", "</").strip() + ">"
    if t.count(tag) != t.count(close):
        problems.append(f"unbalanced {tag.strip()}")
if t.count("<h1") != 1:
    problems.append(f"{t.count('<h1')} h1 tags")
if re.search(r"\bflask\b", re.sub(r"<[^>]+>", " ", t), re.I):
    problems.append("the word 'flask' still appears on the page")
for needle, label in DROP:
    if needle in t:
        problems.append(f"{label}: link survived")
missing = [i for i in re.findall(r'src="(/images/[^"]+)"', t) if not os.path.exists(i.lstrip("/"))]
if missing:
    problems.append(f"missing images: {missing[:3]}")
for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
    json.loads(b)
if problems:
    raise SystemExit("REFUSED:\n  " + "\n  ".join(problems))

if apply_:
    open(P, "w", encoding="utf-8").write(t)

print(("applied" if apply_ else "DRY RUN") + f" — trimmed {before_n} -> {N} bottles")
for l in log:
    print("  ·", l)
print(f"  surviving: {', '.join(b.strip() for b in brands)}")
print(f"  {words} words | {t.count('product-gallery')} galleries")
if not apply_:
    print("\npass --apply to write")
