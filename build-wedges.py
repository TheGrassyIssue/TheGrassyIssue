#!/usr/bin/env python3
# Builds /drops/the-custom-wedge-report.html
import re, json, os, html as H

S = os.path.dirname(os.path.abspath(__file__))
BASE = open(os.path.join(S, "drops/the-ball-marker-atlas.html"), encoding="utf-8").read()
MAN = json.load(open("/tmp/wg/manifest.json"))

TITLE = "The Custom Wedge Report — Stamping Shops, Forged Makers and What &ldquo;Custom&rdquo; Actually Means"
SLUG  = "the-custom-wedge-report"
DESC  = ("Twenty-seven custom wedges from eleven makers, plus every manufacturer stamping program compared. "
         "Independent engravers, Japanese forging houses, hand-ground one-offs, and an honest look at how much "
         "of what gets sold as custom is really a drop-down menu.")

BRAND = {
 "showoutengraving.com": "Show Out Engraving",
 "bettinardi.com": "Bettinardi",
 "miuragolf.com": "Miura",
 "grindworks-online.com": "Grindworks",
 "indigolfclubs.com": "Indi Golf",
 "fourteengolf.us": "Fourteen",
 "newlevelgolf.com": "New Level",
 "pxg.com": "PXG",
 "edelgolf.com": "Edel",
 "kyoeigolf.com": "KYOEI",
 "artisangolftx.com": "Artisan Golf",
}

# price rendering — never convert, never assume a "$" means USD
def price(m):
    p, c = m["price"], m["cur"]
    if c == "JPY":  return "&yen;" + format(int(float(p)), ",")
    if c == "UNLABELLED": return p.replace("–", "&ndash;")   # currency not stated by the seller
    if any(ch.isalpha() for ch in p): return "$" + p
    return "$" + p.rstrip("0").rstrip(".") if "." in p else "$" + p

SECTIONS = [
 ("The Stamping Shops", "showout", "One Person, One Club at a Time",
  "The smallest operations in this report and the only ones doing genuinely one-off work on a club you already own. "
  "You ship them a wedge, they take the head off the shaft, mark it, and send it back. Show Out numbers its Artist "
  "Series pieces 1/1 because there is exactly one of each. Vincent Newman runs it out of a unit in Gilbert, "
  "Arizona; the shipping address on his own site is a house.",
  ["showoutengraving.com"]),

 ("Forged and Built to Order", "forged", "The Configurator Tier",
  "Everything here is made after you order it rather than pulled off a shelf, which is a real thing and not the same "
  "thing as bespoke. You are choosing from a menu &mdash; grind, finish, loft, lie, length, shaft, ferrule &mdash; and "
  "the menu is deep. Bettinardi is the outlier: its one-off Hive drops are single units at set-of-three money.",
  ["bettinardi.com", "indigolfclubs.com", "newlevelgolf.com", "edelgolf.com", "pxg.com"]),

 ("Japan", "japan", "Forging Houses and One-Cut Grinds",
  "Four makers, four different answers to whether you can actually buy one. Grindworks sells at home in yen and sends "
  "everyone else to a distributor. Fourteen ships to North America and Europe and nowhere else. KYOEI puts "
  "&ldquo;we ship worldwide&rdquo; on every page. Miura is forged in Himeji but the storefront you will buy from is a "
  "US company in Scottsdale.",
  ["grindworks-online.com", "fourteengolf.us", "kyoeigolf.com", "miuragolf.com"]),

 ("The Ones You Can't Just Order", "closed", "Fittings, Flights and Bank Transfers",
  "The best work in this report is also the hardest to get. Artisan will hand-grind you a wedge and stamp it however "
  "you like, but only after you fly to Fort Worth and sit a three-hour fitting. That is not a marketing posture &mdash; "
  "it is written plainly on their own site.",
  ["artisangolftx.com"]),
]

