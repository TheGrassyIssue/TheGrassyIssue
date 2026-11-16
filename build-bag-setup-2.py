#!/usr/bin/env python3
"""build-bag-setup-2.py — Golf Bag Setup Ideas, Vol. 2: six winter palettes.
16 November 2026.

Lenny: "curating-your-golf-bag-setup post preformed really well, let's do a v2 or
another similar post." Chose "Bag Setups Vol. 2": same format, six new winter
palettes, all new pieces not in Vol. 1, links both ways. Options sheet
(bag-setups-v2-options.html) approved: "looks good, let's build the post".
Where the sheet offered two options for a role, one was picked here. Swaps from
the sheet: Jones Short Course Bag (Charcoal) in place of the Trouper Moon Gray
(the Moon Gray reads pale grey, not charcoal); the Trouper Ecru moves from the
Desert Sand row to anchor Cream & Red; the Seamus copper marker was a novelty
design and was dropped; the Walker Black Sand towel is no longer on Walker's
store, so No Dirt's Valspar towel replaces it; Apres's Hello Friends driver
cover is sold out in driver size, so Goodbye Friends (same moss sherpa) is used.

Rules carried: no FAQ, American spelling, no stark white frames (restoned), no
women's items, no college-licensed images, no red-white-and-blue (Lenny, Vol. 1).

PRICES: each maker's own store on 16 Nov 2026, in its own currency. Clamp sells
in GBP and Walker in AUD; approximate USD shown beside them (GBP 0.752, AUD 0.65).
Photographs: the makers' own, from their stores. Frames in
research/bag-setup-2-frames.json, setup photographs in research/bag-setup-2-bands.json.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "golf-bag-setup-ideas-vol-2"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/bag-setup-2"
VOL1 = "/drops/curating-your-golf-bag-setup"
FR = json.loads((ROOT / "research/bag-setup-2-frames.json").read_text())
BANDS = json.loads((ROOT / "research/bag-setup-2-bands.json").read_text())

TITLE = "Golf Bag Setup Ideas, Vol. 2: Six Winter Palettes for Your Bag and Headcovers"
DESC = ("Six new golf bag setups for winter, from charcoal and camel to chocolate and sky blue: "
        "a bag, headcovers, towel and one small thing in each, all from independent makers.")
H1 = "Golf Bag Setup Ideas, Vol. 2: Six Winter Palettes"

BRAND = {"jonessportsco.com": "Jones Sports Co.", "seamusgolf.com": "Seamus Golf", "vesselgolf.com": "VESSEL",
         "www.clampgolfcompany.co.uk": "Clamp Golf Company", "nodirtgolf.com": "No Dirt Golf",
         "dormieworkshop.com": "Dormie Workshop", "apresgolf.com": "Apr&egrave;s-Golf", "sundaygolf.com": "Sunday Golf",
         "dimpledivot.com": "Dimple &amp; Divot", "www.jancraigheadcovers.com": "Jan Craig",
         "www.walkergolfthings.com": "Walker Golf Things", "pinsandaces.com": "Pins &amp; Aces", "eastsidegolf.com": "Eastside Golf", "whimgolf.com": "Whim Golf",
         "ghostgolf.com": "Ghost Golf", "malbon.com": "Malbon Golf", "metalwood.studio": "Metalwood Studio"}


def money(dom, p):
    if dom == "www.clampgolfcompany.co.uk":
        return f"&pound;{p:,} (about ${round(p / 0.752):,})"
    if dom == "www.walkergolfthings.com":
        return f"A${p:,} (about ${round(p * 0.65):,})"
    return f"${p:,}" if float(p).is_integer() else f"${p:,.2f}"


# handle -> (dom, name, price, role, copy)
P = {
 # Charcoal & Camel
 "short-course-bag-charcoal": ("jonessportsco.com", "Short Course Bag, Charcoal", 120, "The bag",
   "This is a light carry bag that takes the lines of Jones&rsquo;s Classic stand bag and the pockets of the Trouper, with a built-in cooler. Mid-gray nylon with black trim gives the palette its base without looking like a suit."),
 "charcoal-tweed-head-covers": ("seamusgolf.com", "Charcoal Harris Tweed Driver Cover", 130, "The driver",
   "It is hand-woven Harris Tweed from the Outer Hebrides in a gray herringbone with flecks of black. Same family as the bag, but the texture is what you notice."),
 "sun-day-red-x-vessel-icon-leather-driver-headcover-camel": ("vesselgolf.com", "Sun Day Red x VESSEL Leather Driver Cover, Camel", 200, "The camel",
   "This is pebble-grain leather in camel with a white chainstitched logo and a plush lining. It is the warm piece. Put it on a fairway wood next to the tweed and the bag stops looking cold."),
 "vintage-slate-copy-1": ("www.clampgolfcompany.co.uk", "Vintage Putter Cover, Slate", 71, "The putter",
   "It is a soft genuine-leather cover in slate, made in blade and mallet shapes. It is plain on purpose, because the camel cover is doing the talking."),
 "the-range-rat-grey": ("nodirtgolf.com", "The Range Rat, Dark Gray", 14.99, "The towel",
   "This is a small 16 by 12 inch microfiber towel with a stiff brush built into it. Dark gray hides a whole winter of mud, and it costs less than a sleeve of balls."),
 "rangefinder-pouch-charcoal-2": ("jonessportsco.com", "Rangefinder Pouch, Charcoal", 38, "The pouch",
   "It is a cinch-top pouch that clips on with a YKK carabiner. It matches the bag exactly, so it reads as part of it."),
 # Burgundy & Navy
 "player-v-pro-stand-merlot-by-sasha-vujacic": ("vesselgolf.com", "Player V Pro Stand, MERLOT by Sasha Vujacic", 599, "The bag",
   "This is VESSEL&rsquo;s Player V Pro stand bag in a deep wine red, a limited run inspired by Sasha Vujacic&rsquo;s Aleksander wine. It is the boldest bag on the page, so everything else stays navy."),
 "merlot-headcover-by-sasha-vujacic": ("vesselgolf.com", "MERLOT by Sasha Vujacic Driver Cover", 120, "The driver",
   "It is the matching leather driver cover with a laurel crest. Matching the bag and driver exactly is the one place this kit plays it safe."),
 "paisley-headcovers-navy": ("dormieworkshop.com", "Paisley Headcover, Navy", 180, "The pattern",
   "This is navy leather with a white paisley print, for a fairway wood or hybrid. Paisley is the one pattern in the kit."),
 "navy-tribeca-leather-blade-putter-cover": ("seamusgolf.com", "Navy Tribeca Leather Blade Cover", 140, "The putter",
   "It is navy Tribeca leather lined with gray fleece. It is the quietest piece in the kit, and the one you will look at most."),
 "the-ultimate-caddy-towel-burgundry-silver-stripes": ("nodirtgolf.com", "Ultimate Caddy Towel, Burgundy and Silver Stripes", 29.99, "The towel",
   "This is a 44 by 22 inch towel with a scrub pad built in. Burgundy with a silver stripe ties the towel back to the bag."),
 "wine-genuine-leather-range-finder-pouch": ("www.clampgolfcompany.co.uk", "Wine Leather Rangefinder Pouch", 46, "The pouch",
   "It is a genuine-leather scope pouch in wine. Leather in the same red as the bag finishes the kit."),
 # Olive & Rust
 "trouper-4-0-olive-night": ("jonessportsco.com", "Trouper, Olive Night", 340, "The bag",
   "This is the 2026 Trouper with a reinforced stand and new zippers, in a deep olive. Olive works like navy in winter: it goes with almost everything you wear."),
 "goodbye-friends-green-moss-green-sherpa-fleece-headcover-w-navy-trim": ("apresgolf.com", "Goodbye Friends Moss Green Sherpa Driver Cover", 88, "The driver",
   "It is high-loft moss green sherpa, hand-sewn in California, with a thin navy trim. Soft sherpa against the bag&rsquo;s canvas is the texture contrast."),
 "dormie-chevron-rust-hybrid-headcover": ("dormieworkshop.com", "Chevron Hybrid Cover, Rust", 150, "The hybrid",
   "This is full-grain pebbled leather in a reddish brown that Dormie says was inspired by the course at dusk. It is the rust in the palette."),
 "moss-green-sherpa-fleece-blade-putter-cover": ("apresgolf.com", "Moss Green Sherpa Blade Cover", 58, "The putter",
   "It is the same moss sherpa as the driver cover, in a blade shape with a magnetic closure."),
 "magnetic-golf-towel-midnight-green": ("sundaygolf.com", "Magnetic Golf Towel, Midnight Green", 35, "The towel",
   "This is a waffle towel in a dark green-gray that clips on with a magnet. It sits between the bag and the covers."),
 "essentials-pouch-rust": ("dimpledivot.com", "Essentials Pouch, Rust", 120, "The pouch",
   "It is a flat pouch with a Fidlock magnetic closure and a mesh interior, for a bag without many pockets. Rust here repeats the hybrid cover."),
 # Desert Sand
 "ranger-sage-premium-stand-bag": ("sundaygolf.com", "Ranger Premium Stand Bag, Sage", 400, "The bag",
   "This is Sunday&rsquo;s premium stand bag in a dusty sage, with an orange lining you only see when you open the pockets. It is the base for a pale, sun-faded kit."),
 "shaka-barrel-driver-headcover-bone": ("dormieworkshop.com", "Shaka Barrel Driver Cover, Bone", 170, "The driver",
   "It is a bone leather barrel cover with a blue shaka glove on the side and a baby blue floral top. It is the playful piece, and the blue is soft enough to sit with sage."),
 "sage-waxed-canvas-mallet-putter-cover": ("seamusgolf.com", "Countryman Waxed Canvas Mallet Cover, Sage", 120, "The putter",
   "This is a tan waxed canvas top on a chocolate leather base, with a magnetic closure. Waxed canvas looks better faded, which suits this palette."),
 "the-ultimate-caddy-towel-vaspar": ("nodirtgolf.com", "Ultimate Caddy Towel, Valspar and Cream Stripes", 29.99, "The towel",
   "It is the same 44 by 22 inch caddy towel in a gray sage with a cream stripe, close to the bag without matching it."),
 "rangefinder-pouch-bone-cedar": ("jonessportsco.com", "Rangefinder Pouch, Bone/Cedar", 38, "The pouch",
   "This is a bone pouch with a darker cedar trim that clips on with a carabiner. It picks up the bone driver cover."),
 # Cream & Red
 "trouper-4-0-ecru": ("jonessportsco.com", "Trouper, Ecru", 395, "The bag",
   "This is the 2026 Trouper in ecru with brown leather trim. A cream bag is the canvas; the red goes on top."),
 "red-white-driver-headcover-1-stripe-large-pom-copy": ("www.jancraigheadcovers.com", "Red and White Driver Cover, One Stripe, Large Pom", 84, "The driver",
   "It is a hand-knit wool cover made in the USA, red with one white stripe and a big pom. It is the most obvious red in the bag, and the most fun."),
 "dancing-kooka-leather-blade-cover": ("www.walkergolfthings.com", "Dancing Kooka Leather Blade Cover, Cream / Pinot", 90, "The putter",
   "This is cream leather embroidered with small dancing kookaburras, lined in a deep red velvet. The red only shows when you take it off."),
 "the-ultimate-caddy-towel-white-red-stripe": ("nodirtgolf.com", "Ultimate Caddy Towel, White and Red Stripe", 29.99, "The towel",
   "It is the caddy towel in white with a thin red stripe, which is about as much red as a towel needs."),
 "red-genuine-leather-range-finder-pouch": ("www.clampgolfcompany.co.uk", "Red Leather Rangefinder Pouch", 46, "The pouch",
   "This is a genuine-leather scope pouch in red. Hang it on the cream bag and it does the same job as a ribbon on a box."),
 "red-party-cup-ball-marker": ("pinsandaces.com", "Red Party Cup Ball Marker", 11.96, "The marker",
   "It is a heavy enamel marker shaped like a red party cup, and it sticks to any magnetic surface. It is the joke in the bag."),
 # Chocolate & Sky
 "brown-patchwork-genuine-leather-golf-bag": ("www.clampgolfcompany.co.uk", "Brown Patchwork Genuine Leather Golf Bag", 800, "The bag",
   "This is a handmade leather carry bag in a brown and cream check. It is the most expensive thing here and the only pattern, so the rest of the kit is plain."),
 "brown-tribeca-suede": ("seamusgolf.com", "Brown Suede Leather Driver Cover", 140, "The driver",
   "It is a plain barrel cover in soft brown suede. Seamus calls it a cover for players who let their game do the talking."),
 "dormie-cocoa-chevron-mallet-putter-cover": ("dormieworkshop.com", "Chevron Mallet Cover, Cocoa", 150, "The putter",
   "This is dark brown full-grain leather with an embossed chevron. Dormie describes the color as vintage leather armchairs, which is about right."),
 "the-ultimate-caddy-towel-baby-blue-white-stripes": ("nodirtgolf.com", "Ultimate Caddy Towel, Baby Blue and Cream Stripes", 29.99, "The towel",
   "It is the caddy towel in a pale blue with a cream stripe. This is where the sky comes in."),
 "tiffany-blue-zip-pouch": ("seamusgolf.com", "Tiffany Blue Zippered Pouch", 125, "The pouch",
   "This is a small-run leather pouch in a bright robin&rsquo;s-egg blue with solid brass hardware and a leather pull. It is the one hit of strong color in the kit."),
 "dormie-cocoa-yardage-book": ("dormieworkshop.com", "Chevron Yardage Book Cover, Cocoa", 110, "The yardage book",
   "It is a handmade leather yardage book cover in the same cocoa as the putter cover. It lives in your back pocket, which is where brown leather looks best."),
 "anvil-hat-gray": ("seamusgolf.com", "Anvil Hat, Gray", 48, "The hat",
   "A classic gray cap with Seamus&rsquo;s leather Anvil patch on the front. The tan leather patch is a small dose of camel, right where people look."),
 "vessel-lux-golf-glove-grey": ("vesselgolf.com", "Lux Golf Glove, Gray", 31, "The glove",
   "This is AAA cabretta leather with a perforated finger and an embossed pull tab, in a soft gray that matches the bag rather than the usual white."),
 "ec2200801-608-cranberry-knit-beanie": ("eastsidegolf.com", "Cranberry Knit Beanie", 55, "The beanie",
   "A short cuffed knit beanie in cranberry, about the same red as the bag. It is the first thing to put on for an 8 a.m. tee time."),
 "featherweight-merino-golf-sock-1": ("whimgolf.com", "Featherweight Merino Golf Sock, Navy", 39, "The socks",
   "Navy socks knit in North Carolina from American merino, light and breathable. Navy at the ankle keeps the burgundy up top."),
 "d-d-icon-dad-hat-olive": ("dimpledivot.com", "Icon Dad Hat, Olive", 35, "The hat",
   "A washed, unstructured cotton cap in olive. It has a small orange tab on the side that matches the rust pouch from the same maker."),
 "mossgrove-reversible-woven-belt": ("pinsandaces.com", "Mossgrove Reversible Woven Belt", 39.96, "The belt",
   "A stretch woven belt in moss green with olive leather tips. It reverses, so it works with whatever pants you wear."),
 "seamus-golf-beanie-speckled-loden": ("seamusgolf.com", "Golf Beanie, Speckled Loden", 40, "The beanie",
   "A wide-rib merino blend beanie in a speckled oatmeal. It is the color of the desert at 7 a.m., which is when you will want it."),
 "sand-golf-glove-mens": ("ghostgolf.com", "Golf Glove, Sand", 32, "The glove",
   "This is AAA cabretta leather in sand, with Ghost&rsquo;s rubber logo and pull tab. A sand glove instead of a white one is the quiet finishing touch here."),
 "m-chain-stitch-snapback-crimson-red": ("malbon.com", "M Chain Stitch Snapback, Crimson Red", 48, "The hat",
   "A low-profile red snapback with a raised cream chainstitch M. It puts the red where it is most visible, which is the point of this kit."),
 "mountain-sock-ivory-scarlet": ("malbon.com", "Mountain Sock, Ivory/Scarlet", 28, "The socks",
   "Ivory mid-calf socks with a scarlet heel and toe. Red at the ankle is a nice surprise when you take your shoes off."),
 "mountain-beanie-ivory": ("malbon.com", "Mountain Beanie, Ivory", 48, "The beanie",
   "A cuffed cream beanie with a chenille M in pale sky blue. It brings the blue up from the towel and pouch."),
 "phillips-head-leather-belt-brown": ("metalwood.studio", "Phillips Head Leather Belt, Brown", 138, "The belt",
   "Smooth brown calf leather with small Phillips-head screw studs. It is the brown leather from the bag, worn."),
}

PROSE = 'style="max-width:760px;font-size:16px;line-height:1.7;margin:0 auto 36px;"'

KITS = [
 ("Charcoal &amp; Camel", "charcoal-and-camel", ["#4b4d50", "#b5895a", "#ece6da"], ["Charcoal", "Camel", "Cream"],
  "Gray does the work, camel warms it up.",
  ["This is the easiest palette for winter, because it is already what most people wear when it is cold: gray layers, a camel coat, a cream knit. On a bag it looks calm and grown-up, and it hides mud better than anything on the first page.",
   "The risk is that gray goes flat. The fix is texture and one warm color. Tweed on the driver, smooth leather on the putter, nylon on the bag, and a single camel leather cover in between. Keep the camel to one piece, or it turns into a brown bag.",
   "<strong>Our pick</strong> is the Seamus Charcoal Harris Tweed driver cover at $130. It is the piece that makes a gray bag look chosen, and it will work on whatever bag you carry next."],
  ["short-course-bag-charcoal", "charcoal-tweed-head-covers", "sun-day-red-x-vessel-icon-leather-driver-headcover-camel", "vintage-slate-copy-1", "the-range-rat-grey", "rangefinder-pouch-charcoal-2", "anvil-hat-gray", "vessel-lux-golf-glove-grey"]),
 ("Burgundy &amp; Navy", "burgundy-and-navy", ["#5b1f2a", "#1d2a44", "#b9bcc0"], ["Burgundy", "Navy", "Silver"],
  "The colors of an old club tie.",
  ["Burgundy and navy is a winter palette with a bit of ceremony in it. It looks right in a cold parking lot at 8 a.m. and it looks right in the bar after. The two colors are close in depth, so neither one shouts.",
   "Here the bag carries the burgundy, so the rest leans navy. One pattern, the Dormie paisley, sits on a fairway wood. Silver stays small: a towel stripe and the hardware. If you would rather a navy bag, flip it and keep the burgundy to the covers.",
   "<strong>Our pick</strong> is the Seamus Navy Tribeca blade cover at $140. It is plain navy leather on gray fleece, and it works in any bag on this page."],
  ["player-v-pro-stand-merlot-by-sasha-vujacic", "merlot-headcover-by-sasha-vujacic", "paisley-headcovers-navy", "navy-tribeca-leather-blade-putter-cover", "the-ultimate-caddy-towel-burgundry-silver-stripes", "wine-genuine-leather-range-finder-pouch", "ec2200801-608-cranberry-knit-beanie", "featherweight-merino-golf-sock-1"]),
 ("Olive &amp; Rust", "olive-and-rust", ["#4f5a3a", "#a5532e", "#2f3a33"], ["Olive", "Rust", "Pine"],
  "Olive in the big pieces, rust in the details.",
  ["This is an autumn palette that holds up all winter. Olive is a field color and reads as a neutral on the course, and rust is the color of the leaves that are still on the ground in December. Together they look outdoorsy without looking like hunting gear.",
   "Keep olive to the large, soft things: the bag and two sherpa covers. Then use rust twice, once in leather and once in canvas, so it reads as a decision. The towel sits in between, a dark green-gray that ties both together.",
   "<strong>Our pick</strong> is the Dormie Chevron hybrid cover in Rust at $150. Pebbled leather in that color gets better with every wet round, and it is the one piece that makes this kit."],
  ["trouper-4-0-olive-night", "goodbye-friends-green-moss-green-sherpa-fleece-headcover-w-navy-trim", "dormie-chevron-rust-hybrid-headcover", "moss-green-sherpa-fleece-blade-putter-cover", "magnetic-golf-towel-midnight-green", "essentials-pouch-rust", "d-d-icon-dad-hat-olive", "mossgrove-reversible-woven-belt"]),
 ("Desert Sand", "desert-sand", ["#d8c7a6", "#9aa58b", "#4a3326"], ["Sand", "Sage", "Chocolate"],
  "For the winter golf trip somewhere warm.",
  ["Not every winter round is cold. This is the bag for the trip to Arizona or Palm Springs: pale, soft and a little dusty, the colors of a course in the desert in January.",
   "Sage carries the bag, sand and bone carry the covers, and chocolate shows up once, on the base of the putter cover. The shaka cover brings a little baby blue, which works because it is soft. Anything brighter would break the sun-faded look.",
   "<strong>Our pick</strong> is the Seamus Countryman waxed canvas mallet cover at $120. Waxed canvas over chocolate leather is the whole palette in one piece, and it will look better the more faded it gets."],
  ["ranger-sage-premium-stand-bag", "shaka-barrel-driver-headcover-bone", "sage-waxed-canvas-mallet-putter-cover", "the-ultimate-caddy-towel-vaspar", "rangefinder-pouch-bone-cedar", "seamus-golf-beanie-speckled-loden", "sand-golf-glove-mens"]),
 ("Cream &amp; Red", "cream-and-red", ["#efe7d6", "#b3242b", "#4a3326"], ["Cream", "Red", "Brown"],
  "The holiday bag. Mostly cream, with red used like a ribbon.",
  ["This is the most festive setup on the page, and it works because it is mostly cream. A cream bag with brown leather trim is a calm base. The red goes on top in small amounts, the way you would wrap a present.",
   "Use red three or four times, never on anything large. A knit pom on the driver, a velvet lining you only see when the putter cover comes off, a stripe on the towel and a leather pouch. Keep blue to the flecks in the pom, or the bag starts to look like a flag.",
   "<strong>Our pick</strong> is the Jan Craig red and white knit driver cover at $84. It is hand-knit wool made in the USA, it is the cheapest way into this kit, and it says winter more than anything else in this post."],
  ["trouper-4-0-ecru", "red-white-driver-headcover-1-stripe-large-pom-copy", "dancing-kooka-leather-blade-cover", "the-ultimate-caddy-towel-white-red-stripe", "red-genuine-leather-range-finder-pouch", "red-party-cup-ball-marker", "m-chain-stitch-snapback-crimson-red", "mountain-sock-ivory-scarlet"]),
 ("Chocolate &amp; Sky", "chocolate-and-sky", ["#4a2f22", "#9fc9dd", "#efe7d6"], ["Chocolate", "Sky", "Cream"],
  "Brown leather and one hit of pale blue.",
  ["Brown and pale blue is an old pairing, the colors of a leather armchair and a winter sky. It is warmer than black and white and less expected than navy, and on a golf bag it looks like something you inherited.",
   "Keep the browns in leather and suede, and in two or three shades so it has depth. Then put the blue in exactly two places: a towel and a small pouch. The bag carries the only pattern, a brown and cream check, so everything else stays plain.",
   "<strong>Our pick</strong> is the Seamus Tiffany Blue zippered pouch at $125. It is the piece that turns a brown bag into this palette, and it is as useful off the course as on it."],
  ["brown-patchwork-genuine-leather-golf-bag", "brown-tribeca-suede", "dormie-cocoa-chevron-mallet-putter-cover", "the-ultimate-caddy-towel-baby-blue-white-stripes", "tiffany-blue-zip-pouch", "dormie-cocoa-yardage-book", "mountain-beanie-ivory", "phillips-head-leather-belt-brown"]),
]
PICKS = {"charcoal-tweed-head-covers", "navy-tribeca-leather-blade-putter-cover", "dormie-chevron-rust-hybrid-headcover",
         "sage-waxed-canvas-mallet-putter-cover", "red-white-driver-headcover-1-stripe-large-pom-copy", "tiffany-blue-zip-pouch"}
N = sum(len(k[6]) for k in KITS)
MAKERS = sorted({P[h][0] for k in KITS for h in k[6]})

TAKE = f"""
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>The first volume of <a href="{VOL1}">Golf Bag Setup Ideas</a> was about the basics: pick three colors, use one pattern, and let texture do the work. This one is the same idea for the colder months. Winter changes what you wear, so it should change the bag too.</p>
    <p>Here are six new palettes, each a complete setup from independent makers: a bag, the covers, a towel, one small thing and two things to wear. None of these {N} pieces appeared in Vol. 1. Each setup opens with photographs of the palette in use, then the pieces themselves.</p>
    <p>If you only buy one thing this winter, buy a cover. It is the cheapest way to change the whole mood of a bag you already own.</p>
    <h2 class="products-hdr btk-story-hdr">The Rules, Quickly</h2>
    <p><strong>Sixty, thirty, ten.</strong> One color takes most of the bag, a second takes the covers, and a third shows up only in small things.</p>
    <p><strong>One pattern per bag.</strong> Tweed, paisley, check or a printed cover. Pick one and keep the rest plain.</p>
    <p><strong>Contrast texture.</strong> In winter this is easy: tweed, suede, sherpa and waxed canvas next to leather and nylon.</p>
    <p><strong>Warm it up.</strong> Winter palettes go flat fast. Add one warm color, such as camel, rust or red, in leather.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Setups</span><span>Six, for winter</span></div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>{N}, from {len(MAKERS)} makers</span></div>
      <div class="sidebar-detail"><span class="l">The rule</span><span>Three colors, one pattern</span></div>
      <div class="sidebar-detail"><span class="l">Easiest start</span><span>Charcoal &amp; camel</span></div>
      <div class="sidebar-detail"><span class="l">Vol. 1</span><span><a href="{VOL1}">Six more setups</a></span></div>
      <div class="sidebar-detail"><span class="l">Prices read</span><span>November 16, 2026</span></div>
      <a href="#charcoal-and-camel" class="sidebar-cta">See the setups &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#BagSetup</span>
        <span class="hashtag">#WhatsInTheBag</span>
        <span class="hashtag">#Headcovers</span>
        <span class="hashtag">#WinterGolf</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

