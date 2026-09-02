#!/usr/bin/env python3
"""build-apcph-golf.py — A.P.Cph/Golf, the A.P.C. Golf x Cph/Golf collab.

Lenny, 2026-09-02: "let's do a post about the new CPH/APC collab."

Angle settled with Lenny the same day: full drop report PLUS a real
"how to get it from the US" section, because captainshelmgolf.com is a
Japan-only market (Shopify countryCode JP, domestic shipping policy).
All 18 SKUs covered, men's-led, sold-out pieces included and labelled.

Prices are yen. USD figures are converted at ~160 JPY/USD, the rate on
2026-09-02, and are rounded — they are an orientation, not a quote.

Research + sourcing: research/apcph-golf-dossier.md.

Hero: the drop shipped no campaign banner and no landscape frame — only 1:1
packshots and 2:3 lookbook portraits, which cannot survive a 21:9 crop as
full figures. The way in was the back graphics: they are horizontal by
construction, so a torso band across one reads as a designed hero rather
than a squeezed portrait. Cut from CPH-1330 (black half zip, back view) at
38% down, full width, no upscaling beyond the source.

Chassis cloned from drops/loud-on-purpose-headcovers.html.
"""
import re, os, json

S = os.path.dirname(os.path.abspath(__file__))
ch = open(os.path.join(S, "drops", "loud-on-purpose-headcovers.html"), encoding="utf-8").read()

css_main = re.search(r'(<link rel="preconnect".*</style>)\s*</head>', ch, re.S).group(1)
nav      = re.search(r'(<nav class="nav".*?</nav>)', ch, re.S).group(1)
tail     = re.search(r'(<!-- TGI SEARCH -->.*?)</body>', ch, re.S).group(1)

# The headcover chassis has no .pull-quote rules (only the Lions/Hancock deep
# dives carry them), and verify-post fails any class without CSS. Port the
# canonical rules across verbatim rather than inventing a variant.
if ".pull-quote{" not in css_main:
    css_main = css_main.replace("</style>",
        ".pull-quote{max-width:1400px;margin:0 auto;padding:0 32px}"
        ".pull-quote-inner{font-family:var(--serif);font-style:italic;font-size:22px;line-height:1.4;"
        "padding:32px 0;margin:0;border-top:.5px solid rgba(20,20,20,.15);"
        "border-bottom:.5px solid rgba(20,20,20,.15);color:var(--grass)}"
        ".pull-quote-attr{font-family:var(--mono);font-style:normal;font-size:10px;letter-spacing:.14em;"
        "text-transform:uppercase;color:var(--ink);opacity:.45;margin-top:12px;display:block}"
        "@media(max-width:820px){.pull-quote{padding:0 20px}}"
        "\n</style>", 1)

URL         = "https://thegrassyissue.com/drops/apc-golf-cph-golf-collab"
TITLE       = "A.P.Cph/Golf &mdash; Paris and Tokyo Fuse Logos for an 18-Piece Drop"
TITLE_PLAIN = "A.P.Cph/Golf — Paris and Tokyo Fuse Logos for an 18-Piece Drop"
DESC        = ("A.P.C. Golf and Tokyo's Cph/Golf released an 18-piece collab on September 2, 2026. "
               "Every piece, prices in dollars, what is printed on the back, and how to buy it from the US.")
IMG         = "/images/apcph-golf"
STORE       = "https://captainshelmgolf.com/en/products/"


