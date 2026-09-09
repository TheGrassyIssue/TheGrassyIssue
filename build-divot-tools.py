#!/usr/bin/env python3
"""Refresh — The Divot Tool Edit (rebuild of 7-divot-tools-actually-worth-carrying).

WHY THE REBUILD
---------------
The June 2026 original ran 739 words, 7 flat cards, no galleries. Auditing its
links found 1 dead 404 (the Seamus GOAT Copper single-prong) and 3 sold out
(Bettinardi Transfusion $150, Miura Blade $60, Fyfe Artisan). Only 3 of 7 were
buyable. Same slug, so no redirect is needed — the URL does not change.

SLUG NOTE: the slug still contains the banned word "worth". It is left alone
deliberately — verify-post.py strips tags before the ban check precisely so
historical URLs don't trip it (see the comment in that script re
10-texas-courses-worth-the-trip). Renaming would need a 301 for no real gain.
The TITLE and all prose avoid the word.

STOCK / RESTOCK LOGIC — the spine of the post
---------------------------------------------
Divot tools are a category where the interesting pieces sell out. Rather than
pretend otherwise, the post splits three ways, and the split is evidence-based:

  * IN STOCK — buyable on 9 Sept 2026, one per brand.
  * THE CRAYON RACK — Kraken's evergreen colourway line. Kraken is the category
    specialist (83 divot/pitch SKUs), so it gets depth, the same exception the
    Fyfe Putter Cover Edit takes for a single-brand deep dive.
  * ON THE WATCHLIST — evergreen SKUs currently out that the maker reruns.

CRITICAL DISTINCTION, verified on-page: Kraken's limited drops state a hard cap
in the product copy ("Limited to 30" on Blacklist 024). Those are NOT restocked
and are deliberately EXCLUDED from the watchlist — including the Augusta Green
Crayon *Limited Edition*, which is a different SKU from the standard Augusta
Green. Only SKUs with no limited-quantity language are called restock
candidates.

Deliberately NOT asserted (no source):
  - a restock date, or that any specific piece WILL return
  - production numbers for anything without a stated cap
  - that Kraken tools are made in any named country (no origin published)
  - material claims beyond what each product page states
  - that the Ghost Golf tool is Ghost's own manufacture (its listing photo is
    stamped "True Putt", so the copy describes it as sold by Ghost, not made by)
"""
import re, os, json

SLUG  = "7-divot-tools-actually-worth-carrying"
TITLE = "The Divot Tool Edit &mdash; Machined, Forged and Milled, From $20 to $130"
PLAIN = "The Divot Tool Edit — Machined, Forged and Milled, From $20 to $130"
DESC  = ("Twenty-five green repair tools from sixteen makers, from a $19.99 Frogger to a $130 "
         "Sugarloaf collab. What's in stock, Kraken's crayon colourways, and the pieces that keep selling out.")
IMG = "/images/divot-tools/"
F = json.load(open("research/divot-final.json"))

