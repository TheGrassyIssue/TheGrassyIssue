#!/usr/bin/env python3
"""build-matchstick-btk.py — Brand to Know: Matchstick Golf, 15 October 2026.
Lenny: "let's do a brand to know - https://matchstickgolf.com/", then "let's lean more on the ballmarkers, that's where they
started. Whats the TGI take? this is a very pop culture forward small business, why would someone support them?", then "let's build it".
FACTS (read Oct 15 2026, research/matchstick/sources.md): matchstickgolf.com about page (Dane Delgado bio: ex-NBA writer, learned at
par 3s in Salem, UO; Nile Johnson joined 2023), Dane's own blog posts (launch July 17 2021; lost marker; 800+ orders in seven months;
front-room apartment; work-live loft shop in St. Johns since June 2024; 33 rounds at Glendoveer), products.json descriptions and prices.
Quotes are Dane's own words from Matchstick's site, so no publication is named. All 30 picks in stock; no sale on.
PHOTOS: Matchstick's own (research/matchstick/frame.py). Founder image is Matchstick's published portrait of Dane (about page).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Brand to Know: Matchstick Golf, the Portland Ball Marker Brand With a Sense of Humor"
DESC = ("Brand to Know: Matchstick Golf. A former NBA writer lost his favorite ball marker, drew his own and built a Portland brand "
        "on hand-painted $20 markers: Putterade, Devil Horns, Cash Stack and more, plus one-of-one headcovers. 30 picks.")
H1 = "Brand to Know: Matchstick Golf &mdash; Ball Markers With a Story"
BC = "Matchstick Golf"
SLUG = "brand-to-know-matchstick-golf"
IMG = "/images/matchstick"
SHOP = "https://matchstickgolf.com/products/"
PK = json.loads((ROOT / "research/matchstick/picks.json").read_text())
NAME = {"buildyourowncustomgolf": "Custom Ball Markers", "cash": "Cash Stack", "ballmarkerflamingcoffe": "Flaming Mug",
        "usadreamteambasketball": "USA Basketball &ldquo;Dream Team&rdquo; Upcycled Driver Headcover",
        "osubeaversblackdrivern": "Matchstick x OSU Beavers Driver Headcover No. 1",
        "matchstickmanjonesrang": "Jones x Matchstick Ranger R Shag Bag, Black",
        "oregonstatebeavershead": "Oregon State Beaver, Brushed Gold"}
def price(d):
    p = float(d["price"])
    if d["key"] == "buildyourowncustomgolf":
        return "$120 mold fee + markers"
    return f"${p:,.0f}"
COPY = {
 "oldfashioned": "Matchstick&rsquo;s best seller started as a custom. A friend asked Dane for a marker for his annual guys&rsquo; trip, where they &ldquo;always&rdquo; drink too many Old Fashioneds the first night. Dane added the smoking cigar, liked it too much to keep it private, and his friend agreed to let him sell it. Orange peel, cherry, big ice cubes.",
 "transfusion": "Matchstick made golf&rsquo;s favorite cocktail in pink and lime green; it&rsquo;s the brightest thing you&rsquo;ll set down on a green.",
 "icedcoffeegolfballmark": "Matchstick made this one for hot summer rounds, which in Austin means about May through October.",
 "ballmarkerflamingcoffe": "Matchstick made this cartoon mug with its head on fire for golfers who putt like they&rsquo;re on fire. Matchstick drew it with Big Step Coffee in San Diego, which ships it.",
 "putteradefrost": "Matchstick based Putterade on the plastic sports drink bottle of the late 1990s; anyone who played Little League knows exactly which one. Eight flavors in stock; this is the blue.",
 "putteradelemonlime": "Matchstick makes the same bottle in lemon-lime. &ldquo;All the electrolytes you need to record circles on your scorecard,&rdquo; per Matchstick.",
 "devilhornsblackgold": "Matchstick credits Ronnie James Dio with the sign and pitches it at golfers whose &ldquo;irons are heavy metal.&rdquo; New in September in six colors; black and gold shown.",
 "truffleshuffle": "One of three markers Matchstick made for the 40th anniversary of a certain 1985 movie filmed in Astoria, Oregon. You know the dance. Limited edition.",
 "pirateflag": "From the same Astoria set: a skull-and-crossbones flag for golfers who never say die. Limited edition.",
 "skeletonkey": "Matchstick made a copper skeleton key as the third Astoria marker, to &ldquo;unlock the secret treasure.&rdquo; Limited edition.",
 "vwbus": "Dane made one pop-top camper out of his favorite parts of the VW Bus over the years, with a full kitchen and a golf bag inside.",
 "chefskull": "Matchstick made this skull in a chef&rsquo;s hat on gunmetal plating as a limited collab with The Generous Chef.",
 "cash": "Matchstick calls Cash Stack its most popular marker and &ldquo;often copied.&rdquo; It was one of the first eight designs in 2021: a black nickel stack of hundreds with a yellow band.",
 "pokerchip": "Matchstick made a solid metal poker chip with its own casino logo: red pine trees and the St. Johns Bridge, less than half a mile from the shop.",
 "reddice": "Matchstick made snake eyes in red glitter paint for the one-putt you need on 18.",
 "gaspumpgolfballmarker": "Matchstick made a red gas pump with a golf club leaning on it for the putts that need a little extra gas.",
 "firetruckgolfballmarke": "Matchstick made a fire truck with lights and big tires for days you&rsquo;re on fire on the greens.",
 "oregonstatebeavershead": "From the new officially licensed Matchstick x OSU collection, launched October 8. Eight Beaver markers in stock, from the classic head to the football helmet.",
 "teddyroosevelt": "Teddy in his Rough Riders uniform, &ldquo;for golfers who putt softly and swing the big stick.&rdquo; Proceeds go to the Roosevelt Golf Fund for public school youth golf in North Portland.",
 "ladylibertyballmarker": "A Statue of Liberty marker from a first-edition run limited to 50 pieces.",
 "buildyourowncustomgolf": "Matchstick will make your own marker for a golf trip, wedding party or bachelor weekend. You pay a one-time $120 mold fee plus the markers, and every one comes in the matchbox with free laser engraving.",
 "usadreamteambasketball": "Dane started sewing headcovers out of old sports gear. This one comes from a USA Basketball &ldquo;Dream Team&rdquo; piece, lined in Polartec fleece and stitched with marine-grade thread in his Portland workshop. One of one.",
 "ussoccerupcycledheadco": "Cut from a reclaimed U.S. men&rsquo;s national team snap-up jacket; the back panel spells USA as it wraps around the cover, with the white-and-red neck ribbing kept at the top. One of one.",
 "newyorkbasketballdrive": "Made from a vintage New York basketball jersey, with the Champion size tag moved to the top and the neckline ribbing at the bottom. One of one.",
 "rooseveltpatterndriver": "Matchstick made this cover from 100% recycled material in the pattern of Roosevelt High School, just down the road from the shop. Proceeds go to the Roosevelt Golf Fund, which buys clubs, balls and gear for the school&rsquo;s boys and girls golf teams.",
 "osubeaversblackdrivern": "Officially licensed: Matchstick cut this one from a reclaimed Oregon State knit jacket and paired it with 8 oz. waxed canvas. Polartec lining, UV and water treated.",
 "rooseveltpatterngolfto": "Matchstick put the Roosevelt pattern on a 24 by 16 inch waffle towel in black and yellow. Proceeds go to the Roosevelt Golf Fund.",
 "keylimepie": "Matchstick makes these ten green-and-white shorty ferrules for .355 taper shafts. Matchstick&rsquo;s line: &ldquo;the whipped cream on top of your club&rsquo;s look.&rdquo;",
 "matchstickmanjonesrang": "Matchstick took Jones Sports Co.&rsquo;s Ranger shag bag in recycled ripstop and embroidered its Matchstick Man on it. It holds six dozen balls or six cold cans. Made to order; allow about four weeks.",
 "tigerroarreliefprint": "A linoleum reduction print of Tiger roaring at the Masters, made in-house by Portland artist Audrey Delgado, Dane&rsquo;s mother. The block is destroyed as it&rsquo;s printed, so the run can never be made again.",
}
P = {d["key"]: ("Matchstick Golf", NAME.get(d["key"], d["title"].replace(" - ", ", ")), price(d), SHOP + d["handle"], COPY[d["key"]]) for d in PK}
SEC = [
 ("drinks", "The Drinks Cart", "<strong>Six markers</strong>Matchstick&rsquo;s most recognizable markers are drinks: two cocktails, two coffees and a late-90s sports drink bottle in eight flavors."),
 ("pop", "Pop Culture", "<strong>Six markers</strong>Matchstick made heavy metal hand signs, a three-marker set for a 1985 movie filmed on the Oregon coast, a VW camper and a skull in a chef&rsquo;s hat."),
 ("gamble", "Cash, Dice and Gasoline", "<strong>Five markers</strong>The marker that started it all, plus the rest of the money-and-horsepower shelf."),
 ("home", "Hometown and Custom", "<strong>Four picks</strong>Matchstick makes markers for Oregon State, Teddy Roosevelt for a North Portland high school, Lady Liberty, and one of your own."),
 ("covers", "Then He Started Sewing", "<strong>Five headcovers</strong>Matchstick&rsquo;s newest work isn&rsquo;t a marker. Dane now sews headcovers by hand from reclaimed jackets and jerseys, lined in Polartec fleece. Most are one of one; he also takes commissions if you bring your own garment."),
 ("around", "Around the Marker", "<strong>Four picks</strong>A towel, ferrules, a Jones collab and a print by Dane&rsquo;s mom."),
]
SECTIONS = [(h2, a, [d["key"] for d in PK if d["group"] == a], k) for a, h2, k in SEC]
N = 30
DATE = "2026-10-15"
PQ = {
 "launch": ("I like these. If someone else likes them, that&rsquo;s great.", "Dane Delgado, on his attitude at launch, 2022"),
 "muni": ("These are the types of courses that I play, almost exclusively.", "Dane Delgado, on municipal golf, 2021"),
 "drinks": ("Hey man, I drew this too good. I need to sell it to the public.", "Dane Delgado, on the Old Fashioned marker"),
 "covers": ("Let&rsquo;s reimagine and repurpose something for the golf course, together.", "Matchstick Golf, on its custom headcovers"),
 "pop": ("Your irons are heavy metal. You roll the rock.", "Matchstick Golf, on the Devil Horns marker"),
 "home": ("We think great designs are lost in the dilution of product and inventory.", "Matchstick Golf, on why it releases so few designs"),
 "around": ("How does this not already exist?", "Dane Delgado, on the one-line version of his business plan"),
}
BANDS = {
 "glove": ("On the Glove &middot; Matchstick&rsquo;s own photos",
  "Matchstick shoots its markers the way you&rsquo;ll see them: in a white glove, next to a ball, and out in the world.",
  [("life-1", "A gloved hand holding eight Matchstick ball markers, including a cash stack, a sports drink bottle and a burger", "A handful of Matchstick markers"),
   ("life-2", "The Cash Stack ball marker resting in the palm of a white golf glove", "Cash Stack, the original"),
   ("life-3", "A Pabst Light and Matchstick Golf decal on the side of a golf cart", "The Project Pabst pop-up")]),
 "muni": ("Muni Golf &middot; from Matchstick&rsquo;s blog",
  "Dane writes about the courses he plays, and they&rsquo;re mostly public. One essay asks what a city-owned course owes its community.",
  [("life-4", "Aerial view of a green and bunkers at Glendoveer East in Portland", "Glendoveer East No. 15, Portland"),
   ("life-5", "A sign in the trees reading Possession of Range Balls Is Unlawful", "Possession of range balls is unlawful"),
   ("life-6", "A golfer finishing a swing on a links course at dusk", "From the Matchstick blog")]),
 "shop": ("The Matchbox and the Shop &middot; Matchstick&rsquo;s own photos",
  "Every marker ships in a matchbox with a seal sticker. Since 2024 the shop is Dane&rsquo;s work-live loft in St. Johns, open by posted hours or appointment.",
  [("life-7", "A stack of Matchstick matchboxes with a Cash Stack marker on top", "The matchbox"),
   ("life-8", "An empty loft space with concrete floors and a big window before Matchstick moved in", "HQ in St. Johns, before move-in"),
   ("life-9", "Dane Delgado standing on a fairway lined with tall firs", "Dane on the course")]),
 "sew": ("The Headcovers &middot; Matchstick&rsquo;s own photos",
  "Old jerseys and jackets, cut down and rebuilt as covers. The Oregon State line is officially licensed.",
  [("life-10", "A pile of Matchstick headcovers sewn from sports jerseys, including New York and Seattle colors", "Custom covers from customers&rsquo; jerseys"),
   ("life-11", "Oregon State Beavers headcovers and ball markers laid out on a wood table with tees", "Matchstick x OSU"),
   ("life-12", "Close-up of the USA Dream Team headcover showing the red fleece lining", "Polartec lining, Dream Team cover")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Matchstick Golf makes the ball marker you end up explaining to your playing partners. A Putterade shaped like the plastic sports drink bottle from the late &rsquo;90s. Devil Horns for the guy with a speaker on his cart. An Old Fashioned with a cigar smoking on the rim. A kid doing the Truffle Shuffle. Each one is a small joke, and the joke is the point: Dane Delgado started Matchstick believing a marker should &ldquo;tell a story about a golfer, give them confidence when lining up their putt, and invite an inquiry.&rdquo;</p>
    <p>So why buy from a one-designer shop in North Portland instead of grabbing a marker at the pro shop? Because Matchstick fixed what makes most markers annoying. Every one is magnetic, hand painted and polished, USGA conforming and small enough not to deflect a playing partner&rsquo;s putt, with no logo on it, in a matchbox, for $20. Dane draws every design himself, says each one takes months, and kills plenty before they&rsquo;re made. He plays the golf we play, too: in one three-year stretch he logged 33 rounds at a Portland city-run course and fewer than 10 anywhere that cost more than $75. Your money goes to a guy who loves munis, uses Portland vendors where he can, and sends the proceeds of his Roosevelt line to a local high school&rsquo;s golf teams. That&rsquo;s the kind of brand TGI exists to cover.</p>
    <h2 class="products-hdr btk-story-hdr">Started With a Lost Marker</h2>
    <p>Dane grew up in Oregon&rsquo;s Willamette Valley, tagging along with his uncle at small par 3 courses in Salem, and got serious about golf at the University of Oregon. He spent the first half of his career as a sportswriter covering the NBA. In the summer of 2020 he lost his favorite ball marker. Everything he found to replace it was too big, too expensive or badly drawn, so he drew his own.</p>
    <p>He wrote a business plan that came down to one question, &ldquo;How does this not already exist?&rdquo;, and launched Matchstick on July 17, 2021, a sweaty 88-degree Saturday, with eight designs. He ran it at night from the front room of a small apartment. By September it was a real business, and within seven months it had more than 800 orders, shipped as far as Japan, Ireland and Sweden. Nile Johnson, a friend from the Portland golf scene, joined in 2023 to run sales. In June 2024 Matchstick opened a shop in Dane&rsquo;s work-live loft in St. Johns, down the road from Wildwood, with a putting mat and a PlayStation.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>2021, Portland, Oregon</span></div>
      <div class="sidebar-detail"><span class="l">Founder</span><span>Dane Delgado</span></div>
      <div class="sidebar-detail"><span class="l">Known for</span><span>Hand-painted ball markers</span></div>
      <div class="sidebar-detail"><span class="l">Marker price</span><span>$20 most</span></div>
      <div class="sidebar-detail"><span class="l">Shop</span><span>St. Johns, North Portland</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$20&ndash;$167</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Putterade, Blue</span></div>
      <a href="https://matchstickgolf.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit Matchstick Golf &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#MatchstickGolf</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#BallMarkers</span>
        <span class="hashtag">#PortlandGolf</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FOUNDER = f"""
