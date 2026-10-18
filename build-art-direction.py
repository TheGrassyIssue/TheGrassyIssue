#!/usr/bin/env python3
"""build-art-direction.py — "13 Independent Golf Brands With the Best Art Direction", 17 October 2026.
Lenny: "I'd like to do a post about brands with the best art direction and design" (10 brands -> his picks: no Manors, Birds of
Condor or Engel; "aim for an even dozen"; "add 15 then build the post" = the 12 + Hidden Links Society). Lens: lookbooks and
photography, graphics and logos, product design. Independents only; none of the 13 appear in TGI's last 10 posts.
FACTS: each brand's own store (prices + stock 17 Oct 2026) and product copy, plus TGI's existing Brand to Know research.
PHOTOS: each brand's own (research/art-direction/frame.py). Hero: Kingfisher Golf campaign image.
"""
import html as H, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"
TITLE = "13 Independent Golf Brands With the Best Art Direction in 2026"
DESC = ("The independent golf brands with the best art direction: lookbooks, graphics and product design from Kingfisher, Left of Field, "
        "Sentinel, Whim, Found, Cloud & Wind and seven more, with the pieces that show it best.")
H1 = "13 Independent Golf Brands With the Best Art Direction"
BC = "Best Art Direction"
SLUG = "independent-golf-brands-best-art-direction"
IMG = "/images/art-direction"
DATE = "2026-10-17"
PK = json.loads((ROOT / "research/art-direction/picks.json").read_text())
FR = json.loads((ROOT / "research/art-direction/frames.json").read_text())
CUR = {"left-of-field-golf": "AUD", "found-golf": "AUD", "fyfe-golf": "GBP", "mogshade": "EUR", "slice-town": "SEK"}
def money(s, x):
    c = CUR.get(s, "USD")
    if c == "AUD": return f"A${x:,.0f}"
    if c == "EUR": return f"&euro;{x:,.0f}"
    if c == "GBP": return f"&pound;{x:,.0f}"
    if c == "SEK": return f"{x:,.0f} kr (~${round(x*0.1086):,})"
    return f"${x:,.2f}".replace(".00", "") if x % 1 else f"${x:,.0f}"
def price(s, p):
    return money(s, p["price"]) + (f" (reg. {money(s, p['cmp'])})" if p["cmp"] and p["cmp"] > p["price"] else "")