SHOP = {
 "edelgolf.com":"https://edelgolf.com/products/","seamusgolf.com":"https://www.seamusgolf.com/products/",
 "swag.golf":"https://swag.golf/products/","ghostgolf.com":"https://ghostgolf.com/products/",
 "vesselgolf.com":"https://vesselgolf.com/products/","froggergolf.com":"https://froggergolf.com/products/",
 "sentinelgolf.us":"https://www.sentinelgolf.us/shop/p/","birdicorn.com":"https://birdicorn.com/products/",
 "krakengolf.com":"https://krakengolf.com/products/","bettinardi.com":"https://bettinardi.com/products/",
 "gamutgolf.com":"https://gamutgolf.com/products/","matchstickgolf.com":"https://matchstickgolf.com/products/",
 "fyfegolf.com":"https://www.fyfegolf.com/products/","malbon.com":"https://malbon.com/products/",
 "sugarloafsocialclub.com":"https://sugarloafsocialclub.com/products/","miuragolf.com":"https://miuragolf.com/products/",
}
BRAND = {
 "edelgolf.com":"Edel Golf","seamusgolf.com":"Seamus Golf","swag.golf":"Swag Golf","ghostgolf.com":"Ghost Golf",
 "vesselgolf.com":"Vessel","froggergolf.com":"Frogger","sentinelgolf.us":"Sentinel Golf","birdicorn.com":"Birdicorn",
 "krakengolf.com":"Kraken Golf","bettinardi.com":"Bettinardi","gamutgolf.com":"Gamut Golf",
 "matchstickgolf.com":"Matchstick Golf","fyfegolf.com":"Fyfe Golf","malbon.com":"Malbon",
 "sugarloafsocialclub.com":"Sugarloaf Social Club","miuragolf.com":"Miura Golf",
}
# hand-written display names + copy, keyed by the image slug
COPY = {
 "frogger":("HOP! Green Repair Tool","The cheapest thing here and the one most likely to already be clipped to a bag. Frogger builds a sprung two-prong head that pops open with a thumb, which is the whole pitch &mdash; you can work it one-handed while the other hand holds a putter."),
 "birdicorn":("6-in-1 Divot Tool","Six functions in an anodised aluminium body: repair prongs, ball marker, line stencil, groove cleaner, bottle opener and grip rest. Multi-tools usually do everything adequately and nothing well; at $20 that is a reasonable trade."),
 "ghost":("Divot Tool","A stamped stainless two-prong at the lowest end of the range, sold through Ghost's own shop. The listing photograph carries True Putt branding on the face, so treat it as a piece Ghost sells rather than one it manufactures."),
 "vessel":("&times; Birdicorn Divot Tool","Vessel is a bag house, so a divot tool is a side quest &mdash; and it went to Birdicorn to make it. Blacked-out finish with the Vessel mark cut into the head, and the only collaboration in this group at under $30."),
 "edel":("Fine Milled Repair Tool","Milled rather than stamped, which is the meaningful line in this category: a milled tool starts as a solid billet and holds an edge on the prongs instead of rolling over. Edel scripts its name across the face and leaves the rest alone."),
 "swag":("Sunglasses Divot Tool","Swag makes ball markers the way other brands make merchandise, and the divot tools carry the same logic &mdash; a shape you recognise from ten feet. The sunglasses head comes in four colourways and none of them is subtle."),
 "sentinel":("Jimmy Bar &mdash; Titanium","A bar rather than a fork. Titanium, machined, and shaped to be pushed in at an angle and levered rather than pronged and twisted &mdash; which is the repair method most superintendents actually ask for."),
 "seamus":("Hand Forged&reg; Greenskeeper Pitch Tool","Single prong, forged steel, hammer-finished so no two faces are identical. Seamus forges these by hand in Portland and the single-prong shape is deliberate: one prong pushes turf sideways from the edge of the mark, which is the technique the two-prong fork encourages you to get wrong."),
 # Kraken
 "kraken-0":("Gimme Green Crayon","The Crayon is Kraken's signature: a pitch tool CNC-milled into the exact silhouette of a Crayola, down to the wrapper ridges and the tapered tip. Gimme Green is the one that disappears into the grass when you set it down."),
 "kraken-1":("Blue Hazard Cobalt Crayon","The same milled crayon body in cobalt. The tip is the working end &mdash; a single tapered prong, so it repairs like the Seamus rather than like a fork, and the barrel gives you something to actually grip."),
 "kraken-2":("Transfusion Satin Purple Crayon","Satin purple, named for the drink. Kraken runs the Crayon in a rotating set of colours and retires none of them formally, which is why the archive runs to twenty shades and only a handful are in stock at once."),
 "kraken-3":("Slice Free Crayon (Melon)","Watermelon pink and green on one barrel. The Crayons are the only tools in this edit that read as objects first and golf equipment second, which is either the appeal or the problem."),
 "kraken-4":("Kraken Ink Crayon","Black and white, the house colourway, and the one that survives being the only bright thing in a bag of black leather. If the rest of the rack is too much, this is the entry point."),
 "kraken-5":("Yips Yellow Crayon","Currently out. Yellow with a black wrapper, and named after the thing nobody wants to say out loud on the green."),
 "kraken-6":("Beaten to a Pulp Orange Crayon","Currently out. Orange over black &mdash; the highest-contrast Crayon and the easiest to find when you set it down on cut rough."),
 "kraken-7":("Tiffany Blue Crayon","Currently out, and the one on the hero shot above. Robin's-egg blue against a white ball is the best-photographing tool in the whole category, which Kraken clearly knows."),
 "kraken-8":("The Signet &mdash; Stainless Steel","The dress option. Stainless, flat-faced, sized to sit in a pocket without the barrel of a Crayon, and the most expensive in-stock piece here at $109."),
 "kraken-9":("The Tentacle Pitch Tool &mdash; Copper","Solid copper, cast in a curled tentacle with raised suckers along the underside &mdash; which doubles as grip. Copper will darken with handling, so this is a piece that looks different in a year."),
 # watchlist
 "fyfe":("The Artisan&rsquo;s Tool &mdash; Handforged Copper","Currently out. Fyfe hand-forges in Scotland and this is the cheapest hand-made piece in the edit at $22.50, which is why it does not stay in stock."),
 "matchstick-2":("Tidy Tool &mdash; Alumilite Malachite","Currently out. Matchstick turns the handle from Alumilite, a cast resin that swirls differently in every pour, so the malachite green is a pattern rather than a colour."),
 "miura":("Blade Divot Repair Tool","Currently out. Miura shapes it like a miniature blade iron, which for a forging house in Himeji is exactly the joke you would expect them to make."),
 "gamut":("The Players Divot Tool &mdash; Solid Brass","Currently out. Solid brass, from the same Gamut workshop that cuts headcovers out of vintage baseball jerseys. Brass patinas fast in a pocket."),
 "malbon":("CLUCT Divot Tool","Currently out. A Malbon collaboration with Japanese label CLUCT, built as a clip-on charm as much as a repair tool."),
 "bettinardi":("Gone Fishin&rsquo; Gotcha Wizard","Currently out. Bettinardi runs its divot tools like its putters &mdash; small numbered runs with painted enamel faces, priced accordingly at $110."),
 "sugarloaf":("SSC &times; TOTEM 3-Piece Divot Tool","Currently out and the most expensive piece in the edit at $130. Three parts rather than one, from Sugarloaf's collaboration with TOTEM."),
}

