#!/usr/bin/env python3
"""build-sunday-golf-btk.py — Brand to Know: Sunday Golf, 15 October 2026.
Lenny: "we need to do a post about sunday golf", then "do a nicer deep dive, really cover all our bases. full brand to know treatment".
FACTS (all checked Oct 15 2026):
- sundaygolf.com products.json: 24 in-stock picks, sale prices with compare-at (site-wide markdown on the day).
- sundaygolf.com/pages/compare-golf-bags: heights, weights, club counts, strap types and "Frosty Pocket" can counts.
- sundaygolf.com/pages/faqs: founded August 2020 (sixth anniversary this year), San Diego office, no storefront, "most major golf
  retailers and over 1,000 pro shops", 600D nylon / PU (vegan) leather S-Class / recycled nylon ripstop Ranger, full-length dividers
  on every bag, lifetime product warranty, embroidery on the removable ball pocket (5-10 business days), oversized grips advice.
- sundaygolf.com/pages/about: "Enjoy more." brand promise and manifesto lines quoted verbatim.
- Founder quotes verbatim from two published interviews with Ronan Galvin (Sept 2022, Aug 2023); publications not named on page per
  house rule. Facts from them: co-founders Ronan Galvin and Casey Mathews; Galvin's bag product-development background; the Loma Club
  par 3 origin; one bag from a storage unit; 100,000+ bags sold in its first three years; crowdfunded seed round.
PHOTOS: brand's own (research/sunday-golf/frame.py; life-sources.json). Founder block uses a campaign frame, not a portrait of Galvin
(no brand-published portrait); alt text says what it is.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Brand to Know: Sunday Golf, the San Diego Brand That Made the Par 3 Bag a Category"
DESC = ("Brand to Know: Sunday Golf. How a par 3 course in San Diego turned into the Loma bag, 100,000-plus bags and 1,000-plus pro shops, "
        "plus a size guide and 24 picks from the Loma to the Big Rig.")
H1 = "Brand to Know: Sunday Golf &mdash; Carry Less, Enjoy More"
BC = "Sunday Golf"
SLUG = "brand-to-know-sunday-golf"
IMG = "/images/sunday-golf"
SHOP = "https://sundaygolf.com/products/"
O = json.loads((ROOT / "research/sunday-golf/options.json").read_text())
def pr(d):
    p = float(d["price"]); c = float(d["cmp"] or 0)
    s = f"${p:,.0f}" if p.is_integer() else f"${p:,.2f}"
    return s + (f" (reg. ${c:,.0f})" if c > p else "")
COPY = {
 "thelomaevergreenpar3ba": "The one that started it. Ronan Galvin built the first Loma for the par 3 at the Loma Club in San Diego: 32 inches tall, 1.95 pounds, room for six clubs, a single strap and a pocket for one cold can. It is still the bag to grab for a par 3, a range session or a twilight nine with a wedge, a putter and a few irons. 11 colorways in stock; Evergreen shown.",
 "lomaxlmidnightgreencar": "The Loma grown up for a half set: up to eight clubs at 3.4 pounds and 33 inches, with a double strap and a two-can Frosty pocket. Built for walking nine or a light eighteen. Six colorways.",
 "elcaminoblackyellowmid": "A mid-size stand bag for up to 12 clubs at 3.9 pounds, 34 inches tall, with a double strap and a four-can Frosty pocket. Sunday Golf pitches this colorway at fans of &ldquo;some of the most iconic sports colors around.&rdquo; Nine colorways, new ones added in August.",
 "ryderevergreenfullsize": "Their full-size stand bag: 14 clubs, 4.9 pounds, 35 inches, double strap, four-can Frosty pocket, and still lighter than most full bags. The most colorways of anything they make, 15 in stock; Evergreen shown.",
 "ryder14midnightgreenfu": "Sunday Golf made this Ryder with a 14-way top, one slot per club. Sunday Golf says it fits grips up to 1.25 inches in each slot, so this is the Ryder for players with midsize grips. Midnight Green or black.",
 "stormryderwaterproofst": "The Ryder made tougher, with welded waterproof pockets &ldquo;so your gear stays safe and dry, rain or shine.&rdquo; Black only.",
 "rangersagepremiumstand": "The top of the line and the one bag in the range made from recycled nylon ripstop. 14 clubs, 5.5 pounds, 35 inches, a three-can Frosty pocket. Sage, iron or black.",
 "thebigrigevergreencart": "Sunday Golf made the Big Rig for carts and push carts: 36 inches, 7 pounds, room for 14 clubs and seven cans. Sunday Golf says its tubes fit grips up to 1.5 inches, the most room in the line. 12 colorways.",
 "rydersclasscreamleathe": "Sunday Golf cut this Ryder in polyurethane, or vegan, leather instead of the standard 600D nylon. Five colors; cream shown.",
 "checkerfamilygolfbagse": "A matching black and white checkerboard set, added in May, for a parent and kid who want to show up as a team.",
 "ryderduckcamofullsizes": "The newest bag in the shop, added October 7: the full-size Ryder in a duck camo print, right on time for hunting season.",
 "ryderbobmarleyolivehem": "From the Bob Marley collaboration, the Ryder in olive with hemp-look panels. The same collab comes as a camo Ryder, a rasta Loma and two Big Rigs.",
 "lomamossyoak": "The original Loma in Mossy Oak&rsquo;s Bottomland camo, from Sunday Golf&rsquo;s Mossy Oak collaboration, which also covers the Big Rig and the Big Frosty cooler.",
 "sundaygolfropehatusa25": "A blue rope hat with a USA 250 logo for America&rsquo;s 250th, part of a run of rope hats that also comes in pink and black-and-white.",
 "chestpacktan": "The Chesty is a chest-pack vest you strap over a shirt for your phone, keys and a scorecard on the days you aren&rsquo;t carrying a bag at all. Tan or black.",
 "magneticgolftowelmidni": "Sunday Golf made this towel with a magnet so it sticks to the cart or a clubhead. Added in July in Midnight Green, black and toasted almond.",
 "bigfrostygolfbagcooler": "A slim, water-resistant cooler that rides in the bag and holds up to six cans or four pint cans. Five colors, Mossy Oak camo included.",
 "nickelbagtoastedalmond": "A weather-resistant valuables pouch with waterproof zippers, made to match the bags in the same colors.",
 "caddypenholder": "A miniature tour-style staff bag that holds pens on a desk. New in September and the most Sunday Golf thing in the store.",
 "mickeybeaniebrowngrayc": "A brown and gray checkerboard beanie for the one cold morning Austin gets in November.",
 "bladeputterheadcovermi": "A blade putter cover in durable vegan leather with an elastic fit. Four colors to match the bags.",
 "par3bamboogolftees80ct": "Short bamboo tees, 1&frac12; inches, made for the par 3 course. 80 to a bag.",
 "lomagolfbagwallhookbla": "A wall hook built for the Loma and Loma XL, which is how Sunday Golf suggests storing them: off the floor, legs secured.",
 "coastergolftravelbag": "A rolling travel bag for the whole set, built to keep your clubs safe from &ldquo;baggage claim beatdowns.&rdquo;",
}
P = {d["key"]: ("Sunday Golf", d["name"], pr(d), d["url"], COPY[d["key"]]) for g, d in O}
SEC = {"The Bags": ("The Bags, Smallest to Biggest", "bags", "<strong>Ten bags</strong>Every Sunday Golf bag starts from the Loma&rsquo;s idea: as light as it can be, with full-length dividers and a pocket for a cold one. Smallest to biggest."),
       "Collabs &amp; Camo": ("Collabs &amp; Camo", "collabs", "<strong>Four picks</strong>Sunday Golf made its collabs with Mossy Oak and Bob Marley rather than tour pros, then added duck camo and a hat for America&rsquo;s 250th."),
       "Around the Bag": ("Around the Bag", "around", "<strong>Ten picks</strong>Everything that clips to, rides in or hangs next to the bag, plus a desk toy.")}
SECTIONS = []
for g in ["The Bags", "Collabs &amp; Camo", "Around the Bag"]:
    h2, a, k = SEC[g]
    SECTIONS.append((h2, a, [d["key"] for gg, d in O if gg == g], k))
N = 24
DATE = "2026-10-15"
PQ = {
 "bags": ("I saw player after player lug around their full set when you really only use four or five clubs to play the course.", "Ronan Galvin, co-founder, 2022"),
 "collabs": ("It&rsquo;s quitting golf forever and then showing up again the next day.", "Sunday Golf, from the brand manifesto"),
}
BANDS = {
 "course": ("On the Course &middot; Sunday Golf&rsquo;s own photos",
  "Sunday Golf shoots its bags the way most people actually play: a fourball in a cart, push carts on the fairway, a fist bump across the path, a carry bag over one shoulder on a desert course.",
  [("life-1", "Three golfers on a sunny fairway with two Sunday Golf bags on push carts, one golfer finishing his swing", "Push carts and a full swing"),
   ("life-2", "Two golfers bumping fists between a golf cart and a Sunday Golf stand bag", "The fist bump across the cart path"),
   ("life-3", "A golfer carrying a camo Sunday Golf stand bag over his shoulder with a towel clipped on", "Mossy Oak camo, on the shoulder"),
   ("life-4", "A golfer walking a desert fairway beneath red rock cliffs with a Sunday Golf stand bag behind him", "Red rock and a stand bag"),
   ("life-5", "A golfer in shorts chipping from a grassy slope among palm trees", "A short game afternoon"),
   ("life-6", "A man carrying a black Sunday Golf stand bag on a double strap in front of a rusted wall", "Double strap, black Ryder")]),
 "frosty": ("The Frosty Pocket &middot; Sunday Golf&rsquo;s own photos",
  "Every Sunday Golf bag has an insulated pocket for cold drinks. The brand calls it the Frosty pocket and lists it on the spec sheet next to height and weight: one can on the Loma, seven on the Big Rig.",
  [("life-9", "Two cans in the insulated Frosty pocket of a camo Sunday Golf bag with yellow trim", "Bob Marley camo Ryder, Frosty pocket"),
   ("life-11", "Two cans in the insulated pocket of a burnt orange and white Sunday Golf bag", "Burnt orange Ryder, two cans in"),
   ("life-12", "Cans in the open Frosty pocket of a Mossy Oak Bottomland camo Sunday Golf bag", "Mossy Oak Bottomland")]),
 "details": ("The Details &middot; Sunday Golf&rsquo;s own photos",
  "Up close: a white vegan leather S-Class bag, the mini staff-bag pen holder that doubles as a drink holder in Sunday Golf&rsquo;s own photos, and one of the crew showing it off.",
  [("life-7", "Irons in a cream vegan leather Sunday Golf S-Class bag", "S-Class vegan leather"),
   ("life-10", "A beer bottle in Sunday Golf&rsquo;s mini staff-bag holder next to a hole on putting turf", "The Caddy Pen Holder, off duty"),
   ("life-8", "A smiling man in a Sunday Golf cap holding the mini staff-bag pen holder full of tiny clubs", "The Caddy Pen Holder")]),
 "around": ("The Clubhouse &middot; Sunday Golf&rsquo;s own photos",
  "Sunday Golf&rsquo;s marketing doesn&rsquo;t take itself seriously: an office dog named Mindy, a stars-and-stripes bag for America&rsquo;s 250th, and plenty of pointing.",
  [("life-13", "A shaggy dog named Mindy sitting next to a white and yellow Sunday Golf stand bag", "Mindy, with a stand bag"),
   ("life-14", "A white Sunday Golf stand bag with USA graphics in front of an American flag", "America&rsquo;s 250th bag"),
   ("life-16", "A man with a mustache in a navy Sunday Golf quarter-zip pointing at the logo", "Pointing at the logo")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Sunday Golf made the par 3 bag a category. Before the Loma, a short-course round meant hauling your full bag or carrying a few clubs in your hand. Now there is a two-pound sling with a slot for six clubs and a pocket for one cold can, and every golf retailer sells something like it. The San Diego brand that started it has sold more than 300,000 bags since 2020, and it has grown into full-size stand bags, cart bags, a vegan leather line and collaborations with Mossy Oak and Bob Marley.</p>
    <p>For Austin, the Loma is the right bag for how a lot of us actually play: a twilight nine at <a href="/guides/hancock-1">Hancock</a>, a wedge-and-putter hour at the range, a par 3 on a weeknight with five clubs. Walk nine holes in August with a full staff bag and you&rsquo;ll get it. The bigger bags are good, fairly priced and light, but the Loma is the reason to know this brand.</p>
    <h2 class="products-hdr btk-story-hdr">A Par 3 in San Diego</h2>
    <p>Ronan Galvin was not a golfer growing up. Born in Ireland and raised in North County San Diego, he spent about a decade on the other side of the industry, working in golf bag product development and brokering between bag brands and factories overseas. Back in San Diego, friends took him to the Loma Club, a nine-hole par 3 at Liberty Station, and the game finally made sense to him. What he noticed was everyone else&rsquo;s bag: full sets, carried around a course that only asks for a handful of clubs.</p>
    <p>He built a prototype for that course and took it out. People asked where they could buy one. He started Sunday Golf with his business partner Casey Mathews, with Galen Brunelle also part of the founding team, and named the first bag after the course. The plan was to launch in January 2020. The pandemic stalled the shipments, and by the time the first inventory arrived that August, golf was one of the few things people could still do with friends. The first bags shipped from a storage unit around the corner from the office, and they couldn&rsquo;t keep them in stock.</p>
    <p>The rest grew from there: more than 100,000 bags in the first three years, a crowdfunded seed round from more than 550 small investors in 2023, and, by mid-2026, more than 300,000 bags sold. Sunday Golf says it&rsquo;s now in most major golf retailers and more than 1,000 pro shops. The mission written on its office wall is to &ldquo;Get 500,000 golfers having more fun by 2027,&rdquo; measured in bags.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>August 2020, San Diego</span></div>
      <div class="sidebar-detail"><span class="l">Founders</span><span>Ronan Galvin &amp; Casey Mathews</span></div>
      <div class="sidebar-detail"><span class="l">Known for</span><span>The Loma par 3 bag</span></div>
      <div class="sidebar-detail"><span class="l">Bags sold</span><span>300,000+</span></div>
      <div class="sidebar-detail"><span class="l">Warranty</span><span>Lifetime</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$15&ndash;$400</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>The Loma, Evergreen</span></div>
      <a href="https://sundaygolf.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit Sunday Golf &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#SundayGolf</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#Par3</span>
        <span class="hashtag">#EnjoyMore</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FOUNDER = f"""
