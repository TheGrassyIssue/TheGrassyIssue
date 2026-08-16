#!/usr/bin/env python3
# Brand Revisited — Casualist. Upgrades /drops/brand-to-know-casualist.html in place.
import re, json, os

S = os.path.dirname(os.path.abspath(__file__))
BASE = open(os.path.join(S, "drops/the-payntr-collab-edit.html"), encoding="utf-8").read()
IMGDIR = os.path.join(S, "images/casualist")
META = json.load(open("/tmp/cas/meta.json"))

TITLE = "Casualist — The London Brand That Outgrew Its Own Name"
SLUG = "brand-to-know-casualist"
DESC = ("Casualist started as Casual Pro in 2023 and renamed itself. Elie Reboul's West London "
        "brand designs in London, makes in Portugal, and sells everything from a £38 snapback "
        "with the old logo still on it to a £12,000 electric golf cart.")

COPY = {
"casual-pro-snapback-leisure-hats":("Archive","Casual Pro Snapback, Leisure Hats OG","&pound;38","The oldest thing in the catalogue and still the best seller. The old name is embroidered on the front along with SINCE 2023, LEISURE APPAREL and MELB &ndash; LDN &ndash; LA. 100% recycled quick-dry nylon, five colourways, made to order and shipped in about a week. Restocked this month."),
"windbreaker-coach-jacket-archive":("Archive","Windbreaker Coach Jacket","&pound;89","Navy, with CASUAL PRO across the back in block type. Listed under Archive, which is the only place the old name survives at full size."),
"ball-marker":("Archive","Ball Marker","&pound;15","An eight-point black star with a single eye at the centre. The brand mark, in enamel, for the price of two pints."),
"trust-the-swing-pique-polo":("Polos","Trust the Swing Pique Polo","&pound;115","Cotton pique with a soft unstructured collar. Olive and dusty blue. The polo the brand is built around, and the one that best explains the whole thing: no logo you can read from the fairway."),
"weekend-pique-polo":("Polos","Weekend Pique Polo","&pound;95","The long-sleeve version in ecru and mocha. Same pique, more coverage, and it passes for a normal shirt off the course."),
"dress-code-mockneck-tee":("Polos","Dress Code Mockneck Tee","&pound;85","A mockneck in place of a collar, which solves the clubhouse dress code without looking like it is solving anything. Dusty blue and ecru."),
"no-idea-heavy-tee-organic-cotton":("Tees","No Idea Heavy Tee","&pound;65","Organic cotton, heavyweight, with an illustrated back print. Casualist's sense of humour is dry and it lives mostly on the tees."),
"good-enough-tee":("Tees","Good Enough Tee","&pound;65","Ecru, chest wordmark, nothing else. The plainest thing they make."),
"all-the-gear-sweatshirt":("Layers","All The Gear Sweatshirt","&pound;120","Mushroom brown with ALL THE GEAR NO IDEA scripted across the back. Self-deprecation is the house tone and this is the clearest statement of it."),
"grazer-cardigan-vest":("Layers","Grazer Cardigan Vest","&pound;185","Grey knit, button front, patch pockets. This is the piece from the about page &mdash; the proper cardigan on a drizzly Tuesday morning, meant sincerely."),
"cart-path-ripstop-jacket":("Layers","Cart Path Ripstop Jacket","&pound;240","Olive ripstop, quarter-zip, chest pocket, C logo at the heart. The most expensive garment they sell and the one that looks best in their own photography."),
"pleated-golf-trousers-organic-co":("Bottoms","Pleated Golf Trousers","&pound;160","Organic cotton, single pleat, wide through the leg. Cut closer to a trouser than a golf pant, which is the entire point."),
"legacy-wool-5-panel-cap":("Headwear","Legacy Wool 5 Panel Cap","&pound;45","Herringbone wool with the C mark. Winter weight."),
"legacy-velvet-5-panel-cap":("Headwear","Legacy Velvet 5 Panel Cap","&pound;45","The velvet version. Odd on paper, good in person."),
"casual-5-panels-ripstop-cap":("Headwear","Casual 5 Panels Ripstop Cap","&pound;45","Ripstop, olive and yellow, script wordmark across the front panel."),
"two-tone-course-cap":("Headwear","Two Tone Course Cap","&pound;45","Cream crown, olive brim, Casualist Leisure Goods West London stacked on the front. The one that names the postcode."),
"beach-rover":("The Cart","Beach Rover","&pound;12,000","Soft cream with a yellow striped canopy and an electric drive. Their own copy calls it &ldquo;handsome, unhurried, and built for people who take the game seriously but not themselves,&rdquo; and asks you to enquire for specifications and delivery. Sold out. A seventeen-product apparel brand listing a twelve-thousand-pound vehicle is the most Casualist thing on this page."),
}

