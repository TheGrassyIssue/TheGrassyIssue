#!/usr/bin/env python3
"""build-date-night-2.py — Date Night Vol. 2: 15 Austin restaurants for reconnecting.
8 October 2026. Lenny: "Let's work on Date night Vol. 2, great Austin restaurants for reconnecting. Make sure The
Fish Shop is on the list." From date-night-2-options.html he swapped #10 (Kappo Kappo) for Sway Thai, then picked
"My 15 (Recommended)". Images: "make sure we're leading with images of the restaurants or food and also including a
pic of the space itself."

FACTS: research/date-night-2 (each restaurant checked open on 8 Oct 2026 against its own site plus 2026 coverage;
the 2026 Michelin Guide Texas was released 8 Oct 2026: Fabrik gained a star, Barley Swine kept its star). Earlier
Michelin labels are stated with their year. Roya: alcohol service unconfirmed, so drinks are not mentioned.
PHOTOS: each restaurant's own website, framed 1000x1250 (research/date-night-2/frames.json). Sway's site photos
are web-size (800-1200px); a press-kit request is out. Roya's site has a single photo. Hero: Fish Shop's own photo.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "date-night-vol-2-austin-restaurants-for-reconnecting"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/date-night-2"
FRN = json.loads((ROOT / "research/date-night-2/frames.json").read_text())
DATE = "2026-10-08"

TITLE = "Date Night Vol. 2: 15 Austin Restaurants for Reconnecting"
DESC = ("Fifteen Austin restaurants for a night where you actually talk: Fish Shop, Jeffrey's, Lenoir, Barley "
        "Swine, Sway and more, from tasting menus to a velvet-chair lounge.")
H1 = "Date Night Vol. 2: 15 Austin Restaurants for Reconnecting"

# key -> (name, hood, price, url, copy)
P = {
 # The Splurge
 "barley": ("Barley Swine", "Burnet Rd", "$$$$", "https://www.barleyswine.com",
   "Bryce Gilmore&rsquo;s tasting menu is the longest dinner here, and that&rsquo;s the point. The room feels like a warm lodge, the courses run for hours, and the staff are good enough that GM Stefan Davis won Michelin&rsquo;s 2026 service award the same day the restaurant kept its star. The menu is $125. Book on Tock. It&rsquo;s open Thursday to Sunday."),
 "jeffreys": ("Jeffrey&rsquo;s", "Clarksville", "$$$$", "https://jeffreysofaustin.com",
   "Red leather booths, dark green walls and a martini cart that comes to the table. Jeffrey&rsquo;s has been the Clarksville anniversary room for decades, and Michelin listed it in 2025. Start with the truffled deviled eggs and finish with the chocolate souffl&eacute;. The dining room is open nightly from 4:30."),
 "luties": ("Lutie&rsquo;s", "Commodore Perry Estate", "$$$$", "https://auberge.com/commodore-perry/dine/",
   "Lutie&rsquo;s fills a green-and-gold garden room on the Commodore Perry Estate, looking out over formal gardens and old oaks. It&rsquo;s inside a hotel, and it doesn&rsquo;t feel like one. Order the estate garden bread with cultured butter and anything off the coal fire. Dinner nightly from 5."),
 "fabrik": ("Fabrik", "Tarrytown", "$$$", "https://www.fabrikatx.com",
   "Chef Je Wallerstein&rsquo;s plant-based tasting menu won Fabrik a Michelin star this week. The room in Tarrytown is small and quiet, and the bread course alone is a reason to book. It serves five or eight courses by reservation, and only on Monday, Tuesday, Thursday and Friday."),
 "comedor": ("Comedor", "Downtown", "$$$$", "https://comedortx.com",
   "Tom Kundig designed the room: booths under sculptural lights, and garage doors that open onto the patio. Chef Philip Speer&rsquo;s bone marrow tacos are the order, and the mezcal &ldquo;bone luge&rdquo; that follows is the part you&rsquo;ll both remember. Michelin listed it in 2025."),
 # The Sweet Spot
 "fish": ("Fish Shop", "East 6th", "$$$", "https://www.fishshopatx.com",
   "Chef Justin Huffman, who ran the kitchen at Justine&rsquo;s, and his wife Nicole Rossi opened this upstairs seafood room in July 2025. It has leather banquettes, warm wood and a counter made for two, and Texas Monthly ranked it No. 4 among the best new restaurants in Texas this year. Order the crudo, the Dungeness crab roll and a martini. It gets loud at weekend peaks, so book a weeknight or an early table."),
 "lenoir": ("Lenoir", "Bouldin Creek", "$$$", "https://www.lenoirrestaurant.com",
   "Lenoir is a small bungalow on South 1st with an oak-shaded wine garden behind it, strung with lights. Go for the five-course chef&rsquo;s choice and stay in the garden for one more glass. The menu turns with the seasons. Michelin listed it in 2025. Closed Tuesdays."),
 "roya": ("Roya", "Shoal Creek Blvd", "$$$", "https://www.royaaustin.com",
   "Roya, the newest room here, serves Persian food in a warren of small, deep-blue dining rooms with flattering light. Texas Monthly called it Austin&rsquo;s best new date-night spot. Let the staff choose for the table with the sofreh service, make sure the tahdig comes, and end with Persian tea. There&rsquo;s free parking."),
 "sway": ("Sway", "West Lake Hills", "$$$", "https://swaythai.com",
   "Modern Thai built for sharing and lingering: warm lighting, a string-lit garden and an enclosed rooftop bar that looks back over the city. Bon App&eacute;tit once named it one of the 50 best new restaurants in America. Order the som tam and the crispy chicken skins, then take the last drink upstairs. Walk-ins are welcome; OpenTable for reservations."),
 "emmer": ("Emmer &amp; Rye", "Rainey St", "$$$", "https://emmerandrye.com",
   "Emmer &amp; Rye is the calm room on Rainey Street. It mills heirloom grain in house for its pasta and sends small plates out in waves, so dinner sets its own slow pace. Michelin gave it a Bib Gourmand and a Green Star in 2025. Book on OpenTable."),
 "fonda": ("Fonda San Miguel", "Allandale", "$$$", "https://www.fondasanmiguel.com",
   "An art-filled hacienda that has been serving interior Mexican food since 1975, with a skylit atrium that feels a long way from North Loop. Order the chile relleno or the mole enchiladas, and come early for happy hour in the atrium, Monday to Thursday from 4:30."),
 # The Easy Yes
 "intero": ("Intero", "E Cesar Chavez", "$$&ndash;$$$", "https://www.interorestaurant.com",
   "Intero is a small, warm Italian room with a patio and its own chocolate counter. The pasta is made in house and the menu changes often, so ask what&rsquo;s new, and save room for the chocolate truffles. Closed Mondays."),
 "daidue": ("Dai Due", "Manor Rd", "$$$", "https://www.daidue.com",
   "A rustic dining room behind a butcher counter, cooking only what Central Texas grows and hunts, wild game included. Share the cold meat board, then the smoked pork chop. Michelin gave it a Bib Gourmand and a Green Star in 2025. Dinner Tuesday to Sunday, on Resy."),
 "suerte": ("Suerte", "East 6th", "$$$", "https://www.suerteatx.com",
   "Chef Fermín Núñez won the James Beard award for Best Chef: Texas in 2024, and his masa is the reason. The suadero tacos and the tuna tiradito are the orders. The bar gets buzzy later, so book an early table if the point is conversation. Michelin listed it in 2025."),
 "honeymoon": ("Honey Moon Spirit Lounge", "North University", "$$", "https://honeymoonspiritlounge.com",
   "Honey Moon turned an old house on 34th Street into a lounge with velvet chairs, vintage chandeliers and wallpaper. It&rsquo;s the most affordable romance in the guide. Order the koji-aged steak frites and a second round. Closed Mondays."),
}

SECTIONS = [
    ("The Splurge", "the-splurge", ["barley", "jeffreys", "luties", "fabrik", "comedor"],
     "<strong>Five rooms &middot; $$$ to $$$$</strong>For an anniversary, or for a night that needs to say something. Two Michelin stars, a garden room on a historic estate, a martini cart and a mezcal bone luge. Book these the day you decide, not the day of."),
    ("The Sweet Spot", "the-sweet-spot", ["fish", "lenoir", "roya", "sway", "emmer", "fonda"],
     "<strong>Six rooms &middot; $$$</strong>These are special without the ceremony: a seafood counter for two, a wine garden under the oaks, deep-blue Persian dining rooms, a rooftop over the skyline, a calm room on Rainey and a hacienda that has been doing this since 1975."),
    ("The Easy Yes", "the-easy-yes", ["intero", "daidue", "suerte", "honeymoon"],
     "<strong>Four rooms &middot; $$ to $$$</strong>For a Tuesday, when the point is the two of you and not the bill. Handmade pasta, a butcher counter, masa and a velvet lounge on 34th Street."),
]

N = 15
GRID_CSS = ('<style>/*TGI-DATENIGHT2-GRID*/'
            # every tier three wide, last row centred (Lenny: "the easy yes section should be three wide not four")
            '.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}'
            '.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}'
            '@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}'
            '@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Vol. 1 was about the peace treaty after a 36-hole weekend. This one is for the ordinary weeks, when work and the kids and the tee sheet have quietly taken over and you realize you haven&rsquo;t had a real conversation in a while. The fix isn&rsquo;t a grand gesture. It&rsquo;s a table where you can hear each other.</p>
    <p>Every room here had to pass one test: can two people talk? That means warm light, a noise level you don&rsquo;t have to shout over, and a reason to stay for one more glass: a wine garden, a rooftop, a martini cart, a velvet chair. Some are big nights and some are a Tuesday, and none of them repeat Vol. 1.</p>
    <h2 class="products-hdr btk-story-hdr">Start Here</h2>
    <p>If you book one, make it Fish Shop on a weeknight. Grab the counter, order the crudo and a martini, and let the evening go long. Everything here was open on October 8, 2026, the day the new Michelin Guide Texas came out, and the two stars on this list are current.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Spots</span><span>15</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$$ &ndash; $$$$</span></div>
      <div class="sidebar-detail"><span class="l">Start with</span><span>Fish Shop, East 6th</span></div>
      <div class="sidebar-detail"><span class="l">Michelin stars</span><span>Barley Swine, Fabrik</span></div>
      <div class="sidebar-detail"><span class="l">Verified</span><span>October 8, 2026</span></div>
      <div class="sidebar-detail"><span class="l">Vol. 1</span><span><a href="/drops/date-night-after-36" style="border-bottom:1px solid currentColor;">Date Night After 36</a></span></div>
      <a href="#the-splurge" class="sidebar-cta">See the rooms &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#DateNight</span>
        <span class="hashtag">#AustinEats</span>
        <span class="hashtag">#AustinRestaurants</span>
        <span class="hashtag">#TheGrassyIssue</span>
      </div>
    </div>
  </aside>
</section>
"""

