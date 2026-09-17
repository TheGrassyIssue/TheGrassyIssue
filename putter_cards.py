#!/usr/bin/env python3
"""The twenty putter cards for the late-season switch roundup.

EVERY FACT IN EVERY BODY BLOCK came off the brand's own live product page on
2026-09-16 — description copy, spec table, price and stock state. Nothing here is
inferred from a retailer listing, a forum post or a previous TGI post. Where the
brand publishes no price (Ping), the card says where the figure came from.

FOUR FIGURES WERE WRONG in the research pass that preceded this file and are
corrected here. They are recorded in research/putter-switch-2026.json under
`correction`, and the guard at the bottom of build-putter-switch.py refuses to
build if any of the stale numbers reappear in the copy:
  Machine M12 ZTX      $699 -> $799   ($699 is the Mini-Megalodon, another head)
  Vice VGP03           $189 -> $224   (build-to-order; 224 is a floor)
  Sub 70 "Desert Inn"  $249 -> $199   (and it is the TAIII 254 Wide Blade)
  Cobra Widesport      confirmed $199, currently down from $249.99

WHAT WAS THROWN OUT AT THE CONTACT SHEET, because the brands' own feeds are
full of things that are not the putter:
  bettinardi SOLE, SIGHTLINE, FACE   Golf Digest Hot List badge composited in
  odyssey ai-dual frames 1, 2, 3     Hot List + Zero Torque badges composited in
  odyssey ai-dual frame 5            a RED head on a page selling a black one
  evnroll RS586_Midlock-Mallet-1     the headcover
  evnroll collection-page frames     lifestyle composites with a grip inset
  makefield 4198907968, 4070664814,
           4198906983                the same fitting spec chart, three times
  makefield 4070708331, 4070711274,
           4070626472, 4334450957    grips and a bare shaft
  makefield 2984554140               a headcover
  lab BUMPER, HEEL, SOLE_PLUS        black-on-black; near-solid black at card size
  edel slant / bent / dot frames     indistinguishable from the lead at card size
  scotty group shot (695406)         pictures the 9R and 9.2R alongside the 9.5R

Two frames survive as GOOD PHOTOGRAPHS WITH A BADGE ON TOP — Bettinardi's FACE
and Odyssey's frame 3. localize-putter-switch.py trims the badge corner before
the 4:5 crop. Trimming an overlay the brand pasted on is not retouching a putter.

GALLERY MARKUP must match the house pattern verify-post.py enforces:
.product-gallery > .pg-frame > .pg-track, plus .pg-arw prev/next, .pg-dots with
one .pg-dot per frame, and .pg-count. Image count and dot count must agree.
A one-frame set gets no chrome — arrows that go nowhere are worse than honesty.
"""
import os

IMG = "/images/putter-switch/"

