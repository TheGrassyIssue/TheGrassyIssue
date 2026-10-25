#!/usr/bin/env python3
"""build-lazyface-btk.py — Brand to Know: Lazyface. Cloned from build-parmore-btk.py. 13 October 2026.
Lenny: "Let's do a brand to know post- https://lazyface.com/ fun merch and sunscreen, the texas sun is no joke and something
to be aware of year round", then "all 19".
FACTS: lazyface.com products, home, What's In It, What It's For and FAQ pages (read October 13, 2026); CultureMap Austin
(July 22, 2026: Peoples Rx launch, Austin pop-ups, Atlanta-based, founders); Macon Magazine (August 31, 2026: raised in
Macon, father Dr. David Kent, quotes). Publication names are not printed. Sun facts: American Academy of Dermatology
sunscreen FAQ ("The sun emits harmful UV rays year-round. Even on cloudy days, up to 80%..."); Camp Mabry 29 days a year
at 100F+ is the LCRA/NWS figure already cited in the Field Guide season planner.
PHOTOS: Lazyface's own, shot on a green sweep, plus its lifestyle shots. The Ball Cap's images are only 620px.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Lazyface: Mineral Sunscreen and Fun Golf Merch for the Texas Sun"
DESC = ("Brand to Know: Lazyface, the dermatologist-developed mineral sunscreen that opened its first store in Austin, "
        "plus a Tremont-made golf capsule, hats and tees. All 19 pieces, $10 to $118.")
H1 = "Brand to Know: Lazyface &mdash; Don&rsquo;t Be Stupid. Be Lazy."
BC = "Lazyface"
SLUG = "brand-to-know-lazyface"
IMG = "/images/lazyface"
SHOP = "https://lazyface.com/products/"
A = "Lazyface"
P = {
 # Sunscreen
 "facescreen": (A, "Facescreen, SPF 30", "$35", "facescreen",
   "The reason to know the brand. A broad-spectrum mineral sunscreen built on non-nano zinc oxide that goes on clear, with niacinamide, carrot root extract and vitamin E in the mix. It is fragrance-free, water resistant for 80 minutes and made in the USA. One squeeze before the first tee is the whole routine, which is the point."),
 "facestick": (A, "Facestick, SPF 30", "$25", "facestick",
   "The same mineral SPF 30 in a stick that lives in the bag. It glides on without a streak, so the reapply at the turn takes ten seconds and no wet hands. Lazyface&rsquo;s own advice is to reapply every two hours, and this is the version that makes that likely."),
 "the-face-set": (A, "The Face Set", "$54", "the-face-set",
   "The set puts Facescreen for the morning and Facestick for the bag in one box, for $54 instead of $60. The brand says Dr. Steven Kent spent three years on the formula to get a mineral sunscreen that goes on clear, and this is the easiest way to own both versions of it."),
 # Golf capsule
 "the-wood-cover": (A, "The Wood Cover", "$118", "the-wood-cover",
   "The best thing in the store that is not sunscreen. Made with Tremont Sporting Co., it is pebbled leather in dark green with a white LF and a yellow stripe band, and it fits every wood including the driver. It looks like a vintage clubhouse cover with a sense of humor."),
 "the-mallet-cover": (A, "The Mallet Cover", "$108", "the-mallet-cover",
   "Lazyface figures a properly lazy golfer would pick a mallet, since blades punish mishits more, so the capsule has a mallet cover and no blade. It is a dark green cover with the yellow sun embroidered on top, made with Tremont Sporting Co."),
 "the-golf-towel": (A, "The Golf Towel", "$48", "the-golf-towel",
   "This reversible towel comes in cream and navy, with a checkerboard border and the LF monogram. It hangs off the bag next to the Facestick, which is the right pairing. It is part of the Tremont Sporting Co. capsule."),
 "the-chenille-sun-cap": (A, "The Chenille Sun Cap", "$48", "the-chenille-sun-cap",
   "This green cap wears the brand&rsquo;s sun in fuzzy chenille on the front and breathes well enough for an August round. The chenille is the detail that makes it look like old pro shop merch. Made with Tremont Sporting Co."),
 "the-pennant-1": (A, "The Pennant", "$48", "the-pennant-1",
   "Classic felt with stitched edges, green with Lazyface in yellow script, built like a pennant from a college dorm in 1975. It does nothing on the course and looks great over a garage putting mat."),
 # Hats
 "the-bucket": (A, "The Bucket", "$60", "the-bucket",
   "The most useful hat here for Texas: a cream cotton bucket rated UPF 50+, with a brim all the way around so the back of the neck is covered too. Lazyface pitches it at the lazy river; we would wear it for a summer muni round."),
 "the-river-cap": (A, "The River Cap", "$50", "the-river-cap",
   "This mid-profile snapback is green quick-dry nylon, light enough to forget about. The LF on the front is small and white. It suits a wet morning round or the drive to the lake after."),
 "the-captain-cap": (A, "The Captain Cap", "$45", "the-captain-cap",
   "The Captain is an eggshell quick-dry nylon cap with a rope across a flat brim and a small Lazyface patch. It has weekend boater energy, which also works on a Sunday nine."),
 "the-two-tone-cap": (A, "The Two-Tone Cap", "$35", "the-two-tone-cap",
   "This one has a cream crown, a dark green brim and an LF on the front. It is the plainest cap in the store and the easiest one to wear with anything."),
 "the-sun-cap": (A, "The Sun Cap", "$35", "the-sun-cap",
   "This dark green corduroy cap carries the yellow sun on the front, and the brand pitches it at subtropical winters. It is the cap for a 60-degree January morning at Lions."),
 "the-ball-cap": (A, "The Ball Cap", "$35", "the-ball-cap",
   "A cream cotton cap with a green LF, built to keep the sun out of your eyes for whatever ball you play. The simplest piece here, and it matches the bucket."),
 # Tees and koozie
 "the-frank-tee": (A, "The Frank Tee", "$45", "the-frank-tee",
   "Frank is a frog, lounging on the back of a brushed cotton tee under &ldquo;Stay lazy.&rdquo; The small Lazyface script on the chest keeps the front quiet. Our favorite piece of merch in the store."),
 "the-long-sleeve-tee": (A, "The Long Sleeve Tee", "$40", "the-long-sleeve-tee",
   "This cream long sleeve has a big green LF on the back and checkered stripes running down both arms. The brand&rsquo;s pitch is honest: on days you cannot be bothered to put sunscreen on your forearms, wear this."),
 "the-sun-tee": (A, "The Sun Tee", "$35", "the-sun-tee",
   "A big yellow sun fills the back of this cream tee in 100% ring-spun US cotton, with a small logo on the chest. It is simple, bright and very Texas in July."),
 "the-pocket-tee": (A, "The Pocket Tee", "$35", "the-pocket-tee",
   "This washed green pocket tee has a small LF on the pocket and Lazyface across the back. The brand calls the LF a nod to designers too lazy to set a whole wordmark."),
 "the-koozie": (A, "The Koozie", "$10", "the-koozie",
   "Green, with &ldquo;Stay lazy.&rdquo; on one side and the logo on the other, because cans need sun protection too. The cheapest way into the brand, and the most likely to come home from the course in your bag."),
}
SECTIONS = [
 ("The Sunscreen", "sunscreen", ["facescreen", "facestick", "the-face-set"],
  "<strong>Three picks &middot; $25&ndash;$54</strong>Dermatologist-developed mineral SPF 30 that goes on clear and lasts through a round. This is the product; everything else is merch."),
 ("The Golf Capsule", "golf", ["the-wood-cover", "the-mallet-cover", "the-golf-towel", "the-chenille-sun-cap", "the-pennant-1"],
  "<strong>Five picks &middot; $48&ndash;$118</strong>A small collection made with Tremont Sporting Co., the custom golf shop in Palm Beach: leather covers, a towel, a chenille cap and a pennant."),
 ("Hats for the Texas Sun", "hats", ["the-bucket", "the-river-cap", "the-captain-cap", "the-two-tone-cap", "the-sun-cap", "the-ball-cap"],
  "<strong>Six picks &middot; $35&ndash;$60</strong>A hat is the second-laziest sun protection there is. The bucket is the one for August."),
 ("Tees and a Koozie", "tees", ["the-frank-tee", "the-long-sleeve-tee", "the-sun-tee", "the-pocket-tee", "the-koozie"],
  "<strong>Five picks &middot; $10&ndash;$45</strong>The tees carry a frog, a sun and an LF, and the koozie rides in the cart."),
]
N = 19
PQ = {
 "sunscreen": ("We created Lazyface for people who don&rsquo;t think of themselves as skin people but still want an easy way to protect and take care of their skin.", "Stuart Kent, Lazyface co-founder"),
 "golf": ("Because of our dad, Stuart and I definitely had sun protection implemented at a very young age.", "Dr. Steven Kent, Lazyface co-founder"),
}
CAP = ""
BANDS = {}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Lazyface makes the sunscreen golfers will actually wear, because it asks for one step and nothing else. It is a mineral SPF 30 from a dermatologist who treats skin cancer, it goes on clear instead of ghost-white, and it lasts through a round. Then, because the brand has a sense of humor, there is a whole store of merch around it: a frog tee, a UPF bucket hat and a leather golf capsule made with Tremont Sporting Co.</p>
    <h2 class="products-hdr btk-story-hdr">The Texas Sun Is Not a Summer Problem</h2>
    <p>Golf in Austin means four hours in the open, on fairways with very little shade. Summer gets the attention, and fairly: Camp Mabry averages 29 days a year at 100 degrees or more. But the American Academy of Dermatology is clear that the sun puts out harmful UV rays year-round, and that up to 80% of them get through on a cloudy day. The January round at Lions in a quarter-zip still counts. So does the overcast Saturday in March. Sunscreen on your face before the first tee, every round, is the cheapest habit in golf.</p>
    <h2 class="products-hdr btk-story-hdr">The Brand</h2>
    <p>Lazyface was started by two brothers who grew up in Macon, Georgia: Stuart Kent, an entrepreneur, and Dr. Steven Kent, a dermatologist trained in Mohs skin cancer surgery. Their father is a Mohs surgeon too. The brand says Steven kept getting the same question from patients, what could they have done to prevent it, and the answer was nearly always sunscreen. So the brothers built one for men who skip skincare: one product, no white cast, priced like the drugstore. The brand is based in Atlanta, but it chose Austin for its first store, at Peoples Rx, in July 2026, after pop-ups with RAW Running Club and Austin Rowing Club. All 19 pieces below were in stock on lazyface.com on October 13, 2026.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Atlanta, Georgia</span></div>
      <div class="sidebar-detail"><span class="l">Founders</span><span>Stuart &amp; Dr. Steven Kent</span></div>
      <div class="sidebar-detail"><span class="l">Known for</span><span>Mineral SPF 30</span></div>
      <div class="sidebar-detail"><span class="l">In Austin</span><span>Peoples Rx</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$10&ndash;$118</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Facescreen, $35</span></div>
      <a href="https://lazyface.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit Lazyface &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#Lazyface</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#SunscreenEveryRound</span>
        <span class="hashtag">#AustinGolf</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("Who makes Lazyface sunscreen?", "Brothers Stuart Kent and Dr. Steven Kent, a dermatologist trained in Mohs skin cancer surgery. The brand is based in Atlanta and the brothers grew up in Macon, Georgia."),
 ("Where can I buy Lazyface in Austin?", "Peoples Rx, the Austin pharmacy and wellness store, became Lazyface's first brick-and-mortar retailer in July 2026. It also sells online at lazyface.com."),
 ("Is Lazyface mineral sunscreen?", "Yes. Facescreen and Facestick are broad-spectrum SPF 30 sunscreens built on non-nano zinc oxide. The brand says both go on clear, are fragrance-free and paraben-free, contain no oxybenzone or octinoxate, and are made in the USA."),
 ("How often should I reapply sunscreen on the golf course?", "Lazyface rates its sunscreens water resistant for 80 minutes and recommends reapplying every two hours, or after sweating, swimming or toweling off. On a four-hour round that means at least once, usually at the turn."),
 ("Do I need sunscreen for golf in winter in Texas?", "Yes. The American Academy of Dermatology says the sun emits harmful UV rays year-round and that up to 80% of them can get through clouds, so sunscreen applies on cool and overcast days too."),
 ("How much does Lazyface cost?", "On October 13, 2026: Facestick $25, Facescreen $35, the Face Set $54, caps $35 to $50, the bucket hat $60, tees $35 to $45, and the Tremont golf capsule $48 to $118."),
]
FRN = json.loads((ROOT / "research/lazyface/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-LF-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
    og = f"https://thegrassyissue.com{IMG}/btk-og.jpg"
    items, pos = [], 1
    for sec in SECTIONS:
        for h in sec[2]:
            items.append({"@type": "ListItem", "position": pos, "url": SHOP + P[h][3], "name": H.unescape(f"{P[h][0]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-10-13", "dateModified": "2026-10-13",
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
<link rel="preload" as="image" href="{IMG}/btk-hero.jpg" />
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


def section(sec, n0):
    h2, anchor, ids, kicker = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} {"pick" if len(ids)==1 else "picks"}</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def main(apply_):
    ids = [k for s in SECTIONS for k in s[2]]
    assert len(ids) == N == len(set(ids)) and set(ids) == set(P), (len(ids), set(P) ^ set(ids))
    for k in ids:
        assert FRN[k] and all((ROOT / f.lstrip("/")).is_file() for f in FRN[k]), k
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<!-- TGI-ONE-FOOTER -->'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Mineral sunscreen and golf merch &middot; Atlanta</span><span class="dot"></span>
    <span>19 picks &middot; all in stock, checked October 13, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/btk-hero.jpg" alt="Overhead shot of a person in a yellow tee and straw hat lying on a green and white striped towel on grass, holding a tube of Lazyface Facescreen SPF 30" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
    body += faq_html()
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Kalamunda", "Howie", "No Dirt", "Lehi", "Rookline", "Bethpage", "Hudson", "LBB", "GolfPass", "Woodgrain", "Parmore"):
        if leak in above: bad.append("leak " + leak)
    if fin.count('class="product-card"') != N: bad.append("card count")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", above), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
