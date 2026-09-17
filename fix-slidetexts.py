#!/usr/bin/env python3
"""Fill the 14 homepage carousels that declare data-slidetext but have no captions,
and normalise the two arrow glyph styles. 17 September 2026.

WHAT WAS WRONG
--------------
Fourteen feed cards carry <div class="card-text" data-slidetext="KEY"> but KEY has
no entry in window._slideTexts. The carousel handler reads

    if (textEl && window._slideTexts && window._slideTexts[id]) { ... }

so a missing key fails the guard and the block is skipped silently. No error, no
blank card — the card text simply sits static while the images flip. The per-slide
caption feature is dead on those fourteen and nothing on screen says so. That is
about 8% of the carousel cards.

EVERY CAPTION BELOW DESCRIBES THE ACTUAL SLIDE. The slides were read out of
index.html — from .gear-slide-info where the card has an overlay, and from the
image alt text on the four image-only carousels (birdedit, jlindeberg, mackenzie,
whitetee26). Caption N matches slide N. No generic filler: a caption that could
sit under any slide is worse than no caption, because it reads as padding.

Prices and claims here are only those ALREADY PRINTED on the card's own slides —
this script does not introduce a single new fact about a product. Where a slide
overlay states a price, the caption may restate it; where it does not, the caption
does not invent one.

ARROW GLYPHS
------------
190 cards use &#8249;/&#8250; (‹ ›) and 7 use &#8592;/&#8594; (← →). Two arrow
styles in one feed is just an inconsistency from different build eras. The seven
are normalised to the house chevrons. This touches presentation only — the
onclick handlers are left exactly as they are, including the no-space
gearSlide(this,-1) form, which works and is not worth churning.
"""
import re, os, sys, json, subprocess, tempfile

apply_ = "--apply" in sys.argv
ROOT = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(ROOT, "index.html")

