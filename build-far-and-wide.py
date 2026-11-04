"""build-far-and-wide.py — "Far and Wide: golf brands from across the globe", 4 November 2026.
Cloned from build-collabs-nov.py. Lenny: "Let's do a post; Far and Wide, golf brands from across the globe. I want options
from unique places; South Africa- Odd Ritual, Portugal- Mogshade, Japan-, Sweden-, Canada-. Find the missing places and let's
build a cool post that also has a course recomendation for each country. Something that is distinctly that countries. I like
Banff for Canada for instance." Picks (Lenny, 4 Nov): Japan ANTi COUNTRY CLUB TOKYO, Sweden Late Nine, Canada Rouqe; 6 per brand.
FACTS: product pages (each store's own currency as presented to a US visitor); courses from the resorts' own pages and
reporting checked 4 Nov 2026. Photos: brands' own; course photos credited (Wikimedia Commons licences / Björkliden).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"
TITLE = "Far and Wide: Five Independent Golf Brands From Around the World, and Where to Play in Their Backyard"
DESC = ("Independent golf is community first. Five brands from five countries (Odd Ritual, Mogshade, ANTi COUNTRY CLUB TOKYO, "
        "Late Nine and Rouqe), their lookbooks, 30 pieces, and the course to play in each brand's backyard.")
H1 = "Far and Wide: Golf Brands From Around the World, and Where to Play in Their Backyard"
BC = "Far and Wide"
SLUG = "far-and-wide-golf-brands-around-the-world"
IMG = "/images/far-wide"
SHOP = ""
U = lambda d, h: f"https://{d}/products/{h}"
OR, MG, AC, LN, RQ = "oddritualgolf.com", "mogshadegolf.com", "anticountryclubtokyo.com", "late-nine.com", "rouqegolf.com"
P = {
 "orjk": ("Odd Ritual", "The Caddie Jacket, Navy", "1,900 ZAR (~$115)", U(OR,"the-caddie-jacket-navy"),
   "230gsm cotton twill with a washed cotton lining, a YKK zip and quiet embroidered branding. An everyday jacket that happens to suit a cold first tee."),
 "ortr": ("Odd Ritual", "Pleated Daily Trouser, Black", "990 ZAR (~$60)", U(OR,"pleated-daily-trouser-black"),
   "Soft 235gsm cotton twill, a loose fit with a slight carrot leg, front pleats and an elasticated back waist."),
 "orpo": ("Odd Ritual", "1990s Heritage Polo", "950 ZAR (~$58)", U(OR,"1990s-heritage-polo"),
   "A heavy 200gsm piqu&eacute; with a contrast nylon collar and cuffs, cut oversized with a dropped shoulder. Period cut, current fabric."),
 "orcr": ("Odd Ritual", "ORGC Traditions Crewneck, Burgundy", "1,400 ZAR (~$85)", U(OR,"orgc-traditions-crewneck-burgundy"),
   "Heavyweight cotton fleece with a vintage pigment wash, so it looks broken in from the first wear."),
 "orcp": ("Odd Ritual", "Heritage Rope Cap, Khaki", "550 ZAR (~$33)", U(OR,"heritage-rope-cap-khaki"),
   "An unstructured five-panel with the heritage serif logo in white and brown, and a white rope across the brim."),
 "orcl": ("Odd Ritual", "Classic Polo, Black", "550 ZAR (~$33)", U(OR,"odd-ritual-classic-polo-black"),
   "The on-course piece: lightweight performance polyester, a structured fit and a modern collar."),
 "mgaz": ("Mogshade", "Azulejo Brown Headcover", "$104", U(MG,"azulejo-brown-black-headcover"),
   "The pattern takes its geometry from the hand-painted azulejo tiles on Lisbon&rsquo;s buildings. Woven, not printed."),
 "mgsea": ("Mogshade", "Azulejo Sea &amp; Gray Headcover", "$104", U(MG,"azulejo-emerald-gray-headcover"),
   "The same tile pattern in sea green and gray, from rescued fabric woven in the Serra da Estrela, with a fleece lining."),
 "mgtile": ("Mogshade", "Tiles Orange Headcover", "$104", U(MG,"tiles-orange-headcover"),
   "Part of the Re.Weave line: leftover high-quality fabric from mills in the mountains, turned into a driver cover."),
 "mgcas": ("Mogshade", "Castelo Headcover", "$153", U(MG,"castelo-headcover"),
   "Made with Fabricaal from merino textiles handwoven by artisans on manual wooden looms. The most special cover Mogshade makes."),
 "mgchu": ("Mogshade", "Churra Risca Headcover", "$116", U(MG,"churra-risca-headcover"),
   "Wool from Churra sheep, a breed native to the Serra da Estrela that is now protected because it was close to dying out."),
 "mgcase": ("Mogshade", "Risca Light Course Case", "$141", U(MG,"risca-light-course-case"),
   "A small wool case with a pocket for ball markers and loops for a few tees. The easy gift in this post."),
 "acrg": ("ANTi COUNTRY CLUB TOKYO", "Rugby Knit, Navy", "$248", U(AC,"anti-country-club-rugby-knit-navy"),
   "100% Japanese wool, with the club&rsquo;s college-style initials on the chest."),
 "acvar": ("ANTi COUNTRY CLUB TOKYO", "Varsity Jacket, Brown", "$428", U(AC,"anti-country-club-varsity-jacket-brown"),
   "A wool body with real leather sleeves and the club crest on the back. The statement piece."),
 "acvest": ("ANTi COUNTRY CLUB TOKYO", "Down Vest, Black Check", "$328", U(AC,"anti-country-club-down-vest-black-check"),
   "A wool check outside and more than 80% feathers inside, with a nylon hood. Made for cold mornings."),
 "accord": ("ANTi COUNTRY CLUB TOKYO", "Corduroy Pants, Khaki", "$128.76", U(AC,"anti-country-club-corduroy-pants-khaki"),
   "Thick 100% cotton corduroy in a classic cut. The store converts from yen, hence the cents."),
 "acbkt": ("ANTi COUNTRY CLUB TOKYO", "Wool Bucket Hat", "$64.38", U(AC,"anti-country-club-wool-bucket-hat"),
   "100% wool check with an adjuster inside, so one size fits most heads."),
 "achood": ("ANTi COUNTRY CLUB TOKYO", "College Logo Hoodie, Brown", "$122.91", U(AC,"anti-country-club-college-logo-hoodie-brown"),
   "The &ldquo;ANTi Country Club&rdquo; crest in collegiate type. The easiest way to wear the joke."),
 "lncab": ("Late Nine", "Cable Knit Polo, Burgundy", "2,950 SEK (~$298)", U(LN,"cable-knit-polo-burgundy"),
   "Ultra-fine merino from the first shearing, lightly brushed. Soft, warm and breathable."),
 "lnsl": ("Late Nine", "Double Pleat Slacks, Dark Brown", "3,200 SEK (~$323)", U(LN,"double-pleat-slacks-dark-brown"),
   "Italian four-season wool, a full straight leg and outward-facing double pleats. The piece the brand is built on."),
 "lnins": ("Late Nine", "Instructors Jacket, Navy", "4,350 SEK (~$439)", U(LN,"instructors-jacket-cotton-navy"),
   "Modeled on the blousons golf instructors wore through the &rsquo;90s, with a rounded stand-up collar and a two-way zip."),
 "lnvest": ("Late Nine", "Ribbed Knit Vest, Sage", "2,450 SEK (~$247)", U(LN,"ribbed-vest-sage"),
   "First-shearing merino in a light rib. Warmth without bulk over a polo."),
 "lnqz": ("Late Nine", "Quarter Zip Windbreaker, Navy", "3,750 SEK (~$379)", U(LN,"quarter-zip-windbreaker-navy"),
   "A full collar, a buttoned placket over the zip, dark metal hardware and a drawstring hem."),
 "lnbelt": ("Late Nine", "Loop Belt, Brown Suede", "1,400 SEK (~$141)", U(LN,"loop-belt-brown-suede-silver"),
   "LWG-certified Italian leather and a western-style double loop, from when those belts were a normal sight on the course."),
 "rqstr": ("Rouqe", "Burgundy Striped Polo", "$51", U(RQ,"burgundy-striped-polo"),
   "The retro rugby stripe in four-way stretch with UPF 50+. Restocked after selling out."),
 "rqmock": ("Rouqe", "Brown Mock Neck", "$44", U(RQ,"brown-mock-neck"),
   "The silhouette the whole brand is built on, in lightweight nylon stretch."),
 "rqknit": ("Rouqe", "&ldquo;R&rdquo; Knit Sweater, Beige", "$44", U(RQ,"r-knit-sweater-beige"),
   "A heavyweight merino-blend knit with a big script R, cut cropped. Size up for a standard fit."),
 "rqsw": ("Rouqe", "RQ Sweater", "$29", U(RQ,"rq-sweater"),
   "A retro V-neck in 100% mercerized cotton. The cheapest sweater in this post by a long way."),
 "rqhc": ("Rouqe", "Script Driver Head Cover, Brown", "$25", U(RQ,"script-driver-head-cover-brown"),
   "Leather with a hand-written script embroidery and a soft velvet lining."),
 "rqtwo": ("Rouqe", "Two Tone Polo, Blue", "$51", U(RQ,"two-tone-polo-blue"),
   "Blue body, white sleeves, four-way stretch and UPF 50+. 1974 club pro, current fabric."),
}
# (anchor, country, brand, city, ids, brand paras, course name, course place, course paras, details, image credit)
COUNTRIES = [
 ("south-africa", "South Africa", "Odd Ritual", "Cape Town", ["orjk","ortr","orpo","orcr","orcp","orcl"],
  ["Odd Ritual was born in Cape Town because its founders could not find a local golf brand that spoke to them. The name comes from the small habits every golfer has before a shot: the waggle, the alignment check, the tap on the ball mark. Everything is designed and made in South Africa.",
   "This season leans on workwear: a cotton twill Caddie Jacket, pleated trousers with a carrot leg and a 1990s polo with nylon trim. Prices are in South African rand on the store; the dollar figures here are approximate."],
  "Legend Golf &amp; Safari Resort", "Waterberg, Limpopo",
  ["Legend sits beside the Entabeni Game Reserve in the Waterberg, about three hours from Johannesburg. It reopened in May 2026 after a year-long rebuild, with three courses and the Big Five roaming the wider conservancy.",
   "The reason to go is the Extreme 19th. A helicopter flies you to the top of Hanglip Mountain, and you tee off roughly 400 meters down to a green shaped like the African continent. Nowhere else in golf does a par 3 start with a flight."],
  [("Where", "Waterberg, Limpopo"), ("From", "About 3 hours from Johannesburg"), ("Don&rsquo;t miss", "The Extreme 19th, by helicopter")],
  "Photo: South African Tourism, CC BY 2.0"),
 ("portugal", "Portugal", "Mogshade", "Portugal", ["mgaz","mgsea","mgtile","mgcas","mgchu","mgcase"],
  ["Mogshade makes headcovers and towels in Portugal, to order, on about a three-week lead. The patterns are woven, not printed, and they could only come from one place. The Azulejo covers take their geometry from the hand-painted tiles on Lisbon&rsquo;s buildings.",
   "The materials are local too. The Re.Weave covers use rescued fabric woven in the Serra da Estrela mountains. The Churra covers use wool from a sheep breed native to the same mountains. The Castelo cover is handwoven on wooden looms. The store shows prices in US dollars."],
  "Oitavos Dunes", "Cascais, near Lisbon",
  ["Oitavos Dunes runs through sand dunes and umbrella pines on the coast at Cascais, with the Atlantic on the horizon and the wind off the ocean deciding how it plays. Arthur Hills designed it, and it is the course people mean when they talk about golf near Lisbon.",
   "It is about half an hour from the city, so you can play in the morning and be back for dinner in Alfama. Book ahead and bring a handicap certificate; the club asks for one."],
  [("Where", "Cascais, about 30 minutes from Lisbon"), ("Green fee", "About &euro;115&ndash;&euro;180 (~$131&ndash;$205)"), ("Good to know", "Handicap certificate required")],
  "Photo: R&uacute;disicyon, CC BY-SA 4.0"),
 ("japan", "Japan", "ANTi COUNTRY CLUB TOKYO", "Tokyo", ["acrg","acvar","acvest","accord","acbkt","achood"],
  ["ANTi COUNTRY CLUB TOKYO says it in the name. It takes the old country-club wardrobe (rugby knits, varsity jackets, corduroy, a bucket hat) and makes it feel like something from a Tokyo vintage shop rather than a members&rsquo; lounge.",
   "The fabrics are the real thing: Japanese wool for the rugby knit, a wool body and leather sleeves on the varsity jacket, a down vest with more than 80% feathers. The brand has worked with Metalwood Studio, adidas Golf and Vans. The store shows prices in US dollars, converted from yen."],
  "Kawana Hotel, Fuji Course", "Ito, Izu Peninsula",
  ["Charles Hugh Alison stayed at the Kawana Hotel in 1930 and talked the owner into building a course on the rocky ledge above Sagami Bay. The Fuji Course opened in 1936. On a clear day you can see Oshima Island out to sea and Mount Fuji inland, and in spring the cherry trees bloom between the fairways.",
   "The 15th is the hole people remember, a par 5 with the fairway falling toward the sea. The catch: the Fuji Course is for hotel guests, so you book a room to play it. The Oshima Course next door takes outside visitors."],
  [("Where", "Ito, Shizuoka, about 2 hours from Tokyo"), ("Green fee", "From about &yen;47,800 (~$310) for hotel guests"), ("Good to know", "Stay at the hotel to play the Fuji Course")],
  "Photo: &#27743;&#25144;&#26449;&#12398;&#12392;&#12367;&#12382;&#12358;, CC BY-SA 4.0"),
 ("sweden", "Sweden", "Late Nine", "Stockholm", ["lncab","lnsl","lnins","lnvest","lnqz","lnbelt"],
  ["Late Nine is a Stockholm label built on late-&rsquo;90s tour golf. Co-founder Maxim Lundh grew up copying Sergio Garcia and Jesper Parnevik, and you can see it: pleated slacks, cable knits and the jackets instructors wore on the range.",
   "The materials are a step up from most golf clothing: first-shearing merino for the knits, Italian four-season wool for the slacks and LWG-certified Italian leather for the belt. Prices are in Swedish kronor on the store; the dollar figures are approximate."],
  "Falsterbo Golfklubb", "Sk&aring;ne, southern Sweden",
  ["Most Swedish golf is parkland cut through forest. Falsterbo is the exception: a true links on a flat, sandy spit at the southwest tip of the country, with sea on three sides and a white lighthouse in the middle of the course. The club was founded in 1909, the third oldest in Sweden, and the 18 holes you play today were laid out by a local doctor, Gunnar Bauer, in 1930.",
   "It is a par 71 of about 6,200 yards with around 90 bunkers, and the wind off the water does the rest. Out past the lighthouse is the M&aring;klappen nature reserve, with seals and migrating birds on the sandbank. Play it on a long summer evening, then eat fish in Sk&aring;nor."],
  [("Where", "Falsterbo, 30 minutes from Malm&ouml;, under an hour from Copenhagen"), ("Green fee", "About 1,100&ndash;1,600 SEK (~$111&ndash;$162), ~2,000 SEK in July"), ("Good to know", "Visitors daily with a booked tee time; handicap needed on weekends")],
  "Photos as credited"),
 ("canada", "Canada", "Rouqe", "Canada", ["rqstr","rqmock","rqknit","rqsw","rqhc","rqtwo"],
  ["Rouqe does 1974 club-pro styling: mock necks, retro rugby stripes and script knits, shot on a dry mountain course. The loudest pieces sell out first, and the burgundy stripe here is back after a restock.",
   "It is also the most affordable stop on the trip. Nothing on this list is over $51, and the polos are built for the course in four-way stretch with UPF 50+. The store shows prices in US dollars."],
  "Fairmont Banff Springs", "Banff National Park, Alberta",
  ["Stanley Thompson routed Banff Springs through the Bow Valley below Mount Rundle in the late 1920s, for the Canadian Pacific Railway and its castle of a hotel. It is golf inside a national park, with the Rockies on every side.",
   "The famous hole is the Devil&rsquo;s Cauldron, a par 3 of about 190 yards over a glacial pond to a bowl-shaped green. Play it once and you will understand why it shows up on every list of Canada&rsquo;s great holes."],
  [("Where", "Banff, Alberta, about 90 minutes from Calgary"), ("Green fee", "About CAD 270&ndash;330 in high season (~$197&ndash;$241)"), ("Good to know", "Prices before 5% GST")],
  "Photo: Flickr user &ldquo;Thank you for visiting my page,&rdquo; CC BY 2.0"),
]
SECTIONS = [(c[2], c[0], c[4], c[3]) for c in COUNTRIES]
COURSE_IMG = {"south-africa": "legend", "portugal": "oitavos", "japan": "kawana", "sweden": "falsterbo", "canada": "banff"}
LIFE_KEY = {"south-africa": "odd-ritual", "portugal": "mogshade", "japan": "acct", "sweden": "late-nine", "canada": "rouqe"}
EXTRA = json.loads((ROOT / "research/far-wide/extra.json").read_text())
CREDITS = {"legend": "Photos: South African Tourism, CC BY 2.0",
           "oitavos": "Photos: Oitavos Dunes (1&ndash;3); R&uacute;disicyon, CC BY-SA 4.0 (4)",
           "kawana": "Photos: &#27743;&#25144;&#26449;&#12398;&#12392;&#12367;&#12382;&#12358;, CC BY-SA 4.0 (1); William Cho, CC BY-SA 2.0 (2&ndash;3)",
           "falsterbo": "Photos: Grillo, CC BY-SA 3.0 (1&ndash;2); Jan Ainali, CC BY-SA 3.0 (3&ndash;5)",
           "banff": "Photos: Flickr user &ldquo;Thank you for visiting my page,&rdquo; CC BY 2.0 (1, 3); DXR, CC BY-SA 4.0 (2); AB87, CC BY 3.0 (4)"}
N = 30
PAIRS = {}
BANDS = {}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Independent golf is community first. The brands we cover usually start as a group of friends who play together and could not find clothes or gear that felt like them, so they made their own. The product comes second. The crew, the home course and the local scene come first, and you can see it in every lookbook.</p>
    <p>That makes an indie brand the best travel guide golf has. Follow one from another country and you get a local&rsquo;s view of the game there: the courses they shoot at, the caf&eacute; after the round, the weather they dress for, the jokes they make about the club down the road. It is an insider scoop you will not get from a resort brochure.</p>
    <p><strong>How we picked.</strong> One brand per country, all from our index, chosen because each one could only have come from where it is. Odd Ritual is Cape Town&rsquo;s answer to stiff golf culture. Mogshade weaves Portugal&rsquo;s tiles and mountain wool into headcovers. ANTi COUNTRY CLUB TOKYO turns the members&rsquo; wardrobe into Tokyo streetwear. Late Nine dresses like Swedish tour golf in the &rsquo;90s. Rouqe shoots its 1974 club-pro look in Canadian mountain country. Six pieces from each were in stock on November 4, 2026.</p>
    <p><strong>Then we went to their backyard.</strong> For each country we picked one course you could only play there, the kind you would plan a trip around: a helicopter tee in the Waterberg, Atlantic dunes outside Lisbon, an Alison course above Sagami Bay, a lighthouse links on Sweden&rsquo;s southern tip and Stanley Thompson in the Rockies. Use the brand to get the feel of the place, then go play it.</p>
    <p><strong>A note on prices.</strong> We show each price the way the store shows it to a US visitor. Odd Ritual prices in rand and Late Nine in kronor, so those dollar figures are approximate. Mogshade, ANTi COUNTRY CLUB TOKYO and Rouqe show US dollars.</p>
    <p><strong>What to buy first.</strong> The Mogshade Castelo headcover. It is handwoven on wooden looms and could only have come from Portugal, which is the whole point of this post. On a budget, Rouqe&rsquo;s whole line is under $52.</p>
    <p><strong>Where to go first.</strong> Falsterbo. A real links with a lighthouse on the course, an hour from Copenhagen, is one of the easiest bucket-list rounds in Europe to reach, and one of the few true links on the continent.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Details</div>
      <div class="sidebar-detail"><span class="l">Countries</span><span>5</span></div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>30</span></div>
      <div class="sidebar-detail"><span class="l">Courses</span><span>5</span></div>
      <div class="sidebar-detail"><span class="l">Lookbook photos</span><span>30</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$25&ndash;~$439</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Mogshade Castelo Headcover</span></div>
      <div class="hashtags">
        <span class="hashtag">#GolfTravel</span>
        <span class="hashtag">#IndieGolf</span>
        <span class="hashtag">#GolfStyle</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
CLOSE = """
<section class="products" style="margin-top:8px;padding-top:48px">
  <div class="writeup-body" style="max-width:720px;margin:0 auto">
    <div class="drop-tag grass">The Last Word</div>
    <h2 class="products-hdr" id="last-word">Five Countries Is a Start</h2>
    <p>Golf is played almost everywhere now, and almost everywhere someone is making clothes and gear for it that only make sense from where they are. This is the first stop. If there is a brand from a country we have not covered, send it our way.</p>
    <p>Course details and green fees were checked on November 4, 2026. Seasons and prices change, so confirm with the course before you book.</p>
    <p style="font-family:var(--mono);font-size:10px;letter-spacing:.06em;opacity:.65;line-height:1.8">Header photo: Banff Springs and the Spray River, DXR, CC BY-SA 4.0. Course photos as credited. Product photos are each brand&rsquo;s own.</p>
  </div>
