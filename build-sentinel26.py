#!/usr/bin/env python3
"""
build-sentinel26.py — rebuild the Sentinel Golf Brand to Know page on the
Kingfisher structure.

Lenny, 2026-08-30: "this is the best example of a brand to know page -
/drops/brand-to-know-kingfisher-golf. I want the sentinel golf brand to know
page look the same or similar."

WHAT WAS STRUCTURALLY MISSING (audited, not assumed)
----------------------------------------------------
                     Kingfisher   Sentinel (before)
    product cards        20            27
    swipeable galleries  23             0     <- every card was a single flat image
    pg-frames            70             0
    founder section     "In Her Words - Fiona"  none
    lookbook            "The Lookbook" 3-up    none
    FAQ markup          .faq/.faq-q    hand-rolled inline <div style=...>

So the gap was not copy, it was four things: galleries, a founder voice, a
lookbook, and the house FAQ block.

WHAT IS PRESERVED FROM THE OLD PAGE
-----------------------------------
The whole <head> (title, canonical, og/twitter, Article + FAQPage JSON-LD),
the nav, breadcrumb, hero, the "In the Wild - Basecamp Expedition One" strip
and the "From Instagram" grid, and the More-from-Feed section. Those were
correct; rebuilding them would have risked the template-leak class of bug.

WHAT IS DELETED
---------------
A `section.products` headed "In the Wild - Tagged on Instagram" whose body was
in fact a `.more-grid` of three TGI posts (Mogshade, Austin BBQ, Hot Weather).
The heading promised reader photos and delivered a second More-from-Feed. It
also carried more-card-tag "Brand to Know", which is not one of the three
allowed labels.

THE FOUNDER PHOTO - a deliberate substitution, flagged
------------------------------------------------------
Kingfisher's founder section is built around a 340px portrait of Fiona. There
is NO clean portrait of John Mooty in existence: the only publishable frame is
a YouTube thumbnail with "JOHN MOOTY" and two logos burned across it. Running a
photo of an unnamed man beside "In His Words - John Mooty" would read as a
portrait of him, which would be false. So the image slot holds an Expedition
One camp frame instead, and the alt text says what it actually is. The layout
is byte-identical to Kingfisher's.

  (First pass used look-4, the Polaroid wall - which is ALSO the first frame of
  the "In the Wild" strip further down, so the same photograph ran twice on one
  page. Check for that when picking any image here.)

QUOTES
------
All six are verbatim from ONE source: The Old Ghosts, "Sentinel: Beyond the
Green," by Michael Williams, 9 Dec 2025. That is the only real John Mooty
interview that exists. The much-circulated line "great products tell stories
you want to be a part of" is a Skratch WRITER'S paraphrase, prefaced "As John
puts it," and is NOT in quotation marks in the original - it is not used here.

Section sizes are 5 / 6 / 3 / 8. The grid is 3-wide, so a section of 4 strands
a single orphan card on its own row.
"""
import os, re, json, html, hashlib, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(ROOT, "drops", "brand-to-know-sentinel-golf.html")
IMG = "/images/sentinel-golf"

SK = {p["title"]: p for p in json.load(
    open(os.path.join(ROOT, "research", "sentinel26-skus.json")))}


def money(v):
    return "$" + f"{float(v):,.0f}"


