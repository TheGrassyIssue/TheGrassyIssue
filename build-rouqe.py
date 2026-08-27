#!/usr/bin/env python3
"""
Builds /drops/brand-to-know-rouqe-golf.

BRAND TO KNOW — Rouqe Golf (rouqegolf.com). Men's collection in depth, women's
highlights, and the brand's own on-course photography.

FOUNDER: NOT ESTABLISHED, and the post says so plainly. Checked the site (no
/pages/about — it 404s), Instagram, TikTok, Facebook, LinkedIn, press, podcasts.
WHOIS is privacy-shielded via Domains By Proxy. The only named person anywhere
is Marko Mijaljevic, Head of Design. DO NOT attribute founding to him.

QUOTE — verbatim, from his own portfolio at markomijaljevic.com/rouqe-golf:
  "As Head of Design at Rouqe Golf, I oversee the creative direction of the
   brand, designing seasonal apparel collections, graphics, and visual assets
   that bridge the gap between golf and modern fashion."
  He is separately credited with the SS25 collection (garment design and product
  development) on his NOVA portfolio listing. This is the ONLY sourced quote
  connected to the brand — a second sweep found nothing else.

DATING: rouqegolf.com was registered 2023-04-23 (public WHOIS). That dates the
domain, not the company. The copy says "the domain was registered in spring
2023" rather than asserting a founding year.

VERIFIED FROM THE STORE (2026-08-27, via products.json):
  54 products total — men's collection 21, women's 23.
  Men's: 12 of 21 sold out. Women's: 9 of 23.
  Polos $59-79 | mock necks $59 | knit polos $34 | tees $29 | skorts $69
  dresses $89 | sweaters $39-89 | hats $49 | headcovers $24-34, 3-pack $79
  towel $19 | sunglasses $19 | bag $199. All CAD. Free shipping over $150.
  Legal name "Rouqe Golf Inc" per the Shopify Shop app listing.
  DTC only — no stockists or wholesale found anywhere.

IMAGERY: their lookbook page (/pages/look-book) renders empty — the third-party
gallery app loads nothing. All photography here comes from the product images
themselves, which is where their on-course work actually lives. Frames were
auto-ranked by corner-colour variance so location shots lead and flat studio
packshots fall to the back. Zero landscape frames exist in the entire 233-image
set, so the hero is a scenic portrait cropped where the horizon carries it.

NOT ASSERTED, deliberately: that the brand is Canadian-based (the storefront
defaults to Canada and prices in CAD, which is not the same thing), any founding
year, any collab or tour partnership, and anything from Instagram or TikTok —
both blocked unauthenticated reads, so no caption or follower claims are made.
"""
import json, os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
IMGDIR = os.path.join(ROOT, "images", "rouqe")
IMG  = "/images/rouqe/"
TPL  = os.path.join(ROOT, "drops", "brand-to-know-midiron.html")
SLUG = "brand-to-know-rouqe-golf"
OUT  = os.path.join(ROOT, "drops", SLUG + ".html")
TITLE = "Brand to Know &mdash; Rouqe Golf, the Label Built on Mock Necks and Retro Stripes"
TITLE_TXT = "Brand to Know — Rouqe Golf, the Label Built on Mock Necks and Retro Stripes"
DESC = ("Rouqe Golf makes retro-striped polos, mock necks and skorts, shoots its own campaigns on a "
        "sun-bleached mountain course, and sells out of most of it. A full look at the men's collection, "
        "the women's highlights, and what the brand does and doesn't tell you.")

def frames(key):
    fs = sorted(glob.glob(os.path.join(IMGDIR, f"{key}-*.jpg")),
                key=lambda p: int(re.search(r'-(\d+)\.jpg$', p).group(1)))
    return [os.path.basename(f) for f in fs]

