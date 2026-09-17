#!/usr/bin/env python3
"""The late-season putter switch — twenty putters, eighteen buyable, two on presale.

WHY THIS POST AND WHY NOW
Lenny, 9/16/26: "another putter round up — late season chance to change up your
game", then "include the presale options at the bottom and include all the
suggested putters". So: all eighteen he approved, plus Mizuno and Scotty in their
own section at the foot of the page.

The timing argument is not invented. It is sitting in the prices. Four of the
eighteen are marked down TODAY — MacGregor by $30, Cobra by $50.99, the Odyssey
Ai-ONE by $50 and the Ai-DUAL by $100 — and the reason is the two putters in the
presale section: Mizuno's Z necks land 10/30 and Scotty's 9.5R lands 9/30. The
outgoing model year gets cheap in the four weeks before the new one arrives.
That is the post.

THIS DOES NOT REPLACE ANYTHING. Two putter pages are already live:
  /drops/5-zero-torque-putters-worth-your-attention  (the zero-torque ranking)
  /drops/the-2026-putter-drop-8-worth-the-cash
Depth over consolidation — house rule. This links to both and 301s neither.

BRAND REPEATS: Sub 70, Odyssey, Bettinardi and Makefield each appear twice. That
breaks the usual one-brand-one-slot rule for a roundup. Flagged to Lenny on 9/16
before building; he said build it. The guard below therefore ASSERTS the four
pairs rather than forbidding them, so that if the list is ever trimmed the
assertion fails loudly instead of the rule silently drifting.

EVERY PRICE was read off the brand's own live page on 9/16/26. Four figures from
the earlier research pass were wrong and are corrected; the STALE guard at the
bottom refuses to build if any of them reappear anywhere in the copy.

PING publishes no price on ping.com. The card says so and attributes the figure.

SECTIONS are organised by what the putter is trying to FIX, not by price and not
by brand, because a reader arriving at a putter roundup in September already
knows what is going wrong — they want the shelf that addresses it.

FAQ MARKUP: <details class="faq-q"><summary> inside <div class="faq">.
verify-post.py looks for the literal string '<div class="faq"' for the FAQPage
schema check — a <section> wrapper fails it.
BANNED WORD: 'worth' (the two existing putter slugs contain it; the guard strips
URLs before checking). DATE FORMAT: numeric M/D/YY.
"""
import re, os, json
import putter_cards

SLUG = "late-season-putter-switch"
IMG = "/images/putter-switch/"
TODAY = "9/17/26"    # publish date
PRICED = "9/16/26"   # the day every price was read off the brand's own page
TITLE = "Twenty Putters for the Late-Season Switch, From $170 to $799"
PLAIN = "Twenty Putters for the Late-Season Switch, From $170 to $799"
DESC = ("Eighteen putters you can buy today and two on presale, every price read off the "
        "brand's own page — zero torque, armlock, broomstick, milled blades and the four "
        "models discounted right now because the new model year lands in October.")

st = lambda s: re.sub(r"\s+", " ", re.sub(r"&[a-z]+;|&#\d+;", " ", s)).strip()

