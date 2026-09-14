#!/usr/bin/env python3
"""The Alignment Stick Edit — twelve hand-painted wooden pairs (2026-09-14).

Lenny asked for "12 alignment sticks for better practice" with Thwack Sporting
Co. as one. The 18-grid had fiberglass and carbon in it; he cut the mass-market
tube sets ("I like the wooden ones that are hand painted"), so the post became
an all-wood edit: nine American hickory makers, one walnut, two ash (Scotland,
Sweden). Data + verbatim copy in research/alignment/final.json; every fact on a
card comes from the maker's own page and is recorded there with its source.

Facts we deliberately do NOT assert: stick lengths for Nor'easter, Ekorre and
the Hazy LE (unstated); a place of manufacture for Gamut (unstated); anything
about BubbaWhips' dimensions beyond what Golf.com printed in 2018 (the maker
page carries no specs). Prices in GBP/SEK stay in their currency with a
rough USD in the text.

Quotes: Erik Heltne (Golf.com), Al of ScotSticks and Sebastián Mateu of Ekorre
are verbatim from the sources in final.json. The Thwack and Hazy founders are
unnamed on their sites, so their first-person lines are attributed to "the
founder" and quoted verbatim.

House FAQ markup is <details class="faq-q"><summary>Q</summary><p>A</p></details>.
"""
import re, os, json

SLUG  = "the-alignment-stick-edit"
TITLE = "The Alignment Stick Edit &mdash; Twelve Hand-Painted Pairs for Better Practice, in Hickory, Ash and Walnut"
PLAIN = "The Alignment Stick Edit — Twelve Hand-Painted Pairs for Better Practice, in Hickory, Ash and Walnut"
DESC  = ("Twelve wooden alignment sticks from small makers in West Virginia, Minnesota, New York, North Dakota, "
         "Florida, Scotland and Sweden, from $55 to about $255, plus the three drills that make a pair earn its place in the bag.")
IMG = "/images/alignment/"
F = json.load(open("research/alignment/final.json", encoding="utf-8"))

