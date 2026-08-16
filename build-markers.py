#!/usr/bin/env python3
# Builds /drops/the-ball-marker-atlas.html — 77 markers, 9 categories.
import re, json, os

S = os.path.dirname(os.path.abspath(__file__))
BASE = open(os.path.join(S, "drops/the-payntr-collab-edit.html"), encoding="utf-8").read()
IMGDIR = os.path.join(S, "images/ball-markers")
META = json.load(open("/tmp/mk/meta.json"))

TITLE = "The Ball Marker Atlas — 77 Markers From 20 Brands"
SLUG = "the-ball-marker-atlas"
DESC = ("Seventy-seven golf ball markers across nine categories, from the Long Island shop whose "
        "copper was in the bag for back-to-back Masters wins to hand-forged bronze, licensed "
        "Coca-Cola, tournament one-offs and everything under twenty dollars.")

ORDER = ["The Long Island Guy","Hand-Forged Metal","Pop Culture","Licensed for Real",
         "Tournaments and Courses","Drinks and Snacks","Collabs","Leather and Other Materials","Under Twenty"]

HEADS = {
 "The Long Island Guy": ("Golf Life Metals",
  "Jon Millman works out of a unit on Broadhollow Road in Melville, New York. He hand stamps, torches and paints 1.25&quot; copper discs, and his site says the results have been in play at Majors, the Olympics and the Ryder Cup. It also says &ldquo;back to back Masters won with GLM.&rdquo; The storefront sells replicas of the winning ones."),
 "Hand-Forged Metal": ("Anvil Work",
  "Seamus forges theirs in Portland, Oregon. Fyfe does the same in Scotland. Bronze, copper, steel, nickel and oil can, all struck rather than cast, which is why no two come out identical."),
 "Pop Culture": ("References",
  "The category where a marker stops being a marker and starts being a small opinion about what you like."),
 "Licensed for Real": ("Actual Trademark Deals",
  "Licensing costs money, which is why almost nobody at this scale does it. Pins &amp; Aces has Coca-Cola. SWAG has Tito's."),
 "Tournaments and Courses": ("Places and Dates",
  "Championship one-offs and course-specific pieces, including two named for a hill in Gloucestershire."),
 "Drinks and Snacks": ("Food and Beverage",
  "This is a real category. Matchstick alone makes three flavours of a Gatorade parody, two iced coffees and an Old Fashioned."),
 "Collabs": ("Two Names on One Disc",
  "Seamus does most of the forging for other people's ideas, which is how a Portland blacksmith ends up making an owl for a brand in Los Angeles."),
 "Leather and Other Materials": ("Not Metal",
  "Leather, enamel sets and brushed gold, for anyone who thinks a forged copper disc is a bit much."),
 "Under Twenty": ("Cheap and Good",
  "Nothing here costs more than twenty dollars and several are under ten."),
}

