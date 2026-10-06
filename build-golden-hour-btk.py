#!/usr/bin/env python3
"""build-golden-hour-btk.py — Brand to Know: Golden Hour (cloned from build-shoal-btk.py). 5 October 2026.
Lenny: "then we need to do a brand to know- https://goldenhourclubhouse.co.uk/", then on the options sheet
"expand it a little then build it" (recommended nine plus the Track Pant, Ripstop Pants and tote: twelve cards).
FACTS: catalogue, prices and stock from goldenhourclubhouse.co.uk/products.json on 5 Oct 2026
(research/golden-hour/products.json). Founder story and quotes verbatim from the brand's own blog post,
"How It All Started" (28 May 2025), signed Lewis & Louis. GBP shown first with approximate USD (GBP 1 = $1.34).
PHOTOS: Golden Hour's own store and homepage images, localised to /images/golden-hour.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"

TITLE = "Golden Hour: The UK Golf Brand Named for the Last Light"
DESC = ("Brand to Know: Golden Hour, a UK golf and streetwear label started in 2024 by two friends. Striped polos, "
        "heavy tees, track sets and ripstop, with prices.")
H1 = "Brand to Know: Golden Hour &mdash; Golf Clothes for the Last Light"
BC = "Golden Hour"
SLUG = "brand-to-know-golden-hour"
IMG = "/images/golden-hour"
SHOP = "https://goldenhourclubhouse.co.uk/products/"
A = "Golden Hour"
P = {
 "g01": (A, "Stripe Pique Polo", "&pound;49.99 (~$67)", "stripe-pique-polo",
   "This polo sums up the brand, with red and cream stripes on 100% cotton pique, a contrast collar and Goldenhour in script on the chest. The fit is relaxed and boxy, cut to wear untucked off the course. Only S and 2XL were left when we checked."),
 "g02": (A, "Heritage Polo", "&pound;49.99 (~$67)", "heritage-polo",
   "The Heritage is the quiet one. In navy 100% cotton with a cream contrast collar and a small Golden Hour script, it looks like an old clubhouse rugby shirt cut short. It works with pleated shorts on the course and jeans after. S and 2XL were in stock."),
 "g03": (A, "Clubhouse Waffle Polo", "&pound;45 (~$60)", "clubhouse-waffle-polo",
   "A brown waffle-knit polo with a structured collar, a cream logo on the chest and a large Golden Hour script printed across the back. It is a cotton, polyester and spandex blend, so it stretches through the swing and holds its shape. S and 2XL left."),
 "g04": (A, "Amen Corner Tee", "&pound;40 (~$54)", "amen-corner-tee",
   "Named for the stretch of holes everyone knows, in Augusta pine green. It is heavyweight 300gsm cotton with a small logo on the chest and a big Golden Hour graphic across the back. L and XL were in stock."),
 "g05": (A, "Golden Stripe", "&pound;40 (~$54)", "g",
   "A long-sleeve striped tee in 280gsm cotton with Golden Hour stitched across the chest in blue. The brand calls it a little cropped and says it is &ldquo;a true reflection of us as a brand and not just been a golf brand.&rdquo; Only 2XL was left."),
 "g06": (A, "Rugby Sweatshirt", "&pound;50 (~$67)", "rugby-sweatshirt",
   "A pale blue rugby-collar sweatshirt in 300gsm cotton with Golden Hour Studio stitched across a white chest band. A classic fit, true to size, and the best piece here for a cold morning tee time. S, M and 2XL were in stock."),
 "g15": (A, "Azalea Stripe Polo", "&pound;55 (~$74, sold out)", "azalea-stripe-polo",
   "The Masters polo: green and white stripes on soft 270gsm cotton, with embroidery on the collar and an azalea flower stitched on the back. It came out in April and has sold out."),
 "g16": (A, "GH Tee", "&pound;35 (~$47, sold out)", "gh-tee",
   "A white 280gsm cotton tee with the GH monogram printed on the chest and a large Golden Hour graphic across the back. Classic fit, true to size. Sold out for now."),
 "g17": (A, "Navy Essential Tee", "&pound;35 (~$47, sold out)", "essential-tee",
   "From the Major Season drop: navy 280gsm cotton with Golden Hour printed in white across the chest. The plainest tee in the line, and sold out for now."),
 "g18": (A, "Studio Tee", "&pound;35 (~$47, sold out)", "studio-tee",
   "A white 280gsm cotton tee from the Major Season drop, with Golden Hour on the front and the Studio sunburst logo on the back. Sold out for now."),
 "g19": (A, "The Pocket Tee", "&pound;35 (~$47, sold out)", "signiture-logo-long-sleeve-tee",
   "A black long-sleeve with a small chest mark and the big sunset Golden Hour print across the back, from the brand&rsquo;s 2024 collection. Sold out for now."),
 "g07": (A, "Lightweight Track Jacket", "&pound;70 (~$94)", "lightweight-track-jacket",
   "The jacket is navy nylon and spandex, light enough to stuff in a bag, with white piping, a baby blue mesh lining, a double zip and button cuffs. Golden Hour made it for early starts and breezy evening rounds, and it has the best size run here."),
 "g08": (A, "Lightweight Track Pant", "&pound;50 (~$67)", "lightweight-track-pant",
   "These trousers match the jacket, in the same stretchy nylon blend, with a single pleat, a straight leg and an elastic waist. Wear them together as a track suit or with a polo. Only 2XL was left; the jacket and trousers also come as a &pound;100 set."),
 "g11": (A, "The Ripstop Layer", "&pound;60 (~$80)", "the-links-layer",
   "A black half-zip in nylon ripstop with a light cotton fill, white contrast stitching and two front pockets. The collar stands up or folds down. It is the most streetwear piece in the line, and only size M was left."),
 "g12": (A, "The Ripstop Pants", "&pound;40 (~$54)", "the-links-pants",
   "Cut from the same cotton-filled ripstop as the half-zip, with a straight leg, toggles at the waist and hem, and a back pocket sized for a scorecard. Only 2XL was left."),
 "g14": (A, "Essential Crew Socks", "&pound;10 (~$13)", "essential-crew-socks",
   "White crew socks in a soft cotton-rich knit with a small Golden Hour logo on the side, the pair from the on-course photo up top. At &pound;10 they are the easiest add-on to any order."),
 "g10": (A, "Double Pleated Shorts", "&pound;50 (~$67)", "double-pleated-shorts",
   "Baggy, double-pleated shorts in a sandy cream polyester, bamboo and spandex blend that stays cool. The brand recommends sizing down or wearing a belt. Golden Hour pairs them with nearly every polo, and most sizes were in stock."),
 "g13": (A, "Golden Hour Tote Bag", "&pound;18 (~$24)", "golden-hour-tote-bag",
   "The tote is black nylon ripstop with a zip pocket on the front and a small Golden Hour mark. At &pound;18 it is the cheapest way into the brand, and big enough for shoes and a change of clothes."),
}
SECTIONS = [
 ("Polos and Rugby", "polos", ["g01","g02","g03","g15","g06"],
  "<strong>Five picks &middot; ~$60&ndash;$74</strong>The polos are where Golden Hour started and still what it does best. Two are 100% cotton with contrast collars, one in loud red stripes and one in quiet navy, and the third is a brown waffle knit with a big script logo across the back. The green Azalea Stripe Polo, the brand&rsquo;s Masters piece, is sold out, and the pale blue Rugby Sweatshirt brings the collar into 300gsm cotton for colder mornings. Sizes are running low on all of them."),
 ("Tees", "tees", ["g04","g05","g16","g17","g18","g19"],
  "<strong>Six picks &middot; ~$47&ndash;$54</strong>Heavy cotton, 280 to 300gsm, with the logo printed big across the back. The Amen Corner tee in pine green and the striped long-sleeve Golden Stripe are the two you can buy today. The other four come from earlier drops and are sold out, but they show where the brand started: the GH monogram tee, the navy Essential and Studio tees from the Major Season drop, and the black Pocket Tee with the sunset print from 2024."),
 ("Track and Ripstop", "track-and-ripstop", ["g07","g08","g11","g12"],
  "<strong>Four picks &middot; ~$54&ndash;$94</strong>These are two matching sets. The navy track jacket and trousers are a light nylon and spandex blend with white piping, the kind of suit you warm up in and keep on. The black ripstop half-zip and trousers are cotton-filled and stitched in white, closer to streetwear than golf. Wear either as a set or break them up with a polo."),
 ("Shorts, Socks and the Tote", "shorts-and-tote", ["g10","g14","g13"],
  "<strong>Three picks &middot; ~$13&ndash;$67</strong>The pleated shorts that turn up in nearly every Golden Hour photo, the white crew socks that go with them, and an &pound;18 ripstop tote to carry the shoes home in."),
]
N = 18
PQ = {
 "tees": ("Our vision is simple: to build a brand that seamlessly blends golf and lifestyle.", "Lewis &amp; Louis, Golden Hour"),
}
BANDS = {
 "polos": ("Photography &middot; Golden Hour&rsquo;s own", "Golden Hour shoots its polos at sunset on the course and in a moody clubhouse set.", [("band-1","A golfer in the red Stripe Pique Polo sitting on a bank by the fairway holding an iron","On the course"),("band-2","A golfer in the navy Heritage Polo and pleated shorts standing in a clubhouse beside golf bags","The clubhouse"),("band-3","A foot in a white crew sock and golf shoe mid-stride on the grass","The socks")]),
 "tees": ("Photography &middot; Golden Hour&rsquo;s own", "The brand shot the Azalea Stripe Polo, now sold out, and the Golden Patch cap on the range.", [("band-4","A golfer in a green and white striped long-sleeve polo","Azalea Stripe"),("band-5","A golfer swinging in the green striped polo","The swing"),("band-6","A golfer in the Heritage Polo and a Golden Patch cap with a jacket over his shoulder","The Heritage")]),
 "track-and-ripstop": ("Photography &middot; Golden Hour&rsquo;s own", "The track sets go out in the trees, and a windbreaker sits by the green.", [("band-7","A golfer in the navy track jacket and trousers leaning on a club by a fallen tree","The track set"),("band-8","A golfer in a black windbreaker sitting by his bag near a flag","By the green"),("band-9","A golfer from behind in a black long-sleeve with a sunset Golden Hour print","The back print")]),
 "shorts-and-tote": ("Photography &middot; Golden Hour&rsquo;s own", "The brand photographs its tees on its own crew, on the course and indoors.", [("band-10","Two men in Golden Hour tees, one seated on a wooden chair","The crew"),("band-11","A golfer in black standing on a wooden bridge on the course","The bridge"),("band-12","A man in a white Golden Hour tee sitting in a leather armchair holding a club","The armchair")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Golden Hour dresses golf like a clubhouse in a 1970s photograph: red and cream striped polos, contrast collars, pleated shorts and a lot of script logos. Two friends, Lewis and Louis, started it in the UK in 2024. It began as an Instagram page about golf and clothes, and the name came to them on a fairway at sunset. In their own words: &ldquo;The golden light hitting just right, the perfect moment of calm before the night set in&mdash;thats when the name came to us.&rdquo;</p>
    <p>It suits Austin better than most British golf brands, because it is built for the round that starts at six and ends in the dark. The polos are cotton and cut loose, the shorts are a cool bamboo blend, and the track jacket is light enough to throw in the bag for when the wind picks up on the back nine at Lions. The heavy tees and the rugby sweatshirt are for the few cold months and the patio after.</p>
    <h2 class="products-hdr btk-story-hdr">The Story</h2>
    <p>The founders tell it plainly on their site. They met through mutual friends in 2024 and &ldquo;clicked-sharing the same interests, the same passion for style, and the same love for golf.&rdquo; The Instagram page &ldquo;soon became a thriving community,&rdquo; and the brand followed. They were not sure at first whether it would be about golf or fashion, and settled on both. The post ends, &ldquo;Goldenhour is only getting started!&rdquo;</p>
    <p>On value, Golden Hour is cheap for what it is. Most pieces cost &pound;40 to &pound;50, about $54 to $67, for 100% cotton polos and 300gsm tees, and the track jacket is &pound;70. The Stripe Pique Polo and the Lightweight Track Jacket are the two to buy first. The catch is stock: the brand makes small runs, and most polos are down to S and 2XL, so check your size before you fall for a colour. Prices were read on Golden Hour&rsquo;s own store on 5 October 2026.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>United Kingdom</span></div>
      <div class="sidebar-detail"><span class="l">Founders</span><span>Lewis and Louis</span></div>
      <div class="sidebar-detail"><span class="l">Started</span><span>2024</span></div>
      <div class="sidebar-detail"><span class="l">Known for</span><span>Striped polos, pleated shorts and track sets</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>&pound;10&ndash;&pound;70 (~$13&ndash;$94)</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Stripe Pique Polo, &pound;49.99</span></div>
      <a href="https://goldenhourclubhouse.co.uk/" target="_blank" rel="noopener" class="sidebar-cta">Visit Golden Hour &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#GoldenHour</span>
        <span class="hashtag">#GolfStyle</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#GolfStreetwear</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("Who founded Golden Hour?", "Two friends, Lewis and Louis, who met through mutual friends in 2024. It started as an Instagram page about golf and fashion before they turned it into a clothing brand."),
 ("Where is Golden Hour based?", "In the United Kingdom. Its store, goldenhourclubhouse.co.uk, prices in pounds and also shows prices in US dollars and other currencies."),
 ("How much does Golden Hour cost?", "On 5 October 2026, from \u00a310 for crew socks and \u00a318 for the tote and \u00a340 for tees up to \u00a349.99 for the cotton polos and \u00a370 for the Lightweight Track Jacket, roughly $13 to $94."),
 ("Why is it called Golden Hour?", "The founders say the name came to them walking a fairway at sunset, when the light was golden and the course went calm before dark."),
 ("How does Golden Hour fit?", "Relaxed. The polos are boxy, the Double Pleated Shorts are baggy and the brand suggests sizing down or wearing a belt, and the Golden Stripe long-sleeve is slightly cropped. Several pieces list the model as 6ft 1in wearing a medium."),
]
FRN = json.loads((ROOT / "research/golden-hour/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-GH-GRID*/.products-grid[data-n="4"]{grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}'
            '@media(max-width:1024px){.products-grid[data-n="4"]{grid-template-columns:repeat(2,minmax(0,1fr))}}'
            '.products-grid[data-n="5"]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n="5"]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}'
            '@media(max-width:820px){.products-grid[data-n="5"]>.product-card{flex-basis:calc((100% - 24px)/2)}}'
            '@media(max-width:480px){.products-grid[data-n="4"]{grid-template-columns:1fr}.products-grid[data-n="5"]>.product-card{flex-basis:100%}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-10-05", "dateModified": "2026-10-05",
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
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Golf and streetwear from the UK</span><span class="dot"></span>
    <span>18 picks &middot; checked 5 October 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/btk-hero.jpg" alt="A golfer in a black Golden Hour windbreaker and cap sitting on the course with a flag behind him" fetchpriority="high" /></div></div>
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
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    bad = []
    for leak in ("Manors Revisited", "Nicklaus", "Enron"):
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
