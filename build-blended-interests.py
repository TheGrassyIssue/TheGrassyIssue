#!/usr/bin/env python3
"""build-blended-interests.py — "Golfer And": gear for six blended interests. Cloned from build-radar-three-2.py. 19 October 2026.
Lenny: "a post that's about blending interests — Golfer / Climber, Techie, Fly Fishing, Vintage enthusiasts", then agreed to add
Car person and Surfer, "let's build it". Four picks per pairing, chosen by us from three research sweeps.
FACTS: each brand's own product and About pages, read October 19, 2026 (research/blended/picks.py lists URLs and images).
Voice Caddie and Louisville Golf store JSON was rate-limited at build time; prices are from the research sweep the same day.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Golf Gear for Climbers, Anglers, Techies, Surfers and More"
DESC = ("Golf plus the other thing you love: gear for the climber, the techie, the fly fisherman, the vintage nut, "
        "the car person and the surfer. 36 picks from independent brands, with prices.")
H1 = "Golfer And: Gear for Six Blended Interests"
BC = "Golfer And"
SLUG = "golf-gear-for-climbers-anglers-techies-surfers"
IMG = "/images/blended"
SHOP = ""
P = {
 "c1": ("Metalwood Studio", "Bomber Pant", "$208", "https://metalwood.studio/products/bomber-pant-black",
   "A convertible pant-to-short from the LA golf studio, with what Metalwood itself calls deep, climbing-inspired pockets lined with leopard-print gussets. 100% polyester and a straight leg, in black or seafoam."),
 "c2": ("Howler Brothers", "Reimers Trek Pants", "$119", "https://howlerbros.com/products/reimers-trek-pants",
   "Designed in Austin for camping, hiking and climbing: stretch fabric, reinforced knees and a bungee hem. Howler doesn&rsquo;t sell it as a golf pant, but it moves like the good ones. Drab Olive or Midnight, 32-inch inseam only."),
 "c3": ("Arcade Belts", "Golf Stretch Belt Kit", "$131.95", "https://arcadebelts.com/products/golf-stretch-belt-kit",
   "Three stretch webbing belts in one box: a black Aero with a magnetic buckle, a charcoal Motion and a khaki Futureweave. Arcade&rsquo;s own story names climbing first among the sports it designs for, and this kit is its answer for the course. On sale when we checked."),
 "c4": ("KAVU", "Chilliwack Short", "$150", "https://kavu.com/products/chilliwack-short",
   "Heavy organic cotton canvas with a built-in belt, a half-elastic waist and a gusseted crotch, hand cut and sewn in Seattle. KAVU says exactly those details made the style an instant hit with climbers. Sizes were thin when we checked; Heritage Khaki was on sale at $112.50."),
 "t1": ("Arccos", "Arccos Air", "$349.99", "https://arccosgolf.com/products/air",
   "A tracker smaller than an AirPods case that clips to your belt or sits in a pocket. Motion sensors and GPS pick up every shot on their own, with no club sensors and no phone needed. Arccos says its AI was trained on 1.5 billion real shots."),
 "t2": ("Voice Caddie", "Swing Caddie SC4 PRO", "$599.99", "https://voicecaddie.com/products/sc4-pro",
   "A launch monitor with an alignment stand in the box and a 3D driving range in the app. Voice Caddie launched what it calls the first voice-output GPS rangefinder in 2011 and still makes most of its products in South Korea."),
 "t3": ("Blue Tees Golf", "Player Pro GPS Speaker", "$199.99", "https://blueteesgolf.com/products/player-pro",
   "A Bluetooth speaker with a touchscreen that shows hole layouts, green heat maps and live distances, plus scoring and shot tracking. Blue Tees started with &ldquo;five friends, one laser&rdquo; and lists design among its rules."),
 "t4": ("Shot Scope", "LM1 Launch Monitor", "$199.99", "https://shotscope.com/us/shop/products/golf-launch-monitors/lm1-launch-monitor/",
   "A pocket launch monitor from Scotland: club speed, ball speed, smash factor, carry and total on a 3.5-inch color screen, with about five hours of battery. Shot Scope promises its software and updates stay subscription-free for life."),
 "f1": ("Free Fly", "Men&rsquo;s Elevate Polo", "$88", "https://freeflyapparel.com/products/mens-elevate-polo-bright-white",
   "Free Fly was started in 2011 by fly-fishing guides from Montana and is now based in Charleston. The Elevate is a soft lyocell-blend polo that dries fast and resists odor, and the brand pitches it for your next round of golf."),
 "f2": ("North Coast Golf Co.", "Fisherman Golf Glove", "$28", "https://northcoastgolfco.com/products/north-coast-fisherman-golf-glove",
   "A white golf glove with a tan tab and North Coast&rsquo;s trout logo, from a collection built around Michigan&rsquo;s trout streams and the Great Lakes. There&rsquo;s a matching corduroy hat, socks and a bucket hat."),
 "f3": ("Pins &amp; Aces", "Trout Ball Marker", "$14.95", "https://pinsandaces.com/products/trout-ball-marker",
   "A rainbow trout in cast stainless steel with enamel color and a magnetic back, from the family-owned Colorado brand. Pins &amp; Aces also makes a Divots &amp; Dry Flies rope hat and a trout driver cover."),
 "f4": ("Smathers &amp; Branson", "Fly Fishing Life Belt", "$195", "https://smathersandbranson.com/products/fly-fishing-life-belt-classic-navy",
   "Hand-stitched needlepoint in French cotton thread, a fly-fishing scene on navy, lined with Italian leather and finished with a solid brass buckle. Smathers &amp; Branson has made needlepoint belts since 2004."),
 "v1": ("Louisville Golf", "Calamity Jane Hickory Putter", "$225", "https://louisvillegolf.com/products/calamity-jane%E2%84%A2",
   "A replica of Bobby Jones&rsquo;s Calamity Jane, down to the three whipping points, on a solid hickory shaft with a hand-wrapped leather grip. Made in Louisville, Kentucky, and approved by the Society of Hickory Golfers."),
 "v2": ("Louisville Golf", "Classic 50&rsquo;s Persimmon Driver", "$375", "https://louisvillegolf.com/products/classic-50s-persimmon-driver",
   "A new persimmon driver in the pear shape of the 1950s: 190cc, 11 degrees, a hand-whipped hosel and a mahogany finish, cut from blocks Louisville Golf picks from a family-run saw mill. Its steel shafts were discontinued in 2017, so they&rsquo;re limited to what&rsquo;s left."),
 "v3": ("Jan Craig Headcovers", "Navy &amp; White Pom Driver Cover", "$84", "https://www.jancraigheadcovers.com/products/driver-460-headcover-8-in-pom-1-stripe-navy-white",
   "Hand-knit in the USA from 100% wool: the pom-top sock cover Jan Craig has made since a young Jack Nicklaus ordered a set in the brand&rsquo;s first months. Fits a 460cc driver; custom orders take six to eight weeks."),
 "v4": ("Mulligan&rsquo;s Country Club", "Vintage Tabasco Bloody Mary Polo", "$55", "https://www.mulliganscountryclub.com/shop/vintage-tabasco-bloody-mary-polo",
   "Real secondhand golf gear from a vintage shop in Westwood, Kansas, that opened in 2024 under the motto &ldquo;Reduce. Reuse. Reswing.&rdquo; This one is a vintage Tabasco polo printed with Bloody Marys, golf bags and tees. It&rsquo;s one of one, so it may be gone."),
 "r1": ("STITCH Golf", "SL2 Gen 2 Stand Bag", "$398", "https://stitchgolf.com/products/sl2-gen-2",
   "STITCH, from Cary, North Carolina, says it draws on vintage motorsports and superleggera cars; its first bag, the SL1, was named for Superleggera. The SL2 Gen 2 weighs 5.5 pounds and has a &ldquo;GT Saddle Pocket&rdquo; and swappable straps."),
 "r2": ("Malbon Golf", "Checkered Driver Cover", "$128", "https://malbon.com/products/checkered-driver-cover-black-white",
   "Hand-sewn leather panels with contrast piping in a black-and-white check, which Malbon says brings Formula 1 heritage to the bag. Malbon also has an officially licensed F1 Miami Grand Prix capsule."),
 "r3": ("Ghost Golf", "Rally Headcover", "$75", "https://ghostgolf.com/products/rally-headcover-white-black",
   "Checkered PU leather with RALLY across it, in driver, 3-wood, 5-wood and hybrid sizes and four colorways. The cheapest way to put a checkered flag in the bag."),
 "r4": ("DRVN Golf Co.", "Gated Shift Ball Marker", "$65", "https://drvngolfco.com/products/gated-six-ball-marker",
   "Stainless steel cut with the exposed shift gate of an analog-era manual supercar: reverse plus six forward gears. From DRVN Golf Co., the motorsport-minded putter maker in our <a href=\"/drops/dim-sum-rowena-drvn-small-golf-brands\" style=\"border-bottom:1px solid var(--ink)\">three small brands post</a>."),
 "s1": ("Vissla", "Bogey Man Eco Drirelease Polo", "$60", "https://www.vissla.com/products/m900ebog-bogey-man-eco-drirelease-ss-polo-sag-sage-m900ebog",
   "A soft, fast-drying polo from an Aliso Viejo surf brand, mostly recycled polyester with UPF 40+ and an enzyme wash. Vissla&rsquo;s own line for it: a polo for the round that starts after the morning surf. In sage or dark denim."),
 "s2": ("Kahala", "brrr&deg; Performance Polo, Surf Check", "$105", "https://kahala.com/products/brrr-%C2%AE-performance-polo-surf-check",
   "A Honolulu family company since 1936, Kahala printed this one with surfers at the water&rsquo;s edge checking the break. Cooling, quick-dry stretch fabric with UPF and a classic collar, so it passes a dress code and still reads North Shore."),
 "s3": ("Dormie Workshop", "Surfboard Hybrid Cover", "$145", "https://dormieworkshop.com/products/surfboard",
   "Italian leather with a baby-blue pinstripe inspired by classic longboards and a surf-style Dormie crest, handmade in Halifax and Los Angeles. Dormie made it for the golfer who swaps tees for tide charts."),
 "s4": ("Seamus Golf", "Hand Forged Big Wave Ball Marker", "$36", "https://seamusgolf.com/products/hand-forged-big-wave-ball-mark-steel",
   "Mild steel, forged by a Portland blacksmith and stamped with the Hawaiian Islands, the home of big-wave surfing. Seamus is family-owned and stamps your initials for free."),
 "c5": ("Stio", "Men&rsquo;s Pinion Down Sweater", "$269", "https://www.stio.com/products/mens-pinion-down-sweater",
   "A light down jacket from Jackson, Wyoming: recycled Pertex Quantum ripstop and 800-fill water-repellent down, and it stuffs into its own chest pocket. Stio says it sits under a harness or over a button-up, so it packs into a golf bag for cold mornings."),
 "c6": ("Topo Designs", "Twill Rope Cap", "$38", "https://topodesigns.com/products/twill-rope-cap-golden-horizon",
   "A golf rope cap, except the rope is paracord, from a Colorado brand that started sewing climbing and hiking packs in a Fort Collins basement in 2008. Soft five-panel snapback with a sunrise patch."),
 "t5": ("Stewart Golf", "Q Follow", "$3,049", "https://www.stewartgolfusa.com/products/stewart-golf-q-follow",
   "A compact electric caddie that follows you down the fairway on its own, or runs by remote, built on a composite chassis and handbuilt in Great Britain. Stewart is family-owned and runs its US operation out of Houston."),
 "t6": ("Square Golf", "HE Launch Monitor", "$699", "https://squaregolf.com/products/square-golf-he-launch-monitor",
   "A small camera-based launch monitor for the living room: high-speed machine vision, eight hours of battery and Bluetooth to a phone or PC, with a swing stick and marked balls in the box for spin readings."),
 "f5": ("Duck Camp", "Trout Patch Performance Perforated Hat", "$36", "https://duckcamp.com/products/trout-patch-performance-perforated-hat-highrise",
   "A vented, quick-dry cap with a trout-shaped patch from an Austin hunting and fishing brand whose motto is &ldquo;Fish to catch, birds to hunt, time to kill.&rdquo; Built for the river, and just as good on a hot muni."),
 "f6": ("Winston Collection", "Trout Pull-Up Leather Driver Cover, Whiskey or Navy", "$139.99", "https://winstoncollection.com/products/deer-premium-pullup-leather-golf-headcovers-1",
   "Pull-up leather that darkens and creases the more you carry it, with small leaping trout embroidered across the body and a plaid fleece lining. Handcrafted in the USA by the Michigan headcover maker. Comes in whiskey or navy (both shown), plus a matching hybrid size."),
 "v5": ("Scotch &amp; Skins", "Magnolia Hickory Alignment Sticks", "$75", "https://scotchandskins.com/products/magnolia-1",
   "Hickory, the old shaft wood, turned into a practice tool: 42-inch Grade A Appalachian hickory sticks sealed with beeswax and finished with bronze caps, handcrafted in the USA. Free engraving was on offer when we checked."),
 "v6": ("Modest Vintage Player", "PRO Houndstooth Cabretta Gloves, 2-Pack", "$65", "https://modestvintageplayer.com/products/pro-houndstooth-cabretta-leather-golf-gloves-brown-2-pack",
   "Two cabretta leather gloves with a brown houndstooth back, from a brand that makes gear inspired by the athletes of bygone eras. The easiest way to wear the 1960s every round."),
 "r5": ("Sunday Swagger", "Crew Chief Pennzoil Button Up 2.0", "$79", "https://sundayswagger.com/products/crew-chief-pennzoil%C2%AE-button-up-2-0",
   "An officially licensed Pennzoil and Team Penske golf button-up with the oil-can patch on the chest: stretch, moisture-wicking and UPF 50+. Sunday Swagger says it brings pit-lane precision to the fairway."),
 "r6": ("Devereux Golf", "Keep the Pace Tee", "$39", "https://devereuxgolf.com/products/keep-the-pace-tee-powder-blue",
   "A racing-badge back print with crossed checkered flags and &ldquo;Devereux Golf Racing: Keep Pace of Play.&rdquo; Devereux says it was inspired by vintage racing graphics and one of golf&rsquo;s unwritten rules."),
 "s5": ("Linksoul", "Hokusai Wave Camp Hat", "$38", "https://linksoul.com/products/ls8215-dusty-sage",
   "An unstructured six-panel in water- and sweat-resistant fabric with an embroidered Hokusai wave patch, from the Carlsbad brand John Ashworth started to blend golf with surfing and everything else. Dusty sage or midnight."),
 "s6": ("Slowtide", "Sublime Golf Towel", "$20", "https://slowtide.co/products/40-oz-sublime-golf-towel",
   "A quick-dry golf towel with the sun artwork of Sublime, the Long Beach band, from a towel maker rooted in Hawai&lsquo;i and Vancouver Island. It clips to the bag. On sale from $30 when we checked."),
}
SECTIONS = [
 ("Golfer &amp; Climber", "climber", ["c1","c2","c3","c4","c5","c6"],
  "<strong>Six picks &middot; $38&ndash;$269</strong>For the person whose gym has walls instead of machines. Climbing gear and golf want the same things: stretch, tough fabric, a belt that moves and a layer that packs small. We couldn&rsquo;t find a climbing brand making golf gear yet, so these come from both directions: golf pieces with climbing DNA and climbing brands whose kit works on a course."),
 ("Golfer &amp; Techie", "techie", ["t1","t2","t3","t4","t5","t6"],
  "<strong>Six picks &middot; $199.99&ndash;$3,049</strong>For the golfer with three apps open and a spreadsheet of carry numbers. We skipped the obvious giants: a tracker with no club sensors, three launch monitors under $700, a speaker with a screen and a caddie that follows you."),
 ("Golfer &amp; Fly Fisherman", "fly", ["f1","f2","f3","f4","f5","f6"],
  "<strong>Six picks &middot; $14.95&ndash;$195</strong>For the angler who plays a morning round and fishes the evening hatch. The two sports share early starts, patience and an eye for small details. These come from the river side."),
 ("Golfer &amp; Vintage Nut", "vintage", ["v1","v2","v3","v4","v5","v6"],
  "<strong>Six picks &middot; $55&ndash;$375</strong>For the golfer who would rather hit hickory and persimmon than titanium. A Bobby Jones putter, a 1950s driver, the pom cover Nicklaus carried, a genuine vintage polo, hickory alignment sticks and houndstooth gloves, all for sale today."),
 ("Golfer &amp; Car Person", "car", ["r1","r2","r3","r4","r5","r6"],
  "<strong>Six picks &middot; $39&ndash;$398</strong>For the golfer who knows what a superleggera is. Checkered flags, a pit-crew shirt and a shift gate, from a bag brand built on vintage motorsport to a $65 ball marker."),
 ("Golfer &amp; Surfer", "surf", ["s1","s2","s3","s4","s5","s6"],
  "<strong>Six picks &middot; $20&ndash;$145</strong>For the dawn-patrol surfer who tees off at ten. Two polos from surf and Hawaiian brands, a longboard headcover, a big-wave ball marker, a wave hat and a towel with some Long Beach sun in it. Salt air, slow pace, no rush on the back nine."),
]
N = 36
PQ = {}
CAP = "Photography &middot; each brand&rsquo;s own"
BANDS = {}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Nobody is only a golfer. The guy on the first tee at Lions is also a climber, or a car person, or someone who checks the surf report before the tee sheet. For a long time golf gear pretended otherwise: one look, one catalog, one kind of person. The independent brands are the ones changing that, because they&rsquo;re started by people with a second obsession.</p>
    <p>So we put together six pairings, six picks each. Some brands come from the other world and drift toward golf, like Free Fly, started by fly-fishing guides, or Kahala, a Honolulu shirt company since 1936. Some are golf brands that wear their other love openly: STITCH named its first bag after a superleggera, and Metalwood says its pockets are climbing-inspired. And a few are simply the real thing from the other world that happens to work on a course, like a down layer built to go under a climbing harness.</p>
    <p>The picks run from a $14.95 trout ball marker to a $3,049 caddie that follows you around. Almost everything comes from a small, founder-led company, and a handful are new to TGI. If your second interest isn&rsquo;t here, tell us. There are a lot more pairings to make.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Pairings</span><span>Six</span></div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>Six each, 36 in all</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$14.95&ndash;$3,049</span></div>
      <div class="sidebar-detail"><span class="l">Austin brands</span><span>Howler Brothers and Duck Camp</span></div>
      <div class="sidebar-detail"><span class="l">Cheapest</span><span>Pins &amp; Aces Trout Ball Marker</span></div>
      <div class="hashtags">
        <span class="hashtag">#GolferAnd</span>
        <span class="hashtag">#IndieGolf</span>
        <span class="hashtag">#GolfGifts</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("What golf gear is good for a golfer who also climbs?", "Look for stretch pants with deep pockets and a small drawstring pouch. Metalwood Studio's Bomber Pant ($208) has climbing-inspired pockets, Howler Brothers' Reimers Trek Pants ($119) are a climbing pant from Austin, and an Arcade's Golf Stretch Belt Kit ($131.95) comes from a belt brand built for climbers. Prices checked October 19, 2026."),
 ("What is the best golf tech gift under $700?", "On October 19, 2026 our picks were the Arccos Air tracker ($349.99), the Voice Caddie SC4 PRO launch monitor ($599.99), the Blue Tees Player Pro GPS speaker ($199.99), the Shot Scope LM1 launch monitor ($199.99), which has no subscription, and the Square Golf HE launch monitor ($699)."),
 ("Where can I buy new persimmon or hickory golf clubs?", "Louisville Golf in Kentucky still makes both: a Calamity Jane hickory putter replica ($225) and a Classic 50's persimmon driver ($375) on October 19, 2026."),
 ("What golf gear suits a surfer?", "Look for ocean-rooted brands making golf pieces: Vissla's Bogey Man polo ($60), Kahala's Surf Check performance polo ($105), Dormie Workshop's longboard-striped Surfboard hybrid cover ($145) and Seamus Golf's hand-forged Big Wave ball marker ($36), all checked October 19, 2026."),
 ("Are there golf gifts for fly fishermen?", "Yes. North Coast Golf Co. makes a trout-logo golf glove ($28), Pins & Aces a trout ball marker ($14.95), Smathers & Branson a fly-fishing needlepoint belt ($195), Free Fly, founded by fly-fishing guides, makes a polo it pitches for golf ($88), and Austin's Duck Camp makes a trout-patch performance hat ($36)."),
]
FRN = json.loads((ROOT / "research/blended/frames.json").read_text())
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
         "url": URL, "image": og, "datePublished": "2026-10-19", "dateModified": "2026-10-19",
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
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Six pairings &middot; golf plus the thing you love</span><span class="dot"></span>
    <span>36 picks &middot; prices checked October 19, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Three photos side by side: a golfer in Metalwood climbing-pocket pants on an indoor putting green, a gloved hand holding a fly rod over a river, and a Dormie Workshop headcover with surf stripes and a shaka" fetchpriority="high" /></div></div>
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
    for leak in ("Mackem", "Kalamunda", "Dim Sum", "Rowena", "Woodgrain", "Rookline", "Bethpage", "LBB", "GolfPass"):
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
