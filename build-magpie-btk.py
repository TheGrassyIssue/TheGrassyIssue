#!/usr/bin/env python3
"""build-magpie-btk.py — Brand to Know: Magpie Supply (cloned from build-palm-btk.py). 2 October 2026.

Lenny: "Let's also do a brand to know - https://magpie-supply.com/", approved the TGI Take ("looks good, let's build it").
All 10 products run (the whole store). FACTS: catalogue, prices and stock read from the Squarespace JSON on 2 Oct 2026
(research/magpie/items.json); story from magpie-supply.com/our-story (quoted verbatim). Founder not named on the site.
PHOTOS: Magpie's own store and site images, localised to /images/magpie-supply.

--- original Palm docstring follows ---

Lenny: "Let's do a brand to know - https://palmgolfco.com/", then "looks good" on the 38-option sheet
(research/palm/options.json), so all 38 run. FACTS: catalogue read from palmgolfco.com/products.json on 2 Oct 2026;
story and founder quotes from MyGolfSpy, "Palm Golf Swings And Smiles Its Way To Cult Following" (Sean Fairholm,
21 Mar 2025, a brand-story feature); the MyGolfSpy comfort line is quoted on Palm's own homepage. Product copy written
from each listing and its photos. PHOTOS: Palm's own store images, localised to /images/palm-golf.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"

TITLE = "Magpie Supply: Denver's Small-Batch Leather Golf Brand"
DESC = ("Brand to Know: Magpie Supply, a one-person Denver leather shop making scorecard holders, tee rings, "
        "hammered repair tools and a RossCo headcover. All ten pieces, with prices.")
H1 = "Brand to Know: Magpie Supply, the Denver Leather Shop Making Golf's Small Things"
BC = "Magpie Supply"
SLUG = "brand-to-know-magpie-supply"
IMG = "/images/magpie-supply"
SHOP = "https://magpie-supply.com"

P = {
 "m01": ("Magpie Supply", "Scorecard Holder", "$75", "/on-the-course/p/scorecard-holder",
   "Black full-grain leather with navy stitching, made in Denver, for golfers who would rather keep score in pencil than in an app. It fits a standard scorecard, slips into a back pocket, and the clasp holds a stack of bills for the side game."),
 "m02": ("Magpie Supply", "Tee Ring", "$25", "/on-the-course/p/tee-ring",
   "A leather key ring that holds up to four tees, so you are not digging for a broken one on the par 3. The cheapest thing in the store and the one you will reach for most."),
 "m06": ("Magpie Supply", "The Bag Tag", "$40", "/on-the-course/p/the-bag-tag",
   "Full-grain leather with navy thread and room for your address inside. It works on a Sunday bag, a travel bag or a duffel."),
 "m07": ("Magpie Supply", "Staple Sunglass Case", "$45", "/on-the-course/p/staple-sunglasses-case",
   "Rough-out leather with a snap, for the spare pocket in your bag when the sun goes behind the clouds. Rough-out scuffs and darkens with use, which is the point."),
 "m03": ("Magpie Supply x Queen City Quilt Co.", "The Quilted Pouch", "$55", "/on-the-course/p/the-quilted-pouch",
   "A black-and-navy quilted valuables pouch with a drawstring, made in Denver by the founder's wife at Queen City Quilt Co. By Magpie's count it holds 39 tees, 17 ball markers, five repair tools and three balls."),
 "m04": ("Magpie Supply", "Hammered Copper Repair Tool", "$50", "/on-the-course/p/hammered-brass-repair-tool",
   "Hand-hammered copper, made in Georgia with the founder's friend Chuck and stamped MS on the front and DS on the back. Copper darkens as you carry it. One was left when we checked."),
 "m05": ("Magpie Supply", "Hammered Brass Repair Tool", "$50", "/on-the-course/p/hammered-copper-repair-tool",
   "The same hand-hammered tool in brass, which ages to a duller gold. Also made in Georgia with Chuck, with the same MS and DS stamps."),
 "m08": ("Magpie Supply x RossCo Golf", "The Magpie x RossCo Headcover", "$100", "/on-the-course/p/the-magpie-tweed-headcover",
   "Made in Bandon, Oregon by RossCo Golf: an aqua crown with the magpie stitched on it and a Pendleton grey shaft. It fits a driver or a 3-wood."),
 "m09": ("Magpie Supply", "The Staple 5 Panel", "$45", "/to-wear/p/the-staple-5-panel",
   "A white five-panel with the magpie on the front and the MS logo on the side, made in Colorado. Magpie chose white on purpose, so the sweat ring shows."),
 "m10": ("Magpie Supply", "Staple Sun Shirt", "$70", "/to-wear/p/staple-sun-shirt",
   "A lightweight hooded long sleeve in sand, made in the USA, for early tee times and hot afternoons. The magpie is on the left chest and the wordmark on the cuff. Sizes M to 2XL."),
}
SECTIONS = [
 ("The Leather", "leather", ["m01","m02","m06","m07"],
  "<strong>Four pieces &middot; $25&ndash;$75</strong>This is where Magpie started: full-grain and rough-out leather cut and stitched in Denver, with the same navy thread on everything. Each is a small thing you use every round."),
 ("Made With Friends", "collabs", ["m03","m04","m05","m08"],
  "<strong>Four pieces &middot; $50&ndash;$100</strong>Each of these is made by someone the founder knows: the quilted pouch by the founder&rsquo;s wife, the repair tools with a friend, Chuck, in Georgia, and the headcover by RossCo Golf in Bandon."),
 ("To Wear", "wear", ["m09","m10"],
  "<strong>Two pieces &middot; $45&ndash;$70</strong>A white five-panel and a hooded sun shirt, both made in the USA, both with the magpie on them."),
]
N = 10
PQ = {
 "collabs": ("Nice clubs deserve nicer sleeping bags and these are just that.", "Magpie Supply, on the RossCo headcover"),
 "wear": ("It&rsquo;s white, because we want to see it worn and we want to see that ring of sweat.", "Magpie Supply, on the Staple 5 Panel"),
}
BANDS = {
 "collabs": ("Always above par", "Magpie's own photos, from the course in Denver.", [("band-l1","The Magpie x RossCo headcover on a golf bag on the grass, a golfer on the tee behind","The RossCo cover"),("band-l4","A golfer writing his score in a Magpie leather scorecard holder","The scorecard holder"),("band-l5","A Magpie hammered repair tool on a green beside a pitch mark","The repair tool")]),
 "wear": ("Where the magpies gather", "", [("band-l2","Two golfers by their bags at a Denver course, one in the Magpie sun shirt","After the round"),("band-l3","A golfer at address in the Magpie Staple Sun Shirt","The Sun Shirt"),("band-l6","A golfer silhouetted at the top of his swing at sunset","Last light")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Magpie Supply is the smallest brand we&rsquo;ve profiled, and that&rsquo;s what makes it good. The whole store is ten pieces, and almost every one is something you&rsquo;ll use on every round: a leather scorecard holder, a tee ring, a bag tag and a hammered pitch-mark repair tool. They&rsquo;re made in tiny batches and meant to age, so the leather picks up wear the more you use it.</p>
    <p>It started in Denver with a lost wallet in 2017. Replacing it turned into learning leatherwork, and wallets became totes, backpacks and duffels. Then, in the brand&rsquo;s own words, &ldquo;the focus shifted into curated pieces for golfers, because if your game doesn&rsquo;t look good, at least your bag can.&rdquo; The name comes from the magpies that gather on Denver&rsquo;s golf courses. It&rsquo;s still run by one person writing in the first person. The full-grain leather is stitched in Denver, the quilted pouches are made by the founder&rsquo;s wife at Queen City Quilt Co., the copper and brass repair tools are hammered in Georgia with &ldquo;my good buddy Chuck,&rdquo; and the headcover is made in Bandon, Oregon by RossCo Golf.</p>
    <p>Magpie is for golfers who still keep score on paper and want the small things in their bag to be well made. Stock is very low: one copper repair tool and two quilted pouches were left when we checked. If something catches your eye, buy it soon. Prices were read on Magpie&rsquo;s own store on 2 October 2026.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Denver, Colorado</span></div>
      <div class="sidebar-detail"><span class="l">Since</span><span>2017</span></div>
      <div class="sidebar-detail"><span class="l">Made in</span><span>Denver, Georgia and Bandon, Oregon</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$25&ndash;$100</span></div>
      <div class="sidebar-detail"><span class="l">Also</span><span>Custom orders for trips and events</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Scorecard Holder, $75</span></div>
      <a href="https://magpie-supply.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit Magpie Supply &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#MagpieSupply</span>
        <span class="hashtag">#AlwaysAbovePar</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#LeatherGoods</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("Where is Magpie Supply from?", "Denver, Colorado. It started in 2017 and is named for the magpies that gather on Denver's golf courses."),
 ("What does Magpie Supply make?", "Small leather golf accessories: a scorecard holder, a tee ring, a bag tag and a sunglass case, plus hammered repair tools, a quilted pouch, a RossCo headcover, a five-panel cap and a sun shirt. Prices ran from $25 to $100 on 2 October 2026."),
 ("Where are Magpie Supply products made?", "The leather goods and the quilted pouch are made in Denver, the repair tools in Georgia, the headcover in Bandon, Oregon by RossCo Golf, the cap in Colorado and the sun shirt in the USA."),
 ("Who makes the Magpie x RossCo headcover?", "RossCo Golf, in Bandon, Oregon. It has an aqua crown with the magpie stitched on it and a Pendleton grey shaft, fits a driver or a 3-wood, and cost $100 on 2 October 2026."),
 ("Does Magpie Supply do custom orders?", "Yes. Its site offers custom gear for golf trips and events."),
]
FRN = json.loads((ROOT / "research/magpie/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
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
         "url": URL, "image": og, "datePublished": "2026-10-02", "dateModified": "2026-10-02",
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
            f'    <div class="products-grid">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


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
    <span>Denver, Colorado</span><span class="dot"></span>
    <span>10 picks &middot; in stock 2 October 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Magpie Supply: the RossCo headcover on a golf bag, a golfer writing in the leather scorecard holder, and a golfer at address in the Staple Sun Shirt" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
    body += faq_html()
    out = head_top() + head_rest + body + tail
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
