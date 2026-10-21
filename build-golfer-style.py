#!/usr/bin/env python3
"""build-golfer-style.py — "Dress Like Them": style inspired by five golfers. 21 Oct 2026.
Lenny: "fashion inspo from our favorite golfers- Nelly Korda, Arnold Palmer, Min Woo Lee, Anthony Kim, Mo Norman. I want a few vertical images of the golfers and
then smaller boxes on the right in rows of 2 of picks that are inspired by the golfer selected with at least 6 options for each golfer ... little bit of a different style of post"
-> photos: sponsor/brand imagery + PD/CC, credited -> Korda picks menswear -> Palmer in his prime -> Korda leads with the Porthcawl camo photo (supplied by Lenny)
-> "build the full post" (all 60 options from sheet v4) -> "I don't like those belt buckles for Anthony Kim": Montana Silversmiths x2 cut, 58.
FACTS: research/golfer-style/ (brief from Golf Digest, Golf Monthly, Skratch, PGA.com, SI, InsideHook, Golf Canada, Globe and Mail, Bunkered, Australian Golf Digest).
Prices/stock: each store's live data, Oct 21 2026 (final-picks.json). Never "worth".
"""
import html as H
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/brand-to-know-manors.html"
SLUG = "golfer-style-inspiration"
IMG = "/images/golfer-style"
TITLE = "Golfer Style Inspiration: Dress Like Nelly Korda, Arnold Palmer, Min Woo Lee, Anthony Kim and Moe Norman"
DESC = ("Five golfers with a look of their own, and 58 pieces you can buy now that borrow from it: Korda's camo cargos, Palmer's cardigans, "
        "Min Woo Lee's mock necks, Anthony Kim's AK cap and Moe Norman's turtlenecks and too-short pants.")
H1 = "Dress Like Them: Five Golfers, 58 Pieces Inspired by Their Style"
BC = "Golfer Style Inspiration"
PK = json.loads((ROOT / "research/golfer-style/final-picks.json").read_text())

