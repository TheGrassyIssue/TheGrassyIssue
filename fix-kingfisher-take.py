#!/usr/bin/env python3
"""fix-kingfisher-take.py — new middle paragraph for the Kingfisher TGI Take,
plus two factual errors found next to it. 22 September 2026.

Lenny: "i really don't like the write up in the kingfisher post ... I like the
tee, just not the idea we have, let's swap it out."

THE IDEA THAT WAS WRONG. The old middle paragraph ran:

    "The tees are screen-printed at Lewellyn's in Old East Dallas and the polos
     come off the same lines as performance shirts you already own — the $40
     Golfmobile Tee is the clearest piece of the thinking."

Two things are off. "the polos come off the same lines as performance shirts you
already own" is a put-down of Kingfisher's own polos dressed as an observation —
it tells a reader the polos are generic blanks, which is not something TGI says
about a brand it is recommending. And "the clearest piece of the thinking" is an
abstraction where the paragraph's job is to show the design background of
paragraph one actually landing on a product. The replacement describes the
graphic, because the graphic is the argument.

THE GRAPHIC IS NOT A GOLF CART. The product card on this same page said
"Line-drawn golf cart graphic on white." It is a golfer in shorts finishing his
swing on the roof of an old American two-door, in tall grass, under clouds and a
sun — checked by opening the image rather than reading the card. A "Golfmobile"
is a car; that is the joke, and the page was describing the wrong vehicle.

THE SIDEBAR PRICES WERE STALE, ON A PAGE THAT CLAIMS THEY ARE NOT. The body
says the catalogue "was repriced — polos now $65, tees $40, caps $36 ... Prices
updated throughout." The sidebar still read Polos $56, Tees $35–$36, Caps
$25–$30. Read live off kingfisher-golf.com on 22 September 2026: polos $45–$65,
tees $22–$40, caps $30–$36. The $22 is the Worst Golfer in Dallas Tee; the $9
Golf Tee Box is not apparel and is excluded.

NOT TOUCHED, DELIBERATELY — flagged for Lenny instead:
  · drops/the-summer-tee-edit.html still prices this tee at $30. That post is
    dated 17 June 2026 and does not date its prices, and it covers ten brands.
    Correcting one of ten silently would leave the other nine equally stale and
    the post internally inconsistent. It needs a pass of its own.
  · index.html carries two IG-caption strings with the same "$30" and "vintage
    golf cart" errors. Same argument: that is caption copy with its own history.

Idempotent. Dry run by default.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
POST = ROOT / "drops/brand-to-know-kingfisher-golf.html"
SRC = ROOT / "btk-takes.py"
EMAIL = ROOT.parent / "seeding-emails-2026-09-21.md"

OLD_TAKE = ("The tees are screen-printed at Lewellyn&rsquo;s in Old East Dallas and the "
            "polos come off the same lines as performance shirts you already own &mdash; "
            "the $40 Golfmobile Tee is the clearest piece of the thinking.")
# V1 NARRATED THE PICTURE. Lenny: "let's tone down the description, people can
# see what's on the Tee. It's cool because its high-quality and simple, it's the
# blend of high/low." He is right — the tee is photographed four frames down the
# same page, so describing the golfer, the clouds and the grass spends the
# paragraph on something the reader can already see. The idea is the high/low
# blend: a considered drawing on an ordinary shirt. "Built for frequent wear" is
# Kingfisher's own phrase, from the Function pillar on their about page.
TAKE_V1 = ("What that background buys is on the back of the $40 Golfmobile Tee: a golfer "
           "in shorts finishing his swing on the roof of an old American two-door, clouds "
           "above him, tall grass round the wheels. Navy line on white, no wordmark, and "
           "it reads from across a car park &mdash; which is what a motion designer means "
           "by a graphic that works.")
NEW_TAKE = ("The $40 Golfmobile Tee is where that lands. One navy illustration, "
            "screen-printed at Lewellyn&rsquo;s in Old East Dallas, and nothing else on "
            "the shirt. The drawing is the considered part and the tee under it is built "
            "for frequent wear, which is the high-low blend the brand keeps getting right.")

OLD_CARD = "Line-drawn golf cart graphic on white. The boxy streetwear cut the brand does best."
CARD_V1 = ("A golfer teeing off from the roof of an old two-door, drawn in navy line on "
           "white, with a smaller print on the chest. The boxy streetwear cut the brand "
           "does best.")
NEW_CARD = ("One navy illustration, front and back, on white. The boxy streetwear cut the "
            "brand does best.")

# (label, old sidebar value, new value read live 22 Sep 2026)
PRICES = [("Polos", "$56", "$45&ndash;$65"),
          ("Tees", "$35&ndash;$36", "$22&ndash;$40"),
          ("Caps", "$25&ndash;$30", "$30&ndash;$36")]

# THE EMAIL HAD THREE PROBLEMS, NOT ONE.
#  1. It quoted "the clearest piece of the thinking" — a line that no longer
#     exists on the page, so a brand clicking through would not find it.
#  2. The v1 fix replaced that with a description of the print, which is the
#     same narration Lenny cut from the post.
#  3. THE COVERAGE COUNT: I broke a correct number twice. The draft said
#     "eight times". I changed it to 21 (every post containing the word), Lenny
#     said count posts not mentions, so I changed it to 4 (my own title-or-card
#     heuristic). Both were wrong, and the site already had the answer:
#     data/brand-mentions.json is what renders "Every Grassy Issue Post
#     Featuring Kingfisher Golf" on the brand page. It says 8 — which is what
#     the draft said in the first place. Sugarloaf is 24, not the 44 I put in.
#     Any brand can see this list on the brand page, so the email must match it.
#     Never hand-roll a count the site already publishes.
#  3b. Superseded reasoning kept for the record: It said "eight times"; I changed that
#     to 21, which was every post where the word "Kingfisher" appears. Lenny:
#     "we should only be counting the posts, not the individual mentions." A
#     name-drop in a roundup is not a post about a brand.
#
#     THE RULE NOW: a post counts if the brand is in its title OR the post
#     carries a product card for that brand. Passing mentions do not count.
#     On that basis, 22 Sep 2026: Kingfisher is featured in 4 posts (Brand to
#     Know, Brand to Watch, the Hat & Towel Edit, the Summer Tee Edit) out of 21
#     that name it. Sugarloaf is featured in 25 of 44. Both emails now use this
#     rule, so a brand comparing notes gets the same arithmetic.
EMAIL_ASK_OLD = [
    ("> The ask: the Golfmobile Tee — our own write-up calls it the clearest piece "
     "of the thinking, so it seems like the one to actually photograph."),
    ("> The ask: the Golfmobile Tee — the one with the golfer swinging off the roof "
     "of the car on the back. It's the piece of yours I'd most like to photograph "
     "properly."),
]
EMAIL_ASK_NEW = ("> The ask: the Golfmobile Tee. One navy illustration on a good white tee "
                 "and nothing else going on, which is the piece of yours I'd most like to "
                 "photograph properly.")

EMAIL_BITS = []   # counts are handled by the guard below, from the canonical source


# THE SAME BAD IDEA APPEARS FOUR TIMES, AND IT IS UNSOURCED. "the polos come from
# the same factory teams behind the big-brand shirts you already own" is not just
# deflating — it is a manufacturing claim Kingfisher does not make. Their about
# page, read 22 September 2026, says nothing about factories or partners. What it
# does state is a third principle alongside Fashion and Function: "Affordability
# — Because you should never have to choose between buying a shirt and playing a
# round." That is their framing of the same fact, in their words, and it is true.
#
# "Everything under $56" is also now false in five places, two of them inside the
# FAQ schema. Live on 22 Sep 2026: tees $22–$40, polos $45–$65, caps $30–$36.
BULK = [
    ("Everything under $56.",
     "Everything sits between $22 and $65."),
    ("Everything stays under $56.",
     "Everything sits between $22 and $65."),
    # APOSTROPHES ARE MIXED ON THIS PAGE. "Lewellyn's" appears as a straight
    # quote in the FAQ and as &rsquo; in the take paragraph, so a single literal
    # pattern matched three of four places and silently missed the rest. These
    # are matched by regex on the apostrophe and re-emitted in the straight form
    # the surrounding FAQ text already uses.
    ("Tees are screen-printed at Lewellyn's Print Shop in Old East Dallas, and the "
     "performance polos come from the same factory teams behind the big-brand shirts you "
     "already own.",
     "Tees are screen-printed at Lewellyn's Print Shop in Old East Dallas. The brand "
     "lists affordability beside fashion and function as one of its three stated "
     "principles &mdash; in its own words, you should never have to choose between buying "
     "a shirt and playing a round."),
    ("The polos are produced by the same factory teams behind the big-brand performance "
     "shirts you already own.",
     "The polos carry the same stated principle as the rest of the range: affordability "
     "sits beside fashion and function on the brand&rsquo;s own about page."),
]


def sub_once(text, old, new, label):
    """Converge on `new` from the original text OR from an earlier revision.

    `old` may be a single string or a list of accepted prior forms, so re-running
    after a copy revision moves v1 to v2 instead of reporting "already current"
    and leaving the superseded wording on the page.
    """
    olds = old if isinstance(old, (list, tuple)) else [old]
    if new in text and not any(o in text for o in olds):
        return text, False
    for o in olds:
        if text.count(o) == 1:
            return text.replace(o, new, 1), True
    counts = {o[:28]: text.count(o) for o in olds}
    sys.exit(f"! {label}: no prior form found exactly once — {counts}")


def main(apply_):
    changed = []

    post = POST.read_text(encoding="utf-8")
    post, c1 = sub_once(post, [OLD_TAKE, TAKE_V1], NEW_TAKE, "post take paragraph")
    post, c2 = sub_once(post, [OLD_CARD, CARD_V1], NEW_CARD, "post product card")
    for label, old, new in PRICES:
        pat = f'<span class="l">{label}</span><span>{old}</span>'
        rep = f'<span class="l">{label}</span><span>{new}</span>'
        post, c = sub_once(post, pat, rep, f"sidebar {label}")
        changed.append((f"sidebar {label}", c))
    changed = [("take paragraph", c1), ("product card", c2)] + changed

    for old, new in BULK:
        n = post.count(old)
        if n:
            post = post.replace(old, new)
            changed.append((f"x{n} {old[:34]}...", True))
        elif new not in post:
            sys.exit(f"! bulk pattern not found and replacement absent: {old[:50]}")

    src = SRC.read_text(encoding="utf-8")
    src, c3 = sub_once(src, [OLD_TAKE, TAKE_V1], NEW_TAKE, "btk-takes source")
    changed.append(("btk-takes.py", c3))

    mail = EMAIL.read_text(encoding="utf-8")
    mail, c4 = sub_once(mail, EMAIL_ASK_OLD, EMAIL_ASK_NEW, "seeding email ask")
    changed.append(("email ask", c4))
    for old, new in EMAIL_BITS:
        if new in mail and old not in mail:
            changed.append((f"email: {old[:26]}...", False)); continue
        n = mail.count(old)
        if n != 1:
            sys.exit(f"! email bit found {n}x, expected 1: {old[:46]}")
        mail = mail.replace(old, new, 1)
        changed.append((f"email: {old[:26]}...", True))

    for what, c in changed:
        print(f"  {what:<22}{'changed' if c else 'already current'}")

    if not apply_:
        print("\n  dry run — pass --apply")
        return

    POST.write_text(post, encoding="utf-8")
    SRC.write_text(src, encoding="utf-8")
    EMAIL.write_text(mail, encoding="utf-8")

    # ---- VERIFY ON THE FINISHED FILES ----
    bad = []
    p = POST.read_text(encoding="utf-8")
    plain = re.sub(r"<[^>]+>", " ", p)
    if "come off the same lines as performance shirts" in p:
        bad.append("old take paragraph survived")
    if "golf cart" in p.lower():
        bad.append("'golf cart' still on the page")
    if NEW_TAKE not in p:
        bad.append("new take paragraph did not land")
    # the builder must produce what the page now shows, or a rebuild reverts it
    if NEW_TAKE not in SRC.read_text(encoding="utf-8"):
        bad.append("btk-takes.py would revert the page")
    # sidebar and body must now agree
    for label, _, new in PRICES:
        if f'<span class="l">{label}</span><span>{new}</span>' not in p:
            bad.append(f"sidebar {label} not updated")
    # CHECK THE SIDEBAR SPANS, NOT A BARE STRING. The first version failed on
    # "$56" appearing anywhere, and $56 was still legitimately in body copy at
    # the time — the guard flagged a correct sidebar. Read the actual fields.
    for label, _, new in PRICES:
        if f'<span class="l">{label}</span><span>{new}</span>' not in p:
            bad.append(f"sidebar {label} is not {new}")
    if "under $56" in p:
        bad.append("an 'under $56' claim survived — polos now reach $65")
    if "same factory teams" in p:
        bad.append("the unsourced factory claim survived")
    # banned word, and the take must still be three paragraphs
    if re.search(r"\bworth\b", plain, re.I):
        bad.append("banned word in the page")
    # THE TAKE IS BOUNDED BY ITS OWN PARAGRAPHS, NOT BY </section>. The first
    # version searched from data-btk="take" to the next </section>, which is
    # 16,000 characters away at the end of the sidebar, so it counted six
    # paragraphs from all over the page and failed a correct edit.
    for label, frag in (("opener", "Kingfisher treats a shirt like a design brief"),
                        ("new middle", "the high-low blend the brand keeps getting right"),
                        ("closer", "the graphic to be good rather than loud")):
        if p.count(frag) != 1:
            bad.append(f"take {label} paragraph appears {p.count(frag)} times, expected 1")
    m = EMAIL.read_text(encoding="utf-8")
    if "clearest piece of the thinking" in m:
        bad.append("seeding email still quotes the deleted line")
    if "golfer swinging off the roof" in m:
        bad.append("email still narrates the print")
    if "Strongest of the six" in m:
        bad.append("email header still says six")
    # "eight" is CORRECT — data/brand-mentions.json has 8. An earlier guard here
    # failed the draft for using it, which is how a right number got replaced
    # twice with wrong ones.
    # the email must not cite a post count the site cannot back
    import subprocess
    # EVERY COUNT IN THE EMAILS MUST MATCH data/brand-mentions.json, which is the
    # file that renders the "Every Grassy Issue Post Featuring <brand>" list on
    # each brand page. A brand can open that page and count the cards.
    import json as _json
    mn = _json.loads((ROOT / "data/brand-mentions.json").read_text(encoding="utf-8"))
    WORDS = {8: "eight", 24: "24"}
    kf, sl = len(mn["kingfisher-golf"]), len(mn["sugarloaf-social-club"])
    if f"Kingfisher {WORDS.get(kf, kf)} times" not in m:
        bad.append(f"Kingfisher email count does not match brand-mentions ({kf})")
    if f"Sugarloaf turns up in {sl} posts here" not in m:
        bad.append(f"Sugarloaf email count does not match brand-mentions ({sl})")
    for stale in ("21 pieces here", "44 pieces here", "44 TGI posts", "four posts"):
        if stale in m:
            bad.append(f"email still carries a hand-rolled count: {stale!r}")

    if bad:
        sys.exit("! " + "\n    ".join(bad))
    print("\n  verified: take rewritten, card corrected, sidebar matches the live store,\n"
          "  builder matches the page, email no longer quotes a line that does not exist")
    print("\n  STILL WRONG ELSEWHERE — needs its own pass:")
    print("    drops/the-summer-tee-edit.html  — Golfmobile Tee at $30 (now $40), 10 brands undated")
    print("    index.html IG captions          — '$30' and 'vintage golf cart'")


if __name__ == "__main__":
    main("--apply" in sys.argv)
