#!/usr/bin/env python3
"""
Builds /drops/the-all-black-edit.

Eighteen genuinely all-black men's/unisex pieces, one per brand, head to toe.

COLOUR RULE APPLIED: true black only. Charcoal, gunmetal, washed grey and
near-black navy were all rejected on sight of the product photo, not on the
strength of the colourway name. Cut for failing it: Siegelman (garment-washed
charcoal), Radry (faded tee), Found Golf (washed Box Crew), Artisan (Gunmetal),
Devereux's Anorak (Black/Graphite colourblock), Malbon's jackets (blue zips,
white panels), Kingfisher's black polo (grey pinstripes), Royal Albartross
(every men's shoe has a contrast sole, welt or heel counter), BestGrips (the
"black" ostrich cover photographs green), Lamb Crafted (no isolatable black
frame), Fyfe (cover is half white shearling).

IMAGE RULES (Lenny, 2026-08-27):
  1. No black backgrounds. Two frames were dropped for this — metalwood-1 and
     random-golf-club-1. Sun Mountain shoots against a black backdrop strip, so
     those frames are auto-cropped to the light region before normalising.
  2. Staged and on-model photography leads; blank-background packshots move to
     the back of the gallery. Ten products were reordered on this basis.
  Eight products are studio-only because no staged photography exists anywhere:
  clint-orms, devant, duca-del-cosma, jones, malbon, piretti, seamus,
  sun-mountain. Small leather goods and headcovers never get lifestyle shoots.

SUN MOUNTAIN: CUT ENTIRELY (2026-08-27). Tried the Legacy Leather Stand Bag,
then the Matchplay Ballistic 14-way. Both fail the no-busy-background rule at
source: Sun Mountain shoots its black bags against a corrugated-metal backdrop
with hard black bands running through frame. Cropping to the light region left
band remnants; cropping to the bag's bounding box could not separate them
because the bands overlap the product. There is no clean black Sun Mountain
image to use. Jones Sports Co covers the bag slot.

METALWOOD: Lenny specifically asked for the QUARTER ZIP JERSEY POLO. It has a
white collar and cuffs, the only contrast trim in the post. Kept on his call.

GAPS THAT ARE REAL, NOT OVERSIGHTS: no black glove exists in the brand universe
(Chipp makes red, blue and green only). Mogshade's Dogleg is the only black
sock (Inside Story's entire catalogue is ivory, white, royal, berry, cream).

HERO: Manors Golf lookbook frame (landscape, 1800x1200), cropped 1600x685 at y-offset
0.25 — golfer in black trousers over a putt with the hillside course behind. Lenny's call,
and he noted the hero does not need to be an all-black composition.
  Heroes must come from LANDSCAPE-composed editorial. A 2.34:1 band cut from a portrait
  product shot always slices through the subject — that is what decapitated the Devereux
  model on the first attempt. Manors, Left of Field and Metalwood all publish lookbooks;
  Manors' are the only ones with landscape frames.

Sold-out product is allowed here — Lenny confirmed restocks are coming on all
brands (2026-08-27). Several picks are currently out of stock.
"""
import json, os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
IMGDIR = os.path.join(ROOT, "images", "all-black")
IMG  = "/images/all-black/"
TPL  = os.path.join(ROOT, "drops", "brand-to-know-midiron.html")
SLUG = "the-all-black-edit"
OUT  = os.path.join(ROOT, "drops", SLUG + ".html")
TITLE = "The All-Black Edit"
TITLE_TXT = "The All-Black Edit"
DESC = ("Nineteen genuinely all-black golf pieces, one per brand, head to toe — Manors trousers, "
        "Metalwood, Odd Ritual, a blacked-out stand bag, Italian shoes and the only black sock "
        "in independent golf. Charcoal need not apply.")

def frames(key):
    fs = sorted(glob.glob(os.path.join(IMGDIR, f"{key}-*.jpg")),
                key=lambda p: int(re.search(r'-(\d+)\.jpg$', p).group(1)))
    return [os.path.basename(f) for f in fs]

def card(key, brand, kicker, name, desc, link):
    fr_files = frames(key)
    n = len(fr_files)
    assert n, f"no frames for {key}"
    fr = "".join(f'<div class="pg-frame"><img src="{IMG}{f}" loading="lazy" '
                 f'alt="{brand} &middot; view {i+1} of {n}"></div>'
                 for i, f in enumerate(fr_files))
    dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" '
                   f'aria-label="View image {i+1}"></button>' for i in range(n))
    return f'''  <div class="product-card" id="{key}" data-frames="{n}">
    <div class="product-gallery"><div class="pg-track">{fr}</div><button class="pg-arw prev" aria-label="Previous image">&#8249;</button><button class="pg-arw next" aria-label="Next image">&#8250;</button><span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>
      <div class="product-body">
        <div class="product-brand">{kicker}</div>
        <div class="product-name">{name}</div>
        <div class="product-desc">{desc}</div>
        <a href="{link}" target="_blank" rel="noopener" class="product-link">Visit {brand} &#8599;</a>
      </div>
  </div>'''

