# Lattice Quantum Field Theory and Phenomenology — book manuscript

Book manuscript grown from the Spring 2025 MIT lecture notes. Source of truth
is this git repository; Overleaf (via GitHub sync, tracking `main`) is an
editing surface.

## Layout

| Path | Contents |
|---|---|
| `main.tex` | Master file: parts, chapter includes, front/back matter |
| `preamble.tex` | Packages + exercise/solutions machinery (`\problem{...}{...}`) |
| `macros.tex` | Semantic notation macros — the only place notation is defined |
| `chapters/chNN-slug/` | One directory per chapter: `chNN.tex` wrapper + content files |
| `chapters/*/exercises.tex` | End-of-chapter exercises (solutions toggled at build time) |
| `figures/notes/` | Figures inherited from the lecture notes (to be replaced) |
| `figures/src/` | Programmatic figures: one script each + `lqftbook.mplstyle` |
| `refs/references.bib` | Bibliography (INSPIRE texkeys) |
| `tools/` | `build_bib.py` (INSPIRE resolver), `lint_notation.py`, migration scripts |
| `STATUS.md` | Per-chapter status board |

## Building

```
make            # student build  -> main.pdf
make solutions  # instructor build with worked solutions -> main-solutions.pdf
make figures    # regenerate programmatic figures
make lint       # notation lints + chktex
```

Fast single-chapter iteration: uncomment `\includeonly{...}` in `main.tex`.

CI compiles the book and uploads the PDF artifact on every push and PR.

## Conventions

- Chapter titles live in `chNN.tex` wrappers; content files hold `\section`
  and below. Edit content files, not wrappers.
- Every new figure is a script in `figures/src/` using the house stylesheet;
  no hand-exported binaries without committed source.
- Cite keys are INSPIRE texkeys (`Ding:2015ona`). Run `tools/build_bib.py`
  after adding arXiv IDs.
- Index entries (`\index{...}`) are added during prose conversion, not at the end.
- `\todo{...}` marks open work; it renders red in draft builds and is linted.

## Getting started after unpacking

```
git init && git add -A && git commit -m "Import book skeleton from lecture notes"
```

Then create the GitHub repository, push, and connect Overleaf's GitHub sync
to it if desired.
