#!/usr/bin/env python3
"""Generate /brands/index.html from data/brands.json — the master Brand Index.

Single source of truth: data/brands.json. Add a brand there, rerun this script.
Fields: slug, name, loc, regions[], cats[], line, url, img (optional; auto-resolved).

Design: TGI native — paper background, existing tokens, mono kickers, Fraunces
headings, product-card visual language. Filters are client-side pills; region
hubs get their own static pages (built separately) so discovery is crawl-safe.

House rules honored: H1 avoids the banned word ("Worth Knowing" from the brief
is replaced with the existing franchise name "Brands to Know"). All images local.
"""
import json, os, re, html as H

ROOT = os.path.dirname(os.path.abspath(__file__))

GA = ('<!-- Google Analytics 4 (gtag.js) -->\n'
      '<script async src="https://www.googletagmanager.com/gtag/js?id=G-G89M4116SB"></script>\n'
      '<script>\n  window.dataLayer = window.dataLayer || [];\n  function gtag(){dataLayer.push(arguments);}\n'
      "  gtag('js', new Date());\n  gtag('config', 'G-G89M4116SB');\n</script>")
GC = ('<!-- GoatCounter analytics -->\n<script data-goatcounter="https://thegrassyissue.goatcounter.com/count" '
      'async src="//gc.zgo.at/count.js"></script>')
BRANDS = json.load(open(os.path.join(ROOT, "data", "brands.json")))
MENTIONS = json.load(open(os.path.join(ROOT, "data", "brand-mentions.json")))

# ---------------------------------------------------------------- card images
#
# Lenny, 2026-08-30: "the brands page is showing the same image multiple times."
#
# THE BUG. The old anchor branch searched a HARDCODED list of image directories
# ["texas-brands", "aussie", "left-of-field", …]. Any post whose images live
# somewhere else — /images/grips/, /images/whitetee26/ — missed every candidate
# and fell through to the page-hero fallback. Eleven brands across three posts
# therefore shared three images:
#
#     5x /images/whitetee26/hero.jpg   3 Putt Round, ANTi Country Club Tokyo,
#                                      Badlands, Pluto Golf, Rebolf
#     4x /images/grips/hero.jpg        Garsen, RipIt, Rosemark, Stick
#     2x /images/realtree-puma/hero.jpg  PUMA Golf, Realtree
#
# The failure was silent because a page hero is a real, existing file — nothing
# 404s, the cards just all look the same. `missing_img` only ever caught brands
# that resolved to NOTHING, never brands that resolved to the SAME thing.
#
# THE FIX. Read the post instead of guessing at directory names, in four steps,
# most-specific first, and assert afterwards that no two brands collide.


def _norm(x):
    """Collapse to comparable letters+digits: 'ANTi Country Club Tokyo' -> anticountryclubtokyo."""
    return re.sub(r"[^a-z0-9]", "", (x or "").lower())


def _page_of(url):
    p = ROOT + url.split("#")[0] + ".html"
    return p if os.path.exists(p) else None


def _span(h, i, tag):
    """End offset of the element opening at i, by TAG DEPTH.

    A first cut ended each card at "the next product-card, else i+9000 chars".
    The LAST card in a post has no next card, so its block ran 9000 characters
    past the closing </div> and swallowed the More-from-Feed thumbnails — which
    is how 3 Putt Round ended up showing a Sun Mountain photo. Never bound HTML
    by a character count."""
    d = 0
    for m in re.finditer(rf"<{tag}\b|</{tag}>", h[i:]):
        d += -1 if m.group(0).startswith("</") else 1
        if d == 0:
            return i + m.end()
    return len(h)


def _cards(h):
    """[(brand text, name text, [frame paths])] for every product card on a page.

    Handles both card shapes in the wild: <div class="product-card"> (gallery
    posts) and <a class="product-card"> (older flat-image posts)."""
    out = []
    for m in re.finditer(r'<(div|a) class="product-card[^"]*"[^>]*>', h):
        blk = h[m.start():_span(h, m.start(), m.group(1))]
        bm = re.search(r'<div class="product-brand">(.*?)</div>', blk, re.S)
        nm = re.search(r'<div class="product-name">(.*?)</div>', blk, re.S)
        frames = re.findall(r'src="(/images/[^"]+)"', blk)
        txt = lambda mm: H.unescape(re.sub(r"<[^>]+>", " ", mm.group(1))) if mm else ""
        out.append((txt(bm), txt(nm), frames))
    return out


def resolve_frames(b):
    """Every frame we can honestly attribute to THIS brand, best first."""
    if b.get("img") and os.path.exists(ROOT + b["img"]):
        return [b["img"]]
    url, name = b["url"], b["name"]
    page = _page_of(url)
    h = open(page, encoding="utf-8").read() if page else ""
    dirs = list(dict.fromkeys(re.findall(r'src="(/images/[^/]+)/', h)))

    # 1. anchor -> <dir>/<frag>-N.jpg, across the dirs the page ACTUALLY uses
    if "#" in url:
        frag = url.split("#")[1]
        alias = {"lof": "xelements-polo-0", "midiron": "detour-stripe-polo",
                 "walker": "blooming-grounds-knit-polo-1"}.get(frag, frag)
        for d in dirs:
            hits = [f"{d}/{alias}-{n}.jpg" for n in range(6)
                    if os.path.exists(ROOT + f"{d}/{alias}-{n}.jpg")]
            if hits:
                return hits

    # 2. the product card whose .product-brand names this brand
    for bt, nt, frames in _cards(h):
        lead = _norm(bt.split("·")[0])
        if lead and frames and (lead == _norm(name) or _norm(name).startswith(lead) and len(lead) > 4):
            return frames

    # 3. filename stem that matches the brand — catches posts (the grip report)
    #    where .product-brand holds a LOCATION rather than the brand name.
    n = _norm(name)
    for d in dirs:
        stems = sorted({re.sub(r"-\d+$", "", os.path.splitext(f)[0])
                        for f in os.listdir(ROOT + d) if f.endswith(".jpg")})
        for s in stems:
            ns = _norm(s)
            if len(ns) > 3 and (ns == n or n.startswith(ns)):
                hits = [f"{d}/{s}-{k}.jpg" for k in range(6)
                        if os.path.exists(ROOT + f"{d}/{s}-{k}.jpg")]
                if hits:
                    return hits
                if os.path.exists(ROOT + f"{d}/{s}.jpg"):
                    return [f"{d}/{s}.jpg"]

    # 4. page hero — LAST resort, and now reported rather than shipped silently
    m = re.search(r'<div class="drop-hero-img">\s*<img src="([^"]+)"', h)
    if m and os.path.exists(ROOT + m.group(1)):
        return [m.group(1)]
    return []


