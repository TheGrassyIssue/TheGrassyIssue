#!/usr/bin/env python3
"""build-best-independent.py — /brands/best-independent-golf-brands
24 September 2026.

Lenny: "let's add this category to the index '25 Best Independent Golf Brands
2026'. These will be the 25 brands with the most posts about them." Then:
"build it please".

THE RANKING IS COMPUTED, NEVER TYPED. Rank = number of TGI pages that mention
the brand (data/brand-mentions.json, the same file the brand pages' coverage
lists come from). Ties are listed alphabetically and share the same count.
The page re-ranks every time build-brands.py runs (it is in the CHAIN, after
build-brand-taxonomy.py), so a brand that picks up coverage moves up by itself.

ONLY VERIFIED INDEPENDENTS RANK. data/independence.json holds the ownership
verdicts (researched 24 Sep 2026; notes in research/best-independent/). A brand
ranks only if its status is "independent", which requires a NAMED owner. Brands
marked "not" or "unclear", and brands never checked, are skipped. The build
prints any unchecked brand whose post count would put it in the top 25 so it
gets checked, rather than silently leaving it out forever.

That rule (stated softly on the page since 25 Sep 2026 — Lenny: \"tone down the how this list works rule, they make good stuff, its consistent and theres a solid point of view\") took out several of the most-covered brands in the Index (Malbon,
Manors, Sugarloaf, Quiet Golf, STITCH, Eastside) because each has outside
investors or a corporate owner. The page does NOT list them or explain the cut
(standing rule: no "what we cut" sections, never talk down on brands). It
states the rule once, plainly.

COPY RULES: no 'worth'; counts and names computed; one h1.
Dry run by default; --apply writes the page.
"""
import datetime
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
# "editor-pick": Lenny's call to include a founder-run brand that has taken a
# minority outside investment (Manors, 25 Sep 2026). The method copy names it.
RANKS = ("independent", "editor-pick")
N_TOP = 25
YEAR = 2026
SLUG = "best-independent-golf-brands"
URL = f"/brands/{SLUG}"
OUT = os.path.join(ROOT, "brands", SLUG + ".html")

brands = {b["slug"]: b for b in json.load(open(os.path.join(ROOT, "data", "brands.json"), encoding="utf-8"))}
ment = json.load(open(os.path.join(ROOT, "data", "brand-mentions.json"), encoding="utf-8"))
ind = {k: v for k, v in json.load(open(os.path.join(ROOT, "data", "independence.json"), encoding="utf-8")).items()
       if not k.startswith("_")}
index_html = open(os.path.join(ROOT, "brands", "index.html"), encoding="utf-8").read()
chrome_src = open(os.path.join(ROOT, "brands", "gramicci.html"), encoding="utf-8").read()


def esc(s):
    return html.escape(s, quote=True)


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(s))).strip()


# ------------------------------------------------------------------ the ranking
def posts(slug):
    return len(ment.get(slug, []))


# EDITORIAL ORDER (Lenny, 6 Oct 2026): the list is now our picks, informed by coverage, in the order in
# data/best25-order.json. Every brand on it must still carry a status in RANKS and an owner line.
ORDER = json.load(open(os.path.join(ROOT, "data", "best25-order.json"), encoding="utf-8"))["order"]
for s_ in ORDER:
    if s_ not in brands or not ind.get(s_) or ind[s_].get("status") not in RANKS:
        raise SystemExit(f"{s_}: in best25-order.json but not a brand with a RANKS status in independence.json")
top = [brands[s_] for s_ in ORDER][:N_TOP]
if len(top) != N_TOP:
    raise SystemExit(f"best25-order.json has {len(top)} brands, need {N_TOP}")
floor = min(posts(b["slug"]) for b in top)
unchecked = []
SIG = json.load(open(os.path.join(ROOT, "data", "best25-signature.json"), encoding="utf-8"))

# every brand on the list needs an owner line and a source
for b in top:
    v = ind[b["slug"]]
    if not v.get("owner") or not v.get("src"):
        raise SystemExit(f"{b['slug']}: independent but no owner line/source in independence.json")