COPY = {
"sparky-stencil-lab-edition":
 "Stencil Lab is the pre-set tier &mdash; a fixed design applied to a wedge, cheaper than a commission because he isn&rsquo;t drawing it from scratch. Show Out photograph these designs on engraving plates rather than on a club, so that is what you are looking at. Their line for it: serious about quality, casual about rules.",
"butch-t-cougar-stencil-lab-edition":
 "A college mascot, engraved. Shown on Show Out&rsquo;s sample plate; the design goes on the wedge you send in.",
"desert-diamondback-stencil-lab-edition":
 "The cheapest way into Show Out at $135. Arizona iconography, which is where the shop is. Pictured as an engraving sample rather than a finished club.",
"desert-drought-golf-stencil-lab-edition":
 "Desert Drought. Phoenix humour, in a state where the water conversation is not really a joke. Also shown on a sample plate.",
"showout-commission-gallery":
 "The commission route rather than a fixed design: you send your own club, agree a design, and it comes back one-of-one. Entry-level engraving starts at $125, Signature is $250 and Complex is $375. Every job has the head taken off the shaft first so the shaft never sees heat, then annealed, sanded, buffed and sealed with wax.",
"tropical-noir-1-1-ping-s159-60-artist-series":
 "A Ping s159 taken apart, laser-cut and put back together as a single numbered piece. Sold out, which is what 1/1 means.",
"the-watcher-1-1-titleist-vokey-56-artist-ser":
 "The other Artist Series piece, on a Vokey 56. Vincent Newman works out of a unit in Gilbert, Arizona, and the shipping address on his own site is a house.",
"lefty-love-lucky-wizard-texas-tea-hlx-6-0-lh":
 "A left-handed three-wedge set in Texas Tea, one unit made. Bettinardi&rsquo;s Hive drops are the closest thing a major maker does to a one-off.",
"lefty-love-zombee-black-pvd-hlx-6-0-lh-wedge":
 "Zombee Black PVD, also left-handed, also a single set. The names are not focus-grouped.",
"lefty-love-multi-bomb-steel-patina-hlx-6-0-l":
 "Steel Patina, meant to change colour with use rather than hold a finish.",
"limited-edition-nickel-chrome-blast-face-4":
 "Indi lets you pick your grooves at checkout &mdash; conforming, or the non-conforming set they label Big Box Grooves and mark Not Tournament Approved.",
"limited-edition-bronze-blast-face-4":
 "The bronze version of the same head. Carlsbad, California, out of a fitting studio they call the House of Spin.",
"flx-blast-face-4":
 "FLX is the straighter leading edge, for pickers and firm turf. ATK is the other one.",
"b-i-g-bunker-beater":
 "A dedicated sand club at well under half the price of everything around it.",
"spn-v3-raw-forged-wedges":
 "Raw 1020 carbon that will rust, sold with a build configurator that runs to length in quarter-inch steps and about seventy shafts. New Level ship internationally and say so plainly.",
"desert-eclipse-spn-wedges-closeout":
 "The previous generation on closeout. New Level don&rsquo;t take returns on anything, because everything is built when you order it.",
"sms-pro-wedge":
 "One price across every loft, grind, bounce and weight-bias combination. The flip weight shifts mass to the heel or toe depending on how you order it.",
"custom-stick-em-wedge-chrome":
 "PXG&rsquo;s configurable Stick&rsquo;em in chrome.",
"custom-stick-em-wedge-black":
 "The black version, twenty dollars more.",
"86-raw-wedge":
 "SUS218 stainless, vibratory tumbled to that marbled raw finish, in four factory grinds. Patrick Reed is credited with the spec.",
"grindworks-patrick-reed-barrett-wedge":
 "The Reed signature wedge. Priced in yen and sold domestically &mdash; outside Japan you go through a distributor.",
"zip-wedge":
 "The cheapest thing Grindworks make, still built to order after purchase.",
"frz-wedges-stock":
 "Fourteen sell the same head two ways: stock, or Forged Custom built to order in about twenty business days and non-returnable even unused.",
"dj-6-wedges-stock":
 "Founded in 1981 by Takamitsu Takebayashi, an accomplished amateur who started out designing for other people&rsquo;s brands.",
"kyoei-type-x-wedge":
 "KYOEI CUSTOM lets you choose the back design, the sole grind and the stamping. Note the price carries no currency label anywhere on their site &mdash; shown here exactly as they print it.",
"kyoei-tour-wedge":
 "Described on their own page as one hundred per cent made and hand-ground in Japan. Rooted in Himeji, per their Heritage page.",
"kyoei-triple-weight-wedge":
 "Three machined ports with interchangeable weights. They also sell a non-conforming version of this head, openly.",
"forged-wedge-series-y-grind-qpq":
 "The Y Grind is named after Yoshitaka Miura. QPQ is the hardest of the three finishes.",
"k-grind-2-0":
 "Miura&rsquo;s configurator is the best of any maker here &mdash; lie and loft in two-degree ranges either way, length in quarter inches, thirteen shaft brands, and a free-text box for swing-weight targets.",
"forged-wedge-series-y-grind-raw":
 "Raw, so it patinas. Forged in Himeji; the company you buy from is Miura Golf LLC in Scottsdale.",
"artisan-hand-ground-wedge":
 "Every one hand-ground by Mike Taylor, formerly Nike&rsquo;s tour grinder, who signs the site copy &ldquo;- MT&rdquo;. Stamping and paint fill are included in the price. Right hand only.",
"artisan-custom-finishes":
 "Heat-torched Bluebonnet, Texas Crude PVD, Oxidado, Patina Grey. Thirty to sixty dollars on top, and a nine-week queue after your fitting.",
}

