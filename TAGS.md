# TGI Taste Tags

Set 2026-08-27. These are the classification layer for the Brand Index — the part
that isn't a category filter. `apparel` describes what a brand sells; a taste tag
describes what it *is*. Every tag becomes its own page at `/brands/tag/<slug>`,
which is the linkable, rankable asset. The directory itself is not.

## Rules

1. **Every tag needs written criteria**, printed on its own page. A tag a reader
   can't apply themselves is decoration, not classification.
2. **A brand carries 1–3 tags.** Nothing gets all of them; anything with none
   either doesn't belong in the index or we don't know it well enough yet.
3. **Tags describe the brand, not one product.** If only one item fits, it isn't a
   tag, it's a card.
4. **Tags are not quality.** "Loud on purpose" is not worse than "Quiet luxury".
   There is no ranking here, and no scores anywhere — see the facts strip instead.
5. **Never invent a new tag to fit an awkward brand.** Leave it under-tagged and
   flag it. The list only stays meaningful if it stays short.

## The tags

### Muni energy
Gear made for public golf. Unpretentious, priced so a weekly player can buy it,
often tied to a specific course or local cause.
**Criteria:** core apparel under about $120, *or* an explicit public-course or
community affiliation. No country-club signalling.

### Design nerd
The reason to buy is a design decision, not a logo. These brands publish their
reasoning.
**Criteria:** the brand explains construction or design rationale on its own
product pages, *and* the work would read as considered to someone outside golf.

### Quiet luxury
Expensive and undecorated.
**Criteria:** core piece above about $150, branding limited to a woven label or a
small mark, premium natural or technical materials.

### Loud on purpose
Print, colour and graphics are the product, not a finish applied to it.
**Criteria:** all-over prints, bold colourways, or graphics as the primary design
element across the range rather than on one capsule.

### Dad golf
Deliberately traditional, and not ironic about it.
**Criteria:** references pre-1990 golf clothing — four-button plackets, pleats,
natural fibres, fuller cuts. No athleisure silhouettes.

### Gorpcore
Outdoor and technical crossover.
**Criteria:** technical shells, ripstop, utility hardware, or a genuine hiking,
climbing or workwear lineage.

### Post-round friendly
Reads as normal clothes the moment you leave the course.
**Criteria:** no visible golf branding on the core range, and silhouettes that
work in a bar without explanation.

### Made by hand
Small-batch or hand-finished by a named person.
**Criteria:** hand-cut, hand-sewn, hand-knit, hand-stamped or made to order, by a
maker the brand will name.

### Collab machine
The brand's identity is built on partnerships rather than on its own line.
**Criteria:** collaborations make up a substantial share of the catalogue, or the
brand is better known for who it works with than for what it makes alone.

### Course merch
Tied to a specific course or club &mdash; real or invented.
**Criteria:** the range references a named course, club or municipal facility, or
the brand exists to sell an invented club's merchandise.

### Member-guest
The dressed-up end. What you wear when the round matters.
**Criteria:** the range is cut for an occasion rather than a practice session
&mdash; collared, tailored, coordinated. Distinct from Quiet luxury, which is
about restraint and price rather than occasion.

### Range rat
Built for practice and repetition rather than for the photograph.
**Criteria:** hard-wearing, technical or deliberately cheap, and sold on
durability or function rather than on how it looks in a lookbook.

## Attributes

Separate from taste tags, and rendered in their own row. **Attributes are facts,
not judgements** &mdash; they are checkable, they need no editorial defence, and
they are the raw material for the comparison layer ("bags under $300",
"like Seamus but women-founded"). Never mix them into the taste row.

A brand can carry any number of attributes, including none.

### Women-founded
Founded or co-founded by a woman.
**Criteria:** a named woman is credited as founder or co-founder by the brand or
by a published source. Verified list lives in the founder-quotes research.

### Tour-proven
Genuine use in professional competition.
**Criteria:** a named player used the product in a named event, or the brand
publishes a verifiable tour record. Sponsorship alone does not count.

### Heritage
Founded before 2000.
**Criteria:** a founding year earlier than 2000, stated by the brand.

### Drops and vanishes
Sells in short runs and does not reliably restock.
**Criteria:** the brand states a limited-run or periodic-release model, or its
catalogue is mostly sold out at any given time.

### New to the index
Added to the Brand Index in the last 90 days.
**Criteria:** computed from the `added` date in `data/brands.json`. Not editorial
&mdash; do not hand-assign it.

## Applying them

`data/brands.json` gains a `tags` array and an `attrs` array, plus an `added`
date stamped when a brand first enters the index. `build-brands.py` reads it, renders the
chips on each brand card, and generates one page per tag. A brand with an empty
`tags` array renders without chips and is listed on the index as not yet
classified — which is honest, and better than a wrong tag.
