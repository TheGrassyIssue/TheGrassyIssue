#!/usr/bin/env python3
"""Field Notes — the Austin golf events calendar, autumn 2026 into 2027.

WHY THIS POST EXISTS
--------------------
The homepage "Austin Events" module was advertising four events, three of which
had already happened: the Texas Amateur (6/18-21), the Firecracker Open (7/3-5)
and the Austin City Championship (7/31-8/2). Only the November Tour event was
still ahead. Lenny, 2026-09-16, asked for a Field Note on upcoming golf and
golf-adjacent events, then a refresh of that homepage module.

THE LEDE IS A CORRECTION. The homepage card called the November PGA Tour event
the "Good Good Championship". Good Good Golf announced on 8/27/26 that it was
stepping away as title sponsor. The official tournament site now presents the
event as the AUSTIN CHAMPIONSHIP and states that ticket sales and volunteer
registration are temporarily paused; existing tickets stay valid. The PGA Tour's
own URL still carries the old slug, and every resale site still sells it under
the old name. We report the state of things as of 9/16/26 and date-stamp it.
Guarded: the page must not call it the Good Good Championship in its own voice.

DATES ARE THE PRODUCT. This is a calendar, so a wrong date is worse than a
missing event. Every date here is as the source page states it. Three rules
followed throughout:
  - no event appears without a published, sourced date
  - an annual event with no announced next date gets NO date and goes in the
    "not yet on the calendar" section
  - anything already closed for entry says so on the card

DELIBERATELY NOT ASSERTED:
  - a date for the Random Golf Club Austin meetup. A product URL exists with
    "november-20th" in the slug but no year, and every route to the page —
    product URL, shop mirror, .json endpoint, the SweatPals listing — returned
    empty. RGC is an Austin brand and this is exactly our kind of event, but a
    slug is not a source.
  - entry fees for the City of Austin events. golfatx.bluegolf.com, where the
    fees live, returned completely empty on every path. The card says where to
    look rather than guessing a number.
  - a 2027 City of Austin or Austin Amateur schedule. Neither exists yet.
  - a Five Iron Golf opening date. The 501 Congress lease is signed and
    reported; no opening date is published.
  - that the Butler "H1" league or the Golfinity seasons are open. Both started
    in August and neither page states a year, so they are described as
    in-progress rather than given dates.

WINTER IS GENUINELY THIN, and the post says so rather than padding. The City's
season ends 10/3, Austin Amateur's ends in early October, and neither UT team
plays a home event before the NCAA regional at UT Golf Club in May 2027. From
December the calendar is carried by the indoor and social side.

IMAGERY is reused from the existing library — these are venue photographs we
already localised for the field guide and the private-clubs post. No event
gets a photograph of a course it is not played on; the Senior Men's City
Championship at Morris Williams has no card because we have no Morris Williams
photograph, and it tees off two days from publication anyway.

DATE FORMAT: numeric M/D, M/D/YY in the header.
TWITTER TAGS: og: is mirrored to twitter:. Do not remove.
FAQ MARKUP: <details class="faq-q"><summary>.
"""
import re, os, json

SLUG = "austin-golf-events-calendar"
TITLE = "Field Notes &mdash; What&rsquo;s Actually on the Austin Golf Calendar"
PLAIN = "Field Notes — What's Actually on the Austin Golf Calendar"
DESC = ("Every golf and golf-adjacent event in Austin you can still get to between now "
        "and spring — the PGA Tour's return to Barton Creek under a new name, four charity "
        "and muni tournaments, the weekly leagues that carry the winter, and what still "
        "has no date. Checked 9/16/26.")
IMG = "/images/austin-events/"
FG = "/field-guide/"
LIONS = "/drops/lions-municipal-golf-course-austin"
HANCOCK = "/drops/hancock-golf-course-austin"