# card copy, in order 1..58 (final-picks.json order). (name override or None, price text or None, copy)
C = [
 # Korda 1-12
 (None, None, "Jordan&rsquo;s men&rsquo;s mock neck in plain Obsidian. Mock necks are the backbone of Korda&rsquo;s Nike wardrobe, and Golf Monthly notes she has regularly worn Jordan golf shoes."),
 (None, None, "A plain long-sleeve cotton mock in Rifle Green, the same muted green that runs through her Porthcawl camo. Also in white."),
 (None, None, "A streamlined technical mock from J.Lindeberg, the Swedish label she wore before Nike. Black, white or navy."),
 (None, None, "Camo nylon in greens and browns with a relaxed utility cut: the closest thing here to the cargos she wore at the 2025 AIG Women&rsquo;s Open."),
 (None, None, "Relaxed olive ripstop with magnetic cargo pockets. The Porthcawl fit in one tone, if full camo is a step too far."),
 (None, None, "Double-pleated Italian wool slacks from Stockholm, full and straight in the leg. The men&rsquo;s answer to the wide-leg trousers she wears, with the European lean she talks about."),
 (None, None, "A loose full-zip in khaki. She&rsquo;s worn a men&rsquo;s Nike full-zip at a major, and her Porthcawl look was built around a roomy jacket over the cargos."),
 (None, None, "A woven cotton-blend blouson in tan, the independent take on the oversized Nike Sportswear jacket. Also in steel."),
 (None, None, "Air Jordan golf shoes are in her rotation. The White/Medium Olive/Khaki colorway sits right in her camo palette; six more colorways if not."),
 (None, "$21.97 (was $24)", "She plays in a visor. This is the plain white Nike Ace, unisex and unstructured."),
 (None, None, "Unlined cotton twill with tonal stitching. Skratch called her style a lesson in restraint, and this cap gets it. Beige or white."),
 (None, None, "Olive cabretta leather instead of tour white, to keep even the glove in the same register as the cargos."),
 # Palmer 13-22
 (None, None, "Red was his color. A red sweater led the outfit, usually with a yellow shirt and blue pants that didn&rsquo;t match on purpose. Also navy and off-white."),
 (None, None, "Mohair, buttoned, in green or mustard: two of the cardigan colors he wore, alongside navy and gray."),
 (None, None, "A navy cardigan, the color you&rsquo;ll find him in across the 1960s."),
 (None, None, "Wool and cashmere, V-neck, in gray. The quietest of Palmer&rsquo;s cardigan colors."),
 (None, None, "From Puma&rsquo;s current Arnold Palmer collection, named for the multicolor umbrella logo he adopted in 1961. Forest green, white or pink."),
 (None, None, "Rope caps have been part of Puma&rsquo;s Arnold Palmer range from the start. This one is in the collection now, in navy or white."),
 (None, None, "The yellow shirt: the middle color in the red, yellow and blue outfits he was remembered for."),
 (None, None, "Double-pleated wool-blend trousers in cement or gray. Palmer&rsquo;s slacks always had a razor crease, so press them."),
 (None, None, "Brown leather penny loafers, kept shined. The Puma x Arnold Palmer collection launched with a brown loafer of its own."),
 (None, None, "Yellow leather with the umbrella logo embroidered on it. Seamus says the yellow nods to his trousers. Fairway, mallet and blade covers too."),
 # Min Woo 23-38
 (None, None, "Lee calls lululemon&rsquo;s ABC Slim Fit trouser &ldquo;sharp and fitted,&rdquo; and it&rsquo;s his pick for the course. This is the golf cut."),
 (None, None, "The Evolution polo, one of the lululemon pieces he names as a favorite. Sixteen colorways."),
 (None, None, "His layering piece. Lee&rsquo;s fits are all about layers, and this half-zip goes over or under nearly anything."),
 (None, "$69 (was $88)", "Mock necks are part of what he calls &ldquo;my branding,&rdquo; along with the mullet, the mustache and the shades. This is lululemon&rsquo;s slim-fit golf version."),
 (None, None, "A chef skull marker, made with The Generous Chef. For a player whose catchphrase is &ldquo;Let Him Cook.&rdquo;"),
 (None, None, "A pink check polo from Okka, a Perth label. Lee is from Perth."),
 (None, None, "A light, water-resistant stretch shell from Gray + Haast on Queensland&rsquo;s Gold Coast. Sand, coffee or dark olive."),
 (None, None, "Ivory twill, straight leg. Lee has worn cream and white trousers in his posts this year."),
 (None, "A$99.95", "A blue-and-green plaid knit vest from Byron Bay, inspired by fairway mow lines. Priced in Australian dollars."),
 (None, None, "Shades are part of the uniform. A white wraparound with a green Prizm Jade lens, for days when the look is loud."),
 (None, None, "A five-panel with a detachable neck flap. Okka&rsquo;s own product link calls it the mullet protector."),
 (None, None, "Full-grain leather and waterproof, with a propulsion plate. PAYNTR named it the Chef. We&rsquo;ll let him cook."),
 (None, None, "A handmade gaucho-style leather belt. The cypress and claret version picks up the green and maroon polos he&rsquo;s worn this year."),
 (None, None, "Australian-made white leather with &ldquo;Let The Big Dog Eat&rdquo; on the side. Food talk for the driver."),
 (None, None, "One-off patchwork covers made in Kalamunda, in the hills outside Perth, from current fabrics and deadstock. No two match."),
 (None, None, "A jacquard knit polo from Walker Golf Things on the Gold Coast, with a whole course landscape knit into it."),
 # AK 39-50
 (None, None, "His initials, finally. Kim became an equity partner in Malbon after winning LIV Adelaide in February, and this is from his AK 1% line. Flip it backward."),
 (None, None, "A white cotton tee from the AK 1% line. He hit balls on the LIV range in a plain white T-shirt during his 2024 comeback."),
 (None, None, "An AK polo in black mesh. In 2024 he helped design polos with his initials for Extracurricular; now they&rsquo;re Malbon."),
 (None, None, "Bunkered identified the runners he wore with gym shorts on the LIV range as Autry. The nylon-and-suede Reelwind is in the same family."),
 ("Malbon x CLUCT Leather Belt", None, "Water-buffalo leather finished in Japan, with a chunky engraved brass buckle under a thick silver coating. From Kim&rsquo;s own brand partner. Preorder, ships by Oct 30."),
 ("Custom Needlepoint Belt", None, "Have AK stitched into the strap, and a flag if you like. Charleston Belt sends a digital proof before it&rsquo;s made."),
 (None, None, "A heavyweight white tee, the other way to do his range look."),
 (None, None, "Nylon, mesh-lined and made for the range, the course and the gym. The gym-shorts half of his LIV practice look. Grey and khaki cost less."),
 (None, None, "He was a Nike player in his 2008 breakout year. This is Nike Golf&rsquo;s plain chest-Swoosh polo, in eleven colors."),
 (None, None, "A structured snapback, built to be worn backward. His 2008 hat was always on backward."),
 # Moe 49-58
 (None, None, "Golf Canada remembers him in turtlenecks on steamy summer days. This lightweight long-sleeve mock is made for the heat."),
 (None, None, "His pants &ldquo;often gave out just south of mid-shin,&rdquo; Golf Digest wrote. Sounder cuts this chino on purpose to a cropped length."),
 (None, "$29 (sale)", "The Globe and Mail remembered a &ldquo;tangerine shirt, banana slacks.&rdquo; Here are the banana slacks, marked down and final sale."),
 (None, None, "He liked bright colors and mixing stripes and plaids. The plaid half."),
 (None, None, "The stripe half, with long sleeves. He buttoned his shirts to the chin, however hot it was."),
 (None, None, "At his memorial he wore a favorite sweater &ldquo;more colourful than the fragrant flower arrangements.&rdquo; Royal and ice blue gets close."),
 (None, None, "His things included a black visor. This is a tall-crown tour visor with a terry sweatband."),
 (None, "$29.95", "He wore two watches at once. Start with a $30 Casio."),
 (None, None, "And the second. A Timex with a slip-through fabric strap."),
 (None, None, "Among his things were 10 pairs of golf shoes. At $70, a frugal way to add one more to the rack."),
]
GOLFERS = [
 ("korda", "Nelly Korda", "nelly-korda", 12,
  "Since moving to Nike in 2023, Korda has stuck to mock necks, clean lines and quiet colors. PGA.com&rsquo;s fashion expert called it &ldquo;classy, athletic and graceful &mdash; never overdone.&rdquo; Then at the 2025 AIG Women&rsquo;s Open at Royal Porthcawl she wore camo cargos and an oversized jacket, and Skratch called it the best golf fit of her career. These picks are menswear, borrowing from both sides of her wardrobe.",
  ("Both my parents are European, so I do gravitate toward a more European style &mdash; something a bit more sophisticated.", "Nelly Korda, to The Zoe Report"),
  [("p", "Nelly Korda in camo cargo pants and a brown Nike long-sleeve polo at the 2025 AIG Women&rsquo;s Open, Royal Porthcawl", "2025 AIG Women&rsquo;s Open, Royal Porthcawl &middot; via Instagram"),
   ("a", "Nelly Korda swinging in a black Nike mock neck and white skirt", "Photo: Nike"),
   ("b", "Nelly Korda at full finish in a sage mock neck and white skirt", "Photo: TaylorMade Golf"),
   ("c", "Nelly Korda holding a driver in a sage mock neck against blue sky", "Photo: TaylorMade Golf")]),
 ("palmer", "Arnold Palmer", "arnold-palmer", 10,
  "Esquire put Palmer on its list of the best-dressed men of all time, and the look was simple: a cardigan or sweater in red, navy, foam green, gray or yellow, a shirt in a color that didn&rsquo;t match, and slacks with a razor crease. Since 2017, the winner of his Invitational at Bay Hill gets a red cardigan.",
  ("He&rsquo;d have a red sweater, a yellow shirt and blue pants&hellip; Everything wasn&rsquo;t match-match.", "Kay McMahon, former LPGA player, to Sports Illustrated"),
  [("c", "Arnold Palmer in a navy cardigan over a light blue mock neck with Jack Nicklaus at the Florida Citrus Open", "1960s, Florida Citrus Open &middot; Photo: Arnold Palmer Invitational"),
   ("g", "Arnold Palmer in a dark knit polo with young fans in the 1960s", "1960s &middot; Photo: Courtesy Arnold Palmer Invitational"),
   ("i", "Black-and-white close-up of Arnold Palmer in a striped polo at the top of his swing", "Photo: Courtesy Arnold Palmer Invitational"),
   ("m", "Arnold Palmer swinging in all white in 1953", "1953 &middot; Photo: U.S. Coast Guard, public domain, via Wikimedia Commons")]),
 ("minwoo", "Min Woo Lee", "min-woo-lee", 16,
  "The Perth-born lululemon ambassador won his first PGA Tour title at the 2025 Houston Open and dresses like he&rsquo;s having more fun than everyone else. He lists mock necks, the mullet, the mustache and the shades as his branding, and he turned &ldquo;Let Him Cook&rdquo; into a lululemon collection. Picks here include his lululemon staples, plus color, pattern and a few Australian brands from his corner of the country.",
  ("Look good, feel good, play good.", "Min Woo Lee, to the PGA Tour"),
  [("a", "Min Woo Lee in a navy vest and dark trousers on a golf course", "Photo: lululemon"),
   ("b", "Min Woo Lee walking in a light blue polo and navy trousers", "Photo: lululemon"),
   ("c", "Min Woo Lee crouched reading a putt in a blue polo and sunglasses", "Photo: lululemon"),
   ("d", "Min Woo Lee swinging in a beige mock neck", "Photo: lululemon")]),
 ("ak", "Anthony Kim", "anthony-kim", 10,
  "In 2008 Kim won twice on the PGA Tour and beat Sergio Garc&iacute;a 5 and 4 at the Ryder Cup, with a backward hat and a big custom AK belt buckle. Then he disappeared for 12 years. He came back with LIV in 2024, hitting balls in a white tee, gym shorts and runners, won LIV Adelaide in February 2026 and became an equity partner in Malbon, which now sells his AK 1% line.",
  ("But if we had a bunch of 18-year-old kids, they&rsquo;d all want to wear it. It&rsquo;s a cool idea.", "Anthony Kim on team belt buckles, to Golf Digest, 2008"),
  [("a", "Anthony Kim smiling in a white AK cap and black polo", "Photo: Malbon"),
   ("b", "Anthony Kim in a black AK tee holding the flag with his daughter", "Photo: Malbon"),
   ("c", "Anthony Kim in a grey 1% Better sweatsuit with his family", "Photo: Malbon"),
   ("f", "Anthony Kim full length in a white half-zip windshirt, navy shorts and white AK cap", "Photo: Malbon")]),
 ("moe", "Moe Norman", "moe-norman", 10,
  "The Canadian two-time national amateur champion was golf&rsquo;s purest ball-striker and one of its oddest dressers. He buttoned long-sleeve shirts to the chin in any heat, wore turtlenecks in summer, liked bright colors and mixed stripes with plaids, and his pants were always an inch too short. He wore two watches at once. He was frugal, too, so plenty of these picks are cheap.",
  ("Golf is to have fun.", "Moe Norman, to Golf Digest"),
  [("e", "Moe Norman swinging in a patterned shirt and brown trousers in front of a crowd", "Photo: Graves Golf"),
   ("a", "Moe Norman at address on the range in a light sweater", "Photo: Graves Golf"),
   ("c", "Moe Norman at address in a navy shirt and white visor", "Photo: Graves Golf"),
   ("d", "Moe Norman hitting an iron in a blue shirt and bright blue trousers", "Photo: Graves Golf")]),
]
N = 58
LS = ' style="border-bottom:1px solid var(--ink)"'
CSS = """<style>
.gs-row{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,7fr);gap:48px;align-items:stretch;margin:40px auto 0;max-width:1040px}
.gs-photos{display:flex;flex-direction:column;justify-content:space-between;gap:32px}.gs-photos figure{margin:0}.gs-photos img{width:100%;aspect-ratio:4/5;object-fit:cover;display:block;background:#E8E2D6}
.gs-photos figcaption{font-family:'JetBrains Mono',monospace;font-size:10.5px;letter-spacing:.02em;color:var(--muted,#6b6b5e);margin-top:6px;line-height:1.4}
.gs-row .products-grid{grid-template-columns:1fr 1fr !important;gap:32px 28px}
.gs-row .product-body{padding:18px 20px 20px}
.gs-row .product-card .product-desc{font-size:12.5px;line-height:1.55}
.gs-row .product-name{font-size:15px}
.gs-row .product-brand{font-size:9.5px}
.gs-sec{margin-bottom:40px}
@media (max-width:760px){.gs-row{grid-template-columns:1fr;gap:12px}
 .gs-photos{display:flex;flex-direction:row;justify-content:flex-start;gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;margin:0 -16px;padding:0 16px}
 .gs-photos figure{flex:0 0 72%;scroll-snap-align:start;margin:0}
 .gs-row .products-grid{gap:16px 12px}.gs-row .product-body{padding:14px 12px 16px}.gs-row .product-card .product-desc{font-size:12.5px}}
</style>
"""


