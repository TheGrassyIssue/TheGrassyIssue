#!/usr/bin/env python3
"""Build /drops/brand-to-know-midiron.html from the LOF template + /tmp/midiron_man.json.

House format (memory: reference_post_format):
  <h2 id> + <p class="cat-kicker"><strong>..</strong>..</p> + <div class="products-grid"> around every card.
FAQ <div> lives INSIDE the single products <section>; cut template at `<div class="faq">`,
capture the tail after the faq div closes, and re-append it.

EDITORIAL CONSTRAINTS (agreed with Lenny 2026-08-24):
  * Do NOT name the founders. Midiron publishes no name; the "my grandad" copy is unsigned
    on purpose. Names exist in the AU business register but naming them goes against how
    they present themselves. Write it as a deliberately anonymous brand.
  * Prices are AUD. Show A$ with an approximate USD conversion (rate ~0.717, Aug 2026).
  * "Golf Apparel Research" is Midiron's OWN house descriptor, not a third-party endorser.
    There is no @golfapparelresearch account. "GAR approved" is a self-approval joke.
  * Country of manufacture is NOT PUBLISHED. They say "designed in Australia" and
    "100% Australian owned" only. Never write "made in Australia".
  * No published interviews exist. Every quote below is from their own site copy.
  * Contact Cap: describe only what the photos show. No claim about licensing.
"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
MAN  = json.load(open("/tmp/midiron_man.json"))
TPL  = os.path.join(ROOT, "drops", "brand-to-know-left-of-field-golf.html")
OUT  = os.path.join(ROOT, "drops", "brand-to-know-midiron.html")
SLUG = "brand-to-know-midiron"
TITLE = "Brand to Know &mdash; Midiron, the Sydney Label That Doesn&rsquo;t Sign Its Own Work"
TITLE_TXT = "Brand to Know — Midiron, the Sydney Label That Doesn’t Sign Its Own Work"
DESC = ("Midiron is a Sydney golf label that names no founder, sells in tiny runs and shoots "
        "everything under floodlights. Nine pieces, seven releases, and a grandad's Titleist cap.")
AUD = 0.717

def usd(a): return int(round(int(a) * AUD))

CARDS = {
"contact-cap-navy": dict(
  meta="Sold out",
  desc="Their newest and best release, and the one that gave the brand its line. The copy: &ldquo;Every golfer "
       "has two games. The one they imagine and the one they play.&rdquo; It is built on a navy cap carrying a "
       "white interlocking NY. One side panel is scripted <em>Golf Is A Contact Sport</em>; the other carries "
       "<em>&ldquo;Played between expectation &amp; reality&rdquo;</em>, and Golf Apparel Research is arched across the "
       "back. High-density embroidery front, sides, rear and under the brim &mdash; the under-brim being the one bit "
       "only the wearer ever sees. Released in August, and already sold out."),
"results-cap-black": dict(
  meta="In stock",
  desc="The best piece of writing on the whole site is on this product page: &ldquo;This isn&rsquo;t a lucky golf "
       "cap. It&rsquo;s for the days when you stripe one down the middle and still walk away with a double.&rdquo; "
       "The cap says the same thing more bluntly: embroidered across the front panel, in Japanese and then in English, "
       "is <em>Very good swing. Very bad Result.</em> Black cotton twill, unstructured five-panel, embroidery front and "
       "sides, with a GAR tag on the side &mdash; Golf Apparel Research, which is Midiron&rsquo;s own house descriptor "
       "rather than anyone else&rsquo;s stamp of approval."),
"upcycled-vintage-titleist-cap": dict(
  meta="Sold out &middot; three one-offs",
  desc="The heart of the brand, and the only place the person behind it speaks in the first person. &ldquo;when i "
       "was 10, my grandad gave me a hand me down titleist cap because i didn&rsquo;t have one to wear when we "
       "played golf together. sure, it was nothing special to anyone else, but it meant everything to me.&rdquo; "
       "They hunted down vintage Titleist caps, sent them to Oxy Customs in Melbourne for reworking, and released "
       "three &mdash; one as a giveaway prize, two for sale, each a one-off. Lowercase, unsigned, no marketing voice anywhere in it."),
"tour-spec-cap-black": dict(
  meta="Sold out",
  desc="The clearest statement of what the brand is for: &ldquo;It&rsquo;s made for the quiet parts of golf &mdash; "
       "early starts, empty fairways, late finishes. The moments that don&rsquo;t need witnesses. The ones you do for "
       "yourself.&rdquo; A black cap with the Midiron star wordmark, a Tour Spec script on the side panel and not much "
       "else going on. Their photography "
       "makes the argument better than the copy does."),
"tour-spec-cap-tree-camo": dict(
  meta="In stock",
  desc="Photorealistic tree camo &mdash; their word, and it is in the URL &mdash; on an unstructured five-panel, which "
       "should not work on a golf course and somehow does. The product copy is the brand in one line: &ldquo;No loud "
       "logos. No clubhouse energy. Just a cap that does its job quietly, until someone who knows notices.&rdquo; "
       "Cotton twill with a vintage wash, adjustable strap back, and a stated aim of wearing in rather than out."),
"tour-spec-cap-field-camo": dict(
  meta="In stock &middot; the first release",
  desc="The piece that started the store &mdash; first product published, December 2025. Field camo in flatter "
       "olives and browns, and the more wearable of the two camo caps if you are not fully committed to looking like "
       "you have come straight from a deer stand. Same unstructured five-panel build, same cotton twill, same "
       "adjustable strap back."),
"detour-stripe-polo": dict(
  meta="In stock &middot; limited sizes",
  desc="Their take on a 1990s polo and the most ambitious thing they make. Heavy 300gsm cotton on a unisex boxy fit "
       "that, in their words, &ldquo;sits right without needing to be tucked. Loose where it should be. Structured "
       "where it matters.&rdquo; Bold black and cream rugby stripes, chest embroidery, a vintage-washed twill "
       "appliqu&eacute; with raw edges across the back, custom woven label at the hem and a metal MEMBER bag tag."),
"tour-spec-polo-tree-camo": dict(
  meta="In stock &middot; limited sizes",
  desc="All-over camo print on mid-weight perforated polyester, with raised silicone print and embroidery and a big "
       "arched MIDIRON across the chest. This is the one that photographs best under a flash at night, which is "
       "clearly the point &mdash; almost every shot they have taken of it is on a floodlit course after dark."),
"the-big-stick-headcover": dict(
  meta="In stock",
  desc="A driver cover in camo &mdash; their copy calls this one a field camo &mdash; padded, with embroidered detailing, a custom flag label and a "
       "premium velvet lining. Named &ldquo;The Big Stick,&rdquo; which is either a driver joke or a Teddy Roosevelt "
       "joke and works fine as both. At A$69 it is the cheapest way into the brand that is not a cap, and the only "
       "thing they make that has nothing to do with clothing."),
}

SECTIONS = [
 ("caps", "The Caps",
  "Six caps &middot; A$69 (about US$49)",
  "Caps are the brand, and have been since the first one went up in December 2025. Most are 100 per cent cotton "
  "twill on an unstructured five-panel with an adjustable strap back, and most sign off with the same deadpan "
  "line: <em>Golf Apparel Research approved</em>. That is Midiron approving itself &mdash; Golf Apparel Research "
  "is their own house descriptor, carried with a &trade; in their Instagram name and embroidered onto the goods. "
  "Then each page adds its own warning. The Field Camo: <em>hard to spot, impossible to forget</em>. The Tree "
  "Camo: <em>may attract unsolicited &lsquo;where&rsquo;d you get that?&rsquo; questions</em>. The black one: "
  "<em>you&rsquo;ll stop wearing your other caps</em>. Three of the six below are gone.",
  ["contact-cap-navy","results-cap-black","upcycled-vintage-titleist-cap",
   "tour-spec-cap-black","tour-spec-cap-tree-camo","tour-spec-cap-field-camo"]),

 ("shirts", "The Polos",
  "Two polos &middot; A$129 (about US$92)",
  "Both polos run a unisex boxy cut rather than a golf fit, which is the whole thesis: &ldquo;golf clothing never "
  "felt like the rest of our wardrobe. It belonged on the course, but nowhere else.&rdquo; One is heavyweight "
  "cotton, one is perforated polyester, and they are the only two shirts the brand has put up for sale &mdash; "
  "though a white polo with the same interlocking NY turns up in their latest campaign shots, unlisted.",
  ["detour-stripe-polo","tour-spec-polo-tree-camo"]),

 ("kit", "Everything Else",
  "One headcover &middot; A$69 (about US$49)",
  "The entire non-apparel catalogue, which is one headcover. That is not a criticism &mdash; it is the point of a "
  "brand that has put out nine things in eight months and restocks almost nothing.",
  ["the-big-stick-headcover"]),
]

FAQS = [
 ("Who is behind Midiron?",
  "Midiron does not say, and that appears to be deliberate. There is no founder name anywhere on the site and no "
  "signature on any of the writing &mdash; including the lowercase, first-person story about a grandad&rsquo;s "
  "hand-me-down Titleist cap that is the most personal thing on the site. What they do publish is that the brand is "
  "Australian: &ldquo;100% Australian owned, independent Australian business,&rdquo; run out of Sydney. No "
  "interviews with the founders have been published anywhere."),
 ("Where is Midiron based?",
  "Sydney, Australia. Their business registration publishes a postcode rather than an address &mdash; NSW 2232, in "
  "the Sutherland Shire in the city&rsquo;s south. Their own image descriptions name the location of the night "
  "shoots: &ldquo;At night time on Shortees Golf Course&rdquo; &mdash; the LED-floodlit eighteen-hole par-three at "
  "Terrey Hills, about thirty-five minutes north of the CBD and open until ten at night. The line above their "
  "mailing-list signup reads &ldquo;Built down under, played everywhere.&rdquo;"),
 ("Is Midiron clothing made in Australia?",
  "They do not say. Every geographic claim on the site is about design and ownership rather than manufacturing "
  "&mdash; &ldquo;100% Australian owned, independent Australian business,&rdquo; and &ldquo;designed in "
  "Australia&rdquo; in their page metadata &mdash; and there is no country "
  "of origin listed on any product page. We would not assume either way. What they do publish is construction "
  "detail: 100 per cent cotton twill caps, a 300gsm cotton polo, a mid-weight perforated polyester polo."),
 ("How much does Midiron cost?",
  "Caps are A$69 and polos are A$129, with the headcover also at A$69. At late-August 2026 rates that is roughly "
  "US$49 and US$92. The store is priced in Australian dollars by default, with a currency selector in the site "
  "header offering USD, CAD, GBP, EUR, DKK, NZD and SEK."),
 ("Does Midiron ship internationally?",
  "Yes. Shipping is free within Australia, and the checkout quotes international rates directly &mdash; around "
  "US$15 to the United States and New Zealand and about US$21 to the United Kingdom, both quoted at six to ten "
  "business days. The store sells into fifteen countries. Their contact form also covers &ldquo;international "
  "shipping, swing thoughts or general enquiries&rdquo; if you need something specific."),
 ("Why is everything sold out on Midiron?",
  "Because they built it that way, and they answer this on their own FAQ page: &ldquo;We release in small runs. We "
  "only open the store periodically.&rdquo; Asked whether they restock, the answer is &ldquo;Sometimes. Usually "
  "not.&rdquo; Nine products have gone up since December 2025 and three are already gone. The mailing list gets "
  "first access to drops."),
 ("What does &ldquo;Golf Apparel Research approved&rdquo; mean?",
  "It means Midiron approves of Midiron. Golf Apparel Research is the brand&rsquo;s own house descriptor &mdash; "
  "their Instagram display name is &ldquo;MIDIRON | Golf Apparel Research&trade;&rdquo; and the footer of every "
  "page reads &ldquo;Midiron Mission: Golf Apparel Research&trade;. Engineered for the course, built for everything "
  "after.&rdquo; It appears in the spec list on each product page alongside genuine details like mesh internal "
  "binding, which is the joke. There is no outside body doing the approving."),
 ("What is the Upcycled Vintage Titleist Cap?",
  "Three one-off caps, released in July 2026 and gone immediately. Midiron sourced vintage Titleist caps and sent "
  "them to Oxy Customs, a Melbourne screen-printing and garment-rework studio, to be reworked. It is "
  "the only outside collaboration the brand has done. The reason given is the closest thing to a mission statement "
  "they have published: recreating the feeling of being handed a cap by a grandparent, &ldquo;for anyone who gets it.&rdquo;"),
 ("How many drops has Midiron done?",
  "Seven releases between December 2025 and August 2026, producing nine distinct products &mdash; six caps, two "
  "polos and a headcover. They have never numbered their drops publicly, so anyone describing this as Drop 3 or "
  "Drop 4 is inventing it. The pace works out to roughly one release a month, with two of the seven being "
  "two-piece releases."),
 ("Is Midiron a good brand to buy from?",
  "If you like the aesthetic, buy it when you see it, because it will not be there later. The construction detail "
  "they publish is real &mdash; metal clasp closures, mesh internal binding, 300gsm cotton, custom woven labels "
  "&mdash; and A$69 for a cap is normal money for an independent label. The caveats are that they publish no "
  "manufacturing origin, most of the catalogue is gone at any given moment, and this is a very new and very small operation "
  "with almost nothing in stock at any given moment."),
]

# ---------------------------------------------------------------- build
h = open(TPL, encoding="utf-8").read()
head = h[:h.index('<div class="faq">')]
_i = h.index('<div class="faq">'); _d = 0
for _m in re.finditer(r'<div\b|</div>', h[_i:]):
    _d += 1 if _m.group(0) != "</div>" else -1
    if _d == 0:
        TAIL = h[_i + _m.end():]; break
else:
    raise SystemExit("could not find close of faq div")

def gallery(key, alt):
    fr = MAN[key]["frames"]; n = len(fr)
    t = "".join('<div class="pg-frame"><img src="/images/midiron/%s" loading="lazy" alt="%s"></div>'
                % (f, alt) for f in fr)
    g = '<div class="product-gallery"><div class="pg-track">%s</div>' % t
    if n >= 2:
        g += ('<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
              '<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
              '<span class="pg-count">1/%d</span><div class="pg-dots">%s</div>'
              % (n, "".join('<button class="pg-dot%s" data-i="%d" aria-label="View image %d"></button>'
                            % (" on" if i == 0 else "", i, i + 1) for i in range(n))))
    return g + "</div>", n

def card(key):
    c = CARDS[key]; m = MAN[key]
    name = m["title"].replace('"', "&ldquo;", 1).replace('"', "&rdquo;", 1)
    g, n = gallery(key, "%s by Midiron, Sydney golf brand" % m["title"].replace('"', ""))
    price = "A$%s <span style=\"opacity:.6\">(about US$%d)</span>" % (m["price"], usd(m["price"]))
    return ('  <div class="product-card" data-frames="%d">\n    %s\n'
            '      <div class="product-body">\n'
            '        <div class="product-brand">Midiron &middot; %s</div>\n'
            '        <div class="product-name">%s &middot; %s</div>\n'
            '        <div class="product-desc">%s</div>\n'
            '        <a href="https://midiron.shop/products/%s" target="_blank" rel="noopener" '
            'class="product-link">%s &#8599;</a>\n'
            '      </div>\n  </div>\n'
            % (n, g, c["meta"], name, price, c["desc"], m["handle"],
               "View" if not m["avail"] else "Shop"))

body = []
for sid, sh2, kick_lead, kick_body, keys in SECTIONS:
    body.append('<h2 id="%s">%s</h2>' % (sid, sh2))
    body.append('<p class="cat-kicker"><strong>%s</strong>%s</p>' % (kick_lead, kick_body))
    body.append('<div class="products-grid">')
    body += [card(k) for k in keys]
    body.append('</div>')
BODY = "\n".join(body)

FAQ_HTML = ('<div class="faq">\n' + "\n".join(
    '    <details class="faq-q"><summary>%s</summary><p>%s</p></details>' % (q, a) for q, a in FAQS)
    + "\n  </div>" + TAIL)

page = head + FAQ_HTML
mark = '<section class="products">'
page = page[:page.index(mark) + len(mark)] + "\n" + BODY + "\n" + page[page.index('<div class="faq">'):]

def sub1(pat, rep, s, label):
    s2, n = re.subn(pat, rep, s, count=1, flags=re.S)
    assert n == 1, "head surgery failed: " + label
    return s2

page = sub1(r'<title>.*?</title>', '<title>%s | The Grassy Issue</title>' % TITLE_TXT, page, "title")
page = sub1(r'<meta name="description" content="[^"]*"',
            '<meta name="description" content="%s"' % DESC, page, "description")
for k in ["og:title", "twitter:title"]:
    page = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*(")' % k,
                  r'\g<1>%s\g<2>' % TITLE_TXT, page)
for k in ["og:description", "twitter:description"]:
    page = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*(")' % k,
                  r'\g<1>%s\g<2>' % DESC, page)
page = re.sub(r'(https://thegrassyissue\.com/drops/)brand-to-know-left-of-field-golf',
              r'\g<1>%s' % SLUG, page)
page = sub1(r'<h1>.*?</h1>', '<h1>%s</h1>' % TITLE, page, "h1")
page = sub1(r'(<div class="breadcrumb">.*?<span>/</span>\s*)[^<]*(\s*</div>)',
            r'\g<1>' + TITLE_TXT + r'\g<2>', page, "breadcrumb")
page = sub1(r'<div class="drop-meta">.*?</div>',
            '<div class="drop-meta">\n    <span>9 Pieces</span>\n  </div>', page, "drop-meta")
page = sub1(r'<div class="drop-hero">.*?</div></div>',
            '<div class="drop-hero"><div class="drop-hero-img">'
            '<img src="/images/midiron/hero-midiron.jpg" '
            'alt="Midiron camo golf polo photographed under floodlights on a Sydney par-three course" />'
            '</div></div>', page, "hero")
page = sub1(r'<div class="sidebar-detail"><span class="l">Pieces</span>.*?<span class="l">Range</span><span>[^<]*</span></div>',
  '<div class="sidebar-detail"><span class="l">Pieces</span><span>9</span></div>\n'
  '      <div class="sidebar-detail"><span class="l">Releases</span><span>7</span></div>\n'
  '      <div class="sidebar-detail"><span class="l">Based</span><span>Sydney, AU</span></div>\n'
  '      <div class="sidebar-detail"><span class="l">Range</span><span>A$69 &ndash; A$129</span></div>',
  page, "sidebar")
page = sub1(r'<span class="hashtag">#LeftOfFieldGolf</span>',
            '<span class="hashtag">#Midiron</span>', page, "hashtag")
page = page.replace('<span class="hashtag">#GearEdit</span>',
                    '<span class="hashtag">#AustralianGolf</span>')

INTRO = """
    <p>Midiron will not tell you who runs it. There is no founder name on the site, no photograph, no byline on
    any of the writing &mdash; and the writing is the reason to pay attention. Somewhere on a product page for a
    sold-out cap is this, in lowercase, unsigned:</p>
    <p style="padding-left:18px;border-left:2px solid var(--ink);font-style:italic;">&ldquo;when i was 10, my
    grandad gave me a hand me down titleist cap because i didn&rsquo;t have one to wear when we played golf
    together. sure, it was nothing special to anyone else, but it meant everything to me.&rdquo;</p>
    <p>They went and found vintage Titleist caps, had a Melbourne rework studio customise three of them, gave one away
    and sold the other two as one-offs. That is the whole operation in one gesture: small, specific, slightly sentimental, and gone
    before most people heard about it.</p>
    <p>What can be established is that the brand is Australian and run out of Sydney, that it registered in August
    2025 and put its first product up that December, and that in the eight months since it has released nine things
    across seven drops. Six caps, two polos, one headcover. Three are already sold out, and their own FAQ is blunt
    about whether that changes: &ldquo;Sometimes. Usually not.&rdquo;</p>
    <p>The founding complaint is one every independent golf label starts from, but they put it better than most:
    &ldquo;golf clothing never felt like the rest of our wardrobe. It belonged on the course, but nowhere else.&rdquo;
    What follows from that is a line we have not seen anyone else write &mdash; &ldquo;we don&rsquo;t believe
    changing outfits should be part of finishing a round.&rdquo;</p>
    <p>The photography is doing at least half the work here, and that deserves saying. Most of what they shoot is at
    night, on a floodlit par-three, with a hard flash &mdash; long shadows, wet grass, headlights, someone
    swinging in the dark. It matches a line from the Tour Spec Cap page exactly: the brand is for &ldquo;early
    starts, empty fairways, late finishes. The moments that don&rsquo;t need witnesses.&rdquo;</p>
    <p>One caveat before the gear. Six of the nine products sign off &ldquo;Golf Apparel Research approved,&rdquo;
    which reads like third-party validation and is not. Golf Apparel Research is Midiron&rsquo;s own house descriptor, and
    the line sits at the bottom of the spec list, straight after <em>custom Midiron branded trims</em>, like any
    other feature. They are approving themselves, on purpose, with a straight face. Once you notice it the
    rest of the brand makes more sense.</p>
