#!/usr/bin/env python3
"""Build drops/brand-to-know-seamus.html — Brand to Know: Seamus Golf, Beaverton OR.

EDITORIAL CONSTRAINTS (verified 2026-08-25):
  * Founded 2011, Akbar + Megan Chisti, started in their garage near Portland.
    Megan was a womenswear designer at Pendleton Woolen Mills; she remade a worn
    headcover Akbar's father gave him from a famous links club. NOTE the club is
    disputed (About page: Royal Troon; Akbar in a 2025 interview: Royal Portrush)
    — write "a famous links club" or note Troon per their site, don't overclaim.
  * Named after their Irish Terrier, Seamus O'Reily. Akbar caddied at Bandon
    Dunes in college; Bandon placed the first wholesale order.
  * 2016 Ryder Cup: Matt Kuchar commissioned USA flag covers for the whole US
    team (13 hand-cut stripes, 50 embroidered stars). Kuchar carried Seamus at
    the 2016 Olympics.
  * USGA: sold at every U.S. Open since Chambers Bay 2015; they hammer ball
    markers on-site at the merch pavilion. ~700 shops worldwide.
  * Hand Forged® pieces are hand-HAMMERED (not poured) by their Portland
    blacksmith (~90% of his business is Seamus). Free hand-stamped
    personalization up to 5 characters.
  * Everything cut/sewn in Oregon; wool from PNW mills incl. Pendleton + UK mills.
  * No "worth". No profanity (BMF clip excluded deliberately). All images local.
  * Tag = [Drops & Brands]. Update brands.json profile (seamus exists in Fyfe
    cover edit mentions?) + mentions map after build.
"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
MAN  = json.load(open('/tmp/seamus/manifest.json'))
TPL  = os.path.join(ROOT, "drops", "brand-to-know-midiron.html")
OUT  = os.path.join(ROOT, "drops", "brand-to-know-seamus.html")
SLUG = "brand-to-know-seamus"
TITLE = "Brand to Know &mdash; Seamus Golf, the Oregon Workshop That Covered a Ryder Cup Team"
TITLE_TXT = "Brand to Know — Seamus Golf, the Oregon Workshop That Covered a Ryder Cup Team"
DESC = ("Hand-cut wool headcovers sewn in Beaverton, Oregon since 2011 — Pendleton fabric, a blacksmith who "
        "hammers the ball markers, the 2016 U.S. Ryder Cup team's covers, and 23 best-sellers across drivers, putters and accessories.")
IMG = "/images/seamus/"

def card(slug, name, desc):
    m = MAN[slug]; frames = m['frames']; n = len(frames)
    price = f"${int(m['price'])}"
    link = f"https://www.seamusgolf.com/products/{m['handle']}"
    alt = re.sub(r'&[a-z]+;', '', re.sub(r'<[^>]+>', '', name))
    fr = "".join(f'<div class="pg-frame"><img src="{IMG}{f}" loading="lazy" alt="{alt} by Seamus Golf, handmade in Oregon"></div>' for f in frames)
    dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" aria-label="View image {i+1}"></button>' for i in range(n))
    return f'''  <div class="product-card" data-frames="{n}" id="{slug}">
    <div class="product-gallery"><div class="pg-track">{fr}</div><button class="pg-arw prev" aria-label="Previous image">&#8249;</button><button class="pg-arw next" aria-label="Next image">&#8250;</button><span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>
      <div class="product-body">
        <div class="product-brand">Seamus Golf &middot; In stock</div>
        <div class="product-name">{name} &middot; {price}</div>
        <div class="product-desc">{desc}</div>
        <a href="{link}" target="_blank" rel="noopener" class="product-link">View &#8599;</a>
      </div>
  </div>'''

S1 = [  # The Woods
 ("patriot-driver","USA Wool Driver &mdash; Patriot",
  "The civilian version of the most famous thing Seamus ever made. When Matt Kuchar commissioned American flag covers for the entire 2016 U.S. Ryder Cup team, each one carried thirteen hand-cut stripes and fifty embroidered stars; the Patriot is that DNA in the standing line. Wool, cut and sewn in Beaverton, fleece-lined like everything they make."),
 ("glacier-driver","Pendleton&reg; Glacier Peaks Wool Driver",
  "Their best-selling driver cover, and the origin story as a product. Megan Chisti was a womenswear designer at Pendleton Woolen Mills when she sewed the first Seamus cover; the licensed Pendleton line closes that loop, and Glacier Peaks &mdash; the Pacific Northwest blanket pattern &mdash; is the one their customers buy most."),
 ("dude-driver","&ldquo;The Dude&rdquo; Natural Canvas Driver",
  "An embroidered Big Lebowski homage on natural canvas &mdash; cardigan, White Russian posture and all &mdash; and a permanent resident of the best-sellers page. Seamus plays these references completely straight, which is what makes them land. The Dude abides on the tee box."),
 ("stogie-driver","Kramer &ldquo;The Stogie&rdquo; Natural Canvas Driver",
  "The Seinfeld counterpart: Kramer mid-stride with a cigar, embroidered on the same natural canvas. Between this and the Dude, Seamus has quietly built the best pop-culture corner in headcovers &mdash; hand-sewn in Oregon rather than screen-printed offshore."),
 ("glenaffric-driver","Glen Affric Tartan Driver",
  "The history piece. Glen Affric is held to be Scotland&rsquo;s oldest surviving tartan &mdash; the recovered fragment dates to roughly the sixteenth century &mdash; and Seamus cuts the modern weave into a driver cover. A four-hundred-year-old pattern protecting a titanium head is the whole brand in one object."),
 ("earlst-driver","Earl St Andrews Tartan Driver",
  "The best-selling tartan in the program, named for the home of golf. If you only ever buy one Seamus cover, their own sales data says it will probably be this one &mdash; and there is a matching blade cover below to complete the set."),
 ("irish-driver","Irish National Tartan Driver",
  "The green-and-gold flagship of the Irish side of the tartan shelf, which runs all the way down to individual county patterns &mdash; Antrim, Donegal, Tipperary. St. Patrick&rsquo;s Day availability not guaranteed; it sells."),
 ("roper-driver","Roper Boot Black Tribeca Leather Driver",
  "The most expensive cover in this post, and it reads like a boot &mdash; black Tribeca leather with western stitching up the shaft. Cowboy-boot construction logic applied to a driver, and the rare cover that gets better scuffed."),
 ("uso-driver","2026 U.S. Open Driver &mdash; Navy",
  "Seamus has sold at every U.S. Open since Chambers Bay in 2015, and the Shinnecock capsule is this year&rsquo;s edition &mdash; washed navy with nautical signal flags for the Long Island setting. Championship merch made by a family-owned Oregon workshop instead of a licensing conglomerate."),
]
S2 = [  # The Putters
 ("dude-mallet","&ldquo;The Dude&rdquo; Heel Shafted Mallet",
  "The number-one item on Seamus&rsquo;s own best-selling-headcovers list: the Dude, scaled down to a mallet. Apparently a lot of people want Jeff Bridges guarding their putter, and after enough three-putts the &ldquo;that&rsquo;s just, like, your opinion, man&rdquo; energy is genuinely useful."),
 ("earlst-putter","Earl St Andrews Tartan Blade Putter",
  "The blade companion to the best-selling driver tartan &mdash; same weave, cut for a heel-shafted blade with the fleece lining and one-hand elastic opening the covers are known for."),
 ("glacier-putter","Pendleton&reg; Glacier Peaks Wool Blade Putter",
  "Glacier Peaks again, because their customers keep voting for it &mdash; the blanket-pattern blade cover is a best seller in its own right. The miniature-camp-blanket effect is strongest at putter scale."),
 ("buffalo-putter","Pendleton&reg; Land of the Buffalo Wool Blade Putter",
  "The other Pendleton pattern on the best-seller list &mdash; Land of the Buffalo, a plains motif in rust and cream that reads more Monument Valley than Old Course. The strongest-looking blade cover they make, by our eye."),
 ("sugarskulls-mallet","Pendleton&reg; Sugar Skulls Heel Shafted Mallet",
  "The loudest thing in the Pendleton license and a house best seller in five different cover shapes &mdash; a D&iacute;a de los Muertos skull motif in full color. The mallet is the shape that shows the most of the print."),
 ("harristweed-putter","Navy Harris Tweed Blade Putter",
  "Harris Tweed is the world&rsquo;s only fabric protected by its own act of parliament &mdash; hand-woven in the Outer Hebrides, certified by orb stamp. Seamus imports it and cuts it into blade covers in Oregon. A navy herringbone that will outlast several putters."),
]
S3 = [  # The Accessories
 ("limerick-marker","Hand Forged&reg; Limerick Ball Marker &mdash; Bronze",
  "The top-selling piece of the Hand Forged program. Every one is hammered &mdash; not cast, not poured &mdash; by Seamus&rsquo;s blacksmith in Portland, who now does roughly ninety per cent of his business with the brand, and hand-stamped personalization up to five characters is free."),
 ("drainit-marker","Hand Forged&reg; &ldquo;Drain It&rdquo; Ball Marker &mdash; Steel",
  "A hammered steel marker that says exactly what you are supposed to do next. The forged pieces come out of the smithy slightly different every time, which is the point &mdash; yours will not match anyone else&rsquo;s."),
 ("sugarskulls-marker","Hand Forged&reg; Pendleton&reg; Sugar Skulls Marker &mdash; Oil Can",
  "The Sugar Skulls print translated into hammered metal with an oil-can finish &mdash; the crossover point of the two things Seamus does that nobody else does: licensed Pendleton patterns and blacksmith-made markers."),
 ("horseshoe-marker","Hand Forged&reg; Lucky Horseshoe Marker &mdash; Steel",
  "A horseshoe you can actually carry to the first tee. Steel, hand-hammered, and the best-selling of the superstition markers &mdash; a category only Seamus would think to have."),
 ("markit8-marker","Hand Forged&reg; &ldquo;Mark It 8&rdquo; Marker &mdash; Copper",
  "The Lebowski reference completing the set with the Dude covers above &mdash; a copper marker for anyone who has ever wanted to mark it eight on a card where that would be generous. Over the line? No. $36."),
 ("goat-tag","Hand Forged&reg; Goat Caddie Bottle-Opener Bag Tag",
  "A steel bag tag that is also a bottle opener, hammered into the shape of the brand&rsquo;s goat-caddie mark. The most useful $76 on this page by roughly the ninth hole."),
 ("canyonlands-towel","Canyonlands Golf Towel",
  "The Pendleton desert geometric as a jacquard-woven towel &mdash; part of a towel line that keeps landing in their best sellers. At $45 it is the cheapest way to get the blanket patterns onto your bag."),
 ("dude-shirt","&ldquo;Obviously You&rsquo;re Not A Golfer&rdquo; Dude Shirt",
  "Yes, they make a shirt, and yes, it is a best seller &mdash; the Walter Sobchak line on a camp-collar print covered in Dude iconography. The rare piece of golf clothing whose joke actually holds up on the eighth wear."),
]
def section(hid, h2, strong, kicker, items):
    cards = "\n".join(card(*it) for it in items)
    return (f'<h2 id="{hid}">{h2}</h2>\n'
            f'<p class="cat-kicker"><strong>{strong}</strong>{kicker}</p>\n'
            f'<div class="products-grid">\n{cards}\n</div>\n')

products = "\n".join([
 section("woods","The Woods","Nine covers &middot; $120 to $170",
  "Driver and fairway covers are the engine of the company &mdash; wool, leather, canvas and seersucker, every one cut and sewn in the Beaverton workshop. There is also a Customizer on their site that lets you mash up panels, fasteners and linings into a one-off; we left it out of the grid only because your version will not look like ours. Every pick below comes from their own best-seller lists, plus the Patriot for the story.", S1),
 section("putters","The Putters","Six covers &middot; $120 to $170",
  "The putter shelf is where the fabric library shows off: parliament-protected Harris Tweed, registered Irish tartans, Hawaiian barkcloth and licensed Pendleton patterns, all fleece-lined and shaped for blades and mallets. This is the corner of the catalogue closest to the covers Megan Chisti first sewed in the garage.", S2),
 section("accessories","The Accessories","Eight pieces &middot; $36 to $76",
  "The other half of the workshop, straight off the best-seller list: markers hammered by an actual blacksmith in Portland, a bottle-opener bag tag, Pendleton towels and one very quotable shirt. Personalization on the forged pieces is hand-stamped in-house and free.", S3),
])

FAQS = [
 ("Who founded Seamus Golf?",
  "Akbar and Megan Chisti, in 2011, working out of their garage in the Portland area. Megan was a womenswear designer at Pendleton Woolen Mills; the company began when she remade a worn-out wool headcover that Akbar's father had given him from a famous links club, then sewed prototypes for his golf group."),
 ("Where are Seamus headcovers made?",
  "Beaverton, Oregon — designed, hand-cut, sewn and packaged in their own workshop, with a storefront at the same address. Wool comes from Pacific Northwest mills including Pendleton and from mills in the UK, including genuine Harris Tweed from the Outer Hebrides."),
 ("What is the Seamus Ryder Cup story?",
  "At the 2016 Ryder Cup, Matt Kuchar commissioned personalized American flag covers for the entire U.S. team — thirteen hand-cut stripes and fifty embroidered stars each. Kuchar also carried Seamus at the 2016 Olympics, and Bill Murray used one in the Ryder Cup celebrity match. The USA Wool \"Patriot\" cover in the standing line descends from that commission."),
 ("Does Seamus make official U.S. Open merchandise?",
  "Yes — they have sold at every U.S. Open since Chambers Bay in 2015, and they hammer ball markers on-site at the championship merchandise pavilion. The 2026 Shinnecock Hills capsule (driver cover, mallet cover, pouch, flask, markers) is on their site now."),
 ("What does Hand Forged mean at Seamus?",
  "The metal pieces — ball markers, pitch tools, money clips, bag tags — are hand-hammered by the brand's blacksmith in Portland, who now does roughly ninety per cent of his work for Seamus. They are not cast or poured, each comes out slightly different, and hand-stamped personalization up to five characters is free."),
 ("Why is it called Seamus?",
  "The company is named after the founders' Irish Terrier, Seamus O'Reily. It is pronounced SHAY-mus."),
 ("What is the Seamus tartan program?",
  "Authentic registered tartans — Scottish patterns, a full Irish county collection, and custom tartan work. For the 2019 U.S. Open at Pebble Beach they registered an original design with the Scottish Register of Tartans. It is the most serious fabric program in golf accessories."),
 ("What do Seamus headcovers cost?",
  "Driver covers run roughly $120 to $170 depending on fabric — seersucker and corduroy at the low end, full leather at the top. Putter covers sit between $120 and $170, hand-forged markers at $36 to $48, and the entry point is a $20 wooden bag tag."),
 ("What was Seamus's connection to Bandon Dunes?",
  "Akbar Chisti caddied at Bandon Dunes in college, and the resort placed the brand's first wholesale order — Seamus credits it with getting the company off the ground. Megan quit her Pendleton job shortly after. The pro shops there still carry a dedicated Seamus line."),
 ("How big is Seamus Golf now?",
  "Roughly 700 wholesale accounts worldwide — up from about 45 in the early days — including Japan, the UK and Australia, while the couple still owns the company outright and production stays in Oregon."),
]

faq_html = "\n".join(f'    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>' for q,a in FAQS)
faq_ld = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQS]}, ensure_ascii=False)
art_ld = json.dumps({"@context":"https://schema.org","@type":"Article","headline":TITLE_TXT,
 "description":DESC.replace('&mdash;','—'),
 "author":{"@type":"Organization","name":"The Grassy Issue"},
 "publisher":{"@type":"Organization","name":"The Grassy Issue"},
 "datePublished":"2026-08-25","dateModified":"2026-08-25",
 "mainEntityOfPage":f"https://thegrassyissue.com/drops/{SLUG}"}, ensure_ascii=False)

WRITEUP = '''<div class="writeup">
  <div class="writeup-body">
    <p>The Seamus origin story runs through a closet, like Criquet&rsquo;s, except this one starts with a
    headcover. Akbar Chisti&rsquo;s father had given him a wool cover from a famous links club &mdash; the
    company&rsquo;s own telling says Royal Troon &mdash; and it was wearing out. His wife Megan happened to be a
    womenswear designer at Pendleton Woolen Mills, so in 2011 she remade it from fabric remnants, then sewed a few
    more for his golf group, and then they were running a company out of their garage. It is named after their
    Irish Terrier, Seamus O&rsquo;Reily. You pronounce it SHAY-mus.</p>
    <p>The first wholesale order came from Bandon Dunes, where Akbar had caddied in college &mdash; about as good
    an origin credential as Pacific Northwest golf can issue. Fifteen years later the operation still cuts and sews
    everything in Beaverton, Oregon, sources wool from Pendleton and from UK mills including
    parliament-protected Harris Tweed, and wholesales to roughly 700 shops worldwide while the Chistis still own
    all of it.</p>
    <p>Two things make them a Brand to Know rather than just a nice accessories company. The first is the Ryder
    Cup: in 2016, Matt Kuchar commissioned personalized American flag covers for the entire U.S. team &mdash;
    thirteen hand-cut stripes, fifty embroidered stars, each one sewn in Oregon. The second is the blacksmith. The
    Hand Forged line of markers, pitch tools and money clips is hammered &mdash; not cast &mdash; by a smith in
    Portland who now does about ninety per cent of his business with Seamus, and the USGA lets them set up and
    hammer markers on-site at U.S. Open merchandise pavilions, where the brand has sold every year since Chambers
    Bay in 2015.</p>
    <p>Below, the deep version Lenny asked for: nine wood covers, six putter covers, and eight pieces from the
    forged-and-sewn accessories bench &mdash; drawn from the brand&rsquo;s own best-seller lists. Seamus has appeared in half a dozen of our edits already; this is the page
    those mentions have been waiting for.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>Oregon, 2011</span></div>
      <div class="sidebar-detail"><span class="l">Founders</span><span>Akbar &amp; Megan Chisti</span></div>
      <div class="sidebar-detail"><span class="l">Made in</span><span>Beaverton, OR</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$20 &ndash; $170</span></div>
      <a href="/"  class="sidebar-cta">&larr; Back to Feed</a>
      <div class="hashtags">
        <span class="hashtag">#TheGrassyIssue</span>
        <span class="hashtag">#SeamusGolf</span>
        <span class="hashtag">#Headcovers</span>
        <span class="hashtag">#MadeInOregon</span>
      </div>
    </div>
  </aside>
</div>'''

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
head = rep(head, r'(<div class="breadcrumb">.*?<span>/</span>\s*)[^<]*?(</div>)', r'\g<1>'+TITLE_TXT+r'\g<2>')
head = rep(head, r'<span class="drop-tag grass">\[[^\]]*\]</span>', '<span class="drop-tag grass">[Drops &amp; Brands]</span>')
head = rep(head, r'<h1>.*?</h1>', f'<h1>{TITLE}</h1>')
head = rep(head, r'<div class="drop-meta">.*?</div>', '<div class="drop-meta">\n    <span>23 Picks</span><span>&middot;</span><span>Beaverton, OR &middot; Est. 2011</span>\n  </div>')
head = rep(head, r'<div class="drop-hero"><div class="drop-hero-img"><img src="[^"]*" alt="[^"]*"[^>]*/></div></div>',
           f'<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}patriot-driver-1.jpg" alt="Seamus Golf USA wool driver cover, hand-cut and sewn in Beaverton, Oregon" /></div></div>')
head = rep(head, r'<div class="writeup">.*?</div>\s*</aside>\s*</div>', WRITEUP)

tail = rep(tail, r'<div class="more-grid">.*?</div>\s*</section>',
'''<div class="more-grid">
    <a href="/drops/the-fyfe-putter-cover-edit" class="more-card"><div class="more-kicker">Drops &amp; Brands</div><div class="more-title">The Fyfe Putter Cover Edit &mdash; Handmade in Scotland</div></a>
    <a href="/drops/brand-to-know-criquet" class="more-card"><div class="more-kicker">Drops &amp; Brands</div><div class="more-title">Brand to Know &mdash; Criquet</div></a>
    <a href="/drops/18-driver-headcovers-wed-game" class="more-card"><div class="more-kicker">Drops &amp; Brands</div><div class="more-title">18 Driver Headcovers We&rsquo;d Game</div></a>
  </div>
</section>''')

page = head + '<section class="products">\n' + products + '\n<div class="faq">\n' + faq_html + '\n  </div>\n</section>' + tail
open(OUT, "w", encoding="utf-8").write(page)
words = len(re.sub(r'<[^>]+>',' ',page).split())
print(f"wrote {OUT} ({len(page):,} bytes, ~{words:,} words)")
