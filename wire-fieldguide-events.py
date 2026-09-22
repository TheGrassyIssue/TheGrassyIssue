#!/usr/bin/env python3
"""wire-fieldguide-events.py — link TGI's own events from the Field Guide.
22 September 2026.

Lenny: "let's include a links to the events in the field guide."

WHAT WAS MISSING. The hub's events-and-history section carries four cards, and
only one of them is an event — the Firecracker Open, which is somebody else's.
The Grassy Issue runs two events of its own, /events/the-long-walk and
/events/social-club, and the Field Guide linked to neither. It pointed at
/events three times, all from the nav, and never at either event page.

WHICH EVENTS, AND WHY NOT THE OTHER TWO. There are four pages under /events/.
Two are finished: the Hill Country Amateur ran 16-17 May 2026 and the Texas
Children's Legacy Classic on 14 May 2026, both four months before today. Linking
a hub section headed "what's happening" to a tournament that happened in spring
would be worse than not linking at all. The Long Walk and the Social Club carry
no fixed date — they are recurring and open — so they are the two that belong on
a living page.

THE POSTERS ARE NOT USABLE AS CARD IMAGES. .guide-card-img is a 300px-tall
object-fit:cover band, and both event posters are portrait (800x1200 and
1254x1254). Cropping a poster into a wide band shows a slice of its typography
rather than a picture. So each card takes a real photograph already in
images/field-guide/ that is true to the event:

  The Long Walk  jimmy-clay.jpg   the walk literally starts at Jimmy Clay, and
                                  there is no cart in the frame, which matters
                                  for an event whose whole premise is no carts.
                                  (morris-williams-sunset.jpg was the other
                                  candidate and has a golf cart in it.)
  Social Club    hill-country-golf.jpg  someone mid-swing rather than an empty
                                  course, for a thing that is about who you play
                                  with; the page itself talks about driving "an
                                  hour into the Hill Country".

EVERY FIGURE ON THESE CARDS IS FROM THE EVENT PAGE'S OWN COPY: 36 holes, no
carts, Jimmy Clay to Roy Kizer, donations to First Tee; 8-12 per outing, ninety
minutes out, no dues. Nothing is estimated.

Idempotent. Dry run by default.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
PAGE = ROOT / "field-guide/index.html"
MARK, END = "<!-- TGI-FG-EVENTS -->", "<!-- /TGI-FG-EVENTS -->"
ANCHOR = "What's happening and what came before"

CARDS = [
    dict(href="/events/the-long-walk",
         img="/images/field-guide/jimmy-clay.jpg",
         alt="The open green and red flagstick at Jimmy Clay, where The Long Walk starts",
         tag="TGI Event &middot; 36 Holes",
         title="The Long Walk &mdash; Golf Till You Drop",
         desc="Back-to-back tee times at Jimmy Clay and Roy Kizer, 36 holes on foot with no "
              "carts. Donations go to First Tee.",
         cta="See the event &rarr;"),
    dict(href="/events/social-club",
         img="/images/field-guide/hill-country-golf.jpg",
         alt="A golfer mid-swing on a Hill Country fairway outside Austin",
         tag="TGI Event &middot; 8&ndash;12 Players",
         title="The Grassy Issue Social Club",
         desc="Small groups playing good courses within ninety minutes of Austin. Not a "
              "tournament, not a league, no dues.",
         cta="Join the list &rarr;"),
]


def block():
    out = [MARK]
    for c in CARDS:
        out.append(f'''    <a href="{c['href']}" class="guide-card">
      <img class="guide-card-img" src="{c['img']}" alt="{c['alt']}" loading="lazy" />
      <div class="guide-card-body">
        <div class="guide-card-tag">{c['tag']}</div>
        <div class="guide-card-title">{c['title']}</div>
        <div class="guide-card-desc">{c['desc']}</div>
        <span class="guide-card-link">{c['cta']}</span>
      </div>
    </a>''')
    out.append(f"    {END}")
    return "\n".join(out)


def container_span(b, start):
    """(open_end, close_start, close_end) for the div opening at `start`.

    The first version advanced the cursor by a bare 4 characters per match and
    returned an index in the MIDDLE of the closing "</div>". Everything built on
    that was then off: rfind("</div>", start, end) could not see the container's
    own closing tag, found the last CARD's instead, and the two new cards were
    inserted inside another card — images detached from their bodies and the
    second grid column went empty. It rendered visibly wrong, which is the only
    reason it was caught. So this returns explicit, exact boundaries and the
    caller never has to guess where the container ends.
    """
    depth, j = 0, start
    while True:
        m = re.search(r"<div\b|</div>", b[j:])
        if not m:
            sys.exit("! unterminated .guide-cards container")
        tok = m.group(0)
        pos = j + m.start()
        if tok == "</div>":
            depth -= 1
            if depth == 0:
                return pos, pos + len("</div>")
        else:
            depth += 1
        j = pos + len(tok)


def main(apply_):
    h = PAGE.read_text(encoding="utf-8")

    # every image must exist before anything is written
    for c in CARDS:
        if not (ROOT / c["img"].lstrip("/")).is_file():
            sys.exit(f"! card image missing: {c['img']}")
        if not (ROOT / (c["href"].lstrip("/") + ".html")).is_file():
            sys.exit(f"! event page missing: {c['href']}")

    # THE STRIP MUST BE WHITESPACE-SYMMETRIC WITH THE INSERT. A first version
    # consumed \n* on both sides but re-inserted "\n  ", so the two spaces of
    # indent survived each strip and the file grew one blank line per run while
    # the card count stayed correct. Same failure as build-brand-index.py had.
    # \s* on both sides, and one fixed separator, makes a re-run a true no-op.
    SEP = "\n  "
    h = re.sub(r"\s*" + re.escape(MARK) + r".*?" + re.escape(END) + r"\s*", SEP, h, flags=re.S)

    i = h.find(ANCHOR)
    if i < 0:
        sys.exit("! events section heading not found")
    m = re.search(r'<div class="guide-cards">', h[i:])
    if not m:
        sys.exit("! no .guide-cards container in the events section")
    start = i + m.start()
    close, _ = container_span(h, start)
    before = h[start:close].count('class="guide-card"')
    new = h[:close] + block() + SEP + h[close:]
    s2, e2 = container_span(new, start)
    after = new[start:s2].count('class="guide-card"')
    print(f"  events section: {before} cards -> {after}")
    for c in CARDS:
        print(f"    + {c['href']}")

    if not apply_:
        print("\n  dry run — pass --apply")
        return

    PAGE.write_text(new, encoding="utf-8")

    # ---- VERIFY ON THE FINISHED PAGE ----
    fin = PAGE.read_text(encoding="utf-8")
    bad = []
    if fin.count(MARK) != 1 or fin.count(END) != 1:
        bad.append(f"{fin.count(MARK)} blocks, expected 1")
    blk = fin[fin.index(MARK):fin.index(END)]
    for c in CARDS:
        if f'href="{c["href"]}"' not in blk:
            bad.append(f"{c['href']} not in the block")
        if f'src="{c["img"]}"' not in blk:
            bad.append(f"{c['img']} not in the block")
    # house shape, checked against the markers the neighbouring cards use
    for need in ('class="guide-card"', 'class="guide-card-img"', 'class="guide-card-tag"',
                 'class="guide-card-title"', 'class="guide-card-desc"',
                 'class="guide-card-link"'):
        if blk.count(need) < len(CARDS):
            bad.append(f"only {blk.count(need)} of {len(CARDS)} cards carry {need}")
    # the new cards must sit INSIDE the events grid, not after it
    i2 = fin.find(ANCHOR)
    s2 = i2 + re.search(r'<div class="guide-cards">', fin[i2:]).start()
    c2, e2 = container_span(fin, s2)
    if not (s2 < fin.index(MARK) < fin.index(END) < c2):
        bad.append("cards landed outside the events grid")
    # EVERY CARD IN THE GRID MUST STILL BE A WHOLE CARD. The nesting break that
    # put these cards inside another card left the markup superficially fine —
    # right class names, right counts — and only showed up as detached images
    # and an empty column in a screenshot. Counting the parts inside each <a>
    # catches it without anyone having to look.
    grid = fin[s2:c2]
    for am in re.finditer(r'<a href="[^"]+" class="guide-card">(.*?)</a>', grid, re.S):
        inner = am.group(1)
        href = re.search(r'<a href="([^"]+)"', am.group(0)).group(1)
        if inner.count("<img") != 1:
            bad.append(f"card {href}: {inner.count('<img')} images, expected 1")
        if inner.count('class="guide-card-body"') != 1:
            bad.append(f"card {href}: {inner.count('class=' + chr(34) + 'guide-card-body' + chr(34))} bodies")
        if "guide-card\"" in inner:
            bad.append(f"card {href} contains another card — nesting is broken")
    n_anchor = len(re.findall(r'<a href="[^"]+" class="guide-card">', grid))
    if n_anchor != grid.count('class="guide-card"'):
        bad.append(f"{n_anchor} card anchors but {grid.count('class=' + chr(34) + 'guide-card' + chr(34))} card classes")
    if grid.count("<a ") != grid.count("</a>"):
        bad.append(f"grid anchor imbalance: {grid.count('<a ')} open, {grid.count('</a>')} close")

    # no dead links anywhere on the page
    body = fin[fin.find(">", fin.find("<body")) + 1:]
    inner = (re.search(r"</header>(.*?)<footer", body, re.S) or re.match(r"(.*)", body, re.S)).group(1)
    for u in sorted(set(re.findall(r'href="(/[^"#][^"]*)"', inner))):
        p = u.lstrip("/").rstrip("/")
        if not ((ROOT / (p + ".html")).is_file() or (ROOT / p / "index.html").is_file()
                or (ROOT / p).exists()):
            bad.append(f"dead link: {u}")
    # and the two finished events must NOT have been linked
    for gone in ("hill-country-amateur-2026", "texas-childrens-classic-2026"):
        if gone in blk:
            bad.append(f"linked a finished event: {gone}")
    if bad:
        sys.exit("! " + "\n    ".join(bad))
    print(f"\n  verified: {after} cards in the events grid, house shape, no dead links")


if __name__ == "__main__":
    main("--apply" in sys.argv)
