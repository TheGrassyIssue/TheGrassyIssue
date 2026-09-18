#!/usr/bin/env python3
"""
fix-merrill-faq.py — bring the Merrill FAQ back in line with the facts.
18 September 2026.

WHY
---
btk-template.py deliberately passes the FAQ through untouched: it is
schema-backed, and a reorderer has no business rewriting answers. Correct — but
it means a Brand Revisited can refresh the whole page and leave the FAQ saying
things that stopped being true.

Three of Merrill's four answers were false as of today:
  · "It makes no polos and no moisture-wicking polyester"  -> the Birds Stripe
    Polo is live at $65.
  · "A tight catalogue including the Target Practice Tee at $60 ..."  -> that
    tee is sold out, and the catalogue is ~40 pieces in stock.
  · "Does Merrill Golf make polos?  No."  -> the worst one. This is FAQPage
    schema; Google can surface it as the answer. Shipping it would be handing a
    search engine a confident wrong answer about a brand we cover.

THE HARD PART is that each Q&A exists THREE times on the page, and they must
agree or the structured data contradicts the visible text:
  1. the JSON-LD FAQPage block  (what Google reads)
  2. a styled prose section     (what a reader skims)
  3. the <details> accordion    (what a reader opens)
This script replaces all three from one source of truth below.

Idempotent: matches on the OLD answer text, so a second run finds nothing.
"""
import pathlib, re, sys, json

ROOT = pathlib.Path(__file__).resolve().parent
PAGE = ROOT / "drops/brand-to-know-merrill-golf.html"

# question -> new answer. Every figure read off merrillgolf.com, 18 Sept 2026.
NEW = {
 "What is Merrill Golf?":
   "A golf brand that describes itself as &ldquo;a design venture that aims to "
   "create timeless products through the lens of golf.&rdquo; The range runs "
   "from screen-printed heavyweight tees to mohair cardigans, canvas work "
   "jackets and headcovers handmade in Japan, under a flying-mallard mark drawn "
   "from vintage Americana.",
 "Who is Merrill Golf for?":
   "Golfers who also fish and hunt, and who want to wear the same thing after "
   "the round. The aesthetic reads closer to a tackle shop than a fairway.",
 "What does Merrill Golf sell?":
   "Around forty pieces in stock at a time, from $25 to $160 &mdash; tees, hats "
   "and fleece alongside the Birds Stripe Polo at $65, the Palmer Cardigan at "
   "$160, Baggy Trousers at $125, and headcovers and putter covers at $110 and "
   "$120. Prices read September 2026.",
 "Does Merrill Golf make polos?":
   "Yes, now. The brand went years without one, and we noted its absence when we "
   "first covered it &mdash; but the Birds Stripe Polo is live at $65 in a "
   "custom-dyed cotton jersey, with the Heavy Knit and Rugby polos in the "
   "archive behind it.",
}

# what each answer is replacing, matched loosely on a distinctive fragment
OLD_FRAGMENT = {
 "What is Merrill Golf?":        "It makes no polos and no moisture-wicking",
 "Who is Merrill Golf for?":     "that audience has turned out larger",
 "What does Merrill Golf sell?": "A tight catalogue including the Target Practice Tee",
 "Does Merrill Golf make polos?":"That is a deliberate position rather than a gap",
}


def strip_entities(s):
    """JSON-LD carries plain text, not HTML entities."""
    return (s.replace("&ldquo;", '\\"').replace("&rdquo;", '\\"')
             .replace("&mdash;", "—").replace("&amp;", "&"))


def run(apply_):
    html = PAGE.read_text(encoding="utf-8")
    orig, hits = html, []

    # ALREADY-APPLIED IS NOT A FAILURE. The replacement guard below wants each
    # answer found in >=2 places; on a second run the old fragments are gone, so
    # every count is 0 and the script would "fail" on a page that is already
    # correct. Distinguish the two states up front: no old fragments anywhere,
    # and the new answers present, means the work is done.
    if (not any(f in html for f in OLD_FRAGMENT.values())
            and all(n.split("&mdash;")[0][:40] in html for n in NEW.values())):
        print("  no change — already applied")
        return

    for q, new in NEW.items():
        frag = OLD_FRAGMENT[q]
        # every answer paragraph/segment that contains the old fragment
        n = 0
        # 1. JSON-LD  "text": "....<frag>...."
        def jsonld(m):
            nonlocal n
            if frag in m.group(1):
                n += 1
                return '"text": "' + strip_entities(new) + '"'
            return m.group(0)
        html = re.sub(r'"text"\s*:\s*"([^"]*)"', jsonld, html)

        # 2 + 3. any HTML element whose text carries the fragment
        def htmlblk(m):
            nonlocal n
            if frag in m.group(2):
                n += 1
                return m.group(1) + new + m.group(3)
            return m.group(0)
        html = re.sub(r'(<(?:p|div)[^>]*>)([^<]*?)(</(?:p|div)>)', htmlblk, html, flags=re.S)

        hits.append((q, n))

    # ---- guards ----
    ok = True
    for q, n in hits:
        good = n >= 2                      # schema + at least one rendering
        ok &= good
        print(f"  {'OK  ' if good else 'FAIL'} {q:<32} replaced in {n} place(s)")

    checks = [
      ("no stale 'no polos' answer survives",
       "makes no polos" not in html and "deliberate position rather than a gap" not in html),
      ("no sold-out tee quoted as current",
       "Target Practice Tee at $60" not in html),
      ("schema still parses",
       all(_try_json(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',
                                            html, re.S))),
      ("document still closes", html.rstrip().endswith("</html>")),
    ]
    for label, passed in checks:
        ok &= passed
        print(f"  {'OK  ' if passed else 'FAIL'} {label}")

    if not ok:
        sys.exit("\n! refusing to write")
    if html == orig:
        print("\n  no change — already applied"); return
    if apply_:
        PAGE.write_text(html, encoding="utf-8"); print("\n  written")
    else:
        print("\n  dry run — pass --apply")


def _try_json(b):
    try:
        json.loads(b); return True
    except Exception as e:
        print(f"     JSON-LD parse error: {e}"); return False


if __name__ == "__main__":
    run("--apply" in sys.argv)
