#!/usr/bin/env python3
"""build-clamp-golf-btk.py — Brand to Know: Clamp Golf Company.
1 October 2026. Lenny: "Let's do a solid brand to know - https://www.clampgolfcompany.co.uk/", then
"No on C29,36, no on vintage, vegan puffer and fun section, replace with sold out section titled 'Sold out
but super dope' add flavor images/ IRL stuff, write up and quotes if possible."

FACTS: Clamp's own Meet the Team, FAQs, homepage and product pages, read 1 Oct 2026. Product copy on the
reworked covers is partly templated (it names the wrong source bag on several), so only titles, set
contents and photos are used for those. QUOTES: verbatim from Clamp's Meet the Team page and the Military
Range product page. PHOTOS: Clamp's own (product pages, homepage and Meet the Team). Prices in GBP from
the store, ~USD at 1.3449 (the store's own USD rate, 1 Oct 2026).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "brand-to-know-clamp-golf-company"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/clamp-golf"
FR = json.loads((ROOT / "research/clamp/frames.json").read_text())
SHOP = "https://www.clampgolfcompany.co.uk/products/"
BRAND = "Clamp Golf Co."
R = 1.3449

TITLE = "Clamp Golf Company — Handmade Headcovers From a Yorkshire Workshop"
DESC = ("Clamp Golf Company started in a lockdown garage and now sews headcovers in Yorkshire, from Harris Tweed to "
        "1-of-1 covers cut from Carhartt and Louis Vuitton. 36 picks, plus the ones that got away.")
H1 = "Brand to Know: Clamp Golf Company &mdash; Headcovers Made in a Yorkshire Workshop"


def gbp(a, b=None, frm=False):
    if b and b != a:
        return f"&pound;{a:g}&ndash;&pound;{b:g} (~${round(a * R)}&ndash;${round(b * R)})"
    return ("From " if frm else "") + f"&pound;{a:g} (~${round(a * R)})"


# slug -> (name, detail, price, copy)
P = {
 # New this season
 "military-range": ("Military Range", "New &middot; with Military vs Cancer", gbp(38, frm=True) + " driver",
   "Clamp cuts these from decommissioned military uniforms, clothing and kit donated by the charity Military vs Cancer, so every cover carries a bit of history. Sales go back into the partnership and into donations to the charity. There are driver, wood, hybrid and barrel covers, a shoe bag and two pouches."),
 "brown-genuine-leather-mallet-cover": ("Brown Leather Mallet Cover", "New", gbp(61),
   "This is a genuine leather mallet cover with a matching brown fleece lining, new in August. There is a centre-shafted version too."),
 "black-clamp-golf-co-mascot-headcovers": ("Black Mascot Headcovers", "Genuine leather", gbp(59, frm=True),
   "These are black genuine leather covers with the Clamp mascot embroidered on, in driver, wood and hybrid, with a matching blade cover and two pouches."),
 "brown-genuine-leather-headcovers": ("Limited Run Brown Leather Headcovers", "Numbered", gbp(73, frm=True) + " driver",
   "This limited run is brown genuine leather with a brown fleece lining and embroidered numbers: 1, 3, 4, 7 and X. Barrel shapes and an alignment stick cover are available too."),
 # Reworked
 "reworked-louis-vuitton-headcovers": ("Louis Vuitton Reworked Set", "1 of 1 &middot; four covers", gbp(1150),
   "Clamp cut this driver, wood, hybrid and alignment stick set from a Louis Vuitton bag. At &pound;1,150 it is the most expensive thing in the shop, and there is only one."),
 "carhartt-reworked-headcovers-8": ("Carhartt Reworked Set", "1 of 1 &middot; four covers", gbp(225),
   "This is a driver, wood, hybrid and alignment stick set cut from a Carhartt bag, with a black leather backing and a fleece lining."),
 "1-of-1-grey-patagonia-rework-headcovers": ("Patagonia Reworked Set", "1 of 1 &middot; five pieces", gbp(230),
   "This set was cut from a Patagonia coat, with leather backing: driver, wood, hybrid, a blade cover and a valuables pouch."),
 "1-of-1-ralph-lauren-bear-rework-headcovers": ("Ralph Lauren Bear Reworked Set", "1 of 1 &middot; three covers", gbp(270),
   "This three-cover set is patchworked with the Polo bear front and centre on the driver."),
 "palace-reworked-headcovers": ("Palace Reworked Set", "1 of 1 &middot; four covers", gbp(300),
   "This one was cut from a Palace bag, with leather backing: driver, wood, hybrid and a blade putter cover."),
 "reworked-north-face-headcovers-8": ("North Face Reworked Set", "1 of 1 &middot; five pieces", gbp(210),
   "This North Face set has a driver, wood and hybrid cover, an alignment stick cover and a tee holder."),
 "1-of-1-retro-adidas-rework-headcovers": ("Retro Adidas Reworked Set", "1 of 1 &middot; four covers", gbp(180),
   "These are black covers with the blue Adidas trim and logo: driver, wood, hybrid and an alignment stick cover."),
 "snap-on-reworked-headcovers": ("Snap-On Reworked Set", "1 of 1 &middot; three covers", gbp(160),
   "This is a driver, wood and hybrid set in the red Snap-On branding, the tool company, for whoever keeps a garage as tidy as their bag."),
 "supreme-reworked-mallet-headcover": ("Supreme Reworked Mallet Cover", "1 of 1", gbp(150),
   "This is a single grey mallet cover with the red Supreme tag. It is the cheapest way into the reworked line if you only want to dress the putter."),
 "retro-adidas-reworked-driver-headcover-1": ("Retro Reworked Driver Cover", "1 of 1", gbp(130),
   "A loud vintage sportswear driver cover in neon green, pink and navy. It is one cover, so it suits a bag that is otherwise plain."),
 "vw-van-headcover": ("VW Van Driver Cover", "1 of 1", gbp(30),
   "This driver cover has the VW badge on teal and white. At &pound;30 it is the bargain of the reworked line."),
 # Leather and Yorkshire
 "brown-patchwork-genuine-leather-headcovers-copy": ("Brown Patchwork Leather Headcovers", "Driver to alignment stick", gbp(58, frm=True) + " driver",
   "These covers are patchworked from different brown leathers with a brown fleece lining. No two panels come out quite the same."),
 "eburacum-evergreen": ("Brigantes: Eburacum Evergreen", "Leeds leather", gbp(75, frm=True) + " driver",
   "The Brigantes range is named for the tribe that held northern England, and Eburacum was the Roman name for York. These covers are green leather sourced in Leeds, with a V-cut hem and embroidered numbers for an antique look."),
 "brigantium-bronze": ("Brigantes: Brigantium Bronze", "Leeds leather", gbp(75, frm=True) + " driver",
   "This is the same Brigantes pattern in a bronze-brown leather, with the V-cut hem and embroidered numbers."),
 "headcovers": ("&ldquo;Headcovers&rdquo; Word Covers", "Eight colours", gbp(60, frm=True) + " driver",
   "These leather covers say exactly what they are: &ldquo;Driver&rdquo;, &ldquo;3 Wood&rdquo;, &ldquo;Hybrid&rdquo; or &ldquo;Putter&rdquo; embroidered in quotes. The leather is sourced in Yorkshire, and there are eight colours."),
 "yorkshire-headcover": ("Yorkshire Headcover", "Blue leather", gbp(57, frm=True) + " driver",
   "This blue leather cover has &ldquo;Yorkshire&rdquo; embroidered on it and a matching blue fleece. It is the one for anyone from God&rsquo;s own county."),
 "remove-before-flight-headcover": ("Remove Before Flight Headcover", "Red leather", gbp(60, frm=True) + " driver",
   "This red leather cover has &ldquo;Remove Before Flight&rdquo; stitched down the middle like an aircraft safety tag. Orders over &pound;100 come with a matching bag tag."),
 "custom-embroidered-portrait-covers": ("Custom Portrait Cover", "Send a photo", gbp(90, 125),
   "Send Clamp a photo, of your dog say, and it embroiders the portrait onto a leather cover in the colours you choose."),
 # Harris Tweed
 "brown-and-beige-glen-check-harris-tweed®-headcovers-copy": ("Brown and Beige Houndstooth", "Harris Tweed", gbp(58, frm=True) + " driver",
   "This is genuine Harris Tweed from the Outer Hebrides, backed with brown leather. The houndstooth is the classic one."),
 "pink-harris-tweed®-headcovers": ("Pink and Navy Check", "Harris Tweed", gbp(58, frm=True) + " driver",
   "This Harris Tweed comes in a loud pink and navy check, for a bag that should not be mistaken for anyone else&rsquo;s."),
 "black-white-houndstooth-harris-tweed®-headcovers": ("Black and White Houndstooth", "Harris Tweed", gbp(49, 64),
   "The black and white houndstooth comes as covers and as matching valuables and scope pouches."),
 "harris-macleod-tartan-headcovers": ("Harris Macleod Tartan", "Harris Tweed", gbp(58, frm=True) + " driver",
   "This is the Macleod tartan in Harris Tweed, with leather backing and a fleece lining."),
 "teal-twill-headcovers": ("Teal Twill", "Harris Tweed", gbp(58, frm=True) + " driver",
   "This teal twill is backed with green leather and comes in barrel shapes as well as the standard covers."),
 # Accessories
 "genuine-leather-bag": ("Brown Leather Pouch", "23 &times; 12cm", gbp(55),
   "This drawstring leather pouch holds up to 20 balls, or a lot of tees."),
 "green-genuine-leather-range-finder-pouch": ("Green Leather Scope Pouch", "Magnetic close", gbp(46),
   "This leather rangefinder pouch has a magnetic fastener, a metal clasp and a fleece lining."),
 "yardage-book-holder": ("Leather Yardage Book Holder", "Ten colours", gbp(48),
   "This genuine leather holder fits one yardage book and one scorecard, in ten colours from black to Tiffany blue."),
 "clamp-golf-co-tee-holder": ("Tee Holder", "With six tees", gbp(6),
   "This little leather tee holder clips to the bag with six tees in it. At &pound;6 it is the cheapest thing Clamp makes."),
 "oak-headcover-display": ("Oak Headcover Display", "Local oak", gbp(90),
   "Clamp makes this stand in-house from local oak, to show off a full set of covers at home."),
 "clamp-golf-co-ball-marker-5": ("Yorkshire Rose Ball Marker", "Solid brass", gbp(28),
   "This solid brass marker is machined in-house with the white rose of Yorkshire on it."),
 "dartboard-ball-marker": ("Dartboard Ball Marker", "Solid brass", gbp(28),
   "This is the same solid brass marker with a dartboard, for the pub-league player."),
 "portrait-ball-marker": ("Portrait Ball Marker", "Engraved", gbp(40),
   "Send a photo and Clamp engraves it onto a brass marker. Its own example is a pug."),
 "custom-golf-pin-flags": ("Custom Pin Flags", "Printed or embroidered", gbp(27, frm=True),
   "Clamp prints or embroiders flags with your club crest or logo, from a single flag up to a full 18-hole set."),
}

# ---- Reworked line ("The Vault"), all of it (Lenny, 1 Oct 2026: "I love the supreme, nike, carhartt sold out -
# streetwear stuff, all the reworked options"). In-stock pieces get cards; sold-out ones go to their own section.
RW = json.loads((ROOT / "research/clamp/rework.json").read_text())
FAV = {  # Lenny's favourites, sent as links 1 Oct 2026, with copy written from the photos and set contents
 "carhartt-reworked-headcovers-7": ("Carhartt Reworked Set", "1 of 1 &middot; our pick",
   "Black Carhartt duck canvas with the square Carhartt label on the driver, brass rivets and a utility pocket on the wood: driver, wood, hybrid and an alignment stick cover. It is the best thing in the shop that you can still buy."),
 "supreme-reworked-hybrid-headcover": ("Supreme Reworked Hybrid", "Sold out &middot; was &pound;90",
   "A pale grey hybrid cover cut from a Supreme bag with the box-logo lettering repeated in tone, closed with a toggle and drawcord."),
 "reworked-louis-vuitton-headcovers-2": ("Louis Vuitton Reworked Set", "Sold out &middot; was &pound;1,200",
   "Driver, wood, hybrid and alignment stick, all in the brown LV monogram canvas with leather backing. The one that went first."),
 "orange-nike-rework-headcovers": ("Orange Nike Hybrid", "Sold out &middot; was &pound;65",
   "One hybrid cover in safety orange with a giant white Nike swoosh and wordmark running up the front."),
 "nike-reworked-headcovers-24": ("Nike ACG Reworked Set", "Sold out &middot; was &pound;290",
   "Cut from a Nike ACG pack: black grid ripstop, coyote webbing and buckles, the ACG triangle and the Bigfoot patch. Driver, wood, hybrid and an alignment stick cover."),
 "adidas-reworked-headcovers-2": ("Adidas Reworked Set", "Sold out &middot; was &pound;195",
   "Beige waffle fleece with black zips and drawcords, the Adidas performance logo across the driver and a woven tag: driver, wood and hybrid."),
}

def _inc(o):
    t = (o["inc"] or "").replace(" x ", " ").replace("1 ", "").replace(" &", ",")
    return re.sub(r"\s+", " ", t).strip(" ,")

def rw_copy(o):
    if o["slug"] in FAV:
        return FAV[o["slug"]][2]
    src = f"cut from a {o['src']}" if o["src"] else "cut from a branded original"
    inc = _inc(o)
    return (f"One of one, {src} and backed with leather and a fleece lining." + (f" The set: {inc}." if inc else ""))

def rw_name(o):
    if o["slug"] in FAV:
        return FAV[o["slug"]][0]
    t = H.escape(o["title"].replace("Headcovers", "Set").replace("Headcover", "Cover").replace("reworked", "Reworked").replace("Rework ", "Reworked "))
    return t

LV = [o for o in RW if o["avail"] and "louis-vuitton" in o["slug"]]
STREET = [o for o in RW if o["avail"] and "louis-vuitton" not in o["slug"]]
STREET.sort(key=lambda o: (o["slug"] not in FAV, -o["gbp"]))
LV.sort(key=lambda o: -o["gbp"])
SOLDOUT = [o for o in RW if not o["avail"]]
SOLDOUT.sort(key=lambda o: (o["slug"] not in FAV, -o["gbp"]))
for o in STREET + LV:
    if o["slug"] not in P:
        P[o["slug"]] = (rw_name(o), "1 of 1", gbp(o["gbp"]), rw_copy(o))
    elif o["slug"] in FAV:
        P[o["slug"]] = (FAV[o["slug"]][0], FAV[o["slug"]][1], gbp(o["gbp"]), FAV[o["slug"]][2])
SOLD = {o["slug"]: (rw_name(o), f"&pound;{o['gbp']:g}", rw_copy(o)) for o in SOLDOUT}


SECTIONS = [
    ("new", "New This Season", "new-this-season",
     ["military-range", "brown-genuine-leather-mallet-cover", "black-clamp-golf-co-mascot-headcovers", "brown-genuine-leather-headcovers"],
     "<strong>Four pieces &middot; from &pound;38 (~$51)</strong>The headline this autumn is the Military Range. Clamp works with the charity Military vs Cancer, which donates decommissioned uniforms and kit for Clamp to cut into covers, and sales fund more donations. Alongside it are a new brown leather mallet cover, black mascot covers and a limited run of numbered brown leather covers."),
    ("street", "The Vault: Reworked Streetwear", "reworked",
     [o["slug"] for o in STREET],
     f"<strong>{len(STREET)} one-offs &middot; &pound;30&ndash;&pound;300 (~$40&ndash;$403)</strong>This is the best reworked headcover work we have seen in a while. Clamp takes a Carhartt bag, a Nike pack, a North Face holdall or a Supreme bag, cuts it up, backs it with leather and turns it into a set of covers, usually with the original label, zips and webbing left on. Every one is a one-off in Clamp&rsquo;s limited line, The Vault, and when it sells it is gone. Carhartt, Nike, Adidas and Tommy Hilfiger lead the list, with Palace, Patagonia, Snap-On and a &pound;30 VW cover in the mix."),
    ("lv", "The Vault: Louis Vuitton", "louis-vuitton",
     [o["slug"] for o in LV],
     f"<strong>{len(LV)} pieces &middot; &pound;120&ndash;&pound;1,150 (~$161&ndash;$1,547)</strong>Then there is the monogram. Clamp cuts covers from Louis Vuitton bags, with brown leather backing, and sells them as full sets, single woods and hybrids, a blade cover and alignment stick covers. They are priced like the bag they came from, and they are the loudest thing you could put in a golf bag."),
    ("leather", "Genuine Leather and Yorkshire Pride", "leather",
     ["brown-patchwork-genuine-leather-headcovers-copy", "eburacum-evergreen", "brigantium-bronze", "headcovers", "yorkshire-headcover",
      "remove-before-flight-headcover", "custom-embroidered-portrait-covers"],
     "<strong>Seven pieces &middot; from &pound;57 (~$77)</strong>The everyday Clamp cover is genuine leather sourced in Yorkshire, and the county is all over it. The Brigantes range is named for the tribe that held the north before the Romans, with Leeds leather and a V-cut hem. There is a Yorkshire cover, word covers that say exactly what they are, a Remove Before Flight tag, and a cover with your dog&rsquo;s portrait on it."),
    ("tweed", "Harris Tweed", "harris-tweed",
     ["brown-and-beige-glen-check-harris-tweed®-headcovers-copy", "pink-harris-tweed®-headcovers", "black-white-houndstooth-harris-tweed®-headcovers",
      "harris-macleod-tartan-headcovers", "teal-twill-headcovers"],
     "<strong>Five patterns &middot; from &pound;58 (~$78)</strong>Clamp backs genuine Harris Tweed from the Outer Hebrides with leather, and keeps around twenty patterns going at once. These are the five we would pick: a classic houndstooth, a loud pink check, black and white houndstooth with matching pouches, the Macleod tartan and a teal twill."),
    ("acc", "Accessories", "accessories",
     ["genuine-leather-bag", "green-genuine-leather-range-finder-pouch", "yardage-book-holder", "clamp-golf-co-tee-holder", "oak-headcover-display",
      "clamp-golf-co-ball-marker-5", "dartboard-ball-marker", "portrait-ball-marker", "custom-golf-pin-flags"],
     "<strong>Nine pieces &middot; &pound;6&ndash;&pound;90 (~$8&ndash;$121)</strong>The leatherwork carries over into the small stuff: pouches, a scope case and a yardage book holder in ten colours. There are solid brass ball markers machined in-house, a Yorkshire rose among them, and an oak stand to display the covers at home. Clubs can order a full set of embroidered pin flags."),
]
N = sum(len(x[3]) for x in SECTIONS)

PQ = {
    "idea": ("What started as an idea for more personal headcovers has grown into a workshop making custom pieces for golfers and clubs around the world.", "Clamp Golf Company, Meet the Team"),
    "person": ("There&rsquo;s a person behind every design, every stitch and every parcel that leaves the workshop.", "Clamp Golf Company"),
    "second": ("At Clamp Golf Company, we believe some materials deserve a second life.", "Clamp Golf Company, on the Military Range"),
}

BANDS = {
    "workshop": ("Photography &middot; Clamp Golf Company&rsquo;s own", "Inside the Yorkshire workshop, where the embroidery machines run at up to 800 stitches a minute.",
             [("band-a1", "An embroidery machine stitching in the Clamp Golf Company workshop", "The embroidery machines"),
              ("band-a2", "Spools of embroidery thread on a pegboard wall in the workshop", "The thread wall"),
              ("band-a3", "Hands sewing a Clamp Golf Co. label onto a green headcover", "The label")]),
    "new": ("Photography &middot; Clamp Golf Company&rsquo;s own", "Clamp shot the Military Range in front of the flag it was made to honour.",
             [("band-b1", "A camo carry bag with Military Range headcovers in front of a Union Jack", "Military Range"),
              ("band-b2", "A black Clamp golf bag with matching black leather covers", "All black"),
              ("band-b3", "Leather headcovers embroidered Driver, 3 Wood, 7 Wood and Putter", "Word covers")]),
    "commissions": ("Photography &middot; Clamp Golf Company&rsquo;s own", "Clamp also makes covers to order for clubs and brands, and it shoots them like product launches.",
             [("band-c1", "Red Manchester United headcovers made by Clamp", "For a football club"),
              ("band-c2", "Black Pepsi headcovers made by Clamp beside Pepsi cans", "For a drinks brand"),
              ("band-c3", "Navy Cornwell's Chemists headcovers made by Clamp", "For a local business")]),
    "leather": ("Photography &middot; Clamp Golf Company&rsquo;s own", "The word covers and leather putter covers, shot in the studio.",
             [("band-d1", "White leather word covers reading Driver, 3 Wood and Hybrid", "In white"),
              ("band-d2", "Two brown leather mallet putter covers on an armchair", "Mallet covers"),
              ("band-d3", "Black leather word covers with an alignment stick cover", "In black")]),
    "tweed": ("Photography &middot; Clamp Golf Company&rsquo;s own", "Clamp has made covers for everyone from coffee roasters to the bloke with a black bag.",
             [("band-e1", "Custom black and white headcovers styled with coffee beans", "For a coffee brand"),
              ("band-e2", "A brown leather cover and bag in front of ivy", "Brown leather"),
              ("band-e3", "Black Clamp covers in a black golf bag", "Bag shot")]),
    "acc": ("Photography &middot; Clamp Golf Company&rsquo;s own", "The small stuff gets the same treatment: branded pouches and a cover with a tiger on top.",
             [("band-f1", "Black Pepsi-branded pouches made by Clamp", "Branded pouches"),
              ("band-f2", "A striped headcover with a small tiger mascot on top", "The tiger cover"),
              ("band-f3", "The striped tiger cover from closer in", "Up close")]),
}

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>The base collection is solid: Yorkshire leather, Harris Tweed, word covers, brass markers, all made to order in a small workshop at fair prices. The reworked pieces are why Clamp is on this site. Its limited line, The Vault, takes a Carhartt bag, a Nike ACG pack, a Supreme bag or an Adidas fleece and turns it into a set of headcovers with the original labels, zips, buckles and webbing still on. It is the best reworked headcover work we have seen in a while, and nobody else is doing it at this volume.</p>
    <p>Look at the sold-out list at the bottom of this page and you can see what is going on. An orange Nike hybrid with a giant swoosh, a Supreme hybrid, an ACG set with the Bigfoot patch, a beige Adidas waffle-fleece set and a Louis Vuitton set at &pound;1,200 all sold, one each, and they will not be made again. Streetwear people collect drops, and Clamp has turned headcovers into drops. If you see one you like, buy it, because the next one will be different.</p>
    <p>The collaborations go beyond fashion brands. The new Military Range is cut from decommissioned uniforms donated by Military vs Cancer, and sales fund the charity. Clamp also makes commissions for football clubs, drinks brands and the chemist down the road, and it will cut your own jersey or jacket into covers; its team lists a game-worn Kobe Bryant shirt among the jobs it remembers. For an Austin golfer, that means the old Longhorns jersey in the closet could be your driver cover.</p>
    <p>On price, the everyday covers are fair for handmade: leather drivers from about &pound;57 to &pound;75 ($77 to $100) and Harris Tweed from &pound;58 ($78), with 10% off any set of three. The reworked sets run &pound;130 to &pound;300 ($175 to $400), roughly what the original bag cost, and the LV pieces are priced like Louis Vuitton. Everything is made to order and arrives within two weeks, with a six-month warranty. The store charges US shoppers in dollars, and custom and limited pieces cannot be returned.</p>
    <h2 class="products-hdr btk-story-hdr">The Story</h2>
    <p>Clamp Golf Company is a small team in a Yorkshire workshop. Josh started it and still loves &ldquo;getting stuck into a new design,&rdquo; Ryan runs embroidery and production, Lesley has been at a sewing machine for more than 35 years, and Chloe keeps the orders moving. Their own page describes a week that swings between &ldquo;a whole collection for a golf club&rdquo; and &ldquo;one cover with a story behind it.&rdquo;</p>
    <p>Every cover is cut and sewn in-house, from genuine leather sourced in Yorkshire, faux leather, Harris Tweed and upholstery fabric, with a fleece lining and bonded nylon thread. The embroidery machines run at up to 800 stitches a minute in up to 20 colours, which is how the club crests and portraits happen. Lesley&rsquo;s most memorable custom request was turning a running shoe into a headcover.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Yorkshire, England</span></div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>2020, in a garage, by Josh</span></div>
      <div class="sidebar-detail"><span class="l">Made</span><span>To order, in-house; within 2 weeks</span></div>
      <div class="sidebar-detail"><span class="l">Deal</span><span>10% off sets of 3 or more</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>&pound;6&ndash;&pound;1,150 (~$8&ndash;$1,547)</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Carhartt Reworked Set, &pound;250 (~$336)</span></div>
      <a href="https://www.clampgolfcompany.co.uk/" target="_blank" rel="noopener" class="sidebar-cta">Visit Clamp Golf &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#ClampGolf</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#Headcovers</span>
        <span class="hashtag">#MadeInYorkshire</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

FAQ = [
    ("Where are Clamp Golf headcovers made?",
     "In Clamp Golf Company's own workshop in Yorkshire, England. Every cover is cut, sewn and embroidered in-house."),
    ("How long do Clamp Golf headcovers take?",
     "Everything is made from the point of order, and Clamp says covers arrive no later than two weeks after you order."),
    ("What are Clamp Golf's reworked headcovers?",
     "They are one-off sets cut from branded bags, coats and jerseys, including Carhartt, Nike, Adidas, Supreme, Palace, North Face and Louis Vuitton, backed with leather. Each is made once and sold through Clamp's limited line, The Vault."),
    ("Can Clamp make headcovers from my own jersey or jacket?",
     "Yes. Clamp takes commissions and reworks clothing and bags into headcovers. Its team lists a game-worn Kobe Bryant shirt and a running shoe among its most memorable custom jobs."),
    ("Does Clamp Golf offer a discount on sets?",
     "Yes, 10% off any set of three or more covers, applied automatically in the basket."),
    ("What is Clamp Golf's return policy?",
     "Returns are accepted within 16 days if unused and in original condition, with return shipping paid by the buyer. Limited edition and custom pieces cannot be returned. All purchases carry a six-month warranty."),
]