# ---------------------------------------------------------------- copy
# (title, blurb). Every factual claim traces to the Squarespace product
# description captured 30 Aug 2026; nothing here is invented.
DESC = {
"Basecamp Walker - Black Dyneema":
 "The MacKenzie Walker &mdash; the carry bag that arrived fully formed in the 1990s and has only "
 "been refined since &mdash; rebuilt in black Dyneema composite. Matte, papery, leather-free, and "
 "roughly the strongest fiber per gram anyone weaves. Made to order, six to eight weeks.",
"Sørensen Walker - Dark Nubuck":
 "The same Walker pattern in S&oslash;rensen nubuck, the Danish tannery Arne S&oslash;rensen founded in 1973. "
 "It is the top of the Sentinel range and the best-photographed object on the site. Eight weeks, "
 "all sales final, no customization.",
"1733 Duffle - Saltex Coyote":
 "Built with Chicago&rsquo;s 1733 in triple-layer construction: Saltex nylon shell, cotton batting, "
 "400D packcloth lining, two-way YKK Aquaguard zip, hand-tied 275 paracord pulls. The Saltex is "
 "woven in Japan and heat-treated after a salt bath, so it moves with humidity.",
"1733 Tote - Saltex Navy":
 "The zip briefcase from the same 1733 project, in navy. Boxy, hardware-forward, and rigid enough "
 "to stand on its own in a locker room. The most quietly useful thing Sentinel makes.",
"SCOUT - GOLDENROD RX30":
 "The rangefinder case Sentinel launched on, down to its last colorway. X-Pac RX30 face, 1.5mm "
 "neoprene lining, waterproof end to end, quick-draw, made in the USA. Goldenrod is the only one "
 "of six that survived.",
"Jimmy Bar":
 "Machined with Brooklyn&rsquo;s Jimmytronics from a solid block of Grade 5 titanium: divot tool, "
 "low-profile bottle opener, and a removable T6 pocket clip. Ninety-two millimeters, 25 grams. "
 "Clip it, stash it, or run it on a key ring.",
"Kvadrat Headcovers - Clay Brown":
 "Cut and sewn in New York from Kvadrat&rsquo;s 3D-knit Triangles, a wool/poly/nylon furniture "
 "textile knitted in Denmark. Melton wool lining, bar-tacked nylon webbing. Nothing else in golf "
 "has this texture, and every other Sentinel cover is gone.",
"Anderson's Belt - Navy Woven":
 "Anderson&rsquo;s has made belts in Parma and nowhere else for fifty years. This one runs a 3cm "
 "woven elastic body with charcoal suede detailing and a matte brass roller buckle. Sold here "
 "and only here.",
"Cotton/Hemp Field Sock":
 "Knitted by Japan&rsquo;s KNITWIN Co., founded 1950 on a single hand-operated machine and now "
 "running 130. Fifty-fifty cotton-hemp yarn over a cushion pile bottom. One size, fits 9 to 13, "
 "and it is the deepest stock in the shop.",
"Minami Pullover Hood - Off Black":
 "Minami Co. has been weaving in Japan since 1935 and controls every step from yarn to finish. "
 "The pullover hood is the plainest thing Sentinel sells and the one most likely to leave the "
 "house on a Tuesday. Size down if you are between.",
"Dyneema Suit - Navy":
 "A four-way stretch Dyneema ripstop jacket and trouser &mdash; water-repellent, windproof, "
 "breathable. Hidden waist and pocket zips, shock cord at waist and ankle, heavy-duty two-way "
 "YKK. Cut and sewn in the USA.",
"Basecamp Chair - White Dyneema":
 "Wildingout Products of Japan builds the Chair1987 in chestnut, which is light and shrugs off "
 "water; Sentinel re-skins it in white Dyneema. It packs down flat and looks equally correct in a "
 "living room. Made to order, eight to twelve weeks.",
"Basecamp Robotech Dome":
 "The Free Spirits Tents of Qingdao named their company after a 2009 first ascent of Yaomei Peak "
 "and build for equilibrium rather than for the record book. Eight to ten people, made to order, "
 "and the single most improbable object in golf retail.",
"Felt Target Mat":
 "American wool felt, laser-engraved with alignment markers, with a removable 4-inch donut and "
 "2-inch dot so you can take the hole away entirely. You alternate sides with a single ball "
 "rather than grooving one stroke. Part of the Sentinel Test Lab.",
"Cerakote Rypstick":
 "Dr. Luke Benoit built the Rypstick on overspeed logic borrowed from track: train the extremes "
 "and the middle follows. Sentinel&rsquo;s edition wore a Cerakote ceramic finish. Gone, and it "
 "was gone fast.",
"T.P.S. - SLATE GRAY":
 "The Trestle Pole System takes tent-pole engineering to the practice ground &mdash; anodized "
 "aluminum sections from DAC in South Korea, assembled by DAC&rsquo;s only US-certified supplier, "
 "packed in a Dyneema stake bag. Assembles one-handed.",
"Majo Lockwood Umbrella":
 "Lockwood have been handmaking umbrellas by centuries-old method for generations. Grade-A steel "
 "frame, lathe-turned brass fittings, torched oak handle, MajoTech ripstop woven in Italy. Four "
 "hundred grams, and a combination that existed only here.",
"Basecamp Travel Sleeve - Black ULTRA":
 "A roll-top travel bag borrowed from surf, built in Challenge ULTRA &mdash; a UHMWPE face over "
 "recycled polyester CrossPly at 7.4 oz per square yard, fully waterproof. Fidlock magnetic "
 "closure, YKK waterproof zips.",
"Flyweight 1/4 Zip - Charcoal":
 "Cordura air-jet nylon woven in Italy, cut and sewn in New York, with a Riri waterproof zip and "
 "a coreless paracord label loop. Tailored without being slim. Both colorways sold through and "
 "only the vest remains.",
"DeltaPeak Freemo Crew - Navy":
 "Teijin Frontier knits DELTAPEAK in Japan &mdash; a dense flat face that reads as volume, with UV "
 "protection and real breathability. Cover-stitched seams, cut and sewn in New York. The best "
 "argument Sentinel has made for a plain crewneck.",
"Colfax Q.D. Bag Strap 3.0":
 "Five-eighths-inch mil-spec tubular webbing and Colfax&rsquo;s anti-binding quick-disconnect "
 "swivels, so a camera or rangefinder comes off the bag with one thumb. Designed and made in the "
 "USA, static length, exclusive to Sentinel.",
"Cerakote Shag Tube":
 "Madewell Products invented the BagShag; this is theirs with a Sentinel finish. Aluminum body, "
 "stainless clips, 23 balls, removable rubber stop at the top. Cerakote is a ceramic coating "
 "developed for aerospace and small arms.",
}

