#!/usr/bin/env python3
"""Rebuild — Accessories, On and Off the Course (same slug, 17 Sept 2026).

WHY THE REBUILD
---------------
The original ran 553 words, six flat cards, one image each, no FAQ, no schema.
Auditing its links found two broken:

  * Sentinel "Basecamp Water Bottle $68" pointed at
    /shop/p/no-16-basket-galvanized-76zkc-nctfn-cx85f — a galvanized basket.
    Sentinel runs Squarespace and REUSES SLUG STEMS across products, so a stale
    URL silently becomes a different item. Every Sentinel URL in this file was
    re-read off the live shop on 17 Sept 2026 for that reason. No bottle by that
    name exists in the current range.
  * Depeche Golf "Issue #4" pointed at the bare homepage.

Of the original six, two survive on merit (Dimple & Divot's Murphy brush, now
$50 not $45; Walker's marker 3-pack, now $39.95 not $35), Jones survives on a
different object (the Ranger Cooler is gone), and Mogshade's Estate Headcover is
discontinued. Same slug — the URL does not change, so no redirect is needed and
the existing links and rankings carry over.

THE STRUCTURE IS THE PREMISE
----------------------------
Lenny kept the on/off-course split and asked for it as the page's actual shape
rather than a line in the intro. Three sections, in order: On the Course (8),
Either Way (7), Off the Course (4). Nineteen products, ONE PER BRAND, which is
the house no-repeat rule and also what makes the three-way grouping legible —
no brand appears in two sections arguing with itself.

PRICES: every one read off the brand's own store on 17 September 2026, and every
product was in stock at the time of reading. Nothing here is converted from
another currency; all nineteen list in USD on their own sites.

THE FORDEN TIN: Lenny cleared saying plainly what it is (a nicotine-pouch tin —
Forden's own copy names ZYN, Rogue and VELO). The card says so. Do not soften it
into "pocket tin" — being coy about it by accident was the thing he ruled out.

IMAGE NOTE: Fyfe publishes exactly one frame for the Fescue pouch, so its card
is single-frame by design. gal() handles n == 1 without emitting arrows or dots,
which is what keeps verify-post.py's frame/dot check passing.

Deliberately NOT asserted (no source):
  - country of manufacture for anything that does not state one
  - that the Kaweco is made for golf (Kaweco has made pocket pens since 1883;
    Sentinel stocks it, which is a different claim)
  - durability, longevity or performance claims beyond each product page's own
  - any comparison that ranks one maker above another
"""
import re, os, json

SLUG  = "accessories-on-and-off-the-course"
PLAIN = "The Accessory Edit — 19 Small Things, On Course and Off"
TITLE = "The Accessory Edit &mdash; 19 Small Things, On Course and Off"
DESC  = ("Nineteen accessories from nineteen independent brands, grouped by where they actually live: "
         "in the bag, in both places, or nowhere near a fairway. Prices read live, 17 September 2026.")
IMG   = "/images/accessories/"
DATE  = "September 17, 2026"

