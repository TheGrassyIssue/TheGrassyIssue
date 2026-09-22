#!/usr/bin/env python3
"""build-needlepoint.py — "Needlepoint Belts", 18 belts + 3 key fobs.
22 September 2026.

Lenny: "I want to do a round up on Needlepoint belts, classic golf accessory
that looks great one & off the course", then "we have all 18 belts in the
dedicated page plus the key fobs?" — yes, all of them.

THE CRAFT DISTINCTION IS THE POST'S REASON TO EXIST. Lenny sent three links.
Two of them do not make needlepoint: Zilker builds leather and ribbon belts
(their own site search for "needlepoint" returns a gift card) and Imperial 1916
states "Decoration: flat embroidery" on cotton webbing in its own spec. Only
J.Press was the real thing. If two links from someone who knows golf accessories
land on the wrong craft, the distinction is what a reader needs — so it gets a
section rather than a footnote, and nobody is talked down to for it.

EIGHTEEN BELTS, SIX MAKERS, so several makers appear more than once. That is a
documented exception to the no-repeat-brands rule, agreed with Lenny: needlepoint
is a small field and the pattern IS the product. One belt per maker would have
made this a six-card post about an art form with hundreds of designs.

FACTS. Smathers & Branson's founding detail comes from their own Our Story page
(Bowdoin, 2004, the autumn in Vietnam, the "just a waist" sign-off, attributed to
Peter and Austin as it is on the page). Prices and stock are from each
storefront on 22 September 2026, USD, read from collection listings and product
pages — never from a per-product .json, which reported J.Press's entire line as
sold out while its product pages showed InStock with live add-to-cart.

Idempotent. Dry run by default.
"""
import io
import json
import pathlib
import re
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent
RES = ROOT / "research/needlepoint"
DONOR = ROOT / "drops/the-custom-wedge-report.html"
OUT = ROOT / "drops/the-needlepoint-belt-report.html"
SLUG = "/drops/the-needlepoint-belt-report"
# "GOLF" IS IN THE TITLE BECAUSE THE HEAD TERM HAS IT. The SERP for this category
# is "needlepoint golf belt", not "needlepoint belt": FootJoy and J.McLaughlin both
# carry "Golf Needlepoint Belt" in their own title tags, and Smathers & Branson
# rank on the collection page. The first version of this title said neither golf
# nor Grassy Issue, which left the one page on the site with the deepest coverage
# of the category matching the category's own name only by accident. 47 chars.
TITLE = "Needlepoint Golf Belts — 18 Hand-Stitched Picks"
# CUT FROM THE ORIGINAL, NOT FROM THE LOCALISED FRAME. The gallery copies are
# capped at 1100px, so cropping the hero out of one produced a 1100x471 band that
# the 1336px hero container then stretched. The source on Shopify is 2048x2048,
# which yields a 2000x857 hero at house size with no upscaling. A hero is the
# one image on the page where the localised copy is the wrong input.
HERO_SRC = ("https://cdn.shopify.com/s/files/1/0767/9233/2592/files/"
            "beachy-golf-belt-classic-navy.jpg")
HERO = "/images/needlepoint/hero.jpg"
SEO_MARK, SEO_END = "<!-- TGI-SEO -->", "<!-- /TGI-SEO -->"

# Maker order, anchor, kicker label, section lede.
MAKERS = [
 ("Smathers & Branson", "smathers", "BOWDOIN, 2004 · THE ONE EVERYONE KNOWS",
  "Two roommates were each given a needlepoint belt, went looking for somewhere to "
  "buy one, and found nobody was making them properly. Twenty-one years later they "
  "hold the USGA, Ryder Cup and Pebble Beach licences."),
 ("J.Press", "jpress", "NEW HAVEN, SINCE 1902 · $195 FLAT",
  "The Ivy outfitter treats the needlepoint belt as standard stock rather than a "
  "novelty. Every belt is hand-stitched at an inch and a quarter over full-grain "
  "leather tabs, and they all cost the same."),
 ("Charleston Belt", "charleston", "THE WIDEST RANGE HERE",
  "Charleston carries more designs than anyone else here, and the widest spread of "
  "tone \u2014 a plain basketweave at one end, a belt covered in Ric Flair at the other. "
  "They are also the only maker with a golf charity edition."),
 ("Good Threads", "goodthreads", "STITCHED IN HAITI · 18-COUNT CANVAS",
  "The cheapest hand-stitched belts in the roundup at $125, worked on 18-count canvas "
  "and finished with full-grain Italian leather. Every size is in stock, which is not "
  "true of anyone else here."),
 ("Baldwin Belts", "baldwin", "$124 · MADE TO ORDER",
  "Small runs, often one or two of a size, and a catalogue that reads like somebody's "
  "actual interests rather than a merchandising plan. Sailboats, bourbon, a golf cart."),
 ("Fish Creek", "fishcreek", "BESPOKE FIRST",
  "Mostly a commission house — you send them the thing you want stitched and they "
  "build it. A short rack of finished designs sits alongside the custom work."),
]

