#!/usr/bin/env python3
"""build-homegoods.py — rebuild The Home Golf Decor Edit. 22 September 2026.

Lenny: "redo this one, less booze stuff, more design forward items", "keep that
stand for the bag, they will restock soon", "Intergrate some quotes into the
post for flavor and give it the TGI take also", plus the Foray stash book and
"also maybe some coffee table books".

WHAT CHANGES

  All three decanters and the coaster set are gone, along with the generic bag
  organiser, the celebrity-branded putting mat, the shadow box and the
  retailer-linked leather book. Eighteen picks, every price read from the
  brand's own store on 22 September 2026.

  Single images become swipeable galleries. The page was on the old
  .product-img format — one photo, no arrows — while every other post on the
  site uses .product-gallery. The CSS and the JS are ported verbatim from
  brand-to-know-manors.html rather than rewritten, so the behaviour matches.

  A TGI Take and three founder pull-quotes are added, all three sourced and
  attributed to a named person, a publication and a date.

THE CARD STOPS BEING A LINK. The old card wrapped everything in one <a>. A
gallery puts <button> arrows and dots inside the card, and interactive elements
nested in an anchor is invalid HTML that breaks keyboard use. Cards become divs
with a .product-link anchor in the body, which is what the rest of the site does.

FRAMES WERE CHOSEN BY LOOKING AT THE CONTACT SHEET, and three of them would
have shipped broken otherwise:
  - pencil-sentinel frame 1 is a blank grey placeholder, not the pen.
  - stand-park frame 4 is a different product entirely (a cowhide bag display),
    bled in from the Squarespace gallery.
  - book-impossible leads on a white slipcase that does not read as a book, so
    the open spread leads instead.

TWO THINGS FLAGGED, NOT DECIDED HERE. The Park Golf Stand is out of stock and
in the post anyway at Lenny's instruction, so the card says so rather than
implying it is buyable. And Matchstick's "Tiger Roar Relief Print" is an
illustrated likeness of a living public figure sold by a third party; it is
described by what it is without asserting who it depicts.

Idempotent. Dry run by default.
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
PAGE = ROOT / "drops/home-golf-decor-edit.html"
DONOR = ROOT / "drops/brand-to-know-manors.html"
PICKS = ROOT / "research/homegoods/picks.json"
READ = "23 September 2026"
MARK, END = "<!-- TGI-DECOR -->", "<!-- /TGI-DECOR -->"

# stem -> (frame order, one-line description written from the store's own copy)
COPY = {
 "chair-sentinel": ([0, 2, 3],
  "Sentinel hangs a Dyneema sling on an ash frame and folds the whole thing "
  "flat. The most expensive piece here and the only one you sit in."),
 "poster-mogshade": ([1, 2, 3, 0],
  "Three wool panels of hard-edged geometry, made to order over about eight "
  "weeks. Sold as a trio because they are composed to hang as one."),
 "stand-park": ([0, 1, 2],
  "Solid American walnut out of Missouri, oil finish and wax sealer, made by "
  "hand in Los Angeles. Your carry bag stops living on the floor."),
 "chair-sugarloaf": ([0, 1, 2, 3],
  "Sugarloaf put its mark on a Crazy Creek folding chair in club green. It "
  "packs flat against a wall and comes out for the nine holes that finish "
  "after sunset."),
 "vase-foray": ([0, 1, 2, 3],
  "A bobble-head golfer that is also a vase. It is the least serious object in "
  "the edit and the one most likely to get picked up."),
 "incense-quiet": ([1, 0, 2, 3],
  "The holder spells QUIET PLEASE down its length in slim ceramic. Twenty-five "
  "dollars buys the only piece here that changes how a room smells."),
 "yardage-bluegrass": ([0],
  "Italian Buttero leather, black, cut to hold a scorecard and a yardage book. "
  "Buttero is vegetable-tanned, so it darkens rather than wears out."),
 "yardage-seamus": ([0, 1, 2, 3],
  "The Irish National Tartan, woven in wool and bound to leather. Seamus built "
  "a business on tartan headcovers and this is the desk-sized version."),
 "print-matchstick": ([0, 1, 2],
  "A hand-pulled relief print of a golfer mid-roar, red shirt, blue cap. "
  "Matchstick normally works at ball-marker scale; this is the wall-sized one."),
 "stash-foray": ([0, 1, 2, 3],
  "A faux &ldquo;Rules of Golf&rdquo; volume that opens into a velvet-lined box "
  "with two compartments. It sits on a shelf and fools people."),
 "planter-foray": ([0, 1, 2, 3],
  "Vintage sports books hollowed into a planter, spines still reading Fishing, "
  "Bowling, Golf. One of one, so what you see is what ships."),
 "pencil-sentinel": ([1, 2, 3],
  "The Kaweco Mini Special in black, a pocket pencil that has been in "
  "production in Heidelberg for decades. Sentinel just picked well."),
 "mugs-gumtree": ([0, 3, 2, 1],
  "Gumtree runs a coffee arm, and these two milk-glass mugs carry its club "
  "mark. Heavy, opaque, and the right shape for a flat white."),
 "moka-gumtree": ([0, 1],
  "The club mark sits on the tank of a blacked-out moka pot. Stovetop espresso "
  "is the correct way to start a round and this is the correct object for it."),
 "poster-apres": ([0, 1, 2, 3],
  "Apr&egrave;s-Golf shot five coloured pencils as a still life and printed it "
  "at 11 by 14 inches. Cheap, graphic, and it hangs like a design poster."),
 "mugs-sugarloaf": ([0, 1, 2, 3],
  "Sugarloaf sells these in pairs: two 8-ounce mugs in soda-lime milk glass, "
  "jadeite green and white, stackable and hand-wash only. Its own product copy "
  "opens with &ldquo;These mugs make me happy&rdquo;, which is the whole pitch."),
 "poster-sugarloaf": ([0, 1],
  "The Biarritz green at Yale, framed and ready to hang at forty dollars. "
  "Sugarloaf makes four of these; this is the one with the best light."),
 "book-impossible": ([3, 0, 1],
  "George Peper, former editor in chief of Golf magazine, assembles the hundred "
  "greatest moments in the game here. It ships in a linen slipcase and it is "
  "the centrepiece of a table rather than a shelf."),
 "book-morocco": ([0, 1, 2],
  "Assouline traces golf in Morocco back to the Royal Country Club of Tangier "
  "in 1914. A hundred and twenty dollars for the most unexpected golf book in "
  "print."),
}
GROUPS = [
 ("Objects for the Room", "Furniture, wall pieces and the one thing that changes how a room smells",
  ["chair-sentinel", "poster-mogshade", "stand-park", "chair-sugarloaf",
   "vase-foray", "incense-quiet"]),
 ("Desk &amp; Shelf", "Leather, paper and one pencil that has outlived most golf brands",
  ["yardage-bluegrass", "yardage-seamus", "print-matchstick", "stash-foray",
   "planter-foray", "pencil-sentinel"]),
 ("Kitchen &amp; Wall", "Coffee comes first, then the two cheapest pieces of art in the edit",
  ["mugs-sugarloaf", "mugs-gumtree", "moka-gumtree", "poster-apres",
   "poster-sugarloaf"]),
 ("Coffee Table Books", "Two from Assouline, at opposite ends of what a golf book can cost",
  ["book-impossible", "book-morocco"]),
]

QUOTES = [
 ("It&rsquo;s one of the only sports where you can actually choose what to look "
  "like and how to dress.", None),  # placeholder, replaced below
]
PQ = [
 ("There&rsquo;s a luxury in the restraint, knowing that you have a piece that "
  "is special, that has some storytelling that might make you a little bit more "
  "interesting out there on the course, and that you can&rsquo;t get in a big "
  "box retailer at a pro shop.",
  "Karsten Jurkschat, founder, Gumtree Golf &amp; Nature Club, to Forbes, April 2025"),
 ("The most enjoyable challenge is exploring the boundaries (or lack thereof) "
  "beyond golf and how that can be done in both product and brand the right way, "
  "balancing innovation and tradition.",
  "John Mooty, founder, Sentinel, to The Old Ghosts, December 2025"),
 ("We have only ever made the things we wanted for ourselves and not a single "
  "thing more.",
  "Ian Gilley, founder, Sugarloaf Social Club, brand site, accessed September 2026"),
]


def pull_quote(text, attr):
    return (f'\n<div class="pull-quote">\n  <div class="pull-quote-inner">'
            f'&ldquo;{text}&rdquo;'
            f'<span class="pull-quote-attr">&mdash; {attr}</span></div>\n</div>\n')


def donor_css_js():
    """Lift the gallery CSS, pull-quote CSS and gallery JS from the Manors page.

    Copied rather than retyped: a hand-rewritten copy of a 709-character CSS
    block drifts from the original the first time either is touched.
    """
    d = DONOR.read_text(encoding="utf-8")
    style = d[d.index("<style>"):d.index("</style>")]
    js = re.search(r"<script>[^<]*?pg-track.*?</script>", d, re.S)
    if not js:
        sys.exit("! could not lift the gallery JS from the donor")

    # EVERY RULE FOR EVERY CLASS WE EMIT, collected by selector rather than by
    # slicing a range out of the stylesheet. The first version took
    # ".product-gallery{" up to the next unrelated selector and silently left
    # .pg-count, .pg-dot, .pg-dots and .pg-dot.on behind — verify-post caught
    # five classes on the page with no rule backing them, which is dots and a
    # counter rendering as unstyled junk.
    want = ("product-gallery", "pg-track", "pg-frame", "pg-arw", "pg-count",
            "pg-dots", "pg-dot", "pull-quote", "pull-quote-inner",
            "pull-quote-attr", "cat-kicker")
    # No line anchor. The donor stylesheet is minified and packs several rules
    # onto one line, so a "(?:^|\n)selector{" pattern matches only the first
    # rule per line and silently drops the rest — which is how .cat-kicker,
    # .pg-count and the dot rules went missing on the first pass.
    rules, seen = [], set()
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", style):
        sel, body = m.group(1).strip().lstrip(";").strip(), m.group(2)
        if not sel or sel.startswith("@"):
            continue
        if not any(re.search(r"\.%s(?![\w-])" % re.escape(c), sel) for c in want):
            continue
        rule = f"{sel}{{{body}}}"
        if rule not in seen:
            seen.add(rule)
            rules.append(rule)
    if not rules:
        sys.exit("! no gallery/pull-quote rules found in the donor stylesheet")
    missing = [c for c in want
               if not any(re.search(r"\.%s(?![\w-])" % re.escape(c), r) for r in rules)]
    if missing:
        sys.exit(f"! donor has no rule for: {missing}")
    return "\n".join(rules), "", js.group(0)


def card(pid, p, order, desc):
    n = len(order)
    frames = [p["local"][k] for k in order]
    name = html.escape(p["title"])
    price = f"${p['usd']:,.0f}"
    stock = "" if p["in_stock"] else (
        '<div class="product-stock" style="font-family:var(--mono);font-size:9px;'
        'letter-spacing:.1em;text-transform:uppercase;opacity:.55;margin-bottom:8px;">'
        f'Sold out when we checked, {READ}</div>')
    pg = "".join(
        f'<div class="pg-frame"><img src="{f}" alt="{name} &middot; view {i+1} of {n}" '
        f'loading="lazy" /></div>' for i, f in enumerate(frames))
    dots = "".join(
        f'<button class="pg-dot{" on" if i == 0 else ""}" data-i="{i}" '
        f'aria-label="View image {i+1}"></button>' for i in range(n))
    return (
        f'<div class="product-card" id="{pid}" data-frames="{n}">'
        f'<div class="product-gallery"><div class="pg-track">{pg}</div>'
        f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
        f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
        f'<span class="pg-count">1/{n}</span>'
        f'<div class="pg-dots">{dots}</div></div>'
        f'<div class="product-body">'
        f'<div class="product-brand">{html.escape(p["brand"])}</div>'
        f'<div class="product-name">{name} &middot; {price}</div>'
        f'{stock}'
        f'<div class="product-desc">{desc}</div>'
        f'<a href="{p["url"]}" target="_blank" rel="noopener" class="product-link">'
        f'Shop at {html.escape(p["brand"])} &#8599;</a>'
        f'</div></div>')


TAKE = """
<section class="products" data-btk="take" style="border-top:none;padding-top:0;">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Golf home decor earns its reputation honestly: most of it is a logo applied to an object somebody else designed. The interesting version is the opposite, an object that would survive in a room with no golf in it and happens to have come from a golf brand. That is the filter for these nineteen picks, drawn from twelve brands and running from $25 to $1,400.</p>
    <p style="margin-top:16px">What earns a place here is use. A moka pot goes on the hob every morning. A folding chair comes out for the nine holes that finish after sunset. A ceramic holder changes how a room smells, and a hollowed-out book takes the things you empty out of your pockets. The golf on them is incidental to why you would keep them, and that is the test.</p>
    <p style="margin-top:16px">The range runs from a twenty-five dollar incense holder to a fourteen-hundred-dollar Assouline, which is a wider spread than the category usually offers. Everything was priced and stock-checked on the brand&rsquo;s own store on 23 September 2026, and the one piece that is sold out says so on its card.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Edit</div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>{NPICKS}</span></div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>{NBRANDS}</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$25&ndash;$1,400</span></div>
      <div class="sidebar-detail"><span class="l">Prices read</span><span>23 Sep 2026</span></div>
      <div class="sidebar-detail"><span class="l">Cheapest</span><span>Quiet Golf incense</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Foray stash book</span></div>
      <div class="hashtags">
        <span class="hashtag">#GolfDecor</span>
        <span class="hashtag">#HomeGolf</span>
        <span class="hashtag">#19thHole</span>
        <span class="hashtag">#DesignForward</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

