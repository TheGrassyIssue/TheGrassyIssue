#!/usr/bin/env python3
"""Brand to Know — J.Lindeberg. 23 picks, drawn from the Viktor Hovland collection plus tees.

WHY BRAND TO KNOW AND NOT BRAND REVISITED (Lenny asked for Revisited, 2026-08-28):
J.Lindeberg had NO existing BTK page — only passing mentions inside the Shinnecock capsules
and Jersey Polo Edit posts, and it was absent from data/brands.json. The Revisited playbook
works by upgrading an existing ranking URL so authority consolidates; there was nothing to
upgrade. This page becomes the future Revisited target.

LENNY'S PICKS: carousel = 2 polos (Finn, 30Y Wallis), 1 pant (30Y Devyn Azalea Pink),
1 hat (30Y Cap). Page = the Hovland collection lineup plus five tees. Cleared to exceed 18.
He also asked for fewer sweaters/jackets, so the lineup is polos/pants/shoes/bags/tees only —
the one knit is a knit POLO.

FACT-CHECK NOTES — read before editing copy:
  - Founded 1996 in Stockholm by Johan Lindeberg, after he spent the early nineties building
    Diesel (distributor for Sweden -> marketing director -> CEO of Diesel US). Two accounts
    exist of the Diesel titles; "spent the first half of the nineties building Diesel" is the
    safe phrasing.
  - THE PARNEVIK PARTNERSHIP START YEAR IS NOT DOCUMENTED. "1997" is repeated in secondary
    sources with no primary backing. Vogue Scandinavia says only "mid-90s". Write mid-nineties.
  - The pink-trousers win IS documented precisely: 14 May 2000, GTE Byron Nelson Classic, TPC
    Las Colinas, won on the third playoff hole over Davis Love III. Same day Parnevik hit his
    career-high world ranking of No. 7. Sources: ESPN match report + the brand's own "Pink
    Strategy" anniversary piece.
  - THE FLIPPED CAP BRIM WAS PARNEVIK'S OWN, predating J.Lindeberg. Do not imply the brand
    invented it.
  - JOHAN LINDEBERG HAS NO CURRENT TIE TO THE BRAND and now runs a rival label (JAY3LLE).
    Quote him only as a founder looking back. Current voices are CEO Hans-Christian Meyer
    and Viktor Hovland.
  - DO NOT print the circulating Parnevik "boldest thing I've ever done... pink pants in
    Dallas" quote — the PGA.com source is dead and the wording could not be confirmed.
  - The motorcycle-through-southern-France founding anecdote is unsourced marketing. Omitted.
"""
import re, os, glob, json

ROOT = os.path.dirname(os.path.abspath(__file__))
TPL  = os.path.join(ROOT, "drops", "the-niche-grip-report.html")
OUT  = os.path.join(ROOT, "drops", "brand-to-know-jlindeberg.html")
IMGD = "/images/jlindeberg/"
SLUG = "brand-to-know-jlindeberg"
TITLE = "Brand to Know &mdash; J.Lindeberg"
DESC  = ("J.Lindeberg turns 30 in 2026. The Swedish label that put Jesper Parnevik in tight pink "
         "trousers and changed how golf dresses — the founding story, the Byron Nelson win, and 23 "
         "pieces from the Viktor Hovland line.")
META = json.load(open(os.path.join(ROOT, "research", "jlindeberg-skus.json"), encoding="utf-8"))

def frames(key, limit=4):
    fs = sorted(glob.glob(os.path.join(ROOT, "images", "jlindeberg", f"h-{key}-*.jpg")))
    return [IMGD + os.path.basename(f) for f in fs][:limit]

