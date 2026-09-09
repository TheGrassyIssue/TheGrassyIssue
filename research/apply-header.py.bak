#!/usr/bin/env python3
"""
apply-header.py — one header across Feed, Brands, Field Guide and Events.

Lenny, 2026-08-29: "the header needs to be consistent between the feed, brands
field guide and events page. keep it all the same with the header and
weather/book a tee time line."

WHAT WAS ACTUALLY DIFFERENT (audited, not assumed)
--------------------------------------------------
    Feed         banner ✓  search ✓  toggle ✓  4 links
    Brands       banner ✗  search ✗  toggle ✗  4 links
    Field Guide  banner ✗  search ✗  toggle ✗  4 links, and <nav class="nav">
                 with no role/aria-label
    Events       banner ✗  search ✓  toggle (no aria-expanded/onclick)
                 and only THREE links — "Feed" instead of "The Feed", and no
                 Field Guide link at all. That one is a navigation hole, not a
                 cosmetic difference.

index.html is the reference. Three things have to travel together or the banner
renders as unstyled text with empty spans:
    1. the markup  (.weather-banner + <nav>)
    2. 11 CSS rules for .weather-banner / .wb-*
    3. the ~2.3kB weather script that fills #wb-date, #wb-temp, #wb-desc, #wb-icon

Idempotent. Writes research/header-inventory.json (size+sha) before any write.
Re-run after build-brands.py, which regenerates /brands/index.html.
"""
import os, re, json, hashlib, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(ROOT, "index.html")
# page -> which nav link carries class="active"
TARGETS = {
    "brands/index.html": "/brands/",
    "field-guide/index.html": "/field-guide/",
    "events/index.html": "/events/",
}
MARK = "<!--TGI-HDR-V1-->"        # markup only
# A separate CSS-safe marker. An HTML comment inside <style> is NOT a comment to
# the CSS parser: `<!--TGI-HDR-V1-->` merged into the next selector and the main
# rule parsed as `tgi-hdr-v1-- > .weather-banner`, which matches nothing — so the
# banner silently lost its background, flex layout and padding on all three pages
# while every child rule (.wb-date, .wb-dot …) applied normally.
CSS_MARK = "/*TGI-HDR-V1*/"
JS_MARK = "// TGI-HDR-V1"


def ref_parts():
    s = open(REF, encoding="utf-8").read()
    # Search for CSS ONLY inside <style> blocks. Scanning the whole document let
    # the selector regex match `.nav');` inside a <script> and swallow JavaScript
    # up to the next `{` — that JS got injected into the target's stylesheet,
    # which stopped Chrome's CSS parser dead. /brands/ parsed 93 rules instead of
    # 197 and everything after the injection point silently lost its styling.
    css_src = "\n".join(m.group(1) for m in re.finditer(r"<style\b[^>]*>(.*?)</style>", s, re.S))
    banner = re.search(r"(<!-- WEATHER / DATE / TEE TIME BANNER -->\s*<div class=\"weather-banner\".*?</div>\s*)\n\s*<nav",
                       s, re.S).group(1)
    nav = re.search(r"(<nav class=\"nav\"[^>]*>.*?</nav>)", s, re.S).group(1)
    # Grab the banner CSS but keep @media wrappers intact. A flat findall pulled
    # the (max-width:600px) overrides out of their wrapper, so the mobile padding
    # and 10px type applied at EVERY width and, being last, won — the banner
    # rendered 8px/10px on the three ported pages against 10px/11px on the feed.
    # Selectors the header depends on. `.nav-wordmark` is deliberately EXCLUDED —
    # apply-wordmark.py and apply-green-wordmark.py own that rule, and porting a
    # copy here would fight them.
    #
    # The nav rules matter as much as the banner: /brands/ had none of them, so
    # .nav-inner lost justify-content:space-between, .nav-links fell back to Inter
    # at 16px instead of mono at 10px, and #tgi-search-input rendered as a raw
    # Arial browser input. The banner alone looked right and the row under it did not.
    WANT = re.compile(r"^\s*(?:\.weather-banner|\.wb-[a-z-]+|\.nav\b|\.nav-inner|\.nav-links|"
                      r"\.nav-toggle|#tgi-sbox|#tgi-search-input|#tgi-search-results|#tgi-search)")
    css_parts, seen = [], set()
    for m in re.finditer(r"@media[^{]*\{", css_src):
        depth, i = 1, m.end()
        while depth and i < len(css_src):
            if css_src[i] == "{":
                depth += 1
            elif css_src[i] == "}":
                depth -= 1
            i += 1
        block = css_src[m.start():i]
        if any(WANT.match(x) for x in re.split(r"[,{]", block.split("{",1)[1])) or ".weather-banner" in block or ".nav" in block or "tgi-s" in block:
            css_parts.append(block)
            seen.add((m.start(), i))
    # then the top-level rules, skipping anything already inside a captured @media
    RULE = re.compile(r"(?:\.weather-banner|\.wb-[a-z-]+|\.nav|\.nav-inner|\.nav-links|\.nav-toggle|#tgi-sbox|#tgi-search-input|#tgi-search-results)[^{}]*\{[^}]*\}")
    for m in RULE.finditer(css_src):
        if ".nav-wordmark" in m.group(0): continue
        if not any(a <= m.start() < b for a, b in seen):
            css_parts.insert(len([c for c in css_parts if not c.startswith("@media")]), m.group(0))
    css = css_parts
    js = None
    for m in re.finditer(r"<script\b[^>]*>(.*?)</script>", s, re.S):
        if "wb-temp" in m.group(1) or "wb-date" in m.group(1):
            js = m.group(1)
            break
    return banner, nav, "\n".join(css), js