CAPTIONS = {
 "apcph": [
  "The jacket that set the tone: a collarless zip shell at roughly $179 that sold out on day one. A.P.C. and Cph/Golf fusing logos meant the drop moved at Paris speed rather than golf speed.",
  "The long-sleeve polo pullover, around $117, with a jacquard collar doing the work a printed one cannot. This is the piece that reads as A.P.C. first and golf second.",
  "The half zip, about $96, with NOT A GOLF GENTLEMAN across it — the clearest statement of intent in the whole eighteen and the reason the collab got written up outside golf.",
  "The all-weather cap at roughly $62, gone in three colourways. Caps are always the first thing to clear in a collab drop and always the last thing anyone regrets buying.",
 ],
 "birdedit": [
  "A Gumtree Golf & Nature Club wooden bird call, worked over a green. The object that started this edit and the one that explains it: golf and birding share the same quiet mornings.",
  "Malbon × Gumtree, the Birds of Georgia fairway polo. Two brands that both understand a motif is only good if somebody drew it rather than clip-arted it.",
  "Radry Golf's Gang Gang driver cover. The loudest bird in the edit and the one most likely to get a comment on the first tee.",
  "A Clint Orms ball marker, the 1600 Quail. Orms is a Texas silversmith and buckle-maker; this is the piece in the edit most likely to outlive everyone reading about it.",
  "Winston Collection's flying mallard headcovers. Traditional sporting art applied to a driver, played entirely straight.",
  "The Gumtree Golf & Nature Club state bird headcover — the field-guide idea turned into something you carry fourteen times a round.",
  "Smathers & Branson's wood duck decoy hat, needlepointed. The most preppy object here and unapologetic about it.",
 ],
 "jlindeberg": [
  "Viktor Hovland on course in J.Lindeberg. The tour presence is the shortest explanation of why a Swedish fashion label has lasted thirty years in golf.",
  "The Pink Strategy campaign — pink cap and trousers against a blurred gallery. J.Lindeberg has always been willing to put colour on a man in a sport that defaults to navy.",
  "The 30Y Devyn golf pant in azalea pink, from the anniversary line. A trouser that would be unremarkable in Stockholm and is still a statement on most tee boxes.",
  "The Finn polo in JL Navy colour block. The one to buy if you want the brand's cut without the brand's volume.",
  "The 30Y Wallis knit polo in white. Knitted rather than jersey, which is the detail that separates it from every other white polo in the pro shop.",
  "The 30Y anniversary cap in black. Thirty years of a label that arrived in golf from outside it and never fully joined.",
 ],
 "lionsdeep": [
  "The 16th at Lions Municipal, established 1924. Hogan's hole, and the one people photograph when they finally come to see what the fuss is about.",
  "The clubhouse, and the 1950 story: two Black golfers played in defiance of Jim Crow, the city let them finish, and Muny became the first integrated course in the South.",
  "Par 71, 5,825 yards. Short on the card and nothing like short in practice — the trees and the angles do the defending.",
  "2901 Enfield Road. Thirty-five dollars on a weekday, dogs welcome, two miles from the Capitol. The most important muni in Texas is still open.",
 ],
 "loudhc": [
  "Mogshade's Deco Magenta at $78, woven in Portugal. Loud because of the colour, not because of a joke printed on it — which is the whole thesis of this edit.",
  "Stitch Golf's Lifesaver Knit at $78, which uses every colour at once and somehow resolves. Knitwear hides bad design badly, so this one earns its noise.",
  "Cayce Golf's Swing Thoughts at $65, hand-lettered. The only cover here where the type is the product.",
  "Devereux's Cactus Voodoo at $48, orange on midnight. The cheapest thing in the edit and the one that will date the slowest.",
 ],
 "mackenzie": [
  "A Fyfe × MacKenzie bag carried through Glen Affric. MacKenzie has spent two decades being the bag other brands want their name on, and this is why.",
  "The same collaboration on a VW Westfalia. Fyfe shoot their bags where people actually take them, which is rarer than it sounds.",
  "MacKenzie bags on a boat deck during Fyfe's Between Tides shoot. Leather and canvas photographed in weather that would ruin most golf marketing.",
  "Sentinel Golf's Sørensen Walker. Sentinel bring the restraint; MacKenzie bring the construction.",
  "Sugarloaf Social Club's White Leather Double Seve. The loudest thing in the archive and still unmistakably a MacKenzie underneath.",
  "Miura × Sentinel, the MacKenzie Walker. Three names on one bag, which usually goes wrong and here does not.",
  "Sugarloaf Social Club's Sail Bag 1492 — sailcloth on a golf bag, and the collab that proves MacKenzie will work outside leather.",
  "Fyfe Golf's 21st Edition in Coastal Tones. A colourway that only makes sense if you have seen a Scottish coast in poor light.",
  "The Bandon Dunes Pacific Dunes edition. Course merch at the top of its form: the bag you buy because of where you played, not what it says.",
 ],
 "manorsrev": [
  "Manors, London, established 2019 — the brand that built its identity on saying nobody needed another technical golf polo.",
  "The Outsider Polartec® polo at $115. Then Polartec went on the label. The rebrand in one garment, and the reason this post exists.",
  "Reebok × Manors, the Club C Revenge, June 2025 at $176. The collab that moved them from golf-adjacent to genuinely crossover.",
  "The knitted baker boy cap at $54 — what survived the rebrand. The pieces that were never about fabric technology are the ones still selling.",
 ],
 "nytrip": [
  "Bethpage Black, walking only. The warning sign at the first tee is not a marketing line and everybody finds that out around the fourth.",
  "Tillinghast, 1936. Golf as far as the eye can see, and a public course that hosts majors for $80-odd if you are a New York resident and willing to sleep in a car park.",
  "The Sedgewood Club, established 1928. Stella, holding the green — the kind of small private course that never appears on a list and is better than most that do.",
  "Union Vale, a Stephen Kay design from 2000. The gem of the trip, and an 84, which felt about right for the week.",
 ],
 "pdnightshift": [
  "Public Drip's herringbone half zip at $140. Brooklyn's muni label going dark for autumn — the pattern does the talking so the logo does not have to.",
  "The Anywhere pleated pants in pinstripe at $170. Pleats and a pinstripe on a golf trouser is either a joke or a thesis; Public Drip mean it.",
  "The Triborough waffle knit polo at $110. Named for the bridge, textured enough to wear off the course without explaining yourself.",
  "The 'P' script denim bucket at $65. The cheapest entry to the collection and the one most likely to end up on somebody else's head.",
 ],
 "summerpractice": [
  "Round Rock Driving Range, lit until 10:30pm. The single most useful fact in Austin golf between June and September — you can hit balls after the heat breaks.",
  "Butler Pitch & Putt, downtown, nine holes of par 3. No polo required, no tee time, and the correct answer to ninety spare minutes.",
  "Golfinity in north-west Austin, 22 simulator bays. When it is 105° the honest move is air conditioning and a launch monitor.",
  "Jimmy Clay and Roy Kizer share a lit range open until 9pm in south-east Austin. Thirty-six holes and a range on one site.",
 ],
 "swagcollege": [
  "Swag Golf's college programme: 62 pieces across 15 schools, with student sections rather than logos as the source material.",
  "Texas, the Hook 'Em fairway at $99.99 — the horns and the words in burnt orange, which is the whole brief executed without a single extra idea.",
  "The Texas Den caddy cooler at $222.22, a staff bag shrunk to cooler size. Already gone, which surprised nobody.",
  "Tennessee's Checkerboard at $99.99 — the Neyland end zone applied straight onto a cover. The most literal design in the run and the best one.",
 ],
 "takomorevisit": [
  "The Skyforger 002 full-face wedge at $99. Takomo built a following on irons at a third of retail; the wedge is where they proved it was not a fluke.",
  "The Ignis D2 fairway wood at $269. Direct-to-consumer pricing on a club category most golfers replace last and should replace first.",
  "The Stand Bag 02 at $279. The clearest signal that Takomo stopped being an iron company — bags are a different business entirely.",
  "The Iron 301 MB at $649, forged muscle back. A blade from a direct brand, which is either confidence or a statement about who they think buys from them.",
  "The Ignis D1 driver at $319, sold out. Drivers are the hardest thing to sell direct and the fastest thing to clear when the price is right.",
 ],
 "techbrands": [
  "Radmor's Cool Jade, spun from recycled stone fibre. The roundup's premise in one fabric: the interesting brands are the ones where the material came first.",
  "Reflo's Java-tek — coffee-infused fibre, which sounds like a gimmick until you read what it does to odour retention.",
  "Manors' Seawool, made with oyster shell yarn. Waste from one industry becoming the selling point of another.",
  "Whim Golf in 100% merino. The oldest technical fabric there is, and still the one most brands are trying to synthesise their way back to.",
 ],
 "whitetee26": [
  "Criquet Shirts' slub cotton pocket tee in natural. Austin-made, and the slub is the point — a flat white tee has nowhere to hide.",
  "Metalwood Studio's Rorschach tee in white. The graphic is the only one in the edit that would work as a poster.",
  "Casualist's Good Enough Tee in off-white. A name that tells you exactly how seriously to take it, on a garment made seriously.",
  "Siegelman Stable's embroidered classic tee in white. Embroidery instead of print, which is the detail that puts it at the top of the price range.",
 ],
}

