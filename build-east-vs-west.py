#!/usr/bin/env python3
"""build-east-vs-west.py — East Coast vs. West Coast: three matchups, six brands, 36 picks. 25 October 2026.
Lenny: "let's do a post of East Coast vs. West Coast brands - give me a list of 3 vs 3" -> two clothing brands and one accessory brand
per coast -> Whim Golf vs Metalwood (swapped in for Public Drip), Rookline vs SLOAT, Gumtree vs Jones Sports Co. Whim is NYC (83 Canal St).
Layout: two columns per matchup, WEST LEFT, EAST RIGHT (Lenny). No verdicts: it goes to Reddit for readers to decide. Mobile: West/East tabs.
FACTS: live stores 25 Oct 2026 (research/east-west/catalogue.json, meta.json); brand background from TGI's own published profiles
(Public Drip Revisited, Metalwood FW26, Rookline BTK, SLOAT BTK, Gumtree BTK, Jones Revisited). Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"
FRN = json.loads((ROOT / "research/east-west/frames.json").read_text())
META = json.loads((ROOT / "research/east-west/meta.json").read_text())

TITLE = "East Coast vs. West Coast Golf Brands: 3 Matchups, 36 Picks"
DESC = ("Metalwood vs. Whim, SLOAT vs. Rookline, Jones vs. Gumtree: six independent golf brands from both coasts, "
        "side by side. You decide who wins. Prices checked Oct. 25, 2026.")
H1 = "East Coast vs. West Coast: Three Golf Brand Matchups"
BC = "East Coast vs. West Coast"
SLUG = "east-coast-vs-west-coast-golf-brands"
IMG = "/images/east-vs-west"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"

# key: (item name as shown, copy)
P = {
 "wg1": ("Woven Merino Swing Jacket", "Woven in Connecticut from RWS-certified American merino and left undyed, so each jacket carries small dark flecks from the wool itself. A RiRi zip, a cinched hem and paneled shoulders built for an easy swing. At $499, it&rsquo;s the most expensive piece in the post."),
 "wg2": ("Chartreuse Embroidered Navy Merino Long Sleeve Golf Shirt", "Whim knits this long-sleeve polo from 100% American merino in a centuries-old Massachusetts mill, then finishes it in New York with horn buttons and a light green script. Mid-weight 6.5oz jersey, a standard fit and no synthetics."),
 "wg3": ("Sky Embroidered Slate Merino Long Sleeve Golf Shirt", "A lighter 4.5oz merino jersey, knit in South Carolina and made by hand in New York, with a sky blue script on the chest. It resists odor, and Whim makes it for year-round wear."),
 "wg4": ("Golf Short, Blue Stretch Nylon", "Whim cuts this short at a classic length and says it&rsquo;s &ldquo;not for the guys showing thigh.&rdquo; Water-resistant stretch nylon mesh, a snap and button closure, cut and sewn in New York. Only S and M are left."),
 "wg5": ("WHIM Reebok Classic", "Whim&rsquo;s take on Reebok&rsquo;s &rsquo;80s runner has a leather upper with suede at the toe and heel, a four-color Whim tongue label, a powder blue embossed heel and grass-print sock liners. It ships in custom Whim x Reebok packaging with two sets of laces."),
 "wg6": ("Sheep Hat in Woven Merino", "An adjustable cap in woven American merino from American Woolens, with a brass closure and a small embroidered sheep. The sheep is a nod to where every Whim shirt starts."),
 "mw1": ("Western Yolk Track Jacket, Brown", "Metalwood puts Western yokes front and back on this track jacket, in a polyester, cotton and spandex blend with a silicone patch at the neck. Wear it with the matching track pant for a full brown set."),
 "mw2": ("Pleated Western Track Pant, Brown", "This straight-leg track pant has a permanent pleat and a drawstring waist, in the same stretch blend as the jacket. Metalwood says it tested the pair on a plane and, for once, wasn&rsquo;t miserable."),
 "mw3": ("Piped Longsleeve Quarter Zip Polo, Tan", "Metalwood pipes this long-sleeve quarter-zip polo all over and hides the zip in the placket, in a light polyester mesh. It&rsquo;s the nearest thing to a tour polo in the fall line, and the tan reads more vintage soccer kit than country club."),
 "mw4": ("Contrast Stitch Mock Neck Sweatshirt, Navy", "A navy mock-neck sweatshirt in a poly-cotton blend with contrast cover-stitching throughout and a screen-printed detail. Metalwood&rsquo;s whole description, after the specs: &ldquo;Super wholesome.&rdquo;"),
 "mw5": ("Raglan Sleeve Blouson, Tan", "The blouson pairs raglan sleeves and a Western back yoke with a cotton lining and a concealed button closure over a full zip. Metalwood calls it the &ldquo;butteriest jacket we&rsquo;ve made to date,&rdquo; and it&rsquo;s the priciest piece on this side."),
 "mw6": ("King of the Greens Jersey, Black", "A soccer-style jersey in polyester and cotton with contrast panels and a screen-printed King of the Greens graphic. It shows where Metalwood is heading: fashion first, with golf in the graphics."),
 "rl1": ("Signature Blend Polo", "Cotton and cashmere in a long-sleeve polo you wear like a sweater. Rookline pitches it for a cool morning on the course and the fork and knife afterwards, and it&rsquo;s the first Rookline piece we&rsquo;d buy."),
 "rl2": ("Grid Fleece Windbreaker", "Cut from Japanese Stormfleece, a double weave with a fine wool pile inside, windproof and water-repellent. Chrome zips, a zipper shield, rubberized pulls and hidden drawcords. New this month, and the most technical thing Rookline makes."),
 "rl3": ("Ottoman Rib Cashmere Crew", "Rookline knits this crew from pure cashmere, with a fully fashioned saddle sleeve and an Ottoman rib at the elbow, cuff and hem. Rookline&rsquo;s argument for wearing it to golf: &ldquo;8:04 on a fall Sunday morning qualifies.&rdquo;"),
 "rl4": ("Hudson Quarter Zip", "This midweight quarter zip has a peached interior, moisture wicking, UV protection and a slightly tapered sleeve. Rookline built it for dewsweepers, and it stows in the bag once the sun is up."),
 "rl5": ("Brushed Twill Pivot Pant", "Japanese cotton twill with 3% spandex, cut between slim and wide. It moves through a full swing and holds its shape, and the brushed finish makes it feel more like a trouser than a golf pant."),
 "rl6": ("Yeoman&rsquo;s Performance Short", "A four-way-stretch micro dobby short with room through the seat and thigh, an 8.5-inch inseam and an inner waistband that keeps a polo tucked. Moisture-wicking, and cut for walking eighteen."),
 "sl1": ("Merino Polo", "200gsm RWS-certified merino jersey, sewn in Portugal, with a self-fabric collar, side vents and small sleeve embroidery. It regulates temperature and resists odor, which makes it the SLOAT piece for hot rounds."),
 "sl2": ("Organic Ventile Wind Shirt", "Organic Ventile, woven in Switzerland and sewn in Portugal, in a relaxed quarter zip with raglan sleeves. It handles wind and light rain over a polo, and it comes with SLOAT&rsquo;s lifetime repair guarantee."),
 "sl3": ("Organic Cotton Fleece Crewneck", "480gsm organic cotton fleece with a brushed interior, dropped shoulders and a concealed zip pocket. Heavy, soft and plain, with a small SLOAT patch on the chest."),
 "sl4": ("Organic Cotton Fleece Quarter Zip", "The same 480gsm organic fleece with a stand collar, a metal quarter zip and concealed side-entry zip pockets that keep a scorecard and tees put mid-round."),
 "sl5": ("Organic Cotton Caddie Pant", "A straight-fit 305gsm organic cotton pant inspired by the caddie&rsquo;s uniform, heavier than SLOAT&rsquo;s Day Pant and built to drape. You can walk eighteen in it and wear it to dinner."),
 "sl6": ("Organic Cotton Corduroy Short", "SLOAT cuts this short from fine-wale organic corduroy, with an elastic waist, a drawcord and a pressed front crease. SLOAT&rsquo;s FAQ makes the case that fine wale is light and tailored enough for golf."),
 "gt1": ("State Flower Headcover 2.0", "A driver cover in 16oz off-white canvas, each with a vintage patch hand-embroidered with a US state flower, cut from heirloom textiles made between the 1940s and the 1970s. Made in Manhattan, and every one is different."),
 "gt2": ("Archive Quilt Blade Putter Cover", "A blade putter cover cut from Gumtree&rsquo;s archive quilts, so the pattern changes from one cover to the next. The kind of cover people ask about on the first green."),
 "gt3": ("GUMTREE (COFFEE) Sack Headcover", "Gumtree cuts these covers from the jute sacks its raw coffee beans traveled to New York in before roasting. Each is one of a kind, in driver and fairway wood sizes, made in Manhattan."),
 "gt4": ("Vintage Floral Patchwork Quilt Valuables Pouch", "A zip pouch with a metal clip, cut from a 1950s&ndash;1970s American scrap quilt pieced from floral calico in red, navy, pink and cream. An edition of 40, handmade in New York City."),
 "gt5": ("GGNC x Samuel Falzone Italian Leather Card Holder", "One piece of Italian leather and no stitching, made by hand in New York by Samuel Falzone. A flap opening and a snap closure, in Negroni or black."),
 "gt6": ("Member Caddy Towel", "A white ribbed cotton caddy towel, about 44 by 22 inches, with embroidered GGNC logos in pink or olive. Gumtree promises one lucky bounce off a tree and one rare bird sighting per round."),
 "jn1": ("Trouper, Evergreen/Kodiak", "The 2026 Trouper stand bag from Jones&rsquo;s Heritage Collection, in deluxe vegan leather with a redesigned, reinforced stand and new ergonomic zippers. The most refined bag Jones makes, in green and brown."),
 "jn2": ("Original Jones Bag, Navy/Red/White", "The bag that started it all in 1971, still built for walkers: water-resistant nylon, a single retro strap, an unstructured body and three pockets. As plain now as it was then."),
 "jn3": ("Circa &rsquo;71 Headcover, Brown", "A barrel headcover with a microfleece outside and a sherpa lining, named for the year Jones started. At $45, it&rsquo;s the easiest way into the brand."),
 "jn4": ("Clubhouse Duffle, Ecru/Kodiak", "Jones makes this Heritage Collection duffle in distressed vegan leather, ecru with brown trim, and sizes it for the locker room or a weekend away."),
 "jn5": ("Mt. Hood Ball Marker", "A 1.25-inch marker with Mount Hood above the clouds, made for Jones by Matchstick Golf, the ball-marker studio across town in Portland."),
 "jn6": ("Tour Towel, Green", "An oversized ribbed terry towel with the arched Jones logo, big enough to keep one end wet and one end dry."),
}
SIDES = {
 "wg": ("East", "Whim Golf", "New York, NY", "/brands/whim-golf",
        "Colin Heaberg and Will Gisel met at Camp Dudley in 2006 and launched Whim in 2019, now working out of an office on Canal Street. Most of the line is American merino, knit in New England and South Carolina, then cut, sewn and embroidered in New York. This year it also took an installation to Milan Design Week.",
        "A man in a white Whim sheep cap and a navy quilted vest"),
 "mw": ("West", "Metalwood Studio", "Los Angeles, CA", "/brands/metalwood-studio",
        "Cole Young&rsquo;s Metalwood has grown from heraldry and &rsquo;90s tour polos into a fashion label with a golf accent. The fall line runs on Western yokes, soccer-jersey piping and roomy fits, and the product copy reads like a group chat.",
        "A Metalwood model in a dark jacket and white cap from the FW26 lookbook"),
 "rl": ("East", "Rookline", "Long Island, NY", "/brands/rookline",
        "Matt Dowling launched Rookline in late 2024, and the team are Long Island natives who have walked Bethpage Black dozens of times. Hudson is the performance line, Southside the crews and hoodies, and Hand &amp; Heritage is cotton and cashmere for a cold first tee.",
        "A golfer finishing his swing at sunset in Rookline"),
 "sl": ("West", "SLOAT", "San Francisco, CA", "/brands/sloat",
        "Named for Sloat Boulevard, which runs past the city&rsquo;s courses to Ocean Beach. Dan Fibiger and Teague Moriarty launched in August with natural fibers only: GOTS organic cotton, RWS merino and organic Ventile, sewn by family-run factories in Portugal.",
        "A golfer in a cream SLOAT quarter zip on a foggy course"),
 "gt": ("East", "Gumtree Golf &amp; Nature Club", "Brooklyn, NY", "/brands/gumtree-golf",
        "Karsten Jurkschat&rsquo;s Brooklyn studio makes headcovers and accessories in small runs, many from textiles that already had a life: old quilts, camp tents, the jute sacks its own coffee arrives in. When the fabric runs out, that design is gone, and 2% of every sale goes to carbon removal.",
        "A man in a striped Gumtree polo standing in front of a waterfall"),
 "jn": ("West", "Jones Sports Co", "Portland, OR", "/brands/jones-sports-co",
        "George Jones sewed the first Jones bags in his basement in 1971 and sold them out of the trunk of his taxi. The company still makes the light, unstructured carry bag for walkers, and the accessories share the same plain, sturdy look.",
        "Jones Circa &rsquo;71 headcovers on clubs in a bag on the course"),
}
MATCHUPS = [
 ("design", "Design Studios", "Metalwood Studio vs. Whim Golf", "wg", "mw",
  "Two labels that run like design studios and happen to make golf clothes. Los Angeles turns it up; New York keeps it quiet and natural."),
 ("played-in", "Clothes Made to Be Played In", "SLOAT vs. Rookline", "rl", "sl",
  "Both make clothes for a cold first tee and the dinner after, from opposite ends of the fabric shelf."),
 ("accessories", "The Accessory Makers", "Jones Sports Co vs. Gumtree", "gt", "jn",
  "One makes the bag; the other makes everything you hang on it."),
]
FAQ = [
 ("Which East Coast golf brands are in this matchup?", "Whim Golf from Manhattan, Gumtree Golf & Nature Club from Brooklyn and Rookline from Long Island, New York."),
 ("Which West Coast golf brands are in this matchup?", "Metalwood Studio from Los Angeles, SLOAT from San Francisco and Jones Sports Co from Portland, Oregon."),
 ("What is the difference between East Coast and West Coast golf style?", "In this matchup, the West Coast brands lean relaxed and loud, with roomy fits and pieces built for wind and fog, while the East Coast brands lean tailored and natural, with merino, cashmere and layers for short seasons and cold first tees."),
 ("How much do these golf brands cost?", "The 36 picks run from a $20 Jones ball marker to the $499 Whim Woven Merino Swing Jacket. Clothing starts at $80 for the Whim golf short."),
]


def card(k, idx):
    m = META[k]; item, copy = P[k]; fr = FRN[k]
    brand = SIDES[k[:2]][1]
    price = f"${m['price']:,.0f}"
    label = H.unescape(f"{brand} {item}").replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>'
                   for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>' for j in range(len(fr)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{brand}</div>'
            f'<div class="product-name">{item} &middot; {price}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="{m["url"]}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


EXTRA_CSS = ('<style>/*TGI-EW*/.ew-cols{display:grid;grid-template-columns:1fr 1fr;gap:0;margin-top:18px;border-top:.5px solid var(--ink)}'
             '.ew-col{padding:22px 22px 8px}.ew-col+.ew-col{border-left:.5px solid var(--ink)}'
             '.ew-coast{font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;opacity:.6}'
             '.ew-brand{font-family:var(--serif);font-size:30px;line-height:1.1;margin:6px 0 4px}.ew-brand a{border-bottom:none}'
             '.ew-city{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;margin-bottom:14px}'
             '.ew-head{width:100%;aspect-ratio:3/2;object-fit:cover;display:block;border:.5px solid var(--ink);background:#e8e2d6}'
             '.ew-about{font-size:15px;line-height:1.6;margin:14px 0 20px}'
             '.ew-col .products-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.ew-col .product-card{min-width:0}'
             '.ew-tabs,.ew-tabhint{display:none}.ew-call{border:.5px solid var(--ink);padding:26px 28px;max-width:760px;margin:10px auto 0;text-align:center;background:rgba(45,74,43,.06)}.ew-call p{margin:0;font-size:17px;line-height:1.6}'
             '.ew-toc{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin:0 auto 10px;max-width:900px}.ew-toc a{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;border:.5px solid var(--ink);padding:7px 12px}'
             '@media(max-width:900px){.ew-tabhint{display:block;text-align:center;font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;opacity:.65;margin:18px 0 -8px}.ew-tabs{display:flex;position:sticky;top:0;z-index:20;background:var(--paper);border:.5px solid var(--ink);margin-top:16px}'
             '.ew-tabs button{flex:1;padding:12px 6px;border:none;background:transparent;font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink);cursor:pointer}'
             '.ew-tabs button.on{background:var(--ink);color:var(--paper)}'
             '.ew-cols{display:block;border-top:none;margin-top:0}.ew-col{padding:18px 0 4px}.ew-col+.ew-col{border-left:none}'
             '.ew-cols[data-show="0"] .ew-col:nth-child(2),.ew-cols[data-show="1"] .ew-col:nth-child(1){display:none}'
             '.ew-brand{font-size:26px}.ew-head{aspect-ratio:16/9}.ew-about{font-size:14px;margin:12px 0 16px}'
             '.ew-col .products-grid{gap:12px}.ew-col .product-body{padding:10px 8px 12px}.ew-col .product-name{font-size:13px;line-height:1.3}.ew-col .product-desc{font-size:12.5px;line-height:1.5}}'
             '@media(max-width:340px){.ew-col .products-grid{grid-template-columns:1fr}}</style>\n')

INTRO = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The Idea</div>
    <p>The two coasts dress for golf differently, and the best independent brands on each side show it. New York labels build for short seasons, cold first tees and a round that ends on a subway platform. West Coast labels build for fog, wind and a game that barely stops for winter.</p>
    <p>So we put three of our favorites from each coast head to head: two clothing matchups and one for accessories. <a href="/brands/metalwood-studio">Metalwood Studio</a> against <a href="/brands/whim-golf">Whim Golf</a>, two labels that run like design studios. <a href="/brands/sloat">SLOAT</a> against <a href="/brands/rookline">Rookline</a> for clothes made to be played in. <a href="/brands/jones-sports-co">Jones Sports Co</a> against <a href="/brands/gumtree-golf">Gumtree Golf &amp; Nature Club</a> for the things you carry. Each brand gets six picks, with the West on the left and the East on the right. We&rsquo;ve left the verdicts to you.</p>
    <p>It&rsquo;s for the golfer who already knows which coast they dress like, and the one who wants a little of both. Every price and product was checked on the brands&rsquo; own stores on October 25, 2026.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Matchups</div>
      <div class="sidebar-detail"><span class="l">Matchups</span><span>3</span></div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>3 East, 3 West</span></div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>36</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$20&ndash;$499</span></div>
      <div class="sidebar-detail"><span class="l">Winner</span><span>Your call</span></div>
      <div class="sidebar-detail"><span class="l">Checked</span><span>October 25, 2026</span></div>
      <div class="hashtags">
        <span class="hashtag">#EastVsWest</span>
        <span class="hashtag">#IndependentGolf</span>
        <span class="hashtag">#TheEdit</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""


def column(key, n0):
    coast, brand, city, href, about, alt = SIDES[key]
    ids = [f"{key}{i}" for i in range(1, 7)]
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'<div class="ew-col"><div class="ew-coast">{coast} Coast</div>'
            f'<h3 class="ew-brand"><a href="{href}">{brand}</a></h3><div class="ew-city">{city}</div>'
            f'<img class="ew-head" src="{IMG}/head-{key}.jpg" alt="{alt}" loading="lazy" />'
            f'<p class="ew-about">{about}</p>'
            f'<div class="products-grid">\n{cards}\n</div></div>'), n0 + 6


def matchup(i, m, n0):
    anchor, label, title, e, w, kicker = m
    cw, n0 = column(w, n0); ce, n0 = column(e, n0)
    tabs = (f'<div class="ew-tabs" role="tablist"><button class="on" data-c="0" role="tab">West &middot; {SIDES[w][1]}</button>'
            f'<button data-c="1" role="tab">East &middot; {SIDES[e][1]}</button></div>')
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">Matchup {i} &middot; {label}</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{title}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'  <div class="ew-tabhint">Tap to see the other coast &darr;</div>\n  {tabs}\n  <div class="ew-cols" data-show="0">{cw}{ce}</div>\n</section>\n'), n0


TABS_JS = ("<script>document.querySelectorAll('.ew-tabs').forEach(function(t){var c=t.nextElementSibling;"
           "t.querySelectorAll('button').forEach(function(b){b.addEventListener('click',function(){"
           "t.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===b)});c.setAttribute('data-show',b.dataset.c);"
           "var y=t.getBoundingClientRect().top;if(y<0)t.scrollIntoView({block:'start'});});});});</script>\n")


def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>' for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items = [{"@type": "ListItem", "position": i, "url": META[k]["url"], "name": H.unescape(f"{SIDES[k[:2]][1]} {P[k][0]}")}
             for i, k in enumerate([f"{s}{n}" for m in MATCHUPS for s in (m[4], m[3]) for n in range(1, 7)], 1)]
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC, "url": URL, "image": og,
         "datePublished": "2026-10-25", "dateModified": "2026-10-25",
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


def main(apply_):
    keys = [f"{s}{n}" for m in MATCHUPS for s in (m[4], m[3]) for n in range(1, 7)]
    assert set(keys) == set(P) == set(META), set(P) ^ set(keys)
    for k in keys:
        assert FRN.get(k) and all((ROOT / f.lstrip("/")).is_file() for f in FRN[k]), k
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    toc = "".join(f'<a href="#{m[0]}">{m[2]}</a>' for m in MATCHUPS)
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>The Edit &middot; Three matchups &middot; Six brands</span><span class="dot"></span>
    <span>36 picks &middot; prices checked October 25, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="West and East side by side: two golfers mid-swing in the adidas x Metalwood collab at golden hour, with a palm tree and the Los Angeles hills behind them, and a golfer in a brown swing vest on a Brooklyn brownstone stoop with his bag" fetchpriority="high" /></div></div>
"""
    body += INTRO + f'\n<div class="ew-toc">{toc}</div>\n'
    n = 1
    for i, m in enumerate(MATCHUPS, 1):
        o, n = matchup(i, m, n); body += o
    body += faq_html()
    out = head_top() + head_rest.replace("</head>", EXTRA_CSS + "</head>", 1) + body + TABS_JS + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    if fin.count('class="product-card"') != 36: bad.append("card count")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<script\b.*?</script>", " ", above)), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides|brands)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
