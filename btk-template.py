#!/usr/bin/env python3
"""
btk-template.py — the Brand to Know architecture, as code.
18 September 2026.

WHY THIS EXISTS
---------------
Lenny: "Build this as a reusable template so future Brand to Know articles
automatically follow the same system." And, first: "evaluate the existing
components and reuse them wherever possible. The goal is to improve the
architecture and presentation without unnecessarily rebuilding working TGI
components."

So this is a REORDERER, not a generator. It reads a Brand to Know page that
already exists, cuts it into named blocks on markup anchors, and writes the
same blocks back in the house order with three additions. Every product card,
every FAQ answer, every image and both JSON-LD blocks pass through untouched —
this file never writes product copy, because copy nobody checked is the thing
that gets a price wrong in public.

WHAT THE AUDIT FOUND, AND THEREFORE WHAT IS NOT BEING BUILT
------------------------------------------------------------
Almost all of the requested architecture already has a component on this site:

    the ask                     the component that already does it     built?
    ------------------------    -----------------------------------   ------
    kicker + green chip         .drop-tag.grass                        reused
    hero                        .drop-hero / .drop-hero-img            reused
    THE TGI TAKE                .writeup + .writeup-body (2fr/1fr)     reused
    the Brand Card              .sidebar-card + label/detail/cta       reused
    category dividers           .products-section + .products-hdr      reused
    a short annotation          .sec-note   (in the CSS, unused)       reused
    editorial emphasis          .pull-quote / -inner / -attr           reused
    IF YOU LIKE ...             .more-grid / .more-card                reused
    EXPLORE THE INDEX           .more-link                             reused

Three of those classes — .sec-note, .pull-quote, .sidebar-card — were already
in the stylesheet of every Brand to Know page and rendered on none of them.
Nothing here needed a new class, so nothing here has one. The only new markup
is the START HERE list, and it is built out of .products-section, .sec-note
and ordinary anchors.

THE BRAND CARD IS WHERE IT ALREADY LIVES — one deliberate deviation
--------------------------------------------------------------------
The requested flow puts the Brand Card after THE STORY. It is instead in the
sticky .sidebar beside THE TGI TAKE, which is where it sits on all 33 of the
41 Brand to Know pages that render one. Two reasons, both about keeping the
component rather than moving it:

  - .sidebar is `position:sticky;top:80px`. Dropped into the flow as a
    standalone band after The Story it stops being sticky, which is a change
    to its functionality, not its position.
  - From the sidebar it is on screen from the first screenful AND still beside
    the reader at The Story. After The Story it is only ever in one place.

UPDATE, 18 Sep: Lenny picked the J.Lindeberg page as the reference — "I like the
box on the right" — so SIDEBAR_IN_WRITEUP is True and the card sits beside THE
TGI TAKE on every page. The renderer handles both; set it False to put the card
back in the flow as a full-width band.

THE SPEC FILE
-------------
research/btk/<slug>.json supplies only the things a machine cannot know:

    take        the 100-150 word TGI opinion, as paragraphs
    card        the Brand Card rows, CTA and hashtags
    start_here  3-5 picks, each a product-name substring + one short note
    collection  category headings, each with the name substrings it holds
    related     3-4 brand slugs, each with one connective line

START HERE LINKS, IT DOES NOT COPY
-----------------------------------
Constraint 1 is "do not remove products" and constraint 3 is "keep every
existing product option visible". A START HERE that duplicated five product
cards would satisfy both and still be wrong: the same bag twice on one page,
the second time in a grid, is the ecommerce-page feel this redesign is
supposed to avoid. So the picks are a short list that jumps to the card in
THE COLLECTION, and every product stays exactly once, in one place.

USAGE
    python3 btk-template.py hiroki-golf            # dry run, prints the plan
    python3 btk-template.py hiroki-golf --apply
    python3 btk-template.py --all                  # every spec in research/btk
"""
import json, pathlib, re, sys, shutil, datetime

ROOT = pathlib.Path(__file__).resolve().parent
SPECS = ROOT / "research" / "btk"

# See the long note above. False puts the Brand Card in the flow after The Story.
SIDEBAR_IN_WRITEUP = True   # the J.Lindeberg treatment: box on the right

# Sections that are furniture rather than editorial, matched on their h2. They
# keep their own place in the order instead of being swept into THE STORY.
FAQ_H2 = re.compile(r"\bquestions?\b|\bfaq\b", re.I)
COLLECTION_H2 = re.compile(r"\bcollection\b|\bthe lineup\b|\bpieces\b", re.I)

# Lenny: "the write up needs to happen before the products then a second smaller
# write up after the products." The long sections — who they are and what the
# thing is made of — are the piece; the reader should have them before being
# shown eighteen bags. What is left runs after the products as a coda.
CODA_H2 = re.compile(r"\bcollaborations?\b|\bwhat.s next\b|\bthe last word\b", re.I)


# ---------------------------------------------------------------- parsing

# MARKUP ANCHORS ONLY. A bare class name is not safe to search for: on 18 Sep
# 2026 a removal script looked for "more-card", hit the CSS rule .more-card-img
# inside <style>, and truncated a 67KB page to 52KB. Every pattern here carries
# its opening tag, which cannot occur in a stylesheet.
#
# The [^>]* tails are load-bearing: this script stamps data-btk="..." onto the
# sections it generates, so on a SECOND run `<section class="products">` is
# `<section class="products" data-btk="collection">` and an exact-match anchor
# walks straight past it. The closing quote after each class value is what
# keeps "drop-hero" from also matching a "drop-hero-img".
_ANCHOR = re.compile(
    r'<div class="breadcrumb"[^>]*>'
    r'|<header class="drop-header"[^>]*>'
    r'|<section class="drop-hero"[^>]*>'
    r'|<section class="products"[^>]*>'
    r'|<div class="writeup"[^>]*>'
    r'|<div class="btk-card"[^>]*>'
    r'|<section class="more"[^>]*>'
    # Random Golf Club and Siegelman Stable write More from the Feed as a DIV.
    # Same glue problem as the classless section below: not an anchor, so it
    # rode along inside the product block and its four feed thumbnails were
    # dropped. The closing quote keeps this off "more-card" and "more-grid".
    r'|<div class="more"[^>]*>'
    # A CLASSLESS SECTION IS STILL A SECTION. Several pages carry editorial
    # blocks written as <section style="..."> with no class at all — Sentinel's
    # "In the Wild — Basecamp Expedition One" photo grid is one. Without this
    # alternative they are not boundaries, so they ride along glued to the END of
    # the preceding products block; that block is re-split into product cards and
    # everything that is not a card is discarded. Seven Sentinel photographs went
    # that way. Alternation is left-to-right, so the classed patterns above still
    # win at the same position and this only catches what they miss.
    r'|<section[^>]*>'
    r'|<footer')


def split_faq(block):
    """Pull the FAQ out of a block that also holds product cards.

    On most Brand to Know pages the questions live inside the SAME
    <section class="products"> as the catalogue. render_collection rebuilds
    that section from its product cards alone, so anything else in there —
    the entire FAQ, schema-backed and all — would be dropped on the floor.
    Returns (block-without-faq, faq-html-or-None)."""
    i = block.find('<div class="faq">')
    if i < 0:
        return block, None
    # take the heading immediately above it, if there is one
    # Only adopt the heading directly above the FAQ, and only if nothing else
    # lives between them. Taking the nearest h2 unconditionally swallowed eight
    # product cards on Seamus, because that h2 was a category heading.
    h = block.rfind("<h2", 0, i)
    start = i
    if h >= 0 and '<div class="product-card"' not in block[h:i] \
            and '<div class="products-grid"' not in block[h:i]:
        start = h
    depth, j = 0, i
    for m in re.finditer(r"<div\b[^>]*>|</div>", block[i:]):
        depth += 1 if m.group(0).startswith("<div") else -1
        if depth == 0:
            j = i + m.end()
            break
    return block[:start] + block[j:], block[start:j]


def h2_of(block):
    m = re.search(r"<h2[^>]*>(.*?)</h2>", block, re.S)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""


def _nowild(h):
    """The page without our generated gallery — see the prose check."""
    return re.sub(r'<section[^>]*data-btk="wild".*?</section>', " ", h, flags=re.S)


def _words(h):
    """Visible words in the body — script and style stripped out."""
    b = h[h.find("<body"):]
    b = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", b, flags=re.S)
    return len(re.sub(r"<[^>]+>", " ", b).split())


