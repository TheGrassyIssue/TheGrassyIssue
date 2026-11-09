"""build-gift-guide-2.py — 2026 Holiday Gift Guide, Part 2 of 3 (9 November 2026). Cloned from build-gift-guide-1.py.
Categories: Compliments Guaranteed / A Fresh New Colorway / The One They'd Never Buy Themselves. 12 each, 36 brands, none repeated from Part 1.
Lenny: the best options TGI talked about this year; his picks Parmore camo quarter-zip, Good Threads belt, SLOAT, Draw, Gumtree, Takomo irons.
FACTS: product pages, read November 9, 2026. Prices as shown to a US visitor.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"
TITLE = "The 2026 Golf Gift Guide, Part 2: Statement Pieces, Fresh Colorways and Gifts They'd Never Buy Themselves"
DESC = ("36 golf gifts from 36 independent brands, all from products we featured this year: pieces that get compliments, "
        "the best new colorways and the splurges people never buy for themselves, from $36 to $888.")
H1 = "The 2026 Golf Gift Guide, Part 2: Statement Pieces, Fresh Colorways and Gifts They&rsquo;d Never Buy Themselves"
BC = "Gift Guide 2026, Part 2"
SLUG = "golf-gift-guide-2026-statement-pieces-colorways-splurges"
IMG = "/images/gift-guide-2"
U = lambda d, h: f"https://{d}/products/{h}"
GIFTED = set()
P = {
 "mo": ("Mogshade", "Deco Headcover, Blue", "$112 driver", U("mogshadegolf.com","deco-blue-headcover"),
   "Part of Mogshade&rsquo;s Re.Weave collection: rescued fabric woven in Portugal&rsquo;s Serra da Estrela, lined in fleece. The Deco was our pick in <a href=\"/drops/loud-on-purpose-headcovers\">Loud on Purpose</a>, and it is the cover people pick up off the bag to look at."),
 "sx": ("Sherwood x Dormie", "Hockey Sock Fairway Headcover, Red", "$230", U("dormieworkshop.com","sherwood-x-dormie-hockey-sock-fairway-headcover-red"),
   "Real red Sherwood hockey socks rebuilt as a fairway barrel, with black and white leather stripes and a strip of clear patent leather on the diagonal like a fresh wrap of sock tape. Our favorite collab of the fall."),
 "gtc": ("Gumtree Golf &amp; Nature Club", "Tree Frog Green Camp Tent Headcover", "from $125", "https://www.gumtreegolfandnature.com/shop/p/tree-frog-green-camp-tent-headcover",
   "Cut from a 1970s Coleman waxed canvas tent found in Vermont, so each one carries its own stitching, wear and fifty years of patina. Driver or fairway. Only eight were left when we checked."),
 "stj": ("SLICE TOWN", "Golf Track Jacket, Cobalt", "$190", U("slice-town.com","track-jacket-cobalt"),
   "Cobalt nylon with a double front zip, a high collar and a golf ball print across the back. Designed in Copenhagen. Our pick from the <a href=\"/drops/brand-to-know-slice-town\">Slice Town Brand to Know</a>, and impossible to miss on the range."),
 "pm": ("Parmore", "Camo Quarter-Zip", "$65", U("parmoregolf.com","camo-1-4-zip-rebrand"),
   "Hunting-style camo in browns, tans and greens with a big white arched PARMORE across the chest. Parmore calls it the boldest piece in the range, and it is not wrong. S, M and XL left."),
 "or": ("Odd Ritual", "The Caddie Jacket, Navy", "R1,900 (~$105)", U("oddritualgolf.com","the-caddie-jacket-navy"),
   "Heavy 230gsm cotton twill with a washed cotton lining, a YKK zip and brass press studs at the cuffs and hem. Made locally in Cape Town, and it gets better the more it is worn."),
 "gt": ("Good Threads Needlepoint", "Golf Flags Needlepoint Belt, Navy", "$125", U("goodthreadsneedlepoint.com","golf-flags-needlepoint-belt-navy"),
   "Hand-stitched pearl cotton on 18-count canvas, finished with full-grain leather and a solid brass buckle. Each belt sold feeds a child at the Joan Rose Foundation two meals a day for two weeks."),
 "dr": ("Draw", "Forest Green Unstructured Corduroy Cap", "$58", U("drawgolf.co","forest-green-unstructured-corduroy-cap"),
   "Woven corduroy, a brushed silver buckle and a small pouch on the side that holds a tee. We featured it in <a href=\"/drops/hidden-details-golf-gear\">Hidden Details</a>, and it is still the cap we reach for."),
 "sl": ("SLOAT", "Organic Ventile Wind Shirt", "$295", U("sloat.cc","mens-ventile-wind-shirt"),
   "Organic Ventile cotton sewn in Portugal: light, breathable and naturally resistant to wind and light rain, with raglan sleeves for an easy swing. SLOAT backs every Ventile piece for life and will repair it if something goes wrong."),
 "pd": ("Public Drip x AKASHI-KAMA", "Swing Vest, Patchwork", "$140", U("publicdrip.com","swing-vest-patchwork"),
   "Public Drip&rsquo;s signature swing vest, remade with menswear brand AKASHI-KAMA in Japanese patchwork, with hidden button waist pockets. A limited run; M, L and XL were left when we checked."),
 "mgk": ("Manors Golf", "Recycled Greenskeeper Trouser", "$175", "https://www.manorsgolf.com/products/recycled-greenskeeper-trouser",
   "Four-way stretch, wind- and water-resistant recycled nylon with a drawcord waist, double pleats and eight pockets. One of them hides a small magnet for your ball marker; we only found it by wearing them."),
 "rg": ("Read The Green", "Back &rsquo;90s Windbreaker, Mallard", "$108", U("readthegreen.com","back-90s-windbreaker-mallard"),
   "Two-tone retro detailing and a relaxed cut, made in the spirit of &rsquo;90s golf and reimagined in New York. Our pick from <a href=\"/drops/brand-revisited-read-the-green\">Read The Green Revisited</a>."),
 "cn": ("Criquet", "Coach Nelson Players Shirt, Burnt Orange", "$128", U("criquetshirts.com","willie-nelson-performance-players-shirt-the-signature-burnt-orange"),
   "A tribute to Willie Nelson&rsquo;s Texas football roots and his friendship with Longhorns coach Darrell Royal, in a burnt orange any Austin golfer will recognize. Our pick from <a href=\"/drops/brand-revisited-criquet\">Criquet Revisited</a>."),
 "qs": ("Quiet Golf", "Vintage Supima Cotton Polo", "$118", U("quietgolf.com","vintage-supima-cotton-polo"),
   "Supima cotton with a little stretch, a three-button placket and a small embroidered logo, made in Portugal. Green, sky blue, butter yellow or brown, and quiet in every one of them."),
 "rb": ("Rookline", "Signature Blend Polo, Charcoal Heather", "$165", U("rookline.com","signature-blend-cotton-cashmere-polo-charcoal-heather"),
   "A long-sleeve polo in a cotton-cashmere blend, warm enough for a cold morning and smart enough for dinner after. Charcoal heather is the new color, and it suits winter golf."),
 "ri": ("Radmor", "Inness Knit Polo", "$101.50 (was $145)", U("radmorgolf.com","inness-knit-polo"),
   "Radmor&rsquo;s nod to the 3D-knit polos of the &rsquo;90s, in blues and white with a black collar and three-button placket. Our pick from the <a href=\"/drops/brand-to-know-radmor\">Radmor Brand to Know</a>, and on sale when we checked."),
 "pxg": ("Penta x Barnaby&rsquo;s", "PXB Grid Polo, Lush Ice", "$97", U("penta-golf.com","pentaxbarnabys-grid-polo-lush-ice"),
   "Penta&rsquo;s performance polo with Barnaby&rsquo;s, in a blue-to-black gradient grid. Same lightweight stretch fabric, new palette."),
 "mtp": ("Mount Tee Golf", "Parklands Waffle Polo, Eucalyptus Stripe", "A$110 (~$72)", U("mountteegolf.com.au","parklands-waffle-polo-eucalyptus-stripe"),
   "A 220gsm waffle polo from Melbourne in a eucalyptus-leaf stripe, breathable with a little weight to it. Our pick from the <a href=\"/drops/brand-to-know-mount-tee-golf\">Mount Tee Brand to Know</a>."),
 "ghp": ("Golden Hour Clubhouse", "Stripe Pique Polo, Red", "$69", U("goldenhourclubhouse.co.uk","stripe-pique-polo"),
   "100% cotton pique in a red and white stripe with a contrast collar and a relaxed fit. Bright enough to cheer up a grey December round. S and 2XL left."),
 "dvc": ("Devereux", "Camelback Polo, Brown/White Stripe", "$68", U("devereuxgolf.com","camelback-polo-brown-white-stripe"),
   "Brown and white stripes on a brushed pique with a contrast ribbed collar. It anchored our <a href=\"/drops/golf-capsule-wardrobe\">golf capsule wardrobe</a>."),
 "kf": ("Kingfisher Golf", "Sage Green DAL Cap", "$36", U("kingfisher-golf.com","sage-green-dal-cap"),
   "An unstructured natural canvas crown with a sage green bill and raised DAL embroidery, from Dallas. Our pick in <a href=\"/drops/fall-golf-colorways-2026\">Fall Colorways</a>."),
 "se": ("Sounder", "Eden Cotton-Cashmere Knit, Dark Navy", "$171", "https://soundergolf.com/en-us/products/eden-base-layer-with-pointelle-star-dark-navy",
   "A 14-gauge cotton and cashmere knit with raglan shoulders, thumbhole cuffs and a pointelle star on the back. Machine washable, which matters more than it should. Our pick from the <a href=\"/drops/brand-to-know-sounder\">Sounder Brand to Know</a>."),
 "fl": ("Macade", "Flow Light Knit Hoodie, Pine", "$245", U("macadegolf.com","flow-light-knit-hoodie-pine"),
   "A low-profile knit hoodie in a merino blend with a thermoregulating core that pulls moisture away and holds warmth. Pine is the color. Our pick from the <a href=\"/drops/brand-to-know-macade\">Macade Brand to Know</a>."),
 "dn": ("Students Golf", "Denali Stadium Jacket", "$280", U("studentsgolf.com","denali-stadium-jacket"),
   "A 100% wool stadium jacket with striped ribbing, snap buttons and a down-filled satin lining. Oversized with dropped shoulders. Our pick of the <a href=\"/drops/fall-drops-eastside-students-devereux\">fall drops</a>."),
 "fy": ("Fyfe x MacKenzie", "23rd Edition Carry Bag", "$888", U("fyfegolf.com","mackenzie-golf-bag-x-fyfe-23rd-edtion"),
   "Midnight black waxed canvas with tan leather on the grab loop, a cream suede strap, a tartan-lined pocket and a split cream-and-black base. The 24th Edition we featured sold out; this is the one still available."),
 "hlb": ("Hiroki Golf", "Luxury Leather Sunday Bag, Brown", "$340", U("hirokigolf.com","hiroki-luxury-leather-sunday-golf-bag-brown"),
   "Genuine leather with a waterproof lining, two large leather pockets, a firm leather base, a padded strap and a suede-lined 8-inch opening. A bag that gets better as it ages."),
 "tk3": ("Takomo Golf", "301 MB Forged Irons, 4-PW", "$649", U("takomogolf.com","iron-301-mb"),
   "A players&rsquo; muscle-back blade from Turku, Finland: soft forged feel, real workability and the kind of looks that make people ask what&rsquo;s in the bag. A full 4-iron to pitching wedge set, at a price most brands charge for half that."),
 "pn": ("Pinned Golf", "Prism+ Rangefinder", "$199.99 (was $259.99)", U("pinnedgolf.com","prism-rangefinder-black"),
   "Pinned&rsquo;s easiest rangefinder to use, in navy, red, black or white. Our pick from the <a href=\"/drops/brand-to-know-pinned-golf\">Pinned Brand to Know</a>, and $60 off when we checked."),
 "gl": ("Galvin Green", "Larry Half-Zip Windbreaker, Royal Blue", "$199", "https://www.galvingreen.com/products/larry-windproof-and-water-repellent-golf-jacket-royal-blue",
   "Lighter than a sleeve of golf balls: a windproof, water-repellent half-zip in a stretchy, breathable fabric. Our pick from the <a href=\"/drops/brand-to-know-galvin-green\">Galvin Green Brand to Know</a>."),
 "agv": ("Alba Golf", "Glen Padded Vest, Salmon", "$446", U("albagolf.it","glen-padded-vest-in-salmon"),
   "A padded microfiber vest from Italy with a coating inside for wind and water resistance, in a salmon nobody else in the group will be wearing."),
 "whs": ("Whim Golf", "Slate Merino Long Sleeve Golf Shirt", "$300", U("whimgolf.com","sky-embroidered-slate-merino-long-sleeve-golf-shirt"),
   "100% American merino, nothing synthetic, in a 4.5-ounce jersey with sky blue script on the chest. Our pick from the <a href=\"/drops/brand-to-know-whim-golf\">Whim Brand to Know</a>."),
 "sck": ("Siegelman Stable", "Cable Knit Sweater, Jet Black", "$278", U("siegelmanstable.com","cable-knit-sweater-1"),
   "A 100% cotton cable knit with the white embroidered Siegelman Stable logo on the chest. There are matching cable knit pants if you want to go all the way."),
 "sbt": ("Smathers &amp; Branson", "Golf Tee Pattern Needlepoint Belt", "$195", U("smathersandbranson.com","golf-tee-pattern-belt"),
   "100% hand-stitched needlepoint, lined in Italian leather with a solid brass buckle, delivered in a handmade wooden gift box. The box alone makes it a present."),
 "ks": ("Kraken Golf", "The Signet Stainless Steel Pitch Tool", "$109", U("krakengolf.com","the-signet-stainless-steel-pitch-tool"),
   "Stainless steel, modeled on the signet ring: a mark that says this belongs to me. It was a standout in <a href=\"/drops/7-divot-tools-actually-worth-carrying\">our divot tool roundup</a>."),
 "swm": ("Swell Marks", "Rise &amp; Grind Red Sun Ball Marker", "$65", U("swellmarks.com","red-sun"),
   "Stainless steel, laser colored and hand finished: a red sun and a breaking wave on one side, Rise and Grind on the other. For the dawn patrol. Our pick in <a href=\"/drops/around-the-greens-short-game-kit\">Around the Greens</a>."),
 "pa": ("Par&eacute; x Minted Greens", "Mahjong Set", "$350", U("pare.golf","pare-x-minted-greens-mahjong-set"),
   "144 tiles, a custom green table mat and a green leather briefcase, made for Par&eacute;&rsquo;s third anniversary and Filipino American History Month. For the night after the round. Dice not included."),
}
SECS = [
 ("compliments", "Compliments Guaranteed", "The pieces people ask about on the first tee", ["pd","stj","pm","sl","rg","or","mgk","sx","mo","gtc","dr","gt"],
  "Every golfer has one piece people ask about on the first tee, and this year we kept finding them. Public Drip rebuilt its swing vest with AKASHI-KAMA in Japanese patchwork. Slice Town&rsquo;s cobalt nylon track jacket has a golf ball print across the back, and Parmore&rsquo;s camo quarter-zip has a huge white wordmark across the chest. SLOAT&rsquo;s Ventile wind shirt is sewn in Portugal and backed for life, Read The Green&rsquo;s Back &rsquo;90s windbreaker is pure two-tone nostalgia, and Odd Ritual&rsquo;s caddie jacket comes from Cape Town. Manors&rsquo; Greenskeeper Trouser hides a magnet for your ball marker. On the bag: the Sherwood x Dormie hockey-sock cover, Mogshade&rsquo;s Deco and Gumtree&rsquo;s camp tent cover, cut from a 1970s tent, so no two match. Finish with Draw&rsquo;s corduroy cap, which hides a tee pouch, and a golf-flags needlepoint belt from Good Threads."),
 ("colorways", "A Fresh New Colorway", "The colors we kept coming back to this year", ["cn","ri","pxg","ghp","dvc","mtp","qs","rb","se","fl","dn","kf"],
  "A new colorway is the easiest gift to get right: you already know they like the thing, and now there is a version they don&rsquo;t have. These are the colors we kept coming back to this year. Criquet&rsquo;s Coach Nelson shirt in burnt orange, Radmor&rsquo;s 3D-knit Inness polo, Penta and Barnaby&rsquo;s gradient grid, Golden Hour&rsquo;s red stripe, Devereux&rsquo;s brown-and-white Camelback and Mount Tee&rsquo;s eucalyptus waffle. Quiet Golf&rsquo;s Supima polo is made in Portugal, and Rookline&rsquo;s cotton-cashmere long sleeve comes in charcoal heather. Then the layers: Sounder&rsquo;s Eden knit, Macade&rsquo;s merino hoodie in pine and Students&rsquo; wool Denali stadium jacket, topped with a sage green Kingfisher cap from Dallas."),
 ("never-buy-themselves", "The One They&rsquo;d Never Buy Themselves", "The splurges we featured this year", ["tk3","fy","hlb","pn","agv","whs","sck","gl","sbt","ks","swm","pa"],
  "Everyone has a list of things they would love and will never buy for themselves. These are the ones from our year: a set of Takomo&rsquo;s forged 301 MB blades from Finland, the Fyfe x MacKenzie carry bag and Hiroki&rsquo;s leather Sunday bag. Pinned&rsquo;s Prism+ rangefinder, Alba&rsquo;s padded Glen vest from Italy, Whim&rsquo;s 100% American merino, Siegelman Stable&rsquo;s cable knit and Galvin Green&rsquo;s featherweight Larry windbreaker. Then the small luxuries: Smathers &amp; Branson&rsquo;s hand-stitched golf-tee belt in a wooden gift box, Kraken&rsquo;s Signet pitch tool, Swell Marks&rsquo; Red Sun marker and, for the night after the round, Par&eacute;&rsquo;s mahjong set with Minted Greens."),
]
SECTIONS = [(s[1], s[0], s[3], s[2]) for s in SECS]
N = 36
PAIRS = {}
BANDS = {
 "never-buy-themselves": ("In the wild", "On people, on the course", [("life-a-1","A golfer in a cobalt Slice Town track suit in a shop","SLICE TOWN"),("life-a-2","A man in a patchwork Public Drip swing vest and cap","Public Drip x AKASHI-KAMA"),("life-a-3","A golfer in a blue knit Radmor polo on a tree-lined course","Radmor"),("life-a-4","A golfer in a red Golden Hour stripe polo holding an iron","Golden Hour Clubhouse"),("life-a-5","A golfer in a cap looking through a Pinned rangefinder","Pinned Golf"),("life-a-6","Swell Marks wave ball markers on the green","Swell Marks")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Part 2 of our three-part gift guide is built from our own year. Every gift here is something we featured on The Grassy Issue in 2026, and most of them were our pick in the post they came from: the Deco from Loud on Purpose, Radmor&rsquo;s Inness polo, Pinned&rsquo;s Prism+, Criquet&rsquo;s Coach Nelson shirt. Thirty-six gifts from 36 brands, and none of them appear in <a href=\"/drops/golf-gift-guide-2026-everyday-range-rat-stocking-stuffers\">Part 1</a>.</p>
    <p>This part is for the person who already has the basics. It covers the pieces that get noticed, the colorways that make an old favorite new again, and the splurges people talk themselves out of every year.</p>
    <p><strong>Where to start.</strong> For compliments, Public Drip&rsquo;s patchwork swing vest, $140. For a new colorway, Criquet&rsquo;s Coach Nelson shirt in burnt orange, $128. For the one they&rsquo;d never buy, Takomo&rsquo;s 301 MB irons, $649 for a forged 4-PW set.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Details</div>
      <div class="sidebar-detail"><span class="l">Gifts</span><span>36</span></div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>36</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$36&ndash;$888</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Takomo 301 MB Irons</span></div>
      <div class="hashtags">
        <span class="hashtag">#GolfGiftGuide</span>
        <span class="hashtag">#GolfGifts</span>
        <span class="hashtag">#IndieGolf</span>
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
    <h2 class="products-hdr" id="last-word">Give Them the One They Kept Looking At</h2>
    <p>The best gifts in this part are the ones somebody has already looked at twice. The patchwork vest they stopped to ask about, the cashmere they put back on the rack, the irons they keep watching videos of. A good gift closes that loop.</p>
    <p><strong>Check the details.</strong> A few of these run small or run out. The Gumtree tent covers and the Public Drip vest are limited, and the Parmore quarter-zip and Golden Hour polo are down to a few sizes. Takomo builds each set to your specs, so know their shaft and grip before you order, and Hiroki and Fyfe bags ship from overseas.</p>
    <p><strong>Order early.</strong> Several of these come from small brands with small runs, and December is when they sell through.</p>
    <p>Prices are as each store shows them to a US visitor. Odd Ritual shows rand and Mount Tee shows Australian dollars, so those dollar figures are approximate. Everything was in stock on November 9, 2026. Part 3 covers the last three categories.</p>
  </div>
</section>
"""
HERO_ALT = "Three gifts: green Gumtree headcovers cut from a vintage canvas tent, a brown leather Hiroki Sunday bag, and a Takomo 301 MB forged iron"
FRN = json.loads((ROOT / "research/gift-guide-2026/frames2.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-COL-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
GTAG = ' <span style="font-family:var(--mono,monospace);font-size:9px;letter-spacing:.1em;text-transform:uppercase;border:1px solid currentColor;padding:1px 5px;margin-left:6px;opacity:.7">Gifted</span>'
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
         "url": URL, "image": og, "datePublished": "2026-11-09", "dateModified": "2026-11-09",
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


CBY = {s[0]: s for s in SECS}
def section(sec, n0):
    h2, anchor, ids, kicker = sec
    s = CBY[anchor]
    num = [x[0] for x in SECS].index(anchor) + 1
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{num:02d} &middot; {len(ids)} gifts</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker"><strong>{kicker}</strong></p>\n'
            f'  <div class="writeup-body" style="max-width:720px;margin:0 auto 26px;"><p style="margin:0 0 16px;">{s[4]}</p></div>\n'
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
    <span>The Guide &middot; Holiday Gift Guide 2026, Part 2 of 3</span><span class="dot"></span>
    <span>36 gifts from 36 brands &middot; in stock, checked November 9, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="{HERO_ALT}" fetchpriority="high" /></div></div>
"""
    body += TAKE.replace("@@NB@@", str(len({P[k][0] for s_ in SECTIONS for k in s_[2]})))
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        o, n = section(s, n); body += o
    if "end" in BANDS: body += band("end")
    body += CLOSE
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Vest Edit", "Collab "):
        if leak in above: bad.append("leak " + leak)
    if fin.count('class="product-card"') != N: bad.append("card count")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", above), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file() and not (ROOT.parent / "held-gift-guide" / (href.split('/')[-1] + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
