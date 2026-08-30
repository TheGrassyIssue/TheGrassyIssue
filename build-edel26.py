#!/usr/bin/env python3
"""
build-edel26.py — Brand to Know: Edel Golf, built on the Kingfisher structure.

Lenny, 2026-08-30: "let's do that Edel Golf - brand to know full treatment. Use
Kingfisher golf as a template example."

WHY THIS POST EXISTS
--------------------
The /brands card for Edel led with a blade HEADCOVER because all six Edel images
on disk were headcovers — not one photograph of a putter, from a company whose
entire reputation is putters. This post sources the clubs.

THE FACT THAT CHANGED THE POST
------------------------------
Our index line read "David Edel's putters, fitted like irons and still
hand-finished in Austin." Both halves are now wrong:

  * David Edel LEFT in 2023. MyGolfSpy, Tony Covey, 26 Apr 2023 — the official
    statement is that he "has no affiliation or role with the company moving
    forward." Doug Coors (ex-CoorsTek) bought it.
  * HQ is Arvada, COLORADO. Verified on edelgolf.com/pages/contact-us —
    5280 Ward Rd, Arvada CO 80002, (303) area code. The Liberty Hill TX fitting
    page 404s and the fitter locator returns zero Edel-owned Texas locations; an
    Austin reader now books through GOLFTEC.

Lenny's call: run it as a FOUNDER RETROSPECTIVE, past tense, with the handover
stated plainly — and move the brand out of the Texas hub. Do not write a present
tense sentence that puts this company in Austin.

QUOTES — three sources, three different levels of care
------------------------------------------------------
1. OTL Magazine, "David Edel: Game Changer," by Tony Dean —
   https://otlgolf.com/david-edel-game-changer/. Real quotation marks, attributed.
   NO PUBLICATION DATE on the page (asset paths suggest ~2017) so the post cites
   the outlet and author WITHOUT a date. Don't invent one.
2. Paul Cervantes, "An Interview with David Edel of Edel Golf," 29 May 2018 —
   a Q&A TRANSCRIPT. Answers sit under a bolded `David Edel:` label and are NOT
   in quotation marks in the source. They are verbatim first person, so they are
   attributed here as "told Paul Cervantes" rather than set as a press quote.
3. edelgolf.com's own blog — brand-published, labelled as such in the copy.

The OTL line about reputation is SPLIT by an attribution in the original
("...easy to loose and my Dad instilled that..." / "It bears my name...").
The two halves are never merged here. The source also prints "loose" for "lose";
that fragment is avoided rather than silently corrected.

IMAGE TRAPS HIT (all handled)
-----------------------------
  * eas-2-0-putter-0 had a MyGolfSpy "MOST WANTED" badge burned in — deleted and
    the gallery renumbered, so EAS has 3 frames not 4.
  * Edel-UTIron-Main_mygolfspy_logo.png likewise excluded at download time.
  * The Array galleries leak a GRIP photo (DualLayerPutterGrips*.jpg) into the
    putter galleries — filtered.
  * SMS Pro Wedge ships two marketing BANNERS with text in its gallery — filtered.
  * The Edel 467 filenames say "Augusta" but Edel's own copy carefully says
    "a certain April tradition." Follow their lead: the words Augusta and Masters
    do NOT appear in this post.

18 products, 3 sections of 6 — the grid is 3-wide, so 6/6/6 leaves no orphan row.
"""
import os, re, json, html as H, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SLUG = "brand-to-know-edel-golf"
PAGE = os.path.join(ROOT, "drops", SLUG + ".html")
TPL = os.path.join(ROOT, "drops", "brand-to-know-kingfisher-golf.html")
IMG = "/images/edel-golf"

SK = {p["handle"]: p for p in json.load(
    open(os.path.join(ROOT, "research", "edel26-skus.json")))}