SECTIONS = [
 ("the-carry", "New from the Collection &mdash; The Carry",
  "<strong>Bags first.</strong> Sentinel started by rebuilding somebody else&rsquo;s masterpiece in "
  "materials nobody had brought to golf, and the carry line is still where the brand argues hardest.",
  ["Basecamp Walker - Black Dyneema", "Sørensen Walker - Dark Nubuck",
   "1733 Duffle - Saltex Coyote", "1733 Tote - Saltex Navy", "SCOUT - GOLDENROD RX30"]),
 ("objects-layers", "New from the Collection &mdash; Objects and Layers",
  "<strong>The accessible half.</strong> Six pieces run from a $30 sock to a $540 rain suit, and every "
  "one names the mill or the machine shop that made it. That sourcing is the whole product, really.",
  ["Jimmy Bar", "Kvadrat Headcovers - Clay Brown", "Anderson's Belt - Navy Woven",
   "Cotton/Hemp Field Sock", "Minami Pullover Hood - Off Black", "Dyneema Suit - Navy"]),
 ("test-lab", "New from the Collection &mdash; The Test Lab",
  "<strong>The experiments.</strong> A Japanese camp chair, a Chinese expedition dome, and a wool felt "
  "putting panel with the hole removed. None of these sell in volume. That is not what they are for.",
  ["Basecamp Chair - White Dyneema", "Basecamp Robotech Dome", "Felt Target Mat"]),
]

