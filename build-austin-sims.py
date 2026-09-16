#!/usr/bin/env python3
"""The Austin indoor simulator guide — a full-treatment rebuild.

WHY THIS REPLACES THE OLD POST
------------------------------
/drops/7-indoor-simulators-for-austins-gross-rainy-days was a Layer-2 generated
page: 1,291 words, seven venues, one flat "The Collection — 7 Pieces" section,
no gallery, no FAQ. It was also WRONG about two of its seven. Lenny asked for a
refresh on 2026-09-16 on the premise that "a bunch of new options have opened up."
The premise is correct. The specifics were not the ones he had in mind.

THE TWO CORRECTIONS ARE THE REASON THIS IS URGENT
  Five Iron Golf — the old post links to it and describes it as a place you can
  go. Checked fiveirongolf.com/locations directly on 9/16/26: 42 venues, Texas is
  Dallas-Fort Worth only, and /locations/austin, /austin and /locations/austin-tx
  all return 404. The 501 Congress lease was signed 2026-01-20. No opening date
  has been announced since.

  Southside Golf Co — also on the old post as operating. Their own site on
  9/16/26: "Southside Golf Co is opening in September 2026. Join the opening list
  for facility updates and first access when TrackMan bay reservations go live."
  Online booking still says COMING SOON. It is close. It is not open.

Both are guarded below. Neither may appear outside the "Coming" section.

WHAT THIS POST IS
Fourteen venues a reader can actually book this week, five more on the way, and
an at-a-glance table so nobody has to read fourteen paragraphs to find the
cheapest bay. Scope per Lenny, 9/16: full metro including San Marcos; members-only
venues included with the caveat; retail and fitting bays excluded; and where a
price is not published, we say so and link to booking rather than print a number
we did not verify.

WHY THIS IS DATA-LED RATHER THAN PHOTO-LED
Twelve of the fourteen run JavaScript sites with no usable photography — Golfinity's
rebuilt site serves zero <img> tags, Back Nine's location page carries one coach
headshot, Spare Birdie is all logos on a Popmenu CDN. Rather than pad the page with
stock interiors or, worse, illustrate one venue with another venue's room, the
guide leads on the comparison table and gives each venue a fact-dense entry. Only
X-Golf Cedar Park and Fiber Golf publish real, location-specific photographs, and
those are the only two that get galleries. Same rule as the events post: no venue
gets a photograph of a room it is not.

PRICES WE DELIBERATELY DO NOT PRINT
ROK Golf (nothing published anywhere on their site), Bogey Master (behind the
yourgolfbooking widget), Halftime Co. (not published), 1872's public drop-in rate
(memberships are published, the hourly is not). Each says so and links out.
1872's junior membership shows $125 on the card and $175 in the body text of the
same page — no junior figure is printed.

OCEAN'S GOLFER IS DELIBERATELY ABSENT. It would be the only GOLFZON Vision
Premium room in the metro, which is genuinely a different product. But opened in
a browser on 9/16/26 its booking widget reads "Calendar isn't available yet," the
page renders 426 characters, and the footer says (c)2021. Cannot confirm it
operates. Flagged to Lenny to call before it goes in.

PIN SEEKER'S closed 2024-11-01 and its site and bay-prices page are STILL LIVE,
which is how it keeps surfacing in search. Guarded so it never lands here.

FAQ MARKUP: <details class="faq-q"><summary>. TWITTER: og: mirrored to twitter:.
BANNED WORD: 'worth'. DATE FORMAT: numeric M/D/YY.
"""
import re, os, json
import sims_map
import sims_cards

SLUG = "austin-indoor-golf-simulators"
OLD_SLUG = "7-indoor-simulators-for-austins-gross-rainy-days"
IMG = "/images/austin-sims/"
TODAY = "9/16/26"
TITLE = "Every Indoor Golf Simulator in Austin, Ranked by What You Actually Want"
PLAIN = "Every Indoor Golf Simulator in Austin, Ranked by What You Actually Want"
DESC = ("Fourteen indoor golf simulators across the Austin metro you can book this week "
        "— verified tech, bay counts, hourly rates and membership pricing — plus the five "
        "on the way and the two that are not open yet despite what you have read.")

# ---------------------------------------------------------------- the venues
# (key, name, where, tech, hourly, access, url)  — hourly None = not published
TABLE = [
 ("aig",   "Austin Indoor Golf", "Pflugerville",  "Full Swing",        "$25&ndash;35", "Staffed",   "https://www.austinindoorgolf.com/"),
 ("spare", "Spare Birdie",       "Cedar Park",    "Full Swing",        "$30&ndash;40", "Staffed",   "https://www.sparebirdie.com/virtual-bays"),
 ("drg",   "Dr. Golf Studio",    "NW Austin",     "TrackMan / GCQuad", "$30&ndash;60", "Staffed",   "https://www.drgolfstudio.com/"),
 ("atx",   "ATX Indoor Golf Club","SW Austin",    "TrackMan iO",       "$40&ndash;50", "24/7",      "https://atxindoorgolfclub.com/"),
 ("swing", "Swing Station",      "San Marcos",    "Full Swing",        "$45&ndash;60", "Staffed",   "https://swingstationgolf.com/"),
 ("b9",    "The Back Nine",      "8 locations",   "Full Swing",        "$50&ndash;60", "24/7",      "https://thebackninegolf.com/local/all-locations"),
 ("golfi", "Golfinity",          "N FM 620",      "TrackMan / Uneekor","$50&ndash;100","Staffed",   "https://golfinity.com/book-a-bay"),
 ("xgolf", "X-Golf Cedar Park",  "Cedar Park",    "X-Golf",            "$55&ndash;65", "Staffed",   "https://playxgolf.com/locations/cedar-park/"),
 ("fiber", "Fiber Golf",         "SW Austin",     "TrackMan iO",       "$70",          "24/7",      "https://fibergolf.com/"),
 ("rok",   "ROK Golf",           "Westlake / Bee Cave","TrackMan",     None,           "Staffed",   "https://www.rokgolf.com/"),
 ("bogey", "Bogey Master",       "Hutto",         "TrackMan",          None,           "24/7",      "https://bogeymastergolf.com/"),
 ("1872",  "1872 Golf Club",     "Georgetown",    "Foresight",         None,           "Staffed",   "https://1872gc.com/"),
 ("half",  "Halftime Co.",       "Kyle",          "Simulator",         None,           "24/7",      "https://halftimeco.com/"),
 ("cave",  "Man Cave Golf Club", "Dripping Springs","TrackMan",        "Members",      "24/7",      "https://mancavegolfclub.com/"),
]

