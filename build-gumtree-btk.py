#!/usr/bin/env python3
"""build-gumtree-btk.py — Brand to Know: Gumtree Golf & Nature Club, 15 October 2026. Full treatment.
Lenny: "Let's do a brand to know post- Gumtree golf and Nature, one of my own personal favorites ... Full treatment for this one,
I want it really well done", then (on his own Made in Manhattan cover) "It's faded into a beautiful almost purple color. No loose
threads and I am not precious about my golf stuff, everything gets a little banged up.", then "add 35, 31, okay to show the sold out
stuff at the bottom and pull good quotes as well". The TGI Take opens in Lenny's first person with the pieces he owns.
FACTS (research/gumtree/sources.md): brand site about/press/sustainability/golf-headcovers/field-trips/studio pages; two founder
interviews (Sept 2025, Apr 2025), quoted verbatim, publications not named; Squarespace catalogue (prices + stock re-checked 15 Oct).
PHOTOS: Gumtree's own (research/gumtree/frame.py). Founder image is Gumtree's published portrait of Karsten (about page).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Brand to Know: Gumtree Golf & Nature Club, Brooklyn Headcovers Cut From Quilts, Tents and Waders"
DESC = ("Brand to Know: Gumtree Golf & Nature Club. A Melbourne surfer turned ad creative director sews golf headcovers in Brooklyn "
        "from 1940s quilts, camp tents and fly-fishing waders. His story, the materials, and 36 pieces, sold-out ones included.")
H1 = "Brand to Know: Gumtree Golf &amp; Nature Club &mdash; A Fresh-Air Perspective on Golf"
BC = "Gumtree Golf &amp; Nature Club"
SLUG = "brand-to-know-gumtree-golf-and-nature-club"
IMG = "/images/gumtree"
PK = json.loads((ROOT / "research/gumtree/picks.json").read_text())
SOLD = {d["key"] for d in PK if d["sec"] == "archive"}
NAME = {"westcoastsurftentheadc": "West Coast Surf Tent Headcover", "treefroggreencamptenth": "Tree Frog Green Camp Tent Headcover",
        "stateflowerheadcover20": "State Flower Headcover 2.0", "heirloomquiltputtercov": "Heirloom Quilt Putter Cover 2.0",
        "natureclubneoprenewets": "Nature Club Neoprene Wetsuit Headcover", "nywoolheadcovers": "New York Wool Headcovers",
        "americanwoolheadcover": "American Wool Headcovers, Fall", "studiocollectionheadco": "Studio Collection Headcover",
        "ggncxmalbonbirdsofgeor": "GGNC x Malbon Birds of Georgia Driver Cover", "tofightamockingbirdtee": "To Fight a Mockingbird Tee",
        "stateflowerreferencete": "State Flower Reference Tee", "anatomyofaflyreference": "Anatomy of a Fly Reference Tee",
        "natureclubbestbirdiest": "Nature Club Best Birdies Tee", "loseyourballfindyourse": "Lose Your Ball, Find Yourself Tee",
        "natureclubdeadstocklac": "Nature Club Deadstock Cotton Lace Shirt", "natureclubrockawaystri": "Nature Club Rockaway Stripe Shirt",
        "natureclubtheendlsline": "Nature Club The End Linen Shirt", "studiocollectionsspolo": "Studio Collection S/S Polo",
        "madeinmanhattanvest": "Made in Manhattan Vest", "natureclubvintagewashb": "Nature Club Vintage Wash Barrel Jeans",
        "natureclubbeachcombers": "Nature Club Beachcomber Short", "heirloomquiltvest44lwp": "Heirloom Quilt Vest 4.0",
        "texasstateflower5panel": "Texas State Flower 5-Panel", "newyorkbranchesunstruc": "New York Branches 5-Panel",
        "ggncxpumafieldnotespol": "GGNC x PUMA Field Notes Polo", "ggncxpumahelsinkig": "GGNC x PUMA Helsinki G",
        "ggncxmackenzienybagnav": "GGNC x Mackenzie NY Bag, Navy", "membercaddytowel": "Member Caddy Towel",
        "madeinmanhattanheadcov": "Made in Manhattan Headcover", "stateflorafaunaheadcov": "State Flora &amp; Fauna Headcover 2.0",
        "heirloomquiltcoveracmw": "Heirloom Quilt Headcover 3.0", "fishingwaderheadcover": "Vintage Fly Waders Headcover",
        "gumtreecoffeestudioesp": "GUMTREE (COFFEE) Sack Headcover", "nycsubwaytokenballmark": "NYC Vintage Subway Token Ball Marker Set",
        "vintagenewyorkstateout": "Vintage New York State Outdoor License Ball Markers", "natureclubfishspeciesh": "Freshwater Fish Pitch Repair Tools"}
def price(d):
    p, s = d["price"], d["sale"]
    f = lambda x: f"${x:,.0f}"
    if d["key"] in SOLD:
        return f"Sold out (was {f(p)})"
    return f"{f(s)} (reg. {f(p)})" if s else f(p)
COPY = {
 "tofightamockingbirdtee": "Mine is in the rotation. Gumtree made this one in a day, as a response to a much bigger brand stepping a little too close. The back tells the story of the northern mockingbird, which has no bright feathers to hide behind and survives on mimicry, faking a crowd of birds when it is alone. 6.5 oz American cotton, oversized and boxy, black or off-white.",
 "madeinmanhattanheadcov": "The cover on my driver. 16 oz canvas twill, sewn by hand in the garment district with the NY Branches logo on top and a navy fleece lining, in a run of 20 per size and color. Mine has faded to an almost purple. Sold out, but Gumtree keeps the listing up.",
 "westcoastsurftentheadc": "Cut from a 1970s blue and white waxed canvas camp tent found on California&rsquo;s central coast. Every cover comes from a different part of the tent, so some carry original stitching and more wear than others; Gumtree will try to match your preference if you ask. Driver or fairway.",
 "treefroggreencamptenth": "From a 1970s Coleman tent sourced in Vermont, in lime green waxed canvas with 50 years of patina. Same deal: no two alike, driver or fairway.",
 "stateflowerheadcover20": "A vintage patch hand-embroidered with a state flower, cut from heirloom textiles from across America (1940s to 1970s) and sewn onto 16 oz canvas in Manhattan. Driver only, and down to its last couple of states.",
 "heirloomquiltputtercov": "A blade putter cover from an olive and cream floral cotton quilt, circa 1950 to 1970, made in the garment district with a magnet closure. One of one.",
 "natureclubneoprenewets": "Made from scratch in New York City from herringbone wetsuit neoprene, the surf side of the brand turned into a driver or fairway cover.",
 "nywoolheadcovers": "100% American wool, knit by Fore Ewe in Oregon from yarn that is spun, double waxed and skein dyed. Driver, fairway or hybrid with the Gumtree NY logo, in navy or black.",
 "americanwoolheadcover": "I have the hybrid. 100% American wool knit by Fore Ewe in Oregon, in olive, dusty pink and cream, color matched to the fall Mackenzie x GGNC bag. Driver, fairway or hybrid; buy one or build a set.",
 "studiocollectionheadco": "The in-line canvas cover: 16 oz cotton twill sewn by hand in the garment district, with the GGNCofNY studio logo in oversized embroidery. Six-plus colors, driver or fairway.",
 "ggncxmalbonbirdsofgeor": "From the Malbon collaboration for the 2026 Masters: each cover carries a different hand-embroidered bird of Georgia on off-white canvas, made in Manhattan.",
 "stateflowerreferencete": "Every official American state flower listed on the back, in dusty brown on cream. It is the shirt Josh Allen was photographed wearing in July 2025.",
 "anatomyofaflyreference": "A dry fly with 14 labeled parts, from an illustration first published by E.C. Gregg in New York in 1940. The fly-fishing side of the Nature Club.",
 "natureclubbestbirdiest": "Gumtree printed &ldquo;The best Birdies aren&rsquo;t the ones on your scorecard&rdquo; across the back, on heavyweight 7.5 oz American cotton in olive.",
 "loseyourballfindyourse": "Gumtree made this tee for its Mental Health Awareness Club. A share of the proceeds goes to Project Healthy Minds in New York. Dusty pink or white.",
 "natureclubdeadstocklac": "Gumtree made 15 of these in New York from the last of a vintage cotton lace roll, with shell buttons.",
 "natureclubrockawaystri": "Lightweight cotton with a maroon stripe, shell buttons and Nature Club embroidery on the pocket, cut slightly cropped and made in Manhattan.",
 "natureclubtheendlsline": "Gumtree makes the same shirt in linen with a maroon check. It is made in Manhattan, slightly cropped, and the shirt for an Austin round in May.",
 "studiocollectionsspolo": "A boxy cotton polo with a two-button placket and dropped shoulders, with the GGNCofNY logo embroidered in Brooklyn. Made in the USA.",
 "madeinmanhattanvest": "Cut and sewn in Gumtree&rsquo;s Manhattan studio from 8.5 oz cotton twill, with a double zipper and the NY Branches logo on a pocket. 20 made per color.",
 "natureclubvintagewashb": "Loose barrel jeans made in Portugal from rigid denim, with Nature Club embroidery across the back pocket and a shorter 26.5&Prime; inseam.",
 "natureclubbeachcombers": "Made for the course, the beach or the water: 4-way stretch ripstop, sewn in New York, with a utility pocket and a big woven label.",
 "heirloomquiltvest44lwp": "One of six vests cut from a single cross-stitched quilt from the 1970s or 80s, finished with olive ribbing and a double zip in the Manhattan studio. One left.",
 "texasstateflower5panel": "The Texas bluebonnet, run-stitched on a navy 5-panel and embroidered in New York. The Austin pick.",
 "newyorkbranchesunstruc": "Gumtree puts the NY Branches logo on the front and &ldquo;The Gumtree Golf &amp; Nature Club of New York City&rdquo; on the side. The dad hat version is the one Nick Jonas wore.",
 "membercaddytowel": "Gumtree makes this ribbed cotton caddy towel with embroidered GGNC logos. Per the brand, it comes with &ldquo;one lucky bounce off of a tree and one rare bird sighting per round.&rdquo;",
 "ggncxpumafieldnotespol": "PUMA and Gumtree made this boxy cotton polo for their 2026 collaboration, striped in colors drawn from the Rocky Mountains, the North American puma&rsquo;s habitat. Rickie Fowler wore the collection.",
 "ggncxpumahelsinkig": "PUMA&rsquo;s vintage Helsinki brought back as a golf shoe in canvas, suede and nylon, &ldquo;equally for on the course, the trail or stroll through Brooklyn.&rdquo;",
 "ggncxmackenzienybagnav": "Mackenzie makes this bag to order by hand in navy waxed canvas and full-grain leather, with the NY Branches logo throughout. About eight weeks; monogramming available.",
 "stateflorafaunaheadcov": "A state flower and state bird on each cover, cut from a single 1970s or 80s heirloom textile. All gone.",
 "heirloomquiltcoveracmw": "Cut from one 1960s Americana quilt with hexagon flowers. Twenty-two covers, all sold.",
 "fishingwaderheadcover": "Driver covers from five pairs of 1980s to 2000s fly-fishing waders, straps, buckles and old repair patches included.",
 "gumtreecoffeestudioesp": "Cut from the jute sacks Gumtree&rsquo;s own coffee beans traveled to New York in before roasting.",
 "nycsubwaytokenballmark": "Real New York subway tokens as ball markers, from the first 1953-era designs through the pentagon-cut 1990s version.",
 "vintagenewyorkstateout": "Gumtree made ball markers from New York&rsquo;s metal hunting and fishing license pins of the late 1920s to the early 1940s: one color per year, serial numbers intact.",
 "natureclubfishspeciesh": "Greens &amp; Streams made these pitch repair tools by hand in the image of four fish, engraved with the GGNC mark.",
}
P = {d["key"]: ("Gumtree Golf &amp; Nature Club", NAME[d["key"]], price(d), d["url"], COPY[d["key"]]) for d in PK}
ORDER = {
 "mybag": ["madeinmanhattanheadcov", "americanwoolheadcover", "tofightamockingbirdtee"],
 "covers1": ["westcoastsurftentheadc", "treefroggreencamptenth", "stateflowerheadcover20", "heirloomquiltputtercov", "natureclubneoprenewets"],
 "covers2": ["nywoolheadcovers", "studiocollectionheadco", "ggncxmalbonbirdsofgeor"],
 "tees": ["stateflowerreferencete", "anatomyofaflyreference", "natureclubbestbirdiest", "loseyourballfindyourse"],
 "clothing": ["natureclubdeadstocklac", "natureclubrockawaystri", "natureclubtheendlsline", "studiocollectionsspolo", "madeinmanhattanvest", "natureclubvintagewashb", "natureclubbeachcombers", "heirloomquiltvest44lwp"],
 "hats": ["texasstateflower5panel", "newyorkbranchesunstruc", "membercaddytowel"],
 "collabs": ["ggncxpumafieldnotespol", "ggncxpumahelsinkig", "ggncxmackenzienybagnav"],
 "archive": ["stateflorafaunaheadcov", "heirloomquiltcoveracmw", "fishingwaderheadcover", "gumtreecoffeestudioesp", "nycsubwaytokenballmark", "vintagenewyorkstateout", "natureclubfishspeciesh"],
}
SEC = [
 ("mybag", "From My Bag", "<strong>Three pieces</strong>The covers and the tee I actually own. The knit cover and the tee are in stock; the Made in Manhattan cover sold out a while ago, so its card links to Gumtree&rsquo;s page for the next run."),
 ("covers1", "One of One: Covers Cut From Old Textiles", "<strong>Five covers</strong>These covers are the heart of the brand. Each is cut from a different part of a found textile, so the one you get will not match the photo exactly, and when the textile runs out, the design is retired."),
 ("covers2", "The In-Line Covers", "<strong>Three more covers</strong>Gumtree&rsquo;s repeatable covers, still made in small runs: wool knit in Oregon and canvas sewn in Manhattan."),
 ("tees", "Reference Tees", "<strong>Four tees</strong>Gumtree prints field-guide graphics on heavy American cotton, from state flowers to a 1940 fly diagram."),
 ("clothing", "Nature Club and Made in Manhattan", "<strong>Eight pieces</strong>The clothes side, most of it cut and sewn in Manhattan: lace, stripe and linen shirts, a canvas vest, barrel jeans from Portugal and ripstop shorts."),
 ("hats", "Hats and the Caddy Towel", "<strong>Three picks</strong>A Texas bluebonnet hat for us, the New York hat that started showing up on famous heads, and the towel."),
 ("collabs", "The Collabs", "<strong>Three picks</strong>Gumtree has partnered with PUMA, Malbon, Mackenzie, Almond Surfboards, Nocs and Huckberry, all brands that fit its outdoors theme. These three are in stock now."),
 ("archive", "From the Archive: Sold Out", "<strong>Seven pieces</strong>Gone, but they show what Gumtree does best. One-of-one runs like these sell out fast; get on their mailing list for the next one."),
]
SECTIONS = [(h2, a, ORDER[a], k) for a, h2, k in SEC]
N = sum(len(v) for v in ORDER.values())
DATE = "2026-10-15"
PQ = {
 "slow": ("I like to describe Gumtree to people as almost a slow-fashion golf brand.", "Karsten Jurkschat, founder, 2025"),
 "covers1": ("It&rsquo;s not for everybody. And that&rsquo;s the point, and that&rsquo;s fine.", "Karsten Jurkschat, founder, 2025"),
 "covers2": ("I think there&rsquo;s a luxury in the restraint, knowing that you have a piece that&rsquo;s special.", "Karsten Jurkschat, founder, 2025"),
 "clothing": ("The best Birdies aren&rsquo;t the ones on your scorecard.", "Gumtree Golf &amp; Nature Club, on the Best Birdies tee"),
 "archive": ("We make something, we promote it, it sells out, we use that money to make the next thing and we just keep it feeling tight and special.", "Karsten Jurkschat, founder, 2025"),
}
BANDS = {
 "studio": ("My Visit to Greenpoint &middot; photos by TGI",
  "I stopped by the studio at 55 Nassau Avenue during open hours on <a href=\"/drops/new-york-golf-trip-sedgewood-union-vale-bethpage-black\" style=\"border-bottom:1px solid currentColor\">my week of New York golf</a>, between rounds at Union Vale and Bethpage. It is a showroom and a working studio in one room: the rail is a tree branch, the caps sit on a low table between two leather sofas, and there are surfboards against the wall. Open select Saturdays, weekdays by appointment.",
  [("lenny-studio", "The Gumtree studio in Greenpoint, Brooklyn: leather sofas, a rug, caps laid out on a low table and rails of clothing under tall windows", "The studio, from my visit"),
   ("lenny-rail", "A tree branch used as a clothing rail at Gumtree, hung with striped knits and denim, caps and sneakers below, surfboards against the wall", "The branch rail, from my visit"),
   ("life-2", "Gumtree&rsquo;s striped wool headcovers hanging on a wire newspaper rack", "The wool covers (Gumtree photo)")]),
 "made": ("What It&rsquo;s Made From &middot; Gumtree&rsquo;s own photos",
  "Quilt scraps, tent canvas and old waders before and after: the textiles are the design.",
  [("life-7", "A pile of Gumtree headcovers cut from blue and indigo patchwork quilt fabric", "Patchwork quilt covers"),
   ("life-8", "A Gumtree golf bag and headcovers propped against a tree trunk", "In the wild"),
   ("life-9", "A gray headcover cut from vintage fly-fishing waders among wildflowers", "A wader cover in the wildflowers")]),
 "nature": ("The Nature Club &middot; Gumtree&rsquo;s own photos",
  "The surf side of the brand: the Nature Club shirts and hats are shot on the beach, not the course.",
  [("life-4", "A man in a lace short-sleeve shirt and jeans checking a golf bag on a beach", "The lace shirt on the beach"),
   ("life-5", "A man in a fuzzy sweater adjusting a black Nature Club cap", "Nature Club cap"),
   ("life-6", "A man in a pink check linen shirt standing on a cliff above the ocean with a lighthouse behind", "The End linen shirt")]),
 "walks": ("Just Out for a Walk &middot; Gumtree&rsquo;s own photos",
  "Gumtree&rsquo;s Field Trips are three-day golf trips for about 40 people, built around hikes, bird walks and stargazing as much as rounds (Sonoran Desert, Zion, the Catskills). These photos are from its Just Out for a Walk event in England.",
  [("life-10", "A sandy path winding between grassy dunes toward a green on an English hilltop course", "Cleeve Hill, England"),
   ("life-11", "Sheep grazing on a hilltop golf course in England with a valley below", "Sheep on the course"),
   ("life-12", "An aerial view of a clubhouse surrounded by fields and woods in the English countryside", "The clubhouse from above")]),
 "collab": ("The Collabs &middot; Gumtree&rsquo;s own photos",
  "Gumtree makes its collaboration photos the way it makes everything else: outside, with the birds.",
  [("life-13", "A man in the GGNC x PUMA striped polo standing in front of a waterfall", "GGNC x PUMA Field Notes polo"),
   ("life-14", "A foot in a Nature Club sock and the GGNC x PUMA Helsinki G shoe in the grass", "GGNC x PUMA Helsinki G"),
   ("life-15", "A yellow canary perched on a headcover embroidered with a northern cardinal", "GGNC x Malbon, Birds of Georgia")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Gumtree Golf &amp; Nature Club is one of my personal favorites, and I can show you why. My driver wears a Gumtree Made in Manhattan cover, and after a few seasons it has faded into a beautiful, almost purple color. No loose threads. I am not precious about my golf stuff and everything I own gets a little banged up, but this one just looks better for it. My Fall knit hybrid cover is from Gumtree too, and the To Fight a Mockingbird tee is in the rotation.</p>
    <p>What I like most is how quick this brand is on its feet. The Mockingbird tee is the best example: Gumtree made it in a day, as a response to a much larger brand stepping a little too close. A big company plans a year out; a one-founder studio in Brooklyn can answer by the weekend, and do it with a joke about a bird that survives by imitation.</p>
    <p>That is the whole idea of the brand. Gumtree makes things slowly and in small runs, a lot of them from textiles that already had a life: 1940s quilts, 1970s camp tents, fly-fishing waders, the jute sacks its own coffee beans arrive in. Each headcover is cut from a different part of the source, so no two match, and when the fabric runs out, that design is gone. The repeatable pieces stay close to home too, with wool covers knit in Oregon and canvas sewn in Manhattan&rsquo;s garment district, and 2% of every sale goes to carbon removal. You end up with the cover people ask about on the first tee, and one that wears in instead of wearing out.</p>
    <h2 class="products-hdr btk-story-hdr">From Melbourne to Greenpoint</h2>
    <p>Karsten Jurkschat grew up surfing in Melbourne and started out as a photographer in the surf industry. He went on to become one of advertising&rsquo;s best-known creative directors, leading work for the New York Knicks, the NBA and Apple Music, and was named one of the industry&rsquo;s Creative Directors of the Year in 2020. He moved to New York in 2017, missed the ocean, and burned out.</p>
    <p>Golf is what brought him back outside. During the pandemic he started walking the city&rsquo;s courses at dawn, before anyone else was up. The rest of his life was already set up for what came next: his father was a landscape gardener, and his German grandmother had taught him to sew. He started Gumtree in his spare time, bought a $300 sewing machine, and made every product himself for the first six months. The brand launched in Brooklyn in 2022. It is still self-funded, and Karsten still designs every collection and shoots its photography.</p>
    <p>Since then the covers have sold out in minutes (a run cut from a 1970s Vermont tent went in 11), Josh Allen has worn the State Flower tee, Nick Jonas the New York dad hat, and Rickie Fowler the PUMA collaboration. For the 2025 Ryder Cup at Bethpage, Gumtree cut ten covers from a 1940s red, white and blue quilt and priced them by the result: 10% off for every stroke Team USA won by.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>2022, Brooklyn</span></div>
      <div class="sidebar-detail"><span class="l">Founder</span><span>Karsten Jurkschat</span></div>
      <div class="sidebar-detail"><span class="l">Studio</span><span>55 Nassau Ave, Greenpoint</span></div>
      <div class="sidebar-detail"><span class="l">Known for</span><span>One-of-one headcovers</span></div>
      <div class="sidebar-detail"><span class="l">Gives back</span><span>2% to carbon removal</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$40&ndash;$850</span></div>
      <div class="sidebar-detail"><span class="l">In my bag</span><span>2 covers + the Mockingbird tee</span></div>
      <a href="https://www.gumtreegolfandnature.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit Gumtree &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#GumtreeGolf</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#NatureClub</span>
        <span class="hashtag">#Upcycled</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FOUNDER = f"""
