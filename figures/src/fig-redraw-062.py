"""Redraw of fig-notes-062: the correlation function between two Wilson loops
on time slices t = 0 and t = t-hat.  Each slice is drawn as a spatial lattice
sheet in oblique projection with a red Wilson loop on it; dotted lines
indicate the propagation in time between the slices.
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np

C_RED = "#D55E00"
C_GREEN = "#009E73"
C_BLUE = "#0072B2"

E1 = np.array([0.62, 0.36])  # slanted spatial direction
E2 = np.array([0.00, 0.66])  # vertical spatial direction

fig, ax = plt.subplots(figsize=(4.6, 2.9))
ax.set_aspect("equal")
ax.axis("off")


def P(origin, i, j):
    return origin + i * E1 + j * E2


def sheet(origin):
    """Spatial lattice sheet (green) with a red Wilson loop on it."""
    for i in range(3):        # vertical lines
        a, b = P(origin, i, -0.5), P(origin, i, 3.5)
        ax.plot([a[0], b[0]], [a[1], b[1]], color=C_GREEN, lw=1.4, zorder=2)
    for j in range(4):        # slanted lines
        a, b = P(origin, -0.5, j), P(origin, 2.5, j)
        ax.plot([a[0], b[0]], [a[1], b[1]], color=C_GREEN, lw=1.4, zorder=2)
    # Wilson loop over sites (0,0)-(1,0)-(1,2)-(0,2)
    corners = [(0, 0), (1, 0), (1, 2), (0, 2), (0, 0)]
    pts = np.array([P(origin, i, j) for (i, j) in corners])
    ax.plot(pts[:, 0], pts[:, 1], color=C_RED, lw=2.4,
            solid_joinstyle="round", zorder=3)


OL = np.array([0.0, 0.0])
OR = np.array([5.4, 0.0])
sheet(OL)
sheet(OR)

# dotted lines: propagation in time between corresponding spatial points
for (i, j) in [(0, 0), (1, 0), (1, 2), (0, 2), (0, 3), (2, 1)]:
    a, b = P(OL, i, j), P(OR, i, j)
    ax.plot([a[0] + 0.30, b[0] - 0.30], [a[1], b[1]], color=C_GREEN,
            lw=1.3, ls=(0, (1.6, 2.6)), zorder=1)

ax.text(0.65, -0.95, r"$t = 0$", color=C_BLUE, ha="center", va="top",
        fontsize=11)
ax.text(OR[0] + 0.65, -0.95, r"$t = \hat{t}$", color=C_BLUE, ha="center",
        va="top", fontsize=11)

ax.set_xlim(-0.8, OR[0] + 2.6)
ax.set_ylim(-1.7, 3.4)

fig.savefig("../fig-redraw-062.pdf")
fig.savefig("../fig-redraw-062.png", dpi=200)
print("done 062")
