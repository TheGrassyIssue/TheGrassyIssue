#!/usr/bin/env python3
"""build-dualsport-btk.py — Brand to Know: Dual Sport, 16 October 2026.
Lenny: "lets do a brand to know - https://dualsportbrand.com/", then picks: the 17 REC plus "add 9, 16,21,25,28,36 and 37".
FACTS (research/dualsport/sources.md): brand About page (quoted verbatim), stockists page, Shopify catalogue (prices + stock 16 Oct);
founder facts from his Grass League player page, Amateur Golf Podcast ep. 70 (Aug 2024) and The First Call (May 2025).
"All-American" appears only in his own league bio, so the page says "former Kennesaw State linebacker". No verbatim founder
interview exists, so pull quotes are the brand's own words. PHOTOS: Dual Sport's own (research/dualsport/frame.py); no founder portrait.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Brand to Know: Dual Sport, Golf Clothes From a Kennesaw State Linebacker Who Plays Off Plus Five"
DESC = ("Brand to Know: Dual Sport. Evan Thompson played football and golf at Kennesaw State, then built a brand for athletes who play "
        "more than one sport. Knit polos, boxy windbreakers, a football jersey and 24 pieces from $6.")
H1 = "Brand to Know: Dual Sport &mdash; Golf Clothes for the Two-Sport Athlete"
BC = "Dual Sport"
SLUG = "brand-to-know-dual-sport"
IMG = "/images/dualsport"
PK = json.loads((ROOT / "research/dualsport/picks.json").read_text())
SOLD = set()
NAME = {"flightknitpololightgre": "Flight Knit Polo", "diamondbladepologreen": "Diamond Blade Polo", "iconpoloelectricblue": "Icon Polo",
        "iconpologalaxy": "Icon Polo, Galaxy 2.0", "signaturepolodarkflora": "Signature Polo, Midnight Bloom", "elitewindbreaker": "Elite Windbreaker",
        "pursuitwindbreakerblac": "Pursuit Windbreaker", "cloudperformancequarte": "Cloud Performance Quarter Zip", "shiverquarterzipmist": "Shiver Quarter Zip",
        "knitjersey": "Classic Knit Jersey", "voltknitvest": "Volt Knit Vest", "pursuitshortselectricb": "Pursuit Shorts", "motionpantsblack": "Motion Pants",
        "motionshortsplatinumgr": "Motion Shorts", "archathleticclubhatwhi": "Arch Athletic Club Hat", "dscamohat": "DS Camo Hat",
        "dualathleticclubhatgre": "Dual Athletic Club Hat", "vintagedsclassicunstru": "Vintage DS Classic Unstructured Hat",
        "dualdriverheadcover": "Driver Cover", "dualmalletcover": "Mallet Cover", "thegraytshirt1": "2 Sport Ball Marker",
        "prodaytshirt": "Pro Day Tee", "ballertshirt": "Baller Tee", "throwbacktshirt": "Throwback Tee"}
def price(d):
    p = float(d["price"]); c = float(d["cmp"] or 0)
    f = lambda x: f"${x:,.0f}"
    return f"{f(p)} (reg. {f(c)})" if c > p else f(p)
COPY = {
 "flightknitpololightgre": "This is the pick of the polos. Dual Sport knits it from a viscose blend with raglan sleeves, a bowling-shirt collar and stripes down the sleeves, and cuts it a little long and relaxed. It comes in light gray, seafoam, black or cream. Hang it dry.",
 "diamondbladepologreen": "A stretch performance polo with a diamond steel-plate pattern on the raglan sleeves and a blade collar, in a slimmer, slightly longer cut. Green or black.",
 "iconpoloelectricblue": "The next-gen Icon keeps the signature paneling, adds a contrast dark gray collar and runs slimmer and longer than before. It comes in electric blue, white or dark gray.",
 "iconpologalaxy": "The same Icon polo in the Galaxy 2.0 print, cut a little shorter and more relaxed, with silicone logos front and back. The loud one.",
 "signaturepolodarkflora": "Dual Sport puts a Midnight Bloom floral panel under a black yoke, and its description opens with the motto: it &ldquo;was designed to be versatile.&rdquo; It is half price, with three sizes left.",
 "elitewindbreaker": "This is the cold-morning layer: a wide, boxy quarter-zip in water-resistant nylon with a mesh lining, mock neck, adjustable hem and zip side pockets.",
 "pursuitwindbreakerblac": "Dual Sport puts short sleeves and a three-panel hood on the same boxy, water-resistant shell. It comes in black, with one size left in electric blue.",
 "cloudperformancequarte": "Dual Sport calls it &ldquo;the softest performance quarter zip you&rsquo;ll own.&rdquo; Nylon, polyester and spandex in a slightly relaxed athletic fit. Gray or black.",
 "shiverquarterzipmist": "Dual Sport makes this nylon-spandex quarter zip with white contrast forearms, and updated the sizing to true to size with a relaxed fit. It comes in mist or black.",
 "knitjersey": "A heavy cotton knit cut like a classic football jersey: raglan paneling, appliqu&eacute; numbers on the shoulders, boxy and oversized. The piece that explains the brand best. Hang it dry.",
 "voltknitvest": "Dual Sport knits this midweight cotton sweater vest with contrast paneling, the DUAL wordmark on the front and a big 2 on the back. Hang it dry.",
 "pursuitshortselectricb": "Water-resistant nylon with a 5.5&Prime; inseam, a wider leg, belt loops and a mesh lining, so they go from the range to the course. Electric blue, sage or black.",
 "motionpantsblack": "Dual Sport calls this its best seller. It sits high on the waist with a straight leg and a slight flare at the cuff, in stretch performance fabric, black or platinum gray.",
 "motionshortsplatinumgr": "Dual Sport cuts the Motion pant down to a 7&Prime; short with a wider athletic leg. It comes in platinum gray, navy or black.",
 "archathleticclubhatwhi": "Dual Sport makes this five-panel performance snapback with a perforated back and 3D embroidery, in white or black, plus an unstructured version.",
 "dscamohat": "Dual Sport stitches the interlocking DS logo in 3D embroidery on military camo cotton, with a mid profile.",
 "dualathleticclubhatgre": "Dual Sport puts its varsity-style Dual Athletic Club wordmark on a five-panel, in green or black.",
 "vintagedsclassicunstru": "Dual Sport puts the vintage DS monogram on an unstructured snapback, in camo, black, or white with a black brim.",
 "dualdriverheadcover": "Made with CMC Designs: black faux leather with DUAL running down the cover in applique embroidery.",
 "dualmalletcover": "The CMC Designs mallet cover, split black and white, with the motto &ldquo;Designed to be versatile&rdquo; on the tongue. Fits most mallets.",
 "thegraytshirt1": "A raised-metal 2 with the Dual logo on the back, enamel filled, by CMC Designs. It was the first product in the store, in May 2024.",
 "prodaytshirt": "A garment-dyed, boxy midweight tee named for the pre-draft pro day, with graphics front and back.",
 "ballertshirt": "Cream, with the Dual Sport number 2 printed on the back like a jersey.",
 "throwbacktshirt": "Dual Sport printed this faded charcoal tee with a 2024 graphic in the brand&rsquo;s first summer.",
}
P = {d["key"]: ("Dual Sport", NAME[d["key"]], price(d), "https://dualsportbrand.com/products/" + d["handle"], COPY[d["key"]]) for d in PK}
ORDER = {
 "polos": ["flightknitpololightgre", "diamondbladepologreen", "iconpoloelectricblue", "iconpologalaxy", "signaturepolodarkflora"],
 "layers": ["knitjersey", "elitewindbreaker", "pursuitwindbreakerblac", "cloudperformancequarte", "shiverquarterzipmist", "voltknitvest"],
 "bottoms": ["motionpantsblack", "pursuitshortselectricb", "motionshortsplatinumgr"],
 "hats": ["archathleticclubhatwhi", "dscamohat", "dualathleticclubhatgre", "vintagedsclassicunstru"],
 "acc": ["dualdriverheadcover", "dualmalletcover", "thegraytshirt1"],
 "tees": ["prodaytshirt", "ballertshirt", "throwbacktshirt"],
}
SEC = [
 ("polos", "The Polos", "<strong>Five polos</strong>Dual Sport builds its polos with raglan sleeves, paneling and contrast collars. The fits run athletic, and the models are tall: one is 6&prime;5&Prime; and wears a medium."),
 ("layers", "The Jersey, Windbreakers and Layers", "<strong>Six layers</strong>The football side shows most here: a knit jersey, a sweater vest with a number on the back, and boxy nylon windbreakers."),
 ("bottoms", "Pants and Shorts", "<strong>Three bottoms</strong>Here are the best-selling pant and two shorts, one nylon, one stretch."),
 ("hats", "Hats", "<strong>Four hats</strong>The hats here are all $38, most of them five-panel snapbacks."),
 ("acc", "Covers and the First Marker", "<strong>Three accessories</strong>All three are made with CMC Designs."),
 ("tees", "The Football Tees", "<strong>Three tees</strong>These graphic tees come from the football side of the brand, and all three are on sale."),
]
SECTIONS = [(h2, a, ORDER[a], k) for a, h2, k in SEC]
N = sum(len(v) for v in ORDER.values())
DATE = "2026-10-16"
PQ = {
 "be": ("If there is one thing Dual Sport will remind you of it&rsquo;s to Be More, Be Versatile, and Be Dual.", "Dual Sport, About page"),
 "layers": ("Dual Sport is a community. A community of those driven for more.", "Dual Sport, About page"),
 "hats": ("Inspiring athletes across the globe that versatility is the ultimate definition of athletic excellence", "Dual Sport&rsquo;s vision"),
 "acc": ("Designed to be versatile.", "The Dual Sport motto, on the wristband and the mallet cover"),
}
BANDS = {
 "course": ("On the Course &middot; Dual Sport&rsquo;s own photos",
  "The brand shoots on the course as much as in the studio: polos and nylon on fairways lined with live oaks.",
  [("life-2", "A golfer in the Midnight Bloom Signature polo and black shorts leaning on an iron beside a pond", "Signature polo, Midnight Bloom"),
   ("life-3", "A golfer in the black Pursuit hooded windbreaker and black pants resting on a driver on the fairway", "Pursuit windbreaker"),
   ("life-4", "A golfer in a black speckled top lining up a putt with the black and white Dual mallet cover", "The mallet cover in play")]),
 "studio": ("In the Studio &middot; Dual Sport&rsquo;s own photos",
  "The football look, up close: numbers on the back, raglan seams and short nylon.",
  [("life-5", "A man seen from behind in the black Classic Knit Jersey with a big 2 on the back", "Classic Knit Jersey"),
   ("life-6", "A man seen from behind in the green Diamond Blade polo with patterned raglan sleeves", "Diamond Blade polo"),
   ("life-7", "A man seen from behind in a black polo and electric blue Pursuit shorts", "Pursuit shorts")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Most golf brands start from the clubhouse. Dual Sport starts from the locker room. The best piece in the range is a heavy cotton knit cut like a football jersey, with numbers on the shoulders. There is a sweater vest with a big 2 on the back, a tee named for the pre-draft pro day, and a silicone wristband that reads &ldquo;Designed to be versatile.&rdquo; Then there are the polos, which are good: the Flight Knit has raglan sleeves and a bowling-shirt collar, and it would look right at a muni or a nice club.</p>
    <p>What makes it work is that the guy behind it lives both sides. Evan Thompson played linebacker <em>and</em> golf at Kennesaw State, and he now plays off plus five. The clothes are cut for that body: the models are 6&prime;5&Prime; and wear a medium, the pants are high waisted, and the windbreakers are wide and boxy. If you came to golf from another sport, or still play one, this is a brand made with you in mind.</p>
    <p>It is also young. The first thing Dual Sport sold was a ball marker in May 2024. Two years later it has a full apparel line, covers made with CMC Designs, and four stockists, two of them close to home for Evan: Clermont National in his Florida hometown, and Grass Clippings in Tempe, home of the Grass League he plays in. Prices sit in the middle of the market, polos at $68 to $78, and the older pieces are on sale.</p>
    <h2 class="products-hdr btk-story-hdr">From the Gridiron to Plus Five</h2>
    <p>Evan Thompson grew up in Clermont, Florida, and played both football and golf in college at Kennesaw State, outside Atlanta. As a golfer he qualified for the U.S. Amateur and has chased U.S. Open qualifying, and in 2026 he joined the Grass League, where he plays for the Scottsdale Strikers. His home course is Pinetree Country Club in Kennesaw.</p>
    <p>He also built one of golf&rsquo;s bigger creator followings, filming rounds with pros and NFL players. By 2024 he had about 250,000 followers on TikTok. In a 2025 podcast, The First Call described content creation as the means, but not the end, of his golf ambitions. Dual Sport came out of the same idea. When he talked about it on The Amateur Golf Podcast in August 2024, the company was described as &ldquo;built to help athletes who play more than one sport.&rdquo;</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>2024</span></div>
      <div class="sidebar-detail"><span class="l">Founder</span><span>Evan Thompson</span></div>
      <div class="sidebar-detail"><span class="l">Roots</span><span>Kennesaw State football + golf</span></div>
      <div class="sidebar-detail"><span class="l">Known for</span><span>Knit polos, the football jersey</span></div>
      <div class="sidebar-detail"><span class="l">Stockists</span><span>AZ, GA, NJ, FL</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$6&ndash;$88</span></div>
      <div class="sidebar-detail"><span class="l">Shipping</span><span>Free in the US over $200</span></div>
      <a href="https://dualsportbrand.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit Dual Sport &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#DualSport</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#BeDual</span>
        <span class="hashtag">#TwoSportAthlete</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
def _mini(a, b):
    return (f'<div><div style="font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;opacity:.55;margin-bottom:6px">{a}</div>'
            f'<div style="font-size:14px;line-height:1.6;opacity:.85">{b}</div></div>')
FOUNDER = f"""
<section class="products" style="border-top:none;padding-top:48px">
  <h2 class="products-hdr" id="in-their-words">In Their Words &mdash; Dual Sport</h2>
  <p class="cat-kicker"><strong>The brand&rsquo;s voice</strong>Dual Sport doesn&rsquo;t tell a founder story on its site. It has a manifesto instead. The lines below are verbatim from its About page.</p>
  <div style="max-width:820px;margin:0 auto;font-size:16px;line-height:1.7">
    <p>&ldquo;Dual Sport is a community. A community of those driven for more. A brand that represents athletes that are designed to be versatile. Our products are made to be worn proudly and to make a difference in your community. Each piece is handcrafted with the ability to bring versatile athletes together all over the world.&rdquo;</p>
    <p style="margin-top:16px">The mission: &ldquo;To create an empowering community of athletes dedicated to going above &amp; beyond the status quo.&rdquo; The values are six words: Commitment, Versatility, Determination, Discipline, Unique, Resilient.</p>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:28px;padding-top:24px;border-top:.5px solid rgba(20,20,20,.15)">
      {_mini("The College Years", "Football and golf at Kennesaw State")}
      {_mini("The Game", "Plays off +5.2; U.S. Amateur qualifier")}
      {_mini("The League", "Grass League, Scottsdale Strikers, 2026")}
    </div>
  </div>