COPY = {
 "smathers-branson-beachy-golf-classic-navy":
   "Golf carts and palm trees stitched across classic navy, on the full-grain leather "
   "backing and removable brass buckle that Smathers & Branson put on everything. The "
   "Beachy is the one that reads as golf from ten feet and as pattern from two, which "
   "is the whole trick of a needlepoint belt.",
 "smathers-branson-usga-126th-us-open-shinnecock":
   "The official USGA belt for the 126th US Open at Shinnecock Hills, with the "
   "clubhouse stitched centre-panel and the championship text either side. "
   "Commemorative belts usually age badly. This one is saved by the building, which "
   "has looked the same since 1892.",
 # NOTE: slugify() truncates at 46 chars, so this key loses the final "s"
 # of "skeletons". Matching the manifest exactly rather than fixing the
 # truncation, because the image filenames on disk already use it.
 "smathers-branson-grateful-dead-dancing-skeleto":
   "Dancing skeletons in full spectrum on black, under a licence Smathers & Branson "
   "hold alongside the Rolling Stones and Pink Floyd. It is the clearest argument in "
   "the roundup for the off-course half: nothing about it says golf, and it works over "
   "denim on a Friday.",
 "j-press-dancing-bear-oatmeal":
   "J.Press has sold Ivy clothing since 1902 and treats the needlepoint belt as "
   "ordinary stock. The Dancing Bear runs the motif across oatmeal, with full-grain "
   "leather tabs and a solid brass buckle at an inch and a quarter. Sized up one from "
   "your trouser, per their own rule.",
 "j-press-dark-n-stormy-navy":
   "A cocktail rendered in yarn on navy, which is about as J.Press as an object gets. "
   "The construction is identical across their line, so the only decision is the "
   "pattern, and this is the one that does the most work away from a golf course.",
 "j-press-skull-and-crossbones":
   "Skull and crossbones on navy, an old New Haven wink that predates every other "
   "reference on this page. Same hand-stitching, same leather tabs, same brass. "
   "Worn with grey flannel it reads as heraldry rather than a joke.",
 "charleston-ric-flair":
   "Charleston stitched the Nature Boy onto a belt: the robe, the sunglasses, the strut, "
   "rendered in yarn on a rose ground. It is the loudest thing here by a distance and "
   "the most fun, and the leather backing and hand-stitching are the same as the "
   "sober ones.",
 "charleston-golf-clubs-and-flags-crossed":
   "Crossed clubs and pin flags on a blue ground, which is the most traditional golf "
   "motif here and the easiest to wear. Hand-stitched over leather with a "
   "brass buckle. Four of its six sizes are live.",
 "charleston-yac-first-tee-commemorative-edition":
   "Charleston partner with The First Tee of Greater Charleston on this one, price it "
   "below retail for supporters of the programme, and donate a portion of every sale. "
   "It comes in three designs, one of which is called &ldquo;A Little Tournament in "
   "Augusta&rdquo;. Every size is in stock.",
 "charleston-texture-basketweave-steel-grey-and":
   "No motif at all — steel grey and navy worked as a basketweave texture, so it reads "
   "as a woven belt until somebody looks closely. For anyone who wants the hand and the "
   "leather without a scene stitched across their waist.",
 "charleston-golf-beware-of-the-bogey-man":
   "Golfers mid-swing and a bogey man stitched across navy, with enough going on that "
   "it rewards a second look. The last size is live, and Charleston does not restock "
   "designs on a schedule.",
 "good-threads-golf-flags-green":
   "Pin flags and clubs on a green ground, hand-stitched on 18-count canvas in Haiti "
   "and finished with full-grain Italian leather. At $125 it is the cheapest "
   "hand-stitched belt here, and every size is in stock.",
 "good-threads-golf-tees":
   "Scattered tees and balls across green, which is the most cheerful pattern in the "
   "roundup and the easiest to hand to somebody who does not own one yet. Same canvas, "
   "same Italian leather, same price.",
 "good-threads-golf-bags":
   "Carry bags stitched in a row on navy — a bag belt for a golfer who has opinions "
   "about bags. Good Threads photograph flat on white and let the pattern carry it, "
   "which it does.",
 "baldwin-belts-golf-cart-for-a-picture-perfect":
   "A single cart stitched repeating across the panel, made to order in small runs. "
   "Baldwin's catalogue reads like a list of somebody's actual interests rather than a "
   "merchandising plan, and this is the golf entry. One size left.",
 "baldwin-belts-sailboat-handcrafted-nautical-de":
   "Sailboats on navy, hand-stitched and backed in leather at $124, which is the "
   "cheapest way into the craft short of Good Threads. The off-course belt for anyone "
   "whose other hobby involves water.",
 "baldwin-belts-patriotic-flag-design":
   "Flags worked edge to edge with the most frames of any Baldwin belt here, so the "
   "stitch density is actually visible before you buy. Four sizes live.",
 "fish-creek-alabama-traditions":
   "Fish Creek mostly takes commissions — you send the thing you want stitched and they "
   "build it around ten thousand stitches. Alabama Traditions is one of the few "
   "finished designs sitting on the rack, and it shows what the bespoke work looks like.",
 "charleston-azalea-on-augusta-green":
   "An azalea on Augusta green, which is about as close to naming the tournament as a "
   "product can get without a licence. Same hand-stitching as the belts, on a key ring, "
   "for a tenth of the money.",
 "charleston-golf-green-red-tee":
   "A red tee on a green ground, stitched and leather-backed. The cheapest entry point "
   "to any of these makers, and the one that survives being carried in a pocket with "
   "keys on it.",
 "baldwin-belts-golf-ball":
   "A single golf ball on a brass lobster clasp, hand-stitched, $32. Baldwin's is the "
   "least fussy of the three fobs and the one that looks least like a gift shop.",
}

