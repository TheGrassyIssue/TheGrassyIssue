#!/usr/bin/env python3
"""build-apartments-golf-sims.py — "Austin Apartments With Golf Simulators" 14 October 2026.
Lenny: "Let's do a post about Apartment buildings in Austin with golf simulators. add a plug for my real estate services on
the post like what we have in the field guide." then "Let's build this post" (the 10 TGI picks).
FACTS: every simulator confirmed on the property's own website (amenity line quoted as written); none names a sim brand.
Rents: each property's own floor-plans page or homepage, Oct 14, 2026, base rent unless stated; blank where the property does
not publish one in static HTML. Drive distances: OSRM driving route from the property address (Nominatim geocode) to the
nearest City of Austin muni, free-flow, so real traffic is longer; labelled "about". Left out: student housing (by-the-bed
leases), The Eden at Pearson Ranch (aggregator only), Residences at 6G / Alexan Braker Pointe / The Marlowe (not confirmed).
PHOTOS: each property's own gallery (research/apt-sims/frame.py). Hero: 415 Colorado's golf simulator lounge.
LENNY NOTE: the Field Guide's editor's-note block (wire-field-guide-ad.py), TREC 535.155 elements kept: license holder,
broker (Keller Williams) at half the size of the largest contact info, IABS + Consumer Protection Notice links.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Austin Apartments With Golf Simulators: 10 Buildings With a Sim Room"
DESC = ("Ten Austin apartment buildings with a golf simulator on site, from Alexan Waterloo and 415 Colorado downtown to Mueller, "
        "Oak Hill and Manor, with starting rents and the drive to the nearest muni.")
H1 = "Austin Apartments With Golf Simulators: Ten Buildings With a Sim Room Downstairs"
BC = "Apartments With Golf Simulators"
SLUG = "austin-apartments-with-golf-simulators"
IMG = "/images/austin-apartments-golf-sims"
SHOP = ""
D = json.loads((ROOT / "research/apt-sims/drive.json").read_text())
def drive(k):
    m, mi, t = D[k]
    m = {"Lions Municipal": "Lions"}.get(m, m)
    return f"Nearest muni: {m}, about {mi:g} miles and {t} minutes in light traffic."
P = {
 "alexan": ("Downtown &middot; Waterloo Park &middot; high-rise", "Alexan Waterloo", "studios from $1,957", "https://alexanwaterloo.com/amenities/",
   "The amenity list calls it a &ldquo;Sports Lounge with Golf Simulator,&rdquo; and it sits on the 30th floor with the rest of the shared space, including a pool that looks over downtown. Right on Waterloo Park. One-bedrooms start at $2,641 base. " + drive("alexan")),
 "colorado": ("Downtown &middot; Warehouse District &middot; high-rise", "415 Colorado", "1BR from $3,690", "https://415colorado.com/",
   "The sim room is up high with floor-to-ceiling windows, the one in our hero photo. New in 2025, 328 homes, and the priciest of the ten, with up to eight weeks free when we checked. " + drive("colorado")),
 "amli": ("Mueller &middot; mid-rise", "AMLI North Park", "from $1,709", "https://www.amli.com/apartments/austin/mueller-apartments/amli-north-park",
   "AMLI puts a golf simulator inside and a putting green in the 19,000-square-foot courtyard outside; The Howard in Manor is the only other building here with both. It is also the closest to a muni: Morris Williams is about 1.7 miles away, roughly three minutes in the car."),
 "odell": ("Crestview &middot; North Lamar &middot; mid-rise", "Odell", "studios from $1,260", "https://odellatx.com/amenities/",
   "Greystar opened it in 2025 and lists the sim as &ldquo;Perfect Your Swing in the Year-Round in the Golf Simulator,&rdquo; next to a speakeasy-style game room. The cheapest way into a sim building this close to the middle of town; one-bedrooms from $1,585 base. " + drive("odell")),
 "presidium": ("Tech Ridge &middot; Northeast &middot; mid-rise", "Presidium Tech Ridge", "up to 10 weeks free", "https://presidiumtechridge.com/",
   "The site says &ldquo;Perfect your golf swing in our state-of-the-art simulator,&rdquo; and the photo shows a full bay with a hitting mat and screen. It did not publish rents in plain text when we checked, but it was offering up to ten weeks free. " + drive("presidium")),
 "shiloh": ("Oak Hill &middot; garden-style", "The Shiloh at Oak Hill", "", "https://www.theshilohapartments.com/amenities",
   "The clubhouse has a &ldquo;Recreation Room with Golf Simulator,&rdquo; and the homes sit in four-story buildings off Old Bee Caves Road. Grey Rock, a public course, is closer than any city muni. " + drive("shiloh")),
 "bridge": ("Steiner Ranch &middot; garden &amp; townhomes", "Bridge at Steiner Ranch", "2 weeks free", "https://www.bridgeatsteinerranch.com/",
   "A &ldquo;virtual indoor golf simulator&rdquo; in a dedicated room, and the gallery shows it with a stand bag parked by the mat. Some homes have attached garages, which is where your clubs want to live. " + drive("bridge")),
 "parkest": ("Far South &middot; garden-style", "Park at Estancia", "", "https://parkatestancia.com/austin/park-at-estancia/amenities/",
   "The clubhouse has a multi-sport simulator, and the copy is the best of the ten: &ldquo;tee up for a game of golf, or arm yourself against zombies.&rdquo; " + drive("parkest")),
 "viewest": ("Far South &middot; garden-style", "View at Estancia", "from $1,028", "https://viewatestancia.com/amenities/",
   "Across the street from Park at Estancia, with its own &ldquo;Multi-Sport Simulator&rdquo;; the gallery photo is titled Golf Simulator. It has the lowest starting rents of the ten. It also runs an affordability program, so ask which homes it covers. " + drive("viewest")),
 "howard": ("Manor &middot; garden-style", "The Howard", "from $1,088", "https://thehowardatx.com/amenities/",
   "The Howard is the only suburb that checked out, with an &ldquo;Indoor Golf Simulator&rdquo; plus an &ldquo;Outdoor Putting Green&rdquo; off East Howard Lane. Built in 2024. " + drive("howard")),
}
SECTIONS = [
 ("Downtown &amp; Central", "central", ["colorado", "alexan", "amli", "odell"],
  "<strong>Four buildings</strong>These are high-rise towers downtown and newer mid-rises in Mueller and Crestview, all within about ten minutes of Hancock or Morris Williams."),
 ("North", "north", ["presidium"],
  "<strong>One building</strong>This one sits in Tech Ridge, up by Parmer and I-35."),
 ("West", "west", ["shiloh", "bridge"],
  "<strong>Two buildings</strong>Both are garden-style communities in Oak Hill and Steiner Ranch, with hill country on one side and a long drive to a muni on the other."),
 ("Far South", "south", ["parkest", "viewest"],
  "<strong>Two buildings</strong>These two sit across the street from each other in far South Austin, and Roy Kizer and Jimmy Clay are the closest munis."),
 ("Just Outside Austin", "manor", ["howard"],
  "<strong>One building</strong>This one is out in Manor, east of 130."),
]
N = 10
PAIRS = {}
LIFE = []
UTM = "utm_source=thegrassyissue&amp;utm_medium=referral&amp;utm_campaign=apartments-golf-sims&amp;utm_content=apartments-golf-sims"
SITE = "https://lennyharrington.papasanproperties.com"
def lenny(where):
    sms = "sms:+19143188472?&amp;body=Hi%20Lenny%2C%20I%20found%20you%20through%20The%20Grassy%20Issue%20post%20on%20apartments%20with%20golf%20simulators.%20I%27m%20looking%20to%20rent%20in%20Austin."
    return f'''
<aside class="lre" aria-label="A note from the editor">
 <div class="lre-in">
  <img class="lre-img" src="/images/lenny/headshot.jpg" alt="Lenny Harrington" width="112" height="112" loading="lazy" />
  <div>
   <div class="lre-k">A note from the editor &middot; Lenny&rsquo;s day job</div>
   <p class="lre-h">Want one of these?</p>
   <p class="lre-p">When I&rsquo;m not writing The Grassy Issue, I&rsquo;m a real estate agent in Austin. I can tour these buildings with you, check what specials they&rsquo;re running that week and help you lease the one closest to the course you&rsquo;ll actually play. Buying or selling, too.</p>
   <a class="lre-btn" href="{sms}" data-goatcounter-click="apartments-text-lenny-{where}">Text Lenny &rarr;</a>
   <a class="lre-btn lre-btn2" href="{SITE}/property-search/results/?searchtype=3&amp;{UTM}" target="_blank" rel="noopener" data-goatcounter-click="apartments-view-listings-{where}">View listings &rarr;</a>
   <a class="lre-tel" href="tel:+19143188472">(914) 318-8472</a>
   <div class="lre-c">
    Lenny Harrington &middot; TX License 795491 &middot; Papasan Properties Group<br>
    <span class="lre-b">KELLER WILLIAMS</span> &middot; 1801 S. MoPac Expy., Ste. 100, Austin<br>
    <a href="{SITE}/res/includes/TREC-IABS.pdf?{UTM}" target="_blank" rel="noopener">Texas Real Estate Commission Information About Brokerage Services</a> &middot;
    <a href="{SITE}/assets/docs/TREC-CPN.pdf?{UTM}" target="_blank" rel="noopener">Texas Real Estate Commission Consumer Protection Notice</a><br>
    This is Lenny&rsquo;s own business. No building on this page paid TGI to be here.
   </div>
  </div>
 </div>
</aside>
'''
LRE_CSS = '''<style>/*TGI-LENNY-RE-CSS*/
.lre{max-width:880px;margin:56px auto;padding:0 32px}
.lre-in{border-top:2px solid var(--ink);border-bottom:1px solid var(--ink);padding:28px 0 24px;display:grid;grid-template-columns:112px 1fr;gap:28px;align-items:start}
.lre-img{width:112px;height:112px;border-radius:50%;object-fit:cover;object-position:center 22%;display:block}
.lre-k{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--grass);margin-bottom:12px}
.lre-h{font-family:var(--serif);font-size:34px;line-height:1.1;margin:0 0 12px;font-weight:400}
.lre-p{font-family:var(--serif);font-size:18px;line-height:1.55;margin:0 0 16px}
.lre-btn{display:inline-block;font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;background:var(--grass);color:var(--paper)!important;padding:11px 16px;margin:0 14px 8px 0;border-bottom:none!important;text-decoration:none}
.lre-btn2{background:transparent;color:var(--grass)!important;box-shadow:inset 0 0 0 1px var(--grass)}
.lre-tel{font-family:var(--mono);font-size:11px;letter-spacing:.08em;color:inherit;border-bottom:none!important;text-decoration:none}
.lre-c{font-family:var(--mono);font-size:10px;letter-spacing:.06em;line-height:1.7;opacity:.75;margin-top:18px}
.lre-c a{border-bottom:1px solid currentColor;color:inherit;text-decoration:none}
.lre-b{font-size:11px;letter-spacing:.1em}
@media(max-width:640px){.lre{padding:0 20px}.lre-in{grid-template-columns:1fr;gap:16px}.lre-img{width:84px;height:84px}.lre-h{font-size:28px}.lre-p{font-size:17px}}
</style>
'''
ROWS = [(P[k][1], P[k][0].split(" &middot; ")[0], P[k][2] or "Ask the leasing office", f"{D[k][0].replace('Lions Municipal','Lions')}, about {D[k][2]} min") for s in SECTIONS for k in s[2]]
TABLE = ('<style>/*TGI-APT-TABLE*/#sim-table{padding:40px 20px 8px;border-top:1px solid var(--ink,#141414)}#sim-table .t-in{max-width:1040px;margin:0 auto}#sim-table h2{font-family:var(--serif,Georgia,serif);font-size:clamp(22px,3vw,30px);text-align:center;margin:0 0 6px;font-weight:400}#sim-table .t-sub{font-family:var(--mono,monospace);font-size:10px;letter-spacing:.14em;text-transform:uppercase;text-align:center;opacity:.6;margin-bottom:18px}#sim-table .t-wrap{overflow-x:auto}#sim-table table{width:100%;border-collapse:collapse;min-width:560px;font-size:14px}#sim-table th{font-family:var(--mono,monospace);font-size:10px;letter-spacing:.12em;text-transform:uppercase;text-align:left;border-bottom:1px solid var(--ink,#141414);padding:8px 10px}#sim-table td{padding:10px;border-bottom:.5px solid rgba(20,20,20,.18);vertical-align:top}</style>\n'
         '<section id="sim-table">\n  <div class="t-in">\n    <h2>All ten, side by side.</h2>\n    <div class="t-sub">Starting rent from each building&rsquo;s own site &middot; drive times without traffic &middot; checked October 14, 2026</div>\n    <div class="t-wrap">\n      <table>\n        <thead><tr><th>Building</th><th>Area</th><th>Starting rent or special</th><th>Nearest muni</th></tr></thead>\n        <tbody>\n'
         + "\n".join(f"          <tr><td><strong>{a}</strong></td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in ROWS)
         + "\n        </tbody>\n      </table>\n    </div>\n  </div>\n</section>\n")
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>The rooftop pool used to be the amenity that sold an Austin apartment. Now it is the golf simulator. We went through Austin apartment listings and amenity pages and found ten buildings that have one on site, confirmed on each building&rsquo;s own website, from a 30th-floor sports lounge downtown to a clubhouse in Manor.</p>
    <p>They are not all downtown towers. Half of them are garden-style communities in Oak Hill, Steiner Ranch, far South Austin and Manor, and the cheapest buildings start around $1,000 to $1,300 a month. None of them says which simulator it runs, so ask on the tour if you care whether it is a launch monitor you would buy yourself.</p>
    <h2 class="products-hdr btk-story-hdr">What a Sim Room Is Good For</h2>
    <p>A sim in the building will not replace the range, but it is the best place in town to work on wedge distances at 10pm in August, and it turns a rainy Saturday into nine holes at Pebble Beach. For anyone who plays the munis, the thing to check next is the drive: AMLI North Park is about three minutes from Morris Williams, while Steiner Ranch is closer to half an hour from Hancock. And if your building does not have one, <a href="/drops/austin-indoor-golf-simulators">here is every public indoor sim in Austin</a>.</p>
    <p>Rents and specials came from each building&rsquo;s own site on October 14, 2026, and they change weekly. Starting prices are base rent; the total monthly price with fees is higher. Drive times are without traffic.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Buildings</span><span>Ten</span></div>
      <div class="sidebar-detail"><span class="l">Lowest start</span><span>View at Estancia, ~$1,028</span></div>
      <div class="sidebar-detail"><span class="l">Highest start</span><span>415 Colorado, $3,690 1BR</span></div>
      <div class="sidebar-detail"><span class="l">Closest to a muni</span><span>AMLI North Park</span></div>
      <div class="sidebar-detail"><span class="l">Sim + putting green</span><span>AMLI North Park, The Howard</span></div>
      <div class="sidebar-detail"><span class="l">Best view</span><span>415 Colorado</span></div>
      <a href="#sim-table" class="sidebar-cta">See the table &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#AustinApartments</span>
        <span class="hashtag">#GolfSimulator</span>
        <span class="hashtag">#AustinGolf</span>
        <span class="hashtag">#Munis</span>
      </div>
    </div>
  </aside>
</section>
""" + lenny("top")
FAQ = [
 ("Which Austin apartments have a golf simulator?", "As of October 14, 2026: Alexan Waterloo, 415 Colorado, AMLI North Park, Odell, Presidium Tech Ridge, The Shiloh at Oak Hill, Bridge at Steiner Ranch, Park at Estancia, View at Estancia, and The Howard in Manor, each confirmed on the building's own website. Several West Campus student buildings have one too."),
 ("Which Austin apartment with a golf simulator is closest to a public golf course?", "AMLI North Park in Mueller, about 1.7 miles and three minutes from Morris Williams Golf Course. Alexan Waterloo is about five minutes from Hancock."),
 ("How much do Austin apartments with golf simulators cost?", "On October 14, 2026, published starting base rents ran from about $1,028 at View at Estancia and $1,088 at The Howard to $3,690 for a one-bedroom at 415 Colorado. Several buildings were offering two to ten weeks free."),
 ("Do apartment golf simulators cost extra to use?", "None of these buildings lists a fee on its website; most list the simulator as a resident amenity, often bookable. Ask the leasing office how reservations work."),
]
HERO_ALT = "The golf simulator lounge at 415 Colorado in downtown Austin, with a hitting mat and screen beside floor-to-ceiling windows over the skyline"
FRN = json.loads((ROOT / "research/apt-sims/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-APT-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
            f'<div class="product-name">{item}' + (f' &middot; {price}' if price else '') + '</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="{url}" target="_blank" rel="noopener" class="product-link">Visit the building &#8599;</a></div></div>')


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
         "url": URL, "image": og, "datePublished": "2026-10-14", "dateModified": "2026-10-14",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": items},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Field Notes", "item": "https://thegrassyissue.com/#feed"},
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


