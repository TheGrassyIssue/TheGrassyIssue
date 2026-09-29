#!/usr/bin/env python3
"""build-enron-golf.py — Enron's golf line: what the new Enron is, and should you buy the hat.
29 September 2026. Lenny: "without Irony, Enron has a pretty solid golf collection ...
let's do a post, what is Enron, and why should someone pick up a hat." Then, mid-build:
"let's include, maybe fuck these guys, pro's and con's" -> the Case For and Against section.

FACTS + QUOTES: research/enron/notes.md (verified 29 Sep 2026). Parody status per enron.com's
own terms. The 2001 collapse is stated plainly, with the AP figures. The crypto token is
mentioned once, factually, with no link. The Women of Enron tee is deliberately left out.
PHOTOS: enron.com's own product-page photography. Prices read 29 Sep 2026, USD.
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "enron-golf-collection"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/enron-golf"
FR = json.loads((ROOT / "research/enron/frames-by-handle.json").read_text())
BJ = json.loads((ROOT / "research/enron/band.json").read_text())
SHOP = "https://enron.com/products/"
BRAND = "Enron"

TITLE = "Enron Golf: What Is the New Enron, and Should You Buy the Hat?"
DESC = ("Enron is back as a parody brand, and its Pro E1 golf line is better than it has any right to be. "
        "What the new Enron is, the case for and against, and 12 picks.")
H1 = "Enron Golf: What Is the New Enron, and Should You Buy the Hat?"

P = {
 "pro-e1-enron-pro-e1": ("Pro E1 Hat", "Cream and green", "40",
   "This is the one. It is a 100% cotton five-panel with a cream crown, a green brim and the tilted E logo in red, green and blue. From across the range it reads as a pro-shop cap, and that is the whole joke."),
 "pro-e1-performance-hat": ("Pro E1 Performance Hat", "Black, rope", "40",
   "It has a structured, high-profile black crown with Enron in white script, a braided rope, a pre-curved brim and a COOLMAX sweatband. It is the most technical hat in the line."),
 "pro-e1-boonie-hat": ("Pro E1 Boonie", "White", "40",
   "This is a white polyester bucket with a drawcord and the logo on the front, for the hottest rounds of the year. It is the least serious hat in the line, which is saying something."),
 "enron-was-right-hat": ("Enron Was Right Snapback", "Gray or black", "40",
   "The front reads ENRON WAS RIGHT ABOUT EVERYTHING in white block letters, with a small flag on the side. It is the loudest joke in the shop, and the one to think about before you wear it anywhere near Houston."),
 "shareholder-conference-hat": ("2000 Shareholder Snapback", "Black, flat brim", "32",
   "This is a flat-brim black snapback embroidered 2000 Enron Annual Shareholder Conference. The product copy says it commemorates &ldquo;a very successful year.&rdquo; You will know whether that is funny to you."),
 "dad-hat": ("Dad Hat", "Khaki or black", "32",
   "This is the quiet one: an unstructured cap with the logo on the front and World&rsquo;s Leading Company on the back. It is the least expensive hat here and the easiest to wear."),
 "pro-e1-polo": ("Pro E1 Polo", "Black or green", "68",
   "It is a 5oz cotton and recycled-polyester polo with UPF 40+ protection, side vents and an active fit, with the logo on the chest and PRO E1 across the placket side. The green is the better golf shirt."),
 "pro-e1-polo-pink": ("Pro E1 Polo", "Pink", "68",
   "This one arrived in September in a heavier 6oz pique, wrinkle-resistant with a standard fit. It is pink with the logo on the chest and it looks exactly like a real club polo."),
 "pro-e1-quarter-zip": ("Pro E1 Quarter Zip", "Black", "68",
   "It is a heavyweight 10oz cotton-blend fleece with a relaxed fit, the logo on the chest and Enron in script down the sleeve. It is the piece we would actually wear in November."),
 "pro-e1-driver-cover": ("Pro E1 Driver Cover", "Red, green and blue", "45",
   "This is PU leather in the logo&rsquo;s three colours, split diagonally, with the E up top. It is the best object in the line."),
 "enron-pro-e1-golf-balls": ("Pro E1 Golf Balls", "Three-layer", "20",
   "The balls are three-layer and printed with the logo, in a sleeve box. The page does not say who makes them or how many come in a sleeve."),
 "corporate-puffer-vest-black-1": ("Corporate Puffer Vest", "Black", "88",
   "It is a black nylon puffer with a zip chest pocket and the logo on the left chest, added last week. The product copy calls it &ldquo;The official Enron Corporate Vest.&rdquo;"),
}

SECTIONS = [
    ("hats", "The Hats", "the-hats",
     ["pro-e1-enron-pro-e1", "pro-e1-performance-hat", "pro-e1-boonie-hat", "enron-was-right-hat", "shareholder-conference-hat", "dad-hat"],
     "<strong>Six hats &middot; $32&ndash;$40</strong>Three are from the Pro E1 golf line, and three carry the brand&rsquo;s older jokes."),
    ("golf", "The Pro E1 Line", "pro-e1",
     ["pro-e1-polo", "pro-e1-polo-pink", "pro-e1-quarter-zip", "pro-e1-driver-cover", "enron-pro-e1-golf-balls", "corporate-puffer-vest-black-1"],
     "<strong>Six pieces &middot; $20&ndash;$88</strong>These are the golf clothes and gear that launched in July, plus the vest that arrived last week."),
]

PQ = {
    "logo": ("The logo is beautiful, it&rsquo;s just built to draw you in and ask more, ask why.",
             "Connor Gaydos, Enron&rsquo;s CEO, to the Houston Chronicle, January 2025"),
    "peters": ("It&rsquo;s a pretty sick joke and it disparages the people that did work there.",
               "Diana Peters, a former Enron employee, to the Associated Press, December 2024"),
}

BANDS = {
    "look": ("Photography &middot; Enron&rsquo;s own", "The campaign is shot like a real golf brand&rsquo;s, which is exactly the point.",
             [(x["local"].split("/")[-1][:-4], H.escape("Enron Pro E1 campaign photograph: " + x["title"]), c)
              for x, c in zip(BJ, ["Pro E1 Polo", "Pro E1 Polo, pink", "Pro E1 Quarter Zip"])]),
}

PROSE = 'style="max-width:760px;font-size:16px;line-height:1.7;margin:0 auto 24px;"'

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Without irony, Enron has a good golf collection. The Pro E1 line that launched in July has a cream-and-green five-panel, a UPF polo, a heavyweight quarter zip and a driver cover in the logo&rsquo;s red, green and blue, and it is shot and cut like a real golf brand&rsquo;s. That is the joke, and it works because nobody in the clothes is winking.</p>
    <p>The reason to pick up a hat is the logo. The tilted E is one of the best corporate marks ever drawn, and on a $40 cap it reads as a pro-shop hat until someone gets close enough to read it. Then you have a conversation.</p>
    <p>The reason not to is below, in the case for and against. Start with the Pro E1 Hat at $40. Prices were read from enron.com on 29 September 2026, in US dollars.</p>
    <h2 class="products-hdr btk-story-hdr">What Enron Is</h2>
    <p>The original Enron was a Houston energy company that became one of the largest in America and collapsed in December 2001, after years of accounting fraud hid billions in debt. The Associated Press counts more than 5,000 jobs lost, more than $2 billion in employee pensions wiped out and $60 billion in stock rendered worthless. Executives went to prison.</p>
    <p>The Enron selling golf hats is something else. In 2020 a small Arkansas company co-founded by Connor Gaydos, one of the people behind the satirical Birds Aren&rsquo;t Real, bought the Enron trademark for $275. It relaunched on 2 December 2024, the anniversary of the bankruptcy, with the line &ldquo;We&rsquo;re back. Can we talk?&rdquo; Its own terms of use call the site parody and performance art. Since then it has sold a joke home nuclear reactor called the Enron Egg, filed a real application to sell electricity in Texas, and launched a crypto token that lost most of its value within a day.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">What it is</span><span>A parody brand, by its own terms</span></div>
      <div class="sidebar-detail"><span class="l">CEO</span><span>Connor Gaydos</span></div>
      <div class="sidebar-detail"><span class="l">Relaunched</span><span>2 December 2024</span></div>
      <div class="sidebar-detail"><span class="l">Golf line</span><span>Pro E1, July 2026</span></div>
      <div class="sidebar-detail"><span class="l">Hats</span><span>$32&ndash;$40</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Pro E1 Hat, $40</span></div>
      <a href="https://enron.com/collections/golf" target="_blank" rel="noopener" class="sidebar-cta">See the golf line &#8599;</a>
      <div class="hashtags">
        <span class="hashtag">#Enron</span>
        <span class="hashtag">#GolfHats</span>
        <span class="hashtag">#ProE1</span>
        <span class="hashtag">#GolfCulture</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

def _col(title, items):
    lis = "".join(f'<li style="margin:0 0 12px;">{i}</li>' for i in items)
    return (f'<div style="background:rgba(255,255,255,.55);border:1px solid rgba(20,20,20,.14);padding:22px 24px;text-align:left;">'
            f'<div style="font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--grass);margin-bottom:14px;">{title}</div>'
            f'<ul style="margin:0;padding-left:18px;font-size:15px;line-height:1.6;">{lis}</ul></div>')

FOR = [
    "<strong>The design plays it straight.</strong> The logo is excellent, the colours work on a golf course, and the campaign could pass for any new golf label&rsquo;s.",
    "<strong>The specs are real.</strong> A COOLMAX sweatband on the performance hat, UPF 40+ on the polo, a 10oz fleece on the quarter zip.",
    "<strong>The price is fair.</strong> Hats are $32 to $40, about what an independent golf cap costs.",
    "<strong>It is a good joke.</strong> It comes from the people who made Birds Aren&rsquo;t Real, and it gets a reaction on every first tee.",
]
AGAINST = [
    "<strong>The collapse was real.</strong> Thousands of people lost jobs and retirement savings, and some of them are still angry that the name is being used for a joke.",
    "<strong>The revival has its own money trouble.</strong> Its crypto token lost most of its value within a day of launch, and Bloomberg has reported allegations of investor losses. A hat is not an endorsement, but your $40 goes to the same company.",
    "<strong>You do not know who makes it.</strong> Most product pages name no maker and no country of origin.",
    "<strong>Some of the jokes age badly.</strong> &ldquo;Enron Was Right About Everything&rdquo; and the shareholder hat read very differently to anyone who held Enron stock.",
]

CASE = f"""
<section class="products" style="margin-top:8px;">
  <div class="drop-tag grass">Or Maybe Not</div>
  <h2 class="products-hdr" id="for-and-against">Should You Buy It? The Case For and Against</h2>
  <div {PROSE}>
    <p style="margin:0 0 16px;">This is a fair question to ask about a brand built on a real fraud, so here are both sides.</p>
  </div>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:18px;max-width:1000px;margin:0 auto 28px;">
    {_col("The case for", FOR)}
    {_col("The case against", AGAINST)}
  </div>
  <div {PROSE}>
    <p style="margin:0 0 16px;">Our line: the Pro E1 Hat, the green polo and the driver cover work as golf gear first and a joke second, and they are the ones we would buy. The slogan hats are for people who want to explain the joke, and who know who is in their group.</p>
  </div>
