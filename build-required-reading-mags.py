#!/usr/bin/env python3
"""build-required-reading-mags.py — Required Reading: six independent golf magazines.
28 September 2026.

Lenny: "let's do another fresh required reading post- let's find some
cool/new/independent golf magazines", then "tighter but a deeper dive on each
option", "depeche golf is also a good", and "skip the ones we dont have pics
for" (drops African American Golfer's Digest, whose covers were blocked).

FACTS: research/magazines/notes.md (two research passes, 28 Sep 2026). Prices,
issues and stock from each title's own store, in the store's own currency.
Quotes verbatim from the titles' own pages, or from press where marked.

PHOTOS: the magazines' own covers, spreads and product photography, localised
to images/required-reading-mags/. Sources in research/magazines/img/log.json.
No feed card; that waits for Lenny.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "required-reading-independent-golf-magazines"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/required-reading-mags"
FR = json.loads((ROOT / "research/magazines/frames.json").read_text())

TITLE = "Required Reading: Six Independent Golf Magazines, Cover to Cover"
DESC = ("Six independent golf magazines in print right now: Hiatus, Depeche Golf, The Loop Journal, Golf Quarterly, "
        "Golf Architecture and Links from the Road. Who makes them, what is inside, and what they cost.")
H1 = "Required Reading: Six Independent Golf Magazines, Cover to Cover"

# card key -> (magazine, issue name, price label, shop url, copy)
P = {
 "hiatus-no2": ("Hiatus", "No. 2", "CAD 18", "https://lezspreadtheword.com/products/hiatus-no2",
   "The cover is a clump of turf floating on white. Inside are features on the golf design house HEAD, Modi Oyewole, John Nichols, Amanda Corr and James Ehrlich. The store says quantities are limited."),
 "hiatus-no1": ("Hiatus", "No. 1", "CAD 18", "https://lezspreadtheword.com/products/hiatus",
   "The first issue has a putting green and a mower on the cover. It launched at the Hiatus Golf Invitational in September 2025, and the publisher still has copies, though magCulture in London has sold out."),
 "depeche-5": ("Depeche Golf", "#5 &middot; HOME", "&euro;25", "https://depeche-golf.com/products/depeche-golf-issue-5",
   "This is the newest issue, out in June. Jack Ducey is the Photographer in Residence, and the contents run from Mark Alexander on home improvements to Henri Karttunen on the flag."),
 "depeche-4": ("Depeche Golf", "#4 &middot; Alternatives", "&euro;25", "https://depeche-golf.com/products/depeche-golf-issue-4",
   "It has 19 stories on 160 pages from 18 collaborators and 16 countries, including Kolf: The Revolutionary Kind, Caledonian Colours and Tour de Berlin: Urbanized Golf."),
 "loop-02": ("The Loop Journal", "Volume 02", "&pound;20", "https://theloopgc.myshopify.com/",
   "A caddie in a red bib takes the cover. Inside: Turnberry, Royal Birkdale, Dumbarnie and golf in the Himalayas, with Lottie Woad, Robert Rock and David Duval."),
 "loop-01": ("The Loop Journal", "Volume 01", "&pound;20", "https://theloopgc.myshopify.com/",
   "A lone golfer on a clifftop above the sea takes the cover. Inside: the Northumberland links, a family trip to Perthshire, and Kevin Murray&rsquo;s 16-page photo portfolio."),
 "gq-58": ("Golf Quarterly", "Issue 58", "&pound;10", "https://www.golfquarterly.co.uk/product-page/issue-58",
   "The cover line reads &ldquo;The golfing hustler who bet on everything.&rdquo; Also inside: the game&rsquo;s slowest and quickest players, and how Trevino dumped a 9-iron in a Northumberland loch. A year of four issues is &pound;35."),
 "sagca-26": ("Golf Architecture", "Issue 26", "AUD 20", "https://sagca.com.au/product/sagca-golf-architecture-magazine-issue-26/",
   "This is the current issue, shown here with Issues 25 and 24. Its cover lines include a focus on construction and a more cohesive Metro. Postage is included."),
 "lftr-2": ("Links from the Road", "Volume 2", "&pound;19.95", "https://linksfromtheroad.com/products/volume-2",
   "It covers twelve links from Royal Lytham &amp; St Annes to Silloth-on-Solway, with Castletown on the Isle of Man and an eclectic eighteen from the stretch."),
 "lftr-1": ("Links from the Road", "Volume 1", "&pound;19.95", "https://linksfromtheroad.com/products/volume-1",
   "It covers Cooper&rsquo;s home coast, from Royal Liverpool and Wallasey to Royal Birkdale, Formby and Southport &amp; Ainsdale, plus an essay on what makes a links."),
}

PROSE = 'style="max-width:760px;font-size:16px;line-height:1.7;margin-bottom:36px;"'

# (key, h2, anchor, card keys, kicker, prose paragraphs)
SECTIONS = [
 ("hiatus", "Hiatus", "hiatus", ["hiatus-no2", "hiatus-no1"],
  "<strong>Montreal &middot; twice a year &middot; English and French</strong>Each issue runs about 120 pages and costs CAD 18 from the publisher.",
  ["Hiatus comes from LSTW Publishing, the Montreal house behind the queer magazine LSTW, which has won National Magazine Awards in Canada. Florence Gagnon is the publisher and Carolyne De Bellefeuille is the art director, and every page runs in English and French.",
   "No. 1 launched in September 2025 at the magazine&rsquo;s own Hiatus Golf Invitational, at Club de Golf Le Champ&ecirc;tre in Quebec. It had Bunker Club, a Los Angeles golf club for women and queer golfers, a guide to golf trips in eastern Quebec, and a critique of courses and clubhouses designed around men. No. 2 is out now.",
   "It is the best-designed new title in golf, and the only one here that treats the clubhouse as something to argue with. In the US it is stocked at Metalwood Studio and Skylight Books in Los Angeles, Chess Club in Portland and Another Corner in Philadelphia."]),
 ("depeche", "Depeche Golf", "depeche-golf", ["depeche-5", "depeche-4"],
  "<strong>Germany &middot; twice a year &middot; English</strong>Issues run up to 160 pages. Issue #5 is &euro;25, and #6 ships in November.",
  ["Depeche Golf is made in Korntal-M&uuml;nchingen, near Stuttgart, by co-publishers Mark Horyna and Emil Weber. It calls itself an international golf and culture magazine, &ldquo;From Europe with Love for the Game.&rdquo; Every issue has a theme, a Photographer in Residence, and long essays set next to art.",
   "Issue #5, HOME, came out in June. It goes to St Andrews, spends a summer on the road in Ireland, visits the Engadine Golf Club in St Moritz, looks for the vanishing greens of Singapore, and meets an artist in New Zealand who built an unplayable course through his home town of Christchurch.",
   "It is the most ambitious title here. We gave it one paragraph in July&rsquo;s Magazine Edit, and it deserved more. Issues #1 to #3 are &euro;19.90 and #4 and #5 are &euro;25. A one-year subscription of two issues is &euro;22.50 plus shipping, starting with #6 in November."]),
 ("loop", "The Loop Journal", "the-loop-journal", ["loop-02", "loop-01"],
  "<strong>Cambridge, UK &middot; twice a year &middot; 100 pages</strong>Each issue is &pound;20, and a golf PR agency publishes it.",
  ["The Loop Journal comes from The Loop, a golf PR and marketing agency in Cambridge. Its founders include Mike Harris, a former editor of Golf Monthly, and Alex Narey, who worked at the magazine from 2008. The writing is professional and the travel pieces run long: Narey told Golf Business News there was no set word count.",
   "Volume 01 arrived in February with the Northumberland links and a 16-page portfolio by the photographer Kevin Murray, from Lofoten Links to Pinehurst No. 2 and Royal Portrush. Volume 02 followed in July.",
   "There is one thing to know. An agency that works with golf brands also reviews equipment in these pages. The travel writing is the reason to buy it."]),
 ("gq", "Golf Quarterly", "golf-quarterly", ["gq-58"],
  "<strong>UK &middot; four times a year &middot; 44 pages, A5</strong>An issue is &pound;10 and a year of four is &pound;35, with no advertising.",
  ["Golf Quarterly is the smallest magazine here and probably the funniest. It is pocket-sized, 44 pages with no advertising, and it has run since 2010. The editor is Tim Dickson, who spent 21 years at the Financial Times, and the publisher is Jon Connell, who founded The Week.",
   "It is built on wit and history. Recent issues cover Moe Norman, golf in the Falklands, the year of Bob Hope and the last stymie, and eight decades of a mothers-and-daughters tournament.",
   "There is one caveat. The homepage still shows Autumn 2023, but the shop lists every issue up to No. 58 and still sells subscriptions. We could not confirm a 2026 issue."]),
 ("sagca", "Golf Architecture", "golf-architecture", ["sagca-26"],
  "<strong>Australia &middot; annual since 1997</strong>Each issue is AUD 20, and the price includes postage.",
  ["Golf Architecture is the annual of the Society of Australian Golf Course Architects, and it has been published since 1997. The people who design and restore courses write it, for readers who want to know why a bunker sits where it does.",
   "It is not a lifestyle magazine, and that is the appeal. Past issues interviewed Mike Keiser Jr. and toured Ardfin on the Isle of Jura. Every back issue is AUD 20 with postage, and all but one are in stock."]),
 ("lftr", "Links from the Road", "links-from-the-road", ["lftr-2", "lftr-1"],
  "<strong>Wirral, UK &middot; 18 volumes planned</strong>Each volume is &pound;19.95. Two are out so far.",
  ["Sam Cooper is a golf architect with Clayton, DeVries &amp; Pont and a member at Royal Liverpool. Between 2020 and 2022 he and his wife Harriet played all 225 links courses in Great Britain from a camper van. Links from the Road is that trip, published round the coast in 18 volumes, with illustrations by Will Eagar.",
   "Each chapter mixes architecture, history and his own photography, and each course has a companion podcast episode.",
   "The catch is the wait. Volume 2 came out in April 2025 and there is no sign of Volume 3 yet. Both volumes are still in stock."]),
]

PQ = {
    "gagnon": ("Creating a magazine today is an act of intention &hellip; It&rsquo;s about slowing down, choosing stories that matter, and giving them the space and design they deserve.",
               "Florence Gagnon, publisher of Hiatus, on hiatusgolf.com"),
    "narey": ("In what is now a digital-first media landscape, we do still believe print can still flourish&hellip;",
              "Alex Narey of The Loop, to Golf Business News, February 2026"),
    "cooper": ("I firmly believe the ball along the ground is twice as interesting as the ball through the air.",
               "Sam Cooper, author of Links from the Road"),
}

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Our Magazine Edit in July went 24 titles wide. This one goes six deep. These are the independent golf magazines we would put on the table this fall: who makes them, what is in the latest issue, and what it costs from the maker&rsquo;s own shop.</p>
    <p>The common thread is slowness. Every one is printed, most come out twice a year or less, and only one reviews equipment. Hiatus is the most exciting new title in golf print. Depeche Golf is the most ambitious. Golf Quarterly is the funniest, and the smallest.</p>
    <p>Start with Hiatus No. 2 at CAD 18. For the deep end, Depeche Golf #5 at &euro;25. Prices were read from each magazine&rsquo;s own store on 28 September 2026, in the store&rsquo;s own currency.</p>
    <h2 class="products-hdr btk-story-hdr">How We Chose</h2>
    <p>We left out the titles from <a href="/drops/the-magazine-edit">The Magazine Edit</a>, except Depeche Golf. We only included magazines we could buy from the maker today, with pictures of what you get, and we flag the two that have gone quiet. Club magazines and digital-only titles are out. One society journal made it in, because nobody else writes about course design like the architects themselves.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Titles</span><span>Six</span></div>
      <div class="sidebar-detail"><span class="l">From</span><span>Canada, Germany, UK, Australia</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>&pound;10 to &euro;25 an issue</span></div>
      <div class="sidebar-detail"><span class="l">Newest</span><span>Hiatus No. 2</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Hiatus No. 2, CAD 18</span></div>
      <div class="sidebar-detail"><span class="l">Prices read</span><span>28 September 2026</span></div>
      <a href="#hiatus" class="sidebar-cta">Start with Hiatus &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#RequiredReading</span>
        <span class="hashtag">#GolfMagazines</span>
        <span class="hashtag">#IndependentPrint</span>
        <span class="hashtag">#GolfCulture</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

FAQ = [
    ("What are the best independent golf magazines right now?",
     "Our six are Hiatus (Montreal), Depeche Golf (Germany), The Loop Journal (UK), Golf Quarterly (UK), Golf Architecture (Australia) and Links from the Road (UK). For 24 more, see our Magazine Edit."),
    ("Which golf magazines are new in 2026?",
     "The Loop Journal published Volume 01 in February 2026 and Volume 02 in July. Hiatus published its second issue in 2026, and Depeche Golf released issue #5 in June, with #6 due in November."),
    ("Where can I buy Hiatus golf magazine in the US?",
     "Hiatus lists Metalwood Studio and Skylight Books in Los Angeles, Chess Club in Portland and Another Corner in Philadelphia. The publisher sells both issues online for CAD 18 each."),
    ("Is there a magazine about golf course architecture?",
     "Golf Architecture, the annual of the Society of Australian Golf Course Architects, has been published since 1997 and costs AUD 20 with postage. Links from the Road, by the golf architect Sam Cooper, covers every links course in Great Britain."),
    ("How much is a golf magazine subscription?",
     "Golf Quarterly is £35 a year for four issues. Depeche Golf is €22.50 a year for two issues, plus shipping. Hiatus, The Loop Journal and Links from the Road sell single issues."),
]


def pq(key):
    txt, attr = PQ[key]
    return (f'\n<!-- TGI-RR-PQ-{key} -->\n<div class="pull-quote">\n  <div class="pull-quote-inner">'
            f'&ldquo;{txt}&rdquo;<span class="pull-quote-attr">&mdash; {attr}</span></div>\n</div>\n'
            f'<!-- /TGI-RR-PQ-{key} -->\n')


def card(h, idx):
    mag, issue, price, shop, copy = P[h]
    fr = [f["local"] for f in FR[h]]
    label = H.unescape(f"{mag} {issue}").replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>'
                   for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>'
                   for j in range(len(fr)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{mag}</div>'
            f'<div class="product-name">{issue} &middot; {price}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="{shop}" target="_blank" rel="noopener" class="product-link">Buy from {mag} &#8599;</a></div></div>')


def section(sec, n0):
    key, h2, anchor, ids, kicker, paras = sec
    cards = "\n".join(card(h, n0 + j) for j, h in enumerate(ids))
    prose = "\n".join(f'    <p style="margin:0 0 16px;">{p}</p>' for p in paras)
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{"One issue" if len(ids) == 1 else f"{len(ids)} issues"}</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'  <div {PROSE}>\n{prose}\n  </div>\n'
            f'    <div class="products-grid">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>'
                     for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')

def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items, pos = [], 1
    for sec in SECTIONS:
        for h in sec[3]:
            items.append({"@type": "ListItem", "position": pos, "url": P[h][3], "name": H.unescape(f"{P[h][0]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-09-28", "dateModified": "2026-09-28",
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
            {"@type": "ListItem", "position": 3, "name": "Required Reading: Golf Magazines", "item": URL}]},
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
    assert len(ids) == 10 == len(set(ids)) and set(ids) == set(P)
    for h in ids:
        assert FR.get(h), h
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Required Reading</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Required Reading</span><span class="dot"></span>
    <span>6 magazines &middot; 4 countries</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Hands holding open Depeche Golf issue five on a stone wall, a spread of golf photographs by Jack Ducey" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    s, n = section(SECTIONS[0], n); body += s + pq("gagnon")
    s, n = section(SECTIONS[1], n); body += s
    s, n = section(SECTIONS[2], n); body += s + pq("narey")
    s, n = section(SECTIONS[3], n); body += s
    s, n = section(SECTIONS[4], n); body += s
    s, n = section(SECTIONS[5], n); body += s + pq("cooper")
    body += faq_html()
    out = head_top() + head_rest + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply")
        return
    OUT.write_text(out, encoding="utf-8")
    verify()


def verify():
    fin = OUT.read_text(encoding="utf-8")
    bad = []
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    for leak in ("Burnt Orange", "Manors Revisited", "Nicklaus", "St. Andr"):
        if leak in above:
            bad.append(f"should not appear: {leak}")
    if fin.count('class="product-card"') != 10:
        bad.append("card count")
    for k, (t, _) in PQ.items():
        if fin.count(t[:50]) != 1:
            bad.append(f"pq {k}")
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