# slug -> (brand, display name, price text, copy)
P = {
 "thwack": ("Thwack Sporting Co.", "Pioneer Series &mdash; Pair", "$109",
  "American hickory wrapped by hand in Crawford waxed Irish linen thread &mdash; one stick with an accent wrap, one with a solid nine-inch band &mdash; in four colourways named for West Virginia places: New River, Spruce Knob, Cranberry Glades, Blackwater. The founder writes that the idea came home from a Fried Egg Golf trip, and that the name is &ldquo;the unmistakable sound of a well-struck shot.&rdquo; Forty-two inches, made in small batches in West Virginia, up to fourteen days to build, US shipping only. A $139 &ldquo;Pick Your Own Hickory Switch&rdquo; version lets you choose the blank."),
 "bubbawhips": ("BubbaWhips USA", "2-Color Custom Builder", "$99",
  "The company that put hickory alignment sticks in tour bags. Erik Heltne started BubbaWhips in the Minnesota winter of 2017 &mdash; Bubba and Whip are his sons&rsquo; nicknames &mdash; and by that autumn the sticks were at the Ryder Cup. The builder lets you pick a base colour and ring colours on genuine hickory, hand painted and finished in Minnesota with a weather-sealed matte coat and silver nail caps; three- and four-colour builds start at $120, engraving is $25. Visually, the site says, they are inspired by archery arrows."),
 "scotchskins": ("Scotch &amp; Skins", "Sawgrass Hickory Sticks", "$75",
  "Grade A Appalachian hickory from Atlas Dowel &amp; Wood in Ohio, stained green with white bands, sealed in beeswax and finished with bronze end caps and a laser-engraved wordmark. Forty-two inches, handcrafted in the USA. Scotch &amp; Skins is a glove company first &mdash; founders Adam and Brice describe themselves as &ldquo;lifelong golfers who simply wanted more out of our gloves&rdquo; &mdash; and the sticks carry the same leather-and-brass sensibility. The matching leather cover is sold out."),
 "gamut": ("Gamut Golf", "GG Sticks V3", "$98",
  "From the workshop that cuts headcovers out of vintage jerseys: American-grown hickory milled to a square profile rather than a dowel, with six inches of taper at each end, a blue stain, a white-and-blue striped band and an engraved wordmark. Forty-two inches by three-eighths. Gamut&rsquo;s line is &ldquo;built to last, made to age&rdquo; &mdash; the hickory darkens and marks with use. The V4, Lone Wolf, Shibori and Otey editions have all sold through; V3 is the one in stock."),
 "noreaster": ("Nor&rsquo;easter Sticks", "ACK-ley", "$99",
  "Navy base, &ldquo;Nantucket Red&rdquo; outline, and laser etching included in the price &mdash; the ACK-ley is the non-custom pair from a New England maker whose whole catalogue is otherwise built to order in your colours. Premium hickory, bare ends, three-to-four-week turnaround. Note the timing: the shop is closed 20 September to 10 October, and anything ordered in that window ships mid-October."),
 "hazy": ("Hazy Golf &times; Sun Mountain", "Limited Edition &mdash; 1 of 50", "$130",
  "A run of fifty numbered pairs made with Sun Mountain to mark its Hometown USA bag and the 250th anniversary: hickory painted red, white and navy under a gloss coat, brass end caps, engraved and numbered. Hazy is a Newburgh, New York workshop named for the founder&rsquo;s daughters Hazel and Georgia; his origin line is &ldquo;So I went into the workshop and made my own alignment sticks. Those first sticks eventually became Hazy.&rdquo; The core line, The Brook, is $99 at 43 inches with nickel or brass caps."),
 "clutch": ("Clutch Golf Company", "Hickory Sticks &mdash; Midnight Fairway", "$54.99",
  "The cheapest hickory pair here and the one with the most personality in its copy &mdash; &ldquo;the kind your grandpa might&rsquo;ve used to build a barn and break par.&rdquo; Real hickory at 42 inches, painted black and navy with white bands, engraved, handmade in the USA. Blue Devil is the other colourway in stock. Clutch&rsquo;s founding line is the whole small-maker story in one sentence: if you can&rsquo;t find the gear you want, make it yourself."),
 "hickoryheath": ("Hickory &amp; Heath", "Custom Alignment Sticks", "$75",
  "A family-owned shop that cuts, stains and paints premier hickory to your spec: a main colour, a secondary colour, one of five stripe designs, and optional engraving on one stick with the maker&rsquo;s name on the other. Forty-three inches, which the shop chose so the sticks sit below most woods in the bag with the ends protected. Ten to fourteen business days, no returns on custom work. &ldquo;No plastic. No fiberglass.&rdquo;"),
 "beavertail": ("Beavertail Golf Co.", "The Beaversticks", "$72.22",
  "Hunter Myran hand paints hickory in Dickinson, North Dakota, in six stock designs &mdash; The Cotton Candy, The OG, The Natural, The Frat Boy, The Jordan, The Collegiate &mdash; plus a $82.22 custom, with a name or phrase on both ends of each stick at no charge and silver or black tack caps. Made to order in about a week, shipped for $8.99, and sold through Etsy, where the listing reads &ldquo;every pair is crafted from hand start to finish.&rdquo; Founded 2024."),
 "outwest": ("Out West Atelier", "Painted Walnut Sticks", "$69.99",
  "The only walnut on the list. Out West Atelier builds small-batch hardwood goods in Panama City Beach, Florida, and its sticks are solid black walnut &mdash; noticeably heavier in the hand than hickory &mdash; with a single painted centre band in white or red, a low-VOC protective finish and the shop&rsquo;s desert-landscape mark. Forty-two inches, made to order in a week, US only, and the shipping is $32.50, so read the total before you fall for the wood. A cypress version exists."),
 "scotsticks": ("ScotSticks", "Anniversary 6", "&pound;51 &middot; about $68",
  "Made in Scotland from ash, which the shop points out was golf&rsquo;s original shaft wood before hickory arrived from America. The sixth-anniversary edition is a yellow base with green and red accents &mdash; &ldquo;yellow sun, green turf and seeing red when the snap hooks begin&rdquo; &mdash; at 45 inches by three-eighths, with chamfered ends instead of caps. The maker, Al, has a PhD in golf-ball design funded by The R&amp;A. Made to order, three-week lead, ships worldwide with duties on you."),
 "ekorre": ("Ekorre Golf", "Alignment Sticks &mdash; Three Stripes", "2,400 kr &middot; about $255",
  "Built the way a split-cane fly rod is built: six matched sections of Swedish ash glued into a hexagonal rod, which gives the stick what the maker calls a &ldquo;memory&rdquo; &mdash; it flexes and returns straight rather than taking a set. Sebastián Mateu, a cabinetmaker who caddied in Chile as a boy, developed it as his thesis at Malmstens in Stockholm on the elasticity of wood, and makes them at his workshop in Sigtuna. Three painted stripes, 80 to 85 grams a stick, custom colours for 200 kr, and import duty outside the EU is yours."),
}
HICKORY = ["thwack", "bubbawhips", "scotchskins", "gamut", "noreaster", "hazy", "clutch", "hickoryheath", "beavertail"]
OTHER   = ["outwest", "scotsticks", "ekorre"]
assert set(HICKORY + OTHER) == set(P) == {k for k in F if k != "_meta"}