def card(key, brandline, desc, alt, name=None):
    d = META[key]
    imgs = [i for i in frames(key) if os.path.exists(os.path.join(ROOT, i.lstrip("/")))]
    if not imgs:
        raise SystemExit("NO IMAGES for card: " + key)
    n = len(imgs)
    title = name or d["title"].split(" / ")[0]
    price = f"${float(d['price']):,.0f}"
    fr = "".join(f'<div class="pg-frame"><img src="{u}" loading="lazy" '
                 f'alt="{alt} &middot; view {i+1} of {n}"></div>' for i, u in enumerate(imgs))
    dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" '
                   f'aria-label="View image {i+1}"></button>' for i in range(n))
    arrows = ('<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
              '<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
              f'<span class="pg-count">1/{n}</span>') if n > 1 else ""
    return (f'<div class="product-card" id="{key}" data-frames="{n}">\n'
            f'    <div class="product-gallery"><div class="pg-track">{fr}</div>{arrows}'
            f'<div class="pg-dots">{dots}</div></div>\n'
            f'      <div class="product-body">\n'
            f'        <div class="product-brand">{brandline}</div>\n'
            f'        <div class="product-name">{title} &middot; {price}</div>\n'
            f'        <div class="product-desc">{desc}</div>\n'
            f'      </div>\n    </div>')

SECTIONS = []

SECTIONS.append(("thirty", "The Anniversary Capsule", "30 YEARS &middot; AND A COLOUR",
  "J.Lindeberg is thirty this year and has chosen to celebrate by reselling its own origin story, "
  "which is either shameless or exactly right. The capsule is built around one colour and one "
  "afternoon in Texas, and the pieces carry the anniversary marks quietly enough that you would "
  "have to know what you were looking at.", [
  card("devyn-pink", "Sweden &middot; In stock",
    "This is Azalea Pink, and the whole reason the capsule exists. On 14 May 2000 at the Byron Nelson, "
    "Jesper Parnevik skipped the putting green, changed his trousers, and walked to the first tee "
    "in pink. He won on the third playoff hole over Davis Love III. Johan Lindeberg later called "
    "the idea the Pink Strategy, and the brand has now made it a product again.",
    "J.Lindeberg 30Y Devyn golf pant in Azalea Pink"),
  card("wallis-polo", "Sweden &middot; In stock",
    "A knit polo rather than a jersey one, which is the older reference the brand keeps reaching "
    "for &mdash; Walter Hagen's tailored knits, Palmer's pullovers, the pre-beige era it says golf "
    "lost somewhere in the eighties. The anniversary detailing sits inside the placket.",
    "J.Lindeberg 30Y Wallis knit polo in white"),
  card("matt-polo", "Sweden &middot; In stock",
    "The relaxed cut in the capsule, and the cheapest way to wear the anniversary without "
    "committing to pink. The capsule also runs a polo named for Parnevik himself, the "
    "30Y Jesper Retro Relaxed at $175, which sits outside the Hovland line.",
    "J.Lindeberg 30Y Matt relaxed polo in black"),
  card("30y-cap-blk", "Sweden &middot; In stock",
    "It costs sixty dollars and carries the anniversary mark on the front. Caps are where this brand has always "
    "been most legible &mdash; though the turned-up brim everyone associates with it was Parnevik's "
    "own idea, started to get sun on a pale Swedish face long before the two ever met.",
    "J.Lindeberg 30Y anniversary cap in black"),
  card("tee-30y-hale", "Sweden &middot; In stock",
    "The pink turns up again on a heavier cotton tee. The colour is doing a lot of work across this "
    "capsule and it holds up better here than it has any right to, because Azalea sits closer to "
    "coral than to fuchsia and reads as considered rather than loud.",
    "J.Lindeberg 30Y Hale t-shirt in Azalea Pink"),
]))

