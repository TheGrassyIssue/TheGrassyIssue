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

That rule took out several of the most-covered brands in the Index (Malbon,
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


ranked = sorted((b for s, b in brands.items() if ind.get(s, {}) and ind[s].get("status") == "independent"),
                key=lambda b: (-posts(b["slug"]), plain(b["name"]).lower()))
if len(ranked) < N_TOP:
    raise SystemExit(f"only {len(ranked)} verified independents — need {N_TOP}. Check more brands.")
top = ranked[:N_TOP]
floor = posts(top[-1]["slug"])
if floor < 1:
    raise SystemExit("a brand with no posts made the list — the mentions file looks empty")
unchecked = sorted((s for s in brands if s not in ind and posts(s) >= floor), key=lambda s: -posts(s))

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
#bi .bi-back{margin-top:40px;font-family:var(--bx-mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase}
#bi .bi-back a{color:inherit}
@media(max-width:760px){#bi .rk{grid-template-columns:52px 1fr;gap:16px}#bi .rk-n{font-size:40px}
 #bi .rk-img{grid-column:2}#bi .rk-body{grid-column:2}}
</style>"""

# ---------------------------------------------------------------------- copy
today = datetime.date.today()
asof = f"{today:%B} {today.day}, {today.year}"
n1, n2, n3 = top[0], top[1], top[2]
p1 = posts(n1["slug"])
W = {25: "twenty-five"}
num = lambda n: "one post" if n == 1 else f"{n} posts"

INTRO = f"""<p>These are the {W[N_TOP]} independent golf brands The Grassy Issue has written about most.
We ranked them on the record, not on a gut call: every page on the site that
mentions a brand counts once, and the brands with the most pages sit at the top.
<strong>{esc(plain(n1['name']))}</strong> leads with {num(p1)}, followed by
<strong>{esc(plain(n2['name']))}</strong> and <strong>{esc(plain(n3['name']))}</strong>.</p>
<p>Each brand has its own page in the Brand Index, which links out to every post that counts toward its number.
Read the list as a map of where our attention has actually gone in {YEAR}: the brands we keep going back to for
drops, gift guides, roundups and field notes.</p>"""

HOW = f"""<h2>How this list works</h2>
<p>Independent means structural here, not a matter of style. A brand makes the list only if its founders or a
family still own it, with no corporate parent, no stock listing and no venture-capital, private-equity or
strategic investor on the books. Crowdfunding, a friend's small angel cheque and bank debt do not count against a
brand, because none of them hands control to anyone else. We also required a named owner: if we could not find
who owns a brand in public records, interviews or the brand's own pages, it waits until we can.</p>
<p>We checked ownership for every brand near the top of our coverage on {asof}, using company registers,
funding filings, trade press and founder interviews. The rank itself is the number of TGI pages that mention the
brand. It updates whenever the Brand Index is rebuilt, so this page moves as our coverage does.</p>"""

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
        f'<div class="rk-meta"><b>{num(posts(s))}</b> &middot; {meta}</div>'
        f'<p>{esc(b.get("line", ""))}</p>'
        f'<p class="rk-own">{esc(ind[s]["owner"])}</p>'
        f'<a class="rk-go" href="/brands/{s}">See the brand and its posts &rarr;</a></div></li>')

H1 = f"Our {N_TOP} Best Independent Golf Brands"  # Lenny, 24 Sep 2026
TITLE = f"Our {N_TOP} Best Independent Golf Brands ({YEAR}) | The Grassy Issue"
DESC = (f"The {N_TOP} independent golf brands The Grassy Issue has covered most in {YEAR}, ranked by post count, "
        f"with who owns each one and how we checked.")

schema = {"@context": "https://schema.org", "@graph": [
    {"@type": "CollectionPage", "name": H1, "description": DESC, "url": f"https://thegrassyissue.com{URL}",
     "dateModified": today.isoformat(),
     "isPartOf": {"@type": "WebSite", "name": "The Grassy Issue", "url": "https://thegrassyissue.com"},
     "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
         {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
         {"@type": "ListItem", "position": 2, "name": "The Brand Index", "item": "https://thegrassyissue.com/brands"},
         {"@type": "ListItem", "position": 3, "name": H1}]},
     "mainEntity": {"@type": "ItemList", "itemListOrder": "https://schema.org/ItemListOrderDescending",
                    "numberOfItems": N_TOP, "itemListElement": [
                        {"@type": "ListItem", "position": i, "name": plain(b["name"]),
                         "url": f"https://thegrassyissue.com/brands/{b['slug']}"} for i, b in enumerate(top, 1)]}}]}

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
  <div class="bi-intro">
{INTRO}
  </div>
  <section class="bi-how">
{HOW}
  </section>
  <ol class="bi-list">
{chr(10).join(rows)}
  </ol>
  <div class="bi-back"><a href="/brands/tag/independent">All independent brands in the Index &rarr;</a> &nbsp;&middot;&nbsp; <a href="/brands">&larr; The full Brand Index</a></div>
</main>

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
    if v.get("status") != "independent" and s in brands and f'href="/brands/{s}"' in body:
        bad.append(f"{s} is marked {v.get('status')} but appears on the page")
if out.count('application/ld+json') != 1:
    bad.append("expected exactly one JSON-LD block")
if bad:
    raise SystemExit("!! " + "; ".join(bad))

print(f"{'wrote' if '--apply' in sys.argv else 'DRY RUN'} {URL} — {N_TOP} brands, "
      f"{len(txt.split())} words, floor {floor} posts")
for i, b in enumerate(top, 1):
    print(f"  {i:>2}. {plain(b['name']):28} {posts(b['slug']):>3}")
if unchecked:
    print("\n  !! UNCHECKED brands with enough posts to make the list — research ownership, then add to "
          "data/independence.json:\n     " + ", ".join(f"{s} ({posts(s)})" for s in unchecked))
if "--apply" in sys.argv:
    open(OUT, "w", encoding="utf-8").write(out)
else:
    print("\npass --apply to write")
