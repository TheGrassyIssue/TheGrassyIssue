#!/usr/bin/env python3
"""beef-up-casualist.py — depth pass on /drops/brand-to-know-casualist.
21 September 2026.

Lenny: "let's beef up this post ... I want to get onto the first page of google.
ALso needs a new hero shot."  Target agreed: the British / UK golf brand
category, not the brand name (we already hold page one for that).

WHAT THIS IS NOT. It is not more products. Casualist's whole catalogue is 23
items, 21 in stock, and the page already carries 17 of them; the only thing
missing is a gift card. Padding the product grid would add words and no answers.

WHAT IT IS. Two things the page did not have and no competing page has either.

1. THE BRAND IS NOT FROM LONDON.
   It started as Casual Pro in MELBOURNE and announced the move to London on
   2 April 2024, in a post that says out loud that UK golf is the most
   buttoned-up market it could have picked. A brand that CHOSE Britain is a far
   better answer to "is this a British golf brand" than a brand that happened
   to be born there, and it is the fact the category listicles do not have.

2. AN HONEST ANSWER TO THE CATEGORY QUESTION.
   Designed in London, made in Portugal, founded in Australia. "British" is
   genuinely contested here, so the page answers it properly instead of
   implying one. That section is also where this post joins the rest of TGI's
   UK coverage, which is the cluster the category query actually rewards.

A FACTUAL CORRECTION SHIPS WITH IT.
The live page says Reboul "renamed the brand from Casual Pro in 2023". That
cannot be right: the April 2024 move post is signed "The Casual Pro team", so
the brand was still Casual Pro a year after the date we gave. The rename is
re-dated to what the sources actually support — Casual Pro trading by September
2023, still Casual Pro in April 2024, Casualist thereafter.

SECTION SHELL IS PER-PAGE, NOT UNIVERSAL.
The band and pull-quote markup was lifted from the Vuori page, and the section
shell came with it: <section class="writeup">. On THIS page .writeup is
"display:grid;grid-template-columns:2fr 1fr" — it is the two-column shell that
holds the Details sidebar. Dropping prose into it put the photograph in the
left column and the paragraphs in the right, with a column of dead space down
the page. Every other prose block here is <section class="products"> wrapping a
<div class="writeup-body">, so that is what these use. Copy the component, but
check the shell it lives in: a class name means whatever the local stylesheet
says it means. Caught by rendering, not by any guard.

MARKER DISCIPLINE. New sections use data-btk="prose". btk-template.py drops any
data-btk value it does not special-case, and "prose" is one of the two
writer-owned markers that survive. A new marker invented for this job would
vanish the next time the template runs over the page.

Idempotent — every insert is keyed to a marker comment. Dry run by default.
"""
import datetime
import html as H
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
PAGE = ROOT / "drops/brand-to-know-casualist.html"

MARK_ORIGIN = "<!-- TGI-CASUALIST-ORIGIN -->"
MARK_BRITISH = "<!-- TGI-CASUALIST-BRITISH -->"

NEW_HERO = "/images/casualist/btk-hero-2026.jpg"
OLD_HERO = "/images/casualist/btk-hero.jpg"

TITLE = ("Casualist &mdash; The Australian Brand That Became a British "
         "Golf Label")
DESC = ("Casualist designs in London and makes in Portugal &mdash; but it "
        "started life as Casual Pro in Melbourne and moved to the UK in April "
        "2024. A full look at the brand, its catalogue and what &ldquo;British "
        "golf brand&rdquo; actually means, with prices read on 21 September 2026.")


