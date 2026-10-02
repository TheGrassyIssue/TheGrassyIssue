#!/usr/bin/env python3
"""build-streetwear26.py — The 9 Best Golf Streetwear Brands in 2026 (same URL as the Aug 30 top-five).

1 October 2026. Lenny: "let's update the streetwear page- these are the new picks, keep the position on the
homepage and URL" with nine brands and an award each, then "6 pieces per brand, with the quotes and short write
ups per brand, then make sure we have good images that are on-brand".
The 30 August top-five version and its builder are archived in research/streetwear-oct/.

FACTS: every product read from the brand's own store on 1 Oct 2026 (research/streetwear-oct/picks.json; Shopify
products.json, Metalwood from its product pages). Quotes verbatim: Huynh (Golf Digest, Nov 2022), Young (FORE),
Malbon (Complex, 12 Jul 2024), Ajanaku (Axios Detroit, Jul 2025), Tan (Public Drip About page), Midiron and Hidden
Links Society (their own sites), Clamp (Meet the Team), ALD (as quoted by Golf Digest, 9 May 2024).
Ownership facts carried from the Aug 30 status check (Malbon/Anthos, Eastside/Centric).
GBP at 1.3449 and AUD at 0.6951 to USD.
PHOTOS: brands' own store and campaign images, localised to /images/streetwear-oct.
"""
import html as H
import json
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "best-golf-streetwear-brands-2026"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/streetwear-oct"
CHECKED = "1 October 2026"
PK = json.loads((ROOT / "research/streetwear-oct/picks.json").read_text())

TITLE = "The 9 Best Golf Streetwear Brands in 2026"
DESC = ("The nine best golf streetwear brands of 2026, each with an award: Students, Metalwood, Malbon, Eastside, "
        "Public Drip, Midiron, Clamp, Aimé Leon Dore and Hidden Links Society, with six pieces from each.")
H1 = "The 9 Best Golf Streetwear Brands in 2026"


def gbp(x):
    return f"&pound;{x:,.0f} (~${x*1.3449:,.0f})"


def aud(x):
    return f"A${x:,.0f} (~${x*0.6951:,.0f})"


