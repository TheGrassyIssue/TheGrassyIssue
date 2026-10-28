#!/usr/bin/env python3
"""build-penta-btk.py — Brand to Know: Penta Golf. 28 October 2026. Cloned from build-pare-btk.py.
Lenny: "Let's do a brand to know - https://penta-golf.com/" -> options sheet -> "Lets build the post" (all 20: 14 in stock + 6 sold out).
FACTS: penta-golf.com About + live catalogue (research/penta/catalogue.json, USD, 28 Oct 2026); Monster Children Q&A (Feb 2024).
Founders stay unnamed (the brand never names them). Never "worth".
OLD HEADER (Paré):
Lenny: "Let's do a brand to know - https://pare.golf/collections/all" -> options sheet -> "I want a section about the sold out
stuff, especially the more colorful options and let's also mention that the logo is very similar to prada" + "I love the drawing
of the guy putting". Built from the starred picks + a Paré Boy section + a colorful sold-out section.
FACTS: research/pare/brief.md (about page, MyGolfSpy Aug 2025, Gordon College Jul 2025, Kollective Hustle Jul 2024),
research/pare/catalogue.json (pare.golf live, Oct 27 2026, USD). Home city is NOT published anywhere: never name one.
Left out: the in-stock HYPEGOLF tee with a Tagalog expletive in its name, and the Kapamilya-only (members) pieces.
The Prada point is our observation; the brand's own "The Devil Wears Paré" copy is what we cite. Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Brand to Know: Penta Golf, Golf Clothes From Sydney's Northern Beaches"
DESC = ("Penta Golf is a Northern Beaches, Sydney brand started by friends from a print magazine and a youth culture agency: "
        "zip polos, Hazard shorts and a new capsule with LA's Barnaby's. All 20 pieces, with prices.")
H1 = "Brand to Know: Penta Golf, Golfwear From Sydney's Northern Beaches"
BC = "Brand to Know: Penta Golf"
SLUG = "brand-to-know-penta-golf"
IMG = "/images/penta-golf"
SHOP = "https://penta-golf.com/products/"
C = "Penta Golf"
SO = " &middot; sold out"
P = {
 # Penta x Barnaby's
 "grid-lush": (C, "PXB Grid Polo, Lush Ice", "$99", "pentaxbarnabys-grid-polo-lush-ice",
   "Our pick. The newest thing Penta makes, from its December 2025 collaboration with Barnaby&rsquo;s, the LA glove brand: Penta&rsquo;s usual polo fit, in a blue grid that fades to black at the hem. Every size was in stock."),
 "grid-sorbet": (C, "PXB Grid Polo, Lemon Sorbet", "$99", "penta-x-barnabys-grid-polo-lemon-sorbet",
   "The same Grid Polo in a pale lemon fade with a black collar. Penta&rsquo;s line on the pair: &ldquo;Turns out all your swing needed was a new palette.&rdquo;"),
 "glove-green": (C, "PXB Hand in Hand Glove, Green/Silver", "$36", "penta-x-barnabys-hand-in-hand-glove-green-silver",
   "Barnaby&rsquo;s made its name on gloves, so the collaboration was always going to have one. Cabretta leather with a metallic ball marker built into the back."),
 "glove-salt": (C, "PXB Hand in Hand Glove, Salt/Silver", "$36", "penta-x-barnabys-hand-in-hand-glove-salt-silver",
   "The same glove with salt trim. In stock in left-hand M to XL."),
 "blade": (C, "PXB Blade Putter Cover", "$68", "penta-x-barnabys-blade-putter-cover",
   "A dark green blade cover with the PBG mark on one side and the hand-in-hand logo on the other. The only headcover Penta sells."),
 # Polos
 "optical": (C, "Golf Polo, Optical", "$72", "penta-golf-polo-optical",
   "Penta&rsquo;s version of the golf polo: lightweight poly spandex, and a shiny YKK zip where the buttons usually go. Optical is the navy with a tonal pattern, and it&rsquo;s the colorway with the most sizes left."),
 "metal": (C, "Golf Polo, Metal", "$72", "penta-golf-polo-metal",
   "The same zip polo in bottle green with a white tipped collar. Down to S and M when we checked."),
 "digital": (C, "Golf Polo, Digital", "$72", "penta-golf-polo-digital",
   "The black zip polo, also down to S and M. The campaign shot it in a bunker."),
 "jersey": (C, "PENTA Golf Jersey", "$63", "penta-golf-jersey",
   "The oldest thing still on the shelf, from October 2022: a black football-style jersey with PENTA outlined across the chest and a small badge. XL and XXL only."),
 # Shorts, pants, tees
 "hazard-moss": (C, "Hazard Shorts, Moss", "$90", "hazard-short-moss",
   "Nylon shorts with a built-in quick-release belt, a pocket for your broken tees and a reflective logo. &ldquo;Look good playing your fairway bunker shots,&rdquo; says Penta. Sizes 30 and 32 left."),
 "hazard-black": (C, "Hazard Shorts, Black", "$90", "hazard-short-black",
   "The same short in black, which made our All-Black Edit because it holds a true black in daylight. Down to a 30."),
 "etiquette": (C, "Etiquette Pants", "$144", "etiquette-pants",
   "Breathable, lightweight nylon pants built for walking, &ldquo;(we know you&rsquo;re getting the cart),&rdquo; says the copy. Only a 30 waist left."),
 "footwork": (C, "Footwork Tee, Navy", "$54", "footwork-tee-navy",
   "A navy tee in US cotton with &ldquo;Footwork&rdquo; on the front and a diagram of where your feet go on the back. The copy calls it &ldquo;swing secrets.&rdquo;"),
 "gear": (C, "Gear Specialist Tee", "$54", "gear-specialist-tee",
   "&ldquo;Business in the front, party in the back.&rdquo; Gear Specialist on the chest, and a full pro shop-style ad for Penta Golf, phone number and all, across the back."),
 # Sold out
 "cap-navy": (C, "Players Cap, Navy", "$54" + SO, "players-cap-navy",
   "Nylon ripstop with white contrast stitching and the PENTA wordmark. &ldquo;Sits firm, shades heavy.&rdquo; The newest cap, from July 2025, and gone."),
 "cap-bone": (C, "Players Cap, Bone", "$54" + SO, "off-course-cap-bone",
   "The cream version of the Players Cap with a green wordmark and the PG monogram on the side."),
 "cap-black": (C, "Players Cap, Black", "$54" + SO, "players-cap-black",
   "The black Players Cap, from the first drop in October 2022."),
 "elements-black": (C, "Elements Jacket, Black", "$135" + SO, "penta-elements-jacket",
   "A half-zip shell for wind and rain. Penta&rsquo;s pitch: &ldquo;Remind your loved ones that golf is a 365 day pursuit.&rdquo;"),
 "elements-butter": (C, "Elements Jacket, Butter", "$135" + SO, "penta-elements-jacket-butter",
   "The same jacket in butter cream, from the first drop. The one we&rsquo;d most like to see come back."),
 "member": (C, "Member Shorts", "$90" + SO, "member-trunks",
   "Black nylon shorts from the first drop in October 2022."),
}
SECTIONS = [
 ("Penta &times; Barnaby&rsquo;s", "barnabys", ["grid-lush", "grid-sorbet", "glove-green", "glove-salt", "blade"],
  "<strong>Five pieces &middot; $36&ndash;$99</strong>The December 2025 collaboration with Barnaby&rsquo;s, the LA glove brand: two Grid Polos, two gloves and a blade cover. The newest thing in the store, and the only part of it with every size left."),
 ("The Zip Polos", "polos", ["optical", "metal", "digital", "jersey"],
  "<strong>Four pieces &middot; $63&ndash;$72</strong>Poly spandex polos with a YKK zip instead of buttons, plus the original jersey. Sizes are thin, so check before you fall for one."),
 ("Shorts, Pants and Tees", "bottoms", ["hazard-moss", "hazard-black", "etiquette", "footwork", "gear"],
  "<strong>Five pieces &middot; $54&ndash;$144</strong>The Hazard Shorts with the built-in belt, the nylon Etiquette Pants and two cotton tees with jokes on the back."),
 ("Sold Out", "sold-out", ["cap-navy", "cap-bone", "cap-black", "elements-black", "elements-butter", "member"],
  "<strong>Six pieces you can&rsquo;t buy right now</strong>All three Players Caps, both Elements Jackets and the Member Shorts were sold out when we checked. Prices are what they sold for."),
]
N = 20
PQ = {
 "polos": ("There were really no local brands at the time that spoke to the style we wanted to wear on the course.", "Penta, to Monster Children, 2024"),
 "bottoms": ("Play with good golfers. The humiliation will do you wonders.", "Penta, to Monster Children, 2024"),
}
BANDS = {
 "polos": ("The campaign", "Penta shoots its own clothes outdoors, on the grass and on the beach, in hard evening light.",
   [("band-metal-sun", "A man in the green Penta zip polo adjusting orange-tinted sunglasses against a pale sky", "The Metal polo"),
    ("band-metal-beach", "A man in the green Penta zip polo and black shorts standing on a beach at sunset", "On the beach"),
    ("band-digital", "A man in the black Penta zip polo and olive shorts digging his ball out of the dirt", "The Digital polo, off the fairway")]),
 "bottoms-after": ("The Hazard Shorts, out on the course", "The short Penta named after the part of the course it&rsquo;s built for.",
   [("band-swing", "A golfer in a blue polo and moss Hazard Shorts mid-swing on a fairway", "Moss, mid-swing"),
    ("band-bunker", "A golfer in moss Hazard Shorts and a navy cap playing out of a bunker", "Moss, in the hazard"),
    ("band-black", "A man in a blue polo and black Hazard Shorts on a grassy hill", "Black, on the hill")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Penta is a golf clothing brand from Sydney&rsquo;s Northern Beaches, and its About page puts the whole idea in one line: &ldquo;We started PENTA because golf attire no longer reflected the people playing it.&rdquo; Before the brand, the founders worked together at a creative print magazine and a youth culture agency, and it shows. The clothes are technical, the jokes are dry, and the photos look like a magazine shot them.</p>
    <p><strong>What they make.</strong> Not much, and that&rsquo;s the point. The core is a zip polo in poly spandex with a YKK zip where the buttons usually go, the Hazard Shorts with a quick-release belt built in, and a pair of nylon pants called Etiquette. Around that sit two cotton tees with jokes on the back and a nylon Players Cap that was sold out in every color when we checked. The newest drop, in December 2025, was a capsule with Barnaby&rsquo;s, the LA glove brand: two Grid Polos, two gloves and a blade cover.</p>
    <p><strong>Where they play.</strong> Asked by Monster Children, they named &ldquo;anywhere on the Northern Beaches,&rdquo; with Warringah Golf Club as their local and Shortees, the floodlit par-3 in Sydney, as a shout-out. Monster Children, the Sydney skate and surf magazine, says Penta was the first golf company ever to appear inside its pages. The founders&rsquo; answer to why so many surfers and skaters play golf is the clearest thing they&rsquo;ve said about the brand: &ldquo;You&rsquo;re up against yourself most of the time, and it requires dedication to get better.&rdquo;</p>
    <p><strong>The catch.</strong> Penta drops slowly. When we checked, 14 of its 20 products were in stock, and most of the polos, shorts and pants were down to one or two sizes. The Barnaby&rsquo;s capsule is the only part of the store with a full size run. The store shows US shoppers prices in US dollars.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">At a Glance</div>
      <div class="sidebar-detail"><span class="l">From</span><span>Northern Beaches, Sydney</span></div>
      <div class="sidebar-detail"><span class="l">Home course</span><span>Warringah Golf Club</span></div>
      <div class="sidebar-detail"><span class="l">Oldest piece listed</span><span>October 2022</span></div>
      <div class="sidebar-detail"><span class="l">Latest drop</span><span>Penta &times; Barnaby&rsquo;s, Dec 2025</span></div>
      <div class="sidebar-detail"><span class="l">In stock</span><span>14 of 20 products</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$36&ndash;$144</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>PXB Grid Polo, Lush Ice</span></div>
      <div class="hashtags">
        <span class="hashtag">#PentaGolf</span>
        <span class="hashtag">#NorthernBeaches</span>
        <span class="hashtag">#BrandToKnow</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
STORY = """
<section class="products" data-btk="story" style="margin-top:8px;">
  <div class="drop-tag grass">The Story</div>
  <h2 class="products-hdr" id="story">Golfwear, Anywhere</h2>
  <div class="writeup-body">
    <p>&ldquo;Golfwear, anywhere&rdquo; is how Penta heads its own story. The founders say they came to golf from the worlds where &ldquo;design, subculture, and sport naturally intersect,&rdquo; and that what they saw in the game was &ldquo;a sport rich in tradition, but ready for reinterpretation.&rdquo; Everything is designed in-house, and the brand says it is made for &ldquo;the creatives, the thinkers, and the new generation of players who see golf as culture, not a sport alone.&rdquo;</p>
    <p>The gap they saw was a local one. &ldquo;There were really no local brands at the time that spoke to the style we wanted to wear on the course,&rdquo; they told Monster Children, and the options they did have weren&rsquo;t both technical and good-looking. The first pieces went on sale in October 2022: the Players Cap, the Elements Jacket, the Member Shorts, the Etiquette Pants and the jersey. Only the pants and the jersey are left.</p>
    <p>The founders keep their names off the site, and the brand talks in short, dry lines. Asked by Monster Children for a first-timer&rsquo;s best advice, they said: &ldquo;Just enjoy being out there with friends and try not to smack the shit out of the ball.&rdquo; Asked whether Penta would make the writer swing better: &ldquo;Yes. But best results are achieved with our entire kit.&rdquo;</p>
    <p>We first wrote about Penta in our guide to <a href="/drops/australian-golf-brands-and-trips">Australian golf brands</a>, and the black Hazard Shorts made <a href="/drops/the-all-black-edit">The All-Black Edit</a>. The Barnaby&rsquo;s capsule is the reason for this one, and the Grid Polo is the best thing in the store.</p>
  </div>
