#!/usr/bin/env python3
"""build-metalwood-fw26.py — Metalwood Studio FW26 collection post, 16 October 2026.
Lenny: "we need to do a post about the new metalwood collection- https://metalwood.studio/", then "Let's do the full first
collection and include lookbook images also. Give it a good TGI take on where the brand is heading and recent design ideas".
FACTS (research/metalwood-fall): Shopify catalogue (all 36 FW26 Pt 1 styles, prices + stock 16 Oct; released 10.11 and 10.14),
Metalwood's lookbook blog (FW26 Pt 1, 16 Oct, credits verbatim; earlier 2026 collab lookbooks), product copy quoted verbatim
(clean lines only). Background from TGI's own Brand to Know (June 2026, revisited August). No outside press on FW26 yet.
PHOTOS: Metalwood's own product photos and FW26 Pt 1 lookbook (research/metalwood-fall/frame.py).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Metalwood Studio FW26: Western Yokes, a Faux-Leather Parka and a Goalie Jersey for Golf"
DESC = ("Metalwood Studio's Fall/Winter 2026 collection, all 36 styles from Part 1 with the lookbook: western track jackets, "
        "the Oasis parka, a padded Goalie Jersey, a reversible tee and Trophy pants. Where Cole Young's LA brand is heading next.")
H1 = "Metalwood Studio FW26 &mdash; The Whole First Drop, Plus the Lookbook"
BC = "Metalwood Studio FW26"
SLUG = "metalwood-studio-fw26-collection"
IMG = "/images/metalwood-fw26"
PK = json.loads((ROOT / "research/metalwood-fall/picks.json").read_text())
SOLD = set()
NAME = {d["key"]: H.escape(d["title"]) for d in PK}
COL = {d["key"]: [c.split(" (")[0] for c in d["colors"]] for d in PK}
def price(d):
    return f"${d['price']:,.0f}"
COPY = {
 "raglansleeveblouson": "The top of the range and the piece we&rsquo;d buy first: a cotton-poly blouson with raglan sleeves, a western back yoke and a concealed button closure over a full zip. Metalwood calls it &ldquo;the butteriest jacket we&rsquo;ve made to date.&rdquo; Tan or steel.",
 "oasisparka": "A hooded polyester parka with a faux-leather finish, custom woven pull tabs and water resistance. Black or ruby. The ruby is the loudest thing in the collection, and the lookbook knows it.",
 "cottontwillparka": "Metalwood put drawstrings on the hood, the waist and the hem of this 100% cotton twill parka, plus two snap pockets at the waist and a woven patch on the chest. Stone only.",
 "contrastzipwindbreaker": "Metalwood makes this oversized brown windbreaker with a mesh lining and a contrast-taped nylon coil zip. Per Metalwood, you could spill an espresso all over yourself and be fine.",
 "westernyolktrackjacket": "A track jacket with western yokes front and back, cut from the same stretch fabric as the Pleated Western Track Pant, with the new circular M badge in silicone at the back neck. Brown or black.",
 "ssvneckwindbreaker": "A short-sleeve V-neck windbreaker with a sublimated print all over and a mesh lining. Metalwood&rsquo;s copy says you have to zoom in to see the blades in the print.",
 "trailmixreversiblevest": "Metalwood made this polyester vest reversible, with one side quilted. Metalwood calls it &ldquo;one of the sickest things we&rsquo;ve ever made.&rdquo; One size left in ice.",
 "frankensteinbuttonupsh": "Metalwood stitched this raglan shirt together from a brown and pink check body and contrasting sleeves, with a hidden placket, a flat hem and a chest pocket. The patchwork piece of the season.",
 "mwplacebuttonupshirt": "Metalwood prints the MW Place graphic on the chest of this boxy blue and white stripe button-up, with custom buttons. It pairs with the matching tee and snapback.",
 "longsleevebuttonupshir": "This one is a plain pine check cotton button-up, and even Metalwood&rsquo;s copy admits it is just a nice shirt.",
 "goaliejersey": "Metalwood cut a soccer-goalie jersey in polyester, with padded sleeves and a big 94 on the back. The tagline is &ldquo;Golf is a contact sport.&rdquo; Blue or emerald.",
 "kingofthegreensjersey": "Metalwood prints &ldquo;King of the Green&rdquo; script and SOS Repair Center graphics on this black poly-cotton jersey. One size is left.",
 "pipedlongsleevequarter": "This is the collection&rsquo;s only polo, with long sleeves, mesh piping throughout and a hidden zip placket. Even Metalwood sounds surprised to be making one. Tan or navy.",
 "surftop": "Metalwood runs poly-mesh tape across the chest and sleeves of this cotton-poly crew, in gray or green. The product copy points out that Rory wears baggy pants now.",
 "contraststitchmockneck": "A mock-neck sweatshirt with contrast cover stitching all over and a smeared &ldquo;Metalwood Studio&rdquo; print. Navy or gray.",
 "mountaineercrewneckswe": "Metalwood makes this navy crew with an overdyed vintage wash and a mountain-range logo embroidered on the chest.",
 "dualfacetshirt": "Metalwood makes this tee reversible, with cotton on one side, polyester on the other and contrast ribbing. In Metalwood&rsquo;s words, &ldquo;just when you thought it was one t-shirt&rdquo; it&rsquo;s two. Berry or bone.",
 "heavyweightminimetallo": "The basic, done heavy: an oversized, boxy, cropped cotton tee with the small woven Metalwood patch. Marine, white or tar.",
 "skidmarktshirt": "Metalwood prints a smeared Metalwood Studio graphic on cotton. The copy points at the men&rsquo;s room at Los Feliz Par-3, the LA muni. White or blue.",
 "prescriptiontshirt": "Metalwood prints a grid of golf-ball &ldquo;pills&rdquo; on the chest. Per Metalwood, in college a lost sleeve of balls was a whole prescription. White or navy.",
 "mwplacetshirt": "Metalwood prints the MW Place logo with a red cursor arrow on cotton, in dark purple, white or black. The copy calls the swing &ldquo;so smooth they call me the Silk Road.&rdquo;",
 "creaturetshirt": "Metalwood makes this paneled cotton tee with a sporty Metalwood Studio wordmark, gray with charcoal panels or dark green with yellow. Erin Murray wears the green one in the lookbook.",
 "fliestshirt": "A traditional-fit white tee with the Metalwood script logo, and the cheapest shirt in the drop.",
 "pleatedwesterntrackpan": "Metalwood gave this straight-leg track pant a permanent pleat and a drawstring waist, in the same stretch fabric as the western track jacket. Metalwood says it tested them on a plane. Brown or black.",
 "creaturepant": "Metalwood makes this stretch nylon pant with paneled accents, a snap closure and a Velcro back pocket. The copy is about a ball marker in your pocket. Pewter or black.",
 "trophypant": "Metalwood cut the Trophy pleated and straight legged, with the custom metal belt-loop charm, a back flap pocket and an inside drawstring. Metalwood calls it &ldquo;our greatest fitting pant.&rdquo; Black or brown, a few sizes left.",
 "bustershort": "Metalwood cuts these oversized cotton shorts with contrast stitching and the metal belt-loop charm. Metalwood calls them the &ldquo;buffest shorts you&rsquo;ve ever seen.&rdquo; Olive or black.",
 "myseriousshort": "A pinstripe short in poly-cotton with satin-lined legs, cut oversized. Brown or graphite.",
 "trophyshort": "Metalwood also makes the Trophy as a pleated cotton short with the metal charm. Per Metalwood, it fits like the billowy shorts in photos of Tiger at college. Black, olive or plaid, few sizes left.",
 "igolfdadhat": "A cotton dad hat with &ldquo;iGolf&rdquo; embroidered in an early-internet logo, which Metalwood says took months to finish. White, black or woodland camo.",
 "bomberdadhat": "Metalwood makes this cotton dad hat with a shark mouth embroidered on the brim, in steel or white.",
 "carlsbaddadhat": "Metalwood makes this nylon dad hat with an embroidered logo, in tan, white or black. Carlsbad is Cole Young&rsquo;s hometown.",
 "cadethat": "Metalwood puts a frayed self-fabric patch on the front of this cotton cadet cap. Black or fatigue green.",
 "mwplacesnapbackhat": "Metalwood puts the MW Place graphic on a cotton snapback, brown or black, to match the shirt and tee.",
 "protipsnapbackhat": "Metalwood makes this black five-panel cotton snapback with its wordmark on the front.",
 "metallogosunglassesstr": "An $8 neoprene sunglasses strap in spruce with the Metalwood logo, and the cheapest thing in the drop.",
}
for _k in COPY: assert _k in NAME, _k
P = {d["key"]: ("Metalwood Studio", NAME[d["key"]], price(d), "https://metalwood.studio/products/" + d["handles"][0], COPY[d["key"]]) for d in PK}
G = {d["group"] for d in PK}
def keys(g): return [d["key"] for d in PK if d["group"] == g]
ORDER = {"outerwear": keys("Outerwear"), "shirts": keys("Shirts, Jerseys & Polos"), "sweats": keys("Sweatshirts"),
         "tees": keys("T-Shirts"), "bottoms": keys("Pants & Shorts"), "hats": keys("Hats & Accessories")}
SEC = [
 ("outerwear", "Outerwear", "<strong>Six jackets and a vest</strong>Outerwear is the biggest category in the drop: two parkas, two windbreakers, a western track jacket, the blouson and a reversible vest, from $188 to $298."),
 ("shirts", "Shirts, Jerseys and the One Polo", "<strong>Seven tops</strong>This is where the sports-jersey idea lives, alongside three button-ups and the season&rsquo;s only polo."),
 ("sweats", "Sweatshirts", "<strong>Two sweatshirts</strong>One has a mock neck and contrast stitching; the other is overdyed with a vintage wash."),
 ("tees", "T-Shirts", "<strong>Seven tees</strong>Most of the golf references in the drop are on the graphic tees, from $54 to $72, plus the reversible Dual Face at $138."),
 ("bottoms", "Pants and Shorts", "<strong>Six bottoms</strong>The cuts get bigger again this season, and the custom metal belt-loop charm shows up on the Trophy and Buster styles."),
 ("hats", "Hats and the Strap", "<strong>Six hats and a strap</strong>Most of the hats are $48."),
]
SECTIONS = [(h2, a, ORDER[a], k) for a, h2, k in SEC]
N = sum(len(v) for v in ORDER.values())
DATE = "2026-10-16"
PQ = {
 "butter": ("I know I say this a lot, but this is definitely the butteriest jacket we&rsquo;ve made to date.", "Metalwood Studio, on the Raglan Sleeve Blouson"),
 "shirts": ("Golf is a contact sport. You&rsquo;re just not playing it correctly.", "Metalwood Studio, on the Goalie Jersey"),
 "tees": ("So just when you thought it was one t-shirt. Boom. It&rsquo;s two t-shirts.", "Metalwood Studio, on the Dual Face T-Shirt"),
 "bottoms": ("You know those pics of college Tiger wearing the billowy shorts? That&rsquo;s how these fit.", "Metalwood Studio, on the Trophy Short"),
}
LB = "FW26 Pt 1 lookbook"
BANDS = {
 "look": ("The FW26 Pt 1 Lookbook &middot; Metalwood&rsquo;s own photos",
  "Metalwood published the lookbook on October 16, starring Malcolm Amin and Erin Murray, shot by Ryan Thomas Murray and Chase Thompson in Los Angeles. Nine of our favorites are below, and more run between the sections.",
  [("lb-01", "A man in the steel Raglan Sleeve Blouson tipping a white Bomber Dad Hat", "Raglan Sleeve Blouson, steel"),
   ("lb-05", "A man in the brown Western Yolk Track Jacket, stripe shirt and olive Buster Shorts", "Western Yolk Track Jacket"),
   ("lb-08", "A man in the tan Raglan Sleeve Blouson over the MW Place T-Shirt", "Blouson over the MW Place tee"),
   ("lb-09", "A woman in the green and yellow Creature T-Shirt with black shorts", "Creature T-Shirt"),
   ("lb-11", "A man seen from behind in the SS V-Neck Windbreaker and gray pants", "SS V-Neck Windbreaker"),
   ("lb-21", "A man in a gray striped tee with contrast ribbing", "The Dual Face tee"),
   ("lb-22", "A shirtless man pulling on the blue Goalie Jersey", "Goalie Jersey, blue"),
   ("lb-23", "A man seen from behind in the blue Goalie Jersey with 94 on the back and black shorts", "The 94 on the back"),
   ("lb-02", "The steel Raglan Sleeve Blouson hung on a wooden chair", "Blouson on a chair")]),
 "outerwear": ("Outerwear in the lookbook", "Here are both colors of the faux-leather Oasis parka, black and ruby.",
  [("lb-03", "A man in the black Oasis Parka with the hood up, flashing a peace sign, in black and white", "Oasis Parka, black"),
   ("lb-04", "The black Oasis Parka laid flat, showing its faux-leather sheen", "Oasis Parka, up close"),
   ("lb-18", "The ruby Oasis Parka hanging on a hanger against a white door", "Oasis Parka, ruby")]),
 "shirts": ("Shirts in the lookbook", "The patchwork Frankenstein shirt and the piped quarter-zip polo both show up here.",
  [("lb-27", "A man buttoning the patchwork Frankenstein Button Up Shirt", "Frankenstein Button Up"),
   ("lb-12", "A man in a blue short-sleeve top and black shorts, side view", "Short sleeves, long shorts"),
   ("lb-31", "A man in the tan Piped Longsleeve Quarter Zip Polo and pinstripe trousers", "Piped quarter-zip polo")]),
 "sweats": ("Sweatshirts and the Surf Top in the lookbook", "The lookbook shows off the contrast stitching and striped tape.",
  [("lb-13", "A man seen from behind in a charcoal sweatshirt with contrast stitching", "Contrast stitching"),
   ("lb-19", "A gray Surf Top with blue tape across the chest, folded", "Surf Top, gray"),
   ("lb-28", "A woman in the green Surf Top and a camo iGolf hat", "Surf Top, green")]),
 "tees": ("Tees in the lookbook", "The graphic tees get layered over long sleeves.",
  [("lb-20", "A man in a gray long-sleeve top and brown shorts", "Layered"),
   ("lb-30", "A man in a tan tee over a camo long sleeve, with black pants and a dark cap", "Tee over thermal"),
   ("lb-16", "A close-up of a red top over pinstripe trousers with a Metalwood studio waistband", "The waistband")]),
 "bottoms": ("Pants and shorts in the lookbook", "The shorts are big and the trousers are pleated.",
  [("lb-06", "A pair of olive Buster Shorts hanging alone on a chrome clothes rail", "Buster Shorts on the rail"),
   ("lb-14", "Folded pinstripe trousers with a metal belt-loop charm", "Pinstripe and the metal charm"),
   ("lb-07", "Olive trousers with contrast stitching under a cream jacket with drawstring hem", "Contrast stitch")]),
 "hats": ("Hats in the lookbook", "The cadet cap and dad hats finish the looks.",
  [("lb-26", "A man seen from behind in a tan cadet cap and the brown Western Yolk Track Jacket with the circular M badge", "Cadet Hat and the new M badge"),
   ("lb-25", "A man in the brown Contrast Zip Windbreaker and black pants standing against a white wall", "Full look"),
   ("lb-24", "A man in a black hooded jacket and gray pants, looking down", "Hood up")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>When we profiled Metalwood in June, it ran on medieval heraldry and &rsquo;90s tour polos. FW26 shows Cole Young building something bigger than a golf brand: out of 36 styles, one is a polo and seven are outerwear. There is a padded goalie jersey with a 94 on the back, a reversible tee and a faux-leather parka in ruby red. Golf still shows up in the graphics, like the iGolf hat and a tee about lost sleeves of balls, but the clothes are cut for the rest of the week.</p>
    <p>Three design ideas run through it. Western yokes on the track jacket and blouson. Soccer-jersey details: mesh, piping, padding and big numbers. And hardware, from a custom metal belt-loop charm to a circular M badge and a rounded wordmark that looks like a 2000s kit sponsor. The fits keep getting bigger; Metalwood says the Trophy Short is cut like the billowy shorts Tiger wore in college.</p>
    <p>Where is it heading? 2026 has been the collab year, from the adidas MC70 and Predator Sala to a G.H. Bass Sportocasin shot in Tokyo. FW26 follows that lead: a fashion collection with a golf accent, not golf apparel with a fashion edge. Outerwear now runs $188 to $298, and the &ldquo;Pt 1&rdquo; on the lookbook says more is coming.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Collection</span><span>Fall/Winter 2026, Part 1</span></div>
      <div class="sidebar-detail"><span class="l">Released</span><span>October 11 and 14, 2026</span></div>
      <div class="sidebar-detail"><span class="l">Founder</span><span>Cole Young</span></div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Los Angeles</span></div>
      <div class="sidebar-detail"><span class="l">Styles</span><span>36, in 65 colorways</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$8&ndash;$298</span></div>
      <div class="sidebar-detail"><span class="l">Lookbook</span><span>Ryan Thomas Murray &amp; Chase Thompson</span></div>
      <a href="https://metalwood.studio/" target="_blank" rel="noopener" class="sidebar-cta">Shop Metalwood &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#Metalwood</span>
        <span class="hashtag">#FW26</span>
        <span class="hashtag">#GolfFashion</span>
        <span class="hashtag">#NewCollection</span>
      </div>
      <p style="font-size:13px;line-height:1.55;margin-top:14px;opacity:.8">The brand&rsquo;s backstory is in our <a href="/drops/brand-to-know-metalwood-studio" style="border-bottom:1px solid currentColor">Metalwood Brand to Know</a>.</p>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
SPEC = [("Western yokes", "Front and back on the Western Yolk Track Jacket, across the back of the Raglan Sleeve Blouson"),
        ("Faux leather", "The Oasis Parka: water-resistant polyester with a faux-leather finish, in black or ruby"),
        ("The metal charm", "A custom metal belt-loop charm on the Trophy pant and short and the Buster Short"),
        ("Jersey details", "Padded sleeves on the Goalie Jersey, mesh piping on the polo, mesh tape on the Surf Top"),
        ("Two-in-one", "The Dual Face tee reverses, cotton one side and polyester the other; the Trail Mix vest flips too"),
        ("The marks", "A circular M badge, a rounded sporty wordmark and the MW Place logo with a red cursor")]
def explainer():
    cells = "".join(f'<div style="padding:18px 16px;border:.5px solid rgba(20,20,20,.2)"><div style="font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--grass);margin-bottom:6px">{a}</div><div style="font-size:15px;line-height:1.5">{b}</div></div>' for a, b in SPEC)
    return f"""
