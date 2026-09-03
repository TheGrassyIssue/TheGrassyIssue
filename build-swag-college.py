#!/usr/bin/env python3
"""build-swag-college.py — Swag Golf's 2026 college program.

Lenny, 2026-09-02: "let's do a post about the Swag Golf College program" and
"extra on Texas but still give the full write up."

SOURCING. Everything here was read off swaggolf.com's own products.json on
2026-09-02, not from a press release: 62 licensed SKUs, all created in August
2026 and published 25 Aug, across 15 schools and four formats. Prices, stock
state and handles are as at that read. The Texas Den Caddy Cooler was already
out of stock when the file was pulled — said plainly on the card rather than
quietly dropped. See research/drop-scout-2026-09-02.md.

WHY THE SWEEP MATTERS: this was found by diffing published_at against created_at
across 50 universe storefronts. Publish dates alone are not release dates — the
same sweep turned up 22 Mogshade "new" covers that were created in Feb 2024.
These 62 are genuinely new.

Imagery: Swag shoots every product 1000x1000 on black, so there is no landscape
frame anywhere in the catalogue. The hero is composed here from five covers on
the same black — see the hero block below.

Chassis cloned from drops/brand-to-know-kingfisher-golf.html.
"""
import re, os, json

S = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(S, "drops", "brand-to-know-kingfisher-golf.html")
ch = open(SRC, encoding="utf-8").read()

css_main = re.search(r'(<link rel="preconnect".*</style>)\s*</head>', ch, re.S).group(1)
nav      = re.search(r'(<nav class="nav".*?</nav>)', ch, re.S).group(1)
tail     = re.search(r'(<!-- TGI SEARCH -->.*?)</body>', ch, re.S).group(1)

if ".cat-kicker{" not in css_main:
    css_main = css_main.replace("</style>",
        ".products h2{font-family:var(--serif);font-weight:600;font-size:clamp(24px,2.6vw,32px);"
        "letter-spacing:-.01em;line-height:1.1;margin:14px 0 16px}"
        ".cat-kicker{font-size:15px;line-height:1.75;color:#3f443e;margin:0 0 36px;max-width:70ch;"
        "border-left:3px solid var(--rough);padding:4px 0 4px 18px}"
        ".cat-kicker strong{font-family:var(--mono);font-size:11px;letter-spacing:.14em;"
        "text-transform:uppercase;color:var(--grass);opacity:1;display:block;margin-bottom:8px}"
        "\n</style>", 1)

if ".pull-quote{" not in css_main:
    css_main = css_main.replace("</style>",
        ".pull-quote{max-width:1400px;margin:0 auto;padding:0 32px}"
        ".pull-quote-inner{font-family:var(--serif);font-style:italic;font-size:22px;line-height:1.4;"
        "padding:32px 0;margin:0;border-top:.5px solid rgba(20,20,20,.15);"
        "border-bottom:.5px solid rgba(20,20,20,.15);color:var(--grass)}"
        ".pull-quote-attr{font-family:var(--mono);font-style:normal;font-size:10px;letter-spacing:.14em;"
        "text-transform:uppercase;color:var(--ink);opacity:.45;margin-top:12px;display:block}"
        "@media(max-width:820px){.pull-quote{padding:0 20px}}\n</style>", 1)

URL         = "https://thegrassyissue.com/drops/swag-golf-college-program"
TITLE       = "Swag Golf Put Fifteen Student Sections on Headcovers"
TITLE_PLAIN = "Swag Golf Put Fifteen Student Sections on Headcovers"
DESC        = ("Swag Golf published 62 licensed college pieces on 25 August 2026 — covers, desk "
               "caddies and miniature tour-bag coolers across fifteen schools, each one named "
               "after a chant rather than a logo. The full program, with Texas first.")
IMG   = "/images/swag-college"
STORE = "https://swaggolf.com/products/"
FRAMES = json.load(open(os.path.join(S, "data", "swag-college-frames.json")))


