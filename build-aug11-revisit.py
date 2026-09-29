#!/usr/bin/env python3
"""build-aug11-revisit.py — Aug 11, Revisited (same URL: /drops/brand-to-know-aug-11).
28 September 2026. Lenny: "we can refresh Aug 11", then "let's make it a brand
revisited but keep the same URL" (approving my eight new cards).

Follows the Brand Revisited playbook: same URL, datePublished kept (2026-06-22),
dateModified bumped; a new "What's Changed" section; IRL lookbook bands; new
cards; the original page's still-in-stock hats kept.

FIXES vs the June/August page: removed three unverifiable claims (Dom Dolla
"three of his four Coachella sets", Adam Mosseri / 2.4M followers, "none of that
was paid"); title no longer calls it a golf hat brand; meta no longer mentions
rope caps or buckets; Art Navy/Gold link (handle reused by the brand for a camo
trucker) dropped; duplicate FAQ block gone.

FACTS + QUOTES: research/aug11/notes.md (verified 28 Sep 2026).
PHOTOS: the brand's own product-gallery photography, localised to
images/aug11-revisit/. Prices from aug11.co, read 28 Sep 2026, USD.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "brand-to-know-aug-11"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/aug11-revisit"
FR = json.loads((ROOT / "research/aug11/frames.json").read_text())
BJ = json.loads((ROOT / "research/aug11/bands.json").read_text())
SHOP = "https://aug11.co/products/"
BRAND = "Aug 11"

TITLE = "Aug 11 Hats, Revisited: The Atlanta Hat Brand's New Drops"
DESC = ("Aug 11 is the Atlanta hat brand Johnny Persón built on his sister's birthday. Our revisit: "
        "the new REPS athletic line, The Refill, and 12 hats at $54.95.")
H1 = "Aug 11, Revisited &mdash; The Atlanta Hat Brand Built on a Birthday"

P = {
 "reps-futr-pink-camo-copy-1": ("Reps FUTR Snow Camo", "New &middot; 16 September", "54.95",
   "This is the newest REPS: FUTR colourway, a snow-camo structured snapback with Unbreakable in black script across the front and a yellow tab on the side. The brand marks it a best seller."),
 "art-tiff-blue-black-copy": ("Genuine Sinner", "The Refill &middot; White/Black", "54.95",
   "It is a structured two-tone snapback, white crown and black brim, with a black cross-shaped mark and GENUINE SINNER in red beneath it. It arrived with The Refill at the end of August."),
 "art-trucker-camo-unstructured-copy-1": ("Art White Trucker Camo", "The Refill &middot; Unstructured", "54.95",
   "This puts the Art logo and its orange flash on a white trucker with a camo brim. It is the loudest version of the signature so far."),
 "lord-forgive-me-white-unstructured-copy-1": ("Index", "Short brim &middot; Burnt Orange", "54.95",
   "This is the new shape: an unstructured cap with a short brim and a smaller fit, in burnt orange with AUGUST ELEVEN embroidered on the front."),
 "art-tiff-blue-black": ("Art", "Tiff Blue/Black", "54.95",
   "It is the Art on a black structured snapback, with the flash in a Tiffany-style blue. It came out in June and it is the quietest colourway in the line."),
 "reps-futr-runr-lilac-copy": ("Reps FUTR RUNR", "Taupe", "54.95",
   "This is a panelled runner&rsquo;s cap from the REPS: FUTR line, taupe on top and white below, with AUG11 across the front. It is the one we would wear to the range."),
 "cowboy-killers-copy": ("Champions Cup", "Structured trucker", "54.95",
   "It has a white front, a black brim and a derby crest: Champions Cup Derby, a winged horse, roses and Atlanta, Georgia. It reads like a souvenir from a racetrack."),
 "art-green-orng-copy": ("ATLangeles", "Unstructured", "54.95",
   "This is a washed charcoal unstructured cap with ATLANTA across the front and an old-English LA over the middle, splicing Atlanta and Los Angeles."),
 "art-snapback-black-white": ("Art", "Reverse OG", "54.95",
   "This is the signature: a black structured crown, a white brim and the red-and-white Art logo. It was the first hat we featured, and it is still in stock."),
 "art-5-panel-cotton-trucker-snap-back-hat-black": ("Art Mesh Trucker", "Black", "54.95",
   "It puts the Art logo on a black trucker with a mesh back. It is the version we would take to a summer round."),
 "loverboy-5-panel-cotton-structured-snap-back-hat-white-black": ("Loverboy", "White/Black", "54.95",
   "It has Loverboy in black script on a white structured crown with a black brim. It is one of the three hats the athletic line reworked in August."),
 "everyday-crest-black-copy": ("Crest V2", "Unstructured &middot; Navy", "54.95",
   "This is an unstructured navy cap with a white laurel A crest, contrast stitching and unbreakable resilience on the back tab. It is the most golf-looking hat Aug 11 makes."),
}

SECTIONS = [
    ("new", "New from the Collection &mdash; September 2026", "new-september",
     ["reps-futr-pink-camo-copy-1", "art-tiff-blue-black-copy", "art-trucker-camo-unstructured-copy-1", "lord-forgive-me-white-unstructured-copy-1",
      "art-tiff-blue-black", "reps-futr-runr-lilac-copy", "cowboy-killers-copy", "art-green-orng-copy"],
     "<strong>Eight hats &middot; $54.95 each</strong>These come from this year&rsquo;s drops, including the REPS athletic line and The Refill, and all were in stock when we checked."),
    ("originals", "The Originals, Still in Stock", "the-originals",
     ["art-snapback-black-white", "art-5-panel-cotton-trucker-snap-back-hat-black", "loverboy-5-panel-cotton-structured-snap-back-hat-white-black", "everyday-crest-black-copy"],
     "<strong>Four hats &middot; $54.95 each</strong>Four of the ten hats from our first post are still available. The rest, including the Stables Felt and the navy Loverboy, have sold out."),
]

PQ = {
    "fit": ("Our tagline is quality hats that fit perfectly guaranteed. We guarantee that they will fit you perfectly.",
            "Johnny Pers&oacute;n, founder, on the Honest Ecommerce podcast, March 2025"),
    "recognize": ("My main goal is to build something that people recognize and people see and they&rsquo;re like, that&rsquo;s Aug11. And I know that immediately.",
                  "Johnny Pers&oacute;n on the Honest Ecommerce podcast, March 2025"),
    "resilient": ("I think about all the things that I have been through in my life, I am unbreakably resilient.",
                  "Johnny Pers&oacute;n on the Up Arrow podcast, October 2025"),
}

def _band(key, kick, line, caps):
    return (kick, line, [(x["local"].split("/")[-1][:-4], H.escape(f"Aug 11 photograph: {x['title']}"), c) for x, c in zip(BJ[key], caps)])

BANDS = {
    "athletic": _band("athletic", "Photography &middot; Reps: Athletic", "The athletic line moved the shoot to ice baths, gyms and training floors.",
                      ["Loverboy, athletic", "Loverboy, athletic", "Lord Forgive Me, athletic"]),
    "campaign": _band("campaign", "Photography &middot; Lord Forgive Me", "These show the Lord Forgive Me in the Cam Whitcomb collaboration and the white colourway.",
                      ["Lord Forgive Me x Cam Whitcomb", "Lord Forgive Me x Cam Whitcomb", "Lord Forgive Me, white"]),
}

PROSE = 'style="max-width:760px;font-size:16px;line-height:1.7;margin:0 auto 24px;"'

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Aug 11 is a hat brand, not a golf brand, and that is still the point. When we first wrote about it in June it was a young Atlanta label with a real story and a very good snapback. Three months on, the brand says it has sold more than 100,000 hats, it is stocked at PacSun and Culture Kings, and it has started making hats for running and training.</p>
    <p>What makes it work on a course is what made it work off one: fit. Johnny Pers&oacute;n sells the fit as a guarantee, and the structured five-panel sits the way a golf cap should, with a flat front for the logo. The new Index adds a short brim and a smaller fit for narrower heads.</p>
    <p>Start with the Art (Reverse OG) at $54.95, which is still the signature. For the new stuff, get the Genuine Sinner. Prices were read from aug11.co on 28 September 2026, in US dollars, and the brand runs three hats for $99.99.</p>
    <h2 class="products-hdr btk-story-hdr">The Story</h2>
    <p>Aug 11 is named for Johnny Pers&oacute;n&rsquo;s younger sister, Isabell, born on 11 August 2003. In the brand&rsquo;s telling, late November 2010 was his lowest point, homeless and addicted, until his sister told him the truth: that he was hurting her. He has said he got sober that December. The tagline, Unbreakable Resilience, comes from that year.</p>
    <p>Pers&oacute;n grew up in industrial Costa Mesa, California, down the street from Hurley, Volcom and Quiksilver, and spent about a decade in apparel before launching Aug 11 from Atlanta on 1 November 2023. The first designs were already tattooed on his body. Aaron Judge, Jrue Holiday and Dom Dolla have all worn the hats. Pers&oacute;n says he gifts them without asking for a post, though Judge&rsquo;s came through a sports agency.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Atlanta, Georgia</span></div>
      <div class="sidebar-detail"><span class="l">Founder</span><span>Johnny Pers&oacute;n</span></div>
      <div class="sidebar-detail"><span class="l">Launched</span><span>1 November 2023</span></div>
      <div class="sidebar-detail"><span class="l">Hats sold</span><span>100,000+, by the brand&rsquo;s count</span></div>
      <div class="sidebar-detail"><span class="l">Price</span><span>$54.95; felt $59.95</span></div>
      <div class="sidebar-detail"><span class="l">Deal</span><span>Three hats for $99.99</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Art (Reverse OG), $54.95</span></div>
      <a href="https://aug11.co" target="_blank" rel="noopener" class="sidebar-cta">Shop Aug 11 &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#Aug11</span>
        <span class="hashtag">#BrandRevisited</span>
        <span class="hashtag">#HatCulture</span>
        <span class="hashtag">#UnbreakableResilience</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

CHANGED = f"""
<section class="products" style="margin-top:8px;">
  <div class="drop-tag grass">Revisited &middot; September 2026</div>
  <h2 class="products-hdr" id="what-changed">What&rsquo;s Changed Since June</h2>
  <div {PROSE}>
    <p style="margin:0 0 16px;">The biggest change is athletic. REPS: FUTR is a line of performance hats that started in 2025 and kept growing this year: FUTR and RUNR colourways in April, a sold-out Reps: Athletic drop of the Art, Loverboy and Lord Forgive Me in August, and a Snow Camo version this month. The photography moved with it, from bars and cars to ice baths, garages and gym floors.</p>
    <p style="margin:0 0 16px;">The Refill landed at the end of August with Genuine Sinner, a camo-brimmed Art trucker and the Index, a short-brim unstructured cap tagged for smaller heads. On 22 September came a Lord Forgive Me hat with the country singer Cam Whitcomb, which has already sold out. The brand also sells tees and hoodies now, alongside the hats.</p>
    <p style="margin:0 0 16px;">There is still no golf. We found no golf collection, no tour player and no course collaboration, and we would not want one. The hats already turn up on the first tee because they fit, and the athletic line is the most interesting thing the brand has done for anyone who plays.</p>
  </div>
