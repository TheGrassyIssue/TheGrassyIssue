#!/usr/bin/env python3
"""fix-manors-faq-schema.py — get the Manors FAQ structured data telling the
truth. 22 September 2026.

TWO FAULTS, ONE OF THEM OLDER THAN THIS WEEK'S WORK.

1. A SECOND FAQPage BLOCK ON THE PAGE CARRIES KINGFISHER'S QUESTIONS. Four of
   them — "What is Kingfisher Golf?", "Who founded Kingfisher Golf?", "What does
   Kingfisher Golf sell?", "What is the Worst Golfer in Dallas contest?" — none
   of which appears anywhere in the visible Manors page. This is at HEAD, so it
   predates the September refresh; it is a template leak from whichever build
   last copied a brand page. Two FAQPage blocks on one URL is invalid on its
   own, and schema whose answers are not on the page is the specific thing
   Google demotes rich results for. The block is removed, not rewritten.

2. THE THREE NEW FAQs WERE VISIBLE BUT NOT IN THE SCHEMA. The refresh added
   Greenskeeper, September-drop and pricing questions to the page. Schema that
   omits them is not wrong, only wasteful — these are the three most likely to
   win an answer box, since they are the only ones carrying 2026 prices.

QUESTIONS ARE READ OFF THE RENDERED PAGE, NOT RETYPED. The script parses the
<details><summary> pairs and rebuilds mainEntity from them, so the schema cannot
drift from the copy again. Retyping is how the two got out of step.

The same double-FAQPage pattern is on drops/brand-to-know-twentyfour-golf.html,
where both blocks are at least about TwentyFour and both sets of answers are
visible. That is a merge rather than a deletion and a different page than the
one Lenny asked for, so it is FLAGGED AT THE END, not touched here.

Idempotent. Dry run by default.
"""
import html as htmllib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
PAGE = ROOT / "drops/brand-to-know-manors.html"
ALIEN = "Kingfisher"


def visible_faqs(h):
    """[(question, answer)] straight off the rendered <details> blocks."""
    out = []
    for m in re.finditer(r"<details[^>]*class=\"faq-q\"[^>]*>\s*<summary>(.*?)</summary>"
                         r"\s*<p>(.*?)</p>\s*</details>", h, re.S):
        q, a = (re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", x)).strip()
                for x in m.groups())
        out.append((htmllib.unescape(q), htmllib.unescape(a)))
    return out


def blocks(h):
    return [(m.start(), m.end(), m.group(1)) for m in
            re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)]


def main(apply_):
    h = PAGE.read_text(encoding="utf-8")
    original = h
    vis = visible_faqs(h)
    print(f"  visible FAQs on the page : {len(vis)}")

    faq_spans = []
    for s, e, raw in blocks(h):
        try:
            d = json.loads(raw)
        except json.JSONDecodeError:
            sys.exit(f"! a JSON-LD block at offset {s} does not parse")
        if isinstance(d, dict) and d.get("@type") == "FAQPage":
            faq_spans.append((s, e, d))
    print(f"  FAQPage blocks           : {len(faq_spans)}")
    for s, e, d in faq_spans:
        names = [q["name"] for q in d.get("mainEntity", [])]
        alien = sum(ALIEN.lower() in n.lower() for n in names)
        print(f"      offset {s:<7}{len(names)} questions"
              + (f"   <-- {alien} mention {ALIEN}" if alien else ""))

    # ---- drop any FAQPage block whose questions are not on this page ----
    vis_q = {q for q, _ in vis}
    keep = []
    for s, e, d in faq_spans:
        names = [q["name"] for q in d.get("mainEntity", [])]
        if not names or not any(n in vis_q for n in names):
            print(f"  REMOVING the block at offset {s} — none of its "
                  f"{len(names)} questions is on the page")
            continue
        keep.append((s, e, d))
    if len(keep) != 1:
        sys.exit(f"! expected exactly 1 FAQPage block to keep, got {len(keep)}")

    # ---- rebuild the survivor from the visible copy ----
    ks, ke, _ = keep[0]
    rebuilt = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in vis],
    }, indent=2, ensure_ascii=False)
    new_block = f'<script type="application/ld+json">\n{rebuilt}\n</script>'

    # rewrite back-to-front so earlier offsets stay valid
    edits = sorted([(ks, ke, new_block)]
                   + [(s, e, None) for s, e, d in faq_spans if (s, e) != (ks, ke)],
                   reverse=True)
    for s, e, repl in edits:
        if repl is None:
            lead = h.rfind("\n", 0, s)
            h = h[:lead if lead != -1 else s] + h[e:]
        else:
            h = h[:s] + repl + h[e:]

    print(f"  schema questions         : {len(vis)} (was "
          f"{len(keep[0][2].get('mainEntity', []))})")
    if not apply_:
        print("\n  dry run — pass --apply")
        return
    PAGE.write_text(h, encoding="utf-8")

    # ---- VERIFY THE FILE ON DISK ----
    fin = PAGE.read_text(encoding="utf-8")
    bad = []
    faqs = [d for _, _, raw in blocks(fin)
            for d in [json.loads(raw)]
            if isinstance(d, dict) and d.get("@type") == "FAQPage"]
    if len(faqs) != 1:
        bad.append(f"{len(faqs)} FAQPage blocks survive, expected 1")
    else:
        names = [q["name"] for q in faqs[0]["mainEntity"]]
        answers = [q["acceptedAnswer"]["text"] for q in faqs[0]["mainEntity"]]
        v = visible_faqs(fin)
        if [q for q, _ in v] != names:
            bad.append("schema questions do not match the visible ones in order")
        if [a for _, a in v] != answers:
            bad.append("schema answers do not match the visible ones")
        if any(ALIEN.lower() in n.lower() for n in names):
            bad.append(f"a {ALIEN} question survived in the Manors schema")
    for _, _, raw in blocks(fin):
        try:
            json.loads(raw)
        except json.JSONDecodeError as e:
            bad.append(f"a JSON-LD block stopped parsing: {e}")
    # nothing else may have moved
    if fin.count('class="product-card"') != original.count('class="product-card"'):
        bad.append("the card count changed")
    if fin.count('class="faq-q"') != original.count('class="faq-q"'):
        bad.append("the visible FAQ count changed")
    if bad:
        PAGE.write_text(original, encoding="utf-8")
        sys.exit("! reverted. " + "\n    ".join(bad))

    print(f"\n  wrote {PAGE.name} — 1 FAQPage block, {len(vis)} questions, "
          f"each one matching the visible copy verbatim")
    print("\n  FLAGGED, NOT FIXED:")
    print("    drops/brand-to-know-twentyfour-golf.html also carries two FAQPage")
    print("    blocks (6 + 6). Both are about TwentyFour and both sets of answers")
    print("    are on the page, so it wants merging rather than deleting — a")
    print("    different page than the one this session was asked for.")


if __name__ == "__main__":
    main("--apply" in sys.argv)