<section class="products" style="border-top:none;padding-top:48px">
  <h2 class="products-hdr" id="in-his-words">In His Words &mdash; Ronan Galvin</h2>
  <p class="cat-kicker"><strong>Founder&rsquo;s voice</strong>Quotes below are verbatim from three published interviews with Galvin, from 2022, 2023 and June 2026.</p>
  <div class="bk-founder" style="display:grid;grid-template-columns:340px 1fr;gap:40px;align-items:start;max-width:1100px">
    <div style="border:.5px solid var(--ink);overflow:hidden">
      <img src="{IMG}/life-15.jpg" alt="Four people from the Sunday Golf crew posing with their stand bags in a studio shoot" loading="lazy" style="width:100%;aspect-ratio:4/5;object-fit:cover;display:block" />
    </div>
    <div style="font-size:16px;line-height:1.7">
      <p>Galvin tells the origin story the same way every time: the par 3 came first, and the bag came out of it. &ldquo;I got dragged to a par-3 course in 2019 &mdash;The Loma Club&mdash;and it was way more my jam,&rdquo; he said this summer. &ldquo;It was a lot different than the stereotypical ideas you have about golf where it&rsquo;s kind of long, uptight, and exclusive.&rdquo;</p>
      <p style="margin-top:16px">The brand&rsquo;s position against the big golf companies is just as simple. &ldquo;We say we like to be more relatable than aspirational,&rdquo; he said in 2022. Sunday Golf doesn&rsquo;t sponsor tour players or promise a lower score. Galvin jokingly calls what it sells &ldquo;diet golf&rdquo; or &ldquo;golf light&rdquo;: weekend rounds, range sessions, company scrambles.</p>
      <p style="margin-top:16px">On the timing, he is honest about the luck. &ldquo;We launched the company right when the pandemic hit and we couldn&rsquo;t keep our products in stock. At first it was a bit scary but the lockdown created a huge resurgence in golf. We&rsquo;ve been riding the wave ever since,&rdquo; he said in 2023. And on the product: &ldquo;We&rsquo;re trying to make a good bag, at a good price, that you can enjoy playing with, and obviously people have resonated with that.&rdquo;</p>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:28px;padding-top:24px;border-top:.5px solid rgba(20,20,20,.15)">
        <div>
          <div style="font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;opacity:.55;margin-bottom:6px">The Point</div>
          <div style="font-size:14px;line-height:1.6;opacity:.85">&ldquo;A golf bag is a golf bag, but our products are vehicles to help support that.&rdquo;</div>
        </div>
        <div>
          <div style="font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;opacity:.55;margin-bottom:6px">The Why</div>
          <div style="font-size:14px;line-height:1.6;opacity:.85">&ldquo;To remind the world that life is meant to be enjoyed.&rdquo;</div>
        </div>
        <div>
          <div style="font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;opacity:.55;margin-bottom:6px">The Place</div>
          <div style="font-size:14px;line-height:1.6;opacity:.85">&ldquo;The laid-back lifestyle of San Diego kind of seeps into everyone&rsquo;s veins.&rdquo;</div>
        </div>
      </div>
    </div>
  </div>
