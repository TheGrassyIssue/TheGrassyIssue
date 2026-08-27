#!/usr/bin/env python3
"""
Builds /drops/golf-brands-founded-by-women.

SCOPE (rebuilt 2026-08-27): seventeen golf brands founded or co-founded by a
woman that make MEN'S or UNISEX product. This is the menswear-lens rebuild —
the earlier six-brand version led on womenswear labels and was scrapped.

FOUNDER ATTRIBUTION — every name below was confirmed from a brand-owned About
page, a signed founder interview, or a government company filing. Where a woman
co-founded WITH a husband or partner, we say so rather than rounding up.

VERBATIM QUOTES ONLY. Sources for the three pull-quotes used:
  * Jane Spicer  — KJZZ "The Show" transcript, 23 Jun 2023
  * Erica Bennett — ORKAI's own About page, orkai.life/about
  * Alex Bartholomew — Golf Today Q&A, M. James Ward, 18 May 2019

BRANDS WITH NO FINDABLE QUOTE FROM THE WOMAN FOUNDER (do not invent one):
  Jan Craig / Janet Craig Cruise, Megan Chisti (Seamus), Gail Hanson
  (Bluetross), Christina Rogers (Sinking Birdies), Mary Ann Sheppard (Devant),
  Isabelle Shee (Inside Story), Antje Elle (Duca del Cosma).
  For Seamus and Bluetross the pattern is itself the story: the brand credits
  the wife as co-founder on paper while every published quote is the husband's.

DELIBERATELY EXCLUDED:
  * Birds of Condor — the brand's own About page names no founder, every trade
    profile credits Frankie Kimpton alone, and Zoe Kimpton's co-founder credit
    exists only in one local paper's photo captions. Not assertable.
  * Sierra Madre, Draw & Fade Modern, Goldie Byrd, Foray, KINONA, PRIO, LIJA,
    Jamie Sadock — womenswear-only, dead stores, or both.
  * Rose & Fire — founded by Mike Buchfuhrer. Rose was his grandmother.

CAVEAT CARRIED IN THE COPY: Zalea's markets every item to women ("Headcovers
Made for HER GAME"). It is included because its patterns are neutral, and the
copy says so plainly rather than implying it cuts for men.
"""
import json, os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
IMGDIR = os.path.join(ROOT, "images", "women-founded")
IMG  = "/images/women-founded/"
TPL  = os.path.join(ROOT, "drops", "brand-to-know-midiron.html")
SLUG = "golf-brands-founded-by-women"
OUT  = os.path.join(ROOT, "drops", SLUG + ".html")
TITLE = "Seventeen Golf Brands Founded by Women"
TITLE_TXT = "Seventeen Golf Brands Founded by Women"
DESC = ("Seventeen golf brands founded or co-founded by women that make men's and unisex gear — "
        "hand-knit headcovers since 1962, Horween leather, Cabretta gloves, polos and Italian shoes. "
        "Every founder named and sourced.")

def frames(key):
    fs = sorted(glob.glob(os.path.join(IMGDIR, f"{key}-*.jpg")),
                key=lambda p: int(re.search(r'-(\d+)\.jpg$', p).group(1)))
    return [os.path.basename(f) for f in fs]

def card(key, brand, founders, name, desc, link):
    fr_files = frames(key)
    n = len(fr_files)
    assert n, f"no frames for {key}"
    plain = re.sub(r'&[a-z]+;', "'", brand)
    fr = "".join(f'<div class="pg-frame"><img src="{IMG}{f}" loading="lazy" '
                 f'alt="{brand} &middot; view {i+1} of {n}"></div>'
                 for i, f in enumerate(fr_files))
    dots = "".join(f'<button class="pg-dot{" on" if i==0 else ""}" data-i="{i}" '
                   f'aria-label="View image {i+1}"></button>' for i in range(n))
    return f'''  <div class="product-card" id="{key}" data-frames="{n}">
    <div class="product-gallery"><div class="pg-track">{fr}</div><button class="pg-arw prev" aria-label="Previous image">&#8249;</button><button class="pg-arw next" aria-label="Next image">&#8250;</button><span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>
      <div class="product-body">
        <div class="product-brand">{founders}</div>
        <div class="product-name">{name}</div>
        <div class="product-desc">{desc}</div>
        <a href="{link}" target="_blank" rel="noopener" class="product-link">Visit {brand} &#8599;</a>
      </div>
  </div>'''

