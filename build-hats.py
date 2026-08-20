#!/usr/bin/env python3
# Builds /drops/the-hat-edit-austin-summer.html
import re, json, os, html as H

S = os.path.dirname(os.path.abspath(__file__))
BASE = open(os.path.join(S, "drops/the-custom-wedge-report.html"), encoding="utf-8").read()
SEL = json.load(open("/tmp/ht/final4.json"))
DL  = json.load(open("/tmp/ht/dl_hats.json"))

SLUG = "the-hat-edit-austin-summer"
TITLE = "The Hat Edit &mdash; 28 Summer Caps, Ropes and Buckets From the Brands We Follow"
TITLE_PLAIN = "The Hat Edit — 28 Summer Caps, Ropes and Buckets From the Brands We Follow"
DESC = ("Twenty-eight golf hats from twenty-two independent brands, chosen for an Austin August. Rope crowns, "
        "mesh truckers, perforated caps and full-brim buckets. No visors, no beanies, no wool. Prices in the "
        "currency each brand charges.")

SECTIONS = [
 ("Rope Crowns", "rope", "The Summer Default",
  "A rope across the front of an unstructured crown is the shape that says golf without saying much else. Most of "
  "these are cotton twill and most sit low. Two of them &mdash; the Pins &amp; Aces and the Ghost &mdash; are "
  "perforated as well, which is the difference between a hat you wear for nine and one you wear for eighteen."),
 ("Mesh, Vents and Actual Airflow", "mesh", "Built for Heat, Not Just Photographed in It",
  "The category that matters most in August and gets the least attention. Trucker backs, perforated crowns, mesh "
  "side panels. Radry&rsquo;s trucker is thirty dollars and the cheapest hat in this entire edit."),
 ("Full Brim", "brim", "When a Cap Isn't Enough",
  "Four buckets, and one of them has a neck flap. If you have played Lions or Hancock at two in the afternoon in "
  "July you already understand why this section exists."),
 ("Caps, Dad Hats and Snapbacks", "caps", "The Rest of It",
  "Cotton twill, five panels, structured and unstructured. Nothing technical, nothing claiming to wick. These are "
  "the ones you keep in the car."),
]

ASSIGN = {
 "rope": ["Malbon TORREY PINES ROPE HAT","Sunday Golf Sunday Golf Rope Hat","Field Day Sporting Co. Signature Rope Hat",
          "Seamus Golf Seamus Club Protection Hat","Pins & Aces Perforated Rope Hat","Eastside Golf Prime Green Ace Hat"],
 "mesh": ["Radry Golf Rhino Pills Trucker Hat","Sunday Golf Trucker Golf Hat","Ghost Golf CORE LOGO HAT",
          "Sugarloaf Social Club THE PLAYERS x SSC Runner Cap"],
 "brim": ["Manors Recycled Greenskeeper Bucket Hat","Gumtree Golf & Nature Nature Club - Fishing Hat",
          "Malbon INKWASH BUCKET HAT","Public Drip \"P\" Script Nylon Bucket Hat"],
}