INTRO = [
 "The needlepoint belt is a golf accessory that works better away from the course "
 "than on it, and six makers are still building them one stitch at a time.",

 "The craft is simple to describe and slow to do. Yarn is worked by hand through an "
 "open canvas mesh, one stitch per hole, until a pattern emerges on a strip roughly "
 "an inch and a quarter wide. That strip is then backed with leather and hung on a "
 "brass buckle. A single belt runs to ten thousand stitches or more. Nothing about "
 "the process has changed in a century, which is why the belts look the way they do "
 "and why they cost between a hundred and twenty-four and two hundred and twenty "
 "dollars.",

 "Smathers & Branson began as two roommates at Bowdoin in 2004 who had each been "
 "given a needlepoint belt and could not find anywhere to buy another. They now hold "
 "the USGA, Ryder Cup and Pebble Beach licences. J.Press has been selling them out of "
 "New Haven for far longer without ever making a fuss about it.",

 "What follows is eighteen belts from six makers, every price read from the maker&rsquo;s "
 "own store this week, and three key fobs at the end for anyone who wants the stitch "
 "without the commitment. Roughly half carry a golf motif. The other half are here "
 "because the brief was a belt that works on a Tuesday as well as a Saturday.",
]

CRAFT = ("What counts as needlepoint", "craft", "THE CRAFT",
 "Three things get called needlepoint and only one of them is. It is a useful "
 "distinction to own before spending two hundred dollars.",
 ["<strong>Needlepoint</strong> is yarn stitched by hand through an open canvas mesh, "
  "one stitch per hole, until the pattern fills the canvas. The finished strip has "
  "weight and a visible grid, the back is a mess of yarn, and it gets mounted onto "
  "leather afterwards. Every belt on this page is this.",
  "<strong>Embroidery</strong> is thread worked onto fabric that is already finished — "
  "webbing, twill, canvas. It is machine-fast, it lies flat, and it can render finer "
  "detail than needlepoint can. Imperial 1916 make golf belts this way and say so "
  "plainly in their own spec: cotton webbing, flat embroidery, woven ribbon backing. "
  "Good belts. Different craft.",
  "<strong>Woven ribbon and leather</strong> is the third category, where the pattern "
  "is in the weave or tooled into the hide rather than stitched on top. Zilker Belts "
  "in Austin build this way, in full-grain leather with contrast stitching.",
  "The reason to keep them apart is that the price only makes sense for one of them. "
  "A hand-stitched belt costs what it costs because somebody sat and did ten thousand "
  "stitches. An embroidered belt at the same price is a different proposition, and a "
  "reader should be able to tell which one they are looking at from the listing."])

