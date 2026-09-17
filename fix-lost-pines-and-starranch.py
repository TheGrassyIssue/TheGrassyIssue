#!/usr/bin/env python3
"""Two factual corrections, applied sitewide — 17 September 2026.

1. WOLFDANCER IS NOW LOST PINES RESORT.
   wolfdancergolfclub.com redirects to lostpinesresortandspa.com/golf/. That page
   is titled "Golf at Lost Pines Resort" and the word "Wolfdancer" appears on it
   ZERO times. The course is unchanged — still Arthur Hills, still 7,300 yards,
   par 72 — and the resort's own copy now says "just 20 minutes from Austin",
   where TGI has been saying 30.

   NOT A FIND-AND-REPLACE. Three reasons:
     · "Wolfdancer at Lost Pines" would become "Lost Pines at Lost Pines".
     · The old name is what people still search. Dropping it entirely costs the
       recognition that makes a reader trust the page. First mention on each
       page keeps it as "Lost Pines Resort (formerly Wolfdancer)".
     · Image filenames and alt text describe a real photo of the place; the file
       is not renamed, only the alt text that a reader or crawler sees.

2. THE FIELD GUIDE'S STAR RANCH LINK IS DEAD.
   golfstarranch.com does not resolve. The live site is starranchgolf.com.
   Verified 17 Sept 2026, along with its current rate card: $85-99 Mon-Thu,
   $129-139 Fri/weekends, $62-75 after 3pm.

Every rule below is an exact string with a known context. Anything that does not
match is reported rather than silently skipped, because a rename that half-lands
is worse than one that does not run.
"""
import re, os, sys, html

apply_ = "--apply" in sys.argv

OLD_URL = "https://www.wolfdancergolfclub.com/"
NEW_URL = "https://www.lostpinesresortandspa.com/golf/"