<section class="products" style="border-top:none;padding-top:48px">
  <h2 class="products-hdr" id="in-his-words">In His Words &mdash; Karsten Jurkschat</h2>
  <p class="cat-kicker"><strong>Founder&rsquo;s voice</strong>Quotes below are verbatim from Gumtree&rsquo;s own site and two published interviews with Karsten, from April and September 2025.</p>
  <div class="bk-founder" style="display:grid;grid-template-columns:340px 1fr;gap:40px;align-items:start;max-width:1100px">
    <div style="border:.5px solid var(--ink);overflow:hidden">
      <img src="{IMG}/founder.jpg" alt="Karsten Jurkschat, founder of Gumtree Golf &amp; Nature Club, seated in his studio holding a golf bag full of flowers" loading="lazy" style="width:100%;aspect-ratio:4/5;object-fit:cover;display:block" />
    </div>
    <div style="font-size:16px;line-height:1.7">
      <p>On why he started it, from the brand&rsquo;s About page: &ldquo;When I moved from Melbourne to New York City in 2017, I quickly became addicted to the city. But what I loved about the city, the pace, the chaos, was also what I sought to escape.&rdquo; And on what golf gave him: &ldquo;Even in a city like New York, a golf course at sunrise offers complete immersion in nature.&rdquo;</p>
      <p style="margin-top:16px">He describes the early mornings plainly: &ldquo;I found that getting up at 6 a.m. or 5 a.m. and going to one of the courses in the city and just walking around before everybody&rsquo;s up and playing a round of golf gave me that same disconnect and kind of mental health break that I was kind of looking for.&rdquo; Coming from surfing, the gap in the market surprised him: &ldquo;When I got into golf, I was so surprised there weren&rsquo;t that many brands that were connecting those dots.&rdquo;</p>
      <p style="margin-top:16px">On sewing the first pieces himself: &ldquo;When I started the brand, I thought, &lsquo;You know what, if I really want this to be truly sustainable and the pipeline to be really short, I&rsquo;m gonna try to make them.&rsquo;&rdquo; It still runs short. &ldquo;I source everything myself, the fabric, and do all the design work myself in the studio &mdash; then I take it to the small workshop we use in Manhattan and the guys put it together from there.&rdquo;</p>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:28px;padding-top:24px;border-top:.5px solid rgba(20,20,20,.15)">
        <div>
          <div style="font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;opacity:.55;margin-bottom:6px">The Roots</div>
          <div style="font-size:14px;line-height:1.6;opacity:.85">&ldquo;That&rsquo;s where I learned all my plant knowledge.&rdquo; (On his father, a landscape gardener.)</div>
        </div>
        <div>
          <div style="font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;opacity:.55;margin-bottom:6px">The Start</div>
          <div style="font-size:14px;line-height:1.6;opacity:.85">&ldquo;I didn&rsquo;t really expect it to go anywhere.&rdquo;</div>
        </div>
        <div>
          <div style="font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;opacity:.55;margin-bottom:6px">The 2%</div>
          <div style="font-size:14px;line-height:1.6;opacity:.85">&ldquo;I&rsquo;d sometimes love to have that extra 2%, because we&rsquo;re self-funded and don&rsquo;t have investors.&rdquo;</div>
        </div>
      </div>
    </div>
  </div>