def parse(html):
    """Cut a Brand to Know page into named blocks. Lossless: the concatenation
    of head + every block + tail is the input, byte for byte."""
    # TOP LEVEL ONLY. Several pages nest a <section> inside another one, and a
    # naive anchor list cuts the page in the middle of the outer section: the
    # halves land in different blocks, the reorderer moves them apart, and the
    # document comes out with more <section> than </section>. Takomo went from
    # 8/8 to 11/9 that way and lost 362 words of prose with it. So an anchor only
    # counts as a boundary where the section nesting depth is back to zero.
    depth, marks = 0, []
    for m in re.finditer(r'<section\b[^>]*>|</section>|' + _ANCHOR.pattern, html):
        t = m.group(0)
        if t == "</section>":
            depth = max(0, depth - 1)
            continue
        if _ANCHOR.fullmatch(t) and depth == 0:
            marks.append((m.start(), t))
        if t.startswith("<section"):
            depth += 1
    if not marks:
        raise SystemExit("no section anchors found — is this a Brand to Know page?")

    # the footer anchor ends the body; everything from it is the tail
    foot = next((i for i, (_, t) in enumerate(marks) if t == "<footer"), None)
    if foot is None:
        raise SystemExit("no <footer — refusing to rewrite a page that does not close")

    head, tail = html[:marks[0][0]], html[marks[foot][0]:]
    out = []
    for i in range(foot):
        start = marks[i][0]
        end = marks[i + 1][0]
        out.append((marks[i][1], html[start:end]))
    return head, out, tail


# ---------------------------------------------------------------- stylesheet

# The ONLY new CSS in this redesign, and it is deliberately three selectors.
# START HERE is a numbered list with hairline rules, not a second grid of
# cards: "avoid excessive cards, pills, gradients, shadows or SaaS-style UI."
# .sec-note and .more-card-desc already existed in every Brand to Know
# stylesheet with a font-family and nothing else, so they get a size here and
# keep the family they already had.
CSS_OPEN = "/* btk-template: start-here — generated, edit btk-template.py */"
CSS_SHUT = "/* btk-template: end */"
CSS = CSS_OPEN + """
.start-here{list-style:none;counter-reset:sh;border-top:.5px solid var(--ink)}
.sh-row{counter-increment:sh;display:grid;grid-template-columns:28px 1fr 1.1fr;
  gap:18px;align-items:baseline;padding:14px 0;border-bottom:.5px solid rgba(0,0,0,.18)}
.sh-row::before{content:counter(sh,decimal-leading-zero);font-family:var(--mono);
  font-size:10px;letter-spacing:.1em;opacity:.45}
.sh-name{font-family:var(--serif);font-style:italic;font-size:17px;line-height:1.3;
  border-bottom:1px solid transparent;transition:border-color .15s}
.sh-name:hover{border-bottom-color:var(--ink)}
.sec-note{font-size:14px;line-height:1.6;opacity:.68}
/* An open <details> keeps its marker, so the indicator has to follow state. */
.faq-q[open] summary{margin-bottom:2px}
.faq-q summary{outline:none}
/* the in-body lookbook bands. 21:9 is the masthead; 16:9 in the body discards
   far less of a frame, which is what stopped the crops clipping people's heads.
   object-fit is not optional — without it a fixed aspect-ratio box stretches
   whatever is inside it. */
/* ONE COLUMN, LEFT, WITH THE BOX BESIDE IT.
   Lenny: "move the first box of text to the left so there's room for the box on
   the right." Two columns, the J.Lindeberg layout — and because a page cannot
   have its opening paragraph left-aligned and everything under it centred, the
   WHOLE article column moves left. That is what makes the 34 pages consistent:
   one measure, one left edge, from the Take to the last word of the coda. */
/* NO align-items:start HERE. That was the bug behind "does the box scroll?" —
   it shrink-wrapped the grid row to each item's own height, so the card's
   containing block was the card, and a sticky element with no room to move is
   just an element. Letting the row stretch gives it the full height of the
   write-up to travel against. */
section[data-btk="take"]{display:grid;grid-template-columns:minmax(0,1fr) 300px;
  column-gap:56px;max-width:1400px;margin:0 auto}
section[data-btk="take"] .writeup-body{max-width:760px}
section[data-btk="take"] .sidebar{position:sticky;top:88px;align-self:start}
.btk-story-hdr{margin-top:44px}
@media(max-width:1000px){
  section[data-btk="take"]{grid-template-columns:1fr;row-gap:28px}
  section[data-btk="take"] .sidebar{position:static;max-width:760px}
}

/* THE SPECIAL SENTENCES — larger, and made to stop the eye.
   Lenny, twice: "too small", then "larger and more eyecatching." 38px, the
   brand green on the opening mark, generous air above and below, and a rule
   only under the credit so the sentence itself floats free. */
.pull-quote{max-width:1400px;margin:0 auto;padding:0 32px}
.pull-quote-inner{max-width:900px;margin:0;font-family:var(--serif);
  font-style:italic;font-size:38px;line-height:1.24;letter-spacing:-.015em;
  padding:8px 0 0;position:relative}
.pull-quote-inner:before{content:"\201C";position:absolute;left:-.52em;top:-.18em;
  font-size:2.1em;line-height:1;color:var(--grass,#2f4f2f);opacity:.28}
.pull-quote-attr{display:block;margin-top:24px;padding-top:16px;
  border-top:.5px solid var(--ink);font-family:var(--mono);font-style:normal;
  font-size:10px;letter-spacing:.18em;text-transform:uppercase;opacity:.6;
  max-width:360px}
@media(max-width:820px){
  .pull-quote{padding:0 20px}
  .pull-quote-inner{font-size:26px}
  .pull-quote-inner:before{left:-.3em;font-size:1.6em}
}

/* THE PICTURES, AT THE SHAPE THEY WERE SHOT.
   Lenny: "formatted how they are provided so either landscape or portrait with
   the text wrapped appropriately." So no forced aspect-ratio — the band renders
   at its own proportions, and the template stamps which it is at build time by
   measuring the file. A landscape frame runs the article measure; a portrait
   frame is set narrow and floated so the copy wraps beside it rather than
   leaving a column of empty paper down one side. */
/* THE BUG THAT MADE THESE LOOK BROKEN. The site's base rule is
       .drop-hero-img{width:100%;aspect-ratio:21/9;border:.5px solid var(--ink)}
   and it is written for a DIV that WRAPS a picture. The body bands put that
   class on the IMG element itself, so every one inherited a 21:9 bordered BOX and
   then letterboxed the photograph inside it with object-fit:contain. That is
   exactly what Lenny saw: a visible rectangle, the picture too narrow for it,
   and dead paper down both sides. Undo the container styling first; everything
   below is only meaningful once that is off. */
section.drop-hero:not(:first-of-type) img.drop-hero-img{
  aspect-ratio:auto;border:0;overflow:visible;height:auto}

/* A BREAK, NOT A SLAB. Lenny: "it should just have a smaller break and have
   better design between sections." So the band is sized to sit in a clear
   relationship with the 760px text measure rather than bullying it, is centred
   on the page, and carries its own air above and below so it reads as a
   transition between two sections instead of an object dropped between them. */
section.drop-hero:not(:first-of-type){max-width:1400px;padding:0 32px;
  margin:0 auto;display:flex;justify-content:center}
.drop-hero-img.btk-land{width:100%;max-width:1040px;height:auto;display:block;
  margin:56px auto 60px}
.drop-hero-img.btk-port{width:100%;max-width:520px;height:auto;display:block;
  margin:56px auto 60px}
/* the portrait exception: floated so copy wraps beside it rather than leaving a
   column of empty paper down one side */
section.drop-hero.btk-wrap{max-width:1400px;overflow:hidden;display:block}
section.drop-hero.btk-wrap .drop-hero-img{float:right;margin:4px 0 20px 36px;
  max-width:400px}
@media(max-width:820px){
  section.drop-hero:not(:first-of-type){padding:0 20px}
  .drop-hero-img.btk-land,.drop-hero-img.btk-port{max-width:100%;
    margin:36px auto 40px}
  section.drop-hero.btk-wrap .drop-hero-img{float:none;margin:0 0 20px;
    max-width:100%}
}

/* EVERY SECTION THE SAME WAY — the last two things that gave the set away.
   Measuring the rendered pages turned up two breaks in the rhythm that the
   markup checks could not see:

   1. Headings switched between centred and left depending on whether the
      section happened to carry a data-btk marker. On Walker "The Collection"
      sat centred while "In the Wild" and "Frequently Asked" sat hard left; on
      Après the same split ran down the whole page. Centre them all. The Take
      keeps its left alignment because it shares a column with the Brand Card.
   2. A handful of sections were written with border-top:none inline, so the
      hairline that separates every other section simply wasn't there — the
      missing transition again, in the few places it was hardest to spot.
      An inline style only loses to !important, which is why it is used here. */
section.products .products-hdr{max-width:760px;margin-left:auto;margin-right:auto;
  display:block;width:fit-content}
section[data-btk="take"] .products-hdr{margin-left:0;margin-right:auto}
section.products[style*="border-top:none"]{
  border-top:.5px solid var(--ink) !important;padding-top:40px !important}

/* THE GALLERY. Walker's .ig-grid lives in that page's own <style>, so pages
   that never had one have no rule for it — the generated grid would stack one
   image per row. Restated here, identically, so every page renders it the same. */
.btk-wild-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.btk-wild-grid.n2{grid-template-columns:repeat(2,1fr)}
.btk-wild-grid img{width:100%;aspect-ratio:1/1;object-fit:cover;display:block;
  border:.5px solid var(--ink)}
.btk-wild-credit{font-family:var(--mono);font-size:9px;letter-spacing:.12em;
  text-transform:uppercase;opacity:.45;margin-top:14px}
@media(max-width:820px){.btk-wild-grid{grid-template-columns:repeat(2,1fr);gap:10px}}

/* THE SECTION DECK — the other "special sentence".
   Lenny: "Those sentences pulled out are too small and dont sit right on the
   page." He was looking at <p class="cat-kicker">, NOT .pull-quote — which is
   why the 38px treatment above never reached it. The site default sets it 15px
   with a left rule, so it sat as a small note hard against the left margin
   underneath a CENTRED heading, which is the "doesn't sit right" part. Here it
   is a proper deck: large, centred under its heading, no rule.

   ROMAN, NOT ITALIC. The first pass set these 25px ITALIC, and Lenny: "I find
   this font kinda hard to read." He was right, and the typeface was not the
   problem — Editors Note Text is a display serif whose italic is fine for a
   one-line pull-quote and punishing over five or six centred lines. Body copy
   uses the same face roman at 17px and reads perfectly well. So: roman, a
   shorter measure so lines break sooner, and looser leading.

   AND REGULAR WEIGHT, NOT BOLD. Bold was tried and pulled: the h2 above it is
   already set in the same family at 600, which the family resolves to its 700,
   so a bold deck sat at exactly the heading's weight and the two competed.
   Lenny: "clashes with the title." The hierarchy is carried by size — 21px
   under a 32px heading — which only works while the weights differ. */
section[data-btk] .cat-kicker,
section[data-btk] .sec-intro{font-family:var(--serif);font-style:normal;
  font-weight:400;font-size:21px;line-height:1.6;letter-spacing:0;
  color:var(--ink);opacity:.88;border-left:0;padding:0;max-width:620px;
  margin:0 auto 44px;text-align:center}
/* inside the Take the column is left-aligned, so the deck follows it */
section[data-btk="take"] .cat-kicker,
section[data-btk="take"] .sec-intro{margin-left:0;text-align:left}
@media(max-width:820px){
  section[data-btk] .cat-kicker,
  section[data-btk] .sec-intro{font-size:18px;margin-bottom:32px}
}

/* THE ARTICLE COLUMN. Left, not centred — see the note on the Take above. */
.btk-left{max-width:1400px;margin:0 auto;padding-left:32px;padding-right:32px}
@media(max-width:820px){.btk-left{padding-left:20px;padding-right:20px}}
.products-section{margin-bottom:48px}
.products-section:last-child{margin-bottom:0}

/* THE MEASURE, AND WHEN IT MOVES.
   Lenny's rule: "if there's a box or an image we can push the text to the side
   otherwise let's keep the text centered." So centred is the default — the
   publication setting he asked for originally — and the only sections that go
   left are the ones with something standing beside them: the Take, which
   carries the Brand Card, and any section with a floated picture. */
.btk-measure{max-width:760px;margin-left:auto;margin-right:auto}
section[data-btk] .products-hdr,
section[data-btk] .drop-tag{max-width:760px;margin-left:auto;margin-right:auto;
  display:block;width:fit-content}
section[data-btk="prose"] .writeup-body,
section[data-btk="story"] .writeup-body,
section[data-btk="coda"] .writeup-body{max-width:760px;margin:0 auto}

/* ...and the exception: a section with a box or a picture alongside it sets
   its type to the left, because centred type next to a right-hand box reads as
   a mistake rather than a choice. */
section[data-btk="take"] .writeup-body,
section.btk-wrap .writeup-body{margin:0 auto 0 0}
section[data-btk="take"] .products-hdr,
section[data-btk="take"] .drop-tag{margin-left:0;margin-right:auto}
section[data-btk="take"]{padding-top:34px}
section[data-btk="take"] .writeup-body{font-size:17px}
/* the Brand Card, out of the sticky sidebar and set as a centred block */
/* the masthead, centred with everything else. A left-aligned headline over a
   centred page reads as two designs sharing a screen. */
.drop-header{text-align:center}
.drop-header .drop-meta{justify-content:center}
.drop-header h1{max-width:900px;margin-left:auto;margin-right:auto}
.breadcrumb{text-align:center}
/* START HERE sits between the two measures: wider than the text column because
   it is two columns, narrower than the product grid because it is type. */
.start-here{max-width:1040px;margin-left:auto;margin-right:auto}
.btk-card{max-width:1400px;margin:0 auto;padding:0 32px 8px}
.btk-card .sidebar{position:static;max-width:520px;margin:0 auto}
@media(max-width:820px){
  .btk-card{padding:0 20px 8px}
}
/* THE PROSE SECTIONS. .writeup-body is a 700px measure built for the 2fr
   column of the .writeup grid. Dropped into a full-width .products section it
   keeps that 700px and hugs the left edge under a rule that spans 1400 — half
   the band empty, which reads as broken rather than airy. Centred, with the
   heading centred to match, the full-bleed rule over a narrow measure is a
   deliberate magazine setting instead of a layout mistake. */
.more-card-desc{font-size:13px;line-height:1.5;opacity:.7;margin-top:6px}
@media(max-width:820px){
  .sh-row{grid-template-columns:24px 1fr;gap:6px 14px}
  .sh-row .sec-note{grid-column:2}
}
""" + CSS_SHUT


