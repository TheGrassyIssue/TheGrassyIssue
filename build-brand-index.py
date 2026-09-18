#!/usr/bin/env python3
"""/brands — the field-guide Brand Index (approved from mockups/brand-index.html,
2026-09-14). Rewrites brands/index.html IN PLACE, keeping the site's own head,
weather banner, nav, footer, mobile-menu / search / analytics scripts, and
replacing only the page body. Idempotent.

RUN ORDER: this must be the LAST step after build-brands.py + its header
chain (apply-header → type scripts → fix-mobile-menu → add-nav-search-box →
install-search brands/* → fix-mobile-nav → sync-brand-sitemap), because
build-brands.py regenerates brands/index.html in the OLD design every run.
    python3 build-brand-index.py --apply

Data: site/data/brands.json is the source of truth; card images are the ones
build-brands.py resolved into the page it just wrote (first slide of each
.bi-card), so the two designs never disagree on a brand's photo.

Editorial choices (change here, not in brands.json):
  MATERIAL   — DRAFT "material-forward" list; not a brands.json tag yet.
  PICKS      — the TGI PICKS dozen. Asserts every slug exists.
  VIBES      — the six tiles + their images.
  INTERRUPT  — where the editorial cuts fall (card index) and their images.
  Start Here was removed at Lenny's request (2026-09-14).

Copy rules: no "worth" (headline is "N brands to know."); no verdicts on
brands; counts are computed, never typed.

CSS is scoped under #bx and the three class names that collide with the site
sheet (.hero, .hero-img, .on) are renamed (.bx-hero, .bx-hero-img, .is-on).
"""
import json, re, os, html, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "brands", "index.html")
brands = json.load(open(os.path.join(ROOT, "data", "brands.json"), encoding="utf-8"))
page = open(SRC, encoding="utf-8").read()

# ---- images: from the old-design cards if present, else the previous bx build ----
cards = {}
for m in re.finditer(r'<div class="bi-card"[^>]*>(.*?)<a class="bi-covlink"', page, re.S):
    body = m.group(1)
    slug = re.search(r'href="/brands/([^"]+)"', body).group(1)
    img = re.search(r'<img src="([^"]+)"', body)
    cards[slug] = img.group(1) if img else None
if not cards:  # re-run on an already-converted page
    for m in re.finditer(r'<a class="bc" href="/brands/([^"]+)"[^>]*>.*?<img src="([^"]+)"', page, re.S):
        cards[m.group(1)] = m.group(2)
assert len(cards) >= len(brands) - 5, f"only {len(cards)} card images found"

CATL = {"apparel":"Apparel","equipment":"Clubs","bags":"Bags","headcovers":"Headcovers",
        "headwear":"Headwear","accessories":"Accessories","grips":"Grips","art":"Art","community":"Community"}
REGL = {"usa":"USA","texas":"Texas","australia":"Australia","japan":"Japan","europe":"Europe","world":"Elsewhere"}
TAGL = {"quiet-luxury":"Quiet","material-forward":"Material forward","made-by-hand":"Made by hand",
        "muni-energy":"Muni energy","gorpcore":"Gorpcore","design-nerd":"Design nerd",
        "loud-on-purpose":"Loud on purpose","post-round-friendly":"Post-round friendly",
        "collab-machine":"Collab machine","independent":"Independent","range-rat":"Range rat",
        "course-merch":"Course merch","member-guest":"Member-guest","dad-golf":"Dad golf",
        "collector":"Collector","loud":"Loud"}
MATERIAL = ["sentinel-golf","inside-story","manors","evnroll","piretti","p53","lamb-crafted","takomo-golf","sun-mountain"]
recent = sorted(brands, key=lambda b: b["added"], reverse=True)[:12]
NEW = {b["slug"] for b in recent}

data = []
for b in sorted(brands, key=lambda x: x["name"].lower().lstrip("&")):
    img = b.get("img") or cards.get(b["slug"])
    assert img, f"no image for {b['slug']}"
    assert os.path.exists(ROOT + img), f"missing file {img}"
    tags = list(b["tags"]) + (["material-forward"] if b["slug"] in MATERIAL else [])
    data.append({"slug": b["slug"], "name": b["name"], "loc": b["loc"],
                 "cat": CATL.get(b["cats"][0], b["cats"][0]) if b["cats"] else "",
                 "cats": b["cats"], "regions": b["regions"], "tags": tags, "line": b["line"],
                 "img": img, "url": f"/brands/{b['slug']}", "new": b["slug"] in NEW})
N = len(data)
by = {d["slug"]: d for d in data}
def count(pred): return sum(1 for d in data if pred(d))

