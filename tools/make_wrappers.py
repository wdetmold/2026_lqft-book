#!/usr/bin/env python3
"""Strip \\chapter lines from migrated content files (titles live in the
chapter wrapper) and generate chapters/chNN-*/chNN.tex wrappers."""
import re, pathlib

REPO = pathlib.Path("/home/user/lqft-book")

CH = {
 "ch01-introduction":        ("Introduction: what is lattice QFT?", ["notes-intro.tex"], None),
 "ch02-path-integrals":      ("Path integrals and fields on a lattice", ["quantum-mechanics.tex", "lattices.tex"], None),
 "ch03-scalar-fields":       ("Scalar fields on the lattice", ["scalar.tex", "exercises.tex"], None),
 "ch04-gauge-fields":        ("Lattice gauge fields", ["gauge.tex", "exercises.tex"], None),
 "ch05-hamiltonian-lgt":     ("Hamiltonian lattice gauge theory", [],
   "Promote the Kogut--Susskind Hamiltonian material (currently in Ch.~4 source) to a full chapter; foundation for Ch.~22."),
 "ch06-lattice-fermions":    ("Lattice fermions", ["fermions.tex", "staggered.tex", "chiral.tex", "exercises.tex"], None),
 "ch07-improvement-continuum": ("Improvement and the continuum limit", [],
   "Consolidate Symanzik improvement, clover, RG/continuum-limit material scattered through Chs.~3, 4, 6; add scale setting."),
 "ch08-monte-carlo":         ("Monte Carlo algorithms for lattice QFT", ["algorithms.tex"], None),
 "ch09-gradient-flow":       ("Gradient flow and scale setting", ["wilson-flow-notes.tex"],
   "New chapter: flow equations for gauge and fermion fields, $t_0$/$w_0$ scale setting, flowed observables and renormalisation."),
 "ch10-data-analysis":       ("Data analysis for lattice QFT", [],
   "New chapter: jackknife/bootstrap, correlated fits, model averaging, systematic error budgets, chiral-continuum-volume extrapolation."),
 "ch11-ml-methods":          ("Machine learning methods", [],
   "New chapter: flow-based/normalizing-flow sampling, gauge-equivariant networks (L-CNNs), where ML does and does not help."),
 "ch12-thermodynamics":      ("QCD thermodynamics", ["thermo.tex"], None),
 "ch13-spectroscopy":        ("Hadron spectroscopy", ["spectrum.tex"], None),
 "ch14-matrix-elements":     ("Hadronic matrix elements", ["matrix-elements.tex"], None),
 "ch15-finite-volume":       ("Scattering and finite-volume physics", ["interactions.tex"], None),
 "ch16-isospin-qed":         ("Isospin breaking and QED effects", ["isospin-notes.tex"],
   "New chapter: QED$_\\mathrm{L}$ and friends, renormalisation with QED, finite-volume effects, precision applications."),
 "ch17-strong-coupling-sf":  ("The strong coupling and the Schr\\\"odinger functional", ["schrodinger-functional.tex", "strong-coupling-notes.tex"], None),
 "ch18-lattice-bsm":         ("Strong interactions beyond the Standard Model", ["bsm.tex"], None),
 "ch19-chiral-gauge":        ("Chiral gauge theories on the lattice", ["chiral-gauge.tex"], None),
 "ch20-lattice-susy":        ("Lattice supersymmetry", ["susy.tex"], None),
 "ch21-perfect-actions":     ("Perfect actions and the renormalization group", ["perfect-actions.tex"], None),
 "ch22-quantum-simulation":  ("Quantum simulation of lattice gauge theories", [],
   "New chapter: Hamiltonian formulations (from Ch.~5), Hilbert-space truncations, qubit encodings, near-term algorithms and outlook."),
}

def strip_chapters(path):
    t = path.read_text(encoding="utf-8")
    t2 = re.sub(r"\\chapter\{([^}]*)\}",
                lambda m: "%% [migrated] heading absorbed into chapter wrapper: " + m.group(1),
                t)
    path.write_text(t2, encoding="utf-8")

for chdir, (title, files, todo) in CH.items():
    d = REPO / "chapters" / chdir
    num = chdir[2:4]
    for f in files:
        p = d / f
        if p.exists():
            strip_chapters(p)
    lines = ["% Chapter wrapper — edit content in the sibling files, not here.",
             "\\chapter{%s}" % title,
             "\\label{ch:%s}" % chdir[5:], ""]
    if todo:
        lines += ["\\todo{%s}" % todo, ""]
    for f in files:
        if (d / f).exists():
            lines.append("\\input{chapters/%s/%s}" % (chdir, f[:-4]))
        else:
            lines.append("%% missing: " + f)
    (d / ("ch%s.tex" % num)).write_text("\n".join(lines) + "\n", encoding="utf-8")

print("wrappers written")
