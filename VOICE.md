# TGI House Voice — product copy and section kickers

Set by Lenny, 2026-08-27, after an audit found the previous copy "way too AI and
almost paranoid." This file is the spec. `voice-lint.py` enforces the mechanical
parts of it. Read this before writing any card copy.

## What a product card is for

Tell the reader what the thing **is**, what it's **made of**, where the design
**comes from**, and why it's **good**. That's it. Four things.

A card is roughly 45–75 words, two to four sentences. Brand-to-Know cards can run
longer when the piece anchors a section.

Cover, in whatever order serves the piece:

- **The brand** — who makes it, where, what they're known for. One clause, not a bio.
- **The design** — silhouette, cut, colour, hardware, pattern, proportion.
- **The material** — fabric, leather, weight, hand, construction. Be specific.
- **The lineage** — what it references, what tradition it sits in, what it looks like.
- **The wear** — who it's for, what it goes with, where it fits.

## Banned constructions

These are the tics the audit found. `voice-lint.py` fails a build on any of them.

1. **The punchline flip.** Setup, then reversal, then stop. *"That sounds like a
   low bar. It is not."* / *"licensed MLS gear that does not look like licensed MLS
   gear."* / *"a color he absolutely would not."* Not every card gets a mic drop.
   Most cards should end on a plain declarative sentence.

2. **Narrating our own sourcing.** *"and we did look."* *"the only one we could
   find."* *"the section that took the longest to fill."* *"almost the entire
   category is currently unavailable."* The reader does not care how the sausage
   got made. If a piece is sold out, say it's sold out in the meta line and move on.

3. **Justifying the slot.** Copy that argues why something earned inclusion instead
   of describing it. We picked it; that's the argument.

4. **Verbless fragment openers.** *"The most Grassy Issue object Criquet sells."*
   *"Yes, disc golf."* *"The value item of the whole store."* Start with a sentence.

5. **Stacked em-dash appositives.** Max one em-dash pair per card.

6. **Rule-of-three closers.** *"Austin brand, Austin belt maker, Austin cause, one
   strap of leather."* Lists are not endings.

7. **Hedges and intensifiers.** genuinely, essentially, truly, simply, the rare,
   arguably, admittedly. Also **worth** — a standing site-wide ban.

8. **Self-reference.** "this post," "this list," "our index," "we've covered."
   In-prose brand links do that job silently.

## Reference rewrites

> **Criquet × Zilker "Save Muny" Belt**
> Gaucho belts come out of the Argentine countryside, where ranch hands wanted
> something they could cinch over a work shirt and then forget about. Criquet
> builds theirs with Zilker Belts, a leather shop two miles up the road, in the
> colors of the campaign to save Lions Municipal. The weave has enough give to sit
> right whether you're tucked in or not, and the leather tabs will darken into
> something better-looking by next summer.

> **Duca del Cosma Grado, $179**
> Duca del Cosma is a Dutch house that makes its shoes in Italy, which is why the
> Grado reads less like golf footwear and more like something you'd keep on for
> dinner. Spikeless, waterproof, built on a chunky lugged sole with real streetwear
> proportions, and rendered in one uninterrupted black from upper to outsole. Golf
> Monthly gave it an Editor's Choice.

> **Rouqe RQ Sweater, $39**
> A cream chevron cuts across the chest of a black crewneck and that is the entire
> design — Rouqe's whole argument in one garment. They shoot it against deep maroon
> with a putter in frame and a squint that says the club championship is already
> decided. Rouqe prices its knitwear like it wants you to actually buy it.

## The opening sentence

Set by Lenny, 2026-08-27: **the first sentence of a post is the whole pitch.** If a
reader gets that one line and nothing else, it has to tell them why they are
looking at this post at all.

So the opener carries a judgement, not a fact:

- **why this brand, collection or roundup caught our eye**
- **what the brand does well** — the thing it beats everyone else at
- the reason to keep reading

It is **not** a founding date, a head office, a product count, or an explanation
of the selection criteria. Those belong in sentence two onward.

**It is never about an individual item.** The opener is the brand or the idea.
A specific product, SKU or price belongs in sentence two at the earliest, and
usually on a card. Naming a product category the brand is known for is fine
— *"Jones makes the best carry bag in golf"*, *"Seamus turns the headcover into
the most personal object in the bag"* — because that describes the whole output.

### What the whole intro has to cover

Set by Lenny, 2026-08-29, after the Forden draft opened on a 1938 physics
experiment at MIT: **the intro is an inside look at the brand, not a history
lesson.** Before a reader reaches the first product they need three things:

1. **What it is** — what the brand makes and what it is specific about.
2. **The inspiration** — where the look comes from, in a line or two.
3. **Who it is for** — the actual golfer, described concretely.

A good origin story is still good material. It just does not lead, and it does
not get a paragraph of its own before the reader knows what they are looking at.
Compress it into the "inspiration" beat, or move it further down the page.

The Forden rewrite is the reference: *"Forden Golf makes clothes for municipal
golf, and it is specific about it."* → skate graphics and the Swingman mark
(Edgerton in three lines, not seven) → founder quote → *"the golfer who walks
nine after work, keeps a cheap towel clipped to the bag."*
Naming one thing it sells is not.

> **Before:** Sugarloaf Social Club sells a $1,400 MacKenzie sailcloth bag and a
> $14 paper fan and makes both feel like they belong to the same company.
> **After:** Sugarloaf Social Club runs the widest price range in independent golf
> and holds a single point of view across all of it. *(the bag and the fan move to
> sentence two)*

> **Before:** Blooming Grounds is the best-drawn thing Walker Golf Things have put
> out, a hand-illustrated course scene knitted into the body of the polo.
> **After:** Walker Golf Things draw everything by hand, and Blooming Grounds is the
> fullest expression of that they have put out.

> **Before:** Jones Sports Company has been making single-strap carry bags in
> Portland, Oregon since 1971, and the founding story is better than most because
> it is small.
> **After:** Jones makes the best carry bag in golf by leaving things off it — no
> legs, no cart strap, no panelling to break the surface — and has been doing that
> from Portland, Oregon since 1971.

> **Before:** Left of Field Golf is four years old and runs out of Sydney.
> **After:** Left of Field is the funniest brand in golf that also makes clothes
> you would wear without the joke attached.

> **Before:** The maker to start with works out of a unit on Broadhollow Road in
> Melville, New York.
> **After:** A ball marker is the cheapest thing in golf that can still be properly
> made, and the best of them come out of a unit on Broadhollow Road in Melville,
> New York.

Take the position. "The best carry bag in golf" and "the funniest brand in golf"
are opinions, and having one is the job. Make sure the rest of the post earns it.

## Section kickers

Same rules. A kicker sets up what the section contains and why those pieces belong
together. It is not a place to be clever about what we couldn't find.

## Facts

Everything factual still has to be true and sourced. Quotes remain verbatim-only
per the founder-quote rule. Voice work never invents a material, a price, a
provenance, or a founder's intent. If you don't know the fabric, describe what you
can see.
