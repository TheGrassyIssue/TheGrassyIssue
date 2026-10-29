#!/usr/bin/env python3
"""build-golden-soul-btk.py — Brand to Know: Golden Soul Golf. 28 October 2026. Cloned from build-penta-btk.py.
Lenny: "Let's do a brand to know - goldensoulgolf.com" -> options -> "less bags and more headcovers" -> "let's build it with good lookbook and IRL images" (all 52 from options v2).
FACTS: goldensoulgolf.com About/Mission/Vision + product copy (research/golden-soul/catalogue.json, 28 Oct 2026, USD); Bisque Golf collection page. No founder is published: never name one.
OLD HEADER (Penta):
Lenny: "Let's do a brand to know - https://penta-golf.com/" -> options sheet -> "Lets build the post" (all 20: 14 in stock + 6 sold out).
FACTS: penta-golf.com About + live catalogue (research/penta/catalogue.json, USD, 28 Oct 2026); Monster Children Q&A (Feb 2024).
Founders stay unnamed (the brand never names them). Never "worth".
OLD HEADER (Paré):
Lenny: "Let's do a brand to know - https://pare.golf/collections/all" -> options sheet -> "I want a section about the sold out
stuff, especially the more colorful options and let's also mention that the logo is very similar to prada" + "I love the drawing
of the guy putting". Built from the starred picks + a Paré Boy section + a colorful sold-out section.
FACTS: research/pare/brief.md (about page, MyGolfSpy Aug 2025, Gordon College Jul 2025, Kollective Hustle Jul 2024),
research/pare/catalogue.json (pare.golf live, Oct 27 2026, USD). Home city is NOT published anywhere: never name one.
Left out: the in-stock HYPEGOLF tee with a Tagalog expletive in its name, and the Kapamilya-only (members) pieces.
The Prada point is our observation; the brand's own "The Devil Wears Paré" copy is what we cite. Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Brand to Know: Golden Soul Golf, Handmade Leather Headcovers From Colombia"
DESC = ("Golden Soul Golf makes leather, cowhide and wool headcovers by hand in Colombia, including fitted covers for LAB Golf "
        "putters. 52 pieces, from $90 alignment stick covers to woven Sunday bags, with prices.")
H1 = "Brand to Know: Golden Soul Golf, Handmade Headcovers From Colombia"
BC = "Brand to Know: Golden Soul Golf"
SLUG = "brand-to-know-golden-soul-golf"
IMG = "/images/golden-soul-golf"
SHOP = ""
C = "Golden Soul Golf"
SO = " &middot; sold out"
_OPT = json.loads((ROOT / "research/golden-soul/options.json").read_text())
COPY = {
 # fitted putter covers
 "beaumont-1": "Our pick. An OZ1 cover in red handwoven leather; the brand says each sheet takes nearly four hours to weave before it is cut. The most expensive putter cover here, and the best.",
 "martin-1": "A cowhide OZ1 cover in grey and brown. Golden Soul calls the cowhide OZ1 line back by popular demand, and every hide is different.",
 "macna-1": "The shaggiest cowhide of the bunch, long brown and white hair on the same OZ1 shape.",
 "eastwick-1": "Dark brindle cowhide with a tan leather lip. The quietest of the cowhide OZ1 covers.",
 "savile-center": "For LAB&rsquo;s DF3. Golden Soul says it made this line because customers kept asking for it. Brown herringbone with a tan leather trim.",
 "royal-center": "The same DF3 cover in a bright blue, the loudest color in the fitted line.",
 "bautista-center": "The DF3 cover in burgundy, trimmed in tan leather.",
 "fermin-center": "A grey-green wool DF3 cover, the one that goes with everything else in the bag.",
 "quincy-vzn": "From the first run of covers for LAB&rsquo;s newer VZN putter. Brown and white cowhide.",
 "otis-vzn": "The VZN cover in dark brindle cowhide.",
 "chigiana-zt": "Fitted to TaylorMade&rsquo;s Spider ZT, which Golden Soul says is hard to find a cover for. Black and white houndstooth.",
 "cassian-zt": "The Spider ZT cover in grey tweed with tan leather piping.",
 "wenworth-hs": "From the first run of covers for the OZ1 HS, made for right-handed putters only. Cream and tan cowhide.",
 "quincy-hs": "The OZ1 HS cover in black and white cowhide, the most classic hide in the store.",
 # blades
 "thatcher-putter": "Golden Soul photographs each cowhide cover on its own, so the one in the photos is the one you get. Grey and white hide on a blade cover.",
 "gaulle-putter": "A brown and white cowhide blade cover, also shot one by one.",
 "palette-no-5-putter": "The updated blade cover in a striped fabric the brand sources from Spain, with more padding and a magnetic closure.",
 "emerald-putter": "The same Spanish-fabric blade cover in a green and white weave.",
 "bamberg-putter": "Golden Soul&rsquo;s best-selling blade cover, updated, in a tan plaid. The cheapest putter cover in the post.",
 # mallets
 "brampton-mallet": "Navy handwoven leather on a mallet cover, from the same four-hours-a-sheet line as the red OZ1.",
 "lava-mallet": "A mallet cover in orange-rust leather, one of the brand&rsquo;s best-selling designs, rebuilt with new leathers.",
 "palette-no-5-mallet": "The Palette No. 5 stripe again, on the third generation of Golden Soul&rsquo;s mallet cover.",
 "la-meison": "A blue and white houndstooth mallet cover. It matches the La Meison driver further down.",
 "calder-mid-mallet": "For mid-mallets: a cream croc-textured leather cover with extra padding inside.",
 "levels-mid-mallet": "A woven red, orange and navy textile on the mid-mallet cover, the most colorful piece in the post.",
 "harrington-mid-mallet": "Distressed brown leather on a mid-mallet cover. It will look better in five years.",
 "leopold-mid-mallet": "A green plaid wool mid-mallet cover with tan leather trim.",
 # drivers
 "andes-driver": "From the wool collection: leather below, woolen fabric above, sourced from Peru, Scotland and Ireland. Andes is the pale grey.",
 "champs-2-driver": "The same driver cover in a grey and brown plaid.",
 "portlaoise-driver": "A dark green check over tan leather.",
 "la-meison-driver": "Blue and white houndstooth, the match for the La Meison mallet.",
 "royal-driver": "Bright blue wool over tan leather. It matches the Royal DF3 cover.",
 "roland-driver": "An oatmeal tweed, the most understated driver cover here.",
 # fairways + hybrids
 "tourmaline-fairway": "A fairway cover in a cream and tan textured wool over tan leather.",
 "chigiana-2-fairway": "Black and white houndstooth, the match for the Chigiana ZT putter cover.",
 "savile-fairway": "Brown herringbone, the match for the Savile DF3 cover.",
 "palomino-fairway": "A cream boucl&eacute; fairway cover, the softest-looking piece in the store.",
 "roland-fairway": "Oatmeal tweed, matching the Roland driver.",
 "coldwell-hybrid": "All-leather hybrid covers with stitching done entirely by hand. Coldwell is dark brown, and $120.",
 "radnor-hybrid": "Brown leather with a hand-stitched diamond pattern.",
 "balvene-hybrid": "The same hybrid cover with orange hand-stitched diamonds.",
 "batory-hybrid": "A navy leather hybrid cover, $120.",
 # barrels
 "amazonas": "Golden Soul&rsquo;s barrel covers use fabrics from Europe and handwoven textiles from Colombia, Mexico and Peru. Amazonas is a green-grey weave.",
 "palette-no-5": "The Palette No. 5 stripe on a barrel cover, so the set can match.",
 "sailor": "Red, white and navy stripes. The barrel cover for a summer bag.",
 "belinus": "A barrel cover in distressed brown leather instead of fabric, $130.",
 # bags + accessories
 "the-belmont-sunday": "An all-leather Sunday bag in tan, made with leather from Colombian tanneries, with double straps and a three-way divider. One in stock.",
 "the-monarch": "The all-leather Sunday bag in black with red trim, $1,000 less than the Belmont.",
 "barracks-7": "A seven-club leather carry bag with a cowhide pocket, built on the idea that less is more.",
 "rivelle-yardage": "A yardage book holder in black textured cow leather, lined inside with the brand&rsquo;s Woodford leather.",
 "monroe-finder": "A rangefinder cover in distressed brown leather, cushioned inside with a magnetic closure.",
 "otto-alignment": "A hand-stitched cream leather cover for alignment sticks, $90 and the cheapest piece here.",
}
P = {}
for _c in _OPT:
    P[_c["key"]] = (C, _c["t"], "${:,.0f}".format(_c["price"]), _c["url"], COPY[_c["key"]])
SECTIONS = [
 ("Fitted Putter Covers", "fitted", ["beaumont-1", "martin-1", "macna-1", "eastwick-1", "savile-center", "royal-center", "bautista-center", "fermin-center", "quincy-vzn", "otis-vzn", "wenworth-hs", "quincy-hs", "chigiana-zt", "cassian-zt"],
  "<strong>Fourteen covers &middot; $175&ndash;$275</strong>Covers cut for specific putters: LAB Golf&rsquo;s OZ1, DF3, VZN and OZ1 HS, and TaylorMade&rsquo;s Spider ZT. LAB covers are the deepest part of the store, with hundreds listed."),
 ("Blade Covers", "blades", ["thatcher-putter", "gaulle-putter", "palette-no-5-putter", "emerald-putter", "bamberg-putter"],
  "<strong>Five covers &middot; $150&ndash;$170</strong>Cowhide shot one by one, two Spanish fabrics and the best-selling plaid."),
 ("Mallet Covers", "mallets", ["brampton-mallet", "lava-mallet", "palette-no-5-mallet", "la-meison", "calder-mid-mallet", "levels-mid-mallet", "harrington-mid-mallet", "leopold-mid-mallet"],
  "<strong>Eight covers &middot; $160&ndash;$275</strong>Mallets and mid-mallets, from handwoven leather to an Andean-looking woven textile."),
 ("Drivers", "drivers", ["andes-driver", "champs-2-driver", "portlaoise-driver", "la-meison-driver", "royal-driver", "roland-driver"],
  "<strong>Six covers &middot; $175 each</strong>Leather below and woolen fabric from Peru, Scotland and Ireland above."),
 ("Fairways and Hybrids", "woods", ["tourmaline-fairway", "chigiana-2-fairway", "savile-fairway", "palomino-fairway", "roland-fairway", "coldwell-hybrid", "radnor-hybrid", "balvene-hybrid", "batory-hybrid"],
  "<strong>Nine covers &middot; $120&ndash;$160</strong>Wool fairway covers that match the drivers and putter covers, and all-leather hybrid covers stitched by hand."),
 ("Barrel Covers", "barrels", ["amazonas", "palette-no-5", "sailor", "belinus"],
  "<strong>Four covers &middot; $110&ndash;$130</strong>The round, old-school shape, in woven fabrics and one in leather."),
 ("A Few Bags and Accessories", "bags", ["the-belmont-sunday", "the-monarch", "barracks-7", "rivelle-yardage", "monroe-finder", "otto-alignment"],
  "<strong>Six pieces &middot; $90&ndash;$2,700</strong>Golden Soul also makes leather Sunday bags, a seven-club carry bag and small leather goods. A short sample of the rest of the store."),
]
N = 52
PQ = {
 "mallets": ("Each sheet of handwoven leather requires nearly four hours of work before the manufacturing process even begins.", "Golden Soul Golf, on its handwoven covers"),
 "drivers": ("We hand select every piece of naked leather from the best tanneries in South America and Europe.", "Golden Soul Golf"),
}
BANDS = {
 "fitted": ("The workshop", "Golden Soul makes everything in Colombia. From its own photos of the work: patterns, machines and a lot of hand stitching.",
   [("look-02", "Hands drawing a circle pattern with a compass on paper", "Drawing the pattern"),
    ("look-03", "A craftsman sewing leather on an industrial sewing machine", "At the machine"),
    ("look-34", "Close-up of hands hand-stitching a leather headcover", "Stitched by hand"),
    ("look-35", "Hands working a strip of leather on a workbench", "Leather on the bench"),
    ("look-32", "A craftsman sewing at a machine in a bright workshop", "In the workshop"),
    ("look-26", "A man working at a wooden loom", "At the loom")]),
 "drivers": ("Out on the course", "Golden Soul shoots its covers and bags where they get used.",
   [("look-19", "A golfer carrying a cowhide and leather carry bag through trees", "A cowhide carry bag"),
    ("look-22", "Two golfers walking down a sandy fairway carrying bags", "Walking the course"),
    ("look-23", "A golfer holding the flag on a green with hills behind, in black and white", "At the flag"),
    ("look-25", "Golfers far down a tree-lined fairway", "Down the fairway"),
    ("look-27", "A golfer pulling clubs with striped and leather headcovers from a white bag", "The covers in the bag"),
    ("look-20", "Golfers putting on a green in black and white", "On the green")]),
 "bags": ("The hides", "Cowhide is a Golden Soul signature, and the brand says it pioneered genuine cowhide headcovers.",
   [("look-36", "Black and white cows grazing in a green field", "Where the hides come from"),
    ("look-40", "A stack of brown and white cowhide headcovers", "A pile of cowhide covers"),
    ("look-31", "Close-up of a woven Sunday bag with leather straps and trim", "A woven Sunday bag")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Golden Soul Golf makes headcovers the way most brands make wallets: by hand, in leather, one at a time. Everything is made in Colombia, and the brand says it hand-selects its leather from tanneries in South America and Europe. The result is a store with more than 1,500 listings, most of them one of a kind, because no two hides, weaves or tweeds come out the same.</p>
    <p><strong>The fitted covers.</strong> The reason to know Golden Soul is its putter covers cut for specific putters. LAB Golf&rsquo;s OZ1 and DF3 have shapes that standard mallet covers fit badly, and Golden Soul has hundreds of covers for them, plus new lines for LAB&rsquo;s VZN and OZ1 HS and for TaylorMade&rsquo;s Spider ZT. If you&rsquo;ve bought a LAB putter and hated every cover since, start here.</p>
    <p><strong>The materials.</strong> Cowhide, which the brand says it pioneered on headcovers and photographs one piece at a time, so the cover you see is the cover you get. Wool from Peru, Scotland and Ireland on the drivers and fairways. Striped fabric from Spain. Handwoven leather that takes nearly four hours a sheet before anyone cuts it. Many designs share a name across driver, fairway and putter covers, so a set can match.</p>
    <p><strong>The bags.</strong> Golden Soul also makes all-leather Sunday bags from $1,700, seven-club carry bags at $750, and four woven Sunday bags at $6,500 made with wool the brand says is hand-woven by artisans in Boyac&aacute;, Colombia. We kept this post to the headcovers, with a short sample of the rest at the end.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">At a Glance</div>
      <div class="sidebar-detail"><span class="l">Made in</span><span>Colombia</span></div>
      <div class="sidebar-detail"><span class="l">Known for</span><span>Leather and cowhide headcovers</span></div>
      <div class="sidebar-detail"><span class="l">Fits</span><span>LAB OZ1, DF3, VZN, OZ1 HS; Spider ZT</span></div>
      <div class="sidebar-detail"><span class="l">Listings</span><span>1,567 (961 in stock)</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$90&ndash;$2,700</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Beaumont 1 OZ1 cover</span></div>
      <div class="hashtags">
        <span class="hashtag">#GoldenSoulGolf</span>
        <span class="hashtag">#Headcovers</span>
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
  <h2 class="products-hdr" id="story">Made by Hand in Colombia</h2>
  <div class="writeup-body">
    <p>Golden Soul keeps its own story short. Its About page says the brand offers &ldquo;the most stylish golf accessories created with the finest materials from all over the world,&rdquo; that its leather comes from tanneries in South America and Europe, and that everything is &ldquo;proudly made in Colombia&rdquo; by craftsmen and designers working together. It doesn&rsquo;t name a founder, so neither do we.</p>
    <p>Its mission is &ldquo;designing functional and stylish golf accessories&rdquo; through craftsmanship, attention to detail and &ldquo;innovative textiles.&rdquo; Its stated vision goes further than the product: creating jobs in the communities where it works, supporting players, tournaments and professional leagues, and partnering with charities.</p>
    <p>The product pages tell the rest. The DF3 cover, the brand says, came from customers asking for it &ldquo;not once, but many times over.&rdquo; The Spider ZT line exists because finding a cover that fits a modern putter &ldquo;has become increasingly rare.&rdquo; The woven Sunday bags were made with artisans from the highlands of Boyac&aacute;, known for a centuries-old wool-working tradition.</p>
    <p>You can also find Golden Soul outside its own store. Bisque Golf in Amsterdam stocks a selection and describes every piece as handmade and unique, and some covers have been listed at Dick&rsquo;s Sporting Goods. Golden Soul ships free in the US on orders over $250.</p>
  </div>
</section>
"""
FAQ = [
 ("Where is Golden Soul Golf made?", "In Colombia. The brand says every piece is handmade there, with leather hand-selected from tanneries in South America and Europe."),
 ("Does Golden Soul Golf make covers for LAB Golf putters?", "Yes. It makes fitted covers for LAB Golf's OZ1, DF3, VZN and OZ1 HS, hundreds in all, most priced at $175. It also makes covers for TaylorMade's Spider ZT."),
 ("Are Golden Soul cowhide headcovers one of a kind?", "Yes. Each cowhide cover is photographed individually, so the cover in the photos is the one you receive, and no two hides match."),
 ("How much are Golden Soul Golf headcovers?", "On October 28, 2026, putter covers ran $150 to $275, driver covers $175, fairway covers $160, hybrid covers $120 to $150 and barrel covers $110 to $130."),
 ("Does Golden Soul Golf make golf bags?", "Yes: all-leather Sunday bags from $1,700, seven-club carry bags at $750, and woven Sunday bags at $6,500 made with hand-woven wool from Boyaca, Colombia."),
]
LOOKBOOK = ""
FRN = json.loads((ROOT / "research/golden-soul/frames.json").read_text())
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
         "url": URL, "image": og, "datePublished": "2026-10-28", "dateModified": "2026-10-28",
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
    <span>Brand to Know &middot; Made in Colombia</span><span class="dot"></span>
    <span>52 pieces &middot; checked October 28, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A golfer mid-swing on an open course under a big sky, in black and white, from Golden Soul Golf"" fetchpriority="high" /></div></div>
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
