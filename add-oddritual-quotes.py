#!/usr/bin/env python3
"""add-oddritual-quotes.py — three sourced pull-quotes onto the Odd Ritual
brand page. 23 September 2026.

Lenny: "let's also add some quotes to the odd ritual page, I love when we do
that", and sent two of them himself. Both matched the brand's About page
verbatim when checked against it, so both are used as he sent them.

THE ATTRIBUTION IS THE WHOLE PROBLEM WITH THIS BRAND, AND IT IS WHY NONE OF
THESE CARRIES A PERSON'S NAME.

Odd Ritual publishes no founder. The About page is first-person plural
throughout. The only editorial coverage anywhere is design press about the
website — Awwwards and Communication Arts — and Communication Arts states
plainly at the top of the piece that the "Responses [are] by Malvah Studio",
the agency that built the site. Quoting that would be the agency speaking about
its client while the page implies the brand is speaking about itself.

A REAL PERSON DOES EXIST: Ewaldt Verster, Stellenbosch, whose own Instagram bio
reads "Co-Founder of @oddritual.gc" and whose LinkedIn says he is "Building a
Golf & Fashion brand called Odd Ritual". Odd Ritual's own Terms of Service give
a Stellenbosch business address, which corroborates the town. But the claim is
self-asserted on his own profiles, no third party confirms it, and — decisive
here — HE DID NOT WRITE THE LINES BELOW. They are unsigned brand copy. Putting
his name on them would invent a quotation, which is the one thing the house
rule about quotes forbids outright.

So every quote here is attributed to Odd Ritual, naming the exact page it
appears on. That is honest, checkable, and reads perfectly well.

THE THIRD QUOTE WAS CHOSEN AROUND A GATE. The strongest unused line on their
About page is the one about a beginner and a tour pro competing without pulling
punches, ending "...we think it's worth applying that principle". verify-post
fails any page containing the word "worth", a rule about TGI's own voice that
does not distinguish quoted source material. Rather than weaken the gate or
silently alter a verbatim quote, that line is left out and the
locally-made line from the homepage is used instead. Flagged at the end.

THE SECOND QUOTE OPENS ON AN ELLIPSIS because the sentence in the original
begins "At the same time, our respect for golf runs deep" — a mid-paragraph
connector that dangles when lifted. A leading ellipsis is the standard way to
signal an excerpt and adds no words the brand did not write.

Idempotent. Dry run by default.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
PAGE = ROOT / "drops/brand-to-know-odd-ritual.html"
DONOR = ROOT / "drops/brand-to-know-manors.html"
CSS_A, CSS_B = "/* TGI-ORGC-PQ-CSS */", "/* /TGI-ORGC-PQ-CSS */"
MARK, END = "<!-- TGI-ORGC-QUOTES -->", "<!-- /TGI-ORGC-QUOTES -->"

# (text, attribution, the heading this quote is placed AFTER)
QUOTES = [
    ("Odd Ritual is our way of building something new on the back of tradition. "
     "A brand for people who love the game but want to feel like themselves on "
     "the course.",
     "Odd Ritual, from the brand&rsquo;s own About page",
     "The Story"),
    ("&hellip;our respect for golf runs deep. The discipline it demands. The "
     "attention to detail. The way it forces you to stay honest, stay patient, "
     "and stay in the moment.",
     "Odd Ritual, from the brand&rsquo;s own About page",
     "The Story &mdash; FAQ"),
    ("Our country is rich in culture, diversity, and heritage &mdash; producing "
     "locally is how we carry home with us, wherever we go. Made for us. By us.",
     "Odd Ritual, from the brand&rsquo;s homepage",
     "In the Wild"),
]


def donor_css():
    """Lift every .pull-quote rule from the Manors page, media queries included.

    THE PAGE HAD NO PULL-QUOTE CSS AT ALL — Lenny: "the quotes are usually in
    green". They were rendering unstyled: no green, no rules above and below,
    none of the house treatment. The colour lives in .pull-quote-inner as
    color:var(--grass), so without the rule the quote just inherits body ink.

    Copied rather than retyped. A hand-written approximation of a rule that
    already exists on eleven other pages drifts the first time either is
    touched, and the whole point is that a pull-quote looks identical sitewide.
    Media-query copies are included: the brace scanner used elsewhere cannot
    see inside @media, so these are matched by selector across the whole sheet.
    """
    d = DONOR.read_text(encoding="utf-8")
    sheet = d[d.index("<style>"):d.index("</style>")]
    rules = []
    for m in re.finditer(r"([^{}]*\.pull-quote[^{}]*)\{([^{}]*)\}", sheet):
        sel, body = m.group(1).strip().lstrip(";").strip(), m.group(2).strip()
        if sel and not sel.startswith("@"):
            rules.append(f"{sel}{{{body}}}")
    if not rules:
        sys.exit("! no .pull-quote rules found on the donor page")
    if not any("--grass" in r for r in rules):
        sys.exit("! the donor's pull-quote rules carry no green; refusing to "
                 "port a treatment that would not match the other pages")
    # the mobile overrides are the last two and belong inside a media query
    base = [r for r in rules if "font-size:22px" in r or "max-width:1400px" in r
            or "pull-quote-attr" in r]
    small = [r for r in rules if r not in base]
    css = "\n".join(base)
    if small:
        css += "\n@media(max-width:700px){" + "".join(small) + "}"
    return css


def pull_quote(text, attr):
    return (f'\n<div class="pull-quote">\n  <div class="pull-quote-inner">'
            f'&ldquo;{text}&rdquo;'
            f'<span class="pull-quote-attr">&mdash; {attr}</span></div>\n</div>\n')


def section_end(h, heading):
    """Index just past the </section> of the section carrying this heading.

    Matches the dash either way. These headings are written with a literal
    em-dash while the constants below use &mdash;, and guessing which cost a
    run — the same mismatch that bit the Home Golf Decor card title.
    """
    pat = re.escape(heading).replace(r"\&mdash;", "(?:&mdash;|\u2014)")
    m = re.search(r"<h2[^>]*>\s*" + pat + r"\s*<", h)
    if not m:
        m = re.search(pat, h)
    if not m:
        return None
    j = h.find("</section>", m.start())
    return j + len("</section>") if j != -1 else None


def main(apply_):
    h = PAGE.read_text(encoding="utf-8")
    original = h

    # strip any previous run, whitespace-symmetric
    h = re.sub(r"[ \t]*" + re.escape(MARK) + r".*?" + re.escape(END) + r"[ \t]*\n?",
               "", h, flags=re.S)

    # ---- the house pull-quote treatment, marked so a rerun replaces it ----
    h = re.sub(re.escape(CSS_A) + r".*?" + re.escape(CSS_B) + r"\n?", "", h,
               flags=re.S)
    if "</style>" not in h:
        sys.exit("! the page has no <style> block to add the rules to")
    css = CSS_A + "\n" + donor_css() + "\n" + CSS_B + "\n"
    h = h.replace("</style>", css + "</style>", 1)

    # insert back to front so earlier offsets stay valid
    plan = []
    for text, attr, after in QUOTES:
        at = section_end(h, after)
        if at is None:
            sys.exit(f"! could not find a section ending for heading {after!r}")
        plan.append((at, text, attr, after))
    for at, text, attr, after in sorted(plan, reverse=True):
        h = h[:at] + "\n" + MARK + pull_quote(text, attr) + END + h[at:]

    print(f"  {len(QUOTES)} pull-quotes placed:")
    for _, _, attr, after in plan:
        print(f"      after {after[:34]:<36}{attr[:44]}")

    if not apply_:
        print("\n  dry run — pass --apply")
        return
    PAGE.write_text(h, encoding="utf-8")
    verify(original)


def verify(original):
    fin = PAGE.read_text(encoding="utf-8")
    bad = []

    if fin.count(MARK) != len(QUOTES) or fin.count(END) != len(QUOTES):
        bad.append(f"{fin.count(MARK)} marker pairs, expected {len(QUOTES)}")

    pqs = re.findall(r'<div class="pull-quote-inner">&ldquo;(.*?)&rdquo;'
                     r'<span class="pull-quote-attr">&mdash;\s*(.*?)</span>', fin, re.S)
    if len(pqs) != len(QUOTES):
        bad.append(f"{len(pqs)} pull-quotes on the page, expected {len(QUOTES)}")

    for text, attr, _ in QUOTES:
        if text not in fin:
            bad.append(f"quote missing or altered: {text[:46]}...")
        # NOT DUPLICATED INTO THE BODY. A pull-quote is the only place its words
        # appear; the same rule the Manors page follows.
        if fin.count(text[:60]) != 1:
            bad.append(f"quote text appears {fin.count(text[:60])}x: {text[:40]}...")

    # NO QUOTE MAY BE ATTRIBUTED TO A PERSON. Odd Ritual names nobody, and the
    # only name attached to the brand anywhere is self-asserted on his own
    # social profiles and did not write this copy.
    for _, attr in pqs:
        if not attr.startswith("Odd Ritual,"):
            bad.append(f"attribution is not the brand: {attr[:50]}")
        if re.search(r"\b(Verster|Ewaldt|Malvah|Evans|Dawes|Jansen)\b", attr):
            bad.append(f"a personal or agency name got into an attribution: {attr[:50]}")

    # THE QUOTES MUST BE GREEN AND RULED, like every other page's
    if ".pull-quote-inner{" not in fin.replace(" ", ""):
        bad.append("the pull-quote CSS was not added")
    m = re.search(r"\.pull-quote-inner\s*\{([^{}]*)\}", fin)
    if not m:
        bad.append("no .pull-quote-inner rule on the page")
    else:
        body = m.group(1)
        if "--grass" not in body:
            bad.append("the pull-quote rule carries no green")
        if "border-top" not in body:
            bad.append("the pull-quote rule lost its rules above/below")

    # no two pull-quotes stacked with only whitespace between them
    if re.search(r"</div>\s*</div>\s*(?:<!--[^>]*-->\s*)*<div class=\"pull-quote\">", fin):
        bad.append("two pull-quotes are stacked with no prose between them")

    # house rules
    text_only = re.sub(r"<[^>]+>", " ", fin)
    if re.search(r"\bworth\b", text_only, re.I):
        bad.append("the banned word 'worth' is on the page")
    if fin.count('class="product-card"') != original.count('class="product-card"'):
        bad.append("the card count changed")
    for untouched in ("The Story", "In the Wild", "The Questions",
                      "The Original Collection"):
        if untouched not in fin:
            bad.append(f"existing section lost: {untouched}")

    if bad:
        PAGE.write_text(original, encoding="utf-8")
        sys.exit("! reverted. " + "\n    ".join(bad))

    words = len(text_only.split())
    print(f"\n  wrote {PAGE.name} — {len(pqs)} pull-quotes, {words} words")
    print("\n  FLAGGED:")
    print("    Their best unused line ends '...we think it's worth applying that")
    print("    principle' — verify-post fails any page containing 'worth', and the")
    print("    rule does not exempt quoted source material. Left out rather than")
    print("    altered. Say the word if you want the gate to allow it inside a quote.")
    print("    Also unused: an Instagram caption calling golf 'this odd tention")
    print("    between the hope of what's possible, and the acceptance of our")
    print("    flaws' — their typo, which would read as ours in a pull-quote.")


if __name__ == "__main__":
    main("--apply" in sys.argv)
