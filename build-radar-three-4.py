#!/usr/bin/env python3
"""build-radar-three-4.py — Three indie brands that caught our eye: Swell Marks, Hinotori Golf, Studio Grain. Cloned from build-radar-three-3.py. 29 October 2026.
Lenny: "three indie brands that caught our eye this week" (swellmarks.com, hinotorigolf.com, studiograin.store), then "Let's build it" (picks ours).
FACTS: research/radar-three-4/cat.txt + im.txt (live catalogues Oct 29, all three stores price in USD) and the brands' own pages.
Swell Marks: maker is a U.S. Navy Meteorology and Oceanography Officer (About page) with a Coronado, California workshop (1893 listing); no name given, don't add one.
Hinotori: no About page, no named founder. Hanover, Minnesota per its Parscape directory listing. Studio Grain: "two best friends" (YouTube bio); no names.
No FAQ (Lenny doesn't want The Questions sections).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "3 Indie Golf Brands That Caught Our Eye: Swell Marks, Hinotori, Studio Grain"
DESC = ("Hand-engraved brass ball markers from a Navy oceanographer, Japanese-inspired gloves and headcovers from Minnesota, "
        "and caps from two friends with a YouTube channel. 23 picks with US prices.")
H1 = "Three Indie Golf Brands That Caught Our Eye This Week"
BC = "Swell Marks, Hinotori, Studio Grain"
SLUG = "swell-marks-hinotori-studio-grain-indie-golf-brands"
IMG = "/images/radar-three-4"
SHOP = ""
SW, HI, SG = "Swell Marks", "Hinotori Golf", "Studio Grain"
SWU, HIU, SGU = "https://swellmarks.com/products/", "https://hinotorigolf.com/products/", "https://studiograin.store/products/"
P = {
 # Swell Marks
 "sw-trestles": (SW, "Trestles", "$65", SWU+"trestles",
   "Our pick from Swell Marks. Solid copper, deep-relief engraved and torch finished, inspired by Lower Trestles in San Clemente, where cobblestones on the seafloor shape the swell into clean peaks. The torch leaves every marker a slightly different color."),
 "sw-skulligan": (SW, "Skulligan", "$75", SWU+"skulligan",
   "The newest marker, added October 28. A grinning skull cut from solid brass, with a stainless steel inlay and a pair of sunglasses with teal accents. Swell Marks says it has &ldquo;a healthy disregard for taking the game too seriously.&rdquo;"),
 "sw-redfin": (SW, "Fin Theory &middot; Red Fin B&bull;001", "$75", SWU+"fin-theory-red-fin-b-001",
   "The first release in Fin Theory, a limited series based on surfboard fins. This one is shaped after the Red Fin Mike Hynson introduced through Gordon &amp; Smith in 1965, made in fiberglass and resin."),
 "sw-goodbones": (SW, "Good Bones", "$65", SWU+"good-bones",
   "A shaka that is half hand, half skeleton, in brass filled by hand with polyester surfboard resin. The back has a vertebrae wave and &ldquo;Know the Break.&rdquo; Three resin colors: Sea Glass, Deep Ocean and Sunset."),
 "sw-wave": (SW, "Wave", "$65", SWU+"wave",
   "Stainless steel with deep-relief waves taken from traditional Japanese woodblock prints. The first piece in the Nagare Collection, a series about the way water moves."),
 "sw-pipeline": (SW, "Pipeline", "$65", SWU+"pipeline",
   "Brass, engraved with the hollow barrel of Pipeline on O&rsquo;ahu&rsquo;s North Shore, where deep-water swell hits a shallow reef. The most detailed engraving in the range."),
 "sw-lightning": (SW, "Lightning", "$65", SWU+"lightning",
   "A lightning bolt cutting across a field of repeating waves, in deep-relief brass. The idea: every swell starts as energy from a storm somewhere far away."),
 "sw-1893": (SW, "1893", "$50", SWU+"1893-brass-golf-ball-marker",
   "A tribute to the U.S. Navy Chief Petty Officer community, named for the year the Chief&rsquo;s Mess was founded. Made to order in Chief, Senior Chief or Master Chief, and assembled in the maker&rsquo;s Coronado, California workshop."),
 "sw-pitch": (SW, "Resin Pitch Tools 001&ndash;015", "$30 each", "https://swellmarks.com/collections/pitch-tools",
   "The first run of pitch tools from the Swell Marks garage: a hand-poured resin handle on a single stainless steel prong. Fifteen were made, each one a different color, and six were still in stock when we checked."),
 # Hinotori
 "hi-ryujin-hc": (HI, "Ryujin Barrel Headcover", "From $58", HIU+"ryujin-barrel-headcover",
   "Our pick from Hinotori. A cream barrel cover wrapped in a blue dragon, Ryujin, the dragon god of the sea in Japanese legend. Driver and wood are $68, the hybrid is $58. Pair it with the matching towel."),
 "hi-duck": (HI, "Duck Camo Barrel Headcover", "$58", HIU+"duck-camo-barrel-headcover",
   "Old-school duck camo in earth tones, made, Hinotori says, for golfers who&rsquo;d rather be in the blind at sunrise. Driver, wood and hybrid, all $58."),
 "hi-enso": (HI, "Enso Glove Case", "$80", HIU+"enso-glove-case",
   "A flat case that keeps your glove from getting crushed in the bottom of the bag. Slide the glove in after the 18th, clip the case to the outside. In Lotus or Cherry Blossom prints."),
 "hi-timekeeper": (HI, "The Time Keeper Ball Marker", "$78", HIU+"the-time-keeper-ball-marker",
   "A heavy marker shaped like the classic course clock, made with Luxury Ball Marks. Fewer than 100 were made, and it comes in a green presentation box."),
 "hi-cherry": (HI, "Cherry Blossom Signature Glove", "$28", HIU+"cherry-blossom",
   "AAA Cabretta leather with breathable Lycra side panels and a cherry blossom print on the back. In men&rsquo;s and women&rsquo;s, left or right hand."),
 "hi-seigaiha": (HI, "Seigaiha Signature Glove", "$28", HIU+"mens-seigaiha-signature-glove",
   "The same Cabretta glove with a seigaiha pattern, the overlapping waves found on Japanese textiles, in coral red. Men&rsquo;s and women&rsquo;s."),
 "hi-sentinel": (HI, "Sentinel Performance Hat", "$35", HIU+"sentinel-performance-hat",
   "A tan performance cap with a skeletal stag on the front, from the fall collection. It comes in three sizes, including an XXL for bigger heads that rarely fit standard caps."),
 "hi-towel": (HI, "Ryujin Towel", "$30", HIU+"ryujin-towel",
   "Waffle-weave microfiber with the Ryujin dragon on it, made to match the headcover. Lighter than a cotton towel and quicker to dry."),
 # Studio Grain
 "sg-members": (SG, "Club Members Snapback, Fairway Green", "$40", SGU+"members-hat",
   "Our pick from Studio Grain. A green snapback with &ldquo;A Club For Those Who Tried Their Best&rdquo; on the front. The friendliest golf slogan we&rsquo;ve seen this year."),
 "sg-letterman": (SG, "Brown Grain Lettermen Snapback", "$35", SGU+"brown-grain-lettermen-snapback-hat",
   "A lightweight brown snapback with a pressed varsity-letter GRAIN logo on the front and the script logo stitched on the side."),
 "sg-camo": (SG, "Camo Outdoors Program Hat", "$35", SGU+"camo-studio-grain-outdoors-program-hat",
   "Woodland camo with a Velcro back and &ldquo;Studio Grain Outdoor Program&rdquo; pressed on the front. A hat, they write, &ldquo;for both on and off the course.&rdquo;"),
 "sg-shades": (SG, "Fairway Finders Sunglasses", "$30", SGU+"sunglasses",
   "Chunky square frames in tortoise or black, with gold logos on the arms. &ldquo;Hope these bring you good luck,&rdquo; says the listing."),
 "sg-beanie": (SG, "Fisherman Beanie", "$25", SGU+"fisherman-beanie-green",
   "A short rib-knit fisherman beanie with the script logo, in green, gray or navy. The early tee time option."),
 "sg-deck": (SG, "GRAIN Fingerboard Deck", "$25", SGU+"grain-fingerboard-deck-ocean-blue",
   "Not golf, but the most Studio Grain thing in the store. Handmade fingerboard decks with the three-trees logo, and the brand warns &ldquo;all boards are different.&rdquo; Five finishes."),
}
SECTIONS = [
 ("Swell Marks", "swell-marks", ["sw-trestles","sw-skulligan","sw-redfin","sw-goodbones","sw-wave","sw-pipeline","sw-lightning","sw-1893","sw-pitch"],
  "<strong>Coronado, California &middot; nine picks &middot; $30&ndash;$75</strong>Ball markers in brass, copper and stainless steel, engraved and finished by hand, each named after a surf break or a story. Most are made in small runs, so check stock before you fall for one."),
 ("Hinotori Golf", "hinotori-golf", ["hi-ryujin-hc","hi-duck","hi-enso","hi-timekeeper","hi-cherry","hi-seigaiha","hi-sentinel","hi-towel"],
  "<strong>Hanover, Minnesota &middot; eight picks &middot; $28&ndash;$80</strong>Gloves, headcovers and accessories built around Japanese art and legend, plus a line of bird and animal caps. Most gloves are $28 in both men&rsquo;s and women&rsquo;s."),
 ("Studio Grain", "studio-grain", ["sg-members","sg-letterman","sg-camo","sg-shades","sg-beanie","sg-deck"],
  "<strong>Two friends &middot; six picks &middot; $25&ndash;$40</strong>A small store run alongside a YouTube channel: caps, beanies, sunglasses and handmade fingerboards. Nothing here is over $40."),
]
N = 23
PQ = {
 "swell-marks": ("The ocean sets the standard.", "Swell Marks, on its home page"),
 "hinotori-golf": ("A small detail that makes a big difference.", "Hinotori Golf, on the Enso Glove Case"),
 "studio-grain": ("A club for those who tried their best.", "Studio Grain, on the Club Members Snapback"),
}
CAP = "Photography &middot; each brand&rsquo;s own"
BANDS = {
 "swell-marks": ("From the Swell Marks garage", "Markers on the workbench, on the truck and on the green.", [("band-1","Swell Marks Good Bones shaka markers in green, blue and orange resin on the grass with an old truck behind","Good Bones"),("band-2","Brass and steel Swell Marks markers lined up on a weathered wooden bench in the garage","The workbench"),("band-3","Brass Red Fin markers shaped like surfboard fins scattered on a wooden table","Fin Theory")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Three brands we came across this week, and none of them is trying to be the next big golf apparel label. One makes ball markers in a garage, one started with a glove, and one is two friends with a YouTube channel and a handful of caps. What they share is that each one starts with something the person behind it already loved, the ocean, Japanese art, or just playing golf with friends, and puts it on a small piece of golf kit.</p>
    <p><strong>Swell Marks</strong> is the most crafted of the three. Its About page says the maker is a U.S. Navy Meteorology and Oceanography Officer who has spent nearly two decades studying the ocean, and the markers read like it. Each one is named after a wave, a break or a story: Trestles, Pipeline, a Japanese woodblock wave, a shaka that is half skeleton, a Red Fin based on a 1965 surfboard fin. They are solid brass, copper or stainless steel, engraved in deep relief and finished by hand in a Coronado, California workshop. Most are $65, and many are small runs that sell out. The newest drops are a skull marker called Skulligan and a first batch of fifteen resin pitch tools, each a different color. The maker doesn&rsquo;t give his name, so we won&rsquo;t either.</p>
    <p><strong>Hinotori Golf</strong> is Japanese for firebird, and most of its range draws on Japanese art and legend. The signature gloves are $28 in AAA Cabretta leather, with backs printed in cherry blossom, bonsai, seigaiha waves and a blue dragon, in men&rsquo;s and women&rsquo;s fits. Around them are barrel headcovers, a matching towel, a glove case and a marker made with Luxury Ball Marks. It also makes performance caps with birds and animals on them, from a cardinal to the skeletal stag in this fall&rsquo;s collection. Sixty products, nearly all in stock, and almost nothing over $80.</p>
    <p><strong>Studio Grain</strong> is the smallest and the most fun. Its YouTube bio says it is two best friends &ldquo;learning the process of creating&rdquo;, and the channel is them playing: a series called Golf Is Hard, scrambles, rounds at Olivas Links and in Big Bear, and a podcast. The store has fourteen products. The one that sums it up is a green cap that says &ldquo;A Club For Those Who Tried Their Best.&rdquo;</p>
    <h2 class="products-hdr" style="margin-top:32px">What They Have in Common</h2>
    <p><strong>Golf from the side.</strong> None of the three starts with the course. Swell Marks starts with surf, Hinotori with Japanese art, Studio Grain with friends making videos. Golf is where it all ends up.</p>
    <p><strong>Small things, done carefully.</strong> A marker, a glove, a cap. These are the cheapest ways to make a golf bag look like yours, and all three brands put their effort there.</p>
    <p><strong>Made in small batches.</strong> Numbered resin tools, a marker made in fewer than 100, fingerboards where &ldquo;all boards are different.&rdquo; If you like something, don&rsquo;t wait.</p>
    <h2 class="products-hdr" style="margin-top:32px">Which One Is for You</h2>
    <p><strong>Swell Marks is for the golfer who surfs, or wishes they did.</strong> Start with Trestles or Good Bones.</p>
    <p><strong>Hinotori is for the golfer who wants the bag to say something.</strong> The Ryujin headcover and towel together are the place to start, and the $28 gloves are the easy add.</p>
    <p><strong>Studio Grain is for the golfer who plays for fun first.</strong> Get the Club Members cap.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Swell Marks</span><span>Coronado, CA</span></div>
      <div class="sidebar-detail"><span class="l">Hinotori Golf</span><span>Hanover, MN</span></div>
      <div class="sidebar-detail"><span class="l">Studio Grain</span><span>Two best friends</span></div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>23</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$25&ndash;$80</span></div>
      <div class="sidebar-detail"><span class="l">Our picks</span><span>Trestles, Ryujin Barrel Headcover, Club Members Snapback</span></div>
      <div class="hashtags">
        <span class="hashtag">#OnOurRadar</span>
        <span class="hashtag">#SwellMarks</span>
        <span class="hashtag">#HinotoriGolf</span>
        <span class="hashtag">#StudioGrain</span>
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
    <h2 class="products-hdr" id="last-word">Why We Keep Looking for Brands Like These</h2>
    <p>Most of what ends up in a golf bag is bought without much thought: a sleeve of balls, a glove off the rack, whatever marker came free with the hat. These three brands are a reminder that the small things don&rsquo;t have to be throwaways.</p>
    <p>A Swell Marks marker comes with a surf break and a story behind it, engraved by hand by someone who has spent nearly two decades studying the ocean. A Hinotori glove puts a cherry blossom or a sea dragon on the hand you grip the club with, for $28. And a Studio Grain cap is a small way to back two friends whose channel is mostly them playing golf together, and who put the kindest line in golf on the front of it.</p>
    <p>None of them will change your handicap. They might change how your bag feels when you open it on the first tee, and they put your money behind people who are making things because they care about them. That is what we look for every week. If you find a brand like this, <a href="/work-with-us">tell us about it</a>.</p>
  </div>
</section>
"""
FRN = json.loads((ROOT / "research/radar-three-4/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-R4-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-10-29", "dateModified": "2026-10-29",
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
    <span>On Our Radar</span><span class="dot"></span>
    <span>{N} picks &middot; prices checked October 29, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Three photos side by side: a copper Swell Marks Trestles marker next to a golf ball on the green, a Hinotori Ryujin headcover and towel on a bag on the fairway, and a golfer in a green Studio Grain Club Members cap mid-swing" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
    body += CLOSE
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Kalamunda", "Aberdeen", "Grind City", "We Hit Fairways", "Rookline", "Bethpage", "LBB", "GolfPass"):
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