# per brand: award, display name, profile link, write-up paragraphs, pull quote, band captions, product copy x6
BRANDS = [
 dict(k="students", award="Best Overall", name="Students Golf",
  link=("/drops/students-golf-our-15-favorites", "Our 15 favourite Students pieces"),
  body=["Students is the most complete brand in golf streetwear right now. Michael Huynh built Publish, a Los Angeles streetwear label, before he turned to golf, and it shows in the cut: pleats that hang properly, nylon that looks like outerwear rather than rainwear, knitwear you would wear to dinner.",
        "It is also the deepest catalogue on this list, with more than 600 pieces in stock and a fresh fall drop that went live the morning we checked. You can dress head to toe out of Students, and it sits in Bodega, HBX and Culture Kings next to the labels those shops are known for."],
  pq=("My past as a designer is rooted in streetwear, so it gets me excited to bring those principles to golf in ways that the sport hasn&rsquo;t had access to yet.", "Michael Huynh, Students founder, to Golf Digest, November 2022"),
  band=["The Art Dept. tee, on model", "The full fit", "Through the smoke"],
  copy=["A boxy Mack-style jacket in a print Students says was inspired by an oil slick on a course pond. The statement piece of the fall drop.",
        "A cable-knit polo sweater with a structured collar, collegiate and relaxed. The piece to wear from the first tee to dinner.",
        "Worn-in work pants with reinforced detailing, cut straight and roomy. They look like workwear and swing like golf trousers.",
        "A terry-bodied short-sleeve polo with woven utility details. Soft, structured and a long way from pique.",
        "Lightweight nylon pants in Students&rsquo; own custom camo, with a relaxed utility cut and drawcord hems.",
        "A full sherpa jacket for cold mornings, clean and utilitarian. The warmest thing in the drop."]),
 dict(k="metalwood", award="Best Retro", name="Metalwood Studio",
  link=("/drops/brand-to-know-metalwood-studio", "Read the Metalwood profile"),
  body=["Nobody mines old golf and old sport better than Metalwood. Cole Young left Malbon in 2020 to start it, and the result looks like a pro shop from 1998 run by skaters: soccer jerseys, gradient mesh, a G.H.BASS moc toe and adidas golf shoes built on a Predator upper.",
        "The product copy is half the fun. The Sportocasin listing reads &ldquo;RIP Bobby Jones he woulda loved 10k MOI Drivers,&rdquo; and the MC70 page admits everyone is mad at him for calling it &ldquo;soccer&rdquo;. It is still founder-run, and the entry price is a $62 tee."],
  pq=("I was done helping people build their own empires. I knew I could do it, so I was just going to do it for me.", "Cole Young, Metalwood Studio founder, to FORE Magazine"),
  band=["Metalwood on the course", "The adidas collab, off the pitch", "Studio session"],
  copy=["A pale yellow soccer jersey with &ldquo;King of the Green&rdquo; on the chest and a Metalwood repair-centre graphic on the back. The retro pick in one garment.",
        "adidas Originals and Metalwood put a Predator-style upper on a spiked golf sole, in solar yellow. The most talked-about golf shoe of the year.",
        "A black leather moc-toe with G.H.BASS, which reads as a loafer until you see the sole. It comes boxed with a Metalwood dust bag.",
        "A pale blue gingham overshirt with oversized utility pockets. Metalwood says the pockets hold three iPads and a foot-long sandwich.",
        "A heavyweight olive hood with the Dewey logo across the chest in a hardcore-flyer scrawl.",
        "A long-sleeve mesh top that fades in vertical stripes, with a boxed logo across the chest."]),
 dict(k="malbon", award="Most Influential", name="Malbon Golf",
  link=("/drops/no-budget-malbon", "No Budget: Malbon&rsquo;s most expensive pieces"),
  body=["Every brand on this page owes something to Malbon. Stephen and Erica Malbon started it in 2017 from an Instagram mood board and a pro shop on Fairfax, and proved that golf clothing could sit next to streetwear on a shop rack. The collaborations, from Nike and New Balance to Daniel Arsham and Bushmills, set the template everyone now follows.",
        "It is a bigger company now. Malbon raised a $33 million round led by Anthos Capital, Aaron Heiser, formerly of Nike, is chief executive, and the range runs to GORE-TEX outerwear and cashmere. The influence is not in question, and the six below show both the old Malbon and the new one."],
  pq=("I thought of it more as just trying to inspire young people that old stuffy golfers aren&rsquo;t as lame as you think.", "Stephen Malbon, to Complex, July 2024"),
  band=["Malbon on course", "The Dornoch anorak", "The adidas Samba golf shoe"],
  copy=["A colour-blocked pullover in 2-layer GORE-TEX, engineered with 686, with waterproof zips. The new Malbon at its most technical.",
        "A wool-cashmere crewneck in forest green with the Malbon script at chest and sleeve. The quiet end of the range.",
        "The adidas Samba rebuilt as a golf shoe in pale green leather with a gum sole. Malbon&rsquo;s best-known kind of collab.",
        "A lightweight short-sleeve windshirt with an elastic waist and Malbon script across the back. Built to wear all year.",
        "The Fairway Polo in an all-over Arsham monogram, from the Daniel Arsham collection.",
        "A heavyweight tee with two palms on the back. The cheapest way into Malbon at $68."]),
 dict(k="eastside", award="Best Cultural Point of View", name="Eastside Golf",
  link=("/drops/fall-drops-eastside-students-devereux", "Eastside in our fall drops"),
  body=["Eastside Golf has the clearest point of view in the sport. Olajuwon Ajanaku and Earl Cooper started it to put people who look like them into golf on their own terms, and the Swingman logo says it before the clothes do. It has an Air Jordan collaboration behind it and a following well outside golf.",
        "Centric Brands formed a joint venture with Eastside in August, so it now has a bigger partner behind it. The fall range is the strongest we have seen from them: corduroy, a space-themed polo from the Zero Gravity collection and striped knitwear, and none of it over $140."],
  pq=("I was tired of trying to fit into a mold. Why not come into the sport as I am.", "Olajuwon Ajanaku, Eastside Golf co-founder, to Axios Detroit, July 2025"),
  band=["The Fall &rsquo;26 Gravity look", "Three balls and a Swingman", "The Swingman on the tee"],
  copy=["A navy and cranberry corduroy check with a Swingman at the chest and script across the back. Eastside calls it new ground, and it is the best thing in the drop.",
        "A pique polo printed with a course running out into space, from the Zero Gravity collection.",
        "A double-knit crew with the Eastside Golf name debossed into the fabric and a tonal Swingman. Subtle for Eastside.",
        "A tech-stretch hoodie in blue camo with the script logo, made to swing in on cold mornings.",
        "A soft knit crew in wild grape with a small embroidered Swingman. The easiest piece here to wear anywhere.",
        "A wool-blend polo sweater in green and navy vertical stripes. Vintage in shape, loud in colour."]),
 dict(k="publicdrip", award="Best Emerging Brand", name="Public Drip",
  link=("/drops/public-drip-brooklyns-muni-born-golf-label", "Read the Public Drip profile"),
  body=["Public Drip is the brand on this list most likely to be twice the size next year. Neil Tan started it in Brooklyn in 2020 after getting back into golf at Van Cortlandt Park in the Bronx, and it is made for public-course golfers rather than members.",
        "The clothes are menswear first: herringbone, waffle knit, double-pleated trousers and a felt &ldquo;P&rdquo; on denim. The FW26 Nightshift collection is shot in a clothing shop rather than a clubhouse, and nothing in it costs more than $170."],
  pq=("Creating high-quality, yet approachable products is our nod to the accessibility of the public spaces that made us.", "Neil Tan, Public Drip founder, on the brand&rsquo;s About page"),
  band=["The &ldquo;P&rdquo; Script cap", "Nightshift, in the shop", "FW26: Nightshift"],
  copy=["A long-sleeve polo in a textured waffle knit, in a stretchy nylon blend. The Nightshift piece we would buy first.",
        "A cotton-blend half zip in a soft herringbone knit, in coffee. Menswear with a golf collar.",
        "Double-pleated trousers in a lightweight stretch nylon, modelled on a suit trouser, in pinstripe.",
        "A long-sleeve version of Public Drip&rsquo;s player&rsquo;s mock, in a soft cotton blend with an embroidered script.",
        "A five-panel denim cap with a felt &ldquo;P&rdquo; script and a leather strap. The brand&rsquo;s best-known logo.",
        "The core Public Athlete polo with a knitted contrast collar and an embossed &ldquo;P&rdquo;. The on-course staple."]),
 dict(k="midiron", award="Best Design Language", name="Midiron",
  link=("/drops/brand-to-know-midiron", "Read the Midiron profile"),
  body=["Midiron has the most consistent look of any brand here. The Australian label shoots everything at night on empty courses, cuts every polo boxy and untucked, and writes product copy better than anyone in golf, without ever putting a founder&rsquo;s name to it.",
        "The catalogue is tiny, eight pieces in stock, and every one of them looks like it came from the same world: camo, varsity stripes and caps that read &ldquo;For the love of G*lf&rdquo;. The Big Stick headcover is &ldquo;for the club you trust the least and rely on the most.&rdquo;"],
  pq=("golf clothing never felt like the rest of our wardrobe. It belonged on the course, but nowhere else.", "Midiron, on its own site"),
  band=["After dark, in the bunker", "The Detour stripe, on course", "Tree camo at night"],
  copy=["A boxy performance polo in bush camo that is cut to wear untucked. Midiron&rsquo;s line is that it isn&rsquo;t a golf polo.",
        "Midiron&rsquo;s take on a vintage 90s polo in wide black and white stripes, on the same boxy fit.",
        "The Tour Spec polo in tree camo with a varsity-style Midiron across the chest.",
        "An unstructured ripstop cap in camo with &ldquo;For the love of G*lf&rdquo; embroidered on the front.",
        "A black twill cap made, in Midiron&rsquo;s words, for the days you stripe one down the middle and still make a double.",
        "A padded camo driver cover for the club you trust the least and rely on the most."]),
 dict(k="clamp", award="Best Under-the-Radar", name="Clamp Golf Company",
  link=("/drops/brand-to-know-clamp-golf-company", "Read the Clamp profile"),
  body=["Clamp is a headcover workshop in Yorkshire, and most golfers in the US have never heard of it. They should have. Its reworked covers are cut from real Palace, Supreme, Carhartt and Nike ACG bags and packs, so every set is a one-off, and they are the best streetwear objects in golf right now.",
        "The base collection of leather and tweed covers is solid; the reworked and collab pieces are the best we have seen in a while. They sell out in drops: four of the six below were in stock the day we looked, and we kept the Supreme hybrid and the Nike ACG set, both sold out, because they are the best things Clamp has made."],
  pq=("What started as an idea for more personal headcovers has grown into a workshop making custom pieces for golfers and clubs around the world.", "Clamp Golf Company, Meet the Team"),
  band=["The Clamp workshop", "The Military Range", "Made for a football club"],
  copy=["Cut from a Palace bag with leather backing: driver, wood, hybrid and a blade putter cover. The priciest set here, and the most streetwear thing Clamp makes.",
        "A single grey mallet cover with the red Supreme tag. The cheapest way into the reworked line if you only want to dress the putter.",
        "A pale grey hybrid cover cut from a Supreme bag, with the box-logo lettering repeated in tone and a toggle and drawcord closure. Gone, but it shows what Clamp does with Supreme.",
        "Black Carhartt duck canvas with the square Carhartt label on the driver, brass rivets and a utility pocket on the wood. Our pick from the Clamp Brand to Know, and still in stock.",
        "A driver, wood, hybrid and alignment stick set cut from a Carhartt bag, with black leather backing and a fleece lining.",
        "Cut from a Nike ACG pack, keeping the black grid ripstop, coyote webbing and buckles, the ACG triangle and the Bigfoot patch. Sold out, and the best set Clamp has made."]),
 dict(k="ald", award="Best Fashion Crossover", name="Aim&eacute; Leon Dore",
  link=("/drops/aim-leon-dore-ss26-golf-croc-embossed-footjoys-and-a-sweater", "ALD&rsquo;s SS26 golf capsule"),
  body=["Aim&eacute; Leon Dore is a fashion brand first, and that is why it is here. Teddy Santis&rsquo;s Queens label has made a golf capsule every spring since 2024, the latest with FootJoy, and it treats the course as one more setting for the same clubhouse-prep wardrobe it sells all year.",
        "The SS26 golf capsule has sold through and the ALD Golf page is down, so the six below come from ALD&rsquo;s main fall line. They are the pieces that cross over: a Fair Isle knit polo from the North Face collab, a crested rugby, a fleece-lined windbreaker and caps."],
  pq=("deep admiration for the game and its distinctive style", "Aim&eacute; Leon Dore on its first golf capsule, as quoted by Golf Digest, May 2024"),
  band=["ALD Golf SS26", "Pleats and a polo", "The clubhouse look"],
  copy=["A merino Fair Isle polo from the ALD and The North Face collaboration. The best golf sweater ALD has made that isn&rsquo;t called a golf sweater.",
        "A heavy 360gsm cotton rugby in red with an embroidered crest and a cream collar. Clubhouse prep at its most ALD.",
        "A water-repellent nylon windbreaker lined in fleece, with a two-way zip. Made for October rounds.",
        "A cashmere quarter zip lined in cotton. The most expensive piece on the page, and it looks it.",
        "A blue five-panel snapback with ALD&rsquo;s crest printed on the front.",
        "An unstructured cap in striped denim with a leather and brass strap."]),
 dict(k="hls", award="Best Cult Pick", name="Hidden Links Society",
  link=("/drops/brand-to-know-hidden-links-society", "Read the Hidden Links Society profile"),
  body=["Hidden Links Society sells about thirty products and is documenting a hundred golf courses, and the people who know it really know it. The Public 100 Project has them playing and shooting every course on Golf Digest&rsquo;s Top 100 Public list, one at a time.",
        "The clothes are quiet and well made: a heavyweight overshirt that took more than a year, a &ldquo;Play Faster&rdquo; tee and cap, and a brass pitch-mark tool stamped &ldquo;Fix your damn pitch marks&rdquo;. The clothing tops out at $78."],
  pq=("no memberships, no private gates, no invitations required.", "Hidden Links Society, on The Public 100 Project"),
  band=["The follow-through", "Out of the bunker", "The Play Faster cap"],
  copy=["A charcoal polo sweatshirt that HLS spent more than a year on, understated enough for the clubhouse.",
        "A garment-washed cotton tee with &ldquo;Play Faster.&rdquo; on the back, made to order. A PSA for your group.",
        "A five-panel flat-peak cap with the same message, in walnut.",
        "A perforated bucket hat with the Bud chenille patch, the brand&rsquo;s favourite logo.",
        "A plain garment-washed tee with a small woven badge, for the range or nowhere near a course.",
        "A single-prong pitch-mark tool in aged brass, stamped and heavy. Fix your damn pitch marks."]),
]
for b in BRANDS:
    b["rows"] = PK[b["k"]]
    assert len(b["rows"]) == 6 == len(b["copy"]), b["k"]


