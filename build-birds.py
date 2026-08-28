#!/usr/bin/env python3
"""The Bird Edit — 20 pieces using birds as a design element.

Lenny approved all 20 from the selection grid on 2026-08-28, including three brand
repeats (Malbon x Gumtree twice, Smathers & Branson twice). Grouped so the pairings
read as deliberate rather than padding.

TWO RESEARCH CORRECTIONS worth remembering:
  - RADRY "Gang Gang" is NOT slang. The covers carry embroidered CANADA GEESE — black
    neck, white chinstrap, tan body — on sage corduroy. My first researcher filed it as
    slang because the product description only says "corduroy exterior" and never names
    the motif. Lenny knew. Confirmed by zooming the product photo.
  - GUMTREE'S SLUGS ARE SWAPPED. The product titled "State Bird - Headcover" lives at
    /shop/p/state-flower-headcover-20-mjkea, and "State Flower Crest Headcover" lives at
    /shop/p/state-bird-crest-headcover. Selecting by URL picks the wrong product; the
    State Flower one is genuinely flowers. Always match on title.

SQUARESPACE: gumtreegolfandnature.com yields its whole catalogue at
/shop?format=json-pretty (prices in cents). Same trick that cracked Sentinel.

DELIBERATELY EXCLUDED on taste: Rose & Fire flamingo covers (Palm Beach kitsch),
Robert Mark penguin (cute-mascot), Pins & Aces Open Season mallard (camo + "12 Gauge"),
Original Penguin all-over Pete prints (cartoon novelty), all licensed team merch
(Eagles/Ravens/Cardinals), Sunfish rubber ducks (bath toys, not birds).
"""
import re, os, glob, json

ROOT = os.path.dirname(os.path.abspath(__file__))
TPL  = os.path.join(ROOT, "drops", "the-niche-grip-report.html")
OUT  = os.path.join(ROOT, "drops", "the-bird-edit.html")
IMGD = "/images/birds/"
SLUG = "the-bird-edit"
TITLE = "The Bird Edit"
DESC  = ("Twenty golf pieces that use birds as a design element — Audubon prints, embroidered "
         "Canada geese, sterling quail, needlepoint wood ducks. Plus the brands named after birds "
         "that never put one on the product.")

def frames(prefix, limit=4):
    fs = sorted(glob.glob(os.path.join(ROOT, "images", "birds", prefix + "-*")))
    fs = [f for f in fs if re.search(r"-\d+\.(jpg|jpeg|png|webp)$", f, re.I)]
    return [IMGD + os.path.basename(f) for f in fs][:limit]

def card(cid, brand, name, desc, imgs, alt):
    imgs = [i for i in imgs if os.path.exists(os.path.join(ROOT, i.lstrip("/")))]
    if not imgs:
        raise SystemExit("NO IMAGES for card: " + cid)
    n = len(imgs)
    fr = "".join(f'<div class="pg-frame"><img src="{u}" loading="lazy" '
                 f'alt="{alt} &middot; view {i+1} of {n}"></div>' for i, u in enumerate(imgs))
    dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" '
                   f'aria-label="View image {i+1}"></button>' for i in range(n))
    arrows = ('<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
              '<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
              f'<span class="pg-count">1/{n}</span>') if n > 1 else ""
    return (f'<div class="product-card" id="{cid}" data-frames="{n}">\n'
            f'    <div class="product-gallery"><div class="pg-track">{fr}</div>{arrows}'
            f'<div class="pg-dots">{dots}</div></div>\n'
            f'      <div class="product-body">\n'
            f'        <div class="product-brand">{brand}</div>\n'
            f'        <div class="product-name">{name}</div>\n'
            f'        <div class="product-desc">{desc}</div>\n'
            f'      </div>\n    </div>')

SECTIONS = []

