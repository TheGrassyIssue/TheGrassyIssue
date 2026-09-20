#!/usr/bin/env python3
"""build-wild-spring-dunes.py — drops/on-our-radar-wild-spring-dunes.html.
20 September 2026.

DONOR: drops/lions-municipal-golf-course-austin.html — the house course
deep-dive. It already has the furniture this needs: breadcrumb, drop-header,
21:9 hero, writeup with a sticky sidebar, pull-quote, alternating
section.products with h2.products-hdr, the .tl timeline rows, an FAQ block and
the .more tail.

THE DONOR LEAKS IF YOU LET IT. Lions Muny is an Austin muni with a
desegregation history and a lease fight; none of that belongs on a page about
an East Texas resort course. Donor names are stripped from CSS comments and
the leak guard is SCOPED ABOVE the .more tail, because that tail is supposed
to link other TGI posts — the exact false positive that tripped the Local Rule
build.

EVERY CLAIM IS ATTRIBUTED. The copy lives in research/wild-spring-dunes.json
alongside its source list and a written record of the three places sources
disagreed (yardage, walking policy, the 10th). Nobody from TGI has played the
course, so every judgement of the golf itself is attributed by name to Doak,
Keiser, Abbott or Gavrich. verify() refuses the build if a quote appears on
the page without an attribution marker near it.

THE SOCIAL CLUB BLOCK IS THE POINT OF THE PAGE, EDITORIALLY. Lenny asked for
the link; the reason it works is that the Social Club form already asks how far
you will drive and whether you walk, and this is a walking-only course four
hours from Austin. The guard below requires the link AND requires the reverse
link to exist on the Social Club page, because a one-way cross-link is how
these quietly rot.

Dry run by default.
"""
import json, pathlib, re, sys

import tgi_bands

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/lions-municipal-golf-course-austin.html"
OUT = ROOT / "drops/on-our-radar-wild-spring-dunes.html"
DATA = ROOT / "research/wild-spring-dunes.json"
SOCIAL = ROOT / "events/social-club.html"

SLUG = "on-our-radar-wild-spring-dunes"
TITLE = ("On Our Radar &mdash; Wild Spring Dunes, the Tom Doak Course "
         "in the Piney Woods")
DESC = ("Wild Spring Dunes opened all 18 holes to the public on 8 September 2026 "
        "&mdash; a Tom Doak course on 2,400 acres of former East Texas timber land, "
        "walking only, $275. What it is, how it happened, and whether the drive "
        "from Austin is justified.")

# Donor identity. Anything here found ABOVE the .more tail is a leak.
#
# EACH ENTRY IS A WORD-BOUNDARY PATTERN, AND THE CASE-SENSITIVE ONES SAY SO.
# The first cut listed the bare string "UT " and matched it case-insensitively,
# so it fired on "about ", "but " and "cut " and reported a donor leak that did
# not exist. Same error as matching "Panther" with a bare "pant" during the
# trousers sweep: a substring is not a word. An acronym like UT only means
# anything in capitals, so it is matched with case ON.
DONOR_MARKS = [
    (r"\bLions Muni\b",        re.I),
    (r"\bLions Municipal\b",   re.I),
    (r"\bMuny\b",              re.I),
    (r"\bTenison\b",           re.I),
    (r"\bdesegregat\w*",       re.I),
    (r"\blease fight\b",       re.I),
    (r"\bUT\b",                0),      # case-sensitive: the university, not "but"
    (r"lions-muny",             re.I),
    (r"lions-municipal",        re.I),
    (r"\bEnfield\b",           re.I),
    (r"\bJim Crow\b",          re.I),
]

# Every quotation on this page must sit near one of these attribution markers.
ATTRIBUTIONS = ["Doak", "Keiser", "Abbott", "Gavrich", "Messerall", "Martin",
                "D CEO", "GOLF", "GolfPass", "broker"]

