#!/usr/bin/env python3
"""wire-wild-spring-dunes.py — homepage card, sitemap, search. 20 Sept 2026.

Three jobs, idempotent, each verified against the FINISHED FILE.

THE CARD WAS WRONG THE FIRST TIME. Worth writing down, because the reasoning
that produced it looked careful and was not.

The original docstring here argued: "THIS IS A FIELD NOTE, NOT A DROP, so the
homepage card is the single-image data-type='field' shape with the flag tag —
not a gear carousel. Using the carousel card here would have meant inventing
five 'slides' for a golf course." That is an argument from first principles
about what a Field Note *ought* to look like. Nobody checked what the other
Field Notes on the homepage actually look like. A census of all 35 field cards
says:

  * 28 are posts. EVERY ONE is a gear carousel with `card-tag grass`.
  * The 7 that are single-image with `card-tag flag` are not posts at all —
    the Social Club standing feature and six `cursor:default` utility cards.

So the house shape for a Field Note post is exactly the carousel I talked
myself out of, and the premise was false too: Lions Municipal, Hancock, the NY
trip and the coffee roundup are all carousels of real place photography with
sourced captions. Nothing is invented. Wild Spring Dunes shipped six of their
own frames; four of them were sitting unused.

WHAT THE READER SAW. Because the card had no carousel, its <img> fell through
to `.card-media img {width:100%; height:auto}` — which has no ratio of its own
— so the 1800x771 masthead drew at its native 21:9: a 130px letterbox strip in
a row where every neighbouring card's media is 379px. Under it sat a seven-line
block of card text, where the siblings run three. Lenny: "the wild dunes card
on the homepage is formatted wierd."

The lesson is the one from the body bands, one step further out. There I
verified the files and not the render. Here I rendered the card, screenshotted
it to outputs/wsd-card.png, checked `card broken imgs: 0` — and never opened
the picture. A screenshot nobody looks at is not a verification, it is a file.

SLIDE TEXT GOES IN THE CENTRAL REGISTRY, not an inline script. There are two
mechanisms in index.html and only one works: the slider at the bottom reads
`window._slideTexts` (one underscore), while a number of inline per-card
scripts write `window.__slideTexts` (two). Those cards show slide 1's text and
then never change it. Lions is in the central registry, so this follows Lions.

Dry run by default.
"""
import json, pathlib, re, sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
SITEMAP = ROOT / "sitemap.xml"
SEARCH = ROOT / "search-index.json"
SOCIAL = ROOT / "events/social-club.html"
POST = ROOT / "drops/on-our-radar-wild-spring-dunes.html"

SLUG = "on-our-radar-wild-spring-dunes"
MARK = "<!-- ON OUR RADAR — WILD SPRING DUNES -->"
TITLE = "On Our Radar &mdash; Wild Spring Dunes"
KEY = "wsd26"                      # carousel id; must be unique in index.html
HERO = "/images/wild-spring-dunes/card-1.jpg"   # kept for the search index thumb

# The slides. Frames are the 4:5 card cuts from localize-wild-spring-dunes.py
# (CARD_FRAMES), so the browser's object-fit:cover has nothing left to crop.
#
# Captions are the facts table in research/wild-spring-dunes.json, not readings
# of the photograph. "6,962 yds, 74.6/147, par 72" is the TGA-rated card, which
# is the figure the research settled on over the 7,120 the site projected —
# see _conflicts_resolved. Nothing here is a verdict on the golf.
SLIDES = [
    ("card-1", "Sandy bunkering, and a wall of East Texas pine",
     "Tom Doak &middot; opened 8 September 2026"),
    ("card-2", "The bib, and the only way round",
     "Walking only &mdash; caddies available"),
    ("card-3", "Two players, a boardwalk, and the Piney Woods",
     "2,400 acres of former timber land"),
    ("card-4", "A green above the ravine on the back nine",
     "6,962 yds &middot; 74.6/147 &middot; par 72"),
    ("card-5", "The spring-fed creek the place is named for",
     "Mount Enterprise &middot; 4hr 15min from Austin"),
]