SECTIONS.append(("audubon", "The Audubon Thread", "MALBON &times; GUMTREE AND GUMTREE ALONE",
  "The best bird work in golf right now runs through one small New York label. Gumtree Golf &amp; Nature "
  "Club builds its whole identity on field guides and natural history, and when Malbon wanted a Masters "
  "capsule it went to them rather than to a print studio. What came back was Audubon plates on golf "
  "clothing, which is a stranger and better idea than a logo bird.", [
  card("bog-polo", "Malbon &times; Gumtree &middot; Sold out", "Birds of Georgia Fairway Polo &middot; $148",
    "The polo carries cardinal, blue jay, oriole, scarlet tanager, eastern bluebird, goldfinch and "
    "red-headed woodpecker, "
    "painted in the register of a nineteenth-century plate and printed across a cotton-poly blend. Jason "
    "Day wore it at Augusta in April 2026. The club approved the tops and reportedly asked him to swap the "
    "matching printed trousers for solids, which tells you the print was doing something.",
    frames("f-malbon-birdsofgeorgia-polo"), "Malbon x Gumtree Birds of Georgia polo with Audubon-style bird print"),
  card("bog-cover", "Malbon &times; Gumtree &middot; In stock", "Birds of Georgia Woodpecker Cover &middot; $160",
    "Four covers, four species, and each patch is hand-embroidered and one of a kind. Malbon states the "
    "patches were re-created from heirloom American textiles dating between the 1940s and the 1970s, which "
    "is why the colours sit faded rather than bright. Sixteen-ounce off-white canvas, made in Manhattan.",
    frames("f-malbon-woodpecker-cover"), "Birds of Georgia woodpecker embroidered driver cover on off-white canvas"),
  card("ggnc-statebird", "Gumtree Golf &amp; Nature Club &middot; Sold out", "State Bird Headcover &middot; $185",
    "Gumtree does this without a partner too. Each cover carries an embroidered state bird sitting inside "
    "the outline of its state, so a California quail runs with California and an Ohio cardinal with Ohio. "
    "The drawing is naturalist rather than mascot, and the empty canvas around it does most of the work.",
    frames("f-ggnc-statebird"), "Gumtree State Bird headcover with embroidered state birds on state outlines"),
]))

SECTIONS.append(("waterfowl", "Waterfowl", "GEESE, MALLARDS AND WOOD DUCKS",
  "Duck imagery arrives in golf through the shooting estate rather than through birding, and it brings the "
  "whole visual grammar with it: pull-up leather, needlepoint, corduroy, tan and olive and oxblood. These "
  "are the pieces that would look at home in a gun room, which is either the appeal or the problem "
  "depending on how you feel about that.", [
  card("radry-geese", "Radry Golf &middot; Sold out", "Gang Gang Driver Cover &middot; $65",
    "Radry puts Canada geese across sage corduroy and then says nothing about it &mdash; the product "
    "description mentions the cord and the sherpa lining and stops. The birds are drawn properly, with the "
    "black neck and white chinstrap, some in flight and some standing. The driver has sold out; the blade "
    "and mallet covers run at the same $65.",
    frames("f-radry-gang"), "Radry Gang Gang driver cover with embroidered Canada geese on sage corduroy"),
  card("winston-mallard", "Winston Collection &middot; In stock", "Flying Mallard Headcovers &middot; $119&ndash;140",
    "Soaring drakes stitched densely into whiskey, forest green or black pull-up leather, lined in MacKenzie "
    "plaid polar fleece and built in the USA. Pull-up leather lightens where it bends, so these mark and "
    "patina in the way the imagery wants them to. Driver, fairway and hybrid.",
    frames("f-winston-mallard-hc"), "Winston Collection flying mallard leather headcovers in whiskey pull-up leather"),
  card("sb-woodduck", "Smathers &amp; Branson &middot; In stock", "Wood Duck Decoy Hat &middot; $45",
    "Smathers &amp; Branson put a hand-stitched needlepoint wood duck decoy on a washed twill six-panel with "
    "a nickel slide. The bird is small enough that it reads as texture from any distance, which makes this "
    "the one you would actually wear off the course. The decoy is the smart choice too: a carved bird rather than a live one.",
    frames("f-sb-woodduck-hat"), "Smathers and Branson wood duck decoy needlepoint hat in steel blue"),
  card("sb-upland", "Smathers &amp; Branson &middot; In stock", "Upland Shoot Luggage Tag &middot; $45",
    "The same needlepoint craft turned to a full scene &mdash; game birds flushing over an olive ground, "
    "trimmed in full-grain Italian leather with an ID window on the reverse. Smathers &amp; Branson never "
    "name the species, and upland shoot covers quail, pheasant and grouse alike.",
    frames("f-sb-upland-tag"), "Smathers and Branson upland shoot needlepoint luggage tag with game birds"),
]))

