#!/usr/bin/env python3
# The Lottery Round — Austin + Hill Country private clubs.
# Built off the Hat Edit shell. Every factual claim here was source-verified 2026-08-20.
import os, re, json

S = os.path.dirname(os.path.abspath(__file__))
BASE = open(os.path.join(S, "drops/the-hat-edit-austin-summer.html"), encoding="utf-8").read()
FR = json.load(open("/tmp/pc/frames.json"))

SLUG = "the-lottery-round-austin-private-clubs"
TITLE = ("The Lottery Round &mdash; 12 Private Clubs Around Austin, "
         "and What Not One of Them Will Tell You They Cost")
TITLE_PLAIN = ("The Lottery Round — 12 Private Clubs Around Austin, "
               "and What Not One of Them Will Tell You They Cost")
DESC = ("Twelve private golf clubs in Austin and the Texas Hill Country — Coore & Crenshaw, Pete Dye, "
        "Fazio, Nicklaus, David McLay Kidd. The architecture, the history, and the reason none of them "
        "publishes a single number.")

# ---------------------------------------------------------------- club data
# name, kicker, place, arch line, body paragraphs, link
CLUBS = [
 ("austin-golf-club", "Austin Golf Club", "Spicewood", "Bill Coore &amp; Ben Crenshaw, 2001",
  ["Crenshaw grew up in Austin and learned the game from Harvey Penick. In 2001 he and Bill Coore built a "
   "golf course forty minutes west of town, on Highway 71 in Spicewood, and then more or less closed the door "
   "behind them. It plays to a par of 70 over roughly 6,900 yards.",
   "There is no website. Not a members-only login, not a holding page &mdash; nothing. The domain that carries the "
   "club's name is parked and listed for sale. There is no photography to show you here for the same reason "
   "there is no phone number to give you: the club does not publish itself. Everything you have read about "
   "the place, including the paragraph above, comes from architecture databases and other people's rankings.",
   "That absence is the most honest illustration of this entire post. A club that never asks for your "
   "attention never has to tell you its price."], None),

 ("austin-country-club", "Austin Country Club", "Davenport Ranch", "Pete and Alice Dye, 1984",
  ["The club dates to 1899 and this is its third home. The Dyes routed it down the bluffs to Lake Austin in "
   "1984, and the closing stretch is the reason anyone outside Texas knows the name. The 12th, "
   "&ldquo;Iron Bridge,&rdquo; is a 578-yard par 5 that tumbles downhill to a green tucked under the "
   "Pennybacker Bridge &mdash; the hole in the photograph above. The 13th, &ldquo;Cape Dye,&rdquo; is the more "
   "famous one on television: a 317-yard par 4 whose tee juts out into the lake with the bridge behind it.",
   "Harvey Penick was the head professional here from 1923 to 1971 and stayed on as professional emeritus "
   "until his death in 1995. Tom Kite and Ben Crenshaw both came up under him, though they met as juniors "
   "at the club's previous site, not this one.",
   "It hosted the WGC-Dell Technologies Match Play from 2016 through 2023, when the PGA Tour retired the "
   "World Golf Championships. That was the last time most of us got to see the place."], None),

 ("loraloma", "Loraloma", "Spicewood", "David McLay Kidd, October 2025",
  ["The newest one, and the only club on this list that opened inside the last twelve months. Kidd built "
   "Bandon Dunes and Gamble Sands; this is his first course in Texas. It sits on more than 1,200 acres "
   "inside the 2,200-acre Thomas Ranch masterplan above Lake Travis.",
   "It is grassed wall to wall in Zoysia, which in a Hill Country summer is a genuine agronomic argument "
   "rather than a marketing one. The routing uses the elevation the way Kidd's courses usually do &mdash; wide "
   "corridors, big ground movement, greens you can run a ball onto rather than fly.",
   "Because it is new, it is also the club currently doing the most talking. Loraloma publishes more "
   "photography and more detail about itself than any other club here. It still does not publish a "
   "membership price."], None),

 ("spanish-oaks", "Spanish Oaks Golf Club", "Bee Cave", "Bobby Weed, 2001",
  ["Weed's original design opened the same year as Austin Golf Club, twenty minutes closer to town. It runs "
   "to 7,155 yards at a par of 71, cut through limestone and live oak on ground that does most of the "
   "defending by itself.",
   "Weed came back years later to renovate his own work, which is rarer than it sounds and usually a good "
   "sign &mdash; it means the club kept the architect rather than shopping for a new name.",
   "The membership page lists three categories: Full, Junior and National Golf. Then it lists a phone number."], None),

 ("driftwood", "Driftwood Golf and Ranch Club", "Driftwood", "Tom Fazio, debuted 2022",
  ["A Discovery Land Company property southwest of town, which tells you most of what you need to know about "
   "the model: the golf course is one amenity inside a large private community with its own restaurants, "
   "pools, and comfort stations.",
   "Fazio built the course. Reports around the opening split between fall 2021 and 2022 and neither the club "
   "nor Discovery has ever published a hard date, so treat the year as approximate.",
   "What the club does publish, at length, is real estate. There is no membership page at all."], None),

 ("cimarron-hills", "Cimarron Hills", "Georgetown", "Jack Nicklaus, January 2003",
  ["Thirty miles north of Austin, and the one club on this list that will give you a precise date. Its own "
   "history page says the golf course opened on 1 January 2003, and that Nicklaus was on site every six "
   "weeks through design and construction.",
   "That level of specificity about the golf and total silence about the cost is, by the end of this post, "
   "a pattern you will stop noticing.",
   "It is a full country club &mdash; tennis, pool, a Tuscan-styled clubhouse &mdash; rather than a golf-only "
   "operation."], None),

 ("the-hills", "The Hills Country Club", "Lakeway", "Jack Nicklaus, 1981",
  ["The Hills Signature course was Nicklaus's first design in Texas, opened in 1981, and it is still the "
   "reason to go. Flintrock Falls followed in 2002, co-designed by Nicklaus with Jack Nicklaus II.",
   "Be accurate about the scale, though: the club today runs four courses and 72 holes, adding Live Oak and "
   "Yaupon in Lakeway to the two Nicklaus layouts. It is one of the largest private golf operations in the "
   "region.",
   "It is owned by Invited, formerly ClubCorp, and its pricing language is the most quietly remarkable thing "
   "in this whole piece. See below."], None),

 ("onion-creek", "Onion Creek Club", "South Austin", "Jimmy Demaret, 1974",
  ["The most historically important golf course on this list, and the only one Jimmy Demaret ever designed. "
   "It opened in 1974 in south Austin, short and flat and tree-lined, and it changed professional golf.",
   "In 1978 it hosted the first Legends of Golf, where Sam Snead and Gardner Dickinson beat Peter Thomson and "
   "Kel Nagle by a shot. The event was a television success nobody had predicted, and it led directly to the "
   "founding of the Senior PGA Tour in 1980. Onion Creek kept the tournament through 1989.",
   "Ben Crenshaw built a third nine here in 1996, blended into Demaret's original to make 27 holes. Coore and "
   "Crenshaw came back in 2014 to restore the course after flood damage."], None),

 ("great-hills", "Great Hills Country Club", "Northwest Austin", "Don January &amp; Billy Martindale, 1973",
  ["Built in 1973 by the PGA Championship winner Don January with the architect Billy Martindale, and "
   "genuinely in the hills &mdash; it is a short card, about 6,599 yards at par 71, that plays nothing like a "
   "short card because of what the ground does.",
   "The club is currently working through a course master plan by Chet Williams, so anyone joining now is "
   "buying a course mid-change.",
   "Great Hills is also the most transparent club here about the part that is not money. Membership is by "
   "invitation: an application, one letter from a member, and two additional references."], None),

 ("westlake", "Westlake Country Club", "Westlake", "Lanny Wadkins redesign, 2023",
  ["This was Lost Creek Country Club for fifty years. In September 2023 its owner, Invited, renamed it "
   "Westlake Country Club as part of what the company called the largest club and course transformation in "
   "its 65-year history.",
   "The Lanny Wadkins redesign was unveiled that November. It is the freshest golf course in central Austin "
   "that is not brand new, which is a real category &mdash; mature trees, modern greens.",
   "If you played Lost Creek years ago and have not been back, you have not played this."], None),

 ("river-place", "River Place Country Club", "Northwest Hills", "Tom Kite &amp; Roy Bechtol, early 1990s",
  ["Tom Kite is from Austin, learned under Penick alongside Crenshaw, and this was among his first ventures "
   "into course design, built with Roy Bechtol.",
   "The opening year is genuinely unsettled &mdash; third-party listings claim 1982, 1984, 1994 and 1995, and "
   "Kite's own design site says only that his work began in the early 1990s. We are not going to invent a "
   "date for you.",
   "It plays hard up and down a canyon in the northwest hills, and it is the closest thing on this list to a "
   "golf course that will physically hurt you."], None),
]

