"""Redraw of fig-notes-086: the two-particle scattering amplitude A as the
geometric (bubble-chain) sum of contact interactions f(p) joined by s-channel
two-particle loops -- A = X + X-O-X + X-O-X-O-X + ..."""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np
from matplotlib.patches import Ellipse

BLUE = "#0072B2"
ORANGE = "#D55E00"

LEG = 0.42       # external-leg length
ANG = 33.0       # external-leg opening half-angle (degrees)
SEP = 1.15       # vertex separation across one bubble
BH = 0.78        # bubble height

fig, ax = plt.subplots(figsize=(7.6, 1.15))
ax.set_aspect("equal")
ax.axis("off")


def vertex(x, left_legs=True, right_legs=True):
    """4-point contact vertex: filled dot with external legs."""
    for side, on in ((-1, left_legs), (+1, right_legs)):
        if not on:
            continue
        for s in (+1, -1):
            a = np.deg2rad(ANG)
            ax.plot([x, x + side * LEG * np.cos(a)],
                    [0, s * LEG * np.sin(a)],
                    color=BLUE, lw=1.6, solid_capstyle="round", zorder=3)
    ax.plot([x], [0], marker="o", ms=6.5, color=ORANGE, zorder=5)


def bubble(x1, x2):
    """two-particle loop joining the vertices at x1 and x2"""
    ax.add_patch(Ellipse(((x1 + x2) / 2, 0), x2 - x1, BH, fill=False,
                         edgecolor=BLUE, lw=1.6, zorder=2))


x = 0.0
ax.text(x, 0, r"$\mathcal{A}$", ha="center", va="center", fontsize=16)
x += 0.75
ax.text(x, 0, r"$=$", ha="center", va="center", fontsize=14)

# one vertex
x += 0.75 + LEG
vertex(x)
x += LEG + 0.62
ax.text(x, 0, r"$+$", ha="center", va="center", fontsize=14)

# two vertices, one bubble
x += 0.62 + LEG
vertex(x, right_legs=False)
bubble(x, x + SEP)
vertex(x + SEP, left_legs=False)
x += SEP + LEG + 0.62
ax.text(x, 0, r"$+$", ha="center", va="center", fontsize=14)

# three vertices, two bubbles
x += 0.62 + LEG
vertex(x, right_legs=False)
bubble(x, x + SEP)
vertex(x + SEP, left_legs=False, right_legs=False)
bubble(x + SEP, x + 2 * SEP)
vertex(x + 2 * SEP, left_legs=False)
x += 2 * SEP + LEG + 0.62
ax.text(x, 0, r"$+\;\cdots$", ha="left", va="center", fontsize=14)

ax.set_xlim(-0.4, x + 1.3)
ax.set_ylim(-0.75, 0.75)

fig.savefig("../fig-redraw-086.pdf")
fig.savefig("../fig-redraw-086.png", dpi=200)
