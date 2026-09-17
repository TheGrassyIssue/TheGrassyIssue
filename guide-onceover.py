#!/usr/bin/env python3
"""Austin Golf Guide once-over — 17 September 2026. Stale content out, three
factual defects fixed, one duplication of my own making cleaned up.

THE SERIOUS ONE: THE LIONS RENOVATION CARD
------------------------------------------
The guide carried a card headlined "Lions Muny Is Getting a World-Class
Renovation", promising "a full redesign from Gil Hanse ... what's planned, what's
changing, and when it's happening". Three things wrong with it:

  1. THE ARCHITECT LOOKS WRONG. Nothing I can find attaches Gil Hanse to Lions.
     The name that is documented — including on TGI's own sourced Lions deep dive
     — is BILL COORE AND BEN CRENSHAW, who proposed a restoration in 2017 and
     offered their design work at no cost.
  2. IT IS NOT HAPPENING YET. The Coore & Crenshaw plan is a proposal contingent
     on a lease that is still running on short extensions; the Texas legislature
     extended the Save Historic Muny District through May 2027. "Is getting" and
     "when it's happening" state as settled something that is not.
  3. THE LINK WAS DEAD. The slug
     /drops/lions-muny-is-getting-a-world-class-renovation-heres-whats-c is
     truncated and no such page has ever existed. The pillar page was serving a
     404 from its own News section.

Replaced with a card pointing at the Lions deep dive that actually exists, saying
only what that page sources. No architect is named in the card that is not named
on the destination.

DATED CONTENT REMOVED
---------------------
  * THE WORLD CUP CARD. Austin hosted in 2026; the tournament finished in July.
    "Austin is a host city in 2026. Where to watch matches" is a present-tense
    promise about a past event sitting on an evergreen guide. The POST stays
    live — this only removes its card from the guide.

  * "Public 18s ran $93 to $127 through late August" (Kissing Tree) — past tense
    and a price band with no year on it.

  * "recently renovated" (Fazio Canyons) — undated and drifts by definition.

  * Two date stamps re-dated: the hero eyebrow and the muni price table.

MUNI RATES VERIFIED, NOT CHANGED
--------------------------------
Read from austintexas.gov/golfatx/fees-memberships on 17 September 2026 and every
figure on the page is still correct: $35 Mon-Thu / $41 Fri / $44 Sat-Sun-Holiday
at Lions, Morris Williams, Roy Kizer and Jimmy Clay; sunset $28; Hancock $20
flat. The City still labels the schedule "New Fees Effective 10/1/2025" and has
posted nothing for FY27, so the table is re-dated rather than re-priced.

THE SIMULATOR CARD WAS COUNTING WRONG
-------------------------------------
It said "7 Spots" and used the old headline. The post now covers fourteen open
sims. Card brought in line with what it links to.

A DUPLICATION I CREATED YESTERDAY
---------------------------------
incorporate-special-day-guide.py promoted Vaaler Creek and Kissing Tree into full
special-course entries in section 02 — but both already had honourable-mention
entries further down, so each course appeared twice on one page. The hon entries
carried detail the new blocks did not (Vaaler's designer, yardage and ranking;
Kissing Tree's designer, Audubon status and cart rules), so this MERGES that
detail up into the special-course blocks and then removes the duplicates, rather
than deleting either outright.
"""
import re, os, sys, json

apply_ = "--apply" in sys.argv
P = "field-guide/index.html"
t = open(P, encoding="utf-8").read()
orig = t
log, missed, problems = [], [], []


def sub(old, new, note, count=1):
    global t
    n = t.count(old)
    if n == 0:
        missed.append(f"{note}  —  {old[:70]}")
        return
    if n != count:
        problems.append(f"{note}: expected {count}, found {n}")
        return
    t = t.replace(old, new)
    log.append(f"{note}  (x{n})")


def drop_card(slug, note):
    """Remove a whole <a class="guide-card"> block by its href."""
    global t
    i = t.find(slug)
    if i < 0:
        missed.append(f"{note} — card not found")
        return
    s = t.rfind('<a href="', 0, i)
    e = t.find("</a>", i) + 4
    # eat the trailing whitespace/newline so the grid does not gain a blank slot
    while e < len(t) and t[e] in " \n\r\t":
        e += 1
    t = t[:s] + t[e:]
    log.append(note)


