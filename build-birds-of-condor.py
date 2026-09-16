#!/usr/bin/env python3
"""Brand to Know — Birds of Condor.

WHY THIS POST EXISTS
--------------------
Birds of Condor carries 14 internal mentions across TGI — the fourth-most
referenced brand on the site — and had no dedicated page. Its profile pointer
went to /drops/australian-golf-brands-and-trips, where it was one of six. Lenny
picked it off the revisit shortlist on 2026-09-15 over Malbon, which has the
same problem at 41 mentions and is deferred.

THE SPINE. Frankie Kimpton was a booking agent for Mushroom in Melbourne who
surfed before he played golf, felt unwelcome at the driving range, and started
a hat brand. The thesis quote is a customer's, relayed by him: people buy the
hats without knowing it is a golf brand. Everything else on the page serves
that — the fake Japanese country clubs, the tie-dye Greg Norman parody, the
128 stockists split between golf clubs and surf shops.

SOURCING — every quote is verbatim from a named speaker with a URL:
  - Frankie Kimpton to Kari Hamanaka, Shop-Eat-Surf, 2026-03-04
  - Frankie Kimpton to Angus Smith, Byron Coast Times, 2025-10-31
The condor/triple-eagle explanation is the brand's OWN About-page copy and is
labelled as brand copy on the page, not attributed to a person. Zoe Kimpton is
named as co-founder and nothing more — there is not one published quote from
her anywhere, so she is not given a characterisation.

DELIBERATELY NOT ASSERTED (all checked, none verifiable):
  - a single founding year. The brand says 2016; Shop-Eat-Surf's "seven years
    in" implies 2017; Frankie's own "ten years in" implies 2015. The page says
    the brand dates itself to 2016 from an idea that started around 2013-14,
    and goes no narrower.
  - where anything is MADE. No country, factory or supplier is published
    anywhere. "Designed in Byron Bay" is the only geographic claim the brand
    makes, and designed is not made. Guarded below.
  - any tour player wearing it. Nothing found. The LIV Golf relationship is a
    merchandise licence sold through LIV's shop, NOT a player deal, and the two
    must not blur. Frankie's sourced claim is about WSL surfers, not golfers.
  - any award. None found.
  - the word "larrikin". It is a fair critic's read and the obvious reach for
    an Australian brand with cartoons on it, but nobody on the record says it.
    Their own vocabulary is "art-heavy", "alt-golf", "against the grain".
  - that no condor has been made in professional golf. That is the brand's own
    line, repeated as their claim, not as fact.

US vs AU. There are two storefronts. us.birdsofcondor.com prices in USD and
ships from Buena Park, California with no tariffs; birdsofcondor.com prices in
AUD and carries a much deeper catalogue. Every product linked here is from the
US store and priced in USD, because our readers are American and the duty
difference is real. The genuinely characteristic novelties — air fresheners,
29 beer koozies, the Hat Caddy, the surfboard — are AU-only, and the page says
so rather than linking Americans at a checkout that will surprise them.

STOCK: read 2026-09-15 from variant `available` flags, never page text.

TWITTER TAGS: this script mirrors og: -> twitter:. Eleven posts shipped with
another post's share card because no build script did this. Do not remove it.

DATE FORMAT: numeric M/D, M/D/YY in the header.
FAQ MARKUP: <details class="faq-q"><summary> — div markup fails verify-post.
"""
import re, os, json

SLUG = "brand-to-know-birds-of-condor"
TITLE = "Brand to Know &mdash; Birds of Condor"
PLAIN = "Brand to Know — Birds of Condor"
DESC = ("Birds of Condor explained: Frankie and Zoe Kimpton's Byron Bay label, the "
        "condor that gives it its name, the fake Japanese country clubs on its best-selling "
        "hats, the Coogi and Lyle & Scott collabs, and why half its stockists are surf shops. "
        "Seventeen pieces, US prices and stock checked 9/15/26.")