def card(key, name, kicker, desc, link):
    fr_files = frames(key)
    n = len(fr_files)
    assert n, f"no frames for {key}"
    fr = "".join(f'<div class="pg-frame"><img src="{IMG}{f}" loading="lazy" '
                 f'alt="Rouqe Golf {name} &middot; view {i+1} of {n}"></div>'
                 for i, f in enumerate(fr_files))
    dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" '
                   f'aria-label="View image {i+1}"></button>' for i in range(n))
    return f'''  <div class="product-card" id="{key}" data-frames="{n}">
    <div class="product-gallery"><div class="pg-track">{fr}</div><button class="pg-arw prev" aria-label="Previous image">&#8249;</button><button class="pg-arw next" aria-label="Next image">&#8250;</button><span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>
      <div class="product-body">
        <div class="product-brand">{kicker}</div>
        <div class="product-name">{name}</div>
        <div class="product-desc">{desc}</div>
        <a href="{link}" target="_blank" rel="noopener" class="product-link">Shop Rouqe Golf &#8599;</a>
      </div>
  </div>'''

MENS = [
 ("brown-mock-neck", "Brown Mock Neck", "Mock neck &middot; $59",
  "The piece that sums the brand up. A short-sleeve mock in a deep chocolate brown, worn in their own campaign against dry grass and a cart path at golden hour. The mock neck is Rouqe&rsquo;s signature silhouette &mdash; they make it in six colours and it is the thing that separates them from every label defaulting to a three-button placket.",
  "https://rouqegolf.com/collections/mens"),
 ("burgundy-stripe", "Burgundy Striped Polo", "Polo &middot; $69 &middot; sold out",
  "The best-looking thing they have made. Wide burgundy and cream rugby stripes, boxy through the body, worn in the campaign with a navy script cap. It reads more 1974 club pro than 2026 performance polo, and it is gone &mdash; which tells you what the customer responded to.",
  "https://rouqegolf.com/collections/mens"),
 ("blue-blade-collar", "Blue Blade Collar", "Polo &middot; $69",
  "Pale blue, blade collar, no placket buttons visible from the front. The cleanest men&rsquo;s piece in the range and the one that photographs best on course &mdash; their own shoot puts it against a bleached hillside and lets the colour do the work.",
  "https://rouqegolf.com/collections/mens"),
 ("green-mock-neck", "Green Mock Neck", "Mock neck &middot; $59",
  "Sage green, the colour the brand keeps returning to across both collections. Same mock silhouette as the brown. Shot on a hilltop tee with a valley and a lake behind, which is a long way from the usual white-cyc studio most labels this size can afford.",
  "https://rouqegolf.com/collections/mens"),
 ("script-ls", "Script Long-Sleeve Polo", "Long sleeve &middot; $79 &middot; sold out",
  "Black with cream banding across the chest and a cursive script logo. The most overtly retro thing they make, and the most expensive men&rsquo;s piece at seventy-nine dollars. Also sold out, which is the recurring theme here.",
  "https://rouqegolf.com/collections/mens"),
 ("bw-stripe", "B/W Striped Polo", "Polo &middot; $69 &middot; sold out",
  "Fine black and cream horizontal stripes with a white collar and placket. Closer to a Breton than a golf shirt. Where the burgundy is loud, this is the version you could wear to lunch afterwards without anyone asking about your round.",
  "https://rouqegolf.com/collections/mens"),
 ("two-tone", "Two Tone Polo Blue", "Polo &middot; $69",
  "Royal blue yoke over a white body, with the script mark small on the back of the neck. A colour-blocked shape that has been in and out of golf since the eighties, executed here without the usual contrast piping.",
  "https://rouqegolf.com/collections/mens"),
 ("eagle-polo", "Eagle Polo Black", "Polo &middot; $69 &middot; sold out",
  "Plain black with a small embroidered eagle at the chest. Their studio photography goes dark and moody for this one &mdash; hard light, black background, styled far closer to a streetwear campaign than a golf catalogue.",
  "https://rouqegolf.com/collections/mens"),
 ("roq-polo", "ROQ Polo", "Polo &middot; $69 &middot; sold out",
  "An all-over black and white houndstooth-adjacent print with a solid white collar. The busiest thing in the men&rsquo;s range and a reminder that Rouqe is not only doing quiet tonal basics.",
  "https://rouqegolf.com/collections/mens"),
 ("knit-beige", "&ldquo;R&rdquo; Knit Sweater Beige", "Sweater &middot; $59",
  "Cream knit with an outsized cursive R across the front in a contrasting tone. The kind of piece that works better in the clubhouse than in the swing, and priced thirty dollars under the black version of the same sweater.",
  "https://rouqegolf.com/collections/mens"),
 ("rq-sweater", "RQ Sweater", "Sweater &middot; $39",
  "The value item of the whole store. Black with a cream chevron across the chest, thirty-nine dollars, and shot in the campaign against a deep maroon studio backdrop with a putter and a cigarette-club-champion energy that the price does not suggest.",
  "https://rouqegolf.com/collections/mens"),
]