# ---------------------------------------------------------------- cards' images
# Same image rule as build-brand-index.py: brands.json "img" first, else the
# card image. brands/index.html is in its bare bi-card form when build-brands.py
# calls this and in its bc form afterwards, so both are read.
IMG = {}
for m in re.finditer(r'<div class="bi-card"[^>]*>(.*?)<a class="bi-covlink"', index_html, re.S):
    s, im = re.search(r'href="/brands/([^"]+)"', m.group(1)), re.search(r'<img src="([^"]+)"', m.group(1))
    if s and im:
        IMG.setdefault(s.group(1), im.group(1))
for m in re.finditer(r'<a class="bc" href="/brands/([a-z0-9-]+)"[^>]*>.*?<img src="([^"]+)"', index_html, re.S):
    IMG.setdefault(m.group(1), m.group(2))
for s, b in brands.items():
    if b.get("img"):
        IMG[s] = b["img"]
# LIFESTYLE PHOTOGRAPHY FIRST (Lenny, 24 Sep 2026: "lean more on lifestyle
# images"). independence.json carries a per-brand "img": a 4:3 crop in
# images/best-independent/ of a people-and-place photo, chosen by eye. It beats
# the Index card image, which for most brands is a packshot.
for s, v in ind.items():
    if isinstance(v, dict) and v.get("img"):
        IMG[s] = v["img"]
for b in top:
    if b["slug"] not in IMG:
        raise SystemExit(f"{b['slug']}: no card image in brands/index.html — run build-brand-index.py first")
    if not os.path.exists(ROOT + IMG[b["slug"]]):
        raise SystemExit(f"{b['slug']}: image {IMG[b['slug']]} missing on disk")
    if not os.path.exists(os.path.join(ROOT, "brands", b["slug"] + ".html")):
        raise SystemExit(f"{b['slug']}: no brand page")

# ------------------------------------------------------------------ the chrome
HEAD_END = chrome_src.find("</head>")
BODY_START = chrome_src.find("<body>")
NAV_END = chrome_src.find('<header class="bp-head">')
FOOT_START = chrome_src.find("<footer")
if min(HEAD_END, BODY_START, NAV_END, FOOT_START) < 0:
    raise SystemExit("could not find the chrome landmarks in brands/gramicci.html")
HEAD = chrome_src[:HEAD_END]
NAV = chrome_src[BODY_START + len("<body>"):NAV_END]
TAIL = chrome_src[FOOT_START:]
# The #bx stylesheet lives in build-brand-index.py's CSS constant, not only in the
# built page (which is bare when build-brands.py calls this), so lift it from the
# script source.
_src = open(os.path.join(ROOT, "build-brand-index.py"), encoding="utf-8").read()
_bx = re.search(r'<style id="bx-css">.*?</style>', _src, re.S)
if not _bx:
    raise SystemExit("could not lift #bx-css out of build-brand-index.py")
BXCSS = _bx.group(0).replace('id="bx-css"', 'id="bi-css"').replace("#bx{", "#bi{").replace("#bx ", "#bi ")

