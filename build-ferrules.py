#!/usr/bin/env python3
"""build-ferrules.py — Golf ferrules: what they are, who makes cool ones, where to get them installed in Austin.

1 October 2026. Lenny: "Let's do a post about Ferrules - what are they, who makes cool ones and where you can get
them installed", then "Feralgolfshop.com / Clamp / https://bbandfco.com/ to start", then "show me the post preview".
Picks are a first pass from research/ferrules/picks.json for Lenny to swap.

FACTS: research/ferrules/sel.json (each read from the brand's own store products.json, 1 Oct 2026). Feral and BB&F
founders/story from their own About pages; BB&F pitch quote from GolfWRX WRX Spotlight (13 Mar 2019). Austin shops
from their own repair pages, 1 Oct 2026. GBP shown with ~USD at 1.3449.
PHOTOS: brands' own store images, localised to /images/ferrules (research/ferrules/frames.json).
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "golf-ferrules-guide"
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"
IMG = "/images/ferrules"
_FR = json.loads((ROOT / "research/ferrules/frames.json").read_text())
FRN = {v["key"]: v["frames"] for v in _FR.values()}

TITLE = "Custom Golf Ferrules: What They Are, Who Makes Cool Ones, Where to Get Them Installed"
DESC = ("What a golf ferrule does, the sizes that matter, 28 custom ferrules from Feral Golf, Clamp and BB&F Co, "
        "and where to get them installed in Austin, with prices.")
H1 = "The Smallest Upgrade in the Bag: Custom Ferrules, and Where to Get Them Put On"
GBP = "&pound;26 (~$35)"

FERAL_STD = "$59 for 10, $35 for 5, $15 for one"
BBF_3D = "$22.50 for 3, $49 for 10"

# key -> (brand, item, price, url, copy)
P = {
 "feral-minoan-red": ("Feral Golf", "Minoan Red", FERAL_STD,
   "https://www.feralgolfshop.com/products/feral-golf-minoan-red-geometric-ferrule-ancient-angles",
   "A dusty red band with pink diamonds, like a tile off an old Greek floor. Every standard Feral is a 1-inch, matte, slightly raised print on a toughened polymer, sized to fit both .355 taper and .370 parallel tips."),
 "feral-light-green-marble": ("Feral Golf", "Light Green Marble", FERAL_STD,
   "https://www.feralgolfshop.com/products/feral-golf-light-green-marble-ferrule-fresh-cut-stone",
   "Pale green stone with darker veins. On chrome it looks like a jade ring, and it is the quietest design in the Feral library."),
 "feral-tsunami": ("Feral Golf", "Tsunami", FERAL_STD,
   "https://www.feralgolfshop.com/products/feral-golf-tsunami-ferrule",
   "A breaking wave in navy, cream and rust that reads as a woodblock print at arm&rsquo;s length. Feral cuts this one in three outside diameters to match thinner or thicker hosels."),
 "feral-the-wave": ("Feral Golf", "The Wave", FERAL_STD,
   "https://www.feralgolfshop.com/products/feral-golf-the-wave-golf-ferrule",
   "A single colour fading into white, sold in a run of shades from red through purple. Buy a different colour for each club and the set becomes a rainbow, or keep it to one."),
 "feral-palm-trees": ("Feral Golf", "Palm Trees", FERAL_STD,
   "https://www.feralgolfshop.com/products/feral-golf-palm-trees-golf-ferrule-swing-in-the-breeze",
   "Grey palm silhouettes on white. Subtle from address, and a good match for anything resort-coded in the bag."),
 "feral-the-pollack": ("Feral Golf", "The Pollack", FERAL_STD,
   "https://www.feralgolfshop.com/products/feral-golf-the-pollack-golf-ferrule-abstract-paint-splatter",
   "Red, yellow, blue and black splatter on an off-white base. There is a Red Pollack too, if you want the same idea in fewer colours."),
 "feral-the-glizzy": ("Feral Golf", "The Glizzy", FERAL_STD,
   "https://www.feralgolfshop.com/products/feral-golf-the-glizzy-golf-ferrule-hot-dog-pattern",
   "Tiny hot dogs, buns and all, on light grey. Feral calls it a conversation starter, and it is the one people will ask about on the tee."),
 "feral-kyro-performance": ("Feral Golf", "KYRO Performance Ferrule", "$118 for 10, $30 for one",
   "https://www.feralgolfshop.com/products/kyro-performance-ferrule",
   "KYRO is Feral&rsquo;s textured ferrule, in an inverted pyramid or a dimpled finish, with a matching pattern moulded inside. Feral says it damps vibration at impact. We have not hit it, so treat that as the brand&rsquo;s claim; the texture is the reason to buy it."),
 "feral-your-custom-design": ("Feral Golf", "Your Custom Design", "$89 for 10, $35 for one",
   "https://www.feralgolfshop.com/products/feral-golf-your-custom-design-golf-ferrule-fully-custom-graphics",
   "Send Feral a logo, a pattern or your club&rsquo;s colours and they print it on a ferrule. Ten is $89. For a home course or a member-guest team, this is the move."),
 "clamp-zestful-zebra": ("Clamp Golf Co", "Zestful Zebra", GBP,
   "https://www.clampgolfcompany.co.uk/products/custom-ferrules-15",
   "Yellow ferrules with black rings, ten to a pack, in a Clamp pouch. Every Clamp set is cut for .355 tips and will stretch over .370 after five minutes in hot soapy water."),
 "clamp-icy-intrigue": ("Clamp Golf Co", "Icy Intrigue", GBP,
   "https://www.clampgolfcompany.co.uk/products/custom-ferrules-19",
   "Black with pale blue and white rings. It goes with almost any headcover, which is how Clamp pitches its ferrules in the first place."),
 "clamp-emerald-elegance": ("Clamp Golf Co", "Emerald Elegance", GBP,
   "https://www.clampgolfcompany.co.uk/products/custom-ferrules-11",
   "Black with two green rings. The British racing green option."),
 "clamp-creamsicle-dream": ("Clamp Golf Co", "Creamsicle Dream", GBP,
   "https://www.clampgolfcompany.co.uk/products/custom-ferrules-7",
   "Black with orange and cream rings. Pair it with anything orange from Clamp&rsquo;s reworked headcovers."),
 "clamp-liberty-links": ("Clamp Golf Co", "Liberty Links", GBP,
   "https://www.clampgolfcompany.co.uk/products/custom-ferrules-4",
   "Red, white and navy rings on black. The flag set."),
 "clamp-regal-reflection": ("Clamp Golf Co", "Regal Reflection", GBP,
   "https://www.clampgolfcompany.co.uk/products/custom-ferrules-22",
   "White ferrules with navy rings, the cleanest set Clamp makes, and the one that looks most like a tour van build."),
 "bbf-pinky": ("BB&amp;F Co", "Pinky", "$35 for 10",
   "https://bbandfco.com/products/snaggleferrule",
   "Black, pink and silver, 1 inch tall. One of BB&amp;F&rsquo;s newest drops."),
 "bbf-mint-julep": ("BB&amp;F Co", "Mint Julep", "$35 for 10",
   "https://bbandfco.com/products/mint-julep",
   "Black with green and silver bands. Masters week in a ferrule."),
 "bbf-blue-recluse-blanco-copper-std": ("BB&amp;F Co", "Blue Recluse (Blanco, Copper)", "$38.50 for 10",
   "https://bbandfco.com/products/blue-recluse-blanco-copper-std",
   "White body with copper and three blues, in BB&amp;F&rsquo;s standard 1.3-inch height. The copper ring is the detail that shows on a sunny day."),
 "bbf-1776-no-5": ("BB&amp;F Co", "1776 (No 5)", "$38.50 for 10",
   "https://bbandfco.com/products/1776-no-5",
   "White, navy, copper and red. A dressier flag set than the usual red-white-blue."),
 "bbf-coconut-grove": ("BB&amp;F Co", "Coconut Grove", "$38.50 for 10",
   "https://bbandfco.com/products/coconut-grove",
   "White and silver with neon pink and neon blue stripes. Miami Vice for your 7-iron."),
 "bbf-utah-copper": ("BB&amp;F Co", "Utah (Copper)", "$38.50 for 10",
   "https://bbandfco.com/products/utah-copper",
   "Black, copper, olive and white. Earthy enough to sit next to waxed canvas and leather."),
 "bbf-amazon-goddess-double-deluxe-2": ("BB&amp;F Co", "Amazon Goddess (Double Deluxe, 2&Prime;)", "$20 for 5",
   "https://bbandfco.com/products/amazon-goddess",
   "Twice the height of a normal ferrule, in black, copper, blues and purples. BB&amp;F notes these add one to two swingweight points, so tell your builder."),
 "bbf-monte-rosa": ("BB&amp;F Co", "Monte Rosa", BBF_3D,
   "https://bbandfco.com/products/monte-rosa",
   "3D printed in ABS in black, red, silver and white, 1 inch tall. Choose steel .355, graphite .355 or .370 at checkout. Printed in batches, so allow 5 to 10 business days."),
 "bbf-watermelon-taffy": ("BB&amp;F Co", "Watermelon Taffy", BBF_3D,
   "https://bbandfco.com/products/watermelon-taffy",
   "Olive green, pink, silver, black and white. BB&amp;F will print a matching pitch-mark tool for $39 if you want the set."),
 "bbf-danger-squid": ("BB&amp;F Co", "Danger Squid", BBF_3D,
   "https://bbandfco.com/products/danger-squid",
   "Navy, teal, silver, black and white. The printed ribs catch light in a way moulded plastic does not."),
 "bbf-red-gold-fei-long-ti": ("BB&amp;F Co", "Red &amp; Gold Fei Long (Ti)", "$30 each",
   "https://bbandfco.com/products/red-gold-fei-long-ti",
   "Titanium, 1 inch, engraved with a dragon and finished in red and gold. Metal ferrules are sold one at a time, with a plastic base ring the builder turns down flush to the hosel. Allow 10 to 15 business days."),
 "bbf-stars-stripes-ti": ("BB&amp;F Co", "Stars &amp; Stripes (Ti)", "$30 each",
   "https://bbandfco.com/products/stars-stripes-ti-1",
   "Anodised titanium with the flag wrapped around it. On a wedge or a putter it is a statement; on a full set it is a lot."),
 "bbf-fresh-minted-bills-al": ("BB&amp;F Co", "Fresh Minted Bills (Al)", "$12.50 each",
   "https://bbandfco.com/products/fresh-minted-bills-al",
   "Aluminium, engraved with a dollar bill. Pick the denomination at checkout, which makes the money wedge an obvious idea."),
 "bbf-zigby-goes-down-al": ("BB&amp;F Co", "Zigby Goes Down (Al)", "$12.50 each",
   "https://bbandfco.com/products/zigby-goes-down-al",
   "Aluminium with a black zebra-stripe engraving, here on a steel shaft. Base rings come in black or grey."),
}

SECTIONS = [
    ("Feral Golf: Printed Ferrules", "feral",
     ["feral-minoan-red", "feral-light-green-marble", "feral-tsunami", "feral-the-wave", "feral-palm-trees",
      "feral-the-pollack", "feral-the-glizzy", "feral-kyro-performance", "feral-your-custom-design"],
     "<strong>Nine picks &middot; $59&ndash;$118 for 10</strong>Feral Golf was started by Tyler Gruden and Wyatt Hilkene, and it does something nobody else here does: it prints a full graphic on the ferrule. Marble, splatter paint, palm trees and hot dogs all wrap the whole band, and each one comes in packs of 1, 3, 5 or 10, so you can do one wedge or the whole set. Feral 3D prints and precision-makes everything, and it will print your own design for $89 for 10."),
    ("Clamp Golf Co: Ring Sets", "clamp",
     ["clamp-zestful-zebra", "clamp-icy-intrigue", "clamp-emerald-elegance", "clamp-creamsicle-dream",
      "clamp-liberty-links", "clamp-regal-reflection"],
     f"<strong>Six sets &middot; {GBP} for 10</strong>Clamp is the UK headcover brand behind the reworked streetwear covers in our <a href=\"/drops/brand-to-know-clamp-golf-company\">Clamp Brand to Know</a>, and its ferrules are the classic ringed kind, sold ten to a pack with a Clamp pouch. They are made for matching: the idea is that your ferrules pick up a colour from your headcovers. Clamp says to have them fitted by a pro, and it offers fitting at its own HQ in the UK."),
    ("BB&amp;F Co: Ring Sets", "bbf-rings",
     ["bbf-pinky", "bbf-mint-julep", "bbf-blue-recluse-blanco-copper-std", "bbf-1776-no-5", "bbf-coconut-grove",
      "bbf-utah-copper", "bbf-amazon-goddess-double-deluxe-2"],
     "<strong>Seven sets &middot; $20&ndash;$38.50</strong>Boyd Blade &amp; Ferrule Co. is Patrick Boyd&rsquo;s company, and it is the name club builders bring up first. It has designed ferrules for OEMs since 2007, works with eight of them now, and says its catalogue runs past 6,000 designs, with new ones added daily. The plastic sets come ten to a pack in three heights, 1-inch, standard and the 2-inch Double Deluxe, cut for .355 taper tips and reamable for .370."),
    ("BB&amp;F Co: 3D Printed", "bbf-3d",
     ["bbf-monte-rosa", "bbf-watermelon-taffy", "bbf-danger-squid"],
     f"<strong>Three designs &middot; {BBF_3D}</strong>BB&amp;F&rsquo;s printed ferrules have ribs and grooves you can feel, in colour combinations a moulded ring cannot do. They are printed in ABS in batches, which is why the lead time is 5 to 10 business days."),
    ("BB&amp;F Co: Titanium and Aluminium", "bbf-metal",
     ["bbf-red-gold-fei-long-ti", "bbf-stars-stripes-ti", "bbf-fresh-minted-bills-al", "bbf-zigby-goes-down-al"],
     "<strong>Four designs &middot; $12.50&ndash;$30 each</strong>Metal ferrules are the top end, and BB&amp;F sells them one at a time: titanium at $30 and aluminium at $12.50. Each sits on a thin plastic base ring that your builder turns down so the metal meets the hosel cleanly. Most people put one on a wedge or a putter rather than doing a whole set."),
]
N = 29

PQ = {
    "bbf": ("Since the development of plastics, ferrules have been the final custom touch on a set of clubs.",
            "BB&amp;F Co., 2019"),
    "feral": ("Golf clubs have long told the same story: &lsquo;plain head, plain shaft, plain ferrule.&rsquo;",
              "Feral Golf Co., About"),
}

SHOPS = [
    ("Fab Golf ATX", "Southwest Austin (78735)", "From $25 a club, ferrules billed at cost",
     "Two builders, by appointment. Most jobs take one to two business days, with 24-hour rush available. Text for a quote.",
     "https://www.fabgolfatx.com/services"),
    ("Southside Golf Co", "Manchaca, off Menchaca Rd &amp; FM 1626", "$25 a club",
     "Repairs done in-house by a PGA Professional. Indoor golf opens in early October; club work is by appointment until then.",
     "https://southsidegolfco.com/golf-club-repair-austin"),
    ("Barton Creek Fitting Studio", "Barton Creek, 8511 Carranza Dr", "Ask for a quote",
     "A full-size tour van on site, with ferrule replacement on the repair menu. Call or text 737-280-8665.",
     "https://www.bartoncreekfittingstudio.com/club-repair"),
    ("PGA TOUR Superstore", "North Austin, 10515 N MoPac Expy", "$20 a club",
     "The big-box option, and the cheapest install on this list. The repair counter does ferrules along with regrips and reshafts; bring your own ferrules.",
     "https://www.pgatoursuperstore.com/stores/austin-texas/1218.html"),
    ("Daddy Shack Golf Club", "Pflugerville", "Ask Nolan",
     "Stamping, paint fill, restoration and full builds. Ferrules are not on the current price list, but reshafting is ($15 steel, $18 graphite), so ask when you book.",
     "https://www.daddyshackgolf.com/club-work/"),
]

PROSE = 'style="max-width:760px;font-size:16px;line-height:1.7;margin:0 auto 24px;"'

TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>New ferrules are the cheapest way to make a set of irons feel like yours. For $35 to $60 and an hour of a builder&rsquo;s time, a stock set from a big-box store gets the detail that tour vans add as standard. Clamp and BB&amp;F&rsquo;s ring sets are the classic look; Feral is for people who want their irons to start a conversation. A single titanium ferrule on a wedge or putter is the best small splurge in this guide.</p>
    <p>The catch is fitting. Unless you are already reshafting, changing a ferrule means taking the head off, so time it with your next reshaft or a loft-and-lie check. Prices were read on each brand&rsquo;s own store on 1 October 2026.</p>
    <h2 class="products-hdr btk-story-hdr">What Is a Ferrule?</h2>
    <p>A ferrule is the small ring, usually black plastic, that sits where the shaft goes into the clubhead. It covers the top of the hosel so you see a clean step from metal to shaft instead of a rough edge and a bead of glue. The epoxy inside the hosel holds the head on, so a ferrule is almost entirely cosmetic, and that is why it is fun to change. Now they come printed with marble and palm trees, ringed in a dozen colours, 3D printed with ribs, or machined from titanium.</p>
    <p>The one thing to get right is size. The inside diameter has to match your shaft tip: .355 for most steel iron shafts, .370 for many graphite ones, .335 for woods. Most ferrules here fit .355 and stretch or ream out to .370. Taller and metal ferrules add a little head weight, so mention them to your builder.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Makers</span><span>Feral Golf, Clamp, BB&amp;F Co</span></div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>29 ferrules and sets</span></div>
      <div class="sidebar-detail"><span class="l">Sets from</span><span>$35 for 10</span></div>
      <div class="sidebar-detail"><span class="l">Install</span><span>$20&ndash;$25 a club in Austin</span></div>
      <div class="sidebar-detail"><span class="l">Prices read</span><span>1 October 2026</span></div>
      <a href="#feral" class="sidebar-cta">See the ferrules &darr;</a>
      <a href="#install" class="sidebar-cta" style="margin-top:8px">Where to get them put on &darr;</a>
      <div class="hashtags">
        <span class="hashtag">#Ferrules</span>
        <span class="hashtag">#ClubBuilding</span>
        <span class="hashtag">#CustomIrons</span>
        <span class="hashtag">#AustinGolf</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</section>
"""