def frames(s):
    n = 0
    while os.path.exists(f"images/alignment/{s}-{n+1}.jpg"): n += 1
    assert n, s
    return n

def gal(s, name):
    n = frames(s)
    pl = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>|&[a-z]+;|&#\d+;', '', name)).strip()
    if n == 1:
        return (f'<div class="product-gallery"><div class="pg-track"><div class="pg-frame">'
                f'<img src="{IMG}{s}-1.jpg" alt="{pl}" loading="lazy" /></div></div></div>')
    fr = "".join(f'<div class="pg-frame"><img src="{IMG}{s}-{i+1}.jpg" '
                 f'alt="{pl} &middot; view {i+1} of {n}" loading="lazy" /></div>' for i in range(n))
    dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" '
                   f'aria-label="View image {i+1}"></button>' for i in range(n))
    return (f'<div class="product-gallery"><div class="pg-track">{fr}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>')

def card(s):
    brand, nm, price, desc = P[s]
    return f"""<div class="product-card" data-frames="{frames(s)}">
      {gal(s, brand + " " + nm)}
      <div class="product-body">
        <div class="product-brand">{brand}</div>
        <div class="product-name">{nm} &middot; {price}</div>
        <div class="product-desc">{desc}</div>
        <a href="{F[s]['url']}" target="_blank" rel="noopener" class="product-link">Shop ↗</a>
      </div>
    </div>"""