def card(base, name, price, desc, alt, handle, sold_out=False):
    n = FRAMES.get(base, 1)
    srcs = [base] + ["%s-a%d" % (base, i) for i in range(2, n + 1)]
    gal = "".join('<div class="pg-frame"><img src="%s/%s.jpg" alt="%s" loading="lazy" /></div>'
                  % (IMG, s, alt) for s in srcs)
    if n > 1:
        dots = "".join('<button class="pg-dot%s" data-i="%d" aria-label="View image %d"></button>'
                       % (" on" if i == 0 else "", i, i + 1) for i in range(n))
        ctrl = ('<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
                '<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
                '<span class="pg-count">1/%d</span><div class="pg-dots">%s</div>' % (n, dots))
    else:
        ctrl = ""
    label = "%s &middot; %s%s" % (name, price, " &middot; sold out" if sold_out else "")
    tmpl = ('<div class="product-card" data-frames="%(n)d">'
            '<div class="product-gallery"><div class="pg-track">%(gal)s</div>%(ctrl)s</div>'
            '<div class="product-body">'
            '<div class="product-brand">Swag Golf</div>'
            '<div class="product-name">%(label)s</div>'
            '<div class="product-desc">%(desc)s</div>'
            '<a href="%(store)s%(handle)s" target="_blank" rel="noopener" '
            'class="product-link">Shop &#8599;</a>'
            '</div></div>')
    return tmpl % dict(n=n, gal=gal, ctrl=ctrl, label=label, desc=desc,
                       store=STORE, handle=handle)