COPY = {
"glm-rory-masters-2026": "The 2026 one. GLM's homepage leads with &ldquo;Rory's Masters markers (both)&rdquo; and hosts a video called Making Rory's Grand Slam Marker.",
"qg-seamus-bronze-owl": "An owl in bronze. Quiet Golf sends the design, Seamus swings the hammer. Sold out.",
"qg-seamus-copper-monogram": "Copper monogram, same partnership, also gone.",
"winston-pull-up-leather": "Pull-up leather rather than metal, so it ages like a wallet.",
"golf-life-metals-rory-s-masters-winning-mark": "The 2026 one. GLM's homepage leads with &ldquo;Rory's Masters markers (both)&rdquo; and hosts a video called Making Rory's Grand Slam Marker.",
"golf-life-metals-rory-s-masters-winnin": "The 2025 Masters marker, the one that completed the career Grand Slam.",
"golf-life-metals-rory-s-players-winnin": "Players Championship, 2025. Same hands, same copper.",
"golf-life-metals-tommy-s-tour-champion": "Tommy Fleetwood's 2025 Tour Championship marker.",
"golf-life-metals-darren-clarke-s-senio": "Darren Clarke's 2021 Senior Open winner, and proof this is not a recent fluke.",
"golf-life-metals-shane-lowry-s-ryder-c": "Lowry's Ryder Cup piece. GLM also lists an official Ryder Cup marker.",
"golf-life-metals-jack-nicklaus-glm-mar": "They made one for Jack. The site's line is &ldquo;we've made for Jack, Tiger, Scottie.&rdquo;",
"golf-life-metals-grand-slam-marker": "The Grand Slam design, sold to anyone.",
"golf-life-metals-us-open-shinnecock": "Shinnecock, torched copper, hand-painted numerals.",
"golf-life-metals-fuck-bogeys": "Sits in the same catalogue as the Nicklaus marker. That is the whole personality of the shop in one product listing.",
"golf-life-metals-copper-blanks": "Six dollars for a raw copper disc, if you would rather stamp your own.",
"seamus-golf-hand-forged-anvil-steel-ba": "An anvil, struck on an anvil. Steel.",
"seamus-golf-hand-forged-sakura-ball-ma": "Cherry blossom in copper, and the prettiest thing Seamus forges.",
"seamus-golf-hand-forged-lucky-horsesho": "Steel horseshoe. The $48 tier is where the more involved shapes live.",
"seamus-golf-hand-forged-labyrinth-ball": "A maze in copper. Reads as texture from a foot away.",
"seamus-golf-hand-forged-mesh-dimple-ba": "Dimple pattern in steel, so the marker matches the ball.",
"seamus-golf-hand-forged-touch-gorse-br": "Named for the gorse you will be visiting later.",
"fyfe-golf-bronze-metal-hand-forged-fyf": "Fyfe's house mark in bronze, hand forged in Scotland. &pound;25.",
"fyfe-golf-copper-metal-hand-forged-fyf": "The copper version, which takes a patina faster.",
"fyfe-golf-the-brave-copper-hand-forged": "The Brave, in copper.",
"hame-golf-co-old-tom-copper-marker": "Old Tom Morris in copper from Hame. Sold out, and they make these in small runs.",
"matchstick-golf-truffle-shuffle": "Chunk from The Goonies, in enamel, on a golf course. Nobody asked for this and it is the best thing they make.",
"matchstick-golf-vw-bus": "Orange split-screen bus.",
"matchstick-golf-teddy-roosevelt": "Teddy, pince-nez and all.",
"matchstick-golf-chef-skull": "Skull in a toque over crossed bones.",
"matchstick-golf-caddysaurus": "A dinosaur carrying a bag.",
"matchstick-golf-pirate-flag": "Jolly Roger reading THE COAST.",
"matchstick-golf-josh-allen-buffalo-bil": "A licensed-looking Bills tribute. Buffalo will buy every one.",
"seamus-golf-hand-forged-the-dude-ball-": "The Dude, in bronze. Abides.",
"seamus-golf-hand-forged-jack-nicklaus-": "Nicklaus's &ldquo;Yes Sir!&rdquo; in bronze, the 1986 call rendered as an object.",
"mark-lona-majestic-iron-skull-marker": "Japanese, iron, skull. &yen;10,125, which makes it the most expensive marker here that is not custom copper.",
"pins-aces-coca-cola-bottle-ball-marker": "An actual Coca-Cola licence on a $14.95 ball marker. The contour bottle, correctly rendered.",
"pins-aces-coca-cola-bear-ball-marker": "The polar bear, same deal.",
"pins-aces-blazy-susan-silhoutte-ball-m": "Blazy Susan makes pink rolling papers. This is a co-branded golf ball marker. Read that twice.",
"pins-aces-blazy-susan-smoke-pink-ball-": "The pink smoke version.",
"swag-golf-tito-s-splash-of-grape-ball-": "Tito's, $66.66, which is SWAG's house price and also a choice.",
"swag-golf-tito-s-water-hazard-ball-mar": "The water hazard variant. Same price, same joke.",
"seamus-golf-2026-u-s-women-s-open-rivi": "Riviera, 2026 U.S. Women's Open. Forged, not printed.",
"seamus-golf-2025-ryder-cup-ball-marker": "Bronze Ryder Cup marker for 2025.",
"golf-by-qd-ocean-course-qd-ball-marker": "Kiawah's Ocean Course, from a Mexican brand that mostly makes caddie crowns.",
"sounder-cleeve-hill-ball-marker": "&pound;5 for a marker named after Cleeve Hill in Gloucestershire, which is where Sounder is from.",
"sounder-cleeve-hill-northern-ball-mark": "The same idea in a &pound;65 tin. Sold out.",
"pins-aces-azalea-ball-marker": "Azalea. You know which hole.",
"pins-aces-5280-ball-marker": "Denver's elevation in feet, which is also a local shorthand.",
"pins-aces-liberty-bell-ball-marker": "Philadelphia, crack included.",
"matchstick-golf-putterade-lemon-lime": "A Gatorade bottle relabelled Putterade. There are three flavours.",
"matchstick-golf-iced-coffee": "Iced coffee with a straw. There is a gold version too.",
"matchstick-golf-old-fashioned": "Rocks glass, orange peel, cherry.",
"matchstick-golf-transfusion": "The drink every muni sells and nobody outside golf has heard of.",
"matchstick-golf-flaming-coffee-mug": "A mug on fire with a face. For the front nine.",
"fella-golf-pizza-slice-double-ball-mar": "A slice, from a European brand, doubling as two markers.",
"pins-aces-red-party-cup-ball-marker": "The red Solo cup, in miniature.",
"pins-aces-ice-cubes-ball-marker": "Two ice cubes. Best paired with the one above.",
"swag-golf-rwb-ice-pop-ball-marker": "Red, white and blue rocket pop.",
"seamus-press-golf-panda-tiger": "Seamus forging an artist edition for Press Golf. Panda tiger, which is exactly as odd as it sounds.",
"seamus-pendleton-hand-forged-pendleton": "Sugar skulls in oil can finish, done with Pendleton, who also supply the wool for their towels.",
"quiet-golf-seamus-qg-x-seamus-hand-forged-bro": "An owl in bronze. Quiet Golf sends the design, Seamus swings the hammer. Sold out.",
"quiet-golf-seamus-qg-x-seamus-hand-forged-cop": "Copper monogram, same partnership, also gone.",
"quiet-golf-seamus-qg-x-seamus-hand-for": "Steel pennant, completing the set.",
"parmore-posterlad-limited-release-parm": "Parmore with the designer Posterlad. &pound;10 and the cleanest graphic here.",
"random-golf-club-northwood-northwood-x": "Random Golf Club with Northwood. Sold out.",
"malbon-golf-shanghai-buckets-ball-mark": "Malbon's Shanghai Buckets, marking a store rather than a tournament.",
"malbon-golf-nimbus-buckets-ball-marker": "The Nimbus version, same series.",
"winston-collection-winston-collection-pull-up": "Pull-up leather rather than metal, so it ages like a wallet.",
"winston-collection-winston-collection-": "Tradition leather, the tidier sibling.",
"walker-golf-ball-marker-crest-3-pack-b": "Three crests, black, green and brushed gold, from Australia.",
"birds-of-condor-at-the-turn-ball-mark-": "A hot dog, a beer and a pie in enamel. Australian and accurate.",
"birds-of-condor-blockbusters-ball-mark": "Three film references in a set.",
"matchstick-golf-flame-magnetic-ball-ma": "Six dollars for a magnetic flame pin. The cheapest thing on this page.",
"matchstick-golf-mystery-draw-ball-mark": "Ten dollars and you get whatever they send. The product photo is a question mark.",
"left-of-field-flower-ball-marker-silve": "A$10, silver and sage, from Sydney.",
"left-of-field-script-ball-marker-dark-": "A$7 script marker in dark green.",
"eastside-golf-magnetic-coin-marker": "Eastside's magnetic coin at $13.",
"vessel-metal-ball-marker": "Fifteen dollars, plain metal, made to disappear into a Vessel bag.",
"casualist-ball-marker": "An eight-point star with an eye at the centre. &pound;15, sold out.",
"radmor-bobrad-ball-marker": "BobRad, $15.",
"birds-of-condor-golf-geek-ball-mark": "GOLF GEEK in a comic-book bubble. A$19.95.",
}

