#!/usr/bin/env python3
"""Brand to Know — Bluegrass Fairway. Built on the Students Golf chassis.

All founder quotes are verbatim and DATED: the only two published interviews are
GolfWRX (2017-10-13) and Etsy Journal (2017-05-18). There is no founder interview
after 2017, so every quote carries its year in the copy.

Deliberately NOT asserted (research found no source):
  - that "Single Barrel" is a bourbon reference (implied by 1-of-1 + colourway
    names, never stated by the brand)
  - where the Vintage Pro Shop stock is sourced
  - why Harris Tweed / Pendleton were chosen
"""
import re, os, json

SLUG="brand-to-know-bluegrass-fairway"
TITLE="Brand to Know &mdash; Bluegrass Fairway, the Louisville Shop That Started at a Cobbler&rsquo;s Bench"
PLAIN="Brand to Know — Bluegrass Fairway, the Louisville Shop That Started at a Cobbler's Bench"
DESC=("Bluegrass Fairway makes handmade leather, Harris Tweed and waxed canvas golf goods in Louisville, Kentucky. "
      "Founder Matt Reynolds, the Single Barrel one-offs, the Steurer & Co. collaboration, and 18 pieces from the catalog.")
BASE="https://www.bluegrassfairway.com/products/"

P=[
 ("field-hunter-green","The Field &mdash; Hunter Green &amp; Cream Leather","Fairway Headcover &middot; $115","the-field-hunter-green-cream-leather-golf-headcover-handmade-driver-fairway-hybrid-cover",
  "The Field runs full-grain leather in hunter green over a cream underside, with a contrast stripe on the diagonal. The number sits proud on the crown rather than printed flat. It is the most photographed thing they make, and the one that reads as a Bluegrass Fairway cover from across a car park."),
 ("field-saddle-tan","The Field &mdash; Saddle Tan Leather","Fairway Headcover &middot; $115","the-field-saddle-tan-leather-golf-headcover",
  "The same Field pattern in saddle tan, which is the version that ages most visibly. Leather this light picks up the bag, the boot of the car and the rain, and within a season it stops looking new. That is the intended outcome, not a defect."),
 ("sage-waxed-canvas","The Sage &mdash; Rugged Waxed Canvas","Fairway Headcover &middot; $100","the-sage-rugged-waxed-canvas-golf-headcover",
  "Waxed canvas rather than leather, in a pale sage that goes darker where it is handled. Cheaper than The Field by fifteen dollars and considerably more forgiving in weather &mdash; waxed cotton sheds a shower and dries without cracking."),
 ("scout-navy","The Scout &mdash; Rugged Navy Waxed Canvas","Fairway Headcover &middot; $100","the-scout-rugged-navy-waxed-canvas-golf-headcover",
  "Navy waxed canvas with an olive stripe and the woven Bluegrass Fairway label stitched at the hem. The most restrained cover in the range, and the one to pick if the rest of the bag is already busy."),
 ("harris-tweed-cover","The Harris &mdash; Navy Herringbone Harris Tweed","Fairway Headcover &middot; $110","the-harris-navy-herringbone-harris-tweed-golf-headcover",
  "Authentic Harris Tweed, which by law is handwoven at the weavers&rsquo; homes in the Outer Hebrides and carries the Orb mark. Navy herringbone over a leather base. The brand has never published why it chose the mill, but the pairing of a licensed Scottish cloth with Kentucky leatherwork is the whole idea in one object."),
 ("donegal-wool","The Donegal &mdash; Herringbone Wool &amp; Leather","Fairway Headcover &middot; $110","the-donegal-herringbone-wool-leather-golf-headcover",
  "Cream-and-brown herringbone wool with leather trim and a stitched-on number. Warmer and softer in the hand than the waxed canvas covers, and the one that looks most like something inherited."),
 ("bomber-jacket-driver","Bomber Jacket Leather Driver Headcover","Driver Headcover &middot; $175","bomber-jacket-leather-driver-headcover",
  "Built to read as a flight jacket: distressed brown leather body, shearling collar at the opening, and a winged patch stitched to the flank. The most expensive single cover in the range and the least subtle thing on the page."),
 ("redan-putter-cover","Redan Putter Cover &mdash; Harris Tweed Brown Herringbone","Putter Headcover &middot; $90","redan-putter-cover-in-harris-tweed-brown-herringbone",
  "A blade cover in brown herringbone Harris Tweed with a leather-bound opening and a stamped maker&rsquo;s tag at the toe. Named, like several of their shapes, after a template hole."),
 ("steurer-mcqueen-bag","Steurer &amp; Co. &times; Bluegrass Fairway Sunday Bag","Golf Bag &middot; $850","steurer-co-x-bluegrass-fairway-golf-bag-in-repurposed-barbour-jacket",
  "Built from an original Steve McQueen Barbour International jacket, cut down and rebuilt as a Sunday carry &mdash; the waxed cotton, the tartan lining and the brass zips all come off the donor coat, so the pocket detail is a jacket pocket. Made with Will Jacoby of Steurer &amp; Co., the Louisville leather workshop where Bluegrass Fairway production moved in its first year."),
 ("daily-duffel","Daily Duffel &mdash; Brown Waxed Canvas &amp; Harris Tweed","Duffel Bag &middot; $299","daily-duffel-bag-brown-waxed-canvas-and-harris-tweed",
  "Waxed canvas body, Harris Tweed panel down the flank, leather cap ends and a brass buckle on the shoulder strap. Sized for a locker room rather than a week away."),
 ("blackwatch-shoe-bag","Shoe Bag in Blackwatch Waxed Canvas","Shoe Bag &middot; $155","bluegrass-fairway-shoe-bag-in-blackwatch-waxed-canvas",
  "Blackwatch tartan under wax, with a full-length zip and a grab handle. A shoe bag is the least romantic thing in a golf bag, which is presumably why almost nobody makes a good one."),
 ("buttero-yardage-cover","Premium Italian Buttero Leather Yardage Book Cover","Leather &middot; $110","premium-italian-buttero-leather-golf-yardage-book-cover",
  "Vegetable-tanned Buttero from Conceria Walpier in Tuscany, undyed and unlined, with a small stamped flag at the corner. It arrives almost blond and darkens unevenly with handling. The direct descendant of the broken cover that started the company."),
 ("horween-scorecard","Premium Horween Leather Minimalist Scorecard Holder","Leather &middot; $85","premium-horween-leather-minimalist-golf-scorecard-holder",
  "Horween Chromexcel from Chicago, in the stripped-back version &mdash; card slot, pencil loop, nothing else. The cheapest way into the leather side of the catalog and the piece the brand has sold more of than anything else."),
 ("single-barrel-yardage","Single Barrel Yardage Book / Scorecard Holder","Leather &middot; $190","single-barrel-collection-yardage-book-scorecard-holder",
  "From the Single Barrel collection, which the brand describes as &ldquo;one-off only customs that we make in our Custom Shop in Louisville, KY&hellip; Each piece is 1 of 1.&rdquo; This one is a heavily marbled cognac shell with white contrast stitching. When it sells, that exact hide is gone."),
 ("harris-tweed-pouch","Harris Tweed Zippered Valuables Field Pouch","Pouch &middot; $68","harris-tweed-zippered-golf-valuables-field-pouch-in-brown-herringbone",
  "Brown herringbone Harris Tweed with a leather zip pull and the woven label at the seam. Holds a phone, keys, a wallet and a couple of tees &mdash; the things that otherwise rattle around the bottom of a bag."),
 ("pendleton-valuables-pouch","Single Barrel Pendleton Wool Zippered Valuables Pouch","Pouch &middot; $80","single-barrel-collection-pendleton-wool-zippered-golf-valuables-pouch",
  "Pendleton wool in a full-colour Southwestern pattern, which is the loudest fabric they work with and the reason this one is in the Single Barrel run. Each is cut from a different part of the blanket, so no two land the pattern the same way."),
 ("recon-rangefinder","The Recon &mdash; Waxed Canvas Rangefinder Case","Pouch &middot; $80","the-recon-waxed-canvas-rangefinder-case",
  "Olive waxed canvas with a leather flap and a magnetic closure, cut to take a standard rangefinder without the factory case. The flap is the part that matters &mdash; it opens one-handed."),
 ("needlepoint-belt","Custom Needlepoint Belt","Needlepoint Belt &middot; $200","create-your-own-custom-needlepoint-belt-by-bluegrass-fairway",
  "Hand-stitched needlepoint on a leather tab-and-buckle, built to order with your own motifs &mdash; club logos, state flags, initials. Ships in a branded wooden box. The slowest thing they make and the one with the longest lead time."),
]

