#!/usr/bin/env python3
"""Wire the 18 taxonomy pages into the site graph.

build-brand-taxonomy.py makes taxonomy -> brand links. On its own that is only
half a graph: the 132 brand pages still have one inbound link each and no way
out except back to /brands. This script closes the loop three ways.

1. EVERY BRAND PAGE gets a chip row linking to each taxonomy page it belongs to.
   This is the half that actually fixes the audit finding — a brand page stops
   being a dead end, and every taxonomy page picks up 2-52 inbound links from
   the brand pages themselves rather than only from the Index.

2. /brands GETS A FULL BROWSE BLOCK. Today the Index links to five taxonomy
   pages through its vibe tiles and advertises seventeen in the sitemap. After
   this it links to all eighteen, with computed counts.

3. SITEMAP. Seventeen rows already exist and have been 404ing since they were
   added; they now resolve. 'independent' is new and gets a row.

IDEMPOTENT. Every insertion is fenced with an HTML comment marker and replaced
rather than appended on a re-run, so this can be run after any brand rebuild.

RUN ORDER: after build-brands.py -> build-brand-index.py -> build-brand-taxonomy.py.
"""
import json, re, os, sys, html, glob, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
brands = json.load(open(os.path.join(ROOT, "data", "brands.json"), encoding="utf-8"))
TODAY = "2026-09-17"
ALIAS = {"loud": "loud-on-purpose"}

# Same order and labels as the builder. Kept here rather than imported so this
# script can run against a checkout where the builder has already been deleted.
TAX = [("tag", "design-nerd", "Design nerd"), ("tag", "made-by-hand", "Made by hand"),
       ("tag", "loud-on-purpose", "Loud on purpose"), ("tag", "independent", "Independent"),
       ("tag", "muni-energy", "Muni energy"), ("tag", "post-round-friendly", "Post-round friendly"),
       ("tag", "collab-machine", "Collab machine"), ("tag", "quiet-luxury", "Quiet"),
       ("tag", "gorpcore", "Gorpcore"), ("tag", "range-rat", "Range rat"),
       ("tag", "course-merch", "Course merch"), ("tag", "member-guest", "Member-guest"),
       ("tag", "dad-golf", "Dad golf"),
       ("attr", "new-to-index", "New to the Index"), ("attr", "women-founded", "Women-founded"),
       ("attr", "heritage", "Heritage"), ("attr", "tour-proven", "Tour-proven"),
       ("attr", "drops-and-vanishes", "Drops and vanishes")]

apply_ = "--apply" in sys.argv
notes = []

for kind, slug, _lab in TAX:
    p = os.path.join(ROOT, "brands", kind, slug + ".html")
    if not os.path.exists(p):
        raise SystemExit(f"/brands/{kind}/{slug} does not exist — run build-brand-taxonomy.py --apply first")


def belongs(b):
    out = []
    tags = {ALIAS.get(t, t) for t in b.get("tags", [])}
    attrs = set(b.get("attrs", []))
    for kind, slug, lab in TAX:
        if (kind == "tag" and slug in tags) or (kind == "attr" and slug in attrs):
            out.append((kind, slug, lab))
    return out


COUNTS = {(k, s): sum(1 for b in brands if (k, s, l) in belongs(b)) for k, s, l in TAX}

CSS = """<style id="tx-chip-css">
.bp-taxo{margin:14px 0 0;display:flex;flex-wrap:wrap;gap:7px;align-items:center}
.bp-taxo .bp-taxo-lab{font-family:var(--mono,ui-monospace,monospace);font-size:9.5px;letter-spacing:.15em;
 text-transform:uppercase;opacity:.55;margin-right:2px}
.bp-taxo a{font-family:var(--mono,ui-monospace,monospace);font-size:9.5px;letter-spacing:.13em;
 text-transform:uppercase;padding:6px 9px;border:1px solid rgba(20,20,20,.18);text-decoration:none;
 color:inherit;line-height:1}
.bp-taxo a:hover{background:#141414;color:#fff;border-color:#141414}
</style>"""

# ------------------------------------------------------------ 1. brand pages
START, END = "<!--TX-CHIPS-->", "<!--/TX-CHIPS-->"
touched, skipped, nochip = [], [], []
for b in brands:
    p = os.path.join(ROOT, "brands", b["slug"] + ".html")
    if not os.path.exists(p):
        skipped.append(b["slug"]); continue
    t = open(p, encoding="utf-8").read()
    mine = belongs(b)
    if not mine:
        nochip.append(b["slug"]); continue
    chips = "".join(f'<a href="/brands/{k}/{s}">{html.escape(lab)}</a>' for k, s, lab in mine)
    block = (f'{START}<div class="bp-taxo"><span class="bp-taxo-lab">Also in</span>{chips}</div>{END}')

    t = re.sub(re.escape(START) + r".*?" + re.escape(END), "", t, flags=re.S)  # idempotent
    anchor = re.search(r'(<div class="bp-meta">.*?</div>)', t, re.S)
    if not anchor:
        skipped.append(b["slug"] + " (no .bp-meta)"); continue
    t = t[:anchor.end()] + "\n    " + block + t[anchor.end():]

    if 'id="tx-chip-css"' not in t:
        t = t.replace("</head>", CSS + "\n</head>", 1)
    if apply_:
        open(p, "w", encoding="utf-8").write(t)
    touched.append(b["slug"])
