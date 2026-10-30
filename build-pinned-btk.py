#!/usr/bin/env python3
"""build-pinned-btk.py — Brand to Know: Pinned Golf (golf tech: rangefinders, the Caddie GPS tablet, speakers). 30 October 2026.
Cloned from build-dicey-btk.py. Lenny: "a brand to know - pinnedgolf.com" -> options sheet (18) -> "Let's just show the full line up".
FACTS: pinnedgolf.com Story page, homepage and product copy (read in Chrome 29-30 Oct 2026, USD, all in stock);
Canton Citizen, Mar 27 2025 (founders Matt Buckley, Alec Lorenzo, John Rowell; founded 2018; Presidents Golf Course, Quincy;
Buckley quotes); GolfNewsRI, Jan 23 2026 (Best New Product at the PGA Show in 2025 for the Caddie and 2026 for the Sound Stick PRO;
Massachusetts-based); Golf Monthly Prism+ review ("performs like a rangefinder double its price"). No FAQ. Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Brand to Know: Pinned Golf, Rangefinders and Speakers With Better Vibes"
DESC = ("Pinned Golf is a Massachusetts golf tech brand started in 2018 by three friends who couldn't afford a rangefinder. "
        "The full line-up: the Prism+, the award-winning Caddie GPS tablet and Sound Stick speakers, with prices.")
H1 = "Brand to Know: Pinned Golf, Golf Tech for the Rest of Us"
BC = "Brand to Know: Pinned Golf"
SLUG = "brand-to-know-pinned-golf"
IMG = "/images/pinned-golf"
SHOP = "https://pinnedgolf.com/products/"
C = "Pinned Golf"
P = {
 "prism": (C, "Prism+ Rangefinder", "$259.99", "prism-rangefinder-black",
   "Our pick. The rangefinder that started the company, now in its Prism+ version: slope-adjusted distances, first-target lock, a rechargeable battery and a magnet to stick it to the cart. It comes in ten colorways, including orange, royal blue and a stars-and-stripes USA version. Golf Monthly said it performs like a rangefinder double its price."),
 "caddie": (C, "Caddie GPS Smart Tablet", "$399.99", "the-caddie-golf-tablet",
   "Best New Product at the 2025 PGA Show. An 8-inch weatherproof tablet that sits on your cart with a magnet and shows the whole hole: front, middle and back yardages, hazards, scoring and games, at 45,000+ courses, with no cell service or wifi needed. Down from $449.99."),
 "sspro": (C, "Sound Stick PRO", "$199.98", "sound-stick-pro",
   "Best New Product at the 2026 PGA Show. A magnetic speaker with a color touch screen that pairs with the Pinned app for live yardages, green heat maps and leaderboards, so the music and the numbers come from the same thing on your cart."),
 "sstick": (C, "Sound Stick Speaker", "$99.99", "sound-stick-speaker",
   "The original cart speaker, in six colors. A built-in magnet and a battery that lasts more than 15 hours. Pinned&rsquo;s line for it: better music, better vibes, better golf. Down from $150."),
 "dart": (C, "Dart 2.0 Speaker", "$64.99", "the-dart-2-0-speaker-green",
   "The smallest speaker, a round puck with a stronger magnet, a detachable carabiner and 10+ hours of battery. Six colors. Clip it to the bag if you&rsquo;re walking."),
 "roller": (C, "The Roller Putting Mat", "$175", "roller-putting-mats",
   "A 9-foot indoor putting mat for the office or the living room, made with the original founders of Perfect Practice. Six colors, from white to green and pink. The off-season piece."),
 "stickpro": (C, "Stick Kit PRO", "$399.99", "prism-sound-stick-pro",
   "The Prism+ and the Sound Stick PRO together: the rangefinder for the flag and the speaker for live yardages and music. Down from $459.99."),
 "stick": (C, "Stick Kit", "$299.99", "prism-bundle",
   "The Prism+ with the original Sound Stick, in matching colors. The easy way into both."),
 "combo": (C, "Caddie Combo", "$399.99", "caddie-bundle",
   "The Caddie tablet with a Sound Stick, in red, blue or green. Yardages on the screen, music from the stick."),
 "comboplus": (C, "Caddie Combo+", "$599.99", "caddie-prism",
   "The full setup: the Caddie for maps, heat maps, scoring and stats, and the Prism+ for the exact number to the flag."),
 "mount": (C, "Caddie Cart Mount", "$39.99", "caddie-cart-mount",
   "A mount to hold the Caddie on a push cart or trolley, for anyone who walks."),
 "magpad": (C, "MagPad", "$39.99", "magpad",
   "Pinned calls it the magnetic hub for all of its products: a pad that gives the rangefinder, speakers and Caddie somewhere to stick."),
 "markers": (C, "Ball Markers", "From $14.99", "ball-markers",
   "Thirteen designs, including a Stop 3 Putting sign, a bullseye, a USA flag and a Swing Juice can. The cheapest thing Pinned sells."),
 "towels": (C, "Colorway Towels", "$29.99", "colorway-towels",
   "Golf towels in six colors to match the speakers and rangefinders, with a small Pinned crosshair logo."),
 "hats": (C, "Hats", "$19.99", "p-snapbacks",
   "Snapbacks in four styles, from a cream and navy Pinned Golf hat with a flag to a black Pinned Golf Co. hat. One size."),
 "charger": (C, "Portable Charger", "$39.99", "portable-charger",
   "A backup battery for the Caddie, rangefinder, speaker or phone, printed with Always Dialed In. US shipping only."),
 "prcase": (C, "Extra Prism+ Case", "$29.99", "extra-prism-case",
   "A replacement hard case for the Prism+, in six colors to match the rangefinder."),
 "spcase": (C, "Speaker Case", "$34.99", "speaker-case",
   "A zip case for the Sound Stick, so it survives the trunk."),
}
SECTIONS = [
 ("The Tech", "the-tech", ["prism", "caddie", "sspro", "sstick", "dart", "roller"],
  "<strong>Six products &middot; $64.99&ndash;$399.99</strong>The rangefinder, the two PGA Show winners, the speakers and an indoor putting mat."),
 ("Bundles and Mounts", "bundles", ["stickpro", "stick", "combo", "comboplus", "mount", "magpad"],
  "<strong>Six products &middot; $39.99&ndash;$599.99</strong>Pinned sells most of its tech in pairs, and the bundles are where the biggest savings are."),
 ("The Extras", "extras", ["markers", "towels", "hats", "charger", "prcase", "spcase"],
  "<strong>Six products &middot; $14.99&ndash;$39.99</strong>Markers, towels, hats and the small things that keep the tech charged and in one piece."),
]
N = 18
PQ = {
 "bundles": ("A big part of our brand is better vibes, better golf.", "Matt Buckley, co-founder, to the Canton Citizen"),
}
BANDS = {
 "the-tech-after": ("On the course", "Pinned&rsquo;s own photos of the rangefinder and the hats in use.",
   [("band-1-1", "A golfer checking a distance with a Pinned rangefinder in front of tall pines", "Getting the number"),
    ("band-1-2", "Two golfers pointing down the fairway", "That way"),
    ("band-1-3", "A man in a black Pinned hat on a cloudy day by the water", "The Pinned hat")]),
 "bundles-after": ("The setup", "Speakers, the Caddie and a cart.",
   [("band-2-1", "A row of Pinned speakers and rangefinders in every color lined up under palm trees", "Every color"),
    ("band-2-2", "A golf cart parked on a wide green fairway", "The office"),
    ("band-2-3", "A smiling golfer holding a green Sound Stick and the Caddie tablet in a cart", "Stick and Caddie")]),
 "extras-after": ("Better vibes", "The idea behind the brand, in three photos.",
   [("band-3-1", "A couple sitting in director chairs on a golf course", "Between holes"),
    ("band-3-2", "Two golfers fist-bumping on a fairway lined with palms", "Nice shot"),
    ("band-3-3", "The Caddie tablet lying on a green next to the hole", "On the green")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Pinned Golf makes golf tech, not clothes, but it earns a Brand to Know the same way the clothing brands do: it has a point of view. Rangefinders and GPS gadgets are usually gray, serious and expensive. Pinned makes them in orange, royal blue and stars and stripes, prices them well under the big names, and builds everything around one line: better vibes, better golf.</p>
    <p><strong>The rangefinder.</strong> The company started with one, and the Prism+ is still the center of the line. It does what the expensive ones do, with slope, a quick lock on the flag and a magnet for the cart, for $259.99 and in ten colors. The reviews have mostly been kind: Golf Monthly said it performs like a rangefinder double its price.</p>
    <p><strong>The Caddie and the Sound Stick PRO.</strong> Pinned has now won Best New Product at the PGA Show two years running. In 2025 it was the Caddie, an 8-inch tablet that sticks to the cart and shows the whole hole at 45,000+ courses without cell service. In 2026 it was the Sound Stick PRO, a speaker with a touch screen that pairs with the Pinned app for live yardages and leaderboards. Together they are a cheaper, simpler version of a GPS cart, and you take them home after the round.</p>
    <p><strong>The rest.</strong> Speakers from $64.99, a 9-foot putting mat for the winter, and towels, hats and ball markers in the same colors as the tech. Most of the gear is sold in bundles that save $60 to $200. Right now every purchase also earns entries in a $10,000 golf trip giveaway, which tells you something about who Pinned is selling to: the group chat, not the pro shop.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">At a Glance</div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>2018</span></div>
      <div class="sidebar-detail"><span class="l">Founders</span><span>Matt Buckley, Alec Lorenzo, John Rowell</span></div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Massachusetts</span></div>
      <div class="sidebar-detail"><span class="l">Makes</span><span>Rangefinders, GPS, speakers</span></div>
      <div class="sidebar-detail"><span class="l">PGA Show</span><span>Best New Product, 2025 &amp; 2026</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Prism+ Rangefinder</span></div>
      <div class="hashtags">
        <span class="hashtag">#PinnedGolf</span>
        <span class="hashtag">#BetterVibesBetterGolf</span>
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
  <h2 class="products-hdr" id="story">Why Are They So Expensive?</h2>
  <div class="writeup-body">
    <p>Pinned started on a Saturday at Presidents Golf Course in Quincy, Massachusetts. Matt Buckley, Alec Lorenzo and John Rowell, three friends a few years out of college, all played golf, and none of them owned a rangefinder, in part because of what they cost. By Pinned&rsquo;s own telling, the excuse that day was always the same: the pin was a lot farther away than it looked.</p>
    <p>&ldquo;There&rsquo;s got to be one that&rsquo;s more for the average golfer,&rdquo; Buckley told the Canton Citizen in 2025, &ldquo;same feels and whistles as the fancy ones, but at a more affordable cost.&rdquo; They started Pinned in 2018 while all three had other full-time jobs. &ldquo;It all started out as a side business,&rdquo; Buckley said. &ldquo;I used to ship every single order out of my house way back when. We all ended up quitting our jobs.&rdquo;</p>
    <p>The rangefinder came first, then the speakers, because, as the brand puts it, those 18 holes are a lot more fun when the music is cranking and the cooler is stocked. The Caddie came from a survey of their own customers, who said they would rather read a distance off a screen in the cart. The three founders built it with a team of engineers, and it won Best New Product at the PGA Show in 2025. The Sound Stick PRO won the same award a year later.</p>
    <p>Pinned&rsquo;s story page ends where it began: golf should be fun, and the gear should be too. &ldquo;Golf has changed so much in the past few years,&rdquo; Buckley said. &ldquo;It&rsquo;s not as stuffy of a game. You don&rsquo;t have to be the greatest golfer to get on the course.&rdquo;</p>
  </div>
</section>
"""
FAQ = []
LOOKBOOK = ""
FRN = json.loads((ROOT / "research/pinned/frames.json").read_text())
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
         "url": URL, "image": og, "datePublished": "2026-10-30", "dateModified": "2026-10-30",
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
    <span>Brand to Know &middot; Massachusetts &middot; Est. 2018</span><span class="dot"></span>
    <span>The full line-up, 18 products &middot; checked October 30, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Three friends sitting on the grass at a golf course laughing, holding Pinned speakers and a Prism+ rangefinder" fetchpriority="high" /></div></div>
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