COPY = {
"malbon-torrey-pines-rope-hat":
 "White crown, navy rope, Torrey Pines across the front. Malbon at their most restrained, which is when they are best.",
"sunday-golf-sunday-golf-rope-hat-white-black":
 "White rope crown, black script, thirty-five dollars. Sunday make the plainest good version of this shape.",
"field-day-sporting-co-signature-rope-hat-loden-gold":
 "Loden and gold. Field Day photograph every hat on a wooden stand rather than a model, which is a small thing that makes their whole catalogue look considered.",
"seamus-golf-seamus-club-protection-hat-green":
 "Green rope crown with a stitched leather patch. The best-made hat in this edit, and Seamus forge metal for a living so the patch is not an accident.",
"pins-aces-perforated-rope-hat-pheasant":
 "A pheasant, on cream, with the crown perforated throughout. Pins &amp; Aces have fourteen photographs of this hat on their own site.",
"eastside-golf-prime-green-ace-hat":
 "Green rope with a circle patch. The cleanest shape Eastside make and the one that does not shout.",
"radry-golf-rhino-pills-trucker-hat":
 "Mesh back, thirty dollars, and the cheapest thing in this edit by some distance. Radry&rsquo;s catalogue is mostly sold out, so catch this one while it is live.",
"sunday-golf-trucker-golf-hat-brown":
 "Brown and white, mesh back. A trucker breathes better than anything else here and this one does not look like a giveaway.",
"ghost-golf-core-logo-hat":
 "Perforated right across the crown. Ghost build for heat rather than mentioning it in the copy, though sixty dollars is a real ask for a plain cap.",
"sugarloaf-social-club-the-players-x-ssc-runner-cap":
 "Light blue five-panel with mesh sides, done with THE PLAYERS. The one you would actually walk eighteen in.",
"manors-recycled-greenskeeper-bucket-hat":
 "Recycled fabric, and the only bucket Manors make. Full brim, which is the point.",
"gumtree-golf-nature-nature-club-fishing-hat":
 "Wide brim, neck flap, 70/30 cotton-nylon that Gumtree say is water and stain repellent. The most genuinely sun-proof thing in the edit.",
"malbon-inkwash-bucket-hat":
 "Inkwash blue camo. The Malbon you would reach for in August rather than the one you would photograph.",
"public-drip-p-script-nylon-bucket-hat-white":
 "White nylon rather than canvas, which matters when it is a hundred degrees and you are sweating into it.",
"manors-course-cap":
 "Manors&rsquo; plainest cap and their best &mdash; white, a small checker tab, nothing else. Thirty-five pounds.",
"gumtree-golf-nature-club-di-golf-e-natura-gumtree-da":
 "Cream cotton with Negroni-orange Italian script. Gumtree are Australian and the joke is deliberate.",
"radry-golf-gangs-here-hat":
 "Green crown, orange flame script. Radry get away with things most brands their size cannot.",
"macade-range-snapback-jade":
 "Jade. Macade choose colour better than almost anyone on this list and this is the proof.",
"field-day-sporting-co-wga-is-for-boys-and-girls-cadd":
 "A two-tone caddie cap tied to the Western Golf Association, whose Evans Scholars programme sends caddies to college.",
"fella-golf-contrast-stitch-dad-cap-all-gear-no-game":
 "Teal, contrast stitching, and the text does all the work. Fella know what they are.",
"huega-house-athletic-association-hat-brown":
 "Brown crown, cream collegiate script, San Diego and 2022 stacked underneath. Huega&rsquo;s cleanest.",
"siegelman-stable-siegelman-stable-dad-hat":
 "Cream crown, olive brim, the horse. The most wearable thing Siegelman make and the least shouty.",
"devereux-garage-hat-black-white":
 "Pinstripe, which almost nobody does on a golf cap. It works.",
"students-golf-always-together-snap-back-hat":
 "Black and white, structured. Students&rsquo; cleanest snapback.",
"random-golf-club-royal-snowball-hat":
 "Green with a shield patch, twenty dollars. The cheapest good hat here and it does not look like it.",
"matchstick-west-coast-classic-dad-hat-navy":
 "Navy, PNW script. Same catalogue that produced the Goonies ball marker, which tells you the register.",
"birds-of-condor-feel-good-sports-cap":
 "Blue, red and yellow panels. The Australians being Australian, and a relief in a grid full of navy.",
"olydoe-og-hat-olydoe-shield":
 "Cream with a red shield. Quiet, and priced like it isn&rsquo;t trying.",
}