def ensure_css(head):
    """Idempotent. A second run replaces the block instead of appending one."""
    blk = "\n" + CSS + "\n"
    if CSS_OPEN in head:
        return re.sub(re.escape(CSS_OPEN) + r".*?" + re.escape(CSS_SHUT),
                      lambda _: CSS, head, flags=re.S)
    i = head.rfind("</style>")
    if i < 0:
        raise SystemExit("no </style> in the head — cannot install the stylesheet")
    return head[:i] + blk + head[i:]


# ---------------------------------------------------------------- rendering

# TWO KINDS OF STRING, and mixing them up is how run 2 differed from run 1.
#   ALREADY HTML — the spec file and anything read back off the page. Written
#     with entities on purpose ("The Collection &mdash; 18 Pieces", "Headcovers
#     &amp; Putter Covers"). Passing these through esc() gives &amp;mdash; and
#     the reader sees the entity spelled out.
#   PLAIN TEXT — names and places out of brands.json. These must be escaped.
# esc() is therefore only ever applied to the second kind.
def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def render_writeup(spec, card_html, story_paras=(), story_imgs=()):
    """THE TGI TAKE and THE STORY in one column, the Brand Card sticky beside it.

    Lenny: "Does the box scroll with the page a little? I liked that feature."
    It was not scrolling. position:sticky only travels inside its containing
    block, and with the card alone beside a 110-word Take the grid row was
    SHORTER than the card — zero range, so it just scrolled away like any other
    element. J.Lindeberg's box travels because it sits beside the whole opening
    write-up. So the Take and the Story share one column here and the card has
    something to travel against."""
    paras = "\n".join(f"    <p>{p}</p>" for p in spec["take"])
    body = ('    <div class="drop-tag grass">The TGI Take</div>\n' + paras)
    if story_paras:
        body += ('\n    <h2 class="products-hdr btk-story-hdr">The Story</h2>\n'
                 + "\n".join(f"    {i}" for i in story_imgs)
                 + "\n".join(f"    <p>{p}</p>" for p in story_paras))
    aside = card_html if SIDEBAR_IN_WRITEUP else ""
    return (
        '<section class="products" data-btk="take">\n'
        '  <div class="writeup-body">\n'
        f"{body}\n"
        "  </div>\n"
        f"{aside}"
        "</section>\n\n")


