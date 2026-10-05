#!/usr/bin/env python3
"""strip-outlet-names.py — keep other golf review/media outlets' names out of TGI copy.

4 October 2026. Lenny: "No mentioning by name to any other golf review sites", then "yes" to cleaning every
existing page the same way: keep the quote or the fact, drop the outlet's name.

Applies a fixed table of pattern -> replacement to the rendered pages AND to the builder sources / data files
that hold the same text, so a rebuild cannot bring a name back. Safe to re-run (patterns no longer match once
fixed). Dry run by default.

Deliberately NOT touched (the outlet is the product or the subject, not a source being cited):
  - products sold by Fried Egg Golf (towel, tees, poster, Fried Egg x Seamus cover, Fried Egg Golf Club trips)
  - the-magazine-edit.html, which is a guide to golf media outlets themselves
  - No Laying Up, which is a brand with its own page in the Brand Index
"""
import glob, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
AP = r"(?:&rsquo;|&#x27;|&#39;|’|')"
S = r"\s+"
def q(t):
    """plain text -> regex tolerant of entity apostrophes and wrapped whitespace"""
    out = ""
    for ch in t:
        if ch == "'": out += AP
        elif ch == " ": out += S
        else: out += re.escape(ch)
    return out

O = r"(?:MyGolfSpy|Golf Digest|Golf Monthly|Global Golf Post|Golf Today|GolfWRX)"
RULES = [
 # quote credits: "— X, to OUTLET, 2025" / "via OUTLET" / "as quoted by OUTLET"
 (r",\s+(?:to|via|as quoted by)\s+" + O + r",\s+", ", "),
 (q("told Golf Digest in 2017 that"), "said in 2017 that"),
 (q("told Golf Digest in 2023 that"), "said in 2023 that"),
 (q("Carnahan told Golf Digest there was"), "Carnahan has said there was"),
 (q("Carnahan told Golf Digest the company"), "Carnahan has said the company"),
 (q("he told GolfWRX in October 2017"), "he said in October 2017"),
 # reviews and awards: keep the finding, drop the outlet
 (q("MyGolfSpy called it among the most comfortable gloves it tested."), "One independent glove test called it among the most comfortable it tried."),
 (q("and MyGolfSpy called the Palm glove among the most comfortable it tested."), "and one independent glove test called it among the most comfortable it tried."),
 (q("and MyGolfSpy made it a staff pick in its 2026 push cart testing."), "and it was a staff pick in one major 2026 push cart test."),
 (q("and the 101 MKII took MyGolfSpy's Best Game Improvement Iron."), "and the 101 MKII won a Best Game Improvement Iron award."),
 (q("that won MyGolfSpy's Best GI Iron"), "that won a Best Game-Improvement Iron award"),
 (q("MyGolfSpy's Best Game-Improvement Iron."), "Award-winning game-improvement iron."),
 (q("won MyGolfSpy's Best GI Iron award"), "won a Best Game-Improvement Iron award"),
 (q("MyGolfSpy scored the Compete irons 8.8, best for accuracy and best value in their class"), "One independent test scored the Compete irons 8.8, best for accuracy and best value in their class"),
 (q("Plugged In Golf found it"), "One independent review found it"),
 (q("Golf Monthly called it very stable"), "One independent review called it very stable"),
 (q("MyGolfSpy named it the best game-improvement iron of 2026"), "It was named the best game-improvement iron of 2026 in one major test"),
 (q("It finished third in MyGolfSpy's 2023 players' iron test and took its best-value award."), "It finished third in one major 2023 players' iron test and took its best-value award."),
 (q("Plugged In Golf called it one of the best buys in golf"), "One independent review called it one of the best buys in golf"),
 (q("Plugged In Golf found spin"), "One independent review found spin"),
 (q("MyGolfSpy's 2023 test had it long but inconsistent"), "One 2023 independent test had it long but inconsistent"),
 (q("It took Silver on Golf Digest's 2026 Hot List"), "It took Silver on a major 2026 equipment Hot List"),
 (q("Golf Monthly found the feel soft"), "One independent review found the feel soft"),
 (q("Golf Monthly saw impressive dispersion"), "One independent review saw impressive dispersion"),
 (q("Plugged In Golf called it an excellent short-game tool"), "One independent review called it an excellent short-game tool"),
 (q("Takomo's 101 MKII was MyGolfSpy's best game-improvement iron of 2026, and Edel's SMS Pro wedge took Silver on Golf Digest's 2026 Hot List."), "Takomo's 101 MKII was named the best game-improvement iron of 2026 in one major test, and Edel's SMS Pro wedge took Silver on a major 2026 Hot List."),
 (q("In April 2023 MyGolfSpy reported that David Edel"), "In April 2023 it was reported that David Edel"),
 (q("MyGolfSpy reported at the time that he"), "It was reported at the time that he"),
 (q("Walking a writer through a session for Plugged In Golf,"), "Walking a writer through a fitting session,"),
 (q("and Golf Monthly names it the best aid for clubface control."), "and one major training-aid test names it the best for clubface control."),
 (q("Golf Monthly made it its top training aid of 2026,"), "It was named one major review's top training aid of 2026,"),
 (q("Golf Monthly calls it the best aid for swing path."), "One major training-aid test calls it the best for swing path."),
 (q("Adapted from Luke Kerr-Dineen's The Easiest Way To Break 80 on Golf Digest's The Game Plan, which uses Arccos data and Lou Stagner's research."), "Adapted from Luke Kerr-Dineen's The Easiest Way To Break 80, which uses Arccos data and Lou Stagner's research."),
 (q("Golf Monthly gave it an Editor's Choice."), "It has won an Editor's Choice award."),
 (q("9.6/10 MyGolfSpy."), "9.6/10 in independent testing."),
 (q("#5 in MyGolfSpy testing."), "#5 in independent glove testing."),
 (q("Best for most walkers per MyGolfSpy 2026."), "Best for most walkers in a major 2026 test."),
 (q("Co-best push cart of 2026 (MyGolfSpy)."), "Co-best push cart of 2026 in a major test."),
 (q("MyGolfSpy Staff Most Wanted three years running."), "A staff Most Wanted pick in a major test three years running."),
 (q("MyGolfSpy tested trail runners against spikeless golf shoes"), "An independent test put trail runners against spikeless golf shoes"),
 (q("with MyGolfSpy calling the collab"), "with one review calling the collab"),
 (q("Golf Digest put the price at $1,275 in its first look."), "The price was reported at $1,275 at launch."),
 (q("and it is the one Golf Digest singled out."), "and it is the one the golf press singled out."),
 (q("Golf Digest, on the Savannah, as quoted by Hudson Sutler"), "A golf magazine review of the Savannah, as quoted by Hudson Sutler"),
 (q("is the lightest and the one Golf Digest praised."), "is the lightest and the one reviewers praised."),
 (q("Golf Digest featured the brand."), "The golf press picked it up."),
 (q("Golf Digest has featured the brand's headwear,"), "The golf press has featured the brand's headwear,"),
 (q("Golf Digest has featured the brand's headwear."), "The golf press has featured the brand's headwear."),
 (q("Manors ambassador Adem Wahbi told Golf Digest in 2023 that"), "Manors ambassador Adem Wahbi said in 2023 that"),
 (q("GolfMagic named it one of ten up-and-coming brands for 2026 back in December, describing"), "One golf site named it one of ten up-and-coming brands for 2026 back in December, describing"),
 (q("Golf Digest cover story for a reason."), "Magazine cover story for a reason."),
 (q("(ranked top 35 in Golf Digest)"), "(ranked in the top 35 by a national golf magazine)"),
 # rankings: keep the ranking, drop the publisher
 (q("is Golfweek's #1 public course in Texas"), "is ranked the #1 public course in Texas"),
 (q("Golfweek ranks Black Jack's Crossing the #1 Course You Can Play in Texas and #38 Resort Course in the"), "it is ranked the #1 Course You Can Play in Texas and #38 Resort Course in the"),
 (q("Golfweek ranks Black Jack's Crossing the number one course you can play in Texas and #38 resort course in the"), "Black Jack's Crossing is ranked the number one course you can play in Texas and #38 resort course in the"),
 (q("which the Dallas Morning News and Golfweek have both named one of the best in Texas"), "which the Dallas Morning News has named one of the best in Texas"),
 (q("and The Dallas Morning News and Golfweek have both named it one of the best courses in Texas"), "and The Dallas Morning News has named it one of the best courses in Texas"),
 # Golf Digest's Top 100 Public list (Hidden Links Society's project)
 (q("documenting Golf Digest's Top 100 Public courses one at a time"), "documenting a national Top 100 Public list one course at a time"),
 (q("every course on Golf Digest's Top 100 Public list"), "every course on a national Top 100 Public list"),
 (q("every course on Golf Digest 's Top 100 Public list"), "every course on a national Top 100 Public list"),
 (q("The ranking is Golf Digest's and they say so; the project is theirs."), "The ranking belongs to a magazine and they say so; the project is theirs."),
 (q("the courses on Golf Digest's Top 100 Public list"), "the courses on a national Top 100 Public list"),
 (q("working through Golf Digest's Top 100 Public list"), "working through a national Top 100 Public list"),
 # business and background facts
 (q("an Instagram account that at one point had more followers than Golf Digest"), "an Instagram account that at one point had more followers than some of the big golf magazines"),
 (q("and also owns Skratch and GolfWRX"), "and also owns Skratch and other golf media"),
 (q("Pro Shop also owns Skratch and GolfWRX."), "Pro Shop also owns Skratch and other golf media."),
 (q("Created by Golf Digest lead digital talent Hally Leadbetter."), "Created by golf media personality Hally Leadbetter."),
 (q("Partners with The Fried Egg and Shotgun Start podcasts."), "Partners with golf podcasts."),
 (q("the idea came home from a Fried Egg Golf trip"), "the idea came home from a golf trip"),
 (q("Mike Harris, a former editor of Golf Monthly,"), "Mike Harris, a former editor of a leading UK golf magazine,"),
 (q("ahead of Plugged In Golf, Hoodline and What Now Austin."), "ahead of three other outlets."),
 # Australia trips post: which other media/apparel outfits run trips
 (q("The rest of the field sits it out: No Laying Up, Fried Egg, The Golfer's Journal, Bob Does Sports, Good Good, Skratch, and a dozen clothing labels from Manors to Malbon to Eastside."), "The rest of the field sits it out: the big golf media names, and a dozen clothing labels from Manors to Malbon to Eastside."),
 (q("Fried Egg has a deposit system and a calendar published a year ahead, and points its entire international pro"), "One golf media outfit has a deposit system and a calendar published a year ahead, and points its entire international pro"),
 (q("We checked No Laying Up, Fried Egg Golf, The Golfer's Journal, Bob Does Sports, Good Good and Skratch, plus a dozen apparel labels"), "We checked the big golf media and creator names, plus a dozen apparel labels"),
 (q("Fried Egg publishes its calendar through September 2027 with a deposit system already built, and its entire i"), "One golf media outfit publishes its calendar through September 2027 with a deposit system already built, and its entire i"),
 (q("</a> on Golf Digest's The Game Plan, which uses"), "</a>, which uses"),
 (q("Best push cart for most walkers per MyGolfSpy 2026."), "Best push cart for most walkers in a major 2026 test."),
 (q("documenting all 100 of Golf Digest's top public courses"), "documenting all 100 courses on a national top public list"),
 (q("every course on <em>Golf Digest</em>'s Top 100 Public list"), "every course on a national Top 100 Public list"),
 (q("The rest of the field sits it out: No Laying Up, Fried Egg, The Golfer's Journal, Bob Does Sports, Good Good, Skratch, and a dozen clothing labels from"), "The rest of the field sits it out: the big golf media names, and a dozen clothing labels from"),
 (r"won MyGolfSpy\\u2019s Best GI Iron award", "won a Best Game-Improvement Iron award"),
 (q("The DTC brand that won MyGolfSpy's Best Game-Improvement Iron"), "The DTC brand that won a Best Game-Improvement Iron award"),
 (q("Named by GolfMagic as a 2026 up-and-comer."), "Named a 2026 up-and-comer."),
 (q("both have made Golf Digest's 100 Greatest Public list"), "both have made a national 100 Greatest Public list"),
 (q("The shoe bag Golf Digest called probably the coolest you can buy."), "The shoe bag one golf magazine called probably the coolest you can buy."),
 (r"MyGolfSpy named the Finnish brand(?:\\'|'|&rsquo;|’)s hollow-body 101 MKII its top game-improvement iron of 2026\.", "The Finnish brand's hollow-body 101 MKII was named the top game-improvement iron of 2026 in one major test."),
 (r"Finished #5 in MyGolfSpy(?:\\'|'|&rsquo;|’)s 2025 glove test\.", "Finished #5 in a major 2025 glove test."),
 (q("Robert Rock's strap, Golf Monthly's top aid of 2026."), "Robert Rock's strap, a top-rated aid of 2026."),
 (q("led by a former Golf Monthly editor."), "led by a former UK golf magazine editor."),
]
SKIP = {"drops/the-magazine-edit.html"}

def files():
    out = [p for p in glob.glob(str(ROOT / "**/*.html"), recursive=True)]
    out += glob.glob(str(ROOT / "*.py")) + glob.glob(str(ROOT / "data/*.json")) + glob.glob(str(ROOT / "research/*.json"))
    for p in out:
        rel = pathlib.Path(p).relative_to(ROOT).as_posix()
        if " " in rel or rel.startswith(("drafts/", ".git")) or rel in SKIP or rel == "strip-outlet-names.py" or "before" in rel:
            continue
        yield p, rel

def main(apply_):
    total = 0; changed = []
    for p, rel in files():
        try: s = open(p, encoding="utf-8").read()
        except Exception: continue
        new = s; n = 0
        for pat, rep in RULES:
            new, k = re.subn(pat, rep, new); n += k
        if n:
            total += n; changed.append((rel, n))
            if apply_: open(p, "w", encoding="utf-8").write(new)
    for rel, n in changed: print(f"  {n:3d}  {rel}")
    print(f"  {total} replacements in {len(changed)} files" + ("" if apply_ else " (dry run — pass --apply)"))

if __name__ == "__main__":
    main("--apply" in sys.argv)