SECTIONS.append(("quail", "Quail", "THE ONE EVERYONE REACHES FOR",
  "Quail turns up more than any other species in golf, partly because of Quail Hollow and partly because a "
  "quail with its topknot is instantly legible at two centimetres across. It suits small objects. Both of "
  "these are small objects, and both are made by hand.", [
  card("orms-quail", "Clint Orms &middot; In stock", "Ball Marker 1600 Quail &middot; $330",
    "Clint Orms has engraved silver in Kerrville, Texas for decades, and this is the only bird in his golf "
    "line. A one-inch sterling marker carries a half-inch sterling quail overlay, with wheatgrass engraved "
    "by hand around the bird and scroll work on the reverse. Few objects in golf are made to this "
    "standard, and the price says so.",
    frames("f-clintorms-quail"), "Clint Orms sterling silver 1600 Quail ball marker with hand engraving"),
  card("ssc-quail", "Sugarloaf Social Club &middot; Sold out", "Queen City Quail Knit Cover &middot; $95",
    "Sugarloaf knitted a quail into one hundred per cent wool and finished it with a tassel, made in the "
    "USA by Fore Ewe for Quail Hollow week in Charlotte. Knit is an unforgiving medium for a bird, since "
    "every feather becomes a block of colour, and this one survives the translation.",
    frames("f-ssc-quail-knit"), "Sugarloaf Social Club Queen City Quail knit fairway wood headcover in wool"),
]))

SECTIONS.append(("eagles", "The Eagle Problem", "PATRIOTISM, TATTOO FLASH AND ONE RESTRAINED SHIRT",
  "Eagles are the hardest bird to use well, because in American design an eagle stops being an animal and "
  "becomes a flag. Almost everything here is fighting that. The four below are the ones that win, and they "
  "win by going somewhere specific &mdash; heraldry, tattoo flash, western folk art, or shrinking the bird "
  "until it turns into pattern.", [
  card("dormie-eagle", "Dormie Workshop &middot; In stock", "The Oval Office Driver Cover &middot; $179",
    "Dormie put a bald eagle into a presidential seal on white full-grain leather, with stars embroidered "
    "around it. Dormie treat the bird as heraldry rather than mascot, which is the only way this idea survives, "
    "and the white leather keeps it closer to a crest than a bumper sticker.",
    frames("f-dormie-oval-office"), "Dormie Workshop Oval Office driver cover with embroidered bald eagle seal"),
  card("swag-eagle", "Swag Golf &middot; In stock", "American Ink Mallet Cover &middot; $125",
    "Swag put the eagle through American tattoo flash &mdash; hard black linework, banners, distressed "
    "stripes &mdash; and the borrowed visual language does the heavy lifting. Their other bird covers run "
    "cartoonish; this is the one that holds up, and it is still available.",
    frames("f-swag-americanink"), "Swag Golf American Ink mallet putter cover with tattoo-flash eagle"),
  card("dvx-eagle", "Devereux &middot; Sold out", "Spirit of the West Fairway Cover &middot; $54",
    "Devereux run an eagle and a sun in red and black on white leather, pitched somewhere between a Mexican "
    "blanket and a Pioneertown sign. Devereux have been pushing this desert-western direction for a while "
    "and the bird fits it, reading as folk art rather than national symbol.",
    frames("f-devereux-spiritwest"), "Devereux Spirit of the West fairway cover with embroidered eagle and sun"),
  card("hb-eagle", "Holderness &amp; Bourne &middot; In stock", "The Justice Shirt &middot; $125",
    "H&amp;B shrank the eagle until it stopped being an eagle. Their own copy calls it a stylized eagle "
    "pattern, and at arm's length the shirt reads as a geometric micro-print on performance jersey; the "
    "birds only resolve up close. It is the quietest solution to the eagle problem anyone has found.",
    frames("f-hb-justice-eagle"), "Holderness and Bourne Justice Shirt with stylized eagle micro-print"),
]))