VIBES = [
  ("quiet",    "QUIET",            "Understated. Considered. No giant logos.",                "QUIET LUXURY →",      "/images/quiet-golf/cardroom-corduroy-jacket-a2.jpg", "/brands/tag/quiet-luxury", lambda d: "quiet-luxury" in d["tags"]),
  ("material", "MATERIAL FORWARD", "New materials. Smarter construction. Better golf stuff.", "EXPLORE MATERIALS →", "/images/dyneema/walker-3.jpg", "#directory", lambda d: "material-forward" in d["tags"]),
  ("made",     "MADE",             "Small shops. Real hands. Limited quantities.",             "MADE BY HAND →",      "/images/texas-brands/artisan-3.jpg", "/brands/tag/made-by-hand", lambda d: "made-by-hand" in d["tags"]),
  ("muni",     "MUNI",             "More parking-lot beer than member-guest.",                "MUNI ENERGY →",       "/images/lions/hole16.jpg", "/brands/tag/muni-energy", lambda d: "muni-energy" in d["tags"]),
  ("outdoors", "OUTDOORS",         "Golf meets climbing, camping and trail culture.",         "GORPCORE →",          "/images/sentinel-golf/basecamp-walker-black-dyneema-0.jpg", "/brands/tag/gorpcore", lambda d: "gorpcore" in d["tags"]),
  ("new",      "NEW",              "Recently added to the Index.",                             "NEW TO THE INDEX →",  by[recent[0]["slug"]]["img"], "/brands/attr/new-to-index", lambda d: d["new"]),
]
INTERRUPT = [
  (12, "FROM TEXAS", "Golf stuff being made in our backyard.", "EXPLORE TEXAS →", "/images/texas-brands/hero-texas-brands.jpg", "region:texas"),
  (36, "FROM JAPAN", "Golf culture looks different over here.", "EXPLORE JAPAN →", "/images/japan-golf/itobori-copper-wedge.jpg", "region:japan"),
  (66, "TGI PICKS", "The brands we&rsquo;d actually spend our money on.", "SEE THE PICKS →", "/images/ny-trip/bethpage-bag.jpg", "picks"),
]
PICKS = ["sentinel-golf","mackenzie","sugarloaf-social-club","kingfisher-golf","edel-golf","criquet",
         "quiet-golf","manors","clint-orms","forden-golf","birds-of-condor","cloud-and-wind-golf"]
missing = [p for p in PICKS if p not in by]
assert not missing, f"PICKS not in brands.json: {missing}"
for _, _, _, _, img, _, _ in VIBES: assert os.path.exists(ROOT + img), img
for _, _, _, _, img, _ in INTERRUPT: assert os.path.exists(ROOT + img), img
HERO_IMG = "/images/lions/dusk.jpg"; assert os.path.exists(ROOT + HERO_IMG)
ENDPOINT = re.search(r"(https://script\.google\.com/macros/s/[A-Za-z0-9_-]+/exec)", open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()).group(1)

def esc(s): return html.escape(s, quote=True)

def card(d):
    tags = [t for t in d["tags"] if t in ("quiet-luxury","material-forward","made-by-hand","muni-energy","gorpcore","design-nerd")][:2] \
           or [t for t in d["tags"] if t in TAGL][:1]
    tg = "".join(f'<span class="tag">{TAGL[t].upper()}</span>' for t in tags)
    meta = " · ".join(x for x in (esc(d["loc"].upper().strip("— -")), esc(d["cat"].upper())) if x)
    text = (d["name"]+" "+d["loc"]+" "+d["line"]+" "+" ".join(TAGL.get(t,t) for t in d["tags"])+" "+" ".join(CATL.get(c,c) for c in d["cats"])).lower()
    pl = re.sub(r"\s+", " ", re.sub(r"&[a-z]+;|&#\d+;", "", d["name"])).strip()
    return (f'<a class="bc" href="{d["url"]}" data-slug="{d["slug"]}" data-letter="{d["name"].lstrip("&").strip()[0].upper()}" '
            f'data-cats="{" ".join(d["cats"])}" data-regions="{" ".join(d["regions"])}" '
            f'data-tags="{" ".join(d["tags"])}{" __new" if d["new"] else ""}" data-text="{esc(text)}">'
            f'<div class="bc-img"><img src="{esc(d["img"])}" alt="{esc(pl)}" loading="lazy"><span class="bc-view">VIEW BRAND →</span></div>'
            f'<div class="bc-body"><div class="bc-name">{esc(d["name"])}</div><div class="bc-meta">{meta}</div>'
            f'<p class="bc-line">{esc(d["line"])}</p><div class="bc-tags">{tg}</div></div></a>')

