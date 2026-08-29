#!/usr/bin/env python3
"""
build-ig.py — regenerate /ig, the private 1080x1080 Instagram tile sheet.

Lenny, 2026-08-28: "a private page that uses the cards formatted for instagram
... the words and first image but in a 1x1 square format."

WHY THIS IS GENERATED AND NOT HAND-BUILT
----------------------------------------
The previous ig.html was hand-assembled and had drifted to 109 tiles while the
feed had grown to 173 linkable posts - 64 posts missing, and no way to notice.
This reads index.html as the single source of truth, so /ig can never fall
behind the feed again. Re-run it after publishing anything.

WHAT LANDS ON A TILE
--------------------
  category chip (top-left)  .card-tag  ->  Drops & Brands / Field Notes / News
  photograph (full bleed)   the card's FIRST image - carousel slide 1
  wordmark                  The Grassy Issue
  headline                  .card-title
  blurb                     .card-text, truncated (see below)

WHAT IS SKIPPED, AND WHY
------------------------
* The 8 quote/vignette cards (style="cursor:default") - no image, no
  destination, nothing to post.
* 2 posts genuinely have no image in their card media: the Lions Muny
  renovation and the Masters ticket lottery. They are REPORTED at the end of
  the run rather than silently dropped, because the fix is to give those cards
  an image, not to pretend they do not exist.

BLURB TRUNCATION
----------------
Card blurbs run 0-755 characters (median 233). Anything past ~170 either
overflows the square or shrinks the type past legibility at thumbnail size, so
blurbs are cut at the last sentence end before the limit, falling back to a word
boundary. Cutting mid-word looks broken on a graphic that goes out as artwork.

PRIVACY
-------
noindex+nofollow, and robots.txt already Disallows /ig. It is unlisted, NOT
secret - anyone with the URL can load it. Do not put anything here that would
matter if a stranger opened it.

EXPORT
------
Tiles render at exactly 1080x1080 CSS pixels, so a 1:1 screenshot is already the
right size. Note that .tile-img is a CSS background, so right-click > "Save image
as" will NOT capture the composed tile - screenshot it, or ask me to batch-render
the ones you want to real PNGs.
"""
import re, sys, html, json, statistics, pathlib
from PIL import Image, ImageStat

ROOT = pathlib.Path(__file__).resolve().parent
LIMIT = 170
MIN_WRITEUP = 60      # below this a text slide reads as blank, so it is skipped
TAGS = {"drop": "Drops &amp; Brands", "field": "Field Notes", "news": "News"}


def clean(frag):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", frag)).strip()


def shorten(t, n=LIMIT):
    """Cut at a sentence end if there is one, else a word boundary. Never mid-word."""
    if len(t) <= n:
        return t
    cut = t[:n]
    for stop in ('. ', '? ', '! ', '— '):
        i = cut.rfind(stop)
        if i > n * 0.55:
            return cut[:i + 1].strip()
    i = cut.rfind(' ')
    return (cut[:i] if i > 0 else cut).rstrip(' ,;:&—-') + '…'


def writeup(href):
    """
    The post's OPENING PARAGRAPH, for the text slide. Read from the dedicated
    page's .writeup-body, not from the feed card - the card blurb is a summary
    (median 233 chars), the write-up is the actual prose (first para median 377,
    max 818). 162 of 172 drop pages have one; the rest fall back to the blurb.

    First paragraph only, deliberately: it is written as the hook so it stands
    alone, whereas paragraph two usually refers back to it and reads oddly out of
    context. Paragraphs under 40 chars are skipped - they are kickers and datelines,
    not prose.
    """
    p = ROOT / href.lstrip('/')
    p = p.with_suffix('.html') if not p.suffix else p
    if not p.exists():
        return ''
    s = p.read_text(encoding='utf-8', errors='replace')
    m = re.search(r'class="writeup-body"[^>]*>(.*?)</div>', s, re.S)
    if not m:
        return ''
    for para in re.findall(r'<p[^>]*>(.*?)</p>', m.group(1), re.S):
        t = clean(para)
        if len(t) > 40:
            return t
    return ''


