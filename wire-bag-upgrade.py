#!/usr/bin/env python3
"""wire-bag-upgrade.py — put the bag post at the top of the feed. 22 Sep 2026.

Cuts the 4:5 feed card, inserts the homepage card in the top slot, and verifies
the finished artefacts rather than the strings that went into them.

WHY THE CARD IMAGE IS THE JONES FRAME AND NOT THE HERO. The hero is Shapland's
colour range lined up across a fairway, which is the best picture in the post
and completely unusable at 4:5 — it is a landscape composition, so a portrait
crop either shrinks the bags into the bottom third or decapitates them. Five
crops were cut and looked at before this was settled. The Jones clubhouse frame
is warm, high contrast against a feed of mostly outdoor greens, and carries the
Austin connection; it also means the card and the hero show two different
makers, which suits a post about three of them.

CARD SHAPE IS COPIED FROM THE FEED, NOT INVENTED. The house card is
div.card[data-type] > div.card-media > span.card-tag.grass + a > img, then
div.card-body > div.card-title > a, div.card-text, a.card-link. The Hat & Towel
Edit shipped without the green chip and without data-type because the shape was
written from memory, and it sat in the feed looking wrong and filtering wrong.
The verify block below checks this card against those four markers.

SELF-HEALING: MARK...END delimit the block so a re-run replaces it rather than
declaring victory on any MARK match.

Idempotent. Dry run by default.
"""
import collections
import json
import pathlib
import re
import subprocess
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
NEW = "/drops/upgrading-your-golf-bag"
HERO = "/images/shapland/hero.jpg"
CARD_SRC = ROOT / "images/jones-sports-co/texas-trouper-clubhouse.jpg"
CARD_IMG = "/images/bag-upgrade/card.jpg"
ANCHOR = "<!--TGI-SC-HOME-->"
MARK = "<!-- BAG UPGRADE -->"
END = "<!-- /BAG UPGRADE -->"

TITLE = "Upgrading Your Golf Bag &mdash; Three Makers a Step Above"
BLURB = ("Nine bags from Shapland, Shoal and Jones, $185 to $495. What the money buys, "
         "and the restock dates for the two that are sold out.")
CTA = "Read the bag report &#8599;"
ALT = "The Jones Texas Trouper carry bag resting against a clubhouse bar"

CARD = f'''{MARK}
  <div class="card" data-type="drop">
    <div class="card-media" style="position:relative;">
      <span class="card-tag grass">[Drops &amp; Brands]</span>
      <a href="{NEW}">
        <img src="{CARD_IMG}" alt="{ALT}" loading="lazy" style="width:100%;aspect-ratio:4/5;object-fit:cover;display:block;" />
      </a>
    </div>
    <div class="card-body">
      <div class="card-title"><a href="{NEW}" style="color:inherit;text-decoration:none;border-bottom:none;">{TITLE}</a></div>
      <div class="card-text">{BLURB}</div>
      <a href="{NEW}" class="card-link">{CTA}</a>
    </div>
  </div>
  {END}'''


