"""Redraw of fig-notes-061: a short lattice path of links from site x to site y,
used INLINE in the equation E_Gamma(x,y) = (path of links) = U_mu(x) U_nu(x+mu) ...
Compact staircase of directed links with dots at lattice sites; endpoints
labelled x and y.
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np

C_BLUE = "#0072B2"

fig, ax = plt.subplots(figsize=(2.5, 1.25))
ax.set_aspect("equal")
ax.axis("off")

# staircase path of lattice sites (matches the sketch: R, U, R, D, D, R, U, R)
sites = [(0, 1), (1, 1), (1, 2), (2, 2), (2, 1), (2, 0), (3, 0), (3, 1), (4, 1)]
sites = [np.array(s, dtype=float) for s in sites]


def arrow_on(a, b, frac=0.55):
    """Small arrowhead on the link a->b at fractional position frac."""
    d = b - a
    m = a + frac * d
    eps = 1e-3 * d
    ax.annotate("", xy=m + eps, xytext=m - eps,
                arrowprops=dict(arrowstyle="-|>", color=C_BLUE,
                                mutation_scale=9, shrinkA=0, shrinkB=0))


for a, b in zip(sites[:-1], sites[1:]):
    ax.plot([a[0], b[0]], [a[1], b[1]], color=C_BLUE, lw=1.8,
            solid_capstyle="round", zorder=2)
    arrow_on(a, b)

pts = np.array(sites)
ax.plot(pts[:, 0], pts[:, 1], "o", color=C_BLUE, ms=3.6, zorder=3)

ax.text(-0.18, 1.0, r"$x$", color=C_BLUE, ha="right", va="center", fontsize=11)
ax.text(4.18, 1.0, r"$y$", color=C_BLUE, ha="left", va="center", fontsize=11)

ax.set_xlim(-0.8, 4.8)
ax.set_ylim(-0.4, 2.4)

fig.savefig("../fig-redraw-061.pdf", bbox_inches="tight", pad_inches=0.02)
fig.savefig("../fig-redraw-061.png", dpi=200, bbox_inches="tight",
            pad_inches=0.02)
print("done 061")