def price(p, i):
    o = C[i][1]
    return o if o else f"${p['price_usd']:,.2f}".replace(".00", "")


TAKE = """
<section class="products" data-btk="take">
  <div class="writeup-body">
    <div class="drop-tag grass">The TGI Take</div>
    <p>Most golfers dress like the pro shop told them to. These five didn&rsquo;t, and you could pick each of them out from the far side of the range. That&rsquo;s the bar we used: a look so particular that you can build an outfit around it fifty years later, or from the other side of the world.</p>
    <p><strong>They make it look like their own.</strong> Palmer&rsquo;s cardigans and Korda&rsquo;s cargos have nothing in common except that neither looks like a costume. Palmer wore three colors that didn&rsquo;t match and made it look deliberate. Korda put camo on at a major and made it look like she always had. Wear it with confidence and it reads as style.</p>
    <p><strong>You don&rsquo;t have to copy them.</strong> Nobody needs Moe Norman&rsquo;s pants exactly an inch too short or a sterling AK buckle. Take one idea per golfer: a cardigan over a polo, a mock neck under everything, one loud piece, a white tee and shorts on the range, a second watch. Each section starts with what they actually wore, then gives you a dozen ways in.</p>
    <p>We mixed the brands the way they did. Korda, Lee and Palmer&rsquo;s name are tied to big brands, so Nike, lululemon and Puma are here. Kim now wears Malbon, which started small, and independents from Perth to Stockholm fill in the rest. Everything was in stock when we checked on October 21, 2026.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Edit</div>
      <div class="sidebar-detail"><span class="l">Golfers</span><span>5</span></div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>58</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>$20 to $429</span></div>
      <div class="sidebar-detail"><span class="l">Stock checked</span><span>Oct 21, 2026</span></div>
      <div class="hashtags">
        <span class="hashtag">#GolfStyle</span>
        <span class="hashtag">#GolfFits</span>
        <span class="hashtag">#IndieGolf</span>
      </div>
    </div>
  </aside>
</section>
"""
FAQ = [
 ("What did Nelly Korda wear at the 2025 AIG Women's Open?", "Camo cargo pants with Nike tops and an oversized Nike Sportswear jacket at Royal Porthcawl. Skratch called it the best golf fit of her pro career."),
 ("What clothing brand does Nelly Korda wear?", "Nike, since January 2023. Before that she wore J.Lindeberg. Her clubs are TaylorMade."),
 ("Why did Arnold Palmer wear cardigans?", "Cardigans and sweaters were standard golf wear in his era, and Palmer made them his own in red, navy, foam green, gray and yellow. The winner of the Arnold Palmer Invitational has received a red cardigan since 2017."),
 ("What brand does Min Woo Lee wear?", "lululemon. He became a global ambassador in January 2024, and his favorites include the ABC Slim Fit trouser, the Evolution polo and the Soft Jersey Half Zip."),
 ("What was on Anthony Kim's belt buckle?", "His initials. In 2008 he wore big custom AK buckles that Golf Digest called his bling belt. In 2026 he became an equity partner in Malbon, which sells an AK 1% line."),
 ("How did Moe Norman dress?", "Long-sleeve shirts buttoned to the chin even in heat, turtlenecks in summer, bright colors with stripes and plaids, and pants that were always a little too short. He also wore two watches."),
]
OUT = ROOT / f"drops/{SLUG}.html"
URL = f"https://thegrassyissue.com/drops/{SLUG}"


