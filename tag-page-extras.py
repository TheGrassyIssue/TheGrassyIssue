#!/usr/bin/env python3
"""
tag-page-extras.py — give a taste-tag page a hero and a write-up.
18 September 2026.

WHY
---
Lenny on /brands/tag/gorpcore: "this page is not working correctly ... also
needs a hero shot and a write up."

The tag pages ship as a kicker, a title, a one-line blurb, a criteria box and a
grid of brand cards. That is an index, not a page. Every other editorial surface
on the site opens with a photograph and says something before it starts listing.

WHY THIS IS NOT IN build-brands.py
-----------------------------------
It could be, but TAG_COPY there is a 3-tuple per tag and build-brands.py also
rebuilds 130+ brand pages in the same run. Widening the tuple and re-running the
whole builder to add two blocks to one page is a large blast radius for a small
change. This injector patches only brands/tag/*.html and brands/attr/*.html, is
idempotent, and is safe to re-run after build-brands.py — which is the order it
must run in, because a fresh build drops these blocks.

WHAT IS AND IS NOT INVENTED
----------------------------
Every fact in the write-up is already published on this site, on the brand's own
index entry: Gramicci's 1982 Yosemite origin, Carhartt WIP's European licence
since 1994, Sentinel's Dyneema and Danish textiles from $810, Ghost Golf's 2020
founding and patented magnetic towel, and so on. What is new is the argument
holding them together. No quotes, no prices and no dates that are not already
on the page.

USAGE
    python3 tag-page-extras.py            # dry run
    python3 tag-page-extras.py --apply
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent

# slug -> [(brand label, brand page, image, alt), ...]
# One tile per brand, chosen off a contact sheet rather than by filename —
# people and context where the brand publishes them, product where it does not.
# Salomon took Realtree's seat on this tag in September 2026 and arrived with
# its own localised product shot, so the grid is ten tiles rather than nine.
GALLERY = {
 "gorpcore": [
  ("Agronomy Workshop", "/brands/agronomy-workshop", "/images/gorpcore/agronomy-lifestyle-1.jpg",
   "Agronomy Workshop cap and sunglasses, shot outdoors"),
  ("Gramicci", "/brands/gramicci", "/images/gramicci/earth-tee-a2.jpg",
   "Gramicci tee and climbing-cut trousers worn full-length"),
  ("Left of Field Golf", "/brands/left-of-field-golf", "/images/left-of-field-golf/ig-3.jpg",
   "Two golfers walking a fairway carrying Left of Field bags"),
  ("Odd Ritual", "/brands/odd-ritual", "/images/odd-ritual/02-motus-polo-a2.jpg",
   "Odd Ritual tee and trousers, club in hand"),
  ("Sentinel Golf", "/brands/sentinel-golf", "/images/sentinel-golf/look-2.jpg",
   "A player mid-shot on a links hole, Sentinel Golf"),
  ("Carhartt WIP", "/brands/carhartt-wip", "/images/gorpcore/carhartt-painter-1.jpg",
   "Carhartt WIP washed-black short-sleeve shirt"),
  ("Ghost Golf", "/brands/ghost-golf", "/images/gorpcore/ghost-kovert-1.jpg",
   "Ghost Golf Kovert stand bag"),
  ("Sounder", "/brands/sounder", "/images/gorpcore/sounder-gilet-1.jpg",
   "Sounder fleece gilet"),
  ("Sunday Golf", "/brands/sunday-golf", "/images/gorpcore/sunday-elcamino-1.jpg",
   "Sunday Golf El Camino lightweight carry bag"),
  ("Salomon", "/brands/salomon", "/images/gorpcore/salomon-xt6-1.jpg",
   "Salomon XT-6 trail shoe in walnut, side profile"),
 ],
}

# slug -> (hero src, hero alt, credit, [paragraphs])
EXTRAS = {
 "gorpcore": (
   "/images/tags/gorpcore-hero.jpg",
   "Two golfers in heavy fog, one mid-swing &mdash; technical outerwear weather",
   "Photograph courtesy of Odd Ritual",
   [
    "Gorpcore in golf is less a look than a supply chain. The clothes come from "
    "somewhere else &mdash; a climbing brand, a workwear licence, an outdoor "
    "textile mill &mdash; and arrive on the course already solving a problem. "
    "Gramicci&rsquo;s climbing pants were cut for Yosemite granite in 1982 and "
    "became course staples without the company ever asking them to. Carhartt WIP "
    "has been making workwear-derived apparel in Europe under licence since 1994. "
    "Neither started in golf. Both fit.",

    "The common thread is that the material decision came first. Sentinel builds "
    "walker bags in Minneapolis out of Dyneema and Danish textiles, starting at "
    "$810. Ghost Golf, founded in 2020, designed an accessories line outward from "
    "a patented magnetic towel. Sunday Golf makes carry bags light enough for the "
    "par-three and the casual nine. These are answers to questions about weight, "
    "weather and what a person can carry for four hours, and the styling followed "
    "the answer rather than the other way round.",

    "It travels, too. Odd Ritual came out of Cape Town, Left of Field names every "
    "collection for a stretch of Australian coast, Sounder is British and comes "
    "from the founders of Folk and Urban Golf, Agronomy Workshop works in cotton "
    "out of San Francisco, and Salomon has been making alpine gear in "
    "Annecy since 1947 &mdash; the XT-6 arrived as a trail shoe and got "
    "adopted by everyone else. Ten brands, one shared instinct: dress for "
    "the walk, not the clubhouse.",
   ]),
}

# THE TITLE BLOCK, REBUILT. .bp-head is display:flex with a 28px gap, written
# for a .bp-headtext wrapper that these pages do not have — so the kicker, the
# h1 and the intro became three side-by-side columns and the deck floated off
# to the right of the title. Lenny: "let's make the top better and with a
# cleaner title section." Stacked and centred, with the deck on its own measure
# under the title, and a hairline above the kicker to give the block a top edge.
# Applied to EVERY tag and attribute page, not just the ones with a write-up,
# so the set stays consistent while the rest of the copy is written.
HEAD_CSS = """<style id="tagx-head">
.bp-head{max-width:1200px;margin:0 auto;padding:54px 24px 0;display:block;
  text-align:center;}
