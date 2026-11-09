"""build-gift-guide-1b.py — 2026 Holiday Gift Guide, Part 1 of 3, brand-by-brand format (9 November 2026).
Lenny: pivot to brand-by-brand; 9-10 brands per category, a handful of products per brand, larger template. Brand map approved.
FACTS: product pages read November 9, 2026; prices as shown to a US visitor (Chrome). Brand facts from TGI brand index + product pages.
"""
import html as H, json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import gift_guide_series as GS
ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"
TITLE = "The 2026 Golf Gift Guide, Part 1: Everyday Upgrades, Range Rat Gifts and Stocking Stuffers, Brand by Brand"
DESC = ("30 independent golf brands and the gifts each one does best: everyday kit made as well as it can be, gifts for the golfer who lives "
        "at the range, and small things for a stocking.")
H1 = "The 2026 Golf Gift Guide, Part 1: Everyday Upgrades, Range Rat Gifts and Stocking Stuffers"
BC = "Gift Guide 2026, Part 1"
SLUG = "golf-gift-guide-2026-everyday-range-rat-stocking-stuffers"
IMG = "/images/gift-guide-1b"
D = json.loads((ROOT / "research/gift-guide-2026/p1b-data.json").read_text())
FRN = json.loads((ROOT / "research/gift-guide-2026/frames1b.json").read_text())
BH = json.loads((ROOT / "research/gift-guide-2026/brandhero1.json").read_text())
GBP = {"sinkingbirdies.co.uk"}
NAME_FIX = {"apres-golf-®-3d-rubber-ball-marker": "Sticker Pack, 3 Bumper Stickers", "lpga-vintage-patch-sherpa-fleece-headcover": "Pouch Stash Case",
            "script-hat-copy": "Crest Hat", "goat-point": "Goat Hill Collection Marker", "mystery-pack-4-gloves-4-ball-markers": "Holiday Mystery Pack: 4 Gloves + 4 Markers",
            "drvn-putter-grip": "Pistol Putter Grip", "ball-mark-holster": "Ball Marker Holster", "magpad": "MagPad Magnetic Hub", "colorway-towels": "Colorway Towel",
            "roller-putting-mats": "The Roller 9-Foot Putting Mat", "simmy-indoor-golf-bag": "Simmy Indoor Golf Bag"}
def nm(k):
    v = D[k]; h = k.split("|")[1]
    t = NAME_FIX.get(h) or v["title"]
    t = re.sub(r"\s*[-–|]\s*(Pre-Order|Preorder)\b.*", "", t)
    t = t.replace("•", "&middot;").replace(" - ", ", ").replace(" | ", ", ")
    if t.isupper(): t = t.title()
    return t
def pr(k):
    v = D[k]; p = v["price"]
    s = f"{p:,.2f}".replace(".00", "")
    return f"&pound;{s} (~${round(p*1.33)})" if v["d"] in GBP else f"${s}"
def K(d, h): 
    k = f"{d}|{h}"; assert k in D and "err" not in D[k], k; return k
