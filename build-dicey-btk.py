#!/usr/bin/env python3
"""build-dicey-btk.py — Brand to Know: Dicey Golf. 29 October 2026. Cloned from build-golden-soul-btk.py.
Lenny: "Let's do a brand to know - diceygolf.com" -> options (40) -> "build the post - consolidate the different colorways into one box and pull lots of good lookbook images".
FACTS: diceygolf.com Story, Visit HQ, homepage and product .js copy, read in Chrome 29 Oct 2026 (USD). Founder Dawson Gurley is named by the brand. No press found.
OLD HEADER (Golden Soul):
Lenny: "Let's do a brand to know - goldensoulgolf.com" -> options -> "less bags and more headcovers" -> "let's build it with good lookbook and IRL images" (all 52 from options v2).
FACTS: goldensoulgolf.com About/Mission/Vision + product copy (research/golden-soul/catalogue.json, 28 Oct 2026, USD); Bisque Golf collection page. No founder is published: never name one.
OLD HEADER (Penta):
Lenny: "Let's do a brand to know - https://penta-golf.com/" -> options sheet -> "Lets build the post" (all 20: 14 in stock + 6 sold out).
FACTS: penta-golf.com About + live catalogue (research/penta/catalogue.json, USD, 28 Oct 2026); Monster Children Q&A (Feb 2024).
Founders stay unnamed (the brand never names them). Never "worth".
OLD HEADER (Paré):
Lenny: "Let's do a brand to know - https://pare.golf/collections/all" -> options sheet -> "I want a section about the sold out
stuff, especially the more colorful options and let's also mention that the logo is very similar to prada" + "I love the drawing
of the guy putting". Built from the starred picks + a Paré Boy section + a colorful sold-out section.
FACTS: research/pare/brief.md (about page, MyGolfSpy Aug 2025, Gordon College Jul 2025, Kollective Hustle Jul 2024),
research/pare/catalogue.json (pare.golf live, Oct 27 2026, USD). Home city is NOT published anywhere: never name one.
Left out: the in-stock HYPEGOLF tee with a Tagalog expletive in its name, and the Kapamilya-only (members) pieces.
The Prada point is our observation; the brand's own "The Devil Wears Paré" copy is what we cite. Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Brand to Know: Dicey Golf, Bet-On-Yourself Golf Clothes From Mesa, Arizona"
DESC = ("Dicey Golf is a Mesa, Arizona golf brand founded in 2023 on one idea: bet on yourself. $80 polos, the new Draft Day "
        "collection, casino-chip ball markers and King of Hearts headcovers, with prices.")
H1 = "Brand to Know: Dicey Golf, Golf Clothes for Players Who Go For It"
BC = "Brand to Know: Dicey Golf"
SLUG = "brand-to-know-dicey-golf"
IMG = "/images/dicey-golf"
SHOP = ""
C = "Dicey Golf"
SO = " &middot; sold out"
_CARDS = json.loads((ROOT / "research/dicey/cards.json").read_text())
COPY = {
 "draft-day": "Our pick. The first drop from Dicey&rsquo;s Dynasty Collection: one $80 polo in eight colorways that borrow old team colors. Club Champion is &rsquo;90s hardwood green and gold, Valley Heat is desert purple and orange, Red Zone is old-school Sunday football red and gold, and Vice is black with &rsquo;80s neon pink and aqua. All have checkered rib knit at the collar and cuffs. Swipe for all eight.",
 "cord": "A polo with corduroy on the collar and cuffs, the most fall thing Dicey makes.",
 "fairway": "Subtle green pinstripes on a clean shape, made for the first tee, the clubhouse and the office.",
 "redwood": "Vintage-style brown and cream stripes. Dicey describes it as warm earth tones for the course, the clubhouse or dinner.",
 "heritage": "Bold green and white horizontal stripes with the Dicey script on the chest. The loudest of the striped polos.",
 "cedar": "A brown polo with a textured finish and tipped collar, in the earth tones Dicey keeps coming back to.",
 "evergreen": "A plain dark green polo, the easy one. Dicey pitches it for the course, the office and dinner.",
 "seaside-onyx": "The same minimal textured polo in two colors: Seaside in white and Onyx in black. Swipe for both.",
 "zipper": "A zip-neck polo in four colorways: Sky Drive blue, Lavender Haze, Morning Nine mint and Desert Rose pink. Lightweight and breathable, with an embroidered logo.",
 "check-mate": "An all-over abstract checkered pattern in blue, with a silicone Dicey patch. The one for summer in Arizona.",
 "arizona": "The polo that pairs with Draft Day: a cream body with deep teal, purple and copper trim, Arizona&rsquo;s old-school colors, which Dicey ties to desert sunsets and old-school baseball. A checkered band on the sleeve.",
 "muted": "A subtle all-over pattern in pale blue-green, shown here in a golf cart.",
 "signature": "The Dicey script snapback in eight two-tone colorways, from black and navy to lilac and Carolina blue. The same cream front as the Draft Day polos, with a colored brim to pick up the trim. Swipe for all of them.",
 "wingman": "A snapback with a winged DG crest, in black, navy and green.",
 "rope": "A rope hat with a raised &ldquo;Dialed In&rdquo; script, in olive or green. Dicey calls the look low-key tournament vibes.",
 "yeti": "A blue mesh hat with a Yeti mark, which Dicey says stands for cold-morning tee times.",
 "lodge": "Burnt-orange mesh, a nod to the country club for golfers who prefer pines over fairway fences.",
 "royal-flush": "A bright royal-blue snapback with a white DG monogram.",
 "king-blade": "Playing-card headcovers: King of Hearts in white leather with red stitching, or King of Spades in black. Swipe for both.",
 "king-mallet": "The same King of Hearts and King of Spades designs, cut for a mallet putter.",
 "king-hybrid": "The King cards on a hybrid cover, so the set can match.",
 "darts": "A dartboard ball marker, game-night nostalgia for the green.",
 "eight-ball": "A black 8-ball marker with the Dicey logo on one side.",
 "chips": "A casino chip ball marker in red or white, $5. The most on-brand thing in the store.",
 "high-roller": "A black hoodie with a High Roller graphic, for the cold first tee.",
 "booze-hound": "A green tee with a cartoon hound on the back. The joke is in the name.",
}
P = {k: (C, t, p, u, COPY[k]) for k, t, p, u, _ in _CARDS}
SECTIONS = [
 ("Draft Day", "draft-day", ["draft-day", "arizona", "signature"],
  "<strong>Three pieces &middot; $40&ndash;$80</strong>The Draft Day polo, released October 22, 2026, with the two pieces that wear best alongside it: the retro Arizona polo and the two-tone Signature snapback."),
 ("The Polos", "polos", ["cord", "fairway", "redwood", "heritage", "cedar", "evergreen", "seaside-onyx", "zipper", "check-mate", "muted"],
  "<strong>Ten polos &middot; $80 each</strong>Every Dicey polo costs the same. Stripes, cords, zips and a few loud prints."),
 ("Hats", "hats", ["wingman", "rope", "yeti", "lodge", "royal-flush"],
  "<strong>Five hats &middot; $40 each</strong>Snapbacks, rope hats and mesh, with the colorways grouped together."),
 ("Kings, Darts and Chips", "accessories", ["king-blade", "king-mallet", "king-hybrid", "darts", "eight-ball", "chips", "high-roller", "booze-hound"],
  "<strong>Eight pieces &middot; $5&ndash;$85</strong>The casino side of the brand: playing-card headcovers, game-room ball markers and two pieces for the walk to the car."),
]
N = 26
PQ = {
 "polos": ("Dicey isn&rsquo;t just a brand; it&rsquo;s a mindset.", "Dawson Gurley, founder"),
}
BANDS = {
 "draft-day": ("The world of Dicey", "From Dicey&rsquo;s own campaigns: a roulette table, a leather chair and a golf cart.",
   [("look-lredit-95-of-356", "Two men placing chips on a roulette table, one in a checkered Dicey polo", "Bet on yourself"),
    ("look-lredit-316-of-324", "A man in a Dicey polo leaning back in a leather armchair in a wood-paneled room", "The clubhouse"),
    ("look-lredit-20-of-27-1-4", "Two men laughing in a golf cart on a sunny course", "In the cart"),
    ("look-main-header", "Rows of Draft Day polos on hangers showing their colored collars", "Draft Day, on the rack"),
    ("look-draft-day-mobile-header", "Close-up of Draft Day polo collars in orange, green, blue and pink", "The collars"),
    ("look-polo-1-7ea6964a-7584-4a3", "A man in the cream Arizona Retro polo", "Arizona Retro")]),
 "hats": ("Out in the desert", "Dicey shoots most of its photos around Arizona.",
   [("look-group19-3", "Two people on a desert course, one in a cream jacket with Dicey Golf across the back", "Dicey Golf, across the back"),
    ("look-camo-polo-fixed-2", "A golfer in a camo polo and red hat walking with his bag through dry grass", "Through the rough"),
    ("look-black-hat-2", "A man in a black Dicey hat and green sweatshirt in front of desert grasses", "The black snapback")]),
 "accessories": ("At HQ", "Dicey runs a pro shop at its headquarters in Mesa, open by reservation on weekdays.",
   [("look-dsc02811", "The Dicey Golf HQ pro shop with wood shelves, a green wall and racks of polos", "The HQ pro shop in Mesa"),
    ("look-use-for-fairway", "A black King of Spades headcover on a pink and red casino table", "King of Spades"),
    ("look-wholesale-banner", "Dicey hats on a shelf and polos on a rack", "Hats and polos at HQ")]),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Dicey Golf is a Mesa, Arizona brand built on one line: bet on yourself. Founded in 2023, it makes golf clothes for &ldquo;the players who choose to go for it,&rdquo; and it leans into the risk-and-reward side of the game harder than anyone we&rsquo;ve covered. The ball markers are casino chips, dartboards and 8-balls. The headcovers are playing cards. One of the campaigns is shot at a roulette table.</p>
    <p><strong>The polos.</strong> Underneath the theme is a simple, sensible store. Every polo is $80, and there are a lot of them: stripes, a corduroy-trimmed polo for fall, zip-necks in four pastels, and a run of retro designs. The newest, Draft Day, is one off-white polo in eight colorways that borrow old team colors, from &rsquo;90s hardwood to &rsquo;80s neon. It&rsquo;s the first drop from what Dicey calls the Dynasty Collection.</p>
    <p><strong>The hats and the rest.</strong> Hats are $40, in two-tone snapbacks, rope hats and mesh, and most come in several colors, so we&rsquo;ve grouped the colorways together in one card each. The King of Hearts and King of Spades headcovers come for blades, mallets and hybrids at $50. The ball markers start at $5.</p>
    <p><strong>Where to find it.</strong> Online, or at Dicey&rsquo;s HQ pro shop in Mesa, open weekdays by reservation. Dicey also runs its own tournament, the Dicey Open, at Dobson Ranch in Mesa on December 11, with $2,000 for the winning team.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">At a Glance</div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>2023</span></div>
      <div class="sidebar-detail"><span class="l">Founder</span><span>Dawson Gurley</span></div>
      <div class="sidebar-detail"><span class="l">HQ</span><span>Mesa, Arizona</span></div>
      <div class="sidebar-detail"><span class="l">Motto</span><span>Bet on yourself</span></div>
      <div class="sidebar-detail"><span class="l">Polos</span><span>$80, every one</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Draft Day Polo</span></div>
      <div class="hashtags">
        <span class="hashtag">#DiceyGolf</span>
        <span class="hashtag">#BetOnYourself</span>
        <span class="hashtag">#BrandToKnow</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
STORY = """
<section class="products" data-btk="story" style="margin-top:8px;padding-bottom:48px">
  <div class="drop-tag grass">The Story</div>
  <h2 class="products-hdr" id="story">Play It Safe, or Go For It</h2>
  <div class="writeup-body">
    <p>Dicey tells its own story in a few lines. &ldquo;Golf has always been a game of risk and reward,&rdquo; its Story page says. &ldquo;Every shot asks the same question: play it safe, or go for it? Dicey was created for the players who choose to go for it.&rdquo; The brand was built in 2023 on that single belief, and the name and the dice in the logo follow from it.</p>
    <p>The clothes are made to move off the course too. Dicey says it designs apparel &ldquo;that moves seamlessly from the first tee to whatever comes next, whether that&rsquo;s the clubhouse, a night out, or another round,&rdquo; because &ldquo;the players who go for it shouldn&rsquo;t have to change before the fun starts.&rdquo;</p>
    <p>Founder Dawson Gurley puts it most directly: &ldquo;Dicey isn&rsquo;t just a brand; it&rsquo;s a mindset. It&rsquo;s about trusting yourself, embracing the unknown, and betting on your own game, in golf and in life.&rdquo;</p>
    <p>Three years in, the brand has a headquarters and pro shop in Mesa, a wholesale program for courses and retailers, and its own team tournament. The Draft Day polos, released October 22, are what Dicey calls the first pick from its new Dynasty Collection.</p>
  </div>
</section>
"""
FAQ = []
LOOKBOOK = ""
FRN = json.loads((ROOT / "research/dicey/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-R3-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}</style>\n')
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
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items, pos = [], 1
    for sec in SECTIONS:
        for h in sec[2]:
            items.append({"@type": "ListItem", "position": pos, "url": SHOP + P[h][3], "name": H.unescape(f"{P[h][0]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-10-29", "dateModified": "2026-10-29",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
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
    <span>Brand to Know &middot; Mesa, Arizona &middot; Est. 2023</span><span class="dot"></span>
    <span>26 picks, colorways grouped &middot; checked October 29, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="A golfer in a black Dicey polo finishing his swing among saguaro cactus and desert grass" fetchpriority="high" /></div></div>
"""
    body += TAKE  # Lenny 28 Oct: the story closes the post in place of The Questions
    n = 1
    for s in SECTIONS:
        if s[1] + "-before" in BANDS: body += band(s[1] + "-before")
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
        if s[1] + "-after" in BANDS: body += band(s[1] + "-after")
    body += STORY
    out = head_top() + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<!-- TGI-ONE-FOOTER -->')], flags=re.S)
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
