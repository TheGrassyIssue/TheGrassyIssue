#!/usr/bin/env python3
# Brand Revisited — upgrades /drops/brand-to-know-jones-sports-co.html IN PLACE.
import re, json, os, html as H

S = os.path.dirname(os.path.abspath(__file__))
BASE = open(os.path.join(S, "drops/the-custom-wedge-report.html"), encoding="utf-8").read()
PLAN = json.load(open("/tmp/jn/plan.json"))
DL   = json.load(open("/tmp/jn/dl.json"))

SLUG  = "brand-to-know-jones-sports-co"
TITLE = "Brand Revisited &mdash; Jones Sports Co, and the Taxi Driver Who Started It"
TITLE_PLAIN = "Brand Revisited — Jones Sports Co, and the Taxi Driver Who Started It"
DESC = ("Jones Sports Co has made single-strap carry bags in Portland since 1971, when a 40-year-old taxi driver "
        "sewed the first one in his basement. Sold in 1990, nearly lost, bought back in 2011 for the name alone. "
        "Thirty-two bags and pieces from the current line, with prices.")

SECTION_COPY = {
 "original": ("The 1971 Bag, Still Made",
   "The Original is the shape everything else came from &mdash; 2.9 lbs, three-way divider, unstructured spine. "
   "Jones do not claim to have invented the single-strap carry bag anywhere on their own site; they claim to have "
   "been making them since 1971, which is a narrower and more defensible thing to say. Prices here run from $125 to "
   "$215 depending on which material line the colourway sits in."),
 "stand": ("Where the Patent Lives",
   "Jones describe their stand system as &ldquo;patented&rdquo; and say it &ldquo;remains the gold standard.&rdquo; "
   "All four stand bags are built in what they call F-35 recycled ripstop and rated water resistant. The spread runs "
   "from the 4-lb Short Course, built for ten clubs, up to the Utility X with its insulated cooler pocket."),
 "players": ("Structured Spine, and the One You Ride With",
   "The Players Series is the Original with a structured spine and a two-way divider instead of three. The Olive and "
   "Sonoma colourways use a recycled ripstop Jones says is woven from 100&percnt; PET single-use bottles. The Rider "
   "is the only cart bag they make and the most expensive thing in the range."),
 "collabs": ("Shoes, Slides and a Japanese Fiftieth",
   "Jones collaborate more than most brands their size. The PAYNTR shoe landed in May 2026 and is the first time "
   "Jones has put its name on footwear. The BEAMS capsule marks the Japanese retailer&rsquo;s fiftieth and is built "
   "in a bronze canvas made for it."),
 "campus": ("Eighteen Officially Licensed Schools",
   "Jones calls this &ldquo;Officially Licensed,&rdquo; which is rarer than it sounds at this scale &mdash; eighteen "
   "schools from Arizona to Wake Forest. The licence carries a markup: a Trouper is "
   "$315 in the standard line and $385 in school colours, and a Rider goes $520 to $555. Know that before you shop."),
 "rest": ("Headcovers, Packs and a 1951 Outerwear Label",
   "The Circa &rsquo;71 headcovers are named for the founding year. Forrester&rsquo;s is not a collaboration despite "
   "looking like one &mdash; it is a heritage outerwear label Jones owns and revived, and their own copy dates it to "
   "1951."),
}