# One line per slide, shown in .card-text and swapped by the slider. Same
# sourcing rule as the captions.
SLIDE_TEXTS = [
    "A Tom Doak course on 2,400 acres of former timber land outside Mount "
    "Enterprise, open to the public since 8 September. The reason it looks like "
    "this is that a logging company took the pines off first.",

    "Walking only, with caddies available &mdash; no carts, no exceptions. In a "
    "state where the best golf is almost always behind a gate, this one is "
    "bookable by anyone.",

    "Eleven bridges and a boardwalk run the routing through the Piney Woods. "
    "The land was found by a Dallas office worker who taught himself to read "
    "soil surveys.",

    "6,962 yards, 74.6/147, par 72 off the Pine tees. $275 in peak season, $195 "
    "December to February. Michael Keiser Jr. developed it; a Coore &amp; "
    "Crenshaw course is already in build.",

    "The spring that gives the place its name. Mount Enterprise is 262 miles "
    "from Austin &mdash; about four and a quarter hours, and closer to two and "
    "a half from Dallas.",
]


def card_html():
    slides = "".join(
        f'''          <div class="gear-slide">
            <a href="/drops/{SLUG}">
              <img src="/images/wild-spring-dunes/{fn}.jpg" alt="Wild Spring Dunes &mdash; {name}" loading="lazy" />
              <div class="gear-slide-info"><div class="gear-slide-brand">{brand}</div><div class="gear-slide-name">{name}</div></div>
            </a>
          </div>
'''
        for fn, name, brand in SLIDES)
    return f'''{MARK}
  <div class="card" data-type="field">
    <div class="card-media" style="position:relative;">
      <span class="card-tag grass">[Field Notes]</span>
      <div class="gear-carousel" data-carousel="{KEY}">
        <div class="gear-carousel-track">
{slides}        </div>
        <button class="gear-arrow prev" onclick="gearSlide(this, -1)">&#8249;</button>
        <button class="gear-arrow next" onclick="gearSlide(this, 1)">&#8250;</button>
      </div>
    </div>
    <div class="card-body">
      <div class="card-title"><a href="/drops/{SLUG}" style="color:inherit;text-decoration:none;border-bottom:none;">{TITLE}</a></div>
      <div class="card-text" data-slidetext="{KEY}">{SLIDE_TEXTS[0]}</div>
      <div class="gear-dots" data-dots="{KEY}"></div>
      <div class="gear-counter" data-counter="{KEY}">1 / {len(SLIDES)}</div>
      <a href="/drops/{SLUG}" class="card-link">Read the Field Note &#8599;</a>
    </div>
  </div>
'''


def wire_slidetexts(h):
    """Add our lines to the CENTRAL window._slideTexts registry.

    Anchored on `window._slideTexts = {` — the object the slider actually
    reads. An inline script setting window.__slideTexts would look right in the
    diff and do nothing after slide 1.
    """
    if f'"{KEY}": [' in h or f"{KEY}: [" in h:
        return h, ["slideTexts already present"]
    anchor = "window._slideTexts = {"
    if anchor not in h:
        sys.exit("! window._slideTexts registry not found in index.html")
    lines = ",\n".join('      "' + t.replace('"', '\\"') + '"'
                       for t in SLIDE_TEXTS)
    block = f'{anchor}\n    "{KEY}": [\n{lines}\n    ],'
    return h.replace(anchor, block, 1), ["slideTexts + 5 lines"]


def wire_index(h):
    """Insert the card, or REPLACE one already there.

    Replacement matters: the first version of this card shipped with the wrong
    markup, and a wire script that only ever inserts cannot fix its own output.
    The old block is found by MARK and cut at the end of its .card div, so the
    replace is bounded by this card and cannot eat a neighbour.
    """
    new = card_html()
    if MARK in h:
        i = h.find(MARK)
        # end of THIS card: the first card-link, then out of the two divs
        j = h.find('class="card-link"', i)
        if j < 0:
            sys.exit("! existing card found but no card-link to bound it")
        j = h.find("</div>", h.find("</a>", j))      # close .card-body
        j = h.find("</div>", j + 6)                  # close .card
        if j < 0:
            sys.exit("! could not find the end of the existing card")
        old = h[i:j + 6]
        n_cards = old.count('<div class="card"')
        if n_cards != 1:
            sys.exit(f"! card bounds look wrong — the slice contains "
                     f"{n_cards} cards, expected 1")
        if old.strip() == new.strip():
            return h, ["card already current"]
        return h[:i] + new.rstrip() + "\n" + h[j + 6:], ["card REPLACED"]
    anchor = "<!--TGI-SC-HOME-->"
    if anchor not in h:
        sys.exit("! feed anchor <!--TGI-SC-HOME--> not found in index.html")
    return h.replace(anchor, anchor + "\n" + card_html(), 1), ["card inserted"]


