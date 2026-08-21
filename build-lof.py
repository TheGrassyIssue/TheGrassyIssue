#!/usr/bin/env python3
# Left of Field Golf — Brand to Know. All facts verified against the brand's own site
# (about page, journal entries, product copy, policy pages) 2026-08-21.
# Prices are USD from lofgolf.com/en-us (rate ~0.73 to AUD). Run verify-post.py before pushing.
import os, re, json

S = os.path.dirname(os.path.abspath(__file__))
BASE = open(os.path.join(S, "drops/the-hat-edit-austin-summer.html"), encoding="utf-8").read()
MAN = json.load(open("/tmp/lof/man.json"))
BY_K = {v["k"]: (k, v) for k, v in MAN.items()}

SLUG = "brand-to-know-left-of-field-golf"
TITLE = "Brand to Know &mdash; Left of Field Golf, and the Australian Coast It Is Named After"
TITLE_PLAIN = "Brand to Know — Left of Field Golf, and the Australian Coast It Is Named After"
DESC = ("Left of Field Golf is a Sydney brand started in 2022 in a spare bedroom, built on surf and skate "
        "silhouettes rather than golf ones. Thirty-nine pieces across Elements, SOUTH, RNP, the Pintuck short, "
        "the caps and the Ciel Glue art collaboration.")

SECTIONS = [
 ("elements", "Elements", "The Barnbougle Collection",
  "Elements is their flagship technical line and the clearest thing they have made. It came out of a 2024 trip "
  "to Barnbougle in Tasmania for a mate&rsquo;s 30th &mdash; no plan, no shoot booked &mdash; and they went back "
  "later to photograph the campaign on the same ground. Bridport is the town the course sits beside, Anderson is "
  "the bay it overlooks, and Bass is the strait the wind comes off. Ilias wrote it up himself: "
  "&ldquo;At Barnbougle, the land doesn&rsquo;t host the course &mdash; it <em>is</em> the course. The wind "
  "becomes your caddie and your rival.&rdquo;"),
 ("south", "SOUTH", "The Mornington Peninsula",
  "The Victorian coast, an hour south of Melbourne. Portsea and Sorrento sit at the tip of the peninsula, "
  "Mornington is the town the collection is named for, and Bridgewater Bay is on the ocean side."),
 ("rnp", "RNP", "Royal National Park",
  "Australia&rsquo;s oldest national park, gazetted in 1879 and running down the coast south of Sydney. Audley "
  "is the village at its river crossing; Stanwell sits at its southern edge. The polos in this collection carry "
  "what Left of Field call an RNP yardage print."),
 ("pintuck", "The Pintuck", "The Short That Made Them",
  "Their own copy calls the original &ldquo;our answer to everything wrong with golf shorts today&rdquo; &mdash; "
  "roomy through the trunk, a wider leg opening, cut to sit just above the knee. It became their best seller, and "
  "the 2.0 is a refit of the same idea. If you want the surf-and-skate thesis in one garment, it is this one."),
 ("tees", "Tees", "Where the Thesis Is Most Literal",
  "Boxy, mid-weight, and closer to a skate tee than a golf shirt. The early Clovelly and Huskisson runs were cut "
  "from US cotton with the artwork finished in Marrickville, in Sydney&rsquo;s inner west."),
 ("caps", "Caps", "Including Two Very Good Jokes",
  "Left of Field run at least five separate marks &mdash; a script wordmark, a chainstitched L, a reversed L "
  "patch, a flag insignia and a black cockatoo. Two of the caps below are not really about the logo at all."),
 ("art", "Golf Art", "The Ciel Glue Collaboration",
  "Ciel Glue is a French collage artist based on the Portuguese coast. He surfed from the age of eleven, spent "
  "fifteen years doing graffiti in Paris, and now works entirely analogue &mdash; hand-cutting vintage magazines, "
  "old books and coloured paper. His organising idea is literary: <em>to read the wave</em>, extended into reading "
  "the green. In his words, &ldquo;first you read it, then you shred it.&rdquo; Left of Field showed his originals "
  "at their Melbourne pop-up and added the prints in January 2026. They ship unframed."),
 ("archive", "The Archive", "Sold Out, and Instructive",
  "Left of Field make small runs and let them go. What follows is gone &mdash; but the spread is the point: a "
  "$330 collaboration bag and a $4.90 ball marker, made by the same eight-person operation, four years apart."),
]

