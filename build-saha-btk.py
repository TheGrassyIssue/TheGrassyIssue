#!/usr/bin/env python3
"""build-saha-btk.py — Brand to Know: Saha Golf. 21 October 2026. Cloned from build-bunx-btk.py.
Lenny: "Let's do a brand to know- https://saha.golf/" ... "I want to lead with 4,9,12,19" ... "but include all in the post itself".
Lead: Playfield Polo, Fairway Knight Tee, Saha Logo Cap, Pack of Tees; then every other in-stock product (colorways merged: Lounge Polo, crew socks).
FACTS: saha.golf products.json (USD, Oct 21 2026); Terms of Service (operated by G3LU Corp dba Saha Golf); Shipping policy (ships from US and Turkiye);
homepage banners (Play the Field; free shipping over $100); Instagram @saha.golf (6 posts; "Saha is officially open"). No founder named anywhere.
The ToS business address is a registered-agent office in Austin, so we do NOT call the brand Austin-based. Saha = Turkish for field/pitch (general knowledge).
How's My Drive pieces carry "Call 1-800-PISS-OFF": included per Lenny, but we don't print the line in our copy.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Saha Golf: Football-Kit Polos and Questionable Packaging"
DESC = ("Brand to Know: Saha Golf, a brand-new golf label with a vintage football-kit polo, a knight tee that fades on purpose, "
        "bamboo tees in a cigarette box and clean basics. Every piece, $20 to $169.")
H1 = "Brand to Know: Saha Golf"
BC = "Saha Golf"
SLUG = "brand-to-know-saha-golf"
IMG = "/images/saha"
SHOP = "https://saha.golf/products/"
P = {
 "a1": ("Saha Golf", 'Playfield Polo', '$108', 'playfield-polo',
   'Our pick. Built off vintage football kits: digitally printed navy-and-green stripes, a contrast-tipped ribbed collar and Saha graphics in more than one spot. Saha&rsquo;s line: loud enough to lead the group, easy enough to play eighteen in.'),
 "a2": ("Saha Golf", 'Fairway Knight Tee', '$62', 'fairway-knight-tee',
   'A knight with a golf club on a relaxed cotton tee with 50+ UV protection. Best product note on the site: the club is drawn in such fine lines it may fade, and around the fifteenth wash the knight may finally trade it for a sword. &ldquo;Consider it character development.&rdquo;'),
 "a3": ("Saha Golf", 'Saha Logo Cap', '$40', 'saha-logo-cap',
   'Nothing loud, nothing missing: a black six-panel cap with a curved brim and the embroidered Saha oval. It&rsquo;s the cap in Saha&rsquo;s launch shoot.'),
 "a4": ("Saha Golf", 'Pack of Tees', '$20', 'pack-of-tees',
   'Twelve white-and-green bamboo tees, 70mm with a 10mm cup, in a box styled like a pack of cigarettes. Saha: premium tees, questionable packaging.'),
 "p1": ("Saha Golf", 'Playground Polo', '$115', 'playground-polo',
   'A long-sleeve navy cotton polo with a contrast white collar and placket and embroidered appliqu&eacute; artwork that gives it real weight. It runs oversized; Saha says go at least a size smaller.'),
 "p2": ("Saha Golf", 'Lounge Polo', '$96', 'lounge-polo-green',
   'The clean one: a stretch polo with a contrast-tipped collar and a small Saha logo at the chest, in green or white.'),
 "t1": ("Saha Golf", 'Apr&egrave;s Golf Tee', '$62', 'apres-golf-tee-1',
   'Navy, with Apr&egrave;s Golf arched across the front, for the rituals that follow a round. Relaxed cotton, 50+ UV.'),
 "t2": ("Saha Golf", 'Burning Golf Cart Tee', '$62', 'burning-golf-cart-tee-1',
   'Clean from the front. On the back, a golf cart on fire under the line &ldquo;I&rsquo;d like to see AI do this.&rdquo; Saha says it&rsquo;s about the very human ability to take things too far.'),
 "t3": ("Saha Golf", 'Slice Tee', '$62', 'slice-tee',
   'Green, with a yellow Saha Golfwear graphic at the chest. Simple from far away, better up close.'),
 "t4": ("Saha Golf", 'How&rsquo;s My Drive Tee', '$62', 'hows-my-drive-tee',
   'Inspired by roadside complaint lines: a cartoon golfer on the back with a 1-800 number we won&rsquo;t print here. Clean from the front, loud from the back.'),
 "b1": ("Saha Golf", 'Locker Room Pants', '$169', 'locker-room-pants',
   'Black woven trousers in a soft stretch blend with a relaxed fit. Sharp enough to wear out after the round.'),
 "b2": ("Saha Golf", 'Mulligan Shorts', '$138', 'mulligan-shorts',
   'Dark navy woven stretch shorts with a clean pleated front. Pleats in front, comfort everywhere else.'),
 "x1": ("Saha Golf", 'How&rsquo;s My Drive Cap', '$40', 'hows-my-drive-cap',
   'The complaint-line joke embroidered across a green six-panel cap. Bad drive, same attitude.'),
 "x2": ("Saha Golf", 'Crew Sock 3-Pack', '$50', 'saha-crew-sock-pack',
   'One pair each of white, green and black cotton-rich crew socks with the Saha logo embroidered at the ankle. Three colors, one less decision.'),
 "x3": ("Saha Golf", 'Crew Socks', '$20', 'saha-crew-sock-white',
   'Singles in white, green or black, $20 a pair. Good socks, no speech required.'),
 "x4": ("Saha Golf", 'Saha Clip Towel', '$45', 'saha-clip-towel',
   'A towel with Saha.Golf at the hem, a metal eyelet and a carabiner so it clips straight onto the bag.'),
}
SECTIONS = [
 ("Start Here", "start", ["a1","a2","a3","a4"],
  "<strong>Our four &middot; $20&ndash;$108</strong>The football-kit polo, the knight tee, the logo cap and the tees in the cigarette box."),
 ("The Polos", "polos", ["p1","p2"],
  "<strong>Two more polos &middot; $96&ndash;$115</strong>A long-sleeve appliqu&eacute; polo and the clean everyday one, in two colors."),
 ("The Tees", "tees", ["t1","t2","t3","t4"],
  "<strong>Four tees &middot; $62 each</strong>Relaxed cotton with 50+ UV protection. Most of the jokes live on the back."),
 ("Pants &amp; Shorts", "bottoms", ["b1","b2"],
  "<strong>Two pieces &middot; $138&ndash;$169</strong>Woven stretch, relaxed fit, nothing printed on them."),
 ("Cap, Socks &amp; Towel", "extras", ["x1","x2","x3","x4"],
  "<strong>Four pieces &middot; $20&ndash;$50</strong>The second cap, socks in singles or a three-pack, and a clip towel."),
]
N = 16
PQ = {
 "polos": ("Not here to change the game. Just the way you dress for it.", "Saha Golf, on Instagram"),
 "tees": ("Clean from the front, existential from the back.", "Saha Golf, on the Burning Golf Cart Tee"),
 "bottoms": ("Proper pants. Improper range of motion.", "Saha Golf, on the Locker Room Pants"),
}
CAP = "Photography &middot; Saha Golf"
BANDS = {
 "polos": ("The launch shoot", "Saha&rsquo;s own campaign photos, from its first weeks on Instagram.",
   [("irl-dbtjkrqsslb","A golfer in the black Saha Logo Cap lying on the green beside the hole and ball","The Saha Logo Cap, at eye level with the cup"),
    ("irl-dcv-gyaxvl1","A golfer in sunglasses and the green Slice Tee teeing up a ball","&ldquo;Saha is officially open.&rdquo;"),
    ("irl-dddfbjzxdh8","A golfer in the How&rsquo;s My Drive Tee seen from behind at a range ball basket","&ldquo;Bad drive. Worse attitude.&rdquo;")]),
 "extras": ("The rest of the feed", "Two more from Saha&rsquo;s Instagram, plus the hero above.",
   [("irl-deuy3kfkcrf","The Saha oval logo over a lake fountain at sunset","&ldquo;The course, our way.&rdquo;"),
    ("irl-dehnayhqjhk","The first Saha collection laid out in a grid around the logo","The first collection"),
    ("card-hero","A golfer in the black Saha Logo Cap lying on the green beside the hole","Eye level")]),
}
PROSE = 'style="max-width:760px;font-size:16px;line-height:1.7;margin:0 auto 24px;"'
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Saha Golf is about as new as a golf brand gets. Its Instagram announced &ldquo;Saha is officially open&rdquo; this summer, it has six posts, and there&rsquo;s no founder story anywhere on the site yet. So this one is all about the clothes, and the clothes are good.</p>
    <p><strong>The name is the brief.</strong> Saha is Turkish for field or pitch, the brand ships from both the US and T&uuml;rkiye, and the homepage says Play the Field. You can see it in the lead piece. The Playfield Polo takes its stripes and ribbed collar straight from a vintage football kit, and football shirts on the course are one of the better ideas in golf clothing right now. This is one of the best-looking versions we&rsquo;ve seen.</p>
    <p><strong>They write like golfers.</strong> The Fairway Knight Tee&rsquo;s product page warns that the club may fade after enough washes, and that the knight may eventually trade it for a sword. The bamboo tees come in a cigarette-style box. There&rsquo;s a burning golf cart tee with a joke about AI, and the shorts are called Mulligans. Some of it goes further than we would: the How&rsquo;s My Drive pieces carry a 1-800 punchline we won&rsquo;t print. Most of it is the kind of joke you&rsquo;d make in the cart.</p>
    <p><strong>The basics hold up.</strong> Behind the graphics there&rsquo;s a clean stretch polo, woven trousers, pleated shorts and plain crew socks, and every tee has 50+ UV protection, which matters in Texas in August. Prices sit at the premium end of independent golf: $62 tees, $96 to $115 polos and $169 trousers.</p>
    <p><strong>Two things to know.</strong> It&rsquo;s early, so there isn&rsquo;t much sizing feedback out there yet; Saha says the Playground Polo runs big, so size down. Some orders ship from T&uuml;rkiye, so check delivery times at checkout.</p>
    <p>If you buy one thing, get the Playfield Polo. If you&rsquo;re adding, take the Fairway Knight Tee and a box of tees.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Launched</span><span>Summer 2026</span></div>
      <div class="sidebar-detail"><span class="l">Ships from</span><span>US &amp; T&uuml;rkiye</span></div>
      <div class="sidebar-detail"><span class="l">Polos</span><span>$96&ndash;$115</span></div>
      <div class="sidebar-detail"><span class="l">Tees</span><span>$62, 50+ UV</span></div>
      <div class="sidebar-detail"><span class="l">In the post</span><span>All 19 products</span></div>
      <div class="hashtags">
        <span class="hashtag">#SahaGolf</span>
        <span class="hashtag">#GolfStyle</span>
        <span class="hashtag">#BrandToKnow</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("Who makes Saha Golf?", "Saha Golf is operated by G3LU Corp, according to its terms of service. The site does not name its founders."),
 ("Where does Saha Golf ship from?", "From fulfillment locations in the United States and Türkiye, depending on the product. Its site advertised free shipping on orders over $100 on October 21, 2026."),
 ("What does saha mean?", "Saha is Turkish for field or pitch. The brand's homepage tagline is Play the Field."),
 ("How does the Saha Playground Polo fit?", "Oversized. Saha recommends going at least one size smaller than usual."),
]
LOOKBOOK = ""
FRN = json.loads((ROOT / "research/saha/frames.json").read_text())
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
         "url": URL, "image": og, "datePublished": "2026-10-21", "dateModified": "2026-10-21",
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
    <span>Brand to Know &middot; New this summer &middot; Ships from the US and T&uuml;rkiye</span><span class="dot"></span>
    <span>All 19 products &middot; prices checked October 21, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="The white Saha oval logo floating over a golf course at sunset, from Saha&rsquo;s Instagram" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
    body += LOOKBOOK
    body += faq_html()
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Kalamunda", "Parmore", "Sounder", "Casualist", "BUNX", "Long Iron", "Dim Sum", "Rowena", "Metalwood", "Climber", "Woodgrain", "Rookline", "Bethpage", "LBB", "GolfPass"):
        if leak in above: bad.append("leak " + leak)
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
