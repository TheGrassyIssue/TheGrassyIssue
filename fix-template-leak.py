#!/usr/bin/env python3
"""
fix-template-leak.py — repair posts that kept the TEMPLATE's identity.

THE BUG (found 2026-08-29 when Lenny asked "what's the write up for Forden golf?")
----------------------------------------------------------------------------------
House posts are built by copying `drops/the-niche-grip-report.html` and replacing
the head, hero, write-up and product sections. Several fields were never in the
replace list, so they silently kept the GRIP REPORT's content:

    * the visible FAQ block          -> five questions about golf grips
    * <meta name="twitter:title">    -> "The Niche Grip Report"
    * Article schema "description"   -> "Five independent golf grip makers..."
    * Article schema mainEntityOfPage-> /drops/the-niche-grip-report

Forden additionally kept two whole product sections (The Printed Ones, The Putter
Specialists) and five grip product cards - about 9.5kB of another post's body.

Why nothing caught it: `verify-post.py` checks structure (classes, grids, counts,
word count) and `voice-lint.py` checks prose style. Neither compares a page's
content against its own identity, so a structurally perfect page about the wrong
subject passes both. The FAQ *schema* in the head was correct on every affected
page, which is the tell - the generator wrote fresh JSON-LD but never re-rendered
the visible <details> list from it.

Affected: brand-to-know-forden-golf, brand-to-know-jlindeberg, the-bird-edit,
the-mackenzie-collab-edit-6-bags-you-cant-buy-on-their-site. The last three were
already deployed.

THE FIX
-------
For every post, make these four fields agree with the page's own identity:
  visible FAQ  <- the page's own FAQPage schema (already correct everywhere)
  twitter:title<- og:title
  Article description <- <meta name="description">
  mainEntityOfPage    <- canonical
Idempotent: a second run reports 0 changes. Body-section leaks are NOT auto-cut -
that needs a human to look, and only Forden had one.
"""
import os, re, glob, json, sys, html

ROOT = os.path.dirname(os.path.abspath(__file__))


def head_of(s):
    return s[:s.find("</head>")]


def other_titles(paths):
    """slug -> its own h1, so we can tell a LEAK from a harmless wording difference.

    Comparing og:title to twitter:title flags 130 pages, nearly all benign (one
    carries the ' - The Grassy Issue' suffix, the other doesn't). A real leak is
    narrower and unambiguous: the field holds *another post's* title verbatim.
    """
    out = {}
    for p in paths:
        s = open(p, encoding="utf-8").read()
        m = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        if m:
            t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()
            out[os.path.basename(p)[:-5]] = t
    return out


def norm(x):
    return re.sub(r"\s+", " ", re.sub(r"&[a-z]+;", "-", x or "")).strip().lower()


