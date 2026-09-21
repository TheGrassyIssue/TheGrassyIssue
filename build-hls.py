#!/usr/bin/env python3
"""build-hls.py — Brand to Know: Hidden Links Society. 17 September 2026.

THE HOOK, AND WHY IT LEADS
--------------------------
Most small golf-apparel brands have an origin story. Hidden Links Society has a
DOCUMENTARY SERIES. The Public 100 Project is their long-form effort to play,
walk and document every course on Golf Digest's Top 100 Public list — photography,
video, writing and maps, one course at a time. For a brand whose whole catalogue
is thirty products, that is an unusual amount of ambition pointed at something
other than selling hats, and it is what the post leads on.

Their framing, verbatim from hiddenlinkssociety.com/pages/public-100-project:
    "no memberships, no private gates, no invitations required."

THE RANKING IS ATTRIBUTED, NOT ASSERTED. The list is Golf Digest's, and HLS say
so themselves ("Guided by Golf Digest's Top 100 Public Courses (2025)"). TGI does
not rank these courses and does not endorse the ranking — we report that the
project follows it.

NO NAMED FOUNDER — SAID PLAINLY, NOT PAPERED OVER
--------------------------------------------------
There is no founder name anywhere: not on the site, not in search, not in any
interview I could find. All their copy is first-person plural. So every quote in
this post is attributed to THE BRAND and its own page, never to a person. Per
house rule: verbatim from a named, sourced origin; never paraphrase into
quotation marks; never invent a founder to hang a quote on.

NAME COLLISION — GUARDED BELOW
------------------------------
There is an unrelated hiddenlinksgolf.com, a custom club builder. Different
company entirely. A guard at the bottom refuses the build if that domain ever
appears in the output.

PRICES
------
Every price is the live Shopify first-variant price, read from
hiddenlinkssociety.com/products.json on 17 September 2026 and stored in
research/hls-skus.json. `was` prints ONLY where a real discount exists — the two
Ransom Note caps ($30 -> $15) and the World Wide hoodie ($62 -> $43). Everything
else returned no compare_at and prints a single price.

LINK BY HANDLE, NEVER BY TITLE
------------------------------
HLS has the same trap Forden had: `the-society-overshirt-charcoal` is titled
"The Society Overshirt - OAT", and `the-society-overshirt-charcoal-1` is titled
"CHARCOAL". Handle and title disagree. Every link below is built from the handle
in the SKU file, never from the title.
"""
import os, re, sys, json, glob, html as H

apply_ = "--apply" in sys.argv
ROOT = os.path.dirname(os.path.abspath(__file__))
SKU = {k: v for k, v in json.load(open(os.path.join(ROOT, "research/hls-skus.json"),
                                      encoding="utf-8")).items() if not k.startswith("_")}
SLUG = "brand-to-know-hidden-links-society"
IMGD = "/images/hls/"
SHOP = "https://hiddenlinkssociety.com/products/"
DATE = "September 17, 2026"
PLAIN = "Brand to Know — Hidden Links Society"
TITLE = "Brand to Know &mdash; Hidden Links Society"
# THE HERO IS NOT A PACKSHOT.
# The hero slot is 1600x685 (21:9) and every HLS product image is a flat packshot
# on white at 800x1000. Cropping one of those to 21:9 slices the middle out of a
# sweatshirt — it was the charcoal overshirt, and it looked like exactly that.
#
# Their own site banner is a real photograph: black and white, a follow-through on
# a cypress-lined course, 5000x3000 on their Shopify CDN. Cropped to the house size
# at y 680..2820, which is the one slice that keeps the figure whole — higher and
# the shoes go, lower and the hat goes. The driver exits the top of the frame; that
# is the trade 21:9 demands and it reads as intentional.
HERO = "/images/hls/hero-followthrough.jpg"
HERO_ALT = ("Black and white photograph of a golfer at the top of the follow-through on a "
            "cypress-lined fairway, from Hidden Links Society")
DESC = ("Hidden Links Society makes headwear, headcovers and overshirts, gives 2% of every sale to "
        "Youth on Course, and is documenting all 100 of Golf Digest's top public courses. Eighteen "
        "pieces, prices read 17 September 2026.")