def card(base, name, price, sold, frames, desc, alt, handle):
    gal = "".join(
        '<div class="pg-frame"><img src="%s/%s-%d.jpg" alt="%s &middot; view %d of %d" loading="lazy" /></div>'
        % (IMG, base, i, alt, i + 1, frames) for i in range(frames))
    dots = "".join('<button class="pg-dot%s" data-i="%d" aria-label="View image %d"></button>'
                   % (" on" if i == 0 else "", i, i + 1) for i in range(frames))
    controls = ('<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
                '<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
                '<span class="pg-count">1/%d</span><div class="pg-dots">%s</div>' % (frames, dots)) if frames > 1 else ""
    tag = ' &middot; <span style="color:var(--rough)">Sold out</span>' if sold else ""
    return ('<div class="product-card" data-frames="%d">'
            '<div class="product-gallery"><div class="pg-track">%s</div>%s</div>'
            '<div class="product-body">'
            '<div class="product-brand">A.P.Cph/Golf</div>'
            '<div class="product-name">%s &middot; %s%s</div>'
            '<div class="product-desc">%s</div>'
            '<a href="%s%s" target="_blank" rel="noopener" class="product-link">View on Cph/Golf &#8599;</a>'
            '</div></div>' % (frames, gal, controls, name, price, tag, desc, STORE, handle))


