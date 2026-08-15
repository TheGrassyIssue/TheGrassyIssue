#!/usr/bin/env python3
# Builds /drops/the-payntr-collab-edit.html
import re, json, os

S = os.path.dirname(os.path.abspath(__file__))
BASE = open(os.path.join(S, "drops/brand-to-know-sugarloaf-social-club.html"), encoding="utf-8").read()
IMGDIR = os.path.join(S, "images/payntr")
META = json.load(open("/tmp/payntr/meta.json"))

TITLE = "The PAYNTR Collab Edit — 33 Shoes, Bags and Odds From Golf's Busiest Collaborator"
SLUG = "the-payntr-collab-edit"
DESC = ("PAYNTR Golf has done 25 collaborations with 11 brands, and 13 of them landed in the last "
        "72 days. Students, Sugarloaf Social Club, Jones, Vessel, Bad Birdie, Ghost Golf, Khalhon "
        "and more, plus every accessory PAYNTR makes under its own name.")

# slug: (partner label, display name, blurb)
COPY = {
"students-wt":("Students Golf","Students by PAYNTR WT","White and green with a pebbled saddle, COURSE STUDIES DIVISION stamped along the midsole and STUDENTS printed across a translucent outsole. Seventeen days on sale and gone."),
"students-pt":("Students Golf","Students by PAYNTR PT","The tan colorway of the same shoe. Same outsole treatment, warmer palette, also sold out."),
"ssc-87":("Sugarloaf Social Club","SSC Eighty Seven","The Eighty Seven is PAYNTR's signature silhouette and this is the version people still ask about. Red outsole graphics under a white upper."),
"ssc-slides":("Sugarloaf Social Club","SSC x PAYNTR Summer Slides","Cream slides for the walk from the eighteenth to the car. $50 and long gone."),
"ssc-hat":("Sugarloaf Social Club","SSC x PAYNTR Rope Hat","White five-panel with a rope brim. The cheapest way into a collab that mostly sold through."),
"ssc-vest":("Sugarloaf Social Club","SSC x PAYNTR Tech Vest","Navy, full-zip, minimal branding. Still in stock, which makes it the outlier in this section."),
"ssc-windshirt":("Sugarloaf Social Club","SSC x PAYNTR Windshirt","Cream, cropped, quarter-zip. Reads more track jacket than golf outerwear."),
"ssc-hoody":("Sugarloaf Social Club","SSC x PAYNTR Tech Hoody","Bright red, which is not a color either brand uses much. That's the point of a collab."),
"jones-rs":("Jones Sports Co","Jones RS by PAYNTR","The first Jones shoe, $200, sold out. Jones has been making bags since 1971 and this was their first go at footwear."),
"jones-slide":("Jones Sports Co","Jones x PAYNTR Slide","Black slide with the Jones mark. $55, in stock, the easiest entry point on this whole page."),
"jones-bag":("Jones Sports Co","PAYNTR x Original Jones Bag","A brown canvas Original Jones carry bag with PAYNTR's X mark on the panel. Two heritage-minded brands doing the obvious thing well. $200."),
"jones-dualbag":("Jones Sports Co","PAYNTR x Jones Dual Shoe Bag","Black, holds two pairs, gone."),
"jones-shoebag":("Jones Sports Co","PAYNTR x Jones Shoe Bag","The single-pair version that came first. $65, sold out."),
"khalhon-ff":("Khalhon","PAYNTR x Khalhon FF","Khalhon is the quietest partner here and got the longest run of product. This is the shoe, $250, still available."),
"khalhon-cap":("Khalhon","PAYNTR x Khalhon Corduroy Cap","$30 for a corduroy six-panel. The best value item PAYNTR has attached its name to."),
"khalhon-polo":("Khalhon","PAYNTR x Khalhon Refined Polo","Shot on-model against a grey seamless, which is the only time PAYNTR breaks from product-on-white."),
"badbirdie-splatter":("Bad Birdie","Bad Birdie x PAYNTR Paint Splatter SL","Confetti splatter across the outsole under a plain white upper. All the noise underneath, which is a recurring PAYNTR trick."),
"badbirdie-america":("Bad Birdie","Bad Birdie x PAYNTR AMERICA SL","The July release. Both Bad Birdie shoes sold out and neither came back."),
"vessel":("Vessel","VESSEL x PAYNTR SL Limited Edition","Eight days old at the time of writing. White and navy, and the newest thing in this entire archive."),
"ghost":("Ghost Golf","Ghost Golf Reaper SL","Black upper, red outsole detailing. Ghost is a smaller partner than most on this list and got one of the better-looking shoes."),
"forresters":("Forresters","FO Rainshedder&reg; RS1","Black and cream with FORRESTERS printed across the tread. A waterproof build, $220, sold out."),
"parxdesign":("Par x Design","Gators x Par x Design","Not a product. It's a framed print documenting the Gators collab, listed at $0 and marked sold out. An odd artifact and the most interesting thing in the archive for exactly that reason."),
"movingday":("PAYNTR Golf","Moving Day SC RS Gator &ldquo;Ghost Gray&rdquo;","The house Gator model the Par x Design print was built around. $200, in stock."),
"matchstick":("Matchstick Golf","PAYNTR x Matchstick Ball Marker","$20, two runs, both gone. The smallest object either brand has made."),
"delcampo":("Del Campo","Del Campo by PAYNTR Quarter Sock","A white quarter sock with a smiley on one and the X on the other. $18, and the cheapest collab PAYNTR has done."),
"acc-headcover":("PAYNTR Golf","X Driver Headcover 001","Black with the X mark. PAYNTR's own accessories are plainer than anything they do with partners."),
"acc-mallet":("PAYNTR Golf","X Mallet Putter Cover","$40, magnetic closure, no graphics beyond the mark."),
"acc-blade":("PAYNTR Golf","X Blade Putter Cover","The blade version at the same price."),
"acc-glove":("PAYNTR Golf","X Glove 001 Regular LH","$29 cabretta. Gloves are the category where PAYNTR's footwear-first background shows least."),
"acc-sock-wool":("PAYNTR Golf","X No Show Tab, Wool","Merino no-show with a heel tab. $20."),
"acc-sock-3pk":("PAYNTR Golf","X No Show Tab, 3 Pack","$40 for three, which is the sensible way to buy them."),
"acc-beanie":("PAYNTR Golf","Bobble X Beanie","$14.50. The cheapest thing PAYNTR sells and a leftover from the cricket side of the business."),
"acc-slide":("PAYNTR Golf","X Slide Leather","Leather recovery slide, $50, no partner branding."),
}

