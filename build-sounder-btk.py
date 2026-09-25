#!/usr/bin/env python3
"""build-sounder-btk.py — Sounder, Brand to Know. 25 September 2026.

Lenny: "Let's do a brand to know - https://soundergolf.com/en-us", then on the
28-option grid: "looks good, your call on the homepage feature but lean on the
options with the best photos. Have quotes and what's the TGI take?"

PICKS. The 20 recommended from the grid (1,2,4,5,7,8,9,10,11,12,14,15,16,17,19,
22,23,25,26,27), in research/sounder/picks.json with USD prices read live from
soundergolf.com/en-us on 25 Sep 2026. Three are marked down on the store; those
show the sale price with the list price beside it, as the store shows them.

QUOTES. Five, all verbatim and re-checked against the source page on 25 Sep
2026: TheIndustry.fashion (11 Mar 2021) x3, Menswear Style (5 Jul 2022), and the
Sounder journal (13 Nov 2023). Golf Digest and Hole & Corner quotes from the
research pass were NOT used, because those pages would not load to re-check.
Notes in research/sounder/notes.md.

THE NAME. From Sounder's own journal ("What's in a name?", 24 Apr 2023): the
original Sounder clubs were made by Pratt-Read in Ivoryton, Connecticut; Seve
played them in the seventies; the brand ended in 1982 when a dam burst.

SHELL. Cloned from drops/brand-to-know-galvin-green.html (the newest BTK):
styles, nav, brand-index strip, More-from-TGI block, footer and gallery script
kept byte for byte. Author is Lenny as a Person (the house rule since 24 Sep).
Dry run by default.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-galvin-green.html"
OUT = ROOT / "drops/brand-to-know-sounder.html"
PICKS = json.loads((ROOT / "research/sounder/picks.json").read_text())["products"]
SLUG = "brand-to-know-sounder"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/sounder"
TODAY = "2026-09-25"

TITLE = "Sounder — The London Golf Brand Named for Seve's First Clubs"
DESC = ("Cotton polos, good knitwear and light layers from the founders of Folk and "
        "Urban Golf, under a name borrowed from the clubs Seve played in the seventies.")
H1 = "Sounder &mdash; The London Golf Brand Named for Seve&rsquo;s First Clubs"
AUTHOR = {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
          "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]}

# The Capri's store gallery opens on a two-man campaign shot where neither man
# is clearly in the Capri, so its card leads with the garment instead.
FRAME_ORDER = {1: [1, 2, 3, 0]}

CARD = {
    1: "The Capri drops the buttons entirely: an open, buttonless neck on organic cotton jersey, with a twin-stitched hem and cuff. Made in Portugal.",
    2: "The Clean Lie takes the Play Well shape and, in Sounder&rsquo;s words, adds nothing at all. It comes with no chest logo, only a small star tab on the sleeve.",
    4: "The Play Well is the house polo, and Sounder says the cut took nearly five years to get right. It is organic cotton jersey with a ribbed collar and a jersey hem that keeps the waist neat.",
    5: "The Monterey stripe takes its name from the Monterey Peninsula and runs deep red against navy on the same organic jersey. It is marked down on the store.",
    7: "This long-sleeve Play Well keeps the ribbed collar and cuffs in a navy pinstripe. It is the polo for the first cool morning of the year.",
    8: "The Fuzzy uses a slub cotton that Sounder has knitted for it alone, so the stripe has a soft, uneven texture. It has a relaxed long-sleeve cut and a three-button placket.",
    9: "The Eden knit blends cotton with 10% cashmere in a 14-gauge rib, with raglan shoulders for the swing and thumbholes in the long sleeves. A pointelle star sits on the back.",
    10: "The Fine Cut is an ultra-fine cotton knit polo that works year round. It carries a half-star embroidered on the forearm and goes in the washing machine.",
    11: "The Big Mach is a rugby-style long-sleeve polo in midweight organic sweat, finished with a poplin collar and extended cuffs with thumbholes. Its name comes from Machrihanish, on the Mull of Kintyre.",
    12: "The Raglan Star is a crew-neck sweat in organic cotton with a diagonal shoulder seam. A tonal chenille star sits on the sleeve, with a ball-marker patch as a finishing touch.",
    14: "The Chunky Knit is a waffle knit in 12-gauge Pima cotton, soft and heavy. It has long sleeves with thumbholes and a star on the chest.",
    15: "Sounder made this jacket with Protected Species: fully waterproof to 15,000mm, windproof and breathable, laser-cut and heat-welded, with a two-year waterproof guarantee.",
    16: "The Himalayas fleece takes its name from the Ladies&rsquo; putting course at St Andrews, not the mountains. It is lightweight Italian polar fleece, here in two tones with a two-way zip.",
    17: "The Pac Mach is Japanese recycled ripstop, light enough to stuff into its own drawstring bag. It has elastic cuffs, a drawcord hem and zipped pockets.",
    19: "This overhead Himalayas gilet pairs a half-zip with a deep kangaroo pocket. It takes the edge off a cold start and leaves your arms free to swing.",
    22: "The Clubhouse is a straight-leg five-pocket corduroy, garment-dyed, with silver rivets. Sounder warns that it sizes large, so check the measurements before ordering. Marked down.",
    23: "This Good Walk chino comes in garment-dyed organic cotton ripstop with a little stretch, an elastic drawcord waist and a tapered, cropped leg. Marked down.",
    25: "Sounder brought the Logo Cap back from its first collection: a six-panel cotton cap with a small wordmark patch, adjustable to one size.",
    26: "The Luxe Star beanie mixes wool and cashmere in a close rib with a turn-up and a half-star stitched in cotton. Sounder calls it the most comfortable hat you will ever own.",
    27: "This is a raw-finish brown leather belt, 35mm wide, with a brass roller buckle and a gold Sounder star. Made in England.",
}

KIND = {1: "Polo", 2: "Polo", 4: "Polo", 5: "Polo", 7: "Long-Sleeve Polo", 8: "Long-Sleeve Polo",
        9: "Cotton-Cashmere Knit", 10: "Knitted Polo", 11: "Rugby Polo", 12: "Sweatshirt", 14: "Cotton Knit",
        15: "Waterproof Jacket", 16: "Fleece Jacket", 17: "Packable Jacket", 19: "Fleece Gilet",
        22: "Corduroy Trousers", 23: "Drawcord Chino", 25: "Cap", 26: "Beanie", 27: "Belt"}

GROUPS = [
    ("Polos", [1, 2, 4, 5, 7, 8], "The Polos &mdash; 6 Pieces", "The Polos", "polos",
     "<strong>Organic cotton &middot; made in Portugal &middot; read 25 September 2026</strong>"
     "Sounder built its name on the cotton polo. The Play Well shape is underneath most of these, "
     "and they run $55 to $129."),
    ("Knits", [9, 10, 11, 12, 14], "Knitwear &mdash; 5 Pieces", "Knitwear and Sweats", "knitwear",
     "<strong>Cotton, cashmere blend, Pima &middot; read 25 September 2026</strong>"
     "This is where the brand is at its best. Every piece has sleeves long enough to swing in, "
     "and most go in the washing machine, at $136 to $190."),
    ("Outerwear", [15, 16, 17, 19], "Layers &mdash; 4 Pieces", "Layers", "layers",
     "<strong>Fleece, ripstop, waterproof &middot; read 25 September 2026</strong>"
     "These four light layers cover the cool months, from a packable ripstop at $197 to the Protected Species "
     "rain jacket at $372."),
    ("Rest", [22, 23, 25, 26, 27], "Trousers &amp; Finishing &mdash; 5 Pieces", "Trousers, Hats and a Belt", "trousers",
     "<strong>Cord, ripstop, cotton, leather &middot; read 25 September 2026</strong>"
     "Two pairs of trousers, both marked down, sit with the three small things that finish the look, "
     "at $55 to $102."),
]

PQ = {
    "started": ("We started Sounder because there was no-one in the golf world who made products for people like us. "
                "We love the game, but are embarrassed to admit it because of all the associations that people have "
                "with golf &ndash; the pointless rules and the awful fashion.",
                "Cathal McAteer, co-founder, to TheIndustry.fashion, March 2021"),
    "kindred": ("I met Cathal when he came to see me about building him a set of clubs, and I realised I had found a "
                "kindred spirit &ndash; he has the same relationship with clothes that I have with golf equipment.",
                "James Day, co-founder, to TheIndustry.fashion, March 2021"),
    "anti": ("I&rsquo;ve sadly been anti golf clothes for a long, long time. We would wear chinos, nice polos, and great "
             "jumpers, and we didn&rsquo;t need technical sportswear.",
             "Cathal McAteer, to Menswear Style, July 2022"),
    "dinner": ("Sounder clothing is stylish, hard-wearing and functional &ndash; it looks great on the golf course, but "
               "also in the office or out for dinner.",
               "Cathal McAteer, to TheIndustry.fashion, March 2021"),
    "clubs": ("Ever since Cathal and I first started talking about the business that became Sounder, I&rsquo;ve wanted "
              "us to launch our own golf clubs.",
              "James Day, in the Sounder journal, November 2023"),
}


def pq(key):
    t, a = PQ[key]
    return (f'\n<!-- TGI-SD-PQ-{key} -->\n<div class="pull-quote">\n  <div class="pull-quote-inner">'
            f'&ldquo;{t}&rdquo;<span class="pull-quote-attr">&mdash; {a}</span></div>\n</div>\n'
            f'<!-- /TGI-SD-PQ-{key} -->\n')


def money(x):
    return f"${x:,.0f}" if float(x).is_integer() else f"${x:,.2f}"


BY_N = {p["n"]: p for p in PICKS}


def split_title(t):
    name, _, colour = t.partition(" - ")
    return name.strip(), colour.strip().replace("  ", " ")


def card(p, idx):
    name, colour = split_title(p["title"])
    frames = p["local"]
    order = FRAME_ORDER.get(p["n"], list(range(len(frames))))
    frames = [frames[i] for i in order if i < len(frames)]
    label = H.escape(f"Sounder {name}" + (f", {colour}" if colour else ""), quote=True)
    imgs = "".join(
        f'<div class="pg-frame"><img src="{f}" alt="{label} &middot; view {i+1} of {len(frames)}" loading="lazy" /></div>'
        for i, f in enumerate(frames))
    dots = "".join(
        f'<button class="pg-dot{" on" if i == 0 else ""}" data-i="{i}" aria-label="View image {i+1}"></button>'
        for i in range(len(frames)))
    price = money(p["usd"])
    if p.get("was"):
        price += f' <span style="opacity:.5;text-decoration:line-through">{money(p["was"])}</span>'
    brand_line = f"Sounder &middot; {KIND[p['n']]}" + (f" &middot; {H.escape(colour)}" if colour else "")
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(frames)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(frames)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{brand_line}</div>'
            f'<div class="product-name">{H.escape(name)} &middot; {price}</div>'
            f'<div class="product-desc">{CARD[p["n"]]}</div>'
            f'<a href="{p["url"]}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


def section(g, n0):
    _, ns, tag, h2, anchor, kicker = g
    cards = "\n".join(card(BY_N[n], n0 + i) for i, n in enumerate(ns))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{tag}</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid">\n{cards}\n    </div>\n</section>\n'), n0 + len(ns)


PROSE = 'style="max-width:760px;font-size:16px;line-height:1.7;"'

TAKE = f"""
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Sounder makes the golf clothes that a well-dressed person already owns: cotton polos, good knitwear, a decent chino. It has done that in the same voice since it launched in 2021. What sets it apart is the point of view. The founders decided early that golf clothing did not need to look like golf clothing, and every piece since has held that line.</p>
    <p>The knitwear is the reason to know the name. The Eden knit, a cotton and cashmere rib with raglan shoulders and thumbholes, is the one we would buy first. The Chunky Knit and the Big Mach rugby polo are close behind. Most of it goes in the washing machine, which matters more than it sounds.</p>
    <p>For Austin, start with a Clean Lie polo at $102, the plainest shirt on the page and the easiest to wear anywhere. Add the Pac Mach jacket at $197 for the windy mornings between November and March, and keep the Eden knit for the two weeks a year it gets properly cold.</p>
    <h2 class="products-hdr btk-story-hdr">The Story</h2>
    <p>Sounder is the work of two Londoners. Cathal McAteer founded Folk, the menswear label, and has spent more than 20 years in clothing. James Day is a former PGA professional and club builder who founded Urban Golf, the London indoor golf venue. They met when McAteer came to Day to have a set of clubs built.</p>
    <p>They planned the brand during the 2020 lockdown and launched it in March 2021 with polos, sweats, knitwear, trousers and shorts designed to be worn on the course and off it. Almost everything is made in Portugal from organic cotton. Since then Sounder has made a golf shoe with Grenson, a range with Random Golf Club, a clubhouse pop-up in St Andrews during the 150th Open, and a rain jacket with Protected Species. In 2023 Day started selling vintage clubs he had rebuilt himself.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Launched</span><span>March 2021, London</span></div>
      <div class="sidebar-detail"><span class="l">Founders</span><span>Cathal McAteer, James Day</span></div>
      <div class="sidebar-detail"><span class="l">Owned by</span><span>Its founders</span></div>
      <div class="sidebar-detail"><span class="l">Made in</span><span>Portugal, mostly</span></div>
      <div class="sidebar-detail"><span class="l">Ships to US</span><span>Yes, by DHL</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$55&ndash;$372</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Eden cotton-cashmere knit</span></div>
      <a href="https://soundergolf.com/en-us" target="_blank" rel="noopener" class="sidebar-cta">Visit Sounder ↗</a>
      <div class="hashtags">
        <span class="hashtag">#Sounder</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#BritishGolf</span>
        <span class="hashtag">#GolfKnitwear</span>
        <span class="hashtag">#GolfStyle</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