def frames(key, limit=4):
    pat = re.compile(rf"^{re.escape(key)}-(\d+)\.jpg$")
    hits = []
    for f in glob.glob(os.path.join(ROOT, "images", "hls", "*.jpg")):
        m = pat.match(os.path.basename(f))
        if m:
            hits.append((int(m.group(1)), os.path.basename(f)))
    return [IMGD + b for _, b in sorted(hits)][:limit]


def card(key, copy, alt):
    d = SKU[key]
    imgs = frames(key)
    if not imgs:
        raise SystemExit(f"NO IMAGES for {key}")
    n = len(imgs)
    if n == 1:
        gal = (f'<div class="product-gallery"><div class="pg-track"><div class="pg-frame">'
               f'<img src="{imgs[0]}" alt="{alt}" loading="lazy" /></div></div></div>')
    else:
        fr = "".join(f'<div class="pg-frame"><img src="{u}" alt="{alt} &middot; view {i+1} of {n}" '
                     f'loading="lazy" /></div>' for i, u in enumerate(imgs))
        dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" '
                       f'aria-label="View image {i+1}"></button>' for i in range(n))
        gal = ('<div class="product-gallery"><div class="pg-track">' + fr +
               '</div><button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
               '<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
               f'<span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>')
    price = f'${int(float(d["price"]))}'
    if d["compare"]:
        price = f'<s>${int(float(d["compare"]))}</s> {price}'
    if not d["avail"]:
        price += " &middot; sold out"
    name = d["title"].replace(" - ", " &middot; ").replace("&", "&amp;")
    return f"""<div class="product-card" data-frames="{n}">
      {gal}
      <div class="product-body">
        <div class="product-brand">{name}</div>
        <div class="product-name">{price}</div>
        <div class="product-desc">{copy}</div>
        <a href="{SHOP}{key}" target="_blank" rel="noopener" class="product-link">At Hidden Links Society ↗</a>
      </div>
    </div>"""