B = {
 "left-of-field-golf": ("Left of Field", "Sydney", "/drops/brand-to-know-left-of-field-golf"),
 "fyfe-golf": ("Fyfe Golf", "Fife, Scotland", "/drops/brand-to-know-fyfe-golf"),
 "slice-town": ("SLICE TOWN", "Copenhagen", "/drops/brand-to-know-slice-town"),
 "sentinel-golf": ("Sentinel Golf", "Minneapolis", "/drops/brand-to-know-sentinel-golf"),
 "kingfisher-golf": ("Kingfisher Golf", "Dallas", "/drops/brand-to-know-kingfisher-golf"),
 "forden-golf": ("Forden Golf", "United States", "/drops/brand-to-know-forden-golf"),
 "radry-golf": ("Radry", "Sheboygan, Wisconsin", "/drops/brand-to-know-radry-golf"),
 "hidden-links-society": ("Hidden Links Society", "United States", "/drops/brand-to-know-hidden-links-society"),
 "puttwell": ("Puttwell", "Honolulu", "/drops/brand-to-know-puttwell"),
 "whim-golf": ("Whim Golf", "New York", "/brands/whim-golf"),
 "found-golf": ("Found Golf", "Melbourne", "/drops/brand-to-know-found-golf"),
 "cloud-and-wind-golf": ("Cloud &amp; Wind", "California", "/drops/brand-to-know-cloud-and-wind-golf"),
 "mogshade": ("Mogshade", "Portugal", "/drops/brand-to-know-mogshade"),
}
TAKES = {
 "left-of-field-golf": "Grainy, warm and shot on Australian sea cliffs, Left of Field&rsquo;s pictures sell a feeling before a polo. Founder Nick Ilias put the brief plainly: &ldquo;Our mission isn&rsquo;t to create products that scream &lsquo;golf&rsquo;.&rdquo;",
 "slice-town": "SLICE TOWN makes golf look like a night out in Copenhagen, with motion blur, flash and its own simulator parties. The brand&rsquo;s line: &ldquo;Our purpose is to challenge tradition, and make it possible for golfers to wear whatever they want on the course.&rdquo;",
 "sentinel-golf": "Sentinel shoots against plain walls in black, gray and white, with one red tab for color, and lets Kvadrat textiles and white Dyneema do the talking. Founder John Mooty wants every piece &ldquo;rooted in quality, story, and utility.&rdquo;",
 "mogshade": "Mogshade photographs the making as much as the product: the loom, the rescued Serra da Estrela wool, a finished case on a sandstone cliff. Even the name, an old English word for the play of light and shadow, is a design brief.",
 "kingfisher-golf": "Kingfisher is what happens when an ex-PepsiCo art director starts a golf brand: tees in a cigarette box, campaigns lit like film stills, tees printed in Old East Dallas. Fiona Cohen gets the game, too: &ldquo;You can have the most humbling, humiliating day on the course or at the range and still go back for more.&rdquo;",
 "forden-golf": "Forden&rsquo;s Swingman logo comes from Doc Edgerton&rsquo;s 1938 MIT strobe photo of a golfer, dozens of swings flattened into one mark, and it runs across caps, an umbrella and a pouch tin. The brand wants golf fashion &ldquo;as dynamic and expressive as the game itself.&rdquo;",
 "radry-golf": "Every Radry piece starts as one of Tony Knapton&rsquo;s drawings. The logo&rsquo;s eyes are a circle for birdies and a square for bogeys, with a wavy line for the round in between.",
 "hidden-links-society": "Spare line drawings, a skateboard deck and black-and-white course photos from its Public 100 Project make Hidden Links feel like a field journal. Its idea of golf: &ldquo;no memberships, no private gates, no invitations required.&rdquo;",
 "puttwell": "Puttwell turns a map of Honolulu&rsquo;s Chinatown into a tonal jacquard with Sig On Smith, with one teal triangle as the loud note. Its promise: &ldquo;dress well, play well, treat others well&hellip; Puttwell.&rdquo;",
 "whim-golf": "Whim treats golf objects like design pieces: a Milan Design Week dome sold as a concrete paperweight, a putting green inside a vintage Rimowa trunk, merino shirts knit in an old Massachusetts mill.",
 "found-golf": "Found sells art next to its clothes, from a cast-aluminium vase to a bench, and wants to &ldquo;activate golf as a creative culture through clothing, art, design and storytelling.&rdquo; Co-founder Lance started it because he &ldquo;was confused at the obvious conformity in what everyone was wearing.&rdquo;",
 "cloud-and-wind-golf": "Cloud &amp; Wind makes grips and art-directs them like a fashion line, with blossom patterns, coastal sunsets and a line of Chinese verse on every one. In its own words: &ldquo;We dig back into our heritage and look for inspiration.&rdquo;",
 "fyfe-golf": "Fyfe cuts headcovers from Harris Tweed woven on the Isle of Lewis and from old golf jackets taken apart in its Scottish workshop. Founder Neil Rennie started it because Scottish pro shops felt like &ldquo;Everything was mass-produced and heavily branded.&rdquo;",
}
CARDS = {
 "whim-golf": ["Whim knits this long sleeve from American merino in an old Massachusetts mill, with horn buttons and the script logo embroidered in New York. No synthetics at all.",
               "A hand-poured concrete and gypsum model of La Cupola, Whim&rsquo;s Milan Design Week 2026 installation, with a removable concrete flag. An edition of 10.",
               "Whim cut this packable mesh tote from leftover fabric from its 2024 mesh shorts, first made to carry shirts from the garment district to its Canal Street office."],
 "left-of-field-golf": ["Left of Field cuts the Mornington boxy with longer sleeves, a nod to golden-era polos, in a two-way stretch fabric.",
               "Left of Field rebuilt this seven-panel plaid cap from an old St Andrews cap the team found in a thrift shop in Vietnam.",
               "Left of Field makes the Portsea in four-way-stretch nylon, wind resistant and mesh lined, to move from the first tee to the 18th."],
 "sentinel-golf": ["Sentinel builds this on the MacKenzie Walker in white Dyneema for its Basecamp series. Made to order in six to eight weeks; all sales final.",
               "Sentinel turned the classic MacKenzie fairway cover inside out: a rough-out Sørensen leather shell, a Maharam vinyl base and a pile fleece lining.",
               "Sentinel cuts and sews these in New York from Kvadrat&rsquo;s 3D-knit Triangles fabric, knit in Denmark, with a melton wool lining."],
 "found-golf": ["Soof Flash founder Safa El Samad embroidered golf flash-tattoo designs onto this box sweater with Found&rsquo;s Ellen Keillar and Lance Peach. An edition of 10, made to order.",
               "Found makes this dad cap in organic cotton with dark green found.golf embroidery. Its own product copy: &ldquo;Stealth wealth engaged.&rdquo;",
               "Writer and florist Briony Wright sand-casts this aluminium cone vase, drawing on the markers on sports fields. An edition of 8."],
 "kingfisher-golf": ["Kingfisher sells 12 golf tees in a custom cigarette box, the cheapest thing here and maybe the most art-directed.",
               "Kingfisher printed this tee for its city-wide search for the worst golfer in Dallas, on heavyweight USA cotton. On sale.",
               "Kingfisher makes the Antares in performance fabric with a knit collar and cuffs and a maroon scalloped micro pattern."],
 "cloud-and-wind-golf": ["Cloud &amp; Wind draws The Blossom from flowering trees, with a line of Chinese verse printed along each grip.",
               "Cloud &amp; Wind named Afterglow for the light after sunset on the coast, for the holes you squeeze in before dark.",
               "Cloud &amp; Wind sells the Serenade Trio as a three-grip set in mixed colorways."],
 "forden-golf": ["Forden makes this New Era low-profile mesh trucker with the Swingman on the front and the Forden script on the back.",
               "Forden makes this two-compartment metal tin for nicotine pouches with the Swingman on the lid. It is exactly the kind of object the brand loves.",
               "Forden prints this made-in-USA long sleeve with a puff-print logo on the back. Half price."],
 "radry-golf": ["Radry makes this boxy, garment-washed 7.1 oz cotton tee with Tony Knapton&rsquo;s art embroidered on the front.",
               "Radry washes this cotton snapback for a worn-in feel and embroiders the art on the front. Mid-to-high profile.",
               "Radry makes the Staple Crew in heavyweight 14.7 oz French terry with embroidered artwork, in a relaxed fit."],
 "fyfe-golf": ["Fyfe cut this from a vintage Mizuno golf jacket, taken apart and recut into just four headcovers, so no two match. Made in Scotland.",
          "Fyfe makes this cover from a herringbone tweed woven on the Isle of Lewis, with a purple fleece lining. A summer limited edition that won&rsquo;t return.",
          "Fyfe makes this rangefinder case in water-resistant waxed canvas with a mesh lining and a waterproof YKK zip. Made in Scotland."],
 "slice-town": ["SLICE TOWN sells this yellow knit balaclava &ldquo;for when your game&rsquo;s so bad, you need full anonymity.&rdquo;",
                "SLICE TOWN makes this nylon track jacket, designed in Copenhagen, with a high collar, ST. on the chest and a golf ball printed on the back.",
                "SLICE TOWN makes this boxy short-sleeve windbreaker in charcoal nylon, light enough for a hot round."],
 "mogshade": ["Mogshade makes this case by hand from rescued wool woven in the Serra da Estrela mountains, with loops for tees, a marker pocket and a carabiner.",
              "Mogshade made this screen-printed David Shillinglaw x Golf, Curated tee as a limited edition of 25 pieces.",
              "Mogshade makes this 100% wool poster by hand with Soft Hands Club, for their Loomed Rounds project. Allow eight weeks."],
 "puttwell": ["Puttwell made this polo for the Waikahalulu capsule with Sig On Smith: a tonal jacquard map of Honolulu&rsquo;s Chinatown with a triangle on the back.",
              "Puttwell&rsquo;s first carry bag, made with Sig On Smith in its abstract map print of Chinatown.",
              "Puttwell makes this stripe polo in a cotton-modal blend with a small embroidered crab on the chest."],
 "hidden-links-society": ["Hidden Links puts its Dead Run skeleton runner on an oatmeal tri-blend hoodie. Preorders run through October 25, shipping mid November.",
              "Hidden Links makes this 7-inch popsicle deck to order, with the double Running Man logo underneath. Ride it or hang it.",
              "Hidden Links makes this five-panel cotton cap with Play Faster on the front, &ldquo;a PSA you can wear.&rdquo;"],
}
BANDCAP = {
 "whim-golf": ["In a golf dome", "The merino long sleeve", "The WHIMOWA putting-green trunk"],
 "left-of-field-golf": ["Shot on the coast", "Pleats and a cap", "Wide trousers"],
 "sentinel-golf": ["The merino polo", "The Basecamp vest", "Head to toe"],
 "found-golf": ["Found&rsquo;s cast cone", "The golf-ball light wall", "Embroidery detail"],
 "kingfisher-golf": ["The studio set", "Campaign portrait", "Lit like a film still"],
 "cloud-and-wind-golf": ["Against a coastal sunset", "In the blossoms", "On a stone wall"],
 "forden-golf": ["The Swingman umbrella", "The Swingman, in red", "The caps"],
 "radry-golf": ["Knapton&rsquo;s drawing", "On the course", "At the corner store"],
 "fyfe-golf": ["A jacket before it became covers", "Harris Tweed on the course", "In the locker room"],
 "slice-town": ["The balaclava, in motion", "At a SLICE TOWN event", "The brown quarter zip"],
 "mogshade": ["On the loom", "The packaging", "A course case on the rocks"],
 "puttwell": ["Puttwell in Honolulu", "The label", "The teal triangle"],
 "hidden-links-society": ["The running man", "From the Public 100 Project", "A framed print"],
}
GROUPS = [
 ("pictures", "The Pictures", "Brands whose photography does the selling.", ["left-of-field-golf", "slice-town", "sentinel-golf", "mogshade"]),
 ("graphics", "The Graphics", "Logos, drawings and prints you could hang on a wall.", ["kingfisher-golf", "forden-golf", "radry-golf", "hidden-links-society", "puttwell"]),
 ("objects", "The Objects", "Where the product itself is the design statement.", ["whim-golf", "found-golf", "cloud-and-wind-golf", "fyfe-golf"]),
]
PQ = {
 "pictures": ("Since it started, the project has always been about bringing new ideas, materials, and people into the golf space, not only to make it more interesting but to make it more fun.", "John Mooty, Sentinel Golf founder"),
 "graphics": ("You can learn a lot about life through golf and I wanted my logo to be a reminder of that.", "Tony Knapton, Radry founder"),
 "objects": ("Most products begin with either a material or a story.", "Neil Rennie, Fyfe Golf founder"),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>This is why we cover independent golf. A small brand has no committee standing between the person with the idea and the thing you end up holding, so you get a point of view: a logo lifted from a 1938 strobe photograph, a grip with poetry printed on it, a cap rebuilt from an old St Andrews cap found in a thrift shop in Vietnam. That design language is half the fun of playing now. It turns up in the bag, on the first tee and in conversation with whoever you&rsquo;re paired with.</p>
    <p>The ones that stand out commit to a single idea and carry it everywhere. Kingfisher&rsquo;s founder came from PepsiCo&rsquo;s creative department, and you can see it in the cigarette-box tee pack and campaign images lit like film stills. Forden built a whole range around one historical photograph. Whim took a golf object to Milan Design Week. Fyfe and Mogshade let the material lead, from Harris Tweed and old golf jackets to rescued mountain wool, so every piece comes with a story about where it came from. None of them looks like anything in the pro shop, and none of them looks like each other.</p>
    <p>Where is it going? Look at what these brands sell besides clothes. Found sells sculpture and a bench. Mogshade makes hand-loomed wool posters. Hidden Links has a skateboard deck, and Whim sells a concrete paperweight. Golf brands are starting to make things for the house as well as the course, and we expect more of it, along with more one-of-one pieces cut from old garments, more artist collaborations and more brands throwing their own events the way SLICE TOWN does in Copenhagen. The game is becoming a reason to make things, and the independents are getting there first.</p>
    <p>These 13 do it best, in the pictures they take, the graphics they draw and the objects they make. Each gets a short take, three of its own photos and three pieces, priced on October 17, 2026.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The 13</div>
      <div class="sidebar-detail"><span class="l">The Pictures</span><span>Left of Field, SLICE TOWN, Sentinel, Mogshade</span></div>
      <div class="sidebar-detail"><span class="l">The Graphics</span><span>Kingfisher, Forden, Radry, Hidden Links, Puttwell</span></div>
      <div class="sidebar-detail"><span class="l">The Objects</span><span>Whim, Found, Cloud &amp; Wind, Fyfe</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$9&ndash;$890</span></div>
      <div class="sidebar-detail"><span class="l">Prices</span><span>Checked October 17, 2026</span></div>
      <a href="/brands" class="sidebar-cta">The Brand Index &#8599;</a>
      <div class="hashtags"><span class="hashtag">#ArtDirection</span><span class="hashtag">#GolfDesign</span><span class="hashtag">#IndependentGolf</span></div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("Which independent golf brands have the best art direction?", "Our 13 for 2026 are Left of Field, SLICE TOWN, Sentinel Golf and Mogshade for photography; Kingfisher Golf, Forden Golf, Radry, Hidden Links Society and Puttwell for graphics; and Whim Golf, Found Golf, Cloud & Wind and Fyfe Golf for product and object design."),
 ("How did TGI choose these brands?", "On lookbooks and photography, graphics and logos, and product design. Only independent brands qualified, and we left out any brand featured in our ten most recent posts to keep the list fresh."),
 ("What is the story behind the Forden Golf logo?", "Forden's Swingman logo comes from Doc Edgerton's 1938 strobe photograph of a golfer at MIT, which captured one swing as dozens of overlapping figures."),
 ("Which golf brand is run by a former art director?", "Kingfisher Golf in Dallas. Founder Fiona Cohen was an art director at PepsiCo, specializing in animation and motion design, before starting the brand."),
 ("What is the cheapest way into these brands?", "Kingfisher's tee box at $9, a Cloud & Wind grip at $18, or a Hidden Links Society Play Faster cap at $37, as of October 17, 2026."),
]
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-GT-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}'
            '.ig-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:0 0 26px}.ig-grid figure{margin:0}.ig-grid img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block;background:#eceae5}.ig-cap{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink);opacity:.5;margin-top:8px;line-height:1.5}@media(max-width:720px){.ig-grid{grid-template-columns:repeat(3,1fr);gap:6px}.ig-cap{display:none}}'
            '.ad-group{text-align:center;padding:64px 0 8px;border-top:.5px solid var(--ink);margin-top:40px}.ad-group h2{font-size:clamp(30px,4vw,44px);margin:10px 0 8px}.ad-group p{max-width:640px;margin:0 auto;opacity:.75}.ad-more{display:block;text-align:center;font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;margin:18px 0 0}.ad-more a{border-bottom:1px solid currentColor}</style>\n')