GRAIL = ["Cerakote Rypstick", "T.P.S. - SLATE GRAY", "Majo Lockwood Umbrella",
         "Basecamp Travel Sleeve - Black ULTRA", "Flyweight 1/4 Zip - Charcoal",
         "DeltaPeak Freemo Crew - Navy", "Colfax Q.D. Bag Strap 3.0", "Cerakote Shag Tube"]

LOOK = [("look-1", "Four walkers on the boardwalk at Sand Valley, autumn treeline behind"),
        ("look-2", "A wedge shot spraying sand, Sand Valley fairway beyond"),
        ("look-3", "Sitting out a fire on the water at dusk in a Sentinel shell"),
        ("look-5", "Morning inside the Basecamp dome, two cots and a wool blanket"),
        ("look-6", "Two Basecamp domes mirrored in a pond under autumn colour"),
        ("founder-slot", "A par three across the water at Sand Valley, one walker on the green")]


def gallery(key, name, n):
    frames = "".join(
        f'<div class="pg-frame"><img src="{IMG}/{key}-{i}.jpg" alt="{name} &middot; view {i+1} of {n}" '
        f'loading="lazy" /></div>' for i in range(n))
    dots = "".join(f'<button class="pg-dot{" on" if i == 0 else ""}" data-i="{i}" '
                   f'aria-label="View image {i+1}"></button>' for i in range(n))
    return (f'<div class="product-gallery"><div class="pg-track">{frames}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>')


def card(title, sold=False):
    p = SK[title]
    n = p["frames"]
    nm = (title.replace("- ", "&mdash; ").replace("ø", "&oslash;")
               .replace("'", "&rsquo;"))
    tag = "Sentinel Golf &middot; " + ("Sold Out" if sold else "New")
    link = ('<span class="product-link">Sold Out</span>' if sold else
            f'<a href="{p["url"]}" target="_blank" rel="noopener" class="product-link">Shop &nearr;</a>')
    return f'''<div class="product-card" data-frames="{n}">
      {gallery(p["key"], "Sentinel Golf " + nm, n)}
      <div class="product-body">
        <div class="product-brand">{tag}</div>
        <div class="product-name">{nm} &middot; {money(p["price"])}</div>
        <div class="product-desc">{DESC[title]}</div>
        {link}
      </div>
    </div>'''


def grid(titles, sold=False):
    return ('  <div class="products-grid">\n\n    '
            + "\n\n    ".join(card(t, sold) for t in titles) + "\n\n  </div>")