def packshot_score(path):
    """
    0-100, HIGH = looks like a product shot on white. Same heuristic as the
    homepage packshot audit: flat bright corners +45, low corner noise +25,
    corners agreeing with each other +15, low saturation spread +15.

    Sampled on a 220px thumbnail so scoring ~1,000 images stays quick. Verified
    on a random 120-image sample: 100 lands on product-on-white (Spider putter,
    folded jerseys, polos), 0 lands on lifestyle (a neon sign, a driving range,
    a course at dawn). Roughly 45% of the library scores 100, which is why the
    grid needed sorting rather than just taking the first four images.
    """
    try:
        im = Image.open(path).convert('RGB')
        im.thumbnail((220, 220))
    except Exception:
        return 50                                   # unreadable: treat as neutral
    w, h = im.size
    c = max(8, min(w, h) // 10)
    corners = [im.crop((0, 0, c, c)), im.crop((w - c, 0, w, c)),
               im.crop((0, h - c, c, h)), im.crop((w - c, h - c, w, h))]
    lum, sds = [], []
    for x in corners:
        px = list(x.getdata())
        l = [0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2] for p in px]
        lum.append(statistics.mean(l))
        sds.append(statistics.pstdev(l))
    sat = im.convert('HSV').split()[1]
    s = 0
    if statistics.mean(lum) > 232: s += 45
    if statistics.mean(sds) < 9:   s += 25
    if max(lum) - min(lum) < 14:   s += 15
    if ImageStat.Stat(sat).stddev[0] < 52: s += 15
    return s


_CACHE_PATH = ROOT / "research" / "ig-imagescores.json"
try:
    _CACHE = json.loads(_CACHE_PATH.read_text())
except Exception:
    _CACHE = {}


def rank_images(urls):
    """
    Lifestyle first (Lenny, 2026-08-28: "prioritize pictures that aren't just
    product shots"). Sorts by packshot score ascending, using the original feed
    order to break ties so we do not needlessly scramble a deliberate sequence.
    Scores are cached in research/ (vercelignored) - a cold run scores ~1,000
    images, later runs are instant.
    """
    scored = []
    for i, u in enumerate(urls):
        if u not in _CACHE:
            p = ROOT / u.lstrip('/')
            _CACHE[u] = packshot_score(p) if p.exists() else 50
        scored.append((_CACHE[u], i, u))
    return [u for _, _, u in sorted(scored)]


def type_scale(n):
    """Bigger type for shorter prose. Keeps every text slide filling its square
    without overflowing - the range is 70 to 818 characters."""
    if n <= 330: return 46
    if n <= 470: return 41
    if n <= 620: return 36
    if n <= 780: return 32
    return 28


def scrape(index_html):
    s = index_html.read_text(encoding="utf-8")
    opens = [m.start() for m in re.finditer(r'<div class="card"', s)]
    bounds = opens + [len(s)]
    tiles, noimg = [], []
    for i, a in enumerate(opens):
        seg = s[a:bounds[i + 1]]
        if 'cursor:default' in seg[:200]:          # vignette, nothing to post
            continue
        href = re.search(r'class="card-title"[^>]*>\s*<a href="(/[^"]+)"', seg)
        if not href:
            continue
        title = re.search(r'class="card-title"[^>]*>\s*<a[^>]*>(.*?)</a>', seg, re.S)
        text = re.search(r'class="card-text"[^>]*>(.*?)</(?:div|p)>', seg, re.S)
        media = seg[:seg.find('card-body')] if 'card-body' in seg else seg
        # A FEW images, not one (Lenny, 2026-08-28: "the first few lines and a few
        # images from each post on the box"). 169 of 171 cards carry 4+ carousel
        # images, so four is the grid that nearly always fills; 1 and 3 fall back
        # to their own layouts rather than leaving holes.
        imgs = re.findall(r'<img[^>]+src="([^"]+)"', media)
        if not imgs:
            bg = re.search(r"background-image:url\('([^']+)'\)", media)
            imgs = [bg.group(1)] if bg else []
        img = imgs[0] if imgs else None
        dt = re.search(r'data-type="([^"]+)"', seg[:200])
        blurb = clean(text.group(1)) if text else ''
        # 160 of 171 posts have a real write-up on their page. The other 11 fall
        # back to the card blurb, which is fine at 181-451 chars - but the Summer
        # Practice Guide's blurb is literally "..." (3 chars), and a near-empty
        # paper slide looks broken. MIN_WRITEUP suppresses slide 2 rather than
        # shipping a blank square. That page has no writeup-body markup at all -
        # the real fix is to give it one.
        wu = writeup(href.group(1)) or blurb
        if len(wu) < MIN_WRITEUP:
            wu = ''
        rec = dict(href=href.group(1),
                   tag=TAGS.get(dt.group(1) if dt else '', 'The Grassy Issue'),
                   title=clean(title.group(1)) if title else '',
                   # "first few lines" on the box: the opening of the WRITE-UP,
                   # not the card blurb, cut to ~2 sentences so it sits under a
                   # four-image grid without crowding it.
                   text=shorten(wu, 250) if wu else shorten(blurb, 250),
                   writeup=shorten(wu, 900) if wu else '',
                   # ONE picture, full size (Lenny, 2026-08-28: the 4-up grid
                   # 'still doesn't look right'). rank_images puts the least
                   # packshot-like frame first, so the single image is the most
                   # photographic one the post has.
                   imgs=rank_images(imgs)[:1],
                   img=img)
        (tiles if rec['img'] else noimg).append(rec)
    return tiles, noimg