FAQ = [
 ("What kind of golf hat is best for extreme heat?",
  "Anything that moves air. A trucker back, a perforated crown or mesh side panels will all beat solid cotton twill. "
  "In this edit that means Radry&rsquo;s Rhino Pills trucker, Sunday&rsquo;s brown trucker, Ghost&rsquo;s perforated "
  "Core Logo and Sugarloaf&rsquo;s mesh-sided Runner Cap. A full-brim bucket covers more skin than any cap, and "
  "Gumtree&rsquo;s fishing hat adds a neck flap on top of that."),
 ("Why are there no visors or beanies here?",
  "A visor leaves the top of your head exposed, which is the part that burns. A beanie is a different season "
  "entirely. We also cut wool, corduroy and velvet, all of which appear on these brands&rsquo; sites and none of "
  "which belong in Texas in August."),
 ("What is the cheapest hat in this edit?",
  "Random Golf Club&rsquo;s Royal Snowball at $20, then Radry&rsquo;s Rhino Pills trucker at $30. At the other end, "
  "Ghost Golf&rsquo;s Core Logo is $60 and Gumtree&rsquo;s fishing hat is A$65."),
 ("Are these prices in US dollars?",
  "Not all of them. Manors is in pounds, Gumtree and Birds of Condor are in Australian dollars, and Macade is in "
  "pounds. Nothing here is converted &mdash; each price is what the brand itself charges, in its own currency."),
 ("Which of these brands ship to the US?",
  "Most do, but not all on the same terms. Gumtree sells from Australia through Squarespace rather than a "
  "conventional store, and Manors ships from the UK. Check each brand&rsquo;s own shipping page before ordering, "
  "because international duty is usually the buyer&rsquo;s problem."),
 ("What is a rope hat and why does every golf brand make one?",
  "A cord stitched across the front seam of an unstructured or lightly structured crown. It is a 1970s trucker "
  "detail that came back through golf, and it is cheap to add, which is part of why the shape is everywhere. Six of "
  "the twenty-eight hats here are rope crowns."),
 ("Do any of these brands make more than what is shown?",
  "All of them. This is a cut, not a catalogue &mdash; the sweep behind it covered 705 hats across 35 brands and "
  "530 of those were in stock. Radry in particular has a much deeper line, which is why they have their own post on "
  "this site."),
 ("What was left out and why?",
  "Anything wool, corduroy, velvet or knit, on seasonal grounds. Anything with fewer than three usable product "
  "photographs, because a card with one photo looks broken next to a card with five. And a lot of plain logo caps "
  "that were perfectly fine and completely uninteresting."),
]

INTRO = """    <p>It is August in Austin, which means the back nine happens at a hundred degrees and the only equipment
decision that actually affects your afternoon is what is on your head. So this is a hat edit built for that
specifically: rope crowns, mesh backs, perforated panels and full brims, from twenty-two brands we already follow.</p>
    <p>What is not here is as deliberate as what is. No visors, because the top of your head is the part that burns.
No beanies, for reasons that should not need explaining. And no wool, corduroy or velvet, all of which these same
brands make and all of which can wait until November.</p>
    <p>The sweep behind this ran to 705 hats across 35 brands, 530 of them in stock. Everything below is live as of
today, has at least three usable product photographs, and is priced in the currency the brand actually charges &mdash;
pounds for Manors and Macade, Australian dollars for Gumtree and Birds of Condor, nothing converted.</p>
"""

# ---------------- build ----------------
def sec_of(x):
    key = x["brand"] + " " + x["title"]
    for s, names in ASSIGN.items():
        for n in names:
            if key.startswith(n[:44]): return s
    return "caps"

buckets = {}
for x in SEL:
    if x["slug"] in DL: buckets.setdefault(sec_of(x), []).append(x)

SYM = {"USD?": "$", "GBP": "&pound;", "AUD": "A$", "EUR": "&euro;", "JPY": "&yen;"}
def money(x):
    p = str(x["price"]); v = p.rstrip("0").rstrip(".") if "." in p else p
    return SYM.get(x["cur"], "$") + v

def card(x):
    imgs = DL[x["slug"]]
    frames = "".join('<div class="pg-frame"><img src="%s" alt="%s %s golf hat" loading="lazy" /></div>'
                     % (s, H.escape(x["brand"]), H.escape(x["title"])) for s in imgs)
    return ('    <div class="product-card" data-frames="%d">\n'
            '      <div class="product-gallery"><div class="pg-track">%s</div></div>\n'
            '      <div class="product-body">\n'
            '        <div class="product-brand">%s</div>\n'
            '        <div class="product-name">%s &middot; %s</div>\n'
            '        <div class="product-desc">%s</div>\n'
            '        <a href="%s" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a>\n'
            '      </div>\n    </div>\n') % (
        len(imgs), frames, H.escape(x["brand"]), H.escape(x["title"]), money(x), COPY.get(x["slug"], ""), x["url"])

body = []; ncards = 0
for name, key, kicker, blurb in SECTIONS:
    items = buckets.get(key, [])
    if not items: continue
    ncards += len(items)
    body.append('<h2 id="%s">%s</h2>\n<p class="cat-kicker"><strong>%s</strong>%s</p>\n<div class="products-grid">\n%s</div>\n'
                % (key, name, kicker, blurb, "".join(card(i) for i in items)))

