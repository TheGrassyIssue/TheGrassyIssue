#!/usr/bin/env python3
"""/brands/tag/* and /brands/attr/* — the 18 taxonomy pages the Brand Index has
been linking to, and the sitemap has been advertising, without them existing.

WHY THIS EXISTS
---------------
The 9/17/26 SEO audit found 17 URLs in sitemap.xml that return 404. Every one of
them is a /brands/tag/ or /brands/attr/ page. Five of the seventeen are also
linked from brands/index.html's vibe tiles, so those are internal 404s on top.
Google has been handed a list of dead URLs and a hub page that points into
nothing.

The same audit found the other half of the problem: 132 brand pages, median 105
words, each with EXACTLY ONE inbound internal link. They are starved. These
taxonomy pages are the fix for both at once — each brand appears on every
taxonomy page it qualifies for, so the median brand goes from one inbound link
to three or four, and seventeen dead sitemap rows become seventeen real landing
pages aimed at terms the Index already ranks adjacent to.

THE POINT IS NOT TO MAKE EIGHTEEN MORE THIN PAGES. That would make the problem
worse, not better. Every page here carries hand-written editorial copy that names
specific brands on that page and says something true about why they group. The
INTRO guard below refuses to build any page whose copy is under 90 words or that
does not name at least two brands from its own list.

DATA is data/brands.json (source of truth). CARDS are lifted verbatim from
brands/index.html so a brand's photo and one-liner can never disagree between
the Index and its taxonomy pages. CHROME (head, nav, footer, scripts) is lifted
from an existing brand page so these inherit the header chain, search box and
mobile menu without a second maintenance path.

THE 'loud' TAG IS A TYPO. brands.json gives Swag Golf tags ["loud", "collector",
"design-nerd"]; every other brand of that kind carries "loud-on-purpose". Rather
than silently edit the source of truth mid-flight, ALIAS maps it at build time
and the run prints a reminder. Fix brands.json when convenient and delete ALIAS.

'independent' (22 brands) was NOT in the sitemap's seventeen and has no vibe
tile, but it is a real tag on a fifth of the Index and the page is cheap. Built,
and added to the sitemap by wire-brand-taxonomy.py.

COPY RULES: no 'worth'; no verdicts on brands; counts computed, never typed.
"""
import json, re, os, html, sys, collections
import tax_bodies   # long-form bodies for the taxonomy pages we have built out

ROOT = os.path.dirname(os.path.abspath(__file__))
brands = json.load(open(os.path.join(ROOT, "data", "brands.json"), encoding="utf-8"))
index_html = open(os.path.join(ROOT, "brands", "index.html"), encoding="utf-8").read()
chrome_src = open(os.path.join(ROOT, "brands", "gramicci.html"), encoding="utf-8").read()

ALIAS = {"loud": "loud-on-purpose"}

def tags_of(b):
    return {ALIAS.get(t, t) for t in b.get("tags", [])}