FACES = "".join(
    f"@font-face{{font-family:'Editors Note Text';"
    f"src:url('/assets/fonts/editors-note-text-{f}.woff2') format('woff2');"
    f"font-weight:{w};font-style:{st};font-display:swap}}"
    for f, w, st in [("regular", 400, "normal"), ("italic", 400, "italic"),
                     ("bold", 700, "normal")])

CSS = FACES + """
/* RESPONSIVE SIZING - why every internal dimension is in em, not px.
   The box must stay a true 1:1 at ANY width so it screenshots square on a
   phone. So the tile carries a base font-size that tracks its own width
   (10px at 1080, scaling down with the viewport), and every size inside is a
   multiple of that base. Change the base and the whole composition scales.
   On a 3x phone a full-width box screenshots at ~1100 device px - already
   Instagram size, no resizing needed.
   NB: em compounds, so spacing on an element that sets its own font-size is
   expressed against THAT size (e.g. .ig-h margin .356em x 45 = 16). */
:root{--paper:#F4F1EA;--ink:#141414;--grass:#2D4A2B;
--serif:'Editors Note Text',Georgia,serif;--mono:'JetBrains Mono',monospace}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#2a2a28;color:var(--paper);font-family:var(--mono);padding:18px 0 60px}
.head{max-width:min(1080px,100vw);margin:0 auto 22px;padding:0 14px}
.head h1{font-family:var(--serif);font-style:italic;font-weight:400;font-size:26px;margin-bottom:6px}
.head p{font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;opacity:.62;line-height:1.7}
.tiles{display:flex;flex-direction:column;align-items:center;gap:34px}
.wrap{width:min(1080px,100vw)}
.cap{display:flex;justify-content:space-between;gap:10px;font-size:9.5px;letter-spacing:.1em;
text-transform:uppercase;opacity:.5;padding:0 12px 6px}
.cap a{color:inherit}
.tile{width:min(1080px,100vw);aspect-ratio:1/1;position:relative;overflow:hidden;background:#111;
font-size:min(10px,0.926vw)}
.tile-split{display:flex;flex-direction:column;background:var(--paper);color:var(--ink)}
.ig-grid{position:relative;flex:1;min-height:0;display:grid;gap:.5em;background:#fff}
.ig-grid.g4{grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr}
.ig-grid.g3{grid-template-columns:1.45fr 1fr;grid-template-rows:1fr 1fr}
.ig-grid.g3 .gi:first-child{grid-row:span 2}
.ig-grid.g2{grid-template-columns:1fr 1fr;grid-template-rows:1fr}
.ig-grid.g1{grid-template-columns:1fr;grid-template-rows:1fr}
.gi{background-size:cover;background-position:center;background-repeat:no-repeat;background-color:#fff}
.ig-lower{flex:0 0 auto;padding:3.8em 5.8em 4.4em;position:relative}
.ig-h{font-family:var(--serif);font-weight:700;font-size:4.5em;line-height:1.08;
letter-spacing:-.015em;margin-bottom:.356em;text-wrap:balance}
.ig-p{font-family:var(--serif);font-size:2.7em;line-height:1.4;opacity:.8}
.ig-logo{font-family:var(--mono);font-size:1.3em;letter-spacing:.24em;text-transform:uppercase;
color:var(--grass);margin-bottom:1.077em}
/* slide 2: the write-up, on TGI paper stock */
.tile-paper{background:var(--paper);color:var(--ink);display:flex;flex-direction:column;
justify-content:center;padding:10.4em 9.2em}
.ts-kicker{font-family:var(--mono);font-size:1.6em;letter-spacing:.18em;text-transform:uppercase;
color:var(--grass)}
.ts-rule{width:7.4em;height:.3em;background:var(--ink);opacity:.8;margin:2.4em 0 3.8em}
.ts-body{font-family:var(--serif);line-height:1.44;letter-spacing:-.005em}
.ts-title{font-family:var(--serif);font-weight:700;font-size:3em;line-height:1.2;
margin-bottom:.667em;opacity:.55}
.ts-foot{position:absolute;left:6.571em;bottom:4.286em;font-family:var(--mono);font-size:1.4em;
letter-spacing:.22em;text-transform:uppercase;opacity:.45}
@media print{body{background:#fff}.head,.cap{display:none}.tiles{gap:0}}
"""


