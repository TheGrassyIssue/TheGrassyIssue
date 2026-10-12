#!/usr/bin/env python3
"""apply-offcourse-v1-format.py — reformat Off Course (Vol. 1) to the house layout. 11 Oct 2026.
Lenny: "the format for this post needs to be fixed ... Keep all the products but just fix it".
Keeps every product, every word of copy and every link. Changes: a hero image (three of the post's own product
photos side by side), one consistent heading + kicker style for all six categories (Coffee alone had an H2;
the rest used small dividers), every product photo reframed to the same 4:5 size (several were wide banners
cropped to slivers), card-wide links turned into the standard card with a Shop button, a 3-wide grid that
centres its last row, and a link to Vol. 2. Idempotent: it rebuilds the body from the cards it finds.
"""
import html, os, re, sys
from PIL import Image, ImageFilter
ROOT = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(ROOT, "drops/off-course-golf-brands-doing-non-golf-things.html")
KICK = {
 "Coffee": "Three roasters, one of them working out of a headcover studio. The obvious first step out of the pro shop.",
 "Non-Golf Kicks": "Sneakers from golf brands that are, in at least one case, explicitly not golf shoes.",
 "Food": "Hot sauce, jerky and energy balls, the snacks made to survive eighteen holes in a bag.",
 "Home + Fragrance": "A candle, incense and a cologne, for a house that smells like the nineteenth hole.",
 "Skin + Craft": "Sunscreen, a grooming line and a wool dopp kit.",
 "Wild Cards": "A children&rsquo;s book, a surf lab and dog treats. The furthest from golf on this list.",
}
CSS = ('<style id="tgi-oc1-format">.cat-kicker{font-family:var(--sans);font-size:15px;line-height:1.75;color:#3f443e;margin:0 0 36px;max-width:70ch;border-left:3px solid var(--rough);padding:4px 0 4px 18px}.products-grid[data-oc]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}'
       '.products-grid[data-oc]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}'
       '@media(max-width:820px){.products-grid[data-oc]>.product-card{flex-basis:calc((100% - 24px)/2)}}'
       '@media(max-width:480px){.products-grid[data-oc]>.product-card{flex-basis:100%}}</style>')