# ----------------------------------------------------------------- the lineup
# Lenny cut the price table on 9/17/26 - 'I don't like the table section'. This
# list is NO LONGER RENDERED. It stays because it is the manifest every guard
# below checks the page against: that the eighteen match the cards, that the four
# markdowns are still visible in the card copy now the table is not carrying them,
# and that the brand repeats Lenny approved are still exactly four pairs.
# key, brand, model, price string, head, fixes, sale-from (None = full price)
TABLE = [
 ("macgregor",      "MacGregor",   "MT Milled 002 Wing Back", "$169.99", "Mallet",      "Face balanced, high MOI",   "$199.99"),
 ("cobra",          "Cobra",       "Widesport Vintage",       "$199",    "Wide blade",  "Straight back, straight through", "$249.99"),
 ("sub70-001z",     "Sub 70",      "Sycamore 001Z",           "$199",    "Blade",       "Zero torque",               None),
 ("sub70-taiii",    "Sub 70",      "TAIII 254 Wide Blade",    "$199",    "Wide blade",  "Adjustable arc weighting",  None),
 ("vice",           "Vice Golf",   "VGP03",                   "from $224","Blade",      "Build it your way",         None),
 ("odyssey-aione",  "Odyssey",     "Ai-ONE #1 CH",            "$249.99", "Blade",       "Off-centre ball speed",     "$299.99"),
 ("odyssey-aidual", "Odyssey",     "Ai-DUAL Broomstick",      "$349.99", "Mallet, 48\"","Anchored, toe-up",          "$449.99"),
 ("edel",           "Edel Golf",   "Array B-1",               "$350",    "Wide blade",  "Aim bias",                  None),
 ("roark",          "Roark",       "Lightning 1.0",           "$399",    "Blade",       "Build it your way",         None),
 ("ping",           "Ping",        "Scottsdale TEC Ally Blue H CB", "$399.99", "Mallet", "Alignment, slight arc",    None),
 ("evnroll",        "Evnroll",     "V Series V5.1 MidLock",   "$429",    "Mallet",      "Quiet hands, mid length",   None),
 ("bettinardi-an2", "Bettinardi",  "Antidote SB2 Long",       "$480",    "Mallet, long","Zero torque, split grip",   None),
 ("bettinardi-bb28","Bettinardi",  "BB28 Armlock",            "$495",    "Blade",       "Armlock",                   None),
 ("lab",            "L.A.B. Golf", "VZN.1i Stock",            "$499",    "Mallet",      "Aim bias, zero torque",     None),
 ("piretti",        "Piretti",     "No-Torque Savona 2.5",    "$549",    "Mallet",      "Zero torque, high MOI",     None),
 ("makefield-al",   "Makefield",   "Arm Lock [A] Series",     "$599",    "Blade",       "Armlock, fully specced",    None),
 ("makefield-long", "Makefield",   "Long Putter [A] Series",  "$599",    "Mallet, long","Anchored, fully specced",   None),
 ("machine",        "Machine",     "M12 ZTX Mallet Converter","$799",    "Mallet",      "Zero torque, adjustable",   None),
]


# ------------------------------------------------------------------- the copy
INTRO = """<div class="writeup">
  <p>September is the sensible month to change putters, and almost nobody does it. The
  logic runs backwards in most bags: a golfer three-putts through a summer, resolves to
  do something about it, and then buys a putter in March &mdash; at full price, in the
  week before the first round of the year, with no time to learn it.</p>

  <p>Do it now and you get the two things that matter. You get rounds left to test it in
  conditions you already understand, and an off-season to groove whatever it changes about
  your stroke. You also get the prices, which are not a coincidence.
  <strong>Four of the eighteen putters below are marked down today</strong> &mdash; MacGregor
  by $30, Cobra by $50.99, the Odyssey Ai-ONE by $50 and the Ai-DUAL Broomstick by $100 &mdash;
  and the reason is sitting at the bottom of this page. Mizuno&rsquo;s new zero-torque necks
  reach shops on 10/30 and Scotty&rsquo;s Phantom 9.5R on 9/30. The model year turns over in
  the next six weeks, and the shelf clears first.</p>

  <p>Every price here was read off the brand&rsquo;s own live product page on {PRICED}, not a
  retailer listing. Where a brand publishes no price at all &mdash; Ping does not &mdash; the
  card says so and tells you where the figure came from. The sections are organised by
  what each putter is trying to fix rather than by price or by brand, on the assumption
  that if you are reading a putter roundup in September you already know what is going
  wrong out there.</p>
</div>

""".replace("{PRICED}", PRICED)

SQUARE = """<section class="products">
  <h2 class="products-hdr">When the face will not stay square</h2>
  <p class="cat-kicker">Four putters take four routes to the same idea &mdash; zero torque, toe-up,
  lie-angle balanced. The shaft axis is moved far enough from the head&rsquo;s centre of mass that the putter
  stops wanting to rotate open and shut, so holding it square becomes the default rather than a
  thing you do. It is the fastest-moving category in putters and, as of this year, the widest in
  price: <strong>$199 to $799</strong>.</p>
  """ + putter_cards.grid(["sub70-001z", "lab", "piretti", "machine"]) + """
</section>

"""

