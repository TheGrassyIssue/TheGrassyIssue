#!/usr/bin/env python3
"""build-hat-brands.py — Off the Rack, Off the Radar: Six Hat Brands to Know.
5 October 2026. Lenny: "using this instagram post as a template- let's do a post about these hat brands" (site post
only): Bet on the Horses, Engel, Represent, Orién, Freddy Tyler Paul, then "add some of these from this brand as well"
(F AND CO.). Title option 2, then "beef up the post with good lifestyle images and short blurbs about each brand with
4-5 hats per brand". Engel makes three caps in total, so its section has three.

FACTS: research/hat-brands/options.json (each brand's own store, 5 Oct 2026) and the brands' own story pages.
Non-USD prices in store currency with an approximate dollar figure (EUR 1.17, AUD 0.66).
PHOTOS: brands' own store and site images, localised to /images/hat-brands by research/hat-brands/make_frames.py.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "hat-brands-off-the-rack-off-the-radar"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/hat-brands"
FRN = json.loads((ROOT / "research/hat-brands/frames.json").read_text())

TITLE = "Off the Rack, Off the Radar: Six Hat Brands to Know"
DESC = ("Six independent hat brands from Los Angeles, Amsterdam, Manchester and Queensland: 27 caps and truckers from B.O.T.H., Engel, Represent, Orién, Freddy Tyler Paul and F AND CO., with prices.")
H1 = TITLE

BOTH, ENG, REP, ORI, FTP, FCO = "B.O.T.H.", "Engel", "Represent", "Ori&eacute;n", "Freddy Tyler Paul", "F AND CO."
SO = " &middot; sold out"

# code -> (brand, item, price, url, copy)
P = {
 "BOTH1": (BOTH, "Berry Hills Cap, Red", "$80", "https://betonthehorses.co/products/berry-hills-cap-red",
   "An unstructured cap with the logo in puff print, so the letters stand up off the front. Snapback closure. The red is the loud one of the set."),
 "BOTH2": (BOTH, "Lodi Trucker Cap", "$80", "https://betonthehorses.co/products/berry-hills-cap-1",
   "This is a heavyweight cotton twill trucker with mesh back panels and Bet On The Horses embroidered over a running horse on the front. Adjustable strap."),
 "BOTH3": (BOTH, "Berry Hills Cap, Black", "$80" + SO, "https://betonthehorses.co/products/berry-hills-cap",
   "The same puff-print, unstructured cap as the red, in black. It has sold out; the red is still in stock."),
 "BOTH4": (BOTH, "Ranch Cap, Dust", "$90" + SO, "https://betonthehorses.co/products/ranch-cap-dust",
   "Heavy cotton twill with distressing and paint splatter, so no two are the same, and B.O.T.H. embroidery on the front, the side panel and the back. Sold out for now."),
 "BOTH5": (BOTH, "Ranch Cap, Washed Blue", "$90" + SO, "https://betonthehorses.co/products/wrangler-cap",
   "This is the Ranch Cap in washed blue. It sold out during early access, and the store says a restock is coming."),
 "ENG1": (ENG, "Engel Racing Cap, Burnt Yellow", "&euro;59 (~$69)", "https://engelleisure.com/products/engel-racing-cap-burnt-yellow",
   "Five panels of cotton twill with the Engel Racing logo in wool felt on the front, modelled on old racing-team caps. It closes with a real leather strap."),
 "ENG2": (ENG, "Engel Racing Cap, Desert Brown", "&euro;59 (~$69)", "https://engelleisure.com/products/engel-racing-cap-desert-brown",
   "This one pairs a cream crown with a desert-brown brim, which goes with everything in a fall golf wardrobe. It has the same leather strap and short brim, in one size."),
 "ENG3": (ENG, "Team Engel Cap, Vintage Navy", "&euro;59 (~$69)" + SO, "https://engelleisure.com/products/team-engel-cap-vintage-navy",
   "Unstructured and washed to look worn in, with a gold crest and olive branches embroidered on the front. Sold out for now."),
 "REP1": (REP, "Owners Club Cap, Weathered Black", "$60", "https://representclo.com/products/represent-owners-club-cap-weathered-black",
   "An unstructured five-panel cap in coastal-washed cotton twill, so it feels broken in from the first wear. The cheapest way into Represent."),
 "REP2": (REP, "Represent x &rsquo;47 EngLAnd Old English Cap, Washed Navy", "$110", "https://representclo.com/products/represent-x-47-england-old-english-cap-washed-navy",
   "Built with &rsquo;47 on its HITCH shape, sun-faded and distressed, with Old English lettering chain-stitched in flat white."),
 "REP3": (REP, "Represent x &rsquo;47 EngLAnd Cap, Aged Black", "$110", "https://representclo.com/products/represent-x-47-england-cap-aged-black",
   "It is the same faded HITCH cap in aged black, with the lettering in a Chicano-inspired script for the Los Angeles side of the collection."),
 "REP4": (REP, "Represent x &rsquo;47 Initial Cap, Charcoal", "$65", "https://representclo.com/products/represent-x-47-initial-cap-charcoal",
   "This is the clean one, with a structured crown, a raised R embroidered on the front and Represent script on the side."),
 "REP5": (REP, "Represent x &rsquo;47 Dodgers Cap, Vintage Blue", "$110", "https://representclo.com/products/represent-x-47-mlb-la-cap-vintage-blue",
   "A Dodgers cap on the &rsquo;47 HITCH shape, given Represent&rsquo;s distressed finish so it looks like it has been in the back window of a car for years."),
 "ORI1": (ORI, "The Studio", "$50", "https://shoporien.com/products/the-studio",
   "The Studio is a five-panel cap in aged rust with the logo in aged black embroidery. The fading and distressing are done one at a time, so every one is different."),
 "ORI2": (ORI, "The Archive", "$50", "https://shoporien.com/products/the-crest",
   "The Archive has six panels in aged grey with white embroidery, and each one is hand distressed and labelled by hand."),
 "ORI3": (ORI, "The Atelier", "$50", "https://shoporien.com/products/the-atelier-hat",
   "The Atelier comes in aged black with white embroidery and only light distressing, with a snapback closure and hand-stitched tags inside."),
 "ORI4": (ORI, "The Thrashed Atelier", "$50", "https://shoporien.com/products/aged-black-atelier-cap",
   "This takes the Atelier further, with heavier hand distressing on the same aged black cap."),
 "FTP1": (FTP, "&lsquo;Let Me Steer You to Austin&rsquo; Hat", "$39", "https://freddytylerpaul.com/products/let-me-steer-you-to-austin-hat",
   "A five-panel snapback in cotton canvas with a mesh back, and the one we had to include. A pre-curved brim, mid profile."),
 "FTP2": (FTP, "&lsquo;Quality You Can Feel&rsquo; Hat", "$39", "https://freddytylerpaul.com/products/quality-you-can-feel-hat",
   "The same mid-profile snapback with a mesh back and a slogan that sounds like it came off a feed-store sign."),
 "FTP3": (FTP, "&lsquo;Haven&rsquo;t Been There&rsquo; Hat", "$39", "https://freddytylerpaul.com/products/havent-been-there-hat",
   "This is the soft one, an unstructured six-panel dad hat in cotton with a metal clasp."),
 "FTP4": (FTP, "&lsquo;The Best Thing&rsquo; Hat", "$39", "https://freddytylerpaul.com/products/the-best-thing-hat",
   "It is cotton canvas and mesh with five panels and a plastic snap, and Freddy&rsquo;s embroidery does the work."),
 "FTP6": (FTP, "&lsquo;Freddy&rsquo;s Antique &amp; Vintage&rsquo; Hat", "$39", "https://freddytylerpaul.com/products/freddy-s-antique-vintage",
   "A fake antique-shop logo, sold as a mesh-back snapback or an unstructured dad hat. Pick your shape."),
 "FCO1": (FCO, "Vintage Cord Cap, Red", "A$69 (~$45)", "https://fandco.co.nz/products/vintage-cord-cap-5-panel-red",
   "The cap is heavy washed red corduroy in the short-brim, unstructured five-panel shape, with a relaxed script logo in flat and raised embroidery."),
 "FCO2": (FCO, "Picnic Letterman Cap, Green/White Gingham", "A$69 (~$45)", "https://fandco.co.nz/products/picnic-letterman-cap-short-brim-6-panel-green-white-plaid",
   "Green and white gingham cotton on a short-brim six-panel, sold distressed or clean. The summer one."),
 "FCO3": (FCO, "Winter Plaid Cap, Brown", "A$69 (~$45)", "https://fandco.co.nz/products/winter-plaid-cap-short-brim-5-panel-brown",
   "It is heavy brown plaid cotton with a low, rounded six-panel crown and a buckle strap. Part of the Winter Resort collection."),
 "FCO6": (FCO, "Vintage Trucker Cap, Washed Sea Green", "A$69 (~$45)", "https://fandco.co.nz/products/vintage-trucker-cap-wide-brim-5-panel-washed-sea-green",
   "It puts washed sea-green canvas and mesh panels on the brand&rsquo;s ball-trucker shape, pre-curved brim and snapback."),
 "FCO7": (FCO, "F&hearts;C Cap, Blue Pinstripe", "A$69 (~$45)", "https://fandco.co.nz/products/f%E2%9D%A4c-cap-5-panel-blue-pinstripe",
   "It pairs fine blue pinstripe cotton with an Old English monogram and a sketched heart, on the standard five-panel with a mid-length brim."),
}

# (h2, anchor, ids, kicker, band key, loc)
SECTIONS = [
    ("B.O.T.H. (Bet On The Horses)", "both", ["BOTH1", "BOTH2", "BOTH3", "BOTH4", "BOTH5"],
     "<strong>Los Angeles &middot; $80&ndash;$90</strong>Collin McMannis started Bet On The Horses in Los Angeles in 2026, and the name is about the wager, not the animal: walking away from the safe job to bet on yourself. The clothes pull from American style of the 80s, 90s and 2000s, and the brand is clear that it is &ldquo;Not cosplay cowboy.&rdquo; The caps are heavy cotton twill with puff print or embroidery, and three of these five have already sold out. Collection 02 drops on 7 October.",
     "both"),
    ("Engel", "engel", ["ENG1", "ENG2", "ENG3"],
     "<strong>Amsterdam &middot; &euro;59 (~$69)</strong>Engel Leisure is designed in Amsterdam and makes caps in runs limited to 150 pieces. Every one is cotton twill with a leather strap and a short brim, and the idea is a cap that gets better the longer you own it. There are only three on the store right now: two racing caps and a washed navy crest cap that has sold out.",
     "engel"),
    ("Represent", "represent", ["REP1", "REP2", "REP3", "REP4", "REP5"],
     "<strong>Manchester &middot; $60&ndash;$110</strong>Brothers George and Mike Heaton started Represent in Manchester in 2011 as a college project, screen printing graphics onto blank clothing. It is now one of Britain&rsquo;s biggest streetwear labels, with shops in London, Manchester and Los Angeles. The caps are the easy way in, and four of these come from its run with &rsquo;47, faded and distressed so they look old on day one.",
     "represent"),
    ("Ori&eacute;n", "orien", ["ORI1", "ORI2", "ORI3", "ORI4"],
     "<strong>Made to order &middot; $50</strong>Ori&eacute;n is Ben Selby&rsquo;s studio, and it makes caps slowly, in small batches, each one aged and distressed by hand. The brand puts its idea in one line: &ldquo;Minimal luxury, to us, isn&rsquo;t an aesthetic. It&rsquo;s a filter.&rdquo; All four caps are $50, made to order and on pre-order now.",
     "orien"),
    ("Freddy Tyler Paul", "freddy-tyler-paul", ["FTP1", "FTP2", "FTP3", "FTP4", "FTP6"],
     "<strong>Los Angeles &middot; $39</strong>Freddy Tyler Paul is a musician and photographer from Chicago who moved to Los Angeles in 2020 and taught himself to screenprint and embroider so he could sell clothes alongside his records. His hats are the funniest here, every one $39, and one of them tells you to steer to Austin.",
     "ftp"),
    ("F AND CO.", "f-and-co", ["FCO1", "FCO2", "FCO3", "FCO6", "FCO7"],
     "<strong>Queensland &middot; A$69 (~$45)</strong>F AND CO. is from Burleigh Heads on Australia&rsquo;s Gold Coast and only makes headwear, under the line &ldquo;A Considered Approach to Contemporary Headwear.&rdquo; Shape and fit come first, and every cap goes through rounds of sampling. The short-brim corduroy, gingham, plaid and pinstripe caps here are the most golf-ready shapes in the post.",
     "fandco"),
]

CAP = "Photography &middot; the brand&rsquo;s own"
BANDS = {
    "both": (CAP, "B.O.T.H. shoots its caps with black tees and wild horses.",
             [("band-both-1", "A man in a faded teal Bet On The Horses cap pulled down over his eyes", "B.O.T.H."),
              ("band-both-2", "A man in a black B.O.T.H. trucker cap and black tee", "B.O.T.H."),
              ("band-both-3", "Wild horses running across dry grassland", "B.O.T.H.")]),
    "engel": (CAP, "Engel photographs its caps in the sun, leather strap and all.",
              [("band-engel-1", "Three Engel caps in white, yellow and navy on a wall above wooded hills", "Engel"),
               ("band-engel-2", "The back of a navy Team Engel cap with script embroidery and a leather strap", "Engel"),
               ("band-engel-3", "A yellow Engel Racing cap on concrete in the sun", "Engel")]),
    "represent": (CAP, "Represent shoots its campaigns in black and concrete.",
                  [("band-represent-1", "A man in a black jacket and light jeans against a concrete wall", "Represent"),
                   ("band-represent-2", "A man in a black cap and black jacket beside a concrete wall", "Represent"),
                   ("band-represent-3", "A man in a beanie and black Owners Club hoodie in a white studio", "Represent")]),
    "orien": (CAP, "Ori&eacute;n shoots its caps the way they get worn.",
              [("band-orien-1", "A man in profile wearing a distressed black Ori&eacute;n cap", "Ori&eacute;n"),
               ("band-orien-2", "A man in a black Ori&eacute;n cap, blurred in motion", "Ori&eacute;n"),
               ("band-orien-3", "A man in a black cap and sunglasses leaning against a car beside a eucalyptus tree", "Ori&eacute;n")]),
    "ftp": (CAP, "Freddy Tyler Paul wears his own hats in the brand&rsquo;s photos.",
            [("band-ftp-1", "A man in a washed black bucket hat with goose embroidery", "Freddy Tyler Paul"),
             ("band-ftp-2", "Freddy Tyler Paul in a printed shirt against an orange wall", "Freddy Tyler Paul"),
             ("band-ftp-3", "A man in a camouflage cap and tinted sunglasses", "Freddy Tyler Paul")]),
    "fandco": (CAP, "The brand takes its caps from the coast to the mountains.",
               [("band-fandco-1", "A man in a white F AND CO. cap and black hoodie", "F AND CO."),
                ("band-fandco-2", "A man in a plaid cap and puffer jacket in front of snowy mountains", "F AND CO."),
                ("band-fandco-3", "A man in a cap riding a bicycle with sunflowers in the basket", "F AND CO.")]),
}

N = 27
GRID_CSS = '<style>/*TGI-HATBRANDS-GRID*/.products-grid[data-n=\"3\"]{grid-template-columns:repeat(3,minmax(0,1fr))}.products-grid[data-n=\"4\"]{grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}.products-grid[data-n=\"5\"]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n=\"5\"]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:1024px){.products-grid[data-n=\"4\"]{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:820px){.products-grid[data-n=\"5\"]>.product-card{flex-basis:calc((100% - 24px)/2)}.products-grid[data-n=\"3\"]{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:480px){.products-grid[data-n=\"3\"],.products-grid[data-n=\"4\"]{grid-template-columns:1fr}.products-grid[data-n=\"5\"]>.product-card{flex-basis:100%}}</style>\n'

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>The pro shop sells the same five caps everywhere you go, and most of them have a club logo on the front. The good caps on the course these days come from somewhere else: small clothing labels and one-man studios that treat a hat as the main event rather than merch. This is six of them, from Los Angeles, Amsterdam, Manchester and Australia&rsquo;s Gold Coast, with four or five caps each.</p>
    <p>None of these are golf brands, and that is the point. A faded Represent cap, a corduroy short brim from F AND CO. or a racing cap from Engel looks better with a polo than another tour logo does, and every one of them goes to dinner after. The short-brim and unstructured shapes are the ones we would wear for eighteen holes; the heavy truckers are for the range and the drive there.</p>
    <h2 class="products-hdr btk-story-hdr">Small Runs, Fast</h2>
    <p>Most of these brands make caps in small numbers. Engel limits its runs to 150 pieces, Ori&eacute;n makes every cap to order and distresses it by hand, and B.O.T.H. has sold out of three of the five caps here since its first drop. Sold-out caps are marked, because they tend to come back. If you want one, do not wait for the next sale.</p>
    <p>If you only buy one, buy the Engel Racing Cap in desert brown, a cream crown with a brown brim. It is cotton twill with a real leather strap and a short brim, and it looks like something you found in a vintage shop. Prices were read on each brand&rsquo;s own store on 5 October 2026; non-US prices show an approximate dollar figure. For more, see <a href="/drops/the-hat-edit-6-lids-for-golfers-who-skip-the-pro-shop">The Hat Edit</a> and <a href="/drops/the-hat-edit-austin-summer">our Austin summer hats</a>.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>6</span></div>
      <div class="sidebar-detail"><span class="l">Caps</span><span>27</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$39&ndash;$110</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Engel Racing Cap, Desert Brown, &euro;59 (~$69)</span></div>
      <div class="sidebar-detail"><span class="l">Under $40</span><span>Every Freddy Tyler Paul hat, $39</span></div>
      <div class="sidebar-detail"><span class="l">Prices read</span><span>5 October 2026</span></div>
      <a href="#both" class="sidebar-cta">See the hats &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#GolfHats</span>
        <span class="hashtag">#Headwear</span>
        <span class="hashtag">#Menswear</span>
        <span class="hashtag">#IndependentBrands</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

FAQ = [
    ("What are the best independent hat brands?",
     "This post covers six: B.O.T.H. (Bet On The Horses) and Freddy Tyler Paul from Los Angeles, Engel from Amsterdam, Represent from Manchester, Orien, which makes every cap to order, and F AND CO. from Burleigh Heads in Queensland, which only makes headwear."),
    ("Which caps work best on the golf course?",
     "Short-brim and unstructured caps sit lowest and are easiest to wear for eighteen holes. In this post that means F AND CO.'s short-brim corduroy, gingham and plaid caps, Engel's short-brim racing caps and Represent's unstructured Owners Club Cap."),
    ("How much do these hats cost?",
     "From $39 for any Freddy Tyler Paul hat to $110 for Represent's caps made with '47. Orien's caps are $50, F AND CO.'s are A$69 (about $45), Engel's are 59 euros (about $69) and B.O.T.H.'s are $80 to $90. Prices were read on each brand's own store on 5 October 2026."),
    ("Why are some of the hats sold out?",
     "Several of these brands make caps in small numbers. Engel limits its runs to 150 pieces and B.O.T.H. sold out of three caps after its first drop. Sold-out caps are marked in the post because they often restock."),
]

def card(k, idx):
    brand, item, price, url, copy = P[k]
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


def band(key):
    kick, line, items = BANDS[key]
    figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>'
                     for f, alt, cap in items)
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <p class="cat-kicker"><strong>{kick}</strong>{line}</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


def section(sec, n0):
    h2, anchor, ids, kicker, bkey = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} hats</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n</section>\n' + band(bkey)), n0 + len(ids)


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
            items.append({"@type": "ListItem", "position": pos, "url": P[h][3], "name": H.unescape(f"{P[h][0]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-10-05", "dateModified": "2026-10-05",
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
            {"@type": "ListItem", "position": 3, "name": "Six Hat Brands to Know", "item": URL}]},
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
    ids = [k for s in SECTIONS for k in s[2]]
    assert len(ids) == N == len(set(ids)) and set(ids) == set(P), (len(ids), set(P) ^ set(ids))
    for k in ids:
        assert len(FRN.get(k, [])) >= (1 if k == "FTP1" else 2), k  # FTP1: the store has one photo
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Six Hat Brands to Know</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>B.O.T.H., Engel, Represent, Ori&eacute;n, Freddy Tyler Paul and F AND CO.</span><span class="dot"></span>
    <span>27 caps &middot; prices read 5 October 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A vintage white 4x4 parked on a road through a mountain valley, snow on the peaks and tussock grass in the foreground" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        o, n = section(s, n); body += o
    body += faq_html()
    out = head_top() + head_rest.replace('</head>', GRID_CSS + '</head>', 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    bad = []
    for leak in ("Manors Revisited", "Nicklaus", "Enron", "Ghost", "towel"):
        if leak in above: bad.append("leak " + leak)
    if fin.count('class="product-card"') != N: bad.append("card count")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", above), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