BUYING = ("Before you buy", "before", "SIZING AND STOCK",
 "Two things about needlepoint belts catch people out, and one of them will cost you "
 "a return.",
 ["<strong>Order one size up from your trousers.</strong> J.Press states it on every "
  "product page and the rest assume you know: a needlepoint belt is measured tip to "
  "buckle, not waist. A 34 trouser takes a 36 belt. This is the single most common "
  "reason one of these goes back.",
  "<strong>Stock is thin by design.</strong> These are hand-stitched in small runs, so "
  "a design you like will often have one or two sizes live and no restock date. Good "
  "Threads is the exception and has every size in every belt on this page. Charleston's "
  "Bogey Man and Baldwin's Golf Cart are each down to a single size as this goes up.",
  "<strong>The buckle usually comes off.</strong> Smathers & Branson build theirs to "
  "detach, which means a worn strap can be rehung rather than replaced, and a brass "
  "buckle can be swapped for nickel. Check before you assume the belt is a single "
  "object.",
  "All prices were read from each maker&rsquo;s own storefront on 22 September 2026 and "
  "are in US dollars."])

FAQ = [
 ("What is a needlepoint belt?",
  "A strip of canvas hand-stitched with yarn, one stitch per hole of an open mesh, "
  "then backed with leather and fitted to a buckle. A belt runs to ten thousand "
  "stitches or more, which is why they cost between $124 and $220 and why no two are "
  "quite identical."),
 ("Is an embroidered belt the same thing?",
  "No. Embroidery is thread worked onto fabric that is already finished, usually by "
  "machine, and it lies flat. Needlepoint is yarn worked through open canvas by hand "
  "and has visible grid and weight. Both make good belts; only one explains a "
  "two-hundred-dollar price."),
 ("What size needlepoint belt should I order?",
  "One size up from your trouser size. A 34 trouser takes a 36 belt. J.Press prints "
  "this on every product page and the other makers assume you know it."),
 ("Who makes the best needlepoint golf belts?",
  "Smathers & Branson hold the USGA, Ryder Cup and Pebble Beach licences and have the "
  "deepest golf range. Good Threads are the cheapest hand-stitched at $125 with every "
  "size in stock. Charleston Belt have the widest spread of designs. J.Press are $195 "
  "flat and have been at it since 1902."),
 ("Can you still buy J.Press needlepoint belts?",
  "Yes. Their product pages show in stock with live add-to-cart across the "
  "needlepoint line at $195, as of 22 September 2026, though individual sizes sell "
  "out."),
]


def cut_hero(apply_):
    man = json.loads((RES / "manifest.json").read_text(encoding="utf-8"))
    src = man["smathers-branson-beachy-golf-classic-navy"]["url"] + ".json"
    import urllib.request
    UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}
    def get(u):
        return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=45).read()
    first = json.loads(get(src))["product"]["images"][0]["src"]
    im = Image.open(io.BytesIO(get(first))).convert("RGB")
    w, h = im.size
    ch = round(w / (21 / 9))
    if ch > h:
        sys.exit(f"! hero source too short for 21:9 — {w}x{h}")
    top = round((h - ch) * 0.5)
    band = im.crop((0, top, w, top + ch))
    tw = min(2000, band.width)                 # never upscale
    band = band.resize((tw, round(tw / (21 / 9))), Image.LANCZOS)
    p = ROOT / HERO.lstrip("/")
    print(f"  hero: {w}x{h} -> {band.size[0]}x{band.size[1]}")
    if band.width < 1400:
        sys.exit(f"! hero is only {band.width}px wide; the container is ~1336px")
    if apply_:
        band.save(p, "JPEG", quality=88, optimize=True, progressive=True)
    return band.size