QUIET = """<section class="products">
  <h2 class="products-hdr">When the hands will not stay quiet</h2>
  <p class="cat-kicker">Armlock, mid-lock and broomstick, in ascending order of how much of your
  stroke you are prepared to hand over. All three work the same way underneath &mdash; brace the
  club against something that is not a wrist, and let the shoulders run the motion. Anchoring the
  club to the body has been against the Rules since 2016; bracing a longer grip against the lead
  forearm is not anchoring, which is why the armlock category exists at all.</p>
  """ + putter_cards.grid(["odyssey-aidual", "evnroll", "bettinardi-an2", "bettinardi-bb28",
                           "makefield-al", "makefield-long"]) + """
</section>

"""

AIM = """<section class="products">
  <h2 class="products-hdr">When you cannot aim it</h2>
  <p class="cat-kicker">This is the least glamorous failure and the most common one. Three putters built
  around the premise that the face is not pointing where you think it is &mdash; Ping with a dot and
  a long line, Edel with interchangeable alignment options chosen to cancel a measured aim bias,
  Odyssey with an insert that assumes you will miss the middle and tries to make it cost less.</p>
  """ + putter_cards.grid(["odyssey-aione", "edel", "ping"]) + """
</section>

"""

OBJECT = """<section class="products">
  <h2 class="products-hdr">When nothing is wrong and you just want a better object</h2>
  <p class="cat-kicker">Milled, specced, finished. Two of these are the cheapest putters in the
  guide and two are configurators that start where the shelf ends. None of them are trying to fix
  your stroke, which is its own kind of honesty.</p>
  """ + putter_cards.grid(["macgregor", "cobra", "sub70-taiii", "vice", "roark"]) + """
</section>

"""

# ------------------------------------------------ the bit that stops a bad purchase
CHOOSE = """<section class="writeup">
  <h2>Before you spend anything</h2>

  <p><strong>Know your arc before you shop, not after.</strong> A face-balanced or zero-torque putter
  fights a strong natural arc, and a heavy toe-hang blade fights a stroke that goes straight back
  and straight through. Nothing on this page fixes a mismatch between the two. Twenty minutes on a
  putting green with the putter you already own, watching whether the face opens on the backstroke,
  is free and will rule out half this list.</p>

  <p><strong>Length is a spec, not a size.</strong> Five of these &mdash; both Makefields, both
  Bettinardis and the Odyssey broomstick &mdash; only make sense at lengths a shop will not have on
  the rack. Makefield builds from 36 to 52 inches in half-inch steps; the Odyssey broomstick is
  fixed at 48. Ordering the wrong one is the most expensive mistake available here.</p>

  <p><strong>Adjustability is a real feature and it is not free.</strong> Machine, Edel, Roark,
  Makefield and Vice all sell a platform rather than a putter, and the cheapest configuration is
  rarely the one you will end up with. Read the options list before you read the price.</p>

  <p><strong>Four of these are discounted because something newer is coming.</strong> That is a
  reason to buy, not a reason to hesitate &mdash; a putter does not get slower. But if you want the
  thing the discount is clearing space for, it is in the next section and you can pre-order it
  today.</p>

  <p>If zero torque is specifically what you are here for, we ranked that category on its own in
  <a href="/drops/5-zero-torque-putters-worth-your-attention">the Zero Torque Putter Edit</a>, and
  the model-year releases are gathered in
  <a href="/drops/the-2026-putter-drop-8-worth-the-cash">the 2026 Putter Drop</a>.</p>
</section>

"""

PRESALE = """<section class="products">
  <h2 class="products-hdr">On presale</h2>
  <p class="cat-kicker">Neither of these is in a shop yet. Both are the reason four putters above
  are cheap this month. Scotty&rsquo;s Phantom 9.5R reaches US golf shops on <strong>9/30</strong> and
  Mizuno&rsquo;s M.Craft X Z necks on <strong>10/30</strong>; both take pre-orders now.</p>
  """ + putter_cards.grid(["mizuno", "scotty"], cta="Pre-order &#8599;") + """
</section>

"""