def card(p, i, idx):
    name = C[i][0] or p["name"]
    pr = price(p, i)
    label = H.escape(H.unescape(name).replace('"', ""))
    return (f'<div class="product-card" id="p-{idx}" data-frames="1"><div class="product-gallery">'
            f'<div class="pg-track"><div class="pg-frame"><img src="{IMG}/p-{idx}.jpg" alt="{H.escape(p["brand"])} {label}" loading="lazy" /></div></div>'
            f'</div><div class="product-body"><div class="product-brand">{H.escape(p["brand"])}</div>'
            f'<div class="product-name">{H.escape(name)} &middot; {pr}</div>'
            f'<div class="product-desc">{C[i][2]}</div>'
            f'<a href="{H.escape(p["url"])}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a></div></div>')


def golfer(g, n0):
    key, name, anchor, cnt, intro, (q, who), photos = g
    ps = PK[key]
    assert len(ps) == cnt, key
    figs = "\n".join(f'    <figure><img src="{IMG}/g-{key}-{x}.jpg" alt="{alt}" loading="lazy" /><figcaption>{cap}</figcaption></figure>' for x, alt, cap in photos)
    cards = "\n".join(card(p, n0 - 1 + j, n0 + j) for j, p in enumerate(ps))
    return (f'\n<section class="products gs-sec" style="margin-top:8px;">\n'
            f'  <div class="drop-tag grass">Inspired by &middot; {cnt} pieces</div>\n'
            f'  <h2 class="products-hdr" id="{anchor}">{name}</h2>\n'
            f'  <p class="cat-kicker">{intro}</p>\n'
            f'  <div class="pull-quote" style="margin:28px auto 8px"><div class="pull-quote-inner">&ldquo;{q}&rdquo;<span class="pull-quote-attr">&mdash; {who}</span></div></div>\n'
            f'  <div class="gs-row">\n  <div class="gs-photos">\n{figs}\n  </div>\n'
            f'    <div class="products-grid">\n{cards}\n    </div>\n  </div>\n</section>\n'), n0 + cnt