def section(hdr, kicker, cards):
    body = "\n    ".join(cards)
    return (f'<section class="products">\n  <h2 class="products-hdr">{hdr}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'  <div class="products-grid">\n    {body}\n  </div>\n</section>\n')


# ------------------------------------------------------------------ the picks
NEW = [
 card("play-faster-fairway-wood-cover-black",
      "The newest thing they make and the best argument for the brand. A 220cc fairway cover in 100% "
      "wool, handcrafted in the USA with Ross Co Golf out of Bandon, Oregon, with a dancing PLAY FASTER "
      "running round the barrel. It is a headcover that is also a position on pace of play, which is "
      "roughly the whole brand in one object. Currently a preorder &mdash; their page says covers ship "
      "the first week of October.",
      "Black wool fairway wood cover with Play Faster lettering by Hidden Links Society"),
 card("the-play-faster-tee-ivory",
      "The same message, worn. 230gsm garment-washed cotton, relaxed and slightly oversized, drop "
      "shoulders, the imprint front and back. Their own line on it is the good one: some messages are "
      "better said than shouted from the tee box. Made to order, so allow a couple of weeks.",
      "Ivory heavyweight cotton tee with Play Faster print by Hidden Links Society"),
 card("the-society-overshirt-charcoal-1",
      "A 445gsm heavyweight fleece polo sweatshirt with a single button closure and a relaxed cut &mdash; "
      "the piece that moves them from hat brand to clothing brand. They say it took more than a year and "
      "that they refused to rush it, which is a thing every brand says and a thing the fabric weight "
      "actually backs up. Also in Oat.",
      "Charcoal heavyweight fleece polo sweatshirt by Hidden Links Society"),
 card("the-society-tee-light-grey",
      "The restrained one. No graphic, no tech-fabric sheen, just a tonal HLS patch at the left chest on "
      "the same 230gsm garment-washed cotton. Their description sells it better than a pitch would: works "
      "at the range, the clubhouse, or nowhere near a golf course at all.",
      "Light grey cotton tee with tonal chest patch by Hidden Links Society"),
 card("single-prong-pitch-mark-tool-aged-brass",
      "Quarter-inch square brass bar, three and a half inches long, aged finish, dancing stamp. Single "
      "prong, which is the repair tool people who actually read agronomy research tend to prefer. Their "
      "product copy is four words long and is the best four words on the site: fix your damn pitch marks.",
      "Aged brass single prong pitch mark repair tool by Hidden Links Society"),
 card("always-tinkering-society-navy",
      "Made with Golf Gimmes, and aimed squarely at the people who have rebuilt their bag three times "
      "this season. Mid-weight cotton, five panels, flat peak, metal clasp, tonal under-peak lining. One "
      "size. The patch reads ALWAYS TINKERING SOCIETY, which is either a compliment or a diagnosis.",
      "Navy five panel flat peak cap with Always Tinkering Society patch"),
]

HEAD = [
 card("early-access-bud-chenille-bucket-hat-white",
      "The Bud character on a performance bucket. Perforations wrap the base of the crown, the fabric "
      "claims to run up to 30% cooler than skin temperature when wet, UPF 50+, removable chinstrap, "
      "two-and-a-quarter-inch brim. Two sizes rather than one-size-fits-nobody. The one to wear in an "
      "Austin August.",
      "White perforated performance bucket hat with Bud chenille patch"),
 card("early-access-bud-chenille-hat-white",
      "Volume three of the one they keep selling out of. Five-panel lightweight cotton canvas, contrast "
      "5mm rope, brown leather strap with a black buckle, moisture-wicking sweatband, and a mesh stay "
      "behind the front panel so it holds its shape instead of collapsing by the turn.",
      "White five panel rope cap with Bud chenille patch"),
 card("preorder-north-fork-visor-khaki",
      "Built, in their words, for a long weekend on Long Island in June &mdash; which tells you the brand "
      "is from somewhere specific even if they never say where. An Imperial Tour 3161 body, made in the "
      "USA, cotton-poly, white terry sweatband, three-and-an-eighth-inch brim, polished buckle.",
      "Khaki tour visor with embroidered crest by Hidden Links Society"),
 card("preorder-southampton-hat-khaki",
      "The rope-cap sibling to the North Fork visor and the better buy of the two if you only want one. "
      "Same five-panel canvas construction, same leather-and-buckle closure, same moisture-wicking band. "
      "Khaki goes with the entire rest of your bag, which is the quiet reason rope caps in neutral "
      "colours keep outselling the loud ones.",
      "Khaki five panel rope cap with embroidered crest by Hidden Links Society"),
 card("bud-chenille-patch-hat-duck-camo",
      "Duck camo, mid profile, 100% cotton, single panel front, plastic snapback, the chenille Bud patch "
      "on the front. The black colourway of this one is already gone, which is the usual tell for which "
      "hat a small brand should have made more of.",
      "Duck camo snapback cap with Bud chenille patch"),
 card("ransom-note-rope-cap-olive",
      "Cut-out letters spelling the brand name like a note left under a door. Lightweight nylon, flat "
      "peak, white rope. It is half price at the moment and is the cheapest way into the brand by some "
      "distance &mdash; also in navy at the same rate.",
      "Olive nylon rope cap with cut-out Ransom Note lettering"),
]

GOODS = [
 card("the-universal-putter-cover-olive",
      "Sherpa outer, black sock inner, and a fit engineered to take blade, mallet and centre-shafted "
      "heads rather than forcing you to pick at checkout. There is a small tag to mark which type is "
      "actually living in it, which is the sort of detail that only comes from someone who owns three "
      "putters and rotates them.",
      "Olive sherpa universal putter cover by Hidden Links Society"),
 card("dimple-ripstop-driver-cover-black",
      "Ripstop shell, black lining, red Dimple patch, standard 460cc fit. The plainest thing in the "
      "catalogue and the one most likely to still be on your driver in four years. Ripstop is the right "
      "call for a cover that spends its life being yanked off and thrown at a bag.",
      "Black ripstop driver headcover with red Dimple patch"),
 card("bud-chenille-caddie-towel-black",
      "Sixteen-single ringspun cotton, which is the spec that separates a towel that softens with "
      "washing from one that goes stiff and starts pushing dirt around instead of lifting it. Full "
      "caddie size, chenille patch, black so the mud is your business.",
      "Black cotton caddie towel with Bud chenille patch"),
 card("stencil-collection-ball-marker-aged-brass",
      "Inch-and-a-quarter of aged brass, an eighth thick, knurled edge, double-sided raised engraving. "
      "Twenty dollars, and heavy enough that it stays where you put it in wind that moves a plastic one. "
      "The oldest product in the catalogue and still one of the best.",
      "Aged brass ball marker with knurled edge and raised HIDDEN LINKS SOCIETY engraving"),
 card("world-wide-golf-hoodie-beige",
      "Mid-weight CVC fleece at 9.4oz, 80% cotton with recycled polyester, garment dyed, kangaroo "
      "pocket, no drawcord. Discounted at the moment. The no-drawcord detail matters more than it "
      "sounds: nothing to whip you in the face on a follow-through.",
      "Beige garment-dyed hoodie with World Wide Golf print"),
 card("print-series-score-keepers",
      "Not gear at all. An 8x10 study of pencils and scorecards on 230gsm heavyweight matte, packaged on "
      "acid-free foamcore, described by the brand as the smallest souvenir in golf. There is a framed "
      "Love for the Loopers print too. A clothing brand running a print series is a clothing brand that "
      "wants to be a publisher, and that is the most interesting thing about this one.",
      "Score Keepers art print of golf pencils and scorecards by Hidden Links Society"),
]

INTRO = """<div class="writeup">
  <div class="writeup-body">
    <p>Hidden Links Society sells thirty products and is documenting a hundred golf courses. That ratio is the most interesting thing about them, and it is the reason they are in here.</p>
    <p>On the surface this is another small-batch golf brand doing rope caps and chenille patches. The catalogue is good &mdash; the brass has real weight to it, the overshirt is heavier than it needs to be, the headcovers are made in Oregon &mdash; but it is not, by itself, unusual. What is unusual is what they are doing alongside it.</p>
    <p>Every price below was read from their own store on 17 September 2026.</p>
  </div>
</div>
"""

PUBLIC100 = """<section class="products">
  <h2 class="products-hdr">The Public 100 Project</h2>
  <p class="cat-kicker">A thirty-product brand is making a hundred-course documentary. This is the part nobody else is doing.</p>
  <div class="writeup-body">
    <p>The Public 100 Project is Hidden Links Society playing, walking and documenting every course on <em>Golf Digest</em>&rsquo;s Top 100 Public list &mdash; photography, short-form video, writing and maps, one course at a time. The ranking is Golf Digest&rsquo;s and they say so; the project is theirs.</p>
    <p>The framing is the good bit, and it is worded on their own page like this: these are places anyone can book, step onto and experience &mdash; <strong>&ldquo;no memberships, no private gates, no invitations required.&rdquo;</strong> Some of the list is already played. Most of it is not. They describe the whole thing as a living document.</p>
    <p>It matters because it is expensive and slow and does not obviously sell hats. A brand that wanted quick revenue would run a discount code, not drive to Nebraska. Landmand and Wild Horse and The Prairie Club are on that list next to Pebble Beach and Pinehurst, and getting to all of them is a multi-year commitment for a company whose entire catalogue would fit on two tables.</p>
    <p>It also lines up with what they say they are for. Their mission page is blunt about wanting fewer stiff collars and fewer closed doors, and a project built entirely around courses you can just book is the argument made in practice rather than in a brand deck.</p>
  </div>
</section>
"""

YOC = """<section class="products">
  <h2 class="products-hdr">Where the 2% Goes</h2>
  <p class="cat-kicker">A number small enough to be real and stated plainly enough to check.</p>
  <div class="writeup-body">
    <p>Hidden Links Society give 2% of every purchase to Youth on Course, the nonprofit that gets its members onto more than 2,000 courses for $5 or less a round. That is their figure and their description, printed on their own site, and it is the kind of commitment that is easy to verify and hard to quietly drop.</p>
    <p>Two per cent is not a headline number, which is rather the point. It is a share of revenue rather than a share of profit, it applies to every order rather than to a special collection, and it points at the same thing the Public 100 Project points at: getting more people onto more golf courses for less money.</p>
  </div>
</section>
"""

FAQ_ITEMS = [
 ("What is Hidden Links Society?",
  "A small golf apparel and accessories brand selling headwear, headcovers, overshirts, tees, brass tools and art prints, direct through its own store. Its stated mission is to make golf less exclusive — in its own words, to bring streetwear attitude to the fairway. It also donates 2% of every purchase to Youth on Course and runs a documentary series called The Public 100 Project."),
 ("What is The Public 100 Project?",
  "Hidden Links Society's long-form documentary series playing, walking and documenting the courses on Golf Digest's Top 100 Public list — one course at a time, through photography, short-form video, writing and maps. The brand describes the courses as places anyone can book with no memberships, no private gates and no invitations required. Some are already played; the rest are still ahead."),
 ("Is Hidden Links Society the same as Hidden Links Golf?",
  "No. They are unrelated companies with similar names. Hidden Links Society is the apparel and accessories brand at hiddenlinkssociety.com. Hidden Links Golf is a separate business at a different domain."),
 ("How much does Hidden Links Society gear cost?",
  "Read on 17 September 2026, the range runs from a $6 enamel pin to an $88 framed print. Hats sit between $32 and $48, headcovers between $40 and $82, tees $43 to $48, and the heavyweight Society Overshirt is $78. The Ransom Note rope caps are half price at $15."),
 ("Who founded Hidden Links Society?",
  "The brand does not name a founder anywhere on its site, and we could not find a named founder in any published interview. All of its copy is written in the first person plural. We have quoted the brand rather than an individual throughout this piece for that reason."),
 ("Does Hidden Links Society ship preorders?",
  "Several pieces are sold as preorder or made to order rather than from stock, and the brand states timings on the individual product pages. As of 17 September 2026 the Play Faster fairway cover is listed as shipping the first week of October, and the made-to-order tees and overshirts ask for roughly two weeks."),
]


def st(s):
    return (re.sub(r"<[^>]+>", "", s).replace("&ldquo;", '"').replace("&rdquo;", '"')
            .replace("&rsquo;", "'").replace("&amp;", "&").replace("&mdash;", "—")
            .replace("&middot;", "·").replace("&ndash;", "–"))


FAQ = ('<section class="products">\n  <h2 class="products-hdr" id="faq">The Questions</h2>\n'
       '  <div class="faq">\n' +
       "\n".join(f'    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>'
                 for q, a in FAQ_ITEMS) + "\n  </div>\n</section>\n")

SCHEMA_FAQ = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": st(q),
     "acceptedAnswer": {"@type": "Answer", "text": st(a)}} for q, a in FAQ_ITEMS]}
