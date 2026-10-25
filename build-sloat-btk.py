#!/usr/bin/env python3
"""build-sloat-btk.py — Brand to Know: SLOAT. 21 October 2026. Cloned from build-saha-btk.py.
Lenny: "Let's do a brand to know- https://sloat.cc/" -> options sheet -> "let's build the post and show me the preview" (all 16).
FACTS: sloat.cc products.json (USD, Oct 21 2026; all 16 in stock), About, FAQ, Materials & Factories, Journal (An Ode to the Outerlands; Wear Patterns),
Instagram @sloat.cc; San Francisco Golf launch story (Sep 2 2026). research/sloat/brief.md. Japan production is "being developed" (not claimed).
Patrick Grimes essay deliberately not referenced. Archival RAF image on Wear Patterns not used.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "SLOAT: San Francisco Golf Clothes in Natural Fibers Only"
DESC = ("Brand to Know: SLOAT, a new San Francisco golf brand named for Sloat Boulevard. Organic cotton fleece, merino polos and Ventile outerwear "
        "made in Portugal, hats made in Queens. All 16 pieces, $65 to $595.")
H1 = "Brand to Know: SLOAT"
BC = "SLOAT"
SLUG = "brand-to-know-sloat"
IMG = "/images/sloat"
SHOP = "https://sloat.cc/products/"
P = {
 "v1": ("SLOAT", 'Organic Ventile Jacket', '$595', 'mens-ventile-windbreaker',
   'The big one. Ventile was developed in Britain during the Second World War for RAF pilots: cotton woven so densely that the fibers swell when wet and close up, so it shrugs off wind and rain and still breathes. Two-way YKK zip, snap cuffs, organic cotton lining. Black, charcoal or stone.'),
 "v2": ("SLOAT", 'Organic Ventile Vest', '$345', 'mens-ventile-vest',
   'The same Ventile shell as a vest, cut to go over a polo or a sweatshirt, with a stand collar and snap side tabs. Charcoal, black or stone.'),
 "v3": ("SLOAT", 'Organic Ventile Wind Shirt', '$295', 'mens-ventile-wind-shirt',
   'Our pick of the three. A quarter-zip Ventile pullover with raglan sleeves and a chest pocket, made for walking eighteen in coastal weather. Stone, black or charcoal.'),
 "f1": ("SLOAT", 'Organic Cotton Fleece Quarter Zip', '$225', 'mens-golf-quarter-zip',
   'Heavyweight 480gsm organic cotton fleece with a stand collar, a metal zip and hidden side zip pockets, made to sit over a polo. It&rsquo;s the piece on Christian Dean at Half Moon Bay up top. Four colors.'),
 "f2": ("SLOAT", 'Organic Cotton Fleece Hoodie', '$245', 'mens-organic-cotton-golf-hoodie',
   'The same 480gsm fleece with a jersey-lined hood, a cotton drawcord and a kangaroo pocket. Aluminum, black or navy.'),
 "f3": ("SLOAT", 'Organic Cotton Fleece Crewneck', '$215', 'mens-organic-cotton-golf-crewneck',
   'Dropped shoulders, a brushed inside and a concealed zip pocket, for cold mornings. The Redwood Burl colorway is the rust one on the range below.'),
 "k1": ("SLOAT", 'Merino Polo', '$215', 'mens-merino-wool-golf-polo',
   '200gsm RWS-certified merino jersey, which handles heat, sweat and smell on its own, so it goes a few rounds between washes. Self-fabric collar, side vents. Seed pearl, black or navy.'),
 "k2": ("SLOAT", 'Organic Cotton Jersey Polo', '$155', 'mens-organic-cotton-golf-polo',
   'A classic-fit 170gsm cotton polo with a slightly longer back hem. SLOAT says plainly that it won&rsquo;t wick like a synthetic, which is why they kept it light. Four colors.'),
 "k3": ("SLOAT", 'Organic Cotton T-Shirt', '$85', 'mens-organic-cotton-t-shirt',
   'A relaxed 170gsm tee with raglan sleeves, a bound neckline and side vents. The way in. Navy, seed pearl or stargazer.'),
 "b1": ("SLOAT", 'Organic Cotton Caddie Pant', '$195', 'organic-cotton-caddie-pant',
   'Inspired by &ldquo;the unsung style of the caddie.&rdquo; Heavy 305gsm organic cotton, a straight fit and real drape, in marshmallow.'),
 "b2": ("SLOAT", 'Organic Cotton Day Pant', '$195', 'mens-organic-cotton-golf-pants',
   'Their most casual pant: lighter 195gsm twill, a relaxed fit, an elastic back waistband with belt loops, and articulated knees. Oil green.'),
 "b3": ("SLOAT", 'Organic Cotton Caddie Short', '$145', 'organic-cotton-caddie-short',
   'A traditional flat-front golf short in the heavy 305gsm cotton, so it hangs instead of flapping. Marshmallow.'),
 "b4": ("SLOAT", 'Organic Cotton Golf Short', '$145', 'mens-organic-cotton-golf-shorts',
   'The same flat-front shape in lighter 195gsm cotton that holds a crease all round. Oil green.'),
 "b5": ("SLOAT", 'Organic Cotton Corduroy Short', '$145', 'mens-organic-cotton-corduroy-golf-shorts',
   'Fine-wale corduroy with a pressed crease and a drawcord waist. Navy.'),
 "h1": ("SLOAT", 'Organic Cotton Five Panel Hat', '$65', 'organic-cotton-five-panel-hat',
   'Made in Queens by Winner Caps: organic cotton, a taller front and a leather strap that&rsquo;s meant to patina. Navy, oil green or white.'),
 "h2": ("SLOAT", 'Organic Cotton Six Panel Hat', '$65', 'organic-cotton-six-panel-hat',
   'Their dad hat, with a softer, rounder crown and the same leather strap. White, oil green or navy.'),
}
SECTIONS = [
 ("The Ventile", "ventile", ["v1","v2","v3"],
  "<strong>Three pieces &middot; $295&ndash;$595</strong>Organic Ventile woven in Switzerland, sewn in Portugal, and covered by a lifetime guarantee: if something goes wrong, SLOAT will repair it where it can."),
 ("The Fleece", "fleece", ["f1","f2","f3"],
  "<strong>Three pieces &middot; $215&ndash;$245</strong>Heavyweight 480gsm organic cotton fleece, made in Portugal."),
 ("Polos &amp; the Tee", "polos", ["k1","k2","k3"],
  "<strong>Three pieces &middot; $85&ndash;$215</strong>Merino or organic cotton jersey. No polyester anywhere."),
 ("Trousers &amp; Shorts", "bottoms", ["b1","b2","b3","b4","b5"],
  "<strong>Five pieces &middot; $145&ndash;$195</strong>Two weights of organic cotton and a fine-wale cord, all made in Portugal."),
 ("The Hats", "hats", ["h1","h2"],
  "<strong>Two hats &middot; $65 each</strong>Made in the USA by Winner Caps in Ridgewood, Queens."),
]
N = 16
PQ = {
 "ventile": ("You walked silently &ndash; no synthetic swishing or squeaking betraying your approach. And you know what they say: Bad boys move in silence.", "Patrick Thomas, on Ventile, in SLOAT&rsquo;s Journal"),
 "polos": ("Breathable technical everything is giving microplastic claustrophobia.", "Lauren Goodman, former WSJ Off Duty fashion director, in SLOAT&rsquo;s Journal"),
 "bottoms": ("If you are wearing head to toe Peter Millar in the office on Friday, I am not investing in your fund.", "George ODell, art dealer and &ldquo;aspiring golfer,&rdquo; quoted in SLOAT&rsquo;s Journal"),
 "hats": ("An almost unreasonable attention to details that most people will never consciously notice.", "Dan Fibiger and Teague Moriarty, on what restaurants and clothes have in common"),
}
CAP = "Photography &middot; SLOAT"
BANDS = {
 "fleece": ("In the Outerlands", "SLOAT&rsquo;s own photos from San Francisco&rsquo;s western courses.",
   [("life-4","A golfer in silhouette on a fairway at Golden Gate Park Golf Course","&ldquo;An afternoon at Golden Gate Park Golf Course.&rdquo;"),
    ("life-2","SLOAT co-founder Dan Fibiger holding a yellow flag in a navy quarter zip and white cap","Co-founder Dan Fibiger at Sharp Park, Pacifica"),
    ("life-9","A rust SLOAT crewneck and navy corduroy shorts on a range scattered with balls","The crewneck in Redwood Burl, with the cord short")]),
 "bottoms": ("Launch week", "SLOAT went live on August 28 with a party at Golden Gate Park Golf Course.",
   [("life-10","A white SLOAT pin flag with the orange logo on a green","&ldquo;SLOAT, August 28, 2026. Golden Gate Park Golf Course.&rdquo;"),
    ("life-3","Black-and-white multi-frame swing study at Presidio Golf Course","&ldquo;A study in recovery at Presidio Golf Course.&rdquo;"),
    ("life-14","A laundry line hung with shirts under the SLOAT logo, from the founders&rsquo; trip to Portugal","From the factory trip: &ldquo;surf and golf our way from Lisbon to Porto&rdquo;")]),
}
PROSE = 'style="max-width:760px;font-size:16px;line-height:1.7;margin:0 auto 24px;"'
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>SLOAT is named for Sloat Boulevard, which runs west through San Francisco, past some of the city&rsquo;s best golf courses, until it hits Ocean Beach. The brand went live on August 28 with a party at Golden Gate Park Golf Course, and it already looks like it belongs out there: fog, cypress, cold mornings and a palette the founders say came straight from the sand, dunes, ocean and sky at Ocean Beach.</p>
    <p><strong>The founders aren&rsquo;t golf-industry people, and that&rsquo;s the point.</strong> Dan Fibiger spent nearly 20 years on the sustainability and human-rights side of the apparel business, most recently leading sustainability at Gap Inc. Teague Moriarty is a chef and an owner of Sons &amp; Daughters and Kiln, both two-Michelin-star restaurants in San Francisco. Both surf, and both play the city&rsquo;s public courses. Their opening letter says they have &ldquo;no interest in using sustainability as decoration,&rdquo; and the catalogue backs it up.</p>
    <p><strong>Natural fibers only.</strong> In a sport built on polyester, SLOAT makes everything from GOTS organic cotton, RWS merino and organic Ventile. Three family-run factories in Portugal sew the clothes, and the hats come from Winner Caps in Queens. The Ventile is the standout: a cotton developed for RAF pilots that closes up in the rain and still breathes, made here with a lifetime repair guarantee.</p>
    <p><strong>They tell you the trade-offs.</strong> Their FAQ says cotton won&rsquo;t wick like a synthetic polo and that Ventile is water-resistant, not waterproof. We like a brand that tells you what its clothes won&rsquo;t do. If you play hot, humid golf, start with the merino polo.</p>
    <p><strong>It isn&rsquo;t cheap.</strong> $155 for a cotton polo, $225 for the quarter zip and $595 for the Ventile jacket puts SLOAT at the top end of independent golf. It&rsquo;s 16 pieces, men&rsquo;s only, sold only on sloat.cc, and the brand is eight weeks old, so there isn&rsquo;t much wear-test feedback yet. The way in is a $65 hat or the $85 tee. The piece we&rsquo;d buy is the Ventile Wind Shirt.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>San Francisco</span></div>
      <div class="sidebar-detail"><span class="l">Launched</span><span>Aug 28, 2026</span></div>
      <div class="sidebar-detail"><span class="l">Made in</span><span>Portugal &amp; USA</span></div>
      <div class="sidebar-detail"><span class="l">Fibers</span><span>Natural only</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$65&ndash;$595</span></div>
      <div class="sidebar-detail"><span class="l">In the post</span><span>All 16 pieces</span></div>
      <div class="hashtags">
        <span class="hashtag">#SLOAT</span>
        <span class="hashtag">#SanFranciscoGolf</span>
        <span class="hashtag">#BrandToKnow</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("Who founded SLOAT?", "Dan Fibiger, formerly VP of Global Sustainability at Gap Inc., and Teague Moriarty, a chef and owner of the San Francisco restaurants Sons & Daughters and Kiln. They launched SLOAT in San Francisco on August 28, 2026."),
 ("Where does the name SLOAT come from?", "Sloat Boulevard in San Francisco, which runs west past several of the city's golf courses to the southern end of Ocean Beach."),
 ("Where are SLOAT clothes made?", "The clothes are sewn in Portugal by three family-run factories, and the hats are made in Ridgewood, Queens by Winner Caps. The founders say work in Japan is being developed."),
 ("What is Ventile?", "A densely woven cotton developed in Britain during the Second World War for Royal Air Force pilots. The fibers swell when wet, so it resists wind and rain while staying breathable. SLOAT notes it is water-resistant, not fully waterproof."),
]
_LB = [("life-1","Christian Dean in a cream SLOAT quarter zip and orange-logo cap at Half Moon Bay","Christian Dean at Half Moon Bay&rsquo;s Ocean Course"),
 ("life-6","A golfer in a blue fleece quarter zip holding a driver against a blue sky","The quarter zip, before launch"),
 ("life-7","Black-and-white photo of a golfer in a black hoodie on a coastal course","The hoodie on the coast"),
 ("life-5","Black-and-white silhouette of a golfer at the finish on a fairway","From the Merino Polo post"),
 ("life-11","A weathered TEE 1 sign in coastal dune grass","Tee 1"),
 ("life-15","Cypress trunks over the Pacific","The Outerlands"),
 ("life-13","Black-and-white close-up of irons in a golf bag","Presidio Golf Club, August 2026"),
 ("life-12","A flagstick and ball on a green","Before launch"),
 ("life-8","Black-and-white full-length portrait in a dark jacket and trousers","The jacket, in the studio")]
_figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{a}" loading="lazy" /><figcaption class="ig-cap">{c}</figcaption></figure>' for f, a, c in _LB)
LOOKBOOK = f"""
<section class="products" style="margin-top:8px;">
  <div class="drop-tag grass">Lookbook</div>
  <h2 class="products-hdr" id="lookbook">Out West</h2>
  <p class="cat-kicker"><strong>From SLOAT&rsquo;s feed &middot; nine photos</strong>Half Moon Bay, the Presidio, Golden Gate Park and the coast in between, with SLOAT&rsquo;s captions where they wrote them.</p>
  <div class="ig-grid">
{_figs}
  </div>
</section>
"""

FRN = json.loads((ROOT / "research/sloat/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-R3-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
def card(k, idx):
    brand, item, price, handle, copy = P[k]
    url = SHOP + handle
    fr = FRN[P[k][3]]
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
         "url": URL, "image": og, "datePublished": "2026-10-21", "dateModified": "2026-10-21",
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
        assert FRN[P[k][3]] and all((ROOT / f.lstrip("/")).is_file() for f in FRN[P[k][3]]), k
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
    <span>Brand to Know &middot; San Francisco &middot; Launched August 28, 2026</span><span class="dot"></span>
    <span>All 16 pieces &middot; prices checked October 21, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Christian Dean smiling in a cream SLOAT fleece quarter zip over an olive polo and a SLOAT cap at Half Moon Bay&rsquo;s Ocean Course, from SLOAT&rsquo;s Instagram" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
    body += LOOKBOOK
    body += faq_html()
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Kalamunda", "Parmore", "Sounder", "Casualist", "BUNX", "Long Iron", "Dim Sum", "Rowena", "Metalwood", "Climber", "Woodgrain", "Rookline", "Bethpage", "LBB", "GolfPass"):
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
