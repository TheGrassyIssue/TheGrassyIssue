#!/usr/bin/env python3
"""build-food-trucks.py — The Austin Food Truck Field Guide: 15 stops around town.
26 September 2026.

Lenny: "let's do the best food trucks field guide - 15 stops around town", then
after the 28-option sheet: "build it like a normal post - okay to repeat from
earlier posts - only go with verified options".

PICKS: 15 trucks confirmed operating this month from their own site or
ordering page (research/food-trucks/options.json and the verification pass of
26 Sep). Two changes from the starred 15, both for that rule:
  * Kai Zabb OUT (moved to Celis in June; its own sources disagree on hours).
    KG BBQ IN (repeat from the BBQ Field Guide; Lenny said repeats are fine).
  * Pav Bhaji Express OUT: it has no website, and the only photography is the
    Statesman's. Briscuits IN (repeat from the BBQ Field Guide).
Unconfirmed trucks (Blue Apsara, Song La, Wagyu Yume, Cuantos) are not here.

FACTS: addresses, hours and prices come from each truck's own site or ordering
page, read 26 Sep 2026. Where a truck publishes no prices we give none. Where
sources disagree on hours we say "check before you go" rather than print one.

PHOTOS: each truck's own photography, localised to images/food-trucks-2026/.
Sources in research/food-trucks/frames.json. Hero: Butler Pitch & Putt's own
photo from its Eat & Drink page (Gimme Burger is its on-site truck).

No quotes (standing preference since the towel post). Normal house template:
Take + sidebar, a section per part of town, lookbook bands between sections.
No feed card; that waits for Lenny. Dry run by default.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "austin-food-truck-field-guide"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/food-trucks-2026"
FR = json.loads((ROOT / "research/food-trucks/frames.json").read_text())

TITLE = "The Austin Food Truck Field Guide: 15 Stops Around Town"
DESC = ("Fifteen Austin food trucks we would drive across town for, from breakfast tacos at 7am to "
        "Bib Gourmand barbecue and the smash burger at Butler Pitch & Putt. Hours and prices checked "
        "26 September 2026.")
H1 = "The Austin Food Truck Field Guide &mdash; 15 Stops Around Town"

# key -> (name, where line, dish headline, copy, hours, url)
T = {
 # ---- East Austin
 "veracruz": ("Veracruz All Natural", "The original bus &middot; 2505 Webberville Rd",
   "Migas taco",
   "This is the teal school bus that started it, run by the sisters Reyna and Maritza Vazquez since 2008. Order the migas taco, the one Alton Brown called the best breakfast taco he had eaten.",
   "Mon&ndash;Wed 7am&ndash;3pm &middot; Thu&ndash;Sun 7am&ndash;9pm", "https://www.veracruzallnatural.com/locations"),
 "doughies": ("David Doughie&rsquo;s Bagelry", "At Fleet Coffee &middot; 2427 Webberville Rd",
   "Zhuggy Stardust &middot; $13.75",
   "The bagels are made from Barton Springs Mill grain, aged three days, then boiled and baked. The O.G. with smoked salmon is $16, and Fleet makes the coffee next door.",
   "Thursday to Sunday mornings; check the order page for the day", "https://www.daviddoughies.com"),
 "santa": ("La Santa Barbacha", "The original truck &middot; 2806 Manor Rd",
   "Benito taco &middot; $6",
   "The sisters Daniela and Rosa Landaverde have a Michelin Bib Gourmand for 2024 and 2025, and their site lists them as 2026 James Beard semifinalists. Get the barbacoa taco, also $6.",
   "Daily 7am&ndash;3pm", "https://www.lasantabarbacha.com"),
 "discada": ("Discada", "Outside Chalmers &middot; 1700 E Cesar Chavez St",
   "Three taquitos &middot; $8.50",
   "Beef and pork are cooked together on a plough disc and folded into small taquitos. The Michelin Guide recommends it, and the truck moved here from Rosewood in 2025.",
   "Tue 4&ndash;9pm &middot; Wed&ndash;Sat noon&ndash;9pm &middot; Sun noon&ndash;4pm", "https://www.discadatx.com"),
 "patrizis": ("Patrizi&rsquo;s", "At the Vortex &middot; 2307 Manor Rd",
   "Carbonara Alexandra &middot; $17",
   "The cousins Nic and Matt Patrizi have been making fettuccine by hand on this patio since 2013. The cacio e pepe is $15, and it is the best dinner on a picnic table in town.",
   "Daily 5&ndash;9:30pm", "https://patrizis.com/manor-road"),
 "kgbbq": ("KG BBQ", "At Oddwood Brewing &middot; 3108 Manor Rd",
   "Brisket rice bowl &middot; $18.50",
   "Kareem El-Ghayesh puts an Egyptian spin on Texas barbecue: pomegranate and za&rsquo;atar pork ribs at $17 and smoked lamb chops. It is about a mile from Morris Williams.",
   "Thursday to Sunday from 11am, until sold out", "https://www.kgbbq.com/"),
 # ---- South & Central
 "gimme": ("Gimme Burger", "At Butler Pitch &amp; Putt &middot; 201 Lee Barton Dr",
   "Double smash with American cheese",
   "This is the only truck actually parked on an Austin muni. Michael Fojtasek of Olamaie leads the food, the courtyard is open to non-golfers, and the fried okra is the side to get.",
   "Daily noon&ndash;8pm &middot; breakfast sandwiches Fri&ndash;Sun 8&ndash;11am", "https://butlerpitchandputt.com/eat-drink"),
 "twogoose": ("Two Goose Market &amp; Barbecue", "Clarksville &middot; 706 N Lamar Blvd",
   "Big Honkin&rsquo; breakfast burrito &middot; $16",
   "It opened in December 2025 out of a 1956 Spartan trailer and is already on Southern Living&rsquo;s list of the best new barbecue. It is about a mile from Lions, so it is the stop before an early tee time.",
   "Wed&ndash;Sat 7am&ndash;2pm &middot; Sun 10am&ndash;2pm", "https://www.twogoosebbq.com/"),
 "eggman": ("Eggman ATX", "At The Picnic &middot; 1720 Barton Springs Rd",
   "Bodega Classic &middot; $8.95",
   "Eggman makes New York bodega breakfast sandwiches on a custom kaiser roll. The Big Mess is $12.95, and it is half a mile from Butler Pitch &amp; Putt.",
   "Daily 7am&ndash;1:30pm", "https://www.eggmanatx.com"),
 "briscuits": ("Briscuits", "At Radio Coffee &amp; Beer &middot; 4204 Menchaca Rd",
   "Brisket &amp; jelly biscuit &middot; $17.50",
   "Christopher McGhee and William Spence put barbecue on biscuits, and Michelin gave them a Bib Gourmand for it. The pimento cheese grits are $5.",
   "Thu&ndash;Sat 9am&ndash;3pm &middot; Sun 9am&ndash;1:30pm", "https://briscuits.com/"),
 "distant": ("Distant Relatives", "At Meanwhile Brewing &middot; 3901 Promontory Point Dr",
   "Smoked chicken with chile vinegar butter",
   "Damien Brockway&rsquo;s barbecue traces African American cooking back through the South, and it holds a Michelin Bib Gourmand. The house sausage and the tallow-fried Texas toast are the other orders.",
   "Wednesday to Sunday from noon", "https://www.distatantrelativesatx.com/"),
 "marisquero": ("El Marisquero Seafood", "South Austin &middot; 2056 W Stassney Ln",
   "Aguachile rojo",
   "This is Sinaloa-style seafood: aguachile, a stacked ceviche called the 3 Amigos and Baja fish tacos. It is BYOB, and a second truck runs Friday to Sunday on Colton-Bluff Springs Road.",
   "Daily noon&ndash;7pm", "https://elmarisqueroseafoodtx.com"),
 # ---- North
 "parish": ("Parish Barbecue", "At Austin Beerworks Sprinkle Valley &middot; 10300 Springdale Rd",
   "Prime brisket, half pound &middot; $20",
   "Holden Fulco came through Franklin and InterStellar and cooks with a Louisiana accent. The pulled duck with crispy skin is $25 a half pound, and Michelin gave it a Bib Gourmand in October 2025.",
   "Thu 11am&ndash;8pm &middot; Fri&ndash;Sat 11am&ndash;9pm &middot; Sun 11am&ndash;8pm", "https://parishbarbecue.com"),
 "tlocs": ("T-Loc&rsquo;s Sonora Hot Dogs", "Burnet Road &middot; 5000 Burnet Rd",
   "Hot dog con todo",
   "Miguel Kaiser, who cooked at Per Se, and Zulma Nataren brought the Sonoran dog from Tucson: bacon-wrapped, in a steamed bun they still bring in from Tucson every week. Get a carne asada burrito too.",
   "Tue&ndash;Wed 11am&ndash;3pm &middot; Thu&ndash;Sat 11am&ndash;3pm &amp; 5&ndash;8pm &middot; Sun 11am&ndash;2:30pm", "https://www.tlocs.com"),
 "yenis": ("Yeni&rsquo;s Fusion", "At Night Owl &middot; 8315 Burnet Rd",
   "Empal gentong",
   "Yeni Rosdiyani&rsquo;s menu is the food of West Java. The empal gentong is a coconut curry soup with smoked brisket, and the beef rendang and batagor are close behind. Everything is halal.",
   "Tue&ndash;Sun 4&ndash;10pm, or until sold out", "https://www.yenisfusion.com"),
}

SECTIONS = [
    ("east", "East Austin", "east-austin", ["veracruz", "doughies", "santa", "discada", "patrizis", "kgbbq"],
     "<strong>Six stops &middot; breakfast to dinner</strong>Webberville Road has the mornings, and Manor Road has the rest of the day. "
     "Morris Williams is the nearest muni."),
    ("south", "South &amp; Central", "south-and-central", ["gimme", "twogoose", "eggman", "briscuits", "distant", "marisquero"],
     "<strong>Six stops &middot; closest to Butler and Lions</strong>This section has the one truck on a course, two breakfasts within a mile of a first tee, and two Bib Gourmand barbecue trailers."),
    ("north", "North Austin", "north-austin", ["parish", "tlocs", "yenis"],
     "<strong>Three stops &middot; up Burnet Road and beyond</strong>Parish, T-Loc&rsquo;s and Yeni&rsquo;s are Louisiana barbecue behind a brewery, Sonoran dogs and Indonesian curry."),
]

BANDS = {
    "south": ("Photography &middot; the trucks&rsquo; own",
              "These are Veracruz, La Santa Barbacha and KG BBQ, away from the plate.",
              [("band-1", "The Veracruz All Natural trailer under a blue umbrella, with a customer and a dog on the grass", "Veracruz"),
               ("band-2", "A person from behind in a cowboy hat and a La Santa Barbacha t-shirt", "La Santa Barbacha"),
               ("band-3", "Kareem El-Ghayesh of KG BBQ plating food at an outdoor table", "KG BBQ")]),
    "north": ("Photography &middot; the trucks&rsquo; own",
              "These show Butler Pitch &amp; Putt, where Gimme Burger parks, and the Veracruz patio.",
              [("band-4", "A green flag on a short hole at Butler Pitch & Putt with people playing behind", "Butler Pitch &amp; Putt"),
               ("band-5", "A musician playing guitar beside a cooler at Butler Pitch & Putt", "Music at Butler"),
               ("band-6", "Picnic tables under shade sails at a Veracruz All Natural patio", "Veracruz")]),
}

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Austin eats out of trailers better than most cities eat in restaurants, and the best of them are parked next to a brewery or a coffee shop with a picnic table and room for a golf bag. This is our field guide: fifteen trucks, in three parts of town, from breakfast tacos at 7am to Bib Gourmand barbecue in the afternoon.</p>
    <p>If you only make one stop, go to Gimme Burger at Butler Pitch &amp; Putt. It is the one truck in town that is actually on a golf course, and a smash burger after nine short holes is hard to beat. For breakfast before a tee time, Two Goose is a mile from Lions. For the best meal on a picnic table, Patrizi&rsquo;s.</p>
    <p>Every truck here was confirmed open this month from its own website or ordering page, and the hours and prices are what those pages showed on 26 September 2026. Trucks move and sell out, so check before you drive. We have written about some of these before, in our <a href="/drops/austin-bbq-field-guide">BBQ Field Guide</a> and <a href="/drops/ranking-the-muni-grub-every-on-course-food-spot-in-austin">muni food rankings</a>.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Field Guide</div>
      <div class="sidebar-detail"><span class="l">Stops</span><span>15</span></div>
      <div class="sidebar-detail"><span class="l">Parts of town</span><span>East, South, North</span></div>
      <div class="sidebar-detail"><span class="l">Earliest</span><span>7am: Veracruz, La Santa, Eggman, Two Goose</span></div>
      <div class="sidebar-detail"><span class="l">Latest</span><span>Yeni&rsquo;s, to 10pm</span></div>
      <div class="sidebar-detail"><span class="l">On a course</span><span>Gimme Burger, Butler</span></div>
      <div class="sidebar-detail"><span class="l">Checked</span><span>26 Sep 2026</span></div>
      <a href="#south-and-central" class="sidebar-cta">Start near the courses &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#AustinFoodTrucks</span>
        <span class="hashtag">#AustinEats</span>
        <span class="hashtag">#MuniGolf</span>
        <span class="hashtag">#ATX</span>
      </div>
    </div>
  </aside>
</section>
"""

