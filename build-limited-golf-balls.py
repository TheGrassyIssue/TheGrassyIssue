#!/usr/bin/env python3
"""build-limited-golf-balls.py — The Limited Run: 17 limited-edition golf balls to buy now.
29 September 2026. Lenny: "Let's do a post about Limited edition golf balls, calloway, vice, Seed,
and more have cool limited runs of interesting golf balls", then "looks good, let's put it all together".

FACTS: research/ltd-balls/notes.md (verified on brand stores 29 Sep 2026). Titleist "Icon Edition
Pro V1" excluded (April Fools' story). Prices per dozen unless noted, store currency; Seed in EUR
with approximate USD at 1.1366 (EUR/USD, 29 Sep 2026). PHOTOS: brands' own store images.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "limited-edition-golf-balls"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/limited-balls"
FRN = json.loads((ROOT / "research/ltd-balls/frames.json").read_text())

TITLE = "Limited-Edition Golf Balls: 17 Special Runs to Buy Right Now"
DESC = ("Limited-edition golf balls from Callaway, Vice, Seed, TaylorMade, Bridgestone and more: hot dogs, "
        "cocktails, Oktoberfest, artist collabs and throwbacks, with prices.")
H1 = "The Limited Run: 17 Limited-Edition Golf Balls to Buy Right Now"

# key -> (brand, ball, price, frames key, url, copy)
P = {
 "cocktails": ("Callaway", "Chrome Tour Cocktails", "$59.99", "Chrome Tour Cocktails",
   "https://www.callawaygolf.com/balls/chrome-tour-balls/balls-2026-chrome-tour-truvis-cocktails.html",
   "This puts a margarita, a mojito, a Moscow mule and an old fashioned on four Chrome Tour balls, one drink per ball. The box looks like a bar menu."),
 "hotdog": ("Callaway", "Chrome Tour Hot Dog", "$59.99", "Chrome Tour Hot Dog",
   "https://www.callawaygolf.com/balls/chrome-tour-balls/balls-2026-chrome-tour-truvis-hot-dog.html",
   "It has four hot dog pairings, ketchup, mustard, relish and the dog itself, in a box shaped like a food truck. Callaway calls it &ldquo;a course favorite&rdquo; brought to life."),
 "oktoberfest": ("TaylorMade", "TP5/TP5x pix Oktoberfest", "$64.99", "TP5/TP5x pix Oktoberfest",
   "https://www.taylormadegolf.com/TP5%2FTP5x-pix-Oktoberfest-Golf-Balls/DW-TE938-OK.html",
   "The balls carry beer steins and pretzels, and the dozen comes in a box printed like a bag of pretzels. TaylorMade&rsquo;s line: &ldquo;Oktoberfest flavor on the outside, Tour-proven performance on the inside.&rdquo;"),
 "prost": ("Vice", "Pro(st) Beer", "$44.99", "Pro(st) Beer",
   "https://vicegolf.com/products/vice-pro-prost-edition-beer",
   "It is a cast urethane Vice Pro finished to look like a glass of beer, gold with a white head. The name is &ldquo;A German toast that means cheers!&rdquo;"),
 "gregmike": ("Vice", "Pro Greg Mike Smiley", "$44.99", "Pro Greg Mike Smiley",
   "https://vicegolf.com/products/vice-pro-greg-mike-smiley",
   "This is a yellow three-piece urethane Vice Pro with a smiley face, made with the street artist Greg Mike. The box is covered in them."),
 "striping": ("Vice", "Pro Air Tracer Striping It", "$44.99", "Pro Air Tracer Striping It (Swannies)",
   "https://vicegolf.com/products/vice-pro-air-tracer-striping-it",
   "It is a limited colourway of the Vice Pro Air Tracer from the Swannies x Vice collaboration, with pink and orange stripes wrapped around the ball."),
 "eastside": ("Eastside Golf x Bridgestone", "TOUR B X", "$55", "ESG TOUR B X dozen",
   "https://eastsidegolf.com/products/bridgestone-golf-balls-12-pack-white",
   "This is Bridgestone&rsquo;s TOUR B X with Eastside Golf&rsquo;s Swingman logo on one side and the Bridgestone B on the other."),
 "foreall": ("Fore All x Cynthia Rowley", "Golf Balls, Multi", "$48.99", "Golf Balls, Multi",
   "https://foreall.com/products/cr-x-fa-golf-balls-dozen-multi",
   "It is a three-piece ball from the women&rsquo;s golf brand Fore All and the designer Cynthia Rowley, in a collector box, and sold as final sale."),
 "marooch": ("Seed", "SD-01 MAROOCH", "&euro;39 (~$44)", "SD-01 MAROOCH",
   "https://seedgolf.com/products/sd-01-the-pro-one-marooch",
   "This is Seed&rsquo;s three-piece urethane SD-01 with a custom print for its partnership with the speedgolfer Rob Hogan, better known as Marooch. The product copy says: &ldquo;Grab some before they&rsquo;re gone!&rdquo;"),
 "retro": ("Callaway", "Chrome Tour Retro", "$59.99", "Chrome Tour Retro",
   "https://www.callawaygolf.com/balls/chrome-tour-balls/balls-2026-chrome-tour-retro.html",
   "It is a tribute to Callaway&rsquo;s first golf ball, the Rule 35 from 2000. Rule 35 was Callaway&rsquo;s made-up addition to the 34 rules of golf: &ldquo;Enjoy the Game.&rdquo;"),
 "walkitin": ("Bridgestone", "Walk It In Capsule", "$99.99 kit", "Walk It In Capsule (TOUR B X kit)",
   "https://shop.bridgestonegolf.com/products/walk-it-in-kit",
   "It is a dozen TOUR B X with a hat and socks, a tribute to Tiger&rsquo;s 2000 season in Y2K, VHS-style packaging. Only the medium socks are left."),
 "mtb": ("Snell", "MTB Black LTD", "$38.99", "MTB Black LTD",
   "https://www.snellgolf.com/products/mtb-black-ltd",
   "This is a three-piece cast urethane ball that Snell calls &ldquo;the return of one of the most requested golf balls in Snell history.&rdquo; A four-dozen pack runs through 30 September."),
 "suits": ("Callaway", "Chrome Tour Suits", "$59.99", "Chrome Tour Suits",
   "https://www.callawaygolf.com/balls/chrome-tour-balls/balls-2026-chrome-tour-truvis-suits.html",
   "It has hearts, diamonds, clubs and spades, one suit per ball, in a box like a deck of cards. Callaway: &ldquo;Deal yourself a winning hand.&rdquo;"),
 "tan": ("Vice", "Pro Tan", "$44.99", "Pro Tan",
   "https://vicegolf.com/products/vice-pro-tan",
   "This one is two-tone, like a golfer&rsquo;s tan line, in a box with a sunburnt cartoon golfer. Vice: &ldquo;Some tan lines never fade.&rdquo;"),
 "craic": ("Seed", "SD-01 The Craic", "&euro;39 (~$44)", "SD-01 The Craic",
   "https://seedgolf.com/products/sd-01-the-craic",
   "It is the same SD-01 with a new logo. The product copy: &ldquo;Same great taste, brand new logo.&rdquo;"),
 "halloween": ("Callaway", "Chrome Tour Halloween", "$49.99 (sale)", "Chrome Tour Halloween (2025)",
   "https://www.callawaygolf.com/balls/chrome-tour-balls/balls-2025-chrome-tour-halloween.html",
   "This is last year&rsquo;s scary-movie set, now on sale, and it is the only Halloween ball we found for this October. Callaway: &ldquo;Play if you dare.&rdquo;"),
 "pgahope": ("OnCore", "PGA HOPE Charity Edition", "$36&ndash;$46", "PGA HOPE Charity Edition",
   "https://www.oncoregolf.com/products/pga-hope-special-edition-golf-balls/",
   "It is a co-branded dozen in OnCore&rsquo;s ELIXR or VERO models, and $5 from every dozen goes to PGA HOPE, the PGA&rsquo;s golf programme for veterans."),
}

SECTIONS = [
    ("Food and Drink", "food-and-drink", ["hotdog", "cocktails", "oktoberfest", "prost"],
     "<strong>Four balls &middot; $44.99&ndash;$64.99</strong>This is the season for it: a hot dog truck, a cocktail menu and two Oktoberfest balls."),
    ("Art and Collabs", "art-and-collabs", ["gregmike", "striping", "marooch", "eastside", "foreall"],
     "<strong>Five balls &middot; $44.99&ndash;$55</strong>These balls come from a street artist, an apparel brand, a speedgolfer and a fashion designer."),
    ("Throwbacks and Tributes", "throwbacks", ["retro", "walkitin", "mtb"],
     "<strong>Three balls &middot; $38.99&ndash;$99.99</strong>These look back: Callaway&rsquo;s first ball, Tiger in 2000, and a Snell favourite brought back."),
    ("Just for Fun, and a Good Cause", "fun-and-causes", ["suits", "tan", "craic", "halloween", "pgahope"],
     "<strong>Five balls &middot; $36&ndash;$59.99</strong>The last five run from a deck of cards to a charity dozen."),
]

PROSE = 'style="max-width:760px;font-size:16px;line-height:1.7;margin:0 auto 24px;"'

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>The golf ball used to be the most boring thing in the bag, white with a number on it. Now it is where brands have the most fun. Callaway has put hot dogs, cocktails and pandas on its tour ball, TaylorMade sells its TP5 in a pretzel bag for Oktoberfest, and Vice makes a ball that looks like a glass of beer.</p>
    <p>The best part is that most of these are the brand&rsquo;s real tour ball underneath, with the same urethane cover and the same construction. You are not giving up anything to play a hot dog. They sell in short runs, disappear, and turn up later on resale sites, so if one makes you laugh, buy the dozen now.</p>
    <h2 class="products-hdr btk-story-hdr">What the Designs Are Saying</h2>
    <p><strong>Golf is a food-and-drink sport now.</strong> The biggest theme this year is the snack bar and the clubhouse bar. Hot dogs, margaritas, pretzels and beer are all on tour balls, sold in boxes that look like a food truck, a bar menu or a bag of pretzels. It is the same instinct that made the turn-house hot dog a social media genre: the round is the hangout, and the ball is joining in.</p>
    <p><strong>The box is half the product.</strong> Callaway&rsquo;s cocktails come in a menu, its suits in a deck of cards, its Halloween balls in a horror-movie case. Bridgestone&rsquo;s Tiger tribute comes in a VHS-style sleeve with a hat and socks. These are made to be photographed, gifted and kept on a shelf, which is why so many end up unopened on resale sites.</p>
    <p><strong>Nostalgia sells.</strong> Callaway went back to its first ball, the Rule 35 from 2000. Bridgestone went back to Tiger&rsquo;s 2000 season, and Snell brought back a black ball its customers kept asking for. The turn of the millennium is the new vintage, for the same golfers who grew up on it.</p>
    <p><strong>America turned 250, and the balls noticed.</strong> Flag stripes, 1776 play numbers and red, white and blue alignment lines ran across Callaway, TaylorMade, Titleist and Bridgestone this summer. Most of those have now sold out.</p>
    <p><strong>The collab has moved from the shirt to the ball.</strong> Street artists, apparel brands, a speedgolfer and a fashion designer all have their names on a dozen now, the same way they did on hats and headcovers a few years ago. A ball is cheap to make and easy to collect, so it has become the entry-level collab.</p>
    <p><strong>The calendar is the design brief.</strong> There is a ball for the Fourth of July, one for Oktoberfest, one for Halloween and one for each major. Brands are treating golf balls like seasonal merchandise, and the run is over before the season is.</p>
    <p>If you only buy one, get the Callaway Chrome Tour Hot Dog at $59.99, which comes in a food-truck box. Prices were read from each brand&rsquo;s own store on 29 September 2026, per dozen unless noted.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Balls</span><span>17 limited runs</span></div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>Callaway, Vice, Seed, TaylorMade, Bridgestone and more</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$36&ndash;$99.99</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Chrome Tour Hot Dog, $59.99</span></div>
      <div class="sidebar-detail"><span class="l">Prices read</span><span>29 September 2026</span></div>
      <a href="#food-and-drink" class="sidebar-cta">See the balls &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#GolfBalls</span>
        <span class="hashtag">#LimitedEdition</span>
        <span class="hashtag">#GolfCollabs</span>
        <span class="hashtag">#GolfCulture</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

GONE = f"""
<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr" id="gone">Gone, but Keep an Eye Out</h2>
  <div {PROSE}>
    <p style="margin:0 0 16px;">These sold out before we could get to them, and they are the ones to look for on resale sites or if the brands run them back. Bridgestone had a year of them: a Masters-week Peach Reserve Vault, a Pabst Blue Ribbon kit, an Open-themed Leaderboard Edition, a blacked-out TOUR B X and RX, and its USA 250 balls.</p>
    <p style="margin:0 0 16px;">Callaway&rsquo;s Chrome Tour Major Series, one design for each major, has come off its US store, and the Tour X and Chrome Soft versions of its USA Stripe ball have sold out. Srixon&rsquo;s All-American Z-STAR DIAMOND, Titleist&rsquo;s Folds of Honor Pro V1, Vice&rsquo;s Greg Mike Loudmouf and baseball-stitched Fastball, Malbon&rsquo;s Buckets Tour M and the Bad Birdie x Maxfli Amateurs ball are all gone too.</p>
  </div>
