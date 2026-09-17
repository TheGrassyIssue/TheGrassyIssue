#!/usr/bin/env python3
"""Put the Social Club into the homepage feed — 17 September 2026.

WHY A SINGLE-IMAGE CARD, NOT A CAROUSEL. Most feed cards run a .gear-carousel
because they have four or five products to show. This has one poster and one
destination. The house already has the pattern for that — the Field Notes card
uses .card-media with a single child and no carousel — so this follows it rather
than faking a carousel with one slide, which would render arrows that do nothing.

CARD TYPE "field". The feed types are drop / drops / field / guide / news /
quote. This is neither a product roundup nor an outside news item; it is TGI's
own thing happening in Austin, which is what [Field Notes] covers. Using "news"
would put a [News] chip on our own event and imply somebody else reported it.

NOTE: The Long Walk has never had a homepage card — it lives on /events only.
This card does not change that, and the two do not compete in the feed.

IDEMPOTENT: marker-fenced (TGI-SC-HOME) and replaced rather than appended, so a
re-run after any feed reshuffle is safe.
"""
import re, os, sys

apply_ = "--apply" in sys.argv
URL = "/events/social-club"
POSTER = "/images/social-club-poster.jpg"
S, E = "<!--TGI-SC-HOME-->", "<!--/TGI-SC-HOME-->"

TITLE = "The Grassy Issue Social Club"
TEXT = ("Small groups playing good courses in and around Austin. Eight to twelve players an outing, "
        "two or three tee times, walkers and riders both. No dues, no membership, no obligation to make "
        "any given one &mdash; you pay your own green fee and show up. Close in that means the munis; "
        "further out it means the ninety minutes of Hill Country most people never get around to. "
        "The list is open.")

CARD = f'''{S}
      <div class="card" data-type="field">
    <div class="card-media" style="position:relative;">
      <span class="card-tag flag">[Field Notes]</span>
      <a href="{URL}">
        <img src="{POSTER}" alt="The Grassy Issue Social Club poster — a green over a wide Hill Country horizon" loading="lazy" style="width:100%;display:block;" />
      </a>
    </div>
    <div class="card-body">
      <div class="card-title"><a href="{URL}" style="color:inherit;text-decoration:none;border-bottom:none;">{TITLE}</a></div>
      <div class="card-text">{TEXT}</div>
      <a href="{URL}" class="card-link">Join the list &#8599;</a>
    </div>
  </div>
{E}
'''

notes = []
h = open("index.html", encoding="utf-8").read()
before = len(h)

# ------------------------------------------------------------- idempotency
h = re.sub(re.escape(S) + r".*?" + re.escape(E) + r"\n?", "", h, flags=re.S)

m = re.search(r'\n\s*<div class="card" data-type="', h)
if not m:
    raise SystemExit("could not locate the feed card list")
h = h[:m.start()] + "\n" + CARD + h[m.start():]
notes.append("card inserted at the top of the feed")

# ----------------------------------------------------------------- guards
problems = []
if h.count(S) != 1 or h.count(E) != 1:
    problems.append("markers doubled — not idempotent")
if h.count(URL) != 3:
    problems.append(f"{h.count(URL)} links to the page — expected 3 (image, title, CTA)")
if h.count("<div") != h.count("</div>"):
    problems.append("unbalanced divs")
if h.count("<a ") != h.count("</a>"):
    problems.append("unbalanced anchors")
if not os.path.exists(POSTER.lstrip("/")):
    problems.append("poster missing on disk")
if not os.path.exists("events/social-club.html"):
    problems.append("the page does not exist yet")
if "gear-carousel" in CARD:
    problems.append("single-image card should not carry carousel markup")
if re.search(r"\bworth\b", re.sub(r"&[a-z]+;", " ", TITLE + " " + TEXT), re.I):
    problems.append("banned word 'worth' in the card copy")
# the _slideTexts map is for carousels only — this card must not appear in it
if re.search(r'"social-?club"\s*:', h):
    problems.append("a _slideTexts entry exists for a card with no carousel")
if problems:
    raise SystemExit("REFUSED:\n  " + "\n  ".join(problems))

if apply_:
    open("index.html", "w", encoding="utf-8").write(h)

print(("wired" if apply_ else "DRY RUN") + f" {URL} into the homepage feed  (+{len(h)-before:,} bytes)")
for n in notes:
    print("  ·", n)
print(f"  type: field  ·  [Field Notes] chip  ·  single image, no carousel")
if not apply_:
    print("\npass --apply to write")
