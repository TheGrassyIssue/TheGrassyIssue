#!/usr/bin/env python3
"""Bring the Special Day homepage card and its sitewide references in line with
the rebuilt post — 17 September 2026.

The post was rebuilt as 10 day trips + 4 overnights and moved to a dated-snapshot
price policy. The homepage card still carried the old numbers, and they are the
part a reader sees first:

  Omni Barton Creek   ~$275      -> resort rates (guest rate varies by package)
  Horseshoe Bay       ~$250      -> resort rates
  Vaaler Creek        $75-110    -> $95 Mon-Thu, cart included (read 17 Sept 2026)
  Falconhead          $52-78     -> dynamic pricing (its own rates page says so)
  Avery Ranch         $75-78     -> check rates
  Kissing Tree        $100-130   -> books via Troon
  The Quarry          $59-79     -> check rates

Three more things fixed while in here:

  * "Thirty minutes east" for Lost Pines. The resort's own copy says twenty.
  * The Vaaler Creek slide text ends "worth every one of them" — a banned word in
    TGI copy that predates this session and would have shipped again untouched.
  * The card title still said "8". The post is no longer eight of anything.

CARD TITLE DROPS THE NUMBER RATHER THAN BECOMING "14". The slug stays
8-special-day-rounds-near-austin (inbound links and existing rankings live there),
and a card headline that says 14 against a URL that says 8 invites the reader to
wonder which is out of date. "Special Day Rounds Near Austin" is true regardless
of the count, and the post's own h1 carries the 10-and-4 breakdown.

Every edit below is an exact string. Anything that does not match is reported.
"""
import re, os, sys

apply_ = "--apply" in sys.argv

OLD_TITLE = "8 Special Day Rounds Near Austin"
NEW_TITLE = "Special Day Rounds Near Austin"

# (file, old, new, note)
RULES = [
 # ---------- title, everywhere it is used as a label ----------
 ("*", f">{OLD_TITLE}</a>", f">{NEW_TITLE}</a>", "card title link"),
 ("*", f'alt="{OLD_TITLE}"', f'alt="{NEW_TITLE}"', "more-card alt"),
 ("*", f'<div class="more-card-name">{OLD_TITLE}</div>',
       f'<div class="more-card-name">{NEW_TITLE}</div>', "more-card name"),
 ("index.html", f"<!-- FIELD GUIDE — {OLD_TITLE} -->", f"<!-- FIELD GUIDE — {NEW_TITLE} -->",
  "source comment"),
 ("field-guide/index.html", f'<div class="guide-card-title">{OLD_TITLE}</div>',
  f'<div class="guide-card-title">{NEW_TITLE}</div>', "guide-card title"),

 # ---------- homepage slide metas ----------
 ("index.html", "West Austin · Resort guest · ~$275", "West Austin · Resort guest · resort rates",
  "Barton Creek price"),
 ("index.html", "Horseshoe Bay · ~1 hr NW · ~$250", "Horseshoe Bay · ~1 hr 15 NW · resort rates",
  "Ram Rock price + drive time"),
 ("index.html", "Blanco · ~50 min west · $75–110", "Blanco · ~50 min west · $95 Mon–Thu",
  "Vaaler Creek price"),
 ("index.html", "Lakeway · ~25 min west · $52–78", "Lakeway · ~25 min west · dynamic pricing",
  "Falconhead price"),
 ("index.html", "NW Austin · ~25 min north · $75–78", "Cedar Park · ~30 min north · check rates",
  "Avery Ranch price + location"),
 ("index.html", "San Marcos · ~45 min south · $100–130", "San Marcos · ~45 min south · via Troon",
  "Kissing Tree price"),
 ("index.html", "San Antonio · ~1.25 hrs south · $59–79", "San Antonio · ~1 hr 15 south · check rates",
  "Quarry price"),

 # ---------- homepage slide texts + card text ----------
 ("index.html", "Thirty minutes east and a world away from your Tuesday nine at the muni.",
  "Twenty minutes east and a world away from your Tuesday nine at the muni.",
  "Lost Pines drive time (resort says 20)"),
 ("index.html", "Cart included in the green fee, which softens the $95-110 weekend rate.",
  "Cart included in the green fee &mdash; $95 Monday to Thursday, read 17 September 2026.",
  "Vaaler Creek rate"),
 ("index.html", "Fifty minutes from Austin and worth every one of them.",
  "Fifty minutes from Austin, and the drive out through Blanco is half the point.",
  "banned word 'worth'"),
 ("index.html", "Weekday rates under $55 make this the best value splurge in the Austin metro.",
  "Falconhead moved to dynamic pricing in 2026 and says so on its own rates page, so a quiet weekday can cost a fraction of a Saturday morning.",
  "Falconhead now prices dynamically"),
 ("index.html", "Seventy-five dollars for this much terrain is the kind of math that makes you wonder what you have been doing with your weekends.",
  "Check the rate before you go &mdash; it moves with the day &mdash; but this much terrain thirty minutes north is the kind of find that makes you wonder what you have been doing with your weekends.",
  "Avery Ranch fixed price removed"),
 ("index.html", "Weekday rate is fifty-nine dollars, which feels like a clerical error.",
  "Book it on a weekday and the rate tends to feel like a clerical error for what you get.",
  "Quarry fixed price removed"),

 # ---------- field guide teaser chip ----------
 ("field-guide/index.html", "Day Trips · 8 Courses", "Day Trips · 14 Courses", "guide-card chip"),
 ("field-guide/index.html", "Day Trips &middot; 8 Courses", "Day Trips &middot; 14 Courses",
  "guide-card chip (entity form)"),
]