def resolve_img(b):
    f = resolve_frames(b)
    return f[0] if f else None

CATS = [("apparel","Apparel"),("equipment","Clubs"),("bags","Bags"),
        ("headcovers","Headcovers"),("headwear","Headwear"),("accessories","Accessories"),
        ("grips","Grips"),("art","Art"),("community","Community")]
REGIONS = [("usa","USA"),("texas","Texas"),("australia","Australia"),
           ("japan","Japan"),("europe","Europe"),("world","Elsewhere")]
CATL = dict(CATS); REGL = dict(REGIONS)

# Lifestyle-first gallery frames, chosen by the ranker in tools (see reference memory).
# Falls back to the single resolved thumbnail when a brand has no scored frames.
GAL = json.load(open(os.path.join(ROOT, "data", "brand-gallery.json"), encoding="utf-8")) \
      if os.path.exists(os.path.join(ROOT, "data", "brand-gallery.json")) else {}

TAGS = [("muni-energy","Muni energy"),("design-nerd","Design nerd"),
        ("quiet-luxury","Quiet luxury"),("loud-on-purpose","Loud on purpose"),
        ("dad-golf","Dad golf"),("gorpcore","Gorpcore"),
        ("post-round-friendly","Post-round friendly"),("made-by-hand","Made by hand")]
TAGS += [("collab-machine","Collab machine"),("course-merch","Course merch"),
         ("member-guest","Member-guest"),("range-rat","Range rat")]
TAGL = dict(TAGS)

# Attributes are facts, not judgements — separate row, separate pill group.
ATTRS = [("women-founded","Women-founded"),("tour-proven","Tour-proven"),
         ("heritage","Heritage"),("drops-and-vanishes","Drops and vanishes"),
         ("new-to-index","New to the index")]
ATTRL = dict(ATTRS)
import datetime as _dt
UPD = _dt.date.today().strftime("%-d %b %Y")  # auto-stamp, was hardcoded to 25 Aug 2026

cards = []
missing_img = []
# Resolve every brand up front so collisions can be detected BEFORE the page is
# written. A shared image is the failure mode Lenny actually sees on /brands/;
# it never trips `missing_img`, because the shared file exists and loads fine.
RESOLVED = {b["slug"]: resolve_frames(b) for b in BRANDS}


def gallery_frames(b):
    """The card's slides, in precedence order — with brand-gallery.json policed.

    brand-gallery.json is written by the image ranker (see the taste-tags memo).
    Two defects in it were shipping duplicate-looking cards:

      * rosemark-grips was assigned THREE frames belonging to other brands —
        /images/cloud-and-wind/classic-collection.jpg, the texas-brands hero and
        the custom-wedges hero — with its own grip photo demoted to slide 4. The
        ranker falls back to "any high-scoring lifestyle frame on the site" when
        a brand has too few of its own, which quietly borrows someone else's.
      * puma-golf and realtree got byte-identical six-frame lists, because they
        share one collab post and the ranker scores per POST, not per brand.

    So: an explicit "img" in brands.json is now the highest authority (it is a
    human decision), and ranked frames are kept only when they live in a
    directory this brand actually resolves into.
    """
    slug, own = b["slug"], RESOLVED.get(b["slug"]) or []
    ranked = (GAL.get(slug, {}) or {}).get("frames") or []
    # keep only ranked frames from a directory this brand actually resolves into
    ok_dirs = {os.path.dirname(f) for f in own} | (
        {os.path.dirname(b["img"])} if b.get("img") else set())
    ranked = [f for f in ranked if os.path.dirname("/" + f.lstrip("/")) in ok_dirs]
    # An explicit "img" pins the LEAD only. An earlier cut returned [img] + own and
    # dropped `ranked` entirely, which silently collapsed the swipeable gallery to
    # one slide on every brand we pinned — the cure being worse than the disease.
    lead = [b["img"]] if (b.get("img") and os.path.exists(ROOT + b["img"])) else []
    seen, out = set(), []
    for f in lead + ranked + own:
        f = "/" + f.lstrip("/")
        if f not in seen:
            seen.add(f); out.append(f)
    return out[:6]


GALLERIES = {b["slug"]: gallery_frames(b) for b in BRANDS}
_lead = {}
for _s, _f in GALLERIES.items():
    if _f:
        _lead.setdefault(_f[0], []).append(_s)
DUPES = {k: v for k, v in _lead.items() if len(v) > 1}