INTRO = """<div class="writeup">
  <div class="writeup-body">
    <p>Austin has fourteen indoor golf simulators you can book this week, and four of them did not exist eighteen months ago. That is the real story, and it broke out somewhere almost nobody was watching. The new rooms opened in <strong>Georgetown, Hutto, San Marcos and far southwest Austin</strong>. Downtown still has none. The one announced for Congress Avenue has a signed lease and no date.</p>
    <p>The other shift is a split in what a simulator even is. On one side, the staffed room with a kitchen and a bar and somebody who sets up your bay &mdash; Golfinity, X-Golf, ROK, Spare Birdie, 1872. On the other, the unstaffed 24/7 box you enter with a door code texted to your phone, where nobody takes your order because nobody is there. Fiber Golf, The Back Nine, Bogey Master, ATX, Man Cave. The second model is the one multiplying, and ROK now argues against it by name on their own homepage: &ldquo;full-service, not self-serve.&rdquo;</p>
    <p>Two housekeeping notes before the list, because both are currently wrong on a lot of Austin golf coverage including, until today, ours. <strong>Five Iron Golf is not open.</strong> The lease at 501 Congress was signed in January; their live locations page lists forty-two venues and Austin is not among them. <strong>Southside Golf Co is not open either</strong> &mdash; their own site says &ldquo;opening in September 2026&rdquo; and booking is still switched off. Both are in the Coming section below, where they belong.</p>
    <p>Rates below are per bay unless noted, and a bay generally holds four. Where a venue does not publish a price, we say so and point you at their booking page rather than invent a figure.</p>
  </div>
</div>
"""


def table():
    th = ('text-align:left;padding:9px 8px;border-bottom:1px solid var(--ink);'
          'font-family:var(--mono);font-size:10px;letter-spacing:.14em;'
          'text-transform:uppercase;font-weight:400;opacity:.6;')
    td = 'padding:9px 8px;border-bottom:1px solid rgba(0,0,0,.08);font-size:14px;'
    rows = ""
    for _k, name, where, tech, hourly, access, url in TABLE:
        rate = hourly if hourly else '<span style="opacity:.55;">not published</span>'
        rows += (f'<tr><td style="{td}"><a href="{url}" target="_blank" rel="noopener" '
                 f'style="border-bottom:1px solid rgba(0,0,0,.25);">{name}</a></td>'
                 f'<td style="{td}">{where}</td><td style="{td}">{tech}</td>'
                 f'<td style="{td}font-family:var(--mono);font-size:13px;">{rate}</td>'
                 f'<td style="{td}font-family:var(--mono);font-size:11px;letter-spacing:.08em;'
                 f'text-transform:uppercase;opacity:.7;">{access}</td></tr>\n        ')
    return f"""<section class="products">
  <h2 class="products-hdr">All Fourteen, At a Glance</h2>
  <p class="cat-kicker">Rooms are sorted by hourly rate, and every figure here was read on the venue&rsquo;s own site on {TODAY}.</p>
  <div class="writeup-body">
    <div style="overflow-x:auto;">
    <table style="width:100%;border-collapse:collapse;min-width:640px;">
      <thead><tr>
        <th style="{th}">Venue</th><th style="{th}">Where</th><th style="{th}">Tech</th>
        <th style="{th}">Per Hour</th><th style="{th}">Access</th>
      </tr></thead>
      <tbody>
        {rows}</tbody>
    </table>
    </div>
    <p style="font-size:13px;opacity:.65;margin-top:14px;">Man Cave is membership-only &mdash; there is no drop-in rate. Four venues do not publish an hourly figure anywhere; those entries link straight to booking.</p>
  </div>
</section>
"""


def gallery(key, stems, alts):
    fr = "\n        ".join(
        f'<img src="{IMG}{s}.jpg" alt="{a}" loading="lazy" />' for s, a in zip(stems, alts))
    dots = "".join(f'<span class="pg-dot{" on" if i == 0 else ""}"></span>' for i in range(len(stems)))
    return f"""<div class="product-gallery" data-gallery="{key}">
      <div class="pg-frame"><div class="pg-track">
        {fr}
      </div></div>
      <button class="pg-arw prev" aria-label="Previous">&#8249;</button>
      <button class="pg-arw next" aria-label="Next">&#8250;</button>
      <div class="pg-dots">{dots}</div>
      <div class="pg-count">1 / {len(stems)}</div>
    </div>"""