# ---------------------------------------------------------------- the lineup
# (img slug, brand, product name, price, shop URL, copy)
ON = [
 ("dimple", "Dimple &amp; Divot", "Hickory Golf Brush &mdash; Murphy", "50",
  "https://dimpleanddivot.com/products/hickory-golf-brush-murphy",
  "The brush Dimple &amp; Divot started with, and still the one the rest of its range is built from. It "
  "lists at $50 now, up from $45 a year ago. The handle is American hickory, cut a little "
  "longer than the category standard so there is something to hold rather than something to pinch, and "
  "the bristles are firm nylon, which is the choice that lets it sit against a towel without snagging it. "
  "It comes off the bag on a nickel trigger snap. Dimple &amp; Divot handcrafts them in the United States."),
 ("grooveit", "Grooveit", "The Wet Club Scrub", "24.99",
  "https://grooveitbrush.com/products/grooveit-the-wet-club-scrub",
  "The other way to solve the same problem. The handle is a reservoir: fill it, press the pump, and the "
  "water comes through the bristles while you scrub, so a face caked with Bermuda comes clean without a "
  "trip to the ball washer. It attaches by magnet rather than clip &mdash; no cord, nothing to unhook &mdash; "
  "and Grooveit backs it for three years. At $24.99 it is the cheapest thing in this section and the most "
  "obviously useful."),
 ("seamus", "Seamus Golf", "Hand Forged&reg; Greenskeeper Pitch Tool &mdash; Steel", "76",
  "https://www.seamusgolf.com/products/hand-forged-greenskeeper-pitch-tool-steel",
  "Not a fork. One end is a three-eighths-inch aerification tyne, the other is a three-quarter-inch tip "
  "closer to a nail, and between them sits a rounded face for tamping the surface flat afterwards. Seamus "
  "says it copied the shape from a tool it saw greenkeepers in Monterey using, and worked with a "
  "second-generation blacksmith to reproduce it. Each one is forged by hand, so the hammer marks land "
  "differently on every face."),
 ("gamut", "Gamut Golf", "GG Alignment Sticks V5", "98",
  "https://gamutgolf.com/products/gg-alignment-sticks-v5",
  "Alignment sticks are usually fibreglass driveway markers with a logo on them. These are American-grown "
  "hickory, cut to a square profile rather than a round one, and finished with waxed whipping at the "
  "collar &mdash; the same thread wrap that held hickory shafts together before steel. Gamut says the wood "
  "takes on its own marks with use, which is the argument for buying wooden ones at all. The second "
  "hickory object on this page, and not by accident: it is the material the game was built out of."),
 ("malbon", "Malbon Golf", "Baldwin Buckets Ball Marker", "34",
  "https://www.malbongolf.com/products/baldwin-buckets-ball-marker-green",
  "Stainless steel, an inch across, with the Buckets logo printed in enamel on the face and the M script "
  "debossed into the back. Malbon runs the Buckets mark across a lot of things; on a marker it works "
  "because the whole job of a marker is to be recognisable from putting distance and yours rather than "
  "somebody else&rsquo;s."),
 ("walker", "Walker Golf Things", "Ball Marker Crest 3-Pack", "39.95",
  "https://www.walkergolfthings.com/products/crest-3-pack",
  "Now $39.95, up from $35 a year ago. Three markers rather than one &mdash; the Kooka, "
  "the bottle cap and the new Crest &mdash; in black, green and brushed gold. They are 2.8mm thick with "
  "enamel embossed faces, which is heavier than the stamped tin most markers are, and the practical point "
  "of buying three is that you will lose one."),
 ("radry", "Radry Golf", "The Animals Got Out Again Towel", "45",
  "https://radry.com/products/the-animals-got-out-again-towel",
  "Sixteen by thirty-eight inches of cotton jacquard at 550gsm, which is the middle weight &mdash; heavy "
  "enough to dry a face properly, light enough that it is not still wet on the ninth. There is no hole and "
  "no clip: it is cut as a caddie towel, meant to fold over the top of the clubs and stay there. The animal "
  "motif is woven in rather than printed on, so it reads on both sides."),
 ("devereux", "Devereux Golf", "Skull Caddie Knitted Towel &mdash; Black/White", "38",
  "https://devereuxgolf.com/products/skull-caddie-knitted-towel-black-white",
  "Cotton French terry, knitted rather than woven, which is the softer hand of the two and the reason it "
  "will not scuff a face while you are cleaning it. Same drape-over-the-bag construction as the Radry, same "
  "logic. The skull is Devereux&rsquo;s house motif and it is the loudest thing in this section by some "
  "margin."),
]