MAKERS = [
 ("jan-craig", "Jan Craig Headcovers", "Jan Craig, founder &middot; Janet Craig Cruise, third generation",
  "Jan Craig Headcovers &middot; Hand-knit since 1962",
  "The oldest brand in this post and the one with the best bag résumé. Jan was an avid golfer who could not find covers she liked for a new set, so she knitted her own on a rural route outside Cincinnati with a shared party phone line. Jack Nicklaus ordered a set in the mid-sixties and the thing took off. Tom Watson and multiple Ryder Cup teams carried them. Still hand-knit to order in 100% worsted wool, eight to ten weeks out, $63 to $79 &mdash; the only design change in six decades was adding elastic inside the driver covers.",
  "https://www.jancraigheadcovers.com/"),
 ("seamus", "Seamus Golf", "Megan Chisti, co-founder with her husband Akbar",
  "Seamus Golf &middot; Oregon wool, Scottish mills",
  "Started in a garage in 2011 when a Royal Troon headcover Akbar had been given wore out and Megan &mdash; then a womenswear designer at Pendleton Woolen Mills &mdash; rebuilt it from factory remnants. That is the whole origin: the company is made of Pendleton scrap. Pendleton later became a licensed partner rather than the other way round. First order was Bandon Dunes. Covers run $110 to $140 in wool, leather, waxed canvas and tweed. The company registers as women and minority owned.",
  "https://www.seamusgolf.com/pages/our-story"),
 ("bluetross", "Bluetross", "Gail Hanson, co-founder with her husband Marc",
  "Bluetross &middot; Horween leather, Charleston",
  "The origin object was a pin flag from Newport Country Club that Marc wanted to turn into a headcover for his brother. It still hangs in the production facility, unmade, while the company it accidentally spawned sells $225 versions of the idea. The first prototypes came off Gail's inherited sewing machine, which Marc destroyed inside a month. Italian vachetta and Horween leather, the stuff of luxury handbags, built to patina rather than wear out. Belts, wallets and scorecard covers too.",
  "https://bluetross.com/pages/our-story"),
 ("daphnes", "Daphne&rsquo;s Headcovers", "Jane Spicer, co-founder with her mother Daphne",
  "Daphne&rsquo;s Headcovers &middot; Est. 1979",
  "They invented the animal headcover, and they made Frank &mdash; the tiger Tiger Woods first carried at the 1997 Masters, after which business grew 400% in a quarter. Nike licensed the character and named him. Spicer's one condition was that he stay likable, because her late mother's actual signature is stitched into the label of every cover the company makes. A hundred-plus designs, flat $45.99: wolf, shark, bass, rattlesnake, Nicklaus's Golden Bear.",
  "https://daphnesheadcovers.com/"),
 ("mackem", "Mackem Golf", "Paige Harding, co-founder with her partner Adam Brown",
  "Mackem Golf &middot; Perth, Western Australia",
  "Named for the slang term for natives of Sunderland, which is where Adam is from. Paige has the textiles background and does the pattern-making and construction &mdash; Adam calls her the brains and the brawn of it. Everything is cut and sewn in their own Kalamunda studio rather than outsourced: wool, houndstooth, corduroy, waxed canvas, tartan, plus a line built from reclaimed materials. Covers A$85 to A$95, rangefinder and valuables pouches to A$125.",
  "https://mackemgolf.com/pages/about-us"),
 ("zaleas", "Zalea&rsquo;s Golf Co.", "Zoe Walker-Faure, founder",
  "Zalea&rsquo;s Golf Co. &middot; Hand-sewn, Palm Desert",
  "Said plainly: this is the one brand here that does not market to men. The homepage reads Headcovers Made for HER GAME and every description names a lady golfer. It is in this post because the gingham and stripe patterns are neutral enough to sit on anyone's bag, and because the operation is genuinely remarkable &mdash; started as a dorm-room Etsy shop, still cut by her mother and sewn by her grandmother, prints all drawn by Zoe herself. Twice a year the scrap becomes one-off covers. $70.",
  "https://www.zaleasgolf.com/"),
]

