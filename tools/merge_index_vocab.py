#!/usr/bin/env python3
"""Merge agent-proposed index terms into the master vocabulary.

Input:  tools/index-terms-*.tsv   (INDEX_KEY <TAB> alias1;alias2 <TAB> note)
Output: refs/index-vocabulary.tsv (the file to review and edit)
        review/index-vocabulary-review.md (readable, with near-duplicate flags)

Cross-reference entries ("X, \\see{Y}" style keys) become |see{} entries.
"""
import pathlib, re, unicodedata
from collections import OrderedDict

REPO = pathlib.Path(__file__).resolve().parent.parent

# unify keys that different agents chose differently for the same concept
KEY_UNIFY = {
    "beta function@$\\beta$ function": "beta function@$\\beta$-function",
    "domain-wall fermions": "fermions!domain-wall",
    "overlap fermions": "fermions!overlap",
    "staggered fermions": "fermions!staggered",
    "Dirac-Kähler fermions": "fermions!Dirac-K\\\"ahler",
    "QCD phase diagram": "phase diagram!QCD",
    "renormalisation group equation (RGE)": "renormalisation group equations",
    "Landau gauge": "gauge fixing!Landau",
    "Rome-Southampton method": "renormalisation!RI-MOM",
}

entries = OrderedDict()   # key -> {"aliases": set, "notes": [], "see": target|None}
flags = []

def add(key, aliases, note):
    key = key.strip()
    see = None
    m = re.match(r"^(.*?),\s*\\see\{(.*)\}$", key)
    if m:
        key, see = m.group(1).strip(), m.group(2).strip().replace(", ", "!")
    key = KEY_UNIFY.get(key, key)
    e = entries.setdefault(key, {"aliases": [], "notes": [], "see": None})
    if see:
        e["see"] = see
    for a in aliases:
        a = a.strip()
        if a and a not in e["aliases"]:
            e["aliases"].append(a)
    if note.strip():
        e["notes"].append(note.strip())

for f in sorted(REPO.glob("tools/index-terms-*.tsv")):
    for line in f.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("INDEX_KEY"):
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        add(parts[0], parts[1].split(";"), parts[2] if len(parts) > 2 else "")

# near-duplicate detection (same normalized tail word-set)
def norm(k):
    k = k.split("@")[-1]
    k = re.sub(r"[\\ $\\{\\}!,-]", " ", k.lower())
    return frozenset(w for w in k.split() if len(w) > 2)

seen = {}
for k in entries:
    n = norm(k)
    for k2, n2 in seen.items():
        if n and (n == n2):
            flags.append(f"possible duplicate: `{k}`  ~  `{k2}`")
    seen[k] = n

# ---- write master TSV -----------------------------------------------------
out = REPO / "refs/index-vocabulary.tsv"
with out.open("w", encoding="utf-8") as f:
    f.write("# Master index vocabulary. Edit freely: delete rows, rename keys,\n")
    f.write("# add aliases (';'-separated). '!' = subentry, '@' = sort key,\n")
    f.write("# 'SEE:<target>' in the alias column makes a cross-reference entry.\n")
    f.write("# Then run: python3 tools/apply_index.py\n")
    for k in sorted(entries, key=lambda s: s.split("@")[0].lower()):
        e = entries[k]
        alias = "SEE:" + e["see"] if e["see"] else ";".join(e["aliases"])
        f.write(f"{k}\t{alias}\t{' | '.join(e['notes'][:1])}\n")

# ---- write review doc -----------------------------------------------------
rev = REPO / "review/index-vocabulary-review.md"
with rev.open("w", encoding="utf-8") as f:
    f.write("# Proposed index vocabulary — for review\n\n")
    n_see = sum(1 for e in entries.values() if e["see"])
    f.write(f"{len(entries)} entries ({n_see} cross-references). Source of truth: "
            "`refs/index-vocabulary.tsv` — edit that file (delete/rename/add), then "
            "`python3 tools/apply_index.py && make` regenerates all automatic "
            "`\\aidx` entries and the typeset index.\n\n")
    if flags:
        f.write("## Flagged for your decision (possible duplicates)\n\n")
        for fl in sorted(set(flags)):
            f.write("- " + fl + "\n")
        f.write("\n")
    f.write("## Entries\n\n")
    letter = ""
    for k in sorted(entries, key=lambda s: s.split("@")[0].lower()):
        e = entries[k]
        L = k.split("@")[0][0].upper()
        if L != letter:
            letter = L
            f.write(f"\n### {L}\n\n")
        disp = k.split("@")[-1].replace("!", " → ")
        if e["see"]:
            f.write(f"- {disp} — *see* {e['see'].replace('!', ', ')}\n")
        else:
            f.write(f"- {disp}  (matches: {'; '.join(e['aliases'][:4])})\n")

print(f"{len(entries)} entries merged; {len(set(flags))} duplicate flags")
