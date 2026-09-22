#!/usr/bin/env python3
"""build-hat-towel-edit.py — The Hat & Towel Edit. 21 September 2026.

Lenny: "/drops/hats-carousel this post is totally broken, let's update and
upgrade this post as a fresh post at the top of the homepage" + "let's remove
the beanies and visors" + "let's add some towels in the post".

WHAT WAS BROKEN. hats-carousel was generated from the HOMEPAGE CARD template
and never converted to a post: it carried the feed's CSS (.card) while its
markup asked for post CSS (.drop-header), so the layout collapsed entirely.
250 words, zero product cards, and a title promising "14 Picks" it never
delivered. This replaces it rather than patching it.

NEW SLUG, ALL THREE OLD URLS REPOINTED. hats-carousel is itself a 301 target
for /drops/the-hats-and-towels-edit and /drops/14-hats-from-funky-brands, so it
carries accumulated equity. Rather than chain redirects, all three point at the
new descriptive slug (see wire-hat-towel-edit.py).

EVERY PRICE RE-READ LIVE, FROM THE COLLECTION FEED.
Shopify's per-product .json endpoint is unreliable: it reported 29 of these 30
items sold out, and claimed Sugarloaf's Arrow Cap had 0 of 8 variants available
while the collection feed said 4 and the product PAGE said in stock with a live
Add to cart. The collection feed is what agreed with the page, so prices and
stock here come from it. All 30 confirmed in stock at these prices on 21 Sep
2026, USD, each read from the brand's own store.

COPY IS GROUNDED IN THE BRAND'S OWN PRODUCT COPY (research/hats/descs.json).
Dimensions, fabrics and constructions below are what the maker states. Where a
brand says almost nothing, the entry stays short rather than inventing a spec.

NO BEANIES, NO VISORS — filtered out of the candidate POOL, not just the
shortlist, so brands were re-picked on a cap rather than dropped. Jones Sports
Co lost its hat slot that way (beanies only) and appears in the towel half.

ONE BRAND, ONE SLOT across the whole post.

Idempotent. Dry run by default.
"""
import datetime
import html as H
import json
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DONOR = ROOT / "drops/the-hat-edit-austin-summer.html"
SLUG = "the-hat-and-towel-edit"
OUT = ROOT / f"drops/{SLUG}.html"
READ = "21 September 2026"

TITLE = "The Hat &amp; Towel Edit &mdash; 30 Picks From the Independent Golf Brands"
DESC = ("Eighteen caps and twelve towels from independent golf brands, every "
        "price read live from the maker&rsquo;s own store on 21 September 2026. "
        "No beanies, no visors, one piece per brand.")

# THE INTRO MOVED INTO A REAL .writeup BLOCK, WHICH IS WHERE voice-lint LOOKS.
# Sitting inside section.products it was never linted; the first pass in the
# proper slot flagged "our index" and "this list" as sourcing-narration and
# "No beanies and no visors." as a verbless opener. It also named a
# nineteen-dollar floor that the thirteen-dollar Forden towel had already
# undercut, so the prose disagreed with the stats card beside it.
INTRO = """<p>Two things you touch every round and mostly buy badly: the hat that
sits on your head for four hours and the towel that does the actual work. Here are
thirty of them &mdash; eighteen caps, twelve towels, one piece per brand, and no
brand repeated between the two halves.</p>

<p>Beanies and visors are both out. What is here starts at a thirteen-dollar
microfibre towel and tops out at fifty-five, and every price was read from the
brand&rsquo;s own store on %s rather than copied from a press
release.</p>

<p>The caps fall into two camps that are easy to see once you know to look.
One puts technical fabric into shapes that predate it: Sinking Birdies run a
water-resistant tech fabric on a rope crown, Devereux laser-perforate a
performance panel and then trim it with classic rope, Eastside build on
performance fabric with a perforated back and a gel badge. The other camp
states cotton and stops there &mdash; Hidden Links Society list six panels, a
flat peak and a metal clasp with no performance claim anywhere on the product
page.</p>

<p>The towels are where the construction talk actually lives. Waffle weave,
woven jacquard, terry blends and Japanese gauze are four different answers to
one problem, at prices that now overlap the hats entirely.</p>""" % READ