TITLE = "Brand to Know &mdash; Edel Golf"
DESC = ("Edel Golf fits putters the way good shops fit irons &mdash; by where you actually "
        "aim, measured with a mirror and a laser. A profile of David Edel's method, the "
        "clubs it produced, and the company that carried it on after he left.")


def money(v):
    return v


# ---------------------------------------------------------------- copy
DESCS = {
"bloom":
 "Butterfly and floral engraving cut into a milled body, shot in a flowerbed under smoke. "
 "One of four Workbench limited editions and the least sensible thing Edel has made in "
 "years, which is exactly why it is here.",
"bowline":
 "Named for the knot, detailed in maritime signal flags, photographed on a marina dock "
 "against a rust-red buoy. The best-looking object in the current catalog and the one that "
 "makes the case that a putter can be a piece of design.",
"ice-brick":
 "The Brick shape in a cold blue finish, shot on actual ice. Milled, torque balanced, and "
 "limited &mdash; the Workbench series exists to let the shop build things the main line "
 "cannot justify.",
"swan-neck-mallet":
 "A swan-neck mallet in a torched gold patina, released for a certain April tradition. "
 "Warm metal, dark walnut backdrop, and a shape that leans further from the Array system "
 "than anything else Edel sells.",
"edels-the-brick-putter":
 "A reissue of a heritage Edel head in stainless, torque balanced, sold through in a single "
 "window. The Brick is the shape people email the company about, which is the whole argument "
 "for bringing it back.",
"edel-e-t01-putter":
 "Edel&rsquo;s zero-torque entry, carbon steel, built so the face resists opening through "
 "the stroke. Gone in one release. Zero torque is the loudest category in putters right now "
 "and Edel arrived at it from its own torque-balance work rather than the trend.",
"array-f-1-putter":
 "This is the entry point to the whole system. It takes five interchangeable hosels, six "
 "alignment plates and adjustable weights from a 5g titanium to a 25g tungsten &mdash; a putter "
 "you configure until you aim it straight, rather than one you learn to compensate for.",
"array-f-2-putter":
 "The mid mallet in the Array family, striking surface forged and milled from 1025 carbon "
 "steel. Same modular kit as the F-1; a different footprint behind the ball, which is the "
 "variable that moves most players&rsquo; aim.",
"array-f-3-putter":
 "The largest of the F heads. In an Edel fitting, head size is not a taste question &mdash; "
 "a bigger shape drags some eyes left and settles others, and you find out which you are with "
 "a mirror on the face.",
"array-b-1-putter":
 "The blade in the Array line, for players whose aim locks in behind a thin, square top rail. "
 "Every hosel and plate from the mallets bolts on, so the blade is a configuration rather "
 "than a separate product.",
"center-shafted-array":
 "Added late in 2025: the Array heads with the shaft entering dead centre. Center shafted "
 "reads square to a particular kind of eye, and that eye has been badly served by a market "
 "obsessed with plumber&rsquo;s necks.",
"eas-2-0-putter":
 "Torque balanced, with a concave radius scooped out of the back and a blade profile at "
 "address. At $250 it is the cheapest way into Edel&rsquo;s thinking about face rotation, "
 "and the one they describe as their neutral aiming shape.",
"sms-pro-wedge":
 "Edel builds this in four grinds and three bounce tiers, with a patented Flip Weight that "
 "shifts mass to the heel, the neutral position or the toe &mdash; 56 combinations from one "
 "head. They deliberately run bounce higher than the industry does.",
"sms-wedge":
 "The prior generation, still made: V, C, T, D and P grinds, weighted for how you actually "
 "release the club. The hosel is shortened and the heel scalloped to drag the centre of "
 "gravity toward the middle of the face.",
"edel-sms-utility-iron":
 "The newest club in the range and the first Edel long iron built for players who cannot hit "
 "a 3-iron. Hollow body, forgiving, and priced as a single club rather than a set upgrade.",
"sms-irons":
 "Forged hollow-body 1025 carbon with a maraging steel face cup and a urethane foam fill, "
 "sold by the set. Swing Match Weighting carries the same idea as the putters: the club is "
 "matched to the person, not the shelf.",
"aim-check":
 "The fitting method in a box &mdash; a laser, a mirror for the face and a target, so you can "
 "run the aim test on a practice green. Edel&rsquo;s own copy says 97 per cent of golfers "
 "cannot aim at their intended target. This is how they show you.",
"edel-dual-layer-putter-grips":
 "A dual-layer grip in standard and slim rounds. Grip weight is a live variable in an Edel "
 "fitting rather than an afterthought, because counterweight above the hands changes how the "
 "head releases.",
}