def sec(hdr, kicker, items):
    c = "\n    ".join(card(x) for x in items)
    return (f'<section class="products">\n  <h2 class="products-hdr">{hdr}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'  <div class="products-grid">\n    {c}\n  </div>\n</section>\n')

INTRO = """<div class="writeup">
  <div class="writeup-body">
    <p>This is twelve pairs of alignment sticks, every one of them wood, every one painted or wrapped by hand, from a dozen small shops in West Virginia, Minnesota, New York, North Dakota, Florida, Scotland and Sweden. Prices run from $54.99 to about $255 and everything was in stock on 14 September 2026.</p>
    <p>The alignment stick used to be the one piece of golf equipment nobody designed. You bought two orange fiberglass rods at a hardware store, or a pair with a tube from the pro shop, and they rattled in the bag for a decade. Somewhere around 2017 a few people started turning hickory &mdash; the wood golf shafts were made of before steel &mdash; painting bands on it and selling pairs, and the thing became a small craft category almost overnight. What you get for the money is a stick that looks like it belongs next to the clubs and ages the way a club does. On the range it draws the same line the orange ones did.</p>
    <p>Who it is for: the range regular who has a pair already and is tired of looking at them, and anyone whose practice needs a reason to start.</p>
  </div>
</div>
"""

WHY = """<section class="products">
  <h2 class="products-hdr">Wood, and Which Wood</h2>
  <p class="cat-kicker">Hickory is the default. Ash is the original. Walnut is the outlier.</p>
  <div class="writeup-body">
    <p><strong>Hickory.</strong> Nine of the twelve. It was the shaft wood of golf&rsquo;s first two centuries because it is hard, straight-grained and springy, and the makers here mostly buy it as dowel &mdash; Scotch &amp; Skins names its supplier, Atlas Dowel &amp; Wood in Ohio &mdash; then stain, paint, seal and cap it. It weathers: Gamut says the hickory &ldquo;develops its own character,&rdquo; and that is the point.</p>
    <p><strong>Ash.</strong> ScotSticks makes the case that ash was golf&rsquo;s original wood before hickory crossed from America, and cuts its sticks from it in Scotland. Ekorre goes further and laminates six strips of Swedish ash into a hexagon, the way a split-cane fishing rod is made, so the stick flexes and returns straight.</p>
    <p><strong>Walnut.</strong> Out West Atelier&rsquo;s black walnut is denser and darker than either, and heavier in the hand. Nobody else here uses it.</p>
    <p><strong>The details that differ.</strong> Length runs 42 to 45 inches; Hickory &amp; Heath picked 43 so the sticks sit below the woods in the bag. Ends are either capped &mdash; bronze at Scotch &amp; Skins, brass at Hazy, tack caps at Beavertail, nail caps at BubbaWhips &mdash; or bare and chamfered, as ScotSticks and Ekorre prefer. Almost everyone engraves, and about half will paint your colours to order.</p>
  </div>
</section>
"""

DRILLS = """<section class="products">
  <h2 class="products-hdr">Three Drills That Justify the Pair</h2>
  <p class="cat-kicker">A stick in the bag is decoration until it goes on the ground. These are the three uses that come up in every lesson.</p>
  <div class="writeup-body">
    <p><strong>The railroad track.</strong> One stick on the target line just outside the ball, the second parallel to it along your toes. It is the only honest check on where you are actually aimed, because the eye lies about it from address, and most amateurs who think they aim square are closed. Hit a bucket this way before every round and the first tee stops being a surprise.</p>
    <p><strong>Ball position.</strong> Lay one stick along the toe line and the other perpendicular to it, pointing at the ball. Move the second stick as the club changes &mdash; forward for the driver, centred for wedges &mdash; and you build the memory of where the ball sits for each. This is the drill the range mats quietly ruin, because the mat has a line and the course does not.</p>
    <p><strong>The gate.</strong> Push both sticks into the turf a clubhead-and-a-half apart, just outside the ball, and swing through the gap. It punishes an over-the-top move and an early release with a clatter you cannot ignore, which is why the wooden ones matter here: hickory on titanium sounds worse than fiberglass does, and you will stop doing it sooner.</p>
  </div>
</section>
"""

FAQ_ITEMS = [
 ("Are wooden alignment sticks as straight as fiberglass ones?",
  "The makers here select straight-grained hickory, ash or walnut and most seal it against moisture; Ekorre laminates six strips of ash into a hexagon specifically so the stick returns to straight after flexing. Wood will always move a little more than a fiberglass rod, which is why several shops advise keeping the sticks out of a wet bag."),
 ("What length should an alignment stick be?",
  "The twelve here run 42 to 45 inches. Longer reads better on the ground; shorter fits below the headcovers in a stand bag, which is why Hickory & Heath cuts to 43 inches. Any of them works for the railroad-track and ball-position drills."),
 ("Do these come with a cover or tube?",
  "No. Every pair in this edit ships bare; the tube-and-rods sets are the fiberglass ones from Tour Sticks, SuperStroke and the big brands. Scotch & Skins makes a matching leather cover but it is sold out, and Hazy sells a see-through leather cover for $60."),
 ("Which one is the original hickory alignment stick?",
  "BubbaWhips, started by Erik Heltne in Minnesota in 2017. Golf.com reported that the sticks were in tour players' bags at that year's Ryder Cup within months of launch."),
 ("Which of these can I customise?",
  "BubbaWhips (builder), Hickory & Heath (colours, stripe design, engraving), Beavertail (custom design plus free names), Nor'easter (its main line is fully custom; the ACK-ley is the stock pair), Thwack (Pick Your Own Hickory Switch, $139), Out West (engraving) and Ekorre (custom colours and a name for a fee)."),
 ("Why are the Scottish and Swedish ones priced in pounds and kronor?",
  "Because they are made and sold from there. ScotSticks lists at &pound;51 and ships worldwide with a three-week lead; Ekorre lists at 2,400 kr from Sigtuna. Both note that import duties outside their region are paid by the buyer, so the dollar figures in this post are approximate."),
]
FAQ = """<section class="products">
  <h2 class="products-hdr" id="faq">The Questions</h2>
  <div class="faq">
""" + "\n".join(f'    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>'
                for q, a in FAQ_ITEMS) + """
  </div>
</section>
"""

QUOTE = """<section class="products">
  <h2 class="products-hdr">The One That Started It</h2>
  <p class="cat-kicker">Erik Heltne on the hardware-store rods everybody used before, from Golf.com&rsquo;s 2018 story on BubbaWhips.</p>
<div class="pull-quote">
  <div class="pull-quote-inner">&ldquo;Most golfers, myself included, went to Home Depot and fashioned the goofy bright orange and bright yellow alignment sticks as training aids.&rdquo;<span class="pull-quote-attr">&mdash; Erik Heltne, BubbaWhips founder &middot; Golf.com</span></div>
</div>
</section>
"""

def st(s):
    return (re.sub(r'<[^>]+>', '', s).replace("&ldquo;", '"').replace("&rdquo;", '"')
            .replace("&rsquo;", "'").replace("&amp;", "&").replace("&mdash;", "—")
            .replace("&middot;", "·").replace("&pound;", "£").replace("&times;", "×"))

SCHEMA = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": st(q), "acceptedAnswer": {"@type": "Answer", "text": st(a)}} for q, a in FAQ_ITEMS]}

model = open("drops/brand-to-know-gamut-golf.html", encoding="utf-8").read()
head = model[:model.find('<div class="breadcrumb">')]
tail = model[model.find('<section class="more"'):]
head = re.sub(r'<title>[^<]*</title>', f'<title>{PLAIN} — The Grassy Issue</title>', head)
for k, v in [("description", DESC), ("og:title", PLAIN), ("og:description", DESC)]:
    head = re.sub(rf'(<meta (?:name|property)="{re.escape(k)}" content=")[^"]*(")', lambda m: m.group(1) + v + m.group(2), head)
head = re.sub(r'(<link rel="canonical" href=")[^"]*(")', lambda m: m.group(1) + f"https://thegrassyissue.com/drops/{SLUG}" + m.group(2), head)
head = re.sub(r'(<meta property="og:url" content=")[^"]*(")', lambda m: m.group(1) + f"https://thegrassyissue.com/drops/{SLUG}" + m.group(2), head)
head = re.sub(r'(<meta property="og:image" content=")[^"]*(")', lambda m: m.group(1) + "https://thegrassyissue.com/images/alignment/hero.jpg" + m.group(2), head)
head = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: '<script type="application/ld+json">' + json.dumps(SCHEMA) + '</script>', head, flags=re.S)