NOTE = f"""
<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr" id="how-we-picked">How We Picked</h2>
  <div {PROSE}>
    <p style="margin:0 0 16px;">We started from the six palettes in <a href="{VOL1}">Vol. 1</a> and looked for the ones it left out, especially colors that suit cold, gray days. Then we went through the stores of the independent makers we cover and built each setup piece by piece, mixing brands freely. Every photograph comes from the maker&rsquo;s own store.</p>
    <p style="margin:0 0 16px;">Every piece was in stock when we checked. Prices come from each maker&rsquo;s own store on November 16, 2026, in its own currency. Clamp Golf Company sells from the UK in pounds and Walker Golf Things from Australia in Australian dollars, so we show an approximate US price beside them; everything else is in US dollars. For the bags themselves, see <a href="/drops/upgrading-your-golf-bag">Upgrading Your Golf Bag</a>.</p>
  </div>
</section>
"""


def card(h, idx):
    dom, name, p, role, copy = P[h]
    fr = [f["local"] for f in FR[h]]
    label = H.unescape(f"{BRAND[dom]} {name}").replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>'
                   for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>'
                   for j in range(len(fr)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{"&#9733; Our pick &middot; " if h in PICKS else ""}{BRAND[dom]} &middot; {role}</div>'
            f'<div class="product-name">{name} &middot; {money(dom, p)}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="https://{dom}/products/{h}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


def swatches(cols, names):
    s = "".join(f'<span style="display:inline-flex;flex-direction:column;align-items:center;gap:8px;margin:0 14px;">'
                f'<span style="display:block;width:76px;height:76px;border-radius:50%;background:{c};border:1px solid rgba(0,0,0,.12);"></span>'
                f'<span style="font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;opacity:.75;">{n}</span></span>'
                for c, n in zip(cols, names))
    return f'<div style="display:flex;justify-content:center;margin:10px 0 28px;">{s}</div>'


IMGSTY = 'style="width:100%;aspect-ratio:4/5;object-fit:cover;display:block;background:#e8e2d6;"'


def fig(x):
    b = BRAND.get(x["dom"], x["dom"])
    alt = H.escape(H.unescape(b) + " photograph: " + x["handle"].replace("-", " "))
    return (f'<figure style="margin:0;"><img src="{x["local"]}" alt="{alt}" loading="lazy" {IMGSTY} />'
            f'<figcaption class="ig-cap">{b}</figcaption></figure>')


def grid(items, minw):
    return (f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax({minw}px,1fr));gap:14px;max-width:1180px;margin:0 auto 26px;">'
            + "".join(fig(x) for x in items) + '</div>')