# (stem, name, date, venue, type, cost, url, copy)
EVENTS = {
 "aflcio": ("Texas AFL-CIO &middot; Walter Umphrey Golf Tournament", "10/1",
  "Crystal Falls Golf Course &middot; Leander", "Charity", "Registration tiers published",
  "https://texasaflcio.org/events/golf2026",
  "This one runs as a four-person scramble twenty minutes north of the city, with registration at 7:30am and a 9:00am shotgun. Proceeds go to the Texas AFL-CIO Membership Education Fund and Scholarship Fund, both tax-deductible, and the entry is open to anyone online."),
 "pumpkin-open": ("The Pumpkin Open", "10/3",
  "Hancock Golf Course &middot; Hyde Park", "Municipal", "See BlueGolf",
  "https://www.austintexas.gov/golfatx/tournaments-results",
  "The last event on the City of Austin&rsquo;s 2026 tournament calendar, played over the oldest nine holes in Texas. Registration runs through BlueGolf, and the City does not publish the entry fee on its own page &mdash; you have to click through."),
 "last-gasp": ("The Last Gasp", "10/3",
  "Star Ranch Golf Club &middot; Hutto", "League", "Chapter membership",
  "https://www.mgatour.com/chapters/austin/events",
  "The season finale of the Austin chapter of the Mediocre Golf Association, a deliberately unserious tour that has been running since 2006 and means the name sincerely. A 10:00am start, and you need to join the chapter to play."),
 "gbta": ("GBTA Austin Charity Golf Tournament", "11/2",
  "Onion Creek Country Club &middot; South Austin", "Charity", "Early-bird closed 8/31",
  "https://gbta-austinbta.org/2026_Golf_Tournament_",
  "Austin&rsquo;s business-travel association runs its annual fundraiser with a 9:00am shotgun, a silent auction and a separate bingo-and-lunch option for anyone who would rather not play. Confirm the entry details directly before you pay &mdash; the registration page was still in preview when we checked."),
 "golf-for-joy": ("Golf for Joy Austin", "11/8&ndash;9",
  "800 Congress, then Grey Rock Golf Club", "Charity", "Contact to register",
  "https://www.joyrx.org/events/gfja2026",
  "Two days: a Sunday dinner and live auction downtown, then an 11:45am shotgun at Grey Rock on Monday. The fourth Austin edition of a series that has raised over $4 million for JoyRx programs in children&rsquo;s hospitals, and the page says spots are limited."),
 "austin-championship": ("The Austin Championship &mdash; PGA Tour", "11/12&ndash;15",
  "Omni Barton Creek &middot; Fazio Canyons", "Professional", "Ticket sales paused",
  "https://www.austinchampionship.com/",
  "The Tour&rsquo;s return to Austin after three years away: a 120-player FedExCup Fall field, a $6,000,000 purse and 500 points to the winner, on the Fazio Canyons course Tom Fazio recently helped restore. Tournament week runs 11/9&ndash;15 and competition rounds 11/12&ndash;15."),
 "joe-black-cup": ("46th Texas Joe Black Cup Matches", "11/16&ndash;17",
  "Driftwood Golf &amp; Ranch Club &middot; Driftwood", "Professional", "Free to watch",
  "https://www.ntpga.com/texas-joe-black-cup",
  "A Ryder-Cup-format match between the Northern and Southern Texas PGA Sections, running since 1981 and standing at 22&ndash;21&ndash;2 to the north. It lands the Monday and Tuesday straight after the Tour event, which gives Austin two consecutive weeks of professional golf."),
 "butler-leagues": ("Butler Pitch &amp; Putt Leagues", "Weekly, year-round",
  "Butler Pitch &amp; Putt &middot; Downtown", "League", "From $3",
  "https://butlerpitchandputt.com/leagues-tourneys/morning-social-league",
  "Three standing leagues on nine of the best-value holes in Texas: a Wednesday morning social with a $3 pot, a Tuesday evening scramble where teams are drawn at random, and a women&rsquo;s league every other Tuesday night. Turn up alone and you get paired."),
 "golfinity": ("The Golfinity Tour", "Monthly, year-round",
  "Golfinity &middot; Austin", "Indoor", "Free to play",
  "https://golfinity.com/leagues-tournaments",
  "Twenty simulator bays and a monthly match series that runs straight through the winter at no cost, with championship prizes at the end. No membership needed and walk-ins are welcome, which makes it the easiest thing on this list to actually do."),
 "topgolf": ("Topgolf Austin Fall League", "9/14&ndash;11/9",
  "Topgolf &middot; The Domain", "League", "$475 per team",
  "https://topgolf.com/us/austin/play/leagues/",
  "Eight Monday nights, six of regular season and two of playoffs, with every team making the playoffs and a private bay for three hours a week. <strong>Registration has closed</strong> for both teams and free agents &mdash; this one is here so you know to watch for the spring season."),
}