</section>
"""
HERO_ALT = "Banff Springs golf course beside the Spray River with the Canadian Rockies behind"
FRN = json.loads((ROOT / "research/far-wide/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-COL-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
def card(k, idx):
    brand, item, price, url, copy = P[k]
    fr = FRN[k]
    label = H.unescape(f"{brand} {item}").replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>'
                   for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>'
                   for j in range(len(fr)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{brand}</div>'
            f'<div class="product-name">{item} &middot; {price}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="{url}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>'
                     for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')




def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items, pos = [], 1
    for sec in SECTIONS:
        for h in sec[2]:
            items.append({"@type": "ListItem", "position": pos, "url": P[h][3], "name": H.unescape(f"{P[h][0]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-11-04", "dateModified": "2026-11-04",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": items},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Drops & Brands", "item": "https://thegrassyissue.com/#feed"},
            {"@type": "ListItem", "position": 3, "name": BC, "item": URL}]},
    ]
    t, d = H.escape(TITLE, quote=True), H.escape(DESC, quote=True)
    ld = "".join(f'<script type="application/ld+json">\n{json.dumps(b, indent=1, ensure_ascii=False)}\n</script>\n' for b in blocks)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{t} | The Grassy Issue</title>
<meta name="description" content="{d}" />
<link rel="icon" href="/favicon.ico" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<meta property="og:type" content="article" />
<meta property="og:url" content="{URL}" />
<meta property="og:title" content="{t}" />
<meta property="og:description" content="{d}" />
<meta property="og:image" content="{og}" />
<meta property="og:site_name" content="The Grassy Issue" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{t}" />
<meta name="twitter:description" content="{d}" />
<link rel="canonical" href="{URL}" />
<link rel="preload" as="image" href="{IMG}/hero.jpg" />
{ld}"""