SECTIONS = [
 ("Students Golf", ["students-wt","students-pt"]),
 ("Sugarloaf Social Club", ["ssc-87","ssc-slides","ssc-hat","ssc-vest","ssc-windshirt","ssc-hoody"]),
 ("Jones Sports Co", ["jones-rs","jones-slide","jones-bag","jones-dualbag","jones-shoebag"]),
 ("Khalhon", ["khalhon-ff","khalhon-cap","khalhon-polo"]),
 ("Bad Birdie", ["badbirdie-splatter","badbirdie-america"]),
 ("The One-Offs", ["vessel","ghost","forresters","parxdesign","movingday","matchstick","delcampo"]),
 ("What PAYNTR Makes On Its Own", ["acc-headcover","acc-mallet","acc-blade","acc-glove","acc-sock-wool","acc-sock-3pk","acc-beanie","acc-slide"]),
]

FAQ = [
 ("Who founded PAYNTR?",
  "David Paynter, a former professional cricketer and the great-grandson of England Ashes batsman Eddie Paynter. He started the Payntr brand in 2017 making cricket footwear, then extended it into golf."),
 ("Where is PAYNTR Golf based?",
  "Portland, Oregon. The golf side was co-founded with Mike Forsey and Michael Glancy Jr. Forsey has more than thirty years in performance footwear, and PAYNTR's own site credits Glancy with numerous footwear design and utility patents and signature models for well-known athletes."),
 ("How many collaborations has PAYNTR done?",
  "Twenty-five that are still listed, across eleven partners: Sugarloaf Social Club, Jones Sports Co, Khalhon, Bad Birdie, Students Golf, Vessel, Ghost Golf, Forresters, Par x Design, Matchstick Golf and Del Campo."),
 ("Which PAYNTR collab is the newest?",
  "The VESSEL x PAYNTR SL Limited Edition, released in early August 2026 at $240."),
 ("Why are so many PAYNTR collabs sold out?",
  "The pace. Thirteen of the twenty-five released in the last seventy-two days, most in small runs. Both Bad Birdie shoes, both Students colorways, the SSC Eighty Seven and the Jones RS all sold through without restocking."),
 ("What is the cheapest PAYNTR collaboration?",
  "The Del Campo quarter sock at $18, followed by the Matchstick ball marker at $20 and the Khalhon corduroy cap at $30."),
 ("Does PAYNTR make anything besides shoes?",
  "Yes. Under its own name it sells driver headcovers, blade and mallet putter covers, cabretta gloves, merino no-show socks, beanies and a leather recovery slide, from $14.50 to $50."),
 ("Does PAYNTR do anything for the environment?",
  "Their site states that one tree is planted for every pair sold."),
]