NAME = f"""
<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr" id="the-name">Where the Name Comes From</h2>
  <div {PROSE}>
    <p>Sounder was the brand of clubs Seve Ballesteros played when he arrived on tour in the seventies. The founders took the name, and the star, because Seve was the golfer who got them into the game. Day owns a set of Sounder blades forged for Seve himself.</p>
    <p>The original story had been lost until Rochelle Trimble wrote to them. Her husband had been vice president of manufacturing at Pratt-Read, a piano-key maker in Ivoryton, Connecticut, that started a golf division, and she came up with the name. Pianos make lovely sounds, as she put it. The clubs sold at golf courses across the country until 1982, when a dam burst after a rainstorm and washed the warehouse into the river.</p>
    <p>The brand tells the whole story in its own journal, and it explains the tone of everything else: affection for the game, and very little interest in the numbers.</p>
  </div>
</section>
"""

AUSTIN = f"""
<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr" id="austin">Where It Fits in Austin</h2>
  <div {PROSE}>
    <p>Sounder is a British brand and dresses for British weather, so be honest about the calendar. The cotton polos are at their best from October to May. In July and August a heavy cotton jersey will soak through by the back nine, and a technical shirt will serve you better in that heat.</p>
    <p>The rest of the year is where this brand earns its place. Central Texas gets a run of cold, windy mornings between November and March, and a light layer over a cotton polo is exactly what they call for. The Pac Mach folds into its own bag once the sun is up; the Himalayas gilet leaves your arms free; the knitwear covers the handful of properly cold days.</p>
    <p>It also passes the test the founders set themselves. Every piece here looks right at lunch after the round, which is a lot of what makes a golf wardrobe useful.</p>
  </div>
</section>
"""