WHY = """
<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr" id="why-objects">Why Golf Brands Started Making Objects</h2>
  <div style="max-width:760px;font-size:16px;line-height:1.7;">
    <p>The brands in this edit did not arrive at homeware by way of a licensing deal. They arrived because the people running them make small numbers of things they wanted themselves, and a moka pot is no harder to get right than a polo if you are only making a few hundred.</p>
    <p style="margin-top:16px">Gumtree sells coffee, prints and quilted headcovers out of New York and describes itself as a slow-fashion golf brand. Sentinel builds walking bags out of Dyneema and then builds a chair. Sugarloaf started with hats because it wanted hats. None of them set out to furnish a room, and that is roughly why the objects are good.</p>
  </div>
</section>
"""


def main(apply_):
    data = json.loads(PICKS.read_text(encoding="utf-8"))
    prods = {p["stem"]: p for p in data["products"]}
    missing = [s for _, _, ss in GROUPS for s in ss if s not in prods]
    if missing:
        sys.exit(f"! not in picks.json: {missing}")

    npicks = sum(len(ss) for _, _, ss in GROUPS)
    nbrands = len({prods[s]["brand"] for _, _, ss in GROUPS for s in ss})

    h = PAGE.read_text(encoding="utf-8")
    original = h

    # THE COUNT IS IN THE TITLE, THE H1, THE META AND THE SIDEBAR. Adding one
    # pick used to mean four places to remember; all four now come off GROUPS.
    for a, b in ((f"{npicks - 1} Picks for the 19th Hole",
                  f"{npicks} Picks for the 19th Hole"),):
        h = h.replace(a, b)
    gal_css, pq_css, gal_js = donor_css_js()

    # ---- CSS: (re)install the ported rules, between markers ----
    # MARKED so a rerun can REPLACE them. The first version only injected when
    # ".product-gallery{" was absent, so an incomplete first pass was permanent:
    # the dot, counter and kicker rules stayed missing no matter how many times
    # the extraction was fixed and the script re-run.
    CSS_A, CSS_B = "/* TGI-DECOR-CSS */", "/* /TGI-DECOR-CSS */"
    # whitespace-symmetric: the strip must eat the newline the insert adds
    # back, or one blank line accumulates in the stylesheet per run
    h = re.sub(re.escape(CSS_A) + r".*?" + re.escape(CSS_B) + r"\n?", "",
               h, flags=re.S)
    anchor = ".product-body{"
    if anchor not in h:
        sys.exit("! could not find .product-body in the stylesheet")
    # The two-column layout for the TGI Take block. These selectors live inside
    # (and beside) a media query in the donor, so the brace-pair scanner above
    # cannot see them — without this the sidebar stretches the full width and
    # its labels and values end up at opposite edges of the page.
    take = (
        'section[data-btk="take"]{display:grid;'
        'grid-template-columns:minmax(0,1fr) 300px;'
        'column-gap:56px;max-width:1400px;margin:0 auto}\n'
        'section[data-btk="take"] .writeup-body{max-width:760px}\n'
        'section[data-btk="take"] .sidebar{position:sticky;top:88px;'
        'align-self:start}\n'
        'section[data-btk="take"] .products-hdr{margin-left:0;margin-right:auto}\n'
        '@media(max-width:1000px){'
        'section[data-btk="take"]{grid-template-columns:1fr;row-gap:28px}'
        'section[data-btk="take"] .sidebar{position:static;max-width:760px}}'
    )
    extra = (take + "\n.product-stock{font-family:var(--mono);font-size:9px;"
             "letter-spacing:.1em;text-transform:uppercase;opacity:.55;"
             "margin-bottom:8px}")
    h = h.replace(anchor, CSS_A + "\n" + gal_css + "\n" + extra + "\n"
                  + CSS_B + "\n" + anchor, 1)

    # ---- body: replace the whole products section ----
    # THE OLD INTRO BLOCK GOES TOO. Replacing only the products section left a
    # second, older <div class="writeup"> above it carrying its own QUICK LOOK
    # sidebar — so the rendered page showed two stacked sidebars and a lede
    # still advertising "fourteen brands", "$14-$945", "six categories" and the
    # Vagabond decanter set that this rebuild removes. Every gate passed,
    # because every gate was scoped to the new block. Only the render showed it.
    intro = re.search(r'<div class="writeup">.*?(?=' + re.escape(MARK)
                      + r'|<section class="products" id="products">)', h, re.S)
    if intro:
        h = h[:intro.start()] + h[intro.end():]

    # THE MARKERS ARE THE ANCHOR, not the original section. The first version
    # stripped MARK..END and then looked for <section class="products"
    # id="products"> to replace — but that section was consumed by the first
    # run, so every rerun died with "could not find the products section".
    # Instead: on a virgin page the old section becomes an empty MARK/END pair,
    # and from then on the pair is what gets refilled.
    if MARK not in h:
        m = re.search(r'<section class="products" id="products">.*?</section>', h, re.S)
        if not m:
            sys.exit("! no marker pair and no original products section to replace")
        h = h[:m.start()] + MARK + END + "\n" + h[m.end():]
    m = re.search(re.escape(MARK) + r".*?" + re.escape(END), h, re.S)
    if not m:
        sys.exit("! marker pair went missing")

    blocks, pid = [], 0
    for title, kicker, stems in GROUPS:
        cards = []
        for s in stems:
            pid += 1
            order, desc = COPY[s]
            p = prods[s]
            if max(order) >= len(p["local"]):
                sys.exit(f"! {s}: frame {max(order)} requested, "
                         f"only {len(p['local'])} on disk")
            cards.append(card(f"p-{pid}", p, order, desc))
        blocks.append(
            f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <h2 class="products-hdr">{title}</h2>\n'
            f'  <p class="cat-kicker"><strong>{len(stems)} picks &middot; read {READ}</strong>'
            f'{kicker}.</p>\n    <div class="products-grid">\n'
            + "\n".join(cards) + "\n    </div>\n</section>\n")

    body = (MARK + TAKE.replace("{NPICKS}", str(npicks)).replace("{NBRANDS}", str(nbrands)) + pull_quote(*PQ[0]) + blocks[0] + pull_quote(*PQ[1])
            + blocks[1] + WHY + pull_quote(*PQ[2]) + blocks[2] + blocks[3]
            + END + "\n")
    h = h[:m.start()] + body.rstrip("\n") + h[m.end():]

    # ---- header meta ----
    lo = min(p["usd"] for p in prods.values())
    hi = max(p["usd"] for p in prods.values())
    h = re.sub(r'<div class="drop-meta">.*?</div>',
               f'<div class="drop-meta">\n    <span>{READ}</span><span class="dot"></span>'
               f'\n    <span>{nbrands} Brands</span><span class="dot"></span>'
               f'\n    <span>{npicks} Picks</span><span class="dot"></span>'
               f'\n    <span>${lo:,.0f}&ndash;${hi:,.0f}</span>\n  </div>',
               h, count=1, flags=re.S)
    # converge from the original date OR from any earlier run's value — a
    # plain replace of the 2026-06-21 original silently did nothing once a
    # previous run had already written a different date in
    h = re.sub(r'("dateModified":\s*")[^"]*(")',
               lambda m: m.group(1) + "2026-09-23" + m.group(2), h)

    # THE SEARCH SNIPPET, which is the last place the old edit survives. It
    # still sold "14 brands", "barware" and "$14-$945" to anyone seeing the
    # page in results — the one piece of stale copy a reader meets before
    # they ever load the page. Same string is used for description, og and
    # twitter, so all three move together.
    DESC = (f"{npicks} golf home decor picks from {nbrands} brands &mdash; furniture, prints, "
            "coffee gear, leather and two coffee table books. $25&ndash;$1,400, "
            "priced 23 September 2026.")
    n = 0
    for attr in ('name="description"', 'property="og:description"',
                 'name="twitter:description"'):
        h, k = re.subn(r'(<meta ' + re.escape(attr) + r' content=")[^"]*(")',
                       lambda m: m.group(1) + DESC + m.group(2), h)
        n += k
    if n < 2:
        sys.exit(f"! only {n} description tag(s) updated; expected at least 2")

    # ...and the same sentence a third time, inside the Article JSON-LD. Plain
    # text there, not entities: a literal "&mdash;" in structured data is what
    # Google reads out.
    DESC_TXT = (f"{npicks} golf home decor picks from {nbrands} brands - furniture, prints, "
                "coffee gear, leather and two coffee table books. $25-$1,400, "
                "priced 23 September 2026.")
    h, k = re.subn(r'("description":\s*")[^"]*(")',
                   lambda m: m.group(1) + DESC_TXT + m.group(2), h)
    if k < 1:
        sys.exit("! the JSON-LD description was not updated")

    # ---- gallery JS before </body> ----
    h = re.sub(r"<script>[^<]*?pg-track.*?</script>\s*", "", h, flags=re.S)
    h = h.replace("</body>", gal_js + "\n</body>", 1)

    print(f"  cards      : {pid} in {len(GROUPS)} groups")
    print(f"  pull-quotes: {len(PQ)}")
    print(f"  range      : ${lo:,.0f}-${hi:,.0f}")
    if not apply_:
        print("\n  dry run — pass --apply")
        return
    PAGE.write_text(h, encoding="utf-8")
    verify(original, prods, pid)