BARTON = ("barton-creek", "Barton Creek", "Southwest Austin",
  "Fazio, Palmer, Coore &amp; Crenshaw &mdash; 72 holes")

# ---------------------------------------------------------------- intro
INTRO = """    <p>The premise is simple and slightly stupid, which is the best kind. You come into money. Not
    comfortable money &mdash; the other kind. Where in Austin do you go play golf?</p>
    <p>We put twelve private clubs in and around town and out into the Hill Country against that question,
    and the answers turned out to be better than expected. Coore and Crenshaw. Pete and Alice Dye on Lake
    Austin. The only golf course Jimmy Demaret ever designed, which happens to be the reason the senior tour
    exists. Nicklaus twice. Fazio. And, as of last October, David McLay Kidd's first course in Texas.</p>
    <p>Then we went looking for what any of it costs, and found something more interesting than a number.</p>
    <p>So this runs in two halves. First the golf, because that is the fun part. Then the door, because that
    is the honest part.</p>"""

PART2_HDR = "Part Two &mdash; The Door"

PART2 = """    <p>Here is the finding, and we want to be precise about the claim: <strong>not one of these twelve
    clubs publishes an initiation fee, a monthly due, a food and beverage minimum, or a capital assessment
    anywhere on its own website.</strong> Zero out of twelve. We checked every club's own membership page
    rather than the aggregator sites, because the aggregator sites are guessing.</p>
    <p>What they publish instead is a vocabulary.</p>
    <p>The two Invited clubs &mdash; The Hills and Westlake &mdash; are the most systematic about it. Between them
    they list a full slate of golf membership tiers, and every single tier carries the same three words where
    a price would go: <em>Inquire for Pricing</em>. Westlake's own FAQ asks &ldquo;What is the cost of a
    Westlake membership?&rdquo; and answers it by giving you the membership director's contact details.</p>
    <p>The two Arcis clubs, Onion Creek and River Place, both run a banner advertising a limited-time joining
    offer. Neither states what is being offered, or off what.</p>
    <p>Spanish Oaks names three categories and then a club manager's phone number. Great Hills does not
    discuss money at all, and instead tells you the thing that actually gates it: an application, a letter
    from a member, and two more references. Driftwood has no membership page whatsoever, though it will
    happily show you real estate. Austin Country Club's membership page sits behind a member login. And
    Austin Golf Club, as covered above, has no website to hide anything on.</p>
    <p>One near-miss deserves flagging, because it is the kind of number that gets misquoted. Loraloma's own
    FAQ document does publish a figure: annual dues of roughly $7,000 to $8,400. Those are Thomas Ranch
    <em>homeowners' association</em> dues for the surrounding community. They are not golf membership dues,
    and anyone citing them as the cost of joining Loraloma is wrong.</p>
    <p>You will find dollar figures for several of these clubs if you go looking &mdash; six-figure initiations,
    five-figure annuals. Every one of those numbers traces back to a third-party membership aggregator or a
    forum post, not to the club. We are not going to repeat them as fact, because we cannot stand them up.</p>
    <p>None of this is a scandal. Private clubs are private, quoting a price invites negotiation, and a fee
    that changes by category and by year is genuinely awkward to publish. But the effect deserves naming:
    the only way to learn what any of these clubs costs is to be the kind of person who can already get a
    membership director to return your call. The price is not hidden behind a paywall. It is hidden behind a
    person.</p>
    <p>Which brings us back to the lottery. If it hits, the golf is all still there &mdash; the Dyes on the lake,
    Demaret's only course, Kidd's Zoysia. You just have to find somebody willing to pick up.</p>"""

