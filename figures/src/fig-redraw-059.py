"""Redraw of fig-notes-059: schematic phase diagram of the compact U(1)
lattice gauge theory in the (beta, T) plane. Confined phase at strong
coupling, Coulomb phase at weak coupling. The transition line is second
order (xi -> infinity) at high T and turns first order below the marked
point, meeting the T = 0 axis at beta ~ 1.01, where the strong coupling
expansion breaks down."""
import matplotlib.pyplot as plt
plt.style.use("lqftbook.mplstyle")

import numpy as np
from scipy.interpolate import PchipInterpolator

BLUE = "#0072B2"
HL = "#a8d5f0"  # light-blue highlight of the second-order segment

fig, ax = plt.subplots(figsize=(4.6, 3.2))
ax.axis("off")

# axes as arrows
ax.annotate("", xy=(10.5, 0), xytext=(-0.15, 0),
            arrowprops=dict(arrowstyle="-|>", color="black", lw=1.0,
                            mutation_scale=14))
ax.annotate("", xy=(0, 5.7), xytext=(0, -0.15),
            arrowprops=dict(arrowstyle="-|>", color="black", lw=1.0,
                            mutation_scale=14))
ax.text(10.55, -0.10, r"$\beta$", fontsize=13, ha="left", va="center")
ax.text(-0.35, 5.55, r"$T$", fontsize=13, ha="right", va="top")

# beta -> infinity edge
ax.plot([9.5, 9.5], [0, 5.2], color="black", lw=0.8)

# transition line: second order above the marked point, first order below
x2 = np.linspace(0.3, 5.4, 150)
c2 = PchipInterpolator([0.3, 1.5, 3.0, 4.5, 5.4],
                       [3.90, 3.55, 2.95, 2.30, 1.90])
x1 = np.linspace(5.4, 6.0, 60)
c1 = PchipInterpolator([5.4, 5.8, 6.0], [1.90, 0.90, 0.0])

ax.plot(x2, c2(x2), color=HL, lw=7, solid_capstyle="round", zorder=1)
ax.plot(x2, c2(x2), color=BLUE, lw=1.8, zorder=3)
ax.plot(x1, c1(x1), color=BLUE, lw=1.8, zorder=3)
ax.plot([5.4], [1.90], marker="o", ms=6, color=BLUE, zorder=4)

# tick at beta ~ 1.01 where the line meets the T = 0 axis
ax.plot([6.0, 6.0], [0, 0.12], color="black", lw=0.9)
ax.text(6.0, -0.28, r"$1.01$", ha="center", va="top", fontsize=10)
ax.text(0.0, -0.28, r"$0$", ha="center", va="top", fontsize=12)
ax.text(9.5, -0.28, r"$\infty$", ha="center", va="top", fontsize=12)

# labels and annotations
ax.text(2.0, 3.75, "2nd order", fontsize=10, rotation=-17,
        ha="center", va="bottom")
ax.annotate(r"$\xi \to \infty$", xy=(3.45, 2.83), xytext=(4.6, 3.9),
            fontsize=11, ha="left", va="center",
            arrowprops=dict(arrowstyle="-|>", color="black", lw=1.0,
                            mutation_scale=12))
ax.text(1.8, 1.0, "confined", fontsize=10, ha="center", va="center")
ax.text(7.5, 2.1, "Coulomb", fontsize=10, ha="center", va="center")
ax.annotate("1st order?", xy=(6.0, 0.45), xytext=(7.5, 1.0),
            fontsize=10, ha="left", va="center",
            arrowprops=dict(arrowstyle="-|>", color="black", lw=1.0,
                            mutation_scale=12))

ax.set_xlim(-0.9, 11.1)
ax.set_ylim(-0.9, 5.9)

fig.tight_layout(pad=0.2)
fig.savefig("../fig-redraw-059.pdf")
fig.savefig("../fig-redraw-059.png", dpi=200)
print("done 059")
