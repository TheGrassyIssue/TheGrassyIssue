#!/usr/bin/env python3
"""Build drops/no-budget-malbon.html — No Budget: Malbon, the 24 most expensive
things Malbon has ever sold or stocked, in stock or gone.

SOURCING (verified 2026-08-24/25):
  * Live prices/stock from malbongolf.com/products.json (1,068 products swept).
  * Honma sets from us.honmagolf.com collection JSON — live, in stock, $20,000/$5,800.
  * Bettinardi prices from bettinardi.com product JSON (Hive archive).
  * Delisted Jimmy Choo prices from Wayback captures of malbon.com's own product
    pages (Sunday Golf Bag $3,250, Duffle $2,095, Men's Diamond Shoe $850,
    Driver Cover $625). Shoe Bag $1,275 per Golf Digest first look, Apr 2024.
  * TAG Heuer $2,350 per Hypebeast/Golf Digest, Feb 2024. POTR ¥129,800 per
    Hypebeast, Jan 2023.
  * Banned word "worth" not used. All images local in /images/malbon-money/.
"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
MAN  = json.load(open('/tmp/malbon/manifest.json'))
TPL  = os.path.join(ROOT, "drops", "brand-to-know-midiron.html")
OUT  = os.path.join(ROOT, "drops", "no-budget-malbon.html")
SLUG = "no-budget-malbon"
TITLE = "No Budget: Malbon &mdash; the 24 Most Expensive Things They Have Ever Sold"
TITLE_TXT = "No Budget: Malbon — the 24 Most Expensive Things They Have Ever Sold"
DESC = ("From a $20,000 Honma club set to a $4,450 Jimmy Choo golf bag and one-of-five Bettinardi putters "
        "— the 24 priciest items Malbon has ever sold or stocked, ranked, with what is still buyable.")

IMG = "/images/malbon-money/"

def card(slug, brandstatus, name, price, desc, link):
    frames = MAN[slug]; n = len(frames)
    alt = re.sub(r'&[a-z]+;|&times;', '', re.sub(r'<[^>]+>', '', name))
    fr = "".join(f'<div class="pg-frame"><img src="{IMG}{f}" loading="lazy" alt="{alt} — Malbon high-ticket item"></div>' for f in frames)
    dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" aria-label="View image {i+1}"></button>' for i in range(n))
    return f'''  <div class="product-card" data-frames="{n}" id="{slug}">
    <div class="product-gallery"><div class="pg-track">{fr}</div><button class="pg-arw prev" aria-label="Previous image">&#8249;</button><button class="pg-arw next" aria-label="Next image">&#8250;</button><span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>
      <div class="product-body">
        <div class="product-brand">{brandstatus}</div>
        <div class="product-name">{name} &middot; {price}</div>
        <div class="product-desc">{desc}</div>
        <a href="{link}" target="_blank" rel="noopener" class="product-link">View &#8599;</a>
      </div>
  </div>'''

# ------------------------------------------------------------------ sections
S1 = [  # The Clubs
 ("honma-premium","Malbon &times; Honma &middot; In stock","Premium 14-Club Set","$20,000",
  "The most expensive thing with a Buckets logo on it, and it is not close. Fourteen clubs built on Honma&rsquo;s Beres line &mdash; the Japanese house that has been hand-finishing clubs in Sakata since 1959 &mdash; in black and gold for men and pink and gold for women, with headcovers and a bag included. Forbes reported in January that the sets were actually selling, which tells you more about Malbon&rsquo;s customer than any lookbook could. Sold through Honma&rsquo;s US store, not Malbon&rsquo;s, and still in stock.",
  "https://us.honmagolf.com/products/malbon-x-honma-mens-premium-set"),
 ("honma-performance","Malbon &times; Honma &middot; In stock","Performance 14-Club Set","$5,800",
  "The entry point to the same collaboration, if $5,800 can be called an entry point. Built on Honma&rsquo;s Beres NX platform, in a deep emerald for men and a rose-gold-accented set for women, fourteen clubs with the same included bag treatment. This is the one review outlets could actually get their hands on &mdash; MyGolfSpy called the collab &ldquo;culturally curated&rdquo; &mdash; and the one a scratch golfer could defend buying. Also still in stock at Honma.",
  "https://us.honmagolf.com/products/malbon-x-honma-mens-performance-set"),
 ("bet-fatcat","Malbon &times; Bettinardi &middot; Sold out","BB8 Tri DASS &ldquo;Buckets Fat Cat&rdquo; + NFT","$2,400",
  "March 2022, fifteen made, and a genuine piece of golf-equipment trivia: the first putter ever sold with an NFT attached. Double-aged stainless steel &mdash; Bettinardi&rsquo;s DASS, milled softer and rarer than their standard stock &mdash; with the Fat Cat Buckets character engraved across the flange. The NFT era did not age gracefully; the putter did. Fifteen units means you will essentially never see one.",
  "https://bettinardi.com/products/bb8-tri-dass-malbon-buckets-fat-cat"),
 ("bet-qb6","Malbon &times; Bettinardi &middot; Sold out","DASS QB6 Fancy Coil Neck &ldquo;Wizard Buckets&rdquo; 1 of 9","$2,300",
  "Where the whole Malbon putter story starts: May 2021, nine units, the first Malbon &times; Bettinardi drop ever. A double-aged stainless QB6 with a hand-formed fancy coil neck and the Wizard Buckets character on the face. Everything the two brands have done since &mdash; and they are still dropping together in 2026 &mdash; descends from these nine putters.",
  "https://bettinardi.com/collections/hive-malbon"),
 ("bet-3step","Malbon &times; Bettinardi &middot; Sold out","&ldquo;Gangster Buckets&rdquo; 3-Step Jam Tour Blast 1 of 5","$1,900",
  "One of a pair of five-unit runs from Bettinardi&rsquo;s April 2026 Hive release, with Buckets in a fedora doing his best mid-century mobster. Tour Blast finish on a 3-Step Jam neck &mdash; a genuine tour-department build, not a paint job on a retail head. Five made. Gone the morning it went up.",
  "https://bettinardi.com/products/malbon-x-bettinardi-gangster-buckets-3-step-jam-tour-blast-1-of-5-putter"),
 ("bet-ss3","Malbon &times; Bettinardi &middot; Sold out","&ldquo;Gangster Buckets&rdquo; SS3 Black Ox 1 of 5","$1,900",
  "The other half of the Gangster pair &mdash; a wide-body SS3 mallet in blacked-out Ox finish, same five-unit run, same April 2026 Hive drop, same instant sellout. Between the two Gangster one-of-fives and the plaid INOVAI below, Bettinardi&rsquo;s 2026 Malbon releases were the most limited putters either brand put out this year.",
  "https://bettinardi.com/products/malbon-x-bettinardi-gangster-buckets-ss3-black-ox-1-of-5-putter"),
 ("rollking-remington","Malbon &times; Roll King &middot; In stock","Remington Mallet &ldquo;Wiz Buckets&rdquo; Edition","$1,695",
  "Bettinardi is not Malbon&rsquo;s only putter partner. Roll King &mdash; the small-batch milling operation &mdash; builds the Wiz Buckets editions, a silver mallet with the wizard character engraved on the crown, sold right on Malbon&rsquo;s own site. Unlike everything above it on this list from the putter category, you can put this one in your bag today.",
  "https://malbongolf.com/products/roll-king-remington-mallet-putter-wiz-buckets-edition-right-silver"),
 ("rollking-luciano","Malbon &times; Roll King &middot; In stock","Luciano Blade &ldquo;Wiz Buckets&rdquo; Edition","$1,695",
  "The blade to the Remington&rsquo;s mallet, same $1,695, same Wiz Buckets engraving. The first Roll King &times; Malbon release, in July 2024, came forty at a time in numbered birch crates; the current silver editions sit in open stock. A heel-toe blade from a boutique mill for less than a one-of-five Bettinardi resells for &mdash; the closest thing this list has to sensible.",
  "https://malbongolf.com/products/roll-king-luciano-blade-putter-wiz-buckets-edition-silver"),
]
S2 = [  # The Jimmy Choo Wing
 ("jc-golf-bag","Jimmy Choo &times; Malbon &middot; In stock","2.0 Golf Bag","$4,450",
  "The most expensive item on Malbon&rsquo;s own store, full stop. A denim-and-leather carry bag, water-treated, in the collab&rsquo;s latte-green-pink monogram with an embroidered Buckets. The first Jimmy Choo bag, in April 2024, sold through with ten of the collection&rsquo;s twenty-seven pieces gone in half an hour; this 2.0 version is &mdash; as of this writing &mdash; still buyable.",
  "https://malbongolf.com/products/jimmy-choo-x-malbon-golf-bag-latte-malbon-green-malbon-pink"),
 ("jc-sunday-bag","Jimmy Choo &times; Malbon &middot; Sold out","Sunday Golf Bag","$3,250",
  "A $3,250 Sunday bag &mdash; the format invented for carrying six clubs and nothing else &mdash; is either the funniest or the most honest product in the entire collab, depending on your mood. Monogram canvas with leather trim from the April 2025 2.0 collection, now delisted from Malbon&rsquo;s store entirely. Price per club carried: about $540.",
  "https://malbongolf.com/collections/jimmy-choo"),
 ("jc-duffle","Jimmy Choo &times; Malbon &middot; Sold out","Duffle Bag","$2,095",
  "The quiet one nobody wrote headlines about: a full monogram duffle with green leather trim that outpriced the TAG Heuer watch and every putter on this page except the Fat Cat. Sold on Malbon&rsquo;s site through the 2.0 run and now gone from the catalogue &mdash; the price above is from Malbon&rsquo;s own archived product page.",
  "https://malbongolf.com/collections/jimmy-choo"),
 ("jc-shoebag","Jimmy Choo &times; Malbon &middot; Sold out","Crystal-Embellished Shoe Bag","$1,275",
  "From the original April 2024 collection &mdash; a leather bag for carrying your golf shoes, finished with Jimmy Choo&rsquo;s crystal work. It is the piece that made the first drop read as genuine Jimmy Choo rather than a licensing exercise, and it sold out at Malbon accordingly. Golf Digest put the price at $1,275 in its first look.",
  "https://us.jimmychoo.com/en/men/bags-and-accessories/jimmy-choo-malbon-shoe-bag/"),
 ("jc-diamond-womens","Jimmy Choo &times; Malbon &middot; Sold out","Women&rsquo;s Diamond Golf Shoe","$850",
  "An actual spiked golf shoe from an actual luxury shoemaker &mdash; leather, green-trimmed, with Jimmy Choo&rsquo;s diamond-pattern sole treatment adapted for turf. Still listed on Malbon&rsquo;s store, every size gone. The 2024 originals came in five colorways and were the fastest sellers of the launch.",
  "https://malbongolf.com/products/jimmy-choo-x-malbon-womens-diamond-golf-shoe-latte-malbon-green"),
 ("jc-diamond-mens","Jimmy Choo &times; Malbon &middot; Sold out","Men&rsquo;s Diamond Golf Shoe","$850",
  "The men&rsquo;s build of the same shoe &mdash; white leather, green heel tab, monogram detailing &mdash; at the same $850, verified from Malbon&rsquo;s own archived listing. For scale: that is Jones Sports Co stand bag money for one pair of golf shoes, and they sold anyway.",
  "https://malbongolf.com/collections/jimmy-choo"),
 ("jc-slide","Jimmy Choo &times; Malbon &middot; In stock","Men&rsquo;s Slide","$750",
  "A $750 pool slide in the collab monogram, with an embroidered Buckets in a bucket hat over the toe. This is the piece to point at when someone asks what the Jimmy Choo partnership is actually for &mdash; it has nothing to do with golf and everything to do with the clubhouse afterwards. In stock.",
  "https://malbongolf.com/products/jimmy-choo-x-malbon-mens-slide-latte-malbon-green"),
 ("jc-driver-cover","Jimmy Choo &times; Malbon &middot; Sold out","Driver Cover","$625",
  "A cylindrical monogram driver cover at $625 &mdash; more than most drivers&rsquo; street price a season after release. Sold through the collab collection on Malbon&rsquo;s site and now delisted; the price is from Malbon&rsquo;s archived page, not a resale listing.",
  "https://malbongolf.com/collections/jimmy-choo"),
]
S3 = [  # The Objects
 ("tag-malbon","TAG Heuer &times; Malbon &middot; Sold out","Connected Calibre E4 Golf Edition","$2,350",
  "February 2024: a Swiss watchmaker hands its connected golf watch to Malbon. Eighteen bezel markings for eighteen holes, a Buckets watch face that shifts color as the seconds pass, shot-tracking and caddie-style hole data built in. It released on Malbon&rsquo;s site alongside a small apparel capsule and has since disappeared from the catalogue &mdash; the only watch Malbon has ever sold.",
  "https://hypebeast.com/2024/2/tag-heuer-malbon-golf-collaboration-connected-watch-apparel"),
 ("monzee-camo","Malbon &times; Monzee &middot; In stock","ROBA Cover Camo","$1,500",
  "A fifteen-hundred-dollar plush headcover. The ROBA is a full custom character &mdash; limbs, face, attitude &mdash; in an abstract camo print that Malbon notes varies piece to piece, which is the polite way of saying each one is cut differently on purpose. The single most expensive headcover the brand has ever stocked, and the camo is somehow still available.",
  "https://malbongolf.com/products/monzee-roba-cover-camo-camo-mix"),
 ("monzee-black","Malbon &times; Monzee &middot; Sold out","ROBA Cover Black","$1,500",
  "The blackout version of the same character &mdash; all-black plush, horned, vaguely demonic in the best way &mdash; and the one that actually sold out. If you want a read on where headcover culture is in 2026: the $1,500 black plush monster went before the camo did.",
  "https://malbongolf.com/products/monzee-roba-cover-black-black"),
 ("potr-transcon","POTR &times; Malbon &middot; Sold out","Transcon Golf Bag","&yen;129,800 (about $999)",
  "January 2023, Japan only. POTR is the younger line from Yoshida &amp; Co. &mdash; the Tokyo house behind Porter, whose bags occupy roughly the same cultural slot in Japan that Malbon does in LA. The Transcon was a black ballistic golf bag sold exclusively through Porter&rsquo;s Japanese channels at &yen;129,800, never restocked, and never sold in the US at all. The grail on this list that money least helps with.",
  "https://hypebeast.com/2023/1/porter-malbon-golf-transcon-bag-release-info"),
 ("bet-inovai","Malbon &times; Bettinardi &middot; Sold out","&ldquo;Gangster Buckets&rdquo; INOVAI 6.0 Maroon Plaid","$900",
  "The volume release from the April 2026 Gangster drop, if a putter that sold out in a morning can be called volume. An INOVAI 6.0 mallet wrapped in a maroon plaid finish with a matching mag-closure cover &mdash; the loudest thing Bettinardi milled this year, and the cheapest way anyone got into the Gangster Buckets release.",
  "https://bettinardi.com/products/malbon-x-bettinardi-gangster-buckets-inovai-6-0-maroon-plaid-putter"),
 ("xo-rod","Malbon &times; XO Skeleton &middot; In stock","Epitome MB725 Fishing Rod","$575",
  "Not a typo and not golf: a US-built bass fishing rod with carbon guides and an integrated carbon reel seat, from Malbon&rsquo;s May 2026 &ldquo;Golf &amp; Bass&rdquo; drop. The logic &mdash; same customer, same Saturday, different body of water &mdash; is either genius or completely unhinged, and the fact that it is still in stock suggests the market has not decided either.",
  "https://malbongolf.com/products/xo-skeleton-epitome-mb725-with-carbon-guides-black"),
]
S4 = [  # The $498 Club
 ("bettinardi-cartbag","Malbon &times; Bettinardi &middot; Sold out","Bettinardi Cart Bag","$498",
  "The two putter houses&rsquo; partnership extended to a full leather-look cart bag &mdash; polyurethane shell, tan and navy panelling, both logos riding together. At $498 it was priced like Malbon&rsquo;s own house cart bags and sold out anyway, because it is the only bag either brand has made together.",
  "https://malbongolf.com/products/bettinardi-cart-bag-multi"),
 ("knicks-varsity","Malbon &times; NBA &middot; In stock","Knicks &ldquo;The Garden&rdquo; Varsity Jacket","$498",
  "Wool body, contrast leather sleeves, Knicks orange-and-blue blocking, and a Buckets heart on the back &mdash; from Malbon&rsquo;s NBA run. Nothing on this page says more about where Malbon sits in 2026: a golf brand selling a $498 basketball varsity jacket, in stock, at Madison Square Garden prices.",
  "https://malbongolf.com/products/knicks-the-garden-varsity-jacket-blue"),
]

def section(hid, kicker_strong, kicker_txt, items):
    cards = "\n".join(card(*it) for it in items)
    return (f'<h2 id="{hid}">{kicker_strong[0]}</h2>\n'
            f'<p class="cat-kicker"><strong>{kicker_strong[1]}</strong>{kicker_txt}</p>\n'
            f'<div class="products-grid">\n{cards}\n</div>\n')

products = "\n".join([
 section("clubs",("The Clubs","Eight builds &middot; $1,695 to $20,000"),
  "Half this list is putters and club sets, which tracks: clubs are where golf hides its real money. Malbon has three equipment partners &mdash; Honma in Sakata, Bettinardi in Chicago, Roll King in small-batch runs &mdash; and between them they account for the single most expensive Malbon item ever sold and the most limited, a nine-unit run from 2021.", S1),
 section("jimmychoo",("The Jimmy Choo Wing","Eight pieces &middot; $625 to $4,450"),
  "No partnership has printed money like this one. Two collections &mdash; April 2024 and the 2.0 run in April 2025 &mdash; put a luxury shoemaker&rsquo;s monogram on golf bags, spiked shoes and slides. Ten of the first drop&rsquo;s twenty-seven pieces sold out inside thirty minutes. Every price below is from Malbon&rsquo;s own listings, live or archived; most of the collection is now delisted entirely.", S2),
 section("objects",("The Objects","Six items &middot; $575 to $2,350"),
  "The strangest shelf in the archive: a Swiss connected watch, a pair of $1,500 plush creatures, a Japan-only Porter golf bag, a plaid putter and a bass fishing rod. This is the stuff that makes the brand collectible rather than just successful.", S3),
 section("four98",("The $498 Club","Two pieces &middot; both $498"),
  "The floor of this list still costs as much as a full Sunday-bag setup from most independent brands. Two very different ways to spend the same money &mdash; one gone, one live.", S4),
])

FAQS = [
 ("What is the most expensive thing Malbon has ever sold?",
  "The Malbon x Honma Premium 14-club set at $20,000 — black and gold for men, pink and gold for women, built on Honma's Beres line with headcovers and a bag included. It is sold through Honma's US store rather than malbongolf.com, and as of late August 2026 it is still in stock. On Malbon's own store, the most expensive item ever listed is the $4,450 Jimmy Choo x Malbon 2.0 Golf Bag."),
 ("Does Malbon make golf clubs?",
  "Not by itself — it partners. Honma builds the $20,000 and $5,800 club sets, Bettinardi has milled limited putters with Malbon since May 2021, and Roll King produces the $1,695 Wiz Buckets putters sold on Malbon's own site. There is no Malbon-manufactured club."),
 ("Is there a Malbon x Scotty Cameron putter?",
  "No. Despite what resale listings occasionally imply, Malbon's only putter partners have been Bettinardi (since 2021) and Roll King (since 2024). Any putter marketed as Malbon x Scotty Cameron is not an official product."),
 ("What was the Jimmy Choo x Malbon collab?",
  "Two collections. The first, in April 2024, was twenty-seven pieces — golf bags, spiked Diamond golf shoes, slides, covers and accessories in a latte-green-pink monogram — and ten pieces sold out within about thirty minutes. A 2.0 collection followed in April 2025 with the $4,450 Golf Bag, a $3,250 Sunday bag and a $2,095 duffle. Most of it is now delisted from Malbon's store; a few 2.0 pieces remain live."),
 ("Are the Bettinardi x Malbon putters still available?",
  "Not at retail. Every release — from the nine-unit 2021 Wizard Buckets QB6 to the April 2026 Gangster Buckets one-of-fives — sold out, and Bettinardi archives them in its Hive section afterwards. The only Malbon putters buyable at retail right now are the Roll King Wiz Buckets editions at $1,695 on Malbon's site."),
 ("What is the TAG Heuer x Malbon watch?",
  "A Malbon edition of TAG Heuer's Connected Calibre E4 Golf smartwatch, released February 26, 2024 at $2,350. It carried a bezel with eighteen markings for the eighteen holes, a color-shifting Buckets watch face, and the standard Connected golf features — automatic shot tracking and hole-by-hole distances. It has since disappeared from Malbon's catalogue and was never restocked."),
 ("What is the POTR x Malbon Transcon bag?",
  "A January 2023 golf bag made with POTR, the younger label from Yoshida & Co., the Tokyo maker behind Porter. It sold only through Porter's Japanese channels at ¥129,800 — roughly $999 at the time — was never restocked and never officially sold in the United States, which makes it one of the hardest Malbon items to find."),
 ("Why are Malbon headcovers $1,500?",
  "The two Monzee ROBA covers are less headcovers than plush art objects — full custom characters with limbs and faces, each camo version cut slightly differently. They are the most expensive covers Malbon has ever stocked by a factor of three, and the black one sold out before the camo."),
 ("Did Daniel Arsham make anything expensive with Malbon?",
  "Surprisingly, no. The Arsham x Malbon collections top out at the $448 Stealth Cart Bag and the $428 Cloudburst rain jacket — no putter, sculpture or four-figure piece was ever retailed through Malbon, whatever the resale market implies."),
 ("Does Malbon sell anything besides golf gear?",
  "Increasingly, yes. This list alone includes a Swiss smartwatch, a $498 Knicks varsity jacket from the NBA partnership, a $750 Jimmy Choo pool slide and a $575 US-built bass fishing rod from the May 2026 Golf & Bass drop. The through-line is the customer, not the sport."),
]

faq_html = "\n".join(
  f'    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>' for q,a in
  [(q.replace('"','&quot;'), a) for q,a in FAQS])

faq_ld = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":re.sub('<[^>]+>','',q),"acceptedAnswer":{"@type":"Answer","text":re.sub('<[^>]+>','',a)}} for q,a in FAQS]}, ensure_ascii=False)

art_ld = json.dumps({"@context":"https://schema.org","@type":"Article","headline":TITLE_TXT,
 "description":re.sub('&mdash;','—',DESC),
 "author":{"@type":"Organization","name":"The Grassy Issue"},
 "publisher":{"@type":"Organization","name":"The Grassy Issue"},
 "datePublished":"2026-08-25","dateModified":"2026-08-25",
 "mainEntityOfPage":f"https://thegrassyissue.com/drops/{SLUG}"}, ensure_ascii=False)

WRITEUP = '''<div class="writeup">
  <div class="writeup-body">
    <p>Malbon gets covered two ways: as the brand that made golf cool for people who skateboard, or as the brand
    that charges $60 for a rope hat. Both miss the more interesting story, which is at the top of the price list.
    Since Stephen and Erica Malbon started the label in 2017, it has quietly built a luxury tier that almost no
    golf brand &mdash; independent or otherwise &mdash; has attempted: five-figure club sets, four-figure bags with
    an actual luxury house, one-of-five putters, a Swiss smartwatch.</p>
    <p>So we ranked it. We swept all 1,068 products on Malbon&rsquo;s current store, then went digging for the
    delisted and the archived &mdash; Wayback captures of Malbon&rsquo;s own product pages, Bettinardi&rsquo;s Hive
    archive, Honma&rsquo;s US store, the Japanese release that never came to America. These are the 24 most
    expensive things Malbon has ever sold or stocked, at original retail. No resale prices anywhere on this page.</p>
    <p>Three things stood out. First, the ceiling is higher than anyone assumes &mdash; the Honma Premium set costs
    more than the next four items combined, and Forbes reported in January that it was genuinely selling. Second,
    the Jimmy Choo partnership is the most commercially serious luxury collab in golf, with eight of the 24 slots
    on this list. Third, some of it is still sitting there: nine of the 24 are in stock right now, including the
    $20,000 set, the $4,450 bag and both Roll King putters. The other fifteen are gone, some &mdash; like the
    nine-unit 2021 Bettinardi &mdash; permanently.</p>
    <p>Prices shown are original retail, in USD except the Japan-only POTR bag. Stock status was checked August 24, 2026.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Items</span><span>24</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$498 &ndash; $20,000</span></div>
      <div class="sidebar-detail"><span class="l">Still in stock</span><span>9 of 24</span></div>
      <div class="sidebar-detail"><span class="l">Partners</span><span>8</span></div>
      <a href="/"  class="sidebar-cta">&larr; Back to Feed</a>
      <div class="hashtags">
        <span class="hashtag">#TheGrassyIssue</span>
        <span class="hashtag">#Malbon</span>
        <span class="hashtag">#NoBudget</span>
        <span class="hashtag">#GolfCulture</span>
      </div>
    </div>
  </aside>
</div>'''

# ------------------------------------------------------------------ assemble
tpl = open(TPL, encoding="utf-8").read()

head, rest = tpl.split('<section class="products">', 1)
_, tail = rest.split('</section>', 1)   # tail starts before <section class="more">

# --- head replacements
def rep(s, pat, new, count=0):
    out, n = re.subn(pat, new, s, count=count, flags=re.S)
    assert n > 0, pat
    return out

head = rep(head, r'<title>.*?</title>', f'<title>{TITLE_TXT} | The Grassy Issue</title>', 1)
head = rep(head, r'<meta name="description" content=".*?"', f'<meta name="description" content="{DESC}"', 1)
head = rep(head, r'<meta property="og:url" content=".*?"', f'<meta property="og:url" content="https://thegrassyissue.com/drops/{SLUG}"', 1)
head = rep(head, r'<meta property="og:title" content=".*?"', f'<meta property="og:title" content="{TITLE_TXT}"', 1)
head = rep(head, r'<meta property="og:description" content=".*?"', f'<meta property="og:description" content="{DESC}"', 1)
head = rep(head, r'<meta name="twitter:title" content=".*?"', f'<meta name="twitter:title" content="{TITLE_TXT}"', 1)
head = rep(head, r'<meta name="twitter:description" content=".*?"', f'<meta name="twitter:description" content="{DESC}"', 1)
head = rep(head, r'<link rel="canonical" href=".*?"', f'<link rel="canonical" href="https://thegrassyissue.com/drops/{SLUG}"', 1)
head = rep(head, r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "Article".*?</script>',
           f'<script type="application/ld+json">{art_ld}</script>', 1)
head = rep(head, r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "FAQPage".*?</script>',
           f'<script type="application/ld+json">{faq_ld}</script>', 1)
# breadcrumb + header
head = rep(head, r'(<div class="breadcrumb">.*?<span>/</span>\s*)[^<]*?(</div>)',
           r'\1' + TITLE_TXT.replace('\\','') + r'\2', 1)
head = rep(head, r'<h1>.*?</h1>', f'<h1>{TITLE}</h1>', 1)
head = rep(head, r'<div class="drop-meta">.*?</div>', '<div class="drop-meta">\n    <span>24 Items</span><span>&middot;</span><span>$498 &ndash; $20,000</span>\n  </div>', 1)
head = rep(head, r'<div class="drop-hero"><div class="drop-hero-img"><img src="[^"]*" alt="[^"]*" /></div></div>',
           f'<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}honma-premium-0.jpg" alt="Malbon x Honma Premium black and gold driver — the most expensive Malbon item ever sold" /></div></div>', 1)
head = rep(head, r'<div class="writeup">.*?</div>\s*</aside>\s*</div>', WRITEUP, 1)

# --- more-from-feed in tail
tail = rep(tail, r'<div class="more-grid">.*?</div>\s*</section>',
'''<div class="more-grid">
    <a href="/drops/no-budget" class="more-card"><div class="more-kicker">The Edit</div><div class="more-title">No Budget &mdash; The Most Expensive Golf Gear We Could Find</div></a>
    <a href="/drops/arsham-malbon-chapter-three" class="more-card"><div class="more-kicker">The Drop</div><div class="more-title">Arsham &times; Malbon &mdash; Chapter Three</div></a>
    <a href="/drops/malbon-fall-2026-the-ironworks-collection" class="more-card"><div class="more-kicker">The Drop</div><div class="more-title">Malbon Fall 2026 &mdash; Ironworks</div></a>
  </div>
</section>''', 1)

page = head + '<section class="products">\n' + products + '\n<div class="faq">\n' + faq_html + '\n  </div>\n</section>' + tail
open(OUT, "w", encoding="utf-8").write(page)
words = len(re.sub(r'<[^>]+>',' ',page).split())
print(f"wrote {OUT}  ({len(page):,} bytes, ~{words:,} words)")