def card(s, j, p, idx):
    fr = FR[s]["prods"][j]; name = B[s][0]
    label = H.unescape(f"{name} {p['title']}").replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {k+1} of {len(fr)}" loading="lazy" /></div>' for k, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if k == 0 else ""}" data-i="{k}" aria-label="View image {k+1}"></button>' for k in range(len(fr)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery"><div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button><button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{name}</div><div class="product-name">{H.escape(p["title"])} &middot; {price(s, p)}</div>'
            f'<div class="product-desc">{CARDS[s][j]}</div><a href="{p["url"]}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')
def brand_sec(s, n0):
    name, loc, link = B[s]
    figs = "\n".join(f'  <figure><img src="{f}" alt="{name} campaign image: {re.sub("<[^>]+>","",BANDCAP[s][i])}" loading="lazy" /><figcaption class="ig-cap">{BANDCAP[s][i]}</figcaption></figure>' for i, f in enumerate(FR[s]["band"]))
    cards = "\n".join(card(s, j, p, n0 + j) for j, p in enumerate(PK[s]["prods"]))
    more = "Read our Brand to Know" if link.startswith("/drops/") else "See every TGI story"
    return (f'\n<section class="products" style="margin-top:8px;">\n  <div class="drop-tag grass">{loc}</div>\n  <h2 class="products-hdr" id="{s}">{name}</h2>\n'
            f'  <p class="cat-kicker">{TAKES[s]}</p>\n  <div class="ig-grid">\n{figs}\n  </div>\n'
            f'  <div class="products-grid" data-n="3">\n{cards}\n  </div>\n  <div class="ad-more"><a href="{link}">{more} &rarr;</a></div>\n</section>\n'), n0 + 3
