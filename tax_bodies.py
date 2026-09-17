#!/usr/bin/env python3
"""Editorial bodies for taxonomy pages that have earned one.

build-brand-taxonomy.py generates eighteen pages from a title, a description and
an intro. That is the right floor for a page whose job is routing. It is not
enough for a page someone might arrive at from a search engine having never
heard of us.

This module holds the long-form body for the pages we choose to build out, keyed
by taxonomy slug. A slug absent from BODIES renders exactly as before, so
nothing here can break the other seventeen.

Each entry:
  top     -- sections rendered BETWEEN the intro and the brand grid. Explainer
             material: what the category is, how to read it, what the words mean.
  bottom  -- sections rendered AFTER the brand grid. For gorpcore this is one
             carousel per brand (tax_brands.py), four products each.
  faq     -- [(question, answer)] rendered as a visible FAQ and merged into the
             page's JSON-LD as a FAQPage entity.

HOUSE RULES THAT APPLY HERE AS THEY DO TO POSTS: no 'worth'; no ranking other
brands down; every price read from the brand's own store with the date stated;
never a currency we have not verified.

PRICES IN THIS FILE WERE READ 9/17/26. Sounder charges in sterling and Left of
Field in Australian dollars, because that is what their own stores charge — do
not silently convert them to dollars, and do not copy the site's older Left of
Field figures, which are in USD and do not reconcile against the AUD list price.
"""
import tax_brands

GORP_TOP = """
<section class="tx-sec">
  <h2>What gorpcore means once it reaches a golf course</h2>
  <p>Gorp is trail mix &mdash; good old raisins and peanuts. Gorpcore is what happened when the
  clothing built for carrying that trail mix up a mountain became something people wore because
  they liked how it looked. The golf version arrives late and sideways, and the reason it works is
  more practical than the name suggests.</p>
  <p>Golf already had technical clothing. It simply called it performance, cut it in a polo shape,
  and made it out of shiny polyester. What changes under gorpcore is not the technology but the
  reference: the benchmark stops being a tour player in a Sunday red and starts being hiking,
  climbing and camping kit. That shift matters on the course because a golfer who walks is doing
  roughly a four-mile hike with weather exposure and a load hanging off one shoulder. Outdoor gear
  is designed for exactly that problem. Golf performance apparel is designed around a swing.</p>
  <p>Which is why the pieces on this page skew toward outer layers, bags and trousers rather than
  polos. The polo was never the thing gorpcore had an argument with.</p>
</section>

<section class="tx-sec">
  <h2>The materials, decoded</h2>
  <p>Most of the vocabulary here is borrowed wholesale from outdoor retail, and it is genuinely
  descriptive rather than decorative &mdash; each of these words names a specific construction you
  can see or feel. Here is what the ones you will actually encounter mean.</p>
  <dl class="tx-gloss">
    <dt>Ripstop</dt>
    <dd>The faint grid you can see in the cloth. A reinforcing thread is woven in every few
    millimetres, so a tear runs to the next square and stops rather than opening up the panel.
    <strong>Sounder</strong>'s Pac Mach range uses a Japanese recycled-polyester ripstop light
    enough that the jacket stuffs into a bag made from the same cloth.</dd>

    <dt>Dyneema composite</dt>
    <dd>Not a weave at all &mdash; a laminate, with ultra-high-molecular-weight polyethylene fibre
    laid in sheets between films. It reads matte and slightly papery in the hand and takes no
    leather trim. <strong>Sentinel Golf</strong> builds its Basecamp Walker from it.</dd>

    <dt>X-Pac</dt>
    <dd>A laminated sailcloth construction, usually with a visible X-shaped reinforcing grid. It is
    the standard material for small hard-wearing carry items; Sentinel's rangefinder case pairs an
    RX30 face with a 1.5mm neoprene lining.</dd>

    <dt>Saltex</dt>
    <dd>A nylon woven in Japan, given a salt bath and then heat-treated, which leaves it reacting
    to humidity rather than sitting dead. Sentinel's collaboration with Chicago's 1733 wraps it
    around cotton batting and a 400D packcloth lining.</dd>

    <dt>Polar fleece</dt>
    <dd>Sounder's Himalayas range is Italian polar fleece made up in Portugal &mdash; and the name
    is the joke the whole category runs on. It is called Himalayas after the Ladies' Putting Course
    at St Andrews, not the mountain range.</dd>

    <dt>Hydrostatic head</dt>
    <dd>The millimetre figure on a waterproof: how tall a column of water the fabric holds back
    before it lets go. Sounder's jacket with Protected Species is rated to 15,000mm, with laser-cut
    and heat-welded seams and a two-year waterproof guarantee.</dd>

    <dt>The gusset</dt>
    <dd>The oldest idea here and still the best. A diamond panel set into the crotch of a trouser
    lets the leg travel without the waistband following it. <strong>Gramicci</strong> put one in a
    climbing pant in 1982 alongside an integrated webbing belt, and neither detail has needed
    revising since.</dd>
  </dl>
</section>

<section class="tx-sec">
  <h2>Two routes in, and they behave differently</h2>
  <p>The brands below arrive at the same place from opposite directions, and it is the single most
  useful thing to know before you shop the category.</p>
  <p><strong>Adopted.</strong> <strong>Gramicci</strong> has been making the same climbing pant
  since 1982 and got pulled onto golf courses by golfers, not by a marketing plan.
  <strong>Carhartt WIP</strong> has made workwear-derived clothing in Europe under licence since
  1994 and turns up on this page because of one pique polo. <strong>Realtree</strong> is a
  camouflage licensor rather than a clothing brand, and reaches golf through partners &mdash; PUMA
  Golf and Sun Mountain among them. None of these three set out to dress a golfer. The fit is
  roomier than golf cuts, the fabrics are heavier, and nothing has been engineered around a
  shoulder turn.</p>
  <p><strong>Built.</strong> <strong>Sentinel Golf</strong>, <strong>Sounder</strong>,
  <strong>Left of Field Golf</strong>, <strong>Agronomy Workshop</strong>,
  <strong>Odd Ritual</strong>, <strong>Sunday Golf</strong> and <strong>Ghost Golf</strong> went the
  other way, taking outdoor materials and outdoor hardware and making golf product out of them on
  purpose. Left of Field designed its Elements line after a trip to Barnbougle and named the pieces
  after the coast around it. Sentinel put Dyneema on a bag pattern that had been settled since the
  1990s. These fit like golf clothing and behave like outdoor clothing, which is the combination
  most people are actually looking for.</p>
  <p>A third position sits between them and is the reason this page is not just a fabric list.
  <strong>Agronomy Workshop</strong> and <strong>Odd Ritual</strong> work in heavy cotton and cotton
  twill rather than laminates &mdash; a 17.5oz work shirt made in Los Angeles, a 230gsm twill caddie
  jacket made in Cape Town. No membrane, no rating, no grid in the weave. They belong here because
  gorpcore has always had a workwear half, and because a cotton shirt that shrugs off a morning is
  solving the same problem by older means.</p>
</section>
"""