WOMENS = [
 ("w-dress-black", "&ldquo;R&rdquo; Dress Black", "Dress &middot; $89 &middot; sold out",
  "The flagship, and the most expensive piece Rouqe makes. Sleeveless, collared, cut close through the body with a pleated skirt that moves. Shot on a fairway with mountains behind and no styling tricks &mdash; it does not need them. Gone in both colourways.",
  "https://rouqegolf.com/collections/womens"),
 ("w-dress-pink", "&ldquo;R&rdquo; Dress Pink", "Dress &middot; $89 &middot; sold out",
  "Same cut in a soft rose. Where the black version reads severe, this one is the summer-member-guest answer, and Rouqe photographs it hard &mdash; golden hour, a pink headcover to match, the whole look built around the one piece.",
  "https://rouqegolf.com/collections/womens"),
 ("w-black-skort", "Black Skort", "Skort &middot; $69 &middot; sold out",
  "Nine images on the product page, more than anything else in the store, and they use every one of them &mdash; front, back, in motion, the crossover waistband in close-up. Short, pleated, and clearly the piece the brand expects to carry the women&rsquo;s line.",
  "https://rouqegolf.com/collections/womens"),
]

ACCESSORIES = [
 ("acc-headcovers", "Script Head Covers, 3 Pack", "Headcovers &middot; $79 &middot; sold out",
  "Brown with the cursive script mark, sold as driver, wood and hybrid together for seventy-nine &mdash; twelve dollars less than buying the three separately. The only hard goods Rouqe makes, and the thing most likely to get noticed on a bag.",
  "https://rouqegolf.com/collections/accessories"),
 ("acc-towel", "RQ Jacquard Towel", "Towel &middot; $19 &middot; sold out",
  "Nineteen dollars and jacquard-woven rather than printed, which means the pattern is in the weave and will not crack off after a season. The cheapest thing in the store and the easiest way to try the brand.",
  "https://rouqegolf.com/collections/accessories"),
 ("acc-hat", "Eagle Hat Green", "Hat &middot; $49 &middot; sold out",
  "Rope-free five-panel in a deep green with the eagle mark embroidered at the front. Rouqe makes five hats and every single one is sold out, which is either very good demand planning or none at all.",
  "https://rouqegolf.com/collections/accessories"),
]

WILD = [
 ("shorts-black", "Straight Cut Shorts", "Shorts &middot; $69",
  "Photographed from behind on a fairway, glove in the back pocket, burgundy stripe polo above. The only shorts in the men&rsquo;s collection, cut straight rather than tapered.",
  "https://rouqegolf.com/collections/mens"),
 ("range-tee", "Range Tee Black", "Tee &middot; $29",
  "Boxy cotton tee with a script chest hit and a large back print. Twenty-nine dollars, and the piece the brand uses as its entry point on social.",
  "https://rouqegolf.com/collections/mens"),
 ("fw24-green", "F/W 24 Polo Green", "Polo &middot; $69 &middot; sold out",
  "Racing green with a white collar and the cursive wordmark set large across the chest. The detail photography on this one is the best on the site &mdash; close enough to read the stitch.",
  "https://rouqegolf.com/collections/mens"),
]

