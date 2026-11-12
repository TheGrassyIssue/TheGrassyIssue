#!/usr/bin/env python3
"""build-needlepoint-roundup.py — The Needlepoint Roundup, 11 November 2026. Cloned from build-around-the-greens.py.
Lenny: "I want to do a needlepoint round up, all the best needlepoint items we've seen recently", then on the 44-option
sheet (research/needlepoint-roundup/options.json): "build it, okay to go pretty wide with the picks".
Picks: every in-stock item from the sheet, plus Bluegrass Fairway's Golf Pencils and Skulls belt. Left out: sold out
(Radry LLL blade cover, Gumtree State Bird, S&B Crossed Clubs marker, Sugarloaf can cooler), unconfirmed (S&B Wood Duck hat,
Upland tag, Yellow Lab hat) and the two S&B gloves (final sale, two sizes left). Prices and stock read from each store's
product .js in the browser on Nov 11, 2026. Frames: TGI's own localized frames for items run before, store images for the
rest, refit onto a stone ground (research/gift-guide-2026 refit), see research/needlepoint-roundup/frames.json.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "The Needlepoint Roundup: 36 Belts, Headcovers and Small Things for Golfers"
DESC = ("The best golf needlepoint we have seen this year, all in stock: belts from Smathers & Branson, J.Press, Charleston Belt, "
        "Brewster and Good Threads, Asher Riley headcovers, scorecard holders, key fobs, a flask and two dog collars.")
H1 = "The Needlepoint Roundup"
BC = "The Needlepoint Roundup"
SLUG = "golf-needlepoint-roundup"
IMG = "/images/needlepoint-roundup"
U = lambda d, h: f"https://{d}/products/{h}"
SB = "smathersandbranson.com"
P = {
 # golf belts
 "b1": ("Smathers &amp; Branson", "Golf Tee Pattern Belt, Dark Navy", "$195", U(SB,"golf-tee-pattern-belt"),
   "White tees scattered across dark navy, hand-stitched and lined with full-grain leather, with a solid brass buckle. Two Bowdoin roommates started Smathers &amp; Branson in 2004 after failing to find a second needlepoint belt to buy, and this is the simplest golf pattern they make."),
 "b2": ("Smathers &amp; Branson", "Beachy Golf Belt, Classic Navy", "$195", U(SB,"beachy-golf-belt-classic-navy"),
   "Golf carts and palm trees stitched across classic navy. It reads as golf from ten feet and as pattern from two, which is the trick a good needlepoint belt pulls off. Wear it from the resort course to the dinner after."),
 "b4": ("Smathers &amp; Branson", "Mulligan Belt, Dark Navy", "$195", U(SB,"mulligan-needlepoint-belt-dark-navy"),
   "Smathers &amp; Branson stitches a row of tiny golfers at the top of their swings across dark navy. Hand-stitched, an inch and a quarter wide and lined with full-grain leather."),
 "b5": ("Smathers &amp; Branson", "St Andrews Scene Belt", "$195", U(SB,"st-andrews-scene-needlepoint-belt"),
   "St Andrews&rsquo; stone clubhouse and links, stitched in a long panorama of sky, sandstone and green. The most scenic belt here, and the one for the friend who came back from Scotland talking about nothing else."),
 "b6": ("Smathers &amp; Branson", "Ham and Egging Belt, Blue", "$195", U(SB,"ham-and-egging-belt-blue"),
   "On this one a pig and a chicken chase golf balls across bright blue. Ham-and-egging is what good partners do in a four-ball, one making par when the other cannot, and this is the belt for your regular partner."),
 "b11": ("Charleston Belt", "Grateful for Golf Needlepoint Belt, Navy", "$169.99", U("charlestonbelt.com","grateful-for-golf-leather-and-hand-stitched-needlepoint-belt"),
   "A saddle golf shoe and a tee repeat across navy on a leather-backed, hand-stitched strap from South Carolina. Charleston Belt&rsquo;s point is that navy goes with everything you own, so this one takes no thought in the morning."),
 "b12": ("Good Threads", "Golf Flags Needlepoint Belt, Green", "$125", U("goodthreadsneedlepoint.com","golf-flags-needlepoint-belt-green"),
   "Pin flags and crossed clubs on green, hand-stitched on 18-count canvas and finished with full-grain Italian leather. At $125 it is the least expensive hand-stitched belt here."),
 "b13": ("Good Threads", "Golf Tees Needlepoint Belt", "$125", U("goodthreadsneedlepoint.com","golf-tees-needlepoint-belt"),
   "Tees and balls in a loose pattern across green, on the same canvas and Italian leather as the flags belt. A cheerful first needlepoint belt for someone who has never owned one."),
 "b14": ("Good Threads", "Golf Bags Needlepoint Belt", "$125", U("goodthreadsneedlepoint.com","golf-bags-needlepoint-belt"),
   "A line of carry bags stitched across navy, each in a different color. Made for the golfer who has opinions about bags, and finished like the rest of the Good Threads line."),
 "b15": ("Brewster Belt", "Pinehurst Golf Course Needlepoint Belt", "$180", U("brewsterbelt.com","pinehurst-golf-course-needlepoint-belt"),
   "The Pinehurst clubhouse and its sandhills greens, stitched on bright green with a dark leather tab and brass buckle. Brewster makes a run of famous-course belts, from Augusta to Kiawah, and this is the one we liked most."),
 "b16": ("Brewster Belt", "19th Hole Needlepoint Belt", "$145", U("brewsterbelt.com","19th-hole-needlepoint-belt"),
   "A red 19 flag, crossed clubs and a ball on royal blue. It is the belt about where the round actually ends, finished in tan leather and hand-stitched like everything Brewster sells."),
 "b18": ("Baldwin Belts", "Golf Cart Needlepoint Belt", "$165", U("baldwinbelts.com","copy-of-needlepoint-belt-texas-flag"),
   "Golf carts and crossed clubs on a soft grey ground, made in small runs by a maker whose catalog reads like a list of real hobbies. A quieter color than most golf belts, which makes it easier to wear off the course."),
 "b20": ("Bluegrass Fairway", "Golf Pencils and Skulls Repp Needlepoint Belt", "$140", U("www.bluegrassfairway.com","golf-pencils-and-skulls-repp-needlepoint-belt"),
   "Bluegrass Fairway&rsquo;s take on a trad staple: golf pencils laid out like a repp stripe on navy, with skull-and-crossbones clubs in between. Saddle tan leather tabs, a leather lining and a solid brass buckle, at an inch and a half wide."),
 # off-course belts
 "b3": ("Smathers &amp; Branson", "Fly Fishing Life Belt, Classic Navy", "$195", U(SB,"fly-fishing-life-belt-classic-navy"),
   "Smathers &amp; Branson stitches a fly-fishing scene in French cotton thread on navy and lines it with Italian leather. For the golfer who spends the off-season standing in a river instead."),
 "b7": ("J.Press", "Dancing Bear Needlepoint Belt, Oatmeal", "$195", U("jpress.com","dancing-bear-needlepoint-belt"),
   "J.Press has sold Ivy clothing since 1902 and treats the needlepoint belt as everyday stock. The Dancing Bears run across oatmeal, with full-grain leather tabs and a solid brass buckle. Size up one from your trousers, per their own rule."),
 "b8": ("J.Press", "Dark &lsquo;N&rsquo; Stormy Needlepoint Belt", "$195", U("jpress.com","dark-n-stormy-needlepoint-belt"),
   "Signal flags stitched across navy, a nod to the sailing drink. Same construction as the rest of the J.Press line, and the pattern that works hardest away from a golf course."),
 "b9": ("J.Press", "Skull and Crossbones Needlepoint Belt", "$195", U("jpress.com","needlepoint-belt-skull-and-crossbones"),
   "J.Press stitches white skulls and crossbones on black, an old New Haven wink. With grey flannels it reads as heraldry. Hand-stitched, with leather tabs and a brass buckle."),
 "b10": ("Charleston Belt", "Ric Flair Needlepoint Belt", "$185", U("charlestonbelt.com","ric-flair-needlepoint-belt"),
   "Charleston Belt put the Nature Boy&rsquo;s world on a rose ground: the crown, the sunglasses, the limo. It is the loudest belt here, built with the same leather backing and hand-stitching as the sober ones."),
 # made to order
 "b17": ("Bluegrass Fairway", "Custom Needlepoint Belt", "$200", U("www.bluegrassfairway.com","augusta-tour-visor-needlepoint-belt-1"),
   "Bluegrass Fairway stitches a belt from the images you send: a home course, a club logo, a dog, initials. You approve a mockup first, and it ships in a branded wooden box. Their Christmas cutoff was September 15, so order now for spring."),
 "b19": ("Fish Creek", "Custom Needlepoint Belt", "$189", U("fishcreekbrands.com","custom-needlepoint-belt"),
   "Fish Creek mostly works on commission: you send what you want stitched and they build the belt around it, about ten thousand stitches at a time. The Alabama Traditions design shows what the finished custom work looks like."),
 # headcovers
 "h1": ("Asher Riley", "Flamingo Needlepoint Driver Headcover", "$110", U("asherriley.com","flamingo-needlepoint-driver-headcover"),
   "Pink flamingos among green leaves, hand-stitched and trimmed in white leather with a soft fleece lining, sized for a 460cc driver. Needlepoint suits a flamingo, because the medium wants flat blocks of saturated color."),
 "h2": ("Asher Riley", "Crossing Golf Clubs Needlepoint Driver Headcover", "$110", U("asherriley.com","crossing-golf-clubs-needlepoint-driver-headcover"),
   "Crossed clubs and a ball on royal blue, set into a tan Italian leather sock with a stitched number one. Lined with anti-pill fleece. The most classic of the Asher Riley covers."),
 "h3": ("Asher Riley", "Gopher Golf Needlepoint Driver Headcover", "$110", U("asherriley.com","gopher-golf-needlepoint-driver-headcover"),
   "A buck-toothed gopher pops out of a hole beside a golf ball, stitched above a tan leather body. Every golfer of a certain age knows where he comes from, and he will start a conversation on the first tee."),
 "h4": ("Asher Riley", "American Flag Needlepoint Blade Putter Headcover", "$110", U("asherriley.com","american-flag-needlepoint-blade-putter-headcover"),
   "Stars on one side, stripes on the other, hand-stitched and trimmed in white leather to fit a blade putter. Lined with soft fleece to protect the face."),
 "h5": ("Smathers &amp; Branson", "Big Irish Flag Driver Headcover", "$110", U(SB,"big-irish-flag-needlepoint-driver-headcover"),
   "The Irish tricolor stitched across the top of a white leather driver cover with a green number one. Hand-stitched needlepoint, Italian leather and a fleece lining. For the trip to Ballybunion, or the memory of one."),
 # in the bag
 "c1": ("Smathers &amp; Branson", "Tonal Clubs Golf Scorecard Holder", "$89.50", U(SB,"tonal-clubs-golf-scorecard-holder-dark-navy"),
   "Crossed clubs in two blues on a needlepoint front, wrapped in leather, with a pocket for the card and a loop for the pencil inside. It keeps a scorecard dry and flat for eighteen holes and looks better every season."),
 "c6": ("Asher Riley", "Golf Flag Needlepoint Sunglass Strap", "$79.50", U("asherriley.com","golf-flag-needlepoint-sunglass-straps"),
   "Little yellow pin flags stitched along a navy strap with leather ends that slide over your sunglass arms. Designed in the U.S. and hand-stitched, so your glasses hang at your chest between shots instead of falling off the cart."),
 "t1": ("Asher Riley", "Diagonal Tee Needlepoint Luggage Tag", "$45", U("asherriley.com","diagonal-tee-needlepoint-luggage-tag"),
   "Striped tees in a row on navy, hand-stitched on the front of an English leather tag with a card window on the back. It buckles to the bag with a leather strap, at 4.75 by 2.75 inches."),
 "t2": ("Smathers &amp; Branson", "Monogrammed Azalea Key Fob, Dark Navy", "$50", U(SB,"monogrammed-azalea-key-fob-dark-navy"),
   "A pink azalea on dark navy needlepoint with your three initials stitched into the design. Leather tab and split ring. Clip it to the bag in April."),
 "t4": ("Baldwin Belts", "Golf Ball Needlepoint Key Fob", "$32", U("baldwinbelts.com","needlepoint-key-fob-golf-keychain-with-brass-lobster-claw"),
   "A golf ball stitched on a short needlepoint strap with a brass lobster clasp, so it clips to a bag or a belt loop as easily as a key ring. Baldwin also makes a golf cart version."),
 "t5": ("Charleston Belt", "Golf Cart Needlepoint Key Fob, Red", "$35", U("charlestonbelt.com","key-fob-golf-cart-red-hand-stitched-needlepoint"),
   "A red golf cart on green fairway, hand-stitched in Charleston with a leather tab and a double ring. Throw your golf cart keys on it, or your house keys if you would rather be on one."),
 # 19th hole
 "n1": ("Sugarloaf Social Club", "&ldquo;Nantucket Red&rdquo; Needlepoint Bottle Opener", "$35", U("www.sugarloafsocialclub.com","nantucket-red-needlepoint-bottle-opener"),
   "Sugarloaf set a needlepoint inlay of its arrow, in Nantucket red, into a wooden bottle opener with a hidden magnet that catches the cap. Made with Smathers &amp; Branson, and one of the few pieces from Sugarloaf&rsquo;s fall needlepoint drop still in stock."),
 "n3": ("Smathers &amp; Branson", "Gopher Golf Life Flask, Dark Navy", "$79.50", U(SB,"gopher-golf-life-flask-dark-navy"),
   "A six-ounce stainless steel flask wrapped in needlepoint and full-grain leather, stitched with a gopher, a bucket hat and a &ldquo;Just Be the Ball&rdquo; sign. A very specific film, on a very useful object."),
 "n4": ("Smathers &amp; Branson", "Golfer&rsquo;s Camo Card Wallet", "$65", U(SB,"golfers-camo-credit-card-wallet"),
   "Camouflage, but every patch is fairway, rough or a pin flag. Hand-stitched needlepoint on the front and Italian leather on the back, slim enough for a back pocket on the course."),
 # dog
 "d1": ("Brewster Belt", "On Par Golf Needlepoint Dog Collar", "$85", U("brewsterbelt.com","on-par-golf-needlepoint-dog-collar"),
   "Golf balls in rows on navy, hand-stitched and backed with top-grain leather and a solid brass buckle. Made to order: Brewster sends a digital preview in about three to five business days and stitches nothing until you approve it."),
 "d2": ("Brewster Belt", "Yellow Golf Cart Needlepoint Dog Collar", "$85", U("brewsterbelt.com","yellow-golf-cart-needlepoint-dog-collar"),
   "Yellow golf carts and pin flags on green, built the same way. Brewster also makes argyle, putting and flag patterns at the same price."),
}
SECTIONS = [
 ("Golf Belts", "golf-belts", ["b1","b4","b6","b5","b2","b15","b16","b11","b20","b12","b13","b14"],
  "<strong>The one everyone notices</strong>Tees and carts, a mulligan, St Andrews and Pinehurst, from $125 to $195. Every belt here is hand-stitched on canvas and backed with leather."),
 ("Belts for Off the Course", "off-course-belts", ["b7","b8","b9","b3","b10","b18"],
  "<strong>For dinner after</strong>J.Press bears and signal flags, a skull and crossbones, a fly-fishing scene, the Nature Boy and a golf cart belt quiet enough for the office."),
 ("On the Course", "on-the-course", ["h2","h3","h1","h5","h4","c1"],
  "<strong>The needlepoint you see every hole</strong>Four driver covers, a blade putter cover and a scorecard holder, all hand-stitched and finished in leather."),
 ("Small Things", "small-things", ["c6","t1","t2","t5","t4","n4"],
  "<strong>Clip it on, carry it</strong>A sunglass strap, a luggage tag, three key fobs and a card wallet, from $32 to $79.50."),
 ("Custom, Cocktails and the Dog", "custom-bar-dog", ["b17","b19","n3","n1","d1","d2"],
  "<strong>Made to order, and after the round</strong>Two belts stitched from whatever you send, a flask, a bottle opener and two Brewster collars made to order for the dog."),
]
N = 36
PAIRS = {}
BANDS = {
 "golf-belts": ("Worn, not stored", "Needlepoint out in the world: a belt with jeans, a belt on the boat and a pair of needlepoint loafers.",
   [("life-1","A man in jeans and a navy tee wearing a Smathers &amp; Branson needlepoint belt","Smathers &amp; Branson"),
    ("life-2","A man in a white polo and blue trousers on a boat wearing a Brewster needlepoint belt","Brewster Belt"),
    ("life-3","A man holding a pair of Smathers &amp; Branson needlepoint driving loafers beside a lake at dusk","Smathers &amp; Branson")]),
 "custom-bar-dog": ("From the bench", "A Brewster custom belt with its gift card, a wall of finished belts on Instagram and the Life Belt gift box.",
   [("life-4","A Brewster custom needlepoint belt with its gift card, stitched with a wine glass, a sailboat and a bottle","Brewster Belt"),
    ("life-5","A rack of brightly colored Good Threads needlepoint belts","Good Threads on Instagram"),
    ("life-6","A man holding the wooden Smathers &amp; Branson Life Belt box","Smathers &amp; Branson")]),
 "on-the-course": ("In play", "A Sugarloaf belt on chinos, a scorecard holder on the course and a flag headcover coming off the driver.",
   [("life-7","A man with his hand in his pocket wearing a Sugarloaf Social Club chevron needlepoint belt with chinos","Sugarloaf Social Club"),
    ("life-8","A golfer holding a crossed-clubs needlepoint scorecard holder with a flag-patch glove","Smathers &amp; Branson"),
    ("life-9","A golfer pulling a stars-and-stripes needlepoint headcover off his driver on the course","Smathers &amp; Branson")]),
 "small-things": ("The small stuff", "Key fobs by the dozen, and a needlepoint collar out for a walk.",
   [("life-10","Smathers &amp; Branson needlepoint key fobs spread on a wooden table","Smathers &amp; Branson"),
    ("life-11","A grid of Good Threads needlepoint key fobs","Good Threads on Instagram"),
    ("life-12","A doodle sitting on brick in an Asher Riley needlepoint collar and leash","Asher Riley")]),
}
TREND = """
<div class="pull-quote" style="margin:40px auto 24px"><div class="pull-quote-inner">&ldquo;You had to have someone make one for you.&rdquo;<span class="pull-quote-attr">&mdash; Austin Branson, Smathers &amp; Branson</span></div></div>
"""
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <h2 class="products-hdr" id="the-trend" style="text-align:left;margin:10px 0 18px">Why Needlepoint Is Everywhere</h2>
    <p>Needlepoint has turned up in more than a dozen of our posts since the summer: a belt in our story on the clothes golf founders wanted to wear, a ball marker in a short-game kit, a flamingo headcover in The Bird Edit, a collar in a post about golf dogs. We did not plan it. It kept appearing in the stores of the brands we cover, and the best pieces kept selling out. Radry&rsquo;s needlepoint blade cover and Gumtree&rsquo;s State Bird headcover are both gone, and when we checked Sugarloaf Social Club this week, almost all of its fall needlepoint had sold through.</p>
    <p><strong>The craft is having a moment.</strong> In April, <a href="https://www.stlmag.com/design/from-grandma-hobby-to-gen-z-trend-needlepoint-finds-a-new-audience-in-st-louis/" target="_blank" rel="noopener">St. Louis Magazine</a> reported that local needlepoint shops are seeing a surge led by younger stitchers. One designer, Annie Zigman, said a distributor told her sales were up 305 percent. She pointed to a 2015 industry survey that put the average needlepointer at 61 and said today&rsquo;s stitchers are about 30 years younger. A shop manager there called bag tags a whole new phenomenon of the last couple of years.</p>
    <p><strong>Golf has always been needlepoint&rsquo;s home turf.</strong> The belt with tiny clubs on it belongs to the clubhouse as much as the blazer does. For a long time you could only get one if somebody stitched it for you; Smathers &amp; Branson started in 2004 because its founders kept getting asked where to buy the belts their girlfriends had made them, and a decade in, Austin Branson told The Daily Signal that specialty shops, colleges, yacht clubs and golf courses were still its bread and butter. What has changed is how far the makers have pushed past the belt. Smathers &amp; Branson now stitches scorecard holders, flasks, driver covers and an official belt for the 2026 U.S. Open at Shinnecock Hills, and it made a needlepoint line with FootJoy built around FJ&rsquo;s golf shoe silhouette. Asher Riley stitches driver covers and dog collars, and Brewster makes collars to match its belts. Charleston Belt put Ric Flair on one.</p>
    <p><strong>It fits the rest of what golfers are wearing.</strong> Prep is back in a quieter form; <a href="https://www.whowhatwear.com/fashion/trends/preppy-fashion-trend-2026" target="_blank" rel="noopener">Who What Wear</a> names it one of 2026&rsquo;s defining moods and points to golf as one of the sports shaping the details. A needlepoint belt is the easiest way into that look, and the most personal. You pick the picture, and it is hand-stitched, slow and built to outlast the trousers you wear it with.</p>
    <p><strong>What we did.</strong> We went back through everything we have featured this year, checked what is still in stock and added new pieces from the same makers.</p>
    <p><strong>Why it works on golfers.</strong> Needlepoint is slow, flat and colorful, which suits small pictures of things you love: a course, a cart, a gopher. It is also tough. A hand-stitched canvas backed with leather will outlast the trousers you wear it with, which is why so many of these turn up in grandfathers&rsquo; drawers.</p>
    <p><strong>How to buy a belt.</strong> Order a size up. Bluegrass Fairway recommends two to three inches over your waist, and J.Press says one size up from your trousers. Check the width too: most are an inch and a quarter, Bluegrass Fairway&rsquo;s are an inch and a half.</p>
    <p><strong>What is in here.</strong> There are @@N@@ pieces from @@NB@@ makers, all in stock when we checked on November 11, 2026. Two belts and both dog collars are made to order, so allow a few weeks. Prices are what each store shows a US visitor.</p>
    <p>If belts are what you came for, the full field is in <a href="/drops/the-needlepoint-belt-report">The Needlepoint Belt Report</a>.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Details</div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>@@N@@</span></div>
      <div class="sidebar-detail"><span class="l">Makers</span><span>@@NB@@</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$32&ndash;$200</span></div>
      <div class="sidebar-detail"><span class="l">Belts</span><span>20</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Brewster Pinehurst Golf Course Belt</span></div>
      <div class="hashtags">
        <span class="hashtag">#Needlepoint</span>
        <span class="hashtag">#NeedlepointBelt</span>
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
    <h2 class="products-hdr" id="last-word">Buy It Once</h2>
    <p>A needlepoint belt is a $125 to $200 purchase you make once. Pick a pattern that means something to you, size it up and wear it until the leather goes soft.</p>
    <p>Then add the small stuff. A key fob or a luggage tag is the easiest way to give someone needlepoint without guessing their waist size.</p>
    <p>For more, see <a href="/drops/the-needlepoint-belt-report">The Needlepoint Belt Report</a>, <a href="/drops/golf-bag-accessories-what-to-hang-from-your-bag">what to hang from your bag</a> and <a href="/drops/dogs-and-golf">dogs and golf</a>.</p>
  </div>
</section>
"""
HERO_ALT = "A row of Smathers & Branson needlepoint belts laid out on the grass"
FRN = json.loads((ROOT / "research/needlepoint-roundup/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-NP-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-11-11", "dateModified": "2026-11-11",
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


def section(sec, n0):
    h2, anchor, ids, kicker = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} picks</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n' +
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


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
    <span>The Edit &middot; Belts, headcovers, bag and bar</span><span class="dot"></span>
    <span>@@N@@ picks &middot; in stock, checked November 11, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="{HERO_ALT}" fetchpriority="high" /></div><div style="margin:8px 0 0;font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;opacity:.55">Photo: Smathers &amp; Branson</div></div>
"""
    body = body.replace("@@N@@", str(N)); body += TAKE.replace("@@NB@@", str(len({P[k][0] for s_ in SECTIONS for k in s_[2]}))).replace("@@N@@", str(N)); body += TREND
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
    for w in ("worth", "genuinely", "honestly", "straightforward"):
        if re.search(rf"\b{w}\b", re.sub(r"<[^>]+>", " ", above), re.I): bad.append("banned " + w)
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