SECTIONS = [
 ("October", "Three in three days at the start of the month, then the City&rsquo;s season is over.",
  ["aflcio", "pumpkin-open", "last-gasp"]),
 ("November", "November carries the busiest stretch of the Austin golf year, and the only Tour card on it.",
  ["gbta", "golf-for-joy", "austin-championship", "joe-black-cup"]),
 ("Every Week, All Winter", "What carries December through March, when the outdoor calendar goes quiet.",
  ["butler-leagues", "golfinity", "topgolf"]),
]

INTRO = f"""<div class="writeup">
  <div class="writeup-body">
    <p>Austin&rsquo;s golf calendar is front-loaded and then it falls off a cliff. The City of Austin&rsquo;s tournament season ends on 10/3. Austin Amateur Golf&rsquo;s runs out in early October. Neither University of Texas team plays a single home event this season until an NCAA regional lands at UT Golf Club in May 2027. From December to March the calendar belongs to the indoor and social side, which is better than it sounds.</p>
    <p>In between there is a six-week run in October and November that is the best stretch of the year, including the PGA Tour&rsquo;s first visit to Austin since 2023. Which brings us to the thing everyone has wrong.</p>
    <p><strong>The November Tour event is not called the Good Good Championship any more.</strong> Good Good Golf announced on 8/27 that it was stepping away as title sponsor. The official tournament site now presents the event as <strong>the Austin Championship</strong> and states that ticket sales and volunteer registration are temporarily paused, with existing tickets still valid for the dates purchased. No replacement sponsor has been announced. The PGA Tour&rsquo;s own page still sits at the old URL and every resale site is still selling it under the old name, so if you are searching for tickets you will find a lot of confidently wrong listings. This is where things stood on 9/16/26.</p>
    <p>Everything below carries the date its source page states. Where a thing happens annually but has no announced date, it is in the last section without one, because a calendar that guesses is not a calendar.</p>
  </div>
</div>
"""

UT = """<section class="products">
  <h2 class="products-hdr">Already on the 2027 Calendar</h2>
  <p class="cat-kicker">One date outside this window that is large enough to plan around.</p>
  <div class="writeup-body">
    <p><strong>NCAA Men&rsquo;s Regional Championship &mdash; 5/17&ndash;19/27, The University of Texas Golf Club.</strong> A regional, in Austin, on campus. It is the single biggest piece of golf coming to this city after November, and it is the only home date on either Longhorn schedule.</p>
    <p>That is not a figure of speech. We read both 2026&ndash;27 schedules line by line. The men&rsquo;s team plays Grand Haven, Frisco, Fort Worth, St Andrews, Westlake Village, Waimea, Cabo San Lucas, Daly City, Palm City, Augusta, Richmond Hill and Saint Simons Island &mdash; and then comes home for the regional. The women, ranked third in the country to start the season, play Frisco, St Andrews, Kailua-Kona, Palos Verdes, Houston, Palm Desert, Hilton Head, Fort Worth, Birmingham and Belleair, with nothing in Austin at all.</p>
    <p>One caveat we will not paper over: the women&rsquo;s NCAA regional on 5/10&ndash;12/27 has its site listed as TBA. Austin is not ruled out. It simply has not been assigned, and we are not going to assign it for them.</p>
  </div>
</section>
"""

