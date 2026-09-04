#!/usr/bin/env python3
"""
revisit-takomo.py — Brand Revisited pass on the existing Takomo BTK page.

Per [[brand-revisited-playbook]]: upgrade the RANKING URL, never a new page.

Verified against takomogolf.com 2026-09-04 (product pages, not search):
  Skyforger 002 Wedges  $99   in stock
  Ignis D2 Fairway Wood $269  in stock   (new for 2026)
  Stand Bag 02          $279  in stock   (US & EU only)
  Iron 301 MB           $649  LOW STOCK
  Iron 101U Driving Iron $119 in stock
  Ignis D1 Driver       $319  SOLD OUT + noindex,nofollow on its product page
Lenny chose to include the D1 anyway, marked sold out.

Also fixes live price drift: the Skyforger wedge is $99 now, page said $89.
Idempotent via the marker. Dry-run default; --apply writes.
"""
import re, sys, datetime

MARK = "<!--TGI-TAKOMO-REVISIT-V1-->"
P = "drops/brand-to-know-takomo-golf.html"
TODAY = "2026-09-04"

CARDS = [
 ("skyforger-002-wedges", "sf002", "Skyforger 002 Wedges &middot; $99", None,
  "Full-face grooves run heel to toe, so contact out on the toe still comes off the face with spin. Takomo built the SF002 with George and Wesley Bryan, and it sits alongside the original Skyforger rather than replacing it. Eleven loft and grind combinations, right or left hand, Lamkin Crossline grips as standard.",
  "Takomo Skyforger 002 full-face wedge being played from a fairway lie"),
 ("ignis-d2-fairway-wood", "ignis-d2", "Ignis D2 Fairway Wood &middot; $269", None,
  "The second-generation fairway wood, offered in 3, 5 and 7. Adjustable hosel, a matte crown that stays quiet behind the ball, and a neutral flight rather than a draw bias. Wrench and headcover come in the box. Takomo moved into metalwoods in 2025 and the D2 is the follow-up.",
  "Takomo Ignis D2 fairway wood addressing a golf ball on close-mown turf"),
 ("stand-bag-02", "standbag02", "Stand Bag 02 &middot; $279", None,
  "A four-way top with full-length dividers, a quilted front panel and burnt-orange pulls against black or off-white. Built as a walking bag, with the legs set for firm ground rather than a cart strap. Takomo ships it to the US and EU only.",
  "Takomo Stand Bag 02 in off-white laid on fairway grass beside clubs and golf balls"),
 ("iron-301-mb", "iron301mb", "Iron 301 MB &middot; $649", None,
  "A forged muscle back in 4-PW for players who want the feedback a blade gives and nothing softened. Thin topline, minimal offset, KBS Tour shafts across three flexes. It sits at the sharp end of the 301 family, above the cavity-back CB, and stock is running low.",
  "Takomo Iron 301 MB forged muscle back iron against a green background"),
 ("ignis-d1-driver", "ignis-d1", "Ignis D1 Driver &middot; $319 &middot; sold out", "sold out",
  "Takomo&rsquo;s first driver, a 460cc adjustable head with movable weights, a torque wrench and a vegan-leather cover included. Right-handed only, on Fujikura Ventus shafts in Blue and Red. Every loft and shaft combination is sold out at the time of writing.",
  "A golfer walking with the Takomo Ignis D1 driver over one shoulder"),
 ("iron-101u", "iron-101u", "Iron 101U Driving Iron &middot; $119", None,
  "A hollow-body utility iron for the tee shot that has to find short grass. The hollow construction launches it higher than a traditional driving iron, and Takomo sells it as a single club rather than forcing it into a set.",
  "Takomo Iron 101U hollow-body driving iron"),
]

FAQS = [
 ("What is new from Takomo for 2026?",
  "The Ignis D2 fairway wood at $269 in 3, 5 and 7, the Stand Bag 02 at $279, and the Skyforger 002 full-face wedge at $99. The Iron 301 MB completes the 301 family at $649."),
 ("Who is behind Takomo Golf?",
  "Sebastian Haapahovi founded the company in 2021 and it is based in Turku, Finland. YouTuber Grant Horvat has taken an ownership stake in the brand, and George and Wesley Bryan worked with Takomo on the Skyforger wedges."),
 ("Does Takomo make a driver?",
  "Yes. The Ignis D1 is a 460cc adjustable head at $319, right-handed only, and it marked Takomo's first move into metalwoods. It is sold out in every loft and shaft option as of September 2026."),
]

def card(handle, img, name, badge, desc, alt):
    return f'''
    <a href="https://takomogolf.com/products/{handle}" target="_blank" rel="noopener" class="product-card">
      <div class="product-img">
        <img src="/images/takomo-golf/{img}.jpg" alt="{alt}" loading="lazy" />
      </div>
      <div class="product-body">
        <div class="product-brand">Takomo Golf</div>
        <div class="product-name">{name}</div>
        <div class="product-desc">{desc}</div>
        <span class="product-link">Shop &#8599;</span>
      </div>
    </a>'''

SECTION = MARK + '''
<section class="products">
  <h2 class="products-hdr">New from the Collection</h2>
  <div class="products-grid">''' + "".join(card(*c) for c in CARDS) + '''
  </div>
</section>
'''

APPLY = "--apply" in sys.argv
h = open(P, encoding="utf-8").read()
orig = h

if MARK in h:
    print("already applied"); sys.exit(0)

# 1) price drift: the Skyforger wedge is $99 now
n89 = h.count("$89")
for a, b in [
    ("An $89 wedge", "A $99 wedge"),
    ("The Skyforger wedge, at $89,", "The Skyforger wedge, at $99,"),
    ("The range runs $89 to $679.", "The range runs $99 to $679."),
    ("<span>$89 &ndash; $679</span>", "<span>$99 &ndash; $679</span>"),
    ("<span>$89 – $679</span>", "<span>$99 – $679</span>"),
    ("Skyforger Wedge &middot; $89", "Skyforger Wedge &middot; $99"),
    ("Skyforger Wedge · $89", "Skyforger Wedge · $99"),
    ("At $89 a club", "At $99 a club"),
]:
    h = h.replace(a, b)
print(f"price drift: {n89} '$89' mentions -> {h.count('$89')} remaining")

# 2) new section, inserted after the existing lineup section
m = list(re.finditer(r'</section>', h))
anchor = h.find('The Lineup')
end = h.find('</section>', anchor)
h = h[:end+10] + "\n" + SECTION + h[end+10:]

# 3) FAQ items into the visible list + the FAQPage schema
last = h.rfind('</details>')
add = "".join(f'\n  <details class="faq-item"><summary>{q}</summary><p>{a}</p></details>' for q,a in FAQS)
h = h[:last+10] + add + h[last+10:]

sm = re.search(r'("@type": "FAQPage",\s*"mainEntity": \[)', h)
entries = "".join(
  '\n  {\n   "@type": "Question",\n   "name": %s,\n   "acceptedAnswer": { "@type": "Answer", "text": %s }\n  },'
  % (__import__('json').dumps(q), __import__('json').dumps(a)) for q,a in FAQS)
h = h[:sm.end()] + entries + h[sm.end():]

# 4) freshness signals
h = h.replace('"dateModified": "2026-08-13"', f'"dateModified": "{TODAY}"')

if APPLY and h != orig:
    open(P, "w", encoding="utf-8").write(h)
print(f"cards added: {len(CARDS)} | FAQs added: {len(FAQS)} | dateModified -> {TODAY}")
print("applied" if APPLY else "DRY RUN — pass --apply")