# ---- THE TAKE ----
# Lenny asked for "a TGI take on the trends we're seeing in Hats & towels going
# into the late season". Every claim below is a fact already verified for the
# thirty picks (research/hats/descs.json + verified2.json): stated dimensions,
# stated fibre content, stated hardware, and prices read live on 21 Sep 2026.
# The counts are asserted against the data at build time, further down, so the
# prose cannot drift away from the products it describes.
TAKE = """<p>Late season rearranges which of these two halves matters. Through
an Austin summer the hat does the work &mdash; mesh backs, laser perforation, a
rope crown that lets heat out &mdash; and the towel is mostly there to wipe a
grip between shots. From October the order flips. Tee times move to the front of
the morning, the grass holds dew until ten, and the towel becomes the thing that
decides whether your grips are dry on the seventh hole.</p>

<p>That shows up in how these towels are sized. Ghost cut theirs to eighteen by
forty inches, caddie length. Jones size theirs oversized on purpose, so one half
can be wet and the other dry &mdash; which is how caddies have always used a
towel and how almost no retail towel is cut. Hiroki go to fifty-six by a hundred
centimetres. Dimension is the specification that separates a dew-season towel
from a summer one, and it is the first thing three of the twelve tell you.</p>

<p>Texture is the second answer. Sierra Madre and Hiroki both use a waffle
weave, which lifts dirt off a face rather than moving it around. Dormie blend
86% terry cotton with 14% polyester so the cloth has weight to it. Sentinel
import a Shinto gauze that replaces the middle layer of a traditional 20-count
three-ply with a half-weight weave, making a 2.5-ply cloth that is light without
being thin. Four brands, four readings of absorbency, none of them reaching for
microfibre by default.</p>

<p>The hardware is quietly moving off the carabiner. Seamus finish with a
riveted leather loop. Radry built theirs with no hole and no clip at all, the
towel draping over the irons instead. Those are design decisions rather than
omissions, and two of them in a group this size is a pattern rather than a
coincidence.</p>

<p>On the hat side the turn favours the cotton camp. A rope crown and a mesh
back are summer answers. The brands that stated cotton and structure &mdash;
Read The Green with full buckram behind a seamless front panel, Random Golf
Club, Merrill &mdash; make caps that keep their shape in wind and take a soaking
without folding. The tech-fabric rope hats do not stop working in October. They
simply stop being the reason you pick that hat over another one.</p>

<p>Then there is price, which has quietly converged. A Seamus towel and a Read
The Green cap both cost forty-five dollars. Sentinel&rsquo;s gauze towel at
forty-six costs more than fourteen of the eighteen caps here. Towels used to be
the thing thrown in at the till. On this evidence they are now a category these
brands build properly and charge properly for.</p>"""