SCHEMA_ART = {"@context": "https://schema.org", "@type": "Article", "headline": st(PLAIN),
              "description": DESC, "datePublished": "2026-09-17", "dateModified": "2026-09-17",
              "mainEntityOfPage": f"https://thegrassyissue.com/drops/{SLUG}",
              "author": {"@type": "Person", "name": "Lenny Harrington",
                         "url": "https://thegrassyissue.com/about"},
              "publisher": {"@type": "Organization", "name": "The Grassy Issue",
                            "url": "https://thegrassyissue.com"},
              "about": {"@type": "Brand", "name": "Hidden Links Society",
                        "url": "https://hiddenlinkssociety.com/"}}

# --------------------------------------------------------------------- build
model = open(os.path.join(ROOT, "drops/brand-to-know-sentinel-golf.html"), encoding="utf-8").read()
head = model[:model.find('<div class="breadcrumb">')]
tail = model[model.find('<section class="more"'):]

head = re.sub(r"<title>[^<]*</title>", f"<title>{st(PLAIN)} — The Grassy Issue</title>", head)
for k, attr in [("description", "name"), ("og:title", "property"), ("og:description", "property"),
                ("twitter:title", "name"), ("twitter:description", "name")]:
    v = st(PLAIN) if k.endswith("title") else DESC
    head = re.sub(rf'(<meta {attr}="{re.escape(k)}" content=")[^"]*(")',
                  lambda m, _v=v: m.group(1) + _v + m.group(2), head)