BOTH = [
 ("fella", "Fella Golf", "Pizza Slice Double Ball Marker", "15",
  "https://fellagolf.com/products/pizza-slice-double-ball-marker",
  "Three centimetres across, double-sided: a golden slice of pizza on one face under the line <em>It only "
  "takes one good shot</em>, the Fella logo on the other. It belongs in both columns because a ball marker "
  "spends most of its life in a pocket with keys and coins, and this is the one in there that makes a "
  "stranger ask about it. Fifteen dollars."),
 ("sentinel", "Sentinel Golf", "Kaweco Mini Special", "42",
  "https://www.sentinelgolf.us/shop/p/no-16-basket-galvanized-76zkc-bj2ct",
  "A German pocket pencil that Sentinel stocks alongside its own Dyneema bags, and the most quietly useful "
  "thing in this edit. It is short enough to live in a scorecard holder and machined solidly enough that it "
  "does not care about being in there; the same object writes a grocery list on Tuesday. One housekeeping "
  "note, because it caught us out: Sentinel&rsquo;s shop reuses URL stems between products, so the link "
  "here was re-read off the live listing rather than trusted from memory."),
 ("fyfe", "Fyfe Golf", "Fescue Harris Tweed Drawstring Leather Pouch", "48",
  "https://www.fyfegolf.com/products/fescue-harris-tweed-drawstring-leather-pouch",
  "Harris Tweed herringbone in green and yellow, closed with a leather drawstring and lined inside with "
  "cream fleece &mdash; which is what makes it a valuables pouch rather than a tee bag, because the lining "
  "is the part that stops a watch face getting scratched by a ball. Fyfe hand-makes them in Scotland. Works "
  "equally as the thing you empty your pockets into at the end of the day."),
 ("bluegrass", "Bluegrass Fairway", "Horween Leather Scorecard Holder &mdash; Vintage Bourbon", "85",
  "https://www.bluegrassfairway.com/products/leather-minimalist-golf-scorecard-holder-in-vintage-bourbon",
  "The object in the photograph at the top of this page. Full-grain leather sourced in the United States, "
  "6.75 by 8 inches opened, cut minimal enough that it slides into a back pocket rather than bulging out of "
  "one. Bluegrass Fairway makes them in Louisville and will heat-stamp initials inside if you ask at "
  "checkout. Leather this weight goes lighter where your thumb sits, which is the whole argument for it."),
 ("mogshade", "Mogshade", "Ocean Bottle &times; Mogshade", "59",
  "https://mogshadegolf.com/products/ocean-bottle-x-mogshade",
  "Ninety per cent recycled stainless, double-walled and vacuum insulated, rated by Mogshade for six hours "
  "hot and eighteen cold, and dishwasher safe, which is rarer in this category than it should be. The "
  "engraving is by the artist Fiumani, from Mogshade&rsquo;s Course Flip collection. A bottle is the "
  "clearest case of an object that has to work in a cart holder and on a desk without changing."),
 ("huega", "Huega House", "Squeeze Water Bottle &mdash; Black", "15",
  "https://huegahouse.com/products/huega-squeeze-water-bottle-black",
  "The opposite answer at a quarter of the price. Five hundred and fifty millilitres of flexible "
  "food-grade plastic with an easy-flow spout, BPA free, designed to be squeezed one-handed while you are "
  "moving. No insulation, no ceremony. It is the bottle for a hot Austin nine when you do not want to carry "
  "anything you would be annoyed to leave behind."),
 ("forden", "Forden Golf", "Black Forden Tin", "25",
  "https://www.fordengolf.com/products/forden-golf-aluminem-alloy-pouch-can",
  "A metal tin for nicotine pouches &mdash; Forden names ZYN, Rogue and VELO on the listing. Two "
  "compartments, one for fresh and one for used, which is the actual design problem it solves and the "
  "reason the alternative is a used pouch in a cup holder for eighteen holes. Included here because it is "
  "a well-made everyday-carry object and a lot of golfers use one; if that is not you, it is not for you."),
]