FIT = [
 ("manors", "Manors Golf", "Trousers &middot; &pound;/$163",
  "Lightweight Course Trousers 2.0",
  "The anchor of the whole thing. Four-way stretch, water resistant, cut close enough to read as trousers rather than golf trousers &mdash; which is the entire point of wearing black in the first place. Manors makes a Club Pant too, but it only comes in Earth, Pine Green and Vapour, so this is the one.",
  "https://manorsgolf.com/products/lightweight-course-trousers"),
 ("odd-ritual", "Odd Ritual", "Polo &middot; about $47",
  "Classic Polo",
  "The cheapest thing in the top half and arguably the best value in the post. Deep true black performance polyester, a small wordmark on the left chest, nothing else anywhere. South African, priced in rand, which is why it lands around forty-seven dollars for a polo that would be a hundred here.",
  "https://oddritualgolf.com/products/odd-ritual-classic-polo-black"),
 ("metalwood", "Metalwood Studio", "Jersey polo &middot; $138",
  "Quarter Zip Jersey Polo",
  "Metalwood mostly shouts &mdash; moto graphics, big screen prints, Real Bark Camo. This is the quiet one. Flagging it honestly: the collar and cuffs are white, so it is the only piece here with contrast trim. It earns the slot on cut and fabric, a proper heavyweight jersey knit with a short zip.",
  "https://metalwood.studio/products/quarter-zip-jersey-polo-black"),
 ("devereux", "Devereux Golf", "Knit polo &middot; $88",
  "Phoenician Polo",
  "Textured knit, johnny collar, patch pocket, and a woven neck label doing all the branding. The texture is what makes it &mdash; flat black jersey reads cheap under sun, and a knit like this holds shadow instead of shine.",
  "https://devereuxgolf.com/products/phoenician-polo-black"),
 ("criquet", "Criquet Shirts", "Camp collar &middot; $104",
  "Retro Coach&rsquo;s Players Shirt",
  "The Austin entry, and the least golf-looking garment in the post. Camp-collar popover with a chest flap pocket and no visible logo at all. Wears to dinner without anyone clocking that you played thirty-six.",
  "https://criquetshirts.com/products/retro-coach-s-shirt-black"),
 ("left-of-field", "Left of Field Golf", "Trousers &middot; $225",
  "Stanwell Pleated Wide Trouser",
  "The dressier counterweight to the Manors pant, and the widest leg you will find in golf. Pleated, no front branding, cut to break properly over a shoe. If the Manors trouser is for playing, this one is for the nine holes where you are mostly drinking.",
  "https://lofgolf.com/products/stanwell-pleated-wide-trouser-black-left-of-field-golf"),
 ("malbon", "Malbon Golf", "Crewneck &middot; $248",
  "Studio Seoul Piste Crewneck",
  "Technical piste fabric with a small embroidered mascot patch, which for Malbon counts as restraint. Full size run. The most expensive layer here and the one that will look least like golf on the walk from the car.",
  "https://malbongolf.com/products/studio-seoul-piste-crewneck-black"),
 ("random-golf-club", "Random Golf Club", "Hoodie &middot; $75",
  "City Golf Hoodie",
  "True black fleece, small centred wordmark, and seventy-five dollars. Every blacked-out kit needs one piece you do not care about, and this is it &mdash; the layer that lives in the boot of the car from October onwards.",
  "https://randomgolfclub.com/products/golf-club-hoodie-black"),
 ("fella", "Fella Golf", "Tee &middot; $60",
  "Fella Logo Tee",
  "The plain black tee, done properly. Heavyweight cotton, boxy cut, one small script logo on the chest and nothing on the back. The whole category is usually ruined by a graphic; this is the one that just gets out of the way.",
  "https://fellagolf.com/products/fella-logo-tee-black-1"),
 ("merrill", "Merrill Golf", "Long-sleeve tee &middot; $65",
  "Golf Company LS Tee",
  "The long-sleeve version, for shoulder season and for anyone who has been told about sun damage. Small collegiate wordmark on the chest, true black rather than the washed grey most vintage-styled tees end up as.",
  "https://merrillgolf.com/products/golf-company-ls-tee-black"),
 ("penta", "Penta Golf", "Shorts &middot; $100",
  "Hazard Shorts",
  "The only shorts that survived the colour test. Nylon, belted, with a subtle wordmark on the mesh pocket. Everything else in the category turned out to be charcoal wearing a black name.",
  "https://penta-golf.com/products/hazard-short-black"),
]