</section>
"""
SPEC = [("Heirloom quilts", "American quilts from the 1940s to the 1980s: pinwheels, nine-patches, calico and appliqu&eacute; florals"),
        ("Camp tents", "Waxed canvas tents from the 1950s to the 1980s, grommets, camp rope and repair patches kept"),
        ("Fly-fishing waders", "Retired waders cut into waterproof driver covers, straps and old patches included"),
        ("Coffee sacks", "The jute sacks GUMTREE (COFFEE) beans arrive in, plus burlap feed sacks from working farms"),
        ("American wool", "Knit in Oregon by Fore Ewe from yarn that is spun, double waxed and skein dyed"),
        ("16 oz canvas", "The Studio and Made in Manhattan covers, sewn in Manhattan&rsquo;s garment district")]
def explainer():
    cells = "".join(f'<div style="padding:18px 16px;border:.5px solid rgba(20,20,20,.2)"><div style="font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--grass);margin-bottom:6px">{a}</div><div style="font-size:15px;line-height:1.5">{b}</div></div>' for a, b in SPEC)
    return f"""
<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr" id="what-its-made-from">What It&rsquo;s Made From</h2>
  <p class="cat-kicker"><strong>The materials</strong>Gumtree sources a textile, plans the cuts so each cover shows a different part of it, and has it sewn in New York with a soft lining and an elastic or magnetic closure. Driver covers fit any driver up to 460cc. Vintage pieces are sold as is: spot clean with cold water and let them air dry.</p>
  <div class="mg-spec" style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;max-width:980px;margin:0 auto">{cells}</div>
