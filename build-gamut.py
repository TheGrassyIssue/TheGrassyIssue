#!/usr/bin/env python3
"""Brand to Know — Gamut Golf.

NO FOUNDER QUOTE. Research found zero: no named founder, no About page, no
interview in any outlet, no podcast. Lenny's call was to run it on the upcycling
story and quote the PRODUCT COPY, clearly labelled as brand copy, never attributed
to a person.

Deliberately NOT asserted (no source):
  - that Gamut is MLB licensed (it is not; it cuts covers from genuine vintage
    jerseys, incl. licensed 1990s Mirage Cooperstown Collection throwbacks)
  - that any club endorsed the course covers (no partnership discoverable)
  - "made in the USA" (no country of manufacture published anywhere)
  - that OTEY is Otey Crisman, or WILCOX is Willy Wilcox (both plausible, unconfirmed)
  - a founder name (only identifier on the site is a Yahoo address)
  - the Green Sweeper wood species (their own copy contradicts itself)
"""
import re, os, json

SLUG="brand-to-know-gamut-golf"
TITLE="Brand to Know &mdash; Gamut Golf Cuts Headcovers From Vintage Jerseys and Real Course Towels"
PLAIN="Brand to Know — Gamut Golf Cuts Headcovers From Vintage Jerseys and Real Course Towels"
DESC=("Gamut Golf makes one-of-one driver headcovers from authentic vintage baseball jerseys and genuine course towels, "
      "plus $98 square-profile hardwood alignment sticks. Eighteen pieces, and what the catalog actually tells you.")
B="https://gamutgolf.com/products/"

JERSEY=[
 ("cleveland-indians","Cleveland Indians Jersey Cover","cleveland-indians-jersey","$128",
  "Cut from an authentic Cleveland Indians jersey, with a baby blue sherpa inner and semi-structured driver shape. Marked 1/1 &mdash; the jersey it came from was one garment, so this cover cannot be repeated. The retired team name comes with the cloth rather than being a decision anyone made in 2026."),
 ("ny-giants-51","&rsquo;51 NY Giants Cover","51-new-york-giants","$128",
  "Built from an authentic Mirage 1951 New York Giants jersey with a pastel orange sherpa inner. Mirage made officially licensed Cooperstown Collection throwbacks in the 1990s, so the garment underneath was licensed when it was sewn &mdash; this is a second life for it, not a reproduction."),
 ("milwaukee-braves-57","&rsquo;57 Milwaukee Braves Cover","57-milwaukee-braves","$128",
  "The 1957 Braves, the year they won the World Series, in another Mirage Cooperstown throwback with a baby blue sherpa lining. The Braves left Milwaukee in 1965, which is roughly the point of the whole exercise."),
 ("white-sox","White Sox Cover","white-sox","$128",
  "An authentic Chicago White Sox jersey as the outer, sherpa-lined, one of one. The pinstripe runs wherever the pattern happened to fall on the panel they cut."),
 ("pittsburgh-pirates","Pittsburgh Pirates Cover","pittsburgh-pirates","$128",
  "Pirates jersey outer, sherpa inner, 1/1. Of the baseball run this is the one whose colourway reads most like a golf cover already."),
]

TOWEL=[
 ("shinnecock-us-open","Shinnecock Hills U.S. Open Cover","shinnecock-hills-u-s-open","$108",
  "Cut from an authentic Shinnecock Hills U.S. Open towel with a navy cotton felted inner. No club partnership is claimed or discoverable &mdash; the material is genuine merchandise, repurposed."),
 ("pebble-beach","Pebble Beach Cover","pebble-beach","$118",
  "An actual Pebble Beach towel with a cream sherpa liner. The nap of a used course towel gives it a texture no printed cover reproduces."),
 ("st-andrews-old-course","St. Andrews Old Course Cover","st-andrews","$118",
  "Old Course towel, black sherpa inner. The most quietly recognisable object in the range if you know the towel."),
 ("tpc-sawgrass","TPC Sawgrass Cover","pinehurst-no-2-99-u-s-open-copy","$128",
  "Sawgrass towel combined with cowhide suede on the outer, and a leather branded tee holster stitched to the flank. The most constructed of the towel covers."),
 ("pinehurst-no2-99","Pinehurst No. 2 &rsquo;99 U.S. Open Cover","pinehurst-no-2-99-u-s-open","$118",
  "The 1999 U.S. Open at Pinehurst No. 2 &mdash; Payne Stewart&rsquo;s championship &mdash; cut from a towel of that event. The date is the reason this one carries weight."),
 ("muirfield-village","Muirfield Village Cover","muirfield-village","$118",
  "A Muirfield Village towel lined with deadstock Ralph Lauren suit liner. Two salvaged materials in one object, which is the clearest statement of method in the catalog."),
 ("home-of-golf","Home of Golf Cover","tpc-sawgrass-copy","$128",
  "Built from a Scotland&rsquo;s Big 4 towel with cowhide shrunken sueded leather on the outer. Named for the group rather than any single club, which is a neater solution than it first appears."),
]

