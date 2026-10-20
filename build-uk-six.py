#!/usr/bin/env python3
"""build-uk-six.py — "6 UK independent golf brands that would look great on US soil". Cloned from build-rtg-revisit.py. 20 October 2026.
Lenny: Parmore + Three Putt + research others; "No on womens Famara... tone down the language to just be 6 UK Independent golf brands
that would look great on US soil"; "swap out SINK for FINK"; "I like Casualist, and Sounder" (Reflo and Fyfe dropped). Picks ours.
FACTS: each store's products.json (GBP, Oct 20, 2026); USD approx x1.34. Brand facts from our own Brand to Know posts (Parmore,
Casualist, Sounder), our Three Putt radar post, Son of Edmond's own site (est. 2025, British Wool licence Apr 2026, Son of Edmond Open
May 30 2026), v2 (Oct 20): FINK swapped for No Return Club (Lenny: "more interesting brand"); single hero (Sounder Devon); fresh quotes from brand sites + Golf Business News, none used in earlier posts; deeper TGI take. Sounder prices include sale markdowns.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "6 UK Independent Golf Brands That Belong in the US"
DESC = ("Parmore, Three Putt, Son of Edmond, Casualist, Sounder and No Return Club: six independent UK golf brands that would look great "
        "on an American course. 36 picks with prices in pounds and dollars.")
H1 = "Six UK Independent Golf Brands That Would Look Great on US Soil"
BC = "6 UK Golf Brands"
SLUG = "uk-independent-golf-brands"
IMG = "/images/uk-six"
SHOP = ""
P = {
 "p1": ('Parmore Golf', 'Camo Quarter-Zip', '&pound;65 (~$87)', 'https://parmoregolf.com/products/camo-1-4-zip-rebrand',
   'Parmore&rsquo;s own words: the boldest piece in the range. A realistic hunting camo with PARMORE arched across the chest in collegiate letters, cut as a relaxed stand-collar pullover. Loud on purpose, and it will turn heads at an American muni.'),
 "p2": ('Parmore Golf', 'Stripe Polo, Brown &amp; Cream or Olive &amp; White', '&pound;50 (~$67)', 'https://parmoregolf.com/products/brown-stripes-polo-rebrand',
   'Our pick from Parmore. Horizontal stripes with a solid contrast collar and cuffs, the small &ldquo;+&rdquo; mark on the chest and Parmore on the cuff. Relaxed and easy to wear well beyond the course.'),
 "p3": ('Parmore Golf', 'Capsule Windbreaker', '&pound;75 (~$100)', 'https://parmoregolf.com/products/long-sleeved-windbreaker-rebrand',
   'A khaki pullover windbreaker with cream ribbed trims, raglan sleeves, the &ldquo;+&rdquo; on the chest and the wordmark across the back. The wind layer for when style still matters, says Parmore.'),
 "p4": ('Parmore Golf', 'Cargo Pants', '&pound;65 (~$87)', 'https://parmoregolf.com/products/casual-pants-black',
   'Black paneled cargos with an elastic waist, a tapered leg and Parmore on the thigh pocket. The brand is clear these are not for the course, and that honesty is part of the appeal.'),
 "p5": ('Parmore Golf', 'No Membership Required Tee', '&pound;40 (~$54)', 'https://parmoregolf.com/products/parm-050',
   'The slogan in its loudest form: a sunlit fairway photo printed across a heavyweight 240gsm tee with No Membership Required in Parmore lime. The game belongs to whoever turns up.'),
 "p6": ('Parmore Golf', 'Parmore + Ripstop 5-Panel', '&pound;35 (~$47)', 'https://parmoregolf.com/products/parmore-embroidered-5-panel',
   'A charcoal ripstop cotton cap with the &ldquo;+&rdquo; in raised 3D embroidery and the wordmark on the side.'),
 "t1": ('Three Putt Golf Clothing', 'Contours Hoodie', '&pound;54.99 (~$74)', 'https://threeputtgolfclothing.co.uk/products/contours-golf-hoodie',
   'Our pick from Three Putt. The back print is a topographic map of a single green drawn in one continuous line, with the three-putt that named the brand hidden in it. Heavyweight and oversized.'),
 "t2": ('Three Putt Golf Clothing', 'Tee Time Tee', '&pound;30.99 (~$42)', 'https://threeputtgolfclothing.co.uk/products/tee-time-golf-t-shirt',
   'A cow on a chair with a proper brew, clubs beside it. The cow is where Three Putt started: a West Yorkshire field and the founder&rsquo;s grandad.'),
 "t3": ('Three Putt Golf Clothing', 'The Scenic Route Tee', '&pound;30.99 (~$42)', 'https://threeputtgolfclothing.co.uk/products/the-scenic-route-golf-t-shirt',
   'A hand-drawn course across the back: a golfer mid-swing, the clubhouse, pines, a cart and a low sun, with the cow carrying a bag on the chest.'),
 "t4": ('Three Putt Golf Clothing', 'The Caddie Retro Polo', '&pound;34.99 (~$47)', 'https://threeputtgolfclothing.co.uk/products/the-caddie-golf-polo',
   'Contrast tipping on the collar, placket and cuffs, and the cow on the chest with a bag over its shoulder. Three Putt&rsquo;s line: it never offers a read and takes none of the blame.'),
 "t5": ('Three Putt Golf Clothing', 'Dogleg Polo', '&pound;34.99 (~$47)', 'https://threeputtgolfclothing.co.uk/products/dogleg-golf-polo',
   'The bold one: 100% cotton with curved contrast panels sweeping over the shoulders and the round cow badge on the chest.'),
 "t6": ('Three Putt Golf Clothing', 'Three on the Green Sweatshirt', '&pound;37.99 (~$51)', 'https://threeputtgolfclothing.co.uk/products/three-on-the-green-golf-sweatshirt',
   'A 400gsm cotton crewneck with nothing but the small TPG flag on the chest. The quiet one, in cream, white, black and grey.'),
 "s1": ('Son of Edmond', 'Ilkley Moor Wool Blade Putter Cover', '&pound;39.95 (~$54)', 'https://sonofedmond.co.uk/products/ilkley-moor-wool-blade-putter-cover',
   'Our pick from Son of Edmond. Handmade in Yorkshire with a 100% British Wool lining and a brass magnet closure, in a tweed with a purple stripe the brand compares to summer heather on the moor.'),
 "s2": ('Son of Edmond', 'Waxed Cotton &amp; British Wool Blade Cover', '&pound;39.95 (~$54)', 'https://sonofedmond.co.uk/products/waxed-tan-with-british-wool',
   'Quilted waxed cotton outside, British Wool inside, finished with a brass magnet. Country-jacket materials on a putter cover.'),
 "s3": ('Son of Edmond', 'Houndstooth Headcover', '&pound;30 (~$40)', 'https://sonofedmond.co.uk/products/bradford-hounds-tooth-head-cover',
   'Handmade in Yorkshire from locally woven wool with a soft fleece lining. A brown houndstooth that looks like an old sport coat in the bag.'),
 "s4": ('Son of Edmond', 'British Wool Beanie', '&pound;34.95 (~$47)', 'https://sonofedmond.co.uk/products/british-wool-hats',
   'A fisherman-and-Arran style beanie, 100% British Wool and knitted in the UK, in a run of colors.'),
 "s5": ('Son of Edmond', 'Malham Wool Blade Putter Cover', '&pound;39.95 (~$54)', 'https://sonofedmond.co.uk/products/malham-wool-blade-putter-cover',
   'An intricate houndstooth the brand says recalls the rock formations at Malham, handmade in Yorkshire with a British Wool lining.'),
 "s6": ('Son of Edmond', 'Wool Scorecard Holder', '&pound;20 (~$27)', 'https://sonofedmond.co.uk/products/wool-score-card-green',
   'A little bit of Yorkshire in your back pocket: a scorecard holder in locally woven green wool with a pencil pouch on each side.'),
 "c1": ('Casualist', 'Wool Headcovers, with Mogshade', '&pound;90 (~$121)', 'https://casualist.com/products/wool-headcovers',
   'New this month: a headcover collab with Mogshade made from rescued Portuguese wool offcuts, woven in the Serra da Estrela mountains, with a fleece lining. Blue zigzag tweed.'),
 "c2": ('Casualist', 'Pleated Golf Trousers', '&pound;160 (~$214)', 'https://casualist.com/products/pleated-trousers',
   'Our pick from Casualist. Organic cotton twill with a high waist, clean pleats, a straight leg and a hidden drawstring, made in Portugal. The trouser for the course, the pub and the airport.'),
 "c3": ('Casualist', 'Trust the Swing Pique Polo', '&pound;115 (~$154)', 'https://casualist.com/products/trust-the-swing-pique-polo-olive',
   'A long-sleeve pique polo with a retro rounded collar and a relaxed fit, in olive or dusty blue. Casualist says it works in the clubhouse, the pub, and at that dinner you were slightly underdressed for.'),
 "c4": ('Casualist', 'Grazer Cardigan Vest', '&pound;185 (~$248)', 'https://casualist.com/products/grazer-cardigan-vest-grey',
   'A 100% merino button-front vest with a small embroidered logo and mascot and a caption on the back, made in Portugal. Grey or yellow.'),
 "c5": ('Casualist', 'Cart Path Ripstop Jacket', '&pound;240 (~$322)', 'https://casualist.com/products/cart-path-ripstop-jacket',
   'A light green ripstop jacket with back ventilation, an adjustable waist cord and CASUALIST across the shoulders.'),
 "c6": ('Casualist', 'Legacy Wool 5-Panel Cap', '&pound;45 (~$60)', 'https://casualist.com/products/legacy-wool-5-panel-cap',
   'Soft wool tartan with a rope across the brim and the C logo, in taupe or dark brown, inspired by caps from when golf was slower.'),
 "d1": ('Sounder', 'Pac Mach Jacket', '&pound;145 (~$194)', 'https://soundergolf.com/products/pac-mach-jacket-sea-blue-ripstop',
   'Ultra-light Japanese recycled ripstop that packs into its own drawstring bag, with zipped pockets and the Sounder star on the chest. Sea blue, lava red or deep navy. The jacket for windy Texas winter mornings.'),
 "d2": ('Sounder', 'Himalayas Fleece Jacket, Oat', '&pound;95 (~$127)', 'https://soundergolf.com/products/himalayas-fleece-jacket-oat',
   'Light Italian polar fleece with a two-way zip and a ball-marker patch, named for the Ladies putting course at St Andrews, not the mountains. On sale from &pound;185 when we checked.'),
 "d3": ('Sounder', 'Monterey Stripe Polo', '&pound;45 (~$60)', 'https://soundergolf.com/products/monterey-stripe-polo-in-indigo-and-slate',
   'Organic slub cotton stripes with a ribbed collar, made in Portugal and named for the Monterey Peninsula. Indigo, pine or red and navy, all marked down from &pound;85.'),
 "d4": ('Sounder', 'Capri Collar Polo', '&pound;85 (~$114)', 'https://soundergolf.com/products/capri-collar-polo-mint-natural',
   'Our pick from Sounder. An open-collar organic cotton polo with no buttons and the star on the chest, made in Portugal. Mint, white with spice, or navy.'),
 "d5": ('Sounder', 'Fuzzy Pocket Polo', '&pound;45 (~$60)', 'https://soundergolf.com/products/fuzzy-pocket-polo-in-navy-and-ecru',
   'Sounder&rsquo;s own slub jersey with a contrast patch pocket and a half-star, relaxed and made in Portugal. Navy and ecru or gold and charcoal, down from &pound;85.'),
 "d6": ('Sounder', 'Luxe Star Beanie', '&pound;45 (~$60)', 'https://soundergolf.com/products/luxe-star-beanie-gold',
   'A wool and cashmere rib beanie with a turn-up and the half-star embroidered on it. Gold, dark green or charcoal.'),
 "n1": ("No Return Club", 'Pink Lemonade Harris Tweed Headcover', '&pound;64.99 (~$87)', 'https://noreturnclub.co.uk/products/harris-tweed-pink-lemonade-headcover',
   'Our pick from No Return Club, and new this month. A pink and yellow Harris Tweed check with the new NRC monogram on top, lined in boiled black wool with hidden elastic so it stays on the club. Driver and wood sizes, in what NRC calls extremely limited quantities.'),
 "n2": ("No Return Club", 'Sub-Zero Blue Harris Tweed Headcover', '&pound;64.99 (~$87)', 'https://noreturnclub.co.uk/products/sub-zero-blue-harris-tweed-headcover',
   'Two-tone: a speckled light-gray top over a blue Harris Tweed weave, with the monogram stitched in ice blue. Same boiled-wool lining, same October 11 drop.'),
 "n3": ("No Return Club", 'Twisted Houndstooth Harris Tweed Headcover', '&pound;64.99 (~$87)', 'https://noreturnclub.co.uk/products/twisted-houndstooth-harris-tweed-headcover',
   'Black and white Harris Tweed houndstooth cut on a diagonal under a solid black top. The quietest of the three new covers.'),
 "n4": ("No Return Club", 'Purple Haze Wind Shirt', '&pound;74.99 (~$100)', 'https://noreturnclub.co.uk/products/wind-shirt-purple-haze',
   'Built, in NRC&rsquo;s words, for when the forecast can&rsquo;t make its mind up. A boxy waterproof nylon 3/4-zip with a mesh lining, underarm vents, a swing pocket and a hidden poacher&rsquo;s pocket.'),
 "n5": ("No Return Club", 'Skull Ball Marker, Collectors Edition', '&pound;25.99 (~$35)', 'https://noreturnclub.co.uk/products/ball-marker-brass-skull',
   'A collaboration with SinkGolf: solid brass with a patina that gets better with age, 38mm by 29mm, with a precision-milled back. Only 50 made.'),
 "n6": ("No Return Club", 'Pitchmark Repair Tool', '&pound;44.99 (~$60)', 'https://noreturnclub.co.uk/products/pitchmark-repair-tool',
   'CNC-milled from 303 stainless steel, hand finished with white paint, then torch heat-treated so the color shifts differently on every tool.'),
}
SECTIONS = [
 ("Parmore Golf", "parmore", ["p1","p2","p3","p4","p5","p6"],
  "<strong>Bournemouth &middot; six picks &middot; &pound;35&ndash;&pound;75</strong>A streetwear brand that happens to be about golf, started in 2024 and online only, with three words printed on half the range: No Membership Required. It ships to more than 40 countries."),
 ("Three Putt Golf Clothing", "three-putt", ["t1","t2","t3","t4","t5","t6"],
  "<strong>West Yorkshire &middot; six picks &middot; &pound;30.99&ndash;&pound;54.99</strong>Heavyweight cotton and hand-drawn back prints from a brand launched in 2025 by Graeme Whiles, who learned the game in his grandad&rsquo;s field. That&rsquo;s why a dairy cow turns up everywhere."),
 ("Son of Edmond", "son-of-edmond", ["s1","s2","s3","s4","s5","s6"],
  "<strong>Keighley, Yorkshire &middot; six picks &middot; &pound;20&ndash;&pound;39.95</strong>The newest brand here, established in 2025: headcovers handmade in Yorkshire from locally woven wool. It got a British Wool licence this spring and held its first Son of Edmond Open at Keighley Golf Club in May."),
 ("Casualist", "casualist", ["c1","c2","c3","c4","c5","c6"],
  "<strong>West London &middot; six picks &middot; &pound;45&ndash;&pound;240</strong>Elie Reboul&rsquo;s label, renamed from Casual Pro when the name needed to grow up. Quiet clothes for golf and after, most of it made in Portugal and cut closer than an American golf polo."),
 ("Sounder", "sounder", ["d1","d2","d3","d4","d5","d6"],
  "<strong>London &middot; six picks &middot; &pound;45&ndash;&pound;145</strong>Folk founder Cathal McAteer and former PGA pro James Day, who started Urban Golf, launched Sounder in 2021 on one idea: golf clothes don&rsquo;t need to look like golf clothes. Several pieces were marked down when we checked."),
 ("No Return Club", "no-return-club", ["n1","n2","n3","n4","n5","n6"],
  "<strong>Manchester &middot; six picks &middot; &pound;25.99&ndash;&pound;74.99</strong>The loudest accessories in British golf: skull and revolver ball markers, a slogan that says Play Golf Recklessly, and handmade headcovers in Scotland&rsquo;s Harris Tweed. Three new covers landed on October 11, and NRC says the handmade line won&rsquo;t be mass produced."),
]
N = 36
PQ = {
 "parmore": ("Why was golf apparel designed like it was still 1987?", "Parmore Golf, Our Story"),
 "three-putt": ("The balls were rubbish. The clubs were far too big and too heavy. But it was everything golf should be. Fun. Relaxed. Inclusive.", "Graeme Whiles, founder, Three Putt Golf Clothing"),
 "son-of-edmond": ("Crafted for golfers who notice the difference.", "Founder, Son of Edmond"),
 "casualist": ("The ones who show up in a proper cardigan on a drizzly Tuesday morning and mean it.", "Casualist, on who it makes clothes for"),
 "sounder": ("We believe the true spirit of golf is lost when we view it as an elite sport, rather than a game for everyone.", "James Day, Sounder co-founder, to Golf Business News, July 2022"),
 "no-return-club": ("Born as a source of inspiration for those seeking to break free from the shackles of mundane golf fashion.", "No Return Club, About Us"),
}
CAP = "Photography &middot; each brand&rsquo;s own"
BANDS = {}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Some of the most interesting golf clothing right now is coming out of the UK, and most of it still hasn&rsquo;t made it into American pro shops. These are six independent brands we think would look right at home on a US course, from a muni in Austin to a windy coastal track. Before the picks, here&rsquo;s what we think British brands do better than almost anyone.</p>
    <p><strong>They dress for weather, not for a catalogue.</strong> British golf is played in wind and rain most of the year, and it shows. Parmore&rsquo;s journal says UK weather &ldquo;changes by the hour,&rdquo; Three Putt picks fabrics for an exposed links in February, and No Return Club made a wind shirt for when the forecast can&rsquo;t make up its mind. Sounder named its fleece for the Himalayas putting course at St Andrews. You get light, packable layers that make sense together. That&rsquo;s exactly what a Texas winter round needs, when it starts cold and warms up by the turn.</p>
    <p><strong>They know their materials.</strong> Son of Edmond makes its headcovers from wool woven in Yorkshire mills and carries a British Wool licence. No Return Club covers its drivers in Harris Tweed, the cloth handwoven in Scotland&rsquo;s Outer Hebrides. Casualist and Sounder make most of their polos and knits in Portugal. Fabric is the story, and it&rsquo;s rare to see that from American golf brands at these prices.</p>
    <p><strong>They dress for the clubhouse and the pub.</strong> In Britain the round usually ends with a pint, so the clothes have to work off the course too. Three Putt says its clothes need to &ldquo;look right in the pub afterwards.&rdquo; Casualist&rsquo;s pleated trousers and Sounder&rsquo;s buttonless polo don&rsquo;t read as golf until you see the bag. That&rsquo;s the look American independents have been chasing for years, and the British have been dressing that way all along.</p>
    <p><strong>They poke fun at the members&rsquo; club.</strong> British golf still runs on clubs, dress codes and committees, and these brands push back with humor rather than anger. Look at the names: Three Putt and No Return Club. Then there&rsquo;s a cow on a chair drinking tea, and a brass skull for marking your ball. Parmore asks why golf clothes still look like 1987. It&rsquo;s the same instinct behind the best independent American brands, done in a drier accent.</p>
    <p><strong>They keep it small.</strong> Son of Edmond makes its covers by hand, No Return Club made 50 of its brass skull marker, and its newest Harris Tweed covers come in extremely limited quantities. Buy what you like when you see it; restocks aren&rsquo;t guaranteed.</p>
    <p>The six cover a lot of ground. <a href="/drops/brand-to-know-parmore-golf" style="border-bottom:1px solid var(--ink)">Parmore</a> and <a href="/drops/three-small-golf-brands-on-our-radar" style="border-bottom:1px solid var(--ink)">Three Putt</a> are streetwear first. <a href="/drops/brand-to-know-casualist" style="border-bottom:1px solid var(--ink)">Casualist</a> and <a href="/drops/brand-to-know-sounder" style="border-bottom:1px solid var(--ink)">Sounder</a> are the grown-up end. Son of Edmond and <a href="/drops/brand-to-know-no-return-club" style="border-bottom:1px solid var(--ink)">No Return Club</a> do the bag: wool and tweed headcovers, plus a few pieces of metal for your pocket.</p>
    <p>A few practical notes for American buyers: every price here is in pounds with an approximate dollar figure, sizes run British, and shipping and duties vary by brand, so check at checkout.</p>
    <p>If you buy one thing from each brand: the Parmore stripe polo, the Three Putt Contours hoodie, the Ilkley Moor putter cover, the Casualist pleated trousers, the Sounder Capri polo and the Pink Lemonade cover from No Return Club.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>Six, all independent</span></div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>Six each, 36 in all</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>&pound;20&ndash;&pound;240 (~$27&ndash;$322)</span></div>
      <div class="sidebar-detail"><span class="l">Newest</span><span>Son of Edmond, est. 2025</span></div>
      <div class="sidebar-detail"><span class="l">Currency</span><span>GBP, approx. USD shown</span></div>
      <div class="hashtags">
        <span class="hashtag">#UKGolf</span>
        <span class="hashtag">#IndieGolf</span>
        <span class="hashtag">#GolfStyle</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("Which UK golf brands should Americans know?", "Our six: Parmore (Bournemouth), Three Putt Golf Clothing (West Yorkshire), Son of Edmond (Keighley, Yorkshire), Casualist (West London), Sounder (London) and No Return Club (Manchester). All are independent."),
 ("Do these UK golf brands ship to the US?", "Prices are listed in pounds on each store; shipping costs and any import duties vary by brand, so check at checkout."),
 ("What is Son of Edmond?", "A Yorkshire brand established in 2025 that handmakes headcovers and putter covers from locally woven and British Wool fabrics, priced around £30–£40 (about $40–$54) on October 20, 2026."),
 ("What is No Return Club?", "A Manchester golf accessories brand known for skull and revolver-style ball markers and handmade Harris Tweed headcovers. Its newest Harris Tweed covers were £64.99 (about $87) on October 20, 2026."),
 ("Who is behind Sounder?", "Cathal McAteer, founder of the menswear label Folk, and James Day, a former PGA professional who founded Urban Golf in London. They launched Sounder in March 2021."),
]
LOOKBOOK = f"""
<section class="products" style="margin-top:8px;">
  <div class="drop-tag grass">Lookbook</div>
  <h2 class="products-hdr" id="lookbook">In the Wild</h2>
  <p class="cat-kicker"><strong>Lookbooks and real life &middot; twelve photos</strong>Campaign shots and phone photos from the brands themselves: links greens, Yorkshire stone walls, a beach in a wind jacket and a fire after the round.</p>
  <div class="ig-grid">
  <figure><img src="{IMG}/lb-sounder-22.jpg" alt="Four golfers in Sounder shaking hands on a links green" loading="lazy" /><figcaption class="ig-cap">Sounder &middot; a four-ball on the green</figcaption></figure>
  <figure><img src="{IMG}/lb-p14.jpg" alt="A golfer in the Parmore stripe polo with a carry bag in front of Big Ben" loading="lazy" /><figcaption class="ig-cap">Parmore &middot; stripe polo, Westminster</figcaption></figure>
  <figure><img src="{IMG}/lb-s20.jpg" alt="A Son of Edmond tweed putter cover on a club on the course" loading="lazy" /><figcaption class="ig-cap">Son of Edmond &middot; Ilkley Moor cover, on the course</figcaption></figure>
  <figure><img src="{IMG}/lb-c33.jpg" alt="A golfer in a yellow Casualist cardigan vest mid-swing in long grass" loading="lazy" /><figcaption class="ig-cap">Casualist &middot; Grazer vest at golden hour</figcaption></figure>
  <figure><img src="{IMG}/lb-n18.jpg" alt="Two No Return Club Harris Tweed headcovers on clubs in a bag against concrete" loading="lazy" /><figcaption class="ig-cap">No Return Club &middot; Harris Tweed in the bag</figcaption></figure>
  <figure><img src="{IMG}/lb-bi-sounder-scotland-2840.jpg" alt="A golfer in Sounder trousers seen through a drainage tunnel on a links course" loading="lazy" /><figcaption class="ig-cap">Sounder &middot; Scotland shoot</figcaption></figure>
  <figure><img src="{IMG}/lb-s3.jpg" alt="A stack of Son of Edmond British Wool beanies on a dry-stone wall above green fields" loading="lazy" /><figcaption class="ig-cap">Son of Edmond &middot; British Wool beanies</figcaption></figure>
  <figure><img src="{IMG}/lb-p35.jpg" alt="A man in the green Parmore quarter-zip on a narrow city street" loading="lazy" /><figcaption class="ig-cap">Parmore &middot; quarter-zip, off the course</figcaption></figure>
  <figure><img src="{IMG}/lb-c27.jpg" alt="A man in a Casualist pique polo standing in coastal dune grass" loading="lazy" /><figcaption class="ig-cap">Casualist &middot; in the dune grass</figcaption></figure>
  <figure><img src="{IMG}/lb-pach-mach-beach.jpg" alt="A golfer in a red Sounder Pac Mach jacket swinging on a beach" loading="lazy" /><figcaption class="ig-cap">Sounder &middot; Pac Mach jacket on the beach</figcaption></figure>
  <figure><img src="{IMG}/lb-s34.jpg" alt="A quilted Son of Edmond putter cover against a moorland sky at dusk" loading="lazy" /><figcaption class="ig-cap">Son of Edmond &middot; waxed cotton cover at dusk</figcaption></figure>
  <figure><img src="{IMG}/lb-s38.jpg" alt="A man by an open fire in a Son of Edmond Golf Club T-shirt" loading="lazy" /><figcaption class="ig-cap">Son of Edmond &middot; after the round</figcaption></figure>
  </div>