CATS = [
 ("everyday", "The Everyday Item as Well Done as Possible", "Kit they already use every round, made by someone who cared",
  "The best gift is the thing they already use every round, made better than it had to be. Nobody needs another divot tool; everybody notices when the one in their pocket is machined brass. These ten brands each make the ordinary things in a golfer&rsquo;s bag (the tool, the marker, the towel, the pouch, the belt) about as well as they can be made.",
  [("TOTEM", "", "Machined, then balanced by hand. TOTEM makes divot tools the way other people make watches: brass or titanium, on paracord, each with its own carry case. The three-piece adds a removable ball mark, and the Tag.01 turns a bag tag into a machined object. We named TOTEM our top divot tool this year, and it still is.",
    [K("totem.golf","divot-repair-tool-1pcs"),K("totem.golf","1pcs-divot-tool-brass-copy"),K("totem.golf","3pcs-divot-repair-tool-raw-brass"),K("totem.golf","tag-01-magnetic-ball-mark-tag")]),
   ("DRVN Golf Co.", "United States", "DRVN designs everything around classic cars, and its ball markers are the clearest example: each is milled from stainless steel in the shape of a famous wheel. The MM-722 is the McLaren SLR 722, the LM-40 the Ferrari F40, the P-64 the Porsche 964. The houndstooth Pistol grip borrows from old motorsport interiors.",
    [K("drvngolfco.com","mm-722-ball-marker"),K("drvngolfco.com","lm-40-ball-marker"),K("drvngolfco.com","p-64-ball-marker"),K("drvngolfco.com","drvn-putter-grip")]),
   ("Agronomy Workshop", "California", "Cotton work shirts, hats and towels that feel like they came from a greenkeeper&rsquo;s shed. The heavyweight work shirt is 17.5-ounce cotton, hand-dyed and hand-sewn in Los Angeles, with a tee holder hidden in the chest pocket. The towels are printed like late-night TV ads.",
    [K("agronomywork.shop","spiritual-approach-towel-copy"),K("agronomywork.shop","heavyweight-work-shirt-ss-navy"),K("agronomywork.shop","agronomy-work-hat")]),
   ("Seamus Golf", "Beaverton, Oregon", "Seamus has been making golf&rsquo;s small things by hand in Oregon for years. The Harris Tweed scorecard holder is lined in toffee leather, folds to back-pocket size and now holds a pencil; the Macleod check pouch carries the rest. Their signature tees and a marker holster round out the everyday kit.",
    [K("seamusgolf.com","navy-harris-tweed-scorecard-holder"),K("seamusgolf.com","macleod-check-harris-tweed-drawstring-pouch"),K("seamusgolf.com","seamus-signature-golf-tees-50-pack-1"),K("seamusgolf.com","ball-mark-holster")]),
   ("Clint Orms", "Kerrville, Texas", "A Hill Country silversmith since 1992. Clint Orms engraves sterling silver ball markers by hand, so no two patterns are identical. An American flag, a buffalo head, a quail, the state of Texas: the most everyday object in golf, made like jewelry and meant to be handed down.",
    [K("clintorms.com","ball-marker-1802"),K("clintorms.com","ball-marker-1806-buffalo-head"),K("clintorms.com","ball-marker-1600-quail"),K("clintorms.com","sterling-silver-custom-state-of-texas-ball-marker")]),
   ("Magpie Supply", "Denver, Colorado", "A one-person Denver leather shop making golf&rsquo;s small things. The scorecard holder is black full-grain leather with navy thread, made for leaving the phone in the bag. The tee ring keeps a handful of tees on the bag, and the hammered brass repair tool, made with his friend Chuck, was down to its last two.",
    [K("magpie-supply.com","scorecard-holder"),K("magpie-supply.com","tee-ring"),K("magpie-supply.com","hammered-copper-repair-tool"),K("magpie-supply.com","the-bag-tag")]),
   ("Hudson Sutler", "North Bergen, New Jersey", "Hudson Sutler cuts and sews its bags in its own New Jersey factory, a few miles from Midtown. The waxed canvas pouch with its leather base is the one we would buy first: keys, wallet, phone and markers in, pouch in the bag. The club pouch, shoe bag and small tote cover everything else.",
    [K("hudsonsutler.com","heritage-waxed-canvas-pouch"),K("hudsonsutler.com","canvas-club-pouch"),K("hudsonsutler.com","heritage-golf-shoe-bag"),K("hudsonsutler.com","small-club-tote")]),
   ("Woodgrain Golf", "New York", "Woodgrain dresses golfers the way the game looked in the &rsquo;80s and &rsquo;90s: wide double-pleated trousers, clean polos and old-school caps. The Signature Belt, in croc-embossed leather with polished hardware, is the everyday piece, and it works just as well off the course.",
    [K("woodgrain.golf","the-signature-belt"),K("woodgrain.golf","players-polo-black"),K("woodgrain.golf","relaxed-double-pleated-trouser-black"),K("woodgrain.golf","script-hat-copy")]),
   ("Dimple &amp; Divot", "Raleigh, North Carolina", "Two brothers and one small thing done properly. Dimple &amp; Divot hand-assembles hickory golf brushes in Raleigh, with retractable tethers and trigger snaps; the PRO Plus is the only one with both nylon and metal bristles. The Essentials pouch and a full-grain leather valet tray finish the set.",
    [K("dimpledivot.com","hickory-golf-brush-ryegrass"),K("dimpledivot.com","hickory-golf-brush-pro-hybrid-blue"),K("dimpledivot.com","essentials-pouch-rust"),K("dimpledivot.com","infinity-leather-valet-tray")]),
   ("Manors Golf", "London", "Manors makes technical golf clothes that still look like clothes. The Greenskeeper Trouser is recycled stretch nylon with eight pockets, and one of them hides a magnet for your ball marker; we only found it by wearing them. The Hazard marker, Eighteenth pitch repair and Ranger mockneck complete the everyday kit.",
    [K("www.manorsgolf.com","recycled-greenskeeper-trouser"),K("www.manorsgolf.com","trio-emblem-ball-marker"),K("www.manorsgolf.com","emblem-divot-tool"),K("www.manorsgolf.com","mockneck-ranger-polo")])]),
 ("range-rat", "For the Range Rat", "For the golfer who hits two buckets before a casual nine",
  "Every group has one: the golfer who hits two buckets before a casual nine. They don&rsquo;t want another sleeve of balls; they want the range to feel less like a chore. These ten brands make the things that help: alignment sticks, shag bags, par-3 bags, gloves by the pair and something warm for the cold buckets.",
  [("SAHA", "US &amp; T&uuml;rkiye", "Saha is Turkish for field, and the brand brings a sense of humor to the range. The clip towel hooks onto the bag, the bamboo tees come packed like a pack of cigarettes, and the How&rsquo;s My Drive cap asks the question for you. A crew sock pack covers the rest.",
    [K("saha.golf","saha-clip-towel"),K("saha.golf","pack-of-tees"),K("saha.golf","hows-my-drive-cap"),K("saha.golf","saha-crew-sock-pack")]),
   ("Fella Golf", "Europe", "Golf with zero seriousness and very good gear. Fella&rsquo;s Ripstop Cargo is the most thought-through range pant we know: glove loops, a tee holder and magnetic cargo pockets. Add the stretch glove, a reversible fleece bodywarmer in a golf-cart print and a corduroy cap for the cold buckets.",
    [K("fellagolf.com","fella-ripstop-cargo-pant"),K("fellagolf.com","reversible-bodywarmer-fleece-golfcart-pattern"),K("fellagolf.com","fella-stretch-fit-golf-glove"),K("fellagolf.com","cozy-corduroy-cap-pine-green-1")]),
   ("BLURRD", "", "A range rat goes through gloves, and BLURRD sells them in pairs. Each 2-pack is AAA Cabretta leather in two colorways, from the tan-and-burgundy Heritage to the purple 24K. The holiday mystery pack is the one for the bag: two pairs of gloves and four ball markers.",
    [K("blurrdgoods.com","the-heritage-collection-churchill-2-pack"),K("blurrdgoods.com","the-24k-golf-glove-purple-white-2-pack"),K("blurrdgoods.com","the-saturday-collection-powderd-white-2-pack"),K("blurrdgoods.com","mystery-pack-4-gloves-4-ball-markers")]),
   ("Clutch Golf Company", "United States", "Clutch makes the alignment sticks it couldn&rsquo;t find: 42-inch hickory, handmade to order in the USA. The Range Set pairs them with a hand-stitched leather cover with a window that shows off the stripes. A hardwood club brush is the cheap add-on every range rat needs.",
    [K("clutchgolfcompany.com","range-set-alignment-sticks-leather-cover"),K("clutchgolfcompany.com","hickory-alignment-sticks"),K("clutchgolfcompany.com","handcrafted-leather-alignment-stick-cover-windowed-design"),K("clutchgolfcompany.com","clutch-hardwood-golf-club-brush-range-series")]),
   ("Thwack Sporting Co.", "West Virginia", "American hickory alignment sticks wrapped by hand in waxed Irish linen thread, a first run out of West Virginia. The Dew Sweeper is an American hardwood brush built to live on the bag, and the Pick Your Own Switch is a single hickory stick with an Appalachian joke attached.",
    [K("thwacksportingco.com","pioneer-series-alignment-stick-set"),K("thwacksportingco.com","dew-sweeper-brush"),K("thwacksportingco.com","pick-your-own-switch")]),
   ("Gamut Golf", "United States", "Gamut makes hardwood alignment sticks in colorways good enough to leave in the bag: the V7 pairs midnight navy with butter yellow. The Wilcox 10K pocket brush, in solid ebony and green sandalwood, was made with a tour caddie for life inside the ropes.",
    [K("gamutgolf.com","gg-alignment-sticks-v7"),K("gamutgolf.com","gg-alignment-sticks-v6"),K("gamutgolf.com","wilcox-10k-pocket-brush")]),
   ("Shoal Golf Co.", "United States", "Waxed canvas carry bags for golfers who walk. The Shoal Shag Bag holds 60 to 65 balls without the look of a mesh range bag, and the Simple Sunday Bag is built for a few clubs and a quick nine. The No Dirt caddie towel and corduroy hat match the bags.",
    [K("shoalgolfco.com","the-shoal-shag-bag"),K("shoalgolfco.com","the-shoal-simple-sunday-bag"),K("shoalgolfco.com","shoal-caddie-towel-white-with-green-stripes"),K("shoalgolfco.com","shoal-golf-co-corduroy-hat")]),
   ("Sunday Golf", "San Diego, California", "Lightweight carry bags for the par-3 and the casual nine. The Loma holds up to six clubs and has an insulated two-can pocket, which is all a range session needs. The Simmy is built for the simulator, and the magnetic towel and bamboo tees finish the kit.",
    [K("sundaygolf.com","loma-toasted-almond-par-3-golf-bag"),K("sundaygolf.com","simmy-indoor-golf-bag"),K("sundaygolf.com","loma-magnetic-golf-towel-black"),K("sundaygolf.com","par3-bamboo-golf-tees-80ct")]),
   ("Pinned Golf", "Massachusetts", "Affordable, colorful golf tech from three friends. The Prism+ is our favorite rangefinder for the money and was on sale when we checked. The Roller is a nine-foot putting mat for the office or living room, and the MagPad and towels keep everything on the cart.",
    [K("pinnedgolf.com","prism-rangefinder-black"),K("pinnedgolf.com","roller-putting-mats"),K("pinnedgolf.com","colorway-towels"),K("pinnedgolf.com","magpad")]),
   ("Edel Golf", "Arvada, Colorado", "Edel built its name fitting putters by where you actually aim. The Array alignment plates let Array putter owners swap sight lines to fit their eye. The milled repair tool, glove caddie and Golf Con marker are small, precise things for the practice green.",
    [K("edelgolf.com","array-alignment-plates"),K("edelgolf.com","edel-milled-divot-tool"),K("edelgolf.com","glove-accessory-caddie-gray"),K("edelgolf.com","golf-con-ball-marker")])]),
 ("stocking", "Small Enough for a Stocking", "Small things people keep",
  "Stocking stuffers are where golf gifts go to die, mostly as novelty tees and logo balls nobody plays. These ten brands make small things people keep: markers in brass, leather and enamel, tees that smell like something, a lip balm with a ball marker in the lid. Most of it is under $30.",
  [("Birdie Balm", "Canada", "An all-natural lip balm with a magnetic ball marker built into the lid, so it is always in your pocket. Every marker reads &ldquo;Make This Putt.&rdquo; The stocking-stuffer set adds an On Course lid, and the striped socks are the cheapest good gift here.",
    [K("birdiebalm.co","birdie-balm"),K("birdiebalm.co","3-pack-birdie-balm"),K("birdiebalm.co","stocking-stuffer-3-pack-on-course-lid"),K("birdiebalm.co","two-stripe-socks")]),
   ("Apr&egrave;s-Golf", "California", "Apr&egrave;s-Golf is for golfers who enjoy the drink after as much as the round. The tees come in a pack that looks like a pack of smokes, with a warning that side effects may include enjoying yourself. The stash pouch, socks and bumper stickers keep the joke going.",
    [K("apresgolf.com","warning-habit-forming-premium-golf-tees"),K("apresgolf.com","lpga-vintage-patch-sherpa-fleece-headcover"),K("apresgolf.com","apres-golf-scratch-text-logo-socks-crew"),K("apresgolf.com","apres-golf-®-3d-rubber-ball-marker")]),
   ("Hidden Links Society", "United States", "Anti-country-club golf that gives 2% of every sale to Youth on Course. The aged brass stencil marker is heavy enough to feel like something, the single prong pitch tool matches it, and Tee It High covers both the tees and an ashtray for the 19th hole.",
    [K("hiddenlinkssociety.com","stencil-collection-ball-marker-aged-brass"),K("hiddenlinkssociety.com","single-prong-pitch-mark-tool-aged-brass"),K("hiddenlinkssociety.com","tee-it-high-tees-25-pack"),K("hiddenlinkssociety.com","tee-it-high-ashtray-catch-all-white")]),
   ("Lazyface", "Atlanta, Georgia", "Mineral sunscreen from Dr. Steven Kent for golfers who skip skincare, with a sense of humor about it. The Facestick fits a pocket, the Facescreen covers the whole face without a white cast, and the koozie and smiley socks are pure stocking material.",
    [K("lazyface.com","facestick"),K("lazyface.com","facescreen"),K("lazyface.com","the-koozie"),K("lazyface.com","the-smiley-socks")]),
   ("Pins &amp; Aces", "Arvada, Colorado", "A family-owned brand making heavy, cast stainless steel markers finished in oven-cured enamel, at $14.95 each. Two ice cubes, a red party cup, Denver&rsquo;s 5280 elevation and a crown: pick the one that sounds like them.",
    [K("pinsandaces.com","ice-cubes-ball-marker"),K("pinsandaces.com","red-party-cup-ball-marker"),K("pinsandaces.com","5280-ball-marker"),K("pinsandaces.com","crown-ball-marker")]),
   ("Scotch &amp; Skins", "United States", "Leather ball markers cut from Wickett &amp; Craig leather, from an American tannery founded in 1867, with a metal insert for weight and gold-embossed alignment lines. Handcrafted in the USA and easy to spot on a long putt.",
    [K("scotchandskins.com","ball-marker-1"),K("scotchandskins.com","ball-marker-2"),K("scotchandskins.com","ball-marker-4")]),
   ("3 Putt Round", "Milan, Italy", "Bamboo tees that smell like something, in packs of 21. Eucalyptus to reset after a bad shot, citrus for the first tee, mint and grape in a set named after the drink every golf club serves.",
    [K("3puttround.com","the-eucalyptus-scented-blue-tee-pack"),K("3puttround.com","pin-seeker"),K("3puttround.com","fairway-finder"),K("3puttround.com","the-transfusion")]),
   ("Sinking Birdies", "Hampshire, England", "Bold prints on the small stuff. The solid metal divot tools come in a hippie van and a pizza box, the Cabretta gloves come in loud patterns, and the Marker Deck is a wooden stand for the collection of markers that would otherwise live at the bottom of the bag.",
    [K("sinkingbirdies.co.uk","bogey-machine-divot-tool"),K("sinkingbirdies.co.uk","fresh-slices-divot-tool"),K("sinkingbirdies.co.uk","zigzag-cabretta-golf-glove"),K("sinkingbirdies.co.uk","the-marker-deck")]),
   ("Matchstick Golf", "Portland, Oregon", "Hand-painted ball markers with a sense of humor, out of St. Johns, Portland. Putterade is the signature, the Big Apple is limited to 50 pieces, and the mystery draw is the cheapest surprise in golf.",
    [K("matchstickgolf.com","putterade"),K("matchstickgolf.com","big-apple-ball-marker"),K("matchstickgolf.com","mystery-blind-draw-golf-ball-marker"),K("matchstickgolf.com","flame-magnetic-hat-clip")]),
   ("Swell Marks", "Coronado, California", "Ball markers named after surf breaks, made by a Navy oceanographer. Red Sun is stainless steel, laser colored and hand finished; Skulligan is a cracked skull in sunglasses throwing a shaka; and the resin pitch tools are one-off pours.",
    [K("swellmarks.com","red-sun"),K("swellmarks.com","skulligan-first-wave"),K("swellmarks.com","goat-point"),K("swellmarks.com","resin-pitch-tool-014")])]),
]
GIFTED = set()
SECTIONS = [(c[1], c[0], [k for b in c[4] for k in b[3]], c[2]) for c in CATS]
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
CSS = ('<style>/*TGI-GG-BRAND*/.gg-brand{max-width:1180px;margin:0 auto;padding:44px 0 8px;border-top:1px solid rgba(20,20,20,.12)}'
 '.gg-bhero{margin:0 0 18px;aspect-ratio:2000/860;overflow:hidden}.gg-bhero img{width:100%;height:100%;object-fit:cover;display:block}.gg-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}.gg-bhead{max-width:760px;margin:0 auto 22px;text-align:center}.gg-cat{margin-top:72px;padding-top:56px;border-top:3px solid #2d4a2b}.gg-cat .products-hdr{font-size:clamp(40px,6.2vw,72px);line-height:1.02;letter-spacing:-.01em;margin:10px 0 10px}.gg-bname{font-size:30px;margin:8px 0 10px;line-height:1.15}'
 '.gg-bwhy{font-size:17px;line-height:1.6;margin:0}.gg-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}'
 '.gg-grid[data-n="3"]{grid-template-columns:repeat(3,minmax(0,1fr));max-width:900px;margin:0 auto}'
 '.gg-grid .product-name{font-size:15px}.gg-grid .product-body{padding:12px 12px 14px}'
 '@media(max-width:900px){.gg-grid,.gg-grid[data-n="3"]{grid-template-columns:repeat(2,minmax(0,1fr))}}'
 '.gg-nav{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:10px auto 0;max-width:900px}.gg-nav a{font-family:var(--mono,monospace);font-size:10px;letter-spacing:.08em;text-transform:uppercase;border:1px solid rgba(20,20,20,.25);padding:4px 8px}</style>\n')
