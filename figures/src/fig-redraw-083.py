"""Redraw of fig-notes-083: quark-line diagram for the proton two-point
function.  Two Wick contractions: minus the diagram in which two of the
three quark lines are exchanged (crossed), plus the diagram with three
uncrossed quark lines, between the source and sink interpolating blobs.
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np
from matplotlib.patches import Ellipse

BLUE = "#0072B2"
INK = "0.15"
GREY = "0.82"


def bezier(p0, p1, p2, p3, n=200):
    t = np.linspace(0, 1, n)[:, None]
    p0, p1, p2, p3 = map(np.asarray, (p0, p1, p2, p3))
    return ((1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1
            + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3)


fig, ax = plt.subplots(figsize=(6.4, 1.9))
ax.set_aspect("equal")
ax.axis("off")

EW, EH = 0.42, 1.05          # source/sink ellipse size
DY = 0.30                    # attachment-point spacing


def blob(xc):
    ax.add_patch(Ellipse((xc, 0.0), EW, EH, facecolor=GREY,
                         edgecolor=INK, lw=1.0, zorder=3))
    for s in (+1, 0, -1):
        ax.plot(xc, s * DY, marker="o", ms=3.2, color=INK, zorder=4)


def diagram(x0, x1, crossed):
    blob(x0)
    blob(x1)
    ys = (DY, 0.0, -DY)
    if crossed:
        # top and middle lines are exchanged
        pairs = [(DY, 0.0), (0.0, DY), (-DY, -DY)]
    else:
        pairs = [(y, y) for y in ys]
    for yl, yr in pairs:
        pts = bezier((x0, yl), (x0 + 0.9, yl), (x1 - 0.9, yr), (x1, yr))
        ax.plot(pts[:, 0], pts[:, 1], color=BLUE, lw=1.5,
                solid_capstyle="round", zorder=2)


# minus (crossed) ... plus (uncrossed)
ax.text(-4.35, 0.0, r"$-$", ha="center", va="center", fontsize=15,
        color=INK)
diagram(-3.7, -0.7, crossed=True)
ax.text(0.05, 0.0, r"$+$", ha="center", va="center", fontsize=15,
        color=INK)
diagram(0.7, 3.7, crossed=False)

ax.set_xlim(-4.8, 4.2)
ax.set_ylim(-0.85, 0.85)

fig.savefig("../fig-redraw-083.pdf")
fig.savefig("../fig-redraw-083.png", dpi=200)
print("done")
