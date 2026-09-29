#!/usr/bin/env python3
"""build-no-return-club-btk.py — Brand to Know: No Return Club (Manchester).
29 September 2026. Lenny: "we need to do a brand to know- noreturnclub.co.uk/collections/pro-shop",
"let's do a section on the sold out headcovers, those are worth keeping an eye out for",
and on the Take: "the ethos of NRC is all about that Hero shot, driving the green, hacking a
hybrid from the weeds, going for broke always." Approved: "yes".

FACTS: research/noreturn/notes.md. No named founder (the sole Companies House director is not
publicly tied to the brand, so he is not named). The NR / no-return reading of the name is
presented as ours. Quotes are the brand's own unsigned copy, attributed to the brand.
PRICES: GBP from noreturnclub.co.uk, read 29 Sep 2026, with approximate USD at 1.3230
(GBP/USD close, 29 Sep 2026) per Lenny's standing preference for dollar conversions.
PHOTOS: the brand's own site and product galleries.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "brand-to-know-no-return-club"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/no-return-club"
FR = json.loads((ROOT / "research/noreturn/frames.json").read_text())
BJ = json.loads((ROOT / "research/noreturn/bands.json").read_text())
SHOP = "https://noreturnclub.co.uk/products/"
BRAND = "No Return Club"
FX = 1.3230

def gbp(p):
    v = float(p)
    return f"&pound;{v:.2f} (~${round(v * FX):,})"

TITLE = "No Return Club: The Manchester Golf Brand for the Hero Shot"
DESC = ("No Return Club is a Manchester golf brand built on going for broke: skull ball markers, "
        "handmade Harris Tweed headcovers and Play Golf Recklessly. Our 12 picks.")
H1 = "Brand to Know: No Return Club &mdash; Golf for the Hero Shot"

SOLD = set()
def sold(h):
    return " &middot; Sold out" if h in SOLD else ""

P = {
 "nr-ripstop-5-panel-golf-cap": ("NR Ripstop 5 Panel Cap", "Black", "24.99",
   "This is lightweight nylon ripstop with block NR lettering on the front and script on the side. If you buy one thing, buy this, and wear it on the tee you should be laying up from."),
 "golfcap-five-panel": ("Fairway Runner Cap", "Five-panel, marked down from &pound;25", "19.99",
   "It is a low-profile, one-size cap in water-resistant performance fabric that takes its cues from running. The brand calls it &ldquo;our most N.R.C product to date.&rdquo;"),
 "wind-shirt-purple-haze": ("Wind Shirt", "Purple Haze", "74.99",
   "This is a waterproof nylon three-quarter zip with a mesh lining, built, in the brand&rsquo;s words, for when the forecast &ldquo;can&rsquo;t make its mind up (pretty much everyday in the UK).&rdquo; It is the jacket in every photograph on the site."),
 "golf-t-shirt": ("GOLF Tee", "Bone", "29.99",
   "It is a loose, vintage-washed 230gsm cotton tee with GOLF spelled out in mismatched collegiate letters. The product copy calls golf &ldquo;everyones favourite four-letter word.&rdquo;"),
 "pitchmark-repair-tool": ("Pitchmark Repair Tool", "New &middot; September", "44.99",
   "This is CNC-milled from 303 stainless steel and flame-treated, so every one comes out a different colour. It is the most serious object the brand makes, and it came out this month."),
 "ball-marker-brass-skull": ("Skull Ball Marker", "Collectors Edition", "25.99",
   "It is solid brass with a patina finish, shaped like the brand&rsquo;s skull, made with SinkGolf to mark two years. Only 50 were made."),
 "russian-roulette-ball-marker-hot-pink": ("Russian Roulette Ball Marker", "Hot Pink", "12.99",
   "This is a blacked-out marker shaped like a revolver cylinder, with one chamber in hot pink. The copy says: &ldquo;Spin that chamber. Sink the Putt!&rdquo;"),
 "blue-tip-golf-tees-limited-edition": ("Bamboo Tees", "Blue tip, limited", "15.99",
   "These are 70mm bamboo tees with a coloured tip at the right height, in a limited blue."),
 "bamboo-golf-tees-green": ("Bamboo Tees", "Green tip", "15.99",
   "It is the same 70mm bamboo tee with a green tip, in the brand&rsquo;s standard run."),
 "hickory-golf-club-brush": ("Hickory Groove Brush", "Monochrome black", "24.99",
   "This is a hickory-handled brush with extra-stiff nylon bristles, a speckled lanyard and a carabiner."),
 "golf-towel": ("XL Cotton Towel", "M.O.I, marked down from &pound;34.99", "24.99",
   "It is an extra-large cotton towel in green and black with a carabiner. The graphic is meant to show the impact of a golf ball."),
 "pin-badge-set-limited-edition": ("Pin Badge Set", "Limited", "9.99",
   "It has three enamel pins, Nice Slice, 0 Shots Left and Hello, I Am A Golf Addict. The copy: &ldquo;Genuine NRC Pins. Questionable golfing habits.&rdquo;"),
 # sold out headcovers
 "harris-tweed-mono-weave-headcover": ("Harris Tweed Mono Weave", "Summer 2026", "59.99",
   "It pairs two black-and-white Harris Tweeds with serif embroidery and a boiled black wool lining. It is the one we would buy first."),
 "harris-tweed-purple-haze-twist-headcover": ("Harris Tweed Purple Haze Twist", "Summer 2026", "59.99",
   "It is two purple Harris Tweeds on the diagonal, made to match the Wind Shirt."),
 "harris-tweed-speckled-magpie-headcover": ("Harris Tweed Speckled Magpie", "Summer 2026", "59.99",
   "This is a speckled black tweed with a white panel and serif embroidery."),
 "harris-tweed-loblolly-pine-green-headcover": ("Harris Tweed Loblolly Pine", "Augusta series", "54.99",
   "It is a multi-tone green tweed named after the loblolly pines at Augusta National."),
 "harris-tweed-blooming-azaleas-headcover": ("Harris Tweed Blooming Azaleas", "Augusta series", "54.99",
   "It is a hot pink split tweed with a boiled pink wool lining, named after Augusta&rsquo;s azaleas."),
 "pimento-tweed-headcover": ("Harris Tweed Pimento", "Augusta series", "54.99",
   "This is green over yellow, inspired, as the brand puts it, by &ldquo;Augustas legendary pimento cheese sandwich.&rdquo;"),
 "golf-headcover-blue": ("Birdseye Blue", "Knit", "44.99",
   "It is a blue birdseye knit over black, with a polar fleece lining."),
 "golf-headcovers-houndstooth": ("Houndstooth Red + Oyster", "Knit", "44.99",
   "This is an oversized red and oyster houndstooth. It is the loudest cover in the archive."),
 "golf-headcovers-fleece": ("Typo Fleece", "Fleece", "44.99",
   "It is brushed fleece in a blue-to-white gradient with pink lettering."),
 "usa-headcover-driver": ("USA Driver Cover", "Ryder Cup", "49.99",
   "It was made by hand in Manchester for the Ryder Cup, in red with USA across it."),
 "euro-headcover-driver": ("Euro Driver Cover", "Ryder Cup", "49.99",
   "This is the European side: white leather, a blue gothic B and a numbered blue version."),
 "portrush-driver-headcover": ("Portrush Driver Cover", "PU leather", "39.99",
   "It is black and cream leather made to look like a pint of Irish stout, for the Open at Portrush."),
}

S = json.loads((ROOT / "research/noreturn/sections.json").read_text())
SOLD = set(S["sold"])
SECTIONS = [
    ("wear", "Caps, Tees and the Wind Shirt", "the-clothes",
     ["nr-ripstop-5-panel-golf-cap", "golfcap-five-panel", "wind-shirt-purple-haze", "golf-t-shirt"],
     "<strong>Four pieces &middot; &pound;19.99&ndash;&pound;74.99</strong>These are the caps, the tee and the purple jacket from the campaign."),
    ("bag", "On the Bag", "on-the-bag",
     ["pitchmark-repair-tool", "ball-marker-brass-skull", "russian-roulette-ball-marker-hot-pink", "blue-tip-golf-tees-limited-edition",
      "bamboo-golf-tees-green", "hickory-golf-club-brush", "golf-towel", "pin-badge-set-limited-edition"],
     "<strong>Eight pieces &middot; &pound;9.99&ndash;&pound;44.99</strong>Most of the small things are limited runs."),
    ("sold", "Keep an Eye Out: The Sold-Out Headcovers", "sold-out-headcovers",
     S["sold"],
     "<strong>Twelve covers &middot; all sold out</strong>These are the thing to own. They are handmade in small drops and gone quickly, so join the mailing list and watch for the next one."),
]

PQ = {
    "about": ("Driven by a desire to infuse Golf with modern &amp; rebellious design aesthetics, No Return Club brings together a respect for golf styles of the past with the modern-day fashion twist.",
              "No Return Club, on its About page"),
    "reckless": ("A design with an understated nod to those who take the game less seriously and the style more so.",
                 "No Return Club, on the Play Golf Recklessly hoodie"),
    "mass": ("These items will not be mass produced, we want to continue to innovate our product line with new designs &amp; materials.",
             "No Return Club, on its handmade line, The Bunker"),
}

def _band(key, kick, line, caps):
    return (kick, line, [(x["local"].split("/")[-1][:-4], H.escape("No Return Club photograph: " + x["title"].replace("page:", "")), c) for x, c in zip(BJ[key], caps)])

BANDS = {
    "outdoors": _band("outdoors", "Photography &middot; No Return Club", "These are the brand&rsquo;s own photographs: the tee, the Wind Shirt and a pouch in the grass.",
                      ["The tee", "The Wind Shirt", "The pouch"]),
    "campaign": _band("campaign", "Photography &middot; the Purple Haze shoot", "The Wind Shirt campaign was shot against purple, with the bag and a bucket of balls.",
                      ["Wind Shirt and bag", "Wind Shirt", "NR Ripstop cap"]),
    "covers": _band("covers", "Photography &middot; the headcovers", "The headcovers were shot on a real bag against a concrete wall.",
                    ["Pimento", "Typo Fleece", "Houndstooth"]),
}

PROSE = 'style="max-width:760px;font-size:16px;line-height:1.7;margin:0 auto 24px;"'

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>No Return Club is golf for the hero shot. It means driving the par 4 when the smart play is a 5-iron, hacking a hybrid out of the weeds instead of chipping out sideways, and taking on the flag over water with the round already on the line. You go for broke, every time. If it doesn&rsquo;t come off, you pick up and write NR on the card: no return. We think that is where the name comes from, and it is the whole brand.</p>
    <p>The Manchester label wears it on everything. There is a skull on the logo, a ball marker shaped like a revolver cylinder called Russian Roulette, a pin set promising &ldquo;Questionable golfing habits,&rdquo; and a hoodie that just says Play Golf Recklessly. The swagger comes with real craft, too. The headcovers are Harris Tweed, cut and sewn by hand in Manchester and lined in boiled wool, and the new pitchmark tool is CNC-milled stainless steel, flame-treated so no two come out the same colour. It is the kit of someone who plays badly on purpose and looks good doing it.</p>
    <p>Buy the NR Ripstop cap at &pound;24.99 (about $33), and get on the mailing list for the headcovers, which are the thing to own and are all sold out right now. Prices were read from the brand&rsquo;s store on 29 September 2026, with dollars at that day&rsquo;s rate.</p>
    <h2 class="products-hdr btk-story-hdr">The Story</h2>
    <p>No Return Club is a small independent company from Greater Manchester, registered in March 2024, and its current shop opened in May 2025. It does not put a founder&rsquo;s name on anything, and it has no press, stockists or sponsors: just a shop, an Instagram following of around 6,800, and a run of drops that sell out.</p>
    <p>The range is mostly things for the bag. It includes bamboo tees, machined ball markers, hickory brushes, pouches and headcovers, plus a few caps and tees. The handmade pieces sit in a line called The Bunker, released in small batches every few months, and the covers have followed the golf calendar, with an Augusta set in spring, Ryder Cup covers for each side, and a stout-inspired cover for the Open at Portrush.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Manchester, England</span></div>
      <div class="sidebar-detail"><span class="l">Since</span><span>2024</span></div>
      <div class="sidebar-detail"><span class="l">Made</span><span>Headcovers and pouches by hand in Manchester</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>&pound;9.99&ndash;&pound;74.99</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>NR Ripstop cap, &pound;24.99 (~$33)</span></div>
      <div class="sidebar-detail"><span class="l">Watch for</span><span>The next headcover drop</span></div>
      <a href="https://noreturnclub.co.uk/collections/pro-shop" target="_blank" rel="noopener" class="sidebar-cta">Visit the Pro Shop &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#NoReturnClub</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#PlayGolfRecklessly</span>
        <span class="hashtag">#HarrisTweed</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

FAQ = [
    ("What is No Return Club?",
     "No Return Club is an independent golf brand from Manchester, England, founded in 2024. It makes golf accessories, headcovers and a small range of clothing, with a rebellious, go-for-broke attitude and handmade Harris Tweed covers."),
    ("What does No Return Club mean?",
     "The brand does not explain it, but NR is golf shorthand for no return: a scorecard not handed in, or a hole where you picked up. It fits the brand's Play Golf Recklessly attitude."),
    ("Are No Return Club headcovers handmade?",
     "Yes. The brand says its Harris Tweed headcovers, pouches and alignment stick covers are handmade in Manchester. The Harris Tweed covers are lined in boiled wool."),
    ("Why are No Return Club headcovers sold out?",
     "They are made by hand in small, limited drops. The brand says its handmade line will not be mass produced, so each run sells out and new designs follow. Joining the mailing list is the way to hear about the next drop."),
    ("Does No Return Club ship to the US?",
     "Yes. The shop ships from the UK to the US, the EU and other countries. Prices are in pounds."),
]


def pq(key):
    txt, attr = PQ[key]
    return (f'\n<!-- TGI-NRC-PQ-{key} -->\n<div class="pull-quote">\n  <div class="pull-quote-inner">'
            f'&ldquo;{txt}&rdquo;<span class="pull-quote-attr">&mdash; {attr}</span></div>\n</div>\n'
            f'<!-- /TGI-NRC-PQ-{key} -->\n')

def band(key):
    kick, line, items = BANDS[key]
    figs = "\n".join(f'  <figure><img src="{IMG}/{f}.jpg" alt="{alt}" loading="lazy" /><figcaption class="ig-cap">{cap}</figcaption></figure>'
                     for f, alt, cap in items)
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <p class="cat-kicker"><strong>{kick}</strong>{line}</p>\n'
            f'  <div class="ig-grid">\n{figs}\n</div>\n</section>\n')


def card(h, idx):
    name, detail, price, copy = P[h]
    fr = [f["local"] for f in FR[h]]
    label = H.unescape(f"No Return Club {name} {detail}").replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>'
                   for j, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if j == 0 else ""}" data-i="{j}" aria-label="View image {j+1}"></button>'
                   for j in range(len(fr)))
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery">'
            f'<div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{BRAND} &middot; {detail}</div>'
            f'<div class="product-name">{name} &middot; {gbp(price)}{sold(h)}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="{SHOP}{h}" target="_blank" rel="noopener" class="product-link">{"See the listing" if h in SOLD else "Shop"} &#8599;</a></div></div>')


def section(sec, n0):
    key, h2, anchor, ids, kicker = sec
    cards = "\n".join(card(h, n0 + j) for j, h in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} {"Piece" if len(ids) == 1 else "Pieces"}</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>'
                     for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items, pos = [], 1
    for _, _, _, ids, _ in SECTIONS:
        for h in ids:
            items.append({"@type": "ListItem", "position": pos, "url": SHOP + h, "name": H.unescape(f"No Return Club {P[h][0]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-09-29", "dateModified": "2026-09-29",
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
            {"@type": "ListItem", "position": 3, "name": "No Return Club", "item": URL}]},
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
    ids = [h for s in SECTIONS for h in s[3]]
    assert len(ids) == 24 == len(set(ids)) and set(ids) == set(P), set(P) ^ set(ids)
    for h in ids:
        assert FR.get(h), h
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  No Return Club</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Manchester, England &middot; since 2024</span><span class="dot"></span>
    <span>12 picks &middot; 12 sold-out headcovers</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A golfer in an NR cap and purple No Return Club Wind Shirt addressing a ball in long grass beneath a concrete structure" fetchpriority="high" /></div></div>
"""
    body += TAKE + band("outdoors") + pq("about")
    n = 1
    s, n = section(SECTIONS[0], n); body += s + band("campaign") + pq("reckless")
    s, n = section(SECTIONS[1], n); body += s + band("covers") + pq("mass")
    s, n = section(SECTIONS[2], n); body += s
    body += faq_html()
    out = head_top() + head_rest + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    bad = []
    for leak in ("Manors Revisited", "Nicklaus", "St. Andr", "Abbott"):
        if leak in above: bad.append("leak " + leak)
    if fin.count('class="product-card"') != 24: bad.append("card count")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", above), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
