"""build-far-and-wide-2.py — "Far and Wide, Vol. 2", 19 November 2026. Cloned from build-far-and-wide.py (Vol. 1, 4 Nov).
Lenny: "let's do a Far and Wide vol 2". Picks (Lenny, 19 Nov): New Zealand Hiroki, Scotland Fyfe (more colorful options),
Hong Kong Dim Sum Golf Club, Australia Gray + Haast (option C), Denmark SLICE TOWN, Spain Rebolf. Rebolf Players Club Bowler
swapped for the Green Slopes Tech Polo (the bowler is shot only on a woman model).
FACTS: product .js endpoints (?currency=USD, the price a US visitor sees) re-checked 19 Nov 2026; Dim Sum from its own
Squarespace store in HK$. Brand stories from TGI's own earlier coverage and the brands' about pages. Courses from the clubs'
own pages and reporting gathered 18-19 Nov 2026. Course photos: Wikimedia Commons, credited (research/far-wide-2/extra.json).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"
TITLE = "Far and Wide, Vol. 2: Six Independent Golf Brands From Around the World, and Where to Play in Their Backyard"
DESC = ("Six more indie golf brands from six countries (Hiroki, Fyfe, SLICE TOWN, Rebolf, Dim Sum Golf Club and Gray + Haast), "
        "their lookbooks, 35 pieces, and the course to play in each brand's backyard.")
H1 = "Far and Wide, Vol. 2: Six More Golf Brands From Around the World, and Where to Play in Their Backyard"
BC = "Far and Wide, Vol. 2"
SLUG = "far-and-wide-vol-2-golf-brands-around-the-world"
IMG = "/images/far-wide-2"
U = lambda d, h: f"https://{d}/products/{h}"
HK, FY, ST, RB, GH = "hirokigolf.com", "fyfegolf.com", "slice-town.com", "rebolf.com", "grayandhaast.com"
DS = lambda s: f"https://www.dimsumgolfclub.com/store/p/{s}"
P = {
 "hkbag": ("Hiroki", "Luxury Leather Sunday Bag, Navy", "$340 <span style=\"opacity:.6\">(was $425)</span>", U(HK, "hiroki-luxury-leather-sunday-bag-navy"),
   "The piece that tells you what Hiroki is: navy leather and no loud branding. Made to age, not date. It is on sale as we publish."),
 "hkapiti": ("Hiroki", "&lsquo;Apiti GC&rsquo; Golf Hat, by Edds", "$35 <span style=\"opacity:.6\">(was $50)</span>", U(HK, "hiroki-apiti-gc-golf-hat"),
   "A leafy camo cap with &ldquo;Apiti Golf Club, New Zealand&rdquo; across the front in old-English type. Also in black."),
 "hkhutt": ("Hiroki", "&lsquo;Hutt Park&rsquo; Golf Hat, by Edds", "$35 <span style=\"opacity:.6\">(was $50)</span>", U(HK, "hiroki-hutt-park-golf-hat"),
   "The same hat for a different club: &ldquo;Hutt Park Golf Club&rdquo; in white on black."),
 "hkleath": ("Hiroki", "Leather Headcover, Black", "from $56.25 <span style=\"opacity:.6\">(driver $71.25)</span>", U(HK, "hiroki-leather-headcover-black"),
   "&ldquo;Full stealth mode,&rdquo; in Hiroki&rsquo;s words: black leather with a soft fleece lining, in driver, fairway and hybrid."),
 "hktart": ("Hiroki", "Wool Headcover, Blue Tartan", "$59.25 <span style=\"opacity:.6\">(driver)</span>", U(HK, "hiroki-wool-headcover-tartan"),
   "A barrel-shaped wool-blend cover in blue and green tartan, fleece lined. The driver size was the one in stock."),
 "hknyl": ("Hiroki", "Nylon Headcover, Royal Blue", "from $44.25", U(HK, "hiroki-nylon-headcover-royal-blue"),
   "Ballistic nylon in a blue you can see from the next fairway. Built to handle the weather."),
 "fyrosso": ("Fyfe", "GT Rosso Leather Blade Putter Cover", "$99", U(FY, "gt-rosso-leather-blade-putter-cover"),
   "Racing-red Italian leather with a cream sherpa lining and twin magnets. The loudest thing Fyfe makes."),
 "fyfescue": ("Fyfe", "Fescue Harris Tweed Headcover", "from $89 <span style=\"opacity:.6\">(driver $99)</span>", U(FY, "fescue-harris-tweed-headcover"),
   "Green and yellow Harris Tweed herringbone, the color of a links in late summer, with a bright yellow fleece lining."),
 "fybay": ("Fyfe", "Bay Hill Harris Tweed Headcover", "from $89 <span style=\"opacity:.6\">(driver $95)</span>", U(FY, "bay-hill-harris-tweed-headcover"),
   "Light gray herringbone flecked with blue and orange, and a bright orange fleece lining that shows every time you pull it off."),
 "fyjura": ("Fyfe", "Jura Sunset Tweed Blade Putter Cover", "$95", U(FY, "jura-sunset-tweed-blade-putter-cover"),
   "A Harris Tweed check in rust, teal and lilac, lined in light blue fleece."),
 "fycarl": ("Fyfe", "Carlogie Harris Tweed Mallet Cover", "$117", U(FY, "carlogie-harris-tweed-mallet-putter-cover"),
   "Deep green tweed woven in the Outer Hebrides from pure new wool, with a single Lion Rampant in gold thread."),
 "fymark": ("Fyfe", "Marksman Rangefinder Case, Surf Blue", "$95", U(FY, "marksman-range-finder-case-surf-the-web"),
   "Waxed canvas made for links weather, with a waterproof YKK zip, paracord pulls and a swivel hook."),
 "sldep": ("SLICE TOWN", "Depeche Golf, Issue #5", "$30", U(ST, "depeche-golf-issue-5"),
   "The independent golf magazine&rsquo;s &ldquo;Home&rdquo; issue, with SLICE TOWN in its game changers section."),
 "slcanv": ("SLICE TOWN", "Canvas Logo Cap, Ultramarine", "$60", U(ST, "canvas-logo-cap-navy"),
   "Cotton canvas, six panels, a curved brim and the wordmark stitched in pale blue. The everyday one."),
 "slgreen": ("SLICE TOWN", "Green Sports Cap", "$55", U(ST, "green-sports-cap"),
   "A lightweight five-panel with the SLICE TOWN guy on a yellow patch, built for range sessions that run late."),
 "slguy": ("SLICE TOWN", "Canvas Guy Cap, Ultramarine", "$60", U(ST, "blue-cotton-cap"),
   "Ultramarine cotton canvas with a small embroidered globe on the front. Understated, for SLICE TOWN."),
 "slsock": ("SLICE TOWN", "White Sports Sock, 3-Pack", "$55", U(ST, "white-sports-sock"),
   "Three pairs of cushioned white sports socks with the logo woven into the toe and ankle, packed in a yellow SLICE TOWN box."),
 "rbhood": ("Rebolf", "Swing or Freeze Hoodie", "$127", U(RB, "swing-or-freeze-hood"),
   "A navy full-zip covered in patches, shot by Rebolf in the snow. The statement piece."),
 "rbwgt": ("Rebolf", "Winter Golf Team Long Sleeve Polo", "$110", U(RB, "winter-golf-team-long-sleeve-polo"),
   "Blue with yellow piping and a Winter Golf Games crest on the chest. Pure team uniform."),
 "rbjoga": ("Rebolf", "Joga Yellow Polo", "$97", U(RB, "joga-yellow-polo"),
   "Yellow with green raglan panels and a short zip. It looks like a 1990s football training top, which is the idea."),
 "rbslope": ("Rebolf", "Green Slopes Tech Polo", "$84", U(RB, "green-slopes-tech-polo"),
   "A teal tech polo with the Rebolf script on the sleeve in yellow. The quietest piece here, and the easiest to wear on the course."),
 "rbriv": ("Rebolf", "Riviera Navy Pleated Shorts", "$91", U(RB, "riviera-navy-shorts"),
   "Double-pleated 100% cotton shorts, designed and made in Barcelona, in a relaxed summer fit."),
 "rbbelt": ("Rebolf &times; Balteus", "Croco Green Velcro Belt", "$89", U(RB, "croco-green-velcro-belt"),
   "Croc-textured and inspired by cowboy belts, with a flat Velcro closure and a magnetic ball marker on the tip."),
 "ghsyrah": ("Gray + Haast", "The Clubhouse Polo, Syrah", "$70 <span style=\"opacity:.6\">(was $88)</span>", U(GH, "the-clubhouse-polo-syrah"),
   "Deep wine red with a cream collar, in quick-drying Drirelease fabric."),
 "ghsky": ("Gray + Haast", "Above Par Polo, Sky Blue", "$70 <span style=\"opacity:.6\">(was $88)</span>", U(GH, "sky-blue-polo"),
   "Pale sky blue with a white collar, &ldquo;inspired by clear skies and open fairways.&rdquo; XL and XXL left."),
 "ghherr": ("Gray + Haast", "The Herringbone Polo, Pine", "$67 <span style=\"opacity:.6\">(was $88)</span>", U(GH, "the-herringbone-polo-pine"),
   "A textured pine herringbone with a hidden zip placket, four-way stretch and UPF 50+."),
 "ghrange": ("Gray + Haast", "The Range Polo, Navy + Sand", "$70 <span style=\"opacity:.6\">(was $88)</span>", U(GH, "the-range-polo-navy-sand"),
   "Navy body, sand back panel and collar. Only XXL was left when we checked."),
 "ghplay": ("Gray + Haast", "Players Golf Shorts 8&Prime;, Navy", "$70 <span style=\"opacity:.6\">(was $88)</span>", U(GH, "the-players-golf-shorts-8-navy"),
   "An 8-inch tailored short, light and breathable, that looks as right at lunch as it does on the 18th."),
 "ghcargo": ("Gray + Haast", "Weekend Cargo Golf Short, Stone", "$73 <span style=\"opacity:.6\">(was $97)</span>", U(GH, "weekend-cargo-golf-short-stone"),
   "A relaxed performance cargo with a YKK metal fly, popper pockets and a gel-grip waistband that stays put through the swing."),
 "dsksc": ("Dim Sum Golf Club", "Kau Sai Chau T-Shirt", "HK$435 (~$56)", DS("ksc-tshirt"),
   "A tribute to Hong Kong&rsquo;s only public course, drawn in blue line art inspired by porcelain painting. The pick that ties to the course below."),
 "dspolo": ("Dim Sum Golf Club", "ProTour Polo", "HK$525 (~$67)", DS("pro-tour-polo"),
   "175g nylon-spandex in sage, white or black, with Hong Kong logos given a dim sum twist. Designed and assembled in Hong Kong."),
 "dsgilet": ("Dim Sum Golf Club", "Reversible Golf Gilet", "HK$585 (~$75)", DS("reversible-golf-gilet"),
   "Seven pockets, a fleece lining and two faces: clean on one side, textured on the other. The store notes gilets take seven days."),
 "dshood": ("Dim Sum Golf Club", "Country Club Lightweight Hoodie", "HK$595 (~$76)", DS("country-light-hoodie"),
   "280gsm cotton blend with the club&rsquo;s steamer-basket crest on the back, in navy or green."),
 "dscap": ("Dim Sum Golf Club", "HoleInWan Cap", "HK$315 (~$40)", DS("hole-in-wan-cap"),
   "A cream cotton dad cap with the best pun in this post. Designed and assembled in Hong Kong."),
 "dsset": ("Dim Sum Golf Club", "Ball Marker &amp; Sock Set", "HK$180 (~$23)", DS("dim-sum-ball-marker-tee-set"),
   "A dumpling-basket ball marker and a pair of club socks in a metal tin. The easy gift in this post."),
}
# (anchor, country, brand, city, ids, brand paras, course name, course place, course paras, details)
COUNTRIES = [
 ("new-zealand", "New Zealand", "Hiroki", "Auckland", ["hkbag", "hkapiti", "hkhutt", "hkleath", "hktart", "hknyl"],
  ["Hiroki is an Auckland brand with a Japanese-sounding name, and the name is deliberate. The brand says it was chosen to evoke the precision of Japanese craftsmanship and to work as a filter: if a design feels forced, it does not belong.",
   "The range is narrow on purpose: stand bags, leather Sunday bags, a handful of headcovers and some hats, with the bags named for places from Tokyo to Wellington. The two hats here, made with Edds, carry the names of New Zealand clubs, Apiti and Hutt Park. Hiroki also runs its own events, like a 25-team Summer Shootout at Jack&rsquo;s Point. Every piece here was on sale when we checked; the original prices are shown."],
  "Cape Kidnappers", "Hawke&rsquo;s Bay, North Island",
  ["Cape Kidnappers is the most dramatic round in New Zealand. Tom Doak laid it out across a peninsula at the southern end of Hawke&rsquo;s Bay, on a working sheep and cattle station, and the fairways run out along ridges that stop at cliffs about 140 meters above the Pacific. Doak&rsquo;s own line on the site: if it were any more dramatic, &ldquo;it would probably be cordoned off as a national park.&rdquo;",
   "It opened in 2004. Three times you carry from the end of one ridge to the next, and at the 6th and 15th a pulled approach can leave the planet: Doak reckons the ball hangs for nearly ten seconds before it reaches the ocean. The land around it is a predator-fenced wildlife sanctuary, so expect rare birds in the ravines."],
  [("Where", "Hawke&rsquo;s Bay, on the North Island&rsquo;s east coast"), ("Green fee", "NZ$975 (~$550) international, NZ$500 (~$282) for NZ residents, Oct 2026&ndash;Apr 2027"), ("Good to know", "Lodge guests get 10% off; caddies available")]),
 ("scotland", "Scotland", "Fyfe", "Fife", ["fyrosso", "fyfescue", "fybay", "fyjura", "fycarl", "fymark"],
  ["Fyfe makes headcovers and bags by hand in Scotland. Neil Rennie founded it in Fife in 2021, and the materials are as Scottish as they come: Harris Tweed woven in the Outer Hebrides, tartans, and waxed canvas made for links weather.",
   "Fyfe&rsquo;s best covers are the colorful ones, so that is what we picked: a racing-red leather blade, a green-and-yellow Fescue, Bay Hill with its bright orange lining, a rust-and-teal Jura Sunset check and a green Carlogie mallet with a gold Lion Rampant. The store shows US visitors dollar prices."],
  "Kingsbarns Golf Links", "Kingsbarns, Fife",
  ["Fyfe was founded in Fife, so the backyard course had to be in the Kingdom. Kingsbarns sits seven miles from St Andrews along almost two miles of North Sea coast, and the club&rsquo;s own pitch is that every hole embraces the sea. It looks like it has been there for centuries. It opened in 2000, a Kyle Phillips design, though golf on the site goes back to an 18th-century golfing society.",
   "It is one of the three courses that host the Alfred Dunhill Links every October, alongside the Old Course and Carnoustie. Fairways roll through gorse and dune right down to the rocks. It is not cheap and it closes for winter, so plan it for summer."],
  [("Where", "Seven miles southeast of St Andrews"), ("Green fee", "&pound;486 (~$646), May&ndash;early November 2026"), ("Good to know", "Closed in winter; book well ahead")]),
 ("denmark", "Denmark", "SLICE TOWN", "Copenhagen", ["sldep", "slcanv", "slgreen", "slguy", "slsock"],
  ["SLICE TOWN makes golf clothes for people who came to the game through simulators and late-night range sessions. A Dane and a Swede started it at the end of 2024, and the clothes are designed in Copenhagen. Its line on its own About page: &ldquo;Our purpose is to challenge tradition, and make it possible for golfers to wear whatever they want on the course.&rdquo;",
   "It puts as much into events as product, including a late-night simulator tournament in Copenhagen with a DJ and a bar. The pieces here are the easy way in: three caps, a box of socks and the issue of Depeche Golf that put SLICE TOWN in its game changers section. The store shows US visitors dollar prices."],
  "Københavns Golf Klub", "Dyrehaven, Klampenborg",
  ["Københavns Golf Klub is the first golf club in Scandinavia, founded in 1898. Its first members played on a common in Copenhagen and dug the holes themselves every morning, then filled them in again at night. In 1899 it moved to Dyrehaven, the royal deer park north of the city, and the 18-hole course it opened there in 1928 is still largely the one you play today.",
   "The deer never left. The course runs across the open plain below the old royal hunting lodge, the Hermitage, among herds of fallow and red deer, and the club plays summer greens year-round. It is part golf course, part safari, a short train ride from the city."],
  [("Where", "Klampenborg, north of central Copenhagen"), ("Green fee", "Confirm with the club; a registered handicap is required"), ("Good to know", "Deer on the course, summer greens year-round")]),
 ("spain", "Spain", "Rebolf", "Barcelona", ["rbhood", "rbwgt", "rbjoga", "rbslope", "rbriv", "rbbelt"],
  ["Rebolf is from Barcelona, founded by a golf professional who, in the brand&rsquo;s words, &ldquo;felt he needed a change.&rdquo; Its clothes are made at a local studio in small runs, and they look more like a football kit than a pro shop. Rebolf puts it this way: &ldquo;We bridge the gap between the fairway and the street.&rdquo;",
   "The newest collection goes to the mountains: a patched full-zip and a Winter Golf Games long-sleeve polo, shot in the snow. We paired them with a yellow football polo, a teal tech polo, pleated Riviera shorts and the croc belt Rebolf makes with Balteus. The store shows US visitors dollar prices."],
  "Camiral, Stadium Course", "Caldes de Malavella, Girona",
  ["Camiral, the resort long known as PGA Catalunya, sits in the pine woods near Girona, about an hour from Barcelona. Its Stadium Course, by Neil Coles and &Aacute;ngel Gallardo, has been testing tour players since 1999 and has hosted the Spanish Open three times. Lakes wrap the greens, umbrella pines line every fairway, and the course is irrigated entirely with recycled water.",
   "In 2031 it hosts the Ryder Cup, the first in Spain in more than 30 years. Play it now, before everyone else wants to. Green fees include a buggy, and men need a handicap of 28 or lower."],
  [("Where", "Near Girona, about 1 hour from Barcelona"), ("Green fee", "&euro;143&ndash;&euro;192 with buggy (~$157&ndash;$211)"), ("Good to know", "Host of the 2031 Ryder Cup; handicap max 28 for men")]),
 ("hong-kong", "Hong Kong", "Dim Sum Golf Club", "Hong Kong", ["dsksc", "dspolo", "dsgilet", "dshood", "dscap", "dsset"],
  ["Dim Sum Golf Club started in Hong Kong in the winter of 2023. Its founder, Luke, a UK expat, ran into how limited and exclusive golf access is in the city, so he started a club for people who just wanted to play more. Joining is free; a paid membership adds golf days, simulator nights and trips around Asia.",
   "The clothes come second to the club, and they are full of inside jokes for people who know the city: a dumpling-basket crest, a HoleInWan cap, a ball marker shaped like a steamer. Prices are in Hong Kong dollars; the dollar figures here are approximate. The store notes there are no refunds, and exchanges are only in Hong Kong."],
  "Kau Sai Chau", "Sai Kung",
  ["Kau Sai Chau is Hong Kong&rsquo;s only public golf course, and the trip is half the point: you take a ferry from Sai Kung Town to an island with three courses on it and the mountains of the New Territories all around. The North and South Courses are Gary Player designs; the East Course is by Nelson &amp; Haworth.",
   "It is the course Dim Sum&rsquo;s Kau Sai Chau T-shirt is drawn from, and it is the one round in Hong Kong a visitor can book without knowing a member. Book ahead, and bring an appetite: Sai Kung&rsquo;s seafood restaurants are waiting at the pier when you get back."],
  [("Where", "Kau Sai Chau island, by ferry from Sai Kung"), ("Green fee", "About HK$1,030&ndash;1,360 (~$132&ndash;$174) for visitors at the last published rate; confirm with the club"), ("Good to know", "The only public golf in Hong Kong")]),
 ("australia", "Australia", "Gray + Haast", "Burleigh Heads", ["ghsyrah", "ghsky", "ghherr", "ghrange", "ghplay", "ghcargo"],
  ["Gray + Haast is based in Burleigh Heads on the Gold Coast, and it designs for the rhythm of coastal life: &ldquo;early tee times, late afternoon rounds, and a community that values connection as much as competition,&rdquo; as the brand puts it.",
   "The clothes are clean and colorful: polos with contrast collars in wine, sky blue, pine and navy, and shorts that work as well at lunch as on the course. Every piece here was on sale when we checked, so the original prices are shown too. The store shows US visitors dollar prices."],
  "Cape Wickham Links", "King Island, Tasmania",
  ["Cape Wickham is golf at the end of the map. It sits on the northern tip of King Island, out in Bass Strait between Tasmania and the mainland, and it is routed around the Cape Wickham Lighthouse, built in 1861. Mike DeVries and Darius Oliver designed it, and it opened to the public in late 2015.",
   "Holes run along white-sand beaches and rocky headlands, and the sea is in view the whole way round. Walk it with a caddie if you can; the greens are fescue, and the wind off the strait decides everything. Stay on site and the all-day fee costs the same as 18 holes."],
  [("Where", "King Island, in Bass Strait, Tasmania"), ("Green fee", "A$315 (~$205) for international visitors, A$235 (~$153) for Australians, 2026"), ("Good to know", "Book by phone or email; caddies two weeks ahead")]),
]
SECTIONS = [(c[2], c[0], c[4], c[3]) for c in COUNTRIES]
COURSE_IMG = {"new-zealand": "capek", "scotland": "kingsbarns", "denmark": "rcgc", "spain": "camiral", "hong-kong": "ksc", "australia": "capew"}
LIFE_KEY = {"new-zealand": "hiroki", "scotland": "fyfe", "denmark": "slice", "spain": "rebolf", "hong-kong": "dimsum", "australia": "gh"}
EXTRA = json.loads((ROOT / "research/far-wide-2/extra.json").read_text())
FRN = json.loads((ROOT / "research/far-wide-2/frames.json").read_text())
def _cred(k):
    rows = EXTRA["credits"][k]
    groups = []
    for i, (a, lic, _t) in enumerate(rows, 1):
        a = a.split(" from ")[0].rstrip(". ").strip()
        lab = f"{H.escape(a)}, {lic}" if lic else H.escape(a)
        if groups and groups[-1][0] == lab: groups[-1][1].append(i)
        else: groups.append((lab, [i]))
    if len(groups) == 1: return "Photos: " + groups[0][0]
    fmt = lambda n: str(n[0]) if len(n) == 1 else f"{n[0]}&ndash;{n[-1]}"
    return "Photos: " + "; ".join(f"{lab} ({fmt(n)})" for lab, n in groups)
CREDITS = {k: _cred(k) for k in COURSE_IMG.values()}
N = 35
PAIRS, BANDS = {}, {}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>In <a href="/drops/far-and-wide-golf-brands-around-the-world">Vol. 1</a> we went to South Africa, Portugal, Japan, Sweden and Canada. The idea holds: independent golf is community first. A brand from another country is a local&rsquo;s view of the game there, its weather, its courses, its jokes, and the best way in before you book a flight.</p>
    <p><strong>How we picked.</strong> One brand per country, six new countries, each brand from our own coverage and each one that could only have come from where it is. Hiroki brings Japanese precision to Auckland. Fyfe cuts Harris Tweed in Fife. SLICE TOWN dresses Copenhagen&rsquo;s simulator crowd. Rebolf turns Barcelona football kits into golf clothes. Dim Sum Golf Club is a Hong Kong club first and a brand second. Gray + Haast dresses the Gold Coast. Every piece here was in stock on November 19, 2026.</p>
    <p><strong>Then we went to their backyard.</strong> For each country, the most dramatic course a visitor can actually book: cliff-top fairways 140 meters above the Pacific, a Fife links where every hole meets the sea, a royal deer park outside Copenhagen, the 2031 Ryder Cup venue, an island you reach by ferry and a lighthouse links in Bass Strait.</p>
    <p><strong>A note on prices.</strong> We show each price the way the store shows it to a US visitor. Five of the six stores show US dollars. Dim Sum Golf Club prices in Hong Kong dollars, so those dollar figures are approximate. Hiroki and Gray + Haast were running sales, and we show the original price beside the sale price.</p>
    <p><strong>What to buy first.</strong> The Fyfe Carlogie mallet cover. Harris Tweed from the Outer Hebrides and a gold Lion Rampant could only come from Scotland. On a budget, Dim Sum&rsquo;s ball marker and sock set is about $23.</p>
    <p><strong>Where to go first.</strong> Cape Kidnappers. There is nothing else in golf like hitting an approach along a ridge with a 140-meter drop on both sides. If the flight is too far, Kingsbarns is seven miles from St Andrews.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Details</div>
      <div class="sidebar-detail"><span class="l">Countries</span><span>6</span></div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>35</span></div>
      <div class="sidebar-detail"><span class="l">Courses</span><span>6</span></div>
      <div class="sidebar-detail"><span class="l">Lookbook photos</span><span>36</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>~$23&ndash;$340</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Fyfe Carlogie Mallet Cover</span></div>
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
    <h2 class="products-hdr" id="last-word">Eleven Countries and Counting</h2>
    <p>Between <a href="/drops/far-and-wide-golf-brands-around-the-world">Vol. 1</a> and this one, that is eleven countries, eleven brands and eleven courses. Somewhere there is a brand making golf clothes that only make sense from where it is. If you know one from a country we have not covered, send it our way.</p>
    <p>Course details and green fees were gathered November 18&ndash;19, 2026. Seasons and prices change, so confirm with the course before you book.</p>
    <p style="font-family:var(--mono);font-size:10px;letter-spacing:.06em;opacity:.65;line-height:1.8">Header photo: Cape Kidnappers. Course photos as credited, from the clubs and Wikimedia Commons. Product and lookbook photos are each brand&rsquo;s own.</p>
  </div>
</section>
"""
HERO_ALT = "Aerial view of Cape Kidnappers golf course, its fairways running out along ridges to cliffs above the Pacific"
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
         "url": URL, "image": og, "datePublished": "2026-11-19", "dateModified": "2026-11-19",
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
    <span>The Edit &middot; Six countries, six courses</span><span class="dot"></span>
    <span>35 picks &middot; 36 lookbook photos &middot; checked November 19, 2026</span>
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
