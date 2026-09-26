#!/usr/bin/env python3
"""build-pants-top5.py — The Five Best Golf Pants Right Now, ranked by Lenny.
24 September 2026.

Lenny: "we're gonna do a post of what I think are the 5 best golf pants on the
market right now" — 1 Manors Greenskeeper, 2 Sentinel MajoTech Dark Navy, 3 Odd
Ritual Pleated Daily Trouser Black, 4 Students Science Adjustable Pants, 5
lululemon Daydrift Pleated Trouser. Then: "Let's make this a really well
formatted post- each option gets a write up and lookbook images then the card
itself. Add quotes from each brand about the pants if possible."

SO EACH ENTRY IS: number + heading + write-up, a pull-quote, a lookbook band,
then the single product card with its gallery.

PRICES, 24 Sep 2026, read from each brand's own store:
  Manors $172 (rendered page JSON-LD, USD) — Sentinel $210 (Squarespace page)
  Odd Ritual R 1,300 on 24 Sep, marked down to R 990 by 26 Sep (compare-at R 1,300);
  the store serves rand to a US browser; not converted. 26 Sep: embroidery paragraph
  added at Lenny's request ("talk a little about the embroidered details").
  Students $135 (.js) — lululemon $148 (page og:price, USD)

QUOTES are verbatim with dated sources in research/pants-top5/notes.md. Where
no named person has spoken about the trouser, the pull-quote is the brand's own
product copy and is labelled as such. No quote is repeated in the body.

Shell: drops/brand-to-know-manors.html (same approach as build-fall-drops.py).
Writes drops/best-golf-pants-ranked.html. No feed card. Dry run by default.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "best-golf-pants-ranked"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/pants-top5"

TITLE = "The 5 Best Golf Pants Right Now, Ranked (2026)"
DESC = ("Our five favourite golf pants, ranked: Manors' Greenskeeper, Sentinel's "
        "MajoTech, Odd Ritual's Pleated Daily Trouser, Students' Science Pant and "
        "lululemon's Daydrift. Prices checked 24 September 2026.")
H1 = "The Five Best Golf Pants Right Now &mdash; Ranked"
PROSE = 'style="max-width:760px;font-size:16px;line-height:1.7;"'

PANTS = [
 dict(n=1, key="manors", brand="Manors", name="Recycled Greenskeeper Trouser", colour="Ivory",
      price="$172", url="https://manorsgolf.com/products/recycled-greenskeeper-trouser",
      frames=["manors-3", "manors-1", "manors-4", "manors-6"],
      band=[("manors-0", "A golfer walking across a green in ivory Manors Greenskeeper trousers and white trainers", "On the course, ivory"),
            ("manors-11", "A golfer carrying a leather bag through a pine-lined fairway in ivory Greenskeeper trousers", "Carrying through the pines"),
            ("manors-10", "A golfer standing on a sandy path with his bag in ivory Greenskeeper trousers", "Out on the links")],
      kicker="<strong>No. 1 &middot; Manors, London &middot; $172 &middot; read 24 September 2026</strong>It has double pleats, workwear pockets and a recycled stretch fabric that shrugs off wind and light rain. Seven colours on the store.",
      body=[
        "The Greenskeeper is the pair we reach for first. Manors cuts it from a 178gsm fabric that is 93% recycled nylon and 7% elastane, with four-way stretch and a PFC-free water-resistant finish. It has a full elastic waistband with a drawcord, a gusset for the swing and eight pockets in a workwear layout. Up front sit two deep pleats that give it a relaxed, slightly old-fashioned shape.",
        "That combination is why it tops the list. It moves like a technical pant and looks like something a groundskeeper would wear, which is exactly the point of the name. Manors ambassador Adem Wahbi told Golf Digest in 2023 that the pockets &ldquo;look stylish and just different from what you usually see in golf.&rdquo; On a windy Austin morning it keeps the cold off, and by the back nine it still looks like trousers rather than track pants. We covered the whole brand in <a href=\"/drops/brand-to-know-manors\">Manors, Revisited</a>.",
      ],
      pq=("Many of golf&rsquo;s most recognizable personalities used to wear pleated trousers. Also, double pleats naturally create a more relaxed silhouette, offering both comfort and ease of movement.",
          "Nick Watts, Manors product director, to Forbes, June 2026"),
      card="It is recycled nylon with four-way stretch and a water-resistant finish, double front pleats, eight workwear pockets and an elastic drawcord waist. Shown in Ivory; the store lists seven colours."),
 dict(n=2, key="sentinel", brand="Sentinel", name="MajoTech Trouser", colour="Dark Navy",
      price="$210", url="https://www.sentinelgolf.us/shop/p/8t95uvw1ec28h1za76ycshtzy2kvha-57hyk-8trkf-6g8w5-b2y36-a7r98-ldyan-4y4zm-x76y7-t9lmw-2mc83-t5y3y-tl3d6-zn6k2",
      frames=["sentinel-1", "sentinel-0", "sentinel-2", "sentinel-5"],
      band=[("sentinel-lb1", "A model in a cream hoodie and dark navy Sentinel trousers, from the FW26 lookbook", "FW26 lookbook, dark navy"),
            ("sentinel-lb2", "A model adjusting his cap in a cream top and dark navy Sentinel trousers", "Cut classic, not slim")],
      kicker="<strong>No. 2 &middot; Sentinel, Minneapolis &middot; $210 &middot; read 24 September 2026</strong>Italian MajoTech cloth, cut and sewn in New York, with waterproof zips and a cord lock at the ankle.",
      body=[
        "Sentinel built the MajoTech Trouser around its fabric, and it shows. The fabric comes from MajoTech, an Italian mill the brand says has been weaving since 1941. It is 97% nylon and 3% spandex with a DWR face, four-way stretch and a wrinkle-resistant hand. The trousers are cut and sewn in New York.",
        "The details are where it earns second place. It has YKK waterproof zippers, a Japanese elastic band inside the waist, KaneM snaps and an adjustable cord lock inside each ankle, so you can taper the hem on a wet morning. Sentinel describes the cut as &ldquo;tailored without being slim,&rdquo; and it is the only pant here without a pleat. If you are between sizes, the brand says to size down. There is more on the brand in <a href=\"/drops/brand-to-know-sentinel-golf\">our Sentinel Brand to Know</a>.",
      ],
      pq=("What is important to me at this point is finding the people who care the most about what they make, use the best inputs they can find, and do things the right way at all phases of the process.",
          "John Mooty, Sentinel founder, to The Old Ghosts, December 2025"),
      card="MajoTech nylon-spandex woven in Italy with a DWR face, YKK waterproof zips, KaneM snaps and internal ankle cord locks. Cut and sewn in New York. Sizes S to XL."),
 dict(n=3, key="oddritual", brand="Odd Ritual", name="Pleated Daily Trouser", colour="Black",
      price="R 990", url="https://oddritualgolf.com/products/pleated-daily-trouser-black",
      frames=["oddritual-1", "oddritual-0", "oddritual-4"],
      band=[("oddritual-2", "Close detail of the black Pleated Daily Trouser showing the embroidered RR monogram on the thigh, with a blue Odd Ritual cap in hand", "The RR monogram, on the thigh"),
            ("oddritual-3", "The back of the trouser leg above a rolled hem, with Odd Ritual embroidered in script", "The script, low on the back of the leg"),
            ("oddritual_khaki-1", "A man in a cream polo and khaki Odd Ritual Pleated Daily Trousers holding a hickory club", "The same cut in khaki")],
      kicker="<strong>No. 3 &middot; Odd Ritual, Cape Town &middot; R 990, down from R 1,300 &middot; read 26 September 2026</strong>Cotton twill, front pleats and a carrot-shaped leg, made locally in Cape Town. Priced in rand, the currency the store shows.",
      body=[
        "Odd Ritual is the only brand here working in cotton rather than a performance fabric. The Pleated Daily Trouser is 235gsm cotton twill with front pleats, a stretch band across the back of the waist. It is made in Cape Town. The store has it marked down to R 990 from R 1,300.",
        "The embroidery is what makes it an Odd Ritual trouser. There are two pieces, both in the same gold-toned thread. The brand&rsquo;s RR monogram sits inside a small ring on the front of the thigh, just below the pocket, where you would normally find nothing at all. The Odd Ritual script is stitched low on the back of the leg, a few inches above the hem, where it only shows when you walk away. The brand calls them &ldquo;refined finishing details,&rdquo; and that is fair: on the black, from a few feet away, they read as texture rather than logos.",
        "It sits third because it is the most honest pair of trousers on the list. There is no stretch-nylon trick to it; it is a pleated cotton trouser cut wide at the top and narrow at the ankle, and it looks right with a polo, a knit or a tee. The black is in stock in M, L and XL; the khaki has sold through. We wrote about the brand in <a href=\"/drops/brand-to-know-odd-ritual\">our Odd Ritual Brand to Know</a>.",
      ],
      pq=("Designed for effortless everyday wear, these relaxed trousers are crafted from soft 235gsm cotton twill and cut in a loose fit with a subtle carrot silhouette.",
          "Odd Ritual, from the brand&rsquo;s product description"),
      card="It is 235gsm cotton twill with front pleats and an elasticated back waistband, with an RR monogram embroidered on the thigh and the Odd Ritual script on the back of the leg. Made in Cape Town. In stock in M, L and XL on 26 September."),
 dict(n=4, key="students", brand="Students", name="Science Adjustable Pleated Pants", colour="Black",
      price="$135", url="https://studentsgolf.com/products/science-adjustable-baggy-pants-1",
      frames=["students-10", "students-0", "students-11", "students-4"],
      band=[("students-2", "A man in black Students Science pants standing in front of a silver Porsche in a garage", "In the garage"),
            ("students-7", "A man in a Students sweatshirt and black Science pants among vintage cars", "Relaxed to baggy"),
            ("students-9", "A man in black Science pants walking between classic cars", "Stretch nylon, black")],
      kicker="<strong>No. 4 &middot; Students, California &middot; $135 &middot; read 24 September 2026</strong>A velcro waist that moves the pleat, so one pair of trousers has more than one shape. Two sizes cover waists 30 to 40.",
      body=[
        "Students calls the Science Pant the most unusual trouser in its range, and the reason is the waist. A velcro adjuster lets you move where the pleat sits, which changes how the whole leg falls. The brand says the idea came from military trousers. It is made from a 90% nylon, 10% spandex slack fabric that stretches and breathes.",
        "Because the waist adjusts, it comes in only two sizes: Size 1 for waists 30 to 34 and Size 2 for 34 to 40. It is the least expensive pant on the list at $135, and the one most likely to get a question on the first tee. Founder Michael Huynh started out designing streetwear, and trousers were always his speciality. Students also turned up in <a href=\"/drops/fall-drops-eastside-students-devereux\">our fall drops roundup</a> this week.",
      ],
      pq=("I learned how to make pants really well. That was my category, I felt like.",
          "Michael Huynh, Students founder, to Boardroom, December 2025"),
      card="This stretch nylon pant has an adjustable velcro waist that shifts the pleat and the silhouette. Two sizes: Size 1 for 30 to 34, Size 2 for 34 to 40. Black."),
 dict(n=5, key="lulu", brand="lululemon", name="Daydrift Relaxed-Fit Pleated Trouser", colour="Deep Forest",
      price="$148", url="https://shop.lululemon.com/p/mens-daydrift-pleated-trouser-regular/rh9tqbxsdn?color=76997",
      frames=["lulu-0", "lulu-1", "lulu-2", "lulu-3"],
      band=[("lulu-4", "A hand in the pocket of Deep Forest lululemon Daydrift pleated trousers", "Pleat and pocket"),
            ("lulu-5", "Side view of the Daydrift trouser waistband with belt loops", "Belt loops, now"),
            ("lulu-6", "The back of the Daydrift trouser showing the welt pockets", "Back welt pockets")],
      kicker="<strong>No. 5 &middot; lululemon, Vancouver &middot; $148 &middot; read 24 September 2026</strong>A pleated trouser in lululemon&rsquo;s Luxtreme fabric, sold as casual wear and worn by plenty of golfers anyway.",
      body=[
        "The Daydrift is not sold as a golf pant; lululemon files it under Casual. It plays like one anyway. The fabric is Luxtreme, 69% nylon and 31% Lycra, which wicks sweat, stretches four ways and dries quickly. The waistband is stretch with a hidden drawcord, there is a phone sleeve inside the hand pocket and the back pockets close with hidden snaps.",
        "The latest version added belt loops, which is what moved it onto this list. The cut is roomy through the seat and thigh and falls straight to the hem, and lululemon says it is meant to puddle a little on the shoe. It comes in a 28&Prime; or 30&Prime; inseam. The Deep Forest colour is a green that works with almost any polo.",
      ],
      pq=("Comfort got all dressed up. With their stretch waistband and tailored pleats, these trousers make looking good feel easy.",
          "lululemon, from the brand&rsquo;s product description"),
      card="It is Luxtreme nylon-Lycra that wicks and stretches, with tailored pleats, a stretch waistband with a hidden drawcord and belt loops. Deep Forest, in 28&Prime; or 30&Prime; inseams."),
]

TAKE = f"""
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>These are the five golf pants we would buy right now, counted down from No. 5 to No. 1. Four of the five have a pleat, which says a lot about where golf trousers have gone in the last two years: roomier, softer, and closer to what you would wear to dinner.</p>
    <p>The countdown opens with three pairs with plenty of personality: lululemon&rsquo;s casual trouser that golfers keep wearing on the course, a pant with a movable pleat, and a cotton trouser from Cape Town. It finishes with the two technical ones. Sentinel&rsquo;s MajoTech and Manors&rsquo; Greenskeeper both use stretch nylon with a water-resistant finish, and both handle a cold, windy Austin morning without looking like rain gear.</p>
    <p>Each one gets a write-up, a quote from the brand, its own photography and then the card. Prices were read from each brand&rsquo;s store on 24 September 2026, and Odd Ritual&rsquo;s again on 26 September, when it had been marked down. Four are in US dollars; Odd Ritual prices in rand, and we have left that as the store shows it.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Ranking</div>
      <div class="sidebar-detail"><span class="l">No. 5</span><span>lululemon Daydrift</span></div>
      <div class="sidebar-detail"><span class="l">No. 4</span><span>Students Science Pant</span></div>
      <div class="sidebar-detail"><span class="l">No. 3</span><span>Odd Ritual Pleated Daily</span></div>
      <div class="sidebar-detail"><span class="l">No. 2</span><span>Sentinel MajoTech</span></div>
      <div class="sidebar-detail"><span class="l">No. 1</span><span>Manors Greenskeeper</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$135&ndash;$210</span></div>
      <a href="#no-5" class="sidebar-cta">Start the countdown &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#GolfPants</span>
        <span class="hashtag">#Manors</span>
        <span class="hashtag">#SentinelGolf</span>
        <span class="hashtag">#PleatedTrousers</span>
        <span class="hashtag">#GolfStyle</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