FEET = [
 ("duca-del-cosma", "Duca del Cosma", "Shoes &middot; $179",
  "Grado",
  "Solid black spikeless, waterproof, sizes seven to thirteen. Golf Monthly gave it an Editor's Choice. It is also the only shoe in golf we could find that is black all the way through &mdash; no contrast sole, no white midsole stripe, no orange heel counter. That sounds like a low bar. It is not.",
  "https://ducadelcosma.us/products/grado-black"),
 ("mogshade", "Mogshade", "Socks &middot; $14.90",
  "Dogleg Socks, Black",
  "The only black sock in independent golf, and we did look. Inside Story's entire twenty-three-item catalogue is ivory, white, royal blue, berry and cream. Mogshade is Portuguese, usually works in loud azulejo tile prints, and made exactly one thing that fits this post.",
  "https://www.mogshadegolf.com/products/dogleg-socks"),
]

KIT = [
 ("jones", "Jones Sports Co", "Sunday bag &middot; $175",
  "Original Bomber, Black Vinyl",
  "Unstructured, no legs, no cart strap, nothing. Solid black vinyl with no panelling. Jones has been making this shape since 1971 and the black one is the version that disappears entirely behind whatever you are wearing.",
  "https://www.jonessportsco.com/products/black-vinyl-original"),
 ("seamus", "Seamus Golf", "Headcover &middot; $140",
  "Black Suede Leather Driver",
  "Black suede outside, black fleece lining inside, zero printed graphics. Seamus built its name on Pendleton tartan, so the all-black suede is the outlier in their own range &mdash; the one they make for people who do not want the pattern conversation.",
  "https://seamusgolf.com/products/black-tribeca-suede"),
 ("clint-orms", "Clint Orms", "Belt &middot; $350",
  "1&Prime; Tapered Black Ostrich",
  "Clint Orms is a Texas silversmith better known for engraved buckles, which makes the plain black ostrich strap the sleeper. Full-quill, so it has visible follicle texture rather than flat dyed calf. Snap closures, so you can put a buckle on it later and undo all this restraint.",
  "https://clintorms.com/products/1-tapered-full-quill-ostrich-black"),
]

DETAILS = [
 ("huega-house", "Huega House", "Cap &middot; $49",
  "Icon Performance Hat",
  "Structured performance crown, clean black, their best seller. The shape holds rather than collapsing after two rounds, which is most of what separates a forty-nine dollar hat from a twenty dollar one.",
  "https://huegahouse.com/products/black-icon-performance"),
 ("devant", "Devant Sport Towels", "Towel &middot; $19.95",
  "Tour Microfiber Towel",
  "Twenty bucks, solid black waffle weave, centre hang slit. Devant has been making towels since 1976 and holds the licences for the USGA, the PGA of America, the PGA Tour and the LPGA, so this is the same towel as the ones on tour bags with the logos taken off.",
  "https://bagboy.com/collections/devant-towels/products/devant-tour-microfiber-towel"),
 ("piretti", "Piretti Putters", "Putter &middot; $999",
  "Potenza Wide Body, Black Oxide",
  "The one piece of equipment, and the one splurge. Serialised run of one hundred, 11L17 carbon steel in a black oxide finish, right hand only. Black oxide is a gunsmith's finish rather than a paint &mdash; it will wear at the edges over years, which is the point.",
  "https://pirettigolf.com/products/limited-edition-potenza-wide-body-carbon-steel-with-black-oxide-w-ust-graphite-shaft"),
]

def section(hid, h2, strong, kicker, items):
    return (f'<h2 id="{hid}">{h2}</h2>\n'
            f'<p class="cat-kicker"><strong>{strong}</strong>{kicker}</p>\n'
            f'<div class="products-grid">\n' + "\n".join(card(*it) for it in items) + '\n</div>\n')