IMG = "/images/birds-of-condor/"
AU = "https://birdsofcondor.com"
US = "https://us.birdsofcondor.com"
VOL2 = "/drops/off-course-vol-2-golf-brands-doing-non-golf-things"
AUSSIE = "/drops/australian-golf-brands-and-trips"

M = json.load(open("research/birds-of-condor/manifest.json"))

COPY = {
 # ------------------------------- THE HATS -------------------------------
 "tokyo-snapback": ("Tokyo Country Club Snapback",
  "This is the single best-selling thing the brand makes: washed black denim, 100% cotton, retro patch. The club on the front does not exist."),
 "osaka-snapback": ("Osaka Country Club Snapback",
  "The sister motif in blue denim, fifteen SKUs deep. Tokyo and Osaka take every one of the top eleven slots in the store&rsquo;s own bestseller order."),
 "tokyo-camo": ("Tokyo Country Club Camo Snapback",
  "The same invented club rendered on RealTree-style hunting camo, which is either a joke about golf&rsquo;s relationship with the outdoors or just a good hat. Possibly both."),
 "eldrick": ("Eldrick Snapback",
  "Custom tiger camo, black rope, slight curve brim, sized for larger heads. Eldrick is Tiger Woods&rsquo; actual first name, and that is the entire gag."),
 "neverfind-boonie": ("Neverfind Boonie",
  "Wide-brim sun-smart boonie with a chin cord, printed with the golf-ball motif, in five colourways. The top of the headwear price ladder and the least golf-shaped silhouette they sell."),
 "georgia-visor": ("Georgia Tour Visor",
  "A Masters-green tour visor with a dogwood on the front, from a collection called Georgia On My Mind. Nobody is naming anything here by accident."),
 # ------------------------------ THE CLOTHES -----------------------------
 "lawnpawn-polo": ("Lawn Pawn Polo",
  "Blue and green plaid from the Lawn Pawn collection, whose whole premise is mow lines. S to XXXL, which is a wider run than most brands this size bother with."),
 "belair-qz": ("Bel-Air Quarter Zip Polo",
  "A knitted quarter-zip in cream and rust stripe with a black collar and sleeves &mdash; the most restrained thing in the store, and evidence they can do quiet when they want to."),
 "weekend-hood": ("Weekend at Birdies Hood",
  "Natural-ground hoodie with a checkerboard panel down the sleeve. The pun is doing a lot of work and the hoodie is doing the rest."),
 "condor5000-vest": ("Condor 5000 Shell Vest",
  "A shell vest carrying NASCAR-parody race graphics across the back. Black from the front, which is how it gets into the clubhouse."),
 "global-jacket": ("Global All-Weather Rain Jacket",
  "The most expensive garment they make: a black wind-and-rain shell with taped seams and zip pockets. Proof the catalogue is not only prints."),
 # ------------------------------ THE COLLABS -----------------------------
 "coogi-polo": ("Coogi Polo",
  "DriRelease jersey under an officially licensed archival Coogi print, with debossed branded buttons. <strong>L and XL are gone</strong>; S and M remain."),
 "coogi-tee": ("Coogi T-Shirt",
  "The same licensed print on 100% GOTS-certified organic cotton with a ribbed crew neck, S to XXL. The cheapest way into a collaboration that is now four years old."),
 # -------------------------------- THE ODD -------------------------------
 "lawnpawn-umbrella": ("Lawn Pawn Umbrella",
  "A full-size golf umbrella in mow-line plaid with <em>&ldquo;Peace Love &amp; Putts&rdquo;</em> printed across the inside of the canopy, so only the person holding it can read it. Published 9/15, the newest thing in the store."),
 "playing-cards": ("Golf Life Playing Cards",
  "Fifty-four cards on black-core stock with green foil edging, soft-touch matte lamination and an embossed tuck box sealed with a Triple Eagle sticker. Sold on the US store and nowhere else."),
 "norm-cover": ("Norm Mallet Putter Cover",
  "Blue tie-dye, a cartoon shark in a cap, and a name that is one syllable away from a lawsuit. Tentile shell, crystal velvet lining, magnetic closure, biodegradable packaging."),
 "lords-stickers": ("Lords of Swing Sticker Pack",
  "Twenty-two UV-resistant matt vinyl stickers of koala golfers drawn by Kentaro Yoshida. Fifteen dollars, and the purest distillation of the whole brand."),
}

