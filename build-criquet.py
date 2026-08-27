#!/usr/bin/env python3
"""Build drops/brand-to-know-criquet.html — Brand to Know: Criquet Shirts, Austin.

EDITORIAL CONSTRAINTS (facts verified 2026-08-25, sources in session):
  * Founders Billy Nachman + Hobson Brown, kindergarten friends (Manhattan),
    founded Austin 2010 (brand's own About page; CNBC 11/2017).
  * Origin: Billy's grandfather's vintage 4-button-placket golf shirt.
  * Name: brand says it comes from the sound of crickets ("Comfortably Off-Course").
    Do NOT use the "French spelling of cricket" story (unverified).
  * Clubhouse: 1603 S. 1st St — status uncertain in 2026; write "longtime South
    First clubhouse", no claims it is currently open.
  * Classic Players Shirt $98 — today 100% Peruvian pima; organic cotton was the
    FOUNDING-era pitch. Phrase as history, not current spec. No GOTS claims.
  * Willie Nelson "Willie Forever" was a real licensed collection, now delisted —
    editorial mention only, no product card.
  * $1.4M Series A (CircleUp, Sept 2016). Press: CNBC, Details "The Perfect Polo".
  * No "worth". All images local /images/criquet/. Tag = [Drops & Brands].
"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
MAN  = json.load(open('/tmp/criquet/manifest.json'))
TPL  = os.path.join(ROOT, "drops", "brand-to-know-midiron.html")
OUT  = os.path.join(ROOT, "drops", "brand-to-know-criquet.html")
SLUG = "brand-to-know-criquet"
TITLE = "Brand to Know &mdash; Criquet, the Austin Label That Rebuilt Grandpa&rsquo;s Golf Shirt"
TITLE_TXT = "Brand to Know — Criquet, the Austin Label That Rebuilt Grandpa's Golf Shirt"
DESC = ("Criquet has been making its 4-button Players Shirt in Austin since 2010 — a clubhouse on South First, "
        "a licensed Willie Nelson collection, a Save Muny belt, and the collabs, core and new fall season, reviewed.")
IMG = "/images/criquet/"

def card(slug, status, name, desc):
    m = MAN[slug]; frames = m['frames']; n = len(frames)
    price = f"${int(m['price'])}"
    link = f"https://criquetshirts.com/products/{m['handle']}"
    alt = re.sub(r'&[a-z]+;', '', re.sub(r'<[^>]+>', '', name))
    fr = "".join(f'<div class="pg-frame"><img src="{IMG}{f}" loading="lazy" alt="{alt} by Criquet Shirts, Austin Texas"></div>' for f in frames)
    dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" aria-label="View image {i+1}"></button>' for i in range(n))
    return f'''  <div class="product-card" data-frames="{n}" id="{slug}">
    <div class="product-gallery"><div class="pg-track">{fr}</div><button class="pg-arw prev" aria-label="Previous image">&#8249;</button><button class="pg-arw next" aria-label="Next image">&#8250;</button><span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>
      <div class="product-body">
        <div class="product-brand">Criquet &middot; {status}</div>
        <div class="product-name">{name} &middot; {price}</div>
        <div class="product-desc">{desc}</div>
        <a href="{link}" target="_blank" rel="noopener" class="product-link">View &#8599;</a>
      </div>
  </div>'''

S1 = [  # The Collabs
 ("savemuny","In stock","Zilker Belts &ldquo;Save Muny&rdquo; Gaucho Belt",
  "The most Grassy Issue object Criquet sells. A hand-stitched Argentine-style gaucho belt made with Zilker Belts &mdash; the Austin belt maker two miles from Criquet&rsquo;s own shop &mdash; in the Save Muny colorway supporting the campaign to protect Lions Municipal. Austin brand, Austin belt maker, Austin cause, one strap of leather."),
 ("austinfc","In stock","Austin FC Coaches Players Shirt",
  "Officially licensed MLS gear that does not look like licensed MLS gear. The Coaches Players Shirt takes Criquet&rsquo;s four-button silhouette and runs it in Austin FC&rsquo;s verde with the tree crest small on the chest &mdash; the rare soccer merch you could wear to a tee time at Butler and nobody would blink."),
 ("yeti-bottle","In stock","Criquet &times; YETI 26 oz Water Bottle",
  "Two Austin institutions on one piece of drinkware &mdash; YETI&rsquo;s 26-ounce bottle in navy with the Criquet flag under the logo. There is also a 20-ounce tumbler in forest green if your rounds skew more coffee than water. Fifteen minutes apart by car, finally on the same product."),
 ("jones-duffle","In stock","Criquet &times; Jones Letterman Duffle",
  "Criquet&rsquo;s patch riding on the Letterman Duffle from Jones Sports Co &mdash; the Portland bag maker with its own page in our index. Black canvas, white racing stripes, sized for a weekend trip built around two tee times. The two brands have collaborated on bags going back several drops."),
 ("discmania","In stock","Discmania &ldquo;Carl&rsquo;s Greatest Hits&rdquo; Disc Golf 3-Pack",
  "Yes, disc golf. Carl is Criquet&rsquo;s long-running mascot-slash-alter-ego, and his Greatest Hits is a three-disc set with Discmania, the Finnish disc golf house. Zilker Park has one of the country&rsquo;s oldest disc golf traditions; this is Criquet leaning all the way into which city it lives in."),
 ("manolo","In stock","Manolo Limited Performance Players &mdash; Velvet Elvis",
  "A limited run with Austin artist ecosystem energy: the Performance Players Shirt in five loud-quiet colorways under the Manolo name &mdash; Velvet Elvis is the purple one. Same shirt your grandfather would recognize, in a color he absolutely would not."),
]
S2 = [  # The Core
 ("classic-players","In stock","Classic Players Shirt",
  "The founding document. Billy Nachman found his late grandfather&rsquo;s four-button golf shirt in a closet and, with kindergarten friend Hobson Brown, rebuilt it: long placket, flap chest pocket, removable collar stays so the collar never bacons. It launched the brand in 2010 with an organic-cotton pitch; today&rsquo;s version runs 100 per cent Peruvian pima. Still $98, still the shirt everything else here descends from."),
 ("performance-players","In stock","Performance Players Shirt",
  "The same silhouette re-cut in a poly-cotton-spandex blend for people who actually sweat through an Austin summer. This is the version that shows up on the course &mdash; and in Criquet&rsquo;s best-sellers list in four different colorways at once. Midnight is the default answer."),
 ("throwback","In stock","Throwback Players Shirt",
  "The retro cut of the Players &mdash; boxier, softer, closer to the shirt that started the whole thing. If the Classic is the restoration, the Throwback is the reenactment."),
 ("brrr-polo","In stock","brrr&deg; Long Sleeve Range Polo",
  "The golf-first piece of the range: a long-sleeve polo cut with brrr&deg; cooling fabric &mdash; the mineral-infused yarn that actually pulls heat off your skin. A long sleeve you can wear in a Texas June is a strange and useful thing, and it is one of the brand&rsquo;s consistent best sellers."),
 ("cord-pearlsnap","In stock","Short Sleeve Corduroy Pearl Snap",
  "The other half of Criquet&rsquo;s identity: honky-tonk wear. A short-sleeve corduroy shirt with pearl snaps in burnt orange &mdash; a color chosen by a brand that knows exactly which city and which university it is selling to. Their campaign photography puts it under a cowboy hat, which is accurate."),
 ("terry-toker","In stock","Terrycloth Players Shirt &mdash; Midnight Toker",
  "The Players Shirt in loop terry, colorway named Midnight Toker &mdash; as close as the current catalogue gets to winking at the delisted Willie Nelson collection. Pool deck, clubhouse patio, breakfast taco run: all sanctioned uses."),
]
S3 = [  # The New Season
 ("ls-bluesteel","In stock","Long Sleeve Players Shirt &mdash; Blue Steel",
  "The lead of the new fall drop &mdash; the Players Shirt with sleeves, in a blue-grey knit that covers the September window where Austin pretends to have a fall. Also comes in Peacoat, Blackstone and the paler Mr. Freeze."),
 ("ls-mrfreeze","In stock","Long Sleeve Players Shirt &mdash; Mr. Freeze",
  "The ice-blue version of the same shirt, named with the same energy that named Midnight Toker and Velvet Elvis. Criquet colorway names are a genre of their own, and Mr. Freeze in a 100-degree state is the best of this season&rsquo;s batch."),
 ("lions-tee","In stock","Slub Graphic Tee &mdash; Lions Badge",
  "A vintage-indigo slub tee carrying a Lions badge &mdash; from the brand whose belt collab literally says Save Muny. Between this and the Zilker strap, Criquet has more Lions Municipal merchandise than some golf brands have merchandise."),
 ("canvas-pant","In stock","Comfort Canvas Pant",
  "The fall anchor: a garment-washed canvas five-pocket in camel, faded navy and charcoal. It is the pant equivalent of the Players Shirt thesis &mdash; looks right at a course, a bar, and everywhere in the eight-hour gap between them."),
 ("waffle-rugby","In stock","Waffle Rugby Shirt",
  "A heathered waffle-knit rugby that has been sitting in the best-sellers grid since it arrived. Heather Green is the one &mdash; white collar, tipped cuffs, the collegiate look without a licensing agreement attached."),
 ("oxford-knit","In stock","Oxford Knit Button Down",
  "An oxford that is secretly a knit &mdash; the dressiest thing in this post and the one to want if your office has opinions. Light blue reads standard-issue from six feet away and feels like a polo from zero."),
]

def section(hid, h2, strong, kicker, items):
    cards = "\n".join(card(*it) for it in items)
    return (f'<h2 id="{hid}">{h2}</h2>\n'
            f'<p class="cat-kicker"><strong>{strong}</strong>{kicker}</p>\n'
            f'<div class="products-grid">\n{cards}\n</div>\n')

products = "\n".join([
 section("collabs","The Collabs","Six live collabs &middot; $45 to $150",
  "Criquet collaborates the way Austin institutions do &mdash; locally first. Zilker Belts and YETI are neighbors; Austin FC is the home team; the delisted Willie Nelson &ldquo;Willie Forever&rdquo; collection was the most Texas licensing deal in golf apparel. Jones and Discmania round out the out-of-state guest list. Everything below is live and buyable.", S1),
 section("core","The Core","Six staples &middot; $98 to $128",
  "The catalogue runs past a thousand SKUs, but it all radiates from one shirt: the four-button, flap-pocket, collar-stayed Players Shirt that started the company. The core today splits between that lineage and the honky-tonk side of the closet &mdash; pearl snaps, corduroy, terrycloth.", S2),
 section("newseason","The New Season","Six fall pieces &middot; $58 to $148",
  "The Early Fall drop is live now &mdash; long-sleeve Players Shirts in four colorways, a canvas pant, and a Lions badge tee that belongs in this town&rsquo;s golf conversation. Everything here works for the two weeks of actual autumn Austin receives.", S3),
])

FAQS = [
 ("Who founded Criquet Shirts?",
  "Billy Nachman and Hobson Brown, friends since kindergarten in Manhattan who grew up in prep-school polos and coat-and-tie dress codes. They founded Criquet in Austin in 2010, after Nachman found his late grandfather's vintage four-button golf shirt in a closet and the pair decided to rebuild it properly."),
 ("Where is Criquet based?",
  "Austin, Texas — the brand has said it plainly since day one: \"We founded Criquet here in 2010.\" Its longtime clubhouse-headquarters sat at 1603 South 1st Street in Bouldin Creek, complete with a putting green, an outdoor bar and a Bill Murray mural."),
 ("What is the Criquet Players Shirt?",
  "The signature: a four-button extended placket, a flap chest pocket, and removable collar stays so the collar lies flat instead of curling. The Classic runs $98 in 100 per cent Peruvian pima cotton, with Performance, Throwback, Terrycloth, Long Sleeve and Indigo Knit versions built on the same body."),
 ("Is Criquet organic cotton?",
  "That was the founding pitch — the original Players Shirt was built around organic cotton, and early press leaned on it. The current Classic Players Shirt is listed as 100 per cent Peruvian pima; the organic language has largely left the product pages, so check the specific item if that matters to you."),
 ("Did Criquet really do a Willie Nelson collection?",
  "Yes — an officially licensed \"Willie Forever\" collection sold on both criquetshirts.com and willienelson.com. It has since been delisted from Criquet's store, which makes it a collector's item and arguably the most Texas collab any golf-adjacent brand has done."),
 ("What is the Save Muny belt?",
  "A hand-stitched gaucho belt made with fellow Austin company Zilker Belts in a colorway supporting Save Muny, the campaign to preserve Lions Municipal Golf Course. It sells for $125 alongside a dozen other Criquet x Zilker designs, including Texas Exes and Moontowers."),
 ("Is Criquet a golf brand?",
  "Deliberately half of one. The brrr° cooling Range Polos and Players Shirts are genuine golf pieces — the brand was stocked at PGA Tour Superstore — but the stated thesis has always been \"comfortably off-course\": one shirt for the round, the office and the bar. The pearl snaps and corduroy are the other half of the argument."),
 ("What does Criquet cost?",
  "The core runs $98 to $128 — Classic Players at $98, Performance at $104, brrr° Range Polos and pearl snaps at $128. Collabs span $45 for the YETI bottle to $150 for the Jones duffle. Fall pieces top out at $148 for pants and knits."),
 ("Does Criquet make an Austin FC collection?",
  "Yes — officially licensed MLS gear, with the Coaches Players Shirt and Range Polo carrying Austin FC's tree crest and ATX marks in verde, black and white. It is part of a wider MLS x Criquet program that covers most of the league."),
 ("How big is Criquet?",
  "Bigger than it plays. The catalogue runs over a thousand products including licensed collegiate and MLS lines, the company raised a $1.4 million Series A led by CircleUp back in 2016, and the press file includes CNBC and Details magazine, which once called the Players Shirt \"The Perfect Polo.\""),
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
    <p>Every Texas golf story on this site eventually routes through Criquet, and it is time the brand got its own
    page. The short version: two friends who met in kindergarten in Manhattan &mdash; Billy Nachman and Hobson
    Brown, raised in prep-school polos and coat-and-tie dress codes &mdash; moved the idea to Austin and founded
    Criquet in 2010. The longer version starts in a closet, with the vintage golf shirt Nachman&rsquo;s grandfather
    left behind: four buttons, a long placket, a collar that had opinions. They rebuilt it &mdash; flap pocket,
    removable collar stays, an organic-cotton pitch that was ahead of its schedule &mdash; and called it the
    Players Shirt.</p>
    <p>The name, by the brand&rsquo;s own telling, comes from the sound of crickets &mdash; the noise of being
    comfortably off-course, which has been the thesis ever since. Criquet has never fully committed to being a golf
    brand, and that is the point. One side of the catalogue is Range Polos in brrr&deg; cooling fabric and Players
    Shirts you could tee off in at Butler. The other side is pearl snaps, corduroy and terrycloth &mdash; the
    honky-tonk half of the same closet. The customer is a person, not a handicap.</p>
    <p>What makes them unavoidable for us is how completely Austin they are. The longtime clubhouse-headquarters on
    South First had a putting green, an outdoor bar and a Bill Murray mural. The collab list reads like a city
    directory: Zilker Belts from across the river, YETI from up the road, the home team Austin FC under an official
    MLS license, and &mdash; in the most Texas licensing deal golf apparel has produced &mdash; a Willie Nelson
    &ldquo;Willie Forever&rdquo; collection, now delisted and gone. There is currently a belt in the store that
    says Save Muny and a tee wearing a Lions badge. A golf-adjacent brand carrying Lions Municipal merchandise is,
    around here, the highest available compliment.</p>
    <p>Below: the six live collabs, the six core pieces the company is actually built on, and six picks from the
    new fall drop. Sixteen years in, the $98 shirt that started it is still on the first page of their best-sellers.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>Austin, 2010</span></div>
      <div class="sidebar-detail"><span class="l">Founders</span><span>Nachman &amp; Brown</span></div>
      <div class="sidebar-detail"><span class="l">Signature</span><span>Players Shirt, $98</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$45 &ndash; $150</span></div>
      <a href="/"  class="sidebar-cta">&larr; Back to Feed</a>
      <div class="hashtags">
        <span class="hashtag">#TheGrassyIssue</span>
        <span class="hashtag">#Criquet</span>
        <span class="hashtag">#AustinGolf</span>
        <span class="hashtag">#MadeForTexas</span>
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
head = rep(head, r'<div class="drop-meta">.*?</div>', '<div class="drop-meta">\n    <span>18 Picks</span><span>&middot;</span><span>Austin, TX &middot; Est. 2010</span>\n  </div>')
head = rep(head, r'<div class="drop-hero"><div class="drop-hero-img"><img src="[^"]*" alt="[^"]*"[^>]*/></div></div>',
           f'<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}austinfc-3.jpg" alt="Criquet Austin FC Coaches Players Shirts at the clubhouse bar" style="object-position:center 30%;" /></div></div>')
head = rep(head, r'<div class="writeup">.*?</div>\s*</aside>\s*</div>', WRITEUP)

tail = rep(tail, r'<div class="more-grid">.*?</div>\s*</section>',
'''<div class="more-grid">
    <a href="/drops/texas-golf-brands-and-makers" class="more-card"><div class="more-kicker">Drops &amp; Brands</div><div class="more-title">Made in Texas &mdash; The Golf Brands and Makers Built Here</div></a>
    <a href="/drops/brand-revisited-jones-sports-co" class="more-card"><div class="more-kicker">Drops &amp; Brands</div><div class="more-title">Brand to Know &mdash; Jones Sports Co</div></a>
    <a href="/guides/hancock-golf-course-austin" class="more-card"><div class="more-kicker">Field Notes</div><div class="more-title">Hancock &mdash; The Oldest Course in Texas</div></a>
  </div>
</section>''')

page = head + '<section class="products">\n' + products + '\n<div class="faq">\n' + faq_html + '\n  </div>\n</section>' + tail
open(OUT, "w", encoding="utf-8").write(page)
words = len(re.sub(r'<[^>]+>',' ',page).split())
print(f"wrote {OUT} ({len(page):,} bytes, ~{words:,} words)")

# --- house voice guard -------------------------------------------------------
# Card copy and section kickers are owned by data/copy-deck.json, not by this
# script (see VOICE.md). Re-applying the deck here means a rebuild can never
# silently restore the pre-2026-08-27 copy. Safe to run repeatedly.
import subprocess as _sp, os as _os
_sp.run(["python3", _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "copy-deck.py"),
         "apply"], check=False)
