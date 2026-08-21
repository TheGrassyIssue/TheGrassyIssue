#!/usr/bin/env python3
# Walker Golf Things — Blooming Grounds, launched 21 Aug 2026.
# Facts from Walker's own product copy. Prices are USD (verified: Shopify.currency active=USD
# on the /en-us/ storefront). Run verify-post.py before pushing.
import os, re, json

S = os.path.dirname(os.path.abspath(__file__))
BASE = open(os.path.join(S, "drops/the-hat-edit-austin-summer.html"), encoding="utf-8").read()
MAN = json.load(open("/tmp/wk/man.json"))
BY_I = {v["i"]: (k, v) for k, v in MAN.items()}
RANGE = json.load(open("/tmp/wk/rangeman.json"))          # the other collections
BY_N = {v["n"]: (k, v) for k, v in RANGE.items()}

# Correct line attribution — the collection bucket a product sits in is NOT always its line.
# Most of Walker's "Heritage" collection is Gold Label product, and the Knockout V Polo is
# Par-Tec 2026 despite appearing under Kooka Classics.
LINE = {0: "Gold Label", 3: "Gold Label", 10: "Gold Label", 13: "Gold Label", 9: "Gold Label",
        7: "Heritage", 32: "Par-Tec", 30: "Kooka Classics", 44: "Kooka Classics"}

RANGE_COPY = {
 0:  "One hundred per cent acrylic in a custom stripe knit, with a fine contrast stripe running through the "
     "body. Knit collar, cuffs and hem, three matte buttons. Gold Label is Walker&rsquo;s premium line and "
     "this is its plainest, best piece.",
 3:  "The same classic-fit block in a lightweight acrylic ombre knit, graduating from pale to charcoal down "
     "the body, with a quarter-zip placket instead of buttons. The gradient is knitted, not dyed.",
 10: "A plaid twill body with a satin quilted lining, a 16-wale corduroy collar and a full-length YKK "
     "antique brass zip. The most expensive thing in this section at $180 and the one that looks least like "
     "golf clothing.",
 13: "A wool-blend knit with a brushed finish and a fisherman-style ribbed collar and cuffs. Walker run this "
     "one in Indigo and Almond; the Indigo is the better of the two.",
 9:  "An acrylic-blend yarn in a textured three-stripe knit on a crew block, again with the fisherman collar. "
     "Chocolate with a red and cream stripe &mdash; the most seventies thing Walker make.",
 7:  "Walker&rsquo;s Heritage line, which they pitch as golf before the game went global. A classic rugby "
     "block with a cut-and-sew stripe panel through the body and sleeves, and a white cotton-twill woven "
     "collar. The hero of that range.",
 32: "From the 2026 Par-Tec collection &mdash; Walker&rsquo;s technical line, lightweight and moisture-"
     "wicking, built for airflow rather than looks. This one gets away with both. We covered Par-Tec "
     "properly in its own post.",
 30: "Full-grain leather with a velvet lining and an embroidered &ldquo;Dancing Kooka&rdquo; pattern across "
     "the whole cover. Eighty-nine dollars for a driver headcover is real money and this is one of the few "
     "that earns it.",
 44: "Nine-wale cotton corduroy, mid profile, contrast top-stitching on the peak, snapback closure. "
     "Embroidered Kooka patch on the front and a Bounce logo on the right side. Walker run the corduroy caps "
     "in a rotating set of colours and the red is the one to have.",
}

SLUG = "walker-golf-blooming-grounds-drop"
TITLE = "Walker&rsquo;s Blooming Grounds &mdash; A Spring Collection Landing in an Austin August"
TITLE_PLAIN = "Walker's Blooming Grounds — A Spring Collection Landing in an Austin August"
DESC = ("Walker Golf Things drop Blooming Grounds on 21 August 2026 — a six-piece Australian spring "
        "collection built around a hand-drawn course scene, including a full-jacquard knit polo, a "
        "seersucker camp shirt and a 400gsm hood.")

SECTIONS = [
 ("The Artwork", "Where the Collection Actually Lives",
  "Two pieces carry the Blooming Grounds illustration &mdash; a course scene of trees, a creek and a "
  "green. On the polo it is knitted into the body rather than printed on top of it, which is a genuinely "
  "different and more expensive way to do it.",
  [1, 3]),
 ("The Rest of the Kit", "Seersucker, Fleece and a Chain-Stitched Script",
  "The other four run on Walker&rsquo;s &ldquo;Hedge Script&rdquo; &mdash; a chain-stitched wordmark with a "
  "tiny golfer teeing off out of the W &mdash; plus the Kookaburra patch that shows up somewhere on almost "
  "everything they make.",
  [5, 0, 4, 2]),
]

