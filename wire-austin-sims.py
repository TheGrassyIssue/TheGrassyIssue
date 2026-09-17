#!/usr/bin/env python3
"""Wire the Austin simulator guide: homepage feed card, sitemap, 301 off the old slug.

THE 301 IS THE IMPORTANT PART. /drops/7-indoor-simulators-for-austins-gross-rainy-days
is an indexed live URL that has been carrying two venues that are not open. The new
guide replaces it at a cleaner, keyword-bearing slug, so the old one has to redirect
rather than 404 — same pattern as the Australian post on 2026-09-04 and the Lions Muny
rename. The old file is deleted once the redirect is in, because a file on disk wins
over a vercel.json redirect.

CARD TYPE is data-type="field". Lenny relabelled this a Field Note on 9/16/26, and
the homepage filter chips read that attribute.

FIVE SLIDES, one per image we actually hold, and the captions name the room each frame
shows. No slide may caption a venue the photograph is not of.
"""
import re, json, sys, os

SLUG = "austin-indoor-golf-simulators"
OLD = "7-indoor-simulators-for-austins-gross-rainy-days"
URL = f"/drops/{SLUG}"
OLD_URL = f"/drops/{OLD}"
KEY = "austinsims"
TITLE = "Every Indoor Golf Simulator in Austin, Ranked by What You Actually Want"
PLAIN = "Every Indoor Golf Simulator in Austin, Ranked by What You Actually Want"
IMG = "/images/austin-sims/"
TODAY = "2026-09-16"

SLIDES = [
 ("xgolf-sim", "X-Golf Cedar Park", "Seven bays &middot; $55&ndash;65/hr",
  "Austin has fourteen indoor simulators you can book this week and four of them did not exist eighteen months ago — in Georgetown, Hutto, San Marcos and far southwest Austin, not downtown, which still has none."),
 ("fiber-bay", "Fiber Golf", "TrackMan iO &middot; $70/hr",
  "Two bays on Circle Drive hitting into 40-foot wall-to-wall screens, the largest in the metro. Opened in May, runs 24/7 on a door code, and has no staff at all."),
 ("xgolf-building", "X-Golf Cedar Park", "West Parmer &middot; Opened 8/25",
  "Seven X-Golf sims, a full kitchen and bar, twelve TVs and two party rooms. $55 Monday to Thursday, $65 at weekends, and PXG Master Fitter fittings since it opened."),
 ("fiber-pebble", "Fiber Golf", "500+ courses",
  "The cheapest bay in the metro is Austin Indoor Golf at $25 an hour — one Full Swing bay on a mezzanine inside a pickleball gym. The dearest is Golfinity TrackMan at $100."),
 ("fiber-interior", "The 24/7 Box", "Fiber &middot; Back Nine &middot; Bogey Master",
  "The market has split in two: the staffed room with a kitchen, and the unstaffed box you enter with a texted door code. The second model is the one multiplying."),
]

_ENT = re.compile(r'&[a-z]+;|&#\d+;')
def _alt(b, n):
    return re.sub(r'\s+', ' ', _ENT.sub('', f"{b} {n}")).strip()

CARD = f'''      <div class="card" data-type="field">
    <div class="card-media" style="position:relative;">
      <span class="card-tag grass">[Field Notes]</span>
      <div class="gear-carousel" data-carousel="{KEY}">
        <div class="gear-carousel-track">
''' + "".join(
f'''          <div class="gear-slide">
            <a href="{URL}">
              <img src="{IMG}{s}.jpg" alt="{_alt(b, n)}" loading="lazy" />
              <div class="gear-slide-info"><div class="gear-slide-brand">{b}</div><div class="gear-slide-name">{n}</div></div>
            </a>
          </div>
''' for s, b, n, _ in SLIDES) + f'''        </div>
        <button class="gear-arrow prev" onclick="gearSlide(this, -1)" aria-label="Previous">&#8249;</button>
        <button class="gear-arrow next" onclick="gearSlide(this, 1)" aria-label="Next">&#8250;</button>
      </div>
    </div>
    <div class="card-body">
      <div class="card-title"><a href="{URL}" style="color:inherit;text-decoration:none;border-bottom:none;">{TITLE}</a></div>
      <div class="card-text" data-slidetext="{KEY}">{SLIDES[0][3]}</div>
      <a href="{URL}" class="card-link">Read the field note ↗</a>
    </div>
  </div>
'''

apply_ = "--apply" in sys.argv
notes = []

if CARD.count('onclick="gearSlide(this, -1)"') != 1 or CARD.count('onclick="gearSlide(this, 1)"') != 1:
    raise SystemExit("the new card's gear-arrows are missing their inline onclick")
if CARD.count('class="gear-slide"') != len(SLIDES):
    raise SystemExit("slide count mismatch in the generated card")
for s, _b, _n, _t in SLIDES:
    if not os.path.exists(f"images/austin-sims/{s}.jpg"):
        raise SystemExit(f"slide image missing on disk: {s}.jpg")
if len({s for s, *_ in SLIDES}) != len(SLIDES):
    raise SystemExit("a slide image is used twice")

