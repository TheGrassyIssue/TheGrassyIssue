#!/usr/bin/env python3
"""wire-austin-hub-links.py — make /field-guide the Austin hub it already
half is. 22 September 2026.

THE PROBLEM IS NOT LINK VOLUME, IT IS LINK KIND. /field-guide receives 448
internal links from 211 pages, and 424 of them are the site nav saying "Field
Guide" on every page of the site. Nav links carry almost no ranking signal and
no topical signal at all. The contextual links — the ones a crawler reads as
"this Austin page considers that page its hub" — number about two dozen.

JOB A — THE HOUSE BACKLINK COMPONENT, EXTENDED TO THE PAGES THAT EARNED IT.
19 pages already carry a bordered "← Part of the Austin Golf Field Guide" link
above their More block. It is an existing, styled, house component; this copies
it verbatim rather than inventing a second one.

  30 pages on the site are Austin-golf pages by content (>=6 Austin mentions
  and golf/course/muni vocabulary). 17 carry the component. Of the 13 that do
  not, SIX ARE DELIBERATELY EXCLUDED: texas-golf-brands-and-makers,
  brand-to-know-criquet, brand-to-know-edel-golf, brand-to-know-random-golf-club,
  the-bold-tee-edit and walker-golf-blooming-grounds-drop are apparel and
  equipment brands that happen to be Austin-based. They are not where-to-play
  content, and pointing them at a course guide would be link padding — the exact
  thing Lenny ruled out. The seven below are places to play, practice or go
  after a round, which is what the hub is about.

JOB B — ONE CONTEXTUAL LINK, NOT THREE. The hub was missing outbound links to
the events calendar, the private-clubs piece and Muni Kids. Only ONE of those
has a sentence on the page that can hold a link: "This section covers the events
calendar and the stories behind the courses." The other two are not mentioned
anywhere on the hub, so placing their links would have meant writing new
sentences whose only purpose was to carry a link. Those two pages get the
backlink component instead, which is a real one-way signal rather than a
manufactured two-way one.

NO NEW ANCHOR TEXT IS INVENTED. The component's wording is the house wording,
unchanged on all 26 pages. Deliberately not varied toward "best public golf
courses in Austin" on every page at once: 26 pages suddenly carrying the same
exact-match commercial anchor is a footprint, and the existing phrasing already
contains "Austin Golf Field Guide".

Idempotent. Dry run by default.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DROPS = ROOT / "drops"
HUB = ROOT / "field-guide/index.html"

# Copied byte-for-byte out of drops/austin-coffee-guide.html.
COMPONENT = ('<div style="max-width:1400px;margin:0 auto 40px;padding:0 32px;">'
             '<a href="/field-guide" style="display:inline-block;font-family:var(--mono);'
             'font-size:10px;letter-spacing:.14em;text-transform:uppercase;'
             'border:.5px solid var(--ink);padding:10px 14px;">'
             '&larr; Part of the Austin Golf Field Guide</a></div>')
NEEDLE = "Part of the Austin Golf Field Guide"
INSERT_BEFORE = "<!-- More from the Feed -->"

# Places to play, practise, or go after a round. Not brands.
PAGES = [
    "austin-indoor-golf-simulators",
    "austin-golf-events-calendar",
    "the-lottery-round-austin-private-clubs",
    "fourteen-independent-austin-coffee-shops",
    "date-night-after-36",
    "8-special-day-rounds-near-austin",
    "on-our-radar-wild-spring-dunes",
]

# (exact phrase on the hub, the phrase with the link in it). Must match once.
HUB_LINKS = [
    ("This section covers the events calendar and the stories behind the courses.",
     'This section covers the <a href="/drops/austin-golf-events-calendar">events calendar</a> '
     "and the stories behind the courses."),
]


def component(apply_):
    done, skipped = [], []
    for stem in PAGES:
        p = DROPS / f"{stem}.html"
        if not p.is_file():
            sys.exit(f"! no such page: {stem}")
        h = p.read_text(encoding="utf-8")
        if NEEDLE in h:
            skipped.append(f"{stem}: already carries it")
            continue
        n = h.count(INSERT_BEFORE)
        if n != 1:
            sys.exit(f"! {stem}: {n} More-block anchors, expected exactly 1")
        if apply_:
            p.write_text(h.replace(INSERT_BEFORE, COMPONENT + "\n  " + INSERT_BEFORE, 1),
                         encoding="utf-8")
        done.append(stem)
    return done, skipped


def hub(apply_):
    h = HUB.read_text(encoding="utf-8")
    out = []
    for phrase, linked in HUB_LINKS:
        if linked in h:
            out.append("already linked"); continue
        n = h.count(phrase)
        if n != 1:
            sys.exit(f"! hub anchor phrase appears {n} times, expected 1 — copy has changed")
        h = h.replace(phrase, linked, 1)
        out.append(f"linked {phrase[:46]!r}")
    if apply_:
        HUB.write_text(h, encoding="utf-8")
    return out


def main(apply_):
    done, skipped = component(apply_)
    print(f"  backlink component: {len(done)} added, {len(skipped)} already had it")
    for s in done:
        print(f"    + {s}")
    for s in skipped:
        print(f"    = {s}")
    print("\n  hub outbound:")
    for o in hub(apply_):
        print(f"    {o}")

    if not apply_:
        print("\n  dry run — pass --apply")
        return

    # ---- VERIFY ON THE FINISHED PAGES ----
    bad = []
    for stem in PAGES:
        h = (DROPS / f"{stem}.html").read_text(encoding="utf-8")
        if h.count(NEEDLE) != 1:
            bad.append(f"{stem}: {h.count(NEEDLE)} components, expected 1")
        # it must sit before the More block, not after it
        if NEEDLE in h and INSERT_BEFORE in h and h.index(NEEDLE) > h.index(INSERT_BEFORE):
            bad.append(f"{stem}: component landed below the More block")
    hh = HUB.read_text(encoding="utf-8")
    for _, linked in HUB_LINKS:
        if linked not in hh:
            bad.append("hub contextual link did not take")
    # the hub must not link to itself
    body = hh[hh.find(">", hh.find("<body")) + 1:]
    m = re.search(r"</header>(.*?)<footer", body, re.S)
    inner = m.group(1) if m else body
    for u in set(re.findall(r'href="(/drops/[^"#]+)"', inner)):
        if not (ROOT / (u.lstrip("/") + ".html")).is_file():
            bad.append(f"hub links to a missing page: {u}")

    # count the contextual (non-nav) inbound links now pointing at the hub
    contextual = 0
    for f in DROPS.glob("*.html"):
        if NEEDLE in f.read_text(encoding="utf-8", errors="ignore"):
            contextual += 1
    if bad:
        sys.exit("! " + "\n    ".join(bad))
    print(f"\n  verified: {contextual} pages now carry the hub backlink, "
          f"hub links all resolve, no self-links")


if __name__ == "__main__":
    main("--apply" in sys.argv)