# (file, old, new, note) — exact strings, context-aware
RULES = [
 # ---------- URL swap, safe everywhere ----------
 ("*", OLD_URL, NEW_URL, "course URL -> Lost Pines Resort"),
 ("*", "https://wolfdancergolfclub.com/", NEW_URL, "course URL (no-www) -> Lost Pines Resort"),

 # ---------- Field Guide ----------
 ("field-guide/index.html",
  'alt="Lush resort fairway winding through Texas landscape at Wolfdancer Golf Club"',
  'alt="Lush resort fairway winding through Texas landscape at Lost Pines Resort, formerly Wolfdancer Golf Club"',
  "alt text"),
 ("field-guide/index.html", ">Wolfdancer Golf Club.<", ">Lost Pines Resort.<", "course heading"),
 ("field-guide/index.html", "Resort &middot; Lost Pines &middot; 30 min from downtown",
  "Resort &middot; Lost Pines &middot; 20 min from downtown", "drive time per the resort"),
 ("field-guide/index.html", "Resort · Lost Pines · 30 min from downtown",
  "Resort · Lost Pines · 20 min from downtown", "drive time per the resort"),
 ("field-guide/index.html",
  "The resort play. Wolfdancer sits at the Hyatt Regency Lost Pines",
  "The resort play. Lost Pines Resort &mdash; the course everyone still calls Wolfdancer &mdash; sits at the Hyatt Regency Lost Pines",
  "body copy, keeps the old name once"),
 ("field-guide/index.html",
  "Eight courses within driving distance that feel like a weekend getaway &mdash; Wolfdancer, Vaaler Creek, ColoVista, and more.",
  "Courses within driving distance that feel like a weekend getaway &mdash; Lost Pines Resort, Vaaler Creek, ColoVista, and more.",
  "teaser line"),
 ("field-guide/index.html", "https://www.golfstarranch.com/", "https://www.starranchgolf.com/",
  "DEAD LINK -> live Star Ranch site"),

 # ---------- Road trip post ----------
 ("drops/austin-golf-road-trip.html", "Wolfdancer at Lost Pines", "Lost Pines Resort",
  "meta + schema description"),

 # ---------- Texas courses post ----------
 ("drops/10-texas-courses-worth-the-trip.html", "Wolfdancer at Lost Pines, Horseshoe Bay",
  "Lost Pines Resort, Horseshoe Bay", "intro list"),
 ("drops/10-texas-courses-worth-the-trip.html", ">Wolfdancer Golf Club<", ">Lost Pines Resort<",
  "product name"),
 ("drops/10-texas-courses-worth-the-trip.html",
  "Wolfdancer Golf Club at Hyatt Regency Lost Pines is Arthur Hills&rsquo; best Texas design",
  "Lost Pines Resort &mdash; still Wolfdancer to most people &mdash; at the Hyatt Regency Lost Pines is Arthur Hills&rsquo; best Texas design",
  "body copy, keeps the old name once"),
 ("drops/10-texas-courses-worth-the-trip.html",
  "Wolfdancer Golf Club at Hyatt Regency Lost Pines is Arthur Hills' best Texas design",
  "Lost Pines Resort — still Wolfdancer to most people — at the Hyatt Regency Lost Pines is Arthur Hills' best Texas design",
  "body copy (plain apostrophe variant)"),

 # ---------- Social Club ----------
 ("events/social-club.html", "Wolfdancer at Lost Pines", "Lost Pines Resort out at Bastrop",
  "candidate course list"),

 # ---------- Homepage ----------
 ("index.html", "Wolfdancer &middot; Lost Pines", "Lost Pines Resort", "road-trip slide label"),
 ("index.html", "Wolfdancer · Lost Pines", "Lost Pines Resort", "road-trip slide label"),

 # ---------- remaining exact strings, found by sweeping each file ----------
 ("field-guide/index.html", ">Wolfdancer Golf Club.</div>", ">Lost Pines Resort.</div>", "course name div"),
 ("field-guide/index.html", "Resort · Lost Pines · 30 min from downtown",
  "Resort · Lost Pines · 20 min from downtown", "drive time"),
 ("field-guide/index.html",
  "Eight courses within driving distance that feel like a weekend getaway — Wolfdancer, Vaaler Creek, ColoVista, and more.",
  "Courses within driving distance that feel like a weekend getaway — Lost Pines Resort, Vaaler Creek, ColoVista, and more.",
  "guide-card teaser"),

 ("index.html", 'alt="Wolfdancer Golf Club at Hyatt Lost Pines"',
  'alt="Lost Pines Resort, formerly Wolfdancer Golf Club, at Hyatt Regency Lost Pines"', "alt text"),
 ("index.html", "<!-- 1. Wolfdancer -->", "<!-- 1. Lost Pines Resort -->", "comment"),
 ("index.html", 'alt="Wolfdancer Golf Club — Hill Country elevation view"',
  'alt="Lost Pines Resort — Hill Country elevation view"', "alt text"),
 ("index.html", "#1 · Wolfdancer Golf Club", "#1 · Lost Pines Resort", "slide brand"),
 ("index.html", "Lost Pines · ~30 min east · $150–190",
  "Bastrop · ~20 min east · dynamic pricing", "slide meta"),
 ("index.html", "Arthur Hills carved Wolfdancer through Lost Pines",
  "Arthur Hills carved Lost Pines Resort — still Wolfdancer to most people — through Bastrop", "card text"),
 ("index.html", 'alt="Wolfdancer Golf Club — Lost Pines, TX"',
  'alt="Lost Pines Resort — Bastrop, TX"', "alt text"),
 ("index.html", '<div class="gear-slide-brand">Wolfdancer Golf Club</div>',
  '<div class="gear-slide-brand">Lost Pines Resort</div>', "slide brand"),
 ("index.html", "Day 3: Wolfdancer at Lost Pines —", "Day 3: Lost Pines Resort —", "slideText"),
 ("index.html", "Wolfdancer Golf Club at Hyatt Regency Lost Pines is Arthur Hills' best Texas design",
  "Lost Pines Resort — still Wolfdancer to most people — at the Hyatt Regency is Arthur Hills' best Texas design", "slideText"),

 ("drops/austin-golf-road-trip.html", '<h2 class="day-title">Wolfdancer Golf Club at Lost Pines</h2>',
  '<h2 class="day-title">Lost Pines Resort</h2>', "day title"),
 ("drops/austin-golf-road-trip.html", 'alt="Wolfdancer Golf Club at Hyatt Lost Pines"',
  'alt="Lost Pines Resort, formerly Wolfdancer Golf Club, at Hyatt Regency Lost Pines"', "alt text"),
 ("drops/austin-golf-road-trip.html", '<div class="course-card-name">Wolfdancer Golf Club</div>',
  '<div class="course-card-name">Lost Pines Resort</div>', "course card name"),
 ("drops/austin-golf-road-trip.html", 'alt="Wolfdancer Golf Club course view"',
  'alt="Lost Pines Resort course view"', "alt text"),

 ("drops/10-texas-courses-worth-the-trip.html", 'alt="Wolfdancer Golf Club — Lost Pines, TX"',
  'alt="Lost Pines Resort — Bastrop, TX"', "alt text"),
 ("drops/10-texas-courses-worth-the-trip.html", '<div class="product-brand">Wolfdancer Golf Club</div>',
  '<div class="product-brand">Lost Pines Resort</div>', "product brand"),
]

