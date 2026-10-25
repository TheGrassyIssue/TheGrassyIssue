
FRN = json.loads((ROOT / "research/capsules/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
EXTRA_CSS = ('<style>/*TGI-R3-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}'
             '/*TGI-CAPSULE*/.swatches{display:flex;justify-content:center;gap:18px;flex-wrap:wrap;margin:6px 0 22px}.swatch{display:flex;align-items:center;gap:8px;font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase}.swatch i{display:inline-block;width:22px;height:22px;border-radius:50%;border:.5px solid var(--ink)}'
             '.looks{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin:8px 0 34px}.looks figure{margin:0}.looks img{width:100%;aspect-ratio:4/5;object-fit:cover;border:.5px solid var(--ink);display:block;background:#e8e2d6}.looks figcaption{font-size:13px;line-height:1.5;margin-top:10px;text-align:center}.looks figcaption b{display:block;font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;font-weight:500;margin-bottom:4px}@media(max-width:900px){.looks{grid-template-columns:repeat(2,1fr)}}'
             '.capsule-toc{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin:0 auto 10px;max-width:900px}.capsule-toc a{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;border:.5px solid var(--ink);padding:7px 12px}</style>\n')


def card(k, idx):
    brand, item, price, url, copy = P[k]
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


INTRO = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The Idea</div>
    <p>A capsule wardrobe is a small set of pieces that all go together: about ten staples in one palette, so anything you pull out of the closet works with anything else. Nobody has to think at 6:40 a.m. before a muni tee time, and nobody has to buy a new outfit for the one round a year at a course with a dress code.</p>
    <p>Golf is a good fit for the idea because golf clothes repeat. You need a polo, something for your legs, a layer and a hat, and the only thing that changes is how dressed up the day is. So we built five capsules for five different tastes, each from the independent brands we cover. Each has ten or eleven pieces in a tight palette, and each comes with four outfits made only from those pieces: the muni round, the special-day course, dinner after, and a cold morning.</p>
    <p><strong>How we built them.</strong> Every capsule follows the same rules. Three neutrals and one accent colour. At least three tops, two bottoms and one real layer. One piece that dresses the whole thing up (a pleated trouser, a cashmere crew, a vest). One hat that goes with everything. And no piece that only works with one other piece.</p>
    <p>Every price and size was checked on the brands&rsquo; own stores on October 25, 2026. Prices from UK, Australian, Swedish and South African stores are converted to US dollars, with the original price shown. Some sizes are already thin, and we&rsquo;ve said so on the card.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Capsules</div>
      <div class="sidebar-detail"><span class="l">Capsules</span><span>5</span></div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>52</span></div>
      <div class="sidebar-detail"><span class="l">Outfits</span><span>20</span></div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>29 independents</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$25&ndash;$295</span></div>
      <div class="sidebar-detail"><span class="l">Checked</span><span>October 25, 2026</span></div>
      <div class="hashtags">
        <span class="hashtag">#CapsuleWardrobe</span>
        <span class="hashtag">#GolfStyle</span>
        <span class="hashtag">#TheEdit</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
CLOSE = """
<section class="products" style="margin-top:8px;">
  <div class="drop-tag grass">Build Your Own</div>
  <h2 class="products-hdr" id="build-your-own">How to Build a Golf Capsule Wardrobe</h2>
  <p class="cat-kicker">Start with the palette, not the pieces: pick three neutrals you already wear and one accent you like. Buy the bottoms first, because a good trouser and a good short carry more outfits than any shirt. Then add three tops that each work with both bottoms, one layer that goes over all three, and a hat in one of the neutrals. Leave the loud piece for last and make it the accent. If a new piece only goes with one thing you own, it isn&rsquo;t a capsule piece.</p>
</section>
"""
FAQ = [
 ("What is a golf capsule wardrobe?", "A small set of about ten golf clothes in one palette, usually three neutrals and one accent, where every top works with every bottom so you can dress for any round without thinking about it."),
 ("How many pieces should a golf capsule wardrobe have?", "About ten: three or four tops, two or three bottoms, one or two layers, a hat and socks. That gives you well over a dozen combinations."),
 ("What colours work best for a golf capsule wardrobe?", "Pick three neutrals, such as navy, cream and stone, or black, olive and grey, then one accent colour like forest green, cobalt or terracotta."),
 ("Can a capsule wardrobe work for a course with a dress code?", "Yes. Include one collared polo and one tailored trouser, such as a pleated or chino-cut pant, and the same capsule covers a muni round and a private course."),
 ("Which brands are in TGI's capsule wardrobes?", "Twenty-nine independent brands, including Criquet, Rookline, Woodgrain, Public Drip, Hidden Links Society, Odd Ritual, Sentinel, Late Nine, Metalwood, Read The Green, Sounder, Manors, Gramicci, Mount Tee, Howie Benson and Juniper & James."),
]


def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>'
                     for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items, pos = [], 1
    for cap in CAPS:
        for k in [x for x in P if re.fullmatch(cap[0] + r"\d+", x)]:
            items.append({"@type": "ListItem", "position": pos, "url": P[k][3], "name": H.unescape(f"{P[k][0]} {P[k][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-10-25", "dateModified": "2026-10-25",
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
<link rel="preload" as="image" href="{IMG}/hero.jpg" />
{ld}"""


def capsule(i, cap, n0):
    key, name, anchor, sw, intro, brands, rng = cap
    ids = sorted([x for x in P if re.fullmatch(key + r"\d+", x)], key=lambda x: int(x[2:]))
    sws = "".join(f'<span class="swatch"><i style="background:{c}"></i>{lab}</span>' for lab, c in sw)
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    looks = "\n".join(
        f'  <figure><img src="{IMG}/look-{key}-{m}.jpg" alt="{H.escape(name_)} outfit from the {H.unescape(name)} capsule: {H.escape(cap_)}" loading="lazy" />'
        f'<figcaption><b>{H.escape(name_)}</b>{H.escape(cap_)}</figcaption></figure>'
        for m, (name_, _, cap_) in enumerate(LOOKS[key], 1))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">Capsule {i} &middot; {len(ids)} pieces</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{name}</h2>\n'
            f'  <div class="swatches">{sws}</div>\n'
            f'  <p class="cat-kicker"><strong>{brands} &middot; {rng}</strong>{intro}</p>\n'
            f'    <div class="products-grid" data-n="{len(ids)}">\n{cards}\n    </div>\n'
            f'  <h3 class="products-hdr" style="font-size:26px;margin-top:44px" id="{anchor}-outfits">Four Outfits From the {name}</h3>\n'
            f'  <div class="looks">\n{looks}\n  </div>\n</section>\n'), n0 + len(ids)


def main(apply_):
    ids = [x for c in CAPS for x in sorted([x for x in P if re.fullmatch(c[0] + r"\d+", x)], key=lambda x: int(x[2:]))]
    assert len(ids) == N == len(set(ids)) and set(ids) == set(P), set(P) ^ set(ids)
    for k in ids:
        assert FRN[k] and all((ROOT / f.lstrip("/")).is_file() for f in FRN[k]), k
    for key, looks in LOOKS.items():
        for _, keys, _ in looks:
            assert all(x in P and x.startswith(key) for x in keys), keys
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    toc = "".join(f'<a href="#{c[2]}">{c[1]}</a>' for c in CAPS)
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>The Edit &middot; Five capsules &middot; Twenty outfits</span><span class="dot"></span>
    <span>52 picks &middot; prices checked October 25, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Five golf looks side by side, one from each capsule: tan pleated trousers in a wood-panelled clubroom, a slate waffle polo, a pleated short and knit polo, a merino crew on the course, and a waffle polo with a green cap" fetchpriority="high" /></div></div>
"""
    body += INTRO
    body += f'\n<div class="capsule-toc">{toc}</div>\n'
    n = 1
    for i, c in enumerate(CAPS, 1):
        o, n = capsule(i, c, n); body += o
    body += CLOSE
    body += faq_html()
    out = head_top() + head_rest.replace("</head>", EXTRA_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards, {sum(len(v) for v in LOOKS.values())} looks")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    bad = []
    if fin.count('class="product-card"') != N: bad.append("card count")
    if re.search(r"\bworth\b", re.sub(r"\bFort\s+Worth\b", " ", re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<script\b.*?</script>", " ", above))), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