CLOSER_HDR = "The Closest You'll Get"

CLOSER = """    <p>One asterisk on all of the above. <strong>Barton Creek</strong> runs 72 holes southwest of town and
    the architecture list is absurd for somewhere you can realistically get onto: <strong>Fazio Foothills</strong>
    (1986, Tom Fazio's first course in Texas), <strong>Palmer Lakeside</strong> (1986, out at Lake Travis),
    <strong>Coore Crenshaw</strong> (1991, and yes &mdash; Coore deserves the co-credit the old
    &ldquo;Crenshaw Cliffside&rdquo; name buried), and <strong>Fazio Canyons</strong> (1999).</p>
    <p>It is both things at once: Barton Creek Country Club is a private membership, and Omni Barton Creek
    Resort &amp; Spa sits on the same ground. That does <em>not</em> make it a daily-fee course &mdash; Omni's own
    site reserves the golf for resort guests and members. But a room booking is a door, and it is the only
    door on this entire list that opens without an introduction.</p>
    <p>Barton Creek Country Club lists six membership tiers. Every one of them routes to
    &ldquo;Inquire About Membership.&rdquo;</p>"""

FAQ = [
 ("What are the best private golf clubs in Austin?",
  "Austin Golf Club in Spicewood (Bill Coore and Ben Crenshaw, 2001) and Austin Country Club at Davenport "
  "Ranch (Pete and Alice Dye, 1984) are the two most acclaimed private courses in the Austin area. Spanish "
  "Oaks in Bee Cave, Loraloma in Spicewood, and Driftwood Golf and Ranch Club round out the top tier of "
  "modern private golf in the region."),
 ("How much does it cost to join a private golf club in Austin?",
  "None of the twelve private clubs in and around Austin publishes an initiation fee, monthly dues, food and "
  "beverage minimum, or capital assessment on its own website. Invited-owned clubs such as The Hills and "
  "Westlake Country Club label every membership tier &ldquo;Inquire for Pricing.&rdquo; Any specific dollar "
  "figure you find online comes from third-party aggregators rather than from the clubs themselves."),
 ("Does Austin Golf Club have a website?",
  "No. Austin Golf Club, the Coore and Crenshaw course in Spicewood that opened in 2001, has no public "
  "website. The domain matching the club's name is parked and listed for sale. Information about the course "
  "comes from architecture databases and course rankings rather than from the club."),
 ("Which hole at Austin Country Club sits under the Pennybacker Bridge?",
  "The 12th, named &ldquo;Iron Bridge,&rdquo; is a 578-yard par 5 whose green sits on Lake Austin directly "
  "beneath the Pennybacker Bridge. The more televised 13th, &ldquo;Cape Dye,&rdquo; is a 317-yard drivable "
  "par 4 whose tee box juts into the lake with the bridge behind it. The two get conflated constantly."),
 ("Who designed Loraloma golf course?",
  "David McLay Kidd, the architect behind Bandon Dunes and Gamble Sands. Loraloma opened in October 2025 in "
  "Spicewood, Texas, inside the Thomas Ranch masterplan, and is Kidd's first golf course in Texas. It is "
  "grassed entirely in Zoysia."),
 ("Why is Onion Creek Club historically important?",
  "Onion Creek is the only golf course Jimmy Demaret ever designed, and in 1978 it hosted the first Legends "
  "of Golf, won by Sam Snead and Gardner Dickinson. That event's unexpected television success led directly "
  "to the founding of the Senior PGA Tour in 1980. Onion Creek hosted the tournament through 1989."),
 ("Is Barton Creek public or private?",
  "Both, and neither is quite daily-fee. Barton Creek Country Club is a private membership club, and Omni "
  "Barton Creek Resort &amp; Spa occupies the same property. Omni's own site reserves access to the four golf "
  "courses for resort guests and club members, so booking a room is the practical route onto the course."),
 ("What happened to Lost Creek Country Club?",
  "It was renamed Westlake Country Club in September 2023 by its owner, Invited, as part of what the company "
  "described as the largest club and course transformation in its 65-year history. A Lanny Wadkins course "
  "redesign was unveiled in November 2023."),
]

