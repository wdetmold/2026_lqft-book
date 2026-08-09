"""Redraw of fig-notes-089: radiative generation of psi-bar psi with Wilson
fermions.  A gluon loop on the fermion line with one Wilson-term (a D^2)
insertion gives a linearly divergent contribution
~ a int_BZ d^4k k^2/(k^2 kslash kslash) ~ a Lambda^2 ~ (pi^2/a) psibar psi."""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np

BLUE = "#0072B2"
INK = "0.15"

fig, ax = plt.subplots(figsize=(6.2, 1.5))
ax.set_aspect("equal")
ax.axis("off")

# ---- fermion line with direction arrows ---------------------------------
ax.plot([0.0, 2.6], [0.0, 0.0], color=BLUE, lw=1.6,
        solid_capstyle="round", zorder=2)
for x0 in (0.18, 2.22):
    ax.annotate("", xy=(x0 + 0.2, 0.0), xytext=(x0, 0.0),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, shrinkA=0,
                                shrinkB=0, mutation_scale=13), zorder=3)

# ---- wiggly gluon arc over the middle of the line -----------------------
xa, xb = 0.65, 1.95
xc, R = 0.5 * (xa + xb), 0.5 * (xb - xa)
t = np.linspace(0, 1, 500)
th = np.pi * (1 - t)
r = R + 0.055 * np.sin(2 * np.pi * 7.5 * t)
ax.plot(xc + r * np.cos(th), r * np.sin(th), color=BLUE, lw=1.3, zorder=2)

# ---- Wilson-term insertion ----------------------------------------------
ax.plot(xc, 0.0, marker="o", ms=6.5, color=INK, zorder=4)
ax.text(xc, -0.22, r"$D^2$", color=INK, fontsize=11, ha="center", va="top")

# ---- parametric estimate ------------------------------------------------
ax.text(3.0, 0.12,
        r"$\sim\ a\!\int_{BZ} d^4k\,"
        r"\frac{k^2}{k^2\,k\!\!\!/\,k\!\!\!/}"
        r"\ \sim\ a\Lambda^2\ \sim\ \frac{\pi^2}{a}\,\bar{\psi}\psi$",
        fontsize=13, ha="left", va="center", color=INK)

ax.set_xlim(-0.2, 8.6)
ax.set_ylim(-0.55, 0.95)

fig.savefig("../fig-redraw-089.pdf")
fig.savefig("../fig-redraw-089.png", dpi=200)
print("done 089")