# ---------------------------------------------------------------- 1. homepage
h = open("index.html", encoding="utf-8").read()
for u in (URL, OLD_URL):
    i = h.find(u)
    while i != -1:
        s = h.rfind('<div class="card"', 0, i)
        if s == -1:
            break
        depth, j, end = 0, s, None
        while j < len(h):
            m = re.compile(r'<div\b|</div>').search(h, j)
            if not m:
                break
            if m.group(0).startswith("<div"):
                depth += 1
            else:
                depth -= 1
                if depth == 0:
                    end = m.end(); break
            j = m.end()
        if end and u in h[s:end]:
            h = h[:s] + h[end:]
            notes.append(f"removed existing card for {u}")
        else:
            break
        i = h.find(u)

m = re.search(r'\n\s*<div class="card" data-type="', h)
if not m:
    raise SystemExit("could not locate the feed card list")
h = h[:m.start()] + "\n" + CARD + h[m.start():]

anchor = "  window._slideTexts = {\n"
if h.find(anchor) == -1:
    raise SystemExit("canonical window._slideTexts map not found")
h = re.sub(r'\n?    "' + KEY + r'": \[(?:.*?\n)*?    \],', "", h)
k = h.find(anchor)
def plain(t):
    for a, b in [("&mdash;", "—"), ("&middot;", "·"), ("&times;", "×"),
                 ("&rsquo;", "'"), ("&amp;", "&"), ("&ndash;", "–")]:
        t = t.replace(a, b)
    return t
entry = f'    "{KEY}": [\n' + ",\n".join(
    "      " + json.dumps(plain(t), ensure_ascii=False) for _, _, _, t in SLIDES) + "\n    ],\n"
h = h[:k + len(anchor)] + entry + h[k + len(anchor):]
notes.append(f"card inserted with {len(SLIDES)} slides + captions")

# --------------------------------------------------------------------- 2. 301
vj = json.load(open("vercel.json"))
if not any(r.get("source") == OLD_URL for r in vj.get("redirects", [])):
    vj.setdefault("redirects", []).append(
        {"source": OLD_URL, "destination": URL, "permanent": True})
    notes.append(f"301 added: {OLD_URL} -> {URL}")
else:
    notes.append("301 already present")

# ----------------------------------------------------------------- 3. sitemap
sm = open("sitemap.xml", encoding="utf-8").read()
loc = f"https://thegrassyissue.com{URL}"
old_loc = f"https://thegrassyissue.com{OLD_URL}"
sm = re.sub(r'<url>\s*<loc>' + re.escape(old_loc) + r'</loc>.*?</url>\s*', '', sm, flags=re.S)
if loc not in sm:
    sm = sm.replace("</urlset>", f'<url><loc>{loc}</loc><lastmod>{TODAY}</lastmod>'
                    f'<changefreq>monthly</changefreq><priority>0.8</priority></url>\n</urlset>')
    notes.append("sitemap: new row added, old row removed")
else:
    sm = re.sub(r'(<loc>' + re.escape(loc) + r'</loc>\s*<lastmod>)[0-9-]+(</lastmod>)',
                lambda m: m.group(1) + TODAY + m.group(2), sm)
    notes.append("sitemap: lastmod bumped, old row removed")

# ----------------------------------------- 4. internal links to the old slug
stale = []
for p in (__import__("glob").glob("*.html") + __import__("glob").glob("drops/*.html")
          + __import__("glob").glob("field-guide/*.html")):
    if p.startswith("_tmp_") or p == f"drops/{OLD}.html":
        continue
    try:
        t = open(p, encoding="utf-8").read()
    except OSError:
        continue
    if OLD_URL in t:
        stale.append(p)
and_rewrote = []
if stale:
    # The 301 would cover these, but an internal link should never need a redirect
    # hop: it costs crawl budget and dilutes the signal. Rewrite them in place.
    for p in stale:
        if p == "index.html":
            # index.html is written from `h` further down, which would clobber a
            # write here. Patch the in-memory copy instead.
            n = h.count(OLD_URL)
            h = h.replace(OLD_URL, URL)
            and_rewrote.append(f"index.html ({n}, in-memory)")
            continue
        t = open(p, encoding="utf-8").read()
        n = t.count(OLD_URL)
        t = t.replace(OLD_URL, URL)
        if apply_:
            open(p, "w", encoding="utf-8").write(t)
        and_rewrote.append(f"{p} ({n})")
    notes.append(f"internal links repointed at the new slug on {len(and_rewrote)} page(s): "
                 + ", ".join(and_rewrote))

if apply_:
    open("index.html", "w", encoding="utf-8").write(h)
    json.dump(vj, open("vercel.json", "w"), indent=1, ensure_ascii=False)
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    # A file on disk beats a vercel.json redirect, so the old page has to go.
    if os.path.exists(f"drops/{OLD}.html"):
        os.remove(f"drops/{OLD}.html")
        notes.append(f"removed drops/{OLD}.html — the 301 now covers it")
    print(f"wired {URL} | card + {len(SLIDES)} captions | 301 from {OLD_URL}")
else:
    print("DRY RUN — pass --apply")
for n in notes:
    print("  ·", n)
