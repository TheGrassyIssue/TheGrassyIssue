#!/usr/bin/env python3
"""wire-hat-towel-edit.py — put The Hat & Towel Edit at the top of the feed and
retire the broken page. 21 September 2026.

REDIRECTS, WITHOUT A CHAIN.
/drops/hats-carousel was already the 301 target for two retired hat URLs:
    /drops/the-hats-and-towels-edit  -> hats-carousel
    /drops/14-hats-from-funky-brands -> hats-carousel
Pointing hats-carousel at the new slug would leave those two hopping twice.
All three are repointed straight at /drops/the-hat-and-towel-edit instead.

The old file is deleted, not left orphaned: with cleanUrls on, leaving
drops/hats-carousel.html on disk means Vercel serves the broken page and the
redirect never fires.

Everything derived is rebuilt by its generator, never hand-edited:
  data/post-thumbs.json  <- gen-post-thumbs.py
  search-index.json      <- generate-search-index.py
  brands/*.html          <- scan-new-brand-mentions --rescan -> build-brands -> build-brand-index

Idempotent. Dry run by default.
"""
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
SLUG = "the-hat-and-towel-edit"
NEW = f"/drops/{SLUG}"
OLD = "/drops/hats-carousel"
ALSO = ["/drops/the-hats-and-towels-edit", "/drops/14-hats-from-funky-brands"]
TODAY = "2026-09-21"
ANCHOR = "<!--TGI-SC-HOME-->"
MARK = "<!-- HAT & TOWEL EDIT -->"
HERO = "/images/hats-towels/hero.jpg"

END = "<!-- /HAT & TOWEL EDIT -->"

# THE HOUSE CARD SHAPE, COPIED FROM ITS NEIGHBOURS, NOT INVENTED.
# The first version used card-kicker + card-readmore and no data-type. On the
# rendered feed that showed as a card with no green category chip sitting
# beside 170 that had one, and an unfiltered card in a filtered feed. Every
# other card is:
#   div.card[data-type]  >  div.card-media[position:relative]
#                             span.card-tag.grass   (the chip, overlaid)
#                             a > img
#                        >  div.card-body
#                             div.card-title > a
#                             div.card-text
#                             a.card-link
CARD = f'''{MARK}
  <div class="card" data-type="drop">
    <div class="card-media" style="position:relative;">
      <span class="card-tag grass">[Drops &amp; Brands]</span>
      <a href="{NEW}">
        <img src="/images/hats-towels/hat-sugarloaf-social-club.jpg" alt="Cotton SSC Arrow Cap from Sugarloaf Social Club" loading="lazy" style="width:100%;display:block;" />
      </a>
    </div>
    <div class="card-body">
      <div class="card-title"><a href="{NEW}" style="color:inherit;text-decoration:none;border-bottom:none;">The Hat &amp; Towel Edit &mdash; 30 Picks From the Independent Golf Brands</a></div>
      <div class="card-text">Eighteen caps and twelve towels, one piece per brand, every price read live from the maker&rsquo;s own store. No beanies, no visors.</div>
      <a href="{NEW}" class="card-link">See all 30 picks &#8599;</a>
    </div>
  </div>
  {END}
'''


def run(args, label):
    r = subprocess.run([sys.executable] + args, cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"! {label} failed:\n{r.stdout[-1200:]}{r.stderr[-1200:]}")
    tail = [l for l in r.stdout.strip().splitlines() if l.strip()][-1:]
    print(f"    {label}: {tail[0].strip() if tail else 'ok'}")


def redirects(apply_):
    p = ROOT / "vercel.json"
    v = json.loads(p.read_text(encoding="utf-8"))
    rs = v["redirects"]
    changed = []
    for src in [OLD] + ALSO:
        hit = next((r for r in rs if r["source"] == src), None)
        if hit:
            if hit["destination"] != NEW:
                changed.append(f"{src}: {hit['destination']} -> {NEW}")
                hit["destination"] = NEW
        else:
            rs.append({"source": src, "destination": NEW, "permanent": True})
            changed.append(f"{src}: added -> {NEW}")
    if apply_ and changed:
        p.write_text(json.dumps(v, indent=2) + "\n", encoding="utf-8")
    return changed or ["redirects already correct"]


def homepage(apply_):
    """Insert the card, or bring an already-inserted one up to the house shape.

    SELF-HEALING, because the first insert used the wrong shape. Returning
    'already in the feed' on any MARK match meant a re-run could not correct
    it. The card is now delimited by MARK...END so the whole block can be
    replaced; a pre-END card is migrated by matching to the end of its div.
    """
    p = ROOT / "index.html"
    h = p.read_text(encoding="utf-8")

    if MARK in h:
        s = h.index(MARK)
        if END in h:
            e = h.index(END, s) + len(END)
        else:                                   # pre-END card — find its close
            m = re.compile(r'\n  </div>\n').search(h, s)
            if not m:
                sys.exit("! card block present but its end could not be located")
            e = m.end() - 1
        if h[s:e].rstrip() == CARD.rstrip():
            return "card already in the feed, in the house shape"
        if apply_:
            p.write_text(h[:s] + CARD.rstrip() + h[e:], encoding="utf-8")
        return "card rebuilt to the house shape (chip + data-type + card-link)"

    if ANCHOR not in h:
        sys.exit("! feed anchor not found in index.html")
    if apply_:
        p.write_text(h.replace(ANCHOR, ANCHOR + "\n" + CARD, 1), encoding="utf-8")
    return "card inserted in the top slot"