SECTIONS = [
 ("workbench", "The Workbench &mdash; Where the Shop Shows Off",
  # NOTE: the first draft ended "...photographs its clubs like they are worth looking
  # at." "Worth" is banned in TGI copy, blanket, and verify-post.py catches it.
  "<strong>Four limited editions and two reissues.</strong> The Workbench series is Edel building "
  "objects rather than inventory &mdash; and it is where the current company finally photographs "
  "its clubs like they matter.",
  ["bloom", "bowline", "ice-brick", "swan-neck-mallet",
   "edels-the-brick-putter", "edel-e-t01-putter"]),
 ("array", "The Array System &mdash; Aim, Fitted",
  "<strong>Five hosels, six alignment plates, adjustable weights.</strong> This is the fitting "
  "philosophy turned into a product you can buy: change the shape until the laser says you are "
  "pointed where you think you are.",
  ["array-f-1-putter", "array-f-2-putter", "array-f-3-putter",
   "array-b-1-putter", "center-shafted-array", "eas-2-0-putter"]),
 ("scoring", "Wedges, Irons and the Method Itself",
  "<strong>The rest of the scoring end.</strong> Edel argues the strokes are down here, not off "
  "the tee &mdash; and sells you the aim test separately in case you would rather run it on a "
  "practice green than in a fitting bay.",
  ["sms-pro-wedge", "sms-wedge", "edel-sms-utility-iron", "sms-irons",
   "aim-check", "edel-dual-layer-putter-grips"]),
]

LOOK = [("look-1", "A Bowline putter laid against marina rope on a dock"),
        ("look-2", "Maritime signal-flag inlays on the Bowline sole, against a rust-red buoy"),
        ("look-3", "The Bowline at the water's edge beside a channel marker"),
        ("look-4", "The Bloom putter in a flowerbed under drifting smoke"),
        ("look-5", "The Bloom headcover, floral print, on dark soil and marigolds"),
        ("look-6", "The Ice Brick photographed on ice")]


def gallery(key, name, n):
    frames = "".join(
        f'<div class="pg-frame"><img src="{IMG}/{key}-{i}.jpg" alt="{name} &middot; view {i+1} of {n}" '
        f'loading="lazy" /></div>' for i in range(n))
    dots = "".join(f'<button class="pg-dot{" on" if i == 0 else ""}" data-i="{i}" '
                   f'aria-label="View image {i+1}"></button>' for i in range(n))
    return (f'<div class="product-gallery"><div class="pg-track">{frames}</div>'
            f'<button class="pg-arw prev" aria-label="Previous image">&#8249;</button>'
            f'<button class="pg-arw next" aria-label="Next image">&#8250;</button>'
            f'<span class="pg-count">1/{n}</span><div class="pg-dots">{dots}</div></div>')


def card(handle):
    p = SK[handle]
    n = p["frames"]
    nm = H.escape(p["title"]).replace("&quot;", "&ldquo;", 1).replace("&quot;", "&rdquo;", 1)
    nm = nm.replace("Edel&#x27;s", "Edel&rsquo;s")
    sold = not p["avail"]
    tag = "Edel Golf &middot; " + ("Sold Out" if sold else "Current")
    link = ('<span class="product-link">Sold Out</span>' if sold else
            f'<a href="{p["url"]}" target="_blank" rel="noopener" class="product-link">Shop &nearr;</a>')
    return f'''<div class="product-card" data-frames="{n}">
      {gallery(handle, "Edel Golf " + re.sub(r"<[^>]+>", "", nm), n)}
      <div class="product-body">
        <div class="product-brand">{tag}</div>
        <div class="product-name">{nm} &middot; {p["price"]}</div>
        <div class="product-desc">{DESCS[handle]}</div>
        {link}
      </div>
    </div>'''