COPY = {
"original-jones-bag-evergreen":
 "The Heritage version in what Jones calls deluxe vegan leather. The most expensive Original at $215.",
"original-jones-bag-espresso":
 "Painted Hills, which Jones say is inspired by the landscape of Eastern Oregon. Industrial canvas.",
"original-jones-bag-burnt-clay":
 "The cheapest way into an Original at $125, and the same bag underneath.",
"original-jones-bag-navy-red-white":
 "Water-resistant nylon in the core colourway. This is the one that looks like the old photographs.",
"original-jones-bag-moss":
 "The third Painted Hills colour. Canvas, so it will mark and soften.",
"utility-x-pageant-blue":
 "The flagship. 5.1 lbs, four-way divider, and an insulated cooler pocket built into the bag.",
"utility-x-graystone":
 "Graystone is a 300d recycled ripstop with a wax-effect coating. Jones say it develops &ldquo;a character that is earned, not manufactured.&rdquo;",
"trouper-evergreen-kodiak":
 "The Heritage Trouper in vegan leather, five-way divider, $375.",
"trouper-olive-gray":
 "The standard Trouper at $315, which is the same bag in ripstop rather than vegan leather.",
"rover-stand-bag-high-desert":
 "Jones bill the Rover as their lightest stand bag &mdash; 4.2 lbs, three-way divider.",
"rover-stand-bag-graystone":
 "The Rover in the wax-effect Graystone fabric, which is the best-looking thing they make.",
"short-course-bag-navy":
 "Built for ten clubs and an afternoon, with a cooler pocket. Four pounds.",
"jr-trouper-dark-green":
 "A real Trouper scaled for ages eight to twelve, four-way divider. Not a toy.",
"players-series-ecru":
 "Structured spine, two-way divider. The Heritage Ecru is the $225 end of the Players Series.",
"players-series-deep-green-kodiak":
 "The same bag at $195. Kodiak is the vegan leather trim Jones use across the Heritage line.",
"rider-bag-sienna":
 "The only cart bag Jones make, and the most expensive item in the range at $520.",
"rider-bag-navy-red-white":
 "The Rider in the house colourway.",
"jones-sports-co-rs-by-payntr-golf-white-field":
 "Announced May 2026 and the first Jones shoe. Matt Lemman&rsquo;s line on it: a shoe that &ldquo;looks and feels like Jones, but performs at the highest level the game demands.&rdquo;",
"jones-sports-co-rs-by-payntr-golf-gray-olive":
 "The second colourway. PAYNTR do the sole, Jones do the rest.",
"beams-passenger-tote-bronze":
 "Part of a five-piece capsule for the Japanese retailer&rsquo;s fiftieth, in a bronze canvas made for it.",
"beams-dopp-kit-bronze":
 "Same capsule, same fabric, $45.",
"clockwork-hoodie-steel-blue":
 "With Standard Issue. The only apparel collaboration currently live.",
"jones-x-lusso-cloud-scenario-slide-rocket-swir":
 "Co-designed with Lusso Cloud, who make the slide. A recovery shoe with a Jones sensibility.",
"jones-x-lusso-cloud-scenario-slide-rocket-swi":
 "Co-designed with Lusso Cloud, who make the slide. A recovery shoe with a Jones sensibility.",
"jones-x-lusso-cloud-scenario-slide-rocket-sw":
 "Co-designed with Lusso Cloud, who make the slide. A recovery shoe with a Jones sensibility.",
"michigan-st-rover-stand-dark-green":
 "The Rover in Michigan State colours. $365 against $295 for the same bag in the standard line.",
"georgia-original-jones-stripeshow-white":
 "The Stripeshow Original in Georgia colours, in what Jones call leather-look vinyl.",
"missouri-trouper-onyx-kodiak":
 "The most expensive Campus bag at $410 &mdash; Heritage trim plus the licence.",
"circa-71-headcover-w-sock-black":
 "Named for the founding year, with a sock. The only headcovers Jones make.",
"circa-71-headcover-orange":
 "The sockless version at $55.",
"a2-backpack-graystone":
 "The A2 in the wax-effect Graystone, which Jones list as F-35 recycled ripstop with a soft-hand PU face.",
"out-of-office-backpack-wheat-black":
 "The cheapest pack they sell at $65, and the least golf-looking thing in the range.",
"range-hoodie-pageant-blue":
 "Forrester&rsquo;s, the outerwear label Jones own and revived. Their own copy: &ldquo;The original golf outerwear since 1951.&rdquo;",
"arizona-rangefinder-pouch-alpine":
 "Jones make forty-odd rangefinder pouches. This is the Heritage-trimmed one in Arizona colours.",
}

FAQ = [
 ("Who founded Jones Sports Co?",
  "George Jones, in Portland, Oregon, in 1971. Jones&rsquo; own history page describes him as a 40-year-old taxi "
  "driver who began sewing bags in his basement and selling them out of the trunk of his cab. Their line on it: "
  "&ldquo;Who could have known? George Jones, that&rsquo;s who.&rdquo;"),
 ("Did Jones invent the single-strap golf bag?",
  "Jones does not make that claim. Their own site says only that the company has crafted single-strap carry bags "
  "since 1971, and that its stand system is patented and &ldquo;remains the gold standard.&rdquo; Chris Carnahan, "
  "one of the current owners, told Golf Digest in 2017 that George Jones was &ldquo;the innovator behind the stand "
  "and the straps that are now ubiquitous in golf&rdquo; &mdash; that is his characterisation, not a documented "
  "first."),
 ("What happened to Jones between 1971 and now?",
  "George Jones sold the company in 1990. Sports Illustrated reported in 2020 that the new owners changed what made "
  "the bags distinctive in order to compete with larger manufacturers, the strategy failed, and the company "
  "declined. The Lemman family and Chris Carnahan acquired it in 2011. Matt Lemman&rsquo;s description of what they "
  "bought: &ldquo;Just the name, that was all.&rdquo;"),
 ("How did they rebuild the bag with no patterns left?",
  "By finding old ones. Carnahan told Golf Digest there was no inventory and no production facilities, but "
  "&ldquo;being in Portland, a lot of our family and friends had the old bags, so we were able to gather them and "
  "rebuild the Jones bag to the exact specifications but using modern materials.&rdquo;"),
 ("What are Jones bags actually made of?",
  "Not waxed canvas, despite the look. The stand bags use what Jones call F-35 recycled ripstop, rated water "
  "resistant. The Graystone line is a 300d recycled ripstop with a wax-effect top coating. Heritage colourways use "
  "vegan leather, the Stripeshow and Bomber use leather-look vinyl, and some Players Series colours use a ripstop "
  "Jones says is woven from 100&percnt; PET single-use bottles. There is no real leather in the current line."),
 ("Where are Jones bags made?",
  "Jones is based in Portland, Oregon, and states that customisation and embroidery are done in house there. The "
  "company does not state a country of manufacture for the bags themselves on any product page, and the University "
  "of Oregon&rsquo;s 2021 profile refers to overseas manufacturing relationships without naming a country."),
 ("Why do the Campus Collection bags cost more?",
  "Because they are officially licensed, and the licence carries a markup. A Trouper is $315 in the standard line "
  "and $385 in school colours. A Rider is $520 standard and $555 licensed. Eighteen schools are covered."),
 ("Do tour players use Jones bags?",
  "Jones names one player on its own site: James Nicholas, a brand ambassador on the Korn Ferry Tour who Jones say "
  "won in Bogot&aacute;, Colombia in February 2026. Beyond that they make no tour claim. Carnahan told Golf Digest "
  "the company does not pay players: &ldquo;They buy it because they want it, not because we&rsquo;re paying them "
  "to carry it.&rdquo;"),
]

