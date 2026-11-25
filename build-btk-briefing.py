#!/usr/bin/env python3
"""build-btk-briefing.py — Brand to Know: BRIEFING (BRIEFING GOLF), 25 November 2026.
Lenny: "Let's do a brand to know - https://www.briefing-us.com/" then "lets build it" (picks made by Claude).
FACTS: research/briefing (subagent report: briefing-us.com history/about pages, WWD Japan, fashionsnap, alba.co.jp),
product pages on briefing-us.com read Nov 25, 2026. PRICES: the store is based in Tokyo and priced in yen; it presented
MYR to our fetcher, so yen = MYR / 0.02658 (store rate), rounded to ¥100, USD at ~¥150. No FAQ.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "brand-to-know-briefing-golf"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/briefing"
TITLE = "Brand to Know: BRIEFING, the Japanese Bag Brand Built to Military Spec, and Its Golf Line"
DESC = ("BRIEFING started in 1998 making bags in a US factory that built gear for the military. Its golf line brings ballistic nylon, "
        "Cordura and Dyneema to caddie bags, cart totes and headcovers. 28 picks, with prices in yen and dollars.")
H1 = "Brand to Know: BRIEFING"
FRAMES = json.loads((ROOT / "research/briefing/frames.json").read_text(encoding="utf-8"))

P = {
 "B1": ("BRIEFING GOLF", "CR-9 #02, DL Series", "&yen;120,400 (~$805)", "https://www.briefing-us.com/products/brg263d25",
        "The DL Series caddie bag: matte 500D Cordura ripstop with patches of ECCO leather layered with Dyneema, sized to fit any car. About 3.5 kg, in black, light olive or red brown."),
 "B2": ("BRIEFING GOLF", "CR-10 #02", "&yen;122,300 (~$815)", "https://www.briefing-us.com/products/brg241d39",
        "BRIEFING&rsquo;s pro bag for tour travel: 1680D &times; 840D air ballistic nylon and a carbon stand co-developed with shaft maker Graphite Design. About 4.6 kg."),
 "B5": ("BRIEFING GOLF", "CR-4 #04 &times; Pendleton", "&yen;105,300 (~$700)", "https://www.briefing-us.com/products/bgw263d04",
        "Pendleton&rsquo;s Harding pattern in a camo-inspired colorway made only for BRIEFING, on 610D Cordura polyester oxford. Pendleton has been making wool in Oregon since 1909."),
 "B4": ("BRIEFING GOLF", "CR-4 #04 Nubuck Holiday", "&yen;109,100 (~$725)", "https://www.briefing-us.com/products/brg263d57",
        "The 2026 holiday edition: matte ripstop with waterproof nubuck accents custom-made by ECCO Leather. Beige, green or blue."),
 "B3": ("BRIEFING GOLF", "CR-4 #04 Vivid Metallic", "&yen;118,500 (~$790)", "https://www.briefing-us.com/products/brg263d49",
        "Hollow ballistic nylon with Italian color-foil cowhide from ECCO Leather and glass-enamel logos. A limited run in green or blue."),
 "B6": ("BRIEFING GOLF", "CR-4 #04 Quilted MIL", "&yen;97,800 (~$650)", "https://www.briefing-us.com/products/brg263d07",
        "The MIL Collection is back after three years: military quilting in recycled 210D Cordura nylon twill, finished in gold."),
 "B7": ("BRIEFING GOLF", "CR-5 #04 Mint Kobe 20th", "&yen;90,300 (~$600)", "https://www.briefing-us.com/products/brg263d43",
        "A mint-blue cart bag made for the 20th anniversary of MINT KOBE, with white logos and parts."),
 "B13": ("BRIEFING GOLF", "Self Stand Carry", "&yen;34,600 (~$230)", "https://www.briefing-us.com/products/brg253d05",
        "A stand carrier for a half set, with V-shaped resin separators that grip irons and wedges. Four colors, built for the range or a quick nine."),
 "B14": ("BRIEFING GOLF", "Cart Tote DL", "&yen;24,600 (~$165)", "https://www.briefing-us.com/products/brg263t31",
        "The DL treatment in a cart tote: Cordura ripstop and ECCO-and-Dyneema leather panels, slim enough for a tight trunk."),
 "B17": ("BRIEFING GOLF", "Cart Tote &times; Pendleton", "&yen;21,100 (~$140)", "https://www.briefing-us.com/products/bgw263t09",
        "Pendleton&rsquo;s Harding pattern on 610D Cordura, with a BRIEFING &times; PENDLETON tag on the front."),
 "B18": ("BRIEFING GOLF", "Turf Wire Quilted MIL", "&yen;54,600 (~$365)", "https://www.briefing-us.com/products/brg263t23",
        "A gold-quilted Boston bag for shoes, layers and gear, in recycled 210D Cordura twill."),
 "B20": ("BRIEFING GOLF", "US Slash Golf Cart Tote", "&yen;39,500 (~$265)", "https://www.briefing-us.com/products/brg253t60",
        "Made in the USA: BRIEFING restarted American production of golf pieces for Fall/Winter 2025. In 1050-denier ballistic nylon, &ldquo;the heaviest material used by BRIEFING.&rdquo;"),
 "B23": ("BRIEFING GOLF", "US Stand Up Shoe Bag", "&yen;41,400 (~$275)", "https://www.briefing-us.com/products/brg253g66",
        "From the same Made in USA run, in the same ballistic nylon."),
 "B24": ("BRIEFING GOLF", "Driver Cover DL", "&yen;12,400 (~$85)", "https://www.briefing-us.com/products/brg263g26",
        "500D Cordura ripstop with a boa lining and a patch of ECCO leather layered with Dyneema."),
 "B28": ("BRIEFING GOLF", "Driver Cover &times; Pendleton", "&yen;12,400 (~$85)", "https://www.briefing-us.com/products/bgw263g05",
        "Harding pattern on 610D Cordura, with a plush lining."),
 "B29": ("BRIEFING GOLF", "Rhino Driver Cover", "&yen;18,600 (~$125)", "https://www.briefing-us.com/products/brg263g40",
        "The rhino is BRIEFING&rsquo;s mascot for Cordura&rsquo;s toughness. 500D Cordura TrueLock, water-repellent, in four colors."),
 "B30": ("BRIEFING GOLF", "Rhino Fairway Wood Cover", "&yen;17,300 (~$115)", "https://www.briefing-us.com/products/brg263g41",
        "The rhino&rsquo;s smaller sibling, in 500D ballistic Cordura TrueLock."),
 "B31": ("BRIEFING GOLF", "Driver Cover Vivid Metallic", "&yen;14,900 (~$100)", "https://www.briefing-us.com/products/brg263g51",
        "ECCO Leather color-foil cowhide on hollow ballistic nylon, to match the bag."),
 "B34": ("BRIEFING GOLF", "Barrel Driver Cover Mint Kobe 20th", "&yen;11,100 (~$75)", "https://www.briefing-us.com/products/brg263g44",
        "Mint blue with white logos and a boa lining, made to match the anniversary bag."),
 "B37": ("BRIEFING GOLF", "Transport Cover DL", "&yen;45,100 (~$300)", "https://www.briefing-us.com/products/brg263g33",
        "A travel cover for a full caddie bag: Cordura ripstop body, Dyneema-backed leather panels."),
 "B38": ("BRIEFING GOLF", "US Golf Ball Holster", "&yen;14,900 (~$100)", "https://www.briefing-us.com/products/brg253g65",
        "Made in USA ballistic nylon, built to clip onto the bag."),
 "B41": ("BRIEFING GOLF", "Enamel Circle B Medal Marker", "&yen;9,400 (~$65)", "https://www.briefing-us.com/products/brg261g30",
        "Glossy enamel with the B mark in three colors."),
 "B43": ("BRIEFING GOLF", "Grimloc Golf", "&yen;3,100 (~$20)", "https://www.briefing-us.com/products/brg221g73",
        "The Fidlock magnetic clip that holds BRIEFING putter covers on, sold on its own in seven colors. The cheapest way into the brand."),
 "B45": ("BRIEFING GOLF", "BRIEFING &times; EPON Wedge Set", "&yen;118,500 (~$790)", "https://www.briefing-us.com/products/bgs251g06",
        "52&deg; and 58&deg; forged wedges based on EPON&rsquo;s Tour Wedge Type M, from the forging specialist in Tsubame-Sanjo, Niigata. The second EPON collaboration."),
 "B47": ("BRIEFING GOLF", "Windblock Rib Knit Parka", "&yen;75,200 (~$500)", "https://www.briefing-us.com/products/brg263m53",
        "Quilted taffeta with rib knit and a windproof two-layer laminate in the sleeves, from the Urban Athlete line."),
 "B50": ("BRIEFING GOLF", "Tour Polo", "&yen;21,100 (~$140)", "https://www.briefing-us.com/products/bbg261m03",
        "From the Basics line: a high-gauge textured yarn that wicks moisture."),
 "B53": ("BRIEFING GOLF", "WR Cordura Round Logo Hat", "&yen;10,500 (~$70)", "https://www.briefing-us.com/products/brg263m99",
        "A four-way-stretch Cordura bucket hat with two logos placed on opposite sides."),
 "B54": ("BRIEFING GOLF", "Washi &times; Cordura High Socks", "&yen;5,100 (~$35)", "https://www.briefing-us.com/products/brg261md4",
        "Cordura cotton legs with soles blended with washi, Japanese paper, for breathability."),
}

GROUPS = [
 ("caddie-bags", "Caddie Bags", "The CR Series",
  "BRIEFING numbers its caddie bags CR-something; the CR-4 is the flagship stand bag. These are the current CR bags we&rsquo;d look at first, from the DL Series to the tour bag.",
  ["B1", "B2", "B5", "B4", "B3", "B6", "B7", "B13"]),
 ("totes", "Cart Totes &amp; Bags", "For the Cart and the Car",
  "Cart totes, a Boston bag and the first golf pieces made in the USA again since BRIEFING restarted American production.",
  ["B14", "B17", "B18", "B20", "B23"]),
 ("headcovers", "Headcovers", "Covers, Including a Rhino",
  "Matching covers for most of the bags above, plus the rhino, BRIEFING&rsquo;s stand-in for Cordura itself.",
  ["B24", "B28", "B29", "B30", "B31", "B34"]),
 ("on-course", "On Course", "The Small Stuff and a Wedge Set",
  "Travel cover, ball holster, marker, magnetic clip and the EPON wedges.",
  ["B37", "B38", "B41", "B43", "B45"]),
 ("apparel", "Apparel", "Urban Golf, Worn",
  "BRIEFING GOLF makes a full apparel line; these four are the ones that lean hardest on its materials.",
  ["B47", "B50", "B53", "B54"]),
]

BANDS = {
 "a": ("Urban Golf", [
   ("band-a1.jpg", "Two BRIEFING caddie bags in a bright concrete room", "Caddie bags &middot; BRIEFING GOLF"),
   ("band-a2.jpg", "BRIEFING &times; Pendleton caddie bag, cart tote and covers stacked on a red rug", "BRIEFING &times; Pendleton"),
   ("band-a3.jpg", "Two BRIEFING caddie bags on a wooden porch looking out at trees", "BRIEFING GOLF")]),
 "b": ("On the Course", [
   ("band-b1.jpg", "A golfer carrying a tan BRIEFING stand bag on a fairway, talking with a friend", "MIL Collection &middot; BRIEFING GOLF"),
   ("band-b2.jpg", "A hand pulling a quilted cover off a club in an olive BRIEFING stand bag on the grass", "CR-4 #04 Quilted MIL"),
   ("band-b3.jpg", "A man in the woods with a quilted olive BRIEFING bag over his shoulder", "MIL Collection &middot; BRIEFING GOLF")]),
 "c": ("Off the Course", [
   ("band-c1.jpg", "A hand carrying a navy and tan BRIEFING cart tote", "Cart tote &middot; BRIEFING GOLF"),
   ("band-c2.jpg", "Two BRIEFING caddie bags on a wooden deck in front of a green wall", "BRIEFING GOLF"),
   ("band-c3.jpg", "A man leaning on a brick wall with a BRIEFING shoulder bag", "Off duty &middot; BRIEFING")]),
}

CSS = ('<style>/*TGI-BRIEFING-BTK*/'
       '.products-grid[data-n]{grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}'
       '@media(max-width:1024px){.products-grid[data-n]{grid-template-columns:repeat(2,minmax(0,1fr))}}'
       '.fb-h{font-family:var(--serif);font-weight:600;font-size:clamp(22px,2.4vw,28px);margin:36px 0 12px}'
       '.fb-tbl{width:100%;border-collapse:collapse;margin:14px 0 22px;font-size:14.5px}.fb-tbl th{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;text-align:left;color:#2D4A2B;padding:8px 10px;border-bottom:.5px solid var(--ink)}'
       '.fb-tbl td{padding:10px;border-bottom:.5px solid rgba(20,20,20,.18);vertical-align:top;line-height:1.45}.fb-tbl td:first-child{font-family:var(--serif);font-size:17px;white-space:nowrap}'
       '.fb-pq{font-family:var(--serif);font-size:clamp(22px,2.4vw,28px);line-height:1.35;color:#2D4A2B;margin:24px 0;padding:4px 0 4px 20px;border-left:2px solid #2D4A2B}'
       '.fb-src{font-family:var(--mono);font-size:10px;letter-spacing:.06em;opacity:.6;line-height:1.7;margin-top:22px}'
       '@media(max-width:820px){.fb-tbl .hm{display:none}.fb-tbl td:first-child{white-space:normal}}'
       '</style>\n')


def card(k):
    brand, name, price, url, copy = P[k]
    fr = FRAMES[k]
    label = H.escape(H.unescape(re.sub(r"<[^>]+>", "", f"{brand} {name}")).replace('"', ""), quote=True)
    imgs = "".join(f'<div class="pg-frame"><img src="{IMG}/{f}" alt="{label}{f" &middot; view {j+1} of {len(fr)}" if len(fr) > 1 else ""}" loading="lazy" /></div>' for j, f in enumerate(fr))
    nav = ""
    if len(fr) > 1:
        dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>' for j in range(len(fr)))
        nav = (f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button><button class="pg-arw next" aria-label="Next image">&#8250;</button>'
               f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div>')
    return (f'<div class="product-card" id="p-{k.lower()}" data-frames="{len(fr)}"><div class="product-gallery"><div class="pg-track">{imgs}</div>{nav}</div>'
            f'<div class="product-body"><div class="product-brand">{brand}</div><div class="product-name">{name} &middot; {price}</div>'
            f'<div class="product-desc">{copy}</div><a href="{url}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


def band(k):
    figs = "".join(f'<figure><img src="{IMG}/{s}" alt="{a}" loading="lazy" /><figcaption class="ig-cap">{c}</figcaption></figure>' for s, a, c in BANDS[k][1])
    return f'\n<section class="products" style="margin-top:8px;">\n  <div class="drop-tag grass">{BANDS[k][0]}</div>\n  <div class="ig-grid" style="margin-top:18px">{figs}</div>\n</section>\n'


def pq(text, who):
    return (f'\n<div class="pull-quote" style="margin:56px auto 24px">\n  <div class="pull-quote-inner">&ldquo;{text}&rdquo;'
            f'<span class="pull-quote-attr">&mdash; {who}</span></div>\n</div>\n')


def group(k, tag, cap, intro, ids):
    cards = "\n".join(card(i) for i in ids)
    return (f'\n<section class="products" style="margin-top:8px;">\n  <div class="drop-tag grass">{len(ids)} picks</div>\n'
            f'  <h2 class="products-hdr" id="{k}">{cap}</h2>\n  <p class="cat-kicker"><strong>{tag}</strong>{intro}</p>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n</section>\n')


TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p><strong>It started as a bag brand with a military supplier.</strong> BRIEFING was launched in 1998 by Yuji Nakagawa as a label inside his Japanese company, Celts. He went to the United States looking for a factory that could build to U.S. military spec, and found one that made bags for the military, police and hospitals. The first BRIEFING bag was the Protection Tote, based on a military gun case.</p>
    <p><strong>Then the factory went to war.</strong> After September 11, 2001, BRIEFING says, its American factory switched entirely to military work and BRIEFING production stopped. It came back in 2003. Nakagawa set up Union Gate Group in 2011, and that group runs the brand today out of Tokyo.</p>
    <blockquote class="fb-pq">&ldquo;Paradoxically, Briefing&rsquo;s design concept is to escape from &lsquo;militaryism.&rsquo;&rdquo;<cite style="display:block;font-family:var(--mono);font-style:normal;font-size:10px;letter-spacing:.12em;text-transform:uppercase;margin-top:10px;opacity:.75">BRIEFING, About Us</cite></blockquote>
    <p><strong>The materials are the point.</strong> BRIEFING&rsquo;s main fabric is 1050-denier double-basketweave ballistic nylon, lined with 420-denier pack cloth, with YKK zippers and its red label tape on almost everything. The golf line, which it calls Urban Golf, adds Cordura in every weight, Cordura ripstop, and now Dyneema: the DL Series layers ECCO leather with Dyneema, which is why we put three of its covers in <a href="/drops/favorite-golf-fabrics-2026-cordura-dyneema-organic-cotton">our favorite fabrics of 2026</a>. For Fall/Winter 2025, BRIEFING restarted American production of golf pieces, in that 1050-denier ballistic nylon.</p>
    <p><strong>It collaborates like a golf brand.</strong> Pendleton&rsquo;s Harding pattern this fall, A.P.C. Golf in 2024, forged wedges with EPON, a carbon stand with shaft maker Graphite Design. The bags are numbered, CR-3 through CR-14, and the CR-4 is the flagship stand bag.</p>
    <p><strong>A note on prices.</strong> BRIEFING sells worldwide from its Tokyo store, priced in yen, and has no U.S. shops; its stores are in Japan, Taiwan and South Korea. We show yen with an approximate dollar figure. Read on November 25, 2026.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>1998</span></div>
      <div class="sidebar-detail"><span class="l">Founder</span><span>Yuji Nakagawa</span></div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Tokyo, Japan</span></div>
      <div class="sidebar-detail"><span class="l">Known for</span><span>Ballistic nylon, the CR caddie bags</span></div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>28</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>~$20&ndash;$815</span></div>
      <div class="sidebar-detail"><span class="l">Ships to</span><span>Worldwide from Tokyo</span></div>
      <a href="https://www.briefing-us.com/" class="sidebar-cta" target="_blank" rel="noopener">Visit BRIEFING &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#BRIEFINGGOLF</span>
        <span class="hashtag">#BallisticNylon</span>
        <span class="hashtag">#CaddieBag</span>
        <span class="hashtag">#Cordura</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

RELATED = [
 ("/drops/favorite-golf-fabrics-2026-cordura-dyneema-organic-cotton", "Our Favorite Fabrics of 2026", "Cordura, Dyneema and the BRIEFING DL Series, explained."),
 ("/drops/the-dyneema-edit", "The Dyneema Edit", "Everything we found in the fiber that floats."),
 ("/drops/brand-to-know-sentinel-golf", "Brand to Know: Sentinel Golf", "Another bag maker obsessed with materials."),
]


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    ids = [i for g in GROUPS for i in g[4]]
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC, "url": URL, "image": og,
         "datePublished": "2026-11-25", "dateModified": "2026-11-25",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington", "url": "https://thegrassyissue.com/about"},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": [
            {"@type": "ListItem", "position": n, "name": H.unescape(re.sub(r"<[^>]+>", "", f"{P[i][0]} {P[i][1]}")), "url": P[i][3]} for n, i in enumerate(ids, 1)]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Drops & Brands", "item": "https://thegrassyissue.com/#feed"},
            {"@type": "ListItem", "position": 3, "name": "Brand to Know: BRIEFING", "item": URL}]},
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
<link rel="canonical" href="{URL}" />
<link rel="preload" as="image" href="{IMG}/hero.jpg" />
{ld}"""