def interruption(kicker, title, cta, img, key):
    return (f'<section class="cut" data-key="{key}"><div class="cut-img"><img src="{img}" alt="" loading="lazy"></div>'
            f'<div class="cut-body"><div class="eyebrow">EDITORIAL</div><h2 class="cut-h">{kicker}</h2>'
            f'<p class="cut-p">{title}</p><a class="cta" href="#directory" data-jump="{key}">{cta}</a></div></section>')

ipos = {p: (k, t, c, i, key) for p, k, t, c, i, key in INTERRUPT}
grid = []
for i, d in enumerate(data):
    if i in ipos: grid.append('</div>' + interruption(*ipos[i]) + '<div class="grid">')
    grid.append(card(d))
GRID = '<div class="grid">' + "".join(grid) + '</div>'
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
have = {d["name"].lstrip("&").strip()[0].upper() for d in data}
AZ = "".join(f'<button class="az{"" if L in have else " off"}" data-letter="{L}"{"" if L in have else " disabled"}>{L}</button>' for L in letters)
VIBE_HTML = "".join(
    f'<a class="vibe" href="{href}" data-vibe="{k}"><div class="vibe-img"><img src="{img}" alt="" loading="lazy"></div>'
    f'<div class="vibe-body"><div class="vibe-name">{name}</div><p class="vibe-p">{desc}</p>'
    f'<div class="vibe-foot"><span class="cta">{cta}</span><span class="mono dim">{count(pred)} BRANDS</span></div></div></a>'
    for k, name, desc, cta, img, href, pred in VIBES)
def fgroup(title, items, kind):
    return (f'<div class="fg"><div class="fg-h">{title}</div>' +
            "".join(f'<label class="fo"><input type="checkbox" data-kind="{kind}" value="{v}"><span>{l}</span>'
                    f'<em>{count(lambda d, v=v, kind=kind: v in d[kind])}</em></label>' for v, l in items) + '</div>')
FILTERS = (fgroup("PRODUCT", list(CATL.items()), "cats")
         + fgroup("VIBE", [(k, TAGL[k]) for k in ["quiet-luxury","material-forward","made-by-hand","muni-energy","gorpcore","design-nerd","loud-on-purpose","post-round-friendly"]], "tags")
         + fgroup("LOCATION", list(REGL.items()), "regions"))