def card(key, brand, name, desc, url, stems, alts):
    return f"""<div class="product-card">
    {gallery(key, stems, alts)}
    <div class="product-body">
      <div class="product-brand">{brand}</div>
      <div class="product-name">{name}</div>
      <div class="product-desc">{desc}</div>
      <a href="{url}" class="product-link" target="_blank" rel="noopener">Book a bay &#8599;</a>
    </div>
  </div>"""


# --------------------------------------------- the eight Back Nine locations
# Every address, phone and rate read off that location's own page on 9/16/26.
# Note the branding oddity: the venue Back Nine calls "Round Rock" has a Hutto
# address. We print the address, because that is where the reader drives.
B9 = [
 ("Austin, TX &ndash; South",   "3601 Davis Ln #300, Austin 78749",           "512-617-3337", "$60"),
 ("Austin, TX &ndash; East",    "2023 Airport Blvd, Austin 78722",            "737-363-4653", "$50"),
 ("Austin, TX &ndash; Westlake","3801 N Capital of Texas Hwy D-160, Austin 78746", "512-764-6463", "$60"),
 ("Cedar Park &ndash; Lakeline","12617 Ridgeline Blvd Ste C101, Cedar Park 78613", "512-759-6463", "$55"),
 ("Pflugerville",               "2606 W Pecan St #202, Pflugerville 78660",   "737-266-4653", "$55"),
 ("Round Rock",                 "101 Star Ranch Blvd N #101, Hutto 78634",    "512-737-7222", "$55"),
 ("Leander",                    "11700 Hero Way W #160, Leander 78641",       "512-331-2259", None),
 ("Kyle",                       "340 E FM 150, Building 3 Ste 100, Kyle 78640", "512-737-7263", None),
]


def b9_table():
    th = ('text-align:left;padding:9px 8px;border-bottom:1px solid var(--ink);'
          'font-family:var(--mono);font-size:10px;letter-spacing:.14em;'
          'text-transform:uppercase;font-weight:400;opacity:.6;')
    td = 'padding:9px 8px;border-bottom:1px solid rgba(0,0,0,.08);font-size:14px;'
    rows = ""
    for name, addr, phone, rate in B9:
        r = f"{rate}/hr" if rate else '<span style="opacity:.55;">not published</span>'
        rows += (f'<tr><td style="{td}"><strong>{name}</strong></td>'
                 f'<td style="{td}">{addr}</td>'
                 f'<td style="{td}font-family:var(--mono);font-size:12px;">{phone}</td>'
                 f'<td style="{td}font-family:var(--mono);font-size:13px;">{r}</td></tr>\n        ')
    return f"""<div class="writeup-body">
    <p style="font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;opacity:.6;margin-bottom:6px;">All eight Back Nine locations</p>
    <div style="overflow-x:auto;">
    <table style="width:100%;border-collapse:collapse;min-width:620px;">
      <thead><tr><th style="{th}">Location</th><th style="{th}">Address</th><th style="{th}">Phone</th><th style="{th}">From</th></tr></thead>
      <tbody>
        {rows}</tbody>
    </table>
    </div>
    <p style="font-size:13px;opacity:.65;margin-top:12px;">Rates differ by room, so check the one you are driving to. The venue branded Round Rock has a Hutto address. Kyle and Leander publish no hourly figure.</p>
  </div>
"""


# ------------------------------------------------------------------ sections
BIG = """<section class="products">
  <h2 class="products-hdr">The Big Rooms</h2>
  <p class="cat-kicker">Somebody sets up your bay, runs the kitchen and keeps the glass full.</p>
  """ + sims_cards.grid(["xgolf", "rok"]) + """
  <div class="writeup-body">
    <p><strong>Golfinity &mdash; 12332 N FM 620, Building B.</strong> The biggest room in the city at twenty bays, and the only one that lets you choose your launch monitor by price. TrackMan bays upstairs at $100 an hour; Uneekor and Foresight downstairs at $50. Additional players are $25 each. Six membership tiers from $49 a month for perks and discounts up to $399 for unlimited play across every bay. The Range Bar and Grill does full service, five PGA coaches are on staff, and Club Champion fits clubs on site. Open 9 to 9 Monday through Saturday, 10 to 6 Sunday. One caveat: older coverage describes twenty-two bays and a GEARS unit, and the current site says twenty and mentions no GEARS. Call if the specific bay matters.</p>
    <p><strong>Spare Birdie &mdash; 1400 Discovery Blvd, Cedar Park.</strong> The cheapest confirmed bay in the metro and it is not close: <strong>$30 an hour</strong> Sunday through Thursday and until 4:30 on Friday and Saturday, $40 after that. The catch, if it is one, is that this is a Full Swing multi-sport bay inside a full entertainment room &mdash; golf plus soccer, football, hockey and Laser Shot, up to ten people, with bowling, darts, pool and bocce in the same building and a Southern kitchen and cocktail bar attached. It is the official postgame spot of the Texas Stars. Closed Mondays.</p>
  </div>
</section>
"""