def main(apply_):
    ids = [i for g in GROUPS for i in g[4]]
    assert len(ids) == len(set(ids)) == 28, len(ids)
    for i in ids:
        assert i in P and i in FRAMES, i
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    head_rest = re.sub(r'<script type="application/ld\+json"[^>]*>.*?</script>\s*', "", head_rest, flags=re.S)
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    rel = "".join(f'<li style="padding:10px 0;border-bottom:.5px solid rgba(20,20,20,.2)"><a href="{u}">{t}</a> &mdash; {d_}</li>' for u, t, d_ in RELATED)
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Brand to Know</a><span>/</span>
  BRIEFING</div>

<header class="drop-header">
  <h1>{H1}</h1>
<!--TGI-BY--><p class="tgi-byline">By <a href="/about" rel="author">Lenny Harrington</a> &middot; Updated November 25, 2026</p><!--/TGI-BY-->
  <div class="drop-meta">
    <span>Tokyo, Japan &middot; since 1998</span><span class="dot"></span>
    <span>28 picks &middot; prices checked November 25, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Two black BRIEFING GOLF caddie bags and a cart tote in low light against a dark wall" fetchpriority="high" /></div></div>
"""
    body += TAKE
    C, T, HC, OC, AP = GROUPS
    body += band("a") + group(*C)
    body += pq("It&rsquo;s all about a solid, no-frills design combined with the functionality and durability that golf gear is known for.", "BRIEFING GOLF")
    body += band("b") + group(*T) + group(*HC) + group(*OC) + band("c") + group(*AP)
    body += f"""