FAQ = [
 ("What does &ldquo;custom wedge&rdquo; actually mean?",
  "Three different things, and the word covers all of them. A stamping shop marks a club you already own and no two "
  "come out the same. A made-to-order maker builds from a menu of grinds, finishes and specs after you pay. A "
  "manufacturer program adds text and paint fill to a stock head. Only the first is genuinely one-off."),
 ("Which manufacturers publish their stamping character limits?",
  "Only two. TaylorMade&rsquo;s MyMG5 states twelve characters across five layouts with more than fifty logos. Mizuno "
  "states six characters per wedge in twelve colours, with spaces counting as characters and no symbols beyond a hash "
  "mark. Titleist, Callaway, Cleveland and PING all keep their limits behind configurators that publish nothing."),
 ("What does a manufacturer custom wedge cost?",
  "TaylorMade charges a flat fifty dollars over the stock MG5, taking MyMG5 to $249.99. Callaway Customs on the Opus "
  "SP is $199.99 &mdash; the same as the stock chrome wedge, so entering the program costs nothing. Vokey WedgeWorks "
  "runs $199 to $229 depending on finish. PING publishes no price at all and does not sell direct."),
 ("How long does custom wedge work take?",
  "Manufacturer programs are the fastest: TaylorMade quotes four weeks, and Vokey is currently quoting five to six "
  "because of a self-declared systems delay. Independent shops vary wildly &mdash; Show Out quotes three to fifteen "
  "business days by tier, while Weller Design Lab was booked into October as of the end of July. Artisan is about nine "
  "weeks, after your fitting."),
 ("Can I send in a wedge I already own?",
  "Yes, at every independent shop here. Show Out, Weller and Swing Right all work on your club, and Show Out removes "
  "the head from the shaft first so the shaft never sees heat. Manufacturer programs do not work this way &mdash; you "
  "are ordering a new head."),
 ("Are Japanese custom wedges buyable from the US?",
  "It depends entirely on the maker and it is the single most confusing part of this category. KYOEI puts &ldquo;we "
  "ship worldwide&rdquo; on every page. Fourteen ships to North America and Europe only. Grindworks sells domestically "
  "in yen and routes everyone else to a distributor. Ryoma states delivery within Japan only, and Yururi wants a "
  "Japanese bank transfer."),
 ("Does custom stamping affect whether a wedge is conforming?",
  "Stamping and paint fill do not. Grooves do, and several makers here sell both versions openly &mdash; Indi Golf "
  "labels its non-conforming set Big Box Grooves and marks it Not Tournament Approved, and KYOEI and Yururi both list "
  "non-conforming heads alongside conforming ones."),
 ("Who is Anthony Taranto?",
  "Callaway&rsquo;s Pro Tour Club Artist, based in Carlsbad, who hand stamps, paints and sandblasts tour wedges. He "
  "took the job after a Callaway newspaper ad in 1999, having survived his boat sinking off Panama as a deckhand. His "
  "clubs have gone to Obama, Steph Curry and Jimmy Buffett. You essentially cannot buy one."),
]

# ---------------- build ----------------
by_brand = {}
for m in MAN: by_brand.setdefault(m["brand"], []).append(m)

