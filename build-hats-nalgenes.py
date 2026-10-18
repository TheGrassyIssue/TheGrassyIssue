#!/usr/bin/env python3
"""build-hats-nalgenes.py — "Golf Hats and Nalgenes: 37 Thoughtful Picks Under $70", 17 October 2026.
Revision 2: Lazyface out ("No on lazyface") -> Sugarloaf Social Club SSC Arrow cap (4 in-stock colors); "add Huega House" ->
Athletic Association Hat, 5 colors in one box; new hero (Agronomy Workshop campaign image, "needs a different hero image").
Revision (Lenny, same day): "condense the hats section down to two sections and provide less draw options and condense the
colorways into one box" -> Draw is two cards (corduroy, 3 colors; ripstop, 6 colors) with every colorway in one gallery.
Lenny: "a post about Hats & Nalgenes - two cheap ways to have something thoughtful on and off the course." His picks: Draw hats,
Canto Double Overhead + Brain Dead x Sound & Fury Nalgenes; "I like all the bottles" (Golf Wang Quake dropped: listing never says
Nalgene and its photo shows an FC Barcelona print); hats: no Golf Wang / Brain Dead caps, yes Canto tree camo, Parmore ripstop,
Agronomy Workshop, "other design forward brands".
FACTS: each brand's own store (price + stock 17 Oct 2026) and product copy (research/hats-nalgenes/picks.json).
PHOTOS: each brand's own product photos (research/hats-nalgenes/frame.py). Hero: Agronomy Workshop campaign image.
"""
import html as H, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"
TITLE = "Golf Hats and Nalgenes: 37 Thoughtful Picks Under $70"
DESC = "Golf hats and Nalgene bottles from independent brands like Draw, Agronomy Workshop, Parmore, Canto and Mustard Beetle: 37 thoughtful picks under $70."
H1 = "Hats &amp; Nalgenes: Two Cheap Ways to Carry Something Thoughtful"
BC = "Hats &amp; Nalgenes"
SLUG = "golf-hats-and-nalgenes"
IMG = "/images/hats-nalgenes"
DATE = "2026-10-17"
PK = json.loads((ROOT / "research/hats-nalgenes/picks.json").read_text())
FR = json.loads((ROOT / "research/hats-nalgenes/frames.json").read_text())
COLORS = {0: ["Forest green", "Off-white", "Deep navy"], 3: ["Khaki green", "Brown", "Lilac", "Cobalt blue", "Copper orange", "Off-white and midnight navy"],
          15: ["Nantucket red", "Lavender", "Lemon ice", "Snow white"], 44: ["Green and natural", "Maroon and natural", "Khaki and natural", "Brown", "Black"]}
FR[0] = [FR[i][0] for i in (0, 1, 2)]
FR[3] = [FR[i][0] for i in (3, 4, 5, 6, 7, 8)]
PK[0]["sec"] = PK[3]["sec"] = "on"
PK[3]["url"] = "https://drawgolf.co/collections/all-products"
DROP = {41, 1, 2, 4, 5, 6, 7, 8}   # 41 = Golf Wang Quake bottle; Draw colorways folded into cards 0 and 3
FR[14] = FR[14][:2]             # Mogshade: third frame is a stark white close-up
RATE = {"GBP": 1.34, "EUR": 1.16, "AUD": 0.70}
def money(c, x):
    sym = {"GBP": "&pound;", "EUR": "&euro;", "AUD": "A$"}.get(c)
    if sym: return f"{sym}{x:,.0f} (~${round(x*RATE[c])})"
    return f"${x:,.2f}" if x % 1 else f"${x:,.0f}"
def price(p):
    s = money(p["cur"], p["price"])
    if p.get("cmp") and p["cmp"] > p["price"]: s += f" (reg. {money(p['cur'], p['cmp'])})"
    return s
