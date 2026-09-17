#!/usr/bin/env python3
"""Fold the rebuilt Special Day post into the Austin Golf Guide — 17 Sept 2026.

The post now runs 10 day trips + 4 overnights on a dated-snapshot price policy.
The Field Guide, which is the pillar page everything else points at, still carried
the old shape: eight step-up courses, a blanket "$50 to $180+" price band, and a
teaser card promoting a course the post no longer lists.

WHAT CHANGES

1. THE PRICE BAND COMES OUT. Section 02's intro said "Prices range from $50 to
   $180+ depending on the day". Half these courses no longer publish a rate at
   all — Falconhead prices dynamically and says so on its own rates page — so the
   band was a number a reader could plan around and be wrong about. Replaced with
   the policy, plus the two rate cards that were actually read today.

2. THREE DAY TRIPS ADDED — Vaaler Creek, Kissing Tree, The Quarry. They are in
   the post and were missing here, which is the wrong way round for a pillar page.
   Inserted before Lost Pines so the section still runs close-in to further-out.

3. AN OVERNIGHT GROUP ADDED — Horseshoe Bay, La Cantera, Lajitas. This is the
   "really long drive" tier Lenny asked for, and it is what the guide had no
   place for at all. Lajitas is seven hours away and earns its spot on the
   rankings ITS OWN SITE PRINTS, attributed to Golfweek and the Dallas Morning
   News rather than asserted by us.

   OMNI BARTON CREEK STAYS WHERE IT IS. It is genuinely 20 minutes from downtown,
   so it belongs in the step-up group even though the post files it under
   overnights for the tee-sheet reason. Its entry gains one line about that
   instead of being moved, because moving it would break the section's
   close-to-far ordering for no reader benefit.

4. THE TEASER CARD stops promising ColoVista, which is not in the rebuilt post.

5. TWO FAQs ADDED — the Wolfdancer rename (people still search the old name and
   deserve to land somewhere that explains it) and why the green fees vanished.
   Appended to the visible FAQ AND to the FAQPage schema, in the same order, or
   the page ships a rich result that does not match what is on screen.

6. THE AT-A-GLANCE VIBE CARD gains the two entries the new tier makes possible.

One new CSS rule, .guide-subhead, because the section has no sub-heading class
and inventing one without a rule would leave a classless element on the page.

Every edit is an exact string. Anything that does not match is reported, not
skipped.
"""
import re, os, sys, json

apply_ = "--apply" in sys.argv
P = "field-guide/index.html"
FG = "/images/field-guide/"
SD = "/images/special-day/"
FEED = "/images/feed/"

t = open(P, encoding="utf-8").read()
orig = t
log, missed, problems = [], [], []


def sub(old, new, note, count=1):
    global t
    n = t.count(old)
    if n == 0:
        missed.append(f"{note}  —  {old[:72]}")
        return
    if n != count:
        problems.append(f"{note}: expected {count} match(es), found {n}")
        return
    t = t.replace(old, new)
    log.append(f"{note}  (x{n})")


def course(img, alt, name, meta, body, stats, url):
    s = "".join(f'<div class="special-course-stat"><span class="label">{k}</span>'
                f'<span class="value">{v}</span></div>' for k, v in stats)
    return f"""  <div class="special-course">
    <img class="special-course-img" src="{img}" alt="{alt}" loading="lazy" />
    <div>
      <div class="special-course-name">{name}</div>
      <div class="special-course-meta">{meta}</div>
      <div class="special-course-body">{body}</div>
      <div class="special-course-stats">{s}</div>
      <a href="{url}" target="_blank" rel="noopener" class="special-course-link">Book a tee time ↗</a>
    </div>
  </div>

"""