</section>
"""

FRN = json.loads((ROOT / "research/uk-six/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-R3-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
def card(k, idx):
    brand, item, price, handle, copy = P[k]
    url = SHOP + handle
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
            items.append({"@type": "ListItem", "position": pos, "url": SHOP + P[h][3], "name": H.unescape(f"{P[h][0]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-10-20", "dateModified": "2026-10-20",
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


def section(sec, n0):
    h2, anchor, ids, kicker = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} {"pick" if len(ids)==1 else "picks"}</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def main(apply_):
    ids = [k for s in SECTIONS for k in s[2]]
    assert len(ids) == N == len(set(ids)) and set(ids) == set(P), (len(ids), set(P) ^ set(ids))
    for k in ids:
        assert FRN[k] and all((ROOT / f.lstrip("/")).is_file() for f in FRN[k]), k
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Six independent brands &middot; London, Manchester, Yorkshire and the south coast</span><span class="dot"></span>
    <span>36 picks &middot; prices in pounds, checked October 20, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A golfer mid-swing on a grassy links dune in Devon under a wide evening sky, from Sounder&rsquo;s own photography" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
    body += LOOKBOOK
    body += faq_html()
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Kalamunda", "Dim Sum", "Rowena", "Metalwood", "Climber", "Woodgrain", "Rookline", "Bethpage", "LBB", "GolfPass"):
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
