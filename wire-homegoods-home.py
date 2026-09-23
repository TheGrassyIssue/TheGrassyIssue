#!/usr/bin/env python3
"""wire-homegoods-home.py — bring the Home Golf Decor feed card in line with
the rebuilt post. 23 September 2026.

THE CARD WAS SELLING THINGS THE POST NO LONGER CONTAINS. Two of its four
slides are the PrimePutt mat and the Par x Design print, both cut in the
rebuild; a third quotes the Assouline at its old price. The title still reads
"18 Picks" against a post that now carries 19. A reader clicking that card
arrives somewhere else entirely.

EVERY FIGURE COMES OUT OF picks.json, the same file the post is built from.
Nothing here is typed by hand, so the card cannot drift from the page again:
if a price moves, both move together on the next run of either script.

THE SLIDE TEXT LIVES IN A JS MAP, NOT IN THE CARD. index.html carries a
window._slideTexts entry keyed "homedecor1" which overwrites the visible
<p class="card-text"> on load and on every slide change. Editing the card
markup alone changes nothing a reader sees — the Manors card had exactly this
fault, with three stale prices in the map and correct ones in the HTML.

THE CARD IS MOVED TO SLOT 1 — Lenny: "Let's move it to the fist slot like a
new post." It was at position 137 of 218, and the feed only renders 18 cards
before a Load More button, parking everything past that at left:-9999px. The
refresh was real and nobody would ever have seen it.

MOVED, NOT COPIED. There has only ever been one decor card and there must
still be exactly one when this finishes, so the verify counts the card's two
structural links across the whole file and fails if a stray copy survives.
A raw href count will not do this job: each gear-slide also links to the post,
so going from four slides to five raises that number on a perfectly good move.

Idempotent. Dry run by default.
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
HOME = ROOT / "index.html"
PICKS = ROOT / "research/homegoods/picks.json"
POST = ROOT / "drops/home-golf-decor-edit.html"
SLUG = "/drops/home-golf-decor-edit"
KEY = "homedecor1"

# stem -> (slide headline, the sentence the JS map shows under it)
SLIDES = [
    ("mugs-sugarloaf", "Sold out when we checked, and still the best object here",
     "Two 8-ounce mugs in soda-lime milk glass, jadeite green and white, "
     "stackable and hand-wash only. Sugarloaf's own copy opens with “These "
     "mugs make me happy”, which is the whole pitch."),
    ("chair-sentinel", "A Dyneema sling on an ash frame, folded flat",
     "Sentinel builds walking bags out of Dyneema and then builds a chair out "
     "of it. The most expensive piece in the edit and the only one you sit in."),
    ("stash-foray", "A faux Rules of Golf volume that opens into a box",
     "Velvet-lined, two compartments, and it sits on a shelf and fools people. "
     "The single best-designed object in the edit."),
    ("poster-mogshade", "Three wool panels, made to order over eight weeks",
     "Hard-edged geometry in felt, sold as a trio because the three are "
     "composed to hang as one."),
    ("book-impossible", "George Peper on the hundred greatest moments",
     "The former editor in chief of Golf magazine, hand-bound and delivered in "
     "a linen slipcase. The centrepiece of a table rather than a shelf."),
]
TITLE_OLD = "The Home Golf Decor Edit &mdash; 18 Picks for the 19th Hole"
TITLE_NEW = "The Home Golf Decor Edit &mdash; 19 Picks for the 19th Hole"


def card_span(h):
    k = h.find(f'data-carousel="{KEY}"')
    if k == -1:
        sys.exit(f"! no card carries data-carousel={KEY!r}")
    start = h.rfind('<div class="card" data-type=', 0, k)
    nxt = h.find('<div class="card" data-type=', k)
    if start == -1 or nxt == -1:
        sys.exit("! could not bound the decor card")
    end = h.rfind("</div>", start, nxt)
    return start, h.index("\n", end) + 1


def main(apply_):
    prods = {p["stem"]: p for p in json.loads(PICKS.read_text())["products"]}
    missing = [s for s, _, _ in SLIDES if s not in prods]
    if missing:
        sys.exit(f"! not in picks.json: {missing}")

    h = HOME.read_text(encoding="utf-8")
    original = h
    s, e = card_span(h)
    card = h[s:e]
    pos = h[:s].count('<div class="card" data-type=') + 1
    print(f"  card at feed position {pos}")

    # ---- slides ----
    blocks = []
    for stem, headline, _ in SLIDES:
        p = prods[stem]
        img = p["local"][0]
        price = f"${p['usd']:,.0f}"
        blocks.append(
            f'          <div class="gear-slide">\n'
            f'            <a href="{SLUG}">\n'
            f'              <img src="{img}" alt="{html.escape(p["title"])}" '
            f'loading="lazy" />\n'
            f'              <div class="gear-slide-info">'
            f'<div class="gear-slide-brand">{html.escape(p["brand"])} '
            f'&middot; {price}</div>'
            f'<div class="gear-slide-name">{headline}</div></div>\n'
            f'            </a>\n'
            f'          </div>')
    m = re.search(r'(<div class="gear-carousel-track">\n).*?(\n        </div>)',
                  card, re.S)
    if not m:
        sys.exit("! could not find the carousel track")
    card = card[:m.start()] + m.group(1) + "\n".join(blocks) + m.group(2) + \
        card[m.end():]
    card = re.sub(r'(data-counter="%s">)[^<]*' % KEY,
                  lambda x: x.group(1) + f"1 / {len(SLIDES)}", card)
    # The card writes the dash as a literal em-dash, the post writes it as
    # &mdash;, and guessing which cost a run. Match on the count alone.
    card, k = re.subn(r"(The Home Golf Decor Edit\s*(?:&mdash;|\u2014)\s*)18(\s+Picks)",
                      lambda x: x.group(1) + "19" + x.group(2), card)
    if k == 0 and not re.search(r"Decor Edit\s*(?:&mdash;|\u2014)\s*19\s+Picks", card):
        sys.exit("! the card title is neither the old nor the new form")

    # ---- move it to slot 1 ----
    # Lift the card whole and re-seat it as the first thing in the feed,
    # immediately after the opening <section class="feed">. The Manors card,
    # which currently holds slot 1, keeps its own comment marker and simply
    # moves down one.
    h = h[:s] + h[e:]
    anchor = '<section class="feed" id="feed" role="tabpanel" aria-label="Content feed">\n'
    if anchor not in h:
        sys.exit("! could not find the feed section opener")
    # strip any marker this script left on a previous run before writing a new
    # one — the card lift starts at the <div>, so the comment sits outside it
    # and one more accumulated per run
    MARKER = "  <!-- HOME GOLF DECOR &mdash; rebuilt 23 Sep 2026 -->\n"
    h = h.replace(MARKER, "")
    i = h.index(anchor) + len(anchor)
    h = h[:i] + MARKER + card + h[i:]

    s2, _ = card_span(h)
    print(f"  re-seated at feed position "
          f"{h[:s2].count(chr(60) + 'div class=' + chr(34) + 'card' + chr(34) + ' data-type=') + 1}")

    # ---- the text the reader actually sees ----
    mm = re.search(r"(\n    %s: \[\n).*?(\n    \],?\n)" % KEY, h, re.S)
    if not mm:
        sys.exit(f"! could not find the {KEY} slide-text array")
    body = "\n".join(
        '      "%s"%s' % (t.replace('"', '\\"'),
                          "," if i < len(SLIDES) - 1 else "")
        for i, (_, _, t) in enumerate(SLIDES))
    h = h[:mm.start()] + mm.group(1) + body + mm.group(2) + h[mm.end():]

    nslides = card.count('class="gear-slide"')
    print(f"  slides {nslides}, slide texts {len(SLIDES)}")
    if not apply_:
        print("\n  dry run — pass --apply")
        return
    HOME.write_text(h, encoding="utf-8")
    verify(original, prods)


def verify(original, prods):
    fin = HOME.read_text(encoding="utf-8")
    post = POST.read_text(encoding="utf-8")
    bad = []

    if fin.count(f'data-carousel="{KEY}"') != 1:
        bad.append("the card was duplicated")
    if fin.count('<div class="card" data-type=') != \
            original.count('<div class="card" data-type='):
        bad.append("the feed card count changed")
    s, e = card_span(fin)
    blk = fin[s:e]

    # MOVED, NOT COPIED — tested without assuming the card's markup shape.
    # The first version looked for '<a href="SLUG" class="card-link"' and
    # '<div class="card-title"><a href="SLUG"'; this card uses card-readmore
    # and puts a style attribute on the title link, so both patterns matched
    # zero times and the guard reported a copy on a perfectly good move.
    # The shape-independent invariant: every link to the post in this file
    # lives inside the one card.
    if fin.count(f'href="{SLUG}"') != blk.count(f'href="{SLUG}"'):
        bad.append(f"{fin.count(chr(34))and fin.count('href=' + chr(34) + SLUG + chr(34))} "
                   f"links to the post in the file but only "
                   f"{blk.count('href=' + chr(34) + SLUG + chr(34))} inside the card "
                   "— a stray copy survives")
    # measured from the card's opening tag (s), not from the carousel
    # attribute inside it — the latter always has the card's own <div ...>
    # ahead of it, so the count is 1 on a correct result, never 0
    ahead = fin[:s].count('<div class="card" data-type=')
    if ahead != 0:
        bad.append(f"the card is at slot {ahead + 1}, not slot 1")

    if blk.count('class="gear-slide"') != len(SLIDES):
        bad.append(f"{blk.count('class=' + chr(34) + 'gear-slide' + chr(34))} "
                   f"slides, expected {len(SLIDES)}")
    for stem, headline, _ in SLIDES:
        p = prods[stem]
        if p["local"][0] not in blk:
            bad.append(f"{stem}: image not referenced")
        if not (ROOT / p["local"][0].lstrip("/")).is_file():
            bad.append(f"{stem}: image not on disk")
        if headline not in blk:
            bad.append(f"{stem}: headline missing")
    if "gearSlide(this, -1)" not in blk or "gearSlide(this, 1)" not in blk:
        bad.append("the carousel lost an arrow handler")

    # NOTHING THE POST DROPPED MAY STILL BE ON THE CARD
    for gone in ("primeputt", "par-design", "gosports", "vagabond",
                 "crystal-imagery", "eureka", "wellputt", "perfect-practice"):
        if gone in blk.lower():
            bad.append(f"the card still shows a cut product: {gone}")

    # every price on the card and in its text map must exist on the post
    mm = re.search(r"\n    %s: \[\n(.*?)\n    \],?\n" % KEY, fin, re.S)
    if not mm:
        bad.append("the slide-text array is gone")
    else:
        arr = mm.group(1)
        n = len(re.findall(r'^\s*"', arr, re.M))
        if n != len(SLIDES):
            bad.append(f"slide-text map has {n} entries for {len(SLIDES)} slides")
        for _, _, t in SLIDES:
            if t.replace('"', '\\"') not in arr:
                bad.append(f"slide text not written: {t[:44]}...")
    for p in set(re.findall(r"\$[\d,]+", blk + (mm.group(1) if mm else ""))):
        if p not in post:
            bad.append(f"card shows {p}, which is not a price on the post")
    if "18 Picks" in blk:
        bad.append("the card still says 18 picks")
    if "cdn.shopify.com" in blk or "squarespace-cdn" in blk:
        bad.append("a hot-linked image got onto the card")

    if bad:
        HOME.write_text(original, encoding="utf-8")
        sys.exit("! reverted. " + "\n    ".join(bad))
    print(f"\n  wrote {HOME.name} — {len(SLIDES)} slides, title and every price "
          "agree with the post")
    print("\n  FLAGGED, NOT CHANGED:")
    print("    the post's schema still reads datePublished 2026-06-21 with")
    print("    dateModified 2026-09-23, which is what it is: a June post rebuilt")
    print("    in September. The visible date line reads 23 September 2026.")


if __name__ == "__main__":
    main("--apply" in sys.argv)