FAQ = [
    ("What are the best golf pants right now?",
     "Our ranking, as of September 2026: 1. Manors Recycled Greenskeeper Trouser, 2. Sentinel MajoTech Trouser, 3. Odd Ritual Pleated Daily Trouser, 4. Students Science Adjustable Pleated Pants, 5. lululemon Daydrift Relaxed-Fit Pleated Trouser."),
    ("Which of these golf pants are pleated?",
     "Four of the five. The Manors Greenskeeper has double front pleats, the Odd Ritual and lululemon trousers have front pleats, and the Students Science Pant has a pleat you can move with its velcro waist. The Sentinel MajoTech is a classic flat-front cut."),
    ("Which golf pants here are best in wind and light rain?",
     "The Manors Greenskeeper and the Sentinel MajoTech. Both use stretch nylon with a water-resistant finish; the Sentinel also has waterproof YKK zips and ankle cord locks."),
    ("What is the least expensive pair?",
     "The Students Science Adjustable Pleated Pants at $135 on 24 September 2026. The lululemon Daydrift is $148, the Manors Greenskeeper $172 and the Sentinel MajoTech $210."),
    ("Why is the Odd Ritual price in rand?",
     "Odd Ritual is based in Cape Town and its store prices in South African rand, including for visitors from the US. We show the price the store shows, R 990 (marked down from R 1,300 when we checked on 26 September 2026), rather than converting it."),
    ("Is the lululemon Daydrift a golf pant?",
     "lululemon lists it as casual wear rather than golf. It is made from the brand's Luxtreme fabric, which wicks sweat and stretches four ways, and the latest version has belt loops, which makes it easy to wear on the course."),
]


