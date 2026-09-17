#!/usr/bin/env python3
"""Flesh out /drops/the-water-bottle-edit — 17 September 2026.

WHAT WAS WRONG BEYOND THE LINKS. After this morning's link audit removed two
dead products, the page ran 846 words with 14 cards, no explainer, no FAQ
schema, and three separate count claims that disagreed with each other and with
reality: the H2 said "16 Pieces", the meta description opened "14 bottles from
sixteen brands", and the intro repeated it. The intro also named the Quiet Golf
x SSC MiiR — the product that no longer exists — and described sweeping "all
seventy-plus" brands in the Index, which stood at 131 when this ran.

WHAT THIS ADDS
  · Mogshade Ocean Bottle x Mogshade, $59 — new brand to the post
  · Huega House Squeeze Water Bottle, $15 — new brand to the post
  · Sugarloaf Hidden Gem Scoutfitters 32oz Nalgene, $32 — REPLACES the existing
    SSC card, which pointed at /sugarloaf-swag, a collection page, for a product
    whose continued existence could not be confirmed. Same brand, real product,
    verified price.
  · A materials explainer, which is the thing a reader actually wants and the
    page had none of: what a vacuum does, why 32oz is the walking number, what
    dishwasher-safe rules out.
  · Six Q&As with FAQPage schema. The page already carried .faq-q markup but its
    JSON-LD was Article/WebPage only, so none of it was eligible for rich
    results.

All three additions were read off the brand's own store on 17 September 2026 and
were in stock at the time of reading. Lenny approved all three.

HOUSE FAQ MARKUP IS <details class="faq-q"><summary>. See build-divot-tools.py:
div.faq-q + div.faq-a fails twice over — verify-post.py flags faq-a as a class
with no CSS rule, and apply-faq-style.py cannot see div markup so it appends a
SECOND FAQ rendered from the schema.

SCHEMA NOTE: the page's existing JSON-LD is an Article block. The FAQPage is
merged into an @graph alongside it rather than replacing it, so the Article
markup survives.
"""
import re, os, sys, json, html as H

apply_ = "--apply" in sys.argv
P = "drops/the-water-bottle-edit.html"
IMG = "/images/water-bottles/"

# (slug, brand, name, price, url, copy)
NEW = [
 ("mogshade-ocean", "Mogshade", "Ocean Bottle &times; Mogshade", "59",
  "https://mogshadegolf.com/products/ocean-bottle-x-mogshade",
  "Ninety per cent recycled stainless, double-walled with a vacuum between the layers, and rated by "
  "Mogshade for six hours hot and eighteen cold. It is dishwasher safe, which is rarer in this category "
  "than it should be &mdash; most vacuum bottles are hand-wash because the heat can stress the seal on the "
  "outer wall. The engraving is by the artist Fiumani, from Mogshade&rsquo;s Course Flip collection."),
 ("huega-squeeze", "Huega House", "Squeeze Water Bottle &mdash; Black", "15",
  "https://huegahouse.com/products/huega-squeeze-water-bottle-black",
  "The cheapest thing on this page and the only one built to be squeezed. Five hundred and fifty "
  "millilitres of flexible food-grade plastic with an easy-flow spout, BPA free, designed for drinking "
  "one-handed while you keep walking. There is no insulation and no pretence of any &mdash; your water "
  "will be the temperature of the air within the hour, and at fifteen dollars that is the deal."),
 ("ssc-nalgene", "Sugarloaf Social Club", "Hidden Gem Scoutfitters 32oz Nalgene", "32",
  "https://sugarloafsocialclub.com/products/hidden-gem-scoutfitters-32-oz-nalgene",
  "A 32oz wide-mouth Nalgene in Sugarloaf&rsquo;s Hidden Gem colourway, made in the USA. Nalgene is the "
  "copolyester bottle that came out of a lab-supply company and ended up strapped to every backpack in "
  "North America; the wide mouth is the whole reason, because it takes ice cubes and a bottle brush. "
  "Sugarloaf&rsquo;s own line for it is to fill it at the turn."),
]

t = open(P, encoding="utf-8").read()
log = []