COPY = {
 1: "The hero of the drop and the reason to care. One hundred per cent acrylic in a full custom jacquard, "
    "with the Blooming Grounds artwork &mdash; sky, treeline, creek, fairway &mdash; knitted directly into "
    "the body rather than printed on it. Knit rib collar, three matte pearl buttons, Kookaburra patch on the "
    "left sleeve. Sizes S to XXXL.",
 3: "The hand-drawn piece. 250gsm cotton jersey on an oversized block, with the Hedge Script screen printed "
    "small at the chest and the full-colour Blooming Grounds scene running across the back. Fifty dollars, "
    "and the best value in the collection by a distance.",
 5: "Lightweight poly-cotton seersucker with a wide camp collar, five centre-front buttons and a self-lined "
    "back yoke. Scattered across it are tiny embroidered golfers mid-swing. Walker say to size up for a "
    "relaxed fit, and describe it as the piece for a warm spring afternoon on a verandah &mdash; which in "
    "Austin translates to roughly nine months of the year.",
 0: "The lightweight performance polo, in a cotton-poly-elastane pique on Walker&rsquo;s Featherlite block. "
    "Custom striped ribbed collar, contrast sleeve bands, three-button placket. The most conventionally "
    "golf-looking thing here, and the one that will get the most wear.",
 4: "400gsm brushed fleece with a soft interior, a kangaroo pouch sized for a scorecard and a glove, chunky "
    "ribbed cuffs and hem. Hedge Script chain-stitched at the chest, Kookaburra on the left sleeve. Built "
    "for a cold walk from the carpark, which is not an Austin problem in August &mdash; file this one for "
    "December.",
 2: "Soft cotton twill on a mid box-cap block, navy with contrast Star White stitching through the crown and "
    "brim. A large 14cm front panel carries the Hedge Script embroidery, the Kookaburra sits on the back "
    "right, and it closes with a rear snapback. Fifty dollars, one size. The contrast stitching is the whole "
    "trick here &mdash; it is what stops a navy five-panel from disappearing into every other navy five-panel.",
}

CLOSER = """    <p>If you are buying one thing, buy the knit polo, and buy it because of how it is made rather than
    how it looks in a thumbnail. If you are buying one thing to actually wear this month, it is the tee or the
    Gardener shirt, and the Gardener is the more interesting garment of the two.</p>
    <p>A note on timing. Walker sell in both US and Australian dollars, and the prices quoted throughout this
    post are the US storefront figures. Australian spring runs September to November, so this collection has a
    long shelf life at home and an awkward one here &mdash; which historically means the sizes that survive
    into a northern-hemisphere autumn are the ones nobody in Australia wanted. Check back in October if your
    size has already gone.</p>"""

INTRO = """    <p>Walker Golf Things are Australian, which is the detail that makes this drop land oddly and
    also makes it interesting. Blooming Grounds went live on 21 August, and Walker describe it as an ode to
    spring &mdash; the opening rounds of the season, the flora along the fairways. In Melbourne that is
    exactly right. In Austin it arrives in the back half of an August that has been sitting at a hundred
    degrees.</p>
    <p>So read it as a forward buy rather than a right-now one. Two of the six pieces work here immediately,
    one of them is a December purchase, and the rest sit somewhere in between.</p>
    <p>Six pieces, $50 to $120, sizes S through XXXL, and one reason to pay attention above all the others:
    the knit polo has an entire landscape knitted into it.</p>
    <p>That distinction matters more than it sounds. Most graphic golf shirts are a print sitting on top of a
    finished garment. Walker built the artwork into the structure of the fabric &mdash; a jacquard, where the
    picture is made out of the yarn itself. It costs more, it takes longer, and it is the difference between a
    shirt with a picture on it and a shirt that <em>is</em> the picture. The same scene appears on the tee, and
    there it is a print, and the two sitting side by side make the point better than any description does.</p>
    <p>The rest of the collection is quieter and runs on two things: a chain-stitched script with a small
    golfer built into the lettering, and a kookaburra &mdash; an Australian kingfisher, and Walker&rsquo;s
    recurring mark &mdash; turning up on a sleeve, a cuff or the back of a cap.</p>"""