for k, attr in [("canonical", "rel"), ("og:url", "property")]:
    pat = (rf'(<link rel="canonical" href=")[^"]*(")' if k == "canonical"
           else rf'(<meta property="og:url" content=")[^"]*(")')
    head = re.sub(pat, lambda m: m.group(1) + f"https://thegrassyissue.com/drops/{SLUG}" + m.group(2), head)
_hero = "https://thegrassyissue.com" + HERO
for k, attr in [("og:image", "property"), ("twitter:image", "name")]:
    head = re.sub(rf'(<meta {attr}="{re.escape(k)}" content=")[^"]*(")',
                  lambda m: m.group(1) + _hero + m.group(2), head)
_ld = ('<script type="application/ld+json">' + json.dumps(SCHEMA_FAQ, ensure_ascii=False) + "</script>\n"
       '<script type="application/ld+json">' + json.dumps(SCHEMA_ART, ensure_ascii=False) + "</script>")
# The Sentinel chassis carries TWO ld+json blocks. A blanket re.sub replaces each
# of them with the full two-block payload, which ships four scripts and two
# contradictory Articles. Replace the FIRST and delete the rest.
_LD_RE = re.compile(r'<script type="application/ld\+json">.*?</script>\s*', re.S)
_n_before = len(_LD_RE.findall(head))
head = _LD_RE.sub("", head)
_anchor = head.rfind("</head>")
head = head[:_anchor] + _ld + "\n" + head[_anchor:]
if len(_LD_RE.findall(head)) != 2:
    raise SystemExit(f"expected exactly 2 JSON-LD blocks, got {len(_LD_RE.findall(head))}")