CSS = r"""
<style id="bx-css">
#bx{--bx-paper:#F4F1EA;--bx-paper2:#ECE8DF;--bx-ink:#141414;--bx-ink60:rgba(20,20,20,.62);--bx-ink30:rgba(20,20,20,.3);--bx-rule:rgba(20,20,20,.16);--bx-grass:#2D4A2B;--bx-serif:'Editors Note Text',Georgia,serif;--bx-mono:'JetBrains Mono',ui-monospace,Menlo,monospace;--bx-gutter:clamp(20px,3.2vw,44px);--bx-max:1440px;
  background:var(--bx-paper);color:var(--bx-ink);font-family:var(--bx-serif);font-size:16px;line-height:1.5}
#bx *{box-sizing:border-box}#bx h1,#bx h2,#bx h3,#bx p{margin:0}#bx a{color:inherit;text-decoration:none;border-bottom:0}
#bx img{display:block;width:100%;height:100%;object-fit:cover}
#bx .wrap{max-width:var(--bx-max);margin:0 auto;padding:0 var(--bx-gutter)}
#bx .mono{font-family:var(--bx-mono);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase}
#bx .dim{color:var(--bx-ink60)}#bx .eyebrow{font-family:var(--bx-mono);font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--bx-grass)}
#bx .cta{font-family:var(--bx-mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;border-bottom:1px solid var(--bx-ink);padding-bottom:3px;display:inline-block;width:max-content}
#bx h1,#bx h2,#bx h3{font-weight:700;letter-spacing:-.01em;line-height:1;font-family:var(--bx-serif)}
#bx .bx-hero{padding:clamp(48px,7vh,100px) 0 clamp(44px,6vh,80px)}
#bx .bx-hero .wrap{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr);gap:clamp(32px,5vw,80px);align-items:center}
#bx .bx-hero h1{font-size:clamp(52px,7.4vw,112px);letter-spacing:-.025em;line-height:.92;margin:24px 0 24px}
#bx .bx-hero h1 em{font-style:italic;font-weight:400}
#bx .bx-hero p{font-size:clamp(17px,1.35vw,20px);line-height:1.45;max-width:38ch;color:var(--bx-ink60)}
#bx .search{margin:2px 0 26px;border-bottom:1.5px solid var(--bx-ink);display:flex;align-items:center;gap:14px;padding-bottom:12px;max-width:560px}
#bx .search input{flex:1;background:transparent;border:0;outline:0;font-family:var(--bx-serif);font-size:22px;color:var(--bx-ink);border-radius:0;-webkit-appearance:none;padding:0}
#bx .search input::placeholder{color:var(--bx-ink30)}
#bx .search .k{font-family:var(--bx-mono);font-size:10px;letter-spacing:.12em;color:var(--bx-ink60);border:.5px solid var(--bx-rule);padding:4px 7px}
#bx .modes{margin-top:22px;display:flex;gap:28px}#bx .modes button{background:none;border:0;cursor:pointer;font-family:var(--bx-mono);font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--bx-ink);padding:0 0 4px;border-bottom:1px solid transparent}
#bx .modes button:hover{border-bottom-color:var(--bx-ink)}
#bx .bx-hero-img{aspect-ratio:4/5;background:var(--bx-paper2);position:relative}
#bx .bx-hero-img .cap{position:absolute;left:14px;bottom:12px;color:rgba(244,241,234,.8);font-family:var(--bx-mono);font-size:9.5px;letter-spacing:.16em;text-transform:uppercase}
#bx .bx-hero-img img{filter:saturate(.9) contrast(1.02)}
#bx .sec{padding:clamp(52px,7vh,90px) 0 0}
#bx .sh{display:flex;align-items:baseline;justify-content:space-between;border-top:1px solid var(--bx-ink);padding-top:18px;margin-bottom:34px;gap:20px}
#bx .sh h2{font-size:clamp(28px,3vw,42px)}#bx .sh .sub{font-family:var(--bx-mono);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--bx-ink60)}
#bx .vibes{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(18px,2vw,32px)}
#bx .vibe{display:flex;flex-direction:column;gap:14px}#bx .vibe-img{aspect-ratio:4/3;overflow:hidden;background:var(--bx-paper2)}
#bx .vibe-img img{transition:transform 1.4s cubic-bezier(.2,.7,.2,1);filter:saturate(.92)}#bx .vibe:hover .vibe-img img{transform:scale(1.03)}
#bx .vibe-name{font-family:var(--bx-mono);font-size:13px;letter-spacing:.22em;font-weight:500}
#bx .vibe-p{font-size:16px;color:var(--bx-ink60);margin:4px 0 8px}#bx .vibe-foot{display:flex;justify-content:space-between;align-items:baseline}
#bx .dir-tools{display:flex;flex-direction:column;gap:18px;margin-bottom:30px}
#bx .azbar{display:flex;flex-wrap:wrap;gap:2px}
#bx .az{background:none;border:0;cursor:pointer;font-family:var(--bx-mono);font-size:12px;letter-spacing:.1em;width:34px;height:34px;color:var(--bx-ink);border-bottom:1px solid transparent}
#bx .az:hover{border-bottom-color:var(--bx-ink)}#bx .az.off{color:var(--bx-ink30);cursor:default}
#bx .dir-state{display:flex;justify-content:space-between;align-items:center;gap:20px;font-family:var(--bx-mono);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--bx-ink60);min-height:20px}
#bx .dir-state b{color:var(--bx-ink);font-weight:500}#bx .dir-state button{background:none;border:0;cursor:pointer;font:inherit;color:var(--bx-ink);border-bottom:1px solid var(--bx-ink);padding:0 0 2px;letter-spacing:inherit;text-transform:inherit}
#bx .grid{display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(22px,2.4vw,36px) clamp(16px,1.6vw,26px);padding-bottom:40px}
#bx .bc{display:flex;flex-direction:column;gap:12px}#bx .bc.hide{display:none}
/* .bc-body and .vibe-body are the text halves of their cards. They looked like
   they needed no rule — every child is styled and the parent flex gap does the
   spacing — so they shipped without one, which verify-post correctly flagged
   (house rule: every class used has a CSS rule). min-width:0 is the right rule
   rather than a placeholder: a flex child defaults to min-width:auto, so a long
   unbroken brand name would push the card wider than its column instead of
   wrapping. Costs nothing on the other 131. */
#bx .bc-body{min-width:0}
#bx .vibe-body{min-width:0}
#bx .bc-img{aspect-ratio:4/5;overflow:hidden;background:var(--bx-paper2);position:relative}
#bx .bc-img img{transition:transform 1.2s cubic-bezier(.2,.7,.2,1)}#bx .bc:hover .bc-img img{transform:scale(1.035)}
#bx .bc-view{position:absolute;left:12px;bottom:10px;background:var(--bx-paper);padding:6px 9px;font-family:var(--bx-mono);font-size:9.5px;letter-spacing:.16em;opacity:0;transform:translateY(4px);transition:all .35s}
#bx .bc:hover .bc-view{opacity:1;transform:none}
#bx .bc-name{font-size:19px;font-weight:700;letter-spacing:-.01em;line-height:1.1}
#bx .bc-meta{font-family:var(--bx-mono);font-size:9.5px;letter-spacing:.14em;color:var(--bx-ink60);margin-top:4px}
#bx .bc-line{font-size:14.5px;line-height:1.45;color:var(--bx-ink);opacity:.82;margin-top:8px}
#bx .bc-tags{margin-top:10px;display:flex;gap:6px;flex-wrap:wrap}
#bx .tag{font-family:var(--bx-mono);font-size:9px;letter-spacing:.14em;border:.5px solid var(--bx-grass);color:var(--bx-grass);padding:3px 7px}
#bx .cut{display:grid;grid-template-columns:1.2fr 1fr;gap:clamp(24px,3vw,56px);align-items:center;margin:36px 0 70px;border-top:1px solid var(--bx-ink);border-bottom:1px solid var(--bx-ink);padding:36px 0}
#bx .cut-img{aspect-ratio:3/2;overflow:hidden;background:var(--bx-paper2)}#bx .cut-img img{filter:saturate(.9)}
#bx .cut-body{display:flex;flex-direction:column;gap:16px}#bx .cut-h{font-size:clamp(40px,5vw,72px);letter-spacing:-.02em}
#bx .cut-p{font-size:clamp(18px,1.5vw,22px);color:var(--bx-ink60);max-width:32ch}#bx .cut.hide{display:none}
#bx .zero{display:none;font-family:var(--bx-serif);font-style:italic;font-size:18px;color:var(--bx-ink60);padding:10px 0 60px}#bx .zero.show{display:block}
#bx .submit{border-top:1px solid var(--bx-ink);margin-top:20px;padding:56px 0 64px;display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:end}
#bx .submit h2{font-size:clamp(30px,3.4vw,48px);margin-top:14px}#bx .submit p{color:var(--bx-ink60);font-size:17px;max-width:40ch;margin-top:12px}
#bx .nl{background:var(--bx-grass);color:var(--bx-paper);padding:clamp(64px,9vh,120px) 0}
#bx .nl .wrap{display:grid;grid-template-columns:1.2fr 1fr;gap:48px;align-items:end}
#bx .nl h2{font-size:clamp(40px,5.4vw,84px);letter-spacing:-.02em;line-height:.95;margin-top:18px}#bx .nl p{opacity:.8;font-size:17px;max-width:36ch;margin-top:18px}
#bx .nl form{display:flex;border-bottom:1.5px solid rgba(244,241,234,.6);padding-bottom:12px}
#bx .nl input{flex:1;background:transparent;border:0;outline:0;color:var(--bx-paper);font-family:var(--bx-serif);font-size:20px;min-width:0;border-radius:0;-webkit-appearance:none;padding:0}#bx .nl input::placeholder{color:rgba(244,241,234,.5)}
#bx .nl button{background:none;border:0;color:var(--bx-paper);font-family:var(--bx-mono);font-size:11px;letter-spacing:.16em;cursor:pointer}
#bx .nl .thanks{display:none;font-style:italic;font-size:20px}
#bx .drawer{position:fixed;inset:0;z-index:80;display:none}#bx .drawer.open{display:block}
#bx .scrim{position:absolute;inset:0;background:rgba(20,20,20,.28)}
#bx .panel{position:absolute;top:0;right:0;bottom:0;width:min(440px,92vw);background:var(--bx-paper);border-left:.5px solid var(--bx-ink);padding:26px 30px;display:flex;flex-direction:column;overflow:auto}
#bx .panel-h{display:flex;justify-content:space-between;align-items:center;margin-bottom:26px}#bx .panel-h b{font-family:var(--bx-mono);font-size:11px;letter-spacing:.2em;font-weight:500}
#bx .panel-h button{background:none;border:0;cursor:pointer;font-family:var(--bx-mono);font-size:10.5px;letter-spacing:.14em;color:var(--bx-ink60)}
#bx .fg{border-top:1px solid var(--bx-rule);padding:18px 0}#bx .fg-h{font-family:var(--bx-mono);font-size:10px;letter-spacing:.22em;color:var(--bx-grass);margin-bottom:12px}
#bx .fo{display:flex;align-items:center;gap:12px;padding:6px 0;cursor:pointer;font-size:16px}#bx .fo input{width:14px;height:14px;accent-color:var(--bx-ink);margin:0}#bx .fo em{margin-left:auto;font-style:normal;font-family:var(--bx-mono);font-size:10px;color:var(--bx-ink30)}
#bx .panel-f{margin-top:auto;padding-top:20px;border-top:1px solid var(--bx-ink);display:flex;justify-content:space-between;align-items:center}
#bx .panel-f .apply{background:var(--bx-ink);color:var(--bx-paper);border:0;padding:14px 18px;font-family:var(--bx-mono);font-size:11px;letter-spacing:.16em;cursor:pointer}
#bx .panel-f .clear{background:none;border:0;cursor:pointer;font-family:var(--bx-mono);font-size:10.5px;letter-spacing:.14em;color:var(--bx-ink60)}
@media(max-width:1000px){#bx .bx-hero .wrap{grid-template-columns:1fr}#bx .bx-hero-img{aspect-ratio:3/2}#bx .vibes{grid-template-columns:1fr 1fr}#bx .grid{grid-template-columns:repeat(3,1fr)}#bx .cut{grid-template-columns:1fr}#bx .submit,#bx .nl .wrap{grid-template-columns:1fr}}
@media(max-width:640px){#bx .grid{grid-template-columns:1fr 1fr}#bx .vibes{grid-template-columns:1fr}#bx .bx-hero{padding-top:36px}}
</style>
"""

