#!/usr/bin/env python3
"""build-steakhouses.py — The Best Steakhouses in Austin: 12 Independents.
30 September 2026. A Field Note.

Lenny: "let's do a field note about the best steak houses in Austin", then after
round one: "No on any chains, add Jacobys and do better research", then "yes, look
on instagram for good steak pics, okay if the restaurant has a few locations within
texas just no nationwide chains".

PICKS: research/steakhouses/options2.json (ownership checked; chains excluded with
evidence). Michelin from the Guide's own Austin listing (2025 guide); 2026 Texas
selection lands 8 Oct 2026, recheck then. Our pick: Jeffrey's.
FACTS: dishes, prices and hours from each restaurant's own menu/site, 30 Sep 2026.
PHOTOS: own sites, plus the restaurants' own Instagram for Jeffrey's, Hestia and
Jacoby's (their sites had no plated-steak photo). No press photos. No quotes.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "best-steakhouses-in-austin"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/steakhouses-2026"
FR = {k: [{"local": f"{IMG}/{f}.jpg"} for f in v]
      for k, v in json.loads((ROOT / "research/steakhouses/frames.json").read_text()).items()}

TITLE = "The Best Steakhouses in Austin: 12 Independents"
DESC = ("Twelve independent Austin steakhouses, from Jeffrey's live-oak ribeye to Hestia's Michelin-starred "
        "hearth and Jacoby's own ranch beef. Prices checked 30 Sep 2026.")
H1 = "The Best Steakhouses in Austin &mdash; 12 Independents"
CHECK = "Check before you go"

T = {
 # ---- Downtown
 "hestia": ("Hestia", "Downtown &middot; 607 W 3rd St", "30-day dry-aged Texas Wagyu ribeye &middot; $143",
   "Hestia is not a steakhouse, strictly, but some of the best steak in town is cooked here, over a 20-foot hearth. It holds a Michelin star, and the Wagyu ribeye is one of two steaks on a short &agrave; la carte menu; the Texas Wagyu bavette is $68. Book it for the occasion, not the post-round dinner.",
   "Tue&ndash;Thu &amp; Sun 5:30&ndash;10pm &middot; Fri&ndash;Sat 5:30&ndash;11pm &middot; closed Mon", "https://hestiaaustin.com/"),
 "vanhorns": ("VanHorn&rsquo;s", "Downtown &middot; 238 W 2nd St", "Dry-aged bone-in ribeye, 20oz &middot; $118",
   "VanHorn&rsquo;s is a wood-panelled, red-banquette chophouse in the New York style, with martinis and a raw bar. The dry-aged ribeye and the 16oz dry-aged New York strip ($85) lead the dinner menu, and the porterhouse for two ($185) shows up at lunch. Happy hour runs 3 to 5:30 every day.",
   "Mon&ndash;Fri 11am&ndash;10pm &middot; Sat&ndash;Sun 10am&ndash;10pm", "https://vanhornsatx.com/"),
 "jcarvers": ("J. Carver&rsquo;s", "Downtown &middot; 509 Rio Grande St", "10oz filet, carpet bag style &middot; $74",
   "This oyster bar and chophouse has a wood-burning grill and steaks aged by Fred Linz in Chicago. Order the filet the old way, carpet bag style, with fried oysters and b&eacute;arnaise, or the 30-day dry-aged porterhouse for two at $4.95 an ounce. The dress code rules out gym shorts and athletic wear, so change after the round.",
   "Daily 5&ndash;10pm", "https://www.jcarveratx.com/"),
 "driskill": ("The Driskill Grill", "Downtown &middot; 117 E 7th St, in The Driskill", "26oz Dean &amp; Peeler ribeye, dry-aged 28 days &middot; $175",
   "The grand hotel dining room reopened this year as a steakhouse, run by the Jeffrey&rsquo;s group with April Bloomfield on creative direction. Prime rib is carved tableside for $90, the big cuts are dry-aged on site, and the butcher&rsquo;s cuts start at $43 for a bavette, the value play in an expensive room.",
   "Dinner nightly 4:30&ndash;10:30pm", "https://www.thedriskillgrill.com/"),
 "garrison": ("Garrison", "Downtown &middot; 101 Red River St, at the Fairmont", "25oz Texas Wagyu ribeye",
   "Garrison cooks over post oak in an open kitchen at the Fairmont, and the Michelin Guide recommends it. The 25oz Texas Wagyu ribeye and a 40oz oak-grilled porterhouse are the big orders. Garrison does not post prices online.",
   "Tue&ndash;Wed 5&ndash;9pm &middot; Thu&ndash;Sat 5&ndash;10pm &middot; closed Sun&ndash;Mon", "https://www.garrisongrill.com/"),
 # ---- Clarksville & Central
 "jeffreys": ("Jeffrey&rsquo;s", "&#9733; Our pick &middot; Clarksville &middot; 1204 West Lynn St", "26oz dry-aged bone-in ribeye &middot; $165",
   "This is the steakhouse Austin measures the rest against. Steaks are grilled over local live oak and finished under a 1,200-degree broiler; the Niman Ranch ribeye is dry-aged 32 days, and the 8oz filet comes from Dean &amp; Peeler in Floresville, Texas, for $72. The Michelin Guide recommends it, Austin Chronicle readers voted it the city&rsquo;s best steak this year, and Muny is six minutes away.",
   "Daily 4:30&ndash;11pm", "https://jeffreysofaustin.com/"),
 "alc": ("ALC Steaks", "12th &amp; Lamar &middot; 1205 N Lamar Blvd", "22oz bone-in ribeye &middot; $74",
   "Austin Land &amp; Cattle has been at it since 1993, and it is still the fairest-priced proper steakhouse in central Austin. Steaks come with a side, a 12oz ribeye is $57, and the house move is ALC style, a peppercorn and blue cheese crust for $8. The buffalo-style lamb chops are $27, and Muny is six minutes away.",
   "Mon&ndash;Thu 4&ndash;10pm &middot; Fri&ndash;Sat 4&ndash;11pm &middot; closed Sun", "https://alcsteaks.com/"),
 # ---- East
 "jacobys": ("Jacoby&rsquo;s", "East Cesar Chavez &middot; 3235 E Cesar Chavez St", "Steak frites &middot; market price",
   "The beef comes from the Jacoby family&rsquo;s own ranch in Melvin, Texas, dry-aged 21 to 28 days and served on the Colorado River in East Austin. Steaks change nightly, so call ahead for the butcher&rsquo;s cut, and go on a Thursday, when the steak frites are half price. The chicken fried steak is $29, and weekend brunch has a smoked ribeye benedict.",
   "Wed&ndash;Thu 5&ndash;9pm &middot; Fri&ndash;Sat 5&ndash;10pm &middot; brunch Sat&ndash;Sun 10am&ndash;2pm", "https://www.jacobysaustin.com/"),
 "daidue": ("Dai Due", "Manor Road &middot; 2406 Manor Rd", "95-day dry-aged Texas Wagyu ribeye, 20oz &middot; $162",
   "Jesse Griffiths&rsquo; butcher shop and supper club cooks only Texas meat, and this ribeye spends 95 days dry-aging before it reaches the beef-tallow kitchen. Dai Due has a Michelin Bib Gourmand and a Green Star, the menu changes often, and the $26 dry-aged longhorn cheeseburger is the value order. Morris Williams is five minutes away.",
   CHECK, "https://www.daidue.com/"),
 "justines": ("Justine&rsquo;s", "East 5th &middot; 4710 E 5th St", "Steak frites, 12oz Angus ribeye &middot; $58",
   "Justine&rsquo;s is a moody French brasserie that stays open late, and the steak frites is the reason to go: a wood-grilled 12oz grass-fed Angus ribeye, or a Texas Wagyu New York strip for $75. It was a finalist for best steak in the Austin Chronicle readers&rsquo; poll this year.",
   CHECK, "https://justines1937.com/"),
 # ---- North & the lake
 "bartletts": ("Bartlett&rsquo;s", "Allandale &middot; 2408 W Anderson Ln", "100-hour marinated ribeye",
   "Bartlett&rsquo;s is the north-side neighbourhood grill, locally owned, with steaks cooked over hardwood. The famous order is the 14oz ribeye marinated for 100 hours in pineapple, sesame and ginger, and the prime rib comes with a rosemary salt crust. House rule: no phones in the dining room. The online menu lists no prices.",
   "Sun&ndash;Thu 11am&ndash;9pm &middot; Fri&ndash;Sat 11am&ndash;10pm", "https://bartlettsaustin.com/"),
 "steiner": ("Steiner Ranch Steakhouse", "Lake Travis &middot; 5424 Steiner Ranch Blvd", "Cowboy ribeye, 22oz bone-in",
   "This is the far-west destination: a ranch-themed steakhouse above Lake Travis with Hill Country views and live music on the patio every night. Order the bone-in cowboy ribeye after a round out west, and go on a Wednesday for 20% off bottles. The online menu lists no prices.",
   CHECK, "https://www.steinersteakhouse.com/"),
}

SECTIONS = [
    ("downtown", "Downtown", "downtown", ["hestia", "vanhorns", "jcarvers", "driskill", "garrison"],
     "<strong>Five rooms &middot; closest to Butler</strong>Downtown has the Michelin-starred hearth, two classic chophouses, a reborn hotel dining room and post oak at the Fairmont. Several of them have a dress code."),
    ("central", "Clarksville &amp; Central", "clarksville-and-central", ["jeffreys", "alc"],
     "<strong>Two stops &middot; six minutes from Muny</strong>Our pick and the best-value steakhouse in the city sit a few blocks apart, both a short drive from Lions."),
    ("east", "East Austin", "east-austin", ["jacobys", "daidue", "justines"],
     "<strong>Three stops &middot; ranch to late night</strong>The East Side has beef from a family ranch, a butcher shop that dry-ages for 95 days and steak frites until midnight."),
    ("north", "North &amp; the Lake", "north-and-the-lake", ["bartletts", "steiner"],
     "<strong>Two stops &middot; out of the core</strong>Bartlett&rsquo;s anchors the north side, and Steiner Ranch pairs with a round out toward Lake Travis."),
]

BANDS = {}

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Austin is not a steakhouse town the way Dallas and Houston are, and that works in its favour. The best steaks here come from independents: a Clarksville bistro that grills over live oak, a butcher shop that dry-ages ribeyes for 95 days, a family that serves beef from its own ranch, and a live-fire kitchen with a Michelin star. There is not a national chain on it.</p>
    <p>If you book one, make it Jeffrey&rsquo;s. It is the most complete steak dinner in the city, six minutes from Muny, and the 26oz dry-aged ribeye is the order. For a fair price, ALC Steaks has been getting it right since 1993. For the big occasion, Hestia.</p>
    <p>Our favourite, though, is Jacoby&rsquo;s. It is the one we keep going back to: a family that raises its own cattle in Melvin, Texas, dry-ages the beef and serves it in a reclaimed-wood room on the Colorado River in East Austin. It is not white-tablecloth, and that is the appeal. Go on a Thursday, when the steak frites and martinis are half price, and ask what the butcher&rsquo;s cut is that night.</p>
    <p>Prices are from each restaurant&rsquo;s own menu, read on 30 September 2026, and where a menu does not publish prices we leave them off. Several downtown rooms have a dress code, so change after the round. The Michelin Guide&rsquo;s 2026 Texas selection comes out on 8 October, so the stars and recommendations here may move. For more, see our <a href="/drops/best-chicken-sandwiches-in-austin">chicken sandwich field note</a> and <a href="/drops/austin-food-truck-field-guide">food truck field guide</a>.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Field Note</div>
      <div class="sidebar-detail"><span class="l">Stops</span><span>12, all independent</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Jeffrey&rsquo;s, 26oz ribeye $165</span></div>
      <div class="sidebar-detail"><span class="l">Our favourite</span><span>Jacoby&rsquo;s, Thursday steak frites</span></div>
      <div class="sidebar-detail"><span class="l">Best value</span><span>ALC Steaks, 12oz ribeye $57</span></div>
      <div class="sidebar-detail"><span class="l">Michelin</span><span>Hestia (star), Dai Due (Bib), Jeffrey&rsquo;s &amp; Garrison (recommended)</span></div>
      <div class="sidebar-detail"><span class="l">Near a muni</span><span>Jeffrey&rsquo;s &amp; ALC, ~6 min from Lions</span></div>
      <div class="sidebar-detail"><span class="l">Checked</span><span>30 Sep 2026</span></div>
      <a href="#clarksville-and-central" class="sidebar-cta">Start with our pick &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#AustinEats</span>
        <span class="hashtag">#Steakhouse</span>
        <span class="hashtag">#MuniGolf</span>
        <span class="hashtag">#ATX</span>
      </div>
    </div>
  </aside>
</section>
"""

