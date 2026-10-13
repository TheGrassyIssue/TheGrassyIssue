#!/usr/bin/env python3
"""build-parmore-btk.py — Brand to Know: Parmore Golf. Cloned from build-woodgrain-btk.py. 12 October 2026.
Lenny: "We need to do a brand to know Parmore", then "run all 18 and 3 of the loudest best sold out options that are interesting".
FACTS: parmoregolf.com products (research/parmore/catalog.py), About Us (House Rules + FAQ) and Our Story pages, meta.json
(Bournemouth, England; store currency GBP), read October 12, 2026. GBP prices from products.js?currency=GBP; US visitors are
charged separate USD prices, shown second. No founder names on the site, none invented. Quotes verbatim.
PHOTOS: Parmore's own real photos only. Several product images are AI-generated (file names ChatGPT / Kive.ai / Generated
Image); none are used. The ball marker has only an AI image, so it is listed in the text, not as a card (17 cards + 3 sold out).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Parmore Golf: The UK Streetwear Golf Brand With No Membership Required"
DESC = ("Brand to Know: Parmore Golf, the English streetwear golf label behind \"No Membership Required.\" "
        "Every in-stock piece, from £10 grip socks to a £90 weatherproof quarter-zip, plus three sold-out standouts.")
H1 = "Brand to Know: Parmore Golf &mdash; No Membership Required"
BC = "Parmore Golf"
SLUG = "brand-to-know-parmore-golf"
IMG = "/images/parmore"
SHOP = "https://parmoregolf.com/products/"
A = "Parmore Golf"
def gb(g, u): return f"&pound;{g} &middot; US ${u}"
P = {
 # Layers
 "camo-1-4-zip-rebrand": (A, "Camo Quarter-Zip", gb(65, 100), "camo-1-4-zip-rebrand",
   "Parmore calls it the boldest piece in the range, and it is: a realistic hunting camo in browns and greens with a huge white collegiate PARMORE arched across the chest. It sits closer to a deer stand than a pro shop, which is exactly the point. S to XXL in stock."),
 "green-1-4-zip-rebrand": (A, "Varsity Quarter-Zip", gb(90, 140), "green-1-4-zip-rebrand",
   "The most technical thing they make: a wind- and water-resistant pullover in bottle green with cream varsity stripes at the collar and cuffs, a kangaroo pocket, a drawcord hem and a mesh-vented back. The white &ldquo;+&rdquo; on the upper back is the capsule&rsquo;s symbol, shared with the polos and the windbreaker."),
 "long-sleeved-windbreaker-rebrand": (A, "Capsule Windbreaker", gb(75, 115), "long-sleeved-windbreaker-rebrand",
   "A khaki-stone pullover with cream ribbed trim, white piping along the raglan seams, zip hand pockets and a mesh liner. Small &ldquo;+&rdquo; on the chest, the Parmore wordmark on the back. The cleanest layer on the page."),
 "brown-zip-windbreaker-rebrand": (A, "Colourblock Swing Shirt", gb(70, 110), "brown-zip-windbreaker-rebrand",
   "A short-sleeved full-zip layer in what Parmore calls Coffee Liqueur brown over a grey-olive bottom half. Baggy, drawstring at the hem, logo front and back. Built to throw on over a tee when the forecast cannot decide, and leave on after."),
 # Polos and paneled tees
 "brown-stripes-polo-rebrand": (A, "Stripe Polo, Brown &amp; Cream", gb(50, 78), "brown-stripes-polo-rebrand",
   "A boxy three-button polo in brown and cream stripes with a solid brown collar and cuffs, a white &ldquo;+&rdquo; on the chest and a tiny Parmore on the cuff. A heavier 240gsm knit, so it works on a cold morning too. Our pick."),
 "green-stripes-polo-rebrand": (A, "Stripe Polo, Olive &amp; White", gb(50, 78), "green-stripes-polo-rebrand",
   "The same relaxed polo in olive and cream stripes with the brown collar. Parmore shot it outside the Houses of Parliament with a carry bag over one shoulder, which tells you how far from the clubhouse they want it to go."),
 "red-paneled-tee-rebrand": (A, "Paneled Tee, Red", gb(45, 70), "red-paneled-tee-rebrand",
   "A cardinal red cotton pique tee with white side panels and raglan seams: a retro sports-jersey shape with a small Parmore on the chest. True to size."),
 "grey-paneled-tee-rebrand": (A, "Paneled Tee, Charcoal", gb(45, 70), "grey-paneled-tee-rebrand",
   "The same jersey tee in charcoal with white panels, which Parmore points out is easier to keep clean off the course. Pique cotton, regular fit."),
 # Graphic tees and hoodie
 "parm-050": (A, "No Membership Required Tee", gb(40, 62), "parm-050",
   "The brand&rsquo;s slogan at its loudest: a photo of a golfer on a sunlit fairway printed on the chest, with &ldquo;No Membership Required&rdquo; in Parmore lime across it. A heavyweight 240gsm faded white tee, boxy with dropped shoulders. XS to 3XL."),
 "parm-043": (A, "Drop-Shoulder Graphic Tee", gb(40, 62), "parm-043",
   "Faded bone 240gsm cotton with a navy Parmore wordmark, the &ldquo;no membership required&rdquo; tag and small flag and dot graphics. Sporty without going full football shirt. Slightly oversized."),
 "parm-042": (A, "Motorsport Tee", gb(40, 62), "parm-042",
   "Black heavyweight cotton with a small red italic PARmore racing-style wordmark. The quietest piece in the motorsport family, which also includes the hoodie and the camo trucker. Every size but M in stock."),
 "parm-038": (A, "Minimal Tee", gb(35, 55), "parm-038",
   "One small navy Parmore on the chest of a faded white 240gsm tee, and nothing else. Boxy, roomy through the arms and chest. The cheapest way into the brand that still looks like it."),
 "parm-049": (A, "Motorsport Hoodie", gb(65, 100), "parm-049",
   "A boxy 350gsm black hoodie with a red italic &ldquo;parmore&rdquo; across the chest, a fleece-lined inside and a kangaroo pocket. Parmore pitches it as an off-course layer that doubles as a cold-morning throw-on before a round."),
 # Bottoms, caps, socks
 "casual-pants-black": (A, "Cargo Pants, Black", gb(65, 100), "casual-pants-black",
   "Parmore is upfront that this is a street cargo, not a golf trouser: elasticated waist, tonal panels at the yoke, cargo pockets, a tapered leg and toggle-cinched ankles, with Parmore on the thigh pocket. It is what the brand wears with every polo above. S, M and XL left; the grey pair is sold out."),
 "parm-044": (A, "Camo Trucker Cap", gb(35, 55), "parm-044",
   "A black crown with a camo brim and a bold white PARmore on the front. Parmore calls it the loudest cap in the lineup. It matches the camo quarter-zip if you want to go all the way."),
 "parmore-embroidered-5-panel": (A, "Ripstop 5-Panel", gb(35, 55), "parmore-embroidered-5-panel",
   "The capsule&rsquo;s &ldquo;+&rdquo; mark in raised 3D embroidery on a warm charcoal ripstop cotton cap, with Parmore on the side and a shorter brim. Easier to wear than the trucker, and the one we would buy first."),
 "active-grip-socks": (A, "Active Grip Socks", gb(10, "15.50"), "active-grip-socks",
   "Mid-length socks with rubber grippers on the sole to stop your foot sliding in the shoe through the swing, and the Parmore logo knitted in rather than printed. Black or white, one size."),
 # Sold out
 "zip-up-camo-jacket-rebrand": (A, "Hooded Camo Shell", "&pound;85 &middot; sold out", "zip-up-camo-jacket-rebrand",
   "A full-zip hooded shell in a dark, smoky camo with Parmore running down the front zip. Parmore lists it as the Tie-Dye Hooded Jacket. Sold out in every size when we checked."),
 "zip-up-fleece-rebrand": (A, "Sherpa Teddy Fleece", "&pound;75 &middot; sold out", "zip-up-fleece-rebrand",
   "Olive sherpa with a giant cream &ldquo;PGA&rdquo; monogram on the back and &ldquo;Parmore Golf Apparel&rdquo; underneath. Yes, the initials are the joke. The best piece the brand has made, and gone in every size."),
 "pod-rebrand-hoodie-1": (A, "Varsity Heritage Hoodie", "&pound;65 &middot; sold out", "pod-rebrand-hoodie-1",
   "A grey hoodie with a cream varsity-script Parmore and crest on the chest. The heritage family also had a matching trucker cap and tee, all sold out."),
}
SECTIONS = [
 ("The Layers", "layers", ["camo-1-4-zip-rebrand", "green-1-4-zip-rebrand", "long-sleeved-windbreaker-rebrand", "brown-zip-windbreaker-rebrand"],
  "<strong>Four picks &middot; &pound;65&ndash;&pound;90</strong>Two quarter-zips, a windbreaker and a short-sleeved swing shirt. This is where Parmore does its best work."),
 ("Stripe Polos and Paneled Tees", "polos", ["brown-stripes-polo-rebrand", "green-stripes-polo-rebrand", "red-paneled-tee-rebrand", "grey-paneled-tee-rebrand"],
  "<strong>Four picks &middot; &pound;45&ndash;&pound;50</strong>Boxy striped polos with a contrast collar and two retro jersey-style tees."),
 ("Graphic Tees and the Hoodie", "tees", ["parm-050", "parm-043", "parm-042", "parm-038", "parm-049"],
  "<strong>Five picks &middot; &pound;35&ndash;&pound;65</strong>Heavyweight 240gsm cotton tees, from a single small logo to the full &ldquo;No Membership Required&rdquo; photo print."),
 ("Cargos, Caps and Socks", "extras", ["casual-pants-black", "parm-044", "parmore-embroidered-5-panel", "active-grip-socks"],
  "<strong>Four picks &middot; &pound;10&ndash;&pound;65</strong>A street cargo, two caps and grip socks. Also in stock and not pictured: a nickel ball marker with the Parmore box logo, &pound;8."),
 ("Sold Out, But Loud", "sold-out", ["zip-up-camo-jacket-rebrand", "zip-up-fleece-rebrand", "pod-rebrand-hoodie-1"],
  "<strong>Three that are gone &middot; watch for a restock</strong>The loudest things Parmore has made so far, all sold out on October 12, 2026. They are here because they show where the brand is heading."),
]
N = 20
PQ = {
 "layers": ("Golf has a culture problem. Not a performance problem.", "Parmore Golf, Our Story"),
 "tees": ("We&rsquo;re building a community, not a country club.", "Parmore Golf, House Rules"),
}
CAP = "Photography &middot; Parmore Golf&rsquo;s own"
BANDS = {}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Parmore Golf is a streetwear brand that happens to be about golf, not a golf brand trying to look like streetwear. It started in England in 2024, it sells online only, and its whole pitch fits in three words printed on half the range: No Membership Required. The clothes back it up: boxy heavyweight tees, a camo quarter-zip with PARMORE arched across the chest, a motorsport hoodie and cargo pants it openly says are not golf trousers.</p>
    <p>The best of it is the capsule built around a small &ldquo;+&rdquo; mark: the bottle green varsity quarter-zip, the piped khaki windbreaker and the two stripe polos. They look good on a muni and better at the pub after. If you only buy one thing, make it the brown and cream stripe polo at &pound;50. If you want the loud version, the camo quarter-zip and matching camo trucker are right there.</p>
    <h2 class="products-hdr btk-story-hdr">The Brand</h2>
    <p>Parmore says it started because its founders, &ldquo;not as a designer or a fashion people, but as people who play golf,&rdquo; could not find golf clothes they wanted to wear off the course. Its story page compares the plan to what Supreme did for skateboarding, and its ten House Rules run from &ldquo;No gatekeeping&rdquo; to &ldquo;Question everything.&rdquo; The store is based in Bournemouth and ships to more than 40 countries; prices are in pounds, and US visitors pay set dollar prices, shown second below. Parmore has also collaborated with Mogshade, which we covered in our <a href="/drops/brand-to-know-mogshade">Mogshade Brand to Know</a>. Seventeen pieces were in stock on October 12, 2026, plus the ball marker.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Bournemouth, England</span></div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>2024</span></div>
      <div class="sidebar-detail"><span class="l">Slogan</span><span>No Membership Required</span></div>
      <div class="sidebar-detail"><span class="l">Ships</span><span>40+ countries</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>&pound;8&ndash;&pound;90</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Brown Stripe Polo, &pound;50</span></div>
      <a href="https://parmoregolf.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit Parmore Golf &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#ParmoreGolf</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#NoMembershipRequired</span>
        <span class="hashtag">#GolfStreetwear</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("Where is Parmore Golf from?", "England. Its store lists Bournemouth, and the brand says it sells online only and ships to more than 40 countries."),
 ("When was Parmore Golf founded?", "2024, according to the brand's own About page."),
 ("What does No Membership Required mean?", "It is Parmore's slogan. The brand says it means golf is for everyone who wants to play it, with no committees, dress codes or gatekeeping."),
 ("How much does Parmore Golf cost?", "On October 12, 2026: socks £10, caps £35, tees £35 to £45, polos £50, the hoodie and cargo pants £65, and layers £65 to £90. US visitors see set dollar prices, for example $78 for a polo and $140 for the Varsity Quarter-Zip."),
 ("Is Parmore Golf clothing allowed on the course?", "Most of it is built to be. The polos, quarter-zips and windbreakers are golf pieces; Parmore itself says the cargo pants are a street pant, not a golf trouser."),
]
FRN = json.loads((ROOT / "research/parmore/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-PM-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-10-12", "dateModified": "2026-10-12",
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
    <span>Streetwear golf clothes &middot; England</span><span class="dot"></span>
    <span>17 in stock + 3 sold out &middot; checked October 12, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/btk-hero.jpg" alt="Three Parmore Golf photos: a model in the camo quarter-zip, a golfer in the brown stripe polo by the Houses of Parliament, and a model in the green varsity quarter-zip" fetchpriority="high" /></div></div>
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
    for leak in ("Mackem", "Kalamunda", "Howie", "No Dirt", "Lehi", "Rookline", "Bethpage", "Hudson", "LBB", "GolfPass", "Woodgrain"):
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