BODY = f"""<!--BX-BRAND-INDEX-->
<div id="bx">
<section class="bx-hero"><div class="wrap">
  <div>
    <div class="eyebrow">{N} INDEPENDENT GOLF BRANDS &middot; AUSTIN</div>
    <h1>{N} brands<br>to <em>know.</em></h1>
    <p>A running list of independent golf brands, makers and oddities from Texas to Tokyo &mdash; indie labels, small-batch workshops and under-the-radar names, every one with its own page. Researched and selected by The Grassy Issue.</p>
    <div class="modes"><button type="button" id="bx-m-discover">DISCOVER</button><button type="button" id="bx-m-az">BROWSE A&ndash;Z</button><button type="button" data-open-filter>FILTER</button></div>
  </div>
  <div class="bx-hero-img"><img src="{HERO_IMG}" alt="Lions Municipal Golf Course at dusk, Austin"><div class="cap">LIONS MUNICIPAL &middot; AUSTIN, TX</div></div>
</div></section>

<section class="sec" id="vibes"><div class="wrap">
  <div class="sh"><h2>Browse by vibe</h2><span class="sub">SIX WAYS IN</span></div>
  <div class="vibes">{VIBE_HTML}</div>
</div></section>

<section class="sec" id="directory"><div class="wrap">
  <div class="sh"><h2>The full list</h2><span class="sub" id="bx-count">{N} BRANDS</span></div>
  <div class="search"><input id="bx-q" type="search" placeholder="Search brands, gear, or a vibe&hellip;" autocomplete="off" aria-label="Search the Brand Index"><span class="k">/</span></div>
  <div class="dir-tools"><div class="azbar" role="navigation" aria-label="Jump to letter">{AZ}</div>
    <div class="dir-state"><span id="bx-label">ALPHABETICAL</span><button type="button" data-open-filter>FILTER &rarr;</button></div></div>
  {GRID}
  <p class="zero" id="bx-zero">Nothing in that combination yet &mdash; the Index grows every week.</p>
  <div class="submit"><div><div class="eyebrow">KNOW SOMETHING WE DON&rsquo;T?</div><h2>The Index should never feel finished.</h2><p>Found a brand that belongs here? Send it our way.</p></div><a class="cta" href="mailto:L4harrington@gmail.com?subject=A%20brand%20for%20the%20Index">SUBMIT A BRAND &rarr;</a></div>
</div></section>

<section class="nl" id="join"><div class="wrap">
  <div><div class="eyebrow" style="color:rgba(244,241,234,.7)">THE NEWSLETTER</div><h2>Good golf stuff.<br>Once a week.</h2><p>Independent brands, courses, gear and stories to know.</p></div>
  <div><form id="bx-nl-form" onsubmit="return bxSubmitNL(event)"><input id="bx-nl-email" type="email" required placeholder="Your email" aria-label="Email"><button type="submit">SUBSCRIBE &rarr;</button></form>
  <div class="thanks" id="bx-nl-thanks">You&rsquo;re in. First drop incoming.</div><iframe name="bx-nl-frame" style="display:none" title="hidden"></iframe></div>
</div></section>

<div class="drawer" id="bx-drawer"><div class="scrim"></div><aside class="panel" aria-label="Filter the Index">
  <div class="panel-h"><b>FILTER</b><button type="button" id="bx-d-close">CLOSE &#10005;</button></div>
  {FILTERS}
  <div class="panel-f"><button type="button" class="clear" id="bx-d-clear">CLEAR ALL</button><button type="button" class="apply" id="bx-d-apply"><span id="bx-apply-count">SHOW {N} BRANDS &rarr;</span></button></div>
</aside></div>
</div>
<!--/BX-BRAND-INDEX-->
"""