def pq(k):
    q, who = PQ[k]
    return (f'\n<div class="pull-quote" style="margin:56px auto 24px">\n  <div class="pull-quote-inner">'
            f'&ldquo;{q}&rdquo;<span class="pull-quote-attr">&mdash; {who}</span></div>\n</div>\n')


def band(k):
    kick, line, items = BANDS[k]
    figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>' for f, alt, cap in items)
    return (f'\n<section class="products" style="margin-top:8px;">\n  <p class="cat-kicker"><strong>{kick}</strong>{line}</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


def swatch(k):
    a, ha, b, hb = PAIRS[k]
    cell = 'flex:1;padding:26px 18px 20px;font-family:var(--mono,monospace);font-size:11px;letter-spacing:.14em;text-transform:uppercase;line-height:1.7'
    return (f'  <div style="display:flex;max-width:620px;margin:6px auto 22px;border:1px solid rgba(20,20,20,.2)">'
            f'<div style="{cell};background:{ha};color:{hb}"><strong>{a}</strong><br>{ha}</div>'
            f'<div style="{cell};background:{hb};color:{ha}"><strong>{b}</strong><br>{hb}</div></div>\n')


WIDESTY = 'style="width:100%;aspect-ratio:16/9;object-fit:cover;display:block;background:#eceae5;"'
CBY = {c[0]: c for c in COUNTRIES}
def section(sec, n0):
    h2, anchor, ids, kicker = sec
    c = CBY[anchor]
    num = [x[0] for x in COUNTRIES].index(anchor) + 1
    prose = "\n".join(f'    <p style="margin:0 0 16px;">{p}</p>' for p in c[5])
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    cprose = "\n".join(f'    <p style="margin:0 0 16px;">{p}</p>' for p in c[8])
    det = "".join(f'<div style="flex:1;min-width:180px;padding:12px 14px;border-left:1px solid rgba(20,20,20,.18)"><div style="font-family:var(--mono);font-size:9px;letter-spacing:.14em;text-transform:uppercase;opacity:.6;margin-bottom:6px">{l}</div><div style="font-size:14px;line-height:1.4">{v}</div></div>' for l, v in c[9])
    ci = COURSE_IMG[anchor]
    alt = H.escape(H.unescape(f"{c[6]}, {c[7]}"))
    cf = EXTRA["courses"][ci]
    frames = "".join(f'<div class="pg-frame"><img src="{f}" alt="{alt} &middot; photo {j+1} of {len(cf)}" loading="lazy" /></div>' for j, f in enumerate(cf))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="Photo {j+1}"></button>' for j in range(len(cf)))
    gal = (f'<div data-frames="{len(cf)}"><div class="product-gallery" style="aspect-ratio:16/9"><div class="pg-track">{frames}</div>'
           f'<button class="pg-arw prev" aria-label="Previous photo">&#8249;</button><button class="pg-arw next" aria-label="Next photo">&#8250;</button>'
           f'<span class="pg-count">1/{len(cf)}</span><div class="pg-dots">{dots}</div></div></div>')
    lk = LIFE_KEY[anchor]
    lfigs = "".join(f'<figure><img src="{f}" alt="{H.escape(H.unescape(c[2]))} lookbook photo {j+1}" loading="lazy" /></figure>' for j, f in enumerate(EXTRA["life"][lk]))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{num:02d} &middot; {c[1]}</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{c[2]}</h2>\n'
            f'  <p class="cat-kicker"><strong>{c[3]}</strong></p>\n'
            f'  <div class="writeup-body" style="max-width:720px;margin:0 auto 26px;">\n{prose}\n  </div>\n'
            f'  <p class="cat-kicker" style="margin-bottom:14px"><strong>The lookbook</strong>{c[2]}&rsquo;s own photos</p>\n'
            f'  <div class="ig-grid">{lfigs}</div>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n'
            f'  <div style="max-width:1180px;margin:46px auto 0;">\n'
            f'    <p class="cat-kicker" style="margin-bottom:14px"><strong>Where to play in {c[1]}</strong>{c[6]} &middot; {c[7]}</p>\n'
            f'    <figure style="margin:0 0 22px;">{gal}'
            f'<figcaption style="font-family:var(--mono);font-size:9px;letter-spacing:.06em;opacity:.6;margin-top:8px;text-align:right">Swipe for more &middot; {CREDITS[ci]}</figcaption></figure>\n'
            f'    <h3 style="font-family:var(--serif);font-style:italic;font-weight:400;font-size:26px;text-align:center;margin:0 0 14px">{c[6]}</h3>\n'
            f'    <div class="writeup-body" style="max-width:720px;margin:0 auto 18px;">\n{cprose}\n    </div>\n'
            f'    <div style="display:flex;flex-wrap:wrap;max-width:860px;margin:0 auto;border:1px solid rgba(20,20,20,.18);border-left:0">{det}</div>\n'
            f'  </div>\n</section>\n'), n0 + len(ids)