def section(hid, h2, strong, kicker, items):
    return (f'<h2 id="{hid}">{h2}</h2>\n'
            f'<p class="cat-kicker"><strong>{strong}</strong>{kicker}</p>\n'
            f'<div class="products-grid">\n' + "\n".join(card(*it) for it in items) + '\n</div>\n')

QUOTE = ('\n<div class="pull-quote">\n'
         '  <div class="pull-quote-inner">&ldquo;As Head of Design at Rouqe Golf, I oversee the creative '
         'direction of the brand, designing seasonal apparel collections, graphics, and visual assets that '
         'bridge the gap between golf and modern fashion.&rdquo;'
         '<span class="pull-quote-attr">&mdash; Marko Mijaljevic, Head of Design, Rouqe Golf</span></div>\n</div>\n')

products = (
 section("mens", "The Men&rsquo;s Collection", "Eleven of twenty-one &middot; polos, mocks, knits",
   "The men&rsquo;s side runs to twenty-one pieces and twelve of them are sold out, so this is as much an "
   "archive as a shopping list. Mock necks and retro stripes are the throughline.", MENS)
 + QUOTE +
 section("womens", "From the Women&rsquo;s Side", "Three &middot; the dresses and the skort",
   "The women&rsquo;s collection is the larger of the two and carries the higher price points. These are the "
   "three that define it &mdash; and all three are sold out.", WOMENS)
 + section("accessories", "The Accessories", "Three &middot; headcovers, towel, hat",
   "A short list, because Rouqe barely makes any. Headcovers, a towel, sunglasses, five hats and one bag &mdash; and almost the entire category is currently unavailable.", ACCESSORIES)
 + section("wild", "In the Wild", "Three &middot; the brand&rsquo;s own course photography",
   "Rouqe shoots its own campaigns on what looks like a dry mountain course at golden hour, and the "
   "results carry more atmosphere than most labels ten times the size manage.", WILD)
)

FAQS = [
 ("What is Rouqe Golf?",
  "A direct-to-consumer golf apparel label selling polos, mock necks, tees, skorts, dresses, knit sweaters, hats, headcovers and accessories through its own Shopify store at rouqegolf.com. The storefront defaults to Canada and prices in Canadian dollars. The legal name appears as Rouqe Golf Inc."),
 ("Who founded Rouqe Golf?",
  "Not publicly named. There is no About page on the site — it returns a 404 — and no founder is credited on the store, in any press, or in any interview we could find. The domain's WHOIS record is privacy-shielded. The only named person connected to the brand is Marko Mijaljevic, its Head of Design, who is credited with the SS25 collection. He is not described anywhere as the founder and we are not treating him as one."),
 ("How much does Rouqe Golf cost?",
  "Polos run $59 to $79, mock necks $59, knit polos $34, tees $29, skorts $69, dresses $89, sweaters $39 to $89, hats $49, headcovers $24 to $34 with a three-pack at $79, towels and sunglasses $19 each, and the golf bag $199. All Canadian dollars. Shipping is free over $150."),
 ("Is Rouqe Golf men's or women's?",
  "Both, and the women's collection is the larger of the two — 23 pieces against 21 for the men. Several styles are colour-matched across both lines, in sage green and chocolate brown, and the campaign photography shoots them together."),
 ("What is Rouqe Golf's signature piece?",
  "The mock neck. They make it in six colours at $59 and it is the silhouette the brand keeps returning to across both collections, in short sleeve for men and as a sleeveless tank for women. It is the clearest thing separating them from labels defaulting to a standard three-button polo."),
 ("Why is so much of it sold out?",
  "Twelve of the 21 men's pieces and nine of the 23 women's pieces were unavailable when we checked in August 2026. Small-batch production is normal at this size, and the pieces that go first — the burgundy rugby stripe, the script long-sleeve — are the loudest and most distinctive ones rather than the safe basics."),
 ("Where is Rouqe Golf made?",
  "The brand does not say. There is no manufacturing, factory or materials information anywhere on the store, which is common for labels at this scale but a fair thing to know if it matters to you."),
 ("Does Rouqe Golf sell in shops?",
  "No stockists, wholesale accounts or retail partners turned up anywhere. Everything points to direct-to-consumer through their own site only."),
 ("What does Rouqe Golf's clothing actually look like?",
  "Muted and tonal rather than bright — sage green, chocolate brown, burgundy, cream, black and pale blue, with retro rugby and Breton stripes doing most of the pattern work. Silhouettes are boxy rather than fitted. Two logo lockups run in parallel: a cursive script wordmark and a block letter R."),
 ("Is the photography theirs?",
  "Yes, and it is the strongest thing about the brand. They run two modes — hard-lit studio portraits against black and maroon backdrops, styled closer to streetwear than golf, and genuine on-course work shot at golden hour on a dry mountain course. Every image in this post is Rouqe's own."),
 ("Where do I start?",
  "The brown or green mock neck at $59 if you want the piece that defines the brand. The Script Polo at $24 if you want the cheapest way in. The RQ Sweater at $39 is the best value in the store by some distance."),
]