def gal(slug, alt):
    n = 1
    while os.path.exists(f"images/water-bottles/{slug}-a{n+1}.jpg"):
        n += 1
    pl = re.sub(r"\s+", " ", re.sub(r"<[^>]+>|&[a-z]+;|&#\d+;", "", alt)).strip()
    if n == 1:
        return ('<div class="product-gallery"><div class="pg-track"><div class="pg-frame">'
                f'<img src="{IMG}{slug}.jpg" alt="{pl}" loading="lazy" /></div></div></div>'), n
    fr = "".join(f'<div class="pg-frame"><img src="{IMG}{slug}{"" if i==0 else f"-a{i+1}"}.jpg" '
                 f'alt="{pl} &middot; view {i+1} of {n}" loading="lazy" /></div>' for i in range(n))
    dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" '
                   f'aria-label="View image {i+1}"></button>' for i in range(n))
    return ('<div class="product-gallery"><div class="pg-track">' + fr +
            '</div><button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            '<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>'), n

def card(slug, brand, name, price, url, copy):
    g, n = gal(slug, f"{brand} {name}")
    return f"""<div class="product-card" data-frames="{n}">
      {g}
      <div class="product-body">
        <div class="product-brand">{brand}</div>
        <div class="product-name">{name} &middot; ${price}</div>
        <div class="product-desc">{copy}</div>
        <a href="{url}" target="_blank" rel="noopener" class="product-link">Shop ↗</a>
      </div>
    </div>"""

# ---------------------------------------- 1. swap the collection-level SSC card
k = t.find("sugarloaf-swag")
if k == -1:
    log.append("  !! the old Sugarloaf card is already gone — skipping the swap")
else:
    s = t.rfind('<div class="product-card"', 0, k)
    depth, j, end = 0, s, None
    while j < len(t):
        m = re.compile(r"<div\b|</div>").search(t, j)
        if not m:
            break
        if m.group(0).startswith("<div"):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                end = m.end(); break
        j = m.end()
    if end is None:
        raise SystemExit("unbalanced Sugarloaf card — aborting")
    block = t[s:end]
    if "sugarloaf-swag" not in block or block.count("product-card") != 1:
        raise SystemExit("refusing to replace a block I have not positively identified")
    t = t[:s] + card(*NEW[2]) + t[end:]
    log.append("swapped the collection-level Sugarloaf card for the Hidden Gem Nalgene ($32)")

# --------------------------------------------- 2. append the two new brands
# IDEMPOTENCY: this step has no natural marker, so check for the lead image
# before appending. Without it a second run duplicates both cards.
if f"{IMG}{NEW[0][0]}.jpg" in t and f"{IMG}{NEW[1][0]}.jpg" in t:
    log.append("  · Mogshade and Huega cards already present — not re-adding")
else:
    ins = t.find("</section>", t.find('<div class="products-grid">'))
    grid_end = t.rfind("</div>", 0, ins)
    add = "\n\n    " + card(*NEW[0]) + "\n\n    " + card(*NEW[1]) + "\n  "
    t = t[:grid_end] + add + t[grid_end:]
    log.append("added Mogshade Ocean Bottle ($59) and Huega House Squeeze ($15)")

N = t.count('class="product-card"')

# ------------------------------------------------- 3. counts, intro, headings
t = re.sub(r'(<h2 class="products-hdr">)The Collection[^<]*(</h2>)',
           lambda m: m.group(1) + f"The Collection &mdash; {N} Bottles" + m.group(2), t)
log.append(f"H2 now reads 'The Collection — {N} Bottles'")

INTRO = (
 "<p>This edit runs to sixteen bottles from sixteen brands, and there is not a YETI or a Stanley among "
 "them. It is what the independent side of golf makes when it makes something to drink out of &mdash; MiiR and Ocean Bottle "
 "collaborations, a Nalgene in a colourway, a hip flask in tartan, a bike bottle borrowed wholesale from "
 "cycling, and one squeeze bottle that costs fifteen dollars and makes no apology for it.</p>"
 "<p>The spread runs $14 to $59. That is a four-fold gap for objects that all do the same job, which is "
 "why the section below the grid exists: the money in a water bottle goes almost entirely into things you "
 "cannot see from the product photograph.</p>"
 "<p>Every price here was read off the seller&rsquo;s own page on 17 September 2026, and anything not "
 "buyable that day says so on its card. Small brands run small batches and bottles are a category where "
 "collaborations sell out and do not come back, so treat a sold-out tag as information rather than a "
 "disappointment.</p>")
m = re.search(r'(<div class="writeup-body">)(.*?)(</div>)', t, re.S)
if m and "sixteen bottles from sixteen brands" not in m.group(2).lower():
    t = t[:m.start(2)] + INTRO + t[m.end(2):]
    log.append("intro rewritten (dropped the removed Quiet Golf x SSC reference and the stale brand count)")

DESC = ("Sixteen water bottles from sixteen independent golf brands, $14 to $59 — MiiR and Ocean Bottle "
        "collabs, a Nalgene, a tartan flask. Prices read live, 17 September 2026.")
for k_, attr in [("description", "name"), ("og:description", "property"), ("twitter:description", "name")]:
    t = re.sub(rf'(<meta {attr}="{re.escape(k_)}" content=")[^"]*(")',
               lambda mm: mm.group(1) + DESC + mm.group(2), t)
log.append("meta description rewritten (it said '14 bottles from sixteen brands')")

# ------------------------------------------------------------ 4. explainer
EXPLAIN = """<section class="products">
  <h2 class="products-hdr">What You Are Actually Paying For</h2>
  <p class="cat-kicker">A bottle is a simple object with four expensive decisions inside it.</p>
  <div class="writeup-body">
    <p><strong>The vacuum.</strong> This is the whole ballgame and it is the reason a $15 bottle and a $59 bottle are different products rather than the same product at two prices. A vacuum-insulated bottle is two stainless vessels with the air drawn out of the gap between them; with no air there is almost nothing to carry heat across, so the contents hold temperature for hours instead of minutes. It is expensive because it is two bottles welded into one, and it is why the Ocean Bottle collaboration holds ice for eighteen hours while the Huega squeeze holds it for about as long as your walk to the first tee.</p>
    <p><strong>Capacity, and why 32oz keeps turning up.</strong> A 20oz bottle is a cart bottle. If you are walking eighteen in Texas heat you will drink two or three of them, which means either a refill stop or a bigger vessel &mdash; and that is the argument for a 32oz Nalgene, which holds most of a round in one fill and takes ice cubes through the wide mouth. The trade-off is weight: water is roughly a kilogram a litre, so a full 32oz adds around two pounds to a carry bag you already chose for being light.</p>
    <p><strong>Wide mouth or narrow.</strong> A wide mouth takes ice, takes a bottle brush, and dries properly. A narrow mouth or a straw lid is easier to drink from while moving and much harder to clean, which is how bottles develop a smell. If a bottle cannot fit a brush, assume you will be replacing it rather than reviving it.</p>
    <p><strong>Dishwasher safe, and what it tells you.</strong> Most vacuum bottles are hand-wash only, because dishwasher heat can stress the seal on the outer wall and a bottle that loses its vacuum is just a heavy cup. When a brand does say dishwasher safe &mdash; Mogshade does &mdash; it is a claim about the weld, not about the finish, and it tells you more than any colourway does.</p>
  </div>
</section>
"""

FAQ_ITEMS = [
 ("What size water bottle is best for walking 18 holes?",
  "A 32oz wide-mouth bottle holds most of a round in one fill, which is why Nalgene-style bottles are the walking standard. A 20oz bottle is a cart bottle — you will drink two or three walking in heat. The cost of the bigger bottle is weight: water runs about a kilogram per litre, so a full 32oz adds roughly two pounds to the bag."),
 ("Do I really need a vacuum-insulated golf bottle?",
  "It depends entirely on whether you want cold water at the 14th. A vacuum bottle is two stainless vessels with the air pulled out of the gap between them, so there is almost nothing to carry heat across — the Ocean Bottle collaboration here is rated for eighteen hours cold. A single-wall or plastic bottle reaches air temperature within the hour. If you play early and finish before it warms up, the cheaper bottle is the honest answer."),
 ("Why are some bottles dishwasher safe and most are not?",
  "Dishwasher heat can stress the seal on the outer wall of a vacuum bottle, and a bottle that loses its vacuum is just a heavy cup. That is why most insulated bottles are hand-wash only. When a brand states dishwasher safe, it is making a claim about the quality of the weld rather than about the paint."),
 ("Wide mouth or narrow mouth for a golf bottle?",
  "Wide mouth takes ice cubes, takes a bottle brush and dries properly between rounds. Narrow mouths and straw lids are easier to drink from while you are moving and considerably harder to clean, which is how a bottle starts to smell. If a brush will not fit, plan on replacing it rather than rescuing it."),
 ("What is a Nalgene and why do golf brands keep making them?",
  "Nalgene is a copolyester bottle that started life as laboratory glassware in the 1940s and became the default outdoor water bottle in North America. Golf brands put colourways on it for the same reason they put them on Crazy Creek chairs and MiiR tumblers — the object is already good, already recognisable, and already made in the USA, so the brand is adding a graphic rather than solving a fluid-dynamics problem."),
 ("Were all of these in stock when this was written?",
  "Every link and every price on this page was checked on 17 September 2026. Anything not buyable that day is tagged sold out on its card rather than quietly left as if it were available. Collaboration bottles in particular tend to be single runs that do not return."),
]

def st(s):
    return (re.sub(r"<[^>]+>", "", s).replace("&ldquo;", '"').replace("&rdquo;", '"')
            .replace("&rsquo;", "'").replace("&amp;", "&").replace("&mdash;", "—")
            .replace("&middot;", "·").replace("&times;", "×"))

FAQ = """<section class="products">
  <h2 class="products-hdr" id="faq">The Questions</h2>
  <div class="faq">
""" + "\n".join(f'    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>'
                for q, a in FAQ_ITEMS) + """
  </div>
</section>
"""

if 'id="faq"' in t:
    log.append("  !! a FAQ section already exists — not adding a second")
else:
    tail_at = t.find('<section class="more"')
    if tail_at == -1:
        raise SystemExit("could not find the More-from-the-Feed block to insert before")
    t = t[:tail_at] + EXPLAIN + "\n" + FAQ + "\n" + t[tail_at:]
    log.append(f"added the materials explainer + {len(FAQ_ITEMS)} Q&As")

# ------------------------------------------------------------- 5. FAQ schema
FAQ_SCHEMA = {"@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": st(q),
     "acceptedAnswer": {"@type": "Answer", "text": st(a)}} for q, a in FAQ_ITEMS]}
blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)
if not blocks:
    raise SystemExit("no JSON-LD on the page at all — unexpected")
first = json.loads(blocks[0])
cp = dict(first); cp.pop("@context", None)
merged = {"@context": "https://schema.org", "@graph": [cp, FAQ_SCHEMA]}
_lit = '<script type="application/ld+json">' + json.dumps(merged) + "</script>"
t = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda _m: _lit, t, count=1, flags=re.S)
log.append("FAQPage schema merged into the existing Article block via @graph")

# ------------------------------------------- 6. the .cat-kicker CSS rule
# The class is new to THIS page. verify-post.py fails a page that uses a class
# with no CSS rule behind it — without this the kicker renders full-width.
KICK = (".cat-kicker{font-family:var(--sans);font-size:15px;line-height:1.75;color:#3f443e;"
        "margin:0 0 36px;max-width:70ch;border-left:3px solid var(--rough);padding:4px 0 4px 18px}")
if ".cat-kicker{" not in t:
    _s = t.rfind("</style>")
    if _s == -1:
        raise SystemExit("no <style> block to install the kicker rule into")
    t = t[:_s] + KICK + t[_s:]
    log.append("installed the house .cat-kicker CSS rule (new class on this page)")

# ------------------------------------------------------------------ guards
plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", H.unescape(
    re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", t, flags=re.S))))