FAQ = [
    ("What does a ferrule do on a golf club?",
     "It covers the top of the hosel where the shaft enters the head, so the joint looks clean and finished. It is cosmetic. The epoxy inside the hosel holds the head on, not the ferrule."),
    ("Can I change ferrules without reshafting?",
     "Usually not. The ferrule slides on from the tip of the shaft, so a builder heats the hosel, pulls the head, fits the new ferrule, re-epoxies and turns it down flush. That is why it is cheapest to do when you are reshafting anyway."),
    ("What size ferrule do I need?",
     "Match the inside diameter to your shaft tip: .355 for most taper-tip steel iron shafts, .370 for parallel-tip and many graphite iron shafts, .335 for most woods and hybrids. Most iron ferrules in this guide fit .355 and can be stretched or reamed to .370."),
    ("How much does it cost to have ferrules installed in Austin?",
     "The PGA TOUR Superstore on North MoPac charges $20 a club. Fab Golf ATX and Southside Golf Co both list ferrule replacement at $25 a club, as of 1 October 2026. Barton Creek Fitting Studio and Daddy Shack quote on request."),
    ("Do custom ferrules affect performance?",
     "A standard 1-inch ferrule makes no meaningful difference. Taller or metal ferrules add a little weight near the head, which can raise swingweight by a point or two, so tell your builder."),
]


