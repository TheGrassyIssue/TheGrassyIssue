#!/usr/bin/env python3
"""Wire the Austin events Field Note AND rebuild the stale homepage events module.

TWO JOBS, AND THE SECOND ONE IS THE REASON THIS EXISTS.

1. Standard post wiring: a feed card with a five-slide carousel, canonical
   slideTexts, a sitemap row.

2. Replace the ENTIRE <section class="events"> block on the homepage. It was
   advertising four events, three of which had already happened by the time
   anyone read it:
       117th Texas Amateur      6/18-21   past
       Firecracker Open         7/3-5     past
       Austin City Championship 7/31-8/2  past
       Good Good Championship   11/9-15   upcoming, but WRONG NAME
   The fourth was still ahead but carried the retired sponsor name. Good Good
   Golf stepped away on 8/27/26 and the event is now the Austin Championship
   with ticket sales paused.

   A homepage module that lists three dead events and misnames the fourth is
   worse than no module. It is rebuilt here from the same verified data as the
   Field Note, and the header now links the Field Note so there is one place
   that has to be kept current instead of two.

THE REAL FIX IS THE GUARD. `_assert_future` refuses to write any event card
whose date has already passed relative to TODAY. That is what was missing — the
module had no mechanism to notice it had gone stale. Re-run this script at any
time and it will fail loudly rather than quietly shipping history.

After this: gen-post-thumbs.py --apply, then generate-search-index.py and
build-ig.py --apply. No brands chain — this post adds no brands.
"""
import re, json, sys, datetime

SLUG = "austin-golf-events-calendar"
URL = f"/drops/{SLUG}"
KEY = "austinevents"
TITLE = "Field Notes &mdash; What&rsquo;s Actually on the Austin Golf Calendar"
PLAIN = "Field Notes — What's Actually on the Austin Golf Calendar"
IMG = "/images/austin-events/"
TODAY = datetime.date(2026, 9, 16)
TODAY_S = TODAY.isoformat()

# (stem, date-label, iso-end-date, type, venue, title, desc, url)
EVENTS = [
 ("aflcio", "Oct 1", "2026-10-01", "Charity",
  "Crystal Falls GC &middot; Leander", "Texas AFL-CIO Golf Tournament",
  "A four-person scramble twenty minutes north of the city, 7:30am registration and a 9:00am shotgun. Proceeds to the Texas AFL-CIO education and scholarship funds, and the entry is open to anyone online.",
  "https://texasaflcio.org/events/golf2026"),
 ("pumpkin-open", "Oct 3", "2026-10-03", "Municipal",
  "Hancock Golf Course &middot; Austin", "The Pumpkin Open",
  "The last event on the City of Austin's 2026 calendar, played over the oldest nine holes in Texas. Registration runs through BlueGolf; the City does not publish the entry fee on its own page.",
  "https://www.austintexas.gov/golfatx/tournaments-results"),
 ("golf-for-joy", "Nov 8&ndash;9", "2026-11-09", "Charity",
  "Grey Rock Golf Club &middot; Austin", "Golf for Joy Austin",
  "A Sunday dinner and live auction downtown, then an 11:45am shotgun at Grey Rock. The fourth Austin edition of a series that has raised over $4 million for JoyRx children's hospital programs. Spots are limited.",
  "https://www.joyrx.org/events/gfja2026"),
 ("austin-championship", "Nov 12&ndash;15", "2026-11-15", "Tournament",
  "Omni Barton Creek &middot; Fazio Canyons", "The Austin Championship (PGA Tour)",
  "The Tour's first Austin stop since 2023: 120 players, a $6,000,000 purse, 500 FedExCup points. Formerly the Good Good Championship &mdash; the title sponsor stepped away on 8/27 and ticket sales are currently paused.",
  "https://www.austinchampionship.com/"),
 ("joe-black-cup", "Nov 16&ndash;17", "2026-11-17", "Tournament",
  "Driftwood Golf &amp; Ranch Club", "46th Texas Joe Black Cup",
  "A Ryder-Cup-format match between the Northern and Southern Texas PGA Sections, running since 1981 and standing at 22&ndash;21&ndash;2. Free to watch, and it lands the day after the Tour event leaves town.",
  "https://www.ntpga.com/texas-joe-black-cup"),
 ("ncaa-regional", "May 17&ndash;19", "2027-05-19", "College",
  "UT Golf Club &middot; Austin", "NCAA Men's Regional Championship",
  "The only home date on either Longhorn golf schedule all season, and the biggest golf Austin gets after November. Both UT teams play every other event of 2026&ndash;27 on the road.",
  "https://texaslonghorns.com/sports/mens-golf/schedule"),
]

