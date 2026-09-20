# The Brand to Know spine — agreed 20 September 2026

Agreed with Lenny in session. This is the canonical order and the canonical
names. `btk-template.py` enforces the **furniture**; everything marked
*bespoke* stays the writer's call and the template must not touch it.

Lenny's framing: *"all the different brand to know pages are all a little
different. I want them more cohesive."* The audit found the pages are mostly
already consistent — 36/46 already carry a correctly-named TGI Take. The
incoherence is concentrated in nine legacy pages, one page built outside the
template (AXXA), and one heading that drifted everywhere (the FAQ).

---

## The spine, in order

| # | Block | Name | Fixed? | Present at audit |
|---|-------|------|--------|------------------|
| 1 | Hero image | — | — | 45/46 |
| 2 | The TGI Take | **"The TGI Take"** | **fixed** | 36/46 |
| 3 | Opening write-up | **"The Story"** | **fixed** | 37/46 |
| 4 | Prose sections | *bespoke* | free | varies |
| 5 | Lookbook band | **"In the Wild"** | **fixed** | 37/46 |
| 6 | Product sections | *bespoke* | free | varies |
| 7 | FAQ | **"The Questions"** | **fixed** | 43/46, ~18 names |
| 8 | More from TGI | — | — | 46/46 |

### 2 — The TGI Take
Reference implementation: `brand-to-know-hiroki-golf`. A `.drop-tag` chip
reading "The TGI Take", then two paragraphs, inside `.writeup-body` in
`section[data-btk="take"]`, with the Details `.sidebar` beside it. Sits
**above** the Details card and **before** The Story.

Lenny's definition: *"a simple blurb about the brand, who it's for, the ethos,
ideas behind it and what we think of the product as a whole."* So it covers:
what the brand is → what's distinctive → the signature piece → **who it's
for** → a price entry point.

This is the one place on a BTK page where TGI states a view. It characterises
the brand being featured; it does not rank it against others and does not
explain how it got picked — see `feedback_never_talk_down`.

`section[data-btk="take"]` is a two-column grid. It must contain **exactly two
direct children** (`.writeup-body` and `.sidebar`) — any third child is
auto-placed into the sidebar column. See the AXXA note in `build-axxa.py`.

### 5 — In the Wild
The lookbook band. Name is fixed even where the band's content is
brand-specific; the heading is doing navigational work, not editorial work.

### 7 — The Questions
Was called ~18 different things, including "Frequently Asked", "The Story —
FAQ", and title-prefixed forms like "Brand to Know — BEAMS Golf — FAQ". Now
one name. Always the last section before More from TGI.

---

## Rhythm rule

No two sections may run into each other with nothing between them.

A **product grid counts as imagery** (agreed — a 3-up grid is already a wall of
pictures). So the rule bites only where prose runs into prose with neither a
lookbook band, a pull-quote, nor a grid between.

At audit: **75 of 302 transitions (25%)** were bare under this reading. Under
the stricter reading — band or pull-quote specifically — 276 of 302 failed,
which is not achievable honestly: at least 14 brands have no sourceable
founder quote on record (`reference_founder_quotes`), so the fallback has to
be imagery.

Note the reference page is only half a reference: `birds-of-condor` runs
pull-quotes between its first four prose sections, then has seven sections in
a row with no break at all.

## Typography

Headings and standfirst **centred**; body copy **left**, 760px measure.
Already the behaviour of `section[data-btk]` — `.products-hdr` and
`.cat-kicker` centre, `.writeup-body` stays left.

Exception: `section[data-btk="take"]` keeps its heading left, because it is a
two-column layout and a centred heading over a 1fr/300px grid centres on the
wrong axis.

Pull-quotes are **roman, 38px**, never italic — see
`reference_founder_quotes` for why this has now come up twice.

---

## Work outstanding against this spec

1. **FAQ rename** → `btk-template.py` owns the name; one `--all` pass.
2. **Lookbook rename** → same pass.
3. **The TGI Take** → 10 pages need one written: the 9 legacy pages + AXXA.
   This is copy, not markup — it cannot be generated.
4. **Rhythm** → 75 bare transitions need imagery sourced.
5. **Legacy conversion** → 7 pages (Aug 11, BEAMS, Found Golf, J.Lindeberg,
   Morning People, Olydoe, Fella). Each needs a spec in `research/btk/`.
   Skipped by agreement: `brand-to-watch-kingfisher-golf` (duplicates the
   brand-to-know page) and `muni-kids-10-years` (holstered).

## Two traps worth remembering

`btk-template.py` is a **post-processor**, like `apply-affiliates.py`. A
per-brand `build-*.py` re-run reintroduces that brand's old headings, so the
template pass has to run after any rebuild, and a guard should fail loudly on
a non-canonical furniture heading.

`--all` is driven by the 37 specs in `research/btk/`, which are **not** the
same 37 pages the audit found to be template-era — AXXA is template-era with
no spec. Reconcile the two lists before trusting a pass to have covered
everything.