SECTIONS = [
 ("The Hats",
  "Hats were the first product and remain the best seller. Two invented Japanese country clubs do most of the heavy lifting.",
  ["tokyo-snapback", "osaka-snapback", "tokyo-camo", "eldrick", "neverfind-boonie", "georgia-visor"]),
 ("The Clothes",
  "The apparel runs wider than the prints suggest, and prices ladder cleanly from eighty dollars to a hundred and seventy-five.",
  ["lawnpawn-polo", "belair-qz", "weekend-hood", "condor5000-vest", "global-jacket"]),
 ("The Collaborations",
  "Two are still buyable in full: COOGI, the Australian knitwear house, and Lyle &amp; Scott, which is 151 years old.",
  ["coogi-polo", "coogi-tee"]),
 ("The Odd End",
  "This is where the brand actually lives &mdash; and where the catalogue stops looking like a golf brand at all.",
  ["lawnpawn-umbrella", "playing-cards", "norm-cover", "lords-stickers"]),
]

INTRO = f"""<div class="writeup">
  <div class="writeup-body">
    <p>Frankie Kimpton booked bands for Mushroom in Melbourne before he made golf hats. He grew up surfing competitively in Byron Bay, and golf was the thing he and his mates did when there were no waves. When he started turning up at driving ranges more often, he did not fit, and he has been unusually direct about why.</p>
    <div class="pull-quote">
      <div class="pull-quote-inner">&ldquo;We&rsquo;d rock in with our black jeans and Guns N&rsquo; Roses tees on and get some very interesting looks from the Titleist shirt-tucked, &lsquo;Perry Pros&rsquo; that maxed out the bays. No disrespect to those guys, but the vibe was pretty thick and uninviting. That&rsquo;s when I realized there was nothing really catering, from a fashion sense in golf, for the rest of us &ndash; and we could hit a ball real good, too.&rdquo;<span class="pull-quote-attr">&mdash; Frankie Kimpton, founder, to Shop-Eat-Surf</span></div>
    </div>
    <p>He and Zoe Kimpton, his wife and co-founder, started with ten hats out of a garage. The brand dates itself to 2016, from an idea that began on Melbourne driving-range lunch breaks around 2013 and 2014. Within months it was shipping to South Korea, Japan and the United States. It now has roughly 128 stockists across Australia and New Zealand, and the split is the whole story: about half are golf clubs and driving ranges, and about half are surf and skate shops &mdash; Culture Kings, Stateside Sports, Hillzeez. In November 2025 they opened a first flagship on Lawson Street in Byron Bay, with a restored 1980s golf buggy in the fit-out.</p>
    <p>The clearest statement of what they are is a line Frankie repeats from a customer.</p>
    <div class="pull-quote">
      <div class="pull-quote-inner">&ldquo;One of the best comments I ever heard was from a customer who said, &lsquo;I didn&rsquo;t even know you guys were a golf brand; I just loved the hats.&rsquo; To me, that confirmed that we were on track with our brand.&rdquo;<span class="pull-quote-attr">&mdash; Frankie Kimpton, founder, to Shop-Eat-Surf</span></div>
    </div>
  </div>
</div>
"""

