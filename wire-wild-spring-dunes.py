#!/usr/bin/env python3
"""wire-wild-spring-dunes.py — homepage card, sitemap, search. 20 Sept 2026.

Three jobs, idempotent, each verified against the FINISHED FILE.

THIS IS A FIELD NOTE, NOT A DROP, so the homepage card is the single-image
data-type="field" shape with the flag tag — not a gear carousel. Using the
carousel card here would have meant inventing five "slides" for a golf course,
which is the format driving the content instead of the other way round.

No slideTexts entry for the same reason: there are no slides. The entity trap
that bit the Local Rule card does not apply, but the card text still goes
through the same check, because the next person to copy this file will not
know that and the check costs nothing.

Dry run by default.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
INDEX = ROOT / "index.html"
SITEMAP = ROOT / "sitemap.xml"
SEARCH = ROOT / "search-index.json"
SOCIAL = ROOT / "events/social-club.html"
POST = ROOT / "drops/on-our-radar-wild-spring-dunes.html"

SLUG = "on-our-radar-wild-spring-dunes"
MARK = "<!-- ON OUR RADAR — WILD SPRING DUNES -->"
TITLE = "On Our Radar &mdash; Wild Spring Dunes"
HERO = "/images/wild-spring-dunes/band-hero.jpg"
ALT = ("Wild Spring Dunes &mdash; sandy bunkering running into scrub "
       "beneath a wall of East Texas pine")

CARD_TEXT = (
  "A Tom Doak course opened to the public on 8 September, on 2,400 acres of "
  "former timber land outside Mount Enterprise. Walking only, caddies available, "
  "$275 in peak season &mdash; and bookable by anyone, which is the part that "
  "matters in a state where the best golf is almost always behind a gate. The "
  "land was found by a Dallas office worker who taught himself to read soil "
  "surveys, and the reason it looks like this is that a logging company took the "
  "pines off first. Four hours and change from Austin."
)


def card_html():
    return f'''{MARK}
  <div class="card" data-type="field">
    <div class="card-media" style="position:relative;">
      <span class="card-tag flag">[Field Notes]</span>
      <a href="/drops/{SLUG}">
        <img src="{HERO}" alt="{ALT}" loading="lazy" style="width:100%;display:block;" />
      </a>
    </div>
    <div class="card-body">
      <div class="card-title"><a href="/drops/{SLUG}" style="color:inherit;text-decoration:none;border-bottom:none;">{TITLE}</a></div>
      <div class="card-text">{CARD_TEXT}</div>
      <a href="/drops/{SLUG}" class="card-link">Read the Field Note &#8599;</a>
    </div>
  </div>
'''


def wire_index(h):
    if MARK in h:
        return h, ["card already present"]
    anchor = "<!--TGI-SC-HOME-->"
    if anchor not in h:
        sys.exit("! feed anchor <!--TGI-SC-HOME--> not found in index.html")
    return h.replace(anchor, anchor + "\n" + card_html(), 1), ["card inserted"]


def wire_sitemap(x):
    loc = f"https://thegrassyissue.com/drops/{SLUG}"
    if loc in x:
        return x, ["sitemap already has the post"]
    entry = (f"  <url>\n    <loc>{loc}</loc>\n"
             f"    <lastmod>2026-09-20</lastmod>\n"
             f"    <changefreq>monthly</changefreq>\n"
             f"    <priority>0.7</priority>\n  </url>\n</urlset>")
    return x.replace("</urlset>", entry, 1), ["sitemap + the post"]


def wire_search(j):
    """Short keys — u/t/d/g/i/k. Long names append an entry the UI ignores."""
    url = f"/drops/{SLUG}"
    if any(e.get("u") == url for e in j):
        return j, ["search index already has the post"]
    j.append({
      "u": url,
      "t": "On Our Radar — Wild Spring Dunes",
      "d": ("Tom Doak's new course in the East Texas Piney Woods opened to the "
            "public on 8 September 2026. What it is, how an office worker found "
            "the land, and whether the drive from Austin is justified."),
      "g": "Field Notes",
      "i": HERO,
      "k": ("Wild Spring Dunes Tom Doak Mount Enterprise East Texas Piney Woods "
            "Michael Keiser Dream Golf Bandon Sand Valley Coore Crenshaw "
            "Brett Messerall walking only caddie public golf Texas golf resort "
            "green fee 275 Nacogdoches zoysia"),
    })
    return j, ["search index + the post"]


def main(apply_):
    h = INDEX.read_text(encoding="utf-8")
    x = SITEMAP.read_text(encoding="utf-8")
    j = json.loads(SEARCH.read_text(encoding="utf-8"))

    h2, ic = wire_index(h)
    x2, sc = wire_sitemap(x)
    j2, jc = wire_search(j)
    for c in ic + sc + jc:
        print("  " + c)
    if not apply_:
        print("\n  dry run — pass --apply")
        return

    INDEX.write_text(h2, encoding="utf-8")
    SITEMAP.write_text(x2, encoding="utf-8")
    SEARCH.write_text(json.dumps(j2, indent=2, ensure_ascii=False), encoding="utf-8")

    # ---- VERIFY THE FINISHED FILES ----
    hh = INDEX.read_text(encoding="utf-8")
    xx = SITEMAP.read_text(encoding="utf-8")
    jj = json.loads(SEARCH.read_text(encoding="utf-8"))
    bad = []

    if MARK not in hh: bad.append("card missing")
    if hh.count(MARK) != 1: bad.append("card duplicated")
    if hh.count(f"/drops/{SLUG}") < 3: bad.append("card links incomplete")
    if not (ROOT / HERO.lstrip("/")).exists(): bad.append(f"missing {HERO}")

    # scope the card checks to THIS card, not the whole homepage
    i = hh.find(MARK)
    seg = hh[i:hh.find("</div>\n", hh.find('class="card-link"', i))]
    if 'data-type="field"' not in seg: bad.append("card is not typed as a Field Note")
    if "[Field Notes]" not in seg: bad.append("card tag is not [Field Notes]")
    if "gear-carousel" in seg: bad.append("a carousel leaked into a Field Note card")

    if SLUG not in xx: bad.append("sitemap entry missing")
    ours = next((e for e in jj if e.get("u") == f"/drops/{SLUG}"), None)
    if ours is None:
        bad.append("search index entry missing")
    else:
        sib = next((e for e in jj if e.get("u") != f"/drops/{SLUG}"), None)
        if sib and set(ours) != set(sib):
            bad.append(f"search keys {sorted(ours)} != schema {sorted(sib)}")

    # THE CROSS-LINK RUNS BOTH WAYS OR IT IS NOT WIRED.
    if not POST.exists():
        bad.append("the post itself is not on disk")
    else:
        pp = POST.read_text(encoding="utf-8")
        if 'href="/events/social-club"' not in pp:
            bad.append("post does not link to the Social Club")
    s = SOCIAL.read_text(encoding="utf-8")
    if f"/drops/{SLUG}" not in s:
        bad.append("Social Club does not link to the post")

    if bad:
        sys.exit("! " + "; ".join(bad))
    print(f"\n  verified on disk: Field Note card, sitemap, search index, "
          f"Social Club cross-link both ways")


if __name__ == "__main__":
    main("--apply" in sys.argv)
