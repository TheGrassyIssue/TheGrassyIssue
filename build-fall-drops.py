#!/usr/bin/env python3
"""build-fall-drops.py — Three Fall Drops: Eastside Golf, Students, Devereux.
24 September 2026.

Lenny: "Lots of new fall drops, let's do a round up on three fall drops from
brands we dig" (Eastside new arrivals, Students Fall 2026 Delivery 1, Devereux
Pioneertown Golf Club). He took the recommended 15 from a 24-option grid.

SHELL: drops/brand-to-know-manors.html, same as build-galvin-btk.py — styles,
nav, brand-index strip, More-from-TGI, footer and gallery script kept byte for
byte; everything between breadcrumb and brand-index strip is replaced.

DATA: research/fall-drops/picks.json. All three stores return USD from
/cart.js; prices and stock read 24 Sep 2026.

QUOTES: three, verbatim from named founders, with dated sources in
research/fall-drops/notes.md. NONE of them is about these drops — no named
person has spoken on the record about any of the three — so each attribution
carries its real date and context. Drop descriptions are quoted as brand copy,
labelled as such.

NOT CLAIMED: why Devereux chose the name Pioneertown (the brand never says),
the Devereux shoot location (only a file name suggests Joshua Tree), any
official launch date (all dates here are when the pieces went up on the store),
or an Eastside campaign name (there is none).

Writes drops/fall-drops-eastside-students-devereux.html. No feed card; that
waits for Lenny. Dry run by default.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "fall-drops-eastside-students-devereux"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/fall-drops-2026"
P = {p["n"]: p for p in json.loads((ROOT / "research/fall-drops/picks.json").read_text())["products"]}

TITLE = "Three Fall 2026 Golf Drops: Eastside Golf, Students and Devereux"
DESC = ("Fifteen pieces from three fall drops: Eastside Golf's new arrivals, "
        "Students' \"The Curriculum\" and Devereux's Pioneertown Golf Club. "
        "Prices checked 24 September 2026.")
H1 = "Three Fall Drops We Dig &mdash; Eastside Golf, Students and Devereux"

BRAND = {"eastside": "Eastside Golf", "students": "Students", "devereux": "Devereux"}

# n -> (display name, card copy)
CARDS = {
    1: ("Course Camo Snap Placket Polo",
        "The print is the story: a painted golf course, trees and all, repeated as camo. It is cut in nylon and spandex with a snap placket and an athletic fit."),
    3: ("Signature 1/4 Zip, Wave Stripe",
        "This light tech-stretch quarter zip carries pumice and lava stripes in a wave. Eastside pitches it for morning rounds and crisp days, which is exactly an Austin November."),
    4: ("Pitch Jersey, Prime Green/Navy",
        "It is a football shirt with a golf collar: faded vertical stripes, vintage jersey styling and a relaxed athletic fit, in breathable polyester."),
    5: ("Tip Pique Polo, Wild Grape",
        "This is the plainest piece here, in the best colour Eastside has put out this season. It is cotton-poly pique with mechanical stretch and a mesh knit collar with contrast tipping."),
    6: ("Khaki Field Pant",
        "The Field Pant puts cargo pockets on a lightweight nylon pant with a tapered leg. The waistband is elastic with a drawcord, and it still has belt loops."),
    9: ("Denali Stadium Jacket",
        "Students calls this the defining piece of the drop. It is a heavyweight wool stadium jacket with striped ribbing, leather welt pockets, snap front and a quilted satin lining."),
    10: ("Hereford L/S Sweater Polo",
         "The Hereford is a long-sleeve polo with contrast tipping at the collar, cuffs and hem and a two-button placket, cut relaxed in a cotton-poly blend."),
    11: ("Tradition Double Pleated Wool Pants",
         "These trousers are double pleated in a wool-poly blend with a relaxed leg. There is satin trim inside the waistband and buttoned welt pockets at the back."),
    12: ("Whittier Knit L/S Polo Sweater",
         "The Whittier is a full-fashion cotton knit in wide horizontal stripes with a polo collar. It is the piece from the lookbook that most looks like a prep-school yearbook."),
    14: ("Canyonlands Anorak Jacket",
         "This half-zip anorak comes in an all-over camo print, with an adjustable hood, kangaroo pocket and mesh lining. Built for layering on changeable days."),
    17: ("Homestead Western Polo, Sky",
         "The Homestead is a performance polo with pearl snap buttons and quiet heritage striping. The mesh jacquard collar breathes, and the black colourway has already sold out."),
    18: ("High Noon Polo, Clay",
         "The High Noon is a clay-red pique printed with small skulls and palms. Devereux calls it the Western edge of the Pioneertown story, and it has stretch for the swing."),
    20: ("Disco Rodeo Polo, Bone",
         "The Disco Rodeo is a bone-coloured stretch pique printed all over. It carries the collection&rsquo;s character on the technical side of the range."),
    21: ("Devco Twill Jacket, Vintage Sky",
         "The Devco is a washed cotton twill jacket in a workwear cut, pale blue with an oval patch on the chest. It goes from a cool tee time to dinner without a change."),
    22: ("Piped Quarter Zip, Succulent Green",
         "This lightweight quarter-zip windbreaker has retro piping across the chest and sleeves. The pale green layers easily over any of the polos above."),
}

SECTIONS = [
    ("eastside", [1, 3, 4, 5, 6], "Eastside Golf &mdash; 5 Pieces", "Eastside Golf: Fall New Arrivals", "eastside-golf",
     "<strong>Fall 2026 &middot; landed late August to early September &middot; read 24 September 2026</strong>"
     "Eastside did not give this drop a name. It came in two waves, and the pieces that define it are a painted-course camo print, a wave stripe and a football-style jersey. $78 to $125."),
    ("students", [9, 10, 11, 12, 14], "Students &mdash; 5 Pieces", "Students: &ldquo;The Curriculum&rdquo;", "students",
     "<strong>Fall 2026 Delivery 1 &middot; went up 1 September &middot; read 24 September 2026</strong>"
     "Students built this drop around the start of a school year: glen plaid, knits, pleated trousers and a wool stadium jacket. $148 to $280."),
    ("devereux", [17, 18, 20, 21, 22], "Devereux &mdash; 5 Pieces", "Devereux: Pioneertown Golf Club", "devereux",
     "<strong>Fall 1: &ldquo;The Arrival&rdquo; &middot; went up 31 July &middot; read 24 September 2026</strong>"
     "Devereux&rsquo;s fall collection is high-desert Western: pearl snaps, skull prints and a washed twill jacket. At $74 to $138 it is the least expensive of the three."),
]

PQ = {
    "eastside": ("I was tired of trying to fit into a mold. Why not come into the sport as I am.",
                 "Olajuwon Ajanaku, Eastside Golf co-founder, to Axios Detroit, July 2025"),
    "students": ("My past as a designer is rooted in streetwear, so it gets me excited to bring those "
                 "principles to golf in ways that the sport hasn&rsquo;t had access to yet.",
                 "Michael Huynh, Students founder, to Golf Digest, November 2022"),
    "devereux": ("At Devereux Golf, we&rsquo;re focused on reshaping golf culture without losing sight "
                 "of the sport&rsquo;s roots.",
                 "Robert Brunner, Devereux co-founder, in the brand&rsquo;s Mount Gay capsule release, May 2026"),
}

PROSE = 'style="max-width:760px;font-size:16px;line-height:1.7;"'

INTRO = {
    "eastside": f"""
  <div {PROSE}>
    <p>Eastside Golf was started in 2019 by Olajuwon Ajanaku, with Earl Cooper as co-founder. Both played golf at Morehouse College. This fall the footwear gets the headlines, with new Nike shoes, but the apparel is where the brand is having the most fun.</p>
    <p>The Course Camo print takes a golf landscape and repeats it until it reads as camouflage. The Pitch Jersey borrows from football shirts, and the brand&rsquo;s own copy says it is &ldquo;built to be worn for the culture, not just the course.&rdquo; The Wild Grape polo is the quiet one, and the colour carries it. <a href="/brands/eastside-golf">Everything we have covered from Eastside</a> is on its brand page.</p>
  </div>""",
    "students": f"""
  <div {PROSE}>
    <p>Students was founded in 2021 by Michael Huynh, who came from streetwear, where he founded the label Publish. The brand has always played on school, with tees called Math Club and shorts called Calculus, and <a href="/drops/students-golf-summer-2026">we covered its summer drop</a> in August.</p>
    <p>Fall takes the joke to its natural end. In the brand&rsquo;s own lookbook copy, &ldquo;The Curriculum&rdquo; is &ldquo;inspired by the ritual of preparing for a new academic year and the mindset that came with it.&rdquo; The clothes are Ivy League and prep-school codes: knitted polos, pleated wool trousers, and the Denali, which the brand describes as &ldquo;something earned, worn, and eventually passed down.&rdquo;</p>
  </div>""",
    "devereux": f"""
  <div {PROSE}>
    <p>Devereux is a Scottsdale brand started in 2013 by the brothers Robert and Will Brunner, named for their grandmother. It has been <a href="/drops/brand-to-know-devereux-golf">a Brand to Know here</a> since July, and it has always been the most relaxed of the three.</p>
    <p>Pioneertown Golf Club is its fall collection. The brand&rsquo;s description calls it &ldquo;inspired by high desert travel, Western workwear, vintage Americana, and modern golf.&rdquo; Part one, &ldquo;The Arrival&rdquo;, is mostly polos. Pearl snaps on a performance knit are the detail that sells it.</p>
  </div>""",
}

BANDS = {
    "students": ("Photography &middot; Students&rsquo; own lookbook",
                 "The Curriculum lookbook is shot against a plain backdrop, which lets the clothes do the talking.",
                 [("lb-students-denali", "A man in a black Students Denali wool stadium jacket and an S cap", "The Denali, front"),
                  ("lb-students-denali-back", "The back of the Denali stadium jacket with Students script embroidery", "The Denali, back"),
                  ("lb-students-whittier", "A man in the green and cream striped Whittier knit polo sweater", "Whittier knit, striped")]),
    "devereux": ("Photography &middot; Devereux&rsquo;s own",
                 "The collection page opens on a Joshua tree in the high desert, which sets the scene better than any product shot.",
                 [("lb-devereux-joshua-tree-45", "Joshua trees and boulders in the high desert under a pale sky", "The high desert"),
                  ("lb-devereux-western-detail", "Close detail of a navy Devereux Western polo with white piping at the yoke", "Western piping, up close")]),
}

TAKE = f"""
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Three brands we like put out fall collections within a few weeks of each other, and each went a different direction. Eastside Golf went loud and printed. Students went back to school. Devereux went to the high desert. Together they cover most of what an Austin fall needs: polos for the warm afternoons that keep coming, and one real jacket for the mornings that finally don&rsquo;t.</p>
    <p>If you buy one piece, make it the Students Denali Stadium Jacket at $280. It is wool, it is heavy, and it is the kind of jacket that gets better with years. If you want the most fun for the least money, the Devereux Homestead polo with pearl snaps is $74.</p>
    <p>We picked five from each drop. Every price below was read from the brand&rsquo;s own store on 24 September 2026, in US dollars, with every piece in stock in four sizes or more.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Drops</div>
      <div class="sidebar-detail"><span class="l">Eastside</span><span>Fall new arrivals</span></div>
      <div class="sidebar-detail"><span class="l">Students</span><span>&ldquo;The Curriculum&rdquo;</span></div>
      <div class="sidebar-detail"><span class="l">Devereux</span><span>Pioneertown Golf Club</span></div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>15</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$74&ndash;$280</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Denali Stadium Jacket</span></div>
      <a href="#students" class="sidebar-cta">Jump to the Denali &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#EastsideGolf</span>
        <span class="hashtag">#StudentsGolf</span>
        <span class="hashtag">#DevereuxGolf</span>
        <span class="hashtag">#FallDrops</span>
        <span class="hashtag">#GolfStyle</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