.bp-head .bp-kicker{display:block;margin:0 0 16px;opacity:.9;}
.bp-head h1{font-family:var(--serif);font-size:clamp(38px,5vw,60px);line-height:1.04;
  letter-spacing:-.02em;margin:0 0 18px;}
.bp-head .bp-intro{max-width:620px;margin:0 auto;font-family:var(--serif);
  font-size:19px;line-height:1.56;opacity:.82;}
.bp-crumb{max-width:1200px;margin:0 auto;padding:0 24px;}
@media(max-width:820px){
  .bp-head{padding:34px 20px 0;}
  .bp-head .bp-intro{font-size:17px;}
  .bp-crumb{padding:0 20px;}
}
</style>"""

CSS = """<style id="tagx-css">
/* 40px of air under the deck — with the title block now stacked and centred,
   the intro's last line was landing directly on the hero's top border. */
.tagx-hero{max-width:1400px;margin:40px auto 6px;padding:0 32px;}
.tagx-hero img{width:100%;height:auto;display:block;border:.5px solid var(--ink);}
.tagx-credit{font-family:var(--mono);font-size:9px;letter-spacing:.12em;
  text-transform:uppercase;opacity:.45;margin:8px 0 0;}
.tagx-essay{max-width:1400px;margin:0 auto;padding:30px 32px 4px;}
.tagx-essay .tagx-body{max-width:720px;}
.tagx-essay p{font-family:var(--serif);font-size:17px;line-height:1.72;margin:0 0 18px;}

/* THE BRAND GALLERY. Lenny: "add more images from the brands in the post —
   beef it up a bit." One tile per brand, 4:5 so a mix of on-model photography
   and on-white product sits at a single shape, each in a hairline frame so the
   white-background shots read as framed tiles rather than holes in the paper. */
.tagx-gal{max-width:1400px;margin:8px auto 0;padding:26px 32px 0;}
.tagx-gal h2{font-family:var(--serif);font-weight:600;font-size:22px;margin:0 auto 22px;
  width:fit-content;}
.tagx-gal .tagx-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;}
/* One tile per brand, so the count is the tag's count and will not always
   divide by three — gorpcore went from nine to ten when Salomon arrived. A
   last child sitting at 3n+1 is alone on a new row; put it in column two so
   the short row reads as centred rather than left-hanging. Padding the grid
   with a second photo of some brand to square it off would be the wrong fix:
   the grid means one tile per brand. */
.tagx-gal .tagx-grid > *:last-child:nth-child(3n+1){grid-column:2;}
.tagx-gal a{display:block;text-decoration:none;color:inherit;}
.tagx-gal img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block;
  border:.5px solid var(--ink);transition:transform .3s;}
.tagx-gal a:hover img{transform:scale(1.02);}
.tagx-gal .tagx-cap{font-family:var(--mono);font-size:9.5px;letter-spacing:.1em;
  text-transform:uppercase;margin-top:8px;opacity:.65;}