SECTIONS = [
 ("The Men&rsquo;s Line",
  "Six tops and one jacket, all cut with the roomy shoulder and slightly cropped body Cph/Golf uses across its own range. Every reference is sized M to XL against a 183cm fit model in L, so the cm charts matter more than the letter.",
  [
   ("jacket", "Zipper No Collar Jacket", "&yen;28,600 / ~$179", True, 4,
    "The most expensive piece and the first to go. No collar, zip front, and a raglan-like sleeve so the shoulder does not bind at the top of the swing. Black or navy, with the contrast panel carrying the logo.",
    "A.P.Cph/Golf zipper no collar jacket in black with navy contrast panel", "chg26-apcg-j01"),
   ("polo", "L/S Polo Pullover", "&yen;18,700 / ~$117", False, 4,
    "The one piece still fully stocked in every size and colour, and the clearest statement of what the collab is for. Jacquard collar, embroidered chest logo, dropped shoulder, ribbed cuffs and hem. Black, navy or white.",
    "A.P.Cph/Golf long sleeve polo pullover in navy", "chg26-apcg-t04"),
   ("halfzip", "Half Zip Gentleman L/S Mock Neck Tee", "&yen;15,400 / ~$96", False, 4,
    "The piece that carries the whole joke. Cph/Golf&rsquo;s own line &mdash; NOT A GOLF GENTLEMAN &mdash; is set against 39 RUE MADAME PARIS on the back, A.P.C.&rsquo;s head-office address. Stand collar, half zip, ribbed hem. Down to a single size.",
    "A.P.Cph/Golf half zip mock neck tee in black", "chg26-apcg-t03"),
   ("sweat", "Sweat Pullover", "&yen;17,600 / ~$110", False, 4,
    "Chest logo front, 39 RUE MADAME PARIS across the back. Cut with enough room to read as a sweatshirt rather than a golf layer, which is the point. Black, light grey or navy.",
    "A.P.Cph/Golf sweat pullover in navy", "chg26-apcg-t02"),
   ("thermal", "Thermal L/S Mock Neck Tee", "&yen;15,400 / ~$96", False, 4,
    "The quietest thing in the drop: waffle-knit thermal, logo embroidered small at the centre of the neck so it reads as a detail under a jacket rather than a print. Black, cream or navy.",
    "A.P.Cph/Golf thermal long sleeve mock neck tee in cream", "chg26-apcg-t05"),
   ("mock-tee", "Half Mock Neck Tee", "&yen;12,100 / ~$76", True, 4,
    "The cheapest way into the collab and gone within the day across all nine size-and-colour combinations. Boxy body, raised neckline, big chest logo, Paris address on the back.",
    "A.P.Cph/Golf half mock neck tee in black", "chg26-apcg-t01"),
  ]),

 ("Bottoms, Caps and the Small Stuff",
  "Where the collab turns usable. The pants are the sleeper &mdash; cut loose enough through the hip and hem to read as trousers rather than golf kit &mdash; and the green fork is the only piece anyone can buy on impulse.",
  [
   ("pants", "Adjustable Pants", "&yen;19,800 / ~$124", False, 4,
    "Roomy from the waist through the hem, deliberately away from the tapered technical trouser. Adjustable waist spans roughly 82&ndash;110cm depending on size. Black or navy, and down to one size.",
    "A.P.Cph/Golf adjustable pants in black", "chg26-apcg-p01"),
   ("cap", "All Weather Cap", "&yen;9,900 / ~$62", True, 4,
    "Six-panel, embroidered logo front, collab label on the back, adjustable strap and buckle. Black, navy or white &mdash; all three gone.",
    "A.P.Cph/Golf all weather six panel cap in navy", "chg26-apcg-c01"),
   ("safari", "All Weather Safari Hat", "&yen;9,900 / ~$62", True, 4,
    "The wide-brim alternative at the same price, with a 7.5cm brim and a drawcord for wind. Also sold out in all three colours.",
    "A.P.Cph/Golf all weather safari hat in white", "chg26-apcg-c02"),
   ("socks", "2PC Socks", "&yen;4,400 / ~$28", False, 4,
    "Two pairs, white and navy. A.P.Cph jacquard-woven into the cuff, golf embroidered beneath. Cotton, one size fitting 25&ndash;28cm.",
    "A.P.Cph/Golf two pack socks in white and navy", "chg26-apcg-sx01"),
   ("greenfork", "Green Fork", "&yen;4,400 / ~$28", False, 3,
    "Folding divot tool in light silver metal with a magnetic coin marker seated in the head. 11cm long, 2.5cm marker. The gift item, and the one thing here that needs no sizing.",
    "A.P.Cph/Golf folding green fork divot tool with magnetic ball marker", "chg26-apcg-a01"),
  ]),

 ("The Women&rsquo;s Pieces",
  "Seven references, and not an afterthought &mdash; the skirt is the only piece in the entire collab that uses the navy colour-blocking as a design feature rather than a trim. Four of the seven were already gone when we checked.",
  [
   ("skirt", "Adjustable Skirt", "&yen;16,500 / ~$103", False, 4,
    "A-line mini built on an asymmetric navy panel, the one genuinely graphic cut in the drop. Sized S and M with an adjustable waist. Black, navy or white.",
    "A.P.Cph/Golf adjustable skirt in navy and slate colour blocking", "chg26-apcg-sk01"),
   ("w-polo", "L/S Polo Pullover", "&yen;18,700 / ~$117", False, 4,
    "The women&rsquo;s cut of the piece that anchors the men&rsquo;s line, and like it, still fully stocked. Jacquard collar, embroidered chest logo. Black, navy or white.",
    "A.P.Cph/Golf women's long sleeve polo pullover", "chg26-apcg-wt04"),
   ("w-jacket", "Zipper No Collar Jacket", "&yen;28,600 / ~$179", True, 4,
    "Same no-collar, raglan-sleeved build as the men&rsquo;s, in a women&rsquo;s cut and only two sizes. Both sold out.",
    "A.P.Cph/Golf women's zipper no collar jacket", "chg26-apcg-wj01"),
   ("w-halfzip", "Half Zip Mademoiselle L/S Mock Neck Tee", "&yen;15,400 / ~$96", True, 4,
    "The counterpart to the men&rsquo;s Gentleman half zip, and the naming is the whole gag. Stand collar, half zip, same Paris address graphic. Sold out.",
    "A.P.Cph/Golf women's half zip mademoiselle mock neck tee", "chg26-apcg-wt03"),
   ("w-sweat", "Sweat Pullover", "&yen;17,600 / ~$110", True, 4,
    "Chest logo, 39 RUE MADAME PARIS on the back, women&rsquo;s fit. Black, light grey or navy, all three gone.",
    "A.P.Cph/Golf women's sweat pullover", "chg26-apcg-wt02"),
   ("w-mock-tee", "Half Mock Neck Tee", "&yen;12,100 / ~$76", True, 4,
    "Same boxy silhouette and raised neck as the men&rsquo;s, same price, same result &mdash; sold out in every colour on day one.",
    "A.P.Cph/Golf women's half mock neck tee", "chg26-apcg-wt01"),
   ("w-socks", "2PC Long Socks", "&yen;4,400 / ~$28", False, 4,
    "The long version of the two-pack, white and navy, jacquard cuff. Still available and the cheapest entry point on the women&rsquo;s side.",
    "A.P.Cph/Golf women's two pack long socks in white and navy", "chg26-apcg-wsx01"),
  ]),
]