JS = r"""
<script id="bx-js">
(function(){
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const cards=$$('#bx .bc'),cuts=$$('#bx .cut'),state={q:'',cats:new Set(),tags:new Set(),regions:new Set(),vibe:null,picks:false};
const PICKS=new Set(__PICKS__);
const VIBE={quiet:'quiet-luxury',material:'material-forward',made:'made-by-hand',muni:'muni-energy',outdoors:'gorpcore',new:'__new'};
function apply(){
  let q=state.q.trim().toLowerCase(),n=0;
  cards.forEach(c=>{
    let ok=true;
    if(q) ok=c.dataset.text.includes(q);
    if(ok&&state.cats.size) ok=[...state.cats].some(v=>c.dataset.cats.split(' ').includes(v));
    if(ok&&state.tags.size) ok=[...state.tags].some(v=>c.dataset.tags.split(' ').includes(v));
    if(ok&&state.regions.size) ok=[...state.regions].some(v=>c.dataset.regions.split(' ').includes(v));
    if(ok&&state.vibe) ok=c.dataset.tags.split(' ').includes(state.vibe);
    if(ok&&state.picks) ok=PICKS.has(c.dataset.slug);
    c.classList.toggle('hide',!ok); if(ok)n++;
  });
  const filtering=!!(q||state.cats.size||state.tags.size||state.regions.size||state.vibe||state.picks);
  cuts.forEach(x=>x.classList.toggle('hide',filtering));
  $('#bx-zero').classList.toggle('show',n===0);
  $('#bx-count').textContent=(filtering?n+' OF ':'')+cards.length+' BRANDS';
  $('#bx-label').innerHTML=filtering?('SHOWING <b>'+describe()+'</b> &middot; <button type="button" id="bx-clr">CLEAR</button>'):'ALPHABETICAL';
  const b=$('#bx-clr'); if(b)b.onclick=clearAll;
  $('#bx-apply-count').textContent='SHOW '+n+' BRANDS →';
}
function labelOf(v){const el=document.querySelector('#bx .fo input[value="'+v+'"]');return el?el.nextElementSibling.textContent.toUpperCase():(v==='__new'?'NEW':v.toUpperCase());}
function describe(){const p=[];if(state.q.trim())p.push('“'+state.q.trim()+'”');if(state.vibe)p.push(labelOf(state.vibe));if(state.picks)p.push('TGI PICKS');[...state.cats,...state.tags,...state.regions].forEach(v=>p.push(labelOf(v)));return p.join(' · ');}
function clearAll(){state.q='';$('#bx-q').value='';state.cats.clear();state.tags.clear();state.regions.clear();state.vibe=null;state.picks=false;$$('#bx .fo input').forEach(i=>i.checked=false);apply();}
function goDir(){$('#directory').scrollIntoView({behavior:'smooth',block:'start'});}
$('#bx-q').addEventListener('input',e=>{state.q=e.target.value;state.vibe=null;state.picks=false;apply();});
document.addEventListener('keydown',e=>{const t=document.activeElement.tagName;if(e.key==='/'&&t!=='INPUT'&&t!=='TEXTAREA'){e.preventDefault();goDir();$('#bx-q').focus({preventScroll:true});}});
$$('#bx .vibe').forEach(v=>v.addEventListener('click',e=>{e.preventDefault();clearAll();state.vibe=VIBE[v.dataset.vibe];apply();goDir();}));
$$('#bx [data-jump]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();clearAll();const j=a.dataset.jump;if(j.startsWith('region:'))state.regions.add(j.split(':')[1]);if(j==='picks')state.picks=true;apply();goDir();}));
$$('#bx .az').forEach(b=>b.addEventListener('click',()=>{const t=cards.find(c=>!c.classList.contains('hide')&&c.dataset.letter===b.dataset.letter);if(t){window.scrollTo({top:t.getBoundingClientRect().top+window.scrollY-90,behavior:'instant'});}}));
const drawer=$('#bx-drawer');function openD(){drawer.classList.add('open');document.body.style.overflow='hidden'}function closeD(){drawer.classList.remove('open');document.body.style.overflow=''}
$$('#bx [data-open-filter]').forEach(b=>b.onclick=openD);$('#bx-d-close').onclick=closeD;$('#bx .scrim').onclick=closeD;
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&drawer.classList.contains('open'))closeD();});
$$('#bx .fo input').forEach(i=>i.addEventListener('change',()=>{const s=state[i.dataset.kind];i.checked?s.add(i.value):s.delete(i.value);state.vibe=null;state.picks=false;apply();}));
$('#bx-d-apply').onclick=()=>{closeD();goDir();};$('#bx-d-clear').onclick=clearAll;
$('#bx-m-discover').onclick=()=>$('#vibes').scrollIntoView({behavior:'smooth'});$('#bx-m-az').onclick=goDir;
window.bxSubmitNL=function(e){e.preventDefault();const email=$('#bx-nl-email').value;const f=document.createElement('form');f.method='POST';f.action='__ENDPOINT__';f.target='bx-nl-frame';
  const inp=document.createElement('input');inp.type='hidden';inp.name='email';inp.value=email;f.appendChild(inp);document.body.appendChild(f);f.submit();document.body.removeChild(f);
  $('#bx-nl-form').style.display='none';$('#bx-nl-thanks').style.display='block';return false;};
// deep links: /brands/#tag=made-by-hand, #region=japan, #q=dyneema
const h=new URLSearchParams(location.hash.replace(/^#/,''));
if(h.get('tag')){state.tags.add(h.get('tag'));const i=document.querySelector('#bx .fo input[value="'+h.get('tag')+'"]');if(i)i.checked=true;}
if(h.get('region')){state.regions.add(h.get('region'));const i=document.querySelector('#bx .fo input[value="'+h.get('region')+'"]');if(i)i.checked=true;}
if(h.get('q')){state.q=h.get('q');$('#bx-q').value=h.get('q');}
apply();
window.addEventListener('hashchange',()=>location.reload());
})();
</script>
"""