# ------------------------------------------------------------------------- FAQ
FAQ_ITEMS = [
 ("Is it a bad idea to change putters in the middle of a season?",
  "It is a better idea than changing in March. Switching in September leaves rounds to test the "
  "putter in conditions you already know and a winter to groove whatever it changes about your "
  "stroke, and it catches the four to six weeks when the outgoing model year is discounted. The "
  "case against &mdash; that a new putter costs you strokes while you learn it &mdash; is real, "
  "and it is exactly why doing it before the off-season beats doing it before the first round."),
 ("What does zero torque actually mean on a putter?",
  "The shaft axis is positioned far enough from the head's centre of mass that gravity stops "
  "twisting the face open and shut through the stroke. Brands reach it differently &mdash; Piretti "
  "and Odyssey use a toe-up centre-shafted design, L.A.B. uses lie angle balance, Bettinardi calls "
  "its version Simply Balanced &mdash; but the effect is the same: the putter rests with the toe "
  "up rather than hanging, and holding the face square becomes the default. It suits a stroke that "
  "goes straight back and straight through far better than a strongly arcing one."),
 ("Is an armlock putter legal?",
  "Yes. Anchoring the club or a gripping hand against the body has been against the Rules of Golf "
  "since 2016, but resting a longer grip along the lead forearm is not anchoring, and armlock "
  "putters are played on tour. A true broomstick is also legal provided you do not anchor the top "
  "of the grip against your chest or chin &mdash; which is the part that changed in 2016 and the "
  "part to understand before you buy one."),
 ("Which putters on this list are discounted right now?",
  "Four, as of 9/16/26, the day the prices were read: the MacGregor MT Milled 002 at $169.99 from $199.99, the Cobra Widesport "
  "Vintage at $199 from $249.99, the Odyssey Ai-ONE #1 CH at $249.99 from $299.99, and the Odyssey "
  "Ai-DUAL Broomstick at $349.99 from $449.99. That last one is a $100 reduction and the largest "
  "on the page."),
 ("Why does Ping not list a price for the Scottsdale TEC?",
  "Ping publishes specifications but not prices on ping.com, for any club. The $399.99 figure on "
  "the Scottsdale TEC Ally Blue H card is the launch price GOLF.com reported for every model in "
  "the line, and the card says so rather than presenting it as a figure we read off Ping."),
 ("What is the difference between the Scotty Phantom 9.5R and the 9R?",
  "The same head shape with a different neck. The 9.5R runs an elongated jet neck where the 9R "
  "uses a shorter configuration, and that extra offset from the shaft axis gives the 9.5R "
  "noticeably more toe flow &mdash; so it suits an arcing stroke where the 9R sits closer to "
  "face balanced. The 9.5R also carries a single long sightline down the length of the head."),
]

FAQ = ('<h2 class="products-hdr">Questions</h2>\n<div class="faq">\n'
       + "\n".join(f'  <details class="faq-q"><summary>{q}</summary>\n  <p>{a}</p></details>'
                   for q, a in FAQ_ITEMS)
       + "\n</div>\n")

SCHEMA = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": st(q),
                          "acceptedAnswer": {"@type": "Answer", "text": st(a)}}
                         for q, a in FAQ_ITEMS]}

# --------------------------------------------------------------- assemble page
model = open("drops/brand-to-know-gamut-golf.html", encoding="utf-8").read()
head = model[:model.find('<div class="breadcrumb">')]
tail = model[model.find('<section class="more"'):]

head = re.sub(r'<title>[^<]*</title>', f'<title>{PLAIN} &mdash; The Grassy Issue</title>', head)
for k, v in [("description", DESC), ("og:title", PLAIN), ("og:description", DESC)]:
    head = re.sub(rf'(<meta (?:name|property)="{re.escape(k)}" content=")[^"]*(")',
                  lambda m, v=v: m.group(1) + v + m.group(2), head)
for k, v in [("twitter:title", PLAIN), ("twitter:description", DESC)]:
    head = re.sub(rf'(<meta name="{k}" content=")[^"]*(")',
                  lambda m, v=v: m.group(1) + v + m.group(2), head)