# ---------------------------------------------------------------- 1. prices
sub("Prices range from $50 to $180+ depending on the day, so check rates before you book.",
    "Pricing is the tricky part. Most of these courses have moved to dynamic rates "
    "&mdash; Falconhead says so outright on its own page &mdash; so a posted band would "
    "be out of date inside a fortnight. Two still publish a real rate card, read on 17 "
    "September 2026: Star Ranch at $85&ndash;99 Monday to Thursday, and Vaaler Creek at "
    "$95 with the cart included. Everywhere else, check the booking engine before you go, "
    "and remember that twilight is the cheat code &mdash; Star Ranch drops to $62 after three.",
    "section 02 intro: stale $50-180 band replaced with the policy")

# Falconhead's body carries a weekend figure we did not verify today.
sub("Dynamic pricing means weekday afternoons can be surprisingly affordable; weekend mornings run north of $150.",
    "Falconhead prices dynamically and is unusually straight about it &mdash; its rates page "
    "says prices move up and down in real time on demand &mdash; so a quiet weekday afternoon "
    "and a Saturday morning are not the same purchase.",
    "Falconhead: unverified $150 weekend figure removed")

# ------------------------------------------------- 2. three more day trips
ANCHOR = '  <div class="special-course">\n    <img class="special-course-img" src="/images/field-guide/wolfdancer.jpg"'
NEW_DAY = "".join((
 course(FEED + "c68dec72-banner1.jpg",
        "Hill Country fairway framed by live oaks at Vaaler Creek Golf Club",
        "Vaaler Creek Golf Club.", "Public · Blanco · 50 min from downtown",
        "The underrated one, and the drive out through Blanco is half the reason to go. "
        "Rates read on 17 September 2026: $95 for 18 Monday to Thursday with the cart "
        "included, $75 on the twilight rate &mdash; which starts at 3pm from March through "
        "October and 1pm in the winter. Cart-inclusive pricing is rarer than it should be "
        "and means you know the real cost before you leave the house. The back nine winds "
        "through live oaks and creek beds.",
        [("Rate", "$95 Mon&ndash;Thu"), ("Twilight", "$75"),
         ("Walking", "Cart included"), ("Best for", "The drive, midweek value")],
        "https://www.vaalercreekgolfclub.com/"),
 course(FEED + "ed1deed0-slide1.jpg",
        "Hill Country routing at Kissing Tree Golf Club in San Marcos",
        "Kissing Tree Golf Club.", "Semi-private · San Marcos · 45 min from downtown",
        "Forty-five minutes down I-35 and the Hill Country starts doing the work about "
        "halfway. Semi-private with public tee times most days, polished without being "
        "fussy, and conditioned hot year-round. Tee times book through Troon rather than "
        "the club's own sheet, so the price is generated at the point of booking &mdash; go "
        "through the engine rather than expecting a posted rate.",
        [("Booking", "via Troon"), ("Access", "Public times most days"),
         ("Walking", "Cart standard"), ("Best for", "An easy drive that still feels away")],
        "https://www.kissingtreegolfclub.com/"),
 course(FEED + "85a30a62-Quarry-13-Cliff-Edge-scaled-1-1.jpg",
        "Fairway running beneath hundred-foot limestone walls at The Quarry Golf Club",
        "The Quarry Golf Club.", "Public · San Antonio · 1 hr 15 from downtown",
        "The extra half hour past San Marcos buys you the back nine, which drops into a "
        "genuine hundred-year-old quarry pit and plays inside the walls. The front nine is "
        "open and links-adjacent; the transition between the two is the most abrupt and most "
        "enjoyable in Texas golf. This is the one to book when somebody is visiting and you "
        "want them describing it on the flight home.",
        [("Setting", "Working quarry pit"), ("Nines", "Links front, quarry back"),
         ("Walking", "Cart standard"), ("Best for", "Visitors, one-off occasions")],
        "https://quarrygolf.com/")))

if ANCHOR in t:
    t = t.replace(ANCHOR, NEW_DAY + ANCHOR, 1)
    log.append("three day trips inserted before Lost Pines (Vaaler Creek, Kissing Tree, The Quarry)")
