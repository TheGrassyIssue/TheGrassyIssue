#!/usr/bin/env python3
"""build-evening-spots-2.py — Evening Spots Vol. 2: 15 Austin bars for after the round. 10 October 2026.
Lenny: "Let's do another Evening spots round up vol.2" -> "Just focus on the best Austin spots, not tied to a nearby course"
-> "the strongest 5 plus a fresh search for a total of 15" -> "put it all together".
Swaps at build time: The White Horse and Rosie's Wine Bar publish no photos of their rooms on their own sites (a flyer and
logos only), so Posse East and The Long Goodbye took their places.
Lenny then: "swap out Powder room with White Horse". White Horse card: first build used its flyer and a lesson promo;
superseded: Lenny asked for a different image; the site's /grid page has real room photos (stage, dance floor, patio),
now used. Lenny: "remove the Jazz part, jazz is lame. add another cocktail room" -> Elephant Room out, Drink.Well in. Cloned from build-date-night-2.py.
FACTS: research/evening-spots-2 — every bar checked open on October 10, 2026 against its own site (hours as published there),
plus dated 2026 coverage (CultureMap Tastemakers 2026, Austin Chronicle Best of 2026, CBS Austin, The Infatuation, Axios).
PHOTOS: each bar's own website only (frames: research/evening-spots-2/frames.json). Deep Eddy and Elephant Room publish
few, small photos; Hula Hut's are web-size. Hero: The Roosevelt Room's own main-bar photo.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "evening-spots-vol-2-best-austin-bars"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/evening-spots-2"
FRN = json.loads((ROOT / "research/evening-spots-2/frames.json").read_text())
DATE = "2026-10-10"

TITLE = "Evening Spots Vol. 2: 15 of the Best Bars in Austin"
DESC = ("Fifteen Austin bars for the evening after the round: The Roosevelt Room, Midnight Cowboy, Hula Hut, Deep Eddy "
        "Cabaret, Yellow Jacket and more, every one checked open with current hours.")
H1 = "Evening Spots Vol. 2: 15 of the Best Bars in Austin"

P = {
 # Cocktail rooms
 "roosevelt": ("The Roosevelt Room", "W 5th St &middot; Since 2015", "https://www.therooseveltroomatx.com",
   "Austin&rsquo;s most-awarded cocktail bar, in a 1929 building in the Warehouse District. The classics menu runs to 80-plus drinks, organized by era, from the turn of the century and Prohibition through tiki to modern classics. Table service and no dress code. Reservations are strongly recommended. Open daily from 3pm, until 2am Thursday to Saturday."),
 "midnight": ("Midnight Cowboy", "E 6th St &middot; Speakeasy", "https://midnightcowboymodeling.com",
   "Behind an unmarked door on Dirty Sixth, in a building that used to be a brothel posing as a massage parlor. Ring the buzzer. Inside it is small, dark and quiet, with a tarot-themed menu that got it nominated for CultureMap&rsquo;s 2026 Bar of the Year. Book on OpenTable, parties of eight or fewer. Closed Mondays."),
 "peche": ("P&eacute;ch&eacute;", "W 4th St &middot; Since about 2009", "https://www.pecheaustin.com",
   "Billed as Austin&rsquo;s first absinthe bar, with pre-Prohibition cocktails and a French bistro kitchen behind them. Order a Sazerac or let the bartenders walk you through the absinthe; they like the questions. Happy hour runs all night on Sunday and Monday."),
 "lamezca": ("La Mezca", "Mueller &middot; Opened 2025", "https://www.lamezcaatx.com",
   "A small mezcal bar from Reyna and Maritza Vazquez, the sisters behind Veracruz All Natural, next door to their Mueller restaurant. It pours only artisanal and ancestral mezcal from family producers, with no orange slices and no salt. The Austin Chronicle named it Best Bar for Mezcal Nerds in 2026. Vinyl DJs on Friday and Saturday, open until 2am."),
 # Patios and backyards
 "drinkwell": ("Drink.Well", "North Loop &middot; Since 2012", "https://www.drinkwellaustin.com",
   "A small neighborhood cocktail bar and kitchen on East 53rd Street, and one of the most awarded in town since it opened in 2012. It was a CultureMap Bar of the Year nominee in 2025. The menu turns with the seasons, and the bartenders will make you any classic. Martini Monday, the Tuesday Night Agave Social and happy hour until 5:30pm. Closed Sundays."),
 "yellowjacket": ("Yellow Jacket Social Club", "E 5th St &middot; Patio", "https://yellowjacketsocialclub.com",
   "The East Side patio, under a canopy of trees, with a full kitchen that runs until 2am. Cocktails, draft beer, Frito pie and sandwiches, and a different cheap special every night of the week. Open every day, 11am to 2am."),
 "bonis": ("Boni&rsquo;s Bar Next Door", "S 1st St &middot; New in 2026", "https://www.bonisbar.com",
   "The newest bar here, opened in March by the couple behind Lenoir, in a 1934 bungalow next door to the restaurant. Spanish-leaning cocktails ($12&ndash;$15, start with the gin tonic), Spanish wines from $10 and tapas like stewed pork meatballs. It&rsquo;s named for a great-grandfather who ran rum during Prohibition. Closed Tuesdays."),
 "longgoodbye": ("The Long Goodbye", "Manor Rd &middot; Patio and yard", "https://www.thelonggoodbyeatx.com",
   "An indoor cocktail lounge with covered patios and an outdoor yard on Manor Road. Tuesday is $10 martini night, Wednesday is half-off wine, and Palm Pizza slices are on Monday and Tuesday. Walk-in only. Open until midnight Wednesday to Saturday."),
 "cmw": ("Central Machine Works", "E Cesar Chavez &middot; Beer hall", "https://www.cmwbrewery.com",
   "A brewery and beer hall in a 1940s machine shop, with an 18,000-pound vintage lathe behind the bar and a big beer garden out back. The American Lager took bronze at the 2026 Texas Craft Brewers Cup. There&rsquo;s a full bar, frozen drinks, free shows and trivia on Tuesdays. Closed Mondays."),
 "hulahut": ("Hula Hut", "Lake Austin &middot; Since 1993", "https://www.hulahut.com",
   "A patio built right out over Lake Austin, with bamboo, shade and thousands of colored lights, and a Tex-Mex menu with a Hawaiian twist. You can arrive by boat. It&rsquo;s the sunset pick on this list, so order a rita and stay until the lights come on. No reservations."),
 # Dives and honky-tonks
 "deepeddy": ("Deep Eddy Cabaret", "Lake Austin Blvd &middot; Since 1951", "https://deepeddycabaret.com",
   "Austin&rsquo;s classic dive, opened in 1951 and named for a swimming hole on the river behind it. There&rsquo;s no kitchen: beer, liquor, wine, snacks, pool and a jukebox, and Lone Star by the mug. Open every day, noon to 2am."),
 "posse": ("Posse East", "Hyde Park &middot; Since 1971", "https://www.posseeast.com",
   "Fifty-five years on Duval Street, at the edge of Hyde Park and walking distance from the stadium. A big patio, cheap happy hour, a third-pound cheeseburger and a crowd that has been coming since the 1970s. The bar is open until midnight Monday to Saturday."),
 "meaneyed": ("The Mean Eyed Cat", "W 5th St &middot; Since 2004", "https://themeaneyedcat.com",
   "A Johnny Cash shrine in an old chainsaw repair shop, with a wood patio under a live oak that is more than 300 years old. Order the Mean Marg (tequila with habanero, serrano and jalape&ntilde;o). Happy hour on weekdays, 4 to 8pm. Open daily, 11am to 2am."),
 "whitehorse": ("The White Horse", "E 6th St &middot; Since 2011", "https://www.thewhitehorseaustin.com",
   "The best honky-tonk in East Austin, by its own count and plenty of others&rsquo;. Live country bands every night, two-step lessons Thursday to Sunday at 7pm (donation-based, so go), and the Bomb Tacos truck parked outside until 1:30am. Willie Nelson has been known to drop in. No reservations, cover after 7:30pm. Open daily, 3pm to 2am."),
 "deadrabbit": ("The Dead Rabbit", "E 6th St &middot; Since 2024", "https://www.thedeadrabbittx.com",
   "The Austin outpost of the New York Irish pub that was named World&rsquo;s Best Bar in 2016. It opened on Sixth Street on July 4, 2024. It&rsquo;s a proper pub with Guinness, the house Irish coffee, live music and a Sunday roast, and it&rsquo;s always packed. Book on Resy, but there&rsquo;s always room for walk-ins."),
}

SECTIONS = [
    ("Cocktail Rooms", "cocktail-rooms", ["roosevelt", "midnight", "drinkwell", "peche", "lamezca"],
     "<strong>Five rooms &middot; Downtown, East and North Loop</strong>For when you clean up after the round. Austin&rsquo;s most-awarded cocktail bar, a speakeasy behind a buzzer, a North Loop neighborhood favorite, an absinthe bar and a mezcal room."),
    ("Patios and Backyards", "patios", ["yellowjacket", "bonis", "longgoodbye", "cmw", "hulahut"],
     "<strong>Five patios &middot; All over town</strong>For a warm night when nobody wants to be indoors: a tree-covered East Side patio, a new Spanish backyard bar, martini night on Manor Road, a beer garden behind an old machine shop and a deck over Lake Austin."),
    ("Dives and Honky-Tonks", "dives", ["deepeddy", "posse", "meaneyed", "whitehorse", "deadrabbit"],
     "<strong>Five institutions &middot; Since 1951</strong>For when you&rsquo;re still in your golf shoes. Three dives with a combined 152 years, the best honky-tonk in East Austin and the busiest Irish pub in town."),
]
N = 15
GRID_CSS = ('<style>/*TGI-EVENING2-GRID*/'
            '.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}'
            '.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}'
            '@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}'
            '@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Vol. 1 was five easy spots for the hour after the round. This one is bigger: fifteen of the best bars in Austin, for every kind of evening. Sometimes you want a quiet room with a perfect drink, sometimes a patio until midnight, and sometimes a dive where nobody minds the golf shoes.</p>
    <p>The list is split three ways. The cocktail rooms are for the nights you dress up, the patios are for warm evenings, and the dives and the honky-tonk are Austin institutions. One of them, Boni&rsquo;s, only opened this year. Every bar was checked against its own site on October 10, 2026, and the hours in each card are theirs.</p>
    <h2 class="products-hdr btk-story-hdr">Start Here</h2>
    <p>If you only go to one, make it The Roosevelt Room on a weeknight. Grab a seat at the bar, pick a drink from the decade of your choice, and come back on a Thursday. For a sunset, it&rsquo;s Hula Hut. For a cheap night, it&rsquo;s a mug of Lone Star at Deep Eddy.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Spots</span><span>15</span></div>
      <div class="sidebar-detail"><span class="l">Start with</span><span>The Roosevelt Room</span></div>
      <div class="sidebar-detail"><span class="l">Sunset</span><span>Hula Hut</span></div>
      <div class="sidebar-detail"><span class="l">Newest</span><span>Boni&rsquo;s Bar Next Door</span></div>
      <div class="sidebar-detail"><span class="l">Oldest</span><span>Deep Eddy Cabaret, 1951</span></div>
      <div class="sidebar-detail"><span class="l">Verified</span><span>October 10, 2026</span></div>
      <div class="sidebar-detail"><span class="l">Vol. 1</span><span><a href="/drops/5-post-round-evening-spots-in-austin" style="border-bottom:1px solid currentColor;">5 Post-Round Evening Spots</a></span></div>
      <a href="#cocktail-rooms" class="sidebar-cta">See the bars &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#AustinBars</span>
        <span class="hashtag">#NineteenthHole</span>
        <span class="hashtag">#AustinNights</span>
        <span class="hashtag">#TheGrassyIssue</span>
      </div>
    </div>
  </aside>
</section>
"""

