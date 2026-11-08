"""build-hidden-details.py — Hidden Details: golf clothes and kit with clever little features, 5 November 2026. Cloned from build-baggy-pants.py.
Lenny: "Let's do a post about Hidden details, for instance masterpiece polo has nice little pockets for tees, Draw and agronomy workshop also has
those little Tee pockets ... Manors greenskeeper pants has a little magnet in the pocket for your ball marker." Picks: Lenny's four, his 10 from the
options list, plus the Tool Loafer, A.P.C. cap, Fella cargo and Walker Members Pant to make 18. FACTS: product pages; the Manors magnet is Lenny's own.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"
TITLE = "Hidden Details: 18 Golf Pieces With Tee Pockets, Ball Marker Magnets and Clever Little Features"
DESC = ("The small things that make golf clothes better: tee holders in polos and hats, magnets for your ball marker, glove loops, scorecard pockets "
        "and a loafer that hides a divot tool. 18 pieces from 16 independent brands.")
H1 = "Hidden Details: 18 Pieces With Tee Pockets, Marker Magnets and Clever Little Features"
BC = "Hidden Details"
SLUG = "hidden-details-golf-gear"
IMG = "/images/hidden-details"
U = lambda d, h: f"https://{d}/products/{h}"
P = {
 "mp": ("Masterpiece Sports Club", "Semi-Private Performance Polo", "$118", U("masterpiecegolf.com","pique-poly-golf-polo-ss-cream"),
   "Masterpiece builds its signature tee holder into the polo, so a couple of tees ride on your chest instead of rattling around a pocket. Stretch performance body, cotton poplin collar that holds its shape, side vents at the hem."),
 "ag": ("Agronomy Workshop", "S/S Heavyweight Work Shirt, Earth", "$136", "https://agronomywork.shop/store/heavyweight-work-shirt-ss-earth",
   "A 17.5 oz cotton mock neck, hand-dyed and hand-sewn in Los Angeles. The chest pocket hides a tee holder that takes up to three tees. We covered the shirt on its own in <a href=\"/drops/agronomy-workshop-a-golf-shirt-with-a-hidden-tee-slot-and-no\">our Agronomy Workshop story</a>."),
 "dr": ("Draw", "Forest Green Unstructured Corduroy Cap", "$58", U("drawgolf.co","forest-green-unstructured-corduroy-cap"),
   "Woven corduroy with a brushed silver buckle, and a small pouch on the side that holds a tee. Look closely and it reads as a design detail; on the course it saves a trip to the bag."),
 "fb": ("Fella Golf", "Cha-Cheng Tee Bucket Hat", "$60", U("fellagolf.com","cha-cheng-tee-buckethat"),
   "A lightweight, breathable bucket for hot days, with tee holders worked into the side loops: room for six tees, close when you need them and out of the way when you don&rsquo;t."),
 "rw": ("Rowena Golf Club", "Laurel Linen Trouser, Navy Pinstripe", "$108", U("rowenagolf.com","linen-trouser"),
   "Relaxed linen with a single pleat and elastic at the sides of the waistband, plus a dedicated tee pocket. The little embroidered tee on the pocket tells you where it is."),
 "tc": ("3 Putt Round", "The iPhone Tee Case", "&euro;35 (~$40)", U("3puttround.com","the-tee-case"),
   "A silicone iPhone case with a tee holder molded into the back. 3 Putt Round calls it the first of its kind, and the fastest way to turn strangers into playing partners. Made for recent Pro and Pro Max models."),
 "gk": ("Manors Golf", "Recycled Greenskeeper Trouser", "$176", "https://www.manorsgolf.com/products/recycled-greenskeeper-trouser",
   "Four-way stretch recycled nylon, double pleats, a drawcord waist and eight pockets. The detail Manors doesn&rsquo;t list: a small magnet in the pocket that holds your ball marker. We found it wearing them."),
 "ap": ("A.P.C. Golf", "Golf Cap, Navy", "&euro;95 (~$108)", U("apcstore.com","golf-cap-iaj-cohve-m24230"),
   "Navy cotton with white topstitching, and a removable metal ball marker clipped to the visor, engraved with the A.P.C. logo. Pop it off on the green and put it back when you pick up."),
 "rb": ("Rebolf x Balteus", "Fade Black Velcro Belt", "$91", U("rebolf.com","fade-black-velcro-belt"),
   "A crocodile-textured belt with no buckle, inspired by cowboy belts, that closes flat with Velcro. It also carries a magnetized ball marker, so it is always within reach. Sizes are running thin."),
 "wk": ("Walker Golf Things", "Members Pant, Tan", "$120", U("walkergolfthings.com","members-pant-1"),
   "Light, breathable stretch with an internal ball marker pocket and an internal tee pocket on the right side, so the small things stay out of sight."),
 "fc": ("Fella Golf", "Ripstop Cargo Pant", "$135", U("fellagolf.com","fella-ripstop-cargo-pant"),
   "The most thought-through pant here: Velcro front belt loops hold your glove while you putt, a rope tee holder sits at the left pocket, the cargo pockets close with magnets, and the cuffs cinch."),
 "jj": ("Juniper &amp; James", "Golf Shorts, Driftwood", "$99", U("juniperjamesgolf.com","driftwood"),
   "From New Braunfels, Texas: four-way stretch shorts with UPF 50+ sun protection, a gripper waistband, a glove loop, and a microfiber cloth tucked into the back pocket."),
 "tl": ("ANTi Country Club Tokyo x TOMO &amp; CO.", "Tool Loafer", "$484.56", U("anticountryclubtokyo.com","tool-loafer-anti-country-club-tokyo-x-tomo-co-collaboration-loafer"),
   "Our favorite find. A leopard-print penny loafer where the penny slot holds a divot tool made for the collaboration, stamped &ldquo;LOVE&rdquo; on one and &ldquo;HATE&rdquo; on the other. Golf you can wear to dinner."),
 "rt": ("Manors Golf", "Ripstop Tech Trouser", "$203", "https://www.manorsgolf.com/products/ripstop-tech-trouser",
   "Recycled Toray ripstop with a gusset so the seat doesn&rsquo;t pull when you turn. The scorecard pockets are laser cut, with no stitching or bulk, so a folded card sits flat."),
 "sd": ("Sounder", "Haar Windcheater, Lava Red", "&pound;145 (~$190)", U("soundergolf.com","haar-windcheater-ripstop-lava-red"),
   "A showerproof ripstop half-zip with a hood hidden inside the collar and a scorecard pocket on the back, marked with a small Sounder star. Named for the haar, the sea fog that rolls onto Scotland&rsquo;s east coast links."),
 "pl": ("Pluto Golf", "Road Pants, Olive", "$144", U("pluto.golf","road-pants-olive"),
   "A classic straight-leg, button-fly pant from Indianapolis with a metal crest button and a hidden zip pocket for the things you don&rsquo;t want to lose between holes."),
 "mg": ("Mogshade", "Risca Light Course Case", "$141", U("mogshadegolf.com","risca-light-course-case"),
   "Handmade in Portugal from rescued wool woven in the Serra da Estrela mountains. Inside, a pocket for ball markers and loops for a few tees; the rest is open for a rangefinder or valuables. It clips on with a carabiner."),
 "st": ("STITCH", "SL2 Gen 2 Stand Bag", "$398", U("stitchgolf.com","sl2-gen-2"),
   "A clean stand bag hiding a magnetic pocket built to carry a full 12-pack of balls. The Gen 2 adds 50% more storage. The Onyx colorway is on sale for $189."),
}
SECS = [
 ("where-the-tees-go", "Where the Tees Go", "Polos, shirts, hats, trousers and a phone case", ["mp","ag","dr","fb","rw","tc"],
  "The tee is the thing every golfer needs and nobody has a good place for. These brands found one: a holder built into a polo, a hidden slot in a chest pocket, a pouch on a cap, loops on a bucket, a pocket on a pair of trousers and, yes, the back of your phone."),
 ("marker-glove-card", "The Marker, the Glove and the Card", "Magnets, loops and pockets for the small stuff", ["gk","ap","rb","wk","fc","jj"],
  "The ball marker, the glove you take off to putt, the card you keep score on. Each of these pieces gives one of them a home, from a magnet you only find by wearing the pants to a marker that clips onto your cap."),
 ("hidden-in-plain-sight", "Hidden in Plain Sight", "Shoes, layers, pants and the bag", ["tl","rt","sd","pl","mg","st"],
  "The details you would never spot from across the range: a divot tool in a loafer, laser-cut scorecard pockets, a hood folded into a collar, a hidden zip pocket, a wool case with a place for everything, and a magnet holding a dozen balls."),
]
SECTIONS = [(s[1], s[0], s[3], s[2]) for s in SECS]
N = 18
PAIRS = {}
BANDS = {
 "marker-glove-card": ("In the wild", "On the course and off it", [("life-a-1","A golfer swinging on a tree-lined course in tan Walker pants","Walker Golf Things"),("life-a-2","A golfer climbing out of an old red truck on the course","Juniper &amp; James"),("life-a-3","A hand pulling a phone with a tee in its case from a trouser pocket","3 Putt Round"),("life-a-4","Leopard loafers and yellow socks on a patterned rug","ANTi Country Club Tokyo"),("life-a-5","A golfer by a pond in tan pants holding a club","Walker Golf Things"),("life-a-6","A man in a utility vest and the Fella bucket hat","Fella Golf")]),
 "end": ("Up close", "The details, closer", [("life-b-1","Fella cargo pant with the Velcro belt loop and pocket detail","Fella Golf"),("life-b-2","Tees held in the loops inside a Mogshade course case","Mogshade"),("life-b-3","The side of a green STITCH stand bag","STITCH"),("life-b-4","The star-printed scorecard pocket on the back of a red Sounder windcheater","Sounder"),("life-b-5","The insole of the ANTi Country Club Tokyo Tool Loafer","ANTi Country Club Tokyo"),("life-b-6","A green 3 Putt Round tee case on a red car","3 Putt Round")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>The best golf clothes are full of things you only notice once you have them on. A tee holder inside a chest pocket. A magnet that grabs your ball marker. A loop that holds your glove while you putt. None of them make a piece look different from across the range, and all of them change how it feels to play in it.</p>
    <p>These are the details that separate a brand that makes golf clothes from a brand that plays golf. Somebody on the team got tired of digging for a tee, or putting a marker in the wrong pocket, and fixed it. That is what we love about independent golf: the people designing the clothes are out there using them.</p>
    <p><strong>How we picked.</strong> We started with the details we already loved (Masterpiece&rsquo;s tee holder, the tee pockets from Draw and Agronomy Workshop, and the marker magnet in the Manors Greenskeeper Trouser) and then read through the product pages of every brand in our index for tee holders, magnets, glove loops, scorecard pockets and hidden pockets. Everything was in stock on November 5, 2026.</p>
    <p><strong>Where to start.</strong> The Fella Ripstop Cargo Pant, $135, packs the most into one piece: a glove loop, a tee holder, magnetic pockets and cinch cuffs. For a small gift, the Draw cap is $58 and the Fella bucket is $60. And if you want the one people will ask about, it is the Tool Loafer.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Details</div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>18</span></div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>16</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$58&ndash;$484.56</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Fella Ripstop Cargo Pant</span></div>
      <div class="hashtags">
        <span class="hashtag">#HiddenDetails</span>
        <span class="hashtag">#GolfStyle</span>
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
    <h2 class="products-hdr" id="last-word">The Small Things Are the Point</h2>
    <p>A round of golf is four hours of small, repeated tasks: tee up, mark, pick up, take the glove off, put it back on, write a number down. A detail that saves five seconds on each of those adds up over eighteen holes, and it is the difference between a piece you like and a piece you reach for every time you play.</p>
    <p><strong>What to look for.</strong> The best details are invisible until you need them. A tee holder should keep tees from falling out when you bend over to read a putt. A marker magnet should be strong enough to hold through a swing. A scorecard pocket should fit a folded card without a bulge. If a feature changes how the piece looks more than how it works, it is decoration, not a detail.</p>
    <p><strong>Ask the brand.</strong> Plenty of these features never make it onto the product page. The magnet in the Manors Greenskeeper Trouser is a good example; we only found it by wearing them. If you are buying from a small brand, send them a message and ask what is built in. The people who answer are usually the people who designed it.</p>
    <p><strong>They make better gifts.</strong> A hidden detail is the kind of thing someone finds on the first tee and remembers who gave it to them. The caps, the bucket and the tee case are easy stocking ideas, and the loafer is for the person who has everything.</p>
    <p>Prices are as each store shows them to a US visitor. A.P.C. and 3 Putt Round show euros and Sounder shows pounds, so those dollar figures are approximate. All 18 were in stock on November 5, 2026. If you have a favorite hidden detail we missed, send it our way.</p>
  </div>
</section>
"""
HERO_ALT = "Three close-ups: tees tucked in a hidden chest-pocket holder, a glove held by a belt loop on cargo pants, and two divot tools stamped Love and Hate"
FRN = json.loads((ROOT / "research/hidden/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-COL-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
         "url": URL, "image": og, "datePublished": "2026-11-05", "dateModified": "2026-11-05",
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
            f'  <div class="drop-tag grass">{num:02d} &middot; {len(ids)} pieces</div>\n'
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
    <span>The Edit &middot; Tee pockets, magnets and clever little features</span><span class="dot"></span>
    <span>18 pieces &middot; in stock, checked November 5, 2026</span>
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
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