CSS = """<style>
#bi{max-width:1100px;margin:0 auto;padding:44px 22px 70px}
#bi .bi-crumb{font-family:var(--bx-mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--bx-ink60);margin-bottom:18px}
#bi .bi-crumb a{color:inherit;text-decoration:none;border-bottom:1px solid currentColor}
#bi .bi-eyebrow{font-family:var(--bx-mono);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--bx-ink60);margin-bottom:12px}
#bi h1{font-size:clamp(32px,4.8vw,58px);line-height:1.04;letter-spacing:-.02em;margin:0 0 18px;font-weight:700}
#bi .bi-intro{max-width:64ch;font-size:17.5px;line-height:1.62}
#bi .bi-intro p{margin:0 0 15px}
#bi .bi-how{max-width:64ch;margin:30px 0 0;padding:22px 0 6px;border-top:1px solid var(--bx-ink);border-bottom:1px solid var(--bx-rule)}
#bi .bi-how h2,#bi .bi-faq h2{font-family:var(--bx-serif,Georgia,serif);font-size:24px;letter-spacing:-.01em;margin:0 0 12px}
#bi .bi-how p{font-size:16.5px;line-height:1.62;margin:0 0 14px}
#bi .bi-list{list-style:none;margin:46px 0 0;padding:0}
#bi .rk{display:grid;grid-template-columns:86px 260px 1fr;gap:26px;align-items:start;padding:28px 0;border-top:1px solid var(--bx-rule)}
#bi .rk:first-child{border-top:1px solid var(--bx-ink)}
#bi .rk-n{font-family:var(--bx-serif,Georgia,serif);font-size:58px;line-height:.9;letter-spacing:-.03em}
#bi .rk-img{display:block;aspect-ratio:4/3;overflow:hidden;background:var(--bx-paper2,#ECE8DF)}
#bi .rk-img img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .4s}
#bi .rk-img:hover img{transform:scale(1.03)}
#bi .rk h2{font-family:var(--bx-serif,Georgia,serif);font-size:28px;letter-spacing:-.015em;margin:0 0 6px;line-height:1.1}
#bi .rk h2 a{color:inherit;text-decoration:none}
#bi .rk-meta{font-family:var(--bx-mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--bx-ink60);margin-bottom:12px}
#bi .rk-meta b{color:var(--bx-ink);font-weight:600}
#bi .rk p{font-size:16px;line-height:1.58;margin:0 0 9px;max-width:56ch}
#bi .rk-own{color:var(--bx-ink60)}
#bi .rk-go{display:inline-block;margin-top:6px;font-family:var(--bx-mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:inherit;text-decoration:none;border-bottom:1px solid currentColor;padding-bottom:2px}
#bi .bi-faq{max-width:64ch;margin:54px 0 0}
#bi .bi-faq details{border-top:1px solid var(--bx-rule);padding:14px 0}
#bi .bi-faq summary{cursor:pointer;font-weight:600;font-size:16.5px;list-style:none}
#bi .bi-faq summary::-webkit-details-marker{display:none}
#bi .bi-faq summary::after{content:"+";float:right;opacity:.5}
#bi .bi-faq details[open] summary::after{content:"\\2212"}
#bi .bi-faq p{font-size:16.5px;line-height:1.62;margin:10px 0 0}
#bi .bi-glance{max-width:64ch;margin:30px 0 0}
#bi .bi-glance h2{font-family:var(--bx-serif,Georgia,serif);font-size:24px;letter-spacing:-.01em;margin:0 0 12px}
#bi .bi-tw{overflow-x:auto}
#bi .bi-table{width:100%;border-collapse:collapse;font-size:15px;line-height:1.4}
#bi .bi-table th{text-align:left;font-family:var(--bx-mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;font-weight:600;padding:8px 10px 8px 0;border-bottom:1px solid var(--bx-ink)}
#bi .bi-table td{padding:7px 10px 7px 0;border-bottom:1px solid var(--bx-rule);vertical-align:top}
#bi .bi-table td:first-child{font-family:var(--bx-mono);font-size:12px;opacity:.6}
#bi .bi-table a{color:inherit;text-decoration:none;border-bottom:1px solid rgba(20,20,20,.3)}
#bi .bi-intro a{color:inherit;border-bottom:1px solid currentColor;text-decoration:none}
#bi .bi-back{margin-top:40px;font-family:var(--bx-mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase}
#bi .bi-back a{color:inherit}
@media(max-width:760px){#bi .rk{grid-template-columns:52px 1fr;gap:16px}#bi .rk-n{font-size:40px}
 #bi .rk-img{grid-column:2;position:static;aspect-ratio:4/3}#bi .rk-body{grid-column:2}}
/*TGI-B25-DENSE*/
@media(min-width:880px){#bi .bi-top{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:56px;align-items:start}
 #bi .bi-top .bi-intro,#bi .bi-top .bi-how{max-width:none}
 #bi .bi-top .bi-how{margin:4px 0 0;padding:20px 24px 8px;border:1px solid var(--bx-rule);border-top:2px solid var(--bx-ink);background:rgba(255,255,255,.35)}}
@media(min-width:761px){#bi .rk{grid-template-columns:72px minmax(220px,320px) 1fr;gap:28px}
#bi .rk-img{aspect-ratio:4/5}}
#bi .rk p{max-width:none}
#bi .sig{max-width:none}
#bi .bi-list{margin-top:36px}
#bi{--ink:var(--bx-ink,#141414);--paper:var(--bx-paper,#F4F1EA);--mono:var(--bx-mono,ui-monospace,monospace)}
#bi .bi-by{font-family:var(--bx-mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--bx-ink60);margin:-6px 0 22px}
#bi .bi-by a{color:inherit;border-bottom:1px solid currentColor;text-decoration:none}
#bi .rk-best{font-size:14.5px!important;margin:0 0 10px!important}#bi .rk-best b{font-family:var(--bx-mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;font-weight:600}
#bi .bi-cat{max-width:64ch;margin:50px 0 0;border-top:1px solid var(--bx-ink);padding-top:22px}#bi .bi-cat h2{font-family:var(--bx-serif,Georgia,serif);font-size:24px;margin:0 0 6px}#bi .bi-cat h3{font-size:16px;margin:18px 0 4px}#bi .bi-cat p{font-size:16px;line-height:1.6;margin:0}#bi .bi-cat a,#bi .bi-glance a{color:inherit;border-bottom:1px solid rgba(20,20,20,.3);text-decoration:none}
#bi .sig-h{font-family:var(--bx-mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;margin:18px 0 10px;color:var(--bx-ink60)}
#bi .sig{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;max-width:640px}
#bi .sig-card{border:1px solid var(--bx-rule,#e6e4df);background:#fff;position:relative}
#bi .product-gallery{position:relative;aspect-ratio:4/5;overflow:hidden;background:#ece8df}
#bi .pg-track{display:flex;height:100%;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;scroll-behavior:smooth}
#bi .pg-track::-webkit-scrollbar{display:none}
#bi .pg-frame{flex:0 0 100%;height:100%;scroll-snap-align:center}
#bi .pg-frame img{width:100%;height:100%;object-fit:cover;display:block}
#bi .pg-arw{position:absolute;top:50%;transform:translateY(-50%);width:24px;height:24px;border:.5px solid var(--ink);background:var(--paper);color:var(--ink);font-size:14px;line-height:1;cursor:pointer;opacity:0;transition:opacity .18s;z-index:2;padding:0}
#bi .pg-arw.prev{left:5px}#bi .pg-arw.next{right:5px}
#bi .sig-card:hover .pg-arw{opacity:.9}
#bi .pg-count{position:absolute;top:6px;right:6px;font-family:var(--mono);font-size:8.5px;letter-spacing:.1em;background:var(--paper);border:.5px solid var(--ink);padding:1px 5px;z-index:2}
#bi .pg-dots{position:absolute;bottom:6px;left:0;right:0;display:flex;justify-content:center;gap:4px;z-index:2}
#bi .pg-dot{width:5px;height:5px;border-radius:50%;border:.5px solid var(--ink);background:var(--paper);padding:0;cursor:pointer;opacity:.55}
#bi .pg-dot.on{background:var(--ink);opacity:1}
#bi .sig-b{padding:8px 9px 10px}
#bi .sig-t{font-family:var(--bx-serif,Georgia,serif);font-size:13.5px;line-height:1.3;margin:0}
#bi .sig-p{font-family:var(--bx-mono);font-size:10px;letter-spacing:.06em;margin:5px 0 6px;color:var(--bx-ink60)}
#bi .sig-b a{font-family:var(--bx-mono);font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:inherit;text-decoration:none;border-bottom:1px solid currentColor}
@media(max-width:900px){#bi .pg-arw{opacity:.85}}
@media(max-width:760px){#bi .sig{grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}#bi .sig-t{font-size:12px}}
@media(max-width:480px){#bi .sig{grid-template-columns:repeat(2,minmax(0,1fr))}}
</style>"""

