#!/usr/bin/env python3
"""build-dimple-divot-btk.py — Brand to Know: Dimple & Divot.
27 September 2026.

Lenny: "let's do a brand to know - https://dimpledivot.com/", then after the
28-option grid: "let's put all the brushes in one catagory and find the best
IRL style images possible."

PICKS: my starred 12, with every brush (including the new carved one from In
The Woods) in a single Brushes section.

FACTS: research/dimple-divot/notes.md. Brothers Chris and Nick; Chris's surname
(Mallinson) is on his byline, Nick's only on LinkedIn, so the page says "the
Mallinson brothers" only where Chris's byline carries it and otherwise "Chris
and Nick". Founding year conflicts (site "2020", anniversary post "five years
ago" in June 2026), so the page says "in 2020" only as the brand's own claim.
Hand-assembled in Raleigh per the brand. Partner makers per product copy.

QUOTES: verbatim from "Five Years of Dimple & Divot", bylined Chris Mallinson
and signed Chris and Nick, dimpledivot.com, 5 June 2026.

PHOTOS: the brand's own (site, blog, About page) plus Chris Mallinson's own
portfolio case study. No press photos (their site uses a famous Masters
photograph; not used). IRL frames lead every card. Sources in
research/dimple-divot/frames.json.

Prices and stock read 27 Sep 2026, USD. No feed card; that waits for Lenny.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "brand-to-know-dimple-divot"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/dimple-divot"
FR = json.loads((ROOT / "research/dimple-divot/frames.json").read_text())
SHOP = "https://dimpledivot.com/products/"

TITLE = "Brand to Know: Dimple & Divot, the Hickory Golf Brush From Raleigh"
DESC = ("Dimple & Divot makes hickory golf brushes by hand in Raleigh, North Carolina. The brothers "
        "behind it, their fall In The Woods collection, and fourteen picks from $13 to $120.")
H1 = "Brand to Know: Dimple &amp; Divot &mdash; The Hickory Brush From Raleigh"

# handle -> (name, detail, price, copy, new-in-woods)
P = {
 "carved-hickory-golf-brush": ("Carved Hickory Golf Brush", "In The Woods", 78,
   "This is the new one. The handle is carved so it has a texture you can feel, and it hangs from a green and orange paracord tether on an aluminium carabiner. The brand says the handle took a long time to get right.", True),
 "hickory-golf-brush-highland": ("Hickory Golf Brush", "Classic &middot; Highland", 50,
   "This is the brush that started the company, and the brand still calls it the one everything else is built from. It has the longest hickory handle of the range, firm nylon bristles and a nickel trigger snap.", False),
 "hickory-golf-brush-murphy": ("Hickory Golf Brush", "Classic &middot; Murphy", 50,
   "This is the same Classic with a black-and-white tether. We featured the Murphy in an accessories edit earlier this year, and it is still the one we would clip on first.", False),
 "hickory-golf-brush-pro-hybrid-green": ("Hickory Golf Brush PRO+", "Green", 65,
   "The PRO+ is the only brush they make with both nylon and metal bristles, on a shorter handle with a retractable tether that reaches 20 inches.", False),
 "hickory-golf-brush-mini-grass": ("Hickory Golf Brush Lite", "Keeper", 45,
   "The Lite is the smallest and lightest brush in the range, on a short four-inch tether and a bright blue carabiner that clips off in a second.", False),
 "clay-pigeon-ballmarker": ("Clay Pigeon Ball Marker", "In The Woods", 88,
   "A heavy brass marker in matte orange, cut in the shape of a clay pigeon. It is made for them by Legacy Golf in Denver. The product copy opens with one word: &ldquo;Pull.&rdquo;", True),
 "every-round-carry-divot-tool": ("Every Round Carry Divot Tool", "In The Woods", 118,
   "This is a single-prong repair tool machined from solid aluminium, with an olive paracord tether and the D&amp;D infinity pattern. Legacy Golf makes this one too.", True),
 "fleece-reversible-headcover-driver": ("Fleece Reversible Headcover", "Driver", 98,
   "It is olive sherpa fleece on one side and orange on the other, with an In The Woods patch. Apr&egrave;s Golf sews it in San Francisco. There is a fairway version at $88.", True),
 "essentials-pouch-rust": ("Essentials Pouch", "Rust", 120,
   "This is a flat Cordura pouch with a magnetic Fidlock closure and a mesh inside, for the gloves, tees and markers that rattle around a bag with too few pockets. It is cut and sewn in New York, and the rust is the only colour left in stock.", True),
 "d-d-icon-dad-hat-olive": ("D&amp;D Icon Dad Hat", "Olive", 35,
   "This is a washed, unstructured cotton cap with a curved brim and the D&amp;D mark. The brand says it pairs with the rest of the collection, or warm flannel.", True),
 "fleece-reversible-headcover-fw": ("Fleece Reversible Headcover", "Fairway", 88,
   "The fairway version of the same cover, in the same olive and orange sherpa with the In The Woods patch, also sewn by Apr&egrave;s Golf in San Francisco.", True),
 "d-d-icon-dad-hat-navy": ("D&amp;D Icon Dad Hat", "Navy", 35,
   "This is the same washed, unstructured cap in navy, with the D&amp;D mark on the front and the bright blue Dimple &amp; Divot label inside.", False),
 "d-d-fall-tees-50-ct": ("D&amp;D Fall Tees", "50 count", 13,
   "Fifty orange tees at the standard length, so they are easy to spot in the leaves. It is the least expensive thing on the page.", True),
 "infinity-leather-valet-tray": ("Infinity Leather Valet Tray", "Full-grain leather", 76,
   "This is a wet-moulded tray in vegetable-tanned leather, hand-stamped with the infinity pattern, for the desk or nightstand. Weather &amp; Story makes it in Raleigh, the brand&rsquo;s home town.", False),
}

SECTIONS = [
    ("brushes", "The Brushes", "the-brushes",
     ["carved-hickory-golf-brush", "hickory-golf-brush-highland", "hickory-golf-brush-murphy", "hickory-golf-brush-pro-hybrid-green", "hickory-golf-brush-mini-grass"],
     "<strong>Five brushes &middot; hand-assembled in Raleigh</strong>The new carved brush from the fall collection, and the three models that built the company: the Classic, the PRO+ and the Lite."),
    ("beyond", "Beyond the Brush", "beyond-the-brush",
     ["clay-pigeon-ballmarker", "every-round-carry-divot-tool", "fleece-reversible-headcover-driver", "fleece-reversible-headcover-fw", "essentials-pouch-rust",
      "d-d-icon-dad-hat-olive", "d-d-icon-dad-hat-navy", "d-d-fall-tees-50-ct", "infinity-leather-valet-tray"],
     "<strong>Nine pieces &middot; mostly In The Woods</strong>The fall collection in orange, olive and fleece, made with small American workshops in Denver, San Francisco and New York, plus a navy cap and a leather tray for the desk."),
]

PQ = {
    "disrupt": "We were not trying to disrupt anything. We just thought a better version existed and we wanted to be the ones to make it.",
    "ahead": "By the time someone copies what you made, you should already be two or three versions ahead of it. That has been our answer. We just keep going.",
    "make": "We want to keep developing new products because we are, at our core, people who like to make things.",
}
ATTR = "Chris Mallinson, co-founder, in Dimple &amp; Divot&rsquo;s &ldquo;Five Years&rdquo; post, June 2026"

BANDS = {
    "made": ("Photography &middot; Dimple &amp; Divot&rsquo;s own", "The shop: a brush being assembled by hand, a handle being sanded, and the drawing it all starts from.",
             [("band-a1", "Hands assembling a Dimple & Divot brush and its tether at a workbench", "Assembly"),
              ("band-a2", "A gloved hand holding a hickory brush handle during sanding", "Sanding"),
              ("band-a3", "A technical drawing of the Dimple & Divot brush with its trigger snap and bristle pattern", "The drawing")]),
    "brushes": ("Photography &middot; on the course", "Where the brushes end up: on a wedge, on a carry bag, and at the cart.",
                [("band-b1", "A hickory brush cleaning the grooves of a wedge", "On a wedge"),
                 ("band-b2", "A golfer walking across a fairway with a green carry bag", "On the bag"),
                 ("band-b3", "Golfers laughing around a golf cart on the course", "At the cart")]),
    "woods": ("Photography &middot; In The Woods campaign", "The fall collection was shot where it is named: a bag against a tree, a pouch in the leaves, a divot tool in the grass.",
              [("band-c1", "A golf bag with an orange fleece headcover propped against a tree in the woods", "Against a tree"),
               ("band-c2", "A rust Essentials Pouch lying in fallen leaves", "In the leaves"),
               ("band-c3", "An orange aluminium divot tool in long grass and leaves", "In the grass")]),
    "desk": ("Photography &middot; Dimple &amp; Divot&rsquo;s own", "These show the whole kit, laid out and on the bag.",
             [("band-d1", "A flat lay of the In The Woods collection on an orange plaid blanket", "The collection"),
              ("band-d2", "A golfer standing beside a checked stand bag on the course", "On the course"),
              ("band-d3", "A hickory brush clipped to a golf bag beside a striped towel", "Clipped on")]),
}

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Dimple &amp; Divot does one small thing properly: the golf brush. It has a hickory handle, a nickel snap, firm bristles and a tether in a colour you actually want on your bag. You notice the difference after your third plastic brush.</p>
    <p>The reason to know them is the eye. Chris Mallinson is a designer and art director, and it shows in the logo, the product and the packaging. The new fall collection, In The Woods, pushes further: orange and olive, a clay-pigeon marker, a sherpa headcover and a carved brush, several made with small American workshops.</p>
    <p>Buy the Classic at $50. For the new stuff, the carved brush at $78. Prices were read from the brand&rsquo;s store on 27 September 2026, in US dollars.</p>
    <h2 class="products-hdr btk-story-hdr">The Story</h2>
    <p>Dimple &amp; Divot is two brothers, Chris and Nick, in two different states. The brand dates itself to 2020, and the idea was simple: a better golf brush, made in the United States, built to last.</p>
    <p>A year in, an overseas maker copied it using their own photographs with the logo removed. The brothers went years without pay and nearly quit. Their answer was to keep improving the brush: stronger bristles, a slimmer snap, hybrid bristles, a retractable tether. The brand says it has sold more than 25,000, and every one is still hand-assembled in Raleigh.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Raleigh, North Carolina</span></div>
      <div class="sidebar-detail"><span class="l">Founders</span><span>Brothers Chris &amp; Nick</span></div>
      <div class="sidebar-detail"><span class="l">Since</span><span>2020, by the brand&rsquo;s account</span></div>
      <div class="sidebar-detail"><span class="l">Made</span><span>Hand-assembled in Raleigh</span></div>
      <div class="sidebar-detail"><span class="l">Brushes sold</span><span>25,000+</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$13&ndash;$120</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>The Classic brush, $50</span></div>
      <a href="https://dimpledivot.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit Dimple &amp; Divot &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#DimpleAndDivot</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#HickoryBrush</span>
        <span class="hashtag">#MadeInUSA</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

PROSE = 'style="max-width:760px;font-size:16px;line-height:1.7;"'
MADE = f"""
<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr" id="how-its-made">How It&rsquo;s Made</h2>
  <div {PROSE}>
    <p>The handles are American hickory, the wood that golf clubs were made from before steel. The brand says its brushes are machined, finished and assembled in the United States, and hand-assembled in Raleigh. Early brushes had painted stripes; the current ones drop the paint and leave a matte finish so the grain shows.</p>
    <p>There are four models. The Classic has the longest handle and the most colours. The PRO and PRO+ are shorter, on a retractable tether, and the PRO+ adds metal bristles. The Lite is the smallest, on a carabiner. The brand&rsquo;s collaborations have included Jones, Cleveland and Municipal, and a species brush made with Gumtree Golf &amp; Nature Club.</p>
  </div>
