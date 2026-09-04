#!/usr/bin/env python3
"""
add-quotes.py — pepper sourced quote cards into the newest stretch of the feed.

WHY (2026-09-03): quote cards ran from feed position 59 to 217 at roughly one
every 5-6 cards, but the newest 59 cards had NONE — 23 cards had passed since
the last one. Lenny: "last few havent been peppered in."

SOURCING. Every quote here has a named source recorded beside it. Golf quotes
are heavily misattributed; nothing goes in that can't be traced. The Mark Twain
"good walk spoiled" card is REPLACED for exactly this reason — the Center for
Mark Twain Studies files it under "The Apocryphal Twain" (first in print 1903-04,
never in Twain's books/letters/speeches, Twain credit traces to a 1948 Reader's
Digest, 38 years after his death).

Idempotent via data-q-id. Dry-run by default; --apply writes; --revert removes.
"""
import sys, re

QUOTES = [
    # (id, quote, name, initials, meta, source-note)
    ("dye", "Golf is not a fair game, so why build a course fair?",
     "Pete Dye", "PD", "Architect, 1925&ndash;2020",
     "His own World Golf Hall of Fame profile"),
    ("ross", "Golf should be a pleasure, not a penance.",
     "Donald Ross", "DR", "Architect, 1872&ndash;1948",
     "Ross in his own writing: 'Bearing in mind that golf should be a pleasure and not a penance...'"),
    ("darwin", "If he had needed a 64 on his last round, you were quite certain he could have played a 64.",
     "Bernard Darwin", "BD", "On Hogan at Carnoustie, 1953",
     "The Times, 1953"),
    ("oldtom", "A&rsquo; St Andrews bairns are born wi&rsquo; web feet an&rsquo; wi&rsquo; a gowf club in their hands.",
     "Old Tom Morris", "TM", "St Andrews, 1821&ndash;1908",
     "W.W. Tulloch, 'The Life of Tom Morris'"),
    ("nelson", "Every great player has learned the two Cs: how to concentrate and how to maintain composure.",
     "Byron Nelson", "BN", "Texan, 1912&ndash;2006",
     "World Golf Hall of Fame"),
]

# replaces the apocryphal Twain card in place
TWAIN_REPLACEMENT = ("burke", "I don&rsquo;t give tips. That&rsquo;s for horse racing, not golf.",
    "Jack Burke Jr.", "JB", "Champions G.C., 1923&ndash;2024",
    "Golf Digest, 'My Shot' (Guy Yocom)")

PORTRAIT = ("width:48px;height:48px;border-radius:50%;background:var(--grass);display:flex;"
            "align-items:center;justify-content:center;font-family:var(--mono);font-size:16px;"
            "letter-spacing:0.05em;color:var(--paper);flex-shrink:0;")
META = ("font-family:var(--mono);font-size:9px;letter-spacing:0.1em;text-transform:uppercase;"
        "opacity:0.45;display:block;margin-top:2px;")

def card(q):
    qid, text, name, initials, meta, _src = q
    return (f'<div class="card card-quote" data-type="quote" data-q-id="{qid}">\n'
            f'    <span class="card-tag" style="position:static;">[Quote]</span>\n'
            f'    <blockquote>&ldquo;{text}&rdquo;</blockquote>\n'
            f'    <div class="quote-row">\n'
            f'      <div class="quote-portrait" style="{PORTRAIT}">{initials}</div>\n'
            f'      <div>\n'
            f'        <cite style="display:block;">&mdash; {name}</cite>\n'
            f'        <span style="{META}">{meta}</span>\n'
            f'      </div>\n'
            f'    </div>\n'
            f'  </div>')

def card_spans(h):
    """(start, end) of every top-level feed card, in feed order."""
    out = []
    for m in re.finditer(r'<div class="card[^"]*"[^>]*data-type="', h):
        st = m.start(); d = 0; j = st
        while True:
            t = re.compile(r'<div\b|</div>').search(h, j)
            if not t: break
            d += 1 if t.group(0) == '<div' else -1
            j = t.end()
            if d == 0: break
        out.append((st, j))
    return out

APPLY  = "--apply"  in sys.argv
REVERT = "--revert" in sys.argv
p = "index.html"
h = open(p, encoding="utf-8").read()
orig = h

if REVERT:
    for st, en in reversed(card_spans(h)):
        if 'data-q-id=' in h[st:en]:
            nxt = re.compile(r'\S').search(h, en)
            h = h[:st] + h[(nxt.start() if nxt else en):]
    print("reverted all data-q-id cards")
else:
    # 1) swap the apocryphal Twain card
    swapped = False
    for st, en in card_spans(h):
        if 'Mark Twain' in h[st:en]:
            h = h[:st] + card(TWAIN_REPLACEMENT) + h[en:]
            swapped = True; break
    print("Twain card replaced with Jack Burke Jr." if swapped else "no Twain card found")

    # 2) pepper the five into the newest stretch, before the old run starts
    spans = card_spans(h)
    first_old_quote = next((i for i,(s,e) in enumerate(spans) if 'data-type="quote"' in h[s:e]
                            and 'data-q-id' not in h[s:e]), len(spans))
    step = max(1, first_old_quote // (len(QUOTES) + 1))
    targets = [ (i+1)*step for i in range(len(QUOTES)) ]
    print(f"newest run is {first_old_quote} cards; inserting at positions {targets}")
    for q, pos in reversed(list(zip(QUOTES, targets))):
        if f'data-q-id="{q[0]}"' in h: continue
        st = spans[pos][0]
        indent = "\n\n  "
        h = h[:st] + card(q) + indent + h[st:]

if APPLY and h != orig:
    open(p, "w", encoding="utf-8").write(h)
print("applied" if APPLY else "DRY RUN — pass --apply to write")