NAMES = {  # display names, index-aligned with picks.json
 0: "Unstructured Corduroy Cap, 3 colors", 1: "Off-White Corduroy Cap", 2: "Deep Navy Corduroy Cap", 3: "Unstructured Ripstop Cap, 6 colors",
 4: "Brown Ripstop Cap", 5: "Lilac Ripstop Cap", 6: "Cobalt Blue Ripstop Cap", 7: "Copper Orange Ripstop Cap",
 8: "Off-White &amp; Midnight Navy Ripstop Cap", 9: "Tree Hat", 10: "Golf Brand&copy; Hat", 11: "Agronomy Workshop Hat",
 12: "+ Ripstop Cotton 5-Panel", 13: "Monogram Nylon Dad Hat", 14: "Only Human Cap", 15: "SSC Arrow Cotton Cap, 4 colors", 16: "Logo Cap, Stone",
 17: "Field Notes 6-Panel Dad Hat", 18: "Corduroy Script Cap", 19: "Vintage Patch Two-Tone Hat", 20: "Forest Green Embroidered Hat",
 21: "Cyco Vision Snapback, Tree Camo", 22: "1936 Tokyo Giants Wool Mesh Trucker", 23: "Club Cap, Acorn Corduroy",
 24: "Quail Ball Cap", 25: "Sol Cap, Olive", 26: "ACL Fest 2026 Snapback, Midnight Corduroy", 27: "Paneled Nylon Hat, Cool Sage",
 28: "x Sound &amp; Fury 2026 Nalgene, Brown", 29: "Double Overhead 32oz Nalgene", 30: "Lemon Heads 32oz Nalgene",
 31: "Joshua Tree 32oz Nalgene", 32: "Toad 32oz Nalgene", 33: "Monarch 32oz Nalgene", 34: "Hummingbirds 32oz Nalgene",
 35: "Prairie 32oz Nalgene", 36: "Proceed Slow 32oz Nalgene", 37: "Mythology 32oz Nalgene", 38: "Dark Sky Glow-in-the-Dark Nalgene",
 39: "Defend the Parks Nalgene", 40: "Cold Steel Will Forgive My Sins Nalgene", 42: "NY Branches 32oz Nalgene",
 43: "Printed Bottle, Clear (500ml)", 44: "Athletic Association Hat, 5 colors",
}
CARDS = {
 0: "Draw makes this unstructured cap in forest green, off-white and deep navy corduroy, each with a contrast logo, a brushed silver buckle and a small side pouch that holds a tee. Swipe through all three colors.",
 1: "Draw makes the off-white corduroy cap with a blue embroidered logo, the tee pouch on the side and a brushed silver buckle at the back.",
 2: "Draw pairs deep navy corduroy with a pastel yellow logo here. Unstructured, so it folds into a bag pocket without complaint.",
 3: "Draw makes the ripstop nylon snapback in six colors, from khaki green (&ldquo;hidden on the fairway&rdquo;) and lilac to an off-white crown on a navy brim, every one with the tee pouch. In the US, Soft Hands Club stocks several colors at $39.",
 4: "Draw sells the brown ripstop with a blue logo and calls it &ldquo;camo in the trees.&rdquo;",
 5: "Draw makes this lilac ripstop snapback with a white logo and the same side pouch for a tee. The product page names it &ldquo;Lilac a Pro.&rdquo;",
 6: "Draw cuts this cobalt blue ripstop cap with a white logo for, in the brand&rsquo;s words, &ldquo;blue sky birdie vibes.&rdquo;",
 7: "Draw makes the copper orange ripstop with a white logo and a snapback. It is the brightest of the nine.",
 8: "Draw puts an off-white ripstop crown on a midnight navy brim with a red logo, the most classic-looking cap in its range.",
 9: "Agronomy Workshop prints 90% AIR on the Tree Hat, a 5-panel rope cap in recycled nylon with a golf pencil holder on the side and a pencil in the box.",
 10: "Agronomy Workshop puts its Golf Brand&copy; mark on black recycled nylon, with matching rope across the front and a quick-adjust rope closure.",
 11: "Agronomy Workshop sells its own name on navy recycled nylon, with the same pencil holder and pre-curved brim as the rest of the line.",
 12: "Parmore turns its &ldquo;+&rdquo; cross mark into raised 3D embroidery on a warm charcoal ripstop cotton crown, with a shorter brim and a velcro strap.",
 13: "Quiet Golf makes its monogram dad hat in unstructured 100% nylon with a slightly curved bill and a velcro closure.",
 14: "Mogshade made this waterproof 5-panel camper cap with artist David Shillinglaw and Eritage. A small woven patch sits on the front.",
 15: "American Needle builds this cotton cap for Sugarloaf Social Club, with the woven SSC Arrow on the front and a small red Sugarloaf label on the back. Swipe for the four colors in stock.",
 16: "Sounder brought back the six-panel cotton cap from its debut collection, with a small wordmark patch on the front.",
 17: "Gumtree Golf &amp; Nature Club and Puma embroider two pumas in motion across this unstructured cotton dad hat. On sale.",
 18: "Radmor makes the Script Cap in 8-wale cotton corduroy with its name embroidered in script across the front.",
 19: "Seamus makes this OTTO 5-panel in cream with its Far and Sure circular patch on the front and a red bill.",
 20: "Whim makes its cap in bio-washed cotton chino twill with a white script logo and an adjustable brass closure.",
 21: "Canto makes the Cyco Vision snapback in tree camo with orange embroidery, a lightly structured mid crown and a snap closure.",
 22: "Ebbets Field Flannels builds this trucker from wool broadcloth with vintage mesh at the back and the crest from the 1936 Tokyo Giants uniform.",
 23: "Battenwear makes the Club Cap in the USA from 14-wale cotton corduroy with a leather patch, built for surf mornings and coffee runs.",
 24: "Mustard Beetle embroiders one of its own illustrations, a quail, on a cotton dad hat. A limited edition that ships flat and plastic free.",
 25: "Hikerdelic makes the Sol Cap in recycled nylon as a mid-profile, unstructured snapback with a sun on the front.",
 26: "Austin&rsquo;s Howler Bros made this corduroy snapback for ACL Fest 2026, the cap you can wear to Zilker Park and the muni the next morning.",
 27: "District Vision makes this hat in 75gsm nylon with a DWR finish for rain, a self-fabric strapback and its symbol printed on the front.",
 28: "Brain Dead put its logohead artwork on official Sound &amp; Fury Festival 2026 merch, a 32oz Nalgene with a tethered lid and carry loop.",
 29: "Canto prints Double Overhead on a 32oz wide mouth Nalgene that glows in the dark, with four exclamation marks in the listing to prove it.",
 30: "Canto puts its Lemon Heads graphic on a 32oz wide mouth Nalgene. Allow seven to ten days to ship.",
 31: "Mustard Beetle screenprints a whole desert on this one: cactus wren, desert tortoise, chuckwalla and a Joshua Tree among the monzogranite of Jumbo Rocks.",
 32: "Mustard Beetle draws a toad among amanita mushrooms, ferns, snails and beetles, now on a woodsman bottle with a gold lid.",
 33: "Mustard Beetle screenprints narrowleaf milkweed covered in monarchs at every stage, from eggs and caterpillars to chrysalis and butterflies.",
 34: "Mustard Beetle draws nesting hummingbirds among flowering passionflower on a 50% recycled bottle made in the USA.",
 35: "Mustard Beetle puts a prairie warbler among fireweed, goldenrod and coneflower on this bottle, now sold only with a periwinkle lid.",
 36: "Topo Designs carries Pine Printshop owner Garrett Danielson&rsquo;s Proceed Slow graphic, a trail bottle for birders, on a custom 32oz Nalgene.",
 37: "Otso Cycles commissioned Portland illustrator Mary Lytle for this 32oz bottle, drawn from her bike adventures and a love of biodiversity.",
 38: "Parks Project prints the night sky on a recycled 32oz Nalgene that glows in the dark. On sale.",
 39: "Parks Project makes this bottle for its Defend the Parks campaign and points buyers to the NPCA to help national parks.",
 40: "Crust Bikes makes this mocha 32oz bottle with a dark berry cap in the USA and sells a Nitto cage to carry it on a bike.",
 42: "Gumtree Golf &amp; Nature Club makes this 32oz with Nalgene in the USA from 50% recycled content, in navy and clear. On sale at Soft Hands Club.",
 43: "And Wander worked with illustrator Yu Nagaba and Nalgene on this 500ml clear bottle. The splurge here, shipped from Australia by Maple Store.",
 44: "Huega House makes the Athletic Association Hat in cotton with a structured front and a high profile. The Carlsbad label was started in 2022 by Jonathan Ruley and former NFL player Jake Ryan, and named for the Danish idea of hygge.",
}
BRANDLINK = {"Agronomy Workshop": "/brands/agronomy-workshop", "Parmore": "/drops/brand-to-know-parmore-golf", "Quiet Golf": "/drops/brand-to-know-quiet-golf",
             "Mogshade": "/drops/brand-to-know-mogshade", "Sugarloaf Social Club": "/brands/sugarloaf-social-club", "Sounder": "/drops/brand-to-know-sounder",
             "Gumtree Golf & Nature Club × Puma": "/drops/brand-to-know-gumtree-golf-and-nature-club", "Radmor": None, "Seamus": "/brands/seamus",
             "Whim Golf": "/brands/whim-golf"}