# --------------------------------------------------------------- new sections
ORIGIN = f'''{MARK_ORIGIN}
<section class="products" data-btk="prose">
  <h2 class="products-hdr sec">From Melbourne to London</h2>
  <div class="writeup-body">

  <p>Casualist is not a London brand that grew up in London. It is an
  Australian one that moved. On 2 April 2024 the brand &mdash; still trading as
  Casual Pro &mdash; posted that it had gone &ldquo;from the sunny shores of
  Melbourne, Australia, to the historic streets of London, UK.&rdquo; The post
  is signed by the Casual Pro team, and it is blunt about the trade being
  made.</p>

  <div class="drop-hero tgi-band is-port"><div class="drop-hero-img tgi-free"><img src="/images/casualist/band-coast.jpg" alt="Casualist &mdash; mockneck tee photographed on a shingle beach under an English sky" loading="lazy" /></div>
  <div class="tgi-band-credit">Photography courtesy of Casualist</div>
</div>

  <p>Australian and American golf, the brand wrote, is &ldquo;all about kicking
  back&rdquo; &mdash; less fuss about dress codes, more room for a label built
  on jokes and soft collars. Britain was the opposite bet.</p>

  <div class="pull-quote">
  <p class="pull-quote-inner">&ldquo;things are a bit more buttoned-up in the UK. There, tradition still holds sway, and golfers tend to stick to more formal attire&rdquo;<span class="pull-quote-attr">&mdash; the Casual Pro team, announcing the move, 2 April 2024</span></p>
</div>

  <h3>Why that matters to the clothes</h3>

  <p>A brand that moves toward the strictest dress codes in the game has to
  decide what it is willing to lose. What Casualist kept is the humour &mdash;
  the team signed off that a good sense of humour &ldquo;can beat even the
  gloomiest English weather&rdquo; &mdash; and what it added is the part that
  gets you through the gate: collars, merino, pleats, Portuguese make. The
  Grazer Cardigan Vest at &pound;185 and the Pleated Golf Trousers at &pound;160
  are not Melbourne pieces. They are what the move cost, and they are the two
  things on the site most likely to be mistaken for old British golf.</p>

  <h3>The old name never fully left</h3>

  <p>The rename came later, and the brand never scrubbed the first one. The
  &pound;38 Casual Pro Snapback is still the oldest thing in the catalogue and
  still carries the original logo. The Facebook page is still filed under
  casualproclothing. The Windbreaker Coach Jacket carries CASUAL PRO across the
  shoulders and, underneath in small type, <em>master of none, enthusiast of
  many</em> &mdash; the same phrase The Wedgies used to describe the brand's
  philosophy when Elie Reboul went on the show in May 2024. That jacket is the
  photograph at the top of this page.</p>
  </div>
</section>
'''

BRITISH = f'''{MARK_BRITISH}
<section class="products" data-btk="prose">
  <h2 class="products-hdr sec">Is Casualist a British Golf Brand?</h2>
  <div class="writeup-body">

  <p>Partly, and the honest answer is more useful than a yes. Casualist is
  designed in London, made mostly in Portugal, priced in pounds, and founded in
  Melbourne. Which of those makes a brand British depends on what you are
  actually asking.</p>

  <h3>Designed in Britain</h3>

  <p>Yes, and specifically West London &mdash; the Two Tone Course Cap prints
  it under the words Leisure Goods. The house line is that fabrics are picked
  for &ldquo;how they actually feel after a full round, not just how they
  photograph,&rdquo; which is a British weather argument whether or not it is
  framed as one.</p>

  <div class="drop-hero tgi-band is-port"><div class="drop-hero-img tgi-free"><img src="/images/casualist/band-links.jpg" alt="Casualist &mdash; Weekend Pique Polo photographed on heath and gorse" loading="lazy" /></div>
  <div class="tgi-band-credit">Photography courtesy of Casualist</div>
</div>

  <h3>Made in Britain</h3>

  <p>No. Most pieces are made in Portugal, which is where a great many European
  golf and knitwear labels have their cut-and-sew, and the brand says so plainly
  on its own about page rather than leaving it to be discovered.</p>

  <h3>British-owned</h3>

  <p>The brand is run out of West London by its founder, Elie Reboul, and
  arrived from Australia in 2024. If the question behind the question is
  whether buying it keeps money in a small independent rather than a
  multinational, the answer is yes &mdash; it is one person's brand with 23
  products.</p>

  <h3>Where it sits among the UK independents</h3>

  <p>Casualist belongs to a specific cohort: small British labels that treat
  golf clothing as clothing first. <a href="/brands/manors">Manors</a> is
  the most established of them and the most overtly heritage.
  <a href="/brands/sounder">Sounder</a>, also London, runs colder and more
  technical. <a href="/brands/fyfe-golf">Fyfe</a> works the accessory end,
  <a href="/brands/bunker-mentality">Bunker Mentality</a> the loud end from
  Nottinghamshire, and <a href="/brands/royal-albartross">Royal Albartross</a>
  the shoe end. Casualist's position in that group is the softest collar and
  the driest joke. The whole set is in
  <a href="/brands">our brand index</a>.</p>
  </div>
</section>
'''

