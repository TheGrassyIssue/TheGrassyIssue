#!/usr/bin/env python3
"""build-galvin-btk.py — Galvin Green, Brand to Know. 24 September 2026.

Lenny: "Let's do a brand to know - galvingreen.com. it will get cold and wet in
Austin eventually", then "let's focus more on the transitional weather - no
parkas, heavy duty stuff", "also add some tees or polos", and "add the core
collection, a section about normal everyday wearables."

SHELL. Cloned from drops/brand-to-know-manors.html, the newest BTK page: its
<style> blocks, nav, brand-index strip, More-from-TGI block, footer and gallery
script are kept byte for byte. Everything a reader sees between the breadcrumb
and the brand-index strip is replaced, as is every head tag that names the post.

DATA. research/galvin/picks.json (collect-galvin.py), prices re-read live on
24 Sep 2026 in USD. Six picks are marked down on the store; those show the sale
price with the list price beside it, both as the store shows them.

QUOTES. All five are verbatim from named people with dated sources, recorded in
research/galvin/notes.md. None is repeated in the body.

RYDER CUP. Galvin Green was Team Europe's official WEATHERWEAR supplier in 2016
and 2018 only. Loro Piana was the team outfitter. The copy says exactly that.

Writes drops/brand-to-know-galvin-green.html. Does NOT touch the homepage feed:
the card waits for Lenny's approval. Dry run by default.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
OUT = ROOT / "drops/brand-to-know-galvin-green.html"
PICKS = json.loads((ROOT / "research/galvin/picks.json").read_text())["products"]
SLUG = "brand-to-know-galvin-green"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/galvin-green"

TITLE = "Galvin Green — The Swedish Family Firm Built for In-Between Weather"
DESC = ("A family-owned golf brand from Växjö, Sweden, that has made only golf "
        "clothing since 1990. Polos, windproof layers, mid-layers and everyday "
        "pieces for Austin's cool, damp months.")
H1 = ("Galvin Green &mdash; The Swedish Family Firm That Dresses Golf for the "
      "In-Between Weather")

# hand-read from each pick's live handle, 24 Sep 2026
COLOUR = {
    "Marty": "Crystal Blue", "Muir": "Orange", "Mulligan": "Crystal Blue / White / Navy",
    "Medley": "Navy / Red", "Luis": "Navy", "Lawrence": "Blue / Navy / White",
    "Larry": "Royal Blue", "Leo": "Navy", "Lane": "Sharkskin",
    "Lloyd": "Royal Blue / Black", "Dixon": "Light Grey",
    "Daxton": "Aqua / Cool Grey / White", "Del": "Crystal Blue Melange",
    "Dean": "Crystal Blue / Navy", "Adam": "Royal Blue / Black", "Aston": "Navy",
    "Air": "Black / Forged Iron", "Noah": "White", "Nixon": "Black",
    "Paul": "Blue Bell", "Pedro": "Navy", "Donnie": "Sand", "Danby": "Navy",
    "Carl": "Grey Melange",
}
# list price where the store shows a markdown, read from compare_at_price
WAS = {"Lawrence": 259, "Lloyd": 299, "Dixon": 149, "Daxton": 189,
       "Nixon": 149, "Paul": 129}

KIND = {
    "Marty": "Polo", "Muir": "Polo", "Mulligan": "Polo", "Medley": "Polo",
    "Luis": "Short-Sleeve Windbreaker", "Lawrence": "Wind Jacket",
    "Larry": "Half-Zip Windbreaker", "Leo": "Wind Vest", "Lane": "Wind Pants",
    "Lloyd": "Wind Jacket", "Dixon": "Half-Zip Mid-Layer",
    "Daxton": "Half-Zip Mid-Layer", "Del": "Quarter-Zip Vest",
    "Dean": "Half-Zip Mid-Layer", "Adam": "Half-Zip Rain Jacket",
    "Aston": "GORE-TEX Rain Jacket", "Air": "Short-Sleeve Rain Jacket",
    "Noah": "Pants", "Nixon": "Pants", "Paul": "Shorts", "Pedro": "Shorts",
    "Donnie": "Sweatshirt", "Danby": "Hooded Mid-Layer", "Carl": "Merino V-Neck",
}

CARD = {
    "Marty": "Marty is the plain one: a solid stretch polo with a contrast colour on the collar and sleeve edges, UV 20+ and ribbed cuffs.",
    "Muir": "Muir carries an all-over tonal print on VENTIL8&trade; PLUS, the brand&rsquo;s breathable, quick-drying shirt fabric, with a conventional polo collar holding it down.",
    "Mulligan": "Mulligan runs a colour block across the shoulders and a technical accent on the sleeve, cut in VENTIL8&trade; PLUS with mechanical stretch.",
    "Medley": "Medley puts a small, refined print on a streamlined VENTIL8&trade; PLUS body with a tailored collar, built for the warm end of the season.",
    "Luis": "Luis weighs 94 grams in a medium. It is a short-sleeve quarter-zip windbreaker in INTERFACE-1&trade;, Warming Effect #1, for the round that starts cool and ends warm.",
    "Lawrence": "Lawrence is a two-tone full-zip wind jacket in bluesign&reg; recycled polyester, with elastic cuffs and a drawcord hem. Three sizes left in this colourway.",
    "Larry": "Larry weighs less than a sleeve of golf balls, in the brand&rsquo;s own words. It is a half-zip INTERFACE-1&trade; windbreaker with stretch and a water-repellent finish.",
    "Leo": "Leo is a full-zip INTERFACE-1&trade; vest. It keeps the wind off your chest and leaves your arms free, which is most of what a cool morning asks for.",
    "Lane": "Lane pants are windproof and water repellent with built-in stretch, rated Warming Effect #2. The brand pitches them for days too cold for regular trousers and too dry for rain pants.",
    "Lloyd": "Lloyd is a two-tone INTERFACE-1&trade; windbreaker with a stripe down the back. It is windproof, water repellent and cut with stretch through the swing.",
    "Dixon": "Dixon is the classic half-zip mid-layer: soft bluesign&reg; fabric, Warming Effect #1. The brand suggests sizing up for a looser fit.",
    "Daxton": "Daxton adds front piping and a printed chest graphic to a half-zip in recycled INSULA&trade;. It is made entirely from recycled bottles. Three sizes left.",
    "Del": "Del is a quarter-zip thermal vest at Warming Effect #1. It goes over a polo on its own, or under a wind jacket when the front comes through.",
    "Dean": "Dean pairs old-school colour blocking with INSULA&trade; at Warming Effect #2, the warmer grade. It is soft, stretchy and quick to dry.",
    "Adam": "Adam is a half-zip pullover in Pertex&reg; Shield 3-layer stretch, part of the DRYVR&trade; line. Chest tabs pull the bulk in at the front so the swing stays clean.",
    "Aston": "Aston is the GORE-TEX option: two-layer ePE membrane with a light mesh lining. It is waterproof, windproof and breathable without the weight of a winter shell.",
    "Air": "Air is a short-sleeve rain jacket, a style the brand calls a customer favourite since its debut. It keeps the torso dry and leaves the forearms bare for the swing.",
    "Noah": "Noah pants have a shirt-gripper waistband, stretch and UV 20+, with front and back pockets. Twenty-one sizes were in stock in white on the day we read the store.",
    "Nixon": "Nixon is the lighter trouser: mechanical stretch in a soft bluesign&reg; fabric, offered in sixteen waist and leg combinations.",
    "Paul": "Paul shorts are lightweight and quick-drying, with a shirt-gripper waistband, built-in stretch and UV 20+.",
    "Pedro": "Pedro shorts use VENTIL8&trade; PLUS for airflow and mechanical stretch for movement. They carry UV 20+ and pockets front and back.",
    "Donnie": "Donnie is a lightweight insulated sweatshirt. It sits under a jacket on a cold day or goes over a polo on its own when it is merely cool.",
    "Danby": "Danby is a fitted hoodie in recycled INSULA&trade; at Warming Effect #2, cut close enough to swing in and plain enough to wear to lunch.",
    "Carl": "Carl is a merino V-neck with a fully fashioned saddle shoulder and a small embroidered mark on the left sleeve.",
}

GROUPS = [
    ("polo", "The Polos &mdash; 4 Pieces", "The Polos", "polos",
     "<strong>M-line &middot; VENTIL8&trade; PLUS &middot; read 24 September 2026</strong>"
     "Every Galvin Green polo name starts with M. These four run $99 to $129 and "
     "carry most of the Austin year on their own, from April to the first cold front."),
    ("wind", "Wind Layers &mdash; 6 Pieces", "Wind Layers: INTERFACE-1&trade;", "wind",
     "<strong>L-line &middot; windproof, water repellent &middot; read 24 September 2026</strong>"
     "This is the heart of the page. INTERFACE-1&trade; is the brand&rsquo;s answer to "
     "wind, cool air and light rain, graded Warming Effect #1 to #3 so you can pick "
     "the weight. Prices run $169 to $209, with two jackets marked down."),
    ("mid", "Mid-Layers &mdash; 4 Pieces", "Mid-Layers: INSULA&trade;", "mid",
     "<strong>D-line &middot; thermal insulation &middot; read 24 September 2026</strong>"
     "INSULA&trade; goes on under the wind layer or over a polo on its own. Dixon and "
     "Daxton are marked down to $89.40 and $94.50; Dean at $229 is the warm grade."),
    ("rain", "Light Rain &mdash; 3 Pieces", "Light Rain: DRYVR&trade;", "rain",
     "<strong>A-line &middot; waterproof &middot; read 24 September 2026</strong>"
     "These three shells are for the day it rains properly. All are lightweight and "
     "none is insulated. At $369 to $399 they cost the most on the page, and they come out the least."),
    ("core", "Everyday &mdash; 7 Pieces", "The Core Collection", "core-collection",
     "<strong>Trousers, shorts, knitwear &middot; read 24 September 2026</strong>"
     "The ordinary clothes, which a weather brand makes as carefully as the shells. "
     "Pants and shorts run $77.40 to $169; the sweatshirt, hoodie and merino run $139 to $149."),
]

PQ = {
    "nilsson": ("Functional clothing is especially important in golf, where you&rsquo;re "
                "often exposed to sun, rain and wind. It is incredibly important that you "
                "have the right clothing regardless of the weather, so you can continue to "
                "enjoy your round and play to your best.",
                "Tomas Nilsson, founder, to Golf Business News, July 2020"),
    "fit": ("When we first started in the US, we got some comments that our European "
            "sizing was not okay for US golfers, but that has clearly changed.",
            "Mats Lundqvist, Creative Director, to Golf Today, April 2021"),
    "insula": ("From a time when cotton shirts dominated the scene with shrinkage and heavy "
               "moisture absorption and knitted sweaters weighed golfers down if it rained, "
               "there have been huge advancements in fabric technology for golfers in the "
               "last three decades and the breathable, non-absorbent INSULA garments rank "
               "among our most prized achievements.",
               "Mats Lundqvist, Creative Director, to Golf Business News, July 2020"),
    "compromise": ("It means we will not compromise on the quality or function of our "
                   "products, just to achieve an attractive / commercial price level.",
                   "Mats Lundqvist on the brand&rsquo;s &lsquo;we never compromise&rsquo; "
                   "line, to Golf Today, April 2021"),
    "design": ("Items with overly complicated features and / or are over-designed can "
               "become tired quickly. But, items with a clear, pure design and purpose "
               "will live a lot longer.",
               "Mats Lundqvist, Creative Director, to Golf Today, April 2021"),
}


def pq(key):
    t, a = PQ[key]
    return (f'\n<!-- TGI-GG-PQ-{key} -->\n<div class="pull-quote">\n  <div class="pull-quote-inner">'
            f'&ldquo;{t}&rdquo;<span class="pull-quote-attr">&mdash; {a}</span></div>\n</div>\n'
            f'<!-- /TGI-GG-PQ-{key} -->\n')


def money(x):
    return f"${x:,.0f}" if float(x).is_integer() else f"${x:,.2f}"


def card(p, n):
    name = p["name"]
    frames = p["local"]
    order = [1, 0, 2, 3] if len(frames) >= 4 else list(range(len(frames)))
    frames = [frames[i] for i in order]
    label = f"Galvin Green {name} {KIND[name]}"
    imgs = "".join(
        f'<div class="pg-frame"><img src="{f}" alt="{label}, {COLOUR[name]} &middot; view {i+1} of {len(frames)}" loading="lazy" /></div>'
        for i, f in enumerate(frames))
    dots = "".join(
        f'<button class="pg-dot{" on" if i == 0 else ""}" data-i="{i}" aria-label="View image {i+1}"></button>'
        for i in range(len(frames)))
    price = money(p["usd"])
    if name in WAS:
        price += f' <span style="opacity:.5;text-decoration:line-through">${WAS[name]}</span>'
    return (f'<div class="product-card" id="p-{n}" data-frames="{len(frames)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(frames)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">Galvin Green &middot; {KIND[name]} &middot; {COLOUR[name]}</div>'
            f'<div class="product-name">{name} &middot; {price}</div>'
            f'<div class="product-desc">{CARD[name]}</div>'
            f'<a href="{p["url"]}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


def section(g, n0):
    key, tag, h2, anchor, kicker = g
    ps = [p for p in PICKS if p["group"] == key]
    cards = "\n".join(card(p, n0 + i) for i, p in enumerate(ps))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{tag}</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid">\n{cards}\n    </div>\n</section>\n'), n0 + len(ps)


PROSE = 'style="max-width:760px;font-size:16px;line-height:1.7;"'

TAKE = f"""
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Galvin Green makes clothes for the weather Austin gets for a few weeks each winter, and makes them with more care than anyone we know. The brand is Swedish, family-owned and has done nothing but golf since 1990, which shows in how finely it grades a cool morning: three weights of windproof, three weights of insulation, and a name on every garment that tells you which is which.</p>
    <p>We left the parkas and the heavy winter shells on the rail. Austin does not need them. What it needs is the stuff for a 7:40 tee time that starts in a vest and finishes in a polo, and that is where this brand is strongest.</p>
    <p>Start with Larry, the $199 half-zip windbreaker, and wear it over a Marty polo at $99. Add Del, the $99 thermal vest, on the one morning a front comes through. Keep Adam, the half-zip rain pullover, for the day it pours, and live in Noah pants the rest of the year.</p>
    <h2 class="products-hdr btk-story-hdr">The Story</h2>
    <p>Galvin Green was founded in 1990 in V&auml;xj&ouml;, a small city in southern Sweden, by Tomas Nilsson, an entrepreneur and weekend golfer. Mats Lundqvist designed the first range that summer and went on to lead design as Creative Director. The company is still owned by Nilsson; in September 2025 his son Martin, who started in the warehouse more than twenty years ago, took over as CEO.</p>
    <p>The problem they set out to solve was rain. Golf waterproofs in 1990 were heavy, swing-restricting rain suits in black and navy, and by the brand&rsquo;s account they did not reliably keep water out. Nilsson and Lundqvist went to the best membrane available, GORE-TEX, and made their first GORE-TEX jacket in 1992. In 2024 it launched the DRYVR&trade; waterproof collection, which uses Pertex&reg; Shield alongside GORE-TEX.</p>
    <p>The rest of the range grew out of that one question about weather. INSULA&trade; mid-layers arrived in 2004, the breathable VENTIL8&trade; shirts in 2010 and the INTERFACE-1&trade; windproof line in 2018. The brand stacks them into a layering system it calls Comfort Combinations, which runs from the base layer out to the rain shell.</p>
    <p>You may know the name from the Ryder Cup. Galvin Green was the official weatherwear supplier to Team Europe in 2016 and 2018. It made the rain gear; Loro Piana was the team outfitter.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>1990, V&auml;xj&ouml;, Sweden</span></div>
      <div class="sidebar-detail"><span class="l">Founder</span><span>Tomas Nilsson</span></div>
      <div class="sidebar-detail"><span class="l">CEO</span><span>Martin Nilsson, since 2025</span></div>
      <div class="sidebar-detail"><span class="l">Design</span><span>Mats Lundqvist</span></div>
      <div class="sidebar-detail"><span class="l">Owned by</span><span>The Nilsson family</span></div>
      <div class="sidebar-detail"><span class="l">US base</span><span>Alpharetta, Georgia</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$77.40&ndash;$399</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Larry half-zip windbreaker</span></div>
      <a href="https://www.galvingreen.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit Galvin Green ↗</a>
      <div class="hashtags">
        <span class="hashtag">#GalvinGreen</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#SwedishGolf</span>
        <span class="hashtag">#Layering</span>
        <span class="hashtag">#GolfStyle</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