<section class="products" style="border-top:none;padding-top:48px">
  <h2 class="products-hdr" id="in-his-words">In His Words &mdash; Dane Delgado</h2>
  <p class="cat-kicker"><strong>Founder&rsquo;s voice</strong>Dane writes Matchstick&rsquo;s blog himself. Quotes below are verbatim from his posts on the brand&rsquo;s site, 2021 to 2024.</p>
  <div class="bk-founder" style="display:grid;grid-template-columns:340px 1fr;gap:40px;align-items:start;max-width:1100px">
    <div style="border:.5px solid var(--ink);overflow:hidden">
      <img src="{IMG}/founder.jpg" alt="Dane Delgado, founder of Matchstick Golf, in a black cap and gold chain in front of a bright mural" loading="lazy" style="width:100%;aspect-ratio:4/5;object-fit:cover;display:block" />
    </div>
    <div style="font-size:16px;line-height:1.7">
      <p>He launched after five months of planning because, in his words, &ldquo;I decided I simply couldn&rsquo;t any longer.&rdquo; His first post set the rules. Markers &ldquo;shouldn&rsquo;t be large, chunky, ostentatious objects to brag about.&rdquo; They should be small enough to stay playable, because &ldquo;a playing partner is going to be irate if you don&rsquo;t happen to move your mark&rdquo; and it sends their putt off line. And they should be reasonably priced.</p>
      <p style="margin-top:16px">A year in, he boiled the whole plan down to a sentence: markers &ldquo;should be unobtrusive to your playing partners, they should have a clean, polished finish, the art should be thoughtful and not hack, the presentation should be above the price point, and they shouldn&rsquo;t be the size of a goddamn poker chip.&rdquo;</p>
      <p style="margin-top:16px">He is honest about how small it started. &ldquo;Matchstick was supposed to be a lark. An artistic outlet for a former creative, failed time and again by the free market for personal golf accessories.&rdquo; Two years later he called it something else: &ldquo;At our core, Matchstick is an art company. We make drawings into physical art that are useable every day on the golf course.&rdquo;</p>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:28px;padding-top:24px;border-top:.5px solid rgba(20,20,20,.15)">
        <div>
          <div style="font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;opacity:.55;margin-bottom:6px">The Pitch</div>
          <div style="font-size:14px;line-height:1.6;opacity:.85">&ldquo;Bring better artwork to the course for the regular golfer.&rdquo;</div>
        </div>
        <div>
          <div style="font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;opacity:.55;margin-bottom:6px">The Shop</div>
          <div style="font-size:14px;line-height:1.6;opacity:.85">&ldquo;I&rsquo;m here all the time anyway, why not let people swing by?&rdquo;</div>
        </div>
        <div>
          <div style="font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;opacity:.55;margin-bottom:6px">The Commitment</div>
          <div style="font-size:14px;line-height:1.6;opacity:.85">&ldquo;I got a tattoo of our logo on my arm for everyone to see.&rdquo;</div>
        </div>
      </div>
    </div>
  </div>