def frames(slug):
    n=1
    while os.path.exists(f"images/bluegrass-fairway/{slug}-a{n+1}.jpg"): n+=1
    return n

def gallery(slug,name):
    n=frames(slug); plain=re.sub(r'<[^>]+>|&[a-z]+;','',name)
    if n==1:
        return (f'<div class="product-gallery"><div class="pg-track"><div class="pg-frame">'
                f'<img src="/images/bluegrass-fairway/{slug}.jpg" alt="Bluegrass Fairway {plain}" loading="lazy" /></div></div></div>')
    fr="".join(f'<div class="pg-frame"><img src="/images/bluegrass-fairway/{slug}{"" if i==0 else f"-a{i+1}"}.jpg" '
               f'alt="Bluegrass Fairway {plain} &middot; view {i+1} of {n}" loading="lazy" /></div>' for i in range(n))
    dots="".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" aria-label="View image {i+1}"></button>' for i in range(n))
    return (f'<div class="product-gallery"><div class="pg-track">{fr}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>')

cards="\n    ".join(
 f"""<div class="product-card" data-frames="{frames(s)}">
      {gallery(s,n)}
      <div class="product-body">
        <div class="product-brand">Bluegrass Fairway</div>
        <div class="product-name">{n} &middot; {m.split('&middot;')[-1].strip()}</div>
        <div class="product-desc">{d}</div>
        <a href="{BASE}{h}" target="_blank" rel="noopener" class="product-link">Shop ↗</a>
      </div>
    </div>""" for s,n,m,h,d in P)