FAQ = [
 ("What is Walker Golf Things' Blooming Grounds collection?",
  "Blooming Grounds is a six-piece collection from the Australian brand Walker Golf Things, released on 21 "
  "August 2026. Walker describe it as an ode to the golf course itself and to spring. It comprises the "
  "Blooming Grounds Knit Polo ($120), the Gardener SS Shirt ($110), the Hedge Hood ($110), the Hedge "
  "Featherlite Polo ($100), the Blooming Grounds T-Shirt ($50) and the Hedge Mid Cap ($50)."),
 ("Is the Blooming Grounds Knit Polo printed or knitted?",
  "Knitted. Walker state the artwork is a full custom jacquard knitted directly into the body of the polo "
  "rather than printed onto the surface. The polo is 100% acrylic, with a knit rib collar, three matte pearl "
  "buttons at the placket and a Kookaburra patch on the left sleeve."),
 ("Why is Walker releasing a spring collection in August?",
  "Walker Golf Things is an Australian company, and August sits at the end of winter in the southern "
  "hemisphere, with spring beginning in September. The collection is timed to an Australian spring, which is "
  "why a 400gsm brushed-fleece hood appears in a range landing during a northern-hemisphere summer."),
 ("What is the Hedge Script?",
  "Hedge Script is Walker's chain-stitched wordmark, with a small golfer figure teeing off out of the W. It "
  "appears embroidered on the Hedge Hood and Hedge Mid Cap, and screen printed at the chest of the Blooming "
  "Grounds T-Shirt."),
 ("What fabric is the Gardener SS Shirt?",
  "Lightweight poly-cotton seersucker, cut on Walker's regular short-sleeve shirt block with a wide camp "
  "collar, five centre-front buttons and a self-lined back yoke. It is finished with scattered embroidered "
  "golfer figures. Walker recommend sizing up for a relaxed fit."),
 ("How much does the Blooming Grounds collection cost?",
  "Prices on Walker's US storefront run from $50 for the Hedge Mid Cap and the Blooming Grounds T-Shirt to "
  "$120 for the Blooming Grounds Knit Polo. The Gardener SS Shirt and Hedge Hood are $110 each and the Hedge "
  "Featherlite Polo is $100. These are US dollar prices; Walker also sell in Australian dollars."),
 ("What sizes does Blooming Grounds come in?",
  "The five apparel pieces run S, M, L, XL, XXL and XXXL. The Hedge Mid Cap is one size, with a rear "
  "snapback closure."),
 ("What are Walker Golf Things' other collections?",
  "Beyond seasonal drops like Blooming Grounds, Walker run several standing lines. Gold Label is the premium "
  "range, largely knitwear and outerwear, from around $110 to $180. Heritage is a clubhouse-inspired throwback "
  "line. Par-Tec is the technical performance range. Kooka Classics is the core collection, named for the "
  "kookaburra, and covers polos, caps, headcovers and accessories. Note the collections overlap on Walker's "
  "site &mdash; much of what is filed under Heritage is Gold Label product."),
 ("Does Walker Golf Things still sell the In Flight collection or Hiroki golf bags?",
  "Not on the US storefront as of August 2026. The In Flight collection is down to a single cap and the Hiroki "
  "golf bags collection returns no products at all, though both are still listed as collections. Availability "
  "differs between Walker's Australian and US stores, so stock may exist elsewhere."),
 ("What is the Kookaburra patch on Walker's clothing?",
  "The kookaburra is an Australian kingfisher, and Walker use an embroidered kookaburra as a recurring brand "
  "mark. In this collection it appears as a patch on the left sleeve of the Knit Polo and Hedge Hood, and "
  "embroidered on the back right of the Hedge Mid Cap."),
]

def anchor(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:24]

