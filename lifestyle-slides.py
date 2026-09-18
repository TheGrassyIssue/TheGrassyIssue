#!/usr/bin/env python3
"""
lifestyle-slides.py — the loud headline treatment, over the campaign photography.
17 September 2026.

Lenny: "we're on the right track, I'd like the text overlay on those high-res
nice promotional images."

This is the join between the two halves that were built separately:
  pull-lifestyle.py  got the photographs  (Manors at 6336x9504, Fyfe on the
                     Scottish coast) into ig-lifestyle/
  export-ig.py       got the treatment    (caps condensed, gold opening words,
                     swipe badge, wordmark, measured darkening)
Neither is new here. This puts one on the other and writes a postable slide.

COVER-CROP, NOT CONTAIN — THE OPPOSITE RULE FROM THE PRODUCT SLIDES
--------------------------------------------------------------------
fill_box pads anything far from square, which is right for a packshot: a garment
shot with deliberate margin should not lose 20% of itself to a crop. These are
not packshots. A 2:3 portrait of someone swinging on a clifftop wants to FILL the
frame — padding it would put grey bars either side of the exact photograph we
went and found. So this composes its own crop and always bleeds.

PACKSHOTS ARE REFUSED, NOT RESIZED
----------------------------------
Two of the Fyfe frames are a tweed headcover on white. They passed pull-lifestyle
because that script filtered on RESOLUTION, and a big packshot is still a
packshot — my filter tested the wrong property. A near-white border is the tell,
so anything with one is skipped here and named in the output rather than being
quietly dressed up in editorial type, which would look worse than leaving it out.

HEADLINES COME FROM index.html. Each brand folder maps to its post, and the post
supplies the title verbatim. Nothing is written here.

USAGE
    python3 lifestyle-slides.py                 # dry run
    python3 lifestyle-slides.py --apply
"""
import importlib.util, pathlib, sys, re, json
from PIL import Image, ImageDraw, ImageStat

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT.parent / "ig-lifestyle"
_s = importlib.util.spec_from_file_location("eig", ROOT / "export-ig.py")
E = importlib.util.module_from_spec(_s)
_s.loader.exec_module(E)
S, BASE = E.S, E.BASE

# One distinct line per slide. See lifestyle-lines.py for why these are extracted
# from the post rather than written, and why they describe the collection rather
# than the specific garment in frame.
_ls = importlib.util.spec_from_file_location("llines", ROOT / "lifestyle-lines.py")
LL = importlib.util.module_from_spec(_ls)
_ls.loader.exec_module(LL)

# brand folder -> the post whose headline it carries
POSTS = {
    "manors":               "manors-golf-aw26-collection",
    "fyfe-golf":            "brand-to-know-fyfe-golf",
    "birds-of-condor":      "brand-to-know-birds-of-condor",
    "hidden-links-society": "brand-to-know-hidden-links-society",
    "takomo":               "brand-to-know-takomo-golf",
    "apres-golf":           "brand-to-know-apres-golf",
    "gamut-golf":           "brand-to-know-gamut-golf",
    "bluegrass-fairway":    "brand-to-know-bluegrass-fairway",
    # added 18 September 2026
    "swag-golf":            "swag-golf-college-program",
    "public-drip":          "public-drip-fw26-nightshift",
    "edel-golf":            "brand-to-know-edel-golf",
    "forden-golf":          "brand-to-know-forden-golf",
    "jlindeberg":           "brand-to-know-jlindeberg",
    # Same brand as `manors`, different post. Its folder is seeded with the frames
    # the AW26 carousel did NOT consume, so the two carousels never show the same
    # photograph — two posts from one brand should not look like a repost.
    "manors-revisited":     "brand-to-know-manors",
}


