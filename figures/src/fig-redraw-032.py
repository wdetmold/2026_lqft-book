"""Redraw of fig-notes-032: decay, in the centre-of-mass frame, of a kaon
at rest to two back-to-back pions through the four-quark effective
operator O_4.
"""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np
from matplotlib.patches import Circle

BLUE = "#0072B2"
INK = "0.15"

fig, ax = plt.subplots(figsize=(4.6, 3.0))
ax.set_aspect("equal")
ax.axis("off")

vtx = np.array([0.0, 0.0])

# kaon line (at rest) into the vertex
ax.plot([-2.1, -0.05], [0.0, 0.0], color=BLUE, lw=1.6,
        solid_capstyle="round", zorder=2)
ax.text(-2.25, 0.0, r"$K(\vec{p} = 0)$", ha="right", va="center",
        fontsize=13, color=INK)

# two pion lines out of the vertex, back to back momenta
ax.plot([0.05, 1.9], [0.03, 0.78], color=BLUE, lw=1.6,
        solid_capstyle="round", zorder=2)
ax.plot([0.05, 1.9], [-0.03, -0.78], color=BLUE, lw=1.6,
        solid_capstyle="round", zorder=2)
ax.text(2.05, 0.82, r"$\pi(\hat{p})$", ha="left", va="center",
        fontsize=13, color=INK)
ax.text(2.05, -0.82, r"$\pi(-\hat{p})$", ha="left", va="center",
        fontsize=13, color=INK)

# four-quark operator insertion
ax.add_patch(Circle(vtx, 0.16, facecolor=INK, edgecolor=INK, zorder=4))
ax.text(-0.02, 0.32, r"$\mathcal{O}_4$", ha="right", va="bottom",
        fontsize=13, color=INK)

ax.set_xlim(-4.3, 3.4)
ax.set_ylim(-1.2, 1.25)

fig.savefig("../fig-redraw-032.pdf")
fig.savefig("../fig-redraw-032.png", dpi=200)
print("done")