# ---------------------------------------------------------------------- copy
today = datetime.date.today()
asof = f"{today:%B} {today.day}, {today.year}"
n1, n2, n3 = top[0], top[1], top[2]
p1 = posts(n1["slug"])
W = {25: "twenty-five"}
num = lambda n: "one post" if n == 1 else f"{n} posts"

BESTFOR = json.load(open(os.path.join(ROOT, "data", "best25-bestfor.json"), encoding="utf-8"))
top10 = ", ".join(esc(plain(b["name"])) for b in top[:9]) + " and " + esc(plain(top[9]["name"]))
INTRO = f"""<p>The best independent golf brands right now are {top10}, with fifteen more below. Independent golf is
where the most interesting ideas in the game are coming from: small labels, mostly run by the people who started them,
making golf clothes, bags and headcovers that a big brand would never sign off on.</p>
<p>We picked these {W[N_TOP]} on taste, on our own experience with the brands, and on who is doing the most
interesting work right now. We have spent the year covering them out of Austin, in Brand to Know profiles, drops,
gift guides and the gear we take to the city&rsquo;s munis. Each brand comes with the three signature pieces we would
buy first, and a link to its page in the Brand Index, where every post we have written about it lives.</p>
<p>Looking for more than twenty-five? See every <a href="/brands/tag/independent">independent golf brand</a> in the
Index, or browse <a href="/brands">the full golf brand directory</a>.</p>"""