STICKS=[
 ("alignment-sticks-v3","GG Alignment Sticks V3","gg-sticks-v3","$98",
  "American-grown hickory, 42 inches, a 3/8-inch square profile with six inches of taper. The square section is the functional argument: a round stick rolls off a slope and a square one does not. The current version, and the one usually in stock."),
 ("alignment-sticks-v2","GG Alignment Sticks V2","gg-alignment-sticks-v2","$98",
  "The June 2026 run, in solid shedua &mdash; the African hardwood also sold as etimoe or ovangkol. Same 42-inch square geometry, a darker and more figured grain than the hickory."),
 ("alignment-sticks-v1","GG Alignment Sticks","gg-alignment-sticks-1","$98",
  "The original shedua pair that established the format. Everything since has kept the 42-inch length, the 3/8-inch square section and the six-inch taper, and changed only the species and the finish."),
 ("chain-gang-alignment-sticks","Chain Gang Alignment Sticks","chain-gang-alignment-stick","$98",
  "Solid etimoe, released in March 2026 as part of the five-piece Chain Gang capsule. Same geometry, darkest finish of the run."),
 ("gamut-x-otey","Gamut &times; Otey Alignment Sticks","gamut-x-otey","$98",
  "An August 2026 collaboration edition in American-grown hickory with a green-and-gold decal wrap. Gamut does not identify the collaborator anywhere on the page, and the lettering on the decal is not legible in the product photography."),
 ("green-sweeper","Green Sweeper Series","turbo-alignment-sticks","$98",
  "The June 2025 edition, and the outlier in the range. The listing gives two different hardwoods in two different places, so the species is genuinely unclear from the source; the 42-inch square-profile geometry is the constant."),
]

HARDWARE=[
 ("chain-gang-headcover","Chain Gang Headcover","chain-gang-headcover","$98",
  "Waxed canvas with an ivory sherpa lining. The brand&rsquo;s own copy calls it &ldquo;inspired by the rugged utility of old chain gangs&hellip; cut and sewn as a nod to a harder era, reimagined with intention.&rdquo;"),
 ("shibori","Shibori Cover","shinobi","$108",
  "Hand-dyed in-house using a Japanese-inspired resist technique, which is the only manufacturing step the brand states plainly anywhere. Their line on it: &ldquo;No two are alike, and that&rsquo;s the point.&rdquo;"),
 ("richard-pouch","Richard Pouch","richard-pouch","$88",
  "Genuine suede with a rare deadstock Double RL liner. The copy says it evokes the tool pouches lying around in your grandfather&rsquo;s garage, which is accurate to look at."),
 ("players-divot-tool","The Players Divot Tool","the-players-divot-tool-solid-brass","$69.99",
  "Solid brass, 2 5/8 by 3/4 inches, hand-hammered face. The oldest item still listed &mdash; it dates to July 2024 &mdash; and the one that will outlive everything else here."),
 ("gamut-snapback","Gamut Snapback","gamut-snapback-rope-hat","$42",
  "A rope-front snapback, and one of only three soft goods Gamut makes. The apparel side of the catalog is deliberately tiny: a hat, a tee and a sock."),
 ("azalea-tee","The Azalea Tee","the-azalea-tee","$42",
  "A cotton tee carrying the azalea motif that also appears engraved on the Chain Gang club brush. It arrived alongside that capsule in the spring."),
 ("everyday-sock","Everyday Sock","the-everyday-sock","$22",
  "The cheapest thing Gamut sells and the only one under $38. Currently sold out, which is the default state of most of this catalog."),
]
P = JERSEY + TOWEL + STICKS + HARDWARE