# ---------------------------------------------------------------- the taxonomy
# kind, slug, H1, <title> (<=65 incl suffix), meta description (110-165), intro
TAX = [
("tag", "design-nerd", "Design-Nerd Golf Brands",
 "Design-Nerd Golf Brands — The Grassy Issue",
 "Thirty-seven golf brands that treat design as the product rather than the packaging — from milled putters to socks with a point of view.",
 """<p>This is the largest group in the Index, and the loosest, which is usually a sign a
 category is real rather than invented. What connects <strong>Bettinardi</strong> milling a putter
 from one billet, <strong>Inside Story Socks</strong> printing a narrative into a sock, and
 <strong>A.P.C. Golf</strong> applying a French ready-to-wear house's restraint to a quarter-zip is
 not a look. It is a sequence: the design decision comes first and the golf application comes
 second, rather than a golf product getting a graphic applied at the end.</p>
 <p>You can tell them apart from the merely handsome by what they will not do. A design-led brand
 will ship fewer colourways, hold a silhouette across seasons, and answer a question about
 construction with an actual answer. <strong>Edel</strong> will sell you five hosels because aim bias
 is measurable. <strong>Evnroll</strong> will explain a groove pattern. That willingness to be
 specific in public is the tell.</p>""",
 ),
("tag", "made-by-hand", "Golf Brands That Make It By Hand",
 "Handmade Golf Gear — Small-Batch Brands | The Grassy Issue",
 "Thirty-three golf brands where a person still makes the thing — wedges ground by hand, headcovers cut one at a time, course maps painted to order.",
 """<p>The honest version of &ldquo;handmade&rdquo; is narrow, and this is our attempt to hold the
 line on it. <strong>Artisan Golf</strong> qualifies because Mike Taylor still grinds every wedge
 himself and you cannot order one without an in-person fitting. <strong>Ally Aiken</strong>
 qualifies because every course map is watercolour-painted by the named artist, commissions taken
 one at a time. <strong>Clint Orms</strong> qualifies because a belt buckle is engraved by a
 silversmith in Ingram, Texas.</p>
 <p>What does not qualify: a factory run with a hand-finished detail, or a story about heritage
 attached to a volume product. The practical consequence for a buyer is lead time and scarcity —
 most of the brands here quote weeks rather than days, and several will simply be out. That is the
 trade, and it is the reason the group exists as its own shelf rather than being folded into
 design-led.</p>""",
 ),
("tag", "loud-on-purpose", "Loud Golf Brands, On Purpose",
 "Loud Golf Brands — Bold Apparel & Headcovers | The Grassy Issue",
 "Twenty-five golf brands built to be seen — maximal prints, painted headcovers and graphics that were never going to be subtle.",
 """<p>Loud is a decision, not an accident, and the brands here made it deliberately.
 <strong>Swag Golf</strong> paints headcovers that the rest of the bag has to live up to.
 <strong>Birds of Condor</strong> runs prints that would be at home on a surf shirt.
 <strong>Malbon</strong> built an entire company on the premise that golf clothing had been
 apologising for itself for forty years.</p>
 <p>The useful distinction inside this group is between loud-as-graphic and loud-as-colour.
 <strong>Golf Gods</strong> and <strong>Metalwood Studio</strong> work in imagery and reference;
 <strong>G/FORE</strong> and <strong>J.Lindeberg</strong> work in saturated blocks of colour and
 cut. They land very differently on a first tee and they are shopped for different reasons, which
 is why both sit here rather than being split.</p>""",
 ),
("tag", "independent", "Independent Golf Brands",
 "Independent Golf Brands — Founder-Owned | The Grassy Issue",
 "Twenty-two founder-owned golf brands with no parent company and no outside answer to give — the independent end of the Brand Index.",
 """<p>Independent here means structural, not stylistic: no parent conglomerate, no licensing group,
 nobody upstairs to approve the range. <strong>Bettinardi</strong> is still family-run out of
 Tinley Park. <strong>Eastside Golf</strong> is founder-owned by Olajuwon Ajanaku and Earl Cooper.
 <strong>No Laying Up</strong> answers to its own audience and nobody else.</p>
 <p>It matters to a buyer in two specific ways. Independents tend to move faster — a
 <strong>Gamut Golf</strong> or a <strong>Dormie Workshop</strong> can decide on a Tuesday and ship
 in a month. And they tend to disappear faster, which is why a good number of the brands here also
 carry the drops-and-vanishes attribute. Buy the thing when you see it.</p>""",
 ),
("tag", "muni-energy", "Muni-Energy Golf Brands",
 "Muni Golf Brands — Public-Course Energy | The Grassy Issue",
 "Twenty-two golf brands that dress for a muni rather than a member-guest — public-course culture, parking-lot beer and no dress code anxiety.",
 """<p>Muni energy is a posture more than a price point. It means the brand is dressing for a
 public course on a Saturday morning: a tee time you booked at 11pm, a bag you carry, a beer in the
 lot afterwards. <strong>Devereux</strong>, <strong>Criquet Shirts</strong> and
 <strong>Huega House</strong> all make clothes you could wear to a private club and would never
 feel obliged to.</p>
 <p>The tell is usually what the brand photographs. Muni-energy brands shoot on municipal tracks,
 in carparks, on ranges with mats — not on manicured par threes at golden hour. Several are
 explicitly built around a course: <strong>No Laying Up</strong> around a travelling public-golf
 audience, <strong>Birds of Condor</strong> around Australian links you can walk on for forty
 dollars. It is the largest overlap group in the Index with post-round-friendly, and for obvious
 reasons.</p>""",
 ),
("tag", "post-round-friendly", "Golf Clothes You Can Wear After the Round",
 "Post-Round Golf Clothing Brands | The Grassy Issue",
 "Nineteen golf brands making clothes that do not announce themselves off the course — wearable at the bar, the airport and everywhere after eighteen.",
 """<p>The test is simple and unforgiving: would you keep it on for dinner. Most golf clothing
 fails it, because the thing that makes a polo read as golf — the logo placement, the sheen of the
 fabric, the cut through the shoulder — is exactly the thing that makes it read as golf in a
 restaurant.</p>
 <p>The brands here pass for different reasons. <strong>Aimé Leon Dore</strong> and
 <strong>Carhartt WIP</strong> pass because they are not golf companies and never were.
 <strong>Gramicci</strong> passes because a climbing pant from 1982 was always going to work
 anywhere. <strong>Casualist</strong> and <strong>Criquet</strong> pass because they built to the
 test deliberately, in fabrics and cuts borrowed from menswear rather than from performance
 sportswear. It is the shelf to shop if you travel to golf rather than living at a club.</p>""",
 ),
("tag", "collab-machine", "Golf's Collaboration Machines",
 "Golf Collaboration Brands — Collab Machines | The Grassy Issue",
 "Fourteen golf brands that build through partnership — the labels whose best work usually arrives with somebody else's name on it too.",
 """<p>Some brands express themselves best in their own range. These fourteen express themselves
 best in somebody else's. <strong>MacKenzie Golf Bags</strong> has become a canvas the rest of golf
 paints on. <strong>BEAMS Golf</strong> runs a collaboration calendar dense enough to be its own
 release schedule. <strong>Aimé Leon Dore</strong> turned a FootJoy into a cultural object.</p>
 <p>The practical thing to understand about this group is timing. Collaboration product is made
 once, in a quantity set months earlier, and the restock never comes — <strong>Sentinel</strong>,
 <strong>Siegelman Stable</strong> and <strong>Sugarloaf Social Club</strong> all operate that way.
 If you are tracking a brand here, you are really tracking its announcement channel.</p>""",
 ),
("tag", "quiet-luxury", "Quiet Luxury Golf Brands",
 "Quiet Luxury Golf Brands — Understated | The Grassy Issue",
 "Thirteen golf brands working in restraint — no visible branding, considered fabric and cuts that say nothing at all across a car park.",
 """<p>Quiet is harder than loud, because there is nowhere to hide. Strip the logo and the graphic
 and what is left is fabric, cut and finish, which are the expensive parts. That is why this is the
 smallest of the major groups in the Index and why the price floor across it is the highest.</p>
 <p><strong>Manors Golf</strong> made its name rejecting technical golf aesthetics outright.
 <strong>Quiet Golf</strong> put the thesis in the name. <strong>A.P.C. Golf</strong> arrived from
 Paris ready-to-wear with the restraint already built in, and <strong>MacKenzie</strong> and
 <strong>Dormie Workshop</strong> apply the same logic to leather and canvas rather than cloth. The
 shared quality is that none of them will tell you across a fairway who made the thing you are
 wearing.</p>""",
 ),
("tag", "gorpcore", "Gorpcore Golf Brands",
 "Gorpcore Golf Brands — Outdoor Crossover | The Grassy Issue",
 "Ten golf brands borrowing from climbing, camping and trail kit — what the materials actually mean, the two routes in, and four pieces from each brand.",
 """<p>One of the smaller groups in the Index and the one moving fastest. Gorpcore in golf means the
 construction language of the outdoors — ripstop, Dyneema, welded seams, webbing, fleece, bucket
 hats — arriving in a game that spent thirty years dressing like an office and calling it
 performance.</p>
 <p>Ten brands, reached by two different routes. <strong>Gramicci</strong> and
 <strong>Carhartt WIP</strong> came from genuine outdoor and workwear lineages and were adopted by
 golfers rather than aimed at them. <strong>Sentinel Golf</strong>, <strong>Sounder</strong>,
 <strong>Left of Field Golf</strong>, <strong>Sunday Golf</strong>, <strong>Ghost Golf</strong>,
 <strong>Agronomy Workshop</strong> and <strong>Odd Ritual</strong> went the other way, building
 golf product out of outdoor materials on purpose. <strong>Realtree</strong> sits between the two,
 licensing a camouflage pattern rather than making clothing at all. If you walk your rounds and
 carry, this is the shelf designed for you rather than adapted to you.</p>""",
 ),
("tag", "range-rat", "Range-Rat Golf Brands",
 "Range Practice Gear Brands | The Grassy Issue",
 "Five golf brands built for the people who are at the range more than the first tee — grips, shafts, carts and the unglamorous end of the bag.",
 """<p>Nobody photographs a grip. That is roughly the point of this group: five brands operating in
 the parts of the bag that only matter to people who are there every week.
 <strong>Rosemark</strong> and <strong>Stick Grips</strong> make the one component you touch on
 every single shot. <strong>Garsen</strong> reshapes the putter grip around what the hands actually
 do. <strong>Takomo</strong> sells irons direct so the money goes into the head rather than the
 distribution. <strong>Bag Boy</strong> has been making the thing that carries all of it since
 1946.</p>
 <p>It is the least fashionable shelf in the Index and probably the one with the highest ratio of
 spend to strokes gained.</p>""",
 ),
("tag", "course-merch", "Course Merch and Club Shop Brands",
 "Golf Course Merch Brands | The Grassy Issue",
 "Four brands working the pro shop end of golf — course maps, club towels, and the merchandise a place sells to the people who love it.",
 """<p>Course merch is its own economy, and it runs on attachment rather than performance. Nobody
 buys a towel with a club crest because it dries better. They buy it because they played there, or
 want to, or want it known that they did.</p>
 <p><strong>Devant Sport Towels</strong> has been supplying that economy for decades.
 <strong>Ally Aiken</strong> paints the course itself, one commission at a time.
 <strong>Random Golf Club</strong> and <strong>Sugarloaf Social Club</strong> invert the model —
 building the community first and letting the merchandise follow it, which is why their drops sell
 out to people who have never been anywhere near a specific clubhouse.</p>""",
 ),
("tag", "member-guest", "Member-Guest Golf Brands",
 "Member-Guest Golf Brands — Club Dress Code | The Grassy Issue",
 "Four golf brands cut for the private-club end of the game — clothing and shoes that clear any dress code without looking like they tried.",
 """<p>The narrowest shelf in the Index, and the one with the clearest brief: clothing that will not
 be questioned at the door. <strong>Peter Millar</strong> is the default answer across most of
 American private golf. <strong>Duca del Cosma</strong> and <strong>Royal Albartross</strong> make
 the shoes, from opposite ends of Europe and with opposite ideas about how visible a golf shoe
 should be. <strong>Manors</strong> sits here and in quiet luxury at once, which is the most
 accurate thing anyone can say about Manors.</p>
 <p>One caveat: a dress code is a local document, not a national one. Everything here clears the
 common ones, but the club with the collar rule is the club with the collar rule.</p>""",
 ),
("tag", "dad-golf", "Dad Golf Brands",
 "Dad Golf Brands — Unbothered Classics | The Grassy Issue",
 "Two golf brands making the genuinely unbothered thing — soft collars, honest colours and not one trend in sight.",
 """<p>Two brands, and both earn it honestly. <strong>Criquet Shirts</strong> built a business in
 Austin on a soft-collar players shirt that looks like something found in a good closet from 1978,
 and has resisted every opportunity to make it technical. <strong>Rouqe Golf</strong> works the
 same register from a different starting point.</p>
 <p>The category is small because most brands that court this look are performing it. Dad golf as a
 real position means declining the trend rather than styling it, which is commercially harder than
 it sounds and leaves very few companies standing in it.</p>""",
 ),
("attr", "new-to-index", "New to the Brand Index",
 "New Golf Brands — Recently Added | The Grassy Issue",
 "Fifty-two golf brands added to the Brand Index most recently — the newest entries, from established houses to first drops.",
 """<p>The most recently added entries in the Index, and the fastest-moving page on this part of the
 site. New here means new to us rather than new to golf — <strong>Carhartt WIP</strong> and
 <strong>Bag Boy</strong> both predate most of the Index by decades and were added because a
 specific piece of coverage finally warranted a page.</p>
 <p>Genuinely new arrivals sit alongside them: <strong>Après Golf</strong>,
 <strong>Bluegrass Fairway</strong>, <strong>Beavertail Golf Co.</strong> and
 <strong>Clutch Golf Company</strong> are small enough that a single drop can sell through in a
 week. If you check one taxonomy page periodically, this is the one that will have changed.</p>""",
 ),
("attr", "women-founded", "Women-Founded Golf Brands",
 "Women-Founded Golf Brands | The Grassy Issue",
 "Nineteen golf brands founded or co-founded by women — headcovers, apparel, shoes and accessories across the whole Brand Index.",
 """<p>Nineteen brands in the Index were founded or co-founded by women, and they are spread across
 every category rather than concentrated in apparel. <strong>Daphne's Headcovers</strong> and
 <strong>Jan Craig</strong> are among the oldest names in the whole Index.
 <strong>Foray Golf</strong> and <strong>Bunker Mentality</strong> work in clothing.
 <strong>Duca del Cosma</strong> makes shoes; <strong>ORKAI</strong> and
 <strong>Inside Story Socks</strong> work the accessory end.</p>
 <p>We tag this because it is a fact about who built the company, checkable against the company's
 own record, and because it is a question readers ask us directly. It is not a claim about the
 product, which is why brands here also carry whatever taste tags actually describe what they
 make.</p>""",
 ),
("attr", "heritage", "Heritage Golf Brands",
 "Heritage Golf Brands — The Long-Running Names | The Grassy Issue",
 "Fourteen golf and adjacent brands with real longevity behind them — companies whose archive is older than most of the Brand Index.",
 """<p>Heritage is a word golf marketing has beaten senseless, so the bar here is a date you can
 check. <strong>Bag Boy</strong> has made push carts since 1946. <strong>Jan Craig</strong> has been
 knitting headcovers since 1961. <strong>Carhartt</strong> goes back to 1889 and
 <strong>Gramicci</strong> to a Yosemite climbing pant in 1982.</p>
 <p>What the tag is useful for is separating brands with an actual archive from brands with an
 aesthetic borrowed from one. Both can make good product. Only one of them can reissue something.
 <strong>MacKenzie</strong>, <strong>Bettinardi</strong>, <strong>Sun Mountain</strong> and
 <strong>Jones Sports Co</strong> all draw on their own back catalogue rather than someone
 else's.</p>""",
 ),
("attr", "tour-proven", "Tour-Proven Golf Brands",
 "Tour-Proven Golf Brands — Played at the Top | The Grassy Issue",
 "Eleven golf brands whose product is in play at tour level — equipment, grips and apparel carried by professionals, not just endorsed.",
 """<p>Eleven brands in the Index have product genuinely in play at tour level, which is a narrower
 claim than an endorsement deal. <strong>PXG</strong> and <strong>PUMA Golf</strong> are there at
 full scale. <strong>Takomo</strong> and <strong>Rosemark</strong> are there in spite of their
 size. <strong>Seamus</strong> and <strong>Jan Craig</strong> are there on the headcover, which is
 the one piece of equipment a player chooses entirely for themselves.</p>
 <p>The tag is descriptive rather than a recommendation. Tour usage tells you a product survives
 the most scrutinised environment in the sport; it tells you nothing about whether it suits a
 fourteen handicap, and in several cases it actively does not.</p>""",
 ),
("attr", "drops-and-vanishes", "Golf Brands That Drop and Vanish",
 "Limited Drop Golf Brands | The Grassy Issue",
 "Eleven golf brands that release in small runs and do not restock — if you are waiting for it to come back, it is not coming back.",
 """<p>Eleven brands in the Index operate on a drop model with no restock behind it. The run is
 made, it sells or it does not, and the next thing is a different thing.
 <strong>Sentinel Golf</strong>, <strong>Mogshade</strong>, <strong>Radry</strong> and
 <strong>Gamut Golf</strong> all work this way by design rather than by supply-chain accident.</p>
 <p>This is the single most actionable tag in the Index, and the advice attached to it is blunt:
 the decision is at announcement, not at payday. <strong>Sugarloaf Social Club</strong> and
 <strong>Gumtree Golf &amp; Nature Club</strong> routinely sell through in hours. If you are
 tracking anything here, track the announcement channel rather than the shop.</p>""",
 ),
]

