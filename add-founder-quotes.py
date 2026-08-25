#!/usr/bin/env python3
"""Insert verified founder pull-quotes into recent Brand to Know / Brand Revisited posts.

EVERY quote below was verified verbatim against a named source (2026-08-25 research).
Do NOT edit the QUOTE strings without re-checking the source — these are printed as
direct quotations. Never paraphrase into quotation marks.

Brands deliberately WITHOUT a quote (no verifiable founder statement exists):
  midiron          - no founder named publicly anywhere; site copy is unattributed "we"
  twentyfour-golf  - founder anonymous; About page is unsigned first-person brand copy
  fella-golf       - real sourced founder quotes exist but are Dutch-only (Golf.nl,
                     Oct 2025); running them needs a translation decision from Lenny

Placement: before the Nth section heading, i.e. between product sections.
"""
import re, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))

CSS = ("\n.pull-quote{max-width:1400px;margin:0 auto;padding:0 32px}"
       "\n.pull-quote-inner{font-family:var(--serif);font-style:italic;font-size:22px;line-height:1.4;"
       "padding:32px 0;margin:0;border-top:.5px solid rgba(20,20,20,.15);"
       "border-bottom:.5px solid rgba(20,20,20,.15);color:var(--grass)}"
       "\n.pull-quote-attr{font-family:var(--mono);font-style:normal;font-size:10px;letter-spacing:.14em;"
       "text-transform:uppercase;color:var(--ink);opacity:.45;margin-top:12px;display:block}"
       "\n@media(max-width:640px){.pull-quote{padding:0 20px}.pull-quote-inner{font-size:18px;padding:24px 0}}\n")

# slug -> (quote, attribution, heading index to insert before [1-based])
QUOTES = {
 "brand-to-know-seamus": (
   "Each evolution has been the result of meeting an artisan, maker, or designer that we are inspired to work with.",
   "Akbar Chisti, Seamus Golf co-founder", 2),

 "brand-to-know-criquet": (
   "Hobson and I always loved the vintage, classic golf shirt that Jack, Arnie, and Seve used to wear back in the day.",
   "Billy Nachman, Criquet co-founder", 2),

 "brand-to-know-gramicci": (
   "For me, building clothing is like architecture and engineering. And those were the ideas I put into Gramicci, to make things function in a better way.",
   "Mike Graham, Gramicci founder", 2),

 "brand-to-know-devereux-golf": (
   "Family values and ideals are paramount in everything we do, including our business, so naming it after her is a nod to what we&rsquo;re all about.",
   "Robert Brunner, Devereux co-founder", 2),

 "brand-to-know-left-of-field-golf": (
   "When I first started playing the game, getting dressed for golf felt like a lose-lose situation.",
   "Nick Ilias, Left of Field Golf founder", 3),

 "brand-to-know-sugarloaf-social-club": (
   "All I&rsquo;ve ever wanted to do is make cool stuff with my friends.",
   "Ian Gilley, Sugarloaf Social Club founder", 2),

 "brand-to-know-takomo-golf": (
   "We are not looking to sponsor any tour players because I believe we need to be present where our actual audience is and that&rsquo;s on the Internet.",
   "Sebastian Haapahovi, Takomo Golf founder", 2),

 "brand-to-know-quiet-golf": (
   "Some people go on runs, others go rock climbing or mountain biking. But for us golf is a way to get outside, get away from your phone and have some quiet time for yourself.",
   "Christion Lennon, Quiet Golf co-founder", 2),

 "brand-to-know-huega-house": (
   "We are passionate about the vintage aesthetics of our hats, drawing significant inspiration from classic racing and sports logos.",
   "Jonathan Ruley, Huega House co-founder", 2),

 # NOTE: George Jones, the 1971 founder, is never quoted directly in any source —
 # every account of him is third-person. This is the current owner/creative director.
 "brand-revisited-jones-sports-co": (
   "We didn&rsquo;t want the bags to be a billboard. The logo is small and the quality of the product is what speaks.",
   "Chris Carnahan, Jones Sports Co partner and creative director", 3),
}

def block(quote, attr):
    return (f'\n<div class="pull-quote">\n'
            f'  <div class="pull-quote-inner">&ldquo;{quote}&rdquo;'
            f'<span class="pull-quote-attr">&mdash; {attr}</span></div>\n'
            f'</div>\n')

def main():
    done, skipped = [], []
    for slug, (quote, attr, nth) in QUOTES.items():
        p = os.path.join(ROOT, "drops", slug + ".html")
        if not os.path.exists(p):
            skipped.append((slug, "file missing")); continue
        h = open(p, encoding="utf-8").read()
        if 'class="pull-quote"' in h:
            skipped.append((slug, "already has a pull-quote")); continue

        # 1. inject CSS before the last </style> in the document head
        if ".pull-quote-inner{" not in h:
            i = h.find("</style>")
            assert i > 0, slug
            h = h[:i] + CSS + h[i:]

        # 2. find section headings — newer posts use <h2 id=>, older use <h2 class="products-hdr">
        # note: some posts use class="products-hdr sec", so don't require the closing quote
        heads = [m.start() for m in re.finditer(r'<h2 (?:id=|class="products-hdr)', h)]
        if len(heads) < nth:
            skipped.append((slug, f"only {len(heads)} headings, wanted #{nth}")); continue
        pos = heads[nth - 1]
        h = h[:pos] + block(quote, attr) + h[pos:]

        open(p, "w", encoding="utf-8").write(h)
        done.append((slug, attr))

    print(f"added {len(done)} founder quotes")
    for s, a in done: print(f"   + {s:36} {a}")
    if skipped:
        print(f"skipped {len(skipped)}:")
        for s, why in skipped: print(f"   - {s:36} {why}")

if __name__ == "__main__":
    main()