GROUPS = [
 ("on", "Hats for the Course", "Fourteen caps from golf labels with a point of view.", None),
 ("off", "Hats for Everywhere Else", "Eight from baseball, surf, running and festival makers.", None),
 ("art", "Nalgenes With Art on Them", "Nine bottles drawn by illustrators and printmakers.", None),
 ("brand", "Nalgenes From Brands We Like", "Six from streetwear, parks, bikes and one golf club.", None),
]
PQ = {
 "on": ("Sweat it out on the back nine, then wear it everywhere else.", "Parmore, on its ripstop cap"),
 "brand": ("The pleasure of playing in the mountains", "And Wander&rsquo;s founding idea"),
}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Two things go to every round with you: something on your head and something to drink from. They are also the cheapest way into the brands we like. A cap or a 32oz Nalgene costs less than most shirts, and both get seen more: on the first tee, in the cart and on your desk come Monday morning.</p>
    <p>The good ones are thoughtful in small ways. Draw sews a pouch into the side of every cap to hold a tee. Agronomy Workshop builds a pencil holder into its rope hats and puts the pencil in the box. Ebbets Field Flannels stitches the crest of the 1936 Tokyo Giants onto a wool trucker. None of that costs much, and all of it gives you something to talk about with whoever you&rsquo;re paired with.</p>
    <p>The Nalgene is the same idea in plastic. The 32oz wide-mouth bottle is a plain, familiar shape, which makes it a good blank canvas. Illustrators like Mustard Beetle screenprint whole ecosystems around it, Canto and Parks Project make theirs glow in the dark, and Brain Dead turned one into festival merch. Fill it at the turn, carry it to work, and it says more about you than another branded tumbler.</p>
    <p>Here are 22 hats and 15 bottles, every one in stock and under $70 when we checked on October 17, 2026.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Picks</div>
      <div class="sidebar-detail"><span class="l">Course hats</span><span>14 from golf labels</span></div>
      <div class="sidebar-detail"><span class="l">Everywhere hats</span><span>8</span></div>
      <div class="sidebar-detail"><span class="l">Nalgenes</span><span>15</span></div>
      <div class="sidebar-detail"><span class="l">Range here</span><span>$17&ndash;$66</span></div>
      <div class="sidebar-detail"><span class="l">Prices</span><span>Checked October 17, 2026</span></div>
      <a href="/brands" class="sidebar-cta">The Brand Index &#8599;</a>
      <div class="hashtags"><span class="hashtag">#GolfHats</span><span class="hashtag">#Nalgene</span><span class="hashtag">#IndependentGolf</span></div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
