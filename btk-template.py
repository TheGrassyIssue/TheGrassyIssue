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

Say the word and SIDEBAR_IN_WRITEUP = False moves it; the renderer already
handles both.

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
SIDEBAR_IN_WRITEUP = False

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
    r'|<footer')


def h2_of(block):
    m = re.search(r"<h2[^>]*>(.*?)</h2>", block, re.S)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else ""


def parse(html):
    """Cut a Brand to Know page into named blocks. Lossless: the concatenation
    of head + every block + tail is the input, byte for byte."""
    marks = [(m.start(), m.group(0)) for m in _ANCHOR.finditer(html)]
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

/* THE MEASURE. Lenny: "all the wording to be more centered and read more like
   a publication." One column, one width, centred, used by every piece of
   running text on the page — the Take, both write-ups, the Start Here list and
   the section headings over the product grid. The grid itself stays full
   width; a magazine sets its pictures wide and its type narrow. */
.btk-measure{max-width:760px;margin-left:auto;margin-right:auto}
section[data-btk] .products-hdr,
section[data-btk] .drop-tag{max-width:760px;margin-left:auto;margin-right:auto;
  display:block;width:fit-content}
section[data-btk="prose"] .writeup-body,
section[data-btk="take"] .writeup-body{max-width:760px;margin:0 auto}
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


def render_writeup(spec, card_html):
    """.writeup — THE TGI TAKE, with the Brand Card in its sticky sidebar."""
    paras = "\n".join(f"    <p>{p}</p>" for p in spec["take"])
    aside = card_html if SIDEBAR_IN_WRITEUP else ""
    return (
        '<section class="products" data-btk="take">\n'
        '  <div class="writeup-body">\n'
        '    <div class="drop-tag grass">The TGI Take</div>\n'
        f"{paras}\n"
        "  </div>\n"
        f"{aside}"
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


def find_card(cards, needle):
    hits = [i for i, c in enumerate(cards) if needle.lower() in c["name"].lower()]
    if len(hits) != 1:
        raise SystemExit(
            f'"{needle}" matched {len(hits)} products — make it unique.\n  '
            + "\n  ".join(cards[i]["name"] for i in hits))
    return hits[0]


def collection_kicker(block):
    """On a FIRST run the section heading is the h2. On a SECOND run that h2 is
    gone — it became the .drop-tag kicker and the h2s below it are category
    names — so read the kicker back rather than promoting "Stand Bags" to the
    title of the whole collection."""
    m = re.search(r'<div class="drop-tag grass">(.*?)</div>', block, re.S)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else h2_of(block)


def render_collection(spec, block, cards):
    """THE COLLECTION — the same cards, in the same order of appearance,
    grouped under .products-section headings. Nothing is dropped: the count
    is asserted below, and an unassigned card is an error, not a silent loss."""
    hdr = collection_kicker(block)
    used, groups = set(), []
    for g in spec["collection"]:
        idxs = sorted(find_card(cards, n) for n in g["match"])
        for i in idxs:
            if i in used:
                raise SystemExit(f"product in two categories: {cards[i]['name']}")
            used.add(i)
        groups.append((g["hdr"], idxs))

    missing = [c["name"] for i, c in enumerate(cards) if i not in used]
    if missing:
        raise SystemExit("products in no category (constraint 1 — nothing is "
                         "dropped):\n  " + "\n  ".join(missing))

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
            '    <div class="products-grid">\n'
            f"{body}\n"
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

def build(slug, apply_=False):
    spec = json.loads((SPECS / f"{slug}.json").read_text(encoding="utf-8"))
    page = ROOT / "drops" / spec["page"]
    html = page.read_text(encoding="utf-8")
    brands = json.loads((ROOT / "data" / "brands.json").read_text(encoding="utf-8"))
    brands = brands["brands"] if isinstance(brands, dict) else brands

    head, blocks, tail = parse(html)

    crumb = header = collection = None
    heroes, story, coda, faq, more = [], [], [], None, None
    for tag, b in blocks:
        if tag.startswith('<div class="breadcrumb"'):
            crumb = b
        elif tag.startswith("<header"):
            header = b
        elif tag.startswith('<section class="drop-hero"'):
            heroes.append(b)
        elif tag.startswith('<section class="more"'):
            more = b
        elif tag.startswith('<div class="writeup"') or tag.startswith('<div class="btk-card"'):
            pass                      # a previous run's — rebuilt from the spec
        else:
            mark = re.search(r'data-btk="([a-z-]+)"', b[:120])
            if mark and mark.group(1) in ("prose", "coda"):
                (coda if mark.group(1) == "coda" else story).append(b)
                continue
            if mark:
                # our own output from a previous run. The collection is kept and
                # re-split; everything else we generated is dropped and rebuilt,
                # which is what makes a second run a no-op instead of a double.
                if mark.group(1) == "collection":
                    collection = b
                continue
            h = h2_of(b)
            if COLLECTION_H2.search(h):
                collection = b
            elif FAQ_H2.search(h):
                faq = b
            elif CODA_H2.search(h):
                coda.append(b)
            else:
                story.append(b)

    if collection is None:
        raise SystemExit("no collection section found")
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
    parts = [ensure_css(head), crumb, header]

    # THE READING ORDER.
    #   hero -> the opinion -> who they are -> the card -> picture
    #   -> where to start -> the products -> picture -> the coda -> questions
    # The piece is read before the catalogue is shown, which is the change
    # Lenny asked for and the reason The Story now sits above The Collection.
    if heroes:
        parts.append(heroes[0])
    parts.append(render_writeup(spec, card_html))      # THE TGI TAKE
    parts.extend(mark_prose(story, "prose"))           # the main write-up
    if not SIDEBAR_IN_WRITEUP:
        parts.append('<div class="btk-card">\n' + card_html + "</div>\n\n")
    if len(heroes) > 1:
        parts.append(heroes[1])
    parts.append(render_start_here(spec, cards))
    parts.append(render_collection(spec, collection, cards))
    if len(heroes) > 2:
        parts.extend(heroes[2:])
    parts.extend(mark_prose(coda, "coda"))             # the shorter write-up
    if faq:
        parts.append(faq)
    parts.append(render_related(spec, brands))
    if more:
        parts.append(more)
    parts.append(tail)
    out = "".join(p for p in parts if p)

    # ---- assertions. A reorderer that loses things is worse than no reorderer.
    checks = [
        ("every product card survived",
         out.count('<div class="product-card"') == n_before, f"{n_before}"),
        ("every product link survived",
         out.count('class="product-link"') == html.count('class="product-link"'), ""),
        # by src, not by count: IF YOU LIKE legitimately ADDS four brand
        # thumbnails, so a raw == here fails a correct render. What has to hold
        # is that nothing arrived without leaving.
        ("every image survived",
         set(re.findall(r'<img[^>]+src="([^"]+)"', html))
         <= set(re.findall(r'<img[^>]+src="([^"]+)"', out)),
         f"{html.count('<img')} in, {out.count('<img')} out"),
        ("both JSON-LD blocks survived",
         out.count("application/ld+json") == html.count("application/ld+json"), ""),
        ("FAQ block intact",
         out.count('<div class="faq">') == html.count('<div class="faq">'), ""),
        ("document closes", "</body>" in out and "</html>" in out and "<footer" in out, ""),
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
             for k in ("take", "start-here", "collection", "related")),
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
          f"{len(spec['start_here'])} picks, {len(spec['related'])} related brands")

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
    for s in slugs:
        print(f"\n=== {s}")
        build(s, apply_)
