#!/usr/bin/env python3
"""build-vest-edit.py — The Vest Edit, 2 November 2026. Cloned from build-fall-colorways.py.
Lenny: "Vest edit sounds good, let's use the best options and really pull from fresh brands that we've featured" (I pick).
Picks: 24 vests from 19 brands already in the TGI index, swept from ~80 featured-brand Shopify stores via the browser Nov 2 2026.
Prices as each store presents them to a US visitor (Sounder, No Return Club, Alba, Cph/Golf, Macade, Galvin Green show USD);
Angus & Grace in AUD (x0.70), Late Nine in SEK (x0.10). Copy from each product page's own description. Photos: each brand's own.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Best Golf Vests for Men: 36 Picks for Fall 2026"
DESC = ("The 36 best golf vests for men this fall from 30 independent brands: fleece and sherpa from Jones Sports Co, Sugarloaf and Fella, "
        "padded vests from Sounder and ANTi Country Club Tokyo, wind vests from Sentinel and SLOAT, and sweater vests from Devereux and J.Press.")
H1 = "The Vest Edit: 36 Golf Vests for Fall"
BC = "The Vest Edit"
SLUG = "the-vest-edit-2026"
IMG = "/images/vest-edit"
SHOP = ""
U = lambda d, h: f"https://{d}/products/{h}"
P = {
 "2": ("Jones Sports Co", "Fleece Vest, Pageant Blue/Loden Green", "$178", U("jonessportsco.com","fleece-vest-pageant-blue-loden-green"),
   "A 250 GSM recycled fleece body in pageant blue with loden green woven overlays across the chest pocket and lower back. Warm without the bulk."),
 "30": ("Metalwood Studio", "Trail Mix Reversible Vest, Dijon", "$218", U("metalwood.studio","trail-mix-reversible-vest-dijon"),
   "Deep brown one way, dijon the other, so it is two vests on one hanger. Metalwood&rsquo;s own product page calls it one of the best things they have made."),
 "41": ("Sounder", "Himalayas Overhead Gilet, Oat", "$130 (sale; $212)", U("soundergolf.com","himalayas-fleece-jacket-in-oat"),
   "Lightweight Italian polar fleece in oat that pulls on overhead, with a half-zip and a deep kangaroo pocket. Named for the Himalayas putting course at St Andrews."),
 "57": ("Students Golf", "Turner Sherpa Vest, Hunter", "$120", U("studentsgolf.com","turner-sherpa-zip-vest"),
   "Heavyweight sherpa in hunter green with a big exposed plastic zip, kangaroo pockets and Students embroidered across the back."),
 "22": ("Angus &amp; Grace Go Golfing", "Men&rsquo;s Reversible Fleece Vest, Olive", "360 AUD (~$252)", U("angusandgracegogolfing.com","mens-reversible-fleece-vest"),
   "Olive shell one way, cream fleece the other, with a two-way zip, two zipped waterproof pockets, a high collar and an elastic hem. From Australia."),
 "14": ("Macade", "ArcWeave Gilet, Ashwood", "$195", U("macadegolf.com","arcweave-gilet-ashwood"),
   "A textured cotton-wool blend in warm brown, cut clean and structured so it adds warmth without getting in the way of the swing."),
 "0": ("Eastside Golf", "Black Utility Vest", "$148", U("eastsidegolf.com","el2021401-000-black-utility-vest"),
   "Lightweight nylon with a V-neck, a stack of storage pockets, a purple lining and a gel patch. The most useful vest here if you walk and carry."),
 "8": ("Devereux Golf", "Wayne Vest, Black", "$128", U("devereuxgolf.com","wayne-vest-black"),
   "Devereux&rsquo;s cotton canvas workwear vest: full zip front, Western back yoke and a metal Devereux plate at the back neck."),
 "15": ("We Hit Fairways", "Fairway Stripe Vest, Shadow Black", "$185", U("wehitfairways.com","fairway-stripe-vest-shadow-black"),
   "A slim black puffer with a diagonal green stripe across the chest, cut in a comfort fit that layers easily over a polo."),
 "40": ("Sounder", "Low Light Gilet, Rust", "$103 (sale; $171)", U("soundergolf.com","low-light-gilet-in-rust"),
   "A Sounder bestseller redone in lightweight Japanese showerproof nylon, with a two-way zip, deep front pockets and a zipped chest pocket."),
 "27": ("Puttwell", "Puttwell Tech Vest, Black", "$90", U("puttwellgolfclub.com","puttwell-tech-vest"),
   "A quilted black vest with a snap front and the Puttwell wordmark on the chest. The least expensive padded vest in the edit."),
 "5": ("Alba Golf", "Glen Padded Vest, Salmon", "$446", U("albagolf.it","glen-padded-vest-in-salmon"),
   "Soft polyester microfiber with an internal coating for wind and water resistance, in a salmon you will not see on anyone else. The splurge, from Italy."),
 "1": ("Masterpiece Sports Club", "Proformance Tech Lite Vest", "$148", U("masterpiecegolf.com","proformance-tech-lite-vest"),
   "A khaki and olive color-block with chevron quilting front and back, from the brand&rsquo;s Evergreen collection."),
 "9": ("Jones Sports Co", "Windblocker Vest, Wheat", "$168", U("jonessportsco.com","windblocker-vest-wheat"),
   "Lightweight crinkle nylon with four-way stretch and a brushed mesh lining. The wheat color sits right against brown November grass."),
 "12": ("Sugarloaf Social Club", "SSC Tech Vest, Teal", "$115", U("sugarloafsocialclub.com","tech-vest-2026"),
   "Zip pockets and the SSC arrow on the back, in six colors from teal to Hidden Gem Yellow. Sugarloaf calls it maybe their favorite piece: golfable, and fine on Wall Street too."),
 "13": ("SLOAT", "Organic Ventile Vest, Charcoal", "$345", U("sloat.cc","mens-ventile-vest"),
   "Organic Ventile cotton sewn in Portugal, naturally resistant to wind and light rain. Stand collar, two-way YKK zip and zippered hand pockets."),
 "3": ("No Return Club", "Crinkled Soft Shell Vest, Ice Blue", "$103", U("noreturnclub.co.uk","crinkled-shell-vest"),
   "Crinkled nylon outside and grid fleece inside, made for the cold rounds you play anyway. From the UK, priced in dollars for US visitors."),
 "10": ("Galvin Green", "Lamar Vest, Navy", "$279", U("galvingreen.com","lamar-windproof-and-water-repellent-golf-vest-navy"),
   "A windproof, water-repellent shell over thin recycled Thermore padding, from the Swedish weather specialists. The most technical vest here."),
 "21": ("Devereux Golf", "Highly Addictive Sweater Vest", "$94", U("devereuxgolf.com","highly-addictive-sweater-vest"),
   "A mid-heavy knit in charcoal and white pinstripes with a V-neck, cut slightly oversized. Final sale, so check the size chart."),
 "32": ("Students Golf", "Cimarron Knit Vest Sweater", "$120", U("studentsgolf.com","cimarron-knit-vest-sweater-2"),
   "Sixty percent wool, forty percent mohair, in a brown and cream pattern with an embroidered logo on the chest."),
 "33": ("Ghost Golf", "Patrons Sweater Vest, White", "$80", U("ghostgolf.com","patrons-sweater-vest"),
   "Fine-gauge viscose knit with green tipping and Ghost Golf script across the chest. Old tennis-sweater energy for the course."),
 "52": ("Puttwell", "Gilligan Vest, Deep Green", "$90", U("puttwellgolfclub.com","gilligan-vest"),
   "A soft mid-weight cotton blend with a ribbed V-neck and hem. Put it over a white polo and you are done."),
 "59": ("Late Nine", "Ribbed Knit Vest, Sage", "2,450 kr (~$245)", U("late-nine.com","ribbed-vest-sage"),
   "Ultra-fine first-shearing merino, lightly brushed, in a fine rib. From Stockholm; sage was down to a couple of sizes when we checked."),
 "43": ("Cph/Golf", "Side Quilt Knit Vest, Black", "$107", U("captainshelmgolf.com","chg25-aw-j05-black"),
   "A 12-gauge knit front with quilted sides, a double-rib hem and NOT A GOLF GENTLEMAN in jacquard across the back."),
 "s16": ("Sugarloaf Social Club", "Sherpa Fleece Vest, Copper", "$105 at Badlands", "https://badlands1st.com/products/sugarloaf-social-club-sherpa-fleece-vest-copper",
   "A high-pile fleece that Sugarloaf says feels like your &rsquo;90s vest, in copper with red trim or cream. Sold out on Sugarloaf&rsquo;s own site; Badlands still had both colors."),
 "s29": ("Fella Golf", "Reversible Bodywarmer, Golf Cart Fleece", "$189", U("fellagolf.com","reversible-bodywarmer-fleece-golfcart-pattern"),
   "Sherpa fleece printed all over with golf carts on one side, a clean water-resistant forest green shell on the other. The most fun vest in the post."),
 "s50": ("Juniper &amp; James", "Ribbed Fleece Vest, Weathervane", "$129", U("juniperjamesgolf.com","ribbed-fleece-vest-weathervane"),
   "A ribbed natural-fiber blend fleece with hidden chest and hip pockets, from the New Braunfels brand started by the founder of Duck Camp."),
 "s4": ("ANTi Country Club Tokyo", "Down Vest, Black Check", "$328", U("anticountryclubtokyo.com","anti-country-club-down-vest-black-check"),
   "A wool check shell over real down, with a nylon hood tucked into the collar and the script logo across the back. From Tokyo, priced in dollars for US visitors."),
 "s59": ("Left of Field Golf", "Audley Padded Golf Vest, Sage", "138 AUD (~$97)", U("lofgolf.com","audley-padded-golf-vest-sage"),
   "Textured nylon with a wavy quilt stitch in sage. The Sydney brand calls it the most beautiful garment they have made, and the photos back that up."),
 "s125": ("STITCH", "Player Puffer Vest, Midnight", "$178", U("stitchgolf.com","player-puffer-vest"),
   "A quilted puffer in midnight navy or onyx with a leather tab at the back neck. Clean enough for a members&rsquo; club, warm enough for a December muni."),
 "sen": ("Sentinel Golf", "Cordura Vest, Light Gray", "$278", "https://www.sentinelgolf.us/shop/p/8t95uvw1ec28h1za76ycshtzy2kvha-57hyk-8trkf-6g8w5-b2y36-gykk4-kmx3l-ys7ma-mhtfh",
   "Japanese stretch Cordura that is water repellent, windproof and breathable, with Birdseye mesh inside, Japanese snaps and a waterproof YKK zip. Cut and sewn in New York; stocked in small runs."),
 "s0": ("Ashworth Golf Company", "Aeroflex Vest, Asphalt", "$145", U("ashworth-golf.com","aeroflex-vest-golfman-asphalt"),
   "A four-way stretch softshell with a DWR finish and the Golfman logo at the back yoke. Comes in four colors."),
 "s81": ("Pluto Golf", "Tri-Tone Vest, Bermuda", "$99", U("pluto.golf","tri-tone-vest-bermuda"),
   "Three greens spliced together: a light puffer block across the middle for core warmth, performance polyester above and below. Snap pockets at the hem."),
 "pd": ("Public Drip", "AKASHI-KAMA x Public Drip Swing Vest, Sharkskin", "$140", U("publicdrip.com","swing-vest-sharkskin"),
   "Public Drip&rsquo;s signature swing vest, remade with the menswear brand AKASHI-KAMA in a heathered Japanese fabric. Warm brown with burgundy rib trim at the neck and arms."),
 "s90": ("Rebolf", "Cream Club Vest", "$92", U("rebolf.com","cream-club-vest"),
   "A cream sweater vest with the Rebolf script on the chest and ribbed edges. From Barcelona; also comes in navy."),
 "s151": ("J.Press", "Made-in-Scotland Grey Fair Isle Sweater Vest", "$295", U("jpress.com","made-in-scotland-fair-isle-vest"),
   "One hundred percent wool, knit in Scotland in the Fair Isle pattern from the Shetland Islands. From the Ivy League clothier founded next to Yale in 1902."),
}
SECTIONS = [
 ("Fleece &amp; Texture", "fleece", ["30","2","41","57","s16","22","s29","14","s50"],
  "<strong>The warm ones</strong>Fleece, sherpa and a brushed cotton-wool. These are the vests for a 45-degree first tee, worn over a quarter-zip or a hoodie. Earth tones across the board: brown, dijon, oat, hunter, olive."),
 ("Padded, Quilted &amp; Canvas", "padded", ["0","8","15","s4","40","s125","27","s59","5"],
  "<strong>Core warmth, free arms</strong>Light padding or a heavy canvas that keeps your chest warm and leaves your shoulders alone. Wear one over a polo in the morning and you will not need to take it off at the turn."),
 ("Tech &amp; Wind", "tech", ["1","sen","9","12","s0","13","3","s81","10"],
  "<strong>For the breezy days</strong>Thin shells built to stop wind and shrug off a light drizzle. They pack small, so one can live in the bag from October to March."),
 ("Knit &amp; Sweater Vests", "knit", ["21","pd","32","33","s90","52","59","s151","43"],
  "<strong>The clubhouse ones</strong>The sweater vest is back, and it is the most golf thing you can wear. Pinstripes, mohair, tennis tipping and fine merino. Put it over a collared polo and keep the trousers simple."),
]
N = 36
PAIRS = {}
BANDS = {
 "tech": ("Into the wind", "Teal, navy and charcoal shells, from Sugarloaf Social Club, Galvin Green and SLOAT.",
   [("band-1-1","A man in a Sugarloaf Social Club teal tech vest indoors","Sugarloaf Social Club"),
    ("band-1-2","A close look at the Galvin Green Lamar navy vest","Galvin Green"),
    ("band-1-3","A man in a SLOAT charcoal Ventile vest","SLOAT")]),
 "knit": ("Layered up", "Pinstripes, canvas and merino, from Devereux and Late Nine.",
   [("band-2-1","A man in a Devereux pinstripe sweater vest","Devereux Golf"),
    ("band-2-2","The back yoke of a Devereux black canvas Wayne vest","Devereux Golf"),
    ("band-2-3","A man in a Late Nine sage ribbed knit vest over a polo","Late Nine")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>The vest is the most useful layer in golf. It keeps your chest warm and leaves your arms alone, so nothing pulls across your shoulders on the backswing. In Austin it covers most of November through February on its own. Everywhere else, it goes over a quarter-zip or a hoodie for the first nine and stays on.</p>
    <p><strong>Why these brands.</strong> We went through the online stores of nearly every brand in our index, around 170 of them, and found well over two hundred vests in stock. We kept the 36 we liked best, with no more than two from any one brand. That means names you know from our Brand to Know pages, like Jones Sports Co, Sounder, SLOAT, Sentinel and Late Nine, alongside brands we have only mentioned in passing, like Fella, Pluto and ANTi Country Club Tokyo.</p>
    <p><strong>Four kinds of vest.</strong> Fleece and sherpa are the warmest and the most casual. Padded and quilted vests give you core warmth with almost no bulk. Tech and wind vests are thin shells for breezy days that fold into a bag pocket. Sweater vests are the clubhouse option, and they are having a moment again.</p>
    <p><strong>How to wear one.</strong> A vest should be a little shorter than whatever is under it, so a polo or a quarter-zip hem shows below. Go darker on the vest than the layer underneath, and match the vest to your trousers or your hat, not both. A brown fleece over a cream polo with khakis is the simplest outfit in this post.</p>
    <p><strong>What to spend.</strong> The range runs from $80 to $446. Under $130 gets you a great sweater vest, a quilted vest or a sale Sounder gilet. The money goes up for fabric: Ventile cotton, first-shearing merino, technical padding. If you only buy one, buy the fleece or the padded vest; they get the most rounds.</p>
    <p><strong>What is in here.</strong> 36 vests from @@NB@@ independent brands, all in stock when we checked on November 2, 2026. Prices are what each store shows a US visitor; Angus &amp; Grace and Left of Field are listed in Australian dollars and Late Nine in Swedish kronor, with rough dollar figures beside them.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Details</div>
      <div class="sidebar-detail"><span class="l">Vests</span><span>36</span></div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>@@NB@@</span></div>
      <div class="sidebar-detail"><span class="l">Categories</span><span>4</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$80&ndash;$446</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Metalwood Trail Mix Reversible Vest</span></div>
      <div class="hashtags">
        <span class="hashtag">#GolfVest</span>
        <span class="hashtag">#FallGolf</span>
        <span class="hashtag">#GolfStyle</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
CLOSE = """
<section class="products" style="margin-top:8px;padding-top:48px">
  <div class="writeup-body" style="max-width:720px;margin:0 auto">
    <div class="drop-tag grass">The Last Word</div>
    <h2 class="products-hdr" id="last-word">One Vest, All Winter</h2>
    <p>Most golfers only need one vest. The trick is buying the right one for the rounds you actually play, then wearing it every week until March. Here is how we would choose.</p>
    <p><strong>Start with your coldest regular tee time.</strong> If you play early and your hands are numb on the first tee, buy fleece or sherpa; it is the warmest thing in this post. If you walk and carry, a padded or quilted vest keeps your core warm without making you sweat by the fourth hole. If cold is not the problem and wind is, a thin shell does more than any amount of padding. And if you mostly care how it looks at lunch afterward, get the sweater vest.</p>
    <p><strong>Dress by the thermometer.</strong> These are the combinations we would wear, from mild to miserable:</p>
    <p style="line-height:2"><strong>55&deg; and up:</strong> a knit or a wind vest over a polo. Nothing else.<br>
      <strong>45&deg; to 55&deg;:</strong> a padded vest over a long-sleeve polo or a light quarter-zip.<br>
      <strong>35&deg; to 45&deg;:</strong> fleece or sherpa over a quarter-zip, a beanie in the bag.<br>
      <strong>Below 35&deg;:</strong> a thin base layer, a hoodie, then a wind vest on top to keep the warmth in. Or stay home and watch the replay.</p>
    <p><strong>Get the fit right.</strong> A vest should close over whatever you plan to wear under it without pulling across the chest, and the armholes should be roomy enough that your shoulders turn freely. Try it on over your thickest quarter-zip and make a few practice swings in the mirror. If it rides up at the back at the top of your backswing, size up; Sentinel gives the same advice for its Cordura vest.</p>
    <p><strong>If you buy two.</strong> Pair one warm vest with one thin one: a fleece and a wind shell, or a padded vest and a sweater vest. Between them you are covered from the first cold snap in November to the windy spring rounds in March, and the thin one packs into the bag for the days the forecast is wrong.</p>
    <p><strong>Take care of it.</strong> Wash fleece and sherpa inside out on cold and let them air dry, or the pile mats. Down and padded vests go in on a gentle cycle and come out of the dryer on low with a couple of tennis balls to keep the fill from clumping. Hand-wash or dry-clean wool and mohair knits, and always check the care label first; a good vest should last you a lot of winters.</p>
    <p>For what to wear underneath, see our <a href="/drops/fall-golf-colorways-2026">fall golf colorways</a> and <a href="/drops/the-fall-hoodie-edit-2026">the fall hoodie edit</a>.</p>
  </div>
