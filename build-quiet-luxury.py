#!/usr/bin/env python3
"""build-quiet-luxury.py — The 9 Best Quiet Luxury Golf Brands. 26 October 2026. Structure cloned from build-streetwear26.py.
Lenny: "Let's do Quiet luxury golf brands build that as a post" (after "What other categories are similar to Streetwear").
FACTS: every product read from the brand's own store on 26 Oct 2026 (research/quiet-luxury/*.json, picks.json); product copy
paraphrases each store's own description. Late Nine and Local Rule sell in SEK only, converted at 0.1005 (SEK/USD mid,
27 Oct 2026, poundsterlinglive.com). Pull quotes are the verified quotes already on each brand's TGI profile.
PHOTOS: brands' own store and campaign images (research/quiet-luxury/frame.py, bands.py).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "best-quiet-luxury-golf-brands"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/quiet-luxury"
CHECKED = "26 October 2026"
SEK = 0.1005
PK = json.loads((ROOT / "research/quiet-luxury/picks.json").read_text())
FR = json.loads((ROOT / "research/quiet-luxury/frames.json").read_text())

TITLE = "The 7 Best Quiet Luxury Golf Brands of 2026"
DESC = ("The seven best quiet luxury golf brands of 2026: Late Nine, Whim, Alba, Sounder, Quiet Golf, Local Rule "
        "and Casualist. Merino, cashmere and pleats, six pieces from each, with prices.")
H1 = "The 7 Best Quiet Luxury Golf Brands in 2026"

BRANDS = [
 dict(k="ln", slug="late-nine", award="Best Overall", name="Late Nine",
  link=("/drops/late-nine-stockholm-relaxed-fits-and-the-quiet-part-of-golf", "Read the Late Nine profile"),
  body=["Late Nine is the clearest answer to what quiet luxury looks like on a golf course. Maxim Lundh co-founded it in Stockholm in 2024 around late-nineties tour golf: double-pleated slacks in Italian four-season wool, knit polos, merino vests and an instructor&rsquo;s blouson. There is barely a logo in the range.",
        "The fabrics carry it. The cable polo and the ribbed vest are knit from merino taken at the sheep&rsquo;s first shearing, and the slacks hang with a full straight leg that looks like 2000 in the best way. It is not cheap, but it is the most complete wardrobe on this list."],
  pq=("Tiger Woods won the US Open in 2000 by 15 shots, remember the size of his pants?", "Maxim Lundh, Late Nine co-founder, to The Old Ghosts"),
  band=["Late Nine, on the links", "The FW26 lookbook", "The Instructors Jacket"],
  copy=["Merino from the first shearing, knit into a cable polo. Warm enough for a cold first tee and soft enough to wear to dinner.",
        "Italian four-season wool with a full straight leg and generous double pleats facing outward. The Tiger-in-2000 silhouette, in navy.",
        "Late Nine&rsquo;s take on the knit polos of the &rsquo;80s and &rsquo;90s, designed as an everyday piece and a travel companion.",
        "First-shearing merino again, ribbed into a vest for light warmth over a polo. Sage is the color to get.",
        "Modeled on the jackets golf instructors wore through the &rsquo;90s: a blouson with a rounded stand-up collar.",
        "A cross between a chino and a tailored trouser, in soft cream cord. The pant to wear when slacks feel like too much."]),
 dict(k="wh", slug="whim-golf", award="Best Made in America", name="Whim Golf",
  link=("/drops/brand-to-know-whim-golf", "Read the Whim Golf profile"),
  body=["Whim makes the most American golf shirt we&rsquo;ve found: merino from ranches in Idaho, Colorado, California and Nevada, knit in Massachusetts or South Carolina and finished in New York. No synthetics, and the only branding is a small script on the chest.",
        "The rest of the range keeps to the same rule. The swing jacket is woven merino from Connecticut, the hats are woven merino with a leather strap, and the beanie is knit in Queens."],
  pq=("We want to wear clothes that we feel will look good on us 10 years from now.", "Colin Heaberg, Whim Golf co-founder, to StockX, 2022"),
  band=["The founders, outside Free Golf NYC", "The founding golf trip, Michigan", "The Big Bag, in New York"],
  copy=["100% American merino with no synthetics and a white Whim script on navy. The shirt the brand is built on.",
        "Mid-weight American merino in slate with sky-blue script. The quietest of the long sleeves.",
        "Woven in Connecticut from RWS-certified merino, with a RiRi zipper and a cinch hem. Natural merino, undyed.",
        "A 6.5oz merino knit with short sleeves, from RWS-certified sheep raised in California, Colorado, Idaho and Nevada.",
        "Woven merino with a brass closure and a leather strap. A brim built flat so you can curve it yourself.",
        "Fully fashioned and knit in Queens from American merino. Reversible, with the Whim label on one side."]),
 dict(k="al", slug="alba-golf", award="Best New Brand", name="Alba Golf",
  link=("/drops/brand-to-know-alba-golf", "Read the Alba Golf profile"),
  body=["Alba launched in Milan this October, and it is the most polished debut we&rsquo;ve covered this year. The palette runs to mauve, charcoal, ivory and black with one red vest, the logos are small, and the clothes are built for weather without looking technical.",
        "That is the brand&rsquo;s whole idea, and its About page says it plainly. Three-layer waterproof shells, technical wool knits and a padded vest sit next to cotton piqu&eacute; polos. It is the most expensive brand on this list, and it does not hide that."],
  pq=("Performance is integrated rather than displayed.", "Alba Golf, on its About page"),
  band=["The swing study", "The launch campaign", "Scotland, where the idea started"],
  copy=["A long-sleeve polo in cotton piqu&eacute;, chosen for comfort and year-round wear. In mauve, it is the piece that sums up the brand.",
        "A knit in 100% technical wool with shaped sleeves and a slightly raised collar.",
        "Mostly cotton, blended with nylon, in a clean, tailored trouser.",
        "Polyester microfiber with an internal coating against wind and water. The most color in the range.",
        "A three-layer waterproof jacket and the most expensive piece in this post.",
        "The same three-layer waterproof fabric as the Crest, cut as a quarter-zip."]),
 dict(k="sd", slug="sounder", award="Best British", name="Sounder",
  link=("/drops/brand-to-know-sounder", "Read the Sounder profile"),
  body=["Sounder comes from the founders of Folk and Urban Golf and borrows its name from the clubs Seve played in the seventies. It makes the kind of clothes British golfers wore before golf clothes became sportswear: cotton polos, good knitwear, cords and moleskin.",
        "It is one of the most affordable brands on this list, and its knits are the reason to look. The fine-cut polo and the chunky Pima waffle knit would sit as comfortably in a pub as on the first tee."],
  pq=("We would wear chinos, nice polos, and great jumpers, and we didn&rsquo;t need technical sportswear.", "Cathal McAteer, Sounder co-founder, to Menswear Style, July 2022"),
  band=["Sounder at Trevose", "Sounder in Spain", "The first tee"],
  copy=["An ultra-fine 100% cotton knit with a half-star on the forearm. Our pick from Sounder.",
        "12-gauge Pima cotton in a chunky waffle knit, with extended sleeves and thumbholes.",
        "Organic cotton jersey with a buttonless open placket. A polo that reads like a knit.",
        "A straight-leg, garment-dyed cotton cord in a five-pocket cut.",
        "Mid-weight cotton moleskin with a pleated front, button fly, relaxed waist and tapered leg.",
        "Lightweight Italian polar fleece with a two-way zip, made in Portugal."]),
 dict(k="qg", slug="quiet-golf", award="Best California", name="Quiet Golf",
  link=("/drops/brand-to-know-quiet-golf", "Read the Quiet Golf profile"),
  body=["The name says it. Quiet Golf comes out of Costa Mesa, from Christion Lennon and the Diaz brothers, and treats a round as a way to get off your phone. The clothes follow: cashmere sweaters, Supima polos and a corduroy jacket with nothing louder than a small QG flag.",
        "It is the most Californian version of quiet luxury: relaxed rather than tailored, and built for a walk with friends more than a members&rsquo; lunch."],
  pq=("Golf has a way of doing that. It cuts through everything else.", "Diego Diaz, Quiet Golf co-founder, in the brand&rsquo;s journal"),
  band=["Quiet Golf, mid-swing", "On the links", "Two for the walk"],
  copy=["A 100% cashmere cable knit with the QG flag on the chest. The brand&rsquo;s best piece.",
        "Another 100% cashmere sweater, striped, with the same small flag.",
        "Supima cotton with a little stretch and a three-button placket, made in Portugal.",
        "Cotton, nylon and spandex with a snap front, cut long to allow for shrinkage.",
        "Cotton corduroy with the QG flag and angled hand pockets.",
        "An unstructured cotton twill dad hat with the QG monogram."]),
 dict(k="lr", slug="local-rule", award="Best Value", name="Local Rule",
  link=("/drops/brand-to-know-local-rule", "Read the Local Rule profile"),
  body=["Local Rule is a Stockholm brand that spent three years making its clothes in Portugal, then moved production home to Bor&aring;s. It works in the same Scandinavian register as Late Nine: pleated trousers, knit polos and quiet layers in navy, off-white and beige.",
        "The difference is price. A knit polo is about $120 and the pleated trousers about $151, which makes it the easiest way into the look on this list."],
  pq=("We feel that golf is too much fun to waste on ugly clothes.", "David Zetterlund, Local Rule co-founder, to Golfbranschen, May 2023 (translated)"),
  band=["Local Rule on the course", "The pom-pom beanie, in the heather", "A cap and a clean swing"],
  copy=["A classic knit polo the brand says was inspired by the coast. In off-white.",
        "Single-pleated trousers, a relaxed Scandinavian take on tailoring.",
        "A quarter-zip fleece for cool mornings and layering. In beige.",
        "A long-sleeve performance polo built for competitive rounds.",
        "A light technical vest for changing conditions on and off the course.",
        "An off-white cold-weather beanie. The cheapest thing in the post."]),
 dict(k="cs", slug="casualist", award="Best Off the Course", name="Casualist",
  link=("/drops/brand-to-know-casualist", "Read the Casualist profile"),
  body=["Casualist is Elie Reboul&rsquo;s label, designed in London and made in Portugal. It started as Casual Pro in Melbourne and moved to the UK in 2024, where, as the team put it, golf is a little more buttoned-up.",
        "It is the most playful brand here, but the best of it fits the brief: a merino cardigan vest, organic cotton pleated trousers and a tartan wool cap. These are the pieces that work at the bar as well as the course."],
  pq=("Things are a bit more buttoned-up in the UK.", "The Casual Pro team, announcing the move to London, April 2024"),
  band=["Casualist on the coast", "Out on the links", "The 2026 campaign"],
  copy=["100% merino with a soft, vintage feel, buttoned down the front. The piece that earns Casualist its place here.",
        "Organic cotton twill with a high waist, clean pleats and a straight leg.",
        "Raglan sleeves and a relaxed fit. Casualist pitches it as the polo a club captain with better taste would wear.",
        "An interlock cotton mockneck that stays just dressed-up enough to pass a dress code.",
        "Lightweight ripstop with back ventilation and an adjustable waist cord.",
        "Soft wool tartan with a rope detail."]),
]
for b in BRANDS:
    b["rows"] = PK[b["slug"]]
    assert len(b["rows"]) == 6 == len(b["copy"]), b["k"]


def price(r):
    x = float(r["price"])
    if r["cur"] == "SEK":
        return f"{x:,.0f} kr (~${x * SEK:,.0f})"
    return f"${x:,.0f}" if x.is_integer() else f"${x:,.2f}"


def nice(t):
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\s+[–-]\s+(Light|Mid)-?[Ww]eight$", "", t)
    t = re.sub(r"\bLs\b", "LS", re.sub(r"\bSs\b", "SS", t))
    return t.title() if t.isupper() else t


def card(b, i, idx):
    r = b["rows"][i]
    fr = FR[f'{b["k"]}{i + 1}']
    name = H.escape(nice(r["t"]))
    label = H.unescape(f'{b["name"]} {nice(r["t"])}').replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>'
                   for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>'
                   for j in range(len(fr)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{b["name"]}</div>'
            f'<div class="product-name">{name} &middot; {price(r)}</div>'
            f'<div class="product-desc">{b["copy"][i]}</div>'
            f'<a href="{r["url"]}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


def pq(b):
    q, who = b["pq"]
    return (f'\n<div class="pull-quote" style="margin:8px auto 24px">\n  <div class="pull-quote-inner">'
            f'&ldquo;{q}&rdquo;<span class="pull-quote-attr">&mdash; {who}</span></div>\n</div>\n')


def band(b):
    figs = "\n".join(f'  <figure><img src="{IMG}/band-{b["k"]}-{n}.jpg" alt="{H.unescape(b["name"])}: {H.unescape(c)}" loading="lazy" />'
                     f'<figcaption class="ig-cap">{c}</figcaption></figure>' for n, c in enumerate(b["band"]))
    return f'  <div class="ig-grid" style="margin:8px 0 28px">\n{figs}\n  </div>\n'


def section(b, rank, n0):
    MT = ' style="margin-top:14px"'
    paras = "\n".join(f'    <p{"" if j == 0 else MT}>{p}</p>' for j, p in enumerate(b["body"]))
    cards = "\n".join(card(b, i, n0 + i) for i in range(6))
    href, text = b["link"]
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{b["award"]}</div>\n'
            f'  <h2 class="products-hdr" id="{b["slug"]}">{rank}. {b["name"]}</h2>\n'
            f'  <div style="max-width:760px;margin:0 auto 18px;font-size:16px;line-height:1.75">\n{paras}\n'
            f'    <p style="margin-top:16px;font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;opacity:.6">'
            f'Checked {CHECKED} &middot; <a href="{href}">{text} &rarr;</a></p>\n  </div>\n'
            f'{pq(b)}{band(b)}'
            f'    <div class="products-grid">\n{cards}\n    </div>\n</section>\n'), n0 + 6


TAKE = f"""
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Quiet luxury in golf means clothes that look expensive because of what they are made of and how they are cut, not because of what is printed on them. Merino and cashmere instead of polyester, pleats instead of performance stretch, navy and cream instead of neon, and a logo you have to look for. It is the opposite of a tour-pro billboard, and it is the look a lot of the best independent brands are chasing right now.</p>
    <p>Late Nine is the best overall: the most complete wardrobe, the best fabrics and the clearest point of view, all built on late-nineties tour golf. Whim makes everything in America, from the merino to the hats, and Alba is the most polished new arrival of the year. Sounder, Quiet Golf, Local Rule and Casualist round it out, from British knitwear and California cashmere to Swedish tailoring at the friendliest prices on the list.</p>
    <h2 class="products-hdr btk-story-hdr">How We Picked</h2>
    <p>Every brand had to build its clothes around fabric and cut rather than logos, sell pieces you would wear off the course, and have product in stock on the day we checked. Each brand gets an award and six pieces, all read live from its own store on {CHECKED}. Late Nine and Local Rule only sell in Swedish kronor, so their prices are shown in kronor with a dollar estimate at the {CHECKED[:2]} October rate.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Seven</div>