SELF = """<section class="products">
  <h2 class="products-hdr">The 24/7 Box</h2>
  <p class="cat-kicker">A door code arrives by text. Nobody is there. This is the model that is multiplying.</p>
  """ + sims_cards.grid(["fiber", "atx", "bogey"]) + """
  <div class="writeup-body">
    <p><strong>The Back Nine &mdash; eight locations.</strong> This is the change most people have missed. What used to be one southwest Austin room is now eight across the metro. Full Swing throughout, 24/7 keyless, and a proper iOS and Android app for booking. Rates differ by room &mdash; $60 an hour at South, $50 at East &mdash; so check the one you are driving to. Memberships at South run Par $225, Birdie $295 and Eagle $535 a month, all cheaper on three-, six- or twelve-month prepay, with the annual upfront Par landing at $2,100. South and East are flagged Cross-Play, meaning your membership works at both. Note the old southwest Austin URL now redirects: that venue is called Austin, TX &ndash; South.</p>
  </div>
  """ + b9_table() + """
</section>
"""

COACH = """<section class="products">
  <h2 class="products-hdr">If You Are There to Get Better</h2>
  <p class="cat-kicker">One room in Austin is a coaching academy that happens to rent bays, rather than the reverse.</p>
  """ + sims_cards.grid(["drg"]) + """
</section>
"""

BURBS = """<section class="products">
  <h2 class="products-hdr">Out Past the Toll Roads</h2>
  <p class="cat-kicker">Three of the four rooms that opened in the last year are out here, not in town.</p>
  """ + sims_cards.grid(["1872", "swing", "aig"]) + """
  <div class="writeup-body">
    <p><strong>Halftime Co. &mdash; Plum Creek Business Park, Kyle.</strong> The only option in Kyle, open since 10/30/23 under owner Justin Baker. Two simulators, 300-plus courses, and a thirty-foot putting lab included in the bay rental, which is unusual anywhere and unheard of at this size. Members get 24 hours Monday to Saturday; the public gets 10 to 9 weekdays and 12 to 8 Saturday. Bring your own beer, borrow their clubs. No rate is published, and no street address either &mdash; which is also why they are the one room missing from the map above.</p>
  </div>
</section>
"""

MEMBERS = """<section class="products">
  <h2 class="products-hdr">Members Only</h2>
  <p class="cat-kicker">You cannot drop in here. It earns a place because the number is hard to argue with.</p>
  """ + sims_cards.grid(["cave"]) + """
</section>
"""

COMING = """<section class="products">
  <h2 class="products-hdr">On the Way</h2>
  <p class="cat-kicker">Five more, with what is actually known about each. None of these is bookable today.</p>
  <div class="writeup-body">
    <p><strong>Southside Golf Co &mdash; 11215 Conroy Lane, Manchaca. Opening September 2026.</strong> Four private TrackMan bays from PGA professional Justin Aragon, with published rates already up: $60 per bay per hour off-peak, $75 anytime, up to four players with no per-player fee. Reservations will open five days ahead with a two-hour maximum. Instruction, fitting, club repair and regripping alongside the bays. Their site still says opening list rather than book now, so check before you drive out.</p>
    <p><strong>Another Nine &mdash; 210 Blue Springs Blvd, Georgetown. December 2026.</strong> TrackMan iO on Virtual Golf 3 with 350-plus courses, and a different shape to everyone else: <strong>fully private self-service suites</strong> rather than open bays, up to five guests each, 24/7, hourly, no membership required, mini fridge in every suite. Franchise owner Soham Thakker. It is the first Austin-area room for a nineteen-location national chain, and it will give Georgetown two simulators by January.</p>
    <p><strong>Golf Lounge 18 &mdash; 12901 N I-35, Shops at Tech Ridge. Build-out to February 2027.</strong> Twelve thousand square feet, TrackMan, 450-plus courses, full bar and kitchen. The state filing puts a $500,000 interior build across 11,600 square feet running from late September into February. It would be the chain&rsquo;s fourteenth location and its first in Texas, and the largest sim project announced for the metro.</p>
    <p><strong>512 Golf Co &mdash; &ldquo;Central Austin,&rdquo; 2026.</strong> Six to eight private Foresight bays, a tour-quality putting green, and &mdash; the actual idea &mdash; <strong>coworking</strong>: hot desks, private offices and conference rooms in the same building. Golf-only from $299 a month, golf plus coworking from $599, private offices $1,500, a two-person team suite $2,400, capped at a hundred memberships a tier. They are taking $99 refundable deposits. No address has been published and the site has not been touched since December 2025, so treat the timeline with care.</p>
    <p><strong>Five Iron Golf &mdash; 501 Congress Avenue. No date.</strong> Thirteen and a half thousand square feet, twelve TrackMan simulators, a full bar and restaurant, duckpin bowling, event space, Callaway Tour fitting and a connected fitness facility with locker rooms. The lease was signed 1/20/26. Nothing since. When it lands it will be the only simulator downtown, which remains the strangest gap on this map.</p>
  </div>
</section>
"""