EXTRA_CSS = """
/* The Social Club call-out this page adds. The donor has nothing like it. A class emitted with no rule is the .axxa-note bug from Found Golf,
   so verify() checks each of OWN_CLASSES has a rule in the finished file. */
.wsd-sc{border:1px solid rgba(var(--ink-rgb),.2);padding:30px 32px;margin:40px 0 8px;
  background:rgba(var(--ink-rgb),.02)}
.wsd-sc-hdr{font-family:var(--mono);font-size:10px;letter-spacing:.14em;
  text-transform:uppercase;color:var(--grass);margin-bottom:12px}
.wsd-sc h3{font-size:24px;font-weight:400;margin:0 0 12px;line-height:1.2}
.wsd-sc p{font-size:16px;line-height:1.66;margin:0 0 18px}
.wsd-sc a.wsd-sc-cta{display:inline-block;font-family:var(--mono);font-size:10px;
  letter-spacing:.12em;text-transform:uppercase;border-bottom:1px solid var(--ink);
  padding-bottom:2px}
.wsd-src{font-family:var(--mono);font-size:10px;letter-spacing:.06em;
  line-height:2;opacity:.75}
.wsd-src a{border-bottom:1px solid rgba(var(--ink-rgb),.3)}
"""
EXTRA_CSS = EXTRA_CSS + tgi_bands.BAND_CSS
OWN_CLASSES = ["wsd-sc", "wsd-sc-hdr", "wsd-sc-cta", "wsd-src"]

BANDS = {
    "band-hero": "Sandy bunkering running into scrub beneath a wall of East Texas pine",
    "band-1": "A spring-fed creek and one of the property&rsquo;s bridges",
    "band-2": "A green set above a ravine, with the crossing below",
    "band-3": "Golfers crossing a boardwalk through the pines",
    "band-4": "A Wild Spring Dunes caddie on the course",
    "band-5": "A green and flag against the pine wall",
}
CREDIT = "Photography courtesy of Wild Spring Dunes"


def head_block(donor_head):
    h = donor_head
    subs = [
      (r"<title>.*?</title>", f"<title>{TITLE} &mdash; The Grassy Issue</title>"),
      (r'(<meta name="description" content=")[^"]*(")', rf"\g<1>{DESC}\g<2>"),
      (r'(<meta property="og:url" content="https://thegrassyissue\.com/drops/)[^"]*(")',
       rf"\g<1>{SLUG}\g<2>"),
      (r'(<meta property="og:title" content=")[^"]*(")', rf"\g<1>{TITLE}\g<2>"),
      (r'(<meta property="og:description" content=")[^"]*(")', rf"\g<1>{DESC}\g<2>"),
      (r'(<meta property="og:image" content="https://thegrassyissue\.com/images/)[^"]*(")',
       r"\g<1>wild-spring-dunes/band-hero.jpg\g<2>"),
      (r'(<meta name="twitter:title" content=")[^"]*(")', rf"\g<1>{TITLE}\g<2>"),
      (r'(<meta name="twitter:description" content=")[^"]*(")', rf"\g<1>{DESC}\g<2>"),
      (r'(<link rel="canonical" href="https://thegrassyissue\.com/drops/)[^"]*(")',
       rf"\g<1>{SLUG}\g<2>"),
      (r'("headline":\s*")[^"]*(")', rf"\g<1>{TITLE}\g<2>"),
      (r'("description":\s*")[^"]*(")', rf"\g<1>{DESC}\g<2>"),
      (r'("url":\s*"https://thegrassyissue\.com/drops/)[^"]*(")', rf"\g<1>{SLUG}\g<2>"),
      (r'("@id":\s*"https://thegrassyissue\.com/drops/)[^"]*(")', rf"\g<1>{SLUG}\g<2>"),
      (r'("datePublished":\s*")[^"]*(")', r"\g<1>2026-09-20\g<2>"),
      (r'("dateModified":\s*")[^"]*(")', r"\g<1>2026-09-20\g<2>"),
    ]
    for pat, rep in subs:
        h = re.sub(pat, rep, h, flags=re.S)
    for pat, flags in DONOR_MARKS:
        h = re.sub(rf"/\*[^*]*?{pat}.*?\*/", "", h, flags=re.S | re.I)

    # THE DONOR'S STRUCTURED DATA IS ABOUT A DIFFERENT GOLF COURSE.
    # This was the leak the guard caught: head_block rewrote the meta tags and
    # the Article schema but left an `about: GolfCourse` block naming Lions
    # Municipal, its Enfield Rd address and its phone number, plus a whole
    # FAQPage about Jim Crow and a UT lease. Invisible on the page, served to
    # Google as fact. Both blocks are replaced, not patched.
    h = re.sub(r',\s*"about":\s*\{.*?\n\s*\}\s*\n\s*\}', "\n}", h, flags=re.S)
    h = re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context"[^<]*?"@type":\s*"FAQPage".*?</script>',
               faq_schema(), h, flags=re.S)
    h = h.replace("</head>", about_schema() + "</head>") if "GolfCourse" not in h else h

    i = h.rfind("</style>")
    if i < 0:
        sys.exit("! donor head has no <style> block to extend")
    return h[:i] + EXTRA_CSS + h[i:]