def render_story(spec, imgs=()):
    """The rest of the page's own opening write-up, set as The Story.

    These paragraphs are not new: btk-spec.py took them off the page's existing
    .writeup, which is live and already approved. The first paragraph became the
    Take; everything after it lands here, unchanged."""
    paras = spec.get("story_extra") or []
    if not paras:
        return ""
    body = "\n".join(f"    <p>{x}</p>" for x in paras)
    if imgs:
        body = "\n".join(f"    {i}" for i in imgs) + "\n" + body
    # "story", NOT "prose". They used to share a marker, and on a second run the
    # re-parser could not tell this generated section from a page's own leftover
    # prose: it kept this one AND regenerated it, so the page grew a second "The
    # Story" heading with the same paragraphs under it. Generated sections need
    # names of their own or idempotency is a coin flip.
    return ('<section class="products" data-btk="story">\n'
            '  <h2 class="products-hdr">The Story</h2>\n'
            '  <div class="writeup-body">\n'
            f"{body}\n"
            "  </div>\n"
            "</section>\n\n")


def render_card(spec):
    """The Brand Card, in the markup 33 other Brand to Know pages already use."""
    c = spec["card"]
    rows = "\n".join(
        f'      <div class="sidebar-detail"><span class="l">{k}</span>'
        f"<span>{v}</span></div>"
        for k, v in c["rows"])
    tags = "\n".join(f'        <span class="hashtag">#{t}</span>'
                     for t in c.get("hashtags", []))
    return (
        '  <aside class="sidebar">\n'
        '    <div class="sidebar-card">\n'
        f'      <div class="sidebar-label">{c.get("label", "Details")}</div>\n'
        f"{rows}\n"
        f'      <a href="{c["cta"]["href"]}" target="_blank" rel="noopener" '
        f'class="sidebar-cta">{c["cta"]["text"]}</a>\n'
        '      <div class="hashtags">\n'
        f"{tags}\n"
        "      </div>\n"
        "    </div>\n"
        '  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;'
        "letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;"
        'line-height:1.6;">Some links may earn TGI a commission &mdash; '
        '<a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>\n'
        "  </aside>\n")


def render_start_here(spec, cards):
    """A short editorial list that JUMPS to the card. It does not copy it —
    see the note at the top about why five duplicated product cards would
    satisfy the constraints and still be the wrong page."""
    rows = []
    for pick in spec["start_here"]:
        idx = find_card(cards, pick["match"])
        name = cards[idx]["name"]
        rows.append(
            '      <li class="sh-row">\n'
            f'        <a class="sh-name" href="#p-{idx + 1}">{name}</a>\n'
            f'        <span class="sec-note">{pick["note"]}</span>\n'
            "      </li>")
    return (
        '<section class="products" data-btk="start-here">\n'
        '  <div class="products-section">\n'
        '    <h2 class="products-hdr">Start Here</h2>\n'
        '    <ol class="start-here">\n'
        + "\n".join(rows) + "\n"
        "    </ol>\n"
        "  </div>\n"
        "</section>\n\n")


def render_related(spec, brands):
    """IF YOU LIKE ... — .more-grid and .more-card, pointed at /brands/<slug>
    instead of at posts. Same component, different destination."""
    by = {b["slug"]: b for b in brands}
    cards = []
    for r in spec["related"]:
        b = by.get(r["slug"])
        if not b:
            raise SystemExit(f"related brand not in brands.json: {r['slug']}")
        if not b.get("img"):
            raise SystemExit(f"related brand has no image: {r['slug']}")
        # NO .upper() HERE. .more-card-tag is already text-transform:uppercase
        # in CSS, and uppercasing the string in Python turns "&middot;" into
        # "&MIDDOT;", which is not an entity and prints literally.
        meta = f"{b.get('loc', '')} &middot; {'/'.join(b.get('cats', [])[:2])}"
        cards.append(
            f'    <a class="more-card" href="/brands/{b["slug"]}">\n'
            f'      <div class="more-card-img"><img src="{b["img"]}" '
            f'alt="{esc(b["name"])}" loading="lazy" /></div>\n'
            '      <div class="more-card-body">\n'
            f'        <div class="more-card-name">{esc(b["name"])}</div>\n'
            f'        <div class="more-card-tag">{meta}</div>\n'
            f'        <div class="more-card-desc">{r["why"]}</div>\n'
            "      </div>\n"
            "    </a>")
    return (
        '<section class="more" data-btk="related">\n'
        '  <div class="more-hdr">\n'
        f'    <div class="more-label">If You Like {spec["brand"]}</div>\n'
        '    <a class="more-link" href="/brands">Explore the Brand Index &rarr;</a>\n'
        "  </div>\n"
        '  <div class="more-grid">\n'
        + "\n".join(cards) + "\n"
        "  </div>\n"
        "</section>\n\n")


# ---------------------------------------------------------------- collection

def split_cards(block):
    """Every <div class="product-card"...> in a block, with its name."""
    out, depth, start = [], 0, None
    for m in re.finditer(r'<div class="product-card"[^>]*>|<div\b[^>]*>|</div>', block):
        t = m.group(0)
        if t.startswith('<div class="product-card"'):
            if depth == 0:
                start, depth = m.start(), 1
                continue
        if start is None:
            continue
        depth += 1 if t.startswith("<div") else -1
        if depth == 0:
            html = block[start:m.end()]
            nm = re.search(r'<div class="product-name">(.*?)</div>', html, re.S)
            html = re.sub(r' id="p-\d+"', "", html, count=1)
            out.append({"html": html,
                        "name": re.sub(r"<[^>]+>", "", nm.group(1)).strip() if nm else ""})
            start = None
    return out


def _norm(s):
    import html as _h
    return re.sub(r"\s+", " ", _h.unescape(re.sub(r"<[^>]+>", "", s))).strip().lower()


def find_card(cards, needle, used=None):
    """Exact on normalised text first, substring second, and a name that genuinely
    appears twice (two colourways with one title) is consumed in page order
    rather than treated as an error."""
    used = used if used is not None else set()
    n = _norm(needle)
    exact = [i for i, c in enumerate(cards) if _norm(c["name"]) == n and i not in used]
    if exact:
        return exact[0]
    part = [i for i, c in enumerate(cards)
            if n and n in _norm(c["name"]) and i not in used]
    if part:
        return part[0]
    raise SystemExit(f'"{needle[:60]}" matched no unused product')


def collection_kicker(block):
    """On a FIRST run the section heading is the h2. On a SECOND run that h2 is
    gone — it became the .drop-tag kicker and the h2s below it are category
    names — so read the kicker back rather than promoting "Stand Bags" to the
    title of the whole collection."""
    m = re.search(r'<div class="drop-tag grass">(.*?)</div>', block, re.S)
    if m:
        return re.sub(r"<[^>]+>", "", m.group(1)).strip()
    n = block.count('<div class="product-card"')
    return f"The Collection &mdash; {n} Pieces" if n else "The Collection"