def card(k, idx):
    brand, item, price, url, copy = P[k]
    fr = FRN[k]
    label = H.unescape(f"{brand} {item}").replace('"', "")
    imgs = "".join(f'<div class="pg-frame"><img src="{f}" alt="{H.escape(label)} ferrule &middot; view {j+1} of {len(fr)}" loading="lazy" /></div>'
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


def pq(k):
    q, who = PQ[k]
    return (f'\n<div class="pull-quote" style="margin:56px auto 24px">\n  <div class="pull-quote-inner">'
            f'&ldquo;{q}&rdquo;<span class="pull-quote-attr">&mdash; {who}</span></div>\n</div>\n')


def section(sec, n0):
    h2, anchor, ids, kicker = sec
    cards = "\n".join(card(k, n0 + j) for j, k in enumerate(ids))
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">{len(ids)} picks</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{h2}</h2>\n'
            f'  <p class="cat-kicker">{kicker}</p>\n'
            f'    <div class="products-grid">\n{cards}\n    </div>\n</section>\n'), n0 + len(ids)


def install_html():
    rows = "\n".join(
        f'    <div style="border-top:.5px solid var(--ink);padding:16px 0;display:grid;grid-template-columns:1fr 1.6fr;gap:6px 24px">'
        f'<div><div class="product-brand">{area}</div><div class="product-name"><a href="{url}" target="_blank" rel="noopener">{name}</a></div>'
        f'<div style="font-family:var(--mono);font-size:11px;letter-spacing:.04em;margin-top:4px">{price}</div></div>'
        f'<div class="product-desc" style="margin:0">{note}</div></div>'
        for name, area, price, note, url in SHOPS)
    return (f'\n<section class="products" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">Austin</div>\n'
            f'  <h2 class="products-hdr" id="install">Where to Get Them Installed</h2>\n'
            f'  <p class="cat-kicker"><strong>Five shops &middot; $20&ndash;$25 a club</strong>Fitting a ferrule is a bench job: the builder heats the hosel, pulls the head, slides the new ferrule down the shaft, re-epoxies the head and spins the ferrule on a lathe until it is flush with the hosel. Bring the ferrules with you, and if you have a reshaft or a loft-and-lie check coming up, do it all in one visit. Prices below are from each shop&rsquo;s own site on 1 October 2026, except the PGA TOUR Superstore price, which TGI confirmed.</p>\n'
            f'  <div style="max-width:820px;margin:0 auto">\n{rows}\n  </div>\n</section>\n')


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
            items.append({"@type": "ListItem", "position": pos, "url": P[h][3], "name": H.unescape(f"{P[h][0]} {P[h][1]}")})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-10-01", "dateModified": "2026-10-01",
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
            {"@type": "ListItem", "position": 3, "name": "Custom Golf Ferrules", "item": URL}]},
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
    ids = [k for s in SECTIONS for k in s[2]]
    assert len(ids) == N == len(set(ids)) and set(ids) == set(P), (len(ids), set(P) ^ set(ids))
    for k in ids:
        assert FRN.get(k), k
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    body = f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Custom Golf Ferrules</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>Feral Golf, Clamp and BB&amp;F Co, plus five Austin shops</span><span class="dot"></span>
    <span>29 picks &middot; in stock 1 October 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Custom golf ferrules: textured Feral KYRO ferrules on irons at a course, a red and pink printed ferrule on a wedge, and a handful of Stars and Stripes titanium ferrules from BB&amp;F Co" fetchpriority="high" /></div></div>
"""
    body += TAKE
    n = 1
    for i, s in enumerate(SECTIONS):
        if s[1] == "feral":
            body += pq("feral")
        if s[1] == "bbf-rings":
            body += pq("bbf")
        o, n = section(s, n); body += o
    body += install_html()
    body += faq_html()
    out = head_top() + head_rest + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    bad = []
    for leak in ("Manors Revisited", "Nicklaus", "Enron"):
        if leak in above: bad.append("leak " + leak)
    if fin.count('class="product-card"') != N: bad.append("card count")
    if re.search(r"\bworth\b", re.sub(r"<[^>]+>", " ", above), re.I): bad.append("banned word")
    for f in set(re.findall(rf'src="({IMG}/[^"]+)"', fin)):
        if not (ROOT / f.lstrip("/")).is_file(): bad.append("missing " + f)
    for href in set(re.findall(r'href="(/(?:drops|guides)/[^"#]+)"', above)):
        if not (ROOT / (href.lstrip("/") + ".html")).is_file(): bad.append("dead link " + href)
    if bad: sys.exit("! check failed: " + "; ".join(bad))
    print(f"  wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