def lookbooks():
    figs = "\n".join(f'  <figure><img src="{IMG}/life-{n}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>' for n, alt, cap in LIFE)
    return (f'\n<section class="products" style="margin-top:8px;">\n  <div class="drop-tag grass">{len(LIFE)} photos</div>\n'
            f'  <h2 class="products-hdr" id="lookbooks">From the Lookbooks and In the Wild</h2>\n'
            f'  <p class="cat-kicker"><strong>The pairings on people</strong>Every photo here is the brand&rsquo;s own, from its lookbook, its store or its feed. Royal blue to forest green, in the order above.</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


def main(apply_):
    ids = [k for s in SECTIONS for k in s[2]]
    assert len(ids) == N == len(set(ids)) and set(ids) == set(P), (len(ids), set(P) ^ set(ids))
    for k in ids:
        assert FRN[k] and all((ROOT / f.lstrip("/")).is_file() for f in FRN[k]), k
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>The Edit &middot; Five countries, five courses</span><span class="dot"></span>
    <span>30 picks &middot; 30 lookbook photos &middot; checked November 4, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="{HERO_ALT}" fetchpriority="high" /></div></div>
"""
    body += TAKE.replace("@@NB@@", str(len({P[k][0] for s_ in SECTIONS for k in s_[2]})))
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        o, n = section(s, n); body += o
    body += CLOSE
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Vest Edit", "Collab "):
        if leak in above: bad.append("leak " + leak)
    if fin.count('class="product-card"') != N: bad.append("card count")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", above), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
