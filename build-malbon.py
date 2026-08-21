#!/usr/bin/env python3
# Malbon Men's Fall 2026 — 27 picks from 88. Facts taken from Malbon's own product copy.
import os, re, json

S = os.path.dirname(os.path.abspath(__file__))
BASE = open(os.path.join(S, "drops/the-hat-edit-austin-summer.html"), encoding="utf-8").read()
MAN = json.load(open("/tmp/mb/man.json"))
BY_I = {v["i"]: (k, v) for k, v in MAN.items()}

SLUG = "malbon-fall-2026-the-ironworks-collection"
TITLE = "Malbon Goes to Work &mdash; 27 Picks From the Fall Ironworks Collection"
TITLE_PLAIN = "Malbon Goes to Work — 27 Picks From the Fall Ironworks Collection"
DESC = ("Malbon's Men's Fall 2026 collection, cut from 88 pieces to 27. Stone-washed hickory-stripe "
        "workwear, a Red Wing Shop Moc collab, a CLUCT divot tool made in Japan, and the Inkwash print "
        "that runs through the whole thing.")

SECTIONS = [
 ("The Ironworks Division", "The Spine of the Whole Collection",
  "Malbon put a name on it this season. Ironworks Division is a run of heavyweight stone-washed striped "
  "denim &mdash; hickory stripe, the fabric painters and railroad workers wore &mdash; with antique nickel "
  "hardware and hammer loops. It is the most committed thing in the collection and the least like golf clothing.",
  [50, 51, 9, 1, 53, 84, 52]),
 ("Outerwear and Layers", "Three Ways to Handle a Cold Morning",
  "The reversible flannel is the interesting one: solid cotton on one face, plaid on the other, collarless "
  "and open-fronted so it works as a shirt jacket rather than a coat.",
  [0, 6, 29]),
 ("Shirts and Windshirts", "Herringbone, Chambray and the Inkwash Print",
  "The Station Shirt is stone-washed cotton herringbone twill with engraved snap closures, and it comes in "
  "both brown and olive. The Inkwash windshirt is the technical end of the collection &mdash; nylon and "
  "elastane, mesh-lined back venting, and a print that repeats on the shorts.",
  [47, 39, 55, 2, 25, 42]),
 ("Polos and Knits", "Where the Fabric Does the Talking",
  "No logos to speak of. The Crosscut is a cotton-cashmere pointelle knit with a full button front, the "
  "Brickwork is an enzyme-washed open knit, and the Fairway is overdyed heavyweight pique with contrast "
  "white stitching.",
  [16, 38, 34, 78, 54]),
 ("Bottoms", "Pleats, Herringbone and One Technical Short",
  "The Station Pant is the same stone-washed herringbone as the shirt, and buying both is a genuine "
  "temptation the lookbook is clearly encouraging.",
  [48, 40, 26]),
 ("Shoes, Headwear and Equipment", "The Two Collaborations",
  "The best two pieces in the collection are both made by somebody else.",
  [44, 21, 37]),
]

