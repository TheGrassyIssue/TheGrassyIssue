#!/usr/bin/env python3
"""/work-with-us — the page that turns a ranking into a conversation.

WHY THIS EXISTS (9/17/26). TGI already ranks on page one for brand-name searches
its own subjects run — Read The Green #3, Cloud & Wind #3, Sentinel #4,
Kingfisher #4, Odd Ritual #5. The most qualified visitor the site gets is a brand
employee who googled their own name and landed on 2,000 words about their own
products. Until now there was nothing telling that person TGI was open to working
together: no /advertise, no /partner, no media kit, and an /about page that never
uses the words partner, sponsor or collaborate. The only route in was a personal
Gmail in a mailto.

EDITORIAL-FIRST, NO RATE CARD (Lenny's call). No prices, no ad formats, no
audience numbers. Two reasons: the traffic figures live in GA4 and GoatCounter
where Claude cannot reach them, and publishing a rate card locks pricing in
public before the first conversation has happened. The page says what TGI is,
what it is open to, and — the part that matters — what it will not do.

THE ETHOS SECTION IS THE POINT, NOT A DISCLAIMER. Lenny pulled the Live Giveaways
block off the homepage the same day this was written because it pointed readers at
other companies' promotions for nothing in return. For an index of 131 independent
brands, being explicit that coverage is not for sale is a reason to work with TGI
rather than a limitation on it. Do not soften that section into marketing copy.

DELIBERATELY NOT IN THE TOP NAV. The main nav is reader-facing. A "Work With Us"
item sitting next to Field Guide tells every reader the site is for sale. This
goes in the FOOTER sitewide, on the 131 brand pages where the qualified visitor
actually lands, and in a line from /about. That is full coverage without turning
the masthead into a sales page.

CHASSIS: cloned from about.html, which is the newest hand-built page and already
carries the nav, search box, typography chain and GA4/GoatCounter tags.
"""
import re, os, sys, json

SRC = "about.html"
OUT = "work-with-us.html"
URL = "/work-with-us"
TITLE = "Work With Us &mdash; The Grassy Issue"
DESC = ("How The Grassy Issue works with golf brands — what we are open to, what we do not sell, "
        "and how to start a conversation.")

BODY = """
<div class="breadcrumb"><a href="/">Feed</a><span>/</span>Work With Us</div>

<header class="drop-header">
  <h1>Work With Us</h1>
</header>
<div class="writeup" style="grid-template-columns:1fr;">
  <div class="writeup-body" style="max-width:720px">

    <p>If you make something and you have found your way here, it is probably because you searched
    your own brand name and this site came up. That happens a fair amount now, and for a long time
    there was nothing on the other end of it. This page is the other end of it.</p>

    <p><strong>The Grassy Issue</strong> is a golf publication run out of Austin, Texas. It covers
    the municipal scene here and the independent side of golf apparel and equipment everywhere else.
    The <a href="/brands" style="border-bottom:1px solid var(--ink)">Brand Index</a> currently runs
    to {nbrands} brands and roughly {kwords} thousand words of coverage written about them. More on
    who is behind it is <a href="/about" style="border-bottom:1px solid var(--ink)">on the About
    page</a>.</p>

    <h2 style="font-family:var(--serif);font-weight:600;font-size:24px;margin:32px 0 14px">Who reads it</h2>

    <p>People who walk. The audience skews toward golfers who care what a thing is made of and where
    it came from, who play municipal courses more often than private ones, and who are as likely to
    be looking at a headcover from a two-person studio as at anything with a tour logo on it. There
    is a heavy Austin concentration and a long tail everywhere else.</p>

    <p>If you want numbers before a conversation, ask and you will get them. They are not printed
    here because a figure on a page goes stale the week after it is written.</p>

    <h2 style="font-family:var(--serif);font-weight:600;font-size:24px;margin:32px 0 14px">What we are open to</h2>

    <p><strong>Sending product.</strong> The simplest one and usually the best. Gear gets shot in
    Austin, on real courses, in the weather it was built for. Seeded product does not buy coverage,
    but it does mean the photography is ours rather than a lookbook frame everybody else is running.</p>

    <p><strong>Sponsored Field Notes.</strong> A piece of reporting a brand underwrites &mdash; a
    course, a trip, an event, a making-of. The brand pays for the work to exist. The brand does not
    approve the copy. Anything sponsored is labelled as sponsored, on the page, where a reader sees
    it before they read it.</p>

    <p><strong>Newsletter and social placements.</strong> Straightforward, clearly marked.</p>

    <p><strong>Longer partnerships.</strong> A season, a capsule, a recurring slot. These work best
    when there is an actual editorial reason for them, so they tend to start as a conversation about
    the work rather than about a placement.</p>

    <h2 style="font-family:var(--serif);font-weight:600;font-size:24px;margin:32px 0 14px">What we do not sell</h2>

    <p><strong>Placement in a roundup.</strong> Every brand in an Edit is there because it earned
    the slot. No exceptions, and no paid entries mixed in with chosen ones.</p>

    <p><strong>Approval over what gets written.</strong> Facts get checked with you gladly &mdash;
    prices, materials, founding dates, spellings. Opinions do not.</p>

    <p><strong>Display advertising.</strong> There are no banners here and there is not going to be
    a banner slot.</p>

    <p><strong>Links to somebody else's promotion.</strong> Sweepstakes, giveaways, affiliate
    round-ups for gear nobody here has looked at &mdash; these send a reader away from the site for
    nothing and they are not something TGI carries.</p>

    <p><strong>Coverage of one brand at another's expense.</strong> Comparisons stay on the facts.
    Nobody pays to have a competitor described badly.</p>

    <p>None of that is posturing about purity. It is the reason the brand pages rank: they read as
    reporting, so people trust them, so Google surfaces them, so you ended up here.</p>

    <h2 style="font-family:var(--serif);font-weight:600;font-size:24px;margin:32px 0 14px">Getting in touch</h2>

    <p>Email is best, and it reaches one person rather than an inbox:
    <a href="mailto:Lenny@thegrassyissue.com?subject=Working%20with%20The%20Grassy%20Issue"
       style="border-bottom:1px solid var(--ink)">Lenny@thegrassyissue.com</a>.</p>

    <p>Useful things to put in a first email: what you make, what you are trying to do, and roughly
    when. If there is already coverage of you on the site, a link to it saves a step. If there is
    not, that is fine too &mdash; a good part of the Index started with somebody sending a note.</p>

    <p class="sig">&mdash; Lenny Harrington<br><span>Austin, Texas</span></p>

  </div>
</div>
"""

