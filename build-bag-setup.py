#!/usr/bin/env python3
"""build-bag-setup.py — The Bag, Curated: colour, design and six setups.
28 September 2026.

Lenny: "Let's do a post about color choices, bag design and curating the ideal
personal bag set up." Answers: guide + example kits; mix brands per kit;
"price aside, just design and curating. Let's pull cool images from pinterest
also". Then: "No on red white & blue, tacky ... I want inspiration pics then
individual pieces for sale. Replace red, white and blue with navy blue with a
pop of color." Then "looks good, let's put it all together".

PINTEREST: used for ideas only (palette cards, flat lays, leather, check). The
pins were reposts or AI images with no traceable owner, so none are used.
Every photo here is the maker's own, from its store: kit bands from
research/bag-setup/bands.json, card frames from research/bag-setup/frames.json.

PRICES: each maker's own store, read 28 Sep 2026, in the store's currency.
Hiroki is a New Zealand store (NZD); everything else is USD.
Then "add them if possible. Lean a little more on the inspo pics, I want a vibey
post that is shareable": a six-photo mood board after the Take, and each setup
now leads with two large photographs. Lenny's four pins: Gumtree and Sugarloaf
were traced to their own stores (same shoots); the burgundy bag and the argyle
flat lay had no traceable source and are not used.
No feed card; that waits for Lenny.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "curating-your-golf-bag-setup"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/bag-setup"
FR = json.loads((ROOT / "research/bag-setup/frames.json").read_text())
BANDS = json.loads((ROOT / "research/bag-setup/bands2.json").read_text())

TITLE = "Golf Bag Setup Ideas: How to Match Your Bag, Headcovers and Colors"
DESC = ("Golf bag setup ideas: how to match your bag, headcovers, towel and accessories by color, with four simple rules "
        "and six complete setups from independent makers.")
H1 = "Golf Bag Setup Ideas: How to Match Your Bag, Headcovers and Colors"

BRAND = {"hirokigolf.com": "Hiroki", "apresgolf.com": "Apr&egrave;s-Golf", "dormieworkshop.com": "Dormie Workshop",
         "dimpledivot.com": "Dimple &amp; Divot", "seamusgolf.com": "Seamus Golf", "bluetross.com": "Bluetross",
         "jonessportsco.com": "Jones Sports Co.", "malbon.com": "Malbon Golf", "ghostgolf.com": "Ghost Golf",
         "gumtreegolfandnature.com": "Gumtree Golf &amp; Nature Club", "sugarloafsocialclub.com": "Sugarloaf Social Club",
         "birdsofcondor.com": "Birds of Condor", "radmorgolf.com": "Radmor Golf", "pinterest": "Via Pinterest"}
CUR = {"hirokigolf.com": "NZ$"}

# handle -> (dom, name, price, role, copy)
P = {
 # Clubhouse Green
 "hiroki-fte-sunday-golf-bag-green": ("hirokigolf.com", "FTE Sunday Bag, Forest Green", "369", "The bag",
   "This is a waterproof Sunday bag in a deep forest green, made from Hiroki&rsquo;s PTFE fabric with YKK zips. The green is dark enough to read as a neutral, which is why everything else in the kit can be cream."),
 "og-cream-dream-sherpa-fleece-headcover-w-green-trim": ("apresgolf.com", "OG Cream Dream Sherpa Headcover, Green Trim", "78", "The driver",
   "It is a cream sherpa cover, hand-sewn in California, with a thin green trim at the hem that ties it back to the bag. Cream is the 30 in this kit."),
 "dormie-chevron-green-room-xl-blade-putter-cover-copy": ("dormieworkshop.com", "Chevron Green Room XL Blade Cover", "150", "The putter",
   "This is milled full-grain leather in what Dormie calls Green Room Green, after old clubhouses. It picks up the bag&rsquo;s green in a different texture."),
 "dormie-signature-players-towel-green": ("dormieworkshop.com", "Signature Player&rsquo;s Towel, Green", "30", "The towel",
   "It is a 22 by 44 inch terry towel in a lighter green with a cream stripe, which keeps the kit from going flat."),
 "hickory-golf-brush-pro-hybrid-green": ("dimpledivot.com", "Hickory Golf Brush PRO+, Green", "65", "The brush",
   "The hickory handle and nickel snap are the brass in this palette. It carries both nylon and metal bristles on a retractable tether."),
 # Tweed & Tan
 "macleod-tartan-sunday-bag": ("seamusgolf.com", "Fescue Project Sunday Bag, MacLeod Check Harris Tweed", "995", "The bag",
   "This is Seamus&rsquo;s single-strap Sunday bag in MacLeod check Harris Tweed with tan leather trim. It is the most expensive thing on the page, and the one that sets the whole palette."),
 "the-old-tom-castagna-brown-leather-driver-headcover": ("bluetross.com", "The Old Tom Driver Headcover, Castagna Brown", "225", "The driver",
   "It is full-grain Italian leather in a chocolate brown, with a debossed number one. Brown leather against tweed is the pairing this kit is built on."),
 "macleod-tweed-blade-putter-cover": ("seamusgolf.com", "MacLeod Check Harris Tweed Blade Cover", "130", "The putter",
   "This is the same hand-woven tweed from the Outer Hebrides as the bag, with a brown fleece lining and a magnetic closure. Matching the putter cover to the bag is the one exact match here."),
 "british-tan-aniline-leather-iron-cover": ("seamusgolf.com", "British Tan Aniline Leather Iron Cover", "180", "The irons",
   "It is tan aniline leather lined with shearling, made in Oregon, meant to stop irons chattering in transit. It will darken with use, which is the point."),
 "pendleton-canyonlands-golf-towel": ("seamusgolf.com", "Canyonlands Golf Towel", "45", "The towel",
   "This is a cotton Pendleton towel in red, orange, tan and blue. It is the one pattern that isn&rsquo;t tweed, and its colours already sit inside the MacLeod check."),
 "hickory-golf-brush-highland": ("dimpledivot.com", "Hickory Golf Brush, Highland", "50", "The brush",
   "This is the Classic brush on a green, orange and cream tether, which matches the stripes in the tweed."),
 # Navy, With a Pop
 "hiroki-fte-sunday-golf-bag-navy": ("hirokigolf.com", "FTE Sunday Bag, Navy", "369", "The bag",
   "This is the same waterproof Sunday bag in navy. It is the 60 in this kit and it does not compete with anything."),
 "pink-sherpa-fleece-headcover-w-navy-trim": ("apresgolf.com", "Pink Sherpa Headcover, Navy Trim", "68", "The pop",
   "This is the one piece of colour: a soft pink sherpa cover with a navy trim that ties it to the bag. If pink isn&rsquo;t for you, Apr&egrave;s makes the same idea in yellow."),
 "paisley-towel-navy": ("dormieworkshop.com", "Paisley Towel, Navy", "30", "The towel",
   "It is navy terry with a white paisley print. The pattern is small enough to read as texture from a few feet away."),
 "hickory-golf-brush-pro-hybrid-blue": ("dimpledivot.com", "Hickory Golf Brush PRO+, Blue", "65", "The brush",
   "It has a blue and white tether on hickory, which keeps the accent count at one."),
 # Stone & Bone
 "rover-stand-bag-bone": ("jonessportsco.com", "Rover Stand Bag, Bone", "295", "The bag",
   "This is a bone stand bag with a dual strap and full-length dividers. It is the lightest base on the page and it goes with any shirt."),
 "big-retro-logo-cream-sherpa-fleece-headcover": ("apresgolf.com", "BIG RETRO Logo Cream Sherpa Headcover", "118", "The driver",
   "It is cream sherpa with a big retro wordmark. The soft pile against the bag&rsquo;s smooth finish is the texture contrast this kit relies on."),
 "white-french-seam-xl-blade-cover": ("dormieworkshop.com", "White French Seam XL Blade Cover", "150", "The putter",
   "This is white Italian leather joined with French seams. It sits one shade lighter than the bag."),
 "ironworks-caddy-towel-ivory": ("malbon.com", "Ironworks Caddy Towel, Ivory", "58", "The towel",
   "It is an ivory velour caddy towel, about two feet by four, with a centre slit and faded blue lettering."),
 "rangefinder-pouch-ecru-kodiak": ("jonessportsco.com", "Rangefinder Pouch, Ecru/Kodiak", "45", "The pouch",
   "This is the one soft brown in the kit, an ecru pouch with a kodiak trim that clips on with a YKK carabiner."),
 # Black & White
 "members-walking-bag-black": ("malbon.com", "Members Walking Bag", "368", "The bag",
   "This is a black rip-stop walking bag under six pounds, with a pattern panel down one side. That panel is the only pattern in the kit."),
 "checkered-headcover-black": ("ghostgolf.com", "Checkered Headcover, Black", "100", "The driver",
   "The checks are embossed black on black, so they add texture without adding a second pattern."),
 "black-white-mallet-cover": ("dormieworkshop.com", "Black &amp; White Mallet Cover", "150", "The putter",
   "It is Italian leather with a white top and black base. It is the cleanest piece here."),
 "hiroki-golf-towel-black": ("hirokigolf.com", "Golf Towel, Black", "45", "The towel",
   "This is a large microfibre waffle towel, 56 by 100 cm, in black with a white graphic."),
 "hickory-golf-brush-pro-hybrid-black": ("dimpledivot.com", "Hickory Golf Brush PRO+, Black", "65", "The brush",
   "The black and white tether matches everything, and the hickory is the only warm note."),
 # One Loud Note
 "hiroki-fte-sunday-golf-bag": ("hirokigolf.com", "FTE Sunday Bag, Stone Grey", "369", "The bag",
   "This is the FTE Sunday bag in a pale stone grey. A quiet base is what makes the loud piece work."),
 "hiroki-nylon-headcover-orange": ("hirokigolf.com", "Nylon Headcover, Bright Orange", "69", "The loud one",
   "It is a barrel cover in ballistic nylon with a fleece lining, in an orange you can find from across the range. This is the only loud piece in the kit."),
 "hiroki-golf-towel-grey": ("hirokigolf.com", "Golf Towel, Grey", "45", "The towel",
   "This is the same waffle microfibre towel in grey, which matches the bag instead of the cover."),
 "hickory-golf-brush-gravel": ("dimpledivot.com", "Hickory Golf Brush, Gravel", "50", "The brush",
   "It has a grey tether on hickory. Anything brighter would give the orange competition."),
}

PROSE = 'style="max-width:760px;font-size:16px;line-height:1.7;margin:0 auto 36px;"'

KITS = [
 ("Clubhouse Green", "clubhouse-green", ["#1f3b2c", "#f1ead8", "#b08d57"], ["Forest", "Cream", "Brass"],
  "Forest green, cream and brass are the oldest colours in golf, and the easiest to get right.",
  ["This palette works because every colour in it already exists on a golf course. Deep green reads as a neutral out there, so it never fights the grass, and cream next to it looks deliberate rather than loud. The brass comes from hickory and nickel hardware instead of a third fabric, which keeps the bag from looking matched out of a catalogue.",
   "Keep the greens in one family, deep and slightly cool, and let texture do the work: waterproof nylon on the bag, sherpa on the driver, milled leather on the putter and terry on the towel. It goes with khaki, grey, white and navy, which is most of what anyone wears to play.",
   "<strong>Our pick</strong> is the Dormie Green Room blade cover at $150. You look at your putter cover more than any other piece in the bag, and this one carries the green in leather that darkens with every round. Buy it first and the rest of the kit can follow slowly."],

  ["hiroki-fte-sunday-golf-bag-green", "og-cream-dream-sherpa-fleece-headcover-w-green-trim", "dormie-chevron-green-room-xl-blade-putter-cover-copy", "dormie-signature-players-towel-green", "hickory-golf-brush-pro-hybrid-green"]),
 ("Tweed &amp; Tan", "tweed-and-tan", ["#5a4a3a", "#8b5a2b", "#2e3b2f"], ["Tweed", "Saddle", "Moss"],
  "Harris Tweed, saddle leather and a Pendleton towel make a bag that looks better with age.",
  ["This is the setup for people who want the bag to look like it has a history. Harris Tweed, brown leather and shearling all age well, so the kit gets better as it gets scuffed. The colours are autumnal without trying: brown, moss, rust and a little blue, all taken from the MacLeod check itself.",
   "It breaks the one-pattern rule and gets away with it, because the tweed repeats. The bag and putter cover match exactly, the leathers stay in the brown family, and the Pendleton towel&rsquo;s reds and oranges are already inside the check. Where it goes wrong is adding a second loud pattern, so keep everything else plain.",
   "<strong>Our pick</strong> is the Seamus MacLeod tweed blade cover at $130. It is the same hand-woven tweed from the Outer Hebrides as the $995 bag, so you get the look of the whole setup for a fraction of the price. It also looks right on any bag, including a plain black one."],

  ["macleod-tartan-sunday-bag", "the-old-tom-castagna-brown-leather-driver-headcover", "macleod-tweed-blade-putter-cover", "british-tan-aniline-leather-iron-cover", "pendleton-canyonlands-golf-towel", "hickory-golf-brush-highland"]),
 ("Navy, With a Pop", "navy-with-a-pop", ["#1d2a44", "#e9e4d8", "#f08aa8"], ["Navy", "Oat", "Pink"],
  "Put everything in navy and add one flash of colour.",
  ["Navy is the most forgiving base there is. It works with khaki, grey and white, it hides dirt, and it makes any single bright colour look intentional instead of accidental. That is why this is the easiest setup on the page to copy.",
   "The whole idea rests on restraint. The pink cover is the only bright thing in the bag, so the towel stays navy, the brush tether stays blue and white, and the covers you already own should be dark or neutral. Swap pink for yellow if you prefer, but never use both.",
   "<strong>Our pick</strong> is the Apr&egrave;s-Golf pink sherpa cover at $68. It is the least expensive piece in the kit and the one that makes it. The navy trim ties it back to the bag, so it reads as part of the setup rather than something you found at the pro shop."],

  ["hiroki-fte-sunday-golf-bag-navy", "pink-sherpa-fleece-headcover-w-navy-trim", "paisley-towel-navy", "hickory-golf-brush-pro-hybrid-blue"]),
 ("Stone &amp; Bone", "stone-and-bone", ["#e8e1d3", "#c9bfae", "#7a6a58"], ["Bone", "Stone", "Kodiak"],
  "Tonal cream, stone and one soft brown: quiet, and it never clashes with what you wear.",
  ["A tonal bag is the quietest way to look put together. Cream, stone and bone never clash with what you wear, they photograph beautifully, and they make every club in the bag look cleaner. It is the setup for people who would rather the bag disappear than stand out.",
   "The catch is that tonal lives or dies on texture, because there is no colour to carry it. Put a smooth bag with a shaggy sherpa cover, a leather putter cover and a velour towel, each a shade apart, and it looks rich. Put four smooth things together and it looks unfinished.",
   "<strong>Our pick</strong> is the Jones rangefinder pouch in ecru and kodiak at $45. It adds the one soft brown that the kit needs, and it clips on with a carabiner, so it moves to whatever bag you carry next. It is a small piece that finishes the whole look."],

  ["rover-stand-bag-bone", "big-retro-logo-cream-sherpa-fleece-headcover", "white-french-seam-xl-blade-cover", "ironworks-caddy-towel-ivory", "rangefinder-pouch-ecru-kodiak"]),
 ("Black &amp; White", "black-and-white", ["#111111", "#f5f5f2", "#8a8a86"], ["Black", "White", "Grey"],
  "Black and white is graphic and hard to get wrong: one pattern, everything else plain.",
  ["Black and white is graphic, easy and hard to get wrong. It suits a modern stand bag, it works with almost any outfit, and it looks sharp in a locker room or on the first tee. It is also the most forgiving palette to add to over time.",
   "The discipline is keeping to one pattern. Here the bag carries it, the driver cover&rsquo;s checks are embossed black on black so they read as texture, and everything else is plain. If you add anything, add it in grey, never a third colour.",
   "<strong>Our pick</strong> is the Dormie Black &amp; White mallet cover at $150. It splits the two colours cleanly, white Italian leather on top and black below, so it ties the whole kit together in one piece. It is also the easiest cover on this page to spot on a crowded putting green."],

  ["members-walking-bag-black", "checkered-headcover-black", "black-white-mallet-cover", "hiroki-golf-towel-black", "hickory-golf-brush-pro-hybrid-black"]),
 ("One Loud Note", "one-loud-note", ["#9a9a94", "#e6e3dc", "#f26b1d"], ["Stone", "Chalk", "Orange"],
  "Pair a quiet bag with one piece that shouts. The rule is only one.",
  ["This is the easiest way to show some personality without the bag turning into a costume. The rule is only one: a quiet grey or stone base, a matching towel and brush, and a single piece that shouts. The loud piece gets more attention because nothing else competes with it.",
   "It also lets you change the whole mood of the bag for the price of one cover. A bright orange barrel cover works here, and so does a novelty or cartoon cover, as long as it is the only one. The moment you add a second loud piece, it stops looking chosen.",
   "<strong>Our pick</strong> is the Hiroki bright orange barrel cover at NZ$69. It is ballistic nylon with a fleece lining, it matches the bag&rsquo;s maker and fabric, and it is visible from across the range. It is the whole setup in one piece."],

  ["hiroki-fte-sunday-golf-bag", "hiroki-nylon-headcover-orange", "hiroki-golf-towel-grey", "hickory-golf-brush-gravel"]),
]
PICKS = {'Clubhouse Green': 'dormie-chevron-green-room-xl-blade-putter-cover-copy', 'Tweed &amp; Tan': 'macleod-tweed-blade-putter-cover', 'Navy, With a Pop': 'pink-sherpa-fleece-headcover-w-navy-trim', 'Stone &amp; Bone': 'rangefinder-pouch-ecru-kodiak', 'Black &amp; White': 'black-white-mallet-cover', 'One Loud Note': 'hiroki-nylon-headcover-orange'}
PICKSET = set(PICKS.values())
BKEY = {"clubhouse-green": "Clubhouse Green", "tweed-and-tan": "Tweed & Tan", "navy-with-a-pop": "Navy, With a Pop",
        "stone-and-bone": "Stone & Bone", "black-and-white": "Black & White", "one-loud-note": "One Loud Note"}

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>A good bag setup is not a collection of nice things. It is a palette. The golfers whose bags you notice have usually picked three colours, one pattern at most, and stuck to them from the bag down to the brush.</p>
    <p>This is a guide to doing that on purpose. It starts with four rules, then six complete setups from independent makers, each one opening with photographs of the palette in use and then the individual pieces. Mix brands freely. The palette is what holds it together.</p>
    <p>If you only change one thing, change the driver cover. It is the largest piece of colour on the bag after the bag itself.</p>
    <h2 class="products-hdr btk-story-hdr">The Four Rules</h2>
    <p><strong>Sixty, thirty, ten.</strong> Let one colour take most of the bag, a second take the covers, and a third show up only in small things: a tether, a trim, a brush. Interior designers use the same split for a room.</p>
    <p><strong>One pattern per bag.</strong> Tartan, check, paisley or camo, pick one and make everything else plain. The exception is repeating the same pattern, as the tweed kit below does.</p>
    <p><strong>Match your metals and leathers.</strong> Keep brown leather with brown, black with black, and one metal throughout. It is the detail people notice without knowing why.</p>
    <p><strong>Contrast texture, not just colour.</strong> Nylon, sherpa, leather and terry in the same colour look richer than four colours in the same material.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Setups</span><span>Six</span></div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>29, from nine makers</span></div>
      <div class="sidebar-detail"><span class="l">The rule</span><span>Three colours, one pattern</span></div>
      <div class="sidebar-detail"><span class="l">Easiest start</span><span>Navy, with a pop</span></div>
      <div class="sidebar-detail"><span class="l">Prices read</span><span>28 September 2026</span></div>
      <a href="#clubhouse-green" class="sidebar-cta">See the setups &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#BagSetup</span>
        <span class="hashtag">#WhatsInTheBag</span>
        <span class="hashtag">#Headcovers</span>
        <span class="hashtag">#GolfStyle</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

NOTE = """
<section class="products" style="margin-top:8px;">
  <h2 class="products-hdr" id="how-we-picked">How We Picked</h2>
  <div %s>
    <p style="margin:0 0 16px;">We started on Pinterest, where the best-saved golf bags share a few habits: palette cards, flat lays, tan leather, green check and houndstooth. Most of those pins were reposts with no credit, so we traced what we could back to the makers. The setup photographs come from the makers&rsquo; own stores, and Gumtree Golf &amp; Nature Club and Sugarloaf Social Club set the tone. Two mood-board images, the burgundy bag and the flat lay, were found on Pinterest without a credit; if they are yours, tell us and we will credit or remove them.</p>
    <p style="margin:0 0 16px;">Every piece was in stock when we checked. Prices come from each maker&rsquo;s own store on 28 September 2026, in its own currency. Hiroki sells from New Zealand in New Zealand dollars; everything else is in US dollars. For more on bags themselves, see <a href="/drops/upgrading-your-golf-bag">Upgrading Your Golf Bag</a>.</p>
  </div>
