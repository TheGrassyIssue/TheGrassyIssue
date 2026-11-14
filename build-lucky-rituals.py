#!/usr/bin/env python3
"""build-lucky-rituals.py — Field Notes: Lucky, golf's small rituals. 14 November 2026. Cloned from build-casualist-revisit.py.
Lenny: liked the Agronomy Workshop marker essay -> "something adjacent" -> picked Rituals and superstitions -> options sheet v2 (44) -> "looks good, let's build" (Queens Crest Penny dropped: photo did not show a penny).
FACTS: product data from each store (Shopify .json via browser, 14 Nov 2026); Mint Markers prices move with silver; Ancient Resource Manus Dei page.
Superstition anecdotes are framed as told secondhand. Study: Damisch et al. 2010 Psychological Science; Calin-Jageman & Caldwell 2014 Social Psychology. No FAQ. Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-mackem-golf.html"

TITLE = "Lucky: Golf's Small Rituals, and 43 Objects to Carry Them"
DESC = ("Three coins in the pocket, no ball above a 4, a saint on a chain. Golf's superstitions, whether any of it works, "
        "and 43 lucky objects: real vintage coin markers, saint medals, horseshoes, clovers and dice.")
H1 = "Lucky: Golf&rsquo;s Small Rituals"
BC = "Field Notes: Lucky"
SLUG = "golf-superstitions-lucky-rituals"
IMG = "/images/lucky-rituals"
SHOP = ""
VCC = "Vintage Coin Concepts"
MM = "Mint Markers"
P = {
 # 1. Three coins in the pocket
 "l00": ("Kraken Golf", "Play Bold Lucky Horseshoe Marker", "$89", "https://www.krakengolf.com/products/play-bold-lucky-horseshoe-marker-stainless-steel",
   "A horseshoe in stainless steel, cut as a ball marker. The oldest lucky symbol, made to sit on the green behind your ball."),
 "l01": ("Eastside Golf", "Black/Gold Coin Magnetic Coin Marker", "$25", "https://eastsidegolf.com/products/ep1300101-000-black-gold-coin-magnetic-coin-marker",
   "Eastside&rsquo;s swinging-golfer logo on a black and gold magnetic coin. The cheapest way to start carrying a coin on purpose."),
 "l02": ("Kraken Golf", "The Octopus Coin, Copper", "$99", "https://www.krakengolf.com/products/the-octopus-coin-copper",
   "A copper coin with Kraken&rsquo;s octopus in relief. Copper darkens as it is handled, so the coin you carry for years ends up looking like nobody else&rsquo;s."),
 # 2. Old money
 "l04": (VCC, "1905 Lucky Penny Marker", "$30", "https://vintagecoinconcepts.com/products/las-vegas-ball-markers",
   "A real 1905 Indian Head penny set in a ring stamped LUCKY PENNY (and, for some reason, LAS VEGAS). Our pick: the most literal lucky coin on this page, and more than 120 years old."),
 "l05": (VCC, "1895 U.S. Open Marker", "$30", "https://vintagecoinconcepts.com/products/usga-1895-ballmarker-us-open",
   "A real 1895 Indian Head penny in a ring marking the first U.S. Open, played at Newport that year. The coin was in circulation when the championship began."),
 "l06": (VCC, "1930 Buffalo Nickel Marker", "$30", "https://vintagecoinconcepts.com/products/copper-bobby-jones-ballmarker",
   "A real 1930 Buffalo nickel in a copper ring commemorating the Grand Slam year. In the story told about Chi Chi Rodriguez, his eagle coin was a Buffalo nickel."),
 "l07": (VCC, "1953 Farthing Marker", "$25", "https://vintagecoinconcepts.com/products/ben-hogan-1953-farthing-bm",
   "A real 1953 British farthing, the quarter-penny with a wren on the back, set in a ring for the 1953 Triple Crown season."),
 "l08": (VCC, "Irish Sixpence Marker", "$25", "https://vintagecoinconcepts.com/products/irish-6-pence-eire-ball-marker",
   "A real Irish sixpence with its wolfhound, ringed in copper with &ldquo;May the wind be always at your back.&rdquo; A blessing on a coin, which is about as lucky as a marker gets."),
 "l09": (VCC, "1943 Steel Penny Marker", "$15", "https://vintagecoinconcepts.com/products/1943-uss-intrepid-ball-marker",
   "A real 1943 steel cent, struck in zinc-coated steel that year because copper was needed for the war. The odd one out in any coin jar."),
 "l10": (VCC, "Italian Coin Divot Tool and Marker", "$17.99", "https://vintagecoinconcepts.com/products/italian-coin-divot-repair-tool",
   "A divot tool with a real old Italian coin set in the handle as the marker. Two jobs, one old coin."),
 "l11": (MM, "Liberty Peace Marker", "about $30", "https://irv.com/product/liberty-peace/",
   "Half a troy ounce of .999 silver struck with the Peace dollar&rsquo;s Liberty head. Priced with the silver market, so it moves; check on the day."),
 "l12": (MM, "Memento Mori Marker", "about $30", "https://irv.com/product/memento-mori/",
   "Silver with a skull and MEMENTO MORI: remember you will die. The opposite of a lucky charm, and a fair reminder on a three-putt day."),
 "l13": ("Ancient Resource", "Constantine &ldquo;Manus Dei&rdquo; Bronze, c. 337 AD", "from $125", "https://ancientresource.com/lots/ancient-coins/manus-dei.html",
   "A real Roman bronze, struck after Constantine&rsquo;s death, showing the hand of God reaching down to him. The dealer calls it the first coin to show a Judeo-Christian deity. Not a marker; keep it in the other pocket."),
 # 3. Saints and medals
 "l14": ("The Catholic Company", "Sterling St. Christopher Golf Pendant", "$138.95", "https://www.catholiccompany.com/products/sterling-silver-st-christopher-golf-pendant",
   "St. Christopher, patron of travelers, with a golfer on the medal. For the drive to the course as much as the round."),
 "l15": ("Matthew F. Sheehan", "St. Christopher Golf Pendant", "$92.50", "https://www.matthewfsheehan.com/products/st-christopher-golf-medium-pendant",
   "The same saint in sterling, a little smaller and a little cheaper."),
 "l16": (MM, "Sacred Heart Marker", "about $30", "https://irv.com/product/sacred-heart/",
   "The Sacred Heart in half an ounce of .999 silver, sized to mark a ball. For the putt you are praying over anyway."),
 "l17": (MM, "Our Lady of Guadalupe Marker", "about $30", "https://irv.com/product/our-lady-of-guadalupe/",
   "Our Lady of Guadalupe in .999 silver. Of the religious markers we found, the most detailed strike."),
 "l18": ("Lisa Leonard", "Roman Cross Coin Ball Marker", "$36.99", "https://www.lisaleonard.com/products/roman-cross-coin-golf-ball-marker-bronze-prd-slm0042-bz",
   "A small brass coin with a cross, made by hand, so no two are quite the same. Quieter than a medal."),
 "l19": ("Aim&eacute; Leon Dore", "14Kt Gold Saint George Coin Pendant", "$1,250", "https://www.aimeleondore.com/products/14kt-gold-saint-george-coin-pendant",
   "Saint George and the dragon on green enamel in 14-karat gold. The most expensive way to carry a saint on this page."),
 # 4. Horseshoes, clovers and rabbits
 "l20": ("Smathers &amp; Branson", "Horseshoe Belt, Dark Khaki", "$195", "https://smathersandbranson.com/products/horseshoe-belt-dark-khaki",
   "Hand-stitched needlepoint horseshoes on khaki, with a key fob and bottle opener to match."),
 "l21": ("Siegelman Stable", "Horseshoe Belt", "$288", "https://siegelmanstable.com/products/siegelman-stable-belt",
   "Siegelman Stable&rsquo;s Horseshoe Belt in black leather. Luck you wear every day, not just on the course."),
 "l22": ("Smathers &amp; Branson", "Monogrammed Horseshoe Key Fob", "$50", "https://smathersandbranson.com/products/monogrammed-horseshoe-key-fob-dark-khaki",
   "The belt&rsquo;s horseshoes on a key fob, with your initials. The unmonogrammed version is $35."),
 "l23": ("Smathers &amp; Branson", "Horseshoe Bottle Opener", "$35", "https://smathersandbranson.com/products/horseshoe-bottle-opener-dark-khaki",
   "Needlepoint horseshoes on a bottle opener, for after the round whichever way it went."),
 "l24": ("Duke &amp; Dexter", "Wilde Good Luck Bit Loafer, Men&rsquo;s", "$360", "https://dukeanddexter.com/products/wilde-good-luck-bit-loafer-mens",
   "Black leather bit loafers with GOOD on one toe and LUCK on the other. For the clubhouse, not the course."),
 "l25": ("Daphne&rsquo;s Headcovers", "Rabbit Headcover", "$45.99", "https://www.daphnesheadcovers.com/products/rabbit",
   "A whole plush rabbit for the driver. The rabbit&rsquo;s foot was the lucky charm; this keeps the rest of him."),
 "l26": ("Stick Grips", "Shamrock Putter Grip", "$34.95", "https://stickgripsgolf.com/products/stick-grips-golf-shamrock-putter-grip",
   "A white putter grip covered in green shamrocks, the club where luck is most often asked for."),
 "l27": ("Provision Machining Design", "Stainless Divot Tool, Four-Leaf Clover", "$39.99", "https://www.provisionmachiningdesign.com/products/stainless-steel-golf-divot-tool-with-engraved-four-leaf-clover",
   "A machined stainless divot tool with a four-leaf clover on the face. Also made in copper."),
 "l28": ("Baldwin Belts", "Clover Needlepoint Key Fob", "$32", "https://baldwinbelts.com/products/needlepoint-key-fob-clover-key-fob-hand-stitched-copy",
   "A green clover hand-stitched on navy, with a lobster clasp to hang off a bag."),
 "l29": ("Baldwin Belts", "Clover Needlepoint Sunglass Strap", "$38", "https://baldwinbelts.com/products/needlepoint-sunglass-strap-clover-design-leather-needlepoint-sunglass-strap-sunglass-retainer-custom-sunglass-straps-made-to-order",
   "Clovers on a needlepoint sunglass strap, made to order. Luck you wear around your neck all round."),
 "l30": ("Baldwin Belts", "Evil Eye Needlepoint Key Fob", "$28", "https://baldwinbelts.com/products/evil-eye-key-fob-design-on-either-side-of-fob",
   "The evil eye, which is meant to send bad luck back where it came from. Stitched on both sides."),
 "l31": ("Aim&eacute; Leon Dore", "Diamond Horseshoe Pendant", "$995", "https://www.aimeleondore.com/products/diamond-horseshoe-pendant",
   "A gold horseshoe set with diamonds. Points up, the old saying goes, or the luck runs out."),
 # 5. Count your tees
 "l32": ("Sunday Golf", "Lucky Bamboo Golf Tees, 80", "$15", "https://sundaygolf.com/products/best-golf-tees",
   "Eighty bamboo tees in a bag. Count out your usual number before the first tee and leave the rest."),
 "l33": ("Clamp Golf Co.", "Tee Holder, Green", "&pound;6 (about $8)", "https://www.clampgolfcompany.co.uk/products/clamp-golf-co-tee-holder-green",
   "A holder that keeps a row of tees on the bag. It holds a set number, which suits the golfer who always carries the same count."),
 "l34": ("Sierra Madre", "The Bag Charm Chain", "$38", "https://sierramadregolf.com/products/the-bag-charm-chain",
   "A beaded chain of charms to hang from the bag. Pick the charms that mean something."),
 # 6. Taking a chance
 "l35": ("Malbon", "Acetate Dice", "$45", "https://malbon.com/products/acetate-dice-havana",
   "Tortoiseshell acetate dice in a cork box, made with Akila. For deciding the side bet."),
 "l36": ("Aim&eacute; Leon Dore", "Mulberry Playing Cards", "$50", "https://www.aimeleondore.com/products/mulberry-playing-cards",
   "A deck in black and gold. Cards in the bag for the rain delay."),
 "l37": ("Provision Machining Design", "Brass Ace of Spades Ball Marker", "$29.99", "https://www.provisionmachiningdesign.com/products/ace-of-spades-golf-ball-marker",
   "A brass marker cut as the ace of spades: the best card in the deck, or the death card, depending on who you ask."),
 "l38": ("Sinking Birdies", "Misfortune Cookie Ball Marker", "&pound;9 (about $12)", "https://www.sinkingbirdies.co.uk/products/misfortune-cookie-ball-marker",
   "A fortune cookie whose fortune is not good news. For the golfer who would rather expect the worst."),
 "l39": ("Clamp Golf Co.", "Playing Card Fairway Cover", "&pound;26.95 (about $36)", "https://www.clampgolfcompany.co.uk/products/clearance-1",
   "A fairway cover in red, black and white card suits. A matching driver cover is also listed."),
 "l40": ("Chipp Golf", "Feelin&rsquo; Lucky Glove, 4-Pack", "$60", "https://www.chippgolfco.com/products/feelin-lucky-golf-glove-4-pack",
   "Four white gloves with green shamrocks. For the golfer who only plays in a glove that has already shot a good score."),
 "l41": ("Chipp Golf", "Feelin&rsquo; Lucky Glove", "$24", "https://www.chippgolfco.com/products/feelin-lucky-golf-glove",
   "The same shamrock glove, one at a time."),
 "l42": ("Pluto Golf", "Reversible Lucky Stripes Beanie", "$54", "https://www.pluto.golf/products/reversible-camo-beanie-black-outline-copy",
   "A reversible beanie, black one side and green the other. Turn it inside out when the round turns."),
 # 7. The pencil
 "l43": ("Aim&eacute; Leon Dore", "Kaweco Script Mechanical Pencil", "$120", "https://www.aimeleondore.com/products/kaweco-script-mechanical-pencil",
   "A Kaweco Script mechanical pencil. The one object that writes down whether the rest of it worked."),
}
SECTIONS = [
 ("Three Coins in the Pocket", "coins", ["l00", "l01", "l02"],
  "<strong>Three pieces &middot; $25&ndash;$99</strong>The coin is the most common golf charm. The story told about Jack Nicklaus is that he would not tee off without three coins on him."),
 ("Old Money: Real Vintage Coins", "old-money", ["l04", "l05", "l06", "l07", "l08", "l09", "l10", "l11", "l12", "l13"],
  "<strong>Ten pieces &middot; $15&ndash;$125</strong>A coin is a legal ball-marker, so it can be a real one. Seven of these are built around actual old coins; one is an actual Roman coin."),
 ("Saints and Medals", "saints", ["l14", "l15", "l16", "l17", "l18", "l19"],
  "<strong>Six pieces &middot; $30&ndash;$1,250</strong>St. Christopher for the drive there. The patron of lost things, St. Anthony, for everything after the first tee."),
 ("Horseshoes, Clovers and Rabbits", "symbols", ["l20", "l21", "l22", "l23", "l24", "l25", "l26", "l27", "l28", "l29", "l30", "l31"],
  "<strong>Twelve pieces &middot; $28&ndash;$995</strong>The oldest lucky symbols, worked into things you wear and carry."),
 ("Count Your Tees", "tees", ["l32", "l33", "l34"],
  "<strong>Three pieces &middot; $8&ndash;$38</strong>Five in the pocket, never a broken one, never the one that just went out of bounds."),
 ("Taking a Chance", "chance", ["l35", "l36", "l37", "l38", "l39", "l40", "l41", "l42"],
  "<strong>Eight pieces &middot; $12&ndash;$60</strong>For golfers who would rather play the odds than fight them."),
 ("The Pencil You Keep Score With", "pencil", ["l43"],
  "<strong>One piece &middot; $120</strong>The last ritual of the round."),
]
N = 43
PQ = {
 "old-money": ("A ball-marker is an artificial object when used to mark the spot of a ball to be lifted, such as a tee, a coin&hellip;", "The Rules of Golf, Definitions"),
}
BANDS = {}
TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">Field Notes</div>
    <p>Ask a golfer about their superstitions and most will say they don&rsquo;t have any. Then watch them on the first tee. The same ball number every round. The same coin, from the same pocket. Exactly five tees, never a red one. A glove that stays in the bag because it has already shot a good score.</p>
    <p><strong>The low number.</strong> Golf balls are numbered so you can tell yours from your partner&rsquo;s, and that is all the number means. Plenty of golfers still won&rsquo;t play anything above a 4, on the theory that a high number on the ball means a high number on the card. Ben Crenshaw is the name most often attached to the habit.</p>
    <p><strong>Coins and colors.</strong> The best-known golf superstitions are told about the best-known players: Jack Nicklaus and his three coins, Chi Chi Rodriguez with one coin for birdie putts and another for eagles, Tiger Woods in red on Sunday. Most of these come to us secondhand, through golf writers and caddies, and we pass them on the same way. Whether every detail is exact matters less than how many golfers recognize themselves in them.</p>
    <p><strong>Saints.</strong> St. Christopher, patron of travelers, has been put on golf medals for years. St. Anthony is the patron of lost things, which in golf covers most of the bag.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Rituals</div>
      <div class="sidebar-detail"><span class="l">Ball number</span><span>Nothing above 4</span></div>
      <div class="sidebar-detail"><span class="l">Coins</span><span>Three, same pocket</span></div>
      <div class="sidebar-detail"><span class="l">Tees</span><span>A set count</span></div>
      <div class="sidebar-detail"><span class="l">Sunday</span><span>Wear red</span></div>
      <div class="sidebar-detail"><span class="l">Picks here</span><span>43, $8&ndash;$1,250</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>1905 Lucky Penny, $30</span></div>
      <div class="hashtags">
        <span class="hashtag">#GolfSuperstitions</span>
        <span class="hashtag">#BallMarker</span>
        <span class="hashtag">#FieldNotes</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""
IDEA = """
<section class="products" data-btk="idea" style="margin-top:8px;padding-bottom:24px">
  <div class="drop-tag grass">Does It Work?</div>
  <h2 class="products-hdr" id="does-it-work">The Lucky Ball Study</h2>
  <div class="writeup-body">
    <p>In 2010, three German psychologists published a study in <em>Psychological Science</em> with a golf result in it: people who were handed a ball and told it had been lucky so far sank more practice putts than people handed the same ball with no comment. The idea was that a charm raises confidence, and confidence helps.</p>
    <p>In 2014, two American researchers ran the putting test again with larger groups and published the result in <em>Social Psychology</em>. The lucky ball made no difference. Golfers told their ball was lucky putted almost exactly as well as golfers told nothing.</p>
    <p>So the ball is probably not doing much. The ritual might be. A coin you always mark with, from the same pocket, is part of a routine, and a routine is something familiar to do while the nerves settle. If it stops working, you can always blame the coin.</p>
  </div>