NAMES = f"""
<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr" id="the-names">How to Read a Galvin Green Name</h2>
  <div {PROSE}>
    <p>Every Galvin Green garment has a first name, and the first letter tells you what it does. Almost every piece in the catalogue follows the rule, which turns a confusing website into a quick one once you know it.</p>
    <ul style="padding-left:22px;margin:4px 0 18px;">
      <li><strong>M</strong> is a polo. Marty, Muir, Mulligan, Medley.</li>
      <li><strong>L</strong> is INTERFACE-1&trade;, the windproof layer. Larry, Leo, Lane, Lloyd.</li>
      <li><strong>D</strong> is INSULA&trade;, the insulating mid-layer. Dixon, Del, Dean.</li>
      <li><strong>A</strong> is a waterproof shell. Adam, Aston, Air.</li>
      <li><strong>P</strong> is a pair of shorts, and <strong>N</strong> is an everyday trouser.</li>
      <li><strong>E</strong> is a SKINTIGHT&trade; base layer, and most knitwear starts with <strong>C</strong>.</li>
    </ul>
    <p>The pants follow the same logic as the tops. A waterproof trouser gets an A name, a windproof one an L, and a plain golf trouser an N. So if you want wind pants for a January morning, you are looking for an L.</p>
  </div>
</section>
"""