def grid(handles):
    return ('  <div class="products-grid">\n\n    '
            + "\n\n    ".join(card(h) for h in handles) + "\n\n  </div>")


# ---------------------------------------------------------------- head
FAQ = [
 ("Who is behind Edel Golf?",
  "Edel Golf was founded in 1996 by David Edel, a former caddie, club professional and teacher "
  "who started by building putters. He sold the company and departed in 2023; MyGolfSpy reported "
  "at the time that he has no affiliation or role with the business going forward. Edel Golf is "
  "now owned and run by Doug Coors, formerly of CoorsTek, and is headquartered in Arvada, Colorado."),
 ("What makes an Edel putter fitting different?",
  "Most putter fittings start with feel. Edel starts with aim. The fitter clips a mirror to the "
  "putter face, sets a laser and a target roughly six feet away, and has the player address a ball "
  "and aim at it. Pull the ball away, fire the laser, and you see where the face was actually "
  "pointed. Head shape, hosel and alignment markings are then swapped until the player aims where "
  "they think they are aiming. Only after aim is locked do they fit head weight, grip counterweight "
  "and shaft inserts."),
 ("Why does Edel fit aim before feel?",
  "Their argument is that aim is stable. If you can aim a putter, you can aim it for life; if you "
  "cannot, you will keep making compensations in path and speed to rescue a stroke that started "
  "pointed the wrong way. Edel's own product copy claims 97 per cent of golfers cannot aim at their "
  "intended target, and their published rules of thumb are specific: lines tend to aim golfers left, "
  "lines set further back aim them further left, and no lines at all tends to create a right bias."),
 ("What is a torque balanced putter?",
  "Edel found that putters described as face balanced still want to fall open, because toe hang is "
  "measured with the shaft parallel to the ground while the stroke happens on an inclined plane. A "
  "torque balanced head puts the axis of rotation through the centre with mass distributed evenly "
  "around it, so the face sits toe-up both on the bench and in playing position. In practice it "
  "takes toe hang out of the fitting conversation."),
 ("Is Edel Golf still made in Austin, Texas?",
  "No. Edel ran out of Liberty Hill in the Austin metro through the 2010s, and several product pages "
  "still carry Austin references, but the company moved assembly and headquarters to Colorado at the "
  "end of 2022 and now lists Arvada as its address. There is no Edel-owned fitting facility in Texas "
  "&mdash; an Austin golfer books through the certified fitter network, which locally means GOLFTEC."),
 ("What does Edel Golf cost?",
  "Array putters run $350 and the EAS 2.0 is $250, which historically put a fully custom-fit Edel at "
  "about the price of an off-the-rack premium putter. The Workbench limited editions are $699. Wedges "
  "are $140 to $180 a club, iron sets $830 and up, and the Aim Check training kit is $70."),
 ("Did Bryson DeChambeau play Edel?",
  "Yes, in the founder era. Edel built DeChambeau's putters from the age of eleven and made the "
  "single-length irons he won the 2015 NCAA Championship and US Amateur with. Both David Edel and "
  "the company have told that story publicly. Note that single-length irons are no longer in the "
  "Edel catalog."),
]


def head():
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q,
                              "acceptedAnswer": {"@type": "Answer", "text": a}}
                             for q, a in FAQ]}
    art = {"@context": "https://schema.org", "@type": "Article",
           "headline": "Brand to Know - Edel Golf",
           "description": re.sub(r"&[a-z]+;", "-", DESC),
           "image": f"https://thegrassyissue.com{IMG}/hero.jpg",
           "datePublished": "2026-08-30", "dateModified": "2026-08-30",
           "author": {"@type": "Organization", "name": "The Grassy Issue"},
           "publisher": {"@type": "Organization", "name": "The Grassy Issue"},
           "mainEntityOfPage": f"https://thegrassyissue.com/drops/{SLUG}"}
    return faq_ld, art