# ---------------------------------------------------------------- html
def card(slug, name, place, arch, paras, frames):
    n = len(frames)
    if n:
        pg = ('<div class="product-gallery"><div class="pg-track">'
              + "".join('<div class="pg-frame"><img src="/images/private-clubs/%s" loading="lazy" '
                        'alt="%s golf course in %s, Texas — %s">'
                        '</div>' % (f, name, place, arch.replace("&amp;", "and"))
                        for f in frames)
              + '</div>' + ('<div class="pg-dots">' + "".join('<span></span>' for _ in frames) + '</div>' if n > 1 else '')
              + '</div>')
    else:
        pg = ('<div class="club-noimg"><span class="club-noimg-mark">&mdash;</span>'
              '<span class="club-noimg-txt">No photography published</span></div>')
    body = "".join("<p>%s</p>" % p for p in paras)
    return ('  <div class="product-card club-card" data-frames="%d">\n'
            '    %s\n'
            '    <div class="club-meta"><span class="club-place">%s</span>'
            '<span class="club-arch">%s</span></div>\n'
            '    <h3 class="club-name">%s</h3>\n'
            '    <div class="club-body">%s</div>\n'
            '  </div>\n') % (n, pg, place, arch, name, body)

CSS = """
.club-card{display:flex;flex-direction:column}
.club-meta{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:14px 0 6px}
.club-place{font:500 11px/1 'JetBrains Mono',monospace;letter-spacing:.09em;text-transform:uppercase;
 background:var(--grass);color:var(--paper);padding:5px 9px;border-radius:3px}
.club-arch{font:400 12px/1.3 'JetBrains Mono',monospace;color:#5d5d55;letter-spacing:.02em}
.club-name{font:400 25px/1.15 'Fraunces',Georgia,serif;color:var(--ink);margin:2px 0 10px}
.club-body p{font:400 15px/1.62 'Inter',sans-serif;color:#33332e;margin:0 0 11px}
.club-body p:last-child{margin-bottom:0}
.club-noimg{aspect-ratio:3/2;background:repeating-linear-gradient(135deg,#EDE9E0,#EDE9E0 11px,#E5E0D5 11px,#E5E0D5 22px);
 border:1px solid #D8D2C4;border-radius:6px;display:flex;flex-direction:column;align-items:center;
 justify-content:center;gap:9px}
.club-noimg-mark{font:400 40px/1 'Fraunces',Georgia,serif;color:#A8A29020}
.club-noimg-txt{font:500 11px/1 'JetBrains Mono',monospace;letter-spacing:.11em;text-transform:uppercase;color:#8a8577}
.part-lede{font:400 17px/1.6 'Inter',sans-serif;color:#3a3a34;margin:0 0 26px;max-width:64ch}
.part2 p{font:400 16px/1.7 'Inter',sans-serif;color:#2b2b26;margin:0 0 17px;max-width:70ch}
.part2 strong{font-weight:600;color:var(--ink)}
.closer{background:#EFEBE1;border:1px solid #DDD6C7;border-left:4px solid var(--grass);
 border-radius:6px;padding:24px 26px;margin:34px 0 8px}
.closer p{font:400 15px/1.68 'Inter',sans-serif;color:#2b2b26;margin:0 0 13px;max-width:68ch}
.closer p:last-child{margin-bottom:0}
@media(max-width:640px){.club-name{font-size:22px}.part2 p{font-size:15px}}
"""

