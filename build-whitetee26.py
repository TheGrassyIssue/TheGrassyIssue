#!/usr/bin/env python3
"""
build-whitetee26.py — The White Tee Edit (2026).

BRIEF (Lenny, 2026-08-29): "another white tee round up - research options from
across our brand universe and some not from our list."

SELECTION
Lenny picked from an 18-option grid. Two later edits:
  · #10 Bunker Mentality -> Radry Staple Tee (Bone). Radry has exactly ONE
    white-ish tee and it is down to MD and XL, so it is flagged in the copy.
  · #13 Palmes -> Metalwood. Palmes is a tennis label and was only ever in the
    grid on looks.
Metalwood then appeared twice (Stonehenge already at #5). Lenny: "it's just
Metalwood studio - not metalwood rorschach. Don't make two brand cards." So the
two Metalwood tees share ONE card at $54-$62. Result: 17 cards, 17 brands, which
puts the post back inside the standing no-repeat-brands rule.

SUPERSEDES
`drops/10-white-tees-to-beat-the-texas-heat.html` — summer-framed, and it is
September. New slug, 301 from the old one, per the Aussie-post precedent.

EVERY price, colourway and stock state was verified against the brand's own
store on 2026-08-29, mostly via Shopify /products.json. Images are downloaded
locally to /images/whitetee26/ — never hot-linked.
"""
import json, os, re, html, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
SKUS = json.load(open(os.path.join(ROOT, "research", "whitetee26-skus.json")))
S = {x["key"]: x for x in SKUS}
SLUG = "the-white-tee-edit-2026"
TITLE = "The White Tee Edit &mdash; 17 From the Universe and Beyond"
DESC = ("Seventeen white and off-white golf tees, one per brand, verified in stock: "
        "Odd Ritual, Metalwood Studio, Criquet, Siegelman Stable, Radry and eleven more, "
        "including five labels new to The Grassy Issue.")