NAME = """<section class="products">
  <h2 class="products-hdr">What a Condor Actually Is</h2>
  <p class="cat-kicker">The name is a scoring term, and for once the brand explains itself.</p>
  <div class="writeup-body">
    <p>A birdie is one under on a hole. An eagle is two. An albatross is three. A condor is four &mdash; a hole in one on a par five &mdash; and in the brand&rsquo;s own words on its About page, it is <em>&ldquo;the rarest event in golf. Only a handful ever recorded, none of which have occurred in professional golf. It&rsquo;s also known as a Triple Eagle and is what our logo represents.&rdquo;</em> That last part is literal: the mark stacks three W-shaped eagles.</p>
    <p>Asked why that name and not something more direct, Frankie Kimpton gave an answer that explains the whole catalogue:</p>
    <div class="pull-quote">
      <div class="pull-quote-inner">&ldquo;We wanted something that didn&rsquo;t hit you straight away. Birds of Condor felt a bit mysterious, and it captured that feeling of magic on the course when everything stands still and you&rsquo;re high-fiving your mates after rolling in a putt.&rdquo;<span class="pull-quote-attr">&mdash; Frankie Kimpton, co-founder, to the Byron Coast Times</span></div>
    </div>
  </div>
</section>
"""

ART = """<section class="products">
  <h2 class="products-hdr">They Do Not Draw It Themselves</h2>
  <p class="cat-kicker">Three named artists, and a stated method.</p>
  <div class="writeup-body">
    <div class="pull-quote">
      <div class="pull-quote-inner">&ldquo;We are an art-heavy brand and absolutely thrive on working with an array of artists from around the world to level up our ideas.&rdquo;<span class="pull-quote-attr">&mdash; Frankie Kimpton, founder, to Shop-Eat-Surf</span></div>
    </div>
    <p>That is not a boilerplate claim, and the receipts are on the products. <strong>Kentaro Yoshida</strong> drew the koala golfers of the Lords of Swing series. <strong>Dan Coy</strong>, an Australian tattoo artist, created Birdie &mdash; a winged golf ball &mdash; as a new character for the Lyle &amp; Scott capsule. <strong>Lee McConnell</strong> did the Australian-themed Legionnaire caps that carried the phrase &ldquo;Playa Straya&rdquo;, the run the brand used in January 2020 to donate fifteen Australian dollars a hat to WIRES during the bushfires.</p>
    <p>What the brand does not publish is where any of it is made. There is no country of manufacture, no factory, no supplier list. The only geographic claim is that it is designed in Byron Bay, and designed is not made. We are noting that rather than filling the gap.</p>
  </div>
</section>
"""

BUYING = f"""<section class="products">
  <h2 class="products-hdr">Buying It From Here</h2>
  <p class="cat-kicker">Two storefronts, and the American one is missing the best stuff.</p>
  <div class="writeup-body">
    <p>There is a <a href="{US}">US store</a> priced in dollars that ships from a warehouse in Buena Park, California, with free shipping over $75 and a badge on every product page reading &ldquo;No tariffs, no surprises.&rdquo; It does not ship internationally. There is also the <a href="{AU}">Australian store</a>, priced in Australian dollars, which carries a substantially deeper catalogue. Every price on this page is from the US store.</p>
    <p>The catch is that the most characteristic things Birds of Condor makes are not on the American site. The four car air fresheners, the twenty-nine beer koozies, the tiger-camo Hat Caddy hard case that holds five hats, the one-of-one surfboard shaped with Misfit &mdash; all Australian store only. One of those air fresheners is in our <a href="{VOL2}">Off Course Vol. 2</a> roundup, priced in Australian dollars for exactly this reason. The trade runs the other way on precisely one item: the playing cards are American-only.</p>
    <p>A few other things to know before you order. Prices are laddered with unusual discipline &mdash; snapbacks are a flat $50, headcovers $50, putter grips $35, towels $35, ball markers $15. Left-handed golfers are out of luck on gloves: every right-hand variant is sold out across all three glove products. And a cluster of the Tokyo Country Club headcovers is dead stock, so if you want a cover, the Lawn Pawn and Georgia ones are the healthy ones.</p>
  </div>
</section>
"""