def render_collection(spec, block, cards, pic=None):
    """THE COLLECTION — the same cards, in the same order of appearance,
    grouped under .products-section headings. Nothing is dropped: the count
    is asserted below, and an unassigned card is an error, not a silent loss."""
    hdr = collection_kicker(block)
    used, groups = set(), []
    for g in spec["collection"]:
        idxs = []
        for n in g["match"]:
            i = find_card(cards, n, used)
            used.add(i)
            idxs.append(i)
        idxs.sort()
        groups.append((g["hdr"], idxs))

    # A CARD WITH NO NAME IS NOT A PRODUCT. Forden's section mixes 19 products
    # with 8 caption-only cards (id="det0".."det7") that are detail photographs
    # of the goods — a gallery wearing card markup. They have no name to match a
    # category against, so they read as "products in no category" and stopped the
    # build. They are not dropped and they are not filed under a heading either:
    # they come back as their own strip once the categories are done.
    details = [i for i in range(len(cards))
               if i not in used and not cards[i]["name"].strip()]
    used.update(details)

    missing = [c["name"] for i, c in enumerate(cards) if i not in used]
    if missing:
        raise SystemExit("products in no category (constraint 1 — nothing is "
                         "dropped):\n  " + "\n  ".join(missing))

    # THE PER-CATEGORY COPY. Each category heading on these pages is followed by
    # its own intro paragraph (.cat-kicker on most, .sec-intro on some), and the
    # rebuild kept exactly one of them for the whole collection. Seamus lost
    # three — "Nine covers · $120 to $170 / Driver and fairway covers are the
    # engine of the company..." and two more. They are re-attached to the
    # category they belong to, matched on the heading text.
    _norm = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip().lower()
    kickers = {}
    # ANY paragraph directly under the heading, not just the classed ones.
    # Devereux writes its category intros as a bare <p style="..."> with no
    # class at all, so a pattern keyed on .cat-kicker/.sec-intro missed all six
    # of them. What identifies an intro is its position — first thing after the
    # h2 — not the class someone happened to give it.
    for m in re.finditer(r'<h2[^>]*>(.*?)</h2>\s*(<p[^>]*>.*?</p>)', block, re.S):
        kickers[_norm(m.group(1))] = m.group(2)

    # PULL-QUOTES. A sourced, attributed founder quote sits between categories
    # inside the products block — Akbar Chisti on Seamus, Mike Graham on
    # Gramicci. Splitting the block into cards threw them away. Verbatim quotes
    # from a named person are the last thing on a TGI page that may be lost.
    quotes = re.findall(r'<div class="pull-quote">.*?</div>\s*</div>', block, re.S)

    parts = []
    for name, idxs in groups:
        body = "\n".join(
            # the id is what START HERE jumps to
            cards[i]["html"].replace('<div class="product-card"',
                                     f'<div class="product-card" id="p-{i + 1}"', 1)
            for i in idxs)
        parts.append(
            '  <div class="products-section">\n'
            f'    <h2 class="products-hdr">{name}</h2>\n'
            + (("    " + kickers.pop(_norm(name)) + "\n")
               if _norm(name) in kickers else "")
            + '    <div class="products-grid">\n'
            f"{body}\n"
            "    </div>\n"
            + ("    " + quotes.pop(0) + "\n" if quotes else "")
            + "  </div>\n")
        # a picture between one category and the next, never after the last
        if pic and (name, idxs) != groups[-1]:
            parts.append("</section>\n\n" + pic()
                         + '<section class="products" data-btk="collection-cont">\n')

    # any quote that did not land beside a category still belongs on the page
    if quotes:
        parts.append("".join("  " + q + "\n" for q in quotes))

    # the nameless detail cards, kept together at the end of the collection
    if details:
        parts.append(
            '  <div class="products-section">\n'
            '    <div class="products-grid">\n'
            + "\n".join(cards[i]["html"] for i in details) + "\n"
            "    </div>\n"
            "  </div>\n")

    intro = re.search(r'<p class="sec-intro">.*?</p>', block, re.S)
    return (
        '<section class="products" data-btk="collection">\n'
        f'  <div class="drop-tag grass">{hdr}</div>\n'
        + (("  " + intro.group(0) + "\n") if intro else "")
        + "".join(parts)
        + "</section>\n\n")


# ---------------------------------------------------------------- the order

def bands(slug):
    """The cropped lookbook bands for this brand, hero first."""
    d = ROOT / "images" / slug
    if not d.is_dir():
        return []
    hero = sorted(d.glob("btk-hero.jpg"))
    body = sorted(d.glob("btk-body-*.jpg"),
                  key=lambda p: int(re.search(r"(\d+)", p.stem).group(1)))
    return [f"/images/{slug}/{p.name}" for p in hero + body]


def orientation(src):
    """Landscape or portrait, measured off the actual file.

    Lenny: "formatted how they are provided so either landscape or portrait."
    The template used to force every band into one aspect-ratio box, which meant
    a portrait frame was cropped to a letterbox and a landscape one was cropped
    again. Reading the real dimensions is two lines and removes the guessing."""
    p = ROOT / src.lstrip("/")
    try:
        from PIL import Image
        with Image.open(p) as im:
            w, h = im.size
    except Exception:
        return "land"                     # unreadable: treat as the common case
    return "port" if h > w * 1.08 else "land"


def render_band(src, brand, first=False):
    """Lenny: separate each section with an image. The first is the masthead
    band at 21:9; the rest are 16:9. object-fit on .drop-hero-img is what keeps
    them from stretching — the bug from the first Hiroki build."""
    alt = (f"{brand} lookbook photograph" if not first
           else f"{brand} &mdash; lookbook photograph")
    if first:
        # the masthead keeps its full width and its drama
        return ('<section class="drop-hero">\n'
                f'  <img class="drop-hero-img" src="{src}" alt="{alt}" />\n'
                "</section>\n\n")
    kind = orientation(src)
    return ('<section class="drop-hero">\n'
            f'  <img class="drop-hero-img btk-{kind}" '
            f'src="{src}" alt="{alt}" loading="lazy" />\n'
            "</section>\n\n")


# FRAMES TURNED DOWN FOR THE GALLERY.
# A photograph can be the brand's own, high-resolution and still not editorial.
# Lenny on Hiroki's second tile: "it's just a field" — no product, no person,
# nothing of the brand in it. Listed here rather than deleted, because the file
# is still the page's own photography and may be wanted somewhere else.
WILD_DROP = {"/images/hiroki/jacks-point-1.jpg"}


def wild_frames(slug, html=""):
    """The square frames btk-lookbook.py --squares cut for this brand.

    THE FOLDER IS NOT ALWAYS THE SLUG. Hiroki's page slug is hiroki-golf but its
    pictures live in /images/hiroki/, so looking only under the slug found none,
    the gallery fell below two tiles and the build correctly refused rather than
    drop the page's photographs. Ask the page where its own images are."""
    # ...BUT ONLY THIS BRAND'S FOLDER. Falling back to whatever folder the page
    # mentions most is wrong: every page links four related brands and a feed
    # block, so Forden's gallery came back as Random Golf Club's photographs,
    # Gramicci's as Après Golf's and Jones's as Sun Mountain's — under a credit
    # line naming the wrong brand. A folder qualifies only if its name and the
    # slug are the same thing spelled two ways (hiroki / hiroki-golf).
    dirs = [slug]
    if html:
        body = re.sub(r'<(section|div)[^>]*class="more".*?</\1>', " ", html, flags=re.S)
        body = re.sub(r'<section[^>]*data-btk="related".*?</section>', " ", body, flags=re.S)
        for d in dict.fromkeys(re.findall(r'src="/images/([^/"]+)/', body)):
            if d == slug or d.startswith(slug) or slug.startswith(d):
                dirs.append(d)
    for d in dict.fromkeys(dirs):
        out = [f"/images/{d}/ig-{n}.jpg" for n in range(1, 7)]
        got = [s for s in out if (ROOT / s.lstrip("/")).exists()]
        if got:
            return got
    return []


def wild_title(html):
    """"In the Wild" unless the page already uses it for something else.

    Rouqe Golf names a PRODUCT CATEGORY "In the Wild", so titling the gallery
    that put two identical h2s on the page. Take the first title that is free."""
    have = {re.sub(r"<[^>]+>", "", h).strip().lower()
            for h in re.findall(r"<h2[^>]*>(.*?)</h2>", html, re.S)}
    for t in ("In the Wild", "The Lookbook", "On Course", "The Photographs"):
        if t.lower() not in have:
            return t
    return "The Photographs"


def render_wild(srcs, brand, title="In the Wild"):
    """WALKER'S SECTION, WHICH IS THE ONE THAT WORKS.

    Lenny, looking at Hiroki and Hidden Links: "there's no transition and the
    formatting sucks" — then, pointing at Walker: "I want all the brands to know
    pages and the brands revisited pages to follow similar designs."

    Measuring the two explains it exactly. Every section on Walker is separated
    the same way — a hairline rule, 40px of air, a heading — and its photographs
    live TOGETHER in one gallery under a heading of their own. The other pages
    splice lone photographs between sections with no rule, no padding and no
    heading, so the picture interrupts the page instead of dividing it. That
    missing rule IS the missing transition.

    So the body bands are gone and this takes their place: one gallery, in the
    same slot on every page, built like Walker's."""
    if not srcs:
        return ""
    cells = "\n".join(
        f'    <img src="{s}" alt="{esc(brand)} on course &mdash; lookbook photograph" '
        f'loading="lazy" />' for s in srcs)
    n2 = " n2" if len(srcs) == 2 else ""
    return (f'<section class="products" data-btk="wild">\n'
            f'  <h2 class="products-hdr">{title}</h2>\n'
            f'  <div class="ig-grid btk-wild-grid{n2}">\n{cells}\n  </div>\n'
            f'  <p class="btk-wild-credit">Photography courtesy of {esc(brand)}</p>\n'
            f'</section>\n\n')


