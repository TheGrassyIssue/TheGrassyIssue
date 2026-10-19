#!/usr/bin/env python3
"""apply-muny-deal-2026-10.py — bring the Field Guide and the Lions deep dive up to date
with the October 14, 2026 City/UT announcement on Lions Municipal. 19 October 2026.

Lenny: "update the guide" ... "with links". Both pages said Muny was still living on short
lease extensions / "still waiting on a lease". Sources, all linked on the page:
  CITY      City of Austin release, Oct 14 2026 (ownership to the City via amendments to the 1989
            Brackenridge Development Agreement; Council briefing, amended BDA to Council Nov 19;
            regulating plan + TIRZ back to Council spring 2027; 1950 integration; 75,000 rounds/yr).
  STATESMAN Austin American-Statesman, Oct 14 2026 (anonymous donors would help the city buy the
            141-acre course; still needs city and university approval).
  GOLFWEEK  Golfweek, Oct 15 2026 (deal brokered by the Muny Conservancy).
Patches the live HTML and build-lions.py together so a rebuild keeps the update.
Idempotent: every edit checks for its marker first. Dry run by default; --apply writes.
--one <file> runs a single file (prove-one-then-batch).
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent
CITY = "https://www.austintexas.gov/communications/news/city-austin-and-ut-close-agreement-preserve-muny"
STATESMAN = "https://www.statesman.com/news/local/article/austin-ut-deal-to-preserve-muny-golf-course-22476968.php"
GOLFWEEK = "https://golfweek.usatoday.com/story/sports/golf/courses/2026/10/15/austin-historic-golf-course-ben-crenshaw-lions-municipal/92268087007/"
LS = ' target="_blank" rel="noopener" style="border-bottom:1px solid var(--ink)"'
def a(url, text): return f'<a href="{url}"{LS}>{text}</a>'

# ---------- Field Guide ----------
FG = [
 ("Ben Crenshaw and Tom Kite learned here. One of the first courses in the South to desegregate, in 1951 — years before Brown v. Board. It sits on UT land that's been quietly fought over for a decade; \"save the Muny\" is a sincere Austin cause.",
  "Ben Crenshaw and Tom Kite learned here. In 1950 it became the first public course in the South to integrate, four years before Brown v. Board. It sits on UT land that Austin fought over for more than 50 years, and on October 14, 2026 the city and UT announced a proposed deal to give the city ownership and keep Muny public for good. City Council is scheduled to vote on November 19 (" + a(CITY, "the city&rsquo;s announcement") + "). <!--MUNY-DEAL-26-->"),
 ("to the Coore &amp; Crenshaw restoration that has been offered to the Muny for free and is still waiting on a lease, there's always something happening in Austin golf.",
  "to the October 2026 deal that would finally make the Muny city-owned (" + a(STATESMAN, "Statesman") + "), there's always something happening in Austin golf.<!--MUNY-DEAL-26-->"),
 ("The first integrated course in the South, a lease running on short extensions, and a Coore &amp; Crenshaw restoration offered for free and still waiting. Go play it.",
  "The first integrated course in the South, a proposed deal to make it city-owned for good, and a Coore &amp; Crenshaw restoration offered for free. Go play it.<!--MUNY-DEAL-26-->"),
]

# ---------- Lions deep dive (live HTML and builder) ----------
OLD_DESC = "the fight over the UT lease, "
NEW_DESC = "the fight over the UT land and the 2026 deal to save it, "
INTRO_OLD = "And for most of the last decade, nobody has known how long any of that gets to continue. The land belongs to the University of Texas, the long-term lease ran out in 2019, and the course has been living on short extensions ever since &mdash; which is a strange way to treat the site of one of the quietest, earliest civil rights victories in the South.</p>"
INTRO_NEW = ("And for most of the last decade, nobody knew how long any of that would get to continue. The land belongs to the University of Texas, the long-term lease ran out in 2019, and the course lived on short extensions after that &mdash; a strange way to treat the site of one of the quietest, earliest civil rights victories in the South. "
             "On October 14, 2026, that finally changed: the City of Austin and UT announced a proposed deal to hand Muny to the city for good (" + a(CITY, "city announcement") + ").<!--MUNY-DEAL-26--></p>")
TL_ANCHOR = 'A hundred and two years in, the tee sheet is still full.</div></div>'
TL_NEW = TL_ANCHOR + ('\n    <div class="tl-row"><div class="tl-year">Oct 2026</div><div class="tl-text">The City and UT announce a proposed amendment to the 1989 Brackenridge Development Agreement that would give the city ownership of Muny. '
                      'City Council is scheduled to take it up November 19 (' + a(CITY, "City of Austin") + ').<!--MUNY-DEAL-26--></div></div>')
FIGHT_ANCHOR = "at one point month to month with five months&rsquo; notice of termination.</p>"
FIGHT_NEW = FIGHT_ANCHOR + ('\n    <p style="margin-top:16px"><strong>Now it may finally be over.</strong> On October 14, 2026, the City of Austin said it was close to an agreement with UT to convey ownership of the course to the city, preserving it as a public course and open green space, as part of amendments to the 1989 Brackenridge Development Agreement (' + a(CITY, "city announcement") + '). '
                            'The Austin American-Statesman reported that anonymous donors would help the city buy the 141 acres, and that the deal still needs city and university approval (' + a(STATESMAN, "Statesman") + '); '
                            'Golfweek reported that the Muny Conservancy brokered it (' + a(GOLFWEEK, "Golfweek") + '). '
                            'City Council is scheduled to vote on the amended agreement on November 19, with the remaining pieces of the deal returning to Council in spring 2027. '
                            'Mayor Kirk Watson called it &ldquo;a great day for Austin.&rdquo;<!--MUNY-DEAL-26--></p>')
FAQ_Q_OLD = "Why might Lions Municipal close?"
FAQ_Q_NEW = "Is Lions Municipal going to close?"
FAQ_A_NEW = ("Very likely not. The course sits on 141 acres of the Brackenridge Tract, land deeded to the University of Texas in 1910, and it ran on short lease extensions after the city's long-term lease expired in 2019. "
             "On October 14, 2026, the City of Austin and UT announced a proposed deal that would give the city ownership of the course and preserve it as a public course. "
             "City Council is scheduled to vote on November 19, 2026.")

def patch_faq(t, is_builder):
    if FAQ_Q_NEW in t: return t, 0
    n = 0
    if is_builder:
        t, k = re.subn(r'\("Why might Lions Municipal close\?",\s*\n\s*"[^"]*"\)',
                       '(%s,\n  %s)' % (json.dumps(FAQ_Q_NEW), json.dumps(FAQ_A_NEW)), t); n += k
        return t, n
    # JSON-LD
    t, k = re.subn(r'\{"@type":"Question","name":"Why might Lions Municipal close\?","acceptedAnswer":\{"@type":"Answer","text":"(?:[^"\\]|\\.)*"\}\}',
                   lambda m: '{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}' % (json.dumps(FAQ_Q_NEW), json.dumps(FAQ_A_NEW)), t); n += k
    # visible FAQ
    t, k = re.subn(r'(<details[^>]*class="faq-q"><summary>)Why might Lions Municipal close\?(</summary><p>).*?(</p></details>)',
                   lambda m: m.group(1) + FAQ_Q_NEW + m.group(2) + FAQ_A_NEW + m.group(3), t, flags=re.S); n += k
    return t, n

def rep(t, old, new, label, log, marker_in_new=True):
    if (new in t) or (marker_in_new and "<!--MUNY-DEAL-26-->" in new and new.split("<!--MUNY-DEAL-26-->")[0][-80:] in t and old not in t):
        return t
    c = t.count(old)
    if c == 0: log.append(f"  ! {label}: anchor not found"); return t
    log.append(f"  {label}: {c}x"); return t.replace(old, new)

def do_fg(t, log):
    for i, (o, n) in enumerate(FG, 1): t = rep(t, o, n, f"field-guide edit {i}", log)
    t = re.sub(r'"dateModified": "2026-\d\d-\d\d"', '"dateModified": "2026-10-19"', t, count=1)
    t = re.sub(r'<span>Updated [A-Z][a-z]+ \d{1,2}, 2026</span>', '<span>Updated October 19, 2026</span>', t, count=1)
    return t

def do_lions(t, log, is_builder=False):
    if is_builder:
        t = rep(t, '"the first integrated municipal course in the South. The history, the fight over the UT lease, "',
                '"the first integrated municipal course in the South. The history, the fight over the UT land and the 2026 deal to save it, "', "desc", log, False)
    else:
        c = t.count(OLD_DESC)
        if c: t = t.replace(OLD_DESC, NEW_DESC); log.append(f"  desc: {c}x")
    t = rep(t, INTRO_OLD, INTRO_NEW, "intro", log)
    t = rep(t, TL_ANCHOR, TL_NEW, "timeline", log) if "Oct 2026</div>" not in t else t
    t = rep(t, FIGHT_ANCHOR, FIGHT_NEW, "fight", log) if "Now it may finally be over." not in t else t
    t, k = patch_faq(t, is_builder); log.append(f"  faq: {k} block(s)") if k else None
    t = re.sub(r'"dateModified": "2026-\d\d-\d\d"', '"dateModified": "2026-10-19"', t, count=1)
    t = re.sub(r'Updated [A-Z][a-z]+ \d{1,2}, 2026</p><!--/TGI-BY-->', 'Updated October 19, 2026</p><!--/TGI-BY-->', t, count=1)
    return t

TARGETS = [("field-guide/index.html", do_fg),
           ("drops/lions-municipal-golf-course-austin.html", lambda t, l: do_lions(t, l)),
           ("build-lions.py", lambda t, l: do_lions(t, l, True))]

def main():
    apply_ = "--apply" in sys.argv
    only = sys.argv[sys.argv.index("--one") + 1] if "--one" in sys.argv else None
    bad = []
    for rel, fn in TARGETS:
        if only and rel != only: continue
        p = ROOT / rel; t0 = p.read_text(encoding="utf-8"); log = []
        t = fn(t0, log)
        print(rel, "(changed)" if t != t0 else "(unchanged)"); print("\n".join(log))
        bad += [f"{rel}{x}" for x in log if "!" in x]
        if rel.endswith(".html"):
            vis = re.sub(r"<(script|style)\b.*?</\1>|<[^>]+>", " ", t, flags=re.S)
            for stale in ("still waiting on a lease", "lease running on short extensions", "has been living on short extensions"):
                if stale in vis: bad.append(f"{rel}: stale phrase '{stale}' still visible")
            if re.search(r"\bworth\b", vis, re.I) and not re.search(r"\bworth\b", re.sub(r"<(script|style)\b.*?</\1>|<[^>]+>", " ", t0, flags=re.S), re.I):
                bad.append(f"{rel}: introduced banned word")
            for ld in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
                try: json.loads(ld)
                except Exception as e: bad.append(f"{rel}: JSON-LD broke ({e})")
        if apply_ and t != t0: p.write_text(t, encoding="utf-8")
    if bad: sys.exit("! " + "; ".join(bad))
    print("applied" if apply_ else "dry run — pass --apply")

if __name__ == "__main__":
    main()