COPY = {
 # --- Elements
 32: "The flagship. Their Elements yardage print runs through it, and the collection it belongs to was designed "
     "after a trip to Barnbougle. One hundred and five dollars puts it at the top of their polo range and it is "
     "still the first thing to buy here.",
 27: "Named for Bass Strait, which is where the weather at Barnbougle comes from. The plainest polo in the "
     "Elements line and probably the most wearable thing they make.",
 38: "Windproof and water-repellent with an insulated front panel and YKK hardware. This is the piece that "
     "justifies calling Elements a technical line rather than a styling exercise.",
 29: "The grey contrast panel is not decoration. Left of Field say it is drawn from the curving paths that weave "
     "between Barnbougle&rsquo;s fairways &mdash; which is either very thoughtful or very Australian, and is "
     "probably both.",
 28: "Same trick, different reference: the sweeping panel lines are taken from the rolling dunes at Barnbougle. "
     "A gilet is the correct outer layer for a links course in wind and they clearly know it.",
 30: "The Elements short. Sage, mid-length, cut on the roomier block that runs through everything they do.",
 31: "Pleated, wide-legged and technical &mdash; the least golf-looking trouser in this post and the one most "
     "likely to get worn somewhere other than a course.",
 # --- SOUTH
 13: "The heaviest outer layer in the SOUTH collection, named for the town at the tip of the Mornington "
     "Peninsula. Two hundred and five dollars, and the closest they come to a proper coat.",
 12: "A quarter-zip named for Bridgewater Bay. Pale blue, clean, and the one piece here that would pass "
     "unremarked at a traditional club &mdash; which given the brand&rsquo;s founding complaint is quite funny.",
 14: "Royal blue with a textured face. Sorrento sits next to Portsea at the end of the peninsula; the polos are "
     "named in pairs like that throughout.",
 15: "Beige and white stripe with a rugby collar. The stripe polos are the most immediately recognisable thing "
     "they make and the beige is the better of the two.",
 16: "The same shirt in blue and white. Between this and the beige, the collection&rsquo;s whole colour story "
     "is on the table &mdash; sand, sea, and not much else.",
 # --- RNP
 41: "Sage, padded, with the script wordmark on the left chest. Audley is the old village at the Hacking River "
     "crossing inside Royal National Park, which is the sort of reference nobody outside Sydney will catch.",
 40: "Wide, pleated, black. Stanwell Tops sits above the coast at the park&rsquo;s southern end, where the "
     "escarpment drops to the sea.",
 # --- Pintuck
 19: "Cream, and the cleanest of the four. Above the knee, roomy through the trunk, wider through the leg "
     "opening than a modern golf short has any business being.",
 20: "Navy. The safest colourway and the one that will get worn most.",
 0:  "Slate, and the newest addition &mdash; added in July 2026, after the cream, navy and black.",
 11: "Not a Pintuck, but the same argument in a different fabric: mocha, elasticated, and closer to a swim short "
     "than anything in a pro shop.",
 # --- Tees
 7:  "Their heavyweight classic. Relaxed shoulders, a small chest hit, and the one that works at the course, the "
     "brewery and the airport without trying.",
 6:  "The bird here is a black cockatoo, which recurs across the brand &mdash; on ball markers, on headcovers, "
     "and on the back of caps.",
 52: "Named for Huskisson on the New South Wales south coast. The earlier tee runs were cut from US cotton with "
     "the artwork finished in Marrickville, in Sydney&rsquo;s inner west.",
 35: "A sprayed graphic on white, and the closest the range gets to the graffiti end of the founder&rsquo;s "
     "reference points.",
 # --- Caps
 44: "The best product they make and it is a joke. Sydney Harbour Golf &amp; Country Club does not exist. The "
     "crest is the Harbour Bridge with the two pylons replaced by golf bags, and the entire product description "
     "is five words long: &ldquo;The greatest course to never exist.&rdquo;",
 26: "Bootleg merch for a tournament, made by a brand with no relationship to it. The cap reads THE SOUTHERN "
     "SLAM / AUSTRALIAN OPEN 25 / ROYAL MELBOURNE, and Left of Field sold it at a three-day pop-up in Fitzroy "
     "during that week. Their own copy calls it &ldquo;an independent artistic interpretation&rdquo; and states "
     "plainly that it is not affiliated with any tournament or venue. Correct on both counts.",
 42: "WWOG is Wide World Of Golf. A cotton twill snapback with a slightly shortened brim, which they describe as "
     "their take on a classic vintage cap.",
 39: "The reversed L, applied as a large felt patch with a small circular dot set into the crook that reads as a "
     "golf ball. They have never explained why it is backwards.",
 1:  "Red plaid, and the outlier &mdash; the only loud pattern in a range built almost entirely on sand, sage "
     "and navy.",
 # --- Art
 23: "A diptych, and the most golf-specific thing Ciel Glue has made for them. Eighty-eight dollars, unframed, "
     "printed on 250gsm.",
 25: "A golfer on a Portuguese clifftop, which is where the artist actually lives. The golf prints run on 250gsm "
     "and the surf prints on 300gsm.",
 21: "The surf side of his practice, inspired by his local break at Praia Del Rey. This is the one that explains "
     "the whole collaboration &mdash; the brand and the artist arrived at golf from the same direction.",
 22: "All-female surfers, hand-cut from vintage magazines. Fifty-five dollars.",
 # --- Archive
 100: "Their most narrative product, made with the New Zealand bagmaker Hiroki. Waxed canvas with suede and "
      "leather, designed around the Sydney Red Gum &mdash; <em>Angophora costata</em> &mdash; with an Angophora "
      "bark print on the divider and a flower logo embossed into the leather base. Three hundred and thirty "
      "dollars and long gone.",
 101: "From their own tournament. Left of Field ran the inaugural Down Under (Par) Open in October 2024, a "
      "two-ball scramble at Shortees on Sydney&rsquo;s Northern Beaches, sponsored by a beer company. Ilias made "
      "his first career hole-in-one on the 16th that day.",
 102: "Beige and brown, from the RNP collection. Note that its URL still reads "
      "<em>wattamolla-polo</em> &mdash; Wattamolla is another beach inside Royal National Park, so an earlier "
      "name for this shirt survives in the link.",
 103: "Forest green, and the other half of the RNP polo pair. Garie is the beach at the end of the road through "
      "the park.",
 104: "The sold-out companion to Albatross. Ciel Glue&rsquo;s golf prints go quickly and Left of Field have not "
      "restocked this one.",
 105: "The black cockatoo, cast as a ball marker. Seven dollars fifty, and one of the few places the bird mark "
      "appears as the whole product rather than a detail.",
 106: "Published on 2 September 2022 &mdash; one of the two oldest products in the catalogue and effectively "
      "where the brand started. Four dollars ninety for a script marker in dark green.",
 107: "Tonal flowers on tan. We flagged this one as sold out in the Towel Edit and it has stayed that way.",
}
ARCH_K = {100: 39, 101: 40, 102: 41, 103: 42, 104: 43, 105: 44, 106: 45, 107: 46}