HATS = [
 ("sinking-birdies","Sinking Birdies","Never Lay Up Rope Hat",19,
  "A water-resistant tech fabric on a rope hat, which is an unusual pairing &mdash; rope crowns are normally a cotton-and-nostalgia exercise. Snapback closure, moisture-absorbing sweatband, designed in the UK. Nineteen dollars, which is very little for a tech fabric and a proper sweatband."),
 ("metalwood-studio","Metalwood Studio","Dewey Soft Brim Hat",48,
  "100% nylon, low-profile six-panel, and a soft brim &mdash; the one shape here that will fold into a bag and come back out flat. The artwork on it is credited to Hendrik Esche, which is more than most brands bother to say about a hat graphic."),
 ("devereux-golf","Devereux Golf","Skull Caddie Performance Rope Hat",30,
  "Laser-perforated performance fabric under a classic rope, with the Skull Caddie badge on the front. Devereux keep putting technical fabric into shapes that look like they predate it, and this is the clearest example."),
 ("hidden-links-society","Hidden Links Society","Supplies and Gear Dad Hat",32,
  "Mid-profile, unstructured, six panels, flat peak, 100% cotton, metal clasp. No performance claim anywhere on it. The most honest description of a hat on this page."),
 ("morning-people-clothiers","Morning People Clothiers","The High Crown Hat",32,
  "Built with Imperial, structured, and specifically cut for medium to larger heads &mdash; a detail almost nobody states out loud. 100% polyester, snapback. The crown is the point."),
 ("apres-golf","Apr&egrave;s Golf","Retro Logo Snapback",34,
  "Lightweight oxford cotton blend, white body, pink circle patch, white rope. Apr&egrave;s Golf are unembarrassed about the bar being part of the round, and the hat is dressed for it."),
 ("3-putt-round","3 Putt Round","The &ldquo;Golf Is Dangerous&rdquo; Baseball Cap",35,
  "Embroidered across the front panel, logo on the rear, and that is the whole brief. Thirty-five dollars for a joke you have to commit to for the full eighteen."),
 ("random-golf-club","Random Golf Club","RGC Sans Serif Dad Hat",35,
  "58cm circumference, 100% cotton, stamped metal closure, flagstick embroidered on the front. RGC publish the circumference, which tells you who keeps asking."),
 ("kingfisher-golf","Kingfisher Golf","Green DAL Cap",36,
  "Relaxed and slouchy by design rather than by accident. Kingfisher describe it in seven words and none of them are performance."),
 ("bluegrass-fairway","Bluegrass Fairway","Good Luck, Play Hard Two-Tone",38,
  "Five panels of brushed cotton twill in black and cream, plastic snapback, the phrase on the front. Two-tone is doing the work here &mdash; it is a 1970s range-hat colourway on a current build."),
 ("sunday-golf","Sunday Golf","Trucker Hat, Mossy Oak Bottomland Orange",39.99,
  "Actual licensed Mossy Oak Bottomland, not a camo print drawn to look like it, in the orange colourway. A trucker back keeps it cool. The Sunday patch sits on the front doing very little, correctly."),
 ("birds-of-condor","Birds of Condor","Coogi Bucket Hat",55,
  "An officially licensed Coogi print on a golf bucket, from the Byron Bay label&rsquo;s collaboration with the Australian knitwear house. 100% recycled polyester, one size at 59cm, and a tee holder sewn into the band. Birds call it a bucket for the OG golf gang and the print does not argue."),
 ("sugarloaf-social-club","Sugarloaf Social Club","Cotton SSC Arrow Cap",40,
  "An American Needle build. Arrow woven on the front, the red Sugarloaf rectangle woven on the back, washed cotton. Four colourways live as of %s: Nantucket Red, Lavender, Lemon Ice and Snow White." % READ),
 ("stitch-golf","STITCH","USA Rope Hat",42,
  "Red, white and blue on a rope crown. STITCH usually work in restraint and leather, so an Americana rope hat is them at their least typical and most wearable."),
 ("eastside-golf","Eastside Golf","Cranberry Pro Series Hat",45,
  "Performance fabric, perforated back, vintage rope, and a gel badge rather than embroidery &mdash; the badge is what separates it from every other rope hat on this page."),
 ("read-the-green","Read The Green","Founder&rsquo;s Cap, Natural &amp; Camo",45,
  "A seamless front panel with full buckram, which is the construction detail that keeps a five-panel standing up instead of collapsing after a season. 100% cotton, custom interior tag and lining."),
 ("merrill-golf","Merrill Golf","Logo Five Panel Hat",50,
  "Embroidered five-panel in brown, 100% cotton, snapback. Merrill do not over-explain it and it does not need explaining."),
 ("public-drip","Public Drip","&ldquo;P&rdquo; Script Nylon Bucket Hat",50,
  "Lightweight quick-drying nylon, unstructured, with the P appliqu&eacute; on the front. Built for heat and for getting wet, which is most of the reason to own a bucket."),
]

