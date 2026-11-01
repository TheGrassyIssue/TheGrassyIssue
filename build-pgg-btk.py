#!/usr/bin/env python3
"""build-pgg-btk.py — Brand to Know: Paris Golf Gallery. 1 November 2026. Cloned from build-siegelman-revisit.py.
Lenny: "Let's do a brand to know - parisgolfgallery.com/collections/paris-golf-gallery" -> options sheet (26) -> "let's build the post".
No picks given: built from the in-stock own-label collection (store's 24 other brands left out). Val headcovers combined (two colorways);
Generation Mulligan vintage Greg Norman polo dropped to keep rows of 3. 24 cards.
FACTS: parisgolfgallery.com products.json + About page (USD via Shopify currency=USD, 1 Nov 2026); The Wedge (Shane Breslin, June 22 2025)
for history and quotes. No FAQ. Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Brand to Know: Paris Golf Gallery, the Showroom That Says Golf Is the New Skateboarding"
DESC = ("Paris Golf Gallery started as a Fashion Week showroom in Le Marais and now makes its own line: Golf Is the New Skateboarding tees, "
        "a supporter scarf, handmade ashtrays and caps with Paré, PXG and Odd Ritual. 24 picks in US dollars.")
H1 = "Brand to Know: Paris Golf Gallery"
BC = "Brand to Know: Paris Golf Gallery"
SLUG = "brand-to-know-paris-golf-gallery"
IMG = "/images/paris-golf-gallery"
SHOP = "https://www.parisgolfgallery.com/products/"
PG = "Paris Golf Gallery"
def X(b): return f"{b} x Paris Golf Gallery"
P = {
 "wash": (PG, "Golf Is the New Skateboarding Tee, Washed", "$65", "golf-is-the-new-skateboarding-vintage-cream-brown-regular-tee",
   "Our pick. The shirt that became the shop&rsquo;s calling card, back for winter in six washed colorways, from cream and brown to green and orange. Made in Portugal from 240-gram organic cotton, regular fit, no neck tag."),
 "classic": (PG, "Golf Is the New Skateboarding Tee, First Edition", "$65", "golf-is-the-new-skateboarding-blk-wht",
   "The original from the AW25 Fashion Week showroom: lighter 180-gram organic cotton, made in Portugal, in a relaxed boxy fit. Black with green or white with black."),
 "decks": (PG, "Golf Ball Skate Deck", "$171", "golf-is-the-new-skateboarding-orange-ball-deck",
   "A 7.825-inch skateboard deck in the bright orange and yellow of winter golf balls, made for the Fashion Week edition of the series. For the wall or for the street."),
 "gtees": (PG, "Golf Is the New Skateboarding Tees", "$14", "golf-is-the-new-skateboarding-tees",
   "A pouch of 25 wooden tees in a green-and-yellow marble pattern, printed with the slogan. The cheapest way into the shop."),
 "music": (PG, "Music Legends Tee", "$65", "golf-legends-t-shirt-wash",
   "A washed black tee with Kurt Cobain, Bob Marley and Paul Stanley drawn on a golf course, under the line &ldquo;The Game Remains, The Landscape Doesn&rsquo;t.&rdquo; Relaxed, slightly oversized fit."),
 "football": (PG, "Football Legends Tee", "$65", "football-legends-t-shirt-wash",
   "The same idea for football fans: Zidane, Ronaldo and Maradona on the course, in a vintage-style monochrome print on a black tee."),
 "qzipc": (PG, "Quarter Zip", "$92", "paris-golf-gallery",
   "From the Winter 2026 Fashion Week showroom: a fleece quarter zip with the logo on the chest and, on the back, a PGG flag over a cup that reads &ldquo;Fairway Research Center Inc.&rdquo; Burgundy or navy."),
 "mat": (PG + " x Wellputt", "Putting Mat", "$92", "golf-is-the-new-skateboarding-deck-2nd-generation-copy",
   "A 2.4-meter putting mat made with Wellputt, in brown or forest green, with both logos printed at the end. For the living room in the off-season."),
 "scarf": (PG, "Supporter Scarf", "$52", "paris-golf-gallery-scarf",
   "A football supporter&rsquo;s scarf, 140 by 20 centimeters, in a green-and-blue check with PARIS GOLF GALLERY knitted in. Made to be worn on the course or held up at the 18th."),
 "ashtray": (PG, "Golf Hole Ashtray", "$154", "paris-golf-gallery-ashtray",
   "One of 18 handmade ceramic ashtrays, each shaped like a different golf hole and made with a ceramic artist. No two are the same: one for every hole on the course."),
 "palo": (PG, "Palo Santo", "$14", "paris-golf-gallery-palo-santo",
   "Four sticks of palo santo wood from Ecuador, from naturally fallen trees, in a Paris Golf Gallery wrap. A small, strange and very Paris thing to sell in a golf shop."),
 "perfume": (PG + " x Nas Studio", "Skin Break Perfume", "$63", "nas-studio-x-paris-golf-gallery-skin-break-fragrance-01",
   "A leather scent made by perfumer Alexandra Mettetal, who based it on golf gloves, the quiet before a swing and the heat off a bunker. The most unusual piece in the collection."),
 "baggy": (X("Baggy Pants"), "Limited Edition Cap", "$46", "baggy-pants-limited-edition-paris-golf-gallery-cap",
   "A black cap made with Baggy Pants for the SS25 Fashion Week showroom, with BAGGY in PARIS embroidered on the front."),
 "lof": (X("Left of Field"), "Camo Cap", "$63", "left-of-field-x-paris-golf-gallery-limited-edition-cap",
   "A limited cap with Left of Field in a loud pink camo or a gray camo, with the Paris Golf Gallery logo on the front."),
 "pluto": (X("Pluto Golf"), "Technical Cap", "$57", "pluto-golf-x-paris-golf-gallery-limited-edition-cap",
   "A black ripstop cap with mesh side panels and white elastic cords wrapped around the sides, like outdoor gear. Built for the course and the city."),
 "odd": (X("Odd Ritual"), "SS27 Cap", "$57", "odd-ritual-x-paris-golf-gallery-ss27-cap",
   "A six-panel cotton twill cap with an off-white crown, a blue visor, a raised Odd Ritual Golf Club patch and gold embroidery for the collaboration on the side."),
 "pare": (X("Par&eacute;"), "Le Tour de Par&eacute; Cap", "$46", "pare-x-paris-golf-gallery-tour-de-pare-cap",
   "A cream cap that borrows from the Tour de France, with &ldquo;Le Tour de Par&eacute;&rdquo; embroidered in navy and orange and a flat visor."),
 "pxg": (X("PXG"), "Color Cap", "$46", "pxg-x-paris-golf-gallery-color-cap",
   "A structured PXG cap with raised logo embroidery and Paris Golf Gallery on the side. Yellow, black or white."),
 "vibe": (X("Vibe Caddy"), "Jersey", "$86", "vibe-caddy-x-paris-golf-gallery-jersey",
   "A burgundy football-style jersey made with Vibe Caddy for the SS25 Fashion Week showroom. For the range, the pub or both."),
 "brutta": (X("Brutta Golf"), "Limited Edition Polo", "$109", "brutta-x-paris-golf-gallery-limited-edition-polo",
   "A white polo with black panels across the shoulders, made with Brutta Golf. The most on-course piece here."),
 "hof": (X("House of Flavor"), "Long Sleeve", "$80", "house-of-flavor-x-paris-golf-gallery-limited-edition-t-shirt",
   "A long sleeve made by House of Flavor and Standard Issue for Paris Fashion Week, with BabyLoveBurger, as part of the #GOLFWITHFLAVOR project: food, art and golf in one busy graphic."),
 "lostballs": (X("Lost Balls"), "Anniversary Tee", "$56", "lost-balls-x-paris-golf-gallery-limited-edition-anniversary-t-shirt",
   "An anniversary tee made with Lost Balls to mark Paris Golf Gallery&rsquo;s first years, with a Paris-Tokyo graphic on the back. Gray or cream."),
 "val": (X("Val Golf"), "Thermo Headcover", "$114", "val-golf-x-paris-golf-gallery-thermo-green-headcover",
   "Knit headcovers made with Val Golf in what they call Thermo green and Thermo brown, with a blurred print that looks like a heat map."),
 "slice": (X("Slice Town"), "Butterfly Divot Tool", "$40", "slice-town-x-paris-golf-gallery-remove-pitch",
   "A divot tool that opens like a butterfly knife, made in a numbered run of 200 with Slice Town. A toy for the green that fixes pitch marks."),
}
SECTIONS = [
 ("Golf Is the New Skateboarding", "skate", ["wash", "classic", "decks", "gtees", "music", "football"],
  "<strong>Six pieces &middot; $14&ndash;$171</strong>The slogan that started on a tee at Fashion Week and now runs across shirts, decks and wooden tees."),
 ("The House Line", "house", ["qzipc", "scarf", "mat", "ashtray", "perfume", "palo"],
  "<strong>Six pieces &middot; $14&ndash;$154</strong>A quarter zip, a supporter scarf, a putting mat and the objects that make the shop feel like a gallery."),
 ("Collab Caps", "caps", ["pare", "odd", "pxg", "pluto", "lof", "baggy"],
  "<strong>Six pieces &middot; $46&ndash;$63</strong>Made with brands from the showroom, from Par&eacute; to PXG."),
 ("Collab Clothing and Gear", "collabs", ["brutta", "vibe", "hof", "lostballs", "val", "slice"],
  "<strong>Six pieces &middot; $40&ndash;$114</strong>More collaborations with brands that have shown at the gallery."),
]
N = 24
PQ = {
 "caps": ("It&rsquo;s not a trade show. It&rsquo;s not a pop-up store. It&rsquo;s not an art gallery, but it&rsquo;s everything at the same time.", "Pierre Greilsamer, to The Wedge, 2025"),
}
BANDS = {
 "house-after": ("In the Shop", "From Paris Golf Gallery&rsquo;s own photos.",
   [("band-1-1", "Bottles of Skin Break perfume lined up on a counter", "Skin Break"),
    ("band-1-2", "Handmade ceramic ashtrays shaped like golf holes on a table", "The ashtrays"),
    ("band-1-3", "Pouches of Golf Is the New Skateboarding tees flying against a blue sky", "The tees")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Paris Golf Gallery is a shop, a showroom and a small brand at once. Pierre Greilsamer and Malo Bourdet, who run the Paris branding agency WRKS, started it during Paris Fashion Week in June 2024 as a showroom in Le Marais with six golf brands under one roof. By June 2025 it had 25 brands in a 600-square-meter space in Cadillac&rsquo;s showroom at Op&eacute;ra, according to The Wedge, and it now sells many of them online, from Metalwood to Par&eacute;.</p>
    <p><strong>Its own line.</strong> This post covers the things Paris Golf Gallery makes itself. It started with one slogan on a tee, &ldquo;Golf is the new Skateboarding,&rdquo; and the line has grown from there into washed tees, skate decks, wooden tees, a quarter zip and a supporter scarf. Then come the objects you would not expect from a golf shop: 18 handmade ashtrays, each shaped like a golf hole, a leather perfume and palo santo.</p>
    <p><strong>The collabs.</strong> The other half of the line is caps and pieces made with brands that have shown at the gallery: Par&eacute;, Odd Ritual, PXG, Pluto, Left of Field, Brutta, House of Flavor, Lost Balls, Val Golf and Slice Town. It is the best record of who has passed through the room.</p>
    <p><strong>Buying from the US.</strong> The shop is in Paris, but the site shows prices in US dollars and ships to the US. Prices here were checked on November 1, 2026.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Details</div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>2024, Paris</span></div>
      <div class="sidebar-detail"><span class="l">Founders</span><span>Pierre Greilsamer, Malo Bourdet</span></div>
      <div class="sidebar-detail"><span class="l">Started as</span><span>Fashion Week showroom</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$14&ndash;$171</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Golf Is the New Skateboarding tee</span></div>
      <div class="hashtags">
        <span class="hashtag">#ParisGolfGallery</span>
        <span class="hashtag">#GolfIsTheNewSkateboarding</span>
        <span class="hashtag">#BrandToKnow</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
STORY = """
<section class="products" data-btk="story" style="margin-top:8px;padding-bottom:48px">
  <div class="drop-tag grass">The Story</div>
  <h2 class="products-hdr" id="story">From Skateboards to Fairways</h2>
  <div class="writeup-body">
    <p>Greilsamer and Bourdet came to golf from action sports. They had known each other for 15 years and worked in action sports marketing before starting WRKS, whose clients include Vans, Dickies and Wrangler. Golf found them during the 2020 lockdown, when, as Greilsamer told The Wedge, everything was closed, even surfing, but golf was still allowed.</p>
    <p>What hooked him was the feeling. &ldquo;If you do skateboarding, if you go snowboarding, you want to land the trick,&rdquo; he said. &ldquo;The feeling you get when you land the trick, it&rsquo;s almost exactly the same feeling you get when you hit a great golf shot.&rdquo;</p>
    <p>The gallery itself started with a favor. Captain&rsquo;s Helm Golf, the Japanese brand, asked them for help showing its collection during Fashion Week, and they saw that the new golf brands in Paris were all showing alone, in different places. &ldquo;What about gathering all of them under one roof to tell this story about this new golf lifestyle category?&rdquo; Bourdet remembered thinking. The first showroom in June 2024 had six brands. The online shop followed after the June 2025 edition.</p>
    <p>For more from brands in the room, read our <a href="/drops/brand-to-know-pare-golf">Brand to Know on Par&eacute;</a> and our <a href="/drops/brand-to-know-left-of-field-golf">Brand to Know on Left of Field</a>.</p>
  </div>
</section>
"""
FAQ = []
LOOKBOOK = ""
FRN = json.loads((ROOT / "research/pgg/frames.json").read_text())
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
         "url": URL, "image": og, "datePublished": "2026-11-01", "dateModified": "2026-11-01",
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
    <span>Brand to Know &middot; Paris, France &middot; Est. 2024</span><span class="dot"></span>
    <span>24 picks &middot; prices checked November 1, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A green pouch printed Golf is the new skateboarding lying in a pile of green and yellow wooden golf tees" fetchpriority="high" /></div></div>
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