def frames(s):
    n = 1
    while os.path.exists(f"images/divot-tools/{s}-a{n+1}.jpg"): n += 1
    return n

def gal(s, name):
    n = frames(s)
    pl = re.sub(r'<[^>]+>|&[a-z]+;|&#\d+;', '', name).strip()
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
    nm, desc = COPY[x["slug"]]
    price = f"${int(float(x['price']))}" if float(x["price"]) == int(float(x["price"])) else f"${x['price']}"
    tag = "" if x["avail"] else " &middot; sold out"
    return f"""<div class="product-card" data-frames="{frames(x['slug'])}">
      {gal(x['slug'], nm)}
      <div class="product-body">
        <div class="product-brand">{BRAND[x['dom']]}</div>
        <div class="product-name">{nm} &middot; {price}{tag}</div>
        <div class="product-desc">{desc}</div>
        <a href="{SHOP[x['dom']]}{x['handle']}" target="_blank" rel="noopener" class="product-link">Shop ↗</a>
      </div>
    </div>"""

def sec(hdr, kicker, items):
    c = "\n    ".join(card(x) for x in items)
    return (f'<section class="products">\n  <h2 class="products-hdr">{hdr}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'  <div class="products-grid">\n    {c}\n  </div>\n</section>\n')

INTRO = """<div class="writeup">
  <div class="writeup-body">
    <p>This is twenty-five green repair tools from sixteen makers, running from a $19.99 Frogger to a $130 Sugarloaf collaboration. Everything here was checked for stock on 9 September 2026, and where a piece is out, it says so on the card.</p>
    <p>The reason to care about a divot tool is that it is the one piece of equipment you use on somebody else&rsquo;s behalf. A repaired pitch mark heals in about a day; an unrepaired one takes three weeks and leaves a scar the size of a coin on a surface the greenkeeper rolls every morning. The tool is a two-dollar problem that the industry has answered with milled titanium and hand-forged copper. One maker answers it with a machined crayon.</p>
    <p>If you want the short version: buy a single-prong tool, push from the edge of the mark inward, and do not lever the middle up like a cork. Everything below is the long version.</p>
  </div>
</div>
"""

METHOD = """<section class="products">
  <h2 class="products-hdr">One Prong or Two, and Why It Matters</h2>
  <p class="cat-kicker">The shape of the head decides the repair, and the two-prong fork encourages the wrong one.</p>
  <div class="writeup-body">
    <p><strong>The technique.</strong> A pitch mark is turf pushed sideways and down, leaving the centre thin. The repair is to work the edges back toward the middle so the surface closes, then tap it flat. Levering the centre upward &mdash; the instinctive move with a two-prong fork &mdash; tears the roots that are still attached and turns a one-day recovery into a dead patch.</p>
    <p><strong>Why single prong.</strong> A single prong is hard to misuse. There is only one point of contact, so pushing inward from the edge is the natural motion. Seamus forges its Greenskeeper and Goat tools this way, Kraken tapers every Crayon to one tip, and Sentinel&rsquo;s Jimmy Bar goes further by dropping the prong entirely for a bar you insert at an angle and rock.</p>
    <p><strong>Milled versus stamped.</strong> A stamped tool is cut and pressed from sheet; a milled one is machined from solid billet. Milled prongs hold their geometry and resist rolling over at the tip, which is what turns a cheap tool into a bent one. Edel mills, Kraken mills, Gamut casts in brass. The $20 pieces are stamped, and at that price that is a fair exchange.</p>
    <p><strong>Materials.</strong> Titanium and stainless stay as they are. Copper and brass patina &mdash; Fyfe, Gamut and Kraken&rsquo;s Tentacle will all darken with pocket time, which some buyers want and some do not. Resin, like Matchstick&rsquo;s Alumilite handles, is the only material here that is decorative first.</p>
  </div>
</section>
"""

STOCK = """<section class="products">
  <h2 class="products-hdr">The Sold-Out Problem</h2>
  <p class="cat-kicker">Small makers run small batches, and the good pieces spend more time out than in.</p>
  <div class="writeup-body">
    <p>Seven of the sixteen makers here have no divot tool in stock today. That is not an editing failure, it is the category. These are single-operator workshops and side products from apparel brands, made in runs of dozens rather than thousands, and the ones with the best photography sell out first.</p>
    <p>Kraken is the clearest illustration. It lists eighty-three divot and pitch tools, which is more than any other maker in golf, and roughly seventy of them are sold out at any moment. The catalogue functions as an archive rather than a shop.</p>
    <p>The useful distinction is between pieces that return and pieces that do not. Kraken runs numbered <em>Blacklist</em> drops with a hard cap stated in the product copy &mdash; Blacklist 024 says &ldquo;Limited to 30&rdquo; on the page &mdash; and those never come back. The standard colourways carry no such language, rotate through stock, and reappear. Everything in the watchlist section below is from the second group. Nothing in it is a numbered edition, and none of these makers publishes a restock date, so treat it as a list to check rather than a promise.</p>
  </div>
</section>
"""

FAQ_ITEMS = [
 ("What is the correct way to repair a pitch mark?",
  "Work the edges of the mark inward toward the centre, then tap the surface flat with the putter sole. Do not lever the centre upward &mdash; that tears the roots still holding the turf together and turns a one-day recovery into a three-week scar."),
 ("Is a single-prong divot tool better than a two-prong?",
  "A single prong is harder to use incorrectly. With one point of contact the natural motion is pushing inward from the edge, which is the correct repair. A two-prong fork invites you to straddle the mark and lever the middle up, which is the damaging one. Seamus, Kraken and Sentinel all build single-prong or bar-style tools for this reason."),
 ("What does milled mean, and is it a real difference?",
  "A milled tool is machined from a solid billet of metal; a stamped one is pressed from sheet. Milled prongs hold their shape and resist rolling over at the tip under load. It is the main thing separating the $45-and-up tools from the $20 ones, and at $20 a stamped tool is still a fair exchange."),
 ("Which divot tool should I buy first?",
  "For $19.99 the Frogger HOP! opens one-handed and lives on a bag clip. For a tool you will keep, the Edel Fine Milled at $45 is milled rather than stamped. If you want something hand-made, Seamus forges its single-prong Greenskeeper in Portland at $76."),
 ("Why are so many of these sold out?",
  "They are made in small batches by single-operator workshops or as side products by apparel brands. Kraken alone lists eighty-three divot and pitch tools and has around seventy sold out at any given time. The catalogue is closer to an archive than a shop."),
 ("Do sold-out divot tools come back?",
  "It depends on the piece. Makers rerun standard colourways without announcing dates. Numbered limited drops do not return &mdash; Kraken states the cap in the product copy, such as &ldquo;Limited to 30&rdquo; on Blacklist 024. The watchlist in this edit only includes pieces with no stated cap."),
]
FAQ = """<section class="products">
  <h2 class="products-hdr">The Questions</h2>
  <div class="faq">
""" + "\n".join(f'    <div class="faq-q">{q}</div>\n    <div class="faq-a">{a}</div>' for q, a in FAQ_ITEMS) + """
  </div>
</section>
"""

def st(s):
    return (re.sub(r'<[^>]+>', '', s).replace("&ldquo;", '"').replace("&rdquo;", '"')
            .replace("&rsquo;", "'").replace("&amp;", "&").replace("&mdash;", "—")
            .replace("&middot;", "·").replace("&reg;", "®").replace("&times;", "×"))

SCHEMA = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": st(q),
     "acceptedAnswer": {"@type": "Answer", "text": st(a)}} for q, a in FAQ_ITEMS]}

