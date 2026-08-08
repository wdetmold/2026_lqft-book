#!/usr/bin/env python3
"""One-time migration: Overleaf lecture-notes subfiles -> book chapter layout.

Rules
-----
- Content = text between \\begin{document} and \\end{document}.
- Part-level headers (\\section{Fundamentals} etc.) are dropped (parts live in main.tex).
- Notes \\subsection -> book \\chapter ; \\subsubsection -> \\section.
- schrodinger_func.tex is split by \\subsection and routed to chs 9/16/17.
- thermo.tex: first two subsections (Anatomy, State-of-the-art) demoted to
  \\section inside ch12; the QCD thermodynamics subsection becomes the chapter.
- \\includegraphics refs rewritten to sanitized names via notes-figure-map.tsv.
"""
import re, sys, pathlib

SRC = pathlib.Path("/mnt/user-data/uploads/LQFT_lecture_notes_Detmold")
REPO = pathlib.Path("/home/user/lqft-book")
MAP = REPO / "figures/notes/notes-figure-map.tsv"

PART_HEADERS = {"Fundamentals", "LQFT Phenomenology", "Advanced Topics"}

# source file -> (chapter dir, content filename, mode)
ROUTE = {
    "intro.tex":             ("ch01-introduction",       "notes-intro.tex",      "intro"),
    "quantum_mechanics.tex": ("ch02-path-integrals",     "quantum-mechanics.tex","std"),
    "lattices.tex":          ("ch02-path-integrals",     "lattices.tex",         "demote"),
    "scalar.tex":            ("ch03-scalar-fields",      "scalar.tex",           "std"),
    "gauge.tex":             ("ch04-gauge-fields",       "gauge.tex",            "std"),
    "fermions.tex":          ("ch06-lattice-fermions",   "fermions.tex",         "std"),
    "staggered.tex":         ("ch06-lattice-fermions",   "staggered.tex",        "body"),
    "chiral.tex":            ("ch06-lattice-fermions",   "chiral.tex",           "body"),
    "algorithms.tex":        ("ch08-monte-carlo",        "algorithms.tex",       "std"),
    "thermo.tex":            ("ch12-thermodynamics",     "thermo.tex",           "thermo"),
    "spectrum.tex":          ("ch13-spectroscopy",       "spectrum.tex",         "std"),
    "structure.tex":         ("ch14-matrix-elements",    "matrix-elements.tex",  "std"),
    "interactions.tex":      ("ch15-finite-volume",      "interactions.tex",     "std"),
    "bsm.tex":               ("ch18-lattice-bsm",        "bsm.tex",              "std"),
    "fixed_point.tex":       ("ch21-perfect-actions",    "perfect-actions.tex",  "std"),
    "susy.tex":              ("ch20-lattice-susy",       "susy.tex",             "std"),
    "chiral_gauge.tex":      ("ch19-chiral-gauge",       "chiral-gauge.tex",     "std"),
    # schrodinger_func.tex handled specially below
}

def body_of(path):
    t = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"\\begin\{document\}(.*)\\end\{document\}", t, re.S)
    return (m.group(1) if m else t).strip("\n")

def load_map():
    pairs = []
    for line in MAP.read_text(encoding="utf-8").splitlines():
        parts = line.split("\t")
        if len(parts) == 3:
            ref, orig, new = parts
            pairs.append((ref, new))
            if orig != ref:
                pairs.append((orig, new))
    pairs.sort(key=lambda p: -len(p[0]))  # longest first
    return pairs

FIGMAP = load_map()

def rewrite_figs(s):
    def repl(m):
        opts, arg = m.group(1) or "", m.group(2)
        key = arg[len("images/"):] if arg.startswith("images/") else arg
        new = None
        for ref, tgt in FIGMAP:
            if key == ref:
                new = tgt; break
        if new is None:  # tolerate extension-stripped matches
            for ref, tgt in FIGMAP:
                if key == ref.rsplit(".", 1)[0]:
                    new = tgt; break
        return "\\includegraphics%s{%s}" % (opts, new if new else arg)
    return re.sub(r"\\includegraphics(\[[^\]]*\])?\{([^}]*)\}", repl, s)

def drop_part_headers(s):
    def repl(m):
        title = m.group(1).strip()
        if title in PART_HEADERS:
            return "%% [migrated] part header removed: " + title
        return m.group(0)
    return re.sub(r"\\section\{([^}]*)\}", repl, s)