FAQ = [
 ("What are the best golf hats under $70?", "Our picks include Draw's unstructured corduroy and ripstop caps, Agronomy Workshop's rope hats, Parmore's ripstop 5-panel, Quiet Golf's nylon monogram dad hat, Canto's tree camo snapback and Ebbets Field Flannels' 1936 Tokyo Giants trucker, all priced on October 17, 2026."),
 ("Which golf hats hold a tee or a pencil?", "Every Draw cap has a tee holder side pouch. Agronomy Workshop's 5-panel rope hats have a golf pencil holder and come with a pencil."),
 ("Which Nalgene bottles glow in the dark?", "Canto's Double Overhead 32oz wide mouth Nalgene and Parks Project's Dark Sky 32oz Nalgene both glow in the dark."),
 ("Where can I buy an artist-designed Nalgene?", "Mustard Beetle sells screenprinted 32oz Nalgenes of its own nature illustrations for $30. Topo Designs sells a Pine Printshop bottle and Otso Cycles sells one drawn by Mary Lytle."),
 ("What is the cheapest pick?", "Crust Bikes' Cold Steel Nalgene at $17 and Parks Project's Dark Sky bottle at $19.99 on sale. The cheapest hat is Mustard Beetle's Quail cap at $30."),
]
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-GT-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}'
            '.ad-group{text-align:center;padding:64px 0 8px;border-top:.5px solid var(--ink);margin-top:40px}.ad-group h2{font-size:clamp(30px,4vw,44px);margin:10px 0 8px}.ad-group p{max-width:680px;margin:0 auto;opacity:.75}.ad-more{display:block;text-align:center;font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;margin:18px 0 0}.ad-more a{border-bottom:1px solid currentColor}</style>\n')