# ---- splice ----------------------------------------------------------------
nav_end = page.find("</nav>") + len("</nav>")
foot = page.find("<footer")
assert nav_end > 6 and foot > nav_end, "could not find nav/footer boundaries"
head_end = page.find("</head>")
head = page[:head_end]
head = re.sub(r'<style id="bx-css">.*?</style>\n?', "", head, flags=re.S)
# SEE THE VOCABULARY NOTE IN build-brands.py — it carries the evidence for why
# the title reads the way it does. This file writes the head LAST, so THESE are
# the strings that ship; the equivalents over there only matter between build
# steps. Keep the two in agreement or the next person debugging a title will
# read the wrong file. The year is derived there and imported here for the same
# reason: a hardcoded year goes stale in January without anyone noticing.
YEAR = __import__("datetime").date.today().year
head = re.sub(r'<title>[^<]*</title>', f"<title>{N} Independent Golf Brands to Know ({YEAR}) | The Grassy Issue</title>", head)
head = re.sub(r'(<meta name="description" content=")[^"]*(")',
              lambda m: m.group(1) + f"A running list of {N} independent and indie golf brands — apparel, bags, headcovers and under-the-radar makers from Texas to Tokyo, searchable by product, vibe and location." + m.group(2), head)
head = re.sub(r'(<meta property="og:title" content=")[^"]*(")',
              lambda m: m.group(1) + f"{N} Independent Golf Brands to Know ({YEAR})" + m.group(2), head)