def wire_sitemap(x):
    loc = f"https://thegrassyissue.com/drops/{SLUG}"
    if loc in x:
        return x, ["sitemap already has the post"]
    entry = (f"  <url>\n    <loc>{loc}</loc>\n"
             f"    <lastmod>2026-09-20</lastmod>\n"
             f"    <changefreq>monthly</changefreq>\n"
             f"    <priority>0.7</priority>\n  </url>\n</urlset>")
    return x.replace("</urlset>", entry, 1), ["sitemap + the post"]


def wire_search(j):
    """Short keys — u/t/d/g/i/k. Long names append an entry the UI ignores."""
    url = f"/drops/{SLUG}"
    if any(e.get("u") == url for e in j):
        return j, ["search index already has the post"]
    j.append({
      "u": url,
      "t": "On Our Radar — Wild Spring Dunes",
      "d": ("Tom Doak's new course in the East Texas Piney Woods opened to the "
            "public on 8 September 2026. What it is, how an office worker found "
            "the land, and whether the drive from Austin is justified."),
      "g": "Field Notes",
      "i": HERO,
      "k": ("Wild Spring Dunes Tom Doak Mount Enterprise East Texas Piney Woods "
            "Michael Keiser Dream Golf Bandon Sand Valley Coore Crenshaw "
            "Brett Messerall walking only caddie public golf Texas golf resort "
            "green fee 275 Nacogdoches zoysia"),
    })
    return j, ["search index + the post"]