TAGL = {"design-nerd": "Design nerd", "made-by-hand": "Made by hand", "loud-on-purpose": "Loud on purpose",
        "independent": "Independent", "muni-energy": "Muni energy", "post-round-friendly": "Post-round friendly",
        "collab-machine": "Collab machine", "quiet-luxury": "Quiet", "gorpcore": "Gorpcore",
        "range-rat": "Range rat", "course-merch": "Course merch", "member-guest": "Member-guest",
        "dad-golf": "Dad golf", "new-to-index": "New to the Index", "women-founded": "Women-founded",
        "heritage": "Heritage", "tour-proven": "Tour-proven", "drops-and-vanishes": "Drops and vanishes"}


def members(kind, slug):
    if kind == "tag":
        return [b for b in brands if slug in tags_of(b)]
    return [b for b in brands if slug in b.get("attrs", [])]


# --------------------------------------------------- cards lifted from /brands
CARDS = {}
for m in re.finditer(r'<a class="bc" href="/brands/([a-z0-9-]+)".*?</a>', index_html, re.S):
    CARDS[m.group(1)] = m.group(0)
if len(CARDS) < len(brands):
    raise SystemExit(f"only {len(CARDS)} .bc cards found in brands/index.html for {len(brands)} brands "
                     f"— run build-brand-index.py first")