def pq(t, a, key):
    return (f'\n<!-- TGI-PANTS-PQ-{key} -->\n<div class="pull-quote">\n  <div class="pull-quote-inner">'
            f'&ldquo;{t}&rdquo;<span class="pull-quote-attr">&mdash; {a}</span></div>\n</div>\n'
            f'<!-- /TGI-PANTS-PQ-{key} -->\n')


def card(p):
    fr = [f"{IMG}/{f}.jpg" for f in p["frames"]]
    label = f'{p["brand"]} {p["name"]}'
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)}, {p["colour"]} &middot; view {i+1} of {len(fr)}" loading="lazy" /></div>' for i, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if i == 0 else ""}" data-i="{i}" aria-label="View image {i+1}"></button>' for i in range(len(fr)))
    return (f'<div class="product-card" id="p-{p["n"]}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">No. {p["n"]} &middot; {p["brand"]} &middot; {p["colour"]}</div>'
            f'<div class="product-name">{p["name"]} &middot; {p["price"]}</div>'
            f'<div class="product-desc">{p["card"]}</div>'
            f'<a href="{p["url"]}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


def entry(p):
    words = "One Two Three Four Five".split()[p["n"] - 1]
    paras = "\n".join(f"    <p>{b}</p>" for b in p["body"])
    cols = "" if len(p["band"]) == 3 else ' style="grid-template-columns:repeat(2,1fr)"'
    figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{H.escape(alt)}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>' for f, alt, cap in p["band"])
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">No. {p["n"]} of Five</div>\n'
            f'  <h2 class="products-hdr" id="no-{p["n"]}">{p["n"]}. {p["brand"]} {p["name"]}</h2>\n'
            f'  <p class="cat-kicker">{p["kicker"]}</p>\n'
            f'  <div {PROSE}>\n{paras}\n  </div>\n</section>\n'
            + pq(*p["pq"], p["key"]) +
            f'\n<section class="products" style="margin-top:4px;border-top:none;">\n'
            f'  <div class="ig-grid"{cols}>\n{figs}\n</div>\n'
            f'    <div data-single-card="1"><div class="products-grid">\n{card(p)}\n    </div></div>\n</section>\n')