def frames(s):
    n=1
    while os.path.exists(f"images/gamut-golf/{s}-a{n+1}.jpg"): n+=1
    return n

def gal(s,name):
    n=frames(s); pl=re.sub(r'<[^>]+>|&[a-z]+;','',name)
    if n==1:
        return (f'<div class="product-gallery"><div class="pg-track"><div class="pg-frame">'
                f'<img src="/images/gamut-golf/{s}.jpg" alt="Gamut Golf {pl}" loading="lazy" /></div></div></div>')
    fr="".join(f'<div class="pg-frame"><img src="/images/gamut-golf/{s}{"" if i==0 else f"-a{i+1}"}.jpg" '
               f'alt="Gamut Golf {pl} &middot; view {i+1} of {n}" loading="lazy" /></div>' for i in range(n))
    dots="".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" aria-label="View image {i+1}"></button>' for i in range(n))
    return (f'<div class="product-gallery"><div class="pg-track">{fr}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>')

cards="\n    ".join(
 f"""<div class="product-card" data-frames="{frames(s)}">
      {gal(s,n)}
      <div class="product-body">
        <div class="product-brand">Gamut Golf</div>
        <div class="product-name">{n} &middot; {pr}</div>
        <div class="product-desc">{d}</div>
        <a href="{B}{h}" target="_blank" rel="noopener" class="product-link">Shop ↗</a>
      </div>
    </div>""" for s,n,h,pr,d in P)