COPY = {
 50: "Heavyweight stone-washed striped denim, full metal zip, antique nickel hardware and Ironworks Division "
     "artwork on the back. The anchor piece &mdash; everything else in this section is a variation on it.",
 51: "The carpenter short version: utility patch pockets throughout, a hammer loop, engraved metal tack "
     "button and a metal zip fly. Two hundred and forty-eight dollars for denim shorts is a number, but "
     "these are not summer shorts, they are workwear cut short.",
 9:  "Actual overalls. Adjustable elastic shoulder straps, a multi-compartment bib, hammer loop and utility "
     "pocket, in medium-weight striped denim with the same stone wash. Nobody needs this. It is the most "
     "fun thing Malbon made this year.",
 1:  "Oversized drop-shoulder crewneck in heavyweight cotton jersey with a washed finish and the Ironworks "
     "artwork across the chest. Preorder &mdash; Malbon list it as shipping 26 August.",
 53: "Five-panel, flat brim, structured crown, in the same striped stone-washed denim as the jacket with "
     "Ironworks Division embroidery. The cheapest way into the capsule.",
 84: "Black stone-washed striped denim, padded, soft-lined, embroidered Division branding. Headcovers are "
     "where a capsule like this either lands or falls apart, and this one lands.",
 52: "The plain entry point. Relaxed cotton with a functional chest pocket and the Ironworks graphic. "
     "Sixty-eight dollars.",
 0:  "Solid cotton on one side, contrasting plaid on the reverse, collarless and open-fronted with chore "
     "pockets and snap cuffs. Two jackets, and neither of them reads as a golf jacket. Preorder, shipping "
     "26 August.",
 6:  "Part of Malbon's Icons line. Nylon and spandex, quarter-zip, drawcord hood and waist with lock "
     "stoppers, two zip pockets. The plainest thing here and probably the one you would wear most.",
 29: "A quarter-zip rebuilt as a chambray rugby &mdash; cotton-polyester, colour-blocked across the chest, "
     "stand collar, and an adjustable bungee hem with cord locks. The block is doing a lot of work.",
 47: "Stone-washed cotton herringbone twill, dual chest patch pockets, engraved Malbon snaps behind a "
     "hidden placket. Military workwear read through a golf brand, and the brown is the better of the two.",
 39: "The same shirt in olive. Straight hem, relaxed fit, and it pairs with the Station Pant in the same "
     "cloth if you want to commit to the whole look.",
 55: "Soft washed cotton chambray with oversized utility chest pockets, contrast decorative stitching and "
     "engraved Malbon buttons. The lightest layer in the collection.",
 2:  "Midweight hickory stripe with an antique nickel YKK quarter-zip, dual chest patch pockets and a "
     "drawcord hem. Short-sleeved, which is a strange and good decision.",
 25: "Nylon and elastane, mesh-lined back ventilation, invisible on-seam zip pockets and a silicone zipper "
     "pull. The Inkwash print is the only loud thing Malbon did this season, and the indigo is the version "
     "that works.",
 42: "The same windshirt in olive. Same venting, same drawcord hem. Between the two colourways and the "
     "matching short, the print carries four pieces in the collection.",
 16: "Heavyweight cotton pique, overdyed, with contrast white stitching at the sleeves and hem and tonal "
     "embroidery. The lived-in one.",
 38: "Enzyme-washed open-knit cotton with ribbed hem and cuffs and a full-needle placket. The texture is "
     "the point &mdash; this reads as a knit shirt, not a golf polo.",
 34: "The Brickwork in washed black. Same open knit, same ribbed trims. Harder to place as golf clothing, "
     "which is presumably the idea.",
 78: "Cotton and cashmere, engineered pointelle knit, full button front. The most expensive-feeling piece "
     "in the collection that is not a shoe.",
 54: "The Crosscut in cream. Ribbed sleeve cuffs, subtle branding, and a knit fine enough that it does not "
     "look like a polo at all.",
 48: "Stone-washed cotton herringbone twill, mid-rise, relaxed through the leg. Army herringbone, per "
     "Malbon's own spec sheet.",
 40: "The olive pant. Wide, pleated, cropped short enough to show the shoe &mdash; which given what is in "
     "the last section is probably deliberate.",
 26: "Lightweight stretch nylon, mesh-lined, elastic waist with an internal drawcord, dual zip back welt "
     "pockets, five-inch inseam. The one genuinely technical bottom here.",
 44: "Malbon and Red Wing rebuilt the Shop Moc Oxford for the course. Full-grain oiled Oro Legacy leather "
     "tanned by Red Wing's own S.B. Foot Tanning Company, classic moc toe, Goodyear welt, Traction Tred "
     "outsole. Goodyear welt means it can be resoled, which is a thing almost no golf shoe can claim. Four "
     "hundred dollars and the best object in the collection.",
 21: "A collaboration with CLUCT, the Tokyo streetwear label, carrying artwork by Kaji of Joytown Tattoo "
     "Studio. Handcrafted in Japan from brass with a thick sterling silver coating. Seventy-eight dollars "
     "for a divot tool is absurd and this one nearly justifies it.",
 37: "Stone-washed herringbone twill with a custom woven front label, five-panel, flat brim. The quiet "
     "alternative to the Ironworks cap.",
}

INTRO = """    <p>Malbon's Men's Fall collection runs to eighty-eight pieces, which is more than anyone needs to look
    at. We opened every image and cut it to twenty-seven.</p>
    <p>The useful thing about this one is that it has a spine. Malbon named a sub-line &mdash; Ironworks
    Division &mdash; and built it out of heavyweight stone-washed hickory-stripe denim, the striped cotton
    that painters and railroad crews wore. There is a jacket, a carpenter short, a pair of overalls, a
    sweatshirt, a snapback and a driver headcover, all in the same cloth with antique nickel hardware and
    hammer loops. It is the least golf-looking thing Malbon has made.</p>
    <p>Running underneath it are three other threads: a stone-washed herringbone twill called Station that
    covers a shirt, a pant and a cap; an all-over Inkwash print across two windshirts and a short; and a pair
    of knits doing the quiet work the logos usually do.</p>
    <p>And then there are two collaborations at the end that are better than anything Malbon made alone.</p>"""