def main(apply_):
    h = INDEX.read_text(encoding="utf-8")
    x = SITEMAP.read_text(encoding="utf-8")
    j = json.loads(SEARCH.read_text(encoding="utf-8"))

    h2, ic = wire_index(h)
    h2, tc = wire_slidetexts(h2)
    x2, sc = wire_sitemap(x)
    j2, jc = wire_search(j)
    for c in ic + tc + sc + jc:
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

    if MARK not in hh: bad.append("card missing")
    if hh.count(MARK) != 1: bad.append("card duplicated")
    if hh.count(f"/drops/{SLUG}") < 3: bad.append("card links incomplete")
    if not (ROOT / HERO.lstrip("/")).exists(): bad.append(f"missing {HERO}")

    # scope the card checks to THIS card, not the whole homepage
    i = hh.find(MARK)
    seg = hh[i:hh.find("</div>\n", hh.find('class="card-link"', i))]
    if 'data-type="field"' not in seg: bad.append("card is not typed as a Field Note")
    if "[Field Notes]" not in seg: bad.append("card tag is not [Field Notes]")

    # ---- THE SHAPE GUARD ----
    # The bug this file exists to fix was a card that did not look like its
    # neighbours. So the check is a comparison against the neighbours, read out
    # of the finished index.html — not a restatement of what card_html() emits.
    # A guard that asserts what the generator just wrote proves only that
    # Python works.
    from PIL import Image

    others = [m.start() for m in re.finditer(r'<div class="card" data-type="field"', hh)
              if m.start() != hh.find('<div class="card" data-type="field"', i)]
    peers = []
    for a in others:
        end = hh.find('<div class="card" data-type=', a + 10)
        s = hh[a:end if end > 0 else a + 6000]
        if 'class="card-link"' not in s:      # utility cards, not posts
            continue
        tagm = re.search(r'<span class="card-tag ([a-z]+)"', s)
        peers.append(("gear-carousel" in s, tagm.group(1) if tagm else None))
    post_peers = [p for p in peers if p[0]]
    if len(post_peers) < 10:
        bad.append(f"only found {len(post_peers)} peer Field Note posts — the "
                   f"shape comparison is not meaningful; check the scan")
    else:
        if "gear-carousel" not in seg:
            bad.append(f"card has no carousel, but {len(post_peers)} of "
                       f"{len(peers)} peer Field Note posts do")
        want_tag = Counter(t for c, t in post_peers if t).most_common(1)[0][0]
        got = re.search(r'<span class="card-tag ([a-z]+)"', seg)
        if not got or got.group(1) != want_tag:
            bad.append(f"card tag is '{got.group(1) if got else None}' but the "
                       f"house tag for a Field Note post is '{want_tag}'")

    # ---- THE SLOT GUARD ----
    # .gear-slide img is aspect-ratio:4/5 + object-fit:cover, so anything not
    # 4:5 gets silently cropped by the browser. The 21:9 masthead in this slot
    # is what produced the 130px letterbox strip Lenny saw.
    srcs = re.findall(r'<img src="(/images/wild-spring-dunes/[^"]+)"', seg)
    if not srcs:
        bad.append("card has no images")
    for s in srcs:
        p = ROOT / s.lstrip("/")
        if not p.exists():
            bad.append(f"card image missing: {s}"); continue
        with Image.open(p) as im:
            w, ht = im.size
        if abs(w / ht - 4 / 5) > 0.01:
            shown = min(1.0, (ht * 4 / 5) / w)
            bad.append(f"{s} is {w}x{ht} (ar {w/ht:.2f}) in the 4:5 card slot — "
                       f"the browser would show {shown*100:.0f}% of its width")

    # ---- SLIDE / TEXT / CAPTION COUNTS MUST AGREE ----
    n_slides = seg.count('<div class="gear-slide">')
    if n_slides != len(SLIDES):
        bad.append(f"{n_slides} slides rendered, {len(SLIDES)} defined")
    if seg.count("gear-slide-info") != n_slides:
        bad.append(f"{seg.count('gear-slide-info')} captions for {n_slides} slides")
    if f'data-slidetext="{KEY}"' not in seg:
        bad.append("card text is not wired to the slider")
    reg = re.search(r'window\._slideTexts = \{(.*?)\n  \};', hh, re.S)
    if not reg:
        bad.append("could not read the _slideTexts registry")
    elif f'"{KEY}"' not in reg.group(1):
        bad.append(f"'{KEY}' is not in the _slideTexts registry the slider reads "
                   f"— slide text would freeze after slide 1")
    else:
        block = re.search(rf'"{KEY}": \[(.*?)\n    \]', reg.group(1), re.S).group(1)
        n_txt = len(re.findall(r'\n      "', block))
        if n_txt != n_slides:
            bad.append(f"{n_txt} slide texts for {n_slides} slides")
    n_key = hh.count('data-carousel="' + KEY + '"')
    if n_key != 1:
        bad.append(f"carousel key '{KEY}' appears {n_key} times — must be unique")
    if seg.count("gear-arrow") != 2:
        bad.append(f"{seg.count('gear-arrow')} arrows on the carousel, expected 2")

    # Dots and counter are MARKUP the slider fills in, keyed by data-dots /
    # data-counter. Without them a 5-slide card gives the reader no sign there
    # is anything past slide 1 — which is how this card first shipped, and both
    # of its immediate neighbours have them.
    for attr in ("data-dots", "data-counter"):
        if f'{attr}="{KEY}"' not in seg:
            bad.append(f"card is missing its {attr} element")
    cm = re.search(r'data-counter="[^"]*">(\d+) / (\d+)<', seg)
    if cm and int(cm.group(2)) != n_slides:
        bad.append(f"counter says '/ {cm.group(2)}' but there are {n_slides} slides")

    if SLUG not in xx: bad.append("sitemap entry missing")
    ours = next((e for e in jj if e.get("u") == f"/drops/{SLUG}"), None)
    if ours is None:
        bad.append("search index entry missing")
    else:
        sib = next((e for e in jj if e.get("u") != f"/drops/{SLUG}"), None)
        if sib and set(ours) != set(sib):
            bad.append(f"search keys {sorted(ours)} != schema {sorted(sib)}")

    # THE CROSS-LINK RUNS BOTH WAYS OR IT IS NOT WIRED.
    if not POST.exists():
        bad.append("the post itself is not on disk")
    else:
        pp = POST.read_text(encoding="utf-8")
        if 'href="/events/social-club"' not in pp:
            bad.append("post does not link to the Social Club")
    s = SOCIAL.read_text(encoding="utf-8")
    if f"/drops/{SLUG}" not in s:
        bad.append("Social Club does not link to the post")

    if bad:
        sys.exit("! " + "; ".join(bad))
    print(f"\n  verified on disk: Field Note card, sitemap, search index, "
          f"Social Club cross-link both ways")


if __name__ == "__main__":
    main("--apply" in sys.argv)