def pq(k):
    q, who = PQ[k]
    return f'\n<div class="pull-quote" style="margin:56px auto 24px">\n  <div class="pull-quote-inner">&ldquo;{q}&rdquo;<span class="pull-quote-attr">&mdash; {who}</span></div>\n</div>\n'
def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>' for q, a in FAQ)
    return f'\n<section class="products" style="border-top:none;padding-top:48px">\n  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n'
def head_top():
    og = f"https://thegrassyissue.com{IMG}/btk-og.jpg"
    items = [{"@type": "ListItem", "position": i + 1, "name": H.unescape(B[s][0]), "url": f"https://thegrassyissue.com/brands/{s}"} for i, s in enumerate(s for g in GROUPS for s in g[3])]
    blocks = [
     {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC, "url": URL, "image": og, "datePublished": DATE, "dateModified": DATE,
      "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington", "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
      "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"}, "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
     {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
     {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": items},
     {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
      {"@type": "ListItem", "position": 2, "name": "Drops & Brands", "item": "https://thegrassyissue.com/#feed"}, {"@type": "ListItem", "position": 3, "name": BC, "item": URL}]}]
    t, d = H.escape(TITLE, quote=True), H.escape(DESC, quote=True)
    ld = "".join(f'<script type="application/ld+json">\n{json.dumps(b, indent=1, ensure_ascii=False)}\n</script>\n' for b in blocks)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{t} | The Grassy Issue</title>
<meta name="description" content="{d}" />
<link rel="icon" href="/favicon.ico" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
<meta property="og:type" content="article" />
<meta property="og:url" content="{URL}" />
<meta property="og:title" content="{t}" />
<meta property="og:description" content="{d}" />
<meta property="og:image" content="{og}" />
<meta property="og:site_name" content="The Grassy Issue" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{t}" />
<meta name="twitter:description" content="{d}" />
<link rel="canonical" href="{URL}" />
<link rel="preload" as="image" href="{IMG}/btk-hero.jpg" />
{ld}"""
def main(apply_):
    allb = [s for g in GROUPS for s in g[3]]
    assert set(allb) == set(PK) == set(B) == set(TAKES) == set(CARDS) and len(allb) == 13
    for s in allb:
        for f in FR[s]["band"] + [x for p in FR[s]["prods"] for x in p]:
            assert (ROOT / f.lstrip("/")).is_file(), f
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>October 17, 2026</span><span class="dot"></span>
    <span>13 brands &middot; 39 pieces</span><span class="dot"></span>
    <span>Prices checked October 17, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/btk-hero.jpg" alt="Kingfisher Golf campaign photo: a man in a navy polo with a white collar carrying a vintage brown leather bag on his shoulder against a dark backdrop" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for key, h2, intro, slugs in GROUPS:
        if key in PQ: body += pq(key)
        body += f'\n<section class="ad-group" id="{key}"><div class="drop-tag grass">{len(slugs)} brands</div><h2>{h2}</h2><p>{intro}</p></section>\n'
        for s in slugs:
            o, n = brand_sec(s, n); body += o
    body += faq_html()
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_: print("  dry run"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Kalamunda", "Howie", "Gumtree", "Dual Sport", "Metalwood", "Hypebeast", "Skratch"):
        if leak in above: bad.append("leak " + leak)
    if fin.count('class="product-card"') != 39: bad.append("card count")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", above), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides|brands)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")
if __name__ == "__main__":
    main("--apply" in sys.argv)
