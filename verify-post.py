#!/usr/bin/env python3
"""Verify a TGI drop page against house format. Usage: python3 verify-post.py drops/foo.html"""
import re, sys, os, json, html

def match_div(s, i):
    d = 0
    for m in re.finditer(r'<div\b|</div>', s[i:]):
        d += 1 if m.group(0) != '</div>' else -1
        if d == 0: return i + m.end()
    return -1

def verify(path):
    root = os.path.dirname(os.path.abspath(__file__))
    h = open(path, encoding="utf-8").read()
    fails = []
    def chk(name, ok, detail=""):
        print(("  OK   " if ok else "  FAIL ") + name + (("  " + detail) if detail and not ok else ""))
        if not ok: fails.append(name)

    # --- HOUSE FORMAT (the rule that broke Malbon + Lottery Round, 2026-08-20) ---
    grids = list(re.finditer(r'<div class="products-grid">', h))
    cards = list(re.finditer(r'<div class="product-card', h))
    spans = [(m.start(), match_div(h, m.start())) for m in grids]
    outside = [c.start() for c in cards if not any(a < c.start() < b for a, b in spans)]
    chk("every product-card sits inside a .products-grid", not outside,
        "%d card(s) outside the grid — they will render full-width and oversized" % len(outside))
    chk("at least one .products-grid present", bool(grids) or not cards)

    # EVERY class used in the body must have a CSS rule somewhere on the page.
    # Inventing a class name renders it completely unstyled — this has now bitten
    # three times (spec-table on the wedge post, products-grid + faq-item here).
    # NB: these pages carry SEVERAL <style> blocks — concatenate them all, and strip
    # them out before collecting used classes.
    css = "\n".join(re.findall(r'<style[^>]*>(.*?)</style>', h, re.S))
    body_html = re.sub(r'<style[^>]*>.*?</style>', ' ', h, flags=re.S)
    used = set()
    for attr in re.findall(r'class="([^"]+)"', body_html):
        used.update(attr.split())
    styled = set(re.findall(r'\.([A-Za-z][\w-]*)', css))
    # classes only ever targeted by JS/structure, not styling
    # more-kicker/more-title are unstyled across the whole site (pre-existing, not introduced here)
    # `faq` was in here, which is precisely why three pages shipped with FAQ
    # markup and no .faq rule anywhere — the check designed to catch that was
    # told to ignore it. Removed 2026-08-30.
    EXEMPT = {"products", "more-grid", "more-kicker", "more-title", "aff-disclosure"}  # aff-disclosure is inline-styled by apply-affiliates.py
    unstyled = sorted(c for c in used if c not in styled and c not in EXEMPT)
    chk("every class used has a CSS rule", not unstyled, str(unstyled))

    # A FAQ needs its OWN block rule, not merely a mention. `.faq-q p` appears in
    # a shared font-family list on every page, which was enough to satisfy the
    # generic check above while the layout rules (.faq measure, the item border,
    # the +/- marker) were entirely absent — giving raw browser <details> at
    # full page width. Test for a real `.faq{` declaration.
    # Same loophole as the FAQ: `.cat-kicker` appears in a shared font-family
    # list on every page, which satisfied the generic class check while three
    # pages had NO real kicker rule — so the lede rendered as an unstyled
    # full-width paragraph, sentences running far past the measure below.
    if 'class="cat-kicker"' in body_html:
        chk("cat-kicker has a real CSS rule (not just the font list)",
            bool(re.search(r"\.cat-kicker\s*\{[^}]*max-width", css)),
            "kicker renders full-width - install the house rule")

    if '<div class="faq"' in body_html:
        chk("FAQ markup has the house .faq CSS block",
            bool(re.search(r"\.faq\s*\{", css)),
            "page renders raw <details> at full width - run apply-faq-style.py")

    # Schema and page must agree: marked-up FAQ content has to be visible.
    if '"FAQPage"' in h:
        chk("FAQPage schema has a matching visible FAQ",
            '<div class="faq"' in body_html,
            "schema-only FAQ - Google requires the content be on the page")

    # --- structure ---
    chk("div balance", h.count("<div") == h.count("</div>"), "%d/%d" % (h.count("<div"), h.count("</div>")))
    chk("section balance", h.count("<section") == h.count("</section>"),
        "%d/%d" % (h.count("<section"), h.count("</section>")))
    chk("anchor balance", len(re.findall(r'<a\b', h)) == h.count("</a>"))
    chk("exactly one h1", len(re.findall(r'<h1', h)) == 1)

    # --- galleries ---
    bad = []
    for m in re.finditer(r'<div class="product-card[^"]*" data-frames="(\d+)">', h):
        blk = h[m.start():match_div(h, m.start())]
        if int(m.group(1)) != blk.count('class="pg-frame"'): bad.append(m.group(1))
    chk("data-frames matches actual pg-frame count", not bad, str(bad))

    # Gallery CONTROLS. The page ships JS that drives .pg-dot / .pg-arw / .pg-count; a gallery
    # with 2+ frames must emit all three or the controls silently do nothing. Bare <span> dots
    # (no class) render invisible — that shipped on four posts before this check existed.
    ctl = []
    for m in re.finditer(r'<div class="product-card[^"]*" data-frames="(\d+)">', h):
        n = int(m.group(1)); blk = h[m.start():match_div(h, m.start())]
        dots = len(re.findall(r'<button class="pg-dot[^"]*"', blk))
        cnt = re.search(r'<span class="pg-count">1/(\d+)</span>', blk)
        arw = blk.count('class="pg-arw')
        if n < 2:
            good = dots == 0
        else:
            good = (dots == n and cnt and int(cnt.group(1)) == n
                    and arw == 2 and blk.count('class="pg-dot on"') == 1)
        if not good: ctl.append(n)
    chk("gallery controls complete (dots/arrows/counter)", not ctl,
        "%d gallery(s) wrong — frames %s" % (len(ctl), ctl[:5]))
    chk("no classless <span> dots", '<div class="pg-dots"><span>' not in h)

    # EVERY CARD MUST CARRY AN IMAGE. data-frames="0" with zero pg-frames is
    # internally "consistent", so the check above passes it happily — and the
    # card renders as an empty box. That shipped on the streetwear rebuild when
    # three Casualist cards pointed at an image prefix that did not exist on
    # disk: the builder counted 0 frames, wrote data-frames="0", and every gate
    # agreed the page was fine.
    empty = []
    for m in re.finditer(r'<div class="product-card', h):
        blk = h[m.start():match_div(h, m.start())]
        if "<img" not in blk:
            # A card may be imageless ON PURPOSE when it says so: the private
            # clubs post renders Austin Golf Club with "No photography
            # published" where the frame would be, because the club releases
            # none. That is editorial, not breakage.
            if "No photography published" in blk:
                continue
            nm = re.search(r'class="product-name">([^<]*)', blk)
            empty.append(nm.group(1)[:40] if nm else "?")
    chk("every product-card contains an image", not empty, str(empty[:4]))

    # --- images ---
    srcs = re.findall(r'src="(/images/[^"]+)"', h)
    miss = [s for s in srcs if not os.path.exists(root + s)]
    chk("all local images exist", not miss, str(miss[:4]))
    # only <img> tags — third-party <script src> (analytics) is expected and allowed
    chk("no hot-linked images",
        not [i for i in re.findall(r'<img[^>]*>', h)
             if re.search(r'src="https?://(?!thegrassyissue)', i)])
    imgs = re.findall(r'<img[^>]*>', h)
    chk("every img has alt", all('alt="' in i for i in imgs), "%d imgs" % len(imgs))

    # --- metadata / schema ---
    lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    parsed = []
    for j in lds:
        try: parsed.append(json.loads(j))
        except Exception as e: fails.append("JSON-LD parse"); print("  FAIL JSON-LD parse", e)
    chk("JSON-LD blocks parse", len(parsed) == len(lds))
    slug = os.path.basename(path).replace(".html", "")
    can = re.search(r'<link rel="canonical"[^>]*>', h)
    chk("canonical points at this slug", bool(can) and slug in can.group(0))

    # --- editorial rules ---
    # strip tags first so hrefs/slugs (e.g. the legacy 10-texas-courses-worth-the-trip)
    # don't trip the ban — it applies to prose, not to historical URLs.
    # Drop the More-from-Feed and Instagram strips BEFORE the prose checks. Those
    # cards are auto-generated navigation — their text is another post's TITLE, not
    # copy written for this page. Eight legacy posts still have "worth" in their
    # titles (Lenny declined retitling), so once fix-more-from-feed.py reshuffled
    # which posts each page links to, twelve pages started failing the ban for
    # linking to them. Same principle as the URL strip below: the rule is about
    # prose, not about pointers to things that already exist.
    txt = re.sub(r'<section class="more">.*?</section>', ' ', h, flags=re.S)
    txt = re.sub(r'<a[^>]*class="more-card".*?</a>', ' ', txt, flags=re.S)
    txt = re.sub(r'<[^>]+>', ' ', txt)
    txt = re.sub(r'https?://\S+|/[\w/-]+', ' ', txt)
    # place names containing "Worth" are not the banned word (Fort Worth, Worth Avenue...)
    txt = re.sub(r'\bFort\s+Worth\b', ' ', txt, flags=re.I)
    chk("no banned word 'worth'", not re.search(r'\bworth\b', txt, re.I))
    body = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', h, flags=re.S)
    # TEMPLATE LEAK. These pages are built by grafting a new middle between a
    # donor page's head and its tail, and the join is easy to put in the wrong
    # place — on 18 Sep 2026 the Hiroki build inherited Bluegrass Fairway's
    # "What It Is Made Of" and "The Questions" wholesale, five foreign FAQ
    # answers and all. A duplicated h2 is the signature of that mistake and is
    # never intentional in this format, so it fails here rather than shipping.
    h2s = [re.sub(r'<[^>]+>', '', x).strip().lower()
           for x in re.findall(r'<h2[^>]*>(.*?)</h2>', body, re.S)]
    dupes = sorted({x for x in h2s if h2s.count(x) > 1})
    chk("no duplicated h2 (template leak)", not dupes,
        "repeated: " + ", ".join(dupes) if dupes else "")
    # one FAQ block only — a second one means a donor page's FAQ came along
    chk("exactly one FAQ block", body.count('<div class="faq">') <= 1)
    # the page must actually close; a bad graft can truncate the tail
    # THE CAROUSEL VIEWERS ARE A DIFFERENT PAGE TYPE.
    # Seven pages under drops/ are standalone slide viewers, not articles:
    # no .drop-header, no .products-grid, no .writeup, and dozens of
    # .gear-slide blocks. They have never had a footer and should not — on
    # 18 Sep 2026 this check was read as "these pages are broken", a footer was
    # injected into all seven, and it rendered unstyled in the corner of a
    # layout that has no place for it. A footer is required of articles only.
    _is_viewer = ('class="drop-header"' not in h and 'products-grid' not in h
                  and 'gear-slide' in h)
    chk("document closes (</body></html>)" if not _is_viewer
        else "document closes (slide viewer — no footer expected)",
        '</body>' in h and '</html>' in h
        and ('<footer' in h or _is_viewer))
    words = len(html.unescape(re.sub(r'<[^>]+>', ' ', body)).split())
    # more-cards must use the styled structure — .more-kicker/.more-title have no CSS
    mc = re.findall(r'<a[^>]*class="more-card".*?</a>', h, re.S)
    chk("more-cards carry an image and use .more-card-img/-body",
        all('more-card-img' in c and '<img' in c for c in mc))
    # THE SIDEBAR MUST SIT IN A CONTAINER THAT GIVES IT A COLUMN.
    # Exactly two containers on this site do that, and the CSS is the authority:
    #   legacy    <div class="writeup">      .writeup{display:grid;2fr 1fr}
    #   template  <section data-btk="take">  section[data-btk="take"]{display:grid;
    #                                          minmax(0,1fr) 300px}
    # Anywhere else the aside has no column: it spans the full band under the
    # copy, and because the position:static override is scoped to "take" it also
    # keeps position:sticky from the base .sidebar rule and rides down the page.
    #
    # The previous version only knew the legacy form — it did
    # h.find('<div class="writeup">') and, when that returned -1, left _depth as
    # None and passed. On all 37 template-era pages that div does not exist, so
    # this check COULD NOT FAIL on any of them. It duly reported OK for the AXXA
    # page on 20 Sept, whose aside sat in data-btk="story" (no grid rule at all)
    # — the layout Lenny reported as broken. A guard that returns a plausible
    # value rather than a correct one.
    #
    # Find the aside's immediate parent by walking a stack, and name it.
    _stack, _parent = [], None
    for _m in re.finditer(r'<(div|section|aside)\b[^>]*>|</(?:div|section|aside)>', h):
        _t = _m.group(0)
        if _t.startswith("</"):
            if _stack:
                _stack.pop()
        elif _t.startswith('<aside class="sidebar"'):
            _parent = _stack[-1] if _stack else ""
            break
        elif not _t.rstrip().endswith("/>"):
            _stack.append(_t)
    _ok = (_parent is None                                   # page has no sidebar
           or 'class="writeup"' in _parent
           or 'data-btk="take"' in _parent)
    chk("sidebar sits in a container that gives it a column",
        _ok, "" if _ok else f"parent is {(_parent or '(top level)')[:60]}")
    chk("no legacy .more-kicker/.more-title markup",
        'more-kicker' not in h and 'more-title' not in h)
    chk("word count >= 1200", words >= 1200, str(words))

    # PULL-QUOTES ARE ROMAN, in EVERY .pull-quote-inner block.
    # Lenny, on Birds of Condor: "I dont love the italics". The page carries
    # several .pull-quote-inner blocks (22px, 26px, 38px) and the LAST one wins.
    # A re.search-based check in the build script passed on a page that rendered
    # italic on screen, because it only ever saw the first, roman, block. And a
    # build-time check cannot catch this at all: btk-template.py re-injects the
    # 38px rule AFTER the build. This has to read the finished file.
    # NO TWO PULL-QUOTES BACK TO BACK. Lenny's rhythm rule: a section carries
    # images or a big quote BETWEEN passages of text. Two 38px quotes with
    # nothing between them reads as a wall of green -- how the Found Golf story
    # section first rendered.
    #
    # This needs the END of each .pull-quote element, so it walks div depth from
    # the opening tag to its matching close. A first version measured from the
    # opening tag of one quote to the opening tag of the next, which swallowed
    # the quote's own text and reported every page as stacked -- it returned the
    # same count with the fault injected and removed, i.e. it measured nothing.
    def _close_of(html, open_at):
        depth, i = 0, open_at
        for m in re.finditer(r"<div\b[^>]*>|</div>", html[open_at:]):
            depth += 1 if m.group(0) != "</div>" else -1
            if depth == 0:
                return open_at + m.end()
        return None

    _opens = [m.start() for m in re.finditer(r'<div class="pull-quote"', h)]
    _stacked = 0
    for _i in range(len(_opens) - 1):
        _e = _close_of(h, _opens[_i])
        if _e is None or _e > _opens[_i + 1]:
            continue
        _raw = h[_e:_opens[_i + 1]]
        # A heading, an image or a product grid IS a break, even with few words
        # -- on Birds of Condor an h2 + kicker sits between two quotes and a
        # bare 15-word threshold called that a defect. Lenny's rule is about
        # what separates the quotes, not how chatty it is.
        _structural = re.search(r"<h[23]\b|<img\b|<figure\b|products-grid", _raw)
        _between = re.sub(r"&[#a-z0-9]+;", " ", re.sub(r"<[^>]+>", " ", _raw))
        if not _structural and len(_between.split()) < 15:
            _stacked += 1
    chk("no two pull-quotes stacked with no prose between", _stacked == 0,
        "%d adjacent pair(s) with < 15 words between" % _stacked)


    _qb = re.findall(r"\.pull-quote-inner\b[^{]*\{([^}]*)\}", h)
    _ital = [i for i, b in enumerate(_qb, 1) if "font-style:italic" in b]
    chk("pull-quotes roman in every rule block", not _ital,
        "italic in block(s) %s of %d" % (_ital, len(_qb)))
    # Share-card tags. Added 2026-09-15 after eleven live posts were found
    # sharing on X under "Students Golf Summer 2026 — Summer School Is in
    # Session": every build script copies a model page's <head> and rewrites
    # the og: tags without ever touching twitter:. The page renders perfectly,
    # so nothing caught it until the live URL was fetched and read back.
    def _meta(k, a):
        m = re.search(r'<meta %s="%s" content="([^"]*)"' % (a, re.escape(k)), h)
        return html.unescape(m.group(1)).strip() if m else None
    _ogt, _twt = _meta("og:title", "property"), _meta("twitter:title", "name")
    _ogd, _twd = _meta("og:description", "property"), _meta("twitter:description", "name")
    _suf = " — The Grassy Issue"
    if _ogt and _twt:
        _want = _ogt[:-len(_suf)] if _ogt.endswith(_suf) else _ogt
        chk("twitter:title matches og:title (share card is this post)",
            _twt == _want or _want.startswith(_twt[:30]), f"tw={_twt[:48]!r}")
    if _ogd and _twd:
        chk("twitter:description matches og:description",
            _twd == _ogd or _ogd.startswith(_twd[:40]), f"tw={_twd[:48]!r}")
    print("\n  %s — %d check(s) failed\n" % (os.path.basename(path), len(fails)))
    return len(fails)

if __name__ == "__main__":
    sys.exit(min(1, sum(verify(p) for p in sys.argv[1:])))
