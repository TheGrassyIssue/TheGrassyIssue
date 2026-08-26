#!/usr/bin/env python3
"""Build drops/puma-golf-x-realtree-precision-in-the-wild.html

FACT NOTES (source-verified 2026-08-26). Do not "correct" these:
  * This is DROP TWO of a recurring partnership, launched 24 Aug 2026. Not a one-off.
  * Collection name: "Precision in the Wild". Sold at pumagolf.com (COBRA PUMA GOLF's
    Shopify store) — NOT us.puma.com, where a Realtree search returns nothing.
  * Pattern is Realtree LEGACY — new for Realtree's 40th, and the first pattern
    co-designed by founder Bill Jordan with his son Tyler Jordan. NOT Realtree Edge.
  * Drop one (3 Feb 2025) used Realtree EDGE and debuted on RICKIE FOWLER at the
    WM Phoenix Open. That player tie-in is confirmed for 2025 ONLY.
  * NO ambassador is confirmed for the 2026 Legacy drop. Do not imply Fowler wears it.
  * 10 SKUs, all in stock at time of writing. Men's only. $40-$190.
  * Anniversary math: Realtree's own site says 1984 AND 1986 for the Original pattern
    in the same document. Both companies say "40 years" — use that, never a founding year.
  * PUMA has done camo before via Volition America (Gary Woodland's kit) — but licensed
    from Folds of Honor in red/white/blue, not an outdoor-industry pattern.
  * Store names differ from the press release names. Use the STORE names (on the tag).
  * A COBRA-branded "Realtree Golf Cap" 301s to a generic collection — delisted, excluded.
"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
FR   = json.load(open('/tmp/rt-final.json')) if os.path.exists('/tmp/rt-final.json') else {}
IMG  = "/images/realtree-puma/"
TPL  = os.path.join(ROOT, "drops", "brand-to-know-midiron.html")
OUT  = os.path.join(ROOT, "drops", "puma-golf-x-realtree-precision-in-the-wild.html")
SLUG = "puma-golf-x-realtree-precision-in-the-wild"
TITLE = "PUMA Golf &times; Realtree &mdash; Precision in the Wild"
TITLE_TXT = "PUMA Golf × Realtree — Precision in the Wild"
DESC = ("PUMA Golf's second Realtree collaboration landed 24 August 2026 — ten pieces in Realtree Legacy, "
        "a new pattern for the camo company's 40th. All ten, priced and photographed.")
U = "https://www.pumagolf.com/products/"

def card(handle, brand, name, desc, link):
    frames = FR.get(handle, [])
    n = len(frames)
    alt = re.sub(r'&[a-z]+;', '', re.sub(r'<[^>]+>', '', name))
    fr = "".join(f'<div class="pg-frame"><img src="{IMG}{f}" loading="lazy" '
                 f'alt="{alt} &middot; view {i+1} of {n}"></div>' for i, f in enumerate(frames))
    dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" '
                   f'aria-label="View image {i+1}"></button>' for i in range(n))
    return f'''  <div class="product-card" data-frames="{n}">
    <div class="product-gallery"><div class="pg-track">{fr}</div><button class="pg-arw prev" aria-label="Previous image">&#8249;</button><button class="pg-arw next" aria-label="Next image">&#8250;</button><span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>
      <div class="product-body">
        <div class="product-brand">{brand}</div>
        <div class="product-name">{name}</div>
        <div class="product-desc">{desc}</div>
        <a href="{link}" target="_blank" rel="noopener" class="product-link">Shop PUMA Golf &#8599;</a>
      </div>
  </div>'''

B = "PUMA Golf &times; Realtree"

SHOES = [
 ("realtree-avant-tour-spiked-golf-shoes", B, "AVANT Tour Golf Shoes &middot; $190",
  "The most expensive thing in the drop and, deliberately, the least camouflaged &mdash; Warm White and Birch, with the Legacy pattern held back to trim. A spiked tour shoe that reads as a dress shoe until you turn it over.", U+"realtree-avant-tour-spiked-golf-shoes"),
 ("realtree-helsinki-g-spikeless-golf-shoes", B, "HELSINKI G Spikeless &middot; $130",
  "The opposite approach: full Legacy across the whole upper, on PUMA&rsquo;s retro-running silhouette. The best-looking object in the collection and the one piece that works entirely off the course.", U+"realtree-helsinki-g-spikeless-golf-shoes"),
]

APPAREL = [
 ("realtree-fleece-golf-vest", B, "Fleece Golf Vest &middot; $140",
  "Full-pattern fleece with a shawl-ish collar and a yellow Realtree tab at the chest. The most literal translation of a hunting layer into a golf one, and the piece that most justifies the whole exercise.", U+"realtree-fleece-golf-vest"),
 ("realtree-cloudspun-tech-golf-hoodie", B, "CLOUDSPUN Tech Golf Hoodie &middot; $110",
  "Colour-blocked rather than fully patterned &mdash; Dusty Olive or Alpine Snow body with Legacy on the hood and sleeves. CLOUDSPUN is PUMA&rsquo;s soft-handle knit, so this is the comfortable one.", U+"realtree-cloudspun-tech-golf-hoodie"),
 ("realtree-camo-golf-polo-aw26", B, "Camo Golf Polo &middot; $90",
  "Head-to-toe Legacy on a standard PUMA golf polo. This is the piece the collection is really selling: whether you want to stand on a first tee in full bark pattern is the entire question.", U+"realtree-camo-golf-polo-aw26"),
 ("realtree-solid-golf-polo", B, "Solid Golf Polo &middot; $85",
  "The answer for people whose answer to that question is no. Solid Dusty Olive or Warm White with the pattern confined to a collar tip and a woven tab &mdash; the version you can wear to a members&rsquo; club.", U+"realtree-solid-golf-polo"),
 ("realtree-golf-shorts", B, "8&Prime; Golf Shorts &middot; $88",
  "Eight-inch inseam, full Legacy. Pairs with the solid polo if you want the pattern working on one half of you only, which is how PUMA styles it in nearly every lookbook image.", U+"realtree-golf-shorts"),
 ("realtree-performance-golf-tshirt", B, "Performance Golf T-Shirt &middot; $55",
  "The cheapest way in, and the only piece carrying the Realtree antler logo at scale. Alpine Snow or Dusty Olive, no pattern at all &mdash; a co-brand tee rather than a camo one.", U+"realtree-performance-golf-tshirt"),
]

CAPS = [
 ("realtree-tour-golf-cap", B, "Tour Golf Cap &middot; $40",
  "Full Legacy crown with the PUMA wordmark in yellow. Forty dollars is the lowest-commitment way to try the pattern, which is presumably the point.", U+"realtree-tour-golf-cap"),
 ("realtree-precision-golf-cap", B, "Precision Golf Cap &middot; $40",
  "The rope-style alternative &mdash; Alpine Snow crown, Legacy brim, woven PUMA GOLF patch. The more restrained of the two, and the one that will date better.", U+"realtree-precision-golf-cap"),
]

def section(hid, h2, strong, kicker, items):
    return (f'<h2 id="{hid}">{h2}</h2>\n'
            f'<p class="cat-kicker"><strong>{strong}</strong>{kicker}</p>\n'
            f'<div class="products-grid">\n' + "\n".join(card(*it) for it in items) + '\n</div>\n')

QUOTE = ('\n<div class="pull-quote">\n'
         '  <div class="pull-quote-inner">&ldquo;We see golfers and hunters as having a lot in common. A lot of these guys just '
         'love the outdoors and being in the natural environment.&rdquo;'
         '<span class="pull-quote-attr">&mdash; Chris MacNeill, PUMA Golf, on the first Realtree collection</span></div>\n'
         '</div>\n')

products = (
 section("shoes", "The Shoes", "Two pairs &middot; $130&ndash;$190",
   "The clearest statement of the collection&rsquo;s split personality &mdash; one shoe hides the pattern, one is covered in it.", SHOES)
 + QUOTE +
 section("apparel", "The Apparel", "Six pieces &middot; $55&ndash;$140",
   "Three fully patterned, three that keep Legacy to the trim. PUMA has built the range so you can take as much or as little of the camo as you want.", APPAREL)
 + section("caps", "The Caps", "Two &middot; $40 each",
   "The entry point, and historically the piece of any camo collab that actually sells through.", CAPS)
)

FAQS = [
 ("When did the PUMA Golf x Realtree collection drop?",
  "The current collection, called \"Precision in the Wild,\" launched on 24 August 2026. It's the second PUMA Golf × Realtree release — the first arrived on 3 February 2025."),
 ("Where can I buy it?",
  "pumagolf.com, which is run by COBRA PUMA GOLF. One catch: searching us.puma.com for Realtree returns nothing, because the golf business sits on its own store. Golf Galaxy and Worldwide Golf Shops also carry it."),
 ("What camo pattern is this?",
  "Realtree Legacy, which is new. It's built on the dark bark lines of Realtree's Original pattern but with lighter segmented bark, added texture, and warmer greys and browns replacing Original's cooler hardwood tones. It's also the first Realtree pattern co-designed by founder Bill Jordan and his son Tyler Jordan."),
 ("Is this the same as the 2025 Realtree collection?",
  "No, and the difference is the interesting part. The 2025 drop used Realtree Edge in Deep Forest and Rickie Orange and launched at the WM Phoenix Open, the loudest event on Tour. This one is Dusty Olive and Alpine Snow, released in late August with no tournament moment attached."),
 ("Does a tour player wear it?",
  "Rickie Fowler wore the 2025 Edge collection head to toe on the Thursday of the WM Phoenix Open. No player has been confirmed wearing the 2026 Legacy capsule — PUMA's release doesn't name one."),
 ("How many pieces are in the collection?",
  "Ten: two shoes, six apparel pieces and two caps. Prices run $40 to $190. There's no bag, no headcovers, no glove and no rain kit — the 2025 drop had rain gear and a quarter-zip, this one doesn't."),
 ("Is it men's only?",
  "Yes. Apparel runs S–3XL, footwear 7–15, shorts 28–42. There's no women's or junior offering in either drop."),
 ("Why is Realtree doing golf?",
  "Realtree licenses its patterns rather than manufacturing, and golf is an expansion category for it rather than a home one. It also has a Realtree ClubGlider travel bag with Sun Mountain, so PUMA isn't the only golf partner."),
 ("Has PUMA done camo before?",
  "Yes, through Volition America — the line Gary Woodland wears, tied to Folds of Honor. That camo is patriotic red-white-and-blue rather than an outdoor pattern, which is the distinction PUMA leans on with Realtree."),
 ("Which piece should I buy?",
  "If you want one thing: the HELSINKI G at $130, because it works away from the course. If you want the pattern without committing: either cap at $40. If you want the collection's best piece of design: the fleece vest at $140."),
]

faq_html = "\n".join(f'    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQS)
faq_ld = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in FAQS]}, ensure_ascii=False)
art_ld = json.dumps({"@context":"https://schema.org","@type":"Article","headline":TITLE_TXT,
 "description":DESC,"author":{"@type":"Organization","name":"The Grassy Issue"},
 "publisher":{"@type":"Organization","name":"The Grassy Issue"},
 "datePublished":"2026-08-26","dateModified":"2026-08-26",
 "mainEntityOfPage":f"https://thegrassyissue.com/drops/{SLUG}"}, ensure_ascii=False)

WRITEUP = '''<div class="writeup">
  <div class="writeup-body">
    <p>PUMA Golf and Realtree released their second collection together on Monday. It is called
    Precision in the Wild, it runs to ten pieces, and the interesting part is how
    differently it behaves from the first one.</p>
    <p>Drop one, in February 2025, was a spectacle. Realtree Edge, Deep Forest and Rickie Orange,
    and it arrived on Rickie Fowler head to toe on the Thursday of the WM Phoenix Open &mdash;
    the rowdiest stage in professional golf, chosen deliberately. Drop two arrived on a Monday in
    late August in Dusty Olive and Alpine Snow, with no tournament, no player and no noise.</p>
    <p>What it does have is a new pattern. Realtree Legacy was made for the company&rsquo;s
    fortieth anniversary and is the first pattern co-designed by founder Bill Jordan and his son
    Tyler. It takes the dark bark structure of the Original pattern and warms it &mdash; browns
    and warm greys where Original ran cool, with segmented bark lines and drop shadows doing the
    depth work. On a fleece vest it looks like a hunting layer. On a spikeless PUMA runner it
    looks like something else entirely.</p>
    <p>PUMA has form here: the Volition America line has carried camo golf shirts for years, in
    patriotic red, white and blue for Folds of Honor. Realtree gives them the same visual
    language with actual outdoor-industry provenance behind it, which is the argument PUMA
    itself makes &mdash; that plenty of golf brands have dabbled in camo without any of it
    meaning much.</p>
    <p>All ten pieces are below, priced, with PUMA&rsquo;s own photography. Everything was in
    stock when we checked.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Dropped</span><span>24 Aug 2026</span></div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>10</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$40&ndash;$190</span></div>
      <div class="sidebar-detail"><span class="l">Pattern</span><span>Realtree Legacy</span></div>
      <a href="https://www.pumagolf.com/collections/realtree" target="_blank" rel="noopener" class="sidebar-cta">Shop the collection &nearr;</a>
      <div class="hashtags">
        <span class="hashtag">#TheGrassyIssue</span>
        <span class="hashtag">#PUMAGolf</span>
        <span class="hashtag">#Realtree</span>
        <span class="hashtag">#Camo</span>
      </div>
    </div>
  </aside>
</div>'''

CSS = ("\n.pull-quote{max-width:1400px;margin:0 auto;padding:0 32px}"
       "\n.pull-quote-inner{font-family:var(--serif);font-style:italic;font-size:22px;line-height:1.4;"
       "padding:32px 0;margin:0;border-top:.5px solid rgba(20,20,20,.15);"
       "border-bottom:.5px solid rgba(20,20,20,.15);color:var(--grass)}"
       "\n.pull-quote-attr{font-family:var(--mono);font-style:normal;font-size:10px;letter-spacing:.14em;"
       "text-transform:uppercase;color:var(--ink);opacity:.45;margin-top:12px;display:block}"
       "\n@media(max-width:640px){.pull-quote{padding:0 20px}.pull-quote-inner{font-size:18px;padding:24px 0}}\n")

tpl = open(TPL, encoding="utf-8").read()
head, rest = tpl.split('<section class="products">', 1)
_, tail = rest.split('</section>', 1)

def rep(s, pat, new, count=1):
    out, n = re.subn(pat, new, s, count=count, flags=re.S)
    assert n > 0, pat
    return out

head = rep(head, r'<title>.*?</title>', f'<title>{TITLE_TXT} | The Grassy Issue</title>')
head = rep(head, r'<meta name="description" content=".*?"', f'<meta name="description" content="{DESC}"')
head = rep(head, r'<meta property="og:url" content=".*?"', f'<meta property="og:url" content="https://thegrassyissue.com/drops/{SLUG}"')
head = rep(head, r'<meta property="og:title" content=".*?"', f'<meta property="og:title" content="{TITLE_TXT}"')
head = rep(head, r'<meta property="og:description" content=".*?"', f'<meta property="og:description" content="{DESC}"')
head = rep(head, r'<meta name="twitter:title" content=".*?"', f'<meta name="twitter:title" content="{TITLE_TXT}"')
head = rep(head, r'<meta name="twitter:description" content=".*?"', f'<meta name="twitter:description" content="{DESC}"')
head = rep(head, r'<link rel="canonical" href=".*?"', f'<link rel="canonical" href="https://thegrassyissue.com/drops/{SLUG}"')
head = rep(head, r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "Article".*?</script>',
           f'<script type="application/ld+json">{art_ld}</script>')
head = rep(head, r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "FAQPage".*?</script>',
           f'<script type="application/ld+json">{faq_ld}</script>')
head = rep(head, r'(<div class="breadcrumb">.*?<span>/</span>\s*)[^<]*?(</div>)', r'\g<1>' + TITLE_TXT + r'\g<2>')
head = rep(head, r'<h1>.*?</h1>', f'<h1>{TITLE}</h1>')
head = rep(head, r'<div class="drop-meta">.*?</div>',
           '<div class="drop-meta">\n    <span>10 Pieces</span><span>&middot;</span><span>Dropped 24 Aug 2026 &middot; Realtree Legacy</span>\n  </div>')
head = rep(head, r'<div class="drop-hero"><div class="drop-hero-img"><img src="[^"]*" alt="[^"]*"[^>]*/></div></div>',
           f'<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}hero.jpg" '
           f'alt="A golfer in the Realtree Legacy fleece vest from the PUMA Golf collaboration" style="object-position:center center;" /></div></div>')
head = rep(head, r'<div class="writeup">.*?</div>\s*</aside>\s*</div>', WRITEUP)
head = rep(head, r'</style>', CSS + '</style>')

tail = rep(tail, r'<div class="more-grid">.*?</div>\s*</section>',
'''<div class="more-grid">
    <a href="/drops/the-camo-edit" class="more-card"><div class="more-kicker">The Edit</div><div class="more-title">The Camo Edit</div></a>
    <a href="/drops/gumtree-golf-x-puma-the-field-notes-collection-lands" class="more-card"><div class="more-kicker">The Drop</div><div class="more-title">Gumtree Golf &times; PUMA &mdash; Field Notes</div></a>
    <a href="/drops/brand-to-know-sun-mountain" class="more-card"><div class="more-kicker">Brand to Know</div><div class="more-title">Sun Mountain &mdash; the Montana Company That Put Legs on the Golf Bag</div></a>
  </div>
</section>''')

page = head + '<section class="products">\n' + products + '\n<div class="faq">\n' + faq_html + '\n  </div>\n</section>' + tail
open(OUT, "w", encoding="utf-8").write(page)
words = len(re.sub(r'<[^>]+>', ' ', page).split())
print(f"wrote {OUT} ({len(page):,} bytes, ~{words:,} words)")