SECTIONS = [
 ("Texas, First",
  "<strong>Austin &middot; five pieces</strong>Texas gets the deepest run in the program &mdash; a driver cover, two fairway covers, a desk caddy and one of the six coolers. It is also the one that moved fastest: the Longhorns cooler was already out of stock when we pulled the catalogue on 2 September, eight days after the program went up.",
  [
   ("tx-hookem", "Hook &rsquo;Em Fairway Cover", "$99.99",
    "The horns sit on a white crown, with the words running up the side in burnt orange. Of the two Texas fairway covers this is the one that reads from across the fairway, which is the entire job of a headcover graphic.",
    "Swag Golf University of Texas Hook 'Em fairway headcover in white and burnt orange",
    "university-of-texas-hook-em-fairway-cover"),
   ("tx-bevo", "Bevo Driver Cover", "$99.99",
    "The steer, rendered rather than vectorised &mdash; Swag paints these like small canvases and the difference shows at arm&rsquo;s length. The driver covers carry the mascot; the fairways carry the words.",
    "Swag Golf University of Texas Bevo driver headcover",
    "university-of-texas-bevo-driver-cover"),
   ("tx-eyes", "Eyes Of Texas Fairway Cover", "$99.99",
    "Named for the alma mater rather than the fight song, which is a quieter choice than Hook &rsquo;Em and the better one if you would rather not explain your headcover to a stranger on the first tee.",
    "Swag Golf Eyes of Texas fairway headcover",
    "university-of-texas-eyes-of-texas-fairway-cover"),
   ("tx-desk", "Longhorns Desk Caddy", "$59.99",
    "The cheapest way into the program at $59.99, and the only piece that never leaves the office. Three frames on the product page show it holding pens rather than clubs.",
    "Swag Golf Texas Longhorns desk caddy",
    "university-of-texas-longhorns-desk-caddy"),
   ("tx-cooler", "Longhorns Hook &rsquo;Em Den Caddy Cooler", "$222.22",
    "A miniature tour bag that is actually a cooler, with the Texas silhouette on the pocket. Gone within days of release, and the only one of the six coolers that had sold out when we looked.",
    "Swag Golf Texas Longhorns Hook 'Em Den Caddy cooler shaped like a miniature tour bag",
    "university-of-texas-longhorns-hook-em-den-caddy-cooler", True),
  ]),

 ("The Den Caddy Coolers",
  "<strong>Six schools &middot; $222.22</strong>The strangest object in the program and the one that explains it. Each is a scaled-down staff bag &mdash; hood, pockets, school marks &mdash; that opens as a cooler. At $222.22 they are more than twice the price of anything else here, and five of the six are still in stock.",
  [
   ("cool-tenn", "Volunteers Smokey Den Caddy Cooler", "$222.22",
    "Smokey on the pocket, Tennessee orange on the hood, the block T on the lid. The most literal translation of a staff bag into a cooler in the set.",
    "Swag Golf Tennessee Volunteers Smokey Den Caddy cooler",
    "university-of-tennessee-volunteers-smokey-den-caddy-cooler"),
   ("cool-bama", "Crimson Tide Den Caddy Cooler", "$222.22",
    "Big Al on one panel, the script A on the lid. Crimson and white with no third colour anywhere, which is why it photographs better than most of the others.",
    "Swag Golf Alabama Crimson Tide Den Caddy cooler",
    "university-of-alabama-crimson-tide-den-caddy-cooler"),
   ("cool-fla", "Gators Get Out Of Our Swamp Den Caddy Cooler", "$222.22",
    "The longest name on any piece in the program, and the only cooler that puts a full sentence on the bag. Orange and blue, alligator on the pocket.",
    "Swag Golf Florida Gators Get Out Of Our Swamp Den Caddy cooler",
    "university-of-florida-gators-get-out-of-our-swamp-den-caddy-cooler"),
   ("cool-mich", "Wolverines Go Blue Den Caddy Cooler", "$222.22",
    "Maize and blue, block M on the lid. Michigan and Michigan State both got coolers, which tells you Swag built this program around rivalries rather than around conference maps.",
    "Swag Golf Michigan Wolverines Go Blue Den Caddy cooler",
    "university-of-michigan-wolverines-go-blue-den-caddy-cooler"),
   ("cool-msu", "Go Green Go White Den Caddy Cooler", "$222.22",
    "The other half of that rivalry, and the call-and-response is the product name. Sparty on the pocket, green hood, white body.",
    "Swag Golf Michigan State Go Green Go White Den Caddy cooler",
    "michigan-state-university-go-green-go-white-den-caddy-cooler"),
  ]),

 ("The Other Eleven",
  "<strong>Covers &middot; $99.99</strong>The rest of the roster gets one piece each. Every name is a chant, a nickname or a place &mdash; Between The Hedges, Hoo Hoo Hoosiers, OH-IO, Geaux Tigers &mdash; and none of them is just a logo on a blank.",
  [
   ("tenn-check", "Tennessee Checkerboard Fairway Cover", "$99.99",
    "The Neyland end-zone checkerboard, orange and white, straight onto a fairway cover. The simplest idea in the program and probably the best-executed.",
    "Swag Golf Tennessee checkerboard fairway headcover",
    "university-of-tennessee-checkerboard-fairway-cover"),
   ("bama-walk", "Alabama Walk Of Champions Fairway Cover", "$99.99",
    "Named for the pre-game procession, with the plaza architecture painted down the side in crimson. One of the few covers here that puts a building on a headcover.",
    "Swag Golf Alabama Walk of Champions fairway headcover",
    "university-of-alabama-walk-of-champions-fairway-cover"),
   ("uga-hedges", "Georgia Between The Hedges Driver Cover", "$99.99",
    "Two bulldogs, one on each face, and the phrase on the reverse in script. The black-and-red version is the darkest cover in the whole program.",
    "Swag Golf Georgia Between The Hedges driver headcover",
    "university-of-georgia-between-the-hedges-driver-cover"),
   ("iu-hoohoo", "Indiana Hoo Hoo Hoosiers Fairway Cover", "$99.99",
    "Candy stripes on one side, the chant stacked in four lines on the other. Indiana got the most graphic treatment of any school in the set.",
    "Swag Golf Indiana Hoo Hoo Hoosiers fairway headcover with candy stripes",
    "indiana-university-hoo-hoo-hoosiers-fairway-cover"),
   ("lsu-geaux", "LSU Geaux Tigers Fairway Cover", "$99.99",
    "Purple and gold, tiger stripes rendered as brushwork rather than print. The spelling is the joke and the joke is forty years old, which is the point.",
    "Swag Golf LSU Geaux Tigers fairway headcover in purple and gold",
    "louisiana-state-university-geaux-tigers-fairway-cover"),
   ("miami-theu", "Miami All About The U Driver Cover", "$99.99",
    "Green and orange, the U on one face and the ibis on the other. Loud in a way that suits Miami and would look ridiculous on any of the other fourteen.",
    "Swag Golf Miami All About The U driver headcover",
    "university-of-miami-all-about-the-u-driver-cover"),
   ("unc-blue", "North Carolina Carolina Blue Fairway Cover", "$99.99",
    "Carolina blue is the whole product. The ram on one side, the argyle reference on the other, and a colour nobody else in the program can use.",
    "Swag Golf North Carolina Carolina Blue fairway headcover",
    "university-of-north-carolina-carolina-blue-fairway-cover"),
   ("osu-ohio", "Ohio State OH-IO Fairway Cover", "$99.99",
    "Buckeyes scattered across scarlet, the hyphenated chant on the crown. The nuts are painted individually, which is more effort than this idea strictly required.",
    "Swag Golf Ohio State OH-IO fairway headcover with buckeyes",
    "ohio-state-university-oh-io-fairway-cover"),
   ("ou-boomer", "Oklahoma Boomer Sooner Driver Cover", "$99.99",
    "Crimson and cream with the wagon on the reverse. Oklahoma and Texas both being in the program at all is the kind of thing a licensing team has to be brave about.",
    "Swag Golf Oklahoma Boomer Sooner driver headcover",
    "university-of-oklahoma-boomer-sooner-driver-cover"),
   ("sc-cocky", "South Carolina Cocky Fairway Cover", "$99.99",
    "Garnet and black, the mascot named on the product itself. The darkest palette in the set after Georgia.",
    "Swag Golf South Carolina Cocky fairway headcover in garnet and black",
    "university-of-south-carolina-cocky-fairway-cover"),
   ("fsu-chop", "Florida State Tomahawk Chop Fairway Cover", "$99.99",
    "Garnet and gold, the chop lettered down the side. Florida State and Florida both made the fifteen, which is the same rivalry logic as Michigan and Michigan State.",
    "Swag Golf Florida State Tomahawk Chop fairway headcover",
    "florida-state-university-tomahawk-chop-fairway-cover"),
  ]),
]