SECTIONS = [
 ("The Casual Pro Years", ["casual-pro-snapback-leisure-hats","windbreaker-coach-jacket-archive","ball-marker"]),
 ("Polos and Mocknecks", ["trust-the-swing-pique-polo","weekend-pique-polo","dress-code-mockneck-tee"]),
 ("Tees", ["no-idea-heavy-tee-organic-cotton","good-enough-tee"]),
 ("Layers", ["all-the-gear-sweatshirt","grazer-cardigan-vest","cart-path-ripstop-jacket"]),
 ("Bottoms", ["pleated-golf-trousers-organic-co"]),
 ("Headwear", ["legacy-wool-5-panel-cap","legacy-velvet-5-panel-cap","casual-5-panels-ripstop-cap","two-tone-course-cap"]),
 ("And Then There Is the Cart", ["beach-rover"]),
]

FAQ = [
 ("Who founded Casualist?",
  "Elie Reboul. The about page on their site is signed simply &ldquo;Elie, Founder.&rdquo;"),
 ("Was Casualist always called Casualist?",
  "No. It started as Casual Pro. In the brand's words: &ldquo;The spirit was right, but the name needed to grow up a little.&rdquo; The original Casual Pro snapback is still sold, still the best seller, and still carries the old logo."),
 ("Where is Casualist based?",
  "West London. Their Two Tone Course Cap has &ldquo;Casualist Leisure Goods West London&rdquo; embroidered on the front, and the Casual Pro snapback reads MELB &ndash; LDN &ndash; LA."),
 ("Where is Casualist made?",
  "Designed in London, and most pieces are made in Portugal. Their stated reason for the fabrics they choose is how they feel after a full round rather than how they photograph."),
 ("What currency does Casualist sell in?",
  "British pounds. Prices on this page are the GBP figures from their own store, not converted."),
 ("What does Casualist sell?",
  "Seventeen products: polos, mockneck and heavyweight tees, a sweatshirt, a cardigan vest, a ripstop jacket, pleated trousers, four caps, a ball marker, and an electric golf cart."),
 ("Is the Beach Rover real?",
  "It is listed on their store at &pound;12,000 with a soft cream finish, striped canopy and electric drive, and the listing asks you to enquire for full specifications and delivery. It is currently sold out."),
 ("What is the cheapest thing Casualist makes?",
  "The ball marker at &pound;15, followed by the Casual Pro snapback at &pound;38 and the caps at &pound;45."),
]

def imgs(slug):
    n = len([f for f in os.listdir(IMGDIR) if f.startswith(slug + "-") and f[len(slug)+1].isdigit()])
    return [f"/images/casualist/{slug}-{i+1}.jpg" for i in range(n)]