INTRO = """    <p>Left of Field Golf is four years old and runs out of Sydney. Nick Ilias started it in 2022 in his
    brother&rsquo;s old bedroom &mdash; his words, from a journal entry he wrote in Paris three years later:
    &ldquo;a small room filled with everything from late-night brainstorming sessions to boxes stacked high with
    stock.&rdquo;</p>
    <p>The founding complaint is one a lot of people will recognise. &ldquo;When I first started playing the
    game, getting dressed for golf felt like a lose-lose situation. The outfits I wanted to wear made me feel out
    of place in the pro shop. Adhering to the dress code just didn&rsquo;t feel natural, either.&rdquo;</p>
    <p>What he built instead is not, as it is often described, a brand about Australian landscapes. It is a brand
    about <strong>silhouette</strong>. In their own words the aim is clothing &ldquo;inspired by the attitude and
    silhouettes of surf and skate apparel, with design touches golfers can appreciate as their own,&rdquo; and
    then, flatly: &ldquo;Our mission isn&rsquo;t to create products that scream &lsquo;golf&rsquo;.&rdquo; That
    is why the shorts are roomy and the trousers are pleated and wide, and it is the single most useful thing to
    know before you look at any of it.</p>
    <p>The landscape part is real, but it operates one level down, in the naming. Every collection is tied to a
    specific stretch of Australian coast and the products take their names from places inside it. Elements is
    Barnbougle in Tasmania. SOUTH is the Mornington Peninsula. RNP is Royal National Park, south of Sydney. The
    earliest polos were named after beaches in Sydney Harbour, which is the one case where they said so outright:
    &ldquo;the Clontarf and Nielsen, named after iconic beaches within Sydney Harbour.&rdquo;</p>
    <p>Two other things matter. They spent seven months sampling fabric before releasing their first
    polo, landing on a recycled-PET yarn, and wrote about it plainly: &ldquo;We know we are stepping into an
    industry which is regarded as one of the biggest polluters on earth. But we don&rsquo;t plan to follow the
    footsteps of the past.&rdquo; And in February 2025 they showed at the Paris Golf Gallery during fashion week
    &mdash; their first international outing, sharing a room with Hiroki, Club 72 and Parmore.</p>
    <p>Thirty-nine pieces below, grouped the way the brand actually organises itself. Prices are US dollars from
    their American storefront; they also sell in Australian dollars, and ship worldwide.</p>"""

