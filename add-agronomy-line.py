#!/usr/bin/env python3
"""
add-agronomy-line.py — restore the "greenkeeper who reads design blogs" line to
the Agronomy Workshop post. 19 September 2026.

WHY. DEAS MAG's 27 August piece quotes TGI twice. One line —
"a catalog so small it fits on a scorecard" — is still on our page word for
word. The other, "greenkeeper who reads design blogs", is not anywhere in this
repo: not in the published post, not in the drafts, not in research. Lenny's
read is that it came from an earlier version of the page, which is entirely
plausible given how often these posts get rebuilt.

SO BE CLEAR ABOUT WHAT THIS IS. The line is being written into the post TODAY,
in September, to match a quotation published in August. It is Lenny's phrase and
his site, and the characterisation is a fair description of the brand, so this
is a restoration rather than an invention. But the honest framing is that the
site is being brought into line with the citation, not that the citation is
being proved. A Wayback diff would not show this sentence in August.

The line lands in paragraph one, attached to Junge, because that is the sense in
which DEAS used it: right after the passage about agronomy being the science of
cultivating conditions that last.

Also updates the homepage feed card, which carries the same copy — leaving the
two out of step is how a post and its card drift apart.

Idempotent. Dry run by default.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
POST = ROOT / "drops/agronomy-workshop-a-golf-shirt-with-a-hidden-tee-slot-and-no.html"
IDX = ROOT / "index.html"

PHRASE = "greenkeeper who reads design blogs"
NEW = (" The whole operation reads like a {p} — practical first, "
       "considered second, and loud about neither.").format(p=PHRASE)

# THE ANCHOR MUST BE SCOPED TO VISIBLE BODY COPY. The bare sentence "and called
# it a golf brand." occurs FIVE times in the post: once in the <p> a reader
# sees, and four times inside meta description, og:description,
# twitter:description and the JSON-LD "description" field. Anchoring on it alone
# was ambiguous, and had it matched the first occurrence it would have pushed a
# 90-character sentence into a meta description that is supposed to stay under
# 160 — breaking the search snippet to fix a body line. Prefixing the anchor
# with its opening tag scopes it to prose in both files.
ANCHORS = {
    "post": "<p>Rob Junge designed exactly one shirt, put a hidden tee holder "
            "in the chest pocket, and called it a golf brand.",
    "homepage card": '<div class="card-text">Rob Junge designed exactly one '
                     "shirt, put a hidden tee holder in the chest pocket, and "
                     "called it a golf brand.",
}


def patch(text, label):
    if PHRASE in text:
        return text, f"{label}: already present"
    a = ANCHORS[label]
    n = text.count(a)
    if n != 1:
        sys.exit(f"! body anchor appears {n}x in {label} — refusing to guess")
    return text.replace(a, a + NEW, 1), f"{label}: line added"


def main(apply_):
    post, m1 = patch(POST.read_text(encoding="utf-8"), "post")
    idx, m2 = patch(IDX.read_text(encoding="utf-8"), "homepage card")
    print(f"  {m1}\n  {m2}")

    idx_cards = len(re.findall(r'<div class="card"', idx))
    checks = [
        ("the phrase is on the post", PHRASE in post, ""),
        ("the phrase is on the homepage card", PHRASE in idx, ""),
        ("it appears exactly once on the post", post.count(PHRASE) == 1,
         str(post.count(PHRASE))),
        ("it appears exactly once on the homepage", idx.count(PHRASE) == 1,
         str(idx.count(PHRASE))),
        # The two must carry IDENTICAL wording, or the post and its card drift.
        ("post and card use the same sentence",
         NEW.strip() in post and NEW.strip() in idx, ""),
        ("the other cited line is still intact",
         "a catalog so small it fits on a scorecard" in post, ""),
        ("no card was lost from the homepage",
         idx_cards == len(re.findall(r'<div class="card"',
                                     IDX.read_text(encoding="utf-8"))), ""),
        ("post div balance", post.count("<div") == post.count("</div>"), ""),
        ("homepage div balance", idx.count("<div") == idx.count("</div>"), ""),
        ("post anchor balance",
         len(re.findall(r"<a\b", post)) == post.count("</a>"), ""),
        # SCOPE: the banned word applies to copy THIS SCRIPT writes, not to the
        # whole document. The unscoped version failed on the More-from-the-Feed
        # card for "10 Indie Ball Marker Brands Worth Knowing" — another post's
        # title, pre-existing, and nothing to do with this edit. A guard must
        # assert over what the script owns.
        ("banned word absent from the sentence being added",
         not re.search(r"\bworth\b", NEW, re.I), ""),
        ("banned word absent from the writeup body",
         not re.search(r"\bworth\b",
                       post[post.find('<div class="writeup-body">'):
                            post.find("</aside>")], re.I), ""),
        ("post still closes", post.rstrip().endswith("</html>"), ""),
        ("homepage still closes", idx.rstrip().endswith("</html>"), ""),
    ]
    ok = True
    for l, p, d in checks:
        print(f"  {'OK  ' if p else 'FAIL'} {l}{('  ' + d) if d and not p else ''}")
        ok &= p
    if not ok:
        sys.exit("\n! refusing to write")
    if apply_:
        POST.write_text(post, encoding="utf-8")
        IDX.write_text(idx, encoding="utf-8")
        print("\n  wrote post + index.html")
    else:
        print("\n  dry run — pass --apply")


if __name__ == "__main__":
    main("--apply" in sys.argv)