for b in sorted(BRANDS, key=lambda x: x["name"].lower()):
    img = resolve_img(b)
    if not img: missing_img.append(b["slug"])
    tags = " ".join(b["regions"] + b["cats"] + b.get("tags", []) + b.get("attrs", []))
    chip = REGL.get(b["regions"][-1] if "texas" in b["regions"] else b["regions"][0], "")
    loc = H.escape(b["loc"]) if b["loc"] != "—" else ""
    cats_txt = " &middot; ".join(CATL[c] for c in b["cats"])
    frames = GALLERIES[b["slug"]]
    if frames:
        slides = "".join(
            f'<div class="bi-slide"><img src="{f}" loading="lazy" '
            f'alt="{H.escape(b["name"])} &mdash; {i+1} of {len(frames)}"></div>'
            for i, f in enumerate(frames))
        imgtag = f'<div class="bi-gal" tabindex="0">{slides}</div>'
    else:
        imgtag = '<div class="bi-noimg"></div>'
    men = MENTIONS.get(b["slug"], [])
    bp = f'/brands/{b["slug"]}'
    cov = (f'<a class="bi-covlink" href="{bp}">All coverage &middot; {len(men)} post{"s" if len(men)!=1 else ""} &rarr;</a>'
           if men else "")
    chips = "".join(f'<a class="bi-tag" href="/brands/tag/{t}">{TAGL[t]}</a>'
                    for t in b.get("tags", []) if t in TAGL)
    chips = f'<div class="bi-tags">{chips}</div>' if chips else ""
    ats = "".join(f'<a class="bi-attr" href="/brands/attr/{a}">{ATTRL[a]}</a>'
                  for a in b.get("attrs", []) if a in ATTRL)
    chips += f'<div class="bi-attrs">{ats}</div>' if ats else ""
    cards.append(f'''  <div class="bi-card" data-tags="{tags}">
    <div class="bi-img">{imgtag}</div>
    <div class="bi-body">
      <a class="bi-namelink" href="{bp if men else b["url"]}"><span class="bi-name">{H.escape(b["name"])}</span></a>
      <div class="bi-meta">{loc}{" &middot; " if loc else ""}{cats_txt}</div>
      {chips}
      <p class="bi-line">{b["line"]}</p>
      <a class="bi-more" href="{b["url"]}">Read the profile &rarr;</a>
      {cov}
    </div>
  </div>''')

pills = ['<button class="bi-pill on" data-f="all">All</button>']
pills += [f'<button class="bi-pill bi-pill-taste" data-f="{k}">{v}</button>' for k, v in TAGS]
pills += [f'<button class="bi-pill bi-pill-attr" data-f="{k}">{v}</button>' for k, v in ATTRS]
pills += [f'<button class="bi-pill" data-f="{k}">{v}</button>' for k, v in CATS if k != "community"]
pills += [f'<button class="bi-pill" data-f="{k}">{v}</button>' for k, v in REGIONS if k != "world"]

itemlist = json.dumps({"@context":"https://schema.org","@type":"CollectionPage",
  "name":"Independent Golf Brands to Know — The Brand Index",
  "description":"A running index of independent golf brands — apparel, clubs, bags, headcovers and accessories — researched and curated by The Grassy Issue in Austin, Texas.",
  "url":"https://thegrassyissue.com/brands/",
  "mainEntity":{"@type":"ItemList","numberOfItems":len(BRANDS),
    "itemListElement":[{"@type":"ListItem","position":i+1,"name":b["name"],
      "url":"https://thegrassyissue.com"+b["url"]}
      for i,b in enumerate(sorted(BRANDS,key=lambda x:x["name"].lower()))]}}, ensure_ascii=False)

# lift the shared nav/head bits from index.html so fonts + search match the site
site = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
fonts = "\n".join(re.findall(r'<link[^>]*(?:fonts|preconnect)[^>]*>', site))
margins = re.search(r'@font-face\s*\{[^}]*In The Margins[^}]*\}', site)
margins_css = margins.group(0) if margins else ""

