#!/usr/bin/env python3
"""build-black-friday-2026.py — Black Friday 2026 at independent golf brands. 21 November 2026.
Lenny: "Let's do a black friday round up" -> options sheet (43 brands from the TGI index with a Black Friday deal on their own site)
-> "build it" (all of them; Rhoback has no product photos, so it sits in the table only; big brands left out).
FACTS: each deal line is read from the brand's own homepage banner on Nov 21, 2026 (research/black-friday-2026/sweep.json);
product prices and compare-at prices from each store's products.json the same day (picks.json). Non-US stores show local
currency with rough USD (AUD .65, NZD .59, GBP 1.27, EUR 1.08). "% at checkout" prices are computed from the banner. No FAQ.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"
TITLE = "Black Friday 2026: The Best Deals From Independent Golf Brands"
DESC = ("Black Friday 2026 deals from 42 independent golf brands, checked on their own sites: Puttwell, Eastside, Radmor, Devereux, "
        "Sunday Golf, Casualist and more, with codes, end dates and marked-down picks.")
H1 = "Black Friday 2026: The Best Deals From Independent Golf Brands"
BC = "Black Friday 2026"
SLUG = "black-friday-2026-independent-golf-brands"
IMG = "/images/black-friday-2026"
SHOP = ""
PK = json.loads((ROOT / "research/black-friday-2026/picks.json").read_text())
FRN = json.loads((ROOT / "research/black-friday-2026/frames.json").read_text())
CUR = {'axxa':('A$',.65),'gray-haast':('A$',.65),'penta-golf':('A$',.65),'walker-golf-things':('A$',.65),'hiroki-golf':('NZ$',.59),
       'f-and-co':('NZ$',.59),'royal-albartross':('£',1.27),'sounder':('£',1.27),'duke-dexter':('£',1.27),'fella-golf':('€',1.08),'macade':('€',1.08)}
BR = {  # slug: (name, deal, code/how, ends, status, site)
 'axxa':('AXXA','Up to 67% off sitewide.','No code','—','Live','https://www.axxa.com.au/'),
 'aberdeen-west':('Aberdeen West','20% off sitewide, taken off at checkout.','No code','Nov 30','Live','https://aberdeenwest.com/'),
 'apres-golf':('Apr&egrave;s Golf','Category codes: STUFFERS40, HOODIES30, KIDS30, FLUFFY25 and HATS20.','Codes','—','Live','https://apresgolf.com/'),
 'avoda-golf':('Avoda Golf','Early Black Friday: 20% off Origin iron sets, 10% off wedges.','No code','—','Live','https://avodagolf.com/'),
 'bet-on-the-horses':('B.O.T.H. (Bet On The Horses)','Black Friday sale across the entire collection.','See site','—','Live','https://betonthehorses.co/'),
 'birdie-balm':('Birdie Balm','25% off the entire store.','No code','—','Live','https://birdiebalm.co/'),
 'casualist':('Casualist','Black Friday kits and bundles, plus 10% off with CASUAL10.','CASUAL10','—','Live','https://casualist.com/'),
 'devereux-golf':('Devereux Golf','30% off sitewide; headcovers excluded.','No code','—','Live','https://devereuxgolf.com/'),
 'dimple-divot':('Dimple &amp; Divot','Holiday bundles 15&ndash;20% off.','No code','Nov 30','Live','https://dimpledivot.com/'),
 'dormie-workshop':('Dormie Workshop','Black Friday and Cyber Monday sale starts Nov 27 at 9am ET.','—','—','Starts Nov 27','https://dormieworkshop.com/'),
 'duke-dexter':('Duke + Dexter','Black Friday launches Friday, Nov 27; sign up for 24-hour early access.','—','—','Starts Nov 27','https://dukeanddexter.com/'),
 'eastside-golf':('Eastside Golf','40% off sitewide; exclusions apply.','No code','—','Live','https://eastsidegolf.com/'),
 'edel-golf':('Edel Golf','Black Friday putters and marked-down gear, up to 57% off.','No code','—','Live','https://edelgolf.com/'),
 'edison-golf':('Edison Golf','15% off all wedges, plus free gifts with two or more wedges.','No code','—','Live','https://edisonwedges.com/'),
 'evnroll':('Evnroll','20% off all Zero Torque and EZPZ Reverse Torque putters, plus select accessories.','No code','—','Live','https://www.evnroll.com/'),
 'f-and-co':('F AND CO.','Hat bundles: 20% off two, 30% off three, 35% off four or more, applied at checkout.','No code','—','Live','https://fandco.co.nz/'),
 'fella-golf':('Fella Golf','Black Friday early access by email sign-up.','—','—','Coming','https://fellagolf.com/'),
 'ghost-golf':('Ghost Golf','$100 off select bags, up to 50% off select apparel (final sale).','No code','—','Live','https://ghostgolf.com/'),
 'gray-haast':('Gray + Haast','Black Friday edit, up to 55% off; free cap on orders over A$220.','No code','—','Live','https://grayandhaast.com/'),
 'grind-city-golf':('Grind City Golf','20% off all orders for the whole month, applied at checkout.','No code','Nov 30','Live','https://grindcitygolf.com/'),
 'hiroki-golf':('Hiroki Golf','Up to 40% off while stock lasts.','No code','—','Live','https://hirokigolf.com/'),
 'howie-benson':('Howie Benson','25% off polos, 40% off long sleeves.','No code','—','Live','https://howiebenson.com/'),
 'juniper-james':('Juniper &amp; James','20% off select styles, plus free socks.','No code','—','Live','https://juniperjamesgolf.com/'),
 'kingfisher-golf':('Kingfisher Golf','40% off sitewide.','No code','—','Live','https://kingfisher-golf.com/'),
 'macade':('Macade','Black Friday is coming; club members get early access.','—','—','Coming','https://macadegolf.com/'),
 'mantra-golf':('Mantra Golf','Early Black Friday: up to 60% off sitewide; exclusions apply.','No code','—','Live','https://mantragolf.com/'),
 'morning-people-clothiers':('Morning People Clothiers','36% off with code BlackFriday.','BlackFriday','—','Live','https://morningpeopleclothiers.com/'),
 'palm-golf-co':('Palm Golf Co.','Up to 75% off; any two hats for $75 this week.','No code','Nov 22 (two-hat deal)','Live','https://palmgolfco.com/'),
 'penta-golf':('Penta Golf','30% off sitewide.','No code','—','Live','https://penta-golf.com/'),
 'pins-and-aces':('Pins &amp; Aces','Up to 50% off; $100 off golf bags.','No code','—','Live','https://pinsandaces.com/'),
 'pluto-golf':('Pluto Golf','Buy one, get one 50% off all footwear with code BLACKFRIDAY; marked-down apparel and hats.','BLACKFRIDAY','—','Live','https://www.pluto.golf/'),
 'puttwell':('Puttwell','60% off sitewide.','No code','—','Live','https://puttwellgolfclub.com/'),
 'radmor':('Radmor','30% off all styles.','No code','—','Live','https://radmorgolf.com/'),
 'royal-albartross':('Royal Albartross','Black Friday sale on shoes and accessories, up to 62% off.','No code','—','Live','https://albartross.com/'),
 'stix-golf':('STIX','Up to $320 off every set, no code needed.','No code','—','Live','https://stix.golf/'),
 'sounder':('Sounder','Black Friday sale, up to 80% off.','No code','—','Live','https://soundergolf.com/'),
 'stick-grips':('Stick Grips','20% off sitewide.','No code','—','Live','https://stickgripsgolf.com/'),
 'sunday-golf':('Sunday Golf','25% off sitewide, per the banner; bags are also marked down.','No code','—','Live','https://sundaygolf.com/'),
 'takomo-golf':('Takomo Golf','A free wedge, putter or fairway wood with qualifying orders.','No code','Nov 29','Live','https://takomogolf.com/'),
 'walker-golf-things':('Walker Golf Things','Black Friday sale, up to 50% off.','No code','—','Live','https://www.walkergolfthings.com/'),
 'western-birch':('Western Birch','Buy one, get one 50% off all tees and Driving Nails.','No code','—','Live','https://westernbirch.com/'),
 'woodgrain-golf':('Woodgrain Golf','A Black Friday drop with a countdown on the homepage; sign up for early access.','—','—','Coming','https://woodgrain.golf/'),
}
PCT = {'aberdeen-west':20,'kingfisher-golf':40,'morning-people-clothiers':36,'grind-city-golf':20,'penta-golf':30,'puttwell':60,'eastside-golf':40,'devereux-golf':30,'birdie-balm':25,'radmor':30,'stick-grips':20}
COMING = {'dormie-workshop','duke-dexter','fella-golf','macade','woodgrain-golf'}
def money(slug, x):
    c = CUR.get(slug)
    if not c: return f"${x:,.2f}".replace('.00', '')
    return f"{c[0]}{x:,.0f} (~${x*c[1]:,.0f})"
def clean(t):
    t = re.sub(r"\s*\|\s*", ", ", t); t = re.sub(r"\s+-\s+", ", ", t)
    return H.escape(t.strip()) if t.isupper() is False else H.escape(t.title())
P, KEYS = {}, {}
for slug in BR:
    KEYS[slug] = []
    for j, x in enumerate(PK.get(slug, [])):
        k = f"{slug}--{j}"
        if k not in FRN or not FRN[k]: continue
        pr, was = x['price'], x['was']
        if was:
            price = f"{money(slug, pr)} <span style='opacity:.6'><s>{money(slug, was)}</s></span>"
            copy = f"Marked down {round(100*(1-pr/was))}% on {BR[slug][0]}&rsquo;s own site."
        elif slug in PCT:
            price = f"{money(slug, pr*(1-PCT[slug]/100))} <span style='opacity:.6'>after {PCT[slug]}% (list {money(slug, pr)})</span>"
            copy = f"List price {money(slug, pr)}; the {PCT[slug]}% comes off at checkout."
        elif slug in COMING:
            price = f"{money(slug, pr)} <span style='opacity:.6'>(full price today)</span>"
            copy = "Full price as of November 21. One to watch when the sale opens."
        else:
            price = money(slug, pr)
            copy = f"See the deal above; {BR[slug][0]}&rsquo;s discount applies."
        P[k] = (BR[slug][0], clean(x['title']), price, x['url'], copy)
        KEYS[slug].append(k)
SECTIONS = [
 ("Clothes and Shoes", "clothes", ['puttwell','mantra-golf','eastside-golf','kingfisher-golf','radmor','devereux-golf','howie-benson','casualist','morning-people-clothiers','aberdeen-west','grind-city-golf','juniper-james','gray-haast','axxa','penta-golf','sounder','walker-golf-things','pluto-golf','royal-albartross','bet-on-the-horses'],
  "<strong>20 brands</strong>Polos, knits, hoodies, pants and shoes. Sitewide percentages first, then the marked-down edits."),
 ("Hats, Headcovers and Small Things", "accessories", ['palm-golf-co','apres-golf','f-and-co','hiroki-golf','dimple-divot','birdie-balm','western-birch','pins-and-aces'],
  "<strong>Eight brands</strong>The stocking-stuffer end of Black Friday: caps, putter covers, brushes, balm and tees."),
 ("Clubs, Putters, Grips and Bags", "gear", ['stix-golf','avoda-golf','edison-golf','edel-golf','evnroll','takomo-golf','stick-grips','sunday-golf','ghost-golf'],
  "<strong>Nine brands</strong>Iron sets, wedges, putters, grips and bags from the direct-to-consumer makers."),
 ("Starting Soon", "soon", ['dormie-workshop','duke-dexter','woodgrain-golf','macade','fella-golf'],
  "<strong>Five brands</strong>Not live when we checked. Here is when they open, and what we would look at first."),
]
N = sum(len(KEYS[b]) for s in SECTIONS for b in s[2])
NB = sum(len(s[2]) for s in SECTIONS)
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


def _unused_faq():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>'
                     for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')




def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items, pos = [], 1
    for sec in SECTIONS:
        for h in [k for b in sec[2] for k in KEYS[b]]:
            items.append({"@type": "ListItem", "position": pos, "url": P[h][3], "name": H.unescape(f"{P[h][0]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-11-21", "dateModified": "2026-11-21",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
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
            f'  <figure style="margin:0 0 28px"><img src="{IMG}/banner-{anchor}.jpg" alt="{H.escape(H.unescape(h2))}, from the brand&rsquo;s own photos" loading="lazy" style="width:100%;aspect-ratio:2/1;object-fit:cover;display:block;background:#e8e2d6" /></figure>\n'
            f'  <div class="drop-tag grass">{len(ids)} {"pick" if len(ids)==1 else "picks"}</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}" style="font-size:clamp(44px,7vw,84px);line-height:1;margin:14px 0 16px;letter-spacing:-.01em">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)



def brand_block(slug, n0):
    # v4 (22 Nov): a 3:2 brand image (not one of the three picks), name large to its right; v3 was a small 4:5 box with the brand name large to its right, then the three picks
    name, deal, code, ends, st, site = BR[slug]
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(KEYS[slug]))
    bn = f"{IMG}/bn/{slug}.jpg"
    box = (f'<div class="bf-box"><img src="{bn}" alt="{H.escape(H.unescape(name))}, from the brand&rsquo;s own photos" loading="lazy" /></div>'
           if (ROOT / bn.lstrip("/")).is_file() else "")
    meta = []
    if code not in ("No code", "—", "See site", "Codes"): meta.append(f"Code <strong>{code}</strong>")
    if ends != "—": meta.append(f"Ends {ends}")
    if st != "Live": meta.append(f'<span style="color:#a0522d">{st}</span>')
    meta.append(f'<a href="{site}" target="_blank" rel="noopener">{site.split("//")[1].strip("/")} &#8599;</a>')
    o = (f'\n  <div class="bf-brand" id="{slug}">\n    <div class="bf-head">{box}<div class="bf-txt">'
         f'<h3 class="bf-name">{name}</h3><p class="bf-deal">{deal}</p><p class="bf-meta">{" &middot; ".join(meta)}</p></div></div>\n')
    if cards: o += f'    <div class="products-grid" data-n="{len(KEYS[slug])}">\n{cards}\n    </div>\n'
    return o + '  </div>\n', n0 + len(KEYS[slug])


def section(sec, n0):
    h2, anchor, ids, kicker = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <figure style="margin:0 0 28px"><img src="{IMG}/banner-{anchor}.jpg" alt="{H.escape(H.unescape(h2))}, from the brand&rsquo;s own photos" loading="lazy" style="width:100%;aspect-ratio:2/1;object-fit:cover;display:block;background:#e8e2d6" /></figure>\n'
            f'  <div class="drop-tag grass">{len(ids)} {"pick" if len(ids)==1 else "picks"}</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}" style="font-size:clamp(44px,7vw,84px);line-height:1;margin:14px 0 16px;letter-spacing:-.01em">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)



def section(sec, n0):
    h2, anchor, slugs, kicker = sec
    body = ""
    for s in slugs:
        b, n0 = brand_block(s, n0); body += b
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <h2 class="products-hdr" id="{anchor}" style="font-size:clamp(40px,6vw,72px);line-height:1;margin:14px 0 16px">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n{body}</section>\n'), n0


def table():
    rows = ""
    for s in SECTIONS:
        for slug in s[2]:
            name, deal, code, ends, st, site = BR[slug]
            rows += (f'<tr><td><a href="#{slug}">{name}</a></td><td>{deal}</td><td>{code if code not in ("No code",) else "&mdash;"}</td>'
                     f'<td>{st if st != "Live" else (ends if ends != "—" else "Live")}</td></tr>\n')
    rows += ('<tr><td><a href="https://rhoback.com/" target="_blank" rel="noopener">Rhoback</a></td><td>20% off sitewide, no code needed.</td><td>&mdash;</td><td>Live</td></tr>\n')
    return ('\n<section class="products" style="margin-top:8px">\n  <h2 class="products-hdr" id="all-deals">Every Deal at a Glance</h2>\n'
            '  <p class="cat-kicker">Read from each brand&rsquo;s own site on November 21, 2026. Tap a name to jump to its picks.</p>\n'
            '  <div style="overflow-x:auto"><table class="bf-table" style="width:100%;border-collapse:collapse;font-size:14px">\n'
            '<thead><tr><th>Brand</th><th>Deal</th><th>Code</th><th>Status / ends</th></tr></thead><tbody>\n' + rows +
            '</tbody></table></div>\n</section>\n')


def band():
    figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{a}" loading="lazy" /><figcaption class="ig-cap">{c}</figcaption></figure>'
                     for f, a, c in [("band-1", "A golfer in a Juniper &amp; James quarter-zip mid-swing", "Juniper &amp; James"),
                                     ("band-2", "A golfer in a Howie Benson polo on the course", "Howie Benson"),
                                     ("band-3", "A golfer in a Walker Golf Things polo on the course", "Walker Golf Things")])
    return (f'\n<section class="products" style="margin-top:8px;">\n  <p class="cat-kicker"><strong>On sale, on the course</strong>From the brands&rsquo; own photos.</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Black Friday is the one week a year when the small golf brands we cover put real money on the table, and most of them do it quietly, in a banner at the top of their own site. So we went and read the banners. On November 21 we checked every independent brand in the TGI index with a website, and 42 of them had a Black Friday deal live or announced.</p>
    <p>This is that list, with the big names left out. For each brand you get the deal in one line, any code, the end date where they gave one, and three marked-down pieces we would actually buy. Prices are from each store that morning; non-US brands show their own currency with a rough dollar figure.</p>
    <p><strong>The biggest numbers:</strong> Puttwell at 60% off sitewide, Mantra at up to 60%, Eastside and Kingfisher at 40% off everything, and Palm Golf Co. with any two hats for $75. <strong>The brands we have covered before:</strong> Radmor and Devereux at 30%, Sunday Golf at 25%, Howie Benson at 25&ndash;40%, Hiroki at up to 40%, and Casualist&rsquo;s Black Friday kits. <strong>Codes to remember:</strong> Apr&egrave;s Golf&rsquo;s category codes, Morning People&rsquo;s BlackFriday for 36% off, CASUAL10 at Casualist and BLACKFRIDAY at Pluto.</p>
    <p>Deals change by the hour this week and stock goes fast, so check the brand&rsquo;s site before you count on a price. Five brands, including Dormie Workshop and Woodgrain, open their sales later in the week; we will update this page when they do.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>42 + Rhoback</span></div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>__N__</span></div>
      <div class="sidebar-detail"><span class="l">Checked</span><span>November 21, 2026</span></div>
      <div class="sidebar-detail"><span class="l">Biggest</span><span>Puttwell, 60% off sitewide</span></div>
      <div class="sidebar-detail"><span class="l">Starts later</span><span>Dormie, Duke + Dexter, Woodgrain, Macade, Fella</span></div>
      <div class="hashtags">
        <span class="hashtag">#BlackFriday</span>
        <span class="hashtag">#IndependentGolf</span>
        <span class="hashtag">#TheGrassyIssue</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">disclosure</a></div>
  </aside>
</section>
"""
CLOSE = """
<section class="products" style="margin-top:8px;padding-top:48px">
  <div class="writeup-body" style="max-width:720px;margin:0 auto">
    <div class="drop-tag grass">The Last Word</div>
    <h2 class="products-hdr" id="last-word">Buy the Thing You Already Wanted</h2>
    <p>The best Black Friday purchase is the one that was already in your cart in October. Start with the brands you know, use the table to see who is cheapest this week, and leave the rest. Most of these are small companies, and a sale week is a big part of their year.</p>
    <p>Looking for gift ideas past the deals? Our three-part <a href="/drops/golf-gift-guide-2026-everyday-range-rat-stocking-stuffers">2026 gift guide</a> starts with stocking stuffers. Deals were read on November 21, 2026; if a brand you love is running one we missed, <a href="/work-with-us">tell us about it</a>.</p>
  </div>
</section>
"""
GRID_CSS = ('<style>/*TGI-R4-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:flex-start;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}'
            '.bf-brand{margin:64px 0 0}.bf-head{display:flex;align-items:center;gap:32px;margin:0 0 24px}.bf-box{flex:0 0 min(440px,46%)}.bf-box img{width:100%;aspect-ratio:3/2;object-fit:cover;display:block;background:#e8e2d6}.bf-txt{flex:1;min-width:0}.bf-name{font-family:var(--serif,Georgia,serif);font-size:clamp(40px,6.4vw,88px);line-height:.95;letter-spacing:-.015em;margin:0 0 14px}.bf-deal{font-size:clamp(17px,1.8vw,22px);line-height:1.35;margin:0 0 10px}.bf-meta{font-family:var(--mono);font-size:11px;letter-spacing:.06em;text-transform:uppercase;opacity:.8;margin:0}.bf-meta a{border-bottom:1px solid currentColor}@media(max-width:600px){.bf-head{flex-direction:column;align-items:flex-start;gap:14px}.bf-box{flex-basis:auto;width:100%}.bf-name{font-size:40px;margin-bottom:8px}.bf-deal{font-size:16px}}'
            '.bf-table th,.bf-table td{text-align:left;padding:9px 10px;border-bottom:1px solid rgba(45,74,43,.2);vertical-align:top}.bf-table th{font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase}.bf-table a{border-bottom:1px solid currentColor}</style>\n')
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"


def main(apply_):
    for s in SECTIONS:
        for b in s[2]:
            for k in KEYS[b]:
                assert all((ROOT / f.lstrip("/")).is_file() for f in FRN[k]), k
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
    <span>The Edit</span><span class="dot"></span>
    <span>{NB} brands &middot; {N} picks &middot; deals checked November 21, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Three photos side by side: a golfer swinging in a Casualist vest, a golfer in a Gray + Haast crew with a golf bag, and a golfer in a Radmor knit polo on a course terrace" fetchpriority="high" /></div></div>
"""
    body += TAKE.replace("__N__", str(N)) + table()
    n = 1
    for i, s in enumerate(SECTIONS):
        if i == 1: body += band()
        o, n = section(s, n); body += o
    body += CLOSE
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards, {NB} brands")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Mackem",):
        if leak in above: bad.append("leak " + leak)
    if fin.count('class="product-card"') != N: bad.append("card count")
    txt = re.sub(r"<[^>]+>", " ", above)
    for w in ("worth", "genuinely", "honestly", "straightforward", "selling out"):
        if re.search(rf"\b{w}\b", txt, re.I): bad.append("banned word " + w)
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