PICTURES = f"""
<section class="products" style="margin-top:8px;">
  <h2 id="in-the-campaign">In the Campaign</h2>
  <p class="cat-kicker"><strong>Photography &middot; Sounder&rsquo;s own</strong>Sounder shoots on the links and in the evening light, with people who look as though they have just finished a round rather than a workout. The frame on the left is a first tee in low sun; the other two were shot on the course in England and Spain.</p>
  <div class="ig-grid">
  <figure><img src="{IMG}/life-first-tee.jpg" alt="Three golfers with carry bags walking off a first tee at sunset, from Sounder&rsquo;s campaign" loading="lazy" /><figcaption class="ig-cap">A first tee in low sun</figcaption></figure>
  <figure><img src="{IMG}/life-trevose.jpg" alt="A golfer in an olive Sounder polo and dark trousers on a links course" loading="lazy" /><figcaption class="ig-cap">On the links in England</figcaption></figure>
  <figure><img src="{IMG}/life-spain.jpg" alt="A golfer in a striped polo carrying a bag towards a flag on a course in Spain" loading="lazy" /><figcaption class="ig-cap">Walking in, in Spain</figcaption></figure>
</div>
</section>
"""

FAQ = [
    ("Who owns Sounder?",
     "Its founders, Cathal McAteer and James Day. The UK company register lists the two of them as the people with significant control of the business, which trades as Soundercommunity Ltd."),
    ("Where is Sounder from?",
     "London. McAteer founded the menswear label Folk, and Day founded Urban Golf, the London indoor golf venue. Orders ship from the brand's London warehouse."),
    ("Why is it called Sounder?",
     "Sounder was the brand of clubs Seve Ballesteros played in the seventies, made by Pratt-Read in Ivoryton, Connecticut. The original company ended in 1982 when a dam burst and flooded its warehouse. The founders revived the name and the star logo."),
    ("Does Sounder ship to the US?",
     "Yes. The US store at soundergolf.com/en-us prices in dollars and ships by DHL Express. International customers pay any import duties, taxes and customs charges. TrendyGolf USA also stocks the brand online."),
    ("Is Sounder performance golf wear?",
     "Mostly not, by design. The polos and knitwear are organic cotton, cotton-cashmere and Pima cotton rather than synthetic fabrics. The exceptions on this page are the Protected Species waterproof jacket and the Pac Mach ripstop."),
    ("How much does Sounder cost?",
     "On 25 September 2026 the pieces on this page ran from $55 for the Logo Cap and the marked-down Monterey polo to $372 for the Protected Species waterproof jacket. Full-price polos were $102 to $129 and the knitwear $136 to $190."),
]