HOW = f"""<h2>How we picked</h2>
<p>This is an editor&rsquo;s list, not a formula. Every brand on it makes good things, makes them consistently and has
a clear point of view, and every one is doing something we think is to watch closely in {YEAR}. Almost all
are still run by the people who started them, or by a family, rather than by a parent company. Two are
editor&rsquo;s picks on ownership: Manors, which has taken a minority outside investment, and Odd Ritual, which has
not named its owners publicly.</p>
<p>The three signature pieces for each brand were chosen from its own store, and prices and stock were read there on
{asof}. Prices outside the US are shown in the store&rsquo;s currency with an approximate dollar figure.</p>"""

# Questions section removed (Lenny, 24 Sep 2026: "remove the questions at the bottom").
# Kept here unused in case it comes back; the FAQPage schema went with it.
FAQ = [
    ("What counts as an independent golf brand?",
     "A brand owned by its founders or a family, with no parent company, no public listing and no venture-capital, "
     "private-equity or strategic investor. Crowdfunding, small friends-and-family investment and loans do not "
     "disqualify a brand."),
    ("How are the brands ranked?",
     f"By the number of pages on The Grassy Issue that mention each brand. {esc(plain(n1['name']))} has the most, "
     f"with {num(p1)}. Brands with the same count are listed alphabetically."),
    ("How often does the list change?",
     "Every time the Brand Index is rebuilt. When we publish a new post about a brand, its count goes up and it can "
     "move up the list. Ownership is re-checked when a brand is new to the top 25."),
    ("Where can I read the posts behind each number?",
     "Each brand's page in the Brand Index lists every TGI post that mentions it. Click any brand on this list to "
     "see them."),
]

