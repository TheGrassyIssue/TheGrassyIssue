#!/usr/bin/env python3
"""build-bunx-btk.py — Brand to Know: BUNX Golf. 20 October 2026. Cloned from build-uk-six.py.
Lenny: "Let's do a brand to know - https://www.bunxgolf.com/" ... "Looks good, let's bring in a ton of IRL photos and look book stuff."
FACTS: bunxgolf.com products.json (USD, Oct 20 2026); About page (Logan & Paige Bailey, Utah); MyGolfSpy Aug 28 2026 (Tyler Allred:
hats $34-$38, cowboy/rodeo/camo; V01 tee ~10 bends to break, 27 for $13 / $10 short). IRL photos: BUNX's own Instagram (@bunxgolf)
and site banners; captions quote BUNX's own post captions. Bundles (towel/pouch + tees) left out as duplicates. Founding year not stated (only a 3rd-party DB).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "BUNX Golf: Rodeo Golf Hats and Overbuilt Gear From Utah"
DESC = ("Brand to Know: BUNX Golf, the Utah husband-and-wife brand behind Long Iron Country, the Tex and Rough Rodeo hats, "
        "magnetic towels, a forever divot tool and tees that bend instead of snapping. 22 picks, $10 to $57.")
H1 = "Brand to Know: BUNX Golf"
BC = "BUNX Golf"
SLUG = "brand-to-know-bunx-golf"
IMG = "/images/bunx"
SHOP = "https://www.bunxgolf.com/products/"
B = "BUNX Golf"
P = {
 "h1": ("BUNX Golf", 'Long Iron Country', '$38', 'long-iron-country-golf-hat',
   'Our pick. BUNX&rsquo;s line: long irons went out of style the same year hybrids showed up, and this one is for the holdouts who still take a 3-iron off the tee. High-crown cotton A-frame snapback in camo with natural or chocolate with black.'),
 "h2": ("BUNX Golf", 'Rough Rodeo', '$38', 'rough-rodeo-golf-hat',
   'A heavy woven patch with a flying pig on it, because, per BUNX, anything&rsquo;s possible from a bad lie. Natural cotton with a black microfiber suede brim, or all black with red.'),
 "h3": ("BUNX Golf", 'BUNX Fort Worth', '$38', 'bunx-fort-worth-golf-hat',
   'Yellow chain-stitch script on natural cotton, for the city BUNX calls the beaten stepchild of Dallas and the place where ball striking was invented. The black duck-canvas version was sold out when we checked.'),
 "h4": ("BUNX Golf", 'Club Champ', '$38', 'club-champ-golf-hat',
   'Green cotton corduroy with gold chain-stitch embroidery. The copy: my mom thinks I&rsquo;m a club champ, and that&rsquo;s all that matters.'),
 "h5": ("BUNX Golf", 'The Tex', '$38', 'texas-wedge-golf-hat',
   'Named for the Texas wedge, putting from off the green. Muted camo or charcoal black. The camo one already made <a href="/drops/the-camo-edit" style="border-bottom:1px solid var(--ink)">our Camo Edit</a>.'),
 "h6": ("BUNX Golf", 'TOC (Cashmere Caddie)', '$38', 'cashmere-caddie',
   '&ldquo;Soft name, sharp game.&rdquo; Cashmere Caddie script over a tee graphic, in four colorways: natural with green corduroy, chocolate, dark green, or natural with blue and red.'),
 "h7": ("BUNX Golf", 'Sandy Pars', '$38', 'bunx-golf-hat-sandy-pars-snapback',
   'For the best feeling in golf, according to BUNX: picking the bunker shot clean and tapping in for par. Muted camo or jet black.'),
 "h8": ("BUNX Golf", 'Big Sky Birds', '$38', 'bunx-golf-hat-big-sky-birds',
   'A Montana patch hat on the theory that you won&rsquo;t find a sky bigger than a Montana sky. Blue with the red patch was the colorway in stock.'),
 "h9": ("BUNX Golf", 'Moonlit Mulli', '$38', 'bunx-golf-hat-moonlit-mulligan',
   'A javelina, the desert-course legend that acts like it owns the place, on a Moonlit Mulligans club crest. Cool slate, brown corduroy or white with a green brim.'),
 "h10": ("BUNX Golf", 'BUNX B', '$38', 'bunx-golf-hat-signature-b-a-frame',
   'A starter once told BUNX they looked like baseball players, not golfers. They took it personally and made a B hat. Five colorways from deep camo to Dodger blue.'),
 "h11": ("BUNX Golf", 'Golf Dept', '$34', 'golf-dept',
   'Golfing Dept. printed upside down across the front. BUNX says it&rsquo;s not a misprint, it&rsquo;s a mind game. Green, or natural with a red brim.'),
 "f1": ("BUNX Golf", 'Tex Father + Son', '$57', 'tex-camo-adult-youth',
   'An adult and a youth Tex in matching camo, built identically &ldquo;because that&rsquo;s the entire point.&rdquo; The youth hat alone is $28.'),
 "f2": ("BUNX Golf", 'TOC Father + Son', '$57', 'toc-father-son',
   'The same idea in corduroy: adult and youth Cashmere Caddie hats that actually match. Youth on its own is $28.'),
 "w1": ("BUNX Golf", 'Magnetic Towel, Technical Typography', '$35', 'bunx-golf-towel-technical-typography',
   'Our towel pick. For the golfer who doesn&rsquo;t need a loud graphic: a magnetic tab, an integrated scrub pad and small technical type. Stealth black, pure white or dust.'),
 "w2": ("BUNX Golf", 'Magnetic Towel, Squiggy', '$35', 'bunx-golf-towel-squiggy-abstract',
   'A squiggle pattern over the same magnetic hub and groove-cleaning scrub pad. Turf green or polar blue.'),
 "w3": ("BUNX Golf", 'Magnetic Towel, Sandy Breakfast Club', '$35', 'bunx-golf-towel-sandy-breakfast-club',
   'For the early tee-time crew, with the Sandy Breakfast Club insignia on a white camo towel.'),
 "w4": ("BUNX Golf", 'Magnetic Towel, Dat&rsquo;s Good', '$35', 'bunx-golf-towel-dats-good-gimme-ruler',
   'Printed with a &ldquo;Dat&rsquo;s Good&rdquo; gimme ruler so nobody argues over a generous concede again.'),
 "w5": ("BUNX Golf", 'Magnetic Towel, Camo', '$35', 'bunx-golf-towel-camo',
   'Per BUNX, for when your ball&rsquo;s in the forest and you can&rsquo;t let your partner see you giving it a quick clean. Camo with a ScrubCore pad.'),
 "w6": ("BUNX Golf", 'Magnetic Towel, Cart Path Only', '$35', 'bunx-golf-towel-cart-path-only-rebel',
   'BUNX doesn&rsquo;t condone breaking the rules, but sometimes cart path only really blows. Green, with the rule printed down the side.'),
 "t1": ("BUNX Golf", 'DRT Divot Repair Tool', '$45', 'drt-divot-repair-tool',
   'CNC-machined stainless, PVD coated, laser etched and magnetic. BUNX guarantees you&rsquo;ll pass it down on your deathbed or be buried with it. Six colorways in stock.'),
 "t2": ("BUNX Golf", 'V01 Tees, 27 Pack', '$13', 'bunx-v01-tee',
   'Bendy tees: MyGolfSpy&rsquo;s tester needed about ten back-and-forth bends to break one. Ten colors at 2.75 inches, plus a 1.5-inch pack for $10.'),
 "t3": ("BUNX Golf", 'Scrub Pouch', '$18', 'scrub-pouch',
   'A clip-on pouch with a scrub surface, sized, BUNX says, to clean irons, woods and balls without getting in the way. Fill it, scrub it, play golf.'),
}
SECTIONS = [
 ("The Hats", "hats", ["h1","h2","h3","h4","h5","h6","h7","h8","h9","h10","h11"],
  "<strong>Eleven hats &middot; $34&ndash;$38</strong>Every one is a structured five-panel A-frame snapback, and every one has a story printed on the product page that reads like a golfer wrote it. Colorways are grouped in each card; swipe through."),
 ("Father + Son", "father-son", ["f1","f2"],
  "<strong>Two sets &middot; $57 each</strong>Matching adult and youth hats, sold together."),
 ("The Towels", "towels", ["w1","w2","w3","w4","w5","w6"],
  "<strong>Six magnetic towels &middot; $35 each</strong>Each has a magnetic hub that sticks to the club head or cart and a built-in scrub pad for grooves. The graphics are where BUNX has fun."),
 ("Tools &amp; Tees", "tools", ["t1","t2","t3"],
  "<strong>Three pieces &middot; $13&ndash;$45</strong>The over-engineered small stuff. BUNX also sells the towel and the pouch bundled with a pack of tees."),
]
N = 22
PQ = {
 "hats": ("Before a BUNX hat gets made, it gets overthought&hellip; like really, really overthought.", "BUNX Golf, on Instagram"),
 "towels": ("Golf is rarely played from the fairway.", "BUNX Golf, on Instagram"),
 "tools": ("We started BUNX to raise the standard. No gimmicks. No shortcuts.", "Logan and Paige Bailey, BUNX founders"),
}
CAP = "Photography &middot; BUNX Golf"
BANDS = {
 "hats": ("In the dunes", "BUNX shoots a lot of its gear in sand, which is on brand for a company whose hashtag is #embracethebunker.",
   [("irl-dep16pshdyk","A golfer lying on a square of turf in the middle of sand dunes","&ldquo;Does this count as a beach day?&rdquo;"),
    ("irl-dbb9m8ogeul","A golfer in a BUNX hat sitting in the sand with an iron","&ldquo;Timeless golf gear. For the committed.&rdquo;"),
    ("irl-dy-yrwzhol2","A golfer swinging at the top of a sand dune","&ldquo;Swing smooth.&rdquo;")]),
 "towels": ("On people", "Real people in BUNX hats, from BUNX&rsquo;s Instagram.",
   [("irl-defvpibxldz","A man in a pink shirt and a Cashmere Caddie hat at a cafe table","Cashmere Caddie at lunch"),
    ("irl-drh6dx2aa98","A smiling woman in a camo BUNX hat in a golf cart by a lake","&ldquo;It&rsquo;s birdie hunting season!&rdquo;"),
    ("irl-dliibpyp5iq","A woman pulling down the brim of a Cashmere Caddie hat","Cashmere Caddie, blue brim")]),
 "tools": ("On the course", "Sand, snow and a desert flagstick.",
   [("irl-dyiklkqelb-","A golfer lying face-down in a bunker next to the flagstick and ball","&ldquo;Sandy Golfer in the dunes&rdquo;"),
    ("irl-dvj0dbaerkw","A golfer celebrating by the flag on a desert course","A first hole-in-one, in a BUNX hat"),
    ("irl-drnbeteerwv","A man in a camo BUNX hat in a snowy pine forest","&ldquo;Sunshine or snow.&rdquo;")]),
}
PROSE = 'style="max-width:760px;font-size:16px;line-height:1.7;margin:0 auto 24px;"'
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>BUNX Golf is a husband-and-wife hat company from Utah that writes better Texas jokes than most Texas brands. Logan and Paige Bailey say they knew they were committed the day Paige came home with her own set of clubs. They started BUNX because they were tired of brands slapping &ldquo;an AI-generated logo on the same crappy products&rdquo; and calling it premium. That&rsquo;s a big swing for a small brand. After going through everything they make, we think they mostly back it up.</p>
    <p><strong>The hats are the point.</strong> Every one is the same structured five-panel A-frame snapback at $34 to $38, and the names do the selling. Long Iron Country is for the holdouts still hitting 3-iron off the tee. Club Champ celebrates a &ldquo;hard-earned delusion.&rdquo; The Fort Worth hat calls the city the beaten stepchild of Dallas, and the Tex is named for putting from off the green. The look is rodeo and western: camo, corduroy, chain-stitch script and a flying pig. That&rsquo;s a crowded lane right now. BUNX stands out on the inside of the hat, with printed under-brims, branded taping and a woven label that just says &ldquo;You look good.&rdquo;</p>
    <p><strong>A hat built to be destroyed.</strong> Here&rsquo;s what we want from a golf hat: design and construction good enough that we can absolutely beat it up. Sweat, sun, rain delays, the floor of the cart, the back seat of the car. A cheap hat just falls apart. A well-made one breaks in, and six months later it looks perfectly worn in and like nobody else&rsquo;s. That&rsquo;s the bar for a $38 hat, and a structured cotton crown with real chain-stitch embroidery is what you want for it.</p>
    <p><strong>Then they overbuild the small stuff.</strong> The towels have a magnetic hub and a built-in scrub pad. The DRT divot tool is CNC-machined stainless steel with a PVD coating, and BUNX jokes you&rsquo;ll be buried with it. The V01 tees bend instead of snapping; MyGolfSpy&rsquo;s tester needed about ten back-and-forth bends to break one. To be fair, at roughly 48 cents a tee they only pay off if you break more tees than you lose.</p>
    <p><strong>It feels made for Texas.</strong> The Tex and the Fort Worth hat are the obvious ones, but the whole range fits here: a desert javelina on the Moonlit Mulli, camo that already showed up in <a href="/drops/the-camo-edit"LS>our Camo Edit</a>, and hats you can wear to a muni at 7am and a patio at 7pm. The Father + Son sets are a smart touch for anyone bringing a kid to the range.</p>
    <p>If you buy one thing, get the Long Iron Country in camo and natural. If you buy two, add the DRT.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Founders</span><span>Logan &amp; Paige Bailey</span></div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Utah</span></div>
      <div class="sidebar-detail"><span class="l">Hats</span><span>$34&ndash;$38</span></div>
      <div class="sidebar-detail"><span class="l">Towels</span><span>$35, magnetic</span></div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>22, all in stock</span></div>
      <div class="hashtags">
        <span class="hashtag">#BUNXGolf</span>
        <span class="hashtag">#GolfHats</span>
        <span class="hashtag">#BrandToKnow</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
""".replace('"LS>', '" style="border-bottom:1px solid var(--ink)">')
FAQ = [
 ("Where is BUNX Golf based?", "Utah. BUNX was started by husband and wife Logan and Paige Bailey."),
 ("How much are BUNX Golf hats?", "Adult hats were $34 to $38 on October 20, 2026. Youth hats were $28, and matching Father + Son sets were $57."),
 ("Are BUNX V01 tees really unbreakable?", "They bend rather than snap. In MyGolfSpy's test it took about ten back-and-forth bends to break one. A 27-pack costs $13 for 2.75-inch tees or $10 for 1.5-inch."),
 ("What is the BUNX DRT?", "A $45 divot repair tool CNC-machined from stainless steel, PVD coated, laser etched and magnetic, sold in several colorways."),
]
LOOK = [
 ("irl-depzwyyxklx","A man in a camo BUNX hat looking up against a gray wall","&ldquo;Look good from every angle.&rdquo;"),
 ("irl-drkup9jkskp","A man in a white T-shirt and a BUNX hat leaning on a club","On the bunker set"),
 ("irl-do1tvwdett6","Musician Clayton Mullen singing on stage in the camo Tex","Clayton Mullen in the Camo Tex"),
 ("irl-dmdyom9rnx7","A man with the Caddie hat pulled low over his eyes","&ldquo;Turning heads both on and off the course.&rdquo;"),
 ("irl-drahqioky4h","A hand holding the Moonlit Mulligans hat against a sand-colored wall","&ldquo;Embrace the bunker.&rdquo;"),
 ("irl-dkxmt-ipbwz","A hand holding the Texas Wedge hat over grass","&ldquo;Loft is optional. Looking good isn&rsquo;t.&rdquo;"),
 ("irl-dzdpiibkhko","The Fort Worth hat lying on its technical drawings","&ldquo;It gets overthought.&rdquo;"),
 ("irl-dj2g2h9p9o4","Cashmere Caddie and Golfing Dept hats laid out on a white table","The launch lineup"),
 ("irl-dhhxcooj2bs","A pile of BUNX bags printed Just a hat.","&ldquo;Just a hat.&rdquo;"),
 ("irl-hatpour","A hand pouring sand out of a camo Sandy Pars hat","Sandy Pars, emptied"),
 ("irl-founders-flag","Two people walking across dunes at night carrying a BUNX flag","From the founders&rsquo; page"),
 ("irl-dek7njsbwmw","The woven label inside a blue BUNX hat reading You look good.","&ldquo;Like really, really good.&rdquo;"),
]
_figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{a}" loading="lazy" /><figcaption class="ig-cap">{c}</figcaption></figure>' for f, a, c in LOOK)
LOOKBOOK = f"""
<section class="products" style="margin-top:8px;">
  <div class="drop-tag grass">Lookbook</div>
  <h2 class="products-hdr" id="lookbook">In the Wild</h2>
  <p class="cat-kicker"><strong>From BUNX&rsquo;s feed &middot; twelve photos</strong>Dunes, bunkers, a concert stage and the drafting table, with captions in BUNX&rsquo;s own words where they wrote them.</p>
  <div class="ig-grid">
{_figs}
  </div>
</section>
"""
FRN = json.loads((ROOT / "research/bunx/frames.json").read_text())
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
         "url": URL, "image": og, "datePublished": "2026-10-20", "dateModified": "2026-10-20",
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
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Brand to Know &middot; Utah &middot; Logan &amp; Paige Bailey</span><span class="dot"></span>
    <span>22 picks &middot; prices checked October 20, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A golfer in a blue BUNX patch hat sitting in rippled desert sand with an iron across his knees and his glove beside him" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
    body += LOOKBOOK
    body += faq_html()
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Kalamunda", "Parmore", "Sounder", "Casualist", "Dim Sum", "Rowena", "Metalwood", "Climber", "Woodgrain", "Rookline", "Bethpage", "LBB", "GolfPass"):
        if leak in above: bad.append("leak " + leak)
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