INTRO="""<div class="writeup">
  <div class="writeup-body">
    <p>Bluegrass Fairway is a small workshop in Louisville, Kentucky making leather, Harris Tweed and waxed canvas golf goods by hand &mdash; headcovers, yardage book covers, valuables pouches, rangefinder cases and the occasional needlepoint belt. Around 172 products are live at any one time, priced from about $38 for a hat to $1,100 for a bag built out of a repurposed Barbour jacket.</p>
    <p>The company exists because a cheap yardage book cover fell apart. Matt Reynolds took it to a local shoe cobbler to be repaired, and the cobbler told him they could simply build a better one. They went through roughly three versions. Friends asked for copies, a friend&rsquo;s wife suggested Etsy, and in October 2015 he listed it. One sale came in the first month. Then about a hundred arrived over the next forty days, and the cobbler could not keep up.</p>
    <p>For anyone who likes the idea of golf equipment made from named materials by identifiable people, this is a straightforward recommendation. It is also cheaper to get into than that description implies: a Horween scorecard holder is $85, and a waxed canvas headcover is $100.</p>
  </div>
</div>
"""

PULL="""<section class="products">
  <blockquote class="pull-quote">
    <p>&ldquo;We like being the rock band only you and your buddies know about, that buried treasure.&rdquo;</p>
    <cite>&mdash; Matt Reynolds, founder, to Etsy Journal, May 2017</cite>
  </blockquote>
</section>
"""