SECTIONS.append(("antipodean", "Kookaburras and Lorikeets", "WHAT BIRDS LOOK LIKE FROM AUSTRALIA",
  "Australian golf brands get a completely different bird vocabulary, and they use it. No eagles, no "
  "mallards, no quail &mdash; instead the birds you would actually hear over a course in Queensland. It is "
  "the clearest example in golf of a design language coming straight out of a place.", [
  card("walker-kooka", "Walker Golf &middot; In stock", "Kooka Leather Driver Cover &middot; A$99.95",
    "The kookaburra perched on a golf club is Walker's house mark, taken from the founder's grandfather's "
    "WWII regiment, which gives it a reason to exist beyond decoration. Full-grain leather, velvet fleece "
    "lining, tonal embroidery so the bird sits into the hide rather than on top of it.",
    frames("f-walker-kooka-leather"), "Walker Golf Kooka leather driver cover with embroidered kookaburra"),
  card("boc-markers", "Birds of Condor &middot; In stock", "Birds in the Wild Marker Set &middot; A$39.95",
    "Three enamel markers &mdash; a rainbow lorikeet, a kookaburra and a magpie &mdash; illustrated by Mel "
    "Baxter and credited on the packaging, which almost nobody does. The drawing is naturalist and the "
    "colour is properly Australian. This photographs better than anything else the brand makes.",
    frames("f-boc-birdsinwild-markers"), "Birds of Condor Birds in the Wild enamel ball marker set"),
]))

SECTIONS.append(("flock", "The Rest of the Flock", "SWANS, FLAMINGOS AND BIRDS IN FLIGHT",
  "Everything that refuses to sit in a category. A Danish swan, a needlepoint flamingo, a toile of birds in "
  "flight and a print that reads as a flock only once you stop looking at it directly. The species here "
  "matter less than the handling.", [
  card("huega-swan", "Huega House &middot; In stock", "Vintage Swan Hat &middot; $45",
    "Huega put an embroidered swan on a high-crown structured cotton cap, with The Danish Concept arched "
    "around it. "
    "Huega build their whole identity on a borrowed European calm, and the swan carries it without needing "
    "a word of explanation. Also in black and navy.",
    frames("f-huega-swan-hat"), "Huega House vintage swan embroidered hat in forest green"),
  card("students-mapleton", "Students Golf &middot; In stock", "Mapleton S/S Polo &middot; $97",
    "Students put a flying-bird graphic across the shoulders and sleeves rather than parking it on the "
    "chest, so the birds move with the wearer. One hundred per cent cotton, summer 2026, and part of a "
    "recurring bird series &mdash; the Drummond camp-collar shirt runs the same motifs at $94.",
    frames("f-students-mapleton"), "Students Golf Mapleton polo with flying bird graphic across the shoulders"),
  card("asher-flamingo", "Asher Riley &middot; In stock", "Flamingo Needlepoint Cover &middot; $110",
    "Asher Riley build this in hand-stitched needlepoint over full-grain leather trim, with anti-pill fleece "
    "lining, sized to 460cc. "
    "Needlepoint suits a flamingo, because the medium wants flat blocks of saturated colour and a flamingo "
    "is already close to that. Palm Beach rather than duck blind, and unapologetic about it.",
    frames("f-asherriley-flamingo"), "Asher Riley flamingo needlepoint driver headcover with leather trim"),
  card("greyson-blues", "Greyson &middot; In stock", "Players Club In the Blues Polo &middot; $140",
    "Greyson run a toile-style scenic print with birds in flight worked through it, so the birds function "
    "as part of a landscape rather than as a motif stamped on top. Toile is an old decorative idea and it "
    "lands better on a polo than it has any right to.",
    frames("f-greyson-intheblues"), "Greyson Players Club In the Blues polo with toile bird print"),
  card("sb-towel", "Sinking Birdies &middot; In stock", "Flamingo Magnetic Towel &middot; &pound;17.25",
    "Sinking Birdies run a repeat flamingo print across waffle microfibre at tour size, with the magnet sewn in. This is also "
    "the only piece in Sinking Birdies' range where an actual bird appears, which is a strange fact about a "
    "brand with that name and one we return to below.",
    frames("f-sinkingbirdies-flamingo-towel"), "Sinking Birdies flamingo print magnetic golf towel"),
]))

HERO = IMGD + "hero-birdcall.jpg"

