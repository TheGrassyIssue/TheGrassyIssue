#!/usr/bin/env python3
"""build-st-andre-btk.py — Brand to Know: St. André Golf.
28 September 2026.

Lenny: "Let's do a brand to know https://standre.golf/", then "looks good" to
the 40-option grid with my starred 12.

FACTS: research/st-andre/notes.md. An Atlanta golf sketch-comedy group first,
merch second. Aaron Chewning founded it (Bridgestone says "co-founder"; no
other founder is named anywhere, so the page says "founded by" only). Where
the gear is made is not stated, and the page says so.

QUOTES: verbatim, as read on the page: On The Green Magazine (5 Sep 2025) and
the Atlanta Journal-Constitution (9 Apr 2025). Short product-copy lines are
quoted from standre.golf product pages.

PHOTOS: the brand's own (homepage banners, product pages). No press photos.
IRL frames lead every card that has one. Sources in research/st-andre/frames.json.

Prices and stock read 28 Sep 2026, USD. No feed card; that waits for Lenny.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "brand-to-know-st-andre"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/st-andre"
FR = json.loads((ROOT / "research/st-andre/frames.json").read_text())
SHOP = "https://standre.golf/products/"
BRAND = "St. Andr&eacute;"
BRAND_T = "St. André"

TITLE = "Brand to Know: St. André Golf, the Atlanta Comedy Troupe With a Pro Shop"
DESC = ("St. André Golf is an Atlanta golf sketch-comedy group with a sharp merch line. Who is behind it, "
        "why it looks the way it does, and twelve picks from $10 to $50.")
H1 = "Brand to Know: St. Andr&eacute; Golf &mdash; The Comedy Troupe With a Pro Shop"

# handle -> (name, detail, price-string, copy)
P = {
 "patch-performance-hat-white-black": ("Patch Performance Hat", "Made by Pukka", "35",
   "Pukka makes this one: a lightweight performance-poly cap with a semi-structured front, a Velcro back and a woven St. Andr&eacute; patch. It comes in four colourways, and the product copy says one size fits most, &ldquo;looking at you Jeff!&rdquo;"),
 "puff-mid-crown-cotton-hat": ("Puff Mid Crown Cotton Hat", "Two-tone", "35",
   "This is a cotton snapback with a cream crown, a green, black or navy brim, and the script wordmark in raised 3D embroidery. The product copy sums it up: &ldquo;Two tones, FTW!&rdquo;"),
 "wordmark-trucker-hat": ("Wordmark Trucker Hat", "Royal blue", "35",
   "This is the classic foam-front trucker in royal blue, with a recycled mesh back, a snapback and a mid-to-high crown. The white script wordmark does all the work."),
 "st-andre-classic-driver-cover": ("Classic Driver Cover", "Green check", "35",
   "This is the piece that sums up the brand. It has green faux leather with checkered embroidery all over, a yellow script A, the Classic logo and a plush green lining. It looks like an old country-club cover, from a group that plays public courses off the blue tees."),
 "st-andre-classic-blade-putter-cover": ("Classic Blade Putter Cover", "Green check", "28",
   "This is the blade version of the same cover, in the same green check and yellow script, with the St. Andr&eacute; wordmark along the side and the same green lining."),
 "st-andre-classic-ball-marker": ("Classic Ball Marker", "Two-sided", "10",
   "This is a two-sided marker in zinc alloy with hard enamel fill, and a magnetic well that holds a detachable iron insert. It carries a green-and-white checkered ring around the yellow A, to match the covers."),
 "pspsps-jacquard-towel": ("Pspsps Jacquard Towel", "New &middot; 9 September", "45",
   "This is the newest thing in the shop. It is a 550gsm cotton jacquard caddie towel, 16 by 38 inches, in cream and royal blue, with cats batting golf balls around a hole. The product copy opens: &ldquo;Look what the cat dragged in!&rdquo;"),
 "palm-x-st-andre-glove": ("Palm X St. Andr&eacute; Glove", "With Palm Golf", "20",
   "It is a collaboration with Palm Golf: thin AAA Cabretta leather, a reinforced wrist and a checkered St. Andr&eacute; patch on the tab. It is USGA conforming, and it is the least expensive way into the brand after the marker."),
 "classy-lettermark-socks": ("Classy Lettermark Socks", "Undyed", "12.50",
   "These land just below the calf, with orange stripes and the lettermark. They are left undyed, so the white has a slight natural eggshell colour."),
 "meow-tee": ("Meow Tee", "New for 2026", "35",
   "This is 5.5oz ring-spun cotton, given an extra wash so it feels worn in. A cat stretches across the back under the ANDR&Eacute; wordmark, and a small script A sits on the chest. It comes in black and blue."),
 "mermaid-tee": ("Mermaid Tee", "New for 2026", "35",
   "This one puts a mermaid on the St. Andr&eacute; Golf wordmark across the back, in blue on white or white on blue. It has the same relaxed fit and washed cotton as the Meow."),
 "launched-crewneck-sweatshirt": ("Launched Crewneck", "Sage", "50",
   "This is a 9oz garment-washed crew in 80/20 cotton and polyester, with the ANDR&Eacute; wordmark and a golf ball launching off it. Three of the five sizes were left when we checked."),
}

SECTIONS = [
    ("hats", "The Hats", "the-hats",
     ["patch-performance-hat-white-black", "puff-mid-crown-cotton-hat", "wordmark-trucker-hat"],
     "<strong>Three hats &middot; $35 each</strong>The 2026 hats: a Pukka performance cap, a two-tone puff-print snapback and a royal-blue trucker."),
    ("course", "On the Course", "on-the-course",
     ["st-andre-classic-driver-cover", "st-andre-classic-blade-putter-cover", "st-andre-classic-ball-marker",
      "pspsps-jacquard-towel", "palm-x-st-andre-glove", "classy-lettermark-socks"],
     "<strong>Six pieces &middot; $10&ndash;$45</strong>The Classic covers and marker in green check, the new cat towel, the Palm glove and a pair of undyed socks."),
    ("tees", "Tees &amp; Crew", "tees-and-crew",
     ["meow-tee", "mermaid-tee", "launched-crewneck-sweatshirt"],
     "<strong>Three pieces &middot; $35&ndash;$50</strong>Two of this summer&rsquo;s new tees and the Launched crew, all washed so they feel worn in."),
]

PQ = {
    "classy": ("We wanted it to look classy on a shirt or merch if we wanted to do that. We wanted it to sound like a golf brand, such as a nod to classic golf.",
               "Aaron Chewning, founder, to On The Green Magazine, September 2025"),
    "funny": ("Historically, the game of golf has been uptight and intense. The pros have to be so locked in while they&rsquo;re playing. They may throw out a fist pump, but the game is known for being quiet, solo and demanding. But it can also be really funny, as can most anything.",
              "Aaron Chewning to the Atlanta Journal-Constitution, April 2025"),
    "living": ("I get to joke around on a golf course with my best friends for a living. We get paid to make people laugh. It doesn&rsquo;t get much better.",
               "Aaron Chewning to the Atlanta Journal-Constitution, April 2025"),
}

BANDS = {
    "look": ("Photography &middot; St. Andr&eacute;&rsquo;s own", "The brand shoots itself the way it plays: a beach chair on the putting green, a tee hung on the range fence, a sweater over the shoulders.",
             [("band-a1", "A man in a white St. André tee and red shorts reclining in a beach chair on a putting green", "On the green"),
              ("band-a2", "The back of a white St. André tee hung on a chain-link fence", "On the fence"),
              ("band-a3", "A man in a green St. André cap with a navy sweater over his shoulders", "Over the shoulders")]),
    "hats": ("Photography &middot; St. Andr&eacute;&rsquo;s own", "These show the hats on a rattan chair, with denim, a white tee and sunglasses.",
             [("band-b1", "A faded blue St. André Golf Classics cap on a white tee beside sunglasses", "Golf Classics"),
              ("band-b2", "A black St. André rope hat on a rattan chair", "Rope hat"),
              ("band-b3", "A white St. André rope hat with a yellow Classics patch", "Classics patch")]),
    "worn": ("Photography &middot; on the model", "How it is meant to be worn: loose tees, sunglasses and a hat pulled low.",
             [("band-c1", "A man in a green St. André tee and a white cap with sunglasses", "Green tee"),
              ("band-c2", "A man in a white St. André bucket hat", "Bucket hat"),
              ("band-c3", "A man in a white St. André tee and a grey cap", "White tee")]),
}

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>St. Andr&eacute; is a comedy troupe that happens to make very good golf merch. Aaron Chewning started it in Atlanta in August 2022 with sketches about public-course golf, and the shop grew out of the audience. The tagline says it plainly: It&rsquo;s Just Golf.</p>
    <p>The joke lives in the copy, not the design. The tees are sold as &ldquo;non-performance gear&rdquo; and the cat towel is called Pspsps. But the covers are green checkered leather with a yellow script A, the hats carry a wordmark from an old pro shop, and the name crosses St Andrews with Andr&eacute; 3000. It looks straight. That is what makes it funny.</p>
    <p>Buy the Classic Driver Cover at $35. For the new stuff, the Pspsps towel at $45. Prices were read from the brand&rsquo;s store on 28 September 2026, in US dollars. Stock runs thin, and several pieces are down to one colourway.</p>
    <h2 class="products-hdr btk-story-hdr">The Story</h2>
    <p>Chewning grew up in Snellville, Georgia, played on his high school golf team, studied film and built a Vine following of 1.3 million before the app shut down. He wrote the first golf sketches in 2021, then quit his agency job and paid for the start on a credit card. The cast is Hannah Rae Aslesen and Jonathan Pawlowski, both from Atlanta&rsquo;s comedy and improv scene, and most of the videos are shot at Heritage Golf Links in Tucker.</p>
    <p>The videos took off in the first week, when big golf meme accounts shared them. Bridgestone got in touch within months, the partnership was announced in March 2023, and the group filmed with Tiger Woods. The Atlanta Journal-Constitution reports that St. Andr&eacute; turned a profit two years in, with a design partner and four investment partners, including former Braves pitcher Collin McHugh.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Based</span><span>Atlanta, Georgia</span></div>
      <div class="sidebar-detail"><span class="l">Founder</span><span>Aaron Chewning</span></div>
      <div class="sidebar-detail"><span class="l">Cast</span><span>Hannah Rae Aslesen, Jonathan Pawlowski</span></div>
      <div class="sidebar-detail"><span class="l">Since</span><span>August 2022</span></div>
      <div class="sidebar-detail"><span class="l">Made</span><span>Not stated by the brand</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$10&ndash;$50</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Classic Driver Cover, $35</span></div>
      <a href="https://standre.golf/" target="_blank" rel="noopener" class="sidebar-cta">Visit St. Andr&eacute; &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#StAndreGolf</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#ItsJustGolf</span>
        <span class="hashtag">#GolfComedy</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

FAQ = [
    ("Who is behind St. André Golf?",
     "Aaron Chewning, a filmmaker and comedian from Snellville, Georgia, founded it in Atlanta in August 2022. The cast is Hannah Rae Aslesen and Jonathan Pawlowski."),
    ("Why is it called St. André?",
     "The name combines St Andrews, the home of golf, with André 3000 of the Atlanta group OutKast. Chewning has said he wanted a name that looked classy on a shirt and nodded to classic golf."),
    ("Is St. André a clothing brand or a comedy group?",
     "Both, but the comedy comes first. St. André makes golf sketches for social media and YouTube, and sells hats, tees, headcovers and accessories through its own online shop."),
    ("Where is St. André gear made?",
     "The brand does not say on its site. The Patch Performance Hat is made by Pukka, and the glove is a collaboration with Palm Golf."),
    ("What should I buy first from St. André?",
     "The Classic Driver Cover ($35) in green checkered faux leather is the signature piece. The Classic Ball Marker ($10) and Palm glove ($20) are the least expensive ways in. The Pspsps Jacquard Towel ($45) is the newest release."),
]


def pq(key):
    txt, attr = PQ[key]
    return (f'\n<!-- TGI-SA-PQ-{key} -->\n<div class="pull-quote">\n  <div class="pull-quote-inner">'
            f'&ldquo;{txt}&rdquo;<span class="pull-quote-attr">&mdash; {attr}</span></div>\n</div>\n'
            f'<!-- /TGI-SA-PQ-{key} -->\n')

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
    label = H.unescape(f"St. André {name} {detail}").replace('"', "")
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
            f'<div class="product-name">{name} &middot; ${price}</div>'
            f'<div class="product-desc">{copy}</div>'
            f'<a href="{SHOP}{h}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


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
            items.append({"@type": "ListItem", "position": pos, "url": SHOP + h, "name": H.unescape(f"St. André {P[h][0]}")})
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
            {"@type": "ListItem", "position": 3, "name": "St. André Golf", "item": URL}]},
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
    assert len(ids) == 12 == len(set(ids)) and set(ids) == set(P)
    for h in ids:
        assert FR.get(h), h
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  St. Andr&eacute; Golf</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Atlanta, GA &middot; since 2022</span><span class="dot"></span>
    <span>12 pieces &middot; $10&ndash;$50</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A man in a yellow tee and a St. Andr&eacute; trucker cap with a golf ball in his mouth" fetchpriority="high" /></div></div>
"""
    body += TAKE + band("look") + pq("classy")
    n = 1
    s, n = section(SECTIONS[0], n); body += s + band("hats") + pq("funny")
    s, n = section(SECTIONS[1], n); body += s + band("worn")
    s, n = section(SECTIONS[2], n); body += s + pq("living")
    body += faq_html()
    out = head_top() + head_rest + body + tail
    print(f"  {n-1} picks")
    if not apply_:
        print("  dry run — pass --apply")
        return
    OUT.write_text(out, encoding="utf-8")
    verify()


def verify():
    fin = OUT.read_text(encoding="utf-8")
    bad = []
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    for leak in ("Burnt Orange", "Manors Revisited", "Nicklaus", "Dimple"):
        if leak in above:
            bad.append(f"should not appear: {leak}")
    if fin.count('class="product-card"') != 12:
        bad.append("card count")
    for k, (t, _) in PQ.items():
        if fin.count(t[:50]) != 1:
            bad.append(f"pq {k}")
    if above.count('class="ig-grid"') != 3:
        bad.append("band count")
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