FAQ = [
    ("What are the best bars in Austin?",
     "This guide has 15. Cocktail rooms: The Roosevelt Room, Midnight Cowboy, Drink.Well, Péché and La Mezca. Patios: Yellow Jacket Social Club, Boni's Bar Next Door, The Long Goodbye, Central Machine Works and Hula Hut. Dives and honky-tonks: Deep Eddy Cabaret, Posse East, The Mean Eyed Cat, The White Horse and The Dead Rabbit."),
    ("What is the best cocktail bar in Austin?",
     "The Roosevelt Room in the Warehouse District calls itself Austin's most-awarded cocktail bar, with 80-plus classic cocktails organized by era. Midnight Cowboy, behind a buzzer on East Sixth, is the speakeasy alternative, and Drink.Well is the neighborhood pick in North Loop."),
    ("Where can you watch the sunset with a drink in Austin?",
     "Hula Hut's patio sits right over Lake Austin on Lake Austin Boulevard. Deep Eddy Cabaret, a few minutes away, is the cheaper dive option."),
    ("What are the best patio bars in Austin?",
     "Yellow Jacket Social Club's tree-covered patio on East 5th, The Long Goodbye's covered patios and yard on Manor Road, Central Machine Works' beer garden on East Cesar Chavez, Boni's backyard on South 1st and Hula Hut on Lake Austin."),
    ("Which Austin bars are open until 2am?",
     "Of the bars in this guide, Yellow Jacket Social Club, Deep Eddy Cabaret, The Mean Eyed Cat, The White Horse, The Dead Rabbit (most nights) and La Mezca (Friday and Saturday) stay open until 2am, as does The Roosevelt Room Thursday to Saturday."),
]


def card(k, idx):
    name, hood, url, copy = P[k]
    fr = FRN[k]
    label = H.unescape(name).replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)}, Austin bar &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>'
                   for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>'
                   for j in range(len(fr)))
    return (f'<div class="product-card" id="{k}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{hood}</div>'
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
            items.append({"@type": "ListItem", "position": pos, "url": P[h][2], "name": H.unescape(P[h][0])})
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
            {"@type": "ListItem", "position": 3, "name": "Evening Spots Vol. 2", "item": URL}]},
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
  Evening Spots Vol. 2</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>The Roosevelt Room, Midnight Cowboy, Hula Hut, Deep Eddy and more</span><span class="dot"></span>
    <span>15 bars &middot; Austin, TX &middot; verified October 10, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="The main bar at The Roosevelt Room in downtown Austin, lit up in the evening" fetchpriority="high" /></div></div>
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
    for leak in ("Manors Revisited", "Nicklaus", "Enron", "Fish Shop", "Michelin"):
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