OUTFITTERS = [
 ("orkai", "ORKAI", "Deborah and Erica Bennett, married co-founders",
  "ORKAI &middot; Bags, formerly ORCA Golf",
  "The only brand in this post founded by two women and no man &mdash; Deborah is CEO, Erica is president and chief designer. Official bag supplier to all eight teams at the 2023 LPGA International Crown. Hand-finished in Boca Raton in vegan Nappa rather than hide. They rebranded from ORCA Golf in January 2026 to push into travel and lifestyle. The mark is an orca's fluke, chosen because no two are alike. Retail bags from $275; bespoke commissions to $1,580.",
  "https://orkai.life/"),
 ("hedge", "Hedge", "Meagan Ouderkirk and Antonia DiPaolo, co-founders",
  "Hedge &middot; New York and the Hamptons",
  "Conceived on a tennis court at the Bridgehampton Club out of frustration with kit designed mostly by men. Ouderkirk came from Ralph Lauren. The range is the strangest in golf in the best way &mdash; a $99.99 Sunday bag and $29.99 Cabretta gloves next to a caddie brooch and a stroke-counter bracelet handmade by a named jeweller. Their collab with Criquet exists because golfers at the 2018 PGA Show joked the two brands were dating; they made it real a year later.",
  "https://hedgenewyork.com/"),
 ("sinking-birdies", "Sinking Birdies", "Christina Rogers, co-founder with Mark Williams",
  "Sinking Birdies &middot; Hampshire, England",
  "Bold graphic prints on the things you actually lose &mdash; AAA Cabretta gloves at &pound;18, magnetic microfibre towels, PU driver and mallet covers, bamboo tees, a leather glove case. No florals anywhere. Note how we verified this one: the brand's own site names no founder at all, and the single piece of UK trade press about them names nobody either. Christina Rogers exists in connection with this company in exactly one place &mdash; a Companies House filing dated 4 July 2023, the day it incorporated.",
  "https://www.sinkingbirdies.co.uk/"),
 ("devant", "Devant Sport Towels", "Mary Ann Sheppard, founder",
  "Devant Sport Towels &middot; Fifty years old this year",
  "Began in 1976 when Mary Ann volunteered to take on the small short-run orders a big contract mill could not be bothered with. It now makes over a million towels a year in Pageland, South Carolina and holds licences with the USGA, the PGA of America, the PGA Tour and the LPGA &mdash; which means the towel on the bag at the U.S. Open traces back to her. Fifty years of continuous trading is rare for anyone and close to unheard of for a woman-founded hard-goods company. $12.95 to $24.95.",
  "https://bagboy.com/pages/home-devant"),
 ("inside-story", "Inside Story Socks", "Isabelle Shee, co-founder",
  "Inside Story &middot; Coffee grounds and bottles",
  "Shee was a college golfer at UC Riverside and then UNLV who got the nickname Sock Girl for wearing over-the-knee socks as sun protection &mdash; a teenage workaround for her mother's sunscreen rules that turned into the company. She co-founded it in 2019 with Greg Ashton and her mother Kat. The yarn is nano-particled coffee grounds plus recycled bottle fibre, about 70% upcycled, and carries a four-year no-hole guarantee. Men's crew and calf from $18, collabs with GOLF and HONMA.",
  "https://insidestory.co/"),
]