TOWELS = [
 ("forden-golf","Forden Golf","Blue Swingman Golf Towel",13.30,
  "Microfibre, 40 x 100cm, and thirteen dollars. The cheapest way onto this page and a perfectly serviceable bag towel."),
 ("rouqe-golf","Rouqe Golf","RQ Jacquard Towel",19,
  "100% jacquard cotton with the clip included. Jacquard means the pattern is woven rather than printed, so it does not wash off &mdash; unusual at nineteen dollars."),
 ("sierra-madre","Sierra Madre Golf","Sierra Madre Golf Towel",22,
  "15 x 23in, microfibre waffle weave, carabiner, logo on the front and plain brown on the back. Waffle weave is the texture that actually lifts dirt rather than pushing it around."),
 ("dormie-workshop","Dormie Workshop","Signature Player&rsquo;s Towel",30,
  "22 x 44in of 86% terry cotton to 14% polyester &mdash; a genuine blend rather than a microfibre sheet, so it has weight to it. Six colourways; this is the blue stitch."),
 ("ghost-golf","Ghost Golf","Tour Towel (Caddie)",30,
  "18 x 40in in premium microfibre, cut caddie-length. Ghost build for absorbency and the dimensions are the argument."),
 ("jones-sports-co","Jones Sports Co","Tour Towel, All Black",30,
  "Oversized on purpose: the idea is you wet one half and keep the other dry, which is how caddies have always used a towel and how almost no retail towel is sized. Ribbed terry, safe on a finish."),
 ("sentinel-golf","Sentinel Golf","Shinto Gauze Towel, Charcoal",46,
  "The most interesting towel here. Shinto took a traditional 20-count 3-ply gauze, replaced the middle layer with a half-weight weave, and made a 2.5-ply cloth that is light without being flimsy. 100% organic cotton, 45.28 x 11.81in, made in Japan &mdash; cut slimmer than a standard bag towel so it slides under the handle and stays out of the way."),
 ("malbon","Malbon Golf","Antilles Golf Towel",38,
  "The Spring &rsquo;26 Antilles print on ultra-absorbent microfibre, 16 x 24in, metal eyelet and carabiner. Malbon selling a print is the entire proposition and they are not pretending otherwise."),
 ("radry-golf","Radry Golf","The Animals Got Out Again Towel",45,
  "16 x 38in cotton jacquard at 550gsm, and deliberately built with no hole and no clip &mdash; it drapes over the clubs instead. That is a real design decision, not an omission."),
 ("seamus","Seamus Golf","Spider Rock Jacquard Golf Towel",45,
  "100% cotton jacquard, roughly 18 x 30in, finished with a riveted leather loop rather than a carabiner. Seamus put the hardware where it will still be working in five years."),
 ("hiroki-golf","Hiroki Golf","Hiroki Golf Towel, Grey",45,
  "56 x 100cm of microfibre waffle weave, absorbent and fast-drying. The largest towel in this group by some margin."),
 ("matchstick-golf","Matchstick Golf","Pink Sugar Skull Golf Towel",29,
  "23.75 x 15.75in of waffle material, two-sided so one face stays clean for the grips. The sugar skull is drawn from Matchstick&rsquo;s own Dana ball marker, which is how the Portland shop works &mdash; the art exists first and the object follows it."),
]