OFF = [
 ("jones", "Jones Sports Co", "Dopp Kit &mdash; Evergreen", "65",
  "https://www.jonessportsco.com/products/dopp-kit-evergreen",
  "Jones was in the original version of this edit with the Ranger Cooler, which is no longer made. This is "
  "the replacement and it is a better fit for the section: a full-length zip into the main compartment, a "
  "second zip pocket on the outside for the things you reach for first, and webbing grab handles on a "
  "structure that stands up on a hotel counter instead of slumping. Evergreen is the pick of the colours."),
 ("ssc", "Sugarloaf Social Club", "Hidden Gem Crazy Creek Chair", "75",
  "https://sugarloafsocialclub.com/products/hidden-gem-crazy-creek-chair",
  "Crazy Creek has been making this folding ground chair for decades and it is a fixture at trailheads and "
  "on beaches; Sugarloaf put its Hidden Gem colourway on it. Sixteen and a half inches of seat height, "
  "around a pound and a half, rated to 250 pounds. It is here because it is the clearest example of the "
  "thing this edit is about &mdash; an object from outside golf that a golf brand recognised."),
 ("apres", "Apr&egrave;s Golf", "Apr&egrave;s-Golf Pencils Poster Art, 11&times;14", "34",
  "https://apresgolf.com/products/apres-golf-pencils-poster-art-11x14",
  "A print of golf pencils on matte photo paper, eleven by fourteen, unframed and individually numbered. "
  "Not equipment at all, which is the point of putting it in a list of accessories: the version of this "
  "hobby that shows up at home is usually a framed scorecard or nothing, and a $34 numbered print is a "
  "third option."),
 ("birds", "Birds of Condor", "Flush Puppy Wallet", "19.95",
  "https://birdsofcondor.com/products/flush-puppy-tie-dye-golf-swing-wallet",
  "Cut from a single piece of material with no stitching, which is how it gets to one ounce and three "
  "sixteenths of an inch thick. A bifold sized for notes in six currencies and two pockets that Birds of "
  "Condor rates at eight-plus cards. Vegan and recyclable, per the brand. Under twenty dollars, and it is "
  "the item on this page you would carry every day without thinking about golf once."),
]

ALL = ON + BOTH + OFF

# ------------------------------------------------------------------- guards
_seen_brand, _seen_img = set(), set()
for s, b, n, p, u, c in ALL:
    if b in _seen_brand:
        raise SystemExit(f"brand appears twice: {b} — one product per brand is the rule")
    _seen_brand.add(b)
    if s in _seen_img:
        raise SystemExit(f"image slug used twice: {s}")
    _seen_img.add(s)
    if not os.path.exists(f"images/accessories/{s}.jpg"):
        raise SystemExit(f"lead frame missing on disk: images/accessories/{s}.jpg")
    if not u.startswith("https://"):
        raise SystemExit(f"{b}: shop link is not https")
if not os.path.exists("images/accessories/hero.jpg"):
    raise SystemExit("hero.jpg missing")

def frames(s):
    n = 1
    while os.path.exists(f"images/accessories/{s}-a{n+1}.jpg"):
        n += 1
    return n

def gal(s, name):
    n = frames(s)
    # collapse whitespace AFTER stripping entities, or "Fyfe &mdash; Pouch"
    # leaves a double space in the alt where the dash was
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

def card(x):
    s, brand, name, price, url, copy = x
    pr = f"${price}"
    return f"""<div class="product-card" data-frames="{frames(s)}">
      {gal(s, f"{brand} {name}")}
      <div class="product-body">
        <div class="product-brand">{brand}</div>
        <div class="product-name">{name} &middot; {pr}</div>
        <div class="product-desc">{copy}</div>
        <a href="{url}" target="_blank" rel="noopener" class="product-link">Shop ↗</a>
      </div>
    </div>"""