LABELS = [
 ("kingfisher", "Kingfisher Golf", "Fiona Cohen, founder",
  "Kingfisher Golf &middot; Dallas menswear",
  "The inversion of everything else on this list: a woman designing men's clothes, with no women's line at all. Cohen was an art director at PepsiCo doing animation and motion design, and started this at a kitchen counter in East Dallas with a sewing machine and thrift-store fabric. Tees are screen-printed at a shop in Old East Dallas; the polos come out of the same factories that make the big performance brands. Its breakout was a citywide open call to find the worst golfer in Dallas. Polos $65, tees $40.",
  "https://kingfisher-golf.com/collections/polos"),
 ("rhoback", "Rhoback", "Kristina Loftus, co-founder with her husband Matt and Kevin Hubbard",
  "Rhoback &middot; Charlottesville, Virginia",
  "Before there was a warehouse there was a camper. Kristina was the first of the three to go full time, and spent the brand's first two years towing a pop-up cross-country and selling shirts out of parking lots &mdash; 25,000 miles of it. She built the original website and taught herself the software to do it. Named after their Rhodesian Ridgeback; the two vertical stripes on the back of every piece are the ridge. Men's performance polos $98, vests $154, quarter-zips $145.",
  "https://www.rhoback.com/collections/mens-golf-collection"),
 ("malbon", "Malbon Golf", "Erica Malbon, co-founder with her husband Stephen",
  "Malbon Golf &middot; Los Angeles",
  "Began as an Instagram mood board. Erica came in having co-founded The Now, an LA massage business, with no background in sport or retail at all. The brand launched menswear first in 2017 and did not add a proper women's line until 2023 &mdash; her own account is that they started with men's because that is where the market was. She is co-chief creative officer today, a title she kept when an outside CEO came in. Tees $68, polos $108 to $148, outerwear to $348.",
  "https://malbongolf.com/"),
 ("bunker-mentality", "Bunker Mentality", "Tamasine Green, co-founder with Robert Hart",
  "Bunker Mentality &middot; Nottinghamshire, England",
  "Twenty-plus years independent, which almost nothing in this category manages. The interesting part is recent: they abandoned stocked inventory altogether and moved to made-to-order, so each garment is printed, cut and sewn only once you have bought it and ships straight from a UK factory. No warehouse, no overproduction, no discount cycle. Twenty-four sizes across three body lengths as standard. Men's polos &pound;70, gilets &pound;110.",
  "https://bunker-mentality.com/pages/about-us"),
 ("royal-albartross", "Royal Albartross", "Alex Bartholomew, sole founder",
  "Royal Albartross &middot; Italian and Portuguese leather",
  "One of very few luxury footwear houses in golf founded by a woman, and she trained for it &mdash; fashion and textiles at Brighton, then shoemaking at Cordwainers, then LK Bennett, Burberry and the British Leather Technology Centre. Made in small family-run factories in Italy and Portugal on Vibram soles. The name is a love letter hiding in plain sight: Al Bart for Alex Bartholomew, Ross for her husband, wrapped around the golf term. Men's spikeless $160 to $260, belts $50.",
  "https://us.albartross.com/collections/mens-spikeless-golf-shoes"),
 ("duca-del-cosma", "Duca del Cosma", "Antje Elle, co-founder with Baldovino Mattiazzo",
  "Duca del Cosma &middot; Founded 2004, since sold twice",
  "Included in the past tense and labelled as such. Antje Elle, trained at the Munich School for Fashion Graphic Design, co-founded this with the Venetian designer Baldovino Mattiazzo in 2004; the name means Duke of Cosma, a family name from his side. Neither founder owns it now &mdash; it went to a Dutch shoe-industry veteran around 2015 and again in May 2026 to a Dubai investment firm. So a brand still selling twenty years of Italian heritage has not been owned by either founder for a decade. Men's from $100.",
  "https://ducadelcosma.us/pages/our-story"),
]

def section(hid, h2, strong, kicker, items):
    return (f'<h2 id="{hid}">{h2}</h2>\n'
            f'<p class="cat-kicker"><strong>{strong}</strong>{kicker}</p>\n'
            f'<div class="products-grid">\n' + "\n".join(card(*it) for it in items) + '\n</div>\n')

def quote(text, attr):
    return ('\n<div class="pull-quote">\n'
            f'  <div class="pull-quote-inner">&ldquo;{text}&rdquo;'
            f'<span class="pull-quote-attr">&mdash; {attr}</span></div>\n</div>\n')

Q1 = quote(
  "Well, you know, I think that business is just like hiking, really&hellip; Some days it&rsquo;s great, "
  "you&rsquo;re on top of the summit. Some days it&rsquo;s rainy and muddy, and it stinks. Some days "
  "you&rsquo;re banged up; some days you&rsquo;re on top of the world. But if you continue going, it&rsquo;s "
  "always worthwhile.",
  "Jane Spicer, CEO, Daphne&rsquo;s Headcovers")
Q2 = quote(
  "ORKAI started in my studio, with one bag, one client, one story. Every piece since has carried that same "
  "intention &mdash; designed by hand, made for one. The brand has grown. The standard hasn&rsquo;t moved.",
  "Erica Bennett, co-founder and chief designer, ORKAI")
Q3 = quote(
  "I was an awful employee. I can&rsquo;t tell you how many times my &lsquo;washing machine flooded&rsquo; and "
  "I was ridiculously late for work. I simply could not motivate myself to go to work for anyone else &mdash; "
  "even in my 20&rsquo;s.",
  "Alex Bartholomew, founder, Royal Albartross")

products = (
 section("makers", "The Makers", "Six &middot; headcovers and leather",
   "Brands where a woman is the one physically cutting and sewing the product &mdash; a 1962 hand-knitting "
   "operation, a Pendleton designer working in factory scrap, and a leather shop built on an inherited sewing machine.",
   MAKERS)
 + Q1 +
 section("outfitters", "The Outfitters", "Five &middot; bags, gloves, towels, socks",
   "The things that hang off the bag or go in it. Two of these have been trading since the seventies and "
   "one was verified through a government filing because nobody involved will put their name on the website.",
   OUTFITTERS)
 + Q2 +
 section("labels", "The Labels", "Six &middot; apparel and footwear",
   "Brands cutting an actual men's line, including one that sells nothing else, one that started as a camper "
   "towed across America, and one Italian shoe house that has not been owned by its founders for a decade.",
   LABELS)
 + Q3
)

