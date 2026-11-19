#!/usr/bin/env python3
"""build-five-small-drops-nov.py — Five small, curated November drops, 19 November 2026. Replaces build-curated-drops-nov.py (six-small, never deployed).
Lenny: "I think it needs more lookbook images, and more details on the idea behind the designs" + "let's find more interesting, niche brands
with recent drops". After a wider sweep he picked: Mogshade x Incense Harbour + Fabricaal, Whim Storm suit, Local Rule FW26 tech (swapped in for Seamus, Lenny 11/19)
, Hendrikx (debut), Eastside Golf x Avirex. Edel, Miura and Piretti dropped (packshots only, thin stories).
Sources: brand product/collection/about pages (Mogshade, Whim, Seamus, Hendrikx, Eastside), PMQ listing (Incense Harbour), Seamus blog
(2015 Pendleton), Hypebeast (Hendrikx Nov 6; Eastside x Avirex Nov 12). Hendrikx campaign images from Hypebeast's article gallery; the
archival photo of Jochen Hendrikx from hendrikxgolf.com/en/about. EUR->USD at 1.0968 (ECB via frankfurter, 11/18/26).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Five Small Golf Drops From November: Mogshade, Whim, Local Rule, Hendrikx and Eastside \u00d7 Avirex"
DESC = ("Five small golf drops from November 2026 and the ideas behind them: Mogshade x Incense Harbour and Fabricaal, Whim's Schoeller Storm suit, "
        "Local Rule's FW26 rain layers, Hendrikx's Italian-made debut and Eastside Golf x Avirex.")
H1 = "Five Small Drops, November 2026"
BC = "Five Small Drops"
SLUG = "five-small-golf-drops-november-2026"
IMG = "/images/curated-drops"
U = lambda d, h: f"https://{d}/products/{h}"
HX = lambda h: f"https://hendrikxgolf.com/en/products/{h}"
P = {
 "g1": ("Mogshade &times; Incense Harbour", "Incense Harbour Headcover", "$64", U("mogshadegolf.com","incense-harbour-headcover"),
   "Driver, wood and hybrid covers in Japanese MacLowly water-repellent nylon, in mustard, dirty pink or grey green. A collaboration with the Hong Kong label Incense Harbour."),
 "g2": ("Mogshade &times; Incense Harbour", "Incense Harbour Tote Bag", "$51", U("mogshadegolf.com","incense-harbour-tote-bag"),
   "An oversized tote in the same water-repellent MacLowly nylon, in mustard, dirty pink or black."),
 "g3": ("Mogshade &times; Incense Harbour", "Incense Harbour Tool Tote Bag", "$89", U("mogshadegolf.com","incense-harbour-tool-tote-bag"),
   "A hunter green tool tote in MacLowly nylon with pockets around the outside. For the trunk, the cart or the range."),
 "g4": ("Mogshade &times; Incense Harbour", "Incense Harbour Fish Pouch", "$34", U("mogshadegolf.com","incense-harbour-fish-pouch"),
   "An upcycled pouch shaped like a fish, with buttons for eyes, a Portuguese wool lining and a zip. In dirty pink, grey green or navy."),
 "g5": ("Mogshade", "Only Human Course Case", "$96", U("mogshadegolf.com","only-human-course-case"),
   "Handmade from rescued wool woven in the Serra da Estrela mountains, with a pocket for ball markers, loops for tees, room for a rangefinder and a carabiner to clip it on."),
 "g6": ("Mogshade &times; Fabricaal", "Tear Glasses Case", "$46", U("mogshadegolf.com","tear-glasses-case"),
   "Hand-loomed merino from Fabricaal, one of only three original wool handicrafts still running in Europe, cut into a glasses case. The matching Tear and Zarape headcovers have already sold out."),
 "w1": ("Whim Golf", "Schoeller&reg; Nylon Storm Windbreaker, Clear Water Green", "$378", U("whimgolf.com","schoeller-nylon-storm-windbreaker-clear-water-green"),
   "Cut from Schoeller Dynamic, a Swiss stretch nylon: one dense weave, no laminate, no lining. Wind stays out, light rain beads off, and it breathes through a full round. Made in New York."),
 "w3": ("Whim Golf", "Schoeller&reg; Nylon Storm Windbreaker, Slate Grey", "$378", U("whimgolf.com","schoeller-nylon-storm-windbreaker-slate-grey"),
   "The same shell in slate grey, the quietest of the three colors. Wear it with the matching Storm Pant for the full suit."),
 "w4": ("Whim Golf", "Schoeller&reg; Nylon Storm Pant, Clear Water Green", "$378", U("whimgolf.com","schoeller-nylon-storm-pant-clear-water-green"),
   "The matching pant in the same Schoeller stretch nylon, made to move with every swing and breathe through eighteen. Made in New York."),
 "w5": ("Whim Golf", "Schoeller&reg; Nylon Storm Pant, Slate Grey", "$378", U("whimgolf.com","schoeller-nylon-storm-pant-slate-grey"),
   "Slate grey to finish the suit. Both pieces also come in apple green, the color in the photo at the top of this post."),
 "l1": ("Local Rule", "Tech Anorak, Dusty Olive", "1,439 kr (~$142)", U("local-rule.com","tech-anorak-dusty-olive"),
   "Three-layer waterproof and windproof fabric, a ventilation flap across the upper back, a half zip with a stand-up collar and a pullover cut with no open front to catch the wind. GOLF-WORK-WEAR lettering at the hem. Ships Dec 3."),
 "l2": ("Local Rule", "Midlayer Q-zip, Light Brown", "799 kr (~$79)", U("local-rule.com","midlayer-q-zip-light-brown"),
   "A technical nylon-elastane interlock with laser-cut ventilation and stretch through the swing, cut relaxed so it layers under the anorak. Ships Nov 25."),
 "l3": ("Local Rule", "Midlayer Q-zip, Dark Green", "799 kr (~$79)", U("local-rule.com","midlayer-q-zip-dark-green"),
   "The same midlayer in dark green, with the Local Rule script on the chest."),
 "l4": ("Local Rule", "Midlayer Q-zip, Light Green", "799 kr (~$79)", U("local-rule.com","midlayer-q-zip-light-green"),
   "And in a pale light green, the quietest of the four colors."),
 "h1": ("Hendrikx", "Half-Zip, Caff\u00e8", "&euro;390 (~$428)", HX("half-zip-caffe-men"),
   "Deep brown melange in 19.5-micron merino from a 125-year-old Piedmont mill, knitted in Emilia-Romagna, with a gold zip, a brown eco-leather puller and the H monogram on the hip."),
 "h2": ("Hendrikx", "Half-Zip, Avorio", "&euro;390 (~$428)", HX("half-zip-avorio-men"),
   "The same half-zip in Avorio, a warm ivory, with the monogram stitched in brown."),
 "h3": ("Hendrikx", "Polo, Eredit\u00e0", "&euro;260 (~$285)", HX("polo-eredita-men"),
   "All-season 178 g/m&sup2; cotton piqu&eacute; with a deep green collar and cuffs knitted in Egyptian Giza cotton, and tagua-nut buttons sewn on by hand."),
 "h4": ("Hendrikx", "Polo, Sabbia", "&euro;260 (~$285)", HX("polo-sabbia-men"),
   "The polo in Sabbia, with a sand-colored Giza collar and cuffs. Both polos are machine washable."),
 "h5": ("Hendrikx", "Driver Headcover", "&euro;150 (~$165)", HX("headcover-virgin-wool-and-alpaca"),
   "Sewn by hand in Germany from an Italian virgin wool and alpaca blend, in a deep brown they call Mocha. Wood and hybrid versions too."),
 "a1": ("Eastside Golf &times; Avirex", "ESG &times; Avirex Varsity Jacket", "$448", U("eastsidegolf.com","esg-x-avirex-varsity-jacket"),
   "A wool body with genuine leather sleeves, a varsity E appliqu&eacute;, collaborative patches and a snap front. The sleeve print carries both founding years: Eastside Golf 2019, Avirex 1975."),
 "a2": ("Eastside Golf &times; Avirex", "ESG &times; Avirex MA-1 Nylon Bomber", "$398", U("eastsidegolf.com","esg-x-avirex-nylon-jacket"),
   "Avirex&rsquo;s classic bomber in 100% nylon, with Eastside and Avirex patches up front and Eastside&rsquo;s swinging golfer across the back."),
}
SECTIONS = [
 ("Mogshade &times; Incense Harbour and Fabricaal", "mogshade", ["g1","g2","g3","g4","g5","g6"],
  "<strong>Two capsules in two weeks &middot; Nov 4&ndash;12</strong>Water-repellent Japanese nylon with a three-person Hong Kong label, then hand-loomed Portuguese merino."),
 ("Whim: The FW26 Storm Suit", "whim", ["w1","w3","w4","w5"],
  "<strong>A rain suit that does not look like one &middot; Nov 18</strong>A windbreaker and pant in Swiss Schoeller stretch nylon, made in New York, in clear water green, slate grey and apple green."),
 ("Local Rule: FW26 Tech Layers", "localrule", ["l1","l2","l3","l4"],
  "<strong>Rain or wind, keep playing &middot; Nov 16</strong>A three-layer waterproof anorak and a vented midlayer from Stockholm, designed to be worn one over the other."),
 ("Hendrikx: A Debut, Made in Italy", "hendrikx", ["h1","h2","h3","h4","h5"],
  "<strong>A new label from D&uuml;sseldorf &middot; Nov 6</strong>One half-zip, one polo, two colors each and a headcover, from a family that has played golf since the 1940s."),
 ("Eastside Golf &times; Avirex", "avirex", ["a1","a2"],
  "<strong>Two jackets, two histories &middot; Nov 11&ndash;12</strong>Avirex&rsquo;s flight-jacket heritage meets Eastside&rsquo;s golf: an MA-1 bomber reworked in nylon and a wool-and-leather varsity."),
]
N = 21
SECN = {"mogshade": 6, "whim": 4, "localrule": 4, "hendrikx": 5, "avirex": 2}
PAIRS = {}
IDEA = {
 "mogshade": """<p><strong>Who they made it with.</strong> Incense Harbour is a small Hong Kong label run by Erick Sze and a team of three, which its listing at the city&rsquo;s PMQ design hub says began during COVID, when the founders were looking at Hong Kong with fresh eyes. The name is a direct translation of the Chinese name for Hong Kong, &#39321;&#28207;. Mogshade describes the drop as bringing together Incense Harbour&rsquo;s &ldquo;distinctive approach to everyday objects&rdquo; and its own love of textiles, craftsmanship and the game.</p>
    <p><strong>The fabric.</strong> Everything in the Incense Harbour drop is cut from MacLowly, a Japanese water-repellent nylon, and the pouches are lined in Portuguese wool. The second capsule goes the other way: Fabricaal, short for F&aacute;brica Alentejana de Lanif&iacute;cios, weaves its merino on manual wooden looms in Portugal&rsquo;s Alentejo, in what Mogshade calls one of only three original secular wool handicrafts still running in Europe.</p>""",
 "whim": """<p><strong>One layer, no laminate.</strong> Most rain gear is a sandwich of face fabric, membrane and lining. Whim&rsquo;s Storm suit skips the sandwich: it is a single dense stretch weave of Schoeller Dynamic, a Swiss nylon, with a water-repellent finish on the outside. Wind stays out and light rain beads off, while body heat and moisture pass through. In Whim&rsquo;s words, it &ldquo;breathes the way a shell should, so it wears cool through a full round instead of trapping you in.&rdquo;</p>
    <p><strong>Made to be worn as a suit.</strong> The windbreaker and pant come in matching colors and are made in New York. The lookbook leans all the way in: golfers head to toe in one color, on a grey late-fall course.</p>""",
 "localrule": """<p><strong>Who they are.</strong> Local Rule is a three-person company out of Stockholm, started in 2022 by two founders from an advertising agency and named for the supplementary sheet a club prints for its own course: the sanctioned exception to the general rules. In 2025 it began moving production home to Bor&aring;s. We covered the whole story in our <a href="/drops/brand-to-know-local-rule">Brand to Know</a>.</p>
    <p><strong>The idea.</strong> Local Rule&rsquo;s line for this drop is four words: &ldquo;Rain or wind, keep playing.&rdquo; The anorak is a pullover, not a jacket, so there is no open front flapping through your swing. It is cut from a three-layer waterproof, windproof fabric with a vent across the upper back to let heat out as you walk. The midlayer underneath is a nylon-elastane interlock with laser-cut ventilation. Local Rule&rsquo;s own advice is to wear one over the other on cold, wet days, which is exactly how the clean Scandinavian studio lookbook shows them.</p>
    <p><strong>Timing.</strong> Both are pre-orders: the midlayer ships from Local Rule&rsquo;s warehouse on November 25 and the anorak on December 3. Prices are in Swedish kronor.</p>""",
 "hendrikx": """<p><strong>A family thing.</strong> Hendrikx was founded in 2025 by Jan Hendrikx and his partner Karolina, working from D&uuml;sseldorf, where his family has lived since the 1850s. Golf has been in the family since the 1940s. The black-and-white photo below is Jan&rsquo;s grandfather, Jochen Hendrikx, in the 1970s, and the brand says it has always loved the way he dressed and that much of what it makes still comes back to that.</p>
    <p><strong>Made in Italy, all the way down.</strong> The half-zip is knitted in a small family workshop in Emilia-Romagna from 19.5-micron merino spun at a 125-year-old mill in Piedmont. The polo&rsquo;s collar and cuffs are knitted in Egyptian Giza cotton, and its six-hole tagua-nut buttons are sewn on by hand with thread that forms a sideways H. Even the labels and hangtags are sourced in Italy, and both pieces are machine washable. The debut campaign was shot at Ch&acirc;teau d&rsquo;Augerville, south of Paris.</p>""",
 "avirex": """<p><strong>Flight jackets, meet the first tee.</strong> Avirex built its name on military flight jackets, and the MA-1 bomber is the classic shape. Eastside Golf reworks it in red nylon, puts its swinging golfer across the back and pairs it with a varsity jacket in wool and leather. &ldquo;Two legacies. One statement,&rdquo; is how Eastside puts it.</p>
    <p><strong>The details.</strong> Collaborative patches on both, an ESG crest on the bomber&rsquo;s chest, a varsity E on the wool body and both brands&rsquo; founding years printed down the sleeve. It is a two-piece capsule, which is exactly the point: no tees, no hats, just the jackets.</p>""",
}
BANDS = {
 "mogshade": [("band-mogshade-1","Mogshade x Incense Harbour totes on shoreline rocks","Mogshade &times; Incense Harbour"),
   ("band-mogshade-2","Navy and rust Mogshade fish pouches beside a fly reel","Mogshade &times; Incense Harbour"),
   ("band-mogshade-3","Three Mogshade x Incense Harbour headcovers on dark rocks","Mogshade &times; Incense Harbour"),
   ("band-mogshade-4","A weaver at a manual wooden loom at Fabricaal in Portugal","Fabricaal, Alentejo"),
   ("band-mogshade-5","A tattooed arm opening a Mogshade x Fabricaal glasses case","Mogshade &times; Fabricaal"),
   ("band-mogshade-6","Fabricaal wool on a stone wall above a whitewashed Portuguese village","Mogshade &times; Fabricaal")],
 "whim": [("band-whim-1","A golfer in the clear water green Whim Storm suit playing from a sandy waste area","Whim &middot; Clear Water Green"),
   ("band-whim-2","A golfer in a slate grey Whim Storm suit putting","Whim &middot; Slate Grey"),
   ("band-whim-3","A golfer in an apple green Whim Storm suit tending the flag","Whim &middot; Apple Green")],
 "localrule": [("band-localrule-1","A man in the Local Rule Tech Anorak in dusty olive","Local Rule &middot; Tech Anorak"),
   ("band-localrule-2","A man in the navy Local Rule Midlayer Q-zip","Local Rule &middot; Midlayer Q-zip"),
   ("band-localrule-3","Side view of the dark green Local Rule Midlayer Q-zip","Local Rule &middot; Midlayer Q-zip")],
 "hendrikx": [("band-hendrikx-1","Archival black-and-white photo of Jochen Hendrikx putting in the 1970s","Jochen Hendrikx, 1970s"),
   ("band-hendrikx-2","A man in a Hendrikx polo seated in a leather armchair","Hendrikx &middot; Ch&acirc;teau d&rsquo;Augerville"),
   ("band-hendrikx-3","A man in the Hendrikx Caff&egrave; half-zip holding a flagstick","Hendrikx"),
   ("band-hendrikx-4","A golfer in Hendrikx crouching to read a putt","Hendrikx"),
   ("band-hendrikx-5","A man in the Hendrikx Eredit&agrave; polo in a golf cart","Hendrikx"),
   ("band-hendrikx-6","The embroidered H monogram on a Hendrikx merino half-zip","Hendrikx")],
 "avirex": [("band-avirex-1","A golfer swinging in the red Eastside x Avirex MA-1 bomber on a city street","Eastside Golf &times; Avirex"),
   ("band-avirex-2","A man in the Eastside x Avirex varsity jacket under elevated train tracks","Eastside Golf &times; Avirex"),
   ("band-avirex-3","Side view of the Eastside x Avirex varsity jacket","Eastside Golf &times; Avirex")],
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>November is when the big brands go loud: holiday collections, bundles, a hundred new products at a time. The drops we like best this month went the other way. Five small brands and collaborations put out a handful of pieces each, every one of them built around a single idea you can explain in a sentence.</p>
    <p><strong>How we found them.</strong> We checked the stores of 133 brands in our index for everything added since mid-October, then looked further afield for debuts and collaborations, and set aside anything we had already covered. What was left: a Hong Kong collaboration in Japanese nylon, a one-layer rain suit, a Stockholm anorak built to be worn over its own midlayer, a family label making knitwear in Italy and two jackets from brands founded 44 years apart.</p>
    <p><strong>What ties them together.</strong> Material and origin. MacLowly nylon and hand-loomed Portuguese wool, Swiss Schoeller made up in New York, three-layer Swedish rain gear, Piedmont merino and Giza cotton finished in Emilia-Romagna, wool and leather on a varsity. Each section below starts with the idea, then the lookbook, then the pieces.</p>
    <p><strong>What is in here.</strong> 21 pieces from five drops, none of them featured on TGI before. Prices are what each store shows a US visitor; Hendrikx sells in euros and Local Rule in kronor, so we list a rough dollar figure beside those. Everything was in stock when we checked on November 19, 2026.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Details</div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>21</span></div>
      <div class="sidebar-detail"><span class="l">Drops</span><span>5</span></div>
      <div class="sidebar-detail"><span class="l">Dropped</span><span>Nov 4 &ndash; Nov 18</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$34&ndash;$448</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Hendrikx Half-Zip, Caff&egrave;</span></div>
      <div class="hashtags">
        <span class="hashtag">#NewDrops</span>
        <span class="hashtag">#IndieGolf</span>
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
    <h2 class="products-hdr" id="last-word">Small Runs Go Fast</h2>
    <p>Two Fabricaal headcovers were gone inside a week, Local Rule&rsquo;s whole autumn delivery sold through before this one, and a debut label making two shirts in two colors does not make many of either. If something here is the one, do not wait for Black Friday to find out whether it is still there.</p>
    <p>For more from these brands, see our <a href="/brands/mogshade">Mogshade</a>, <a href="/brands/whim-golf">Whim</a>, <a href="/brands/local-rule">Local Rule</a> and <a href="/brands/eastside-golf">Eastside Golf</a> pages.</p>
  </div>
</section>
"""
HERO_ALT = "A golfer in an apple green Whim Schoeller Storm windbreaker and pant swinging on a tee box under a grey November sky"
FRN = json.loads((ROOT / "research/curated-drops/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-AG-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-11-19", "dateModified": "2026-11-19",
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
    figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>' for f, alt, cap in BANDS[anchor])
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} picks</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'  <div class="writeup-body" style="max-width:760px;margin:0 auto 26px">\n    {IDEA[anchor]}\n  </div>\n'
            f'  <div class="ig-grid">\n{figs}\n  </div>\n'
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
    for s in SECTIONS: assert len(s[2]) == SECN[s[1]], s[0]
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
    <span>The Edit &middot; New drops</span><span class="dot"></span>
    <span>21 picks from 5 drops &middot; checked November 19, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="{HERO_ALT}" fetchpriority="high" /></div></div>
"""
    body += TAKE.replace("@@NB@@", str(len({P[k][0] for s_ in SECTIONS for k in s_[2]})))
    n = 1
    for s in SECTIONS:
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
    for leak in ("Pins &amp; Aces", "Pins & Aces"):
        if leak in above: bad.append("leak " + leak)
    if fin.count('class="product-card"') != N: bad.append("card count")
    if re.search(r"\b(worth|genuinely|honestly|straightforward|selling out)\b", re.sub(r"<[^>]+>", " ", above), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