</section>
"""
SPEC = [("Stretch performance", "86% polyester, 14% spandex: the Icon, Diamond Blade and Signature polos"),
        ("Viscose knit", "57% viscose, 43% polyester in the Flight Knit polo. Hang dry to avoid shrinkage"),
        ("Water-resistant nylon", "90% nylon, 10% spandex with a mesh lining: the windbreakers and Pursuit shorts"),
        ("Cloud fabric", "Nylon, polyester and spandex in the quarter zip and hoodie, sold as the softest they make"),
        ("Heavy cotton knit", "100% cotton in the football jersey and the Volt vest. Hang dry these too"),
        ("CMC Designs", "The faux-leather driver and mallet covers and the enamel ball marker")]
def explainer():
    cells = "".join(f'<div style="padding:18px 16px;border:.5px solid rgba(20,20,20,.2)"><div style="font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--grass);margin-bottom:6px">{a}</div><div style="font-size:15px;line-height:1.5">{b}</div></div>' for a, b in SPEC)
    return f"""
<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr" id="what-its-made-of">What It&rsquo;s Made Of</h2>
  <p class="cat-kicker"><strong>The fabrics</strong>Dual Sport lists the fabric and the model&rsquo;s height and size on every product page. Read them: most pieces are cut athletic or relaxed, and the knits shrink if you put them in the dryer.</p>
  <div class="mg-spec" style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;max-width:980px;margin:0 auto">{cells}</div>
