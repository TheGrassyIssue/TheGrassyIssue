#!/usr/bin/env python3
"""Build /drops/texas-golf-brands-and-makers.html from the LOF template + /tmp/tx/man.json.

House format (see memory reference_post_format):
  <h2 id> + <p class="cat-kicker"> + <div class="products-grid"> wrapping every .product-card.
The FAQ <div> lives INSIDE the single products <section>; cut the template at
`<div class="faq">` and leave the last section OPEN — the template's </section> closes it.
"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
MAN  = json.load(open("/tmp/tx/man.json"))
TPL  = os.path.join(ROOT, "drops", "brand-to-know-left-of-field-golf.html")
OUT  = os.path.join(ROOT, "drops", "texas-golf-brands-and-makers.html")
SLUG = "texas-golf-brands-and-makers"
TITLE = ("Made in Texas &mdash; The Golf Brands and Makers Built Here")
TITLE_TXT = "Made in Texas — The Golf Brands and Makers Built Here"
DESC = ("Sixteen golf brands founded and based in Texas — Fort Worth forges, Dallas shirt makers, "
        "Hill Country silversmiths and Austin knitters. Who they are, what they make and where.")

# ---------------------------------------------------------------- copy
# Every fact below traces to the brand's own site or a named publication.
# NOT PUBLISHED items (founding years for Chipp, Kingfisher, Lamb, Ally Aiken,
# AustinKnittyLimits) are deliberately absent — do not add them.
CARDS = {
"artisan": dict(
  city="Fort Worth", meta="Est. 2017",
  desc="Mike Taylor and John Hatfield left the Nike payroll on a Friday in February 2017 and "
       "opened the doors of the same building the following Monday &mdash; the ten-thousand-square-foot "
       "shop Nike had used to build golf clubs. Taylor was Nike&rsquo;s model maker for irons and wedges; "
       "Hatfield built putters. Taylor still grinds every wedge himself, and you cannot order one without "
       "coming to Fort Worth to be fitted. The banner across their site is not marketing: proudly made in Fort Worth."),
"p53": dict(
  city="Fort Worth", meta="Founded by Christopher Griffin",
  desc="Named for Ben Hogan&rsquo;s 1953 season, the year he won three of the four. Griffin left Microsoft "
       "in 2012 to build it and leases space at Leonard Golf Links &mdash; the old Nike building &mdash; from "
       "Marty Leonard, whose father founded Colonial. Every iron starts as a single billet of certified American "
       "steel, struck at around 2,100&deg;F under a gravity hammer, then machined, ground and finished in house. "
       "Admitted by invitation only, in their own words."),
"piretti": dict(
  city="Spring", meta="Est. 2008",
  desc="Mike Johnson designs every head and every one is milled from a solid billet &mdash; there is no cast putter "
       "in the line and never has been. His two quiet arguments with the rest of the industry: heads run fifteen to forty-five grams "
       "heavier than standard, and loft is specced at 2.5 degrees because greens are cut shorter than they used "
       "to be. Made and crafted in the United States, out of a shop on Stuebner Airline Road north of Houston."),
"edison": dict(
  city="Rockport", meta="Est. 2018",
  desc="Terry Koehler has been designing wedges longer than most brands have existed &mdash; EIDOLON, which put "
       "the first CNC-milled grooves in a production wedge, then SCOR, then the Ben Hogan relaunch. Edison is the "
       "distillation. The patented Koehler Sole puts high and low bounce in the same head so one wedge covers more "
       "lies. In 2021 he moved the whole operation &mdash; design, assembly, shipping &mdash; to the Gulf Coast at Rockport."),
"lamb": dict(
  city="Plano", meta="Family-owned machine shop",
  desc="Tyson Lamb started in his mother&rsquo;s garage north of Dallas and the shop in Plano still runs on six "
       "employees. Their own description is the least romantic and the most accurate: a family owned Texas based "
       "machine shop. Putters are the headline, but the engraving is the signature &mdash; it turns up on ball "
       "markers, divot tools, and the leather. American made in large volumes, which for a six-person shop means "
       "something different than it does elsewhere."),

"criquet": dict(
  city="Austin", meta="Est. 2010",
  desc="Hobson Brown and Billy Nachman founded Criquet in Austin in 2010, and the Players Shirt is still the whole "
       "argument: a soft, unfussy, slightly retro polo for people who did not want to dress like a tour caddie. The "
       "Top-Shelf runs 92 percent Pima cotton with removable collar stays. Designed at the Clubhouse in Austin and "
       "made in Peru &mdash; they print that on the product page rather than hiding it."),
"olydoe": dict(
  city="Dallas", meta="Launched October 2025",
  desc="Scott Matthews quit investment banking in New York because he could not find a cotton polo he wanted to "
       "play golf in, moved to Dallas, and started a brand on what he calls an anti-polyester manifesto. Everything "
       "is Supima cotton with hollow-core yarn &mdash; the performance without the plastic hand. The star in the logo "
       "is two stars, one from the Chicago flag and one from the Texas flag &mdash; he started playing on a nine-hole "
       "course in rural Illinois, grew into the game in Chicago, and landed in Dallas."),
"sierramadre": dict(
  city="Austin", meta="Founded by Bonny Riddle &amp; Michelle Anderson",
  desc="Women&rsquo;s golf clothing designed by two women who play, which shows up in the details rather than the "
       "silhouettes: built-in bras, pockets that actually hold something, and an elastic loop on the All Square Skort "
       "for your glove. The skort is Peruvian cotton; the Bad Madres bucket hat has its patch hand-stitched on in "
       "Austin. Now stocked in select Golf Galaxy stores, which for a six-year-old brand is a real signal."),
"juniperjames": dict(
  city="New Braunfels", meta="Launched July 2025",
  desc="The newest brand here by some distance. James Elledge named it after his twin daughter and son and brought "
       "over what he learned starting Duck Camp, the Texas hunting and fishing label &mdash; specifically, how "
       "breathable fabric is supposed to work. The Comfort Polo is 48 percent Lenzing micro modal and 47 percent "
       "polyester &mdash; they list it on the page, which is the standard we are asking for &mdash; cut with a spread "
       "dress collar and mother-of-pearl buttons. Home courses listed on the site: Landa Park, Kissing Tree, The Quarry."),
"kingfisher": dict(
  city="Dallas", meta="Founded by Fiona Cohen",
  desc="Cohen was an art director at PepsiCo before this, and Kingfisher began at her kitchen counter in East "
       "Dallas with a sewing machine and a pile of thrift-store fabric. The brand sits in the overlap of her design "
       "background and her brother&rsquo;s golf habit. Not in a pro shop yet, by their own admission. They ran a "
       "Worst Golfer in Dallas contest and signed the winner as their first sponsored athlete, which tells you the tone."),

"bestgrips": dict(
  city="Conroe", meta="First grips shipped 2010",
  desc="A father and son, Harry and Zach, making leather grips in Conroe. The origin is on their own "
       "site and it earns the space: Harry&rsquo;s father Bud took up golf while recovering from losing a leg in a plane crash, and the two "
       "of them ran the East Texas Amputee Golf Tournament. The line runs from the extra-tacky MicroPerf to Horween "
       "Dublin leathers, custom stitch colours, no minimum order, and a stated policy of no paid endorsements."),
"chipp": dict(
  city="Dallas", meta="Founded by Randall Pulfer &amp; Tyler Lane",
  desc="Two college roommates who met at Wisconsin&ndash;Madison, asked why golf gloves are so boring, and started answering it "
       "in Dallas during the pandemic. Premium cabretta leather, perforated on both sides of every finger, with a "
       "reinforced palm. The structure is the interesting part: ten percent of every glove goes to a charitable "
       "partner, and many of the designs are drawn from that partner&rsquo;s mission. The first two were Feelin&rsquo; Lucky "
       "and Texas Hole&rsquo;em."),
"clintorms": dict(
  city="Kerrville", meta="Est. 1992",
  desc="Orms began engraving in Dallas in 1992, moved to Houston, then to the Hill Country, and now works from a "
       "showroom on Water Street in Kerrville, with the bench still out in Ingram. He started out polishing for the "
       "sculptor and saddle maker Buck Brumley, then apprenticed under four silver designers across the West. His buckles are "
       "named for Texas counties &mdash; Bexar, Pecos, Duval &mdash; and he will not reproduce more than ten pieces "
       "from any one design. The ball markers are solid sterling and gold, hand-engraved. Ben Crenshaw is a client."),

"knitty": dict(
  city="Austin", meta="Hand-knit, one at a time",
  desc="Maggie knits headcovers, and the reason she knows how is that her mother taught her. The first set she made "
       "was a Father&rsquo;s Day present for her golf-loving father, in University of Maryland colours. What she sells "
       "now is the retro striped driver-and-fairway kind with a tassel or a pom on top, sets of three at around ninety-five "
       "dollars, putter covers for thirty-five. Her tagline is where every stitch tells a story, and it is not a slogan "
       "so much as an accurate description of the business."),
"allyaiken": dict(
  city="Austin", meta="First course painted 2020",
  desc="Ally Aiken is a watercolour artist and graphic designer in Austin. Her older sister gave her a watercolour "
       "set and calligraphy tools one Christmas; in 2020 she painted her first golf course map as a gift for her "
       "husband Campbell and has not stopped since. The catalogue now runs to hundreds of courses, including Roy "
       "Kizer and Onion Creek here in Austin, Brook Hollow and Dallas Athletic Club up in Dallas. Commissions and "
       "wholesale both open."),

"edel": dict(
  city="Austin", meta="Founded by David Edel",
  desc="David Edel built the brand around the idea that a putter should be fitted like a set of irons &mdash; that "
       "head shape, shaft lean and sightline change where you aim before you have moved a muscle. The build is still "
       "done here and they say so on the product page: The Brick is milled in the USA from premium stainless and "
       "hand-finished in Austin, and the E-T01 is machined from carbon steel then hand-painted, polished and assembled "
       "in Austin. Each head is individually finished by their own craftsmen."),
}

SECTIONS = [
 ("forges", "The Forges",
  "Clubs &middot; Fort Worth, Spring, Rockport, Austin, Plano",
  "Texas builds golf clubs for a specific and unromantic reason: Nike used to build them here, and when Nike "
  "left the equipment business in 2016 it left behind a building in Fort Worth and a group of people who knew "
  "how to grind a wedge. Two of the shops below occupy that building&rsquo;s footprint. The other two got here "
  "on their own. What they share is that a named person touches the club before it ships.",
  ["artisan","p53","piretti","edison","edel","lamb"]),

 ("shirts", "The Shirt Makers",
  "Apparel &middot; Austin, Dallas, New Braunfels",
  "Golf apparel is the easiest category to start a brand in and the hardest to stay in, which is why this group "
  "spans fifteen years &mdash; Criquet has been at it since 2010, Juniper &amp; James launched last summer. Let us "
  "be plain about it: most of what follows is designed in Texas and sewn somewhere else, and the good ones say so "
  "on the product page. We have flagged it either way.",
  ["criquet","olydoe","sierramadre","juniperjames","kingfisher"]),

 ("leather", "Leather, Silver and Grip",
  "Accessories &middot; Conroe, Dallas, Kerrville",
  "The part of the game you actually hold. Two of these three are hand-work in the literal sense &mdash; a "
  "silversmith engraving a marker, a father and son wrapping a grip &mdash; and all three are small enough that "
  "an order goes past a person rather than a system.",
  ["bestgrips","chipp","clintorms"]),

 ("makers", "One at a Time",
  "Makers &middot; Austin",
  "Not brands so much as two people making things by hand and selling them. Both started as a gift for a family "
  "member, which is how a surprising amount of this ends up beginning.",
  ["knitty","allyaiken"]),
]

FAQS = [
 ("What golf brands are made in Texas?",
  "Several, and in more categories than people expect. Clubs and metal: Artisan Golf and P53 in Fort Worth, "
  "Piretti in Spring, Edison Golf in Rockport, Lamb Crafted in Plano. Leather and silver: BestGrips in Conroe, "
  "Chipp Golf Co in Dallas, Clint Orms in Kerrville. Apparel: Criquet and Sierra Madre in Austin, Olydoe and "
  "Kingfisher in Dallas, Juniper &amp; James in New Braunfels. Individual makers: AustinKnittyLimits and Ally "
  "Aiken Design, both in Austin."),
 ("Why are so many golf club makers based in Fort Worth?",
  "Because Nike was. Nike built its golf clubs in a facility in Fort Worth and exited the equipment business in "
  "2016, which released a building and a group of experienced club builders into the same city. Artisan Golf was "
  "founded by two former Nike craftsmen, Mike Taylor and John Hatfield, in February 2017 and works out of the "
  "former Nike golf club facility. P53&rsquo;s Christopher Griffin leases space at Leonard Golf Links, in the "
  "building Nike used, from Marty Leonard &mdash; daughter of Marvin Leonard, who founded Colonial."),
 ("Which of these brands actually manufacture in Texas?",
  "Artisan grinds and finishes every club in Fort Worth. Edel hand-finishes its putters in Austin. P53 forges in the Pacific Northwest but does all "
  "machining, grinding and finishing in Fort Worth. Piretti mills in the United States. Lamb Crafted machines in "
  "Plano. BestGrips states designed and made in Texas. Clint Orms engraves by hand in Texas. On the apparel side "
  "it is mostly design here, sewing elsewhere &mdash; Criquet prints made in Peru on the Top-Shelf Players Shirt, "
  "and Sierra Madre&rsquo;s All Square Skort is Peruvian cotton."),
 ("Who founded Artisan Golf?",
  "Mike Taylor and John Hatfield, both former Nike employees. Hatfield has given the exact date: February 17, "
  "2017 was their last day on the Nike payroll, and on Monday February 20 they walked in the same door and "
  "started Artisan. Taylor was Nike&rsquo;s model maker for irons and wedges; Hatfield built putters. Wedges "
  "are ground by Taylor personally and can only be ordered after an in-person fitting in Fort Worth."),
 ("What does P53 stand for?",
  "Ben Hogan&rsquo;s 1953 season. Hogan won the Masters, the U.S. Open and the Open Championship that year, and "
  "the Fort Worth connection is direct &mdash; Hogan is the city&rsquo;s golfing patron saint. Founder "
  "Christopher Griffin left Microsoft in 2012 to start the company. Irons are sold privately, each client is "
  "invited to Fort Worth to be fitted in person."),
 ("Where are Edel putters made?",
  "In Austin. Edel&rsquo;s own product pages state it plainly: The Brick is precision-milled in the U.S.A. from "
  "premium stainless steel and hand-finished in Austin, Texas, and the E-T01 is machined in the U.S.A. from premium "
  "carbon steel then hand-painted and assembled in Austin. Their wording is that each head is individually painted, "
  "polished and built by their master craftsmen. The brand was founded by David Edel and is known for fitting "
  "putters the way most fitters approach irons."),
 ("Where can I buy Texas-made golf headcovers?",
  "AustinKnittyLimits hand-knits retro striped driver and fairway wood covers in Austin, sold in sets of three "
  "for around ninety-five dollars with putter covers at about thirty-five. Lamb Crafted in Plano makes leather "
  "headcovers alongside its putters and engraved accessories. Both are small operations, so stock moves and "
  "custom work is usually possible if you ask."),
 ("Which Texas brand makes custom ball markers?",
  "Clint Orms Engravers &amp; Silversmiths, now on Water Street in Kerrville. Orms started the business in Dallas "
  "in 1992, moved to Houston, and settled in the Hill Country. Everything is solid sterling silver and gold, "
  "hand-engraved, and he holds a rule of never reproducing more than ten pieces from a single design. His buckles "
  "are named after Texas counties and his client list includes Ben Crenshaw and Nolan Ryan."),
 ("Are there Texas golf brands making womens apparel?",
  "Sierra Madre Golf in Austin, founded by Bonny Riddle and Michelle Anderson, is the most established &mdash; "
  "built-in bras, functional pockets, and an elastic glove loop on the All Square Skort, now stocked in select "
  "Golf Galaxy locations. Kingfisher Golf in Dallas, founded by Fiona Cohen, is newer and smaller, and started "
  "on a kitchen counter in East Dallas with a sewing machine and thrift-store fabric."),
 ("What is the best Texas golf brand to start with?",
  "It depends what you want. For a shirt you will wear off the course, Criquet&rsquo;s Players Shirt is the "
  "obvious first purchase and has been for sixteen years. For something you will keep, a Clint Orms sterling "
  "ball marker or a set of BestGrips leather grips will outlast most of your bag. For clubs, Artisan is the "
  "one you travel for &mdash; but you have to go to Fort Worth to be fitted, so treat it as a trip rather than "
  "a transaction."),
]

# ---------------------------------------------------------------- build
h = open(TPL, encoding="utf-8").read()
head = h[:h.index('<div class="faq">')]
_i = h.index('<div class="faq">'); _d = 0
for _m in re.finditer(r"<div\b|</div>", h[_i:]):
    _d += 1 if _m.group(0) != "</div>" else -1
    if _d == 0: TAIL = h[_i + _m.end():]; break
else: raise SystemExit("could not find close of faq div")

def gallery(key, alt):
    fr = MAN[key]["frames"]; n = len(fr)
    t = "".join('<div class="pg-frame"><img src="/images/texas-brands/%s" loading="lazy" alt="%s"></div>'
                % (f, alt) for f in fr)
    g = '<div class="product-gallery"><div class="pg-track">%s</div>' % t
    if n >= 2:
        g += ('<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
              '<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
              '<span class="pg-count">1/%d</span><div class="pg-dots">%s</div>'
              % (n, "".join('<button class="pg-dot%s" data-i="%d" aria-label="View image %d"></button>'
                            % (" on" if i == 0 else "", i, i + 1) for i in range(n))))
    return g + "</div>", n

def card(key):
    c = CARDS[key]; m = MAN[key]; name = m["name"]
    g, n = gallery(key, "%s golf, %s Texas" % (name, c["city"].replace("&amp;", "and")))
    return ('  <div class="product-card" data-frames="%d">\n    %s\n'
            '      <div class="product-body">\n'
            '        <div class="product-brand">%s</div>\n'
            '        <div class="product-name">%s &middot; %s</div>\n'
            '        <div class="product-desc">%s</div>\n'
            '        <a href="https://%s" target="_blank" rel="noopener" class="product-link">Visit &#8599;</a>\n'
            '      </div>\n  </div>\n' % (n, g, c["city"] if c.get("loc_raw") else c["city"] + ", Texas",
   name, c["meta"], c["desc"], m["dom"]))

body = []
for sid, sh2, kick_lead, kick_body, keys in SECTIONS:
    body.append('<h2 id="%s">%s</h2>' % (sid, sh2))
    body.append('<p class="cat-kicker"><strong>%s</strong>%s</p>' % (kick_lead, kick_body))
    body.append('<div class="products-grid">')
    body += [card(k) for k in keys]
    body.append('</div>')
BODY = "\n".join(body)

FAQ_HTML = ('<div class="faq">\n' + "\n".join(
    '    <details class="faq-q"><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in FAQS)
    + "\n  </div>" + TAIL)

page = head + FAQ_HTML
page = page[:page.index('<section class="products">') + len('<section class="products">')] \
       + "\n" + BODY + "\n" + page[page.index('<div class="faq">'):]

# ---- head surgery -------------------------------------------------
def sub1(pat, rep, s, label):
    s2, n = re.subn(pat, rep, s, count=1, flags=re.S)
    assert n == 1, "head surgery failed: " + label
    return s2

page = sub1(r'<title>.*?</title>', '<title>%s | The Grassy Issue</title>' % TITLE_TXT, page, "title")
page = sub1(r'<meta name="description" content="[^"]*"',
            '<meta name="description" content="%s"' % DESC, page, "description")
page = re.sub(r'(<meta property="og:title" content=")[^"]*(")', r'\g<1>%s\g<2>' % TITLE_TXT, page)
page = re.sub(r'(<meta property="og:description" content=")[^"]*(")', r'\g<1>%s\g<2>' % DESC, page)
page = re.sub(r'(<meta name="twitter:title" content=")[^"]*(")', r'\g<1>%s\g<2>' % TITLE_TXT, page)
page = re.sub(r'(<meta name="twitter:description" content=")[^"]*(")', r'\g<1>%s\g<2>' % DESC, page)
page = re.sub(r'(https://thegrassyissue\.com/drops/)brand-to-know-left-of-field-golf',
              r'\g<1>%s' % SLUG, page)
page = sub1(r'<h1>.*?</h1>', '<h1>%s</h1>' % TITLE, page, "h1")
page = sub1(r'(<div class="breadcrumb">.*?<span>/</span>\s*)[^<]*(\s*</div>)',
            r'\g<1>' + TITLE_TXT + r'\g<2>', page, "breadcrumb")
page = sub1(r'<div class="drop-meta">.*?</div>',
            '<div class="drop-meta">\n    <span>16 Brands</span>\n  </div>', page, "drop-meta")
page = sub1(r'<div class="drop-hero">.*?</div></div>',
            '<div class="drop-hero"><div class="drop-hero-img">'
            '<img src="/images/texas-brands/hero-texas-brands.jpg" '
            'alt="A Texas club maker grinding a forged wedge head" /></div></div>', page, "hero")

# sidebar
page = sub1(r'<div class="sidebar-detail"><span class="l">Pieces</span>.*?<span class="l">Range</span><span>[^<]*</span></div>',
  '<div class="sidebar-detail"><span class="l">Brands</span><span>16</span></div>\n'
  '      <div class="sidebar-detail"><span class="l">Categories</span><span>4</span></div>\n'
  '      <div class="sidebar-detail"><span class="l">Cities</span><span>9</span></div>\n'
  '      <div class="sidebar-detail"><span class="l">Oldest</span><span>1992</span></div>', page, "sidebar")
page = sub1(r'<span class="hashtag">#LeftOfFieldGolf</span>',
            '<span class="hashtag">#MadeInTexas</span>', page, "hashtag")
page = page.replace('<span class="hashtag">#GearEdit</span>',
                    '<span class="hashtag">#TexasGolf</span>')

# ---- intro writeup -------------------------------------------------
INTRO = """
    <p>The test for this list was narrow on purpose: founded in Texas, and still based in Texas. No brands that
    put a longhorn on a hat from an office in California. No companies that opened a Dallas warehouse and started
    calling themselves Texan. Founded here, run from here.</p>
    <p>Sixteen cleared it, and the surprise is how little any of them have in common. There is a silversmith in Kerrville
    who has been hand-engraving since 1992 and will not make more than ten of anything. There is a woman in Austin
    who painted a golf course for her husband in 2020 and now has hundreds in the catalogue. There is a father and
    son in Conroe wrapping leather grips, an investment banker who quit New York for Dallas over a polyester polo,
    and two men in Fort Worth who walked out of Nike on a Friday and opened their own shop in the same building on
    the Monday.</p>
    <p>That last one is the closest thing to a pattern. When Nike left the golf equipment business in 2016 it left
    a building in Fort Worth and a group of people who knew how to grind a wedge, and two of the best club shops
    in the country grew out of the vacancy. Ben Hogan is buried in that city. Marvin Leonard built Colonial there.
    It is not an accident that the metal work clusters where it does.</p>
    <p>A note on honesty, because it matters in the apparel section: designed in Texas and made in Texas are not
    the same claim, and we have not blurred them. Criquet prints <em>made in Peru</em> on the Players Shirt. Artisan
    prints <em>made in Fort Worth</em> on the building. Both are fine. Pretending they are the same thing is not.</p>