CHOOSE = """<section class="products">
  <h2 class="products-hdr">How to Pick One</h2>
  <p class="cat-kicker">Answer these four and fourteen rooms come down to two.</p>
  <div class="writeup-body">
    <p><strong>Do you want a person there?</strong> This is the biggest fork. Staffed rooms set up your bay, bring food and drink, and have somebody to ask when the software sulks. Unstaffed rooms are cheaper per hour, open at 2am, and entirely your problem if the projector drops. If you have never hit into a screen before, go somewhere staffed the first time.</p>
    <p><strong>Are you practising or drinking?</strong> Practice means data you can act on: TrackMan or GCQuad, a coach in the building, and video you keep. Dr. Golf Studio, ROK and Golfinity&rsquo;s upstairs bays are built for that. Drinking means a kitchen, a group of six and games that are not golf &mdash; Spare Birdie, X-Golf, 1872.</p>
    <p><strong>How many of you are there?</strong> Almost everywhere charges per bay, not per head, so a foursome at Fiber Golf&rsquo;s $70 is $17.50 each while a single at Spare Birdie&rsquo;s $30 is $30. The exception is Golfinity, which adds $25 a player. Austin Indoor Golf at $25 for the whole bay is the outright cheapest way to get four people swinging indoors in this city.</p>
    <p><strong>How often, honestly?</strong> The membership maths is brutal and simple. Man Cave at $107 a month beats paying $50 an hour the moment you play three times. The Back Nine&rsquo;s Par tier at $225 needs four or five visits. If you are going once a quarter, ignore every membership on this page and pay by the hour.</p>
  </div>
</section>
"""

TECH = """<section class="products">
  <h2 class="products-hdr">What the Launch Monitor Actually Does</h2>
  <p class="cat-kicker">Five systems are in use across these fourteen rooms, and no two of them measure the ball the same way.</p>
  <div class="writeup-body">
    <p>Every venue on this page leads with its hardware, which is useless information unless you know what the hardware does. Here is the short version, described as each manufacturer describes itself rather than ranked, because the right one depends entirely on what you walked in to do.</p>
    <p><strong>TrackMan</strong> is radar. It tracks the ball through the air by Doppler, which is why it started life on tour ranges and driving ranges rather than indoors. ROK runs one radar plus two cameras and uses <strong>RCT balls</strong> &mdash; Titleist balls with a marker the camera can read for spin, which matters because indoors the ball hits a screen long before radar would otherwise see enough flight. In Austin: Golfinity upstairs, ROK, Bogey Master, Man Cave, Dr. Golf Studio&rsquo;s Studio Bay 5.</p>
    <p><strong>TrackMan iO</strong> is the newer indoor-specific unit, mounted overhead rather than sat behind you, which is how a room with two bays and no space to spare can still run TrackMan. Fiber Golf and ATX Indoor Golf Club both run it, and Another Nine will when it opens in Georgetown.</p>
    <p><strong>Full Swing</strong> pairs infrared with a high-speed camera. It is the most widely installed system in this metro by some distance &mdash; The Back Nine across all eight rooms, Spare Birdie, Swing Station and Austin Indoor Golf all run it, which means the majority of simulator golf played in Austin is played on Full Swing.</p>
    <p><strong>Foresight</strong> is photometric: cameras only, reading the ball and clubface off high-speed images at impact rather than tracking flight. <strong>GCQuad</strong> is the four-camera unit in that family. 1872 Golf Club in Georgetown runs Foresight, 512 Golf Co will, and Dr. Golf Studio keeps a GCQuad in Bay 6.</p>
    <p><strong>X-Golf</strong> is proprietary and the outlier: the Cedar Park room combines a camera, an infrared laser and a physical impact sensor rather than committing to one method. It is also the only system here you cannot buy for your garage.</p>
    <p>One thing none of the above measures: <strong>your body</strong>. That is what <strong>GEARS</strong> does &mdash; full three-dimensional motion capture of how you move, not where the ball went &mdash; and it has just returned to ROK&rsquo;s Westlake room as a 90-minute evaluation run only by senior instructor Phil Snow. It is the only installation of it on this list.</p>
  </div>
</section>
"""

# Break-even is computed against each venue's OWN published hourly rate, so the
# comparison is like-for-like. Rooms with no published hourly rate cannot appear
# here at all — that is the same rule as the main table.
BREAKEVEN = [
 ("Austin Indoor Golf &mdash; Executive", "$49.99", "3 hrs included",        "$35 peak",  "about 1.5 hrs"),
 ("Dr. Golf Studio &mdash; single, non-peak", "$90", "open bays free",       "$30",       "3 hrs"),
 ("Golfinity &mdash; Social",           "$99",     "8 hrs downstairs",       "$50",       "2 hrs"),
 ("Man Cave Golf Club",                 "$107.17", "unlimited, 24/7",        "&mdash;",   "2 hrs at $50 elsewhere"),
 ("ATX Indoor Golf Club",               "$150",    "24/7 access",            "$50",       "3 hrs"),
 ("X-Golf &mdash; Weekday Warrior",     "$175",    "1 hr/day, Mon&ndash;Thu","$55",       "about 3 hrs"),
 ("Golfinity &mdash; Performance",      "$199",    "8 hrs TrackMan",         "$100",      "2 hrs"),
 ("The Back Nine &mdash; Par",          "$225",    "unlimited, 1-hr slots",  "$60 South", "under 4 hrs"),
 ("Fiber Golf",                         "$250",    "membership",             "$70",       "about 3.5 hrs"),
 ("The Back Nine &mdash; Birdie",       "$295",    "unlimited, 2-hr slots",  "$60 South", "about 5 hrs"),
]