def about_schema():
    """Wild Spring Dunes as a GolfCourse, replacing the donor's."""
    return ('<script type="application/ld+json">\n{\n'
            '  "@context": "https://schema.org",\n'
            '  "@type": "GolfCourse",\n'
            '  "name": "Wild Spring Dunes",\n'
            '  "address": {"@type": "PostalAddress",\n'
            '    "streetAddress": "21043 US-259",\n'
            '    "addressLocality": "Mount Enterprise",\n'
            '    "addressRegion": "TX", "postalCode": "75681",\n'
            '    "addressCountry": "US"},\n'
            '  "url": "https://www.wildspringdunes.com/",\n'
            '  "publicAccess": true,\n'
            '  "isAccessibleForFree": false\n}\n</script>\n')


def faq_schema():
    d = json.loads(DATA.read_text(encoding="utf-8"))
    def clean(s):
        return (s.replace("&ldquo;", "\u201c").replace("&rdquo;", "\u201d")
                 .replace("&rsquo;", "\u2019").replace("&mdash;", "\u2014")
                 .replace("&amp;", "&").replace('"', "'"))
    qs = ",\n".join(
        '    {"@type":"Question","name":"%s","acceptedAnswer":'
        '{"@type":"Answer","text":"%s"}}' % (clean(q), clean(a))
        for q, a in d["faq"])
    return ('<script type="application/ld+json">\n{\n'
            '  "@context": "https://schema.org",\n  "@type": "FAQPage",\n'
            '  "mainEntity": [\n' + qs + '\n  ]\n}\n</script>')


def faq_block(rows):
    """The visible FAQ. verify-post.py wants exactly one on a page."""
    items = "\n".join(
        f'    <details class="faq-q"><summary>{q}</summary>\n'
        f'      <p>{a}</p></details>' for q, a in rows)
    return ('<section class="products">\n'
            '  <h2 class="products-hdr">Before You Book</h2>\n'
            f'  <div class="faq">\n{items}\n  </div>\n</section>\n\n')


def band(name, first=False):
    """Delegates to tgi_bands so the 21:9-crop bug is fixed in one place."""
    return tgi_bands.band(ROOT, f"/images/wild-spring-dunes/{name}.jpg",
                          BANDS[name], credit=CREDIT if first else None,
                          masthead=first)


def sidebar(d):
    # ALL the rows. An earlier cut showed seven here and repeated them in an
    # inline box below the opening paragraphs, which is the same table twice.
    rows = d["facts"]
    det = "\n".join(
        f'      <div class="sidebar-detail"><span class="l">{k}</span>'
        f'<span>{v}</span></div>' for k, v in rows)
    tags = "\n".join(f'        <span class="hashtag">#{t}</span>' for t in
                     ["WildSpringDunes", "TomDoak", "TexasGolf",
                      "PineyWoods", "OnOurRadar"])
    return f'''  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Short Version</div>
{det}
      <a href="https://www.wildspringdunes.com/golf" target="_blank" rel="noopener" class="sidebar-cta">Book a Tee Time &rarr;</a>
      <a href="/events/social-club" class="sidebar-cta" style="margin-top:8px;">The TGI Social Club &rarr;</a>
      <a href="/field-guide" class="sidebar-cta" style="margin-top:8px;">The Austin Golf Guide &rarr;</a>
      <div class="hashtags">
{tags}
      </div>
    </div>
  </aside>
'''


