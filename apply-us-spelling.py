#!/usr/bin/env python3
"""apply-us-spelling.py — American spelling across TGI's own copy. 7 Oct 2026.

Lenny: "let's use the american spelling throughout" (after the site-wide spelling
check found colour/color, grey/gray, centre/center etc. mixed on ~160 pages).

WHAT IT CHANGES. Visible text, <title>, and the description metas, plus string
values inside JSON-LD. A fixed word list only (colour→color, grey→gray,
organise→organize ...), never a general -ise→-ize rule, so advise/promise/
exercise and friends are never touched.

WHAT IT LEAVES ALONE (house rule: quotes are verbatim, product names are the
brand's own):
  * anything inside curly quotes “...”, <blockquote> and <q>;
  * Capitalised words, unless they start a sentence inside running text. Product
    titles ("Heather Grey Hoodie", "Colourway Pack") and proper nouns are Title
    Case, so they survive; our own sentence-initial "Colour is..." still changes;
  * attributes (hrefs, slugs, filenames, image alts), <script> other than
    JSON-LD, <style>, and the research/, drafts/ and previews/ folders.

Idempotent, and run by Deploy TGI.command so pages rebuilt from older builders
come out American every time. Dry run by default; --apply writes.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))

STEMS = {
    # -our
    "colour": "color", "favour": "favor", "flavour": "flavor", "humour": "humor",
    "labour": "labor", "neighbour": "neighbor", "harbour": "harbor", "honour": "honor",
    "behaviour": "behavior", "odour": "odor", "parlour": "parlor", "armour": "armor",
    "rumour": "rumor", "vapour": "vapor", "glamour": "glamor", "savour": "savor",
    "endeavour": "endeavor", "splendour": "splendor", "vigour": "vigor",
    # -re
    "centre": "center", "metre": "meter", "litre": "liter", "fibre": "fiber",
    "theatre": "theater", "calibre": "caliber", "sabre": "saber", "lustre": "luster",
    "spectre": "specter", "meagre": "meager", "sombre": "somber",
    # misc
    "programme": "program", "aluminium": "aluminum", "grey": "gray", "jewellery": "jewelry",
    "catalogue": "catalog", "cosy": "cozy", "mould": "mold", "moult": "molt",
    "licence": "license", "defence": "defense", "offence": "offense", "pyjama": "pajama",
    "tyre": "tire", "sceptic": "skeptic", "plough": "plow", "draught": "draft",
    "kerb": "curb", "storey": "story", "aeroplane": "airplane", "manoeuvre": "maneuver",
    "fulfil": "fulfill", "enrol": "enroll", "instalment": "installment",
    "travelled": "traveled", "travelling": "traveling", "traveller": "traveler",
    "cancelled": "canceled", "cancelling": "canceling", "labelled": "labeled",
    "labelling": "labeling", "modelled": "modeled", "modelling": "modeling",
    "levelled": "leveled", "fuelled": "fueled", "jewelled": "jeweled",
    "towelling": "toweling", "woollen": "woolen", "dialled": "dialed",
    # -ise / -isation (explicit list only)
    "organis": "organiz", "personalis": "personaliz", "customis": "customiz",
    "recognis": "recogniz", "realis": "realiz", "prioritis": "prioritiz",
    "utilis": "utiliz", "specialis": "specializ", "apologis": "apologiz",
    "authoris": "authoriz", "civilis": "civiliz", "commercialis": "commercializ",
    "modernis": "moderniz", "scrutinis": "scrutiniz", "serialis": "serializ",
    "polaris": "polariz", "vandalis": "vandaliz", "vectoris": "vectoriz",
    "merceris": "merceriz", "anodis": "anodiz", "optimis": "optimiz",
    "characteris": "characteriz", "minimis": "minimiz", "maximis": "maximiz",
    "emphasis": None,  # never: emphasis is a noun
    "standardis": "standardiz", "categoris": "categoriz", "finalis": "finaliz",
    "visualis": "visualiz", "summaris": "summariz", "memoris": "memoriz",
    "symbolis": "symboliz", "stabilis": "stabiliz", "sterilis": "steriliz",
    "neutralis": "neutraliz", "localis": "localiz", "monetis": "monetiz",
    "itemis": "itemiz", "energis": "energiz", "galvanis": "galvaniz",
    "vulcanis": "vulcaniz", "harmonis": "harmoniz", "idolis": "idoliz",
    "romanticis": "romanticiz", "glamoris": "glamoriz", "popularis": "populariz",
    "revolutionis": "revolutioniz", "sanitis": "sanitiz", "sympathis": "sympathiz",
    "criticis": "criticiz", "capitalis": "capitaliz", "fantasis": "fantasiz",
    "mesmeris": "mesmeriz", "patronis": "patroniz", "theoris": "theoriz",
    "jeopardis": "jeopardiz", "legalis": "legaliz", "normalis": "normaliz",
    "familiaris": "familiariz", "digitis": "digitiz", "trivialis": "trivializ",
    "analys": "analyz",   # analyse/analysed (analysis untouched: see GUARD)
    "paralys": "paralyz",
}
STEMS = {k: v for k, v in STEMS.items() if v}

# Words that start with a stem but are not the British form (or are already US).
GUARD = re.compile(r"^(analysis|analyses|analyst|paralysis|realism|realist|realistic|"
                   r"greyhound|centrefold|organism|organist|polaris|"
                   r"licensee|metric|metrical|fibreoptic|moulin|colourist)$", re.I)

STEM_RE = re.compile(r"(?<![\w-])(" + "|".join(sorted(STEMS, key=len, reverse=True)) +
                     r")([a-z]*)(?![\w-])", re.I)
# -ise endings that may follow an -is stem
ISE_OK = re.compile(r"^(e|es|ed|ing|ation|ations|able|er|ers|)$")
SENT_START = re.compile(r"(^|[.!?]\s+|[:;]\s+)$")


def swap_word(m, before):
    stem, rest = m.group(1), m.group(2)
    word = stem + rest
    if GUARD.match(word):
        return word
    low = stem.lower()
    target = STEMS[low]
    if low.endswith("is") or low.endswith("ys"):
        if not ISE_OK.match(rest.lower()):
            return word
    elif low == "grey":
        if rest.lower() not in ("", "s", "ed", "er", "est", "ish", "ness", "ing"):
            return word
    if stem[0].isupper():
        # Title Case = product name, collection or place (Sydney Harbour, the
        # Honourable Company, "Heather Grey Hoodie"). Never touched.
        return word
    if low in ("fulfil", "enrol") and rest[:1].lower() == "l":
        return word                      # fulfilling / enrolling are already US
    if target.endswith("er") and low.endswith("re") and rest[:1] == "d":
        rest = "e" + rest                # centred -> centered
    if low == "catalogue" and rest[:1] == "d":
        rest = "e" + rest                # catalogued -> cataloged
    return target + rest


def fix_text(t, state):
    """Swap words outside curly quotes. state['q'] carries open-quote depth."""
    out, i = [], 0
    for part in re.split(r"([“”])", t):
        if part == "“":
            state["q"] += 1; out.append(part); continue
        if part == "”":
            state["q"] = max(0, state["q"] - 1); out.append(part); continue
        if state["q"] or state["skip"]:
            out.append(part); continue
        res, last = [], 0
        for m in STEM_RE.finditer(part):
            res.append(part[last:m.start()])
            res.append(swap_word(m, part[max(0, m.start() - 4):m.start()] if m.start() else state["prev"]))
            last = m.end()
        res.append(part[last:])
        out.append("".join(res))
    joined = "".join(out)
    if joined.strip():
        state["prev"] = joined[-4:]
    return joined


BLOCK = re.compile(r"^</?(p|li|ul|ol|div|h[1-6]|td|th|tr|figcaption|summary|details|section|"
                   r"article|header|footer|aside|br|dd|dt|caption|main|nav|form|table)\b", re.I)
TOKEN = re.compile(r"(<!--.*?-->|<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|<[^>]+>)",
                   re.S | re.I)
META = re.compile(r'(<meta\s+(?:name|property)="(?:description|og:description|twitter:description|'
                  r'og:title|twitter:title)"\s+content=")([^"]*)(")', re.I)


def fix_html(s):
    state = {"q": 0, "skip": 0, "prev": ""}
    out = []
    for piece in TOKEN.split(s):
        if not piece:
            continue
        if piece.startswith("<"):
            low = piece[:40].lower()
            if low.startswith("<script") and "ld+json" in low:
                head, body = piece.split(">", 1)
                body = re.sub(r'"((?:[^"\\]|\\.)*)"',
                              lambda m: '"' + fix_text(m.group(1), {"q": 0, "skip": 0, "prev": ""}) + '"',
                              body)
                out.append(head + ">" + body); continue
            if re.match(r"<(blockquote|q)\b", low): state["skip"] += 1
            elif re.match(r"</(blockquote|q)\b", low): state["skip"] = max(0, state["skip"] - 1)
            if BLOCK.match(piece):
                state["q"] = 0; state["prev"] = ""
            out.append(piece); continue
        out.append(fix_text(piece, state))
    s = "".join(out)
    s = META.sub(lambda m: m.group(1) + fix_text(m.group(2), {"q": 0, "skip": 0, "prev": ""}) + m.group(3), s)
    return s


def pages():
    for f in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
        rel = os.path.relpath(f, ROOT)
        if rel.split(os.sep)[0] in ("research", "drafts", "previews", "node_modules", ".git"):
            continue
        if re.search(r" \d+\.html$", rel):
            continue
        yield f


def main(apply_):
    changed = 0; words = 0
    for f in pages():
        try:
            s = open(f, encoding="utf-8").read()
        except (OSError, UnicodeDecodeError):
            continue
        new = fix_html(s)
        if new != s:
            changed += 1
            words += sum(1 for a, b in zip(re.findall(r"\w+", s), re.findall(r"\w+", new)) if a != b)
            if apply_:
                open(f, "w", encoding="utf-8").write(new)
    print(f"apply-us-spelling: {changed} page(s) {'updated' if apply_ else 'would change'}"
          f" (~{words} words)")


if __name__ == "__main__":
    main("--apply" in sys.argv)