def imgs(slug):
    p = f"/images/ball-markers/{slug}.jpg"
    return [p] if os.path.exists(S + p) else []

def money(m):
    c, p = m["cur"], m["price"]
    sym = {"USD":"$","GBP":"&pound;","EUR":"&euro;","AUD":"A$","JPY":"&yen;"}.get(c, c+" ")
    if c == "JPY": return f"{sym}{int(p):,}"
    return f"{sym}{int(p) if p==int(p) else f'{p:.2f}'}"

def card(slug, m):
    ims = imgs(slug)
    if not ims: return ""
    alt = re.sub(r"&\w+;|&#\d+;", " ", f"{m['brand']} {m['title']} golf ball marker")
    frames = f'<div class="pg-frame"><img src="{ims[0]}" alt="{alt}" loading="lazy" /></div>'
    so = ' <span class="so">&middot; Sold out</span>' if not m["avail"] else ""
    blurb = COPY.get(slug, "")
    title = m["title"].replace("&", "&amp;")
    title = re.sub(r'\s*[-–]\s*Ball Marker$|\s*Ball Marker$|\s*Ball Mark$', '', title).strip() or m["title"]
    return f"""
    <div class="product-card" data-frames="1">
      <div class="product-gallery"><div class="pg-track">{frames}</div></div>
      <div class="product-body">
        <div class="product-brand">{m['brand']}</div>
        <div class="product-name">{title} &middot; {money(m)}{so}</div>
        <div class="product-desc">{blurb}</div>
        <a href="{m['url']}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a>
      </div>
    </div>"""