def writeup(paras, hdr=None, side="", extra=""):
    h = f'    <h2 class="products-hdr" style="margin-top:0;">{hdr}</h2>\n' if hdr else ""
    body = "\n".join(f"    <p>{p}</p>" for p in paras)
    return ('<div class="writeup">\n  <div class="writeup-body">\n'
            + h + body + "\n" + extra + "  </div>\n" + side + "</div>\n\n")


def pull(q):
    return ('<div class="pull-quote">\n'
            f'  <p class="pull-quote-inner">&ldquo;{q["text"]}&rdquo;'
            f'<span class="pull-quote-attr">&mdash; {q["attr"]}</span></p>\n'
            '</div>\n\n')


def timeline(rows):
    body = "\n".join(
        f'    <div class="tl-row"><div class="tl-year">{y}</div>'
        f'<div class="tl-text">{t}</div></div>' for y, t in rows)
    return ('<section class="products">\n'
            '  <h2 class="products-hdr">How It Happened</h2>\n'
            f'  <div class="tl">\n{body}\n  </div>\n</section>\n\n')


def social_block(sc):
    return ('<section class="products">\n'
            '  <div class="wsd-sc">\n'
            '    <div class="wsd-sc-hdr">The Grassy Issue Social Club</div>\n'
            f'    <h3>{sc["hdr"]}</h3>\n'
            f'    <p>{sc["body"]}</p>\n'
            f'    <a href="{sc["href"]}" class="wsd-sc-cta">{sc["cta"]}</a>\n'
            '  </div>\n</section>\n\n')


def sources(links):
    items = "\n".join(
        f'    <div><a href="{u}" target="_blank" rel="noopener">{t}</a></div>'
        for t, u in links)
    return ('<section class="products">\n'
            '  <h2 class="products-hdr">Where This Came From</h2>\n'
            '  <div class="sec-note">Nobody from TGI has played it yet. Every '
            'judgement of the golf below is attributed to the person who made it.</div>\n'
            f'  <div class="wsd-src">\n{items}\n  </div>\n</section>\n\n')


def build():
    d = json.loads(DATA.read_text(encoding="utf-8"))
    t = d["take"]
    donor = DONOR.read_text(encoding="utf-8")

    head = head_block(donor[:donor.find("</head>")])
    body_start = donor.find("<body")
    nav = donor[body_start:donor.find('<div class="breadcrumb">')]
    tail = donor[donor.find('<div class="more">'):]

    p = head + "</head>\n" + nav
    p += ('<div class="breadcrumb">\n'
          '  <a href="/#feed">Feed</a> / <a href="/#feed">Field Notes</a> / '
          'On Our Radar\n</div>\n\n')
    p += ('<header class="drop-header">\n'
          f'  <h1>{TITLE}</h1>\n'
          '  <div class="drop-meta">\n'
          '    <span>Mount Enterprise, Texas</span><span class="dot"></span>\n'
          '    <span>Opened 8 September 2026</span><span class="dot"></span>\n'
          '    <span>Reported 20 September 2026</span>\n'
          '  </div>\n</header>\n\n')
    p += band("band-hero", first=True)

    # The Take — opening argument, with the facts box and the sticky sidebar
    p += writeup([f"<strong>{t[0]}</strong>", t[1], t[2]], side=sidebar(d))
    p += pull(d["pullquote"])

    p += band("band-1")
    p += writeup([t[3], t[4], t[5], t[6]],
                 hdr="The Office Worker and the Timber Trucks")

    p += band("band-2")
    p += writeup([t[7], t[8], t[9], t[10], t[11]], hdr="A Cold Email to Tom Doak")

    p += timeline(d["timeline"])

    p += band("band-3")
    p += writeup([t[12], t[13], t[14], t[15]], hdr="What Doak Built")

    p += band("band-4")
    p += writeup([t[16], t[17], t[18]], hdr="What It Gives Texas")

    p += band("band-5")
    p += writeup([t[19], t[20], t[21]], hdr="Is It a Trip? Yes &mdash; With Conditions")

    p += faq_block(d["faq"])
    p += social_block(d["social_club"])
    p += sources(d["links"])
    p += tail
    return p