def card(i):
    sl, m = BY_I[i]
    fr = m["frames"]
    alt = "%s Walker Golf Things %s" % (m["title"], (m["type"] or "").lower())
    pg = ('<div class="product-gallery"><div class="pg-track">'
          + "".join('<div class="pg-frame"><img src="/images/walker-blooming-grounds/%s" loading="lazy" '
                    'alt="%s"></div>' % (f, alt) for f in fr)
          + '</div>'
          + (('<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
              '<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
              '<span class="pg-count">1/%d</span>' % len(fr)
              + '<div class="pg-dots">'
              + "".join('<button class="pg-dot%s" data-i="%d" aria-label="View image %d"></button>'
                        % (" on" if j == 0 else "", j, j + 1) for j in range(len(fr)))
              + '</div>') if len(fr) > 1 else '')
          + '</div>')
    sold = '' if m["avail"] else ' <span class="oos">Sold out</span>'
    # HOUSE FORMAT: text inside .product-body, outbound link is .product-link
    return ('  <div class="product-card" data-frames="%d">\n'
            '    %s\n'
            '      <div class="product-body">\n'
            '        <div class="product-brand">Walker Golf Things &middot; %s</div>\n'
            '        <div class="product-name">%s &middot; $%s%s</div>\n'
            '        <div class="product-desc">%s</div>\n'
            '        <a href="%s" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a>\n'
            '      </div>\n'
            '  </div>\n') % (len(fr), pg, m["type"], m["title"], m["price"], sold, COPY[i], m["url"])

CSS = """
.oos{font:500 10px/1 'JetBrains Mono',monospace;letter-spacing:.08em;text-transform:uppercase;
 color:#9a3b3b;border:1px solid #d9b3b3;border-radius:3px;padding:3px 6px;margin-left:5px;white-space:nowrap}
"""

h = BASE
h = h.replace("the-hat-edit-austin-summer", SLUG)
h = h.replace("/images/hat-edit/hero.jpg", "/images/walker-blooming-grounds/hero-blooming-grounds.jpg")
h = re.sub(r"<title>.*?</title>", "<title>%s &mdash; The Grassy Issue</title>" % TITLE, h, flags=re.S)
for pat in [r'(<meta name="description" content=")[^"]*(")',
            r'(<meta property="og:description" content=")[^"]*(")',
            r'(<meta name="twitter:description" content=")[^"]*(")']:
    h = re.sub(pat, lambda m: m.group(1) + DESC + m.group(2), h)
for pat in [r'(<meta property="og:title" content=")[^"]*(")',
            r'(<meta name="twitter:title" content=")[^"]*(")']:
    h = re.sub(pat, lambda m: m.group(1) + TITLE_PLAIN + m.group(2), h)
h = re.sub(r'(<h1[^>]*>).*?(</h1>)', lambda m: m.group(1) + TITLE + m.group(2), h, count=1, flags=re.S)
h = re.sub(r'(<div class="writeup-body">).*?(</div>)',
           lambda m: m.group(1) + "\n" + INTRO + "\n  " + m.group(2), h, count=1, flags=re.S)

body = '<section class="products">\n'
for name, kicker, lede, ids in SECTIONS:
    body += ('<h2 id="%s">%s</h2>\n<p class="cat-kicker"><strong>%s</strong>%s</p>\n'
             '<div class="products-grid">\n' % (anchor(name), name, kicker, lede))
    body += "".join(card(i) for i in ids)
    body += '</div>\n'
def range_card(n):
    sl, m = BY_N[n]
    fr = m["frames"]
    alt = "%s Walker Golf Things %s" % (m["title"], (m["type"] or "").lower())
    pg = ('<div class="product-gallery"><div class="pg-track">'
          + "".join('<div class="pg-frame"><img src="/images/walker-blooming-grounds/%s" loading="lazy" '
                    'alt="%s"></div>' % (f, alt) for f in fr)
          + '</div>'
          + (('<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
              '<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
              '<span class="pg-count">1/%d</span>' % len(fr)
              + '<div class="pg-dots">'
              + "".join('<button class="pg-dot%s" data-i="%d" aria-label="View image %d"></button>'
                        % (" on" if j == 0 else "", j, j + 1) for j in range(len(fr)))
              + '</div>') if len(fr) > 1 else '')
          + '</div>')
    return ('  <div class="product-card" data-frames="%d">\n'
            '    %s\n'
            '      <div class="product-body">\n'
            '        <div class="product-brand">Walker Golf Things &middot; %s</div>\n'
            '        <div class="product-name">%s &middot; $%s</div>\n'
            '        <div class="product-desc">%s</div>\n'
            '        <a href="%s" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a>\n'
            '      </div>\n'
            '  </div>\n') % (len(fr), pg, LINE[n], m["title"], m["price"], RANGE_COPY[n], m["url"])