# key: (brand, headline, body, url, [(stem, alt)])
CARDS = {

# ---------------------------------------------------- the face will not stay square
"sub70-001z": ("Sub 70", "Sycamore 001Z &middot; $199",
  "Sub 70 took its classic 001 blade and rebuilt it as a true zero-torque putter, which is rarer than the category makes it sound &mdash; almost every zero-torque design arrives as a mallet because the geometry is easier there. Milled from soft 1045 carbon steel and co-designed with Joel Pera of Just a Potamus Golf, the same partnership behind Sub 70&rsquo;s QPQ black iron finish. <strong>It keeps the compact profile better players ask for while removing the open-and-shut face rotation a normal blade allows.</strong> $199, in stock.",
  "https://www.golfsub70.com/sub-70-001z-zero-torque-blade-putter.html",
  [("sub70-001z", "The Sub 70 Sycamore 001Z zero torque blade putter at address behind a golf ball on a green"),
   ("sub70-001z-a2", "The milled sole and Sub 70 branding on the Sycamore 001Z blade putter"),
   ("sub70-001z-a3", "The Sycamore 001Z putter head viewed from the heel alongside a golf ball"),
   ("sub70-001z-a4", "The top line and single sightline of the Sub 70 Sycamore 001Z blade putter")]),

"lab": ("L.A.B. Golf", "VZN.1i Stock &middot; $499",
  "L.A.B. built the VZN.1i around a single claim, and it is a claim about you rather than about the putter: <strong>most players aim poorly and have no idea they are doing it.</strong> The head is optically shaped to show precisely where the face is pointing, with a system of crown lines running both parallel and perpendicular to the target line. Behind the aiming sit the usual L.A.B. mechanics &mdash; zero torque and lie angle balance &mdash; keeping the head on path once you have pointed it. $499 for the stock build; L.A.B. quote one to two weeks.",
  "https://labgolf.com/products/vzn1i-stock-putter",
  [("lab", "The sole of the L.A.B. Golf VZN.1i putter showing the adjustable weight ports"),
   ("lab-a2", "The L.A.B. Golf VZN.1i putter head lit against a black studio backdrop"),
   ("lab-a3", "A player's-eye view down the shaft of the L.A.B. Golf VZN.1i putter")]),

"piretti": ("Piretti", "No-Torque Savona 2.5 365g &middot; $549",
  "A toe-up design that limits rotation and keeps the face square through the stroke, milled entirely from 303 stainless with a mid-milled face for a quieter sound and a softer strike. The Savona 2.5 is the high-MOI mallet of the no-torque line in a centre-shaft setup, <strong>milled to 365 grams</strong>. Piretti credit Mike Johnson&rsquo;s push for a genuinely no-torque stroke that still looked and felt like a classic putter, which is the tension the whole category is trying to resolve. Satin finish, KBS steel shaft, Piretti Touring Pro Black grip.",
  "https://pirettigolf.com/products/no-torque-series-savona-2-5",
  [("piretti", "The Piretti No-Torque Savona 2.5 mallet putter showing the milled sole and no-torque badging"),
   ("piretti-a2", "The Piretti Savona 2.5 putter head from above with the centre shaft entering the crown"),
   ("piretti-a3", "The Savona 2.5 mallet head viewed from the rear showing the milled cavity"),
   ("piretti-a4", "The satin milled face and topline of the Piretti No-Torque Savona 2.5")]),

"machine": ("Machine", "M12 ZTX Mallet Converter &middot; $799",
  "The dearest putter here and, by a distance, the most adjustable object in golf. The M12 ZTX is a patented modular build, <strong>100% CNC milled from aerospace materials</strong>, with tungsten adjustable weighting driving the MOI. Hosel port angles into the ZTX flanges are 70&deg; as standard and move up or down three degrees in half, one or two-degree increments through Machine&rsquo;s Upper Delta Mods; the long-putter ports start at 77&deg;. New loft spacers sit between head and flange to change loft by one or two degrees, and double as a second sighting optic square to the face.",
  "https://machineputters.com/products/m12-ztx-mallet-converter-stock",
  [("machine", "The Machine M12 ZTX mallet converter putter head resting on a dark leather surface"),
   ("machine-a2", "The Machine M12 ZTX putter at address showing the sightline and modular flange"),
   ("machine-a3", "A close view of the milled face and copper accent on the Machine M12 ZTX"),
   ("machine-a4", "The rear of the Machine M12 ZTX showing the adjustable tungsten weight ports")]),

# ---------------------------------------------------- the hands will not stay quiet
"odyssey-aidual": ("Odyssey", "Ai-DUAL Broomstick &middot; $349.99",
  "Down from $449.99, <strong>the largest single markdown in this roundup</strong>. A 48-inch broomstick on a modern centre-shafted design: the shaft sits just above the head&rsquo;s centre of gravity, so the putter rests toe-up rather than with toe hang and wants to stay square through the stroke. The &frac12; Ball alignment frames the ball rather than pointing at it. Dual-layer insert &mdash; soft urethane over a firm inner layer &mdash; with a deeper, more aggressive 19&deg; Forward Roll Design groove to get the ball rolling sooner.",
  "https://odyssey.callawaygolf.com/putters/putters-2026-square-to-square-ai-dual-max-1-2-ball-broomstick.html",
  [("odyssey-aidual", "The Odyssey Ai-DUAL broomstick putter head behind a golf ball on a putting green"),
   ("odyssey-aidual-a2", "The Odyssey Ai-DUAL Square 2 Square MAX head from above showing the half-ball alignment")]),

"evnroll": ("Evnroll", "V Series V5.1 MidLock &middot; $429",
  "MidLock sits between a conventional putter and a full armlock &mdash; a longer grip braced against the lead forearm without committing to 42 inches. The V5.1 head is the players&rsquo; mallet of the V Series: curved rear wings, a connected back alignment bar, a single top sightline, and a <strong>100% milled 303 stainless face set in a milled 6061 aluminium body</strong> with tungsten and steel weights for MOI. One thing to know before you order: the Long Slant hosel comes with two shafts of offset.",
  "https://evnroll.com/products/v-series-v5-1-midlock-mallet-putter",
  [("evnroll", "The Evnroll V5.1 MidLock mallet putter at address showing the connected rear alignment bar"),
   ("evnroll-a2", "The sole of the Evnroll V5.1 MidLock showing the tungsten and steel weight ports"),
   ("evnroll-a3", "The Evnroll V5.1 MidLock mallet head viewed from directly above")]),

"bettinardi-an2": ("Bettinardi", "Antidote SB2 Long &middot; $480",
  "A <strong>500-gram zero-torque mallet built from the ground up as a long putter</strong>, which matters more than it sounds: most long putters are short-putter heads on a longer stick. Bettinardi&rsquo;s Simply Balanced geometry aligns the shaft with the head so the face stays square rather than rotating. The lie is fixed at 79&deg; and the loft at 3&deg;, both set for a split-grip long stroke rather than inherited from elsewhere; toe hang reads &minus;90&deg;. 303 stainless face and engine, 6061 aluminium body, sapphire blue anodised.",
  "https://bettinardi.com/products/antidote-sb2-long-putter",
  [("bettinardi-an2", "The Bettinardi Antidote SB2 Long zero torque mallet putter from the rear"),
   ("bettinardi-an2-a2", "The Antidote SB2 Long head from above showing the sapphire blue body and alignment"),
   ("bettinardi-an2-a3", "The milled face of the Bettinardi Antidote SB2 Long putter"),
   ("bettinardi-an2-a4", "The Bettinardi Antidote SB2 Long mallet viewed from the toe at address")]),

"bettinardi-bb28": ("Bettinardi", "BB28 Armlock &middot; $495",
  "400 grams of 303 stainless in Savannah Blue, built for a grip that rests against the lead forearm so the shoulders drive the stroke and the wrists stay out of it entirely. Shaped on direct Tour feedback, it abandons the slot-back of the previous BB28 for a lower profile and a squarer, more compact look at address. The <strong>5&deg; of standard loft exists to cancel out the forward press an armlock setup demands</strong> &mdash; a spec that looks wrong on paper and is exactly right in the hand. New Variable Depth Flymill face, 70&deg; lie, 1&frac12; offset.",
  "https://bettinardi.com/products/bb28-armlock-putter-1",
  [("bettinardi-bb28", "The Bettinardi BB28 Armlock putter from the rear showing the Savannah Blue finish"),
   ("bettinardi-bb28-a2", "The sole of the Bettinardi BB28 Armlock reading 400g and milled in the USA"),
   ("bettinardi-bb28-a3", "The Bettinardi BB28 Armlock blade at address with the flame-toned finish visible")]),

"makefield-al": ("Makefield", "Arm Lock [A] Series &middot; $599",
  "CNC milled and assembled in the USA, and built to order to a degree almost nobody else offers on an armlock. <strong>36 to 42 inches in half-inch steps, lie angles from 66 to 74 plus 79, and four hosels</strong> &mdash; heel double bend, slant neck, plumbers neck and centre shaft &mdash; all in right or left hand. Standard loft is Makefield&rsquo;s own 1.8&deg;, with 3&deg; and 5&deg; heads available for players who need more forward press cancelled out. Head shapes are the Defiant and the VS series.",
  "https://makefieldgolf.com/products/makefield-arm-lock-a-series",
  [("makefield-al", "The Makefield Arm Lock putter head at address on a dark studio surface"),
   ("makefield-al-a2", "A close view of the Makefield Arm Lock head showing the milled top line and sightline"),
   ("makefield-al-a3", "The full length of the Makefield Arm Lock putter shown upright")]),

"makefield-long": ("Makefield", "Long Putter [A] Series &middot; $599",
  "The broom. Anchored against the chest or under the chin, it is the bluntest instrument available for a stroke that has stopped behaving &mdash; and Makefield&rsquo;s own copy names the yips directly rather than dancing around them. Centre shaft only, <strong>42 to 52 inches in half-inch steps at a 79&deg; lie</strong>, right and left hand, with the VS, TF and the new TITAN heads and head weights that vary by shape. CNC milled and assembled in the USA; two-piece SuperStroke or Winn grip.",
  "https://makefieldgolf.com/products/makefield-broomstick-a-series",
  [("makefield-long", "The Makefield Long putter head at address showing the milled crown and sightline"),
   ("makefield-long-a2", "A group of Makefield putter heads laid out on a dark surface showing the shape options"),
   ("makefield-long-a3", "The full length of the Makefield Long broomstick putter shown upright")]),

# ---------------------------------------------------------------- you cannot aim it
"odyssey-aione": ("Odyssey", "Ai-ONE #1 CH &middot; $249.99",
  "Down from $299.99. The #1 is Odyssey&rsquo;s plumber-neck blade and CH is the centre-shafted version, so it sits face balanced. The insert is the whole argument: an aluminium backer under a White Hot urethane striking surface, contoured on the back of the face by Callaway&rsquo;s AI to hold ball speed on strikes away from the middle. That is a more honest promise than most putter marketing makes, because <strong>the premise is that you will miss the centre, not that this will stop you.</strong> SL 90 Stroke Lab steel shaft.",
  "https://odyssey.callawaygolf.com/putters/ai-one/putters-2024-ai-one-one-ch.html",
  [("odyssey-aione", "The Odyssey Ai-ONE #1 CH centre shafted blade putter at address"),
   ("odyssey-aione-a2", "The Odyssey Ai-ONE #1 CH putter viewed from above showing the single sightline"),
   ("odyssey-aione-a3", "The Ai-ONE #1 CH putter from the rear showing the centre shaft entry"),
   ("odyssey-aione-a4", "The sole and weight ports of the Odyssey Ai-ONE #1 CH putter")]),

"edel": ("Edel Golf", "Array B-1 &middot; $350",
  "A wide blade forged and machine milled from 1025 carbon steel &mdash; the softer end of the material scale, and the reason Edel putters sound the way they do. What you are actually buying is the adjustability: <strong>five interchangeable hosels</strong> in single bend, slant, short plumber, long plumber and torque balanced, multiple alignment options, and adjustable weighting. Edel&rsquo;s argument, made for years now, is that every golfer has an aim bias and the right alignment aid is the thing that cancels it.",
  "https://edelgolf.com/products/array-b-1-putter",
  [("edel", "The Edel Array B-1 wide blade putter at address showing the alignment line"),
   ("edel-a2", "The rear of the Edel Array B-1 putter showing the Array badging and adjustable weights"),
   ("edel-a3", "The sole of the Edel Array B-1 reading precision milled with the Edel signature")]),

"ping": ("Ping", "Scottsdale TEC Ally Blue H CB &middot; $399.99",
  "Ping added the Ally Blue H as one of two new hosel configurations for the US market, and the Anser-style hosel is there specifically to sit under the square footprint of the head rather than fight it. Full shaft offset, a <strong>370-gram head on a 37.75-inch mid-length shaft with a 17-inch SuperStroke grip</strong>, built for a slight arc. The alignment system is called Eye Q &mdash; a dot plus a long line, the dot working as an anchor point for the eyes. Kristoffer Reitan won the Truist Championship with an Ally Blue H that Ping designated a PLD, though it carried the same white finish, steel sole plate and PEBAX insert as this line. <em>Ping publishes no price on ping.com; $399.99 is the launch figure GOLF.com reported for every Scottsdale TEC model.</em>",
  "https://ping.com/en-us/golf-clubs/putters/all-putters/scottsdale-tec-ally-blue-h-cb-putter",
  [("ping", "The Ping Scottsdale TEC Ally Blue H CB putter at address showing the Eye Q alignment"),
   ("ping-a2", "The Ping Scottsdale TEC Ally Blue H putter face and Anser style hosel"),
   ("ping-a3", "The cavity and steel sole plate of the Ping Scottsdale TEC Ally Blue H CB")]),

# ------------------------------------------------ nothing is wrong, you want a better object
"macgregor": ("MacGregor", "MT Milled 002 Wing Back &middot; $169.99",
  "Was $199.99, now $169.99 &mdash; the cheapest milled putter here by a wide margin. The MT Milled range starts life as a single billet of carbon steel and is CNC milled to shape, and the 002 is the wing-back mallet, weight pushed out into the wings to raise MOI. <strong>Centre shaft and face balanced</strong>, so it suits a stroke that goes straight back and straight through. 360g head including screws, 70&deg; lie, 3&deg; loft, 10-gram weights pre-installed in heel and toe with 5g and 20g kits at $20. Plush magnetic headcover included.",
  "https://www.macgregorgolf.com/putters/macgregor-golf-mt-milled-002-wing-back-mallet-center-shaft-putter/",
  [("macgregor", "The MacGregor MT Milled 002 wing back mallet putter shown from the rear"),
   ("macgregor-a2", "The MacGregor MT Milled 002 putter at address showing the alignment pattern"),
   ("macgregor-a3", "The milled face of the MacGregor MT Milled 002 wing back mallet"),
   ("macgregor-a4", "The sole of the MacGregor MT Milled 002 showing the heel and toe weights")]),

"cobra": ("Cobra", "Widesport Vintage &middot; $199",
  "Down from $249.99. A chunkier blade profile on a single-bend shaft, which puts it squarely in straight-back-straight-through territory &mdash; toe hang is 0&deg;. The face is the interesting part: LA GOLF&rsquo;s Descending Loft Face Technology, which <strong>steps the loft down through 4&deg;, 3&deg;, 2&deg; and 1&deg; rather than holding one figure across the face</strong>, evening out launch and getting the ball rolling end over end sooner. 70&deg; lie throughout; the 34-inch head is 370g and the 35-inch is 360g. KBS CT Tour shaft, SuperStroke Zenergy Pistol 1.0.",
  "https://www.cobragolf.com/products/vintage-widesport-putter",
  [("cobra", "The Cobra Widesport Vintage blade putter at an angle showing the single bend shaft"),
   ("cobra-a2", "The Cobra Widesport Vintage putter at address showing the alignment"),
   ("cobra-a3", "The Descending Loft Face Technology grooves on the Cobra Widesport Vintage face"),
   ("cobra-a4", "The sole of the Cobra Widesport Vintage putter with the Cobra badging")]),

"sub70-taiii": ("Sub 70", "TAIII 254 Wide Blade &middot; $199",
  "A limited edition built with Tommy Armour III, and the detailing is the reason to look twice. The alignment lines are replaced by a <strong>single sight dot on the top line</strong>, and the Las Vegas sign is laser-etched into the sole in reference to his 254 &mdash; a scoring record that has stood on the PGA Tour since 2003. Milled from one billet of 1045 steel with a double-milled tour face. It ships with 15-gram weights installed and two each of 5g, 10g and 20g in the box, so the swing weight and the arc are yours to set.",
  "https://www.golfsub70.com/sub-70-taiii-254-wide-blade-putter.html",
  [("sub70-taiii", "The Sub 70 TAIII 254 wide blade putter on grass showing the CNC milled badging"),
   ("sub70-taiii-a2", "The Sub 70 TAIII 254 putter at address behind a golf ball with the sight dot visible"),
   ("sub70-taiii-a3", "The laser etched Las Vegas sign and 254 on the sole of the Sub 70 TAIII wide blade"),
   ("sub70-taiii-a4", "The topline and face of the Sub 70 TAIII 254 limited edition wide blade putter")]),

"vice": ("Vice Golf", "VGP03 &middot; from $224",
  "Vice does not really sell you a putter, it sells you a configurator, and the VGP03 is the one to configure. <strong>Every choice after the $224 floor is yours</strong>: single or dual body colour, painted alignment, line, logo, sole details and face details, shaft model, length from 31 to 36 inches in half-inch steps, and a grip list that runs from their own pistol in six colours up to a Vice x P2 React. Build-to-order, which is why $224 is a starting position rather than a sticker.",
  "https://www.vicegolf.com/golf-club-customization/putters/vgp03",
  [("vice", "The Vice Golf VGP03 blade putter at address in black with lime green detailing"),
   ("vice-a2", "The Vice VGP03 putter from above showing the painted alignment line"),
   ("vice-a3", "The sole of the Vice VGP03 putter showing the VGP03 badging and paintfill"),
   ("vice-a4", "The Vice Golf VGP03 blade putter viewed from the heel")]),

"roark": ("Roark", "Lightning 1.0 &middot; $399",
  "Roark came out of decades of aerospace manufacturing, and the Lightning is its traditional blade &mdash; deliberately familiar in shape, then opened right up underneath. Hosel and face insert options, finish, and other personalised details, with <strong>different component combinations changing the balance, feel and response of the finished putter rather than only its looks</strong>. Stock configurations exist and are the cheapest way in; the point of the platform is that they are a starting position, not the end of it.",
  "https://roarkgolf.com/products/lightning",
  [("roark", "The Roark Lightning 1.0 milled blade putter at an angle showing the polished finish"),
   ("roark-a2", "The milled face of the Roark Lightning 1.0 blade putter"),
   ("roark-a3", "The sole plate of the Roark Lightning 1.0 reading Lightning 1.0 with the Roark mark"),
   ("roark-a4", "The Roark Lightning 1.0 putter viewed from above at address")]),

# ------------------------------------------------------------------------- presale
"mizuno": ("Mizuno", "M.Craft X Z2 &amp; Z3 &middot; $399.99",
  "Pre-order opened 9 September; these land in shops on <strong>30 October</strong>. Two new zero-torque necks for the M.Craft X platform &mdash; the Z2 in a new Triple Wide profile that keeps a blade-ish look at address, the Z3 a Dome Mallet with more alignment and more forgiveness. Both carry one degree of integrated shaft lean and ship with a matching SuperStroke TLT Pistol 1.0. Because M.Craft X is modular, the Z2 and Z3 back pieces are also sold on their own at $149.99 if the platform is already in your bag.",
  "https://mizunogolf.com/us/golf-clubs/m-craft-x-putters/",
  [("mizuno", "The Mizuno M.Craft X Z2 putter head with its modular back piece and weights"),
   ("mizuno-a2", "The Mizuno M.Craft X Z3 dome mallet head shown with the modular components"),
   ("mizuno-a3", "The Mizuno M.Craft X Z2 triple wide head viewed from above"),
   ("mizuno-a4", "The milled face of the Mizuno M.Craft X Z3 zero torque putter")]),

"scotty": ("Scotty Cameron", "Phantom 9.5R &middot; $549 MAP",
  "Pre-sale is open now and it reaches golf shops on <strong>30 September, US only</strong>. The 9.5R shares the 9R head shape but runs an elongated jet neck, which is what gives it more toe flow than either the 9R or the 9.2R, and a single long sightline stretching the length of the head. Full-face Studio Carbon Steel insert with chain-link milling. <strong>Cameron Young has won all three of his PGA Tour titles with a 9.5R</strong>, including the 2026 PLAYERS; Jackson Koivun put one in play the week before winning the 3M Open. 3.5&deg; loft, 70&deg; lie, 33, 34 and 35 inches, right hand only.",
  "https://www.scottycameron.com/putters/phantom/phantom-9-5r/",
  [("scotty", "The Scotty Cameron Phantom 9.5R mallet putter photographed on a dark carbon surface"),
   ("scotty-a2", "The Scotty Cameron Phantom 9.5R head from above showing the long single sightline"),
   ("scotty-a3", "The chain-link milled Studio Carbon Steel face of the Phantom 9.5R"),
   ("scotty-a4", "The Scotty Cameron Phantom 9.5R showing the jet neck and Phantom badging")]),
}

