#!/usr/bin/env python3
"""
export-ig.py — turn /ig into real 1080x1080 JPEGs, as multi-slide CAROUSELS,
with a caption file per post. 17 September 2026.

THE PROBLEM THIS SOLVES
-----------------------
build-ig.py has been generating /ig faithfully for weeks — 389 tiles, rebuilt
from index.html every run so it can never fall behind the feed. And not one of
them could leave the browser. .tile-img is a CSS background, so "save image as"
gets you nothing; the only export was screenshotting tiles by hand, one at a
time. 389 tiles against 23 posts actually on the account is the whole story.

So the grid does not look like the site. It is mostly "TODAY ON THE GRASSY
ISSUE" cover cards — wrappers that would suit any publication — while the site
itself shipped Hidden Links Society, the Austin sims, Lions Muny, 132 brands.
None of that is legible from the grid because none of it ever got out of /ig.

WHY PILLOW AND NOT A HEADLESS BROWSER
-------------------------------------
Rendering the existing tile HTML would have been the obvious route and it is not
available: Playwright's chromium is installed but will not start in this sandbox
(libXdamage.so.1 missing, and no root to apt-get it). Pillow needs no browser, is
deterministic, and — the part that actually decides it — the real fonts are on
disk, so the type is TGI's own rather than a substitute that looks close.

Editor's Note Text ships as .woff/.woff2 for the web, which Pillow cannot read.
The .otf originals were copied into assets/fonts/ so this script depends on the
repo and not on anyone's Downloads folder staying put. In The Margins was
already there. The only substitution is the mono kicker: the site asks for
JetBrains Mono, which is not vendored, so DejaVu Sans Mono stands in. At 13px,
tracked out to .24em and uppercase, the two are near enough to indistinguishable.

WHAT A CAROUSEL LOOKS LIKE
--------------------------
    slide 1      COVER     the approved /ig composition — category chip, lead
                           photograph, green wordmark, headline, two-sentence
                           summary. Unchanged from what is on /ig today.
    slides 2..N  PRODUCT   one per carousel image, full bleed, with that slide's
                           OWN caption bar. The homepage cards already carry
                           .gear-slide-brand and .gear-slide-name per slide
                           ("#1 - Play Faster Fairway Wood Cover" / "100% wool -
                           made with Ross Co Golf - $82"), so the copy is written
                           and verified. Nothing is invented here.
    last         END       the URL. A carousel that does not say where to go is
                           a carousel that converts nothing.

NOTHING IS INVENTED. Every price, product name and sentence on every slide is
lifted from index.html, which has already been through verify-post and
voice-lint. This script composes; it does not write copy.

IMAGE CROPPING is build-ig.py's, imported rather than reimplemented: rank_images
puts the least packshot-like frame first, and tile_crop does face-aware square
cropping so nobody gets beheaded by a centre crop. That logic took real work and
there is no reason to have two versions of it drifting apart.

OUTPUT LANDS OUTSIDE site/
--------------------------
    ~/Desktop/TheGrassyIssue/ig-export/
Deliberately NOT inside site/. Roughly 1,900 JPEGs at full quality would
otherwise be rsynced to the mirror and deployed to Vercel, which nobody wants.

USAGE
    python3 export-ig.py                 # 12 most recent posts (a sane first batch)
    python3 export-ig.py --limit 40
    python3 export-ig.py --all           # all 389 - slow, hundreds of MB
    python3 export-ig.py --slug brand-to-know-hidden-links-society
    python3 export-ig.py --all --force   # re-render everything from scratch

RERUNNING IS CHEAP. A post already exported is skipped, so the weekly habit is
just `python3 export-ig.py --all` after publishing — only the new ones render.
"""
import os, re, sys, html, json, importlib.util, pathlib, datetime, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageStat

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent / "ig-export"
S = 1080                      # Instagram's square, 1:1
BASE = S / 108.0              # the tile's own em base: 10px at 1080 in the CSS

PAPER, INK, GRASS, WHITE = "#F4F1EA", "#141414", "#2D4A2B", "#FFFFFF"

# ---------------------------------------------------------------- build-ig.py
# Imported, not copied. The filename has a hyphen so it is not a legal module
# name; importlib takes the path directly. main() is guarded by __name__ over
# there, so importing runs the module-level setup and nothing else.
_spec = importlib.util.spec_from_file_location("build_ig", ROOT / "build-ig.py")
BIG = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(BIG)

F_DIR = ROOT / "assets" / "fonts"
MONO_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def font(which, px):
    p = {"serif": F_DIR / "editors-note-text-regular.otf",
         "bold": F_DIR / "editors-note-text-bold.otf",
         "italic": F_DIR / "editors-note-text-italic.otf",
         "mono": pathlib.Path(MONO_PATH)}[which]
    if not p.exists():
        raise SystemExit(f"missing font {p} — cannot render type in the house face")
    return ImageFont.truetype(str(p), int(px))


