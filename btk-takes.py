#!/usr/bin/env python3
"""
btk-takes.py — write a real TGI Take into every Brand to Know spec.
18 September 2026.

WHY
---
Lenny: "The TGI take's need more meat, why we like them, what they are doing
well, who the products are for, etc."

He was right, and the reason was structural. btk-spec.py derives each spec from
the page that already exists, and for the Take it took THE FIRST PARAGRAPH OF
THE EXISTING WRITE-UP. That paragraph is almost always brand history — who
founded it, when, out of which garage. Useful, but it is not a verdict, and it
was already going to be read again thirty seconds later in The Story. Median
length across the 34 specs was 76 words; one was 17.

THE SHAPE, taken from Hiroki — the only hand-written Take on the site
----------------------------------------------------------------------
  1. the verdict        what they are doing well, in our own words
  2. the proof piece     the one product that makes the case, with its price
  3. who it is for       plus the cheapest way to find out if you agree

WHAT IS AND IS NOT INVENTED HERE
---------------------------------
Every FACT below — founders, dates, cities, materials, prices, collaborators,
sold-out counts — is read off the brand's own Brand to Know page, which was
researched and checked when that page was built. What is new is the OPINION
holding those facts together, which is what a Take is and what was missing.

House rules observed: never the word "worth"; no comparisons that put another
brand down; no invented quotes; no price that is not already on the page.

The displaced first paragraph is not lost — it stays in The Story, which is
where it was always going.

USAGE
    python3 btk-takes.py            # dry run, prints each Take and its length
    python3 btk-takes.py --apply
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
SPECS = ROOT / "research" / "btk"

TAKES = {

# The two Brand Revisited-style pages. They were converted after the first 30
# Takes were written, so they were still carrying the derived first paragraph
# — 62 and 41 words against a 118-word average. Same three beats, same rule:
# every fact below is read off the page, the opinion is ours.
"jones-sports-co": [
 "Jones has been making the same bag since 1971 and the restraint is the whole product. No legs, no cart strap, no panelling &mdash; a 2.9 lb carry bag with a three-way divider and an unstructured spine, which is why an Original off the shelf today still looks like the photographs from 1975. The 2011 owners found no patterns, no inventory and no factory, and reverse-engineered the shape from bags borrowed off old customers rather than redrawing it.",
 "The Original at $125 in Burnt Clay is the proof piece. It is the cheapest bag they make and it is the same bag as the $215 Evergreen underneath &mdash; the price difference is material, not construction, which is a rare thing to be able to say about a range.",
 "This is for the walker who wants the bag to disappear and does not need it to do anything else. The line runs $45 to $520 across 32 pieces, so a headcover or a ball pouch is an easy way to test the making before committing to a bag.",
],

"walker-golf": [
 "Walker Golf is built on a specifically Australian relationship to the game &mdash; municipal, unfussy, cheap to join &mdash; and the clothes are cut to match rather than to signal. Jack Fardell competed in the X Games at eleven and rode for adidas before he and co-founder Glenn Walker shipped the first collection in July 2022, and the skate background shows up as fit and restraint, not graphics.",
 "The Par-Tec Quarter Zip Fleece at $110 is the clearest version of it: the house performance fabric is lightweight, stretchy and moisture-wicking, and nothing on the garment announces any of that.",
 "It suits the player who wants to wear the same thing to the muni and the pub afterwards, and who would rather the piece read as clothes than as kit. Twenty-two pieces run $44.95 to $229.95, and a Kooka cap is the cheapest way to see whether the making is for you.",
],

"apres-golf": [
 "What Apr&egrave;s Golf is actually selling is provenance you cannot order twice. The fleece is hi-loft sherpa, hand-sewn in California, but the reason a cover costs $88 is the patch on the front &mdash; Chamonix, St. Moritz, Alta, Mad River Glen &mdash; cut off a ski jacket that someone wore somewhere before it got anywhere near a golf bag.",
 "The Fruit Looper&trade; at $88 is the one to look at first, because it is the clearest version of the trick: a sherpa cover carrying a crest that has nothing to do with golf and somehow belongs on a bag anyway.",
 "This suits the player who likes an object with a history attached and does not want the history to be his own brand&rsquo;s logo. Fifty pieces are in stock across eight groups, and $38 is the cheapest way in.",
],

"birds-of-condor": [
 "Birds of Condor is funny on purpose and designed properly anyway, which is a harder combination than it sounds. Frankie and Zoe Kimpton started with ten hats out of a Byron Bay garage in 2016 and were shipping to South Korea, Japan and the United States within months &mdash; the joke travelled because the making held up.",
 "The Tokyo and Osaka Country Club snapbacks at $50 are the proof. They are gags about clubs that do not exist, executed to the standard of clubs that do.",
 "It is for the player who finds golf&rsquo;s seriousness about itself a bit much, and who would rather the hat say something than say a brand name. The range starts at $15 and runs to $175, so the cost of finding out is small.",
],

"bluegrass-fairway": [
 "Bluegrass Fairway exists because a yardage book cover fell apart and Matt Reynolds took it to a cobbler instead of binning it, and you can still see that decision in the goods. This is a Louisville workshop building in leather, Harris Tweed and waxed canvas at a standard that assumes you are keeping the thing.",
 "The Field in hunter green and cream leather at $115 makes the case: a headcover built like a small piece of luggage rather than a novelty.",
 "It suits the player who replaces gear when it wears out rather than when it bores him. Eighteen pieces run from $68 to $850, and the tweed and canvas covers around the $100 mark are the honest entry point.",
],

"casualist": [
 "The most telling thing about Casualist is what Elie Reboul refused to throw away. He renamed the brand from Casual Pro in 2023 because the name needed to grow up &mdash; and then kept selling the old snapback, which is still the best-seller with the previous name stitched across the front.",
 "The Weekend Pique Polo at &pound;95 is where the grown-up version shows: made in Portugal, cut closer than an American golf polo, plain enough to wear somewhere that is not a golf course.",
 "This is for the player who wants a European cut and does not need the shirt to announce the sport. The range opens at &pound;38 for the hat that started it.",
],

"cloud-and-wind-golf": [
 "Cloud &amp; Wind makes one thing and has thought about it more than most brands think about a whole catalogue. Grips are the only part of the club you actually touch, and they are the cheapest component to change &mdash; a fact the industry treats as a commodity and this brand treats as an opportunity.",
 "Every grip carries a line of Chinese verse printed along the shaft, which is the detail that gives the game away: $18 a grip, and somebody still costed in the poetry.",
 "It is for the tinkerer, and for anyone whose clubs are fine but feel anonymous. Fifteen-plus colourways at $18 each, or $50 for three &mdash; the least expensive way to change how a set feels in your hands.",
],

"devereux-golf": [
 "Devereux is an apparel brand that happens to be famous for headcovers, and it is better to know that going in. Robert Brunner left the gas industry, spent a year at fashion school in Los Angeles and came back with a clothing line; the leather covers are the signature, not the business.",
 "The Devco Twill Jacket at $138 is the piece that shows the training &mdash; cut closer to a work coat than a golf shell, and fine off the course.",
 "It suits desert and shoulder-season golf, and the player who wants the round to be one part of the day rather than an outfit change. Twenty-six pieces run $18 to $248.",
],

"edel-golf": [
 "Edel sells a method, and the putter is what the method produces. A fitter clips a mirror to the face, sets a laser six feet away and asks you to aim &mdash; then takes the ball away and fires it, and shows you that where you were pointed is nowhere near where you believed. Head shape, hosel and top lines get swapped until the eye and the face agree. Feel is discussed last, which is the opposite of how putters are usually sold.",
 "The Array putters at $699 are that process made physical, and the $400 &ldquo;Brick&rdquo; is the same thinking at a lower number.",
 "This is for the player who misses on the same side every week and has never been told why. Wedges start at $140 if you want to meet the shop before committing to the putter.",
],

"forden-golf": [
 "Forden knows exactly who it is dressing and does not hedge. The graphics are in-jokes about the muni, the scorecard and the putt left short; the cuts are boxy cotton and heavyweight fleece rather than anything technical. Nothing in the range is trying to get you past a starter who would ask what you shot.",
 "The Swingman mark is the tell &mdash; it comes from Harold Edgerton&rsquo;s 1938 strobe photography, which is a more considered reference than the price list suggests.",
 "It is for the player whose home course has a chain-link fence and a good hot dog. The whole range runs $14 to $77, and the $14 tee picks are as low-stakes as an introduction gets.",
],

"fyfe-golf": [
 "Fyfe started as a complaint: Neil Rennie kept walking into Scottish pro shops and finding nothing in them that had anything to do with Scotland. The answer is a Fife workshop making to order in Harris Tweed, Scottish tartan and waxed canvas from Dundee &mdash; and, several times a year, in something that used to be an RAF flight suit, a caddie&rsquo;s coverall or a yacht sail.",
 "The Arran at &pound;65 is the everyday version of the idea; the upcycled runs are the reason to keep an eye on the site.",
 "This is for the player who wants the cover to come from somewhere specific. Thirty-two pieces are in stock, twenty-three of them headcovers.",
],

"gamut-golf": [
 "Gamut makes headcovers out of things that already existed, and the sourcing is what separates it. The baseball covers are cut from authentic vintage jerseys, several marked 1 of 1. The course covers are cut from genuine towels &mdash; Shinnecock, Pebble Beach, the Old Course, Sawgrass, Pinehurst.",
 "A $128 cover built from a Cooperstown Collection throwback is not a print of a jersey; it is the jersey, which is why the same cover cannot be made twice.",
 "It suits the player who wants one object in the bag nobody else can order. Twenty-five pieces run $22 to $128, and the hardwood alignment sticks at $98 are the sleeper.",
],

"gramicci": [
 "Gramicci is not a golf brand, which is exactly why it works for golf. Mike Graham designed the original climbing pant in 1982 for big walls in Yosemite &mdash; integrated webbing belt, gusseted crotch, full range of motion &mdash; and those three decisions turn out to describe a good walking trouser better than most things sold as one.",
 "The G-Short at $70 is the piece to start with: the climbing pattern cut short, in cotton that breathes in July.",
 "This is for the player who walks munis in real heat and would rather not be dressed as a golfer while doing it. Eighteen pieces, with the UPF tops from $53.",
],

"hidden-links-society": [
 "The ratio is the story here. Hidden Links Society sells about thirty products and is documenting a hundred golf courses, and that is a lopsided way to run a clothing brand &mdash; which is the point. The catalogue is good on its own terms: real weight in the brass, an overshirt heavier than it needs to be, headcovers made in Oregon.",
 "But the Public 100 project is what the shop is funding, and the 2% is accounted for rather than implied.",
 "It suits the player who wants the purchase to point at something beyond the purchase. Eighteen pieces run $20 to $82.",
],

"huega-house": [
 "Huega House solved fit before it solved anything else, which is why it grew the way it did. Jonathan Ruley and Jake Ryan &mdash; the latter a former Green Bay linebacker &mdash; split $10,000 in 2022 because neither could find a hat that sat right, and reached $2.3 million in annual revenue by mid-2024 without venture money.",
 "The Athletics Hat at $45 is the one that did it: a rope-free, low-drama cap that holds shape through a wet round.",
 "This is for the player who has a drawer of hats that nearly work. Thirty pieces run $22 to $88, and the name &mdash; from the Danish hygge &mdash; tells you the register they are aiming for.",
],

"kingfisher-golf": [
 "Kingfisher treats a shirt like a design brief rather than a merchandise run, which follows from where it came from: Fiona Cohen spent years as an art director at PepsiCo specialising in animation and motion design before starting a golf label in Dallas.",
 "The tees are screen-printed at Lewellyn&rsquo;s in Old East Dallas and the polos come off the same lines as performance shirts you already own &mdash; the $40 Golfmobile Tee is the clearest piece of the thinking.",
 "It is for the player who wants the graphic to be good rather than loud. The brand&rsquo;s breakout was a city-wide search for the worst golfer in Dallas, which tells you the tone better than a lookbook would.",
],

"left-of-field-golf": [
 "Left of Field is the funniest brand in golf that also makes clothes you would wear without the joke attached, and both halves matter. Nick Ilias started it in his brother&rsquo;s old bedroom in Sydney in 2022, out of a frustration a lot of players share &mdash; that dressing for golf felt like choosing between looking wrong on the course and looking wrong everywhere else.",
 "The Elements Polo at $105 is the serious end of the range and the reason the humour lands elsewhere.",
 "This suits the player who wants a wardrobe with a sense of humour and a straight face available when needed. Thirty-nine pieces across eight collections, from $4 to $330.",
],

"metalwood-studio": [
 "Metalwood is art-directed first and merchandised second, and Cole Young has never pretended otherwise. The design language runs on medieval heraldry and industrial signage, which sounds like a stretch until you see it lined up &mdash; it is the most internally consistent visual identity in independent golf.",
 "The Tri-Metal Tee at $54 is the entry point; the Mechanic Jacket at $278 is the argument.",
 "It is for the player who cares what the clothes look like on a hanger, not only at address. The adidas partnership and a La Brea Avenue store are the receipts that the point of view is travelling. Thirty-six pieces run $16 to $278.",
],

"midiron": [
 "Midiron writes better than anyone else in golf and will not tell you who is doing it &mdash; no founder name, no photograph, no byline. What is on the site is a line about a grandad&rsquo;s hand-me-down Titleist cap, lowercase and unsigned, and then the brand went and found vintage Titleist caps, had a Melbourne studio rework three, gave one away and sold the other two.",
 "The Tour Spec Cap at A$69 (about US$49) is the everyday version of that sensibility.",
 "This is for the player who reads the product page. Nine pieces exist, seven releases so far, A$69 to A$129 &mdash; a small catalogue held to an unusually high standard of attention.",
],

"mogshade": [
 "Mogshade makes to order, which is the whole ethic rather than a delivery inconvenience. Nothing is overproduced because nothing is produced until it is bought, and the fabrics are natural, recycled, upcycled, offcut or deadstock &mdash; including rescued wool from the Serra da Estrela mountain factories.",
 "The Churra Mono headcover at &euro;84 is built on that rescued wool and is the piece that explains the name, an old dialect word for light and shadow moving through leaves.",
 "It suits the player who would rather wait three weeks for something made for him than have it tomorrow from a warehouse. The Contour towel at &euro;39 is the low-commitment way in.",
],

"odd-ritual": [
 "Odd Ritual rewrites golf culture from the Southern Hemisphere, and the name says how. It is taken from the small private habits every player has before a shot &mdash; the waggle, the alignment check, the tap on the ball mark &mdash; which is a warmer idea of the game than the one the founders found in Cape Town when they went looking for a local brand that spoke to them.",
 "The 1990s Heritage Polo at roughly $102 is the clearest piece: period cut, current fabric, no irony.",
 "This is for the player who likes the game and not the gatekeeping. Thirty-one pieces run from about $11 to $176.",
],

"quiet-golf": [
 "Quiet Golf is the rare brand whose name is an accurate spec. Christion Lennon came from Museum of Peace &amp; Quiet and built this with Raul and Diego Diaz around the idea that golf clothing can be considered without being loud &mdash; the owl crest, the QG monogram and the pennant are all there, and none of them shouts.",
 "The Jagger Polo at $114 in active pique is the piece that carries it, cut for the course and fine in a restaurant afterwards.",
 "It suits the player who wants good fabric and no branding to explain. Twenty-four pieces, from a $50 Pro Shop Tee up to cashmere, with a Costa Mesa flagship if you want to feel it first.",
],

"radry-golf": [
 "The smiley face on a Radry hat is not a smiley face, and once Tony Knapton tells you what it is you cannot unsee it. One eye is a circle for birdies, the other a square for bogeys, and the wave where the mouth should be is the up and down of a round &mdash; a logo about coming to terms with the game rather than winning it.",
 "The Gang Gang covers at $65 are the most direct expression; the numbered runs mean the good ones do not come back.",
 "This is for the player who finds golf psychologically funny. Thirty pieces run $18 to $3,900, and a $55 tee is the cheapest way to test the sense of humour.",
],

"random-golf-club": [
 "Random Golf Club is a community that happens to run a pro shop, and buying from it is closer to joining than to shopping. Erik Anders Lang and Evan Roosevelt started it in 2017 to change who golf is for; the first meetup was eleven strangers playing ten holes in Melbourne, and there are now 30,000 members across 140 chapters.",
 "The RGC Sans Serif Dad Hat at $35 is the one you will actually see on a course, and it functions as a handshake.",
 "It suits the player who travels and would rather not play alone. The range runs $20 to $249, and the events &mdash; the Mad Scramble Tour, the Classics &mdash; are the real product.",
],

"read-the-green": [
 "Read The Green began as three words shouted across a miniature golf course and became a hat brand with genuine range. Four lifelong friends built it, and the discipline shows in how little has been added: caps first, then a small apparel line that earned its place rather than padding the catalogue.",
 "The Founder&rsquo;s Cap at $47 is the signature &mdash; five-panel corduroy, embroidered, with a custom interior lining most people never see.",
 "This is for the player who wants a good hat that moves between the course and the city without a costume change. The range runs $40 to $150, and the &rsquo;97 Vintage Pullover is the piece that put them on the map.",
],

"rouqe-golf": [
 "Rouqe does 1974 club-pro styling better than any label its size, and the proof is which pieces are missing rather than which are in stock. Twelve of the twenty-one men&rsquo;s pieces have sold out, and the loudest went first &mdash; the burgundy and cream rugby stripe, the black long-sleeve with cream banding, the houndstooth.",
 "The mock neck is the silhouette everything is built on, cut in six colours at fifty-nine dollars, in a category where most brands default to a polo.",
 "It suits the player who wants period styling without period fabric. Fifty-four products across men&rsquo;s and women&rsquo;s, $19 to $199 CAD.",
],

"sentinel-golf": [
 "Sentinel is a product design lab that happens to make golf equipment, and John Mooty staffs it by calling in favours outside the game &mdash; a Danish tannery, a Nashville chair company, a Brooklyn machine shop, tent-pole engineers in South Korea. The reference point is not golf; it is the Boundary Waters.",
 "The Basecamp Walker in black Dyneema at $890 is the clearest statement: a carry bag engineered the way an outdoor brand engineers a tent.",
 "This is for the walker who already owns serious outdoor gear and has noticed golf bags are not built to that standard. The model is limited pre-order &mdash; no restocks, no discounts &mdash; so the $98 SCOUT is the low-risk introduction.",
],

"siegelman-stable": [
 "Siegelman Stable&rsquo;s heritage is real rather than borrowed, which is rarer than it should be. Max&rsquo;s father Robbie founded Siegelman Racing Stable in 1982 and trained harness racehorses for decades; the horse-and-sulky mark on the clothing is the family&rsquo;s actual logo, not a mood board reference.",
 "The Short Sleeve Harness Shirt at $258 is the piece where the racing language and the golf shirt genuinely meet.",
 "It suits the player who wants the story behind the garment to survive being asked about. Max&rsquo;s first job was caddying, the Maxfli collaboration runs under &ldquo;Harness the Drive&rdquo;, and the range spans $48 to $780.",
],

"sugarloaf-social-club": [
 "Sugarloaf runs the widest price range in independent golf and holds one point of view across all of it &mdash; a MacKenzie sailcloth bag at $1,400 and a paper fan at $14 read as the same company, which is genuinely hard to do.",
 "It started as a group chat between college roommates in 2011, named after the course they had spent four years on; Ian Gilley filed the LLC in 2017.",
 "This is for the player who follows projects rather than seasons. Thirty-three are catalogued, from THE PLAYERS work to the caddie scholarship, and the &ldquo;Major&rdquo; Stripe Sport Polo at $95 is the piece most likely to be in stock when you look.",
],

"sun-mountain": [
 "Sun Mountain invented the bag with legs and four decades later still makes the lightest way to walk a golf course. Rick Reimers quit a club pro job in 1981 and designed a bag in his head on the drive to Montana because the car radio was broken &mdash; the nylon carry bag that resulted weighed less than half what leather and vinyl bags did.",
 "The Matchplay Swift Sunday at $315 is the modern descendant of that first idea, and the Legacy Leather at $1,200 is the other end of the same catalogue.",
 "It suits anyone who walks, and particularly anyone who has been talked into riding by the weight of their bag. Eighteen picks run $35 to $1,200.",
],

"takomo-golf": [
 "Takomo&rsquo;s argument is the price, and it holds up because nothing else about the clubs is a compromise. Launched in 2021 out of Turku, Finland, it designs the heads, partners with established foundries and ships direct &mdash; no pro shop margin, no retail middleman, and the saving goes to the tag.",
 "A set of forged S20C cavity backs at $649 is the headline, and the 101 MKII took MyGolfSpy&rsquo;s Best Game Improvement Iron.",
 "This is for the player who wants forged irons and has been quietly priced out of them. The Skyforger wedge at $99 is the cheapest way to hold the build quality before committing to a set.",
],

"twentyfour-golf": [
 "TwentyFour is a cap brand that added clothes, and reading the catalogue in that order makes it make sense: eighteen of its twenty-four products are hats, and the six garments sit on top of a cap line that is almost permanently sold out.",
 "The OG Camo Cap went live on 15 January 2025 and the digital camo on it has become the closest thing the brand has to a signature, turning up since on a thermal and a second colourway.",
 "It suits the player who buys hats seriously and clothes occasionally. Eleven pieces are buyable today, A$55 to A$130, and the Motion Polo at A$110 is where the apparel side is strongest.",
],

}


if __name__ == "__main__":
    apply_ = "--apply" in sys.argv
    n = 0
    for slug, paras in sorted(TAKES.items()):
        f = SPECS / f"{slug}.json"
        if not f.exists():
            print(f"  SKIP {slug} — no spec"); continue
        d = json.loads(f.read_text(encoding="utf-8"))
        old = sum(len(re.sub(r"<[^>]+>", "", p).split()) for p in d.get("take", []))
        new = sum(len(re.sub(r"<[^>]+>", "", p).split()) for p in paras)
        # THE OLD TAKE IS NOT DELETED. It was the first paragraph of the page's
        # own write-up; it belongs in The Story, so it goes back to the front of
        # story_extra rather than off the page.
        if apply_:
            # RUN THIS TWICE AND IT USED TO EAT ITSELF. On the second run
            # d["take"] is already the hand-written Take, so "the old paragraph"
            # was the NEW one — and it got prepended to The Story, printing the
            # Take twice on the page. Thirty specs did exactly that before the
            # check below caught it. A paragraph that IS the new Take is never
            # displaced copy, so it never moves.
            keep = [p for p in d.get("take", [])
                    if p not in d.get("story_extra", []) and p not in paras]
            d["story_extra"] = keep + d.get("story_extra", [])
            d["take"] = paras
            f.write_text(json.dumps(d, indent=1, ensure_ascii=False) + "\n",
                         encoding="utf-8")
        print(f"  {slug:<24} take {old:>3} -> {new:>3} words"
              + ("   (old para moved into The Story)" if apply_ else ""))
        n += 1
    print(f"\n  {n} Take(s) " + ("written" if apply_ else "ready — pass --apply"))
