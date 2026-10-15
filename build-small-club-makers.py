#!/usr/bin/env python3
"""build-small-club-makers.py — "Small Golf Club Makers: 17 Independent Brands for Putters, Irons and Drivers" 15 October 2026.
Lenny: "Let's do a post about small brands making equipment, putters, irons and drivers." Picked from a 25-maker options sheet:
putters 1-8, irons 13-18 (added New Level), drivers 21-23 (dropped Sub 70, Hogan, Lazrus).
FACTS: Shopify stores re-read Oct 15 2026 via products.json (Lajosi, Hanna, T Squared, Gambit, Tad Moore, BALDO, Vega, New Level,
BombTech, Tour Edge). Kronos (Squarespace), Carbon (WooCommerce), Artisan (Wix), P53 (Squarespace), Itobori (Jimdo) read from their own
pages Oct 15 2026. Rates Oct 15 2026: 1 USD = 1.447 AUD, 0.75491 GBP, 157.98 JPY. Artisan's own pages give putter starts of $1,040 and
$1,100. P53 and Itobori publish no prices. Quotes verbatim from each brand's own site. Excluded as covered/not independent: Vice, Takomo,
STIX, Haywood, Edel, Avoda, Krank, Edison, Toulon (Callaway), Logan Olson (TaylorMade).
PHOTOS: brands' own (research/club-makers/frame.py). Hero: Artisan Golf PROTO putter on the Fort Worth workbench.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Small Golf Club Makers: 17 Independent Brands for Putters, Irons and Drivers"
DESC = ("Seventeen small, independent golf club makers: handmade and milled putters, forged irons from Fort Worth and Japan, "
        "and the few small brands still making drivers. Prices and where they're made.")
H1 = "Small Brands Making Clubs: 17 Independent Makers of Putters, Irons and Drivers"
BC = "Small Brands Making Clubs"
SLUG = "small-golf-club-makers-putters-irons-drivers"
IMG = "/images/club-makers"
SHOP = ""
P = {
 # Putters
 "lajosi": ("Lajosi Putters &middot; Melbourne", "Flow Neck Gecko, Oil Can Finish", "A$999.99 (~$691)", "https://www.lajosi.com/products/flow-neck-gecko-with-oil-can-finish",
   "Kari Lajosi is a toolmaker by trade, and his story page says he &ldquo;still completes most of the putter making process himself.&rdquo; His Workbench drops are one-offs in finishes you won&rsquo;t see anywhere else: this oil-can mallet, a Rainbow PVD DD201 blade (A$949.99, ~$657) and a black-oxide LP421 with a copper insert (A$1,199.99, ~$829). Most pieces from past drops already show sold."),
 "kronos": ("Kronos Golf &middot; California", "Touch 2.0 Groovy Grooves", "$540", "https://kronosgolf.com/onlinecatalog/touch-2gg",
   "Kronos hand-polishes and hand-paints its heads and names them after instruments: Trombone, Cornet, Hendrix. &ldquo;To us, a putter is a precision instrument,&rdquo; its about page says. The Touch 2.0 is the classic blade; the Release Si pin neck in raw stainless is $590 and the Kampe Konvertible mallet is $640."),
 "artisanp": ("Artisan Golf &middot; Fort Worth, TX", "Custom Putter", "from $1,040", "https://www.artisangolftx.com/putters",
   "Mike Taylor and John Hatfield built clubs for tour players at Nike&rsquo;s old club workshop in Fort Worth, and now machine fully custom putters there. Every build starts with a phone call with Hatfield or a fitting in Fort Worth, then a $300 deposit, and takes about four to six weeks. Artisan&rsquo;s own pages give the starting price as $1,040 on one and $1,100 on another. &ldquo;From a block of steel to the finished product, We make tools that can be trusted.&rdquo;"),
 "carbon": ("Carbon Putters &middot; Colorado", "Carbon Duke &ldquo;One in the Chamber&rdquo;", "$350", "https://carbonputters.com/product/carbon-duke-one-in-the-chamber/",
   "A family shop that mills every head from one piece of carbon steel, built to order in Colorado, and names them like an Old West posse: Ringo, Holliday, Masterson, The Kid. The Duke is down to its last one. The Ringo with a Colorado flag finish is $750, and a milled-to-order 330g Ringo is $350."),
 "hanna": ("Hanna Golf &middot; Iowa", "Des Moines Milled Putter", "$330", "https://hannagolf.com/products/des-moines",
   "&ldquo;Hanna Golf is built by an underdog, for the underdog.&rdquo; Every putter is milled to order in Iowa and ships in two to five weeks, and models are named for towns: the Des Moines, the Salt Lake Zip ($330) and the Amarillo ($295). The numbered batches sell out."),
 "tsquared": ("T Squared Putters &middot; Orchard Park, NY", "TS-503 Blade", "$349", "https://tsquaredputters.com/products/ts-503-blade",
   "Two brothers mill these in the family&rsquo;s precision machine shop near Buffalo, and instead of bending a stock head to fit you, they mill your loft and lie in. &ldquo;Nothing is outsourced. Nothing is bent.&rdquo; The custom TS-503 is $599. For a zero-torque mallet, they make the T-Zero at $429."),
 "gambit": ("Gambit Golf &middot; Ohio", "GP-Z1", "$295", "https://gambitgolf.com/products/gp-z1",
   "James, an engineer who used to design surgical instruments, put a CNC mill in his basement in early 2025. He makes serialized batches of 50 or fewer, and the GP-Z1 ships in two to four weeks. The mirror-finish GP-B2 blade is $325 and the raw GP-MM1 mallet is $300."),
 "tadmoore": ("Tad Moore", "CaraMia Hickory Putter", "$250", "https://tadmoore.com/products/caramia-putter",
   "Tad Moore has designed clubs since 1963, and now makes new hickory-shafted putters copied from the old masters: the CaraMia is a William Gibson replica with a brass sole plate, and the DUNN mallet is also $250. For a modern putter, his Custom PRO 1 ($700) is built to your specs over the phone."),
 # Irons
 "artisani": ("Artisan Golf &middot; Fort Worth, TX", "Muscle Back, Half Cavity &amp; Full Cavity", "from $360 per iron", "https://www.artisangolftx.com/irons-1",
   "&ldquo;We fit in the dirt,&rdquo; says Mike Taylor: fittings happen outdoors on real turf at the old Nike workshop. The S20 heads are forged in Japan, then assembled, stamped and paint-filled by hand in Fort Worth. You can mix all three models in one set, 4-iron to PW, and everything is made to order."),
 "p53": ("P53 &middot; Fort Worth, TX", "1/953 Series Irons", "by application", "https://p53irons.com/irons",
   "Christopher Griffin left Microsoft to make irons forged in the US from US steel, each from a single billet. The 1/953 Series is capped at 953 clients worldwide, and P53 publishes no prices; you apply or come by referral. &ldquo;My ambition: reclaim the lost legacy of great American irons.&rdquo;"),
 "baldoi": ("BALDO &middot; Himeji, Japan", "Forged Muscle Back MB, Limited to 100 Sets", "&yen;178,200 (~$1,128)", "https://baldo-golf.com/products/baldo-forged-muscle-back-iron-mb-limited-edition-of-100-sets",
   "BALDO means &ldquo;brave&rdquo; or &ldquo;bold,&rdquo; and the irons look it. The MB is a 5&ndash;PW set limited to 100. The TT Tour Pocket is &yen;191,400 (~$1,212), and the UNUS MCB, with a geometric back, is &yen;154,000 (~$975) for 6&ndash;PW. Its store is in Japan, so ask about shipping before you order."),
 "itobori": ("Itobori &middot; Aichi, Japan", "Itobori Blade", "through dealers", "https://www.itobori.com/product/iron-1/%E4%B8%80%E5%88%80%E5%BD%AB-itobori-blade/",
   "The name means &ldquo;one-cut carving,&rdquo; and the heads are shaved by hand one at a time from forged S25C. The Straight Flush has an engraved back, and the new SF Pocket CB came out in May 2026. Itobori sells through dealers and publishes no prices, and we couldn&rsquo;t find an official US dealer."),
 "vega": ("Vega &middot; Forged in Japan", "Mizar Pro Cavity Irons", "&pound;1,794 (~$2,376)", "https://www.vega-golf.com/products/vega-mizar-pro-cavity-irons",
   "Vega forges its heads in Ichikawa, Japan, and claims to have made the first forged cavity back. &ldquo;We believe in puritan design.&rdquo; The Mizar Pro Blade costs the same. Only five sets of the SS Black DLC get made per run, at &pound;2,303 (~$3,051) each."),
 "newlevel": ("New Level Golf &middot; Scottsdale, AZ", "RAW 702 MB Forged Irons", "$130 per club", "https://newlevelgolf.com/products/raw-702-mb-forged-irons",
   "One-piece forged 1020 carbon steel, and the Raw finish has no plating at all, so it rusts as you play. &ldquo;We weren&rsquo;t sure anything could look better than this MB, then we saw it in raw.&rdquo; The RAW 702 CB is also $130 a club, and chrome MBs are on sale at $130 (from $149). We first covered them in <a href='/drops/the-wedge-drop'>The Wedge Drop</a>."),
 # Drivers
 "bombtech": ("BombTech Golf &middot; Vermont", "Atomic Driver", "$357", "https://bombtechgolf.com/products/bombtech-atomic-driver",
   "Tyler Sullivan engineered BombTech&rsquo;s first driver with University of Vermont engineering students, and the brand still refuses tour money: &ldquo;We don&rsquo;t do wrenches, we don&rsquo;t pay pros to play our clubs.&rdquo; The Atomic is marked down from $497, and the black Core three wood is $107."),
 "baldod": ("BALDO &middot; Himeji, Japan", "UNUS Model DD Driver Head", "&yen;104,500 (~$661)", "https://baldo-golf.com/products/unus-driver-dd",
   "BALDO says every head shape starts from hundreds of designer sketches. The UNUS DD is a 452cc head with a forged face and carbon crown, sold as a head to build up with your shaft; the matching UNUS FD fairway is &yen;71,500 (~$453) and the TT GT5 Deep Proto driver is &yen;88,000 (~$557)."),
 "touredge": ("Tour Edge &middot; Batavia, IL", "Exotics LS Driver", "$399.99", "https://touredge.com/products/exotics-ls-driver",
   "David Glod started Tour Edge in 1986 and still owns it, which makes it the oldest of our three driver makers. The clubs are hand-assembled in Illinois, and every one carries a lifetime warranty that covers the shaft. The LS driver is down from $499.99; the Exotics Mini Driver and LS fairway are $399.99 each."),
}
SECTIONS = [
 ("Putters", "putters", ["lajosi", "kronos", "artisanp", "carbon", "hanna", "tsquared", "gambit", "tadmoore"],
  "<strong>Eight makers</strong>Where the small makers are: one person with a mill can make a great putter. Handmade one-offs, family machine shops and a basement in Ohio."),
 ("Irons", "irons", ["artisani", "p53", "baldoi", "itobori", "vega", "newlevel"],
  "<strong>Six makers</strong>Irons need a forge, so the small makers are fitters who finish heads by hand, and Japanese workshops. Two of them are in Fort Worth."),
 ("Drivers &amp; Woods", "drivers", ["bombtech", "baldod", "touredge"],
  "<strong>Three makers</strong>Drivers are the hardest thing for a small brand to make and sell. These three are still doing it."),
]
N = 17
PAIRS = {}
LIFE = []
BANDS = {
 "putters": ("In the Workshop", "Where the putters get made: a toolmaker&rsquo;s bench in Melbourne, a machine shop in Iowa, a family machine shop near Buffalo. All photos are the makers&rsquo; own.", [
   ("life-1", "Kari Lajosi working on a putter head at his bench", "Lajosi &middot; Melbourne"),
   ("life-2", "Hands checking a putter head with a level in a vise", "Lajosi &middot; the finishing work"),
   ("life-3", "A Hanna Golf maker standing in front of CNC mills and a toolbox", "Hanna Golf &middot; Iowa"),
   ("life-4", "Hanna Golf's machine shop with an American flag on the wall", "Hanna Golf &middot; the mill"),
   ("life-5", "Tad Moore sitting in his workshop with his dog", "Tad Moore &middot; designing since 1963"),
   ("life-6", "A T Squared putter held up in front of a rack of finished heads", "T Squared &middot; Orchard Park, NY")]),
 "irons": ("Forged, Ground and Fitted", "Sparks in Fort Worth, fittings on real turf, and the people who forge P53&rsquo;s irons. All photos are the makers&rsquo; own.", [
   ("life-7", "Sparks flying as a club head is ground at Artisan Golf", "Artisan &middot; Fort Worth"),
   ("life-8", "An Artisan Golf fitting tent on a driving range", "Artisan &middot; fitting in the dirt"),
   ("life-9", "Two forge workers in hard hats and safety glasses", "P53 &middot; forged in the US"),
   ("life-10", "Tongs and tooling in a forge", "P53 &middot; billet to blade"),
   ("life-11", "A golf bag on a course below desert mountains", "New Level &middot; Scottsdale"),
   ("life-12", "Hand-carved Itobori iron heads on a poker table with chips", "Itobori &middot; carved by hand")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>We cover a lot of small brands making clothes and headcovers. This one is about the clubs: seventeen small, independent makers of putters, irons and drivers, from a toolmaker in Melbourne to a basement mill in Ohio to two shops in Fort Worth working out of the building where Nike used to make tour clubs.</p>
    <p><strong>Our take: start with the putter.</strong> It is the one club where a small maker can match anyone, because a putter is one piece of steel and one person with a mill can make a great one. A milled putter from Hanna, Gambit or Carbon costs $295 to $350, about what a cast putter from a big brand costs off the rack, and it comes with someone&rsquo;s name on the back who answers your email. That is why eight of our 17 make putters.</p>
    <p><strong>Irons are a fitting, not a purchase.</strong> Hardly any small maker owns a forge, so the independents either finish forged heads by hand and fit you for them, or they are small Japanese workshops. If you live in Texas, the best version of this is a three-hour drive away: <a href="#irons">Artisan</a> fits you outdoors on real turf in Fort Worth, and P53 forges in the US from US steel and caps its whole program at 953 clients.</p>
    <p><strong>The driver is a values call.</strong> A driver takes titanium, testing and a lot of money, and the big companies release a new one every year. Only a few small brands stay in that fight, which is why we have three. Buy BombTech, BALDO or Tour Edge because you like who makes it, not because you expect it to out-tech a tour bag.</p>
    <p>Every price here comes from the maker&rsquo;s own site, checked October 15, 2026, in the store&rsquo;s currency with US dollars in brackets. Two of them don&rsquo;t publish prices at all, and most putters are made to order, so expect to wait two to six weeks.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Makers</span><span>17</span></div>
      <div class="sidebar-detail"><span class="l">Putters</span><span>8</span></div>
      <div class="sidebar-detail"><span class="l">Irons</span><span>6</span></div>
      <div class="sidebar-detail"><span class="l">Drivers</span><span>3</span></div>
      <div class="sidebar-detail"><span class="l">Closest to Austin</span><span>Artisan &amp; P53, Fort Worth</span></div>
      <div class="sidebar-detail"><span class="l">Most handmade</span><span>Lajosi, Melbourne</span></div>
      <div class="sidebar-detail"><span class="l">Oldest</span><span>Tad Moore, since 1963</span></div>
      <a href="#putters" class="sidebar-cta">Start with putters &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#IndependentGolf</span>
        <span class="hashtag">#MilledPutter</span>
        <span class="hashtag">#ForgedIrons</span>
        <span class="hashtag">#GolfClubs</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
<section class="products" style="border-top:none;padding-top:0">
  <p class="cat-kicker">For bigger direct-to-consumer club brands, read our <a href="/drops/dtc-golf-club-brands">guide to DTC golf club brands</a>. For wedges, see <a href="/drops/the-custom-wedge-report">The Custom Wedge Report</a>.</p>
</section>

<section class="products" style="margin-top:8px;">
  <div class="writeup-body" style="max-width:760px;margin:0 auto;text-align:left">
    <div class="drop-tag grass">How They&rsquo;re Made</div>
    <h2 class="products-hdr btk-story-hdr" id="how-made">How These Clubs Get Made</h2>
    <p style="text-align:left"><strong>Putters: milled, not cast.</strong> Most big-brand putters are cast: molten steel is poured into a mold, then ground and finished. Almost every small maker here mills instead. A CNC machine carves the head out of a solid block of steel, usually stainless or soft carbon steel, which takes hours per head but holds tight tolerances and gives the face its feel. Carbon Putters mills each head from a single piece of carbon steel. Hanna designs, mills and assembles in Iowa. T Squared mills your loft and lie straight into the head, instead of bending a stock head to fit you afterward. Then comes the handwork that makes each one different: Kronos hand-polishes and hand-paints, Gambit paints custom art, and Lajosi&rsquo;s oil-can, torched and rainbow finishes are applied by hand, one putter at a time.</p>
    <p style="text-align:left"><strong>Irons: forged, then finished by hand.</strong> A forged iron starts as a bar of soft carbon steel, heated and pressed into shape under enormous force, then milled, ground, polished and usually chrome plated. Cast irons are poured like most putters. The forging grades show up in the specs here: S20C at Artisan, S25C at Itobori, 1020 at New Level. P53 forges every iron in the US from a single billet of US steel. Artisan&rsquo;s heads are forged in Japan, then assembled, stamped and paint-filled by hand in Fort Worth. Itobori shaves each head by hand. New Level skips the plating altogether on its Raw irons, so they rust as you play.</p>
    <p style="text-align:left"><strong>Drivers: titanium and testing.</strong> A modern driver is a hollow titanium head, often with a separately forged face welded on and a carbon crown to save weight, built to the rules&rsquo; limits on size and how much the face can spring. BALDO&rsquo;s UNUS DD pairs a forged titanium semi-cup face with a carbon crown. Tour Edge hand-assembles its clubs in Illinois, and BombTech&rsquo;s first driver was engineered with University of Vermont engineering students. The tooling and testing are why so few small makers try.</p>
  </div>
</section>

<section class="products" style="margin-top:8px;">
  <div class="writeup-body" style="max-width:760px;margin:0 auto;text-align:left">
    <div class="drop-tag grass">What They&rsquo;re Doing Differently</div>
    <h2 class="products-hdr btk-story-hdr" id="differently">Design Choices and Strategies From the Small Makers</h2>
    <p style="text-align:left">The big brands sell technology and a new model every year. The small makers are selling something else: scarcity, a person behind every club, and a fit built into the steel. Here is how that shows up.</p>
    <p style="text-align:left"><strong>Fit built in, not bent in.</strong> T Squared mills your loft and lie straight into the head instead of bending a stock head after the fact. Artisan won&rsquo;t cut steel for a putter until it has talked to you on the phone or fitted you in Fort Worth.</p>
    <p style="text-align:left"><strong>Raw on purpose.</strong> New Level sells irons with no plating at all, so they rust as you play, and Kronos offers its Release Si in raw stainless. The bet is that golfers want a club that ages like a good pair of boots.</p>
    <p style="text-align:left"><strong>The finish is the art.</strong> Every Lajosi Workbench putter is a one-off in oil-can, torched or rainbow finishes, and Gambit paints custom art into its heads. BALDO and Itobori do the same on irons, with geometric and engraved backs that treat the back of the club as the place for design.</p>
    <p style="text-align:left"><strong>Names with a personality.</strong> Kronos names putters after instruments, Carbon after Old West gunslingers, Hanna after towns. The big brands use model numbers.</p>
    <p style="text-align:left"><strong>Scarcity by design.</strong> P53 caps its whole program at 953 clients, BALDO&rsquo;s MB runs to 100 sets, Vega makes its SS Black DLC five sets at a time, and Gambit serializes batches of 50 or fewer. Most of Lajosi&rsquo;s one-offs from past drops already show sold.</p>
    <p style="text-align:left"><strong>Made to order, so no warehouse.</strong> Hanna, Gambit, Carbon and Artisan build after you buy, which is why you wait two to six weeks and why their prices stay where they are.</p>
    <p style="text-align:left"><strong>The maker is the brand.</strong> T Squared says nothing ships until it passes &ldquo;a hands on inspection by someone whose last name is on the back of the head.&rdquo; Hanna calls itself an underdog. Tad Moore&rsquo;s name has been on clubs since 1963.</p>
    <p style="text-align:left"><strong>No tour money.</strong> BombTech says it plainly: &ldquo;we don&rsquo;t pay pros to play our clubs.&rdquo; The money goes into the price instead.</p>
    <p style="text-align:left"><strong>One thing, done well.</strong> Most of these makers do putters only or irons only. Of our 17, only BALDO shows up in two sections, irons and woods, and Artisan is the rare small shop making both putters and irons.</p>
  </div>
</section>
"""
FAQ = [
 ("Who are the best small independent golf club makers?", "For putters: Lajosi, Kronos, Artisan Golf, Carbon Putters, Hanna Golf, T Squared, Gambit Golf and Tad Moore. For irons: Artisan Golf and P53 in Fort Worth, BALDO and Itobori from Japan, Vega and New Level. For drivers: BombTech, BALDO and Tour Edge."),
 ("Are there custom golf club makers in Texas?", "Yes. Artisan Golf in Fort Worth makes fully custom putters and forged irons and fits you on real turf, and P53, also in Fort Worth, makes US-forged irons by application."),
 ("How much does a handmade or milled putter cost?", "From small makers here: about $250 to $350 for Hanna, Gambit, Carbon and T Squared, $540 to $640 for Kronos, around $1,040 to $1,100 to start for an Artisan custom build, and A$950 to A$1,200 (about $657 to $829) for a Lajosi one-off."),
 ("Why are there so few small driver brands?", "Drivers need titanium heads, testing and conformance to the rules, which costs far more than milling a putter, and the big brands release new drivers every year. BombTech, BALDO and Tour Edge are among the few independents still making them."),
 ("What is the difference between a milled and a cast putter?", "A cast putter is made by pouring molten steel into a mold and finishing it. A milled putter is carved by a CNC machine from a solid block of steel, which takes longer and holds tighter tolerances. Most small putter makers, including Carbon, Hanna, T Squared and Gambit, mill their heads."),
 ("What does forged mean on a golf iron?", "A forged iron is pressed into shape from a heated bar of soft carbon steel, such as S20C or 1020, then milled, ground and polished. Cast irons are poured into molds. Artisan, P53, BALDO, Itobori, Vega and New Level all make forged irons."),
 ("How long do custom putters take?", "Most small makers mill to order: Hanna ships in two to five weeks, Gambit in two to four, and Artisan takes about four to six weeks after your phone consult."),
]
HERO_ALT = "An Artisan Golf PROTO putter head resting on a steel workbench with copper rods and tools in the Fort Worth shop"
FRN = json.loads((ROOT / "research/club-makers/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-FF-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
def card(k, idx):
    brand, item, price, handle, copy = P[k]
    url = SHOP + handle
    fr = FRN[k]
    label = H.unescape(f"{brand} {item}").replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>'
                   for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>'
                   for j in range(len(fr)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{brand}</div>'
            f'<div class="product-name">{item} &middot; {price}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="{url}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>'
                     for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')




def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items, pos = [], 1
    for sec in SECTIONS:
        for h in sec[2]:
            items.append({"@type": "ListItem", "position": pos, "url": SHOP + P[h][3], "name": H.unescape(f"{P[h][0]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-10-15", "dateModified": "2026-10-15",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": items},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Drops & Brands", "item": "https://thegrassyissue.com/#feed"},
            {"@type": "ListItem", "position": 3, "name": BC, "item": URL}]},
    ]
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
<link rel="preload" as="image" href="{IMG}/hero.jpg" />
{ld}"""



def pq(k):
    q, who = PQ[k]
    return (f'\n<div class="pull-quote" style="margin:56px auto 24px">\n  <div class="pull-quote-inner">'
            f'&ldquo;{q}&rdquo;<span class="pull-quote-attr">&mdash; {who}</span></div>\n</div>\n')


def band(k):
    kick, line, items = BANDS[k]
    figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>' for f, alt, cap in items)
    return (f'\n<section class="products" style="margin-top:8px;">\n  <p class="cat-kicker"><strong>{kick}</strong>{line}</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


def swatch(k):
    a, ha, b, hb = PAIRS[k]
    cell = 'flex:1;padding:26px 18px 20px;font-family:var(--mono,monospace);font-size:11px;letter-spacing:.14em;text-transform:uppercase;line-height:1.7'
    return (f'  <div style="display:flex;max-width:620px;margin:6px auto 22px;border:1px solid rgba(20,20,20,.2)">'
            f'<div style="{cell};background:{ha};color:{hb}"><strong>{a}</strong><br>{ha}</div>'
            f'<div style="{cell};background:{hb};color:{ha}"><strong>{b}</strong><br>{hb}</div></div>\n')


def band(k):
    kick, line, items = BANDS[k]
    figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{H.escape(alt)}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>' for f, alt, cap in items)
    return (f'\n<section class="products" style="margin-top:8px;">\n  <p class="cat-kicker"><strong>{kick}</strong>{line}</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


def section(sec, n0):
    h2, anchor, ids, kicker = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} picks</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n' +
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def lookbooks():
    figs = "\n".join(f'  <figure><img src="{IMG}/life-{n}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>' for n, alt, cap in LIFE)
    return (f'\n<section class="products" style="margin-top:8px;">\n  <div class="drop-tag grass">{len(LIFE)} photos</div>\n'
            f'  <h2 class="products-hdr" id="lookbooks">From the Lookbooks and In the Wild</h2>\n'
            f'  <p class="cat-kicker"><strong>The pairings on people</strong>Every photo here is the brand&rsquo;s own, from its lookbook, its store or its feed. Royal blue to forest green, in the order above.</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


def main(apply_):
    ids = [k for s in SECTIONS for k in s[2]]
    assert len(ids) == N == len(set(ids)) and set(ids) == set(P), (len(ids), set(P) ^ set(ids))
    for k in ids:
        assert FRN[k] and all((ROOT / f.lstrip("/")).is_file() for f in FRN[k]), k
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
    <span>Putters, irons and drivers</span><span class="dot"></span>
    <span>17 makers &middot; prices checked October 15, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="{HERO_ALT}" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        o, n = section(s, n); body += o
        if s[1] in BANDS: body += band(s[1])
    body += faq_html()
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Kalamunda", "Lehi", "LBB", "GolfPass", "Hypebeast", "Old Ghosts", "Instagram"):
        if leak in above: bad.append("leak " + leak)
    if fin.count('class="product-card"') != N: bad.append("card count")
    if re.search(r"\bworth\b", re.sub(r"\bFort\s+Worth\b", " ", re.sub(r"<[^>]+>", " ", above), flags=re.I), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