def build(slug, apply_=False):
    spec = json.loads((SPECS / f"{slug}.json").read_text(encoding="utf-8"))
    page = ROOT / "drops" / spec["page"]
    html = page.read_text(encoding="utf-8")
    brands = json.loads((ROOT / "data" / "brands.json").read_text(encoding="utf-8"))
    brands = brands["brands"] if isinstance(brands, dict) else brands

    head, blocks, tail = parse(html)

    crumb = header = collection = None
    heroes, story, coda, faq, more = [], [], [], None, None
    writeup_imgs = []
    wild_template, wild_curated = [], []
    already_merged = False
    for tag, b in blocks:
        if tag.startswith('<div class="breadcrumb"'):
            crumb = b
        elif tag.startswith("<header"):
            header = b
        elif tag.startswith('<section class="drop-hero"'):
            heroes.append(b)
        elif tag.startswith('<section class="more"') or tag.startswith('<div class="more"'):
            # ...unless it is OUR related block from a previous run. That block
            # is regenerated from the spec, and letting it land here would
            # overwrite the page's real More from the Feed with a copy of
            # something we are about to rebuild anyway.
            if 'data-btk=' not in b[:120]:
                more = b
        elif tag.startswith('<div class="writeup"') or tag.startswith('<div class="btk-card"'):
            # Rebuilt from the spec — but the spec holds TEXT only, so an image
            # set inside the write-up (Devereux opens with a .writeup-img of a
            # polo collar) would be dropped with the rest of the block. Keep any
            # such image and hand it to The Story.
            writeup_imgs.extend(re.findall(r'<img class="writeup-img"[^>]*>', b))
            # ...and the founder quote, for the same reason. Gramicci's Mike
            # Graham and Metalwood's Cole Young both sit in a .pull-quote inside
            # the write-up, which the spec (paragraphs only) cannot carry.
            writeup_imgs.extend(
                re.findall(r'<div class="pull-quote">.*?</div>\s*</div>', b, re.S))
        else:
            mark = re.search(r'data-btk="([a-z-]+)"', b[:120])
            # RESCUE BEFORE REGENERATING. The Story section is rebuilt from the
            # spec, but on the FIRST run it was given things the spec does not
            # hold: the write-up's own image and its founder pull-quote, lifted
            # out of a block that was about to be dropped. On a SECOND run those
            # now live inside this generated section, and dropping it threw them
            # away again — Devereux lost its collar photograph, Birds of Condor
            # lost Frankie Kimpton's quote. Take them back out before it goes.
            # OUR OWN GALLERY, ON A RE-RUN. It is regenerated, so it is dropped
            # here — but it holds two different kinds of picture and they must
            # be treated differently. The ig-N.jpg squares this template cut are
            # template output and may vanish. Anything else in there was a
            # CURATED photograph promoted into the gallery on an earlier run
            # (Hiroki's leather-detail.jpg and jacks-point-1.jpg), and losing
            # those would be losing the page's own photography.
            if mark and mark.group(1) == "wild":
                for s in re.findall(r'<img[^>]+src="([^"]+)"', b):
                    (wild_template if re.search(r"/ig-\d+\.jpg$", s)
                     else wild_curated).append(s)
                continue
            if mark and mark.group(1) in ("story", "take"):
                writeup_imgs.extend(re.findall(r'<img class="writeup-img"[^>]*>', b))
                writeup_imgs.extend(
                    re.findall(r'<div class="pull-quote">.*?</div>\s*</div>', b, re.S))
                continue
            # A native Story we already merged into keeps its own marker so a
            # later run neither drops it nor injects the spec paragraphs twice.
            if mark and mark.group(1) == "story-native":
                story.append(b)
                already_merged = True
                continue
            # (A migration rule lived here that dropped any data-btk="prose"
            # block headed "The Story", on the assumption it was our own output
            # from before The Story got its own marker. Every page has since been
            # rebuilt, so the generated one now carries data-btk="story" and is
            # handled above — which left this rule matching nothing but NATIVE
            # Story sections, and deleting them. Bluegrass Fairway lost 430 words
            # and both Matt Reynolds interviews to it. A migration that has
            # finished migrating is not neutral; it is a live grenade.)
            if mark and mark.group(1) in ("prose", "coda"):
                (coda if mark.group(1) == "coda" else story).append(b)
                continue
            if mark:
                # our own output from a previous run. The collection is kept and
                # re-split; everything else we generated is dropped and rebuilt,
                # which is what makes a second run a no-op instead of a double.
                # PREFIX, AND ACCUMULATE. render_collection emits one section
                # per category: the first is data-btk="collection", the rest
                # are data-btk="collection-cont". An equality test matched only
                # the first and silently dropped the others, so a second run on
                # Seamus saw 9 of its 23 cards. It refused to write rather than
                # publish a page missing 14 products — the guard doing its job,
                # but the bug is here. Both halves matter: the prefix finds the
                # continuations, the += keeps them all.
                if mark.group(1).startswith("collection"):
                    collection = (collection or "") + b
                # The FAQ is LIFTED, not regenerated — there is nothing in the
                # spec to rebuild it from. On a second run it arrives already
                # wrapped in its own marked section, and dropping it here (as
                # every other marked block is dropped) deleted the whole FAQ.
                elif mark.group(1) == "faq":
                    faq = b
                continue
            h = h2_of(b)
            # ONLY on a block that also holds products. Run against the FAQ's
            # own section it empties that section, and the classifier below then
            # overwrites the good extraction with the empty remainder — which is
            # exactly how the Hiroki rebuild lost its FAQ.
            if '<div class="product-card"' in b:
                b, got_faq = split_faq(b)
            else:
                got_faq = None
            if got_faq and not faq:
                faq = ('<section class="products" data-btk="faq">\n'
                       + got_faq + "\n</section>\n\n")
            if '<div class="product-card"' in b:
                collection = (collection or "") + b
            # THE FAQ IS THE ACCORDION, NOT EVERY BLOCK THAT SAYS "FAQ".
            # These pages carry TWO blocks matching the heading pattern: the
            # schema-backed <div class="faq"> accordion, and a separate prose
            # section headed "The Story — FAQ" that is ordinary editorial
            # writing (and on Gramicci, Quiet Golf and Huega House also holds
            # the founder's pull-quote). Assigning faq on the heading alone let
            # the second overwrite the first, and whichever lost went in the
            # bin — 492 words on Metalwood, 438 on Odd Ritual. The accordion is
            # identified by its own markup; a heading match with no accordion
            # anywhere on the page still counts, for older pages that predate it.
            elif '<div class="faq"' in b or (
                    FAQ_H2.search(h) and '<div class="faq"' not in html):
                faq = b
            elif CODA_H2.search(h):
                coda.append(b)
            else:
                story.append(b)

    if not collection:
        raise SystemExit("no product cards found anywhere on the page")
    cards = split_cards(collection)
    n_before = html.count('<div class="product-card"')
    if len(cards) != n_before:
        raise SystemExit(f"card parser saw {len(cards)} of {n_before}")

    def mark_prose(blocks, kind):
        """Stamp the prose sections so the centring rule finds them — and only
        them. The product grid must stay full width."""
        return [b if 'data-btk=' in b[:120]
                else b.replace('<section class="products">',
                               f'<section class="products" data-btk="{kind}">', 1)
                for b in blocks]

    card_html = render_card(spec)

    # THE LEGACY MASTHEAD. 40 of the 41 Brand to Know pages open with
    #     <div class="drop-hero"><div class="drop-hero-img"><img ...></div></div>
    # and it is a DIV, not a <section>, so parse() never split it off — it rides
    # along inside the header block. The template then appended its own 21:9 band
    # directly beneath it and the page opened with two photographs stacked, no
    # type between them. Invisible in the section scan (which looks for
    # <section class="drop-hero">), obvious the moment you look at the render.
    #
    # The band replaces it, so it is removed — but ONLY when there is a band to
    # replace it with. A brand whose harvest came up empty keeps the one picture
    # it has rather than losing its masthead entirely.
    dropped_imgs = set()
    legacy_hero = re.search(
        r'\s*<div class="drop-hero">\s*<div class="drop-hero-img">.*?</div>\s*</div>',
        header or "", re.S)
    if legacy_hero and bands(slug):
        dropped_imgs = set(re.findall(r'<img[^>]+src="([^"]+)"', legacy_hero.group(0)))
        header = header[:legacy_hero.start()] + header[legacy_hero.end():]

    # DOES THIS PAGE ALREADY HAVE A PHOTO GALLERY OF ITS OWN?
    # .ig-grid is also what the related-brands block uses, so a bare search for
    # the class says yes on every page. A native gallery is one that is neither
    # ours (data-btk="wild") nor the related block (.more).
    # ...and .ig-grid is not the only way a page builds one. Après, Fyfe, Rouqe
    # and TwentyFour each hand-rolled a grid class of their own under an "In the
    # Wild" heading, so a class-only test said no and the template emitted a
    # SECOND section with the same heading. Detect the heading as well.
    def _is_gallery(s):
        if 'data-btk="wild"' in s or 'class="more"' in s:
            return False
        # A HEADING IS NOT A GALLERY. Rouqe Golf names a PRODUCT CATEGORY "In
        # the Wild" — thirteen product cards under it — and a heading-only test
        # read that as a gallery, so the page got none at all. Photographs, not
        # products: a section holding product cards is never the gallery.
        if 'class="product-card"' in s or 'data-btk="collection' in s:
            return False
        if "ig-grid" in s:
            return True
        return (re.search(r"<h2[^>]*>\s*(In the Wild|On Course|The Craft|The Lookbook)", s)
                and len(re.findall(r"<img", s)) >= 3)
    _has_native_wild = any(
        _is_gallery(s) for s in re.findall(r"<section\b.*?</section>", html, re.S))

    parts = [ensure_css(head), crumb, header]

    # THE PHOTOGRAPHS. Lenny: "let's always separate each section with an
    # image." bands(slug) returns the crops btk-lookbook.py made, hero first.
    # They are spent in order and never repeated: when a brand's harvest runs
    # out the remaining joins simply have no picture, which is honest, where
    # showing the same photograph twice would read as padding.
    pics = bands(slug) or [
        # a page that already had heroes of its own keeps them
        m.group(1) for b in heroes
        for m in [re.search(r'src="([^"]+)"', b)] if m]
    pics = list(dict.fromkeys(pics))

    def band():
        return render_band(pics.pop(0), spec["brand"], first=not band.used) \
            if pics and not setattr(band, "used", True) else ""
    band.used = False

    # WHICH JOINS GET A PICTURE WHEN THERE AREN'T ENOUGH TO GO ROUND.
    #
    # pic() used to pop greedily in reading order, so a brand with two frames
    # spent both at the top. Hidden Links Society has a FOUR-part write-up (the
    # Take, the Story, The Public 100 Project, Where the 2% Goes) and exactly two
    # photographs: one became the masthead, the second landed between the Take
    # and the Story — cutting the argument in half after one paragraph — and the
    # entire 18-piece collection then ran with no break at all.
    #
    # A join inside continuous prose is the LEAST useful place for a scarce
    # picture and the most damaging: it reads as an interruption. The most
    # useful is where the page changes mode, from reading to browsing. So when
    # there are fewer frames than joins, they are spent by rank, not by order:
    #
    #   0  the masthead
    #   1  the write-up ending and the products starting
    #   2  between one product category and the next
    #   3  after the coda
    #   4  inside the write-up
    #
    # With enough frames every join still gets one and nothing changes.
    RANK = {"masthead": 0, "precollection": 1, "category": 2, "coda": 3, "writeup": 4}
    n_cat_joins = max(0, len(spec.get("collection", [])) - 1)
    kinds = (["masthead", "writeup", "precollection"]
             + (["precollection"] if spec.get("start_here") else [])
             + ["category"] * n_cat_joins + ["coda"])
    # (document order, kind) — the order index is the unique key, so no id() games
    joins = list(enumerate(kinds))
    chosen = {n for n, _ in sorted(joins, key=lambda j: (RANK[j[1]], j[0]))[:len(pics)]}
    _seq = list(joins)

    def pic(first=False, kind="category"):
        """Emit a band at this join only if this join earned one.

        ONLY THE MASTHEAD NOW. The body joins used to get a lone photograph each;
        see render_wild for why that is gone. Keeping the machinery rather than
        deleting it means the masthead still picks the best frame by the same
        rules, and the ranking comment below still documents a real decision."""
        if not pics or kind != "masthead":
            return ""
        for j in _seq:                      # next unconsumed join of this kind
            if j[1] == kind:
                _seq.remove(j)
                if j[0] not in chosen:
                    return ""
                return render_band(pics.pop(0), spec["brand"], first=first)
        return ""

    # THE READING ORDER, with a picture at every join.
    parts.append(pic(first=True, kind="masthead"))      # masthead band
    # The Story rides in the same column as the Take so the Brand Card beside
    # them has something to stay level with as the reader scrolls.
    # ...unless the page already has a Story section of its own (Bluegrass
    # Fairway does). Emitting our heading as well gave it two "The Story"s.
    _has_native_story = any(re.search(r"<h2[^>]*>\s*The Story\s*</h2>", b)
                            for b in story)
    _story_in_take = ((spec.get("story_extra") or [])
                      if SIDEBAR_IN_WRITEUP and not _has_native_story else [])
    parts.append(render_writeup(spec, card_html, _story_in_take, writeup_imgs))
    parts.append(pic(kind="writeup"))
    # THE NATIVE "THE STORY". Bluegrass Fairway already has a section headed
    # The Story of its own, so emitting ours beside it gave the page two
    # identical headings. Both bodies are real copy and neither may be dropped,
    # so they are merged: our paragraphs go into the top of the page's own
    # section and no second one is emitted.
    native_story = next(
        (i for i, b in enumerate(story)
         if re.search(r"<h2[^>]*>\s*The Story\s*</h2>", b)), None)
    if _story_in_take:
        pass                    # already emitted beside the Brand Card, above
    elif already_merged:
        pass                    # the paragraphs are already in the page's own Story
    elif native_story is not None and spec.get("story_extra"):
        b = story[native_story]
        k = b.find("</h2>") + len("</h2>")
        body = "\n".join(f"    {i}" for i in writeup_imgs) \
            + "\n".join(f"    <p>{x}</p>" for x in spec["story_extra"])
        b = (b[:k] + '\n  <div class="writeup-body">\n'
             + body + "\n  </div>\n" + b[k:])
        # STAMP IT. Without a marker of its own this merged section reads on the
        # next run as an ordinary prose block headed "The Story", which the
        # migration rule drops — taking the page's native story with it.
        # Bluegrass Fairway lost 430 words that way, including both Matt
        # Reynolds interviews.
        # Stamp whether or not the section already carries a marker. A plain
        # string replace of '<section class="products">' matched nothing once an
        # earlier run had stamped it data-btk="prose", so the stamp silently
        # failed and the spec paragraphs were injected again on every run —
        # Bluegrass grew by 778 characters a pass.
        if re.search(r'<section[^>]*data-btk="[a-z-]+"', b[:160]):
            b = re.sub(r'(<section[^>]*)data-btk="[a-z-]+"',
                       r'\1data-btk="story-native"', b, count=1)
        else:
            b = b.replace('<section class="products"',
                          '<section class="products" data-btk="story-native"', 1)
        story[native_story] = b
    else:
        parts.append(render_story(spec, writeup_imgs))   # the main write-up
    parts.extend(mark_prose(story, "prose"))            # any other prose sections
    if not SIDEBAR_IN_WRITEUP:
        parts.append('<div class="btk-card">\n' + card_html + "</div>\n\n")
    # THE RETIRED BODY BANDS. Only the btk-body-N crops this template made are
    # exempt from the image check — named literally, so a real photograph going
    # missing still fails. Hiroki proved why that matters: its body bands were
    # not template crops at all but two curated originals (leather-detail.jpg,
    # jacks-point-1.jpg), and a looser exemption would have deleted them.
    dropped_imgs |= {s for s in re.findall(r'<img[^>]+src="([^"]+)"', html)
                     if re.search(r"/btk-body-\d+\.jpg$", s)}
    # ...and the curated ones are not dropped, they are PROMOTED: a photograph
    # the page already chose leads the gallery, with generated squares filling
    # in behind it.
    dropped_imgs |= set(wild_template)      # template squares may come and go
    dropped_imgs |= WILD_DROP               # ...and so may a turned-down frame
    _own = [s for s in wild_curated if s not in WILD_DROP] + [
        m.group(1) for b in heroes[1:]
        for m in [re.search(r'<img[^>]+src="([^"]+)"', b)]
        if m and not re.search(r"/btk-(hero|body-\d+)\.jpg$", m.group(1))
        and m.group(1) not in WILD_DROP]
    # THE GALLERY, in Walker's slot: after the reading, before the browsing.
    # A page that already has a gallery of its own (Devereux, Manors, Mogshade,
    # Radry, Read The Green, Takomo, Walker) keeps it — generating a second one
    # would put two photo grids on the same page, which is the inconsistency
    # this is meant to remove, not a fix for it.
    if not _has_native_wild:
        _g = list(dict.fromkeys(_own + wild_frames(slug, html)))
        # Three across, so 6 or 3 — never a hanging last tile. TWO is allowed as
        # its own two-across row: Hiroki has exactly two curated photographs and
        # no lifestyle harvest, and the alternative was dropping them.
        _g = (_g[:6] if len(_g) >= 6 else _g[:3] if len(_g) >= 3
              else _g[:2] if len(_g) == 2 else [])
        parts.append(render_wild(_g, spec["brand"], wild_title(html)))
    parts.append(pic(kind="precollection"))
    if spec.get("start_here"):
        parts.append(render_start_here(spec, cards))
        parts.append(pic(kind="precollection"))
    # THE COLLECTION, with a picture between each category
    parts.append(render_collection(spec, collection, cards, pic))
    parts.extend(mark_prose(coda, "coda"))              # the shorter write-up
    parts.append(pic(kind="coda"))
    if faq:
        parts.append(faq)
    parts.append(render_related(spec, brands))
    if more:
        parts.append(more)
    parts.append(tail)
    out = "".join(p for p in parts if p)

    # THE FAQ IS OPEN. Lenny: "automatically expand all the FAQ sections so we're
    # not clicking to expand." <details open> shows the answer on load and keeps
    # the disclosure triangle working, so a reader can still collapse one. It
    # also means the answers are in the rendered text for anyone — or anything —
    # reading the page without running the click.
    out = re.sub(r'<details(?![^>]*\bopen\b)([^>]*class="faq-q")', r'<details open\1', out)
    out = re.sub(r'<details(?![^>]*\bopen\b)(\s*>)', r'<details open\1', out)

    # ---- assertions. A reorderer that loses things is worse than no reorderer.
    checks = [
        ("every product card survived",
         out.count('<div class="product-card"') == n_before, f"{n_before}"),
        ("every product link survived",
         out.count('class="product-link"') == html.count('class="product-link"'), ""),
        # by src, not by count: IF YOU LIKE legitimately ADDS four brand
        # thumbnails, so a raw == here fails a correct render. What has to hold
        # is that nothing arrived without leaving.
        # ...with ONE deliberate exception: the legacy masthead the 21:9 band
        # replaces. dropped_imgs holds exactly that one src and nothing else, so
        # this stays a real check rather than a loosened one.
        ("every image survived",
         set(re.findall(r'<img[^>]+src="([^"]+)"', html)) - dropped_imgs
         <= set(re.findall(r'<img[^>]+src="([^"]+)"', out)),
         f"{html.count('<img')} in, {out.count('<img')} out"),
        ("both JSON-LD blocks survived",
         out.count("application/ld+json") == html.count("application/ld+json"), ""),
        ("FAQ block intact",
         out.count('<div class="faq">') == html.count('<div class="faq">'), ""),
        ("document closes", "</body>" in out and "</html>" in out and "<footer" in out, ""),
        # THE CHECK THAT WAS MISSING. Every assertion above counts THINGS —
        # cards, links, images, schema blocks. None of them counts WORDS, so a
        # run could drop whole paragraphs of prose and still report eleven
        # greens. Takomo lost 362 words and Gramicci 85 before this existed, and
        # both went live until verify-post caught them afterwards. A reorderer
        # must not lose sentences either.
        # Counted with OUR OWN gallery stripped from both sides. Its heading and
        # credit line are template chrome that legitimately appears or vanishes
        # as a page gains or loses a generated gallery, and that 8-word swing
        # read as lost editorial copy. Every real paragraph is still counted.
        ("no prose lost", _words(_nowild(out)) >= _words(_nowild(html)),
         f"{_words(_nowild(html))} in, {_words(_nowild(out))} out"),
        ("section tags balance",
         out.count("<section") == out.count("</section>"),
         f"{out.count('<section')}/{out.count('</section>')}"),
        ("no duplicated h2",
         len(set(re.findall(r'<h2[^>]*>(.*?)</h2>', out, re.S)))
         == len(re.findall(r'<h2[^>]*>(.*?)</h2>', out, re.S)), ""),
        # run 1 shipped "The Collection &amp;mdash; 18 Pieces", which renders
        # as the entity spelled out on the page. Cheap to test for, invisible
        # in a byte count, and only noticed because run 2 escaped it again.
        # Only NEW damage. This page already carried one double-escape in a
        # More-from-the-Feed alt attribute before any of this ran, and a
        # reorderer has no business quietly rewriting a neighbouring section's
        # content on its way past.
        ("no NEW double-escaped entities",
         len(re.findall(r"&amp;(?=[a-z]{2,8};|#\d)", out))
         <= len(re.findall(r"&amp;(?=[a-z]{2,8};|#\d)", html)), ""),
        ("exactly one Brand Card",
         out.count('<div class="sidebar-card">') == 1,
         str(out.count('<div class="sidebar-card">'))),
        # COUNT MARKUP, NOT TEXT. The first version of this check counted
        # every occurrence of data-btk="take" and reported 4, because the
        # stylesheet above mentions the selector three times. A check that
        # cries wolf gets switched off, so it counts opening tags only.
        ("exactly one of each generated section",
         all(len(re.findall(r'<(?:section|div)[^>]*data-btk="' + k + '"', out)) == 1
             for k in (("take", "start-here", "collection", "related")
                       if spec.get("start_here") else
                       ("take", "collection", "related"))),
         ", ".join(k + "=" + str(len(re.findall(r'<(?:section|div)[^>]*data-btk="' + k + '"', out)))
                   for k in ("take", "start-here", "collection", "related"))),
        ("start-here anchors resolve",
         all(f'id="p-{i}"' in out
             for i in [int(x) for x in re.findall(r'href="#p-(\d+)"', out)]), ""),
    ]
    bad = [c for c in checks if not c[1]]
    for name, ok, extra in checks:
        print(f"  {'ok  ' if ok else 'FAIL'} {name}" + (f"  ({extra})" if extra else ""))
    if bad:
        raise SystemExit("\nrefusing to write — see failures above")

    print(f"\n  {len(html):,} -> {len(out):,} bytes    "
          f"{len(cards)} products in {len(spec['collection'])} categories, "
          f"{len(spec.get('start_here') or [])} picks, {len(spec['related'])} related brands")

    if apply_:
        # NOT next to the page. Anything left in drops/ ships to Vercel, and a
        # .orig of a live post is a duplicate of that post on the public site.
        bakdir = SPECS / "backups"; bakdir.mkdir(parents=True, exist_ok=True)
        bak = bakdir / (page.stem + ".pre-template.html")
        if not bak.exists():          # the pre-template page, kept once
            shutil.copy2(page, bak)
        page.write_text(out, encoding="utf-8")
        print(f"  wrote {page.name}   (original kept as {bak.name})")
    else:
        print("\n  dry run — pass --apply to write")
    return out


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    apply_ = "--apply" in sys.argv
    slugs = ([p.stem for p in sorted(SPECS.glob("*.json"))]
             if "--all" in sys.argv else args)
    if not slugs:
        raise SystemExit(__doc__.strip().split("USAGE")[-1])
    # --all must not stop at the first page that refuses. A page that fails its
    # checks is left exactly as it was and named at the end; the rest still get
    # built. Stopping the batch would leave the site half-converted.
    done, failed = [], []
    for s in slugs:
        print(f"\n=== {s}")
        try:
            build(s, apply_)
            done.append(s)
        except SystemExit as e:
            print(f"  -- skipped: {e}")
            failed.append((s, str(e).strip().splitlines()[0][:70]))
    if len(slugs) > 1:
        print(f"\n{'='*60}\n  built {len(done)}   skipped {len(failed)}")
        for s, why in failed:
            print(f"    {s:<26} {why}")