def dims(rel):
    """Real pixel size, read off the file. Never guessed.

    width/height on an <img> is what stops the page reflowing as each frame
    arrives — the browser reserves the box before the bytes land. Getting the
    numbers wrong is worse than omitting them, because the browser trusts them
    and lays out to a shape the image does not have. So these come from the
    file on disk, not from the constants the resize was *asked* for.
    """
    with Image.open(ROOT / rel.lstrip("/")) as im:
        return im.size


def gallery(slug, m):
    fr = ""
    for i, f in enumerate(m["frames"]):
        w, h = dims(f)
        fr += (f'<div class="pg-frame"><img src="{f}" alt="{m["title"]} &middot; view {i+1} of '
               f'{len(m["frames"])}" loading="lazy" decoding="async" '
               f'width="{w}" height="{h}" /></div>')
    # NO DOTS ON A SINGLE-FRAME CARD. verify-post.py requires dots == 0 when
    # data-frames < 2, because one dot on a gallery that cannot move is a control
    # that does nothing. Good Threads and Baldwin publish one usable image for
    # some products, so three cards here are genuinely single-frame.
    dots = ("" if len(m["frames"]) < 2 else
            "".join(f'<button class="pg-dot{" on" if i == 0 else ""}" data-i="{i}" '
                    f'aria-label="View image {i+1}"></button>'
                    for i in range(len(m["frames"]))))
    ctrl = ('<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            '<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            if len(m["frames"]) > 1 else "")
    return (f'<div class="product-gallery"><div class="pg-track">{fr}</div>{ctrl}'
            f'<span class="pg-count">1/{len(m["frames"])}</span>'
            f'<div class="pg-dots">{dots}</div></div>')


def card(slug, m):
    if slug not in COPY:
        sys.exit(f"! no copy written for {slug}")
    return (f'<div class="product-card" data-frames="{len(m["frames"])}">{gallery(slug, m)}'
            f'<div class="product-body"><div class="product-brand">{m["brand"]}</div>'
            f'<div class="product-name">{m["title"]} &middot; {m["price"]}</div>'
            f'<div class="product-desc">{COPY[slug]}</div>'
            f'<a href="{m["url"]}" target="_blank" rel="noopener" class="product-link">'
            f'Shop &#8599;</a></div></div>')


def section(h2, anchor, kick, lede, cards):
    return (f'\n<section class="products">\n<h2 id="{anchor}">{h2}</h2>\n'
            f'<p class="cat-kicker"><strong>{kick}</strong>{lede}</p>\n'
            f'<div class="products-grid">\n      ' + "\n      ".join(cards) +
            '\n</div>\n</section>\n')


def essay(h2, anchor, kick, lede, paras):
    ps = "\n    ".join(f"<p>{p}</p>" for p in paras)
    return (f'\n<section class="products">\n<h2 id="{anchor}">{h2}</h2>\n'
            f'<p class="cat-kicker"><strong>{kick}</strong>{lede}</p>\n</section>\n'
            f'<div class="writeup">\n  <div class="writeup-body">\n    {ps}\n  </div>\n</div>\n')


def body(man, hero_wh):
    secs = ""
    used = set()
    for label, anchor, kick, lede in MAKERS:
        picks = [(s, m) for s, m in man.items() if m["brand"] == label and m["kind"] == "belt"]
        if not picks:
            sys.exit(f"! no belts found for {label}")
        used |= {s for s, _ in picks}
        secs += section(label, anchor, kick, lede, [card(s, m) for s, m in picks])
    fobs = [(s, m) for s, m in man.items() if m["kind"] == "key"]
    used |= {s for s, _ in fobs}
    secs += section("Key fobs", "fobs", "THE CHEAP WAY IN",
                    "These carry the same hand-stitching on a key ring, between $32 and $35. "
                    "Smathers &amp; Branson make twenty key fobs and not one golf design, "
                    "so these come from Charleston and Baldwin.",
                    [card(s, m) for s, m in fobs])
    missing = set(man) - used
    if missing:
        sys.exit(f"! {len(missing)} product(s) never made it onto the page: {sorted(missing)}")
    secs += essay(*CRAFT)
    secs += essay(*BUYING)
    qs = "\n    ".join(f'<details open class="faq-q"><summary>{q}</summary><p>{a}</p></details>'
                       for q, a in FAQ)
    secs += (f'\n<div class="writeup">\n  <div class="writeup-body">\n'
             f'  <h2 class="products-hdr sec">Questions</h2>\n'
             f'  <div class="faq">\n    {qs}\n  </div>\n  </div>\n</div>\n')
    intro = "\n    ".join(f"<p>{p}</p>" for p in INTRO)
    belts = sum(1 for m in man.values() if m["kind"] == "belt")
    return f"""<header class="drop-header">
  <h1>{TITLE}</h1>
  <div class="drop-meta">
    <span>{belts} Belts &middot; {len(man)-belts} Key Fobs</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{HERO}" alt="A Smathers &amp; Branson needlepoint golf belt, carts and palm trees stitched on navy" width="{hero_wh[0]}" height="{hero_wh[1]}" fetchpriority="high" decoding="async" /></div></div>

<div class="writeup">
  <div class="writeup-body">
    {intro}
  </div>
</div>
{secs}"""