FAQ_ITEMS = [
 ("What is a condor in golf?",
  "A condor is four under par on a single hole &mdash; in practice a hole in one on a par five. It sits above a birdie (one under), an eagle (two under) and an albatross (three under), and it is also called a triple eagle. Birds of Condor takes its name and its logo from it; the mark stacks three W-shaped eagles. The brand describes it on its own About page as the rarest event in golf."),
 ("Who founded Birds of Condor?",
  "Frankie and Zoe Kimpton, a married couple based in Byron Bay, New South Wales. Frankie is credited as founder and creative director and worked as a booking agent for the Australian music company Mushroom before starting the brand; Zoe is credited as co-founder. The brand dates itself to 2016, from an idea that began in Melbourne around 2013 and 2014, and the first drop was ten hats."),
 ("Where is Birds of Condor made?",
  "The brand does not say. It publishes no country of manufacture, no factory and no supplier information anywhere on its site. What it does publish is that the range is designed in Byron Bay, that its accessories meet Oeko-Tex Standard 100, that its headcovers ship in biodegradable packaging, and that the 2022 Coogi capsule used organic cotton and recycled polyester. Anyone telling you where the hats are sewn is guessing."),
 ("Can you buy Birds of Condor in the US?",
  "Yes. There is a separate US storefront at us.birdsofcondor.com priced in US dollars and shipping from a California warehouse, with no import duty and free shipping over $75. It carries the hats, apparel and headcovers but not the air fresheners, koozies, Hat Caddy or surfboard, which are Australian-store only. In physical retail the brand is carried by DICK'S Sporting Goods, Golf Galaxy and PGA TOUR Superstore."),
 ("What has Birds of Condor collaborated on?",
  "The two that matter are COOGI, the Australian knitwear house whose sweaters Biggie Smalls wore, which produced an eleven-piece capsule in July 2022; and Lyle &amp; Scott, the Scottish label founded in 1874, whose two-part &ldquo;Friends of a Feather&rdquo; drop landed in 2024 with a new winged-golf-ball character by tattoo artist Dan Coy. Both are still buyable. There is also a merchandise line sold through LIV Golf's own shop, and a &ldquo;Grow the Game&rdquo; collection with Ugandan golfer Kawuki &ldquo;Roger&rdquo; Sali whose proceeds went to a junior programme in Entebbe."),
 ("What is Birds of Condor's best-selling product?",
  "The Tokyo Country Club snapback. The brand's own store sorts Tokyo and Osaka Country Club hats into all eleven of the top bestseller positions, and its listing copy for newer versions describes them as evolutions of its best-selling hats. Tokyo Country Club is thirteen products deep and Osaka fifteen &mdash; the two deepest single-motif families it sells. Neither club exists."),
]
FAQ = """<section class="products">
  <h2 class="products-hdr" id="faq">The Questions</h2>
  <div class="faq">
""" + "\n".join(f'    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>'
                for q, a in FAQ_ITEMS) + """
  </div>
</section>
"""


def frames(s):
    n = 1
    while os.path.exists(f"images/birds-of-condor/{s}-a{n+1}.jpg"):
        n += 1
    return n


def gal(s, name):
    n = frames(s)
    pl = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>|&[a-z]+;|&#\d+;', '', name)).strip()
    if n == 1:
        return (f'<div class="product-gallery"><div class="pg-track"><div class="pg-frame">'
                f'<img src="{IMG}{s}.jpg" alt="{pl}" loading="lazy" /></div></div></div>')
    fr = "".join(f'<div class="pg-frame"><img src="{IMG}{s}{"" if i==0 else f"-a{i+1}"}.jpg" '
                 f'alt="{pl} &middot; view {i+1} of {n}" loading="lazy" /></div>' for i in range(n))
    dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" '
                   f'aria-label="View image {i+1}"></button>' for i in range(n))
    return (f'<div class="product-gallery"><div class="pg-track">{fr}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>')


def price_tag(r):
    p, a = str(r["price"]).strip(), r["availability"]
    if a == "sold out":
        return f"{p} &middot; sold out"
    if a.startswith("partial"):
        return f"{p} &middot; almost gone"
    return p


