#!/usr/bin/env python3
"""build-chicken-sandwiches.py — The Best Chicken Sandwiches in Austin: 15 to Know.
30 September 2026. A Field Note.

Lenny: "Let's do a field note about the best chicken sandwiches in the city", then
"Let's aim for 12 options- okay to repeat if location is in a different field guide.
Let's finish up this post".

PICKS: 12 from (plus Ben & Lynn's, added at Lenny's request 30 Sep: own menu page, $11.95; hours from Lenny's screenshot of the B&L site). Hattie B's and June's added 30 Sep at Lenny's request; June's is his pick. Hattie B's price/hours from its own ordering site; June's from its own menu PDF (8.31.26); June's sandwich photo is from its own Instagram, post C_gMNWZvPqZ, 4 Sep 2024; second frame is the cafe from its site) research/chicken-sandwich/options.json (30 candidates, each checked
on the spot's own site or Toast/Square page). Repeats: Bird Bird Biscuit (sandwiches
guide) and Spicy Boys (wings guide). Flyrite left out: its sandwich description is only
in third-party coverage. Pebble Onebird left out: opened 20 Sep, no track record yet.

FACTS: sandwich names, components, prices and hours from each spot's own site or
ordering page. Where a spot lists no price online, none is given. Where hours are
not published or conflict, the card says "check before you go".

PHOTOS: each spot's own photography, in images/chicken-sandwiches-2026/.
No quotes. Normal house template. Dry run by default.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "best-chicken-sandwiches-in-austin"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/chicken-sandwiches-2026"
FR = {
 "tumble": ["tumble-22-1"], "galaxy": ["galaxy-cafe-1"], "better": ["better-half-1"], "hattie": ["hattie-bs-1"], "loro": ["loro-1"], "junes": ["junes-all-day-sandwich-1", "junes-all-day-1"],
 "lucys": ["lucys-fried-chicken-1"], "birdbird": ["bird-bird-biscuit-1"], "spicy": ["spicy-boys-fried-chicken-1"],
 "benlynn": ["ben-and-lynns-1", "ben-and-lynns-2"],
 "cockti": ["cockti-juicy-fried-chicken-1", "cockti-juicy-fried-chicken-3"], "diablo": ["diablo-hot-chicken-1"],
 "tiger": ["golden-tiger-2", "golden-tiger-1", "golden-tiger-3"], "jewboy": ["jewboy-burgers-1"],
 "dang": ["dang-hot-89-1", "dang-hot-89-2"],
}
FR = {k: [{"local": f"{IMG}/{f}.jpg"} for f in v] for k, v in FR.items()}

TITLE = "The Best Chicken Sandwiches in Austin: 15 to Know"
DESC = ("Fifteen Austin chicken sandwiches, led by our pick at June's All Day, plus Nashville hot at "
        "Tumble 22 and Hattie B's. Prices and hours checked 30 Sep 2026.")
H1 = "The Best Chicken Sandwiches in Austin &mdash; 15 to Know"
CHECK = "Check before you go"

T = {
 # ---- West, Central & South
 "tumble": ("Tumble 22", "Tarrytown &middot; 2304 Lake Austin Blvd", "The O.G. &middot; $12.49",
   "The O.G. is Nashville hot on an all-natural breast, crispy or grilled, with coleslaw, bread-and-butter pickles and Duke&rsquo;s mayo. There are six heat levels, from Painless to Stupid Hot. It is three minutes from Lions, and there are more Tumble 22s on Burnet, South Lamar and Great Hills.",
   "Hours vary by location; check before you go", "https://tumble22.com/"),
 "galaxy": ("Galaxy Cafe", "Clarksville &middot; 1000 W Lynn St", "Spicy Fried Chicken Sandwich",
   "Galaxy puts a fried breast on ciabatta with cabbage slaw, fresh jalape&ntilde;os, house pickles and chipotle mayo. It is five minutes from both Lions and Butler, so it is the easy lunch after a morning nine.",
   CHECK, "https://www.galaxycafeaustin.com"),
 "better": ("Better Half", "Old West Austin &middot; 406 Walsh St", "Taiwanese Spicy Chicken Sandwich &middot; $16",
   "This is the most unusual sandwich here: a mala-spiced crispy breast with Szechuan and Japanese peppercorn, zucchini-noodle slaw, Thai basil green curry mayo, mint and crispy garlic. It is on the evening menu, so plan it for after the round.",
   "Mon 8am&ndash;3pm &middot; Tue&ndash;Thu 8am&ndash;10pm &middot; Fri&ndash;Sat 8am&ndash;11pm &middot; Sun 8am&ndash;10pm", "https://www.betterhalfbar.com"),
 "hattie": ("Hattie B&rsquo;s Hot Chicken", "South Lamar &middot; 2529 S Lamar Blvd", "Fried Sandwich &middot; $11.50",
   "The Nashville hot chicken institution has two Austin locations, here and at Domain Northside. A boneless breast is fried and spiced your way, from Southern with no heat up to Shut the Cluck Up, then goes on a toasted bun with creamy slaw, Nashville Comeback Sauce and pickles, with a side. The grilled version is the same price.",
   "Sun&ndash;Thu 10:45am&ndash;10pm &middot; Fri&ndash;Sat 10:45am&ndash;11pm", "https://hattieb.com/locations"),
 "junes": ("June&rsquo;s All Day", "&#9733; Our pick &middot; South Congress &middot; 1722 S Congress Ave", "Fried Chicken Sandwich &middot; $23",
   "This is the best chicken sandwich in the city. June&rsquo;s is the all-day caf&eacute; on South Congress, and its fried chicken sandwich comes with kohlrabi ranch slaw, hot sauce and jalape&ntilde;os. It is the most expensive one here and it earns the price. Butler is five minutes away.",
   "Lunch Mon&ndash;Fri 11am&ndash;4pm &middot; brunch Sat&ndash;Sun 9am&ndash;3pm &middot; dinner daily 4&ndash;10pm", "https://junesallday.com/"),
 "loro": ("Loro", "South Lamar &middot; 2115 S Lamar Blvd", "Crispy Chicken Sandwich &middot; $13.50",
   "Loro smokes the chicken, batters and fries it, then adds citrus-cabbage slaw, pickles, honey and smoked hot sauce. It is part of the $15 Lunch Two Step from 11 to 2, five minutes from Butler.",
   "Sun&ndash;Thu 11am&ndash;10pm &middot; Fri&ndash;Sat 11am&ndash;11pm", "https://www.loroeats.com/locations/austin/south-lamar/"),
 "lucys": ("Lucy&rsquo;s Fried Chicken", "South Congress &middot; 2218 College Ave", "The Revival &middot; $15.50",
   "The Revival stacks fried chicken with honey mustard slaw, pickles, mayo and American cheese, and comes with kettle chips. College Avenue is the last Lucy&rsquo;s still open, and this is the classic Southern version of the sandwich.",
   "Sun&ndash;Thu 11am&ndash;9pm &middot; Fri&ndash;Sat 11am&ndash;10pm", "https://www.lucysfriedchicken.com"),
 # ---- East
 "birdbird": ("Bird Bird Biscuit", "Manor Road &middot; 2701 Manor Rd", "Queen Beak &middot; $11.50",
   "The Queen Beak puts a fried chicken breast with black pepper honey and bacon-infused chipotle mayo on a handmade buttermilk biscuit. It opens at 7:30, five minutes from Morris Williams, so it is the one to eat before the round. It is in our <a href=\"/drops/sandwiches-before-the-round\">sandwiches guide</a> too.",
   "Mon&ndash;Wed 7:30am&ndash;2pm &middot; Thu&ndash;Sat 7:30am&ndash;9pm &middot; Sun 7:30am&ndash;3pm", "https://www.birdbirdbiscuit.com/"),
 "spicy": ("Spicy Boys Fried Chicken", "East 6th &middot; 1701 E 6th St", "The OG &middot; $9.49",
   "The OG is a crispy thigh on a Martin&rsquo;s potato roll with sweet chili honey, pickled papaya, herbs and Thai basil ranch, and at $9.49 it is the cheapest sandwich here. The Hot Gai in the photo swaps in white American and massaman mayo. There are also St. Elmo and Pflugerville locations.",
   CHECK, "https://www.spicyboyschicken.com/"),
 "benlynn": ("Ben &amp; Lynn&rsquo;s", "East Cesar Chavez &middot; 2600 E Cesar Chavez St", "B&amp;L Classic &middot; $11.95",
   "Joshua Weissman named his first restaurant after his parents and put it in a restored 1920s bungalow. The B&amp;L Classic is Texas fried chicken with house-made dill pickles and B&amp;L sauce on a butter-toasted bun. Pay $1.95 more and it gets dunked in YamYum, sweet and lightly spicy, which is the second photo. The homepage just says &ldquo;Open Sundays ;)&rdquo;, and yes, that one is aimed at Chick-fil-A.",
   "Mon&ndash;Thu 11:30am&ndash;midnight &middot; Fri&ndash;Sat 11:30am&ndash;2am &middot; Sun 11:30am&ndash;midnight", "https://www.benandlynns.com/menu"),
 "cockti": ("Cockti Juicy Fried Chicken", "Rosewood &middot; 1309 Rosewood Ave", "Chipotle Cinnamon Chicken Sandwich",
   "Cockti rubs a fried jumbo tender or thigh in chipotle and cinnamon and adds green onion, cilantro, lime, agave, spicy pickles and chipotle ranch. A gluten-free masa bun is available, and the second photo is the Spicy version. The trailer moved here from East MLK.",
   CHECK, "https://cockti-fried-chicken.square.site/"),
 "diablo": ("Diablo Hot Chicken", "Govalle &middot; 2505 Webberville Rd", "El Chingon",
   "The Vazquez sisters of Veracruz All Natural opened this in March, in the same trailer park as their original bus. El Chingon is the thigh and El Favorito the breast, both with coleslaw, dill pickles and ranch. Ask for it wet and it gets a citrus glaze. Heat runs from heatless to diablo.",
   CHECK, "https://www.diablohotchicken.com"),
 "tiger": ("Golden Tiger", "East 6th &middot; 1816 E 6th St", "Thai Chicken Sandwich",
   "Golden Tiger glazes a fried thigh in sweet chili and adds lettuce, Thai basil, pickled serranos and onion, from a truck on Whisler&rsquo;s patio. The photos also show the Original and the Buffalo, which comes with blue cheese.",
   "Evenings and late night; check before you go", "https://goldentigerforever.square.site/"),
 # ---- North
 "jewboy": ("JewBoy Burgers", "North Loop &middot; 5111 Airport Blvd", "Can You Grill It? &middot; $11",
   "This is the one grilled sandwich here. JewBoy marinates a boneless thigh and serves it with melted Swiss, bacon, Schmutz sauce and lettuce on a potato bun. It is about seven minutes from Hancock.",
   "Tue&ndash;Thu 11am&ndash;9pm &middot; Fri&ndash;Sat 11am&ndash;10pm &middot; Sun 11am&ndash;9pm &middot; closed Mon", "https://jewboyburgers.com"),
 "dang": ("Dang Hot 89", "At Celis Brewery &middot; 10001 Metric Blvd", "Boneless Chicken Sandwich",
   "Dang Hot 89 puts fried boneless thighs on a Texas bun with slaw, Dang Sauce and pickles, and serves it with fries. It is the far-north Nashville hot option, parked behind a brewery.",
   CHECK, "https://howdy-89-llc.square.site"),
}

SECTIONS = [
    ("west", "West, Central &amp; South", "west-central-south", ["junes", "tumble", "galaxy", "better", "hattie", "loro", "lucys"],
     "<strong>Seven stops &middot; closest to Lions and Butler</strong>June&rsquo;s makes our favourite on South Congress, Tumble 22 is three minutes from Muny, Better Half serves Taiwanese mala on West 5th, and Loro smokes its chicken before frying it."),
    ("east", "East Austin", "east-austin", ["birdbird", "benlynn", "spicy", "cockti", "diablo", "tiger"],
     "<strong>Six stops &middot; breakfast to late night</strong>Bird Bird opens at 7:30am on Manor Road, Ben &amp; Lynn&rsquo;s fries in a bungalow on Cesar Chavez, and the trailers on East 6th, Rosewood and Webberville run into the night. Morris Williams is the nearest muni."),
    ("north", "North Austin", "north-austin", ["jewboy", "dang"],
     "<strong>Two stops &middot; up Airport and Metric</strong>JewBoy grills its chicken near Hancock, and Dang Hot 89 serves Nashville hot behind a brewery in the far north."),
]

BANDS = {}

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>The chicken sandwich is the best thing to eat after a round in Austin. It is cheap, it travels, and the city has every version of it: Nashville hot, Thai, Taiwanese, a chipotle-cinnamon rub, one on a biscuit and one off the grill. This is our field note, fifteen of them in three parts of town.</p>
    <p>If you only try one, make it the fried chicken sandwich at June&rsquo;s All Day on South Congress. It is the best in the city. For Nashville hot, go to Tumble 22 on Lake Austin Boulevard, three minutes from Lions. For something you will not find anywhere else, get Better Half&rsquo;s Taiwanese spicy chicken. Before an early tee time at Morris Williams, get the Queen Beak at Bird Bird Biscuit.</p>
    <p>Every spot was confirmed open this month from its own website or ordering page. Prices are the ones those pages list, and where a spot does not post a price online we leave it off. Trailers move and hours change, so check before you drive. For more, see our <a href="/drops/sandwiches-before-the-round">sandwiches guide</a>, <a href="/drops/best-wings-in-austin">wings guide</a> and <a href="/drops/austin-food-truck-field-guide">food truck field guide</a>.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Field Note</div>
      <div class="sidebar-detail"><span class="l">Stops</span><span>15</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>June&rsquo;s All Day, $23</span></div>
      <div class="sidebar-detail"><span class="l">Parts of town</span><span>West &amp; South, East, North</span></div>
      <div class="sidebar-detail"><span class="l">Closest to a muni</span><span>Tumble 22, 3 min from Lions</span></div>
      <div class="sidebar-detail"><span class="l">Earliest</span><span>Bird Bird Biscuit, 7:30am</span></div>
      <div class="sidebar-detail"><span class="l">Cheapest</span><span>Spicy Boys OG, $9.49</span></div>
      <div class="sidebar-detail"><span class="l">Checked</span><span>30 Sep 2026</span></div>
      <a href="#west-central-south" class="sidebar-cta">Start near the courses &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#AustinEats</span>
        <span class="hashtag">#ChickenSandwich</span>
        <span class="hashtag">#MuniGolf</span>
        <span class="hashtag">#ATX</span>
      </div>
    </div>
  </aside>
</section>
"""