def structured(man, hero_wh):
    """ItemList + BreadcrumbList, built from the same manifest the cards are.

    ItemList follows the shape already shipping on the-drop-report-september-2026
    and off-course-vol-2 — position, name, url — so a roundup on this site looks
    like every other roundup on this site. It is derived from the manifest rather
    than hand-listed, which is the only way it cannot drift out of step with the
    21 cards on the page.

    BreadcrumbList marks up a trail that was already visible and unannotated.
    """
    items = [{"@type": "ListItem", "position": i + 1, "name": f'{m["brand"]} {m["title"]}',
              "url": m["url"],
              "image": "https://thegrassyissue.com" + m["frames"][0]}
             for i, (s, m) in enumerate(man.items())]
    il = {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE,
          "numberOfItems": len(items), "itemListElement": items}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Feed",
         "item": "https://thegrassyissue.com/"},
        {"@type": "ListItem", "position": 2, "name": "Drops & Brands",
         "item": "https://thegrassyissue.com/#feed"},
        {"@type": "ListItem", "position": 3, "name": TITLE}]}
    return (f"{SEO_MARK}\n"
            f'<script type="application/ld+json">{json.dumps(il, ensure_ascii=False)}</script>\n'
            f'<script type="application/ld+json">{json.dumps(bc, ensure_ascii=False)}</script>\n'
            f"{SEO_END}\n")