def card(slug):
    m = META[slug]; sect, name, price, blurb = COPY[slug]
    ims = imgs(slug)
    alt = re.sub(r"&\w+;|&#\d+;", " ", "Casualist " + name).strip()
    frames = "".join(f'<div class="pg-frame"><img src="{u}" alt="{alt} &middot; view {i+1} of {len(ims)}" loading="lazy" /></div>'
                     for i, u in enumerate(ims))
    dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" aria-label="View image {i+1}"></button>'
                   for i in range(len(ims))) if len(ims) > 1 else ""
    nav = ('<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
           '<button class="pg-arw next" aria-label="Next image">&#8250;</button>') if len(ims) > 1 else ""
    count = f'<span class="pg-count">1/{len(ims)}</span>' if len(ims) > 1 else ""
    so = ' <span class="so">&middot; Sold out</span>' if not m["avail"] else ""
    return f"""
    <div class="product-card" data-frames="{len(ims)}">
      <div class="product-gallery">
        <div class="pg-track">{frames}</div>
        {nav}{count}
        <div class="pg-dots">{dots}</div>
      </div>
      <div class="product-body">
        <div class="product-brand">Casualist</div>
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
OLDT = "The PAYNTR Collab Edit &mdash; 33 Shoes, Bags and Odds From Golf&rsquo;s Busiest Collaborator"
for old in [OLDT, "The PAYNTR Collab Edit — 33 Shoes, Bags and Odds From Golf's Busiest Collaborator"]:
    h = h.replace(old + " &mdash; The Grassy Issue", TITLE + " &mdash; The Grassy Issue")
    h = h.replace(old + " — The Grassy Issue", TITLE + " — The Grassy Issue")
    h = h.replace(old, TITLE)
h = h.replace("the-payntr-collab-edit", SLUG)
for k in ["description", "og:description", "twitter:description"]:
    h = re.sub(r'(<meta (?:name|property)="%s" content=")[^"]*(")' % re.escape(k),
               lambda m: m.group(1) + DESC + m.group(2), h)

def fix_article(m):
    d = json.loads(m.group(1))
    d["headline"] = TITLE; d["description"] = DESC
    d["url"] = f"https://thegrassyissue.com/drops/{SLUG}"
    d["datePublished"] = "2026-05-28"; d["dateModified"] = "2026-08-14"
    d["mainEntityOfPage"] = {"@type": "WebPage", "@id": f"https://thegrassyissue.com/drops/{SLUG}"}
    return '<script type="application/ld+json">\n' + json.dumps(d, indent=2) + '\n</script>'
h = re.sub(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', fix_article, h, count=1, flags=re.S)

faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":re.sub(r"&\w+;|&#\d+;"," ",q),
   "acceptedAnswer":{"@type":"Answer","text":re.sub(r"&\w+;|&#\d+;"," ",a)}} for q,a in FAQ]}
_blk = '<script type="application/ld+json">\n' + json.dumps(faq_ld, indent=2) + '\n</script>'
h = re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "FAQPage".*?</script>',
           lambda m: _blk, h, count=1, flags=re.S)

h = h.replace('<span class="drop-tag grass">[The Edit]</span>', '<span class="drop-tag grass">[Brand Revisited]</span>')
h = h.replace('<a href="/#feed">The Edit</a>', '<a href="/#feed">Brand Revisited</a>')
h = re.sub(r'<div class="drop-hero">.*?</div></div>',
  '<div class="drop-hero"><div class="drop-hero-img"><img src="/images/casualist/hero.jpg" '
  'alt="Casualist Beach Rover golf cart parked on a links course under a grey sky" /></div></div>',
  h, count=1, flags=re.S)

writeup = """<div class="writeup">
  <div class="writeup-body">
    <p>The best-selling item Casualist makes has the wrong name on it. The Casual Pro Snapback is the oldest thing in the catalogue, it restocked this month, and stitched across the front is CASUAL PRO, SINCE 2023, LEISURE APPAREL, MELB &ndash; LDN &ndash; LA. That was the brand before this one.</p>
    <p>Elie Reboul renamed it. His explanation, on the about page, is two sentences long: the spirit was right, but the name needed to grow up a little. Casualist is the version with sharper details and a clearer point of view. What he did not do is retire the old hat, and the archive section still sells a navy coach jacket with CASUAL PRO in block type across the back.</p>
    <p>The brand is West London. It says so on the Two Tone Course Cap, under the words Leisure Goods. Everything is designed there and most of it is made in Portugal, with fabric chosen for how it feels after eighteen holes rather than how it reads on a screen. The test they apply to anything before making it is whether they would wear it properly and repeatedly, not once and not for the photos.</p>
    <p>Seventeen products. Polos with collars soft enough to pack, tees that carry the jokes, a cardigan vest meant sincerely for a drizzly Tuesday, pleated trousers cut closer to trousers than to golf pants. And, at the bottom of the catalogue, a &pound;12,000 electric golf cart in cream with a striped canopy.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Founder</span><span>Elie Reboul</span></div>
      <div class="sidebar-detail"><span class="l">Based</span><span>West London</span></div>
      <div class="sidebar-detail"><span class="l">Made</span><span>Portugal</span></div>
      <div class="sidebar-detail"><span class="l">Was</span><span>Casual Pro, 2023</span></div>
      <div class="sidebar-detail"><span class="l">Prices</span><span>GBP</span></div>
      <a href="https://casualist.com" target="_blank" rel="noopener" class="sidebar-cta">casualist.com &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#TheGrassyIssue</span>
        <span class="hashtag">#GolfCulture</span>
        <span class="hashtag">#BrandRevisited</span>
        <span class="hashtag">#Casualist</span>
      </div>
    </div>
  </aside>
</div>"""
h = re.sub(r'<div class="writeup">.*?</aside>\s*</div>', writeup, h, count=1, flags=re.S)
h = h.replace("<span>33 Pieces</span>", "<span>17 Pieces</span>")

start = h.find('<section class="products">')
end = h.find('<section class="more"')
if end == -1: end = h.find('<div class="more"')
assert start != -1 and end != -1 and end > start
h = h[:start] + '<section class="products">\n' + grid + faq_html + '</section>\n\n' + h[end:]

out = os.path.join(S, f"drops/{SLUG}.html")
open(out, "w", encoding="utf-8").write(h)
print("wrote", out, len(h), "bytes")