</section>
""" % PROSE

FAQ = [
    ("How do I choose colours for my golf bag setup?",
     "Pick three colours and split them roughly 60/30/10: one for the bag, one for the headcovers, and one for small accents like the brush tether or towel stripe. Keep to one pattern, and match leathers and metals."),
    ("Should my headcovers match my golf bag?",
     "They should belong to the same palette, but they don't need to match exactly. A contrasting cover in one of your three colours usually looks better than an exact match, and a different texture, such as sherpa against nylon, adds depth."),
    ("What is the most versatile golf bag colour?",
     "Navy, stone and dark green are the most forgiving. They work with most clothing and make a single accent colour look deliberate."),
    ("Can I mix headcover brands?",
     "Yes. Every setup in this guide mixes makers. The palette holds it together, not the logo."),
    ("How many patterns should be on a golf bag?",
     "One. Tartan, check, paisley or camo, choose one and keep the rest plain. Repeating the same pattern, such as a tweed bag with a matching tweed putter cover, counts as one."),
]


def price(h):
    dom, _, p, _, _ = P[h]
    return f"{CUR.get(dom, '$')}{p}"


def card(h, idx):
    dom, name, _, role, copy = P[h]
    fr = [f["local"] for f in FR[h]]
    label = H.unescape(f"{BRAND[dom]} {name}").replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>'
                   for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>'
                   for j in range(len(fr)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{"&#9733; Our pick &middot; " if h in PICKSET else ""}{BRAND[dom]} &middot; {role}</div>'
            f'<div class="product-name">{name} &middot; {price(h)}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="https://{dom}/products/{h}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


def swatches(cols, names):
    s = "".join(f'<span style="display:inline-flex;flex-direction:column;align-items:center;gap:6px;margin:0 8px;">'
                f'<span style="display:block;width:44px;height:44px;border-radius:50%;background:{c};border:1px solid rgba(0,0,0,.12);"></span>'
                f'<span style="font-family:var(--mono);font-size:9px;letter-spacing:.1em;text-transform:uppercase;opacity:.7;">{n}</span></span>'
                for c, n in zip(cols, names))
    return f'<div style="display:flex;justify-content:center;margin:6px 0 22px;">{s}</div>'


IMGSTY = 'style="width:100%;aspect-ratio:4/5;object-fit:cover;display:block;background:#eceae5;"'


def fig(x, big=False):
    b = BRAND.get(x["dom"], x["dom"])
    alt = H.escape(H.unescape(b) + " photograph: " + H.unescape(x["title"]))
    return (f'<figure style="margin:0;"><img src="{x["local"]}" alt="{alt}" loading="lazy" {IMGSTY} />'
            f'<figcaption class="ig-cap">{b}</figcaption></figure>')


def grid(items, minw):
    return (f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax({minw}px,1fr));gap:14px;max-width:1180px;margin:0 auto 26px;">'
            + "".join(fig(x) for x in items) + '</div>')


def mood():
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">The Mood</div>\n'
            f'  <h2 class="products-hdr" id="the-mood">Bags That Stop You on the First Tee</h2>\n'
            f'  <p class="cat-kicker"><strong>Before the rules</strong>These are the bags that made us want to write this.</p>\n'
            f'  {grid(BANDS["mood"], 300)}\n</section>\n')


def kit(i, k, n0):
    name, anchor, cols, names, kicker, paras, ids = k
    band = BANDS[BKEY[anchor]]
    makers = []
    for x in band:
        b = BRAND.get(x["dom"], x["dom"])
        if b not in makers:
            makers.append(b)
    credit = ", ".join(makers[:-1]) + " and " + makers[-1] if len(makers) > 1 else makers[0]
    prose = "\n".join(f'    <p style="margin:0 0 16px;">{p}</p>' for p in paras)
    cards = "\n".join(card(h, n0 + j) for j, h in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">Setup {i}</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{name}</h2>\n'
            f'  <p class="cat-kicker"><strong>{" &middot; ".join(names)}</strong>{kicker}</p>\n'
            f'  {grid(band[:2], 320)}\n'
            f'  {swatches(cols, names)}\n'
            f'  <div {PROSE}>\n{prose}\n  </div>\n'
            f'  {grid(band[2:], 200)}\n'
            f'  <p class="cat-kicker"><strong>The pieces</strong>The photographs come from {credit.rstrip(".")}. The {len(ids)} pieces below were all in stock when we checked.</p>\n'
            f'    <div class="products-grid">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>'
                     for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')

def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items, pos = [], 1
    for k in KITS:
        for h in k[6]:
            items.append({"@type": "ListItem", "position": pos, "url": f"https://{P[h][0]}/products/{h}", "name": H.unescape(f"{BRAND[P[h][0]]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-09-28", "dateModified": "2026-09-28",
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
            {"@type": "ListItem", "position": 3, "name": "Golf Bag Setup Ideas", "item": URL}]},
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


def main(apply_):
    ids = [h for k in KITS for h in k[6]]
    assert len(ids) == 29 == len(set(ids)) and set(ids) == set(P), (len(ids), set(P) ^ set(ids))
    for h in ids:
        assert FR.get(h), h
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Golf Bag Setup Ideas</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>A guide to the bag setup</span><span class="dot"></span>
    <span>6 setups &middot; 29 pieces</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A green Jones golf bag with cream sherpa headcovers on a bench in front of steel lockers" fetchpriority="high" /></div></div>
"""
    body += TAKE + mood()
    n = 1
    for i, k in enumerate(KITS, 1):
        s, n = kit(i, k, n)
        body += s
    body += NOTE + faq_html()
    out = head_top() + head_rest + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply")
        return
    OUT.write_text(out, encoding="utf-8")
    verify()


def verify():
    fin = OUT.read_text(encoding="utf-8")
    bad = []
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    for leak in ("Burnt Orange", "Manors Revisited", "Nicklaus"):
        if leak in above:
            bad.append(f"should not appear: {leak}")
    if fin.count('class="product-card"') != 29:
        bad.append("card count")
    if above.count('<figure style="margin:0;">') != 42:
        bad.append("inspiration photo count")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", above), re.I):
        bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file():
            bad.append(f"missing {f}")
    if bad:
        OUT.unlink()
        sys.exit("! removed. " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