def sec(hdr, kicker, items):
    c = "\n    ".join(card(x) for x in items)
    return (f'<section class="products">\n  <h2 class="products-hdr">{hdr}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'  <div class="products-grid">\n    {c}\n  </div>\n</section>\n')

INTRO = """<div class="writeup">
  <div class="writeup-body">
    <p>This is nineteen accessories from nineteen different brands, organised not by price or by maker but by where each one actually lives.</p>
    <p>Some of this stuff only makes sense on a golf course. A pitch repair tool has one job and it is a job that exists nowhere else. Some of it never goes near one &mdash; a dopp kit is a dopp kit. And then there is the middle group, which is the interesting one: objects that go out in a bag on Saturday and stay in a pocket, on a desk or on a kitchen counter for the rest of the week without looking like sports equipment that wandered indoors.</p>
    <p>That middle group is where independent golf brands have got noticeably better in the last few years, and it is why the page is split three ways rather than sorted by price. Everything below was checked on the brand&rsquo;s own store on 17 September 2026 and was in stock at the time of reading. One product per brand, so nobody is here twice.</p>
  </div>
</div>
"""

CRAFT = """<section class="products">
  <h2 class="products-hdr">What Separates the $15 Version From the $85 One</h2>
  <p class="cat-kicker">Four things do most of the work, and none of them is branding.</p>
  <div class="writeup-body">
    <p><strong>Material that changes.</strong> Hickory and full-grain leather both move under handling &mdash; they darken, they go lighter where a thumb sits, they take on the marks of whatever they have been through. Gamut&rsquo;s hickory sticks and Bluegrass Fairway&rsquo;s Horween holder both cost more than the moulded alternative and both look different after a season, which is either the whole appeal or completely beside the point depending on the buyer. Stainless and food-grade plastic do the opposite and stay exactly as they arrived.</p>
    <p><strong>Forged versus pressed.</strong> A forged piece is beaten into shape from solid stock; a pressed one is stamped out of sheet. It matters most on anything with a working edge. Seamus forges its pitch tool by hand and the tip holds its geometry rather than rolling over under load. On a ball marker, which does nothing but sit still, it matters a good deal less &mdash; though Walker&rsquo;s 2.8mm enamel-embossed discs still feel like objects rather than tokens.</p>
    <p><strong>Woven versus printed.</strong> On towels this is the entire difference. A jacquard weave &mdash; Radry&rsquo;s animals, Devereux&rsquo;s skull &mdash; puts the pattern into the cloth, so it reads on both faces and does not crack off after twenty washes the way a screen print does. Weight is the other variable: 550gsm is the middle, heavy enough to actually dry something and light enough to dry itself out before the back nine.</p>
    <p><strong>Lining, and other things you cannot see.</strong> The cream fleece inside Fyfe&rsquo;s tweed pouch is what makes it a valuables pouch instead of a tee bag. The second compartment in Forden&rsquo;s tin is the only reason to buy a tin. The reservoir in the handle of the Grooveit brush is the product. The cheapest way to tell a considered accessory from a merchandised one is to look for the part that solves a problem nobody mentions in the product title.</p>
  </div>
</section>
"""

PRICES = """<section class="products">
  <h2 class="products-hdr">A Note on Prices, Stock and Dead Links</h2>
  <p class="cat-kicker">Small-brand accessory lists go stale faster than almost anything else in golf.</p>
  <div class="writeup-body">
    <p>The earlier version of this page listed six accessories and, by September, two of its links no longer went where they said. One pointed at a product that had been discontinued and had its URL quietly inherited by something else entirely; another had decayed to a bare homepage. Two of the six had gone up in price. That is not unusual for a small-brand roundup left alone for a year &mdash; independent makers retire colourways, run out of a batch and move on &mdash; but it does mean a list like this is only as good as the last time somebody opened every link.</p>
    <p>So every price on this page was read off the brand&rsquo;s own store on 17 September 2026, and every item was buyable at the time of reading. Nothing has been converted from another currency; all nineteen list in dollars on their own sites. Two pieces from the original six earned their way back in &mdash; Dimple &amp; Divot&rsquo;s Murphy brush and Walker&rsquo;s marker three-pack &mdash; and both are listed at their current prices rather than the old ones.</p>
    <p>Small-batch accessories sell out. If something here is gone by the time you get to it, the maker almost certainly reruns it; none of these are numbered editions.</p>
  </div>
</section>
"""

FAQ_ITEMS = [
 ("What golf accessories actually work off the course too?",
  "The ones built around a function that is not specific to golf. A vacuum-insulated bottle, a leather scorecard holder sized like a wallet, a pocket pencil, a valuables pouch and a slim bifold all do the same job at a desk as they do in a bag. Anything shaped around a rule of golf — a pitch repair tool, a ball marker — does not travel, though a good marker does earn its place in a pocket."),
 ("How much should I spend on a golf towel?",
  "Between $38 and $45 buys a cotton jacquard caddie towel at around 550gsm, which is the useful middle weight. The thing to check is whether the pattern is woven in or printed on: a woven jacquard reads on both faces and survives washing, a screen print cracks. Both the Radry and the Devereux here are knitted or woven rather than printed."),
 ("Is a hand-forged pitch tool better than a cheap two-prong fork?",
  "The shape matters more than the price. A single prong or a bar is hard to misuse, because the natural motion is pushing turf inward from the edge of the mark — which is the correct repair. A two-prong fork invites you to straddle the mark and lever the centre up, which tears the roots still holding it together. Seamus's Greenskeeper is a single-point tool for that reason, with a rounded face on the same head for tamping the surface flat afterwards."),
 ("What is the difference between a golf brush with a water reservoir and a dry one?",
  "A dry brush needs a wet towel or a ball washer to be much use on a caked face. A reservoir brush like the Grooveit carries its own water and pumps it through the bristles, so it works anywhere on the course. The trade-off is that a dry hickory-handled brush like Dimple & Divot's is a simpler object with nothing to fail and nothing to refill."),
 ("Why do so many small golf brands sell pouches?",
  "Because a round creates a specific storage problem — keys, a watch, a wedding ring, tees, a marker — and nothing else in the bag solves it. The detail that separates a valuables pouch from a tee bag is the lining: a fleece or soft interior stops a watch face getting scratched. Fyfe's tweed pouch is lined in cream fleece; that is what the $48 is for."),
 ("Were all of these in stock when this was written?",
  "Yes. Every one of the nineteen was checked on the brand's own store on 17 September 2026 and every price on this page was read the same day. Small-batch accessories do sell out, and none of these are numbered limited editions, so makers generally rerun them."),
]

def st(s):
    return (re.sub(r'<[^>]+>', '', s).replace("&ldquo;", '"').replace("&rdquo;", '"')
            .replace("&rsquo;", "'").replace("&amp;", "&").replace("&mdash;", "—")
            .replace("&middot;", "·").replace("&reg;", "®").replace("&times;", "×")
            .replace("&egrave;", "è"))

# HOUSE FAQ MARKUP IS <details class="faq-q"><summary>. See the note in
# build-divot-tools.py: div.faq-q + div.faq-a fails twice over — verify-post.py
# flags faq-a as a class with no CSS rule, and apply-faq-style.py cannot see div
# markup so it appends a SECOND FAQ rendered from the schema.
FAQ = """<section class="products">
  <h2 class="products-hdr" id="faq">The Questions</h2>
  <div class="faq">
""" + "\n".join(f'    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>'
                for q, a in FAQ_ITEMS) + """
  </div>
</section>
"""

SCHEMA = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": st(q),
     "acceptedAnswer": {"@type": "Answer", "text": st(a)}} for q, a in FAQ_ITEMS]}