notes.append(f"brand pages given a taxonomy chip row: {len(touched)}")
if nochip:
    notes.append(f"  no tag or attr, so no chips: {', '.join(nochip)}")
if skipped:
    notes.append(f"  !! skipped: {', '.join(skipped)}")

# ------------------------------------------------------------- 2. /brands hub
BSTART, BEND = "<!--TX-BROWSE-->", "<!--/TX-BROWSE-->"
ip = os.path.join(ROOT, "brands", "index.html")
idx = open(ip, encoding="utf-8").read()
rows = "".join(
    f'<a href="/brands/{k}/{s}"><span class="txb-lab">{html.escape(lab)}</span>'
    f'<span class="txb-n">{COUNTS[(k, s)]}</span></a>' for k, s, lab in TAX)
browse = f"""{BSTART}<section class="sec" id="browse-by"><div class="wrap">
  <h2 class="sec-h">Browse the Index by character</h2>
  <p class="sec-p">Eighteen ways through {len(brands)} brands. Every brand sits on as many of these as
  genuinely describe it, so these overlap on purpose.</p>
  <div class="txb">{rows}</div>
</div></section>
<style id="txb-css">
#bx .txb{{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:10px;margin-top:22px}}
#bx .txb a{{display:flex;justify-content:space-between;align-items:baseline;gap:10px;padding:13px 14px;
 border:1px solid var(--bx-rule,#e6e4df);text-decoration:none;color:inherit}}
#bx .txb a:hover{{background:var(--bx-ink,#141414);color:var(--bx-paper,#F4F1EA);border-color:var(--bx-ink,#141414)}}
#bx .txb .txb-lab{{font-size:14.5px;font-weight:600;letter-spacing:-.01em}}
#bx .txb .txb-n{{font-family:var(--bx-mono);font-size:10px;letter-spacing:.14em;opacity:.6}}
</style>{BEND}"""

idx = re.sub(re.escape(BSTART) + r".*?" + re.escape(BEND), "", idx, flags=re.S)
anchor = idx.find('<section class="sec" id="directory">')
if anchor == -1:
    raise SystemExit("could not find the #directory section in brands/index.html")
idx = idx[:anchor] + browse + "\n" + idx[anchor:]
if apply_:
    open(ip, "w", encoding="utf-8").write(idx)
notes.append(f"/brands browse block: all {len(TAX)} taxonomy pages linked with computed counts")

# --------------------------------------------------------------- 3. sitemap
sp = os.path.join(ROOT, "sitemap.xml")
sm = open(sp, encoding="utf-8").read()
added, bumped = 0, 0
for kind, slug, _lab in TAX:
    loc = f"https://thegrassyissue.com/brands/{kind}/{slug}"
    if loc not in sm:
        sm = sm.replace("</urlset>", f'<url><loc>{loc}</loc><lastmod>{TODAY}</lastmod>'
                        f'<changefreq>monthly</changefreq><priority>0.6</priority></url>\n</urlset>')
        added += 1
    else:
        sm2 = re.sub(r'(<loc>' + re.escape(loc) + r'</loc>\s*<lastmod>)[0-9-]+(</lastmod>)',
                     lambda m: m.group(1) + TODAY + m.group(2), sm)
        bumped += sm2 != sm
        sm = sm2
if apply_:
    open(sp, "w", encoding="utf-8").write(sm)
notes.append(f"sitemap: {added} row(s) added, {bumped} lastmod bumped — "
             f"the 17 that were 404ing now resolve")

# ----------------------------------------------------------------- 4. verify
live = {f"/brands/{k}/{s}" for k, s, _l in TAX}
smlocs = {re.sub(r"^https://thegrassyissue\.com", "", u).rstrip("/")
          for u in re.findall(r"<loc>(.*?)</loc>", sm)}
dead = sorted(u for u in smlocs if u.startswith("/brands/tag/") or u.startswith("/brands/attr/")
              if u not in live)
if dead:
    raise SystemExit(f"sitemap still advertises taxonomy URLs that do not exist: {dead}")

refs = set()
for p in (glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "brands", "*.html"))
          + glob.glob(os.path.join(ROOT, "brands", "*", "*.html"))):
    refs |= set(re.findall(r'href="(/brands/(?:tag|attr)/[a-z0-9-]+)"',
                           open(p, encoding="utf-8", errors="ignore").read()))
broken = sorted(refs - live)
if broken:
    raise SystemExit(f"internal links point at taxonomy URLs that do not exist: {broken}")

inb = collections.Counter()
for b in brands:
    for k, s, _l in belongs(b):
        inb[b["slug"]] += 1
vals = sorted(inb.values()) or [0]
print(("wired" if apply_ else "DRY RUN —") + f" {len(TAX)} taxonomy pages")
for n in notes:
    print("  ·", n)
print(f"\n  brand pages now reachable from {vals[0]}-{vals[-1]} taxonomy pages "
      f"(median {vals[len(vals)//2]}), on top of their Index card")
print(f"  taxonomy URLs referenced anywhere on the site: {len(refs)}; all resolve")
if not apply_:
    print("\npass --apply to write")