h = open(P, encoding="utf-8").read()
orig = h
log, problems = [], []


def carousel_span(doc, key):
    """Balanced-div slice of the .gear-carousel element itself.

    NOT a card-boundary slice: slicing from the card to the next 'card-link'
    overruns into the following card, which made takomorevisit look like it had
    nine slides and techbrands eight. The div depth counter is the honest way.
    """
    i = doc.find(f'data-carousel="{key}"')
    if i < 0:
        return None
    s = doc.rfind("<div", 0, i)
    d = 0
    for m in re.finditer(r"<div\b|</div>", doc[s:]):
        d += 1 if m.group(0).startswith("<div") else -1
        if d == 0:
            return doc[s:s + m.end()]
    return None


# ---------------------------------- 1. captions must match slide counts
for key, caps in CAPTIONS.items():
    seg = carousel_span(h, key)
    if seg is None:
        problems.append(f"{key}: carousel not found")
        continue
    n = seg.count('class="gear-slide"')
    if n != len(caps):
        problems.append(f"{key}: {n} slides but {len(caps)} captions")
    if f'data-slidetext="{key}"' not in h:
        problems.append(f"{key}: no card declares data-slidetext for it")

# ---------------------------------------- 2. insert into _slideTexts
k = h.find("window._slideTexts = {")
if k < 0:
    problems.append("could not find the _slideTexts literal")