FAQS = [
 ("Which golf brands are founded by women?",
  "Seventeen are covered here, all currently trading with stock: Jan Craig Headcovers, Seamus Golf, Bluetross, Daphne's Headcovers, Mackem Golf, Zalea's Golf Co., ORKAI, Hedge, Sinking Birdies, Devant Sport Towels, Inside Story Socks, Kingfisher Golf, Rhoback, Malbon Golf, Bunker Mentality, Royal Albartross and Duca del Cosma. Each founder is named from a brand-owned page, a signed interview or a company filing."),
 ("Are there women-founded golf brands that make men's clothing?",
  "Yes, six of them here. Kingfisher Golf makes men's polos and tees and nothing else — founder Fiona Cohen designs no women's line at all. Rhoback, Malbon and Bunker Mentality all run full men's ranges, Royal Albartross makes men's leather golf shoes, and Duca del Cosma makes men's Italian footwear."),
 ("Who made Tiger Woods' tiger headcover?",
  "Daphne's Headcovers, the Phoenix company Jane Spicer started with her mother Daphne in 1979. Woods first carried it at the 1997 Masters. Nike later licensed the character and named him Frank. Daphne's covers are a flat $45.99."),
 ("What is the oldest women-founded golf brand?",
  "Jan Craig Headcovers, founded in 1962 by Jan Craig, who knitted her own covers because she could not find any she liked. Jack Nicklaus ordered a set in the mid-1960s. Devant Sport Towels is next at 1976, and Daphne's at 1979."),
 ("Is Seamus Golf women-owned?",
  "Partly. Megan Chisti co-founded it in 2011 with her husband Akbar, and the company registers as women and minority owned. Megan was a womenswear designer at Pendleton Woolen Mills and rebuilt the original headcover from Pendleton remnants — though nearly every published quote about the company is Akbar's."),
 ("Which of these brands make headcovers?",
  "Six. Jan Craig hand-knits wool covers to order. Seamus works in Scottish wool, leather and waxed canvas. Bluetross uses Horween and Italian leather. Daphne's makes the novelty animals. Mackem Golf sews wool and corduroy in Perth. Sinking Birdies does bold-print PU."),
 ("Do any of these brands make golf bags?",
  "Two. ORKAI, founded by Deborah and Erica Bennett, makes stand and cart bags from $275 and was the official bag supplier to all eight teams at the 2023 LPGA International Crown. Hedge makes a $99.99 Sunday bag."),
 ("Why isn't Rose & Fire on this list?",
  "It is not women-owned, though it is very often assumed to be. It was founded by Mike Buchfuhrer. Rose was his grandmother, who designed hats after the Second World War, and Fire is a play on his surname."),
 ("What happened to KINONA and PRIO Golf?",
  "Both appear in most articles on this subject and neither has a working store. KINONA's domain redirects to an unrelated site and PRIO's has lapsed to a parking page. LIJA and Jamie Sadock don't resolve at all. That is why this list was rebuilt from live stores rather than from other lists."),
 ("How were these brands verified?",
  "Every founder had to be named in a source we opened — a signed About page, a named interview, or in one case a Companies House filing — rather than inferred from a brand seeming women-led. Every store was checked for live stock. Birds of Condor was cut because its own About page names no founder and only one local paper credits a woman co-founder."),
 ("Where should I start if I only buy one thing?",
  "An object with history: a Jan Craig hybrid cover at $63, hand-knit the same way since 1962. Cheapest way in: Inside Story men's calf socks at $18, or a Devant towel at $12.95. For clothing: a Kingfisher polo at $65."),
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
    <p>Start with the thing that kept happening while we reported this out. Seamus Golf was
    founded by Megan and Akbar Chisti. Megan was the trained designer, she rebuilt the headcover
    that started the company, and she still sews product &mdash; and there is not a single
    published quote from her anywhere. Bluetross was founded by Gail and Marc Hanson. The first
    prototypes came off Gail&rsquo;s inherited sewing machine. The biggest feature ever written
    about the company is headlined &ldquo;the unlikely story of a man who quit his job to make
    leather headcovers,&rdquo; and she appears in it twice, once as the source of the machine.</p>
    <p>Neither brand is hiding anything. Both credit her plainly on their own About page. The
    voice just defaults to him.</p>
    <p>So this is seventeen golf brands founded or co-founded by women, filtered to the ones
    making things men actually buy &mdash; headcovers, leather, bags, gloves, towels, socks,
    polos, shoes. That filter turned out to be the hard part. Almost every women-founded golf
    brand makes women&rsquo;s apparel and nothing else, and almost every independent brand
    making unisex hard goods was founded by men. The overlap is thin, and finding it meant
    checking dozens of names one at a time.</p>
    <p>The rule was: name the woman, cite where we found her, and confirm the store still has
    stock in it. Where someone co-founded with a husband or a mother, we say so rather than
    rounding up. One brand was cut outright because the only place a woman is called co-founder
    is a photo caption in a hometown newspaper. One is included with a caveat printed on it.
    The oldest has been hand-knitting since 1962 and once dressed a Ryder Cup team; the newest
    started at a kitchen counter last year.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>17</span></div>
      <div class="sidebar-detail"><span class="l">Oldest</span><span>1962</span></div>
      <div class="sidebar-detail"><span class="l">Newest</span><span>2025</span></div>
      <div class="sidebar-detail"><span class="l">Checked</span><span>Aug 2026</span></div>
      <a href="/brands/" class="sidebar-cta">Browse the Brand Index &rarr;</a>
      <div class="hashtags">
        <span class="hashtag">#TheGrassyIssue</span>
        <span class="hashtag">#WomenInGolf</span>
        <span class="hashtag">#IndependentGolf</span>
        <span class="hashtag">#BrandsToKnow</span>
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
           lambda m: f'<script type="application/ld+json">{art_ld}</script>')