AUSTIN = f"""
<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr" id="austin">Why It Works in Austin</h2>
  <div {PROSE}>
    <p>Central Texas does not have much of a winter. It has a run of cold fronts between November and March, each one bringing a grey, windy morning, and then a warm afternoon two days later. A heavy jacket is wrong for almost all of it. What the season asks for is a set of light layers you can take off one at a time.</p>
    <p>Galvin Green builds its whole range around that idea. INTERFACE-1&trade; exists for the in-between: the brand claims it covers 95 rounds out of 100, and it grades each piece with a Warming Effect number from 1 to 3. INSULA&trade; uses the same scale. Pick a #1 for a crisp start and a #2 for the morning after a front.</p>
    <p>The rain gear here is the light end of the line. We have left out the insulated shells and the parkas. For a city that sees a handful of truly wet rounds a year, one packable jacket and a pair of wind pants cover most of it.</p>
  </div>
</section>
"""

PICTURES = f"""
<section class="products" style="margin-top:8px;">
  <h2 id="in-the-campaign">In the Campaign</h2>
  <p class="cat-kicker"><strong>Photography &middot; Galvin Green&rsquo;s own</strong>The brand shoots on links courses at the edges of the day, in the light Austin gets on a winter morning. The half-zip in the first frame is Adam; the group in the second wears the INSULA&trade; mid-layers.</p>
  <div class="ig-grid">
  <figure><img src="{IMG}/life-adam.jpg" alt="A golfer carrying his bag at sunset in a light blue Galvin Green Adam half-zip rain jacket" loading="lazy" /><figcaption class="ig-cap">Adam half-zip &middot; evening light</figcaption></figure>
  <figure><img src="{IMG}/life-insula.jpg" alt="Three golfers talking on a green in Galvin Green INSULA mid-layers and trousers" loading="lazy" /><figcaption class="ig-cap">INSULA mid-layers on the green</figcaption></figure>
  <figure><img src="{IMG}/life-dusk.jpg" alt="A golfer at the top of his backswing at dusk in a white and red Galvin Green jacket" loading="lazy" /><figcaption class="ig-cap">A late round on the links</figcaption></figure>
</div>
</section>
"""

