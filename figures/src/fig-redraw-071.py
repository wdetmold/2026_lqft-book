"""Redraw of fig-notes-071: the "clover term"
    C_{mu nu} = -(i/8) ( Q_{mu nu} - Q_{mu nu}^dagger ),
where Q is the clover-leaf arrangement of the four plaquettes around a
site: products of 16 links centred at n. The first group has all four
plaquettes traversed with the same (counter-clockwise) circulation; the
second is its reverse.
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np
from matplotlib.patches import Arc

BLUE = "#0072B2"

fig, ax = plt.subplots(figsize=(5.4, 1.7))
ax.set_aspect("equal")
ax.axis("off")


def arrow_on(a, b, ms=7):
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = 0.5 * (a + b)
    eps = 1e-3 * (b - a)
    ax.annotate("", xy=m + eps, xytext=m - eps,
                arrowprops=dict(arrowstyle="-|>", color=BLUE,
                                mutation_scale=ms, shrinkA=0, shrinkB=0))


def plaq(x, y, w, sense):
    """Square plaquette with a circulation arrow on each of its 4 edges."""
    c = [(x, y), (x + w, y), (x + w, y + w), (x, y + w)]  # ccw corners
    if sense == "cw":
        c = c[::-1]
    for i in range(4):
        a, b = c[i], c[(i + 1) % 4]
        ax.plot([a[0], b[0]], [a[1], b[1]], color=BLUE, lw=1.3,
                solid_capstyle="round")
        arrow_on(a, b)


def clover(cx, cy, sense):
    """Four plaquettes arranged around the central site (cx, cy)."""
    w, g = 0.95, 0.14
    for dx in (-1, 1):
        for dy in (-1, 1):
            x = cx + (g if dx > 0 else -g - w)
            y = cy + (g if dy > 0 else -g - w)
            plaq(x, y, w, sense)


def paren(cx, mirror=False):
    ax.add_patch(Arc((cx + (0.45 if not mirror else -0.45), 0.0),
                     1.0, 2.9, theta1=110, theta2=250,
                     angle=0 if not mirror else 180,
                     color="black", lw=1.1))


# C_{mu nu} = -i/8 ( clover - clover^dagger )
ax.text(-3.0, 0.0, r"$C_{\mu\nu} \;=\; -\dfrac{i}{8}$", fontsize=15,
        ha="left", va="center")
paren(-0.15)
clover(1.35, 0.0, "ccw")
ax.text(2.95, 0.0, r"$-$", fontsize=15, ha="center", va="center")
clover(4.55, 0.0, "cw")
paren(6.05, mirror=True)

ax.set_xlim(-3.15, 6.35)
ax.set_ylim(-1.55, 1.55)

fig.savefig("../fig-redraw-071.pdf", bbox_inches="tight", pad_inches=0.02)
fig.savefig("../fig-redraw-071.png", dpi=200, bbox_inches="tight",
            pad_inches=0.02)
print("done 071")
