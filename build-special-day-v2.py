#!/usr/bin/env python3
"""build-special-day-v2.py — rebuild of /drops/8-special-day-rounds-near-austin.
24 September 2026.

Lenny: "let's give this post some love- looking a little dated", then chose the
full rebuild: current house layout, a sharp hero, each course as its own entry
with its write-up, a band of the course's own photography and a card. Same URL.

WHAT IS KEPT. The copy. It was rewritten and fact-checked on 17 September 2026
and it is good: every course description, "A Word on What These Cost",
"Picking the Right One" and the FAQ (visible and JSON-LD) are lifted from the
pre-rebuild page, saved at research/special-day/original-2026-09-24.html, which
is what this script reads. So a rerun never reads its own output. Prices keep
their 17 September read date because that is when they were read.

WHAT IS NEW. Layout (Manors BTK shell, as the pants and fall-drops posts),
the hero (The Quarry at sunset, from quarrygolf.com), 3-5 photographs per course
from each course's own website, localised to images/special-day/v2/, a sidebar
that answers "which one?", and short practical card copy.

STANDARD TEMPLATE, NOT THE ONE-OFF. Lenny, after seeing a per-course layout:
"follow the normal template- that top 5 post was a one off". So each group
(Day Trips, Overnights) is one section: heading, kicker, one band of course
photography, then the usual three-across grid of cards. Each card carries the
original write-up and a multi-photo gallery of that course.

Dry run by default.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
ORIG = ROOT / "research/special-day/original-2026-09-24.html"
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "8-special-day-rounds-near-austin"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
V2 = "/images/special-day/v2"
PROSE = 'style="max-width:760px;font-size:16px;line-height:1.7;"'

# per course, in page order: (band images, card images, card copy)
IMGS = {
 0: (["c0-b0", "c0-b1", "c0-b2"], ["c0-c0", "c0-b0"],
     "Tee times book through the resort, and the rate depends on the day and on whether you are staying. The course is an Arthur Hills design at 7,300 yards and par 72."),
 1: (["c1-b0", "/images/austin-road-trip/falconhead-hole8.jpg", "/images/field-guide/falconhead.jpg"], ["c1-b2", "c1-b1"],
     "Falconhead prices dynamically, so the rate moves with the day and the tee time. Check the booking page before you rule it out."),
 2: (["c2-b0", "c2-b1", "c2-b2"], ["c2-c0", "c2-c1"],
     "Avery Ranch is semi-private, and public tee times go through its own booking page, so check the rate there."),
 3: (["c3-b0", "/images/field-guide/grey-rock.jpg", "c3-b2"], ["c3-b1", "c3-b0"],
     "Grey Rock sits twenty minutes from central Austin with golf and tennis on one property. Rates are on its booking page."),
 4: (["c4-b0", "c4-b1", "c4-c0"], ["/images/field-guide/star-ranch.jpg", "c4-b0"],
     "Rates read on 17 September 2026 were $85 to $99 Monday to Thursday, $129 to $139 on Fridays and weekends and $62 to $75 after 3pm."),
 5: (["c5-b0", "c5-b1", "c5-b2"], ["c5-c0", "/images/field-guide/vaaler-creek.jpg"],
     "Vaaler Creek charged $95 for 18 with a cart Monday to Thursday on 17 September 2026, and $75 on the twilight rate."),
 6: (["c6-b0", "c6-b1", "c6-b2"], ["c6-c0", "c6-c1"],
     "Tee times book through Troon, so the price moves with the day and the season rather than sitting on a rate card."),
 7: (["c7-b0", "c7-b1", "c7-b2"], ["c7-c0", "c7-c1"],
     "The Quarry sits an hour and a quarter south in San Antonio, and the back nine plays inside the old pit. Rates are on its booking page."),
 8: (["c8-b0", "c8-b1", "c8-b2"], ["c8-c0", "c8-c1"],
     "The range closes thirty minutes before sunset, and two hours before sunset on Tuesdays. Rates are on the club's booking page."),
 9: (["c9-b0", "c9-b1", "c9-b2"], ["c9-c0", "c9-c1"],
     "ShadowGlen plays long from the back tees, and wind is a real factor out east. Rates are on its booking page."),
 10: (["c10-b0", "c10-b1", "c10-b2"], ["c10-c0", "c10-c1"],
      "Horseshoe Bay prices golf with a stay, so the rate depends on the package and the season. Four courses on one property."),
 11: (["c11-b0", "c11-b1", "c11-b2"], ["c11-c0", "c11-c1"],
       "Barton Creek has four courses on the property, and staying at the resort usually opens up the tee sheet."),
 12: (["c12-b0", "c12-b1", "c12-b2"], ["c12-c0", "c12-c1"],
       "La Cantera pairs the golf with the Resort &amp; Spa, and the rate depends on the stay and the season."),
 13: (["c13-b0", "c13-b1", "c13-b2"], ["c13-c0", "c13-c1", "/images/special-day/lajitas.jpg"],
       "Lajitas sits seven hours west on the Rio Grande. Plan three nights and book the golf with the room."),
 14: (["c14-0", "c14-1", "c14-2"], ["c14-3", "c14-4"], ""),
}

# ADDED 24 SEP 2026 — Lenny: "add this one into the list- wildspringdunes.com".
# Facts from wildspringdunes.com (read 24 Sep 2026: all 18 open to the public on
# 8 September 2026, walking only, rates below, 2,400+ acres, Mt Enterprise TX)
# and GolfPass's review (Tom Doak design, developer Michael Keiser). Drive time
# from Austin is about four hours, so it goes in the overnights, before Lajitas.
WSD = dict(
    name="Wild Spring Dunes",
    meta="Mt Enterprise &middot; ~4 hrs 15 east &middot; $275 peak",
    desc=("Tom Doak&rsquo;s new course opened all 18 holes to the public on 8 September 2026, deep in the East Texas "
          "pines a little over four hours from Austin. The property runs to more than 2,400 acres of pine and hardwood forest, "
          "meadow and spring-fed ravine, and the round is walking only. Rates read on 24 September 2026 were $275 for 18 "
          "from September to November and $195 in December, January and February, with a $140 same-day replay in peak "
          "season. Tee times are open through the end of 2027, and the developer is Michael Keiser, son of Mike Keiser, "
          "who built Bandon Dunes. There is more in our "
          "<a href=\"/drops/on-our-radar-wild-spring-dunes\">On Our Radar Field Note</a>."),
    url="https://www.wildspringdunes.com/golf")
WSD_FAQ = ("What is Wild Spring Dunes?",
           "A new walking-only course by Tom Doak in Mt Enterprise, in the East Texas pines a little over four hours from Austin. "
           "All 18 holes opened to the public on 8 September 2026. The course's own rates page listed $275 for 18 holes "
           "from September to November 2026 and $195 in the winter months, read on 24 September 2026.")


def src(x):
    return x if x.startswith("/") else f"{V2}/{x}.jpg"


def original():
    h = ORIG.read_text(encoding="utf-8")
    body = h[h.index("<body"):]
    cards = []
    for c in body.split('<div class="product-card"')[1:]:
        g = lambda k: re.search(r'class="' + k + r'"[^>]*>(.*?)</div>', c, re.S).group(1).strip()
        cards.append(dict(name=g("product-brand"), meta=g("product-name"), desc=g("product-desc"),
                          url=re.search(r'href="(http[^"]+)"', c).group(1)))
    intro = re.findall(r"<p>(.*?)</p>", re.search(r'<div class="writeup">\s*<div class="writeup-body">(.*?)</div>', body, re.S).group(1), re.S)

    def section(title):
        i = body.index(f'<h2 class="products-hdr">{title}')
        s = body.rfind("<section", 0, i)
        return body[s:body.index("</section>", i) + len("</section>")]
    cost, pick = section("A Word on What These Cost"), section("Picking the Right One")
    fs = body.rfind("<section", 0, body.index('id="faq"'))
    faq = body[fs:body.index("</section>", fs) + len("</section>")]
    lds = [json.loads(m) for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)]
    title = re.search(r"<title>(.*?)</title>", h).group(1)
    desc = re.search(r'<meta name="description" content="([^"]*)"', h).group(1)
    return cards, intro, cost, pick, faq, lds, title, desc


def band(n, name):
    b = IMGS[n][0]
    figs = "\n".join(
        f'  <figure><img src="{src(x)}" alt="{H.escape(H.unescape(name))}, photograph from the course&rsquo;s own website, view {i+1}" loading="lazy" /></figure>'
        for i, x in enumerate(b))
    return f'  <div class="ig-grid">\n{figs}\n</div>\n'


# Light edits to the 17 Sep copy, only where voice-lint flags it: "this list" /
# "on this page" are sourcing narration, and the Falconhead card opened without
# a verb. Nothing else in the copy is touched.
DESC_FIX = [
    ("The closest thing to a big-day course you can reach without committing the whole morning to driving. Falconhead moved",
     "Falconhead is the closest thing to a big-day course you can reach without committing the whole morning to driving. It moved"),
    ("the one on this list most likely", "the one here most likely"),
    ("the best-value big day on this page if", "the best-value big day here if"),
    ("East out through Manor, and the least scenic drive on this list attached to", "ShadowGlen sits east out through Manor, the least scenic drive here, attached to"),
    ("the only one on this page where", "the only one here where"),
]


def fixed(t):
    for a, b in DESC_FIX:
        t = t.replace(a, b)
    return t


def frames(n):
    out = []
    for x in IMGS[n][0] + IMGS[n][1]:   # lead with a course shot, not a scorecard or a patio
        if src(x) not in out:
            out.append(src(x))
    return out[:5]


def card(n, c, idx):
    fr = frames(n)
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(H.unescape(c["name"]))} &middot; view {i+1} of {len(fr)}" loading="lazy" /></div>' for i, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if i == 0 else ""}" data-i="{i}" aria-label="View image {i+1}"></button>' for i in range(len(fr)))
    return (f'<div class="product-card" id="c-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{c["name"]}</div>'
            f'<div class="product-name">{c["meta"]}</div>'
            f'<div class="product-desc">{fixed(c["desc"])}</div>'
            f'<a href="{c["url"]}" target="_blank" rel="noopener" class="product-link">Course site &#8599;</a></div></div>')


def group(cards, rng, hid, h2, kick, band_imgs):
    figs = "\n".join(f'  <figure><img src="{src(x)}" alt="{H.escape(alt)}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>' for x, alt, cap in band_imgs)
    grid = "\n".join(card(i, cards[i], i + 1) for i in rng)
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <h2 class="products-hdr" id="{hid}">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kick}</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n'
            f'  <div class="products-grid">\n{grid}\n  </div>\n</section>\n')


def main(apply_):
    cards, intro, cost, pick, faq, lds, title, desc = original()
    if len(cards) != 14:
        sys.exit(f"! expected 14 courses in the original, found {len(cards)}")
    cards.append(WSD)                       # index 14
    title = title.replace("4 Overnights", "5 Overnights")
    desc = desc.replace("plus four overnight trips", "plus five overnight trips")
    intro = [p.replace("Four are overnights, because some of this golf is too far or too good to squeeze into a single day, and one of them is seven hours west at the edge of Big Bend.",
                       "Five are overnights, because some of this golf is too far or too good to squeeze into a single day: one is Tom Doak&rsquo;s brand-new course in the East Texas pines, and one is seven hours west at the edge of Big Bend.") for p in intro]
    pick = pick.replace("La Cantera if half the group is not playing, Lajitas",
                        "La Cantera if half the group is not playing, Wild Spring Dunes if you want the newest course in the state, Lajitas")
    faq = faq.replace("  </div>\n</section>", f'    <details open class="faq-q"><summary>{WSD_FAQ[0]}</summary><p>{WSD_FAQ[1]}</p></details>\n  </div>\n</section>', 1)
    for x in lds:
        if x.get("@type") == "Article":
            x["headline"] = x["headline"].replace("4 Overnights", "5 Overnights")
            x["description"] = x.get("description", "").replace("four overnight", "five overnight")
        if x.get("@type") == "FAQPage":
            x["mainEntity"].append({"@type": "Question", "name": WSD_FAQ[0], "acceptedAnswer": {"@type": "Answer", "text": WSD_FAQ[1]}})
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    head_rest = head_rest.replace("</style>",
        "section.products > div > p + p{margin-top:16px}\n</style>", 1)
    tail = d[d.index('<div class="more" data-brandindex="1">'):]

    art = next(x for x in lds if x.get("@type") == "Article")
    art.update({"dateModified": "2026-09-24", "image": f"https://thegrassyissue.com{V2}/og.jpg", "url": URL})
    faqld = next(x for x in lds if x.get("@type") == "FAQPage")
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
        {"@type": "ListItem", "position": 2, "name": "Field Notes", "item": "https://thegrassyissue.com/#feed"},
        {"@type": "ListItem", "position": 3, "name": "Special Day Rounds", "item": URL}]}
    ld = "".join(f'<script type="application/ld+json">\n{json.dumps(b, indent=1, ensure_ascii=False)}\n</script>\n' for b in (art, faqld, crumbs))
    og = f"https://thegrassyissue.com{V2}/og.jpg"
    head = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="icon" href="/favicon.ico" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
<meta property="og:type" content="article" />
<meta property="og:url" content="{URL}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:image" content="{og}" />
<meta property="og:site_name" content="The Grassy Issue" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{desc}" />
<link rel="canonical" href="{URL}" />
<link rel="preload" as="image" href="{V2}/hero.jpg" />
{ld}"""

    paras = "\n".join(f"    <p>{p}</p>" for p in intro)
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Field Notes</a><span>/</span>
  Special Day Rounds</div>

