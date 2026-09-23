#!/usr/bin/env python3
"""wire-manors-home.py — promote the refreshed Manors card to the top of the
feed and rebuild its carousel. 22 September 2026.

Lenny, asked whether the refresh would make a new card at the top: "Move it to
the top of the feed."

WHAT MOVES AND WHAT DOES NOT. The card itself is MOVED, not copied — there has
only ever been one Manors brand card and there must still be only one when this
finishes. It is lifted whole from its chronological slot at position 33 and
re-seated at position 1. The verify step counts links to the page across the
whole file and fails if the number changed, because a copy-instead-of-move here
would put two identical cards on the homepage.

IT LANDS ON ITS OWN ORPHANED COMMENT. The top of the feed already carries
"<!-- BRAND REVISITED — Manors -->" with no card under it — a marker left behind
when the card was last reordered. The card is re-seated directly beneath it, so
the comment means something again instead of being reinserted somewhere new.

THE CAROUSEL WAS LYING ABOUT TWO PRICES. The existing slides read "Outsider
Polartec® Polo · $115" and "Reebok x Manors · $176"; both were corrected on the
post to $114 and $174 from a live read on 22 September. Leaving the homepage on
the old figures is how a reader gets one number on the feed and another on the
page they click through to. The slides are rebuilt around the September drop and
the Greenskeeper trouser, which is what the refresh is actually about.

THE SLIDE IMAGES ALREADY EXIST. Every file referenced below was downloaded by
localise-manors-revisit.py, except tech-trouser.jpg which has been on the page
since the 2 September build. Nothing is fetched here and nothing is hot-linked.

THE CARD TEXT SAID "sixteen pieces". The page now carries 31. That sentence is
updated; the rest of the blurb is the approved copy and is left alone.

THE DATE FRAMING IS NOT CHANGED, AND THAT IS DELIBERATE. The post header reads
"September 2, 2026 · updated September 22, 2026" and it stays that way even at
the top of the feed, because the page IS a refresh of a September 2 post rather
than a new one. Flagged at the end so Lenny can overrule it.

Idempotent. Dry run by default.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
HOME = ROOT / "index.html"
SLUG = "/drops/brand-to-know-manors"
KEY = "manorsrev"
ANCHOR = "<!-- BRAND REVISITED &mdash; Manors -->"
ANCHOR_ALT = "<!-- BRAND REVISITED — Manors -->"

# (image, alt, brand line, name line)
SLIDES = [
    ("/images/manors/new-merino-hoodie.jpg",
     "Manors Merino Tech Hoodie in sand, worn with olive trousers",
     "Merino Tech Hoodie &middot; $301",
     "New in September, and the top of the range"),
    ("/images/manors/tech-trouser.jpg",
     "Manors Recycled Greenskeeper Trouser in ivory",
     "Recycled Greenskeeper Trouser &middot; $174",
     "Eight pockets, a double pleat, and the whole argument"),
    ("/images/manors/wild-clifftop.jpg",
     "A golfer in a Manors polo at the finish of a tee shot on a clifftop "
     "fairway with the sea and a rock stack behind",
     "Manors &middot; London, est. 2019",
     "They said nobody needed a technical polo"),
    ("/images/manors/new-ripstop-vest.jpg",
     "Manors Ripstop Tech Vest in sand, worn over a hooded mid-layer",
     "Ripstop Tech Vest &middot; $214",
     "Recycled TORAY ripstop, water repellent"),
    ("/images/manors/new-primaloft-cardigan.jpg",
     "Manors Heritage Primaloft cardigan in maroon",
     "Heritage Primaloft&reg; Cardigan &middot; $214",
     "Golden-age knitwear, rebuilt in Primaloft"),
]
OLD_TEXT = ("three collaborations, and the sixteen pieces that show both halves "
            "still on the rail.")
NEW_TEXT = ("three collaborations, the September drop, and the thirty-one pieces "
            "that show both halves still on the rail.")

# THE TEXT THE READER ACTUALLY SEES. The <p class="card-text"> in the card is
# only the pre-JS default; a window._slideTexts map further down index.html
# overwrites it on load and on every slide change. Editing the card markup alone
# leaves the visible blurb untouched — and the old map still read "$115",
# "$176" and "$54", every one of them corrected on the post this morning. One
# entry per slide, in slide order.
SLIDE_TEXTS = [
    "The Merino Tech Hoodie at $301, new in September. One hundred per cent "
    "merino on a silhouette the 2019 brand would have called beside the point.",
    "The Recycled Greenskeeper Trouser at $174. Eight pockets, a double pleat "
    "Manors calls a nod to on-course etiquette, and the clearest object in the "
    "range.",
    "Manors, London, established 2019 — the brand that built its identity "
    "on saying nobody needed another technical golf polo.",
    "The Ripstop Tech Vest at $214. Recycled TORAY ripstop, which earned its "
    "name outdoors long before golf took an interest in it.",
    "The Heritage Primaloft® Cardigan at $214. Golden-age golf knitwear "
    "rebuilt in Primaloft Active Evolve, which is both halves of the argument "
    "in one garment.",
]


def rewrite_slide_texts(h):
    """Replace the manorsrev entry in the window._slideTexts map."""
    m = re.search(r"(\n      manorsrev: \[\n).*?(\n      \],?\n)", h, re.S)
    if not m:
        sys.exit("! could not find the manorsrev slide-text array")
    body = "\n".join(
        '        "%s"%s' % (t.replace('"', '\\"'),
                            "," if i < len(SLIDE_TEXTS) - 1 else "")
        for i, t in enumerate(SLIDE_TEXTS))
    return h[:m.start()] + m.group(1) + body + m.group(2) + h[m.end():]


def card_span(h):
    """(start, end) of the single Manors feed card, by its carousel key."""
    k = h.find(f'data-carousel="{KEY}"')
    if k == -1:
        sys.exit(f"! no card carries data-carousel={KEY!r}")
    start = h.rfind('<div class="card" data-type=', 0, k)
    if start == -1:
        sys.exit("! could not find the opening div of the Manors card")
    nxt = h.find('<div class="card" data-type=', k)
    if nxt == -1:
        sys.exit("! could not find the card that follows the Manors card")
    # back off the trailing blank line / comment that belongs to the NEXT card
    end = h.rfind("</div>", start, nxt)
    end = h.index("\n", end) + 1
    return start, end


def build_track(old_block):
    """Rebuild the slides, preserving whatever wrapper the card already uses."""
    slides = "\n".join(
        f'          <div class="gear-slide">\n'
        f'            <a href="{SLUG}">\n'
        f'              <img src="{img}" alt="{alt}" loading="lazy" />\n'
        f'              <div class="gear-slide-info">'
        f'<div class="gear-slide-brand">{brand}</div>'
        f'<div class="gear-slide-name">{name}</div></div>\n'
        f'            </a>\n'
        f'          </div>'
        for img, alt, brand, name in SLIDES)
    m = re.search(r'(<div class="gear-carousel-track">\n).*?(\n        </div>)',
                  old_block, re.S)
    if not m:
        sys.exit("! could not find the gear-carousel-track to rebuild")
    return old_block[:m.start()] + m.group(1) + slides + m.group(2) + \
        old_block[m.end():]


def main(apply_):
    h = HOME.read_text(encoding="utf-8")
    original = h
    links_before = h.count(f'href="{SLUG}"')

    s, e = card_span(h)
    card = h[s:e]
    pos_before = h[:s].count('<div class="card" data-type=') + 1
    print(f"  Manors card found at feed position {pos_before}")

    # rebuild slides + fix the piece count, before moving anything
    card = build_track(card)
    if OLD_TEXT in card:
        card = card.replace(OLD_TEXT, NEW_TEXT, 1)
    elif NEW_TEXT not in card:
        sys.exit("! the card blurb is neither the original nor the updated one")

    # lift it out
    h = h[:s] + h[e:]

    # re-seat under its own orphaned comment
    anchor = ANCHOR if ANCHOR in h else ANCHOR_ALT
    if anchor not in h:
        sys.exit("! the 'BRAND REVISITED — Manors' comment is not in the feed")
    i = h.index(anchor) + len(anchor)
    if not h[i:].startswith("\n"):
        sys.exit("! unexpected layout after the anchor comment")
    h = h[:i + 1] + card + h[i + 1:]
    h = rewrite_slide_texts(h)

    s2, _ = card_span(h)
    pos_after = h[:s2].count('<div class="card" data-type=') + 1
    print(f"  re-seated at feed position   {pos_after}")
    print(f"  slides                       {len(SLIDES)}")

    if not apply_:
        print("\n  dry run — pass --apply")
        return
    HOME.write_text(h, encoding="utf-8")

    # ---- VERIFY THE FILE ON DISK ----
    fin = HOME.read_text(encoding="utf-8")
    bad = []

    # MOVED, NOT COPIED
    if fin.count(f'data-carousel="{KEY}"') != 1:
        bad.append(f"{fin.count(chr(34) + KEY + chr(34))} carousels named {KEY}, "
                   "expected 1 — the card was copied, not moved")
    # NOT a raw href count. Every gear-slide wraps its image in a link to the
    # post, so going from 4 slides to 5 raises that count by one on a perfectly
    # correct move — the first version of this guard failed the good result.
    # The invariant that actually distinguishes a move from a copy is that the
    # card's two structural links exist exactly once each in the whole file.
    for once, what in ((f'<a href="{SLUG}" class="card-link"', "card-link"),
                       (f'<div class="card-title"><a href="{SLUG}"', "card-title")):
        if fin.count(once) != 1:
            bad.append(f"{fin.count(once)} {what} elements point at the post, "
                       "expected 1 — the card was copied, not moved")
    if fin.count('<div class="card" data-type=') != \
            original.count('<div class="card" data-type='):
        bad.append("the total feed card count changed")

    s3, e3 = card_span(fin)
    blk = fin[s3:e3]

    slide_links = blk.count(f'<a href="{SLUG}">')
    total_links = fin.count(f'href="{SLUG}"')
    if total_links != 2 + slide_links:
        bad.append(f"{total_links} links to the post on the page, expected "
                   f"{2 + slide_links} (2 structural + {slide_links} slides) — "
                   "a stray copy of the card survives somewhere")
    if fin[:s3].count('<div class="card" data-type=') != 0:
        bad.append(f"the card is at position "
                   f"{fin[:s3].count('<div class=' + chr(34) + 'card' + chr(34) + ' data-type=') + 1}"
                   ", not 1")

    # slides complete and local
    for img, alt, brand, name in SLIDES:
        if not (ROOT / img.lstrip("/")).is_file():
            bad.append(f"{img} is not on disk")
        if img not in blk:
            bad.append(f"{img} not referenced in the card")
        if brand not in blk:
            bad.append(f"slide line missing: {brand}")
    if blk.count('class="gear-slide"') != len(SLIDES):
        bad.append(f"{blk.count('class=' + chr(34) + 'gear-slide' + chr(34))} "
                   f"slides rendered, expected {len(SLIDES)}")
    if "gearSlide(this, -1)" not in blk or "gearSlide(this, 1)" not in blk:
        bad.append("the carousel lost an arrow handler")
    if "cdn.shopify.com" in blk or "cdn.sanity.io" in blk:
        bad.append("a hot-linked image got into the card")

    # NO PRICE ON THE CARD MAY DISAGREE WITH THE POST
    post = (ROOT / "drops/brand-to-know-manors.html").read_text(encoding="utf-8")
    for p in set(re.findall(r"\$\d+", blk)):
        if p not in post:
            bad.append(f"the card shows {p}, which is not a price on the post")
    for stale in ("$115", "$176", "$54"):
        if stale + "<" in blk or stale + "&" in blk:
            bad.append(f"stale price {stale} survived on the card")

    # THE SLIDE-TEXT MAP IS CHECKED OUTSIDE THE CARD, WHICH IS THE WHOLE POINT.
    # It lives hundreds of lines further down index.html, so every guard scoped
    # to `blk` passed while the visible blurb still said $115 and $176. One
    # entry per slide, and no price in it that the post does not carry.
    m = re.search(r"\n      manorsrev: \[\n(.*?)\n      \],?\n", fin, re.S)
    if not m:
        bad.append("the manorsrev slide-text array is gone")
    else:
        arr = m.group(1)
        n = len(re.findall(r'^\s*"', arr, re.M))
        if n != len(SLIDES):
            bad.append(f"slide-text map has {n} entries for {len(SLIDES)} "
                       "slides — the blurb will fall out of step with the image")
        for p in set(re.findall(r"\$\d+", arr)):
            if p not in post:
                bad.append(f"slide text shows {p}, which is not a price on the post")
        for stale in ("$115", "$176", "$54"):
            if stale in arr:
                bad.append(f"stale price {stale} survived in the slide text")
        for t in SLIDE_TEXTS:
            if t.replace('"', '\\"') not in arr:
                bad.append(f"slide text not written: {t[:46]}...")

    # the card title must still be the post's h1 subject
    if "Manors Golf, Revisited" not in blk:
        bad.append("the card title changed")
    if "sixteen pieces" in blk:
        bad.append("the blurb still says sixteen pieces")

    if bad:
        HOME.write_text(original, encoding="utf-8")
        sys.exit("! reverted. " + "\n    ".join(bad))

    print(f"\n  wrote {HOME.name} — Manors card moved {pos_before} -> 1, "
          f"{len(SLIDES)} slides, prices agree with the post")
    print("\n  FLAGGED, NOT CHANGED:")
    print("    the post header still reads 'September 2, 2026 · updated")
    print("    September 22, 2026'. It is a refresh of a September 2 post, so")
    print("    that is accurate — but it will sit above newer posts in the feed.")
    print("    Say the word and I will reframe it as a 22 September publish.")


if __name__ == "__main__":
    main("--apply" in sys.argv)
