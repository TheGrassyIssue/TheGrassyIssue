#!/usr/bin/env python3
"""Refresh the homepage Vibe Board from Lenny's own Pinterest board.

SOURCE. https://pin.it/2UlGtqukc resolves to
pinterest.com/l4harrington/golf-vision-board — Lenny's public board, 60 pins.
The board page itself is virtualised and renders almost nothing to the DOM, so
the pins came from Pinterest's own public RSS feed for the board
(/l4harrington/golf-vision-board.rss), which returns the 25 most recent. Those
25 were downloaded, contact-sheeted, and looked at before anything was chosen.

WHAT WENT IN — 15 pins, replacing all 15 currently on the board.

WHAT DELIBERATELY DID NOT, and why it is a judgement call and not an oversight:
seven of the 25 are press or agency photographs of named, recognisable golfers
(Tiger in the green jacket, John Daly mid-swing, Calvin Peete, a Kevin Costner
"Tin Cup" publicity still whose frame still carries the Warner Bros. caption
strip and a distributor phone number). They are the most charismatic images on
the board and they are also the ones TGI has the least business republishing on
its own server. The existing Vibe Board has never carried a face; it is
landscape, gear and texture. Keeping it that way is both the safer call and the
more consistent one. Also skipped: the bare "The Masters" wordmark (pin 11),
which is a trademark and not a vibe.

If Lenny wants any of them anyway, the downloads are keyed by pin index and the
swap is a one-line change to PICKS.

NAMING follows the existing convention exactly: an 8-hex prefix, a hyphen, then
Pinterest's own image hash. Do not invent a different scheme — the localiser
that produced the current filenames used this one and the audit scripts assume
it.

Images are localised to /images/feed/ at the same sizes as their neighbours.
Never hot-link i.pinimg.com.
"""
import json, os, re, shutil, sys, hashlib

SRC = "/tmp/pins"                       # the 25 downloads, indexed 00..24
DEST = "images/feed"
apply_ = "--apply" in sys.argv

# (pin index, pinimg hash, alt text, overlay caption)
PICKS = [
 (0,  "a78b1374692375238795520beb73115c",
  "Shingled clubhouse on the hill above a green ringed by sandy waste bunkers",
  "Clubhouse hill"),
 (1,  "3118c7d8ab69fbf7611f3a46b78d4968",
  "Rows of folded green caddie bibs stacked and numbered before a tournament",
  "Bib stack"),
 (3,  "bb35364af78e8800a0ddfd79f2f400fe",
  "Dark saturated green with a white flag and two cloverleaf bunkers cut into it",
  "Flag down"),
 (5,  "453bb79fc9fff7b467cf3f6c966e0e5b",
  "Illustrated hole diagram showing a narrow dogleg lined with drawn trees",
  "On paper"),
 (8,  "028c5e8b1bb1020a1df027084be8f2ad",
  "Flat graphic illustration of a golf hole in layered greens with white bunkers",
  "Drawn green"),
 (10, "773a85f84039deae4dab385bc006edce",
  "Vintage leather Sunday bag with a patterned strap leaning against a bar stool",
  "Bar lean"),
 (14, "1d95c4b05dfd70aa146118c6925b87be",
  "Tweed and stitched leather headcovers beside forged irons in a canvas carry bag",
  "Cover set"),
 (15, "e015d14dec4bf78a78dbc852e3e01984",
  "Walker with a carry bag reflected in still water on a course at first light",
  "Mirror water"),
 (16, "e5375f118efa417bde7924a7d8c1a4a1",
  "Loaded golf cart with bags and brightly coloured headcovers stacked in the back",
  "Full cart"),
 (17, "e23e0ea940846953d8c9f37a3f93979c",
  "Canvas and leather Sunday bag laid down in rough grass with a navy towel clipped on",
  "Down in it"),
 (18, "b6bc58ba422a910df87be9635b9108de",
  "Orange carabiner clipped through a woven green webbing belt on a pale background",
  "Clip on"),
 (19, "54128b27230d63846c466add08329674",
  "Engraved orange line illustration of a fist gripping a dagger wrapped by a snake",
  "Snake work"),
 (20, "0572d24661f8c10bd054b05053002f20",
  "Golfer seen from behind carrying a black stand bag with a printed towel hanging off it",
  "Walk on"),
 (23, "ce98fa77edbbeac980d6fc119b0a520e",
  "Bright shop interior with clothing rails, a centre table of folded knits and globe pendants",
  "Front of house"),
 (24, "6b56656438f2be6f462a33b15ccf4e94",
  "Shop interior with a pale wood counter, open shelving and a wall of framed prints",
  "Counter goods"),
]