def breakeven():
    th = ('text-align:left;padding:9px 8px;border-bottom:1px solid var(--ink);'
          'font-family:var(--mono);font-size:10px;letter-spacing:.14em;'
          'text-transform:uppercase;font-weight:400;opacity:.6;')
    td = 'padding:9px 8px;border-bottom:1px solid rgba(0,0,0,.08);font-size:14px;'
    rows = ""
    for name, cost, inc, hourly, be in BREAKEVEN:
        rows += (f'<tr><td style="{td}">{name}</td>'
                 f'<td style="{td}font-family:var(--mono);font-size:13px;">{cost}</td>'
                 f'<td style="{td}">{inc}</td>'
                 f'<td style="{td}font-family:var(--mono);font-size:13px;">{hourly}</td>'
                 f'<td style="{td}"><strong>{be}</strong></td></tr>\n        ')
    return f"""<section class="products">
  <h2 class="products-hdr">When a Membership Starts Paying</h2>
  <p class="cat-kicker">Every tier here is measured against that same venue&rsquo;s own hourly rate, so the comparison is like for like.</p>
  <div class="writeup-body">
    <p>Simulator memberships look expensive until you divide. The figure that matters is not the monthly price, it is how many hours a month you would have to play before the membership costs less than just booking a bay &mdash; and for most of these rooms that number is between two and five hours. Which is to say: if you go twice a month, join. If you go twice a quarter, do not.</p>
    <div style="overflow-x:auto;">
    <table style="width:100%;border-collapse:collapse;min-width:680px;">
      <thead><tr>
        <th style="{th}">Membership</th><th style="{th}">Per Month</th><th style="{th}">Includes</th>
        <th style="{th}">Their Hourly</th><th style="{th}">Breaks Even At</th>
      </tr></thead>
      <tbody>
        {rows}</tbody>
    </table>
    </div>
    <p style="font-size:13px;opacity:.65;margin-top:14px;">Unlimited tiers keep improving past break-even; capped-hour tiers do not, so the hours you are given are the hours to judge them on. ROK, Bogey Master, Halftime Co. and 1872 are absent because none publishes an hourly rate to measure a membership against. Dr. Golf Studio&rsquo;s figures are promotional through 9/30/26. Man Cave is membership-only, so its comparison is against what you would pay somewhere else.</p>
  </div>
</section>
"""

FIRST = """<section class="products">
  <h2 class="products-hdr">Before You Go the First Time</h2>
  <p class="cat-kicker">Each of these differs room to room and will otherwise catch you out at the door.</p>
  <div class="writeup-body">
    <p><strong>The rate is for the bay, not for you.</strong> Almost everywhere on this page charges per bay and lets four people use it, so the per-head cost collapses the moment you bring friends. A foursome in Fiber Golf&rsquo;s $70 bay pays $17.50 each. The exception is Golfinity, which adds $25 per additional player.</p>
    <p><strong>Clubs are not a given.</strong> Bogey Master requires you to bring your own &mdash; that is stated plainly on their site. Austin Indoor Golf rents a right-handed set for $20 and has <strong>no left-handed rentals at all</strong>, which is the single most useful sentence in this guide if you play left-handed. Halftime Co. lends clubs. Check before you drive out.</p>
    <p><strong>Balls sometimes come with the room.</strong> Austin Indoor Golf includes Titleist Pro V1s and tees in the rate. ROK uses RCT balls because their TrackMan cameras need the marker to read spin. Most others supply whatever is in the bay.</p>
    <p><strong>The drinking rules are all over the place.</strong> Bogey Master, ATX Indoor Golf Club, Swing Station and Halftime Co. all welcome BYOB. Austin Indoor Golf holds a TABC licence and sells beer, wine and seltzers itself, so outside alcohol is prohibited there &mdash; though outside food is explicitly welcome, which is the reverse of most places. X-Golf, Golfinity, Spare Birdie, ROK and 1872 pour their own.</p>
    <p><strong>Unstaffed means unstaffed.</strong> At Bogey Master a door code arrives by text and the door opens fifteen minutes before your slot. Fiber Golf, The Back Nine, ATX and Man Cave work the same way. Nobody is coming to fix the projector, and nobody is coming to take your order either. Go somewhere staffed for a first visit.</p>
    <p><strong>One accessibility note, because they say it themselves.</strong> Austin Indoor Golf&rsquo;s single bay sits on a mezzanine reached by stairs, with no elevator, and their FAQ states it is not wheelchair accessible. It is also the cheapest room in the metro, which makes the trade-off a real one to flag rather than bury.</p>
  </div>
</section>
"""

FAQ_ITEMS = [
 ("Is Five Iron Golf open in Austin yet?",
  "No. Five Iron signed a lease for 501 Congress Avenue on 1/20/26 for a 13,500 square foot flagship with twelve TrackMan simulators, but as of 9/16/26 Austin does not appear on their live locations page, which lists 42 venues with Dallas-Fort Worth as the only Texas entry. No opening date has been announced."),
 ("Is Southside Golf Co open?",
  "Not quite. As of 9/16/26 their own site says the facility is opening in September 2026 and that online booking is coming soon. Published rates are already up at $60 per bay per hour off-peak and $75 anytime, covering up to four players, but reservations are not live yet. It is the closest of the five to opening."),
 ("What is the cheapest golf simulator in Austin?",
  "Austin Indoor Golf in Pflugerville at $25 an hour off-peak, which covers the whole bay for up to four players with no per-guest fee. Spare Birdie in Cedar Park is the cheapest in-town option at $30 an hour Sunday through Thursday. Both are per bay rather than per person."),
 ("Which Austin simulators are open 24 hours?",
  "Fiber Golf, The Back Nine at all eight locations, ATX Indoor Golf Club, Bogey Master in Hutto and Man Cave Golf Club in Dripping Springs all run unstaffed 24/7 access with a door code. Halftime Co. and 1872 Golf Club give members 24-hour access but keep shorter staffed hours for the public."),
 ("Which simulator has TrackMan?",
  "Golfinity's upstairs bays, ROK Golf at both locations, Bogey Master, Man Cave and Dr. Golf Studio's Studio Bay 5 all run TrackMan. Fiber Golf and ATX Indoor Golf Club run the newer TrackMan iO. The Back Nine, Spare Birdie, Swing Station and Austin Indoor Golf run Full Swing; 1872 runs Foresight; X-Golf runs its own proprietary system."),
 ("Can I bring my own beer to an Austin golf simulator?",
  "At several, yes. Bogey Master, ATX Indoor Golf Club, Swing Station and Halftime Co. all welcome BYOB. Austin Indoor Golf holds a TABC licence and sells beer and wine itself, so outside alcohol is prohibited there, though outside food is explicitly welcome. X-Golf, Golfinity, Spare Birdie, ROK and 1872 all serve alcohol on site."),
 ("Is there a golf simulator in downtown Austin?",
  "No. As of 9/16/26 there is no indoor simulator in downtown Austin. Five Iron's 501 Congress location would be the first, and it has no announced opening date. The nearest options are ROK Golf in Westlake and ATX Indoor Golf Club on US 290."),
]