FAQ = [
 ("What is Malbon's Ironworks Division collection?",
  "Ironworks Division is a workwear sub-line within Malbon's Fall 2026 collection, built from heavyweight "
  "stone-washed striped denim &mdash; hickory stripe &mdash; with antique nickel hardware. It includes the "
  "Foreman Jacket ($348), Foreman Short ($248), Foreman Overall ($348), Foreman Sweatshirt ($168), Foreman "
  "Snapback ($58) and the Division Driver Cover ($128)."),
 ("Is the Malbon Red Wing golf shoe a real collaboration?",
  "Yes. The Red Wing Moc Oxford is a collaboration between Malbon and Red Wing, reworking Red Wing's Shop "
  "Moc Oxford for golf. It is built in full-grain oiled Oro Legacy leather tanned by Red Wing's own S.B. "
  "Foot Tanning Company, with a moc toe, Goodyear welt construction and a Traction Tred outsole. It retails "
  "at $400."),
 ("Can the Malbon Red Wing golf shoe be resoled?",
  "It uses Goodyear welt construction, which is the standard resolable shoe construction and is what allows "
  "traditional work boots to be rebuilt rather than replaced. Almost no modern golf shoe is built this way, "
  "as most use cemented or injection-moulded soles."),
 ("Who made the Malbon CLUCT divot tool?",
  "It is a collaboration with CLUCT, a Tokyo streetwear label, featuring artwork by Kaji of Joytown Tattoo "
  "Studio. Malbon state each piece is handcrafted in Japan from brass with a thick sterling silver (925) "
  "coating. It retails at $78."),
 ("What is the Inkwash print in Malbon's fall collection?",
  "Inkwash is an all-over print that appears on the Pine Inkwash Windshirt in two colourways, indigo and "
  "olive, and on the matching Scooter Inkwash Short. The windshirts are 88% nylon and 12% elastane with "
  "mesh-lined back ventilation; the short is lightweight stretch nylon with a five-inch inseam."),
 ("What is Malbon's Station fabric?",
  "Station pieces are made from stone-washed cotton herringbone twill, described by Malbon as army "
  "herringbone twill. The fabric runs across the Station Shirt ($228, in brown and olive), the Station Pant "
  "($228) and the Station Snapback ($48)."),
 ("How much does Malbon's fall collection cost?",
  "The picks in this post run from $48 for the Station Snapback to $400 for the Red Wing Moc Oxford. Most "
  "of the collection sits between $148 and $248, with the heavyweight Ironworks denim outerwear and the "
  "Foreman Overall at $348."),
 ("Are any pieces in the Malbon fall collection preorder?",
  "Yes. At the time of writing Malbon list the Grounds Reversible Jacket and the Foreman Sweatshirt as "
  "preorder items shipping 26 August. Availability changes, so check the product page before ordering."),
]