def cut_card(apply_):
    im = Image.open(CARD_SRC).convert("RGB")
    w, h = im.size
    tw = round(h * 4 / 5)
    if tw > w:
        sys.exit(f"! source too narrow for a 4:5 card — {w}x{h}")
    im = im.crop(((w - tw) // 2, 0, (w - tw) // 2 + tw, h))
    target_w = min(1200, im.width)             # never upscale
    im = im.resize((target_w, round(target_w * 5 / 4)), Image.LANCZOS)
    p = ROOT / CARD_IMG.lstrip("/")
    print(f"  card: {w}x{h} -> {im.size[0]}x{im.size[1]}")
    if apply_:
        p.parent.mkdir(parents=True, exist_ok=True)
        im.save(p, "JPEG", quality=88, optimize=True, progressive=True)
    return im.size


def homepage(apply_):
    p = ROOT / "index.html"
    h = p.read_text(encoding="utf-8")
    if MARK in h:
        s = h.index(MARK)
        if END not in h:
            sys.exit("! card block present without its END marker")
        e = h.index(END, s) + len(END)
        if h[s:e].rstrip() == CARD.rstrip():
            return "card already in the feed, in the house shape"
        if apply_:
            p.write_text(h[:s] + CARD.rstrip() + h[e:], encoding="utf-8")
        return "card rebuilt to the house shape"
    if ANCHOR not in h:
        sys.exit("! feed anchor not found in index.html")
    if apply_:
        p.write_text(h.replace(ANCHOR, ANCHOR + "\n" + CARD, 1), encoding="utf-8")
    return "card inserted in the top slot"


def run(args, label):
    r = subprocess.run([sys.executable] + args, cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"! {label} failed:\n{r.stdout[-700:]}{r.stderr[-700:]}")
    tail = [l for l in r.stdout.strip().splitlines() if l.strip()][-1:]
    print(f"    {label}: {tail[0].strip() if tail else 'ok'}")


def main(apply_):
    cut_card(apply_)
    print("  homepage:", homepage(apply_))
    if not apply_:
        print("\n  dry run — pass --apply")
        return

    print("\n  regenerating derived artefacts:")
    run(["gen-post-thumbs.py", "--apply"], "gen-post-thumbs")
    run(["generate-search-index.py"], "generate-search-index")

    # ---- VERIFY THE FINISHED ARTEFACTS ----
    bad = []
    idx = (ROOT / "index.html").read_text(encoding="utf-8")
    if MARK not in idx:
        bad.append("homepage card missing")
    elif idx.index(MARK) - idx.index(ANCHOR) > 400:
        bad.append("homepage card is not in the top slot")
    blk = idx[idx.index(MARK):idx.index(END) + len(END)] if MARK in idx and END in idx else ""
    # Checked against the markers the NEIGHBOURING cards use, so a change to the
    # house shape surfaces here instead of shipping a card that looks wrong.
    for need, why in (('data-type="drop"', "no filter type — the feed chips would drop it"),
                      ('class="card-tag grass"', "no green category chip"),
                      ('class="card-link"', "non-house read-more"),
                      ('class="card-title"', "no card-title")):
        if need not in blk:
            bad.append(f"homepage card: {why}")
    kinds = collections.Counter(re.findall(r'<div class="card" data-type="(\w+)"', idx))
    if kinds and not kinds["drop"]:
        bad.append("no drop-type cards in the feed — the shape assumption is wrong")
    if idx.count(MARK) != 1 or idx.count(END) != 1:
        bad.append(f"{idx.count(MARK)} card blocks in the feed, expected 1")

    p = ROOT / CARD_IMG.lstrip("/")
    if not p.is_file():
        bad.append("card image missing")
    else:
        im = Image.open(p)
        if abs(im.width / im.height - 4 / 5) > 0.01:
            bad.append(f"card image is {im.width}x{im.height}, not 4:5")

    thumbs = json.loads((ROOT / "data/post-thumbs.json").read_text(encoding="utf-8"))
    if NEW not in thumbs:
        bad.append("no post-thumbs entry for the new post")
    elif thumbs[NEW].get("img") != HERO:
        bad.append(f"post-thumbs is {thumbs[NEW].get('img')}, not this post's hero")
    si = json.loads((ROOT / "search-index.json").read_text(encoding="utf-8"))
    if not any(r.get("u") == NEW for r in si):
        bad.append("new post missing from the search index")
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    if f"<loc>https://thegrassyissue.com{NEW}</loc>" not in sm:
        bad.append("new post missing from the sitemap")
    # the two new brands must have landed with it
    brands = {b["slug"] for b in json.loads((ROOT / "data/brands.json").read_text(encoding="utf-8"))}
    for s in ("shapland", "shoal-golf"):
        if s not in brands:
            bad.append(f"{s} not in brands.json")
        if not (ROOT / f"brands/{s}.html").is_file():
            bad.append(f"no brand page for {s}")

    if bad:
        sys.exit("! " + "\n    ".join(bad))
    print(f"\n  verified: card in the top slot wearing the house shape, "
          f"{len(brands)} brands, post in sitemap + search index")


if __name__ == "__main__":
    main("--apply" in sys.argv)
