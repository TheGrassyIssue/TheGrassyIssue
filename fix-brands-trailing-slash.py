#!/usr/bin/env python3
"""fix-brands-trailing-slash.py — stop /brands declaring a URL that redirects.
21 September 2026.

FOUND BY indexability-audit.py, which reported two symptoms of one cause:
  "/brands missing from sitemap"  and  "/brands/ in sitemap, no such page".

THE CAUSE. vercel.json sets trailingSlash: false, so Vercel 301s /brands/ to
/brands. But three places still declare the trailing-slash form:
    build-brands.py:316   JSON-LD  "url"
    build-brands.py:341   <link rel="canonical">
    build-brands.py:344   <meta property="og:url">
plus the sitemap entry itself.

WHY IT MATTERS MORE THAN IT LOOKS. A sitemap entry that 301s is untidy; Google
follows it. A self-referencing canonical that points at a redirecting URL is
the real problem — the page tells Google "the canonical version of me lives at
/brands/", Google fetches that and is bounced to /brands, and the two signals
disagree. /brands is the hub we are actively trying to rank for "independent
golf brand directory", so it is the last page that should be sending Google a
contradictory canonical.

THE GENERATOR IS FIXED, NOT THE FILE. brands/index.html is rewritten by
build-brands.py on every run and then restyled by build-brand-index.py.
Editing the HTML would be undone by the next build — the same mistake as
hand-editing post-thumbs.json.

A NOTE ON THE AUDIT THAT FOUND THIS. indexability-audit.py's canonical_self
check does `.rstrip("/")` on both sides, which normalises the trailing slash
away — so that check PASSED this page. It surfaced only through the sitemap
cross-reference. The rstrip is now removed there too, so a future trailing-slash
canonical is caught directly rather than by luck.

Idempotent. Dry run by default.
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
BAD = "https://thegrassyissue.com/brands/"
GOOD = "https://thegrassyissue.com/brands"


def main(apply_):
    gen = ROOT / "build-brands.py"
    g = gen.read_text(encoding="utf-8")
    n = g.count(f'{BAD}"')
    print(f"  build-brands.py: {n} declaration(s) of the trailing-slash form")
    if apply_ and n:
        gen.write_text(g.replace(f'{BAD}"', f'{GOOD}"'), encoding="utf-8")

    sm = ROOT / "sitemap.xml"
    s = sm.read_text(encoding="utf-8")
    hit = f"<loc>{BAD}</loc>" in s
    print(f"  sitemap.xml: {'lists the trailing-slash form' if hit else 'already correct'}")
    if apply_ and hit:
        sm.write_text(s.replace(f"<loc>{BAD}</loc>", f"<loc>{GOOD}</loc>"), encoding="utf-8")

    if not apply_:
        print("\n  dry run — pass --apply")
        return

    print("\n  regenerating /brands through its own chain:")
    for args, label in ((["build-brands.py"], "build-brands"),
                        (["build-brand-index.py", "--apply"], "build-brand-index")):
        r = subprocess.run([sys.executable] + args, cwd=ROOT, capture_output=True, text=True)
        if r.returncode:
            sys.exit(f"! {label} failed:\n{r.stdout[-800:]}{r.stderr[-800:]}")
        tail = [l for l in r.stdout.strip().splitlines() if l.strip()][-1:]
        print(f"    {label}: {tail[0].strip() if tail else 'ok'}")

    # ---- VERIFY THE PUBLISHED PAGE, NOT THE GENERATOR ----
    h = (ROOT / "brands/index.html").read_text(encoding="utf-8")
    bad = []
    cm = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)', h, re.I)
    if not cm:
        bad.append("no canonical on /brands")
    elif cm.group(1) != GOOD:
        bad.append(f"canonical is {cm.group(1)}, expected {GOOD}")
    om = re.search(r'<meta[^>]+property=["\']og:url["\'][^>]*content=["\']([^"\']+)', h, re.I)
    if om and om.group(1) != GOOD:
        bad.append(f"og:url is {om.group(1)}")
    if f'{BAD}"' in h:
        bad.append("the trailing-slash form survives somewhere on the page")
    s2 = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    if f"<loc>{BAD}</loc>" in s2:
        bad.append("sitemap still lists the trailing-slash form")
    if f"<loc>{GOOD}</loc>" not in s2:
        bad.append("sitemap does not list /brands at all")
    if bad:
        sys.exit("! " + "; ".join(bad))
    print(f"\n  verified: /brands canonical, og:url, JSON-LD and sitemap all on {GOOD}")


if __name__ == "__main__":
    main("--apply" in sys.argv)
