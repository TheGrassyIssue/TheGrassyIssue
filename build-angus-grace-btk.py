#!/usr/bin/env python3
"""build-angus-grace-btk.py — Brand to Know: Angus & Grace Go Golfing (Sydney). 30 October 2026.
Cloned from build-pinned-btk.py. Lenny: "a brand to know - angusandgracegogolfing.com/collections/mens" -> options sheet (53)
-> "Let's build it, need some great lookbook images and good quotes". Colorways consolidated into one box each; 21 boxes in rows of 3.
FACTS: brand about + stockists pages; product copy read in Chrome 30 Oct 2026 (AUD; ~USD at x0.70 as on the Mount Tee post);
The Old Ghosts, "Making It Look Good with Angus and Grace", Michael Williams, Apr 24 2025 (Matthew Burns: UTS fashion degree,
five years as a tailor at P. Johnson; quotes); AGM Golf Vendor Spotlight, Mar 16 2026 (name, Golf Daddy origin, made to order,
"Neutral but impactful"); No Laying Up Pro Shop NLU x AAGGG collection (USD). Lookbook: Take Studios Jan 2025, Chad Konik Feb 2024,
NLU shoot, all hosted on the brand's own store. No FAQ. Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Brand to Know: Angus & Grace Go Golfing, the Sydney Label Named for Two Westies"
DESC = ("Angus & Grace Go Golfing is a Sydney golf label from former P. Johnson tailor Matthew Burns, named for his two West Highland "
        "terriers. Polos, knits, shorts, trousers and GOLF DADDY caps, with prices.")
H1 = "Brand to Know: Angus &amp; Grace Go Golfing"
BC = "Brand to Know: Angus &amp; Grace Go Golfing"
SLUG = "brand-to-know-angus-and-grace-go-golfing"
IMG = "/images/angus-grace-go-golfing"
SHOP = "https://angusandgracegogolfing.com/products/"
C = "Angus &amp; Grace Go Golfing"
def A(a): return f"A${a} (~${round(a * 0.70)})"
P = {
 "upf": (C, "UPF 50+ Short Sleeve Polo", A(160), "upf-50-mens-short-sleeve-polo-2",
   "Our pick. The polo AAGGG builds the rest of the range around: UPF 50+ fabric, a straight cut and a small swinging-golfer logo on the sleeve instead of a chest logo. Five colors: navy, mint blue, green, white and steel blue."),
 "knit": (C, "3 Button Knit Polo", A(160), "3-button-knit-polo-navy-1",
   "This is the piece that shows the tailoring background. 100% cotton knit, straight cut, with a ribbed collar, cuffs, hem and a three-button placket. Navy, stone, light blue and cream. It looks as right at dinner as it does on the first tee."),
 "cashpolo": (C, "Men&rsquo;s Cashmere Polo", A(400), "mens-cashmere-polo",
   "A long sleeve cashmere polo in charcoal. The most expensive top in the men&rsquo;s collection and the one that best fits Burns&rsquo; idea of a single wardrobe for golf and everything else."),
 "gdtee": (C, "GOLF DADDY Tee", A(80), "golf-daddy-tee-shirt-navy",
   "The sub-brand that started as a Father&rsquo;s Day joke, on a classic tee with GOLF DADDY embroidered on the left chest. Steel and two versions of navy."),
 "heavy": (C, "Heavyweight Tee", A(80), "heavyweight-tee-shirt-navy-1",
   "A plain navy tee in 300gsm cotton jersey with a ribbed neck and a straight cut. No logo on the front, which is the point."),
 "crew": (C, "Knit Crewneck", "From " + A(180), "knit-crewneck-navy-1",
   "100% wool, an easy straight cut and ribbed neckline, cuffs and hem. Navy at A$220 and stone at A$180. The layer for an early tee time."),
 "hoodie": (C, "Men&rsquo;s Cashmere Hoodie", A(450), "mens-cashmere-hoodie",
   "A charcoal cashmere hoodie, the top of the price range. It is the clearest case of a golf brand making something you would wear on a Sunday with no clubs involved."),
 "coach": (C, "Coach Jacket", A(440), "wet-weather-jacket-navy-1",
   "A waterproof jacket with storm shields, a two-way zipper, a proper collar and ribbed hem and cuffs. Olive and navy. It reads like a coach jacket, not a rain shell."),
 "puffer": (C, "Men&rsquo;s Puffer Vest", A(440), "womens-puffer-vest-copy",
   "A quilted puffer vest in charcoal with a wave-stitched pattern and a high collar. The warmest piece in the men&rsquo;s range that still leaves your arms free to swing."),
 "fleece": (C, "Men&rsquo;s Reversible Fleece Vest", A(360), "reversible-fleece-vest-navy-1",
   "Waterproof fabric on one side and fleece on the other, with a two-way zipper, two zipped waterproof pockets, a high collar and elasticated hem and armholes. Navy."),
 "shorts": (C, "Men&rsquo;s Shorts", A(220), "shorts-navy-new-1",
   "Mid rise, straight cut and two inches above the knee, with side seam pockets and an inverted box pleat with a flap back pocket. Seven colors: navy, beige, stone, blue steel, dark brown, cream and olive. AAGGG says the waist runs generous, so size down if in doubt."),
 "trouser": (C, "Men&rsquo;s Trouser", A(250), "trouser-navy-new-1",
   "The long version of the shorts: mid rise, straight cut, side seam pockets and the same pleated flap back pocket, in 100% polyester. Six colors: navy, beige, cream, dark green, green and charcoal. Same note on the waist."),
 "gdcap": (C, "GOLF DADDY Cap", A(60), "golf-daddy-cap-2",
   "The cap that made the sub-brand. GOLF DADDY in orange on yellow, green trucker mesh and beige, plus green and pink seersucker versions on pre-order."),
 "gdaaggg": (C, "GOLF DADDY + AAGGG Cap", A(60), "golf-daddy-aaggg-cap-copy",
   "GOLF DADDY over a small AAGGG label. Blue-on-blue stripe seersucker, or washed denim with a brown suede brim."),
 "dogs": (C, "AAGG Dogs Cap", A(60), "aagg-dogs-cap-copy",
   "A faux suede cap with the dogs themselves, Angus and Grace, embroidered tone on tone. Navy or washed gray."),
 "fivepanel": (C, "GOLF DADDIES 5 Panel Cap", A(60), "golf-daddy-cap-1",
   "A five-panel cap with a GOLF DADDIES patch of two golfers, in light blue with a suede brim or yellow with mesh."),
 "visor": (C, "AAGGG Visor", A(60), "aaggg-visor-navy-1",
   "100% nylon with AAGGG in 3D embroidery across the front. Navy or cream."),
 "bucket": (C, "AAGGG Bucket Hat", A(60), "aaggg-bucket-hat",
   "A light blue bucket hat with the full name stitched across the front. The one to pack for a links trip."),
 "fliers": (C, "The Fliers Club Cap", A(60), "the-fliers-club-cap-1",
   "Made with The Fliers Club: a cotton canvas cap with The Fliers Club&rsquo;s embroidered emblem, in light blue or white."),
 "flierspolo": (C, "The Fliers Club UPF 50+ Long Sleeve Polo", "A$60 (~$42), down from A$160", "the-fliers-club-upf-50-long-sleeve-polo-navy-1",
   "The long sleeve version of the UPF polo with The Fliers Club patch on the chest, in navy. Cut from A$160 to A$60, the best price on the site right now."),
 "agp": (C, "Australian Golf Passport Tee", A(80), "australian-golf-passport-tee-shirt-pre-order",
   "Merch for the Australian Golf Passport podcast: a slate blue tee with a small golfer on the chest and a tour-style list of courses on the back. A pre-order that ships November 9 to 20."),
}
SECTIONS = [
 ("Polos, Tees and Knits", "polos", ["upf", "knit", "cashpolo", "gdtee", "heavy", "crew"],
  "<strong>Six pieces &middot; A$80&ndash;A$400</strong>The UPF polo, the cotton knit and the GOLF DADDY tee do most of the work. Prices in Australian dollars, with US dollars at about 70 cents."),
 ("Layers, Shorts and Trousers", "layers", ["hoodie", "coach", "puffer", "fleece", "shorts", "trouser"],
  "<strong>Six pieces &middot; A$220&ndash;A$450</strong>Weatherproof layers that do not look technical, and one pair of shorts and one pair of trousers in thirteen colors between them."),
 ("Caps, Visors and a Bucket", "caps", ["gdcap", "gdaaggg", "dogs", "fivepanel", "visor", "bucket"],
  "<strong>Six styles &middot; all A$60</strong>Every hat costs the same. GOLF DADDY in four versions, the dogs, a visor and a bucket."),
 ("The Collabs", "collabs", ["fliers", "flierspolo", "agp"],
  "<strong>Three pieces &middot; A$60&ndash;A$80</strong>Made with The Fliers Club and the Australian Golf Passport podcast."),
]
N = 21
PQ = {
 "layers": ("I don&rsquo;t think golf clothing needs to exist in its own category. I want one wardrobe.", "Matthew Burns, founder, to The Old Ghosts"),
 "caps": ("It actually started as something fun we did around Father&rsquo;s Day a few years ago and it took off!", "AAGGG on GOLF DADDY, to AGM Golf"),
}
BANDS = {
 "polos-after": ("The lookbook", "From AAGGG&rsquo;s January 2025 lookbook, shot by Take Studios.",
   [("band-1-1", "A man in a dark brown short sleeve pocket polo against a white wall", "The pocket polo"),
    ("band-1-2", "A man in a brown zip vest over a cream long sleeve polo and a white visor", "Vest and visor"),
    ("band-1-3", "A hand in the pocket of cream pleated trousers with a small navy AAGGG label", "The trouser pocket")]),
 "layers-after": ("On the course", "AAGGG out of the studio: a cart, a fairway and the umbrella.",
   [("band-2-1", "A long-haired golfer in a navy cap and white pocket polo stepping out of a golf cart", "From the No Laying Up shoot"),
    ("band-2-2", "Two golfers on a wide green fairway pointing toward a cart under a big sky", "That way"),
    ("band-2-3", "A plaid umbrella and a gray sweater with a golfer graphic lying on the grass", "The umbrella and the jumper")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Angus &amp; Grace Go Golfing makes the kind of golf clothes you forget are golf clothes. There are no big logos, no technical seams and no loud prints. It is a tight range of polos, knits, shorts and trousers in navy, stone, olive and brown, cut by a former tailor, and a run of caps that do the joking for everything else. Angus and Grace, for anyone wondering, are founder Matthew Burns&rsquo; two West Highland White Terriers.</p>
    <p><strong>The clothes.</strong> Burns spent five years as a tailor at P. Johnson in Sydney, and it shows in the details. The shorts and trousers share one pattern: mid rise, straight cut, side seam pockets and an inverted box pleat with a flap on the back pocket. The knit polo is 100% cotton with a ribbed collar and a three-button placket. The UPF 50+ polo, which we would buy first, swaps the chest logo for a small swinging golfer on the sleeve. &ldquo;Neutral but impactful is always the goal,&rdquo; the brand told AGM Golf, and that sentence covers most of the range.</p>
    <p><strong>The caps.</strong> GOLF DADDY started as a Father&rsquo;s Day idea and turned into a sub-brand, on caps, tees and a five-panel with a patch of two golfers. Every hat on the site costs A$60. They are the playful half of a brand whose name was chosen, in its own words, to feel a little playful and not take itself too seriously.</p>
    <p><strong>Buying it in the US.</strong> The site prices everything in Australian dollars, so a A$160 polo comes to about $112. AAGGG has also made exclusive pieces with No Laying Up, sold in US dollars through the NLU Pro Shop, including mock necks, pocket polos and the GOLF DADDY hat. If you are in Sydney, the shop at 39 William Street in Paddington has a putting area and old golf films on a projector.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">At a Glance</div>
      <div class="sidebar-detail"><span class="l">Founder</span><span>Matthew Burns</span></div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Paddington, Sydney</span></div>
      <div class="sidebar-detail"><span class="l">Shop</span><span>39 William St, Paddington</span></div>
      <div class="sidebar-detail"><span class="l">Named for</span><span>Two Westies, Angus and Grace</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>A$60&ndash;A$450</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>UPF 50+ Short Sleeve Polo</span></div>
      <div class="hashtags">
        <span class="hashtag">#AAGGG</span>
        <span class="hashtag">#GolfDaddy</span>
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
  <h2 class="products-hdr" id="story">One Wardrobe, With an Option for Golf</h2>
  <div class="writeup-body">
    <p>Matthew Burns studied fashion at the University of Technology Sydney and then spent five years as a tailor at P. Johnson, the Sydney tailoring house. &ldquo;That place was an education in itself,&rdquo; he told The Old Ghosts in 2025. The customers, he said, taught him as much as the work did.</p>
    <p>When he started his own label, he named it after his dogs. &ldquo;I wanted the name to feel a little playful and not take itself too seriously,&rdquo; the brand told AGM Golf. &ldquo;Golf can sometimes feel quite traditional, so having something lighthearted felt right.&rdquo; The clothes went the other way: clean, classic and minimal, in what the brand calls harmonious capsule collections.</p>
    <p>The idea behind them is simple. &ldquo;I don&rsquo;t think golf clothing needs to exist in its own category,&rdquo; Burns said. &ldquo;I want one wardrobe&mdash;you should be able to hug your friends, go on hot dates, hit the pub, go to work, or play a round of golf, all in the same clothes.&rdquo; On design, he talks about purpose more than style: &ldquo;It&rsquo;s the practical details&mdash;whether it&rsquo;s fabric or pockets&mdash;that give a piece purpose. Garments with purpose become your best friends, because they work with you.&rdquo;</p>
    <p>The business now has three parts. There is the shop on William Street in Paddington, with stockists at Playfair Golf and Goods in Randwick and Mulligans Clubmakers in Armadale, Melbourne. There is the online store. And there is a made-to-order program for golf clubs, which ships straight from the factories to the club. &ldquo;Do not be shy!&rdquo; the brand told club buyers. &ldquo;We can go as bold and creative as you like, or keep things very classic and understated.&rdquo;</p>
    <p>As for his own game, Burns is relaxed about it. &ldquo;I feel like I always hit it well and score poorly,&rdquo; he said. &ldquo;I&rsquo;m not trying to win the US Open, so I may as well try and make it look good. No one cares what I shoot!&rdquo;</p>
  </div>
</section>
"""
FAQ = []
LOOKBOOK = ""
FRN = json.loads((ROOT / "research/angus-grace/frames.json").read_text())
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
    <span>Brand to Know &middot; Sydney, Australia</span><span class="dot"></span>
    <span>21 pieces, every colorway in one box &middot; checked October 30, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Founder Matthew Burns standing in the doorway of the Angus and Grace Go Golfing shop on William Street, Paddington" fetchpriority="high" /></div></div>
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
