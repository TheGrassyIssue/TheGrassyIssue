#!/usr/bin/env python3
"""
apply-faq-style.py — make every FAQ on the site use one structure and one stylesheet.

Lenny, 2026-08-30: "fix the FAQ sections across the website - not formatting
perfectly."

WHAT WAS ACTUALLY WRONG
-----------------------
Four different states were live at once:

  30 pages  <div class="faq"> + <details class="faq-q">, WITH the house CSS.
            These were correct and are the reference for everything below.

   3 pages  the same markup with NO .faq CSS at all, so the browser fell back to
            raw <details> defaults: full-bleed 1340px measure, no rule between
            items, question and answer at identical weight, a stock ▼ marker.
            Unreadable. These are best-golf-streetwear-brands-2026, Edel and
            Sentinel — the three most recent builds.

            ROOT CAUSE, and it is self-inflicted: all three were generated from
            drops/brand-to-know-kingfisher-golf.html, which carries FAQPage
            schema but has NO visible FAQ, and therefore never carried the .faq
            rules. The builders copy the template's <head> wholesale, so they
            emitted FAQ markup into a stylesheet that had no idea what .faq was.

   2 pages  an older div-based structure (.faq-item/.faq-q/.faq-a) that renders
            permanently expanded — no accordion, and a different look again.

  26 pages  FAQPage schema in the head and NO visible FAQ anywhere on the page.
            That is a Google structured-data policy violation (the marked-up
            content has to be visible to the reader), and it wastes eight or so
            real questions per page that someone already wrote.

WHY NO GATE CAUGHT IT
---------------------
verify-post.py's "every class used has a CSS rule" check has `faq` in its EXEMPT
set, and `faq-q` was matched by an unrelated font-family rule that happens to
list `.faq-q p`. So the one check that exists for exactly this failure mode was
looking straight past it. That is fixed in verify-post.py alongside this script.

WHAT THIS DOES
--------------
  1. installs the house CSS on any page that has FAQ markup and lacks it
  2. converts the div-based FAQs to the standard <details> structure
  3. renders a visible FAQ, built from the page's OWN FAQPage schema, on pages
     that have the schema and no visible block

Idempotent: a second run reports 0 changes. Dry run by default.
"""
import glob, html, json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))

# The house FAQ style, lifted verbatim from the 30 pages that were already
# correct. Do not "improve" it here — this file's job is to make everything
# match the reference, not to introduce a fourth look.
CSS = """<style>
/*TGI-FAQ-V1*/
.faq{max-width:820px}
.faq-q{border-top:.5px solid var(--ink);padding:14px 0}
.faq-q summary{font-family:var(--serif);font-size:16px;cursor:pointer;list-style:none}
.faq-q summary::-webkit-details-marker{display:none}
.faq-q summary:before{content:"+ ";font-family:var(--mono);opacity:.5}
.faq-q[open] summary:before{content:"\\2212 "}
.faq-q p{font-family:var(--serif);font-size:13px;line-height:1.6;opacity:.8;margin:10px 0 0}
</style>"""

MARK = "/*TGI-FAQ-V1*/"


def styles_of(h):
    """CSS only from inside <style> blocks.

    Scanning the whole document would match `.faq` inside a JSON-LD answer or a
    script string. apply-header.py already shipped that bug once by matching a
    selector inside a <script>; not repeating it here.
    """
    return "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", h, re.S))


def body_of(h):
    return re.sub(r"<style[^>]*>.*?</style>", " ", h, flags=re.S)


def faq_schema(h):
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        if '"FAQPage"' not in j:
            continue
        try:
            d = json.loads(j)
        except Exception:
            return None
        out = []
        for q in d.get("mainEntity", []):
            try:
                out.append((q["name"], q["acceptedAnswer"]["text"]))
            except (KeyError, TypeError):
                return None
        return out or None
    return None


def render(items):
    rows = "\n".join(
        '    <details class="faq-q"><summary>%s</summary><p>%s</p></details>'
        % (q, a) for q, a in items)
    return '<div class="faq">\n%s\n  </div>' % rows


def ensure_css(h):
    """Add the house rules unless this page already has a real .faq rule.

    Test for `.faq{` specifically. An earlier cut tested for the substring
    ".faq" and found the font-family rule that lists `.faq-q p`, concluded every
    page was styled, and changed nothing at all.
    """
    # ONLY style pages that actually have a FAQ. A first run reported "css
    # installed 150" because this ran unconditionally and was cheerfully adding
    # a dead .faq block to 120 pages that have no FAQ anywhere on them.
    if '<div class="faq"' not in body_of(h):
        return h, False
    if MARK in h or re.search(r"\.faq\s*\{", styles_of(h)):
        return h, False
    i = h.find("</head>")
    if i < 0:
        return h, False
    return h[:i] + CSS + "\n" + h[i:], True


# Match the selector plus any continuation before the brace, so compound and
# pseudo-class forms go too. A first cut anchored on `\.faq-item\s*\{` and left
# `.faq-item:first-child { ... }` behind on the field guide as dead CSS.
LEGACY = re.compile(r"\.faq(?:-item|-a|-q)?[^{}]*\{[^}]*\}")
LEGACY_SIG = re.compile(r"\.faq-a[^{}]*\{|\.faq-item[^{}]*\{")