def card(m):
    frames = "".join(
        '<div class="pg-frame"><img src="%s" alt="%s %s custom golf wedge" loading="lazy" /></div>'
        % (src, BRAND[m["brand"]], H.escape(m["title"]))
        for src in m["imgs"])
    commission = m["brand"] == "artisangolftx.com" or m["slug"] == "showout-commission-gallery"
    label = "Commission &#8599;" if commission else "Shop &#8599;"
    desc = COPY.get(m["slug"], "")
    return ('    <div class="product-card" data-frames="%d">\n'
            '      <div class="product-gallery"><div class="pg-track">%s</div></div>\n'
            '      <div class="product-body">\n'
            '        <div class="product-brand">%s</div>\n'
            '        <div class="product-name">%s &middot; %s</div>\n'
            '        <div class="product-desc">%s</div>\n'
            '        <a href="%s" target="_blank" rel="noopener" class="product-link">%s</a>\n'
            '      </div>\n    </div>\n') % (
        len(m["imgs"]), frames, BRAND[m["brand"]], H.escape(m["title"]), price(m), desc, m["url"], label)

body = []
ncards = 0
for name, anchor, kicker, blurb, doms in SECTIONS:
    cards = []
    for d in doms:
        for m in by_brand.get(d, []):
            cards.append(card(m)); ncards += 1
    body.append('<h2 id="%s">%s</h2>\n<p class="cat-kicker"><strong>%s.</strong> %s</p>\n<div class="products-grid">\n%s</div>\n'
                % (anchor, name, kicker, blurb, "".join(cards)))

OEM = """<h2 id="programs">The Manufacturer Programs</h2>
<p class="cat-kicker"><strong>What They Will And Won&rsquo;t Tell You.</strong> Every major maker runs a wedge
personalisation program. Two of them publish what the limits actually are. The rest hide the options behind a
configurator that renders nothing until you are inside it, which makes the category almost impossible to compare
honestly &mdash; so here is only what each brand states itself.</p>
<div class="spec-table-wrap"><table class="spec-table">
<thead><tr><th>Program</th><th>Current model</th><th>Price</th><th>What&rsquo;s published</th><th>Lead time</th></tr></thead>
<tbody>
<tr><td>TaylorMade MyMG5</td><td>MG5</td><td>$249.99<br><span class="muted">$50 over stock</span></td>
<td>12 characters, 5 layouts, 50+ logos. Four finishes, five grinds.</td><td>4 weeks</td></tr>
<tr><td>Mizuno Custom Stamping</td><td>Pro T-1 / T-3</td><td>$180 base<br><span class="muted">stamping price not stated</span></td>
<td>6 characters per wedge, spaces count, letters/numbers/# only, 12 named colours. Dealer channel only.</td><td>Not stated</td></tr>
<tr><td>Titleist Vokey WedgeWorks</td><td>SM11</td><td>$199&ndash;$229</td>
<td>Four finishes, 26 loft/bounce/grind combos, six WedgeWorks-exclusive grinds. Character limits not published.</td><td>5&ndash;6 weeks<br><span class="muted">self-declared delay</span></td></tr>
<tr><td>Callaway Customs</td><td>Opus SP / SP+</td><td>$199.99<br><span class="muted">no upcharge to enter</span></td>
<td>Finish, paint, stamped text and emojis, shaft bands, ferrules. Opus Raw is custom-only. Limits not published.</td><td>Not stated</td></tr>
<tr><td>Cleveland My Custom Wedge</td><td>RTZ 2</td><td>$199.99&ndash;$219.99</td>
<td>Paintfill, engraving, ferrules, skins, custom components. Site is a client-rendered app; nothing further is published.</td><td>Not stated</td></tr>
<tr><td>PING</td><td>s259</td><td><span class="muted">no price published</span></td>
<td>Nothing. No character limits, no paint-fill palette, no upcharges, and PING does not sell direct &mdash; you take the design to a retailer.</td><td>Not stated</td></tr>
</tbody></table></div>
<p>The pattern is the interesting part. The two brands that publish hard numbers are the two with the tightest limits.
Mizuno will give you six characters and tells you so; Titleist will give you considerably more and tells you nothing
until you are three clicks into a builder.</p>
"""

faq_html = "".join(
    '    <details class="faq-q"><summary>%s</summary><p>%s</p></details>\n' % (q, a)
    for q, a in FAQ)