STORY="""<section class="products">
  <h2 class="products-hdr">The Story</h2>
  <p class="cat-kicker">Reynolds has given two published interviews, both in 2017. The quotes below are from those, and are dated accordingly.</p>
  <div class="writeup-body">
    <p>Reynolds grew up in Louisville and took his first job at Wildwood Country Club. He became a scratch player and finished inside the top five at the Kentucky Open. When Bluegrass Fairway started he was working at his family&rsquo;s insurance agency, and had been since he was twenty-two. &ldquo;I work at my family&rsquo;s insurance agency and have since I was 22 years old, so the Bluegrass Fairway thing is kind of a side project for me,&rdquo; he told GolfWRX in October 2017. Whether that is still true is not something the brand has said publicly since.</p>
    <p>The cobbler could not scale, so production moved into the workshop of Will Jacoby &mdash; then Steurer &amp; Jacoby, now Steurer &amp; Co. &mdash; a Louisville leather house. In 2017 Reynolds said the sewing was being done there by Will&rsquo;s daughters, Meg and Jane, with him helping. He also mentioned that his grandmother and her five sisters were quiltmakers, and that they taught him to sew. The current arrangement is not published; the Single Barrel collection page now refers to a Custom Shop of their own.</p>
    <p>On what the brand is for, he was direct: &ldquo;We want to provide a classy product that reflects what we appreciate about the game of golf. Needless to say, I doubt you&rsquo;ll see something in neon orange from us.&rdquo; And, to Etsy the same year: &ldquo;The golf business right now, if you go into a golf store, it&rsquo;s all neon colors and fluorescents, and that&rsquo;s just not my style.&rdquo; Nine years of catalog bears that out &mdash; the loudest thing in the range is a Pendleton blanket print.</p>
    <p>Early orders set the tone. The Orlando Magic bought logo scorecard holders for a golf event about three months in. The USGA ordered yardage book holders for the Mid-Amateur, which Reynolds said sold out the first day. Curtis Strange became a customer. By December 2018 the brand had sold more than seven thousand scorecard holders.</p>
    <p>One line has aged in an interesting way. In 2017 he described the materials as &ldquo;super high-quality, made-in-the-USA materials, and we make everything by hand right here in Kentucky. We don&rsquo;t mass produce.&rdquo; The making is still in Kentucky. The materials have travelled: alongside Horween out of Chicago, the premium tier now runs on Italian leather &mdash; Buttero from Conceria Walpier, Pueblo from Badalassi Carlo &mdash; plus Harris Tweed from the Outer Hebrides and Pendleton wool. The claim about handwork holds; the sourcing map has widened.</p>
  </div>
</section>
"""

MATERIALS="""<section class="products">
  <h2 class="products-hdr">What It Is Made Of</h2>
  <p class="cat-kicker">The tanneries and mills are named on the product pages, which is rarer in golf than it should be.</p>
  <div class="writeup-body">
    <p><strong>Leather.</strong> Horween of Chicago supplies Chromexcel and shell cordovan. The Italian side is Conceria Walpier, whose Buttero is the pale vegetable-tanned hide used on the yardage book covers, and Badalassi Carlo, who make Pueblo. La Perla Azzurra supplies a camo-printed leather. North American bison and roughout suede appear on individual runs.</p>
    <p><strong>Cloth.</strong> Harris Tweed appears on roughly twenty products and carries the Orb mark, which requires it to be handwoven at the weaver&rsquo;s home in the Outer Hebrides from virgin Scottish wool. Pendleton wool covers the louder pieces. Waxed canvas comes from British Millerain and from American 10oz duck.</p>
    <p><strong>Construction.</strong> Vinymo thread, hand-finished edges, and the standard line across the pouch range: all bags are handmade in the USA. The Single Barrel pieces are one-offs cut from single hides &mdash; when the hide is gone, the piece is not repeatable.</p>
  </div>
</section>
"""