def main(apply_):
    man = json.loads((RES / "manifest.json").read_text(encoding="utf-8"))
    hero_wh = cut_hero(apply_)
    donor = DONOR.read_text(encoding="utf-8")
    header = donor.find('<header class="drop-header"')
    more = donor.find('<div class="more"')
    if min(header, more) < 0 or header > more:
        sys.exit("! donor structure not recognised")
    page = donor[:header] + body(man, hero_wh) + donor[more:]

    crumb = ('<div class="breadcrumb">\n  <a href="/">Feed</a><span>/</span>\n'
             '  <a href="/#feed">Drops &amp; Brands</a><span>/</span>\n  ' + TITLE + '\n</div>')
    page, n = re.subn(r'<div class="breadcrumb">.*?</div>', lambda m: crumb, page,
                      count=1, flags=re.S)
    if not n:
        sys.exit("! breadcrumb not found — it would still name the donor post")

    desc = ("Eighteen hand-stitched needlepoint golf belts from six makers, $124 to $220, "
            "plus three key fobs — and what separates needlepoint from embroidery.")
    h = page[:page.find("</head>")]
    def sub1(pat, rep, s):
        s2, k = re.subn(pat, lambda m: rep, s, count=1)
        if not k:
            sys.exit(f"! head pattern missing: {pat[:40]}")
        return s2
    h = sub1(r"<title>.*?</title>", f"<title>{TITLE}</title>", h)
    h = sub1(r'<meta name="description" content="[^"]*"',
             f'<meta name="description" content="{desc}"', h)
    h = sub1(r'<link rel="canonical" href="[^"]*"',
             f'<link rel="canonical" href="https://thegrassyissue.com{SLUG}"', h)
    for p, r in ((r'<meta property="og:title" content="[^"]*"', f'<meta property="og:title" content="{TITLE}"'),
                 (r'<meta property="og:description" content="[^"]*"', f'<meta property="og:description" content="{desc}"'),
                 (r'<meta property="og:url" content="[^"]*"', f'<meta property="og:url" content="https://thegrassyissue.com{SLUG}"'),
                 (r'<meta name="twitter:title" content="[^"]*"', f'<meta name="twitter:title" content="{TITLE}"'),
                 (r'<meta name="twitter:description" content="[^"]*"', f'<meta name="twitter:description" content="{desc}"')):
        h = re.sub(p, lambda m: r, h, count=1)
    hl = '"headline": ' + json.dumps(TITLE)
    h = re.sub(r'"headline"\s*:\s*"(?:[^"\\]|\\.)*"', lambda m: hl, h, count=1)
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                         "mainEntity": [{"@type": "Question", "name": q,
                                         "acceptedAnswer": {"@type": "Answer", "text": a}}
                                        for q, a in FAQ]}, ensure_ascii=False)
    h, k = re.subn(r'\{\s*"@context"[^{]*?"@type"\s*:\s*"FAQPage".*?\}(?=\s*</script>)',
                   lambda m: faq_ld, h, count=1, flags=re.S)
    if not k:
        sys.exit("! no FAQPage block in the donor head")
    h = re.sub(r'"url"\s*:\s*"https://thegrassyissue\.com/drops/[^"]*"',
               lambda m: f'"url": "https://thegrassyissue.com{SLUG}"', h)

    # ---- THE SOCIAL IMAGE. The donor hands down /images/og-image.jpg, which 121
    # other drops pages are also using, so every share of every post on this site
    # currently shows one identical picture. A roundup whose whole argument is
    # visual is the wrong page to let inherit it.
    hero_abs = "https://thegrassyissue.com" + HERO
    h = sub1(r'<meta property="og:image" content="[^"]*"',
             f'<meta property="og:image" content="{hero_abs}"', h)
    h = re.sub(r'\s*<meta property="og:image:(?:width|height)"[^>]*>', "", h)
    h = re.sub(r'\s*<meta name="twitter:image"[^>]*>', "", h)
    h = re.sub(r'(<meta property="og:image" content="[^"]*"\s*/?>)',
               lambda m: (m.group(1) +
                          f'\n  <meta property="og:image:width" content="{hero_wh[0]}" />'
                          f'\n  <meta property="og:image:height" content="{hero_wh[1]}" />'
                          f'\n  <meta name="twitter:image" content="{hero_abs}" />'),
               h, count=1)

    # ---- ItemList + BreadcrumbList, inserted last so a re-run replaces rather
    # than stacks. The donor carries neither, but marker-delimiting it means a
    # future donor that does carry one cannot produce two.
    h = re.sub(re.escape(SEO_MARK) + r".*?" + re.escape(SEO_END) + r"\n?", "", h, flags=re.S)
    h = h.rstrip() + "\n" + structured(man, hero_wh)
    page = h + page[page.find("</head>"):]

    # ---- guards, read on the finished page, from <body> not from the header ----
    bad = []
    all_body = page[page.find(">", page.find("<body")) + 1:page.find('<div class="more"')]
    plain = re.sub(r"<[^>]+>", " ", all_body)
    if "custom-wedges" in all_body:
        bad.append("donor imagery survived")
    for ph in ("Show Out", "Vokey", "Grindworks", "Custom Wedge Report"):
        if ph.lower() in plain.lower():
            bad.append(f"donor copy survived: {ph!r}")
    n_cards = all_body.count('<div class="product-card"')
    if n_cards != len(man):
        bad.append(f"{n_cards} cards, expected {len(man)}")
    if all_body.count('<div class="products-grid">') != len(MAKERS) + 1:
        bad.append("a section is missing its products-grid — cards would render full width")
    for slug, m in man.items():
        for f in m["frames"]:
            if not (ROOT / f.lstrip("/")).is_file():
                bad.append(f"missing image {f}")
        if f'data-frames="{len(m["frames"])}"' not in all_body:
            bad.append(f"{slug}: no card declaring {len(m['frames'])} frames")
    # data-frames must equal the real frame count on every card
    for dm, blk in re.findall(r'data-frames="(\d+)"(.*?)</div>\s*<div class="product-body"',
                              all_body, re.S):
        if blk.count("pg-frame") != int(dm):
            bad.append(f"a card says {dm} frames but renders {blk.count('pg-frame')}")
    # ---- SEO guards, all read off `page` as a browser/crawler would see it ----
    head_fin = page[:page.find("</head>")]
    if "og-image.jpg" in head_fin:
        bad.append("og:image still the shared site image")
    n_og = head_fin.count('property="og:image"')
    if n_og != 1:
        bad.append(f"{n_og} og:image tags, expected 1")
    if f'content="https://thegrassyissue.com{HERO}"' not in head_fin:
        bad.append("og:image does not point at this post's hero")
    for tag in ("og:image:width", "og:image:height", "twitter:image"):
        if head_fin.count(tag) != 1:
            bad.append(f"{head_fin.count(tag)} {tag} tags, expected 1")
    # every ld+json block must parse — a schema block that 404s the validator is
    # worse than none, and json.dumps upstream is no proof of what landed here
    types = []
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S):
        try:
            d = json.loads(blk)
        except json.JSONDecodeError as e:
            bad.append(f"unparseable ld+json: {e}"); continue
        types.append(d.get("@type"))
    for need in ("ItemList", "BreadcrumbList", "FAQPage", "Article"):
        if types.count(need) != 1:
            bad.append(f"{types.count(need)} {need} blocks, expected 1")
    ild = next((json.loads(b) for b in
                re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S)
                if '"ItemList"' in b), None)
    if ild:
        if ild["numberOfItems"] != len(man) or len(ild["itemListElement"]) != len(man):
            bad.append(f"ItemList declares {ild['numberOfItems']} of {len(man)} products")
        # the schema must name the things the page actually shows
        for it in ild["itemListElement"]:
            if it["url"] not in all_body:
                bad.append(f"ItemList links {it['url']}, which no card on the page does")
                break
    if TITLE not in head_fin or f"<h1>{TITLE}</h1>" not in all_body:
        bad.append("title and h1 disagree")
    if len(TITLE) > 60:
        bad.append(f"title is {len(TITLE)} chars, over the 60 that render in a SERP")
    dmeta = re.search(r'<meta name="description" content="([^"]*)"', head_fin)
    if not dmeta or not 120 <= len(dmeta.group(1)) <= 160:
        bad.append(f"description is {len(dmeta.group(1)) if dmeta else 0} chars, want 120-160")
    # CLS / LCP: every image sized, hero prioritised and not lazy
    imgs = re.findall(r"<img[^>]*>", all_body)
    unsized = [i for i in imgs if not re.search(r'width="\d+"', i)]
    if unsized:
        bad.append(f"{len(unsized)} of {len(imgs)} images carry no width/height")
    hero_img = next((i for i in imgs if HERO in i), "")
    if 'fetchpriority="high"' not in hero_img:
        bad.append("hero is not fetchpriority=high — it is the LCP element")
    if 'loading="lazy"' in hero_img:
        bad.append("hero is lazy-loaded, which defers the LCP element")
    for i in imgs:
        m_ = re.search(r'src="([^"]+)"', i)
        w_ = re.search(r'width="(\d+)"', i)
        h_ = re.search(r'height="(\d+)"', i)
        if m_ and w_ and h_:
            f_ = ROOT / m_.group(1).lstrip("/")
            if f_.is_file():
                with Image.open(f_) as im_:
                    if im_.size != (int(w_.group(1)), int(h_.group(1))):
                        bad.append(f"{m_.group(1)}: declared {w_.group(1)}x{h_.group(1)}, "
                                   f"file is {im_.size[0]}x{im_.size[1]}")

    words = len(plain.split())
    if words < 1200:
        bad.append(f"{words} words, verify-post.py needs 1200")
    if re.search(r"\bworth\b", re.sub(r"fort worth", "", plain, flags=re.I), re.I):
        bad.append("banned word in body copy")
    if bad:
        sys.exit("! " + "\n    ".join(bad))

    print(f"  {n_cards} cards, {sum(len(m['frames']) for m in man.values())} frames, {words} words")
    if not apply_:
        print("\n  dry run — pass --apply")
        return
    OUT.write_text(page, encoding="utf-8")
    print(f"  wrote {OUT.relative_to(ROOT)} ({len(page)//1024} KB)")


if __name__ == "__main__":
    main("--apply" in sys.argv)