for pat, val in [(r'(<link rel="canonical" href=")[^"]*(")', f"https://thegrassyissue.com/drops/{SLUG}"),
                 (r'(<meta property="og:url" content=")[^"]*(")', f"https://thegrassyissue.com/drops/{SLUG}"),
                 (r'(<meta property="og:image" content=")[^"]*(")', f"https://thegrassyissue.com{IMG}hero.jpg")]:
    head = re.sub(pat, lambda m, v=val: m.group(1) + v + m.group(2), head)
head = re.sub(r'<script type="application/ld\+json">.*?</script>',
              lambda m: '<script type="application/ld+json">' + json.dumps(SCHEMA) + '</script>',
              head, flags=re.S)

body = ('<div class="breadcrumb">\n  <a href="/">Feed</a><span>/</span>\n'
        '  <a href="/#feed">Drops &amp; Brands</a><span>/</span>\n  Late-Season Putter Switch</div>\n'
        f'<header class="drop-header">\n  <h1>{TITLE}</h1>\n  <div class="drop-meta">\n'
        f'    <span>{TODAY}</span><span class="dot"></span>\n'
        '    <span>Drops &amp; Brands</span><span class="dot"></span>\n'
        f'    <span>{len(TABLE)} In Stock &middot; 2 On Presale</span>\n  </div>\n</header>\n\n'
        f'<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}hero.jpg" '
        'alt="A milled putter head resting on leather, one of twenty putters in this late-season switch guide" /></div></div>\n'
        + INTRO + SQUARE + QUIET + AIM + OBJECT + CHOOSE + PRESALE + FAQ)

# ------------------------------------------------------------------- guards
_txt = st(re.sub(r"<[^>]+>", " ", body))
# The two existing putter slugs contain the banned word. Strip URLs before checking.
_prose = re.sub(r'href="[^"]*"', " ", body)
_prose = st(re.sub(r"<[^>]+>", " ", _prose))
if re.search(r"\bworth\b", re.sub(r"\bFort\s+Worth\b", " ", _prose, flags=re.I), re.I):
    raise SystemExit("BANNED WORD 'worth' in the body copy")

if len(TABLE) != 18:
    raise SystemExit(f"the guide is built around eighteen buyable putters; TABLE has {len(TABLE)}")
if [t[0] for t in TABLE] != sorted({t[0] for t in TABLE}, key=[t[0] for t in TABLE].index):
    raise SystemExit("duplicate key in TABLE")
if {t[0] for t in TABLE} != set(putter_cards.BUYABLE):
    raise SystemExit("the table and the cards disagree about which eighteen are buyable")

# Every stale figure from the first research pass, refused by name.
STALE = [(r"\$699", "Machine M12 ZTX is $799 — $699 is the Mini-Megalodon, a different head"),
         (r"\$189", "Vice VGP03 starts at $224, not $189"),
         (r"\$249(?!\.99)", "the Sub 70 TAIII 254 is $199, not $249"),
         (r"Desert\s+Inn", "the Sub 70 model is the TAIII 254 Wide Blade; Desert Inn is not its name")]
for pat, why in STALE:
    if re.search(pat, _txt, re.I):
        raise SystemExit(f"stale figure in the copy: {why}")

# Ping publishes no price. If we print one, we must say where it came from.
_ping = putter_cards.CARDS["ping"][2]
if "399.99" in _ping and "GOLF.com" not in _ping:
    raise SystemExit("Ping publishes no price — the card must attribute the figure it prints")

# The four markdowns are the spine of the post. Table and prose must agree.
_disc = [t for t in TABLE if t[6]]
if len(_disc) != 4:
    raise SystemExit(f"the intro claims four putters are discounted; the table marks {len(_disc)}")
# The table used to carry these. It is gone, so each markdown must survive in the
# putter's own card copy or the intro's "four of the eighteen" claim goes unbacked.
for _k, _b, _m, _p, _h, _f, _was in _disc:
    _card = putter_cards.CARDS[_k][2]
    if _was not in _card:
        raise SystemExit(f"{_b} {_m} is marked down from {_was} and the table no longer "
                         f"exists — the card copy must state the old price itself")
    if _p not in _txt:
        raise SystemExit(f"{_b} {_m}: {_p} is not visible anywhere on the page")