FAQ = [
    ("What is in Eastside Golf's fall 2026 drop?",
     "Eastside's fall new arrivals landed in two waves between late August and early September 2026. The pieces that define it are the Course Camo print polo and shorts, the Pumice/Lava Wave Stripe signature range, the Pitch Jersey and new Wild Grape and Cranberry colourways. Polos run $68 to $88."),
    ("What is Students Golf's \"The Curriculum\"?",
     "It is the name of Students' Fall 2026 Delivery 1, which went up on the brand's store on 1 September 2026. The brand describes it as inspired by preparing for a new academic year, drawing on Ivy League and prep-school wardrobes. The centrepiece is the Denali Stadium Jacket at $280."),
    ("What is Devereux's Pioneertown Golf Club collection?",
     "Devereux's fall 2026 collection, which the brand describes as inspired by high desert travel, Western workwear, vintage Americana and modern golf. Part one, called The Arrival, went up on 31 July 2026. Most polos in it are $74."),
    ("Which of the three drops is the least expensive?",
     "Devereux. The five pieces picked here run $74 to $138. Eastside's run $78 to $125, and Students' $148 to $280."),
    ("Do these brands ship in the US?",
     "All three are American brands selling in US dollars from their own stores. Devereux is based in Scottsdale, Arizona, and Students in Southern California; Eastside Golf opened its first store at Detroit Metro Airport in 2025."),
    ("Who founded Students Golf?",
     "Michael Huynh, a designer who came from streetwear and founded the label Publish, launched Students in 2021."),
]