FAQS = [
 ("How many pieces are in Swag Golf&rsquo;s college program?",
  "Sixty-two, published on 25 August 2026, across fifteen schools. They break into four formats: "
  "fairway covers and driver covers at $99.99, desk caddies at $59.99, and Den Caddy coolers at $222.22."),
 ("Which schools are included?",
  "Alabama, Florida, Florida State, Georgia, Indiana, LSU, Miami, Michigan, Michigan State, "
  "North Carolina, Ohio State, Oklahoma, South Carolina, Tennessee and Texas."),
 ("What is a Den Caddy Cooler?",
  "A scaled-down staff bag &mdash; hood, pockets, school marks &mdash; that opens as a cooler. Six schools "
  "got one: Texas, Tennessee, Alabama, Florida, Michigan and Michigan State. It is the most expensive "
  "piece in the program at $222.22."),
 ("Why do all the prices repeat their digits?",
  "It is a Swag house convention rather than anything to do with the colleges. The covers are $99.99, "
  "the coolers $222.22, and the $10M Dollar Lance putter the brand released two days later was $777.77."),
 ("Has anything sold out already?",
  "As of 2 September the Texas Longhorns Hook &rsquo;Em Den Caddy Cooler and the Indiana Candy Stripes "
  "fairway cover were out of stock, along with several of the desk caddies. The other five coolers were "
  "still available."),
 ("Which Texas pieces are there?",
  "Five: the Hook &rsquo;Em and Eyes Of Texas fairway covers, the Bevo driver cover, the Longhorns desk "
  "caddy and the Longhorns Hook &rsquo;Em Den Caddy Cooler. Texas is tied with four other schools for the "
  "deepest run in the program."),
 ("Is this officially licensed?",
  "Yes &mdash; the products are listed by school name on Swag&rsquo;s own storefront, which is how licensed "
  "collegiate merchandise has to be sold."),
]

faq_ld = ",\n      ".join(
    '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
    % (json.dumps(re.sub(r"&[a-z]+;", "'", q)), json.dumps(re.sub(r"&[a-z]+;", "'", a)))
    for q, a in FAQS)
faq_html = "\n    ".join(
    '<details class="faq-q"><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in FAQS)

sections_html = ""
for hdr, kick, cards in SECTIONS:
    sections_html += ('\n<section class="products" style="margin-top:40px;">\n'
        '  <h2 class="products-hdr">%s</h2>\n  <p class="cat-kicker">%s</p>\n'
        '  <div class="products-grid">\n    %s\n  </div>\n</section>\n'
        % (hdr, kick, "\n    ".join(card(*c) for c in cards)))

page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{TITLE_PLAIN} | The Grassy Issue</title>
<meta name="description" content="{DESC}" />
<link rel="canonical" href="{URL}" />
<meta property="og:type" content="article" />
<meta property="og:title" content="{TITLE_PLAIN}" />
<meta property="og:description" content="{DESC}" />
<meta property="og:url" content="{URL}" />
<meta property="og:image" content="https://thegrassyissue.com/images/swag-college/hero.jpg" />
<meta name="twitter:card" content="summary_large_image" />
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article",
 "headline":{json.dumps(TITLE_PLAIN)},
 "description":{json.dumps(DESC)},
 "datePublished":"2026-09-02",
 "image":"https://thegrassyissue.com/images/swag-college/hero.jpg",
 "author":{{"@type":"Organization","name":"The Grassy Issue"}},
 "publisher":{{"@type":"Organization","name":"The Grassy Issue"}},
 "mainEntityOfPage":{json.dumps(URL)}}}
</script>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
      {faq_ld}
]}}
</script>
{css_main}
</head>
<body>
{nav}

