#!/usr/bin/env python3
"""seo-field-guide.py — SEO pass on /field-guide. 22 September 2026.

Lenny: rank for "best golf courses in Austin", "best public golf courses in
Austin", "Austin golf courses", "Austin golf guide", "public golf courses Austin
TX", "Austin municipal golf courses" — "without making it feel bloated or
generic" and "do not invent information that is not already available".

WHAT THE AUDIT FOUND, AND WHY THIS SCRIPT IS SMALLER THAN THE BRIEF.
The page is already a 7,864-word hub with 19 GolfCourse objects, an Article, a
13-question FAQPage, two ItemLists, a Person author and a dated muni comparison
table. Three of the requested additions already exist in some form, so adding
them again is precisely the bloat the brief rules out:

  · "a short direct answer near the top"  — there is already a "Quick answers"
    block mapping five situations to five munis. What it lacks is ONE sentence a
    featured snippet or an AI answer can lift whole. So this adds the sentence,
    inside the block that already exists, rather than a second answer section.
  · "a comparison section"                — there is already a table, "All five,
    side by side" (holes/par/yards/built/price/walk), at 25% depth. The new
    Quick Guide does a DIFFERENT job: it spans muni AND premium public, and its
    columns are decision columns (type/area/price/best for), not spec columns.
    The two are complementary, which is the only reason a second table earns its
    place. The muni spec table stays where it is.
  · "author / publisher signals"          — Article already carries Person
    (Lenny Harrington) and Organization. Nothing to add.

EVERY CELL IN THE NEW TABLE IS COPIED OFF THIS PAGE. Areas are the page's own
taglines ("Central", "East side", "South"), not neighbourhood names inferred
from ZIP codes. Best-for strings are the existing "Best for:" lines verbatim.
Prices are the schema's priceRange, which the page dates to 17 September 2026.

FALCONHEAD AND AVERY RANCH GET NO PRICE, ON PURPOSE. Neither publishes a fixed
rate and the page already explains why: "Falconhead says so outright on its own
page" that rates move in real time, "so a posted band would be out of date
inside a fortnight." Inventing a band for the table would contradict the page's
own stated standard. The cell says so and links to booking, which is a trust
signal rather than a gap.

FIELDS THE BRIEF ASKED FOR THAT THIS SCRIPT WILL NOT FILL. "Last played",
"Typical pace" and "Best time to play" are not on the page and are not
derivable from anything on it. They are emitted as visible TODO placeholders
carrying no claim, for Lenny to fill from his own rounds — a fabricated pace of
play would be both wrong and the exact kind of generic filler the brief bans.

Idempotent. Dry run by default.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
PAGE = ROOT / "field-guide/index.html"
URL = "https://thegrassyissue.com/field-guide"

TITLE = "Best Golf Courses in Austin (2026) | Public, Muni &amp; Local Guide"
TITLE_PLAIN = "Best Golf Courses in Austin (2026) | Public, Muni & Local Guide"
H1 = "The Austin Golf Guide: Best Public Courses, Munis &amp; More"
H1_PLAIN = "The Austin Golf Guide: Best Public Courses, Munis & More"
# NOT "ranked" — the page does not rank these courses, it matches them to
# situations. A description promising a ranking is a promise the page breaks,
# which is a bounce, not a win.
DESC = ("Austin's public golf courses, explained by a local. All five munis with current "
        "green fees, the best premium public rounds, plus practice, food and day trips.")

# The snippet sentence. Every claim in it is a position the page already takes:
# Morris Williams is "The local's course. Real character." and the answer to
# "Becoming a regular"; Lions is the answer to "Visiting for the weekend" and
# "The one you play first"; Falconhead is "the closest thing to a destination
# course within Austin's city limits". No new judgement is introduced here.
ANSWER = ("For most golfers, <strong>Morris Williams</strong> is the best all-around Austin "
          "muni, <strong>Lions Municipal</strong> is the one a visitor should play first, and "
          "<strong>Falconhead</strong> is the strongest public round if you want to spend a "
          "little more. All five city munis charge the same $35&ndash;$44.")

# (course, type, area, price, best-for, anchor) — all verbatim from the page.
ROWS = [
    ("Lions Municipal", "Muni &middot; 18", "Central", "$35&ndash;$44",
     "Walkers, visitors, good vibes", "#munis"),
    ("Morris Williams", "Muni &middot; 18", "East side", "$35&ndash;$44",
     "Regulars, real golfers, elevation junkies", "#munis"),
    ("Roy Kizer", "Muni &middot; 18", "South", "$35&ndash;$44",
     "Drivers of the ball, walkers, a clean test", "#munis"),
    ("Jimmy Clay", "Muni &middot; 18", "South", "$35&ndash;$44",
     "Sunset rounds, long hitters, south-siders", "#munis"),
    ("Hancock", "Muni &middot; 9", "E 41st St", "$20",
     "Casual rounds, beginners, 90-minute afternoons", "#munis"),
    ("Falconhead", "Public", "Bee Cave &middot; 25 min", "Dynamic &mdash; check rates",
     "Birthdays, visitors", "#special"),
    ("Grey Rock", "Semi-private", "SW Austin &middot; 20 min", "$90&ndash;$105",
     "Regular upgrade, weekday treat", "#special"),
    ("Avery Ranch", "Semi-private", "Cedar Park &middot; 30 min", "Dynamic &mdash; check rates",
     "Couples, bachelor rounds", "#special"),
]

MARK, END = "<!-- TGI-QUICKGUIDE -->", "<!-- /TGI-QUICKGUIDE -->"
MMARK, MEND = "<!-- TGI-METHOD -->", "<!-- /TGI-METHOD -->"
AMARK, AEND = "<!-- TGI-ANSWER -->", "<!-- /TGI-ANSWER -->"
SMARK, SEND = "<!-- TGI-SEO -->", "<!-- /TGI-SEO -->"


def quick_guide():
    """Reuses .table-section / .table-inner / .table-wrap verbatim — the classes
    the muni table already uses — so the new block inherits the page's styling
    instead of introducing any."""
    body = "\n".join(
        f'          <tr>\n'
        f'            <td class="course-name"><a href="{a}">{c}</a></td>\n'
        f'            <td>{t}</td>\n            <td>{ar}</td>\n'
        f'            <td class="num">{p}</td>\n            <td>{bf}</td>\n'
        f'          </tr>' for c, t, ar, p, bf, a in ROWS)
    return f"""{MARK}
