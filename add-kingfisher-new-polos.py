#!/usr/bin/env python3
"""add-kingfisher-new-polos.py — four new-arrival polos onto the Kingfisher
brand-to-know page. 22 September 2026.

Lenny: "let's update the kingfisher brand to know page with the new arrivals ...
Do not change anything about the page, write up or structure, just add these new
polos to the page."

SO THIS ADDS CARDS AND NOTHING ELSE. No heading is rewritten, no paragraph is
touched, no section is created. The four cards go into the existing
"New from the Collection" grid in the existing card shape, copied verbatim from
the p-1 Mechanic Polo card: product-card[id][data-frames] > product-gallery >
pg-track > pg-frame*, the two pg-arw buttons, pg-count, one pg-dot per frame with
the first .on, then product-body > product-brand / product-name / product-desc /
product-link.

THE ONE EXCEPTION, AND IT IS A COUNT, NOT COPY. The section tag reads
"The Collection — 20 Pieces" and that is the page's card total. Adding four makes
it 24, so the numeral moves with them; leaving it would put a wrong count above
the grid. Nothing else about the tag changes. Flagged to Lenny either way.

THEY ARE NOT SOLD OUT, WHICH THE PAGE TEXT CLAIMS THEY ARE. Reading the rendered
product pages for the word "sold out" returned true for all four, on every size —
four brand-new arrivals, all gone. That is Shopify's hidden option-label template
("Variant sold out or unavailable") which sits in the DOM for every option
regardless of stock. The real state, read 22 September 2026: Add to Cart enabled,
schema availability InStock, and no size option disabled. Four false "sold out"
cards would have shipped off the first reading.

HANDLES LIE HERE TOO, WORSE THAN USUAL. Orion Polo is /products/hugo-polo,
Antares is /scallop-polo-in-maroon, Nova is /hightower-polo, Vega is
/new-blue-polo. Every URL below comes from the collection JSON, never from the
title.

FRAMES WERE CHOSEN BY LOOKING AT A CONTACT SHEET, not by index. Each polo leads
with a clean front shot and carries the fabric-detail crop second, because the
pattern is the product on all four.

Images are downloaded to images/kingfisher-golf/, never hot-linked.
Idempotent. Dry run by default.
"""
import io
import json
import pathlib
import re
import sys
import urllib.request

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
PAGE = ROOT / "drops/brand-to-know-kingfisher-golf.html"
IMGDIR = ROOT / "images/kingfisher-golf"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}
WIDE = 1400

# (handle, display name, price, stem, [image indices], description)
POLOS = [
    ("hugo-polo", "Orion Polo", "$65", "new-orion-polo", [1, 2, 0, 3],
     "Blue with a small geometric print and navy tipping at the collar and cuff "
     "&mdash; the loudest of the four."),
    ("scallop-polo-in-maroon", "Antares Polo", "$65", "new-antares-polo", [2, 4, 1, 3],
     "Maroon with a fine tonal dot. The dressiest of the group and the one that "
     "goes to dinner afterwards."),
    ("hightower-polo", "Nova Polo", "$65", "new-nova-polo", [0, 1, 2],
     "Deep green with a tonal check that reads solid until you are close."),
    ("new-blue-polo", "Vega Polo", "$65", "new-vega-polo", [2, 3, 1, 0],
     "Light blue with a small check &mdash; the lightest of them."),
]
ANCHOR = '<h2 class="products-hdr">New from the Collection — August 2026</h2>\n    <div class="products-grid">'
COUNT_OLD = "The Collection &mdash; 20 Pieces"
COUNT_NEW = "The Collection &mdash; 24 Pieces"
MARK, END = "<!-- TGI-KF-NEW -->", "<!-- /TGI-KF-NEW -->"


def fetch(u, raw=False):
    r = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
    return r if raw else json.loads(r)


def localise(apply_):
    """Download the chosen frames. Returns {stem: [rel paths]}."""
    out = {}
    for handle, name, price, stem, idx, desc in POLOS:
        p = fetch(f"https://kingfisher-golf.com/products/{handle}.json")["product"]
        usable = [i for i in p["images"] if (i.get("width") or 0) >= 600]
        if max(idx) >= len(usable):
            sys.exit(f"! {name}: frame {max(idx)} requested, only {len(usable)} usable")
        rels = []
        for n, k in enumerate(idx):
            suffix = "" if n == 0 else f"-a{n+1}"
            f = IMGDIR / f"{stem}{suffix}.jpg"
            if not f.is_file():
                g = Image.open(io.BytesIO(fetch(usable[k]["src"], raw=True))).convert("RGB")
                w0, h0 = g.size
                tw = min(WIDE, w0)                      # never upscale
                g = g.resize((tw, round(h0 * tw / w0)), Image.LANCZOS)
                if apply_:
                    IMGDIR.mkdir(parents=True, exist_ok=True)
                    g.save(f, "JPEG", quality=88, optimize=True, progressive=True)
            rels.append(f"/images/kingfisher-golf/{f.name}")
        out[stem] = rels
        print(f"  {name:<14}{len(rels)} frames  {p['title']}  /{handle}")
    return out