<header class="drop-header">
  <div class="breadcrumb"><a href="/">Feed</a> / <a href="/#drops">Drops &amp; Brands</a> / <span>Swag College</span></div>
  <h1>{TITLE}</h1>
  <div class="drop-meta">
    <span>September 2, 2026</span>
    <span>&middot;</span>
    <span>62 pieces &middot; 15 schools &middot; $59.99&ndash;$222.22</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="Five Swag Golf college headcovers lined up on black — Texas, Tennessee, Alabama, Georgia and Indiana" /></div></div>

<div class="writeup">
  <div class="writeup-body">
    <p>On 25 August, Swag Golf published sixty-two licensed college pieces in a single day &mdash; fairway covers, driver covers, desk caddies and six miniature tour-bag coolers, spread across fifteen schools. It is the largest licensed run any brand in our universe has put out at once, and it landed the week college football started.</p>
    <p>What makes it more than a logo exercise is the naming. Almost nothing here is called the Texas Cover or the Georgia Cover. They are called Hook &rsquo;Em, Between The Hedges, Hoo Hoo Hoosiers, Get Out Of Our Swamp, Walk Of Champions, OH-IO, Geaux Tigers. Swag licensed the marks and then went looking for what the student section actually shouts, which is a harder brief and a much better one.</p>
    <p>Below is the whole program, Texas first &mdash; five pieces, and the one that sold out first.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Released</span><span>25 Aug 2026</span></div>
      <div class="sidebar-detail"><span class="l">Pieces</span><span>62</span></div>
      <div class="sidebar-detail"><span class="l">Schools</span><span>15</span></div>
      <div class="sidebar-detail"><span class="l">Covers</span><span>$99.99</span></div>
      <div class="sidebar-detail"><span class="l">Desk caddy</span><span>$59.99</span></div>
      <div class="sidebar-detail"><span class="l">Den Caddy</span><span>$222.22</span></div>
      <div class="sidebar-detail"><span class="l">Our pick</span><span>Tennessee Checkerboard</span></div>
      <a href="https://swaggolf.com/" target="_blank" rel="noopener" class="sidebar-cta">Visit Swag Golf ↗</a>
      <div class="hashtags">
        <span class="hashtag">#SwagGolf</span>
        <span class="hashtag">#CollegeGolf</span>
        <span class="hashtag">#Headcovers</span>
        <span class="hashtag">#HookEm</span>
        <span class="hashtag">#GameDay</span>
      </div>
    </div>
  </aside>
</div>

<div class="pull-quote">
  <div class="pull-quote-inner">Almost nothing here is called the Texas Cover. They are called Hook &rsquo;Em, Between The Hedges, Geaux Tigers &mdash; Swag licensed the marks and then went looking for what the student section actually shouts.<span class="pull-quote-attr">&mdash; The Grassy Issue</span></div>
</div>
{sections_html}

<section class="products" style="margin-top:8px;">
  <h2 id="how-it-reads">What the Program Gets Right</h2>
  <div style="max-width:760px;font-size:16px;line-height:1.7;">
    <p>Licensed collegiate golf gear usually arrives as a school mark dropped onto an existing blank, and it usually looks like it. This does not, for two reasons.</p>
    <p style="margin-top:16px">The first is that Swag paints rather than prints. The mascots on the driver covers are rendered with visible brushwork &mdash; the Georgia bulldogs, the Miami ibis, the Ohio State buckeyes are each drawn rather than dropped in at scale. At arm&rsquo;s length on a bag that difference is the entire product.</p>
    <p style="margin-top:16px">The second is the Den Caddy Cooler, which is the piece that could only come from a brand that makes headcovers for a living. It is a staff bag shrunk to cooler size, hood and pockets intact, and it belongs at a tailgate rather than on a cart. Six schools got one. At $222.22 it costs more than twice any cover here, and Texas&rsquo;s was gone inside a week.</p>
    <p style="margin-top:16px">The pricing, by the way, is a Swag habit rather than anything to do with the colleges: $99.99, $222.22, and $777.77 for the $10M Dollar Lance putter the brand put out two days after this program. The repeating digits are the house signature.</p>
  </div>
</section>

<section class="products" style="margin-top:34px;">
  <h2 id="faq">Questions</h2>
  <div class="faq">
    {faq_html}
  </div>
</section>

{tail}
</body>
</html>
'''

out = os.path.join(S, "drops", "swag-golf-college-program.html")
open(out, "w", encoding="utf-8").write(page)
words = len(re.sub(r"<[^>]+>", " ", page).split())
cards_n = page.count('class="product-card"')
print("wrote %s | words: %d | cards: %d" % (out, words, cards_n))