SECTIONS.append(("polos", "The Polos", "SIX FROM THE HOVLAND LINE",
  "Viktor Hovland has worn J.Lindeberg since 2019 and extended for three more years in January "
  "2025, which makes his collection the clearest statement of what the brand actually wants to be "
  "now. It is quieter than the archive suggests. Most of these are plain technical solids, and the "
  "one that breaks pattern is the one to look at.", [
  card("finn-polo", "Sweden &middot; In stock",
    "This is the most interesting garment in the collection by some distance. Colour-blocked navy and "
    "bright blue with hard white lines running through it, in a range that otherwise sticks to "
    "solids. This is the piece that remembers the brand used to be a fashion house.",
    "J.Lindeberg Finn polo in JL Navy colour block"),
  card("sidd-polo", "Sweden &middot; In stock",
    "Brindle is the warm brown J.Lindeberg has quietly turned into a house colour over the last few "
    "seasons, and it runs across polos, pants and knitwear so pieces sit together without matching. "
    "A useful colour on a golf course, where most of what surrounds you is green.",
    "J.Lindeberg Sidd polo in Brindle"),
  card("bo-polo", "Sweden &middot; In stock",
    "This one is white, plain and technical, and the hardest garment in golf to get right because there is nowhere for "
    "a bad collar or a cheap-feeling fabric to hide, and the reason tour players default to it. "
    "This is what the brand is judged on when nobody is looking at the archive.",
    "J.Lindeberg Bo polo in white"),
  card("tod-polo", "Sweden &middot; In stock",
    "Bias Bridge is the house pattern, and printing it micro is the smart move &mdash; it reads as "
    "texture at conversational distance and only resolves into a logo up close. Navy ground, so it "
    "works with almost anything else here.",
    "J.Lindeberg Tod print polo in Bias Bridge micro navy"),
  card("tourtech-slim", "Sweden &middot; In stock",
    "Tour Tech is the performance line the staff players actually wear, cut slim here and coloured "
    "Winetasting, which is a deep oxblood rather than the burgundy the name suggests. The fabric is "
    "the point; the colour is the reason to pick this one.",
    "J.Lindeberg Tour Tech slim fit polo in Winetasting"),
  card("lionel-polo", "Sweden &middot; In stock",
    "Ninety-five dollars, black, and nothing else going on, which makes it the value entry to a "
    "brand whose anniversary staff bag costs eight times as much. Every range needs one of these "
    "and most brands price it worse.",
    "J.Lindeberg Lionel polo in black"),
]))

SECTIONS.append(("pants", "The Pants", "WHERE THE BRAND MADE ITS NAME",
  "Trousers are the reason anyone knows this label. The story golf tells about J.Lindeberg is a "
  "story about leg width &mdash; about a Swede turning up on the range in something cut close when "
  "everyone else was swimming in pleated XXXL. The current line is more restrained than that "
  "history, but the shapes are still the sharpest part of the range.", [
  card("mitch-stripe", "Sweden &middot; In stock",
    "A striped technical pant, and the closest thing the current collection has to the old "
    "silhouette. Parnevik put the original version best: &ldquo;I remember the first "
    "pair of pants Johan gave me. They were so tight I could hardly bend over to pick the ball out "
    "of the hole but I shot a 63, so I didn&rsquo;t really care.&rdquo;",
    "J.Lindeberg Mitch stripe pant in JL Navy"),
  card("ellott-pant", "Sweden &middot; In stock",
    "Winetasting turns up again on a pant, and proves the brand still commits to a colour rather "
    "than hedging into grey. A deep red trouser is a harder sell than a red polo, which is probably "
    "why almost nobody else makes one.",
    "J.Lindeberg Ellott pant in Winetasting"),
  card("elof-pant", "Sweden &middot; In stock",
    "The Brindle brown in trouser form at $135, and the piece that gains most from being seen in "
    "person &mdash; the fabric has a dry hand that photographs flat and wears well. A sensible "
    "middle of the range.",
    "J.Lindeberg Elof pant in Brindle"),
  card("mitch-light", "Sweden &middot; In stock",
    "Light poly in Moonbeam, built for heat, and the pant to reach for in an Austin August when "
    "anything heavier stops being a garment and becomes a decision. Pale enough to keep the sun "
    "off, cut narrow enough to stay tidy.",
    "J.Lindeberg Mitch pant light poly in Moonbeam"),
]))