def is_packshot(im):
    """A near-white border all the way round means a product on a sweep."""
    w, h = im.size
    band = max(2, min(w, h) // 25)
    edges = [im.crop((0, 0, w, band)), im.crop((0, h - band, w, h)),
             im.crop((0, 0, band, h)), im.crop((w - band, 0, w, h))]
    means = [ImageStat.Stat(e.convert("L")).mean[0] for e in edges]
    return sum(means) / 4 > 225


def bleed(im):
    """Fill 1080 square from any shape. Anchored at 0.38 rather than centre —
    heads and horizons both sit above the middle of a golf photograph."""
    w, h = im.size
    sc = max(S / w, S / h)
    im = im.resize((max(S, int(w * sc)), max(S, int(h * sc))), Image.LANCZOS)
    x = (im.width - S) // 2
    y = int((im.height - S) * 0.38)
    return im.crop((x, y, x + S, y + S))


def title_for(slug):
    src = (ROOT / "index.html").read_text(encoding="utf-8")
    m = re.search(r'class="card-title"[^>]*>\s*<a href="/drops/' + re.escape(slug)
                  + r'"[^>]*>(.*?)</a>', src, re.S)
    return E.ent(m.group(1)) if m else slug.replace("-", " ").title()


def caption(title, slug):
    """Same withholding rule as the digest: name the thing, do not answer it.
    The headline is an invitation; adding the write-up makes it a substitute."""
    return (f"{title}\n\n"
            f"The full piece \u2014 link in bio.\n"
            f"thegrassyissue.com/drops/{slug}\n\n"
            + " ".join("#" + t for t in E.CORE + ["golfbrands", "golfwear"]) + "\n")


def main():
    apply_ = "--apply" in sys.argv
    made, refused, built = 0, [], []
    for folder in sorted(p for p in SRC.iterdir() if p.is_dir()):
        slug = POSTS.get(folder.name)
        if not slug:
            continue
        title = title_for(slug)
        # Slide 1 carries the post title; every slide after it gets its own line.
        # The list is finite on purpose — when it runs out the carousel stops
        # rather than repeating, because one sentence on twelve photographs is
        # exactly the bug this rewrite exists to remove.
        lines = [title] + LL.lines_for(slug)
        out = folder / "slides"
        if apply_:
            out.mkdir(exist_ok=True)
            for stale in out.glob("*.jpg"):
                stale.unlink()          # counts shrink as well as grow; don't leave orphans
        n = 0
        for f in sorted(folder.glob("*.jpg")):
            if n >= len(lines) or n >= LL.MAX_SLIDES:
                break
            im = Image.open(f).convert("RGB")
            if is_packshot(im):
                refused.append(f"{folder.name}/{f.name}")
                continue
            sl = bleed(im)
            d = ImageDraw.Draw(sl, "RGBA")
            E.caps_headline(d, sl, lines[n], int(9.4 * BASE))
            # The badge belongs on the FIRST slide only. On slide four it is
            # telling someone already swiping to start swiping.
            if n == 0:
                E.swipe_badge(d)
            E.wordmark(d)
            n += 1
            if apply_:
                sl.save(out / f"{n:02d}-{folder.name}.jpg", "JPEG", quality=92, optimize=True)
            made += 1
        if n and apply_:
            # a carousel that does not say where to go converts nothing
            E.endcard({"href": f"/drops/{slug}"}).save(
                out / f"{n + 1:02d}-end.jpg", "JPEG", quality=92, optimize=True)
            (out / "caption.txt").write_text(caption(title, slug), encoding="utf-8")
            for stale in out.glob("*.jpg"):
                if not stale.name[:2].isdigit():
                    stale.unlink()
        if n:
            built.append((folder.name, n + 1, title))
    print(("wrote " if apply_ else "DRY RUN ") + f"{made} slides + {len(built)} end cards/captions")
    print()
    for b, total, t in sorted(built, key=lambda x: -x[1]):
        print(f"  {b:<22} {total:>2} slides   {t[:52]}")
    if refused:
        print(f"\n  refused {len(refused)} packshot(s) — a product on white does not"
              f" become editorial by having type put on it:")
        for r in refused:
            print("    ·", r)
    if not apply_:
        print("\n  pass --apply to write")


if __name__ == "__main__":
    main()