def sec(hdr,kicker,items):
    c="\n    ".join(
     f"""<div class="product-card" data-frames="{frames(sl)}">
      {gal(sl,nm)}
      <div class="product-body">
        <div class="product-brand">Gamut Golf</div>
        <div class="product-name">{nm} &middot; {pr}</div>
        <div class="product-desc">{d}</div>
        <a href="{B}{h}" target="_blank" rel="noopener" class="product-link">Shop ↗</a>
      </div>
    </div>""" for sl,nm,h,pr,d in items)
    return (f'<section class="products">\n  <h2 class="products-hdr">{hdr}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'  <div class="products-grid">\n    {c}\n  </div>\n</section>\n')


INTRO="""<div class="writeup">
  <div class="writeup-body">
    <p>Gamut Golf makes driver headcovers out of things that already existed. The baseball covers are cut from authentic vintage jerseys, several of them marked 1 of 1. The course covers are cut from genuine course towels &mdash; Shinnecock, Pebble Beach, the Old Course, Sawgrass, Pinehurst. Alongside those sit hardwood alignment sticks at $98, a solid brass divot tool, waxed canvas pouches and a set of walnut brushes.</p>
    <p>The idea is not new &mdash; repurposing salvaged cloth into golf goods has been done before &mdash; but the sourcing is unusually specific. A cover built from a Mirage Cooperstown Collection throwback carries a team name that was retired decades ago, on fabric that was licensed when it was sewn in the 1990s. A Muirfield Village cover is lined with deadstock Ralph Lauren suit liner. The Richard Pouch uses rare deadstock Double RL. Each object is a second life for something, and because the input is finite, most of the interesting pieces are one of one.</p>
    <p>For anyone who has looked at a rack of printed headcovers and wanted something with provenance, this is the catalog to read. It is also small &mdash; 35 products, most of them sold out most of the time.</p>
  </div>
</div>
"""

UPCYCLE="""<section class="products">
  <h2 class="products-hdr">What They Are Actually Made Of</h2>
  <p class="cat-kicker">The product pages are unusually literal about materials, which makes the method easy to follow.</p>
  <div class="writeup-body">
    <p><strong>The jerseys.</strong> Five covers are cut from authentic baseball jerseys: Cleveland Indians, White Sox, Pittsburgh Pirates, and two Mirage Cooperstown Collection throwbacks &mdash; the 1951 New York Giants and the 1957 Milwaukee Braves. Mirage produced officially licensed Cooperstown reissues in the 1990s, so the garments carried licensed marks when they were made. Gamut is cutting finished goods into new ones rather than printing logos, which is a different act entirely. Several are marked 1/1 for the obvious reason: one jersey yields one cover.</p>
    <p><strong>The towels.</strong> Seven covers are built from real course towels. Shinnecock Hills U.S. Open with a navy cotton felted inner. Pebble Beach with cream sherpa. The Old Course with black sherpa. Sawgrass paired with cowhide suede and a leather tee holster. Pinehurst No. 2 from the 1999 U.S. Open. Muirfield Village with that deadstock Ralph Lauren lining. The seventh, Home of Golf, is cut from a Scotland&rsquo;s Big 4 towel and named for the group rather than a single club. No club partnership is stated on any of them, and none is discoverable &mdash; the material is genuine merchandise given a second use.</p>
    <p><strong>The sticks.</strong> The alignment sticks are the other half of the business and the reason to look past the covers. Every version runs 42 inches with a 3/8-inch square profile and six inches of taper. The square section is the whole argument for spending $98 on something available in fiberglass for twenty: a square stick stays where it is laid on a sloping range mat. Species rotate &mdash; American-grown hickory on the V3 and the Otey edition, solid etimoe on the Chain Gang run, shedua on the earlier versions. Etimoe and shedua are trade names for the same African hardwood, so the variety is narrower than the naming suggests.</p>
  </div>
</section>
"""

CONTEXT="""<section class="products">
  <h2 class="products-hdr">What the Catalog Tells You</h2>
  <p class="cat-kicker">Gamut has never given an interview, so the products are the only record.</p>
  <div class="writeup-body">
    <p>There is no About page. No founder is named anywhere on the site, no publication has interviewed them, and the only personal identifier in the entire web presence is an email address in the returns policy. The Terms of Service still carries the unfilled Shopify template fields where a trading name and business address should be. That is not a criticism so much as a description of scale: this is a very small operation that has spent its effort on product rather than on the page that explains the product.</p>
    <p>What can be dated is the output. The web presence begins in November 2023 and the oldest item still listed, the brass divot tool, dates to July 2024. Twenty-eight of the thirty-five current products were published in 2026, so the pace has increased sharply. The five-piece Chain Gang capsule &mdash; sticks, headcover, club brush, pocket brush and pouch, in waxed canvas and hardwood &mdash; landed in one drop in late March 2026, the week before the Masters. The club brush in that set is engraved with a single azalea.</p>
    <p>The tagline has moved from &ldquo;A Life Aligned&rdquo; to &ldquo;Know Your Line.&rdquo; Two recurring lines in the product copy do the work an About page would: &ldquo;Built to last, made to age,&rdquo; and, on the waxed canvas, &ldquo;the waxed canvas will wear in, not out.&rdquo; Both are brand copy rather than anyone&rsquo;s quote, but they describe the catalog accurately.</p>
    <p>Stock is the practical caveat. Most of the covers are single-garment builds, so the majority of the range is sold out at any given moment, and a piece that sells is generally gone rather than restocked.</p>
  </div>
</section>
"""

FAQ_ITEMS=[
 ("Are the baseball headcovers officially licensed?",
  "No, and they do not need to be. Gamut cuts them from authentic vintage jerseys it has sourced secondhand, including 1990s Mirage Cooperstown Collection throwbacks that were officially licensed when they were manufactured. The covers are upcycled finished garments, not new products bearing printed team marks."),
 ("Are the course covers made with the clubs?",
  "No club partnership is stated by Gamut or discoverable elsewhere. The covers are cut from genuine course towels &mdash; real merchandise, repurposed. The Home of Golf cover sidesteps the question by being named for Scotland&rsquo;s Big 4 rather than one club."),
 ("Why do the alignment sticks cost $98?",
  "They are hardwood rather than fiberglass &mdash; hickory, etimoe or shedua depending on the run &mdash; and they use a 3/8-inch square profile over 42 inches with a six-inch taper. The square section is the point: it will not roll away on a sloping mat."),
 ("What is the Chain Gang collection?",
  "A five-piece capsule released in one drop in March 2026: alignment sticks in etimoe, a waxed canvas headcover, a walnut club brush, a hickory pocket brush and a waxed canvas pouch lined in Turkish herringbone wool. The brand says it is &ldquo;inspired by the rugged utility of old chain gangs.&rdquo;"),
 ("Is Gamut Golf independent?",
  "Every available signal says yes &mdash; no parent company, no funding announcement, no corporate footprint, and a catalog of one-of-one pieces that sells out and stays out. No outside investment is disclosed."),
]
FAQ="""<section class="products">
  <h2 class="products-hdr">The Questions</h2>
  <div class="faq">
"""+"\n".join(f'    <div class="faq-q">{q}</div>\n    <div class="faq-a">{a}</div>' for q,a in FAQ_ITEMS)+"""
  </div>
</section>
"""
def st(s): return (re.sub(r'<[^>]+>','',s).replace("&ldquo;",'"').replace("&rdquo;",'"')
                   .replace("&rsquo;","'").replace("&amp;","&").replace("&mdash;","—").replace("&hellip;","..."))
SCHEMA={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
 {"@type":"Question","name":st(q),"acceptedAnswer":{"@type":"Answer","text":st(a)}} for q,a in FAQ_ITEMS]}