# ------------------------------------------------------- chrome + the bx style
HEAD_END = chrome_src.find("</head>")
BODY_START = chrome_src.find("<body>")
NAV_END = chrome_src.find("<header class=\"bp-head\">")
FOOT_START = chrome_src.find("<footer")
if min(HEAD_END, BODY_START, NAV_END, FOOT_START) < 0:
    raise SystemExit("could not find the chrome landmarks in brands/gramicci.html")
HEAD = chrome_src[:HEAD_END]
NAV = chrome_src[BODY_START + len("<body>"):NAV_END]
TAIL = chrome_src[FOOT_START:]

# The Index's own stylesheet, so a card looks identical on both surfaces. Every
# rule in it is scoped "#bx ...", including the custom-property block, so the
# whole sheet is re-scoped to this page's wrapper rather than copied blind — a
# copied "#bx .bc{}" would apply to nothing here and the cards would render raw.
_bx = [m.group(0) for m in re.finditer(r'<style[^>]*id="bx-css"[^>]*>.*?</style>', index_html, re.S)]
if not _bx or ".bc{" not in _bx[0]:
    raise SystemExit("could not lift the #bx-css block out of brands/index.html")
BXCSS = _bx[0].replace('id="bx-css"', 'id="tx-css"').replace("#bx{", "#tx{").replace("#bx ", "#tx ")
if "#tx .bc{" not in BXCSS:
    raise SystemExit("re-scoping #bx -> #tx did not take; the card rules would not apply")