def mood():
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">The Mood</div>\n'
            f'  <h2 class="products-hdr" id="the-mood">Bags for Cold Mornings</h2>\n'
            f'  <p class="cat-kicker"><strong>Before the setups</strong>Leather, canvas and tweed, the textures that suit winter.</p>\n'
            f'  {grid(BANDS["mood"], 240)}\n</section>\n')


def kit(i, k, n0):
    name, anchor, cols, names, kicker, paras, ids = k
    band = BANDS[anchor]
    makers = []
    for x in band:
        b = BRAND.get(x["dom"], x["dom"])
        if b not in makers:
            makers.append(b)
    credit = ", ".join(makers[:-1]) + " and " + makers[-1] if len(makers) > 1 else makers[0]
    prose = "\n".join(f'    <p style="margin:0 0 16px;">{p}</p>' for p in paras)
    cards = "\n".join(card(h, n0 + j) for j, h in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">Setup {i}</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{name}</h2>\n'
            f'  <p class="cat-kicker"><strong>{" &middot; ".join(names)}</strong>{kicker}</p>\n'
            f'  {grid(band[:2], 320)}\n'
            f'  {swatches(cols, names)}\n'
            f'  <div {PROSE}>\n{prose}\n  </div>\n'
            f'  {grid(band[2:], 200)}\n'
            f'  <p class="cat-kicker"><strong>The pieces</strong>The photographs come from {credit.rstrip(".")}. The {len(ids)} pieces below were all in stock when we checked.</p>\n'
            f'    <div class="products-grid">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items, pos = [], 1
    for k in KITS:
        for h in k[6]:
            items.append({"@type": "ListItem", "position": pos, "url": f"https://{P[h][0]}/products/{h}", "name": H.unescape(f"{BRAND[P[h][0]]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-11-16", "dateModified": "2026-11-16",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": items},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Drops & Brands", "item": "https://thegrassyissue.com/#feed"},
            {"@type": "ListItem", "position": 3, "name": "Golf Bag Setup Ideas, Vol. 2", "item": URL}]},
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


def main(apply_):
    ids = [h for k in KITS for h in k[6]]
    assert len(ids) == len(set(ids)) and set(ids) == set(P), set(P) ^ set(ids)
    for h in ids:
        assert FR.get(h), h
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Golf Bag Setup Ideas, Vol. 2</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>A guide to the winter bag</span><span class="dot"></span>
    <span>6 setups &middot; {N} pieces</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A golfer beside a gray Jones stand bag with black and cream sherpa headcovers on a dry winter course" fetchpriority="high" /></div></div>
"""
    body += TAKE + mood()
    n = 1
    for i, k in enumerate(KITS, 1):
        s, n = kit(i, k, n)
        body += s
    body += NOTE
    out = head_top() + head_rest + body + tail
    print(f"  {n-1} cards, {len(MAKERS)} makers")
    if not apply_:
        print("  dry run — pass --apply")
        return
    OUT.write_text(out, encoding="utf-8")
    verify()


def verify():
    fin = OUT.read_text(encoding="utf-8")
    bad = []
    above = re.sub(r"<style\b.*?</style>|<script\b.*?</script>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    text = re.sub(r"<[^>]+>", " ", above)
    if fin.count('class="product-card"') != N:
        bad.append("card count")
    for w in ("worth", "genuinely", "honestly", "straightforward", "selling out", "colour", "favourite", "grey"):
        if re.search(rf"\b{w}", text, re.I):
            bad.append(f"banned/British word: {w}")
    if re.search(r'class="faq', above) or "FAQPage" in fin:
        bad.append("FAQ present")
    if VOL1 not in above:
        bad.append("no link to Vol. 1")
    vol1 = (ROOT / f"drops/curating-your-golf-bag-setup.html").read_text(encoding="utf-8")
    for h in P:
        if f"/products/{h}" in vol1:
            bad.append(f"{h} already in Vol. 1")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file():
            bad.append(f"missing {f}")
    if bad:
        OUT.unlink()
        sys.exit("! removed. " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