</section>
"""
SPECS = [("Loma", "Par 3", '32"', "1.95 lb", "6", "1 can", "Single"),
         ("Loma XL", "Par 3", '33"', "3.4 lb", "8", "2 cans", "Double"),
         ("El Camino", "Mid-size stand", '34"', "3.9 lb", "Up to 12", "4 cans", "Double"),
         ("Ryder", "Full-size stand", '35"', "4.9 lb", "14", "4 cans", "Double"),
         ("Ranger", "Premium stand", '35"', "5.5 lb", "14", "3 cans", "Double"),
         ("Big Rig", "Cart", '36"', "7 lb", "14", "7 cans", "Single")]
def size_guide():
    th = "".join(f'<th style="text-align:left;padding:10px 12px;font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;border-bottom:1px solid var(--ink)">{h}</th>'
                 for h in ["Bag", "Type", "Height", "Weight", "Clubs", "Frosty pocket", "Strap"])
    rows = "".join("<tr>" + "".join(f'<td style="padding:10px 12px;border-bottom:.5px solid rgba(20,20,20,.15){";font-weight:500" if i == 0 else ""}">{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in SPECS)
    return f"""
<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr" id="size-guide">Which Sunday Golf Bag? A Size Guide</h2>
  <p class="cat-kicker"><strong>Size guide</strong>Sunday Golf publishes these specs on its own comparison page. Every bag has full-length dividers and is 600D nylon unless noted: the S-Class bags are polyurethane (vegan) leather and the Ranger is recycled nylon ripstop. If you play oversized grips, Sunday Golf points you to the Ryder 14 or the Big Rig.</p>
  <div style="overflow-x:auto;max-width:980px;margin:0 auto"><table style="width:100%;border-collapse:collapse;font-size:15px;min-width:640px">
    <thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table></div>
  <p class="cat-kicker" style="margin-top:24px"><strong>Our rule of thumb</strong>Par 3s and range sessions: the Loma. Walking nine with a half set: the Loma XL. Walking eighteen with most of your clubs: the El Camino. Full bag, carrying: the Ryder. Riding in a cart or pushing a cart: the Big Rig.</p>
