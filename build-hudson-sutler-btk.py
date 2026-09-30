#!/usr/bin/env python3
"""build-hudson-sutler-btk.py — Brand to Know: Hudson Sutler.
30 September 2026.

Lenny: "let's do a brand to know - https://www.hudsonsutler.com/", then "add all
okay to use 20ish total options" after the 26-option grid (my 18 stars plus the
Heritage Cooler Bag and Heritage Shave Kit).

FACTS: Hudson Sutler's own About, FAQ and product pages, read 30 Sep 2026.
Co-founder Mike Chepucavage and the Featherlite launch: PGA.com, 25 Jan 2026.
InsideHook (12 Oct 2017) for the early New York maker description. A second
founder name seen only in search summaries is left out.
QUOTES: verbatim. The Golf Digest line is as quoted on the Savannah product page.
PHOTOS: the brand's own (product pages and homepage banners). No press photos.
Prices and stock read 30 Sep 2026, USD. TGI Take follows the Austin-angle +
value-verdict rule (Lenny, 30 Sep). No feed card yet.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "brand-to-know-hudson-sutler"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/hudson-sutler"
FR = json.loads((ROOT / "research/hudson-sutler/frames.json").read_text())
SHOP = "https://www.hudsonsutler.com/products/"
BRAND = "Hudson Sutler"
BRAND_T = "Hudson Sutler"

TITLE = "Hudson Sutler — Golf and Travel Bags Made in New Jersey"
DESC = ("Hudson Sutler cuts and sews golf bags, shoe bags, coolers and duffels in North Bergen, New Jersey. "
        "Why it suits an Austin golf trip, and 20 picks from $50 to $399.")
H1 = "Brand to Know: Hudson Sutler &mdash; Golf Trip Bags, Made in New Jersey"

P = {
 "hudson-looper-bag": ("Hudson Looper Golf Bag 2.0", "Four colourways", "399",
   "This is a 4.2-pound carry bag in coated ballistic nylon with a water-repellent finish, carbon fibre legs and an 8-inch four-way top with full-length dividers. It has two shoulder straps, six pockets, a magnetic rangefinder pocket and an insulated drinks pocket, and it fits 14 clubs."),
 "hudson-feather-lite-golf-bag": ("Hudson Featherlite Golf Bag", "Hunter green &middot; 2026 launch", "365",
   "The new one launched at the 2026 PGA Show. It weighs 3.5 pounds and has an 8-inch top with a grab handle, carbon fibre legs, four outside pockets and the magnetic rangefinder pocket. It is the stripped-back bag of the pair."),
 "small-heritage-range-bucket": ("Small Heritage Range Bucket", "Five colourways", "125",
   "This 18oz waxed canvas bucket has a full-grain leather handle and a nylon lining, and it holds about 50 balls. Use it for a chipping session, or keep the balls from courses you have played on a shelf."),
 "canvas-club-pouch": ("Canvas Club Pouch", "Three colourways", "50",
   "This two-tone canvas zip pouch with a leather pull is 10 inches long, sized for tees, balls, ball marks, a charger and earbuds. At $50 it is the least expensive way into the brand."),
 "small-club-tote": ("Small Club Tote", "Navy", "65",
   "An open-top canvas tote sized for a pair of spikes, a hat and a light layer, with a slip pocket on the outside. It doubles as a lunch bag, or carries three bottles of wine as a host gift."),
 "savannah-golf-shoe-bag": ("Savannah Golf Shoe Bag", "Three colourways", "125",
   "This lightweight shoe bag is coated 1000-denier nylon with an interior divider, leather-trimmed handles and two outside pockets. It fits most golf shoes up to a US men&rsquo;s 15, and it is the one Golf Digest singled out."),
 "heritage-golf-shoe-bag": ("Heritage Golf Shoe Bag", "Waxed canvas", "149",
   "The waxed canvas version has a padded divider, full-grain leather handles and a zip pocket on the front for a phone or keys. It is the one to monogram with a club crest."),
 "heritage-leather-golf-shoe-bag": ("Heritage All Leather Golf Shoe Bag", "Chestnut", "249",
   "The same shape comes in full-grain leather, with brass zip sliders and leather pulls. Hudson Sutler pitches it as a gift for golf pros and club members, and it is the most polished thing in the range."),
 "montauk-cooler-bag": ("Montauk Cooler Bag", "Three colourways", "159",
   "This flip-top cooler has an 18oz canvas outside, a waterproof vinyl base, a welded liner and half an inch of foam. The shoulder strap comes off, and it goes from the course to the lake without looking like a cooler."),
 "kiawah-cooler-backpack": ("Kiawah Cooler Backpack", "Grey or navy", "199",
   "This roll-top cooler backpack is coated nylon with a welded waterproof liner and padded straps. It keeps your hands free for everything else you are carrying to the first tee or the boat."),
 "heritage-cooler-bag": ("Heritage Cooler Bag", "Waxed canvas", "185",
   "Hudson Sutler takes its best-selling cooler and upgrades it with waxed canvas, full-grain leather trim and brass hardware. It keeps the half inch of insulation, the welded liner and the removable strap."),
 "wilmington-duffel-with-shoe-compartment": ("Wilmington Duffel", "With shoe compartment", "199",
   "This barrel duffel in coated 1000-denier nylon has leather handles and a separate outside compartment for spikes or wet gear. It sits between the Commuter and the Weekender in size, right for a locker or one night away."),
 "heritage-weekender-1": ("Heritage Weekender", "Waxed canvas", "299",
   "PGA.com singled this out at the PGA Show: 18oz waxed canvas, full-grain leather handles, a side-access shoe compartment and a padded laptop sleeve. It is carry-on size, and the canvas gets better the more it gets beaten up."),
 "medium-chatham-duffel-bag": ("Medium Chatham Duffel", "Two colourways", "155",
   "This is Hudson Sutler&rsquo;s original barrel duffel in water-resistant canvas with a nylon base, rust-proof zips and an inside valuables pocket. It is the gym-to-weekend bag."),
 "heritage-leather-weekender-bag": ("Heritage All Leather Weekender", "Chestnut or espresso", "399",
   "The Weekender comes in hand-selected pebbled aniline leather, with the same laptop sleeve and shoe compartment. It is lighter than it looks, and it will pick up a patina."),
 "charleston-garment-bag": ("Charleston Garment Bag", "Charcoal and navy", "165",
   "This nylon garment bag holds two suits, with a diagonal zip and an outside pocket for shoes. It is the one for the wedding weekend, and a monogram makes it a groomsman gift."),
 "yorktown-toiletry-bag": ("Yorktown Toiletry Bag", "Hunter green or navy", "75",
   "This compact canvas toiletry bag has a spill-resistant nylon base and lining, and it is sized for TSA-friendly bottles."),
 "heritage-shave-kit": ("Heritage Shave Kit", "Waxed canvas", "115",
   "The waxed canvas dopp kit has a leather grab loop, a brass YKK zip and room for a week of travel-size bottles."),
 "heritage-waxed-canvas-pouch": ("Heritage Waxed Canvas Pouch", "Waxed canvas", "72",
   "This zip pouch in 18oz waxed canvas has a full-grain leather base and an inside divider. It slips into a golf bag or the Weekender."),
 "flatiron-backpack-20l": ("Flatiron Backpack", "Navy", "199",
   "This everyday backpack in coated nylon has a padded laptop sleeve, a removable pouch for chargers and earbuds, and padded straps. It is the bag for the flight to the golf trip."),
}

SECTIONS = [
    ("course", "On the Course", "on-the-course",
     ["hudson-looper-bag", "hudson-feather-lite-golf-bag", "small-heritage-range-bucket", "canvas-club-pouch", "small-club-tote"],
     "<strong>Five pieces &middot; $50&ndash;$399</strong>Hudson Sutler makes two carry bags, the Looper and the new Featherlite, plus a range bucket, a pouch and a small tote for the clubhouse."),
    ("shoes", "Shoe Bags", "shoe-bags",
     ["savannah-golf-shoe-bag", "heritage-golf-shoe-bag", "heritage-leather-golf-shoe-bag"],
     "<strong>Three shoe bags &middot; $125&ndash;$249</strong>The shoe bag is what the brand is known for in golf, in nylon, waxed canvas or full-grain leather."),
    ("coolers", "Coolers", "coolers",
     ["montauk-cooler-bag", "kiawah-cooler-backpack", "heritage-cooler-bag"],
     "<strong>Three coolers &middot; $159&ndash;$199</strong>Each one has a welded waterproof liner, for a summer round or a day on the lake."),
    ("trip", "The Golf Trip", "the-golf-trip",
     ["wilmington-duffel-with-shoe-compartment", "heritage-weekender-1", "medium-chatham-duffel-bag", "heritage-leather-weekender-bag", "charleston-garment-bag"],
     "<strong>Five bags &middot; $155&ndash;$399</strong>Three duffels have a shoe compartment built in, and the garment bag handles the dinner jacket."),
    ("small", "Small Goods", "small-goods",
     ["yorktown-toiletry-bag", "heritage-shave-kit", "heritage-waxed-canvas-pouch", "flatiron-backpack-20l"],
     "<strong>Four pieces &middot; $72&ndash;$199</strong>Two toiletry bags, a waxed pouch and the backpack you carry on the plane."),
]

PQ = {
    "steps": ("It takes our team of artisans over 200 steps to make a single bag by hand.", "Hudson Sutler, on its New Jersey factory"),
    "digest": ("This is probably the coolest shoe bag that you can buy.", "Golf Digest, on the Savannah, as quoted by Hudson Sutler"),
    "need": ("We build our bags with everything you need and nothing you don&rsquo;t.", "Hudson Sutler"),
}

BANDS = {
    "trip": ("Photography &middot; Hudson Sutler&rsquo;s own", "The bags where they are meant to be: on the course, in the back of the car, on the range.",
             [("band-c1", "Two golfers on a green in autumn with trees behind", "On the course"),
              ("band-c2", "A woman lifting a Hudson Sutler duffel out of the back of an SUV", "Loading up"),
              ("band-c3", "A golfer swinging on a range with a Hudson Sutler duffel on the grass", "On the range")]),
    "factory": ("Photography &middot; the factory floor", "Cut, sewn and stitched in North Bergen, New Jersey.",
             [("band-b1", "A leather handle being stitched onto waxed canvas beside an American flag label", "The handle"),
              ("band-b2", "A Hudson Sutler worker cutting canvas with an industrial cutter", "Cutting"),
              ("band-b3", "Hands guiding leather through a sewing machine", "Sewing")]),
    "life": ("Photography &middot; Hudson Sutler&rsquo;s own", "The brand shoots its bags in use: a duffel on the ferry, wine totes on a tailgate, a monogram on a garment bag.",
             [("band-a1", "A man carrying a navy canvas duffel with leather handles on a ferry", "On the ferry"),
              ("band-a2", "Three waxed canvas wine totes on a truck tailgate with a dog behind", "Wine totes"),
              ("band-a3", "A navy garment bag monogrammed JTC with a white shirt on a hanger", "Monogrammed")]),
}

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Why Hudson Sutler, and why for Austin golfers now? Because fall is golf-trip season here. The heat breaks, and the group chat starts planning a weekend at Horseshoe Bay, a run out to the Hill Country or a flight to somewhere with a proper links course. Hudson Sutler makes everything that trip needs, the carry bag, the shoe bag, the cooler and the duffel, and it cuts, sews and embroiders all of it on its own factory floor in North Bergen, New Jersey, a few miles from Midtown Manhattan.</p>
    <p>It is for the golfer who walks and carries, travels a few times a year and likes things that get better with wear: waxed canvas that creases and darkens, and leather handles that pick up a patina. It is also the easiest group gift in golf. Almost everything can be monogrammed, and custom orders ship in four to six weeks, so a bachelor trip or a member-guest team can all show up with matching bags.</p>
    <p>Is it good value? For bags made by hand in the US, the prices are fair, and a few pieces stand out. Start with the $125 Savannah shoe bag. The Heritage Weekender at $299, in 18oz waxed canvas with a shoe compartment and a laptop sleeve, is the piece that makes the case for the brand. For an August round at Muny, the $159 Montauk cooler has a welded liner and half an inch of foam. The golf bags are harder to call. At $365 and $399, the Featherlite and Looper are serious money for a carry bag, so buy one if you want your bag to match the rest of the kit.</p>
    <p>Prices were read from Hudson Sutler&rsquo;s store on 30 September 2026, in US dollars. Ground shipping is free over $250, and unused items can be returned within 30 days, except anything personalised.</p>
    <h2 class="products-hdr btk-story-hdr">The Story</h2>
    <p>Hudson Sutler makes bags for golf and travel, and it makes them itself. Every bag is cut, sewn and embroidered at its factory in North Bergen, and the brand says a single bag passes through more than ten sets of hands. The materials are industrial: 18oz canvas, waxed canvas, 1000-denier coated nylon and full-grain leather. InsideHook was already calling it a New York maker of colourful, utilitarian canvas bags in 2017.</p>
    <p>Golf has become a bigger part of the business. At the 2026 PGA Show, co-founder Mike Chepucavage launched the Featherlite, a 3.5-pound stand bag, and showed the Heritage Weekender beside it. Readers of The Grassy Issue will know the name from Sugarloaf Social Club&rsquo;s <a href="/drops/ssc-hidden-gem-collection">Hidden Gem</a> cooler, which Hudson Sutler made.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>North Bergen, New Jersey</span></div>
      <div class="sidebar-detail"><span class="l">Made</span><span>In its own New Jersey factory</span></div>
      <div class="sidebar-detail"><span class="l">Co-founder</span><span>Mike Chepucavage</span></div>
      <div class="sidebar-detail"><span class="l">Custom</span><span>Monograms; made to order in 4&ndash;6 weeks</span></div>
      <div class="sidebar-detail"><span class="l">Shipping</span><span>Free ground over $250</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$50&ndash;$399</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Heritage Weekender, $299</span></div>
      <a href="https://www.hudsonsutler.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit Hudson Sutler &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#HudsonSutler</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#MadeInUSA</span>
        <span class="hashtag">#GolfTrip</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

FAQ = [
    ("Where are Hudson Sutler bags made?",
     "In the brand's own factory in North Bergen, New Jersey, a few miles from Midtown Manhattan. Every bag is cut, sewn and embroidered there."),
    ("Can Hudson Sutler bags be personalised?",
     "Yes. Most bags can be monogrammed, and personalised orders take an extra 7 to 10 days to ship. Custom made-to-order bags take four to six weeks. Personalised items cannot be returned."),
    ("What golf bags does Hudson Sutler make?",
     "Two carry bags: the Looper 2.0 ($399, 4.2 lb) and the Featherlite ($365, 3.5 lb), which launched at the 2026 PGA Show."),
    ("Which Hudson Sutler shoe bag should I buy?",
     "The Savannah ($125) in coated nylon is the lightest and the one Golf Digest praised. The Heritage ($149) is waxed canvas with leather handles, and the all-leather version is $249."),
    ("Is Hudson Sutler good for an Austin golf trip?",
     "Yes. The Heritage Weekender ($299) and Wilmington Duffel ($199) have shoe compartments built in, and the Montauk cooler ($159) has a welded liner for hot rounds. Ground shipping is free over $250."),
]


def pq(key):
    txt, attr = PQ[key]
    return (f'\n<!-- TGI-HS-PQ-{key} -->\n<div class="pull-quote">\n  <div class="pull-quote-inner">'
            f'&ldquo;{txt}&rdquo;<span class="pull-quote-attr">&mdash; {attr}</span></div>\n</div>\n'
            f'<!-- /TGI-HS-PQ-{key} -->\n')

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
    label = H.unescape(f"Hudson Sutler {name} {detail}").replace('"', "")
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
            items.append({"@type": "ListItem", "position": pos, "url": SHOP + h, "name": H.unescape(f"Hudson Sutler {P[h][0]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-09-30", "dateModified": "2026-09-30",
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
            {"@type": "ListItem", "position": 3, "name": "Hudson Sutler", "item": URL}]},
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
    assert len(ids) == 20 == len(set(ids)) and set(ids) == set(P)
    for h in ids:
        assert FR.get(h), h
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Hudson Sutler</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>North Bergen, New Jersey &middot; made in the USA</span><span class="dot"></span>
    <span>20 pieces &middot; $50&ndash;$399</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A golfer walking down a fairway under oak trees with a navy Hudson Sutler carry bag on his back" fetchpriority="high" /></div></div>
"""
    body += TAKE + band("trip")
    n = 1
    s, n = section(SECTIONS[0], n); body += s + band("factory") + pq("steps")
    s, n = section(SECTIONS[1], n); body += s + pq("digest")
    s, n = section(SECTIONS[2], n); body += s + band("life")
    s, n = section(SECTIONS[3], n); body += s + pq("need")
    s, n = section(SECTIONS[4], n); body += s
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
    for leak in ("Manors Revisited", "Nicklaus", "Macade", "Hewit"):
        if leak in above:
            bad.append(f"should not appear: {leak}")
    if fin.count('class="product-card"') != 20:
        bad.append("card count")
    for k, (t, _) in PQ.items():
        if fin.count(t[:50]) != 1:
            bad.append(f"pq {k}")
    if above.count('class="ig-grid"') != 3:
        bad.append("band count")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", above), re.I):
        bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file():
            bad.append(f"missing {f}")
    if bad:
        OUT.unlink()
        sys.exit("! removed. " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
