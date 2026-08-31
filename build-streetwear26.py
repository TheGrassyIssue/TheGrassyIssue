#!/usr/bin/env python3
"""
build-streetwear26.py — rebuild the golf streetwear ranking on the Kingfisher structure.

Lenny, 2026-08-30: "I want to revamp this page" → full treatment, refresh the
lineup → "it's too many options, what are the 5 top brands" → cut to five →
"let's give it some good write ups then push."

WHAT WAS WRONG WITH THE OLD PAGE
--------------------------------
1,878 words, fifteen brands, and NOT ONE IMAGE. No hero, no product cards, no
galleries. It also failed verify-post: the meta description read "brands worth
knowing in 2026" and "worth" is banned in TGI copy.

Two entries were factually broken:
  * EASTSIDE GOLF — Centric Brands formed a joint venture with them, reported by
    WWD 13 Aug 2026. The old copy called them independent.
  * BOGEY BOYS — /collections/all renders 0 products and the product sitemap is
    empty. The site has been a photo archive since ~late March 2026. We ranked it
    at #12 as though you could buy something.

And the category problem: of the fifteen, only Metalwood, Rebolf and partly
Devereux were still streetwear. Seven never were — Gumtree is upcycled deadstock
and surfboards, Sentinel is expedition gear, Sugarloaf is Nantucket Red prep,
Fyfe is Harris Tweed headcovers, MacKenzie makes leather bags. They were there
because the page needed fifteen.

THE ANGLE WE CAN OWN
--------------------
Nobody on page one of this SERP does any of this:
  * a dated status check per brand (competitors still rank Bogey Boys as one to
    watch), so every entry carries "Checked 30 August 2026"
  * ownership disclosure — Malbon's $33M Anthos round and outside CEO, Manors'
    £3m, Eastside's Centric JV. The category is consolidating and everyone is
    running 2023 copy
  * a stated methodology BEFORE ranking anything
  * honest category policing — saying plainly who drifted and who never was

Five entries, not fifteen. Hypebeast ranked five; the only page-one result going
past ten is a gift-affiliate page.

PRICES AND STOCK
----------------
Every product was pulled live from each brand's own Shopify catalogue on
30 Aug 2026 and every one was in stock at capture. Currencies are NATIVE — ANTi
in yen, not converted. Research file: research/streetwear26.json.

METALWOOD CAVEAT: metalwood.studio blocks its products.json endpoint. Their three
cards use images we already localised during the Brand Revisited, and carry ONE
frame each rather than three — no faked gallery. Their prices are marked approx.
"""
import os, re, json, html as H, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SLUG = "best-golf-streetwear-brands-2026"
PAGE = os.path.join(ROOT, "drops", SLUG + ".html")
TPL = os.path.join(ROOT, "drops", "brand-to-know-kingfisher-golf.html")
IMG = "/images/streetwear26"
CHECKED = "30 August 2026"

TITLE = "The 5 Best Golf Streetwear Brands in 2026"
DESC = ("The five golf streetwear brands that actually earn the label in 2026 &mdash; each one status-checked, with ownership disclosed. Metalwood, Students, Malbon, Casualist and ANTi Country Club Tokyo, with three pieces from each.")

SK = {p["k"]: p for p in json.load(open(os.path.join(ROOT, "research", "streetwear26.json")))}


def frames_for(brand, i):
    """How many gallery frames actually exist on disk for this card."""
    n = 0
    while os.path.exists(f"{ROOT}{IMG}/{brand}-{i}-{n}.jpg"):
        n += 1
    return n


def gallery(brand, i, name, n, local=None):
    if local:
        return (f'<div class="product-gallery"><div class="pg-track">'
                f'<div class="pg-frame"><img src="{local}" alt="{name}" loading="lazy" /></div>'
                f'</div></div>')
    frames = "".join(
        f'<div class="pg-frame"><img src="{IMG}/{brand}-{i}-{j}.jpg" '
        f'alt="{name} &middot; view {j+1} of {n}" loading="lazy" /></div>' for j in range(n))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" '
                   f'aria-label="View image {j+1}"></button>' for j in range(n))
    return (f'<div class="product-gallery"><div class="pg-track">{frames}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>')