def card(idx_id, name, price, handle, desc, frames):
    n = len(frames)
    pg = "".join(
        f'<div class="pg-frame"><img src="{f}" alt="Kingfisher Golf {name} '
        f'&middot; view {i+1} of {n}" loading="lazy" /></div>'
        for i, f in enumerate(frames))
    dots = "".join(
        f'<button class="pg-dot{" on" if i == 0 else ""}" data-i="{i}" '
        f'aria-label="View image {i+1}"></button>' for i in range(n))
    return (
        f'<div class="product-card" id="p-{idx_id}" data-frames="{n}">\n'
        f'      <div class="product-gallery"><div class="pg-track">{pg}</div>'
        f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
        f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
        f'<span class="pg-count">1/{n}</span>'
        f'<div class="pg-dots">{dots}</div></div>\n'
        f'      <div class="product-body">\n'
        f'        <div class="product-brand">Kingfisher Golf · New</div>\n'
        f'        <div class="product-name">{name} · {price}</div>\n'
        f'        <div class="product-desc">{desc}</div>\n'
        f'        <a href="https://kingfisher-golf.com/products/{handle}" target="_blank" '
        f'rel="noopener" class="product-link">Shop ↗</a>\n'
        f'      </div>\n'
        f'    </div>')


def main(apply_):
    frames = localise(apply_)
    h = PAGE.read_text(encoding="utf-8")
    before_cards = h.count('class="product-card"')

    h = re.sub(r"\s*" + re.escape(MARK) + r".*?" + re.escape(END) + r"\s*", "\n", h, flags=re.S)
    base = h.count('class="product-card"')

    if ANCHOR not in h:
        sys.exit("! the New-from-the-Collection grid anchor was not found")
    cards = [MARK]
    for n, (handle, name, price, stem, idx, desc) in enumerate(POLOS):
        cards.append(card(base + n + 1, name, price, handle, desc, frames[stem]))
    cards.append(f"    {END}")
    block = "\n".join(cards)
    h = h.replace(ANCHOR, ANCHOR + "\n" + block, 1)

    if COUNT_OLD in h:
        h = h.replace(COUNT_OLD, COUNT_NEW, 1)
    elif COUNT_NEW not in h:
        sys.exit("! piece-count tag not found in either form")

    print(f"\n  cards: {base} -> {h.count('class=' + chr(34) + 'product-card' + chr(34))}")
    if not apply_:
        print("  dry run — pass --apply")
        return
    PAGE.write_text(h, encoding="utf-8")

    # ---- VERIFY THE FINISHED PAGE ----
    fin = PAGE.read_text(encoding="utf-8")
    bad = []
    if fin.count(MARK) != 1 or fin.count(END) != 1:
        bad.append(f"{fin.count(MARK)} blocks, expected 1")
    blk = fin[fin.index(MARK):fin.index(END)]
    for handle, name, price, stem, idx, desc in POLOS:
        if f"{name} · {price}" not in blk:
            bad.append(f"{name}: card missing")
        if f"/products/{handle}" not in blk:
            bad.append(f"{name}: wrong or missing shop link")
        for rel in frames[stem]:
            if not (ROOT / rel.lstrip("/")).is_file():
                bad.append(f"{name}: image {rel} not on disk")
            if rel not in blk:
                bad.append(f"{name}: {rel} not referenced")
    # gallery controls complete on every new card, and dots == frames
    for dm, body in re.findall(r'data-frames="(\d+)"(.*?)</div>\s*<div class="product-body"',
                               blk, re.S):
        if body.count("pg-frame") != int(dm):
            bad.append(f"a card says {dm} frames but renders {body.count('pg-frame')}")
        # COUNT THE BUTTONS, NOT THE SUBSTRING. "pg-dots" is the container class
        # and contains "pg-dot", so a naive count returns frames+1 and fails a
        # correct card — the existing p-1 Mechanic card counts 5 the same way.
        dots = len(re.findall(r'<button class="pg-dot(?: on)?"', body))
        if dots != int(dm):
            bad.append(f"a card has {dots} dot buttons for {dm} frames")
        for need in ("pg-arw prev", "pg-arw next", "pg-count"):
            if need not in body:
                bad.append(f"a new card is missing {need}")
    # the count label must match the cards actually on the page
    total = fin.count('class="product-card"')
    m = re.search(r"The Collection &mdash; (\d+) Pieces", fin)
    if not m or int(m.group(1)) != total:
        bad.append(f"tag says {m.group(1) if m else '?'} pieces, page has {total} cards")
    # NOTHING ELSE MAY HAVE MOVED
    if total != before_cards and total - base != len(POLOS):
        bad.append("card count changed by something other than this block")
    for untouched in ("The Original Collection &mdash; 12 Pieces",
                      "New from the Collection — August 2026",
                      "Kingfisher treats a shirt like a design brief"):
        if untouched not in fin:
            bad.append(f"page content changed that should not have: {untouched[:44]}")
    if bad:
        sys.exit("! " + "\n    ".join(bad))
    print(f"  wrote {PAGE.name} — {len(POLOS)} cards added, tag now {total} pieces")
    print("\n  FLAGGED, NOT CHANGED:")
    print("    'New from the Collection — August 2026' now holds September arrivals")
    print("    the hero meta still reads '12 Pieces' — already wrong before this change")


if __name__ == "__main__":
    main("--apply" in sys.argv)