elif not problems:
    ins = h.index("{", k) + 1
    block = ""
    for key, caps in CAPTIONS.items():
        body = ",\n".join("        " + json.dumps(c, ensure_ascii=False) for c in caps)
        block += f"\n      {key}: [\n{body}\n      ],"
    h = h[:ins] + block + h[ins:]
    log.append(f"{len(CAPTIONS)} caption sets added "
               f"({sum(len(v) for v in CAPTIONS.values())} captions)")

# ------------------------------------------- 3. normalise arrow glyphs
before_old = h.count("&#8592;") + h.count("&#8594;")
h = re.sub(r'(<button class="gear-arrow prev"[^>]*>)&#8592;(</button>)', r"\1&#8249;\2", h)
h = re.sub(r'(<button class="gear-arrow next"[^>]*>)&#8594;(</button>)', r"\1&#8250;\2", h)
after_old = h.count("&#8592;") + h.count("&#8594;")
if before_old:
    log.append(f"arrow glyphs normalised to the house chevrons ({before_old - after_old} swapped)")

# ------------------------------------------------------------- guards
if h.count("<div") != h.count("</div>"):
    problems.append("unbalanced divs")
if h.count("<a ") != h.count("</a>"):
    problems.append("unbalanced anchors")
for tag in ('class="card"', "gear-slide", "data-carousel"):
    if h.count(tag) != orig.count(tag):
        problems.append(f"{tag} count changed — an edit touched the feed markup")
# banned word
for key, caps in CAPTIONS.items():
    for c in caps:
        if re.search(r"\bworth\b", c, re.I):
            problems.append(f"{key}: banned word 'worth' in a caption")

# the literal is JS, not JSON — node is the only honest validator
if k >= 0 and not problems:
    d, end = 0, None
    for j in range(h.index("{", k), len(h)):
        if h[j] == "{":
            d += 1
        elif h[j] == "}":
            d -= 1
            if d == 0:
                end = j
                break
    js = h[k:end + 1].replace("window._slideTexts", "var _st")
    checks = "".join(
        f"if(!_st.{key}||_st.{key}.length!=={len(v)}){{throw new Error('{key} wrong');}}"
        for key, v in CAPTIONS.items())
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as fh:
        fh.write(js + "\n" + checks + "\nconsole.log(Object.keys(_st).length);")
        tmp = fh.name
    r = subprocess.run(["node", tmp], capture_output=True, text=True)
    if r.returncode:
        problems.append("_slideTexts broken — " + r.stderr.strip().splitlines()[-1])
    else:
        log.append(f"_slideTexts parses as JS, {r.stdout.strip()} keys")
    os.unlink(tmp)

# Every declared key must now resolve. The key list has to come from NODE, not a
# regex: pre-existing entries use different indentation from the ones inserted
# above, so a formatting-based regex sees only its own work and reports ~170
# false gaps. Ask the parser what the object actually contains.
if not problems and k >= 0:
    d, end = 0, None
    for j in range(h.index("{", k), len(h)):
        if h[j] == "{":
            d += 1
        elif h[j] == "}":
            d -= 1
            if d == 0:
                end = j
                break
    js = h[k:end + 1].replace("window._slideTexts", "var _st")
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as fh:
        fh.write(js + "\nconsole.log(JSON.stringify(Object.keys(_st)));")
        tmp = fh.name
    r = subprocess.run(["node", tmp], capture_output=True, text=True)
    os.unlink(tmp)
    have = set(json.loads(r.stdout)) if r.returncode == 0 else set()
    declared = set(re.findall(r'data-slidetext="([a-z0-9-]+)"', h))
    gap = sorted(declared - have)
    if gap:
        problems.append(f"still declared with no captions: {gap}")
    else:
        log.append(f"all {len(declared)} declared keys now resolve")

if problems:
    raise SystemExit("REFUSED:\n  " + "\n  ".join(problems))

if apply_:
    open(P, "w", encoding="utf-8").write(h)

print(("applied" if apply_ else "DRY RUN") + f"  ({len(h)-len(orig):+,} bytes)")
for l in log:
    print("  ·", l)
if not apply_:
    print("\npass --apply to write")