# The eighteen you can buy today, in the order the sections run.
BUYABLE = ["sub70-001z", "lab", "piretti", "machine",
           "odyssey-aidual", "evnroll", "bettinardi-an2", "bettinardi-bb28",
           "makefield-al", "makefield-long",
           "odyssey-aione", "edel", "ping",
           "macgregor", "cobra", "sub70-taiii", "vice", "roark"]
PRESALE = ["mizuno", "scotty"]


def gallery(key, frames):
    fr = "\n        ".join(f'<img src="{IMG}{s}.jpg" alt="{a}" loading="lazy" />' for s, a in frames)
    if len(frames) == 1:
        return (f'<div class="product-gallery" data-gallery="{key}">\n'
                f'      <div class="pg-frame"><div class="pg-track">\n        {fr}\n      </div></div>\n    </div>')
    dots = "".join(f'<span class="pg-dot{" on" if i == 0 else ""}"></span>' for i in range(len(frames)))
    return f"""<div class="product-gallery" data-gallery="{key}">
      <div class="pg-frame"><div class="pg-track">
        {fr}
      </div></div>
      <button class="pg-arw prev" aria-label="Previous">&#8249;</button>
      <button class="pg-arw next" aria-label="Next">&#8250;</button>
      <div class="pg-dots">{dots}</div>
      <div class="pg-count">1 / {len(frames)}</div>
    </div>"""