def drop_hon(name, note):
    """Remove a whole <div class="hon-item"> block by its hon-name."""
    global t
    i = t.find(f'<div class="hon-name">{name}')
    if i < 0:
        missed.append(f"{note} — hon-item not found")
        return
    s = t.rfind('<div class="hon-item">', 0, i)
    nxt = t.find('<div class="hon-item">', i)
    end = t.find("</section>", i)
    e = nxt if 0 < nxt < end else end
    t = t[:s] + t[e:]
    log.append(note)


# ==================================================== 1. the Lions card
OLD_LIONS = '''<a href="/drops/lions-muny-is-getting-a-world-class-renovation-heres-whats-c" class="guide-card">
      <img class="guide-card-img" src="/images/field-guide/renovation.jpg" alt="Golf course under renovation with earth movers reshaping the landscape" loading="lazy" />
      <div class="guide-card-body">
        <div class="guide-card-tag">News · Renovation</div>
        <div class="guide-card-title">Lions Muny Is Getting a World-Class Renovation</div>
        <div class="guide-card-desc">The historic course is getting a full redesign from Gil Hanse. What's planned, what's changing, and when it's happening.</div>
        <span class="guide-card-link">Read the story →</span>
      </div>
    </a>'''
NEW_LIONS = '''<a href="/drops/lions-municipal-golf-course-austin" class="guide-card">
      <img class="guide-card-img" src="/images/lions/course.jpg" alt="Fairway and live oaks at Lions Municipal Golf Course in Austin" loading="lazy" />
      <div class="guide-card-body">
        <div class="guide-card-tag">History · Lions Muny</div>
        <div class="guide-card-title">The Most Important Muni in Texas Is Still Open</div>
        <div class="guide-card-desc">The first integrated course in the South, a lease running on short extensions, and a Coore &amp; Crenshaw restoration offered for free and still waiting. Go play it.</div>
        <span class="guide-card-link">Read the story →</span>
      </div>
    </a>'''
sub(OLD_LIONS, NEW_LIONS, "Lions card: dead slug + unsupported Gil Hanse claim replaced")

sub("From the Firecracker Open — 81 years running at Lions — to the Gil Hanse renovation that's about to transform the Muny, there's always something happening in Austin golf.",
    "From the Firecracker Open &mdash; 81 years running at Lions &mdash; to the Coore &amp; Crenshaw restoration that has been offered to the Muny for free and is still waiting on a lease, there's always something happening in Austin golf.",
    "section 05 intro: Hanse claim corrected to the sourced Coore & Crenshaw proposal")

# ================================================ 2. dated content out
drop_card("/drops/where-to-watch-the-world-cup-in-austin",
          "World Cup card removed — the 2026 tournament finished in July (the post stays live)")

sub('<div class="guide-card-tag">Simulators · 7 Spots</div>',
    '<div class="guide-card-tag">Simulators &middot; 14 Spots</div>', "sims card: count 7 -> 14")
sub("<div class=\"guide-card-title\">7 Indoor Simulators for Austin's Gross Rainy Days</div>",
    '<div class="guide-card-title">Every Indoor Golf Simulator in Austin, Ranked</div>',
    "sims card: headline matched to the post")
sub("When it's 105° or sideways rain, these sim spots keep your swing alive. TrackMan bays, leagues, and full-bar setups across town.",
    "Fourteen sims across the metro you can book this week &mdash; verified tech, bay counts and hourly rates, plus the five on the way.",
    "sims card: description matched to the post")

sub("Fazio Canyons is the headliner — a recently renovated Tom Fazio design through Hill Country canyons",
    "Fazio Canyons is the headliner &mdash; a Tom Fazio design through Hill Country canyons",
    "'recently renovated' removed — undated by construction")

sub("<span>Updated August 2026</span>", "<span>Updated September 2026</span>",
    "hero eyebrow re-dated")
sub("and day trips. Updated August 2026.", "and day trips. Updated September 2026.",
    "meta description re-dated")
sub("Green fees current as of July 2026 · Updated quarterly",
    "Green fees read 17 September 2026 &middot; City schedule effective 1 Oct 2025",
    "muni price table: re-dated and sourced to the City's own effective date")

# ========================= 3. merge the duplicated courses, then de-dupe
sub("Cart-inclusive pricing is rarer than it should be and means you know the real cost before you leave the house. The back nine winds through live oaks and creek beds.",
    "Cart-inclusive pricing is rarer than it should be and means you know the real cost before you leave the house. A Michael Lowry design at 6,946 yards, ranked #10 in Texas by the Dallas Morning News, with a restored 1860s ranch house for a clubhouse and a shaded deck over the 18th.",
    "Vaaler Creek: detail merged up from its honourable mention")