def promote(s):
    s = drop_part_headers(s)
    s = s.replace("\\subsubsection", "\\SUBSECTMP")
    s = s.replace("\\subsection", "\\chapter")
    s = s.replace("\\SUBSECTMP", "\\section")
    s = s.replace("\\section*{", "\\section*{")  # no-op, clarity
    return s

def demote_to_section(s):
    # for files folded INTO an existing chapter: subsection -> section
    s = drop_part_headers(s)
    s = s.replace("\\subsubsection", "\\SUBSECTMP")
    s = s.replace("\\subsection", "\\section")
    s = s.replace("\\SUBSECTMP", "\\subsection")
    return s

def process(mode, s):
    s = rewrite_figs(s)
    if mode == "std":
        return promote(s)
    if mode == "intro":
        return re.sub(r"\\section\{\s*Introduction[^}]*\}",
                      "\\\\chapter{Introduction: what is lattice QFT?}", s, count=1)
    if mode == "body":     # subsubsection-level file folded into a chapter
        return promote(s)  # its subsubsections -> sections; no subsection present
    if mode == "demote":   # lattices.tex: becomes a section of ch02
        return demote_to_section(s)
    if mode == "thermo":
        s = drop_part_headers(s)
        # demote the two front subsections, promote the thermodynamics one
        s = s.replace("\\subsection{Anatomy of a LQCD calculation}",
                      "\\section{Anatomy of a LQCD calculation}")
        s = s.replace("\\subsection{State-of-the-art}",
                      "\\section{State-of-the-art}")
        s = s.replace("\\subsubsection", "\\SUBSECTMP")
        s = s.replace("\\subsection", "\\chapter")
        s = s.replace("\\SUBSECTMP", "\\section")
        return s
    raise ValueError(mode)

def main():
    written = []
    for src, (chdir, fname, mode) in ROUTE.items():
        out = REPO / "chapters" / chdir / fname
        out.write_text(process(mode, body_of(SRC / "sections" / src)) + "\n",
                       encoding="utf-8")
        written.append(str(out))
    # ---- split schrodinger_func.tex --------------------------------------
    s = rewrite_figs(body_of(SRC / "sections" / "schrodinger_func.tex"))
    pieces = re.split(r"(?=\\subsection\{)", s)
    frag = {"schrodinger": [], "wilson": [], "isospin": [], "strong": [], "other": []}
    for p in pieces:
        m = re.match(r"\\subsection\{([^}]*)\}", p)
        t = (m.group(1).lower() if m else "")
        if "schr" in t: frag["schrodinger"].append(p)
        elif "wilson" in t: frag["wilson"].append(p)
        elif "isospin" in t: frag["isospin"].append(p)
        elif "strong" in t: frag["strong"].append(p)
        else: frag["other"].append(p)
    def prom(x): return promote("".join(x))
    (REPO/"chapters/ch17-strong-coupling-sf/schrodinger-functional.tex").write_text(
        prom(frag["other"] + frag["schrodinger"]) + "\n", encoding="utf-8")
    (REPO/"chapters/ch17-strong-coupling-sf/strong-coupling-notes.tex").write_text(
        prom(frag["strong"]) + "\n", encoding="utf-8")
    (REPO/"chapters/ch09-gradient-flow/wilson-flow-notes.tex").write_text(
        prom(frag["wilson"]) + "\n", encoding="utf-8")
    (REPO/"chapters/ch16-isospin-qed/isospin-notes.tex").write_text(
        prom(frag["isospin"]) + "\n", encoding="utf-8")
    # ---- exercises --------------------------------------------------------
    for src, ch in [("scalarfield.tex", "ch03-scalar-fields"),
                    ("gaugefield.tex",  "ch04-gauge-fields"),
                    ("fermions.tex",    "ch06-lattice-fermions")]:
        t = (SRC / "problems" / src).read_text(encoding="utf-8", errors="replace")
        t = re.sub(r".*?\\begin\{document\}", "", t, flags=re.S)
        t = re.sub(r"\\end\{document\}.*", "", t, flags=re.S)
        # strip any local (re)definitions of \problem or counters
        t = re.sub(r"\\newcounter\{probcount\}.*?\\addtocounter\{probcount\}\{1\}\}", "",
                   t, flags=re.S)
        t = rewrite_figs(t)
        (REPO/"chapters"/ch/"exercises.tex").write_text(
            "\\section*{Exercises}\n" + t.strip() + "\n", encoding="utf-8")
    print("wrote", len(written) + 7, "content files")

if __name__ == "__main__":
    main()