<header class="drop-header">
  <h1>Special Day Rounds Near Austin &mdash; 10 Day Trips and 5 Overnights</h1>
  <div class="drop-meta">
    <span>September 17, 2026 &middot; updated September 24, 2026</span><span class="dot"></span>
    <span>Field Notes</span><span class="dot"></span>
    <span>10 day trips &middot; 5 overnights</span>
  </div>
</header>

<section class="drop-hero">
  <img class="drop-hero-img" src="{V2}/hero.jpg" alt="The Quarry Golf Club in San Antonio at sunset, fairways and the old quarry pit below the city skyline" fetchpriority="high" />
</section>

<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
{paras}
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Which One?</div>
      <div class="sidebar-detail"><span class="l">Half a day</span><span>Grey Rock, Falconhead</span></div>
      <div class="sidebar-detail"><span class="l">Impress a visitor</span><span>The Quarry</span></div>
      <div class="sidebar-detail"><span class="l">Four for a birthday</span><span>Star Ranch, Vaaler Creek</span></div>
      <div class="sidebar-detail"><span class="l">The drive matters</span><span>Vaaler Creek</span></div>
      <div class="sidebar-detail"><span class="l">Stay the night</span><span>Horseshoe Bay</span></div>
      <div class="sidebar-detail"><span class="l">Three days free</span><span>Lajitas</span></div>
      <a href="#picking" class="sidebar-cta">How to choose &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#AustinGolf</span>
        <span class="hashtag">#TexasGolf</span>
        <span class="hashtag">#HillCountry</span>
        <span class="hashtag">#GolfTrip</span>
      </div>
    </div>
  </aside>