FAQ = [
    ("What are the best food trucks in Austin right now?",
     "Our fifteen, as of September 2026: Veracruz All Natural, David Doughie's, La Santa Barbacha, Discada, Patrizi's and KG BBQ in East Austin; Gimme Burger, Two Goose, Eggman, Briscuits, Distant Relatives and El Marisquero in South and Central; Parish Barbecue, T-Loc's and Yeni's Fusion in North Austin."),
    ("Is there a food truck at an Austin golf course?",
     "Yes, one. Gimme Burger is the permanent on-site truck at Butler Pitch & Putt, open daily from noon to 8pm, and the courtyard is open to non-golfers. The other city courses have clubhouse kitchens rather than trucks."),
    ("Which Austin food trucks are open for breakfast?",
     "Veracruz All Natural, La Santa Barbacha, Eggman ATX and Two Goose all open at 7am on their serving days. David Doughie's bagels and Briscuits are morning-only trucks, and Gimme Burger does breakfast sandwiches Friday to Sunday from 8am."),
    ("Which Austin food trucks have a Michelin Bib Gourmand?",
     "In this guide: La Santa Barbacha, Briscuits, Distant Relatives and Parish Barbecue. Discada is recommended in the Michelin Guide."),
    ("Where is the nearest good food truck to Lions Municipal?",
     "Two Goose Market & Barbecue at 706 N Lamar is about a mile away and opens at 7am Wednesday to Saturday, which suits an early tee time."),
    ("Do Austin food trucks keep regular hours?",
     "Most publish hours, but many close when they sell out and some move. Every truck here was confirmed on its own site or ordering page on 26 September 2026; check the link on each card before you go."),
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
            f'<div class="product-body"><div class="product-brand">Stop {idx:02d} &middot; {where}</div>'
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
         "url": URL, "image": og, "datePublished": "2026-09-26", "dateModified": "2026-09-26",
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
            {"@type": "ListItem", "position": 3, "name": "Austin Food Truck Field Guide", "item": URL}]},
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
  Austin Food Truck Field Guide</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>September 26, 2026</span><span class="dot"></span>
    <span>Austin &middot; 3 parts of town</span><span class="dot"></span>
    <span>15 trucks &middot; checked 26 Sep</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Friends at a green picnic table at Butler Pitch &amp; Putt, one in an Austin 49 jersey, with the course behind them" fetchpriority="high" /></div></div>
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
    for leak in ("Burnt Orange", "Manors Revisited", "Kai Zabb", "Pav Bhaji", "Knuckle", "Blue Apsara"):
        if leak in above:
            bad.append(f"should not appear: {leak}")
    if fin.count('class="product-card"') != 15:
        bad.append("card count")
    if 'class="pull-quote"' in above:
        bad.append("a pull-quote got in")
    if above.count('class="ig-grid"') != 2:
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
