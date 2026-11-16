#!/usr/bin/env python3
"""build-dune-golf.py — Dune x Golf: the characters of Dune: Part Three on a golf course. 16 November 2026.
Lenny: "Dune & Golf crossover" -> characters from the new film -> more accessories -> "build the post and I'll pull the images".
CHARACTER IMAGES: each section has a slot at images/dune-golf/char-<key>.jpg. Lenny is adding his own cleared stills
there himself; until he does, the slot holds a brand campaign stand-in. Do not fetch film stills or cast photos.
FACTS: characters per the announced cast (Tatler Asia guide, 10 Nov 2026); US release December 18, 2026.
No quotes from the book or the films. Prices/stock read from each store 16 Nov 2026 (Shopify .js).
Clamp sells in GBP (0.752). Men's products only. No FAQ. Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"
TITLE = "Dune x Golf: What the Characters of Dune: Part Three Would Wear on the Course"
DESC = ("Dune: Part Three opens December 18. What Emperor Paul, Hayt, Scytale, Stilgar, Gurney and Farok would wear "
        "and carry on a golf course: 42 pieces from independent golf brands, plus a bag for the spice.")
H1 = "Dune &times; Golf"
BC = "Dune &times; Golf"
SLUG = "dune-part-three-golf"
IMG = "/images/dune-golf"
DATE = "2026-11-16"

# key: (brand, item, price, url, copy)
P = {
 "d00": ("VESSEL", "Sunday IV Croc Black Leather Stand", "$999", "https://vesselgolf.com/products/sunday-iv-leather-stand-croc-black",
   "Croc-embossed black leather. An emperor doesn&rsquo;t carry his own bag, but if he did."),
 "d01": ("Oakley &times; Metalwood", "UV Top", "$120", "https://metalwood.studio/products/oakley-metalwood-uv-top-white",
   "A long-sleeve UV top. The closest thing in golf to a stillsuit."),
 "d02": ("Mantra Golf", "Signature Mock Neck L/S, Desert Sage", "$98", "https://mantragolf.com/products/signature-mock-neck-ls-desert-sage",
   "A Pima cotton mock in Desert Sage, for the desert he came from."),
 "d03": ("Pins &amp; Aces", "Royal Collection &rsquo;26 Headcover Set", "$121.98, was $164.85", "https://pinsandaces.com/products/royal-collection-26-headcover-set",
   "Crowns, crests and a little excess. Fit for the throne."),
 "d04": ("Par&eacute;", "Par&eacute; &times; Imperial Manila Hat, Black", "$55", "https://pare.golf/products/pare-x-imperial-manila-hat-black",
   "It says Imperial on the label."),
 "d05": ("Seamus Golf", "Torch Flask, Onyx and Gold", "$140", "https://seamusgolf.com/products/torch-flask-onyx-and-gold-goat-logo",
   "Onyx and gold, for the throne room."),
 "d06": ("Oakley &times; Metalwood", "Scar Sunglasses, Dark Grey", "$224", "https://metalwood.studio/products/oakley-metalwood-scar-sunglasses-dark-grey",
   "For a man with mechanical eyes."),
 "d07": ("Malbon Golf", "Division Blade Cover", "$108", "https://malbon.com/products/division-blade-cover-black-stone-washed-denim",
   "A blade putter cover for a swordmaster."),
 "d08": ("Kraken Golf", "Production Shears Pitch Tool, Stainless", "$149", "https://www.krakengolf.com/products/production-shears-stainless-steel-pitch-tool",
   "A stainless pitch tool built like a precision instrument. Tleilaxu-grade engineering."),
 "d09": ("Kraken Golf", "Here Be Titanium Puzzle Ball Marker", "$99", "https://www.krakengolf.com/products/here-be-titanium-puzzle-ball-marker",
   "A titanium puzzle-piece marker, for a man assembled from parts."),
 "d10": ("Whim Golf", "Steel Ball Mark Repair Tool", "$30", "https://whimgolf.com/products/steel-ball-mark-repair-tool",
   "Simple, steel and sharp."),
 "d11": ("Oakley &times; Metalwood", "Icon Jacket, Pitch Black", "$240", "https://metalwood.studio/products/oakley-metalwood-icon-jacket-pitch-black",
   "Pitch black, for a man grown in a tank."),
 "d12": ("Gramicci &times; thisisneverthat", "Reversible Fleece Vest", "$170", "https://www.gramicci.com/products/tnt-gramicci-reversible-fleece-vest",
   "One face out, one face in."),
 "d13": ("Malbon Golf", "Grounds Reversible Jacket", "$348", "https://malbon.com/products/grounds-reversible-jacket-brown",
   "Brown one way, something else the other."),
 "d14": ("Metalwood Studio", "Dual Face T-Shirt", "$138", "https://metalwood.studio/products/dual-face-t-shirt-bone",
   "A Dual Face tee. On the nose."),
 "d15": ("Oakley &times; Metalwood", "Reversible Beanie", "$60", "https://metalwood.studio/products/oakley-metalwood-reversible-beanie-pitch-black",
   "For a quick change between holes."),
 "d16": ("Palm Golf Co.", "Swing and Smile Hybrid Headcover", "$79.99", "https://palmgolfco.com/products/rhythm-tan-hybrid-headcover",
   "It says Swing and Smile. Whose smile, though?"),
 "d17": ("Pins &amp; Aces", "Anthracite Reversible Woven Belt", "$39.96, was $49.95", "https://pinsandaces.com/products/anthracite-reversible-woven-belt",
   "Two faces, one waist."),
 "d18": ("VESSEL &times; MiiR", "Vacuum Insulated Bottle", "$39", "https://vesselgolf.com/products/vessel-x-miir-vacuum-insulated-bottle",
   "Water discipline, insulated."),
 "d19": ("Devereux Golf", "Nomad Polo, Brindle", "$74", "https://devereuxgolf.com/products/nomad-polo-brindle",
   "A polo called Nomad, in brindle."),
 "d20": ("Devereux Golf", "Daily Hoodie, Desert Drift", "$118", "https://devereuxgolf.com/products/daily-hoodie-desert-drift",
   "Desert Drift: the color of a sietch at dusk."),
 "d21": ("Dormie Workshop", "Barrel Headcover, Dunes", "$165", "https://dormieworkshop.com/products/dormie-barrel-dunes",
   "Dormie&rsquo;s leather barrel cover, in a colorway called Dunes."),
 "d22": ("Pins &amp; Aces", "Cactus Ball Marker", "$11.96, was $14.95", "https://pinsandaces.com/products/cactus-ball-marker-1",
   "A cactus marker for a desert man."),
 "d23": ("Lazyface", "The Chenille Sun Cap", "$48", "https://lazyface.com/products/the-chenille-sun-cap",
   "A soft cap for a hard sun."),
 "d24": ("Students Golf", "Caprock Knit Zip Sweater", "$188", "https://studentsgolf.com/products/caprock-knit-zip-sweater",
   "A rugged knit zip for a man who sings between battles."),
 "d25": ("Gramicci", "Big Wale Carpenter Pant", "$140", "https://www.gramicci.com/products/big-wale-carpenter-pant",
   "Big wale cord carpenter pants. Workwear for a soldier-poet."),
 "d26": ("Seamus Golf", "USA Wool Driver Cover, Navy", "$140", "https://seamusgolf.com/products/usa-wool-driver-head-cover-navy",
   "USA-made wool, built to take a beating."),
 "d27": ("Pins &amp; Aces", "Tees &amp; Tunes Gift Pack, Black", "$68.15, was $104.85", "https://pinsandaces.com/products/tees-tunes-gift-pack",
   "A pack built around a speaker, for the musician of the group."),
 "d28": ("Winston Collection", "Drawstring Player&rsquo;s Pouch, Waxed Canvas", "$79.99", "https://winstoncollection.com/products/drawstring-players-pouch-waxed-canvas",
   "A waxed canvas pouch for a soldier&rsquo;s kit."),
 "d29": ("Kraken Golf", "Bedrock Copper Ball Marker", "$109", "https://www.krakengolf.com/products/bedrock-copper-golf-ball-marker",
   "Solid copper, like the man."),
 "d30": ("Students Golf", "Stockton Work Pants", "$138", "https://studentsgolf.com/products/stockton-work-pants",
   "Work pants for a long campaign."),
 "d31": ("Gramicci", "Japanese Denim Trucker", "$200", "https://www.gramicci.com/products/japanese-denim-trucker",
   "Japanese denim with years left in it."),
 "d32": ("Devereux Golf", "Grand Canyon Country Club Hoodie, Faded Black", "$84", "https://devereuxgolf.com/products/grand-canyon-country-club-hoodie-faded-black",
   "Faded black, like a stillsuit after a decade of war."),
 "d33": ("Winston Collection", "Midnight Camo Stripe Leather Headcovers", "$109.99", "https://winstoncollection.com/products/midnight-camo-stripe-tradition-leather-headcovers",
   "Midnight camo leather for a veteran&rsquo;s bag."),
 "d34": ("Clamp Golf Co.", "Vintage Valuables Pouch", "&pound;60 (about $80)", "https://www.clampgolfcompany.co.uk/products/vintage-valuables-pouch",
   "A vintage-look leather valuables pouch."),
 "d35": ("Winston Collection", "Classic Scorecard Holder, Colombian Leather", "$59.99", "https://winstoncollection.com/products/classic-scorecard-holders-in-colombian-leather",
   "A leather scorecard holder that has kept count of a lot."),
 "d36": ("Seamus Golf", "Hand Forged Goat Caddie Ball Marker, Copper", "$36", "https://seamusgolf.com/products/hand-forged-goat-caddie-ball-mark-copper",
   "A hand-forged copper marker, the color of melange."),
 "d37": ("Sunday Golf", "Big Rig Cart Bag, Burnt Orange", "$300, was $330", "https://sundaygolf.com/products/the-big-rig-burnt-orange-cart-bag",
   "A burnt orange cart bag. Spice-colored."),
 "d38": ("Mantra Golf", "Catalyst Polo, Point Collar, Snake", "$68, was $88", "https://mantragolf.com/products/catalyst-polo-point-collar-snake",
   "Mantra&rsquo;s Snake print. For Shai-Hulud."),
 "d39": ("Winston Collection", "Exotic Snakeskin Texture Leather Headcovers", "$49.99, was $99.99", "https://winstoncollection.com/products/exotic-snakeskin-leather-headcovers",
   "Snakeskin-texture leather, half off. For the worm."),
 "d40": ("Provision Machining &amp; Design", "Copper Divot Tool with Spade", "$39.99", "https://www.provisionmachiningdesign.com/products/copper-spade-golf-divot-tool",
   "A copper divot tool with a spade, for digging into the spice."),
 "d41": ("Dormie Workshop", "Chevron Rust Hybrid Headcover", "$150", "https://dormieworkshop.com/products/dormie-chevron-rust-hybrid-headcover",
   "Leather chevrons in rust."),
}

# key, name, kicker, sketch(html), ids
CH = [
 ("paul", "Paul Atreides, Emperor", "The Emperor",
  "<p>Twelve years after the last film, Paul rules the Known Universe. He&rsquo;s worshipped as Muad&rsquo;Dib and increasingly trapped by it. His bag would be the most expensive thing on the range, and it would still carry a little of the desert he came from.</p>",
  ["d00", "d01", "d02", "d03", "d04", "d05"]),
 ("hayt", "Hayt (Duncan Idaho)", "The Ghola",
  "<p>Duncan Idaho died defending Paul in the first film. The Bene Tleilax bring him back as Hayt, a ghola grown from his cells, with mechanical eyes and a past he can&rsquo;t quite reach, and present him to the Emperor as a gift. His kit is hard, polished and built like a weapon.</p>",
  ["d06", "d07", "d08", "d09", "d10", "d11"]),
 ("scytale", "Scytale", "The Face Dancer",
  "<p>A Tleilaxu Face Dancer who can wear any face he wants, and one of the conspirators circling Paul. Everything he carries is reversible, two-faced or a little disguised.</p>",
  ["d12", "d13", "d14", "d15", "d16", "d17"]),
 ("stilgar", "Stilgar", "The Naib",
  "<p>Once the leader of Sietch Tabr, Stilgar now stands at the Emperor&rsquo;s side as a true believer. He&rsquo;s still a man of the desert: nothing wasted, especially water.</p>",
  ["d18", "d19", "d20", "d21", "d22", "d23"]),
 ("gurney", "Gurney Halleck", "The Warrior-Poet",
  "<p>Fighter, poet and musician, Paul&rsquo;s oldest teacher and one of the few people who still talks to him straight. Wool, cord and a pouch for whatever he&rsquo;d play between holes.</p>",
  ["d24", "d25", "d26", "d27", "d28", "d29"]),
 ("farok", "Farok", "The Veteran",
  "<p>A Fremen veteran of the holy war fought in Paul&rsquo;s name, quietly losing faith in what it became. His kit is workwear that has seen a long campaign.</p>",
  ["d30", "d31", "d32", "d33", "d34", "d35"]),
 ("spice", "The Spice and Shai-Hulud", "Arrakis",
  "<p>Everything on Arrakis runs on the spice, so everything spice-colored goes in this bag: copper, rust, burnt orange and a snakeskin cover for the worm.</p>",
  ["d36", "d37", "d38", "d39", "d40", "d41"]),
]
N = 42

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p><em>Dune: Part Three</em> opens December 18. It adapts Frank Herbert&rsquo;s 1969 novel <em>Dune Messiah</em> and picks up twelve years after the last film: Paul is Emperor, a holy war has been fought in his name, and a conspiracy is forming around the throne.</p>
    <p>We asked a simple question: what would these people carry on a golf course? Six characters from the new film, plus a bag for the spice itself. The Harkonnens and Duke Leto don&rsquo;t make this one, so they&rsquo;re out.</p>
    <p><strong>How we picked.</strong> Six pieces per character, clothing and accessories, all from independent golf brands and all in stock as of November 16. Some of the matches are serious, like a desert-colored polo for a desert man. Some are not, like a Dual Face T-shirt for a Face Dancer.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Cast</div>
      __LIST__
      <div class="sidebar-detail"><span class="l">In theaters</span><span>December 18, 2026</span></div>
      <div class="sidebar-detail"><span class="l">Prices</span><span>Checked Nov 16, 2026</span></div>
      <div class="hashtags">
        <span class="hashtag">#Dune</span>
        <span class="hashtag">#GolfStyle</span>
        <span class="hashtag">#Crossover</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
STORY = """
<section class="products" data-btk="story" style="margin-top:8px;padding-bottom:48px">
  <div class="drop-tag grass">Keep Going</div>
  <h2 class="products-hdr" id="more">More Crossovers</h2>
  <div class="writeup-body">
    <p>For more golf through someone else&rsquo;s eyes, read <a href="/drops/climbing-golf-crossover-gear">Climbing x Golf</a>, our ritual-object guide <a href="/drops/golf-superstitions-lucky-rituals">Lucky</a>, and <a href="/drops/golf-gear-for-climbers-anglers-techies-surfers">golf gear for climbers, anglers, techies and surfers</a>.</p>
  </div>