faq_html = "".join('    <details class="faq-q"><summary>%s</summary><p>%s</p></details>\n' % (q, a) for q, a in FAQ)
faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": re.sub(r"&[a-z]+;", "'", q),
     "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"&[a-z]+;", "'", a)}} for q, a in FAQ]}, ensure_ascii=False)

h = BASE
h = h.replace("the-custom-wedge-report", SLUG)
h = h.replace("/images/custom-wedges/hero.jpg", "/images/hat-edit/hero.jpg")
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
assert start > 0 and fq > start
h = h[:start] + '<section class="products">\n' + "".join(body) + '\n  ' + h[fq:]
h = re.sub(r'(<div class="faq">).*?(  </div>\n</section>)', lambda m: m.group(1) + "\n" + faq_html + m.group(2),
           h, count=1, flags=re.S)
for b in list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)):
    if '"FAQPage"' in b.group(1):
        h = h[:b.start()] + '<script type="application/ld+json">' + faq_ld + '</script>' + h[b.end():]; break
for b in reversed(list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S))):
    try: d = json.loads(b.group(1))
    except Exception: continue
    if isinstance(d, dict) and d.get("@type") in ("Article", "BlogPosting", "NewsArticle"):
        d["headline"] = TITLE_PLAIN; d["description"] = DESC
        if "image" in d:
            u = "https://thegrassyissue.com/images/hat-edit/hero.jpg"
            d["image"] = [u] if isinstance(d["image"], list) else u
        h = h[:b.start()] + '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False, indent=2) + '</script>' + h[b.end():]
h = h.replace("The Custom Wedge Report — Stamping Shops, Forged Makers and What “Custom” Actually Means", TITLE_PLAIN)
h = re.sub(r'<span>\d+ Wedges</span>', '<span>28 Hats</span>', h)
h = h.replace('<span class="hashtag">#CustomWedges</span>', '<span class="hashtag">#TheHatEdit</span>')
h = h.replace('alt="Grindworks 86 RAW forged custom golf wedge, tumbled raw finish"',
              'alt="Golf hats from independent brands, chosen for summer heat"')
h = re.sub(r'(<span class="l">Wedges</span><span>)\d+(</span>)',
           lambda m: '<span class="l">Hats</span><span>%d</span>' % ncards, h)
h = re.sub(r'(<span class="l">Brands</span><span>)\d+(</span>)',
           lambda m: m.group(1) + str(len({x["brand"] for x in SEL})) + m.group(2), h)

MORE = ("""    <a href="/drops/radry-hats-the-full-lineup" class="more-card"><div class="more-kicker">The Edit</div><div class="more-title">Radry Hats &mdash; The Full Lineup</div></a>
    <a href="/drops/brand-revisited-jones-sports-co" class="more-card"><div class="more-kicker">Brand Revisited</div><div class="more-title">Jones Sports Co</div></a>
    <a href="/drops/brand-to-know-sugarloaf-social-club" class="more-card"><div class="more-kicker">Brand to Know</div><div class="more-title">Sugarloaf Social Club</div></a>
    <a href="/drops/the-hot-weather-roundup" class="more-card"><div class="more-kicker">The Roundup</div><div class="more-title">Hot Weather Golf Gear</div></a>
""")
m = re.search(r'(<div class="more-grid">)(.*?)(</div>\s*</section>)', h, re.S)
if m: h = h[:m.start()] + m.group(1) + "\n" + MORE + "  " + m.group(3) + h[m.end():]

out = os.path.join(S, "drops", SLUG + ".html")
open(out, "w", encoding="utf-8").write(h)
print("wrote", out)
print("  cards:", ncards, "| frames:", sum(len(DL[x["slug"]]) for x in SEL if x["slug"] in DL))
print("  sections:", {k: len(v) for k, v in buckets.items()})
print("  div balance:", len(re.findall(r"<div\b", h)) == h.count("</div>"))
print("  anchor balance:", len(re.findall(r"<a\b", h)) == h.count("</a>"))
for mm in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S): json.loads(mm.group(1))
print("  json-ld: ok")