N = len(BRANDS)
page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Independent Golf Brands to Know — The Brand Index | The Grassy Issue</title>
<meta name="description" content="A running index of {N} independent golf brands — apparel, clubs, bags, headcovers and accessories from Texas, Australia, Japan and beyond. Researched and curated from Austin.">
<link rel="canonical" href="https://thegrassyissue.com/brands/">
<meta property="og:title" content="Independent Golf Brands to Know — The Brand Index">
<meta property="og:description" content="A running index of {N} independent golf brands, researched and curated by The Grassy Issue.">
<meta property="og:url" content="https://thegrassyissue.com/brands/">
<meta property="og:type" content="website">
{fonts}
<script type="application/ld+json">{itemlist}</script>
<style>
{margins_css}
@font-face{{font-family:'Editors Note Text';src:url('/assets/fonts/editors-note-text-regular.woff2') format('woff2'),url('/assets/fonts/editors-note-text-regular.woff') format('woff');font-weight:400;font-style:normal;font-display:swap}}@font-face{{font-family:'Editors Note Text';src:url('/assets/fonts/editors-note-text-italic.woff2') format('woff2'),url('/assets/fonts/editors-note-text-italic.woff') format('woff');font-weight:400;font-style:italic;font-display:swap}}@font-face{{font-family:'Editors Note Text';src:url('/assets/fonts/editors-note-text-bold.woff2') format('woff2'),url('/assets/fonts/editors-note-text-bold.woff') format('woff');font-weight:700;font-style:normal;font-display:swap}}@font-face{{font-family:'Editors Note Text';src:url('/assets/fonts/editors-note-text-bolditalic.woff2') format('woff2'),url('/assets/fonts/editors-note-text-bolditalic.woff') format('woff');font-weight:700;font-style:italic;font-display:swap}}:root{{--ink:#141414;--paper:#F4F1EA;--grass:#2D4A2B;--rough:#A8A878;--flag:#C7362C;
--serif:'Editors Note Text',Georgia,serif;--display:'In The Margins','Editors Note Text',Georgia,serif;
--sans:'Inter',-apple-system,sans-serif;--mono:'JetBrains Mono',monospace;}}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:var(--paper);color:var(--ink);font-family:var(--sans);}}
.nav{{border-bottom:1px solid rgba(20,20,20,.15);background:var(--paper);position:sticky;top:0;z-index:50;}}
.nav-inner{{max-width:1200px;margin:0 auto;display:flex;align-items:center;gap:28px;padding:14px 24px;}}
.nav-wordmark{{font-family:var(--display);font-size:22px;color:var(--ink);text-decoration:none;letter-spacing:.01em;}}
.nav-links{{display:flex;gap:20px;}}
.nav-links a{{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink);text-decoration:none;opacity:.75;}}
.nav-links a.active{{opacity:1;border-bottom:2px solid var(--grass);padding-bottom:2px;}}
.nav-cta{{margin-left:auto;font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink);text-decoration:none;border:1px solid var(--ink);padding:7px 12px;border-radius:2px;}}
.bi-hero{{position:relative;height:30vh;min-height:240px;max-height:340px;overflow:hidden;background:var(--ink);}}
.bi-hero img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 70%;}}
.bi-hero img.mobile{{display:none;}}
.bi-hero::after{{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,20,20,.15) 0%,rgba(20,20,20,0) 30%,rgba(20,20,20,0) 55%,rgba(20,20,20,.55) 100%);pointer-events:none;}}
.bi-hero-content{{position:absolute;inset:0;z-index:2;max-width:1200px;margin:0 auto;padding:22px 24px;display:flex;flex-direction:column;justify-content:space-between;}}
.bi-hero-stamp{{color:var(--paper);font-family:var(--mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;display:flex;align-items:center;gap:10px;}}
.bi-hero-stamp .pulse{{width:8px;height:8px;border-radius:50%;background:var(--flag);animation:bipulse 1.8s ease-in-out infinite;}}
@keyframes bipulse{{0%,100%{{opacity:1;transform:scale(1);}}50%{{opacity:.4;transform:scale(.85);}}}}
.bi-hero-title{{color:var(--paper);font-family:var(--serif);font-weight:400;font-style:italic;font-size:clamp(28px,3.6vw,46px);line-height:.95;letter-spacing:-.02em;}}
.bi-hero-sub{{color:var(--paper);margin-top:10px;max-width:540px;font-size:13px;line-height:1.5;opacity:.92;}}
@media(max-width:640px){{.bi-hero img.desktop{{display:none;}}.bi-hero img.mobile{{display:block;object-position:center 65%;}}.bi-hero{{height:26vh;min-height:210px;}}}}
.bi-head{{max-width:1200px;margin:0 auto;padding:44px 24px 8px;}}
.bi-kicker{{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--grass);}}
h1{{font-family:var(--serif);font-weight:600;font-size:clamp(34px,5vw,54px);line-height:1.05;letter-spacing:-.01em;margin:14px 0 18px;max-width:20ch;}}
.bi-intro{{font-size:17px;line-height:1.65;color:#42463f;max-width:64ch;}}
.bi-intro em{{font-style:italic;}}
.bi-count{{font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:#6e736c;margin-top:14px;}}
.bi-filters{{max-width:1200px;margin:26px auto 6px;padding:0 24px;display:flex;flex-wrap:wrap;gap:8px;}}
.bi-pill{{font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;
background:transparent;border:1px solid rgba(20,20,20,.35);border-radius:100px;padding:7px 14px;cursor:pointer;color:var(--ink);}}
.bi-pill.on{{background:var(--ink);color:var(--paper);border-color:var(--ink);}}
.bi-grid{{max-width:1200px;margin:22px auto 80px;padding:0 24px;display:grid;grid-template-columns:repeat(auto-fill,minmax(268px,1fr));gap:22px;}}
.bi-card{{background:#fff;border:1px solid rgba(20,20,20,.12);border-radius:8px;overflow:hidden;color:var(--ink);display:flex;flex-direction:column;transition:transform .15s ease, box-shadow .15s ease;}}
.bi-imglink,.bi-namelink{{color:inherit;text-decoration:none;}}
.bi-card:hover{{transform:translateY(-3px);box-shadow:0 10px 28px rgba(20,20,20,.10);}}
.bi-img{{aspect-ratio:4/3;overflow:hidden;background:#eceae2;position:relative;}}
.bi-img img{{width:100%;height:100%;object-fit:cover;display:block;}}
.bi-gal{{display:flex;height:100%;overflow-x:auto;scroll-snap-type:x mandatory;
  scrollbar-width:none;-ms-overflow-style:none;}}
.bi-gal::-webkit-scrollbar{{display:none;}}
.bi-slide{{flex:0 0 100%;scroll-snap-align:start;height:100%;}}
.bi-slide img{{width:100%;height:100%;object-fit:cover;display:block;}}
.bi-gal:focus-visible{{outline:2px solid var(--grass);outline-offset:-2px;}}
.bi-tags{{display:flex;flex-wrap:wrap;gap:5px;margin:0 0 8px;}}
.bi-tag{{font-family:var(--mono);font-size:9.5px;letter-spacing:.07em;text-transform:uppercase;
  border:1px solid rgba(61,107,53,.35);color:#3d6b35;background:rgba(61,107,53,.06);
  padding:3px 7px;border-radius:3px;text-decoration:none;white-space:nowrap;}}
.bi-tag:hover{{background:#3d6b35;color:#fff;border-color:#3d6b35;}}
.bi-attrs{{display:flex;flex-wrap:wrap;gap:5px;margin:0 0 8px;}}
.bi-attr{{font-family:var(--mono);font-size:9.5px;letter-spacing:.07em;text-transform:uppercase;
  border:1px solid rgba(20,20,20,.22);color:#4a4a44;background:transparent;
  padding:3px 7px;border-radius:3px;text-decoration:none;white-space:nowrap;}}
.bi-attr:hover{{background:var(--ink);color:var(--paper);border-color:var(--ink);}}
.bi-pill-attr{{border-style:dashed;}}
.bi-pill-attr.on{{background:var(--ink);color:var(--paper);border-style:solid;}}
.bi-pill-taste{{border-color:rgba(61,107,53,.45);color:#3d6b35;}}
.bi-pill-taste.on{{background:#3d6b35;border-color:#3d6b35;color:#fff;}}
.bi-noimg{{width:100%;height:100%;background:repeating-linear-gradient(45deg,#eceae2,#eceae2 10px,#e4e1d7 10px,#e4e1d7 20px);}}
.bi-body{{padding:16px 16px 18px;display:flex;flex-direction:column;gap:7px;flex:1;}}
.bi-name{{font-family:var(--serif);font-weight:600;font-size:19px;letter-spacing:-.01em;}}
.bi-meta{{font-family:var(--mono);font-size:10px;letter-spacing:.06em;text-transform:uppercase;color:var(--grass);}}
.bi-line{{font-size:13.5px;line-height:1.55;color:#4a4f48;flex:1;}}
.bi-more{{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;border-bottom:1px solid var(--ink);align-self:flex-start;padding-bottom:2px;color:inherit;text-decoration:none;}}
.bi-covlink{{margin-top:10px;border-top:1px solid rgba(20,20,20,.1);padding-top:9px;font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;color:var(--grass);text-decoration:none;}}
.bi-covlink:hover{{color:var(--ink);}}
.bi-zero{{display:none;max-width:1200px;margin:30px auto;padding:0 24px;font-family:var(--mono);font-size:12px;color:#6e736c;}}
footer{{border-top:1px solid rgba(20,20,20,.15);padding:26px 24px 60px;max-width:1200px;margin:0 auto;font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:#6e736c;}}
@media(max-width:640px){{.nav-links{{gap:12px;}}.nav-links a{{font-size:9.5px;}}.nav-cta{{display:none;}}}}
</style>
{GA}
{GC}
</head>
<body>
<nav class="nav" role="navigation" aria-label="Main navigation">
  <div class="nav-inner">
    <a href="/" class="nav-wordmark">The Grassy Issue</a>
    <div class="nav-links">
      <a href="/#feed">The Feed</a>
      <a href="/brands/" class="active">Brands</a>
      <a href="/field-guide/">Field Guide</a>
      <a href="/events/">Events</a>
    </div>
  </div>
</nav>

<div class="bi-hero">
  <img src="/images/hero-wide.jpg" alt="Sunset over the green and flag at Jimmy Clay Golf Course, Austin" class="desktop" loading="eager" />
  <img src="/images/hero.jpg" alt="Sunset over the green and flag at Jimmy Clay Golf Course, Austin" class="mobile" loading="eager" />
  <div class="bi-hero-content">
    <div class="bi-hero-stamp"><span class="pulse"></span><span>The Brand Index &middot; Live from Austin</span></div>
    <div>
      <div class="bi-hero-title">THE GRASSY ISSUE</div>
      <p class="bi-hero-sub">A running index of modern golf culture. Independent brands, gear, courses, people and things worth knowing. Curated from Austin.</p>
    </div>
  </div>
</div>

<header class="bi-head">
  <span class="bi-kicker">[ The Brand Index ]</span>
  <h1>Independent Golf Brands to Know</h1>
  <p class="bi-intro">A running index of independent golf brands &mdash; apparel, clubs, bags,
  headcovers and the occasional oddity &mdash; from Texas to Tasmania to Tokyo. Every brand here
  has been researched, photographed and written up by The Grassy Issue, curated from Austin.
  Each card links to our full coverage. <em>The index grows every week.</em></p>
  <div class="bi-count"><span id="bi-showing">{N}</span> of {N} brands &middot; Updated {UPD}</div>
</header>

<div class="bi-filters" role="tablist" aria-label="Filter brands">
{chr(10).join("  "+p for p in pills)}
</div>

<div class="bi-grid" id="bi-grid">
{chr(10).join(cards)}
</div>
<p class="bi-zero" id="bi-zero">Nothing in that combination yet &mdash; the index grows every week.</p>

<footer>The Grassy Issue &middot; Golf culture, in a running feed &middot; Austin, TX</footer>

<script>
(function(){{
  var pills=document.querySelectorAll('.bi-pill'),cards=document.querySelectorAll('.bi-card');
  var showing=document.getElementById('bi-showing'),zero=document.getElementById('bi-zero');
  pills.forEach(function(p){{p.addEventListener('click',function(){{
    pills.forEach(function(x){{x.classList.remove('on');}});p.classList.add('on');
    var f=p.dataset.f,n=0;
    cards.forEach(function(c){{
      var show=f==='all'||(' '+c.dataset.tags+' ').indexOf(' '+f+' ')>=0;
      c.style.display=show?'':'none';if(show)n++;}});
    showing.textContent=n;zero.style.display=n?'none':'block';
  }});}});
}})();
</script>
</body>
</html>'''

os.makedirs(os.path.join(ROOT, "brands"), exist_ok=True)
open(os.path.join(ROOT, "brands", "index.html"), "w", encoding="utf-8").write(page)
print(f"wrote brands/index.html — {N} brands, {len(page)} bytes")
if missing_img: print("no image resolved for:", missing_img)
if DUPES:
    print("\n!! DUPLICATE card images — these brands share a lead frame:")
    for k, v in DUPES.items():
        print(f"   {k}\n       " + ", ".join(v))
    print("   Fix by adding an anchor to the brand's url in data/brands.json, or an\n"
          "   explicit \"img\", so resolve_frames() can tell them apart.\n")

# ------------------------------------------------- per-brand coverage pages
THUMBS = json.load(open(os.path.join(ROOT, "data", "post-thumbs.json")))

def brand_page(b):
    slug = b["slug"]; name = H.escape(b["name"])
    men = MENTIONS.get(slug, [])
    men = sorted(men, key=lambda e: not e.get("profile"))
    loc = H.escape(b["loc"]) if b["loc"] != "—" else ""
    cats_txt = " &middot; ".join(CATL[c] for c in b["cats"])
    img = resolve_img(b)
    tiles = []
    for e in men:
        t = THUMBS.get(e["url"], {})
        ti = t.get("img")
        cat = H.escape(t.get("cat", "Drops & Brands"))
        badge = '<span class="bp-badge">The Profile</span>' if e.get("profile") else ""
        thumb = (f'<div class="bp-thumb"><img src="{ti}" loading="lazy" alt="{H.escape(e["title"])}">{badge}</div>'
                 if ti else f'<div class="bp-thumb bp-nothumb">{badge}</div>')
        tiles.append(f'''  <a class="bp-card" href="{e["url"]}">
    {thumb}
    <div class="bp-body">
      <div class="bp-kicker">{cat}</div>
      <div class="bp-title">{H.escape(e["title"])}</div>
    </div>
  </a>''')
    ld = json.dumps({"@context":"https://schema.org","@type":"CollectionPage",
      "name":f"{b['name']} — All Grassy Issue Coverage",
      "url":f"https://thegrassyissue.com/brands/{slug}",
      "mainEntity":{"@type":"ItemList","numberOfItems":len(men),
        "itemListElement":[{"@type":"ListItem","position":i+1,"name":e["title"],
          "url":"https://thegrassyissue.com"+e["url"]} for i,e in enumerate(men)]}}, ensure_ascii=False)
    heroimg = f'<img src="{img}" alt="{name} — independent golf brand" loading="eager">' if img else ''
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{b["name"]} &mdash; All Coverage | The Grassy Issue</title>
<meta name="description" content="Every Grassy Issue post featuring {b["name"]} — {len(men)} article{"s" if len(men)!=1 else ""}, from the full profile to every edit and roundup that includes the brand.">
<link rel="canonical" href="https://thegrassyissue.com/brands/{slug}">
<meta property="og:title" content="{b["name"]} — All Grassy Issue Coverage">
<meta property="og:url" content="https://thegrassyissue.com/brands/{slug}">
<meta property="og:type" content="website">
{fonts}
<script type="application/ld+json">{ld}</script>
<style>
{margins_css}
@font-face{{font-family:'Editors Note Text';src:url('/assets/fonts/editors-note-text-regular.woff2') format('woff2'),url('/assets/fonts/editors-note-text-regular.woff') format('woff');font-weight:400;font-style:normal;font-display:swap}}@font-face{{font-family:'Editors Note Text';src:url('/assets/fonts/editors-note-text-italic.woff2') format('woff2'),url('/assets/fonts/editors-note-text-italic.woff') format('woff');font-weight:400;font-style:italic;font-display:swap}}@font-face{{font-family:'Editors Note Text';src:url('/assets/fonts/editors-note-text-bold.woff2') format('woff2'),url('/assets/fonts/editors-note-text-bold.woff') format('woff');font-weight:700;font-style:normal;font-display:swap}}@font-face{{font-family:'Editors Note Text';src:url('/assets/fonts/editors-note-text-bolditalic.woff2') format('woff2'),url('/assets/fonts/editors-note-text-bolditalic.woff') format('woff');font-weight:700;font-style:italic;font-display:swap}}:root{{--ink:#141414;--paper:#F4F1EA;--grass:#2D4A2B;--rough:#A8A878;--flag:#C7362C;
--serif:'Editors Note Text',Georgia,serif;--display:'In The Margins','Editors Note Text',Georgia,serif;
--sans:'Inter',-apple-system,sans-serif;--mono:'JetBrains Mono',monospace;}}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:var(--paper);color:var(--ink);font-family:var(--sans);}}
.nav{{border-bottom:1px solid rgba(20,20,20,.15);background:var(--paper);position:sticky;top:0;z-index:50;}}
.nav-inner{{max-width:1200px;margin:0 auto;display:flex;align-items:center;gap:28px;padding:14px 24px;}}
.nav-wordmark{{font-family:var(--display);font-size:22px;color:var(--ink);text-decoration:none;letter-spacing:.01em;}}
.nav-links{{display:flex;gap:20px;}}
.nav-links a{{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink);text-decoration:none;opacity:.75;}}
.nav-links a.active{{opacity:1;border-bottom:2px solid var(--grass);padding-bottom:2px;}}
.bp-head{{max-width:1200px;margin:0 auto;padding:44px 24px 6px;display:flex;gap:28px;align-items:flex-start;flex-wrap:wrap;}}
.bp-heroimg{{width:190px;aspect-ratio:1/1;overflow:hidden;border:1px solid rgba(20,20,20,.2);background:#eceae2;flex-shrink:0;}}
.bp-heroimg img{{width:100%;height:100%;object-fit:cover;display:block;}}
.bp-headtext{{flex:1;min-width:260px;}}
.bp-crumb{{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;margin-bottom:12px;}}
.bp-crumb a{{color:var(--ink);text-decoration:none;opacity:.7;}}
.bp-crumb span{{opacity:.4;margin:0 6px;}}
.bp-kickline{{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--grass);}}
h1{{font-family:var(--serif);font-weight:600;font-size:clamp(32px,4.6vw,50px);line-height:1.05;letter-spacing:-.01em;margin:10px 0 10px;}}
.bp-meta{{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#6e736c;margin-bottom:12px;}}
.bp-line{{font-size:16px;line-height:1.65;color:#3f443e;max-width:60ch;margin-bottom:16px;}}
.bp-profile{{display:inline-block;font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;border-bottom:1px solid var(--ink);padding-bottom:2px;color:var(--ink);text-decoration:none;}}
.bp-grid{{max-width:1200px;margin:30px auto 80px;padding:0 24px;display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:22px;}}
.bp-card{{background:#fff;border:1px solid rgba(20,20,20,.12);border-radius:8px;overflow:hidden;color:var(--ink);text-decoration:none;display:flex;flex-direction:column;transition:transform .15s ease, box-shadow .15s ease;}}
.bp-card:hover{{transform:translateY(-3px);box-shadow:0 10px 28px rgba(20,20,20,.10);}}
.bp-thumb{{aspect-ratio:16/10;overflow:hidden;background:#eceae2;position:relative;}}
.bp-thumb img{{width:100%;height:100%;object-fit:cover;display:block;transition:transform .3s ease;}}
.bp-card:hover .bp-thumb img{{transform:scale(1.04);}}
.bp-nothumb{{background:repeating-linear-gradient(45deg,#eceae2,#eceae2 10px,#e4e1d7 10px,#e4e1d7 20px);}}
.bp-badge{{position:absolute;top:10px;left:10px;background:var(--grass);color:var(--paper);font-family:var(--mono);font-size:9px;letter-spacing:.12em;text-transform:uppercase;padding:4px 8px;border-radius:2px;}}
.bp-body{{padding:14px 16px 16px;display:flex;flex-direction:column;gap:6px;flex:1;}}
.bp-kicker{{font-family:var(--mono);font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--grass);}}
.bp-title{{font-family:var(--serif);font-weight:600;font-size:16.5px;line-height:1.3;letter-spacing:-.01em;}}
footer{{border-top:1px solid rgba(20,20,20,.15);padding:26px 24px 60px;max-width:1200px;margin:0 auto;font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:#6e736c;}}
@media(max-width:640px){{.nav-links{{gap:12px;}}.nav-links a{{font-size:9.5px;}}.bp-heroimg{{width:120px;}}}}
</style>
</head>
<body>
<nav class="nav" role="navigation" aria-label="Main navigation">
  <div class="nav-inner">
    <a href="/" class="nav-wordmark">The Grassy Issue</a>
    <div class="nav-links">
      <a href="/#feed">The Feed</a>
      <a href="/brands/" class="active">Brands</a>
      <a href="/field-guide/">Field Guide</a>
      <a href="/events/">Events</a>
    </div>
  </div>
</nav>

<header class="bp-head">
  <div class="bp-heroimg">{heroimg}</div>
  <div class="bp-headtext">
    <div class="bp-crumb"><a href="/">Feed</a><span>/</span><a href="/brands/">The Brand Index</a><span>/</span>{name}</div>
    <div class="bp-kickline">[ All Coverage &middot; {len(men)} Post{"s" if len(men)!=1 else ""} ]</div>
    <h1>{name}</h1>
    <div class="bp-meta">{loc}{" &middot; " if loc else ""}{cats_txt}</div>
    <p class="bp-line">{b["line"]}</p>
    <a class="bp-profile" href="{b["url"]}">Read the full profile &rarr;</a>
  </div>
</header>

<div class="bp-grid">
{chr(10).join(tiles)}
</div>

<footer>The Grassy Issue &middot; Golf culture, in a running feed &middot; Austin, TX</footer>
{GA}
{GC}
</body>
</html>'''

npages = 0
for b in BRANDS:
    if not MENTIONS.get(b["slug"]):
        continue
    html_out = brand_page(b)
    open(os.path.join(ROOT, "brands", b["slug"] + ".html"), "w", encoding="utf-8").write(html_out)
    npages += 1
print(f"wrote {npages} per-brand coverage pages in /brands/")

# ------------------------------------------------- taste-tag pages
# One page per tag at /brands/tag/<slug>. These, not the index, are the linkable
# assets — "the eleven brands doing Muni energy" is something people cite; a
# directory is not. Criteria are printed on the page so the tag is checkable.
TAG_COPY = {
 "muni-energy": ("Muni energy",
   "Gear made for public golf &mdash; unpretentious, priced so a weekly player can buy it, and often tied to a specific course or local cause.",
   "Core apparel under about $120, or an explicit public-course or community affiliation. No country-club signalling."),
 "design-nerd": ("Design nerd",
   "Brands where the reason to buy is a design decision rather than a logo, and which will tell you what that decision was.",
   "The brand explains construction or design rationale on its own product pages, and the work reads as considered to someone outside golf."),
 "quiet-luxury": ("Quiet luxury",
   "Expensive and undecorated. The money goes into the material, not the branding.",
   "Core piece above about $150, branding limited to a woven label or small mark, premium natural or technical materials."),
 "loud-on-purpose": ("Loud on purpose",
   "Print, colour and graphics are the product, not a finish applied to it afterwards.",
   "All-over prints, bold colourways, or graphics as the primary design element across the range rather than on one capsule."),
 "dad-golf": ("Dad golf",
   "Deliberately traditional, and not ironic about it.",
   "References pre-1990 golf clothing &mdash; four-button plackets, pleats, natural fibres, fuller cuts. No athleisure silhouettes."),
 "gorpcore": ("Gorpcore",
   "Outdoor and technical crossover, usually with a real lineage outside golf.",
   "Technical shells, ripstop, utility hardware, or a genuine hiking, climbing or workwear history."),
 "post-round-friendly": ("Post-round friendly",
   "Reads as normal clothes the moment you leave the course.",
   "No visible golf branding on the core range, and silhouettes that work in a bar without explanation."),
 "collab-machine": ("Collab machine",
   "Brands whose identity is built on who they work with rather than on their own line.",
   "Collaborations make up a substantial share of the catalogue, or the brand is better known for its partnerships than for what it makes alone."),
 "course-merch": ("Course merch",
   "Tied to a specific course or club &mdash; sometimes a real one, sometimes not.",
   "The range references a named course, club or municipal facility, or the brand exists to sell an invented club&rsquo;s merchandise."),
 "member-guest": ("Member-guest",
   "The dressed-up end of the index. What you wear when the round actually matters.",
   "The range is cut for an occasion rather than a practice session &mdash; collared, tailored, coordinated. Distinct from Quiet luxury, which is about restraint and price rather than occasion."),
 "range-rat": ("Range rat",
   "Built for practice and repetition rather than for the photograph.",
   "Hard-wearing, technical or deliberately cheap, and sold on durability or function rather than on how it looks in a lookbook."),
 "made-by-hand": ("Made by hand",
   "Small-batch or hand-finished by a named person.",
   "Hand-cut, hand-sewn, hand-knit, hand-stamped or made to order, by a maker the brand will name."),
}

EMDASH = "\u2014"


def tag_page(tag, label, blurb, criteria, key="tags", base="tag"):
    """Clone a generated brand page and swap its body — reuses the real head,
    nav, CSS and footer rather than duplicating them here."""
    tpl_brand = next(b for b in BRANDS if MENTIONS.get(b["slug"]))
    tpl = brand_page(tpl_brand)

    members = [b for b in sorted(BRANDS, key=lambda x: x["name"].lower()) if tag in b.get(key, [])]
    tiles = []
    for b in members:
        frames = (GAL.get(b["slug"], {}) or {}).get("frames") or []
        f = "/" + frames[0].lstrip("/") if frames else (resolve_img(b) or "")
        men = MENTIONS.get(b["slug"], [])
        href = f'/brands/{b["slug"]}' if men else b["url"]
        thumb = (f'<div class="bp-thumb"><img src="{f}" loading="lazy" alt="{H.escape(b["name"])}"></div>'
                 if f else '<div class="bp-thumb bp-nothumb"></div>')
        others = "".join(f'<a class="bi-tag" href="/brands/tag/{t}">{TAGL[t]}</a>'
                         for t in b.get("tags", []) if t != tag and t in TAGL)
        locx = H.escape(b["loc"]) if b["loc"] != EMDASH else ""
        tagbar = '<div class="bi-tags">' + others + '</div>' if others else ""
        tiles.append(
            '  <a class="bp-card" href="' + href + '">\n    ' + thumb +
            '\n    <div class="bp-body">\n      <div class="bp-cat">' + locx +
            '</div>\n      <div class="bp-title">' + H.escape(b["name"]) +
            '</div>\n      <p class="bp-line">' + b["line"] + '</p>\n      ' +
            tagbar + '\n    </div>\n  </a>')

    desc = re.sub(r"&[a-z]+;", " ", blurb)
    ld = json.dumps({"@context":"https://schema.org","@type":"CollectionPage",
      "name": f"{label} \u2014 golf brands | The Grassy Issue", "description": desc,
      "url": f"https://thegrassyissue.com/brands/{base}/{tag}",
      "mainEntity":{"@type":"ItemList","numberOfItems":len(members),
        "itemListElement":[{"@type":"ListItem","position":i+1,"name":b["name"],
          "url":"https://thegrassyissue.com"+b["url"]} for i,b in enumerate(members)]}},
      ensure_ascii=False)

    out = tpl
    out = re.sub(r"<title>.*?</title>", f"<title>{label} &mdash; Golf Brands | The Grassy Issue</title>", out, 1, re.S)
    out = re.sub(r'<meta name="description" content=".*?">',
                 f'<meta name="description" content="{desc} {len(members)} independent golf brands tagged {label}.">', out, 1, re.S)
    out = re.sub(r'<link rel="canonical" href=".*?">',
                 f'<link rel="canonical" href="https://thegrassyissue.com/brands/{base}/{tag}">', out, 1, re.S)
    out = re.sub(r'<meta property="og:url" content=".*?">',
                 f'<meta property="og:url" content="https://thegrassyissue.com/brands/{base}/{tag}">', out, 1, re.S)
    out = re.sub(r'<meta property="og:title" content=".*?">',
                 f'<meta property="og:title" content="{label} &mdash; Golf Brands">', out, 1, re.S)
    out = re.sub(r'<script type="application/ld\+json">.*?</script>',
                 f'<script type="application/ld+json">{ld}</script>', out, 1, re.S)
    out = out.replace("</style>", """
.tg-crit{background:rgba(61,107,53,.06);border-left:3px solid #3d6b35;padding:14px 18px;margin:0 0 28px;}
.tg-crit b{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:#3d6b35;display:block;margin-bottom:5px;}
.tg-crit p{margin:0;font-size:14.5px;line-height:1.6;}
.bi-tags{display:flex;flex-wrap:wrap;gap:5px;margin-top:8px;}
.bi-tag{font-family:var(--mono);font-size:9.5px;letter-spacing:.07em;text-transform:uppercase;
  border:1px solid rgba(61,107,53,.35);color:#3d6b35;background:rgba(61,107,53,.06);
  padding:3px 7px;border-radius:3px;text-decoration:none;white-space:nowrap;}
</style>""", 1)

    body = f'''  <div class="bp-crumb"><a href="/">Feed</a> <span>/</span> <a href="/brands/">Brands</a> <span>/</span> {label}</div>
  <header class="bp-head">
    <span class="bp-kicker">[ " + ("Taste tag" if base=="tag" else "Attribute") + " ]</span>
    <h1>{label}</h1>
    <p class="bp-intro">{blurb}</p>
  </header>
  <div class="tg-crit"><b>What earns this tag</b><p>{criteria}</p></div>
  <div class="bp-grid">
{chr(10).join(tiles)}
  </div>
  <p class="bp-foot"><a href="/brands/">&larr; Back to the Brand Index</a></p>
'''
    out = re.sub(r"(<main[^>]*>).*?(</main>)", lambda m: m.group(1) + "\n" + body + m.group(2), out, 1, re.S)
    return out

os.makedirs(os.path.join(ROOT, "brands", "tag"), exist_ok=True)
ntag = 0
for tag, (label, blurb, criteria) in TAG_COPY.items():
    if not any(tag in b.get("tags", []) for b in BRANDS):
        continue
    open(os.path.join(ROOT, "brands", "tag", tag + ".html"), "w", encoding="utf-8").write(
        tag_page(tag, label, blurb, criteria))
    ntag += 1
print(f"wrote {ntag} taste-tag pages in /brands/tag/")

ATTR_COPY = {
 "women-founded": ("Women-founded",
   "Brands founded or co-founded by a woman.",
   "A named woman is credited as founder or co-founder by the brand or by a published source."),
 "tour-proven": ("Tour-proven",
   "Gear with real use in professional competition, not just a sponsorship deal.",
   "A named player used the product in a named event, or the brand publishes a verifiable tour record. Sponsorship alone does not count."),
 "heritage": ("Heritage",
   "Brands that were making this before most of the field existed.",
   "A founding year earlier than 2000, stated by the brand."),
 "drops-and-vanishes": ("Drops and vanishes",
   "Short runs, no reliable restock. Buy it when you see it.",
   "The brand states a limited-run or periodic-release model, or its catalogue is mostly sold out at any given time."),
 "new-to-index": ("New to the index",
   "Brands added to the Brand Index in the last ninety days.",
   "Computed from the date a brand first entered the index, not editorially assigned."),
}

os.makedirs(os.path.join(ROOT, "brands", "attr"), exist_ok=True)
nattr = 0
for a, (label, blurb, criteria) in ATTR_COPY.items():
    if not any(a in b.get("attrs", []) for b in BRANDS):
        continue
    page = tag_page(a, label, blurb, criteria, key="attrs", base="attr")
    open(os.path.join(ROOT, "brands", "attr", a + ".html"), "w", encoding="utf-8").write(page)
    nattr += 1
print(f"wrote {nattr} attribute pages in /brands/attr/")