h = BASE
h = h.replace("the-hat-edit-austin-summer", SLUG)
h = h.replace("/images/hat-edit/hero.jpg", "/images/private-clubs/hero-private-clubs.jpg")
h = re.sub(r"<title>.*?</title>", "<title>%s &mdash; The Grassy Issue</title>" % TITLE, h, flags=re.S)
h = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1) + DESC + m.group(2), h)
h = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1) + DESC + m.group(2), h)
h = re.sub(r'(<meta name="twitter:description" content=")[^"]*(")', lambda m: m.group(1) + DESC + m.group(2), h)
h = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1) + TITLE_PLAIN + m.group(2), h)
h = re.sub(r'(<meta name="twitter:title" content=")[^"]*(")', lambda m: m.group(1) + TITLE_PLAIN + m.group(2), h)
h = re.sub(r'(<h1[^>]*>).*?(</h1>)', lambda m: m.group(1) + TITLE + m.group(2), h, count=1, flags=re.S)
h = re.sub(r'(<div class="writeup-body">).*?(</div>)',
           lambda m: m.group(1) + "\n" + INTRO + "\n  " + m.group(2), h, count=1, flags=re.S)

# ---- body: part one grid, then part two prose, then the Barton Creek closer
cards = "".join(card(c[0], c[1], c[2], c[3], c[4], FR.get(c[0], [])) for c in CLUBS)
# HOUSE FORMAT — cards MUST be wrapped in <div class="products-grid">. Direct children of
# <section class="products"> fall out of the grid and render full-width and oversized.
body = ('<section class="products">\n'
        '<h2 id="part-one">Part One &mdash; The Golf</h2>\n'
        '<p class="cat-kicker"><strong>Eleven Clubs, West to South</strong>The twelfth, Barton Creek, gets '
        'its own section at the end &mdash; it is the only one on the list you can realistically play. '
        'Every photograph is the club\'s own.</p>\n'
        '<div class="products-grid">\n'
        + cards +
        '</div>\n'
        '</section>\n'
        # NOTE: this section is intentionally left unclosed — the template's </section>
        # after the FAQ block closes it. See the cut below.
        '<section class="products part2">\n'
        '<h2 id="part-two">%s</h2>\n' % PART2_HDR + PART2 + '\n'
        '<h2 id="closest" style="margin-top:38px">%s</h2>\n' % CLOSER_HDR +
        '  <div class="closer">\n' + CLOSER + '\n  </div>\n')