# verify-post.py requires the FAQ wrapper to be <div class="faq">, not a <section>:
# the FAQPage-schema check looks for '<div class="faq"' specifically, so that a page
# carrying the schema provably carries the visible copy too. Matches the events post.
FAQ = ('<h2 class="products-hdr">Questions</h2>\n<div class="faq">\n'
       + "".join(f'  <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>\n'
                 for q, a in FAQ_ITEMS) + '</div>\n')


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
                  lambda m, v=v: m.group(1) + v + m.group(2), head)
for k, v in [("twitter:title", PLAIN), ("twitter:description", DESC)]:
    head = re.sub(rf'(<meta name="{k}" content=")[^"]*(")',
                  lambda m, v=v: m.group(1) + v + m.group(2), head)
for pat, val in [(r'(<link rel="canonical" href=")[^"]*(")', f"https://thegrassyissue.com/drops/{SLUG}"),
                 (r'(<meta property="og:url" content=")[^"]*(")', f"https://thegrassyissue.com/drops/{SLUG}"),
                 (r'(<meta property="og:image" content=")[^"]*(")', f"https://thegrassyissue.com{IMG}xgolf-sim.jpg")]:
    head = re.sub(pat, lambda m, v=val: m.group(1) + v + m.group(2), head)
head = re.sub(r'<script type="application/ld\+json">.*?</script>',
              lambda m: '<script type="application/ld+json">' + json.dumps(SCHEMA) + '</script>',
              head, flags=re.S)

body = ('<div class="breadcrumb">\n  <a href="/">Feed</a><span>/</span>\n'
        '  <a href="/#feed">Guides</a><span>/</span>\n  Austin Indoor Simulators</div>\n'
        f'<header class="drop-header">\n  <h1>{TITLE}</h1>\n  <div class="drop-meta">\n'
        f'    <span>{TODAY}</span><span class="dot"></span>\n'
        '    <span>Guide</span><span class="dot"></span>\n'
        f'    <span>Austin, Texas &middot; {len(TABLE)} Rooms</span>\n  </div>\n</header>\n\n'
        f'<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}xgolf-sim.jpg" '
        'alt="A private simulator bay at X-Golf Cedar Park, one of fourteen indoor golf simulators in the Austin metro" /></div></div>\n'
        + INTRO + table() + sims_map.section() + BIG + SELF + COACH + BURBS + MEMBERS
        + TECH + breakeven() + FIRST + COMING + CHOOSE + FAQ)

# ------------------------------------------------------------------- guards
_txt = st(re.sub(r'<[^>]+>', ' ', body))

_w = re.sub(r'\bFort\s+Worth\b', ' ', _txt, flags=re.I)
if re.search(r'\bworth\b', _w, re.I):
    raise SystemExit("BANNED WORD 'worth' in the body copy")

if len(TABLE) != 14:
    raise SystemExit(f"the guide is built around fourteen open rooms; TABLE has {len(TABLE)}")
if len({t[0] for t in TABLE}) != len(TABLE):
    raise SystemExit("duplicate venue key in TABLE")

# The two corrections are the whole point. Neither may be presented as open.
for name, why in [("Five Iron", "42 locations live on 9/16/26, Austin not among them, /locations/austin 404s"),
                  ("Southside", "their own site says 'opening in September 2026', booking still off")]:
    for m in re.finditer(re.escape(name), _txt):
        seg = _txt[max(0, m.start() - 400): m.end() + 400].lower()
        # "on the way" is the map legend's own heading for the unopened column,
        # so it counts as not-open context exactly like the prose phrasings do
        if not any(k in seg for k in ("not open", "no date", "opening", "coming", "not quite",
                                      "does not appear", "lease", "on the way")):
            raise SystemExit(f"{name} appears without the not-open context ({why})")
# The intro SHOULD name both corrections — that is the lede. What must never happen
# is either one appearing among the venue sections, where a reader would take it as
# a room they can book. Those sections only.
for nm in ("Five Iron", "Southside"):
    if nm in st(BIG + SELF + COACH + BURBS + MEMBERS):
        raise SystemExit(f"{nm} is not open — it may appear in the intro, the Coming "
                         f"section and the FAQ, never among the bookable venues")