def imgs(slug):
    n = len([f for f in os.listdir(IMGDIR) if f.startswith(slug + "-") and f[len(slug)+1].isdigit()])
    return [f"/images/payntr/{slug}-{i+1}.jpg" for i in range(n)]

def card(slug):
    m = META[slug]; partner, name, blurb = COPY[slug]
    ims = imgs(slug)
    alt = re.sub(r"&\w+;|&#\d+;", " ", f"{partner} {name}").strip()
    frames = "".join(f'<div class="pg-frame"><img src="{u}" alt="{alt} &middot; view {i+1} of {len(ims)}" loading="lazy" /></div>'
                     for i, u in enumerate(ims))
    dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" aria-label="View image {i+1}"></button>'
                   for i in range(len(ims))) if len(ims) > 1 else ""
    nav = ('<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
           '<button class="pg-arw next" aria-label="Next image">&#8250;</button>') if len(ims) > 1 else ""
    count = f'<span class="pg-count">1/{len(ims)}</span>' if len(ims) > 1 else ""
    so = ' <span class="so">&middot; Sold out</span>' if not m["avail"] else ""
    p = m["price"]
    price = "&mdash;" if p == 0 else ("$" + (str(int(p)) if p == int(p) else f"{p:.2f}"))
    return f"""
    <div class="product-card" data-frames="{len(ims)}">
      <div class="product-gallery">
        <div class="pg-track">{frames}</div>
        {nav}{count}
        <div class="pg-dots">{dots}</div>
      </div>
      <div class="product-body">
        <div class="product-brand">{partner}</div>
        <div class="product-name">{name} &middot; {price}{so}</div>
        <div class="product-desc">{blurb}</div>
        <a href="{m['url']}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a>
      </div>
    </div>"""

grid = ""
for hdr, slugs in SECTIONS:
    grid += f'\n  <h2 class="products-hdr sec">{hdr}</h2>\n  <div class="products-grid">'
    grid += "".join(card(s) for s in slugs if s in META)
    grid += "\n  </div>\n"

faq_html = '\n  <h2 class="products-hdr sec">Questions</h2>\n  <div class="faq">' + "".join(
    f'\n    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ) + "\n  </div>\n"

h = BASE
OLD = "Sugarloaf Social Club &mdash; The Group Chat That Became a Golf Brand"
OLD2 = "Sugarloaf Social Club — The Group Chat That Became a Golf Brand"
h = h.replace(OLD + " &mdash; The Grassy Issue", TITLE + " &mdash; The Grassy Issue")
h = h.replace(OLD2 + " — The Grassy Issue", TITLE + " — The Grassy Issue")
h = h.replace(OLD, TITLE).replace(OLD2, TITLE)
h = h.replace("brand-to-know-sugarloaf-social-club", SLUG)
for k in ["description", "og:description", "twitter:description"]:
    h = re.sub(r'(<meta (?:name|property)="%s" content=")[^"]*(")' % re.escape(k),
               lambda m: m.group(1) + DESC + m.group(2), h)

def fix_article(m):
    d = json.loads(m.group(1))
    d["headline"] = TITLE; d["description"] = DESC
    d["url"] = f"https://thegrassyissue.com/drops/{SLUG}"
    d["datePublished"] = "2026-08-14"; d["dateModified"] = "2026-08-14"
    d["mainEntityOfPage"] = {"@type": "WebPage", "@id": f"https://thegrassyissue.com/drops/{SLUG}"}
    return '<script type="application/ld+json">\n' + json.dumps(d, indent=2) + '\n</script>'
h = re.sub(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', fix_article, h, count=1, flags=re.S)

faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":re.sub(r"&\w+;|&#\d+;"," ",q),
   "acceptedAnswer":{"@type":"Answer","text":re.sub(r"&\w+;|&#\d+;"," ",a)}} for q,a in FAQ]}
