"""Redraw of fig-notes-072: coordinatisation of the original lattice with
respect to the block centres, n_mu = x_mu + eta_mu^(i).

A 2a-block of the fine lattice is highlighted; its four sites are labelled
x_mu + eta_mu^(i).  Point labels follow the correction noted in the caption
of the hand-drawn figure: eta^(1) = (0,1), eta^(2) = (1,0), eta^(3) = (1,1).
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np
from matplotlib.patches import Rectangle

VERM = "#D55E00"
GREEN = "#009E73"
GRAY = "0.65"

fig, ax = plt.subplots(figsize=(4.6, 3.4))
ax.set_aspect("equal")
ax.axis("off")

# Fine lattice (spacing a).
lo, hi, pad = 0, 3, 0.35
for k in range(lo, hi + 1):
    ax.plot([lo - pad, hi + pad], [k, k], color=GRAY, lw=0.8, zorder=1)
    ax.plot([k, k], [lo - pad, hi + pad], color=GRAY, lw=0.8, zorder=1)

# The (2a)^D block containing the four sites x + eta^(i).
ax.add_patch(Rectangle((0.55, 0.55), 1.9, 1.9, facecolor=GREEN, alpha=0.13,
                       edgecolor=GREEN, lw=1.2, zorder=2))

# Block sites: x_r (block coordinate, large dot) and the other three sites.
ax.scatter([1], [1], s=70, color=VERM, zorder=4)
ax.scatter([1, 2, 2], [2, 1, 2], s=22, color=VERM, zorder=4)

lab = dict(fontsize=9.5, color="k", zorder=5)
ax.text(0.92, 0.68, r"$x_\mu+\eta^{(0)}_\mu$", ha="right", va="top", **lab)
ax.text(0.88, 2.26, r"$x_\mu+\eta^{(1)}_\mu$", ha="right", va="bottom", **lab)
ax.text(2.12, 0.68, r"$x_\mu+\eta^{(2)}_\mu$", ha="left", va="top", **lab)
ax.text(2.12, 2.26, r"$x_\mu+\eta^{(3)}_\mu$", ha="left", va="bottom", **lab)

# Legend of the eta^(i) offsets.
entries = [r"$\eta^{(0)}_\mu=(0,0)$", r"$\eta^{(1)}_\mu=(0,1)$",
           r"$\eta^{(2)}_\mu=(1,0)$", r"$\eta^{(3)}_\mu=(1,1)$"]
for j, e in enumerate(entries):
    ax.text(4.15, 2.55 - 0.62 * j, e, fontsize=10, ha="left", va="center")

ax.set_xlim(-1.2, 6.3)
ax.set_ylim(-0.6, 3.6)

fig.savefig("../fig-redraw-072.pdf")
fig.savefig("../fig-redraw-072.png", dpi=200)
print("done 072")