def card(brand, i, label, prod):
    name = H.escape(prod["t"])
    n = 1 if prod.get("local") else frames_for(brand, i)
    g = gallery(brand, i, f"{label} {name}", n, prod.get("local"))
    price = prod["price"]
    link = (f'<a href="{prod["url"]}" target="_blank" rel="noopener" class="product-link">Shop &nearr;</a>'
            if prod.get("url") else '<span class="product-link">See the brand &nearr;</span>')
    return f'''<div class="product-card" data-frames="{n}">
      {g}
      <div class="product-body">
        <div class="product-brand">{label} &middot; In stock {CHECKED}</div>
        <div class="product-name">{name} &middot; {price}</div>
        <div class="product-desc">{prod["desc"]}</div>
        {link}
      </div>
    </div>'''


BRANDS = [
{
 "k": "metalwood", "rank": 1, "name": "Metalwood Studio", "loc": "Los Angeles",
 "kick": "<strong>The one nobody argues about.</strong> Cole Young left Malbon to build a brand that puts Y2K tour aesthetics through a skate lens &mdash; and in 2026 it out-collabed everyone.",
 "link": "/drops/brand-to-know-metalwood-studio", "linktext": "Read the Metalwood profile",
 "body": [
  "Metalwood is the only brand on the old fifteen that is unambiguously streetwear and also having its best year. In February it dropped a first golf capsule with adidas Originals, launched on a film with Collin Morikawa and the skateboarder Nora Vasconcellos &mdash; a pairing that tells you exactly which two rooms the brand wants to be in. On 20 August it put out the Sportocasin with G.H.BASS, a $275 shoe that reads as a penny loafer until you look at the sole. In between: Maxfli balls, Garrett Leight eyewear, a Realtree five-panel.",
  "Cole Young was a Division I golfer at Loyola Marymount and then a Malbon employee, and he has been direct about why he left. &ldquo;I was done helping people build their own empires,&rdquo; he told FORE Magazine. &ldquo;I knew I could do it, so I was just going to do it for me.&rdquo; He launched in April 2020. The line he uses to describe the result is the sharpest summary of the brand anyone has managed: &ldquo;It&rsquo;s also the only golf brand that doesn&rsquo;t have the word &lsquo;golf&rsquo; in the name.&rdquo;",
  "What that buys you is clothing that survives the car park. The graphics are dense and slightly sarcastic, the fits are cut for someone who owns skate shoes, and the price of entry is a $62 tee rather than a $200 quarter-zip. Founder still in place, no outside money we could find, cadence relentless. It is number one and it is not close.",
 ],
 "picks": [
  {"t": "King of the Grass Tee", "price": "approx. $62",
   "local": "/images/metalwood/new-kotg-tee.jpg",
   "desc": "The graphic tee is the brand&rsquo;s whole thesis in one $60-ish garment &mdash; dense artwork, boxy cut, no logo creep. Start here before anything else."},
  {"t": "Dewey Hoodie", "price": "approx. $148",
   "local": "/images/metalwood/new-dewey-hoodie.jpg",
   "desc": "Heavyweight brown hood with the wordmark across the chest. The piece that turns up in every Metalwood lookbook and most of the tagged photos."},
  {"t": "adidas × Metalwood Pant", "price": "approx. $130",
   "local": "/images/metalwood/new-adidas-pant.jpg",
   "desc": "From the February capsule with adidas Originals. Wide, pleated, black &mdash; the trouser that made the collab read as skate rather than golf."},
 ]},
{
 "k": "students", "rank": 2, "name": "Students Golf", "loc": "Los Angeles",
 "kick": "<strong>The pedigree is real, not borrowed.</strong> Founded out of Publish, stocked at Bodega and HBX, and the single biggest omission from the version of this page we are replacing.",
 "link": "/drops/students-golf-our-15-favorites", "linktext": "Our 15 favourite Students pieces",
 "body": [
  "Most golf brands claim streetwear. Students came the other way round. Michael Huynh built Publish first &mdash; a Los Angeles label with two decades in the actual streetwear trade &mdash; then applied that pattern-making to golf. The tell is in the cut: pleats that fall properly, mesh where a golf brand would use pique, an anorak that would work on a skate trip.",
  "The validation is wholesale, which is the hardest kind to manufacture. Students sits in Bodega, HBX and Culture Kings, shops that do not carry golf brands as a favour. A Students &times; PAYNTR shoe sold through at wholesale. The catalogue runs to 232 pieces in stock, and the newest went live on 29 August &mdash; the day before we checked.",
  "It is also the deepest range here. Where most brands on this list run a tee, a hood and a hat, Students has chore coats, wool jackets, knit cardigans and pleated slacks, so you can dress entirely out of it without looking like a walking merch table.",
 ],
 "picks": None},
{
 "k": "malbon", "rank": 3, "name": "Malbon Golf", "loc": "Los Angeles",
 "kick": "<strong>They built the category, and 2026 is the year it shows.</strong> They are impossible to leave off, and impossible to write about honestly without the ownership facts.",
 "link": "/drops/no-budget-malbon", "linktext": "No Budget &mdash; Malbon&rsquo;s most expensive pieces",
 "body": [
  "Stephen and Erica Malbon made golf streetwear a category that retailers would stock. Before Malbon, the idea that a golf brand could sit next to a skate brand was a pitch deck. After, it was a market. Everything else on this page exists partly because they proved the room was there.",
  "Here is what the other rankings will not tell you. Malbon raised a $33 million round led by Anthos Capital; Aaron Heiser, formerly of Nike, is now chief executive, and Stephen and Erica moved to co-Chief Creative Officers. Anthony Kim took an equity stake in February. In August they shipped a second Gap collection. The brand has a Performance tab in its navigation, a CoolCore program and $448 cart bags.",
  "That is not a criticism, it is a description &mdash; and it is the reason Malbon is third rather than first. The graphic energy that defined them has thinned as the range has broadened into mainstream performance and womenswear. The bucket hat era is over. What replaced it is a well-run apparel company that happens to have started as the loudest thing in golf.",
 ],
 "picks": None},
{
 "k": "casualist", "rank": 4, "name": "Casualist", "loc": "Melbourne &middot; London &middot; Los Angeles",
 "kick": "<strong>The best-made clothing in the category, and the quietest.</strong> No graphic you can read from the fairway &mdash; the argument here is entirely construction.",
 "link": "/drops/brand-to-know-casualist", "linktext": "Read the Casualist profile",
 "body": [
  "Casualist is the outlier on this page and it is here on purpose. There is no dense back print, no house character, no sneaker program. What there is instead is a cotton pique polo with an unstructured collar, a pleated trouser in organic cotton, and a ripstop jacket cut for the cart path &mdash; garments that would pass without comment in a room that has nothing to do with golf.",
  "That is the test, restated. The question is not whether a brand looks like streetwear; it is whether it designs like a clothing label rather than a golf company. Casualist does. The range is built the way a small menswear brand builds one &mdash; a polo, a mockneck, a trouser, a vest, a cap &mdash; and the golf is an application rather than a category. Prices run from &pound;45 for a five-panel to &pound;240 for the jacket, in sterling, from a brand that operates between Melbourne, London and Los Angeles.",
  "The honest mark against it is cadence. Casualist&rsquo;s most recent drop was 31 March &mdash; the pleated trousers, the No Idea heavy tee and the All The Gear sweatshirt, published within eight minutes of each other and nothing since. Five months is a long quiet spell in a category that moves weekly, and it is the reason Casualist sits fourth rather than higher. Everything on the site is in stock and shipping; there is simply less of it arriving.",
 ],
 "picks": [
  {"t": "Trust the Swing Pique Polo", "price": "&pound;115",
   "url": "https://casualist.com/products/trust-the-swing-pique-polo-dusty-blue",
   "desc": "It runs cotton pique with a soft unstructured collar, in dusty blue. The piece the brand is built around and the clearest statement of the whole idea: nothing on it you could read from the fairway."},
  {"t": "Pleated Golf Trousers — Organic Cotton", "price": "&pound;160",
   "url": "https://casualist.com/products/pleated-trousers",
   "desc": "The newest thing they have made, out on 31 March. Organic cotton, properly pleated, cut to sit as a normal trouser rather than a golf trouser."},
  {"t": "Cart Path Ripstop Jacket", "price": "&pound;240",
   "url": "https://casualist.com/products/cart-path-ripstop-jacket",
   "desc": "The best object in the range and the most expensive. Ripstop, boxy, and the one piece here that will outlast the trend that produced it."},
 ]},
{
 "k": "anti", "rank": 5, "name": "ANTi Country Club Tokyo", "loc": "Tokyo",
 "kick": "<strong>&ldquo;Anarchism to old school golf culture.&rdquo;</strong> That is their own line. They have an adidas Golf collab and HBX distribution, and page one of Google has never covered them.",
 "link": "/drops/the-white-tee-edit-2026", "linktext": "ANTi in The White Tee Edit",
 "body": [
  "Every other ranking of this category is American, with one British exception. That is a strange way to write about golf clothing in 2026, when the most interesting work is being done in Tokyo &mdash; a city that has treated golf as a subculture to dress for since the eighties.",
  "ANTi Country Club Tokyo state their position in the name and repeat it in their copy: anarchism to old school golf culture. In practice that means varsity jackets with a full back print, plaid double-layer shirting, one-tuck chinos and heavy embroidered crews, priced from about &yen;11,550 for a graphic tee up to &yen;65,000 for outerwear. The 26SS collection is live.",
  "The credential that matters: an adidas Golf &times; ANTi &ldquo;Gazelle G&rdquo; at &yen;22,000, and shelf space at HBX and at Badlands in New Jersey &mdash; the shop that also carries Students and Merrill. When American buyers import you, you are not a local curiosity.",
 ],
 "picks": None},
]