def ent(s):
    """Card copy is HTML. &middot; and &mdash; must become characters, not words."""
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def tracked(d, xy, text, fnt, fill, track):
    """Pillow has no letter-spacing, and the kicker is nothing without it.
    Draws char by char and returns the width used."""
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=fnt, fill=fill)
        x += d.textlength(ch, font=fnt) + track
    return x - xy[0]


def wrap(d, text, fnt, width):
    """Greedy wrap on real measured widths — textwrap counts characters, which
    is wrong for a proportional face and shows up as ragged right edges."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _open(url):
    p = ROOT / url.lstrip("/").split("?")[0]
    return Image.open(p).convert("RGB") if p.exists() else None


def fill_box(url, bw, bh, anchor=0.42):
    """A site path -> exactly bw x bh, filled, no letterbox stripes.

    THE BUG THIS REPLACES. The first version called tile_crop and then squared
    the result. tile_crop already outputs 1080x734 — the tile's picture band —
    so squaring it cropped a second time, and the leftovers showed up as grey
    bars down both sides of every slide. One crop, decided here, or none.

    Which crop depends on the source, because the two kinds of image on this
    site want opposite treatment:
      near the target shape  -> COVER and crop. Nothing is lost that matters.
      far off it             -> CONTAIN onto build-ig's _edge_colour. Packshots
                                are 4:5 on white; cover-cropping one to a square
                                slices 20% off a product that was photographed
                                with deliberate margin. Padding in the frame's
                                own edge tone reads as full bleed instead.
    anchor is where the crop sits vertically — 0.42 rather than 0.5 keeps heads
    and club faces in, which centre-cropping does not.
    """
    im = _open(url)
    if im is None:
        return None
    w, h = im.size
    src, tgt = w / h, bw / bh
    # THE WINDOW USED TO START AT 0.78 AND THAT WAS WRONG BY TWO HUNDREDTHS.
    #
    # The house packshot is 4:5, which is 0.800, and the IG slide is 1:1 — so
    # every single product shot scored 0.800 against the window, fell inside it,
    # and got COVER-CROPPED. Twenty per cent off the height of a frame that was
    # photographed with deliberate margin. Lenny: "why are some of these so
    # zoomed in?" Because of this line.
    #
    # The docstring below already said packshots must be contained rather than
    # cropped; the number just did not agree with it. 0.86 puts 4:5 (0.800) and
    # 3:4 (0.750) firmly on the CONTAIN side where they belong, and leaves
    # genuinely near-square frames cropping as intended.
    if 0.86 <= src / tgt <= 1.28:
        scale = max(bw / w, bh / h)
        im = im.resize((max(bw, int(w * scale)), max(bh, int(h * scale))), Image.LANCZOS)
        x = (im.width - bw) // 2
        y = int((im.height - bh) * anchor)
        return im.crop((x, y, x + bw, y + bh))
    pad = Image.new("RGB", (bw, bh), BIG._edge_colour(im))
    scale = min(bw / w, bh / h)
    im = im.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)
    pad.paste(im, ((bw - im.width) // 2, (bh - im.height) // 2))
    return pad


# --------------------------------------------------------------- the slides
def cover(rec):
    """The approved /ig composition, at real pixels.

    Every dimension below is the CSS em value x BASE, so this is the same
    composition Lenny already signed off on rather than a new design:
      .ig-grid  flex 0 0 68%      .ig-lower  padding 3.4em 5.8em 3.2em
      .ig-logo  1.3em / .24em     .ig-h  4.5em / 1.08     .ig-p  2.7em / 1.4
    """
    im = Image.new("RGB", (S, S), PAPER)
    d = ImageDraw.Draw(im)

    # 68% of 1080 is 734 — which is exactly the shape tile_crop already targets
    # (TILE_W, TILE_H = 1080, 734 over there), so the picture band is filled
    # straight from it and the face-aware placement it decided is preserved.
    pic_h = BIG.TILE_H
    photo = fill_box(BIG.tile_crop(rec["imgs"][0]), S, pic_h) if rec.get("imgs") else None
    im.paste(photo, (0, 0)) if photo else d.rectangle([0, 0, S, pic_h], fill="#DDD9D0")

    # category chip, top-left, over the photo
    chip_f = font("mono", 1.25 * BASE)
    label = ent(rec["tag"]).upper()
    pad_x, pad_y = int(1.8 * BASE), int(1.1 * BASE)
    w = sum(d.textlength(c, font=chip_f) + 2.4 for c in label)
    d.rectangle([int(2.6 * BASE), int(2.6 * BASE),
                 int(2.6 * BASE) + w + pad_x * 2,
                 int(2.6 * BASE) + chip_f.size + pad_y * 2], fill=GRASS)
    tracked(d, (int(2.6 * BASE) + pad_x, int(2.6 * BASE) + pad_y),
            label, chip_f, WHITE, 2.4)

    x = int(5.8 * BASE)
    y = pic_h + int(3.4 * BASE)
    inner = S - x * 2

    logo_f = font("mono", 1.3 * BASE)
    tracked(d, (x, y), "THE GRASSY ISSUE", logo_f, GRASS, 1.3 * BASE * 0.24)
    y += int(logo_f.size + 1.077 * logo_f.size)

    h_f = font("bold", 4.5 * BASE)
    for line in wrap(d, ent(rec["title"]), h_f, inner)[:3]:
        d.text((x, y), line, font=h_f, fill=INK)
        y += int(h_f.size * 1.08)
    y += int(h_f.size * 0.356)

    p_f = font("serif", 2.7 * BASE)
    # .ig-p is opacity .8 on #141414 over #F4F1EA — composited to a flat value,
    # because Pillow text has no opacity and a second layer is not worth it.
    for line in wrap(d, ent(rec["text"]), p_f, inner):
        if y + p_f.size > S - int(3.2 * BASE):
            break
        d.text((x, y), line, font=p_f, fill="#3E3D39")
        y += int(p_f.size * 1.4)
    return im


def product(url, kicker, meta):
    """A carousel image, full bleed, with the copy that belongs to THAT slide."""
    im = fill_box(url, S, S)
    if im is None:
        return None
    d = ImageDraw.Draw(im, "RGBA")
    if not (kicker or meta):
        return im

    k_f, m_f = font("bold", 3.1 * BASE), font("serif", 2.3 * BASE)
    k_lines = wrap(d, ent(kicker), k_f, S - int(11.6 * BASE)) if kicker else []
    m_lines = wrap(d, ent(meta), m_f, S - int(11.6 * BASE))[:2] if meta else []
    block = (len(k_lines) * k_f.size * 1.12 + len(m_lines) * m_f.size * 1.35
             + 5.8 * BASE)

    # A scrim, not a solid bar: the photograph is the point, the copy has to be
    # readable over it, and a hard bar crops the picture for no reason.
    grad = Image.new("L", (1, S), 0)
    gd = ImageDraw.Draw(grad)
    start = int(S - block - 6 * BASE)
    for i in range(start, S):
        gd.point((0, i), fill=int(215 * ((i - start) / max(1, S - start)) ** 0.85))
    im.paste(Image.new("RGB", (S, S), INK), (0, 0),
             grad.resize((S, S), Image.BILINEAR))

    y = int(S - block - 2.2 * BASE)
    x = int(5.8 * BASE)
    for line in k_lines:
        d.text((x, y), line, font=k_f, fill=WHITE)
        y += int(k_f.size * 1.12)
    for line in m_lines:
        d.text((x, y), line, font=m_f, fill="#E2DED5")
        y += int(m_f.size * 1.35)
    return im


# ------------------------------------------------------------------- DIGEST
#
# Lenny, 17 September 2026: "the posts give too much away and keep people from
# visiting the site, I'd rather do a once weekly or twice weekly post of an
# overview of what we've been covering."
#
# He is right, and the per-post carousels above are the problem. They carry the
# product name, the spec AND the price on every slide, plus a two-sentence
# summary in the caption. Someone who swipes one has read the roundup. There is
# nothing left on the site for them, so they do not go.
#
# The digest is built to WITHHOLD. Each post gets a photograph, a number and its
# headline — and that is the whole slide. No prices, no specs, no summary, no
# "here are the three we liked". A headline is an invitation; a headline plus the
# answer is a substitute. The caption is the same discipline: a numbered list of
# titles, one link, nothing else.
#
# This is the "Today on The Grassy Issue" franchise done properly — the format
# was never the problem, the ratio was, and so was giving the whole thing away.
DIGEST_TITLE = "This Week on"


# --------------------------------------------------------- THE LOUD TREATMENT
#
# Lenny, 17 September 2026, pointing at @golfheadz: "I want something more
# similar to this page." What that account actually does, looked at rather than
# guessed: full-bleed product photography, headline in ALL-CAPS CONDENSED SANS
# anchored bottom-left, the first few words in a GOLD HIGHLIGHT and the rest in
# white, a SWIPE LEFT badge top-right, and the wordmark small and centred at the
# base. The serif reads as a magazine; the condensed caps read as a feed.
#
# The highlight is the part doing most of the work. Two tones inside one
# headline give the eye somewhere to land at thumbnail size, which a single
# weight of anything does not.
#
# NOT vendored: golfheadz's actual face. Liberation Sans Narrow Bold is the
# closest condensed grotesque on this box and is metrically sane at display
# size. If TGI ever licenses a real condensed (Druk, Knockout, Barlow
# Condensed), change COND_PATH and nothing else.
COND_PATH = "/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf"
HL = "#E8B54A"

# Frames that must never lead a slide. A page screenshot or a poster is a
# picture of type, and no amount of resolution or headline treatment saves it —
# it reads as a screenshot of a website because it is one. build-ig's
# rank_images scores packshot-likeness but has no concept of "this is our own
# marketing art", so the filename is the signal available.
NOT_PHOTO = re.compile(r"(poster|screenshot|banner|flyer|promo|artwork|tile|"
                       r"logo|wordmark|graphic|cover-card)", re.I)


def cond(px):
    return ImageFont.truetype(COND_PATH, int(px))


def photo_first(urls):
    """rank_images, then push anything that is not a photograph to the back."""
    ranked = BIG.rank_images([u for u in urls if u]) if urls else []
    real = [u for u in ranked if not NOT_PHOTO.search(u)]
    return real + [u for u in ranked if NOT_PHOTO.search(u)]


def caps_headline(d, im, text, y_from, max_lines=3, gold_words=2, size=5.0):
    """Caps condensed, bottom-anchored, opening words in gold. Returns the top y."""
    f = cond(size * BASE)
    lines = wrap(d, text.upper(), f, S - int(9 * BASE))[:max_lines]
    block = len(lines) * f.size * 1.12
    _darken_to(im, int(S - block - 12 * BASE), S, 34)
    y = int(S - block - y_from)
    done = 0
    for ln in lines:
        cx = int(4.4 * BASE)
        for w in ln.split():
            d.text((cx, y), w, font=f, fill=HL if done < gold_words else "#FFFFFF")
            cx += d.textlength(w + " ", font=f)
            done += 1
        y += int(f.size * 1.12)
    return block


def swipe_badge(d):
    bf = cond(1.9 * BASE)
    lbl = "SWIPE LEFT ❯❯"
    bw = d.textlength(lbl, font=bf)
    d.rectangle([S - int(bw + 6.4 * BASE), int(2.2 * BASE),
                 S - int(2.2 * BASE), int(2.2 * BASE + bf.size + 2.6 * BASE)],
                fill=(0, 0, 0, 155))
    d.text((S - int(bw + 4.3 * BASE), int(3.4 * BASE)), lbl, font=bf, fill="#FFFFFF")


def wordmark(d, colour="#D9D5CC"):
    wm = cond(1.7 * BASE)
    t = "THE GRASSY ISSUE"
    w = sum(d.textlength(c, font=wm) + 1.7 * BASE * 0.22 for c in t)
    tracked(d, ((S - w) / 2, S - int(4.6 * BASE)), t, wm, colour, 1.7 * BASE * 0.22)


def hook(rec):
    """The distinctive part of a headline, for teasing on the cover.

    EXTRACTION, NOT REWRITING — house rule. Franchise prefixes ("Brand to Know
    —", "Field Notes —") are the same on every post and carry no information, so
    they come off; then the title is cut at its first comma or colon, which is
    where TGI headlines put the qualifier. "Twenty Putters for the Late-Season
    Switch, From $170 to $799" -> "Twenty Putters for the Late-Season Switch".
    Nothing is reworded and no claim is added.
    """
    t = ent(rec["title"])
    t = re.sub(r"^(Brand to Know|Brand Revisited|Field Notes?|News|Drop)\s*[—\-–:]\s*",
               "", t, flags=re.I)
    return re.split(r"\s*[,:]\s", t)[0].strip()


def _scrim(im, from_y, strength=232, gamma=0.8):
    grad = Image.new("L", (1, S), 0)
    gd = ImageDraw.Draw(grad)
    for j in range(from_y, S):
        gd.point((0, j), fill=int(strength * ((j - from_y) / max(1, S - from_y)) ** gamma))
    im.paste(Image.new("RGB", (S, S), INK), (0, 0), grad.resize((S, S), Image.BILINEAR))


def _darken_to(im, y0, y1, target=62):
    """Guarantee white type is readable over whatever photograph turned up.

    THE FIRST VERSION OF THESE COVERS FAILED ON EXACTLY THIS. The scrim was a
    fixed proportional gradient, which is fine over a dark course photograph and
    useless over a pale one — and the lead image the week this shipped was a
    framed print on a light grey sweep, so "THIS WEEK" came out white on near
    white and could not be read at all. A cover that depends on the luck of the
    week's photography is not a cover.

    So the band under the type is MEASURED and then darkened by however much it
    actually needs to reach `target` mean luminance. A dark photo is left nearly
    alone; a pale one gets pushed hard. Either way the type reads.
    """
    band = im.crop((0, max(0, y0), S, min(S, y1))).convert("L")
    mean = ImageStat.Stat(band).mean[0]
    if mean <= target:
        return
    need = min(0.86, 1 - (target / max(mean, 1)))
    ov = Image.new("L", (1, S), 0)
    od = ImageDraw.Draw(ov)
    span = max(1, y1 - y0)
    for j in range(max(0, y0 - int(9 * BASE)), S):
        t = min(1.0, max(0.0, (j - (y0 - 9 * BASE)) / (span * 0.55)))
        od.point((0, j), fill=int(255 * need * (t ** 0.75)))
    im.paste(Image.new("RGB", (S, S), INK), (0, 0), ov.resize((S, S), Image.BILINEAR))


def best_photo(recs):
    """The most photographic frame of the WEEK, not just the newest post's.

    rank_images scores how packshot-like a frame is and puts the least
    packshot-like first, so pooling every image across the week's posts and
    ranking the pool finds a real photograph even in a week whose newest post is
    a product cut-out on white. The cover is the one slide that has to carry.
    """
    pool = []
    for r in recs:
        pool += r.get("imgs", [])
    ranked = photo_first(pool)
    return ranked[0] if ranked else (recs[0]["imgs"][0] if recs and recs[0].get("imgs") else None)


def cover_photo(recs, when):
    """The week's best photograph, THIS WEEK in caps condensed, the names under
    it, and a swipe badge — the golfheadz lockup in TGI's colours."""
    lead = best_photo(recs)
    im = fill_box(BIG.tile_crop(lead), S, S, anchor=0.3) if lead else None
    if im is None:
        return None
    d = ImageDraw.Draw(im, "RGBA")
    names = [hook(r) for r in recs]
    line_f = cond(2.7 * BASE)
    lines = []
    for nm in names:
        lines += wrap(d, nm.upper(), line_f, S - int(11 * BASE))[:1]
    big = cond(11.2 * BASE)
    block = big.size * 1.02 + 6.4 * BASE + len(lines) * line_f.size * 1.5
    _darken_to(im, int(S - block - 12 * BASE), S, 44)

    swipe_badge(d)
    x = int(4.4 * BASE)
    y = int(S - block - 6.2 * BASE)
    d.text((x, y), "THIS WEEK", font=big, fill=WHITE)
    y += int(big.size * 1.02)
    sm = cond(1.6 * BASE)
    tracked(d, (x + int(0.4 * BASE), y), f"{len(recs)} STORIES   {when.upper()}",
            sm, HL, 1.6 * BASE * 0.2)
    y += int(sm.size * 2.5)
    for ln in lines:
        d.rectangle([x, y + int(0.9 * BASE), x + int(0.55 * BASE),
                     y + int(line_f.size * 0.92)], fill=HL)
        d.text((x + int(2.0 * BASE), y), ln, font=line_f, fill="#F2EFE8")
        y += int(line_f.size * 1.5)
    return im


def cover_grid(recs, when):
    """B — a 2x2 of the week's photographs with a type plate across the middle.

    Reads as "several things happened" at a glance, which is what a digest is,
    and four frames give four chances for one of them to catch an eye."""
    im = Image.new("RGB", (S, S), INK)
    half = S // 2
    for i, r in enumerate(recs[:4]):
        cell = fill_box(BIG.tile_crop(r["imgs"][0]), half, half)  # one per post: the mix is the point
        if cell:
            im.paste(cell, ((i % 2) * half, (i // 2) * half))
    d = ImageDraw.Draw(im, "RGBA")

    plate_h = int(30 * BASE)
    top = (S - plate_h) // 2
    d.rectangle([0, top, S, top + plate_h], fill=PAPER)
    d.rectangle([0, top, S, top + int(0.9 * BASE)], fill=GRASS)

    big = font("bold", 8.2 * BASE)
    y = top + int(5.4 * BASE)
    for line in ["THIS WEEK ON", "THE GRASSY ISSUE"]:
        w = d.textlength(line, font=big)
        d.text(((S - w) / 2, y), line, font=big, fill=INK)
        y += int(big.size * 1.02)
    sub = font("mono", 1.55 * BASE)
    lbl = f"{len(recs)} STORIES  ·  {when.upper()}"
    w = sum(d.textlength(c, font=sub) + 1.55 * BASE * 0.22 for c in lbl)
    tracked(d, ((S - w) / 2, y + int(1.4 * BASE)), lbl, sub, GRASS, 1.55 * BASE * 0.22)
    return im


def cover_number(recs, when):
    """C — the count as the whole image. One enormous numeral, then the names.

    The loudest of the three and the most legible at thumbnail size, where a
    digit survives scaling that type does not."""
    lead = best_photo(recs)
    im = fill_box(BIG.tile_crop(lead), S, S, anchor=0.34) if lead else None
    if im is None:
        return None
    _darken_to(im, 0, S, 48)
    d = ImageDraw.Draw(im, "RGBA")

    num = font("bold", 46 * BASE)
    t = str(len(recs))
    w = d.textlength(t, font=num)
    d.text(((S - w) / 2, int(S * 0.055)), t, font=num, fill=WHITE)

    y = int(S * 0.545)
    lab = font("bold", 6.2 * BASE)
    for line in ["stories from", "The Grassy Issue"]:
        w = d.textlength(line, font=lab)
        d.text(((S - w) / 2, y), line, font=lab, fill=WHITE)
        y += int(lab.size * 1.05)

    y += int(2.6 * BASE)
    small = font("mono", 1.42 * BASE)
    for r in recs[:4]:
        nm = hook(r).upper()
        w = sum(d.textlength(c, font=small) + 1.42 * BASE * 0.18 for c in nm)
        if w > S - 10 * BASE:
            nm = nm[:34].rstrip() + "…"
            w = sum(d.textlength(c, font=small) + 1.42 * BASE * 0.18 for c in nm)
        tracked(d, ((S - w) / 2, y), nm, small, "#CBDCC4", 1.42 * BASE * 0.18)
        y += int(small.size * 1.9)
    return im


COVERS = {"photo": cover_photo, "grid": cover_grid, "number": cover_number}


def digest_cover(n, when):
    im = Image.new("RGB", (S, S), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, S, int(1.6 * BASE)], fill=GRASS)

    ey = font("mono", 1.5 * BASE)
    lbl = when.upper()
    w = sum(d.textlength(c, font=ey) + 1.5 * BASE * 0.22 for c in lbl)
    tracked(d, ((S - w) / 2, int(S * 0.20)), lbl, ey, GRASS, 1.5 * BASE * 0.22)

    big = font("serif", 7.4 * BASE)
    y = int(S * 0.30)
    for line in [DIGEST_TITLE, "The Grassy", "Issue"]:
        tw = d.textlength(line, font=big)
        d.text(((S - tw) / 2, y), line, font=big, fill=INK)
        y += int(big.size * 1.03)

    y += int(3.4 * BASE)
    sub = font("bold", 3.0 * BASE)
    line = f"{n} stories"
    tw = d.textlength(line, font=sub)
    d.text(((S - tw) / 2, y), line, font=sub, fill=GRASS)

    foot = font("mono", 1.35 * BASE)
    lbl = "SWIPE  ·  FULL POSTS AT THEGRASSYISSUE.COM"
    w = sum(d.textlength(c, font=foot) + 1.35 * BASE * 0.2 for c in lbl)
    tracked(d, ((S - w) / 2, int(S - 7.4 * BASE)), lbl, foot, "#6C6A63", 1.35 * BASE * 0.2)
    return im


def digest_item(rec, i, n):
    """A photograph and the headline, in the loud treatment. Still no prices,
    no specs, no summary — the withholding rule is unchanged, only the type is."""
    lead = photo_first(rec.get("imgs", []))
    im = fill_box(BIG.tile_crop(lead[0]), S, S, anchor=0.38) if lead else None
    if im is None:
        return None
    d = ImageDraw.Draw(im, "RGBA")
    block = caps_headline(d, im, ent(rec["title"]), int(9.4 * BASE))
    k = cond(1.5 * BASE)
    tracked(d, (int(4.4 * BASE), int(S - block - 14.2 * BASE)),
            f"{i:02d} / {n:02d}   {ent(rec['tag']).upper()}", k, HL, 1.5 * BASE * 0.2)
    wordmark(d)
    return im


def digest_caption(recs, when):
    body = "\n".join(f"{i:02d}  {ent(r['title'])}" for i, r in enumerate(recs, 1))
    return (f"{DIGEST_TITLE} The Grassy Issue — {when}\n\n{body}\n\n"
            "All of it, in full, at thegrassyissue.com — link in bio.\n\n"
            + " ".join("#" + t for t in CORE) + "\n")


def endcard(rec):
    """The last slide, in the same loud system as the rest.

    It was still the old cream serif card after the treatment changed, which
    made every carousel end on a slide that looked like it came from a different
    account. A carousel is a system or it is nothing."""
    im = Image.new("RGB", (S, S), INK)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, S, int(1.4 * BASE)], fill=HL)

    big = cond(10.4 * BASE)
    y = int(S * 0.30)
    for line in ["READ IT", "IN FULL"]:
        w = d.textlength(line, font=big)
        d.text(((S - w) / 2, y), line, font=big, fill=WHITE)
        y += int(big.size * 1.0)

    y += int(4.0 * BASE)
    u = font("bold", 3.2 * BASE)
    line = "thegrassyissue.com"
    w = d.textlength(line, font=u)
    d.text(((S - w) / 2, y), line, font=u, fill=HL)

    y += int(u.size * 2.1)
    sub = cond(1.55 * BASE)
    lbl = "LINK IN BIO"
    w = sum(d.textlength(c, font=sub) + 1.55 * BASE * 0.24 for c in lbl)
    tracked(d, ((S - w) / 2, y), lbl, sub, "#9A968D", 1.55 * BASE * 0.24)
    wordmark(d, "#6E6A62")
    return im


# ------------------------------------------------------------------ captions
CORE = ["golf", "golfstyle", "indiegolf", "golfapparel", "atxgolf",
        "austingolf", "austintexas", "golflife", "publicgolf", "golfgear"]
BYTAG = {"Drops & Brands": ["golfbrands", "newdrop", "golfwear"],
         "Field Notes": ["golfcourse", "muni", "golftrip"],
         "News": ["golfnews", "golfculture"]}


def caption(rec):
    body = ent(rec["text"])
    tags = CORE + BYTAG.get(ent(rec["tag"]), [])
    return (f"{ent(rec['title'])}\n\n{body}\n\n"
            f"Full post — link in bio. thegrassyissue.com{rec['href']}\n\n"
            + " ".join("#" + t for t in tags) + "\n")


# ---------------------------------------------------------------------- main
def slides_for(rec, seg):
    """Cover, then one slide per carousel image, then the end card."""
    media = seg[:seg.find("card-body")] if "card-body" in seg else seg
    urls = re.findall(r'<img[^>]+src="([^"]+)"', media)
    kick = re.findall(r'gear-slide-brand">(.*?)</div>', media, re.S)
    meta = re.findall(r'gear-slide-name">(.*?)</div>', media, re.S)

    out = [("01-cover", cover(rec))]
    seen, n = set(), 0
    for i, u in enumerate(urls):
        if u in seen:
            continue
        seen.add(u)
        n += 1
        if n > 8:          # 10 slides total is the safe carousel ceiling
            break
        im = product(u, kick[i] if i < len(kick) else "",
                     meta[i] if i < len(meta) else "")
        if im:
            out.append((f"{n + 1:02d}-slide", im))
    out.append((f"{len(out) + 1:02d}-end", endcard(rec)))
    return out


def main():
    argv = sys.argv[1:]
    only = None
    if "--slug" in argv:
        only = argv[argv.index("--slug") + 1]
    limit = (10 ** 6 if "--all" in argv else
             int(argv[argv.index("--limit") + 1]) if "--limit" in argv else 12)

    src = (ROOT / "index.html").read_text(encoding="utf-8")
    opens = [m.start() for m in re.finditer(r'<div class="card"', src)]
    bounds = opens + [len(src)]
    # SIX URLS HAVE MORE THAN ONE FEED CARD — Lions Muny, Casualist, Mogshade,
    # Kingfisher, premium-tees, hats. Keying by href and letting the last one win
    # picked whichever card happened to sit lower in the feed, and for Lions that
    # was the typographic News panel with no <img> at all: the carousel came out
    # as a cover and an end card with nothing in between, while the card directly
    # above it had four photographs. Keep the card with the most images instead.
    segs = {}
    for i, a in enumerate(opens):
        seg = src[a:bounds[i + 1]]
        h = re.search(r'class="card-title"[^>]*>\s*<a href="(/[^"]+)"', seg)
        if not h:
            continue
        def _n(x):
            m = x[:x.find("card-body")] if "card-body" in x else x
            return len(re.findall(r'<img[^>]+src="', m))
        if h.group(1) not in segs or _n(seg) > _n(segs[h.group(1)]):
            segs[h.group(1)] = seg

    tiles, noimg = BIG.scrape(ROOT / "index.html")
    if only:
        tiles = [t for t in tiles if only in t["href"]]
        if not tiles:
            raise SystemExit(f"no post matching --slug {only}")

    # ---------------------------------------------------------------- digest
    if "--digest" in argv:
        i = argv.index("--digest")
        n = int(argv[i + 1]) if i + 1 < len(argv) and argv[i + 1].isdigit() else 5
        when = datetime.date.today().strftime("%d %B %Y").lstrip("0")
        recs = [r for r in tiles if r.get("imgs")][:n]
        d = OUT / "digests" / datetime.date.today().isoformat()
        d.mkdir(parents=True, exist_ok=True)

        # --cover photo|grid|number|quiet ; --covers renders all of them side by
        # side so the choice is made by looking rather than by description.
        # Lenny picked "photo", 17 September 2026 — the only treatment that puts the
        # actual names on the cover, so the hook is "Hidden Links Society" and not
        # "we posted some things". --cover grid|number|quiet overrides per run.
        style = argv[argv.index("--cover") + 1] if "--cover" in argv else "photo"
        if "--covers" in argv:
            for k2, fn in COVERS.items():
                im2 = fn(recs, when)
                if im2:
                    im2.save(d / f"00-cover-{k2}.jpg", "JPEG", quality=92, optimize=True)
            digest_cover(len(recs), when).save(d / "00-cover-quiet.jpg", "JPEG",
                                               quality=92, optimize=True)
            print(f"cover options -> {d}")
            return
        cov = COVERS[style](recs, when) if style in COVERS else digest_cover(len(recs), when)
        if cov is None:
            cov = digest_cover(len(recs), when)
        cov.save(d / "01-cover.jpg", "JPEG", quality=92, optimize=True)
        k = 1
        for j, rec in enumerate(recs, 1):
            im = digest_item(rec, j, len(recs))
            if im:
                k += 1
                im.save(d / f"{k:02d}-{rec['href'].rsplit('/', 1)[-1][:40]}.jpg",
                        "JPEG", quality=92, optimize=True)
        endcard({"href": ""}).save(d / f"{k + 1:02d}-end.jpg", "JPEG",
                                   quality=92, optimize=True)
        (d / "caption.txt").write_text(digest_caption(recs, when), encoding="utf-8")
        print(f"digest -> {d}  ({k + 1} slides, {len(recs)} stories)")
        for r in recs:
            print("   ·", ent(r["title"])[:66])
        return

    todo = tiles[:limit]

    OUT.mkdir(parents=True, exist_ok=True)
    made, skipped, renamed, queue = 0, 0, 0, []
    force = "--force" in argv

    # FOLDERS ARE NUMBERED NEWEST FIRST — 001 is the most recent post, so the
    # folder list sorts into feed order instead of alphabetically, where
    # "10-indie-ball-marker-brands" led and the newest post sat wherever its
    # name happened to fall.
    #
    # The number is POSITION, not an id, so it moves: publish something and
    # everything below it shifts by one. That means each run has to re-number
    # what is already on disk rather than leaving stale prefixes behind, and it
    # has to find a post's existing folder under whatever number it had last
    # time — which is what prior_dir does. The slug stays in the name so the
    # folder is still readable, and so a rename can never collide with another
    # post that happens to want the same number.
    def prior_dir(slug):
        for p in OUT.iterdir():
            if not p.is_dir():
                continue
            n = p.name
            if n == slug or (len(n) == len(slug) + 4 and n[:3].isdigit()
                             and n[3] == "-" and n[4:] == slug):
                return p
        return None

    for rank, rec in enumerate(todo, 1):
        slug = rec["href"].rstrip("/").rsplit("/", 1)[-1]
        d = OUT / f"{rank:03d}-{slug}"
        old = prior_dir(slug)
        if old and old != d:
            old.rename(d)
            renamed += 1
        d.mkdir(exist_ok=True)

        # RESUME. A full run is ~1,400 renders; if it dies halfway, or the
        # terminal is closed, nothing already finished should be redone. A post
        # counts as done when its cover and its caption both exist. This is also
        # what makes the weekly habit cheap: after publishing, rerun --all and
        # only the new posts render.
        if not force and (d / "01-cover.jpg").exists() and (d / "caption.txt").exists():
            skipped += 1
            queue.append((d.name, len(list(d.glob("*.jpg"))), ent(rec["title"])))
            continue
        try:
            sl = slides_for(rec, segs.get(rec["href"], ""))
        except Exception as e:
            print(f"  !! {slug}: {e}")
            continue
        for name, im in sl:
            im.save(d / f"{name}.jpg", "JPEG", quality=92, optimize=True)
        (d / "caption.txt").write_text(caption(rec), encoding="utf-8")
        made += 1
        queue.append((d.name, len(sl), ent(rec["title"])))
        print(f"  {d.name:<56} {len(sl)} slides")

    # The count is the whole QUEUE, not what this run happened to render. On a
    # resumed run `made` is 0 and the header read "0 posts ready" over a list of
    # 192 — which is the opposite of the truth.
    lines = ["# IG queue — generated by export-ig.py",
             f"# {datetime.date.today()} · {len(queue)} carousels ready "
             f"({made} rendered this run) · newest first", ""]
    for slug, n, title in queue:
        lines.append(f"- [ ] **{title}** — `{slug}/` · {n} slides")
    (OUT / "QUEUE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    size = sum(f.stat().st_size for f in OUT.rglob("*.jpg")) / 1_048_576
    print(f"\n{made} rendered, {skipped} already done, {renamed} re-numbered"
          f" -> {OUT}  ({size:.0f} MB total)")
    if noimg:
        print(f"{len(noimg)} post(s) skipped for having no card image:")
        for r in noimg[:5]:
            print("   !!", r["href"])
    if not ("--all" in argv or "--slug" in argv):
        print(f"\n(first {limit} only — pass --limit N or --all)")


if __name__ == "__main__":
    main()