head = re.sub(r'(<meta property="og:description" content=")[^"]*(")',
              lambda m: m.group(1) + f"A running list of {N} independent and indie golf brands, searchable by product, vibe and location." + m.group(2), head)
tail = page[foot:]
# drop the old page's own pill/gallery script(s) and any previous bx-js
tail = re.sub(r'<script>\s*\(function\(\)\{\s*var pills=.*?</script>\s*', "", tail, count=1, flags=re.S)
tail = re.sub(r'<script id="bx-js">.*?</script>\s*', "", tail, flags=re.S)
tail = tail.replace("<footer", JS.replace("__PICKS__", json.dumps(PICKS)).replace("__ENDPOINT__", ENDPOINT) + "<footer", 1)
out = head + CSS + page[head_end:nav_end] + "\n" + BODY + tail
hero_html = out.split('<section class="bx-hero">')[1].split("</section>")[0]
assert 'id="bx-q"' not in hero_html, (
    "the search input is back in the hero. It was moved into #directory on\n"
    "2026-09-14 because typing in it fired goDir(), which smooth-scrolled the\n"
    "page away from the box mid-keystroke. Lenny: \"move the search bar lower\n"
    "so it dosent glitch out.\"")
dir_html = out.split('id="directory"')[1]
assert 'id="bx-q"' in dir_html.split("</section>")[0], "search input is not in #directory"
assert "if(e.target.value.length>1)goDir()" not in out, "auto-scroll-on-type is back"
assert out.count("<!--BX-BRAND-INDEX-->") == 1 and out.count('id="bx-js"') == 1 and out.count('id="bx-css"') == 1
assert "bi-card" not in out.split("<!--BX-BRAND-INDEX-->")[1].split("<!--/BX-BRAND-INDEX-->")[0]
assert not re.search(r"\bworth\b", re.sub(r"fort worth", "", re.sub(r"<[^>]+>", " ", BODY), flags=re.I), re.I), "banned word in body copy"

print(f"{N} brands · vibes " + ", ".join(f"{n}={count(p)}" for _, n, _, _, _, _, p in VIBES) + f" · {len(out)//1024} KB")
if "--apply" in sys.argv:
    open(SRC, "w", encoding="utf-8").write(out); print("wrote brands/index.html")
else:
    print("(dry run — pass --apply)")