def card(key, cta="See it &#8599;"):
    brand, name, desc, url, frames = CARDS[key]
    return f"""<div class="product-card">
    {gallery(key, frames)}
    <div class="product-body">
      <div class="product-brand">{brand}</div>
      <div class="product-name">{name}</div>
      <div class="product-desc">{desc}</div>
      <a href="{url}" class="product-link" target="_blank" rel="noopener">{cta}</a>
    </div>
  </div>"""


def grid(keys, cta="See it &#8599;"):
    return '<div class="products-grid">\n    ' + "\n    ".join(card(k, cta) for k in keys) + '\n  </div>'


def check():
    """Every frame on disk, every alt written, no image on two cards."""
    missing, thin = [], []
    for k, (_b, _n, _d, _u, frames) in CARDS.items():
        for s, a in frames:
            if not os.path.exists(f"images/putter-switch/{s}.jpg"):
                missing.append(s)
            if len(a) < 25:
                thin.append((s, a))
    if missing:
        raise SystemExit(f"card images missing on disk: {missing}")
    if thin:
        raise SystemExit(f"alt text too thin to be useful: {thin}")
    stems = [s for v in CARDS.values() for s, _a in v[4]]
    if len(stems) != len(set(stems)):
        dupe = [s for s in set(stems) if stems.count(s) > 1]
        raise SystemExit(f"an image is used on two cards: {dupe}")
    if set(BUYABLE) | set(PRESALE) != set(CARDS):
        raise SystemExit("BUYABLE + PRESALE must account for every card exactly once")
    if len(BUYABLE) != 18 or len(PRESALE) != 2:
        raise SystemExit(f"expected 18 buyable and 2 presale; got {len(BUYABLE)} and {len(PRESALE)}")
    return len(CARDS), len(stems)


if __name__ == "__main__":
    n, f = check()
    print(f"{n} putter cards, {f} frames, all present and unique")