FAQS = [
 ("What is A.P.Cph/Golf?",
  "A collaboration between A.P.C. Golf, the golf line of the Paris label A.P.C., and Cph/Golf, the golf line of the Tokyo streetwear brand CAPTAINS HELM. The name fuses both marks into one — A.P.Cph — and it appears on the chest of nearly every piece. It released on September 2, 2026 as 18 references: 11 men's and unisex, 7 women's."),
 ("How much does the collab cost?",
  "Prices run ¥4,400 to ¥28,600 — roughly $28 to $179 at about 160 yen to the dollar in early September 2026. The socks and the green fork are ¥4,400 each, the polo is ¥18,700, and the no-collar jacket tops it at ¥28,600. Those dollar figures move with the exchange rate and exclude any forwarding fee, duty or import tax."),
 ("Can I buy it from the United States?",
  "Not directly. Cph/Golf's webstore is configured as a Japan-only market and its shipping policy covers domestic delivery, down to noting delays to Japan's remote islands. There is no international checkout. The routes that exist are a proxy service that buys on your behalf, or a forwarding service that gives you a Japanese address to ship to — both add cost and neither is guaranteed for an independent Shopify store."),
 ("Is A.P.C. Golf itself sold in the US?",
  "Yes. A.P.C.'s US store carries the mainline A.P.C. Golf range — caps, polos, trousers, gloves and accessories, roughly $50 to $350. What is not sold there is this collab. The price gap is striking: A.P.C. Golf's own polos run $245 to $295 on the US site, while the collab polo converts to about $117."),
 ("What is printed on the back of the pieces?",
  "39 RUE MADAME PARIS — printed across the back of several tops, including the sweat pullover and the half mock neck tee. That is A.P.C.'s head office in the 6th arrondissement; its Paris store sits across the street at number 38. The half zip goes further and sets the address against Cph/Golf's own brand line, NOT A GOLF GENTLEMAN."),
 ("What size should I take?",
  "Japanese sizing, so size up if you are used to US letter sizes, and use the centimetre charts on each product page rather than the letter. Cph/Golf lists every measurement in cm and photographs the range on a 183cm fit model wearing L. The men's tops run M to XL, the women's pieces and the skirt run S to M."),
 ("Who are Cph/Golf and A.P.C. Golf?",
  "Cph/Golf is the golf line of CAPTAINS HELM, a Tokyo label that filters a California outdoor-lifestyle influence through a Japanese lens — printed slogans, unusual collars, rugged outer layers. A.P.C. is the Paris house founded by Jean Touitou, known for minimalism and raw denim; its golf line launched in Korea and Japan in 2021 and reached Europe later."),
]

faq_schema = ",\n  ".join('{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
    % (json.dumps(q), json.dumps(a)) for q, a in FAQS)