else:
    missed.append("could not find the Lost Pines block to insert before")

# Omni Barton keeps its slot in the step-up group — it really is 20 minutes from
# downtown — but gains the line that explains why the post files it as an
# overnight: the room is usually what gets you the tee sheet.
sub("The most impressive golf experience within Austin city limits, no question.",
    "The most impressive golf experience within Austin city limits, no question. It is the "
    "one course on this list where the drive is twenty minutes and staying over is still the "
    "move &mdash; guest tee times come first, so booking a room is often the difference "
    "between playing Fazio Canyons and playing what was left.",
    "Omni Barton: guest-tee-sheet line added")

# ------------------------------------------------------- 3. overnight group
SUBHEAD = """
  <div class="guide-subhead">
    <div class="guide-section-kicker">Make it a weekend</div>
    <h3 class="guide-section-h2">When the drive is long enough to stay over.</h3>
    <p>Three that are too far, or too good, to compress into a single day. Golf at all
    three is priced as part of a stay, so the number you are quoted depends on whether
    you have a room, which package you booked and the time of year.</p>
  </div>

"""
NEW_NIGHT = "".join((
 course(FEED + "89123d8f-Ram-Rock-Aerial-Water-Shot-1920x920-min.jpg",
        "Aerial view of the Ram Rock course along Lake LBJ at Horseshoe Bay Resort",
        "Horseshoe Bay Resort.", "Resort · Horseshoe Bay · 1 hr 15 northwest",
        "Four courses on one property &mdash; Ram Rock, Apple Rock, Slick Rock and Summit "
        "Rock &mdash; which is the entire argument for staying the night instead of driving "
        "out and back. Ram Rock is the hard one and has been since it opened. Apple Rock is "
        "the one people come home talking about. Two nights lets you play all four and still "
        "eat dinner like a person.",
        [("Courses", "Four"), ("Drive", "~1 hr 15 NW"),
         ("Pricing", "Resort rates"), ("Best for", "A full golf weekend")],
        "https://www.hsbresort.com/golf/"),
 course(SD + "lacantera.jpg",
        "Quarry ledge and Hill Country fairway at La Cantera Golf Club near San Antonio",
        "La Cantera Golf Club.", "Resort · San Antonio · 1 hr 15 south",
        "Cut into quarry and Hill Country ledge just north of San Antonio, and close enough "
        "that you could day-trip it &mdash; but the resort is the reason not to. The property "
        "pairs the golf with the Resort &amp; Spa, which turns a long Saturday into a real "
        "weekend and means nobody drives home tired. The pick when half the group is not "
        "playing.",
        [("Setting", "Quarry &amp; ledge"), ("Drive", "~1 hr 15 south"),
         ("Pricing", "Resort rates"), ("Best for", "Mixed groups, anniversaries")],
        "https://www.lacanteragolfclub.com/"),
 course(SD + "lajitas.jpg",
        "Putting green at dusk below the Chihuahuan Desert mesas at Black Jack's Crossing, Lajitas Golf Resort",
        "Lajitas Golf Resort &mdash; Black Jack&rsquo;s Crossing.",
        "Resort · Lajitas · 7 hours west",
        "The far end of the list and the one that needs real commitment: seven hours west, on "
        "the Rio Grande at the edge of Big Bend, in country that looks like nowhere else in "
        "Texas. Lajitas prints the accolades on its own page &mdash; Golfweek ranks Black "
        "Jack&rsquo;s Crossing the #1 Course You Can Play in Texas and #38 Resort Course in "
        "the USA, and the Dallas Morning News has had it at #1 in Texas since 2013. Go for "
        "three nights or do not go.",
        [("Drive", "~7 hrs west"), ("Setting", "Rio Grande, Big Bend"),
         ("Pricing", "Resort rates"), ("Best for", "The trip of the year")],
        "https://www.lajitasgolfresort.com/golf/")))

