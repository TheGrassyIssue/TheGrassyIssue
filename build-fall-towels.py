#!/usr/bin/env python3
"""build-fall-towels.py — The Ultimate Fall Golf Towel Roundup: 50 towels, 50 brands.
25 September 2026.

Lenny: "let's do the ultimate golf towel round up going into Fall- 50 towels".
He saw an 89-option grid from 56 brands (towel-options-2026-09-25.html), asked
for new Malbon/Sentinel/Students/Fyfe options, then said "go with your
suggested cuts" (Bunker Mentality, Swannies, Stitch, Sinking Birdies, Clutch,
Garsen). Two changes after that, both reported to him:
  * Mogshade came OUT: its US storefront shows the Contour towel sold out at
    $65 (only the EU store has it, at EUR 39). Clutch came back IN as #50.
  * Students and Fyfe sell no towels today, so neither is here.

SHELL: drops/brand-to-know-manors.html, same as build-fall-drops.py.

DATA: research/towels/picks.json. Prices and stock read 25 Sep 2026 from each
brand's own store. USD wherever the store offers a US price; 3 Putt Round
(EUR) and Birds of Condor (AUD, US store behind a bot wall) are shown in their
own currency and labelled, never converted.

QUOTES: none. Lenny, 25 Sep: "No quotes on this post".

HERO: Sunday Golf's own photograph from its golf-towels collection page
(1920x1213): a golfer with a stack of their towels over his shoulders. Lenny
picked it ("top left works") from an eight-option sheet after rejecting four.

Writes drops/fall-golf-towel-roundup-2026.html. No feed card; that waits for
Lenny. Dry run by default.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "fall-golf-towel-roundup-2026"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/fall-towels-2026"
P = {p["id"]: p for p in json.loads((ROOT / "research/towels/picks.json").read_text())}
READ = "25 September 2026"

TITLE = "50 Golf Towels for Fall 2026, From 50 Independent Brands"
DESC = ("The ultimate fall golf towel roundup: 50 towels from 50 independent golf brands, "
        "from $13 to $57. Knits, chenille, jacquard, magnets and a few jokes. "
        "Prices checked 25 September 2026.")
H1 = "The Ultimate Fall Golf Towel Roundup &mdash; 50 Towels, 50 Independent Brands"

# id -> (brand display, detail line, product name, price override, card copy)
# price override: None = use USD from picks.json; or a display string for non-USD stores.
C = {
 # ---- Heavy, dark and built for fall
 "T87": ("Malbon", "Microfiber &middot; Forest", "Malbon Golf Towel", None,
         "Malbon&rsquo;s script M runs the full length of this deep forest-green microfiber towel. It has a metal eyelet and carabiner, and it has never been in a TGI post before."),
 "T13": ("Devereux", "Knitted cotton &middot; Black", "Knitted Cactus Voodoo Towel", None,
         "The Cactus Voodoo graphic is knitted in, not printed, in gold on black cotton. It is the heaviest-feeling towel in this section and the most fun to look at."),
 "T15": ("Dormie Workshop", "Terry &middot; 22&Prime; &times; 44&Prime;", "Signature Player&rsquo;s Towel, Black", None,
         "Dormie makes this full tour-size towel in cotton terry with a little polyester, finished with a quiet grey stripe and the Dormie script. Of its six colourways, the black is the one we would pick for fall."),
 "T30": ("Jones Sports Co.", "Reversible &middot; Black", "Rain Hood Towel", None,
         "One side is water-resistant, so it drapes over your clubs as a hood when the weather turns. Flip it over and it is a normal towel again. It is the most useful towel here for a wet November."),
 "T51": ("Hidden Links Society", "Chenille &middot; 100% cotton", "Bud Chenille Caddie Towel, Black", None,
         "Hidden Links weaves this black caddie towel from ringspun cotton and sews a chenille Bud patch in one corner. The brand calls it the OG caddie towel."),
 "T84": ("Sentinel", "Organic cotton gauze &middot; Made in Japan", "Shinto Gauze Towel, Charcoal", None,
         "Made by Shinto in Japan from 2.5-ply organic cotton gauze, so it feels light and substantial at once. It is slimmer than a normal bag towel, so it slides under the handle when you carry."),
 "T16": ("Edel Golf", "Ribbed cotton &middot; 21.5&Prime; &times; 42&Prime;", "Retro Caddy Towel, Navy", None,
         "Edel puts its embroidered wings on an oversized ribbed-cotton caddy towel with retro striping. It is made for Edel by PRG."),
 "T33": ("Galvin Green", "Tri-fold &middot; Black", "Theo Golf Towel", None,
         "A compact tri-fold with an embroidered logo and a built-in hook. It is the tidiest towel in the post, from the Swedish family firm we made a Brand to Know this month."),
 "T37": ("PXG", "Waffle microfiber &middot; Grey", "Darkness Repeat Player&rsquo;s Towel", None,
         "The Darkness skull repeats across both sides in grey on grey, so it reads as a texture until you look closely. A woven loop holds it to the bag."),
 "T07": ("Bettinardi", "Navy &middot; Limited", "VDF Navy Towel", None,
         "A grey pattern taken from Bettinardi&rsquo;s variable-depth fly-milled putter faces, over navy, with the wordmark on both sides. Stock is limited."),
 "T48": ("SWAG Golf", "Waffle microfiber &middot; 16&Prime; &times; 40&Prime;", "Black Melting Skull Towel", None,
         "SWAG runs its melting skull in a blackout drip over a grey base. It is the brand&rsquo;s best-known graphic done in the quietest way we have seen it."),
 "T62": ("Sunday Golf", "Magnetic &middot; Black", "Magnetic Golf Towel", None,
         "This black waffle towel has a magnet that snaps onto a Sunday Loma bag, a cart post or a clubhead."),
 "T50": ("Walker Golf Things", "Cotton velour &middot; 16.5&Prime; &times; 33&Prime;", "Kooka Icon Tour Towel", None,
         "A 490gsm cotton velour tour towel with Walker&rsquo;s kookaburra knitted in as a jacquard. Walker&rsquo;s Kooka towel has run here before; this is the white-and-pine jacquard, from the Gold Coast label started by the pro skater Jack Fardell."),
 "T67": ("Palm Golf", "Ribbed cotton &middot; 42&Prime; &times; 19&Prime;", "Wanderer Caddie Towel", None,
         "Palm cuts a centre slit in this charcoal ribbed caddie towel so it drapes over a club. Palm pitches it at purists, and it looks the part."),
 "T53": ("Local Rule", "Microfiber and cotton &middot; Dark Green", "Iron Logo Towel", None,
         "Local Rule puts microfiber on the front for the dirt and soft cotton on the back for drying. It is the Stockholm label at its most understated."),
 "T52": ("Hiroki Golf", "Waffle microfiber &middot; 56 &times; 100cm", "Hiroki Golf Towel, Green", None,
         "Hiroki prints its bold graphic in green and cream on a large caddy-size waffle towel. We have run the grey one before; the green suits the season better. Hiroki is from Auckland."),
 "T77": ("The Fried Egg", "Terry &middot; 44&Prime; &times; 22&Prime;", "Fried Egg Golf Towel, Green", None,
         "The golf-architecture site and podcast puts its Fried Egg Golf script on a classic green tour towel."),
 "T11": ("Clutch Golf Co.", "Cotton &middot; 44&Prime; &times; 22&Prime;", "Classic Tour Caddie Towel", None,
         "Clutch makes a plain white caddie towel with hunter-green stripes that is as big as a beach towel. At $12.95 it is the least expensive towel in the post."),
 # ---- Jacquard, plaid and pattern
 "T43": ("Seamus", "Cotton jacquard &middot; Leather loop", "Chief Joseph Aqua Jacquard Towel", None,
         "The Chief Joseph pattern woven in aqua cotton, finished with a riveted leather loop and the Seamus monogram. Seamus recommends hand washing because of the leather."),
 "T83": ("Manors", "Gentleman Jack collab", "Gentleman Jack &times; Manors Paisley Towel", None,
         "This towel comes from the Manors and Gentleman Jack capsule and carries the same paisley as the capsule&rsquo;s polos. It is the most dressed-up towel in the post."),
 "T79": ("Shoal", "Tour size &middot; Built-in scrub pad", "Shoal &times; No Dirt Caddie Towel, Olive", None,
         "An olive caddie towel with cream stripes and a non-abrasive scrub pad built into one end, so there is no need for a separate brush."),
 "T64": ("Good Good", "Jacquard", "Born To Golf Jacquard Towel", None,
         "Good Good weaves GOOD in big green varsity letters into a cream jacquard. It is the most classic-looking thing the YouTube crew makes."),
 "T41": ("Rouqe Golf", "Cotton jacquard", "RQ Jacquard Towel", None,
         "Rouqe weaves its RQ monogram into a black and white cotton jacquard and includes the clip. At $14 it is the least expensive jacquard here."),
 "T69": ("Stick Grips", "Waffle &middot; 23.6&Prime; &times; 15.75&Prime;", "Camo Golf Towel", None,
         "Stick Grips prints a grey duck camo on a waffle towel and hangs it from a steel carabiner. It suits the season without being loud about it."),
 "T25": ("Ghost Golf", "Microfiber waffle &middot; 18&Prime; &times; 40&Prime;", "Tour Towel (Caddie), Camo", None,
         "Ghost&rsquo;s full caddie-size tour towel in camo, with a deep waffle weave. The brand says it holds up to 400% of its weight in water."),
 "T61": ("Sugarloaf Social Club", "Made in the USA &middot; 34&Prime; &times; 60&Prime;", "The Tour Towel", None,
         "Green and white stripes, made in the USA with the women&rsquo;s brand Byrdie Golf. At 34 by 60 inches it is the biggest towel in the post, and the brand shot it on a beach."),
 "T40": ("Ripit", "100% cotton &middot; 16&Prime; &times; 36&Prime;", "Check Golf Towel", None,
         "Todd Watts&rsquo;s Australian art-grip brand makes this one in pink, orange and green checks. Ripit warns that it may be too nice to get dirty."),
 "T20": ("Forden Golf", "Microfiber &middot; 40 &times; 100cm", "Green Swingman Golf Towel", None,
         "A dark green microfiber towel scattered with Forden&rsquo;s Swingman, a logo taken from Doc Edgerton&rsquo;s 1938 strobe photograph of a golf swing at MIT. At $13.30 it is the second least expensive towel here."),
 "T01": ("3 Putt Round", "Microfiber &middot; 50 &times; 100cm", "&ldquo;It&rsquo;s Always Tee Time&rdquo; Tour Towel", "&euro;29",
         "The Milan brand prints the slogan on one side and a green check on the other, with a fabric handle to hang it. It is sold in euros only."),
 "T38": ("Radry Golf", "Cotton jacquard &middot; 16&Prime; &times; 38&Prime;", "The Animals Got Out Again Towel", None,
         "Radry has woven its animals across a 550gsm jacquard in grey and black. It has no hole or clip; it is made to drape over the clubs."),
 # ---- Loud on purpose
 "T09": ("Birds of Condor", "Waffle microfiber &middot; 39&Prime; &times; 14&Prime;", "Hellfire Golf Club Towel", "A$29.95",
         "From Birds of Condor&rsquo;s Stranger Things collection: &ldquo;Birdies, bogeys, dungeons &amp; dragons.&rdquo; A Hellfire Club print with a centre slit to hang it. Price is from the Australian store, in Australian dollars."),
 "T35": ("OKKA Golf", "Waffle microfiber &middot; Magnet", "Mister Chippa Golf Towel", None,
         "A pink sunburst starring the Mister Chippa character, printed on both sides, from the one-person Perth label. It has a carabiner and a magnet, and each one comes with a free donut ball marker."),
 "T18": ("Foray Golf", "Cotton velour &middot; Made in the USA", "Bogey Monster Golf Towel", None,
         "A white velour towel with Foray&rsquo;s Bogey Monster woven in black, made in the USA. It is small, at 16 by 19 inches."),
 "T27": ("Golf Gods", "Waffle microfiber &middot; Magnet", "Stickman Golf Towel", None,
         "A pastel stick-figure print on the front and a black and white block pattern on the back, with a magnet to hold it on."),
 "T81": ("Sunday Swagger", "Microfiber", "Tequila Time Golf Towel", None,
         "Sunday Swagger prints limes and tequila glasses on white and trims it in lime green. The brand&rsquo;s own words: for rounds that come with a side of bad decisions."),
 "T75": ("No Laying Up", "Velour &middot; 42&Prime; &times; 22&Prime;", "Logo Towel, Green &amp; Black", None,
         "The classic NLU repeat print in green and black. There is no clip, on purpose: it is a big velour towel meant to be draped."),
 "T85": ("USAG", "Waffle microfiber &middot; 15&Prime; &times; 25&Prime;", "Tour Championship Towel", None,
         "A fake newspaper front page, &ldquo;Golf Times Weekly&rdquo;, printed on a waffle towel. It is the best joke in the post."),
 "T04": ("Apr&egrave;s Golf", "Woven jacquard &middot; 500gsm", "&ldquo;I will not Apr&egrave;s-Golf.&rdquo; Towel", None,
         "One line, woven over and over like lines on a school blackboard, in blue on cream. It is plush, heavy cotton with a centre hang loop."),
 "T56": ("Vice Golf", "Microfiber &middot; Extra large", "Outer Space Towel", None,
         "A big microfiber towel with Vice&rsquo;s script in lime on a dark ground, large enough to use part wet and part dry."),
 "T55": ("Stix Golf", "Microfiber &middot; Carabiner", "Nicklaus Golf Towel", None,
         "Stix puts Jack Nicklaus&rsquo;s signature and a Golden Bear on this one, from its Nicklaus partnership. It clips to a bag, belt loop or cart."),
 "T17": ("Evnroll", "Cotton &middot; 42&Prime; &times; 21.5&Prime;", "Evnroll Retro Towel", None,
         "Evnroll gives a white cotton towel a red retro stripe and its Putters logo."),
 "T05": ("BestGrips", "Microfiber &middot; 22&Prime; &times; 40&Prime;", "BestGrips Players Towel", None,
         "Made with Players Towel, in BestGrips&rsquo; black and white. It has a putter slit, so it is harder to leave behind."),
 "T28": ("Hazy Golf", "Ribbed cotton &middot; 44&Prime; &times; 22&Prime;", "Hazy Tour Towel", None,
         "Hazy embroiders its script on a white ribbed caddy towel and offers it in green or red and blue stripes."),
 "T44": ("Sierra Madre", "Waffle microfiber &middot; 15&Prime; &times; 23&Prime;", "Sierra Madre Golf Towel", None,
         "Sierra Madre prints its logo in lime green on the front and leaves the back all brown. Their words: pretty in the front, business in the back."),
 "T03": ("Ally Aiken", "Microfiber &middot; 16&Prime; &times; 24&Prime;", "On the Green Golf Towel", None,
         "The Austin artist best known for her watercolour course maps made this illustrated towel, finished with a gold grommet and ring."),
 # ---- Magnetic and technical
 "T59": ("Frogger", "Magnetic &middot; Waffle", "TRAX Golf Towel", None,
         "Frogger&rsquo;s Latch-it magnetic fastener lets you take the towel off the bag and stick it anywhere. It comes in a spread of bright colours."),
 "T86": ("VESSEL", "Magnetic &middot; 10&Prime; &times; 10&Prime;", "Magnetic Golf Towel", None,
         "VESSEL sews a strong magnet into a small square of waffle microfiber, so it lifts with a clubhead or sticks to a cart post."),
 "T57": ("Haywood Golf", "Magnetic &middot; 23&Prime; &times; 16&Prime;", "Magnetic Golf Towel", None,
         "A silicone-covered magnet plus a carabiner, in a range of prints from course scenes to camo."),
 "T58": ("MNML Golf", "Recycled PET &middot; 37&Prime; &times; 20&Prime;", "Eco Golf Towel", None,
         "A waffle towel made entirely from recycled plastic, with a centre loop and an outer loop, so it hangs either way."),
 "T73": ("Pluto Golf", "Magnetic &middot; Slim", "Slim Magnet Towel, Red Camo", None,
         "Pluto cuts this magnetic towel long and slim and prints it in its own red camo. Their line: square towels are for squares."),
}

SECTIONS = [
    ("heavy", "Heavy, Dark and Built for Fall", "heavy-and-dark",
     ["T87", "T13", "T15", "T30", "T51", "T84", "T16", "T33", "T37", "T07", "T48", "T62", "T50", "T67", "T53", "T52", "T77", "T11"],
     "<strong>The fall section</strong>Knits, chenille, gauze, ribbed cotton and waffle, mostly in the colours that hide mud. "
     "If you only buy one towel this season, it is in here."),
    ("pattern", "Jacquard, Plaid and Pattern", "jacquard-and-pattern",
     ["T43", "T83", "T79", "T64", "T41", "T69", "T25", "T61", "T40", "T20", "T01", "T38"],
     "<strong>Woven and printed patterns</strong>This group covers jacquard, paisley, camo, checks and stripes. "
     "These are the ones that look like they belong on a bag stand in a clubhouse."),
    ("loud", "Loud on Purpose", "loud-on-purpose",
     ["T09", "T35", "T18", "T27", "T81", "T75", "T85", "T04", "T56", "T55", "T17", "T05", "T28", "T44", "T03"],
     "<strong>Jokes, mascots and prints</strong>A towel is the one accessory where nobody minds a bit of noise. "
     "Two of these are sold in their home currency, and we have left the price that way."),
    ("tech", "Magnetic and Technical", "magnetic-and-technical",
     ["T59", "T86", "T57", "T58", "T73"],
     "<strong>Magnets and recycled fibre</strong>Magnets that stick to a clubhead or a cart post, and one towel made from recycled plastic bottles."),
]

# Lenny 25 Sep: "add lookbook/IRL/Journal images between catagories. No quotes on this post"
# Brands' own photography (homepages / journals), localised; sources in research/towels/irl-picks.json.
BANDS = {
    "pattern": ("Photography &middot; the brands&rsquo; own",
                "Shoal, Ripit and Manors show their towels and their golfers out on the course.",
                [("irl-a1", "A Shoal Golf Co. cap and a cream towel on an olive and tan stand bag on the grass", "Shoal"),
                 ("irl-a2", "A golfer in a patterned shirt teeing up a ball beside a pond", "Ripit"),
                 ("irl-a3", "A golfer in a Manors jacket holding the pin with a yellow flag", "Manors")]),
    "loud": ("Photography &middot; the brands&rsquo; own",
             "Birds of Condor, No Laying Up and OKKA take the loud stuff out in the wild.",
             [("irl-b1", "A golfer in a Ventura tee holding a club across his shoulders under palm trees", "Birds of Condor"),
              ("irl-b2", "Two golfers walking down the fairway pushing their bags", "No Laying Up"),
              ("irl-b3", "A man sitting in a room with a green plaid curtain and a golf bag beside him", "OKKA Golf")]),
    "tech": ("Photography &middot; MNML Golf&rsquo;s own",
             "MNML photographs its recycled-fibre towels and bags on the course, in the evening light.",
             [("irl-c1", "A golfer in a red shirt walking up the fairway carrying his bag", "Walking up"),
              ("irl-c2", "A golfer carrying a white stand bag toward the trees", "Carry bag"),
              ("irl-c3", "Two golfers on a green beside a white stand bag", "On the green")]),
}

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>A towel is the cheapest way to change how a golf bag looks, and fall is when it earns its keep. The mornings are wet, the bunkers are damp and the grooves fill up. So this is the big one: fifty towels from fifty independent brands, one per brand, sorted into four groups.</p>
    <p>If you want one towel for the season, start with the heavy section. The Devereux knitted Cactus Voodoo and the Sentinel gauze towel from Japan are the two we would reach for first, and the Jones Rain Hood is the practical pick for a wet November. For a present, the Seamus Chief Joseph jacquard or the Manors and Gentleman Jack paisley. For a laugh, the USAG newspaper towel.</p>
    <p>Every towel below was in stock on the brand&rsquo;s own store on 25 September 2026, and every price was read there that day. Prices are in US dollars wherever the store offers them. Two brands sell only in their own currency, and we have left those prices alone. If you want more, our <a href="/drops/the-towel-edit-vol-3">Towel Edit, Vol. 3</a> and <a href="/drops/the-hat-and-towel-edit">Hat &amp; Towel Edit</a> go deeper on a few of these brands.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Roundup</div>
      <div class="sidebar-detail"><span class="l">Towels</span><span>50</span></div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>50, all independent</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>{RANGE}</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Devereux Cactus Voodoo</span></div>
      <div class="sidebar-detail"><span class="l">Wet-day pick</span><span>Jones Rain Hood</span></div>
      <div class="sidebar-detail"><span class="l">Prices read</span><span>25 Sep 2026</span></div>
      <a href="#heavy-and-dark" class="sidebar-cta">Start with the fall section &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#GolfTowel</span>
        <span class="hashtag">#FallGolf</span>
        <span class="hashtag">#IndependentGolf</span>
        <span class="hashtag">#GolfAccessories</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

FAQ = [
    ("What is the best golf towel for fall?",
     "For cold, wet mornings, a heavy cotton towel or one with a water-resistant side. In this roundup the Jones Sports Co. Rain Hood Towel ($50) doubles as a rain cover for your clubs, and the knitted and chenille towels from Devereux and Hidden Links Society are the heaviest."),
    ("Microfiber or cotton: which golf towel is better?",
     "Microfiber waffle towels pull dirt out of grooves and dry quickly. Cotton, terry and velour towels are heavier, softer and better at drying hands and grips. Several towels here, such as Local Rule's Iron Logo Towel, put microfiber on one side and cotton on the other."),
    ("How much does a good golf towel cost?",
     "In this roundup the towels run from $12.95 (Clutch Golf Co.) to $57 (Sugarloaf Social Club), and most are between $25 and $45. Prices were read from each brand's own store on 25 September 2026."),
    ("Do magnetic golf towels work?",
     "Yes. A magnetic towel sticks to a clubhead, a cart post or any metal on your bag, so you can pick it up with a club and are less likely to leave it behind. Frogger, VESSEL, Haywood, Pluto and Sunday Golf all make one here."),
    ("Are all of these golf brands independent?",
     "Yes. Every towel comes from an independent golf brand rather than one of the big equipment companies, and each brand appears once."),
    ("Which golf towels here are made in the USA or Japan?",
     "Foray Golf's Bogey Monster towel and Sugarloaf Social Club's Tour Towel are made in the USA. Sentinel's Shinto gauze towel is made in Japan."),
]


def money(x):
    return f"${x:,.0f}" if float(x).is_integer() else f"${x:,.2f}"


def price(i):
    ov = C[i][3]
    return ov if ov else money(P[i]["usd"])


def band(key):
    kick, line, items = BANDS[key]
    figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>'
                     for f, alt, cap in items)
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <p class="cat-kicker"><strong>{kick}</strong>{line}</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


def card(i, idx):
    p = P[i]
    brand, detail, name, _, copy = C[i]
    fr = p["local"]
    label = H.unescape(f"{brand} {name}").replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {k+1} of {len(fr)}" loading="lazy" /></div>'
                   for k, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if k == 0 else ""}" data-i="{k}" aria-label="View image {k+1}"></button>'
                   for k in range(len(fr)))
    return (f'<div class="product-card" id="t-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{idx:02d} &middot; {brand} &middot; {detail}</div>'
            f'<div class="product-name">{name} &middot; {price(i)}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="{H.escape(p["url"])}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


def section(sec, n0):
    key, h2, anchor, ids, kicker = sec
    cards = "\n".join(card(i, n0 + k) for k, i in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} Towels</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>'
                     for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items, pos = [], 1
    for _, _, _, ids, _ in SECTIONS:
        for i in ids:
            items.append({"@type": "ListItem", "position": pos, "url": P[i]["url"],
                          "name": H.unescape(f"{C[i][0]} {C[i][2]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-09-25", "dateModified": "2026-09-25",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": items},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Drops & Brands", "item": "https://thegrassyissue.com/#feed"},
            {"@type": "ListItem", "position": 3, "name": "Fall Golf Towel Roundup", "item": URL}]},
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
    ids = [i for s in SECTIONS for i in s[3]]
    assert len(ids) == 50 == len(set(ids)), len(ids)
    assert set(ids) == set(C), set(ids) ^ set(C)
    brands = [C[i][0] for i in ids]
    assert len(set(brands)) == 50, "a brand repeats"
    for i in ids:
        assert P[i].get("local"), f"{i} has no images"
        assert C[i][3] or P[i].get("usd"), f"{i} has no USD price"
    usd = [P[i]["usd"] for i in ids if not C[i][3]]
    rng = f"{money(min(usd))}&ndash;{money(max(usd))}"
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Fall Golf Towel Roundup</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>September 25, 2026</span><span class="dot"></span>
    <span>Fall 2026 &middot; 50 brands</span><span class="dot"></span>
    <span>50 towels &middot; {rng}</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A golfer on the course with a stack of Sunday Golf towels draped over his shoulders and a drink in his hand" fetchpriority="high" /></div></div>
"""
    body += TAKE.replace("{RANGE}", rng)
    n = 1
    for sec in SECTIONS:
        if sec[0] in BANDS:
            body += band(sec[0])
        s, n = section(sec, n)
        body += s
    body += faq_html()
    out = head_top() + head_rest + body + tail
    print(f"  {n-1} cards, USD range {rng}")
    if not apply_:
        print("  dry run — pass --apply")
        return
    OUT.write_text(out, encoding="utf-8")
    verify()


def verify():
    fin = OUT.read_text(encoding="utf-8")
    bad = []
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    for leak in ("Burnt Orange", "Manors Revisited"):
        if leak in above:
            bad.append(f"donor text leaked: {leak}")
    if fin.count('class="product-card"') != 50:
        bad.append("card count " + str(fin.count('class="product-card"')))
    if 'pull-quote-inner">&ldquo;' in above or 'class="pull-quote"' in above:
        bad.append('a pull-quote got in')
    if above.count('class="ig-grid"') != 3:
        bad.append('band count')
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", above), re.I):
        bad.append("banned word")
    if "Mogshade" in above:
        bad.append("Mogshade should be out")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file():
            bad.append(f"missing {f}")
    if bad:
        OUT.unlink()
        sys.exit("! removed. " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