INTRO = """    <p>Jones Sports Company has been making single-strap carry bags in Portland, Oregon since 1971, and the
founding story is better than most because it is small. George Jones was a forty-year-old taxi driver. He sewed the
first bags in his basement and sold them out of the trunk of his cab. Jones still tells it that way on their own
history page, and finishes the thought with a line that is hard to improve on: &ldquo;Who could have known? George
Jones, that&rsquo;s who.&rdquo;</p>
    <p>What their site skips is the middle. George sold the company in 1990. The new owners tried to make a Jones bag
compete with the big manufacturers by making it less like a Jones bag, and it did not work; by the early 2000s the
brand was effectively gone. The Lemman family and Chris Carnahan bought it in 2011, and what they bought was almost
nothing. Matt Lemman, asked later what came with the deal: &ldquo;Just the name, that was all.&rdquo; No patterns, no
inventory, no factory.</p>
    <p>So they reverse-engineered it. Carnahan has said they gathered old bags from family and friends around
Portland &mdash; there were plenty, because this is a Portland brand and the bags last &mdash; and rebuilt to the
original specifications in modern materials. That is why the Original looks like the photographs from 1975 and weighs
2.9 lbs.</p>
    <p>Thirty-two pieces from the current line below, across every bag they make plus the collaborations, with prices
as Jones lists them. One correction to something you will read elsewhere: Jones does not claim anywhere on its own
site to have invented the single-strap carry bag, and we are not going to claim it for them.</p>
"""

# ---------------- build ----------------
by_sec = {}
for it in PLAN["items"]:
    if it["slug"] in DL:
        by_sec.setdefault(it["sec"], []).append(it)

def card(it):
    imgs = DL[it["slug"]]
    frames = "".join(
        '<div class="pg-frame"><img src="%s" alt="Jones Sports Co %s" loading="lazy" /></div>'
        % (src, H.escape(it["title"])) for src in imgs)
    price = "$" + it["price"].rstrip("0").rstrip(".") if "." in it["price"] else "$" + it["price"]
    sold = "" if it.get("avail", True) else " &middot; sold out"
    return ('    <div class="product-card" data-frames="%d">\n'
            '      <div class="product-gallery"><div class="pg-track">%s</div></div>\n'
            '      <div class="product-body">\n'
            '        <div class="product-brand">Jones Sports Co</div>\n'
            '        <div class="product-name">%s &middot; %s%s</div>\n'
            '        <div class="product-desc">%s</div>\n'
            '        <a href="%s" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a>\n'
            '      </div>\n    </div>\n') % (
        len(imgs), frames, H.escape(it["title"]), price, sold, COPY.get(it["slug"], ""), it["url"])

body = []
ncards = 0
for name, anchor, _ in PLAN["sections"]:
    items = by_sec.get(anchor, [])
    if not items: continue
    kicker, blurb = SECTION_COPY[anchor]
    cards = "".join(card(i) for i in items); ncards += len(items)
    body.append('<h2 id="%s">%s</h2>\n<p class="cat-kicker"><strong>%s</strong>%s</p>\n<div class="products-grid">\n%s</div>\n'
                % (anchor, name, kicker, blurb, cards))

faq_html = "".join('    <details class="faq-q"><summary>%s</summary><p>%s</p></details>\n' % (q, a) for q, a in FAQ)
faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": re.sub(r"&[a-z]+;", "'", q),
     "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"&[a-z]+;", "'", a)}} for q, a in FAQ]},
    ensure_ascii=False)