</section>
"""
STORY = """
<section class="products" data-btk="story" style="margin-top:8px;padding-bottom:48px">
  <div class="drop-tag grass">Keep Going</div>
  <h2 class="products-hdr" id="more">More on the Small Things</h2>
  <div class="writeup-body">
    <p>For markers made to be markers, read <a href="/drops/the-ball-marker-atlas">The Ball Marker Atlas</a> and our <a href="/drops/brand-to-know-matchstick-golf">Brand to Know on Matchstick Golf</a>. For more hand-stitched horseshoes and clovers, see <a href="/drops/golf-needlepoint-roundup">the needlepoint roundup</a>.</p>
    <p>It&rsquo;s only superstition if it stops working.</p>
  </div>
</section>
"""
FAQ = []
LOOKBOOK = ""
FRN = json.loads((ROOT / "research/lucky-rituals/frames.json").read_text())
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
GRID_CSS = ('<style>/*TGI-R3-GRID*/.products-grid[data-n]{display:flex;flex-wrap:wrap;justify-content:center;gap:24px}.products-grid[data-n]>.product-card{flex:0 0 calc((100% - 48px)/3);min-width:0}@media(max-width:820px){.products-grid[data-n]>.product-card{flex-basis:calc((100% - 24px)/2)}}@media(max-width:480px){.products-grid[data-n]>.product-card{flex-basis:100%}}.product-card[data-frames="1"] .pg-arw,.product-card[data-frames="1"] .pg-count,.product-card[data-frames="1"] .pg-dots{display:none!important}</style>\n')
def card(k, idx):
    brand, item, price, handle, copy = P[k]
    url = handle if handle.startswith("http") else SHOP + handle
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
            items.append({"@type": "ListItem", "position": pos, "url": (P[h][3] if P[h][3].startswith("http") else SHOP + P[h][3]), "name": H.unescape(f"{P[h][0]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-11-14", "dateModified": "2026-11-14",
         "author": {"@type": "Person", "@id": "https://thegrassyissue.com/about#lenny", "name": "Lenny Harrington",
                    "url": "https://thegrassyissue.com/about", "sameAs": ["https://instagram.com/thegrassyissue"]},
         "publisher": {"@type": "Organization", "name": "The Grassy Issue", "url": "https://thegrassyissue.com/"},
         "mainEntityOfPage": {"@type": "WebPage", "@id": URL}},
        {"@context": "https://schema.org", "@type": "ItemList", "name": TITLE, "itemListElement": items},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Feed", "item": "https://thegrassyissue.com/"},
            {"@type": "ListItem", "position": 2, "name": "Field Notes", "item": "https://thegrassyissue.com/#feed"},
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
  <a href="/#feed">Field Notes</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Field Notes &middot; Superstitions &middot; Ball Markers</span><span class="dot"></span>
    <span>43 picks &middot; prices checked November 14, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Six ball markers built around real old coins: a 1905 Indian Head penny, a 1943 steel cent, a 1930 Buffalo nickel, an 1895 penny, an Irish sixpence and a 1953 farthing" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for s in SECTIONS:
        if s[1] + "-before" in BANDS: body += band(s[1] + "-before")
        if s[1] in BANDS: body += band(s[1])
        if s[1] in PQ: body += pq(s[1])
        o, n = section(s, n); body += o
        if s[1] + "-after" in BANDS: body += band(s[1] + "-after")
    body += IDEA + STORY
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