</section>
"""

FAQ = [
    ("Who makes Dimple & Divot golf brushes?",
     "Two brothers, Chris and Nick. Chris Mallinson, a designer and art director, writes the brand's posts. The company is based in Raleigh, North Carolina."),
    ("Where are Dimple & Divot brushes made?",
     "The brand says its brushes are machined, finished and assembled in the United States, and that every brush is hand-assembled at its Raleigh headquarters."),
    ("Which Dimple & Divot brush should I buy?",
     "The Classic ($50) has the longest hickory handle and the most colours. The PRO+ ($65) adds metal bristles and a retractable tether. The Lite ($45) is the smallest, on a carabiner. The new Carved Hickory brush ($78) has a textured handle."),
    ("What is In The Woods?",
     "Dimple & Divot's fall 2026 collection, released 27 September 2026: the carved brush, a clay-pigeon ball marker, an aluminium divot tool, a fleece headcover, the Essentials Pouch in rust, an olive cap and orange tees."),
    ("Do hickory brushes damage golf clubs?",
     "The Classic, Lite and carved brushes use firm nylon bristles, which the brand says will not harm clubs. The PRO+ combines nylon and metal bristles for more cleaning power, which the brand also says is safe for clubs."),
]


def pq(key):
    return (f'\n<!-- TGI-DD-PQ-{key} -->\n<div class="pull-quote">\n  <div class="pull-quote-inner">'
            f'&ldquo;{PQ[key]}&rdquo;<span class="pull-quote-attr">&mdash; {ATTR}</span></div>\n</div>\n'
            f'<!-- /TGI-DD-PQ-{key} -->\n')


def band(key):
    kick, line, items = BANDS[key]
    figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>'
                     for f, alt, cap in items)
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <p class="cat-kicker"><strong>{kick}</strong>{line}</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


def card(h, idx):
    name, detail, price, copy, new = P[h]
    fr = [f["local"] for f in FR[h]]
    label = H.unescape(f"Dimple & Divot {name} {detail}").replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>'
                   for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>'
                   for j in range(len(fr)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">Dimple &amp; Divot &middot; {detail}</div>'
            f'<div class="product-name">{name} &middot; ${price}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="{SHOP}{h}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


def section(sec, n0):
    key, h2, anchor, ids, kicker = sec
    cards = "\n".join(card(h, n0 + j) for j, h in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} {"Piece" if len(ids) == 1 else "Pieces"}</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>'
                     for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items, pos = [], 1
    for _, _, _, ids, _ in SECTIONS:
        for h in ids:
            items.append({"@type": "ListItem", "position": pos, "url": SHOP + h, "name": H.unescape(f"Dimple & Divot {P[h][0]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-09-27", "dateModified": "2026-09-27",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": items},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Drops & Brands", "item": "https://thegrassyissue.com/#feed"},
            {"@type": "ListItem", "position": 3, "name": "Dimple & Divot", "item": URL}]},
    ]
    t, d = H.escape(TITLE, quote=True), H.escape(DESC, quote=True)
    ld = "".join(f'<script type="application/ld+json">\n{json.dumps(b, indent=1, ensure_ascii=False)}\n</script>\n' for b in blocks)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{t} | The Grassy Issue</title>
<meta name="description" content="{d}" />
<link rel="icon" href="/favicon.ico" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<meta property="og:type" content="article" />
<meta property="og:url" content="{URL}" />
<meta property="og:title" content="{t}" />
<meta property="og:description" content="{d}" />
<meta property="og:image" content="{og}" />
<meta property="og:site_name" content="The Grassy Issue" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{t}" />
<meta name="twitter:description" content="{d}" />
<link rel="canonical" href="{URL}" />
<link rel="preload" as="image" href="{IMG}/hero.jpg" />
{ld}"""