def build_nav(nav, active_href):
    """Same nav, with class="active" moved to this page's own link."""
    out = re.sub(r'\s*class="active"', "", nav)
    # the feed link is href="#feed" on index; make it absolute everywhere else
    out = out.replace('<a href="#feed"', '<a href="/#feed"')
    out = re.sub(rf'(<a href="{re.escape(active_href)}")', r'\1 class="active"', out, count=1)
    return out


def fix(path, banner, nav, css, js, active, apply_):
    p = os.path.join(ROOT, path)
    s = open(p, encoding="utf-8").read()
    orig, notes = s, []

    # 1. markup: replace everything from <body> up to and including </nav>
    new_block = MARK + "\n" + banner + "\n" + build_nav(nav, active)
    m = re.search(r"(<body[^>]*>)(.*?)</nav>", s, re.S)
    if m:
        cur = m.group(2)
        keep = re.search(r'(<a href="#[^"]*" class="skip-link">.*?</a>)', cur, re.S)
        skip = (keep.group(1) + "\n\n") if keep else ""
        rebuilt = m.group(1) + "\n\n" + skip + new_block
        if rebuilt != m.group(0):
            s = s[:m.start()] + rebuilt + s[m.end():]
            notes.append("header markup unified")

    # 2. CSS — append once, before the last </style>
    if ".weather-banner" not in orig:
        k = s.rfind("</style>")
        if k > 0:
            # `css` arrives already joined by ref_parts(). Joining again split it
            # character by character — "+1386 banner CSS blocks" was the tell.
            s = s[:k] + "\n" + CSS_MARK + "\n" + css + "\n" + s[k:]
            notes.append(f"+{css.count('{')} banner CSS rules")

    # 3. JS — append once, before </body>
    if js and "wb-temp" not in orig:
        k = s.rfind("</body>")
        if k > 0:
            s = s[:k] + f"<script>{JS_MARK}\n{js}</script>\n" + s[k:]
            notes.append("+weather script")

    if s != orig and apply_:
        open(p, "w", encoding="utf-8").write(s)
    return notes, s != orig


def main(apply_=False):
    banner, nav, css, js = ref_parts()
    inv, n = {}, 0
    for path, active in TARGETS.items():
        full = os.path.join(ROOT, path)
        if not os.path.exists(full):
            print(f"  !! missing {path}")
            continue
        if apply_:
            b = open(full, "rb").read()
            inv[path] = {"size": len(b), "sha1": hashlib.sha1(b).hexdigest()}
        notes, changed = fix(path, banner, nav, css, js, active, apply_)
        if changed:
            n += 1
            print(f"  {path}: {'; '.join(notes)}")
    if apply_ and inv:
        os.makedirs(os.path.join(ROOT, "research"), exist_ok=True)
        json.dump(inv, open(os.path.join(ROOT, "research", "header-inventory.json"), "w"), indent=1)
    print(f"\n{'updated' if apply_ else 'would update'} {n} page(s)")
    if not apply_:
        print("(dry run - pass --apply to write)")


if __name__ == "__main__":
    main("--apply" in sys.argv)