SECTIONS.append(("tees", "The Tees", "OFF-COURSE, MOSTLY",
  "The brand runs a serious tee programme because roughly forty per cent of the business is now "
  "fashion rather than golf, and the tees are where those two halves meet. None of these read as "
  "golf clothing, which is the point &mdash; J.Lindeberg has always argued the clothes should work "
  "before and after the round as well as during it.", [
  card("tee-hale-heavy", "Sweden &middot; In stock",
    "This is heavyweight cotton with the logo worn large, the most streetwear-adjacent thing here. "
    "Black, so it does not announce itself until you are close enough to read it.",
    "J.Lindeberg Hale heavy logo t-shirt in black"),
  card("tee-dennis", "Sweden &middot; In stock",
    "A printed technical tee in a faded purple heather, cut for playing in rather than sitting "
    "around in. The print is loose and washed out rather than graphic, which keeps it on the right "
    "side of merch.",
    "J.Lindeberg Dennis printed t-shirt in clay fade purple heather"),
  card("tee-parcie", "Sweden &middot; In stock",
    "This one is white cotton with the logo small, the plainest thing in the range and the one most likely to "
    "get worn every week, which is usually how it goes.",
    "J.Lindeberg Parcie logo tee in white"),
  card("tee-coma-linen", "Sweden &middot; In stock",
    "This is linen, in Estate Blue, at fifty-eight dollars. This is the piece that has nothing to do with "
    "golf at all and everything to do with why the brand still shows at Copenhagen Fashion Week.",
    "J.Lindeberg Coma linen tee in Estate Blue"),
]))

SECTIONS.append(("shoes", "Shoes and Bags", "THE REST OF THE KIT",
  "Both halves of the brand come through here. The sneakers are the fashion side reasoning about golf "
  "shoes, and the bags are the golf side reasoning about how much a person will pay for one. The "
  "staff bag is the most expensive object J.Lindeberg sells to a man who is not buying outerwear.", [
  card("vent500-blk", "Sweden &middot; In stock",
    "The Vent 500 SE is the spikeless they push hardest, and it is a running-shoe silhouette with a "
    "golf outsole rather than a golf shoe pretending to be a sneaker. Black keeps the panelling "
    "legible without shouting.",
    "J.Lindeberg Vent 500 SE golf sneaker in black"),
  card("ace-lowtop", "Sweden &middot; In stock",
    "Cleaner and lower than the Vent, closer to a court shoe, and white so it will look worse in "
    "three rounds and better in thirty. The pick of the two if you want something that leaves the "
    "course with you.",
    "J.Lindeberg Ace low-top golf sneaker in white"),
  card("staffbag-prime", "Sweden &middot; In stock",
    "Seven hundred and eighty dollars of tour bag, which is what a staff bag costs when a fashion "
    "house makes one. Black, full size, and built to be carried by somebody paid to carry it.",
    "J.Lindeberg Staff Bag Prime in black"),
  card("flare-bag", "Sweden &middot; In stock",
    "This is the one to actually buy &mdash; a colour-blocked carry bag in Set Sail at $300, light enough to walk "
    "with and loud enough to find, and the piece in this section that best reflects the brand's "
    "Scandinavian design line.",
    "J.Lindeberg Flare colour block golf bag in Set Sail"),
]))

HERO = IMGD + "hero-pinkstrategy.jpg"