</section>
"""
HERO_ALT = "Three photos side by side: a golfer in a Macade brown ArcWeave gilet on the course, a man in a SLOAT charcoal Ventile vest, and a man in a Devereux black canvas Wayne vest"
FRN = json.loads((ROOT / "research/vest-edit-2/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-VE-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
def card(k, idx):
    brand, item, price, url, copy = P[k]
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
         "url": URL, "image": og, "datePublished": "2026-11-02", "dateModified": "2026-11-02",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
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


def swatch(k):
    a, ha, b, hb = PAIRS[k]
    cell = 'flex:1;padding:26px 18px 20px;font-family:var(--mono,monospace);font-size:11px;letter-spacing:.14em;text-transform:uppercase;line-height:1.7'
    return (f'  <div style="display:flex;max-width:620px;margin:6px auto 22px;border:1px solid rgba(20,20,20,.2)">'
            f'<div style="{cell};background:{ha};color:{hb}"><strong>{a}</strong><br>{ha}</div>'
            f'<div style="{cell};background:{hb};color:{ha}"><strong>{b}</strong><br>{hb}</div></div>\n')


def section(sec, n0):
    h2, anchor, ids, kicker = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} picks</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n' +
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def lookbooks():
    figs = "\n".join(f'  <figure><img src="{IMG}/life-{n}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>' for n, alt, cap in LIFE)
    return (f'\n<section class="products" style="margin-top:8px;">\n  <div class="drop-tag grass">{len(LIFE)} photos</div>\n'
            f'  <h2 class="products-hdr" id="lookbooks">From the Lookbooks and In the Wild</h2>\n'
            f'  <p class="cat-kicker"><strong>The pairings on people</strong>Every photo here is the brand&rsquo;s own, from its lookbook, its store or its feed. Royal blue to forest green, in the order above.</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


def main(apply_):
    ids = [k for s in SECTIONS for k in s[2]]
    assert len(ids) == N == len(set(ids)) and set(ids) == set(P), (len(ids), set(P) ^ set(ids))
    for s in SECTIONS: assert len(s[2]) == 9, s[0]
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
    <span>The Edit &middot; Four kinds of vest, 30 brands</span><span class="dot"></span>
    <span>36 picks &middot; in stock, checked November 2, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="{HERO_ALT}" fetchpriority="high" /></div></div>
"""
    body += TAKE.replace("@@NB@@", str(len({P[k][0] for s_ in SECTIONS for k in s_[2]})))
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        o, n = section(s, n); body += o
    body += CLOSE
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Mackem", "hex code", "pairing"):
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