def money(x):
    return f"${x:,.0f}" if float(x).is_integer() else f"${x:,.2f}"


def pq(key):
    t, a = PQ[key]
    return (f'\n<!-- TGI-FALL-PQ-{key} -->\n<div class="pull-quote">\n  <div class="pull-quote-inner">'
            f'&ldquo;{t}&rdquo;<span class="pull-quote-attr">&mdash; {a}</span></div>\n</div>\n'
            f'<!-- /TGI-FALL-PQ-{key} -->\n')


def card(n, idx):
    p = P[n]
    name, copy = CARDS[n]
    fr = p["local"]
    brand = BRAND[p["brand"]]
    label = f"{brand} {name}"
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{label} &middot; view {i+1} of {len(fr)}" loading="lazy" /></div>'
                   for i, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if i == 0 else ""}" data-i="{i}" aria-label="View image {i+1}"></button>'
                   for i in range(len(fr)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{brand} &middot; {H.escape(p["colour"])}</div>'
            f'<div class="product-name">{name} &middot; {money(p["usd"])}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="{p["url"]}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


def band(key):
    kick, line, items = BANDS[key]
    cols = "" if len(items) == 3 else ' style="grid-template-columns:repeat(2,1fr)"'
    figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>'
                     for f, alt, cap in items)
    return (f'  <p class="cat-kicker"><strong>{kick}</strong>{line}</p>\n'
            f'  <div class="ig-grid"{cols}>\n{figs}\n</div>\n')