WRITEUP = """<p>Golf is the only sport whose scoring language is entirely ornithological. A birdie, an eagle, an
albatross, and in the fever dreams of people who have never made one, a condor. The words arrived by accident
&mdash; American slang around 1900, where a &ldquo;bird&rdquo; was anything excellent &mdash; and the game has
been quietly committed to them ever since. What is odd is how rarely that vocabulary makes it onto the products.
For a sport that counts in birds, golf puts remarkably few of them on anything.</p>

<p>The brands that do bother tend to be the ones with something else going on. <strong>Gumtree Golf &amp; Nature
Club</strong> treats natural history as the entire premise and sells bird calls next to headcovers.
<strong>Clint Orms</strong> has been engraving sterling in Kerrville, Texas for decades and puts a quail on a ball
marker the way he would put one on a belt buckle. <strong>Radry</strong> embroiders Canada geese across corduroy
and then declines to mention it in the product description. In each case the bird is not decoration bolted onto
golf; it is the thing the brand already cared about, pointed at a golf object.</p>

<p>Two design problems come up over and over. The first is the eagle, which in American hands stops being a bird within about a
second and becomes a flag &mdash; the pieces that survive it go somewhere specific, into heraldry or tattoo flash
or western folk art, rather than reaching for the default. The second is scale. A bird rendered large is a
mascot; a bird rendered small is a pattern. Almost everything good here is small.</p>

<p>And then there is the funniest thing the research turned up, which is how many golf brands are named after a
bird and have never once put a bird on a product. <strong>Jones</strong> built a line around its famous
&ldquo;birdie patch,&rdquo; and the patch is a <em>badminton shuttlecock</em>. <strong>Sinking Birdies</strong>
sells a Birdie Train range whose logo is a locomotive. <strong>Fyfe Golf</strong> names its cloths Black Grouse,
Fulmar and Peregrine, writes copy about seabirds drifting above the Atlantic coastline, and then delivers plain
grey herringbone every time. <strong>Seamus</strong> carries no bird at all across roughly 290 products, and
their house animal is a goat. <strong>Eastside</strong>'s &ldquo;Birdie Camo&rdquo; is duck camo.
<strong>Rhoback</strong>'s Birdie Stripe is a stripe. The scoring term did all the work, and the animal never
turned up.</p>"""

SIDEBAR = [("In this edit", "20 pieces, 17 brands"), ("Range", "$17 &ndash; $330"),
           ("Most species", "Malbon &times; Gumtree, 7 birds"), ("Best made", "Clint Orms sterling quail"),
           ("Hardest bird", "The American eagle")]

FAQ = [
 ("Why is golf scoring named after birds?",
  "The terms come from American slang around 1900, when calling something a &ldquo;bird&rdquo; meant it was "
  "excellent. A hole played one under par became a birdie, and the sequence extended upward into eagle, "
  "albatross and the largely theoretical condor for four under."),
 ("Which golf brand does birds best?",
  "On current evidence, Gumtree Golf &amp; Nature Club. Their State Bird headcovers pair an embroidered state "
  "bird with its state outline, and their Birds of Georgia collaboration with Malbon put Audubon-style plates "
  "of the cardinal, blue jay, oriole and scarlet tanager onto a polo Jason Day wore at Augusta."),
 ("What is the Radry Gang Gang cover?",
  "A corduroy headcover with Canada geese embroidered across it, sherpa-lined, at $65. The name reads as slang "
  "and the product description never mentions the birds, so it is routinely missed. The driver cover has sold "
  "out; the blade and mallet versions run at the same price."),
 ("Are there golf brands named after birds that do not use birds?",
  "Many. Jones Sports Co's &ldquo;birdie patch&rdquo; is a badminton shuttlecock. Sinking Birdies' Birdie Train "
  "logo is a locomotive. Fyfe Golf names tweeds after the black grouse, fulmar and peregrine without putting a "
  "bird on any of them. Seamus Golf's house animal is a goat."),
 ("What is the most expensive bird piece in golf?",
  "The Clint Orms Ball Marker 1600 Quail at $330 &mdash; sterling silver with a sterling "
  "quail overlay and hand-engraved wheatgrass, made in Kerrville, Texas. It is a fraction of the size of "
  "anything else on the page."),
 ("Which bird pieces can you still buy?",
  "Most of them. The Winston Collection mallard covers, Smathers &amp; Branson wood duck hat and upland tag, "
  "Dormie's Oval Office cover, Swag's American Ink mallet, Asher Riley's flamingo, Walker's Kooka cover, the "
  "Birds of Condor marker set, Huega House's swan hat and the Holderness &amp; Bourne, Students and Greyson "
  "shirts are all live. The Malbon polo, the Sugarloaf quail and the Radry driver have gone."),
]