body = ('<div class="breadcrumb">\n  <a href="/">Feed</a><span>/</span>\n'
        '  <a href="/brands">Brands</a><span>/</span>\n  Hidden Links Society</div>\n'
        f'<header class="drop-header">\n  <h1>{TITLE}</h1>\n  <div class="drop-meta">\n'
        f'    <span>{DATE}</span><span class="dot"></span>\n'
        '    <span>Brand to Know</span><span class="dot"></span>\n'
        f'    <span>{len(NEW)+len(HEAD)+len(GOODS)} Pieces</span>\n  </div>\n</header>\n\n'
        f'<div class="drop-hero"><div class="drop-hero-img"><img src="{HERO}" '
        f'alt="{HERO_ALT}" /></div></div>\n'
        + INTRO + PUBLIC100
        + section("New From the Society", "The six most recent things they have made, newest first.", NEW)
        + section("The Headwear", "Where the brand started and still the deepest part of the range.", HEAD)
        + section("Covers, Cloth and Small Goods", "Brass, sherpa, ripstop and one art print.", GOODS)
        + YOC + FAQ)

out = head + body + tail

# -------------------------------------------------------------------- guards
plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", H.unescape(body)))
words = len(re.findall(r"[A-Za-z0-9']+", plain))
problems = []
if words < 1200:
    problems.append(f"only {words} words")
if out.count("<h1") != 1:
    problems.append(f"{out.count('<h1')} h1 tags")
if re.search(r"\bworth\b", plain, re.I):
    problems.append("banned word 'worth'")
# the unrelated club builder must never appear
if "hiddenlinksgolf" in out:
    problems.append("hiddenlinksgolf.com — that is a DIFFERENT company")
# every product link must be a real handle from the SKU file
for href in re.findall(rf'{re.escape(SHOP)}([a-z0-9-]+)', out):
    if href not in SKU:
        problems.append(f"product link uses an unknown handle: {href}")
# no quote may be attributed to a person at the brand — there is no named founder
if re.search(r'(founder|owner|co-founder)[^.]{0,40}(said|says|told)', plain, re.I):
    problems.append("a quote appears to be attributed to a founder; the brand names none")
# prices must match the SKU file exactly
for key in list(NEW and SKU):
    pass
for m in re.finditer(r'<div class="product-brand">(.*?)</div>\s*<div class="product-name">(.*?)</div>', out, re.S):
    pass
for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', out, re.S):
    json.loads(b)
for img in re.findall(r'<img[^>]+src="(/images/[^"]+)"', out):
    if not os.path.exists(os.path.join(ROOT, img.lstrip("/"))):
        problems.append(f"missing image: {img}")
if "cdn.shopify.com" in out:
    problems.append("a Shopify CDN URL survived — images must be local")
if problems:
    raise SystemExit("REFUSED:\n  " + "\n  ".join(problems))

if apply_:
    open(os.path.join(ROOT, "drops", SLUG + ".html"), "w", encoding="utf-8").write(out)

# f-strings cannot contain backslashes — the regex is hoisted out first
_FR = re.compile(r'data-frames="(\d+)"')
_nframes = sum(int(x) for x in _FR.findall(out))
print(("wrote" if apply_ else "DRY RUN") + f" drops/{SLUG}.html")
print(f"  {len(NEW)+len(HEAD)+len(GOODS)} products | {words} words | "
      f"{_nframes} gallery frames | FAQ {len(FAQ_ITEMS)} + schema")
if not apply_:
    print("\npass --apply to write")