FAQ = [
    ("What is the best steakhouse in Austin?",
     "Our pick is Jeffrey's in Clarksville, for its live-oak-grilled, 32-day dry-aged 26oz ribeye ($165). The rest of our twelve: Hestia, VanHorn's, J. Carver's, The Driskill Grill, Garrison, ALC Steaks, Jacoby's, Dai Due, Justine's, Bartlett's and Steiner Ranch Steakhouse. All are independent."),
    ("Which Austin steakhouses are in the Michelin Guide?",
     "In the 2025 guide, Hestia holds one star, Dai Due has a Bib Gourmand and a Green Star, and Jeffrey's and Garrison are Recommended. The 2026 Texas selection is announced on 8 October 2026."),
    ("Which Austin steakhouse is closest to a golf course?",
     "Jeffrey's (1204 West Lynn) and ALC Steaks (1205 N Lamar) are each about six minutes from Lions Municipal. Downtown spots like VanHorn's, Hestia and Garrison are about five to seven minutes from Butler Pitch & Putt, and Dai Due is about five minutes from Morris Williams."),
    ("Where can I get a good steak in Austin for under $60?",
     "ALC Steaks has a 12oz ribeye for $57 with a side, Justine's steak frites is $58, the Driskill Grill's butcher's cuts start at $43, and Jacoby's steak frites is half price on Thursdays."),
    ("Do Austin steakhouses have a dress code?",
     "Some do. J. Carver's asks for proper attire and rules out gym shorts and athletic wear. If you are coming straight off the course, change first or choose a more relaxed spot like ALC Steaks, Bartlett's or Jacoby's."),
]