def verify(original, prods, ncards):
    fin = PAGE.read_text(encoding="utf-8")
    bad = []
    if fin.count(MARK) != 1 or fin.count(END) != 1:
        bad.append("marker block is not present exactly once")
    blk = fin[fin.index(MARK):fin.index(END)]

    if blk.count('class="product-card"') != ncards:
        bad.append(f"{blk.count(chr(34))} and "
                   f"{blk.count('class=' + chr(34) + 'product-card' + chr(34))} cards, "
                   f"expected {ncards}")
    # OLD FORMAT MUST BE GONE
    if "product-img" in blk:
        bad.append("a card still uses the old single-image .product-img format")
    if re.search(r'<a [^>]*class="product-card"', fin):
        bad.append("a card is still an <a> wrapper; buttons cannot nest in a link")
    # gallery wiring
    for dm, body in re.findall(r'data-frames="(\d+)"(.*?)</div><div class="product-body"',
                               blk, re.S):
        if body.count("pg-frame") != int(dm):
            bad.append(f"card says {dm} frames, renders {body.count('pg-frame')}")
        dots = len(re.findall(r'<button class="pg-dot(?: on)?"', body))
        if dots != int(dm):
            bad.append(f"card has {dots} dot buttons for {dm} frames")
        for need in ("pg-arw prev", "pg-arw next", "pg-count"):
            if need not in body:
                bad.append(f"a card is missing {need}")
    if ".product-gallery{" not in fin:
        bad.append("gallery CSS was not added")
    if "pg-track" not in fin.split("</style>")[1].split("<body")[0] and \
            fin.count("pg-track") < 2:
        bad.append("gallery JS is missing")
    if ".pull-quote{" not in fin:
        bad.append("pull-quote CSS was not added")

    # every price and image must match the captured read
    for s, p in prods.items():
        price = f"${p['usd']:,.0f}"
        if f"{html.escape(p['title'])} &middot; {price}" not in blk:
            bad.append(f"{s}: card missing or price disagrees with the read")
        if p["url"] not in blk:
            bad.append(f"{s}: shop link missing")
        if not p["in_stock"] and "Sold out when we checked" not in blk:
            bad.append(f"{s}: sold out but the page does not say so")
    for rel in re.findall(r'src="(/images/home-golf-decor/[^"]+)"', blk):
        if not (ROOT / rel.lstrip("/")).is_file():
            bad.append(f"{rel} not on disk")
    if "cdn.shopify.com" in blk or "squarespace-cdn" in blk:
        bad.append("a hot-linked image survived")

    # The booze is gone. Reported WITH CONTEXT and with the offset, because
    # "booze item survived: decanter" sends you grepping a file that has already
    # been reverted to the version that of course still contains it.
    for gone in ("Decanter", "decanter", "Coaster Set", "Whiskey", "Hip Flask"):
        for mm in re.finditer(re.escape(gone), blk):
            ctx = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ",
                                             blk[max(0, mm.start() - 80):mm.end() + 60]))
            bad.append(f"booze item survived at +{mm.start()}: ...{ctx.strip()}...")
    # quotes attributed
    pq = re.findall(r'<div class="pull-quote-inner">&ldquo;(.*?)&rdquo;'
                    r'<span class="pull-quote-attr">&mdash;\s*(.*?)</span>', fin, re.S)
    if len(pq) != len(PQ):
        bad.append(f"{len(pq)} pull-quotes, expected {len(PQ)}")
    for t, a in pq:
        if not re.search(r"(Jurkschat|Mooty|Gilley)", a):
            bad.append(f"pull-quote not attributed to a named founder: {a[:40]}")
        if fin.count(t[:60]) != 1:
            bad.append(f"pull-quote text is duplicated in the body: {t[:40]}")
    # ONE SIDEBAR, AND NO STALE FIGURES ANYWHERE ON THE PAGE. Scoped to the
    # whole document, not to the new block — the duplicate sidebar and the old
    # lede sat outside it and every block-scoped check waved them through.
    if fin.count('class="sidebar-card"') != 1:
        bad.append(f"{fin.count(chr(34))and fin.count('class=' + chr(34) + 'sidebar-card' + chr(34))} "
                   "sidebars on the page, expected 1")
    for m in re.finditer(r'<meta [^>]*description" content="([^"]*)"', fin):
        d = m.group(1)
        if "12 brands" not in d or "$25" not in d:
            bad.append(f"a description tag still describes the old edit: {d[:70]}")
    if "QUICK LOOK" in fin:
        bad.append("the old QUICK LOOK sidebar survived")
    for stale in ("$945", "fourteen brands", "six categories", "Vagabond",
                  "barware", "$14 Dibdaub", "PrimePutt"):
        if stale in fin:
            ctx = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ",
                         fin[max(0, fin.index(stale) - 80):fin.index(stale) + 70]))
            bad.append(f"stale intro copy survived ({stale}): ...{ctx.strip()}...")

    # house rules
    text = re.sub(r"<[^>]+>", " ", fin)
    if re.search(r"\bworth\b", text, re.I):
        bad.append("the banned word 'worth' is on the page")
    words = len(text.split())
    if words < 1200:
        bad.append(f"{words} words, gate wants 1200")

    if bad:
        PAGE.write_text(original, encoding="utf-8")
        sys.exit("! reverted. " + "\n    ".join(bad))
    print(f"\n  wrote {PAGE.name} — {ncards} cards, {words} words, galleries wired")
    print("\n  FLAGGED:")
    print("    Park Golf Stand is sold out and in the post at Lenny's request;")
    print("    its card says so rather than implying it is buyable.")
    print("    Matchstick's 'Tiger Roar Relief Print' is an illustrated likeness")
    print("    of a living public figure sold by a third party — described by")
    print("    what it is, without asserting who it depicts. Say if you'd rather")
    print("    it came out.")


if __name__ == "__main__":
    main("--apply" in sys.argv)