TARGETS = sorted(set(
    [f for f, *_ in RULES if f != "*"] +
    ["index.html", "field-guide/index.html", "drops/8-special-day-rounds-near-austin.html",
     "drops/10-texas-courses-worth-the-trip.html", "drops/austin-golf-road-trip.html",
     "events/social-club.html"]))

files = {f: open(f, encoding="utf-8").read() for f in TARGETS if os.path.exists(f)}
orig = dict(files)
log, missed = [], []

for f, old, new, note in RULES:
    scope = list(files) if f == "*" else ([f] if f in files else [])
    hit = 0
    for p in scope:
        n = files[p].count(old)
        if n:
            files[p] = files[p].replace(old, new)
            log.append(f"{p:44} {note}  (x{n})")
            hit += n
    if hit == 0 and f != "*":
        missed.append(f"{f}: {note}  —  {old[:64]}")

# ------------------------------------------------------------------- guards
problems = []
for p, t in files.items():
    if OLD_URL in t or "wolfdancergolfclub.com" in t:
        problems.append(f"{p}: the old wolfdancergolfclub.com URL survived")
    if "golfstarranch.com" in t:
        problems.append(f"{p}: the dead golfstarranch.com URL survived")
    if "Lost Pines at Lost Pines" in t or "Lost Pines Resort at Hyatt Regency Lost Pines" in t:
        problems.append(f"{p}: produced a doubled Lost Pines phrase")
    for tag in ("<div", "<section", "<a "):
        if t.count(tag) != orig[p].count(tag):
            problems.append(f"{p}: {tag} count changed — a replacement ate markup")
    if len(t) < len(orig[p]) * 0.97:
        problems.append(f"{p}: lost more than 3% of its bytes")
if problems:
    raise SystemExit("REFUSED:\n  " + "\n  ".join(problems))

if apply_:
    for p, t in files.items():
        if t != orig[p]:
            open(p, "w", encoding="utf-8").write(t)

print(("applied" if apply_ else "DRY RUN") + " — Lost Pines rename + Star Ranch dead link")
for l in log:
    print("  ·", l)
if missed:
    print("\n  NOT FOUND (check these by hand):")
    for m in missed:
        print("    !!", m)
print()
for p, t in files.items():
    if t != orig[p]:
        left = len(re.findall(r"Wolfdancer", t))
        print(f"  {p:44} {len(t)-len(orig[p]):+5d} bytes   'Wolfdancer' left: {left}")
if not apply_:
    print("\npass --apply to write")