WRITEUP = """<p>J.Lindeberg is the brand that made golf clothing fit, and it did it by dressing one Swede in
trousers nobody else would wear. The label was founded in <strong>Stockholm in 1996</strong> by
<strong>Johan Lindeberg</strong>, who had spent the first half of the nineties building Diesel &mdash; first as
its distributor in Sweden, later running the American business &mdash; and who arrived in golf with a fashion
marketer's read on a sport that had stopped caring how it looked. Thirty years on, that founding argument has
been so completely absorbed that it is hard to remember it was ever an argument.</p>

<p>The pitch was simple and slightly rude. Golf in the late eighties and early nineties had drifted into
oversized polos, pleated slacks and beige, and Lindeberg thought the game had lost its own history. His
reference points ran backwards rather than forwards &mdash; Walter Hagen's tailored knits, Arnold Palmer's
pullovers, seventies silhouettes, Steve McQueen. He wanted golf to look like it had before it got comfortable.</p>

<p>To prove it he needed a player, and from the mid-nineties he had <strong>Jesper Parnevik</strong>. Parnevik
gives him the credit without hedging: <em>&ldquo;Johan Lindeberg deserves a lot of the credit, though. When he
first approached me, he had this idea to go back to the time when golfers dressed smart.&rdquo;</em> On what
came before, he is blunter &mdash; <em>&ldquo;Something happened in the &rsquo;80s when all the clothes became
XXXL in size, very loose and tacky.&rdquo;</em> And on the first pair of trousers he was handed:
<em>&ldquo;They were so tight I could hardly bend over to pick the ball out of the hole but I shot a 63, so I
didn&rsquo;t really care.&rdquo;</em></p>

<p>The moment everything turned on is precisely dated. <strong>14 May 2000, the GTE Byron Nelson Classic at TPC
Las Colinas.</strong> Parnevik started the final round three shots back, and instead of warming up he changed
his trousers and walked to the first tee in pink. He won on the third playoff hole, beating Davis Love III. The
same day, he reached number seven in the world &mdash; the highest ranking any Swede had held. Lindeberg named
the idea <strong>the Pink Strategy</strong>, and the brand has revived it as the campaign for its thirtieth
year, which is why a pink trouser sits at the top of this page.</p>

<p>One correction, since the two stories get welded together: <strong>the turned-up cap brim was Parnevik's own
invention</strong>, not the brand's. He started flipping it soon after turning pro, in Florida, to get sun on a
pale Swedish face, and kept it because his peripheral vision was clearer, all of which predates the partnership.</p>

<p>The company Johan Lindeberg started is no longer his. He left over clashes with investors, has been in and
out since, and now runs a separate label; his own summary of the exit is <em>&ldquo;I left that boardroom with
nothing. But I stood up for what I believed in.&rdquo;</em> The brand has been owned since 2012 by the people
behind the Danish group Bestseller, and is run from Stockholm by chief executive
<strong>Hans-Christian Meyer</strong>, who is unusually candid about the years in between:
<em>&ldquo;For 10 years, the brand was not that successful and did not make much profit.&rdquo;</em> Revenue
went from $60 million in 2020 to $130 million in 2022, and the business is now roughly sixty per cent sport and
forty per cent fashion, with womenswear past half of sales.</p>

<p>Which brings it to <strong>Viktor Hovland</strong>, who has worn the brand since 2019 and re-signed for three
more years in January 2025. His collection is the honest picture of J.Lindeberg now: quieter than the archive,
built on technical solids, brown and oxblood and navy, with one colour-blocked polo in it that remembers what
this label used to be. Everything below comes from that line, plus the anniversary capsule and a handful of tees.</p>"""

SIDEBAR = [("Founded", "1996, Stockholm"), ("By", "Johan Lindeberg, ex-Diesel"),
           ("Turning point", "Byron Nelson, 14 May 2000"), ("Now worn by", "Viktor Hovland"),
           ("In this edit", "23 pieces, $58 &ndash; $780")]

FAQ = [
 ("Who founded J.Lindeberg and when?",
  "Johan Lindeberg founded the brand in Stockholm in 1996. He had spent the first half of the nineties "
  "building Diesel &mdash; initially as its distributor in Sweden, later running the US business &mdash; before "
  "starting his own label. Golf was part of the concept from the beginning rather than added later."),
 ("What is the Jesper Parnevik connection?",
  "Parnevik was J.Lindeberg's first PGA Tour ambassador, from the mid-nineties. His tailored, close-cut look "
  "stood against the oversized silhouettes of the era and effectively launched the brand in golf. On 14 May "
  "2000 he won the GTE Byron Nelson Classic in pink trousers, beating Davis Love III on the third playoff hole."),
 ("What is the Pink Strategy?",
  "The name Johan Lindeberg gave to the pink-trousers moment at the 2000 Byron Nelson. J.Lindeberg revived it "
  "in June 2026 as the campaign for its thirtieth anniversary, and the 30Y capsule includes an Azalea Pink "
  "golf pant, cap and t-shirt referencing it directly."),
 ("Did J.Lindeberg invent the turned-up cap brim?",
  "No. The flipped brim was Jesper Parnevik's own habit, started shortly after he turned professional in "
  "Florida to get sun on his face, and kept because it improved his peripheral vision. It predates his "
  "partnership with the brand."),
 ("Is Johan Lindeberg still involved with the brand?",
  "No. He left after disagreements with investors, has been in and out of the company over the years, and is "
  "not associated with it now. He has since started a separate label. J.Lindeberg has been owned since 2012 by "
  "the owners of the Danish group Bestseller and is led by chief executive Hans-Christian Meyer."),
 ("Which tour players wear J.Lindeberg?",
  "Viktor Hovland is the headline ambassador, signed since 2019 and extended three years from January 2025. The "
  "roster also includes Matt Wallace, Matthieu Pavon, Niklas N&oslash;rgaard, Kevin Yu, Camilo Villegas, Curtis "
  "Luck, Anna Nordqvist, Yealimi Noh, Morgane Metraux and Mariah Stackhouse. The brand is also the official "
  "apparel partner of USA Golf for the Olympics and clothing supplier to the DP World Tour."),
 ("Is J.Lindeberg only a golf brand?",
  "No. It sells golf alongside ready-to-wear, tailoring, denim, ski and racket sport, and shows at Copenhagen "
  "Fashion Week. As of the last publicly disclosed figures the business ran roughly sixty per cent sport to "
  "forty per cent fashion, with womenswear above half of sales."),
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
              lambda m: m.group(1)+'<a href="/">The Feed</a> &rsaquo; <a href="/drops/">Drops</a> &rsaquo; J.Lindeberg'+m.group(2),
              head, flags=re.S)