products = (
 section("fit", "The Fit", "Eleven &middot; polos, tees, trousers, layers",
   "Two trousers because they solve different problems, three collars, two tees, and the shorts that survived. "
   "Everything here was checked against the product photo rather than the colourway name.", FIT)
 + section("feet", "The Feet", "Two &middot; shoes and socks",
   "A short section, and not for lack of looking. Golf makes almost nothing black from the ankle down "
   "without a contrast sole or a cream stripe.", FEET)
 + section("kit", "The Kit", "Three &middot; bag, cover, belt",
   "The hardware, and the section that took the longest to fill. Blacked-out bags are usually let down by "
   "one red zip pull, and blacked-out leather is usually just very dark brown.", KIT)
 + section("details", "The Details", "Three &middot; cap, towel, putter",
   "The last twenty dollars and the first thousand. One of these is the cheapest thing in the post and "
   "one is the most expensive, and they are both doing the same job.", DETAILS)
)

FAQS = [
 ("What are the best all-black golf clothes?",
  "Nineteen pieces are covered here, one per brand. For trousers, Manors' Lightweight Course Trousers 2.0 at $163 or Left of Field's Stanwell pleated wide trouser at $225. For a collar, Odd Ritual's Classic Polo at about $47 or Devereux's textured Phoenician knit at $88. For a layer, Malbon's Studio Seoul piste crewneck at $248 or Random Golf Club's hoodie at $75."),
 ("Are there any genuinely all-black golf shoes?",
  "Very few. Duca del Cosma's Grado at $179 is solid black through the upper and sole. Most black golf shoes have a contrast element somewhere — Royal Albartross's Strider Lite has an orange heel counter and the Tailor brogue has a cream midsole, which is why neither is in this post."),
 ("Which brands make a black golf bag with no contrast trim?",
  "Jones Sports Co's Original Bomber in black vinyl at $175 — unstructured, no legs, no contrast panelling. Most blacked-out bags are undone by a coloured zip pull or a metal logo plate. Sun Mountain makes black bags but photographs all of them against a striped metal backdrop, so we left them out."),
 ("Is there a black golf sock?",
  "Mogshade's Dogleg sock at $14.90 is the only one we found across the whole independent field. Inside Story Socks, the specialist, stocks ivory, white, royal blue, berry red and cream — no black at all."),
 ("What about a black golf glove?",
  "There isn't one, at least not among the independents. Chipp Golf Co makes three gloves and they are red, blue and green. It's the one genuine hole in an all-black kit."),
 ("Why are charcoal and washed-black pieces excluded?",
  "Because they don't sit right next to true black. Garment-washed and vintage-dyed pieces photograph as dark grey, and a charcoal polo against black trousers reads as a mistake rather than a choice. Every piece here was judged from the product photo, not the colourway name."),
 ("What's the cheapest way into an all-black kit?",
  "A Devant Tour microfiber towel at $19.95, Mogshade Dogleg socks at $14.90, and Odd Ritual's Classic Polo at about $47. That's a visible chunk of the look for under a hundred dollars."),
 ("Which piece here is the splurge?",
  "The Piretti Potenza Wide Body in black oxide at $999, a serialised run of one hundred in 11L17 carbon steel, right hand only. After that, Clint Orms' full-quill black ostrich belt at $350."),
 ("Is any of this actually in stock?",
  "Some of it isn't. Several picks — the Metalwood polo among them — are sold out at the time of writing, and we included them anyway because the brands restock. Check the product page before you plan a whole outfit around one piece."),
 ("Does an all-black kit work in summer heat?",
  "Not especially, and Austin in August is the wrong place to argue otherwise. Black absorbs more heat than a light colour in direct sun. The performance-fabric pieces here — the Odd Ritual polo, the Manors trouser, the Penta short — move air better than cotton, but this is a look that makes more sense in shoulder season."),
]

faq_html = "\n".join(f'    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQS)
faq_ld = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
  {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in FAQS]}, ensure_ascii=False)
art_ld = json.dumps({"@context":"https://schema.org","@type":"Article","headline":TITLE_TXT,
 "description":DESC,"author":{"@type":"Organization","name":"The Grassy Issue"},
 "publisher":{"@type":"Organization","name":"The Grassy Issue"},
 "datePublished":"2026-08-27","dateModified":"2026-08-27",
 "mainEntityOfPage":f"https://thegrassyissue.com/drops/{SLUG}"}, ensure_ascii=False)

