#!/usr/bin/env python3
"""
takomo-fitting.py — add the "Which Iron Is Yours" fitting section.

Every handicap range and every "for who" line here is VERBATIM from Takomo's own
product pages (read from the live rendered pages 2026-09-04), not inferred from
the club category. Takomo publishes an explicit target HCP range on each iron,
which is what makes the section possible.

The one editorial line per club is TGI's read, kept clearly separate from the
brand's own words.

Idempotent. Dry-run default; --apply writes.
"""
import re, sys

P = "drops/brand-to-know-takomo-golf.html"
MARK = "<!--TGI-TAKOMO-FITTING-V1-->"

CSS = """/*TGI-FIT-CSS-V1*/
.fit-tbl{max-width:820px;margin:22px 0 0}
.fit-row{display:grid;grid-template-columns:170px max-content 1fr;gap:18px;padding:18px 0;border-top:.5px solid rgba(20,20,20,.14);align-items:start}
.fit-row:last-child{border-bottom:.5px solid rgba(20,20,20,.14)}
.fit-club{font-family:var(--serif);font-style:italic;font-size:18px;line-height:1.25}
.fit-price{font-family:var(--mono);font-size:10px;letter-spacing:.1em;opacity:.55;display:block;margin-top:4px;font-style:normal}
.fit-hcp{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;background:var(--rough);color:var(--ink);padding:4px 8px;display:inline-block;white-space:nowrap}
.fit-body{font-size:14px;line-height:1.6}
.fit-body .fit-quote{opacity:.75;display:block;margin-bottom:5px}
@media(max-width:700px){.fit-row{grid-template-columns:1fr;gap:7px}}
"""

# (club, price, set, HCP verbatim, Takomo's "for who" verbatim, TGI read)
ROWS = [
 ("Iron 101 MKII", "$579 &middot; 5-GW", "HCP 15&ndash;40+",
  "For beginners, higher-handicap players and golfers seeking extra carry and forgiveness without working too hard.",
  "The widest net Takomo casts. A 431 cast hollow body, and the only set that ships with a gap wedge instead of a 4-iron."),
 ("Iron 201 MKII", "$649 &middot; 4-PW", "HCP 5&ndash;25",
  "Improving golfers who have outgrown game-improvement irons. Solid ballstrikers who desire distance and forgiveness over everything else.",
  "The step up from the 101, in a shorter blade with a thinner topline. Still hollow, still forgiving."),
 ("Iron 201T MKII", "$679 &middot; 4-PW", "HCP 0&ndash;15",
  "Consistent ballstrikers who want to shotshape but need a bit of forgiveness built into a compact, precise package.",
  "Tungsten in the 4 through 7 irons keeps the long end playable. The widest handicap overlap in the range."),
 ("Iron 301 CB", "$649 &middot; 4-PW", "HCP 0&ndash;5",
  "Advanced golfers who value control and added forgiveness.",
  "One-piece forged S20C, and the point where the range stops helping and starts responding."),
 ("Iron 301 MB", "$649 &middot; 4-PW", "HCP 0&ndash;2 or better",
  "Superior golfers that need workability over everything and value a soft feel.",
  "Takomo puts a warning on its own product page: &ldquo;if used by higher handicappers, you&rsquo;re going to have a bad time.&rdquo;"),
 ("Iron 101U", "$119 &middot; single club", "HCP 0&ndash;15",
  "Players looking for an explosive, forgiving alternative off the tee or in the fairway.",
  "A hollow-body utility rather than a driving iron proper, in three lofts, right-handed only."),
]

def row(club, price, hcp, quote, read):
    return f'''    <div class="fit-row">
      <div class="fit-club">{club}<span class="fit-price">{price}</span></div>
      <div><span class="fit-hcp">{hcp}</span></div>
      <div class="fit-body"><span class="fit-quote">&ldquo;{quote}&rdquo;</span>{read}</div>
    </div>'''

SECTION = MARK + f'''
<section class="products">
  <h2 class="products-hdr">Which Iron Is Yours</h2>
  <div class="writeup" style="grid-template-columns:1fr;padding-top:0">
    <div class="writeup-body" style="max-width:760px">
      <p>Takomo prints a target handicap range on every iron page, which makes the range unusually easy to read from the outside. The quoted lines below are the brand&rsquo;s own; the note under each is ours.</p>
    </div>
  </div>
  <div class="fit-tbl">
{chr(10).join(row(*r) for r in ROWS)}
  </div>
</section>
'''

APPLY = "--apply" in sys.argv
h = open(P, encoding="utf-8").read()
if MARK in h:
    print("already applied"); sys.exit(0)

k = h.rfind("</style>"); h = h[:k] + CSS + h[k:]
anchor = h.find('<section class="products" style="border-top:none">')   # the pull-quote block
if anchor < 0:
    anchor = h.find('<section class="products" style="border-top:none;padding-top:48px">')  # the FAQ
h = h[:anchor] + SECTION + "\n" + h[anchor:]

if APPLY:
    open(P, "w", encoding="utf-8").write(h)
print(f"fitting section added: {len(ROWS)} clubs, all HCP ranges verbatim from takomogolf.com")
print("applied" if APPLY else "DRY RUN — pass --apply")