def card(s):
    r = M[s]
    name, desc = COPY[s]
    return f"""<div class="product-card" data-frames="{frames(s)}">
      {gal(s, name)}
      <div class="product-body">
        <div class="product-brand">Birds of Condor</div>
        <div class="product-name">{name} &middot; {price_tag(r)}</div>
        <div class="product-desc">{desc}</div>
        <a href="{r['url']}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a>
      </div>
    </div>"""


def sec(head, kicker, slugs):
    c = "\n    ".join(card(s) for s in slugs)
    return (f'<section class="products">\n  <h2 class="products-hdr">{head}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'  <div class="products-grid">\n    {c}\n  </div>\n</section>\n')


def st(s):
    for a, b in [("&ldquo;", '"'), ("&rdquo;", '"'), ("&rsquo;", "'"), ("&lsquo;", "'"),
                 ("&amp;", "&"), ("&mdash;", "—"), ("&middot;", "·"), ("&ndash;", "–"),
                 ("&times;", "×"), ("&pound;", "£")]:
        s = s.replace(a, b)
    return re.sub(r'<[^>]+>', '', s)


SCHEMA = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": st(q),
                          "acceptedAnswer": {"@type": "Answer", "text": st(a)}}
                         for q, a in FAQ_ITEMS]}

PULLQUOTE_CSS = (
    "/*TGI-PULLQUOTE*/\n"
    ".pull-quote{max-width:1400px;margin:0 auto;padding:0 32px}\n"
    ".pull-quote-inner{font-family:var(--serif);font-style:italic;font-size:22px;"
    "line-height:1.4;padding:32px 0;margin:0;border-top:.5px solid rgba(20,20,20,.15);"
    "border-bottom:.5px solid rgba(20,20,20,.15);color:var(--grass)}\n"
    ".pull-quote-attr{font-family:var(--mono);font-style:normal;font-size:10px;"
    "letter-spacing:.14em;text-transform:uppercase;color:var(--ink);opacity:.45;"
    "margin-top:12px;display:block}\n"
    "@media(max-width:768px){.pull-quote{padding:0 20px}"
    ".pull-quote-inner{font-size:18px;padding:24px 0}}\n"
    "/*/TGI-PULLQUOTE*/")
# The model page (Gamut) has no pull-quote rule, so verify-post fails "every class
# used has a CSS rule" without this. Copied verbatim from brand-to-know-manors.html,
# which is where the house style for attributed quotes actually lives. Same move as
# the .cat-kicker rule carried onto the TwentyFour page on 2026-09-14.

model = open("drops/brand-to-know-gamut-golf.html", encoding="utf-8").read()
head = model[:model.find('<div class="breadcrumb">')]
tail = model[model.find('<section class="more"'):]
head = re.sub(r'<title>[^<]*</title>', f'<title>{PLAIN} — The Grassy Issue</title>', head)
for k, v in [("description", DESC), ("og:title", PLAIN), ("og:description", DESC)]:
    head = re.sub(rf'(<meta (?:name|property)="{re.escape(k)}" content=")[^"]*(")',
                  lambda m: m.group(1) + v + m.group(2), head)
for k, v in [("twitter:title", PLAIN), ("twitter:description", DESC)]:
    head = re.sub(rf'(<meta name="{k}" content=")[^"]*(")',
                  lambda m, v=v: m.group(1) + v + m.group(2), head)
head = re.sub(r'(<link rel="canonical" href=")[^"]*(")',
              lambda m: m.group(1) + f"https://thegrassyissue.com/drops/{SLUG}" + m.group(2), head)
head = re.sub(r'(<meta property="og:url" content=")[^"]*(")',
              lambda m: m.group(1) + f"https://thegrassyissue.com/drops/{SLUG}" + m.group(2), head)
head = re.sub(r'(<meta property="og:image" content=")[^"]*(")',
              lambda m: m.group(1) + f"https://thegrassyissue.com{IMG}tokyo-snapback.jpg" + m.group(2), head)
if "TGI-PULLQUOTE" not in head:
    head = head.replace("</style>", PULLQUOTE_CSS + "\n</style>", 1)