def price(k, raw):
    x = float(raw)
    if k == "clamp":
        return gbp(x)
    if k == "midiron":
        return aud(x)
    return f"${x:,.0f}" if x.is_integer() else f"${x:,.2f}"


def nice(t):
    t = re.sub(r"\s+", " ", t).strip()
    return t.title() if t.isupper() else t


def frames(k, i):
    n = 0
    while (ROOT / f"images/streetwear-oct/{k}-{i}-{n}.jpg").is_file():
        n += 1
    return [f"{IMG}/{k}-{i}-{j}.jpg" for j in range(n)]


def card(b, i, idx):
    r = b["rows"][i]
    fr = frames(b["k"], i)
    name = H.escape(nice(r["t"]))
    label = H.unescape(f'{b["name"]} {nice(r["t"])}').replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>'
                   for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>'
                   for j in range(len(fr)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{b["name"]}</div>'
            f'<div class="product-name">{name} &middot; {("Sold out &middot; was " if r.get("sold") else "") + price(b["k"], r["price"])}</div>'
            f'<div class="product-desc">{b["copy"][i]}</div>'
            f'<a href="{r["url"]}" target="_blank" rel="noopener" class="product-link">{"View" if r.get("sold") else "Shop"} &#8599;</a></div></div>')


def pq(b):
    q, who = b["pq"]
    return (f'\n<div class="pull-quote" style="margin:8px auto 24px">\n  <div class="pull-quote-inner">'
            f'&ldquo;{q}&rdquo;<span class="pull-quote-attr">&mdash; {who}</span></div>\n</div>\n')