# ------------------------------------------------------------------ chassis
model = open("drops/7-divot-tools-actually-worth-carrying.html", encoding="utf-8").read()
head = model[:model.find('<div class="breadcrumb">')]
tail = model[model.find('<section class="more"'):]

head = re.sub(r'<title>[^<]*</title>', f'<title>{PLAIN} — The Grassy Issue</title>', head)
for k, attr in [("description", "name"), ("og:title", "property"), ("og:description", "property"),
                ("twitter:title", "name"), ("twitter:description", "name")]:
    v = PLAIN if k.endswith("title") else DESC
    head = re.sub(rf'(<meta {attr}="{re.escape(k)}" content=")[^"]*(")',
                  lambda m, _v=v: m.group(1) + _v + m.group(2), head)
for k, attr in [("canonical", None), ("og:url", "property")]:
    if k == "canonical":
        head = re.sub(r'(<link rel="canonical" href=")[^"]*(")',
                      lambda m: m.group(1) + f"https://thegrassyissue.com/drops/{SLUG}" + m.group(2), head)
    else:
        head = re.sub(r'(<meta property="og:url" content=")[^"]*(")',
                      lambda m: m.group(1) + f"https://thegrassyissue.com/drops/{SLUG}" + m.group(2), head)
for k, attr in [("og:image", "property"), ("twitter:image", "name")]:
    head = re.sub(rf'(<meta {attr}="{re.escape(k)}" content=")[^"]*(")',
                  lambda m: m.group(1) + f"https://thegrassyissue.com{IMG}hero.jpg" + m.group(2), head)