</section>
"""

FAQ = [
    ("Are limited-edition golf balls the same as the regular ones?",
     "Usually, yes. Most limited runs here are the brand's regular tour ball with a new print, such as Callaway's Chrome Tour, TaylorMade's TP5 and TP5x and Vice's Pro. The performance is the same; the design is what changes."),
    ("What limited-edition golf balls are available right now?",
     "As of 29 September 2026: Callaway's Chrome Tour Hot Dog, Cocktails, Suits and Retro; TaylorMade's TP5 pix Oktoberfest; Vice's Pro(st) Beer, Tan, Greg Mike Smiley and Striping It; Seed's SD-01 MAROOCH and The Craic; Bridgestone's Walk It In capsule; Snell's MTB Black LTD; and more."),
    ("How much do limited-edition golf balls cost?",
     "Most are priced like the brand's regular premium ball: around $45 a dozen from Vice, $59.99 from Callaway and $64.99 from TaylorMade. Bridgestone's Walk It In is a $99.99 kit with a hat and socks."),
    ("Do limited-edition golf balls sell out?",
     "Yes. Brands make them in short runs and many sell out within weeks. Several 2026 editions from Bridgestone, Srixon, Titleist and Callaway are already gone."),
    ("Is there a Halloween golf ball this year?",
     "We did not find a new 2026 Halloween ball on the brands' stores. Callaway's 2025 Chrome Tour Halloween scary-movie set is still available, on sale at $49.99."),
]


def card(k, idx):
    brand, ball, price, fk, url, copy = P[k]
    fr = [f["local"] for f in FRN[fk]]
    label = H.unescape(f"{brand} {ball}").replace('"', "")
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
            f'<div class="product-name">{ball} &middot; {price}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="{url}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


def section(sec, n0):
    h2, anchor, ids, kicker = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} balls</div>\n'
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
    for sec in SECTIONS:
        for h in sec[2]:
            items.append({"@type": "ListItem", "position": pos, "url": P[h][4], "name": H.unescape(f"{P[h][0]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-09-29", "dateModified": "2026-09-29",
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
            {"@type": "ListItem", "position": 3, "name": "Limited-Edition Golf Balls", "item": URL}]},
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
    ids = [k for s in SECTIONS for k in s[2]]
    assert len(ids) == 17 == len(set(ids)) and set(ids) == set(P)
    for k in ids:
        assert FRN.get(P[k][3]), k
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Limited-Edition Golf Balls</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Callaway, Vice, Seed, TaylorMade and more</span><span class="dot"></span>
    <span>17 balls &middot; in stock 29 September 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Callaway Chrome Tour Hot Dog golf balls in front of their food-truck boxes on a red checked tablecloth" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        o, n = section(s, n); body += o
    body += GONE + faq_html()
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
    if fin.count('class="product-card"') != 17: bad.append("card count")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", above), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