TARGETS = sorted(set([f for f, *_ in RULES if f != "*"] + [
    "index.html", "field-guide/index.html",
    "drops/brand-to-know-sentinel-golf.html",
    "drops/the-hat-edit-austin-summer.html",
    "drops/7-books-to-elevate-your-golf-game.html",
]))

files, orig = {}, {}
for f in TARGETS:
    if os.path.exists(f):
        files[f] = orig[f] = open(f, encoding="utf-8").read()

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
        missed.append(f"{f}: {note}  —  {old[:70]}")

# ------------------------------------------------------------------- guards
problems = []
for p, t in files.items():
    if t == orig[p]:
        continue
    for tag in ("<div", "<section", "<a ", "gear-slide"):
        if t.count(tag) != orig[p].count(tag):
            problems.append(f"{p}: {tag} count changed — an edit ate markup")
    if OLD_TITLE in t:
        problems.append(f"{p}: the old '8 Special Day' title survived somewhere")
    if len(t) < len(orig[p]) * 0.99:
        problems.append(f"{p}: lost more than 1% of its bytes")

# the slideTexts literal is JS, not JSON — validate it with node, never json.loads
if "index.html" in files and files["index.html"] != orig["index.html"]:
    import subprocess, tempfile
    h = files["index.html"]
    # NOT h.find("window._slideTexts") — the first hit is a READ of the map inside
    # the carousel code, not the declaration. Anchor on the assignment, then
    # brace-match to the close; the literal has no reliable "\n};" terminator.
    k = h.find("window._slideTexts = {")
    if k < 0:
        problems.append("index.html: could not find the _slideTexts literal")
    else:
        d, end = 0, None
        for j in range(h.index("{", k), len(h)):
            if h[j] == "{":
                d += 1
            elif h[j] == "}":
                d -= 1
                if d == 0:
                    end = j
                    break
        js = h[k:end + 1].replace("window._slideTexts", "var _st")
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as fh:
            fh.write(js + "\nconsole.log(Object.keys(_st).length);")
            tmp = fh.name
        r = subprocess.run(["node", tmp], capture_output=True, text=True)
        if r.returncode:
            problems.append("index.html: _slideTexts no longer parses as JS — " +
                            r.stderr.strip().splitlines()[-1])
        else:
            log.append(f"{'index.html':44} _slideTexts parses, {r.stdout.strip()} keys")
        os.unlink(tmp)

# banned word, scoped to the copy this script touched
for p, t in files.items():
    if t == orig[p]:
        continue
    for m in re.finditer(r"\bworth\b", t, re.I):
        frag = t[max(0, m.start() - 90):m.start() + 90]
        if "special-day" in frag or "Vaaler" in frag or "Quarry" in frag:
            problems.append(f"{p}: banned word 'worth' left in Special Day copy")

if problems:
    raise SystemExit("REFUSED:\n  " + "\n  ".join(problems))

if apply_:
    for p, t in files.items():
        if t != orig[p]:
            open(p, "w", encoding="utf-8").write(t)

print(("applied" if apply_ else "DRY RUN") + " — Special Day card + sitewide references")
for l in log:
    print("  ·", l)
if missed:
    print("\n  NOT FOUND (check by hand):")
    for m in missed:
        print("    !!", m)
print()
for p, t in files.items():
    if t != orig[p]:
        print(f"  {p:44} {len(t)-len(orig[p]):+5d} bytes")
if not apply_:
    print("\npass --apply to write")
