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
BRANDS = json.load(open(os.path.join(ROOT, "data", "brands.json")))
MENTIONS = json.load(open(os.path.join(ROOT, "data", "brand-mentions.json")))

# ---------------------------------------------------------------- card images
def resolve_img(b):
    if b.get("img") and os.path.exists(ROOT + b["img"]):
        return b["img"]
    url = b["url"]
    if "#" in url:                                  # anchor brands -> lead frame
        frag = url.split("#")[1]
        for d in ["texas-brands", "aussie", "left-of-field", "midiron", "walker-blooming-grounds"]:
            base = {"lof": "xelements-polo-0-0", "midiron": "detour-stripe-polo-5",
                    "walker": "blooming-grounds-knit-polo-1-0"}.get(frag, frag + "-0")
            # sierra madre lead frame is -2 after the tennis cut; try -0.. -2
            for cand in [base, frag + "-2", frag + "-1"]:
                p = f"/images/{d}/{cand}.jpg"
                if os.path.exists(ROOT + p):
                    return p
    page = ROOT + url.split("#")[0] + ".html"       # page brands -> page hero
    if os.path.exists(page):
        h = open(page, encoding="utf-8").read()
        m = re.search(r'<div class="drop-hero-img">\s*<img src="([^"]+)"', h)
        if m and os.path.exists(ROOT + m.group(1)):
            return m.group(1)
    return None

CATS = [("apparel","Apparel"),("equipment","Clubs"),("bags","Bags"),
        ("headcovers","Headcovers"),("headwear","Headwear"),("accessories","Accessories"),
        ("grips","Grips"),("art","Art"),("community","Community")]
REGIONS = [("usa","USA"),("texas","Texas"),("australia","Australia"),
           ("japan","Japan"),("europe","Europe"),("world","Elsewhere")]
CATL = dict(CATS); REGL = dict(REGIONS)

cards = []
missing_img = []
for b in sorted(BRANDS, key=lambda x: x["name"].lower()):
    img = resolve_img(b)
    if not img: missing_img.append(b["slug"])
    tags = " ".join(b["regions"] + b["cats"])
    chip = REGL.get(b["regions"][-1] if "texas" in b["regions"] else b["regions"][0], "")
    loc = H.escape(b["loc"]) if b["loc"] != "—" else ""
    cats_txt = " &middot; ".join(CATL[c] for c in b["cats"])
    imgtag = (f'<img src="{img}" loading="lazy" alt="{H.escape(b["name"])} — independent golf brand">'
              if img else '<div class="bi-noimg"></div>')
    men = MENTIONS.get(b["slug"], [])
    bp = f'/brands/{b["slug"]}'
    cov = (f'<a class="bi-covlink" href="{bp}">All coverage &middot; {len(men)} post{"s" if len(men)!=1 else ""} &rarr;</a>'
           if men else "")
    cards.append(f'''  <div class="bi-card" data-tags="{tags}">
    <a class="bi-imglink" href="{bp if men else b["url"]}"><div class="bi-img">{imgtag}</div></a>
    <div class="bi-body">
      <a class="bi-namelink" href="{bp if men else b["url"]}"><span class="bi-name">{H.escape(b["name"])}</span></a>
      <div class="bi-meta">{loc}{" &middot; " if loc else ""}{cats_txt}</div>
      <p class="bi-line">{b["line"]}</p>
      <a class="bi-more" href="{b["url"]}">Read the profile &rarr;</a>
      {cov}
    </div>
  </div>''')

pills = ['<button class="bi-pill on" data-f="all">All</button>']
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
:root{{--ink:#141414;--paper:#F4F1EA;--grass:#2D4A2B;--rough:#A8A878;--flag:#C7362C;
--serif:'Fraunces',Georgia,serif;--display:'In The Margins','Fraunces',Georgia,serif;
--sans:'Inter',-apple-system,sans-serif;--mono:'JetBrains Mono',monospace;}}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:var(--paper);color:var(--ink);font-family:var(--sans);}}
.nav{{border-bottom:1px solid rgba(20,20,20,.15);background:var(--paper);position:sticky;top:0;z-index:50;}}
.nav-inner{{max-width:1200px;margin:0 auto;display:flex;align-items:center;gap:28px;padding:14px 24px;}}
.nav-wordmark{{font-family:var(--display);font-size:22px;color:var(--ink);text-decoration:none;letter-spacing:.01em;}}
.nav-links{{display:flex;gap:20px;}}
.nav-links a{{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink);text-decoration:none;opacity:.75;}}
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
.bi-img{{aspect-ratio:4/3;overflow:hidden;background:#eceae2;}}
.bi-img img{{width:100%;height:100%;object-fit:cover;display:block;}}
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
  <div class="bi-count"><span id="bi-showing">{N}</span> of {N} brands &middot; Updated 25 Aug 2026</div>
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

# ------------------------------------------------- per-brand coverage pages
THUMBS = json.load(open(os.path.join(ROOT, "data", "post-thumbs.json")))
GC = ('<!-- GoatCounter analytics -->\n<script data-goatcounter="https://thegrassyissue.goatcounter.com/count" '
      'async src="//gc.zgo.at/count.js"></script>')

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
:root{{--ink:#141414;--paper:#F4F1EA;--grass:#2D4A2B;--rough:#A8A878;--flag:#C7362C;
--serif:'Fraunces',Georgia,serif;--display:'In The Margins','Fraunces',Georgia,serif;
--sans:'Inter',-apple-system,sans-serif;--mono:'JetBrains Mono',monospace;}}
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:var(--paper);color:var(--ink);font-family:var(--sans);}}
.nav{{border-bottom:1px solid rgba(20,20,20,.15);background:var(--paper);position:sticky;top:0;z-index:50;}}
.nav-inner{{max-width:1200px;margin:0 auto;display:flex;align-items:center;gap:28px;padding:14px 24px;}}
.nav-wordmark{{font-family:var(--display);font-size:22px;color:var(--ink);text-decoration:none;letter-spacing:.01em;}}
.nav-links{{display:flex;gap:20px;}}
.nav-links a{{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink);text-decoration:none;opacity:.75;}}
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