FAQ = [
 ("Who founded Left of Field Golf?",
  "Nick Ilias, who started the brand in Sydney in 2022. He has written that he began it in his brother&rsquo;s "
  "old bedroom, surrounded by boxes of stock. The company trades as LOFG Clubhaus Pty Ltd and is based in "
  "Beverly Hills, in Sydney&rsquo;s St George district."),
 ("What is Left of Field Golf's design philosophy?",
  "Their stated aim is golf clothing built on surf and skate silhouettes rather than traditional golf ones. In "
  "their own words: &ldquo;Our mission isn&rsquo;t to create products that scream &lsquo;golf&rsquo;. It&rsquo;s "
  "to make clothing that pushes the game&rsquo;s evolving style, while staying accessible enough to cut through "
  "the hype.&rdquo; The founding frustration was feeling out of place in a pro shop wearing what he actually "
  "wanted to wear."),
 ("Why are Left of Field products named after Australian places?",
  "Each collection is tied to a specific stretch of coast and the products are named for places within it. "
  "Elements takes its names from around Barnbougle in Tasmania (Bridport, Anderson, Bass). SOUTH is the "
  "Mornington Peninsula in Victoria (Portsea, Sorrento, Mornington, Bridgewater). RNP is Royal National Park "
  "south of Sydney (Audley, Stanwell, Garie). The brand confirmed the convention when it described two early "
  "polos as &ldquo;named after iconic beaches within Sydney Harbour.&rdquo;"),
 ("What is the Elements collection?",
  "Elements is Left of Field&rsquo;s flagship technical range, launched in October 2025. It was designed after a "
  "2024 trip to Barnbougle Dunes in Tasmania for a friend&rsquo;s 30th birthday, and the campaign was later shot "
  "at the same course. It includes the Elements Polo, Bass Polo, Elements Weather Jacket, Bridport Crewneck, "
  "Anderson Insulated Gilet, Dune Short and a pleated wide-leg technical trouser."),
 ("What is the Pintuck short?",
  "The Pintuck is Left of Field&rsquo;s signature golf short and, by their own description, their best seller. "
  "The brand pitched the original as &ldquo;our answer to everything wrong with golf shorts today&rdquo; &mdash; "
  "a roomier fit through the trunk, a wider leg opening, and a length that sits just above the knee. Pintuck 2.0 "
  "arrived in 2026 as a refined version and runs in cream, navy, black and slate."),
 ("Is Sydney Harbour Golf &amp; Country Club a real club?",
  "No. It is invented. Left of Field&rsquo;s entire product description for the cap is &ldquo;The greatest course "
  "to never exist.&rdquo; The crest shows the Sydney Harbour Bridge with its two pylons replaced by bags of golf "
  "clubs. It has been one of their longest-running products since August 2024."),
 ("What is the Southern Slam cap?",
  "An unofficial, self-made tribute to the Australian summer of golf, sold at a three-day Left of Field pop-up in "
  "Fitzroy, Melbourne, over the weekend of the 2025 Australian Open at Royal Melbourne. The brand states clearly "
  "that it is &ldquo;an independent artistic interpretation and is not affiliated with, endorsed by, or sponsored "
  "by any official tournament or venue.&rdquo; There is no event actually called the Southern Slam."),
 ("Who is Ciel Glue?",
  "A French collage artist based on the Portuguese coast, who collaborates with Left of Field on their Golf Art "
  "prints. He began surfing at eleven and spent fifteen years doing graffiti in Paris before moving to collage. "
  "He works entirely analogue, hand-cutting vintage magazines, old books and coloured paper. His originals were "
  "shown at Left of Field&rsquo;s Melbourne pop-up in December 2025 and the prints were added in January 2026."),
 ("Does Left of Field Golf ship to the United States?",
  "Yes. They run a US storefront at lofgolf.com/en-us priced in US dollars, and ship internationally from "
  "Australia. Their published international rates are A$29.95 standard, which they quote at six to twelve "
  "business days, and A$66.95 express at three to seven. Returns are free within 30 days."),
 ("Where can I buy Left of Field Golf in a shop?",
  "They list five stockists: Playfair Golf Club and Woolooware Golf Pro Shop in Australia, Club 72 and Soft "
  "Hands Club in the United Kingdom, and Happy Golfer in Sweden. Otherwise it is direct from lofgolf.com. They "
  "have no permanent retail of their own and trade through occasional pop-ups."),
]

