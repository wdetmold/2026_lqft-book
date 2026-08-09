"""Redraw of fig-notes-019: domain-wall mass profile M(s) = m sgn(s) (red)
along the fifth dimension and the massless chiral mode
b0(s) = N exp(-m|s|) bound to the defect at s = 0 (blue), for an infinite
fifth dimension."""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np

RED = "#D55E00"
BLUE = "#0072B2"

m, A = 1.0, 1.65
s = np.linspace(-4.2, 4.2, 400)

fig, ax = plt.subplots(figsize=(4.6, 2.9))
ax.axis("off")

# axes: s axis as an arrow, vertical guide at the defect s = 0
ax.annotate("", xy=(4.8, 0), xytext=(-4.5, 0),
            arrowprops=dict(arrowstyle="-|>", color="black", lw=0.9,
                            mutation_scale=12))
ax.plot([0, 0], [-1.5, 2.0], color="0.65", lw=0.8, zorder=1)
ax.text(4.85, -0.12, r"$s$", fontsize=12, ha="left", va="top")

# M(s) = m sgn(s)
ax.plot([-4.2, 0], [-m, -m], color=RED, lw=2.2, solid_capstyle="round",
        zorder=3)
ax.plot([0, 0], [-m, m], color=RED, lw=2.2, zorder=3)
ax.plot([0, 4.2], [m, m], color=RED, lw=2.2, solid_capstyle="round",
        zorder=3)
ax.text(3.0, m + 0.14, r"$M(s)$", color=RED, fontsize=12,
        ha="center", va="bottom")
ax.text(4.35, m, r"$+m$", color=RED, fontsize=10, ha="left", va="center")
ax.text(-4.35, -m, r"$-m$", color=RED, fontsize=10, ha="right", va="center")

# massless mode bound to the wall
ax.plot(s, A * np.exp(-m * np.abs(s)), color=BLUE, lw=2.0, zorder=4)
ax.text(-1.15, 1.05, r"$b_0(s)$", color=BLUE, fontsize=12,
        ha="right", va="bottom")

ax.set_xlim(-5.6, 5.4)
ax.set_ylim(-1.6, 2.1)

fig.tight_layout(pad=0.2)
fig.savefig("../fig-redraw-019.pdf")
fig.savefig("../fig-redraw-019.png", dpi=200)
print("done 019")