def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>' for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items = [{"@type": "ListItem", "position": p["n"], "url": p["url"], "name": f'{p["brand"]} {p["name"]}'} for p in PANTS]
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC, "url": URL, "image": og,
         "datePublished": "2026-09-24", "dateModified": "2026-09-24",
         "author": {"@type": "Organization", "name": "The Grassy Issue"},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListOrder": "https://schema.org/ItemListOrderAscending", "itemListElement": items},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Drops & Brands", "item": "https://thegrassyissue.com/#feed"},
            {"@type": "ListItem", "position": 3, "name": "The Five Best Golf Pants", "item": URL}]},
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
    # one card per entry: centre it at a readable width instead of leaving it
    # in the first column of a three-column grid
    head_rest = head_rest.replace("</style>", "[data-single-card] .products-grid{grid-template-columns:minmax(0,460px);justify-content:center}\nsection.products > div > p + p{margin-top:16px}\n</style>", 1)
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  The Five Best Golf Pants</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>September 24, 2026</span><span class="dot"></span>
    <span>5 pairs &middot; ranked</span><span class="dot"></span>
    <span>$135&ndash;$210 &middot; plus R 990</span>
  </div>
</header>

<section class="drop-hero">
  <img class="drop-hero-img" src="{IMG}/hero.jpg" alt="A golfer walking a green with his putter in olive Manors Greenskeeper trousers, the Manors logo on the thigh pocket, from the brand&rsquo;s Greenskeeper Collection page" fetchpriority="high" />