FAQ_ITEMS=[
 ("Who makes Bluegrass Fairway?",
  "Matt Reynolds, in Louisville, Kentucky. He founded it in October 2015 after a cobbler offered to rebuild a yardage book cover that had fallen apart. Production moved early on into the Louisville workshop of Will Jacoby of Steurer &amp; Co."),
 ("What is the Single Barrel collection?",
  "A run of one-off pieces the brand describes as &ldquo;one-off only customs that we make in our Custom Shop in Louisville, KY&hellip; Each piece is 1 of 1.&rdquo; Roughly 34 products carry the tag, priced from about $80 to $300. Each is cut from a specific hide or a specific part of a blanket, so it cannot be reordered."),
 ("Is Bluegrass Fairway independent?",
  "There is no public record of a parent company, outside investment or acquisition, and it has been founder-led since 2015. The brand describes itself as &ldquo;a small team focused on making each piece right.&rdquo;"),
 ("What does it cost to get in?",
  "A cotton logo hat is $38 and the minimalist Horween scorecard holder is $85. Waxed canvas headcovers are $100 and leather ones $115. The Steurer &amp; Co. collaboration bags run $850 to $1,100."),
 ("Do they sell anything they do not make?",
  "A little. Around 28 products are Bluegrass Fairway apparel produced by partners &mdash; the Tour Visor is made by Holderness &amp; Bourne &mdash; and a Vintage Pro Shop collection of about nine items launched in May 2026, selling secondhand and new-old-stock golf clothing under the labels &ldquo;Gently Used,&rdquo; &ldquo;New Old Stock&rdquo; and &ldquo;New.&rdquo; The other 135 products are their own."),
]
FAQ="""<section class="products">
  <h2 class="products-hdr">The Questions</h2>
  <div class="faq">
"""+"\n".join(f'    <div class="faq-q">{q}</div>\n    <div class="faq-a">{a}</div>' for q,a in FAQ_ITEMS)+"""
  </div>
</section>
"""
def strip(s): return re.sub(r'<[^>]+>','',s).replace("&ldquo;",'"').replace("&rdquo;",'"').replace("&rsquo;","'").replace("&amp;","&").replace("&hellip;","...").replace("&mdash;","—")
SCHEMA={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
 {"@type":"Question","name":strip(q),"acceptedAnswer":{"@type":"Answer","text":strip(a)}} for q,a in FAQ_ITEMS]}

model=open("drops/students-golf-summer-2026.html",encoding="utf-8").read()
head=model[:model.find('<div class="breadcrumb">')]
tail=model[model.find('<section class="more"'):]
head=re.sub(r'<title>[^<]*</title>',f'<title>{PLAIN} — The Grassy Issue</title>',head)
for k,v in [("description",DESC),("og:title",PLAIN),("og:description",DESC)]:
    head=re.sub(rf'(<meta (?:name|property)="{re.escape(k)}" content=")[^"]*(")',lambda m:m.group(1)+v+m.group(2),head)
head=re.sub(r'(<link rel="canonical" href=")[^"]*(")',lambda m:m.group(1)+f"https://thegrassyissue.com/drops/{SLUG}"+m.group(2),head)
head=re.sub(r'(<meta property="og:url" content=")[^"]*(")',lambda m:m.group(1)+f"https://thegrassyissue.com/drops/{SLUG}"+m.group(2),head)
head=re.sub(r'(<meta property="og:image" content=")[^"]*(")',lambda m:m.group(1)+"https://thegrassyissue.com/images/bluegrass-fairway/hero.jpg"+m.group(2),head)
_schema_block='<script type="application/ld+json">'+json.dumps(SCHEMA)+'</script>'
head=re.sub(r'<script type="application/ld\+json">.*?</script>',lambda m:_schema_block,head,flags=re.S)

body=(f'<div class="breadcrumb">\n  <a href="/">Feed</a><span>/</span>\n  <a href="/#feed">Drops &amp; Brands</a><span>/</span>\n  Bluegrass Fairway</div>\n'
 f'<header class="drop-header">\n  <h1>{TITLE}</h1>\n  <div class="drop-meta">\n'
 f'    <span>September 4, 2026</span><span class="dot"></span>\n    <span>Brand to Know</span><span class="dot"></span>\n'
 f'    <span>Louisville, Kentucky &middot; est. 2015</span>\n  </div>\n</header>\n\n'
 '<div class="drop-hero"><div class="drop-hero-img"><img src="/images/bluegrass-fairway/hero.jpg" '
 'alt="A hand pulling a Bluegrass Fairway Horween leather scorecard holder from a green jacket pocket on course" /></div></div>\n'
 +INTRO+PULL
 +f'<section class="products">\n  <h2 class="products-hdr">The Collection &mdash; 18 Pieces</h2>\n'
  f'  <p class="cat-kicker">The current catalog runs to 172 products; these eighteen cover the range, $68 to $850.</p>\n'
  f'  <div class="products-grid">\n    {cards}\n  </div>\n</section>\n'
 +STORY+MATERIALS+FAQ)

open(f"drops/{SLUG}.html","w",encoding="utf-8").write(head+body+tail)
print(f"wrote drops/{SLUG}.html | {len(P)} products | ~{len(re.sub(r'<[^>]+>',' ',head+body+tail).split())} words")