# alt text and per-card copy, written from what the product photography actually shows
CARD = {
 "criquet": ("Criquet Shirts &middot; Austin, TX", "Slub Cotton Pocket T-Shirt &middot; Natural &middot; $64",
   "Criquet cuts this in natural slub cotton and adds a chest patch pocket with a tonal embroidered Grassy C. The texture does the work a print would do elsewhere, which is why it is the one here that will still look considered in three summers. Austin makes it, and it comes closest to a house tee."),
 "huega": ("Huega House &middot; In stock", "Essential Tee &middot; Cream &middot; $57",
   "Huega House keeps this one blank: a heavyweight cream crew, a small tonal wordmark at the right chest, nothing else. Buy it if every other tee here feels like it is talking too much."),
 "siegelman": ("Siegelman Stable &middot; In stock", "Embroidered Classic Tee &middot; White &middot; $102",
   "Siegelman Stable builds this on thirteen-ounce jersey and puts one small black embroidery of a harness racer and sulky at the left chest. It is the most expensive plain tee here by some distance, and the weight is the argument for it."),
 "radry": ("Radry Golf &middot; MD and XL only", "Staple Tee &middot; Bone &middot; $55",
   "Radry cuts this in Bone rather than white and prices it at $55, with a small tonal mark at the centre chest and an orange tab at the collar. Radry makes one pale tee and this is it, which is also why it is down to two sizes."),
 "anti": ("ANTi Country Club Tokyo &middot; New to TGI", "2026 SS &lsquo;A&rsquo; Embroidered T-Shirt &middot; White &middot; &yen;11,550",
   "ANTi Country Club Tokyo comes with Vans and Metalwood collaborations behind it. The Old English A is embroidered at the left chest in thread matched to the body, so it reads as texture at any distance. Nothing here is more restrained."),
 "odd-ritual": ("Odd Ritual &middot; Cape Town", "Odd Birdie T-Shirt &middot; White &middot; R1,000",
   "Odd Ritual builds the best single graphic here. A cream panel across the back carries the wordmark arched over a black bird, and the front holds only a small navy embroidery. It drops at the shoulder, cuts boxy, and gets photographed on a model rather than a hanger."),
 "casualist": ("Casualist &middot; London", "Good Enough Tee &middot; Off-white &middot; &pound;65",
   "Casualist weighs this at three hundred and eighty grams and runs a hand-drawn collage of golf ephemera across the back in pink, black and red. Casualist shoots it on a course instead of a studio wall, which is the reason it reads as clothing."),
 "fella": ("Fella Golf &middot; Amsterdam", "Taqueria T-Shirt &middot; White &middot; &euro;60",
   "Red back print arching Taqueria FELLA over a taco built from a golf ball, with breakfast ball tacos beneath. A joke that lands because the drawing is good, not because the line is."),
 "jlindeberg": ("J.Lindeberg &middot; Stockholm", "30Y Hale T-Shirt &middot; White &middot; &euro;95",
   "Cut for the label's thirtieth year. A small boxed logo at the left chest, then the full name in black caps over a pink-red rectangle across the back. The only piece here from a brand your pro shop already stocks."),
 "metalwood": ("Metalwood Studio &middot; Two white tees", "Rorschach &middot; $54 &nbsp;&middot;&nbsp; Stonehenge &middot; $62",
   "Metalwood is the only label with real depth in white, so it gets both. The Rorschach puts a red inkblot under the wordmark and is the strongest front print in the roundup; the Stonehenge spells METAL WOOD in stacked boulder lettering. Rorschach has the better size run."),
 "seamus": ("Seamus Golf &middot; Portland, OR", "Chasing Rainbows T-Shirt &middot; Natural &middot; $55",
   "Seamus puts a red-outlined oval badge on the back and sets the name in serif with a rainbow arc through it. The body is garment-dyed, so the ground is bone rather than optic white, which keeps it from reading as merchandise."),
 "walker": ("Walker Golf Things &middot; Australia", "Torana T-Shirt &middot; White &middot; A$59.95",
   "Walker cuts this around an orange Holden Torana printed centre chest, a golf bag propped against it. It is the only front graphic in the roundup that is neither a logo nor a badge, and the specificity is the point."),
 "pluto": ("Pluto Golf &middot; Indianapolis &middot; New to TGI", "Boy Pluto Floater Tee &middot; White &middot; $44",
   "Founded by Quentin Purtee and Leen Dhillon for golfers who came in through sneakers. The astronaut mascot is drawn mid-swing in single-colour line art, large and centred. Forty-four dollars, and it reproduces perfectly small."),
 "rebolf": ("Rebolf &middot; Barcelona &middot; New to TGI", "Rodeo White Tee &middot; &euro;35",
   "Rebolf prices this at thirty-five euro and cuts it with a burgundy ringer collar, RODEO GOLF RANGE arched over a cowboy-golfer illustration. It is the cheapest tee here and the only ringer, so it breaks up a grid that otherwise runs to plain crews."),
 "badlands": ("Badlands &middot; Atlantic Highlands, NJ &middot; New to TGI", "Great Atlantic T-Shirt &middot; White/Blue &middot; $45",
   "A navy laurel crest reading GREAT ATLANTIC SPORTING CLUB over Monmouth County, on six-and-a-half-ounce American cotton. A shop that started selling other people's clothes and now makes its own."),
 "3putt": ("3 Putt Round &middot; Milan &middot; New to TGI", "Who&rsquo;s Your Caddy? T-Shirt &middot; White &middot; &euro;45",
   "3 Putt Round cuts everything except two lines of small type centre chest. Restraint this severe either works completely or not at all, and on a white tee it works."),
 "nlu": ("No Laying Up &middot; New to TGI", "Take A Caddie T-Shirt &middot; White &middot; $48",
   "Made with Field Day for the Western Golf Association, whose Evans Scholarship puts caddies through college. The green WGA Bureau of Caddies crest sits on the back. The one tee here that pays for something."),
}
ALT = {
 "criquet":"Criquet Shirts slub cotton pocket t-shirt in natural",
 "huega":"Huega House Essential Tee in cream","siegelman":"Siegelman Stable embroidered classic tee in white",
 "radry":"Radry Golf Staple Tee in bone","anti":"ANTi Country Club Tokyo embroidered A t-shirt in white",
 "odd-ritual":"Odd Ritual Odd Birdie t-shirt in white","casualist":"Casualist Good Enough Tee in off-white",
 "fella":"Fella Golf Taqueria t-shirt in white","jlindeberg":"J.Lindeberg 30Y Hale t-shirt in white",
 "metalwood":"Metalwood Studio Rorschach and Stonehenge t-shirts in white",
 "seamus":"Seamus Golf Chasing Rainbows t-shirt in natural","walker":"Walker Golf Things Torana t-shirt in white",
 "pluto":"Pluto Golf Boy Pluto Floater tee in white","rebolf":"Rebolf Rodeo ringer tee in white",
 "badlands":"Badlands Great Atlantic t-shirt in white and blue",
 "3putt":"3 Putt Round Who's Your Caddy t-shirt in white","nlu":"No Laying Up Take A Caddie t-shirt in white",
}
SECTIONS = [
 # 5 / 6 / 6 rather than 5/4/5/3. The grid is three wide, so a four-card section
 # strands one card alone on its own row and a three-card section reads thin.
 # These counts fill every row.
 ("blank","The Ones With Nothing On Them",
  "TEXTURE, WEIGHT AND EMBROIDERY &middot; $55&ndash;$102",
  "A white tee with no graphic has nowhere to hide, so these five are judged on cloth and cut alone. Slub, thirteen-ounce jersey, bone, and one Tokyo embroidery matched to its own body. They are the hardest ones to photograph and the easiest ones to wear.",
  ["criquet","huega","siegelman","radry","anti"]),
 ("backs","The Back Prints",
  "THE GRAPHIC IS BEHIND YOU &middot; $48&ndash;&euro;95",
  "Six labels that leave the front almost bare and put the whole idea across the shoulders. It is the format that suits golf best, because the person who sees it is the one standing behind you on the tee.",
  ["odd-ritual","casualist","fella","jlindeberg","seamus","nlu"]),
 ("fronts","The Front Graphics",
  "CHEST-FIRST &middot; &euro;35&ndash;A$59.95",
  "Prints that do their work face on: an inkblot, a Holden, an astronaut, a cowboy, a Monmouth County crest and two lines of type. These are the six that read at thumbnail size, which is the only test that matters once a photograph of you exists.",
  ["metalwood","walker","pluto","rebolf","badlands","3putt"]),
]

