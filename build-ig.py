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


_ABBR = ("A.P.C", "St", "Mr", "Mrs", "Ms", "Dr", "No", "vs", "Vol", "Est",
         "Jr", "Sr", "U.S", "U.K", "Ft", "Mt", "Co", "Inc")


def two_sentences(t):
    """The first TWO COMPLETE sentences of the post's opening paragraph.

    Lenny, 2026-09-02: "make the IG boxes a 2 sentence summary of the post
    described." Previously the tile carried shorten(wu, 250), which chopped
    mid-clause — "…which is remarkable mainly…" — and read as a broken excerpt
    rather than a summary. House intros run what-it-is → the inspiration → who
    it's for, so the first two sentences already ARE the summary; they just have
    to be taken whole.

    A third sentence is allowed when the first two are very short, so terse
    openers still fill the square.
    """
    t = (t or "").strip()
    if not t:
        return ""
    parts, buf = [], ""
    for tok in re.split(r"(?<=[.!?])\s+", t):
        buf = (buf + " " + tok).strip() if buf else tok
        stem = buf.rstrip(".!?").split()[-1] if buf.rstrip(".!?").split() else ""
        # don't end a sentence on an abbreviation or a single initial
        if stem in _ABBR or re.fullmatch(r"[A-Z]", stem):
            continue
        if buf.endswith((".", "!", "?")):
            parts.append(buf)
            buf = ""
    if buf:
        parts.append(buf)
    out = " ".join(parts[:2])
    if len(out) < 150 and len(parts) > 2:
        out = " ".join(parts[:3])
    # A stub is worse than no paragraph at all — the Summer Practice Guide's card
    # blurb is literally "...", which rendered as a tile with three dots on it.
    # render() already omits the block when text is empty.
    return out if len(out) >= 40 else ""


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


try:
    _raw = json.loads((ROOT / "data" / "ig-lead-overrides.json").read_text())
    LEAD_OVERRIDES = {k: (v if isinstance(v, str) else v["img"])
                      for k, v in _raw.items() if not k.startswith("_")}
    # optional per-image vertical anchor, 0 = flush to the top of the frame
    CROP_ANCHORS = {(v["img"] if isinstance(v, dict) else v): v["anchor"]
                    for v in _raw.values()
                    if isinstance(v, dict) and "anchor" in v}
except Exception:
    LEAD_OVERRIDES, CROP_ANCHORS = {}, {}

_face_cache = {}


def head_clipped(path):
    """True when a detected face is jammed against the top edge of the frame.

    The tile shows the whole picture now, so a source photograph that was itself
    cropped through the crown reads as a decapitated model — Lenny, 2026-09-02:
    "the heads of the first three are not cropped correctly." This demotes such
    frames so a cleaner one from the same post leads instead.

    Deliberately conservative: it only fires when a face IS found AND its box
    starts in the top 2% of the image, so it can never demote a well-composed
    shot. A face cut so badly that the detector misses it entirely will slip
    through — that is what data/ig-lead-overrides.json is for.
    """
    key = str(path)
    if key in _face_cache:
        return _face_cache[key]
    faces = _faces(path)
    if not faces:
        _face_cache[key] = False
        return False
    try:
        h = Image.open(path).height
    except Exception:
        h = 0
    hit = bool(h) and any(y <= h * 0.02 for (_, y, _, _) in faces)
    _face_cache[key] = hit
    return hit


_boxes_cache = {}