SLIDES = [
 ("austin-championship", "Nov 12&ndash;15", "The Austin Championship &middot; PGA Tour",
  "The PGA Tour returns to Austin for the first time since 2023 — and not under the name everyone is still using. Good Good Golf stepped away as title sponsor on 8/27; the event is now the Austin Championship, and ticket sales are paused."),
 ("golf-for-joy", "Nov 8&ndash;9", "Golf for Joy &middot; Grey Rock",
  "Dinner and a live auction downtown on the Sunday, an 11:45am shotgun at Grey Rock on the Monday. Fifteen years and $4 million raised for children's hospital programs."),
 ("pumpkin-open", "Oct 3", "The Pumpkin Open &middot; Hancock",
  "The last event on the City of Austin's 2026 tournament calendar, played over the oldest nine holes in Texas."),
 ("butler-leagues", "Weekly", "Butler Pitch &amp; Putt Leagues",
  "Three standing leagues downtown starting at a $3 buy-in. Turn up on your own and they pair you — this is what carries the Austin winter."),
 ("joe-black-cup", "Nov 16&ndash;17", "Texas Joe Black Cup &middot; Driftwood",
  "North Texas against South Texas in Ryder Cup format, running since 1981, free to watch, the day after the Tour packs up."),
 ("ncaa-regional", "May 17&ndash;19", "NCAA Regional &middot; UT Golf Club",
  "The only home date on either Longhorn schedule all season. Both UT teams play every other event of 2026-27 on the road — then a regional lands on campus."),
]

apply_ = "--apply" in sys.argv
notes = []


def _assert_future(evts):
    """The whole point. The old module shipped three past events because nothing
    ever checked. Never write a card for something that has already happened."""
    stale = [(s, d) for s, _lbl, d, *_r in evts
             if datetime.date.fromisoformat(d) < TODAY]
    if stale:
        raise SystemExit(
            f"REFUSING TO WRITE — these events are already past as of {TODAY_S}: "
            f"{stale}. This guard exists because the module it replaces was "
            "advertising the Texas Amateur, the Firecracker Open and the City "
            "Championship months after they finished.")


_assert_future(EVENTS)

def _host(u):
    """f-strings cannot contain a backslash, so the domain strip lives here."""
    return re.sub(r"https?://(www\.)?", "", u).split("/")[0]

_ENT = re.compile(r'&[a-z]+;|&#\d+;')
def _alt(t):
    return re.sub(r'\s+', ' ', _ENT.sub(' ', t)).strip()

# ------------------------------------------------- 1. the events module
cards = "".join(f'''    <a href="{url}" target="_blank" rel="noopener" class="event-card">
      <div class="event-img">
        <span class="event-date">{lbl}</span>
        <span class="event-type">{typ}</span>
        <img src="{IMG}{stem}.jpg" alt="{_alt(venue)} — {_alt(title)}" style="width:100%;height:100%;object-fit:cover;display:block;" loading="lazy" />
      </div>
      <div class="event-body">
        <div class="event-venue">{venue}</div>
        <div class="event-title">{title}</div>
        <div class="event-desc">{desc}</div>
        <div class="event-source">{_host(url)} ↗</div>
      </div>
    </a>
''' for stem, lbl, _iso, typ, venue, title, desc, url in EVENTS)

MODULE = f'''<section class="events">
  <div class="events-header">
    <div class="events-label">
      <span class="cal-icon">&#9670;</span>
      Austin Events
    </div>
    <span class="events-count"><a href="{URL}" style="color:inherit;text-decoration:none;border-bottom:1px solid currentColor;">{len(EVENTS)} upcoming &mdash; see the full calendar</a></span>
  </div>
  <div class="events-grid">
{cards}  </div>
</section>'''

h = open("index.html", encoding="utf-8").read()
i = h.find('<section class="events">')
if i < 0:
    raise SystemExit("could not find the homepage events module")
j = h.find('</section>', i) + len('</section>')
old = h[i:j]
old_titles = re.findall(r'<div class="event-title">([^<]*)</div>', old)
h = h[:i] + MODULE + h[j:]
notes.append(f"events module rebuilt: {len(old_titles)} cards -> {len(EVENTS)}")
notes.append(f"  removed: {old_titles}")