def faq_html():
    rows = "\n".join(f'    <details open class="faq-q"><summary>{H.escape(q)}</summary><p>{H.escape(a)}</p></details>' for q, a in FAQ)
    return (f'\n<section class="products" style="border-top:none;padding-top:48px">\n'
            f'  <h2 class="products-hdr" id="faq">The Questions</h2>\n  <div class="faq">\n{rows}\n  </div>\n</section>\n\n')


def head_top():
    og = f"https://thegrassyissue.com{IMG}/og.jpg"
    items, pos = [], 1
    for g in GOLFERS:
        for j, p in enumerate(PK[g[0]]):
            items.append({"@type": "ListItem", "position": pos, "url": p["url"], "name": H.unescape(C[pos - 1][0] or p["name"])})
            pos += 1
    blocks = [
        {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
         "url": URL, "image": og, "datePublished": "2026-10-21", "dateModified": "2026-10-21",
         "about": [{"@type": "Person", "name": g[1]} for g in GOLFERS],
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


def main(apply_):
    assert len(C) == N == sum(g[3] for g in GOLFERS)
    for i in range(1, N + 1):
        assert (ROOT / f"images/golfer-style/p-{i}.jpg").is_file(), i
    d = DONOR.read_text(encoding="utf-8")
    head_rest = d[d.index("<style>"):d.index('<div class="breadcrumb">')]
    tail = d[d.index('<div class="more" data-brandindex="1">'):]
    jump = " &middot; ".join(f'<a href="#{g[2]}"{LS}>{g[1]}</a>' for g in GOLFERS)
    body = CSS + f"""<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  {BC}</div>

<header class="drop-header">
  <h1>{H1}</h1>
  <div class="drop-meta">
    <span>5 golfers &middot; 58 pieces</span><span class="dot"></span>
    <span>In stock when we checked, October 21, 2026</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Five golfers side by side: Arnold Palmer in a navy cardigan, Nelly Korda in camo cargo pants, Anthony Kim in a white Malbon windshirt, Min Woo Lee in a navy vest and Moe Norman mid-swing in a patterned shirt" fetchpriority="high" /></div></div>
"""
    body += TAKE
    body += f'\n<section class="products" style="margin-top:8px;">\n  <p class="cat-kicker"><strong>Jump to</strong>{jump}</p>\n</section>\n'
    n = 1
    for g in GOLFERS:
        o, n = golfer(g, n); body += o
    body += faq_html()
    out = head_top() + head_rest + body + tail
    print(f"  {n-1} cards")
    if not apply_:
        print("  dry run — pass --apply"); return
    OUT.write_text(out, encoding="utf-8")
    fin = OUT.read_text(encoding="utf-8")
    above = re.sub(r"<style\b.*?</style>|<script\b.*?</script>|<!--.*?-->", "", fin[:fin.index('<div class="more" data-brandindex')], flags=re.S)
    bad = []
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
