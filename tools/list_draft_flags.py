#!/usr/bin/env python3
"""Report every piece of machine-drafted material still awaiting the author.

Scans the manuscript for
    \\problemdraft[note]{...}{...}   -- a whole unverified exercise
    \\unverified{...}                -- one unverified claim inside good material
and prints a checklist with file:line locations.

    python3 tools/list_draft_flags.py            # checklist
    python3 tools/list_draft_flags.py --count    # just the totals (for CI)

To clear a flag: delete "draft" from \\problemdraft (and any [note]), or
unwrap \\unverified{...}.
"""
import pathlib, re, sys

REPO = pathlib.Path(__file__).resolve().parent.parent
FILES = sorted(REPO.glob("chapters/*/*.tex"))

def first_words(text, n=11):
    t = re.sub(r"\\label\{[^}]*\}", "", text)
    t = re.sub(r"\\textbf\{([^}]*)\}", r"\1", t)
    t = re.sub(r"[\\{}$]", "", t)
    t = " ".join(t.split())
    w = t.split()
    return " ".join(w[:n]) + ("..." if len(w) > n else "")

problems, claims = [], []
for f in FILES:
    text = f.read_text(encoding="utf-8")
    for m in re.finditer(r"\\problemdraft(\[[^\]]*\])?\{", text):
        line = text[:m.start()].count("\n") + 1
        note = (m.group(1) or "")[1:-1]
        problems.append((f, line, note, first_words(text[m.end():m.end()+220])))
    for m in re.finditer(r"\\remarkdraft(\[[^\]]*\])?\{", text):
        line = text[:m.start()].count("\n") + 1
        note = " ".join((m.group(1) or "")[1:-1].split())
        problems.append((f, line, note,
                         "REMARK: " + first_words(text[m.end():m.end()+220])))
    for m in re.finditer(r"\\unverified\{", text):
        line = text[:m.start()].count("\n") + 1
        claims.append((f, line, first_words(text[m.end():m.end()+200], 14)))

if "--count" in sys.argv:
    print(f"{len(problems)} unverified exercise(s)/remark(s), "
          f"{len(claims)} unverified claim(s)")
    sys.exit(0)

print("Draft material awaiting author verification")
print("=" * 62)
if problems:
    print(f"\nUnverified exercises ({len(problems)}):\n")
    for f, line, note, snip in problems:
        rel = f.relative_to(REPO)
        print(f"  [ ] {rel}:{line}")
        print(f"      {snip}")
        if note:
            print(f"      note: {note}")
if claims:
    print(f"\nUnverified claims inside checked material ({len(claims)}):\n")
    for f, line, snip in claims:
        print(f"  [ ] {f.relative_to(REPO)}:{line}\n      {snip}")
if not problems and not claims:
    print("\nNothing outstanding — no draft flags in the manuscript.")
else:
    print("\nClear a flag by deleting 'draft' from \\problemdraft (and any [note]),")
    print("or by unwrapping \\unverified{...}.")
