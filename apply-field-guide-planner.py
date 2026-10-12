#!/usr/bin/env python3
"""apply-field-guide-planner.py — adds two sections to the Field Guide (12 October 2026):
  1. "How to book a tee time in Austin" — a booking cheat sheet (#booking)
  2. "When to play golf in Austin" — a month-by-month season planner (#seasons)
Lenny picked these two from the options ("Season planner, Tee-time booking cheat sheet").

FACTS (read 12 Oct 2026; nothing unverified is printed):
  - Golf ATX rules/fees: austintexas.gov/golfatx, /golfatx/fees-memberships, course pages, and the city release
    "Golf ATX weekend tee time reservations move online-only beginning October 27, 2025".
  - Grey Rock: greyrockgolfandtennis.com/golf/rates. Star Ranch: starranchgolf.com/rates. Forest Creek: forestcreek.com
    rates + FAQ. Plum Creek: plumcreekgolf.com/golf/rates. Omni Barton Creek: omnihotels.com .../golf/rates
    (members and registered resort guests only).
  - Climate: NWS Austin/San Antonio 1991–2020 normals, Camp Mabry (weather.gov/media/ewx/climate/ATT*.pdf).
    29 days a year at 100°F+: LCRA summary of the same normals.
  - Overseeding Oct–Nov with rye or Poa trivialis on a bermuda base: City of Austin (austintexas.gov/node/57003).
  - Muni maintenance closures and 2026 events: each Golf ATX course page; austintexas.gov/golfatx/tournaments-results.
NOT printed because unverified: muni evening/sunset start times, muni walking rules (except Hancock, walk-only),
muni cancellation terms, sunrise/sunset times, frost-delay policy, and booking windows at courses whose own sites
publish none. Idempotent: replaces its own marked block. Dry run by default.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
F = ROOT / "field-guide/index.html"
START, END = "<!-- TGI-FG-PLANNER -->", "<!-- /TGI-FG-PLANNER -->"
ANCHOR = "<!-- TGI-METHOD -->"

BOOK_ROWS = [
 # course, how, window, price, notes
 ("Lions, Morris Williams, Roy Kizer, Jimmy Clay", "Golf ATX online (account required), pro shop or phone",
  "Weekdays: 7 days out, from 9am online. Weekends: online only, Monday 8pm for that Saturday and Sunday",
  "$35 Mon&ndash;Thu &middot; $41 Fri &middot; $44 weekends; evening $29&ndash;$34; sunset $28",
  "One weekend tee time per account, up to four players. Cart is $18 a person extra ($12 at sunset). Card only. Each course closes one Monday a month."),
 ("Hancock (9 holes)", "No tee times &mdash; pay station, first come first served", "Walk up",
  "$20; $16 sunset or junior; $18 senior or college", "Walking only. One fee covers play all day."),
 ("Grey Rock", "Online (ezlinks) or 512-288-4297", "7 days out (14 for members)",
  "$90 Mon&ndash;Thu &middot; $105 Fri&ndash;Sun, cart included; walking rate $70 / $85",
  "City of Austin resident card takes $5 off. Cancel 24 hours out or pay a $25 no-show fee per player. Closed the first Tuesday of the month."),
 ("Star Ranch", "Online (ezlinks) or (512) 252-4653", "7 days out (8 for members)",
  "$85&ndash;$99 Mon&ndash;Thu &middot; $129&ndash;$139 Fri&ndash;Sun; after 3pm $62 / $75",
  "Cart and range balls included. Cancel 48 hours out or pay the full fee."),
 ("Forest Creek", "Online or 512-388-2874", "30 days out",
  "Dynamic &mdash; no rate card", "Earlier bookings usually cost less. Walking is allowed."),
 ("Plum Creek", "Online or (512) 262-5555", "Not published &mdash; check the tee sheet",
  "From $70 Mon&ndash;Thu &middot; $100 Fri&ndash;Sun; twilight from 3pm $58 / $70; from 5pm $35 / $45",
  "Juniors 18 and under play free with a paying adult on weekdays, and after 1pm on weekends."),
 ("Falconhead, Avery Ranch, ShadowGlen, Crystal Falls, Vaaler Creek, Kissing Tree", "Each course&rsquo;s own booking engine", "Varies",
  "Dynamic &mdash; check the engine", "These courses publish no fixed booking window on their own sites; GolfNow listings carry GolfNow&rsquo;s terms, not the course&rsquo;s."),
]

MONTHS = [
 ("January", "62&deg; / 42&deg;", "2.64", "Bermuda is dormant and the munis are playing on their winter overseed. Cheap, quiet, cold mornings &mdash; book late-morning tee times."),
 ("February", "67&deg; / 46&deg;", "1.89", "The driest month of the year. Good walking weather and wide-open tee sheets."),
 ("March", "73&deg; / 52&deg;", "2.88", "Spring opens. Aerification starts at the munis (Lions in mid-March, Kizer at the end of the month). The Mid-Am Spring Championship is at Jimmy Clay."),
 ("April", "80&deg; / 59&deg;", "2.42", "Peak season begins and weekend tee times go fast &mdash; be online at 8pm Monday. The Lloyd Morrison Spring Partnership is at Lions."),
 ("May", "87&deg; / 67&deg;", "5.04", "The wettest month. Aerification at every 18-hole muni; check the closure calendar before you book."),
 ("June", "93&deg; / 73&deg;", "3.68", "Play early. Firecracker qualifiers are at Lions, and aerification continues."),
 ("July", "97&deg; / 75&deg;", "1.96", "The Firecracker Open at Lions over the Fourth (July 3&ndash;5 in 2026), which the city calls the oldest amateur tournament in Texas. First tee or last light only."),
 ("August", "98&deg; / 75&deg;", "2.74", "The hottest month. City Championships at Morris Williams, Jimmy Clay, Kizer and Lions at the start of the month. Sunset rounds at $28 make the most sense."),
 ("September", "91&deg; / 70&deg;", "3.45", "Still hot, but the evenings come back. The Junior and Senior City Championships run mid-month."),
 ("October", "83&deg; / 61&deg;", "3.91", "The best month to play in Austin. Courses close for a day or two to overseed &mdash; it happens this month at every muni, so check before you drive."),
 ("November", "72&deg; / 51&deg;", "2.92", "Overseed coming in, mild days, short afternoons. A great month for 36 on a Saturday if you start early."),
 ("December", "64&deg; / 43&deg;", "2.72", "Quiet and cool. Every muni is closed on Christmas Day; holiday rates apply on listed holidays."),
]

def block():
    rows = "\n".join(
        f'          <tr>\n            <td class="course-name">{c}</td>\n            <td>{h}</td>\n            <td>{w}</td>\n            <td class="num">{p}</td>\n            <td>{n}</td>\n          </tr>'
        for c, h, w, p, n in BOOK_ROWS)
    mrows = "\n".join(
        f'          <tr>\n            <td class="course-name">{m}</td>\n            <td class="num">{t}</td>\n            <td class="num">{r} in</td>\n            <td>{note}</td>\n          </tr>'
        for m, t, r, note in MONTHS)
    return f"""{START}