FAQ = [
    ("Who owns Galvin Green?",
     "The Nilsson family. Tomas Nilsson founded the brand in 1990 and still owns it, and his son Martin Nilsson became CEO in September 2025. No sale to an outside owner has been reported."),
    ("Where is Galvin Green from?",
     "Växjö, in southern Sweden, which is still its headquarters. The US business is run from Alpharetta, Georgia, and the brand entered the US market in 2013."),
    ("What do the letters in Galvin Green product names mean?",
     "The first letter tells you the category. M is a polo, L is the INTERFACE-1 windproof line, D is INSULA insulation, A is a waterproof shell, P is shorts, N is an everyday trouser and E is a SKINTIGHT base layer. Almost every product follows the rule."),
    ("What is INTERFACE-1?",
     "Galvin Green's windproof, water-repellent layer, launched in 2018. It sits between a mid-layer and a full rain shell, and each piece is rated Warming Effect #1, #2 or #3. The brand claims it covers 95 rounds out of 100."),
    ("Is Galvin Green waterproof gear GORE-TEX?",
     "Some of it. Galvin Green made its first GORE-TEX jacket in 1992. Since 2024 its waterproof line, DRYVR, uses both GORE-TEX and Pertex Shield. On this page, Aston is GORE-TEX; Adam and Air use Pertex."),
    ("Did Galvin Green dress Team Europe at the Ryder Cup?",
     "It supplied the weatherwear in 2016 and 2018. Loro Piana was the team outfitter for those matches, so Galvin Green made the rain gear rather than the full uniform."),
    ("Does Galvin Green sizing fit American golfers?",
     "The brand's creative director has said early US customers found the European sizing off, and that the feedback has since turned good. For the mid-layers, Galvin Green itself suggests sizing up for a looser fit."),
    ("How much does Galvin Green cost?",
     "On 24 September 2026 the pieces on this page ran from $77.40 for Paul shorts on markdown to $399 for the Adam and Aston rain jackets. Polos were $99 to $129 and the wind layers $169 to $209."),
]