</section>

"""
    body += group(cards, range(0, 10), "day-trips", "Day Trips &mdash; 10 Courses",
                  "<strong>Leave after breakfast, home for dinner</strong>Nothing here is further out than about an hour and a quarter.",
                  [("c7-b0", "The Quarry Golf Club from above, fairways running into the old quarry", "The Quarry &middot; San Antonio"),
                   ("c5-b1", "Vaaler Creek Golf Club from above, a fairway beside a long blue lake", "Vaaler Creek &middot; Blanco"),
                   ("c0-b0", "A creek running across the golf course at Lost Pines Resort", "Lost Pines &middot; Bastrop")])
    body += "\n" + cost + "\n"
    body += group(cards, [10, 11, 12, 14, 13], "overnights", "Make It a Weekend &mdash; 5 Overnights",
                  "<strong>Stay the night</strong>This golf is too far, or too good, to compress into one day.",
                  [("c14-0", "Golfers and caddies walking a fairway through the pines at Wild Spring Dunes", "Wild Spring Dunes &middot; new"),
                   ("c10-b0", "A green on the water at Horseshoe Bay Resort", "Horseshoe Bay"),
                   ("c13-b1", "A green reflected in water under desert cliffs at Lajitas", "Lajitas &middot; Black Jack&rsquo;s Crossing")])
    body += "\n" + pick.replace('<h2 class="products-hdr">Picking the Right One', '<h2 class="products-hdr" id="picking">Picking the Right One', 1) + "\n"
    body += "\n" + faq + "\n\n"

    out = head + head_rest + body + tail
    print(f"  15 courses, {sum(len(v[0]) + len(v[1]) for v in IMGS.values())} image slots")
    if not apply_:
        print("  dry run — pass --apply")
        return
    OUT.write_text(out, encoding="utf-8")
    verify(cards)


def verify(cards):
    fin = OUT.read_text(encoding="utf-8")
    bad = []
    if fin.count('class="product-card"') != 15:
        bad.append("card count")
    for c in cards:
        if fixed(c["desc"])[:80] not in fin:  # includes the added course
            bad.append(f"original copy lost for {c['name']}")
    for f in set(re.findall(r'src="(/images/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file():
            bad.append(f"missing {f}")
    if "wolfdancer.jpg" in fin.split('<div class="more"')[0]:
        bad.append("the old low-res hero is still on the page")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", fin), re.I):
        bad.append("banned word")
    if bad:
        OUT.write_text(ORIG.read_text(encoding="utf-8"), encoding="utf-8")
        sys.exit("! restored the original. " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