EXTRA = """<style>
#tx{max-width:1180px;margin:0 auto;padding:44px 22px 70px;font-family:var(--bx-sans,inherit)}
#tx .tx-crumb{font-family:var(--bx-mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--bx-ink60);margin-bottom:18px}
#tx .tx-crumb a{color:inherit;text-decoration:none;border-bottom:1px solid currentColor}
#tx h1{font-size:clamp(30px,4.4vw,52px);line-height:1.06;letter-spacing:-.02em;margin:0 0 10px;font-weight:700}
#tx .tx-count{font-family:var(--bx-mono);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--bx-ink60);margin-bottom:24px}
#tx .tx-sec{max-width:72ch;margin:42px auto 0}
#tx .tx-sec h2{font-family:var(--bx-serif,Georgia,serif);font-size:24px;letter-spacing:-.01em;margin:0 0 14px}
#tx .tx-sec p{font-size:17px;line-height:1.65;margin:0 0 15px}
#tx .tx-sec-lead{opacity:.8}
#tx .tx-gloss{margin:22px 0 0;padding:0}
#tx .tx-gloss dt{font-family:var(--bx-mono,ui-monospace,monospace);font-size:10.5px;letter-spacing:.14em;
 text-transform:uppercase;margin:20px 0 6px;padding-top:14px;border-top:1px solid var(--bx-rule,#e6e4df)}
#tx .tx-gloss dd{margin:0;font-size:16.5px;line-height:1.62}
#tx section#picks{max-width:1200px}
#tx .tx-picks{margin:26px auto 0;display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:28px}
#tx .brand-card .product-body h3 a{color:inherit;text-decoration:none;border-bottom:1px solid rgba(20,20,20,.25)}
#tx .brand-card .product-body h3 a:hover{border-bottom-color:currentColor}
#tx .tx-lineup{list-style:none;margin:14px 0 0;padding:0}
#tx .tx-lineup li{display:flex;justify-content:space-between;align-items:baseline;gap:12px;
 padding:7px 0;border-top:1px solid var(--bx-rule,#e6e4df);font-size:13.5px;line-height:1.4}
#tx .tx-lineup li span{flex:1}
#tx .tx-lineup li b{font-family:var(--bx-mono,ui-monospace,monospace);font-size:11.5px;
 letter-spacing:.04em;font-weight:600;white-space:nowrap}
#tx .tx-more{display:inline-block;margin-top:13px;font-family:var(--bx-mono,ui-monospace,monospace);
 font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;color:inherit;
 border-bottom:1px solid currentColor;padding-bottom:2px;opacity:.7}
#tx .tx-more:hover{opacity:1}
#tx .product-card{border:1px solid var(--bx-rule,#e6e4df);background:var(--bx-paper,#F4F1EA)}
#tx .product-body{padding:15px 16px 18px}
#tx .product-body h3{font-family:var(--bx-serif,Georgia,serif);font-size:18px;margin:4px 0 6px;letter-spacing:-.01em}
#tx .product-body p{font-size:14.5px;line-height:1.55;margin:9px 0 0}
#tx .cat-kicker{font-family:var(--bx-mono,ui-monospace,monospace);font-size:9.5px;letter-spacing:.15em;text-transform:uppercase;opacity:.6}
#tx .tx-price{font-family:var(--bx-mono,ui-monospace,monospace);font-size:12px;letter-spacing:.06em}
#tx .tx-faq{max-width:72ch;margin:46px auto 0}
#tx .tx-faq h2{font-family:var(--bx-serif,Georgia,serif);font-size:24px;margin:0 0 6px}
#tx .tx-faq details{border-top:1px solid var(--bx-rule,#e6e4df);padding:14px 0}
#tx .tx-faq summary{cursor:pointer;font-weight:600;font-size:16.5px;list-style:none}
#tx .tx-faq summary::-webkit-details-marker{display:none}
#tx .tx-faq summary::after{content:"+";float:right;opacity:.5}
#tx .tx-faq details[open] summary::after{content:"\2212"}
#tx .tx-faq p{font-size:16.5px;line-height:1.62;margin:10px 0 0}
.product-gallery{position:relative;aspect-ratio:4/5;overflow:hidden;background:#e8e5dc}
.pg-track{display:flex;height:100%;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;-ms-overflow-style:none;scroll-behavior:smooth}
.pg-track::-webkit-scrollbar{display:none}
.pg-frame{flex:0 0 100%;height:100%;scroll-snap-align:center}
.pg-frame img{width:100%;height:100%;object-fit:cover;display:block}
.pg-arw{position:absolute;top:50%;transform:translateY(-50%);width:30px;height:30px;border:.5px solid var(--bx-ink,#141414);background:var(--bx-paper,#F4F1EA);color:var(--bx-ink,#141414);font-size:17px;line-height:1;cursor:pointer;opacity:0;transition:opacity .18s;z-index:2;padding:0}
.pg-arw.prev{left:8px}.pg-arw.next{right:8px}
.product-card:hover .pg-arw{opacity:.9}
.pg-arw:hover{opacity:1}
.pg-count{position:absolute;top:8px;right:8px;font-family:var(--bx-mono,ui-monospace,monospace);font-size:9px;letter-spacing:.1em;background:var(--bx-paper,#F4F1EA);border:.5px solid var(--bx-ink,#141414);padding:2px 6px;z-index:2}
.pg-dots{position:absolute;bottom:8px;left:0;right:0;display:flex;justify-content:center;gap:5px;z-index:2}
.pg-dot{width:6px;height:6px;border-radius:50%;border:.5px solid var(--bx-ink,#141414);background:var(--bx-paper,#F4F1EA);padding:0;cursor:pointer;opacity:.55;transition:opacity .15s}
.pg-dot.on{background:var(--bx-ink,#141414);opacity:1}
@media(max-width:900px){.pg-arw{opacity:.85}}
#tx .tx-intro{max-width:62ch;font-size:17px;line-height:1.62}
#tx .tx-intro p{margin:0 0 15px}
#tx .tx-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(232px,1fr));gap:34px 26px;margin:42px 0 0}
#tx .tx-also{margin:58px 0 0;padding:26px 0 0;border-top:1px solid var(--bx-rule,#e6e4df)}
#tx .tx-also h2{font-size:15px;letter-spacing:.02em;margin:0 0 14px;font-weight:700}
#tx .tx-also-list{display:flex;flex-wrap:wrap;gap:8px}
#tx .tx-also-list a{font-family:var(--bx-mono);font-size:10px;letter-spacing:.13em;text-transform:uppercase;
 padding:8px 11px;border:1px solid var(--bx-rule,#e6e4df);text-decoration:none;color:inherit}
#tx .tx-also-list a:hover{background:var(--bx-ink,#1a1a1a);color:var(--bx-paper,#fff)}
#tx .tx-back{margin-top:26px;font-family:var(--bx-mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase}
#tx .tx-back a{color:inherit}
</style>"""