# ------------------------------------------------------- 2. feed card
CARD = f'''      <div class="card" data-type="field">
    <div class="card-media" style="position:relative;">
      <span class="card-tag grass">[Field Notes]</span>
      <div class="gear-carousel" data-carousel="{KEY}">
        <div class="gear-carousel-track">
''' + "".join(
f'''          <div class="gear-slide">
            <a href="{URL}">
              <img src="{IMG}{s}.jpg" alt="{_alt(n)}" loading="lazy" />
              <div class="gear-slide-info"><div class="gear-slide-brand">{d}</div><div class="gear-slide-name">{n}</div></div>
            </a>
          </div>
''' for s, d, n, _ in SLIDES) + f'''        </div>
        <button class="gear-arrow prev" onclick="gearSlide(this, -1)" aria-label="Previous">&#8249;</button>
        <button class="gear-arrow next" onclick="gearSlide(this, 1)" aria-label="Next">&#8250;</button>
      </div>
    </div>
    <div class="card-body">
      <div class="card-title"><a href="{URL}" style="color:inherit;text-decoration:none;border-bottom:none;">{TITLE}</a></div>
      <div class="card-text" data-slidetext="{KEY}">{SLIDES[0][3]}</div>
      <a href="{URL}" class="card-link">See the calendar ↗</a>
    </div>
  </div>
'''

if CARD.count('onclick="gearSlide(this, -1)"') != 1 or CARD.count('onclick="gearSlide(this, 1)"') != 1:
    raise SystemExit("the new card's gear-arrows are missing their inline onclick")

k = h.find(URL)
if k != -1:
    s = h.rfind('<div class="card"', 0, k)
    depth, jj, end = 0, s, None
    while jj < len(h):
        m = re.compile(r'<div\b|</div>').search(h, jj)
        if not m:
            break
        if m.group(0).startswith("<div"):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                end = m.end(); break
        jj = m.end()
    if end and URL in h[s:end] and '<div class="card"' in h[s:end]:
        h = h[:s] + h[end:]
        notes.append("removed existing feed card")

m = re.search(r'\n\s*<div class="card" data-type="', h)
if not m:
    raise SystemExit("could not locate the feed card list")
h = h[:m.start()] + "\n" + CARD + h[m.start():]

anchor = "  window._slideTexts = {\n"
if h.find(anchor) == -1:
    raise SystemExit("canonical window._slideTexts map not found")
h = re.sub(r'\n?    "' + KEY + r'": \[(?:.*?\n)*?    \],', "", h)
kk = h.find(anchor)
def plain(t):
    for a, b in [("&mdash;", "—"), ("&middot;", "·"), ("&ndash;", "–"),
                 ("&rsquo;", "'"), ("&amp;", "&")]:
        t = t.replace(a, b)
    return t
entry = f'    "{KEY}": [\n' + ",\n".join(
    "      " + json.dumps(plain(t), ensure_ascii=False) for _, _, _, t in SLIDES) + "\n    ],\n"
h = h[:kk + len(anchor)] + entry + h[kk + len(anchor):]

# --------------------------------------------------------- 3. sitemap
sm = open("sitemap.xml", encoding="utf-8").read()
loc = f"https://thegrassyissue.com{URL}"
if loc not in sm:
    sm = sm.replace("</urlset>", f'<url><loc>{loc}</loc><lastmod>{TODAY_S}</lastmod>'
                    f'<changefreq>weekly</changefreq><priority>0.8</priority></url>\n</urlset>')
    notes.append("sitemap: row added (changefreq weekly — it is a calendar)")
else:
    sm = re.sub(r'(<loc>' + re.escape(loc) + r'</loc>\s*<lastmod>)[0-9-]+(</lastmod>)',
                lambda m: m.group(1) + TODAY_S + m.group(2), sm)
    notes.append("sitemap: lastmod bumped")

# ---------------------------------------------------------- guards
if "Firecracker Open" in MODULE or "Texas Amateur" in MODULE:
    raise SystemExit("a past event is back in the homepage module")
if re.search(r'Good Good Championship(?!.{0,120}(stepped away|Formerly|former))', MODULE, re.S):
    raise SystemExit("the homepage must not present the event under the retired sponsor name")
if h.count('<section class="events">') != 1:
    raise SystemExit("the events module was duplicated")

if apply_:
    open("index.html", "w", encoding="utf-8").write(h)
    open("sitemap.xml", "w", encoding="utf-8").write(sm)
    print(f"homepage events module rebuilt with {len(EVENTS)} future events + feed card inserted")
else:
    print("DRY RUN — pass --apply")
for n in notes:
    print(" ", n)