WRITE = json.load(open(os.path.join(ROOT, "data", "best25-writeups.json"), encoding="utf-8"))
missing_w = [b["slug"] for b in top if b["slug"] not in WRITE]
PROFILE = re.compile(r"/drops/(brand-to-know|brand-revisited|brand-to-watch|fella-golf)")
def sig_html(s_, name):
    items = SIG.get(s_, [])
    if not items:
        return ""
    cards = []
    for p in items:
        fr = p["frames"]
        imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{esc(name)} {esc(p["title"])}, view {j+1} of {len(fr)}" loading="lazy" width="500" height="625"></div>' for j, f in enumerate(fr))
        dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>' for j in range(len(fr)))
        ctl = (f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button><button class="pg-arw next" aria-label="Next image">&#8250;</button>'
               f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div>') if len(fr) > 1 else ""
        note = " &middot; made to order" if p.get("made_to_order") else ""
        cards.append(f'<div class="sig-card product-card" data-frames="{len(fr)}"><div class="product-gallery"><div class="pg-track">{imgs}</div>{ctl}</div>'
                     f'<div class="sig-b"><p class="sig-t">{esc(p["title"])}</p><div class="sig-p">{p["price"]}{note}</div>'
                     f'<a href="{esc(p["url"])}" target="_blank" rel="noopener">Shop &#8599;</a></div></div>')
    return f'<div class="sig-h">Three signature pieces</div><div class="sig">{"".join(cards)}</div>'


rows = []
for i, b in enumerate(top, 1):
    s = b["slug"]
    name = plain(b["name"])
    meta = " &middot; ".join(x for x in (esc(b.get("loc", "").strip("— -")),
                                         esc(", ".join(b.get("cats", [])))) if x)
    rows.append(
        f'<li class="rk" id="no-{i}"><div class="rk-n">{i:02d}</div>'
        f'<a class="rk-img" href="/brands/{s}"><img src="{IMG[s]}" alt="{esc(name)}" loading="{"eager" if i < 3 else "lazy"}"'
        f' width="520" height="390"></a>'
        f'<div class="rk-body"><h2><a href="/brands/{s}">{esc(name)}</a></h2>'
        f'<div class="rk-meta">{meta}</div><p class="rk-best"><b>Best for:</b> {BESTFOR.get(s, "")}</p>'
        f'<p>{esc(WRITE.get(s, b.get("line", "")))}</p>'
        f'<p class="rk-own">{esc(ind[s]["owner"])}</p>'
        + (f'<a class="rk-go" href="{b["url"]}">{"Read our Brand to Know" if PROFILE.search(b.get("url", "")) else "Read our coverage"} &rarr;</a> &nbsp; '
           if b.get("url", "").startswith("/drops/") else "")
        + f'<a class="rk-go" href="/brands/{s}">See the brand and all {num(posts(s))} &rarr;</a>'
        + sig_html(s, name) + '</div></li>')

def frm(s_):
    it = SIG.get(s_, [])
    return it[0]["price"] if it else "&mdash;"
GLANCE_OLD = "\n".join(
    f'<tr><td>{i:02d}</td><td><a href="#no-{i}">{esc(plain(b["name"]))}</a></td>'
    f'<td>{esc((b.get("loc") or "").strip("— -")) or "&mdash;"}</td>'
    f'<td>{esc(", ".join(c.title() for c in b.get("cats", [])))}</td></tr>' for i, b in enumerate(top, 1))
DASHES = "\u2014 -"
GLANCE = "\n".join(
    f'<tr><td>{i:02d}</td><td><a href="#no-{i}">{esc(plain(b["name"]))}</a></td>'
    f'<td>{esc((b.get("loc") or "").strip(DASHES)) or "&mdash;"}</td><td>{BESTFOR.get(b["slug"], "")}</td></tr>' for i, b in enumerate(top, 1))
CATS = [("apparel", "Best independent golf apparel brands"), ("bags", "Best independent golf bag brands"),
        ("headcovers", "Best independent headcover makers"), ("accessories", "Best independent golf accessories brands")]
RANK = {b["slug"]: i for i, b in enumerate(top, 1)}
bycat = []
for c, h in CATS:
    names = [f'<a href="#no-{RANK[b["slug"]]}">{esc(plain(b["name"]))}</a>' for b in top if c in b.get("cats", [])]
    if names:
        bycat.append(f'<h3>{h}</h3><p>{", ".join(names)}.</p>')
BYCAT = "".join(bycat)
H1 = f"Our {N_TOP} Best Independent Golf Brands"  # Lenny, 24 Sep 2026
TITLE = f"Our {N_TOP} Best Independent Golf Brands ({YEAR}) | The Grassy Issue"
DESC = (f"Our {N_TOP} best independent golf brands for {YEAR}, picked in Austin: founder-run labels making clothes, bags "
        f"and headcovers, with three signature pieces from each.")

schema = {"@context": "https://schema.org", "@graph": [
    {"@type": "CollectionPage", "name": H1, "description": DESC, "url": f"https://thegrassyissue.com{URL}",
     "dateModified": today.isoformat(), "datePublished": "2026-09-24",
     "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
     "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
     "isPartOf": {"@type": "WebSite", "name": "The Grassy Issue", "url": "https://thegrassyissue.com"},
     "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
         {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
         {"@type": "ListItem", "position": 2, "name": "The Brand Index", "item": "https://thegrassyissue.com/brands"},
         {"@type": "ListItem", "position": 3, "name": H1}]},
     "mainEntity": {"@type": "ItemList", "itemListOrder": "https://schema.org/ItemListOrderDescending",
                    "numberOfItems": N_TOP, "itemListElement": [
                        {"@type": "ListItem", "position": i, "item": {"@type": "Organization", "name": plain(b["name"]),
                         "url": f"https://thegrassyissue.com/brands/{b['slug']}",
                         "description": plain(BESTFOR.get(b["slug"], ""))}} for i, b in enumerate(top, 1)]}}]}