body += ('<h2 id="elsewhere">Elsewhere in the Range</h2>\n'
         '<p class="cat-kicker"><strong>Gold Label, Heritage, Par-Tec and the Kooka</strong>Blooming Grounds '
         'is six pieces out of a much bigger catalogue, and the rest of it is where Walker actually live. '
         'Gold Label is the premium end &mdash; knits, and a lot of them. Heritage is the clubhouse throwback. '
         'Par-Tec is the technical line. Kooka Classics is the core, named for the kookaburra. Note that the '
         'collections overlap: most of what sits in Walker&rsquo;s Heritage collection is Gold Label product, '
         'so we have labelled each piece by the line it actually belongs to rather than the bucket it was '
         'filed under.</p>\n'
         '<div class="products-grid">\n'
         + "".join(range_card(n) for n in [0, 3, 10, 13, 9, 7, 32, 30, 44])
         + '</div>\n')

body += ('<h2 id="the-call">The Call</h2>\n'
         '<p class="cat-kicker"><strong>What to Buy and When</strong>Six pieces, one hemisphere out of '
         'step.</p>\n' + CLOSER + '\n')
start = h.index('<section class="products">')
fq = h.index('<div class="faq">')   # FAQ div sits INSIDE the products section
h = h[:start] + body + '  ' + h[fq:]

faq_html = "".join('    <details class="faq-q"><summary>%s</summary><p>%s</p></details>\n'
                   % (q, a) for q, a in FAQ)
h = re.sub(r'(<div class="faq">).*?(  </div>\n</section>)',
           lambda m: m.group(1) + "\n" + faq_html + m.group(2), h, count=1, flags=re.S)
h = h.replace("</style>", CSS + "</style>", 1)

import html as _html
def _plain(s): return _html.unescape(re.sub(r"<[^>]+>", "", s)).strip()
def _fix_ld(m):
    try: d = json.loads(m.group(1))
    except Exception: return m.group(0)
    if d.get("@type") == "FAQPage":
        d["mainEntity"] = [{"@type": "Question", "name": _plain(q),
                            "acceptedAnswer": {"@type": "Answer", "text": _plain(a)}} for q, a in FAQ]
    else:
        d["headline"] = d["name"] = _plain(TITLE)
        d["description"] = _plain(DESC)
        d["image"] = ["https://thegrassyissue.com/images/walker-blooming-grounds/hero-blooming-grounds.jpg"]
        d["datePublished"] = d["dateModified"] = "2026-08-20"
        if isinstance(d.get("mainEntityOfPage"), dict):
            d["mainEntityOfPage"]["@id"] = "https://thegrassyissue.com/drops/" + SLUG
        d.pop("keywords", None)
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + '</script>'
h = re.sub(r'<script type="application/ld\+json">(.*?)</script>', _fix_ld, h, flags=re.S)

h = h.replace("The Hat Edit — 28 Summer Caps, Ropes and Buckets From the Brands We Follow", TITLE_PLAIN)
h = h.replace("The Hat Edit &mdash; 28 Summer Caps, Ropes and Buckets From the Brands We Follow", TITLE)
h = re.sub(r'<span>\d+ Hats</span>', '<span>15 Pieces</span>', h)
h = h.replace('<span class="hashtag">#TheHatEdit</span>', '<span class="hashtag">#BloomingGrounds</span>')
h = re.sub(r'(<span class="l">Hats</span><span>)\d+(</span>)', r'\g<1>15\g<2>', h)
h = h.replace('<span class="l">Hats</span>', '<span class="l">Pieces</span>')
h = re.sub(r'(<span class="l">Brands</span><span>)\d+(</span>)', r'\g<1>5\g<2>', h)
h = h.replace('<span class="l">Brands</span>', '<span class="l">Lines</span>')

MORE = ("""    <a href="/drops/brand-revisited-walker-golf" class="more-card"><div class="more-kicker">Brand Revisited</div><div class="more-title">Walker Golf Things</div></a>
    <a href="/drops/malbon-fall-2026-the-ironworks-collection" class="more-card"><div class="more-kicker">The Drop</div><div class="more-title">Malbon Goes to Work</div></a>
    <a href="/drops/the-hat-edit-austin-summer" class="more-card"><div class="more-kicker">The Edit</div><div class="more-title">The Hat Edit &mdash; Austin Summer</div></a>
""")
h = re.sub(r'(<div class="more-grid">).*?(</div>\s*</section>)',
           lambda m: m.group(1) + "\n" + MORE + "  " + m.group(2), h, count=1, flags=re.S)

out = os.path.join(S, "drops", SLUG + ".html")
open(out, "w", encoding="utf-8").write(h)
print("wrote", out, len(h), "bytes")