def section(sec, n0):
    key, ns, tag, h2, anchor, kicker = sec
    cards = "\n".join(card(n, n0 + i) for i, n in enumerate(ns))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{tag}</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            + INTRO[key] + "\n"
            + (band(key) if key in BANDS else "")
            + f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid">\n{cards}\n    </div>\n</section>\n'), n0 + len(ns)


def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>'
                     for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items = []
    pos = 1
    for key, ns, *_ in SECTIONS:
        for n in ns:
            p = P[n]
            items.append({"@type": "ListItem", "position": pos, "url": p["url"],
                          "name": f"{BRAND[p['brand']]} {H.unescape(CARDS[n][0])}"})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-09-24", "dateModified": "2026-09-24",
         "author": {"@type": "Organization", "name": "The Grassy Issue"},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": items},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Drops & Brands", "item": "https://thegrassyissue.com/#feed"},
            {"@type": "ListItem", "position": 3, "name": "Three Fall Drops", "item": URL}]},
    ]
    t, d = H.escape(TITLE, quote=True), H.escape(DESC, quote=True)
    ld = "".join(f'<script type="application/ld+json">\n{json.dumps(b, indent=1, ensure_ascii=False)}\n</script>\n' for b in blocks)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{t}</title>
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
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    allp = [P[n] for _, ns, *_ in SECTIONS for n in ns]
    lo, hi = min(p["usd"] for p in allp), max(p["usd"] for p in allp)
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Three Fall Drops</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>September 24, 2026</span><span class="dot"></span>
    <span>Fall 2026 &middot; 3 brands</span><span class="dot"></span>
    <span>{len(allp)} pieces &middot; {money(lo)}&ndash;{money(hi)}</span>
  </div>
</header>

<section class="drop-hero">
  <img class="drop-hero-img" src="{IMG}/hero.jpg" alt="A golfer finishing his swing on a dirt road through the high desert, a still from the film on Devereux&rsquo;s homepage" fetchpriority="high" />
</section>
"""
    body += TAKE
    n = 1
    for sec in SECTIONS:
        body += pq(sec[0])
        s, n = section(sec, n)
        body += s
    body += faq_html()
    out = head_top() + head_rest + body + tail
    print(f"  {n-1} cards, range {money(lo)}-{money(hi)}")
    if not apply_:
        print("  dry run — pass --apply")
        return
    OUT.write_text(out, encoding="utf-8")
    verify()


def verify():
    fin = OUT.read_text(encoding="utf-8")
    bad = []
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    if "Manors" in above:
        bad.append("Manors text leaked")
    if fin.count('class="product-card"') != 15:
        bad.append("card count")
    for k, (t, _) in PQ.items():
        if fin.count(t[:50]) != 1:
            bad.append(f"pull-quote {k} appears {fin.count(t[:50])}x")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", fin), re.I):
        bad.append("banned word")
    if re.search(r"Joshua Tree National|movie set|film set|shot in Joshua", fin, re.I):
        bad.append("an unverified Pioneertown/location claim got in")
    for p in P.values():
        for f in p["local"]:
            if not (ROOT / f.lstrip("/")).is_file():
                bad.append(f"missing {f}")
    for f in re.findall(rf'src="({IMG}/[^"]+)"', fin):
        if not (ROOT / f.lstrip("/")).is_file():
            bad.append(f"missing {f}")
    if bad:
        OUT.unlink()
        sys.exit("! removed. " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