_blk = '<script type="application/ld+json">\n' + json.dumps(faq_ld, indent=2) + '\n</script>'
h = re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "FAQPage".*?</script>',
           lambda m: _blk, h, count=1, flags=re.S)

h = h.replace('<span class="drop-tag grass">[Brand to Know]</span>', '<span class="drop-tag grass">[The Edit]</span>')
h = h.replace('<a href="/#feed">Brand to Know</a>', '<a href="/#feed">The Edit</a>')
h = re.sub(r'<div class="drop-hero">.*?</div></div>',
  '<div class="drop-hero"><div class="drop-hero-img"><img src="/images/payntr/hero.jpg" '
  'alt="Students by PAYNTR golf shoe with STUDENTS printed across the translucent outsole" /></div></div>',
  h, count=1, flags=re.S)

writeup = """<div class="writeup">
  <div class="writeup-body">
    <p>Look at the bottom of a PAYNTR collab and you will find the partner's name printed across the outsole. Not a logo on the tongue, not a hangtag. The tread. Turn over the Students shoe and STUDENTS reads through translucent rubber; the Forresters shoe says FORRESTERS across the same panel. It is a small decision and it explains why these things sell out, because the branding is invisible until somebody is standing behind you on a tee box.</p>
    <p>PAYNTR has now done twenty-five collaborations with eleven brands. Thirteen of them landed in the last seventy-two days. The previous twelve are spread across the nineteen months before that, so the pace has roughly quadrupled this summer and nobody in the independent golf press has said so.</p>
    <p>The brand comes from cricket. David Paynter played professionally, is the great-grandson of England Ashes batsman Eddie Paynter, and started the label in 2017 because cricket footwear was bad. Golf came later, run out of Portland, Oregon with Mike Forsey and Michael Glancy Jr., two people with long careers in performance footwear before this. That background is why the shoes are competent and why the graphics live where they do.</p>
    <p>Everything below is catalogued: every partner, every piece still listed, what it cost and whether you can still buy it. Six of the eleven partners are brands we already cover. At the end is the stuff PAYNTR makes under its own name, which is notably plainer than anything it makes with somebody else.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Collabs</span><span>25</span></div>
      <div class="sidebar-detail"><span class="l">Partners</span><span>11</span></div>
      <div class="sidebar-detail"><span class="l">Since</span><span>2017 &middot; golf later</span></div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Portland, OR</span></div>
      <a href="https://payntrgolf.com" target="_blank" rel="noopener" class="sidebar-cta">payntrgolf.com &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#TheGrassyIssue</span>
        <span class="hashtag">#GolfCulture</span>
        <span class="hashtag">#GearEdit</span>
        <span class="hashtag">#PAYNTR</span>
      </div>
    </div>
  </aside>
</div>"""
h = re.sub(r'<div class="writeup">.*?</aside>\s*</div>', writeup, h, count=1, flags=re.S)
h = h.replace("<span>33 Projects</span>", "<span>33 Pieces</span>")

start = h.find('<section class="products">')
end = h.find('<section class="more"')
if end == -1: end = h.find('<div class="more"')
assert start != -1 and end != -1 and end > start
h = h[:start] + '<section class="products">\n' + grid + faq_html + '</section>\n\n' + h[end:]

out = os.path.join(S, f"drops/{SLUG}.html")
open(out, "w", encoding="utf-8").write(h)
print("wrote", out, len(h), "bytes")