def main(apply_=False):
    tpl = open(TPL, encoding="utf-8").read()

    # ---- head: rebuilt field by field. NEVER inherit the template's identity
    #      (see fix-template-leak.py — this is exactly how that bug is created).
    faq_ld, art = head()
    h = tpl[:tpl.find("</head>")]
    # strip every JSON-LD block from the template, then re-add ours
    h = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', "", h, flags=re.S)
    repl = {
        r"<title>[^<]*</title>": f"<title>{TITLE} &mdash; The Grassy Issue</title>",
        r'(<meta name="description" content=")[^"]*(")': rf"\g<1>{DESC}\g<2>",
        r'(<meta property="og:title" content=")[^"]*(")': rf"\g<1>{TITLE}\g<2>",
        r'(<meta name="twitter:title" content=")[^"]*(")': rf"\g<1>{TITLE}\g<2>",
        r'(<meta property="og:description" content=")[^"]*(")': rf"\g<1>{DESC}\g<2>",
        r'(<meta name="twitter:description" content=")[^"]*(")': rf"\g<1>{DESC}\g<2>",
        r'(<meta property="og:image" content=")[^"]*(")': rf"\g<1>https://thegrassyissue.com{IMG}/hero.jpg\g<2>",
        r'(<meta name="twitter:image" content=")[^"]*(")': rf"\g<1>https://thegrassyissue.com{IMG}/hero.jpg\g<2>",
        r'(<meta property="og:url" content=")[^"]*(")': rf"\g<1>https://thegrassyissue.com/drops/{SLUG}\g<2>",
        r'(<link rel="canonical" href=")[^"]*(")': rf"\g<1>https://thegrassyissue.com/drops/{SLUG}\g<2>",
    }
    for pat, rep in repl.items():
        h = re.sub(pat, rep, h, count=1)
    h += ('<script type="application/ld+json">\n' + json.dumps(art, indent=1, ensure_ascii=False)
          + "\n</script>\n<script type=\"application/ld+json\">\n"
          + json.dumps(faq_ld, indent=1, ensure_ascii=False) + "\n</script>\n</head>\n")

    nav = re.search(r"(<body>.*?</nav>)", tpl, re.S).group(1)

    header = f'''
<div class="breadcrumb">
  <a href="/">Feed</a><span>/</span>
  <a href="/#feed">Drops &amp; Brands</a><span>/</span>
  Brand to Know &mdash; Edel Golf
</div>

<header class="drop-header">
  <span class="drop-tag grass">[Drops &amp; Brands]</span>
  <h1>Brand to Know &mdash; Edel Golf</h1>
  <div class="drop-meta">
    <span>edelgolf.com</span><span class="dot"></span>
    <span>Founded 1996</span><span class="dot"></span>
    <span>18 Pieces</span>
  </div>
</header>

<div class="drop-hero"><div class="drop-hero-img"><img src="{IMG}/hero.jpg" alt="The Edel 467, a swan-neck mallet in torched gold patina, on a bar top beside two drinks and a ball" /></div></div>
'''

    writeup = '''<div class="writeup">
  <div class="writeup-body">
    <p>Edel Golf fits putters the way a good shop fits irons &mdash; by measurement, not by feel. A fitter clips a mirror to the face of the putter, sets a laser and a target about six feet away, and asks you to address a ball and aim at it. Then they take the ball away and fire the laser. Where the beam lands is where you were actually pointed, which for most people is nowhere near where they believed. Head shape, hosel and the lines painted on the top get swapped until the two agree. Only then does anyone talk about weight or feel.</p>
    <p>The idea came from teaching. David Edel caddied, turned professional and spent years giving lessons before he built anything, and he has said the club-design world had very few teachers in it. He started making putters in 1996 on the Oregon coast, moved the company to the Texas Hill Country outside Austin in the 2010s, and built a fitting system his own materials once put at more than twenty million combinations. The premise underneath all of it is that a golfer who cannot aim will spend a lifetime inventing compensations for a fault that was set before the stroke began.</p>
    <p>So this is a brand for the player who suspects the problem is not their stroke. It rewards anyone willing to sit through an hour of measurement instead of rolling six putters on a shop carpet, and anyone who would rather own one club that fits than replace one every spring. Array putters run $350, the wedges $140 to $180, and the Workbench limited editions $699. One caveat, stated plainly: David Edel sold the company and left in 2023, and Edel Golf now operates out of Colorado. The method outlived him. The rest of this page is about both halves of that.</p>
  </div>
  <aside class="sidebar">
    <div class="sidebar-card">
      <div class="sidebar-label">Details</div>
      <div class="sidebar-detail"><span class="l">Founded</span><span>1996, Oregon</span></div>
      <div class="sidebar-detail"><span class="l">Founder</span><span>David Edel (to 2023)</span></div>
      <div class="sidebar-detail"><span class="l">Now</span><span>Arvada, CO</span></div>
      <div class="sidebar-detail"><span class="l">Putters</span><span>$250&ndash;$699</span></div>
      <div class="sidebar-detail"><span class="l">Wedges</span><span>$140&ndash;$180</span></div>
      <div class="sidebar-detail"><span class="l">Irons</span><span>$830&ndash;$1,520</span></div>
      <a href="https://edelgolf.com" target="_blank" rel="noopener" class="sidebar-cta">Shop Edel Golf &nearr;</a>
      <div class="hashtags">
        <span class="hashtag">#TheGrassyIssue</span>
        <span class="hashtag">#GolfCulture</span>
        <span class="hashtag">#BrandToKnow</span>
        <span class="hashtag">#EdelGolf</span>
        <span class="hashtag">#PutterFitting</span>
        <span class="hashtag">#AimFirst</span>
      </div>
    </div>
  </aside>
</div>
'''

    prods = ""
    for i, (sid, hdr, kick, handles) in enumerate(SECTIONS):
        pull = ('''
<div class="pull-quote">
  <div class="pull-quote-inner">&ldquo;I don&rsquo;t say we build a perfect putter, and we don&rsquo;t. But then I don&rsquo;t know what a perfect putter is. We build golf clubs that are custom fit to the player and will work for them.&rdquo;<span class="pull-quote-attr">&mdash; David Edel, Edel Golf founder</span></div>
</div>
''' if i == 0 else "")
        prods += f'''
<section class="products"{' style="border-top:none;padding-top:48px"' if i else ''}>{pull}
  <h2 class="products-hdr" id="{sid}">{hdr}</h2>
  <p class="cat-kicker">{kick}</p>
{grid(handles)}
</section>
'''

    # Founder section. Kingfisher's 340px slot holds a portrait of Fiona. There is
    # no publishable photograph of David Edel — the only images of him belong to
    # OTL and Plugged In Golf. So the slot holds the aim rig in use on a practice
    # green, which is the thing he actually invented, and the alt text says so.
    founder = f'''
<section class="products" style="border-top:none;padding-top:48px">
  <h2 class="products-hdr" id="in-his-words">In His Words &mdash; David Edel on the Thing He Built</h2>
  <p class="cat-kicker"><strong>Founder&rsquo;s voice, past tense.</strong> Quotes below are verbatim from Tony Dean&rsquo;s profile for OTL Magazine and from a 2018 Q&amp;A with Paul Cervantes, both given while Edel still owned the company.</p>
  <div class="bk-founder" style="display:grid;grid-template-columns:340px 1fr;gap:40px;align-items:start;max-width:1100px">
    <div style="border:.5px solid var(--ink);overflow:hidden">
      <img src="{IMG}/turf-1.jpg" alt="Two golfers running Edel&rsquo;s aim test on a practice green, one crouching to check the ball&rsquo;s line" loading="lazy" style="width:100%;aspect-ratio:4/5;object-fit:cover;display:block" />
    </div>
    <div style="font-size:16px;line-height:1.7">
      <p>Edel grew up in Reedsport on the Oregon coast, where his family ran a salmon fishing resort, a general store and a campground. He came to golf at fifteen. He caddied, taught, worked three jobs in golf shops to stay near the game, and spent time in South America under the wing of Roberto DeVicenzo &mdash; whose trophies, including a Claret Jug, he later bought.</p>
      <p style="margin-top:16px">Teaching came first and the clubs came out of it. &ldquo;If you do what you love, you never work a day in your life&hellip; What I really enjoyed most was teaching,&rdquo; he told his own company&rsquo;s journal, which also records his observation that &ldquo;not many club designers were teachers.&rdquo; He began building putters in 1996. &ldquo;I started building putters in 1996,&rdquo; he told OTL Magazine, sitting at a cluttered desk in Liberty Hill, Texas.</p>
      <p style="margin-top:16px">The ambition was never a prettier club. &ldquo;I want to change the game of golf. I want to give players the ability to reduce golf to an internal challenge where they are limited by their skills and not by their equipment,&rdquo; he told OTL. And on why the short end of the bag: &ldquo;Everyone wants to be able to hit a tee shot 300 yards, perfectly straight, and that&rsquo;s fine. The short game, however, with putters and wedges, accounts for more strokes and if they don&rsquo;t work right, it shows.&rdquo;</p>
      <p style="margin-top:16px">Asked in 2018 how the shop treated a club professional versus a weekend player, Edel told Paul Cervantes: &ldquo;Our philosophy is we treat everyone as if they were a tour player. We don&rsquo;t make a club different for a tour player than we do for an average player trying to get better.&rdquo; He sold the company five years later.</p>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:28px;padding-top:24px;border-top:.5px solid rgba(20,20,20,.15)">
        <div>
          <div style="font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;opacity:.55;margin-bottom:6px">The Standard</div>
          <div style="font-size:14px;line-height:1.6;opacity:.85">&ldquo;When a player uses one of my putters, I want all of their practice balls to be in one tight little group.&rdquo;</div>
        </div>
        <div>
          <div style="font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;opacity:.55;margin-bottom:6px">The Name</div>
          <div style="font-size:14px;line-height:1.6;opacity:.85">&ldquo;It bears my name. I want to build a brand, so that the name Edel has a reputation&hellip;it means something.&rdquo;</div>
        </div>
        <div>
          <div style="font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;opacity:.55;margin-bottom:6px">The Ledger</div>
          <div style="font-size:14px;line-height:1.6;opacity:.85">&ldquo;If I die tomorrow&hellip; I did it my way, I did it the right way.&rdquo;</div>
        </div>
      </div>
    </div>
  </div>
</section>
'''

    handover = '''
<section class="products" style="border-top:none;padding-top:48px">
  <h2 class="products-hdr" id="after">After the Founder</h2>
  <p class="cat-kicker"><strong>What happens to a company built on one man&rsquo;s eye when he walks away.</strong></p>
  <div style="max-width:760px;font-size:16px;line-height:1.75">
    <p>In April 2023 MyGolfSpy reported that David Edel had moved on to pursue other interests, and that he had no affiliation or role with the company going forward. Doug Coors &mdash; of the brewing family, previously of the technical ceramics firm CoorsTek &mdash; had taken ownership. Assembly and headquarters moved to Colorado at the end of 2022; the company now lists an address in Arvada, and the Liberty Hill fitting page is gone.</p>
    <p style="margin-top:16px">Texas has not vanished from the site. Several product pages still say hand-finished in Austin, and there is a Texas ball marker in the accessories. But there is no Edel-owned fitting bay in the state any more. An Austin golfer who wants the aim test now books it through the certified fitter network, which locally means GOLFTEC &mdash; three of them inside the city.</p>
    <p style="margin-top:16px">What survived the handover is the method, which was always the actual asset. The Array system still sells on interchangeable hosels and alignment plates. The Aim Check kit, released under the new ownership, takes the mirror-and-laser test that used to require a certified fitting and puts it in a box for $70 &mdash; arguably the most confident thing the company has done since the sale, because it gives away the trick that used to bring people through the door. On the Champions Tour, Tim Petrovic signed in June 2024 and plays the irons, an SMS wedge and an EAS putter. Doug Coors called him &ldquo;the perfect addition to Team Edel.&rdquo;</p>
    <p style="margin-top:16px">One of the fitters put the goal better than any of the marketing does. Walking a writer through a session for Plugged In Golf, Edel master fitter Matt Jones kept returning to the same phrase for what the whole exercise is chasing: matching feel to real.</p>
  </div>
</section>
'''

    figs = "\n".join(
        f'''    <figure style="margin:0;border:.5px solid var(--ink);overflow:hidden">
      <img src="{IMG}/{k}.jpg" alt="{a}" loading="lazy" style="width:100%;aspect-ratio:4/5;object-fit:cover;display:block" />
    </figure>''' for k, a in LOOK)
    lookbook = f'''
<section class="products" style="border-top:none;padding-top:48px">
  <h2 class="products-hdr" id="lookbook">The Lookbook</h2>
  <p class="cat-kicker"><strong>The Workbench campaigns.</strong> Bowline shot at a marina, Bloom in a flowerbed, Ice Brick on ice &mdash; the first Edel photography in years that treats a putter as an object rather than a spec sheet.</p>
  <div class="bk-look" style="display:grid;grid-template-columns:repeat(3,1fr);gap:24px">
{figs}
  </div>
  <div style="font-family:var(--mono);font-size:9px;letter-spacing:.1em;text-transform:uppercase;opacity:.45;margin-top:14px">Photography courtesy of Edel Golf</div>
</section>
'''

    faq_html = ('<div class="faq">\n' + "\n".join(
        f'    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>'
        for q, a in FAQ) + "\n  </div>")
    faq_sec = f'''
<section class="products" style="border-top:none;padding-top:48px">
  <h2 class="products-hdr" id="faq">The Story &mdash; FAQ</h2>
  {faq_html}
</section>
'''

    more = tpl[tpl.rfind('<section class="more">'):]

    out = (h + nav + header + writeup + prods + founder + handover
           + lookbook + faq_sec + more)

    # .bk-founder / .bk-look carry ONLY the mobile override — the grids themselves are
    # inline-styled. Without this the founder grid keeps a fixed 340px first column on a
    # phone and the copy column collapses to a few characters wide. verify-post.py also
    # fails any class with no CSS rule anywhere on the page.
    if ".bk-founder" not in out:
        k = out.rfind("</style>")
        out = out[:k] + (
            "\n/*TGI-BTK-LAYOUT*/\n"
            ".bk-founder,.bk-look{max-width:1100px}\n"
            "@media(max-width:820px){.bk-founder{grid-template-columns:1fr!important}"
            ".bk-look{grid-template-columns:repeat(2,1fr)!important}}\n"
            "@media(max-width:480px){.bk-look{grid-template-columns:1fr!important}}\n"
        ) + out[k:]

    n = out.count('<div class="product-card')
    print(f"  cards {n}  galleries {out.count('pg-track')}  frames {out.count('pg-frame')}")
    words = len(H.unescape(re.sub(r"<[^>]+>", " ",
                re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", out, flags=re.S))).split())
    print(f"  words {words}   bytes {len(out)}")
    if apply_:
        open(PAGE, "w", encoding="utf-8").write(out)
        print("  written", PAGE)
    else:
        print("  (dry run - pass --apply)")


if __name__ == "__main__":
    main("--apply" in sys.argv)