GORP_FAQ = [
 ("What does gorpcore mean in golf?",
  "Gorpcore describes outdoor and hiking clothing worn as a style choice rather than for a hike "
  "&mdash; gorp being trail mix. In golf it means ripstop, fleece, laminated bag fabrics, webbing "
  "and bucket hats replacing the shiny polyester that the category used to call performance. The "
  "practical case is that walking eighteen holes is closer to a four-mile hike with a load than it "
  "is to any other sport, so equipment designed for hiking tends to do the job well."),
 ("Is gorpcore allowed under a golf dress code?",
  "Usually, but the checks are the same ones as always and have nothing to do with the fabric. "
  "Most private clubs still ask for a collar, still refuse denim, and many still ask that a hat be "
  "worn forward. A ripstop jacket, a fleece and a gusseted cotton trouser pass those tests without "
  "difficulty. The pieces that draw attention are collarless tops and cargo pockets, so if you are "
  "playing somewhere with a printed code, that is the pair to check before you go."),
 ("How is this different from technical golf apparel?",
  "Mostly by reference point rather than by technology. Technical golf apparel takes a golf "
  "silhouette and improves the fabric. Gorpcore takes an outdoor silhouette &mdash; a shell, a "
  "fleece, a gusseted trouser &mdash; and brings it to the course largely as it is. You can see the "
  "difference in what each one optimises: a golf polo is cut around the swing, while a hiking shell "
  "is cut around carrying something for several hours in weather."),
 ("Which of these brands actually make golf-specific products?",
  "Sentinel Golf, Left of Field Golf, Sounder, Sunday Golf, Ghost Golf, Agronomy Workshop and Odd "
  "Ritual all design for golf directly. Gramicci and Carhartt WIP make outdoor and workwear "
  "clothing that golfers adopted, so nothing in either range is built around a golf swing. Realtree "
  "is a camouflage licensor rather than a manufacturer, and reaches the course through partners "
  "such as PUMA Golf and Sun Mountain."),
 ("What should I buy first?",
  "An outer layer, because it is where the difference is most obvious and most useful. A packable "
  "ripstop jacket covers the wind and the shower you did not plan for and takes up almost no room "
  "in the bag; a proper waterproof with a stated hydrostatic head and welded seams is the step up "
  "from that. Bags and trousers are the deeper end of the category and are easier to judge once you "
  "have lived with one piece of it."),
]


BODIES = {
 "gorpcore": {"top": GORP_TOP,
              "bottom": tax_brands.brands_section(tax_brands.GORP_BRANDS),
              "faq": GORP_FAQ},
}