def swatch(k):
    a, ha, b, hb = PAIRS[k]
    cell = 'flex:1;padding:26px 18px 20px;font-family:var(--mono,monospace);font-size:11px;letter-spacing:.14em;text-transform:uppercase;line-height:1.7'
    return (f'  <div style="display:flex;max-width:620px;margin:6px auto 22px;border:1px solid rgba(20,20,20,.2)">'
            f'<div style="{cell};background:{ha};color:{hb}"><strong>{a}</strong><br>{ha}</div>'
            f'<div style="{cell};background:{hb};color:{ha}"><strong>{b}</strong><br>{hb}</div></div>\n')


def section(sec, n0):
    h2, anchor, ids, kicker = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} picks</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n' +
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def lookbooks():
    figs = "\n".join(f'  <figure><img src="{IMG}/life-{n}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>' for n, alt, cap in LIFE)
    return (f'\n<section class="products" style="margin-top:8px;">\n  <div class="drop-tag grass">{len(LIFE)} photos</div>\n'
            f'  <h2 class="products-hdr" id="lookbooks">From the Lookbooks and In the Wild</h2>\n'
            f'  <p class="cat-kicker"><strong>The pairings on people</strong>Every photo here is the brand&rsquo;s own, from its lookbook, its store or its feed. Royal blue to forest green, in the order above.</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


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
  <a href="/#feed">Field Notes</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Ten buildings, every sim confirmed</span><span class="dot"></span>
    <span>Rents and specials checked October 14, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="{HERO_ALT}" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        o, n = section(s, n); body += o
    body += lenny("bottom") + TABLE
    body += faq_html()
    out = head_top() + head_rest.replace("</head>", GRID_CSS + LRE_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Kalamunda", "Lehi", "Rookline", "LBB", "GolfPass", "Hypebeast", "Old Ghosts", "Instagram", "Shop &#8599;"):
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