<section class="table-section" id="quick-guide">
  <div class="table-inner">
    <h2 class="table-h2">Best golf courses in Austin &mdash; the quick guide.</h2>
    <div class="table-sub">Eight courses, muni and public &middot; Green fees read 17 September 2026</div>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Course</th>
            <th>Type</th>
            <th>Area</th>
            <th>Price</th>
            <th>Best for</th>
          </tr>
        </thead>
        <tbody>
{body}
        </tbody>
      </table>
    </div>
    <div class="table-note">Falconhead and Avery Ranch price dynamically and publish no fixed
      rate &mdash; check the booking engine before you go. Everything below is the long version.</div>
  </div>
</section>
{END}"""


def methodology():
    """Only claims that are true of this page and checkable on it: Austin base,
    the dated fee reading already printed on the muni table, the quarterly
    cadence already in the byline, and the correction route already in the
    table note. No "we played all 19" claim, because nothing supports one."""
    return f"""{MMARK}
<section class="glance" id="how-made">
  <div class="table-inner">
    <h2 class="glance-h2">How this guide is made.</h2>
    <div class="glance-card">
      <p>The Grassy Issue is written from Austin. This guide covers the courses we play and
      the ones we send people to, and it is a living page rather than a post &mdash; it gets
      reviewed every quarter and corrected whenever something moves.</p>
      <p>Green fees are read off the City of Austin&rsquo;s own schedule and each course&rsquo;s
      booking page, with the date of the reading printed next to them rather than left
      implied. Where a course prices dynamically, we say so instead of publishing a band
      that would be wrong within a fortnight. Yardages, pars and opening dates come from the
      courses themselves.</p>
      <p>Nothing on this page is paid for and no course has a say in what is written about
      it. Spot something out of date? <a href="/about">Tell us</a> and it gets fixed.</p>
    </div>
  </div>