faq_html = "\n".join(f'    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQS)
faq_ld = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in FAQS]}, ensure_ascii=False)
art_ld = json.dumps({"@context":"https://schema.org","@type":"Article","headline":TITLE_TXT,
 "description":DESC,"author":{"@type":"Organization","name":"The Grassy Issue"},
 "publisher":{"@type":"Organization","name":"The Grassy Issue"},
 "datePublished":"2026-08-27","dateModified":"2026-08-27",
 "mainEntityOfPage":f"https://thegrassyissue.com/drops/{SLUG}"}, ensure_ascii=False)

WRITEUP = '''<div class="writeup">
  <div class="writeup-body">
    <p>Rouqe Golf sells a burgundy and cream rugby-striped polo that looks like it was pulled off a
    club pro in 1974, and it is sold out. So is the black long-sleeve with the cream chest banding.
    So is the houndstooth. Twelve of the twenty-one pieces in the men&rsquo;s collection are gone,
    and the ones that went first are the loudest, which is a more interesting fact about a brand
    than any amount of copy about performance fabric.</p>
    <p>What is left is a small, unusually coherent range. Mock necks in six colours at fifty-nine
    dollars, which is the silhouette the whole thing is built on. Retro stripes. A palette of sage
    green, chocolate brown, burgundy and cream that runs across both the men&rsquo;s and
    women&rsquo;s lines &mdash; the brown mock neck and the brown skort are shot together on the
    same couple, which is a level of coordination most labels this size do not bother with.</p>
    <p>The photography is the other thing. Rouqe shoots two ways: hard-lit studio portraits against
    black and deep maroon, styled closer to a streetwear campaign than a golf catalogue, and real
    on-course work at golden hour on a dry mountain course with a lake in the middle distance.
    Everything you see below is theirs. It is better than the budget suggests.</p>
    <p>Here is what they will not tell you: who they are. There is no About page &mdash; the URL
    returns a 404. No founder is named on the store, in any interview, or in any press we could
    find, and the domain registration is privacy-shielded. The one person publicly attached to the
    brand is Marko Mijaljevic, its Head of Design, credited with the SS25 collection. The domain
    was registered in spring 2023, which dates the shopfront rather than the company. For a label
    whose whole pitch is a point of view, the anonymity is a strange choice &mdash; and the clothes
    are good enough that it is the only thing holding the story back.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Products</span><span>54</span></div>
      <div class="sidebar-detail"><span class="l">Men&rsquo;s</span><span>21</span></div>
      <div class="sidebar-detail"><span class="l">Women&rsquo;s</span><span>23</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$19&ndash;$199 CAD</span></div>
      <div class="sidebar-detail"><span class="l">Checked</span><span>Aug 2026</span></div>
      <a href="/brands/" class="sidebar-cta">Browse the Brand Index &rarr;</a>
      <div class="hashtags">
        <span class="hashtag">#TheGrassyIssue</span>
        <span class="hashtag">#RouqeGolf</span>
        <span class="hashtag">#IndependentGolf</span>
        <span class="hashtag">#BrandsToKnow</span>
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
           lambda m: f'<script type="application/ld+json">{art_ld}</script>')
head = rep(head, r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "FAQPage".*?</script>',
           lambda m: f'<script type="application/ld+json">{faq_ld}</script>')
head = rep(head, r'(<div class="breadcrumb">.*?<span>/</span>\s*)[^<]*?(</div>)', lambda m: m.group(1) + "Brand to Know — Rouqe Golf" + m.group(2))
head = rep(head, r'<h1>.*?</h1>', f'<h1>{TITLE}</h1>')
head = rep(head, r'<div class="drop-meta">.*?</div>',
           '<div class="drop-meta">\n    <span>54 Products</span><span>&middot;</span>'
           '<span>Men&rsquo;s 21 &middot; Women&rsquo;s 23 &middot; Store checked Aug 2026</span>\n  </div>')
head = rep(head, r'<div class="drop-hero"><div class="drop-hero-img"><img src="[^"]*" alt="[^"]*"[^>]*/></div></div>',
           f'<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}hero.jpg" '
           f'alt="A golfer in the Rouqe Golf Blue Blade Collar polo on a dry hillside course, from the brand&rsquo;s own campaign" /></div></div>')
head = rep(head, r'<div class="writeup">.*?</div>\s*</aside>\s*</div>', lambda m: WRITEUP)
head = rep(head, r'</style>', CSS + '</style>')

tail = rep(tail, r'<div class="more-grid">.*?</div>\s*</section>',
'''<div class="more-grid">
    <a href="/drops/the-all-black-edit" class="more-card">\n      <div class="more-card-img"><img src="/images/all-black/hero.jpg" alt="The All-Black Edit  Twenty Pieces, Head to Toe" loading="lazy" /></div>\n      <div class="more-card-body"><div class="more-card-name">The All-Black Edit &mdash; Twenty Pieces, Head to Toe</div><div class="more-card-tag">The Edit</div></div>\n    </a>
    <a href="/drops/golf-brands-founded-by-women" class="more-card">\n      <div class="more-card-img"><img src="/images/women-founded/hero.jpg" alt="Seventeen Golf Brands Founded by Women" loading="lazy" /></div>\n      <div class="more-card-body"><div class="more-card-name">Seventeen Golf Brands Founded by Women</div><div class="more-card-tag">The Roundup</div></div>\n    </a>
    <a href="/drops/brand-to-know-kingfisher-golf" class="more-card">\n      <div class="more-card-img"><img src="/images/kingfisher-golf/hero-package.jpg" alt="Kingfisher Golf  the Dallas Label Founded by Fiona Cohen" loading="lazy" /></div>\n      <div class="more-card-body"><div class="more-card-name">Kingfisher Golf &mdash; the Dallas Label Founded by Fiona Cohen</div><div class="more-card-tag">Brand to Know</div></div>\n    </a>
  </div>
</section>''')

page = head + '<section class="products">\n' + products + '\n<div class="faq">\n' + faq_html + '\n  </div>\n</section>' + tail
open(OUT, "w", encoding="utf-8").write(page)
words = len(re.sub(r'<[^>]+>', ' ', page).split())
n = len(MENS) + len(WOMENS) + len(WILD)
print(f"wrote {OUT} ({len(page):,} bytes, ~{words:,} words, {n} cards)")

# --- house voice guard -------------------------------------------------------
# Card copy and section kickers are owned by data/copy-deck.json, not by this
# script (see VOICE.md). Re-applying the deck here means a rebuild can never
# silently restore the pre-2026-08-27 copy. Safe to run repeatedly.
import subprocess as _sp, os as _os
_sp.run(["python3", _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "copy-deck.py"),
         "apply"], check=False)