</section>
"""
SPEC = [("Magnetic", "Sticks to a hat clip or divot tool"), ("Oven-cured enamel", "Hand painted, then polished"),
        ("High-polish back", "Clean finish on both sides"), ("USGA conforming", "Legal in competition"),
        ("No logo", "The art is the whole face"), ("Matchbox packaging", "Ships in a matchbox with a seal sticker")]
def explainer():
    cells = "".join(f'<div style="padding:18px 16px;border:.5px solid rgba(20,20,20,.2)"><div style="font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--grass);margin-bottom:6px">{a}</div><div style="font-size:15px;line-height:1.5">{b}</div></div>' for a, b in SPEC)
    return f"""
<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr" id="what-makes-a-matchstick-marker">What Makes a Matchstick Marker</h2>
  <p class="cat-kicker"><strong>The spec</strong>Matchstick lists the same details on every marker it sells. Most are $20.</p>
  <div class="mg-spec" style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;max-width:980px;margin:0 auto">{cells}</div>
</section>
"""
FAQ = [
 ("Who owns Matchstick Golf?", "Dane Delgado founded Matchstick Golf in Portland, Oregon in 2021 and is its lead designer. He was a sportswriter covering the NBA before starting the brand. Nile Johnson joined in 2023 to run business development."),
 ("Where is Matchstick Golf based?", "In the St. Johns neighborhood of North Portland, Oregon. The shop is in Dane's work-live loft at 7440 N. Charleston Ave., open by posted hours or appointment, and local orders can be picked up there."),
 ("How much are Matchstick ball markers?", "Most Matchstick ball markers are $20. Licensed Oregon State markers are $24 and limited editions like Lady Liberty are $30."),
 ("Are Matchstick ball markers magnetic?", "Yes. Every Matchstick marker is magnetic, made with oven-cured enamel and a high-polish back, USGA conforming, and packed in a matchbox."),
 ("Can Matchstick make a custom ball marker?", "Yes. Custom markers for trips, weddings and events cost a one-time $120 mold fee plus the markers, with free laser engraving and matchbox packaging."),
 ("Does Matchstick Golf make headcovers?", "Yes. Matchstick hand sews headcovers in Portland from reclaimed jackets and jerseys or premium fabric, lined with Polartec fleece. Most are one of one, and it takes custom commissions."),
 ("What is the Roosevelt Golf Fund?", "A Matchstick project for Roosevelt High School in North Portland. Proceeds from its Roosevelt pattern headcovers, towel and Teddy Roosevelt marker buy clubs, balls and gear for the school's boys and girls golf teams."),
]
FRN = json.loads((ROOT / "research/matchstick/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-MG-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}'
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
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>October 15, 2026</span><span class="dot"></span>
    <span>Portland &middot; est. 2021</span><span class="dot"></span>
    <span>30 picks &middot; prices checked October 15, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/btk-hero.jpg" alt="Matchstick Golf&rsquo;s Cash Stack ball marker, a stack of hundred-dollar bills with a yellow band, on bamboo tees in a white golf glove" fetchpriority="high" /></div></div>
"""
    body += TAKE
    body += band("glove")
    body += pq("launch")
    body += FOUNDER
    body += explainer()
    body += pq("muni")
    body += band("muni")
    n = 1
    for s, b in zip(SECTIONS, [None, None, "shop", None, "sew", None]):
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
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Kalamunda", "Howie", "No Dirt", "Lehi", "Rookline", "Bethpage", "Hudson", "LBB", "GolfPass", "Woodgrain", "Parmore", "Lazyface", "Mount Tee", "Melbourne", "Sunday Golf", "Loma", "Sports Illustrated", "GolfLink", "Golf Link"):
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