# Append inside section 02, just before its closing tag. The anchor is the
# </section> that immediately precedes the NEW GUIDE SECTIONS comment — that is
# section 02's close and nothing else's.
MARK = "<!-- ==================== NEW GUIDE SECTIONS ==================== -->"
_i = t.find(MARK)
_c = t.rfind("</section>", 0, _i)
if _i < 0 or _c < 0:
    missed.append("could not find the end of section 02 to append the overnight group")
else:
    t = t[:_c] + SUBHEAD + NEW_NIGHT + t[_c:]
    log.append("overnight group appended to section 02 (Horseshoe Bay, La Cantera, Lajitas)")

# ------------------------------------------------------------ 4. teaser card
sub("Courses within driving distance that feel like a weekend getaway — Lost Pines Resort, Vaaler Creek, ColoVista, and more.",
    "Ten day trips inside an hour and a quarter, plus four overnights that reach as far as Big Bend.",
    "teaser card copy (ColoVista is no longer in the post)")
sub("Courses within driving distance that feel like a weekend getaway &mdash; Lost Pines Resort, Vaaler Creek, ColoVista, and more.",
    "Ten day trips inside an hour and a quarter, plus four overnights that reach as far as Big Bend.",
    "teaser card copy (entity form)")

# ------------------------------------------------------------------ 5. FAQs
NEW_FAQ = [
 ("What happened to Wolfdancer Golf Club?",
  "It is now branded Lost Pines Resort. The old wolfdancergolfclub.com address redirects to the resort's own golf page, which no longer uses the Wolfdancer name anywhere. The course is unchanged — the same Arthur Hills design out at Bastrop — and the resort's current copy puts it about 20 minutes from Austin."),
 ("Why do so many courses near Austin no longer list a green fee?",
  "Dynamic pricing. Rates move with demand, tee time, day of week and season, the way airline seats do. Falconhead states this openly on its rates page. Others book through Troon or GolfNow, where the price is generated at the point of booking. A course that still posts a fixed rate card — Vaaler Creek and Star Ranch both do — is now the exception rather than the rule."),
]
_last = t.rfind("</details>")
if _last < 0:
    problems.append("no FAQ block found")
else:
    ins = "\n" + "\n".join(f'<details class="faq-q"><summary>{q}</summary><p>{a}</p></details>'
                           for q, a in NEW_FAQ)
    t = t[:_last + len("</details>")] + ins + t[_last + len("</details>"):]
    log.append(f"{len(NEW_FAQ)} FAQs appended to the visible list")

# ...and the same two into the FAQPage schema, in the same order
_ms = [m for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
       if '"FAQPage"' in m.group(1)]
if not _ms:
    problems.append("no FAQPage schema to extend")