body = ('<div class="breadcrumb">\n  <a href="/">Feed</a><span>/</span>\n'
        '  <a href="/#feed">Drops &amp; Brands</a><span>/</span>\n  The Alignment Stick Edit</div>\n'
        f'<header class="drop-header">\n  <h1>{TITLE}</h1>\n  <div class="drop-meta">\n'
        '    <span>September 14, 2026</span><span class="dot"></span>\n'
        '    <span>Drops &amp; Brands</span><span class="dot"></span>\n'
        '    <span>12 Pairs &middot; 12 Makers</span>\n  </div>\n</header>\n\n'
        '<div class="drop-hero"><div class="drop-hero-img"><img src="/images/alignment/hero.jpg" '
        'alt="A golf bag with wooden alignment sticks against a cabinetmaker&rsquo;s bench in the Ekorre Golf workshop, Sigtuna, Sweden" /></div></div>\n'
        + INTRO + WHY
        + sec("American Hickory &mdash; Nine Makers",
              "From the original in Minnesota to a first run out of West Virginia, listed by the story rather than the price.", HICKORY)
        + QUOTE
        + sec("Ash and Walnut &mdash; Three More",
              "The original shaft wood, cut in Scotland and laminated in Sweden, and the one walnut pair in the category.", OTHER)
        + DRILLS + FAQ)

out = head + body + tail
assert not re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", body), re.I), "banned word"
open(f"drops/{SLUG}.html", "w", encoding="utf-8").write(out)
print(f"wrote drops/{SLUG}.html | {len(P)} products | ~{len(re.sub(r'<[^>]+>', ' ', out).split())} words")