<section class="products" style="padding-top:44px">
  <div class="writeup-body" style="max-width:720px;margin:0 auto">
    <div class="drop-tag grass">The Last Word</div>
    <h2 class="products-hdr" id="last-word">Built for the Trunk</h2>
    <p>Most golf bags are designed around the course. BRIEFING&rsquo;s are designed around everything else, too: the drive, the trunk, the airport, the walk from the car. If you&rsquo;re going to own one bag for a long time, a luggage brand that started in a military supplier&rsquo;s factory is a good place to look. If we got a detail wrong, <a href="/work-with-us">tell us</a>.</p>
    <div class="drop-tag grass" style="margin-top:34px">More Like This</div>
    <ul style="list-style:none;padding:0;margin:10px 0 0;font-size:17px">{rel}</ul>
  </div>
</section>
"""
    out = head_top() + head_rest.replace("</head>", CSS + "</head>", 1) + body + tail
    if not apply_:
        print("  dry run — pass --apply"); return
    o = ROOT / f"drops/{SLUG}.html"
    o.write_text(out, encoding="utf-8")
    fin = o.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", above)
    bad = []
    for w in ("worth", "genuinely", "honestly", "straightforward", "selling out", "Manors", "Sentinel Basecamp Dyneema duffles"):
        if re.search(rf"\b{w}\b", txt, re.I): bad.append("word " + w)
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if fin.count('class="product-card"') != 28: bad.append("card count")
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote drops/{SLUG}.html · 28 picks")


if __name__ == "__main__":
    main("--apply" in sys.argv)