def gallery(k, n, alt):
    fr = "".join(f'<div class="pg-frame"><img src="/images/whitetee26/{k}-{i}.jpg" loading="lazy" '
                 f'alt="{alt} &middot; view {i+1} of {n}"></div>' for i in range(n))
    dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" '
                   f'aria-label="View image {i+1}"></button>' for i in range(n))
    return (f'<div class="product-gallery"><div class="pg-track">{fr}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>')

def card(k):
    x = S[k]; brand, name, desc = CARD[k]; n = x["frames"]
    host = x["host"]
    return (f'  <div class="product-card" id="{k}" data-frames="{n}">\n'
            f'    {gallery(k, n, ALT[k])}\n'
            f'      <div class="product-body">\n'
            f'        <div class="product-brand">{brand}</div>\n'
            f'        <div class="product-name">{name}</div>\n'
            f'        <div class="product-desc">{desc}</div>\n'
            f'        <a class="product-link" href="{x["url"]}" target="_blank" rel="noopener">{host} &#8599;</a>\n'
            f'      </div>\n  </div>')

def build():
    tpl = open(os.path.join(ROOT, "drops", "the-niche-grip-report.html"), encoding="utf-8").read()
    head = tpl[:tpl.find('<section class="products"')]
    tail = tpl[tpl.find('<div class="faq"'):]

    body = ""
    for sid, h2, kick, blurb, keys in SECTIONS:
        body += f'\n<h2 id="{sid}">{h2}</h2>\n  <p class="cat-kicker"><strong>{kick}</strong> &mdash; {blurb}</p>\n'
        body += '  <div class="products-grid">\n' + "\n".join(card(k) for k in keys) + "\n  </div>\n"

    writeup = """<p>A white golf tee is the least forgiving thing you can put on. There is no
pattern hiding the cut, no colour flattering the cloth, and every wash shows. Which is exactly why it
rewards doing properly: the good ones are obvious and so are the bad ones.</p>

<p>The reference here is less golf than it is the plain American tee &mdash; heavyweight jersey, boxy
through the body, a graphic that either earns its place or is not there at all. What has changed is
who is making them. Five of the seventeen below come from labels that have never appeared on this
site, and two of those are better than anything the established names shipped this year.</p>

<p>Who it is for: the golfer who wants one shirt that works for the range, the round and the drive
home, and would rather it not announce a brand from forty yards. Seventeen tees, one per label, every
price and size checked against the brand&rsquo;s own store this week. They run from thirty-five euro
to a hundred and two dollars, and the cheapest one is not the worst one.</p>

<p>Two things to know before you click. Radry makes exactly one pale tee and it is down to two sizes,
so that one is a race. And Metalwood is the only label here with real depth in white, which is why it
is the single card carrying two shirts rather than two cards carrying one each.</p>"""

    # head: swap identity fields
    h = head
    h = re.sub(r"<title>.*?</title>", f"<title>{TITLE} &mdash; The Grassy Issue</title>", h, flags=re.S)
    for pat, val in [(r'(<meta name="description" content=")[^"]*(")', DESC),
                     (r'(<meta property="og:description" content=")[^"]*(")', DESC),
                     (r'(<meta name="twitter:description" content=")[^"]*(")', DESC),
                     (r'(<meta property="og:title" content=")[^"]*(")', TITLE),
                     (r'(<meta name="twitter:title" content=")[^"]*(")', TITLE)]:
        h = re.sub(pat, lambda m, v=val: m.group(1) + v + m.group(2), h)
    for pat in [r'(<meta property="og:url" content="https://thegrassyissue\.com/drops/)[^"]*(")',
                r'(<link rel="canonical" href="https://thegrassyissue\.com/drops/)[^"]*(")']:
        h = re.sub(pat, lambda m: m.group(1) + SLUG + m.group(2), h)
    h = re.sub(r'(<meta property="og:image" content="https://thegrassyissue\.com)[^"]*(")',
               lambda m: m.group(1) + "/images/whitetee26/hero.jpg" + m.group(2), h)
    h = re.sub(r"<h1[^>]*>.*?</h1>", f"<h1>{TITLE}</h1>", h, flags=re.S)
    h = re.sub(r'(<div class="drop-meta">).*?(</div>)',
               lambda m: m.group(1) + "Drops &amp; Brands &middot; 29 August 2026 &middot; 17 pieces &middot; $35&ndash;$102" + m.group(2), h, flags=re.S)
    h = re.sub(r'(<div class="drop-hero-img">\s*<img[^>]+src=")[^"]*(")',
               lambda m: m.group(1) + "/images/whitetee26/hero.jpg" + m.group(2), h)
    h = re.sub(r'(<div class="drop-hero-img">\s*<img[^>]+alt=")[^"]*(")',
               lambda m: m.group(1) + "White golf tees from Odd Ritual, Metalwood Studio and Criquet" + m.group(2), h)
    # Breadcrumb. The last crumb is bare text after the final separator, INSIDE
    # the breadcrumb element. A loose `&rsaquo;` regex matched the CSS rule in the
    # <style> block instead and left "The Niche Grip Report" visible on the page.
    # The separator is <span>/</span>, not an &rsaquo; entity — the final crumb is
    # the bare text node after the LAST closing </span>.
    def _crumb(m):
        inner = m.group(2)
        k = inner.rfind("</span>")
        if k >= 0:
            inner = inner[:k + len("</span>")] + "\n  White Tee Edit"
        return m.group(1) + inner + m.group(3)
    for tag in ("nav", "div"):
        h = re.sub(rf'(<{tag} class="breadcrumb"[^>]*>)(.*?)(</{tag}>)', _crumb, h,
                   count=1, flags=re.S)

    # Sidebar. The template's rows are the grip report's ("Brands 5", a grips
    # price range, #GolfGrips) and nothing in the head-swap touched them.
    rows = ('<div class="sidebar-detail"><span class="l">Brands</span><span>17</span></div>\n'
            '      <div class="sidebar-detail"><span class="l">Countries</span><span>9</span></div>\n'
            '      <div class="sidebar-detail"><span class="l">Range</span><span>&euro;35&ndash;$102</span></div>\n'
            '      <div class="sidebar-detail"><span class="l">New to TGI</span><span>5 brands</span></div>\n'
            '      <div class="sidebar-detail"><span class="l">Checked</span><span>Aug 2026</span></div>\n      ')
    h = re.sub(r'(<div class="sidebar-label">Details</div>\s*)(?:<div class="sidebar-detail">.*?</div>\s*)+',
               lambda m: m.group(1) + rows, h, count=1, flags=re.S)
    tags = ("".join(f'<span class="hashtag">#{t}</span>\n        '
                    for t in ("TheGrassyIssue", "WhiteTee", "IndependentGolf", "GolfStyle"))).rstrip() + "\n      "
    h = re.sub(r'(<div class="hashtags">\s*)(?:<span class="hashtag">.*?</span>\s*)+',
               lambda m: m.group(1) + tags, h, count=1, flags=re.S)
    h = re.sub(r'(<div class="writeup-body">).*?(</div>\s*<aside)',
               lambda m: m.group(1) + writeup + m.group(2), h, flags=re.S)

    faqs = [("What is the best white golf tee in 2026?",
             "It depends what you want it to do. For a blank tee, Criquet's natural slub pocket tee at $64 and Siegelman Stable's 13oz embroidered classic at $102 are the two best-made here. For a graphic, Metalwood Studio's Rorschach at $54 and Odd Ritual's Odd Birdie are the strongest designs."),
            ("Which golf brands make a plain white tee with no logo?",
             "Huega House's Essential Tee in cream and 3 Putt Round's Who's Your Caddy are the closest to blank. Criquet, Siegelman Stable and ANTi Country Club Tokyo all carry only a small tonal mark or embroidery."),
            ("What is the cheapest good white golf tee?",
             "Rebolf's Rodeo White Tee at 35 euro, out of Barcelona. It has a burgundy ringer collar and a cowboy-golfer illustration, and it is the only ringer in this roundup."),
            ("Are any of these tees not from golf brands?",
             "All seventeen are golf labels or golf-adjacent. Badlands is a New Jersey shop that now makes its own, and No Laying Up's tee is a collaboration with Field Day for the Western Golf Association, which funds the Evans Scholarship for caddies."),
            ("Why is Metalwood Studio the only brand with two tees?",
             "Metalwood is the only label in this roundup carrying real depth in white. Rather than give it two entries, the Rorschach and the Stonehenge share one card at $54 and $62."),
            ("Do white golf tees actually stay white?",
             "Not without help. Garment-dyed and slub bodies like Seamus and Criquet hide wear better than optic white. Wash cold, dry flat, and treat grass early rather than after the round.")]
    faq_html = ('<div class="faq">\n' + "\n".join(
        f'    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs) + "\n  </div>")
    tail = re.sub(r'<div class="faq">.*?</div>\s*(?=</section>|<section|<div class="more)', faq_html + "\n  ",
                  tail, count=1, flags=re.S)

    out = h + '<section class="products">\n' + body + "\n" + tail
    p = os.path.join(ROOT, "drops", SLUG + ".html")
    open(p, "w", encoding="utf-8").write(out)
    print(f"wrote {p}")
    ncards = out.count('class="product-card"')
    print(f"  cards: {ncards}   sections: {out.count('<h2 id=')}")
    print(f"  words: {len(re.sub(r'<[^>]+>',' ',out).split())}")

if __name__ == "__main__":
    build()