model=open("drops/students-golf-summer-2026.html",encoding="utf-8").read()
head=model[:model.find('<div class="breadcrumb">')]
tail=model[model.find('<section class="more"'):]
head=re.sub(r'<title>[^<]*</title>',f'<title>{PLAIN} — The Grassy Issue</title>',head)
for k,v in [("description",DESC),("og:title",PLAIN),("og:description",DESC)]:
    head=re.sub(rf'(<meta (?:name|property)="{re.escape(k)}" content=")[^"]*(")',lambda m:m.group(1)+v+m.group(2),head)
head=re.sub(r'(<link rel="canonical" href=")[^"]*(")',lambda m:m.group(1)+f"https://thegrassyissue.com/drops/{SLUG}"+m.group(2),head)
head=re.sub(r'(<meta property="og:url" content=")[^"]*(")',lambda m:m.group(1)+f"https://thegrassyissue.com/drops/{SLUG}"+m.group(2),head)
head=re.sub(r'(<meta property="og:image" content=")[^"]*(")',lambda m:m.group(1)+"https://thegrassyissue.com/images/gamut-golf/hero.jpg"+m.group(2),head)
_sb='<script type="application/ld+json">'+json.dumps(SCHEMA)+'</script>'
head=re.sub(r'<script type="application/ld\+json">.*?</script>',lambda m:_sb,head,flags=re.S)

body=('<div class="breadcrumb">\n  <a href="/">Feed</a><span>/</span>\n  <a href="/#feed">Drops &amp; Brands</a><span>/</span>\n  Gamut Golf</div>\n'
 f'<header class="drop-header">\n  <h1>{TITLE}</h1>\n  <div class="drop-meta">\n'
 '    <span>September 6, 2026</span><span class="dot"></span>\n    <span>Brand to Know</span><span class="dot"></span>\n'
 '    <span>25 of 35 Pieces</span>\n  </div>\n</header>\n\n'
 '<div class="drop-hero"><div class="drop-hero-img"><img src="/images/gamut-golf/hero.jpg" '
 'alt="A golfer walking up to a green framed by mature trees, from Gamut Golf&#39;s own course photography" /></div></div>\n'
 +INTRO+UPCYCLE
 +sec("The Jersey Covers &mdash; 5 Pieces","Each one cut from a single authentic jersey, so each one is the only one.",JERSEY)
 +sec("The Towel Covers &mdash; 7 Pieces","Built from genuine course towels. No club partnership is claimed on any of them.",TOWEL)
 +sec("The Alignment Sticks &mdash; 6 Editions","Every version runs 42 inches with a 3/8-inch square profile and a six-inch taper. Only the species changes.",STICKS)
 +sec("Hardware and Apparel &mdash; 7 Pieces","Brushes, a brass divot tool, a pouch, and the three soft goods that make up the whole apparel line.",HARDWARE)
 +CONTEXT+FAQ)

open(f"drops/{SLUG}.html","w",encoding="utf-8").write(head+body+tail)
print(f"wrote drops/{SLUG}.html | {len(P)} products | ~{len(re.sub(r'<[^>]+>',' ',head+body+tail).split())} words")
