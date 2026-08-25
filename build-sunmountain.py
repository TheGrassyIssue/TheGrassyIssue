#!/usr/bin/env python3
"""Build drops/brand-to-know-sun-mountain.html — Brand to Know: Sun Mountain Sports.

FACT NOTES (researched + source-verified 2026-08-25). Do not "correct" these:
  * Founded 1981 by Rick Reimers in SAN JOSE, CALIFORNIA. Moved to Missoula, Montana
    in 1984. Do NOT say "founded in Montana."
  * Eclipse, 1986 — first lightweight stand bag. Sun Mountain is CREDITED with it and
    says it was first to PATENT the stand system. Attribute; don't state as bare fact.
  * BACK 9 (c.1981) nylon carry bag; FRONT 9 (1984) first commercial success; the
    company then built the L8 bag for Ping as an OEM.
  * Speed Cart, 1999 — created the push-cart category. Micro-Cart (4-wheel) 2004.
  * C-130 cart bag introduced 2005.
  * Outerwear from 1990 (Headwind windshirt). US Presidents Cup outerwear 2011 + 2013.
  * Golf Datatech: best-selling golf bag brand three consecutive years (2010-2012).
  * SOLD to Solace Capital Partners (LA private equity) 7 March 2022. Reimers had been
    founder, director and SOLE SHAREHOLDER — no partners, investors or board, 41 years.
    He kept Sun Mountain Motor Sports (the Finn scooter).
  * Bags are ASSEMBLED in Missoula. NOT "made in the USA" — components/fabrics come
    from Asia. Use the brand's own wording: "assembled in the USA."
  * Grant Knudson is President and Chief Brand Officer. Do NOT call him CEO — the
    current CEO title could not be verified.
  * Site markets "45 Years" (1981-2026). Don't write "over 45."
UNVERIFIED, do not use: the "41 years is enough" Reimers sale quote (search-summary only);
"C-130 Hot List winner five consecutive years."
"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
FIN  = json.load(open('/tmp/sm-final.json')) if os.path.exists('/tmp/sm-final.json') else None
IMG  = "/images/sun-mountain/"
TPL  = os.path.join(ROOT, "drops", "brand-to-know-midiron.html")
OUT  = os.path.join(ROOT, "drops", "brand-to-know-sun-mountain.html")
SLUG = "brand-to-know-sun-mountain"
TITLE = "Brand to Know &mdash; Sun Mountain, the Montana Company That Put Legs on the Golf Bag"
TITLE_TXT = "Brand to Know — Sun Mountain, the Montana Company That Put Legs on the Golf Bag"
DESC = ("Sun Mountain invented the modern stand bag in 1986 and the push cart category in 1999, "
        "and still assembles its bags in Missoula, Montana. Eighteen picks across bags, carts, travel and accessories.")

# frames on disk
FR = FIN['products'] if FIN else {}

def card(handle, brand, name, desc, link, extra=()):
    frames = list(FR.get(handle, []))
    frames += [f for f in extra if f not in frames]
    n = len(frames)
    alt = re.sub(r'&[a-z]+;', '', re.sub(r'<[^>]+>', '', name))
    fr = "".join(f'<div class="pg-frame"><img src="{IMG}{f}" loading="lazy" '
                 f'alt="{alt} &middot; view {i+1} of {n}"></div>' for i, f in enumerate(frames))
    dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" '
                   f'aria-label="View image {i+1}"></button>' for i in range(n))
    return f'''  <div class="product-card" data-frames="{n}">
    <div class="product-gallery"><div class="pg-track">{fr}</div><button class="pg-arw prev" aria-label="Previous image">&#8249;</button><button class="pg-arw next" aria-label="Next image">&#8250;</button><span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>
      <div class="product-body">
        <div class="product-brand">{brand}</div>
        <div class="product-name">{name}</div>
        <div class="product-desc">{desc}</div>
        <a href="{link}" target="_blank" rel="noopener" class="product-link">Shop Sun Mountain &#8599;</a>
      </div>
  </div>'''

U = "https://www.sunmountain.com/products/"

BAGS = [
 ("legacy-leather-stand-bag","Sun Mountain","Legacy Leather Stand Bag &middot; $1,200",
  "The top of the range and the least Sun Mountain-looking thing they make &mdash; full-grain leather, a single strap, and the silhouette of a bag from before anyone thought to attach legs. It is the company quoting its own prehistory back at itself.", U+"legacy-leather-stand-bag", ("irl-06.jpg",)),
 ("hometown-waxed-canvas-stand-bag","Sun Mountain","Hometown Waxed Canvas Stand Bag &middot; $450",
  "Twelve-ounce waxed canvas, made for the country&rsquo;s 250th and limited to 1,776 individually numbered bags. The current halo product, and the one that best explains why a Montana company keeps leaning on Americana.", U+"hometown-waxed-canvas-stand-bag", ()),
 ("matchplay-ballistic-14-way-stand-bag","Sun Mountain","Matchplay Ballistic 14-way &middot; $435",
  "Ballistic nylon, fourteen full-length dividers, and the best-looking thing in the current line &mdash; the Grove green in particular. This is the walking bag for people who want structure without carrying a cart bag on their back.", U+"matchplay-ballistic-14-way-stand-bag", ("irl-18.jpg","irl-16.jpg","irl-19.jpg")),
 ("matchplay-swift-sunday","Sun Mountain","Matchplay Swift Sunday &middot; $315",
  "A Sunday bag with the Matchplay treatment. For the nine holes after work when carrying a full stand bag feels like overkill and carrying nothing feels like a mistake.", U+"matchplay-swift-sunday", ()),
 ("eclipse-e-2-5-stand-bag","Sun Mountain","Eclipse E-2.5 Stand Bag &middot; $224",
  "The name matters here. The original Eclipse in 1986 was the bag with legs; the E-2.5 is its lightweight descendant, and at $224 it is the most Sun Mountain purchase on this list &mdash; the invention, still in production, still cheap.", U+"eclipse-e-2-5-stand-bag", ("irl-29.jpg",)),
 ("h2no-e-4-5-vlo-stand-bag","Sun Mountain","H2NO E-4.5 VLO Stand Bag &middot; $380",
  "Fully waterproof, seam-sealed, with the VLO (very low-profile) leg mechanism. Sun Mountain built the first waterproof golf bags in 2007; this is where that line ended up.", U+"h2no-e-4-5-vlo-stand-bag", ()),
 ("c-series-c-130-cart-bag","Sun Mountain","C-Series C-130 Cart Bag &middot; $325",
  "Introduced in 2005 and plausibly the most common cart bag in the game &mdash; a 10.5-inch fourteen-way top, thirteen pockets, and a top oriented so the pockets face you when it is strapped to a cart. The default answer for two decades.", U+"c-series-c-130-cart-bag", ("irl-30.jpg","irl-03.jpg")),
 ("matchplay-cart-bag","Sun Mountain","Matchplay Cart Bag &middot; $450",
  "The Matchplay language applied to a riding bag. Cleaner than the C-130 and considerably more expensive, for people who ride but do not want their bag to look like rental equipment.", U+"matchplay-cart-bag", ("irl-12.jpg",)),
 ("h2no-c-130-cart-bag","Sun Mountain","H2NO C-130 Cart Bag &middot; $400",
  "The C-130 shape in the waterproof H2NO fabric. If you play somewhere the forecast is a genuine variable rather than a formality, this is the version to buy.", U+"h2no-c-130-cart-bag", ()),
]

CARTS = [
 ("speed-cart-x-push-cart","Sun Mountain","Speed Cart X &middot; $300",
  "The Speed Cart arrived in 1999 as the first genuinely foldable three-wheel push cart and created a category that did not previously exist. The X is the current version, and MyGolfSpy made it a staff pick in its 2026 push cart testing.", U+"speed-cart-x-push-cart", ("irl-31.jpg",)),
 ("px4-push-cart","Sun Mountain","PX4 Push Cart &middot; $330",
  "Four wheels instead of three, which trades a little folded bulk for a cart that tracks dead straight across a sidehill. The answer if your course is anything other than flat.", U+"px4-push-cart", ("irl-23.jpg",)),
 ("speed-cart-seat","Sun Mountain","Speed Cart Seat &middot; $75",
  "A seat that clips to the cart you already own. Unglamorous, and the single best $75 you can spend if you walk somewhere with a slow group in front of you.", U+"speed-cart-seat", ()),
]

TRAVEL = [
 ("clubglider3-travel-bag","Sun Mountain","ClubGlider3 Travel Bag &middot; $450",
  "The ClubGlider&rsquo;s trick is a set of retractable legs and wheels that take the weight of the bag off your arm entirely &mdash; you tip it and tow it rather than carry it. Launched in 2008; travel covers went from a rounding error to roughly seven per cent of the company&rsquo;s sales.", U+"clubglider3-travel-bag", ("irl-13.jpg","irl-11.jpg","irl-05.jpg")),
 ("kube-travel-cover","Sun Mountain","Kube Travel Cover &middot; $290",
  "The hard-sided alternative &mdash; a clamshell case for people who have watched a baggage handler work and would like a rigid shell between that and their driver.", U+"kube-travel-cover", ("irl-14.jpg",)),
]

ACC = [
 ("hazy-golf-x-sun-mountain-limited-edition-alignment-sticks","Hazy Golf &times; Sun Mountain","Limited Edition Alignment Sticks &middot; $130",
  "Sun Mountain&rsquo;s collaboration streak is the most interesting thing about the current era &mdash; Victus, Marucci, Realtree, Municipal, Bad Birdie. These are the prettiest of the small stuff.", U+"hazy-golf-x-sun-mountain-limited-edition-alignment-sticks", ("irl-27.jpg",)),
 ("canvas-leather-headcover-driver-1","Sun Mountain","Canvas/Leather Headcover &mdash; Driver &middot; $40",
  "Canvas body, leather trim, no branding to speak of. Made to sit on top of the Hometown without arguing with it.", U+"canvas-leather-headcover-driver-1", ()),
 ("leather-headcover-chevron-driver","Sun Mountain","Leather Headcover Chevron &middot; $35",
  "The dressier option, and the one that goes with the Legacy Leather bag if you are committing to the whole look.", U+"leather-headcover-chevron-driver", ()),
 ("colter-ii-blanket","Sun Mountain","Colter II Blanket &middot; $100",
  "A quilted, packable blanket named after John Colter, the trapper who walked out of the Lewis and Clark expedition and into what is now Montana. The most Missoula object in the catalogue.", U+"colter-ii-blanket", ()),
]

def section(hid, h2, strong, kicker, items):
    cards = "\n".join(card(*it) for it in items)
    return (f'<h2 id="{hid}">{h2}</h2>\n'
            f'<p class="cat-kicker"><strong>{strong}</strong>{kicker}</p>\n'
            f'<div class="products-grid">\n{cards}\n</div>\n')

QUOTE = ('\n<div class="pull-quote">\n'
         '  <div class="pull-quote-inner">&ldquo;And by the time I got to Montana, I had pretty much designed a new sort of golf bag in my head.&rdquo;'
         '<span class="pull-quote-attr">&mdash; Rick Reimers, Sun Mountain founder, on the drive north with a broken car radio</span></div>\n'
         '</div>\n')

products = (
 section("bags","The Bags","Nine picks &middot; $224&ndash;$1,200",
  "Where the company actually lives. The Eclipse line is the direct descendant of the 1986 bag that started all of this; the Matchplay is the modern flagship; the C-130 has been the default cart bag since 2005.", BAGS)
 + QUOTE +
 section("carts","The Push Carts","Three picks &middot; $75&ndash;$330",
  "Sun Mountain did to walking carts in 1999 what it had done to bags in 1986 &mdash; the Speed Cart folded down small enough that people actually bought one, and a category appeared.", CARTS)
 + section("travel","Travel","Two picks &middot; $290&ndash;$450",
  "The ClubGlider is the third invention on this page: legs and wheels that carry the weight for you through an airport. The Kube is the armoured alternative.", TRAVEL)
 + section("accessories","Accessories","Four picks &middot; $35&ndash;$130",
  "Headcovers, sticks and a blanket named after a mountain man. Small things, and the place the brand&rsquo;s current collaboration habit shows up first.", ACC)
)

FAQS = [
 ("Who founded Sun Mountain and when?",
  "Rick Reimers founded Sun Mountain in 1981. He started it in San Jose, California, and moved the company to Missoula, Montana in 1984 — a detail often lost, because Sun Mountain is so thoroughly identified with Montana now. Reimers was a club and teaching pro in Northern California before he quit, and by his own account designed his first bag in his head on the drive north."),
 ("Did Sun Mountain invent the golf stand bag?",
  "Sun Mountain is credited with creating the first modern lightweight stand bag — the Eclipse, in 1986 — and the company says it was the first to patent the stand mechanism used on essentially every stand bag since. No source we found establishes an earlier bag with built-in legs. Their nylon BACK 9 (around 1981) and FRONT 9 (1984) came first and made the lightweight carry bag viable; the legs came after."),
 ("Is Sun Mountain still family owned?",
  "No. Reimers ran it for 41 years as founder, director and sole shareholder — no partners, no outside investors, no board. In March 2022 he sold Sun Mountain Sports to Solace Capital Partners, a Los Angeles private equity firm. He kept Sun Mountain Motor Sports, which makes the Finn golf scooter he launched in 2019."),
 ("Are Sun Mountain bags made in the USA?",
  "They are assembled in the USA — specifically in Missoula, Montana, which is the company's own wording and the accurate one. Fabrics and components are sourced overseas. The Montana assembly operation is real and unusual for the category; \"made in the USA\" would be overstating it."),
 ("What is the Sun Mountain C-130?",
  "Their cart bag, introduced in 2005, and arguably the most widely used cart bag in golf. The current version has a 10.5-inch fourteen-way top, thirteen pockets, and a top reversed so the pockets face the player when the bag is strapped to a cart."),
 ("Did Sun Mountain invent the push cart?",
  "Not the push cart, but the modern folding one. The Speed Cart, launched in 1999, was the first easily foldable three-wheel cart, and the company's own line is that it \"created an entirely new category.\" The four-wheel Micro-Cart followed in 2004."),
 ("What is a ClubGlider?",
  "Sun Mountain's travel bag with retractable legs and wheels that take the weight off your arm — you tilt it and tow it rather than drag it. It launched in 2008 and grew travel covers from roughly half a per cent of company sales to about seven per cent."),
 ("Was Sun Mountain really the best-selling golf bag brand?",
  "Yes, by retail market share. Golf Datatech's 2012 report had them as the best-selling golf bag brand for a third consecutive year, and they accounted for 16.5% of US golf bag sales in 2010."),
 ("Which Sun Mountain bag should I buy?",
  "Walking and want light: the Eclipse E-2.5 at $224. Walking and want the nice one: the Matchplay Ballistic at $435. Riding: the C-130 at $325. Rain: the H2NO line. Buying an object rather than equipment: the Hometown waxed canvas or the Legacy Leather."),
 ("Does Sun Mountain make anything besides bags?",
  "Push carts since 1999, travel covers since 2008, and outerwear since 1990 — the Headwind windshirt in 1990 and golf fleece in 1991 were both firsts for the category. They supplied the US Presidents Cup team's outerwear in 2011 and 2013."),
]

faq_html = "\n".join(f'    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQS)
faq_ld = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in FAQS]}, ensure_ascii=False)
art_ld = json.dumps({"@context":"https://schema.org","@type":"Article","headline":TITLE_TXT,
 "description":DESC,"author":{"@type":"Organization","name":"The Grassy Issue"},
 "publisher":{"@type":"Organization","name":"The Grassy Issue"},
 "datePublished":"2026-08-25","dateModified":"2026-08-25",
 "mainEntityOfPage":f"https://thegrassyissue.com/drops/{SLUG}"}, ensure_ascii=False)

WRITEUP = '''<div class="writeup">
  <div class="writeup-body">
    <p>In 1981 a club pro named Rick Reimers quit his job in Northern California and drove north
    to Montana to ski and think. The car radio was broken. He spent the whole drive designing a
    golf bag in his head &mdash; and what came out the other end was a nylon carry bag that
    weighed less than half what the leather and vinyl bags of the day weighed.</p>
    <p>That was the BACK 9, and it was more interesting than it was successful. The FRONT 9 in
    1984 fixed that with a moulded top and bottom, sold properly, and became the shape every
    other carry bag copied. It also earned Sun Mountain a job building the L8 bag for Ping
    &mdash; a startup in Missoula quietly manufacturing for one of golf&rsquo;s giants.</p>
    <p>Then, in 1986, they put legs on it. The Eclipse is the bag Sun Mountain is credited with
    inventing, the one that patented the stand mechanism now hinged onto essentially every carry
    bag in the game. They did the same trick twice more: the Speed Cart in 1999 folded small
    enough that walking carts became something people actually owned, and the ClubGlider in 2008
    put retractable legs on a travel bag so an airport stopped being a workout.</p>
    <p>Here is the part that gets left out. Reimers ran the company for 41 years as founder,
    director and sole shareholder &mdash; no partners, no investors, no board of directors. In
    March 2022 he sold Sun Mountain Sports to Solace Capital Partners, a Los Angeles private
    equity firm, and kept the scooter business. The bags are still assembled in Missoula, which
    remains genuinely unusual; the fabrics come from Asia, and the company says
    &ldquo;assembled in the USA&rdquo; rather than made, which is the honest version.</p>
    <p>What follows is eighteen picks across the four things they make. The through-line is that
    three of them are categories Sun Mountain either created or reshaped &mdash; which is a
    strange thing to be able to say about a company most golfers think of as the sensible
    default.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>1981</span></div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Missoula, MT</span></div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>18</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$35&ndash;$1,200</span></div>
      <a href="https://www.sunmountain.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit Sun Mountain &nearr;</a>
      <div class="hashtags">
        <span class="hashtag">#TheGrassyIssue</span>
        <span class="hashtag">#SunMountain</span>
        <span class="hashtag">#StandBag</span>
        <span class="hashtag">#BrandToKnow</span>
      </div>
    </div>
  </aside>
</div>'''

CSS = ("\n.pull-quote{max-width:1400px;margin:0 auto;padding:0 32px}"
       "\n.pull-quote-inner{font-family:var(--serif);font-style:italic;font-size:22px;line-height:1.4;"
       "padding:32px 0;margin:0;border-top:.5px solid rgba(20,20,20,.15);"
       "border-bottom:.5px solid rgba(20,20,20,.15);color:var(--grass)}"
       "\n.pull-quote-attr{font-family:var(--mono);font-style:normal;font-size:10px;letter-spacing:.14em;"
       "text-transform:uppercase;color:var(--ink);opacity:.45;margin-top:12px;display:block}"
       "\n@media(max-width:640px){.pull-quote{padding:0 20px}.pull-quote-inner{font-size:18px;padding:24px 0}}\n")

tpl = open(TPL, encoding="utf-8").read()
head, rest = tpl.split('<section class="products">', 1)
_, tail = rest.split('</section>', 1)

def rep(s, pat, new, count=1):
    out, n = re.subn(pat, new, s, count=count, flags=re.S)
    assert n > 0, pat
    return out

head = rep(head, r'<title>.*?</title>', f'<title>{TITLE_TXT} | The Grassy Issue</title>')
head = rep(head, r'<meta name="description" content=".*?"', f'<meta name="description" content="{DESC}"')
head = rep(head, r'<meta property="og:url" content=".*?"', f'<meta property="og:url" content="https://thegrassyissue.com/drops/{SLUG}"')
head = rep(head, r'<meta property="og:title" content=".*?"', f'<meta property="og:title" content="{TITLE_TXT}"')
head = rep(head, r'<meta property="og:description" content=".*?"', f'<meta property="og:description" content="{DESC}"')
head = rep(head, r'<meta name="twitter:title" content=".*?"', f'<meta name="twitter:title" content="{TITLE_TXT}"')
head = rep(head, r'<meta name="twitter:description" content=".*?"', f'<meta name="twitter:description" content="{DESC}"')
head = rep(head, r'<link rel="canonical" href=".*?"', f'<link rel="canonical" href="https://thegrassyissue.com/drops/{SLUG}"')
head = rep(head, r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "Article".*?</script>',
           f'<script type="application/ld+json">{art_ld}</script>')
head = rep(head, r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "FAQPage".*?</script>',
           f'<script type="application/ld+json">{faq_ld}</script>')
head = rep(head, r'(<div class="breadcrumb">.*?<span>/</span>\s*)[^<]*?(</div>)', r'\g<1>' + TITLE_TXT + r'\g<2>')
head = rep(head, r'<h1>.*?</h1>', f'<h1>{TITLE}</h1>')
head = rep(head, r'<div class="drop-meta">.*?</div>',
           '<div class="drop-meta">\n    <span>18 Picks</span><span>&middot;</span><span>Missoula, MT &middot; Est. 1981</span>\n  </div>')
head = rep(head, r'<div class="drop-hero"><div class="drop-hero-img"><img src="[^"]*" alt="[^"]*"[^>]*/></div></div>',
           f'<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}hero.jpg" '
           f'alt="A golfer walking under live oaks carrying a Sun Mountain stand bag" style="object-position:center center;" /></div></div>')
head = rep(head, r'<div class="writeup">.*?</div>\s*</aside>\s*</div>', WRITEUP)
head = rep(head, r'</style>', CSS + '</style>')

tail = rep(tail, r'<div class="more-grid">.*?</div>\s*</section>',
'''<div class="more-grid">
    <a href="/drops/the-stand-bag-edit" class="more-card"><div class="more-kicker">The Edit</div><div class="more-title">18 Bags Built to Walk 18</div></a>
    <a href="/drops/brand-revisited-jones-sports-co" class="more-card"><div class="more-kicker">Brand Revisited</div><div class="more-title">Jones Sports Co, and the Taxi Driver Who Started It</div></a>
    <a href="/drops/brand-to-know-seamus" class="more-card"><div class="more-kicker">Brand to Know</div><div class="more-title">Seamus Golf &mdash; the Oregon Workshop</div></a>
  </div>
</section>''')

page = head + '<section class="products">\n' + products + '\n<div class="faq">\n' + faq_html + '\n  </div>\n</section>' + tail
open(OUT, "w", encoding="utf-8").write(page)
words = len(re.sub(r'<[^>]+>', ' ', page).split())
print(f"wrote {OUT} ({len(page):,} bytes, ~{words:,} words)")