PENDING = f"""<section class="products">
  <h2 class="products-hdr">Not Yet on the Calendar</h2>
  <p class="cat-kicker">Real events with no published date. We are not going to invent one.</p>
  <div class="writeup-body">
    <ul>
      <li><strong>Five Iron Golf, 501 Congress.</strong> The lease was signed in January for a 13,500 square foot flagship with twelve Trackman bays, duckpin bowling, a full bar and league play. No opening date has been published. It would be the most significant addition to Austin&rsquo;s indoor scene in years.</li>
      <li><strong>The Muny Conservancy&rsquo;s winter events.</strong> The annual 19th Hole Party and the Imagine Muny benefit at ACL Live both happen; neither has a 2027 date posted. Given that legislation pushed the <a href="{LIONS}">Lions Municipal</a> dissolution date to May 2027, the next one matters more than usual.</li>
      <li><strong>Austin Indoor Golf league nights.</strong> The Pflugerville site says weekly leagues launch in autumn 2026 and offers a waitlist signup. No date, no price.</li>
      <li><strong>PopStroke putting leagues.</strong> Both Austin locations are open &mdash; Harris Ridge and Cedar Park &mdash; and the company&rsquo;s boilerplate promises weekly putting leagues, but no Austin dates are published for either.</li>
      <li><strong>A Random Golf Club Austin meetup.</strong> There is a product URL with a November date in the slug and no year in it, and every route to that page came back empty. RGC is an Austin brand and this is exactly the sort of thing this list is for, so we will keep trying.</li>
      <li><strong>The 2027 City of Austin and Austin Amateur schedules.</strong> Neither is published. The City&rsquo;s page currently ends at the Pumpkin Open.</li>
    </ul>
  </div>
</section>
"""

FAQ_ITEMS = [
 ("Is the Good Good Championship still happening in Austin?",
  "The tournament is still scheduled at Omni Barton Creek for 11/12&ndash;15/26, but it is no longer called the Good Good Championship. Good Good Golf announced on 8/27/26 that it was stepping away as title sponsor, and the official tournament site now presents the event as the Austin Championship. HNS Sports Group and the PGA Tour have said the event proceeds as planned. No replacement title sponsor has been announced as of 9/16/26."),
 ("Can you still buy tickets to the Austin Championship?",
  "Not through official channels right now. The tournament site states that ticket sales and volunteer registration have been temporarily paused, and that existing tickets remain valid for the dates purchased and existing volunteer registrations will be honoured. Resale sites are still listing the event under its former name at various prices; those are not official sales, and we would wait for primary sales to reopen."),
 ("What golf can you actually play in Austin in the winter?",
  "The outdoor tournament calendar effectively ends on 10/3 with the Pumpkin Open, but the social and indoor side runs year-round. Butler Pitch &amp; Putt holds three weekly leagues downtown, starting at a $3 buy-in. Golfinity runs a free monthly tour across twenty simulator bays with no membership required. Topgolf's league at the Domain runs in defined seasons &mdash; the autumn season is closed, so watch for spring."),
 ("Which Austin golf tournaments can the public enter?",
  "More than you would think. The Texas AFL-CIO scramble at Crystal Falls on 10/1 takes open online registration, as does the GBTA charity tournament at Onion Creek on 11/2. Golf for Joy at Grey Rock on 11/9 takes registrations by email and says spots are limited. The City of Austin's Pumpkin Open at Hancock is open to the public through BlueGolf, though the City does not publish the entry fee on its own page."),
 ("When does professional golf come to Austin?",
  "Twice in one week this year. The Austin Championship runs 11/12&ndash;15 at Omni Barton Creek's Fazio Canyons course with a 120-player field and a $6,000,000 purse, and the Texas Joe Black Cup follows immediately on 11/16&ndash;17 at Driftwood, a Ryder-Cup-format match between the Northern and Southern Texas PGA Sections that has been running since 1981."),
]
FAQ = """<section class="products">
  <h2 class="products-hdr" id="faq">The Questions</h2>
  <div class="faq">
""" + "\n".join(f'    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>'
                for q, a in FAQ_ITEMS) + """
  </div>
</section>
"""


