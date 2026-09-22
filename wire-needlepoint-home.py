#!/usr/bin/env python3
"""wire-needlepoint-home.py — put the needlepoint report into the feed.
22 September 2026.

WHY THIS EXISTS: THE POST SHIPPED AS AN ORPHAN. The page went live at
/drops/the-needlepoint-belt-report in commit ae9eaf4e and is reachable, but it
is in no sitemap, no search index and nowhere on the homepage, because the
wiring step never ran. Lenny noticed before I did: "the needlepoint post isn't
showing up on the site." Deploying a page is not publishing it — three separate
artefacts have to name it before anyone but a direct-link visitor can find it,
and Google cannot discover it at all.

Lenny: "feature the ric flair at the one spot on the homepage, then 3 of your
choices + a key fob." Five slides, Ric Flair leading.

THE CARD SHAPE IS COPIED OUT OF index.html, NOT WRITTEN FROM MEMORY. The house
gear card is card[data-type] > card-media > card-tag.grass + gear-carousel
[data-carousel] > gear-carousel-track > gear-slide*, then the two gear-arrow
buttons, then card-body > card-title > a, card-text[data-slidetext],
gear-dots[data-dots], gear-counter[data-counter], a.card-link. The Hat & Towel
Edit once shipped without the green chip and without data-type because the shape
was written from memory, and it sat in the feed looking wrong and filtering
wrong. The verify block checks against those markers.

THE ARROWS NEED THEIR INLINE HANDLERS. gearSlide(this, ±1) is bound by the
onclick attribute, not by a delegated listener, so a carousel card that ships
without them renders fine and silently does nothing when clicked. Same for the
three data-* keys: data-carousel, data-slidetext, data-dots and data-counter
must all carry the SAME slug or the caption and counter track a different card.
Both are checked below.

Idempotent. Dry run by default.
"""
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
RES = ROOT / "research/needlepoint"
POST = "/drops/the-needlepoint-belt-report"
KEY = "needlepoint"
ANCHOR = "<!--TGI-SC-HOME-->"
MARK, END = "<!-- NEEDLEPOINT -->", "<!-- /NEEDLEPOINT -->"

TITLE = "Needlepoint Golf Belts &mdash; 18 Hand-Stitched Picks"
BLURB = ("Eighteen hand-stitched belts from six makers, $124 to $220, plus three key fobs. "
         "Prices and stock read from each maker&rsquo;s own store on 22 September 2026.")
CTA = "Read the belt report &#8599;"

# Lenny's order: Ric Flair first, then three of mine, then a key fob.
# (manifest slug, the kicker line above the product name)
SLIDES = [
    ("charleston-ric-flair", "The loudest belt in golf"),
    ("smathers-branson-usga-126th-us-open-shinnecock", "Official USGA, 126th US Open"),
    ("good-threads-golf-flags-green", "Cheapest hand-stitched here"),
    ("j-press-dancing-bear-oatmeal", "New Haven, since 1902"),
    ("charleston-azalea-on-augusta-green", "The cheap way in"),
]


def slides_html(man):
    out = []
    for slug, kicker in SLIDES:
        if slug not in man:
            sys.exit(f"! {slug} is not in the manifest")
        m = man[slug]
        # SHORT NAME, NOT THE FULL STORE TITLE. The Shinnecock belt's real title
        # runs to 76 characters ("...Logo-Text-Clubhouse Centered (Classic Navy)")
        # and overflows the caption strip at card width.
        name = re.sub(r"\s*\(.*?\)\s*$", "", m["title"]).strip()
        name = re.sub(r"\s*Needlepoint Belt$", "", name).strip()
        name = re.sub(r"^Key Fob &mdash;\s*|^Key Fob —\s*", "", name).strip()
        if len(name) > 46:
            name = name[:44].rstrip() + "…"
        alt = f'{m["brand"]} {name}'
        out.append(
            f'          <div class="gear-slide">\n'
            f'            <a href="{m["url"]}" target="_blank" rel="noopener">\n'
            f'              <img src="{m["frames"][0]}" alt="{alt}" loading="lazy" />\n'
            f'              <div class="gear-slide-info">'
            f'<div class="gear-slide-brand">{kicker}</div>'
            f'<div class="gear-slide-name">{name} &middot; {m["price"]}</div></div>\n'
            f'            </a>\n'
            f'          </div>')
    return "\n".join(out)


def card(man):
    return f'''{MARK}
  <div class="card" data-type="drop">
    <div class="card-media" style="position:relative;">
      <span class="card-tag grass">[Drops &amp; Brands]</span>
      <div class="gear-carousel" data-carousel="{KEY}">
        <div class="gear-carousel-track">
{slides_html(man)}
        </div>
        <button class="gear-arrow prev" onclick="gearSlide(this, -1)">&#8249;</button>
        <button class="gear-arrow next" onclick="gearSlide(this, 1)">&#8250;</button>
      </div>
    </div>
    <div class="card-body">
      <div class="card-title"><a href="{POST}" style="color:inherit;text-decoration:none;border-bottom:none;">{TITLE}</a></div>
      <div class="card-text" data-slidetext="{KEY}">{BLURB}</div>
      <div class="gear-dots" data-dots="{KEY}"></div>
      <div class="gear-counter" data-counter="{KEY}">1 / {len(SLIDES)}</div>
      <a href="{POST}" class="card-link">{CTA}</a>
    </div>
  </div>
  {END}'''