ML = json.loads((ROOT / "research/gift-guide-2026/model-lead.json").read_text()).get("1", {})  # on-model frame leads (Lenny, 9 Nov 2026)
def card(k, idx):
    v = D[k]; fr = FRN[k]
    if k in ML: fr = [fr[ML[k]]] + [x for i, x in enumerate(fr) if i != ML[k]]
    brand = v.get("brand", "")
    label = H.unescape(nm(k)).replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>' for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>' for j in range(len(fr)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery"><div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button><button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-name">{nm(k)} &middot; {pr(k)}</div>'
            f'<a href="{v["url"]}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')
def bslug(n): return re.sub(r"[^a-z0-9]+", "-", H.unescape(n).lower()).strip("-")
def category(c, n0, num):
    anchor, title, kicker, intro, brands = c
    nav = "".join(f'<a href="#b-{bslug(b[0])}">{b[0]}</a>' for b in brands)
    o = (f'\n<section class="products gg-cat">\n  <div class="drop-tag grass">{num:02d} &middot; {len(brands)} brands</div>\n'
         f'  <h2 class="products-hdr" id="{anchor}">{title}</h2>\n  <p class="cat-kicker"><strong>{kicker}</strong></p>\n'
         f'  <div class="writeup-body" style="max-width:760px;margin:0 auto 10px;"><p>{intro}</p></div>\n  <div class="gg-nav">{nav}</div>\n')
    for name, loc, why, keys in brands:
        cards = "".join(card(k, n0 + j) for j, k in enumerate(keys)); n0 += len(keys)
        lc = f'<div class="drop-tag grass" style="display:inline-block">{loc}</div>' if loc else ""
        hero = BH[H.unescape(name)]
        o += (f'  <div class="gg-brand" id="b-{bslug(name)}"><figure class="gg-bhero"><img src="{hero}" alt="{H.escape(H.unescape(name))}" loading="lazy" /><h3 class="gg-sr">{name}</h3></figure>'
              f'<div class="gg-bhead">{lc}<p class="gg-bwhy">{why}</p></div>'
              f'<div class="products-grid gg-grid" data-n="{len(keys)}">{cards}</div></div>\n')
    return o + "</section>\n", n0
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>This year&rsquo;s gift guide is three posts and nine categories, and it is built brand by brand. A single product dropped into a category never says much on its own, so each brand here gets its own block: why it belongs in the category, and four gifts that prove it. Every brand is independent, and none appears twice across the three posts.</p>
    <p>Part 1 covers the gifts that get used the most: everyday kit made as well as it can be, gifts for the golfer who lives at the range, and small things for a stocking. Thirty brands, about a hundred and twenty gifts, from a $6 hat clip to a sterling silver ball marker.</p>
    <p><strong>Where to start.</strong> For the everyday upgrade, TOTEM&rsquo;s brass divot tool. For the range rat, Clutch&rsquo;s Range Set. For the stocking, Birdie Balm, which puts a ball marker in the lid of a lip balm.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Details</div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>30</span></div>
      <div class="sidebar-detail"><span class="l">Gifts</span><span>@@N@@</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$6&ndash;$380</span></div>
      <div class="sidebar-detail"><span class="l">Categories</span><span>3 of 9</span></div>
      <div class="hashtags"><span class="hashtag">#GolfGiftGuide</span><span class="hashtag">#GolfGifts</span><span class="hashtag">#IndieGolf</span></div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