def disp_brand(p):
    return H.escape(p["brand"]).replace("&amp;", "&amp;")
def card(i, idx):
    p = PK[i]; fr = FR[i]; name = p["brand"]
    label = H.unescape(f"{name} {NAMES[i]}").replace('"', "")
    alt = (lambda k: f"{H.escape(label)} in {COLORS[i][k].lower()}") if i in COLORS else (lambda k: f"{H.escape(label)} &middot; view {k+1} of {len(fr)}")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{alt(k)}" loading="lazy" /></div>' for k, f in enumerate(fr))
    dots = "".join(f'<button class="pg-dot{" on" if k == 0 else ""}" data-i="{k}" aria-label="View image {k+1}"></button>' for k in range(len(fr)))
    more = BRANDLINK.get(name)
    desc = CARDS[i] + (f' <a href="{more}" style="border-bottom:1px solid currentColor">More on {H.escape(name.split(" ×")[0])}</a>.' if more else "")
    return (f'<div class="product-card" id="p-{idx}" data-frames="{len(fr)}"><div class="product-gallery"><div class="pg-track">{imgs}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button><button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{len(fr)}</span><div class="pg-dots">{dots}</div></div>'
            f'<div class="product-body"><div class="product-brand">{disp_brand(p)}</div><div class="product-name">{NAMES[i]} &middot; {price(p)}</div>'
            f'<div class="product-desc">{desc}</div><a href="{p["url"]}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')
def pq(k):
    q, who = PQ[k]
    return f'\n<div class="pull-quote" style="margin:56px auto 24px">\n  <div class="pull-quote-inner">&ldquo;{q}&rdquo;<span class="pull-quote-attr">&mdash; {who}</span></div>\n</div>\n'
def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>' for q, a in FAQ)
    return f'\n<section class="products" style="border-top:none;padding-top:48px">\n  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n'
def head_top(items):
    og = f"https://thegrassyissue.com{IMG}/btk-og.jpg"
    blocks = [
     {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC, "url": URL, "image": og, "datePublished": DATE, "dateModified": DATE,
      "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington", "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
      "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"}, "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
     {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
     {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": items},
     {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
      {"@type": "ListItem", "position": 2, "name": "Drops & Brands", "item": "https://thegrassyissue.com/#feed"}, {"@type": "ListItem", "position": 3, "name": H.unescape(BC), "item": URL}]}]
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
def main(apply_):
    order = {g[0]: [i for i, p in enumerate(PK) if p["sec"] == g[0] and i not in DROP] for g in GROUPS}
    n_tot = sum(len(v) for v in order.values())
    assert n_tot == 37, n_tot
    for i in range(len(PK)):
        if i in DROP: continue
        assert i in NAMES and i in CARDS, i
        for f in FR[i]: assert (ROOT / f.lstrip("/")).is_file(), f
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>October 17, 2026</span><span class="dot"></span>
    <span>22 hats &middot; 15 bottles</span><span class="dot"></span>
    <span>Prices checked October 17, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/btk-hero.jpg" alt="A hand adjusting a black Agronomy Workshop rope hat with a pencil tucked into its side holder" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1; items = []
    for key, h2, sub, intro in GROUPS:
        if key in PQ: body += pq(key)
        body += f'\n<section class="ad-group" id="{key}"><div class="drop-tag grass">{len(order[key])} picks</div><h2>{h2}</h2><p>{sub}</p></section>\n'
        body += '\n<section class="products" style="margin-top:8px;">\n'
        if intro: body += f'  <p class="cat-kicker">{intro}</p>\n'
        body += f'  <div class="products-grid" data-n="3">\n'
        for i in order[key]:
            body += card(i, n) + "\n"
            items.append({"@type": "ListItem", "position": n, "name": H.unescape(f'{PK[i]["brand"]} {NAMES[i]}'), "url": PK[i]["url"]})
            n += 1
        body += '  </div>\n'
        body += '</section>\n'
    body += faq_html()
    out = head_top(items) + head_rest.replace("</head>", GRID_CSS + "</head>", 1) + body + tail
    print(f"  {n-1} cards")
    if not apply_: print("  dry run"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    bad = []
    for leak in ("Mackem", "Kalamunda", "Howie"):
        if leak in above: bad.append("leak " + leak)
    if fin.count('class="product-card"') != 37: bad.append("card count")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", above), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides|brands)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")
if __name__ == "__main__":
    main("--apply" in sys.argv)
