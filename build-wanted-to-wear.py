#!/usr/bin/env python3
"""build-wanted-to-wear.py — "Everyone made the golf clothes they wanted to wear. Here's what they actually made." 12 October 2026.
Lenny noticed how many brands say a version of "We wanted to make golf clothes that we actually wanted to wear", then
"that's a great idea for a post- build it", then "needs more everything" (v2: 14 brands, 27 picks, the gap/answer table,
four pull quotes, grouped by what "wanted to wear" turned out to mean).
FACTS: founding lines are verbatim quotes or paraphrases already published on TGI (each brand's own post); publication
names are not repeated. Products and prices read live on each brand's store, October 12, 2026. Conversions: GBP x1.3234,
AUD x0.70, NZD x0.57, ZAR x0.055; where a brand charges US customers a set dollar price, that price is shown second.
PHOTOS: each brand's own; many frames reused from TGI's earlier posts (research/wanted-to-wear/frame.py).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "The Golf Clothes They Wanted to Wear: 17 Brands, One Origin Story"
DESC = ("Seventeen independent golf brands started with the same sentence: we made what we wanted to wear. "
        "Here is what each one actually made, 33 pieces from a 1962 knit headcover to camo quarter-zips.")
H1 = "Everyone Made the Golf Clothes They Wanted to Wear. Here&rsquo;s What They Actually Made."
BC = "The Clothes They Wanted to Wear"
SLUG = "golf-brands-clothes-they-wanted-to-wear"
IMG = "/images/wanted-to-wear"
SHOP = ""
def cc(line, made): return f"<strong>The line:</strong> {line}<br><br><strong>What they made:</strong> {made}"
def more(slug, label): return f' More in <a href="/drops/{slug}">{label}</a>.'
SAME = "<strong>Same brand, second answer.</strong> "
P = {
 # The Originals
 "jancraig": ("Jan Craig Headcovers", "Driver Headcover, Navy &amp; White", "$79", "https://www.jancraigheadcovers.com/driver-460-headcover-8-in-pom-1-stripe-navy-white/",
   cc("In 1962 Jan Craig, an avid golfer outside Cincinnati, could not find headcovers she liked, so she knitted her own.",
      "The same cover, more than sixty years on: hand-knit in the USA from 100% worsted wool with a big pom on top. The brand says the only change to Jan&rsquo;s design is elastic inside the driver cover. Jack Nicklaus ordered a set in the mid-sixties." + more("golf-brands-founded-by-women", "our women-founded brands guide"))),
 "smathers": ("Smathers &amp; Branson", "Golf Tee Pattern Needlepoint Belt", "$195", "https://smathersandbranson.com/products/golf-tee-pattern-belt",
   cc("Two roommates at Bowdoin in 2004 were each given a needlepoint belt and could not find anywhere to buy another.",
      "So they made them: 100% hand-stitched needlepoint, lined in Italian leather, with a solid brass buckle and a wooden gift box. This one is golf tees on dark navy. The brand now holds USGA and Ryder Cup licenses." + more("the-needlepoint-belt-report", "The Needlepoint Belt Report"))),
 "smathers2": ("Smathers &amp; Branson", "Crossed Clubs Needlepoint Ball Marker", "$22.50", "https://smathersandbranson.com/products/crossed-clubs-golf-ball-marker",
   SAME + "The belt idea, shrunk to the size of a coin: two crossed clubs stitched in needlepoint on classic navy. It is the cheapest piece on this page and the one that will match the belt." + more("small-golf-accessories-small-things-big-impact", "our small accessories roundup")),
 "ashworth1": ("Ashworth Golf", "The O.G. Polo", "$98", "https://www.ashworth-golf.com/products/the-o-g-polo-white-denim",
   cc("John Ashworth co-founded the company in California in 1987 as a relaxed alternative to the polyester golf wore then.",
      "A roomier cotton polo with a walking-golfer logo, and Fred Couples in it. The O.G. is the brand&rsquo;s update of that first polo, white with denim tipping, in a cotton-performance blend. John Ashworth came back as creative director in 2024." + more("brand-to-know-ashworth", "our Ashworth Brand to Know"))),
 "ashworth2": ("Ashworth Golf", "1987 Golfman Hoodie", "$115", "https://www.ashworth-golf.com/products/1987-golfman-hoodie-grey-heather",
   SAME + "The Golfman, the walking-golfer logo from 1987, above the kangaroo pocket of a soft grey hoodie. The original California-casual idea, for the drive home."),
 "criquet1": ("Criquet", "Classic Players Shirt, Navy Microstripe", "$98", "https://criquetshirts.com/products/classic-players-shirt-navy-microstripe",
   cc("Billy Nachman and Hobson Brown grew up in prep-school polos and coat-and-tie dress codes. In Austin in 2010 they rebuilt a vintage golf shirt from Nachman&rsquo;s grandfather&rsquo;s closet.",
      "A golf shirt that passes as a shirt: 100% pima cotton, a four-button placket, a chest pocket and removable collar stays so the points never curl. Still $98, fifteen years on." + more("brand-to-know-criquet", "our Criquet Brand to Know"))),
 "criquet2": ("Criquet", "Throwback Players Shirt, Navy", "$104", "https://criquetshirts.com/products/throwback-players-shirt-navy",
   SAME + "The brand calls it the Classic Players Shirt &ldquo;with its hair slicked back a little bit&rdquo;: the same pima cotton with contrast piping. S, M and L in stock."),
 "seamus1": ("Seamus Golf", "Irish National Tartan Driver", "$130", "https://www.seamusgolf.com/products/irish-national-tartan-headcovers",
   cc("Akbar Chisti&rsquo;s wool headcover from a famous links club had worn through. In 2011 his wife Megan, a designer at Pendleton, remade it from fabric remnants, then made a few more for his golf group.",
      "Headcovers cut and sewn in Beaverton, Oregon, in registered tartans and mill wool. The Irish National tartan is green with black, yellow and white in the overplaid." + more("brand-to-know-seamus", "our Seamus Brand to Know"))),
 "seamus2": ("Seamus Golf", "Navy Harris Tweed Blade Putter Cover", "$130", "https://www.seamusgolf.com/products/navy-harris-tweed-magnet-putter-cover",
   SAME + "Hand-woven Harris Tweed from the Outer Hebrides in a navy herringbone, with a magnetic closure. The worn-out links cover, put back together properly."),
 # Something older
 "woodgrain": ("Woodgrain Golf", "Legacy Double Pleated Trouser, Cream", "$180", "https://woodgrain.golf/products/relaxed-double-pleated-trouser",
   cc("&ldquo;We wanted to make golf clothes that we actually wanted to wear.&rdquo; &mdash; Christian &amp; Em, the founders. The sentence this whole post is named after.",
      "The golf look from old photos: a wide, 100% cotton trouser with two deep pleats a side, cut to hang like 1992." + more("brand-to-know-woodgrain-golf", "our Woodgrain Brand to Know"))),
 "woodgrain2": ("Woodgrain Golf", "Wool Hat", "$49", "https://woodgrain.golf/products/wool-hat",
   SAME + "A five-panel cap in brown plaid wool with a 3D WG on the front and a green lining printed &ldquo;Swing smooth, Dress sharp.&rdquo; The easiest way into the look."),
 "latenine": ("Late Nine", "Cable Knit Polo, Burgundy", "2,950 SEK &middot; US $387", "https://late-nine.com/products/cable-knit-polo-burgundy",
   cc("&ldquo;There was a specific aesthetic we wanted to wear that we felt wasn&rsquo;t really available,&rdquo; co-founder Maxim Lundh said. The name is the time of day he could actually get a round in.",
      "Quiet Stockholm luxury: a long-sleeved polo cable-knit from first-shearing merino, lightly brushed, with an oversized 70s collar. S and M in stock." + more("late-nine-stockholm-relaxed-fits-and-the-quiet-part-of-golf", "our Late Nine post"))),
 "latenine2": ("Late Nine", "Double Pleat Slacks, Dark Brown", "3,200 SEK &middot; US $427", "https://late-nine.com/products/double-pleat-slacks-dark-brown",
   SAME + "Italian four-season wool, a full straight leg and outward-facing double pleats, with an unlined waistband. The second brand here to decide the answer was pleats; this pair is wool and costs more than twice Woodgrain&rsquo;s."),
 "oddritual": ("Odd Ritual Golf", "1990s Heritage Polo", "R 950 (~$52)", "https://oddritualgolf.com/products/1990s-heritage-polo",
   cc("The founders went looking in Cape Town for a local golf brand that spoke to them and could not find one. Their words: &ldquo;A brand for people who love the game but want to feel like themselves on the course.&rdquo;",
      "A 200gsm cream pique polo with a navy nylon collar and cuffs, cut oversized with a dropped shoulder. Marked down from R 1,650 when we checked; L, XL and 2XL left." + more("brand-to-know-odd-ritual", "our Odd Ritual Brand to Know"))),
 "oddritual2": ("Odd Ritual Golf", "The Caddie Jacket, Navy", "R 1,900 (~$105)", "https://oddritualgolf.com/products/the-caddie-jacket-navy",
   SAME + "A 230gsm cotton twill jacket with a washed cotton lining, a YKK zip and quiet embroidered branding, named for the jackets caddies wear. Down from R 3,200, every size in stock."),
 "manors": ("Manors Golf", "Course Polo", "$86", "https://manorsgolf.com/products/course-polo",
   cc("Two London school friends started Manors in 2019 because they could not find clothes they wanted to play in. &ldquo;We didn&rsquo;t need a technical polo,&rdquo; co-founder Jojo Regan said in 2021.",
      "The twist: the Course Polo 2.0 is now exactly that, in Seawool made from recycled oyster shells and plastic bottles, with UV 50+ protection and moisture management. The look stayed retro; the fabric caught up." + more("brand-to-know-manors", "our Manors Brand to Know"))),
 "manors2": ("Manors Golf", "Lightweight Pleated Trouser", "$172", "https://manorsgolf.com/products/greenskeeper-chino-trousers",
   SAME + "A double-pleated golf chino in water-resistant stretch fabric, with a ticket pocket for the scorecard. Retro shape, modern cloth, the whole Manors story in one pair of trousers."),
 # Something louder
 "parmore": ("Parmore Golf", "Camo Quarter-Zip", "&pound;65 &middot; US $100", "https://parmoregolf.com/products/camo-1-4-zip-rebrand",
   cc("Parmore says it began with people who could not find golf clothes they wanted to wear off the course, &ldquo;not as a designer or a fashion people, but as people who play golf.&rdquo;",
      "Streetwear with no apology: hunting camo with a giant collegiate PARMORE across the chest. The loudest answer on this page." + more("brand-to-know-parmore-golf", "our Parmore Brand to Know"))),
 "parmore2": ("Parmore Golf", "Stripe Polo, Brown &amp; Cream", "&pound;50 &middot; US $78", "https://parmoregolf.com/products/brown-stripes-polo-rebrand",
   SAME + "The quiet side of the same brand: a boxy 240gsm stripe polo with a brown contrast collar and a small cross on the chest. Shot outside the Houses of Parliament."),
 "devereux": ("Devereux Golf", "Disco Rodeo Polo, Bone", "$74", "https://devereuxgolf.com/products/disco-rodeo-polo-bone",
   cc("&ldquo;It all came from when I played, thinking, &lsquo;What can I wear?&rsquo;&rdquo; co-founder Robert Brunner said. He and his brother Will named the brand after their grandmother in 2013.",
      "Polos with personality: a stretch pique in bone with a wavy all-over print, the performance side of the Fall drop." + more("brand-to-know-devereux-golf", "our Devereux Brand to Know"))),
 "devereux2": ("Devereux Golf", "Mechanic Short-Sleeve Quarter-Zip", "$104", "https://devereuxgolf.com/products/mechanic-qtr-zip-faded-black-pinstripe",
   SAME + "Based on the short-sleeved windbreakers of the 1990s and cut in a faded black conductor stripe. Only M and XL left."),
 "howie1": ("Howie Benson", "Resort Camp Collar Polo, Brunette", "$108", "https://howiebenson.com/products/resort-camp-collar-polo-brunette",
   cc("Howie Benson says it was started &ldquo;because we couldn&rsquo;t find what we were looking for.&rdquo; It names no founder and lists New York, Boston and San Diego as home.",
      "A resort shirt rebuilt to play 18: the camp collar and easy fit of a vacation shirt, in a textured stretch knit. Their tagline is &ldquo;Taste over Tradition.&rdquo;" + more("brand-to-know-howie-benson", "our Howie Benson Brand to Know"))),
 "howie2": ("Howie Benson", "Single Button Polo Pullover, Brown", "$118", "https://howiebenson.com/products/single-button-pullover-brown",
   SAME + "The brand calls it &ldquo;the layer that doesn&rsquo;t look like every other quarter-zip&rdquo;: a midweight textured pullover with a clean one-button collar."),
 # Something from home
 "fyfe1": ("Fyfe Golf", "Black Grouse Harris Tweed Headcover", "&pound;65 (~$86)", "https://www.fyfegolf.com/products/black-grouse",
   cc("Neil Rennie walked into Scottish pro shops and found nothing that had anything to do with Scotland. &ldquo;I couldn&rsquo;t find that more elevated product, with heritage and provenance.&rdquo;",
      "Headcovers handmade in Scotland from Harris Tweed. Black Grouse is a black and white houndstooth with a red fleece lining, for a driver or fairway wood." + more("brand-to-know-fyfe-golf", "our Fyfe Brand to Know"))),
 "fyfe2": ("Fyfe Golf", "The Brave Copper Ball Marker", "&pound;25 (~$33)", "https://www.fyfegolf.com/products/the-brave-copper-hand-forged-ball-marker",
   SAME + "Hand-forged in copper by a swordsmith at a Scottish forge that still makes battle swords, with the Lion Rampant and the Saltire on the face. Provenance you can put on a green."),
 "localgc1": ("Local GC", "Mallard Wool Headcover", "NZ$110 (~$63)", "https://www.localgc.co.nz/product/mallard-wool-head-cover",
   cc("Myles Brock says he started Local GC in his workshop north of Auckland because he &ldquo;found a hole in the market when it came to locally made, quality headcovers.&rdquo;",
      "Made-to-order covers from a one-man shop. This one has a mallard on a forest green wool outer, made to order in seven to ten days." + more("brand-to-know-local-gc", "our Local GC Brand to Know"))),
 "localgc2": ("Local GC", "Black and Red Tartan Headcovers", "NZ$99 (~$56)", "https://www.localgc.co.nz/product/black-and-red-tartan-headcovers",
   SAME + "A black and red tartan wool blend, made to order in slip-on or barrel shapes for a driver, wood or hybrid."),
 "lof": ("Left of Field Golf", "Bridgewater 1/4 Zip", "A$270 &middot; US $205", "https://lofgolf.com/products/bridgewater-1-4-zip",
   cc("&ldquo;When I first started playing the game, getting dressed for golf felt like a lose-lose situation,&rdquo; founder Nick Ilias said. &ldquo;The outfits I wanted to wear made me feel out of place in the pro shop.&rdquo;",
      "Clean Australian layers that sit in between: a nylon-spandex quarter-zip in sky blue with contrast stitching." + more("brand-to-know-left-of-field-golf", "our Left of Field Brand to Know"))),
 "lof2": ("Left of Field Golf", "Mornington Polo, Beige/White Stripe", "A$150 (~$105)", "https://lofgolf.com/products/mornington-polo-beige-white-stripe",
   SAME + "Extended sleeves and a wider, boxier cut that nods to golf&rsquo;s golden era, in a soft beige and white stripe. M, L and XL in stock."),
 "olydoe": ("Olydoe", "OG Supima Hollow Polo", "$110", "https://olydoe.com/products/og-supima-hollow-golf-polo-1",
   cc("Scott Matthews was an investment banker in New York who could not find a cotton polo he wanted to wear on a golf course. He calls the brand an &ldquo;anti-polyester manifesto.&rdquo;",
      "A cotton polo that works like a performance one: American-grown Supima with hollow-core yarns that move moisture off the skin. The brand is based in Dallas and launched in 2025." + more("brand-to-know-olydoe", "our Olydoe Brand to Know"))),
 "olydoe2": ("Olydoe", "Pleated Walker Pant", "$115", "https://olydoe.com/products/pleated-walker-pant",
   SAME + "No polyester here either: a lightweight blend of cotton, Tencel and linen, pleated, for a humid round. Every size from 30 to 38 in stock."),
 # Something that fit
 "huega1": ("Huega House", "Icon Performance Hat, Black", "$49", "https://huegahouse.com/products/black-icon-performance",
   cc("Jonathan Ruley and former Green Bay Packers linebacker Jake Ryan, future brothers-in-law, could not find a hat that fit right. In 2022 they split $10,000 and made their own.",
      "Hats that fit, first and foremost: a structured performance cap with a moisture-wicking sweatband and perforated side panels. By mid-2024 the brand was doing $2.3 million a year with no outside money." + more("brand-to-know-huega-house", "our Huega House Brand to Know"))),
 "huega2": ("Huega House", "Athletics Hat, Vintage Camo", "$45", "https://huegahouse.com/products/athletics-vintage-camo",
   SAME + "The mid-profile Athletics crown in a washed-out camo that reads like a 1990s hunting catalog. The fit is the point; the camo is the fun."),
}
SECTIONS = [
 ("The Originals", "originals", ["jancraig", "ashworth1", "ashworth2", "smathers", "smathers2", "criquet1", "criquet2", "seamus1", "seamus2"],
  "<strong>Nine picks &middot; 1962 to 2011</strong>Long before it was a pitch-deck line, it was a golfer with knitting needles, a California polo, two college roommates with one belt each, a grandfather&rsquo;s shirt and a worn-out headcover."),
 ("Something Older", "older", ["woodgrain", "woodgrain2", "latenine", "latenine2", "oddritual", "oddritual2", "manors", "manors2"],
  "<strong>Eight picks &middot; four brands</strong>For these founders, &ldquo;what we wanted to wear&rdquo; turned out to be what golfers wore before 2000: pleats, cable knits, contrast collars and caddie jackets."),
 ("Something Louder", "louder", ["parmore", "parmore2", "devereux", "devereux2", "howie1", "howie2"],
  "<strong>Six picks &middot; three brands</strong>For these, it meant personality: camo, prints, resort collars and conductor stripes."),
 ("Something From Home", "from-home", ["fyfe1", "fyfe2", "localgc1", "localgc2", "lof", "lof2", "olydoe", "olydoe2"],
  "<strong>Eight picks &middot; four brands</strong>For these, it meant provenance: Harris Tweed from Scotland, wool covers from a New Zealand workshop, Australian layers and American Supima cotton."),
 ("Something That Fit", "fit", ["huega1", "huega2"],
  "<strong>Two picks &middot; one brand</strong>And sometimes it was simpler than taste. Sometimes the hat just did not fit."),
]
N = 33
PQ = {
 "originals": ("We wanted to make golf clothes that we actually wanted to wear.", "Woodgrain Golf, and nearly everyone else"),
 "older": ("There was a specific aesthetic we wanted to wear that we felt wasn&rsquo;t really available.", "Maxim Lundh, Late Nine co-founder"),
 "louder": ("It all came from when I played, thinking, &lsquo;What can I wear?&rsquo;", "Robert Brunner, Devereux co-founder"),
 "from-home": ("Going around the pro shops and golf retailers, I couldn&rsquo;t find that more elevated product, with heritage and provenance.", "Neil Rennie, Fyfe Golf founder"),
}
CAP = ""
BANDS = {}
ROWS = [
 ("Jan Craig Headcovers", "Headcovers she liked", "Hand-knit wool covers, since 1962"),
 ("Ashworth Golf", "An alternative to polyester", "A roomier cotton polo, 1987"),
 ("Smathers &amp; Branson", "A second needlepoint belt", "Hand-stitched belts and accessories"),
 ("Criquet", "A shirt that passes as a shirt", "Grandad&rsquo;s vintage golf shirt, rebuilt"),
 ("Seamus Golf", "A replacement for a worn-out cover", "Headcovers sewn in Oregon"),
 ("Woodgrain Golf", "Golf clothes they wanted to wear", "Wide double-pleated trousers"),
 ("Late Nine", "A specific aesthetic", "Merino knits and wool slacks"),
 ("Odd Ritual Golf", "A local brand that spoke to them", "1990s-style polos and caddie jackets"),
 ("Manors Golf", "Clothes they wanted to play in", "Retro shapes, now in technical fabric"),
 ("Parmore Golf", "Clothes to wear off the course", "Camo quarter-zips and streetwear"),
 ("Devereux Golf", "&ldquo;What can I wear?&rdquo;", "Printed polos and 90s windbreakers"),
 ("Howie Benson", "&ldquo;What we were looking for&rdquo;", "Resort-collar polos"),
 ("Fyfe Golf", "Heritage and provenance", "Harris Tweed made in Scotland"),
 ("Local GC", "Locally made headcovers", "One-man-workshop covers, made to order"),
 ("Left of Field Golf", "Not out of place in the pro shop", "Clean Australian layers"),
 ("Olydoe", "A cotton golf polo", "Supima and linen, no polyester"),
 ("Huega House", "A hat that fit", "Hats, then everything else"),
]
TABLE = ("<style>/*TGI-WTW-TABLE*/#the-gap{padding:40px 20px 8px;border-top:1px solid var(--ink,#141414)}#the-gap .table-inner{max-width:1040px;margin:0 auto}#the-gap .table-h2{font-family:var(--serif,Georgia,serif);font-size:clamp(22px,3vw,30px);text-align:center;margin:0 0 6px}#the-gap .table-sub{font-family:var(--mono,monospace);font-size:10px;letter-spacing:.14em;text-transform:uppercase;text-align:center;opacity:.6;margin-bottom:18px}#the-gap .table-wrap{overflow-x:auto}#the-gap table{width:100%;border-collapse:collapse;min-width:560px;font-size:14px}#the-gap th{font-family:var(--mono,monospace);font-size:10px;letter-spacing:.12em;text-transform:uppercase;text-align:left;border-bottom:1px solid var(--ink,#141414);padding:8px 10px}#the-gap td{padding:10px;border-bottom:.5px solid rgba(20,20,20,.18);vertical-align:top}#the-gap td.course-name{font-weight:600}</style>\n<section id=\"the-gap\">\n  <div class=\"table-inner\">\n"
         "    <h2 class=\"table-h2\">Seventeen brands, one sentence &mdash; and seventeen answers.</h2>\n"
         "    <div class=\"table-sub\">What each founder said was missing, and what they made instead</div>\n"
         "    <div class=\"table-wrap\">\n      <table>\n        <thead>\n          <tr>\n            <th>Brand</th>\n            <th>What they couldn&rsquo;t find</th>\n            <th>What they made</th>\n          </tr>\n        </thead>\n        <tbody>\n"
         + "\n".join(f"          <tr>\n            <td class=\"course-name\">{b}</td>\n            <td>{g}</td>\n            <td>{m}</td>\n          </tr>" for b, g, m in ROWS)
         + "\n        </tbody>\n      </table>\n    </div>\n  </div>\n</section>\n")
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Read enough About pages and you start to hear the same sentence. <em>We couldn&rsquo;t find golf clothes we wanted to wear, so we made them.</em> It is the founding story of almost every independent golf brand we cover, and we have printed versions of it again and again on this site, most recently this week, in our Woodgrain post, before we noticed.</p>
    <p>The sentence is true, which is why it keeps coming up. For decades the choice in a pro shop was a shiny performance polo with a big logo on the chest, and the people who started these brands were simply the ones who got fed up first. But the line tells you nothing about the brand. What does tell you something is what each founder decided they wanted.</p>
    <p>So we went back through our own coverage and found seventeen brands with the same origin story. They split, almost neatly, into four answers. Some wanted <strong>something older</strong>: pleats, cable knits and the clothes from 1990s golf photos. Some wanted <strong>something louder</strong>: camo, prints and resort collars. Some wanted <strong>something from home</strong>: Harris Tweed, New Zealand wool, Supima cotton. And one just wanted <strong>a hat that fit</strong>. Below, each brand&rsquo;s line in their words or ours, then two pieces that show what they actually made.</p>
    <h2 class="products-hdr btk-story-hdr">How to Read the Sentence</h2>
    <p>When a brand tells you it made what it wanted to wear, the useful question is: wanted instead of what? Woodgrain wanted the trousers from old tournament photos instead of a slim five-pocket. Olydoe wanted cotton instead of polyester. Fyfe wanted Scotland instead of mass-produced. Huega House wanted a hat that sat right on the head. The answer to that question is the brand. The sentence is just the doorway.</p>
    <p>All 33 pieces were in stock on each brand&rsquo;s own store on October 12, 2026. Prices are in each store&rsquo;s currency, with an approximate dollar figure; where a brand charges US customers a set dollar price, that is shown second instead.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>Seventeen</span></div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>33</span></div>
      <div class="sidebar-detail"><span class="l">Oldest</span><span>Jan Craig, 1962</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$22.50&ndash;US $427</span></div>
      <div class="sidebar-detail"><span class="l">Loudest</span><span>Parmore Camo Quarter-Zip</span></div>
      <div class="sidebar-detail"><span class="l">Quietest</span><span>Late Nine Cable Knit Polo</span></div>
      <div class="sidebar-detail"><span class="l">Simplest reason</span><span>Huega House: the hat didn&rsquo;t fit</span></div>
      <a href="#the-gap" class="sidebar-cta">See the table &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#IndependentGolf</span>
        <span class="hashtag">#GolfStyle</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#WhatWeWantedToWear</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
""" + TABLE
FAQ = [
 ("Why do so many golf brands say they made clothes they wanted to wear?", "Because for decades golf clothing mostly meant shiny performance polos from a few big companies. Independent brands started when golfers who wanted something else, from knit headcovers and pleated trousers to streetwear and Harris Tweed, made it themselves."),
 ("Which golf brand on this list is the oldest?", "Jan Craig Headcovers. Jan Craig started hand-knitting her own covers in 1962 because she could not find any she liked, and the covers are still hand-knit in the USA."),
 ("Which brands make golf clothes without polyester?", "Olydoe calls itself an anti-polyester brand and makes Supima cotton polos and cotton, Tencel and linen trousers. Odd Ritual's Heritage Polo is a cotton pique, and Late Nine works in merino and Italian wool."),
 ("Which brands here make pleated golf trousers?", "Woodgrain (the Legacy Double Pleated Trouser, $180), Late Nine (Double Pleat Slacks in Italian wool), Manors (the Lightweight Pleated Trouser, $172) and Olydoe (the Pleated Walker Pant, $115)."),
 ("How much do these pieces cost?", "On October 12, 2026 they ran from $22.50 (Smathers & Branson's needlepoint ball marker) to US $427 (Late Nine's wool slacks), with most between $50 and $200."),
]
HERO_ALT = "Three golf clothing photos side by side: a model in Woodgrain's cream double pleated trousers, a model in Late Nine's burgundy cable knit polo, and a model in Odd Ritual's cream 1990s Heritage Polo"
FRN = json.loads((ROOT / "research/wanted-to-wear/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-WTW-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-10-12", "dateModified": "2026-10-12",
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
            f'  <div class="drop-tag grass">{len(ids)} picks</div>\n'
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
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Seventeen brands, one origin story</span><span class="dot"></span>
    <span>33 picks &middot; in stock, checked October 12, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="{HERO_ALT}" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
    body += faq_html()
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Kalamunda", "No Dirt", "Lehi", "Rookline", "Hudson", "LBB", "GolfPass", "Tarraing", "Hypebeast", "Old Ghosts"):
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