</section>
"""
    body += TAKE
    # COUNTDOWN — Lenny: "let's organize the list in decending order". No. 5
    # comes first and the page builds to No. 1; the ranks themselves are unchanged.
    for p in reversed(PANTS):
        body += entry(p)
    body += f"""
<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr" id="more-pants">Want More Options?</h2>
  <div {PROSE}>
    <p>These five came out of a much longer look at the category. <a href="/drops/the-pants-edit">The Pants Edit</a> has eighteen trousers, one per brand, if none of these is quite your cut.</p>
  </div>
</section>
"""
    body += faq_html()
    out = head_top() + head_rest + body + tail
    print(f"  {len(PANTS)} entries")
    if not apply_:
        print("  dry run — pass --apply")
        return
    OUT.write_text(out, encoding="utf-8")
    verify()


def verify():
    fin = OUT.read_text(encoding="utf-8")
    bad = []
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    if "Manors, Revisited" not in above:
        pass
    if re.search(r"Manors Golf, Revisited &mdash; The Brand", above):
        bad.append("Manors page text leaked")
    if fin.count('class="product-card"') != 5:
        bad.append("card count")
    for p in PANTS:
        t = p["pq"][0]
        if fin.count(t[:50]) != 1:
            bad.append(f"pull-quote {p['key']} appears {fin.count(t[:50])}x")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", fin), re.I):
        bad.append("banned word")
    for f in re.findall(rf'src="({IMG}/[^"]+)"', fin):
        if not (ROOT / f.lstrip("/")).is_file():
            bad.append(f"missing {f}")
    order = [fin.index(f'id="no-{n}"') for n in range(5, 0, -1)]
    if order != sorted(order):
        bad.append("countdown out of order (should run No. 5 to No. 1)")
    if bad:
        OUT.unlink()
        sys.exit("! removed. " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