GALJS = """<script>
(function(){
  document.querySelectorAll('.product-gallery').forEach(function(g){
    var track=g.querySelector('.pg-track'),
        dots=[].slice.call(g.querySelectorAll('.pg-dot')),
        count=g.querySelector('.pg-count'),
        n=parseInt(g.parentNode.getAttribute('data-frames'),10)||1;
    if(n<2) return;
    function idx(){ return Math.round(track.scrollLeft/track.clientWidth); }
    function go(i){ track.scrollTo({left:track.clientWidth*Math.max(0,Math.min(n-1,i)),behavior:'smooth'}); }
    function sync(){ var i=idx();
      dots.forEach(function(d,j){ d.classList.toggle('on',j===i); });
      if(count) count.textContent=(i+1)+'/'+n; }
    track.addEventListener('scroll',function(){ window.requestAnimationFrame(sync); },{passive:true});
    dots.forEach(function(d){ d.addEventListener('click',function(e){ e.preventDefault(); go(+d.dataset.i); }); });
    var p=g.querySelector('.pg-arw.prev'), nx=g.querySelector('.pg-arw.next');
    if(p) p.addEventListener('click',function(e){ e.preventDefault(); go(idx()-1); });
    if(nx) nx.addEventListener('click',function(e){ e.preventDefault(); go(idx()+1); });
  });
})();
</script>"""


