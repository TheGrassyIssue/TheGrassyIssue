#!/usr/bin/env python3
"""build-siegelman-revisit.py — Brand Revisited: Siegelman Stable. 31 October 2026. Cloned from build-beams-revisit.py.
Lenny: "let's do a brand revisited Siegelman stables" -> options sheet (55) -> "let's pick more golf friendly items and some of the collabs".
27 cards: Maxfli + Harness golf pieces (9), fall layers that work on a course (9), collabs (6), hats + belt (3).
FACTS: siegelmanstable.com products.json (USD, in stock, read 31 Oct 2026); GOLF.com June 16 2026 (Max caddied five years; press-release quote);
amNY Aug 4 2026 (Yankees 13-piece capsule, CC Sabathia, Lenny Santiago, Shaw Pecas, Brunson hats, Max quote); Roastbrief July 7 2026 (Bazooka capsule,
gum-pocket cap, look-alike contest July 9). Prince caps/tees: SU25 originals, back on the site Oct 8 2026. No FAQ. Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Siegelman Stable Revisited: Maxfli, the Yankees and 33 Golf-Ready Picks"
DESC = ("Back to Siegelman Stable: what is left of the Maxfli golf capsule, a Yankees collection with CC Sabathia, Prince caps, "
        "fall knits and hoodies for a cold course and 33 picks with US prices.")
H1 = "Brand Revisited: Siegelman Stable"
BC = "Brand Revisited: Siegelman Stable"
SLUG = "brand-revisited-siegelman-stable"
IMG = "/images/siegelman-stable-revisit"
SHOP = "https://siegelmanstable.com/products/"
SS = "Siegelman Stable"
MX = "Siegelman Stable x Maxfli"
P = {
 "0": (MX, "Golf Polo", "$158", "maxfli-golf-polo",
   "Our pick. A light gray polo with a green collar and the Maxfli and stable logos at the chest, in a 10-ounce organic cotton jersey that is heavier than most golf polos. Unisex fit, true to size."),
 "1": (MX, "Pullover Jacket", "$298", "retro-track-jacket-2",
   "The statement piece from &ldquo;Harness the Drive&rdquo;: charcoal and green tech poplin lined in athletic mesh, with zip pockets, hidden inner pockets and elastic cuffs. It is the jacket on the course in the campaign photos."),
 "5": (SS, "Racing Stable Track Shorts", "$132", "racing-stable-track-shorts-1",
   "Tech poplin shorts lined in mesh, with an elastic waist, a drawcord and the stable logo on the left thigh. The most on-course piece in the shop. Green or gray."),
 "6": (MX, "Five-Panel Hat", "$78", "siegelman-stable-hat-84",
   "A structured two-tone cap in charcoal and green cotton chino twill, made in the USA, with the horse-and-sulky logo up front."),
 "7": (MX, "Dad Hat", "$76", "siegelman-stable-dad-hat-12",
   "The unstructured six-panel version in pale gray and kelly green, also made in the USA. The softer of the two Maxfli caps."),
 "8": (MX, "Golf Tote", "$48", "golf-tote",
   "A heavyweight canvas tote in off-white with green straps and a reinforced base, with both logos printed on the front. Shoes, a towel and a sleeve of balls fit with room to spare."),
 "9": (SS, "Rib Zip Up Cardigan", "$378", "rib-zip-up-cardigan-2",
   "New for fall: a ribbed cotton cardigan with a two-way zip and an embroidered logo. Relaxed enough to layer over a polo on a cold first tee. Cobalt or black."),
 "10": (SS, "Cable Knit Sweater", "$278", "cable-knit-sweater-1",
   "A classic cotton cable knit with a small white logo on the chest and a slim shape, from the October 13 drop. Size up if you want room to swing. Black or gray."),
 "11": (SS, "Logo Knit", "$282", "siegelman-stable-logo-knit-5",
   "A loose tricot knit with the horse and sulky across the chest, in cotton with a little recycled polyester. Seven colors, from light blue to coal."),
 "12": (SS, "Henley Sweatshirt", "$252", "henley-sweatshirt-1",
   "An oversized cotton henley with ribbed collar, cuffs and hem and a stable badge on the chest. The ochre one is the color of the October 27 drop. Also in cobalt."),
 "13": (SS, "Racing Stable Crewneck", "$198", "racing-stable-crewneck-sweatshirt",
   "Heavyweight organic cotton fleece with Siegelman Racing Stable across the chest, from the cobalt set that landed September 22. Also gray, white and navy."),
 "14": (SS, "Track Jacket", "$348", "track-jacket",
   "Black with white panels across the shoulders and sleeves, outlined in gold piping, with the horse logo on the chest. It is oversized, with a gathered hem, and it matches the Track Pant."),
 "15": (SS, "Mock Neck Sherpa Jacket", "$468", "mock-neck-sherpa-jacket-1",
   "A zip-front sherpa made in Los Angeles with an embroidered leather patch on the back. For the coldest morning tee time of the year. Gray or navy."),
 "16": (SS, "Pleated Pant", "$212", "pleated-pant-2",
   "A straight-leg pleated trouser made in Los Angeles, with a woven stable patch on the back pocket. In black, navy or red."),
 "18": ("Siegelman Stable x Prince", "Five-Panel Hat", "$78", "siegelman-stable-x-prince-tennis-hat",
   "A pro-style cap with the Prince ribbon above the stable logo and a small tennis racket on the side. Navy with a green brim, or white with green."),
 "19": ("Siegelman Stable x Prince", "Six-Panel Hat", "$78", "siegelman-stable-x-prince-tennis-dad-hat",
   "The six-panel version, in white with a navy ribbon or a bright tennis-ball green with a red horse and sulky."),
 "20": ("Siegelman Stable x Prince", "Boxy Tee", "$98", "prince-tennis-crop-tee-1",
   "A 13-ounce cotton jersey tee made in Los Angeles, with the Prince ribbon graphic. Hunter green or white."),
 "21": ("Siegelman Stable x New York Yankees", "Coaches Jacket", "$548", "new-york-yankees-coaches-jacket",
   "The top piece of the Yankees collection: heavy cotton twill lined in Bemberg, with a Yankees logo on the chest, the full stable artwork across the back and silver snaps and collar tips."),
 "22": ("Siegelman Stable x Yankees x New Era", "59FIFTY A-Frame Fitted", "$86", "siegelman-stable-x-new-york-yankees-x-new-era-59fifty-a-frame-fitted-cap",
   "A gray New Era fitted with the interlocking NY in navy, Siegelman Stable on one side and the Racing Stable logo at the back."),
 "23": ("Siegelman Stable x Mets x New Era", "9FORTY A-Frame Snapback", "$76", "siegelman-stable-hat-68",
   "The July Mets cap, with the Mets logo between two blue horse-and-sulky logos on black, or the stable script in orange on white or blue."),
 "24": (SS, "Canvas Dad Hat", "$76&ndash;$82", "siegelman-stable-canvas-dad-hat-4",
   "An unstructured six-panel in washed cotton canvas, made in the USA, with a buckle back. The wash makes every one a little different. Four colors."),
 "25": (SS, "Corduroy Hat", "$88", "copy-of-beige-corduroy-siegelman-stable-hat",
   "Black corduroy with the logo in wheat gold, made in the USA. A fall cap that goes with every knit above."),
 "26": (SS, "Oval Belt", "$288&ndash;$298", "oval-belt",
   "A suede belt with an engraved oval buckle in antique nickel and a metal name plate, made in New York. Beige or black."),
 "27": (SS, "Track Pant", "$328", "track-pant",
   "The other half of the October 27 track set: a wide-leg pant with white side panels edged in gold piping and a drawstring waist. Wear it with the Track Jacket or on its own."),
 "28": (SS, "Embroidered Hoodie", "$248", "embroidered-hoodie-1",
   "A relaxed cotton fleece hoodie with the stable logo embroidered small on the chest, front pockets and a banded hem. The quiet one. Gray, navy, white or black."),
 "29": (SS, "Racing Stable Hoodie", "$248", "racing-stable-hoodie-2",
   "Organic cotton fleece, garment-washed, with SIEGELMAN arched across the chest and the Racing Stable logo on the back. Boxy and a little cropped. Five colors, including the fall cobalt."),
 "30": (SS, "Emblem Oversized Zip Hoodie", "$248", "oversize-zip-hoodie",
   "A 22-ounce cotton fleece zip-up made in Los Angeles, washed so it looks lived-in, with distressed Siegelman Stable lettering across the chest. Black, green or blue."),
 "31": (SS, "NYC Racing Stable Zip Hoodie", "$248", "nyc-racing-stable-zip-hoodie",
   "An oversized navy zip-up in 22-ounce fleece, made in Los Angeles, with a small Racing Stable crest on the chest and the horse and sulky across the back."),
 "32": ("Siegelman Stable x Indy 500", "Graphic Hoodie", "$212", "seieglman-stable-graphic-hoodie",
   "From the Indianapolis 500 collaboration: a heavy 24-ounce white hoodie, made in Los Angeles, with a red Indy 500 graphic front and back."),
 "33": (SS, "Chicago Racing Stable Zip Hoodie", "$248", "chicago-racing-stable-zip-hoodie",
   "A heather gray zip-up from July with a Chicago Racing Stable logo on the chest and the horse logo across the back. Oversized, 22-ounce fleece."),
 "34": ("Siegelman Stable x New York Yankees", "Zip Hoodie", "$248", "new-york-yankees-zip-hoodie",
   "Navy 22-ounce fleece with a Yankees logo on the chest and NEW YORK over the horse and sulky across the back. The hoodie from the campaign photos."),
 "35": ("Siegelman Stable x New York Yankees", "Hoodie", "$248", "new-york-yankees-hoodie",
   "An oversized pullover in pale gray with a small navy Yankees logo on the chest."),
 "36": ("Siegelman Stable x New York Mets", "Hoodie", "$248", "new-york-mets-hoodie",
   "Black fleece with New York written across the chest in Mets script, from the July collection. Oversized."),
}
SECTIONS = [
 ("Golf: Harness the Drive", "golf", ["0", "1", "5", "6", "7", "8"],
  "<strong>Six pieces &middot; $48&ndash;$298</strong>What is still in stock from the Maxfli capsule, plus the shorts we would wear on the course."),
 ("Fall Layers for a Cold Round", "layers", ["9", "10", "11", "12", "13", "15", "14", "27", "16"],
  "<strong>Nine pieces &middot; $198&ndash;$468</strong>From the fall drops of September and October, and a pair of trousers that sit right over a golf shoe."),
 ("Hoodies", "hoodies", ["29", "28", "30", "31", "33", "32"],
  "<strong>Six pieces &middot; $212&ndash;$248</strong>For the range, the cart and the ride home. Most are heavy 22-ounce fleece."),
 ("The Collabs: Yankees, Mets and Prince", "collabs", ["34", "35", "21", "22", "36", "23", "18", "19", "20"],
  "<strong>Nine pieces &middot; $76&ndash;$548</strong>The Yankees collection from August, the Mets pieces from July and the Prince caps and tees, back since October 8."),
 ("Hats and a Belt", "hats", ["24", "25", "26"],
  "<strong>Three pieces &middot; $76&ndash;$298</strong>Two everyday caps and a belt to finish the look."),
]
N = 33
PQ = {
 "layers": ("Golf has always had a strong sense of tradition, and this collection gave us the opportunity to reinterpret that through our signature Siegelman Stable designs.", "Max Siegelman, on the Maxfli collection, June 2026"),
}
BANDS = {
 "golf-after": ("Harness the Drive", "From Siegelman Stable&rsquo;s Maxfli campaign.",
   [("band-1-1", "A Maxfli pullover jacket and cap left on a wooden bench beside a bucket of golf balls", "Between nines"),
    ("band-1-2", "A golfer in a white Siegelman Stable cap and green-and-charcoal Maxfli jacket at the top of his swing", "The pullover jacket"),
    ("band-1-3", "A golfer in a charcoal and green Maxfli cap lying on the green to line up a putt", "Reading the line")]),
 "collabs-after": ("The Yankees Collection", "From the August campaign, which features former Yankees pitcher CC Sabathia.",
   [("band-2-1", "A man in a navy New York hoodie and white Yankees cap, seen from behind", "The zip hoodie"),
    ("band-2-2", "A man holding a bat across his shoulders, showing the Siegelman Stable artwork on the back of a navy coaches jacket", "The coaches jacket"),
    ("band-2-3", "A man in the navy Yankees coaches jacket and shorts sitting on a stool with a bat", "Jacket and shorts")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>We wrote about Siegelman Stable in July, a few weeks after its Maxfli golf collection came out for the U.S. Open at Shinnecock Hills. Since then, the brand that Max Siegelman built on his family&rsquo;s harness racing stable has had its busiest stretch yet: a Mets cap with New Era in July, a Bazooka gum capsule with a cap that has a pocket for exactly one piece of gum, and in August a 13-piece New York Yankees collection.</p>
    <p><strong>The Yankees.</strong> The Yankees collection went live on August 4 online and at Yankee Stadium, with headwear, jackets, shorts, sweatshirts and tees, and New Era caps. Former Yankees pitcher CC Sabathia is in the campaign. amNY noted the brand&rsquo;s profile rose this year when Knicks guard Jalen Brunson kept wearing its hats in interviews. Max told amNY the collection is about &ldquo;honoring tradition while creating pieces that feel timeless.&rdquo;</p>
    <p><strong>The golf is still here.</strong> Most of the Maxfli capsule is still in stock: the heavyweight polo, the pullover jacket, both caps and the tote. Add the mesh-lined track shorts and you have a full outfit for a warm round. Max&rsquo;s first job was caddying, for five years, and it shows in how much of this works on a course.</p>
    <p><strong>Fall/Winter &rsquo;26.</strong> The fall line has come in drops: a cobalt Racing Stable set on September 22, cotton cable knits and a ribbed zip cardigan on October 13, and a black-and-ochre track set on October 27. For a cold round, the knits, the sherpa and the hoodies are the ones we would reach for. The Prince Tennis caps and tees, first made in 2025, came back on October 8.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">What&rsquo;s New</div>
      <div class="sidebar-detail"><span class="l">Golf</span><span>Maxfli, June</span></div>
      <div class="sidebar-detail"><span class="l">Mets</span><span>July</span></div>
      <div class="sidebar-detail"><span class="l">Yankees</span><span>August 4</span></div>
      <div class="sidebar-detail"><span class="l">Fall drops</span><span>Sept 22 &ndash; Oct 27</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$48&ndash;$548</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Maxfli Golf Polo</span></div>
      <div class="hashtags">
        <span class="hashtag">#SiegelmanStable</span>
        <span class="hashtag">#HarnessTheDrive</span>
        <span class="hashtag">#BrandRevisited</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
STORY = """
<section class="products" data-btk="story" style="margin-top:8px;padding-bottom:48px">
  <div class="drop-tag grass">The Story</div>
  <h2 class="products-hdr" id="story">From the Stable to the Stadium</h2>
  <div class="writeup-body">
    <p>Max Siegelman&rsquo;s father, Robbie, founded Siegelman Racing Stable in 1982 and trained harness racehorses for decades. In 2020, with $600, Max printed hats with the family&rsquo;s horse-and-sulky logo and sent them to the NBA bubble. The logo on every piece in this post is the stable&rsquo;s own.</p>
    <p>Six years on, the brand has worked with the Knicks, Mets, Yankees, Rangers, Prince, Ford and the Indy 500, and golf has become part of it. &ldquo;Together with Maxfli, we wanted to create something that feels rooted in the game, but also expressive, unexpected and true to how people are engaging with golf today,&rdquo; Max said when the collection launched in June.</p>
    <p>A portion of proceeds still goes to equine therapy, the work Robbie started decades ago.</p>
    <p>For the full story, read our <a href="/drops/brand-to-know-siegelman-stable">Brand to Know on Siegelman Stable</a> and our <a href="/drops/maxfli-siegelman-stable-harness-the-drive">post on the Maxfli drop</a>.</p>
  </div>
</section>
"""
FAQ = []
LOOKBOOK = ""
FRN = json.loads((ROOT / "research/siegelman-revisit/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-R3-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-10-31", "dateModified": "2026-10-31",
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
    <span>Brand Revisited &middot; New York &middot; Est. 2020</span><span class="dot"></span>
    <span>33 picks &middot; prices checked October 31, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Two golfers in Siegelman Stable x Maxfli jackets and two caddies in Maxfli bibs walking off a green, from the Harness the Drive campaign" fetchpriority="high" /></div></div>
"""
    body += TAKE  # Lenny 28 Oct: the story closes the post in place of The Questions
    n = 1
    for s in SECTIONS:
        if s[1] + "-before" in BANDS: body += band(s[1] + "-before")
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
        if s[1] + "-after" in BANDS: body += band(s[1] + "-after")
    body += STORY
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    if fin.count('class="product-card"') != N: bad.append("card count")
    if re.search(r"\bworth\b", re.sub(r"\bFort\s+Worth\b", " ", re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<script\b.*?</script>", " ", above))), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