def homepage(man, apply_):
    p = ROOT / "index.html"
    h = p.read_text(encoding="utf-8")
    c = card(man)
    if MARK in h:
        if END not in h:
            sys.exit("! card block present without its END marker")
        s, e = h.index(MARK), h.index(END) + len(END)
        if h[s:e].rstrip() == c.rstrip():
            return "already in the feed, in the house shape"
        if apply_:
            p.write_text(h[:s] + c.rstrip() + h[e:], encoding="utf-8")
        return "rebuilt to the house shape"
    if ANCHOR not in h:
        sys.exit("! feed anchor not found in index.html")
    if apply_:
        p.write_text(h.replace(ANCHOR, ANCHOR + "\n" + c, 1), encoding="utf-8")
    return "inserted in the top slot"


def sitemap(apply_):
    p = ROOT / "sitemap.xml"
    s = p.read_text(encoding="utf-8")
    loc = f"https://thegrassyissue.com{POST}"
    if f"<loc>{loc}</loc>" in s:
        return "already listed"
    entry = (f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>2026-09-22</lastmod>\n"
             f"    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n")
    if "</urlset>" not in s:
        sys.exit("! sitemap has no </urlset>")
    if apply_:
        p.write_text(s.replace("</urlset>", entry + "</urlset>", 1), encoding="utf-8")
    return "added"


def run(args, label):
    r = subprocess.run([sys.executable] + args, cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"! {label} failed:\n{r.stdout[-800:]}{r.stderr[-800:]}")
    tail = [l for l in r.stdout.strip().splitlines() if l.strip()][-1:]
    print(f"    {label}: {tail[0].strip() if tail else 'ok'}")


def main(apply_):
    man = json.loads((RES / "manifest.json").read_text(encoding="utf-8"))
    print(f"  {len(SLIDES)} slides, Ric Flair leading")
    print("  homepage:", homepage(man, apply_))
    print("  sitemap :", sitemap(apply_))
    if not apply_:
        print("\n  dry run — pass --apply")
        return

    print("\n  regenerating derived artefacts:")
    run(["gen-post-thumbs.py", "--apply"], "gen-post-thumbs")
    run(["generate-search-index.py"], "generate-search-index")

    # ---- VERIFY THE THREE ARTEFACTS THAT MAKE A PAGE DISCOVERABLE ----
    bad = []
    idx = (ROOT / "index.html").read_text(encoding="utf-8")
    if MARK not in idx:
        bad.append("homepage card missing")
    elif idx.index(MARK) - idx.index(ANCHOR) > 400:
        bad.append("card is not in the top slot")
    blk = idx[idx.index(MARK):idx.index(END) + len(END)] if MARK in idx and END in idx else ""
    for need, why in (('data-type="drop"', "no filter type — the feed chips would drop it"),
                      ('class="card-tag grass"', "no green category chip"),
                      ('class="card-link"', "non-house read-more"),
                      ('class="card-title"', "no card-title"),
                      ("gearSlide(this, -1)", "prev arrow has no handler — it would do nothing"),
                      ("gearSlide(this, 1)", "next arrow has no handler — it would do nothing")):
        if need not in blk:
            bad.append(f"homepage card: {why}")
    if blk.count('class="gear-slide"') != len(SLIDES):
        bad.append(f"card renders {blk.count('class=' + chr(34) + 'gear-slide' + chr(34))} slides, "
                   f"expected {len(SLIDES)}")
    # every data-* key must agree, or the caption tracks a different carousel
    for attr in ("data-carousel", "data-slidetext", "data-dots", "data-counter"):
        if f'{attr}="{KEY}"' not in blk:
            bad.append(f"card: {attr} missing or not {KEY!r}")
    if f"1 / {len(SLIDES)}" not in blk:
        bad.append("counter does not declare the real slide count")
    if idx.count(MARK) != 1 or idx.count(END) != 1:
        bad.append(f"{idx.count(MARK)} card blocks, expected 1")
    # every slide image must exist
    for src in re.findall(r'<img src="([^"]+)"', blk):
        if not (ROOT / src.lstrip("/")).is_file():
            bad.append(f"slide image missing: {src}")

    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    if sm.count(f"<loc>https://thegrassyissue.com{POST}</loc>") != 1:
        bad.append("post not in the sitemap exactly once")
    si = json.loads((ROOT / "search-index.json").read_text(encoding="utf-8"))
    if not any(r.get("u") == POST for r in si):
        bad.append("post missing from the search index")
    th = json.loads((ROOT / "data/post-thumbs.json").read_text(encoding="utf-8"))
    if POST not in th:
        bad.append("post missing from post-thumbs")

    if bad:
        sys.exit("! " + "\n    ".join(bad))
    print(f"\n  verified: card in the top slot ({len(SLIDES)} slides, both arrows wired), "
          f"in sitemap, in search index, in post-thumbs")


if __name__ == "__main__":
    main("--apply" in sys.argv)