# Brand repeats are deliberate and approved. Assert them so a silent trim fails loudly.
_brands = [t[1] for t in TABLE]
for _b in ("Sub 70", "Odyssey", "Bettinardi", "Makefield"):
    if _brands.count(_b) != 2:
        raise SystemExit(f"{_b} should appear twice — Lenny approved the repeat on 9/16/26; "
                         f"found {_brands.count(_b)}. If the list changed, change this guard too.")

# Presale must stay presale. Neither may be presented as something you can buy.
for _k, _why in [("mizuno", "pre-order opened 9/9, retail 10/30"),
                 ("scotty", "pre-sale now, in shops 9/30")]:
    _blk = putter_cards.CARDS[_k][2]
    if not re.search(r"pre-?order|pre-?sale", _blk, re.I):
        raise SystemExit(f"{_k} is not shipping yet ({_why}) — the card must say so")
if "Pre-order &#8599;" not in body:
    raise SystemExit("the presale cards must not carry the same call to action as stock")
for _k in putter_cards.PRESALE:
    _before = body[:body.find('<h2 class="products-hdr">On presale</h2>')]
    if f'data-gallery="{_k}"' in _before:
        raise SystemExit(f"{_k} is on presale and may only appear in the presale section")

_ncards, _nframes = putter_cards.check()
if _ncards != 20:
    raise SystemExit(f"twenty putters were approved; putter_cards has {_ncards}")
for _k in putter_cards.CARDS:
    if f'data-gallery="{_k}"' not in body:
        raise SystemExit(f"card {_k} was built but never placed in the body")
_nboxes = body.count('class="product-card"')
if _nboxes != 20:
    raise SystemExit(f"expected 20 putter boxes, found {_nboxes}")

_imgs = re.findall(r'src="(/images/putter-switch/[\w.-]+)"', body)
_gone = [p for p in _imgs if not os.path.exists("." + p)]
if _gone:
    raise SystemExit(f"images missing on disk: {_gone}")
if len(_imgs) != len(set(_imgs)):
    raise SystemExit("an image is used twice on the page")

# Gallery chrome: image count and dot count must agree, on every card.
for _k, _v in putter_cards.CARDS.items():
    _n = len(_v[4])
    if body.count(f'data-gallery="{_k}"') != 1:
        raise SystemExit(f"gallery {_k} missing or duplicated")
    _blk = body[body.find(f'data-gallery="{_k}"'):]
    _blk = _blk[:_blk.find('<div class="product-body">')]
    # count the dots, not the wrapper: 'pg-dot' is a prefix of 'pg-dots'
    _dots = len(re.findall(r'class="pg-dot(?: on)?"', _blk))
    if _blk.count("<img") != _n:
        raise SystemExit(f"gallery {_k}: {_blk.count('<img')} images, expected {_n}")
    if _n > 1 and _dots != _n:
        raise SystemExit(f"gallery {_k}: {_dots} dots against {_n} images")
    if _n == 1 and _dots:
        raise SystemExit(f"gallery {_k} has one frame and should carry no chrome")

_words = len(_txt.split())
if _words < 1200:
    raise SystemExit(f"word count {_words} is below the 1200 floor")
if body.count('<details class="faq-q">') != len(FAQ_ITEMS):
    raise SystemExit('FAQ markup must be <details class="faq-q">')
if '<div class="faq"' not in body:
    raise SystemExit('the FAQ wrapper must be <div class="faq"> — verify-post.py matches that literal')

# Depth over consolidation: this post must point at the two that already exist.
for _slug in ("5-zero-torque-putters", "the-2026-putter-drop"):
    if _slug not in body:
        raise SystemExit(f"the existing putter page /{_slug} must be linked, not replaced")

open(f"drops/{SLUG}.html", "w", encoding="utf-8").write(head + body + tail)
print(f"wrote drops/{SLUG}.html | {len(TABLE)} buyable + 2 presale | ~{_words} words")
print(f"  {_nboxes} boxes, {len(_imgs)} frames, {len(FAQ_ITEMS)} FAQ entries")
print(f"  discounted today: {', '.join(t[1] + ' ' + t[2] for t in _disc)}")