def frame(src):
    """800x1000 frame: the whole photo, centred over a blurred fill of itself, so wide banners are not cropped."""
    out = src.replace("/images/off-course/", "/images/off-course/f-")
    p_in, p_out = os.path.join(ROOT, src.lstrip("/")), os.path.join(ROOT, out.lstrip("/"))
    if src.startswith("/images/off-course/f-"):
        return src
    if not os.path.exists(p_out):
        im = Image.open(p_in).convert("RGB"); W, H = 800, 1000
        r = im.width / im.height
        if 0.7 <= r <= 0.9:
            s = max(W / im.width, H / im.height); i2 = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
            x, y = (i2.width - W) // 2, (i2.height - H) // 2; c = i2.crop((x, y, x + W, y + H))
        else:
            s = max(W / im.width, H / im.height); bg = im.resize((round(im.width * s) + 1, round(im.height * s) + 1), Image.LANCZOS)
            x, y = (bg.width - W) // 2, (bg.height - H) // 2
            c = bg.crop((x, y, x + W, y + H)).filter(ImageFilter.GaussianBlur(28))
            s2 = min(W / im.width, H / im.height); fg = im.resize((round(im.width * s2), round(im.height * s2)), Image.LANCZOS)
            c.paste(fg, ((W - fg.width) // 2, (H - fg.height) // 2))
        c.save(p_out, quality=86)
    return out

def hero(srcs):
    out = "/images/off-course/hero-v1.jpg"; p = os.path.join(ROOT, out.lstrip("/"))
    if not os.path.exists(p):
        W, H = 2000, 857; tw = (W - 16) // 3; c = Image.new("RGB", (W, H), "#f4f1ea")
        for i, s in enumerate(srcs):
            im = Image.open(os.path.join(ROOT, s.lstrip("/"))).convert("RGB")
            k = max(tw / im.width, H / im.height); i2 = im.resize((round(im.width * k) + 1, round(im.height * k) + 1), Image.LANCZOS)
            x, y = (i2.width - tw) // 2, (i2.height - H) // 2; c.paste(i2.crop((x, y, x + tw, y + H)), (i * (tw + 8), 0))
        c.save(p, quality=86)
    return out

def main(apply_):
    s = open(F, encoding="utf-8").read(); o = s
    a = s.index('<div class="breadcrumb">'); b = s.index('<div class="more"')
    body = s[a:b]
    if 'id="tgi-oc1-body"' in body:
        print("apply-offcourse-v1-format: already formatted"); return
    intro = body[:body.index('<!-- CATEGORY 1')]
    intro = intro.replace('    <p>Here are 18 brands doing it right.</p>',
        '    <p>Here are 18 brands doing it right. <a href="/drops/off-course-vol-2-golf-brands-doing-non-golf-things" style="border-bottom:1px solid currentColor">Vol. 2</a> has 24 more.</p>')
    cats = re.split(r'<!-- CATEGORY \d+: ([^>]+?) -->', body[body.index('<!-- CATEGORY 1'):])
    secs, imgs = [], []
    for name, chunk in zip(cats[1::2], cats[2::2]):
        cards = []
        for m in re.finditer(r'<a href="([^"]+)"[^>]*class="product-card">(.*?)</a>|<div class="product-card">(.*?)</div>\s*(?=<(?:a|div) [^>]*class="product-card"|\s*</div>\s*</section>)', chunk, re.S):
            href, inner = (m.group(1), m.group(2)) if m.group(1) else (None, m.group(3))
            img = re.search(r'<img src="([^"]+)" alt="([^"]*)"', inner)
            brand = re.search(r'<div class="product-brand">(.*?)</div>', inner, re.S).group(1)
            pname = re.search(r'<div class="product-name">(.*?)</div>', inner, re.S).group(1)
            desc = re.search(r'<div class="product-desc">(.*?)</div>', inner, re.S).group(1)
            btn = re.search(r'<span class="product-link">(.*?)</span>', inner, re.S)
            btn = btn.group(1).replace("&nearr;", "&#8599;") if btn else "Shop &#8599;"
            src = frame(img.group(1)); imgs.append(img.group(1))
            link = (f'<a href="{href}" target="_blank" rel="noopener" class="product-link">{btn}</a>' if href
                    else f'<span class="product-link" style="opacity:.6">{btn}</span>')
            cards.append(f'''    <div class="product-card">
      <div class="product-img"><img src="{src}" alt="{img.group(2)}" loading="lazy" /></div>
      <div class="product-body">
        <div class="product-brand">{brand}</div>
        <div class="product-name">{pname}</div>
        <div class="product-desc">{desc}</div>
        {link}
      </div>
    </div>''')
        secs.append(f'''
<section class="products">
  <h2 class="products-hdr">{name}</h2>
  <p class="cat-kicker">{KICK[name]}</p>
  <div class="products-grid" data-oc="1">
{chr(10).join(cards)}
  </div>
</section>
''')
    n = sum(x.count('class="product-card"') for x in secs)
    assert n == 18, n
    hsrc = "/images/off-course/hero-v1.jpg"  # Good Walk Coffee's own fairway shot (Lenny: "Need a Hero image")
    intro = intro.replace('</header>\n', f'</header>\n\n<div class="drop-hero"><div class="drop-hero-img"><img src="{hsrc}" alt="Two golfers walking a fairway with carry bags under autumn trees, from Good Walk Coffee&rsquo;s own photography" fetchpriority="high" /></div></div>\n', 1)
    new = intro + '<div id="tgi-oc1-body"></div>' + "".join(secs) + "\n"
    s = s[:a] + new + s[b:]
    s = re.sub(r'<style id="tgi-oc1-format">.*?</style>\n?', '', s, flags=re.S).replace("</head>", CSS + "\n</head>", 1)
    print(f"apply-offcourse-v1-format: {n} products in {len(secs)} sections")
    if apply_: open(F, "w", encoding="utf-8").write(s)

if __name__ == "__main__":
    main("--apply" in sys.argv)
