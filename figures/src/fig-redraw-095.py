"""Redraw of fig-notes-095 (vector note page, CropBox = the SU(2)/SU(3)
schematic phase diagram in the (beta, T) plane): deconfined phase above a
gently falling transition line (2nd order for SU(2), 1st order for SU(3)),
confined phase below. Within the confined phase a dotted line at beta_r
marks the roughening transition where the strong coupling expansion breaks
down; the highlighted beta -> infinity edge is the continuum limit,
xi -> infinity. Companion of fig-redraw-059 (U(1) case).
"""
import matplotlib.pyplot as plt

plt.style.use("lqftbook.mplstyle")

import numpy as np

BLUE = "#0072B2"
HL = "#a8d5f0"  # light-blue highlight of the xi -> infinity edge

fig, ax = plt.subplots(figsize=(4.6, 3.0))
ax.axis("off")

# axes as arrows
ax.annotate("", xy=(10.5, 0), xytext=(-0.15, 0),
            arrowprops=dict(arrowstyle="-|>", color="black", lw=1.0,
                            mutation_scale=14))
ax.annotate("", xy=(0, 5.9), xytext=(0, -0.15),
            arrowprops=dict(arrowstyle="-|>", color="black", lw=1.0,
                            mutation_scale=14))
ax.text(10.55, -0.10, r"$\beta$", fontsize=13, ha="left", va="center")
ax.text(-0.35, 5.75, r"$T$", fontsize=13, ha="right", va="top")

# beta -> infinity edge, highlighted: the continuum limit, xi -> infinity
ax.plot([9.5, 9.5], [0, 5.3], color=HL, lw=7, solid_capstyle="round",
        zorder=1)
ax.plot([9.5, 9.5], [0, 5.3], color="black", lw=0.8, zorder=2)

# deconfinement transition line, gently falling towards large beta
xt = np.linspace(0, 9.5, 200)
yt = 4.05 - 0.55 * xt / 9.5 - 0.25 * (xt / 9.5) ** 2
ax.plot(xt, yt, color=BLUE, lw=1.8, zorder=3)

# roughening transition: dotted line at beta_r inside the confined phase
ax.plot([4.5, 4.5], [0, 2.6], color=BLUE, lw=1.4, ls=(0, (1, 2.2)),
        zorder=3)
ax.text(4.5, -0.28, r"$\beta_r$", ha="center", va="top", fontsize=12)

# phase labels
ax.text(4.7, 4.75, "deconfined", fontsize=10, ha="center", va="center")
ax.text(2.2, 1.55, "confined", fontsize=10, ha="center", va="center")
ax.text(6.9, 1.45, "confined", fontsize=10, ha="center", va="center")

# order of the transition, arrow to the transition line
ax.annotate("2nd order $SU(2)$\n1st order $SU(3)$",
            xy=(0.85, 3.85), xytext=(-3.5, 3.15),
            fontsize=9, ha="left", va="center", linespacing=1.5,
            arrowprops=dict(arrowstyle="-|>", color="black", lw=1.0,
                            mutation_scale=12,
                            connectionstyle="arc3,rad=-0.25"))

# xi -> infinity at the beta -> infinity edge (two arrows, as in the notes)
ax.text(10.35, 5.0, r"$\xi \to \infty$", fontsize=11, ha="left",
        va="center")
ax.annotate("", xy=(9.62, 4.55), xytext=(10.55, 4.95),
            arrowprops=dict(arrowstyle="-|>", color="black", lw=1.0,
                            mutation_scale=12))
ax.annotate("", xy=(9.68, 2.15), xytext=(10.9, 4.6),
            arrowprops=dict(arrowstyle="-|>", color="black", lw=1.0,
                            mutation_scale=12,
                            connectionstyle="arc3,rad=-0.35"))

ax.set_xlim(-3.7, 11.9)
ax.set_ylim(-0.8, 6.1)

fig.tight_layout(pad=0.2)
fig.savefig("../fig-redraw-095.pdf")
fig.savefig("../fig-redraw-095.png", dpi=200)
print("done 095")