<section class="table-section" id="booking">
  <div class="table-inner">
    <h2 class="table-h2">How to book a tee time in Austin &mdash; the cheat sheet.</h2>
    <div class="table-sub">Booking rules and rates read on each course&rsquo;s own site, October 12, 2026</div>
    <p class="price-note-fine" style="max-width:820px;margin:0 auto 18px;">The one rule that matters most: weekend tee times at the city munis are released online only, at 8pm on the Monday before, and the good ones are gone within minutes. Make a Golf ATX account before then. Weekday times open seven days ahead at 9am.</p>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Course</th>
            <th>How to book</th>
            <th>Tee times open</th>
            <th>18 holes</th>
            <th>Good to know</th>
          </tr>
        </thead>
        <tbody>
{rows}
        </tbody>
      </table>
    </div>
  </div>
</section>
<section class="table-section" id="seasons">
  <div class="table-inner">
    <h2 class="table-h2">When to play golf in Austin &mdash; the season planner.</h2>
    <div class="table-sub">Average high / low and rainfall: NWS 1991&ndash;2020 normals, Camp Mabry &middot; Muni closures and events: City of Austin, 2026</div>
    <p class="price-note-fine" style="max-width:820px;margin:0 auto 18px;">Austin golf has two seasons that matter: March to May and October to November. The city munis are bermuda overseeded with rye or Poa trivialis each fall, so greens change character through the year, and core aerification runs from March to August. Camp Mabry averages 29 days a year at 100&deg; or more. In summer, play at first light or take a sunset rate, and drink water before you are thirsty.</p>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Month</th>
            <th>High / low</th>
            <th>Rain</th>
            <th>What it means for your golf</th>
          </tr>
        </thead>
        <tbody>
{mrows}
        </tbody>
      </table>
    </div>
  </div>
</section>
{END}
"""

def main(apply_):
    t = F.read_text(encoding="utf-8"); orig = t
    if START in t:
        t = t[:t.index(START)] + t[t.index(END) + len(END) + 1:]
    assert ANCHOR in t, "no TGI-METHOD anchor"
    t = t.replace(ANCHOR, block() + ANCHOR, 1)
    toc_old = '<a href="#reference">Quick Reference</a>'
    toc_new = '<a href="#booking">Booking</a>\n      <a href="#seasons">When to Play</a>\n      <a href="#reference">Quick Reference</a>'
    if '<a href="#booking">' not in t and toc_old in t:
        t = t.replace(toc_old, toc_new, 1)
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", block()), re.I):
        sys.exit("! banned word in block")
    print(f"  field-guide: {'changed' if t != orig else 'unchanged'}; booking rows {len(BOOK_ROWS)}, months {len(MONTHS)}")
    if apply_ and t != orig:
        F.write_text(t, encoding="utf-8"); print("  wrote field-guide/index.html")

if __name__ == "__main__":
    main("--apply" in sys.argv)