WRITEUP = '''<div class="writeup">
  <div class="writeup-body">
    <p>All-black is the easiest look in golf to describe and the hardest to actually assemble,
    because roughly half of what the industry sells as black is not black. It is charcoal, or
    gunmetal, or garment-washed to a soft grey, or a navy so deep it only reveals itself next to
    the real thing. Put two of those together on a first tee and the whole idea falls apart.</p>
    <p>So the rule for this one was simple and slightly tedious: open the product photo and look
    at it. Not the colourway name, not the filter, the actual picture. A lot of things did not
    survive that.</p>
    <p>Siegelman&rsquo;s black hoodies are vintage-dyed to a visible faded grey. Devereux&rsquo;s
    Anorak is a black and graphite colourblock. Malbon&rsquo;s jackets all have blue zips or white
    side panels. BestGrips sells a putter cover whose file name says black and whose photograph is
    unmistakably green. Royal Albartross makes handsome shoes and every single men&rsquo;s pair
    has a contrast sole, welt or heel counter. Artisan&rsquo;s darkest putter finish is called
    Gunmetal, which is at least honest.</p>
    <p>What is left is nineteen pieces, one per brand, head to toe &mdash; two trousers, three
    collars, two tees, a hoodie, shorts, shoes, socks, a bag, a headcover, a belt, a cap, a towel and one
    thousand-dollar putter. Two gaps we could not fill and will not pretend otherwise: nobody
    independent makes a black glove, and exactly one brand makes a black sock.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>19</span></div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>19</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$14.90&ndash;$999</span></div>
      <div class="sidebar-detail"><span class="l">Checked</span><span>Aug 2026</span></div>
      <a href="/brands/" class="sidebar-cta">Browse the Brand Index &rarr;</a>
      <div class="hashtags">
        <span class="hashtag">#TheGrassyIssue</span>
        <span class="hashtag">#AllBlack</span>
        <span class="hashtag">#IndependentGolf</span>
        <span class="hashtag">#GolfStyle</span>
      </div>
    </div>
  </aside>
</div>'''

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
           lambda m: f'<script type="application/ld+json">{art_ld}</script>')
head = rep(head, r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "FAQPage".*?</script>',
           lambda m: f'<script type="application/ld+json">{faq_ld}</script>')
head = rep(head, r'(<div class="breadcrumb">.*?<span>/</span>\s*)[^<]*?(</div>)', lambda m: m.group(1) + TITLE_TXT + m.group(2))
head = rep(head, r'<h1>.*?</h1>', f'<h1>{TITLE}</h1>')
head = rep(head, r'<div class="drop-meta">.*?</div>',
           '<div class="drop-meta">\n    <span>19 Pieces</span><span>&middot;</span>'
           '<span>One per brand &middot; True black only &middot; Checked Aug 2026</span>\n  </div>')
head = rep(head, r'<div class="drop-hero"><div class="drop-hero-img"><img src="[^"]*" alt="[^"]*"[^>]*/></div></div>',
           f'<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}hero.jpg" '
           f'alt="A golfer in black Manors trousers standing over a putt, from the Manors Golf lookbook" /></div></div>')
head = rep(head, r'<div class="writeup">.*?</div>\s*</aside>\s*</div>', lambda m: WRITEUP)

tail = rep(tail, r'<div class="more-grid">.*?</div>\s*</section>',
'''<div class="more-grid">
    <a href="/drops/golf-brands-founded-by-women" class="more-card">\n      <div class="more-card-img"><img src="/images/women-founded/hero.jpg" alt="Seventeen Golf Brands Founded by Women" loading="lazy" /></div>\n      <div class="more-card-body"><div class="more-card-name">Seventeen Golf Brands Founded by Women</div><div class="more-card-tag">The Roundup</div></div>\n    </a>
    <a href="/drops/brand-to-know-criquet" class="more-card">\n      <div class="more-card-img"><img src="/images/criquet/austinfc-3.jpg" alt="Criquet, the Austin Label That Rebuilt Grandpas Golf Shirt" loading="lazy" /></div>\n      <div class="more-card-body"><div class="more-card-name">Criquet, the Austin Label That Rebuilt Grandpa&rsquo;s Golf Shirt</div><div class="more-card-tag">Brand to Know</div></div>\n    </a>
    <a href="/drops/brand-to-know-sun-mountain" class="more-card">\n      <div class="more-card-img"><img src="/images/sun-mountain/hero.jpg" alt="Sun Mountain, the Montana Company That Put Legs on the Golf Bag" loading="lazy" /></div>\n      <div class="more-card-body"><div class="more-card-name">Sun Mountain, the Montana Company That Put Legs on the Golf Bag</div><div class="more-card-tag">Brand to Know</div></div>\n    </a>
  </div>
</section>''')

page = head + '<section class="products">\n' + products + '\n<div class="faq">\n' + faq_html + '\n  </div>\n</section>' + tail
open(OUT, "w", encoding="utf-8").write(page)
words = len(re.sub(r'<[^>]+>', ' ', page).split())
n = len(FIT) + len(FEET) + len(KIT) + len(DETAILS)
print(f"wrote {OUT} ({len(page):,} bytes, ~{words:,} words, {n} pieces)")