faq_html = "\n    ".join('<details class="faq-q"><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in FAQS)

sections_html = ""
for hdr, kick, cards in SECTIONS:
    sections_html += ('\n<section class="products" style="margin-top:40px;">\n'
        '  <h2 class="products-hdr">%s</h2>\n  <p class="cat-kicker">%s</p>\n'
        '  <div class="products-grid">\n    %s\n  </div>\n</section>\n'
        % (hdr, kick, "\n    ".join(card(*c) for c in cards)))

page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{TITLE} &mdash; The Grassy Issue</title>
<meta name="description" content="{DESC}" />
<link rel="icon" href="/favicon.ico" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
<meta property="og:type" content="article" />
<meta property="og:url" content="{URL}" />
<meta property="og:title" content="{TITLE_PLAIN}" />
<meta property="og:description" content="{DESC}" />
<meta property="og:image" content="https://thegrassyissue.com/images/apcph-golf/jacket-1.jpg" />
<meta property="og:site_name" content="The Grassy Issue" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{TITLE_PLAIN}" />
<meta name="twitter:description" content="18 pieces, Japan only, and a Paris address printed on the back." />
<link rel="canonical" href="{URL}" />
<script type="application/ld+json">
{{
 "@context": "https://schema.org",
 "@type": "Article",
 "headline": "{TITLE_PLAIN}",
 "description": "{DESC}",
 "url": "{URL}",
 "datePublished": "2026-09-02",
 "dateModified": "2026-09-02",
 "author": {{"@type": "Organization", "name": "The Grassy Issue"}},
 "publisher": {{"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"}},
 "mainEntityOfPage": {{"@type": "WebPage", "@id": "{URL}"}}
}}
</script>
<script type="application/ld+json">
{{
 "@context": "https://schema.org",
 "@type": "FAQPage",
 "mainEntity": [
  {faq_schema}
 ]
}}
</script>
{css_main}
</head>
<body>
{nav}

<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  A.P.Cph/Golf</div>

<header class="drop-header">
  <h1>A.P.Cph/Golf &mdash; Paris and Tokyo Fuse Logos for an 18-Piece Drop</h1>
  <div class="drop-meta">
    <span>September 2, 2026</span><span class="dot"></span>
    <span>18 pieces &middot; ~$28&ndash;$179</span><span class="dot"></span>
    <span>Status checked Sep 2, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="/images/apcph-golf/hero.jpg" alt="The back of the A.P.Cph/Golf half zip in black, printed NOT A GOLF GENTLEMAN above the address 39 RUE MADAME PARIS" /></div></div>

<div class="writeup">
  <div class="writeup-body">
    <p>The two marks do not sit side by side on these eighteen pieces. They have been welded into one, <strong>A.P.Cph</strong>, embroidered or printed on the chest of nearly everything A.P.C. Golf and Tokyo&rsquo;s Cph/Golf released together this morning. Prices run &yen;4,400 to &yen;28,600, or roughly $28 to $179, with the no-collar jacket at the top of the range and a two-pack of socks at the bottom.</p>
    <p>The graphics do the arguing. Several tops carry <strong>39 RUE MADAME PARIS</strong> across the back &mdash; A.P.C.&rsquo;s head office in the 6th, with its Paris store across the road at 38 &mdash; transplanted onto Japanese golf wear. The half zip goes one better and runs that address against Cph/Golf&rsquo;s own house line, <strong>NOT A GOLF GENTLEMAN</strong>. Everything sits in black, navy, white, cream and light grey, with navy doing the colour-blocking.</p>
    <p>It is aimed at the golfer who dresses for the parking lot as much as the first tee, which both labels have been serving for years from opposite ends of the world. The complication is geography: this is a Japan-only release on a Japan-only store, and six of the eighteen sold out on day one. What follows is every piece, what it costs in dollars, and the honest options for getting one from the States.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>18</span></div>
      <div class="sidebar-detail"><span class="l">Released</span><span>Sep 2, 2026</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>&yen;4,400&ndash;&yen;28,600</span></div>
      <div class="sidebar-detail"><span class="l">In USD</span><span>~$28&ndash;$179</span></div>
      <div class="sidebar-detail"><span class="l">Ships</span><span>Japan only</span></div>
      <div class="sidebar-detail"><span class="l">Sold out</span><span>6 of 18</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>L/S Polo Pullover</span></div>
      <a href="https://captainshelmgolf.com/en/collections/new" target="_blank" rel="noopener" class="sidebar-cta">See the drop ↗</a>
      <div class="hashtags">
        <span class="hashtag">#APCGolf</span>
        <span class="hashtag">#CphGolf</span>
        <span class="hashtag">#CaptainsHelm</span>
        <span class="hashtag">#JapanGolf</span>
        <span class="hashtag">#GolfStyle</span>
      </div>
    </div>
  </aside>
</div>

<div class="pull-quote">
  <div class="pull-quote-inner">&ldquo;I don&rsquo;t like the way that amateur players try to dress like professional golfers. I just want them to be chic.&rdquo;<span class="pull-quote-attr">&mdash; Jean Touitou, founder of A.P.C., on premiering the label&rsquo;s first golf collection</span></div>
</div>
{sections_html}
<section class="products" style="margin-top:48px;">
  <h2 class="products-hdr">How to Actually Get It From the US</h2>
  <div style="max-width:760px;font-size:16px;line-height:1.7;">
    <p>Cph/Golf&rsquo;s store is set up as a Japanese market and nothing else. The shipping policy is written entirely for domestic delivery &mdash; business days, remote-island timing &mdash; and there is no international checkout to find. So there are two indirect routes, and both cost more than the sticker.</p>
    <p style="margin-top:16px"><strong>A proxy service</strong> &mdash; ZenMarket, Buyee and similar &mdash; buys the item for you with a Japanese card and address, receives it, then forwards it on. The caveat is that these services are built around Mercari, Yahoo Auctions, Rakuten and Amazon Japan; an independent Shopify store like this one is a less certain fit, so check the service supports it before you count on it.</p>
    <p style="margin-top:16px"><strong>A forwarding service</strong> gives you a Japanese address and nothing else &mdash; you place the order yourself and it ships onward from their warehouse. Cheaper, but it only works if the store accepts your card.</p>
    <p style="margin-top:16px">Either way, budget for the forwarding fee, international postage and US duty on top of the yen price, and size from the centimetre charts rather than the letter &mdash; the range is photographed on a 183cm model wearing L.</p>
    <p style="margin-top:16px">If what you actually want is A.P.C. Golf rather than this specific capsule, that is straightforward: A.P.C.&rsquo;s US store carries the mainline range, roughly $50 to $350. The prices there make the collab look sharp &mdash; A.P.C. Golf&rsquo;s own polos sit at $245 to $295, against about $117 for the A.P.Cph polo.</p>
  </div>
</section>

<section class="products" style="border-top:none;padding-top:48px">
  <h2 class="products-hdr" id="faq">Frequently Asked</h2>
  <div class="faq">
    {faq_html}
  </div>
</section>

<section class="more">
  <div class="more-hdr">
    <span class="more-label">More from TGI</span>
    <a href="/" class="more-link">Back to Feed &rarr;</a>
  </div>
  <div class="more-grid">
    <a href="/drops/public-drip-fw26-nightshift" class="more-card">
      <div class="more-card-img"><img src="/images/publicdrip-fw26/herringbone-half-zip-coffee-1.jpg" alt="Public Drip FW26: Nightshift" loading="lazy" /></div>
      <div class="more-card-body"><div class="more-card-name">Public Drip FW26: Nightshift</div><div class="more-card-tag">Drops &amp; Brands</div></div>
    </a>
    <a href="/drops/japan-golf-roundup" class="more-card">
      <div class="more-card-img"><img src="/images/apcph-golf/polo-1.jpg" alt="The Japan Golf Roundup" loading="lazy" /></div>
      <div class="more-card-body"><div class="more-card-name">The Japan Golf Roundup</div><div class="more-card-tag">Drops &amp; Brands</div></div>
    </a>
    <a href="/drops/loud-on-purpose-headcovers" class="more-card">
      <div class="more-card-img"><img src="/images/loud-headcovers/mogshade-deco-magenta-0.jpg" alt="Loud on Purpose" loading="lazy" /></div>
      <div class="more-card-body"><div class="more-card-name">Loud on Purpose</div><div class="more-card-tag">Drops &amp; Brands</div></div>
    </a>
  </div>
</section>

<footer><div class="inner"><span>&copy; 2026 The Grassy Issue</span><a href="/">Back to Feed</a></div></footer>
{tail}</body>
</html>
'''

out = os.path.join(S, "drops", "apc-golf-cph-golf-collab.html")
open(out, "w", encoding="utf-8").write(page)
words = len(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", "", page, flags=re.S)).split())
cards = page.count('class="product-card"')
print("wrote %s | words: %d | cards: %d" % (out, words, cards))