</section>
"""
FAQ = [
 ("Who founded Gumtree Golf & Nature Club?", "Karsten Jurkschat, an Australian-born photographer and former advertising creative director who grew up surfing in Melbourne and moved to New York in 2017. He started Gumtree in his spare time during the pandemic and launched it in Brooklyn in 2022."),
 ("Where is Gumtree Golf & Nature Club based?", "Brooklyn, New York. The studio and showroom is at 55 Nassau Avenue in Greenpoint, open on select Saturdays and by appointment during the week."),
 ("What are Gumtree headcovers made from?", "The one-of-a-kind covers are cut from vintage textiles: heirloom quilts from the 1940s to 1980s, waxed canvas camp tents, fly-fishing waders and coffee sacks. The in-line covers are American wool knit in Oregon or 16 oz canvas sewn in Manhattan's garment district."),
 ("How much do Gumtree headcovers cost?", "On October 15, 2026, wool covers were $85, canvas and vintage-textile covers $120 to $185, with some on sale."),
 ("Will my Gumtree headcover look like the photo?", "Not exactly, for the one-of-a-kind covers. Each is cut from a different part of the source textile, so the pattern, fade and stitching change from cover to cover, and they can show wear from their previous life."),
 ("Does Gumtree give back?", "Yes. Gumtree contributes 2% of every purchase to permanent carbon removal through Stripe Climate."),
 ("What are Gumtree Field Trips?", "Three-day golf and nature trips for about 40 people, mixing rounds at local courses with hikes, bird walks and stargazing. Past trips went to the Sonoran Desert, St. George and Zion, and the Catskills."),
]
FRN = json.loads((ROOT / "research/gumtree/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-GT-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}'
            '.bk-founder{max-width:1100px}@media(max-width:820px){.bk-founder{grid-template-columns:1fr!important}}'
            '.ig-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:0 0 34px}.ig-grid figure{margin:0}.ig-grid img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block;background:#eceae5}.ig-cap{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink);opacity:.5;margin-top:8px;line-height:1.5}@media(max-width:720px){.ig-grid{grid-template-columns:repeat(2,1fr);gap:10px}}@media(max-width:720px){.mg-spec{grid-template-columns:repeat(2,1fr)!important}}</style>\n')


def card(k, idx):
    brand, item, price, handle, copy = P[k]
    url = handle
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
            f'<a href="{url}" target="_blank" rel="noopener" class="product-link">{"View on Gumtree" if k in SOLD else "Shop"} &#8599;</a></div></div>')


def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>'
                     for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')




def head_top():
    og = f"https://thegrassyissue.com{IMG}/btk-og.jpg"
    items, pos = [], 1
    for sec in SECTIONS:
        for h in sec[2]:
            items.append({"@type": "ListItem", "position": pos, "url": P[h][3], "name": H.unescape(f"{P[h][0]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": DATE, "dateModified": DATE,
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
<link rel="preload" as="image" href="{IMG}/btk-hero.jpg" />
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
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>October 15, 2026</span><span class="dot"></span>
    <span>Brooklyn &middot; est. 2022</span><span class="dot"></span>
    <span>36 pieces &middot; prices checked October 15, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/btk-hero.jpg" alt="Two men in Gumtree Nature Club clothes by a black Porsche with surfboards at a beach parking lot, the ocean behind them" fetchpriority="high" /></div></div>
"""
    body += TAKE
    body += band("studio")
    body += pq("slow")
    body += FOUNDER
    body += explainer()
    body += band("made")
    n = 1
    for s, b in zip(SECTIONS, [None, None, None, "nature", None, "walks", "collab", None]):
        if b: body += band(b)
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
    for leak in ("Mackem", "Kalamunda", "Howie", "No Dirt", "Lehi", "Rookline", "Hudson", "LBB", "GolfPass", "Woodgrain", "Parmore", "Lazyface", "Mount Tee", "Sunday Golf", "Loma", "Matchstick", "Good Morning America", "Forbes", "Esquire", "Hypebeast", "Golf Digest", "Skratch", "Ad Age"):
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