def esc(s):
    return html.escape(s, quote=True)


def page(kind, slug, h1, title, desc, intro, notes):
    ms = members(kind, slug)
    url = f"/brands/{kind}/{slug}"
    others = [(k, s, TAGL[s], len(members(k, s))) for k, s, *_ in TAX if s != slug]
    others.sort(key=lambda o: -o[3])
    chips = "".join(
        f'<a href="/brands/{k}/{s}">{esc(lab)} <span class="dim">{n}</span></a>' for k, s, lab, n in others)
    cards = "\n".join(CARDS[b["slug"]] for b in ms)

    schema = {"@context": "https://schema.org", "@type": "CollectionPage",
              "name": h1, "description": desc,
              "url": f"https://thegrassyissue.com{url}",
              "isPartOf": {"@type": "WebSite", "name": "The Grassy Issue",
                           "url": "https://thegrassyissue.com"},
              "breadcrumb": {"@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
                  {"@type": "ListItem", "position": 2, "name": "The Brand Index",
                   "item": "https://thegrassyissue.com/brands/"},
                  {"@type": "ListItem", "position": 3, "name": h1}]},
              "mainEntity": {"@type": "ItemList", "numberOfItems": len(ms), "itemListElement": [
                  {"@type": "ListItem", "position": i + 1, "name": b["name"],
                   "url": f"https://thegrassyissue.com/brands/{b['slug']}"} for i, b in enumerate(ms)]}}

    # A built-out page (tax_bodies.BODIES) gets explainer sections between the intro
    # and the grid, product picks after it, and an FAQ. A slug with no entry renders
    # exactly as it always did, so this cannot disturb the other seventeen pages.
    B = tax_bodies.BODIES.get(slug, {})
    top, bottom, faq = B.get("top", "").strip(), B.get("bottom", "").strip(), B.get("faq", [])
    faq_html = ""
    if faq:
        faq_html = ('<section class="tx-faq"><h2>Questions</h2>'
                    + "".join(f"<details><summary>{esc(q)}</summary><p>{a}</p></details>"
                              for q, a in faq) + "</section>")
        # CollectionPage and FAQPage both describe this URL, so they go in one @graph
        # rather than two competing top-level blocks.
        _cp = dict(schema); _cp.pop("@context", None)
        schema = {"@context": "https://schema.org", "@graph": [_cp, {
            "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer",
                                               "text": re.sub(r"\s+", " ",
                                                              re.sub(r"<[^>]+>", "", a)).strip()}}
                           for q, a in faq]}]}

    head = HEAD
    head = re.sub(r"<title>[^<]*</title>", f"<title>{title}</title>", head)
    for k, v in [("description", desc), ("og:title", title.split(" | ")[0].split(" — ")[0]),
                 ("og:description", desc)]:
        head = re.sub(rf'(<meta (?:name|property)="{re.escape(k)}" content=")[^"]*(")',
                      lambda m, v=v: m.group(1) + esc(v) + m.group(2), head)
    for k, v in [("twitter:title", title.split(" | ")[0].split(" — ")[0]), ("twitter:description", desc)]:
        head = re.sub(rf'(<meta name="{k}" content=")[^"]*(")',
                      lambda m, v=v: m.group(1) + esc(v) + m.group(2), head)
    for pat, val in [(r'(<link rel="canonical" href=")[^"]*(")', f"https://thegrassyissue.com{url}"),
                     (r'(<meta property="og:url" content=")[^"]*(")', f"https://thegrassyissue.com{url}")]:
        head = re.sub(pat, lambda m, v=val: m.group(1) + v + m.group(2), head)
    head = re.sub(r'<script type="application/ld\+json">.*?</script>',
                  lambda m: '<script type="application/ld+json">' + json.dumps(schema) + "</script>",
                  head, count=1, flags=re.S)
    if "application/ld+json" not in head:
        head += '\n<script type="application/ld+json">' + json.dumps(schema) + "</script>"
    head += "\n" + BXCSS + "\n" + EXTRA

    body = f"""<main id="tx">
  <div class="tx-crumb"><a href="/">Feed</a> &nbsp;/&nbsp; <a href="/brands/">The Brand Index</a> &nbsp;/&nbsp; {esc(h1)}</div>
  <h1>{esc(h1)}</h1>
  <div class="tx-count">{len(ms)} brands in the Index</div>
  <div class="tx-intro">
{intro.strip()}
  </div>
{top}
  <div class="tx-grid">
{cards}
  </div>
{bottom}
{faq_html}
  <div class="tx-also">
    <h2>Other ways into the Index</h2>
    <div class="tx-also-list">{chips}</div>
    <div class="tx-back"><a href="/brands/">&larr; All {len(brands)} brands</a></div>
  </div>
</main>

"""
    # SHARE CARDS. The head was lifted from a brand page, which carries og: tags
    # but no twitter: ones, so these pages had nothing for a Twitter/X or Slack
    # unfurl to read and no image at all. Twitter falls back to og:, but og:image
    # was never set either — so a shared link rendered as a bare grey box.
    _picks = re.search(r'<section class="tx-sec" id="picks">.*?</section>', body, re.S)
    first_img = (re.search(r'<img[^>]+src="(/images/[^"]+)"', _picks.group(0)) if _picks else None) \
        or re.search(r'<img[^>]+src="(/images/[^"]+)"', body)
    extra = [f'<meta name="twitter:card" content="summary_large_image">',
             f'<meta name="twitter:title" content="{esc(title.split(" | ")[0].split(" — ")[0])}">',
             f'<meta name="twitter:description" content="{esc(desc)}">']
    if first_img:
        img = "https://thegrassyissue.com" + first_img.group(1)
        extra += [f'<meta property="og:image" content="{img}">',
                  f'<meta name="twitter:image" content="{img}">']
    head2 = head + "\n" + "\n".join(extra)

    tail = TAIL.replace("</body>", GALJS + "\n</body>") if "product-gallery" in body else TAIL
    return head2 + "\n</head>\n<body>" + NAV + body + tail, ms


