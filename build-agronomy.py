#!/usr/bin/env python3
"""
build-agronomy.py — Agronomy Workshop, Brand Revisited. 19 September 2026.

Lenny: "let's beef up the agronomy page — it's getting attention. Follow the
brand revisited template." It is getting attention because DEAS MAG quoted our
original post twice on 27 August.

THE ANGLE, AND WHY IT IS NOT DEAS'S ANGLE
-----------------------------------------
DEAS got there first and got there well. Their piece runs manifesto → material →
sample sale → close, built on the reading that "the long game" means duration
rather than distance. Writing our expansion around those same beats would
produce a structural copy of the piece currently sending us readers — not
word-for-word, but in shape, which is the harder kind to defend.

So this is the story DEAS did not tell: Rob Junge is a working creative director
— Wondersauce, Vimeo, Field Mag, Treaty, Lalo, Playback — and Agronomy Workshop
reads as an identity project executed at product level. DEAS never mentions he
has a design career at all. The spine is his Are.na channel, created 25 May 2021
and still being added to the day before we published: four and a half years of
collecting before twelve SKUs.

WHAT WE COULD NOT GET, STATED PLAINLY IN THE COPY
--------------------------------------------------
There is not one published word of Rob Junge speaking about this brand. No
interview, podcast, profile or quote, anywhere, in any year. Three research
passes. So this page carries NO founder quotes, and says so rather than
implying access we do not have. Everything in quotation marks here is either
the brand's own site copy or a named publication, and each is attributed.

DELIBERATELY NOT PRINTED, all flagged by research as unverifiable:
  · the Victoria Buchanan line DEAS attributes to LinkedIn — we could not find
    it anywhere, and reprinting an unverifiable quote because another outlet
    ran it is how errors launder.
  · the David McGillivray post — text appears only as a search-result title;
    x.com blocks unauthenticated reads, so nobody has actually read the post.
  · the "misery sport" Instagram bio — login-walled, unread.
  · any production quantity or factory name — the brand publishes neither.
  · the SUNY Purchase degree — rests solely on LinkedIn scrapes.

Prices and stock are read from the brand's Shopify backend, not the Framer
front end, because the front end displays compare_at_price on the sample sale —
i.e. it shows full retail where the sale price should be.

Idempotent. Dry run by default.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
CAT  = ROOT / "research/agronomy-catalogue.json"
SRC  = ROOT / "drops/brand-to-know-merrill-golf.html"      # furniture donor
OUT  = ROOT / "drops/agronomy-workshop-a-golf-shirt-with-a-hidden-tee-slot-and-no.html"
SLUG = "/drops/agronomy-workshop-a-golf-shirt-with-a-hidden-tee-slot-and-no"

TITLE = ("Agronomy Workshop &mdash; A Golf Shirt with a Hidden Tee Slot "
         "and Nothing to Prove")
DESC  = ("Agronomy Workshop makes twelve things in San Francisco: a 17.5 oz "
         "cotton work shirt hand-sewn in Los Angeles, five rope hats and a "
         "towel. Prices and stock read 19 September 2026.")
HERO  = "/images/agronomy/hero.jpg"
STORE = "https://agronomywork.shop"

# LINES OTHER PUBLICATIONS HAVE QUOTED FROM THIS PAGE. THEY MUST SURVIVE EVERY
# REBUILD.
#
# DEAS MAG cited The Grassy Issue twice in "The Raw Material of the Fairway"
# (27 August 2026), both times from this post, and /about now carries a Press
# block that says "Both lines are from our Agronomy Workshop piece."
#
# The first version of this builder replaced the whole body with fresh copy and
# deleted both lines. For a while the citation on our own About page pointed at
# a page that no longer contained what it claimed, and DEAS's link landed on a
# piece missing the words they had quoted. add-press.py has a guard for exactly
# this, but it only fires when the ABOUT page is rebuilt — nothing stopped the
# POST from dropping them. That guard is now duplicated here, at the end that
# can actually destroy them.
#
# If a future edit genuinely needs to drop one of these, it has to be a
# deliberate decision that also updates /about — not a silent casualty of a
# rewrite.
CITED_LINES = [
    "a catalog so small it fits on a scorecard",
    "greenkeeper who reads design blogs",
]

SECTIONS = [
    ("Tops", "The Work Shirt &mdash; 5",
     "One garment in two lengths and three colourways. 17.5 oz cotton, "
     "hand-dyed and hand-sewn in Los Angeles."),
    ("Headwear", "The Hats &mdash; 5",
     "Five-panel rope caps in recycled nylon. Each ships with a pencil."),
    ("Towels", "The Towel &mdash; 2",
     "Both colourways are sold out as of this morning."),
]

# Peers, not filler: two design-led labels that publish their specs (Casualist,
# Forden), plus the two edits Agronomy would sit inside. /drops/gorpcore was the
# first pick and is not in the catalogue — more_entries() refused to guess a
# name or an image for it, which is the behaviour we want.
MORE_SLUGS = [
    "/drops/the-bold-tee-edit",
    "/drops/brand-to-know-casualist",
    "/drops/brand-to-know-forden-golf",
    "/drops/best-golf-streetwear-brands-2026",
]


# THE FAQ IS WRITTEN ONCE AND USED THREE TIMES — visible markup, JSON-LD,
# and the guard that checks they agree. Google requires FAQ structured data
# to have matching content on the page; the first build shipped schema with
# no visible FAQ, which is a rich-result violation. One list, no drift.
FAQ = [
    ("What is Agronomy Workshop?",
     "Agronomy Workshop is a San Francisco golf apparel brand founded in "
     "2025 by the designer and creative director Rob Junge. It sells twelve "
     "pieces: a heavyweight cotton work shirt in two sleeve lengths, five "
     "rope caps and a golf towel."),
    ("Where is Agronomy Workshop made?",
     "The work shirt is hand-dyed and hand-sewn in Los Angeles. The brand "
     "describes it as 100% heavyweight cotton at 17.5 oz, made in the USA "
     "from imported yarns. Orders ship from San Francisco."),
    ("What is the hidden tee slot in the Agronomy Workshop shirt?",
     "The chest pocket carries a concealed holder the brand says holds up to "
     "three tees. The shirt also uses a mock neck in place of a collar, and "
     "the logo is tonal embroidery on the back rather than a chest print."),
    ("How much does Agronomy Workshop cost?",
     "Prices read on 19 September 2026: the long-sleeve work shirt is $172, "
     "the short-sleeve $136, rope caps $64 and the Unusual Lies towel $56. "
     "A sample sale offers flawed pieces at $99 and $38."),
]


def plain(s):
    return (s.replace("&mdash;", "—").replace("&middot;", "·")
             .replace("&amp;", "&").replace("&rsquo;", "’")
             .replace("&ldquo;", "“").replace("&rdquo;", "”")
             .replace("&copy;", "©").replace('"', "&quot;"))


def more_entries():
    """Image and title come from the site's own registry, never hand-written —
    the alternative put a T-shirt on a card linking to The Hat Edit."""
    cat = json.loads((ROOT / "research/more-catalogue.json").read_text(encoding="utf-8"))
    out = []
    for s in MORE_SLUGS:
        e = cat.get(s)
        if not e:
            sys.exit(f"! {s} missing from more-catalogue.json")
        if not (ROOT / e["img"].lstrip("/")).exists():
            sys.exit(f"! catalogue image missing for {s}: {e['img']}")
        out.append((s, e["img"], e["name"]))
    return out


def card(p):
    img = f"/images/agronomy/p-{p['handle']}.jpg"
    sizes = p.get("sizes") or []
    out = [s["size"] for s in sizes if not s.get("available")]
    live = [s["size"] for s in sizes if s.get("available")]
    if not live:
        note = "Sold out"
    elif out and out != ["Default Title (one size)"]:
        note = "Sold out in " + ", ".join(out)
    else:
        note = "All sizes"
    desc = p.get("description_verbatim", "").strip()
    return (
        f'    <div class="product-card">\n'
        f'      <div class="product-img"><img src="{img}" alt="{plain(p["title"])}" loading="lazy" /></div>\n'
        f'      <div class="product-body">\n'
        f'        <div class="product-brand">Agronomy Workshop</div>\n'
        f'        <div class="product-name">{p["title"]}</div>\n'
        f'        <div class="product-price">${p["price"]}</div>\n'
        f'        <div class="product-desc">&ldquo;{desc}&rdquo; <em>{note}.</em></div>\n'
        f'        <a href="{p["product_url"]}" target="_blank" rel="noopener" class="product-link">'
        f'View on Agronomy Workshop &#8599;</a>\n'
        f'      </div>\n    </div>\n')


def lookbook(files, caption):
    """A .btk-wild-grid band. The component and its CSS already exist in the
    Brand to Know furniture — three columns, 1:1 object-fit cover — so nothing
    new is invented here."""
    imgs = "".join(
        f'    <img src="/images/agronomy/{f}" alt="{plain(a)}" loading="lazy" />\n'
        for f, a in files)
    return ('<section class="products">\n'
            f'  <div class="btk-wild-grid">\n{imgs}  </div>\n'
            f'  <div class="btk-wild-credit">{caption}</div>\n'
            '</section>\n')


# Two lookbook bands. Band A is the three frames that used to be the hero —
# Lenny: "move those three into the body." Band B is the on-model and in-situ
# photography that was sitting unused in the catalogue.
LOOK_A = [
    ("life-0.jpg", "Two golfers sitting in the fescue above a bunkered links hole, one in the Work Shirt"),
    ("life-1.jpg", "Close-up of the Work Shirt chest pocket holding two tees and a clover flower"),
    ("life-7.jpg", "Two golfers at golden hour on a dune ridge, both in Agronomy Workshop"),
]
LOOK_B = [
    ("life-11.jpg", "The L/S Work Shirt in Earth worn against a brick wall"),
    ("life-12.jpg", "The Work Shirt worn walking a city alley with a golf bag"),
    ("life-16.jpg", "The S/S Work Shirt in Navy on a studio seamless"),
    ("life-20.jpg", "The Tree Hat in Navy worn in profile"),
    ("life-14.jpg", "The Tree Hat and Work Shirt worn against a cypress trunk"),
    ("life-22.jpg", "The Unusual Lies towel in Earth held up against the sea"),
]


def more_block():
    cards = "\n".join(
        f'    <a href="{h}" class="more-card">\n'
        f'      <div class="more-card-img"><img src="{i}" alt="{plain(n)}" loading="lazy" /></div>\n'
        f'      <div class="more-card-body"><div class="more-card-name">{n}</div>'
        f'<div class="more-card-tag">The Edit</div></div>\n    </a>'
        for h, i, n in more_entries())
    return ('<!-- More from the Feed -->\n<div class="more">\n  <div class="more-hdr">\n'
            '    <span class="more-label">More from TGI</span>\n'
            '    <a href="/" class="more-link">See All &rarr;</a>\n  </div>\n'
            f'  <div class="more-grid">\n{cards}\n  </div>\n</div>\n\n')


EXTRA_CSS = """
/* --- agronomy revisited --- */
/* .product-price is used by several roundups but its rule lives on THOSE pages,
   not in the Brand to Know furniture this page clones. verify-post caught the
   class being used with no rule behind it. Copied verbatim from the house rule
   so this page renders identically to the others. */
