"""build-baggy-pants.py — loose, baggy golf pants roundup, 4 November 2026. Cloned from build-far-and-wide.py.
Lenny: "Let's do a round up of loose baggy pants for golf, my personal favorite", then "show me the preview" (picks are mine from the
options list; nothing repeated from The Pants Edit or the Top 5 Pants). FACTS: product pages, each store's currency as shown to a US visitor.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"
TITLE = "Loose Golf Pants: 18 Wide, Baggy and Barrel-Leg Trousers for Breathability and a Free Swing"
DESC = ("Why we love loose golf pants: air, flow and room to swing. Eighteen wide-leg, pleated, barrel and relaxed trousers from 18 independent brands, "
        "including Students, Woodgrain, Late Nine, Fella, Grind City, Slice Town and SLOAT.")
H1 = "Room to Move: 18 Loose Golf Pants for Breathability, Flow and a Free Swing"
BC = "Loose Golf Pants"
SLUG = "baggy-golf-pants-edit"
IMG = "/images/baggy-pants"
SHOP = ""
U = lambda d, h: f"https://{d}/products/{h}"
P = {
 "sci": ("Students", "Science Adjustable Pleated Pants, Black", "$135", U("studentsgolf.com","science-adjustable-baggy-pants-1"),
   "Our favorite. A velcro waist moves the pleats and changes the silhouette, from relaxed to properly baggy, in stretch nylon that breathes. Inspired by military trousers."),
 "wl": ("Winslow", "Simple Pant, Cream", "$80", U("winslowla.com","simple-pant"),
   "100% cotton with double pleats and a roomy, easy leg. Made to dress up or down, and one of the best prices here."),
 "apc": ("A.P.C. Golf", "Renato Golf Trousers, Navy", "&euro;260 (~$297)", U("apcstore.com","renato-golf-trousers-iaj-psanz-h08055"),
   "A.P.C.&rsquo;s Renato trouser cut wide for golf, in water-repellent fabric with a little stretch."),
 "rw": ("Rowena Golf Club", "Laurel Linen Trouser, Navy Pinstripe", "$108", U("rowenagolf.com","linen-trouser"),
   "Lightweight linen in a relaxed, straight leg with a single pleat, elastic at the sides of the waistband and a tee pocket. Rowena says it is built to walk in and flow with the game. Also in cr&egrave;me."),
 "cph": ("Cph/Golf", "Belted Adjustable Wide Pants", "$121", U("captainshelmgolf.com","chg26-aw-p02"),
   "Stretch wide pants with a generous, roomy silhouette and a built-in belt to dial the waist. A regular in the Tokyo brand&rsquo;s line."),
 "gc": ("Grind City Golf", "No¹⁸ Barrel Leg Trousers", "$72", U("grindcitygolf.com","men-s-barrel-leg-pants"),
   "A modern take on golf tailoring: a curved barrel leg that is full through the knee and tapers at the hem."),
 "slt": ("Slice Town", "Wide Pleated Pants, Brown", "$185", U("slice-town.com","wide-pleated-pants-brown"),
   "Wool-blend, single front pleats and a properly wide leg, designed in Copenhagen. Extra long and wide in the waist, so size down."),
 "wk": ("Walker Golf Things", "Pleated Easy Pant, Navy", "$101", U("walkergolfthings.com","pleated-easy-pant-1"),
   "Relaxed enough to chill, sharp enough to wear on course all day. Walker calls it the pant between the fairway and Friday night."),
 "pare": ("Par&eacute;", "Plisse Pants 2.0", "$150", U("pare.golf","pare-plisse-pants-2-0"),
   "The second version of Par&eacute;&rsquo;s pleated-texture pant, built around effortless comfort. Made to be worn everywhere."),
 "ag": ("Angus &amp; Grace", "Men&rsquo;s Trouser", "250 AUD (~$163)", U("angusandgracegogolfing.com","mens-trouser"),
   "Straight cut with an inverted box pleat and a generous fit through the waist, from the Australian brand. If in doubt, size down."),
 "grcar": ("Gramicci", "Big Wale Carpenter Pant", "$140", U("gramicci.com","big-wale-carpenter-pant"),
   "Wide-wale cotton corduroy in a carpenter cut with a below-knee break line, plus the elastic waist and built-in Gramicci belt."),
 "wd": ("Woodgrain Golf", "Relaxed Double Pleated Trouser, Tan", "$180", U("woodgrain.golf","relaxed-double-pleated-trouser-tan"),
   "Wide leg, double pleats and 100% cotton, cut after the way golf trousers looked in the &rsquo;80s and &rsquo;90s. Also in black, chocolate and cream."),
 "ln": ("Late Nine", "Double Pleat Trousers, Beige", "2,800 SEK (~$283)", U("late-nine.com","double-pleats-beige"),
   "Stockholm&rsquo;s take on the pleated chino: two pleats, a full leg and a light, durable cotton twill with a subtle texture. New for SS26."),
 "lof": ("Left of Field Golf", "Elements Pleated Wide Leg Tech Trouser", "$60", U("lofgolf.com","xpleated-wide-leg-tech-trouser"),
   "The Sydney brand&rsquo;s wide-leg tech pant, pleated at the front and shot on the dunes. On sale from $100, and the lowest price here."),
 "fl": ("Fella Golf", "Ripstop Cargo Pant", "$135", U("fellagolf.com","fella-ripstop-cargo-pant"),
   "Lightweight ripstop in a relaxed fit, with magnetic cargo pockets, a rope tee holder and velcro belt loops to hold your glove while you putt. Cinch the cuffs or wear them loose."),
 "sloat": ("SLOAT", "Organic Cotton Day Pant", "$195", U("sloat.cc","mens-organic-cotton-golf-pants"),
   "SLOAT&rsquo;s most casual pant: light organic cotton twill sewn in Portugal, an elastic waist, belt loops and fuller proportions."),
 "tf": ("Twentyfour Golf", "Clubhouse Pants, Olive", "$93.03", U("twentyfourgolf.com","clubhouse-pants-olive"),
   "Relaxed through the leg with a straight cut, in a stretchy nylon blend. Course to clubhouse without a change."),
 "mac": ("Macade", "Lightweight Relaxed Trouser, Stone Blue", "$130", U("macadegolf.com","lightweight-stone-blue-relaxed-trouser"),
   "The hot-weather pick: a relaxed cut in moisture-managing fabric with ROICA stretch, made for summer rounds."),
}
SECS = [
 ("properly-baggy", "Properly Baggy", "Wide legs, long drops and plenty of fabric", ["sci","wd","lof","wl","apc","rw"],
  "These are the ones that read baggy from across the range. Wide all the way down, room to swing, and a hem that sits on the shoe rather than above it."),
 ("barrel-and-pleats", "Barrel Legs and Pleats", "Full through the knee, shaped at the hem", ["gc","cph","slt","wk","pare","ln"],
  "The barrel leg is the newest shape in golf: full through the thigh and knee, then curved in toward the ankle. Pleats do a similar job with a dressier look, adding room at the top without making the pant sloppy."),
 ("workwear-and-easy", "Workwear and Easy Waists", "Carpenter cuts, tech fabrics, easy waists", ["grcar","fl","sloat","tf","mac","ag"],
  "Baggy pants started as work pants, and these keep that feel: heavy cotton, corduroy, carpenter details, stretch tech fabrics and waists you can adjust on the fourth hole."),
]
SECTIONS = [(s[1], s[0], s[3], s[2]) for s in SECS]
N = 18
PAIRS = {}
BANDS = {
 "barrel-and-pleats": ("In the wild", "Loose pants on the course", [("life-a-1","A golfer holding the flagstick on a links course","SLOAT"),("life-a-2","A golfer crouching to read a putt in loose pants","Slice Town"),("life-a-3","A golfer mid-swing on an autumn course","Par&eacute;"),("life-a-4","Two golfers on the course in wide pants, seen from behind","Cph/Golf"),("life-a-5","Two golfers climbing out of a dune bunker with a carry bag","Left of Field"),("life-a-6","Wide black trousers and sneakers in the dune grass","Left of Field")]),
 "workwear-and-easy": ("The lookbook", "Barrels and pleats, on people", [("life-b-1","Grind City barrel pants with a striped shirt","Grind City Golf"),("life-b-2","Grind City barrel pants in black","Grind City Golf"),("life-b-3","Slice Town wide trousers","Slice Town"),("life-b-4","Slice Town loose pants and a cap","Slice Town"),("life-b-5","Slice Town wide pleated pants in brown","Slice Town"),("life-b-6","Par&eacute; Plisse pants with a black sweater","Par&eacute;")]),
 "end": ("Outside", "Loose pants out in the world", [("life-c-1","Walker pleated pants on a course under the mountains","Walker Golf Things"),("life-c-2","Walker pleated pants and a glove at the waist","Walker Golf Things"),("life-c-3","Walker pleated pants with a tee in the pocket","Walker Golf Things"),("life-c-4","A group of golfers on the course at golden hour","Walker Golf Things"),("life-c-5","Winslow cream pleated pants outdoors by an old truck","Winslow"),("life-c-6","Walker pleated pants on a course with kangaroos","Walker Golf Things")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Loose pants are our favorite thing to golf in, for three simple reasons. They breathe: air moves around your legs on a hot Austin afternoon instead of the fabric sticking to you. They flow: a wide leg hangs and moves with you, and it looks relaxed walking down the fairway. And they give you room: nothing pulls at the knee when you crouch to read a putt or the hip when you turn through the ball.</p>
    <p>Independent brands have been cutting golf pants this way for a few seasons now. Students, Woodgrain, Grind City, Slice Town and Walker take shapes from workwear and streetwear and make them work on the course, and the lookbooks below show how they wear.</p>
    <p><strong>How we picked.</strong> We went through the stores of the brands in our index, from Austin to Stockholm and Sydney, and pulled every men&rsquo;s pant cut wide, baggy, barrel or relaxed that was in stock on November 4, 2026, then kept one pair per brand: 18 brands, 18 pants. Nothing here repeats our <a href="/drops/the-pants-edit">Pleated Pants Edit</a> or our <a href="/drops/best-golf-pants-ranked">five best golf pants</a>.</p>
    <p><strong>How to wear them.</strong> Go one size down if you are between sizes; most of these run generous on purpose. Let the hem sit on the shoe. A boxy polo or a short knit balances the volume, and a chunky shoe keeps a wide leg from swallowing your feet.</p>
    <p><strong>Where to start.</strong> The Students Science Adjustable Pleated Pants, $135, the Students pant from our <a href="/drops/best-golf-pants-ranked">best golf pants ranking</a> and still the pair we reach for first. The velcro waist lets you move the pleats and decide how baggy you want them, and the stretch nylon breathes on hot days. On a budget, the Left of Field wide-leg tech trouser is $60 on sale, the Grind City barrel leg is $72 and the Winslow Simple Pant is $80.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Details</div>
      <div class="sidebar-detail"><span class="l">Pants</span><span>18</span></div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>18</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$60&ndash;~$297</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Students Science Adjustable Pleated Pants</span></div>
      <div class="hashtags">
        <span class="hashtag">#BaggyPants</span>
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
    <h2 class="products-hdr" id="last-word">Wear Them Loose, Wear Them Everywhere</h2>
    <p>The case for a loose pant gets clearer the longer the round goes. By the back nine on a warm day, a slim trouser is stuck to your legs and pulling at the knee every time you mark a ball. A wide leg is still moving air, still hanging straight, and still letting you squat to read a putt without a second thought. That is the whole argument: breathability, flow and room to move, all day.</p>
    <p><strong>Pick the fabric for your weather.</strong> Nylon, ripstop and stretch blends (Students Science, Left of Field, Fella, Twentyfour, Macade, Cph/Golf) are the hot-weather and rainy-day choice: light, quick to dry and easy to pack. Cotton twill and corduroy (Woodgrain, Late Nine, Gramicci, SLOAT, Winslow) feel softer, soften more with every wash, and are better from fall into spring. Linen (Rowena) is the coolest thing you can wear on a humid day. Wool blends (Slice Town) drape the best and hold a crease, the dressiest option here.</p>
    <p><strong>Get the size right.</strong> Most of these run big on purpose. Students sells the Science pant in two sizes because the velcro waist adjusts; Slice Town and Angus &amp; Grace say to size down. If you are between sizes on anything with pleats, go down. Gramicci, Cph/Golf and SLOAT use built-in belts or elastic, so they are the most forgiving.</p>
    <p><strong>Style it so the pant leads.</strong> Keep the top boxy and a little short, a polo, a cropped knit or a quarter-zip, so the volume sits on your legs instead of everywhere. Let the hem break on the shoe or bunch slightly; a chunky spikeless shoe or a classic saddle keeps a wide leg from swallowing your feet. A belt helps, especially with pleats, and a cap or bucket keeps the whole look relaxed.</p>
    <p><strong>Take care of them.</strong> Wash cotton and corduroy cold and hang to dry if you want to keep the length. Nylon pants can go in with your polos. If a pair is too long, a tailor can take up the hem in an afternoon, but leave some break; part of the appeal is the way a wide leg moves when you walk.</p>
    <p>Prices are as each store shows them to a US visitor. A.P.C., Late Nine and Angus &amp; Grace show euros, Swedish kronor and Australian dollars, so those dollar figures are approximate. All 18 were in stock on November 4, 2026. If you have a loose pant you love that we missed, send it our way.</p>
  </div>
</section>
"""
HERO_ALT = "A golfer lying on a putting green reading a book, in loose tan Walker pleated pants"
FRN = json.loads((ROOT / "research/baggy/frames.json").read_text())
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
         "url": URL, "image": og, "datePublished": "2026-11-04", "dateModified": "2026-11-04",
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
            f'  <div class="drop-tag grass">{num:02d} &middot; {len(ids)} pants</div>\n'
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
    <span>The Edit &middot; Loose, wide and barrel-leg</span><span class="dot"></span>
    <span>18 pants &middot; in stock, checked November 4, 2026</span>
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