def render(tiles):
    """Two slides per post: (a) the photograph, (b) the write-up on paper.
    Post them together as an Instagram carousel, a before b."""
    out = []
    for n, t in enumerate(tiles, 1):
        cells = "".join(
            f'<div class="gi" '
            f'style="background-image:url(\'{u}\')"></div>' for u in t["imgs"])
        g = f'g{min(len(t["imgs"]), 4)}'
        txt = f'<div class="ig-p">{t["text"]}</div>' if t["text"] else ''
        out.append(f'''  <div class="wrap">
    <div class="cap"><span>{n:03d}a &middot; {t["tag"]} &middot; {len(t["imgs"])} images</span><a href="{t["href"]}" target="_blank">{t["href"]}</a></div>
    <div class="tile tile-split">
      <div class="ig-grid {g}">
        {cells}
      </div>
      <div class="ig-lower">
        <div class="ig-logo">The Grassy Issue</div>
        <div class="ig-h">{t["title"]}</div>
        {txt}
      </div>
    </div>
  </div>''')
        if t["writeup"]:
            out.append(f'''  <div class="wrap">
    <div class="cap"><span>{n:03d}b &middot; write-up &middot; {len(t["writeup"])} chars</span><span>&nbsp;</span></div>
    <div class="tile tile-paper">
      <div class="ts-kicker">{t["tag"]}</div>
      <div class="ts-rule"></div>
      <div class="ts-title">{t["title"]}</div>
      <div class="ts-body" style="font-size:{type_scale(len(t["writeup"]))/10:.1f}em">{t["writeup"]}</div>
      <div class="ts-foot">The Grassy Issue &middot; thegrassyissue.com</div>
    </div>
  </div>''')
    return "\n".join(out)


def main():
    tiles, noimg = scrape(ROOT / "index.html")
    page = f'''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="robots" content="noindex, nofollow" />
<title>TGI &mdash; Instagram Tiles</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<style>{CSS}</style>
</head><body>
<div class="head">
  <h1>Instagram Tiles</h1>
  <p>{len(tiles)} posts {len(tiles)} posts &middot; 1080middot; {sum(1 for t in tiles if t["writeup"])} write-up slides {len(tiles)} posts &middot; 1080middot; 1080 &times; 1080 &middot; newest first<br>
  Private &mdash; noindex, disallowed in robots.txt. Screenshot a tile at 1:1 to get exact pixels.<br>
  Generated by build-ig.py &mdash; re-run after publishing.</p>
</div>
<div class="tiles">
{render(tiles)}
</div>
</body></html>'''
    if "--apply" in sys.argv:
        (ROOT / "ig.html").write_text(page, encoding="utf-8")
    print(f"{'wrote' if '--apply' in sys.argv else 'would write'} ig.html: {len(tiles)} tiles")
    if noimg:
        print(f"  {len(noimg)} post(s) skipped - no image on the feed card:")
        for r in noimg:
            print(f"      · {r['title'][:58]}  ({r['href']})")
    _CACHE_PATH.parent.mkdir(exist_ok=True)
    _CACHE_PATH.write_text(json.dumps(_CACHE, indent=0, sort_keys=True))
    if "--apply" not in sys.argv:
        print("\n(dry run - pass --apply to write)")


if __name__ == "__main__":
    main()