head = HEAD
head = re.sub(r"<title>[^<]*</title>", f"<title>{esc(TITLE)}</title>", head)
short = TITLE.split(" | ")[0]
for k, v in [("description", DESC), ("og:title", short), ("og:description", DESC)]:
    head = re.sub(rf'(<meta (?:name|property)="{re.escape(k)}" content=")[^"]*(")',
                  lambda m, v=v: m.group(1) + esc(v) + m.group(2), head)
head = re.sub(r'<meta name="twitter:[^"]*" content="[^"]*">\s*', "", head)
head = re.sub(r'<meta property="og:image" content="[^"]*">\s*', "", head)
for pat in (r'(<link rel="canonical" href=")[^"]*(")', r'(<meta property="og:url" content=")[^"]*(")'):
    head = re.sub(pat, lambda m: m.group(1) + f"https://thegrassyissue.com{URL}" + m.group(2), head)
head = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', "", head, flags=re.S)
img0 = "https://thegrassyissue.com" + IMG[n1["slug"]]
head += ("\n" + f'<script type="application/ld+json">{json.dumps(schema)}</script>'
         + f'\n<meta property="og:image" content="{img0}">'
         + '\n<meta name="twitter:card" content="summary_large_image">'
         + f'\n<meta name="twitter:title" content="{esc(short)}">'
         + f'\n<meta name="twitter:description" content="{esc(DESC)}">'
         + f'\n<meta name="twitter:image" content="{img0}">'
         + "\n" + BXCSS + "\n" + CSS)

faq_html = "".join(f"<details><summary>{esc(q)}</summary><p>{a}</p></details>" for q, a in FAQ)
body = f"""<main id="bi">
  <div class="bi-crumb"><a href="/">Feed</a> &nbsp;/&nbsp; <a href="/brands">The Brand Index</a> &nbsp;/&nbsp; Best Independent Golf Brands</div>
  <div class="bi-eyebrow">The Brand Index &middot; {YEAR} list &middot; Updated {asof}</div>
  <h1>{esc(H1)}</h1>
  <div class="bi-by">By <a href="/about">Lenny Harrington</a>, editor &middot; Austin, Texas</div>
  <div class="bi-top">
  <div class="bi-intro">
{INTRO}
  </div>
  <section class="bi-how">
{HOW}
  </section>
  </div>
  <ol class="bi-list">
{chr(10).join(rows)}
  </ol>
  <section class="bi-cat">
<h2>The best independent golf brands by category</h2>
{BYCAT}
  </section>
  <div class="bi-back"><a href="/brands/tag/independent">All independent brands in the Index &rarr;</a> &nbsp;&middot;&nbsp; <a href="/brands">&larr; The full Brand Index</a></div>
</main>
<script>
(function(){{
  document.querySelectorAll('.product-gallery').forEach(function(g){{
    var track=g.querySelector('.pg-track'),
        dots=[].slice.call(g.querySelectorAll('.pg-dot')),
        count=g.querySelector('.pg-count'),
        n=parseInt(g.parentNode.getAttribute('data-frames'),10)||1;
    if(n<2) return;
    function idx(){{ return Math.round(track.scrollLeft/track.clientWidth); }}
    function go(i){{ track.scrollTo({{left:track.clientWidth*Math.max(0,Math.min(n-1,i)),behavior:'smooth'}}); }}
    function sync(){{ var i=idx();
      dots.forEach(function(d,j){{ d.classList.toggle('on',j===i); }});
      if(count) count.textContent=(i+1)+'/'+n; }}
    track.addEventListener('scroll',function(){{ window.requestAnimationFrame(sync); }},{{passive:true}});
    dots.forEach(function(d){{ d.addEventListener('click',function(e){{ e.preventDefault(); go(+d.dataset.i); }}); }});
    var p=g.querySelector('.pg-arw.prev'), nx=g.querySelector('.pg-arw.next');
    if(p) p.addEventListener('click',function(e){{ e.preventDefault(); go(idx()-1); }});
    if(nx) nx.addEventListener('click',function(e){{ e.preventDefault(); go(idx()+1); }});
  }});
}})();
</script>
"""
out = head + "\n</head>\n<body>" + NAV + body + TAIL

