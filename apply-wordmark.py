#!/usr/bin/env python3
"""
apply-wordmark.py — set the masthead in Editor's Note Text caps, sitewide.

WHY (Lenny, 2026-08-29: "stronger more stoic banner font")
----------------------------------------------------------
The wordmark was In The Margins, a hand-drawn marker face. Ten candidates were
rendered at real nav size on paper stock; Lenny chose Editor's Note Text in caps
- already self-hosted, so no new network request, and it ties the masthead to
the body serif.

THE INCONSISTENCY THIS ALSO FIXES
---------------------------------
`index.html` drew the wordmark as an SVG image (assets/logo-wordmark-only.svg,
14 <path>s, no live text). The other 274 pages rendered live text styled with
var(--display). So the homepage masthead and every post masthead were different
objects and could drift apart - as they had. This converts the homepage to the
same live text everyone else uses, so ONE CSS rule now governs all of them.

The SVG is left on disk, unreferenced, so the old mark can be restored.

SCOPE - deliberately narrow
---------------------------
Only `.nav-wordmark` changes. `var(--display)` is NOT touched: it is also used by
`.prog-name` on 24 pages, and repointing the variable would silently restyle those
too. Post titles and body copy are untouched.

Idempotent: re-running reports 0 changes. Writes research/wordmark-inventory.json
(path + size + sha1) before any write, per the house rule after the IBM Plex Mono
revert took SIGBUS and left five files at zero bytes.
"""
import os, re, glob, json, hashlib, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
MARK = "/*TGI-WM-V1*/"

# Caps need more tracking and less size than mixed case to sit at the same
# optical weight next to the mono nav links.
SPEC = ("font-family:var(--serif);font-style:normal;font-weight:700;"
        "font-size:21px;letter-spacing:.085em;text-transform:uppercase;"
        "line-height:1;white-space:nowrap")


def inventory(paths):
    inv = {}
    for p in paths:
        b = open(p, "rb").read()
        inv[os.path.relpath(p, ROOT)] = {"size": len(b),
                                         "sha1": hashlib.sha1(b).hexdigest()}
    os.makedirs(os.path.join(ROOT, "research"), exist_ok=True)
    with open(os.path.join(ROOT, "research", "wordmark-inventory.json"), "w") as f:
        json.dump(inv, f, indent=1)
    return inv


def fix(path, apply_):
    s = open(path, encoding="utf-8", errors="replace").read()
    orig, notes = s, []

    # 1. homepage only: swap the SVG <img> for the same live text every other
    #    page uses, so one rule governs all 275 mastheads.
    m = re.search(r'(<a href="/" class="nav-wordmark">)\s*<img[^>]*>\s*(</a>)', s)
    if m:
        s = s[:m.start()] + m.group(1) + "The Grassy Issue" + m.group(2) + s[m.end():]
        notes.append("homepage: SVG <img> -> live text")

    # 2. replace the .nav-wordmark rule. Match the whole block so we overwrite
    #    whatever spec is there rather than appending a competing one.
    def repl(mm):
        return f".nav-wordmark{{{MARK}{SPEC}}}"

    new, n = re.subn(r"\.nav-wordmark\s*\{[^}]*\}", repl, s, count=1)
    if n and new != s:
        s = new
        notes.append("nav-wordmark -> Editors Note Text caps 700")
    elif n:
        pass  # already correct

    # the homepage carried extra img-sizing rules that now have nothing to size
    s2 = re.sub(r"\.nav-wordmark\s+img\s*\{[^}]*\}", "", s)
    if s2 != s:
        s = s2
        notes.append("dropped .nav-wordmark img rule")

    if s != orig and apply_:
        open(path, "w", encoding="utf-8").write(s)
    return notes


def main(apply_=False):
    paths = [p for p in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)
             if "/drafts/" not in p.replace(os.sep, "/")]
    paths = [p for p in paths if "nav-wordmark" in open(p, encoding="utf-8",
                                                        errors="replace").read()]
    if apply_:
        inventory(paths)
    changed = 0
    for p in paths:
        notes = fix(p, apply_)
        if notes:
            changed += 1
            if len(notes) > 1 or "homepage" in notes[0]:
                print(f"  {os.path.relpath(p, ROOT)}: {'; '.join(notes)}")
    print(f"\n{'updated' if apply_ else 'would update'} {changed} of {len(paths)} pages")
    if not apply_:
        print("(dry run - pass --apply to write)")


if __name__ == "__main__":
    main("--apply" in sys.argv)