</section>
"""
FAQ = [
 ("Who founded Dual Sport?", "Evan Thompson, a former Kennesaw State linebacker who also played golf for the school. He is a plus-handicap amateur, a U.S. Amateur qualifier and a golf content creator, and he plays in the Grass League for the Scottsdale Strikers."),
 ("When did Dual Sport start?", "The brand launched in spring 2024. Its first product was the 2 Sport ball marker, in May 2024. Polos, outerwear and pants followed in 2025 and 2026."),
 ("How much does Dual Sport cost?", "On October 16, 2026, polos were $68 to $78, windbreakers $88, pants $78, shorts $58 to $64 and hats $38, with older pieces on sale. US shipping is free over $200."),
 ("How does Dual Sport fit?", "Athletic to relaxed, and long. Every product page lists the model's height, weight and size. A 6'5\" model wears a medium or large in most polos. The Shiver Quarter Zip was updated to true to size. Hang dry the knits to avoid shrinkage."),
 ("Where can I buy Dual Sport in person?", "Dual Sport lists four stockists: Grass Clippings in Tempe, Arizona; Iron Horse Golf Club in Alpharetta, Georgia; Badlands in Atlantic Highlands, New Jersey; and Clermont National in Clermont, Florida."),
 ("Is Dual Sport only for golf?", "No. The name is the point: the brand is built for athletes who play more than one sport, and the range mixes golf polos with football jerseys, graphic tees and training-style shorts."),
]
FRN = json.loads((ROOT / "research/dualsport/frames.json").read_text())
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
    <span>Kennesaw State roots &middot; est. 2024</span><span class="dot"></span>
    <span>24 pieces &middot; prices checked October 16, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/btk-hero.jpg" alt="Three Dual Sport photos on the course: a golfer in the black Volt knit vest by a sprinkler, three players in Dual Sport windbreakers and shorts shaking hands on a fairway, and a golfer in black Motion pants in front of a white clubhouse" fetchpriority="high" /></div></div>
"""
    body += TAKE
    body += pq("be")
    body += FOUNDER
    body += band("course")
    body += explainer()
    n = 1
    for s, b in zip(SECTIONS, [None, "studio", None, None, None, None]):
        if b: body += band(b)
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