SCHEMA = {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "name": "Work With Us",
    "url": "https://thegrassyissue.com" + URL,
    "description": re.sub(r"&mdash;", "—", DESC),
    "isPartOf": {"@type": "WebSite", "name": "The Grassy Issue",
                 "url": "https://thegrassyissue.com"},
    "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
        {"@type": "ListItem", "position": 2, "name": "Work With Us"}]},
    "publisher": {"@type": "Organization", "name": "The Grassy Issue",
                  "url": "https://thegrassyissue.com",
                  "founder": {"@type": "Person", "name": "Lenny Harrington"},
                  "email": "Lenny@thegrassyissue.com"},
}

apply_ = "--apply" in sys.argv

# ---- live counts, so the page cannot drift from the data ------------------
brands = json.load(open("data/brands.json", encoding="utf-8"))
src = json.load(open("research/brand-source-v3.json", encoding="utf-8"))
NB = len(brands)
KW = round(sum(v["words"] for v in src.values()) / 1000)
body = BODY.replace("{nbrands}", str(NB)).replace("{kwords}", str(KW))

# ---- build on the about.html chassis --------------------------------------
t = open(SRC, encoding="utf-8").read()
head = t[:t.find("</head>")]
# The chassis keeps its footer, the search JS, the mobile drawer AND both
# analytics tags in the BODY, just above </body> — not in <head>. Slicing the
# tail at </body> silently dropped GA4 and GoatCounter; the guard below caught
# it. Start the tail at the footer so everything below it comes across.
_f = t.find("<footer", t.find('<div class="writeup"'))
if _f == -1:
    raise SystemExit("could not find the footer in the chassis")
tail = t[_f:]
nav = re.search(r'<nav class="nav".*?</nav>', t, re.S).group(0)

head = re.sub(r"<title>[^<]*</title>", f"<title>{TITLE}</title>", head)
head = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + DESC + m.group(2), head)
head = re.sub(r'(<link rel="canonical" href=")[^"]*(")',
              lambda m: m.group(1) + "https://thegrassyissue.com" + URL + m.group(2), head)
# lambda, not a literal: json.dumps output contains \u and \" sequences that
# re.sub would read as regex escapes in a replacement string
_ld = '<script type="application/ld+json">' + json.dumps(SCHEMA) + "</script>"
head = re.sub(r'<script type="application/ld\+json">.*?</script>',
              lambda _m: _ld, head, flags=re.S)
# about.html carries no og:/twitter: tags; give this one a share card
plain_title = TITLE.split(" &mdash; ")[0]
head += (f'\n<meta property="og:title" content="{plain_title}">'
         f'\n<meta property="og:description" content="{DESC}">'
         f'\n<meta property="og:url" content="https://thegrassyissue.com{URL}">'
         f'\n<meta property="og:type" content="website">'
         f'\n<meta name="twitter:card" content="summary_large_image">'
         f'\n<meta name="twitter:title" content="{plain_title}">'
         f'\n<meta name="twitter:description" content="{DESC}">')

out = head + "</head>\n<body>\n" + nav + "\n" + body + "\n" + tail

# ---- guards ---------------------------------------------------------------
import html as H
plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", H.unescape(body)))
words = len(re.findall(r"[A-Za-z0-9']+", plain))
problems = []
if re.search(r"\bworth\b", plain, re.I):
    problems.append("banned word 'worth'")
if words < 400:
    problems.append(f"only {words} words")
if out.count("<h1") != 1:
    problems.append(f"{out.count('<h1')} h1 tags")
if "G-G89M4116SB" not in out:
    problems.append("GA4 tag did not come across from the chassis")
if "goatcounter" not in out.lower():
    problems.append("GoatCounter tag did not come across")
if 'id="tgi-search-input"' not in out:
    problems.append("search box missing")
for n in (str(NB), str(KW)):
    if n not in out:
        problems.append(f"live count {n} did not render")
d = re.search(r'<meta name="description" content="([^"]*)"', out).group(1)
if not 110 <= len(d) <= 165:
    problems.append(f"meta description {len(d)} chars")
ttl = re.search(r"<title>([^<]*)</title>", out).group(1)
if len(ttl) > 65:
    problems.append(f"title {len(ttl)} chars")
json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', out, re.S).group(1))
if problems:
    raise SystemExit("REFUSED:\n  " + "\n  ".join(problems))

if apply_:
    open(OUT, "w", encoding="utf-8").write(out)

print(("wrote" if apply_ else "DRY RUN") + f" {URL}  ({words} words)")
print(f"  Index counts rendered live: {NB} brands, ~{KW}k words of brand coverage")
print(f"  title {len(ttl)}c | description {len(d)}c | schema ok | GA4 + GoatCounter + search inherited")
if not apply_:
    print("\npass --apply to write")