CLOSE = """
<section class="products" style="margin-top:8px;padding-top:48px">
  <div class="writeup-body" style="max-width:720px;margin:0 auto">
    <div class="drop-tag grass">The Last Word</div>
    <h2 class="products-hdr" id="last-word">Buy From the Brand, Not Just the Product</h2>
    <p>The reason this guide is built brand by brand is simple: the best gift is usually the second thing you buy from a brand you already trust. Find the brand that sounds like the person you are buying for, then pick the piece that fits.</p>
    <p><strong>Know what they play.</strong> Edel&rsquo;s alignment plates only fit Edel&rsquo;s Array putters, Clutch makes its sticks to order, and Magpie&rsquo;s brass repair tool was down to its last two. Small brands make small runs, and stock moves fast in December.</p>
    <p>Prices are as each store shows them to a US visitor. Sinking Birdies shows pounds, so those dollar figures are approximate. Everything was in stock on November 9, 2026. <a href="/drops/golf-gift-guide-2026-statement-pieces-colorways-splurges">Part 2</a> and <a href="/drops/golf-gift-guide-2026-heirlooms-tiny-makers-off-season">Part 3</a> cover the other six categories.</p>
  </div>
</section>
"""
HERO_ALT = "Three gifts: a brass TOTEM divot tool hanging from a wooden chair, a Shoal waxed canvas shag bag on the grass, and a hand holding a tin of Birdie Balm on the course"
def head_top(n):
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items = [{"@type": "ListItem", "position": i + 1, "url": D[k]["url"], "name": H.unescape(nm(k))} for i, k in enumerate(k for c in CATS for b in c[4] for k in b[3])]
    blocks = [{"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC, "url": URL, "image": og,
               "datePublished": "2026-11-09", "dateModified": "2026-11-09",
               "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington", "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
               "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"}, "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
              {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": items},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
                  {"@type": "ListItem", "position": 2, "name": "Drops & Brands", "item": "https://thegrassyissue.com/#feed"},
                  {"@type": "ListItem", "position": 3, "name": BC, "item": URL}]}]
    t, d = H.escape(TITLE, quote=True), H.escape(DESC, quote=True)
    ld = "".join(f'<script type="application/ld+json">\n{json.dumps(b, indent=1, ensure_ascii=False)}\n</script>\n' for b in blocks)
    return (f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8" />\n<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
            f'<title>{t} | The Grassy Issue</title>\n<meta name="description" content="{d}" />\n<link rel="icon" href="/favicon.ico" />\n<link rel="apple-touch-icon" href="/apple-touch-icon.png" />\n'
            f'<link rel="preconnect" href="https://fonts.googleapis.com" />\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />\n'
            f'<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />\n'
            f'<meta property="og:type" content="article" />\n<meta property="og:url" content="{URL}" />\n<meta property="og:title" content="{t}" />\n<meta property="og:description" content="{d}" />\n'
            f'<meta property="og:image" content="{og}" />\n<meta property="og:site_name" content="The Grassy Issue" />\n<meta name="twitter:card" content="summary_large_image" />\n'
            f'<meta name="twitter:title" content="{t}" />\n<meta name="twitter:description" content="{d}" />\n<link rel="canonical" href="{URL}" />\n<link rel="preload" as="image" href="{IMG}/hero.jpg" />\n{ld}')