def fix(path, apply_, titles):
    s = open(path, encoding="utf-8").read()
    orig, notes = s, []
    head = head_of(s)
    me = os.path.basename(path)[:-5]
    foreign = {norm(t) for sl, t in titles.items() if sl != me}

    def meta(pat):
        m = re.search(pat, head)
        return m.group(1) if m else None

    ogt = meta(r'<meta property="og:title" content="([^"]*)"')
    desc = meta(r'<meta name="description" content="([^"]*)"')
    can = meta(r'<link rel="canonical" href="([^"]*)"')

    # 1. twitter:title must match og:title
    tw = meta(r'<meta name="twitter:title" content="([^"]*)"')
    # only a LEAK if it holds another post's title verbatim
    if ogt and tw and tw != ogt and norm(tw) in foreign:
        s = s.replace(f'<meta name="twitter:title" content="{tw}"',
                      f'<meta name="twitter:title" content="{ogt}"', 1)
        notes.append(f"twitter:title {tw!r} -> og:title")

    # 1b. twitter:description - same leak, separate tag. Found only after fixing
    #     twitter:title, because the grep for grip words kept coming back non-zero.
    twd = meta(r'<meta name="twitter:description" content="([^"]*)"')
    if desc and twd and twd != desc and twd.startswith("Five independent golf grip makers"):
        s = s.replace(f'<meta name="twitter:description" content="{twd}"',
                      f'<meta name="twitter:description" content="{desc}"', 1)
        notes.append("twitter:description -> meta description")

    # 2 & 3. Article schema description + mainEntityOfPage
    for m in list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)):
        try:
            d = json.loads(m.group(1))
        except Exception:
            continue
        if d.get("@type") != "Article":
            continue
        changed = False
        # description is a leak only when the schema also points at another post
        mep0 = d.get("mainEntityOfPage")
        leaked = isinstance(mep0, str) and not mep0.rstrip("/").endswith(os.path.basename(path)[:-5])
        if leaked and desc and d.get("description"):
            d["description"] = desc.replace("&mdash;", "-")
            changed = True
            notes.append("Article description resynced")
        # Article headline. Found 2026-08-29 on the White Tee Edit: the head-swap
        # rewrote <title>, og:title and twitter:title but not the JSON-LD headline,
        # so the schema still announced "The Niche Grip Report". Same test as the
        # other fields - only a leak if it holds ANOTHER post's title verbatim.
        hl = d.get("headline")
        if ogt and hl and norm(hl) != norm(ogt) and norm(hl) in foreign:
            d["headline"] = html.unescape(ogt).replace("—", "-")
            changed = True
            notes.append(f"Article headline {hl!r} -> og:title")

        # schema image kept pointing at /images/grips/hero.jpg - use og:image.
        # TWO guards, both learned the hard way:
        #  - skip the grip report itself; grips/hero.jpg is ITS OWN image, and a
        #    first pass "fixed" it into the generic og-image.jpg.
        #  - never swap in the generic social fallback: 131 posts point og:image
        #    there, so it is not evidence of anything.
        ogi = meta(r'<meta property="og:image" content="([^"]*)"')
        if (ogi and d.get("image") and d["image"] != ogi
                and "/images/grips/" in d["image"]
                and me != "the-niche-grip-report"
                and not ogi.endswith("/images/og-image.jpg")):
            d["image"] = ogi
            changed = True
            notes.append("schema image -> og:image")

        mep = d.get("mainEntityOfPage")
        slug = os.path.basename(path)[:-5]
        if isinstance(mep, str) and not mep.rstrip("/").endswith(slug) and can:
            d["mainEntityOfPage"] = can
            changed = True
            notes.append(f"mainEntityOfPage {mep} -> {can}")
        if changed:
            s = s.replace(m.group(1), json.dumps(d, ensure_ascii=False), 1)

    # 4. visible FAQ rebuilt from this page's own FAQPage schema
    fs = [m for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
          if '"FAQPage"' in m.group(1)]
    i = s.find('<div class="faq"')
    if fs and i >= 0:
        items = [(q["name"], q["acceptedAnswer"]["text"])
                 for q in json.loads(fs[0].group(1))["mainEntity"]]
        shown = re.findall(r'<summary>(.*?)</summary>', s[i:i + 12000], re.S)
        # Compare with entities decoded. Four pages differ only in typography
        # (&mdash; / &ldquo; in the rendered FAQ vs plain characters in the JSON).
        # Those are CORRECT as rendered - rebuilding them from schema would strip
        # the proper dashes and curly quotes out of the visible page.
        def key(x):
            # strip quote marks entirely - the wedge report renders &ldquo;custom
            # wedge&rdquo; where its schema has 'custom wedge'. Same question.
            t = html.unescape(re.sub(r"<[^>]+>", "", x)).replace("—", "-")
            return norm(re.sub(r"[\"'“”‘’]", "", t))
        if [key(x) for x in shown] != [key(q) for q, _ in items]:
            new = ('<div class="faq">\n' + "\n".join(
                f'    <details class="faq-q"><summary>{q}</summary><p>{a}</p></details>'
                for q, a in items) + "\n  </div>")
            depth, j = 0, i
            for m in re.finditer(r"<div\b|</div>", s[i:]):
                depth += -1 if m.group(0) == "</div>" else 1
                j = i + m.end()
                if depth == 0:
                    break
            s = s[:i] + new + s[j:]
            notes.append(f"visible FAQ rebuilt from schema ({len(items)} Q, was {len(shown)})")

    if s != orig and apply_:
        open(path, "w", encoding="utf-8").write(s)
    return notes


def shared_faqs(paths):
    """Report any FAQ question-set that appears on more than one page.

    THE BLIND SPOT THIS CLOSES (Lenny, 2026-08-30: "the FAQ is repeating on a
    bunch of pages"). The repair above rebuilds the VISIBLE FAQ from the page's
    own FAQPage schema, on the assumption the schema is right — which held for
    the four pages it was written for. It is useless when the clone copied BOTH:
    the White Tee Edit carried the Niche Grip Report's eight grip questions in
    the visible block AND in the JSON-LD, so visible matched schema and the
    check passed while the page shipped another post's FAQ.

    Two pages can never legitimately share an identical question set, so this is
    reported rather than auto-fixed — writing a real FAQ needs a human.
    """
    import hashlib, collections
    by = collections.defaultdict(list)
    for p in paths:
        s = open(p, encoding="utf-8", errors="replace").read()
        qs = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", q)).strip().lower()
              for q in re.findall(r"<summary>(.*?)</summary>", s, re.S)]
        if qs:
            by[hashlib.md5("|".join(qs).encode()).hexdigest()].append(
                (os.path.basename(p), qs[0]))
    return {k: v for k, v in by.items() if len(v) > 1}


def main(apply_=False):
    n = 0
    paths = sorted(glob.glob(os.path.join(ROOT, "drops", "*.html")))
    titles = other_titles(paths)
    for p in paths:
        notes = fix(p, apply_, titles)
        if notes:
            n += 1
            print(f"{os.path.basename(p)}")
            for x in notes:
                print("   -", x)
    print(f"\n{'fixed' if apply_ else 'would fix'} {n} page(s)")

    dupes = shared_faqs(paths)
    if dupes:
        print("\n!! SHARED FAQ — these pages carry an identical question set,")
        print("   which means one of them was cloned WITH the other's FAQ.")
        print("   Not auto-fixable: write a real FAQ for the wrong one.")
        for v in dupes.values():
            print(f'\n   first question: "{v[0][1][:70]}"')
            for name, _ in v:
                print("      -", name)
    else:
        print("no shared FAQ sets")
    if not apply_:
        print("(dry run - pass --apply to write)")


if __name__ == "__main__":
    main("--apply" in sys.argv)