sub("Tee times book through Troon rather than the club's own sheet, so the price is generated at the point of booking &mdash; go through the engine rather than expecting a posted rate.",
    "A Gary Stephenson design that opened in October 2018, certified as an Audubon Signature Sanctuary and irrigated entirely with reclaimed water. The thing to know: the surrounding community is 55-and-over, the golf course is not &mdash; Kissing Tree runs a separate public tee sheet and anyone can book it, through Troon rather than the club's own page. Read the cart rules first: no non-playing riders, two players per cart, and check in no more than sixty minutes before your time.",
    "Kissing Tree: detail merged up from its honourable mention")

drop_hon("Vaaler Creek", "Vaaler Creek honourable mention removed (now a full entry above)")
drop_hon("Kissing Tree", "Kissing Tree honourable mention removed (now a full entry above)")

# ============================================================== guards
_removed_cards = orig.count('class="guide-card"') - t.count('class="guide-card"')
_removed_hon = orig.count('class="hon-item"') - t.count('class="hon-item"')
if _removed_cards != 1:
    problems.append(f"{_removed_cards} guide-cards removed, expected exactly 1 (World Cup)")
if _removed_hon != 2:
    problems.append(f"{_removed_hon} hon-items removed, expected exactly 2")
for tag in ("<div", "<section", "<a ", "<details", "<img"):
    if t.count(tag) > orig.count(tag):
        problems.append(f"{tag!r} count grew — a removal added markup")
for o, c in (("<div", "</div>"), ("<a ", "</a>"), ("<section", "</section>"),
             ("<details", "</details>")):
    if t.count(o) != t.count(c):
        problems.append(f"unbalanced {o} / {c}")

# nothing may still point at a page that does not exist
for u in sorted(set(re.findall(r'href="(/[^"#][^"]*)"', t))):
    p = u.lstrip("/")
    if not (os.path.exists(p) or os.path.exists(p + ".html")
            or os.path.exists(os.path.join(p, "index.html"))):
        problems.append(f"dead internal link: {u}")

# the claims this script exists to kill must be gone
for dead, why in (("Gil Hanse", "unsupported architect attribution"),
                  ("World Cup", "dated event content"),
                  ("lions-muny-is-getting", "dead slug"),
                  ("recently renovated", "undated qualifier"),
                  ("$93 to $127", "stale undated price band"),
                  ("Updated August 2026", "stale date stamp")):
    if dead in t:
        problems.append(f"{dead!r} survived — {why}")

# no course may appear twice as both a full entry and an honourable mention
_full = set(re.findall(r'<div class="special-course-name">(.*?)</div>', t))
_hon = set(re.findall(r'<div class="hon-name">(.*?)</div>', t))
_dupe = _full & _hon
if _dupe:
    problems.append(f"course listed twice on the page: {sorted(_dupe)}")

# muni rates must still read exactly what the City publishes (verified 17/9/26)
for fee in ("$35", "$41", "$44", "$20"):
    if fee not in t:
        problems.append(f"verified City rate {fee} went missing")

for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
    json.loads(b)
for img in re.findall(r'<img[^>]+src="(/images/[^"]+)"', t):
    if not os.path.exists(img.lstrip("/")):
        problems.append(f"missing image: {img}")
if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", t), re.I):
    problems.append("banned word 'worth' in the copy")

if problems:
    raise SystemExit("REFUSED:\n  " + "\n  ".join(problems))

if apply_:
    open(P, "w", encoding="utf-8").write(t)

print(("applied" if apply_ else "DRY RUN") + f" — once-over on {P}")
for l in log:
    print("  ·", l)
if missed:
    print("\n  NOT FOUND (check by hand):")
    for m in missed:
        print("    !!", m)
# f-strings cannot contain backslashes, so the escaped quotes go in variables first
_GC, _HI, _SC = 'class="guide-card"', 'class="hon-item"', 'class="special-course"'
print(f"\n  guide-cards {orig.count(_GC)} -> {t.count(_GC)}"
      f"  |  hon-items {orig.count(_HI)} -> {t.count(_HI)}"
      f"  |  special-courses {t.count(_SC)}"
      f"  |  {len(t)-len(orig):+,} bytes")
if not apply_:
    print("\npass --apply to write")
