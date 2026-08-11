"""Redraw of fig-notes-052: handwritten annotated Lagrangian for the
gauge-fixed (non-gauge-invariant) chiral lattice theory -- the same equation
as eq:gflag in the text, with the annotations 'gauge fixing', 'counterterms'
and 'ghosts needed if non-Abelian' attached to the corresponding terms.
NOTE: the original is an equation, not a diagram; its \\includegraphics is
commented out in chiral-gauge.tex since the equation is typeset there."""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np

GREEN = "#009E73"

fig, ax = plt.subplots(figsize=(8.6, 1.7))
ax.axis("off")
ax.set_xlim(0, 10)
ax.set_ylim(0, 2)

Y = 1.35        # equation baseline
FS = 13

chunks = [
    (r"$\mathcal{L} \;\supset\; \frac{1}{g^2}F_{\mu\nu}F_{\mu\nu}"
     "\\;-\\;\\frac{r}{2}\\left(\\bar{\\psi}_R\\,□\\,\\psi_L"
     r"+\mathrm{h.c.}\right)\;+\;$", None),
    (r"$\tilde{\kappa}\left[(\partial_\mu A_\mu)^2+(A_\mu^2)^3\right]$",
     r"$\tilde{\kappa}=\frac{1}{2\xi g^2}$:" "\n" r"gauge fixing"),
    (r"$\;+\;$", None),
    (r"$\rho\,A_\mu^2 \,+\, \mathrm{other\ counterterms}$",
     "counterterms"),
    (r"$\;+\;$", None),
    (r"$\mathrm{ghosts}$", "needed if\nnon-Abelian"),
]

renderer = fig.canvas.get_renderer()
inv = ax.transData.inverted()

x = 0.1
for text, note in chunks:
    t = ax.text(x, Y, text, ha="left", va="center", fontsize=FS)
    bb = t.get_window_extent(renderer=renderer)
    (x0, _), (x1, _) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
    if note is not None:
        # shallow green under-arc plus annotation, as in the notes
        xs = np.linspace(x0 + 0.03, x1 - 0.03, 60)
        xm, hw = (x0 + x1) / 2, (x1 - x0) / 2
        ys = Y - 0.42 - 0.10 * (1 - ((xs - xm) / hw) ** 2)
        ax.plot(xs, ys, color=GREEN, lw=1.1, clip_on=False)
        ax.text(xm, Y - 0.68, note, ha="center", va="top", fontsize=9,
                color=GREEN)
    x = x1 + 0.05

fig.savefig("../fig-redraw-052.pdf")
fig.savefig("../fig-redraw-052.png", dpi=200)