# lambda, not a literal: json.dumps output carries \u and \" that re.sub would
# read as escapes in a replacement string
_sb = '<script type="application/ld+json">' + json.dumps(SCHEMA) + '</script>'
head = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: _sb, head, flags=re.S)

body = ('<div class="breadcrumb">\n  <a href="/">Feed</a><span>/</span>\n'
        '  <a href="/#feed">Drops &amp; Brands</a><span>/</span>\n  The Accessory Edit</div>\n'
        f'<header class="drop-header">\n  <h1>{TITLE}</h1>\n  <div class="drop-meta">\n'
        f'    <span>{DATE}</span><span class="dot"></span>\n'
        '    <span>Drops &amp; Brands</span><span class="dot"></span>\n'
        f'    <span>{len(ALL)} Pieces &middot; {len(ALL)} Brands</span>\n  </div>\n</header>\n\n'
        f'<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}hero.jpg" '
        'alt="A brown leather golf scorecard holder being drawn out of a back pocket on a fairway" /></div></div>\n'
        + INTRO
        + sec(f"On the Course &mdash; {len(ON)} Pieces",
              "Each of these does one job, and it is a job that exists nowhere else.", ON)
        + CRAFT
        + sec(f"Either Way &mdash; {len(BOTH)} Pieces",
              "Goes out in the bag, stays in a pocket or on a desk the rest of the week.", BOTH)
        + sec(f"Off the Course &mdash; {len(OFF)} Pieces",
              "Never sees a fairway. Made by people who spend their lives on them.", OFF)
        + PRICES
        + FAQ)

out = head + body + tail
open(f"drops/{SLUG}.html", "w", encoding="utf-8").write(out)

# -------------------------------------------------------------- post-checks
import html as H
plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", H.unescape(body)))
words = len(re.findall(r"[A-Za-z0-9']+", plain))
problems = []
if re.search(r"\bworth\b", plain, re.I):
    problems.append("banned word 'worth' in the copy")
if words < 1200:
    problems.append(f"only {words} words (house minimum 1200)")
if out.count("<h1") != 1:
    problems.append(f"{out.count('<h1')} h1 tags")
if out.count('class="product-card"') != len(ALL):
    problems.append("card count does not match the lineup")
for s, *_ in ALL:
    for i in range(2, frames(s) + 1):
        if not os.path.exists(f"images/accessories/{s}-a{i}.jpg"):
            problems.append(f"{s}: frame {i} referenced but missing")
json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', out, re.S).group(1))
if problems:
    raise SystemExit("REFUSED:\n  " + "\n  ".join(problems))

print(f"wrote drops/{SLUG}.html")
print(f"  {len(ALL)} products / {len(_seen_brand)} brands  |  on {len(ON)} · both {len(BOTH)} · off {len(OFF)}")
print(f"  {words} words  |  {sum(frames(s) for s,*_ in ALL)} gallery frames  |  FAQ {len(FAQ_ITEMS)} Q&A + schema")