def anchor(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')[:24]

SEC_ORDER = ["elements", "south", "rnp", "pintuck", "tees", "caps", "art", "archive"]

def card(k):
    # COPY is keyed by pool index (and 100-107 for the archive); the manifest is keyed by
    # download order. POOL2K bridges the two — build it from the same section order used
    # when the images were fetched.
    real_k = POOL2K[k]
    sl, m = BY_K[real_k]
    fr = m["frames"]
    alt = "%s Left of Field Golf" % m["title"]
    pg = ('<div class="product-gallery"><div class="pg-track">'
          + "".join('<div class="pg-frame"><img src="/images/left-of-field/%s" loading="lazy" alt="%s"></div>'
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
    # HOUSE FORMAT: text inside .product-body, outbound link is .product-link
    return ('  <div class="product-card" data-frames="%d">\n'
            '    %s\n'
            '      <div class="product-body">\n'
            '        <div class="product-brand">Left of Field Golf</div>\n'
            '        <div class="product-name">%s &middot; $%s%s</div>\n'
            '        <div class="product-desc">%s</div>\n'
            '        <a href="%s" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a>\n'
            '      </div>\n'
            '  </div>\n') % (len(fr), pg, m["title"], m["price"], sold, COPY[k], m["url"])

SEC_IDS = {
 "elements": [32, 27, 38, 29, 28, 30, 31],
 "south":    [13, 12, 14, 15, 16],
 "rnp":      [41, 40],
 "pintuck":  [19, 20, 0, 11],
 "tees":     [7, 6, 52, 35],
 "caps":     [44, 26, 42, 39, 1],
 "art":      [23, 25, 21, 22],
 "archive":  [100, 101, 102, 103, 104, 105, 106, 107],
}

POOL2K = {}
_k = 0
for _sec in SEC_ORDER:
    for _pi in SEC_IDS[_sec]:
        POOL2K[_pi] = _k
        _k += 1
assert _k == len(MAN), "POOL2K built %d entries, manifest has %d" % (_k, len(MAN))

CSS = """
.oos{font:500 10px/1 'JetBrains Mono',monospace;letter-spacing:.08em;text-transform:uppercase;
 color:#9a3b3b;border:1px solid #d9b3b3;border-radius:3px;padding:3px 6px;margin-left:5px;white-space:nowrap}
"""

h = BASE
h = h.replace("the-hat-edit-austin-summer", SLUG)
h = h.replace("/images/hat-edit/hero.jpg", "/images/left-of-field/hero-left-of-field.jpg")
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
for key, name, kicker, lede in SECTIONS:
    body += ('<h2 id="%s">%s</h2>\n<p class="cat-kicker"><strong>%s</strong>%s</p>\n'
             '<div class="products-grid">\n' % (anchor(name), name, kicker, lede))
    body += "".join(card(i) for i in SEC_IDS[key])
    body += '</div>\n'
start = h.index('<section class="products">')
fq = h.index('<div class="faq">')      # FAQ div sits INSIDE the products section
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
        d["image"] = ["https://thegrassyissue.com/images/left-of-field/hero-left-of-field.jpg"]
        d["datePublished"] = d["dateModified"] = "2026-08-21"
        if isinstance(d.get("mainEntityOfPage"), dict):
            d["mainEntityOfPage"]["@id"] = "https://thegrassyissue.com/drops/" + SLUG
        d.pop("keywords", None)
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + '</script>'
h = re.sub(r'<script type="application/ld\+json">(.*?)</script>', _fix_ld, h, flags=re.S)

h = h.replace("The Hat Edit — 28 Summer Caps, Ropes and Buckets From the Brands We Follow", TITLE_PLAIN)
h = h.replace("The Hat Edit &mdash; 28 Summer Caps, Ropes and Buckets From the Brands We Follow", TITLE)
h = re.sub(r'<span>\d+ Hats</span>', '<span>39 Pieces</span>', h)
h = h.replace('<span class="hashtag">#TheHatEdit</span>', '<span class="hashtag">#LeftOfFieldGolf</span>')
h = re.sub(r'(<span class="l">Hats</span><span>)\d+(</span>)', r'\g<1>39\g<2>', h)
h = h.replace('<span class="l">Hats</span>', '<span class="l">Pieces</span>')
h = re.sub(r'(<span class="l">Brands</span><span>)\d+(</span>)', r'\g<1>8\g<2>', h)
h = h.replace('<span class="l">Brands</span>', '<span class="l">Collections</span>')

MORE = ("""    <a href="/drops/3-aussie-golf-brands-you-should-know" class="more-card"><div class="more-kicker">The Edit</div><div class="more-title">3 Aussie Golf Brands You Should Know</div></a>
    <a href="/drops/walker-golf-blooming-grounds-drop" class="more-card"><div class="more-kicker">The Drop</div><div class="more-title">Walker&rsquo;s Blooming Grounds</div></a>
    <a href="/drops/the-ball-marker-atlas" class="more-card"><div class="more-kicker">The Atlas</div><div class="more-title">The Ball Marker Atlas</div></a>
""")
h = re.sub(r'(<div class="more-grid">).*?(</div>\s*</section>)',
           lambda m: m.group(1) + "\n" + MORE + "  " + m.group(2), h, count=1, flags=re.S)

out = os.path.join(S, "drops", SLUG + ".html")
open(out, "w", encoding="utf-8").write(h)
print("wrote", out, len(h), "bytes")