FAQ = [
    ("Where is the best chicken sandwich in Austin?",
     "Our fifteen, as of September 2026: June's All Day (our pick), Tumble 22, Galaxy Cafe, Better Half, Hattie B's, Loro and Lucy's Fried Chicken in West, Central and South Austin; Bird Bird Biscuit, Ben & Lynn's, Spicy Boys, Cockti, Diablo Hot Chicken and Golden Tiger in East Austin; JewBoy Burgers and Dang Hot 89 in North Austin."),
    ("Where can I get Nashville hot chicken in Austin?",
     "Tumble 22's O.G. comes in six heat levels, from Painless to Stupid Hot, and Hattie B's on South Lamar runs from Southern to Shut the Cluck Up. Diablo Hot Chicken on Webberville Road and Dang Hot 89 at Celis Brewery are the trailer options."),
    ("Which chicken sandwich is closest to an Austin golf course?",
     "Tumble 22 on Lake Austin Boulevard is about three minutes from Lions Municipal. Galaxy Cafe in Clarksville is about five minutes from Lions and Butler Pitch & Putt, Loro on South Lamar is about five minutes from Butler, and Bird Bird Biscuit on Manor Road is about five minutes from Morris Williams."),
    ("Where can I get a chicken sandwich for breakfast in Austin?",
     "Bird Bird Biscuit opens at 7:30am every day, and the Queen Beak is a fried chicken biscuit. Better Half opens at 8am."),
    ("Is there a good grilled chicken sandwich in Austin?",
     "JewBoy Burgers' Can You Grill It? is a grilled marinated thigh with Swiss and bacon for $11. Tumble 22 will also make its O.G. with grilled chicken."),
    ("Are these prices and hours current?",
     "They are what each spot's own website or ordering page showed on 30 September 2026. Several trailers do not post prices or hours online, so the card says to check before you go."),
]

