"""Redraw of fig-notes-030: the hadron-to-vacuum correlation function.
A quark loop connects the hadron interpolating operator chi~_H (blob at
the left) to the local operator O (point at the right); the dotted line
indicates that nothing propagates beyond the operator (vacuum).
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np

BLUE = "#0072B2"
INK = "0.15"


def bezier(p0, p1, p2, p3, n=200):
    t = np.linspace(0, 1, n)[:, None]
    p0, p1, p2, p3 = map(np.asarray, (p0, p1, p2, p3))
    return ((1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1
            + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3)


fig, ax = plt.subplots(figsize=(4.6, 3.0))
ax.set_aspect("equal")
ax.axis("off")

pL = np.array([-1.6, 0.0])   # hadron source chi~_H
pR = np.array([1.3, 0.0])    # local operator O

# quark loop: fat on the left, narrowing to the operator point
up = bezier(pL, (-1.35, 0.95), (0.45, 0.75), pR)
dn = bezier(pL, (-1.35, -0.95), (0.45, -0.75), pR)
for pts in (up, dn):
    ax.plot(pts[:, 0], pts[:, 1], color=BLUE, lw=1.6,
            solid_capstyle="round", zorder=2)

# source blob and operator point
ax.plot(*pL, marker="o", ms=9, color=INK, zorder=4)
ax.plot(*pR, marker="o", ms=6, color=INK, zorder=4)

# dotted line to the right of O: nothing (vacuum)
ax.plot([pR[0] + 0.12, pR[0] + 1.0], [0.0, 0.0], color=INK, lw=1.2,
        ls=(0, (1, 2.2)), zorder=2)

ax.text(pL[0] - 0.2, pL[1] + 0.35, r"$\tilde{\chi}_H$", ha="right",
        va="bottom", fontsize=13, color=INK)
ax.text(pR[0] + 0.05, pR[1] + 0.3, r"$\mathcal{O}$", ha="left",
        va="bottom", fontsize=13, color=INK)

ax.set_xlim(-2.6, 2.7)
ax.set_ylim(-1.35, 1.45)

fig.savefig("../fig-redraw-030.pdf")
fig.savefig("../fig-redraw-030.png", dpi=200)
print("done")