</section>
"""
FRN = json.loads((ROOT / "research/dune-golf/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-R3-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}'
 '.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}'
 '@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}'
 '.product-card[data-frames="1"] .pg-arw,.product-card[data-frames="1"] .pg-count,.product-card[data-frames="1"] .pg-dots{display:none!important}'
 '.bc-top{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:48px;align-items:center;margin:0 auto 36px}'
 '.bc-camp{margin:0}.bc-camp img{display:block;width:100%;aspect-ratio:4/5;object-fit:cover;border:.5px solid var(--ink)}'
 '.bc-txt{text-align:center}.bc-txt p{margin:0 0 14px!important;line-height:1.65}.bc-txt .products-hdr{margin-top:6px!important}'
 '.dg-role{font-family:var(--serif);font-style:italic;font-size:clamp(22px,2.2vw,30px);color:var(--grass);margin-bottom:14px}'
 '@media(max-width:820px){.bc-top{grid-template-columns:1fr;gap:22px}}'
 '</style>\n')


def card(k, idx):
    brand, item, price, url, copy = P[k]
    fr = FRN[k]
    label = H.unescape(f"{brand} {item}").replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>' for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>' for j in range(len(fr)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{brand}</div>'
            f'<div class="product-name">{item} &middot; {price}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="{url}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items = [{"@type": "ListItem", "position": i + 1, "url": P[k][3], "name": H.unescape(re.sub(r"<[^>]+>", "", f"{P[k][0]} {P[k][1]}"))}
             for i, k in enumerate(k for c in CH for k in c[4])]
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": DATE, "dateModified": DATE,
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": items},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Drops & Brands", "item": "https://thegrassyissue.com/#feed"},
            {"@type": "ListItem", "position": 3, "name": "Dune x Golf", "item": URL}]},
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


def section(c, n0):
    key, name, role, sketch, ids = c
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" id="c-{key}" style="margin-top:8px;">\n'
            f'  <div class="bc-top">\n'
            f'    <figure class="bc-camp" data-char-slot="{key}"><img src="{IMG}/char-{key}.jpg" alt="{H.escape(H.unescape(name))}" loading="lazy" /></figure>\n'
            f'    <div class="bc-txt">\n'
            f'      <div class="dg-role">{role}</div>\n'
            f'      <h2 class="products-hdr" id="{key}">{name}</h2>\n'
            f'      {sketch}\n'
            f'    </div>\n  </div>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def main(apply_):
    ids = [k for c in CH for k in c[4]]
    assert len(ids) == N == len(set(ids)) and set(ids) == set(P), (len(ids), set(P) ^ set(ids))
    for k in ids:
        assert FRN[k] and all((ROOT / f.lstrip("/")).is_file() for f in FRN[k]), k
    for c in CH:
        assert (ROOT / IMG.lstrip("/") / f"char-{c[0]}.jpg").is_file(), c[0]
    lst = "\n      ".join(f'<div class="sidebar-detail"><span class="l">{c[2]}</span><span><a href="#c-{c[0]}">{c[1]}</a></span></div>' for c in CH)
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
    <span>Drops &amp; Brands &middot; Crossover</span><span class="dot"></span>
    <span>7 sections &middot; {N} pieces &middot; prices checked November 16, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A golfer swinging on a high-desert course under a wide sky" fetchpriority="high" /></div></div>
"""
    body += TAKE.replace("__LIST__", lst)
    n = 1
    for c in CH:
        o, n = section(c, n); body += o
    body += STORY
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    text = re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<script\b.*?</script>", " ", above))
    bad = []
    if fin.count('class="product-card"') != N: bad.append("card count")
    if re.search(r"\b(worth|genuinely|honestly|straightforward|selling out)\b", text, re.I): bad.append("banned word")
    for f in set(re.findall(r'src="(/images/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