head = rep(head, r'<script type="application/ld\+json">\{"@context": "https://schema\.org", "@type": "FAQPage".*?</script>',
           lambda m: f'<script type="application/ld+json">{faq_ld}</script>')
head = rep(head, r'(<div class="breadcrumb">.*?<span>/</span>\s*)[^<]*?(</div>)', lambda m: m.group(1) + TITLE_TXT + m.group(2))
head = rep(head, r'<h1>.*?</h1>', f'<h1>{TITLE}</h1>')
head = rep(head, r'<div class="drop-meta">.*?</div>',
           '<div class="drop-meta">\n    <span>17 Brands</span><span>&middot;</span>'
           '<span>Men&rsquo;s and unisex &middot; Founders named &middot; Stores checked Aug 2026</span>\n  </div>')
head = rep(head, r'<div class="drop-hero"><div class="drop-hero-img"><img src="[^"]*" alt="[^"]*"[^>]*/></div></div>',
           f'<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}hero.jpg" '
           f'alt="A golfer carrying a leather bag in a Kingfisher Golf polo, the Dallas menswear label founded by Fiona Cohen" /></div></div>')
head = rep(head, r'<div class="writeup">.*?</div>\s*</aside>\s*</div>', lambda m: WRITEUP)
head = rep(head, r'</style>', CSS + '</style>')

tail = rep(tail, r'<div class="more-grid">.*?</div>\s*</section>',
'''<div class="more-grid">
    <a href="/drops/brand-to-know-kingfisher-golf" class="more-card"><div class="more-kicker">Brand to Know</div><div class="more-title">Kingfisher Golf &mdash; the Dallas Label Founded by Fiona Cohen</div></a>
    <a href="/drops/brand-to-know-seamus" class="more-card"><div class="more-kicker">Brand to Know</div><div class="more-title">Seamus Golf, the Oregon Workshop That Covered a Ryder Cup Team</div></a>
    <a href="/drops/brand-to-know-sun-mountain" class="more-card"><div class="more-kicker">Brand to Know</div><div class="more-title">Sun Mountain, the Montana Company That Put Legs on the Golf Bag</div></a>
  </div>
</section>''')

page = head + '<section class="products">\n' + products + '\n<div class="faq">\n' + faq_html + '\n  </div>\n</section>' + tail
open(OUT, "w", encoding="utf-8").write(page)
words = len(re.sub(r'<[^>]+>', ' ', page).split())
nbrands = len(MAKERS) + len(OUTFITTERS) + len(LABELS)
print(f"wrote {OUT} ({len(page):,} bytes, ~{words:,} words, {nbrands} brands)")