def card(s):
    name, date, venue, typ, cost, url, copy = EVENTS[s]
    pl = re.sub(r'<[^>]+>|&[a-z]+;|&#\d+;', '', name).strip()
    return f"""<div class="product-card" data-frames="1">
      <div class="product-gallery"><div class="pg-track"><div class="pg-frame">
        <img src="{IMG}{s}.jpg" alt="{pl} &mdash; {re.sub(r'&[a-z]+;', '', venue)}" loading="lazy" /></div></div></div>
      <div class="product-body">
        <div class="product-brand">{date} &middot; {typ}</div>
        <div class="product-name">{name}</div>
        <div class="product-desc"><strong>{venue}</strong> &middot; {cost}<br>{copy}</div>
        <a href="{url}" target="_blank" rel="noopener" class="product-link">Details &#8599;</a>
      </div>
    </div>"""


def sec(head, kicker, stems):
    c = "\n    ".join(card(s) for s in stems)
    return (f'<section class="products">\n  <h2 class="products-hdr">{head}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'  <div class="products-grid">\n    {c}\n  </div>\n</section>\n')


def st(s):
    for a, b in [("&ldquo;", '"'), ("&rdquo;", '"'), ("&rsquo;", "'"), ("&amp;", "&"),
                 ("&mdash;", "—"), ("&middot;", "·"), ("&ndash;", "–")]:
        s = s.replace(a, b)
    return re.sub(r'<[^>]+>', '', s)


SCHEMA = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": st(q),
                          "acceptedAnswer": {"@type": "Answer", "text": st(a)}}
                         for q, a in FAQ_ITEMS]}

model = open("drops/brand-to-know-gamut-golf.html", encoding="utf-8").read()
head = model[:model.find('<div class="breadcrumb">')]
tail = model[model.find('<section class="more"'):]
head = re.sub(r'<title>[^<]*</title>', f'<title>{PLAIN} — The Grassy Issue</title>', head)
for k, v in [("description", DESC), ("og:title", PLAIN), ("og:description", DESC)]:
    head = re.sub(rf'(<meta (?:name|property)="{re.escape(k)}" content=")[^"]*(")',
                  lambda m: m.group(1) + v + m.group(2), head)
for k, v in [("twitter:title", PLAIN), ("twitter:description", DESC)]:
    head = re.sub(rf'(<meta name="{k}" content=")[^"]*(")',
                  lambda m, v=v: m.group(1) + v + m.group(2), head)
head = re.sub(r'(<link rel="canonical" href=")[^"]*(")',
              lambda m: m.group(1) + f"https://thegrassyissue.com/drops/{SLUG}" + m.group(2), head)
head = re.sub(r'(<meta property="og:url" content=")[^"]*(")',
              lambda m: m.group(1) + f"https://thegrassyissue.com/drops/{SLUG}" + m.group(2), head)
head = re.sub(r'(<meta property="og:image" content=")[^"]*(")',
              lambda m: m.group(1) + f"https://thegrassyissue.com{IMG}austin-championship.jpg" + m.group(2), head)
_sb = '<script type="application/ld+json">' + json.dumps(SCHEMA) + '</script>'
head = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: _sb, head, flags=re.S)

N = sum(len(s[2]) for s in SECTIONS)
body = ('<div class="breadcrumb">\n  <a href="/">Feed</a><span>/</span>\n'
        '  <a href="/#feed">Field Notes</a><span>/</span>\n  Austin Golf Calendar</div>\n'
        f'<header class="drop-header">\n  <h1>{TITLE}</h1>\n  <div class="drop-meta">\n'
        '    <span>9/16/26</span><span class="dot"></span>\n'
        '    <span>Field Notes</span><span class="dot"></span>\n'
        f'    <span>Austin, Texas &middot; {N} Events</span>\n  </div>\n</header>\n\n'
        f'<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}austin-championship.jpg" '
        'alt="Omni Barton Creek, Fazio Canyons — host of the Austin Championship in November" /></div></div>\n'
        + INTRO
        + "".join(sec(*s) for s in SECTIONS)
        + UT + PENDING + FAQ)