""" + "\n".join(f'      <div class="sidebar-detail"><span class="l">{b["award"].replace("Best ", "")}</span><span><a href="#{b["slug"]}">{b["name"]}</a></span></div>' for b in BRANDS) + f"""
      <div class="sidebar-detail"><span class="l">Checked</span><span>{CHECKED}</span></div>
      <a href="/brands" class="sidebar-cta">The full Brand Index &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#QuietLuxury</span>
        <span class="hashtag">#GolfStyle</span>
        <span class="hashtag">#OldMoneyGolf</span>
        <span class="hashtag">#DropsAndBrands</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">disclosure</a></div>
  </aside>
</section>
"""

FAQ = [
    ("What is quiet luxury golf clothing?",
     "Golf clothes that look expensive because of their fabric and cut rather than their logos: merino, cashmere and cotton knits, pleated wool or cotton trousers, muted colors and small or hidden branding."),
    ("What is the best quiet luxury golf brand in 2026?",
     "Late Nine, from Stockholm. Its range of double-pleated wool slacks, merino knit polos and vests is the most complete on our list, and it carries almost no visible logos."),
    ("Which quiet luxury golf brand is the most affordable?",
     "Sounder and Local Rule. On 26 October 2026 Sounder's knit polos and cords started around $75 to $115, and Local Rule's knit polo was 1,199 Swedish kronor, about $120."),
    ("Is there a quiet luxury golf brand made in the USA?",
     "Whim Golf makes its clothing, hats and accessories in the USA, and its merino shirts use wool from ranches in Idaho, Colorado, California and Nevada, finished in New York."),
    ("What is old money golf style?",
     "It is the same look under another name: pleats, knitwear, earth tones and very little branding, closer to a 1990s clubhouse than to modern tour apparel."),
]


def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>'
                     for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items = [{"@type": "ListItem", "position": i + 1, "name": H.unescape(b["name"]), "url": f"{URL}#{b['slug']}"}
             for i, b in enumerate(BRANDS)]
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": H.unescape(DESC),
         "url": URL, "image": og, "datePublished": "2026-10-26", "dateModified": "2026-10-26",
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
            {"@type": "ListItem", "position": 3, "name": "Best Quiet Luxury Golf Brands", "item": URL}]},
    ]
    t, d = H.escape(TITLE, quote=True), DESC.replace('"', "&quot;")
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
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Best Quiet Luxury Golf Brands</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>7 brands &middot; 7 awards</span><span class="dot"></span>
    <span>42 pieces &middot; prices checked {CHECKED}</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Quiet luxury golf in 2026: a Late Nine golfer in a ribbed knit vest carrying his bag through the dunes, Alba Golf's Milan launch campaign in navy and white, and a Sounder golfer walking the links at Trevose" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for rank, b in enumerate(BRANDS, 1):
        o, n = section(b, rank, n); body += o
    body += faq_html()
    out = head_top() + head_rest + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Manors Revisited", "Nicklaus", "Enron"):
        if leak in above: bad.append("leak " + leak)
    if fin.count('class="product-card"') != 42: bad.append("card count")
    plain = re.sub(r"<[^>]+>", " ", above)
    if re.search(r"\bworth\b|\bgenuinely\b|\bhonestly\b|\bstraightforward\b", plain, re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