def strip_legacy(h):
    """Remove the bespoke FAQ rules from the two div-era pages.

    Converting their MARKUP without touching their CSS made them worse, not
    better: Mogshade's own sheet sets .faq{max-width:1400px} and styles .faq-q
    as a 19px italic serif heading. Once .faq-q became the <details> element,
    every summary inherited that, and the block ran the full 1400px. Strip the
    legacy rules first, then let the house block land.

    Only touches pages that actually carry .faq-a / .faq-item — the div-era
    signature. The 30 correct pages define .faq and .faq-q too, and must not be
    stripped.
    """
    out, changed = [], False
    for m in re.finditer(r"(<style[^>]*>)(.*?)(</style>)", h, re.S):
        pass
    def sub(m):
        nonlocal changed
        css = m.group(2)
        # Never touch the block we just installed.
        if MARK in css or not LEGACY_SIG.search(css):
            return m.group(0)
        new = LEGACY.sub("", css)
        if new != css:
            changed = True
        return m.group(1) + new + m.group(3)
    h = re.sub(r"(<style[^>]*>)(.*?)(</style>)", sub, h, flags=re.S)
    return h, changed


def convert_divs(h):
    """(.faq-item, .faq-q div, .faq-a div) -> the standard <details> block."""
    if 'class="faq-item"' not in body_of(h):
        return h, False
    items = []
    for m in re.finditer(
            r'<div class="faq-item">\s*<div class="faq-q">(.*?)</div>\s*'
            r'<div class="faq-a">(.*?)</div>\s*</div>', h, re.S):
        q = re.sub(r"\s+", " ", m.group(1)).strip()
        a = re.sub(r"\s+", " ", m.group(2)).strip()
        a = re.sub(r"^<p>|</p>$", "", a).strip()
        items.append((q, a))
    if not items:
        return h, False
    first = h.find('<div class="faq-item">')
    last = h.rfind('<div class="faq-item">')
    end = h.find("</div>", h.find("</div>", h.find("</div>", last) + 6) + 6) + 6
    return h[:first] + render(items) + h[end:], True


def add_visible(h, title):
    """Render the page's own FAQPage schema as a visible block.

    Inserted immediately before <section class="more">, in the same section
    wrapper the correct pages use. The content is NOT invented — it is the
    schema that is already on the page and already being served to Google.
    """
    if "<details" in body_of(h) or 'class="faq-item"' in body_of(h):
        return h, False
    items = faq_schema(h)
    if not items:
        return h, False
    i = h.find('<section class="more">')
    if i < 0:
        i = h.find("<footer")
    if i < 0:
        return h, False
    sec = ('<section class="products" style="border-top:none;padding-top:48px">\n'
           '  <h2 class="products-hdr" id="faq">%s</h2>\n  %s\n</section>\n\n'
           % (title, render(items)))
    return h[:i] + sec + h[i:], True


def main(apply_=False):
    paths = sorted(glob.glob(os.path.join(ROOT, "drops", "*.html")))
    paths += sorted(glob.glob(os.path.join(ROOT, "guides", "*.html")))
    for extra in ("field-guide/index.html", "brands/index.html"):
        p = os.path.join(ROOT, extra)
        if os.path.exists(p):
            paths.append(p)

    n = {"css": 0, "converted": 0, "rendered": 0, "stripped": 0}
    for p in paths:
        h = orig = open(p, encoding="utf-8").read()
        name = os.path.basename(p)
        notes = []

        h, did = convert_divs(h)
        if did:
            n["converted"] += 1
            notes.append("div-based FAQ -> <details>")

        h, did = strip_legacy(h)
        if did:
            n["stripped"] = n.get("stripped", 0) + 1
            notes.append("legacy div-era FAQ CSS stripped")

        m = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S)
        t = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else ""
        # keep the heading short — an h1 like "The 5 Best Golf Streetwear Brands
        # in 2026" makes a terrible section header with " — FAQ" bolted on.
        title = "Frequently Asked" if len(t) > 34 else (t + " &mdash; FAQ" if t else "Frequently Asked")
        h, did = add_visible(h, title)
        if did:
            n["rendered"] += 1
            notes.append("visible FAQ rendered from this page's own schema")

        h, did = ensure_css(h)
        if did:
            n["css"] += 1
            notes.append("house .faq CSS installed")

        if notes:
            print("%-52s %s" % (name[:52], "; ".join(notes)))
            if apply_ and h != orig:
                open(p, "w", encoding="utf-8").write(h)

    print("\ncss installed        %d" % n["css"])
    print("div FAQs converted   %d" % n["converted"])
    print("FAQs made visible    %d" % n["rendered"])
    print("legacy CSS stripped  %d" % n["stripped"])
    if not apply_:
        print("\n(dry run - pass --apply to write)")


if __name__ == "__main__":
    main("--apply" in sys.argv)