# ---------------------------------------------------------------------- checks
bad = []
if out.count("<h1") != 1:
    bad.append("h1 count")
if len(TITLE) > 65:
    bad.append(f"title {len(TITLE)} chars")
if not 110 <= len(DESC) <= 165:
    bad.append(f"description {len(DESC)} chars")
txt = plain(body)
if re.search(r"\bworth\b", txt, re.I):
    bad.append("banned word 'worth'")
if len(re.findall(r'<li class="rk"', out)) != N_TOP:
    bad.append("row count")
for b in top:
    if f'href="/brands/{b["slug"]}"' not in out:
        bad.append(f"{b['slug']} not linked")
for s, v in ind.items():
    if v.get("status") not in RANKS and s in brands and f'href="/brands/{s}"' in body:
        bad.append(f"{s} is marked {v.get('status')} but appears on the page")
if out.count('application/ld+json') != 1:
    bad.append("expected exactly one JSON-LD block")
if bad:
    raise SystemExit("!! " + "; ".join(bad))

print(f"{'wrote' if '--apply' in sys.argv else 'DRY RUN'} {URL} — {N_TOP} brands, "
      f"{len(txt.split())} words, floor {floor} posts")
for i, b in enumerate(top, 1):
    print(f"  {i:>2}. {plain(b['name']):28} {posts(b['slug']):>3}")
if missing_w:
    print("\n  !! no write-up yet (falls back to the Index line) — add to data/best25-writeups.json: " + ", ".join(missing_w))
if unchecked:
    print("\n  !! UNCHECKED brands with enough posts to make the list — research ownership, then add to "
          "data/independence.json:\n     " + ", ".join(f"{s} ({posts(s)})" for s in unchecked))
if "--apply" in sys.argv:
    open(OUT, "w", encoding="utf-8").write(out)
    # Each ranked brand's own page carries one quiet line back to the list (Lenny, 4 Oct 2026, SEO step 3).
    # Idempotent: the marked block is removed from every brand page first, then re-added for the current top 25.
    RK0, RK1 = "<!--TGI-BEST25-->", "<!--/TGI-BEST25-->"
    rank = {b["slug"]: i for i, b in enumerate(top, 1)}
    for s_ in brands:
        bp = os.path.join(ROOT, "brands", s_ + ".html")
        if not os.path.exists(bp): continue
        h = open(bp, encoding="utf-8").read(); h0 = h
        h = re.sub(re.escape(RK0) + r".*?" + re.escape(RK1), "", h, flags=re.S)
        if s_ in rank and '<div class="bp-actions">' in h:
            line = (f'{RK0}<div class="bp-rank" style="font-family:var(--bx-mono,ui-monospace,monospace);font-size:10.5px;'
                    f'letter-spacing:.14em;text-transform:uppercase;margin:12px 0 0">'
                    f'<a href="/brands/best-independent-golf-brands#no-{rank[s_]}" style="color:inherit;border-bottom:1px solid currentColor;text-decoration:none">'
                    f'No. {rank[s_]} on Our {N_TOP} Best Independent Golf Brands &rarr;</a></div>{RK1}')
            h = h.replace('<div class="bp-actions">', line + '<div class="bp-actions">', 1)
        if h != h0: open(bp, "w", encoding="utf-8").write(h)
    print(f"  rank line on {len(rank)} brand pages")
else:
    print("\npass --apply to write")