FAQ = [
    ("What are the best Austin restaurants for a date night?",
     "This guide has 15, none repeated from our first date-night list. For a big night: Barley Swine, Jeffrey's, Lutie's, Fabrik and Comedor. Special without ceremony: Fish Shop, Lenoir, Roya, Sway, Emmer & Rye and Fonda San Miguel. Easy weeknights: Intero, Dai Due, Suerte and Honey Moon Spirit Lounge."),
    ("Where is Fish Shop in Austin?",
     "Upstairs at 1401 E. 6th St. in East Austin. Chef Justin Huffman and Nicole Rossi opened it in July 2025, and it takes reservations on OpenTable. It is open for lunch and dinner on weekdays and from 4pm on weekends, with $2 oysters at weekday happy hour."),
    ("Which Austin restaurants have a Michelin star in 2026?",
     "Of the restaurants in this guide, Barley Swine kept its star and Fabrik earned its first in the Michelin Guide Texas released on October 8, 2026."),
    ("What is a romantic Austin restaurant with outdoor seating?",
     "Lenoir's oak-shaded wine garden on South 1st, Lutie's garden room and patio at the Commodore Perry Estate, Sway's string-lit garden and rooftop in West Lake Hills, and Intero's patio on East Cesar Chavez."),
    ("What is an affordable date night spot in Austin?",
     "Honey Moon Spirit Lounge on 34th Street is the most affordable room in this guide, and Intero's pasta and Suerte's tacos keep a weeknight dinner reasonable."),
]