# ----------------------------------------------------------------------- guards
apply_ = "--apply" in sys.argv
notes, written = [], []
seen_slugs = set()

for kind, slug, h1, title, desc, intro in TAX:
    ms = members(kind, slug)
    if not ms:
        raise SystemExit(f"{kind}/{slug} matches no brands — check brands.json")
    if len(ms) < 2:
        raise SystemExit(f"{kind}/{slug} has {len(ms)} brand — a one-item page is a thin page")
    if slug in seen_slugs:
        raise SystemExit(f"duplicate taxonomy slug {slug}")
    seen_slugs.add(slug)
    if len(title) > 65:
        raise SystemExit(f"{slug}: title is {len(title)} chars, must be 65 or under\n  {title}")
    if not (110 <= len(desc) <= 165):
        raise SystemExit(f"{slug}: description is {len(desc)} chars, must be 110-165\n  {desc}")
    plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", intro)).strip()
    if re.search(r"\bworth\b", plain, re.I):
        raise SystemExit(f"{slug}: BANNED WORD 'worth' in the intro copy")
    if len(plain.split()) < 90:
        raise SystemExit(f"{slug}: intro is {len(plain.split())} words — under the 90-word floor. "
                         f"Eighteen thin pages would make the audit finding worse, not better.")
    # the copy must name at least two brands that are actually ON this page
    named = sum(1 for b in ms if b["name"] in plain)
    if named < 2:
        raise SystemExit(f"{slug}: intro names {named} brand(s) from its own list, needs 2+ — "
                         f"generic copy is what we are trying to stop shipping")
    # the printed count word must match the computed count
    WORDS = {2: "two", 4: "four", 5: "five", 7: "seven", 10: "ten", 11: "eleven", 13: "thirteen", 14: "fourteen",
             19: "nineteen", 22: "twenty-two", 25: "twenty-five", 33: "thirty-three", 37: "thirty-seven",
             52: "fifty-two"}
    w = WORDS.get(len(ms))
    if w and w not in (plain + " " + desc).lower():
        raise SystemExit(f"{slug}: {len(ms)} brands but the copy does not say '{w}' — counts must "
                         f"match the data, and the data moved")

    out, ms = page(kind, slug, h1, title, desc, intro, notes)
    if out.count("<h1") != 1:
        raise SystemExit(f"{slug}: expected exactly one h1, found {out.count('<h1')}")
    miss = [b["slug"] for b in ms if f'href="/brands/{b["slug"]}"' not in out]
    if miss:
        raise SystemExit(f"{slug}: members missing from the rendered grid: {miss}")
    d = os.path.join(ROOT, "brands", kind)
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, slug + ".html")
    if apply_:
        open(p, "w", encoding="utf-8").write(out)
    written.append((f"/brands/{kind}/{slug}", len(ms), len(plain.split())))

# every brand must now be reachable from at least one taxonomy page
covered = {b["slug"] for kind, slug, *_ in TAX for b in members(kind, slug)}
orphans = [b["slug"] for b in brands if b["slug"] not in covered]

print(("wrote" if apply_ else "DRY RUN") + f" {len(written)} taxonomy pages")
for u, n, w in sorted(written, key=lambda x: -x[1]):
    print(f"  {u:38} {n:>3} brands  {w:>3}w intro")
inb = collections.Counter()
for kind, slug, *_ in TAX:
    for b in members(kind, slug):
        inb[b["slug"]] += 1
print(f"\ninbound taxonomy links per brand: min {min(inb.values())}, "
      f"median {sorted(inb.values())[len(inb)//2]}, max {max(inb.values())}")
print(f"brands reachable from a taxonomy page: {len(covered)} of {len(brands)}")
if orphans:
    print(f"  !! {len(orphans)} brand(s) on NO taxonomy page (they keep their single inbound link): "
          + ", ".join(orphans))
if any("loud" in b.get("tags", []) for b in brands):
    print("\n  !! brands.json still tags Swag Golf 'loud' rather than 'loud-on-purpose'. "
          "ALIAS handles it at build time; fix the data and delete ALIAS when convenient.")
if not apply_:
    print("\npass --apply to write")