def retire_old(apply_):
    f = ROOT / "drops/hats-carousel.html"
    if not f.exists():
        return "old page already removed"
    if apply_:
        f.unlink()
    return "deleted drops/hats-carousel.html (the redirect cannot fire while it exists)"


def drop_stale_thumb(apply_):
    """The first build inherited the donor's masthead, so gen-post-thumbs
    derived the coverage thumb from /images/hat-edit/hero.jpg — the OTHER
    post's picture. The generator never overwrites an existing entry without
    --refresh, and --refresh rewrites all 205, so the entry is deleted and
    re-derived from this post's own hero with no blast radius."""
    p = ROOT / "data/post-thumbs.json"
    t = json.loads(p.read_text(encoding="utf-8"))
    cur = t.get(NEW, {}).get("img")
    if cur == HERO:
        return "post-thumbs already on our hero"
    if cur is None:
        return "no post-thumbs entry yet — the generator will derive one"
    if apply_:
        t.pop(NEW, None)
        p.write_text(json.dumps(dict(sorted(t.items())), indent=1,
                                ensure_ascii=False), encoding="utf-8")
    return f"post-thumbs: dropped stale entry ({cur}) for the generator to re-derive"


def sitemap(apply_):
    p = ROOT / "sitemap.xml"
    s = p.read_text(encoding="utf-8")
    notes = []
    s2 = re.sub(r"\s*<url>(?:(?!</url>).)*" + re.escape(OLD) + r"(?:(?!</url>).)*</url>",
                "", s, flags=re.S)
    if s2 != s:
        notes.append("removed hats-carousel from the sitemap"); s = s2
    if NEW not in s:
        entry = (f"  <url>\n    <loc>https://thegrassyissue.com{NEW}</loc>\n"
                 f"    <lastmod>{TODAY}</lastmod>\n    <changefreq>monthly</changefreq>\n"
                 f"    <priority>0.8</priority>\n  </url>\n")
        s = s.replace("</urlset>", entry + "</urlset>")
        notes.append("added the new slug to the sitemap")
    if apply_ and notes:
        p.write_text(s, encoding="utf-8")
    return notes or ["sitemap already correct"]


def main(apply_):
    for n in redirects(apply_):
        print("  " + n)
    print("  " + homepage(apply_))
    print("  " + retire_old(apply_))
    print("  " + drop_stale_thumb(apply_))
    for n in sitemap(apply_):
        print("  " + n)
    if not apply_:
        print("\n  dry run — pass --apply")
        return

    print("\n  rebuilding derived artefacts:")
    run(["scan-new-brand-mentions.py", "--rescan", "--apply"], "scan-mentions")
    run(["gen-post-thumbs.py", "--apply"], "gen-post-thumbs")
    run(["build-brands.py"], "build-brands")
    run(["build-brand-index.py", "--apply"], "build-brand-index")
    run(["generate-search-index.py"], "generate-search-index")

    # ---- VERIFY THE FINISHED ARTEFACTS ----
    bad = []
    if (ROOT / "drops/hats-carousel.html").exists():
        bad.append("the broken page is still on disk")
    v = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
    for src in [OLD] + ALSO:
        r = next((x for x in v["redirects"] if x["source"] == src), None)
        if not r or r["destination"] != NEW:
            bad.append(f"{src} does not point at {NEW}")
    if any(r["destination"] == OLD for r in v["redirects"]):
        bad.append("something still redirects to the retired slug")

    idx = (ROOT / "index.html").read_text(encoding="utf-8")
    if MARK not in idx:
        bad.append("homepage card missing")
    elif idx.index(MARK) - idx.index(ANCHOR) > 400:
        bad.append("homepage card is not in the top slot")
    if OLD in idx:
        bad.append("homepage still links the retired slug")

    thumbs = json.loads((ROOT / "data/post-thumbs.json").read_text(encoding="utf-8"))
    if NEW not in thumbs:
        bad.append("no post-thumbs entry for the new post")
    elif thumbs[NEW].get("img") != HERO:
        bad.append(f"post-thumbs is {thumbs[NEW].get('img')}, not this post's hero")
    si = json.loads((ROOT / "search-index.json").read_text(encoding="utf-8"))
    if not any(r.get("u") == NEW for r in si):
        bad.append("new post missing from the search index")
    if any(r.get("u") == OLD for r in si):
        bad.append("retired slug still in the search index")

    # nothing published should still link the dead page
    for p in ROOT.rglob("*.html"):
        if "drafts" in p.parts or "research" in p.parts:
            continue
        if OLD in p.read_text(encoding="utf-8", errors="ignore"):
            bad.append(f"{p.relative_to(ROOT)} still links {OLD}")

    if bad:
        sys.exit("! " + "; ".join(bad[:8]))
    print(f"\n  verified: 3 URLs redirect straight to {NEW} with no chain, "
          f"card in the top slot, old page gone, thumbs + search current")


if __name__ == "__main__":
    main("--apply" in sys.argv)