</section>
"""
FAQ = [
 ("Where is Penta Golf from?", "Sydney's Northern Beaches. The founders have named Warringah Golf Club as their local course."),
 ("Who started Penta Golf?", "A group of friends who worked together at a creative print magazine and a youth culture agency before starting the brand. They don't put their names on the website."),
 ("What does Penta Golf make?", "Zip-neck golf polos in poly spandex, the Hazard Shorts with a built-in belt, the nylon Etiquette Pants, cotton tees, nylon caps and an all-weather jacket. Everything is designed in-house."),
 ("What is Penta x Barnaby's?", "A December 2025 collaboration with Barnaby's, the LA glove brand: two Grid Polos at $99, two cabretta leather gloves with a built-in ball marker at $36, and a blade putter cover at $68."),
 ("How much does Penta Golf cost?", "On October 28, 2026, its store showed US shoppers $36 to $144: $54 tees, $72 zip polos, $90 Hazard Shorts and $144 Etiquette Pants. 14 of its 20 products were in stock, many in only one or two sizes."),
]
LOOKBOOK = ""
FRN = json.loads((ROOT / "research/penta/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-R3-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
def card(k, idx):
    brand, item, price, handle, copy = P[k]
    url = SHOP + handle
    fr = FRN[k]
    label = H.unescape(f"{brand} {item}").replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>'
                   for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>'
                   for j in range(len(fr)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{brand}</div>'
            f'<div class="product-name">{item} &middot; {price}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="{url}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>'
                     for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')




def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items, pos = [], 1
    for sec in SECTIONS:
        for h in sec[2]:
            items.append({"@type": "ListItem", "position": pos, "url": SHOP + P[h][3], "name": H.unescape(f"{P[h][0]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-10-28", "dateModified": "2026-10-28",
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
            {"@type": "ListItem", "position": 3, "name": BC, "item": URL}]},
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



def pq(k):
    q, who = PQ[k]
    return (f'\n<div class="pull-quote" style="margin:56px auto 24px">\n  <div class="pull-quote-inner">'
            f'&ldquo;{q}&rdquo;<span class="pull-quote-attr">&mdash; {who}</span></div>\n</div>\n')


def band(k):
    kick, line, items = BANDS[k]
    figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>' for f, alt, cap in items)
    return (f'\n<section class="products" style="margin-top:8px;">\n  <p class="cat-kicker"><strong>{kick}</strong>{line}</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


def section(sec, n0):
    h2, anchor, ids, kicker = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} {"pick" if len(ids)==1 else "picks"}</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def main(apply_):
    ids = [k for s in SECTIONS for k in s[2]]
    assert len(ids) == N == len(set(ids)) and set(ids) == set(P), (len(ids), set(P) ^ set(ids))
    for k in ids:
        assert FRN[k] and all((ROOT / f.lstrip("/")).is_file() for f in FRN[k]), k
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Brand to Know &middot; Northern Beaches, Sydney</span><span class="dot"></span>
    <span>20 pieces, 6 of them sold out &middot; checked October 28, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A man in orange-tinted sunglasses and the navy Penta Optical zip polo sitting on the grass on a sunny day" fetchpriority="high" /></div></div>
"""
    body += TAKE + STORY
    n = 1
    for s in SECTIONS:
        if s[1] + "-before" in BANDS: body += band(s[1] + "-before")
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
        if s[1] + "-after" in BANDS: body += band(s[1] + "-after")
    body += faq_html()
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    if fin.count('class="product-card"') != N: bad.append("card count")
    if re.search(r"\bworth\b", re.sub(r"\bFort\s+Worth\b", " ", re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<script\b.*?</script>", " ", above))), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