faq_ld = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
    {"@type":"Question","name":re.sub(r"&[a-z]+;","'",q),
     "acceptedAnswer":{"@type":"Answer","text":re.sub(r"&[a-z]+;","'",a)}} for q,a in FAQ]}, ensure_ascii=False)

INTRO = """    <p>The wedge is the only club most golfers will ever have marked with their own name, and an entire small
industry has grown up around that. It runs from a man in Gilbert, Arizona taking the head off your Vokey so the shaft
never sees heat, through Japanese forging houses that will hand-grind a sole to your attack angle, up to a Callaway
employee in Carlsbad whose work is in the bags of two former presidents and cannot be bought at any price.</p>
    <p>It also runs through a lot of drop-down menus. Of the makers here, only a handful do genuinely one-off work:
Show Out and the other independent engravers, Artisan in Fort Worth, KYOEI&rsquo;s custom programme, and Anthony
Taranto, whose wedges are not for sale. Grindworks, Fourteen, Bettinardi, Edel, New Level, Indi and Miura all label
their wedges custom, and all of them mean built-to-order from a fixed set of options. That is a genuinely good thing to
buy. It is not the same thing, and the word does not distinguish between them.</p>
    <p>Twenty-seven wedges below from eleven makers, then every manufacturer program compared on what it actually
publishes. Prices are in the currency the seller prints, and where a seller prints no currency at all &mdash; KYOEI
does not, anywhere on its site &mdash; it is shown here exactly as they show it.</p>
"""

# assemble from the atlas skeleton
h = BASE
h = re.sub(r"<title>.*?</title>", "<title>%s &mdash; The Grassy Issue</title>" % TITLE, h, flags=re.S)
h = re.sub(r'(<meta name="description" content=")[^"]*(")', lambda m: m.group(1)+DESC+m.group(2), h)
h = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1)+TITLE+m.group(2), h)
h = re.sub(r'(<meta property="og:description" content=")[^"]*(")', lambda m: m.group(1)+DESC+m.group(2), h)
h = h.replace("the-ball-marker-atlas", SLUG)
h = h.replace("/images/ball-markers/hero.jpg", "/images/custom-wedges/hero.jpg")

# swap the H1
h = re.sub(r'(<h1[^>]*>).*?(</h1>)', lambda m: m.group(1)+TITLE+m.group(2), h, count=1, flags=re.S)

# swap intro
h = re.sub(r'(<div class="writeup-body">).*?(</div>)', lambda m: m.group(1)+"\n"+INTRO+"  "+m.group(2), h, count=1, flags=re.S)

# replace everything between <section class="products"> and its FAQ block
start = h.find('<section class="products">')
fq    = h.find('<h2 class="products-hdr sec">Questions</h2>')
assert start > 0 and fq > start, "anchors not found"
h = h[:start] + '<section class="products">\n' + "".join(body) + OEM + '\n  ' + h[fq:]

# swap FAQ items + schema
h = re.sub(r'(<div class="faq">).*?(  </div>\n</section>)',
           lambda m: m.group(1)+"\n"+faq_html+m.group(2), h, count=1, flags=re.S)
blocks=list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S))
for b in blocks:
    if '"FAQPage"' in b.group(1):
        h = h[:b.start()] + '<script type="application/ld+json">'+faq_ld+'</script>' + h[b.end():]
        break

# details sidebar
h = re.sub(r'(<span class="l">Markers</span><span>)\d+(</span>)', lambda m: '<span class="l">Wedges</span><span>%d</span>' % ncards, h)
h = re.sub(r'(<span class="l">Brands</span><span>)\d+(</span>)', lambda m: m.group(1)+"11"+m.group(2), h)

out = os.path.join(S, "drops", SLUG + ".html")
open(out, "w", encoding="utf-8").write(h)
print("wrote", out)
print("  cards:", ncards, " frames:", sum(len(m["imgs"]) for m in MAN))
print("  brands:", len({m["brand"] for m in MAN}))
print("  div balance:", len(re.findall(r"<div\b", h)) == h.count("</div>"))
print("  anchor balance:", len(re.findall(r"<a\b", h)) == h.count("</a>"))
for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
    json.loads(m.group(1))
print("  json-ld: ok")