def faq_html():
    rows = "\n".join(
        f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>'
        for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')


def head_top():
    art = {
        "@context": "https://schema.org", "@type": "Article", "headline": TITLE,
        "description": DESC, "url": URL, "image": f"https://thegrassyissue.com{IMG}/hero.jpg",
        "datePublished": "2026-09-24", "dateModified": "2026-09-24",
        "author": {"@type": "Organization", "name": "The Grassy Issue"},
        "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": URL},
    }
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
        {"@type": "ListItem", "position": 2, "name": "Drops & Brands", "item": "https://thegrassyissue.com/#feed"},
        {"@type": "ListItem", "position": 3, "name": "Galvin Green", "item": URL}]}
    t, d = H.escape(TITLE, quote=True), H.escape(DESC, quote=True)
    og = f"https://thegrassyissue.com{IMG}/hero.jpg"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{t}</title>
<meta name="description" content="{d}" />
<link rel="icon" href="/favicon.ico" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
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
<link rel="preload" as="image" href="{IMG}/btk-hero.jpg" />
<script type="application/ld+json">
{json.dumps(art, indent=1, ensure_ascii=False)}
</script>
<script type="application/ld+json">
{json.dumps(faq, indent=1, ensure_ascii=False)}
</script>
<script type="application/ld+json">
{json.dumps(crumbs, indent=1, ensure_ascii=False)}
</script>
"""


def main(apply_):
    d = DONOR.read_text(encoding="utf-8")
    style_at = d.index("<style>")
    body_at = d.index('<div class="breadcrumb">')
    tail_at = d.index('<div class="more" data-brandindex="1">')
    head_rest = d[style_at:body_at]

    lo, hi = min(p["usd"] for p in PICKS), max(p["usd"] for p in PICKS)
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Galvin Green</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>September 24, 2026</span><span class="dot"></span>
    <span>V&auml;xj&ouml;, Sweden &middot; est. 1990</span><span class="dot"></span>
    <span>{len(PICKS)} pieces &middot; {money(lo)}&ndash;{money(hi)}</span>
  </div>
</header>

<section class="drop-hero">
  <img class="drop-hero-img" src="{IMG}/btk-hero.jpg" alt="A lone golfer carrying his bag along a links fairway beside the water at dusk, from Galvin Green&rsquo;s campaign" fetchpriority="high" />
</section>
"""
    body += TAKE + pq("nilsson") + NAMES + AUSTIN + pq("compromise") + PICTURES
    n = 1
    order = {g[0]: g for g in GROUPS}
    s, n = section(order["polo"], n); body += s + pq("fit")
    s, n = section(order["wind"], n); body += s + pq("insula")
    s, n = section(order["mid"], n); body += s
    s, n = section(order["rain"], n); body += s + pq("design")
    s, n = section(order["core"], n); body += s
    body += faq_html()

    out = head_top() + head_rest + body + d[tail_at:]
    print(f"  {n-1} cards, {len(PQ)} pull-quotes, {len(FAQ)} FAQs, range {money(lo)}-{money(hi)}")
    if not apply_:
        print("  dry run — pass --apply")
        return
    OUT.write_text(out, encoding="utf-8")
    verify()


def verify():
    fin = OUT.read_text(encoding="utf-8")
    bad = []
    if "Manors" in re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S):
        bad.append("Manors text leaked into the Galvin page above the More block")
    if fin.count('class="product-card"') != len(PICKS):
        bad.append("card count")
    for k, (t, a) in PQ.items():
        if fin.count(t[:60]) != 1:
            bad.append(f"pull-quote {k} appears {fin.count(t[:60])}x")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", fin), re.I):
        bad.append("banned word")
    if re.search(r"dressed Team Europe|team outfitter to Europe", fin):
        bad.append("Ryder Cup overstated")
    for p in PICKS:
        for f in p["local"]:
            if not (ROOT / f.lstrip("/")).is_file():
                bad.append(f"missing {f}")
    for f in ("btk-hero", "hero", "life-adam", "life-insula", "life-dusk"):
        if not (ROOT / f"images/galvin-green/{f}.jpg").is_file():
            bad.append(f"missing {f}.jpg")
    if bad:
        OUT.unlink()
        sys.exit("! removed. " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
