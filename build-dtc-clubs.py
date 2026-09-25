#!/usr/bin/env python3
"""build-dtc-clubs.py — Buying Golf Clubs Direct: Entry, Intermediate, Absolute Stick.
25 September 2026.

Lenny: "I want to do a post of DTC golf club brands- Entry, Intermediate and
Absolute stick as the three categories- Entry- Stix golf, Vice / Intermediate-
Takomo, Haywood golf, Edel golf / Absolute stick - Avoda". Then, on the options
sheet and the product-detail pass: "your call".

TIERS are Lenny's, not re-sorted. Seventeen picks: three per brand, except Vice
(two — the VGW01 wedge was dropped after it came last of 26 in MyGolfSpy's 2024
wedge test; there was no honest way to recommend it).

PRICES: read from each brand's own US store on 25 Sep 2026 in USD (Haywood via
its USD view; Vice shows cents because it prices from euros). "From" prices are
stated with what they buy. Research notes: research/dtc-clubs/.

QUOTES: one per brand, each re-checked verbatim against its source on 25 Sep
2026 (stix.golf, GOLF.com, MyGolfSpy x2, Forbes, Golf Monthly).

CAREFUL CLAIMS
  - Takomo SF002 is NOT called forged: reviewers disagree on forged vs cast.
  - Edel: fitting now runs from its Denver-area HQ (the old Liberty Hill fitting
    page redirects there); MyGolfSpy (Sep 2025) says the custom putter shop is
    still in the Austin area. The copy says exactly that.
  - Avoda: no returns after 48 hours. Said plainly, twice.
  - STIX: played clubs come back for partial refund or store credit, not cash.
Dry run by default.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-sounder.html"
OUT = ROOT / "drops/dtc-golf-club-brands.html"
PICKS = {p["n"]: p for p in json.loads((ROOT / "research/dtc-clubs/picks.json").read_text())["products"]}
SLUG = "dtc-golf-club-brands"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/dtc-clubs"
TODAY = "2026-09-25"

TITLE = "Buying Golf Clubs Direct: Six DTC Brands, From Entry to Absolute Stick"
DESC = ("Six direct-to-consumer golf club brands sorted into Entry, Intermediate and Absolute Stick: "
        "STIX, Vice, Takomo, Haywood, Edel and Avoda, with prices and where to try them in Austin.")
H1 = "Buying Golf Clubs Direct &mdash; Entry, Intermediate and Absolute Stick"
AUTHOR = {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
          "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]}

# n -> (kind line, display name, price html, card copy)
CARD = {
    1: ("Complete 10-club set", "Play 10-Club Set", "$699",
        "The Play set puts a whole bag in one box: a 460cc titanium driver, 3-wood, hybrid, 6-iron to pitching wedge, a 56&deg; wedge, a milled mallet putter, a stand bag and four headcovers. It comes in regular flex only, and STIX aims it at beginners and returning golfers."),
    3: ("Complete 14-club set", "C02 Compete 14-Club Set", "$1,599",
        "The Compete set goes up to a full 14 clubs: an adjustable carbon-crown driver, hollow-body 4&ndash;PW irons, 52/56/60 wedges and a mallet putter, in regular, stiff or X-stiff. STIX pitches it at 0&ndash;10 handicaps. MyGolfSpy scored the Compete irons 8.8, best for accuracy and best value in their class, though among the shortest."),
    5: ("Wedge set", "Compete Wedge Set, 52/56/60", "$299",
        "This set gives you three stainless wedges for less than most brands charge for one: milled faces, a dual finish rated for 5,000 swings, and a double sole grind on the 56&deg; and 60&deg;. Stiff steel shafts only."),
    7: ("Irons", "VGI01 Irons", "from $599.14 <span style=\"opacity:.5;text-decoration:line-through\">$770.57</span>",
        "The VGI01 is Vice&rsquo;s players&rsquo; iron: a triple-forged, two-piece hollow body with low offset and a thin topline, built to order in Munich on KBS Tour Lite steel. Plugged In Golf found it forgiving for its size but very low-launching, so fitting matters here. The sale price covers the stock build; custom builds start higher."),
    10: ("Zero-twist mallet putter", "VGP04 ZT", "$239",
         "The VGP04 ZT runs the shaft axis through the head&rsquo;s centre of mass, Vice&rsquo;s take on the zero-torque putter, in an all-steel 380g mallet. Golf Monthly called it very stable at nearly half the price of rivals, with a high-pitched sound at impact."),
    12: ("Game-improvement irons", "Iron 101 MKII", "$579",
         "The 101 MKII is a hollow-body game-improvement set, 5-iron to gap wedge, with KBS Tour Lite or Tour shafts at no extra cost. MyGolfSpy named it the best game-improvement iron of 2026, most accurate in the test and about a yard and a half short of average."),
    14: ("Players cavity-back irons", "Iron 301 CB", "$649",
         "The 301 CB is forged from S20C steel as a compact players&rsquo; cavity back, 4-iron to pitching wedge. It finished third in MyGolfSpy&rsquo;s 2023 players&rsquo; iron test and took its best-value award."),
    15: ("Wedge", "Skyforger 002", "$99",
         "Takomo designed the Skyforger 002 with George and Wesley Bryan, and it comes in lofts from 46&deg; to 60&deg; with two grinds. Plugged In Golf called it one of the best buys in golf; the grind choice is narrower than the big brands offer."),
    17: ("Forged combo irons", "CB2 + MB2 Combo", "from $849",
         "This combo pairs forged, fully CNC-milled cavity backs in the long irons with muscle backs from the 7-iron down, in 1020 carbon steel. Haywood builds it to order in Vancouver and ships in about three weeks; it is meant for 0&ndash;11 handicaps."),
    19: ("Forged wedge", "Signature Wedge", "from $118",
         "The Signature wedge is forged S20C with a CNC-milled face and grooves, in lofts from 48&deg; to 60&deg; and a raw or brushed finish. Plugged In Golf found spin on par with the big names and the feel on the firm side."),
    21: ("Try-before-you-buy", "7-Iron Purchase Program", "from $100",
         "Haywood builds you one 7-iron to your specs in any of its iron models. You keep it, and its price comes back as a code toward a full set that never expires. The 7-iron itself cannot be returned."),
    22: ("Forged players irons", "SMS Pro Irons", "$190 per club &middot; $1,330 for 4&ndash;PW",
         "The SMS Pro is forged from 1025 carbon steel with three movable weights you shift to control the clubface; a free SMS Pro wedge comes with a full set. It ships in two to three weeks. MyGolfSpy&rsquo;s 2023 test had it long but inconsistent, so get fitted first."),
    24: ("Wedge", "SMS Pro Wedge", "$180",
         "The SMS Pro wedge carries a patented flip weight you set toward the heel, the toe or neutral, in four grinds. It took Silver on Golf Digest&rsquo;s 2026 Hot List, with testers praising its bunker play."),
    25: ("Fitted putter", "Array Putter", "$350",
         "The Array has a forged, milled face in an aluminium frame and takes five interchangeable hosels and six alignment plates, so it can be set to how you actually aim. This is the fitting idea Edel was founded on."),
    26: ("One-length irons", "Origin Same Length", "from $985",
         "The Origin Same Length makes every iron one length, with one head weight and one setup. The heads are forged carbon steel with a 4mm topline. The $985 buys 6-iron to pitching wedge; 4&ndash;PW is $1,379. Golf Monthly found the feel soft and the concept an adjustment."),
    28: ("Curved-face irons", "Origin Curved, Traditional Length", "from $1,712",
         "This is the curved face from Bryson&rsquo;s U.S. Open set in conventional lengths: a milled bulge across the face to straighten off-centre strikes. The $1,712 buys 5&ndash;PW; 4&ndash;PW is $1,997. Golf Monthly saw impressive dispersion at high speed and less control on softer shots."),
    30: ("Wedge", "W3 Wedge", "$192",
         "The W3 is Avoda&rsquo;s high-bounce wedge, forged, with a very thin sole, sold as a gap, sand or lob. Plugged In Golf called it an excellent short-game tool that rewards leaning the shaft."),
}

BRANDS = [
    # tier, key, name, anchor, kicker, picks, quote
    ("Entry", "stix", "STIX", "stix",
     "<strong>Chicago &middot; complete sets &middot; read 25 September 2026</strong>"
     "Gabe Coyne started STIX in Chicago in 2020 to sell complete, matte-black sets online, with no tour players "
     "and no yearly driver. A six-question quiz stands in for a fitting. You get 30 days: unused clubs come back "
     "for a refund, played clubs for a partial refund or store credit.",
     [1, 3, 5], "stix"),
    ("Entry", "vice", "Vice", "vice",
     "<strong>Munich &middot; built to order &middot; read 25 September 2026</strong>"
     "Vice launched in 2012 as a direct-to-consumer golf ball, then moved into clubs after merging with HIO, a "
     "Munich fitting studio, in 2023. Clubs are built to order in Munich. Individual clubs come back within 30 "
     "days even after you have played them, with a free return label.",
     [7, 10], "vice"),
    ("Intermediate", "takomo", "Takomo", "takomo",
     "<strong>Turku, Finland &middot; online only &middot; read 25 September 2026</strong>"
     "Takomo is Sebastian Haapahovi&rsquo;s company, started in Finland in 2020. The design team works in Finland; a manufacturer in "
     "Taiwan makes the clubs. There is a free online fitting quiz, and you can hit the stock 7-iron of a set and "
     "still return it within 30 days. Custom builds are final.",
     [12, 14, 15], "takomo"),
    ("Intermediate", "haywood", "Haywood", "haywood",
     "<strong>Vancouver &middot; built in-house &middot; read 25 September 2026</strong>"
     "Josh Haywood started the company in Vancouver in 2018, after a shop wanted $700 for three wedges, and told "
     "Forbes in 2023 that it was still bootstrapped, with no outside investors. Every club is custom-built in-house. US prices include duties, so nothing "
     "extra is due at the door.",
     [17, 19, 21], "haywood"),
    ("Intermediate", "edel", "Edel", "edel",
     "<strong>Colorado and Texas &middot; fitting first &middot; read 25 September 2026</strong>"
     "David Edel began making putters in 1996 and built a fitting system around where golfers actually aim. Pins "
     "&amp; Aces bought the company in a deal announced in January 2025, cut the iron prices, and brought back the "
     "custom putter work in the Austin area.",
     [22, 24, 25], "edel"),
    ("Absolute Stick", "avoda", "Avoda", "avoda",
     "<strong>Pittsburgh &middot; fitting required &middot; read 25 September 2026</strong>"
     "Tom Bailey set out to build himself a set of irons and ended up making the one-length, curved-face set "
     "Bryson DeChambeau won the 2024 U.S. Open with. Every Avoda is built to order after a fitting, online or at "
     "one of more than 120 fitters. There are no returns after 48 hours.",
     [26, 28, 30], "avoda"),
]

TIERS = {
    "Entry": ("tier-entry", "Entry",
              "Entry is where the direct model is simplest: a full bag, or a set of irons, for less than a single "
              "set costs at retail. STIX sells everything in one box; Vice lets you build clubs one at a time and "
              "send them back after playing them."),
    "Intermediate": ("tier-intermediate", "Intermediate",
                     "This is the middle tier. All three sell irons you would find in a good player&rsquo;s "
                     "bag for well under the big-brand price, and all three give you a real way to try before you "
                     "commit."),
    "Absolute Stick": ("tier-absolute-stick", "Absolute Stick",
                       "Absolute Stick is one brand, and the fitting is not optional. Avoda builds irons you will "
                       "not find anywhere else, to your numbers, and does not take them back."),
}

PQ = {
    "stix": ("When did buying golf clubs get so complicated? Clubs became so over-designed, over-hyped, and "
             "over-priced. It didn&rsquo;t make sense to me, that&rsquo;s why I started Stix.",
             "Gabe Coyne, founder, on stix.golf"),
    "vice": ("We always heard fellow golfers complaining about the high prices of golf balls and when we "
             "investigated the market more closely we were surprised by the steep mark-ups by all the middlemen "
             "involved in the process.",
             "Ingo D&uuml;llmann, Vice co-founder, to GOLF.com, February 2019"),
    "takomo": ("This acquisition represents a natural evolution of our mission to provide technologically "
               "advanced, beautifully designed equipment that golfers can actually afford.",
               "Sebastian Haapahovi, Takomo CEO, on buying Otso&rsquo;s putter technology, via MyGolfSpy, December 2025"),
    "haywood": ("It wasn&rsquo;t that I didn&rsquo;t have the money, it was more that I didn&rsquo;t understand why I "
                "should pay this much for new wedges.",
                "Josh Haywood, founder, to Forbes, February 2023"),
    "edel": ("We want a true, forged player&rsquo;s iron that&rsquo;s very forgiving, very approachable and "
             "that&rsquo;s not going to break the bank.",
             "Nick Mertz, owner of Pins &amp; Aces and Edel, to MyGolfSpy, September 2025"),
    "avoda": ("If I wouldn&rsquo;t use it, I&rsquo;m not going to sell it to someone, and that is the truth.",
              "Tom Bailey, Avoda founder, to Golf Monthly, June 2024"),
}


def pq(key):
    t, a = PQ[key]
    return (f'\n<!-- TGI-DTC-PQ-{key} -->\n<div class="pull-quote">\n  <div class="pull-quote-inner">'
            f'&ldquo;{t}&rdquo;<span class="pull-quote-attr">&mdash; {a}</span></div>\n</div>\n'
            f'<!-- /TGI-DTC-PQ-{key} -->\n')


def card(n, idx, brand):
    p = PICKS[n]
    kind, name, price, copy = CARD[n]
    frames = p["local"]
    label = H.escape(f"{brand} {H.unescape(name)}", quote=True)
    imgs = "".join(
        f'<div class="pg-frame"><img src="{f}" alt="{label} &middot; view {i+1} of {len(frames)}" loading="lazy" /></div>'
        for i, f in enumerate(frames))
    dots = "".join(
        f'<button class="pg-dot{" on" if i == 0 else ""}" data-i="{i}" aria-label="View image {i+1}"></button>'
        for i in range(len(frames)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(frames)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(frames)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{brand} &middot; {kind}</div>'
            f'<div class="product-name">{name} &middot; {price}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="{p["url"]}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


# TIER BANDS. Lenny, 25 Sep 2026: "make the title sections between categories a
# little bigger or better to better see the difference between Entry /
# Intermediate / Stick". The tier heads were the same size and style as the
# brand heads under them, so the three tiers read as six equal sections. Each
# tier now opens with a heavy green rule, the tier number, a large green title,
# the brands and price span, then the intro. (A full green band was tried first;
# Lenny: "a little too much - let's find a nice middle ground".)
TIER_META = {
    "Entry": ("01", "STIX &middot; Vice", "Full sets from $699 &middot; clubs from $239"),
    "Intermediate": ("02", "Takomo &middot; Haywood &middot; Edel", "Iron sets from $579 &middot; wedges from $99"),
    "Absolute Stick": ("03", "Avoda", "Built to order from $985"),
}
TIER_CSS = """
.tier-band{max-width:1336px;margin:72px auto 8px;padding:26px 0 30px;border-top:4px solid var(--grass,#2D4A2B);border-bottom:1px solid rgba(20,20,20,.15)}
@media(max-width:1400px){.tier-band{margin-left:32px;margin-right:32px}}
@media(max-width:700px){.tier-band{margin-left:20px;margin-right:20px}}
.tier-band .tier-count{font-family:var(--mono);font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--grass,#2D4A2B);font-weight:600}
.tier-band h2.tier-title{font-family:var(--serif);font-weight:700;font-size:clamp(40px,5.2vw,64px);line-height:1;letter-spacing:-.02em;margin:10px 0 12px;color:var(--grass,#2D4A2B);text-align:left;border:0;padding:0}
.tier-band .tier-brands{display:inline-block;font-family:var(--mono);font-size:12px;letter-spacing:.16em;text-transform:uppercase;margin:0 18px 14px 0}
.tier-band .tier-price{display:inline-block;font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;opacity:.6;margin:0 0 14px}
.tier-band p.tier-intro{max-width:720px;font-size:16.5px;line-height:1.65;margin:0}
"""


def tier_head(t):
    anchor, label, text = TIERS[t]
    num, brands, price = TIER_META[t]
    return (f'\n<section class="tier-band" id="{anchor}">\n'
            f'  <div class="tier-count">Tier {num} of 03</div>\n'
            f'  <h2 class="tier-title">{label}</h2>\n'
            f'  <div class="tier-brands">{brands}</div>\n'
            f'  <div class="tier-price">{price}</div>\n'
            f'  <p class="tier-intro">{text}</p>\n</section>\n')


def brand_section(b, n0):
    tier, key, name, anchor, kicker, ns, _ = b
    cards = "\n".join(card(n, n0 + i, name) for i, n in enumerate(ns))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{tier} &middot; {name}</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{name}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid">\n{cards}\n    </div>\n</section>\n'), n0 + len(ns)


PROSE = 'style="max-width:760px;font-size:16px;line-height:1.7;"'

TAKE = f"""
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Buying golf clubs direct from the people who make them has stopped being a gamble. The six brands here skip the shop and the tour contracts, and the money goes into the clubs instead. The irons in the middle of this page hold their own against clubs that cost twice as much, and independent testers keep saying so.</p>
    <p>The tiers are built around how you would actually shop. <strong>Entry</strong> is STIX and Vice: a whole bag for under $1,600, or clubs you can play for a month and still send back. <strong>Intermediate</strong> is Takomo, Haywood and Edel: forged irons for $579 to $1,330, from brands that give you a real way to try before you buy. <strong>Absolute Stick</strong> is Avoda: the one-length, curved-face irons from Bryson&rsquo;s U.S. Open, built to order after a fitting and not returnable.</p>
    <p>If we were buying today, we would start in the middle. Order Haywood&rsquo;s custom 7-iron for $100, and if you like it, put that money toward the forged combo. Or buy Takomo&rsquo;s 301 CB at $649 and hit the 7-iron before deciding to keep it. Either way you end up with forged irons, fitted to you, for less than one big-brand set.</p>
    <h2 class="products-hdr btk-story-hdr">How Buying Direct Works</h2>
    <p>Without a shop there is no one to hand you a 7-iron, so each brand solves fitting its own way. STIX and Takomo ask you a few questions online. Haywood builds you one club first. Vice sends you to Club Champion to hit a demo. Edel and Avoda want a proper fitting, at a certified fitter or with a swing video.</p>
    <p>The part that varies most is the return policy, so read it before you pay. Vice takes played clubs back. STIX gives a partial refund or credit on played clubs. Takomo and Haywood let you hit the 7-iron of a stock set, but custom builds are final. Avoda takes nothing back after 48 hours.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>6, in 3 tiers</span></div>
      <div class="sidebar-detail"><span class="l">Entry</span><span>STIX, Vice</span></div>
      <div class="sidebar-detail"><span class="l">Intermediate</span><span>Takomo, Haywood, Edel</span></div>
      <div class="sidebar-detail"><span class="l">Absolute Stick</span><span>Avoda</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$99&ndash;$1,712</span></div>
      <div class="sidebar-detail"><span class="l">Easiest return</span><span>Vice, 30 days, played</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Haywood 7-iron, then the combo</span></div>
      <div class="hashtags">
        <span class="hashtag">#DTCGolf</span>
        <span class="hashtag">#GolfClubs</span>
        <span class="hashtag">#ForgedIrons</span>
        <span class="hashtag">#ClubFitting</span>
        <span class="hashtag">#AustinGolf</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

AUSTIN = f"""
<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr" id="austin">Where to Try Them in Austin</h2>
  <div {PROSE}>
    <p><strong>Vice</strong> sends golfers to Club Champion to hit its clubs, and Club Champion has two Austin studios: on North Capital of Texas Highway and inside Golfinity on FM 620. Call ahead to check the Vice demos are in.</p>
    <p><strong>Avoda</strong> lists Common Ground Golf in Bertram, about an hour northwest, as its fitter for the Austin area. You can also send Avoda a swing video and get specs back within 48 hours, free.</p>
    <p><strong>Edel</strong> still builds its custom putters in the Austin area, but its fitting experience now runs from its headquarters outside Denver. Its fitter locator lists certified fitters elsewhere.</p>
    <p><strong>STIX, Takomo and Haywood</strong> are online only. Use the quiz, or in Haywood&rsquo;s case the 7-iron, and let the return window do the rest.</p>
  </div>
</section>
"""

PICTURES = f"""
<section class="products" style="margin-top:8px;">
  <h2 id="in-the-workshop">From the Brands</h2>
  <p class="cat-kicker"><strong>Photography &middot; the brands&rsquo; own</strong>A dawn round from STIX, and Haywood&rsquo;s forged irons, before and after the Vancouver workshop finishes them.</p>
  <div class="ig-grid">
  <figure><img src="{IMG}/life-stix-bridge.jpg" alt="Golfers crossing a bridge on a golf course at sunrise, from STIX" loading="lazy" /><figcaption class="ig-cap">STIX &middot; first light</figcaption></figure>
  <figure><img src="{IMG}/life-haywood-build.jpg" alt="A club being ground on a wheel in Haywood Golf&rsquo;s workshop, sparks flying" loading="lazy" /><figcaption class="ig-cap">Haywood &middot; built in-house</figcaption></figure>
  <figure><img src="{IMG}/life-haywood-irons.jpg" alt="Two Haywood forged irons resting on grass" loading="lazy" /><figcaption class="ig-cap">Haywood &middot; forged irons</figcaption></figure>
</div>
</section>
"""

FAQ = [
    ("What is a DTC golf club brand?",
     "A direct-to-consumer brand sells clubs straight to you, mostly online, instead of through golf shops. Without the retail margin or tour player contracts, prices come in well under the big brands."),
    ("Are DTC golf clubs as good as big-brand clubs?",
     "Many are. Takomo's 101 MKII was MyGolfSpy's best game-improvement iron of 2026, and Edel's SMS Pro wedge took Silver on Golf Digest's 2026 Hot List. Quality varies by model, so read independent tests before you buy."),
    ("Can I try DTC clubs before I buy?",
     "Usually, in some form. Vice clubs can be hit at Club Champion; Haywood builds you one 7-iron and credits it toward a set; Takomo lets you hit the stock 7-iron and still return the set; Avoda does free online fittings from a swing video."),
    ("Which DTC brands take back clubs you have played?",
     "Vice takes back individual clubs within 30 days even after play, with a free return label. STIX offers a partial refund or store credit on played clubs within 30 days. Avoda clubs cannot be returned after 48 hours."),
    ("Where can I get fitted for DTC clubs near Austin?",
     "Club Champion's two Austin studios stock Vice, so call ahead for demos. Avoda lists Common Ground Golf in Bertram as its Austin-area fitter. Edel's fittings run from its Denver-area headquarters."),
    ("What are Avoda irons?",
     "Avoda makes forged irons in one-length, combo-length and curved-face versions. Founder Tom Bailey built the one-length, curved-face set Bryson DeChambeau used to win the 2024 U.S. Open. Sets start at $985 for 6-iron to pitching wedge."),
]


def faq_html():
    rows = "\n".join(
        f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>'
        for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')


def head_top():
    art = {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC, "url": URL,
           "image": f"https://thegrassyissue.com{IMG}/hero.jpg", "datePublished": TODAY, "dateModified": TODAY,
           "author": AUTHOR,
           "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
           "mainEntityOfPage": {"@type": "WebPage", "@id": URL}}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
        {"@type": "ListItem", "position": 2, "name": "Drops & Brands", "item": "https://thegrassyissue.com/#feed"},
        {"@type": "ListItem", "position": 3, "name": "DTC Golf Club Brands", "item": URL}]}
    t, d = H.escape(TITLE, quote=True), H.escape(DESC, quote=True)
    og = f"https://thegrassyissue.com{IMG}/hero.jpg"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{t}</title>
<meta name="description" content="{d}" />
<meta name="author" content="Lenny Harrington">
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
<script type="application/ld+json">
{json.dumps(art, indent=1, ensure_ascii=False)}
</script>
<script type="application/ld+json">
{json.dumps(faq, indent=1, ensure_ascii=False)}
</script>
<script type="application/ld+json">
{json.dumps(crumbs, indent=1, ensure_ascii=False)}
</script>
"""


def main(apply_):
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    head_rest = head_rest.replace("</style>", TIER_CSS + "</style>", 1)
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    n_picks = sum(len(b[5]) for b in BRANDS)
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  DTC Golf Club Brands</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>6 brands &middot; 3 tiers</span><span class="dot"></span>
    <span>{n_picks} picks &middot; $99&ndash;$1,712</span>
  </div>
</header>

<section class="drop-hero">
  <img class="drop-hero-img" src="{IMG}/btk-hero.jpg" alt="A golfer silhouetted mid-swing against the evening sky, from STIX" fetchpriority="high" />
</section>
"""
    body += TAKE + AUSTIN + PICTURES
    n, last = 1, None
    for b in BRANDS:
        if b[0] != last:
            body += tier_head(b[0]); last = b[0]
        s, n = brand_section(b, n)
        body += s + pq(b[6])
    body += faq_html()
    out = head_top() + head_rest + body + tail
    print(f"  {n-1} cards, {len(PQ)} pull-quotes, {len(FAQ)} FAQs")
    if not apply_:
        print("  dry run — pass --apply")
        return
    OUT.write_text(out, encoding="utf-8")
    verify(n - 1)


def verify(n_cards):
    fin = OUT.read_text(encoding="utf-8")
    bad = []
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->|<script\b.*?</script>", "",
                   fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    for leak in ("Sounder", "McAteer", "Raglan"):
        if leak in above:
            bad.append(f"{leak} leaked from the donor")
    if fin.count('class="product-card"') != n_cards or n_cards != 17:
        bad.append("card count")
    if set(CARD) != {n for b in BRANDS for n in b[5]}:
        bad.append("CARD keys vs BRANDS picks")
    for k, (t, a) in PQ.items():
        if fin.count(t[:50]) != 1:
            bad.append(f"pull-quote {k} x{fin.count(t[:50])}")
    txt = re.sub(r"<[^>]+>", " ", fin)
    if re.search(r"\bworth\b", txt, re.I):
        bad.append("banned word")
    if re.search(r"Skyforger[^.]{0,60}forged|forged[^.]{0,30}Skyforger", txt):
        bad.append("Skyforger called forged")
    for p in PICKS.values():
        for f in p["local"]:
            if not (ROOT / f.lstrip("/")).is_file():
                bad.append(f"missing {f}")
    for f in ("btk-hero", "hero", "life-stix-bridge", "life-haywood-build", "life-haywood-irons"):
        if not (ROOT / f"images/dtc-clubs/{f}.jpg").is_file():
            bad.append(f"missing {f}.jpg")
    if bad:
        OUT.unlink()
        sys.exit("! removed. " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