def main(apply_):
    ids = [h for s in SECTIONS for h in s[3]]
    assert len(ids) == 14 == len(set(ids)) and set(ids) == set(P)
    for h in ids:
        assert FR.get(h), h
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Dimple &amp; Divot</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Raleigh, NC &middot; since 2020</span><span class="dot"></span>
    <span>14 pieces &middot; $13&ndash;$120</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Dimple &amp; Divot hickory brushes laid out on grey with their coloured tethers, carabiners and nickel snaps" fetchpriority="high" /></div></div>
"""
    body += TAKE + band("made") + pq("disrupt") + MADE + band("brushes")
    n = 1
    s, n = section(SECTIONS[0], n); body += s + pq("ahead") + band("woods")
    s, n = section(SECTIONS[1], n); body += s + band("desk") + pq("make")
    body += faq_html()
    out = head_top() + head_rest + body + tail
    print(f"  {n-1} picks")
    if not apply_:
        print("  dry run — pass --apply")
        return
    OUT.write_text(out, encoding="utf-8")
    verify()


def verify():
    fin = OUT.read_text(encoding="utf-8")
    bad = []
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    for leak in ("Burnt Orange", "Manors Revisited", "Nicklaus"):
        if leak in above:
            bad.append(f"should not appear: {leak}")
    if fin.count('class="product-card"') != 14:
        bad.append("card count")
    for k, t in PQ.items():
        if fin.count(t[:50]) != 1:
            bad.append(f"pq {k}")
    if above.count('class="ig-grid"') != 4:
        bad.append("band count")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", above), re.I):
        bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file():
            bad.append(f"missing {f}")
    if bad:
        OUT.unlink()
        sys.exit("! removed. " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
