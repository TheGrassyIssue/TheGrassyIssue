#!/usr/bin/env python3
"""build-dogs-golf.py — Dogs and Golf. 22 October 2026. Cloned from build-sloat-btk.py.
Lenny: "Let's do a post about Dogs & golf, products and our personal stance on dogs on the course" -> stance: "All for it, be careful and mindful
but yeah bring him along and the best golf dogs belong to the greenskeepers" -> "finish up the dogs post" (all 27 picks; his own dog story to add when he sends it).
FACTS: research/dogs-golf/brief.md (Golf Digest 2014, GOLF.com 2022, GolfPass 2015, City of Austin Roy Kizer rules, WXYZ, NBC, KOAA, brand pages).
Prices/stock: each store, Oct 22 2026 (picks.json). Hero + band: Sounder's own photos. Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Dogs on the Golf Course: Our Take, and 29 Pieces of Golf Dog Gear"
DESC = ("Should you bring your dog golfing? We're all for it, carefully. Where dogs are welcome, course etiquette, and 29 golf dog collars, "
        "bandanas, bowls and headcovers.")
H1 = "Dogs and Golf: Bring Them Along (Carefully)"
BC = "Dogs and Golf"
SLUG = "dogs-and-golf"
IMG = "/images/dogs-golf"
SHOP = ""
P = {
 "d1": ("Brewster Belt", "On Par Golf Needlepoint Dog Collar", "$85", "https://brewsterbelt.com/products/on-par-golf-needlepoint-dog-collar",
   "Hand needlepoint backed with top-grain leather and a solid brass buckle in a silver finish. Made to order: you get a digital preview in about three to five business days, and nothing is stitched until you approve it."),
 "d2": ("Brewster Belt", "Yellow Golf Cart Needlepoint Dog Collar", "$85", "https://brewsterbelt.com/products/yellow-golf-cart-needlepoint-dog-collar",
   "The same build with a yellow golf cart stitched down the strap. Brewster also does argyle, putting and flag patterns at the same price."),
 "d3": ("The Worthy Dog", "Golf Collar", "$20.50", "https://theworthydog.com/products/golf-collar-4785",
   "Woven golf-print ribbon on nylon webbing with a quick-release buckle, in green or pink. There&rsquo;s a matching lead, bandana and toy."),
 "d4": ("The Worthy Dog", "Golf Lead", "$21", "https://theworthydog.com/products/golf-lead-4786",
   "The matching lead, same golf print over nylon webbing."),
 "d7": ("Rhoback", "The Mulligan Performance Dog Bandana", "$26", "https://rhoback.com/products/the-mulligan-performance-bandana",
   "Quick-drying four-way-stretch fabric in fairway green. Rhoback is named after the Rhodesian Ridgeback, so the dog gear isn&rsquo;t an afterthought."),
 "d8": ("Rhoback", "The Birdie Stripe Performance Dog Bandana", "$26", "https://rhoback.com/products/dogs-accessories-performance-bandana-the-birdie-stripe-fairway-green-fleet-navy",
   "Green and navy stripes, breathable and one size. Rhoback pitches it for a hike or for watching golf at home."),
 "d9": ("The Foggy Dog", "Golf Appliqu&eacute; Dog Bandana", "$29", "https://www.thefoggydog.com/products/golf-applique-dog-bandana",
   "A navy triangle tie with a chenille putting green and flag, and a green hem. Add your dog&rsquo;s name if you like. Three sizes."),
 "d10": ("The Worthy Dog", "Golf Bandana", "$20", "https://theworthydog.com/products/golf-bandana-5265",
   "A square tie-on bandana in soft polyester, in the same golf print as the collar."),
 "d13": ("Sounder", "Sounder x Yeti Dog Bowl", "$69", "https://soundergolf.com/products/sounder-x-yeti-dog-bowl",
   "Our pick for the bag. A limited Yeti bowl that holds eight cups, in double-wall stainless with a non-slip base. Sounder&rsquo;s line: &ldquo;There is a near-perfect correlation between the quality of a golf club in the UK and that club&rsquo;s attitude to dogs.&rdquo;"),
 "d11": ("The Worthy Dog", "Golf Bag Toy", "$20.25", "https://theworthydog.com/products/golf-bag-toy-5485",
   "A tough plush golf bag with a rugged outer layer, made for rough play."),
 "d12": ("CocoTherapy", "Golf Champ Toy Set", "$44.96", "https://cocotherapy.com/products/golf-champ-toy-set",
   "A plush bag with a club, a tee and two balls, and every piece squeaks. For gentle chewers only."),
 "d14": ("A.P.C.", "Dog Waste Bag Holder", "$100", "https://www.apc-us.com/products/dog-waste-bag-holder-cohiz-m66088_iai",
   "Japanese denim with &ldquo;A.P.C. Toutou&rdquo; embroidered on it and a press-stud closure. The most expensive way to carry poop bags, and you will need poop bags."),
 "d16": ("Seamus Golf", "Seamus Lab Canvas Driver Cover", "$130", "https://www.seamusgolf.com/products/seamus-lab-head-covers-with-personalization",
   "Ivory canvas embroidered all over with Labs and lined in brown fleece, made &ldquo;to celebrate all the greenskeepers&rsquo; best friends.&rdquo; Seamus itself is named after the founders&rsquo; Irish Terrier."),
 "d17": ("Daphne&rsquo;s Headcovers", "Golden Retriever Driver Headcover", "$45.99", "https://www.daphnesheadcovers.com/products/golden-retriever",
   "Soft fur and floppy ears, fits a 460cc driver. Daphne&rsquo;s lists eighteen breeds, from Beagle to Australian Shepherd."),
 "d18": ("Daphne&rsquo;s Headcovers", "Black Lab Driver Headcover", "$45.99", "https://www.daphnesheadcovers.com/products/black-lab",
   "Shiny black fur and floppy ears. Add embroidery if you want your dog&rsquo;s name on it."),
 "d19": ("Daphne&rsquo;s Headcovers", "Doodle Driver Headcover", "$45.99", "https://www.daphnesheadcovers.com/products/doodle",
   "Soft amber fur, for doodle people."),
 "d20": ("Big Dog Golf Co.", "Dancing Dog Headcover", "$79", "https://bigdoggolfco.com/products/dancing-dog",
   "White leather embroidered with the brand&rsquo;s dancing dog logo, made in Australia."),
 "d21": ("Swag Golf", "Saints &ldquo;Gumbo&rdquo; 2.0 Driver Cover", "$99.99", "https://swag.golf/products/nfl-new-orleans-saints-gumbo-2-0-driver-cover",
   "Gumbo is the Saints&rsquo; dog mascot, and Swag made Gumbo a &ldquo;massive scruffy dog face&rdquo; with a fleur-de-lis on the forehead."),
 "d22": ("Pins &amp; Aces", "Man&rsquo;s Best Friend Polo, Light", "$69.95", "https://pinsandaces.com/products/mans-best-friend-light",
   "A small all-over dog print, made for the golfer whose golden retriever never misses a round."),
 "d23": ("Pins &amp; Aces", "Man&rsquo;s Best Friend Polo, Dark", "$69.95", "https://pinsandaces.com/products/mans-best-friend-dark",
   "The dark version, a nod &ldquo;to the four-legged sidekick who never judges your slice.&rdquo;"),
 "d24": ("Rhoback", "The Golf Dog Poly Hat", "$38", "https://rhoback.com/products/the-golf-dog-poly-solid-fleet-navy",
   "A navy performance hat with Rhoback&rsquo;s golf dog on the front."),
 "d25": ("Smathers &amp; Branson", "Yellow Lab Performance Hat", "$45", "https://smathersandbranson.com/products/yellow-lab-needlepoint-performance-hat-navy",
   "A hand-stitched needlepoint Lab on a light, sweat-wicking navy six-panel."),
 "d31": ("Old Faithful Golf Co.", "TRUSTY Caddy Golf Towel", "$40", "https://oldfaithfulgolf.com/products/old-faithful-trusty-caddy-golf-towel-copy-1",
   "A 22-by-44-inch caddy towel in white, navy and red, &ldquo;branded with Trusty, the Old Faithful mascot&rdquo;: a dog with a club in its mouth. Old Faithful is a small Canadian brand that went live in November 2024."),
 "d28": ("Old Faithful Golf Co.", "The Dancing TRUSTY Fairway Wood Headcover", "$75", "https://oldfaithfulgolf.com/products/dancing-trusty-fairway-wood-headcover",
   "Black pebbled synthetic leather covered in white Trustys, lined in burgundy sherpa. Made for your go-to fairway wood: &ldquo;Your &lsquo;old faithful&rsquo; has been good to you. Now return the favor.&rdquo;"),
 "d29": ("Old Faithful Golf Co.", "The Heritage TRUSTY Fairway Headcover", "$85", "https://oldfaithfulgolf.com/products/the-heritage-trusty-fairway-headcover-in-genuine-leather",
   "Tan cowhide embroidered with dancing Trustys in different colors, a cream sherpa lining and a club member patch on the back. Fits any fairway wood, 3 through 9."),
 "d30": ("Old Faithful Golf Co.", "The TRUSTY Corduroy Barrel Headcover", "$70&ndash;$75", "https://oldfaithfulgolf.com/products/the-trusty-corduroy-barrel-hybrid-headcover",
   "Green corduroy barrel cover with Trusty in white and a tight elastic band inside: &ldquo;the club ain&rsquo;t going anywhere.&rdquo; Hybrid $70, fairway wood $75."),
 "d32": ("Old Faithful Golf Co.", "The Old Faithful TRUSTY Golf Polo", "$105", "https://oldfaithfulgolf.com/products/the-old-faithful-trusty-golf-polo",
   "Burgundy with a small all-over Trusty print, a structured collar, four buttons and a club member patch on the sleeve. A limited run, and only XX-Large is left."),
 "d33": ("Old Faithful Golf Co.", "TRUSTY &lsquo;Golden&rsquo; Snapback Golf Hat", "$37", "https://oldfaithfulgolf.com/products/old-faithful-trusty-golden-golf-hat",
   "A black structured five-panel with Trusty embroidered in gold on the corner."),
 "d34": ("Old Faithful Golf Co.", "TRUSTY Rope Hat", "$40", "https://oldfaithfulgolf.com/products/old-faithful-trusty-rope-hat",
   "A structured rope hat with Trusty on the front, in black or navy. Both carry the club member tag."),
}
SECTIONS = [
 ("On the Dog", "on-the-dog", ["d1","d2","d3","d4","d7","d8","d9","d10"],
  "<strong>Collars, leads and bandanas &middot; $20&ndash;$85</strong>A leash is the rule almost everywhere dogs are welcome, so you may as well make it a good one."),
 ("In the Bag", "in-the-bag", ["d13","d11","d12","d14","d31"],
  "<strong>Bowls, toys and a towel &middot; $20&ndash;$100</strong>Water, something to chew in the cart barn, and the poop bags you will definitely need."),
 ("Dogs on Your Headcovers", "headcovers", ["d16","d28","d29","d30","d17","d18","d19","d20","d21"],
  "<strong>Nine covers &middot; $46&ndash;$130</strong>For the days your dog has to stay home."),
 ("Dogs on You", "on-you", ["d32","d22","d23","d33","d34","d24","d25"],
  "<strong>Polos and hats &middot; $37&ndash;$105</strong>Dog-print clothes from independent golf brands, including a polo covered in Old Faithful&rsquo;s mascot, Trusty."),
]
N = 29
PQ = {
 "on-the-dog": ("Everyone knows a tired dog is a good dog, and we get a lot of good dogs here.", "Mike Beaver, Indian Valley Golf Club, to Golf Digest"),
 "headcovers": ("The fact is, dogs can&rsquo;t cause as much trouble as how some people drive carts.", "Sandy Loeffler, The Links at Highlands Ranch, to Golf Digest"),
}
CAP = "Photography &middot; Sounder"
BANDS = {
 "in-the-bag": ("Dogs welcome", "Photos from Sounder, the English golf brand behind the dog bowl.",
   [("life-2","A chalkboard sign at a golf club reading Well behaved dogs welcome","&ldquo;Well behaved dogs welcome.&rdquo;"),
    ("life-3","A Sounder x Yeti dog bowl full of water on the grass","The Sounder x Yeti bowl, in use"),
    ("life-4","A dog drinking from a Sounder bowl on a golf course","Hydration break")]),
}
PROSE = 'style="max-width:760px;font-size:16px;line-height:1.7;margin:0 auto 24px;"'
ETQ_CSS = """<style>
.dog-etq{display:grid;grid-template-columns:1.15fr 1fr;gap:48px;align-items:start;max-width:1000px;margin:8px auto 0;text-align:left}
.dog-etq ol{margin:0;padding:0;list-style:none;counter-reset:e}
.dog-etq li{counter-increment:e;position:relative;padding:14px 0 14px 44px;border-bottom:1px solid rgba(20,20,20,.15);font-size:16px;line-height:1.6}
.dog-etq li:first-child{padding-top:0}
.dog-etq li:first-child::before{top:0}
.dog-etq li::before{content:counter(e,decimal-leading-zero);position:absolute;left:0;top:14px;font-family:var(--mono);font-size:12px;letter-spacing:.08em;opacity:.55}
.dog-etq li strong{display:block;margin-bottom:2px}
.dog-etq figure{margin:0}
.dog-etq img{width:100%;height:auto;display:block;border:1px solid #141414}
.dog-etq figcaption{font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;opacity:.6;margin-top:10px}
@media(max-width:760px){.dog-etq{grid-template-columns:1fr;gap:28px}}
</style>
"""
WHERE = """
<section class="products" style="margin-top:8px;">
  <div class="drop-tag grass">Where to Go</div>
  <h2 class="products-hdr" id="where">Where You Can Bring a Dog</h2>
  <p class="cat-kicker"><strong>Austin.</strong> The City of Austin&rsquo;s rules for Roy Kizer say it plainly: &ldquo;Dogs must be on a leash and under control.&rdquo; Golf Advisor reported in 2015 that every Austin muni allowed dogs, along with Delaware Springs in Burnet (&ldquo;scoop the poop, and keep them on a leash&rdquo;). Policies change, so call the pro shop before you load your dog in the car.</p>
  <p class="cat-kicker"><strong>Elsewhere in the US.</strong> Golf Digest has named Belgrade Lakes in Maine, Indian Valley in Marin County and Seaside in Oregon as dog-friendly. Plenty of others allow it quietly or with permission, and plenty don&rsquo;t at all. Ask first, every time.</p>
  <p class="cat-kicker"><strong>The UK and Ireland.</strong> Golf Digest says dogs are more likely to be welcome at old links with common walking ground than at newer inland clubs. The St Andrews Links are a public park with dogs on them every day, Cruden Bay is known for it, and Scotland&rsquo;s Outdoor Access Code asks walkers crossing a course to keep dogs on a short lead.</p>
</section>
"""
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag flag">The TGI Take</div>
    <p>We&rsquo;re all for dogs on the golf course. Not every course and not every round, but where they&rsquo;re allowed, bring your dog along. A walking round with a dog at your heel is about as good as golf gets: the pace slows down, nobody minds the bogey, and you stop staring at your phone between shots.</p>
    <p><strong>Be careful about it.</strong> A dog on the course is a guest, and so are you. Keep your dog on a leash, off the greens and out of the bunkers, pick up after them, and keep them quiet when someone&rsquo;s hitting. Start with a short loop on a quiet evening before you try eighteen together. If the club says no dogs, it&rsquo;s no dogs.</p>
    <p><strong>The British figured this out a long time ago.</strong> On the old links of the UK and Ireland dogs are part of the scenery. The Old Course at St Andrews closes on Sundays and turns into one of the biggest dog parks in the world, and Sunningdale&rsquo;s club historian says overseas visitors are surprised by how many dogs they see. In the US it&rsquo;s rarer, but closer than you think: Austin&rsquo;s own city courses allow leashed dogs.</p>
    <p><strong>The best golf dogs belong to the greenskeepers.</strong> Every good course seems to have one riding in the maintenance cart: Blu, the pit mix who chases geese for the grounds crew at Detroit Golf Club; Lucky, Lefty and Charlie, the goose dogs at Pebble Beach; Rio, the superintendent&rsquo;s Lab at King&rsquo;s Deer in Colorado. Golf Digest put it simply: most courses allow only one dog, the superintendent&rsquo;s. Give a wave on the way past.</p>
    <p>Below: the etiquette, 29 pieces of golf dog gear (from a $20 bandana to a $130 headcover embroidered with Labs), and where you can bring a dog. Everything was in stock when we checked on October 22, 2026.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Short Version</div>
      <div class="sidebar-detail"><span class="l">Our stance</span><span>Bring your dog</span></div>
      <div class="sidebar-detail"><span class="l">The rule</span><span>Leash on, off the greens</span></div>
      <div class="sidebar-detail"><span class="l">In Austin</span><span>City courses allow leashed dogs</span></div>
      <div class="sidebar-detail"><span class="l">Gear</span><span>29 picks, $20&ndash;$130</span></div>
      <div class="hashtags">
        <span class="hashtag">#GolfDogs</span>
        <span class="hashtag">#WalkingGolf</span>
        <span class="hashtag">#MuniGolf</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>

<section class="products" style="margin-top:8px;">
  <div class="drop-tag grass">Etiquette</div>
  <h2 class="products-hdr" id="etiquette">How to Bring a Dog Golfing</h2>
  <div class="dog-etq">
    <ol>
      <li><strong>Ask first.</strong> Check the course policy, and if you&rsquo;re a guest, ask your host or the pro shop.</li>
      <li><strong>Leash on.</strong> &ldquo;On a leash and under control&rdquo; is the standard almost everywhere.</li>
      <li><strong>Off the greens, tees and bunkers.</strong> Paw prints in a bunker are your job to rake.</li>
      <li><strong>Carry bags, and use them.</strong> No exceptions.</li>
      <li><strong>Quiet on the shot.</strong> The best golf dogs sit when someone&rsquo;s swinging.</li>
      <li><strong>Walk, don&rsquo;t ride.</strong> A dog tied up in a moving cart is a bad idea.</li>
      <li><strong>Start small.</strong> Trainer Jonathan Klein&rsquo;s advice is to treat the first two or three rounds as training.</li>
      <li><strong>Bring water.</strong> Especially in Texas.</li>
    </ol>
    <figure>
      <img src="/images/ny-trip/sedgewood-stella.jpg" alt="Lenny Harrington putting at the Sedgewood Club with Stella, a golden mixed lab, sitting on the green" width="800" height="1000" loading="lazy" />
      <figcaption>Lenny and Stella, holding the green at the Sedgewood Club</figcaption>
    </figure>
  </div>
</section>
"""
FAQ = [
 ("Can you bring a dog on a golf course?", "Some courses allow it, usually on a leash, off the greens and tees, and with the owner cleaning up. Always check the course policy first. Many UK and Irish links courses welcome dogs; in the US it is rarer."),
 ("Are dogs allowed on Austin golf courses?", "The City of Austin's rules for Roy Kizer Golf Course say dogs must be on a leash and under control. Check with each course's pro shop before you go, as policies can change."),
 ("Can you take a dog on the Old Course at St Andrews?", "The Old Course closes to golf on Sundays and the public, dogs included, can walk it. Pick up after your dog and stay off the greens."),
 ("What should a dog wear on the golf course?", "A secure collar and a leash, plus a bandana or cooling layer in heat. Bring water and a bowl, and waste bags."),
]
_LB = []
_figs = ""
LOOKBOOK = ""
_FRN1 = {k: [f"/images/dogs-golf/p-{k[1:]}.jpg"] for k in P}
# extra frames per product (Lenny, 23 Oct 2026: "need more images in each products box"); research/extra-images/frame_extras.py
_EX = json.loads((ROOT / "research/extra-images/dogs-golf/frames.json").read_text())
FRN = {k: v + _EX.get(k[1:], []) for k, v in _FRN1.items()}
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-R3-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items, pos = [], 1
    for sec in SECTIONS:
        for h in sec[2]:
            items.append({"@type": "ListItem", "position": pos, "url": P[h][3], "name": H.unescape(f"{P[h][0]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-10-22", "dateModified": "2026-10-22",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": items},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Field Notes", "item": "https://thegrassyissue.com/#feed"},
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
  <a href="/#feed">Field Notes</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>The Grassy Issue &middot; Dogs on the course</span><span class="dot"></span>
    <span>29 picks &middot; prices checked October 22, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A dog sitting on a golf course fairway with a lead on, from Sounder&rsquo;s photos" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
    body += LOOKBOOK
    body += WHERE
    body += faq_html()
    out = head_top() + head_rest.replace("</head>", GRID_CSS + ETQ_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Kalamunda", "Parmore", "Casualist", "BUNX", "Long Iron", "Dim Sum", "Rowena", "Metalwood", "Climber", "Woodgrain", "Rookline", "Bethpage", "LBB", "GolfPass"):
        if leak in above: bad.append("leak " + leak)
    if fin.count('class="product-card"') != N: bad.append("card count")
    if re.search(r"\bworth\b", re.sub(r"\bFort\s+Worth\b", " ", re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<script\b.*?</script>", " ", above))), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