_sb = '<script type="application/ld+json">' + json.dumps(SCHEMA) + '</script>'
head = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: _sb, head, flags=re.S)

N = sum(len(s[2]) for s in SECTIONS)
body = ('<div class="breadcrumb">\n  <a href="/">Feed</a><span>/</span>\n'
        '  <a href="/#feed">Drops &amp; Brands</a><span>/</span>\n  Birds of Condor</div>\n'
        f'<header class="drop-header">\n  <h1>{TITLE}</h1>\n  <div class="drop-meta">\n'
        '    <span>9/15/26</span><span class="dot"></span>\n'
        '    <span>Drops &amp; Brands</span><span class="dot"></span>\n'
        f'    <span>Byron Bay, Australia &middot; {N} Pieces</span>\n  </div>\n</header>\n\n'
        f'<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}tokyo-snapback.jpg" '
        'alt="The Tokyo Country Club snapback, the best-selling hat Birds of Condor makes" /></div></div>\n'
        + INTRO + NAME
        + "".join(sec(*s) for s in SECTIONS)
        + ART + BUYING + FAQ)

# ---- guards -------------------------------------------------------------
placed = [s for sc in SECTIONS for s in sc[2]]
if sorted(placed) != sorted(COPY):
    raise SystemExit(f"section/COPY mismatch: unplaced={set(COPY)-set(placed)} extra={set(placed)-set(COPY)}")
if len(placed) != len(set(placed)):
    raise SystemExit("a stem is placed twice")
miss = [s for s in placed if s not in M]
if miss:
    raise SystemExit(f"placed but not in manifest: {miss}")
gone = [s for s in placed if not os.path.exists(f"images/birds-of-condor/{s}.jpg")]
if gone:
    raise SystemExit(f"images missing on disk: {gone}")
_txt = re.sub(r'<[^>]+>', ' ', body)
if re.search(r'\bworth\b', _txt, re.I):
    raise SystemExit("BANNED WORD 'worth' in the body copy")
# manufacturing: the brand publishes NONE, so the page must not imply any
for bad in ["made in australia", "australian-made", "australian made", "sewn in byron",
            "made in byron", "handmade in australia"]:
    if bad in _txt.lower():
        raise SystemExit(f"'{bad}' — Birds of Condor publishes NO manufacturing information")
if "larrikin" in _txt.lower():
    raise SystemExit("'larrikin' is nobody's word but ours — not on the record, keep it out")
# LIV is a merch licence, never a player deal
if re.search(r"liv (golf )?(player|pro|tour)", _txt, re.I):
    raise SystemExit("the LIV relationship is a merchandise licence, NOT a player deal")
for yr in ("2015", "2017"):
    if re.search(rf"founded in {yr}|since {yr}", _txt, re.I):
        raise SystemExit(f"founding year {yr} is one of three conflicting figures — hedge, do not pick")
# every quote on the page must carry an attribution span
_q = body.count("&ldquo;")
_att = body.count('class="pull-quote-attr">&mdash; Frankie Kimpton')
if _att < 3:
    raise SystemExit(f"only {_att} attributed pull-quotes; every quote needs a named source")
if "Zoe Kimpton" in _txt and re.search(r"Zoe (Kimpton )?(said|says|told|explains)", _txt):
    raise SystemExit("there is no published quote from Zoe Kimpton anywhere — do not invent one")
if body.count('<details class="faq-q">') != len(FAQ_ITEMS):
    raise SystemExit('FAQ must use <details class="faq-q"><summary> markup')
if AUSSIE in body:
    raise SystemExit("do not link the Australian roundup as the profile — this page replaces it")

open(f"drops/{SLUG}.html", "w", encoding="utf-8").write(head + body + tail)
print(f"wrote drops/{SLUG}.html | {len(SECTIONS)} sections | {N} pieces | "
      f"~{len(re.sub(r'<[^>]+>', ' ', head+body+tail).split())} words")