def verify(path):
    """READ THE FINISHED FILE."""
    h = path.read_text(encoding="utf-8")
    d = json.loads(DATA.read_text(encoding="utf-8"))
    bad = []

    i = h.find('<div class="more">')
    ours = h[:i] if i > 0 else h

    for pat, flags in DONOR_MARKS:
        m = re.search(pat, ours, flags)
        if m:
            at = max(0, m.start() - 60)
            bad.append(f"donor content leaked: {m.group(0)!r} "
                       f"in ...{re.sub(chr(92)+'s+', ' ', ours[at:m.end()+60])}...")

    for b in BANDS:
        if f"/images/wild-spring-dunes/{b}.jpg" not in h:
            bad.append(f"{b} not on the page")
        if not (ROOT / f"images/wild-spring-dunes/{b}.jpg").exists():
            bad.append(f"{b}.jpg not on disk")

    for c in OWN_CLASSES:
        if f'class="{c}"' not in h and f'"{c} ' not in h:
            bad.append(f"{c} declared but never used")
        if f".{c}{{" not in h.replace(" ", "").replace("\n", ""):
            bad.append(f"{c} used but has no CSS rule")

    # EVERY QUOTED PASSAGE MUST BE ATTRIBUTED, IN ITS OWN PARAGRAPH.
    #
    # The first version of this check looked for an attribution word within 320
    # characters either side of the quotation. That is a proximity proxy, not a
    # rule: a fabricated quote dropped between two properly-sourced paragraphs
    # passes, because the neighbours supply the names. Fault injection is what
    # showed it up — and only after the injection itself was fixed, because the
    # first attempt appended a paragraph that build() never renders and so
    # proved nothing either.
    #
    # The real editorial rule is tighter and easier to check: the paragraph that
    # carries a quotation names who said it. So the unit is the <p>, not a
    # character window.
    paras = re.findall(r"<p>(.*?)</p>", ours, re.S)
    quoted = [x for x in paras if "&ldquo;" in x]
    n_quotes = sum(x.count("&ldquo;") for x in paras)
    if n_quotes < 10:
        bad.append(f"only {n_quotes} quotations — the reporting is thin")
    for x in quoted:
        if not any(a in x for a in ATTRIBUTIONS):
            flat = re.sub(r"<[^>]+>", "", x)
            bad.append(f"paragraph carries a quotation but names nobody: "
                       f"{flat[:90]}...")

    # the Social Club link, both directions
    if 'href="/events/social-club"' not in ours:
        bad.append("no Social Club link in the body")
    if ours.count('href="/events/social-club"') < 2:
        bad.append("Social Club linked only once (want sidebar + call-out)")
    if SOCIAL.exists():
        s = SOCIAL.read_text(encoding="utf-8")
        if f"/drops/{SLUG}" not in s:
            bad.append("Social Club page does not link back — cross-link is one-way")

    # house rules
    if re.search(r"\bworth\b", ours, re.I):
        bad.append("the word 'worth' is on the page")

    # the two numbers sources disagreed on must appear as the resolved value
    if "6,962" not in ours:
        bad.append("the rated yardage (6,962) is missing")
    if "walking-only" not in ours and "walking only" not in ours:
        bad.append("the walking-only policy is missing")

    bad += tgi_bands.verify_bands(ROOT, h)

    if "</html>" not in h:
        bad.append("page is truncated")
    return bad


def main(apply_):
    page = build()
    if not apply_:
        print(f"  would write {OUT.relative_to(ROOT)}  ({len(page):,} bytes)")
        print("\n  dry run — pass --apply")
        return
    OUT.write_text(page, encoding="utf-8")
    bad = verify(OUT)
    if bad:
        sys.exit("! " + "\n! ".join(bad))
    h = OUT.read_text(encoding="utf-8")
    words = len(re.sub(r"<[^>]+>", " ", h[:h.find('<div class="more">')]).split())
    print(f"  wrote {OUT.relative_to(ROOT)}  ({len(h):,} bytes)")
    print(f"  {h.count('drop-hero-img')} bands, {h.count('<h2')} headings, "
          f"{len(re.findall(r'&ldquo;', h))} quotations, ~{words} words")


if __name__ == "__main__":
    main("--apply" in sys.argv)