def band(key):
    kick, line, items = BANDS[key]
    figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>'
                     for f, alt, cap in items)
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <p class="cat-kicker"><strong>{kick}</strong>{line}</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


def card(k, idx):
    name, where, dish, copy, hours, url = T[k]
    fr = [f["local"] for f in FR[k]]
    label = H.unescape(name).replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; photo {j+1} of {len(fr)}" loading="lazy" /></div>'
                   for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>'
                   for j in range(len(fr)))
    return (f'<div class="product-card" id="stop-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">No. {idx:02d} &middot; {where}</div>'
            f'<div class="product-name">{name} &middot; {dish}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<div class="product-desc" style="font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;opacity:.7;margin-top:8px">{hours}</div>'
            f'<a href="{H.escape(url)}" target="_blank" rel="noopener" class="product-link">Hours &amp; menu &#8599;</a></div></div>')


def section(sec, n0):
    key, h2, anchor, ids, kicker = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} Stops</div>\n'
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
        for k in ids:
            items.append({"@type": "ListItem", "position": pos, "url": T[k][5], "name": H.unescape(T[k][0])})
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
            {"@type": "ListItem", "position": 2, "name": "Field Notes", "item": "https://thegrassyissue.com/#feed"},
            {"@type": "ListItem", "position": 3, "name": "Best Steakhouses in Austin", "item": URL}]},
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
    ids = [k for s in SECTIONS for k in s[3]]
    assert len(ids) == 12 == len(set(ids)) and set(ids) == set(T)
    for k in ids:
        assert FR.get(k), f"{k} has no photos"
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Field Notes</a><span>/</span>
  Best Steakhouses in Austin</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>September 30, 2026</span><span class="dot"></span>
    <span>Austin &middot; 3 parts of town</span><span class="dot"></span>
    <span>12 steakhouses &middot; checked 30 Sep</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A sliced dry-aged bone-in ribeye with charred peppers on an oval plate at The Driskill Grill" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for sec in SECTIONS:
        if sec[0] in BANDS:
            body += band(sec[0])
        s, n = section(sec, n)
        body += s
    body += faq_html()
    out = head_top() + head_rest + body + tail
    print(f"  {n-1} stops")
    if not apply_:
        print("  dry run — pass --apply")
        return
    OUT.write_text(out, encoding="utf-8")
    verify()


def verify():
    fin = OUT.read_text(encoding="utf-8")
    bad = []
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    for leak in ("Manors Revisited", "Fogo", "Perry", "Bob&rsquo;s"):
        if leak in above:
            bad.append(f"should not appear: {leak}")
    if fin.count('class="product-card"') != 12:
        bad.append("card count")
    if 'class="pull-quote"' in above:
        bad.append("a pull-quote got in")
    if above.count('class="ig-grid"') != 0:
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