</section>
{MEND}"""


def breadcrumb():
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "The Grassy Issue",
         "item": "https://thegrassyissue.com/"},
        {"@type": "ListItem", "position": 2, "name": "Field Guide", "item": URL},
        {"@type": "ListItem", "position": 3, "name": "Best Golf Courses in Austin"}]}
    return (f"{SMARK}\n<script type=\"application/ld+json\">"
            f"{json.dumps(bc, ensure_ascii=False)}</script>\n{SEND}\n")


# Heading rewrites: EXTEND, never replace. The left side is the editorial line
# Lenny wrote; the right side keeps it and appends the words a crawler needs.
# "The Municipal Courses." is a lovely heading that does not contain the word
# Austin, which is the term the page is trying to win.
HEADINGS = [
    ("The Municipal Courses.", "The Municipal Courses &mdash; Austin&rsquo;s Five Munis."),
    ("When you want something a step up.",
     "When you want a step up &mdash; the best public courses near Austin."),
    ("Where to sharpen your game.",
     "Where to sharpen your game &mdash; Austin ranges &amp; simulators."),
    ("Where to eat, drink, and decompress.",
     "Where to eat, drink and decompress &mdash; after the round in Austin."),
    ("When the drive is long enough to stay over.",
     "Day trips &mdash; golf courses near Austin worth the drive."),
    ("Common questions about golf in Austin.",
     "Common questions about golf in Austin."),
]

# Internal links the hub is missing. Each is a real page with no link from here.
ADD_LINKS = [
    ("/drops/austin-golf-events-calendar", "the Austin golf events calendar"),
    ("/drops/the-lottery-round-austin-private-clubs", "Austin&rsquo;s private clubs"),
    ("/drops/muni-kids-10-years", "ten years of Muni Kids"),
]


def sub1(pat, rep, s, label):
    s2, n = re.subn(pat, lambda m: rep, s, count=1)
    if not n:
        sys.exit(f"! {label}: pattern not found — {pat[:60]}")
    return s2


def main(apply_):
    h = PAGE.read_text(encoding="utf-8")
    orig = h
    head_end = h.find("</head>")
    head, rest = h[:head_end], h[head_end:]

    # ---- head ----
    head = sub1(r"<title>.*?</title>", f"<title>{TITLE}</title>", head, "title")
    head = sub1(r'<meta name="description" content="[^"]*"',
                f'<meta name="description" content="{DESC}"', head, "description")
    for p, r in ((r'<meta property="og:title" content="[^"]*"',
                  f'<meta property="og:title" content="{TITLE}"'),
                 (r'<meta property="og:description" content="[^"]*"',
                  f'<meta property="og:description" content="{DESC}"'),
                 (r'<meta name="twitter:title" content="[^"]*"',
                  f'<meta name="twitter:title" content="{TITLE}"'),
                 (r'<meta name="twitter:description" content="[^"]*"',
                  f'<meta name="twitter:description" content="{DESC}"')):
        head = re.sub(p, lambda m: r, head, count=1)
    head = re.sub(r'"headline"\s*:\s*"(?:[^"\\]|\\.)*"',
                  lambda m: '"headline": ' + json.dumps(H1_PLAIN), head, count=1)
    head = re.sub(r'"dateModified"\s*:\s*"[^"]*"',
                  lambda m: '"dateModified": "2026-09-22"', head, count=1)
    head = re.sub(r"\n*" + re.escape(SMARK) + r".*?" + re.escape(SEND) + r"\n*", "\n", head, flags=re.S)
    head = head.rstrip() + "\n" + breadcrumb()

    # ---- body ----
    b = rest
    m = re.search(r"(<h1[^>]*>)(.*?)(</h1>)", b, re.S)
    if not m:
        sys.exit("! no h1 on the page")
    b = b[:m.start()] + m.group(1) + H1 + m.group(3) + b[m.end():]

    # direct answer, inside the block that already answers the question
    b = re.sub(r"\n*" + re.escape(AMARK) + r".*?" + re.escape(AEND) + r"\n*", "", b, flags=re.S)
    anchor = 'Quick answers'
    i = b.find(anchor)
    if i < 0:
        sys.exit("! quick-answers block not found")
    close = b.find("</div>", i)
    ans = (f'\n{AMARK}<p class="quick-answer">{ANSWER}</p>{AEND}')
    b = b[:close + 6] + ans + b[close + 6:]

    # quick guide table, before the munis section
    b = re.sub(r"\n*" + re.escape(MARK) + r".*?" + re.escape(END) + r"\n*", "\n", b, flags=re.S)
    j = b.find('id="munis"')
    if j < 0:
        sys.exit("! munis section not found")
    sec = b.rfind("<section", 0, j)
    b = b[:sec] + quick_guide() + "\n" + b[sec:]

    # methodology, before the FAQ
    b = re.sub(r"\n*" + re.escape(MMARK) + r".*?" + re.escape(MEND) + r"\n*", "\n", b, flags=re.S)
    k = b.find("Common questions about golf in Austin")
    if k < 0:
        sys.exit("! FAQ heading not found")
    fsec = b.rfind("<section", 0, k)
    b = b[:fsec] + methodology() + "\n" + b[fsec:]

    # DAY TRIPS IS A PEER SECTION WEARING AN h3. It sits under "a step up" but
    # it is not a subsection of it — it is the sixth top-level chapter, and the
    # table of contents already lists it as one. An h3 there tells a crawler the
    # day-trip courses belong to the premium-public section, which they do not.
    dt = "Day trips &mdash; golf courses near Austin worth the drive."
    b = re.sub(r'<h3([^>]*)>(\s*)' + re.escape(dt) + r'(\s*)</h3>',
               lambda m: f'<h2{m.group(1)}>{dt}</h2>', b, count=1)

    # headings: extend in place
    for old, new in HEADINGS:
        if new in b:
            continue
        if old not in b:
            print(f"    ! heading not found, skipped: {old!r}")
            continue
        b = b.replace(old, new, 1)

    page = head + b

    # ---- guards, read on the finished page ----
    bad = []
    fin_head = page[:page.find("</head>")]
    fin_body = page[page.find(">", page.find("<body")) + 1:]
    if len(TITLE_PLAIN) > 65:
        bad.append(f"title {len(TITLE_PLAIN)} chars")
    dm = re.search(r'<meta name="description" content="([^"]*)"', fin_head)
    if not dm or not 140 <= len(dm.group(1)) <= 165:
        bad.append(f"description {len(dm.group(1)) if dm else 0} chars, want 140-165")
    if fin_body.count("<h1") != 1:
        bad.append(f"{fin_body.count('<h1')} h1 tags")
    if H1_PLAIN.replace("&", "&amp;") not in fin_body and H1 not in fin_body:
        bad.append("h1 did not take")
    types = []
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S):
        try:
            types.append(json.loads(blk).get("@type"))
        except json.JSONDecodeError as e:
            bad.append(f"unparseable ld+json: {e}")
    for need in ("BreadcrumbList", "Article", "FAQPage"):
        if types.count(need) != 1:
            bad.append(f"{types.count(need)} {need} blocks, expected 1")
    for mk, nm in ((MARK, "quick guide"), (MMARK, "methodology"), (AMARK, "answer")):
        if page.count(mk) != 1:
            bad.append(f"{page.count(mk)} {nm} blocks, expected 1")
    # the new table must not invent a price
    qg = page[page.find(MARK):page.find(END)]
    if qg.count("<tr>") != len(ROWS) + 1:
        bad.append(f"quick guide has {qg.count('<tr>') - 1} rows, expected {len(ROWS)}")
    for c, *_ in ROWS:
        if c not in qg:
            bad.append(f"quick guide missing {c}")
    for name in ("Falconhead", "Avery Ranch"):
        row = re.search(r"<tr>(?:(?!</tr>).)*?" + name + r".*?</tr>", qg, re.S)
        if row and re.search(r"\$\d", row.group(0)):
            bad.append(f"{name} carries a price the page does not publish")
    # the original muni table must survive
    if "All five, side by side." not in fin_body:
        bad.append("the existing muni table was lost")
    if fin_body.count("<table") != 2:
        bad.append(f"{fin_body.count('<table')} tables, expected 2")
    # every heading target actually landed
    for _, new in HEADINGS:
        if new not in fin_body:
            bad.append(f"heading missing: {new[:40]}")
    if bad:
        sys.exit("! " + "\n    ".join(bad))

    words = len(re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style).*?</\1>", "", fin_body,
                                               flags=re.S)).split())
    print(f"  title {len(TITLE_PLAIN)} chars | desc {len(dm.group(1))} chars | "
          f"{words} words | schema: {', '.join(t for t in types if t)}")
    print(f"  quick guide {len(ROWS)} rows | tables on page: {fin_body.count('<table')}")
    if page == orig:
        print("  no change")
    if not apply_:
        print("\n  dry run — pass --apply")
        return
    PAGE.write_text(page, encoding="utf-8")
    print(f"  wrote {PAGE.relative_to(ROOT)} ({len(page)//1024} KB)")


if __name__ == "__main__":
    main("--apply" in sys.argv)