</section>
"""

FAQ = [
    ("Is Enron a real company again?",
     "The name belongs to a new company run by Connor Gaydos, one of the creators of Birds Aren't Real, which bought the Enron trademark in 2020. Its own terms of use describe the site as parody and performance art, but it sells real merchandise, and it filed a real application to sell electricity in Texas in January 2025."),
    ("What happened to the original Enron?",
     "The Houston energy company filed for bankruptcy on 2 December 2001 after years of accounting fraud. The Associated Press reports that the collapse put more than 5,000 people out of work and wiped out more than $2 billion in employee pensions."),
    ("What is Enron Pro E1?",
     "Pro E1 is Enron's golf line, launched in July 2026: hats, a polo, a quarter zip, a tee, a driver cover, golf balls and wooden tees, priced from $15 to $68."),
    ("How much is an Enron golf hat?",
     "The Pro E1 Hat, Performance Hat, Boonie and Enron Was Right Snapback are $40. The Dad Hat and the 2000 Shareholder Snapback are $32."),
    ("Who is behind the new Enron?",
     "Connor Gaydos is the CEO. The trademark is owned by The College Company, an Arkansas company he co-founded, which bought it for $275 in May 2020."),
]


def pq(key):
    txt, attr = PQ[key]
    return (f'\n<!-- TGI-EN-PQ-{key} -->\n<div class="pull-quote">\n  <div class="pull-quote-inner">'
            f'&ldquo;{txt}&rdquo;<span class="pull-quote-attr">&mdash; {attr}</span></div>\n</div>\n'
            f'<!-- /TGI-EN-PQ-{key} -->\n')

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
    label = H.unescape(f"Enron {name} {detail}").replace('"', "")
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
            items.append({"@type": "ListItem", "position": pos, "url": SHOP + h, "name": H.unescape(f"Enron {P[h][0]}")})
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
            {"@type": "ListItem", "position": 3, "name": "Enron Golf", "item": URL}]},
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
  Enron Golf</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Pro E1 &middot; July 2026</span><span class="dot"></span>
    <span>12 picks &middot; $20&ndash;$88</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A golfer adjusting a cream and green Enron Pro E1 cap with the tilted E logo" fetchpriority="high" /></div></div>
"""
    body += TAKE + band("look") + pq("logo")
    n = 1
    s, n = section(SECTIONS[0], n); body += s
    s, n = section(SECTIONS[1], n); body += s + pq("peters") + CASE
    body += faq_html()
    out = head_top() + head_rest + body + tail
    print(f"  {n-1} picks")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    bad = []
    for leak in ("Manors Revisited", "Nicklaus", "St. Andr", "Women of Enron", "$ENRON", "Playboy"):
        if leak in above: bad.append("leak " + leak)
    if fin.count('class="product-card"') != 12: bad.append("card count")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", above), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
