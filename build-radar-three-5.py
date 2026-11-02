#!/usr/bin/env python3
"""build-radar-three-5.py — Three golf brands on our radar: ITL Golf, Masterpiece Sports Club, 52 Sundays. Cloned from build-radar-three-4.py. 2 November 2026.
Lenny: "Let's do a post about these three brands" (itlgolf.com, masterpiecegolf.com, 52sundays.co), options sheet (110), then "lets build the post" (no picks: ours, 9 each).
FACTS: research/radar5 (catalogues Nov 2, USD). ITL: Our Story page (Stefan Cox, PGA Pro 10+ yrs, grew up outside London); CTV News Calgary (director of instruction, Calgary G&CC).
Masterpiece and 52 Sundays name no founders or city: don't add any.
ORIGINAL DOCSTRING (radar 4): — Three indie brands that caught our eye: Swell Marks, Hinotori Golf, Studio Grain. Cloned from build-radar-three-3.py. 29 October 2026.
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

TITLE = "Feel, Look, Habit: Three Golf Brands on Our Radar (ITL Golf, Masterpiece Sports Club, 52 Sundays)"
DESC = ("Cabretta gloves and leather goods from a Calgary teaching pro, performance golf clothes from Masterpiece Sports Club, "
        "and tees, hats and towels from 52 Sundays. 27 picks with US prices.")
H1 = "Feel, Look, Habit: Three Golf Brands on Our Radar"
BC = "ITL Golf, Masterpiece Sports Club, 52 Sundays"
SLUG = "itl-golf-masterpiece-sports-club-52-sundays"
IMG = "/images/radar-three-5"
SHOP = ""
IT, MS, FS = "ITL Golf", "Masterpiece Sports Club", "52 Sundays"
ITU, MSU, FSU = "https://itlgolf.com/products/", "https://masterpiecegolf.com/products/", "https://52sundays.co/products/"
P = {
 # ITL
 "it-glove": (IT, "ITL 2.0 Signature Glove", "$30", ITU+"mens-itl-2-0-signature-glove-classic-colors",
   "Our pick from ITL, and the glove that started the brand. Cabretta leather cut to 0.5mm for feel, in ten classic colors (Ghost White, Black, Chalk, Sand, Cognac, Baja Blue and more) and nine seasonal ones, from Augusta Green and Sage to Citrus and Retro Pink."),
 "it-practice": (IT, "ITL Practice Glove", "$20", ITU+"mens-itl-practice-glove",
   "The range glove: the same Cabretta leather at 0.75mm, a little thicker so it lasts through long sessions. Ghost White, Steel Blue and Dusty Rose."),
 "it-woods": (IT, "Premium Leather Driver &amp; Fairway Covers", "$110 each", ITU+"itl-premium-leather-driver-cover",
   "Leather barrel covers in three looks: the Vanguard in black and blues, the Prestige in black, forest green and tan, and the Icon in white and black. A driver and fairway bundle is $180."),
 "it-blade": (IT, "Premium Blade Cover", "$110", ITU+"itl-premium-blade-cover",
   "A leather blade putter cover with a patterned lining, in the same three color schemes as the woods covers. A mallet version is also $110."),
 "it-tourn": (IT, "Leather Tournament Belt", "$120", ITU+"mens-itl-leather-tournament-belt",
   "A leather belt with a contrast stripe down the middle and a small ITL badge. Chocolate, Cognac and Black."),
 "it-woodsbelt": (IT, "Leather Woods Belt", "$130", ITU+"mens-itl-leather-woods-belt",
   "Two-tone leather in four pairings: black and ghost white, chocolate and dusty rose, cognac and chocolate, navy and denim blue."),
 "it-wallet": (IT, "Player&rsquo;s Wallet", "$170", ITU+"itl-leather-glove-wallet",
   "A zip leather case that holds a glove, tees, a marker and a scorecard pencil, so the small things stop rolling around the bottom of the bag. Black, Cognac, Chocolate and Midnight Navy."),
 "it-duffle": (IT, "Leather Monarch Duffle", "$700", ITU+"itl-leather-monarch-duffle",
   "The biggest thing ITL makes: a full leather weekend duffle in Cognac, Chocolate or Black. For the golf trip, not the range session."),
 "it-cap": (IT, "The Player&rsquo;s Cap", "$30", ITU+"the-players-cap",
   "A structured five-panel with the ITL icon embroidered flat on the front. Black/White, Forest Green/Stone and Stone."),
 # Masterpiece
 "ms-tritech": (MS, "Tri-Tech Performance Polo", "$118", MSU+"tri-tech-performance-polo-white",
   "Our pick from Masterpiece. A performance polo with small contrast panels at the sides and the club crest on the chest, shown here in white and in black."),
 "ms-wave": (MS, "Wave Polo", "$138", MSU+"wave-polo",
   "The loudest polo in the line: a black-and-gray wave print all over, with a vintage-style label at the collar. Black."),
 "ms-short": (MS, "PROformance Tempo Short", "$128", MSU+"proformance-tempo-short",
   "A golf short with a built-in tee holder at the pocket. Midnight, Sage and a two-tone version."),
 "ms-pant": (MS, "PROformance Tempo Pant", "$138", MSU+"proformance-tempo-pant-2-tone",
   "The two-tone olive pant from the brand&rsquo;s on-course shoot, with darker panels down the legs. Sizes 30 to 40."),
 "ms-hoodie": (MS, "Performance Tech Hoodie", "$138", MSU+"performance-tech-hoodie",
   "A tech hoodie with the script logo across the chest and tee loops on the hem. Midnight or Cream."),
 "ms-vest": (MS, "PROformance Tech Lite Vest", "$148", MSU+"proformance-tech-lite-vest",
   "A lightweight olive vest with darker panels across the front, made to layer over a polo on a cool morning."),
 "ms-glove": (MS, "Apex Gloves", "$35", MSU+"apex-course-glove",
   "Printed golf gloves in Course (a green course-map print), Red Tiger, Camo, Phantom Camo and Stealth. Not every size is in stock in every print."),
 "ms-cap": (MS, "Money Shot Cap", "$50", MSU+"money-shot-cap-red",
   "A trucker-style cap with MONEY SHOT across the front. Red, Green and Midnight."),
 "ms-bag": (MS, "Signature Stand Bag", "$400", MSU+"masterpiece-signature-stand-bag",
   "A stand bag in a pebbled black finish with the script logo down the front. Midnight or White."),
 # 52 Sundays
 "s5-gsup": (FS, "G&rsquo;s Up Holes Down Tee", "$30", FSU+"gs-up-holes-down-tee-black",
   "Our pick from 52 Sundays. A graphic tee with the line on the back, in Black, Forest Green and White."),
 "s5-cherries": (FS, "Sunday Cherries Tee", "$35", FSU+"sunday-cherries-tee",
   "Two golf balls drawn as cherries on a black midweight cotton tee. A few sizes have sold out."),
 "s5-hermosa": (FS, "Hermosa Sage Polo", "$60", FSU+"hermosa-sage-polo",
   "A sage polo with a vertical pattern, named for Hermosa Avenue, which the brand calls a place it is proud to call home. S to XXXL."),
 "s5-fairway": (FS, "Fairway Hat", "$35", FSU+"fairway-hat-pine",
   "A clean cap with a script F, in Pine, Eucalyptus, Indigo Blue, Burgundy and Smoke."),
 "s5-ballhog": (FS, "The Ball Hog Classic Hat", "$35", FSU+"the-ball-hog-classic-black-walnut",
   "A rope hat with a circular patch on the front. Walnut/Black or Tan/Red."),
 "s5-icon": (FS, "52 Icon Headcovers", "$45&ndash;$50", FSU+"icon-driver-cover",
   "Textured blue leatherette covers with a big 52 stitched on. The driver cover is $50 and the 3-wood is $45."),
 "s5-reserve": (FS, "Pro-Five Reserve Driver Headcover", "$50", FSU+"the-pro-five-reserve-driver-headcover",
   "A black driver cover with high-density embroidery, made with Pro-Five Brewery. A limited run."),
 "s5-rope": (FS, "Pro-Five Brewery Rope Hat", "$35", FSU+"pro-five-golf-rope-hat",
   "The other half of the Pro-Five collaboration: a black perforated rope hat with a water- and sweat-repellent finish."),
 "s5-towels": (FS, "Golf Towels", "$15", FSU+"read-the-break-golf-towel",
   "Printed towels with a clip, in Read the Break, Course No.52 and Station 052. The cheapest way into the brand."),
}
SECTIONS = [
 ("ITL Golf (Inside The Leather)", "itl-golf", ["it-glove","it-practice","it-woods","it-blade","it-tourn","it-woodsbelt","it-wallet","it-duffle","it-cap"],
  "<strong>Calgary &middot; nine picks &middot; $20&ndash;$700</strong>It started with one Cabretta glove and grew into leather headcovers, belts and bags, made by a teaching pro."),
 ("Masterpiece Sports Club", "masterpiece-sports-club", ["ms-tritech","ms-wave","ms-short","ms-pant","ms-hoodie","ms-vest","ms-glove","ms-cap","ms-bag"],
  "<strong>Nine picks &middot; $35&ndash;$400</strong>Performance golf clothes with a clubhouse feel, from polos and shorts to a tech hoodie and a stand bag."),
 ("52 Sundays", "52-sundays", ["s5-gsup","s5-cherries","s5-hermosa","s5-fairway","s5-ballhog","s5-icon","s5-reserve","s5-rope","s5-towels"],
  "<strong>Nine picks &middot; $15&ndash;$60</strong>Graphic tees, hats, headcovers and towels. Nothing here is over $60."),
]
N = 27
PQ = {
 "itl-golf": ("The best part of golf isn&rsquo;t always the shot itself&mdash;it&rsquo;s everything around it.", "ITL Golf, on its Our Story page"),
 "masterpiece-sports-club": ("We&rsquo;re here to make golf a lifestyle, not just a game.", "Masterpiece Sports Club, on its About page"),
 "52-sundays": ("Life is better when you golf.", "52 Sundays, on the Sunday Cherries Tee"),
}
CAP = "Photography &middot; each brand&rsquo;s own"
BANDS = {
 "masterpiece-sports-club": ("ITL on the course", "From ITL&rsquo;s own photos.", [("band-1-1","A golfer in an orange ITL glove on the course","Seasonal color"),("band-1-2","Leather ITL headcovers in a golf bag on the fairway","The bag"),("band-1-3","A golfer pulling a white ITL glove from the bag","Classic white")]),
 "52-sundays": ("Masterpiece on the course", "From Masterpiece Sports Club&rsquo;s own photos.", [("band-2-1","A golfer in olive Masterpiece Tempo Pants putting by a lake","Tempo Pant"),("band-2-2","A golfer in the Masterpiece Wave Polo","Wave Polo"),("band-2-3","A golfer with the Masterpiece Signature Stand Bag","Signature Stand Bag")]),
 "end": ("52 Sundays on the course", "From 52 Sundays&rsquo; own photos.", [("band-3-1","A golfer in the 52 Sundays Hermosa Sage Polo","Hermosa Sage Polo"),("band-3-2","A 52 Icon headcover being pulled off a club","52 Icon"),("band-3-3","A Course No.52 towel hanging from a golf bag","Course No.52 towel")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Three brands we came across this week, each built around a different part of the game: the feel of it, the look of it and the habit of it. One began with a single leather glove, one makes performance clothes that want to look at home in the clubhouse, and one is a small line of tees, hats and towels built around the idea of playing every Sunday.</p>
    <p><strong>ITL Golf</strong> stands for Inside The Leather. Stefan Cox, a PGA Professional with more than ten years in the game, grew up outside London, according to ITL&rsquo;s site, and CTV News Calgary has reported him as director of instruction at the Calgary Golf and Country Club. ITL&rsquo;s Our Story page says he couldn&rsquo;t ignore how disposable most golf gloves felt, so he spent years testing Cabretta leather until he had one he liked. The 2.0 Signature Glove is $30, and the line has since grown into leather headcovers, belts, a glove wallet and a $700 duffle.</p>
    <p><strong>Masterpiece Sports Club</strong> calls itself an elevated golf lifestyle brand, &ldquo;from the course to the clubhouse.&rdquo; The clothes are performance pieces with a members&rsquo;-club look: polos with crests and vintage labels, Tempo shorts and pants with tee holders built in, a tech hoodie, a vest, printed gloves and a stand bag. Its About page says golf is personal for its founders but does not name them, so neither do we.</p>
    <p><strong>52 Sundays</strong> started, its Our Story page says, with a simple idea: there are 52 weeks in a year, &ldquo;and if we&rsquo;re doing it right, we&rsquo;re golfing every Sunday.&rdquo; It is the cheapest and most casual of the three: $30 graphic tees, $35 hats, $15 towels and a collaboration with Pro-Five Brewery.</p>
    <h2 class="products-hdr" style="margin-top:32px">Which One Is for You</h2>
    <p><strong>ITL is for the golfer who notices the details.</strong> If you replace a glove the minute it goes stiff, this is your brand. Start with the $30 2.0 Signature Glove, the product ITL was built on, in nineteen colors. Add the $170 Player&rsquo;s Wallet to keep a glove, tees and a marker in one leather case. Save the $700 Monarch Duffle for the golf trip.</p>
    <p><strong>Masterpiece is for the golfer who wants the full outfit.</strong> Buy from it if you like your clothes to match and want to walk from the 18th green into dinner. The Tri-Tech Polo ($118) with the Tempo Short ($128) is the core look, and the short has a tee holder built in. The Tempo Pant and Tech Lite Vest cover cooler mornings. The $35 Apex gloves are the cheapest way to try it.</p>
    <p><strong>52 Sundays is for the weekly game with friends.</strong> These are clothes for the standing tee time with the same group: easy, a little funny and cheap enough to buy a few. Get the G&rsquo;s Up Holes Down Tee ($30) and a Fairway Hat ($35), and wear the Hermosa Sage Polo ($60) on the course. A $15 towel is the easiest gift in this post. Nothing here is over $60.</p>
    <p><strong>If you only buy one thing from each:</strong> the ITL 2.0 Signature Glove, the Masterpiece Tri-Tech Polo and the 52 Sundays Fairway Hat. That is $183 for all three, and you will use every one of them every time you play.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">ITL Golf</span><span>Calgary, Stefan Cox</span></div>
      <div class="sidebar-detail"><span class="l">Masterpiece</span><span>Performance golf clothes</span></div>
      <div class="sidebar-detail"><span class="l">52 Sundays</span><span>Tees, hats, towels</span></div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>27</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$15&ndash;$700</span></div>
      <div class="sidebar-detail"><span class="l">Our picks</span><span>ITL 2.0 Signature Glove, Tri-Tech Polo, G&rsquo;s Up Holes Down Tee</span></div>
      <div class="hashtags">
        <span class="hashtag">#OnOurRadar</span>
        <span class="hashtag">#ITLGolf</span>
        <span class="hashtag">#MasterpieceSportsClub</span>
        <span class="hashtag">#52Sundays</span>
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
    <h2 class="products-hdr" id="last-word">Three Ways Into a Golf Brand</h2>
    <p>These three show how many ways there are to start. ITL began with one object a teaching pro thought could be better, and grew outward from it. Masterpiece started with the whole wardrobe and a name to live up to. 52 Sundays started with a feeling about how often you should be playing.</p>
    <p>None of them is big, and all three sell direct. Buying a glove, a polo or a $15 towel from one of them puts money behind people building something they care about. That is what we look for every week. If you find a brand like this, <a href="/work-with-us">tell us about it</a>.</p>
  </div>
</section>
"""
FRN = json.loads((ROOT / "research/radar5/frames.json").read_text())
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
         "url": URL, "image": og, "datePublished": "2026-11-02", "dateModified": "2026-11-02",
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
    <span>{N} picks &middot; prices checked November 2, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Three photos side by side: a golfer in an ITL glove hitting out of a bunker, a golfer in Masterpiece olive Tempo Pants by a lake, and a golfer in the 52 Sundays Hermosa Sage Polo holding the flagstick" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
    body += band("end")
    body += CLOSE
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Swell Marks", "Hinotori", "Studio Grain", "Kalamunda", "Rookline"):
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