# Venues we established do not belong here at all.
for banned, why in [("Pin Seeker", "closed 2024-11-01; its site and prices page are still live"),
                    ("Ocean's Golfer", "booking calendar dead, (c)2021 footer — unconfirmed"),
                    ("Oceans Golfer", "same"),
                    ("Pac Golf", "reported closed"),
                    ("Puttshack", "no Austin location"),
                    ("Mulligans", "Bertram is outside the metro")]:
    if banned.lower() in _txt.lower():
        raise SystemExit(f"{banned} does not belong in this guide — {why}")

# Prices we could not verify must never be printed.
UNPRICED = {"rok": "ROK Golf", "bogey": "Bogey Master", "half": "Halftime Co.", "1872": "1872 Golf Club"}
for k, nm in UNPRICED.items():
    row = [t for t in TABLE if t[0] == k][0]
    if row[4] is not None:
        raise SystemExit(f"{nm} has no published hourly rate — the table must show 'not published'")
if re.search(r"junior[^.]{0,60}\$\s?1[27]5", _txt, re.I):
    raise SystemExit("1872's junior tier shows $125 and $175 on the same page — print neither")

if len(B9) != 8:
    raise SystemExit(f"The Back Nine runs eight Austin-metro rooms; B9 has {len(B9)}")
if len({a for _n, a, _p, _r in B9}) != 8:
    raise SystemExit("two Back Nine rows share an address")
for _n, _a, _p, _r in B9:
    if not re.match(r'^[\d()\-. ]{10,16}$', _p):
        raise SystemExit(f"Back Nine {_n}: phone {_p!r} does not look like a phone number")
# Break-even may only cite a venue whose hourly rate we actually publish.
_unpriced_names = ("ROK", "Bogey Master", "Halftime", "1872")
for _row in BREAKEVEN:
    if any(u in _row[0] for u in _unpriced_names):
        raise SystemExit(f"{_row[0]} publishes no hourly rate — it cannot carry a break-even")

_map_open = [m for m in sims_map.PINS if m[4] == "open"]
_map_coming = [m for m in sims_map.PINS if m[4] == "coming"]
if len(_map_open) != 21:
    raise SystemExit(f"map should plot 21 open rooms (14 venues, Back Nine as 8); got {len(_map_open)}")
if len(_map_coming) != 4:
    raise SystemExit(f"map should plot 4 coming rooms; got {len(_map_coming)}")
if len({(m[2], m[3]) for m in sims_map.PINS}) != len(sims_map.PINS):
    raise SystemExit("two map pins share a coordinate")
for m in sims_map.PINS:
    if not (29.82 <= m[2] <= 30.78 and -98.20 <= m[3] <= -97.45):
        raise SystemExit(f"{m[1]} is outside the metro frame — check the geocode")
_approx = [m[1] for m in sims_map.PINS if not m[5]]
if len(_approx) != 4:
    raise SystemExit(f"four venues are centroid-placed and must stay marked; got {_approx}")
if 'dasharray' not in body:
    raise SystemExit("the approximate pins lost their dashed ring — precision must stay visible")
for _absent in ("Halftime", "512 Golf"):
    if _absent not in _txt:
        raise SystemExit(f"{_absent} has no plottable address and the map note must say so")

_ncards, _nframes = sims_cards.check()
if _ncards != 10:
    raise SystemExit(f"ten venues have real photography and should have boxes; got {_ncards}")
for _k in sims_cards.CARDS:
    if f'data-gallery="{_k}"' not in body:
        raise SystemExit(f"card {_k} was built but never placed in the body")
# A venue with no photography of its own must never borrow another venue's.
for _noimg in ("Golfinity", "Spare Birdie", "Halftime"):
    if _noimg not in _txt:
        raise SystemExit(f"{_noimg} has no imagery and must still appear as prose")
_nboxes = body.count('class="product-card"')
if _nboxes != 10:
    raise SystemExit(f"expected 10 venue boxes, found {_nboxes}")

_imgs = re.findall(r'src="(/images/austin-sims/[\w.-]+)"', body)
_gone = [p for p in _imgs if not os.path.exists("." + p)]
if _gone:
    raise SystemExit(f"images missing on disk: {_gone}")
if len(_imgs) != len(set(_imgs)):
    raise SystemExit("an image is used twice on the page")

_words = len(_txt.split())
if _words < 1200:
    raise SystemExit(f"word count {_words} is below the 1200 floor")
if body.count('<details class="faq-q">') != len(FAQ_ITEMS):
    raise SystemExit("FAQ markup must be <details class=\"faq-q\">")

for key, n in [("xgolf", 2), ("fiber", 4)]:
    if body.count(f'data-gallery="{key}"') != 1:
        raise SystemExit(f"gallery {key} missing or duplicated")
    blk = body[body.find(f'data-gallery="{key}"'):]
    blk = blk[:blk.find("</div>\n    <div class=\"product-body\"")]
    # count the dots, not the wrapper: 'pg-dot' is a prefix of 'pg-dots'
    _dots = len(re.findall(r'class="pg-dot(?: on)?"', blk))
    if blk.count("<img") != n or _dots != n:
        raise SystemExit(f"gallery {key}: {blk.count('<img')} images and {_dots} dots, both must be {n}")

open(f"drops/{SLUG}.html", "w", encoding="utf-8").write(head + body + tail)
print(f"wrote drops/{SLUG}.html | {len(TABLE)} open rooms | 5 coming | ~{_words} words")
print(f"  galleries: X-Golf (2 frames), Fiber Golf (4 frames)")
print(f"  unpriced and linked to booking: {', '.join(UNPRICED.values())}")