def card(k, idx):
    name, hood, price, url, copy = P[k]
    fr = FRN[k]
    label = H.unescape(name).replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)}, Austin date-night restaurant &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>'
                   for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>'
                   for j in range(len(fr)))
    return (f'<div class="product-card" id="{k}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{hood} &middot; {price}</div>'
            f'<div class="product-name">{name}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="{url}" target="_blank" rel="noopener" class="product-link">View &#8599;</a></div></div>')


def section(sec, n0):
    h2, anchor, ids, kicker = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} spots</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


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
            items.append({"@type": "ListItem", "position": pos, "url": P[h][3], "name": H.unescape(P[h][0])})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": DATE, "dateModified": DATE,
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
            {"@type": "ListItem", "position": 3, "name": "Date Night Vol. 2", "item": URL}]},
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
        assert len(FRN.get(k, [])) >= 1, k
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Field Notes</a><span>/</span>
  Date Night Vol. 2</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Fish Shop, Jeffrey&rsquo;s, Lenoir, Barley Swine, Sway and more</span><span class="dot"></span>
    <span>15 spots &middot; Austin, TX &middot; verified October 8, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Fish Shop&rsquo;s dining room in East Austin, with leather banquettes and framed art in warm evening light" fetchpriority="high" /></div></div>
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
    for leak in ("Manors Revisited", "Nicklaus", "Enron"):
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