"""
page = sub1(r'(<div class="writeup-body">).*?(\s*</div>)', lambda m: m.group(1) + INTRO + m.group(2),
            page, "intro")

def strip(s):
    s = re.sub(r'<[^>]+>', '', s)
    for a, b in [("&mdash;","—"),("&ndash;","–"),("&rsquo;","’"),("&ldquo;","“"),("&rdquo;","”"),
                 ("&amp;","&"),("&middot;","·"),("&trade;","™"),("&eacute;","é")]:
        s = s.replace(a, b)
    return s

art = json.dumps({"@context":"https://schema.org","@type":"Article","headline":TITLE_TXT,
  "description":DESC,"author":{"@type":"Organization","name":"The Grassy Issue"},
  "publisher":{"@type":"Organization","name":"The Grassy Issue"},
  "datePublished":"2026-08-24","dateModified":"2026-08-24",
  "mainEntityOfPage":"https://thegrassyissue.com/drops/%s" % SLUG}, ensure_ascii=False)
faq = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":
  [{"@type":"Question","name":strip(q),
    "acceptedAnswer":{"@type":"Answer","text":strip(a)}} for q, a in FAQS]},
  ensure_ascii=False)

page = re.sub(r'<script type="application/ld\+json">.*?</script>',
              lambda m: '<script type="application/ld+json">%s</script>' % art,
              page, count=1, flags=re.S)
last = page.rfind('<script type="application/ld+json">')
end = page.index('</script>', last) + len('</script>')
page = page[:last] + '<script type="application/ld+json">%s</script>' % faq + page[end:]

open(OUT, "w", encoding="utf-8").write(page)
print("wrote", OUT, len(page), "bytes")
print("cards:", page.count('<div class="product-card'), " grids:", page.count('<div class="products-grid">'))

# --- house voice guard -------------------------------------------------------
# Card copy and section kickers are owned by data/copy-deck.json, not by this
# script (see VOICE.md). Re-applying the deck here means a rebuild can never
# silently restore the pre-2026-08-27 copy. Safe to run repeatedly.
import subprocess as _sp, os as _os
_sp.run(["python3", _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "copy-deck.py"),
         "apply"], check=False)