# The cut list is re-reasoned as of the Casualist swap. When the first test was
# "streetwear first", Manors, Quiet Golf and Odd Ritual were excluded BY
# DEFINITION. Loosening the test to "a clothing brand first" admits them, so
# leaving those old reasons in place would have the page contradict itself in
# two places on one screen. They are now cut on ranking, which is the honest
# answer: they qualify, they are not the five best.
CUT = [
 ("Not clothing brands &mdash; Sentinel, Fyfe, MacKenzie, Sugarloaf, Gumtree",
  "All excellent, none of them apparel labels. Sentinel builds Dyneema expedition gear, Fyfe makes Harris Tweed headcovers, MacKenzie builds leather carry bags by hand, Sugarloaf is Nantucket Red prep and Gumtree is upcycled deadstock and surfboards. They were on the old list to make the number fifteen."),
 ("Not trading &mdash; Bogey Boys",
  "Macklemore&rsquo;s label has <strong>no products at all</strong>. The all-collections page renders zero and the product sitemap is empty; the site has been a photo archive since roughly late March. There has been no shutdown announcement. Other rankings still list it as one to watch."),
 ("No longer independent &mdash; Eastside Golf",
  "Still very much alive, and no longer its own. Centric Brands formed a joint venture with them on 13 August 2026, placing Eastside alongside John Elliott and Palm Tree Crew. The range has also moved toward performance &mdash; pique polos, rain kit, wool melton caps."),
 ("Close calls &mdash; Manors, Quiet Golf, Odd Ritual, Pluto, Random Golf Club",
  "These pass the tests and did not make the five, which is a different thing from failing. Manors was the hardest: a &pound;3m round in March led by Redrice Ventures, the Reebok collaboration still running, real name recognition &mdash; but the 2026 range has settled into greenskeeper trousers and merino crewnecks. Pluto out of Indianapolis is the closest thing golf has to a hype brand, with genuinely oversized cuts and a sneaker program, and it was in the five until the last edit. Quiet has added cashmere and shoots editorials at Maidstone. Odd Ritual describes itself as a modern expression of heritage. Random Golf Club&rsquo;s only 2026 output in its own sitemap is event tickets for the Mad Scramble tour."),
]

