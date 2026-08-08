#!/usr/bin/env python3
"""Standing manuscript lints. Extend NOTATION_RULES as conventions are fixed.

Run: python3 tools/lint_notation.py   (exit 0 always; prints findings)
"""
import pathlib, re, sys

REPO = pathlib.Path(__file__).resolve().parent.parent
FILES = sorted(REPO.glob("chapters/*/*.tex"))

NOTATION_RULES = [
    # (regex, message) — add project conventions here as they are decided.
    (r"\\varepsilon\b.*\\epsilon\b|\\epsilon\b.*\\varepsilon\b",
     "mixed epsilon variants on one line"),
    (r"\\mathrm\{Tr\}|\\text\{Tr\}|(?<!\\)\bTr\b(?![a-z])",
     "Tr should use a single macro (define \\tr in macros.tex)"),
    (r"TODO|FIXME|XXX",
     "open TODO marker"),
]

findings = 0
for f in FILES:
    for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        if line.lstrip().startswith("%"):
            continue
        for rx, msg in NOTATION_RULES:
            if re.search(rx, line):
                print(f"{f.relative_to(REPO)}:{i}: {msg}")
                findings += 1
                break

print(f"-- {findings} lint finding(s) in {len(FILES)} files")
