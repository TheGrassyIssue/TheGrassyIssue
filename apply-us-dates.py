#!/usr/bin/env python3
"""apply-us-dates.py — American date order across TGI's own copy. 8 Oct 2026.
Lenny: "swap it for Month then day, american style" (on the Field Guide's "Updated 8 October 2026").
Same reach and guards as apply-us-spelling.py: visible text, <title>, description metas and JSON-LD string values;
never inside curly quotes, <blockquote> or <q>; never attributes, other scripts, styles, or research/drafts/previews.

  8 October 2026   -> October 8, 2026
  19 Sept 2026     -> Sept. 19, 2026
  8 October        -> October 8      (no year)
Idempotent. Runs in Deploy TGI.command right after apply-us-spelling. Dry run by default.
"""
import glob, os, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
ABBR = "Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec"
FULL = re.compile(rf"\b(\d{{1,2}}) ({MONTHS})(?: (\d{{4}}))?\b(?!,? \d)")
SHORT = re.compile(rf"\b(\d{{1,2}}) ({ABBR})\.?(?: (\d{{4}}))?\b")

def swap(t):
    def full(m):
        d, mo, y = m.group(1), m.group(2), m.group(3)
        if not 1 <= int(d) <= 31: return m.group(0)
        return f"{mo} {int(d)}, {y}" if y else f"{mo} {int(d)}"
    def short(m):
        d, mo, y = m.group(1), m.group(2), m.group(3)
        if not 1 <= int(d) <= 31: return m.group(0)
        return f"{mo}. {int(d)}, {y}" if y else f"{mo}. {int(d)}"
    return SHORT.sub(short, FULL.sub(full, t))

def fix_text(t, st):
    out = []
    for part in re.split(r"([“”])", t):
        if part == "“": st["q"] += 1; out.append(part); continue
        if part == "”": st["q"] = max(0, st["q"] - 1); out.append(part); continue
        out.append(part if (st["q"] or st["skip"]) else swap(part))
    return "".join(out)

TOKEN = re.compile(r"(<!--.*?-->|<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|<[^>]+>)", re.S | re.I)
BLOCK = re.compile(r"^</?(p|li|ul|ol|div|h[1-6]|td|th|tr|figcaption|summary|details|section|article|header|footer|aside|br|dd|dt)\b", re.I)
META = re.compile(r'(<meta\s+(?:name|property)="(?:description|og:description|twitter:description|og:title|twitter:title)"\s+content=")([^"]*)(")', re.I)

def fix_html(s):
    st = {"q": 0, "skip": 0}; out = []
    for piece in TOKEN.split(s):
        if not piece: continue
        if piece.startswith("<"):
            low = piece[:40].lower()
            if low.startswith("<script") and "ld+json" in low:
                head, body = piece.split(">", 1)
                body = re.sub(r'"((?:[^"\\]|\\.)*)"', lambda m: '"' + fix_text(m.group(1), {"q": 0, "skip": 0}) + '"', body)
                out.append(head + ">" + body); continue
            if re.match(r"<(blockquote|q)\b", low): st["skip"] += 1
            elif re.match(r"</(blockquote|q)\b", low): st["skip"] = max(0, st["skip"] - 1)
            if BLOCK.match(piece): st["q"] = 0
            out.append(piece); continue
        out.append(fix_text(piece, st))
    s = "".join(out)
    s = re.sub(r"(<title>)(.*?)(</title>)", lambda m: m.group(1) + fix_text(m.group(2), {"q": 0, "skip": 0}) + m.group(3), s, flags=re.S)
    return META.sub(lambda m: m.group(1) + fix_text(m.group(2), {"q": 0, "skip": 0}) + m.group(3), s)

def main(apply_):
    changed = 0
    for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
        rel = os.path.relpath(f, ROOT)
        if rel.split(os.sep)[0] in ("research", "drafts", "previews", "node_modules", ".git") or re.search(r" \d+\.html$", rel):
            continue
        try: s = open(f, encoding="utf-8").read()
        except (OSError, UnicodeDecodeError): continue
        new = fix_html(s)
        if new != s:
            changed += 1
            if apply_: open(f, "w", encoding="utf-8").write(new)
    print(f"apply-us-dates: {changed} page(s) {'updated' if apply_ else 'would change'}")

if __name__ == "__main__":
    main("--apply" in sys.argv)