words = len(re.findall(r"[A-Za-z0-9']+", plain))
problems = []
if words < 1200:
    problems.append(f"only {words} words")
if t.count("<div") != t.count("</div>"):
    problems.append("unbalanced divs")
if t.count("<a ") != t.count("</a>"):
    problems.append("unbalanced anchors")
if t.count("<h1") != 1:
    problems.append(f"{t.count('<h1')} h1 tags")
if "sugarloaf-swag" in t:
    problems.append("the collection-level Sugarloaf link survived")
for slug, *_ in NEW:
    if f"{IMG}{slug}.jpg" not in t:
        problems.append(f"{slug}: card did not land")
    if not os.path.exists(f"images/water-bottles/{slug}.jpg"):
        problems.append(f"{slug}: lead image missing on disk")
if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", INTRO + EXPLAIN + FAQ), re.I):
    problems.append("banned word 'worth' in new copy")
for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
    json.loads(b)
if problems:
    raise SystemExit("REFUSED:\n  " + "\n  ".join(problems))

if apply_:
    open(P, "w", encoding="utf-8").write(t)

print(("applied" if apply_ else "DRY RUN") + f" — {os.path.basename(P)}")
for l in log:
    print("  ·", l)
print(f"  {N} bottles | {words} words | {t.count('product-gallery')} galleries")
if not apply_:
    print("\npass --apply to write")