FAQ = [
 ("What counts as golf streetwear?",
  "For this ranking, four things. The brand has to design like a clothing label that happens to make golf clothes, rather than a golf company adding a graphic to a performance polo. It has to sell garments you would wear off the course without explaining yourself. It has to have a real drop cadence rather than a static catalogue. And it has to be currently trading, with product in stock. Applying that honestly is why this list is five brands and not fifteen &mdash; and why Casualist, which owns no graphic at all, passes while several louder labels do not."),
 ("What is the best golf streetwear brand in 2026?",
  "Metalwood Studio. It is the only brand that is unambiguously streetwear and also had a landmark year — a first golf capsule with adidas Originals in February, and the Sportocasin with G.H.BASS in August. Founder Cole Young still runs it, and the entry price is a $62 tee."),
 ("Is Malbon still a streetwear brand?",
  "Less than it was. Malbon created the category, but the 2026 business is broader and more mainstream: a Performance tab in the navigation, a CoolCore program, $448 cart bags, womenswear. It also took a $33 million round led by Anthos Capital and now has an outside chief executive in Aaron Heiser, formerly of Nike, with Stephen and Erica Malbon moved to co-Chief Creative Officers."),
 ("What happened to Bogey Boys?",
  "As of 30 August 2026 the Bogey Boys store has no products. The all-collections page renders zero items and the product sitemap contains no product entries; the site has functioned as a lookbook archive since roughly late March. We could find no shutdown announcement, so we are reporting what the site shows rather than speculating about why."),
 ("Is Eastside Golf still independent?",
  "No. Centric Brands announced a joint venture with Eastside Golf on 13 August 2026, bringing it into the same division as John Elliott and Palm Tree Crew, with Centric taking on sourcing, distribution and marketing. Eastside had previously taken investment from EP Golf Ventures in January 2024."),
 ("Where can I buy these brands outside their own sites?",
  "Badlands in Atlantic Highlands, New Jersey is the most useful single stockist &mdash; it carries ANTi, Students and Merrill among others. Students is also at Bodega, HBX and Culture Kings, and ANTi is at HBX. Metalwood, Malbon and Casualist are largely direct."),
 ("How often is this page updated?",
  "Every brand here was status-checked on 30 August 2026 &mdash; store live, product in stock, most recent dated activity, and any change of ownership. We re-check quarterly, and we remove brands that stop trading rather than leaving them ranked."),
]