</section>
"""
FAQ = [
 ("Who founded Sunday Golf?", "Ronan Galvin and Casey Mathews founded Sunday Golf in San Diego in August 2020, with Galen Brunelle also part of the founding team. Galvin had spent about a decade in golf bag product development before he took up the game at the Loma Club, a par 3 course in San Diego."),
 ("What is the Sunday Golf Loma bag?", "The Loma is Sunday Golf's original par 3 bag: 32 inches tall, 1.95 pounds, room for six clubs, a single strap and an insulated pocket for one can. It was designed for the Loma Club par 3 in San Diego and is named after it."),
 ("Which Sunday Golf bag should I buy?", "Pick by how many clubs you carry. The Loma holds 6, the Loma XL 8, the El Camino up to 12, and the Ryder, Ranger and Big Rig hold 14. The Big Rig is the cart bag; the rest are carry or stand bags."),
 ("What is a Frosty pocket?", "Sunday Golf's name for the insulated drinks pocket on every bag. It holds one can on the Loma, two on the Loma XL, four on the El Camino and Ryder, three on the Ranger and seven on the Big Rig."),
 ("Does Sunday Golf have a warranty?", "Yes. Sunday Golf offers a lifetime product warranty, plus free returns."),
 ("Can you personalize a Sunday Golf bag?", "Yes. Sunday Golf embroiders names or initials on the removable ball pocket, which takes 5 to 10 business days."),
 ("Where can I buy Sunday Golf in Austin?", "Sunday Golf sells direct at sundaygolf.com and says it is stocked by most major golf retailers and more than 1,000 pro shops, so big golf stores in Austin often carry the Loma and Ryder."),
 ("How much does Sunday Golf cost?", "On October 15, 2026, most of the store was on sale. Bags ran from $130 for the Loma to $400 for the Ranger, and accessories from $15 for par 3 tees."),
]
FRN = json.loads((ROOT / "research/sunday-golf/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-SG-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}'
            '.bk-founder{max-width:1100px}@media(max-width:820px){.bk-founder{grid-template-columns:1fr!important}}'
            '.ig-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:0 0 34px}.ig-grid figure{margin:0}.ig-grid img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block;background:#eceae5}.ig-cap{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink);opacity:.5;margin-top:8px;line-height:1.5}@media(max-width:720px){.ig-grid{grid-template-columns:repeat(2,1fr);gap:10px}}</style>\n')


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
            f'<a href="{url}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


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
    <span>San Diego &middot; est. 2020</span><span class="dot"></span>
    <span>24 picks &middot; prices checked October 15, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/btk-hero.jpg" alt="Four friends piled into a golf cart beside a green, arms up, with a Sunday Golf Loma bag standing next to the cart" fetchpriority="high" /></div></div>
"""
    body += TAKE
    body += band("course")
    body += FOUNDER
    body += size_guide()
    body += band("frosty")
    n = 1
    for s, b in zip(SECTIONS, [None, "details", "around"]):
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
    for leak in ("Mackem", "Kalamunda", "Howie", "No Dirt", "Lehi", "Rookline", "Bethpage", "Hudson", "LBB", "GolfPass", "Woodgrain", "Parmore", "Lazyface", "Mount Tee", "Melbourne", "Golf Today", "Substack", "San Diego Magazine", "Golf Digest"):
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