grid = ""
for cat in ORDER:
    items = {k: v for k, v in META.items() if v["cat"] == cat}
    if not items: continue
    label, intro = HEADS[cat]
    grid += f'\n  <h2 class="products-hdr sec">{cat} &middot; {label}</h2>\n'
    grid += f'  <p class="sec-intro">{intro}</p>\n  <div class="products-grid">'
    grid += "".join(card(k, v) for k, v in items.items())
    grid += "\n  </div>\n"

FAQ = [
 ("Who makes the ball markers used by tour pros?",
  "Golf Life Metals, run by Jon Millman out of Melville on Long Island, is the one most often in play. Their site states the markers have been used in Majors, PGA tournaments, the Olympics and the Ryder Cup, claims more than 1,500 designs and 50+ tour pros, and says &ldquo;back to back Masters won with GLM.&rdquo;"),
 ("How much does a Golf Life Metals marker cost?",
  "Their listed custom copper markers run roughly $115 to $214. Replicas of tour-winning designs are $115. A raw copper blank is $6."),
 ("What is a hand-forged ball marker?",
  "One struck from metal by hand rather than cast or printed. Seamus Golf forges theirs in Portland, Oregon and Fyfe Golf forges in Scotland, in bronze, copper, steel, nickel and oil can finishes. Because each is struck individually, no two are identical."),
 ("What is the most expensive marker here?",
  "Golf Life Metals custom copper at up to $214. Outside custom work, MARK &amp; LONA's Majestic Iron Skull at &yen;10,125 and SWAG's markers at $66.66 are the top of the range."),
 ("What is the cheapest?",
  "Matchstick Golf's flame magnetic pin and a Golf Life Metals copper blank, both $6. Left of Field's script marker is A$7 and Sounder's Cleeve Hill marker is &pound;5."),
 ("Are any ball markers officially licensed?",
  "A few. Pins &amp; Aces makes Coca-Cola bottle and polar bear markers and a series with the rolling-paper brand Blazy Susan. SWAG Golf makes two for Tito's."),
 ("Which brands make course-specific markers?",
  "Seamus does championship editions including the 2026 U.S. Women's Open at Riviera and the 2025 Ryder Cup. Golf by QD makes one for Kiawah's Ocean Course. Sounder makes two for Cleeve Hill, their home course in Gloucestershire."),
 ("Do prices on this page convert to dollars?",
  "No. Each price is shown in the currency the brand charges: US dollars, British pounds, euros, Australian dollars and Japanese yen."),
]