else:
    m = _ms[0]
    d = json.loads(m.group(1))
    ent = d.get("mainEntity") or next((g["mainEntity"] for g in d.get("@graph", [])
                                       if g.get("@type") == "FAQPage"), None)
    if ent is None:
        problems.append("FAQPage schema has no mainEntity to extend")
    else:
        ent.extend({"@type": "Question", "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in NEW_FAQ)
        t = t[:m.start()] + ('<script type="application/ld+json">' +
                             json.dumps(d, ensure_ascii=False) + "</script>") + t[m.end():]
        log.append(f"schema mainEntity extended to {len(ent)} questions")

# --------------------------------------------------------- 6. at-a-glance
sub('<li><span>Toughest test</span><span class="ref">ShadowGlen</span></li>',
    '<li><span>Toughest test</span><span class="ref">ShadowGlen</span></li>'
    '<li><span>Visitors you want to impress</span><span class="ref">The Quarry</span></li>'
    '<li><span>Stay the night</span><span class="ref">Horseshoe Bay (four courses)</span></li>',
    "at-a-glance vibe card: two entries added")

# ------------------------------------------------------------------- CSS
CSS_RULE = (".guide-subhead { margin: 48px 0 32px; padding-top: 32px; "
            "border-top: 1px solid rgba(0,0,0,0.12); max-width: 720px; }\n"
            ".guide-subhead p { font-family: var(--serif); font-size: 17px; "
            "line-height: 1.55; opacity: 0.8; margin-top: 8px; }\n")
if ".guide-subhead" not in re.sub(r'class="guide-subhead"', "", t[:t.find("</style>")]):
    t = t.replace("</style>", CSS_RULE + "</style>", 1)
    log.append("added the .guide-subhead CSS rule")

# ------------------------------------------------------------------ guards
# Exact expected deltas. Six new courses, each contributing 8 divs (special-course,
# its inner wrapper, name, meta, body, stats, and 4 stat divs = 10 — counted below
# from the generated markup rather than asserted, so the number cannot drift) plus
# one .guide-subhead wrapper. Sections must not change at all: if the count moved,
# an insertion landed outside section 02.
_added = NEW_DAY + NEW_NIGHT + SUBHEAD
for tag, extra in (("<section", 0), ("<a ", _added.count("<a ")),
                   ("<div", _added.count("<div")), ("<details", 2)):
    exp = orig.count(tag) + extra
    if t.count(tag) != exp:
        problems.append(f"{tag!r} count is {t.count(tag)}, expected {exp} "
                        f"— an edit ate or duplicated markup")
if t.count("<div") != t.count("</div>"):
    problems.append("unbalanced divs")
if t.count("<a ") != t.count("</a>"):
    problems.append("unbalanced anchors")
if t.count("<details") != t.count("</details>"):
    problems.append("unbalanced details")
# ColoVista keeps its honourable-mention entry in the guide — it is a real Bastrop
# course with real copy here. What it must NOT do is appear in the teaser card for
# a post that no longer lists it, which is the only thing this guard is about.
if "ColoVista" in "".join(re.findall(r'<div class="guide-card-desc">(.*?)</div>', t, re.S)):
    problems.append("the Special Day teaser card still promotes ColoVista, which is not in the post")
if "$50 to $180" in t:
    problems.append("the stale price band survived")
if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", t), re.I):
    problems.append("banned word 'worth' present in the guide copy")
for img in re.findall(r'<img[^>]+src="(/images/[^"]+)"', t):
    if not os.path.exists(img.lstrip("/")):
        problems.append(f"missing image on disk: {img}")
for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
    try:
        json.loads(b)
    except Exception as e:
        problems.append(f"JSON-LD no longer parses: {e}")
# visible FAQ count must match schema count
_vis = len(re.findall(r'<details class="faq-q">', t))
_sch = 0
for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
    if '"FAQPage"' in b:
        d = json.loads(b)
        e_ = d.get("mainEntity") or next((g["mainEntity"] for g in d.get("@graph", [])
                                          if g.get("@type") == "FAQPage"), [])
        _sch = len(e_)
        break
if _vis != _sch:
    problems.append(f"visible FAQ ({_vis}) does not match FAQPage schema ({_sch})")

if problems:
    raise SystemExit("REFUSED:\n  " + "\n  ".join(problems))

if apply_:
    open(P, "w", encoding="utf-8").write(t)

print(("applied" if apply_ else "DRY RUN") + f" — Special Day folded into {P}")
for l in log:
    print("  ·", l)
if missed:
    print("\n  NOT FOUND (check by hand):")
    for m_ in missed:
        print("    !!", m_)
_n = len(re.findall(r'class="special-course"', t))
print(f"\n  special-course blocks: {len(re.findall(chr(34)+'special-course'+chr(34), orig))} -> {_n}"
      f"  |  FAQs: {_vis} visible / {_sch} schema  |  {len(t)-len(orig):+,} bytes")
if not apply_:
    print("\npass --apply to write")
