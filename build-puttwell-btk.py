#!/usr/bin/env python3
"""build-puttwell-btk.py — Brand to Know: Puttwell (cloned from build-ashworth-btk.py). 4 October 2026.\nLenny: "Let's do a brand to know - https://puttwellgolfclub.com/", approved the TGI Take ("looks good, let's build the post"). All in-stock styles (gloves merged into one card). Sources: puttwellgolfclub.com about page and catalogue read 4 Oct 2026; Hypebeast 12 Feb 2025 (Jami Ablan, Sig Zane); Juce Magazine (Drop Zone). Photos: Puttwell store and lookbook images.\n\nLenny: "Let's do a brand to know- https://www.ashworth-golf.com/", then "drop a7,a8,9,a10,a11,a23, then build the post and make sure we have multiple images for each product". 31 picks from research/ashworth/picks.json; catalogue read 3 Oct 2026. Quotes verbatim from FashionUnited (16 Dec 2024), Global Golf Post (7 Mar 2025), Golf Today (14 Dec 2022). Photos: Ashworth's own store images.\n

Lenny: "Let's also do a brand to know - https://magpie-supply.com/", approved the TGI Take ("looks good, let's build it").
All 10 products run (the whole store). FACTS: catalogue, prices and stock read from the Squarespace JSON on 2 Oct 2026
(research/magpie/items.json); story from magpie-supply.com/our-story (quoted verbatim). Founder not named on the site.
PHOTOS: Magpie's own store and site images, localised to /images/magpie-supply.

--- original Palm docstring follows ---

Lenny: "Let's do a brand to know - https://palmgolfco.com/", then "looks good" on the 38-option sheet
(research/palm/options.json), so all 38 run. FACTS: catalogue read from palmgolfco.com/products.json on 2 Oct 2026;
story and founder quotes from MyGolfSpy, "Palm Golf Swings And Smiles Its Way To Cult Following" (Sean Fairholm,
21 Mar 2025, a brand-story feature); the MyGolfSpy comfort line is quoted on Palm's own homepage. Product copy written
from each listing and its photos. PHOTOS: Palm's own store images, localised to /images/palm-golf.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"

TITLE = "Puttwell: The Hawaii Golf Brand With DJ Roots"
DESC = ("Brand to Know: Puttwell, the Hawaii golf brand started by a crew from music and art. The Sig On Smith "
        "Waikahalulu capsule, Extra Butter and Sig Zane collabs, polos, tees and putter covers, with prices.")
H1 = "Brand to Know: Puttwell, the Hawaii Golf Brand That Knows Its Roll"
BC = "Puttwell"
SLUG = "brand-to-know-puttwell"
IMG = "/images/puttwell"
SHOP = "https://puttwellgolfclub.com/products/"
A = "Puttwell"
P = {
 "p05": (f"{A} x Sig On Smith", "Waikahalulu Fridays Only Polo", "$110", "waikahalulu-fridays-only-polo-1",
   "The best thing in the store: a performance polo with a tonal jacquard map of Honolulu&rsquo;s Chinatown, home of the Sig On Smith creative house, and a bold triangle on the back. Quiet from the front, loud from behind. Only an XXL was left when we checked."),
 "p08": (f"{A} x Sig On Smith", "Waikahalulu Golf Bag", "$325", "sig-on-smith-golf-bag",
   "Puttwell&rsquo;s first golf bag, a lightweight carry bag in Sig On Smith&rsquo;s abstract Chinatown map print with blue accents that pick up the neighbourhood&rsquo;s storefronts."),
 "p06": (f"{A} x Sig On Smith", "Waikahalulu Country Club Tee", "$55", "waikahalulu-country-club-tee-3",
   "A members-only back print that is really the opposite: a tribute to Chinatown&rsquo;s open community. &ldquo;Fridays only. Everyone welcome.&rdquo; Down to an XL in black."),
 "p07": (f"{A} x Sig On Smith", "Waikahalulu Country Club Longsleeve", "$65", "waikahalulu-country-club-longsleeve-3",
   "The long-sleeve version, with hand-cut map art of Sig On Smith&rsquo;s neighbourhood across the back. A medium was left."),
 "p09": (f"{A} x Sig On Smith", "Sig On Smith Golf Glove", "$29.95", "sig-on-smith-golf-glove-right-hand",
   "A white glove with a subtle city-map overlay, breathable perforations and a Puttwell pull tab. Sold for right- or left-handed golfers."),
 "p14": (f"{A} x Extra Butter", "Drop Zone Performance Vest", "$120", "extra-butter-performance-vest",
   "From the Drop Zone collection with the New York boutique Extra Butter: a quilted, weather-ready vest with button closure and small co-branded logos front and back. A large was left."),
 "p30": (f"{A} x Sig Zane", "Sig Zane Toon Tee", "$25 (was $50)", "sig-zane-toon-tee",
   "From the Sig Zane collaboration: a cartoon of the Hawaii designer himself unwinding on the golf course. Marked down, in a small only."),
 "p01": (A, "Course Cali Stripe Polo", "$90", "course-cali-stripe-polo",
   "A bone polo with a bold green stripe in a cotton, modal and stretch blend. New in April and the best-looking of the everyday polos."),
 "p02": (A, "Club Polo", "$90", "club-polo",
   "A knit dobby performance polo in navy or tan, with a little stretch and a textured face."),
 "p11": (A, "Course Solid Polo", "$80", "puttwell-course-solid-polo-1",
   "The daily polo: lightweight, breathable stretch fabric, minimal branding and a relaxed fit. Burgundy or denim blue."),
 "p03": (A, "Fairway Quarter Zip Wind Jacket", "$120", "fairway-quarter-zip-wind-jacket",
   "A quarter-zip wind shell in bone or navy, the layer for a breezy back nine."),
 "p04": (A, "Tech Vest", "$90", "puttwell-tech-vest",
   "A black tech vest with the Puttwell wordmark, for cool mornings."),
 "p12": (A, "Gilligan Vest", "$90", "gilligan-vest",
   "A deep-green cotton sweater vest with a ribbed V-neck and a slightly boxy fit, a nod to old golf style."),
 "p13": (A, "Drive Mock Neck L/S", "$100", "drive-mock-neck-l-s",
   "A high-stretch mock neck base layer in black, with Puttwell on the collar and a small logo at the wrist."),
 "p23": (A, "Collide Performance Short", "$85", "collide-performance-short",
   "A water-resistant, lightweight short with an elastic drawcord waist and zip pockets."),
 "p24": (A, "Deep Cuts Tee", "$50", "deep-cuts-tee",
   "The record-crate tee: a back graphic about the overlooked tracks and late sets, in black or bone. This is the DJ side of the brand in one shirt."),
 "p25": (A, "Know Your Roll Tee", "$50", "know-your-roll-tee-1",
   "The tagline across the back of a vintage-washed cotton tee. Know your roll, play your game."),
 "p28": (A, "Wordmark Tee", "$50", "wordmark-tee-1",
   "A heavyweight vintage-wash tee with the Puttwell wordmark on the chest, in bone or washed black."),
 "p27": (A, "Wordmark L/S Tee", "$30 (was $60)", "puttwell-wordmark-l-s-tee",
   "The long-sleeve wordmark tee in deep green, marked down to half price."),
 "p26": (A, "Club Car Tee", "$25 (was $50)", "club-car-tee",
   "An outline of a golf cart on a garment-washed bone tee. Marked down."),
 "p21": (A, "Fast Back Putter Cover", "$45", "fast-back-putter-cover",
   "A contoured synthetic-leather cover for fast-back mallets, with a tonal PW monogram and a magnetic closure."),
 "p16": (A, "Mallet Putter Cover", "$22.50 (was $45)", "mallet-putter-cover-copy",
   "Synthetic leather with green piping, dual-logo embroidery and a magnetic closure, in black or frost. Half price."),
 "p17": (A, "Blade Putter Cover", "$22.50 (was $45)", "blade-putter-cover-copy",
   "The blade version, embroidered with &ldquo;Know Your Roll&rdquo; and the wordmark. Black or frost, half price."),
 "p15": (A, "Driver Cover", "$25 (was $50)", "driver-cover-copy",
   "Puttwell on the front and Know Your Roll on the back, in black or frost. Half price."),
 "p29": (A, "Snake Driver Cover", "$25 (was $50)", "snake-driver-cover",
   "An all-over snake print with the wordmark on the front and Know Your Roll on the back. Half price."),
 "p19": (A, "Metal Ball Marker", "$10", "metal-ball-marker",
   "A magnetic marker with &ldquo;Know Your Roll&rdquo; raised on one side and Puttwell on the other, set in a base with alignment marks."),
 "p18": (A, "Metal Ball Marker 2 Pack", "$12", "metal-ball-marker-2-pack",
   "Two enamel markers in two colours with the Puttwell icons."),
 "p22": (A, "Putting Discs", "$30", "putting-disks",
   "A three-pack of practice discs for working on pace, with a carabiner for the bag. The anti-three-putt kit."),
 "p20": (A, "Know Your Roll Mini Towel", "$30", "know-your-roll-mini-towel",
   "A waffle-knit microfibre towel with Know Your Roll on one side and Puttwell on the other, with a loop for the bag."),
}
SECTIONS = [
 ("The Collaborations", "collabs", ["p05","p08","p06","p07","p09","p14","p30"],
  "<strong>Seven picks &middot; $25&ndash;$325</strong>The Waikahalulu capsule with Honolulu&rsquo;s Sig On Smith is built around Chinatown, with a map print, a tonal polo and Puttwell&rsquo;s first golf bag. Plus the Drop Zone vest with Extra Butter and the last of the Sig Zane collection. Several are down to one size."),
 ("Polos and Layers", "polos", ["p01","p02","p11","p03","p04","p12","p13","p23"],
  "<strong>Eight picks &middot; $80&ndash;$120</strong>The everyday line: clean stretch polos, a wind jacket, two vests, a mock neck and a short. These are the pieces with full size runs."),
 ("The Tees", "tees", ["p24","p25","p28","p27","p26"],
  "<strong>Five picks &middot; $25&ndash;$50</strong>Where the music comes through: Deep Cuts for the crate-diggers, Know Your Roll for the tagline, and the wordmark tees. Two are marked down."),
 ("On the Course", "course", ["p21","p16","p17","p15","p29","p19","p18","p22","p20"],
  "<strong>Nine picks &middot; $10&ndash;$45</strong>Putter and driver covers, magnetic markers, practice discs and a towel. Most of the covers are half price right now."),
]
N = 29
PQ = {
 "polos": ("dress well, play well, treat others well... Puttwell", "Puttwell&rsquo;s brand promise"),
}
BANDS = {
 "collabs": ("Waikahalulu", "Puttwell's own photos from the Sig On Smith capsule.", [("band-1","A golfer on a Honolulu rooftop with the Puttwell x Sig On Smith golf bag","On the roof"),("band-2","A golfer in the Waikahalulu polo and Sig On Smith glove","The polo and glove"),("band-3","A golfer in the Country Club longsleeve on a Chinatown street at night","Chinatown at night")]),
 "polos": ("Know your roll", "", [("band-4","A golfer finishing his swing on a Hawaii course","The finish"),("band-5","A golfer walking a fairway in a Puttwell tee","Down the fairway"),("band-6","Puttwell golfers in a cart under the trees","Cart path")]),
 "tees": ("Deep cuts", "", [("band-7","The back of a Puttwell Hilo, Hawaii tee in black and white","Hilo, Hawaii"),("band-8","The Waikahalulu Country Club back print","Fridays only"),("band-9","A golfer in a Puttwell tee by a golf cart","The tee")]),
 "course": ("On the green", "", [("band-10","A Puttwell putter grip lying on the green","The grip"),("band-11","A Puttwell glove pulling a club from the Sig On Smith bag","From the bag"),("band-12","Hands gripping a Puttwell putter","Flatstick")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Puttwell is a golf brand made by people from the music world, and it shows. It started in Hawaii in 2021 with a crew from music and art, including Jami Ablan, a DJ with the Nocturnal Sound Crew, and it still dresses like it: a tagline of &ldquo;Know your roll,&rdquo; a Deep Cuts tee about the overlooked tracks, and a collaboration with Extra Butter called Drop Zone, a golf rule and a needle on vinyl at the same time. The brand promise fits on a business card: &ldquo;dress well, play well, treat others well... Puttwell.&rdquo;</p>
    <p>Its best work is the Hawaii work. The Sig Zane collection put the kou flower on polos and caps, and the Waikahalulu capsule with Sig On Smith maps Honolulu&rsquo;s Chinatown into a tonal jacquard polo and Puttwell&rsquo;s first golf bag. That sense of place is what separates it from the dozens of streetwear-golf labels that started around the same time. The everyday line &mdash; clean stretch polos, a wind jacket, putter covers and ball markers &mdash; is solid and fairly priced, from $10 markers to $120 layers.</p>
    <p>The honest caveat: it is a small brand that moves in drops. It went quiet for much of 2024, and right now only about 30 styles are in stock, many down to one colour or a few sizes. If something catches your eye, buy it now. Prices were read on Puttwell&rsquo;s own store on 4 October 2026.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>2021, Hawaii</span></div>
      <div class="sidebar-detail"><span class="l">Founders</span><span>A music-and-art collective, including DJ Jami Ablan</span></div>
      <div class="sidebar-detail"><span class="l">Known for</span><span>DJ-culture graphics and Hawaii collaborations</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$10&ndash;$325</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Waikahalulu Fridays Only Polo, $110</span></div>
      <a href="https://puttwellgolfclub.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit Puttwell &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#Puttwell</span>
        <span class="hashtag">#KnowYourRoll</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#HawaiiGolf</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("Where is Puttwell from?", "Hawaii. Puttwell was founded in 2021 by a collective from music and art, and now sells from Hawaii to Los Angeles, New York, Japan and Australia."),
 ("Who founded Puttwell?", "A group of creatives from music and art. One of the founders is Jami Ablan, a DJ with the Nocturnal Sound Crew. The brand does not name the others on its site."),
 ("What does Know Your Roll mean?", "It is Puttwell's tagline, and it appears on tees, towels, ball markers and putter covers. The Know Your Roll tee spells it out: know your roll, play your game."),
 ("What is the Waikahalulu collection?", "A capsule with Sig On Smith, a creative house in Honolulu's Chinatown. It includes a jacquard map-print polo, Country Club tees and Puttwell's first golf bag, which cost $325 on 4 October 2026."),
 ("Which brands has Puttwell collaborated with?", "Sig Zane Designs in Hawaii, the New York boutique Extra Butter on the Drop Zone collection, and Sig On Smith on the Waikahalulu capsule."),
]
FRN = json.loads((ROOT / "research/puttwell/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
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
         "url": URL, "image": og, "datePublished": "2026-10-04", "dateModified": "2026-10-04",
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
            f'    <div class="products-grid">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


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
    <span>Hawaii, since 2021</span><span class="dot"></span>
    <span>29 picks &middot; in stock 4 October 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A Honolulu golf course with the city skyline and mountains behind, from Puttwell" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
    body += faq_html()
    out = head_top() + head_rest + body + tail
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