def faq_html():
    rows = "\n".join(
        f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>'
        for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')


def head_top():
    art = {
        "@context": "https://schema.org", "@type": "Article", "headline": TITLE,
        "description": DESC, "url": URL, "image": f"https://thegrassyissue.com{IMG}/hero.jpg",
        "datePublished": TODAY, "dateModified": TODAY, "author": AUTHOR,
        "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": URL},
    }
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
        {"@type": "ListItem", "position": 2, "name": "Drops & Brands", "item": "https://thegrassyissue.com/#feed"},
        {"@type": "ListItem", "position": 3, "name": "Sounder", "item": URL}]}
    t, d = H.escape(TITLE, quote=True), H.escape(DESC, quote=True)
    og = f"https://thegrassyissue.com{IMG}/hero.jpg"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{t}</title>
<meta name="description" content="{d}" />
<meta name="author" content="Lenny Harrington">
<link rel="icon" href="/favicon.ico" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
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
<script type="application/ld+json">
{json.dumps(art, indent=1, ensure_ascii=False)}
</script>
<script type="application/ld+json">
{json.dumps(faq, indent=1, ensure_ascii=False)}
</script>
<script type="application/ld+json">
{json.dumps(crumbs, indent=1, ensure_ascii=False)}
</script>
"""


def main(apply_):
    d = DONOR.read_text(encoding="utf-8")
    style_at = d.index("<style>")
    body_at = d.index('<div class="breadcrumb">')
    tail_at = d.index('<div class="more" data-brandindex="1">')
    head_rest = d[style_at:body_at]
    # the donor's own head tags that name the post must not leak (they live above <style>)
    lo, hi = min(p["usd"] for p in PICKS), max(p["usd"] for p in PICKS)
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Sounder</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>London &middot; est. 2021</span><span class="dot"></span>
    <span>{len(PICKS)} pieces &middot; {money(lo)}&ndash;{money(hi)}</span>
  </div>
</header>

<section class="drop-hero">
  <img class="drop-hero-img" src="{IMG}/btk-hero.jpg" alt="A golfer in a red Sounder Pac Mach jacket and grey beanie holding a club on a beach at dusk" fetchpriority="high" />
</section>
"""
    body += TAKE + pq("started") + NAME + pq("kindred") + AUSTIN + PICTURES
    n = 1
    s, n = section(GROUPS[0], n); body += s + pq("anti")
    s, n = section(GROUPS[1], n); body += s + pq("dinner")
    s, n = section(GROUPS[2], n); body += s + pq("clubs")
    s, n = section(GROUPS[3], n); body += s
    body += faq_html()

    out = head_top() + head_rest + body + d[tail_at:]
    print(f"  {n-1} cards, {len(PQ)} pull-quotes, {len(FAQ)} FAQs, range {money(lo)}-{money(hi)}")
    if not apply_:
        print("  dry run — pass --apply")
        return
    OUT.write_text(out, encoding="utf-8")
    verify()


def verify():
    fin = OUT.read_text(encoding="utf-8")
    bad = []
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->|<script\b.*?</script>", "",
                   fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    for leak in ("Galvin", "INSULA", "Nilsson"):
        if leak in above:
            bad.append(f"{leak} text leaked from the donor")
    if fin.count('class="product-card"') != len(PICKS):
        bad.append("card count")
    if set(CARD) != {p["n"] for p in PICKS}:
        bad.append("CARD keys do not match picks")
    for k, (t, a) in PQ.items():
        if fin.count(t[:60]) != 1:
            bad.append(f"pull-quote {k} appears {fin.count(t[:60])}x")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", fin), re.I):
        bad.append("banned word")
    for p in PICKS:
        for f in p["local"]:
            if not (ROOT / f.lstrip("/")).is_file():
                bad.append(f"missing {f}")
    for f in ("btk-hero", "hero", "life-first-tee", "life-trevose", "life-spain"):
        if not (ROOT / f"images/sounder/{f}.jpg").is_file():
            bad.append(f"missing {f}.jpg")
    if bad:
        OUT.unlink()
        sys.exit("! removed. " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