# ----------------------------------------------------------------- assemble
tpl = open(TPL, encoding="utf-8").read()
head, tail = tpl.split('<section class="products">', 1)

head = re.sub(r"<title>.*?</title>", f"<title>{TITLE} &mdash; The Grassy Issue</title>", head, flags=re.S)
for k in ("description", "og:description"):
    head = re.sub(rf'(<meta (?:name|property)="{k}" content=")[^"]*(")', lambda m: m.group(1)+DESC+m.group(2), head)
head = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1)+TITLE+m.group(2), head)
head = re.sub(r'(<meta property="og:image" content="https://thegrassyissue\.com)[^"]*(")',
              lambda m: m.group(1)+HERO+m.group(2), head)
for pat in (r'(<link rel="canonical" href="https://thegrassyissue\.com/drops/)[^"]*(")',
            r'(<meta property="og:url" content="https://thegrassyissue\.com/drops/)[^"]*(")'):
    head = re.sub(pat, lambda m: m.group(1)+SLUG+m.group(2), head)
head = re.sub(r"(<h1[^>]*>).*?(</h1>)", lambda m: m.group(1)+TITLE+m.group(2), head, flags=re.S)
head = re.sub(r'(<div class="breadcrumb">).*?(</div>)',
              lambda m: m.group(1)+'<a href="/">The Feed</a> &rsaquo; <a href="/drops/">Drops</a> &rsaquo; The Bird Edit'+m.group(2),
              head, flags=re.S)
head = re.sub(r'(<div class="drop-meta">).*?(</div>)',
              lambda m: m.group(1)+'Drops &amp; Brands &middot; 28 August 2026 &middot; 20 pieces, 17 brands'+m.group(2),
              head, flags=re.S)
head = re.sub(r'(<div class="drop-hero-img">)\s*<img[^>]*>',
              lambda m: m.group(1)+f'<img src="{HERO}" alt="A hand working a Gumtree Golf &amp; Nature Club wooden bird call over a putting green">',
              head, flags=re.S)
head = re.sub(r'(<div class="writeup-body"[^>]*>).*?(</div>)', lambda m: m.group(1)+WRITEUP+m.group(2), head, flags=re.S)
sb = "".join(f'<div class="sidebar-detail"><strong>{k}</strong>{v}</div>' for k, v in SIDEBAR)
head = re.sub(r'(<div class="sidebar-card">).*?(</div>\s*</aside>)',
              lambda m: m.group(1)+'<div class="sidebar-label">The Edit</div>'+sb+m.group(2), head, flags=re.S)
head = re.sub(r'("headline"\s*:\s*")[^"]*(")', lambda m: m.group(1)+TITLE+m.group(2), head)
for k in ("datePublished", "dateModified"):
    head = re.sub(rf'("{k}"\s*:\s*")[^"]*(")', lambda m: m.group(1)+"2026-08-28"+m.group(2), head)
faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
    {"@type":"Question","name":re.sub(r"&[a-z]+;|&#\d+;"," ",q),
     "acceptedAnswer":{"@type":"Answer","text":re.sub(r"&[a-z]+;|&#\d+;"," ",a)}} for q,a in FAQ]}
head = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "FAQPage".*?</script>',
              '<script type="application/ld+json">'+json.dumps(faq_ld)+'</script>', head, flags=re.S)

body = []
for anchor, hdr, kicker, lede, cards in SECTIONS:
    body.append(f'<h2 id="{anchor}">{hdr}</h2>')
    body.append(f'<p class="cat-kicker"><strong>{kicker}</strong>{lede}</p>')
    body.append('<div class="products-grid">\n' + "\n".join(cards) + '\n</div>')

faq_html = ('<div class="faq">\n<h2 id="faq">Questions</h2>\n' + "\n".join(
    f'<details class="faq-q"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ) + '\n</div>')
rest = tail[tail.find('<div class="faq">'):] if '<div class="faq">' in tail else tail
rest = re.sub(r'<div class="faq">.*?</div>\s*(?=<section|<div class="more")', faq_html, rest, count=1, flags=re.S)

out = head + '<section class="products">\n' + "\n".join(body) + "\n" + rest
open(OUT, "w", encoding="utf-8").write(out)
print(f"wrote {OUT}")
print(f"sections={len(SECTIONS)} cards={sum(len(s[4]) for s in SECTIONS)} words~{len(re.sub(r'<[^>]+>',' ',out).split())}")