# ---------------------------------------------------------------- sanity gates
if len(PICKS) != 15:
    raise SystemExit(f"the board holds 15 pins; this build has {len(PICKS)}")
if len({p[1] for p in PICKS}) != 15:
    raise SystemExit("two picks share an image hash — no duplicate pins on the board")
if len({p[3] for p in PICKS}) != 15:
    raise SystemExit("two picks share an overlay caption")
for idx, h, alt, cap in PICKS:
    if len(cap) > 18:
        raise SystemExit(f"caption {cap!r} is too long for the overlay chip")
    if len(alt) < 40:
        raise SystemExit(f"alt text for pin {idx} is too thin to be useful: {alt!r}")
    if re.search(r"\bworth\b", alt, re.I) or re.search(r"\bworth\b", cap, re.I):
        raise SystemExit("banned word 'worth'")
# The faces stay off. Guard the four press photos by hash so a future edit that
# pastes one back in has to delete this check on purpose rather than by accident.
PRESS = {"560dc3a5a55fd69c5b1bba7a28ed3b3f": "John Daly, agency photo",
         "fb01b3bebbeab7ef60273e5ff053f212": "Masters/Instagram repost",
         "e990f566da825f2f03af336178c30d0e": "Tin Cup publicity still (caption strip visible in frame)",
         "11f72acf74cbbde7fb2faa1eb7b69885": "Calvin Peete, agency photo",
         "8196fb87c1ceda7a24a1c31f33afe4ea": "The Masters wordmark — a trademark, not a vibe"}
for _i, h, _a, _c in PICKS:
    if h in PRESS:
        raise SystemExit(f"{h} is {PRESS[h]} — see this file's docstring before re-adding")

# ------------------------------------------------------------------ localise
notes, pins = [], []
for idx, h, alt, cap in PICKS:
    src = os.path.join(SRC, f"{idx:02d}.jpg")
    if not os.path.exists(src):
        raise SystemExit(f"missing download {src} — re-run the pin fetch first")
    prefix = hashlib.sha1(h.encode()).hexdigest()[:8]
    name = f"{prefix}-{h}.jpg"
    dest = os.path.join(DEST, name)
    if apply_:
        shutil.copy2(src, dest)
    pins.append((f"/{DEST}/{name}", alt, cap))
    notes.append(f"{idx:02d} -> {name}  [{cap}]")

BLOCK = "".join(
    f'''    <div class="vibe-pin">
      <img src="{u}" alt="{a}" loading="lazy" />
      <div class="vibe-overlay"><span>{c}</span></div>
    </div>
''' for u, a, c in pins)

# ------------------------------------------------------------------- rewrite
h_ = open("index.html", encoding="utf-8").read()
m = re.search(r'(<section class="vibe-board">.*?<div class="vibe-grid">\n)(.*?)(  </div>\n</section>)',
              h_, re.S)
if not m:
    raise SystemExit("could not locate the vibe-grid block in index.html")
old = m.group(2)
old_imgs = re.findall(r'src="([^"]+)"', old)
new = h_[:m.start(2)] + BLOCK + h_[m.end(2):]

_npins = new.count('class="vibe-pin"')
if _npins != 15:
    raise SystemExit(f"result has {_npins} pins, expected 15")
if len(re.findall(r'<section class="vibe-board">', new)) != 1:
    raise SystemExit("the vibe-board section got duplicated")
for u, _a, _c in pins:
    if new.count(f'src="{u}"') != 1:
        raise SystemExit(f"{u} appears more than once in the page")

if apply_:
    open("index.html", "w", encoding="utf-8").write(new)
    print(f"vibe board refreshed: {len(old_imgs)} pins -> 15")
else:
    print("DRY RUN — pass --apply")
    print(f"  would replace {len(old_imgs)} pins with 15")
for n in notes:
    print("  ·", n)
print("\n  retired (files left on disk, nothing else references them):")
for u in old_imgs:
    print("     ", u.split("/")[-1])