def band(b):
    figs = "\n".join(f'  <figure><img src="{IMG}/band-{b["k"]}-{n}.jpg" alt="{H.unescape(b["name"])}: {H.unescape(c)}" loading="lazy" />'
                     f'<figcaption class="ig-cap">{c}</figcaption></figure>' for n, c in enumerate(b["band"]))
    return f'  <div class="ig-grid" style="margin:8px 0 28px">\n{figs}\n  </div>\n'


def section(b, rank, n0):
    MT = ' style="margin-top:14px"'
    paras = "\n".join(f'    <p{"" if j == 0 else MT}>{p}</p>' for j, p in enumerate(b["body"]))
    cards = "\n".join(card(b, i, n0 + i) for i in range(6))
    href, text = b["link"]
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{b["award"]}</div>\n'
            f'  <h2 class="products-hdr" id="{b["k"]}">{rank}. {b["name"]}</h2>\n'
            f'  <div style="max-width:760px;margin:0 auto 18px;font-size:16px;line-height:1.75">\n{paras}\n'
            f'    <p style="margin-top:16px;font-family:var(--mono);font-size:11px;letter-spacing:.1em;text-transform:uppercase;opacity:.6">'
            f'Checked {CHECKED} &middot; <a href="{href}">{text} &rarr;</a></p>\n  </div>\n'
            f'{pq(b)}{band(b)}'
            f'    <div class="products-grid">\n{cards}\n    </div>\n</section>\n'), n0 + 6