# ---------------------------------------------------------------- assemble
def main(apply_=False):
    s = open(PAGE, encoding="utf-8").read()
    before = len(s)
    open("/tmp/sentinel-before.html", "w").write(s)

    # --- prefix: head, nav, breadcrumb, header, hero (unchanged but for the count)
    cut = s.find('<div class="writeup">')
    head = s[:cut].replace("<span>12 Pieces</span>", "<span>22 Pieces</span>")

    # --- the two Instagram blocks and the More section, lifted verbatim
    def section_at(needle):
        # ASSERT. First cut passed "In the Wild &mdash; Basecamp Expedition One",
        # but the old page renders that heading with a LITERAL em dash. find()
        # returned -1, rfind("<section", 0, -1) walked to the last section in the
        # file, and the Expedition One strip was silently replaced by the bogus
        # "In the Wild - Tagged on Instagram" more-grid — which then rendered as a
        # SECOND "More from the Feed" halfway up the page.
        j = s.find(needle)
        if j < 0:
            raise SystemExit(f"section_at: {needle!r} not found in the source page")
        i = s.rfind("<section", 0, j)
        return s[i:s.find("</section>", i) + 10]

    wild = section_at("In the Wild — Basecamp Expedition One")
    igrid = section_at("From Instagram &mdash; @sentinelgolf.us")
    more = s[s.rfind('<section class="more">'):]

    # --- house FAQ, rebuilt from this page's own (correct) FAQPage schema
    faq_ld = [m.group(1) for m in re.finditer(
        r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
        if '"FAQPage"' in m.group(1)][0]
    qs = [(q["name"], q["acceptedAnswer"]["text"])
          for q in json.loads(faq_ld)["mainEntity"]]
    faq = ('<div class="faq">\n' + "\n".join(
        f'    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>'
        for q, a in qs) + "\n  </div>")

    # --- writeup: what it is -> the inspiration -> who it is for
    writeup = '''<div class="writeup">
  <div class="writeup-body">
    <p>Sentinel Golf is a product design lab in Minneapolis that makes golf equipment the way an outdoor brand makes a tent. Founder John Mooty runs it on a limited pre-order model &mdash; a window opens, you buy or you miss it, and there are no restocks and no discounts &mdash; and spends the rest of his time convincing manufacturers outside the game to take a job in it. A Danish tannery. A Nashville chair company. A Brooklyn machine shop. Tent-pole engineers in South Korea. The catalog reads like a list of favors called in.</p>
    <p>The reference point is not golf at all; it is the Boundary Waters, the million-acre stretch of protected Minnesota wilderness where you camp, canoe and fish all day with no cell service and can drink the water under your canoe. Mooty built the Basecamp series to hold that feeling inside a golf trip, and the second Basecamp capsule was shot at Sand Valley across three days of camping, fishing and golf on one itinerary. It is why the writer Michael Williams called Sentinel an American Snow Peak, but for golf.</p>
    <p>Which makes it a brand for a fairly specific reader: the walker who cares where the fabric was woven, who would rather own four objects for a decade than forty for a season, and who is not put off by an eight-week wait or a bag that costs more than a driver. Prices run from a $30 sock to a $2,900 dome tent. The sold-out archive is longer than the live shop, and that is the point &mdash; 112 of the 196 things Sentinel has made are already gone.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Founder</span><span>John Mooty</span></div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Minneapolis, MN</span></div>
      <div class="sidebar-detail"><span class="l">Walkers</span><span>$810&ndash;$1,750</span></div>
      <div class="sidebar-detail"><span class="l">Apparel</span><span>$30&ndash;$540</span></div>
      <div class="sidebar-detail"><span class="l">Camp</span><span>$148&ndash;$3,900</span></div>
      <div class="sidebar-detail"><span class="l">Model</span><span>Limited Pre-Order</span></div>
      <a href="https://www.sentinelgolf.us/shop" target="_blank" rel="noopener" class="sidebar-cta">Shop Sentinel Golf &nearr;</a>
      <div class="hashtags">
        <span class="hashtag">#TheGrassyIssue</span>
        <span class="hashtag">#GolfCulture</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#SentinelGolf</span>
        <span class="hashtag">#IndieGolf</span>
        <span class="hashtag">#MightAsWellMakeIt</span>
      </div>
    </div>
  </aside>
</div>
'''

    # --- product sections
    prods = ""
    for i, (sid, hdr, kick, titles) in enumerate(SECTIONS):
        pull = ('''
<div class="pull-quote">
  <div class="pull-quote-inner">&ldquo;Since it started, the project has always been about bringing new ideas, materials, and people into the golf space, not only to make it more interesting but to make it more fun.&rdquo;<span class="pull-quote-attr">&mdash; John Mooty, Sentinel Golf founder</span></div>
</div>
''' if i == 0 else "")
        prods += f'''
<section class="products"{' style="border-top:none;padding-top:48px"' if i else ''}>{pull}
  <h2 class="products-hdr" id="{sid}">{hdr}</h2>
  <p class="cat-kicker">{kick}</p>
{grid(titles)}
</section>
'''

    # --- founder. Same two-column layout as Kingfisher; see module docstring
    #     for why the image slot is not a portrait.
    founder = '''
<section class="products" style="border-top:none;padding-top:48px">
  <h2 class="products-hdr" id="in-his-words">In His Words &mdash; John Mooty on Building Sentinel</h2>
  <p class="cat-kicker"><strong>One interview exists.</strong> Every quote below is verbatim from The Old Ghosts, &ldquo;Sentinel: Beyond the Green,&rdquo; by Michael Williams, 9 December 2025.</p>
  <div class="bk-founder" style="display:grid;grid-template-columns:340px 1fr;gap:40px;align-items:start;max-width:1100px">
    <div style="border:.5px solid var(--ink);overflow:hidden">
      <img src="/images/sentinel-golf/hero-new.jpg" alt="A Basecamp dome pitched under a turning oak, Expedition One at Sand Valley" loading="lazy" style="width:100%;aspect-ratio:4/5;object-fit:cover;display:block" />
    </div>
    <div style="font-size:16px;line-height:1.7">
      <p>Mooty does not give many interviews &mdash; one, as far as the record goes &mdash; and when he does he talks about sourcing rather than about himself. Asked what the project has been about since the start, he answers in the same register the products do.</p>
      <p style="margin-top:16px">&ldquo;Since it started, the project has always been about bringing new ideas, materials, and people into the golf space, not only to make it more interesting but to make it more fun. That is still the best part for me, but in terms of evolution, the most enjoyable challenge is exploring the boundaries (or lack thereof) beyond golf and how that can be done in both product and brand the right way, balancing innovation and tradition.&rdquo;</p>
      <p style="margin-top:16px">On where Basecamp came from: &ldquo;It came from the idea of just building an itinerary that sounded like the most fun trip to leave the house for. In Minnesota, we have the largest chain of interconnected lakes and over a million acres of protected wilderness called the Boundary Waters, where you have no choice but to camp, canoe, and fish all day. You also have no cell service, no planes flying overhead, and can drink the water under your canoe so the experience with the people you are with is very special. The Basecamp series tries to embody this feeling in the form of a golf trip.&rdquo;</p>
      <p style="margin-top:16px">And on whether made-in-America is the standard: &ldquo;Definitely, but it is also not an absolute requirement. What is important to me at this point is finding the people who care the most about what they make, use the best inputs they can find, and do things the right way at all phases of the process. If that is here in the US, in Japan, Europe, or elsewhere, I am here for it.&rdquo;</p>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:28px;padding-top:24px;border-top:.5px solid rgba(20,20,20,.15)">
        <div>
          <div style="font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;opacity:.55;margin-bottom:6px">Quality</div>
          <div style="font-size:14px;line-height:1.6;opacity:.85">&ldquo;Ideally, the assortment is always rooted in quality, story, and utility.&rdquo;</div>
        </div>
        <div>
          <div style="font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;opacity:.55;margin-bottom:6px">Lanes</div>
          <div style="font-size:14px;line-height:1.6;opacity:.85">&ldquo;People may not relate to every lane but my hope is they all can be appreciated and encouraged.&rdquo;</div>
        </div>
        <div>
          <div style="font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;opacity:.55;margin-bottom:6px">He Reads</div>
          <div style="font-size:14px;line-height:1.6;opacity:.85">&ldquo;F/CE, Norda, Saunders Militaria and Foreign Rider. I really enjoy how they all approach and appreciate both product and storytelling.&rdquo;</div>
        </div>
      </div>
    </div>
  </div>
</section>
'''

    figs = "\n".join(
        f'''    <figure style="margin:0;border:.5px solid var(--ink);overflow:hidden">
      <img src="{IMG}/{k}.jpg" alt="{a}" loading="lazy" style="width:100%;aspect-ratio:4/5;object-fit:cover;display:block" />
    </figure>''' for k, a in LOOK)
    lookbook = f'''
<section class="products" style="border-top:none;padding-top:48px">
  <h2 class="products-hdr" id="lookbook">The Lookbook</h2>
  <p class="cat-kicker"><strong>Basecamp Expedition One, Sand Valley, autumn 2025.</strong> Three days of camping, fishing and golf on one itinerary &mdash; the trip the whole Basecamp line was drawn from.</p>
  <div class="bk-look" style="display:grid;grid-template-columns:repeat(3,1fr);gap:24px">
{figs}
  </div>
  <div style="font-family:var(--mono);font-size:9px;letter-spacing:.1em;text-transform:uppercase;opacity:.45;margin-top:14px">Photography courtesy of Sentinel Golf</div>
</section>
'''

    grail = f'''
<section class="products" style="border-top:none;padding-top:48px">
  <h2 class="products-hdr" id="grail-closet">The Grail Closet &mdash; Eight That Are Gone</h2>
  <p class="cat-kicker"><strong>112 of 196 products are sold out.</strong> No restocks, no discounts, no back catalog. These eight are the ones people still ask after, and the archive is a fair argument for the brand on its own.</p>
{grid(GRAIL, sold=True)}
</section>
'''

    faq_sec = f'''
<section class="products" style="border-top:none;padding-top:48px">
  <h2 class="products-hdr" id="faq">The Story &mdash; FAQ</h2>
  {faq}
</section>
'''

    out = head + writeup + prods + founder + lookbook + grail + wild + igrid + faq_sec + more

    # --- gallery CSS + JS, ported from the Kingfisher page
    kf = open(os.path.join(ROOT, "drops", "brand-to-know-kingfisher-golf.html"),
              encoding="utf-8").read()
    if ".pg-track" not in out:
        i = kf.find(".product-card{position:relative}")
        j = kf.find("</style>", i)
        css = kf[i:j]
        k = out.rfind("</style>")
        out = out[:k] + "\n/*TGI-SENTINEL-GALLERY*/\n" + css + "\n" + out[k:]
    if "pg-track" not in out.split("</style>")[-1] or "querySelectorAll('.product-gallery')" not in out:
        js = [m.group(1) for m in re.finditer(r"<script\b[^>]*>(.*?)</script>", kf, re.S)
              if "pg-track" in m.group(1)][0]
        k = out.rfind("</body>")
        out = out[:k] + f"<script>{js}</script>\n" + out[k:]
    # .faq / .faq-q / .cat-kicker CSS, likewise
    for sel in (".faq-q", ".cat-kicker"):
        if sel not in out.split("</body>")[0].split("<style")[-1] and sel + "{" not in out:
            m = re.search(re.escape(sel) + r"[^{}]*\{[^}]*\}", kf)
            if m:
                k = out.rfind("</style>")
                out = out[:k] + "\n" + m.group(0) + "\n" + out[k:]

    # .bk-founder / .bk-look exist ONLY to carry the mobile override — the grids
    # themselves are inline-styled. Kingfisher ships these as `.kf-*` inside its
    # @media block and nowhere else; without the block the founder grid keeps a
    # fixed 340px first column on a phone and the copy column collapses to ~30px.
    if ".bk-founder" not in out:
        k = out.rfind("</style>")
        out = out[:k] + (
            "\n/*TGI-BTK-LAYOUT*/\n"
            ".bk-founder,.bk-look{max-width:1100px}\n"
            "@media(max-width:820px){.bk-founder{grid-template-columns:1fr!important}"
            ".bk-look{grid-template-columns:repeat(2,1fr)!important}}\n"
            "@media(max-width:480px){.bk-look{grid-template-columns:1fr!important}}\n"
        ) + out[k:]

    ncards = out.count('<div class="product-card')
    nframes = out.count('class="pg-frame"')
    print(f"  cards {ncards}   galleries {out.count('pg-track')}   frames {nframes}")
    print(f"  bytes {before} -> {len(out)}")
    if apply_:
        open(PAGE, "w", encoding="utf-8").write(out)
        print("  written")
    else:
        print("  (dry run - pass --apply)")


if __name__ == "__main__":
    main("--apply" in sys.argv)