faq_html = '\n  <h2 class="products-hdr sec">Questions</h2>\n  <div class="faq">' + "".join(
    f'\n    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ) + "\n  </div>\n"

h = BASE
for old in ["The PAYNTR Collab Edit &mdash; 33 Shoes, Bags and Odds From Golf&rsquo;s Busiest Collaborator",
            "The PAYNTR Collab Edit — 33 Shoes, Bags and Odds From Golf's Busiest Collaborator"]:
    h = h.replace(old + " &mdash; The Grassy Issue", TITLE + " &mdash; The Grassy Issue")
    h = h.replace(old + " — The Grassy Issue", TITLE + " — The Grassy Issue")
    h = h.replace(old, TITLE)
h = h.replace("the-payntr-collab-edit", SLUG)
for k in ["description", "og:description", "twitter:description"]:
    h = re.sub(r'(<meta (?:name|property)="%s" content=")[^"]*(")' % re.escape(k),
               lambda m: m.group(1) + DESC + m.group(2), h)

def fix_article(m):
    d = json.loads(m.group(1))
    d["headline"] = TITLE; d["description"] = DESC
    d["url"] = f"https://thegrassyissue.com/drops/{SLUG}"
    d["datePublished"] = "2026-08-14"; d["dateModified"] = "2026-08-14"
    d["mainEntityOfPage"] = {"@type": "WebPage", "@id": f"https://thegrassyissue.com/drops/{SLUG}"}
    return '<script type="application/ld+json">\n' + json.dumps(d, indent=2) + '\n</script>'
h = re.sub(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', fix_article, h, count=1, flags=re.S)

faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":re.sub(r"&\w+;|&#\d+;"," ",q),
   "acceptedAnswer":{"@type":"Answer","text":re.sub(r"&\w+;|&#\d+;"," ",a)}} for q,a in FAQ]}
_blk = '<script type="application/ld+json">\n' + json.dumps(faq_ld, indent=2) + '\n</script>'
h = re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "FAQPage".*?</script>',
           lambda m: _blk, h, count=1, flags=re.S)

h = h.replace("</style>", ".sec-intro{font-family:var(--sans);font-size:13px;line-height:1.6;opacity:.75;max-width:760px;margin:-8px 0 22px}\n</style>", 1)
h = re.sub(r'<div class="drop-hero">.*?</div></div>',
  '<div class="drop-hero"><div class="drop-hero-img"><img src="/images/ball-markers/hero.jpg" '
  'alt="Hand-stamped torched copper golf ball markers from Golf Life Metals on Long Island" /></div></div>',
  h, count=1, flags=re.S)

writeup = """<div class="writeup">
  <div class="writeup-body">
    <p>A ball marker is the cheapest thing in the bag and the only piece of equipment you hand to a stranger. That combination has produced a small industry: seventy-seven markers here, from twenty brands, in nine categories that had to be invented because no existing ones fit.</p>
    <p>The one to know about first works out of a unit on Broadhollow Road in Melville, New York. Jon Millman hand stamps, torches and paints copper discs under the name Golf Life Metals, and his own storefront sells replicas of the markers that won the 2025 and 2026 Masters, the 2025 Players, the 2025 Tour Championship and the 2021 Senior Open. The site says the work has been in play at the Olympics and the Ryder Cup, claims more than fifteen hundred designs for fifty-plus tour pros, and puts it plainly: back to back Masters won with GLM. Six inches down the same page is a marker that says Fuck Bogeys.</p>
    <p>Below that the field splits. Seamus forges in Portland and Fyfe forges in Scotland, both striking metal by hand so nothing comes out twice. Pins &amp; Aces holds a real Coca-Cola licence and another with a rolling-paper company. Matchstick has built a catalogue that includes Chunk from The Goonies, a dinosaur caddie and three flavours of a Gatorade parody. Sounder named two after a hill in Gloucestershire.</p>
    <p>Prices run from six dollars to two hundred and fourteen, in five currencies, none of them converted. Everything below is what the brand charges.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Markers</span><span>77</span></div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>20</span></div>
      <div class="sidebar-detail"><span class="l">Categories</span><span>9</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$6 &ndash; $214</span></div>
      <a href="/"  class="sidebar-cta">&larr; Back to Feed</a>
      <div class="hashtags">
        <span class="hashtag">#TheGrassyIssue</span>
        <span class="hashtag">#GolfCulture</span>
        <span class="hashtag">#BallMarkers</span>
        <span class="hashtag">#GearEdit</span>
      </div>
    </div>
  </aside>
</div>"""
h = re.sub(r'<div class="writeup">.*?</aside>\s*</div>', writeup, h, count=1, flags=re.S)
h = h.replace("<span>33 Pieces</span>", "<span>77 Markers</span>")

start = h.find('<section class="products">')
end = h.find('<section class="more"')
if end == -1: end = h.find('<div class="more"')
assert start != -1 and end != -1 and end > start
h = h[:start] + '<section class="products">\n' + grid + faq_html + '</section>\n\n' + h[end:]

out = os.path.join(S, f"drops/{SLUG}.html")
open(out, "w", encoding="utf-8").write(h)
print("wrote", out, len(h), "bytes")