def band(key):
    kick, line, items = BANDS[key]
    figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>'
                     for f, alt, cap in items)
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <p class="cat-kicker"><strong>{kick}</strong>{line}</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


def card(k, idx):
    name, where, dish, copy, hours, url = T[k]
    fr = [f["local"] for f in FR[k]]
    label = H.unescape(name).replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; photo {j+1} of {len(fr)}" loading="lazy" /></div>'
                   for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>'
                   for j in range(len(fr)))
    return (f'<div class="product-card" id="stop-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">No. {idx:02d} &middot; {where}</div>'
            f'<div class="product-name">{name} &middot; {dish}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<div class="product-desc" style="font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;opacity:.7;margin-top:8px">{hours}</div>'
            f'<a href="{H.escape(url)}" target="_blank" rel="noopener" class="product-link">Hours &amp; menu &#8599;</a></div></div>')


def section(sec, n0):
    key, h2, anchor, ids, kicker = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} Stops</div>\n'
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
        for k in ids:
            items.append({"@type": "ListItem", "position": pos, "url": T[k][5], "name": H.unescape(T[k][0])})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-09-30", "dateModified": "2026-09-30",
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
            {"@type": "ListItem", "position": 3, "name": "Best Chicken Sandwiches in Austin", "item": URL}]},
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
    ids = [k for s in SECTIONS for k in s[3]]
    assert len(ids) == 15 == len(set(ids)) and set(ids) == set(T)
    for k in ids:
        assert FR.get(k), f"{k} has no photos"
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Field Notes</a><span>/</span>
  Best Chicken Sandwiches in Austin</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>September 30, 2026</span><span class="dot"></span>
    <span>Austin &middot; 3 parts of town</span><span class="dot"></span>
    <span>15 sandwiches &middot; checked 30 Sep</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Dang Hot 89 fried chicken sandwich with pickles, slaw and sauce, crinkle fries on red-checked paper" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for sec in SECTIONS:
        if sec[0] in BANDS:
            body += band(sec[0])
        s, n = section(sec, n)
        body += s
    body += faq_html()
    out = head_top() + head_rest + body + tail
    print(f"  {n-1} stops")
    if not apply_:
        print("  dry run — pass --apply")
        return
    OUT.write_text(out, encoding="utf-8")
    verify()


def verify():
    fin = OUT.read_text(encoding="utf-8")
    bad = []
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    for leak in ("Manors Revisited", "Knuckle", "Flyrite", "Veracruz All Natural&rsquo;s migas"):
        if leak in above:
            bad.append(f"should not appear: {leak}")
    if fin.count('class="product-card"') != 15:
        bad.append("card count")
    if 'class="pull-quote"' in above:
        bad.append("a pull-quote got in")
    if above.count('class="ig-grid"') != 0:
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