head = re.sub(r'(<div class="drop-meta">).*?(</div>)',
              lambda m: m.group(1)+'Drops &amp; Brands &middot; 28 August 2026 &middot; 23 pieces &middot; Stockholm'+m.group(2),
              head, flags=re.S)
head = re.sub(r'(<div class="drop-hero-img">)\s*<img[^>]*>',
              lambda m: m.group(1)+f'<img src="{HERO}" alt="J.Lindeberg&rsquo;s Pink Strategy campaign &mdash; pink cap and pink trousers against a blurred gallery crowd">',
              head, flags=re.S)
head = re.sub(r'(<div class="writeup-body"[^>]*>).*?(</div>)', lambda m: m.group(1)+WRITEUP+m.group(2), head, flags=re.S)
sb = "".join(f'<div class="sidebar-detail"><strong>{k}</strong>{v}</div>' for k, v in SIDEBAR)
head = re.sub(r'(<div class="sidebar-card">).*?(</div>\s*</aside>)',
              lambda m: m.group(1)+'<div class="sidebar-label">The Brand</div>'+sb+m.group(2), head, flags=re.S)
head = re.sub(r'("headline"\s*:\s*")[^"]*(")', lambda m: m.group(1)+"Brand to Know - J.Lindeberg"+m.group(2), head)
for k in ("datePublished", "dateModified"):
    head = re.sub(rf'("{k}"\s*:\s*")[^"]*(")', lambda m: m.group(1)+"2026-08-28"+m.group(2), head)
clean = lambda s: re.sub(r"\s+", " ", re.sub(r"&[a-z]+;|&#\d+;", " ", s)).strip()
faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
    {"@type":"Question","name":clean(q),"acceptedAnswer":{"@type":"Answer","text":clean(a)}} for q,a in FAQ]}
head = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "FAQPage".*?</script>',
              '<script type="application/ld+json">'+json.dumps(faq_ld)+'</script>', head, flags=re.S)

body = []
for anchor, hdr, kicker, lede, cards in SECTIONS:
    body.append(f'<h2 id="{anchor}">{hdr}</h2>')
    body.append(f'<p class="cat-kicker"><strong>{kicker}</strong>{lede}</p>')
    body.append('<div class="products-grid">\n' + "\n".join(cards) + '\n</div>')
faq_html = ('<div class="faq">\n<h2 id="faq">The Story &mdash; FAQ</h2>\n' + "\n".join(
    f'<details class="faq-q"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ) + '\n</div>')
rest = tail[tail.find('<div class="faq">'):] if '<div class="faq">' in tail else tail
rest = re.sub(r'<div class="faq">.*?</div>\s*(?=<section|<div class="more")', faq_html, rest, count=1, flags=re.S)

out = head + '<section class="products">\n' + "\n".join(body) + "\n" + rest
open(OUT, "w", encoding="utf-8").write(out)
print(f"wrote {OUT}")
print(f"sections={len(SECTIONS)} cards={sum(len(s[4]) for s in SECTIONS)} words~{len(re.sub(r'<[^>]+>',' ',out).split())}")
