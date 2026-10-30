#!/usr/bin/env python3
"""build-graphic-tees-2.py — The Graphic Tee Edit Vol. 2: 39 tees in a tee-wall layout. 29 October 2026.
Lenny: "another graphic tee round up vol 2" -> kept 6 from round 1 (Mogshade, Hidden Links, Malbon, Devereux, Walker, Students),
round 2 from recently added brands (dropped Dual Sport x3, Foray, Slice Town, SAHA Burning Cart, St Andre Divots or Death),
asked about Parmore (Motorsport + No Membership Required added; Parmore's AI listing images are excluded) ->
"build the post but I really want to show off the tees, is there a way to better format the post?"
FORMAT (v2, Lenny: different hero, lead with on-model/IRL, add lookbook breaks): hero is three on-model back prints; tiles lead with on-model shots where the brand has them; four 3-up lookbook bands; the body is a big-tile wall (3 across desktop, 2 on phones), the graphic
first, hover/tap flips to the other side or on-model shot; short captions. Split: Back Prints / Up Front.
FACTS: live catalogues Oct 29 (research/graphic-tees-2/final.txt). All prices USD on the brand's US store except AXXA (A$).
Golf Gods sells US through golfgodsonline.com ($50, marked down from $55). Mogshade shows $103 to US shoppers.
Vol. 1 = /drops/the-bold-tee-edit. No FAQ.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"
SLUG = "the-graphic-tee-edit-vol-2"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/graphic-tee-edit-vol-2"
FRN = json.loads((ROOT / "research/graphic-tees-2/frames.json").read_text())
DATE = "2026-10-29"
TITLE = "The Graphic Tee Edit Vol. 2: 39 Golf Tees With Something to Say"
DESC = ("Thirty-nine graphic golf tees from 18 independent brands: big back prints from Hinotori, Dicey, Devereux and Golf Gods, "
        "plus slogans, photo prints and a $16 St Andre. Prices checked October 29, 2026.")
H1 = "The Graphic Tee Edit Vol. 2"

T = {  # key: (brand, name, price, url, note)
 # Back prints
 "dicey-booze": ("Dicey Golf", "Booze Hound Tee", "$40", "https://diceygolf.com/products/booze-hound-tshirt",
   "A hound in a golf cart across the back of a green tee, with Booze Hound lettered above and below. The loudest back in the edit."),
 "hin-redwing": ("Hinotori Golf", "Redwing Marsh Tee", "$38", "https://hinotorigolf.com/products/redwing-marsh-tee",
   "A full-color marsh scene with a red-winged blackbird on the reeds, printed big on a slate blue tee. Part of Hinotori&rsquo;s fall bird series."),
 "dev-highway": ("Devereux Golf", "Highway Driving Range Tee", "$38", "https://devereuxgolf.com/products/highway-driving-range-tee-black",
   "Old roadside-sign lettering on black: Highway Driving Range, Biggest Buckets in Town. From Devereux&rsquo;s fall run, every tee $38."),
 "sa-justgolf": ("St Andr&eacute;", "It&rsquo;s Just Golf Tee", "$16", "https://standre.golf/products/just-golf-white",
   "Script St Andr&eacute; across the back over the line &ldquo;Hitting the stupid little ball into the stupid little hole.&rdquo; In green or white. The cheapest tee here, and the most honest."),
 "gg-gilmore": ("Golf Gods", "Gilmore T-Shirt", "$50", "https://golfgodsonline.com/products/golf-gods-gilmore-t-shirt",
   "Gilmore and a big 18 on the back like a hockey jersey, and a G crest on the front. You know the movie. Marked down from $55."),
 "hin-koi": ("Hinotori Golf", "Koi Flow Tee V1", "$38", "https://hinotorigolf.com/products/koi-flow-v1",
   "A koi swimming down the back of an olive tee, in the same Japanese-print style as Hinotori&rsquo;s gloves and headcovers."),
 "malbon-gd": ("Malbon Golf", "Grateful Dead Bermuda Riders Tee", "$68", "https://www.malbon.com/products/grateful-dead-bermuda-riders-tee-ivory",
   "From Malbon&rsquo;s Grateful Dead collaboration: skeletons in a green golf cart on the back, the Dead lettering above. In ivory or ash heather."),
 "hls-faster": ("Hidden Links Society", "The Play Faster Tee", "$48", "https://hiddenlinkssociety.com/products/the-play-faster-tee-ivory",
   "Two words in a big serif across the back of an ivory tee: Play Faster. Small on the front. Wear it to the course on a Saturday."),
 "saha-drive": ("SAHA Golf", "How&rsquo;s My Drive Tee", "$62", "https://saha.golf/products/hows-my-drive-tee",
   "A cartoon golfer mid-swing and a bumper-sticker joke: How&rsquo;s my drive? Call 1-800-PISS-OFF. Printed on the back of a white tee."),
 "hin-wild": ("Hinotori Golf", "Wilderness Club Tee", "$38", "https://hinotorigolf.com/products/greenhead-tee-copy",
   "A poster-style mountain scene with an elk in the trees, framed like a national park print on the back of a sand tee."),
 "pw-deepcuts": ("Puttwell", "Deep Cuts Tee", "$50", "https://puttwellgolfclub.com/products/deep-cuts-tee",
   "Deep Cuts in a heavy serif across the back, in bone or black. A putter maker&rsquo;s joke, and a good one."),
 "axxa-manly": ("AXXA", "Manly Country Club Combi Tee", "A$50", "https://www.axxa.com.au/products/white-manly-country-club-oversize-tee-copy",
   "A camper van parked at the &ldquo;Manly Country Club,&rdquo; drawn in blue on an oversized white tee. From an Australian brand that mixes golf and surf. About $36 US."),
 "hin-river": ("Hinotori Golf", "River Run Tee", "$38", "https://hinotorigolf.com/products/river-run-tee",
   "A trout jumping out of the water with Hinotori in script above it, on a washed coral tee. The brightest color here."),
 "palm-rhythm": ("Palm Golf Co.", "Rhythm T-Shirt", "$39.99", "https://palmgolfco.com/products/rhythm-t-shirt-cream",
   "Find Your Rhythm arched over a palm tree and flowers, on the back of a cream or black tee. Palm Golf&rsquo;s easy, sunny style."),
 "sa-trynot": ("St Andr&eacute;", "Try Not To Die Tee", "$20", "https://standre.golf/products/try-not-to-die-tee-faded-black",
   "A skeleton and the line &ldquo;Tee it high, try not to die&rdquo; in old tattoo lettering on the back. In indigo or faded black."),
 "pw-roll": ("Puttwell", "Know Your Roll Tee", "$50", "https://puttwellgolfclub.com/products/know-your-roll-tee-1",
   "The companion to Deep Cuts: Know Your Roll across the back, in mushroom or washed black. For anyone who reads greens for too long."),
 "gg-story": ("Golf Gods", "Golf Gods Story T-Shirt", "$50", "https://golfgodsonline.com/products/golf-gods-story-t-shirt",
   "Golf Gods stacked four times down the back of a heavy faded black tee, with the brand&rsquo;s story printed underneath in small type."),
 "dicey-19th": ("Dicey Golf", "19th Hole Pocket Tee", "$40", "https://diceygolf.com/products/19th-hole-frocket",
   "A cartoon golfer carrying a flag on the back, The Best Hole Is the 19th underneath, and a small pocket print on the front."),
 "axxa-cold": ("AXXA", "Too Cold To Golf Tee", "A$50", "https://www.axxa.com.au/products/too-cold-to-golf-tee",
   "Ski goggles on the back of a cream tee and the line &ldquo;It&rsquo;s too cold to golf.&rdquo; The excuse for the next three months. About $36 US."),
 "axxa-surf": ("AXXA", "Busy Planning Surf Trip Tee", "A$50", "https://www.axxa.com.au/products/busy-planning-surf-trip-tee",
   "Handwritten across the back of a brown tee: I&rsquo;m busy planning my next surf trip. For the golfer who would rather be in the water. About $36 US."),
 "mog-human": ("Mogshade", "Only Human Oversized T-Shirt", "$103", "https://www.mogshadegolf.com/products/only-human-oversized-t-shirt",
   "A loose, hand-drawn line illustration across the back of an oversized black tee. The most art-world tee in the edit, and the most expensive."),
 "lazy-frank": ("Lazyface", "The Frank Tee", "$45", "https://lazyface.com/products/the-frank-tee",
   "Frank the frog lounging in a pond under the words Stay Lazy, on the back of a brushed-cotton cream tee. A small Lazyface script on the front."),
 "gg-gimme": ("Golf Gods", "Gimme T-Shirt", "$50", "https://golfgodsonline.com/products/gimme-t-shirt",
   "A square of putting green with the flag and the hole printed on the back, and Gimme lettered small on the front. For the two-footer you never had to hit."),
 "palm-cart": ("Palm Golf Co.", "Cart Cruisin&rsquo; T-Shirt", "$39.99", "https://palmgolfco.com/products/cart-cruisin-t-shirt-tan",
   "A golf cart under the palms and the Palm Golf &amp; Surf Club name, printed on the back of a tan tee."),
 # Up front
 "saha-knight": ("SAHA Golf", "Fairway Knight Tee", "$62", "https://saha.golf/products/fairway-knight-tee",
   "A knight statue holding a golf club, drawn in fine lines on the front of a white tee. SAHA&rsquo;s line for it: a gentleman&rsquo;s game, medieval consequences."),
 "dicey-maroon": ("Dicey Golf", "Maroon Dicey Staple Tee", "$50", "https://diceygolf.com/products/maroon-dicey-staple-tee",
   "Dicey in a big white script across the chest of a maroon tee. The simplest tee here, and the one that looks best on the course."),
 "dicey-camo": ("Dicey Golf", "Hidden Range Camo Box Tee", "$40", "https://diceygolf.com/products/dicey-camo",
   "All-over hunting camo with DICEY in varsity gold across the chest. A boxy fit."),
 "dicey-ice": ("Dicey Golf", "Ice In My Veins Tee", "$40", "https://diceygolf.com/products/cold-blooded-putting-tee",
   "A golfer reading a putt next to a beer-can-style Ice In My Veins graphic. For the player who makes the six-footer."),
 "gg-brogey": ("Golf Gods", "Brogey T-Shirt", "$50", "https://golfgodsonline.com/products/brogey-t-shirt-in-white",
   "Brogey in varsity letters across a white tee. A bogey made with your friends, which is most of them."),
 "sa-nascart": ("St Andr&eacute;", "Nascart 500 Tee", "$16", "https://standre.golf/products/nascart-500-black",
   "A racing-poster graphic on the front: checkered flags, a golf cart and the Nascart 500. Sixteen dollars."),
 "gg-swing": ("Golf Gods", "Swing King T-Shirt", "$50", "https://golfgodsonline.com/products/swing-king-t-shirt-in-brown",
   "A cartoon bear in a polo and golf glove on a brown tee. The friendliest tee here."),
 "walker-rodeo": ("Walker Golf Things", "Rodeo T-Shirt", "$60", "https://walkergolfthings.com/products/rodeo-t-shirt",
   "A cowboy riding a kangaroo, drawn in Walker&rsquo;s loose cartoon style on the chest of a white tee. From the October drop."),
 "students-swang": ("Students Golf", "Swang S/S T-Shirt", "$50", "https://studentsgolf.com/products/swang-s-s-t-shirt-1",
   "A big sketchy green golfer mid-swing across the front of a white tee. Students at its most relaxed."),
 "pw-toon": ("Puttwell", "Sig Zane Toon Tee", "$25", "https://puttwellgolfclub.com/products/sig-zane-toon-tee",
   "A colorful cartoon from Puttwell&rsquo;s collaboration with Hawaiian designer Sig Zane, on a heather tee. Marked down to $25."),
 "parm-motor": ("Parmore", "Motorsport Tee", "$63", "https://parmoregolf.com/products/parm-042",
   "A small racing-style Parmore graphic in red across the chest of a heavy black tee. Quieter than most here, and sharper for it."),
 "parm-nmr": ("Parmore", "Graphic Tee, No Membership Required", "$63", "https://parmoregolf.com/products/parm-050",
   "A photo print on the chest of a golfer on the course, under Parmore&rsquo;s line: no membership required. In white or black."),
 "winslow": ("Winslow", "Slub Tee, Brown", "$50", "https://winslowla.com/products/slub-tee-1",
   "A faded, vintage-style Winslow graphic on a brown slub tee, with the look of something you found in a pro shop in 1985."),
 "both-fade": ("Bet On The Horses", "Fade Away Tee", "$90", "https://betonthehorses.co/products/start-gate-t-shirt",
   "Horses at the start gate printed across the chest of a cream tee. Bet On The Horses&rsquo; nod to the racetrack."),
 "both-malibu": ("Bet On The Horses", "Malibu Slub Tee", "$80", "https://betonthehorses.co/products/berry-hills-t-shirt-1",
   "The quiet one: a sun-faded black slub tee with a raw, cropped feel. The tee to wear under everything else on this page."),
}
SECTIONS = [
 ("Back Prints", "back-prints", ["dicey-booze", "hin-redwing", "dev-highway", "sa-justgolf", "gg-gilmore", "hin-koi", "malbon-gd", "hls-faster",
   "saha-drive", "hin-wild", "pw-deepcuts", "axxa-manly", "hin-river", "palm-rhythm", "sa-trynot", "pw-roll", "gg-story", "dicey-19th",
   "axxa-cold", "axxa-surf", "gg-gimme", "mog-human", "palm-cart", "lazy-frank"],
  "Twenty-four tees where the graphic is on the back. The front stays quiet, and the back does the talking when you walk off the green.",
  [(9, "band-1", "Out on the course", [("Hinotori Redwing Marsh tee hanging from a golf cart", "Hinotori"), ("A golfer in the Hinotori Wilderness Club tee holding a club on the course", "Hinotori"), ("A golfer in the AXXA Busy Planning Surf Trip tee by the sea at sunset", "AXXA")]),
   (18, "band-2", "Worn in", [("Two friends in AXXA Manly Country Club tees", "AXXA"), ("The Devereux Highway Driving Range tee on a model", "Devereux"), ("The Malbon Grateful Dead Bermuda Riders tee on a model", "Malbon")])]),
 ("Up Front", "up-front", ["dicey-camo", "dicey-ice", "gg-brogey", "sa-nascart", "gg-swing", "walker-rodeo", "students-swang", "pw-toon",
   "parm-motor", "parm-nmr", "saha-knight", "dicey-maroon", "winslow", "both-fade", "both-malibu"],
  "Fifteen tees with the graphic on the chest, from a $16 race poster to an $80 sun-faded slub.",
  [(6, "band-3", "In the wild", [("The Hinotori Redwing Marsh tee hanging on a rail by a golf cart", "Hinotori"), ("The Students Swang tee on a model", "Students"), ("The AXXA Manly Country Club tee on a model", "AXXA")]),
   (15, "band-4", "One more look", [("A man in the Bet On The Horses Fade Away tee", "Bet On The Horses"), ("The Dicey Ice In My Veins tee lying in autumn leaves", "Dicey"), ("A man in the Walker Rodeo tee on an outdoor court", "Walker")])]),
]
N = 39
CSS = """<style>/*TGI-TEEWALL*/
.tw-hero img{width:100%;height:auto;display:block}
.tw-stats{display:flex;flex-wrap:wrap;justify-content:center;gap:10px 28px;margin:22px auto 8px;font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase}
.tw-stats b{font-family:inherit;font-size:20px;letter-spacing:0;display:block;text-align:center;color:var(--grass,#2D4A2B)}
.tw-jump{display:flex;justify-content:center;gap:10px;margin:18px 0 0}
.tw-jump a{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;border:1px solid currentColor;padding:8px 14px;border-radius:999px}
.products-grid[data-tw]{display:grid;grid-template-columns:repeat(3,1fr);gap:28px 22px;margin-top:26px}
@media(max-width:900px){.products-grid[data-tw]{grid-template-columns:repeat(2,1fr);gap:20px 12px}}
.products-grid[data-tw] .product-card.tw-card{border:0;padding:0;background:none;box-shadow:none;display:block;min-width:0}
.tw-tile{display:block;color:inherit;text-decoration:none}
.tw-img{position:relative;aspect-ratio:4/5;overflow:hidden;background:#E8E2D6}
.tw-img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:opacity .35s ease,transform .6s ease}
.tw-img img.tw-b{opacity:0}
.tw-tile:hover .tw-img img.tw-a{transform:scale(1.02)}
.tw-tile.has-b:hover .tw-img img.tw-b,.tw-tile.flip .tw-img img.tw-b{opacity:1}
.tw-flip{position:absolute;right:8px;bottom:8px;font-family:var(--mono);font-size:9px;letter-spacing:.12em;text-transform:uppercase;background:rgba(243,239,230,.92);border:1px solid rgba(0,0,0,.15);padding:6px 8px;border-radius:999px;cursor:pointer}
.tw-num{position:absolute;left:8px;top:8px;font-family:var(--mono);font-size:10px;background:rgba(243,239,230,.92);padding:4px 7px;border-radius:999px}
.tw-cap{display:flex;justify-content:space-between;align-items:baseline;gap:10px;margin-top:10px}
.tw-brand{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;opacity:.65}
.tw-price{font-family:var(--mono);font-size:12px;white-space:nowrap}
.tw-name{font-style:italic;font-size:17px;line-height:1.25;margin:3px 0 4px}
.tw-note{font-size:14px;line-height:1.5;opacity:.82;margin:0}
.tw-band{margin:44px 0 40px}.tw-band-k{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;text-align:center;margin:0 0 14px;opacity:.7}
.tw-shop{display:inline-block;margin-top:6px;font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;border-bottom:1px solid currentColor}
@media(max-width:600px){.tw-name{font-size:15px}.tw-note{font-size:13px}}
</style>
"""
JS = """<script>/*TGI-TEEWALL*/document.addEventListener('click',function(e){var b=e.target.closest('.tw-flip');if(!b)return;e.preventDefault();e.stopPropagation();b.closest('.tw-tile').classList.toggle('flip');});</script>
"""
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Vol. 1, <a href="/drops/the-bold-tee-edit" style="border-bottom:1px solid currentColor;">The Bold Tee Edit</a>, made the case that the golf graphic tee grew up. This is what it looks like a season later: thirty-nine tees from eighteen brands, every one in stock and new to our tee posts. Most come from brands we have only added to the Brand Index since September, which tells you where the energy is. The big apparel names are making polos. The small brands are making tees.</p>
    <h2 class="products-hdr btk-story-hdr">What We&rsquo;re Seeing</h2>
    <p><strong>The back is the new front.</strong> Twenty-four of these tees are back prints. The chest gets a small logo or nothing, and the back gets the whole idea. It makes sense for golf: nobody sees your chest when you&rsquo;re over the ball, but everyone behind you on the tee box sees your back, and the joke lands as you walk off the green.</p>
    <p><strong>Illustration over logos.</strong> The best tees here are drawn, not typeset. Hinotori prints full scenes like old national park posters: a blackbird in the reeds, a trout jumping, an elk in the pines. AXXA draws a camper van at the &ldquo;Manly Country Club,&rdquo; Palm Golf does palms and flowers, Walker does a cowboy riding a kangaroo. It&rsquo;s closer to a band tee or a souvenir shirt than to anything you&rsquo;d find in a pro shop.</p>
    <p><strong>Roadside Americana and racing.</strong> Old signs, old engines and old fonts are everywhere. Devereux&rsquo;s Highway Driving Range tee reads like a sign on a two-lane road. St Andr&eacute; made a racing poster called the Nascart 500. Parmore&rsquo;s Motorsport tee and Dicey&rsquo;s beer-can parody Ice In My Veins come from the same place: the gas station, the racetrack and the cooler in the back of the truck.</p>
    <p><strong>Golf that laughs at itself.</strong> &ldquo;Hitting the stupid little ball into the stupid little hole.&rdquo; &ldquo;Play Faster.&rdquo; &ldquo;It&rsquo;s too cold to golf.&rdquo; &ldquo;Stay Lazy.&rdquo; A cartoon golfer with a 1-800 number nobody should call. These brands aren&rsquo;t selling you a better swing. They&rsquo;re selling the feeling of a bad round with good friends.</p>
    <p><strong>Type that does the talking.</strong> At the other end, a few brands have dropped the picture altogether. Puttwell&rsquo;s Deep Cuts and Know Your Roll and Hidden Links Society&rsquo;s Play Faster are just two or three words in a heavy serif across the back. It&rsquo;s the quietest look in the edit, and some of the best.</p>
    <p><strong>The outdoors comes to the course.</strong> Dicey&rsquo;s hunting-camo box tee, Hinotori&rsquo;s fall run of birds, AXXA and Palm Golf mixing golf with surf. Golf brands are borrowing from hunting, fishing and surfing, the way they once borrowed from tennis and prep.</p>
    <p><strong>Heavier, washed, boxier.</strong> The blanks have changed too. Many of these tees are garment-dyed or faded, cut boxy or oversized, and heavy enough to keep their shape. Golf Gods&rsquo; Story tee is a heavy faded black, Mogshade&rsquo;s is oversized, and Hinotori&rsquo;s River Run is washed coral.</p>
    <h2 class="products-hdr btk-story-hdr">Who&rsquo;s Doing Something New</h2>
    <p><strong>Hinotori</strong> is best known for gloves, but its tees are turning into a seasonal series: the fall pieces are built around birds and the outdoors, and they match the brand&rsquo;s hats and headcovers. <strong>Puttwell</strong>, a putter maker, makes tees that are only about putting. <strong>Malbon</strong> has gone back to licensed icons with the Grateful Dead, and Puttwell has also worked with the Hawaiian designer Sig Zane. <strong>Parmore</strong> is putting photography on the chest instead of a logo, and <strong>Golf Gods</strong> turned a golf movie into a hockey jersey with the Gilmore 18. And <strong>St Andr&eacute;</strong> is pricing like a band merch table: two of its tees are $16.</p>
    <p>We&rsquo;ve kept the captions short so the tees can do the work. Hover over a tee (or tap Flip on a phone) to see the graphic laid flat or the other side.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Tees</span><span>39</span></div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>18</span></div>
      <div class="sidebar-detail"><span class="l">Back prints</span><span>24</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$16&ndash;$103</span></div>
      <div class="sidebar-detail"><span class="l">Cheapest</span><span>St Andr&eacute;, $16</span></div>
      <div class="sidebar-detail"><span class="l">Checked</span><span>October 29, 2026</span></div>
      <div class="sidebar-detail"><span class="l">Vol. 1</span><span><a href="/drops/the-bold-tee-edit" style="border-bottom:1px solid currentColor;">The Bold Tee Edit</a></span></div>
      <a href="#back-prints" class="sidebar-cta">See the tees &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#GraphicTees</span>
        <span class="hashtag">#GolfStyle</span>
        <span class="hashtag">#IndependentGolf</span>
        <span class="hashtag">#TheGrassyIssue</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">disclosure</a></div>
  </aside>
</section>
"""
CLOSE = """
<section class="products" style="margin-top:8px;padding-top:48px">
  <div class="writeup-body" style="max-width:720px;margin:0 auto">
    <div class="drop-tag grass">The Last Word</div>
    <h2 class="products-hdr" id="last-word">Why the Graphic Tee Keeps Winning</h2>
    <p>A golf polo tells people you play golf. A good graphic tee tells them how you play it: whether you take it seriously, whether you laugh at the bad holes, whether you go home after 18 or stay for the 19th. That is why small brands keep putting their best ideas on a $40 tee. It&rsquo;s the cheapest way into a brand, and it&rsquo;s the piece people actually ask about.</p>
    <p>If you buy one tee from this page, make it a back print. Start with Hinotori if you want art, Dicey or SAHA if you want a laugh, and St Andr&eacute; if you want two tees for less than the price of one sleeve of balls. Then wear it to the course and walk slowly off the 18th green.</p>
  </div>
</section>
"""


def tile(k, n):
    brand, name, price, url, note = T[k]
    fr = FRN[k]; alt = H.unescape(f"{brand} {name}").replace('"', '')
    b = f'<img class="tw-b" src="{fr[1]}" alt="{H.escape(alt)}, other view" loading="lazy" />' if len(fr) > 1 else ''
    flip = '<span class="tw-flip" role="button" aria-label="Flip to see the other side">Flip</span>' if len(fr) > 1 else ''
    return (f'<div class="product-card tw-card" id="{k}"><a class="tw-tile{" has-b" if len(fr) > 1 else ""}" href="{url}" target="_blank" rel="noopener">'
            f'<div class="tw-img"><img class="tw-a" src="{fr[0]}" alt="{H.escape(alt)}" loading="lazy" />{b}<span class="tw-num">{n:02d}</span>{flip}</div>'
            f'<div class="tw-cap"><span class="tw-brand">{brand}</span><span class="tw-price">{price}</span></div>'
            f'<div class="tw-name">{name}</div><p class="tw-note">{note}</p><span class="tw-shop">Shop &#8599;</span></a></div>')


def band(key, kicker, items):
    figs = "".join(f'<figure><img src="{IMG}/{key}-{i}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>'
                   for i, (alt, cap) in enumerate(items, 1))
    return f'\n  <div class="tw-band"><p class="tw-band-k">{kicker}</p><div class="ig-grid">{figs}</div></div>\n'


def section(sec, n0):
    h2, anchor, ids, kicker, bands = sec
    out = (f'\n<section class="products" style="margin-top:8px;">\n  <div class="drop-tag grass">{len(ids)} tees</div>\n'
           f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n  <p class="cat-kicker">{kicker}</p>\n')
    start, n = 0, n0
    for cut, key, bk, items in bands + [(len(ids), None, None, None)]:
        chunk = ids[start:cut]
        if chunk:
            out += f'  <div class="products-grid" data-tw="1" data-n="{len(chunk)}">\n' + "\n".join(tile(k, n + j) for j, k in enumerate(chunk)) + '\n  </div>\n'
            n += len(chunk)
        if key: out += band(key, bk, items)
        start = cut
    return out + '</section>\n', n


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items, pos = [], 1
    for sec in SECTIONS:
        for k in sec[2]:
            items.append({"@type": "ListItem", "position": pos, "url": T[k][3], "name": H.unescape(f"{T[k][0]} {T[k][1]}")}); pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC, "url": URL, "image": og,
         "datePublished": DATE, "dateModified": DATE,
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": items},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Drops & Brands", "item": "https://thegrassyissue.com/#feed"},
            {"@type": "ListItem", "position": 3, "name": "The Graphic Tee Edit Vol. 2", "item": URL}]},
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
    ids = [k for s in SECTIONS for k in s[2]]
    NB = len({T[k][0] for k in ids}); NBACK = len(SECTIONS[0][2])
    assert len(ids) == N == len(set(ids)) and set(ids) == set(T), (len(ids), set(T) ^ set(ids))
    for k in ids: assert FRN.get(k), k
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  The Graphic Tee Edit Vol. 2</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>{N} tees &middot; {NB} brands</span><span class="dot"></span>
    <span>Prices checked October 29, 2026</span>
  </div>
</header>

<div class="drop-hero tw-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Three back prints worn on the course and the coast: the Hinotori Wilderness Club tee, the AXXA Too Cold To Golf tee at sunset and the Devereux Highway Driving Range tee" fetchpriority="high" /></div></div>
<div class="tw-stats"><span><b>{N}</b>tees</span><span><b>{NB}</b>brands</span><span><b>{NBACK}</b>back prints</span><span><b>$16</b>cheapest</span></div>
<div class="tw-jump"><a href="#back-prints">Back Prints &darr;</a><a href="#up-front">Up Front &darr;</a></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        o, n = section(s, n); body += o
    body += CLOSE
    out = head_top() + head_rest.replace("</head>", CSS + "</head>", 1) + body + tail.replace("</body>", JS + "</body>", 1)
    print(f"  {n-1} tees")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Kalamunda", "Aberdeen", "Swell Marks", "honky"):
        if leak in above: bad.append("leak " + leak)
    if fin.count('class="product-card tw-card"') != N: bad.append("card count")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", above), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