</section>
"""

FAQ = [
    ("What is Aug 11?",
     "Aug 11 is an Atlanta hat brand founded by Johnny Persón and launched on 1 November 2023. It is not a golf company, but its structured snapbacks and unstructured caps have crossed over onto the course. Most hats are $54.95."),
    ("Where does the name Aug 11 come from?",
     "It is the birthday of Persón's younger sister, Isabell, born on 11 August 2003. In the brand's telling, she was the turning point in 2010, when he was homeless and addicted. The tagline is Unbreakable Resilience."),
    ("What is new from Aug 11 in 2026?",
     "The REPS: FUTR athletic line, with FUTR and RUNR colourways in April and a Snow Camo version in September; The Refill collection in late August, including the short-brim Index; and a Lord Forgive Me hat with the country singer Cam Whitcomb in September."),
    ("Are Aug 11 hats good for golf?",
     "They are not built as golf hats, but the fit is why they show up on courses. The Crest V2 unstructured cap is the most golf-looking, and the Art Mesh Trucker is the one we would take to a summer round."),
    ("How much do Aug 11 hats cost?",
     "Most hats are $54.95 and the Stables Felt is $59.95. The brand also runs a deal of three hats for $99.99."),
    ("Who wears Aug 11 hats?",
     "Aaron Judge, Jrue Holiday and Dom Dolla have all worn Aug 11. Persón says he gifts hats without asking for a post."),
]


def pq(key):
    txt, attr = PQ[key]
    return (f'\n<!-- TGI-A11-PQ-{key} -->\n<div class="pull-quote">\n  <div class="pull-quote-inner">'
            f'&ldquo;{txt}&rdquo;<span class="pull-quote-attr">&mdash; {attr}</span></div>\n</div>\n'
            f'<!-- /TGI-A11-PQ-{key} -->\n')

def band(key):
    kick, line, items = BANDS[key]
    figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>'
                     for f, alt, cap in items)
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <p class="cat-kicker"><strong>{kick}</strong>{line}</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


def card(h, idx):
    name, detail, price, copy = P[h]
    fr = [f["local"] for f in FR[h]]
    label = H.unescape(f"Aug 11 {name} {detail}").replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>'
                   for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>'
                   for j in range(len(fr)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{BRAND} &middot; {detail}</div>'
            f'<div class="product-name">{name} &middot; ${price}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="{SHOP}{h}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


def section(sec, n0):
    key, h2, anchor, ids, kicker = sec
    cards = "\n".join(card(h, n0 + j) for j, h in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} {"Piece" if len(ids) == 1 else "Pieces"}</div>\n'
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
    for _, _, _, ids, _ in SECTIONS:
        for h in ids:
            items.append({"@type": "ListItem", "position": pos, "url": SHOP + h, "name": H.unescape(f"Aug 11 {P[h][0]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-06-22", "dateModified": "2026-09-28",
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
            {"@type": "ListItem", "position": 3, "name": "Aug 11", "item": URL}]},
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
    ids = [h for s in SECTIONS for h in s[3]]
    assert len(ids) == 12 == len(set(ids)) and set(ids) == set(P)
    for h in ids:
        assert FR.get(h), h
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Aug 11, Revisited</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Atlanta, GA &middot; since 2023</span><span class="dot"></span>
    <span>Revisited September 2026 &middot; 12 hats</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A man in a black satin Aug 11 Lord Forgive Me cap under red neon" fetchpriority="high" /></div></div>
"""
    body += TAKE + pq("fit") + CHANGED + band("athletic")
    n = 1
    s, n = section(SECTIONS[0], n); body += s + pq("recognize") + band("campaign")
    s, n = section(SECTIONS[1], n); body += s + pq("resilient")
    body += faq_html()
    out = head_top() + head_rest + body + tail
    print(f"  {n-1} picks")
    if not apply_:
        print("  dry run — pass --apply")
        return
    OUT.write_text(out, encoding="utf-8")
    verify()


def verify():
    fin = OUT.read_text(encoding="utf-8")
    bad = []
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    for leak in ("Burnt Orange Manors", "Manors Revisited", "Nicklaus", "St. Andr", "Mosseri", "Coachella", "rope cap", "bucket"):
        if leak.lower() in above.lower():
            bad.append(f"should not appear: {leak}")
    if fin.count('class="product-card"') != 12:
        bad.append("card count")
    for k, (t, _) in PQ.items():
        if fin.count(t[:50]) != 1:
            bad.append(f"pq {k}")
    if above.count('class="ig-grid"') != 2:
        bad.append("band count")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", above), re.I):
        bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file():
            bad.append(f"missing {f}")
    if bad:
        sys.exit("! NOT written check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
