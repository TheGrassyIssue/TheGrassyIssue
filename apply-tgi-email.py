#!/usr/bin/env python3
"""apply-tgi-email.py — move public contact points to the TGI address.
22 September 2026.

Lenny: "I also now have a dedicated email - Lenny@thegrassyissue.com".

The site was handing brands a personal Gmail. /work-with-us says "Email is best,
and it reaches one person rather than an inbox" and then prints an @gmail.com
address; the brand index has a "a brand for the Index" mailto; /about, the Field
Guide, the homepage footer and the Social Club page all carry the same one. With
seeding emails about to go out to six brands, the address on the receiving end
is part of the pitch.

BOTH THE PAGES AND THE BUILDERS. Four scripts regenerate these pages —
build-work-with-us.py, build-social-club.py, build-brand-index.py and
add-about-link.py — and each has the Gmail baked in. Changing only the HTML
would hold until the next rebuild and then quietly revert, which is the failure
mode that put a stale hero on two brand pages earlier this month.

THE NEWSLETTER FORM IS DELIBERATELY NOT TOUCHED, AND THAT IS THE WHOLE POINT OF
THIS COMMENT. index.html posts signups to

    https://formsubmit.co/ajax/l4harrington@gmail.com

FormSubmit delivers to an address only after that address has confirmed itself
once, by clicking a link in an activation email. Repointing the endpoint would
therefore stop signups reaching anyone until Lenny completes that step — and the
handler ends in `.catch(() => {})` and shows the success message regardless, so
the form would look like it was working while every signup went nowhere. A
silent failure on the one form that collects readers is not a change to make on
someone's behalf. It is listed at the end as a thing for Lenny to do, in order.

Idempotent. Dry run by default.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
OLD_RE = re.compile(r"[Ll]4harrington@gmail\.com")
NEW = "Lenny@thegrassyissue.com"
# Anything matching this keeps the old address. One entry, one reason.
KEEP = [("formsubmit.co", "newsletter endpoint — needs FormSubmit activation first")]

TARGETS = [
    "index.html", "about.html", "work-with-us.html",
    "brands/index.html", "field-guide/index.html", "events/social-club.html",
    "build-work-with-us.py", "build-social-club.py", "build-brand-index.py",
    "add-about-link.py",
]


def protected(line):
    return any(k in line for k, _ in KEEP)


def swap(text):
    """Replace on a per-line basis so protected lines can be excluded."""
    out, changed, kept = [], 0, 0
    for line in text.splitlines(keepends=True):
        if OLD_RE.search(line):
            if protected(line):
                kept += len(OLD_RE.findall(line))
                out.append(line)
                continue
            line, n = OLD_RE.subn(NEW, line)
            changed += n
        out.append(line)
    return "".join(out), changed, kept


def main(apply_):
    total_c = total_k = 0
    results = []
    for rel in TARGETS:
        p = ROOT / rel
        if not p.is_file():
            sys.exit(f"! missing target: {rel}")
        t = p.read_text(encoding="utf-8")
        new, c, k = swap(t)
        total_c += c
        total_k += k
        results.append((rel, c, k, new != t))
        if apply_ and new != t:
            p.write_text(new, encoding="utf-8")

    for rel, c, k, ch in results:
        flag = "" if not k else f"   ({k} kept: {KEEP[0][1]})"
        print(f"  {rel:<28}{c} swapped{flag}")
    print(f"\n  {total_c} replaced, {total_k} deliberately left")

    if not apply_:
        print("\n  dry run — pass --apply")
        return

    # ---- VERIFY ----
    bad = []
    for rel in TARGETS:
        t = (ROOT / rel).read_text(encoding="utf-8")
        for line in t.splitlines():
            if OLD_RE.search(line) and not protected(line):
                bad.append(f"{rel}: gmail survived on an unprotected line")
                break
    # the form endpoint must be intact and still point at the confirmed address
    idx = (ROOT / "index.html").read_text(encoding="utf-8")
    if "formsubmit.co/ajax/l4harrington@gmail.com" not in idx:
        bad.append("newsletter endpoint was changed — signups would silently stop")
    # no half-formed addresses
    for rel in TARGETS:
        t = (ROOT / rel).read_text(encoding="utf-8")
        if re.search(r"Lenny@thegrassyissue\.com[a-zA-Z0-9.]", t):
            bad.append(f"{rel}: malformed address after replacement")
    # mailto subjects must have survived intact
    wu = (ROOT / "work-with-us.html").read_text(encoding="utf-8")
    if "?subject=Working%20with%20The%20Grassy%20Issue" not in wu:
        bad.append("work-with-us mailto lost its subject line")
    bi = (ROOT / "brands/index.html").read_text(encoding="utf-8")
    if "?subject=A%20brand%20for%20the%20Index" not in bi:
        bad.append("brand index mailto lost its subject line")
    # builders and their output must now agree
    for builder, page in (("build-work-with-us.py", "work-with-us.html"),
                          ("build-social-club.py", "events/social-club.html"),
                          ("build-brand-index.py", "brands/index.html")):
        b = (ROOT / builder).read_text(encoding="utf-8")
        pg = (ROOT / page).read_text(encoding="utf-8")
        if NEW in pg and NEW not in b:
            bad.append(f"{page} updated but {builder} would revert it")

    if bad:
        sys.exit("! " + "\n    ".join(bad))
    print(f"\n  verified: {total_c} contact points on {NEW}, builders match their pages,\n"
          f"  newsletter endpoint untouched")
    print("\n  STILL ON THE OLD ADDRESS, ON PURPOSE:")
    for k, why in KEEP:
        print(f"    {k} — {why}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