NEW_FAQ = [
 ("Where is Casualist from?",
  "London now, Melbourne originally. The brand began as Casual Pro in Australia "
  "and announced its move to the UK on 2 April 2024. It is based in West London."),
 ("Is Casualist a British golf brand?",
  "Designed in Britain, made in Portugal, founded in Australia. It is a British-based "
  "independent rather than a British-manufactured one, and the brand is open about "
  "the Portuguese make on its own about page."),
 ("Why did Casualist move to the UK?",
  "The brand's own explanation, in April 2024, was that Australian and American golf "
  "is relaxed about dress codes while in the UK &ldquo;tradition still holds sway.&rdquo; "
  "It moved toward the stricter market on purpose."),
 ("What does &ldquo;master of none, enthusiast of many&rdquo; mean?",
  "It is the brand's own line, printed in small type on the back of the Windbreaker "
  "Coach Jacket. The Wedgies used the same phrase to describe the Casual Pro philosophy "
  "when Elie Reboul appeared on the show in May 2024."),
]


def add_band_css(h):
    """THE MARKUP AND ITS STYLESHEET TRAVEL TOGETHER.

    The band markup was copied from the Vuori page, which carries BAND_CSS
    because tgi_bands.py put it there. Copying the divs without the rules gave
    four classes with no CSS — .tgi-band, .tgi-free, .is-port, .tgi-band-credit
    — so the bands rendered in the fixed 21:9 hero box that .tgi-free exists to
    escape, cropping most of both portraits away. verify-post.py caught it
    ("every class used has a CSS rule"), which is precisely why that check
    exists: an implied rule is indistinguishable from a forgotten one.
    """
    if ".drop-hero.tgi-band" in h:
        return h, "band CSS already present"
    from tgi_bands import BAND_CSS
    if "</style>" not in h:
        sys.exit("! no <style> block to extend")
    return h.replace("</style>", BAND_CSS.rstrip() + "\n</style>", 1), "band CSS injected"


def swap_hero(h):
    if NEW_HERO in h:
        return h, "hero already swapped"
    if OLD_HERO not in h:
        sys.exit("! old hero not found — page structure changed")
    h = h.replace(f'<img class="drop-hero-img" src="{OLD_HERO}"',
                  f'<img class="drop-hero-img" src="{NEW_HERO}"', 1)
    h = h.replace('alt="Casualist &mdash; lookbook photograph"',
                  'alt="Two golfers walking up a parkland fairway in Casual Pro '
                  'windbreakers, the brand\'s original name across their backs"', 1)
    # og/twitter images point at the masthead too
    h = h.replace(f"https://thegrassyissue.com{OLD_HERO}",
                  f"https://thegrassyissue.com{NEW_HERO}")
    return h, "hero swapped to btk-hero-2026.jpg"


def fix_rename_date(h):
    """THE CORRECTION. 'renamed ... in 2023' is contradicted by a post signed
    'The Casual Pro team' in April 2024."""
    old = ("He renamed the brand from Casual Pro in 2023 because the name "
           "needed to grow up")
    if old not in h:
        return h, "rename-date sentence not found (already corrected?)"
    new = ("He renamed the brand from Casual Pro because the name needed to "
           "grow up &mdash; the move post of April 2024 is still signed by the "
           "Casual Pro team, so the change came after that")
    return h.replace(old, new, 1), "corrected the 2023 rename date"


def insert_sections(h):
    notes = []
    # both go after the opening take/story section, before In the Wild
    anchor = '<section class="products" data-btk="wild">'
    if anchor not in h:
        sys.exit("! 'In the Wild' section not found — cannot place new sections")
    for mark, block, label in ((MARK_ORIGIN, ORIGIN, "Melbourne to London"),
                               (MARK_BRITISH, BRITISH, "Is Casualist British")):
        if mark in h:
            notes.append(f"{label} already present")
            continue
        h = h.replace(anchor, block + "\n" + anchor, 1)
        notes.append(f"{label} section inserted")
    return h, notes