h = BASE
h = h.replace("the-custom-wedge-report", SLUG)
h = h.replace("/images/custom-wedges/hero.jpg", "/images/jones-sports-co/hero.jpg")
h = re.sub(r"<title>.*?</title>", "<title>%s &mdash; The Grassy Issue</title>" % TITLE, h, flags=re.S)
for pat in ['name="description"', 'property="og:description"', 'name="twitter:description"']:
    h = re.sub(r'(<meta %s content=")[^"]*(")' % re.escape(pat), lambda m: m.group(1) + DESC + m.group(2), h)
for pat in ['property="og:title"', 'name="twitter:title"']:
    h = re.sub(r'(<meta %s content=")[^"]*(")' % re.escape(pat), lambda m: m.group(1) + TITLE + m.group(2), h)
h = re.sub(r'(<h1[^>]*>).*?(</h1>)', lambda m: m.group(1) + TITLE + m.group(2), h, count=1, flags=re.S)
h = re.sub(r'(<div class="writeup-body">).*?(</div>)', lambda m: m.group(1) + "\n" + INTRO + "  " + m.group(2),
           h, count=1, flags=re.S)

start = h.find('<section class="products">')
fq = h.find('<h2 class="products-hdr sec">Questions</h2>')
assert start > 0 and fq > start, "anchors not found"
h = h[:start] + '<section class="products">\n' + "".join(body) + '\n  ' + h[fq:]
h = re.sub(r'(<div class="faq">).*?(  </div>\n</section>)', lambda m: m.group(1) + "\n" + faq_html + m.group(2),
           h, count=1, flags=re.S)
for b in list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)):
    if '"FAQPage"' in b.group(1):
        h = h[:b.start()] + '<script type="application/ld+json">' + faq_ld + '</script>' + h[b.end():]
        break
for b in reversed(list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S))):
    try: d = json.loads(b.group(1))
    except Exception: continue
    if isinstance(d, dict) and d.get("@type") in ("Article", "BlogPosting", "NewsArticle"):
        d["headline"] = TITLE_PLAIN; d["description"] = DESC
        if "image" in d:
            u = "https://thegrassyissue.com/images/jones-sports-co/hero.jpg"
            d["image"] = [u] if isinstance(d["image"], list) else u
        h = h[:b.start()] + '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False, indent=2) + '</script>' + h[b.end():]
h = h.replace("The Custom Wedge Report — Stamping Shops, Forged Makers and What “Custom” Actually Means", TITLE_PLAIN)
h = re.sub(r'<span>\d+ Wedges</span>', '<span>32 Pieces</span>', h)
h = h.replace('<span class="hashtag">#CustomWedges</span>', '<span class="hashtag">#JonesSportsCo</span>')
h = h.replace('alt="Grindworks 86 RAW forged custom golf wedge, tumbled raw finish"',
              'alt="Jones Sports Co single strap carry bag, made in Portland Oregon since 1971"')
h = re.sub(r'(<span class="l">Wedges</span><span>)\d+(</span>)',
           lambda m: '<span class="l">Pieces</span><span>%d</span>' % ncards, h)
h = re.sub(r'(<span class="l">Brands</span><span>)\d+(</span>)', lambda m: m.group(1) + "1" + m.group(2), h)

MORE = ("""    <a href="/drops/the-stand-bag-edit" class="more-card"><div class="more-kicker">The Edit</div><div class="more-title">The Stand Bag Edit</div></a>
    <a href="/drops/the-payntr-collab-edit" class="more-card"><div class="more-kicker">The Edit</div><div class="more-title">The PAYNTR Collab Edit</div></a>
    <a href="/drops/brand-to-know-beams-golf" class="more-card"><div class="more-kicker">Brand to Know</div><div class="more-title">BEAMS Golf</div></a>
    <a href="/drops/the-custom-wedge-report" class="more-card"><div class="more-kicker">The Edit</div><div class="more-title">The Custom Wedge Report</div></a>
""")
m = re.search(r'(<div class="more-grid">)(.*?)(</div>\s*</section>)', h, re.S)
if m:
    h = h[:m.start()] + m.group(1) + "\n" + MORE + "  " + m.group(3) + h[m.end():]

out = os.path.join(S, "drops", SLUG + ".html")
open(out, "w", encoding="utf-8").write(h)
print("wrote", out)
print("  cards:", ncards, "| frames:", sum(len(DL[i["slug"]]) for s in by_sec.values() for i in s))
print("  div balance:", len(re.findall(r"<div\b", h)) == h.count("</div>"))
print("  anchor balance:", len(re.findall(r"<a\b", h)) == h.count("</a>"))
for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S): json.loads(m.group(1))
print("  json-ld: ok")