"""
page = sub1(r'(<div class="writeup-body">).*?(\s*</div>)', lambda m: m.group(1) + INTRO + m.group(2),
            page, "intro")

# ---- JSON-LD -------------------------------------------------------
def jld(o): return json.dumps(o, ensure_ascii=False)
lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S)
art = jld({"@context":"https://schema.org","@type":"Article","headline":TITLE_TXT,
  "description":DESC,"author":{"@type":"Organization","name":"The Grassy Issue"},
  "publisher":{"@type":"Organization","name":"The Grassy Issue"},
  "datePublished":"2026-08-21","dateModified":"2026-08-21",
  "mainEntityOfPage":"https://thegrassyissue.com/drops/%s" % SLUG})
faq = jld({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":re.sub(r'&[a-z]+;','',q),
   "acceptedAnswer":{"@type":"Answer","text":re.sub(r'&mdash;','—',re.sub(r'&rsquo;','’',
     re.sub(r'&amp;','&',a)))}} for q,a in FAQS]})
page = re.sub(r'<script type="application/ld\+json">.*?</script>',
              '<script type="application/ld+json">%s</script>' % art.replace("\\", "\\\\"),
              page, count=1, flags=re.S)
# replace the LAST ld+json (the FAQ block)
last = page.rfind('<script type="application/ld+json">')
end = page.index('</script>', last) + len('</script>')
page = page[:last] + '<script type="application/ld+json">%s</script>' % faq + page[end:]

open(OUT, "w", encoding="utf-8").write(page)
print("wrote", OUT, len(page), "bytes")
print("cards:", page.count('<div class="product-card'), " grids:", page.count('<div class="products-grid">'))

# --- house voice guard -------------------------------------------------------
# Card copy and section kickers are owned by data/copy-deck.json, not by this
# script (see VOICE.md). Re-applying the deck here means a rebuild can never
# silently restore the pre-2026-08-27 copy. Safe to run repeatedly.
import subprocess as _sp, os as _os
_sp.run(["python3", _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "copy-deck.py"),
         "apply"], check=False)