def extend_faq(h):
    added = [q for q, _a in NEW_FAQ if f"<summary>{q}</summary>" not in h]
    if not added:
        return h, "FAQ already extended"
    rows = "".join(
        f'\n    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>'
        for q, a in NEW_FAQ if q in added)
    h = h.replace('  </div>\n</section>', rows + '\n  </div>\n</section>', 1) \
         if False else re.sub(r'(<details[^>]*class="faq-q">(?:(?!</details>).)*</details>)(\s*</div>)',
                              lambda m: m.group(1) + rows + m.group(2), h, count=1, flags=re.S)
    return h, f"{len(added)} FAQ entries added"


def sync_faq_schema(h):
    """The FAQPage block must list exactly the questions the page shows, or the
    rich result disagrees with the document and Google drops it."""
    qs = [(H.unescape(re.sub(r"<[^>]+>", "", q)),
           H.unescape(re.sub(r"<[^>]+>", "", a)))
          for q, a in re.findall(r'<summary>(.*?)</summary><p>(.*?)</p>', h, re.S)]
    import json
    ent = [{"@type": "Question", "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qs]

    def repl(m):
        blob = json.loads(m.group(1))
        if isinstance(blob, dict) and blob.get("@type") == "FAQPage":
            blob["mainEntity"] = ent
            return ('<script type="application/ld+json">'
                    + json.dumps(blob, ensure_ascii=False, indent=2)
                    + "</script>")
        return m.group(0)

    h2 = re.sub(r'<script type="application/ld\+json">(.*?)</script>', repl, h,
                flags=re.S)
    return h2, f"FAQ schema synced to {len(qs)} questions"


def retitle(h):
    notes = []
    plain_t = H.unescape(re.sub(r"<[^>]+>", "", TITLE))
    plain_d = H.unescape(re.sub(r"<[^>]+>", "", DESC))
    h = re.sub(r"<title>[^<]*</title>",
               f"<title>{plain_t} &mdash; The Grassy Issue</title>", h, count=1)
    h = re.sub(r'(<meta name="description" content=")[^"]*(")',
               lambda m: m.group(1) + plain_d + m.group(2), h, count=1)
    for prop in ("og:title", "twitter:title"):
        h = re.sub(rf'(<meta (?:property|name)="{prop}" content=")[^"]*(")',
                   lambda m: m.group(1) + plain_t + m.group(2), h, count=1)
    for prop in ("og:description", "twitter:description"):
        h = re.sub(rf'(<meta (?:property|name)="{prop}" content=")[^"]*(")',
                   lambda m: m.group(1) + plain_d + m.group(2), h, count=1)
    h = re.sub(r"(<h1[^>]*>).*?(</h1>)", lambda m: m.group(1) + TITLE + m.group(2),
               h, count=1, flags=re.S)
    # THE OLD TITLE EXISTS IN TWO ENCODINGS.
    # The H1 writes it with &mdash;; the breadcrumb writes it with a literal
    # U+2014. Matching only the entity form left the old headline sitting in
    # the breadcrumb of a page whose H1 had changed — the render is what showed
    # it, not the guards. Replace both spellings, and assert neither survives.
    for dash in ("&mdash;", "\u2014"):
        h = h.replace(f"Casualist {dash} The London Brand That Outgrew Its Own Name",
                      plain_t)
    notes.append("title, meta, og/twitter, H1 and breadcrumb updated")

    # The sidebar carried the same 2023 claim the body just corrected.
    h = h.replace("<span>Casual Pro, 2023</span>",
                  "<span>Casual Pro, Melbourne</span>")
    notes.append("sidebar 'Was' row re-dated to Casual Pro, Melbourne")

    # Article schema: headline/description/dateModified
    today = datetime.date.today().isoformat()
    for key, val in (("headline", plain_t), ("description", plain_d),
                     ("dateModified", today)):
        h = re.sub(rf'("{key}":\s*")[^"]*(")',
                   lambda m, _v=val: m.group(1) + _v + m.group(2), h, count=1)
    notes.append(f"Article schema headline/description/dateModified={today}")
    return h, notes


def main(apply_):
    h = original = PAGE.read_text(encoding="utf-8")
    notes = []
    h, n = add_band_css(h); notes.append(n)
    h, n = swap_hero(h); notes.append(n)
    h, n = fix_rename_date(h); notes.append(n)
    h, ns = insert_sections(h); notes += ns
    h, n = extend_faq(h); notes.append(n)
    h, ns = retitle(h); notes += ns
    h, n = sync_faq_schema(h); notes.append(n)

    for x in notes:
        print("  " + x)
    if not apply_:
        print("\n  dry run — pass --apply")
        return

    PAGE.write_text(h, encoding="utf-8")

    # ---- VERIFY THE FINISHED PAGE ----
    hh = PAGE.read_text(encoding="utf-8")
    body = hh[hh.find("<body"):]
    bad = []

    words = len(re.sub(r"\s+", " ", H.unescape(re.sub(
        r"<[^>]+>", " ", re.sub(r'<(script|style)\b.*?</\1>', "", body, flags=re.S)
    ))).split())
    before = len(re.sub(r"\s+", " ", H.unescape(re.sub(
        r"<[^>]+>", " ", re.sub(r'<(script|style)\b.*?</\1>', "", original[original.find("<body"):], flags=re.S)
    ))).split())
    # Only meaningful on a FIRST build. A re-run inserts nothing (every step is
    # marker-keyed), so demanding growth every time would make the script fail
    # precisely because it is correctly idempotent. Guard the guard.
    first_build = any("inserted" in n for n in notes)
    if first_build and words <= before:
        bad.append(f"word count did not grow: {before} -> {words}")
    if words < 2000:
        bad.append(f"page is {words} words — under the depth this pass is for")

    for must, label in ((MARK_ORIGIN, "origin section"), (MARK_BRITISH, "british section"),
                        (NEW_HERO, "new hero"), ("band-coast.jpg", "coast band"),
                        ("band-links.jpg", "links band")):
        if must not in hh:
            bad.append(f"{label} missing from the finished page")
    if OLD_HERO in hh:
        bad.append("old hero still referenced")
    if re.search(r"renamed the brand from Casual Pro in 2023", hh):
        bad.append("the 2023 rename claim survived")
    if "Casual Pro, 2023" in hh:
        bad.append("the sidebar still says 'Casual Pro, 2023'")
    # the old headline, in EITHER dash encoding, must be gone everywhere
    for dash in ("&mdash;", "\u2014"):
        if f"Casualist {dash} The London Brand That Outgrew" in hh:
            bad.append(f"old headline survives with {dash!r}")
    if hh.count("<h1") != 1:
        bad.append(f"{hh.count('<h1')} h1 tags")
    h3s = len(re.findall(r"<h3", body))
    if h3s < 5:
        bad.append(f"only {h3s} h3s — the heading tree is still flat")

    # every internal link must resolve to a real page on disk
    for href in sorted(set(re.findall(r'href="(/(?:brands|drops)/[^"#]*)"', body))):
        p = ROOT / (href.lstrip("/") + ".html")
        if href.rstrip("/") == "/brands":
            p = ROOT / "brands/index.html"
        if not p.is_file():
            bad.append(f"internal link 404: {href}")

    # FAQ document and schema must agree
    doc_q = re.findall(r"<summary>(.*?)</summary>", hh, re.S)
    sch = re.search(r'"@type":\s*"FAQPage".*?"mainEntity":\s*(\[.*?\n\s*\])', hh, re.S)
    if not sch:
        bad.append("FAQPage schema not found")
    else:
        import json
        n_sch = len(json.loads(sch.group(1)))
        if n_sch != len(doc_q):
            bad.append(f"FAQ mismatch: {len(doc_q)} on the page, {n_sch} in schema")

    if re.search(r"\bworth\b", body, re.I):
        bad.append("the word 'worth' appears in the copy")

    if bad:
        sys.exit("! " + "; ".join(bad))

    print(f"\n  verified: {before} -> {words} words, {h3s} h3s, "
          f"{len(doc_q)} FAQ entries in page and schema, all internal links resolve")


if __name__ == "__main__":
    main("--apply" in sys.argv)