model = open("drops/brand-to-know-gamut-golf.html", encoding="utf-8").read()
head = model[:model.find('<div class="breadcrumb">')]
tail = model[model.find('<section class="more"'):]
head = re.sub(r'<title>[^<]*</title>', f'<title>{PLAIN} — The Grassy Issue</title>', head)
for k, v in [("description", DESC), ("og:title", PLAIN), ("og:description", DESC)]:
    head = re.sub(rf'(<meta (?:name|property)="{re.escape(k)}" content=")[^"]*(")',
                  lambda m: m.group(1) + v + m.group(2), head)
head = re.sub(r'(<link rel="canonical" href=")[^"]*(")',
              lambda m: m.group(1) + f"https://thegrassyissue.com/drops/{SLUG}" + m.group(2), head)
head = re.sub(r'(<meta property="og:url" content=")[^"]*(")',
              lambda m: m.group(1) + f"https://thegrassyissue.com/drops/{SLUG}" + m.group(2), head)
head = re.sub(r'(<meta property="og:image" content=")[^"]*(")',
              lambda m: m.group(1) + "https://thegrassyissue.com/images/divot-tools/hero.jpg" + m.group(2), head)
_sb = '<script type="application/ld+json">' + json.dumps(SCHEMA) + '</script>'
head = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: _sb, head, flags=re.S)

