# TGI Write-Up Style — Killing the AI Tells

Diagnosed 12 Aug 2026 by counting patterns across the five most recent posts. The tells below are mine, not hypothetical — the counts are real.

## What's actually wrong

| Tell | Where it's worst | Count |
|---|---|---|
| Em dash mid-sentence | Walker Golf | 11 in cards + 6 in writeup |
| Triple adjective lists ("breathable, moisture-wicking, temperature-regulating") | everywhere | 3–4 per page |
| "genuinely / actually / quietly" | Hydration, No Budget | 2.5–2.8 per 1k words |
| "which is" appositive | Hydration | 4 |
| "more than it sounds / than you'd think" | Hydration | 5 |
| Punchy fragment closer ("That's the point.") | Walker | 2 |
| The "X that says Y" / "X for people who Z" formula | all product cards | pervasive |
| Every card the same length and shape | all | structural |

The single loudest one is the em dash. It's the reason the copy reads machine-made even when the facts are good.

## Rules

1. **Two em dashes per page, maximum.** The "Product Name — Colorway" card convention doesn't count; that's a house format. Everything else becomes a period, a comma, or gets restructured. Most of the time the clause after the dash should just be its own sentence.

2. **No adjective triads.** "Breathable, moisture-wicking, temperature-regulating" is spec-sheet noise. Pick the one that matters or describe what it does: "light enough that you stop noticing it around the third hole."

3. **Ban list:** genuinely, actually, quietly, seamlessly, elevated, curated, effortless, thoughtful, "the perfect X," "a masterclass in," "does the heavy lifting," "at its best," "no notes."

4. **Cut the last sentence.** Nine times out of ten the final line explains the significance of what was already said. "That's the point." "And this fleece proves it." "Which matters more than it sounds." Delete them. Trust the reader.

5. **Kill the formula.** "The polo that says you came to play but you're not wearing a uniform" is a construction, not an observation. Replace with something physical and checkable: how it fits, what it does at hour four, what it looks like next to the thing you already own.

6. **Vary the length.** Some cards get one line. Some get five. Right now they're all four sentences and it reads like a template, because it is one.

7. **One opinion per card, stated plainly.** "Best-looking thing Walker makes right now" is better than three sentences circling the same claim.

8. **Specifics over adjectives.** A number, a material, a place, a comparison. "Heavy cream rugby collar" beats "premium detailing" every time.

---

## Before / after — real examples from the Walker page

**Before**
> Knockout V Polo — The newest addition. V-neck knit collar in Maple, ultra-lightweight Par-Tec fabric engineered for movement. Breathable, moisture-wicking, temperature-regulating. The polo that says you came to play but you're not wearing a uniform. Walker makes things for the course and the pub, and this one works at both. $120.

**After**
> Knockout V Polo — Maple. The knit V-collar is the whole thing here. It sits flatter than a normal placket and doesn't gap when you lean over a putt. Par-Tec fabric, so it's light and it moves. $120.

---

**Before**
> Members Polo — Sandstone colorway, custom contrast knit collar, 3-button placket. Ultra-lightweight body with the embroidered Kooka patch that's become Walker's signature. The fabric disappears on you — you forget you're wearing a performance polo. That's the point. $100.

**After**
> Members Polo — Sandstone. Contrast knit collar, three-button placket, Kooka patch at the chest. The body fabric is light enough that you stop noticing it around the third hole. $100.

---

**Before**
> Featherlite Kooka Polo — Forest and Gold. The lightest polo in the Par-Tec lineup. Optimal stretch, maximum breathability, minimal weight. The contrast collar adds just enough personality to keep it from being boring. An Australian brand that understands that golf in the heat requires fabric that actually works. $100.

**After**
> Featherlite Kooka Polo — Forest and Gold. The lightest thing Walker makes. Built for August, and the gold collar keeps it from reading as a plain green polo. $100.

---

**Before**
> The single best-looking thing Walker makes right now. A tonal chevron knit in deep forest with a heavy cream rugby collar and a three-button placket — the collar does all the work, giving the whole thing a weight and structure most golf knits don't have. Wears like a sweater, plays like a polo, and looks completely at home in a pub afterward.

**After**
> Best-looking thing Walker makes right now. Tonal chevron knit in deep forest under a heavy cream rugby collar. Most golf knits go floppy at the neck; this one holds its shape. Wears more like a sweater than a polo.

---

## Check before publishing

Run this on any new page:

```
grep -o '&mdash;\|—' FILE | wc -l          # target: under 5 including card headers
grep -ioE '\b(genuinely|actually|quietly|curated|elevated|seamless)\b' FILE
grep -oE "[Tt]hat'?s the (point|whole|difference)" FILE
```

If the em dash count is over 10, the page reads like a machine wrote it regardless of how good the facts are.