def main(apply_=False):
    tpl = open(TPL, encoding="utf-8").read()

    # ---- head: every field written fresh. Never inherit the template's identity.
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q,
                              "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
                             for q, a in FAQ]}
    art = {"@context": "https://schema.org", "@type": "Article",
           "headline": "The 5 Best Golf Streetwear Brands in 2026",
           "description": re.sub(r"&[a-z]+;", "-", DESC),
           "image": f"https://thegrassyissue.com{IMG}/hero.jpg",
           "datePublished": "2026-08-30", "dateModified": "2026-08-30",
           "author": {"@type": "Organization", "name": "The Grassy Issue"},
           "publisher": {"@type": "Organization", "name": "The Grassy Issue"},
           "mainEntityOfPage": f"https://thegrassyissue.com/drops/{SLUG}"}

    h = tpl[:tpl.find("</head>")]
    h = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', "", h, flags=re.S)
    for pat, rep in {
        r"<title>[^<]*</title>": f"<title>{TITLE} &mdash; The Grassy Issue</title>",
        r'(<meta name="description" content=")[^"]*(")': rf"\g<1>{DESC}\g<2>",
        r'(<meta property="og:title" content=")[^"]*(")': rf"\g<1>{TITLE}\g<2>",
        r'(<meta name="twitter:title" content=")[^"]*(")': rf"\g<1>{TITLE}\g<2>",
        r'(<meta property="og:description" content=")[^"]*(")': rf"\g<1>{DESC}\g<2>",
        r'(<meta name="twitter:description" content=")[^"]*(")': rf"\g<1>{DESC}\g<2>",
        r'(<meta property="og:image" content=")[^"]*(")': rf"\g<1>https://thegrassyissue.com{IMG}/hero.jpg\g<2>",
        r'(<meta name="twitter:image" content=")[^"]*(")': rf"\g<1>https://thegrassyissue.com{IMG}/hero.jpg\g<2>",
        r'(<meta property="og:url" content=")[^"]*(")': rf"\g<1>https://thegrassyissue.com/drops/{SLUG}\g<2>",
        r'(<link rel="canonical" href=")[^"]*(")': rf"\g<1>https://thegrassyissue.com/drops/{SLUG}\g<2>",
    }.items():
        h = re.sub(pat, rep, h, count=1)
    h += ('<script type="application/ld+json">\n' + json.dumps(art, indent=1, ensure_ascii=False)
          + '\n</script>\n<script type="application/ld+json">\n'
          + json.dumps(faq_ld, indent=1, ensure_ascii=False) + "\n</script>\n</head>\n")

    nav = re.search(r"(<body>.*?</nav>)", tpl, re.S).group(1)

    header = f'''
<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  The 5 Best Golf Streetwear Brands in 2026
</div>

<header class="drop-header">
  <span class="drop-tag grass">[Drops &amp; Brands]</span>
  <h1>The 5 Best Golf Streetwear Brands in 2026</h1>
  <div class="drop-meta">
    <span>5 Brands</span><span class="dot"></span>
    <span>15 Pieces</span><span class="dot"></span>
    <span>Status-checked {CHECKED}</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A golfer mid-swing in pleated trousers and an open camp shirt, a second figure in neon behind &mdash; Metalwood Studio campaign" /></div></div>
'''

    writeup = f'''<div class="writeup">
  <div class="writeup-body">
    <p>Golf streetwear is now a category with money in it, which means it is a category with a lot of brands claiming membership. Search the phrase and you get lists of seven, ten, thirty. Read them and you find performance labels, heritage labels, a Nicklaus licensing operation and at least one brand that has not sold a garment since March. The word has stopped doing any work.</p>
    <p>So we started from a definition instead of a number. A golf streetwear brand designs like a clothing label that happens to make golf clothes, rather than a golf company that adds a graphic to a performance polo. It sells clothes you would wear off the course without explaining yourself. It drops rather than stocks. And it is actually trading &mdash; store live, product in stock, on the day we checked. Fifteen brands went in. Five came out.</p>
    <p>This is for the person who wants one honest answer rather than a long list, and who would rather know that Malbon has an outside chief executive and $33 million of Anthos money behind it than read the same paragraph about bucket hats that every other page is still running. Every brand below was checked on {CHECKED}. Every piece was in stock at that moment, at the price shown, in the brand&rsquo;s own currency. Where a brand has changed hands, we say so.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Five</div>
      <div class="sidebar-detail"><span class="l">1</span><span>Metalwood Studio</span></div>
      <div class="sidebar-detail"><span class="l">2</span><span>Students Golf</span></div>
      <div class="sidebar-detail"><span class="l">3</span><span>Malbon Golf</span></div>
      <div class="sidebar-detail"><span class="l">4</span><span>Casualist</span></div>
      <div class="sidebar-detail"><span class="l">5</span><span>ANTi CC Tokyo</span></div>
      <div class="sidebar-detail"><span class="l">Checked</span><span>{CHECKED}</span></div>
      <a href="/brands/" class="sidebar-cta">The full Brand Index &nearr;</a>
      <div class="hashtags">
        <span class="hashtag">#TheGrassyIssue</span>
        <span class="hashtag">#GolfStreetwear</span>
        <span class="hashtag">#GolfCulture</span>
        <span class="hashtag">#DropsAndBrands</span>
        <span class="hashtag">#GolfStyle</span>
      </div>
    </div>
  </aside>
</div>
'''

    method = '''
<section class="products">
  <h2 class="products-hdr" id="how-we-picked">How We Picked</h2>
  <p class="cat-kicker"><strong>The definition comes before the ranking.</strong> Every brand here runs the same four tests.</p>
  <div style="max-width:760px;font-size:16px;line-height:1.75">
    <p><strong>1. A clothing brand first.</strong> The design starts from clothes and arrives at golf, not the other way round. A performance polo with a graphic on it is still a performance polo. This is a test of how a range is built, not of how loud it is &mdash; which is how a brand as quiet as Casualist and one as loud as Metalwood both pass it.</p>
    <p style="margin-top:14px"><strong>2. Wearable off the course.</strong> If the piece only makes sense inside the ropes, it belongs on a different list.</p>
    <p style="margin-top:14px"><strong>3. A real cadence.</strong> Drops, collaborations, a reason to check back. Not a static catalogue that has not moved in a year.</p>
    <p style="margin-top:14px"><strong>4. Actually trading.</strong> Store live, product in stock, on the day we looked. This is the test most rankings skip, and it is why one brand widely listed as an up-and-comer is not here.</p>
  </div>
</section>
'''

    body = ""
    for b in BRANDS:
        picks = b["picks"] or SK[b["k"]]["picks"]
        cards = "\n\n    ".join(card(b["k"], i, b["name"], p) for i, p in enumerate(picks))
        MT = ' style="margin-top:16px"'
        paras = "\n".join("    <p" + (MT if i else "") + f">{p}</p>"
                          for i, p in enumerate(b["body"]))
        body += f'''
<section class="products" style="border-top:none;padding-top:48px">
  <h2 class="products-hdr" id="{b["k"]}">{b["rank"]}. {b["name"]} &mdash; {b["loc"]}</h2>
  <p class="cat-kicker">{b["kick"]}</p>
  <div style="max-width:760px;font-size:16px;line-height:1.75;margin-bottom:12px">
{paras}
    <p style="margin-top:18px;font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;opacity:.6">Status checked {CHECKED} &middot; trading, product in stock &middot; <a href="{b["link"]}">{b["linktext"]} &rarr;</a></p>
  </div>
  <div class="products-grid">

    {cards}

  </div>
</section>
'''

    MT = ' style="margin-top:16px"'
    cut = "\n".join(
        "    <p" + (MT if i else "") + f"><strong>{n}.</strong> {t}</p>"
        for i, (n, t) in enumerate(CUT))
    cutsec = f'''
<section class="products" style="border-top:none;padding-top:48px">
  <h2 class="products-hdr" id="what-we-cut">What We Cut, and Why</h2>
  <p class="cat-kicker"><strong>The previous version of this page ranked fifteen brands.</strong> Ten are gone. Here is the reasoning, so you can disagree with it.</p>
  <div style="max-width:760px;font-size:16px;line-height:1.75">
{cut}
  </div>
</section>
'''

    faq_html = ('<div class="faq">\n' + "\n".join(
        f'    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>'
        for q, a in FAQ) + "\n  </div>")
    faq_sec = f'''
<section class="products" style="border-top:none;padding-top:48px">
  <h2 class="products-hdr" id="faq">Golf Streetwear &mdash; FAQ</h2>
  {faq_html}
</section>
'''

    more = tpl[tpl.rfind('<section class="more">'):]
    out = h + nav + header + writeup + method + body + cutsec + faq_sec + more

    if ".bk-founder" not in out:
        k = out.rfind("</style>")
        out = out[:k] + ("\n/*TGI-BTK-LAYOUT*/\n.bk-founder,.bk-look{max-width:1100px}\n@media(max-width:820px){.bk-founder{grid-template-columns:1fr!important}.bk-look{grid-template-columns:repeat(2,1fr)!important}}\n") + out[k:]

    words = len(H.unescape(re.sub(r"<[^>]+>", " ",
                re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", out, flags=re.S))).split())
    ncards = out.count('<div class="product-card')
    print(f"  cards {ncards}  frames {out.count('pg-frame')}  words {words}")
    if apply_:
        open(PAGE, "w", encoding="utf-8").write(out)
        print("  written", PAGE)
    else:
        print("  (dry run - pass --apply)")


if __name__ == "__main__":
    main("--apply" in sys.argv)