@media(max-width:820px){
  .tagx-hero,.tagx-essay,.tagx-gal{padding-left:20px;padding-right:20px;}
  .tagx-essay p{font-size:16px;}
  .tagx-gal .tagx-grid{grid-template-columns:repeat(2,1fr);gap:12px;}
  /* two columns: the 3n+1 centring rule above is meaningless and would shove
     a tile into the wrong cell, so switch it off */
  .tagx-gal .tagx-grid > *:last-child:nth-child(3n+1){grid-column:auto;}
}
</style>"""


def head_only(html):
    """The title-block restyle, for every tag/attr page. Idempotent."""
    html = re.sub(r'<style id="tagx-head">.*?</style>\s*', "", html, flags=re.S)
    return html.replace("</head>", HEAD_CSS + "\n</head>", 1)


def strip(html):
    """Remove anything a previous run added, so this is idempotent."""
    html = re.sub(r'<style id="tagx-head">.*?</style>\s*', "", html, flags=re.S)
    html = re.sub(r'<style id="tagx-css">.*?</style>\s*', "", html, flags=re.S)
    html = re.sub(r'<div class="tagx-hero".*?</div>\s*', "", html, flags=re.S)
    html = re.sub(r'<section class="tagx-essay".*?</section>\s*', "", html, flags=re.S)
    html = re.sub(r'<section class="tagx-gal".*?</section>\s*', "", html, flags=re.S)
    return html


def build(slug, html):
    src, alt, credit, paras = EXTRAS[slug]
    if not (ROOT / src.lstrip("/")).exists():
        return None, f"hero missing on disk: {src}"
    html = strip(html)

    hero = (f'<div class="tagx-hero">\n'
            f'  <img src="{src}" alt="{alt}" />\n'
            f'  <p class="tagx-credit">{credit}</p>\n'
            f'</div>\n')
    body = "\n".join(f"    <p>{p}</p>" for p in paras)
    essay = (f'<section class="tagx-essay">\n  <div class="tagx-body">\n'
             f'{body}\n  </div>\n</section>\n')

    # after the header block (kicker / h1 / intro), before the criteria box
    m = re.search(r"</header>\s*", html)
    if not m:
        return None, "no </header> anchor"
    gal = ""
    for label, href, src, alt in GALLERY.get(slug, []):
        if not (ROOT / src.lstrip("/")).exists():
            return None, f"gallery image missing: {src}"
        gal += (f'    <a href="{href}"><img src="{src}" alt="{alt}" loading="lazy" />'
                f'<div class="tagx-cap">{label}</div></a>\n')
    if gal:
        gal = ('<section class="tagx-gal">\n  <h2>In the Wild</h2>\n'
               f'  <div class="tagx-grid">\n{gal}  </div>\n</section>\n')

    html = html[:m.end()] + hero + essay + gal + html[m.end():]

    html = html.replace("</head>", HEAD_CSS + "\n" + CSS + "\n</head>", 1)
    return html, "ok"


if __name__ == "__main__":
    apply_ = "--apply" in sys.argv

    # PASS 1 — the title block, on every tag and attribute page.
    heads = 0
    for d in ("tag", "attr"):
        for p in sorted((ROOT / "brands" / d).glob("*.html")):
            if p.stem in EXTRAS:
                continue                    # pass 2 writes the whole head
            out = head_only(p.read_text(encoding="utf-8"))
            if apply_:
                p.write_text(out, encoding="utf-8")
            heads += 1
    print(f"  title block restyled on {heads} page(s)\n")

    # PASS 2 — hero and write-up, where the copy exists.
    done = 0
    for slug in sorted(EXTRAS):
        hit = None
        for d in ("tag", "attr"):
            p = ROOT / "brands" / d / f"{slug}.html"
            if p.exists():
                hit = p
                break
        if not hit:
            print(f"  SKIP {slug} — no page")
            continue
        out, why = build(slug, hit.read_text(encoding="utf-8"))
        if not out:
            print(f"  FAIL {slug} — {why}")
            continue
        words = sum(len(re.sub(r"<[^>]+>", " ", p).split()) for p in EXTRAS[slug][3])
        print(f"  ok   {slug:<16} hero + {len(EXTRAS[slug][3])} paragraphs, {words} words"
              f" + {len(GALLERY.get(slug, []))} gallery tiles")
        if apply_:
            hit.write_text(out, encoding="utf-8")
        done += 1
    print(f"\n  {done} page(s) " + ("updated" if apply_ else "ready — pass --apply"))