<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr" id="design-notes">Design Notes</h2>
  <p class="cat-kicker"><strong>What&rsquo;s new this season</strong>These are the six details we kept noticing across the drop, and several of them feel new for Metalwood.</p>
  <div class="mg-spec" style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;max-width:980px;margin:0 auto">{cells}</div>
</section>
"""
FAQ = [
 ("When did Metalwood FW26 come out?", "Metalwood released Fall/Winter 2026 Part 1 in two drops, on October 11 and October 14, 2026, and published the FW26 Pt 1 lookbook on October 16."),
 ("How much is Metalwood FW26?", "On October 16, 2026, tees were $54 to $72 (the reversible Dual Face tee is $138), hats $42 to $48, shirts and jerseys $148 to $198, pants and shorts $148 to $208, and outerwear $188 to $298. A sunglasses strap is $8."),
 ("How many pieces are in the collection?", "Part 1 has 36 styles in 65 colorways: seven outerwear pieces, seven shirts and jerseys, two sweatshirts, seven tees, six pants and shorts, six hats and a sunglasses strap."),
 ("Who shot the Metalwood FW26 lookbook?", "Ryan Thomas Murray and Chase Thompson, in Los Angeles, starring Malcolm Amin and Erin Murray."),
 ("Where can I buy Metalwood FW26?", "Online at metalwood.studio, where some of the first-drop pieces were already down to their last sizes, and at Metalwood's store on La Brea Avenue in Los Angeles."),
 ("Is there a Metalwood FW26 Part 2?", "The lookbook is titled Pt 1, which points to a second release, but Metalwood had not announced dates as of October 16, 2026."),
 ("How does Metalwood fit?", "Big. Many FW26 pieces are labeled oversized or boxy, the Trophy Short is cut long and loose, and the Heavyweight tee is boxy and cropped. Most product pages include a size chart."),
]
FRN = json.loads((ROOT / "research/metalwood-fall/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-GT-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}'
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
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>October 16, 2026</span><span class="dot"></span>
    <span>Los Angeles &middot; Fall/Winter 2026</span><span class="dot"></span>
    <span>36 styles &middot; prices checked October 16, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/btk-hero.jpg" alt="From the Metalwood FW26 Pt 1 lookbook: a man in the steel Raglan Sleeve Blouson tipping the brim of a white Bomber Dad Hat with a shark mouth on it" fetchpriority="high" /></div></div>
"""
    body += TAKE
    body += pq("butter")
    body += band("look")
    body += explainer()
    n = 1
    for s in SECTIONS:
        body += band(s[1])
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
    for leak in ("Mackem", "Kalamunda", "Howie", "No Dirt", "Lehi", "Rookline", "Hudson", "LBB", "GolfPass", "Woodgrain", "Parmore", "Lazyface", "Mount Tee", "Sunday Golf", "Loma", "Matchstick", "Gumtree", "Karsten", "Good Morning America", "Forbes", "Esquire", "Hypebeast", "Golf Digest", "Skratch", "Ad Age"):
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