.product-price{font-family:var(--mono);font-size:11px;letter-spacing:.05em;margin-bottom:10px}
.q-list{margin:18px 0 0;padding:0;list-style:none;counter-reset:q;}
.q-item{padding:16px 0;border-top:1px solid rgba(0,0,0,.12);counter-increment:q;}
.q-item:last-child{border-bottom:1px solid rgba(0,0,0,.12);}
.q-ask{font-family:var(--serif);font-size:19px;line-height:1.35;}
.q-ask::before{content:counter(q);font-family:var(--mono);font-size:10px;
  vertical-align:super;opacity:.45;margin-right:8px;}
.q-ans{font-size:14px;line-height:1.65;opacity:.75;margin-top:6px;}
"""


def build():
    d = json.loads(CAT.read_text(encoding="utf-8"))
    src = SRC.read_text(encoding="utf-8")
    head = src[:src.find('<div class="breadcrumb">')]
    tail = src[src.find("<footer"):]

    old = re.search(r"<title>([^<]*)</title>", head).group(1)
    head = head.replace(old, plain(TITLE))
    head = re.sub(r'<meta name="description" content="[^"]*"',
                  f'<meta name="description" content="{DESC}"', head)
    for k in ("og:description", "twitter:description"):
        head = re.sub(rf'((?:property|name)="{k}" content=)"[^"]*"', rf'\1"{DESC}"', head)
    for k in ("og:title", "twitter:title"):
        head = re.sub(rf'((?:property|name)="{k}" content=)"[^"]*"',
                      rf'\1"{plain(TITLE)}"', head)
    head = head.replace("/drops/brand-to-know-merrill-golf", SLUG)
    head = re.sub(r'(content=")/images/[^"]*(")', rf'\1{HERO}\2', head)
    head = re.sub(r'(content=")https://thegrassyissue\.com/images/[^"]*(")',
                  rf'\1https://thegrassyissue.com{HERO}\2', head)
    head = re.sub(r'("image"\s*:\s*")[^"]*(")',
                  rf'\1https://thegrassyissue.com{HERO}\2', head)
    head = re.sub(r'("(?:headline|name)"\s*:\s*")[^"]*(")',
                  rf'\1{plain(TITLE)}\2', head, count=1)
    # The Article/WebPage JSON-LD carries its OWN "description" field, separate
    # from the <meta> tags rewritten above. Leaving it behind published a
    # paragraph about Merrill Golf inside this page's structured data.
    head = re.sub(r'("description"\s*:\s*)"[^"]*"', rf'\1"{DESC}"', head, count=1)


    # REPLACE THE DONOR'S FAQ STRUCTURED DATA WHOLESALE.
    # The Merrill page ships an FAQPage JSON-LD block whose every question is
    # about Merrill Golf. Swapping the visible copy while leaving that in place
    # would publish another brand's FAQs to Google under this URL — invisible on
    # the page, wrong in the search result. Rewritten from verified facts only.
    faq = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q,
                           "acceptedAnswer": {"@type": "Answer", "text": a}}
                          for q, a in FAQ]}
    head = re.sub(
        r'<script type="application/ld\+json">\s*\{\s*"@context"[^<]*?"@type":\s*"FAQPage".*?</script>',
        '<script type="application/ld+json">\n'
        + json.dumps(faq, indent=1) + "\n</script>",
        head, count=1, flags=re.S)

    head = head.replace("</style>", EXTRA_CSS + "</style>", 1)

    prods = d["products"]
    by_cat = {c: [p for p in prods if p.get("category") == c] for c, _, _ in SECTIONS}
    n_out = sum(1 for p in prods
                if not any(s.get("available") for s in (p.get("sizes") or [])))

    # The five questions, verbatim from the brand's homepage.
    Q = [
        ("Does a golf shirt need to be made of plastic?",
         "Natural materials have almost completely been replaced by plastics and "
         "polyester in golf. Cotton can be soft, durable and breathable yet "
         "synthetic materials have become the de facto choice."),
        ("Do you really need a traditional collar?",
         "So many things in golf are the way they are under the guise of "
         "&lsquo;tradition&rsquo;. The majority of golf courses still enforce a "
         "dress code but there&rsquo;s more than one way to check that box."),
        ("Can a shirt bring you joy?",
         "How can you design a shirt so that you&rsquo;ll be excited to pull it "
         "out of the closet. While you can&rsquo;t show off the neck label on the "
         "course, we wanted something to represent the hyper attention to detail. "
         "There&rsquo;s something nice about a few tees fitting perfectly in your "
         "front pocket."),
        ("Does everything need to be so obvious?",
         "How could anyone know what it&rsquo;s for, if it doesn&rsquo;t scream "
         "golf? Branding in golf today feels so over the top. Does it all need to "
         "be so on the nose? How about some subtlety?"),
        ("Shouldn&rsquo;t a life-long sport have life-long products?",
         "It feels like so much of the industry is fixated on the latest trend "
         "&amp; churning out fast fashion for profit with cheap &amp; disposable "
         "products. What would the opposite approach look like?"),
    ]
    qs = "\n".join(
        f'    <li class="q-item"><div class="q-ask">&ldquo;{a}&rdquo;</div>'
        f'<div class="q-ans">{b}</div></li>' for a, b in Q)

    faq_html = (
        '<section class="products">\n'
        f'  <h2 class="products-hdr" id="faq">{plain(TITLE)} &mdash; FAQ</h2>\n'
        '  <div class="faq">\n'
        + "".join(
            f'    <details open class="faq-q"><summary>{q}</summary>'
            f'<p>{a}</p></details>\n' for q, a in FAQ)
        + '  </div>\n</section>\n')

    LOOK_A_HTML = lookbook(LOOK_A,
        'On the course &middot; photographs courtesy of Agronomy Workshop')
    LOOK_B_HTML = lookbook(LOOK_B,
        'The rest of the range, in situ &middot; photographs courtesy of Agronomy Workshop')

    secs = []
    for cat, hdr, note in SECTIONS:
        rows = by_cat[cat]
        secs.append(f'<section class="products">\n'
                    f'  <h2 class="products-hdr">{hdr}</h2>\n'
                    f'  <div class="sec-note">{note}</div>\n'
                    f'  <div class="products-grid">\n\n'
                    + "\n".join(card(p) for p in rows) + "  </div>\n</section>\n")

    body = f'''<div class="breadcrumb">
  <a href="/#feed">Feed</a> / <a href="/brands">Brands</a> / Agronomy Workshop
</div>

<div class="drop-hero"><div class="drop-hero-img"><img src="{HERO}" alt="The Agronomy Workshop L/S Heavyweight Work Shirt in navy, hung on a garment rack in the middle of a golf course with three tees in the chest pocket" /></div>
  <div style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:8px;">The L/S Heavyweight Work Shirt &middot; photograph courtesy of Agronomy Workshop</div>
</div>

<div class="drop-tag grass">Brand Revisited</div>

<header class="drop-header">
  <h1>{TITLE}</h1>
  <div class="drop-meta">
    <span>12 Pieces</span><span class="dot"></span>
    <span>San Francisco</span><span class="dot"></span>
    <span>Prices read 19 September 2026</span>
  </div>
</header>

<div class="writeup">
  <div class="writeup-body">
    <p><strong>The moodboard is four and a half years older than the
    company.</strong> Rob Junge keeps a public Are.na channel called Agronomy
    Workshop. It was created on 25 May 2021, it holds 1,113 blocks, and the last
    thing was added to it on 18 September 2026 &mdash; the day before this was
    written. The brand itself launched in October 2025. So the collecting ran for
    four and a half years before there was anything to sell, and it did not stop
    when there was.</p>

    <p>That gap is the most interesting fact about this brand, and it explains
    the thing people notice first. Agronomy Workshop does not behave like a golf
    company that hired a designer. It behaves like a designer who happens to have
    made golf clothes &mdash; which is exactly what it is. Junge is a working
    creative director: Wondersauce through the mid-2010s, then product design at
    Vimeo, then independent practice in San Francisco with Field Mag, Treaty,
    Lalo and Soft Services on the list, then Head of Design at the sports
    streaming startup Playback.
    The whole operation reads like a greenkeeper who reads design blogs:
    practical first, considered second, and loud about neither.</p>

    <p>Read the catalogue that way and the decisions stop looking like restraint
    and start looking like art direction.
    Twelve SKUs &mdash; a catalog so small it fits on a scorecard.
    A shirt whose logo is
    embroidered tonal on the back, legible from about a foot away. A cap called
    the Golf Brand&copy; Hat, whose entire graphic is the words &ldquo;Golf
    Brand&rdquo; with a copyright symbol. A site set in Gerstner Programm, a
    Swiss-modernist typeface, in a category that runs on athletic sans-serifs.
    None of that is apparel thinking. All of it is identity thinking.</p>

    <p>What we cannot tell you is what he makes of any of it. There is no
    published interview with Rob Junge about this brand &mdash; not a profile,
    not a podcast, not a quote in anyone else&rsquo;s coverage. Everything below
    in quotation marks is the brand&rsquo;s own site copy or a named
    publication.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">The Brand</div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>2025</span></div>
      <div class="sidebar-detail"><span class="l">Based</span><span>San Francisco</span></div>
      <div class="sidebar-detail"><span class="l">Made</span><span>Los Angeles</span></div>
      <div class="sidebar-detail"><span class="l">Catalogue</span><span>{len(prods)} pieces</span></div>
      <div class="sidebar-detail"><span class="l">Sold out</span><span>{n_out} of {len(prods)}</span></div>
      <div class="sidebar-detail"><span class="l">Prices read</span><span>19 Sept 2026</span></div>
      <a href="{STORE}" target="_blank" rel="noopener" class="sidebar-cta">Shop Agronomy Workshop &#8599;</a>
      <a href="/brands" class="sidebar-cta" style="margin-top:8px;">The Brand Index &rarr;</a>
      <div class="hashtags">
        <span class="hashtag">#AgronomyWorkshop</span>
        <span class="hashtag">#BrandRevisited</span>
        <span class="hashtag">#GolfStyle</span>
        <span class="hashtag">#MadeInUSA</span>
      </div>
    </div>
  <div class="aff-disclosure" style="font-family:var(--mono);font-size:9px;letter-spacing:.08em;text-transform:uppercase;opacity:.5;margin-top:14px;line-height:1.6;">Some links may earn TGI a commission &mdash; <a href="/disclosure" style="border-bottom:1px solid currentColor;">details</a></div>
  </aside>
</div>

<div class="writeup">
  <div class="writeup-body">
    <p><strong>There is a through-line in the work, and it is soil.</strong>
    Treaty, where Junge was creative director, was a CBD line out of Hudson Hemp,
    built on a Hudson Valley farm and sold on the specifics of the ground it grew
    in. Damp, the wine project he co-founded, opens with the line
    &ldquo;Honest wine reflects the ground from which the grapes are grown.&rdquo;
    Then a golf brand named for the science of cultivating land. Three consecutive
    ventures about what happens in dirt, from a man who then went and made a shirt
    to last a decade.</p>

    <p>The timing is its own small story. Playback raised $22 million in March
    2025 and shut down that December, its team landing at Disney and ESPN the
    following March. Agronomy Workshop went live in October 2025 &mdash; in the
    gap, while the startup was closing.</p>
  </div>
</div>

{LOOK_A_HTML}
{secs[0]}
{secs[1]}
{secs[2]}
{LOOK_B_HTML}
<div class="writeup">
  <div class="writeup-body">
    <p><strong>What has changed since we first wrote this up.</strong> The
    catalogue is the same size, but it is thinner than it looks. Four of the five
    shirts are gone in XL &mdash; only the long-sleeve in Navy still runs the full
    size range. Both towels are sold out. For a brand whose towel is the cheapest
    thing it makes and is called Unusual Lies, that is the item that keeps
    selling out.</p>

    <p>There is also a sample sale now, which is the most revealing page on the
    site. Flawed units, each defect named in the product title &mdash; Thread
    Pull, Missing Front Rope, Minor Brim Scratch &mdash; under copy that reads:
    &ldquo;With every production run a number of pieces get set to the side for
    inconsistencies. They usually have a small issue that most people
    wouldn&rsquo;t notice. Every piece has its issue called out specifically. If
    that sounds like something you can live with, it&rsquo;s yours.&rdquo;
    Shirts come down to $99 from $172 and hats to $38 from $64. One thing to
    know before you click: the page itself displays the full retail figure
    where the sale price should be, so read the number in the cart rather than
    the one on the page.</p>

    <p>The distribution has not moved much. Soft Hands Club in the UK announced
    itself as the brand&rsquo;s retailer and built the page &mdash; &ldquo;Soft
    Hands Club is proud to be Agronomy Workshop&rsquo;s UK retailer&rdquo; &mdash;
    but the collection currently reads &ldquo;coming soon&rdquo; and holds no
    products. In the US it is direct, plus listings on Mav Farm and Over Under.
    GolfMagic named it one of ten up-and-coming brands for 2026 back in December,
    describing &ldquo;a fun towel and a cap&rdquo; and an
    &ldquo;integrated pen holder&rdquo; &mdash; the brand says pencil, and ships
    one in the box.</p>

    <p>Eleven months in, the shape of the thing is holding: one shirt, five hats,
    a towel, no collaborations, no seasons. The newsletter promises
    &ldquo;Serious Interviews with Creatives &amp; Unserious Guides on How to Run
    a Golf Brand&copy;&rdquo; and has not yet published an issue anyone can find.
    The Are.na channel, meanwhile, keeps growing.</p>
  </div>
</div>


<section class="products">
  <h2 class="products-hdr">The Five Questions</h2>
  <div class="sec-note">The closest thing the brand has to a manifesto sits on
    its homepage under the heading &ldquo;Questions we asked before designing a
    golf shirt.&rdquo; Reproduced in full, in the brand&rsquo;s words.</div>
  <ol class="q-list">
{qs}
  </ol>
</section>

<div class="writeup">
  <div class="writeup-body">
    <p><strong>The answers are checkable, which is the unusual part.</strong>
    Question one is about plastic, and the shirt is &ldquo;100% Heavyweight
    Cotton (17.5 oz). Made in the USA from imported yarns&rdquo; &mdash; note the
    second half of that sentence, which most brands would have left off. Question
    two is about collars, and the shirt has a mock neck instead. Question three
    is about joy, and there is a hidden tee holder inside the chest pocket that
    &ldquo;holds up to 3 tees.&rdquo; Question four is about subtlety, and the
    logo is tonal embroidery on the back.</p>

    <p>One line is scoped more narrowly than it first reads. The questions are
    about a golf <em>shirt</em>, and the shirts are cotton. The five caps are
    &ldquo;100% Recycled Nylon.&rdquo;</p>
  </div>
</div>

'''
    return head + body + faq_html + "\n" + more_block() + tail


def links_ok(page):
    bad = []
    for h in sorted(set(re.findall(r'href="(/drops/[^"#?]+)"', page))):
        s = h[len("/drops/"):].rstrip("/")
        if s == SLUG.split("/")[-1]:
            continue
        if not (ROOT / "drops" / f"{s}.html").exists():
            bad.append(h)
    return (not bad), ("broken: " + ", ".join(bad) if bad else "")


def main(apply_):
    page = build()
    d = json.loads(CAT.read_text(encoding="utf-8"))
    prods = d["products"]
    head = page[:page.find("<body")]
    flat = re.sub(r"\s+", " ", page)      # what the browser collapses it to
    words = len(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ",
                page[page.find("<body"):])).split())

    # Lines research flagged as unverifiable. None may appear.
    BANNED = ["misery sport", "Victoria Buchanan", "optimal conditions",
              "McGillivray", "incredible testament", "SUNY Purchase"]

    checks = [
        (f"{len(prods)} product cards",
         page.count('<div class="product-card"') == len(prods),
         str(page.count('<div class="product-card"'))),
        ("cards are div-shaped, not anchor-shaped",
         '<a class="product-card"' not in page, ""),
        # Five h2 sections: the Five Questions, three collection bands
        # (Tops / Headwear / Towels), and the FAQ.
        ("five h2 sections", page.count('<h2 class="products-hdr"') == 5,
         str(page.count('<h2 class="products-hdr"'))),
        ("all three collection bands render",
         all(h in page for _c, h, _n in SECTIONS), ""),
        ("all five questions are present", page.count('class="q-item"') == 5, ""),
        # Lenny: "move the questions towards the bottom". Assert the position,
        # not just the presence — a section can exist and still be in the wrong
        # place, which is how the homepage card once shipped at DOM slot 24.
        ("the Five Questions sit below the product sections",
         page.index("The Five Questions") > page.rindex('<h2 class="products-hdr">The Towel'), ""),
        ("the Five Questions sit above the FAQ",
         page.index("The Five Questions") < page.index('id="faq"'), ""),
        # THE CITATION GUARD. See CITED_LINES at the top of this file. The first
        # run of this builder dropped both DEAS-quoted lines, which left /about
        # crediting this page for words it no longer contained. Rebuilding is
        # allowed to change anything on this page EXCEPT these.
        # Checked against whitespace-NORMALISED markup, because that is what a
        # reader and a quoting journalist actually see: HTML collapses runs of
        # whitespace, so a phrase broken across two source lines still renders
        # as one sentence. The first version of this guard compared against raw
        # source and failed on my own restored copy purely because the line
        # wrapped — a false alarm that would have tempted a future editor to
        # loosen the check. Normalise, then compare.
        ("lines DEAS MAG quoted are still on the page",
         all(q in flat for q in CITED_LINES),
         str([q for q in CITED_LINES if q not in flat])),
        ("each cited line appears exactly once",
         all(flat.count(q) == 1 for q in CITED_LINES),
         str({q: flat.count(q) for q in CITED_LINES})),
        # And the other direction: /about must still be claiming them, or the
        # quotes are orphaned here and the Press block has gone stale.
        ("/about still credits this page for those lines",
         all(q in (ROOT / "about.html").read_text(encoding="utf-8")
             for q in CITED_LINES)
         and "agronomy-workshop-a-golf-shirt" in
             (ROOT / "about.html").read_text(encoding="utf-8"), ""),
        # Two lookbook bands, and the hero photograph is not reused in either.
        ("two lookbook bands render",
         page.count('class="btk-wild-grid"') == 2, ""),
        ("lookbook bands hold the right number of frames",
         page.count('class="btk-wild-grid"') == 2
         and len(re.findall(r'btk-wild-grid">(?:\s*<img[^>]*>)+', page)) == 2, ""),
        ("every lookbook frame is a distinct photograph",
         len({f for f, _ in LOOK_A + LOOK_B}) == len(LOOK_A + LOOK_B), ""),
        ("the hero photograph is not reused in a lookbook band",
         "life-9.jpg" not in [f for f, _ in LOOK_A + LOOK_B], ""),
        ("the three former hero frames are now in the body",
         all(f'/images/agronomy/{f}' in page for f, _ in LOOK_A), ""),
        # Google requires FAQ structured data to have matching visible
        # content. The first build shipped schema with no FAQ on the page —
        # a rich-result violation. Both now come from one list.
        ("every schema FAQ question is visible on the page",
         all(f"<summary>{q}</summary>" in page for q, _ in FAQ), ""),
        ("visible FAQ count matches the schema",
         page.count('class="faq-q"') == len(FAQ), ""),
        # The whole point of the page is that we have no founder quotes. If a
        # future edit adds one, it has to be sourced deliberately, not slip in.
        ("no quote is attributed to Rob Junge",
         not re.search(r'Junge[^.]{0,40}(?:said|says|told|explains)', page), ""),
        ("the absence of founder quotes is disclosed",
         "no published interview with Rob Junge"
         in re.sub(r"\s+", " ", page), ""),
        ("no unverifiable line was printed",
         not any(b in page for b in BANNED),
         str([b for b in BANNED if b in page])),
        ("the sample-sale price display bug is disclosed",
         "read the number in the cart" in page, ""),
        ("the nylon caps are disclosed",
         "100% Recycled Nylon" in page, ""),
        ("every local image exists",
         all((ROOT / s.lstrip("/")).exists()
             for s in re.findall(r'src="(/images/agronomy/[^"]+)"', page)), ""),
        ("no hot-linked images",
         not re.search(r'<img[^>]+src="https?://', page), ""),
        ("every img has alt", all('alt="' in i for i in re.findall(r"<img[^>]*>", page)), ""),
        ("banned word 'worth' absent from body copy",
         not re.search(r"\bworth\b", re.sub(r'<div class="more".*', "", page, flags=re.S), re.I), ""),
        ("every internal /drops/ link resolves", *links_ok(page)),
        ("four distinct More cards",
         len(set(re.findall(r'<a href="([^"]+)" class="more-card"', page))) == 4, ""),
        ("no More card uses this post's own imagery",
         not re.search(r'class="more-card-img"><img src="/images/agronomy/', page), ""),
        ("sidebar counts match the data",
         f'<span class="l">Catalogue</span><span>{len(prods)} pieces</span>' in page, ""),
        ("word count is a feature, not a stub", words >= 1200, str(words)),
        ("canonical points at this slug", SLUG in page, ""),
        ("no donor slug in the head", "merrill" not in head.lower(), ""),
        ("og/twitter image is this hero",
         all(HERO in m for m in re.findall(
             r'(?:og:image|twitter:image)" content="([^"]*)"', head)), ""),
        ("exactly one h1", len(re.findall(r"<h1", page)) == 1, ""),
        ("div balance", page.count("<div") == page.count("</div>"),
         f'{page.count("<div")}/{page.count("</div>")}'),
        ("section balance", page.count("<section") == page.count("</section>"), ""),
        # COUNT REAL TAGS. page.count("<li") also matches every <link> in the
        # head — six of them — so the naive substring count reported 11 opens
        # against 5 closes and failed a balanced document.
        ("ol/li balance",
         page.count("<ol") == page.count("</ol>")
         and len(re.findall(r"<li\b", page)) == page.count("</li>"), ""),
        ("anchor balance", len(re.findall(r"<a\b", page)) == page.count("</a>"), ""),
        ("document closes", page.rstrip().endswith("</html>"), ""),
    ]
    ok = True
    for l, p, dd in checks:
        print(f"  {'OK  ' if p else 'FAIL'} {l}{('  ' + dd) if dd and not p else ''}")
        ok &= p
    if not ok:
        sys.exit("\n! refusing to write")
    print(f"\n  {len(page):,} bytes / {words} words")
    if apply_:
        OUT.write_text(page, encoding="utf-8"); print(f"  wrote {OUT.name}")
    else:
        print("  dry run — pass --apply")


if __name__ == "__main__":
    main("--apply" in sys.argv)