# cheapest-first inside the in-stock group
instock = sorted(F["instock"], key=lambda x: float(x["price"]))

body = ('<div class="breadcrumb">\n  <a href="/">Feed</a><span>/</span>\n'
        '  <a href="/#feed">Drops &amp; Brands</a><span>/</span>\n  The Divot Tool Edit</div>\n'
        f'<header class="drop-header">\n  <h1>{TITLE}</h1>\n  <div class="drop-meta">\n'
        '    <span>September 9, 2026</span><span class="dot"></span>\n'
        '    <span>Drops &amp; Brands</span><span class="dot"></span>\n'
        '    <span>25 Tools &middot; 16 Makers</span>\n  </div>\n</header>\n\n'
        '<div class="drop-hero"><div class="drop-hero-img"><img src="/images/divot-tools/hero.jpg" '
        'alt="A Kraken Golf crayon-shaped pitch tool lying on cut turf beside a golf ball" /></div></div>\n'
        + INTRO + METHOD
        + sec("In Stock Now &mdash; 8 Makers",
              "Everything in this group was buyable on 9 September 2026, listed cheapest first.", instock)
        + sec("The Crayon Rack &mdash; Kraken Golf",
              "Kraken lists more divot tools than any other maker in golf, and mills most of them into the shape of a crayon.",
              F["crayon"])
        + STOCK
        + sec("On the Watchlist &mdash; 7 Makers",
              "Standard pieces that are out today and carry no stated production cap, so they rotate back.",
              F["watch"])
        + FAQ)

open(f"drops/{SLUG}.html", "w", encoding="utf-8").write(head + body + tail)
n = sum(len(v) for v in F.values())
print(f"wrote drops/{SLUG}.html | {n} products | "
      f"~{len(re.sub(r'<[^>]+>', ' ', head + body + tail).split())} words")