def main(apply_):
    keys = [k for c in CATS for b in c[4] for k in b[3]]
    assert len(keys) == len(set(keys))
    for k in keys: assert FRN.get(k), k
    n = len(keys)
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    body = (f'<div class="breadcrumb">\n  <a href="/">Feed</a><span>/</span>\n  <a href="/#feed">Drops &amp; Brands</a><span>/</span>\n  {BC}</div>\n\n'
            f'<header class="drop-header">\n  <h1>{H1}</h1>\n  <div class="drop-meta">\n    <span>The Guide &middot; Holiday Gift Guide 2026, Part 1 of 3</span><span class="dot"></span>\n'
            f'    <span>30 brands &middot; {n} gifts &middot; in stock, checked November 9, 2026</span>\n  </div>\n</header>\n\n'
            f'<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="{HERO_ALT}" fetchpriority="high" /></div></div>\n')
    body += GS.nav(1)
    body += TAKE.replace("@@N@@", str(n))
    i = 1
    for num, c in enumerate(CATS, 1):
        o, i = category(c, i, num); body += o
    body += CLOSE
    body += GS.nav(1, "Keep going: the rest of the 2026 Gift Guide")
    out = head_top(n) + head_rest.replace("</head>", CSS + GS.CSS + "</head>", 1) + body + tail
    print(f"  {n} cards, {sum(len(c[4]) for c in CATS)} brands")
    if not apply_: return
    OUT.write_text(out, encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", out[:out.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    if "Mackem" in above: bad.append("leak")
    txt = re.sub(r"<[^>]+>", " ", above)
    for w in ("worth", "genuinely", "honestly", "straightforward", "selling out"):
        if re.search(rf"\b{w}\b", txt, re.I): bad.append("banned " + w)
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', out)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    if bad: sys.exit("! " + "; ".join(bad))
    print("  wrote", OUT.relative_to(ROOT))
if __name__ == "__main__": main("--apply" in sys.argv)