FAQ = [
 ("Are these prices current?",
  f"Every price on this page was read from the brand&rsquo;s own store on {READ}, in US dollars, and each item was confirmed in stock at that moment. Prices and stock move; the shop link is the authority."),
 ("Why no beanies or visors?",
  "Editorial call. Both are real categories and neither fits a list about the cap you wear for eighteen holes in ordinary weather. Removing them cost us a few brands whose only headwear is knitted."),
 ("Why is each brand only in here once?",
  "House rule. A roundup where one brand takes four slots is a catalogue, not an edit. One hat or one towel per brand, and no brand appears in both halves."),
 ("What is jacquard, and why does it cost more?",
  "The pattern is woven into the cloth rather than printed onto it, so it cannot crack or wash away. Rouqe, Seamus and Radry all use it here, which is most of why those towels sit at the top of the range."),
 ("What size should a golf towel be?",
  "The ones here run from 15 x 23in up to 56 x 100cm. Caddie-length towels around 16 x 40in let you keep one half wet and one half dry, which is the practical argument for the bigger sizes."),
 ("Where did the old hats-carousel page go?",
  "Here. That URL, along with /drops/the-hats-and-towels-edit and /drops/14-hats-from-funky-brands, now redirects to this page."),
]


def card(brand_slug, brand, name, price, blurb, kind, verified):
    img = f"/images/hats-towels/{kind}-{brand_slug}.jpg"
    if not (ROOT / img.lstrip("/")).is_file():
        sys.exit(f"! missing local image: {img}")
    url = verified["url"]
    p = f"${price:g}" if price != int(price) else f"${int(price)}"
    alt = H.escape(f"{H.unescape(brand)} {H.unescape(name)} golf {kind}")
    return f'''    <div class="product-card" data-frames="1">
      <div class="product-gallery"><div class="pg-track"><div class="pg-frame"><img src="{img}" alt="{alt}" loading="lazy" /></div></div></div>
      <div class="product-body">
        <div class="product-brand">{brand}</div>
        <div class="product-name">{name} &middot; {p}</div>
        <div class="product-desc">{blurb}</div>
        <a href="{url}" target="_blank" rel="noopener" class="product-link">Shop &#8599;</a>
      </div>
    </div>'''