def card(i):
    sl, m = BY_I[i]
    fr = m["frames"]
    alt = "%s Malbon %s" % (m["title"], (m["type"] or "").rstrip("s").lower())
    pg = ('<div class="product-gallery"><div class="pg-track">'
          + "".join('<div class="pg-frame"><img src="/images/malbon-fall/%s" loading="lazy" alt="%s"></div>'
                    % (f, alt) for f in fr)
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
    # HOUSE FORMAT: card text lives inside <div class="product-body"> (that div carries the
    # padding), and the outbound link is class="product-link". There is no .product-shop.
    return ('  <div class="product-card" data-frames="%d">\n'
            '    %s\n'
            '      <div class="product-body">\n'
            '        <div class="product-brand">Malbon &middot; %s</div>\n'
            '        <div class="product-name">%s &middot; $%s%s</div>\n'
            '        <div class="product-desc">%s</div>\n'
            '        <a href="%s" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a>\n'
            '      </div>\n'
            '  </div>\n') % (len(fr), pg, m["type"], m["title"], m["price"], sold, COPY[i], m["url"])

# Only genuinely new classes go here. .cat-kicker / .products-grid / .product-* already
# exist in the template — reuse them rather than inventing parallel styles.
CSS = """
.oos{font:500 10px/1 'JetBrains Mono',monospace;letter-spacing:.08em;text-transform:uppercase;
 color:#9a3b3b;border:1px solid #d9b3b3;border-radius:3px;padding:3px 6px;margin-left:5px;white-space:nowrap}
"""

h = BASE
h = h.replace("the-hat-edit-austin-summer", SLUG)
h = h.replace("/images/hat-edit/hero.jpg", "/images/malbon-fall/hero-malbon-fall.jpg")
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

def anchor(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:24]

# HOUSE FORMAT — do not deviate. Every section is:
#   <h2 id="…">  +  <p class="cat-kicker">  +  <div class="products-grid"> cards </div>
# Cards MUST sit inside .products-grid (3-up desktop / 2-up / 1-up). Direct children of
# <section class="products"> fall out of the grid and render full-width and oversized.
body = '<section class="products">\n'
for name, kicker, lede, ids in SECTIONS:
    body += ('<h2 id="%s">%s</h2>\n'
             '<p class="cat-kicker"><strong>%s</strong>%s</p>\n'
             '<div class="products-grid">\n' % (anchor(name), name, kicker, lede))
    body += "".join(card(i) for i in ids)
    body += '</div>\n'
# section left OPEN — template's </section> after the FAQ closes it
start = h.index('<section class="products">')
fq = h.index('<div class="faq">')
h = h[:start] + body + '  ' + h[fq:]

# HOUSE FORMAT: .faq-q + bare <p>. There is no .faq-item or .faq-a CSS on these pages.
faq_html = "".join('    <details class="faq-q"><summary>%s</summary><p>%s</p></details>\n'
                   % (q, a) for q, a in FAQ)
h = re.sub(r'(<div class="faq">).*?(  </div>\n</section>)',
           lambda m: m.group(1) + "\n" + faq_html + m.group(2), h, count=1, flags=re.S)
h = h.replace("</style>", CSS + "</style>", 1)

# ---- rebuild JSON-LD from this post's own content (template metadata leaks otherwise)
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
        d["image"] = ["https://thegrassyissue.com/images/malbon-fall/hero-malbon-fall.jpg"]
        d["datePublished"] = d["dateModified"] = "2026-08-20"
        if isinstance(d.get("mainEntityOfPage"), dict):
            d["mainEntityOfPage"]["@id"] = "https://thegrassyissue.com/drops/" + SLUG
        d.pop("keywords", None)
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + '</script>'
h = re.sub(r'<script type="application/ld\+json">(.*?)</script>', _fix_ld, h, flags=re.S)

# ---- residual Hat Edit metadata
h = h.replace("The Hat Edit — 28 Summer Caps, Ropes and Buckets From the Brands We Follow", TITLE_PLAIN)
h = h.replace("The Hat Edit &mdash; 28 Summer Caps, Ropes and Buckets From the Brands We Follow", TITLE)
h = re.sub(r'<span>\d+ Hats</span>', '<span>27 Pieces</span>', h)
h = h.replace('<span class="hashtag">#TheHatEdit</span>', '<span class="hashtag">#MalbonIronworks</span>')
h = re.sub(r'(<span class="l">Hats</span><span>)\d+(</span>)', r'\g<1>27\g<2>', h)
h = h.replace('<span class="l">Hats</span>', '<span class="l">Pieces</span>')
h = re.sub(r'(<span class="l">Brands</span><span>)\d+(</span>)', r'\g<1>3\g<2>', h)
h = h.replace('<span class="l">Brands</span>', '<span class="l">Collabs</span>')

MORE = ("""    <a href="/drops/the-hat-edit-austin-summer" class="more-card"><div class="more-kicker">The Edit</div><div class="more-title">The Hat Edit &mdash; Austin Summer</div></a>
    <a href="/drops/the-custom-wedge-report" class="more-card"><div class="more-kicker">The Report</div><div class="more-title">The Custom Wedge Report</div></a>
    <a href="/drops/the-lottery-round-austin-private-clubs" class="more-card"><div class="more-kicker">The Guide</div><div class="more-title">The Lottery Round &mdash; Austin Private Clubs</div></a>
""")
h = re.sub(r'(<div class="more-grid">).*?(</div>\s*</section>)',
           lambda m: m.group(1) + "\n" + MORE + "  " + m.group(2), h, count=1, flags=re.S)

out = os.path.join(S, "drops", SLUG + ".html")
open(out, "w", encoding="utf-8").write(h)
print("wrote", out, len(h), "bytes")