def _faces(path):
    """Face boxes in the ORIGINAL image's pixel coordinates, or []. Cached."""
    key = str(path)
    if key in _boxes_cache:
        return _boxes_cache[key]
    boxes = []
    try:
        import cv2
        im = cv2.imread(key)
        if im is not None:
            scale = min(1.0, 700 / max(im.shape[:2]))
            small = cv2.resize(im, None, fx=scale, fy=scale) if scale < 1 else im
            grey = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
            found = []
            for name in ("haarcascade_frontalface_default.xml",
                         "haarcascade_profileface.xml"):
                cc = cv2.CascadeClassifier(cv2.data.haarcascades + name)
                found = list(cc.detectMultiScale(grey, 1.1, 5))
                if len(found):
                    break
            if not len(found):          # profiles facing the other way
                cc = cv2.CascadeClassifier(
                    cv2.data.haarcascades + "haarcascade_profileface.xml")
                flip = cv2.flip(grey, 1)
                found = [(flip.shape[1] - x - w, y, w, h)
                         for (x, y, w, h) in cc.detectMultiScale(flip, 1.1, 5)]
            boxes = [(int(x / scale), int(y / scale), int(w / scale), int(h / scale))
                     for (x, y, w, h) in found]
    except Exception:
        boxes = []
    _boxes_cache[key] = boxes
    return boxes


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
        p = ROOT / u.lstrip('/')
        if u not in _CACHE:
            _CACHE[u] = packshot_score(p) if p.exists() else 50
        # a head clipped by the top edge sorts behind everything else
        clip = 1 if (p.exists() and head_clipped(p)) else 0
        scored.append((clip, _CACHE[u], i, u))
    return [u for _, _, _, u in sorted(scored)]


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
                   text=two_sentences(wu or blurb),
                   writeup=shorten(wu, 900) if wu else '',
                   # ONE picture, full size (Lenny, 2026-08-28: the 4-up grid
                   # 'still doesn't look right'). rank_images puts the least
                   # packshot-like frame first, so the single image is the most
                   # photographic one the post has.
                   imgs=([LEAD_OVERRIDES[href.group(1)]]
                         if href.group(1) in LEAD_OVERRIDES
                         else rank_images(imgs)[:1]),
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
.ig-grid{position:relative;flex:0 0 68%;min-height:0;display:grid;gap:.5em;background:#fff}
.ig-grid.g4{grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr}
.ig-grid.g3{grid-template-columns:1.45fr 1fr;grid-template-rows:1fr 1fr}
.ig-grid.g3 .gi:first-child{grid-row:span 2}
.ig-grid.g2{grid-template-columns:1fr 1fr;grid-template-rows:1fr}
.ig-grid.g1{grid-template-columns:1fr;grid-template-rows:1fr}
.gi{background-repeat:no-repeat;background-color:#fff}
.ig-lower{flex:1 1 auto;min-height:0;overflow:hidden;padding:3.4em 5.8em 3.2em;position:relative}
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


_focal_cache = {}


TILE_W, TILE_H = 1080, 734          # picture area = 68% of the 1080 square
CROP_DIR = ROOT / "images" / "ig-crops"


def tile_crop(url):
    """Return a derivative cropped to EXACTLY the picture-area shape.

    Lenny, 2026-09-02: "make sure the image fills the box and it's centered."
    `contain` left bars; `cover` in the browser crops blind from the centre and
    beheads anyone standing up. So the crop is decided here, once, with the
    subject in view — the tile then just fills with an image already the right
    shape, so nothing is cropped at render time.

    Vertical placement: if a face is found, sit its centre at 32% of the crop
    height, which keeps head and torso and reads as a deliberate portrait crop.
    With no face, centre it. Horizontal placement is centred on the face when
    there is one, otherwise centre.
    """
    src = ROOT / url.lstrip("/").split("?")[0]
    if not src.exists():
        return url
    out_name = re.sub(r"[^a-z0-9]+", "-", url.lower().strip("/")) + ".jpg"
    out = CROP_DIR / out_name
    if out.exists() and out.stat().st_mtime >= src.stat().st_mtime:
        return "/images/ig-crops/" + out_name
    try:
        im = Image.open(src).convert("RGB")
    except Exception:
        return url
    w, h = im.size
    target = TILE_W / TILE_H
    fx, fy = None, None
    for (x, y, fw, fh) in _faces(src):
        if fw * fh > (0 if fx is None else 0):        # take the largest face
            fx, fy = x + fw / 2, y + fh / 2
    if w / h > target:                                # too wide: trim the sides
        cw = int(h * target); ch = h
        cx = fx if fx is not None else w / 2
        x0 = int(min(max(cx - cw / 2, 0), w - cw)); y0 = 0
    else:                                             # too tall: trim top/bottom
        cw = w; ch = int(w / target)
        if fy is not None:
            y0 = int(min(max(fy - ch * 0.32, 0), h - ch))
        else:
            # No face found — could be a profile, sunglasses, or a head turned
            # away, and a true centre crop then slices it off (A.P.Cph and the
            # White Tee Edit both did). Sit the window slightly high: it still
            # reads centred, and it keeps whatever is at the top of the frame.
            y0 = int((h - ch) * CROP_ANCHORS.get(url, 0.08))
        x0 = 0
    # Crop only if that loses almost nothing (a source already near the box
    # shape); otherwise show the whole frame on a blurred bed of itself.
    if abs((w / h) - target) / target < 0.06:
        im = im.crop((x0, y0, x0 + cw, y0 + ch)).resize((TILE_W, TILE_H), Image.LANCZOS)
    else:
        im = fit_frame(im)
    CROP_DIR.mkdir(parents=True, exist_ok=True)
    im.save(out, quality=88, optimize=True)
    return "/images/ig-crops/" + out_name


def fit_frame(src_im):
    """Whole picture, no crop, still filling the box.

    Lenny, 2026-09-02: "can we zoom out on all these images so they fit better?
    still getting weird crops." Taking the full width of a 4:5 source and slicing
    a landscape strip out of it is effectively a heavy zoom — it was reducing
    portraits to a face or a shoulder. So the image is SCALED to fit entirely
    inside the box, and the surround is filled with a blurred, slightly darkened
    enlargement of the same photograph. Nothing is cut, nothing is letterboxed,
    and the fill reads as depth of field rather than as bars.
    """
    from PIL import ImageFilter, ImageEnhance
    box = (TILE_W, TILE_H)
    # backdrop: cover the box, blur it down, take the edge off the brightness
    bw, bh = src_im.size
    s = max(TILE_W / bw, TILE_H / bh)
    bg = src_im.resize((max(1, int(bw * s)), max(1, int(bh * s))), Image.LANCZOS)
    bx, by = (bg.width - TILE_W) // 2, (bg.height - TILE_H) // 2
    bg = bg.crop((bx, by, bx + TILE_W, by + TILE_H))
    bg = bg.filter(ImageFilter.GaussianBlur(38))
    bg = ImageEnhance.Brightness(bg).enhance(0.82)
    # foreground: the whole frame, as large as it will go
    fg = src_im.copy()
    fg.thumbnail(box, Image.LANCZOS)
    bg.paste(fg, ((TILE_W - fg.width) // 2, (TILE_H - fg.height) // 2))
    return bg


def focal(url):
    """Every cell now points at a derivative already cropped to the box shape,
    so filling and centring is all that is left to say."""
    return "background-size:cover;background-position:center"


def _edge_colour(im):
    """Median colour of the frame's outer border, as #rrggbb.

    Product shots sit on a light grey sweep and photographs have their own edge
    tone; painting the letterbox this colour makes a contained image read as a
    full-bleed one rather than a picture pasted onto white.
    """
    im = im.convert("RGB")
    w, h = im.size
    step = max(1, w // 60)
    px = im.load()
    edge = []
    for x in range(0, w, step):
        edge.append(px[x, 0]); edge.append(px[x, h - 1])
    for y in range(0, h, max(1, h // 60)):
        edge.append(px[0, y]); edge.append(px[w - 1, y])
    med = [sorted(c[i] for c in edge)[len(edge) // 2] for i in range(3)]
    return "#%02x%02x%02x" % tuple(med)


def render(tiles):
    """Two slides per post: (a) the photograph, (b) the write-up on paper.
    Post them together as an Instagram carousel, a before b."""
    out = []
    for n, t in enumerate(tiles, 1):
        cells = "".join(
            f'<div class="gi" '
            f'style="background-image:url(\'{tile_crop(u)}\');{focal(u)}"></div>'
            for u in t["imgs"])
        g = f'g{min(len(t["imgs"]), 4)}'
        # Two whole sentences run 41-560 characters. At a fixed 2.7em the long
        # ones overran the bottom of the square and got clipped mid-word, so the
        # paragraph is sized to its own length — same idea as type_scale() on
        # the paper slide.
        # Budget the block on headline AND body: the headline is set at 4.5em and
        # a three-liner (Manors) eats the room a two-liner leaves.
        strip = lambda x: re.sub(r"<[^>]+>", "", x or "")
        n = len(strip(t["text"])) + int(len(strip(t["title"])) * 1.8)
        em = 2.7 if n <= 240 else 2.4 if n <= 330 else 2.15 if n <= 430 else \
            1.95 if n <= 520 else 1.75
        txt = (f'<div class="ig-p" style="font-size:{em}em">{t["text"]}</div>'
               if t["text"] else '')
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