# ---- guards -------------------------------------------------------------
placed = [s for sc in SECTIONS for s in sc[2]]
if sorted(placed) != sorted(EVENTS):
    raise SystemExit(f"section/EVENTS mismatch: unplaced={set(EVENTS)-set(placed)} extra={set(placed)-set(EVENTS)}")
if len(placed) != len(set(placed)):
    raise SystemExit("an event is placed twice")
gone = [s for s in placed if not os.path.exists(f"images/austin-events/{s}.jpg")]
if gone:
    raise SystemExit(f"images missing on disk: {gone}")
_txt = re.sub(r'<[^>]+>', ' ', body)
# Place names containing "Worth" are not the banned word. verify-post.py strips
# Fort Worth for exactly this reason; this guard has to match it or a UT away
# schedule that legitimately lists Fort Worth, Texas fails the build.
_wtxt = re.sub(r'\bFort\s+Worth\b', ' ', _txt, flags=re.I)
if re.search(r'\bworth\b', _wtxt, re.I):
    raise SystemExit("BANNED WORD 'worth' in the body copy")
# The rename is the lede. The page may REPORT the old name as the old name, but
# must never present the event under it.
# The old name SHOULD appear — readers are searching it, and the FAQ leads with
# it on purpose. What must never happen is the old name standing alone as the
# event's current name. So: every mention has to sit near a correction.
if "Austin Championship" not in _txt:
    raise SystemExit("the renamed event must be named on the page")
CORRECTIONS = ("no longer", "stepping away", "former", "now presents",
               "not called", "retired", "under a new name")
for m in re.finditer(r'Good Good Championship', _txt, re.I):
    window = _txt[max(0, m.start() - 320): m.end() + 320].lower()
    if not any(c in window for c in CORRECTIONS):
        raise SystemExit(
            "an uncorrected 'Good Good Championship' mention at char "
            f"{m.start()} — as of 8/27/26 the event is the Austin Championship, "
            "so every use of the old name must sit beside the correction")
# no event may carry a date we did not source
for s, (n, d, *_rest) in EVENTS.items():
    if not d or d.strip() in ("TBA", "TBD", "soon"):
        raise SystemExit(f"{s} has no real date — it belongs in 'Not Yet on the Calendar'")
# past events must not reappear: this post exists because three stale ones shipped
for past in ("Firecracker Open", "117th Texas Amateur", "Austin City Championship"):
    if past in _txt:
        raise SystemExit(f"'{past}' already happened in 2026 — it must not be on a forward calendar")
if "randomgolfclub.com/products" in body:
    raise SystemExit("the RGC meetup URL is unverified — link the brand, not a page we could not read")
if "5/17&ndash;19/27" not in body or "University of Texas Golf Club" not in body:
    raise SystemExit("the NCAA regional date/venue is the one big 2027 anchor — keep both")
# The women's regional site is listed TBA on the official schedule. Never state
# or imply it lands in Austin.
if re.search(r"women[^.]{0,80}regional[^.]{0,80}(Austin|UT Golf)", _txt, re.I):
    raise SystemExit("the women's NCAA regional site is TBA — do not place it in Austin")
if body.count('<details class="faq-q">') != len(FAQ_ITEMS):
    raise SystemExit('FAQ must use <details class="faq-q"><summary> markup')

open(f"drops/{SLUG}.html", "w", encoding="utf-8").write(head + body + tail)
print(f"wrote drops/{SLUG}.html | {len(SECTIONS)} sections | {N} events | "
      f"~{len(re.sub(r'<[^>]+>', ' ', head+body+tail).split())} words")