TAKE = f"""
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Golf streetwear stopped being one look a while ago. It now covers a Los Angeles label with 600 pieces in stock, a headcover workshop in Yorkshire, a Queens fashion house, a Brooklyn muni brand and an Australian label that only shoots at night. So instead of ranking nine brands against each other on one scale, we gave each one the award it wins outright.</p>
    <p>Students is the best overall: the deepest range, cut by people who made streetwear before they made golf clothes. Metalwood owns retro, Malbon built the room everyone else is standing in, and Eastside has the clearest reason to exist. Public Drip is the one to watch, Midiron has the strongest look, Clamp is the find, ALD is the crossover and Hidden Links Society is the cult pick.</p>
    <h2 class="products-hdr btk-story-hdr">How We Picked</h2>
    <p>Every brand had to design like a clothing label rather than a golf company, sell things you would wear off the course, and be trading, with product in stock, on the day we checked. 52 of the 54 pieces below were in stock on their brand&rsquo;s own store on {CHECKED}, at the price shown, in the brand&rsquo;s own currency; the other two are sold-out Clamp collabs, marked as such.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Nine</div>
""" + "\n".join(f'      <div class="sidebar-detail"><span class="l">{b["award"].replace("Best ", "")}</span><span><a href="#{b["k"]}">{b["name"]}</a></span></div>' for b in BRANDS) + f"""
      <div class="sidebar-detail"><span class="l">Checked</span><span>{CHECKED}</span></div>
      <a href="/brands" class="sidebar-cta">The full Brand Index &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#GolfStreetwear</span>
        <span class="hashtag">#GolfStyle</span>
        <span class="hashtag">#GolfCulture</span>
        <span class="hashtag">#DropsAndBrands</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

FAQ = [
    ("What is the best golf streetwear brand in 2026?",
     "Students Golf. Its founder Michael Huynh came from streetwear, its range is the deepest in the category with more than 600 pieces in stock, and it is stocked by Bodega, HBX and Culture Kings."),
    ("What counts as golf streetwear?",
     "For this list, a brand has to design like a clothing label rather than a golf company, make clothes you would wear off the course, and be trading with product in stock. That admits a headcover workshop like Clamp and a fashion house like Aimé Leon Dore alongside Metalwood and Malbon."),
    ("Is Malbon still independent?",
     "Malbon raised a $33 million round led by Anthos Capital, and Aaron Heiser, formerly of Nike, is chief executive. Stephen and Erica Malbon remain as creative leads."),
    ("Does Aimé Leon Dore still make golf clothes?",
     "ALD has released a golf capsule every spring since 2024, most recently with FootJoy. As of 1 October 2026 that capsule has sold through and the ALD Golf page is offline, so the pieces in this guide come from its main fall line."),
    ("How often is this list updated?",
     "Every piece was checked on 1 October 2026, and all but two sold-out Clamp collabs were in stock. We re-check the list each season and replace anything that sells out or any brand that stops trading."),
]


def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>'
                     for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items = [{"@type": "ListItem", "position": i + 1, "name": H.unescape(b["name"]), "url": f"{URL}#{b['k']}"}
             for i, b in enumerate(BRANDS)]
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": H.unescape(DESC),
         "url": URL, "image": og, "datePublished": "2026-08-30", "dateModified": "2026-10-01",
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
            {"@type": "ListItem", "position": 3, "name": "Best Golf Streetwear Brands", "item": URL}]},
    ]
    t, d = H.escape(TITLE, quote=True), DESC.replace('"', "&quot;")
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


def main(apply_):
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Best Golf Streetwear Brands</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>9 brands &middot; 9 awards</span><span class="dot"></span>
    <span>54 pieces &middot; checked {CHECKED}</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Golf streetwear in 2026: a Students Golf Art Dept. look, a Metalwood player kicking a ball in the adidas golf shoe, and a Public Drip cap" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for rank, b in enumerate(BRANDS, 1):
        o, n = section(b, rank, n); body += o
    body += faq_html()
    out = head_top() + head_rest + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    bad = []
    for leak in ("Manors Revisited", "Nicklaus", "Enron"):
        if leak in above: bad.append("leak " + leak)
    if fin.count('class="product-card"') != 54: bad.append("card count")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", above), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