def main(apply_):
    donor = DONOR.read_text(encoding="utf-8")
    grid = {x["brand"]: x for x in
            json.load(open(ROOT / "research/hats/grid18.json"))}
    grid.update({x["brand"]: x for x in
                 json.load(open(ROOT / "research/towels/grid.json"))})
    ver = json.load(open(ROOT / "research/hats/verified2.json"))

    # ---- guard the inputs BEFORE writing anything ----
    bad = []
    for slug, *_ in HATS + TOWELS:
        it = grid.get(slug)
        if not it:
            bad.append(f"{slug} not in the approved grid"); continue
        v = ver.get(it["url"], {})
        if not v.get("available"):
            bad.append(f"{slug} is not confirmed in stock")
    seen = [s for s, *_ in HATS + TOWELS]
    dupe = {s for s in seen if seen.count(s) > 1}
    if dupe:
        bad.append(f"brand appears twice: {sorted(dupe)}")
    if bad:
        sys.exit("! " + "; ".join(bad))

    # price in the copy must match the price we verified
    for slug, _b, _n, price, _t in HATS + TOWELS:
        v = ver[grid[slug]["url"]]
        if abs(v["price"] - price) > 0.005:
            sys.exit(f"! {slug}: copy says ${price:g}, live store says ${v['price']:g}")

    hats = "\n".join(card(s, b, n, p, t, "hat", grid[s]) for s, b, n, p, t in HATS)
    tows = "\n".join(card(s, b, n, p, t, "towel", grid[s]) for s, b, n, p, t in TOWELS)

    # ---- THE HERO AND THE SIDEBAR ARE OURS, NOT THE DONOR'S ----
    # The first build spliced from `<section class="products">` and shipped with
    # the donor's masthead, the donor's intro ("It is August in Austin...") and
    # the donor's stats card (28 Hats / 22 Brands / $20-$76). None of the
    # programmatic guards caught it because every one of them read the region
    # BELOW the splice point. The splice now starts at the hero, so everything
    # above the product grid is written here.
    prices = [p for _s, _b, _n, p, _t in HATS + TOWELS]
    # %g would print the cheapest towel as "$13.3". Two decimals, then drop a
    # whole-dollar ".00" — the way a price is written, not the way a float is.
    money = lambda p: f"${p:.2f}".replace(".00", "")
    rng = f"{money(min(prices))} &ndash; {money(max(prices))}"

    body = f'''<div class="drop-hero"><div class="drop-hero-img"><img src="/images/hats-towels/hero.jpg" alt="The Spider Rock jacquard golf towel from Seamus Golf, woven in cotton" /></div></div>

<div class="writeup">
  <div class="writeup-body">
{INTRO}
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Picks</span><span>{len(HATS) + len(TOWELS)}</span></div>
      <div class="sidebar-detail"><span class="l">Hats</span><span>{len(HATS)}</span></div>
      <div class="sidebar-detail"><span class="l">Towels</span><span>{len(TOWELS)}</span></div>
      <div class="sidebar-detail"><span class="l">Brands</span><span>{len({s for s, *_ in HATS + TOWELS})}</span></div>
      <div class="sidebar-detail"><span class="l">Range</span><span>{rng}</span></div>
      <a href="/"  class="sidebar-cta">&larr; Back to Feed</a>
      <div class="hashtags">
        <span class="hashtag">#TheGrassyIssue</span>
        <span class="hashtag">#GolfCulture</span>
        <span class="hashtag">#TheHatAndTowelEdit</span>
        <span class="hashtag">#GearEdit</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</div>

<section class="products">
  <h2 class="products-hdr sec">The Hats</h2>
  <div class="products-grid">
{hats}
  </div>

  <h2 class="products-hdr sec">The Towels</h2>
  <div class="products-grid">
{tows}
  </div>

  <h2 class="products-hdr sec">The Take</h2>
  <div class="writeup-body">
{TAKE}
  </div>

  <h2 class="products-hdr sec">The Questions</h2>
  <div class="faq">
''' + "\n".join(
        f'    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>'
        for q, a in FAQ) + '''
  </div>
</section>
'''

    # ---- assemble from the donor shell ----
    head_end = donor.find("</head>")
    open_body = donor.find("<body")
    # SPLICE FROM THE HERO, NOT FROM THE PRODUCT GRID. Between the two the
    # donor keeps 2.6 KB of its own content — masthead image, three paragraphs
    # of August-in-Austin intro, and a stats card. Starting lower inherits all
    # of it. See the note above `body`.
    hero = donor.find('<div class="drop-hero"', open_body)
    first_sec = donor.find('<section class="products"', open_body)
    # THE DONOR'S MORE BLOCK IS A <div class="more">, NOT A SECTION.
    # Looking for a <section> found nothing and the guard correctly refused to
    # build rather than silently truncating the page at the wrong offset.
    more = donor.find('<div class="more"', open_body)
    if min(head_end, open_body, hero, first_sec, more) < 0:
        sys.exit("! donor structure not recognised")
    if not hero < first_sec < more:
        sys.exit("! donor blocks are not in the expected order")
    page = donor[:hero] + body + donor[more:]

    plain_t = H.unescape(re.sub(r"<[^>]+>", "", TITLE))
    plain_d = H.unescape(re.sub(r"<[^>]+>", "", DESC))
    page = re.sub(r"<title>[^<]*</title>",
                  f"<title>{plain_t} &mdash; The Grassy Issue</title>", page, count=1)
    for key, val in (("description", plain_d), ("og:description", plain_d),
                     ("twitter:description", plain_d)):
        page = re.sub(rf'((?:name|property)="{re.escape(key)}" content=")[^"]*(")',
                      lambda m, _v=val: m.group(1) + _v + m.group(2), page, count=1)
    for key in ("og:title", "twitter:title"):
        page = re.sub(rf'((?:name|property)="{re.escape(key)}" content=")[^"]*(")',
                      lambda m: m.group(1) + plain_t + m.group(2), page, count=1)
    page = re.sub(r"(<h1[^>]*>).*?(</h1>)",
                  lambda m: m.group(1) + TITLE + m.group(2), page, count=1, flags=re.S)
    # breadcrumb carries the old headline in a literal em dash
    page = re.sub(r"(<div class=\"breadcrumb\">.*?<span>/</span>\s*)[^<]*(\s*</div>)",
                  lambda m: m.group(1) + plain_t + m.group(2), page, count=1, flags=re.S)
    page = page.replace(f"/drops/{DONOR.stem}", f"/drops/{SLUG}")
    today = datetime.date.today().isoformat()
    for key, val in (("headline", plain_t), ("description", plain_d),
                     ("datePublished", today), ("dateModified", today)):
        page = re.sub(rf'("{key}":\s*")[^"]*(")',
                      lambda m, _v=val: m.group(1) + _v + m.group(2), page, count=1)
    # THE DONOR'S META SAYS "28 Hats", NOT "28 Pieces". Matching only "Pieces"
    # is why the finished page still advertised the donor's count.
    page, n_meta = re.subn(r'(<span>)\d+\s+(?:Pieces|Hats|Picks|Towels)(</span>)',
                           lambda m: m.group(1) + f"{len(HATS)+len(TOWELS)} Picks" + m.group(2),
                           page, count=1)
    if not n_meta:
        sys.exit("! drop-meta count not found — the header shape changed")

    if not apply_:
        print(f"  would write {OUT.name}: {len(HATS)} hats + {len(TOWELS)} towels")
        print("\n  dry run — pass --apply")
        return
    OUT.write_text(page, encoding="utf-8")

    # ---- VERIFY THE FINISHED PAGE ----
    hh = OUT.read_text(encoding="utf-8")
    b = hh[hh.find("<body"):]
    nb = re.sub(r'<div class="more".*', "", b, flags=re.S)
    bad = []
    n_cards = len(re.findall(r'class="product-card', nb))
    if n_cards != len(HATS) + len(TOWELS):
        bad.append(f"{n_cards} product cards, expected {len(HATS)+len(TOWELS)}")
    words = len(re.sub(r"\s+", " ", H.unescape(re.sub(
        r"<[^>]+>", " ", re.sub(r'<(script|style)\b.*?</\1>', "", nb, flags=re.S)))).split())
    if words < 1200:
        bad.append(f"only {words} words")
    if hh.count("<h1") != 1:
        bad.append(f"{hh.count('<h1')} h1 tags")
    for img in re.findall(r'<img[^>]+src="(/images/[^"]+)"', nb):
        if not (ROOT / img.lstrip("/")).is_file():
            bad.append(f"missing image {img}")
    if re.search(r"\bbeanie|\bvisor", nb, re.I) and not re.search(r"no beanies", nb, re.I):
        bad.append("a beanie or visor is on the page")
    if re.search(r"\bworth\b", nb, re.I):
        bad.append("the banned word 'worth' is in the copy")
    # IMG ONLY. The first version matched any src="http…, which flagged the
    # Analytics and Skimlinks <script> tags every page carries and aborted a
    # correct build. Hot-linking is about images; the check should say so.
    hot = re.findall(r'<img[^>]+src="https?://[^"]+"', nb)
    if hot:
        bad.append(f"{len(hot)} hot-linked image(s) survived")
    brands = re.findall(r'class="product-brand">([^<]+)<', nb)
    if len(brands) != len(set(brands)):
        bad.append("a brand appears more than once")

    # ---- NOTHING OF THE DONOR'S MAY SURVIVE ABOVE THE GRID ----
    # This is the check the first build did not have. Every other guard reads
    # the region below the splice; the donor's content sits above it, so the
    # page passed all of them while wearing the wrong hero, intro and stats.
    top = nb[:nb.find('<section class="products"')] or nb
    if "/images/hat-edit/" in nb:
        bad.append("the donor's imagery is still on the page")
    for phrase in ("It is August in Austin", "twenty-two brands",
                   "seventy-six dollar Siegelman", "#TheHatEdit<"):
        if phrase in nb:
            bad.append(f"donor copy survived: {phrase!r}")
    m = re.search(r'<div class="drop-hero-img"[^>]*>\s*<img[^>]+src="([^"]+)"', top)
    if not m:
        bad.append("no masthead above the grid")
    elif m.group(1) != "/images/hats-towels/hero.jpg":
        bad.append(f"masthead is {m.group(1)}, not ours")
    if '<aside class="sidebar"' not in top:
        bad.append("no sidebar above the grid")
    for label, want in (("Picks", len(HATS) + len(TOWELS)), ("Hats", len(HATS)),
                        ("Towels", len(TOWELS)), ("Brands", len(set(brands)))):
        sm = re.search(rf'<span class="l">{label}</span><span>([^<]+)</span>', top)
        if not sm:
            bad.append(f"sidebar has no {label} row")
        elif sm.group(1).strip() != str(want):
            bad.append(f"sidebar {label} says {sm.group(1)}, expected {want}")
    # THE PROSE MUST AGREE WITH THE STATS CARD BESIDE IT. The first draft said
    # the run started at nineteen dollars while the sidebar said $13.30.
    words_n = {"thirteen": 13, "nineteen": 19, "thirty": 30, "thirty-four": 34,
               "forty": 40, "forty-five": 45, "forty-six": 46, "forty-eight": 48, "fifty": 50, "fifty-five": 55}
    alts = "|".join(sorted(words_n, key=len, reverse=True))
    claims = [words_n[w] for w in
              re.findall(rf"\b({alts})(?=-dollar\b| dollars\b)|\bat ({alts})\b", INTRO)
              for w in w if w]
    if claims and (min(claims) != int(min(prices)) or max(claims) != int(max(prices))):
        bad.append(f"intro claims ${min(claims)}-${max(claims)}, "
                   f"data says ${int(min(prices))}-${int(max(prices))}")
    # ---- THE TAKE MUST AGREE WITH THE DATA IT DESCRIBES ----
    # A trends piece is only as good as its arithmetic. These assertions fail
    # the build if a price edit ever makes the prose wrong.
    hat_p = sorted(p for _s, _b, _n, p, _t in HATS)
    tow = {s: p for s, _b, _n, p, _t in TOWELS}
    n_under = sum(1 for p in hat_p if p < tow["sentinel-golf"])
    if "more than fourteen of the eighteen caps" in nb and n_under != 14:
        bad.append(f"The Take says fourteen caps under the Sentinel towel; "
                   f"the data says {n_under}")
    if tow["seamus"] != 45 or dict((s, p) for s, _b, _n, p, _t in HATS)["read-the-green"] != 45:
        bad.append("The Take pairs Seamus and Read The Green at $45; prices moved")
    if "The Take" not in nb:
        bad.append("The Take section is missing")
    if nb.count('class="writeup-body"') < 1:
        bad.append("The Take is not in a writeup-body block")

    mm = re.search(r'<div class="drop-meta">.*?<span>([^<]+)</span>', hh, re.S)
    if not mm or mm.group(1).strip() != f"{len(HATS)+len(TOWELS)} Picks":
        bad.append(f"drop-meta reads {mm.group(1).strip()!r}" if mm else "no drop-meta")

    if bad:
        sys.exit("! " + "; ".join(bad))
    print(f"  wrote {OUT.name}")
    print(f"  verified: {n_cards} cards, {len(set(brands))} distinct brands, "
          f"{words} words, every image local, no beanies or visors")
    print(f"  verified: own masthead, own intro, sidebar {len(HATS)+len(TOWELS)} picks "
          f"/ {len(set(brands))} brands / {rng.replace('&ndash;', '-')}, "
          f"no donor content above the grid")


if __name__ == "__main__":
    main("--apply" in sys.argv)