start = h.index('<section class="products">')
# In this template the FAQ <div> lives INSIDE the single products <section>, and the
# </section> that follows the FAQ is what closes it. So cut to the faq div and leave the
# last section in `body` OPEN — the template's trailing </section> closes it.
# (Cutting to the enclosing <section> instead re-imports every card in the template.)
fq = h.index('<div class="faq">')
h = h[:start] + body + '  ' + h[fq:]

faq_html = "".join(
    '    <details class="faq-item"><summary>%s</summary><div class="faq-a"><p>%s</p></div></details>\n' % (q, a)
    for q, a in FAQ)
h = re.sub(r'(<div class="faq">).*?(  </div>\n</section>)',
           lambda m: m.group(1) + "\n" + faq_html + m.group(2), h, count=1, flags=re.S)

h = h.replace("</style>", CSS + "</style>", 1)

# ---- rebuild BOTH JSON-LD blocks from this post's real content.
# The template's Article description and its entire FAQPage survived the copy last time.
import html as _html
def _plain(s):
    return _html.unescape(re.sub(r"<[^>]+>", "", s)).replace("—", "—").strip()

def _fix_ld(m):
    raw = m.group(1)
    try:
        d = json.loads(raw)
    except Exception:
        return m.group(0)
    t = d.get("@type")
    if t == "FAQPage":
        d["mainEntity"] = [{"@type": "Question", "name": _plain(q),
                            "acceptedAnswer": {"@type": "Answer", "text": _plain(a)}}
                           for q, a in FAQ]
    else:
        d["headline"] = _plain(TITLE)
        d["name"] = _plain(TITLE)
        d["description"] = _plain(DESC)
        d["image"] = ["https://thegrassyissue.com/images/private-clubs/hero-private-clubs.jpg"]
        d["datePublished"] = "2026-08-20"
        d["dateModified"] = "2026-08-20"
        if isinstance(d.get("mainEntityOfPage"), dict):
            d["mainEntityOfPage"]["@id"] = "https://thegrassyissue.com/drops/" + SLUG
        d.pop("keywords", None)
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + '</script>'

h = re.sub(r'<script type="application/ld\+json">(.*?)</script>', _fix_ld, h, flags=re.S)

# ---- residual Hat Edit metadata (template leaks — see site-hygiene memory)
h = h.replace("The Hat Edit — 28 Summer Caps, Ropes and Buckets From the Brands We Follow", TITLE_PLAIN)
h = h.replace("The Hat Edit &mdash; 28 Summer Caps, Ropes and Buckets From the Brands We Follow", TITLE)
h = re.sub(r'<span>\d+ Hats</span>', '<span>12 Clubs</span>', h)
h = h.replace('<span class="hashtag">#TheHatEdit</span>', '<span class="hashtag">#TheLotteryRound</span>')
h = re.sub(r'(<span class="l">Hats</span><span>)\d+(</span>)', r'\g<1>12\g<2>', h)
h = h.replace('<span class="l">Hats</span>', '<span class="l">Clubs</span>')
h = re.sub(r'(<span class="l">Brands</span><span>)\d+(</span>)', r'\g<1>9\g<2>', h)
h = h.replace('<span class="l">Brands</span>', '<span class="l">Architects</span>')

MORE = ("""    <a href="/drops/the-austin-golf-road-trip" class="more-card"><div class="more-kicker">The Guide</div><div class="more-title">The Austin Golf Road Trip</div></a>
    <a href="/drops/hancock-golf-course" class="more-card"><div class="more-kicker">Field Notes</div><div class="more-title">Hancock &mdash; The Oldest Course in Texas</div></a>
    <a href="/field-guide" class="more-card"><div class="more-kicker">The Field Guide</div><div class="more-title">The Austin Golf Guide</div></a>
""")
h = re.sub(r'(<div class="more-grid">).*?(</div>\s*</section>)',
           lambda m: m.group(1) + "\n" + MORE + "  " + m.group(2), h, count=1, flags=re.S)

out = os.path.join(S, "drops", SLUG + ".html")
open(out, "w", encoding="utf-8").write(h)
print("wrote", out, len(h), "bytes")
