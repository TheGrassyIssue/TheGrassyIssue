#!/usr/bin/env python3
"""build-no-dirt-golf-btk.py — Brand to Know: No Dirt Golf. Cloned from build-howie-benson-btk.py. 11 October 2026.
Lenny: "Let's do a brand to know- https://nodirtgolf.com/collections/all", then "go with your 12".
FACTS: nodirtgolf.com products JSON (research/no-dirt-golf/products-2026-10-11.json), home, About (/pages/contact),
Wholesale and refund-policy pages and two brand blog posts, read October 11, 2026. The site names no founder; the copy never
invents one. Lehi, Utah is the address in the refund policy. Wholesale claims are quoted as the brand's own.
PHOTOS: No Dirt Golf's own product, About and Wholesale images (frames in research/no-dirt-golf/frames.json).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "No Dirt Golf: The Golf Towel With the Club Brush Built In"
DESC = ("Brand to Know: No Dirt Golf, the Utah towel brand that sews a club brush into every towel. Twelve picks, from the "
        "$14.99 Range Rat to the $29.99 tour-size Ultimate Caddy Towel.")
H1 = "Brand to Know: No Dirt Golf &mdash; The Towel That Replaces the Brush"
BC = "No Dirt Golf"
SLUG = "brand-to-know-no-dirt-golf"
IMG = "/images/no-dirt-golf"
SHOP = "https://nodirtgolf.com/products/"
A = "No Dirt Golf"
UC = "the-ultimate-caddy-towel-"
P = {
 # The Ultimate Caddy Towel
 UC+"vaspar": (A, "Ultimate Caddy Towel, Valspar + Cream Stripes", "$29.99", UC+"vaspar",
   "Our pick. A muted olive green with a band of cream stripes at one end, the color of a fairway in late summer. It is the tour-size towel, 44 by 22 inches, big enough to drape over the irons in the rain, with the non-abrasive scrub pad woven into one corner. It looks like it came out of a caddie shack, not a gift shop."),
 UC+"dutch-boy": (A, "Ultimate Caddy Towel, Cream + Chocolate Stripes", "$29.99", UC+"dutch-boy",
   "Cream with chocolate-brown stripes, the warmest towel in the range and the one to hang on a tan or brown carry bag. The textured weave lifts dirt rather than smearing it, which matters more on a light towel than a dark one."),
 UC+"white-burgundy-and-yellow-stripes": (A, "Ultimate Caddy Towel, White + Burgundy and Gold Stripes", "$29.99", UC+"white-burgundy-and-yellow-stripes",
   "White with thin burgundy and gold stripes, one of the newer colorways. It has the look of an old club towel with the member colors running across the bottom."),
 UC+"burgundry-silver-stripes": (A, "Ultimate Caddy Towel, Burgundy + Silver Stripes", "$29.99", UC+"burgundry-silver-stripes",
   "A deep burgundy body with silver stripes. Dark enough to hide a round of mud between washes, and the color we would hang on a navy or black bag for fall."),
 UC+"green-white-stripe": (A, "Ultimate Caddy Towel, Green + Light Blue Stripe", "$29.99", UC+"green-white-stripe",
   "Bottle green with a pale blue stripe. It is the most traditional-looking towel on the page, and the one that sits best next to a tartan or tweed headcover."),
 UC+"navy-white-stripe": (A, "Ultimate Caddy Towel, Navy + White Stripe", "$29.99", UC+"navy-white-stripe",
   "Navy with white stripes, the safe pick that goes with every bag. Same 44 by 22 inch size and built-in scrub pad as the rest of the Ultimate Caddy line."),
 # The Classic
 "the-classic-forest-green": (A, "The Classic, Forest Green", "$25.99", "the-classic-forest-green",
   "A longer, narrower 16 by 39 inch waffle-weave microfiber with a bristle brush stitched into one corner and a loop handle to hang it from the bag. The brand says its microfiber holds water longer than a regular towel, which makes it the one to wet at the turn on a dry August day."),
 "the-classic-navy": (A, "The Classic, Navy", "$25.99", "the-classic-navy",
   "The Classic in navy with a contrast blue edge. The brush sits in a black triangle in the corner; fold it over, scrub the grooves, flip it back and dry the face."),
 "the-classic-irish-mint": (A, "The Classic, Irish Mint", "$25.99", "the-classic-irish-mint",
   "A pale mint that looks good against a white or cream bag. Same waffle microfiber and corner brush as the other Classics. Several of the Classic colors and all four printed versions were sold out when we checked, so this is one of the few lighter shades still in stock."),
 # The small ones
 "magnet-towel-dark-green": (A, "Magnet Towel, Dark Green", "$23.99", "magnet-towel-dark-green",
   "A smaller microfiber towel with a strong magnet in a clip at the top, so it sticks to a cart frame or the head of an iron instead of hanging off the bag. The cleaning pad sits in the bottom corner. Best for players who ride."),
 "magnet-towel-navy": (A, "Magnet Towel, Navy", "$23.99", "magnet-towel-navy",
   "The Magnet Towel in navy. It does the same job as the Classic in a smaller size and grabs onto anything metal, so it is always within reach on a cart."),
 "the-r-green": (A, "The Range Rat, Green", "$14.99", "the-r-green",
   "The cheapest way into No Dirt and the one we would buy first for an Austin muni. A compact 16 by 12 inch towel with a full-bristle brush pad and a carabiner, small enough for a back pocket, a caddie bib or a carry-bag strap. The brand says it was built for the range and for caddies who want cleaning power without a full-size towel."),
}
SECTIONS = [
 ("The Ultimate Caddy Towel", "caddy", [UC+"vaspar",UC+"dutch-boy",UC+"white-burgundy-and-yellow-stripes",UC+"burgundry-silver-stripes",UC+"green-white-stripe",UC+"navy-white-stripe"],
  "<strong>Six picks &middot; $29.99</strong>The tour-size towel, 44 by 22 inches, with a non-abrasive scrub pad built into one corner and a band of stripes across one end. There are 25 colorways; these are the six that look most like a towel from an old club."),
 ("The Classic", "classic", ["the-classic-forest-green","the-classic-navy","the-classic-irish-mint"],
  "<strong>Three picks &middot; $25.99</strong>The longer, narrower towel: 16 by 39 inches of waffle-weave microfiber with a bristle brush in the corner and a loop handle."),
 ("The Magnet Towel and the Range Rat", "small", ["magnet-towel-dark-green","magnet-towel-navy","the-r-green"],
  "<strong>Three picks &middot; $14.99&ndash;$23.99</strong>Two smaller towels: one that sticks to a cart or an iron with a magnet, and a pocket-size towel with a full-bristle brush for the range."),
]
N = 12
PQ = {
 "caddy": ("The golf towel you didn&rsquo;t know you needed until now.", "No Dirt Golf, About page"),
 "small": ("The thing doesn&rsquo;t clean, it just smears mud around like a toddler with finger paint.", "No Dirt Golf, on the old golf brush"),
}
CAP = "Photography &middot; No Dirt Golf&rsquo;s own"
BANDS = {
 "caddy": (CAP, "On the course, at the beach and on the grass.", [("band-1","A caddie in a white No Dirt bib holding the flagstick on a green while a golfer putts","The caddie"),("band-2","A gray No Dirt Classic towel hanging on a rail above a beach","The beach"),("band-3","A blue No Dirt waffle towel with its woven label lying on grass","The weave")]),
 "small": (CAP, "Custom towels from No Dirt&rsquo;s wholesale page, made for golf clubs.", [("band-4","A white custom No Dirt towel printed with puffins and the Bandon Dunes name","Bandon Dunes"),("band-5","A navy custom No Dirt towel printed with a repeating white crest","National Golf Links of America"),("band-6","A gray custom No Dirt towel printed with the Sheep Ranch logo","Sheep Ranch")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Most golf bags carry two things to do one job: a towel that gets soggy by the back nine and a brush that hangs off the side collecting mud. No Dirt Golf puts them together. Every towel has a cleaning pad sewn into one corner, a scrub pad on the big caddie towels and a bristle brush on the rest, so the grooves get cleaned with the same thing that dries the face. It is a small idea, done properly, and the brand says it was the first to bring it to market.</p>
    <p>The reason it earns a Brand to Know is the Ultimate Caddy Towel. It is tour size, 44 by 22 inches, in a textured weave with a band of stripes at one end, and in the right colors it looks like something from the caddie shack at an old club, not an impulse buy at the pro-shop register. Valspar green with cream, cream with chocolate, burgundy with silver: they sit quietly on a carry bag and cost $29.99, less than most logo towels. For an Austin muni walker, start smaller. The Range Rat is $14.99, clips to a bag strap or a back pocket, and does the job of a towel and a brush for the price of one.</p>
    <h2 class="products-hdr btk-story-hdr">The Brand</h2>
    <p>No Dirt Golf launched in January 2023 in Lehi, Utah, with the stated goal &ldquo;to enrich the player experience.&rdquo; It does not name a founder on its site. Much of its business is wholesale: the brand says it has taken orders from &ldquo;40+ top 100 golf clubs in America&rdquo; and has over 3,000 accounts, and its wholesale page shows custom towels for Bandon Dunes, National Golf Links of America and Sheep Ranch. It also makes collaboration towels, including the caddie towel on our <a href="/drops/brand-to-know-shoal-golf">Shoal Golf Co. Brand to Know</a>. Shipping in the US is free over $50. All 12 towels below were in stock on nodirtgolf.com on October 11, 2026.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Lehi, Utah</span></div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>2023</span></div>
      <div class="sidebar-detail"><span class="l">Known for</span><span>Towels with a built-in club brush</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>Four towels, 50+ colors</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$14.99&ndash;$29.99</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Ultimate Caddy, Valspar + Cream, $29.99</span></div>
      <a href="https://nodirtgolf.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit No Dirt Golf &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#NoDirtGolf</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#GolfTowel</span>
        <span class="hashtag">#CaddyTowel</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("Where is No Dirt Golf from?", "Lehi, Utah, the address on its store policies. The brand launched in January 2023."),
 ("Who founded No Dirt Golf?", "The brand does not name a founder on its site."),
 ("What is the Ultimate Caddy Towel?", "No Dirt Golf's tour-size towel: 44 by 22 inches, a textured weave with a band of stripes at one end and a non-abrasive scrub pad built into one corner for cleaning grooves. It was $29.99 in 25 colorways on October 11, 2026."),
 ("How much does No Dirt Golf cost?", "On October 11, 2026, the Range Rat was $14.99, the Magnet Towel $23.99, the Classic $25.99 ($27.99 for prints) and the Ultimate Caddy Towel $29.99. US shipping is free over $50."),
 ("Can No Dirt Golf make custom towels?", "Yes. The brand makes custom logo towels for golf clubs and says it has more than 3,000 wholesale accounts. Its blog says individual towels can also be customized with a name or logo."),
]
FRN = json.loads((ROOT / "research/no-dirt-golf/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-ND-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
    og = f"https://thegrassyissue.com{IMG}/btk-og.jpg"
    items, pos = [], 1
    for sec in SECTIONS:
        for h in sec[2]:
            items.append({"@type": "ListItem", "position": pos, "url": SHOP + P[h][3], "name": H.unescape(f"{P[h][0]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-10-11", "dateModified": "2026-10-11",
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
<link rel="preload" as="image" href="{IMG}/btk-hero.jpg" />
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
    <span>Golf towels with a built-in club brush &middot; Lehi, Utah</span><span class="dot"></span>
    <span>12 picks &middot; all in stock, checked October 11, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/btk-hero.jpg" alt="No Dirt Golf Ultimate Caddy Towels in cream, burgundy, green, gray, white and orange laid out on a fairway" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
    body += faq_html()
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Kalamunda", "Howie", "Rookline", "Bethpage", "Hudson", "LBB", "GolfPass"):
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
